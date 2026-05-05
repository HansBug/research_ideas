from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..agents import (
    build_dimensions,
    build_input_dossier,
    build_review_policy_packet,
    compose_scores,
    estimate_evidence_regime,
    extract_prediction_dossier,
    extract_reference_dossier,
    final_confidence,
    maybe_refine_overall_reason,
    overall_reason,
    route_contract,
    synthesize_result,
    deterministic_missing_evidence_critic,
    deterministic_pragmatic_quality,
    deterministic_equivalence,
    deterministic_traceability,
    equivalence_with_llm,
    missing_evidence_with_llm,
    pragmatic_quality_with_llm,
    traceability_with_llm,
)


def run_contract_router_node(
    llm: ChatOpenAI | None,
    prompt: str,
) -> tuple[Any, list[str]]:
    notes: list[str] = []
    return route_contract(prompt, llm, notes), notes


def run_input_analyst_node(request: Any) -> tuple[Any, list[str]]:
    return build_input_dossier(request), []


def run_prediction_extractor_node(
    llm: ChatOpenAI | None,
    pred_output: str | None,
) -> tuple[Any, list[str]]:
    notes: list[str] = []
    return extract_prediction_dossier(pred_output, llm, notes), notes


def run_reference_extractor_node(
    llm: ChatOpenAI | None,
    ref_output: str | None,
) -> tuple[Any, list[str]]:
    notes: list[str] = []
    return extract_reference_dossier(ref_output, llm, notes), notes


def run_evidence_regime_node(
    llm: ChatOpenAI | None,
    request: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> tuple[Any, list[str]]:
    return estimate_evidence_regime(request, pred_dossier, ref_dossier, llm=llm), []


def run_review_policy_builder_node(
    llm: ChatOpenAI | None,
    contract: Any,
    regime: Any,
    request: Any,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> tuple[dict[str, Any], list[Any], list[str]]:
    notes: list[str] = []
    policy_packet = build_review_policy_packet(
        llm,
        contract,
        regime,
        request,
        input_dossier,
        pred_dossier,
        ref_dossier,
        notes,
    )
    return policy_packet, build_dimensions(contract, regime), notes


def run_traceability_node(
    llm: ChatOpenAI | None,
    input_dossier: Any,
    pred_dossier: Any,
) -> tuple[list[Any], list[str]]:
    notes: list[str] = []
    trace_results = traceability_with_llm(llm, input_dossier, pred_dossier) if llm is not None else None
    if trace_results:
        notes.append("Traceability agent used candidate-guided LLM reasoning.")
        return trace_results, notes
    if llm is not None:
        notes.append("Traceability agent fell back to deterministic candidate scoring.")
    return deterministic_traceability(input_dossier, pred_dossier), notes


def run_equivalence_node(
    llm: ChatOpenAI | None,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    report = deterministic_equivalence(input_dossier, pred_dossier, ref_dossier)
    if llm is None:
        return report, notes
    llm_report = equivalence_with_llm(llm, input_dossier, pred_dossier, ref_dossier, report)
    if llm_report is not None:
        notes.append("Equivalence agent used deterministic candidates plus LLM refinement.")
        return llm_report, notes
    notes.append("Equivalence agent fell back to deterministic comparison.")
    return report, notes


def run_quality_node(
    llm: ChatOpenAI | None,
    contract: Any,
    regime: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    report = deterministic_pragmatic_quality(contract, regime, policy_packet, input_dossier, pred_dossier)
    if llm is None:
        return report, notes
    llm_report = pragmatic_quality_with_llm(llm, contract, regime, policy_packet, input_dossier, pred_dossier, report)
    if llm_report is not None:
        notes.append("Pragmatic-quality agent used deterministic cues plus LLM refinement.")
        return llm_report, notes
    notes.append("Pragmatic-quality agent fell back to deterministic quality inspection.")
    return report, notes


def run_missing_evidence_node(
    llm: ChatOpenAI | None,
    contract: Any,
    regime: Any,
    request: Any,
    policy_packet: dict[str, Any],
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    notes: list[str] = []
    report = deterministic_missing_evidence_critic(
        contract,
        regime,
        request,
        policy_packet,
        input_dossier,
        pred_dossier,
        ref_dossier,
        equivalence_report,
        quality_report,
    )
    if llm is None:
        return report, notes
    llm_report = missing_evidence_with_llm(
        llm,
        contract,
        regime,
        request,
        policy_packet,
        input_dossier,
        pred_dossier,
        ref_dossier,
        equivalence_report,
        quality_report,
        report,
    )
    if llm_report is not None:
        notes.append("Missing-evidence critic used deterministic restraint rules plus LLM refinement.")
        return llm_report, notes
    notes.append("Missing-evidence critic fell back to deterministic evidence-discipline rules.")
    return report, notes


def run_score_composer_node(
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
) -> tuple[list[Any], list[Any], float, float]:
    dimension_results, harmful_issues, overall_score = compose_scores(
        dimensions,
        request,
        contract,
        regime,
        policy_packet,
        pred_dossier,
        ref_dossier,
        trace_results,
        equivalence_report,
        quality_report,
        evidence_critic,
    )
    confidence = final_confidence(regime, policy_packet, trace_results, equivalence_report, evidence_critic)
    return dimension_results, harmful_issues, overall_score, confidence


def run_final_synthesizer_node(
    llm: ChatOpenAI | None,
    *,
    request: Any,
    backend_label: str,
    regime: Any,
    policy_packet: dict[str, Any],
    overall_score: float,
    trace_results: list[Any],
    equivalence_report: dict[str, Any],
    quality_report: dict[str, Any],
    harmful_issues: list[Any],
    evidence_critic: dict[str, Any],
    dimension_results: list[Any],
    notes: list[str],
    confidence: float,
) -> tuple[Any, list[str]]:
    draft_reason = overall_reason(
        regime,
        policy_packet,
        overall_score,
        dimension_results,
        trace_results,
        equivalence_report,
        quality_report,
        harmful_issues,
        evidence_critic,
    )
    final_reason = maybe_refine_overall_reason(llm, regime, policy_packet, draft_reason, notes, dimension_results)
    return (
        synthesize_result(
            request=request,
            backend_label=backend_label,
            overall_score=overall_score,
            overall_reason_text=final_reason,
            dimension_results=dimension_results,
            trace_results=trace_results,
            harmful_issues=harmful_issues,
            notes=notes,
            confidence=confidence,
        ),
        [],
    )
