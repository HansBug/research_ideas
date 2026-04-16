from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import ElementIssue, EvidenceItem
from ..prompts import EQUIVALENCE_SYSTEM_PROMPT
from .common import (
    clip01,
    combined_overlap_score,
    dedupe_strings,
    find_best_relation_overlap,
    initial_targets_from_behaviors,
    is_grounded_to_input,
    major_element_name_set,
    make_evidence_item,
    overlap_score,
    requirement_grounding_tokens,
    shared_source_target_map,
)
from .llm_helpers import invoke_llm_json


def _extra_issue_from_element(element: Any, issue_type: str, reason_text: str) -> ElementIssue:
    return ElementIssue(
        element_id=element.element_id,
        element_kind=element.kind,
        element_text=element.label or element.text,
        issue_type=issue_type,
        reason_text=reason_text,
    )


def _extra_issue_from_relation(relation: Any, issue_type: str, reason_text: str) -> ElementIssue:
    return ElementIssue(
        element_id=relation.relation_id,
        element_kind=relation.kind,
        element_text=relation.description or relation.evidence_text,
        issue_type=issue_type,
        reason_text=reason_text,
    )


def _synthetic_issue(element_id: str, issue_type: str, element_text: str, reason_text: str) -> ElementIssue:
    return ElementIssue(
        element_id=element_id,
        element_kind="structure",
        element_text=element_text,
        issue_type=issue_type,
        reason_text=reason_text,
    )


def _detect_guard_polarity_conflict(pred_relation: Any, ref_relation: Any) -> bool:
    if not pred_relation.condition or not ref_relation.condition:
        return False
    pred = pred_relation.condition.lower()
    ref = ref_relation.condition.lower()
    patterns = [
        ("<", ">"),
        (">", "<"),
        ("<=", ">="),
        (">=", "<="),
        (" not ", " "),
    ]
    for left, right in patterns:
        if left in pred and right in ref:
            return True
        if right in pred and left in ref:
            return True
    return False


def _major_relation_labels(pred_dossier: Any) -> tuple[set[str], set[str]]:
    major_names = major_element_name_set(pred_dossier)
    major_relations: set[str] = set()
    internal_relations: set[str] = set()
    for relation in pred_dossier.relations:
        source = relation.source_label.lower().strip()
        target = relation.target_label.lower().strip()
        if source and target and source in major_names and target in major_names:
            major_relations.add(relation.relation_id)
        else:
            internal_relations.add(relation.relation_id)
    return major_relations, internal_relations


def _parallel_structure_diagnostics(pred_dossier: Any, ref_dossier: Any) -> dict[str, Any]:
    ref_initial_targets = initial_targets_from_behaviors(ref_dossier)
    pred_initial_targets = initial_targets_from_behaviors(pred_dossier)
    ref_parallel_markers = int(ref_dossier.surface_markers.get("parallel", 0) or 0)
    ref_parallel_expected = ref_parallel_markers >= 2 or (
        ref_parallel_markers >= 1 and len(ref_dossier.relations) <= 2 and len(ref_initial_targets) >= 3
    )
    pred_parallel_explicit = pred_dossier.surface_markers.get("parallel", 0) > 0
    shared_sources = shared_source_target_map(pred_dossier)
    branching_targets = max((len(targets) for targets in shared_sources.values()), default=0)
    major_names = major_element_name_set(pred_dossier)
    major_to_major_relations = [
        relation
        for relation in pred_dossier.relations
        if relation.source_label.lower().strip() in major_names and relation.target_label.lower().strip() in major_names
    ]
    severe_parallel_mismatch = (
        ref_parallel_expected and not pred_parallel_explicit and len(major_to_major_relations) >= max(2, len(ref_initial_targets))
    )
    branch_family_credit = (
        ref_parallel_expected
        and not pred_parallel_explicit
        and branching_targets >= max(2, len(ref_initial_targets))
        and not major_to_major_relations
    )
    return {
        "ref_initial_targets": ref_initial_targets,
        "pred_initial_targets": pred_initial_targets,
        "ref_parallel_markers": ref_parallel_markers,
        "ref_parallel_expected": ref_parallel_expected,
        "pred_parallel_explicit": pred_parallel_explicit,
        "branching_targets": branching_targets,
        "major_to_major_relations": major_to_major_relations,
        "severe_parallel_mismatch": severe_parallel_mismatch,
        "branch_family_credit": branch_family_credit,
    }


def deterministic_equivalence(
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> dict[str, Any]:
    grounding_tokens = requirement_grounding_tokens(input_dossier)
    supported_restructures: list[str] = []
    harmful_extras: list[ElementIssue] = []
    missing_items: list[str] = []
    contradictions: list[ElementIssue] = []
    dependency_breaks: list[ElementIssue] = []

    ref_elements = ref_dossier.elements
    pred_elements = pred_dossier.elements
    major_relation_ids, internal_relation_ids = _major_relation_labels(pred_dossier)
    structural = _parallel_structure_diagnostics(pred_dossier, ref_dossier)
    grounded_relation_state_names: set[str] = set()

    matched_ref_elements = 0
    for ref_element in ref_elements:
        best = max(
            (combined_overlap_score(ref_element.text, pred_element.text) for pred_element in pred_elements),
            default=0.0,
        )
        if best >= 0.34:
            matched_ref_elements += 1
        else:
            missing_items.append(ref_element.label or ref_element.text)

    relation_coverages: list[float] = []
    for ref_relation in ref_dossier.relations:
        best_overlap = find_best_relation_overlap(ref_relation, pred_dossier.relations)
        relation_coverages.append(best_overlap)
        if best_overlap < 0.24:
            missing_items.append(ref_relation.description or ref_relation.evidence_text)
        else:
            for pred_relation in pred_dossier.relations:
                score = find_best_relation_overlap(pred_relation, [ref_relation])
                if score >= 0.40 and _detect_guard_polarity_conflict(pred_relation, ref_relation):
                    contradictions.append(
                        _extra_issue_from_relation(
                            pred_relation,
                            "contradiction",
                            "The relation looks aligned to a reference behavior but the guard polarity appears inconsistent.",
                        )
                    )
                    break

    if structural["severe_parallel_mismatch"]:
        contradictions.append(
            _synthetic_issue(
                "parallel_structure_mismatch",
                "contradiction",
                "parallel/orthogonal structure mismatch",
                "The reference exposes orthogonal or parallel regions, but the prediction replaces them with major cross-state transitions that collapse the branch structure.",
            )
        )
        missing_items.append("parallel or orthogonal branch structure from the reference")

    if structural["branch_family_credit"]:
        supported_restructures.append(
            "The prediction exposes branch-specific control families without explicit parallel separators; this can be a supported restructure when the branches remain behaviorally separated."
        )

    for relation in pred_dossier.relations:
        best_ref = find_best_relation_overlap(relation, ref_dossier.relations)
        grounded = is_grounded_to_input(relation.description or relation.evidence_text, grounding_tokens)
        if grounded:
            if relation.source_label:
                grounded_relation_state_names.add(relation.source_label.lower().strip())
            if relation.target_label:
                grounded_relation_state_names.add(relation.target_label.lower().strip())

        relation_is_major = relation.relation_id in major_relation_ids
        relation_is_internal = relation.relation_id in internal_relation_ids
        wrapper_like = any(
            token in (relation.source_label or "").lower() or token in (relation.target_label or "").lower()
            for token in ["initialstate", "finalstate", "start", "end"]
        )
        if structural["severe_parallel_mismatch"] and relation_is_major:
            dependency_breaks.append(
                _extra_issue_from_relation(
                    relation,
                    "contradiction",
                    "This major cross-state transition looks incompatible with the reference's orthogonal or parallel branch structure.",
                )
            )
            continue
        if best_ref < 0.22:
            if grounded and not relation_is_major and not wrapper_like:
                supported_restructures.append(
                    f"{relation.description or relation.evidence_text} differs from the reference surface form but remains requirement-grounded."
                )
            elif structural["branch_family_credit"] and relation_is_internal:
                supported_restructures.append(
                    f"{relation.description or relation.evidence_text} looks like an internal implementation detail inside a branch family rather than a harmful extra."
                )
            elif grounded and not structural["severe_parallel_mismatch"] and (not relation_is_major or best_ref >= 0.12):
                supported_restructures.append(
                    f"{relation.description or relation.evidence_text} is weakly aligned to the reference but still grounded in the requirements."
                )
            else:
                harmful_extras.append(
                    _extra_issue_from_relation(
                        relation,
                        "extra",
                        "This predicted relation lacks clear support from the reference and the visible requirements, and wrapper-state transitions do not receive automatic credit.",
                    )
                )

    for element in pred_elements:
        best_ref = max((combined_overlap_score(element.text, ref_element.text) for ref_element in ref_elements), default=0.0)
        grounded = is_grounded_to_input(element.text, grounding_tokens)
        relation_grounded = element.label.lower().strip() in grounded_relation_state_names
        if best_ref < 0.25:
            if grounded or relation_grounded:
                supported_restructures.append(
                    f"{element.label or element.text} is not a close surface match to the reference but is grounded in the input requirements."
                )
            elif structural["branch_family_credit"] and "initial" in (element.label or "").lower():
                supported_restructures.append(
                    f"{element.label or element.text} looks like a local wrapper or entry state inside an equivalent branch-family decomposition."
                )
            elif structural["branch_family_credit"] and element.label.lower().strip() in {
                relation.target_label.lower().strip() for relation in pred_dossier.relations
            }:
                supported_restructures.append(
                    f"{element.label or element.text} behaves like a branch controller under an equivalent decomposition."
                )
            else:
                harmful_extras.append(
                    _extra_issue_from_element(
                        element,
                        "extra",
                        "This predicted element is weakly grounded in both the reference and the input requirements.",
                    )
                )

    ref_element_coverage = matched_ref_elements / max(1, len(ref_elements))
    ref_relation_coverage = (
        sum(relation_coverages) / max(1, len(relation_coverages)) if relation_coverages else ref_element_coverage
    )
    contradiction_count = len(contradictions) + len(dependency_breaks)
    harmful_count = len(harmful_extras)
    equivalence_strength = clip01(
        0.42 * ref_element_coverage
        + 0.38 * ref_relation_coverage
        + 0.08 * min(1.0, len(supported_restructures) / 3.0)
        - 0.12 * contradiction_count
        - 0.08 * min(4, harmful_count)
        + (0.12 if structural["branch_family_credit"] else 0.0)
        - (0.16 if structural["severe_parallel_mismatch"] else 0.0)
    )
    evidence: list[EvidenceItem] = []
    if ref_dossier.relations:
        evidence.append(
            make_evidence_item(
                "reference",
                None,
                ref_dossier.relations[0].evidence_text,
                "Reference relation used as a comparison anchor.",
            )
        )
    if pred_dossier.relations:
        evidence.append(
            make_evidence_item(
                "prediction",
                None,
                pred_dossier.relations[0].evidence_text,
                "Predicted relation compared against the reference and requirements.",
            )
        )
    if structural["severe_parallel_mismatch"]:
        evidence.append(
            make_evidence_item(
                "comparison",
                "comparison:parallel-structure",
                "Reference parallel structure vs. prediction cross-state transitions",
                "Structural comparison found a collapse of orthogonal or parallel branches.",
            )
        )

    return {
        "equivalence_strength": equivalence_strength,
        "ref_element_coverage": ref_element_coverage,
        "ref_relation_coverage": ref_relation_coverage,
        "missing_item_count": len(missing_items),
        "harmful_extra_count": harmful_count,
        "contradiction_count": contradiction_count,
        "supported_restructures": dedupe_strings(supported_restructures)[:8],
        "harmful_extras": harmful_extras[:10],
        "missing_items": dedupe_strings(missing_items)[:10],
        "contradictions": (contradictions + dependency_breaks)[:10],
        "dependency_breaks": dependency_breaks[:10],
        "parallel_structure_mismatch": structural["severe_parallel_mismatch"],
        "parallel_branch_credit": structural["branch_family_credit"],
        "major_relation_divergence_count": len(structural["major_to_major_relations"]),
        "evidence": evidence[:4],
        "confidence": 0.72 if ref_dossier.observability == "high" else 0.60,
    }


def _json_safe_report(report: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in report.items():
        if isinstance(value, list) and value and isinstance(value[0], ElementIssue):
            safe[key] = [
                {
                    "element_id": item.element_id,
                    "element_kind": item.element_kind,
                    "element_text": item.element_text,
                    "issue_type": item.issue_type,
                    "reason_text": item.reason_text,
                }
                for item in value
            ]
        elif isinstance(value, list) and value and isinstance(value[0], EvidenceItem):
            safe[key] = [
                {
                    "source": item.source,
                    "locator": item.locator,
                    "snippet": item.snippet,
                    "explanation": item.explanation,
                }
                for item in value
            ]
        else:
            safe[key] = value
    return safe


def equivalence_with_llm(
    llm: ChatOpenAI,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    base_report: dict[str, Any],
) -> dict[str, Any] | None:
    payload = invoke_llm_json(
        llm,
        [
            ("system", EQUIVALENCE_SYSTEM_PROMPT),
            (
                "user",
                "Judge semantic equivalence and meaningful differences.\n\n"
                "Return JSON with keys: equivalence_strength, supported_restructures, harmful_extras, "
                "missing_items, contradictions, confidence.\n\n"
                f"Requirements:\n{json.dumps([item.requirement_text for item in input_dossier.requirements], ensure_ascii=False, indent=2)}\n\n"
                f"Input constraints:\n{json.dumps(input_dossier.constraints[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n"
                f"Prediction behaviors:\n{json.dumps(pred_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction markers:\n{json.dumps(pred_dossier.surface_markers, ensure_ascii=False, indent=2)}\n\n"
                f"Reference summary:\n{ref_dossier.summary}\n"
                f"Reference behaviors:\n{json.dumps(ref_dossier.behaviors[:10], ensure_ascii=False, indent=2)}\n\n"
                f"Reference markers:\n{json.dumps(ref_dossier.surface_markers, ensure_ascii=False, indent=2)}\n\n"
                f"Deterministic candidate report:\n{json.dumps(_json_safe_report(base_report), ensure_ascii=False, indent=2)}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        return None
    harmful_extras: list[ElementIssue] = []
    for idx, item in enumerate(payload.get("harmful_extras", []), start=1):
        if isinstance(item, dict):
            harmful_extras.append(
                ElementIssue(
                    element_id=str(item.get("element_id") or f"pred_extra_{idx}"),
                    element_kind=str(item.get("element_kind") or "element"),
                    element_text=str(item.get("element_text") or ""),
                    issue_type="extra",
                    reason_text=str(item.get("reason_text") or "LLM judged this as a harmful unsupported extra."),
                )
            )
        else:
            harmful_extras.append(
                ElementIssue(
                    element_id=f"pred_extra_{idx}",
                    element_kind="element",
                    element_text=str(item),
                    issue_type="extra",
                    reason_text="LLM judged this as a harmful unsupported extra.",
                )
            )
    contradictions: list[ElementIssue] = []
    for idx, item in enumerate(payload.get("contradictions", []), start=1):
        if isinstance(item, dict):
            contradictions.append(
                ElementIssue(
                    element_id=str(item.get("element_id") or f"pred_contradiction_{idx}"),
                    element_kind=str(item.get("element_kind") or "relation"),
                    element_text=str(item.get("element_text") or ""),
                    issue_type="contradiction",
                    reason_text=str(item.get("reason_text") or "LLM judged this as a contradiction."),
                )
            )
        else:
            contradictions.append(
                ElementIssue(
                    element_id=f"pred_contradiction_{idx}",
                    element_kind="relation",
                    element_text=str(item),
                    issue_type="contradiction",
                    reason_text="LLM judged this as a contradiction.",
                )
            )
    report = dict(base_report)
    report["equivalence_strength"] = float(payload.get("equivalence_strength", report.get("equivalence_strength", 0.5)))
    report["supported_restructures"] = [
        str(item).strip() for item in payload.get("supported_restructures", report.get("supported_restructures", []))
    ][:8]
    if harmful_extras:
        report["harmful_extras"] = harmful_extras[:10]
    report["missing_items"] = [str(item).strip() for item in payload.get("missing_items", report.get("missing_items", []))][
        :10
    ]
    if contradictions:
        report["contradictions"] = contradictions[:8]
    report["confidence"] = float(payload.get("confidence", report.get("confidence", 0.6)))
    return report
