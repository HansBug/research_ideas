"""LangGraph runtime 用的可变共享状态容器。

**作用**：把 pipeline 各 stage 的输入、中间产物、最终结果统一收纳到
一个 :class:`ReviewGraphState` dataclass，供 ``graph/runtime.py`` 与
所有 agent 节点共享读写。

**设计思路**：

* **单一真理源**：每个 stage 完成后把自己的输出写到 ``state`` 的
  对应字段（如 ``state.input_dossier`` / ``state.regime``），下游
  stage 直接读，无需再传参；
* **可变 + slots**：使用 ``@dataclass(slots=True)`` 兼顾性能；状态
  对象在整个 pipeline 中**共享**（不拷贝），所以所有写操作都是
  in-place；
* **agent 无 state**：agent 函数本身不持有状态——所有状态写入
  ``ReviewGraphState`` 实例。这种设计让 pipeline 容易做 stage
  re-run / partial replay；
* **context_packets / fanout_log**：用于跨 agent 的上下文传播与
  fan-out / fan-in 结构追踪（见 ``agents/orchestrator.py``）。

**关键约束**：

* ``request`` 是构造时必传的入参；其余字段都给 default，让 stage
  可以增量填充；
* ``llm`` / ``llm_model_name`` / ``llm_provider`` / ``backend_label``
  在 :func:`graph.runtime.run_expert_review_workflow` 入口被设置，
  agent 内部不应改写。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .dossiers import ArtifactDossier, EvidenceRegime, InputDossier, ReviewContract
from .request import ExpertReviewRequest
from .result import ExpertReviewResult


@dataclass(slots=True)
class ReviewGraphState:
    """LangGraph runtime 的共享状态。

    所有 pipeline stage 都向同一个 :class:`ReviewGraphState` 实例
    写入自己的 stage 输出。

    :ivar request: 评审请求（构造时必传）
    :ivar llm: ``FallbackLLMClient`` 实例 (或 ``None`` 走 deterministic)
    :ivar llm_model_name: 实际使用的 model 名
    :ivar llm_provider: 实际命中的 primary provider key
    :ivar backend_label: 标识本次走的 backend 形态
        (``"langgraph_multi_agent_v1_llm"`` /
        ``"..._deterministic"``)
    :ivar notes: pipeline 各 stage 累计的过程笔记
    :ivar contract: 由 contract_router 写入
    :ivar regime: 由 evidence_regime_estimator 写入
    :ivar input_dossier: 由 input_analyst 写入
    :ivar pred_dossier: 由 prediction_extractor 写入
    :ivar ref_dossier: 由 reference_extractor 写入（无 ref 时为 None）
    :ivar policy_packet: 由 review_policy_builder 写入
    :ivar dimensions: 由 review_policy_builder 下发的
        :class:`schema.DimensionDefinition` 列表
    :ivar trace_results: 由 traceability agent 写入
    :ivar equivalence_report: 由 equivalence agent 写入（无 ref 时
        由 :func:`graph.runtime._default_equivalence_report` 填默认）
    :ivar quality_report: 由 pragmatic_quality agent 写入
    :ivar evidence_critic: 由 missing_evidence_critic 写入
    :ivar dimension_results: 由 score_composer 写入（6 个
        :class:`schema.DimensionReviewResult`）
    :ivar harmful_issues: 由 score_composer 写入
    :ivar overall_score: 由 score_composer 写入（已经过 mode shaping）
    :ivar confidence: 由 score_composer 写入
    :ivar result: 由 final_synthesizer 写入的最终
        :class:`schema.ExpertReviewResult`
    :ivar context_packets: 跨 agent 上下文 dict-of-dict，便于 audit
    :ivar fanout_log: fan-out / fan-in 操作的字符串日志
    """

    request: ExpertReviewRequest
    llm: Any | None = None
    llm_model_name: str | None = None
    llm_provider: str | None = None
    backend_label: str = "langgraph_multi_agent_v1"
    notes: list[str] = field(default_factory=list)
    contract: ReviewContract | None = None
    regime: EvidenceRegime | None = None
    input_dossier: InputDossier | None = None
    pred_dossier: ArtifactDossier | None = None
    ref_dossier: ArtifactDossier | None = None
    policy_packet: dict[str, Any] = field(default_factory=dict)
    dimensions: list[Any] = field(default_factory=list)
    trace_results: list[Any] = field(default_factory=list)
    equivalence_report: dict[str, Any] = field(default_factory=dict)
    quality_report: dict[str, Any] = field(default_factory=dict)
    evidence_critic: dict[str, Any] = field(default_factory=dict)
    dimension_results: list[Any] = field(default_factory=list)
    harmful_issues: list[Any] = field(default_factory=list)
    overall_score: float = 0.0
    confidence: float = 0.0
    result: ExpertReviewResult | None = None
    context_packets: dict[str, dict[str, Any]] = field(default_factory=dict)
    fanout_log: list[str] = field(default_factory=list)


__all__ = ["ReviewGraphState"]
