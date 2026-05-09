from __future__ import annotations

from typing import Any

from ..schema import DimensionReviewResult, ElementIssue, EvidenceItem, TraceLink, judgement_from_score
from ..utils import normalize_id
from ..tools import status_counts
from .common import clip01
from .rubric_scorer import RubricScore, llm_rubric_score


def _missing_signal_count(items: list[str]) -> int:
    count = 0
    for item in items:
        text = str(item or "").strip()
        if not text:
            continue
        count += max(1, text.count("|") + 1)
    return count


def _safe_int(value: Any) -> int | None:
    try:
        return int(float(value))
    except Exception:
        return None


def _f1_from_tp_fp_fn(tp: int, fp: int, fn: int) -> float:
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return 0.0 if precision + recall == 0 else (2 * precision * recall) / (precision + recall)


def _normalized_locator_token(value: Any, fallback: str) -> str:
    token = normalize_id(str(value or ""))
    return token or fallback


def _requirement_locator(requirement_id: str) -> str:
    return f"input:requirement:{_normalized_locator_token(requirement_id, 'unknown_requirement')}"


def _prediction_locator(element_id: str) -> str:
    return f"prediction:element:{_normalized_locator_token(element_id, 'unknown_element')}"


def _trace_dimension_evidence(trace_results: list[Any], *, limit: int = 2) -> list[EvidenceItem]:
    status_priority = {"missing": 0, "partial": 1, "matched": 2}
    ranked = sorted(
        trace_results,
        key=lambda item: (
            status_priority.get(str(getattr(item, "status", "")), 3),
            -len(getattr(item, "matched_element_ids", [])),
            -float(getattr(item, "confidence", 0.0) or 0.0),
        ),
    )
    evidence: list[EvidenceItem] = []
    seen: set[tuple[str, str]] = set()
    for item in ranked:
        req_locator = _requirement_locator(str(getattr(item, "requirement_id", "")))
        req_key = ("input", req_locator)
        if req_key not in seen:
            seen.add(req_key)
            evidence.append(
                EvidenceItem(
                    source="input",
                    locator=req_locator,
                    snippet=str(getattr(item, "requirement_text", "") or ""),
                    explanation=str(getattr(item, "reason_text", "") or ""),
                )
            )
        matched_ids = list(getattr(item, "matched_element_ids", []))
        if matched_ids:
            pred_locator = _prediction_locator(str(matched_ids[0]))
            pred_key = ("prediction", pred_locator)
            if pred_key not in seen:
                seen.add(pred_key)
                evidence.append(
                    EvidenceItem(
                        source="prediction",
                        locator=pred_locator,
                        snippet=str(matched_ids[0]),
                        explanation=(
                            f"Predicted element anchor currently used for requirement {getattr(item, 'requirement_id', '')}."
                        ),
                    )
                )
        if len(evidence) >= limit:
            break
    return evidence[:limit]


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
    *,
    llm: Any = None,
) -> tuple[list[DimensionReviewResult], list[ElementIssue], float]:
    matched, partial, missing = status_counts(trace_results)
    requirement_count = max(1, len(trace_results))
    matched_ratio = matched / requirement_count
    partial_ratio = partial / requirement_count
    missing_ratio = missing / requirement_count
    trace_ratio = (matched + 0.5 * partial) / requirement_count
    harmful_extras = list(equivalence_report.get("harmful_extras", []))
    missing_items = list(equivalence_report.get("missing_items", []))
    contradictions = list(equivalence_report.get("contradictions", []))
    dependency_breaks = list(equivalence_report.get("dependency_breaks", []))
    quality_issues = list(quality_report.get("issues", []))
    harmful_count = len(harmful_extras)
    contradiction_count = len(contradictions)
    dependency_break_count = len(dependency_breaks)
    missing_signal_count = _missing_signal_count(missing_items)
    equivalence_strength = float(equivalence_report.get("equivalence_strength", trace_ratio))
    ref_element_coverage = clip01(float(equivalence_report.get("ref_element_coverage", equivalence_strength)))
    ref_relation_coverage = clip01(float(equivalence_report.get("ref_relation_coverage", equivalence_strength)))
    reference_alignment = clip01(0.45 * ref_element_coverage + 0.55 * ref_relation_coverage)
    trace_conflict_count = int(equivalence_report.get("trace_conflict_count", 0) or 0)
    allow_element_level_claims = bool(
        evidence_critic.get("allow_element_level_claims", policy_packet.get("allow_element_level_claims", False))
    )
    allow_requirement_defect_claims = bool(
        evidence_critic.get("allow_requirement_defect_claims", policy_packet.get("allow_requirement_defect_claims", False))
    )
    summary_mode = regime.regime == "summary_only"
    protocol_mode = regime.regime == "protocol_only"
    score_semantics = str(policy_packet.get("score_semantics") or "artifact_quality")
    summary_row_type = str(policy_packet.get("summary_row_type") or "summary_public_score")
    summary_target = str(policy_packet.get("summary_target") or "unknown")
    summary_target_axis = str(policy_packet.get("summary_target_axis") or "generic_target")
    record_diagram_type = str(policy_packet.get("record_diagram_type") or "unknown")
    component_target = str(policy_packet.get("component_target") or "unknown")
    component_review_mode = bool(policy_packet.get("component_review_mode", False))
    component_public_tp = _safe_int(policy_packet.get("component_public_tp"))
    component_public_fp = _safe_int(policy_packet.get("component_public_fp"))
    component_public_fn = _safe_int(policy_packet.get("component_public_fn"))
    component_pred_total = _safe_int(policy_packet.get("component_pred_total"))
    component_reference_total = _safe_int(policy_packet.get("component_reference_total"))
    component_public_f1 = None
    if component_public_tp is not None and component_public_fp is not None and component_public_fn is not None:
        component_public_f1 = _f1_from_tp_fp_fn(component_public_tp, component_public_fp, component_public_fn)
    vv_roles = list(evidence_critic.get("vv_roles", []))
    evidence_warning_count = len(evidence_critic.get("warnings", []))
    missing_flag_count = len(evidence_critic.get("missing_evidence_flags", []))
    behavior_issue_types = {
        str(item.issue_type)
        for item in contradictions + dependency_breaks
        if str(getattr(item, "issue_type", "")).strip()
    }
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

    completeness_score = clip01(0.18 + 0.78 * trace_ratio - 0.08 * min(4, harmful_count))
    behavior_base = equivalence_strength
    behavior_score = clip01(0.20 + 0.72 * behavior_base - 0.12 * contradiction_count)
    traceability_score = clip01(0.18 + 0.76 * trace_ratio - 0.07 * min(4, harmful_count))
    clarity_score = clip01(float(quality_report.get("clarity_score_hint", 0.6)) - 0.04 * min(4, len(harmful_extras)))
    evidence_score = clip01(
        0.82
        - max(0.0, 0.86 - float(evidence_critic.get("confidence_cap", 0.7)))
        - 0.08 * len(evidence_critic.get("warnings", []))
        + (0.06 if regime.regime == "record_level" else 0.0)
    )

    # ─── S2-Q1: rubric-LLM override (feature flag) ────────────────────────────
    # Replaces the 6 deterministic dim scores above with LLM rubric outputs,
    # while keeping the post-transforms (summary_mode / protocol_mode /
    # component_review_mode blends) intact. Sanity bounds prevent the LLM
    # from giving extreme scores (Phase 15 / Week 0 LLM-mode showed record
    # ScoreAlign collapsing -19.30 without rubric anchoring).
    #
    # Iter feature flags (read from request.metadata):
    #   rubric_llm_enabled       — master on/off
    #   rubric_iter_a_asymmetric — Iter-A: regime-aware bound widths
    #   rubric_iter_b_diff_prompt — Iter-B: append differentiation hint
    #   rubric_iter_c_regimes    — Iter-C: list of regimes to actually apply
    #                              rubric on (e.g. ["record_level"]); empty
    #                              list means apply on all regimes
    rubric_metadata: dict[str, RubricScore] = {}
    request_metadata = getattr(request, "metadata", None) or {}
    rubric_flag = bool(
        policy_packet.get("rubric_llm_enabled", False)
        or request_metadata.get("rubric_llm_enabled", False)
    )
    iter_a_asymmetric = bool(request_metadata.get("rubric_iter_a_asymmetric", False))
    iter_b_diff_prompt = bool(request_metadata.get("rubric_iter_b_diff_prompt", False))
    iter_c_regimes = list(request_metadata.get("rubric_iter_c_regimes", []) or [])
    # Q3-paraphrase / Q3-temp: per-rerun overrides driven by SC wrapper
    rubric_prompt_variant = str(request_metadata.get("rubric_prompt_variant", "v1") or "v1")
    rubric_temp_override = request_metadata.get("rubric_temperature_override")
    if rubric_temp_override is not None:
        try:
            rubric_temp_override = float(rubric_temp_override)
        except (TypeError, ValueError):
            rubric_temp_override = None

    # Iter-C: selective application by regime
    regime_label_for_check = str(regime.regime if hasattr(regime, "regime") else regime)
    if rubric_flag and iter_c_regimes:
        rubric_active_for_regime = regime_label_for_check in iter_c_regimes
        if not rubric_active_for_regime:
            rubric_flag = False  # skip rubric for this regime

    if rubric_flag and llm is not None:
        regime_label = str(regime.regime if hasattr(regime, "regime") else regime)
        input_text_summary = str(getattr(request, "input_text", "") or "")
        pred_text_summary = str(getattr(request, "pred_output", "") or "")
        ref_text_summary = getattr(request, "ref_output", None)
        ref_text_summary = str(ref_text_summary) if ref_text_summary else None
        common_extras = {
            "trace_ratio": round(trace_ratio, 3),
            "matched_ratio": round(matched_ratio, 3),
            "missing_ratio": round(missing_ratio, 3),
            "harmful_count": harmful_count,
            "contradiction_count": contradiction_count,
            "equivalence_strength": round(equivalence_strength, 3),
        }
        for dim_name, det_estimate, current_score_var in [
            ("notation_syntax", syntax_score, "syntax_score"),
            ("semantic_completeness", completeness_score, "completeness_score"),
            ("behavioral_consistency", behavior_score, "behavior_score"),
            ("requirement_traceability", traceability_score, "traceability_score"),
            ("pragmatic_clarity", clarity_score, "clarity_score"),
            ("evidence_discipline", evidence_score, "evidence_score"),
        ]:
            rubric_result = llm_rubric_score(
                dim_name,
                pred_summary=pred_text_summary,
                ref_summary=ref_text_summary,
                input_summary=input_text_summary,
                regime_label=regime_label,
                deterministic_estimate=det_estimate,
                extra_signals=common_extras,
                llm=llm,
                asymmetric_bounds=iter_a_asymmetric,
                differentiation_mode=iter_b_diff_prompt,
                prompt_variant=rubric_prompt_variant,
                temperature_override=rubric_temp_override,
            )
            rubric_metadata[dim_name] = rubric_result
            if dim_name == "notation_syntax":
                syntax_score = rubric_result.score
            elif dim_name == "semantic_completeness":
                completeness_score = rubric_result.score
            elif dim_name == "behavioral_consistency":
                behavior_score = rubric_result.score
            elif dim_name == "requirement_traceability":
                traceability_score = rubric_result.score
            elif dim_name == "pragmatic_clarity":
                clarity_score = rubric_result.score
            elif dim_name == "evidence_discipline":
                evidence_score = rubric_result.score

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
    if component_review_mode and component_public_f1 is not None:
        syntax_score = clip01(0.30 * syntax_score + 0.70 * component_public_f1)
        completeness_score = clip01(0.08 * completeness_score + 0.92 * component_public_f1)
        behavior_score = clip01(0.08 * behavior_score + 0.92 * component_public_f1)
        traceability_score = clip01(0.08 * traceability_score + 0.92 * component_public_f1)
        clarity_score = clip01(0.20 * clarity_score + 0.80 * component_public_f1)
        evidence_score = clip01(0.35 * evidence_score + 0.65 * component_public_f1)

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

    if missing_ratio >= 0.45 and trace_ratio <= 0.55:
        missing_cap = clip01(0.22 + 0.46 * trace_ratio + 0.18 * reference_alignment)
        completeness_score = min(completeness_score, missing_cap)
        traceability_score = min(traceability_score, missing_cap)

    if dependency_break_count or trace_conflict_count or equivalence_report.get("parallel_structure_mismatch"):
        behavior_cap = clip01(0.22 + 0.42 * equivalence_strength + 0.18 * matched_ratio)
        behavior_score = min(behavior_score, behavior_cap)

    if summary_mode and not allow_requirement_defect_claims:
        completeness_score = max(completeness_score, 0.18 if score_semantics == "summary_stat_stddev" else 0.42)
        traceability_score = max(traceability_score, 0.16 if score_semantics == "summary_stat_stddev" else 0.40)
    if protocol_mode:
        completeness_score = max(completeness_score, 0.22)
        behavior_score = max(behavior_score, 0.22)
        traceability_score = max(traceability_score, 0.20)

    evidence_score = clip01(evidence_score - min(0.22, 0.025 * evidence_warning_count + 0.020 * missing_flag_count))
    if missing_flag_count:
        evidence_cap = clip01(0.84 - 0.03 * max(0, missing_flag_count - 1))
        if summary_mode and not allow_element_level_claims:
            evidence_cap = min(evidence_cap, 0.74)
        if component_review_mode:
            evidence_cap = min(evidence_cap, 0.78)
        evidence_score = min(evidence_score, evidence_cap)

    summary_score_stretch = 1.0
    summary_score_adjustment = 0.0
    summary_target_offset = float(policy_packet.get("summary_target_semantic_bias", 0.0) or 0.0)
    summary_row_interaction = float(policy_packet.get("summary_row_target_interaction_bias", 0.0) or 0.0)
    summary_row_bonus = max(0.0, summary_row_interaction)
    summary_target_penalty = max(0.0, -summary_row_interaction)
    summary_semantic_adjustment = 0.0
    summary_public_signal = clip01(0.65 * summary_score_hint + 0.20 * evidence_score + 0.15 * clarity_score)
    summary_hidden_risk = clip01(
        0.50 * (1.0 - summary_score_hint)
        + 0.25 * (1.0 - clarity_score)
        + 0.25 * min(1.0, len(pred_dossier.structural_warnings) / 4.0)
    )
    # Tier 1 ablation 验证：summary_public_gain / summary_hidden_risk_scale 单删 |ΔHAI| < 0.05；
    # 已从 policy_library 删字段，这里改为常量 1.0 内联化（即直接乘 1）。
    summary_row_pivot = 0.5
    if summary_mode:
        if summary_row_type == "raw_score_row":
            summary_row_pivot = 0.68
            summary_score_stretch = 1.10
        elif summary_row_type == "run_level_score":
            summary_row_pivot = 0.75
            summary_score_stretch = 1.22
        elif summary_row_type == "aggregate_stddev":
            summary_row_pivot = 0.15
            summary_score_stretch = 1.06
        else:
            summary_row_pivot = 0.41
            summary_score_stretch = 1.01

        row_semantic_gain = {
            "raw_score_row": 1.00,
            "run_level_score": 0.86,
            "aggregate_average": 0.58,
            "aggregate_max": 0.62,
            "aggregate_min": 0.62,
            "summary_public_score": 0.46,
            "aggregate_stddev": 0.0,
        }.get(summary_row_type, 0.46)
        row_semantic_bias = {
            "raw_score_row": 0.03,
            "run_level_score": 0.01,
            "aggregate_average": -0.01,
            "aggregate_max": 0.0,
            "aggregate_min": 0.0,
            "summary_public_score": 0.0,
            "aggregate_stddev": -0.02,
        }.get(summary_row_type, 0.0)
        if summary_target_axis == "coarse_public_quality_target":
            summary_semantic_adjustment = (
                0.14 * (summary_public_signal - 0.44)
                - 0.03 * summary_hidden_risk
            )
        elif summary_target_axis == "structure_intensive_target":
            summary_semantic_adjustment = (
                0.06 * (summary_public_signal - 0.58)
                - 0.11 * summary_hidden_risk
            )
        else:
            summary_semantic_adjustment = (
                0.10 * (summary_public_signal - 0.50)
                - 0.05 * summary_hidden_risk
            )
        summary_score_adjustment = (
            summary_target_offset
            + summary_row_interaction
            + row_semantic_bias
            + row_semantic_gain * summary_semantic_adjustment
        )

    # Tier 4 step a：移除 record-level 大量 rescue/penalty 分支（A7 strict 0、A8 反向、A6 dead）；
    # 但保留 record_reference_alignment_rescue 的 high_alignment_bonus —— Step 4a 实测移除整段后
    # HAI 从 87.11 掉到 86.27 (-0.84)，需要把这个常触发的 bonus 加回来。
    record_score_stretch = 1.0
    record_high_alignment_bonus = 0.0
    record_score_adjustment = 0.0
    record_diagram_offset = float(policy_packet.get("record_diagram_semantic_bias", 0.0) or 0.0)
    record_alignment_matched_floor = float(policy_packet.get("record_alignment_matched_floor", 0.0) or 0.0)
    if regime.regime == "record_level":
        record_score_stretch = 1.18
        no_core_issues = dependency_break_count == 0 and trace_conflict_count == 0
        if (
            matched_ratio >= record_alignment_matched_floor
            and partial_ratio >= 0.50
            and equivalence_strength >= 0.75
            and reference_alignment >= 0.85
            and missing_signal_count <= 1
            and no_core_issues
        ):
            quality = min(
                1.0,
                0.20 * matched_ratio + 0.30 * partial_ratio + 0.25 * equivalence_strength + 0.25 * reference_alignment,
            )
            record_high_alignment_bonus = 0.16 * quality
        record_score_adjustment = record_diagram_offset + record_high_alignment_bonus

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
                " The main mismatch is in guard or trigger semantics."
                if "wrong_guard_or_trigger" in behavior_issue_types
                else ""
            )
            + (
                " The main mismatch is in action or effect semantics."
                if "wrong_action_or_effect" in behavior_issue_types
                else ""
            )
            + (
                " Dependency-sensitive mismatches between supported states and their attached transitions are also detected."
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
                f" {trace_conflict_count} trace judgement(s) conflicted with the equivalence report."
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
            *_trace_dimension_evidence(trace_results, limit=2)
        ],
        "behavioral_consistency": list(equivalence_report.get("evidence", []))[:2],
        "requirement_traceability": [
            *_trace_dimension_evidence(trace_results, limit=2)
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
        "behavioral_consistency": (
            sorted(
                {
                    issue_type
                    for issue_type in behavior_issue_types
                    if issue_type in {"wrong_guard_or_trigger", "wrong_action_or_effect"}
                }
            )
            if allow_element_level_claims
            else []
        )
        or (["wrong_guard_or_trigger"] if (contradictions or dependency_breaks) and allow_element_level_claims else []),
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
    if component_review_mode and component_public_f1 is not None:
        component_note = (
            f" Component target `{component_target}` uses structured public TP/FP/FN evidence"
            f" with tp={component_public_tp}, fp={component_public_fp}, fn={component_public_fn},"
            f" yielding component_f1={component_public_f1:.4f}."
        )
        for key in ("semantic_completeness", "behavioral_consistency", "requirement_traceability", "evidence_discipline"):
            reason_map[key] += component_note

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
                    "matched_ratio": round(matched_ratio, 6),
                    "partial_ratio": round(partial_ratio, 6),
                    "missing_ratio": round(missing_ratio, 6),
                    "summary_row_type": summary_row_type,
                    "summary_target": summary_target,
                    "summary_target_axis": summary_target_axis,
                    "record_diagram_type": record_diagram_type,
                    "component_review_mode": component_review_mode,
                    "component_target": component_target,
                    "component_public_tp": component_public_tp,
                    "component_public_fp": component_public_fp,
                    "component_public_fn": component_public_fn,
                    "component_pred_total": component_pred_total,
                    "component_reference_total": component_reference_total,
                    "component_public_f1": round(component_public_f1, 6) if component_public_f1 is not None else None,
                    "component_source_kind": policy_packet.get("component_source_kind"),
                    "reference_alignment": round(reference_alignment, 6),
                    "structural_warning_count": len(pred_dossier.structural_warnings),
                    "extraction_conflict_count": len(pred_dossier.extraction_conflicts),
                    "parallel_structure_mismatch": bool(equivalence_report.get("parallel_structure_mismatch")),
                    "parallel_branch_credit": bool(equivalence_report.get("parallel_branch_credit")),
                    "trace_conflict_count": trace_conflict_count,
                    "dependency_break_count": len(dependency_breaks),
                    "equivalence_strength": round(equivalence_strength, 6),
                    "ref_element_coverage": round(ref_element_coverage, 6),
                    "ref_relation_coverage": round(ref_relation_coverage, 6),
                    "missing_signal_count": missing_signal_count,
                    "record_score_stretch": record_score_stretch,
                    "record_score_adjustment": round(record_score_adjustment, 6),
                    "record_diagram_offset": round(record_diagram_offset, 6),
                    "record_high_alignment_bonus": round(record_high_alignment_bonus, 6),
                    "summary_score_stretch": summary_score_stretch,
                    "summary_score_adjustment": round(summary_score_adjustment, 6),
                    "summary_public_signal": round(summary_public_signal, 6),
                    "summary_hidden_risk": round(summary_hidden_risk, 6),
                    "summary_semantic_adjustment": round(summary_semantic_adjustment, 6),
                    "summary_target_offset": round(summary_target_offset, 6),
                    "summary_row_bonus": round(summary_row_bonus, 6),
                    "summary_target_penalty": round(summary_target_penalty, 6),
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
        overall_score = clip01(summary_row_pivot + summary_score_stretch * (overall_score - summary_row_pivot))
        overall_score = clip01(overall_score + summary_score_adjustment)
    elif protocol_mode:
        protocol_hint = clip01(float(evidence_critic.get("protocol_assurance_score_hint", 0.34)))
        overall_score = clip01(0.25 * overall_score + 0.75 * protocol_hint)
    elif regime.regime == "record_level":
        # Stretch the compressed record-level score range, then apply only narrow
        # corrections to the dominant Phase 8 residual clusters.
        overall_score = clip01(0.50 + record_score_stretch * (overall_score - 0.50))
        overall_score = clip01(overall_score + record_score_adjustment)
    if component_review_mode and component_public_f1 is not None:
        overall_score = clip01(component_public_f1)
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
        # Record-level confidence is interpreted as tight score-alignment reliability
        # rather than generic reviewer self-belief, so it must remain much lower.
        base = 0.09 + 0.15 * base
    if policy_packet.get("component_review_mode"):
        base = max(base, 0.88)
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
