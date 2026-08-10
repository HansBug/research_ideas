"""LG-G1 safe local trace export helpers for LangGraph runs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from archive.agent_loop_method.langgraph.instrumentation.common import _hash_file, _hash_payload
from archive.agent_loop_method.langgraph.instrumentation.operator_stream import _LG_D1_ACADEMIC_EVIDENCE_SOURCES, _LG_D1_SECRET_VALUE_PATTERNS
from archive.agent_loop_method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult, LoopConfig

LG_G1_TRACE_EXPORT_SCHEMA_VERSION = "lg-g1.safe-trace-export.v1"

LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER = "lg_g1_optional_trace_export"

_LG_G1_ACADEMIC_EVIDENCE_SOURCES = list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES)

_LG_G1_UNSAFE_TRACE_SOURCE_KEYS = {
    "prompt",
    "raw_prompt",
    "raw_output",
    "raw_response",
    "provider_response",
    "message",
    "messages",
    "choice",
    "choices",
    "content",
    "raw_nl",
    "input_nl",
    "nl",
    "api_key",
    "apikey",
    "authorization",
    "headers",
    "bearer",
    "password",
    "secret",
    "token",
    "access_token",
    "refresh_token",
}

def _lg_g1_trace_export_policy(config: LoopConfig) -> dict[str, Any]:
    """Return LG-G1 opt-in trace export policy from ``record_policy``.

    LG-G1 is deliberately optional and default-off.  Keeping the switch inside
    ``record_policy`` avoids a new public runtime backend/config branch and
    keeps the implementation small.
    """

    raw = config.record_policy.get("lg_g1_trace_export") if isinstance(config.record_policy, dict) else None
    raw = raw if isinstance(raw, dict) else {}
    raw_enabled = raw.get("enabled", False)
    if not isinstance(raw_enabled, bool):
        raise ValueError("LG-G1 trace export enabled must be a boolean")
    enabled = raw_enabled
    mode = str(raw.get("mode") or ("local" if enabled else "disabled"))
    if not enabled:
        mode = "disabled"
    if mode not in {"disabled", "local"}:
        raise ValueError("LG-G1 trace export mode must be 'disabled' or 'local'")
    if enabled and mode == "disabled":
        raise ValueError("LG-G1 enabled trace export requires mode 'local'")
    return {
        "schema_version": LG_G1_TRACE_EXPORT_SCHEMA_VERSION,
        "enabled": enabled,
        "mode": mode,
        "external_trace_status": "disabled_not_configured",
        "default_off": not enabled,
        "redaction_policy": "hash_length_ids_counts_only",
    }

def _lg_g1_has_secret_like_value(value: Any) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            key_norm = re.sub(r"[^a-z0-9]+", "_", str(key).lower()).strip("_")
            if (
                key_norm in _LG_G1_UNSAFE_TRACE_SOURCE_KEYS
                or any(fragment in key_norm for fragment in ("api_key", "apikey", "bearer", "password", "secret"))
                or key_norm.endswith("_token")
            ):
                return True
            if _lg_g1_has_secret_like_value(nested):
                return True
        return False
    if isinstance(value, (list, tuple, set)):
        return any(_lg_g1_has_secret_like_value(item) for item in value)
    return isinstance(value, str) and any(pattern.search(value) for pattern in _LG_D1_SECRET_VALUE_PATTERNS)

def _lg_g1_stage_ids(rows: list[Any]) -> list[str]:
    return [str(item.get("stage_id") if isinstance(item, dict) else getattr(item, "stage_id", "")) for item in rows]

def _lg_g1_safe_trace_payload(record: Any, *, run_record_path: str | Path) -> dict[str, Any]:
    final_artifacts = record.final_artifacts if isinstance(getattr(record, "final_artifacts", None), dict) else {}
    if _lg_g1_has_secret_like_value(final_artifacts):
        raise ValueError("LG-G1 trace export refused secret-like final_artifacts payload")
    operator = final_artifacts.get("operator_log") if isinstance(final_artifacts.get("operator_log"), dict) else {}
    runtime_trace = final_artifacts.get("langgraph_runtime_trace") if isinstance(final_artifacts.get("langgraph_runtime_trace"), dict) else {}
    return {
        "schema_version": LG_G1_TRACE_EXPORT_SCHEMA_VERSION,
        "instrumentation_layer": LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER,
        "external_upload_performed": False,
        "external_trace_status": "disabled_not_configured",
        "redaction_policy": "hash_length_ids_counts_only",
        "snapshot_phase": "before_lg_g1_export_artifact_append",
        "counts_scope": "canonical_record_before_export_artifact_append",
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_G1_ACADEMIC_EVIDENCE_SOURCES),
        "run": {
            "run_id_hash": _hash_payload(str(record.run_id)),
            "run_id_length": len(str(record.run_id)),
            "record_status": record.status,
            "run_record_path_hash": _hash_payload(str(run_record_path)),
        },
        "counts": {
            "stage_records": len(record.stage_records),
            "llm_interactions": len(record.llm_interactions),
            "fix_log": len(record.fix_log),
            "scenario_history": len(record.scenario_history),
            "repair_history": len(record.repair_history),
            "logs": len(record.logs),
        },
        "stage_sequence": _lg_g1_stage_ids(record.stage_records),
        "hashes": {
            "stage_records_hash": _hash_payload(record.stage_records),
            "llm_interactions_hash": _hash_payload(record.llm_interactions),
            "fix_log_hash": _hash_payload(record.fix_log),
            "scenario_history_hash": _hash_payload(record.scenario_history),
            "repair_history_hash": _hash_payload(record.repair_history),
            "final_dsl_hash": final_artifacts.get("final_dsl_hash"),
            "operator_log_hash": operator.get("operator_log_hash"),
            "langgraph_node_trace_hash": runtime_trace.get("node_trace_hash"),
        },
        "verdict_summary": {
            "verdict": final_artifacts.get("verdict"),
            "verdict_source_stage_id": final_artifacts.get("verdict_source_stage_id"),
            "agent_loop_result_status": final_artifacts.get("agent_loop_result_status"),
            "main_result_eligible": final_artifacts.get("main_result_eligible"),
            "oracle_weak": final_artifacts.get("oracle_weak"),
        },
    }

def _write_lg_g1_trace_artifact(record: Any, *, run_record_path: str | Path) -> dict[str, Any]:
    path = Path(run_record_path)
    run_id_hash = _hash_payload(str(record.run_id))
    trace_file = f"lg_g1_trace.{run_id_hash.removeprefix('sha256:')[:12]}.json"
    trace_path = path.with_name(trace_file)
    payload = _lg_g1_safe_trace_payload(record, run_record_path=path)
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"
    if _lg_g1_has_secret_like_value(payload):
        raise ValueError("LG-G1 trace export refused secret-like trace payload")
    trace_path.write_text(encoded, encoding="utf-8")
    return {
        "schema_version": LG_G1_TRACE_EXPORT_SCHEMA_VERSION,
        "instrumentation_layer": LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER,
        "trace_artifact_name": trace_file,
        "trace_path_hash": _hash_payload(str(trace_path)),
        "trace_hash": _hash_file(trace_path),
        "trace_payload_hash": _hash_payload(payload),
        "redaction_policy": "hash_length_ids_counts_only",
        "external_upload_performed": False,
        "external_trace_status": "disabled_not_configured",
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_G1_ACADEMIC_EVIDENCE_SOURCES),
    }

def _augment_run_record_with_lg_g1_trace_export(
    result: AgentLoopResult,
    *,
    enabled: bool,
    mode: str,
) -> None:
    if not enabled:
        return
    if not result.run_record_path:
        raise ValueError("LG-G1 local trace export requires a persisted run_record_path")
    if mode != "local":
        raise ValueError("LG-G1 trace export currently supports only local mode")
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    record.environment["lg_g1_trace_export_enabled"] = True
    record.environment["lg_g1_trace_export_schema_version"] = LG_G1_TRACE_EXPORT_SCHEMA_VERSION
    record.environment["lg_g1_trace_export_instrumentation_layer"] = LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER
    record.environment["lg_g1_external_trace_status"] = "disabled_not_configured"
    record.run_config["lg_g1_trace_export_enabled"] = True
    record.run_config["lg_g1_trace_export_mode"] = mode
    record.run_config["lg_g1_external_trace_status"] = "disabled_not_configured"
    artifact = _write_lg_g1_trace_artifact(record, run_record_path=path)
    record.environment["lg_g1_trace_export_status"] = "local_enabled"
    record.environment["lg_g1_trace_export_hash"] = artifact["trace_hash"]
    record.environment["lg_g1_trace_export_path_hash"] = artifact["trace_path_hash"]
    record.final_artifacts["lg_g1_trace_export"] = artifact
    record.logs.append(
        {
            "event": "lg_g1_trace_export",
            "instrumentation_layer": LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER,
            "status": "local_enabled",
            "trace_hash": artifact["trace_hash"],
            "does_not_replace_academic_evidence": True,
        }
    )
    write_agent_loop_run_record(record, path)

