from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import RequirementTraceResult
from ..prompts import ARBITRATION_SYSTEM_PROMPT
from .common import clip01
from .llm_helpers import invoke_llm_json


def _downgrade_status(status: str) -> str:
    if status == "matched":
        return "partial"
    if status == "partial":
        return "missing"
    return status


def _upgrade_status(status: str) -> str:
    if status == "missing":
        return "partial"
    if status == "partial":
        return "matched"
    return status


def arbitrate_trace_and_equivalence(
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    trace_results: list[RequirementTraceResult],
    equivalence_report: dict[str, Any],
) -> tuple[list[RequirementTraceResult], dict[str, Any], list[str]]:
    notes: list[str] = []
    harmful_ids = {item.element_id for item in equivalence_report.get("harmful_extras", [])}
    contradiction_ids = {item.element_id for item in equivalence_report.get("contradictions", [])}
    dependency_break_ids = {item.element_id for item in equivalence_report.get("dependency_breaks", [])}
    severe_parallel_mismatch = bool(equivalence_report.get("parallel_structure_mismatch"))
    branch_family_credit = bool(equivalence_report.get("parallel_branch_credit"))

    adjusted_results: list[RequirementTraceResult] = []
    trace_conflict_count = 0
    upgraded_count = 0

    for item in trace_results:
        lowered = item.requirement_text.lower()
        matched_ids = set(item.matched_element_ids)
        new_status = item.status
        reason_suffixes: list[str] = []
        confidence = item.confidence
        structural_requirement = any(
            token in lowered for token in ["parallel", "orthogonal", "concurrent", "region", "substate", "collision"]
        )

        should_downgrade_for_issue_ids = bool(matched_ids & (harmful_ids | contradiction_ids | dependency_break_ids))
        if branch_family_credit and structural_requirement and not severe_parallel_mismatch and not (matched_ids & (contradiction_ids | dependency_break_ids)):
            should_downgrade_for_issue_ids = False

        if should_downgrade_for_issue_ids:
            new_status = _downgrade_status(new_status)
            confidence = min(confidence, 0.56 if new_status == "partial" else 0.48)
            reason_suffixes.append(
                "some of the supporting predicted items were later judged structurally unsafe or contradictory"
            )

        if severe_parallel_mismatch and any(
            token in lowered for token in ["parallel", "orthogonal", "concurrent", "region", "substate", "state area"]
        ):
            new_status = _downgrade_status(new_status)
            confidence = min(confidence, 0.54 if new_status == "partial" else 0.46)
            reason_suffixes.append(
                "the reference exposes orthogonal or parallel structure that the prediction collapsed into incompatible cross-state transitions"
            )

        if branch_family_credit and item.status == "missing" and any(
            token in lowered for token in ["parallel", "orthogonal", "concurrent", "region", "control", "collision"]
        ):
            new_status = _upgrade_status(new_status)
            confidence = max(confidence, 0.52)
            reason_suffixes.append(
                "the prediction still exposes branch-specific control families, so this requirement is better treated as partially supported than fully missing"
            )

        if new_status != item.status:
            if item.status == "missing" and new_status != "missing":
                upgraded_count += 1
            else:
                trace_conflict_count += 1

        adjusted_results.append(
            RequirementTraceResult(
                requirement_id=item.requirement_id,
                requirement_text=item.requirement_text,
                status=new_status,
                reason_text=(
                    item.reason_text.rstrip(".")
                    + (". However, " + "; ".join(reason_suffixes) + "." if reason_suffixes else "")
                ),
                matched_element_ids=item.matched_element_ids[:4],
                confidence=round(confidence, 6),
            )
        )

    adjusted_report = dict(equivalence_report)
    adjusted_report["equivalence_strength"] = clip01(
        float(equivalence_report.get("equivalence_strength", 0.5))
        - 0.08 * trace_conflict_count
        + 0.04 * min(2, upgraded_count)
    )
    adjusted_report["trace_conflict_count"] = trace_conflict_count
    adjusted_report["trace_upgrade_count"] = upgraded_count
    if trace_conflict_count:
        notes.append(
            f"Arbiter downgraded {trace_conflict_count} trace judgement(s) after reconciling trace support with structural or equivalence conflicts."
        )
    if upgraded_count:
        notes.append(
            f"Arbiter upgraded {upgraded_count} trace judgement(s) from missing to partial where branch-family evidence suggested equivalent restructuring."
        )
    return adjusted_results, adjusted_report, notes


def arbitrate_with_llm(
    llm: ChatOpenAI,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    trace_results: list[RequirementTraceResult],
    equivalence_report: dict[str, Any],
) -> tuple[list[RequirementTraceResult], dict[str, Any], list[str]] | None:
    payload = invoke_llm_json(
        llm,
        [
            ("system", ARBITRATION_SYSTEM_PROMPT),
            (
                "user",
                "Resolve conflicts between traceability and equivalence outputs.\n\n"
                "Return JSON with keys: requirement_overrides, equivalence_strength, arbitration_notes.\n"
                "Each requirement_overrides item should contain: requirement_id, status, reason_text, confidence.\n\n"
                f"Requirements:\n{json.dumps([item.requirement_text for item in input_dossier.requirements], ensure_ascii=False, indent=2)}\n\n"
                f"Prediction summary:\n{pred_dossier.summary}\n\n"
                f"Reference summary:\n{ref_dossier.summary}\n\n"
                f"Trace results:\n{json.dumps([{'requirement_id': item.requirement_id, 'status': item.status, 'reason_text': item.reason_text, 'matched_element_ids': item.matched_element_ids, 'confidence': item.confidence} for item in trace_results], ensure_ascii=False, indent=2)}\n\n"
                f"Equivalence report:\n{json.dumps({'equivalence_strength': equivalence_report.get('equivalence_strength'), 'supported_restructures': equivalence_report.get('supported_restructures', []), 'harmful_extras': [{'element_id': item.element_id, 'element_text': item.element_text, 'reason_text': item.reason_text} for item in equivalence_report.get('harmful_extras', [])], 'contradictions': [{'element_id': item.element_id, 'element_text': item.element_text, 'reason_text': item.reason_text} for item in equivalence_report.get('contradictions', [])], 'parallel_structure_mismatch': equivalence_report.get('parallel_structure_mismatch', False)}, ensure_ascii=False, indent=2)}",
            ),
        ],
        operation="arbiter",
    )
    if not isinstance(payload, dict):
        return None

    override_map = {item.requirement_id: item for item in trace_results}
    allow_status_override = bool(
        equivalence_report.get("trace_conflict_count")
        or equivalence_report.get("trace_upgrade_count")
        or equivalence_report.get("parallel_structure_mismatch")
        or equivalence_report.get("contradictions")
        or equivalence_report.get("dependency_breaks")
    )
    if allow_status_override:
        for item in payload.get("requirement_overrides", []):
            if not isinstance(item, dict):
                continue
            requirement_id = str(item.get("requirement_id") or "").strip()
            if requirement_id not in override_map:
                continue
            base = override_map[requirement_id]
            override_status = str(item.get("status") or base.status).strip() or base.status
            if override_status not in {"matched", "partial", "missing"}:
                override_status = base.status
            override_map[requirement_id] = RequirementTraceResult(
                requirement_id=base.requirement_id,
                requirement_text=base.requirement_text,
                status=override_status,
                reason_text=str(item.get("reason_text") or base.reason_text),
                matched_element_ids=base.matched_element_ids[:4],
                confidence=float(item.get("confidence", base.confidence)),
            )
    report = dict(equivalence_report)
    base_strength = float(report.get("equivalence_strength", 0.5))
    proposed_strength = float(payload.get("equivalence_strength", base_strength))
    report["equivalence_strength"] = clip01(max(base_strength - 0.06, min(base_strength + 0.06, proposed_strength)))
    raw_notes = payload.get("arbitration_notes", [])
    if isinstance(raw_notes, str):
        raw_notes = [raw_notes]
    notes = [str(item).strip() for item in raw_notes if str(item).strip()]
    if not allow_status_override and payload.get("requirement_overrides"):
        notes.append("LLM arbitration notes were retained, but requirement statuses stayed with deterministic arbitration because no explicit conflict required override.")
    return list(override_map.values()), report, notes
