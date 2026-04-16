from __future__ import annotations

from typing import Any

from ..expert_review_schema import DimensionReviewResult, ElementIssue, EvidenceItem, TraceLink, judgement_from_score
from ..expert_review_utils import normalize_id
from ..tools import status_counts
from .common import clip01


def compose_scores(
    dimensions: list[Any],
    request: Any,
    contract: Any,
    regime: Any,
    policy_packet: dict[str, Any],
    pred_dossier: Any,
    ref_dossier: Any,
    trace_results: list[Any],
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    evidence_critic: dict[str, Any],
) -> tuple[list[DimensionReviewResult], list[ElementIssue], float]:
    matched, partial, missing = status_counts(trace_results)
    requirement_count = max(1, len(trace_results))
    trace_ratio = (matched + 0.5 * partial) / requirement_count
    harmful_extras = list(equivalence_report.get("harmful_extras", []))
    contradictions = list(equivalence_report.get("contradictions", []))
    dependency_breaks = list(equivalence_report.get("dependency_breaks", []))
    quality_issues = list(quality_report.get("issues", []))
    allow_element_level_claims = bool(
        evidence_critic.get("allow_element_level_claims", policy_packet.get("allow_element_level_claims", False))
    )
    allow_requirement_defect_claims = bool(
        evidence_critic.get("allow_requirement_defect_claims", policy_packet.get("allow_requirement_defect_claims", False))
    )
    summary_mode = regime.regime == "summary_only"
    protocol_mode = regime.regime == "protocol_only"
    score_semantics = str(policy_packet.get("score_semantics") or "artifact_quality")
    vv_roles = list(evidence_critic.get("vv_roles", []))
    dimension_results: list[DimensionReviewResult] = []

    syntax_score = 0.18
    if pred_dossier.format_guess != "missing":
        syntax_score += 0.25
    if pred_dossier.elements:
        syntax_score += 0.18
    if pred_dossier.relations:
        syntax_score += 0.20
    if pred_dossier.format_guess in {"json_structured_model", "json_generic", "plantuml_like", "ttool_xml", "xml"}:
        syntax_score += 0.10
    if pred_dossier.observability == "low":
        syntax_score -= 0.06
    syntax_score = clip01(syntax_score)

    completeness_score = clip01(0.18 + 0.78 * trace_ratio - 0.08 * min(4, len(harmful_extras)))
    behavior_base = equivalence_report.get("equivalence_strength", trace_ratio)
    behavior_score = clip01(0.20 + 0.72 * float(behavior_base) - 0.12 * len(contradictions))
    traceability_score = clip01(0.18 + 0.76 * trace_ratio - 0.07 * min(4, len(harmful_extras)))
    clarity_score = clip01(float(quality_report.get("clarity_score_hint", 0.6)) - 0.04 * min(4, len(harmful_extras)))
    evidence_score = clip01(
        0.82
        - max(0.0, 0.86 - float(evidence_critic.get("confidence_cap", 0.7)))
        - 0.08 * len(evidence_critic.get("warnings", []))
        + (0.06 if regime.regime == "record_level" else 0.0)
    )
    summary_score_hint = clip01(float(quality_report.get("summary_score_hint", clarity_score)))
    if summary_mode:
        if score_semantics == "summary_stat_stddev":
            syntax_score = clip01(0.12 + 0.28 * syntax_score)
            completeness_score = clip01(0.05 + 0.30 * summary_score_hint)
            behavior_score = clip01(0.05 + 0.32 * summary_score_hint)
            traceability_score = clip01(0.04 + 0.24 * summary_score_hint)
            clarity_score = clip01(0.12 + 0.24 * float(quality_report.get("quality_score_hint", clarity_score)))
            evidence_score = max(evidence_score, 0.74)
        else:
            syntax_score = clip01(0.35 * syntax_score + 0.65 * summary_score_hint)
            completeness_score = clip01(0.25 * completeness_score + 0.75 * summary_score_hint)
            behavior_score = clip01(0.25 * behavior_score + 0.75 * summary_score_hint)
            traceability_score = clip01(0.20 * traceability_score + 0.80 * summary_score_hint)
            clarity_score = clip01(0.30 * clarity_score + 0.70 * float(quality_report.get("quality_score_hint", clarity_score)))
            evidence_score = max(evidence_score, 0.70)
    elif protocol_mode:
        protocol_hint = clip01(float(evidence_critic.get("protocol_assurance_score_hint", 0.34)))
        syntax_score = clip01(0.10 + 0.20 * protocol_hint)
        completeness_score = clip01(0.14 + 0.28 * protocol_hint)
        behavior_score = clip01(0.16 + 0.28 * protocol_hint)
        traceability_score = clip01(0.14 + 0.24 * protocol_hint)
        clarity_score = clip01(0.34 + 0.22 * float(quality_report.get("quality_score_hint", clarity_score)))
        evidence_score = clip01(0.48 + 0.28 * protocol_hint + 0.05 * min(4, len(vv_roles)))

    pred_markers = pred_dossier.surface_markers
    ref_markers = ref_dossier.surface_markers
    self_named_composites = pred_markers.get("self_named_composite", 0)
    if self_named_composites:
        syntax_score = clip01(syntax_score - 0.22)
        behavior_score = clip01(behavior_score - 0.16)
        clarity_score = clip01(clarity_score - 0.16)
        completeness_score = clip01(completeness_score - 0.10)
        traceability_score = clip01(traceability_score - 0.08)

    composite_transition_risk = pred_markers.get("cross_composite_transition", 0)
    if composite_transition_risk:
        penalty = min(0.24, 0.08 * composite_transition_risk)
        syntax_score = clip01(syntax_score - penalty)
        behavior_score = clip01(behavior_score - penalty)
        completeness_score = clip01(completeness_score - min(0.16, penalty))
        traceability_score = clip01(traceability_score - min(0.12, penalty))
    if self_named_composites or composite_transition_risk:
        structural_cap = clip01(0.16 + 0.55 * syntax_score)
        completeness_score = min(completeness_score, structural_cap)
        traceability_score = min(traceability_score, structural_cap)

    if ref_markers["parallel"] > pred_markers["parallel"]:
        completeness_score = clip01(completeness_score - 0.10)
        behavior_score = clip01(behavior_score - 0.10)
        traceability_score = clip01(traceability_score - 0.06)
    pseudostate_gap = (
        max(0, ref_markers["choice"] - pred_markers["choice"])
        + max(0, ref_markers["fork"] - pred_markers["fork"])
        + max(0, ref_markers["join"] - pred_markers["join"])
        + max(0, ref_markers["junction"] - pred_markers["junction"])
    )
    if pseudostate_gap >= 2:
        penalty = min(0.24, pseudostate_gap * 0.05)
        completeness_score = clip01(completeness_score - penalty)
        behavior_score = clip01(behavior_score - penalty)
        traceability_score = clip01(traceability_score - min(0.12, penalty * 0.75))
        pseudo_cap = clip01(0.20 + 0.60 * behavior_score)
        completeness_score = min(completeness_score, pseudo_cap)
        traceability_score = min(traceability_score, pseudo_cap)

    if equivalence_report.get("parallel_structure_mismatch"):
        completeness_score = clip01(completeness_score - 0.18)
        behavior_score = clip01(behavior_score - 0.24)
        traceability_score = clip01(traceability_score - 0.16)
        clarity_score = clip01(clarity_score - 0.10)
        structural_cap = clip01(0.18 + 0.52 * behavior_score)
        completeness_score = min(completeness_score, structural_cap)
        traceability_score = min(traceability_score, structural_cap)
    elif equivalence_report.get("parallel_branch_credit"):
        behavior_score = clip01(behavior_score + 0.10)
        completeness_score = clip01(completeness_score + 0.06)
        traceability_score = clip01(traceability_score + 0.05)

    if dependency_breaks:
        penalty = min(0.28, 0.07 * len(dependency_breaks))
        completeness_score = clip01(completeness_score - min(0.18, penalty * 0.70))
        behavior_score = clip01(behavior_score - penalty)
        traceability_score = clip01(traceability_score - min(0.16, penalty * 0.80))
        clarity_score = clip01(clarity_score - min(0.10, penalty * 0.45))

    trace_conflict_count = int(equivalence_report.get("trace_conflict_count", 0) or 0)
    if trace_conflict_count:
        penalty = min(0.16, 0.05 * trace_conflict_count)
        completeness_score = clip01(completeness_score - penalty)
        behavior_score = clip01(behavior_score - min(0.12, penalty))
        traceability_score = clip01(traceability_score - penalty)

    if summary_mode and not allow_requirement_defect_claims:
        completeness_score = max(completeness_score, 0.18 if score_semantics == "summary_stat_stddev" else 0.42)
        traceability_score = max(traceability_score, 0.16 if score_semantics == "summary_stat_stddev" else 0.40)
    if protocol_mode:
        completeness_score = max(completeness_score, 0.22)
        behavior_score = max(behavior_score, 0.22)
        traceability_score = max(traceability_score, 0.20)

    score_map = {
        "notation_syntax": syntax_score,
        "semantic_completeness": completeness_score,
        "behavioral_consistency": behavior_score,
        "requirement_traceability": traceability_score,
        "pragmatic_clarity": clarity_score,
        "evidence_discipline": evidence_score,
    }
    reason_map = {
        "notation_syntax": (
            "No concrete artifact was provided, so notation review can only reflect what the public protocol says it checks."
            if protocol_mode
            else "Only coarse structural observables are available, so notation review remains summary-level rather than element-level."
            if summary_mode
            else "The predicted artifact is "
            + ("structurally reviewable" if syntax_score >= 0.7 else "only partially well-formed")
            + f", with format guess `{pred_dossier.format_guess}` and {len(pred_dossier.elements)} visible elements. "
            + pred_dossier.observability_reason
        ),
        "semantic_completeness": (
            f"Requirement coverage was judged as a coarse summary statistic (`{policy_packet.get('aggregate_signal')}`), not as direct per-element matching."
            if summary_mode and not allow_requirement_defect_claims
            else "Protocol-only evidence does not justify per-element completeness claims; only coarse assurance coverage can be reported."
            if protocol_mode
            else f"{matched} requirement(s) were matched, {partial} partial, and {missing} missing. "
            + (
                "Key requirement-driven content is largely covered."
                if completeness_score >= 0.7
                else "Important requirement-driven content is still missing or weakly evidenced."
            )
        ),
        "behavioral_consistency": (
            "Behavioral consistency was judged at the public-summary level rather than by exact transition-by-transition replay."
            if summary_mode
            else "Behavioral judgement in protocol-only mode reflects what the evaluation process can validate, not hidden artifact behavior."
            if protocol_mode
            else "Behavioral judgement emphasizes semantic equivalence rather than surface isomorphism. "
            + (
                "The prediction preserves core behavior reasonably well."
                if behavior_score >= 0.7
                else "Behavioral preservation is incomplete or contradicted by visible evidence."
            )
            + (
                " The arbiter also found dependency-sensitive mismatches between supported states and their attached transitions."
                if dependency_breaks
                else ""
            )
        ),
        "requirement_traceability": (
            "Traceability remained coarse because the current evidence regime does not justify direct requirement-to-element blame."
            if summary_mode and not allow_requirement_defect_claims
            else "Protocol-only evidence supports process-level traceability comments only; no direct requirement-to-element trace can be claimed."
            if protocol_mode
            else "Traceability was assessed from explicit requirement-to-artifact links and unsupported extras. "
            + (
                "Most major requirements can be grounded to visible predicted content."
                if traceability_score >= 0.7
                else "Too many requirements or predicted structures remain weakly grounded."
            )
            + (
                f" {trace_conflict_count} trace judgement(s) were downgraded after arbitration."
                if trace_conflict_count
                else ""
            )
        ),
        "pragmatic_clarity": (
            f"Quality inspection found grounded-ratio={quality_report.get('grounded_ratio', 0.0):.2f}, "
            f"generic-name-count={quality_report.get('generic_name_count', 0)}, "
            f"and score-semantics=`{score_semantics}`. "
            + (
                "The artifact remains reasonably disciplined."
                if clarity_score >= 0.7
                else "Readability or proportional complexity is a visible weakness."
            )
        ),
        "evidence_discipline": (
            f"Current regime is `{regime.regime}` with policy profile `{policy_packet.get('profile_name')}`. "
            + (
                "The review stayed broadly within the visible evidence."
                if evidence_score >= 0.7
                else "The evidence regime forces caution, and confidence must remain restrained."
            )
            + (f" Visible V&V roles: {', '.join(vv_roles[:4])}." if vv_roles else "")
        ),
    }
    evidence_issues = [
        ElementIssue(
            element_id=f"evidence_warning_{idx}",
            element_kind="evidence_regime",
            element_text=warning,
            issue_type="evidence_overreach",
            reason_text=warning,
        )
        for idx, warning in enumerate(evidence_critic.get("warnings", [])[:2], start=1)
    ]
    evidence_map = {
        "notation_syntax": pred_dossier.evidence[:2],
        "semantic_completeness": [
            EvidenceItem(source="input", locator=None, snippet=item.requirement_text, explanation=item.reason_text)
            for item in trace_results[:2]
        ],
        "behavioral_consistency": list(equivalence_report.get("evidence", []))[:2],
        "requirement_traceability": [
            EvidenceItem(source="input", locator=None, snippet=item.requirement_text, explanation=item.reason_text)
            for item in trace_results[:2]
        ],
        "pragmatic_clarity": list(quality_report.get("evidence", []))[:2],
        "evidence_discipline": list(evidence_critic.get("evidence", []))[:2],
    }
    issue_map = {
        "notation_syntax": [],
        "semantic_completeness": harmful_extras[:4] if allow_element_level_claims else [],
        "behavioral_consistency": (contradictions + dependency_breaks)[:4] if allow_element_level_claims else [],
        "requirement_traceability": (harmful_extras + dependency_breaks)[:6] if allow_element_level_claims else [],
        "pragmatic_clarity": quality_issues[:6],
        "evidence_discipline": evidence_issues[:2],
    }
    trace_link_map = {
        "notation_syntax": [],
        "semantic_completeness": [
            TraceLink(
                source_id=item.requirement_id,
                target_id=item.matched_element_ids[0],
                relation=item.status,
                reason_text=item.reason_text,
            )
            for item in trace_results
            if item.matched_element_ids
        ][:6]
        if allow_element_level_claims
        else [],
        "behavioral_consistency": [],
        "requirement_traceability": [
            TraceLink(
                source_id=item.requirement_id,
                target_id=item.matched_element_ids[0],
                relation=item.status,
                reason_text=item.reason_text,
            )
            for item in trace_results
            if item.matched_element_ids
        ][:6]
        if allow_element_level_claims
        else [],
        "pragmatic_clarity": [],
        "evidence_discipline": [],
    }
    focus_norm = {normalize_id(item) for item in contract.requested_focus}
    issue_taxonomy_map = {
        "notation_syntax": (
            ["syntax_or_notation"]
            if not protocol_mode
            and (
                syntax_score < 0.60
                or (regime.regime == "record_level" and (trace_ratio < 0.98 or pred_dossier.structural_warnings))
            )
            else []
        ),
        "semantic_completeness": (
            [
                *(
                    ["missing_required_behavior"]
                    if allow_requirement_defect_claims
                    and (missing or partial or (regime.regime == "record_level" and trace_ratio < 0.98))
                    else []
                ),
                *(["unsupported_extra_structure"] if harmful_extras and allow_element_level_claims else []),
            ]
        ),
        "behavioral_consistency": ["wrong_guard_or_trigger"] if (contradictions or dependency_breaks) and allow_element_level_claims else [],
        "requirement_traceability": (
            [
                *(
                    ["missing_required_behavior"]
                    if allow_requirement_defect_claims
                    and (missing or partial or (regime.regime == "record_level" and trace_ratio < 0.98))
                    else []
                ),
                *(
                    ["unsupported_extra_structure"]
                    if allow_element_level_claims
                    and (
                        harmful_extras
                        or equivalence_report.get("missing_items")
                        or (regime.regime == "record_level" and trace_ratio < 0.98)
                    )
                    else []
                ),
            ]
        ),
        "pragmatic_clarity": (
            list(quality_report.get("issue_taxonomy", []))
            if clarity_score < 0.60 or {"clarity", "quality"} & focus_norm
            else []
        ),
        "evidence_discipline": list(evidence_critic.get("issue_taxonomy", [])),
    }

    for dimension in dimensions:
        score = round(score_map[dimension.name], 6)
        dimension_results.append(
            DimensionReviewResult(
                dimension_name=dimension.name,
                title=dimension.title,
                score=score,
                judgement=judgement_from_score(score),
                reason_text=reason_map[dimension.name],
                evidence=evidence_map[dimension.name],
                trace_links=trace_link_map[dimension.name],
                issues=issue_map[dimension.name],
                metric_payload={
                    "regime": regime.regime,
                    "format_guess": pred_dossier.format_guess,
                    "analysis_mode": pred_dossier.analysis_mode,
                    "pred_observability": pred_dossier.observability,
                    "ref_observability": ref_dossier.observability,
                    "trace_ratio": round(trace_ratio, 6),
                    "structural_warning_count": len(pred_dossier.structural_warnings),
                    "extraction_conflict_count": len(pred_dossier.extraction_conflicts),
                    "parallel_structure_mismatch": bool(equivalence_report.get("parallel_structure_mismatch")),
                    "parallel_branch_credit": bool(equivalence_report.get("parallel_branch_credit")),
                    "trace_conflict_count": trace_conflict_count,
                    "dependency_break_count": len(dependency_breaks),
                    "issue_taxonomy": issue_taxonomy_map[dimension.name],
                    "policy_profile": policy_packet.get("profile_name"),
                    "score_semantics": score_semantics,
                    "aggregate_signal": policy_packet.get("aggregate_signal"),
                    "allow_element_level_claims": allow_element_level_claims,
                    "allow_requirement_defect_claims": allow_requirement_defect_claims,
                    "vv_roles": vv_roles,
                    "missing_evidence_flags": evidence_critic.get("missing_evidence_flags", []),
                },
                confidence=min(float(evidence_critic.get("confidence_cap", 0.7)), 0.90),
            )
        )

    total_weight = sum(item.weight for item in dimensions) or 1.0
    overall_score = sum(item.score * dimension.weight for item, dimension in zip(dimension_results, dimensions)) / total_weight
    if summary_mode:
        blend = 0.20 if score_semantics == "summary_stat_stddev" else 0.35
        overall_score = clip01(blend * overall_score + (1.0 - blend) * summary_score_hint)
    elif protocol_mode:
        protocol_hint = clip01(float(evidence_critic.get("protocol_assurance_score_hint", 0.34)))
        overall_score = clip01(0.25 * overall_score + 0.75 * protocol_hint)
    return dimension_results, harmful_extras + contradictions + dependency_breaks, clip01(overall_score)


def final_confidence(
    regime: Any,
    policy_packet: dict[str, Any],
    trace_results: list[Any],
    equivalence_report: dict[str, Any],
    evidence_critic: dict[str, Any],
) -> float:
    if not trace_results:
        base = 0.42
    else:
        base = sum(item.confidence for item in trace_results) / len(trace_results)
    base = 0.55 * base + 0.45 * float(equivalence_report.get("confidence", 0.55))
    if regime.regime == "record_level":
        base = 0.08 + 0.78 * base
    if policy_packet.get("score_semantics") == "summary_stat_stddev":
        base -= 0.06
    if regime.regime == "protocol_only":
        base = 0.40 + 0.08 * min(4, len(evidence_critic.get("vv_roles", [])))
    if equivalence_report.get("parallel_structure_mismatch"):
        base -= 0.10
    if equivalence_report.get("trace_conflict_count"):
        base -= min(0.10, 0.03 * int(equivalence_report.get("trace_conflict_count", 0) or 0))
    return round(min(float(evidence_critic.get("confidence_cap", 0.75)), clip01(base)), 6)


__all__ = ["compose_scores", "final_confidence"]
