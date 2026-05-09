"""``traceability`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.agents` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import RequirementTraceResult
from ..prompts import TRACEABILITY_SYSTEM_PROMPT
from .common import (
    candidate_texts_from_dossier,
    clip01,
    combined_overlap_score,
    infer_count_hint,
    initial_targets_from_behaviors,
    major_element_name_set,
    shared_source_target_map,
)
from .llm_helpers import invoke_llm_json


def _requirement_profile(requirement_text: str) -> dict[str, Any]:
    """内部 helper：``_requirement_profile``。

    :param requirement_text: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    lowered = requirement_text.lower()
    return {
        "requires_parallel": any(token in lowered for token in ["parallel", "orthogonal", "concurrent"]),
        "requires_region_count": "region" in lowered or "substate" in lowered or "state area" in lowered,
        "count_hint": infer_count_hint(requirement_text),
        "event_driven": any(token in lowered for token in ["when ", "if ", "receive", "received", "trigger", "detected"]),
        "transition_focused": any(token in lowered for token in ["transit", "transition", "enters", "enters the", "goes to"]),
        "state_focused": any(token in lowered for token in ["state", "mode", "substate", "region"]),
        "overall_context_only": any(token in lowered for token in ["describes", "represents", "model describes", "diagram describes"]),
    }


def _structural_requirement_support(requirement_text: str, pred_dossier: Any) -> tuple[float, list[str], str]:
    """内部 helper：``_structural_requirement_support``。

    :param requirement_text: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    profile = _requirement_profile(requirement_text)
    reasons: list[str] = []
    matched_ids: list[str] = []
    support = 0.0
    initial_targets = initial_targets_from_behaviors(pred_dossier)
    major_states = major_element_name_set(pred_dossier)
    branch_map = shared_source_target_map(pred_dossier)
    max_branch_count = max((len(targets) for targets in branch_map.values()), default=0)

    if profile["requires_parallel"]:
        if pred_dossier.surface_markers.get("parallel", 0) > 0:
            support += 0.64
            reasons.append("explicit parallel or orthogonal markers are visible in the prediction dossier")
        elif max_branch_count >= 2 or len(initial_targets) >= 2:
            support += 0.32
            reasons.append("multiple branch families are visible, but explicit parallel markers are missing")
    if profile["requires_region_count"]:
        count_hint = int(profile["count_hint"] or 0)
        visible_count = max(len(initial_targets), len(major_states))
        if count_hint and visible_count >= count_hint:
            support += 0.30 if pred_dossier.surface_markers.get("parallel", 0) > 0 else 0.18
            reasons.append(f"the prediction exposes at least {count_hint} visible state/branch targets")
        elif visible_count >= 2:
            support += 0.12
            reasons.append("the prediction exposes multiple visible state/branch targets")
        structural_elements = [
            item
            for item in pred_dossier.elements
            if "initial" not in (item.label or "").lower() and "start" not in (item.label or "").lower()
        ]
        if not structural_elements:
            structural_elements = list(pred_dossier.elements)
        matched_ids.extend(item.element_id for item in structural_elements[: min(3, len(structural_elements))])

    if support > 0 and not reasons:
        reasons.append("structural evidence was found in the prediction dossier")
    return clip01(support), matched_ids[:4], "; ".join(reasons)


def deterministic_traceability(
    input_dossier: Any,
    pred_dossier: Any,
) -> list[RequirementTraceResult]:
    """``deterministic_traceability`` 函数。

    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    candidates = candidate_texts_from_dossier(pred_dossier)
    results: list[RequirementTraceResult] = []

    for requirement in input_dossier.requirements:
        profile = _requirement_profile(requirement.requirement_text)
        scored: list[tuple[float, str, str, str]] = []
        for candidate_id, kind, candidate_text in candidates:
            score = combined_overlap_score(requirement.requirement_text, candidate_text)
            if profile["event_driven"] and kind == "relation":
                score += 0.08
            if profile["transition_focused"] and kind == "relation":
                score += 0.06
            if profile["state_focused"] and kind == "state":
                score += 0.04
            if profile["overall_context_only"] and kind in {"state", "behavior"}:
                score -= 0.06
            if score <= 0.02:
                continue
            scored.append((score, candidate_id, kind, candidate_text))

        scored.sort(key=lambda item: item[0], reverse=True)
        top = scored[:4]
        top_score = top[0][0] if top else 0.0

        structural_score, structural_ids, structural_reason = _structural_requirement_support(
            requirement.requirement_text,
            pred_dossier,
        )
        matched_ids = [item[1] for item in top if item[0] >= max(0.25, top_score * 0.68)]
        if structural_ids:
            matched_ids.extend(structural_ids)
        matched_ids = matched_ids[:4]
        best_support = max(top_score, structural_score)

        if best_support >= 0.58 or (top_score >= 0.46 and structural_score >= 0.18):
            status = "matched"
            confidence = 0.74 if best_support >= 0.66 else 0.64
            reasons = []
            if top:
                reasons.append("best candidate overlap is strong enough to support semantic grounding")
            if structural_reason:
                reasons.append(structural_reason)
            reason = "Requirement is supported by visible predicted evidence because " + "; ".join(reasons) + "."
        elif best_support >= 0.22 or matched_ids:
            status = "partial"
            confidence = 0.52
            reasons = []
            if top:
                reasons.append("some lexical or stem-level overlap exists")
            if structural_reason:
                reasons.append(structural_reason)
            if not reasons:
                reasons.append("the prediction only exposes weak supporting evidence")
            reason = "Requirement has only partial support because " + "; ".join(reasons) + "."
        else:
            status = "missing"
            confidence = 0.46
            reason = "No convincing predicted evidence could be linked to this requirement."

        results.append(
            RequirementTraceResult(
                requirement_id=requirement.requirement_id,
                requirement_text=requirement.requirement_text,
                status=status,
                reason_text=reason,
                matched_element_ids=matched_ids,
                confidence=confidence,
            )
        )
    return results


def traceability_with_llm(
    llm: ChatOpenAI,
    input_dossier: Any,
    pred_dossier: Any,
) -> list[RequirementTraceResult] | None:
    """``traceability_with_llm`` 函数。

    :param llm: 见函数签名与上下文。
    :param input_dossier: 见函数签名与上下文。
    :param pred_dossier: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    if not input_dossier.requirements:
        return []
    candidates = candidate_texts_from_dossier(pred_dossier)
    compact_candidates = []
    for req in input_dossier.requirements:
        scored: list[tuple[float, str, str]] = []
        for candidate_id, kind, candidate_text in candidates:
            score = combined_overlap_score(req.requirement_text, candidate_text)
            if score <= 0.0:
                continue
            scored.append((score, f"{candidate_id}|{kind}", candidate_text))
        scored.sort(key=lambda item: item[0], reverse=True)
        compact_candidates.append(
            {
                "requirement_id": req.requirement_id,
                "requirement_text": req.requirement_text,
                "structural_markers": pred_dossier.surface_markers,
                "candidate_evidence": [
                    {"candidate_id": item[1], "candidate_text": item[2][:240], "score_hint": round(item[0], 4)}
                    for item in scored[:5]
                ],
            }
        )
    payload = invoke_llm_json(
        llm,
        [
            ("system", TRACEABILITY_SYSTEM_PROMPT),
            (
                "user",
                "Review each requirement against the prediction dossier.\n\n"
                "Return JSON with key trace_results, where each item has: "
                "requirement_id, status, reason_text, matched_element_ids, confidence.\n\n"
                f"Input summary:\n{input_dossier.summary}\n\n"
                f"Input behaviors:\n{json.dumps(input_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Input constraints:\n{json.dumps(input_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n\n"
                f"Prediction constraints:\n{json.dumps(pred_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction ambiguities:\n{json.dumps(pred_dossier.ambiguities[:8], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction structural markers:\n{json.dumps(pred_dossier.surface_markers, ensure_ascii=False, indent=2)}\n\n"
                f"Trace candidates:\n{json.dumps(compact_candidates, ensure_ascii=False, indent=2)}",
            ),
        ],
        operation="traceability",
    )
    if not isinstance(payload, dict):
        return None
    requirement_map = {req.requirement_id: req.requirement_text for req in input_dossier.requirements}
    trace_results: list[RequirementTraceResult] = []
    for item in payload.get("trace_results", []):
        if not isinstance(item, dict):
            continue
        requirement_id = str(item.get("requirement_id", "")).strip()
        if not requirement_id or requirement_id not in requirement_map:
            continue
        trace_results.append(
            RequirementTraceResult(
                requirement_id=requirement_id,
                requirement_text=requirement_map[requirement_id],
                status=str(item.get("status") or "partial"),
                reason_text=str(item.get("reason_text") or ""),
                matched_element_ids=[str(x) for x in item.get("matched_element_ids", [])[:4]],
                confidence=float(item.get("confidence", 0.55)),
            )
        )
    return trace_results or None