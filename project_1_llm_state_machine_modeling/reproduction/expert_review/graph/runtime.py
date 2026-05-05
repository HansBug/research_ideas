from __future__ import annotations

from typing import Any

from langchain_openai import ChatOpenAI

from ..agents import record_agent_context, record_fanout, run_parallel
from ..llm_telemetry import llm_run_context, summarize_current_llm_usage
from ..schemas.graph_state import ReviewGraphState
from ..schemas.request import ExpertReviewRequest
from ..schemas.result import ExpertReviewResult
from .nodes import (
    run_contract_router_node,
    run_equivalence_node,
    run_evidence_regime_node,
    run_final_synthesizer_node,
    run_input_analyst_node,
    run_missing_evidence_node,
    run_prediction_extractor_node,
    run_quality_node,
    run_reference_extractor_node,
    run_review_policy_builder_node,
    run_score_composer_node,
    run_traceability_node,
)
from .subgraphs import ordered_stage_groups


def _default_equivalence_report(state: ReviewGraphState) -> dict[str, Any]:
    trace_matched = sum(1 for item in state.trace_results if item.status == "matched")
    trace_partial = sum(1 for item in state.trace_results if item.status == "partial")
    trace_ratio = (trace_matched + 0.5 * trace_partial) / max(1, len(state.trace_results))
    return {
        "equivalence_strength": trace_ratio,
        "supported_restructures": [],
        "harmful_extras": [],
        "missing_items": [],
        "contradictions": [],
        "dependency_breaks": [],
        "parallel_structure_mismatch": False,
        "parallel_branch_credit": False,
        "major_relation_divergence_count": 0,
        "trace_conflict_count": 0,
        "evidence": state.pred_dossier.evidence[:2] if state.pred_dossier else [],
        "confidence": 0.58 if state.regime and state.regime.regime == "record_level" else 0.52,
    }


def _append_runtime_notes(state: ReviewGraphState) -> None:
    state.notes.append(
        "Graph stages: "
        + " | ".join(f"{name}=" + ",".join(stage) for name, stage in ordered_stage_groups())
    )
    state.notes.append(
        "Agent context trimming: "
        + "; ".join(
            f"{name}=>{','.join(packet['context_keys'])}"
            for name, packet in state.context_packets.items()
        )
    )
    if state.contract is not None:
        state.notes.extend(state.contract.notes)
        state.notes.append(f"Contract strictness: {state.contract.strictness}.")
    if state.policy_packet:
        state.notes.append(f"Policy profile: {state.policy_packet.get('profile_name')}.")
    if state.pred_dossier is not None and state.ref_dossier is not None:
        state.notes.append(
            f"Prediction dossier mode: {state.pred_dossier.analysis_mode}; reference dossier mode: {state.ref_dossier.analysis_mode}."
        )
        state.notes.append(
            "Prediction dossier probe: "
            f"{state.pred_dossier.format_guess} (confidence={state.pred_dossier.format_confidence:.2f}, observability={state.pred_dossier.observability})."
        )
    if state.regime is not None:
        state.notes.append(f"Evidence regime rationale: {state.regime.rationale}")
        state.notes.extend(state.regime.caution_rules[:2])
    if state.evidence_critic.get("vv_roles"):
        state.notes.append("Recognized V&V roles from evidence: " + ", ".join(state.evidence_critic["vv_roles"][:4]) + ".")
    state.notes.extend(state.quality_report.get("notes", [])[:2])
    if state.evidence_critic.get("missing_evidence_flags"):
        state.notes.append("Missing-evidence flags: " + ", ".join(state.evidence_critic["missing_evidence_flags"][:4]) + ".")
    state.notes.extend(state.evidence_critic.get("warnings", [])[:2])
    if state.fanout_log:
        state.notes.append("Fan-out/fan-in: " + " | ".join(state.fanout_log))


def run_expert_review_workflow(
    request: ExpertReviewRequest,
    *,
    llm: ChatOpenAI | None = None,
    llm_model_name: str | None = None,
    llm_provider: str | None = None,
    backend_label: str = "langgraph_multi_agent_v1",
) -> ExpertReviewResult:
    with llm_run_context(
        llm_configured=llm is not None,
        configured_model_name=llm_model_name,
        configured_provider=llm_provider,
    ):
        state = ReviewGraphState(
            request=request,
            llm=llm,
            llm_model_name=llm_model_name,
            llm_provider=llm_provider,
            backend_label=backend_label,
        )

        record_agent_context(state, "Contract Router", context_keys=["prompt"], summary="Prompt-only contract parsing.")
        state.contract, contract_notes = run_contract_router_node(llm, request.prompt)
        state.notes.extend(contract_notes)

        record_fanout(state, "preparation_fanout", ("Input Analyst", "Prediction Extractor", "Reference Extractor"))
        record_agent_context(state, "Input Analyst", context_keys=["input_text", "prompt"], summary="Requirement and grounding extraction.")
        record_agent_context(state, "Prediction Extractor", context_keys=["pred_output"], summary="Prediction-only artifact lifting.")
        record_agent_context(state, "Reference Extractor", context_keys=["ref_output"], summary="Reference-only artifact lifting.")
        preparation = run_parallel(
            {
                "input": lambda: run_input_analyst_node(request),
                "prediction": lambda: run_prediction_extractor_node(llm, request.pred_output),
                "reference": lambda: run_reference_extractor_node(llm, request.ref_output),
            }
        )
        state.input_dossier, input_notes = preparation["input"]
        state.pred_dossier, pred_notes = preparation["prediction"]
        state.ref_dossier, ref_notes = preparation["reference"]
        state.notes.extend(input_notes + pred_notes + ref_notes)

        record_agent_context(
            state,
            "Evidence Regime Estimator",
            context_keys=["prompt", "input_dossier", "pred_dossier", "ref_dossier"],
            summary="Evidence regime inference without task-type assumptions.",
        )
        state.regime, regime_notes = run_evidence_regime_node(llm, request, state.pred_dossier, state.ref_dossier)
        state.notes.extend(regime_notes)

        record_agent_context(
            state,
            "Review Policy Builder",
            context_keys=["contract", "regime", "input_dossier", "pred_dossier", "ref_dossier"],
            summary="Policy packet and rubric weight assembly.",
        )
        state.policy_packet, state.dimensions, policy_notes = run_review_policy_builder_node(
            llm,
            state.contract,
            state.regime,
            request,
            state.input_dossier,
            state.pred_dossier,
            state.ref_dossier,
        )
        state.notes.extend(policy_notes)

        record_fanout(
            state,
            "analysis_fanout",
            ("Traceability Agent", "Equivalence and Difference Agent", "Pragmatic Quality Agent"),
        )
        record_agent_context(
            state,
            "Traceability Agent",
            context_keys=["input_dossier", "pred_dossier"],
            summary="Requirement-to-prediction linking only.",
        )
        record_agent_context(
            state,
            "Equivalence and Difference Agent",
            context_keys=["input_dossier", "pred_dossier", "ref_dossier"],
            summary="Prediction/reference semantic comparison only.",
        )
        record_agent_context(
            state,
            "Pragmatic Quality Agent",
            context_keys=["contract", "regime", "policy_packet", "input_dossier", "pred_dossier"],
            summary="Pragmatic quality and proportionality inspection.",
        )

        analysis_tasks: dict[str, Any] = {
            "trace": lambda: run_traceability_node(llm, state.input_dossier, state.pred_dossier),
            "quality": lambda: run_quality_node(
                llm,
                state.contract,
                state.regime,
                state.policy_packet,
                state.input_dossier,
                state.pred_dossier,
            ),
        }
        if state.regime.has_reference:
            analysis_tasks["equivalence"] = lambda: run_equivalence_node(
                llm,
                state.input_dossier,
                state.pred_dossier,
                state.ref_dossier,
            )
        analysis_results = run_parallel(analysis_tasks)
        state.trace_results, trace_notes = analysis_results["trace"]
        state.quality_report, quality_notes = analysis_results["quality"]
        state.notes.extend(trace_notes + quality_notes)
        if "equivalence" in analysis_results:
            state.equivalence_report, equivalence_notes = analysis_results["equivalence"]
            state.notes.extend(equivalence_notes)
        else:
            state.equivalence_report = _default_equivalence_report(state)

        record_agent_context(
            state,
            "Missing-Evidence Critic",
            context_keys=[
                "contract",
                "regime",
                "policy_packet",
                "input_dossier",
                "pred_dossier",
                "ref_dossier",
                "equivalence_report",
                "quality_report",
            ],
            summary="Evidence discipline and confidence capping.",
        )
        state.evidence_critic, evidence_notes = run_missing_evidence_node(
            llm,
            state.contract,
            state.regime,
            request,
            state.policy_packet,
            state.input_dossier,
            state.pred_dossier,
            state.ref_dossier,
            state.equivalence_report,
            state.quality_report,
        )
        state.notes.extend(evidence_notes)

        # Tier 2 ablation 验证（E1）：跳过 arbiter 整段 ΔHAI = +0.1556（反向贡献），
        # 已删除 arbitrate_trace_and_equivalence 调用与 arbiter 模块。trace_conflict_count
        # 仍由 deterministic_equivalence 在 equivalence_report 中维护。

        record_fanout(state, "final_fanin", ("Missing-Evidence Critic", "Score Composer", "Final Synthesizer"))
        record_agent_context(
            state,
            "Score Composer",
            context_keys=[
                "dimensions",
                "contract",
                "regime",
                "policy_packet",
                "pred_dossier",
                "ref_dossier",
                "trace_results",
                "equivalence_report",
                "quality_report",
                "evidence_critic",
            ],
            summary="Dimension scoring and confidence composition.",
        )
        state.dimension_results, state.harmful_issues, state.overall_score, state.confidence = run_score_composer_node(
            state.dimensions,
            request,
            state.contract,
            state.regime,
            state.policy_packet,
            state.pred_dossier,
            state.ref_dossier,
            state.trace_results,
            state.equivalence_report,
            state.quality_report,
            state.evidence_critic,
        )

        _append_runtime_notes(state)
        record_agent_context(
            state,
            "Final Synthesizer",
            context_keys=[
                "request",
                "regime",
                "policy_packet",
                "dimension_results",
                "trace_results",
                "equivalence_report",
                "quality_report",
                "evidence_critic",
                "notes",
            ],
            summary="Final result assembly with no new findings.",
        )
        state.result, synth_notes = run_final_synthesizer_node(
            llm,
            request=request,
            backend_label=backend_label,
            regime=state.regime,
            policy_packet=state.policy_packet,
            overall_score=state.overall_score,
            trace_results=state.trace_results,
            equivalence_report=state.equivalence_report,
            quality_report=state.quality_report,
            harmful_issues=state.harmful_issues,
            evidence_critic=state.evidence_critic,
            dimension_results=state.dimension_results,
            notes=state.notes,
            confidence=state.confidence,
        )
        state.notes.extend(synth_notes)

        llm_usage_summary = summarize_current_llm_usage(record_count=1)
        state.result.llm_model_name = llm_model_name
        state.result.llm_provider = llm_provider
        state.result.llm_usage_summary = llm_usage_summary
        if llm is not None and not llm_usage_summary.effective_llm_used:
            state.result.used_review_backend = f"{backend_label}_fallback_only"
            state.result.notes.append(
                "LLM was configured, but no workflow stage produced a usable LLM output; this run is effectively deterministic."
            )
        elif llm is not None and llm_usage_summary.operation_failure_count > 0:
            state.result.notes.append(
                "LLM path was partially effective, but some stages fell back after unusable LLM responses."
            )
        return state.result
