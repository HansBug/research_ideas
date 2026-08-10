"""LangGraph runtime for the project_1 full-staged agent loop.

PR-langgraph deliberately makes LangGraph the default orchestration layer for
``method.loop.run_agent_loop``.  The public path no longer exposes a
``runtime_backend`` switch and it does not call the historical monolithic staged
runtime driver.  Instead, this module owns the loop control flow as a
``StateGraph`` with explicit nodes for start, initial modelling, validation,
repair, waiver-continuation, verdict routing, and trace-audit finalisation.

The existing ``method.staged_runtime`` module is still used as the canonical
stage-semantics library: it provides dataclasses, deterministic SD tools,
SL-adapter contracts, FixRequest/FixLog helpers, eligibility policy, and run
record construction.  That reuse is intentionally different from leaving an old
runtime backend available; LangGraph is now the only public orchestration path.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import pickle
import platform
import re
import sqlite3
import uuid
from collections import Counter, defaultdict
import copy
from dataclasses import asdict, is_dataclass, replace
from pathlib import Path
from typing import Any, TypedDict

try:  # Python 3.10 compatibility for LangGraph reducer annotations.
    from typing import Annotated
except ImportError:  # pragma: no cover - depends on interpreter minor version.
    from typing_extensions import Annotated

try:  # Python 3.10 compatibility for the repo venv.
    from typing import NotRequired
except ImportError:  # pragma: no cover - depends on interpreter minor version.
    from typing_extensions import NotRequired

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_store
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command, Send

from method.llm_stages import ChatProvider, LLMStageConfig, estimate_prompt_tokens
from method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
import method.staged_runtime as staged_runtime
from method.schema import (
    AgentLoopResult,
    DesignFeedback,
    FixPlan,
    RepairRejection,
    RepairReviewFeedback,
    RevisedFixPlan,
    SL10RepairReviewOutput,
    GroundedElement,
    GroundingMap,
    LoopConfig,
    ModelReviewFeedback,
    ScenarioResult,
    ScenarioSet,
    SimFeedback,
    StageContext,
    StageResultMeta,
)
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    FullStagedRuntimeConfig,
    _LLMRetryExhausted,
    _RunState,
    _ValidationPass,
    RepairRequest,
    ScenarioGenerationRequest,
    _apply_grounding_update_hints,
    _append_flow_log,
    _append_llm_stage_run,
    _append_stage,
    _build_record,
    _clone_stage_context,
    _coerce_sl9_decision_output,
    _compact_json,
    _default_sl10_output_from_local_checks,
    _diagnostic_variable_role_summary,
    _dsl_diff_summary,
    _extract_grounding_update_hints,
    _feedback_brief,
    _final_rejection_reason,
    _final_rejection_source_stage_id,
    _fix_log_entry,
    _fix_request_batch_from_plan,
    _fix_request_batch_with_repair_memory,
    _hash_text,
    _is_llm_stage_run,
    _local_repair_check_evidence,
    _mark_retry_exhausted,
    _make_waived_design_feedback,
    _make_waived_sim_feedback,
    _mark_sc12_verdict,
    _meta,
    _merge_scenario_sets_by_name,
    _model_review_blocks,
    _record_deterministic_iteration,
    _repair_memory_for_log,
    _repair_memory_for_prompt,
    _repair_review_from_sl10,
    _repair_selected_reason,
    _scenario_history_item,
    _selected_feedback_trace,
    _select_first_blocking,
    _short_hash,
    _sl10_noop_override_waiver_audit,
    _sl9_meta,
    _stale_overridden_scenario_waiver_audit,
    _stale_overridden_sd6_validation_waiver_audit,
    _stage_ids,
    _utc_now,
)
from method.langgraph.constants import GRAPH_RUNTIME_SCHEMA_VERSION, NODE_EDGE_SCHEMA_VERSION
from method.langgraph.registry import (
    build_langgraph_node_registry as _build_langgraph_node_registry_foundation,
    graph_registry_consistency as _graph_registry_consistency_foundation,
)
from method.langgraph.state import _CompatState
from method.langgraph.instrumentation.common import (
    _canonical_json_payload,
    _hash_canonical_payload,
    _hash_file,
    _hash_payload,
    _jsonable,
    _package_version,
)
from method.langgraph.checkpointing import _PickleCheckpointSerde, _checkpoint_resume_smoke
from method.langgraph.instrumentation.operator_stream import (
    LG_D1_INSTRUMENTATION_LAYER,
    LG_D1_OPERATOR_EVENT_SCHEMA_VERSION,
    LG_D1_STREAM_SUMMARY_SCHEMA_VERSION,
    _LG_D1_ACADEMIC_EVIDENCE_SOURCES,
    _LG_D1_FORBIDDEN_OPERATOR_COMPACT_KEYS,
    _LG_D1_FORBIDDEN_OPERATOR_KEY_FRAGMENTS,
    _LG_D1_FORBIDDEN_OPERATOR_KEY_SUFFIXES,
    _LG_D1_FORBIDDEN_OPERATOR_PAYLOAD_KEYS,
    _LG_D1_LLM_PROGRESS_ALLOWED_PAYLOAD_KEYS,
    _LG_D1_LLM_PROGRESS_EVENT_TYPES,
    _LG_D1_SECRET_VALUE_PATTERNS,
    _append_lg_d1_operator_event,
    _augment_run_record_with_lg_d1_operator_log,
    _build_lg_d1_stream_summary,
    _flow_log_stage_rows_by_stage,
    _hash_file as _lg_d1_hash_file,
    _llm_progress_operator_events,
    _llm_stream_usage_from_interactions,
    _merge_operator_events,
    _node_for_stage,
    _node_stage_ids_by_node_id,
    _operator_event_key,
    _operator_stage_flow_payload,
    _pop_precise_stage_node,
    _primary_stage_id_for_node,
    _run_graph_with_lg_d1_stream,
    _safe_node_exit_payload,
    _sanitize_lg_d1_llm_progress_payload,
    _sanitize_lg_d1_operator_payload,
    _stage_result_operator_events,
    _terminal_operator_event,
    _write_lg_d1_operator_artifacts,
    build_lg_d1_operator_event,
    lg_d1_llm_stream_runtime_metadata,
    reconstruct_lg_d1_stream_summary_from_jsonl,
)
from method.langgraph.instrumentation.trace_export import (
    LG_G1_TRACE_EXPORT_INSTRUMENTATION_LAYER,
    LG_G1_TRACE_EXPORT_SCHEMA_VERSION,
    _LG_G1_ACADEMIC_EVIDENCE_SOURCES,
    _LG_G1_UNSAFE_TRACE_SOURCE_KEYS,
    _augment_run_record_with_lg_g1_trace_export,
    _lg_g1_has_secret_like_value,
    _lg_g1_safe_trace_payload,
    _lg_g1_stage_ids,
    _lg_g1_trace_export_policy,
    _write_lg_g1_trace_artifact,
)
from method.langgraph.instrumentation.tool_wrappers import (
    LG_E3_TOOLNODE_WRAPPER_INSTRUMENTATION_LAYER,
    LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
    _LG_E3_SENSITIVE_SUMMARY_KEY_EXACT,
    _augment_run_record_with_lg_e3_toolnode_trace,
    _lg_e3_fixed_tool_call,
    _lg_e3_summary_key_is_sensitive,
    _lg_e3_toolnode_wrappers_enabled,
    _record_lg_e3_toolnode_event,
    _safe_lg_e3_tool_summary,
    build_lg_e3_toolnode_wrapper_registry,
)
from method.langgraph.instrumentation.retry_timeout import (
    LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION,
    LG_D2_LLM_NODE_ENVELOPE_EVENT_TYPES,
    LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER,
    LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION,
    _append_lg_d2_envelope_event,
    _lg_d2_attempt_error_kind,
    _lg_d2_emit_interaction_attempt_events,
    _lg_d2_envelope_event,
    _lg_d2_envelope_safe_summary,
    _lg_d2_error_kind_from_exception,
    _lg_d2_event_match_signature,
    _lg_d2_exception_is_provider_retryable,
    _lg_d2_fallback_unique_signature,
    _lg_d2_flow_log_match_signature,
    _lg_d2_latest_attempt_index,
    _lg_d2_latest_interaction_index,
    _lg_d2_operator_events_from_flow_logs,
    _lg_d2_retry_error_for_exception,
    _lg_d2_retryable_taxonomy,
    _lg_d2_stage_meta_for_retry_error,
    _lg_d2_wrap_llm_stage_node,
    build_lg_d2_llm_node_envelope_policy,
)
from method.langgraph.instrumentation.send_parallel import (
    LG_E2_SEND_PARALLEL_INSTRUMENTATION_LAYER,
    LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
    _LG_E2_ORDERING_KEY_FIELDS,
    _LgE2SendState,
    _augment_run_record_with_lg_e2_send_parallel_trace,
    _lg_e2_aggregate_worker_results,
    _lg_e2_build_isolated_context,
    _lg_e2_canonicalize_scenario_results,
    _lg_e2_canonicalize_worker_results,
    _lg_e2_coverage_summary,
    _lg_e2_execute_send_graph,
    _lg_e2_feedback_scenario_results,
    _lg_e2_finalize_metadata_from_record,
    _lg_e2_final_verdict_summary,
    _lg_e2_first_blocking_id,
    _lg_e2_metadata_for_feedback,
    _lg_e2_normalized_scenario_name,
    _lg_e2_preflight,
    _lg_e2_run_sd6_send_parallel_or_serial,
    _lg_e2_scenario_history_summary,
    _lg_e2_scenario_result_sort_key,
    _lg_e2_selected_feedback_digest,
    _lg_e2_serial_equivalence_payload,
    _lg_e2_single_scenario_set,
    _lg_e2_worker_ordering_key,
    _lg_e2_worker_result_reducer,
    _lg_e2_worker_specs,
    build_lg_e2_send_parallel_contract,
)
from method.langgraph.instrumentation.store import (
    _drain_transients,
    _drop_transient,
    _get_transient,
    _put_transient,
    _transient_namespace,
    _transient_namespace_label,
    langgraph_store_compat_smoke,
)
from method.langgraph.subgraphs.context_engineering import (
    LG_C2_CANONICAL_RECORD_FIELD,
    LG_C2_CONTEXT_INSTRUMENTATION_LAYER,
    LG_C2_CONTEXT_NODE_IDS,
    LG_C2_CONTEXT_SUBGRAPH_ID,
    LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION,
    LG_C2_ContextAssemblyResult,
    LG_C2_ContextRedactionBlocked,
    _LG_C2_ContextState,
    _build_lg_c2_context_subgraph,
    _lg_c2_prompt_budget_metadata,
    _lg_c2_secret_like_field_detected,
    _lg_c2_within_prompt_budget,
    assemble_lg_c2_prompt_context,
    build_lg_c2_context_subgraph_contract,
)
from method.stages.ids import StageId, StageStatus
from method.stages.ids import FeedbackSource
from method.stages.sd_tools import freeze_scenario_set, mark_warning_repair_attempt, run_sd8_fix_plan

LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION = "lg-f1.resume-reconciliation.v1"
LG_B3_WAIVER_ENTRY_ENVELOPE_SCHEMA_VERSION = "lg-b3.waiver-entry-envelope.v1"
LG_C1_REDUCER_STATE_SCHEMA_VERSION = "lg-c1.reducer-json-state.v1"

_LG_C1_APPEND_ONLY_REDUCER_CHANNEL_NAMES = (
    "graph_trace",
    "operator_events",
    "toolnode_wrapper_events",
    "lg_e2_send_parallel_events",
    "stage_record_events",
    "llm_interaction_events",
    "fix_log_events",
    "scenario_history_events",
    "repair_history_events",
)
_LG_C1_JSON_SAFE_CHANNEL_NAMES = (
    "nl",
    "run_id",
    "iteration",
    "iteration_stage_start",
    "validation_ref",
    "iteration_record",
    "selected_trace",
    "accepted",
    "repair_patch",
    "runtime_error",
    "operator_stream_enabled",
    "toolnode_wrapper_enabled",
    *_LG_C1_APPEND_ONLY_REDUCER_CHANNEL_NAMES,
)
_LG_C1_LIVE_OBJECT_CHANNEL_NAMES = (
    "runtime_state",
    "runtime_result",
    "validation_result",
    "validation_context",
    "validation_feedback",
    "validation_stage_metas",
    "validation_scenario_set",
    "validation_continuation_source",
    "repair_validation",
    "repair_selected_feedback",
    "repair_fix_plan",
    "repair_effective_fix_plan",
    "repair_request_batch",
    "repair_active_request_batch",
    "repair_sl9_decision",
    "repair_request",
    "repair_local_review",
    "repair_local_meta",
    "repair_local_sd10_repair_review",
    "repair_sl10_output",
    "repair_repair_review",
    "repair_last_repair_review",
    "repair_last_sl10_output",
    "waiver_validation_source",
    "waiver_result",
)
_LG_C1_CHECKPOINT_SERDE_MODE = "pickle_for_live_object_bridge_with_json_safe_reducer_channels"

_VALID_RECORD_STATUSES = {"success", "failed", "rejected", "budget_exhausted", "error", "invalid"}


























































def _lg_c1_event_key(event: Any) -> str:
    return json.dumps(_jsonable(event), ensure_ascii=False, sort_keys=True, default=str)


def _lg_c1_append_only_reducer(existing: list[dict[str, Any]] | None, new_events: Any) -> list[dict[str, Any]]:
    """Merge append-only LangGraph channels without duplicating full-state updates.

    Most current graph nodes still return a full state dict.  A naive ``operator.add``
    reducer would therefore duplicate every previously emitted trace event when a
    node returns ``{"graph_trace": old + [new]}``.  LG-C1 keeps the public stage
    semantics unchanged and uses a prefix-aware reducer instead:

    - if the incoming value is the full ledger with the old prefix, accept it;
    - if the incoming value is an older prefix, keep the existing ledger;
    - otherwise append only events that are not already present.
    """

    old = list(existing or [])
    if new_events is None:
        return old
    incoming = list(new_events if isinstance(new_events, list) else [new_events])
    if not incoming:
        return old
    if len(incoming) >= len(old) and incoming[: len(old)] == old:
        return incoming
    if len(old) >= len(incoming) and old[: len(incoming)] == incoming:
        return old
    merged = list(old)
    seen = {_lg_c1_event_key(item) for item in merged}
    for item in incoming:
        key = _lg_c1_event_key(item)
        if key in seen:
            continue
        merged.append(item)
        seen.add(key)
    return merged




class _GraphLoopState(TypedDict, total=False):
    nl: str
    graph_trace: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    operator_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    operator_stream_enabled: bool
    toolnode_wrapper_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    stage_record_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    llm_interaction_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    fix_log_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    scenario_history_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    repair_history_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    toolnode_wrapper_enabled: bool
    run_id: str
    runtime_state: Any
    iteration: int
    iteration_stage_start: int
    validation_ref: str
    lg_e2_send_parallel_events: Annotated[list[dict[str, Any]], _lg_c1_append_only_reducer]
    iteration_record: dict[str, Any]
    selected_trace: Any
    accepted: bool
    repair_patch: dict[str, Any]
    runtime_result: Any
    runtime_error: NotRequired[str]











def build_lg_c1_graph_state_contract() -> dict[str, Any]:
    """Return LG-C1's reducer / JSON-safe graph-state boundary contract.

    This is deliberately a boundary contract, not a durable-resume claim.  The
    real agent loop still carries live ``_RunState`` / validation / repair
    objects through LangGraph and therefore still uses pickle for in-memory
    checkpoints.  LG-C1 only makes the append-only evidence mirrors explicit as
    reducer channels and records which parts are JSON-safe.
    """

    return {
        "schema_version": LG_C1_REDUCER_STATE_SCHEMA_VERSION,
        "append_only_reducer_channel_names": list(_LG_C1_APPEND_ONLY_REDUCER_CHANNEL_NAMES),
        "json_safe_channel_names": list(_LG_C1_JSON_SAFE_CHANNEL_NAMES),
        "live_object_channel_names": list(_LG_C1_LIVE_OBJECT_CHANNEL_NAMES),
        "pickle_required_channel_names": list(_LG_C1_LIVE_OBJECT_CHANNEL_NAMES),
        "checkpoint_serde": "pickle",
        "checkpoint_serde_mode": _LG_C1_CHECKPOINT_SERDE_MODE,
        "checkpoint_backend": "memory",
        "checkpoint_backend_type": "InMemorySaver",
        "real_agent_loop_json_checkpoint_supported": False,
        "real_agent_loop_resume_supported": False,
        "real_agent_loop_resume_scope": "not_claimed_in_LG_C1",
        "json_safe_scope": (
            "append-only reducer mirrors and graph-state readiness metadata only; "
            "canonical academic evidence remains in AgentLoopRunRecord"
        ),
        "live_object_boundary_reason": (
            "runtime_state, validation/repair working objects, adapter outputs and "
            "pyfcstm/scenario objects are still live Python objects in the graph"
        ),
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources": list(_LG_D1_ACADEMIC_EVIDENCE_SOURCES),
    }


def _lg_c1_stage_record_events(stage_records: list[Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(stage_records or []):
        safe = _jsonable(row)
        if not isinstance(safe, dict):
            safe = {"value": safe}
        events.append(
            {
                "index": index,
                "stage_id": str(safe.get("stage_id") or ""),
                "stage_kind": str(safe.get("stage_kind") or ""),
                "status": str(safe.get("status") or ""),
                "ok": bool(safe.get("ok")) if isinstance(safe.get("ok"), bool) else safe.get("ok"),
                "payload_hash": _hash_payload(safe),
            }
        )
    return events


def _lg_c1_llm_interaction_events(llm_interactions: list[Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(llm_interactions or []):
        safe = _jsonable(row)
        if not isinstance(safe, dict):
            safe = {"value": safe}
        usage = safe.get("usage") if isinstance(safe.get("usage"), dict) else {}
        events.append(
            {
                "index": index,
                "stage_id": str(safe.get("stage_id") or ""),
                "schema_validation_ok": safe.get("schema_validation_ok"),
                "stream": usage.get("stream") if isinstance(usage, dict) else None,
                "payload_hash": _hash_payload(safe),
            }
        )
    return events


def _lg_c1_fix_log_events(fix_log: list[Any]) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(fix_log or []):
        safe = _jsonable(row)
        if not isinstance(safe, dict):
            safe = {"value": safe}
        events.append(
            {
                "index": index,
                "entry_id": str(safe.get("entry_id") or ""),
                "phase": str(safe.get("phase") or ""),
                "request_id": str(safe.get("request_id") or ""),
                "decision": str(safe.get("decision") or ""),
                "candidate_dsl_hash": safe.get("candidate_dsl_hash"),
                "payload_hash": _hash_payload(safe),
            }
        )
    return events


def _lg_c1_generic_history_events(rows: list[Any], *, id_key: str | None = None) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(rows or []):
        safe = _jsonable(row)
        if not isinstance(safe, dict):
            safe = {"value": safe}
        event = {"index": index, "payload_hash": _hash_payload(safe)}
        if id_key:
            event[id_key] = str(safe.get(id_key) or "")
        for optional_key in ("name", "stage_id", "source_stage", "scenario_set_id", "decision", "phase"):
            if optional_key in safe and optional_key not in event:
                event[optional_key] = _jsonable(safe.get(optional_key))
        events.append(event)
    return events


def _sync_lg_c1_canonical_mirror_channels(graph_state: _GraphLoopState) -> None:
    """Mirror canonical ledgers into JSON-safe reducer channels.

    The mirrors are hash/summary ledgers.  They are useful for checkpoint
    readiness and reducer audits, but they do not become the final verdict source.
    """

    runtime_state = graph_state.get("runtime_state")
    if not isinstance(runtime_state, _RunState):
        return
    graph_state["stage_record_events"] = _lg_c1_stage_record_events(runtime_state.stage_records)
    graph_state["llm_interaction_events"] = _lg_c1_llm_interaction_events(runtime_state.llm_interactions)
    graph_state["fix_log_events"] = _lg_c1_fix_log_events(runtime_state.fix_log)
    graph_state["scenario_history_events"] = _lg_c1_generic_history_events(
        runtime_state.scenario_history,
        id_key="scenario_set_id",
    )
    graph_state["repair_history_events"] = _lg_c1_generic_history_events(runtime_state.repair_history)


def _lg_c1_json_serialization_audit(channel_values: dict[str, Any]) -> dict[str, Any]:
    failures: dict[str, str] = {}
    for channel, value in channel_values.items():
        try:
            json.dumps(_jsonable(value), ensure_ascii=False, sort_keys=True, allow_nan=False, default=str)
        except Exception as exc:  # pragma: no cover - failure shape is asserted by callers if ever triggered.
            failures[channel] = f"{type(exc).__name__}: {str(exc)[:200]}"
    return {
        "all_json_safe_reducer_channels_serializable": not failures,
        "failure_count": len(failures),
        "failures": failures,
    }


def _lg_c1_channel_summary(value: Any) -> dict[str, Any]:
    safe = _jsonable(value if value is not None else [])
    count = len(safe) if isinstance(safe, list) else (len(safe) if isinstance(safe, dict) else 0)
    return {
        "count": count,
        "payload_hash": _hash_payload(safe),
    }


def _lg_c1_hash_sequence(rows: list[Any]) -> list[str]:
    return [_hash_payload(_jsonable(row)) for row in rows or []]


def _lg_c1_event_hashes(rows: Any) -> list[str]:
    return [str(row.get("payload_hash") or "") for row in (rows or []) if isinstance(row, dict)]


def _lg_c1_operator_log_events_from_record(record: Any) -> list[dict[str, Any]]:
    final_artifacts = getattr(record, "final_artifacts", {}) if record is not None else {}
    operator_log = final_artifacts.get("operator_log") if isinstance(final_artifacts, dict) else {}
    path_text = operator_log.get("operator_log_path") if isinstance(operator_log, dict) else None
    if not path_text:
        return []
    try:
        path = Path(str(path_text))
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except Exception:
        return []


def _lg_c1_operator_log_audit(record: Any, graph_operator_events: list[dict[str, Any]]) -> dict[str, Any]:
    operator_log_events = _lg_c1_operator_log_events_from_record(record)
    graph_types = sorted({str(row.get("event_type") or row.get("event") or "") for row in graph_operator_events if isinstance(row, dict)})
    log_types = sorted({str(row.get("event_type") or row.get("event") or "") for row in operator_log_events if isinstance(row, dict)})
    graph_lg_d2_count = sum(
        1 for row in graph_operator_events if isinstance(row, dict) and str(row.get("event_type") or "").startswith("lg_d2_")
    )
    log_lg_d2_count = sum(
        1 for row in operator_log_events if isinstance(row, dict) and str(row.get("event_type") or "").startswith("lg_d2_")
    )
    return {
        "graph_state_operator_event_count": len(graph_operator_events),
        "operator_log_event_count": len(operator_log_events),
        "graph_state_event_types": graph_types,
        "operator_log_event_types": log_types,
        "lg_d2_envelope_event_count": graph_lg_d2_count,
        "operator_log_lg_d2_envelope_event_count": log_lg_d2_count,
        "operator_log_includes_graph_state_events": len(operator_log_events) >= len(graph_operator_events),
        "operator_log_missing_graph_state_event_types": [event_type for event_type in graph_types if event_type and event_type not in log_types],
        "operator_log_extra_event_types": [event_type for event_type in log_types if event_type and event_type not in graph_types],
        "operator_log_events_hash": _hash_payload(operator_log_events),
        "graph_state_operator_events_hash": _hash_payload(graph_operator_events),
        "scope": (
            "operator_events reducer channel is the LangGraph graph-state operator probe; "
            "complete tee-able LG-D1 operator ledger remains final_artifacts.operator_log.operator_log_path"
        ),
    }


def _build_lg_c1_graph_state_readiness(record: Any, graph_state: _GraphLoopState) -> dict[str, Any]:
    contract = build_lg_c1_graph_state_contract()
    graph_state_channel_values = {
        channel: _jsonable(graph_state.get(channel, []))
        for channel in contract["append_only_reducer_channel_names"]
    }
    # The final run record can be redacted during ``_build_record``.  For
    # canonical academic ledgers, final readiness therefore records two views:
    # (1) graph-state reducer channels as actually accumulated by LangGraph;
    # (2) persisted-record mirrors reconstructed from the final, redacted
    # AgentLoopRunRecord.  LG-C1 must not silently replace (1) with (2), because
    # that would make reducer consistency self-certifying.
    persisted_channel_values = dict(graph_state_channel_values)
    persisted_channel_values["stage_record_events"] = _lg_c1_stage_record_events(record.stage_records)
    persisted_channel_values["llm_interaction_events"] = _lg_c1_llm_interaction_events(record.llm_interactions)
    persisted_channel_values["fix_log_events"] = _lg_c1_fix_log_events(record.fix_log)
    persisted_channel_values["scenario_history_events"] = _lg_c1_generic_history_events(
        record.scenario_history,
        id_key="scenario_set_id",
    )
    persisted_channel_values["repair_history_events"] = _lg_c1_generic_history_events(record.repair_history)
    canonical_stage_hashes = _lg_c1_hash_sequence(record.stage_records)
    canonical_llm_hashes = _lg_c1_hash_sequence(record.llm_interactions)
    canonical_fix_hashes = _lg_c1_hash_sequence(record.fix_log)
    canonical_scenario_hashes = _lg_c1_hash_sequence(record.scenario_history)
    canonical_repair_hashes = _lg_c1_hash_sequence(record.repair_history)

    graph_state_consistency = {
        "stage_records_match": _lg_c1_event_hashes(graph_state_channel_values.get("stage_record_events")) == canonical_stage_hashes,
        "llm_interactions_match": _lg_c1_event_hashes(graph_state_channel_values.get("llm_interaction_events")) == canonical_llm_hashes,
        "fix_log_match": _lg_c1_event_hashes(graph_state_channel_values.get("fix_log_events")) == canonical_fix_hashes,
        "scenario_history_match": _lg_c1_event_hashes(graph_state_channel_values.get("scenario_history_events")) == canonical_scenario_hashes,
        "repair_history_match": _lg_c1_event_hashes(graph_state_channel_values.get("repair_history_events")) == canonical_repair_hashes,
    }
    persisted_consistency = {
        "stage_records_match": _lg_c1_event_hashes(persisted_channel_values.get("stage_record_events")) == canonical_stage_hashes,
        "llm_interactions_match": _lg_c1_event_hashes(persisted_channel_values.get("llm_interaction_events")) == canonical_llm_hashes,
        "fix_log_match": _lg_c1_event_hashes(persisted_channel_values.get("fix_log_events")) == canonical_fix_hashes,
        "scenario_history_match": _lg_c1_event_hashes(persisted_channel_values.get("scenario_history_events")) == canonical_scenario_hashes,
        "repair_history_match": _lg_c1_event_hashes(persisted_channel_values.get("repair_history_events")) == canonical_repair_hashes,
    }
    operator_log_audit = _lg_c1_operator_log_audit(
        record,
        graph_state_channel_values.get("operator_events") if isinstance(graph_state_channel_values.get("operator_events"), list) else [],
    )
    return {
        **contract,
        "final_reducer_channel_summaries": {
            channel: _lg_c1_channel_summary(value)
            for channel, value in persisted_channel_values.items()
        },
        "final_reducer_channel_events": persisted_channel_values,
        "graph_state_reducer_channel_summaries": {
            channel: _lg_c1_channel_summary(value)
            for channel, value in graph_state_channel_values.items()
        },
        "graph_state_reducer_channel_events": graph_state_channel_values,
        "final_reducer_channel_event_sources": {
            "graph_trace": "LangGraph graph state reducer channel",
            "operator_events": "LangGraph graph state operator probe channel; full operator log audited separately",
            "toolnode_wrapper_events": "LangGraph graph state reducer channel",
            "lg_e2_send_parallel_events": "LG-E2 Send fan-out audit channel; canonical SD-6 feedback remains AgentLoopRunRecord",
            "stage_record_events": "persisted AgentLoopRunRecord.stage_records",
            "llm_interaction_events": "persisted AgentLoopRunRecord.llm_interactions",
            "fix_log_events": "persisted AgentLoopRunRecord.fix_log",
            "scenario_history_events": "persisted AgentLoopRunRecord.scenario_history",
            "repair_history_events": "persisted AgentLoopRunRecord.repair_history",
        },
        "graph_state_vs_canonical_consistency": graph_state_consistency,
        "graph_state_vs_canonical_consistency_ok": all(graph_state_consistency.values()),
        "persisted_record_mirror_canonical_consistency": persisted_consistency,
        "persisted_record_mirror_canonical_consistency_ok": all(persisted_consistency.values()),
        # Backward-compatible name now deliberately means the real graph-state
        # reducer mirror check, not the self-generated persisted mirror check.
        "mirror_canonical_consistency": graph_state_consistency,
        "mirror_canonical_consistency_ok": all(graph_state_consistency.values()),
        "operator_log_audit": operator_log_audit,
        "json_serialization_audit": _lg_c1_json_serialization_audit({
            **graph_state_channel_values,
            "persisted_record_reducer_channel_events": persisted_channel_values,
            "operator_log_audit": operator_log_audit,
        }),
        "canonical_counts": {
            "stage_records": len(record.stage_records),
            "llm_interactions": len(record.llm_interactions),
            "fix_log": len(record.fix_log),
            "scenario_history": len(record.scenario_history),
            "repair_history": len(record.repair_history),
        },
    }


def _inject_lg_c1_graph_state_readiness(record: Any, graph_state: _GraphLoopState) -> None:
    readiness = _build_lg_c1_graph_state_readiness(record, graph_state)
    contract = {
        key: readiness[key]
        for key in (
            "schema_version",
            "append_only_reducer_channel_names",
            "json_safe_channel_names",
            "live_object_channel_names",
            "pickle_required_channel_names",
            "checkpoint_serde",
            "checkpoint_serde_mode",
            "checkpoint_backend",
            "checkpoint_backend_type",
            "real_agent_loop_json_checkpoint_supported",
            "real_agent_loop_resume_supported",
            "real_agent_loop_resume_scope",
            "json_safe_scope",
            "live_object_boundary_reason",
            "does_not_replace_academic_evidence",
            "academic_evidence_sources",
        )
    }
    record.run_config["lg_c1_graph_state_contract"] = contract
    record.environment.update(
        {
            "lg_c1_reducer_state_schema_version": readiness["schema_version"],
            "lg_c1_append_only_reducer_channel_names": readiness["append_only_reducer_channel_names"],
            "lg_c1_json_safe_channel_names": readiness["json_safe_channel_names"],
            "lg_c1_live_object_channel_names": readiness["live_object_channel_names"],
            "lg_c1_pickle_required_channel_names": readiness["pickle_required_channel_names"],
            "lg_c1_reducer_channel_count": len(readiness["append_only_reducer_channel_names"]),
            "lg_c1_academic_evidence_sources": readiness["academic_evidence_sources"],
            "checkpoint_serde_mode": readiness["checkpoint_serde_mode"],
            "real_agent_loop_json_checkpoint_supported": readiness["real_agent_loop_json_checkpoint_supported"],
            "lg_c1_mirror_canonical_consistency_ok": readiness["mirror_canonical_consistency_ok"],
            "lg_c1_json_safe_reducer_channels_serializable": readiness["json_serialization_audit"][
                "all_json_safe_reducer_channels_serializable"
            ],
        }
    )
    record.final_artifacts["lg_c1_graph_state_readiness"] = readiness
    record.logs.append(
        {
            "event": "lg_c1_graph_state_readiness",
            "schema_version": LG_C1_REDUCER_STATE_SCHEMA_VERSION,
            "append_only_reducer_channel_count": len(readiness["append_only_reducer_channel_names"]),
            "mirror_canonical_consistency_ok": readiness["mirror_canonical_consistency_ok"],
            "all_json_safe_reducer_channels_serializable": readiness["json_serialization_audit"][
                "all_json_safe_reducer_channels_serializable"
            ],
            "real_agent_loop_json_checkpoint_supported": readiness["real_agent_loop_json_checkpoint_supported"],
            "does_not_replace_academic_evidence": True,
        }
    )







































































































































def build_langgraph_node_registry() -> dict[str, Any]:
    """Return PR-langgraph's explicit StateGraph node/edge registry.

    LG-M1-D1 keeps this no-arg function as the public compatibility facade.
    The foundation registry builder receives LG-C2 context identifiers by
    injection so ``method.langgraph.registry`` does not import this facade and
    does not own context-engineering behavior.
    """

    return _build_langgraph_node_registry_foundation(
        context_subgraph_id=LG_C2_CONTEXT_SUBGRAPH_ID,
        context_node_ids=LG_C2_CONTEXT_NODE_IDS,
    )


def graph_registry_consistency(planned_stage_graph: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """Compare planned stage IDs with registry coverage via the compatibility facade."""

    return _graph_registry_consistency_foundation(planned_stage_graph, registry)


def langgraph_compat_smoke() -> dict[str, Any]:
    """Run the PR-langgraph compatibility smoke against installed LangGraph."""

    result: dict[str, Any] = {
        "ok": False,
        "langgraph_version": _package_version("langgraph"),
        "langgraph_checkpoint_version": _package_version("langgraph-checkpoint"),
        "stategraph_compile_ok": False,
        "invoke_ok": False,
        "stream_ok": False,
        "checkpoint_smoke_ok": False,
    }
    try:
        graph = StateGraph(_CompatState)

        def inc(state: _CompatState) -> _CompatState:
            return {"value": int(state.get("value", 0)) + 1}

        graph.add_node("inc", inc)
        graph.add_edge(START, "inc")
        graph.add_edge("inc", END)
        checkpointer = InMemorySaver(serde=_PickleCheckpointSerde())
        app = graph.compile(checkpointer=checkpointer)
        result["stategraph_compile_ok"] = True
        config = {"configurable": {"thread_id": "pr-langgraph-compat-smoke"}}
        invoked = app.invoke({"value": 1}, config=config)
        result["invoke_ok"] = invoked.get("value") == 2
        streamed = list(app.stream({"value": 1}, config={"configurable": {"thread_id": "pr-langgraph-compat-stream"}}))
        result["stream_ok"] = bool(streamed)
        state = app.get_state(config)
        result["checkpoint_smoke_ok"] = state is not None
        result["ok"] = all(
            bool(result[key]) for key in ("stategraph_compile_ok", "invoke_ok", "stream_ok", "checkpoint_smoke_ok")
        )
    except Exception as exc:  # pragma: no cover - failure payload is tested indirectly by callers.
        result["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    return result






def _graph_runtime_metadata(
    *,
    registry: dict[str, Any],
    compat: dict[str, Any],
    graph_config_hash: str,
    toolnode_wrapper_enabled: bool = True,
    checkpoint_metadata: dict[str, Any] | None = None,
    lg_e2_send_parallel_enabled: bool = True,
) -> dict[str, Any]:
    lg_c1_contract = build_lg_c1_graph_state_contract()
    lg_e2_contract = build_lg_e2_send_parallel_contract()
    lg_d2_policy = build_lg_d2_llm_node_envelope_policy()
    metadata = {
        "graph_runtime_backend": "langgraph",
        "graph_runtime_status": "enabled" if compat.get("ok") else "disabled_with_reason",
        "graph_runtime_backend_version": GRAPH_RUNTIME_SCHEMA_VERSION,
        "langgraph_version": compat.get("langgraph_version", _package_version("langgraph")),
        "langgraph_checkpoint_version": compat.get("langgraph_checkpoint_version", _package_version("langgraph-checkpoint")),
        "graph_runtime_id": f"langgraph:{GRAPH_RUNTIME_SCHEMA_VERSION}",
        "graph_config_hash": graph_config_hash,
        "node_edge_schema_version": registry.get("schema_version", NODE_EDGE_SCHEMA_VERSION),
        "checkpoint_backend": "memory",
        "checkpoint_backend_type": "InMemorySaver",
        "checkpoint_serde": "pickle",
        "checkpoint_serde_mode": lg_c1_contract["checkpoint_serde_mode"],
        "checkpoint_path_hash": "sha256:memory",
        "resumed_from_checkpoint": False,
        "resume_checkpoint_id_hash": None,
        "real_agent_loop_json_checkpoint_supported": lg_c1_contract["real_agent_loop_json_checkpoint_supported"],
        "lg_c1_reducer_state_schema_version": LG_C1_REDUCER_STATE_SCHEMA_VERSION,
        "lg_c1_append_only_reducer_channel_names": lg_c1_contract["append_only_reducer_channel_names"],
        "lg_c1_json_safe_channel_names": lg_c1_contract["json_safe_channel_names"],
        "lg_c1_live_object_channel_names": lg_c1_contract["live_object_channel_names"],
        "lg_c1_pickle_required_channel_names": lg_c1_contract["pickle_required_channel_names"],
        "lg_c1_reducer_channel_count": len(lg_c1_contract["append_only_reducer_channel_names"]),
        "lg_c1_academic_evidence_sources": lg_c1_contract["academic_evidence_sources"],
        "instrumentation_layer": "langgraph",
        "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
        "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "lg_e3_toolnode_wrapper_registry_hash": _hash_payload(build_lg_e3_toolnode_wrapper_registry()),
        "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
        "lg_e2_send_parallel_enabled": bool(lg_e2_send_parallel_enabled),
        "lg_e2_send_parallel_schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
        "lg_e2_send_parallel_contract_hash": _hash_payload(lg_e2_contract),
        "lg_e2_send_parallel_ordering_key_fields": lg_e2_contract["ordering_key_fields"],
        "llm_node_envelope_policy": lg_d2_policy,
        "llm_node_envelope_policy_hash": lg_d2_policy["policy_hash"],
        "lg_d2_llm_node_envelope_schema_version": LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION,
        "lg_d2_llm_node_envelope_event_schema_version": LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION,
        "lg_d2_llm_node_envelope_instrumentation_layer": LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER,
        "checkpoint_resume_smoke": _checkpoint_resume_smoke(),
        "langgraph_compat_smoke": compat,
        "dependency_versions": {
            "python": platform.python_version(),
            "langgraph": compat.get("langgraph_version", _package_version("langgraph")),
            "langgraph-checkpoint": compat.get("langgraph_checkpoint_version", _package_version("langgraph-checkpoint")),
            "langchain-core": _package_version("langchain-core"),
        },
    }
    if checkpoint_metadata:
        metadata.update(_jsonable(checkpoint_metadata))
    return metadata


def _planned_stage_graph_from_config(cfg: LoopConfig) -> dict[str, Any]:
    from method.loop import build_planned_stage_graph

    return build_planned_stage_graph(cfg)


def _provider_model_redacted(cfg: LoopConfig, provider: ChatProvider | None = None) -> str:
    if cfg.llm_model:
        return cfg.llm_model
    if provider is not None:
        return getattr(provider, "model_id", "<provider:model>")
    return os.environ.get("LLM_MODEL") or "<mock:model>"


def _provider_config_read(cfg: LoopConfig) -> bool:
    if cfg.llm_provider_mode != "real_env":
        return False
    return all(bool(os.environ.get(key)) for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"))

# Historical PR-LG-A1 compatibility placeholder.  LG-A2 must not write this
# module-level dict anymore: transient validation payloads live in the
# per-compiled LangGraph Store created by ``_build_graph``.
_TRANSIENT_OBJECTS: dict[str, Any] = {}














def _trace_node(graph_state: _GraphLoopState, node_id: str, event: str = "node_enter", **payload: Any) -> None:
    trace = list(graph_state.get("graph_trace", []) or [])
    trace.append({"node_id": node_id, "event": event, "instrumentation_layer": "langgraph", **_jsonable(payload)})
    graph_state["graph_trace"] = trace
    stage_ids = _node_stage_ids_by_node_id().get(node_id, [])
    _append_lg_d1_operator_event(
        graph_state,
        event_type=event,
        node=node_id,
        stage_id=stage_ids[0] if len(stage_ids) == 1 else None,
        payload={"graph_trace_index": len(trace) - 1, "stage_ids": stage_ids, **payload},
    )
    runtime_state = graph_state.get("runtime_state")
    if isinstance(runtime_state, _RunState):
        _append_flow_log(
            runtime_state.logs,
            event="langgraph_node_event",
            level="info",
            node_id=node_id,
            graph_event=event,
            graph_payload=_compact_json(payload, max_list_items=8),
        )
    _sync_lg_c1_canonical_mirror_channels(graph_state)


def _initial_run_id(nl: str, runtime_cfg: FullStagedRuntimeConfig) -> str:
    if runtime_cfg.run_id:
        return runtime_cfg.run_id
    input_hash = hashlib.sha256(f"{nl}\n{runtime_cfg.initial_dsl}".encode("utf-8")).hexdigest()[:12]
    return f"pr-langgraph-{input_hash}-{uuid.uuid4().hex[:12]}"


def _run_initial_modeling_node_logic(*, nl: str, runtime_cfg: FullStagedRuntimeConfig, adapters: FullStagedRuntimeAdapters, state: _RunState) -> None:
    if adapters.initial_modeling is None:
        return
    _append_flow_log(
        state.logs,
        event="stage_enter",
        stage_id=StageId.SL_1_INITIAL_MODELING.value,
        reason="initial_modeling_adapter_available",
        nl_hash=_hash_text(nl),
    )
    initial_context = StageContext(nl=nl, current_dsl=state.current_dsl, grounding_map=runtime_cfg.grounding_map)
    initial_run = adapters.initial_modeling(nl, initial_context)
    initial_run = _append_llm_stage_run(
        run=initial_run,
        expected_stage_id=StageId.SL_1_INITIAL_MODELING,
        stage_records=state.stage_records,
        iteration_stage_metas=None,
        llm_interactions=state.llm_interactions,
        logs=state.logs,
    )
    if _is_llm_stage_run(initial_run):
        parsed_output = getattr(initial_run, "parsed_output", {}) or {}
        if isinstance(parsed_output, dict) and parsed_output.get("candidate_dsl"):
            state.current_dsl = str(parsed_output["candidate_dsl"])
            _append_flow_log(
                state.logs,
                event="stage_result",
                stage_id=StageId.SL_1_INITIAL_MODELING.value,
                ok=True,
                candidate_dsl_hash=_hash_text(state.current_dsl),
                grounding_seed_count=len(parsed_output.get("grounding_seeds") or []),
                assumption_count=len(parsed_output.get("assumptions") or []),
                jump="SD-2",
                candidate_dsl=state.current_dsl,
            )
            seeds = parsed_output.get("grounding_seeds") or []
            assumptions = parsed_output.get("assumptions") or []
            if seeds and runtime_cfg.grounding_map is None:
                try:
                    runtime_cfg.grounding_map = GroundingMap(
                        elements=[GroundedElement(**item) if isinstance(item, dict) else item for item in seeds],
                        source_summary={
                            "source_stage": StageId.SL_1_INITIAL_MODELING.value,
                            "assumptions": assumptions,
                        },
                    )
                except Exception as exc:
                    _append_flow_log(
                        state.logs,
                        event="grounding_seed_coercion_failed",
                        level="warning",
                        stage_id=StageId.SL_1_INITIAL_MODELING.value,
                        message=str(exc),
                    )
    elif isinstance(initial_run, str) and initial_run:
        state.current_dsl = initial_run
        _append_flow_log(
            state.logs,
            event="stage_result",
            stage_id=StageId.SL_1_INITIAL_MODELING.value,
            ok=True,
            candidate_dsl_hash=_hash_text(state.current_dsl),
            jump="SD-2",
            candidate_dsl=state.current_dsl,
        )






def _build_graph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    checkpointer: Any | None = None,
    store: Any | None = None,
) -> Any:
    from method.langgraph.nodes.sc import register_sc_nodes
    from method.langgraph.nodes.sd import register_sd_nodes
    from method.langgraph.nodes.sl import register_sl_nodes
    from method.langgraph.subgraphs.repair import _build_repair_subgraph
    from method.langgraph.subgraphs.validation import _build_validation_subgraph
    from method.langgraph.subgraphs.waiver import (
        _build_waiver_continuation_subgraph,
        _build_waiver_entry_envelope,
        _drop_repair_subgraph_state,
        _seed_waiver_exception_evidence,
    )
    graph = StateGraph(_GraphLoopState)
    store = store or InMemoryStore()
    store_instance_id = f"lg-a2-store-{uuid.uuid4().hex[:12]}"
    transient_lifecycle: dict[str, Any] = {
        "backend": "langgraph_inmemory_store",
        "namespace": "",
        "store_instance_id": store_instance_id,
        "put_count": 0,
        "get_count": 0,
        "drop_count": 0,
        "final_item_count": 0,
        "cleanup_status": "not_finalized",
        "final_drain_count": 0,
        "drained_item_count": 0,
        "cleanup_errors": [],
    }
    validation_subgraph = _build_validation_subgraph(runtime_cfg=runtime_cfg, adapters=adapters)
    waiver_continuation_subgraph = _build_waiver_continuation_subgraph(validation_subgraph=validation_subgraph)
    repair_subgraph = _build_repair_subgraph(runtime_cfg=runtime_cfg, adapters=adapters)

    def _set_transient_run_metadata(run_id: str) -> None:
        transient_lifecycle["namespace"] = _transient_namespace_label(run_id)

    def _transient_metadata() -> dict[str, Any]:
        return _jsonable(transient_lifecycle)

    def _drop_state_validation_ref(graph_state: _GraphLoopState) -> None:
        runtime_state = graph_state.get("runtime_state")
        run_id = runtime_state.run_id if isinstance(runtime_state, _RunState) else runtime_cfg.run_id
        _drop_transient(run_id, str(graph_state.get("validation_ref") or ""), lifecycle=transient_lifecycle)
        graph_state.pop("validation_ref", None)

    def _drop_validation_subgraph_state(graph_state: _GraphLoopState) -> None:
        """Keep non-serializable validation working objects out of checkpoints."""

        for key in list(graph_state.keys()):
            if str(key).startswith("validation_") and key not in {"validation_ref"}:
                graph_state.pop(key, None)

    def _drop_waiver_subgraph_state(graph_state: _GraphLoopState) -> None:
        """Keep LG-B3 waiver subgraph transient channels out of checkpoints."""

        for key in list(graph_state.keys()):
            if str(key).startswith("waiver_"):
                graph_state.pop(key, None)

    def _inject_transient_metadata(record: Any) -> None:
        lifecycle = _transient_metadata()
        record.environment.update(
            {
                "transient_backend": lifecycle["backend"],
                "transient_namespace": lifecycle["namespace"],
                "transient_store_instance_id": lifecycle["store_instance_id"],
                "transient_put_count": lifecycle["put_count"],
                "transient_get_count": lifecycle["get_count"],
                "transient_drop_count": lifecycle["drop_count"],
                "transient_final_item_count": lifecycle["final_item_count"],
                "transient_cleanup_status": lifecycle["cleanup_status"],
                "transient_final_drain_count": lifecycle["final_drain_count"],
            }
        )
        record.run_config["transient_lifecycle"] = lifecycle
        record.final_artifacts["transient_lifecycle"] = lifecycle

    def sc0_start(graph_state: _GraphLoopState) -> Command:
        nl = graph_state["nl"]
        run_id = _initial_run_id(nl, runtime_cfg)
        _set_transient_run_metadata(run_id)
        runtime_state = _RunState(run_id=run_id, run_started_at=_utc_now(), current_dsl=runtime_cfg.initial_dsl)
        graph_state = dict(graph_state)
        graph_state["runtime_state"] = runtime_state
        graph_state["iteration"] = 0
        _trace_node(graph_state, "sc0_start")
        _append_stage(runtime_state.stage_records, _meta(StageId.SC_0_START, ok=True))
        _append_flow_log(
            runtime_state.logs,
            event="run_start",
            stage_id=StageId.SC_0_START.value,
            run_id=run_id,
            max_iterations=runtime_cfg.max_iterations,
            scenario_max_retries=runtime_cfg.scenario_max_retries,
            adapter_mode=runtime_cfg.adapter_mode,
            real_llm_provider_api=runtime_cfg.real_llm_provider_api,
            initial_dsl_hash=_hash_text(runtime_state.current_dsl),
            initial_dsl=runtime_state.current_dsl,
            graph_runtime_backend="langgraph",
        )
        return Command(goto="sl1_initial_modeling", update=graph_state)

    def sl1_initial_modeling(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        _trace_node(graph_state, "sl1_initial_modeling")
        runtime_state = graph_state["runtime_state"]
        try:
            _lg_d2_wrap_llm_stage_node(
                graph_state,
                stage_id=StageId.SL_1_INITIAL_MODELING,
                graph_node="sl1_initial_modeling",
                subgraph_id=None,
                call=lambda: _run_initial_modeling_node_logic(nl=graph_state["nl"], runtime_cfg=runtime_cfg, adapters=adapters, state=runtime_state),
            )
        except _LLMRetryExhausted as exc:
            _mark_retry_exhausted(runtime_state, exc)
        if runtime_cfg.max_iterations == 0 and runtime_state.verdict_source_stage_id is None:
            _mark_sc12_verdict(
                runtime_state,
                verdict="not_converged",
                source_stage_id=StageId.SC_0_START.value,
                reason="max_iterations=0 leaves no SD-2 validation budget",
                record_status="budget_exhausted",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
        graph_state["runtime_state"] = runtime_state
        return Command(goto="iteration_gate", update=graph_state)

    def iteration_gate(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        _trace_node(graph_state, "iteration_gate", iteration=graph_state.get("iteration"))
        runtime_state: _RunState = graph_state["runtime_state"]
        if runtime_state.verdict_source_stage_id is not None:
            return Command(goto="sc13_trace_audit", update=graph_state)
        if int(graph_state.get("iteration", 0)) >= runtime_cfg.max_iterations:
            return Command(goto="sc12_budget_exhausted", update=graph_state)
        return Command(goto="validation_pass", update=graph_state)

    def validation_pass(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = int(graph_state.get("iteration", 0))
        _trace_node(graph_state, "validation_pass", iteration=iteration)
        _append_flow_log(
            runtime_state.logs,
            event="iteration_enter",
            iteration=iteration,
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            scenario_set_id=runtime_state.scenario_set.scenario_set_id if runtime_state.scenario_set is not None else None,
            oracle_weak=runtime_state.oracle_weak,
            graph_node="validation_pass",
        )
        iteration_stage_start = len(runtime_state.stage_records)
        graph_state["iteration_stage_start"] = iteration_stage_start
        try:
            graph_state = dict(
                validation_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:validation:{iteration}"}},
                )
            )
            runtime_state = graph_state["runtime_state"]
            validation = graph_state.get("validation_result")
            if not isinstance(validation, _ValidationPass):
                raise TypeError("validation subgraph did not return a _ValidationPass")
            _drop_validation_subgraph_state(graph_state)
        except _LLMRetryExhausted as exc:
            _drop_validation_subgraph_state(graph_state)
            _mark_retry_exhausted(runtime_state, exc)
            runtime_state.iteration_records.append(
                {
                    "iteration": iteration,
                    "dsl_hash": _hash_text(runtime_state.current_dsl),
                    "stage_ids": _stage_ids(runtime_state.stage_records[iteration_stage_start:]),
                    "selected_feedback": None,
                    "scenario_epoch": None,
                    "oracle_weak": runtime_state.oracle_weak,
                    "scenario_set_id": runtime_state.scenario_set.scenario_set_id if runtime_state.scenario_set is not None else None,
                    "exit_reason": runtime_state.verdict_reason,
                }
            )
            graph_state["runtime_state"] = runtime_state
            _drop_state_validation_ref(graph_state)
            return Command(goto="validation_decision", update=graph_state)

        runtime_state.warning_budget_state = validation.context.warning_budget_state
        runtime_state.scenario_set = validation.scenario_set
        if validation.scenario_set is not None:
            runtime_state.scenario_epoch = max(runtime_state.scenario_epoch, validation.scenario_set.epoch + 1)
        runtime_state.oracle_weak = validation.oracle_weak
        runtime_state.scenario_history.extend(validation.scenario_history)
        _record_deterministic_iteration(runtime_state, iteration, validation)

        selected_trace = None
        if validation.selected is not None:
            source, selected_feedback, source_stage = validation.selected
            selected_trace = _selected_feedback_trace(source, selected_feedback, source_stage, scenario_set=validation.scenario_set)
        _append_flow_log(
            runtime_state.logs,
            event="iteration_validation_result",
            iteration=iteration,
            selected_feedback=selected_trace,
            stage_ids=_stage_ids(validation.stage_metas),
            scenario_set_id=validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            oracle_weak=runtime_state.oracle_weak,
            jump="SC-12 success" if selected_trace is None else "SD-8 repair",
            graph_node="validation_pass",
        )

        graph_state["runtime_state"] = runtime_state
        old_ref = graph_state.get("validation_ref")
        if isinstance(old_ref, str):
            _drop_transient(runtime_state.run_id, old_ref, lifecycle=transient_lifecycle)
        graph_state["validation_ref"] = _put_transient(runtime_state.run_id, "validation", iteration, validation, lifecycle=transient_lifecycle)
        graph_state["selected_trace"] = selected_trace
        graph_state["iteration_record"] = {
            "iteration": iteration,
            "dsl_hash": _hash_text(runtime_state.current_dsl),
            "stage_ids": _stage_ids(validation.stage_metas),
            "selected_feedback": selected_trace,
            "scenario_epoch": validation.scenario_epoch,
            "oracle_weak": runtime_state.oracle_weak,
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
        }
        return Command(goto="validation_decision", update=graph_state)

    def validation_decision(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration_record = dict(graph_state.get("iteration_record") or {})
        _trace_node(graph_state, "validation_decision", iteration=graph_state.get("iteration"))
        if runtime_state.verdict_source_stage_id is not None:
            _drop_state_validation_ref(graph_state)
            return Command(goto="sc13_trace_audit", update=graph_state)
        validation_ref = str(graph_state.get("validation_ref") or "")
        validation = _get_transient(runtime_state.run_id, validation_ref, lifecycle=transient_lifecycle) if validation_ref else None
        weak_sim_feedback = getattr(validation, "feedback", {}).get("sim") if validation is not None else None
        if (
            getattr(validation, "selected", None) is None
            and isinstance(weak_sim_feedback, SimFeedback)
            and not weak_sim_feedback.ok
            and getattr(weak_sim_feedback, "oracle_weak", False)
        ):
            reason = f"sim_failed_but_oracle_weak:{getattr(weak_sim_feedback, 'weak_oracle_reason', '') or 'weak_oracle'}"
            _mark_sc12_verdict(
                runtime_state,
                verdict="not_converged",
                source_stage_id=StageId.SD_6_SIM.value,
                reason=reason,
                record_status="failed",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            iteration_record["exit_reason"] = reason
            runtime_state.iteration_records.append(iteration_record)
            command_goto = "sc13_trace_audit"
        elif getattr(validation, "selected", None) is None:
            stage_metas = getattr(validation, "stage_metas", []) or []
            source_stage_id = stage_metas[-1].stage_id if stage_metas else StageId.SC_0_START.value
            _mark_sc12_verdict(
                runtime_state,
                verdict="success",
                source_stage_id=source_stage_id,
                reason="full_pass_all_required_feedback_ok",
            )
            iteration_record["exit_reason"] = "full_pass_all_required_feedback_ok"
            runtime_state.iteration_records.append(iteration_record)
            command_goto = "sc13_trace_audit"
        else:
            command_goto = "repair_path"
        graph_state["runtime_state"] = runtime_state
        graph_state["iteration_record"] = iteration_record
        if command_goto != "repair_path":
            _drop_state_validation_ref(graph_state)
        return Command(goto=command_goto, update=graph_state)

    def repair_path(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = int(graph_state.get("iteration", 0))
        iteration_stage_start = int(graph_state.get("iteration_stage_start", len(runtime_state.stage_records)))
        iteration_record = dict(graph_state.get("iteration_record") or {})
        _trace_node(graph_state, "repair_path", iteration=iteration)
        validation_ref = str(graph_state.get("validation_ref") or "")
        validation = _get_transient(runtime_state.run_id, validation_ref, lifecycle=transient_lifecycle) if validation_ref else None
        if not isinstance(validation, _ValidationPass):
            raise TypeError("repair_path requires validation_ref pointing to a _ValidationPass")
        try:
            graph_state["repair_validation"] = validation
            graph_state = dict(
                repair_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:repair:{iteration}"}},
                )
            )
            runtime_state = graph_state["runtime_state"]
            accepted = bool(graph_state.get("repair_accepted"))
            repair_patch = dict(graph_state.get("repair_patch") or {})
            _drop_repair_subgraph_state(graph_state)
            graph_state["repair_patch"] = repair_patch
        except _LLMRetryExhausted as exc:
            _drop_repair_subgraph_state(graph_state)
            _mark_retry_exhausted(runtime_state, exc)
            iteration_record["exit_reason"] = runtime_state.verdict_reason
            iteration_record["repair_stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])[len(iteration_record.get("stage_ids") or []) :]
            runtime_state.iteration_records.append(iteration_record)
            graph_state["runtime_state"] = runtime_state
            graph_state["iteration_record"] = iteration_record
            return Command(goto="repair_decision", update=graph_state)
        iteration_record.update(repair_patch)
        _append_flow_log(
            runtime_state.logs,
            event="iteration_repair_result",
            iteration=iteration,
            accepted=accepted,
            repair_patch=_compact_json(repair_patch, max_list_items=10),
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            jump=(
                "waiver_continue"
                if bool(repair_patch.get("waiver_continue")) and not accepted
                else ("SD-2 next iteration" if accepted else "SC-12 or retry")
            ),
            graph_node="repair_path",
            graph_subgraph="repair_subgraph",
        )
        graph_state["runtime_state"] = runtime_state
        graph_state["iteration_record"] = iteration_record
        graph_state["accepted"] = accepted
        graph_state["repair_patch"] = repair_patch
        return Command(goto="repair_decision", update=graph_state)

    def repair_decision(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = int(graph_state.get("iteration", 0))
        iteration_record = dict(graph_state.get("iteration_record") or {})
        accepted = bool(graph_state.get("accepted"))
        repair_patch = dict(graph_state.get("repair_patch") or {})
        _trace_node(graph_state, "repair_decision", iteration=iteration, accepted=accepted)
        if runtime_state.verdict_source_stage_id is not None:
            command_goto = "sc13_trace_audit"
        elif bool(repair_patch.get("waiver_continue")) and not accepted:
            command_goto = "waiver_continue"
        elif not accepted:
            reason = iteration_record.get("exit_reason") or "repair review rejected candidate"
            can_retry_rejection = (
                runtime_state.pending_repair_rejection is not None
                and runtime_state.pending_original_fix_plan is not None
                and iteration + 1 < runtime_cfg.max_iterations
            )
            if can_retry_rejection:
                iteration_record["exit_reason"] = "repair_review_rejected_retry_with_revised_fix_plan"
                iteration_record["next_iteration_repair_plan"] = "RevisedFixPlan"
                runtime_state.iteration_records.append(iteration_record)
                graph_state["iteration"] = iteration + 1
                command_goto = "iteration_gate"
            else:
                reason = _final_rejection_reason(iteration_record=iteration_record, repair_history=runtime_state.repair_history)
                iteration_record["exit_reason"] = reason
                _mark_sc12_verdict(
                    runtime_state,
                    verdict="not_converged",
                    source_stage_id=_final_rejection_source_stage_id(iteration_record),
                    reason=str(reason),
                    record_status="rejected",
                    result_status="not_converged",
                    stage_ok=False,
                    stage_status=StageStatus.FAIL,
                )
                runtime_state.iteration_records.append(iteration_record)
                command_goto = "sc13_trace_audit"
        elif iteration + 1 >= runtime_cfg.max_iterations:
            iteration_record["budget_gate"] = {
                "source_stage_id": StageId.SC_11_ACCEPT_CANDIDATE.value,
                "iter_plus_one": iteration + 1,
                "max_iterations": runtime_cfg.max_iterations,
                "next_stage_allowed": False,
                "post_accept_validation_attempted": True,
            }
            _append_flow_log(
                runtime_state.logs,
                event="post_accept_validation_enter",
                stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                iteration=iteration,
                reason="SC-11 accepted candidate but no next global iteration remains; run same-iteration full validation",
                current_dsl_hash=_hash_text(runtime_state.current_dsl),
                current_dsl=runtime_state.current_dsl,
                scenario_set_id=runtime_state.scenario_set.scenario_set_id if runtime_state.scenario_set is not None else None,
                oracle_weak=runtime_state.oracle_weak,
                jump="SD-2 post_accept_validation",
                graph_node="repair_decision",
            )
            try:
                graph_state.pop("validation_continuation_source", None)
                graph_state = dict(
                    validation_subgraph.invoke(
                        graph_state,
                        config={"configurable": {"thread_id": f"{runtime_state.run_id}:validation-post-accept:{iteration}"}},
                    )
                )
                runtime_state = graph_state["runtime_state"]
                post_accept_validation = graph_state.get("validation_result")
                if not isinstance(post_accept_validation, _ValidationPass):
                    raise TypeError("validation subgraph did not return a _ValidationPass after post-accept validation")
                _drop_validation_subgraph_state(graph_state)
            except _LLMRetryExhausted as exc:
                _drop_validation_subgraph_state(graph_state)
                _mark_retry_exhausted(runtime_state, exc)
                iteration_record["exit_reason"] = runtime_state.verdict_reason
                iteration_record["post_accept_stage_ids"] = _stage_ids(runtime_state.stage_records[int(graph_state.get("iteration_stage_start", len(runtime_state.stage_records))):])[len(iteration_record.get("stage_ids") or []) :]
                runtime_state.iteration_records.append(iteration_record)
                command_goto = "sc13_trace_audit"
                graph_state["runtime_state"] = runtime_state
                graph_state["iteration_record"] = iteration_record
                _drop_state_validation_ref(graph_state)
                return Command(goto=command_goto, update=graph_state)

            runtime_state.warning_budget_state = post_accept_validation.context.warning_budget_state
            runtime_state.scenario_set = post_accept_validation.scenario_set
            if post_accept_validation.scenario_set is not None:
                runtime_state.scenario_epoch = max(runtime_state.scenario_epoch, post_accept_validation.scenario_set.epoch + 1)
            runtime_state.oracle_weak = post_accept_validation.oracle_weak
            runtime_state.scenario_history.extend(post_accept_validation.scenario_history)
            runtime_state.deterministic_feedback["iterations"].append(
                {
                    "iteration": iteration,
                    "post_accept_validation": True,
                    "parse": _jsonable(post_accept_validation.feedback.get(FeedbackSource.PARSE.value)),
                    "semantic": _jsonable(post_accept_validation.feedback.get(FeedbackSource.SEMANTIC.value)),
                    "design": _jsonable(post_accept_validation.feedback.get(FeedbackSource.DESIGN.value)),
                    "sim": _jsonable(post_accept_validation.feedback.get(FeedbackSource.SIM.value)),
                    "model_review": _jsonable(post_accept_validation.feedback.get(FeedbackSource.MODEL_REVIEW.value)),
                    "stage_ids": _stage_ids(post_accept_validation.stage_metas),
                    "scenario_epoch": post_accept_validation.scenario_epoch,
                    "oracle_weak": post_accept_validation.oracle_weak,
                    "langgraph_subgraph": "validation_subgraph",
                }
            )
            if post_accept_validation.selected is not None:
                source, feedback_obj, source_stage = post_accept_validation.selected
                iteration_record["post_accept_selected_feedback"] = _selected_feedback_trace(
                    source, feedback_obj, source_stage, scenario_set=post_accept_validation.scenario_set
                )
            else:
                iteration_record["post_accept_selected_feedback"] = None
            iteration_record["post_accept_stage_ids"] = _stage_ids(post_accept_validation.stage_metas)
            iteration_record["post_accept_scenario_epoch"] = post_accept_validation.scenario_epoch
            iteration_record["post_accept_oracle_weak"] = post_accept_validation.oracle_weak
            iteration_stage_start = int(graph_state.get("iteration_stage_start", len(runtime_state.stage_records)))
            iteration_record["stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])

            weak_sim_feedback = post_accept_validation.feedback.get(FeedbackSource.SIM.value)
            if (
                post_accept_validation.selected is None
                and isinstance(weak_sim_feedback, SimFeedback)
                and not weak_sim_feedback.ok
                and getattr(weak_sim_feedback, "oracle_weak", False)
            ):
                reason = f"sim_failed_but_oracle_weak:{getattr(weak_sim_feedback, 'weak_oracle_reason', '') or 'weak_oracle'}"
                _mark_sc12_verdict(
                    runtime_state,
                    verdict="not_converged",
                    source_stage_id=StageId.SD_6_SIM.value,
                    reason=reason,
                    record_status="failed",
                    result_status="not_converged",
                    stage_ok=False,
                    stage_status=StageStatus.FAIL,
                )
                iteration_record["exit_reason"] = reason
                iteration_record["budget_gate"]["post_accept_validation_success"] = False
                runtime_state.iteration_records.append(iteration_record)
                command_goto = "sc13_trace_audit"
            elif post_accept_validation.selected is None:
                source_stage_id = post_accept_validation.stage_metas[-1].stage_id if post_accept_validation.stage_metas else StageId.SC_11_ACCEPT_CANDIDATE.value
                _mark_sc12_verdict(
                    runtime_state,
                    verdict="success",
                    source_stage_id=source_stage_id,
                    reason="full_pass_all_required_feedback_ok_after_sc11_post_accept_validation",
                )
                iteration_record["exit_reason"] = "full_pass_all_required_feedback_ok_after_sc11_post_accept_validation"
                iteration_record["budget_gate"]["post_accept_validation_success"] = True
                runtime_state.iteration_records.append(iteration_record)
                command_goto = "sc13_trace_audit"
            else:
                post_accept_waiver_audit = _stale_overridden_sd6_validation_waiver_audit(
                    validation=post_accept_validation,
                    fix_log=runtime_state.fix_log,
                    current_dsl_hash=_hash_text(runtime_state.current_dsl),
                )
                if post_accept_waiver_audit is not None:
                    graph_state["validation_continuation_source"] = post_accept_validation
                    validation_ref = _put_transient(
                        runtime_state.run_id,
                        "post_accept_validation",
                        iteration,
                        post_accept_validation,
                        lifecycle=transient_lifecycle,
                    )
                    graph_state["validation_ref"] = validation_ref
                    repair_patch = {
                        "waiver_continue": True,
                        "accepted_candidate": False,
                        "selected_feedback": iteration_record.get("post_accept_selected_feedback"),
                        "repair_stage_ids": [],
                        "waiver_audit": _jsonable(post_accept_waiver_audit),
                        "exit_reason": "post_accept_stale_overridden_scenario_waiver_continue",
                    }
                    graph_state["repair_patch"] = repair_patch
                    try:
                        graph_state = dict(
                            waiver_continuation_subgraph.invoke(
                                graph_state,
                                config={
                                    "configurable": {
                                        "thread_id": f"{runtime_state.run_id}:post-accept-waiver-continuation:{iteration}"
                                    }
                                },
                            )
                        )
                        runtime_state = graph_state["runtime_state"]
                        post_accept_continued_validation = graph_state.get("waiver_result") or graph_state.get("validation_result")
                        if not isinstance(post_accept_continued_validation, _ValidationPass):
                            raise TypeError("waiver continuation subgraph did not return a _ValidationPass after post-accept waiver")
                        waiver_input_envelope = _jsonable(graph_state.get("waiver_input_envelope") or {})
                        _drop_validation_subgraph_state(graph_state)
                        _drop_waiver_subgraph_state(graph_state)
                    except _LLMRetryExhausted as exc:
                        waiver_input_envelope = _jsonable(graph_state.get("waiver_input_envelope") or {})
                        if waiver_input_envelope:
                            _seed_waiver_exception_evidence(
                                graph_state,
                                envelope=waiver_input_envelope,
                                tail_node="waiver_sim_tail",
                                iteration=iteration,
                                retry_stage_id=exc.stage_id,
                            )
                        _drop_validation_subgraph_state(graph_state)
                        _drop_waiver_subgraph_state(graph_state)
                        _mark_retry_exhausted(runtime_state, exc)
                        iteration_record["exit_reason"] = runtime_state.verdict_reason
                        iteration_record["post_accept_waiver_audit"] = _jsonable(post_accept_waiver_audit)
                        iteration_record["waiver_entry_envelope"] = waiver_input_envelope
                        runtime_state.iteration_records.append(iteration_record)
                        command_goto = "sc13_trace_audit"
                        graph_state["runtime_state"] = runtime_state
                        graph_state["iteration_record"] = iteration_record
                        _drop_state_validation_ref(graph_state)
                        return Command(goto=command_goto, update=graph_state)

                    runtime_state.warning_budget_state = post_accept_continued_validation.context.warning_budget_state
                    runtime_state.scenario_set = post_accept_continued_validation.scenario_set
                    if post_accept_continued_validation.scenario_set is not None:
                        runtime_state.scenario_epoch = max(runtime_state.scenario_epoch, post_accept_continued_validation.scenario_set.epoch + 1)
                    runtime_state.oracle_weak = post_accept_continued_validation.oracle_weak
                    runtime_state.scenario_history.extend(post_accept_continued_validation.scenario_history)
                    runtime_state.deterministic_feedback["iterations"].append(
                        {
                            "iteration": iteration,
                            "post_accept_validation": True,
                            "continued_after_post_accept_waiver": True,
                            "waiver_audit": _jsonable(post_accept_waiver_audit),
                            "parse": _jsonable(post_accept_continued_validation.feedback.get("parse")),
                            "semantic": _jsonable(post_accept_continued_validation.feedback.get("semantic")),
                            "design": _jsonable(post_accept_continued_validation.feedback.get("design")),
                            "sim": _jsonable(post_accept_continued_validation.feedback.get("sim")),
                            "model_review": _jsonable(post_accept_continued_validation.feedback.get("model_review")),
                            "stage_ids": _stage_ids(post_accept_continued_validation.stage_metas),
                            "scenario_epoch": post_accept_continued_validation.scenario_epoch,
                            "oracle_weak": post_accept_continued_validation.oracle_weak,
                            "langgraph_subgraph": "waiver_continuation_subgraph",
                        }
                    )
                    if post_accept_continued_validation.selected is not None:
                        source, feedback_obj, source_stage = post_accept_continued_validation.selected
                        iteration_record["post_accept_waiver_selected_feedback"] = _selected_feedback_trace(
                            source,
                            feedback_obj,
                            source_stage,
                            scenario_set=post_accept_continued_validation.scenario_set,
                        )
                    else:
                        iteration_record["post_accept_waiver_selected_feedback"] = None
                    iteration_record["post_accept_waiver_audit"] = _jsonable(post_accept_waiver_audit)
                    iteration_record["post_accept_waiver_stage_ids"] = _stage_ids(
                        post_accept_continued_validation.stage_metas[len(post_accept_validation.stage_metas) :]
                    )
                    iteration_record["post_accept_waiver_scenario_epoch"] = post_accept_continued_validation.scenario_epoch
                    iteration_record["post_accept_waiver_oracle_weak"] = post_accept_continued_validation.oracle_weak
                    iteration_record["waiver_continue"] = True
                    iteration_record["waiver_audit"] = _jsonable(post_accept_waiver_audit)
                    iteration_record["waiver_entry_envelope"] = waiver_input_envelope
                    iteration_record["stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])

                    weak_sim_feedback = post_accept_continued_validation.feedback.get("sim")
                    if (
                        post_accept_continued_validation.selected is None
                        and isinstance(weak_sim_feedback, SimFeedback)
                        and not weak_sim_feedback.ok
                        and getattr(weak_sim_feedback, "oracle_weak", False)
                    ):
                        reason = f"sim_failed_but_oracle_weak:{getattr(weak_sim_feedback, 'weak_oracle_reason', '') or 'weak_oracle'}"
                        _mark_sc12_verdict(
                            runtime_state,
                            verdict="not_converged",
                            source_stage_id=StageId.SD_6_SIM.value,
                            reason=reason,
                            record_status="failed",
                            result_status="not_converged",
                            stage_ok=False,
                            stage_status=StageStatus.FAIL,
                        )
                        iteration_record["exit_reason"] = reason
                        iteration_record["budget_gate"]["post_accept_validation_success"] = False
                        runtime_state.iteration_records.append(iteration_record)
                        command_goto = "sc13_trace_audit"
                    elif post_accept_continued_validation.selected is None:
                        source_stage_id = (
                            post_accept_continued_validation.stage_metas[-1].stage_id
                            if post_accept_continued_validation.stage_metas
                            else StageId.SC_11_ACCEPT_CANDIDATE.value
                        )
                        _mark_sc12_verdict(
                            runtime_state,
                            verdict="success",
                            source_stage_id=source_stage_id,
                            reason="full_pass_all_required_feedback_ok_after_post_accept_stale_scenario_waiver",
                        )
                        iteration_record["exit_reason"] = "full_pass_all_required_feedback_ok_after_post_accept_stale_scenario_waiver"
                        iteration_record["budget_gate"]["post_accept_validation_success"] = True
                        iteration_record["budget_gate"]["post_accept_waiver_continue"] = True
                        runtime_state.iteration_records.append(iteration_record)
                        command_goto = "sc13_trace_audit"
                    else:
                        reason = _repair_selected_reason(iteration_record["post_accept_waiver_selected_feedback"])
                        _mark_sc12_verdict(
                            runtime_state,
                            verdict="not_converged",
                            source_stage_id=(iteration_record.get("post_accept_waiver_selected_feedback") or {}).get("source_stage") or StageId.SC_11_ACCEPT_CANDIDATE.value,
                            reason=str(reason),
                            record_status="budget_exhausted",
                            result_status="not_converged",
                            stage_ok=False,
                            stage_status=StageStatus.FAIL,
                        )
                        iteration_record["exit_reason"] = str(reason)
                        iteration_record["budget_gate"]["post_accept_validation_success"] = False
                        iteration_record["budget_gate"]["post_accept_waiver_continue"] = True
                        runtime_state.iteration_records.append(iteration_record)
                        command_goto = "sc13_trace_audit"
                else:
                    reason = _repair_selected_reason(iteration_record["post_accept_selected_feedback"])
                    _mark_sc12_verdict(
                        runtime_state,
                        verdict="not_converged",
                        source_stage_id=iteration_record["post_accept_selected_feedback"].get("source_stage") or StageId.SC_11_ACCEPT_CANDIDATE.value,
                        reason=str(reason),
                        record_status="budget_exhausted",
                        result_status="not_converged",
                        stage_ok=False,
                        stage_status=StageStatus.FAIL,
                    )
                    iteration_record["exit_reason"] = str(reason)
                    iteration_record["budget_gate"]["post_accept_validation_success"] = False
                    runtime_state.iteration_records.append(iteration_record)
                    command_goto = "sc13_trace_audit"
        else:
            runtime_state.iteration_records.append(iteration_record)
            graph_state["iteration"] = iteration + 1
            command_goto = "iteration_gate"
        graph_state["runtime_state"] = runtime_state
        graph_state["iteration_record"] = iteration_record
        if command_goto != "waiver_continue":
            _drop_state_validation_ref(graph_state)
        return Command(goto=command_goto, update=graph_state)

    def waiver_continue(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = int(graph_state.get("iteration", 0))
        iteration_stage_start = int(graph_state.get("iteration_stage_start", len(runtime_state.stage_records)))
        iteration_record = dict(graph_state.get("iteration_record") or {})
        validation = _get_transient(runtime_state.run_id, str(graph_state.get("validation_ref") or ""), lifecycle=transient_lifecycle)
        waiver_input_envelope: dict[str, Any] = {}
        _trace_node(graph_state, "waiver_continue", iteration=iteration)
        try:
            if not isinstance(validation, _ValidationPass):
                raise TypeError("waiver_continue requires transient validation_ref to resolve to a _ValidationPass")
            repair_patch = dict(graph_state.get("repair_patch") or {})
            validation_ref = str(graph_state.get("validation_ref") or "")
            waiver_input_envelope = _jsonable(
                _build_waiver_entry_envelope(
                    repair_patch=repair_patch,
                    validation_ref=validation_ref,
                    validation=validation,
                    iteration=iteration,
                )
            )
            graph_state["validation_continuation_source"] = validation
            graph_state = dict(
                waiver_continuation_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:waiver-continuation:{iteration}"}},
                )
            )
            runtime_state = graph_state["runtime_state"]
            continued_validation = graph_state.get("waiver_result") or graph_state.get("validation_result")
            if not isinstance(continued_validation, _ValidationPass):
                raise TypeError("waiver continuation subgraph did not return a _ValidationPass result")
            waiver_input_envelope = _jsonable(graph_state.get("waiver_input_envelope") or {})
            _drop_validation_subgraph_state(graph_state)
            _drop_waiver_subgraph_state(graph_state)
        except _LLMRetryExhausted as exc:
            if waiver_input_envelope:
                _seed_waiver_exception_evidence(
                    graph_state,
                    envelope=waiver_input_envelope,
                    tail_node=(
                        "waiver_sim_tail"
                        if str(waiver_input_envelope.get("tail_start_stage") or "") == StageId.SD_6_SIM.value
                        else "waiver_design_tail"
                    ),
                    iteration=iteration,
                    retry_stage_id=exc.stage_id,
                )
            waiver_input_envelope = _jsonable(
                graph_state.get("waiver_input_envelope")
                or graph_state.get("waiver_retry_error_envelope")
                or waiver_input_envelope
                or {}
            )
            _drop_validation_subgraph_state(graph_state)
            _drop_waiver_subgraph_state(graph_state)
            _mark_retry_exhausted(runtime_state, exc)
            iteration_record["exit_reason"] = runtime_state.verdict_reason
            iteration_record["repair_stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])[len(iteration_record.get("stage_ids") or []) :]
            iteration_record["waiver_entry_envelope"] = waiver_input_envelope
            runtime_state.iteration_records.append(iteration_record)
            command_goto = "sc13_trace_audit"
            graph_state["runtime_state"] = runtime_state
            graph_state["iteration_record"] = iteration_record
            _drop_state_validation_ref(graph_state)
            return Command(goto=command_goto, update=graph_state)

        runtime_state.warning_budget_state = continued_validation.context.warning_budget_state
        runtime_state.scenario_set = continued_validation.scenario_set
        if continued_validation.scenario_set is not None:
            runtime_state.scenario_epoch = max(runtime_state.scenario_epoch, continued_validation.scenario_set.epoch + 1)
        runtime_state.oracle_weak = continued_validation.oracle_weak
        runtime_state.scenario_history.extend(continued_validation.scenario_history)
        runtime_state.deterministic_feedback["iterations"].append(
            {
                "iteration": iteration,
                "continued_after_waiver": True,
                "parse": _jsonable(continued_validation.feedback.get("parse")),
                "semantic": _jsonable(continued_validation.feedback.get("semantic")),
                "design": _jsonable(continued_validation.feedback.get("design")),
                "sim": _jsonable(continued_validation.feedback.get("sim")),
                "model_review": _jsonable(continued_validation.feedback.get("model_review")),
                "stage_ids": _stage_ids(continued_validation.stage_metas),
                "scenario_epoch": continued_validation.scenario_epoch,
                "oracle_weak": continued_validation.oracle_weak,
                "langgraph_subgraph": "validation_subgraph",
            }
        )
        if continued_validation.selected is not None:
            source, feedback_obj, source_stage = continued_validation.selected
            iteration_record["post_waiver_selected_feedback"] = _selected_feedback_trace(
                source,
                feedback_obj,
                source_stage,
                scenario_set=continued_validation.scenario_set,
            )
        else:
            iteration_record["post_waiver_selected_feedback"] = None
        iteration_record["post_waiver_stage_ids"] = _stage_ids(continued_validation.stage_metas[len(validation.stage_metas) :])
        iteration_record["post_waiver_scenario_epoch"] = continued_validation.scenario_epoch
        iteration_record["post_waiver_oracle_weak"] = continued_validation.oracle_weak
        iteration_record["waiver_entry_envelope"] = waiver_input_envelope
        iteration_record["stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])

        weak_sim_feedback = continued_validation.feedback.get("sim")
        if (
            continued_validation.selected is None
            and isinstance(weak_sim_feedback, SimFeedback)
            and not weak_sim_feedback.ok
            and getattr(weak_sim_feedback, "oracle_weak", False)
        ):
            reason = f"sim_failed_but_oracle_weak:{getattr(weak_sim_feedback, 'weak_oracle_reason', '') or 'weak_oracle'}"
            _mark_sc12_verdict(
                runtime_state,
                verdict="not_converged",
                source_stage_id=StageId.SD_6_SIM.value,
                reason=reason,
                record_status="failed",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            iteration_record["exit_reason"] = reason
            runtime_state.iteration_records.append(iteration_record)
            command_goto = "sc13_trace_audit"
        elif continued_validation.selected is None:
            source_stage_id = continued_validation.stage_metas[-1].stage_id if continued_validation.stage_metas else StageId.SD_4_DESIGN.value
            _mark_sc12_verdict(
                runtime_state,
                verdict="success",
                source_stage_id=source_stage_id,
                reason="full_pass_all_required_feedback_ok_after_waiver_continue",
            )
            iteration_record["exit_reason"] = "full_pass_all_required_feedback_ok_after_waiver_continue"
            runtime_state.iteration_records.append(iteration_record)
            command_goto = "sc13_trace_audit"
        else:
            iteration_record["exit_reason"] = "waiver_continue_revealed_downstream_blocking_feedback"
            runtime_state.iteration_records.append(iteration_record)
            if iteration + 1 >= runtime_cfg.max_iterations:
                reason = _final_rejection_reason(
                    iteration_record={"selected_feedback": iteration_record.get("post_waiver_selected_feedback")},
                    repair_history=runtime_state.repair_history,
                )
                _mark_sc12_verdict(
                    runtime_state,
                    verdict="not_converged",
                    source_stage_id=(iteration_record.get("post_waiver_selected_feedback") or {}).get("source_stage") or StageId.SD_4_DESIGN.value,
                    reason=str(reason),
                    record_status="budget_exhausted",
                    result_status="not_converged",
                    stage_ok=False,
                    stage_status=StageStatus.FAIL,
                )
                command_goto = "sc13_trace_audit"
            else:
                graph_state["iteration"] = iteration + 1
                command_goto = "iteration_gate"
        graph_state["runtime_state"] = runtime_state
        graph_state["iteration_record"] = iteration_record
        if command_goto != "iteration_gate":
            _drop_state_validation_ref(graph_state)
        return Command(goto=command_goto, update=graph_state)

    def sc12_budget_exhausted(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        _trace_node(graph_state, "sc12_budget_exhausted", iteration=graph_state.get("iteration"))
        if runtime_state.verdict_source_stage_id is None:
            source_stage_id = StageId.SC_11_ACCEPT_CANDIDATE.value
            reason = "max_iterations exhausted"
            if runtime_state.iteration_records:
                last_iter = runtime_state.iteration_records[-1]
                selected = last_iter.get("post_waiver_selected_feedback") or last_iter.get("selected_feedback")
                if isinstance(selected, dict):
                    source_stage_id = str(selected.get("source_stage") or source_stage_id)
                    reason = _repair_selected_reason(selected)
            _mark_sc12_verdict(
                runtime_state,
                verdict="not_converged",
                source_stage_id=source_stage_id,
                reason=reason,
                record_status="budget_exhausted",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
        graph_state["runtime_state"] = runtime_state
        _drop_state_validation_ref(graph_state)
        return Command(goto="sc13_trace_audit", update=graph_state)

    def sc13_trace_audit(graph_state: _GraphLoopState) -> Command:
        graph_state = dict(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        _trace_node(graph_state, "sc13_trace_audit")
        _drain_transients(runtime_state.run_id, lifecycle=transient_lifecycle)
        if runtime_state.final_record_status not in _VALID_RECORD_STATUSES:
            runtime_state.final_record_status = "failed"
            runtime_state.final_verdict = "not_converged"
            runtime_state.result_status = "not_converged"
            if runtime_state.error_message is None:
                runtime_state.error_message = "runtime exited without convergence"

        _append_stage(runtime_state.stage_records, _meta(StageId.SC_13_TRACE_AUDIT, ok=True))
        _append_flow_log(
            runtime_state.logs,
            event="run_end",
            stage_id=StageId.SC_13_TRACE_AUDIT.value,
            run_id=runtime_state.run_id,
            verdict=runtime_state.final_verdict,
            result_status=runtime_state.result_status,
            record_status=runtime_state.final_record_status,
            final_dsl_hash=_hash_text(runtime_state.current_dsl),
            stage_count=len(runtime_state.stage_records),
            iteration_count=len(runtime_state.iteration_records),
            repair_count=len(runtime_state.repair_history),
            final_dsl=runtime_state.current_dsl,
            graph_runtime_backend="langgraph",
        )
        _sync_lg_c1_canonical_mirror_channels(graph_state)

        result = AgentLoopResult(
            final_dsl=runtime_state.current_dsl,
            status=runtime_state.result_status,  # type: ignore[arg-type]
            error_message=runtime_state.error_message,
            llm_model=runtime_cfg.provider_model_redacted or "none-pr-langgraph-explicit-adapters",
            run_record_id=runtime_state.run_id,
        )

        if runtime_cfg.write_run_record:
            record = _build_record(cfg=runtime_cfg, nl=graph_state["nl"], state=runtime_state)
            _inject_transient_metadata(record)
            _inject_lg_c1_graph_state_readiness(record, graph_state)
            try:
                path = staged_runtime.write_agent_loop_run_record(record, staged_runtime.agent_loop_run_record_path(runtime_cfg.output_dir, runtime_state.run_id))
                result.run_record_path = str(path)
                if record.status == "invalid" and record.final_artifacts.get("redaction_failed") is True:
                    result.status = "spec_failed"
                    result.error_message = str(record.final_artifacts.get("error_message") or "run record redaction failed")
            except Exception as exc:
                result.status = "spec_failed"
                result.error_message = f"run record write failed: {type(exc).__name__}: {str(exc)[:300]}"
                result.run_record_path = None
        graph_state["runtime_state"] = runtime_state
        graph_state["runtime_result"] = result
        return Command(goto=END, update=graph_state)

    register_sc_nodes(
        graph,
        sc0_start=sc0_start,
        iteration_gate=iteration_gate,
        validation_decision=validation_decision,
        repair_decision=repair_decision,
        waiver_continue=waiver_continue,
        sc12_budget_exhausted=sc12_budget_exhausted,
        sc13_trace_audit=sc13_trace_audit,
    )
    register_sl_nodes(graph, sl1_initial_modeling=sl1_initial_modeling)
    register_sd_nodes(graph, validation_pass=validation_pass, repair_path=repair_path)

    graph.add_edge(START, "sc0_start")
    checkpointer = checkpointer or InMemorySaver(serde=_PickleCheckpointSerde())
    return graph.compile(checkpointer=checkpointer, store=store)







def _augment_run_record_with_graph_trace(result: AgentLoopResult, graph_trace: list[dict[str, Any]]) -> None:
    if not result.run_record_path:
        return
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    safe_trace = _jsonable(graph_trace)
    record.environment["langgraph_node_trace_count"] = len(safe_trace)
    record.environment["langgraph_node_trace_hash"] = _hash_payload(safe_trace)
    record.run_config["langgraph_node_trace"] = safe_trace
    record.logs.append(
        {
            "event": "langgraph_node_trace",
            "instrumentation_layer": "langgraph",
            "node_trace": safe_trace,
            "node_trace_hash": record.environment["langgraph_node_trace_hash"],
        }
    )
    validation_stage_node_order = [
        "validation_sd2_parse",
        "validation_sd3_semantic",
        "validation_sd4_design",
        "validation_sd5a_reuse_coverage",
        "validation_sl5_scenario_generation",
        "validation_sd5a_scenario_coverage",
        "validation_sc5f_scenario_freeze",
        "validation_sd6_sim",
        "validation_sl7_model_review",
    ]
    validation_subgraph_node_order = [
        "validation_subgraph",
        *validation_stage_node_order,
        "validation_finalize",
    ]
    validation_subgraph_node_ids = set(validation_subgraph_node_order)
    validation_trace = [
        item for item in safe_trace if str(item.get("node_id") or "") in validation_subgraph_node_ids
    ]
    validation_seen = {str(item.get("node_id") or "") for item in validation_trace}
    validation_subgraph_runtime_trace = {
        "subgraph_id": "validation_subgraph",
        "node_trace_count": len(validation_trace),
        "node_trace_hash": _hash_payload(validation_trace),
        "stage_node_ids": [node_id for node_id in validation_stage_node_order if node_id in validation_seen],
        "node_ids": [str(item.get("node_id") or "") for item in validation_trace],
        "join_key_fields": [
            "iteration",
            "attempt_index",
            "validation_ref",
            "validation_stage_ids",
            "scenario_set_id",
            "selected_feedback_kind",
            "continued_after_waiver",
        ],
    }
    repair_stage_node_order = [
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
    ]
    repair_subgraph_node_order = [
        "repair_enter",
        *repair_stage_node_order,
        "repair_finalize",
    ]
    repair_subgraph_node_ids = set(repair_subgraph_node_order)
    repair_trace = [
        item for item in safe_trace if str(item.get("node_id") or "") in repair_subgraph_node_ids
    ]
    repair_seen = {str(item.get("node_id") or "") for item in repair_trace}
    repair_subgraph_runtime_trace = {
        "subgraph_id": "repair_subgraph",
        "node_trace_count": len(repair_trace),
        "node_trace_hash": _hash_payload(repair_trace),
        "stage_node_ids": [node_id for node_id in repair_stage_node_order if node_id in repair_seen],
        "node_ids": [str(item.get("node_id") or "") for item in repair_trace],
        "join_key_fields": [
            "iteration",
            "batch_id",
            "request_id",
            "candidate_dsl_hash",
            "repair_stage_ids",
            "fix_log_entry_count",
        ],
    }
    waiver_subgraph_node_order = [
        "waiver_subgraph_enter",
        "waiver_tail_decision",
        "waiver_design_tail",
        "waiver_sim_tail",
        "waiver_subgraph_finalize",
    ]
    waiver_subgraph_node_ids = set(waiver_subgraph_node_order)
    waiver_trace = [
        item for item in safe_trace if str(item.get("node_id") or "") in waiver_subgraph_node_ids
    ]
    waiver_seen = {str(item.get("node_id") or "") for item in waiver_trace}
    waiver_subgraph_runtime_trace = {
        "subgraph_id": "waiver_continuation_subgraph",
        "node_trace_count": len(waiver_trace),
        "node_trace_hash": _hash_payload(waiver_trace),
        "node_ids": [str(item.get("node_id") or "") for item in waiver_trace],
        "stage_node_ids": [node_id for node_id in ("waiver_design_tail", "waiver_sim_tail") if node_id in waiver_seen],
        "nested_subgraph_ids": ["validation_subgraph"] if waiver_trace else [],
        "join_key_fields": [
            "iteration",
            "waiver_audit_kind",
            "tail_start_stage",
            "validation_ref",
            "post_waiver_stage_ids",
        ],
    }
    record.final_artifacts["langgraph_runtime_trace"] = {
        "node_trace_count": len(safe_trace),
        "node_trace_hash": record.environment["langgraph_node_trace_hash"],
        "delegated_monolithic_runtime": False,
        "validation_subgraph_runtime_trace": validation_subgraph_runtime_trace,
        "repair_subgraph_runtime_trace": repair_subgraph_runtime_trace,
        "waiver_subgraph_runtime_trace": waiver_subgraph_runtime_trace,
    }
    write_agent_loop_run_record(record, path)




def _refresh_lg_c1_readiness_after_lg_d1_operator_log(result: AgentLoopResult, graph_state: _GraphLoopState) -> None:
    """Refresh LG-C1 readiness after LG-D1 writes the complete operator log.

    The first readiness injection happens inside SC-13 before the run record is
    persisted.  LG-D1 operator artifacts are added later because they need the
    final run-record path and stage ledger.  Refreshing here lets LG-C1 audit the
    full tee-able operator log instead of only graph-state operator probes.
    """

    if not result.run_record_path:
        return
    path = result.run_record_path
    record = read_agent_loop_run_record(path)
    _inject_lg_c1_graph_state_readiness(record, graph_state)
    write_agent_loop_run_record(record, path)


# D3 exposes a neutral alias so non-core modules can refresh graph-state
# readiness while the historical LG-C1 private helper names remain centralized
# in this core module for auditability.
_refresh_graph_state_readiness_after_operator_log = _refresh_lg_c1_readiness_after_lg_d1_operator_log






def run_full_staged_langgraph_runtime(
    nl: str,
    *,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    initial_dsl: str = "",
    planned_stage_graph: dict[str, Any] | None = None,
    resolved_config: dict[str, Any] | None = None,
    run_id: str | None = None,
    provider: ChatProvider | None = None,
    called_from_loop: bool = False,
    operator_stream_enabled: bool = True,
    toolnode_wrapper_enabled: bool = True,
    lg_e2_send_parallel_enabled: bool = True,
) -> AgentLoopResult:
    """Run the canonical full-staged loop through the default LangGraph runtime."""

    config.validate_for_run()
    registry = build_langgraph_node_registry()
    planned = planned_stage_graph or _planned_stage_graph_from_config(config)
    consistency = graph_registry_consistency(planned, registry)
    if not consistency["ok"]:
        raise ValueError(f"LangGraph registry does not cover planned stage graph: {consistency}")
    compat = langgraph_compat_smoke()
    if not compat.get("ok"):
        raise RuntimeError(f"LangGraph compatibility smoke failed: {compat}")
    resolved = resolved_config or config.resolved_config()
    lg_g1_trace_policy = _lg_g1_trace_export_policy(config)
    lg_c2_context_contract = build_lg_c2_context_subgraph_contract()
    lg_c2_context_contract_hash = _hash_payload(lg_c2_context_contract)
    graph_config = {
        "registry": registry,
        "lg_c2_context_subgraph_contract": lg_c2_context_contract,
        "lg_c2_context_subgraph_contract_hash": lg_c2_context_contract_hash,
        "planned_stage_graph": planned,
        "resolved_config": resolved,
        "condition_hash": resolved.get("condition_hash"),
        "condition_id": config.condition_id,
        "max_iterations": config.max_iterations,
        "scenario_max_retries": config.scenario_max_retries,
        "min_sl10_rework_attempts": int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        "policy_profile": config.policy_profile,
        "llm_provider_mode": config.llm_provider_mode,
        "runtime_backend": "langgraph_default",
        "checkpoint_backend": "memory",
        "checkpoint_serde": "pickle",
        "runtime_schema_version": GRAPH_RUNTIME_SCHEMA_VERSION,
        "node_edge_schema_version": NODE_EDGE_SCHEMA_VERSION,
        "lg_d1_operator_stream_enabled": bool(operator_stream_enabled),
        "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
        "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "lg_e2_send_parallel_enabled": bool(lg_e2_send_parallel_enabled),
        "lg_e2_send_parallel_schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
    }
    if lg_g1_trace_policy["enabled"]:
        graph_config.update(
            {
                "lg_g1_trace_export_enabled": True,
                "lg_g1_trace_export_mode": lg_g1_trace_policy["mode"],
            }
        )
    graph_config_hash = _hash_payload(graph_config)
    metadata = _graph_runtime_metadata(
        registry=registry,
        compat=compat,
        graph_config_hash=graph_config_hash,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        lg_e2_send_parallel_enabled=lg_e2_send_parallel_enabled,
    )
    run_id = run_id or config.run_id or f"pr-langgraph-{hashlib.sha256(nl.encode('utf-8')).hexdigest()[:12]}"
    initial_lg_d1_stream_metadata = lg_d1_llm_stream_runtime_metadata(real_llm_provider_api=config.llm_provider_mode == "real_env")
    runtime_cfg = FullStagedRuntimeConfig(
        initial_dsl=initial_dsl,
        run_id=run_id,
        output_dir=config.output_dir,
        max_iterations=config.max_iterations,
        scenario_max_retries=config.scenario_max_retries,
        min_sl10_rework_attempts=int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        policy_profile=config.policy_profile,
        write_run_record=config.write_run_record,
        adapter_mode=config.llm_provider_mode,
        allow_main_result_eligible=config.condition_id == "full_staged_v1" and config.llm_provider_mode == "real_env",
        resolved_loop_config=resolved,
        run_config_extra={
            "runtime_implementation": "method.langgraph_runtime.run_full_staged_langgraph_runtime",
            "langgraph_called_from_loop": called_from_loop,
            "canonical_runtime_backend": "langgraph",
            "graph_node_registry": registry,
            "graph_registry_consistency": consistency,
            "graph_config_hash": graph_config_hash,
            "instrumentation_layer": "langgraph",
            "lg_d1_operator_log_enabled": bool(operator_stream_enabled),
            "lg_d1_instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
            "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "lg_e3_toolnode_wrapper_registry": build_lg_e3_toolnode_wrapper_registry(),
            "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
            "lg_e2_send_parallel_enabled": bool(lg_e2_send_parallel_enabled),
            "lg_e2_send_parallel_schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
            "lg_e2_send_parallel_contract": build_lg_e2_send_parallel_contract(),
            **({"lg_g1_trace_export_policy": lg_g1_trace_policy} if lg_g1_trace_policy["enabled"] else {}),
            "lg_c2_context_subgraph_contract": lg_c2_context_contract,
            "lg_c2_context_subgraph_contract_hash": lg_c2_context_contract_hash,
            "lg_c2_context_subgraph_canonical_record_field": LG_C2_CANONICAL_RECORD_FIELD,
            "llm_stream_required": initial_lg_d1_stream_metadata["llm_stream_required"],
            "stage_semantics_module": "method.staged_runtime",
        },
        environment_extra={
            **metadata,
            "runner": "method.langgraph_runtime.run_full_staged_langgraph_runtime",
            "stage_semantics_module": "method.staged_runtime",
            "loop_entrypoint": "method.loop.run_agent_loop" if called_from_loop else "method.langgraph_runtime.run_full_staged_langgraph_runtime",
            "record_schema_version": "pr-c.default-full-staged-runtime.v1",
            "lg_d1_operator_log_enabled": bool(operator_stream_enabled),
            "lg_d1_instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
            "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "lg_e3_toolnode_wrapper_registry_hash": _hash_payload(build_lg_e3_toolnode_wrapper_registry()),
            "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
            "lg_e2_send_parallel_enabled": bool(lg_e2_send_parallel_enabled),
            "lg_e2_send_parallel_schema_version": LG_E2_SEND_PARALLEL_SCHEMA_VERSION,
            "lg_e2_send_parallel_contract_hash": _hash_payload(build_lg_e2_send_parallel_contract()),
            "lg_g1_trace_export_enabled": bool(lg_g1_trace_policy["enabled"]),
            "lg_g1_trace_export_status": "local_enabled" if lg_g1_trace_policy["enabled"] else "disabled",
            "lg_g1_trace_export_schema_version": LG_G1_TRACE_EXPORT_SCHEMA_VERSION,
            "lg_g1_external_trace_status": lg_g1_trace_policy["external_trace_status"],
            "lg_c2_context_subgraph_schema_version": LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION,
            "lg_c2_context_subgraph_contract_hash": lg_c2_context_contract_hash,
            "lg_c2_context_subgraph_canonical_record_field": LG_C2_CANONICAL_RECORD_FIELD,
            **initial_lg_d1_stream_metadata,
        },
        real_llm_provider_api=config.llm_provider_mode == "real_env",
        provider_config_read=_provider_config_read(config),
        provider_model_redacted=_provider_model_redacted(config, provider),
        default_loop_config_entry_integrated=called_from_loop or config.condition_id == "full_staged_v1",
    )
    app = _build_graph(runtime_cfg=runtime_cfg, adapters=adapters)
    state, operator_events, graph_stream_status = _run_graph_with_lg_d1_stream(
        app,
        initial_state={
            "nl": nl,
            "graph_trace": [],
            "operator_events": [],
            "operator_stream_enabled": bool(operator_stream_enabled),
            "toolnode_wrapper_events": [],
            "lg_e2_send_parallel_events": [],
            "stage_record_events": [],
            "llm_interaction_events": [],
            "fix_log_events": [],
            "scenario_history_events": [],
            "repair_history_events": [],
            "toolnode_wrapper_enabled": bool(toolnode_wrapper_enabled),
            "run_id": run_id,
        },
        run_id=run_id,
        operator_stream_enabled=bool(operator_stream_enabled),
    )
    result = state.get("runtime_result")
    if not isinstance(result, AgentLoopResult):
        raise TypeError("LangGraph runtime did not return an AgentLoopResult")
    graph_trace = list(state.get("graph_trace", []) or [])
    _augment_run_record_with_graph_trace(result, graph_trace)
    toolnode_events = list(state.get("toolnode_wrapper_events", []) or [])
    _augment_run_record_with_lg_e3_toolnode_trace(
        result,
        events=toolnode_events,
        enabled=bool(toolnode_wrapper_enabled),
    )
    lg_e2_events = list(state.get("lg_e2_send_parallel_events", []) or [])
    _augment_run_record_with_lg_e2_send_parallel_trace(
        result,
        events=lg_e2_events,
        enabled=bool(lg_e2_send_parallel_enabled),
    )
    operator_events = _merge_operator_events(operator_events, state.get("operator_events"))
    _augment_run_record_with_lg_d1_operator_log(
        result,
        operator_events=operator_events,
        graph_stream_status=graph_stream_status,
        operator_stream_enabled=bool(operator_stream_enabled),
    )
    _refresh_lg_c1_readiness_after_lg_d1_operator_log(result, state)
    _augment_run_record_with_lg_g1_trace_export(
        result,
        enabled=bool(lg_g1_trace_policy["enabled"]),
        mode=str(lg_g1_trace_policy["mode"]),
    )
    result.resolved_config = resolved
    result.planned_stage_graph = planned
    return result


# Export private compatibility helpers for the thin facade and D3 submodules.
__all__ = [name for name in globals() if not name.startswith("__")]
