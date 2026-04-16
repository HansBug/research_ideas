from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..agents import (
    arbitrate_trace_and_equivalence,
    arbitrate_with_llm,
    deterministic_equivalence,
    deterministic_traceability,
    equivalence_with_llm,
    traceability_with_llm,
)


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


def run_arbitration_node(
    llm: ChatOpenAI | None,
    input_dossier: Any,
    pred_dossier: Any,
    ref_dossier: Any,
    trace_results: list[Any],
    equivalence_report: dict[str, Any],
) -> tuple[list[Any], dict[str, Any], list[str]]:
    trace_results, equivalence_report, notes = arbitrate_trace_and_equivalence(
        input_dossier,
        pred_dossier,
        ref_dossier,
        trace_results,
        equivalence_report,
    )
    if llm is None:
        return trace_results, equivalence_report, notes
    llm_result = arbitrate_with_llm(
        llm,
        input_dossier,
        pred_dossier,
        ref_dossier,
        trace_results,
        equivalence_report,
    )
    if llm_result is None:
        return trace_results, equivalence_report, notes
    llm_trace, llm_report, llm_notes = llm_result
    notes.extend(llm_notes[:4])
    if llm_notes:
        notes.append("Arbiter used deterministic reconciliation plus LLM conflict review.")
    return llm_trace, llm_report, notes
