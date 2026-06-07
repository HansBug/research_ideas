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




class _ValidationSubgraphState(_GraphLoopState, total=False):
    """State carried by the LG-B1 validation subgraph.

    The subgraph mutates the canonical ``_RunState`` object in the same way as
    the old validation pass helper, but the orchestration edges are now explicit
    LangGraph nodes.  ``validation_*`` keys are transient subgraph channels and
    are not the academic evidence source; SC-13 still writes
    ``AgentLoopRunRecord`` as the canonical ledger.
    """

    validation_context: StageContext
    validation_feedback: dict[str, Any]
    validation_stage_metas: list[Any]
    validation_scenario_history: list[dict[str, Any]]
    validation_scenario_set: Any
    validation_scenario_epoch: int
    validation_oracle_weak: bool
    validation_scenario_phase_complete: bool
    validation_attempt_index: int
    validation_retry_mode: str
    validation_coverage_directive: Any
    validation_previous_scenarios: list[Any]
    validation_selected_scenarios: list[Any]
    validation_selected_coverage: dict[str, Any]
    validation_scenario_merge: dict[str, Any]
    validation_raw_generated_scenario_count: int
    validation_coverage_gap: bool
    validation_dsl_changed_since_freeze: bool
    validation_next_epoch: int
    validation_result: Any
    validation_continuation_source: Any
    validation_continued_after_waiver: bool
    validation_waiver_audit: Any
    validation_lg_e2_send_metadata: dict[str, Any]


class _WaiverSubgraphState(_ValidationSubgraphState, total=False):
    """State carried by the LG-B3 waiver continuation subgraph.

    LG-B3 keeps the canonical post-waiver evidence in ``_RunState`` and
    ``AgentLoopRunRecord``.  ``waiver_*`` keys are transient orchestration
    channels used to make the repair→waiver envelope and validation-tail
    continuation explicit without duplicating LG-B1 validation semantics.
    """

    waiver_input_envelope: dict[str, Any]
    waiver_validation_ref: str
    waiver_validation_source: Any
    waiver_tail_kind: str
    waiver_tail_start_stage: str
    waiver_result: Any

class _RepairSubgraphState(_GraphLoopState, total=False):
    """State carried by the LG-B2 repair subgraph.

    The canonical repair data remains in ``_RunState`` / AgentLoopRunRecord.
    ``repair_*`` keys are transient subgraph channels used only to make
    SD-8→SL-9→SL-10→SC-11 orchestration visible to LangGraph.
    """

    repair_validation: Any
    repair_selected_trace: dict[str, Any]
    repair_source: str
    repair_source_stage: str
    repair_selected_feedback: Any
    repair_fix_plan: Any
    repair_effective_fix_plan: Any
    repair_request_batch: Any
    repair_aggregate_stage_ids: list[str]
    repair_max_rework_attempts: int
    repair_rework_attempt: int
    repair_rework_locked_initial: bool
    repair_active_request_batch: Any
    repair_sl9_decision: Any
    repair_candidate_dsl: str
    repair_request: Any
    repair_local_review: Any
    repair_local_meta: Any
    repair_local_check_evidence: dict[str, Any]
    repair_local_sd10_repair_review: Any
    repair_review_input_summary: dict[str, Any]
    repair_sl10_output: Any
    repair_repair_review: Any
    repair_memory: dict[str, Any]
    repair_grounding_update_hints: list[dict[str, Any]]
    repair_noop_override_waiver_audit: Any
    repair_last_iteration_patch: dict[str, Any]
    repair_last_repair_review: Any
    repair_last_sl10_output: Any
    repair_accepted: bool
    repair_patch: dict[str, Any]




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

def _build_validation_subgraph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
) -> Any:
    """Build the LG-B1 stage-level validation subgraph.

    The canonical stage semantics remain in ``method.staged_runtime`` helpers
    and adapters, while LangGraph now owns the SD-2→SL-7 validation routing.
    """

    graph = StateGraph(_ValidationSubgraphState)

    def _state(graph_state: _ValidationSubgraphState) -> _ValidationSubgraphState:
        return dict(graph_state)

    def _runtime_state(graph_state: _ValidationSubgraphState) -> _RunState:
        return graph_state["runtime_state"]

    def _iteration(graph_state: _ValidationSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def _validation_result(graph_state: _ValidationSubgraphState, *, scenario_epoch: int | None) -> _ValidationPass:
        feedback = dict(graph_state.get("validation_feedback") or {})
        return _ValidationPass(
            graph_state["validation_context"],
            feedback,
            list(graph_state.get("validation_stage_metas") or []),
            _select_first_blocking(feedback),
            graph_state.get("validation_scenario_set"),
            list(graph_state.get("validation_scenario_history") or []),
            bool(graph_state.get("validation_oracle_weak", False)),
            scenario_epoch,
        )

    def validation_enter(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        scenario_set = runtime_state.scenario_set
        _trace_node(graph_state, "validation_subgraph", event="subgraph_enter", iteration=iteration)
        _append_flow_log(
            runtime_state.logs,
            event="iteration_validation_enter",
            iteration=iteration,
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            scenario_set_id=scenario_set.scenario_set_id if scenario_set is not None else None,
            oracle_weak=runtime_state.oracle_weak,
            dsl=runtime_state.current_dsl,
            graph_subgraph="validation_subgraph",
        )
        continuation_source = graph_state.get("validation_continuation_source")
        if isinstance(continuation_source, _ValidationPass):
            source, selected_feedback, source_stage = continuation_source.selected or ("", None, "")
            waiver_audit = graph_state.get("validation_waiver_audit")
            if (
                isinstance(waiver_audit, dict)
                and waiver_audit.get("kind") in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
                and source == FeedbackSource.SIM.value
                and source_stage == StageId.SD_6_SIM.value
                and isinstance(selected_feedback, SimFeedback)
            ):
                waiver_kind = str(waiver_audit.get("kind") or "")
                if waiver_kind == "sl10_noop_override_waiver":
                    enter_reason = "SL-10 accepted a no-op override for the current SD-6 scenario request; continue to SL-7 without DSL edit"
                    stage_reason = "sl10_noop_override_waiver_marked_non_blocking_for_SL-7"
                    skipped_reason = (
                        "waiver_continue: SL-10 passed a no-op candidate with local_override_rationale "
                        "for the current SD-6 scenario_regression; continuing to SL-7 without SC-11 "
                        "budget consumption or DSL edit"
                    )
                else:
                    enter_reason = "SL-9 rejected stale overridden SD-6 scenario request; continue to SL-7 without DSL edit"
                    stage_reason = "stale_overridden_scenario_waiver_marked_non_blocking_for_SL-7"
                    skipped_reason = (
                        "waiver_continue: stale SD-6 scenario hard request was rejected by SL-9 "
                        "and matched a prior SL-10 local_override_rationale for the same scenario; "
                        "continuing to SL-7 without DSL edit"
                    )
                context = _clone_stage_context(continuation_source.context, current_dsl=runtime_state.current_dsl)
                context.warning_budget_state = continuation_source.context.warning_budget_state
                scenario_set = continuation_source.scenario_set
                context.scenario_set = scenario_set
                feedback = dict(continuation_source.feedback)
                waived_sim = _make_waived_sim_feedback(selected_feedback, waiver_audit)
                feedback[FeedbackSource.SIM.value] = waived_sim
                stage_metas = list(continuation_source.stage_metas)
                scenario_history = list(continuation_source.scenario_history)

                waiver_meta = _meta(StageId.SD_6_SIM, ok=True, status=StageStatus.ADVISORY)
                waiver_meta.input_hash = _hash_text(runtime_state.current_dsl)
                waiver_meta.output_hash = _short_hash(waiver_audit)
                waiver_meta.skipped_reason = skipped_reason
                _trace_node(
                    graph_state,
                    "validation_sd6_sim",
                    iteration=iteration,
                    continued_after_waiver=True,
                    waiver_audit_kind=waiver_audit.get("kind"),
                )
                _append_stage(runtime_state.stage_records, waiver_meta)
                stage_metas.append(waiver_meta)
                _append_flow_log(
                    runtime_state.logs,
                    event="waiver_continue_validation_enter",
                    iteration=iteration,
                    source_stage=StageId.SD_6_SIM.value,
                    reason=enter_reason,
                    current_dsl_hash=_hash_text(runtime_state.current_dsl),
                    current_dsl=runtime_state.current_dsl,
                    waiver_audit=_jsonable(waiver_audit),
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_enter",
                )
                _append_flow_log(
                    runtime_state.logs,
                    event="stage_result",
                    stage_id=StageId.SD_6_SIM.value,
                    iteration=iteration,
                    ok=True,
                    status=str(StageStatus.ADVISORY),
                    reason=stage_reason,
                    feedback=_feedback_brief(StageId.SD_6_SIM.value, waived_sim),
                    jump="SL-7",
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_sd6_sim",
                )
                graph_state["validation_context"] = context
                graph_state["validation_feedback"] = feedback
                graph_state["validation_stage_metas"] = stage_metas
                graph_state["validation_scenario_history"] = scenario_history
                graph_state["validation_scenario_set"] = scenario_set
                graph_state["validation_scenario_epoch"] = continuation_source.scenario_epoch
                graph_state["validation_oracle_weak"] = continuation_source.oracle_weak
                graph_state["validation_continued_after_waiver"] = True
                graph_state["validation_waiver_audit"] = _jsonable(waiver_audit)
                _trace_node(
                    graph_state,
                    "validation_sl7_model_review",
                    iteration=iteration,
                    continued_after_waiver=True,
                    waiver_audit_kind=waiver_audit.get("kind"),
                )
                return Command(goto="validation_sl7_model_review", update=graph_state)
            if (
                source != FeedbackSource.DESIGN.value
                or source_stage != StageId.SD_4_DESIGN.value
                or not isinstance(selected_feedback, DesignFeedback)
            ):
                graph_state["validation_result"] = continuation_source
                return Command(goto="validation_finalize", update=graph_state)
            context = _clone_stage_context(continuation_source.context, current_dsl=runtime_state.current_dsl)
            context.warning_budget_state = continuation_source.context.warning_budget_state
            waived_design = _make_waived_design_feedback(selected_feedback)
            feedback = dict(continuation_source.feedback)
            feedback[FeedbackSource.DESIGN.value] = waived_design
            stage_metas = list(continuation_source.stage_metas)
            scenario_history = list(continuation_source.scenario_history)
            scenario_set = continuation_source.scenario_set
            waiver_meta = _meta(StageId.SD_4_DESIGN, ok=True, status=StageStatus.ADVISORY)
            waiver_meta.input_hash = _hash_text(runtime_state.current_dsl)
            waiver_meta.output_hash = _short_hash([item.instance_key for item in selected_feedback.blocking_items])
            waiver_meta.skipped_reason = (
                "waiver_continue: non-hard SD-4 blocking warnings were rejected/waived by "
                "SL-9; continuing downstream validation without DSL edit"
            )
            _trace_node(graph_state, "validation_sd4_design", iteration=iteration, continued_after_waiver=True)
            _append_stage(runtime_state.stage_records, waiver_meta)
            stage_metas.append(waiver_meta)
            _append_flow_log(
                runtime_state.logs,
                event="waiver_continue_validation_enter",
                iteration=iteration,
                source_stage=StageId.SD_4_DESIGN.value,
                reason="SL-9 rejected/waived non-hard SD-4 requests; continue downstream without SC-11 DSL edit",
                current_dsl_hash=_hash_text(runtime_state.current_dsl),
                current_dsl=runtime_state.current_dsl,
                graph_subgraph="validation_subgraph",
                graph_node="validation_enter",
            )
            _append_flow_log(
                runtime_state.logs,
                event="stage_result",
                stage_id=StageId.SD_4_DESIGN.value,
                iteration=iteration,
                ok=True,
                status=str(StageStatus.ADVISORY),
                reason="waiver_continue_design_items_marked_non_blocking_for_downstream_validation",
                jump="SL-5" if scenario_set is None else "SD-5A",
                graph_subgraph="validation_subgraph",
                graph_node="validation_sd4_design",
            )
            graph_state["validation_context"] = context
            graph_state["validation_feedback"] = feedback
            graph_state["validation_stage_metas"] = stage_metas
            graph_state["validation_scenario_history"] = scenario_history
            graph_state["validation_scenario_set"] = scenario_set
            graph_state["validation_scenario_epoch"] = runtime_state.scenario_epoch
            graph_state["validation_oracle_weak"] = continuation_source.oracle_weak
            graph_state["validation_continued_after_waiver"] = True
            if scenario_set is None:
                graph_state["validation_retry_mode"] = "initial"
                graph_state["validation_attempt_index"] = 0
                graph_state["validation_coverage_directive"] = None
                graph_state["validation_previous_scenarios"] = []
                graph_state["validation_selected_scenarios"] = []
                graph_state["validation_selected_coverage"] = {"coverage_report": {}, "coverage_gap": False, "retry_directive": None}
                _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=0, continued_after_waiver=True)
                return Command(goto="validation_sl5_scenario_generation", update=graph_state)
            _trace_node(graph_state, "validation_sd5a_reuse_coverage", iteration=iteration, continued_after_waiver=True)
            return Command(goto="validation_sd5a_reuse_coverage", update=graph_state)

        graph_state["validation_context"] = StageContext(
            nl=graph_state["nl"],
            current_dsl=runtime_state.current_dsl,
            grounding_map=runtime_cfg.grounding_map,
            scenario_set=scenario_set,
            warning_budget_state=runtime_state.warning_budget_state or {},
        )
        graph_state["validation_feedback"] = {}
        graph_state["validation_stage_metas"] = []
        graph_state["validation_scenario_history"] = []
        graph_state["validation_scenario_set"] = scenario_set
        graph_state["validation_scenario_epoch"] = runtime_state.scenario_epoch
        graph_state["validation_oracle_weak"] = runtime_state.oracle_weak
        _trace_node(graph_state, "validation_sd2_parse", iteration=iteration)
        return Command(goto="validation_sd2_parse", update=graph_state)

    def validation_sd2_parse(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_2_PARSE.value, iteration=iteration, reason="full_validation_pass")
        parse_feedback, parse_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd2_parse",
            stage_id=StageId.SD_2_PARSE.value,
            graph_node="validation_sd2_parse",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "context": context},
            call=lambda: adapters.parse(runtime_state.current_dsl, context),
        )
        feedback[FeedbackSource.PARSE.value] = parse_feedback
        _append_stage(runtime_state.stage_records, parse_meta)
        stage_metas.append(parse_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_2_PARSE.value,
            iteration=iteration,
            ok=parse_feedback.ok,
            status=str(parse_meta.status),
            feedback=_feedback_brief(StageId.SD_2_PARSE.value, parse_feedback),
            jump="SD-3" if parse_feedback.ok else "SD-8",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd2_parse",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not parse_feedback.ok:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sd3_semantic", iteration=iteration)
        return Command(goto="validation_sd3_semantic", update=graph_state)

    def validation_sd3_semantic(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_3_SEMANTIC.value, iteration=iteration, reason="SD-2 ok")
        semantic_feedback, semantic_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd3_semantic",
            stage_id=StageId.SD_3_SEMANTIC.value,
            graph_node="validation_sd3_semantic",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "context": context},
            call=lambda: adapters.semantic(runtime_state.current_dsl, context),
        )
        feedback[FeedbackSource.SEMANTIC.value] = semantic_feedback
        _append_stage(runtime_state.stage_records, semantic_meta)
        stage_metas.append(semantic_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_3_SEMANTIC.value,
            iteration=iteration,
            ok=semantic_feedback.ok,
            status=str(semantic_meta.status),
            feedback=_feedback_brief(StageId.SD_3_SEMANTIC.value, semantic_feedback),
            jump="SD-4" if semantic_feedback.ok else "SD-8",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd3_semantic",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not semantic_feedback.ok:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sd4_design", iteration=iteration)
        return Command(goto="validation_sd4_design", update=graph_state)

    def validation_sd4_design(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state.get("validation_scenario_set")
        _append_flow_log(runtime_state.logs, event="stage_enter", stage_id=StageId.SD_4_DESIGN.value, iteration=iteration, reason="SD-3 ok")
        design_feedback, design_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd4_design",
            stage_id=StageId.SD_4_DESIGN.value,
            graph_node="validation_sd4_design",
            iteration=iteration,
            input_payload={"context": context},
            call=lambda: adapters.design(context),
        )
        feedback[FeedbackSource.DESIGN.value] = design_feedback
        _append_stage(runtime_state.stage_records, design_meta)
        stage_metas.append(design_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_4_DESIGN.value,
            iteration=iteration,
            ok=not bool(design_feedback.blocking_items),
            status=str(design_meta.status),
            feedback=_feedback_brief(StageId.SD_4_DESIGN.value, design_feedback),
            jump="SD-8" if design_feedback.blocking_items else ("SL-5" if scenario_set is None else "SD-5A"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd4_design",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if design_feedback.blocking_items:
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=None)
            return Command(goto="validation_finalize", update=graph_state)
        if scenario_set is None:
            graph_state["validation_retry_mode"] = "initial"
            graph_state["validation_attempt_index"] = 0
            graph_state["validation_coverage_directive"] = None
            graph_state["validation_previous_scenarios"] = []
            graph_state["validation_selected_scenarios"] = []
            graph_state["validation_selected_coverage"] = {"coverage_report": {}, "coverage_gap": False, "retry_directive": None}
            _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=0)
            return Command(goto="validation_sl5_scenario_generation", update=graph_state)
        _trace_node(graph_state, "validation_sd5a_reuse_coverage", iteration=iteration)
        return Command(goto="validation_sd5a_reuse_coverage", update=graph_state)

    def validation_sl5_scenario_generation(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        attempt_index = int(graph_state.get("validation_attempt_index", 0))
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        scenario_epoch = int(graph_state.get("validation_next_epoch", graph_state.get("validation_scenario_epoch", 0))) if retry_mode == "targeted" else int(graph_state.get("validation_scenario_epoch", 0))
        coverage_directive = graph_state.get("validation_coverage_directive")
        previous_scenarios = list(graph_state.get("validation_previous_scenarios") or [])
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_5_SCENARIO_GENERATION.value,
            iteration=iteration,
            reason="scenario_set_absent" if retry_mode == "initial" and attempt_index == 0 else ("scenario_coverage_gap_retry" if retry_mode == "initial" else "targeted_refresh_after_frozen_gap_or_dsl_change"),
            attempt_index=attempt_index,
            coverage_directive=_compact_json(coverage_directive, max_list_items=6),
            previous_scenario_names=[scenario.name for scenario in previous_scenarios],
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl5_scenario_generation",
        )
        request = ScenarioGenerationRequest(
            nl=graph_state["nl"],
            current_dsl=runtime_state.current_dsl,
            context=context,
            attempt_index=attempt_index,
            coverage_directive=coverage_directive,
            previous_scenarios=previous_scenarios,
            scenario_epoch=scenario_epoch,
        )
        generated = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_5_SCENARIO_GENERATION,
            graph_node="validation_sl5_scenario_generation",
            subgraph_id="validation_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.scenario_generate(request),
                expected_stage_id=StageId.SL_5_SCENARIO_GENERATION,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=graph_state["validation_stage_metas"],
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
                parsed_summary={"attempt_index": attempt_index, "kind": "scenario_generation" if retry_mode == "initial" else "scenario_refresh"},
            ),
        )
        raw_scenarios = list(getattr(generated, "parsed_output", []) or []) if _is_llm_stage_run(generated) else list(generated or [])
        scenarios, scenario_merge = _merge_scenario_sets_by_name(previous_scenarios, raw_scenarios)
        if _is_llm_stage_run(generated):
            try:
                generated.parsed_output = scenarios
                if isinstance(getattr(generated, "interaction", None), dict):
                    generated.interaction["scenario_merge_policy"] = scenario_merge
            except Exception:
                pass
        else:
            sl5_meta = _meta(StageId.SL_5_SCENARIO_GENERATION, ok=True)
            sl5_meta.input_hash = _hash_text(runtime_state.current_dsl)
            sl5_meta.output_hash = _short_hash(scenarios)
            _append_stage(runtime_state.stage_records, sl5_meta)
            graph_state["validation_stage_metas"].append(sl5_meta)
        graph_state["validation_selected_scenarios"] = scenarios
        graph_state["validation_scenario_merge"] = _jsonable(scenario_merge)
        graph_state["validation_raw_generated_scenario_count"] = len(raw_scenarios)
        _trace_node(graph_state, "validation_sd5a_scenario_coverage", iteration=iteration, attempt_index=attempt_index)
        return Command(goto="validation_sd5a_scenario_coverage", update=graph_state)

    def validation_sd5a_scenario_coverage(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        scenarios = list(graph_state.get("validation_selected_scenarios") or [])
        attempt_index = int(graph_state.get("validation_attempt_index", 0))
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        coverage, coverage_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd5a_scenario_coverage",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            graph_node="validation_sd5a_scenario_coverage",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "scenarios": scenarios, "attempt_index": attempt_index, "retry_mode": retry_mode},
            call=lambda: adapters.scenario_coverage(runtime_state.current_dsl, scenarios),
        )
        _append_stage(runtime_state.stage_records, coverage_meta)
        graph_state["validation_stage_metas"].append(coverage_meta)
        selected_coverage = dict(coverage)
        graph_state["validation_selected_coverage"] = selected_coverage
        gap = bool(coverage.get("coverage_gap"))
        scenario_merge = graph_state.get("validation_scenario_merge") or {}
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            iteration=iteration,
            ok=not gap,
            attempt_index=attempt_index,
            status=str(coverage_meta.status),
            n_scenarios=len(scenarios),
            raw_generated_scenario_count=int(graph_state.get("validation_raw_generated_scenario_count", 0)),
            scenario_names=[scenario.name for scenario in scenarios],
            scenario_merge_policy=scenario_merge,
            coverage=_compact_json(coverage, max_list_items=8),
            jump="SC-5F" if not gap else ("SL-5 retry" if attempt_index < runtime_cfg.scenario_max_retries else "SC-5F weak_oracle"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd5a_scenario_coverage",
        )
        retry_exhausted = gap and attempt_index >= runtime_cfg.scenario_max_retries
        weak = retry_exhausted or bool(selected_coverage.get("oracle_weak"))
        history = list(graph_state.get("validation_scenario_history") or [])
        item = _scenario_history_item(
            iteration=iteration,
            attempt_index=attempt_index,
            scenarios=scenarios,
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=retry_exhausted,
            oracle_weak=weak,
        )
        if retry_mode == "targeted":
            previous_set = graph_state.get("validation_scenario_set")
            item.update(
                {
                    "targeted_retry_after_frozen_gap": bool(graph_state.get("validation_coverage_gap")),
                    "targeted_retry_after_dsl_change": bool(graph_state.get("validation_dsl_changed_since_freeze")),
                    "previous_scenario_set_id": getattr(previous_set, "scenario_set_id", None),
                    "previous_source_dsl_hash": getattr(previous_set, "source_dsl_hash", None),
                    "current_dsl_hash": _hash_text(runtime_state.current_dsl),
                }
            )
        item["scenario_merge_policy"] = _jsonable(scenario_merge)
        history.append(item)
        graph_state["validation_scenario_history"] = history
        graph_state["validation_oracle_weak"] = weak
        if not gap or attempt_index >= runtime_cfg.scenario_max_retries:
            _trace_node(graph_state, "validation_sc5f_scenario_freeze", iteration=iteration)
            return Command(goto="validation_sc5f_scenario_freeze", update=graph_state)
        graph_state["validation_coverage_directive"] = coverage.get("retry_directive") or {"retry_reason": "coverage_gap" if retry_mode == "initial" else "frozen_scenario_coverage_gap"}
        graph_state["validation_previous_scenarios"] = scenarios
        graph_state["validation_attempt_index"] = attempt_index + 1
        _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=attempt_index + 1)
        return Command(goto="validation_sl5_scenario_generation", update=graph_state)

    def validation_sd5a_reuse_coverage(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        scenario_set = graph_state["validation_scenario_set"]
        current_dsl_hash = _hash_text(runtime_state.current_dsl)
        dsl_changed_since_freeze = bool(scenario_set.source_dsl_hash and scenario_set.source_dsl_hash != current_dsl_hash)
        coverage, coverage_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd5a_scenario_coverage",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            graph_node="validation_sd5a_reuse_coverage",
            iteration=iteration,
            input_payload={"current_dsl": runtime_state.current_dsl, "scenarios": list(scenario_set.scenarios), "scenario_set_id": scenario_set.scenario_set_id},
            call=lambda: adapters.scenario_coverage(runtime_state.current_dsl, list(scenario_set.scenarios)),
        )
        _append_stage(runtime_state.stage_records, coverage_meta)
        graph_state["validation_stage_metas"].append(coverage_meta)
        gap = bool(coverage.get("coverage_gap"))
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_5A_SCENARIO_COVERAGE.value,
            iteration=iteration,
            ok=not gap and not dsl_changed_since_freeze,
            reason="reuse_frozen_scenario_set",
            scenario_set_id=scenario_set.scenario_set_id,
            coverage_gap=gap,
            dsl_changed_since_freeze=dsl_changed_since_freeze,
            coverage=_compact_json(coverage, max_list_items=8),
            jump="SC-5F reuse" if not gap and not dsl_changed_since_freeze else "SL-5 targeted_retry",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd5a_reuse_coverage",
        )
        item = _scenario_history_item(
            iteration=iteration,
            attempt_index=0,
            scenarios=list(scenario_set.scenarios),
            coverage=coverage,
            coverage_meta=coverage_meta,
            retry_exhausted=False,
            oracle_weak=False,
        )
        item.update(
            {
                "scenario_set_id": scenario_set.scenario_set_id,
                "epoch": scenario_set.epoch,
                "reused_frozen_oracle": True,
                "dsl_changed_since_freeze": dsl_changed_since_freeze,
                "previous_source_dsl_hash": scenario_set.source_dsl_hash,
                "current_dsl_hash": current_dsl_hash,
            }
        )
        graph_state["validation_scenario_history"] = list(graph_state.get("validation_scenario_history") or []) + [item]
        if not gap and not dsl_changed_since_freeze:
            freeze_meta = _meta(StageId.SC_5F_SCENARIO_FREEZE, ok=True)
            freeze_meta.input_hash = _hash_text(runtime_state.current_dsl)
            freeze_meta.output_hash = _hash_text(scenario_set.scenario_set_id)
            _append_stage(runtime_state.stage_records, freeze_meta)
            graph_state["validation_stage_metas"].append(freeze_meta)
            _append_flow_log(
                runtime_state.logs,
                event="stage_result",
                stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
                iteration=iteration,
                ok=True,
                reason="reused_frozen_scenario_set",
                scenario_set_id=scenario_set.scenario_set_id,
                epoch=scenario_set.epoch,
                n_scenarios=len(scenario_set.scenarios),
                jump="SD-6",
                graph_subgraph="validation_subgraph",
                graph_node="validation_sc5f_scenario_freeze",
            )
            graph_state["validation_oracle_weak"] = False
            graph_state["validation_scenario_epoch"] = scenario_set.epoch + 1
            context.scenario_set = scenario_set
            _trace_node(graph_state, "validation_sd6_sim", iteration=iteration)
            return Command(goto="validation_sd6_sim", update=graph_state)
        graph_state["validation_retry_mode"] = "targeted"
        graph_state["validation_coverage_directive"] = coverage.get("retry_directive") or {
            "retry_reason": "dsl_changed_since_scenario_freeze" if dsl_changed_since_freeze else "frozen_scenario_coverage_gap",
            "previous_scenario_set_id": scenario_set.scenario_set_id,
            "previous_source_dsl_hash": scenario_set.source_dsl_hash,
            "current_dsl_hash": current_dsl_hash,
        }
        graph_state["validation_previous_scenarios"] = list(scenario_set.scenarios)
        graph_state["validation_selected_scenarios"] = list(scenario_set.scenarios)
        graph_state["validation_selected_coverage"] = dict(coverage)
        graph_state["validation_coverage_gap"] = gap
        graph_state["validation_dsl_changed_since_freeze"] = dsl_changed_since_freeze
        graph_state["validation_next_epoch"] = scenario_set.epoch + 1
        graph_state["validation_oracle_weak"] = (runtime_cfg.scenario_max_retries == 0 and (gap or dsl_changed_since_freeze)) or bool(dict(coverage).get("oracle_weak"))
        _append_flow_log(
            runtime_state.logs,
            event="frozen_scenario_refresh_targeted_retry",
            level="warning",
            iteration=iteration,
            scenario_set_id=scenario_set.scenario_set_id,
            scenario_max_retries=runtime_cfg.scenario_max_retries,
            coverage_gap=gap,
            dsl_changed_since_freeze=dsl_changed_since_freeze,
            graph_subgraph="validation_subgraph",
        )
        if runtime_cfg.scenario_max_retries == 0:
            _trace_node(graph_state, "validation_sc5f_scenario_freeze", iteration=iteration)
            return Command(goto="validation_sc5f_scenario_freeze", update=graph_state)
        graph_state["validation_attempt_index"] = 1
        _trace_node(graph_state, "validation_sl5_scenario_generation", iteration=iteration, attempt_index=1)
        return Command(goto="validation_sl5_scenario_generation", update=graph_state)

    def validation_sc5f_scenario_freeze(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        retry_mode = str(graph_state.get("validation_retry_mode") or "initial")
        scenarios = list(graph_state.get("validation_selected_scenarios") or [])
        selected_coverage = dict(graph_state.get("validation_selected_coverage") or {})
        weak = bool(graph_state.get("validation_oracle_weak", False))
        if weak:
            selected_coverage = {
                **selected_coverage,
                "oracle_weak": True,
                "weak_oracle_reason": "scenario_refresh_retry_exhausted" if retry_mode == "targeted" else "scenario_coverage_retry_exhausted",
            }
            _append_flow_log(
                runtime_state.logs,
                event="scenario_refresh_retry_exhausted" if retry_mode == "targeted" else "scenario_coverage_retry_exhausted",
                level="warning",
                iteration=iteration,
                scenario_max_retries=runtime_cfg.scenario_max_retries,
                coverage_gap=graph_state.get("validation_coverage_gap"),
                dsl_changed_since_freeze=graph_state.get("validation_dsl_changed_since_freeze"),
                graph_subgraph="validation_subgraph",
            )
        epoch = int(graph_state.get("validation_next_epoch", graph_state.get("validation_scenario_epoch", 0))) if retry_mode == "targeted" else int(graph_state.get("validation_scenario_epoch", 0))
        scenario_set, freeze_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sc5f_freeze_scenario_set",
            stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
            graph_node="validation_sc5f_scenario_freeze",
            iteration=iteration,
            input_payload={
                "scenarios": scenarios,
                "source_dsl_hash": _hash_text(runtime_state.current_dsl),
                "source_inspect_hash": _short_hash(context.inspect_json) if context.inspect_json is not None else "",
                "source_grounding_hash": _short_hash(runtime_cfg.grounding_map) if runtime_cfg.grounding_map is not None else None,
                "coverage_report": selected_coverage,
                "epoch": epoch,
            },
            call=lambda: freeze_scenario_set(
                scenarios,
                source_dsl_hash=_hash_text(runtime_state.current_dsl),
                source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
                source_grounding_hash=_short_hash(runtime_cfg.grounding_map) if runtime_cfg.grounding_map is not None else None,
                coverage_report=selected_coverage,
                epoch=epoch,
            ),
        )
        scenario_set.coverage_report["oracle_weak"] = weak
        _append_stage(runtime_state.stage_records, freeze_meta)
        graph_state["validation_stage_metas"].append(freeze_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SC_5F_SCENARIO_FREEZE.value,
            iteration=iteration,
            ok=True,
            reason="refreshed_scenario_set" if retry_mode == "targeted" else None,
            scenario_set_id=scenario_set.scenario_set_id,
            epoch=scenario_set.epoch,
            n_scenarios=len(scenario_set.scenarios),
            oracle_weak=weak,
            source_dsl_hash=scenario_set.source_dsl_hash,
            jump="SD-6",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sc5f_scenario_freeze",
        )
        history = list(graph_state.get("validation_scenario_history") or [])
        if history:
            history[-1]["scenario_set_id"] = scenario_set.scenario_set_id
            history[-1]["epoch"] = scenario_set.epoch
            history[-1]["oracle_weak"] = weak
        graph_state["validation_scenario_history"] = history
        graph_state["validation_scenario_set"] = scenario_set
        graph_state["validation_scenario_epoch"] = scenario_set.epoch + 1
        graph_state["validation_oracle_weak"] = weak
        context.scenario_set = scenario_set
        _trace_node(graph_state, "validation_sd6_sim", iteration=iteration)
        return Command(goto="validation_sd6_sim", update=graph_state)

    def validation_sd6_sim(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state["validation_scenario_set"]
        context.scenario_set = scenario_set
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            reason="waiver_continue_scenario_set_ready" if graph_state.get("validation_continued_after_waiver") else "scenario_set_ready",
            scenario_set_id=scenario_set.scenario_set_id,
            n_scenarios=len(scenario_set.scenarios),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        sim_feedback, sim_meta, lg_e2_metadata = _lg_e2_run_sd6_send_parallel_or_serial(
            graph_state,
            runtime_cfg=runtime_cfg,
            adapters=adapters,
            current_dsl=runtime_state.current_dsl,
            scenario_set=scenario_set,
            context=context,
            iteration=iteration,
            enabled_requested=bool(runtime_cfg.run_config_extra.get("lg_e2_send_parallel_enabled", True)),
        )
        feedback[FeedbackSource.SIM.value] = sim_feedback
        lg_e2_metadata = {
            **lg_e2_metadata,
            "iteration": iteration,
            "stage_id": StageId.SD_6_SIM.value,
            "scenario_set_id": scenario_set.scenario_set_id,
            "sim_meta_hash": _hash_payload(sim_meta),
        }
        graph_state["validation_lg_e2_send_metadata"] = _jsonable(lg_e2_metadata)
        lg_e2_events = list(graph_state.get("lg_e2_send_parallel_events", []) or [])
        lg_e2_events.append(_jsonable(lg_e2_metadata))
        graph_state["lg_e2_send_parallel_events"] = lg_e2_events
        _append_flow_log(
            runtime_state.logs,
            event="lg_e2_send_parallel_result",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            parallel_send_enabled=bool(lg_e2_metadata.get("parallel_send_enabled")),
            fallback_reason=lg_e2_metadata.get("fallback_reason"),
            fanout_count=lg_e2_metadata.get("fanout_count"),
            worker_count=lg_e2_metadata.get("worker_count"),
            serial_equivalence_hash=lg_e2_metadata.get("serial_equivalence_hash"),
            canonical_result_hash=lg_e2_metadata.get("canonical_result_hash"),
            selected_feedback_digest=lg_e2_metadata.get("selected_feedback_digest"),
            scenario_epoch=lg_e2_metadata.get("scenario_epoch"),
            oracle_weak=lg_e2_metadata.get("oracle_weak"),
            lg_e2_metadata=_jsonable(lg_e2_metadata),
            does_not_replace_academic_evidence=True,
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        _append_lg_d1_operator_event(
            graph_state,
            event_type="lg_e2_send_parallel_result",
            node="validation_sd6_sim",
            stage_id=StageId.SD_6_SIM.value,
            payload={
                "parallel_send_enabled": bool(lg_e2_metadata.get("parallel_send_enabled")),
                "fallback_reason": lg_e2_metadata.get("fallback_reason"),
                "fanout_count": lg_e2_metadata.get("fanout_count"),
                "worker_count": lg_e2_metadata.get("worker_count"),
                "serial_equivalence_hash": lg_e2_metadata.get("serial_equivalence_hash"),
                "canonical_result_hash": lg_e2_metadata.get("canonical_result_hash"),
                "does_not_replace_academic_evidence": True,
            },
        )
        _append_stage(runtime_state.stage_records, sim_meta)
        stage_metas.append(sim_meta)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_6_SIM.value,
            iteration=iteration,
            ok=sim_feedback.ok,
            status=str(sim_meta.status),
            feedback=_feedback_brief(StageId.SD_6_SIM.value, sim_feedback),
            jump="SL-7" if sim_feedback.ok else ("SC-12 weak_oracle" if getattr(sim_feedback, "oracle_weak", False) else "SD-8"),
            graph_subgraph="validation_subgraph",
            graph_node="validation_sd6_sim",
        )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        if not sim_feedback.ok:
            if getattr(sim_feedback, "oracle_weak", False):
                _append_flow_log(
                    runtime_state.logs,
                    event="sim_failed_but_oracle_weak",
                    level="warning",
                    stage_id=StageId.SD_6_SIM.value,
                    iteration=iteration,
                    weak_oracle_reason=getattr(sim_feedback, "weak_oracle_reason", ""),
                    weak_oracle_evidence=_jsonable(getattr(sim_feedback, "weak_oracle_evidence", {})),
                    after_waiver_continue=bool(graph_state.get("validation_continued_after_waiver", False)),
                    graph_subgraph="validation_subgraph",
                    graph_node="validation_sd6_sim",
                )
                graph_state["validation_oracle_weak"] = True
            graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=scenario_set.epoch)
            return Command(goto="validation_finalize", update=graph_state)
        _trace_node(graph_state, "validation_sl7_model_review", iteration=iteration)
        return Command(goto="validation_sl7_model_review", update=graph_state)

    def validation_sl7_model_review(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        context: StageContext = graph_state["validation_context"]
        feedback = dict(graph_state.get("validation_feedback") or {})
        stage_metas = list(graph_state.get("validation_stage_metas") or [])
        scenario_set = graph_state["validation_scenario_set"]
        oracle_weak = bool(graph_state.get("validation_oracle_weak", False))
        waiver_audit = graph_state.get("validation_waiver_audit")
        waiver_audit_kind = waiver_audit.get("kind") if isinstance(waiver_audit, dict) else None
        review_reason = (
            "waiver_continue_SD-6_stale_scenario_request"
            if waiver_audit_kind == "stale_overridden_scenario_waiver"
            else "waiver_continue_SD-6_sl10_noop_override"
            if waiver_audit_kind == "sl10_noop_override_waiver"
            else ("waiver_continue_SD-6 ok" if graph_state.get("validation_continued_after_waiver") else "SD-6 ok")
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_7_MODEL_REVIEW.value,
            iteration=iteration,
            reason=review_reason,
            scenario_set_id=scenario_set.scenario_set_id,
            oracle_weak=oracle_weak,
            waiver_audit=_jsonable(waiver_audit) if isinstance(waiver_audit, dict) else None,
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl7_model_review",
        )
        review_payload = {
            "parse": feedback.get(FeedbackSource.PARSE.value),
            "semantic": feedback.get(FeedbackSource.SEMANTIC.value),
            "design": feedback.get(FeedbackSource.DESIGN.value),
            "sim": feedback.get(FeedbackSource.SIM.value),
            "oracle_weak": oracle_weak,
            "waiver_continue": bool(graph_state.get("validation_continued_after_waiver", False)),
        }
        if isinstance(waiver_audit, dict):
            review_payload["waiver_audit"] = _jsonable(waiver_audit)
        review_run = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_7_MODEL_REVIEW,
            graph_node="validation_sl7_model_review",
            subgraph_id="validation_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.model_review(
                    runtime_state.current_dsl,
                    context,
                    review_payload,
                ),
                expected_stage_id=StageId.SL_7_MODEL_REVIEW,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=stage_metas,
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
            ),
        )
        if _is_llm_stage_run(review_run):
            review_feedback = getattr(review_run, "feedback", None)
            if not isinstance(review_feedback, ModelReviewFeedback):
                raise TypeError("SL-7 LLMStageRun must carry ModelReviewFeedback in .feedback")
            review_meta = getattr(review_run, "stage_meta")
        else:
            review_feedback, review_meta = review_run
            _append_stage(runtime_state.stage_records, review_meta)
            stage_metas.append(review_meta)
        feedback[FeedbackSource.MODEL_REVIEW.value] = review_feedback
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_7_MODEL_REVIEW.value,
            iteration=iteration,
            ok=not _model_review_blocks(review_feedback),
            status=str(review_meta.status),
            feedback=_feedback_brief(StageId.SL_7_MODEL_REVIEW.value, review_feedback),
            jump="SD-8" if _model_review_blocks(review_feedback) else "SC-12 success",
            graph_subgraph="validation_subgraph",
            graph_node="validation_sl7_model_review",
        )
        if isinstance(review_feedback, ModelReviewFeedback):
            hints = _extract_grounding_update_hints(source_stage_id=StageId.SL_7_MODEL_REVIEW.value, payload=review_feedback)
            _apply_grounding_update_hints(
                cfg=runtime_cfg,
                state=runtime_state,
                hints=hints,
                iteration=iteration,
                source_stage_id=StageId.SL_7_MODEL_REVIEW.value,
            )
        graph_state["validation_feedback"] = feedback
        graph_state["validation_stage_metas"] = stage_metas
        graph_state["validation_result"] = _validation_result(graph_state, scenario_epoch=scenario_set.epoch)
        return Command(goto="validation_finalize", update=graph_state)

    def validation_finalize(graph_state: _ValidationSubgraphState) -> Command:
        graph_state = _state(graph_state)
        _trace_node(graph_state, "validation_finalize", event="subgraph_exit", iteration=graph_state.get("iteration"))
        return Command(goto=END, update=graph_state)

    graph.add_node("validation_enter", validation_enter)
    graph.add_node("validation_sd2_parse", validation_sd2_parse)
    graph.add_node("validation_sd3_semantic", validation_sd3_semantic)
    graph.add_node("validation_sd4_design", validation_sd4_design)
    graph.add_node("validation_sl5_scenario_generation", validation_sl5_scenario_generation)
    graph.add_node("validation_sd5a_scenario_coverage", validation_sd5a_scenario_coverage)
    graph.add_node("validation_sd5a_reuse_coverage", validation_sd5a_reuse_coverage)
    graph.add_node("validation_sc5f_scenario_freeze", validation_sc5f_scenario_freeze)
    graph.add_node("validation_sd6_sim", validation_sd6_sim)
    graph.add_node("validation_sl7_model_review", validation_sl7_model_review)
    graph.add_node("validation_finalize", validation_finalize)
    graph.add_edge(START, "validation_enter")
    return graph.compile(checkpointer=False)



def _waiver_kind_from_patch(repair_patch: dict[str, Any]) -> str:
    waiver_audit = repair_patch.get("waiver_audit")
    if isinstance(waiver_audit, dict) and waiver_audit.get("kind"):
        kind = str(waiver_audit.get("kind"))
        if kind not in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}:
            raise ValueError(f"waiver entry envelope received unsupported waiver_audit.kind={kind!r}")
        return kind
    selected_trace = repair_patch.get("selected_feedback")
    if isinstance(selected_trace, dict) and selected_trace.get("source_stage") == StageId.SD_6_SIM.value:
        raise ValueError("waiver entry envelope requires SD-6 waiver_audit.kind; refusing unhandled sim waiver fallback")
    return "design_warning_waiver"


def _waiver_tail_start_stage(waiver_kind: str) -> str:
    return (
        StageId.SD_6_SIM.value
        if waiver_kind in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
        else StageId.SD_4_DESIGN.value
    )


def _validate_waiver_kind_selected_consistency(*, kind: str, validation: "_ValidationPass") -> None:
    selected = validation.selected
    if selected is None:
        raise ValueError(f"waiver entry envelope requires validation.selected for tail_kind={kind!r}")
    source, feedback, source_stage = selected
    sd6_waiver_kinds = {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"}
    if kind in sd6_waiver_kinds:
        if source != FeedbackSource.SIM.value or source_stage != StageId.SD_6_SIM.value or not isinstance(feedback, SimFeedback):
            raise ValueError(
                "waiver entry envelope requires waiver_audit.kind="
                f"{kind!r} to match canonical SD-6 sim validation.selected"
            )
        return
    if kind == "design_warning_waiver":
        if source != FeedbackSource.DESIGN.value or source_stage != StageId.SD_4_DESIGN.value or not isinstance(feedback, DesignFeedback):
            raise ValueError(
                "waiver entry envelope requires design_warning_waiver to match canonical SD-4 design validation.selected"
            )
        return
    raise ValueError(f"waiver entry envelope received unsupported tail_kind={kind!r}")


def _validate_waiver_repair_patch_contract(*, repair_patch: dict[str, Any], validation: "_ValidationPass") -> dict[str, Any] | None:
    forbidden_keys = {
        "scenario_epoch",
        "oracle_weak",
        "iteration",
        "graph_state_iteration",
        "validation_ref",
        "validation_source",
        "validation_source_stage_ids",
        "validation_scenario_epoch",
        "validation_oracle_weak",
        "post_waiver_stage_ids",
        "post_waiver_selected_feedback",
        "post_waiver_scenario_epoch",
        "post_waiver_oracle_weak",
    }
    polluted_keys = sorted(str(key) for key in repair_patch.keys() if str(key) in forbidden_keys)
    if polluted_keys:
        raise ValueError(
            "waiver entry envelope forbids validation/scenario/oracle/iteration metadata inside repair_patch: "
            + ", ".join(polluted_keys)
        )
    repair_selected = repair_patch.get("selected_feedback")
    if repair_selected is None:
        return None
    if not isinstance(repair_selected, dict):
        raise ValueError("waiver entry envelope requires repair_patch.selected_feedback to be a dict when present")
    validation_selected = (
        _selected_feedback_trace(*validation.selected, scenario_set=validation.scenario_set)
        if validation.selected is not None
        else None
    )
    if not isinstance(validation_selected, dict):
        raise ValueError("waiver entry envelope requires validation.selected when repair_patch.selected_feedback is present")
    for key in ("source", "source_stage"):
        repair_value = repair_selected.get(key)
        validation_value = validation_selected.get(key)
        if repair_value is not None and str(repair_value) != str(validation_value):
            raise ValueError(
                "waiver entry envelope selected_feedback mismatch: "
                f"repair_patch.{key}={repair_value!r} validation_source.{key}={validation_value!r}"
            )
    for key in ("scenario_set_id",):
        repair_value = repair_selected.get(key)
        validation_value = validation_selected.get(key)
        if repair_value is not None and validation_value is not None and str(repair_value) != str(validation_value):
            raise ValueError(
                "waiver entry envelope selected_feedback mismatch: "
                f"repair_patch.{key}={repair_value!r} validation_source.{key}={validation_value!r}"
            )
    return validation_selected


def _build_waiver_entry_envelope(
    *,
    repair_patch: dict[str, Any],
    validation_ref: str,
    validation: Any,
    iteration: int,
) -> dict[str, Any]:
    """Build and validate the LG-B3 repair→waiver entry envelope.

    The envelope is the machine-checkable contract between LG-B2 repair output
    and LG-B3 waiver continuation.  It deliberately keeps repair decision
    evidence in ``repair_patch`` and validation-tail metadata in the transient
    ``_ValidationPass`` source instead of pretending ``repair_patch`` alone
    carries scenario/oracle/iteration state.
    """

    if not isinstance(repair_patch, dict):
        raise TypeError("waiver entry envelope requires repair_patch to be a dict")
    if not bool(repair_patch.get("waiver_continue")):
        raise ValueError("waiver entry envelope requires repair_patch.waiver_continue=true")
    if bool(repair_patch.get("accepted_candidate")):
        raise ValueError("waiver entry envelope requires no accepted_candidate")
    if "candidate_dsl" in repair_patch and str(repair_patch.get("candidate_dsl") or ""):
        raise ValueError("waiver entry envelope forbids non-empty candidate_dsl on no-edit waiver path")
    if not validation_ref:
        raise ValueError("waiver entry envelope requires a validation_ref")
    if not isinstance(validation, _ValidationPass):
        raise TypeError("waiver entry envelope requires validation to be a _ValidationPass")
    validation_selected_trace = _validate_waiver_repair_patch_contract(repair_patch=repair_patch, validation=validation)
    kind = _waiver_kind_from_patch(repair_patch)
    _validate_waiver_kind_selected_consistency(kind=kind, validation=validation)
    start_stage = _waiver_tail_start_stage(kind)
    waiver_audit = repair_patch.get("waiver_audit")
    if kind in {"stale_overridden_scenario_waiver", "sl10_noop_override_waiver"} and not isinstance(waiver_audit, dict):
        raise ValueError("waiver entry envelope requires waiver_audit dict for SD-6 waiver")
    return {
        "schema_version": LG_B3_WAIVER_ENTRY_ENVELOPE_SCHEMA_VERSION,
        "repair_patch": _jsonable(repair_patch),
        "repair_patch_keys": sorted(str(key) for key in repair_patch.keys()),
        "waiver_continue": True,
        "waiver_audit_kind": waiver_audit.get("kind") if isinstance(waiver_audit, dict) else None,
        "accepted_candidate": False,
        "selected_feedback": _jsonable(repair_patch.get("selected_feedback")),
        "repair_stage_ids": _jsonable(repair_patch.get("repair_stage_ids")),
        "exit_reason": repair_patch.get("exit_reason"),
        "validation_ref": validation_ref,
        "validation_source_stage_ids": _stage_ids(validation.stage_metas),
        "validation_scenario_epoch": validation.scenario_epoch,
        "validation_oracle_weak": validation.oracle_weak,
        "validation_source": {
            "object_type": type(validation).__name__,
            "selected_feedback": _jsonable(
                validation_selected_trace
                if validation_selected_trace is not None
                else (
                    _selected_feedback_trace(*validation.selected, scenario_set=validation.scenario_set)
                    if validation.selected is not None
                    else None
                )
            ),
            "stage_ids": _stage_ids(validation.stage_metas),
        },
        "iteration": int(iteration),
        "graph_state_iteration": int(iteration),
        "tail_start_stage": start_stage,
        "tail_kind": kind,
    }


def _drop_repair_subgraph_state(graph_state: dict[str, Any]) -> None:
    for key in list(graph_state.keys()):
        if str(key).startswith("repair_") and key != "repair_patch":
            graph_state.pop(key, None)




def _build_waiver_continuation_subgraph(*, validation_subgraph: Any) -> Any:
    """Build the LG-B3 waiver continuation subgraph.

    The subgraph normalizes the repair→waiver input envelope and delegates the
    actual SD/SL validation-tail semantics to the LG-B1 validation subgraph.
    It intentionally does not redefine SD-4/SD-6/SL-7 academic judgments.
    """

    graph = StateGraph(_WaiverSubgraphState)

    def _state(graph_state: _WaiverSubgraphState) -> _WaiverSubgraphState:
        return dict(graph_state)

    def _iteration(graph_state: _WaiverSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def waiver_subgraph_enter(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        repair_patch = dict(graph_state.get("repair_patch") or {})
        validation_ref = str(graph_state.get("validation_ref") or "")
        validation = graph_state.get("validation_continuation_source")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("waiver continuation subgraph requires a _ValidationPass validation_continuation_source")
        envelope = _build_waiver_entry_envelope(
            repair_patch=repair_patch,
            validation_ref=validation_ref,
            validation=validation,
            iteration=iteration,
        )
        kind = str(envelope["tail_kind"])
        start_stage = str(envelope["tail_start_stage"])
        graph_state["waiver_input_envelope"] = envelope
        graph_state["waiver_validation_ref"] = validation_ref
        graph_state["waiver_validation_source"] = validation
        graph_state["waiver_tail_kind"] = kind
        graph_state["waiver_tail_start_stage"] = start_stage
        _trace_node(graph_state, "waiver_subgraph_enter", event="subgraph_enter", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_enter",
            iteration=iteration,
            waiver_tail_kind=kind,
            tail_start_stage=start_stage,
            waiver_input_envelope=_jsonable(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_enter",
        )
        return Command(goto="waiver_tail_decision", update=graph_state)

    def waiver_tail_decision(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        iteration = _iteration(graph_state)
        start_stage = str(graph_state.get("waiver_tail_start_stage") or StageId.SD_4_DESIGN.value)
        kind = str(graph_state.get("waiver_tail_kind") or "design_warning_waiver")
        _trace_node(graph_state, "waiver_tail_decision", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
        return Command(goto="waiver_sim_tail" if start_stage == StageId.SD_6_SIM.value else "waiver_design_tail", update=graph_state)

    def _invoke_validation_tail(graph_state: _WaiverSubgraphState, *, tail_node: str) -> _WaiverSubgraphState:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        validation = graph_state.get("waiver_validation_source")
        if not isinstance(validation, _ValidationPass):
            validation = graph_state.get("validation_continuation_source")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("waiver continuation tail requires a _ValidationPass validation source")
        graph_state["validation_continuation_source"] = validation
        repair_patch = dict(graph_state.get("repair_patch") or {})
        waiver_audit = repair_patch.get("waiver_audit")
        graph_state["validation_waiver_audit"] = _jsonable(waiver_audit) if isinstance(waiver_audit, dict) else None
        _trace_node(
            graph_state,
            tail_node,
            iteration=iteration,
            tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
        )
        try:
            invoked = dict(
                validation_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:waiver-tail:{tail_node}:{iteration}"}},
                )
            )
        except _LLMRetryExhausted as exc:
            graph_state["waiver_retry_error_envelope"] = dict(graph_state.get("waiver_input_envelope") or {})
            graph_state["waiver_retry_error_tail_node"] = tail_node
            raise
        continued_validation = invoked.get("validation_result")
        if not isinstance(continued_validation, _ValidationPass):
            raise TypeError("validation subgraph did not return a _ValidationPass after waiver continuation")
        invoked["waiver_result"] = continued_validation
        return invoked

    def waiver_design_tail(graph_state: _WaiverSubgraphState) -> Command:
        return Command(goto="waiver_subgraph_finalize", update=_invoke_validation_tail(graph_state, tail_node="waiver_design_tail"))

    def waiver_sim_tail(graph_state: _WaiverSubgraphState) -> Command:
        return Command(goto="waiver_subgraph_finalize", update=_invoke_validation_tail(graph_state, tail_node="waiver_sim_tail"))

    def waiver_subgraph_finalize(graph_state: _WaiverSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state: _RunState = graph_state["runtime_state"]
        iteration = _iteration(graph_state)
        continued_validation = graph_state.get("waiver_result")
        if not isinstance(continued_validation, _ValidationPass):
            continued_validation = graph_state.get("validation_result")
        if not isinstance(continued_validation, _ValidationPass):
            raise TypeError("waiver continuation subgraph did not receive a _ValidationPass result")
        envelope = dict(graph_state.get("waiver_input_envelope") or {})
        _trace_node(
            graph_state,
            "waiver_subgraph_finalize",
            event="subgraph_exit",
            iteration=iteration,
            tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
            post_waiver_stage_ids=_stage_ids(continued_validation.stage_metas),
        )
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_finalize",
            iteration=iteration,
            waiver_tail_kind=graph_state.get("waiver_tail_kind"),
            tail_start_stage=graph_state.get("waiver_tail_start_stage"),
            post_waiver_stage_ids=_stage_ids(continued_validation.stage_metas),
            waiver_input_envelope_hash=_short_hash(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_finalize",
        )
        return Command(goto=END, update=graph_state)

    graph.add_node("waiver_subgraph_enter", waiver_subgraph_enter)
    graph.add_node("waiver_tail_decision", waiver_tail_decision)
    graph.add_node("waiver_design_tail", waiver_design_tail)
    graph.add_node("waiver_sim_tail", waiver_sim_tail)
    graph.add_node("waiver_subgraph_finalize", waiver_subgraph_finalize)
    graph.add_edge(START, "waiver_subgraph_enter")
    graph.add_edge("waiver_subgraph_finalize", END)
    return graph.compile(checkpointer=False)


def _seed_waiver_exception_evidence(
    graph_state: dict[str, Any],
    *,
    envelope: dict[str, Any],
    tail_node: str,
    iteration: int,
    retry_stage_id: str | None = None,
) -> None:
    """Preserve LG-B3 evidence before entering a nested tail that may raise.

    LangGraph subgraph state updates are not returned to the parent when an
    inner node raises ``_LLMRetryExhausted``.  The parent therefore pre-seeds a
    minimal, semantically equivalent trace/envelope so retry-exhausted waiver
    tails remain distinguishable from ordinary validation failures in the final
    ``AgentLoopRunRecord``.
    """

    if not envelope:
        return
    kind = str(envelope.get("tail_kind") or "")
    start_stage = str(envelope.get("tail_start_stage") or "")
    graph_state["waiver_input_envelope"] = dict(envelope)
    graph_state["waiver_tail_kind"] = kind
    graph_state["waiver_tail_start_stage"] = start_stage
    runtime_state = graph_state.get("runtime_state")
    _trace_node(graph_state, "waiver_subgraph_enter", event="subgraph_enter", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, "waiver_tail_decision", iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, tail_node, iteration=iteration, tail_kind=kind, tail_start_stage=start_stage)
    _trace_node(graph_state, "validation_subgraph", event="subgraph_enter", iteration=iteration, continued_after_waiver=True)
    if start_stage == StageId.SD_6_SIM.value:
        _trace_node(graph_state, "validation_sd6_sim", iteration=iteration, continued_after_waiver=True, waiver_audit_kind=envelope.get("waiver_audit_kind"))
    else:
        _trace_node(graph_state, "validation_sd4_design", iteration=iteration, continued_after_waiver=True)
    retry_node_by_stage = {
        StageId.SL_5_SCENARIO_GENERATION.value: "validation_sl5_scenario_generation",
        StageId.SD_5A_SCENARIO_COVERAGE.value: "validation_sd5a_scenario_coverage",
        StageId.SC_5F_SCENARIO_FREEZE.value: "validation_sc5f_scenario_freeze",
        StageId.SD_6_SIM.value: "validation_sd6_sim",
        StageId.SL_7_MODEL_REVIEW.value: "validation_sl7_model_review",
    }
    retry_node = retry_node_by_stage.get(str(retry_stage_id or ""))
    if retry_node is not None:
        _trace_node(graph_state, retry_node, iteration=iteration, continued_after_waiver=True, retry_exhausted=True)
    if isinstance(runtime_state, _RunState):
        _append_flow_log(
            runtime_state.logs,
            event="waiver_subgraph_enter",
            iteration=iteration,
            waiver_tail_kind=kind,
            tail_start_stage=start_stage,
            waiver_input_envelope=_jsonable(envelope),
            graph_subgraph="waiver_continuation_subgraph",
            graph_node="waiver_subgraph_enter",
        )
    seen_trace_keys: set[tuple[str, str, str]] = set()
    deduped_trace: list[dict[str, Any]] = []
    for item in list(graph_state.get("graph_trace", []) or []):
        if not isinstance(item, dict):
            continue
        key = (
            str(item.get("node_id") or ""),
            str(item.get("event") or ""),
            str(item.get("iteration") or ""),
        )
        if key in seen_trace_keys:
            continue
        seen_trace_keys.add(key)
        deduped_trace.append(item)
    graph_state["graph_trace"] = deduped_trace

def _build_repair_subgraph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
) -> Any:
    """Build the LG-B2 stage-level repair subgraph.

    LangGraph owns the repair micro-loop: SD-8 prepares a request batch, SL-9
    proposes/accepts per-request edits, SL-10 reviews or requests rework, and
    SC-11 records accepted candidate handoff.  Canonical stage semantics remain
    in ``method.staged_runtime`` helpers; this subgraph only replaces the
    previous Python-level repair-path orchestration.
    """

    graph = StateGraph(_RepairSubgraphState)

    def _state(graph_state: _RepairSubgraphState) -> _RepairSubgraphState:
        return dict(graph_state)

    def _runtime_state(graph_state: _RepairSubgraphState) -> _RunState:
        return graph_state["runtime_state"]

    def _iteration(graph_state: _RepairSubgraphState) -> int:
        return int(graph_state.get("iteration", 0))

    def repair_enter(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation = graph_state.get("repair_validation")
        if not isinstance(validation, _ValidationPass):
            raise TypeError("repair subgraph requires repair_validation=_ValidationPass")
        assert validation.selected is not None
        source, selected_feedback, source_stage = validation.selected
        selected_trace = _selected_feedback_trace(source, selected_feedback, source_stage, scenario_set=validation.scenario_set)
        variable_role_summary = _diagnostic_variable_role_summary(graph_state["nl"], selected_feedback)
        if variable_role_summary:
            selected_trace["variable_role_summary"] = variable_role_summary
        if selected_trace["pre_scenario"]:
            runtime_state.pre_scenario_repair_count += 1
        _trace_node(graph_state, "repair_enter", event="subgraph_enter", iteration=iteration, source_stage=source_stage)
        _append_flow_log(
            runtime_state.logs,
            event="repair_path_enter",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            source=source,
            source_stage=source_stage,
            selected_feedback=selected_trace,
            current_dsl_hash=_hash_text(runtime_state.current_dsl),
            current_dsl=runtime_state.current_dsl,
            jump="SD-8",
            graph_subgraph="repair_subgraph",
            graph_node="repair_enter",
        )
        graph_state["repair_validation"] = validation
        graph_state["repair_source"] = source
        graph_state["repair_source_stage"] = source_stage
        graph_state["repair_selected_feedback"] = selected_feedback
        graph_state["repair_selected_trace"] = selected_trace
        return Command(goto="repair_sd8_fix_requests", update=graph_state)

    def repair_sd8_fix_requests(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        source = str(graph_state["repair_source"])
        source_stage = str(graph_state["repair_source_stage"])
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        _trace_node(graph_state, "repair_sd8_fix_requests", iteration=iteration, source_stage=source_stage)

        rework_locked = runtime_state.pending_repair_rejection is not None and runtime_state.pending_original_fix_plan is not None
        if rework_locked:
            fix_plan, fix_meta = _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="sd8_fix_plan",
                stage_id=StageId.SD_8_FIX_PLAN.value,
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "selected_feedback": None,
                    "source": "repair_review",
                    "rejection": runtime_state.pending_repair_rejection,
                    "original": runtime_state.pending_original_fix_plan,
                },
                call=lambda: run_sd8_fix_plan(
                    None,
                    source="repair_review",
                    rejection=runtime_state.pending_repair_rejection,
                    original=runtime_state.pending_original_fix_plan,
                ),
            )
        else:
            fix_plan, fix_meta = _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="sd8_fix_plan",
                stage_id=StageId.SD_8_FIX_PLAN.value,
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "selected_feedback": selected_feedback,
                    "source": source,
                    "source_stage": source_stage,
                    "grounding_map": runtime_cfg.grounding_map,
                    "before_dsl": runtime_state.current_dsl,
                },
                call=lambda: run_sd8_fix_plan(
                    selected_feedback,
                    source=source,
                    source_stage=source_stage,
                    grounding_map=runtime_cfg.grounding_map,
                    before_dsl=runtime_state.current_dsl,
                ),
            )
        _append_stage(runtime_state.stage_records, fix_meta)
        effective_fix_plan = fix_plan.original if isinstance(fix_plan, RevisedFixPlan) else fix_plan
        assert isinstance(effective_fix_plan, FixPlan)
        aggregate_stage_ids = [fix_meta.stage_id]
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            ok=True,
            status=str(fix_meta.status),
            plan_kind="RevisedFixPlan" if isinstance(fix_plan, RevisedFixPlan) else "FixPlan",
            fix_plan=_compact_json(effective_fix_plan, max_list_items=10),
            jump="SL-9",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sd8_fix_requests",
        )
        request_batch = _fix_request_batch_from_plan(
            iteration=iteration,
            source=source,
            source_stage=source_stage,
            selected_trace=selected_trace,
            fix_plan=fix_plan,
            effective_fix_plan=effective_fix_plan,
            scenario_set=validation.scenario_set,
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="request_batch",
            batch=request_batch,
            old_dsl=runtime_state.current_dsl,
            next_action="sl9_decision_and_repair",
            notes=["SD-8 produced FixRequestBatch; deterministic stage does not decide final repair."],
        )
        _append_flow_log(
            runtime_state.logs,
            event="fix_request_batch",
            stage_id=StageId.SD_8_FIX_PLAN.value,
            iteration=iteration,
            batch_id=request_batch.batch_id,
            request_count=len(request_batch.requests),
            hard_block=request_batch.has_hard_block,
            requests=_jsonable(request_batch.requests),
            next_action="SL-9",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sd8_fix_requests",
        )
        if source == FeedbackSource.DESIGN.value and isinstance(selected_feedback, DesignFeedback):
            _lg_e3_fixed_tool_call(
                graph_state,
                tool_name="warning_repair_attempt_marker",
                stage_id="warning_budget_state",
                graph_node="repair_sd8_fix_requests",
                iteration=iteration,
                input_payload={
                    "warning_budget_state": validation.context.warning_budget_state,
                    "instance_keys": [item.instance_key for item in selected_feedback.blocking_items],
                },
                call=lambda: mark_warning_repair_attempt(
                    validation.context.warning_budget_state,
                    [item.instance_key for item in selected_feedback.blocking_items],
                ),
            )
            runtime_state.warning_budget_state = validation.context.warning_budget_state

        graph_state["repair_fix_plan"] = fix_plan
        graph_state["repair_effective_fix_plan"] = effective_fix_plan
        graph_state["repair_request_batch"] = request_batch
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_rework_locked_initial"] = rework_locked
        graph_state["repair_max_rework_attempts"] = max(1 + runtime_cfg.min_sl10_rework_attempts, runtime_cfg.max_iterations - iteration)
        graph_state["repair_rework_attempt"] = 0
        graph_state["repair_last_iteration_patch"] = {}
        graph_state["repair_last_repair_review"] = None
        graph_state["repair_last_sl10_output"] = None
        return Command(goto="repair_sl9_repair", update=graph_state)

    def repair_sl9_repair(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        fix_plan = graph_state["repair_fix_plan"]
        request_batch = graph_state["repair_request_batch"]
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        attempt_rework_locked = bool(graph_state.get("repair_rework_locked_initial")) or rework_attempt > 0
        repair_memory_for_attempt = _repair_memory_for_prompt(runtime_state.fix_log)
        active_request_batch = _fix_request_batch_with_repair_memory(
            request_batch,
            repair_memory=repair_memory_for_attempt,
            rework_locked=attempt_rework_locked,
        )
        _trace_node(
            graph_state,
            "repair_sl9_repair",
            iteration=iteration,
            rework_attempt=rework_attempt,
            rework_locked=attempt_rework_locked,
            batch_id=active_request_batch.batch_id,
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_enter",
            stage_id=StageId.SL_9_REPAIR.value,
            iteration=iteration,
            reason="fix_requests_ready" if not attempt_rework_locked else "sl10_rework_locked",
            rework_attempt=rework_attempt,
            rework_locked=attempt_rework_locked,
            batch_id=active_request_batch.batch_id,
            request_ids=[request.request_id for request in active_request_batch.requests],
            repair_memory=_compact_json(repair_memory_for_attempt, max_list_items=8),
            old_dsl=runtime_state.current_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl9_repair",
        )
        request = RepairRequest(
            nl=graph_state["nl"],
            grounding_map=runtime_cfg.grounding_map,
            old_dsl=runtime_state.current_dsl,
            fix_plan=fix_plan,
            selected_feedback=selected_feedback,
            selected_feedback_trace=selected_trace,
            scenario_set=validation.scenario_set,
            iteration=iteration,
            repair_attempt=len(runtime_state.repair_history),
            fix_request_batch=active_request_batch,
            fix_log=[
                *list(runtime_state.fix_log),
                {
                    "entry_id": f"runtime-current-repair-memory-{rework_attempt}",
                    "iteration": iteration,
                    "phase": "current_sl9_repair_memory",
                    "repair_memory": repair_memory_for_attempt,
                    "next_action": "sl9_must_address_repair_memory",
                },
            ],
            rework_locked=attempt_rework_locked,
        )
        request.repair_memory = repair_memory_for_attempt
        repair_run = _lg_d2_wrap_llm_stage_node(
            graph_state,
            stage_id=StageId.SL_9_REPAIR,
            graph_node="repair_sl9_repair",
            subgraph_id="repair_subgraph",
            call=lambda: _append_llm_stage_run(
                run=adapters.repair(request),
                expected_stage_id=StageId.SL_9_REPAIR,
                stage_records=runtime_state.stage_records,
                iteration_stage_metas=None,
                llm_interactions=runtime_state.llm_interactions,
                logs=runtime_state.logs,
                iteration=iteration,
            ),
        )
        parsed_output: Any = {}
        if _is_llm_stage_run(repair_run):
            parsed_output = getattr(repair_run, "parsed_output", {}) or {}
            if not isinstance(parsed_output, dict):
                raise TypeError("SL-9 LLMStageRun parsed_output must be a dict with candidate_dsl/decisions")
            candidate_dsl = str(parsed_output.get("candidate_dsl") or "")
            aggregate_stage_ids.append(getattr(repair_run, "stage_meta").stage_id)
        else:
            if isinstance(repair_run, dict):
                parsed_output = dict(repair_run)
                candidate_dsl = str(parsed_output.get("candidate_dsl") or "")
            else:
                candidate_dsl = str(repair_run or "")
                parsed_output = {"candidate_dsl": candidate_dsl}
            repair_meta = _sl9_meta(runtime_state.current_dsl, fix_plan, candidate_dsl)
            _append_stage(runtime_state.stage_records, repair_meta)
            aggregate_stage_ids.append(repair_meta.stage_id)
            runtime_state.llm_interactions.append(
                {
                    "stage_id": StageId.SL_9_REPAIR.value,
                    "provider": runtime_cfg.adapter_mode,
                    "model_id": "explicit-adapter",
                    "real_llm_provider_api": False,
                    "prompt_template_version": "pr-b1-repair-adapter.v2-fixrequest",
                    "input_hash": _hash_text(runtime_state.current_dsl),
                    "prompt_hash": repair_meta.prompt_hash,
                    "raw_output_hash": repair_meta.output_hash,
                    "raw_output": candidate_dsl,
                    "parsed_output": {"candidate_dsl": candidate_dsl},
                    "schema_validation_ok": bool(candidate_dsl),
                    "note": "Explicit adapter returned DSL only; runtime fills per-request SL-9 decisions for compatibility.",
                }
            )
        request.candidate_dsl = candidate_dsl
        sl9_decision = _coerce_sl9_decision_output(
            parsed_output,
            batch=active_request_batch,
            candidate_dsl=candidate_dsl,
            rework_locked=attempt_rework_locked,
        )
        sl9_decision.diff_summary = sl9_decision.diff_summary or _dsl_diff_summary(runtime_state.current_dsl, candidate_dsl)
        request.sl9_decision = sl9_decision
        request.diff_summary = dict(sl9_decision.diff_summary)
        request.fix_log = list(runtime_state.fix_log)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_9_REPAIR.value,
            iteration=iteration,
            ok=bool(sl9_decision.accepted_request_ids),
            rework_attempt=rework_attempt,
            accepted_request_ids=sl9_decision.accepted_request_ids,
            rejected_request_ids=sl9_decision.rejected_request_ids,
            decisions=_jsonable(sl9_decision.decisions),
            diff_summary=sl9_decision.diff_summary,
            jump="SL-10" if sl9_decision.accepted_request_ids else "waiver_continue_or_exit",
            candidate_dsl=candidate_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl9_repair",
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl9_decision" if rework_attempt == 0 else "sl9_rework_decision",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            next_action="sl10_review" if sl9_decision.accepted_request_ids else "reject_or_waiver",
            notes=[*sl9_decision.repair_rationale, *( ["rework_locked=true"] if attempt_rework_locked else [] )],
        )
        graph_state["repair_active_request_batch"] = active_request_batch
        graph_state["repair_sl9_decision"] = sl9_decision
        graph_state["repair_candidate_dsl"] = candidate_dsl
        graph_state["repair_request"] = request
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        if sl9_decision.accepted_request_ids:
            return Command(goto="repair_sl10_review", update=graph_state)

        hard_rejected = any(req.hard_block for req in active_request_batch.requests)
        stale_waiver_audit = (
            _stale_overridden_scenario_waiver_audit(
                active_request_batch=active_request_batch,
                sl9_decision=sl9_decision,
                fix_log=runtime_state.fix_log,
                current_dsl_hash=_hash_text(runtime_state.current_dsl),
                scenario_set=validation.scenario_set,
            )
            if hard_rejected
            else None
        )
        standard_waiver_continue = (
            not hard_rejected
            and bool(active_request_batch.requests)
            and all(req.waiver_allowed for req in active_request_batch.requests)
            and all(decision.decision == "reject" for decision in sl9_decision.decisions)
        )
        waiver_continue = standard_waiver_continue or stale_waiver_audit is not None
        waiver_reason = (
            ":stale_overridden_scenario_waiver"
            if stale_waiver_audit is not None
            else ":waiver_continue"
            if standard_waiver_continue
            else ":hard_block"
            if hard_rejected
            else ":waiver_only"
        )
        rejection = RepairRejection(
            rejected_by_stage=StageId.SL_9_REPAIR.value,
            reason="sl9_rejected_all_fix_requests" + waiver_reason,
            target_resolved=waiver_continue,
            regression_detected=False,
            drift_risk="minor" if stale_waiver_audit is not None else "major" if hard_rejected else "minor",
            evidence=[
                *_jsonable(sl9_decision.decisions),
                *([_jsonable(stale_waiver_audit)] if stale_waiver_audit is not None else []),
            ],
        )
        repair_review = RepairReviewFeedback(
            ok=waiver_continue,
            target_resolved=waiver_continue,
            drift_risk=rejection.drift_risk,
            local_rejection=None if waiver_continue else rejection,
        )
        if waiver_continue:
            _append_flow_log(
                runtime_state.logs,
                event=(
                    "sl9_all_rejected_stale_scenario_waiver_continue"
                    if stale_waiver_audit is not None
                    else "sl9_all_rejected_waiver_continue"
                ),
                level="info",
                stage_id=StageId.SL_9_REPAIR.value,
                iteration=iteration,
                source_stage=str(graph_state.get("repair_source_stage") or ""),
                batch_id=active_request_batch.batch_id,
                note="no candidate DSL; downstream validation continues without SC-11 acceptance",
                waiver_audit=_jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
                jump="continue_after_current_stage",
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl9_repair",
            )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl9_all_rejected",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            next_action="continue_after_waiver" if waiver_continue else "exit_rejected",
            notes=[
                rejection.reason,
                *(
                    [f"waiver_audit:{stale_waiver_audit['kind']}:{_short_hash(stale_waiver_audit)}"]
                    if stale_waiver_audit is not None
                    else []
                ),
            ],
        )
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review": _jsonable(repair_review),
            "accepted": False,
            "waiver_continue": waiver_continue,
            "waiver_audit": _jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
        }
        runtime_state.repair_history.append(repair_payload)
        graph_state["repair_accepted"] = False
        graph_state["repair_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": False,
            "waiver_continue": waiver_continue,
            "waiver_audit": _jsonable(stale_waiver_audit) if stale_waiver_audit is not None else None,
            "exit_reason": "all_fix_requests_rejected_as_waiver_continue" if waiver_continue else rejection.reason,
            "retryable_repair_rejection": False,
        }
        return Command(goto="repair_finalize", update=graph_state)

    def repair_sl10_review(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_feedback = graph_state["repair_selected_feedback"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        active_request_batch = graph_state["repair_active_request_batch"]
        sl9_decision = graph_state["repair_sl9_decision"]
        candidate_dsl = str(graph_state.get("repair_candidate_dsl") or "")
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        attempt_rework_locked = bool(graph_state.get("repair_rework_locked_initial")) or rework_attempt > 0
        max_rework_attempts = int(graph_state.get("repair_max_rework_attempts", 1))
        _trace_node(
            graph_state,
            "repair_sl10_review",
            iteration=iteration,
            rework_attempt=rework_attempt,
            batch_id=active_request_batch.batch_id,
        )
        review_request = RepairRequest(
            nl=graph_state["nl"],
            grounding_map=runtime_cfg.grounding_map,
            old_dsl=runtime_state.current_dsl,
            fix_plan=effective_fix_plan,
            selected_feedback=selected_feedback,
            selected_feedback_trace=selected_trace,
            scenario_set=validation.scenario_set,
            candidate_dsl=candidate_dsl,
            iteration=iteration,
            repair_attempt=len(runtime_state.repair_history),
            warning_budget_state=validation.context.warning_budget_state,
            fix_request_batch=active_request_batch,
            fix_log=list(runtime_state.fix_log),
            sl9_decision=sl9_decision,
            diff_summary=sl9_decision.diff_summary,
            rework_locked=attempt_rework_locked,
        )
        local_review, local_meta = _lg_e3_fixed_tool_call(
            graph_state,
            tool_name="sd10_repair_review_local_check",
            stage_id=StageId.SD_10_REPAIR_REVIEW.value,
            graph_node="repair_sl10_review",
            iteration=iteration,
            input_payload={"repair_request": review_request},
            call=lambda: adapters.repair_review(review_request),
        )
        local_check_evidence = _local_repair_check_evidence(
            repair_review=local_review,
            repair_review_meta=local_meta,
            scenario_set=validation.scenario_set,
        )
        review_request.local_check_evidence = local_check_evidence
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SD_10_REPAIR_REVIEW.value,
            iteration=iteration,
            ok=local_review.ok,
            status=str(local_meta.status),
            local_check_evidence=local_check_evidence,
            jump="SL-10",
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl10_review",
        )
        local_sd10_repair_review = _jsonable(local_review)
        repair_review_input_summary = {
            "nl_hash": _hash_text(graph_state["nl"]),
            "has_nl_input": bool(graph_state["nl"]),
            "has_grounding_map": runtime_cfg.grounding_map is not None,
            "old_dsl_hash": _hash_text(runtime_state.current_dsl),
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "fix_plan_target": getattr(effective_fix_plan, "target", None),
            "fix_plan_source_stage": getattr(effective_fix_plan, "source_stage", None),
            "fix_request_batch_id": active_request_batch.batch_id,
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "inputs": ["NL", "GroundingMap", "old_dsl", "candidate_dsl", "FixRequestBatch", "SL9Decisions", "FixLog", "LocalCheckEvidence", "ScenarioSet"],
            "local_check_stage_id": StageId.SD_10_REPAIR_REVIEW.value,
            "active_review_stage_id": StageId.SL_10_REPAIR_REVIEW.value,
            "rework_attempt": rework_attempt,
            "rework_locked": attempt_rework_locked,
        }
        if adapters.sl10_review is not None:
            _append_flow_log(
                runtime_state.logs,
                event="stage_enter",
                stage_id=StageId.SL_10_REPAIR_REVIEW.value,
                iteration=iteration,
                reason="candidate_dsl_and_local_evidence_ready",
                rework_attempt=rework_attempt,
                batch_id=active_request_batch.batch_id,
                inputs=repair_review_input_summary["inputs"],
                old_dsl_hash=_hash_text(runtime_state.current_dsl),
                candidate_dsl_hash=_hash_text(candidate_dsl),
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl10_review",
            )
            sl10_run = _lg_d2_wrap_llm_stage_node(
                graph_state,
                stage_id=StageId.SL_10_REPAIR_REVIEW,
                graph_node="repair_sl10_review",
                subgraph_id="repair_subgraph",
                call=lambda: _append_llm_stage_run(
                    run=adapters.sl10_review(review_request, local_review),
                    expected_stage_id=StageId.SL_10_REPAIR_REVIEW,
                    stage_records=runtime_state.stage_records,
                    iteration_stage_metas=None,
                    llm_interactions=runtime_state.llm_interactions,
                    logs=runtime_state.logs,
                    iteration=iteration,
                ),
            )
            if _is_llm_stage_run(sl10_run):
                sl10_output = getattr(sl10_run, "feedback", None)
                if not isinstance(sl10_output, SL10RepairReviewOutput):
                    parsed = getattr(sl10_run, "parsed_output", {}) or {}
                    sl10_output = SL10RepairReviewOutput(
                        ok=bool(parsed.get("decision") == "pass"),
                        decision=str(parsed.get("decision") or "invalid_output"),  # type: ignore[arg-type]
                        target_resolved=bool(parsed.get("target_resolved", False)),
                        regression_detected=bool(parsed.get("regression_detected", True)),
                        drift_risk=str(parsed.get("drift_risk") or "major"),  # type: ignore[arg-type]
                        rework_instructions=[str(item) for item in parsed.get("rework_instructions", [])],
                        evidence=_jsonable(parsed.get("evidence", [])),
                        local_override_rationale=[str(item) for item in parsed.get("local_override_rationale", [])],
                        local_check_evidence=local_check_evidence,
                        review_meta=None,
                        meta=getattr(sl10_run, "stage_meta"),
                    )
                sl10_output.local_check_evidence = sl10_output.local_check_evidence or local_check_evidence
                aggregate_stage_ids.append(getattr(sl10_run, "stage_meta").stage_id)
            else:
                sl10_output, sl10_meta = sl10_run
                _append_stage(runtime_state.stage_records, sl10_meta)
                aggregate_stage_ids.append(sl10_meta.stage_id)
        else:
            sl10_output = _default_sl10_output_from_local_checks(local_review=local_review, local_evidence=local_check_evidence)
            assert sl10_output.meta is not None
            _append_stage(runtime_state.stage_records, sl10_output.meta)
            aggregate_stage_ids.append(sl10_output.meta.stage_id)
        repair_review = _repair_review_from_sl10(
            sl10_output,
            local_review=local_review,
            candidate_dsl_hash=_hash_text(candidate_dsl),
            local_check_evidence_hash=_short_hash(local_check_evidence),
        )
        accepted = bool(sl10_output.ok)
        previous_candidate_hashes = [
            str(entry.get("candidate_dsl_hash") or "")
            for entry in runtime_state.fix_log
            if entry.get("candidate_dsl_hash")
            and str(entry.get("phase") or "") in {"sl10_review", "sl10_rework_review"}
        ]
        repair_memory = _repair_memory_for_log(
            sl10_output=sl10_output,
            local_check_evidence=local_check_evidence,
            candidate_dsl=candidate_dsl,
            previous_candidate_hashes=previous_candidate_hashes,
        )
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            iteration=iteration,
            ok=accepted,
            rework_attempt=rework_attempt,
            decision=sl10_output.decision,
            target_resolved=sl10_output.target_resolved,
            regression_detected=sl10_output.regression_detected,
            drift_risk=sl10_output.drift_risk,
            rework_instructions=sl10_output.rework_instructions,
            repair_memory=_compact_json(repair_memory, max_list_items=8),
            evidence=_compact_json(sl10_output.evidence, max_list_items=8),
            local_override_rationale=sl10_output.local_override_rationale,
            jump="SC-11" if accepted else ("SL-9 rework" if rework_attempt + 1 < max_rework_attempts else "SC-12 rejected"),
            graph_subgraph="repair_subgraph",
            graph_node="repair_sl10_review",
        )
        sl10_grounding_hints = _extract_grounding_update_hints(
            source_stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            payload=sl10_output,
        )
        sl10_grounding_hints = _apply_grounding_update_hints(
            cfg=runtime_cfg,
            state=runtime_state,
            hints=sl10_grounding_hints,
            iteration=iteration,
            source_stage_id=StageId.SL_10_REPAIR_REVIEW.value,
        )
        noop_override_waiver_audit = (
            _sl10_noop_override_waiver_audit(
                active_request_batch=active_request_batch,
                sl9_decision=sl9_decision,
                local_review=local_review,
                local_check_evidence=local_check_evidence,
                sl10_output=sl10_output,
                old_dsl=runtime_state.current_dsl,
                candidate_dsl=candidate_dsl,
                scenario_set=validation.scenario_set,
            )
            if accepted
            else None
        )
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_local_check_evidence"] = local_check_evidence
        graph_state["repair_local_sd10_repair_review"] = local_sd10_repair_review
        graph_state["repair_review_input_summary"] = repair_review_input_summary
        graph_state["repair_sl10_output"] = sl10_output
        graph_state["repair_repair_review"] = repair_review
        graph_state["repair_memory"] = repair_memory
        graph_state["repair_grounding_update_hints"] = sl10_grounding_hints
        graph_state["repair_noop_override_waiver_audit"] = noop_override_waiver_audit
        if noop_override_waiver_audit is not None:
            _append_flow_log(
                runtime_state.logs,
                event="sl10_noop_override_waiver_continue",
                level="info",
                stage_id=StageId.SL_10_REPAIR_REVIEW.value,
                iteration=iteration,
                source_stage=str(graph_state.get("repair_source_stage") or ""),
                batch_id=active_request_batch.batch_id,
                note="SL-10 accepted a no-op local override; downstream validation continues without SC-11 budget consumption",
                waiver_audit=_jsonable(noop_override_waiver_audit),
                jump="continue_after_current_stage",
                graph_subgraph="repair_subgraph",
                graph_node="repair_sl10_review",
            )
            repair_review = RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="minor")
            _fix_log_entry(
                state=runtime_state,
                iteration=iteration,
                phase="sl10_noop_override_waiver",
                batch=active_request_batch,
                decisions=sl9_decision.decisions,
                old_dsl=runtime_state.current_dsl,
                candidate_dsl=candidate_dsl,
                diff_summary=sl9_decision.diff_summary,
                local_check_evidence=local_check_evidence,
                sl10_review=sl10_output,
                repair_memory=repair_memory,
                next_action="continue_after_waiver",
                notes=[
                    f"waiver_audit:{noop_override_waiver_audit['kind']}:{_short_hash(noop_override_waiver_audit)}",
                    *sl10_output.local_override_rationale,
                    *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
                ],
            )
            repair_payload = {
                "iteration": iteration,
                "selected_feedback": selected_trace,
                "plan_kind": active_request_batch.legacy_plan_kind,
                "fix_plan": _jsonable(effective_fix_plan),
                "fix_request_batch": _jsonable(active_request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "candidate_dsl": candidate_dsl,
                "candidate_dsl_hash": _hash_text(candidate_dsl),
                "repair_review_input_summary": repair_review_input_summary,
                "local_check_evidence": _jsonable(local_check_evidence),
                "sd10_repair_review": local_sd10_repair_review,
                "sl10_repair_review": _jsonable(sl10_output),
                "grounding_update_hints": _jsonable(sl10_grounding_hints),
                "repair_review": _jsonable(repair_review),
                "accepted": False,
                "accepted_noop_override": True,
                "waiver_continue": True,
                "waiver_audit": _jsonable(noop_override_waiver_audit),
                "repair_stage_ids": list(aggregate_stage_ids),
                "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
                "fix_log_entry_count": len(runtime_state.fix_log),
                "rework_attempt": rework_attempt,
            }
            runtime_state.repair_history.append(repair_payload)
            graph_state["repair_accepted"] = False
            graph_state["repair_patch"] = {
                "selected_feedback": selected_trace,
                "repair_stage_ids": list(aggregate_stage_ids),
                "fix_request_batch": _jsonable(active_request_batch),
                "sl9_decision": _jsonable(sl9_decision),
                "local_check_evidence": _jsonable(local_check_evidence),
                "sl10_repair_review": _jsonable(sl10_output),
                "grounding_update_hints": _jsonable(sl10_grounding_hints),
                "repair_review": _jsonable(repair_review),
                "accepted_candidate": False,
                "accepted_noop_override": True,
                "waiver_continue": True,
                "waiver_audit": _jsonable(noop_override_waiver_audit),
                "fix_log_entry_count": len(runtime_state.fix_log),
                "rework_attempts_used": rework_attempt + 1,
                "exit_reason": "sl10_noop_override_waiver_continue",
                "retryable_repair_rejection": False,
            }
            return Command(goto="repair_finalize", update=graph_state)
        if accepted:
            return Command(goto="repair_sc11_accept_candidate", update=graph_state)
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl10_review" if rework_attempt == 0 else "sl10_rework_review",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            local_check_evidence=local_check_evidence,
            sl10_review=sl10_output,
            repair_memory=repair_memory,
            next_action="sl9_rework" if rework_attempt + 1 < max_rework_attempts else "exit_rejected_rework_budget_exhausted",
            notes=[
                *sl10_output.rework_instructions,
                *(
                    f"repair_memory:{item.get('kind') or item}" if isinstance(item, dict) else f"repair_memory:{item}"
                    for item in repair_memory.get("actionable_rework_guidance", [])
                    if item
                ),
                *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
            ],
        )
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review_input_summary": repair_review_input_summary,
            "local_check_evidence": _jsonable(local_check_evidence),
            "sd10_repair_review": local_sd10_repair_review,
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted": False,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempt": rework_attempt,
        }
        runtime_state.repair_history.append(repair_payload)
        graph_state["repair_last_repair_review"] = repair_review
        graph_state["repair_last_sl10_output"] = sl10_output
        graph_state["repair_last_iteration_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "local_check_evidence": _jsonable(local_check_evidence),
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": False,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempts_used": rework_attempt + 1,
        }
        runtime_state.pending_repair_rejection = None
        runtime_state.pending_original_fix_plan = None
        runtime_state.pending_rework_request = _jsonable(sl10_output)
        if rework_attempt + 1 < max_rework_attempts:
            graph_state["repair_rework_attempt"] = rework_attempt + 1
            return Command(goto="repair_sl9_repair", update=graph_state)
        last_patch = dict(graph_state.get("repair_last_iteration_patch") or {})
        last_patch["exit_reason"] = repair_review.local_rejection.reason if repair_review.local_rejection is not None else "sl10 repair review requested rework"
        last_patch["retryable_repair_rejection"] = False
        last_patch["next_iteration_repair_plan"] = "<none:sl10_rework_budget_exhausted>"
        graph_state["repair_accepted"] = False
        graph_state["repair_patch"] = last_patch
        return Command(goto="repair_finalize", update=graph_state)

    def repair_sc11_accept_candidate(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        validation: _ValidationPass = graph_state["repair_validation"]
        selected_trace = dict(graph_state.get("repair_selected_trace") or {})
        effective_fix_plan = graph_state["repair_effective_fix_plan"]
        active_request_batch = graph_state["repair_active_request_batch"]
        sl9_decision = graph_state["repair_sl9_decision"]
        candidate_dsl = str(graph_state.get("repair_candidate_dsl") or "")
        aggregate_stage_ids = list(graph_state.get("repair_aggregate_stage_ids") or [])
        rework_attempt = int(graph_state.get("repair_rework_attempt", 0))
        local_check_evidence = dict(graph_state.get("repair_local_check_evidence") or {})
        local_sd10_repair_review = graph_state.get("repair_local_sd10_repair_review")
        repair_review_input_summary = dict(graph_state.get("repair_review_input_summary") or {})
        sl10_output = graph_state["repair_sl10_output"]
        repair_review = graph_state["repair_repair_review"]
        repair_memory = dict(graph_state.get("repair_memory") or {})
        sl10_grounding_hints = list(graph_state.get("repair_grounding_update_hints") or [])
        _trace_node(
            graph_state,
            "repair_sc11_accept_candidate",
            iteration=iteration,
            rework_attempt=rework_attempt,
            candidate_dsl_hash=_hash_text(candidate_dsl),
        )
        sc11_meta = _meta(StageId.SC_11_ACCEPT_CANDIDATE, ok=True)
        _append_stage(runtime_state.stage_records, sc11_meta)
        aggregate_stage_ids.append(sc11_meta.stage_id)
        _append_flow_log(
            runtime_state.logs,
            event="stage_result",
            stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
            iteration=iteration,
            ok=True,
            reason="SL-10 accepted candidate; next iteration must restart at SD-2",
            old_dsl_hash=_hash_text(runtime_state.current_dsl),
            candidate_dsl_hash=_hash_text(candidate_dsl),
            jump="SD-2 next iteration",
            candidate_dsl=candidate_dsl,
            graph_subgraph="repair_subgraph",
            graph_node="repair_sc11_accept_candidate",
        )
        _fix_log_entry(
            state=runtime_state,
            iteration=iteration,
            phase="sl10_review" if rework_attempt == 0 else "sl10_rework_review",
            batch=active_request_batch,
            decisions=sl9_decision.decisions,
            old_dsl=runtime_state.current_dsl,
            candidate_dsl=candidate_dsl,
            diff_summary=sl9_decision.diff_summary,
            local_check_evidence=local_check_evidence,
            sl10_review=sl10_output,
            repair_memory=repair_memory,
            next_action="sc11_accept_then_sd2",
            notes=[
                *sl10_output.rework_instructions,
                *(
                    f"repair_memory:{item.get('kind') or item}" if isinstance(item, dict) else f"repair_memory:{item}"
                    for item in repair_memory.get("actionable_rework_guidance", [])
                    if item
                ),
                *(f"grounding_update_hint:{item['hint_hash']}" for item in sl10_grounding_hints),
            ],
        )
        repair_payload = {
            "iteration": iteration,
            "selected_feedback": selected_trace,
            "plan_kind": active_request_batch.legacy_plan_kind,
            "fix_plan": _jsonable(effective_fix_plan),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "candidate_dsl": candidate_dsl,
            "candidate_dsl_hash": _hash_text(candidate_dsl),
            "repair_review_input_summary": repair_review_input_summary,
            "local_check_evidence": _jsonable(local_check_evidence),
            "sd10_repair_review": local_sd10_repair_review,
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted": True,
            "repair_stage_ids": list(aggregate_stage_ids),
            "scenario_set_id": validation.scenario_set.scenario_set_id if validation.scenario_set is not None else None,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempt": rework_attempt,
        }
        runtime_state.repair_history.append(repair_payload)
        runtime_state.current_dsl = candidate_dsl
        runtime_state.pending_repair_rejection = None
        runtime_state.pending_original_fix_plan = None
        runtime_state.pending_rework_request = None
        graph_state["repair_aggregate_stage_ids"] = aggregate_stage_ids
        graph_state["repair_accepted"] = True
        graph_state["repair_patch"] = {
            "selected_feedback": selected_trace,
            "repair_stage_ids": list(aggregate_stage_ids),
            "fix_request_batch": _jsonable(active_request_batch),
            "sl9_decision": _jsonable(sl9_decision),
            "local_check_evidence": _jsonable(local_check_evidence),
            "sl10_repair_review": _jsonable(sl10_output),
            "grounding_update_hints": _jsonable(sl10_grounding_hints),
            "repair_review": _jsonable(repair_review),
            "accepted_candidate": True,
            "fix_log_entry_count": len(runtime_state.fix_log),
            "rework_attempts_used": rework_attempt + 1,
            "exit_reason": "candidate_accepted_for_next_full_pass",
        }
        return Command(goto="repair_finalize", update=graph_state)

    def repair_finalize(graph_state: _RepairSubgraphState) -> Command:
        graph_state = _state(graph_state)
        runtime_state = _runtime_state(graph_state)
        iteration = _iteration(graph_state)
        _trace_node(
            graph_state,
            "repair_finalize",
            event="subgraph_exit",
            iteration=iteration,
            accepted=bool(graph_state.get("repair_accepted")),
            repair_stage_ids=list(graph_state.get("repair_patch", {}).get("repair_stage_ids", [])) if isinstance(graph_state.get("repair_patch"), dict) else [],
        )
        if "repair_patch" not in graph_state:
            raise RuntimeError(
                "repair subgraph contract violation: repair_finalize requires an explicit repair_patch; "
                "each SD-8/SL-9/SL-10/SC-11 exit branch must record accept/reject/waiver evidence before finalizing"
            )
        return Command(goto=END, update=graph_state)

    graph.add_node("repair_enter", repair_enter)
    graph.add_node("repair_sd8_fix_requests", repair_sd8_fix_requests)
    graph.add_node("repair_sl9_repair", repair_sl9_repair)
    graph.add_node("repair_sl10_review", repair_sl10_review)
    graph.add_node("repair_sc11_accept_candidate", repair_sc11_accept_candidate)
    graph.add_node("repair_finalize", repair_finalize)
    graph.add_edge(START, "repair_enter")
    # The parent graph already owns the run-level checkpoint.  The repair
    # subgraph intentionally carries live _RunState / feedback / adapter
    # objects so that SD-8/SL-9/SL-10/SC-11 can update the canonical evidence
    # ledger in place.  Giving this nested graph its own pickle-backed
    # checkpointer would try to serialize pyfcstm/runtime objects on every
    # waiver/rework boundary and can fail with weakref objects in real runs.
    # Stage-level visibility is preserved through explicit _trace_node events,
    # flow logs, fix_log, repair_history and the parent graph checkpoint.
    return graph.compile(checkpointer=False)

def _build_graph(
    *,
    runtime_cfg: FullStagedRuntimeConfig,
    adapters: FullStagedRuntimeAdapters,
    checkpointer: Any | None = None,
    store: Any | None = None,
) -> Any:
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

    graph.add_node("sc0_start", sc0_start)
    graph.add_node("sl1_initial_modeling", sl1_initial_modeling)
    graph.add_node("iteration_gate", iteration_gate)
    graph.add_node("validation_pass", validation_pass)
    graph.add_node("validation_decision", validation_decision)
    graph.add_node("repair_path", repair_path)
    graph.add_node("repair_decision", repair_decision)
    graph.add_node("waiver_continue", waiver_continue)
    graph.add_node("sc12_budget_exhausted", sc12_budget_exhausted)
    graph.add_node("sc13_trace_audit", sc13_trace_audit)

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




def _lg_f1_actual_interrupt_node(interrupt_after: str) -> str:
    """Map LG-F1 human/stage breakpoints onto the parent graph checkpoint boundary.

    LG-F1 deliberately supports controlled node-boundary resume on the parent
    graph.  Nested repair/validation subgraphs still run with ``checkpointer=False``
    because they carry live Python objects; therefore a request such as
    ``repair_sl10_review`` is recorded as requested evidence but executed at the
    nearest durable parent checkpoint, ``repair_path``.
    """

    requested = str(interrupt_after or "").strip()
    if requested in {
        "sc0_start",
        "sl1_initial_modeling",
        "iteration_gate",
        "validation_pass",
        "validation_decision",
        "repair_path",
        "repair_decision",
        "waiver_continue",
        "sc12_budget_exhausted",
        "sc13_trace_audit",
    }:
        return requested
    repair_aliases = {
        "SD-8",
        "SD_8",
        StageId.SD_8_FIX_PLAN.value,
        "SL-9",
        "SL_9",
        StageId.SL_9_REPAIR.value,
        "SL-10",
        "SL_10",
        StageId.SL_10_REPAIR_REVIEW.value,
        "SC-11",
        "SC_11",
        StageId.SC_11_ACCEPT_CANDIDATE.value,
        "repair_enter",
        "repair_sd8_fix_requests",
        "repair_sl9_repair",
        "repair_sl10_review",
        "repair_sc11_accept_candidate",
        "repair_finalize",
    }
    if requested in repair_aliases or requested.startswith("repair_"):
        return "repair_path"
    validation_aliases = {
        StageId.SD_2_PARSE.value,
        StageId.SD_3_SEMANTIC.value,
        StageId.SD_4_DESIGN.value,
        StageId.SL_5_SCENARIO_GENERATION.value,
        StageId.SD_5A_SCENARIO_COVERAGE.value,
        StageId.SD_6_SIM.value,
        StageId.SL_7_MODEL_REVIEW.value,
    }
    if requested in validation_aliases or requested.startswith("validation_"):
        return "validation_pass"
    raise ValueError(f"unsupported LG-F1 interrupt_after breakpoint: {interrupt_after!r}")


def _lg_f1_path_hash(path: str | Path) -> str:
    return _hash_text(str(Path(path).expanduser().resolve()))


def _lg_f1_checkpoint_id_hash(checkpoint: Any) -> str:
    config = getattr(checkpoint, "config", {}) or {}
    configurable = config.get("configurable", {}) if isinstance(config, dict) else {}
    checkpoint_id = str(configurable.get("checkpoint_id") or "")
    if not checkpoint_id:
        return "sha256:<missing-checkpoint-id>"
    return _hash_text(checkpoint_id)


def _lg_f1_graph_config(
    *,
    config: LoopConfig,
    registry: dict[str, Any],
    planned: dict[str, Any],
    resolved: dict[str, Any],
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    actual_interrupt_after: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
) -> dict[str, Any]:
    return {
        "registry": registry,
        "planned_stage_graph": planned,
        "resolved_config": resolved,
        "condition_hash": resolved.get("condition_hash"),
        "condition_id": config.condition_id,
        "max_iterations": config.max_iterations,
        "scenario_max_retries": config.scenario_max_retries,
        "min_sl10_rework_attempts": int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        "policy_profile": config.policy_profile,
        "llm_provider_mode": config.llm_provider_mode,
        "runtime_backend": "langgraph_lg_f1_resume_experiment",
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_serde": "pickle",
        "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
        "runtime_schema_version": GRAPH_RUNTIME_SCHEMA_VERSION,
        "node_edge_schema_version": NODE_EDGE_SCHEMA_VERSION,
        "lg_d1_operator_stream_enabled": bool(operator_stream_enabled),
        "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
        "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
        "lg_f1_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "lg_f1_requested_interrupt_after": requested_interrupt_after,
        "lg_f1_actual_interrupt_after": actual_interrupt_after,
        "lg_f1_scope": "controlled_parent_node_boundary_resume",
    }


def _lg_f1_runtime_config(
    *,
    nl: str,
    config: LoopConfig,
    planned: dict[str, Any],
    resolved: dict[str, Any],
    registry: dict[str, Any],
    consistency: dict[str, Any],
    compat: dict[str, Any],
    graph_config_hash: str,
    initial_dsl: str,
    run_id: str,
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    actual_interrupt_after: str,
    resumed_from_checkpoint: bool,
    resume_checkpoint_id_hash: str | None = None,
    resume_diff_report_path: str | None = None,
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
) -> FullStagedRuntimeConfig:
    checkpoint_metadata = {
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_serde": "pickle",
        "checkpoint_serde_mode": _LG_C1_CHECKPOINT_SERDE_MODE,
        "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
        "checkpoint_backend_status": "enabled",
        "checkpoint_path": str(checkpoint_path),
        "resumed_from_checkpoint": bool(resumed_from_checkpoint),
        "resume_checkpoint_id_hash": resume_checkpoint_id_hash,
        "real_agent_loop_resume_supported": True,
        "real_agent_loop_resume_support_level": "controlled_parent_node_boundary_only",
        "real_agent_loop_resume_scope": "controlled_parent_node_boundary_resume; nested subgraphs are not mid-node crash checkpoints",
        "real_agent_loop_arbitrary_mid_node_resume_supported": False,
        "real_agent_loop_nested_subgraph_resume_supported": False,
        "real_agent_loop_json_checkpoint_supported": False,
        "resume_run_main_result_eligible": False,
        "resume_cli_entrypoint": "python -m project_1_llm_state_machine_modeling.method.experiments.checkpoint_resume",
        "resume_cli_workdir": "repo_root",
        "resume_cli_requires_pythonpath": False,
        "resume_cli_pythonpath_entrypoint": "PYTHONPATH=project_1_llm_state_machine_modeling python -m method.experiments.checkpoint_resume",
        "resume_cli_legacy_entrypoint": "PYTHONPATH=project_1_llm_state_machine_modeling python -m method.pr_lg_f1_resume_experiment",
        "resume_cli_legacy_package_entrypoint": "python -m project_1_llm_state_machine_modeling.method.pr_lg_f1_resume_experiment",
        "resume_diff_report_path": resume_diff_report_path,
        "resume_diff_report_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "lg_f1_requested_interrupt_after": requested_interrupt_after,
        "lg_f1_actual_interrupt_after": actual_interrupt_after,
        "lg_f1_mid_node_crash_supported": False,
        "lg_f1_transient_store_durable": False,
        "lg_f1_scope_note": (
            "SQLite persists the parent LangGraph checkpoint.  LG-F1 does not claim "
            "arbitrary mid-node crash recovery because nested subgraphs and transient "
            "Store objects are still live-object boundaries."
        ),
    }
    metadata = _graph_runtime_metadata(
        registry=registry,
        compat=compat,
        graph_config_hash=graph_config_hash,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        checkpoint_metadata=checkpoint_metadata,
    )
    initial_lg_d1_stream_metadata = lg_d1_llm_stream_runtime_metadata(real_llm_provider_api=config.llm_provider_mode == "real_env")
    return FullStagedRuntimeConfig(
        initial_dsl=initial_dsl,
        run_id=run_id,
        output_dir=config.output_dir,
        max_iterations=config.max_iterations,
        scenario_max_retries=config.scenario_max_retries,
        min_sl10_rework_attempts=int(config.budget_policy.get("min_sl10_rework_attempts", 1)) if isinstance(config.budget_policy, dict) else 1,
        policy_profile=config.policy_profile,
        write_run_record=config.write_run_record,
        adapter_mode=config.llm_provider_mode,
        # LG-F1 resume runs are evidence-only and must never become Path1/Path2 main results.
        allow_main_result_eligible=False,
        resolved_loop_config=resolved,
        run_config_extra={
            "runtime_implementation": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "langgraph_called_from_loop": False,
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
            "llm_stream_required": initial_lg_d1_stream_metadata["llm_stream_required"],
            "stage_semantics_module": "method.staged_runtime",
            "lg_f1_resume_experiment": True,
            "resume_run_main_result_eligible": False,
            "resumed_from_checkpoint": bool(resumed_from_checkpoint),
            "resume_checkpoint_id_hash": resume_checkpoint_id_hash,
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": _lg_f1_path_hash(checkpoint_path),
            "resume_diff_report_path": resume_diff_report_path,
            "resume_diff_report_schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        },
        environment_extra={
            **metadata,
            "runner": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "stage_semantics_module": "method.staged_runtime",
            "loop_entrypoint": "method.langgraph_runtime.run_lg_f1_resume_experiment",
            "record_schema_version": "pr-c.default-full-staged-runtime.v1",
            "lg_d1_operator_log_enabled": bool(operator_stream_enabled),
            "lg_d1_instrumentation_layer": LG_D1_INSTRUMENTATION_LAYER,
            "lg_e3_toolnode_wrappers_enabled": bool(toolnode_wrapper_enabled),
            "lg_e3_toolnode_wrapper_schema_version": LG_E3_TOOLNODE_WRAPPER_SCHEMA_VERSION,
            "lg_e3_toolnode_wrapper_registry_hash": _hash_payload(build_lg_e3_toolnode_wrapper_registry()),
            "lg_e3_toolnode_wrapper_llm_tool_choice_exposed": False,
            **initial_lg_d1_stream_metadata,
        },
        real_llm_provider_api=config.llm_provider_mode == "real_env",
        provider_config_read=_provider_config_read(config),
        provider_model_redacted=_provider_model_redacted(config, provider),
        default_loop_config_entry_integrated=False,
    )


def _lg_f1_prepare_runtime(
    *,
    config: LoopConfig,
    checkpoint_path: str | Path,
    requested_interrupt_after: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], str, str]:
    config.validate_for_run()
    registry = build_langgraph_node_registry()
    planned = _planned_stage_graph_from_config(config)
    consistency = graph_registry_consistency(planned, registry)
    if not consistency["ok"]:
        raise ValueError(f"LangGraph registry does not cover planned stage graph: {consistency}")
    compat = langgraph_compat_smoke()
    if not compat.get("ok"):
        raise RuntimeError(f"LangGraph compatibility smoke failed: {compat}")
    resolved = config.resolved_config()
    actual_interrupt_after = _lg_f1_actual_interrupt_node(requested_interrupt_after)
    graph_config = _lg_f1_graph_config(
        config=config,
        registry=registry,
        planned=planned,
        resolved=resolved,
        checkpoint_path=checkpoint_path,
        requested_interrupt_after=requested_interrupt_after,
        actual_interrupt_after=actual_interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    return registry, planned, consistency, compat, resolved, _hash_payload(graph_config), actual_interrupt_after


def _lg_f1_sqlite_saver(checkpoint_path: str | Path) -> tuple[Any, sqlite3.Connection]:
    try:
        from langgraph.checkpoint.sqlite import SqliteSaver
    except Exception as exc:  # pragma: no cover - depends on optional package installation.
        raise RuntimeError(
            "LG-F1 durable resume requires langgraph-checkpoint-sqlite; "
            "install langgraph-checkpoint-sqlite and do not silently fall back to memory"
        ) from exc

    path = Path(checkpoint_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(path), check_same_thread=False)
    saver = SqliteSaver(conn, serde=_PickleCheckpointSerde())
    saver.setup()
    return saver, conn


def _lg_f1_state_snapshot(state: dict[str, Any] | None) -> dict[str, Any]:
    state = dict(state or {})
    runtime_state = state.get("runtime_state")
    if isinstance(runtime_state, _RunState):
        return {
            "stage_records": _jsonable(runtime_state.stage_records),
            "stage_ids": _stage_ids(runtime_state.stage_records),
            "fix_log": _jsonable(runtime_state.fix_log),
            "llm_interactions": _jsonable(runtime_state.llm_interactions),
            "scenario_history": _jsonable(runtime_state.scenario_history),
            "repair_history": _jsonable(runtime_state.repair_history),
            "final_dsl_hash": _hash_text(runtime_state.current_dsl),
            "verdict": runtime_state.final_verdict,
            "result_status": runtime_state.result_status,
        }
    return {
        "stage_records": [],
        "stage_ids": [],
        "fix_log": [],
        "llm_interactions": [],
        "scenario_history": [],
        "repair_history": [],
        "final_dsl_hash": None,
        "verdict": None,
        "result_status": None,
    }


def _lg_f1_record_snapshot(record: Any) -> dict[str, Any]:
    return {
        "stage_records": _jsonable(record.stage_records),
        "stage_ids": [str(item.get("stage_id") if isinstance(item, dict) else getattr(item, "stage_id", "")) for item in record.stage_records],
        "fix_log": _jsonable(record.fix_log),
        "llm_interactions": _jsonable(record.llm_interactions),
        "scenario_history": _jsonable(record.scenario_history),
        "repair_history": _jsonable(record.repair_history),
        "final_dsl_hash": record.final_artifacts.get("final_dsl_hash"),
        "verdict": record.final_artifacts.get("verdict"),
        "result_status": record.final_artifacts.get("agent_loop_result_status"),
    }


def _lg_f1_prefix_preserved(prefix: list[Any], full: list[Any]) -> bool:
    return list(full[: len(prefix)]) == list(prefix)


def _lg_f1_append_only_audit(prefix: dict[str, Any], resumed: dict[str, Any]) -> dict[str, Any]:
    fix_log = list(resumed.get("fix_log") or [])
    fix_ids = [
        str(item.get("entry_id") or item.get("fix_log_entry_id") or item.get("candidate_dsl_hash") or _hash_payload(item))
        for item in fix_log
        if isinstance(item, dict)
    ]
    return {
        "stage_records_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("stage_records") or [], resumed.get("stage_records") or []),
        "fix_log_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("fix_log") or [], resumed.get("fix_log") or []),
        "llm_interactions_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("llm_interactions") or [], resumed.get("llm_interactions") or []),
        "scenario_history_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("scenario_history") or [], resumed.get("scenario_history") or []),
        "repair_history_prefix_preserved": _lg_f1_prefix_preserved(prefix.get("repair_history") or [], resumed.get("repair_history") or []),
        "duplicate_fix_log_entry_detected": len(fix_ids) != len(set(fix_ids)),
    }


def _lg_f1_stage_replay_audit(
    *,
    prefix: dict[str, Any],
    resumed: dict[str, Any],
    actual_interrupt_after: str,
    next_nodes_after_interrupt: list[str],
) -> dict[str, Any]:
    """Explain repeated stage ids after resume instead of treating all repeats as replay bugs.

    LG-F1 may intentionally resume at a parent boundary after the repair
    subgraph has produced SD-8/SL-9/SL-10/SC-11 evidence.  The next parent node
    is then ``repair_decision`` which routes to a full post-repair validation
    pass.  That means resumed records are expected to contain a prefix ending
    at SC-11 followed by SD-2/SD-3/.../SC-13.  This helper makes that route
    machine-readable so reviewers can distinguish expected post-repair
    revalidation from accidental replay / duplicate ledger pollution.
    """

    prefix_ids = [str(item) for item in (prefix.get("stage_ids") or [])]
    resumed_ids = [str(item) for item in (resumed.get("stage_ids") or [])]
    prefix_preserved = _lg_f1_prefix_preserved(prefix_ids, resumed_ids)
    suffix = resumed_ids[len(prefix_ids) :] if prefix_preserved else resumed_ids
    repeated_after_resume = [stage_id for stage_id in suffix if stage_id in set(prefix_ids)]
    post_repair_full_revalidation_expected = (
        bool(prefix_preserved)
        and actual_interrupt_after == "repair_path"
        and "repair_decision" in set(next_nodes_after_interrupt)
        and suffix[:3] == ["SD-2", "SD-3", "SD-4"]
    )
    unexpected_stage_replay_detected = bool(repeated_after_resume) and not post_repair_full_revalidation_expected
    explanation = (
        "Expected: interrupt_after mapped to parent node repair_path; after resume the pending repair_decision "
        "routes into a full post-repair validation pass, so SD-2/SD-3/... appear after the preserved repair prefix."
        if post_repair_full_revalidation_expected
        else (
            "No repeated stage ids after the preserved prefix."
            if not repeated_after_resume
            else "Repeated stage ids after resume are not explained by a known LG-F1 parent-boundary route."
        )
    )
    return {
        "schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "prefix_stage_ids": prefix_ids,
        "resumed_stage_ids": resumed_ids,
        "suffix_after_resume": suffix,
        "repeated_stage_ids_after_resume": repeated_after_resume,
        "prefix_preserved": prefix_preserved,
        "post_repair_full_revalidation_expected": post_repair_full_revalidation_expected,
        "unexpected_stage_replay_detected": unexpected_stage_replay_detected,
        "actual_interrupt_after": actual_interrupt_after,
        "next_nodes_after_interrupt": list(next_nodes_after_interrupt),
        "explanation": explanation,
    }


def _lg_f1_compare_hash(value: Any) -> str:
    """Hash a comparison payload after dropping known run-local bookkeeping."""

    def scrub(item: Any) -> Any:
        if isinstance(item, dict):
            cleaned: dict[str, Any] = {}
            for key, value in item.items():
                key_s = str(key)
                lowered = key_s.lower()
                if any(fragment in lowered for fragment in ("run_id", "timestamp", "created_at", "updated_at", "path", "checkpoint_id")):
                    cleaned[key_s] = "<allowed-run-local-diff>"
                else:
                    cleaned[key_s] = scrub(value)
            return cleaned
        if isinstance(item, list):
            return [scrub(value) for value in item]
        return item

    return _hash_payload(scrub(value))


def _lg_f1_comparison_checks(
    prefix: dict[str, Any],
    resumed: dict[str, Any],
    uninterrupted: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    baseline_available = uninterrupted is not None
    comparison_basis = "independent_uninterrupted_baseline" if baseline_available else "no_independent_baseline"
    comparison_method = "independent_uninterrupted_baseline" if baseline_available else "not_available"
    comparison_target = "uninterrupted_vs_resumed" if baseline_available else "baseline_unavailable"
    for field in ("stage_ids", "fix_log", "llm_interactions", "scenario_history", "repair_history", "final_dsl_hash", "verdict", "result_status"):
        prefix_value = prefix.get(field)
        resumed_value = resumed.get(field)
        resumed_hash = _lg_f1_compare_hash(resumed_value)
        uninterrupted_hash = _lg_f1_compare_hash(uninterrupted.get(field)) if baseline_available else None
        verdict = (
            "consistent"
            if baseline_available and uninterrupted_hash == resumed_hash
            else ("unacceptable_diff" if baseline_available else "not_applicable")
        )
        note = (
            "LG-F1 compares an independent uninterrupted baseline against the resumed final evidence; "
            "prefix hash is recorded separately for append-only resume auditing."
            if baseline_available
            else (
                "No independent uninterrupted baseline was provided; this check only records resumed/prefix hashes "
                "and must not be cited as independent baseline equivalence."
            )
        )
        checks.append(
            {
                "field": field,
                "uninterrupted_value_hash": uninterrupted_hash,
                "resumed_value_hash": resumed_hash,
                "prefix_value_hash": _lg_f1_compare_hash(prefix_value),
                "verdict": verdict,
                "comparison_method": comparison_method,
                "comparison_basis": comparison_basis,
                "comparison_target": comparison_target,
                "baseline_available": baseline_available,
                "uninterrupted_baseline_available": baseline_available,
                "note": note,
            }
        )
    return checks


def _lg_f1_finalize_result(
    *,
    result: AgentLoopResult,
    state: _GraphLoopState,
    operator_events: list[dict[str, Any]],
    graph_stream_status: str,
    operator_stream_enabled: bool,
    toolnode_wrapper_enabled: bool,
    resolved: dict[str, Any],
    planned: dict[str, Any],
) -> None:
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
        enabled=True,
    )
    operator_events = _merge_operator_events(operator_events, state.get("operator_events"))
    _augment_run_record_with_lg_d1_operator_log(
        result,
        operator_events=operator_events,
        graph_stream_status=graph_stream_status,
        operator_stream_enabled=bool(operator_stream_enabled),
    )
    _refresh_lg_c1_readiness_after_lg_d1_operator_log(result, state)
    result.resolved_config = resolved
    result.planned_stage_graph = planned


def _lg_f1_patch_record_with_report(record_path: str | Path, report: dict[str, Any]) -> None:
    record = read_agent_loop_run_record(record_path)
    record.environment.update(
        {
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": report["checkpoint_path_hash"],
            "resumed_from_checkpoint": True,
            "resume_checkpoint_id_hash": report["resume"]["checkpoint_id_hash"],
            "real_agent_loop_resume_supported": True,
            "real_agent_loop_resume_support_level": report["real_agent_loop_resume_support_level"],
            "real_agent_loop_resume_scope": report["real_agent_loop_resume_scope"],
            "real_agent_loop_arbitrary_mid_node_resume_supported": False,
            "real_agent_loop_nested_subgraph_resume_supported": False,
            "resume_run_main_result_eligible": False,
            "resume_diff_report_path": report["resume_diff_report_path"],
            "resume_diff_report_schema_version": report["schema_version"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "baseline_comparison_note": report["baseline_comparison_note"],
            "verdict_scope": report["verdict_scope"],
            "lg_f1_mid_node_crash_supported": False,
            "lg_f1_stage_replay_explanation": report["stage_replay_audit"]["explanation"],
        }
    )
    record.run_config.update(
        {
            "lg_f1_resume_experiment": True,
            "checkpoint_backend": "sqlite",
            "checkpoint_backend_type": "SqliteSaver",
            "checkpoint_path_hash": report["checkpoint_path_hash"],
            "resumed_from_checkpoint": True,
            "resume_checkpoint_id_hash": report["resume"]["checkpoint_id_hash"],
            "resume_run_main_result_eligible": False,
            "resume_diff_report_path": report["resume_diff_report_path"],
            "resume_diff_report_schema_version": report["schema_version"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "verdict_scope": report["verdict_scope"],
        }
    )
    record.final_artifacts["main_result_eligible"] = False
    record.final_artifacts["main_result_eligibility_reason"] = "LG-F1 resume run is evidence-only; resume artifacts are excluded from main-result statistics"
    record.final_artifacts["resume_run_main_result_eligible"] = False
    record.final_artifacts["resume_diff_report_path"] = report["resume_diff_report_path"]
    record.final_artifacts["lg_f1_resume_verdict"] = report["verdict"]
    record.final_artifacts["lg_f1_baseline_comparison_method"] = report["baseline_comparison_method"]
    record.final_artifacts["lg_f1_baseline_comparison_verdict"] = report["baseline_comparison_verdict"]
    record.final_artifacts["lg_f1_verdict_scope"] = report["verdict_scope"]
    record.logs.append(
        {
            "event": "lg_f1_resume_reconciliation",
            "schema_version": report["schema_version"],
            "resume_diff_report_path": report["resume_diff_report_path"],
            "verdict": report["verdict"],
            "baseline_comparison_method": report["baseline_comparison_method"],
            "baseline_comparison_verdict": report["baseline_comparison_verdict"],
            "verdict_scope": report["verdict_scope"],
            "main_result_eligible": False,
        }
    )
    write_agent_loop_run_record(record, record_path)


def resume_lg_f1_from_checkpoint(
    *,
    checkpoint_path: str | Path,
    thread_id: str,
    expected_graph_config_hash: str,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    nl: str = "LG-F1 resume from durable checkpoint.",
    initial_dsl: str = "",
    interrupt_after: str = "repair_path",
    checkpoint_id_hash: str | None = None,
    resume_diff_report_path: str | None = None,
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
) -> dict[str, Any]:
    """Resume a controlled LG-F1 parent-graph checkpoint and fail loud on mismatch."""

    path = Path(checkpoint_path)
    if not path.exists():
        raise FileNotFoundError(f"LG-F1 checkpoint missing: {path}")
    registry, planned, consistency, compat, resolved, graph_config_hash, actual_interrupt_after = _lg_f1_prepare_runtime(
        config=config,
        checkpoint_path=path,
        requested_interrupt_after=interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    if expected_graph_config_hash and expected_graph_config_hash != graph_config_hash:
        raise ValueError(
            f"LG-F1 graph_config_hash mismatch: expected {expected_graph_config_hash}, actual {graph_config_hash}; "
            "refusing to resume from an incompatible checkpoint"
        )
    saver, conn = _lg_f1_sqlite_saver(path)
    try:
        runtime_cfg = _lg_f1_runtime_config(
            nl=nl,
            config=config,
            planned=planned,
            resolved=resolved,
            registry=registry,
            consistency=consistency,
            compat=compat,
            graph_config_hash=graph_config_hash,
            initial_dsl=initial_dsl,
            run_id=thread_id,
            checkpoint_path=path,
            requested_interrupt_after=interrupt_after,
            actual_interrupt_after=actual_interrupt_after,
            resumed_from_checkpoint=True,
            resume_checkpoint_id_hash=checkpoint_id_hash,
            resume_diff_report_path=resume_diff_report_path,
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            provider=provider,
        )
        app = _build_graph(runtime_cfg=runtime_cfg, adapters=adapters, checkpointer=saver)
        checkpoint = app.get_state({"configurable": {"thread_id": thread_id}})
        if checkpoint is None or not getattr(checkpoint, "values", None):
            raise RuntimeError(f"LG-F1 checkpoint not found for thread_id={thread_id!r}; refusing to rerun from scratch")
        if not getattr(checkpoint, "next", None):
            raise RuntimeError(f"LG-F1 checkpoint for thread_id={thread_id!r} has no pending next node; refusing ambiguous resume")
        actual_checkpoint_hash = _lg_f1_checkpoint_id_hash(checkpoint)
        if checkpoint_id_hash and checkpoint_id_hash != actual_checkpoint_hash:
            raise ValueError(
                f"LG-F1 checkpoint id mismatch for thread_id={thread_id!r}: expected {checkpoint_id_hash}, actual {actual_checkpoint_hash}"
            )
        state = app.invoke(None, config=checkpoint.config)
        if not isinstance(state, dict) or "runtime_result" not in state:
            raise RuntimeError("LG-F1 resume did not reach SC-13 runtime_result; refusing to report success")
        result = state.get("runtime_result")
        if not isinstance(result, AgentLoopResult):
            raise TypeError("LG-F1 resumed graph did not return an AgentLoopResult")
        _lg_f1_finalize_result(
            result=result,
            state=state,
            operator_events=[],
            graph_stream_status="disabled",
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            resolved=resolved,
            planned=planned,
        )
        return {
            "state": state,
            "result": result,
            "record_path": result.run_record_path,
            "checkpoint_id_hash": actual_checkpoint_hash,
            "graph_config_hash": graph_config_hash,
        }
    finally:
        conn.close()


def run_lg_f1_resume_experiment(
    nl: str,
    *,
    config: LoopConfig,
    adapters: FullStagedRuntimeAdapters,
    initial_dsl: str = "",
    checkpoint_path: str | Path,
    interrupt_after: str = "repair_path",
    operator_stream_enabled: bool = False,
    toolnode_wrapper_enabled: bool = True,
    provider: ChatProvider | None = None,
    uninterrupted_adapters: FullStagedRuntimeAdapters | None = None,
    uninterrupted_provider: ChatProvider | None = None,
) -> dict[str, Any]:
    """Run a deterministic LG-F1 durable checkpoint/resume reconciliation experiment.

    The helper is intentionally evidence-only: it writes ``resume_diff_report.json``
    and patches the resumed run record so ``main_result_eligible`` remains false.
    """

    path = Path(checkpoint_path)
    run_id = config.run_id or f"lg-f1-{hashlib.sha256(nl.encode('utf-8')).hexdigest()[:12]}"
    uninterrupted_snapshot: dict[str, Any] | None = None
    uninterrupted_record_path: str | None = None
    uninterrupted_run_id = f"{run_id}-uninterrupted"
    if uninterrupted_adapters is not None:
        baseline_cfg = replace(config, run_id=uninterrupted_run_id)
        baseline_result = run_full_staged_langgraph_runtime(
            nl,
            config=baseline_cfg,
            adapters=uninterrupted_adapters,
            initial_dsl=initial_dsl,
            run_id=uninterrupted_run_id,
            provider=uninterrupted_provider if uninterrupted_provider is not None else provider,
            called_from_loop=False,
            operator_stream_enabled=bool(operator_stream_enabled),
            toolnode_wrapper_enabled=bool(toolnode_wrapper_enabled),
        )
        if not baseline_result.run_record_path:
            raise RuntimeError("LG-F1 uninterrupted baseline did not write an AgentLoopRunRecord")
        uninterrupted_record_path = str(baseline_result.run_record_path)
        uninterrupted_snapshot = _lg_f1_record_snapshot(read_agent_loop_run_record(baseline_result.run_record_path))
    registry, planned, consistency, compat, resolved, graph_config_hash, actual_interrupt_after = _lg_f1_prepare_runtime(
        config=config,
        checkpoint_path=path,
        requested_interrupt_after=interrupt_after,
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
    )
    report_path = path.parent / "resume_diff_report.json"
    saver, conn = _lg_f1_sqlite_saver(path)
    try:
        runtime_cfg = _lg_f1_runtime_config(
            nl=nl,
            config=config,
            planned=planned,
            resolved=resolved,
            registry=registry,
            consistency=consistency,
            compat=compat,
            graph_config_hash=graph_config_hash,
            initial_dsl=initial_dsl,
            run_id=run_id,
            checkpoint_path=path,
            requested_interrupt_after=interrupt_after,
            actual_interrupt_after=actual_interrupt_after,
            resumed_from_checkpoint=False,
            resume_checkpoint_id_hash=None,
            resume_diff_report_path=str(report_path),
            operator_stream_enabled=operator_stream_enabled,
            toolnode_wrapper_enabled=toolnode_wrapper_enabled,
            provider=provider,
        )
        app = _build_graph(runtime_cfg=runtime_cfg, adapters=adapters, checkpointer=saver)
        initial_state: _GraphLoopState = {
            "nl": nl,
            "graph_trace": [],
            "operator_events": [],
            "operator_stream_enabled": bool(operator_stream_enabled),
            "toolnode_wrapper_events": [],
            "stage_record_events": [],
            "llm_interaction_events": [],
            "fix_log_events": [],
            "scenario_history_events": [],
            "repair_history_events": [],
            "toolnode_wrapper_enabled": bool(toolnode_wrapper_enabled),
            "run_id": run_id,
        }
        prefix_state = app.invoke(
            initial_state,
            config={"configurable": {"thread_id": run_id}},
            interrupt_after=[actual_interrupt_after],
        )
        checkpoint = app.get_state({"configurable": {"thread_id": run_id}})
        if checkpoint is None or not getattr(checkpoint, "values", None) or not getattr(checkpoint, "next", None):
            raise RuntimeError(
                f"LG-F1 interrupt_after={actual_interrupt_after!r} did not leave a resumable checkpoint; "
                "refusing to report durable resume success"
            )
        checkpoint_id_hash = _lg_f1_checkpoint_id_hash(checkpoint)
        prefix_snapshot = _lg_f1_state_snapshot(prefix_state if isinstance(prefix_state, dict) else getattr(checkpoint, "values", {}))
    finally:
        conn.close()

    resumed = resume_lg_f1_from_checkpoint(
        checkpoint_path=path,
        thread_id=run_id,
        expected_graph_config_hash=graph_config_hash,
        config=config,
        adapters=adapters,
        nl=nl,
        initial_dsl=initial_dsl,
        interrupt_after=interrupt_after,
        checkpoint_id_hash=checkpoint_id_hash,
        resume_diff_report_path=str(report_path),
        operator_stream_enabled=operator_stream_enabled,
        toolnode_wrapper_enabled=toolnode_wrapper_enabled,
        provider=provider,
    )
    record_path = resumed["record_path"]
    if not record_path:
        raise RuntimeError("LG-F1 resumed run did not write an AgentLoopRunRecord")
    record = read_agent_loop_run_record(record_path)
    resumed_snapshot = _lg_f1_record_snapshot(record)
    next_nodes_after_interrupt = list(getattr(checkpoint, "next", ()) or [])
    append_only_audit = _lg_f1_append_only_audit(prefix_snapshot, resumed_snapshot)
    stage_replay_audit = _lg_f1_stage_replay_audit(
        prefix=prefix_snapshot,
        resumed=resumed_snapshot,
        actual_interrupt_after=actual_interrupt_after,
        next_nodes_after_interrupt=next_nodes_after_interrupt,
    )
    comparison_checks = _lg_f1_comparison_checks(prefix_snapshot, resumed_snapshot, uninterrupted_snapshot)
    uninterrupted_baseline_available = uninterrupted_snapshot is not None
    baseline_comparison_method = (
        "independent_uninterrupted_baseline" if uninterrupted_baseline_available else "not_available"
    )
    baseline_comparison_verdict = (
        "unacceptable_diff"
        if any(item.get("verdict") == "unacceptable_diff" for item in comparison_checks)
        else ("consistent" if uninterrupted_baseline_available else "not_applicable")
    )
    unacceptable = [
        key for key, value in append_only_audit.items() if key != "duplicate_fix_log_entry_detected" and value is not True
    ]
    if append_only_audit["duplicate_fix_log_entry_detected"]:
        unacceptable.append("duplicate_fix_log_entry_detected")
    if stage_replay_audit["unexpected_stage_replay_detected"]:
        unacceptable.append("unexpected_stage_replay_detected")
    unacceptable.extend(
        f"comparison:{item['field']}" for item in comparison_checks if item.get("verdict") == "unacceptable_diff"
    )
    verdict = "consistent" if not unacceptable else "unacceptable_diff"
    report: dict[str, Any] = {
        "schema_version": LG_F1_RESUME_RECONCILIATION_SCHEMA_VERSION,
        "resume_experiment_id": run_id,
        "thread_id": run_id,
        "checkpoint_backend": "sqlite",
        "checkpoint_backend_type": "SqliteSaver",
        "checkpoint_path": str(path),
        "checkpoint_path_hash": _lg_f1_path_hash(path),
        "checkpoint_backend_status": "enabled",
        "graph_config_hash": graph_config_hash,
        "uninterrupted_run_id": uninterrupted_run_id if uninterrupted_baseline_available else None,
        "uninterrupted_run_record_path": uninterrupted_record_path,
        "interrupted_run_id": run_id,
        "resumed_run_id": run_id,
        "artifact_hash_scope": "academic_evidence_snapshot",
        "uninterrupted_artifact_hash": _hash_payload(uninterrupted_snapshot) if uninterrupted_baseline_available else None,
        "resumed_artifact_hash": _hash_payload(resumed_snapshot),
        "interrupt": {
            "requested_after": interrupt_after,
            "actual_after": actual_interrupt_after,
            "checkpoint_id_hash": checkpoint_id_hash,
            "next_nodes_after_interrupt": next_nodes_after_interrupt,
            "prefix_stage_ids": prefix_snapshot["stage_ids"],
        },
        "resume": {
            "resumed_from_checkpoint": True,
            "checkpoint_id_hash": resumed["checkpoint_id_hash"],
            "record_path": str(record_path),
            "resumed_stage_ids": resumed_snapshot["stage_ids"],
        },
        "append_only_audit": append_only_audit,
        "stage_replay_audit": stage_replay_audit,
        "comparison_checks": comparison_checks,
        "uninterrupted_baseline_available": uninterrupted_baseline_available,
        "baseline_comparison_method": baseline_comparison_method,
        "baseline_comparison_verdict": baseline_comparison_verdict,
        "baseline_comparison_note": (
            "Independent uninterrupted baseline was compared with the resumed evidence snapshot."
            if uninterrupted_baseline_available
            else (
                "No independent uninterrupted baseline was produced for this run; comparison_checks are "
                "not_applicable and the top-level verdict only covers resume append-only/stage-replay audits."
            )
        ),
        "verdict_scope": (
            "append_only_stage_replay_and_independent_baseline_comparison"
            if uninterrupted_baseline_available
            else "append_only_stage_replay_only_no_independent_baseline"
        ),
        "allowed_diff_keys": [
            "run_id",
            "timestamps",
            "checkpoint_id",
            "checkpoint_path",
            "resume_diff_report_path",
            "operator_log_path",
        ],
        "acceptable_diffs": [],
        "unacceptable_diff_findings": unacceptable,
        "verdict": verdict,
        "main_result_eligible": False,
        "resume_run_main_result_eligible": False,
        "resume_run_main_result_eligible_assertion": {
            "expected": False,
            "actual": bool(record.final_artifacts.get("main_result_eligible")),
            "ok": record.final_artifacts.get("main_result_eligible") is False,
        },
        "run_record_path": str(record_path),
        "resume_diff_report_path": str(report_path),
        "real_agent_loop_resume_supported": True,
        "real_agent_loop_resume_support_level": "controlled_parent_node_boundary_only",
        "real_agent_loop_resume_scope": "controlled_parent_node_boundary_resume",
        "real_agent_loop_arbitrary_mid_node_resume_supported": False,
        "real_agent_loop_nested_subgraph_resume_supported": False,
        "mid_node_crash_supported": False,
        "transient_store_durable": False,
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(_jsonable(report), ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    _lg_f1_patch_record_with_report(record_path, report)
    return report


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
