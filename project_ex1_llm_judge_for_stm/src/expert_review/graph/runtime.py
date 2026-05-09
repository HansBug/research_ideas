"""LangGraph runtime —— pipeline 主调度器。

**作用**：把 12 个 agent 节点（含 1 个已删除的 arbiter）按
:func:`graph.subgraphs.ordered_stage_groups` 给出的 3-stage 顺序逐段
执行，把状态写入共享 :class:`schemas.graph_state.ReviewGraphState`，
最终返回 :class:`schema.ExpertReviewResult`。

**设计思路**：

1. **共享 state 容器**：所有 agent 通过 ``state.xxx`` 字段读写，避免
   长参数列表；
2. **stage 内部允许 fan-out 并行**：例如 PREPARATION 内 input /
   prediction / reference 三个 extractor 并行；ANALYSIS 内 trace +
   quality + (可选 equivalence) 并行；
3. **不暴露 LangGraph 库依赖**：本模块不直接使用 langgraph 的 graph
   构造，只做线性 + 局部并行调度。"langgraph" 出现在 backend_label
   是历史名遗留，与库无关。
4. **LLM 缺失降级**：``llm`` 参数可为 ``None``，此时所有 ``run_*_node``
   走 deterministic 路径——pipeline 仍能完整跑完并产出
   :class:`ExpertReviewResult`；
5. **strict-llm 不在本层**：本 runtime 不实现 strict 校验，是
   :func:`benchmark.run_benchmark_iteration` 的 ``strict_llm`` 参数
   职责（issue I-4）。

**关键约束**：

* :func:`run_expert_review_workflow` 是模块对外唯一入口；
* :func:`_default_equivalence_report` 在无 ref 时回填默认 equivalence，
  其 confidence 0.58 / 0.52 是 hardcode（设计 bias，未来可参数化）；
* :func:`_append_runtime_notes` 在 score_composer 后、final_synthesizer
  前写入 audit notes；顺序敏感不可调换。
"""

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
    """无参考制品时构造 fallback equivalence_report。

    当 :attr:`ReviewGraphState.regime` 标识 ``has_reference == False``
    时，equivalence agent 不会真正运行——本函数从 ``trace_results``
    估算一个 weak 版本的 equivalence_strength 填进去，让下游
    ``score_composer`` 仍有可用字段。

    :param state: 当前 :class:`ReviewGraphState` 实例
    :return: 与 :func:`agents.equivalence.deterministic_equivalence`
        返回 dict 同 schema 的 fallback 版本，但
        ``equivalence_strength`` 仅基于 trace_ratio
    :rtype: dict[str, Any]

    .. note::
        confidence 字段 hardcode 为 0.58（record_level）/ 0.52（其它），
        是 W2 时期经验值，尚未参数化。
    """
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
    """把 pipeline 关键过程信息追加到 ``state.notes`` (audit 用)。

    在 score_composer 后、final_synthesizer 前调用——把当时已有的所有
    stage label / context_packets / contract notes / policy profile /
    dossier mode / regime rationale / vv_roles / quality notes /
    missing_evidence flags / fan-out log 写入 ``state.notes``。

    本函数对 state 做 in-place 修改，无返回值。

    :param state: 当前 :class:`ReviewGraphState`，将在 ``state.notes``
        末尾追加多条 audit 字符串
    """
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
    """执行完整 3-stage 评审 pipeline，返回 :class:`ExpertReviewResult`。

    Pipeline 流程：

    1. **PREPARATION**: Contract Router → (并行) Input Analyst /
       Prediction Extractor / Reference Extractor → Evidence Regime
       Estimator → Review Policy Builder
    2. **ANALYSIS**: (并行) Traceability Agent / Pragmatic Quality Agent /
       (可选) Equivalence Agent
    3. **FINAL**: Missing-Evidence Critic → Score Composer →
       _append_runtime_notes → Final Synthesizer
    4. 末尾：从 :func:`llm_telemetry.summarize_current_llm_usage`
       拉 LLM usage summary 注入 result。

    :param request: 待评审的 :class:`ExpertReviewRequest`
    :param llm: 装配好的 LLM client（通常是
        :class:`fallback_llm.FallbackLLMClient`）；``None`` 时全管线
        走 deterministic 路径
    :param llm_model_name: 用于回填 result.llm_model_name 字段
    :param llm_provider: 用于回填 result.llm_provider 字段
    :param backend_label: backend 标识（默认
        ``"langgraph_multi_agent_v1"``，由 :class:`agent.ExpertReviewAgent`
        在调用前会加 ``_llm`` / ``_deterministic`` 后缀）
    :return: 完整填充后的 :class:`ExpertReviewResult`
    :rtype: ExpertReviewResult

    后处理 backend label 规则：

    * 若 ``llm is not None`` 但实际 LLM usage summary 显示
      ``effective_llm_used == False``（所有 stage 都走了 deterministic
      fallback），label 后缀改为 ``"_fallback_only"`` 标记此次本质为
      deterministic-only run，方便 strict_llm 路径过滤。
    """
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
            llm=llm,
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
