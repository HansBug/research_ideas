from __future__ import annotations

import json
from typing import Any

from langchain_openai import ChatOpenAI

from ..schema import ExpertReviewResult, judgement_from_score
from ..prompts.synthesis import FINAL_SYNTHESIS_SYSTEM_PROMPT
from ..tools import evidence_summary_from_dimensions, validate_result_shape
from .llm_helpers import invoke_llm_json


def _dimension_score_map(dimension_results: list[Any]) -> dict[str, float]:
    return {str(item.dimension_name): float(item.score) for item in dimension_results}


def coarse_overall_judgement(
    regime: Any,
    policy_packet: dict[str, Any],
    overall_score: float,
    dimension_results: list[Any],
) -> str:
    if not dimension_results:
        return judgement_from_score(overall_score)
    scores = _dimension_score_map(dimension_results)
    completeness = scores.get("semantic_completeness", overall_score)
    behavior = scores.get("behavioral_consistency", overall_score)
    traceability = scores.get("requirement_traceability", overall_score)
    clarity = scores.get("pragmatic_clarity", overall_score)
    evidence = scores.get("evidence_discipline", overall_score)
    support_anchor = 0.34 * behavior + 0.28 * traceability + 0.22 * completeness + 0.16 * clarity
    judgement_anchor = overall_score + 0.42 * max(0.0, support_anchor - overall_score)
    score_semantics = str(policy_packet.get("score_semantics") or "artifact_quality")
    if getattr(regime, "regime", "") == "summary_only" and score_semantics != "summary_stat_stddev":
        public_anchor = 0.45 * support_anchor + 0.30 * clarity + 0.25 * evidence
        judgement_anchor = max(judgement_anchor, 0.52 * overall_score + 0.48 * public_anchor)
    if getattr(regime, "regime", "") == "protocol_only":
        judgement_anchor = min(max(judgement_anchor, 0.35 * overall_score + 0.65 * evidence), 0.72)
    if score_semantics == "summary_stat_stddev":
        judgement_anchor = min(judgement_anchor, 0.72)
    if policy_packet.get("component_review_mode"):
        component_f1 = dimension_results[0].metric_payload.get("component_public_f1")
        if component_f1 is not None:
            judgement_anchor = float(component_f1)
    if evidence < 0.40:
        judgement_anchor = min(judgement_anchor, 0.54)
    if min(completeness, behavior, traceability) < 0.38:
        judgement_anchor = min(judgement_anchor, 0.54)
    return judgement_from_score(max(0.0, min(1.0, judgement_anchor)))


def overall_reason(
    regime: Any,
    policy_packet: dict[str, Any],
    overall_score: float,
    dimension_results: list[Any],
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
    judgement = coarse_overall_judgement(regime, policy_packet, overall_score, dimension_results)
    score_map = _dimension_score_map(dimension_results)
    strengths: list[str] = []
    weaknesses: list[str] = []
    if score_map.get("semantic_completeness", 0.0) >= 0.72:
        strengths.append("coverage")
    if score_map.get("behavioral_consistency", 0.0) >= 0.72:
        strengths.append("behavior")
    if score_map.get("requirement_traceability", 0.0) >= 0.72:
        strengths.append("traceability")
    if score_map.get("pragmatic_clarity", 0.0) >= 0.72:
        strengths.append("clarity")
    if score_map.get("semantic_completeness", 1.0) < 0.55:
        weaknesses.append("coverage gaps")
    if score_map.get("behavioral_consistency", 1.0) < 0.55:
        weaknesses.append("behavioral mismatch")
    if score_map.get("requirement_traceability", 1.0) < 0.55:
        weaknesses.append("weak traceability")
    if score_map.get("evidence_discipline", 1.0) < 0.60:
        weaknesses.append("evidence limits")

    parts = [f"Overall judgement: {judgement}, with an overall score of {overall_score:.3f}."]
    if strengths and weaknesses:
        parts.append(
            f"The review sees solid {'/'.join(strengths[:2])}, but the main concern is {'/'.join(weaknesses[:2])}."
        )
    elif strengths:
        parts.append(f"The strongest visible aspect is {'/'.join(strengths[:2])}.")
    elif weaknesses:
        parts.append(f"The main weakness is {'/'.join(weaknesses[:2])}.")
    if regime.regime == "summary_only":
        parts.append(
            "This remains a coarse summary-level judgement rather than a direct per-element defect review."
            if score_semantics != "summary_stat_stddev"
            else "This row behaves like an aggregate variability or dispersion statistic, so the judgement stays intentionally coarse."
        )
    elif regime.regime == "protocol_only":
        parts.append("This is a protocol-level assurance review, not a direct artifact-level defect review.")
        if evidence_critic.get("vv_roles"):
            parts.append("Recognized V&V roles: " + ", ".join(evidence_critic["vv_roles"][:4]) + ".")
    else:
        parts.append(f"Requirement traceability found {matched} matched, {partial} partial, and {missing} missing requirements.")
    if supported_restructures:
        parts.append(
            "The review still gives credit for equivalent-but-different structure where the visible behavior remains aligned."
        )
    if equivalence_report.get("parallel_structure_mismatch"):
        parts.append("A parallel or orthogonal structure mismatch remains a major concern.")
    elif equivalence_report.get("parallel_branch_credit"):
        parts.append("The prediction looks closer to branch-family restructuring than to a genuine semantic defect.")
    if contradictions:
        parts.append(f"{len(contradictions)} behavior-level contradiction or conflict signal(s) were retained in the final view.")
    elif harmful_issues:
        parts.append(f"{len(harmful_issues)} unsupported or risky extra structure item(s) were identified.")
    if equivalence_report.get("trace_conflict_count"):
        parts.append(
            f"{int(equivalence_report.get('trace_conflict_count', 0) or 0)} trace judgement(s) had to be downgraded after arbitration."
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
    policy_packet = {}
    if dimension_results and isinstance(dimension_results[0].metric_payload, dict):
        policy_packet = dict(dimension_results[0].metric_payload)
    regime_name = str(policy_packet.get("regime") or request.metadata.get("review_surface") or "")
    regime_proxy = type("RegimeProxy", (), {"regime": regime_name})()
    result = ExpertReviewResult(
        prompt=request.prompt,
        overall_score=round(overall_score, 6),
        overall_judgement=coarse_overall_judgement(regime_proxy, policy_packet, overall_score, dimension_results),
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


__all__ = ["coarse_overall_judgement", "maybe_refine_overall_reason", "overall_reason", "synthesize_result"]
