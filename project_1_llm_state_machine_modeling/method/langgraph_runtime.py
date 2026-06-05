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
import uuid
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any, TypedDict

try:  # Python 3.10 compatibility for the repo venv.
    from typing import NotRequired
except ImportError:  # pragma: no cover - depends on interpreter minor version.
    from typing_extensions import NotRequired

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.config import get_store
from langgraph.graph import END, START, StateGraph
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command

from method.llm_stages import ChatProvider
from method.run_record import read_agent_loop_run_record, write_agent_loop_run_record
import method.staged_runtime as staged_runtime
from method.schema import (
    AgentLoopResult,
    DesignFeedback,
    GroundedElement,
    GroundingMap,
    LoopConfig,
    ModelReviewFeedback,
    SimFeedback,
    StageContext,
)
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    FullStagedRuntimeConfig,
    _LLMRetryExhausted,
    _RunState,
    _ValidationPass,
    ScenarioGenerationRequest,
    _apply_grounding_update_hints,
    _append_flow_log,
    _append_llm_stage_run,
    _append_stage,
    _build_record,
    _clone_stage_context,
    _compact_json,
    _extract_grounding_update_hints,
    _feedback_brief,
    _final_rejection_reason,
    _final_rejection_source_stage_id,
    _hash_text,
    _is_llm_stage_run,
    _mark_retry_exhausted,
    _make_waived_design_feedback,
    _make_waived_sim_feedback,
    _mark_sc12_verdict,
    _meta,
    _merge_scenario_sets_by_name,
    _model_review_blocks,
    _record_deterministic_iteration,
    _repair_selected_reason,
    _run_repair_path,
    _scenario_history_item,
    _selected_feedback_trace,
    _select_first_blocking,
    _short_hash,
    _stage_ids,
    _utc_now,
)
from method.stages.ids import ALL_STAGE_SPECS, StageId, StageStatus
from method.stages.ids import FeedbackSource
from method.stages.sd_tools import freeze_scenario_set

GRAPH_RUNTIME_SCHEMA_VERSION = "pr-langgraph.stategraph.v1"
NODE_EDGE_SCHEMA_VERSION = "pr-langgraph.stage-nodes.v1"
LG_D1_OPERATOR_EVENT_SCHEMA_VERSION = "lg-d1.operator-event.v1"
LG_D1_STREAM_SUMMARY_SCHEMA_VERSION = "lg-d1.stream-summary.v1"
LG_D1_INSTRUMENTATION_LAYER = "langgraph_streaming"

_VALID_RECORD_STATUSES = {"success", "failed", "rejected", "budget_exhausted", "error", "invalid"}
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


class _PickleCheckpointSerde:
    """Serializer for in-memory LangGraph checkpoints containing Python dataclasses.

    The durable academic evidence remains the JSON AgentLoopRunRecord written at
    SC-13.  LangGraph checkpoints are an orchestration/resume aid and need to
    carry live typed objects such as ``_RunState`` and ``_ValidationPass`` across
    graph nodes; the default msgpack serializer cannot encode those internal
    dataclasses.  We therefore make the serializer explicit and record it in
    runtime metadata instead of silently relying on LangGraph defaults.
    """

    def dumps_typed(self, obj: Any) -> tuple[str, bytes]:
        return "pickle", pickle.dumps(obj)

    def loads_typed(self, data: tuple[str, bytes]) -> Any:
        kind, payload = data
        if kind != "pickle":
            raise ValueError(f"unsupported checkpoint payload type: {kind}")
        return pickle.loads(payload)


class _CompatState(TypedDict, total=False):
    value: int


class _GraphLoopState(TypedDict, total=False):
    nl: str
    graph_trace: list[dict[str, Any]]
    operator_events: list[dict[str, Any]]
    operator_stream_enabled: bool
    run_id: str
    runtime_state: Any
    iteration: int
    iteration_stage_start: int
    validation_ref: str
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


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if is_dataclass(value) and not isinstance(value, type):
        return _jsonable(asdict(value))
    return str(value)


def _hash_payload(payload: Any) -> str:
    encoded = json.dumps(_jsonable(payload), ensure_ascii=False, sort_keys=True, default=str)
    return "sha256:" + hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _hash_file(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


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
    return {str(node.get("node_id") or ""): [str(item) for item in node.get("stage_ids", [])] for node in build_langgraph_node_registry()["nodes"]}


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

    from method.gpt_client import get_stream_enabled, get_stream_include_usage_enabled

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


def _stage_result_operator_events(record: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(record.stage_records):
        if not isinstance(row, dict):
            row = _jsonable(row)
        stage_id = str(row.get("stage_id") or "")
        stage_error = row.get("stage_error") or row.get("output_validation_error")
        events.append(
            build_lg_d1_operator_event(
                run_id=record.run_id,
                event_type="stage_result",
                node=_node_for_stage(stage_id),
                stage_id=stage_id,
                payload={
                    "stage_index": index,
                    "stage_kind": row.get("stage_kind"),
                    "enabled": row.get("enabled"),
                    "ran": row.get("ran"),
                    "ok": row.get("ok"),
                    "status": str(row.get("status") or ""),
                    "stage_error_hash": _hash_text(str(stage_error)) if stage_error else None,
                },
            )
        )
    return events


def _llm_progress_operator_events(record: Any) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for row in _llm_stream_usage_from_interactions(record.llm_interactions):
        stage_id = str(row.get("stage_id") or "")
        event_type = "llm_stream_progress" if row.get("stream") is True else "llm_request_progress"
        events.append(
            build_lg_d1_operator_event(
                run_id=record.run_id,
                event_type=event_type,
                node=_node_for_stage(stage_id),
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


def _package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except Exception:
        return "unknown"


def _canonical_stage_ids() -> list[str]:
    return [spec.stage_id for spec in ALL_STAGE_SPECS]


def build_langgraph_node_registry() -> dict[str, Any]:
    """Return PR-langgraph's explicit StateGraph node/edge registry."""

    nodes = [
        {
            "node_id": "sc0_start",
            "label": "SC-0 start/run setup",
            "kind": "control_node",
            "stage_ids": [StageId.SC_0_START.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "sl1_initial_modeling",
            "label": "SL-1 initial NL to DSL modeling",
            "kind": "llm_stage_node",
            "stage_ids": [StageId.SL_1_INITIAL_MODELING.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "iteration_gate",
            "label": "iteration budget/verdict router",
            "kind": "control_node",
            "stage_ids": [],
            "delegated_subgraph": False,
        },
        {
            "node_id": "validation_pass",
            "label": "SD/SL validation pass",
            "kind": "validation_subgraph",
            "stage_ids": [
                StageId.SD_2_PARSE.value,
                StageId.SD_3_SEMANTIC.value,
                StageId.SD_4_DESIGN.value,
                StageId.SL_5_SCENARIO_GENERATION.value,
                StageId.SD_5A_SCENARIO_COVERAGE.value,
                StageId.SC_5F_SCENARIO_FREEZE.value,
                StageId.SD_6_SIM.value,
                StageId.SL_7_MODEL_REVIEW.value,
            ],
            "delegated_subgraph": True,
            "subgraph_id": "validation_subgraph",
            "subgraph_node_ids": [
                "validation_enter",
                "validation_sd2_parse",
                "validation_sd3_semantic",
                "validation_sd4_design",
                "validation_sl5_scenario_generation",
                "validation_sd5a_scenario_coverage",
                "validation_sd5a_reuse_coverage",
                "validation_sc5f_scenario_freeze",
                "validation_sd6_sim",
                "validation_sl7_model_review",
                "validation_finalize",
            ],
        },
        {
            "node_id": "validation_decision",
            "label": "post-validation success/weak-oracle/repair router",
            "kind": "control_node",
            "stage_ids": [StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "repair_path",
            "label": "SD-8 fix requests + SL-9 repair + SL-10 repair review",
            "kind": "stage_group_node",
            "stage_ids": [
                StageId.SD_8_FIX_PLAN.value,
                StageId.SL_9_REPAIR.value,
                StageId.SL_10_REPAIR_REVIEW.value,
                StageId.SC_11_ACCEPT_CANDIDATE.value,
            ],
            "delegated_subgraph": False,
        },
        {
            "node_id": "repair_decision",
            "label": "post-repair retry/waiver/budget router",
            "kind": "control_node",
            "stage_ids": [StageId.SC_11_ACCEPT_CANDIDATE.value, StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "waiver_continue",
            "label": "continue downstream validation after accepted no-edit waiver",
            "kind": "validation_subgraph_continuation",
            "stage_ids": [
                StageId.SD_4_DESIGN.value,
                StageId.SL_5_SCENARIO_GENERATION.value,
                StageId.SD_5A_SCENARIO_COVERAGE.value,
                StageId.SC_5F_SCENARIO_FREEZE.value,
                StageId.SD_6_SIM.value,
                StageId.SL_7_MODEL_REVIEW.value,
                StageId.SC_12_EXIT.value,
            ],
            "delegated_subgraph": True,
            "subgraph_id": "validation_subgraph",
            "subgraph_node_ids": [
                "validation_enter",
                "validation_sd4_design",
                "validation_sl5_scenario_generation",
                "validation_sd5a_scenario_coverage",
                "validation_sd5a_reuse_coverage",
                "validation_sc5f_scenario_freeze",
                "validation_sd6_sim",
                "validation_sl7_model_review",
                "validation_finalize",
            ],
        },
        {
            "node_id": "sc12_budget_exhausted",
            "label": "SC-12 budget-exhausted verdict",
            "kind": "control_node",
            "stage_ids": [StageId.SC_12_EXIT.value],
            "delegated_subgraph": False,
        },
        {
            "node_id": "sc13_trace_audit",
            "label": "SC-13 trace audit and run-record write",
            "kind": "control_node",
            "stage_ids": [StageId.SC_13_TRACE_AUDIT.value],
            "delegated_subgraph": False,
        },
    ]
    edges = [
        {"source": START, "target": "sc0_start"},
        {"source": "sc0_start", "target": "sl1_initial_modeling"},
        {"source": "sl1_initial_modeling", "target": "iteration_gate"},
        {"source": "iteration_gate", "target": "validation_pass", "condition": "continue_validation"},
        {"source": "iteration_gate", "target": "sc12_budget_exhausted", "condition": "budget_exhausted"},
        {"source": "iteration_gate", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "validation_pass", "target": "validation_decision"},
        {"source": "validation_decision", "target": "repair_path", "condition": "repair_required"},
        {"source": "validation_decision", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "repair_path", "target": "repair_decision"},
        {"source": "repair_decision", "target": "waiver_continue", "condition": "waiver_continue"},
        {"source": "repair_decision", "target": "iteration_gate", "condition": "next_iteration"},
        {"source": "repair_decision", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "waiver_continue", "target": "iteration_gate", "condition": "next_iteration"},
        {"source": "waiver_continue", "target": "sc13_trace_audit", "condition": "verdict_ready"},
        {"source": "sc12_budget_exhausted", "target": "sc13_trace_audit"},
        {"source": "sc13_trace_audit", "target": END},
    ]
    return {
        "schema_version": NODE_EDGE_SCHEMA_VERSION,
        "runtime_backend": "langgraph",
        "opaque_wrapper": False,
        "delegated_monolithic_runtime": False,
        "canonical_stage_sequence": _canonical_stage_ids(),
        "nodes": nodes,
        "edges": edges,
        "instrumentation_layer": "langgraph",
        "notes": [
            "LangGraph owns the default orchestration path; no public staged/langgraph backend switch remains.",
            "method.staged_runtime is reused only as the canonical stage-semantics/helper library.",
        ],
    }


def graph_registry_consistency(planned_stage_graph: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    """Compare planned SC/SD/SL stage IDs with LangGraph registry coverage."""

    planned = [str(item) for item in planned_stage_graph.get("planned", [])]
    covered: list[str] = []
    node_stage_pairs: list[dict[str, str]] = []
    for node in registry.get("nodes", []):
        node_id = str(node.get("node_id") or "")
        for stage_id in node.get("stage_ids", []):
            covered_stage_id = str(stage_id)
            covered.append(covered_stage_id)
            node_stage_pairs.append({"node_id": node_id, "stage_id": covered_stage_id})
    covered_set = set(covered)
    planned_set = set(planned)
    missing = [stage_id for stage_id in planned if stage_id not in covered_set]
    extra = [stage_id for stage_id in covered if stage_id not in planned_set]
    duplicate_stage_ids = sorted({stage_id for stage_id in covered if covered.count(stage_id) > 1})
    duplicate_stage_id_nodes = {
        stage_id: [item["node_id"] for item in node_stage_pairs if item["stage_id"] == stage_id]
        for stage_id in duplicate_stage_ids
    }
    opaque = bool(registry.get("opaque_wrapper")) or len(registry.get("nodes", [])) <= 1
    delegated_monolithic = bool(registry.get("delegated_monolithic_runtime")) or any(
        str(node.get("delegation_target") or "").endswith("run_full_staged_deterministic_runtime")
        for node in registry.get("nodes", [])
        if isinstance(node, dict)
    )
    return {
        "ok": not missing and not extra and not opaque and not delegated_monolithic,
        "missing_stage_ids": missing,
        "extra_stage_ids": extra,
        "opaque_wrapper": opaque,
        "delegated_monolithic_runtime": delegated_monolithic,
        "planned_count": len(planned),
        "covered_count": len(covered),
        "duplicate_stage_ids": duplicate_stage_ids,
        "duplicate_stage_id_nodes": duplicate_stage_id_nodes,
        "duplicate_stage_id_policy": (
            "allowed_when_one SC/SD/SL stage is represented by both a stage_group node "
            "and a routing/audit control node; duplicates are reported for audit and "
            "do not by themselves make registry coverage invalid"
        ),
    }


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


def langgraph_store_compat_smoke() -> dict[str, Any]:
    """Run a focused LangGraph Store smoke for LG-A2 transient object storage.

    LG-A2 relies on ``StateGraph.compile(store=...)`` and node-local
    ``get_store()`` rather than a module-level Python dict.  This smoke is kept
    separate from the generic checkpoint smoke so CI can fail fast if the
    installed LangGraph version changes Store APIs in a way that would make
    transient validation objects disappear between nodes.
    """

    result: dict[str, Any] = {
        "ok": False,
        "langgraph_version": _package_version("langgraph"),
        "inmemory_store_ok": False,
        "namespace_isolation_ok": False,
        "compile_store_ok": False,
        "get_store_ok": False,
        "delete_ok": False,
    }
    try:
        store = InMemoryStore()
        ns_a = ("lg-a2-store-smoke", "a")
        ns_b = ("lg-a2-store-smoke", "b")
        store.put(ns_a, "same-key", {"value": 1})
        store.put(ns_b, "same-key", {"value": 2})
        item_a = store.get(ns_a, "same-key")
        item_b = store.get(ns_b, "same-key")
        result["inmemory_store_ok"] = bool(item_a and item_a.value == {"value": 1})
        result["namespace_isolation_ok"] = bool(item_b and item_b.value == {"value": 2})
        store.delete(ns_a, "same-key")
        result["delete_ok"] = store.get(ns_a, "same-key") is None and store.get(ns_b, "same-key") is not None

        class _StoreSmokeState(TypedDict, total=False):
            value: int

        graph = StateGraph(_StoreSmokeState)

        def node(state: _StoreSmokeState) -> _StoreSmokeState:
            active_store = get_store()
            active_store.put(("lg-a2-store-smoke", "node"), "value", {"value": int(state.get("value", 0)) + 1})
            item = active_store.get(("lg-a2-store-smoke", "node"), "value")
            return {"value": int((item.value if item is not None else {}).get("value", 0))}

        graph.add_node("store_node", node)
        graph.add_edge(START, "store_node")
        graph.add_edge("store_node", END)
        app = graph.compile(store=store)
        result["compile_store_ok"] = True
        output = app.invoke({"value": 41})
        result["get_store_ok"] = output.get("value") == 42 and store.get(("lg-a2-store-smoke", "node"), "value") is not None
        result["ok"] = all(
            bool(result[key])
            for key in ("inmemory_store_ok", "namespace_isolation_ok", "compile_store_ok", "get_store_ok", "delete_ok")
        )
    except Exception as exc:  # pragma: no cover - returned payload is enough for callers/tests.
        result["error"] = f"{type(exc).__name__}: {str(exc)[:300]}"
    return result


def _checkpoint_resume_smoke() -> dict[str, Any]:
    """Exercise LangGraph checkpoints/resume for append-only repair ledger metadata."""

    class _LedgerState(TypedDict, total=False):
        fix_log: list[dict[str, Any]]
        checkpoint_label: str

    labels = ["after_SD-8", "after_SL-9", "after_SL-10_rework"]

    def compile_app() -> Any:
        graph = StateGraph(_LedgerState)

        def append_entry(label: str):
            def _node(state: _LedgerState) -> _LedgerState:
                log = list(state.get("fix_log", []) or [])
                log.append(
                    {
                        "entry_id": f"checkpoint-smoke-{len(log) + 1}",
                        "phase": label,
                        "candidate_dsl_hash": f"sha256:{label}",
                    }
                )
                return {"fix_log": log, "checkpoint_label": label}

            return _node

        for label in labels:
            graph.add_node(label, append_entry(label))
        graph.add_edge(START, labels[0])
        graph.add_edge(labels[0], labels[1])
        graph.add_edge(labels[1], labels[2])
        graph.add_edge(labels[2], END)
        return graph.compile(checkpointer=InMemorySaver(serde=_PickleCheckpointSerde()))

    app = compile_app()
    config = {"configurable": {"thread_id": "pr-langgraph-fixlog-append-only-smoke"}}
    final_state = app.invoke({"fix_log": []}, config=config)
    history = list(app.get_state_history(config))
    snapshots = [
        snapshot.values.get("fix_log", [])
        for snapshot in reversed(history)
        if isinstance(getattr(snapshot, "values", None), dict) and snapshot.values.get("fix_log")
    ]
    append_only = True
    duplicate_entry_detected = False
    last: list[dict[str, Any]] = []
    for log in snapshots:
        if log[: len(last)] != last:
            append_only = False
        ids = [str(entry.get("entry_id")) for entry in log if isinstance(entry, dict)]
        duplicate_entry_detected = duplicate_entry_detected or len(ids) != len(set(ids))
        last = list(log)

    resume_checks: list[dict[str, Any]] = []
    for index, label in enumerate(labels):
        resume_app = compile_app()
        thread_id = f"pr-langgraph-resume-{label}"
        run_config = {"configurable": {"thread_id": thread_id}}
        prefix_state = resume_app.invoke({"fix_log": []}, config=run_config, interrupt_after=[label])
        checkpoint = resume_app.get_state(run_config)
        resumed = resume_app.invoke(None, config=checkpoint.config)
        prefix_log = list(prefix_state.get("fix_log", []) or [])
        resumed_log = list(resumed.get("fix_log", []) or [])
        ids = [str(entry.get("entry_id")) for entry in resumed_log if isinstance(entry, dict)]
        resume_checks.append(
            {
                "breakpoint": label,
                "prefix_count": len(prefix_log),
                "expected_prefix_count": index + 1,
                "resumed_count": len(resumed_log),
                "prefix_preserved": resumed_log[: len(prefix_log)] == prefix_log,
                "append_only": resumed_log[: len(prefix_log)] == prefix_log and len(ids) == len(set(ids)),
                "next_nodes_after_interrupt": list(getattr(checkpoint, "next", ()) or []),
            }
        )

    resume_append_only = all(item["append_only"] for item in resume_checks)
    return {
        "scope": "toy_ledger_langgraph_api_smoke",
        "real_agent_loop_resume_supported": False,
        "real_agent_loop_resume_scope": "not_claimed_in_PR_langgraph_round1",
        "academic_claim": (
            "This smoke validates LangGraph interrupt/resume API shape and append-only "
            "ledger behavior on a minimal FixLog-like state only. It is not evidence "
            "that an interrupted real agent-loop run can be resumed for main-result "
            "statistics."
        ),
        "checked_breakpoints": labels,
        "checkpoint_history_count": len(history),
        "final_fix_log_count": len(final_state.get("fix_log", []) or []),
        "fix_log_append_only": append_only and len(final_state.get("fix_log", []) or []) == len(labels),
        "duplicate_entry_detected": duplicate_entry_detected,
        "resume_checks": resume_checks,
        "resume_append_only": resume_append_only,
        "resume_api": "StateGraph interrupt_after/get_state/invoke(None)/InMemorySaver",
    }


def _graph_runtime_metadata(*, registry: dict[str, Any], compat: dict[str, Any], graph_config_hash: str) -> dict[str, Any]:
    return {
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
        "checkpoint_path_hash": "sha256:memory",
        "resumed_from_checkpoint": False,
        "resume_checkpoint_id_hash": None,
        "instrumentation_layer": "langgraph",
        "checkpoint_resume_smoke": _checkpoint_resume_smoke(),
        "langgraph_compat_smoke": compat,
        "dependency_versions": {
            "python": platform.python_version(),
            "langgraph": compat.get("langgraph_version", _package_version("langgraph")),
            "langgraph-checkpoint": compat.get("langgraph_checkpoint_version", _package_version("langgraph-checkpoint")),
            "langchain-core": _package_version("langchain-core"),
        },
    }


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


def _transient_namespace(run_id: str) -> tuple[str, str]:
    return ("transient", run_id)


def _transient_namespace_label(run_id: str) -> str:
    return f"transient/{run_id}"


def _put_transient(run_id: str, kind: str, iteration: int, value: Any, *, lifecycle: dict[str, Any] | None = None) -> str:
    """Store a transient object inside the active LangGraph Store context.

    This helper must only be called from compiled LangGraph nodes, because it
    depends on ``langgraph.config.get_store()`` being available in the current
    runnable context.  It deliberately does not write the historical module
    level ``_TRANSIENT_OBJECTS`` dict.
    """

    key = f"{kind}:{iteration}:{uuid.uuid4().hex[:8]}"
    get_store().put(
        _transient_namespace(run_id),
        key,
        {
            "_transient_wrapper": True,
            "object": value,
            "kind": kind,
            "iteration": iteration,
            "object_type": type(value).__name__,
            "run_id": run_id,
        },
    )
    if lifecycle is not None:
        lifecycle["put_count"] = int(lifecycle.get("put_count", 0)) + 1
    return key


def _get_transient(run_id: str, key: str, *, lifecycle: dict[str, Any] | None = None) -> Any:
    """Load a transient object from the active LangGraph Store context."""

    item = get_store().get(_transient_namespace(run_id), key)
    if item is None:
        raise KeyError(f"missing transient LangGraph runtime object: {key}")
    if lifecycle is not None:
        lifecycle["get_count"] = int(lifecycle.get("get_count", 0)) + 1
    value = item.value
    if isinstance(value, dict) and value.get("_transient_wrapper") is True and "object" in value:
        return value["object"]
    return value


def _drop_transient(run_id: str | None, key: str | None, *, lifecycle: dict[str, Any] | None = None) -> None:
    """Delete a transient Store object if it exists in the active graph node."""

    if key:
        try:
            namespace = _transient_namespace(str(run_id or ""))
            existed = get_store().get(namespace, key) is not None
            get_store().delete(namespace, key)
            if lifecycle is not None and existed:
                lifecycle["drop_count"] = int(lifecycle.get("drop_count", 0)) + 1
        except Exception as exc:
            if lifecycle is not None:
                lifecycle.setdefault("cleanup_errors", []).append(f"drop:{type(exc).__name__}:{str(exc)[:160]}")


def _drain_transients(run_id: str, *, lifecycle: dict[str, Any] | None = None) -> dict[str, Any]:
    """Final-drain all transient items in this run's Store namespace."""

    namespace = _transient_namespace(run_id)
    items = list(get_store().search(namespace))
    deleted = 0
    for item in items:
        get_store().delete(namespace, item.key)
        deleted += 1
    remaining = list(get_store().search(namespace))
    cleanup_status = "no_leak" if not remaining else f"partial_leak_{len(remaining)}_items"
    if lifecycle is not None:
        lifecycle["final_drain_count"] = int(lifecycle.get("final_drain_count", 0)) + 1
        lifecycle["final_item_count"] = len(remaining)
        lifecycle["cleanup_status"] = cleanup_status
        lifecycle["drained_item_count"] = int(lifecycle.get("drained_item_count", 0)) + deleted
    return {
        "drained_count": deleted,
        "final_item_count": len(remaining),
        "cleanup_status": cleanup_status,
    }


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


def _initial_run_id(nl: str, runtime_cfg: FullStagedRuntimeConfig) -> str:
    if runtime_cfg.run_id:
        return runtime_cfg.run_id
    input_hash = hashlib.sha256(f"{nl}\n{runtime_cfg.initial_dsl}".encode("utf-8")).hexdigest()[:12]
    return f"pr-langgraph-{input_hash}-{uuid.uuid4().hex[:12]}"


def _run_initial_modeling_node_logic(*, nl: str, runtime_cfg: FullStagedRuntimeConfig, adapters: FullStagedRuntimeAdapters, state: _RunState) -> None:
    if adapters.initial_modeling is None:
        return
    try:
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
    except _LLMRetryExhausted as exc:
        _mark_retry_exhausted(state, exc)


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
            repair_patch = dict(graph_state.get("repair_patch") or {})
            waiver_audit = repair_patch.get("waiver_audit")
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
        parse_feedback, parse_meta = adapters.parse(runtime_state.current_dsl, context)
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
        semantic_feedback, semantic_meta = adapters.semantic(runtime_state.current_dsl, context)
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
        design_feedback, design_meta = adapters.design(context)
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
        generated = adapters.scenario_generate(request)
        generated = _append_llm_stage_run(
            run=generated,
            expected_stage_id=StageId.SL_5_SCENARIO_GENERATION,
            stage_records=runtime_state.stage_records,
            iteration_stage_metas=graph_state["validation_stage_metas"],
            llm_interactions=runtime_state.llm_interactions,
            logs=runtime_state.logs,
            iteration=iteration,
            parsed_summary={"attempt_index": attempt_index, "kind": "scenario_generation" if retry_mode == "initial" else "scenario_refresh"},
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
        coverage, coverage_meta = adapters.scenario_coverage(runtime_state.current_dsl, scenarios)
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
        coverage, coverage_meta = adapters.scenario_coverage(runtime_state.current_dsl, list(scenario_set.scenarios))
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
        scenario_set, freeze_meta = freeze_scenario_set(
            scenarios,
            source_dsl_hash=_hash_text(runtime_state.current_dsl),
            source_inspect_hash=_short_hash(context.inspect_json) if context.inspect_json is not None else "",
            source_grounding_hash=_short_hash(runtime_cfg.grounding_map) if runtime_cfg.grounding_map is not None else None,
            coverage_report=selected_coverage,
            epoch=epoch,
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
        sim_feedback, sim_meta = adapters.sim(runtime_state.current_dsl, scenario_set, context)
        feedback[FeedbackSource.SIM.value] = sim_feedback
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
        review_run = adapters.model_review(
            runtime_state.current_dsl,
            context,
            review_payload,
        )
        review_run = _append_llm_stage_run(
            run=review_run,
            expected_stage_id=StageId.SL_7_MODEL_REVIEW,
            stage_records=runtime_state.stage_records,
            iteration_stage_metas=stage_metas,
            llm_interactions=runtime_state.llm_interactions,
            logs=runtime_state.logs,
            iteration=iteration,
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


def _build_graph(*, runtime_cfg: FullStagedRuntimeConfig, adapters: FullStagedRuntimeAdapters) -> Any:
    graph = StateGraph(_GraphLoopState)
    store = InMemoryStore()
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
        _run_initial_modeling_node_logic(nl=graph_state["nl"], runtime_cfg=runtime_cfg, adapters=adapters, state=runtime_state)
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
        try:
            accepted, repair_patch = _run_repair_path(
                nl=graph_state["nl"],
                cfg=runtime_cfg,
                adapters=adapters,
                state=runtime_state,
                iteration=iteration,
                validation=_get_transient(runtime_state.run_id, str(graph_state.get("validation_ref") or ""), lifecycle=transient_lifecycle),
            )
        except _LLMRetryExhausted as exc:
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
            reason = f"SC-11 budget gate blocked SD-2 revalidation: iter+1={iteration + 1} >= max_iterations={runtime_cfg.max_iterations}"
            _mark_sc12_verdict(
                runtime_state,
                verdict="not_converged",
                source_stage_id=StageId.SC_11_ACCEPT_CANDIDATE.value,
                reason=reason,
                record_status="budget_exhausted",
                result_status="not_converged",
                stage_ok=False,
                stage_status=StageStatus.FAIL,
            )
            iteration_record["exit_reason"] = reason
            iteration_record["budget_gate"] = {
                "source_stage_id": StageId.SC_11_ACCEPT_CANDIDATE.value,
                "iter_plus_one": iteration + 1,
                "max_iterations": runtime_cfg.max_iterations,
                "next_stage_allowed": False,
            }
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
        _trace_node(graph_state, "waiver_continue", iteration=iteration)
        try:
            graph_state["validation_continuation_source"] = validation
            graph_state = dict(
                validation_subgraph.invoke(
                    graph_state,
                    config={"configurable": {"thread_id": f"{runtime_state.run_id}:validation-waiver:{iteration}"}},
                )
            )
            runtime_state = graph_state["runtime_state"]
            continued_validation = graph_state.get("validation_result")
            if not isinstance(continued_validation, _ValidationPass):
                raise TypeError("validation subgraph did not return a _ValidationPass after waiver continuation")
            _drop_validation_subgraph_state(graph_state)
        except _LLMRetryExhausted as exc:
            _drop_validation_subgraph_state(graph_state)
            _mark_retry_exhausted(runtime_state, exc)
            iteration_record["exit_reason"] = runtime_state.verdict_reason
            iteration_record["repair_stage_ids"] = _stage_ids(runtime_state.stage_records[iteration_stage_start:])[len(iteration_record.get("stage_ids") or []) :]
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
    return graph.compile(checkpointer=InMemorySaver(serde=_PickleCheckpointSerde()), store=store)


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
    record.final_artifacts["langgraph_runtime_trace"] = {
        "node_trace_count": len(safe_trace),
        "node_trace_hash": record.environment["langgraph_node_trace_hash"],
        "delegated_monolithic_runtime": False,
    }
    write_agent_loop_run_record(record, path)


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
    record.run_config["lg_d1_operator_log_enabled"] = True
    record.run_config["instrumentation_layer_detail"] = LG_D1_INSTRUMENTATION_LAYER
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
    graph_config = {
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
        "runtime_backend": "langgraph_default",
        "checkpoint_backend": "memory",
        "checkpoint_serde": "pickle",
        "runtime_schema_version": GRAPH_RUNTIME_SCHEMA_VERSION,
        "node_edge_schema_version": NODE_EDGE_SCHEMA_VERSION,
        "lg_d1_operator_stream_enabled": bool(operator_stream_enabled),
    }
    graph_config_hash = _hash_payload(graph_config)
    metadata = _graph_runtime_metadata(registry=registry, compat=compat, graph_config_hash=graph_config_hash)
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
    operator_events = _merge_operator_events(operator_events, state.get("operator_events"))
    _augment_run_record_with_lg_d1_operator_log(
        result,
        operator_events=operator_events,
        graph_stream_status=graph_stream_status,
        operator_stream_enabled=bool(operator_stream_enabled),
    )
    result.resolved_config = resolved
    result.planned_stage_graph = planned
    return result
