"""LG-C2 deterministic context-engineering subgraph helpers.

This subgraph assembles prompt context, budget metadata, and redaction guards;
it never calls providers and never owns validation/repair/waiver orchestration.
"""

from __future__ import annotations

import re
from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from method.langgraph.instrumentation.common import _hash_payload
from method.llm_stages import LLMStageConfig, estimate_prompt_tokens
from method.stages.ids import StageId

LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION = "lg-c2.context-subgraph.v1"

LG_C2_CONTEXT_SUBGRAPH_ID = "context_engineering_subgraph"

LG_C2_CONTEXT_INSTRUMENTATION_LAYER = "langgraph_context_engineering"

LG_C2_CONTEXT_NODE_IDS = [
    "context_evidence_collect",
    "context_budget_gate",
    "context_compact_full_select",
    "context_redaction_guard",
]

LG_C2_CANONICAL_RECORD_FIELD = "AgentLoopRunRecord.llm_interactions[].context_engineering"

class _LG_C2_ContextState(TypedDict, total=False):
    stage_id: str
    payload_candidates: list[tuple[str, dict[str, Any]]]
    prompt_char_counts: dict[str, int]
    prompt_token_estimates: dict[str, int]
    prompt_messages_by_level: dict[str, list[dict[str, str]]]
    budget_metadata_by_level: dict[str, dict[str, Any]]
    selected_level: str
    selected_payload: dict[str, Any]
    selected_prompt_messages: list[dict[str, str]]
    selected_payload_hash: str
    selected_prompt_messages_hash: str
    selection_reason: str
    redaction_guard: dict[str, Any]
    node_trace: list[dict[str, Any]]

class LG_C2_ContextRedactionBlocked(RuntimeError):
    """Raised before provider calls when LG-C2 context redaction guard blocks payload."""

    def __init__(self, *, stage_id: str, payload_hash: str, guard: dict[str, Any]) -> None:
        self.stage_id = stage_id
        self.payload_hash = payload_hash
        self.guard = dict(guard)
        super().__init__(
            "LG-C2 context redaction guard blocked secret-like prompt context before provider call "
            f"for {stage_id}; payload_hash={payload_hash}"
        )

class LG_C2_ContextAssemblyResult:
    """Prompt context selected by the LG-C2 context-engineering subgraph."""

    def __init__(self, payload: dict[str, Any], metadata: dict[str, Any], prompt_messages: list[dict[str, str]]) -> None:
        self.payload = payload
        self.metadata = metadata
        self.prompt_messages = prompt_messages

def build_lg_c2_context_subgraph_contract() -> dict[str, Any]:
    """Return the auditable LG-C2 context subgraph contract.

    The subgraph is intentionally an instrumentation / context-assembly layer:
    it chooses between existing full/compact prompt payloads and records budget,
    hash, and redaction-guard provenance.  It does not alter FixLog, NFRR,
    eligibility, stage verdict sources, or E1/E2 model-quality fields.
    """

    return {
        "schema_version": LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION,
        "subgraph_id": LG_C2_CONTEXT_SUBGRAPH_ID,
        "instrumentation_layer": LG_C2_CONTEXT_INSTRUMENTATION_LAYER,
        "node_ids": list(LG_C2_CONTEXT_NODE_IDS),
        "stage_ids": [StageId.SL_9_REPAIR.value, StageId.SL_10_REPAIR_REVIEW.value],
        "canonical_record_field": LG_C2_CANONICAL_RECORD_FIELD,
        "payload_hash_fields": [
            "stage_id",
            "compaction_level",
            "selected_payload_hash",
            "selected_prompt_messages_hash",
            "budget_metadata",
            "redaction_guard",
        ],
        "budget_metadata_required": [
            "prompt_chars",
            "estimated_prompt_tokens",
            "prompt_token_budget",
            "prompt_token_estimator",
            "chars_per_token_estimate",
            "compaction_level",
            "prompt_compaction_applied",
            "compact_only_when_over_budget",
            "budget_exceeded",
        ],
        "redaction_guard_before_provider": True,
        "redaction_guard_policy": "hash-and-fail-closed-on-secret-like-context-fields",
        "no_sample_specific_behavior": True,
        "does_not_replace_academic_evidence": True,
        "academic_evidence_sources_preserved": [
            "AgentLoopRunRecord.fix_log",
            "AgentLoopRunRecord.repair_history",
            "AgentLoopRunRecord.llm_interactions",
            "AgentLoopRunRecord.final_artifacts",
            "NFRR/eligibility fields",
        ],
    }

def _lg_c2_prompt_budget_metadata(
    *,
    stage_id: str,
    prompt_messages: list[dict[str, str]],
    cfg: LLMStageConfig,
    compaction_level: str,
) -> dict[str, Any]:
    prompt_chars = sum(len(str(message.get("content", ""))) for message in prompt_messages)
    estimated_tokens = estimate_prompt_tokens(
        prompt_messages,
        estimator=cfg.prompt_token_estimator,
        chars_per_token=cfg.prompt_chars_per_token,
        model=cfg.model,
    )
    budget = cfg.max_prompt_tokens
    return {
        "stage_id": stage_id,
        "prompt_chars": prompt_chars,
        "estimated_prompt_tokens": estimated_tokens,
        "prompt_token_budget": budget,
        "prompt_token_estimator": cfg.prompt_token_estimator,
        "chars_per_token_estimate": cfg.prompt_chars_per_token,
        "compaction_level": compaction_level,
        "prompt_compaction_applied": compaction_level != "none",
        "compact_only_when_over_budget": True,
        "budget_exceeded": estimated_tokens > budget if budget is not None else False,
    }

def _lg_c2_within_prompt_budget(prompt_messages: list[dict[str, str]], cfg: LLMStageConfig) -> bool:
    if cfg.max_prompt_tokens is None:
        return True
    return (
        estimate_prompt_tokens(
            prompt_messages,
            estimator=cfg.prompt_token_estimator,
            chars_per_token=cfg.prompt_chars_per_token,
            model=cfg.model,
        )
        <= cfg.max_prompt_tokens
    )

def _lg_c2_secret_like_field_detected(value: Any) -> bool:
    """Conservative guard for obvious secret-like context fields.

    This is intentionally sample-agnostic and only flags credential-shaped keys or
    values.  Raw provider keys are never written into the metadata; callers can
    use the boolean/hash-only status to fail closed if future context surfaces
    become unsafe.
    """

    secret_key_re = re.compile(r"(api[_-]?key|token|secret|password|credential|authorization)", re.IGNORECASE)
    secret_value_re = re.compile(r"(sk-[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{12,}|LLM_API_KEY\s*=)")

    def walk(item: Any, path: str = "payload") -> bool:
        if isinstance(item, dict):
            for key, nested in item.items():
                key_text = str(key)
                if secret_key_re.search(key_text):
                    return True
                if walk(nested, f"{path}.{key_text}"):
                    return True
        elif isinstance(item, (list, tuple, set)):
            for index, nested in enumerate(item):
                if walk(nested, f"{path}[{index}]"):
                    return True
        elif isinstance(item, str) and secret_value_re.search(item):
            return True
        return False

    return walk(value)

def _build_lg_c2_context_subgraph(*, prompt_builder: Any, cfg: LLMStageConfig):
    """Build the LG-C2 context-engineering subgraph.

    The graph nodes are deliberately small and deterministic: evidence collect
    builds candidate prompts, budget gate computes estimates, compact/full select
    chooses the first candidate inside budget (or the compact fallback), and
    redaction guard emits a hash-only safety summary.
    """

    graph = StateGraph(_LG_C2_ContextState)

    def evidence_collect(state: _LG_C2_ContextState) -> _LG_C2_ContextState:
        candidates = list(state.get("payload_candidates") or [])
        prompts = {level: prompt_builder(payload) for level, payload in candidates}
        return {
            **state,
            "prompt_messages_by_level": prompts,
            "node_trace": [
                *list(state.get("node_trace") or []),
                {
                    "node_id": "context_evidence_collect",
                    "candidate_levels": [level for level, _ in candidates],
                    "candidate_count": len(candidates),
                },
            ],
        }

    def budget_gate(state: _LG_C2_ContextState) -> _LG_C2_ContextState:
        prompts = dict(state.get("prompt_messages_by_level") or {})
        budget_by_level = {
            level: _lg_c2_prompt_budget_metadata(
                stage_id=str(state.get("stage_id") or ""),
                prompt_messages=messages,
                cfg=cfg,
                compaction_level=level,
            )
            for level, messages in prompts.items()
        }
        return {
            **state,
            "budget_metadata_by_level": budget_by_level,
            "prompt_char_counts": {level: meta["prompt_chars"] for level, meta in budget_by_level.items()},
            "prompt_token_estimates": {level: meta["estimated_prompt_tokens"] for level, meta in budget_by_level.items()},
            "node_trace": [
                *list(state.get("node_trace") or []),
                {
                    "node_id": "context_budget_gate",
                    "prompt_token_budget": cfg.max_prompt_tokens,
                    "prompt_token_estimates": {level: meta["estimated_prompt_tokens"] for level, meta in budget_by_level.items()},
                },
            ],
        }

    def compact_full_select(state: _LG_C2_ContextState) -> _LG_C2_ContextState:
        candidates = list(state.get("payload_candidates") or [])
        prompts = dict(state.get("prompt_messages_by_level") or {})
        selected_level = candidates[-1][0]
        selected_payload = candidates[-1][1]
        selected_prompt = prompts[selected_level]
        selection_reason = "fallback_compact_over_budget"
        for level, payload in candidates:
            prompt = prompts[level]
            selected_level, selected_payload, selected_prompt = level, payload, prompt
            if _lg_c2_within_prompt_budget(prompt, cfg):
                selection_reason = "within_budget"
                break
        return {
            **state,
            "selected_level": selected_level,
            "selected_payload": selected_payload,
            "selected_prompt_messages": selected_prompt,
            "selected_payload_hash": _hash_payload(selected_payload),
            "selected_prompt_messages_hash": _hash_payload(selected_prompt),
            "selection_reason": selection_reason,
            "node_trace": [
                *list(state.get("node_trace") or []),
                {
                    "node_id": "context_compact_full_select",
                    "selected_level": selected_level,
                    "selection_reason": selection_reason,
                    "selected_payload_hash": _hash_payload(selected_payload),
                    "selected_prompt_messages_hash": _hash_payload(selected_prompt),
                },
            ],
        }

    def redaction_guard(state: _LG_C2_ContextState) -> _LG_C2_ContextState:
        selected_payload = dict(state.get("selected_payload") or {})
        selected_prompt = list(state.get("selected_prompt_messages") or [])
        secret_like = _lg_c2_secret_like_field_detected(
            {
                "selected_payload": selected_payload,
                "selected_prompt_messages": selected_prompt,
            }
        )
        guard = {
            "status": "blocked" if secret_like else "passed",
            "secret_like_field_detected": secret_like,
            "policy": "hash_only_metadata_no_raw_secret_persistence",
            "checked_before_provider": True,
            "payload_hash": str(state.get("selected_payload_hash") or ""),
            "prompt_messages_hash": str(state.get("selected_prompt_messages_hash") or ""),
        }
        return {
            **state,
            "redaction_guard": guard,
            "node_trace": [
                *list(state.get("node_trace") or []),
                {
                    "node_id": "context_redaction_guard",
                    "status": guard["status"],
                    "secret_like_field_detected": secret_like,
                    "payload_hash": guard["payload_hash"],
                },
            ],
        }

    graph.add_node("context_evidence_collect", evidence_collect)
    graph.add_node("context_budget_gate", budget_gate)
    graph.add_node("context_compact_full_select", compact_full_select)
    graph.add_node("context_redaction_guard", redaction_guard)
    graph.add_edge(START, "context_evidence_collect")
    graph.add_edge("context_evidence_collect", "context_budget_gate")
    graph.add_edge("context_budget_gate", "context_compact_full_select")
    graph.add_edge("context_compact_full_select", "context_redaction_guard")
    graph.add_edge("context_redaction_guard", END)
    return graph.compile(checkpointer=False)

def assemble_lg_c2_prompt_context(
    *,
    stage_id: str,
    payload_candidates: list[tuple[str, dict[str, Any]]],
    prompt_builder: Any,
    cfg: LLMStageConfig,
) -> LG_C2_ContextAssemblyResult:
    """Select an SL-9/SL-10 prompt payload through the LG-C2 context subgraph."""

    if not payload_candidates:
        raise ValueError("LG-C2 context subgraph requires at least one payload candidate")
    app = _build_lg_c2_context_subgraph(prompt_builder=prompt_builder, cfg=cfg)
    final_state = app.invoke({"stage_id": stage_id, "payload_candidates": payload_candidates, "node_trace": []})
    selected_level = str(final_state["selected_level"])
    selected_payload = dict(final_state["selected_payload"])
    selected_prompt = list(final_state["selected_prompt_messages"])
    budget_metadata = dict(final_state["budget_metadata_by_level"][selected_level])
    guard = dict(final_state["redaction_guard"])
    metadata = {
        **budget_metadata,
        "context_engineering_schema_version": LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION,
        "subgraph_id": LG_C2_CONTEXT_SUBGRAPH_ID,
        "instrumentation_layer": LG_C2_CONTEXT_INSTRUMENTATION_LAYER,
        "stage_id": stage_id,
        "compaction_level": selected_level,
        "selection_reason": str(final_state["selection_reason"]),
        "selected_payload_hash": str(final_state["selected_payload_hash"]),
        "prompt_payload_hash": str(final_state["selected_payload_hash"]),
        "selected_prompt_messages_hash": str(final_state["selected_prompt_messages_hash"]),
        "budget_metadata": budget_metadata,
        "redaction_guard": guard,
        "redaction_guard_fail_closed": guard.get("status") == "blocked",
        "node_trace": list(final_state.get("node_trace") or []),
        "node_ids": list(LG_C2_CONTEXT_NODE_IDS),
        "canonical_record_field": LG_C2_CANONICAL_RECORD_FIELD,
        "context_subgraph_contract_hash": _hash_payload(build_lg_c2_context_subgraph_contract()),
        "does_not_replace_academic_evidence": True,
    }
    if guard.get("status") == "blocked":
        raise LG_C2_ContextRedactionBlocked(
            stage_id=stage_id,
            payload_hash=str(final_state["selected_payload_hash"]),
            guard={
                **guard,
                "context_engineering_schema_version": LG_C2_CONTEXT_SUBGRAPH_SCHEMA_VERSION,
                "subgraph_id": LG_C2_CONTEXT_SUBGRAPH_ID,
                "canonical_record_field": LG_C2_CANONICAL_RECORD_FIELD,
                "node_trace_hash": _hash_payload(metadata["node_trace"]),
            },
        )
    return LG_C2_ContextAssemblyResult(selected_payload, metadata, selected_prompt)

