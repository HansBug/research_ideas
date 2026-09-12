"""LG-D1 operator stream helpers for the LangGraph runtime.

This module owns prompt-safe operator events, JSONL stream summaries, and the
tee-style graph stream runner.  It does not import ``archive.agent_loop_method.langgraph_runtime``;
the runtime module remains the compatibility facade.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from archive.agent_loop_method.langgraph.registry import build_langgraph_node_registry as _build_registry
from archive.agent_loop_method.langgraph.subgraphs.context_engineering import LG_C2_CONTEXT_NODE_IDS, LG_C2_CONTEXT_SUBGRAPH_ID
from archive.agent_loop_method.langgraph.instrumentation.common import _hash_file, _hash_payload, _jsonable
from archive.agent_loop_method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult
from archive.agent_loop_method.staged_runtime import _RunState, _hash_text, _utc_now
from archive.agent_loop_method.stages.ids import StageId

LG_D1_OPERATOR_EVENT_SCHEMA_VERSION = "lg-d1.operator-event.v1"

LG_D1_STREAM_SUMMARY_SCHEMA_VERSION = "lg-d1.stream-summary.v1"

LG_D1_INSTRUMENTATION_LAYER = "langgraph_streaming"

_LG_D1_FORBIDDEN_OPERATOR_PAYLOAD_KEYS = {
    "messages",
    "message",
    "prompt",
    "raw_prompt",
    "raw_output",
    "chunk_text",
    "delta_text",
    "completion_text",
    "content",
    "text",
    "response_text",
    "output_text",
    "choices",
    "delta",
    "api_key",
    "apikey",
    "authorization",
    "headers",
    "token",
    "access_token",
    "refresh_token",
    "bearer_token",
}

_LG_D1_FORBIDDEN_OPERATOR_KEY_FRAGMENTS = ("api_key", "apikey", "secret", "credential", "password", "bearer", "token")

_LG_D1_FORBIDDEN_OPERATOR_KEY_SUFFIXES = (
    "_api_key",
    "_secret",
    "_credential",
    "_password",
    "_bearer",
    "_token",
)

_LG_D1_FORBIDDEN_OPERATOR_COMPACT_KEYS = {
    "apikey",
    "authorization",
    "accesstoken",
    "refreshtoken",
    "bearertoken",
    "token",
    "headers",
}

_LG_D1_SECRET_VALUE_PATTERNS: tuple[re.Pattern[str], ...] = (
    re.compile(r"sk-[A-Za-z0-9][A-Za-z0-9_-]{7,}"),
    re.compile(r"gh[opsur]_[A-Za-z0-9_]{8,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{8,}"),
    re.compile(r"Bearer\s+[A-Za-z0-9._\-]{12,}", re.IGNORECASE),
    re.compile(r"(?i)(?:secret|token|api[_-]?key|password)[A-Za-z0-9._:\-]{4,}"),
)

_LG_D1_LLM_PROGRESS_EVENT_TYPES = {"llm_stream_progress", "llm_request_progress"}

_LG_D1_LLM_PROGRESS_ALLOWED_PAYLOAD_KEYS = {
    "interaction_index",
    "stage_id",
    "stream",
    "stream_include_usage_requested",
    "token_usage_available",
    "stream_usage_zero_reported",
    "chunk_count",
    "first_chunk_seconds",
    "elapsed_seconds",
    "prompt_chars",
    "completion_chars",
    "estimated_prompt_tokens",
    "estimated_completion_tokens",
    "estimated_total_tokens",
    "token_usage_estimation_method",
    "attempt_count",
    "attempt_stream_observed",
    "usage_payload_hash",
}

_LG_D1_ACADEMIC_EVIDENCE_SOURCES = [
    "AgentLoopRunRecord.stage_records",
    "AgentLoopRunRecord.llm_interactions",
    "AgentLoopRunRecord.fix_log",
    "AgentLoopRunRecord.scenario_history",
    "AgentLoopRunRecord.final_artifacts.final_dsl",
]

def _sanitize_lg_d1_operator_payload(value: Any) -> tuple[Any, int]:
    """Return a JSON-safe operator payload without raw prompt/output fields.

    LG-D1's operator stream is a terminal/debugging aid, not a new raw evidence
    store.  It may carry sizes, hashes, timings and verdicts, but never prompts,
    raw LLM outputs, chunk text, headers or API-key-like fields.
    """

    if isinstance(value, dict):
        sanitized: dict[str, Any] = {}
        omitted = 0
        for key, nested in value.items():
            key_text = str(key)
            key_norm = key_text.lower()
            key_compact = re.sub(r"[^a-z0-9]", "", key_norm)
            if key_norm in _LG_D1_FORBIDDEN_OPERATOR_PAYLOAD_KEYS or any(
                fragment in key_norm for fragment in _LG_D1_FORBIDDEN_OPERATOR_KEY_FRAGMENTS
            ) or any(
                key_norm.endswith(suffix) for suffix in _LG_D1_FORBIDDEN_OPERATOR_KEY_SUFFIXES
            ) or key_compact in _LG_D1_FORBIDDEN_OPERATOR_COMPACT_KEYS or key_compact.startswith("raw"):
                omitted += 1
                continue
            if any(fragment in key_compact for fragment in ("token", "secret", "password", "apikey", "credential", "bearer")):
                omitted += 1
                continue
            safe_nested, nested_omitted = _sanitize_lg_d1_operator_payload(nested)
            sanitized[key_text] = safe_nested
            omitted += nested_omitted
        return sanitized, omitted
    if isinstance(value, (list, tuple, set)):
        rows = []
        omitted = 0
        for item in value:
            safe_item, item_omitted = _sanitize_lg_d1_operator_payload(item)
            rows.append(safe_item)
            omitted += item_omitted
        return rows, omitted
    if isinstance(value, str) and any(pattern.search(value) for pattern in _LG_D1_SECRET_VALUE_PATTERNS):
        return "<omitted:secret-like-value>", 1
    return _jsonable(value), 0

def _sanitize_lg_d1_llm_progress_payload(value: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Allowlist LLM progress payload fields so chunks/messages never persist."""

    sanitized: dict[str, Any] = {}
    omitted = 0
    for key, nested in value.items():
        key_text = str(key)
        if key_text not in _LG_D1_LLM_PROGRESS_ALLOWED_PAYLOAD_KEYS:
            _, nested_omitted = _sanitize_lg_d1_operator_payload(nested)
            omitted += 1 + nested_omitted
            continue
        safe_nested, nested_omitted = _sanitize_lg_d1_operator_payload(nested)
        sanitized[key_text] = safe_nested
        omitted += nested_omitted
    return sanitized, omitted

def build_lg_d1_operator_event(
    *,
    run_id: str,
    event_type: str,
    node: str | None = None,
    stage_id: str | None = None,
    payload: dict[str, Any] | None = None,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Build one LG-D1 JSONL-safe operator event."""

    if event_type in _LG_D1_LLM_PROGRESS_EVENT_TYPES and isinstance(payload, dict):
        safe_payload, omitted_count = _sanitize_lg_d1_llm_progress_payload(payload)
    else:
        safe_payload, omitted_count = _sanitize_lg_d1_operator_payload(payload or {})
    if omitted_count:
        if not isinstance(safe_payload, dict):
            safe_payload = {"value": safe_payload}
        safe_payload["omitted_raw_content_field_count"] = omitted_count
    event = {
        "schema_version": LG_D1_OPERATOR_EVENT_SCHEMA_VERSION,
        "run_id": str(run_id),
        "event_type": str(event_type),
        "timestamp": timestamp or _utc_now(),
        "node": node,
        "stage_id": stage_id,
        "instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
        "payload": safe_payload,
        "payload_hash": _hash_payload(safe_payload),
    }
    # Validate strict JSON compatibility and reject NaN/Infinity before a long
    # real run can produce an unreadable operator log.
    json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    return event

def _append_lg_d1_operator_event(
    graph_state: _GraphLoopState,
    *,
    event_type: str,
    node: str | None = None,
    stage_id: str | None = None,
    payload: dict[str, Any] | None = None,
) -> None:
    if not bool(graph_state.get("operator_stream_enabled", True)):
        return
    runtime_state = graph_state.get("runtime_state")
    run_id = getattr(runtime_state, "run_id", None) or graph_state.get("run_id") or ""
    if not run_id:
        return
    events = list(graph_state.get("operator_events", []) or [])
    events.append(
        build_lg_d1_operator_event(
            run_id=str(run_id),
            event_type=event_type,
            node=node,
            stage_id=stage_id,
            payload=payload or {},
        )
    )
    graph_state["operator_events"] = events

def _node_stage_ids_by_node_id() -> dict[str, list[str]]:
    registry = _build_registry(context_subgraph_id=LG_C2_CONTEXT_SUBGRAPH_ID, context_node_ids=LG_C2_CONTEXT_NODE_IDS)
    return {str(node.get("node_id") or ""): [str(item) for item in node.get("stage_ids", [])] for node in registry["nodes"]}

def _safe_node_exit_payload(node_state: dict[str, Any]) -> dict[str, Any]:
    runtime_state = node_state.get("runtime_state")
    payload: dict[str, Any] = {
        "state_keys": sorted(str(key) for key in node_state.keys() if key not in {"runtime_state", "nl"}),
    }
    if isinstance(runtime_state, _RunState):
        payload.update(
            {
                "stage_count": len(runtime_state.stage_records),
                "iteration_count": len(runtime_state.iteration_records),
                "repair_count": len(runtime_state.repair_history),
                "record_status": runtime_state.final_record_status,
                "result_status": runtime_state.result_status,
                "verdict": runtime_state.final_verdict,
                "verdict_source_stage_id": runtime_state.verdict_source_stage_id,
                "current_dsl_hash": _hash_text(runtime_state.current_dsl),
            }
        )
    if isinstance(node_state.get("iteration"), int):
        payload["iteration"] = node_state.get("iteration")
    return payload

def _llm_stream_usage_from_interactions(llm_interactions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, interaction in enumerate(llm_interactions):
        if not isinstance(interaction, dict):
            continue
        usage = interaction.get("usage") if isinstance(interaction.get("usage"), dict) else {}
        attempts = interaction.get("attempts") if isinstance(interaction.get("attempts"), list) else []
        attempt_stream_flags: list[bool] = []
        for attempt in attempts:
            if isinstance(attempt, dict):
                attempt_usage = attempt.get("usage") if isinstance(attempt.get("usage"), dict) else {}
                if isinstance(attempt_usage.get("stream"), bool):
                    attempt_stream_flags.append(bool(attempt_usage.get("stream")))
        stream_value = usage.get("stream")
        stream_observed = bool(stream_value) if isinstance(stream_value, bool) else (True if any(attempt_stream_flags) else None)
        rows.append(
            {
                "interaction_index": index,
                "stage_id": str(interaction.get("stage_id") or ""),
                "stream": stream_observed,
                "stream_include_usage_requested": usage.get("stream_include_usage_requested"),
                "token_usage_available": usage.get("token_usage_available"),
                "stream_usage_zero_reported": usage.get("stream_usage_zero_reported"),
                "chunk_count": usage.get("chunk_count"),
                "first_chunk_seconds": usage.get("first_chunk_seconds"),
                "elapsed_seconds": usage.get("elapsed_seconds"),
                "prompt_chars": usage.get("prompt_chars"),
                "completion_chars": usage.get("completion_chars"),
                "estimated_prompt_tokens": usage.get("estimated_prompt_tokens"),
                "estimated_completion_tokens": usage.get("estimated_completion_tokens"),
                "estimated_total_tokens": usage.get("estimated_total_tokens"),
                "attempt_count": len(attempts),
                "attempt_stream_observed": any(attempt_stream_flags) if attempt_stream_flags else None,
                "usage_payload_hash": _hash_payload(usage),
            }
        )
    return rows

def lg_d1_llm_stream_runtime_metadata(
    *,
    real_llm_provider_api: bool,
    llm_interactions: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Return prompt-safe LG-D1 metadata about provider stream discipline."""

    from archive.agent_loop_method.gpt_client import get_stream_enabled, get_stream_include_usage_enabled

    stream_rows = _llm_stream_usage_from_interactions(llm_interactions or [])
    observed_values = [row.get("stream") for row in stream_rows if isinstance(row.get("stream"), bool)]
    observed = (all(bool(value) for value in observed_values) if observed_values else None)
    return {
        "llm_stream_required": True,
        "llm_stream_required_reason": (
            "PR-E1/LG-D1 real-provider runs must keep stream enabled so long structured generations "
            "remain auditable and provider/proxy stalls are classified as invalid infrastructure failures."
        ),
        "llm_stream_config_enabled": bool(get_stream_enabled()),
        "llm_stream_include_usage_config_enabled": bool(get_stream_include_usage_enabled()),
        "llm_stream_observed": observed,
        "llm_stream_observation_source": "llm_interactions.usage.stream" if observed_values else "pending_llm_interactions",
        "real_llm_provider_api": bool(real_llm_provider_api),
        "llm_stream_interaction_count": len(stream_rows),
    }

def _build_lg_d1_stream_summary(events: list[dict[str, Any]]) -> dict[str, Any]:
    # Keep this sequence aligned with the durable LangGraph node trace.
    # LG-B1 validation subgraphs deliberately use ``subgraph_enter`` /
    # ``subgraph_exit`` in addition to ordinary ``node_enter`` events, and
    # LG-D1 operator logs must not collapse those academic orchestration
    # boundaries away.  Synthetic ``node_exit`` events from tee streaming remain
    # excluded because they are operator-progress signals rather than graph-trace
    # entries.
    node_sequence = [
        str(event.get("node"))
        for event in events
        if event.get("event_type") in {"node_enter", "subgraph_enter", "subgraph_exit"} and event.get("node")
    ]
    stage_sequence = [
        str(event.get("stage_id"))
        for event in events
        if event.get("event_type") == "stage_result" and event.get("stage_id")
    ]
    terminal_events = [event for event in events if event.get("event_type") == "terminal_verdict"]
    terminal_payload = terminal_events[-1].get("payload", {}) if terminal_events else {}
    llm_events = [event for event in events if event.get("event_type") in {"llm_stream_progress", "llm_request_progress"}]
    stream_values = [
        event.get("payload", {}).get("stream")
        for event in llm_events
        if isinstance(event.get("payload", {}).get("stream"), bool)
    ]
    chunk_total = 0
    for event in llm_events:
        value = event.get("payload", {}).get("chunk_count")
        if isinstance(value, int) and not isinstance(value, bool):
            chunk_total += value
    return {
        "schema_version": LG_D1_STREAM_SUMMARY_SCHEMA_VERSION,
        "run_id": str(events[0].get("run_id")) if events else "",
        "instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
        "operator_event_count": len(events),
        "node_sequence": node_sequence,
        "stage_sequence": stage_sequence,
        "final_verdict": terminal_payload.get("verdict"),
        "record_status": terminal_payload.get("record_status"),
        "result_status": terminal_payload.get("result_status"),
        "verdict_source_stage_id": terminal_payload.get("verdict_source_stage_id"),
        "run_record_path_hash": terminal_payload.get("run_record_path_hash"),
        "llm_stream_observed": (all(bool(value) for value in stream_values) if stream_values else None),
        "llm_stream_chunk_count_total": chunk_total,
        "llm_interaction_event_count": len(llm_events),
        "event_type_counts": {
            event_type: sum(1 for event in events if event.get("event_type") == event_type)
            for event_type in sorted({str(event.get("event_type")) for event in events})
        },
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
    }

def reconstruct_lg_d1_stream_summary_from_jsonl(path: str | Path) -> dict[str, Any]:
    """Reconstruct LG-D1 progress summary from a tee-able JSONL operator log."""

    events: list[dict[str, Any]] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("schema_version") != LG_D1_OPERATOR_EVENT_SCHEMA_VERSION:
            raise ValueError(f"unsupported LG-D1 operator event schema: {event.get('schema_version')}")
        events.append(event)
    return _build_lg_d1_stream_summary(events)

def _operator_event_key(event: dict[str, Any]) -> str:
    return json.dumps(event, ensure_ascii=False, sort_keys=True, default=str)

def _merge_operator_events(existing: list[dict[str, Any]], new_events: Any) -> list[dict[str, Any]]:
    merged = list(existing)
    seen = {_operator_event_key(event) for event in merged if isinstance(event, dict)}
    for event in new_events or []:
        if not isinstance(event, dict):
            continue
        key = _operator_event_key(event)
        if key in seen:
            continue
        merged.append(event)
        seen.add(key)
    return merged

def _primary_stage_id_for_node(node_id: str) -> str | None:
    stage_ids = _node_stage_ids_by_node_id().get(node_id, [])
    return stage_ids[0] if len(stage_ids) == 1 else None

def _node_for_stage(stage_id: str) -> str | None:
    for node_id, stage_ids in _node_stage_ids_by_node_id().items():
        if stage_id in stage_ids:
            return node_id
    return None

_REPAIR_STAGE_NODE_BY_STAGE_ID = {
    StageId.SD_8_FIX_PLAN.value: "repair_sd8_fix_requests",
    StageId.SL_9_REPAIR.value: "repair_sl9_repair",
    StageId.SD_10_REPAIR_REVIEW.value: "repair_sl10_review",
    StageId.SL_10_REPAIR_REVIEW.value: "repair_sl10_review",
    StageId.SC_11_ACCEPT_CANDIDATE.value: "repair_sc11_accept_candidate",
}

_OPERATOR_STAGE_FLOW_PAYLOAD_KEYS = {
    "graph_subgraph",
    "graph_node",
    "jump",
    "reason",
    "status",
    "ok",
    "decision",
    "target_resolved",
    "regression_detected",
    "drift_risk",
    "rework_attempt",
    "rework_locked",
    "batch_id",
    "request_count",
    "hard_block",
    "accepted_request_ids",
    "rejected_request_ids",
    "source",
    "source_stage",
    "plan_kind",
    "old_dsl_hash",
    "candidate_dsl_hash",
    "current_dsl_hash",
    "scenario_set_id",
    "oracle_weak",
}

def _flow_log_stage_rows_by_stage(record: Any) -> dict[str, list[dict[str, Any]]]:
    rows_by_stage: dict[str, list[dict[str, Any]]] = {}
    for item in getattr(record, "logs", []) or []:
        if not isinstance(item, dict):
            continue
        if item.get("event") not in {"stage_result", "llm_stage_result"}:
            continue
        stage_id = str(item.get("stage_id") or "")
        graph_node = str(item.get("graph_node") or "")
        if not stage_id or not graph_node:
            continue
        rows_by_stage.setdefault(stage_id, []).append(item)
    return rows_by_stage

def _operator_stage_flow_payload(row: dict[str, Any] | None) -> dict[str, Any]:
    if not row:
        return {}
    payload: dict[str, Any] = {"flow_event": str(row.get("event") or "")}
    for key in _OPERATOR_STAGE_FLOW_PAYLOAD_KEYS:
        if key in row:
            payload[key] = _jsonable(row.get(key))
    decisions = row.get("decisions")
    if isinstance(decisions, list):
        payload["decision_count"] = len(decisions)
        payload["decision_summaries"] = [
            {
                "request_id": str(item.get("request_id") or ""),
                "decision": str(item.get("decision") or ""),
                "waiver": bool(item.get("waiver")) if isinstance(item.get("waiver"), bool) else item.get("waiver"),
                "rework_locked": (
                    bool(item.get("rework_locked"))
                    if isinstance(item.get("rework_locked"), bool)
                    else item.get("rework_locked")
                ),
            }
            for item in decisions
            if isinstance(item, dict)
        ][:12]
    diff_summary = row.get("diff_summary")
    if isinstance(diff_summary, dict):
        payload["diff_summary"] = {
            key: _jsonable(diff_summary.get(key))
            for key in ("candidate_dsl_hash", "n_diff_lines", "changed")
            if key in diff_summary
        }
    for hash_key in ("local_check_evidence", "repair_memory", "evidence", "fix_plan"):
        if hash_key in row:
            payload[f"{hash_key}_hash"] = _hash_payload(row.get(hash_key))
    return payload

def _pop_precise_stage_node(
    rows_by_stage: dict[str, list[dict[str, Any]]],
    stage_id: str,
    *,
    default_node: str | None = None,
) -> tuple[str | None, dict[str, Any] | None]:
    rows = rows_by_stage.get(stage_id) or []
    if rows:
        row = rows.pop(0)
        return str(row.get("graph_node") or ""), row
    if stage_id in _REPAIR_STAGE_NODE_BY_STAGE_ID:
        return _REPAIR_STAGE_NODE_BY_STAGE_ID[stage_id], None
    return default_node if default_node is not None else _node_for_stage(stage_id), None

def _stage_result_operator_events(record: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    rows_by_stage = _flow_log_stage_rows_by_stage(record)
    for index, row in enumerate(record.stage_records):
        if not isinstance(row, dict):
            row = _jsonable(row)
        stage_id = str(row.get("stage_id") or "")
        stage_error = row.get("stage_error") or row.get("output_validation_error")
        node, flow_row = _pop_precise_stage_node(rows_by_stage, stage_id)
        stage_flow = _operator_stage_flow_payload(flow_row)
        events.append(
            build_lg_d1_operator_event(
                run_id=record.run_id,
                event_type="stage_result",
                node=node,
                stage_id=stage_id,
                payload={
                    "stage_index": index,
                    "stage_kind": row.get("stage_kind"),
                    "enabled": row.get("enabled"),
                    "ran": row.get("ran"),
                    "ok": row.get("ok"),
                    "status": str(row.get("status") or ""),
                    "stage_error_hash": _hash_text(str(stage_error)) if stage_error else None,
                    **({"stage_flow": stage_flow} if stage_flow else {}),
                },
            )
        )
    return events

def _llm_progress_operator_events(record: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    rows_by_stage = _flow_log_stage_rows_by_stage(record)
    for row in _llm_stream_usage_from_interactions(record.llm_interactions):
        stage_id = str(row.get("stage_id") or "")
        event_type = "llm_stream_progress" if row.get("stream") is True else "llm_request_progress"
        node, _flow_row = _pop_precise_stage_node(rows_by_stage, stage_id)
        events.append(
            build_lg_d1_operator_event(
                run_id=record.run_id,
                event_type=event_type,
                node=node,
                stage_id=stage_id,
                payload=row,
            )
        )
    return events

def _terminal_operator_event(record: Any, *, run_record_path_hash: str) -> dict[str, Any]:
    final_artifacts = record.final_artifacts if isinstance(record.final_artifacts, dict) else {}
    return build_lg_d1_operator_event(
        run_id=record.run_id,
        event_type="terminal_verdict",
        node="sc13_trace_audit",
        stage_id=StageId.SC_13_TRACE_AUDIT.value,
        payload={
            "verdict": final_artifacts.get("verdict"),
            "verdict_source_stage_id": final_artifacts.get("verdict_source_stage_id"),
            "record_status": record.status,
            "result_status": final_artifacts.get("agent_loop_result_status"),
            "main_result_eligible": final_artifacts.get("main_result_eligible"),
            "oracle_weak": final_artifacts.get("oracle_weak"),
            "final_dsl_hash": final_artifacts.get("final_dsl_hash"),
            "run_record_path_hash": run_record_path_hash,
        },
    )

def _write_lg_d1_operator_artifacts(
    *,
    record: Any,
    run_record_path: str | Path,
    operator_events: list[dict[str, Any]],
    graph_stream_status: str,
) -> dict[str, Any]:
    path = Path(run_record_path)
    operator_log_path = path.with_name(f"{record.run_id}.operator_log.jsonl")
    stream_summary_path = path.with_name(f"{record.run_id}.stream_summary.json")
    run_record_path_hash = _hash_payload(str(path))
    full_events = _merge_operator_events([], operator_events)
    full_events = _merge_operator_events(full_events, _stage_result_operator_events(record))
    full_events = _merge_operator_events(full_events, _llm_progress_operator_events(record))
    from archive.agent_loop_method.langgraph.instrumentation.retry_timeout import _lg_d2_operator_events_from_flow_logs

    full_events = _merge_operator_events(full_events, _lg_d2_operator_events_from_flow_logs(record, existing_events=full_events))
    full_events.append(_terminal_operator_event(record, run_record_path_hash=run_record_path_hash))

    operator_log_path.parent.mkdir(parents=True, exist_ok=True)
    with operator_log_path.open("w", encoding="utf-8") as f:
        for event in full_events:
            f.write(json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False) + "\n")

    summary = reconstruct_lg_d1_stream_summary_from_jsonl(operator_log_path)
    stream_summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    stream_summary_payload_hash = _hash_payload(summary)
    stream_metadata = lg_d1_llm_stream_runtime_metadata(
        real_llm_provider_api=bool(record.run_config.get("real_llm_provider_api")),
        llm_interactions=record.llm_interactions,
    )
    return {
        "schema_version": "lg-d1.operator-log-artifacts.v1",
        "operator_event_schema_version": LG_D1_OPERATOR_EVENT_SCHEMA_VERSION,
        "stream_summary_schema_version": LG_D1_STREAM_SUMMARY_SCHEMA_VERSION,
        "instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
        "graph_stream_status": graph_stream_status,
        "langgraph_stream_status": graph_stream_status,
        "operator_log_path": str(operator_log_path),
        "operator_log_hash": _hash_file(operator_log_path),
        "stream_summary_path": str(stream_summary_path),
        "stream_summary_hash": _hash_file(stream_summary_path),
        "stream_summary_payload_hash": stream_summary_payload_hash,
        "operator_event_count": len(full_events),
        "run_record_path_hash": run_record_path_hash,
        "llm_stream_required": stream_metadata["llm_stream_required"],
        "llm_stream_config_enabled": stream_metadata["llm_stream_config_enabled"],
        "llm_stream_include_usage_config_enabled": stream_metadata["llm_stream_include_usage_config_enabled"],
        "llm_stream_observed": stream_metadata["llm_stream_observed"],
        "llm_stream_observation_source": stream_metadata["llm_stream_observation_source"],
        "llm_stream_interaction_count": stream_metadata["llm_stream_interaction_count"],
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
    }

def _augment_run_record_with_lg_d1_operator_log(
    result: AgentLoopResult,
    *,
    operator_events: list[dict[str, Any]],
    graph_stream_status: str,
    operator_stream_enabled: bool,
) -> None:
    if not operator_stream_enabled or not result.run_record_path:
        return
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    artifacts = _write_lg_d1_operator_artifacts(
        record=record,
        run_record_path=path,
        operator_events=operator_events,
        graph_stream_status=graph_stream_status,
    )
    from archive.agent_loop_method.langgraph.instrumentation.retry_timeout import (
        LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION,
        LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER,
        LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION,
        build_lg_d2_llm_node_envelope_policy,
    )

    lg_d2_policy = build_lg_d2_llm_node_envelope_policy()
    record.run_config["lg_d1_operator_log_enabled"] = True
    record.run_config["instrumentation_layer_detail"] = LG_D1_INSTRUMENTATION_LAYER
    record.run_config["llm_node_envelope_policy_hash"] = lg_d2_policy["policy_hash"]
    record.environment["llm_node_envelope_policy"] = lg_d2_policy
    record.environment["llm_node_envelope_policy_hash"] = lg_d2_policy["policy_hash"]
    record.environment["lg_d2_llm_node_envelope_schema_version"] = LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION
    record.environment["lg_d2_llm_node_envelope_event_schema_version"] = LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION
    record.environment["lg_d2_llm_node_envelope_instrumentation_layer"] = LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER
    record.environment["lg_d1_operator_log_enabled"] = True
    record.environment["lg_d1_instrumentation_layer"] = LG_D1_INSTRUMENTATION_LAYER
    record.environment["lg_d1_graph_stream_status"] = graph_stream_status
    record.environment["llm_stream_required"] = artifacts["llm_stream_required"]
    record.environment["llm_stream_config_enabled"] = artifacts["llm_stream_config_enabled"]
    record.environment["llm_stream_include_usage_config_enabled"] = artifacts["llm_stream_include_usage_config_enabled"]
    record.environment["llm_stream_observed"] = artifacts["llm_stream_observed"]
    record.environment["llm_stream_observation_source"] = artifacts["llm_stream_observation_source"]
    record.environment["llm_stream_interaction_count"] = artifacts["llm_stream_interaction_count"]
    record.final_artifacts["operator_log"] = artifacts
    record.logs.append(
        {
            "event": "lg_d1_operator_log_artifacts",
            "instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "operator_event_count": artifacts["operator_event_count"],
            "operator_log_hash": artifacts["operator_log_hash"],
            "stream_summary_hash": artifacts["stream_summary_hash"],
            "does_not_replace_academic_evidence": True,
        }
    )
    write_agent_loop_run_record(record, path)

def _run_graph_with_lg_d1_stream(
    app: Any,
    *,
    initial_state: _GraphLoopState,
    run_id: str,
    operator_stream_enabled: bool,
) -> tuple[_GraphLoopState, list[dict[str, Any]], str]:
    if not operator_stream_enabled:
        state = app.invoke(initial_state, config={"configurable": {"thread_id": run_id}})
        return state, [], "disabled"

    final_state: _GraphLoopState | None = None
    operator_events: list[dict[str, Any]] = []
    try:
        stream_iter = app.stream(
            initial_state,
            config={"configurable": {"thread_id": run_id}},
            stream_mode="updates",
        )
    except TypeError as exc:
        # Some LangGraph versions can expose invoke but lack the exact stream
        # signature.  A non-generator ``stream`` implementation can still run
        # arbitrary setup/provider code before raising ``TypeError``; replaying
        # with ``invoke`` would risk duplicate LLM calls and corrupted academic
        # evidence.  Fail loud instead of making an unauditable fallback.
        raise RuntimeError(
            "LangGraph stream setup failed with TypeError; refusing fallback invoke because "
            "stream setup may already have provider/stage side effects"
        ) from exc
    for chunk in stream_iter:
        if not isinstance(chunk, dict):
            continue
        for node_id, update in chunk.items():
            if not isinstance(update, dict):
                continue
            operator_events = _merge_operator_events(operator_events, update.get("operator_events"))
            final_state = update  # LangGraph Command nodes return the graph-state update.
            operator_events.append(
                build_lg_d1_operator_event(
                    run_id=run_id,
                    event_type="node_exit",
                    node=str(node_id),
                    stage_id=_primary_stage_id_for_node(str(node_id)),
                    payload=_safe_node_exit_payload(update),
                )
            )
    if final_state is None:
        checkpoint = app.get_state({"configurable": {"thread_id": run_id}})
        state = getattr(checkpoint, "values", {}) if checkpoint is not None else {}
        if isinstance(state, dict) and "runtime_result" in state:
            operator_events = _merge_operator_events(operator_events, state.get("operator_events"))
            return state, operator_events, "degraded_with_reason:langgraph_stream_updates_empty_checkpoint_recovered"
        raise RuntimeError(
            "LangGraph stream produced no usable updates and no checkpoint runtime_result; "
            "refusing fallback invoke because stream execution may already have provider/stage side effects"
        )
    return final_state, operator_events, "enabled"

