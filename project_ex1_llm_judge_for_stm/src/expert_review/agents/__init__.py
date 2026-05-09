"""``agents`` 子包入口 —— 12 个 agent 的统一 re-export。

**作用**：把每个 agent 的对外 API（``deterministic_*`` /
``*_with_llm`` / 装配函数等）re-export 到 ``expert_review.agents``
名空间，方便 :mod:`graph.runtime` / :mod:`graph.nodes` 一处导入。

**设计思路**：

* 所有 agent 都符合 "deterministic / LLM 双路径" 模式：每个 agent
  都先有 ``deterministic_*`` 函数作纯规则路径；对应有
  ``*_with_llm`` 函数作 LLM-精化路径，LLM 失败 / 返回空时由调用方
  fallback 到 deterministic 版本（在 :mod:`graph.nodes` 实现）；
* :mod:`agents.orchestrator` 提供 stage 标识常量（PREPARATION_FANOUT
  / ANALYSIS_FANOUT / FINAL_FANIN）+ ``record_agent_context`` /
  ``record_fanout`` / ``run_parallel`` helper；
* 12 个 agent 的目录结构与 :mod:`graph.edges` 中 stage 元组的成员
  名直接对应。

参考：

* 主讨论 §3.4 6-dim form-filling pipeline
* :mod:`graph.runtime` 主调度 + :mod:`graph.nodes` 节点封装
"""

from .contract_router import default_contract, route_contract
from .evidence_regime_estimator import estimate_evidence_regime
from .final_synthesizer import maybe_refine_overall_reason, overall_reason, synthesize_result
from .input_analyst import build_input_dossier
from .orchestrator import ANALYSIS_FANOUT, FINAL_FANIN, PREPARATION_FANOUT, record_agent_context, record_fanout, run_parallel
from .prediction_extractor import extract_prediction_dossier
from .reference_extractor import extract_reference_dossier
from .review_policy_builder import build_dimensions, build_review_policy_packet
from .score_composer import compose_scores, final_confidence
from .equivalence import deterministic_equivalence, equivalence_with_llm
from .missing_evidence_critic import deterministic_missing_evidence_critic, missing_evidence_with_llm
from .pragmatic_quality import deterministic_pragmatic_quality, pragmatic_quality_with_llm
from .traceability import deterministic_traceability, traceability_with_llm

__all__ = [
    "ANALYSIS_FANOUT",
    "FINAL_FANIN",
    "PREPARATION_FANOUT",
    "build_dimensions",
    "build_input_dossier",
    "build_review_policy_packet",
    "compose_scores",
    "default_contract",
    "deterministic_equivalence",
    "deterministic_missing_evidence_critic",
    "deterministic_pragmatic_quality",
    "deterministic_traceability",
    "estimate_evidence_regime",
    "equivalence_with_llm",
    "extract_prediction_dossier",
    "extract_reference_dossier",
    "final_confidence",
    "maybe_refine_overall_reason",
    "missing_evidence_with_llm",
    "overall_reason",
    "pragmatic_quality_with_llm",
    "record_agent_context",
    "record_fanout",
    "route_contract",
    "run_parallel",
    "synthesize_result",
    "traceability_with_llm",
]
