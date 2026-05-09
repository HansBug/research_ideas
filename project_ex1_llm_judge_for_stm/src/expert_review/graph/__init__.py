"""``graph`` 子包入口 —— LangGraph 风格 pipeline 编排层。

**作用**：把分散在 ``agents/`` 中的 12 个 agent 组装成一个 3-stage 顺序
执行的评审 pipeline：

1. PREPARATION_STAGE (6 agents 部分并行)：从 prompt + input + pred + ref
   产出 contract / dossier / regime / policy_packet 等中间产物；
2. ANALYSIS_STAGE (3 agents 部分并行)：基于 dossier 计算 trace /
   equivalence / pragmatic_quality 三个核心 report；
3. FINAL_STAGE (3 agents 顺序，原 4 个含 Disagreement Arbiter 已删除)：
   missing-evidence critic → score_composer → final_synthesizer，
   产出最终 :class:`schema.ExpertReviewResult`。

**设计思路**：

* :mod:`graph.edges` 持有 stage 名字常量，是 pipeline 顺序的 *单一真理源*；
* :mod:`graph.nodes` 提供 12 个 ``run_*_node`` 函数，每个是单 agent 的
  调用包装（处理 LLM 缺失时的 deterministic fallback）；
* :mod:`graph.runtime` 持有 :func:`run_expert_review_workflow` 主入口，
  按 :func:`graph.subgraphs.ordered_stage_groups` 顺序调度全部 node。

参考：

* 主讨论 §3.4 / §I-18（4 阶段抽象 vs 代码 3 阶段实际结构 issue）
"""

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
from .runtime import run_expert_review_workflow

__all__ = [
    "run_contract_router_node",
    "run_equivalence_node",
    "run_evidence_regime_node",
    "run_expert_review_workflow",
    "run_final_synthesizer_node",
    "run_input_analyst_node",
    "run_missing_evidence_node",
    "run_prediction_extractor_node",
    "run_quality_node",
    "run_reference_extractor_node",
    "run_review_policy_builder_node",
    "run_score_composer_node",
    "run_traceability_node",
]
