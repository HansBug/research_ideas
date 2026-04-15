from __future__ import annotations

import json
import re

from langchain_openai import ChatOpenAI

from .expert_review_prompts import AGENT_SYSTEM_PROMPT, render_dimension_guidance, render_request_prompt
from .expert_review_rubrics import resolve_review_profile
from .expert_review_schema import (
    DimensionReviewResult,
    ElementIssue,
    EvidenceItem,
    ExpertReviewRequest,
    ExpertReviewResult,
    RequirementTraceResult,
    TraceLink,
    dimension_review_from_dict,
    element_issue_from_dict,
    evidence_item_from_dict,
    judgement_from_score,
    requirement_trace_from_dict,
    to_dict,
)
from .expert_review_tools import (
    RequirementItem,
    build_requirement_trace,
    compute_set_match,
    extract_model_inventory,
    machine_elements_from_payload,
    merge_inventory,
    parse_json_payload,
    parse_requirement_items,
)
from .expert_review_utils import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER_ORDER,
    PROVIDER_CONFIGS,
    count_machine_components,
    ensure_json,
    normalize_machine,
    resolve_api_env,
)


def _content_to_text(content: object) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if isinstance(text, str):
                parts.append(text)
            else:
                parts.append(str(item))
        return "".join(parts)
    return "" if content is None else str(content)


def _invoke_llm_text(
    llm: ChatOpenAI,
    messages: list[tuple[str, str]],
    *,
    json_mode: bool = False,
) -> str:
    runnable = llm.bind(response_format={"type": "json_object"}) if json_mode else llm
    try:
        response = runnable.invoke(messages)
        text = _content_to_text(getattr(response, "content", response)).strip()
        if text:
            return text
    except Exception:
        pass
    chunks: list[str] = []
    for chunk in runnable.stream(messages):
        text = _content_to_text(getattr(chunk, "content", chunk))
        if text:
            chunks.append(text)
    return "".join(chunks).strip()


class ExpertReviewAgent:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        provider_order: list[str] | None = None,
        temperature: float = 0.0,
        timeout: int = 180,
    ) -> None:
        self.model_name = model
        self.provider_order = provider_order or list(DEFAULT_PROVIDER_ORDER)
        self.temperature = temperature
        self.timeout = timeout
        self._provider_key, self._llm = self._build_llm()

    def _build_llm(self) -> tuple[str | None, ChatOpenAI | None]:
        env = resolve_api_env()
        for provider_key in self.provider_order:
            provider = PROVIDER_CONFIGS.get(provider_key)
            if provider is None:
                continue
            api_key = None
            for env_key in provider["env_keys"]:
                api_key = env.get(env_key)
                if api_key:
                    break
            if not api_key:
                continue
            try:
                llm = ChatOpenAI(
                    model=self.model_name,
                    api_key=api_key,
                    base_url=provider["base_url"],
                    temperature=self.temperature,
                    timeout=self.timeout,
                    max_retries=0,
                )
                return provider_key, llm
            except Exception:
                continue
        return None, None

    def review(self, request: ExpertReviewRequest) -> ExpertReviewResult:
        if self._llm is None:
            return heuristic_expert_review(request)
        try:
            llm_result = llm_primary_review(self._llm, self.model_name, self._provider_key, request)
            heuristic_result = heuristic_expert_review(request, llm=self._llm)
            return _blend_architecture_result(request, llm_result, heuristic_result)
        except Exception as exc:
            result = heuristic_expert_review(request, llm=self._llm)
            result.notes.append(f"LLM primary review failed: {type(exc).__name__}: {exc}")
            return result


def _score_from_match(match_result: dict[str, object], fallback: float = 0.5) -> float:
    metrics = match_result.get("metrics", {})
    if isinstance(metrics, dict) and "f1" in metrics:
        return float(metrics["f1"])
    return fallback


def _head(items: list[str], limit: int = 8) -> list[str]:
    return [str(item) for item in items[:limit]]


GENERIC_STATE_NAME_TOKENS = {
    "idle",
    "start",
    "end",
    "state",
    "state1",
    "state2",
    "processing",
    "process",
    "waiting",
    "wait",
    "ready",
    "init",
    "initial",
    "final",
    "working",
    "running",
    "loop",
}

INPUT_STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "that",
    "this",
    "from",
    "into",
    "when",
    "where",
    "which",
    "while",
    "then",
    "will",
    "have",
    "has",
    "are",
    "must",
    "should",
    "than",
    "less",
    "more",
    "also",
    "other",
    "about",
    "according",
    "system",
    "information",
}

GENERIC_BLOCK_NAME_TOKENS = {
    "message",
    "frame",
    "data",
    "info",
    "information",
    "payload",
    "object",
    "block",
    "component",
}


def _artifact_excerpt(text: str | None, max_chars: int = 2800) -> str:
    if not text:
        return "[not provided]"
    stripped = text.strip()
    if len(stripped) <= max_chars:
        return stripped
    remaining = len(stripped) - max_chars
    return f"{stripped[:max_chars]}\n...[truncated {remaining} chars]"


def _tokenize_text(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    spaced = spaced.replace("_", " ")
    return [token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9]*", spaced)]


def _exact_state_names(artifact_text: str | None, inventory: dict[str, object], limit: int = 50) -> list[str]:
    payload = parse_json_payload(artifact_text)
    if isinstance(payload, dict):
        machine = normalize_machine(payload)
        result: list[str] = []
        for state in machine.get("states", []):
            name = str(state.get("name", "")).strip()
            if name and name not in result:
                result.append(name)
            if len(result) >= limit:
                return result
        if result:
            return result
    return _state_name_head(inventory, limit=limit)


def _exact_block_names(artifact_text: str | None, inventory: dict[str, object], limit: int = 50) -> list[str]:
    payload = parse_json_payload(artifact_text)
    if isinstance(payload, dict):
        machine = normalize_machine(payload)
        result: list[str] = []
        for block in machine.get("blocks", []):
            name = str(block.get("name", "")).strip()
            if name and name not in result:
                result.append(name)
            if len(result) >= limit:
                return result
        if result:
            return result
    return _block_name_head(inventory, limit=limit)


def _state_name_head(inventory: dict[str, object], limit: int = 20) -> list[str]:
    result: list[str] = []
    for raw in inventory.get("states", []):
        name = str(raw).split("|", 1)[0].strip()
        if name and name not in result:
            result.append(name)
        if len(result) >= limit:
            break
    return result


def _block_name_head(inventory: dict[str, object], limit: int = 20) -> list[str]:
    result: list[str] = []
    for raw in inventory.get("blocks", []):
        name = str(raw).strip()
        if name and name not in result:
            result.append(name)
        if len(result) >= limit:
            break
    return result


def _state_name_quality_summary(input_text: str, artifact_text: str | None, inventory: dict[str, object]) -> dict[str, object]:
    input_tokens = {
        token
        for token in _tokenize_text(input_text)
        if len(token) >= 4 and token not in INPUT_STOPWORDS
    }
    domain_specific: list[str] = []
    generic_placeholder: list[str] = []
    exact_states = _exact_state_names(artifact_text, inventory)
    for name in exact_states:
        tokens = [token.lower() for token in _tokenize_text(name)]
        if not tokens:
            continue
        if any(token in GENERIC_STATE_NAME_TOKENS or re.fullmatch(r"state\d+", token) for token in tokens):
            generic_placeholder.append(name)
            continue
        if any(token in input_tokens for token in tokens):
            domain_specific.append(name)
    return {
        "domain_specific_state_examples": domain_specific[:8],
        "generic_or_placeholder_state_examples": generic_placeholder[:8],
        "state_name_count": len(exact_states),
    }


def _block_name_quality_summary(input_text: str, artifact_text: str | None, inventory: dict[str, object]) -> dict[str, object]:
    input_tokens = {
        token
        for token in _tokenize_text(input_text)
        if len(token) >= 4 and token not in INPUT_STOPWORDS
    }
    domain_specific: list[str] = []
    generic_data_like: list[str] = []
    seen = _exact_block_names(artifact_text, inventory)
    for name in seen:
        tokens = [token.lower() for token in _tokenize_text(name)]
        if not tokens:
            continue
        if any(token in GENERIC_BLOCK_NAME_TOKENS for token in tokens):
            generic_data_like.append(name)
        if any(token in input_tokens for token in tokens):
            domain_specific.append(name)
    return {
        "domain_specific_block_examples": domain_specific[:8],
        "generic_data_like_block_examples": generic_data_like[:8],
        "block_name_count": len(seen),
        "signal_count": len(list(inventory.get("signals", []))),
    }


def _compact_inventory_side(inventory: dict[str, object], counts: dict[str, object]) -> dict[str, object]:
    return {
        "counts": counts,
        "blocks": _head(list(inventory.get("blocks", [])), 10),
        "signals": _head(list(inventory.get("signals", [])), 12),
        "states": _head(list(inventory.get("states", [])), 14),
        "transitions": _head(list(inventory.get("transitions", [])), 14),
        "rules": _head(list(inventory.get("rules", [])), 8),
    }


def _compact_requirement_context(requirement_results: list[RequirementTraceResult]) -> dict[str, object]:
    matched = [item for item in requirement_results if item.status == "matched"]
    partial = [item for item in requirement_results if item.status == "partial"]
    missing = [item for item in requirement_results if item.status == "missing"]
    return {
        "matched_count": len(matched),
        "partial_count": len(partial),
        "missing_count": len(missing),
        "sample_matched": [
            {
                "requirement_id": item.requirement_id,
                "requirement_text": item.requirement_text,
                "matched_element_ids": item.matched_element_ids[:3],
            }
            for item in matched[:5]
        ],
        "sample_partial": [
            {
                "requirement_id": item.requirement_id,
                "requirement_text": item.requirement_text,
                "matched_element_ids": item.matched_element_ids[:3],
            }
            for item in partial[:5]
        ],
        "sample_missing_ids": [item.requirement_id for item in missing[:3]],
    }


def _compact_precomputed_context(
    input_text: str,
    inventory: dict[str, object],
    requirement_results: list[RequirementTraceResult],
    unsupported: list[ElementIssue],
    pred_artifact_text: str | None = None,
) -> dict[str, object]:
    return {
        "prediction_summary": _compact_inventory_side(
            inventory["prediction_inventory"],
            dict(inventory.get("prediction_counts", {})),
        ),
        "prediction_state_name_quality": _state_name_quality_summary(
            input_text,
            pred_artifact_text,
            inventory["prediction_inventory"],
        ),
        "prediction_block_name_quality": _block_name_quality_summary(
            input_text,
            pred_artifact_text,
            inventory["prediction_inventory"],
        ),
        "reference_summary": _compact_inventory_side(
            inventory["reference_inventory"],
            dict(inventory.get("reference_counts", {})),
        ),
        "requirement_trace_summary": _compact_requirement_context(requirement_results),
        "unsupported_model_elements": [to_dict(item) for item in unsupported[:8]],
    }


def _dimension_evidence_summary(dimension_results: list[DimensionReviewResult]) -> list[EvidenceItem]:
    items: list[EvidenceItem] = []
    for dimension in dimension_results:
        items.extend(dimension.evidence[:1])
    return items[:8]


def _clip01(value: float) -> float:
    return max(0.0, min(1.0, value))


def _apply_dimension_delta(
    dimension_results: list[DimensionReviewResult],
    dimension_name: str,
    delta: float,
) -> None:
    for item in dimension_results:
        if item.dimension_name != dimension_name:
            continue
        item.score = round(_clip01(item.score + delta), 6)
        item.judgement = judgement_from_score(item.score)
        break


def _apply_generic_grounding_calibration(
    request: ExpertReviewRequest,
    inventory: dict[str, object],
    dimension_results: list[DimensionReviewResult],
) -> list[str]:
    notes: list[str] = []
    pred_inventory = inventory["prediction_inventory"]
    pred_counts = dict(inventory.get("prediction_counts", {}))
    explicit_state_count = int(pred_counts.get("state_count", 0) or 0)
    explicit_transition_count = int(pred_counts.get("transition_count", 0) or 0)
    if explicit_state_count >= 6 and explicit_transition_count >= 6:
        state_quality = _state_name_quality_summary(request.input_text, request.pred_output, pred_inventory)
        domain_count = len(state_quality["domain_specific_state_examples"])
        generic_count = len(state_quality["generic_or_placeholder_state_examples"])
        state_count = int(state_quality["state_name_count"])
        if state_count >= 6:
            if domain_count >= 6 and domain_count >= generic_count + 3:
                _apply_dimension_delta(dimension_results, "semantic_completeness", 0.16)
                _apply_dimension_delta(dimension_results, "behavioral_consistency", 0.16)
                _apply_dimension_delta(dimension_results, "requirement_traceability", 0.16)
                _apply_dimension_delta(dimension_results, "pragmatic_clarity", 0.08)
                notes.append(
                    "Applied generic semantic-grounding boost because the model contains many domain-specific state names and comparatively few placeholder states."
                )
            elif generic_count >= domain_count + 2 and generic_count >= 4:
                _apply_dimension_delta(dimension_results, "semantic_completeness", -0.10)
                _apply_dimension_delta(dimension_results, "behavioral_consistency", -0.10)
                _apply_dimension_delta(dimension_results, "requirement_traceability", -0.08)
                _apply_dimension_delta(dimension_results, "pragmatic_clarity", -0.08)
                notes.append(
                    "Applied generic placeholder-state penalty because the model relies heavily on generic state names relative to requirement-grounded state names."
                )

    block_quality = _block_name_quality_summary(request.input_text, request.pred_output, pred_inventory)
    domain_block_count = len(block_quality["domain_specific_block_examples"])
    generic_data_block_count = len(block_quality["generic_data_like_block_examples"])
    block_count = int(block_quality["block_name_count"])
    signal_count = int(block_quality["signal_count"])
    if block_count >= 4 and explicit_state_count < 4 and explicit_transition_count < 4:
        if domain_block_count >= 5 and signal_count >= 1:
            _apply_dimension_delta(dimension_results, "semantic_completeness", 0.20)
            _apply_dimension_delta(dimension_results, "behavioral_consistency", 0.15)
            _apply_dimension_delta(dimension_results, "requirement_traceability", 0.18)
            _apply_dimension_delta(dimension_results, "pragmatic_clarity", 0.10)
            notes.append(
                "Applied generic architecture-grounding boost because the model contains many requirement-grounded block names and explicit interactions."
            )
        elif block_count >= 6 and signal_count == 0:
            _apply_dimension_delta(dimension_results, "semantic_completeness", -0.12)
            _apply_dimension_delta(dimension_results, "behavioral_consistency", -0.10)
            _apply_dimension_delta(dimension_results, "requirement_traceability", -0.08)
            _apply_dimension_delta(dimension_results, "pragmatic_clarity", -0.10)
            notes.append(
                "Applied generic architecture penalty because the model contains many blocks but almost no explicit interactions."
            )
    return notes


def _architecture_blend_weight(request: ExpertReviewRequest) -> float | None:
    inventory = extract_model_inventory(
        request.pred_output,
        request.pred_output,
        request.ref_output,
        request.ref_output,
    )
    pred_counts = dict(inventory.get("prediction_counts", {}))
    state_count = int(pred_counts.get("state_count", 0) or 0)
    transition_count = int(pred_counts.get("transition_count", 0) or 0)
    block_count = len(list(inventory["prediction_inventory"].get("blocks", [])))
    signal_count = len(list(inventory["prediction_inventory"].get("signals", [])))
    if block_count < 4 or state_count >= 4 or transition_count >= 4:
        return None
    block_quality = _block_name_quality_summary(request.input_text, inventory["prediction_inventory"])
    domain_block_count = len(block_quality["domain_specific_block_examples"])
    if signal_count == 0:
        return 0.75
    if signal_count >= 3 and domain_block_count >= 5:
        return 0.25
    return 0.5


def _blend_architecture_result(
    request: ExpertReviewRequest,
    llm_result: ExpertReviewResult,
    heuristic_result: ExpertReviewResult,
) -> ExpertReviewResult:
    llm_weight = _architecture_blend_weight(request)
    if llm_weight is None:
        return llm_result
    heuristic_weight = 1.0 - llm_weight
    blended_score = _clip01(llm_result.overall_score * llm_weight + heuristic_result.overall_score * heuristic_weight)
    llm_result.overall_score = round(blended_score, 6)
    llm_result.overall_judgement = judgement_from_score(blended_score)
    llm_result.overall_reason_text = (
        llm_result.overall_reason_text
        + f" Final overall score blended LLM judgement ({llm_weight:.2f}) with a deterministic architecture-oriented reviewer ({heuristic_weight:.2f}) for stability."
    )
    llm_result.notes.append(
        f"Applied architecture stability blend: llm_weight={llm_weight:.2f}, heuristic_weight={heuristic_weight:.2f}."
    )
    return llm_result


def _requirement_results(requirements: list[RequirementItem], inventory: dict[str, object]) -> list[RequirementTraceResult]:
    traces = build_requirement_trace(requirements, inventory.get("prediction_inventory", {}))
    results: list[RequirementTraceResult] = []
    for trace in traces:
        matches = trace["matches"]
        status = trace["status"]
        if status == "matched":
            reason = (
                f"Requirement {trace['requirement_id']} is supported by "
                f"{len(matches)} predicted element(s), including {matches[0]['element_text']}."
            )
            confidence = 0.7
        elif status == "partial":
            reason = (
                f"Requirement {trace['requirement_id']} has only limited lexical support in the prediction; "
                "manual semantic confirmation is still needed."
            )
            confidence = 0.5
        else:
            reason = (
                f"No clear predicted element could be traced to requirement {trace['requirement_id']}; "
                "this likely indicates an omission or a naming mismatch."
            )
            confidence = 0.45
        results.append(
            RequirementTraceResult(
                requirement_id=trace["requirement_id"],
                requirement_text=trace["requirement_text"],
                status=status,
                matched_element_ids=[item["element_text"] for item in matches[:6]],
                reason_text=reason,
                confidence=confidence,
            )
        )
    return results


ARTIFACT_EXTRACTION_SYSTEM_PROMPT = """
You extract model elements from arbitrary software modeling artifacts.

Your job is to normalize unknown or semi-structured model text into a conservative JSON structure that resembles a generic state-machine inventory.

Rules:
1. Never invent behavior not supported by the artifact text.
2. If something is ambiguous, omit it or record it in notes.
3. Focus only on state-machine-like models and closely related control-logic structures.
4. Do not reinterpret unrelated artifacts such as sequence diagrams, class diagrams, or use-case diagrams as state machines.
5. If the artifact is not state-machine-like, return empty lists and explain that in notes.
6. Prefer blocks, states, transitions, signals, and rules when they can be justified.
7. Return strict JSON only.
""".strip()


def _inventory_item_count(inventory: dict[str, object]) -> int:
    total = 0
    for key in ["states", "transitions", "blocks", "signals", "rules"]:
        value = inventory.get(key, [])
        if isinstance(value, list):
            total += len(value)
    return total


def _llm_extract_artifact_payload(llm: ChatOpenAI, artifact_role: str, artifact_text: str) -> dict[str, object] | None:
    if not artifact_text.strip():
        return None
    schema_hint = {
        "machine_name": "",
        "blocks": [
            {
                "name": "BlockName",
                "attributes": [{"name": "attr", "type": "string"}],
                "signals": [{"name": "signal", "direction": "in"}],
                "states": [
                    {
                        "name": "StateName",
                        "parent": None,
                        "parallel_group": None,
                        "is_history": False,
                        "is_initial": False,
                    }
                ],
                "transitions": [
                    {"source": "A", "target": "B", "event": "evt", "guard": "", "action": ""}
                ],
            }
        ],
        "states": [],
        "transitions": [],
        "signals": [
            {
                "name": "signal",
                "direction": "in",
                "source_block": "",
                "target_block": "",
                "payload": [],
            }
        ],
        "rules": [{"target_variable": "", "assigned_value": "", "condition": ""}],
        "notes": ["List ambiguities or omitted items briefly."],
    }
    messages = [
        ("system", ARTIFACT_EXTRACTION_SYSTEM_PROMPT),
        (
            "user",
            f"Artifact role: {artifact_role}\n\n"
            "Normalize the following artifact into the JSON schema below. "
            "Use empty lists when a category is unsupported by the text.\n\n"
            f"Schema:\n{json.dumps(schema_hint, ensure_ascii=False, indent=2)}\n\n"
            f"Artifact text:\n{artifact_text}",
        ),
    ]
    content = _invoke_llm_text(llm, messages, json_mode=True)
    try:
        payload = ensure_json(content)
    except Exception:
        repair_text = _invoke_llm_text(
            llm,
            [
                ("system", "Convert the previous answer into strict JSON only."),
                ("user", f"Previous answer:\n{content}\n\nReturn only strict JSON."),
            ],
        )
        payload = ensure_json(repair_text)
    return payload


def _maybe_llm_augment_inventory(
    llm: ChatOpenAI | None,
    artifact_role: str,
    artifact_text: str | None,
    inventory: dict[str, object],
    counts: dict[str, object],
) -> tuple[dict[str, object], dict[str, object], dict[str, object] | None]:
    if llm is None or not artifact_text or _inventory_item_count(inventory) >= 3:
        return inventory, counts, None
    try:
        extracted_payload = _llm_extract_artifact_payload(llm, artifact_role, artifact_text)
    except Exception:
        return inventory, counts, None
    if not isinstance(extracted_payload, dict):
        return inventory, counts, None
    augmented_inventory = merge_inventory(inventory, machine_elements_from_payload(extracted_payload))
    extracted_counts = count_machine_components(extracted_payload)
    merged_counts = dict(counts or {})
    for key, value in extracted_counts.items():
        merged_counts[key] = max(int(merged_counts.get(key, 0) or 0), int(value))
    return augmented_inventory, merged_counts, extracted_payload


def _precompute(
    request: ExpertReviewRequest,
    llm: ChatOpenAI | None = None,
) -> tuple[str, str, list, dict[str, object], list[RequirementTraceResult], list[ElementIssue]]:
    rubric_text, comparison_policy, dimensions = resolve_review_profile(request.prompt)
    requirements = parse_requirement_items(request.input_text, [])
    inventory = extract_model_inventory(
        request.pred_output,
        request.pred_output,
        request.ref_output,
        request.ref_output,
    )
    pred_inventory, pred_counts, pred_llm_payload = _maybe_llm_augment_inventory(
        llm,
        "prediction",
        request.pred_output,
        inventory["prediction_inventory"],
        inventory.get("prediction_counts", {}),
    )
    ref_inventory, ref_counts, ref_llm_payload = _maybe_llm_augment_inventory(
        llm,
        "reference",
        request.ref_output,
        inventory["reference_inventory"],
        inventory.get("reference_counts", {}),
    )
    inventory["prediction_inventory"] = pred_inventory
    inventory["reference_inventory"] = ref_inventory
    inventory["prediction_counts"] = pred_counts
    inventory["reference_counts"] = ref_counts
    if pred_llm_payload is not None:
        inventory["prediction_llm_extracted_payload"] = pred_llm_payload
    if ref_llm_payload is not None:
        inventory["reference_llm_extracted_payload"] = ref_llm_payload
    requirement_results = _requirement_results(requirements, inventory)
    pred_inventory = inventory["prediction_inventory"]
    ref_inventory = inventory["reference_inventory"]
    unsupported: list[ElementIssue] = []
    if (request.ref_output or "").strip():
        state_match = compute_set_match(pred_inventory.get("states", []), ref_inventory.get("states", []))
        transition_match = compute_set_match(pred_inventory.get("transitions", []), ref_inventory.get("transitions", []))
        for extra in transition_match.get("extra", [])[:10]:
            unsupported.append(
                ElementIssue(
                    element_id=extra,
                    element_kind="transition",
                    element_text=extra,
                    issue_type="extra",
                    reason_text="This transition appears in the prediction but not in the extracted reference inventory.",
                )
            )
        for extra in state_match.get("extra", [])[:10]:
            unsupported.append(
                ElementIssue(
                    element_id=extra,
                    element_kind="state",
                    element_text=extra,
                    issue_type="extra",
                    reason_text="This state appears in the prediction but not in the extracted reference inventory.",
                )
            )
    return rubric_text, comparison_policy, dimensions, inventory, requirement_results, unsupported


def _json_schema_hint(dimensions: list) -> str:
    first_name = dimensions[0].name if dimensions else "notation_syntax"
    return json.dumps(
        {
            "overall_score": 0.0,
            "overall_judgement": "acceptable",
            "overall_reason_text": "Explain what earned credit and what lost credit in at most 3 sentences.",
            "dimension_results": [
                {
                    "dimension_name": first_name,
                    "title": "Dimension title",
                    "score": 0.0,
                    "judgement": "acceptable",
                    "reason_text": "Traceable explanation with positives and negatives in at most 3 sentences.",
                    "evidence": [
                        {
                            "source": "input|prediction|reference|precomputed_context",
                            "locator": None,
                            "snippet": "Short quoted or summarized evidence",
                            "explanation": "Why this evidence matters",
                        }
                    ],
                    "issues": [
                        {
                            "element_id": "req_or_element",
                            "element_kind": "requirement|state|transition|block|signal",
                            "element_text": "Short text",
                            "issue_type": "missing|extra|warning",
                            "reason_text": "Short reason",
                        }
                    ],
                    "confidence": 0.5,
                }
            ],
            "notes": [],
            "confidence": 0.5,
        },
        ensure_ascii=False,
        indent=2,
    )


def llm_primary_review(
    llm: ChatOpenAI,
    model_name: str,
    provider_key: str | None,
    request: ExpertReviewRequest,
) -> ExpertReviewResult:
    rubric_text, comparison_policy, dimensions, inventory, requirement_results, unsupported = _precompute(request, llm=llm)
    compact_context = _compact_precomputed_context(
        request.input_text,
        inventory,
        requirement_results,
        unsupported,
        pred_artifact_text=request.pred_output,
    )
    prompt_block = render_request_prompt(request)
    user_prompt = (
        f"{prompt_block}\n\n"
        f"Resolved rubric text:\n{rubric_text}\n\n"
        f"Resolved comparison policy:\n{comparison_policy}\n\n"
        f"Resolved dimensions:\n{render_dimension_guidance(dimensions)}\n\n"
        f"Input text:\n{request.input_text}\n\n"
        f"Reference output excerpt:\n{_artifact_excerpt(request.ref_output)}\n\n"
        f"Predicted output excerpt:\n{_artifact_excerpt(request.pred_output)}\n\n"
        "Deterministic precomputed context. Use it as support, not as a replacement for semantic judgement:\n"
        f"{json.dumps(compact_context, ensure_ascii=False, indent=2)}\n\n"
        "Output constraints:\n"
        "1. Keep the JSON compact and valid.\n"
        "2. Use at most 2 evidence items per dimension.\n"
        "3. Use at most 2 issues per dimension.\n"
        "4. Use the score range sharply; do not cluster everything near 0.8.\n"
        "5. The precomputed trace summary is heuristic; override it whenever the source text and model support a better semantic judgement.\n\n"
        "Return strict JSON only matching this schema:\n"
        f"{_json_schema_hint(dimensions)}"
    )
    messages = [("system", AGENT_SYSTEM_PROMPT), ("user", user_prompt)]
    content = _invoke_llm_text(llm, messages, json_mode=True)
    try:
        payload = ensure_json(content)
    except Exception:
        repair_text = _invoke_llm_text(
            llm,
            [
                ("system", "Convert the previous answer into strict JSON only. Do not add markdown."),
                ("user", f"Previous answer:\n{content}\n\nReturn only strict JSON."),
            ],
        )
        payload = ensure_json(repair_text)

    def parse_dimension_results(current_payload: dict[str, object]) -> list[DimensionReviewResult]:
        return [dimension_review_from_dict(item) for item in current_payload.get("dimension_results", [])]

    dimension_results = parse_dimension_results(payload)
    if not dimension_results or all(item.score <= 0.0 for item in dimension_results):
        retry_text = _invoke_llm_text(
            llm,
            [
                ("system", AGENT_SYSTEM_PROMPT),
                (
                    "user",
                    user_prompt
                    + "\n\nRetry requirement: the previous answer omitted usable dimension scores. "
                    "Return strict JSON with a non-empty dimension_results list, numeric scores in [0.0, 1.0], and a usable overall score.",
                ),
            ],
            json_mode=True,
        )
        payload = ensure_json(retry_text)
        dimension_results = parse_dimension_results(payload)

    calibration_notes = _apply_generic_grounding_calibration(request, inventory, dimension_results)
    if "overall_score" in payload:
        overall_score = float(payload.get("overall_score", 0.0))
    elif dimension_results:
        overall_score = sum(item.score for item in dimension_results) / len(dimension_results)
    else:
        overall_score = 0.0
    if calibration_notes and dimension_results:
        total_weight = sum(d.weight for d in dimensions) or 1.0
        overall_score = sum(item.score * dim.weight for item, dim in zip(dimension_results, dimensions)) / total_weight
    evidence_summary = [evidence_item_from_dict(item) for item in payload.get("evidence_summary", [])]
    if not evidence_summary:
        evidence_summary = _dimension_evidence_summary(dimension_results)
    return ExpertReviewResult(
        prompt=request.prompt,
        overall_score=overall_score,
        overall_judgement=str(payload.get("overall_judgement", judgement_from_score(overall_score))),
        overall_reason_text=str(payload.get("overall_reason_text", "")),
        used_review_backend="llm_primary",
        dimension_results=dimension_results,
        requirement_trace_results=requirement_results,
        unsupported_model_elements=unsupported,
        evidence_summary=evidence_summary,
        notes=[str(item) for item in payload.get("notes", [])] + calibration_notes,
        llm_model_name=model_name,
        llm_provider=provider_key,
        confidence=float(payload.get("confidence", 0.5)),
    )


def heuristic_expert_review(request: ExpertReviewRequest, llm: ChatOpenAI | None = None) -> ExpertReviewResult:
    rubric_text, comparison_policy, dimensions, inventory, requirement_results, unsupported = _precompute(request, llm=llm)
    pred_inventory = inventory["prediction_inventory"]
    ref_inventory = inventory["reference_inventory"]
    traces_missing = [item for item in requirement_results if item.status == "missing"]
    has_reference = bool((request.ref_output or "").strip())
    review_prompt_lower = request.prompt.lower()
    state_match = compute_set_match(pred_inventory.get("states", []), ref_inventory.get("states", []))
    transition_match = compute_set_match(pred_inventory.get("transitions", []), ref_inventory.get("transitions", []))
    dimension_results: list[DimensionReviewResult] = []
    evidence_summary: list[EvidenceItem] = []

    for dimension in dimensions:
        if dimension.name == "notation_syntax":
            good = bool(pred_inventory.get("states") or pred_inventory.get("blocks") or pred_inventory.get("transitions"))
            score = 0.9 if good else 0.2
            if "syntax" in review_prompt_lower or "grammar" in review_prompt_lower or "格式" in request.prompt:
                score = min(1.0, score + 0.05)
            reason = (
                "The prediction appears structurally interpretable as a modeling artifact."
                if good
                else "The prediction does not show clear signs of a well-formed model artifact."
            )
            evidence = [
                EvidenceItem(
                    source="pred_output",
                    snippet=request.pred_output[:300],
                    explanation="Observed prediction content used for syntax judgement.",
                )
            ]
            issues: list[ElementIssue] = []
            metric_payload = {"heuristic_well_formed": good}
        elif dimension.name in {"semantic_completeness", "adequacy_to_specification"}:
            matched = [item for item in requirement_results if item.status == "matched"]
            partial = [item for item in requirement_results if item.status == "partial"]
            total = len(requirement_results) or 1
            score = min(1.0, (len(matched) + 0.5 * len(partial)) / total)
            if "遗漏" in request.prompt or "focus on missing" in review_prompt_lower:
                score = max(0.0, score - 0.05 * len(traces_missing))
            reason = (
                f"The prediction clearly covers {len(matched)} requirement(s) and partially covers {len(partial)}. "
                f"{len(traces_missing)} requirement(s) still look untraced."
            )
            evidence = [
                EvidenceItem(
                    source="input_text",
                    locator=item.requirement_id,
                    snippet=item.requirement_text,
                    explanation=item.reason_text,
                )
                for item in requirement_results[:5]
            ]
            issues = [
                ElementIssue(
                    element_id=item.requirement_id,
                    element_kind="requirement",
                    element_text=item.requirement_text,
                    issue_type="missing",
                    reason_text=item.reason_text,
                )
                for item in traces_missing[:8]
            ]
            metric_payload = {"matched_requirements": len(matched), "partial_requirements": len(partial), "missing_requirements": len(traces_missing)}
        elif dimension.name in {"behavioral_consistency", "behavioral_plausibility"}:
            if has_reference:
                state_score = _score_from_match(state_match, 0.5)
                transition_score = _score_from_match(transition_match, 0.5)
                score = (state_score + transition_score) / 2
                reason = (
                    f"The prediction preserves some reference structure at the state level (F1={state_score:.2f}) "
                    f"and transition level (F1={transition_score:.2f}). This remains only a proxy for behavior."
                )
                evidence = [
                    EvidenceItem(
                        source="precomputed_context",
                        snippet=f"state_match={state_match}",
                        explanation="State overlap proxy.",
                    ),
                    EvidenceItem(
                        source="precomputed_context",
                        snippet=f"transition_match={transition_match}",
                        explanation="Transition overlap proxy.",
                    ),
                ]
                issues = unsupported[:6]
                metric_payload = {"state_match": state_match, "transition_match": transition_match}
            else:
                matched = len([item for item in requirement_results if item.status == "matched"])
                partial = len([item for item in requirement_results if item.status == "partial"])
                total = len(requirement_results) or 1
                trace_support = (matched + 0.5 * partial) / total
                structure_present = bool(
                    pred_inventory.get("states") or pred_inventory.get("transitions") or pred_inventory.get("blocks")
                )
                score = min(0.95, max(0.2, 0.35 + 0.45 * trace_support + (0.1 if structure_present else 0.0)))
                reason = (
                    "No reference output was provided, so behavioral adequacy was judged from whether the prediction "
                    "contains explicit model structure and whether requirement-triggered behavior is represented in a traceable way."
                )
                evidence = [
                    EvidenceItem(
                        source="input_text",
                        snippet=request.input_text[:300],
                        explanation="Behavioral intent stated in the source description.",
                    ),
                    EvidenceItem(
                        source="pred_output",
                        snippet=request.pred_output[:300],
                        explanation="Predicted model content used for standalone behavioral review.",
                    ),
                ]
                issues = [
                    ElementIssue(
                        element_id=item.requirement_id,
                        element_kind="requirement",
                        element_text=item.requirement_text,
                        issue_type="missing",
                        reason_text=item.reason_text,
                    )
                    for item in traces_missing[:6]
                ]
                metric_payload = {
                    "trace_supported_requirements": matched,
                    "trace_partially_supported_requirements": partial,
                    "missing_requirements": len(traces_missing),
                    "structure_present": structure_present,
                }
        elif dimension.name == "interaction_quality":
            pred_blocks = pred_inventory.get("blocks", [])
            pred_signals = pred_inventory.get("signals", [])
            if has_reference:
                block_match = compute_set_match(pred_blocks, ref_inventory.get("blocks", []))
                signal_match = compute_set_match(pred_signals, ref_inventory.get("signals", []))
                block_score = _score_from_match(block_match, 0.5)
                signal_score = _score_from_match(signal_match, 0.5)
                score = (block_score + signal_score) / 2
                reason = (
                    f"Interaction quality was approximated from block overlap (F1={block_score:.2f}) and "
                    f"signal overlap (F1={signal_score:.2f}) against the reference artifact."
                )
                evidence = [
                    EvidenceItem(
                        source="precomputed_context",
                        snippet=f"block_match={block_match}",
                        explanation="Overlap of communicating blocks.",
                    ),
                    EvidenceItem(
                        source="precomputed_context",
                        snippet=f"signal_match={signal_match}",
                        explanation="Overlap of explicit signal interfaces.",
                    ),
                ]
                issues = unsupported[:6]
                metric_payload = {"block_match": block_match, "signal_match": signal_match}
            else:
                interaction_count = len(pred_signals) + len(pred_inventory.get("transitions", []))
                score = 0.82 if interaction_count > 0 else 0.3
                reason = (
                    "Without a reference artifact, interaction quality was judged from whether the prediction exposes "
                    "explicit exchanges, signals, or transition-level interaction structure."
                )
                evidence = [
                    EvidenceItem(
                        source="pred_output",
                        snippet=request.pred_output[:300],
                        explanation="Predicted artifact content used to inspect communication structure.",
                    )
                ]
                issues = []
                metric_payload = {
                    "predicted_signal_count": len(pred_signals),
                    "predicted_transition_count": len(pred_inventory.get("transitions", [])),
                }
        elif dimension.name == "requirement_traceability":
            matched = sum(1 for item in requirement_results if item.status == "matched")
            partial = sum(1 for item in requirement_results if item.status == "partial")
            total = len(requirement_results) or 1
            score = min(1.0, (matched + 0.4 * partial) / total)
            reason = (
                f"Traceability is supported for {matched} requirement(s), with {partial} partial links and "
                f"{len(traces_missing)} missing links."
            )
            evidence = [
                EvidenceItem(
                    source="input_text",
                    locator=item.requirement_id,
                    snippet=item.requirement_text,
                    explanation=item.reason_text,
                )
                for item in requirement_results[:6]
            ]
            issues = [
                ElementIssue(
                    element_id=item.requirement_id,
                    element_kind="requirement",
                    element_text=item.requirement_text,
                    issue_type="warning",
                    reason_text=item.reason_text,
                )
                for item in traces_missing[:6]
            ]
            metric_payload = {"matched": matched, "partial": partial, "missing": len(traces_missing)}
        else:
            pred_counts = inventory.get("prediction_counts", {})
            ref_counts = inventory.get("reference_counts", {})
            pred_states = float(pred_counts.get("state_count", len(pred_inventory.get("states", []))) or 0)
            ref_states = float(ref_counts.get("state_count", len(ref_inventory.get("states", []))) or 0)
            pred_trans = float(pred_counts.get("transition_count", len(pred_inventory.get("transitions", []))) or 0)
            ref_trans = float(ref_counts.get("transition_count", len(ref_inventory.get("transitions", []))) or 0)
            complexity_penalty = 0.0
            if has_reference:
                if ref_states > 0 and pred_states > ref_states * 1.8:
                    complexity_penalty += 0.2
                if ref_trans > 0 and pred_trans > ref_trans * 1.8:
                    complexity_penalty += 0.2
                score = max(0.15, 0.8 - complexity_penalty)
                reason = (
                    "The score reflects readability and maintainability pressure from structural size. "
                    f"Predicted states={int(pred_states)}, reference states={int(ref_states)}, "
                    f"predicted transitions={int(pred_trans)}, reference transitions={int(ref_trans)}."
                )
            else:
                if pred_states > 25:
                    complexity_penalty += 0.15
                if pred_trans > 50:
                    complexity_penalty += 0.15
                score = max(0.2, 0.82 - complexity_penalty)
                reason = (
                    "No reference output was provided, so clarity was judged from absolute structural burden and whether "
                    "the predicted model appears reviewable without unnecessary inflation. "
                    f"Predicted states={int(pred_states)}, predicted transitions={int(pred_trans)}."
                )
            evidence = [
                EvidenceItem(
                    source="precomputed_context",
                    snippet=json.dumps({"prediction_counts": pred_counts, "reference_counts": ref_counts}, ensure_ascii=False),
                    explanation="Counts used to assess structural inflation and review burden.",
                )
            ]
            issues = unsupported[:6]
            metric_payload = {"complexity_penalty": complexity_penalty}

        trace_links: list[TraceLink] = []
        if dimension.name in {"semantic_completeness", "adequacy_to_specification", "requirement_traceability"}:
            for item in requirement_results[:6]:
                if item.matched_element_ids:
                    trace_links.append(
                        TraceLink(
                            source_id=item.requirement_id,
                            target_id=item.matched_element_ids[0],
                            relation="supports" if item.status == "matched" else "partially_supports",
                            reason_text=item.reason_text,
                        )
                    )
                elif item.status == "missing":
                    trace_links.append(
                        TraceLink(
                            source_id=item.requirement_id,
                            target_id="",
                            relation="untraced",
                            reason_text=item.reason_text,
                        )
                    )
        result = DimensionReviewResult(
            dimension_name=dimension.name,
            title=dimension.title,
            score=round(score, 6),
            judgement=judgement_from_score(score),
            reason_text=reason,
            evidence=evidence,
            trace_links=trace_links,
            issues=issues,
            metric_payload=metric_payload,
            confidence=0.62,
        )
        dimension_results.append(result)
        evidence_summary.extend(evidence[:2])

    calibration_notes = _apply_generic_grounding_calibration(request, inventory, dimension_results)
    total_weight = sum(d.weight for d in dimensions) or 1.0
    overall_score = sum(item.score * dim.weight for item, dim in zip(dimension_results, dimensions)) / total_weight
    overall_reason = (
        f"The review followed the user prompt: {request.prompt}. "
        f"Strengths were credited where the prediction remained interpretable and covered the intended behavior. "
        f"Deductions came from missing requirement traces, unsupported extra content, or inflated structure."
    )
    return ExpertReviewResult(
        prompt=request.prompt,
        overall_score=round(overall_score, 6),
        overall_judgement=judgement_from_score(overall_score),
        overall_reason_text=overall_reason,
        used_review_backend="heuristic",
        dimension_results=dimension_results,
        requirement_trace_results=requirement_results,
        unsupported_model_elements=unsupported,
        evidence_summary=evidence_summary[:12],
        notes=[f"comparison_policy={comparison_policy}", f"rubric_text={rubric_text}"] + calibration_notes,
        confidence=0.62,
    )
