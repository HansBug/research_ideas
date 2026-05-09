"""Pipeline 各 stage 的 agent 调用包装层。

**作用**：把 :mod:`agents/` 下的 12 个 agent 业务函数包装成统一签名的
``run_*_node(...) -> tuple[结果, notes]`` 形式，供 :mod:`graph.runtime`
按 stage 顺序调用。

**设计思路**：

1. 每个 ``run_*_node`` 处理：
   - LLM 缺失时的 deterministic fallback；
   - LLM 调用产物为空时的 fallback（如 LLM 返回 ``None``）；
   - audit 笔记累积（``notes`` 列表）；
2. **不在本层做业务计算**——所有真实业务（评分、合并、 squeeze）都
   在 :mod:`agents/` 内；
3. **节点函数无状态**——所有状态由 :class:`schemas.graph_state.ReviewGraphState`
   持有，本层函数仅按签名读写。

**关键约束**：

* 12 个 ``run_*_node`` 函数顺序与 :mod:`graph.edges` 中的 stage 元组
  对齐；
* 节点函数返回的第二个元素（``notes``）会被 ``runtime.py`` 写入
  ``state.notes``，不应包含敏感数据。
"""

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
    """PREPARATION-1: 调用 contract router 推断评审契约。

    :param llm: LLM client（``None`` 走 deterministic）
    :param prompt: 评审 prompt 字符串
    :return: ``(ReviewContract, notes)`` 二元组
    """
    notes: list[str] = []
    return route_contract(prompt, llm, notes), notes


def run_input_analyst_node(request: Any) -> tuple[Any, list[str]]:
    """PREPARATION-2: 调用 input analyst 解析 NL 需求文本。

    本节点 deterministic-only（不接收 LLM 参数），始终从 prompt /
    input_text 抽取结构化 :class:`InputDossier`。

    :param request: :class:`ExpertReviewRequest`
    :return: ``(InputDossier, notes=空列表)``
    """
    return build_input_dossier(request), []


def run_prediction_extractor_node(
    llm: ChatOpenAI | None,
    pred_output: str | None,
) -> tuple[Any, list[str]]:
    """PREPARATION-3: 调用 prediction extractor 解析预测制品。

    :param llm: LLM client（``None`` 走 deterministic parser-only）
    :param pred_output: 预测制品文本（``None`` 时返回 stub dossier）
    :return: ``(ArtifactDossier with role='prediction', notes)``
    """
    notes: list[str] = []
    return extract_prediction_dossier(pred_output, llm, notes), notes


def run_reference_extractor_node(
    llm: ChatOpenAI | None,
    ref_output: str | None,
) -> tuple[Any, list[str]]:
    """PREPARATION-4: 调用 reference extractor 解析参考制品。

    :param llm: LLM client
    :param ref_output: 参考制品文本（``None`` 时返回 stub dossier，
        regime 后续会标 has_reference=False）
    :return: ``(ArtifactDossier with role='reference', notes)``
    """
    notes: list[str] = []
    return extract_reference_dossier(ref_output, llm, notes), notes


def run_evidence_regime_node(
    llm: ChatOpenAI | None,
    request: Any,
    pred_dossier: Any,
    ref_dossier: Any,
) -> tuple[Any, list[str]]:
    """PREPARATION-5: 调用 evidence regime estimator 推断 regime。

    :param llm: LLM client
    :param request: :class:`ExpertReviewRequest`
    :param pred_dossier: PREPARATION-3 产出的 :class:`ArtifactDossier`
    :param ref_dossier: PREPARATION-4 产出的 :class:`ArtifactDossier`
    :return: ``(EvidenceRegime, notes=空列表)``
    """
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
    """PREPARATION-6: 构造 policy_packet 与 :class:`DimensionDefinition` 列表。

    :param llm: LLM client
    :param contract: PREPARATION-1 产出的 :class:`ReviewContract`
    :param regime: PREPARATION-5 产出的 :class:`EvidenceRegime`
    :param request: :class:`ExpertReviewRequest`
    :param input_dossier: PREPARATION-2 产出的 :class:`InputDossier`
    :param pred_dossier: 预测制品 dossier
    :param ref_dossier: 参考制品 dossier
    :return: ``(policy_packet dict, dimensions list, notes)``
    """
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
    """ANALYSIS-1: 调用 traceability agent 计算需求-制品对应关系。

    流程：若有 LLM 则先尝试 LLM 路径；LLM 失败 / 返回空时回退
    deterministic 路径。两条路径输出 schema 一致。

    :param llm: LLM client
    :param input_dossier: :class:`InputDossier`
    :param pred_dossier: 预测制品 dossier
    :return: ``(list[RequirementTraceResult], notes)``
    """
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
    """ANALYSIS-2: 调用 equivalence agent 比较预测/参考制品的行为等价。

    流程：始终先跑 deterministic_equivalence；若有 LLM 则尝试用
    equivalence_with_llm 精化；精化失败保留 deterministic 版本。

    :param llm: LLM client
    :param input_dossier: :class:`InputDossier`
    :param pred_dossier: 预测制品 dossier
    :param ref_dossier: 参考制品 dossier
    :return: ``(equivalence_report dict, notes)``
    """
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
    """ANALYSIS-3: 调用 pragmatic quality agent 评制品的实用清晰度。

    :param llm: LLM client
    :param contract: :class:`ReviewContract`
    :param regime: :class:`EvidenceRegime`
    :param policy_packet: PREPARATION-6 产出的 dict
    :param input_dossier: :class:`InputDossier`
    :param pred_dossier: 预测制品 dossier
    :return: ``(quality_report dict, notes)``
    """
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
    """FINAL-1: 调用 missing-evidence critic 计算 confidence_cap / vv_roles。

    本节点产出的 ``evidence_critic`` dict 直接影响 score_composer 的
    ``evidence_discipline`` 维度评分与最终 confidence 计算。

    :param llm: LLM client
    :param contract: :class:`ReviewContract`
    :param regime: :class:`EvidenceRegime`
    :param request: :class:`ExpertReviewRequest`
    :param policy_packet: PREPARATION-6 产出
    :param input_dossier: :class:`InputDossier`
    :param pred_dossier: 预测制品 dossier
    :param ref_dossier: 参考制品 dossier（可空）
    :param equivalence_report: ANALYSIS-2 产出
    :param quality_report: ANALYSIS-3 产出
    :return: ``(evidence_critic dict, notes)``，含 confidence_cap /
        warnings / vv_roles / missing_evidence_flags /
        protocol_assurance_score_hint 等字段
    """
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
    *,
    llm: ChatOpenAI | None = None,
) -> tuple[list[Any], list[Any], float, float]:
    """FINAL-2: 调用 score composer 跑 6 次 LLM rubric + mode-specific shaping。

    本节点是整个 pipeline 中 LLM 调用最密集的位置（最多 6 次 rubric
    LLM call + 可能的额外 LLM 调用）。它承担：

    1. 6 个 dim 的 deterministic_estimate 计算；
    2. 调用 :func:`agents.rubric_scorer.llm_rubric_score` 跑 LLM rubric；
    3. 应用 mode-specific blend / penalty / rescue / stretch（详见
       :mod:`agents.score_composer`）；
    4. 计算 overall_score 与 confidence。

    :return: 4 元组 ``(dimension_results 列表, harmful_issues 列表,
        overall_score, confidence)``

    .. note::
        见 issue I-15 ：本节点的 mode-specific shaping 远比讨论稿
        描述的 "5+1 + 派生" 简单平均复杂——overall_score 经过多层
        线性 blend / penalty / bonus 调整后才返回。
    """
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
        llm=llm,
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
    """FINAL-3: 调用 final synthesizer 装配最终 :class:`ExpertReviewResult`。

    流程：
        1. ``overall_reason`` 拼装 deterministic NL feedback 草稿；
        2. ``maybe_refine_overall_reason`` 用 LLM 精化（可选）；
        3. ``synthesize_result`` 把所有字段打包为 :class:`ExpertReviewResult`。

    :return: ``(ExpertReviewResult, 空 notes 列表)``
    """
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
