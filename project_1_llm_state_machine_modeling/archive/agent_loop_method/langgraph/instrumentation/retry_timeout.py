"""LG-D2 retry/timeout envelope instrumentation for LangGraph LLM nodes."""

from __future__ import annotations

import json
from collections import Counter
from typing import Any

from method.langgraph.instrumentation.common import _hash_canonical_payload, _hash_payload, _jsonable, _canonical_json_payload
from method.langgraph.instrumentation.operator_stream import LG_D1_OPERATOR_EVENT_SCHEMA_VERSION, _sanitize_lg_d1_operator_payload
from method.staged_runtime import _LLMRetryExhausted, _RunState, _append_flow_log, _append_stage, _hash_text, _meta, _utc_now
from method.schema import StageResultMeta
from method.stages.ids import StageId, StageStatus

LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION = "lg-d2.llm-node-envelope.v1"

LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION = "lg-d2.llm-node-envelope-event.v1"

LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER = "langgraph_llm_node_envelope"

LG_D2_LLM_NODE_ENVELOPE_EVENT_TYPES = {
    "lg_d2_envelope_enter",
    "lg_d2_retry",
    "lg_d2_timeout",
    "lg_d2_envelope_exit",
    "lg_d2_retry_exhausted",
}

def build_lg_d2_llm_node_envelope_policy() -> dict[str, Any]:
    """Return the canonical LG-D2 node-level LLM envelope policy.

    LG-D2 is intentionally an outer, LangGraph-visible diagnostics envelope. It
    does not change the inner PR-B2 LLM-stage retry ledger, prompt, stream flag,
    or ``max_tokens`` default.  The policy is hashed with canonical JSON so a
    run record can later prove exactly which envelope contract was in force.
    """

    policy = {
        "schema_version": LG_D2_LLM_NODE_ENVELOPE_SCHEMA_VERSION,
        "enabled": True,
        "max_envelope_attempts": 2,
        "timeout_s": None,
        "backoff": {"strategy": "none", "base_ms": 0, "max_ms": 0},
        "jitter": {"enabled": False, "seed": 0},
        "retryable_error_taxonomy": [
            "provider_5xx",
            "provider_502",
            "provider_504",
            "provider_error",
            "network_error",
            "timeout",
            "stream_interrupted",
            "schema_invalid",
            "empty_output",
        ],
        "non_retryable_error_taxonomy": ["schema_contract_error", "stage_id_mismatch", "deterministic_feedback"],
        "stream_default": True,
        "max_tokens_default": None,
        "outer_envelope_does_not_replace_inner_attempt_ledger": True,
        "fake_clock_supported_for_tests": True,
        "real_sleep_required_for_tests": False,
    }
    policy["policy_hash"] = _hash_canonical_payload(policy)
    return policy

def _lg_d2_retryable_taxonomy(policy: dict[str, Any] | None = None) -> set[str]:
    policy = policy or build_lg_d2_llm_node_envelope_policy()
    return {str(item) for item in policy.get("retryable_error_taxonomy", [])}

def _lg_d2_error_kind_from_exception(exc: BaseException) -> str:
    name = type(exc).__name__.lower()
    message = str(exc).lower()
    text = f"{name} {message}"
    # Provider HTTP status codes must win over generic words such as
    # "timeout"/"connection"; otherwise Cloudflare/API 504 Gateway Timeout
    # incidents are incorrectly reported as local timeouts, which blurs the
    # invalid-run vs model-quality boundary in experiment audits.
    if "502" in text:
        return "provider_502"
    if "504" in text:
        return "provider_504"
    if "5xx" in text or "500" in text or "503" in text:
        return "provider_5xx"
    if isinstance(exc, TimeoutError):
        return "timeout"
    if "timeout" in name or "timeout" in message or "timed out" in message:
        return "timeout"
    if "stream" in name or "stream" in message:
        return "stream_interrupted"
    if "network" in name or "connection" in name or "network" in message or "connection" in message:
        return "network_error"
    return "provider_error"

def _lg_d2_exception_is_provider_retryable(exc: BaseException, policy: dict[str, Any]) -> bool:
    """Return True only for upstream/provider-like failures safe to map into invalid-run evidence.

    Local contract/programming errors such as TypeError, ValueError, AssertionError,
    KeyError, AttributeError, import errors and cancellation must not be disguised
    as provider_error, because that would corrupt root-cause evidence and make
    academic trace audits misleading.
    """

    if isinstance(exc, (TypeError, ValueError, AssertionError, KeyError, AttributeError, ImportError, NotImplementedError)):
        return False
    error_kind = _lg_d2_error_kind_from_exception(exc)
    retryable = _lg_d2_retryable_taxonomy(policy)
    if error_kind in {"timeout", "stream_interrupted", "network_error", "provider_502", "provider_504", "provider_5xx"}:
        return True
    if error_kind == "provider_error":
        text = f"{type(exc).__name__}: {exc}".lower()
        provider_markers = ("provider", "openai", "api", "http", "502", "503", "504", "5xx", "rate limit", "connection", "network", "upstream")
        return any(marker in text for marker in provider_markers) and error_kind in retryable
    return error_kind in retryable

def _lg_d2_retry_error_for_exception(stage_id: StageId, exc: BaseException) -> dict[str, Any]:
    error_kind = _lg_d2_error_kind_from_exception(exc)
    return {
        "error_kind": error_kind,
        "error_message": f"{type(exc).__name__}: {str(exc)[:300]}",
        "exception_type": type(exc).__name__,
        "stage_id": stage_id.value,
        "source": "lg_d2_llm_node_envelope",
    }

def _lg_d2_stage_meta_for_retry_error(stage_id: StageId, retry_error: dict[str, Any]) -> StageResultMeta:
    meta = _meta(stage_id, ok=False, status=StageStatus.ERROR)
    meta.stage_error = str(retry_error.get("error_message") or f"{stage_id.value} retry exhausted")
    return meta

def _lg_d2_envelope_safe_summary(value: Any, *, max_chars: int = 240) -> Any:
    safe = _jsonable(value)
    if isinstance(safe, str):
        return {"text_hash": _hash_text(safe), "text_chars": len(safe)}
    if isinstance(safe, list):
        return {"item_count": len(safe), "items_hash": _hash_canonical_payload(safe)}
    if isinstance(safe, dict):
        out: dict[str, Any] = {}
        for key, nested in safe.items():
            key_text = str(key)
            key_norm = key_text.lower()
            if any(fragment in key_norm for fragment in ("prompt", "message", "raw", "output", "content", "text", "nl", "secret", "token", "api_key", "apikey")) or key_norm.endswith("_dsl") or key_norm == "dsl":
                out[f"{key_text}_hash"] = _hash_canonical_payload(nested)
                out[f"{key_text}_chars"] = len(_canonical_json_payload(nested))
            elif isinstance(nested, (dict, list, tuple, set)):
                out[f"{key_text}_hash"] = _hash_canonical_payload(nested)
                out[f"{key_text}_count"] = len(nested)
            else:
                out[key_text] = nested
        return out
    text = str(safe)
    return text if len(text) <= max_chars else {"text_hash": _hash_text(text), "text_chars": len(text)}

def _lg_d2_latest_interaction_index(state: _RunState) -> int | None:
    if not state.llm_interactions:
        return None
    return len(state.llm_interactions) - 1

def _lg_d2_latest_attempt_index(interaction: dict[str, Any] | None) -> int | None:
    attempts = interaction.get("attempts") if isinstance(interaction, dict) else None
    if isinstance(attempts, list) and attempts:
        return len(attempts) - 1
    return None

def _lg_d2_attempt_error_kind(attempt: Any) -> str | None:
    if not isinstance(attempt, dict):
        return None
    for key in ("error_kind", "status", "kind"):
        value = attempt.get(key)
        if value:
            text = str(value)
            if text.lower() not in {"ok", "success", "passed"}:
                return text
    return None

def _lg_d2_envelope_event(
    *,
    run_id: str,
    event_type: str,
    stage_id: StageId,
    graph_node: str,
    subgraph_id: str | None,
    policy: dict[str, Any],
    iteration: int | None = None,
    envelope_attempt_index: int = 0,
    canonical_interaction_id: int | None = None,
    canonical_attempt_index: int | None = None,
    error_kind: str | None = None,
    retryable: bool | None = None,
    elapsed_ms: int = 0,
    planned_sleep_ms: int = 0,
    outcome: str | None = None,
    safe_summary: Any | None = None,
) -> dict[str, Any]:
    payload = {
        "schema_version": LG_D2_LLM_NODE_ENVELOPE_EVENT_SCHEMA_VERSION,
        "event_type": event_type,
        "stage_id": stage_id.value,
        "iteration": iteration,
        "graph_node": graph_node,
        "subgraph_id": subgraph_id,
        "policy_hash": policy.get("policy_hash"),
        "envelope_attempt_index": envelope_attempt_index,
        "canonical_interaction_id": canonical_interaction_id,
        "canonical_attempt_index": canonical_attempt_index,
        "error_kind": error_kind,
        "retryable": retryable,
        "elapsed_ms": int(elapsed_ms),
        "planned_sleep_ms": int(planned_sleep_ms),
        "outcome": outcome,
        "safe_summary": _lg_d2_envelope_safe_summary(safe_summary or {}),
        "does_not_replace_academic_evidence": True,
    }
    safe_payload, omitted_count = _sanitize_lg_d1_operator_payload(payload)
    if omitted_count:
        safe_payload["omitted_raw_content_field_count"] = omitted_count
    event = {
        # LG-D2 events live inside the LG-D1 operator-log JSONL stream, so the
        # top-level schema must remain LG-D1-compatible.  The LG-D2-specific
        # schema is carried in payload["schema_version"] to keep existing
        # stream-summary reconstruction and LG-C1 audit stable after upstream
        # merges such as LG-F1 checkpoint/resume.
        "schema_version": LG_D1_OPERATOR_EVENT_SCHEMA_VERSION,
        "run_id": str(run_id),
        "event_type": event_type,
        "timestamp": _utc_now(),
        "node": graph_node,
        "stage_id": stage_id.value,
        "instrumentation_layer": LG_D2_LLM_NODE_ENVELOPE_INSTRUMENTATION_LAYER,
        "payload": safe_payload,
        "payload_hash": _hash_canonical_payload(safe_payload),
    }
    json.dumps(event, ensure_ascii=False, sort_keys=True, allow_nan=False)
    return event

def _append_lg_d2_envelope_event(
    graph_state: _GraphLoopState,
    *,
    event_type: str,
    stage_id: StageId,
    graph_node: str,
    subgraph_id: str | None,
    policy: dict[str, Any] | None = None,
    iteration: int | None = None,
    envelope_attempt_index: int = 0,
    canonical_interaction_id: int | None = None,
    canonical_attempt_index: int | None = None,
    error_kind: str | None = None,
    retryable: bool | None = None,
    elapsed_ms: int = 0,
    planned_sleep_ms: int = 0,
    outcome: str | None = None,
    safe_summary: Any | None = None,
) -> None:
    if not bool(graph_state.get("operator_stream_enabled", True)):
        return
    runtime_state = graph_state.get("runtime_state")
    run_id = getattr(runtime_state, "run_id", None) or graph_state.get("run_id") or ""
    if not run_id:
        return
    policy = policy or build_lg_d2_llm_node_envelope_policy()
    if iteration is None and subgraph_id is not None and isinstance(graph_state.get("iteration"), int):
        iteration = int(graph_state["iteration"])
    event = _lg_d2_envelope_event(
        run_id=str(run_id),
        event_type=event_type,
        stage_id=stage_id,
        graph_node=graph_node,
        subgraph_id=subgraph_id,
        policy=policy,
        iteration=iteration,
        envelope_attempt_index=envelope_attempt_index,
        canonical_interaction_id=canonical_interaction_id,
        canonical_attempt_index=canonical_attempt_index,
        error_kind=error_kind,
        retryable=retryable,
        elapsed_ms=elapsed_ms,
        planned_sleep_ms=planned_sleep_ms,
        outcome=outcome,
        safe_summary=safe_summary,
    )
    events = list(graph_state.get("operator_events", []) or [])
    events.append(event)
    graph_state["operator_events"] = events
    if isinstance(runtime_state, _RunState):
        _append_flow_log(
            runtime_state.logs,
            event=event_type,
            stage_id=stage_id.value,
            iteration=iteration,
            graph_node=graph_node,
            graph_subgraph=subgraph_id,
            envelope_attempt_index=envelope_attempt_index,
            canonical_interaction_id=canonical_interaction_id,
            canonical_attempt_index=canonical_attempt_index,
            error_kind=error_kind,
            outcome=outcome,
            retryable=retryable,
            policy_hash=policy.get("policy_hash"),
        )

def _lg_d2_emit_interaction_attempt_events(
    graph_state: _GraphLoopState,
    *,
    stage_id: StageId,
    graph_node: str,
    subgraph_id: str | None,
    policy: dict[str, Any],
    interaction_index: int | None,
    interaction: dict[str, Any] | None,
) -> None:
    attempts = interaction.get("attempts") if isinstance(interaction, dict) else None
    if not isinstance(attempts, list):
        return
    taxonomy = _lg_d2_retryable_taxonomy(policy)
    for index, attempt in enumerate(attempts):
        error_kind = _lg_d2_attempt_error_kind(attempt)
        if not error_kind:
            continue
        _append_lg_d2_envelope_event(
            graph_state,
            event_type="lg_d2_timeout" if error_kind == "timeout" else "lg_d2_retry",
            stage_id=stage_id,
            graph_node=graph_node,
            subgraph_id=subgraph_id,
            policy=policy,
            envelope_attempt_index=0,
            canonical_interaction_id=interaction_index,
            canonical_attempt_index=index,
            error_kind=error_kind,
            retryable=error_kind in taxonomy,
            outcome="inner_attempt_failure_observed",
            safe_summary={"attempt_index": index, "attempt": attempt},
        )

def _lg_d2_wrap_llm_stage_node(
    graph_state: _GraphLoopState,
    *,
    stage_id: StageId,
    graph_node: str,
    subgraph_id: str | None,
    call: Any,
) -> Any:
    """Run one stage-level LLM node under LG-D2 retry/timeout diagnostics envelope.

    The wrapper is deliberately outside the PR-B2 stage adapter.  It records a
    LangGraph-visible enter/exit/retry/exhausted ledger, performs only bounded
    outer retries for provider-like transient exceptions, and keeps the inner
    ``llm_interactions`` attempt ledger canonical.
    """

    runtime_state = graph_state.get("runtime_state")
    policy = build_lg_d2_llm_node_envelope_policy()
    if not isinstance(runtime_state, _RunState) or not bool(policy.get("enabled", True)):
        return call()
    before_count = len(runtime_state.llm_interactions)
    max_attempts = max(1, int(policy.get("max_envelope_attempts") or 1))
    taxonomy = _lg_d2_retryable_taxonomy(policy)
    last_retry_error: dict[str, Any] | None = None
    last_interaction: dict[str, Any] | None = None
    last_error_kind: str | None = None

    for envelope_attempt_index in range(max_attempts):
        _append_lg_d2_envelope_event(
            graph_state,
            event_type="lg_d2_envelope_enter",
            stage_id=stage_id,
            graph_node=graph_node,
            subgraph_id=subgraph_id,
            policy=policy,
            envelope_attempt_index=envelope_attempt_index,
            outcome="enter",
            safe_summary={"before_llm_interaction_count": before_count, "max_envelope_attempts": max_attempts},
        )
        try:
            result = call()
        except _LLMRetryExhausted as exc:
            interaction_index = _lg_d2_latest_interaction_index(runtime_state)
            interaction = runtime_state.llm_interactions[interaction_index] if interaction_index is not None else dict(exc.interaction or {})
            attempt_index = _lg_d2_latest_attempt_index(interaction)
            error_kind = exc.error_kind
            retryable = error_kind in taxonomy
            last_retry_error = dict(exc.retry_error or {})
            last_interaction = dict(interaction or {})
            last_error_kind = error_kind
            exhausted_now = envelope_attempt_index >= max_attempts - 1 or not retryable
            _append_lg_d2_envelope_event(
                graph_state,
                event_type="lg_d2_timeout" if error_kind == "timeout" else ("lg_d2_retry_exhausted" if exhausted_now else "lg_d2_retry"),
                stage_id=stage_id,
                graph_node=graph_node,
                subgraph_id=subgraph_id,
                policy=policy,
                envelope_attempt_index=envelope_attempt_index,
                canonical_interaction_id=interaction_index,
                canonical_attempt_index=attempt_index,
                error_kind=error_kind,
                retryable=retryable,
                outcome="exhausted" if exhausted_now else "retry_planned",
                safe_summary={"retry_error": exc.retry_error, "interaction_hash": _hash_canonical_payload(interaction)},
            )
            if error_kind == "timeout" and exhausted_now:
                _append_lg_d2_envelope_event(
                    graph_state,
                    event_type="lg_d2_retry_exhausted",
                    stage_id=stage_id,
                    graph_node=graph_node,
                    subgraph_id=subgraph_id,
                    policy=policy,
                    envelope_attempt_index=envelope_attempt_index,
                    canonical_interaction_id=interaction_index,
                    canonical_attempt_index=attempt_index,
                    error_kind=error_kind,
                    retryable=retryable,
                    outcome="exhausted",
                    safe_summary={"retry_error": exc.retry_error},
                )
            _append_lg_d2_envelope_event(
                graph_state,
                event_type="lg_d2_envelope_exit",
                stage_id=stage_id,
                graph_node=graph_node,
                subgraph_id=subgraph_id,
                policy=policy,
                envelope_attempt_index=envelope_attempt_index,
                canonical_interaction_id=interaction_index,
                canonical_attempt_index=attempt_index,
                error_kind=error_kind,
                retryable=retryable,
                outcome="exhausted" if exhausted_now else "retry_planned",
                safe_summary={"after_llm_interaction_count": len(runtime_state.llm_interactions)},
            )
            if exhausted_now:
                raise
            continue
        except Exception as exc:
            error_kind = _lg_d2_error_kind_from_exception(exc)
            retryable = _lg_d2_exception_is_provider_retryable(exc, policy)
            if not retryable:
                _append_lg_d2_envelope_event(
                    graph_state,
                    event_type="lg_d2_envelope_exit",
                    stage_id=stage_id,
                    graph_node=graph_node,
                    subgraph_id=subgraph_id,
                    policy=policy,
                    envelope_attempt_index=envelope_attempt_index,
                    error_kind="schema_contract_error",
                    retryable=False,
                    outcome="non_retryable_exception_re_raised",
                    safe_summary={"exception_type": type(exc).__name__, "exception_hash": _hash_text(str(exc))},
                )
                raise

            retry_error = _lg_d2_retry_error_for_exception(stage_id, exc)
            interaction = {
                "stage_id": stage_id.value,
                "provider": "lg-d2-envelope",
                "model_id": "outer-envelope",
                "schema_validation_ok": False,
                "retry_error": retry_error,
                "retry_count": envelope_attempt_index,
                "attempts": [
                    {
                        "status": retry_error["error_kind"],
                        "error_kind": retry_error["error_kind"],
                        "error_message": retry_error["error_message"],
                        "source": "lg_d2_outer_envelope_exception",
                        "envelope_attempt_index": envelope_attempt_index,
                    }
                ],
            }
            last_retry_error = retry_error
            last_interaction = interaction
            last_error_kind = error_kind
            exhausted_now = envelope_attempt_index >= max_attempts - 1
            interaction_index: int | None = None
            canonical_attempt_index: int | None = None
            if exhausted_now:
                # Only unrecovered provider-like envelope failures enter the
                # canonical llm_interactions ledger and invalid-run path.  A
                # transient failure later recovered by the next envelope attempt
                # remains visible in the LG-D2 operator log but must not pollute
                # the canonical successful interaction sequence.
                runtime_state.llm_interactions.append(interaction)
                interaction_index = len(runtime_state.llm_interactions) - 1
                canonical_attempt_index = 0
            _append_lg_d2_envelope_event(
                graph_state,
                event_type="lg_d2_timeout" if error_kind == "timeout" else ("lg_d2_retry_exhausted" if exhausted_now else "lg_d2_retry"),
                stage_id=stage_id,
                graph_node=graph_node,
                subgraph_id=subgraph_id,
                policy=policy,
                envelope_attempt_index=envelope_attempt_index,
                canonical_interaction_id=interaction_index,
                canonical_attempt_index=canonical_attempt_index,
                error_kind=error_kind,
                retryable=True,
                outcome="exhausted" if exhausted_now else "retry_planned",
                safe_summary={"exception_type": type(exc).__name__, "retry_error": retry_error},
            )
            if error_kind == "timeout" and exhausted_now:
                _append_lg_d2_envelope_event(
                    graph_state,
                    event_type="lg_d2_retry_exhausted",
                    stage_id=stage_id,
                    graph_node=graph_node,
                    subgraph_id=subgraph_id,
                    policy=policy,
                    envelope_attempt_index=envelope_attempt_index,
                    canonical_interaction_id=interaction_index,
                    canonical_attempt_index=canonical_attempt_index,
                    error_kind=error_kind,
                    retryable=True,
                    outcome="exhausted",
                    safe_summary={"retry_error": retry_error},
                )
            _append_lg_d2_envelope_event(
                graph_state,
                event_type="lg_d2_envelope_exit",
                stage_id=stage_id,
                graph_node=graph_node,
                subgraph_id=subgraph_id,
                policy=policy,
                envelope_attempt_index=envelope_attempt_index,
                canonical_interaction_id=interaction_index,
                canonical_attempt_index=canonical_attempt_index,
                error_kind=error_kind,
                retryable=True,
                outcome="exhausted" if exhausted_now else "retry_planned",
                safe_summary={"after_llm_interaction_count": len(runtime_state.llm_interactions)},
            )
            if exhausted_now:
                meta = _lg_d2_stage_meta_for_retry_error(stage_id, retry_error)
                _append_stage(runtime_state.stage_records, meta)
                raise _LLMRetryExhausted(stage_id=stage_id.value, retry_error=retry_error, interaction=interaction) from exc
            continue

        interaction_index = len(runtime_state.llm_interactions) - 1 if len(runtime_state.llm_interactions) > before_count else None
        interaction = runtime_state.llm_interactions[interaction_index] if interaction_index is not None else None
        _lg_d2_emit_interaction_attempt_events(
            graph_state,
            stage_id=stage_id,
            graph_node=graph_node,
            subgraph_id=subgraph_id,
            policy=policy,
            interaction_index=interaction_index,
            interaction=interaction,
        )
        _append_lg_d2_envelope_event(
            graph_state,
            event_type="lg_d2_envelope_exit",
            stage_id=stage_id,
            graph_node=graph_node,
            subgraph_id=subgraph_id,
            policy=policy,
            envelope_attempt_index=envelope_attempt_index,
            canonical_interaction_id=interaction_index,
            canonical_attempt_index=_lg_d2_latest_attempt_index(interaction),
            outcome="ok",
            safe_summary={"after_llm_interaction_count": len(runtime_state.llm_interactions)},
        )
        return result

    # Defensive: the loop should either return or raise from the final attempt.
    retry_error = last_retry_error or {"error_kind": last_error_kind or "provider_error", "error_message": f"{stage_id.value} envelope retry exhausted"}
    interaction = last_interaction or {"stage_id": stage_id.value, "retry_error": retry_error, "attempts": []}
    meta = _lg_d2_stage_meta_for_retry_error(stage_id, retry_error)
    _append_stage(runtime_state.stage_records, meta)
    raise _LLMRetryExhausted(stage_id=stage_id.value, retry_error=retry_error, interaction=interaction)

def _lg_d2_event_match_signature(event: dict[str, Any]) -> tuple[str, str, str, str, str, str, str, str, str, str]:
    """Return the reducer-vs-flow-log matching signature for one LG-D2 event.

    This signature intentionally excludes fallback-only fields such as
    ``flow_log_index``.  Normal reducer events do not carry that index, so using
    it for matching would make every flow-log row look missing and duplicate
    LG-D2 evidence in the operator log.
    """

    payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
    return (
        str(event.get("event_type") or ""),
        str(event.get("stage_id") or ""),
        str(payload.get("iteration") if payload.get("iteration") is not None else ""),
        str(event.get("node") or payload.get("graph_node") or ""),
        str(payload.get("subgraph_id") or ""),
        str(payload.get("error_kind") or ""),
        str(payload.get("outcome") or ""),
        str(payload.get("envelope_attempt_index") if payload.get("envelope_attempt_index") is not None else ""),
        str(payload.get("canonical_interaction_id") if payload.get("canonical_interaction_id") is not None else ""),
        str(payload.get("canonical_attempt_index") if payload.get("canonical_attempt_index") is not None else ""),
    )

def _lg_d2_flow_log_match_signature(row: dict[str, Any], *, event_type: str, stage_id: StageId, graph_node: str) -> tuple[str, str, str, str, str, str, str, str, str, str]:
    graph_subgraph = row.get("graph_subgraph")
    subgraph_id = None if graph_subgraph in {None, "<none>", ""} else str(graph_subgraph)
    return (
        event_type,
        stage_id.value,
        str(row.get("iteration") if row.get("iteration") is not None else ""),
        graph_node,
        str(subgraph_id or ""),
        str(row.get("error_kind") or ""),
        str(row.get("outcome") or ""),
        str(row.get("envelope_attempt_index") if row.get("envelope_attempt_index") is not None else ""),
        str(row.get("canonical_interaction_id") if row.get("canonical_interaction_id") is not None else ""),
        str(row.get("canonical_attempt_index") if row.get("canonical_attempt_index") is not None else ""),
    )

def _lg_d2_fallback_unique_signature(row: dict[str, Any], *, flow_index: int, event_type: str, stage_id: StageId, graph_node: str) -> tuple[str, str, str, str, str, str, str, str, str, str, str]:
    return (*_lg_d2_flow_log_match_signature(row, event_type=event_type, stage_id=stage_id, graph_node=graph_node), str(flow_index))

def _lg_d2_operator_events_from_flow_logs(record: Any, *, existing_events: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    """Recover LG-D2 envelope events from canonical flow logs if graph updates drop them.

    LangGraph does not commit a node's reducer-channel update when an inner
    subgraph raises before returning a ``Command``.  The human/academic flow log
    is still appended on the shared ``_RunState`` before the exception is
    converted into an invalid run.  Reconstructing sanitized LG-D2 operator
    events from that canonical log prevents retry-exhausted/timeout evidence
    from disappearing after an upstream merge or checkpoint/resume path, without
    changing stage order, retry semantics, prompts, or the inner PR-B2 attempt
    ledger.

    Normal non-exception paths already contain LG-D2 events in graph-state
    reducer updates.  The signature check below therefore treats flow-log
    recovery as a gap-filler, not a second source of duplicate evidence.
    """

    policy = build_lg_d2_llm_node_envelope_policy()
    events: list[dict[str, Any]] = []
    existing_counts = Counter(
        _lg_d2_event_match_signature(event)
        for event in (existing_events or [])
        if isinstance(event, dict) and str(event.get("event_type") or "") in LG_D2_LLM_NODE_ENVELOPE_EVENT_TYPES
    )
    fallback_seen: set[tuple[str, str, str, str, str, str, str, str, str, str, str]] = set()
    for flow_index, row in enumerate(getattr(record, "logs", []) or []):
        if not isinstance(row, dict):
            continue
        event_type = str(row.get("event") or "")
        if event_type not in LG_D2_LLM_NODE_ENVELOPE_EVENT_TYPES:
            continue
        stage_text = str(row.get("stage_id") or "")
        try:
            stage_id = StageId(stage_text)
        except Exception:
            continue
        graph_node = str(row.get("graph_node") or "") or None
        graph_subgraph = row.get("graph_subgraph")
        subgraph_id = None if graph_subgraph in {None, "<none>", ""} else str(graph_subgraph)
        graph_node_text = graph_node or "unknown_lg_d2_flow_log_node"
        match_signature = _lg_d2_flow_log_match_signature(row, event_type=event_type, stage_id=stage_id, graph_node=graph_node_text)
        fallback_signature = _lg_d2_fallback_unique_signature(
            row,
            flow_index=flow_index,
            event_type=event_type,
            stage_id=stage_id,
            graph_node=graph_node_text,
        )
        if existing_counts[match_signature] > 0:
            existing_counts[match_signature] -= 1
            continue
        if fallback_signature in fallback_seen:
            continue
        event = _lg_d2_envelope_event(
            run_id=str(record.run_id),
            event_type=event_type,
            stage_id=stage_id,
            graph_node=graph_node_text,
            subgraph_id=subgraph_id,
            policy=policy,
            iteration=row.get("iteration") if isinstance(row.get("iteration"), int) else None,
            envelope_attempt_index=int(row.get("envelope_attempt_index") or 0),
            canonical_interaction_id=row.get("canonical_interaction_id") if isinstance(row.get("canonical_interaction_id"), int) else None,
            canonical_attempt_index=row.get("canonical_attempt_index") if isinstance(row.get("canonical_attempt_index"), int) else None,
            error_kind=row.get("error_kind"),
            retryable=row.get("retryable") if isinstance(row.get("retryable"), bool) else None,
            outcome=row.get("outcome"),
            safe_summary={
                "source": "record.logs fallback",
                "flow_log_index": flow_index,
                "policy_hash": row.get("policy_hash"),
                "merge_conflict_resilient_recovery": True,
            },
        )
        # Preserve the original flow-log timestamp where possible so JSONL order
        # stays close to the terminal replay log; schema remains LG-D1-compatible.
        if isinstance(row.get("ts"), str):
            event["timestamp"] = row["ts"]
        events.append(event)
        fallback_seen.add(fallback_signature)
    return events

