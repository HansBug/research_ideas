from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import ExpertReviewResult, judgement_from_score
from ..prompts.synthesis import FINAL_SYNTHESIS_SYSTEM_PROMPT
from ..tools import evidence_summary_from_dimensions, validate_result_shape
from .llm_helpers import invoke_llm_json


def overall_reason(
    regime: Any,
    policy_packet: dict[str, Any],
    overall_score: float,
    trace_results: list[Any],
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    harmful_issues: list[Any],
    evidence_critic: dict[str, Any],
) -> str:
    matched = sum(1 for item in trace_results if item.status == "matched")
    partial = sum(1 for item in trace_results if item.status == "partial")
    missing = sum(1 for item in trace_results if item.status == "missing")
    supported_restructures = equivalence_report.get("supported_restructures", [])
    contradictions = equivalence_report.get("contradictions", [])
    score_semantics = policy_packet.get("score_semantics")
    parts = [
        f"Review used the `{regime.regime}` evidence regime with policy `{policy_packet.get('profile_name')}` and produced an overall score of {overall_score:.3f}.",
    ]
    if regime.regime == "summary_only":
        parts.append(
            "The task was treated as a coarse summary-level judgement rather than a direct per-element comparison."
            if score_semantics != "summary_stat_stddev"
            else "The task was treated as an aggregate variability/dispersion row, so the score remained contract-driven and intentionally coarse."
        )
    elif regime.regime == "protocol_only":
        parts.append("The task was treated as a protocol-level assurance review, not as direct artifact-level defect detection.")
        if evidence_critic.get("vv_roles"):
            parts.append("Recognized V&V roles: " + ", ".join(evidence_critic["vv_roles"][:4]) + ".")
    else:
        parts.append(f"Requirement traceability found {matched} matched, {partial} partial, and {missing} missing requirements.")
    if supported_restructures:
        parts.append("The comparison explicitly gave credit for supported equivalent-but-different structure where visible behavior remained aligned.")
    if contradictions:
        parts.append(f"{len(contradictions)} likely behavioral contradiction(s) were detected.")
    elif harmful_issues:
        parts.append(f"{len(harmful_issues)} unsupported or risky extra item(s) were identified.")
    if quality_report.get("issue_taxonomy"):
        parts.append("Quality review explicitly tracked: " + ", ".join(quality_report["issue_taxonomy"][:3]) + ".")
    if equivalence_report.get("parallel_structure_mismatch"):
        parts.append("A major parallel or orthogonal structure mismatch was detected and propagated into the final judgement.")
    elif equivalence_report.get("parallel_branch_credit"):
        parts.append("The arbiter retained credit for branch-family restructuring even though the surface form differs from the reference.")
    if equivalence_report.get("trace_conflict_count"):
        parts.append(
            f"Arbitration downgraded {int(equivalence_report.get('trace_conflict_count', 0) or 0)} trace judgement(s) after reconciling semantic support with structural conflicts."
        )
    if evidence_critic.get("warnings"):
        parts.append(f"Caution: {evidence_critic['warnings'][0]}")
    return " ".join(parts)


def maybe_refine_overall_reason(
    llm: ChatOpenAI | None,
    regime: Any,
    policy_packet: dict[str, Any],
    draft_reason: str,
    notes: list[str],
    dimension_results: list[Any],
) -> str:
    if llm is None:
        return draft_reason
    payload = invoke_llm_json(
        llm,
        [
            ("system", FINAL_SYNTHESIS_SYSTEM_PROMPT),
            (
                "user",
                "Compose a final reviewer-facing explanation without adding new findings.\n\n"
                "Return JSON with key overall_reason_text.\n\n"
                f"Regime: {getattr(regime, 'regime', '')}\n"
                f"Policy: {json.dumps(policy_packet, ensure_ascii=False, indent=2)}\n\n"
                f"Draft reason:\n{draft_reason}\n\n"
                f"Visible notes:\n{json.dumps(notes[:12], ensure_ascii=False, indent=2)}\n\n"
                f"Dimension reasons:\n{json.dumps([item.reason_text for item in dimension_results], ensure_ascii=False, indent=2)}",
            ),
        ],
    )
    if not isinstance(payload, dict):
        return draft_reason
    refined = str(payload.get("overall_reason_text") or "").strip()
    return refined or draft_reason


def synthesize_result(
    *,
    request: Any,
    backend_label: str,
    overall_score: float,
    overall_reason_text: str,
    dimension_results: list[Any],
    trace_results: list[Any],
    harmful_issues: list[Any],
    notes: list[str],
    confidence: float,
) -> ExpertReviewResult:
    result = ExpertReviewResult(
        prompt=request.prompt,
        overall_score=round(overall_score, 6),
        overall_judgement=judgement_from_score(overall_score),
        overall_reason_text=overall_reason_text,
        used_review_backend=backend_label,
        dimension_results=dimension_results,
        requirement_trace_results=trace_results,
        unsupported_model_elements=harmful_issues,
        evidence_summary=evidence_summary_from_dimensions(dimension_results),
        notes=notes,
        confidence=confidence,
    )
    return validate_result_shape(result)


__all__ = ["maybe_refine_overall_reason", "overall_reason", "synthesize_result"]
