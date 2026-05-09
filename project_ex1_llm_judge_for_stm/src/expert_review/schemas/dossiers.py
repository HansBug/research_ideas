"""Pipeline 中间产物 dossier dataclass 集合。

**作用**：定义 pipeline 各 agent 之间传递的 5 类中间状态容器：

1. :class:`ReviewContract`：从 prompt 里推断出的 "评审契约"——
   告诉下游 agent "这次评审的重点 / strict 级别 / 等价规则" 等；
2. :class:`EvidenceRegime`：证据 regime 估计——artifact 的可观测度
   是 element-level / summary-level / protocol-only / mixed_evidence
   中的哪一种，会显著影响后续维度的 sanity bound 与 confidence cap；
3. :class:`ArtifactElement`：制品中的单个元素（state / event / 等）
   的 dossier 条目；
4. :class:`ArtifactRelation`：制品中的单个关系（transition）的
   dossier 条目；
5. :class:`ArtifactDossier`：把整个制品（pred / ref）的 elements +
   relations + 衍生分析（observability / surface markers /
   structural warnings 等）打包成单个 dossier；
6. :class:`InputDossier`：把 NL 需求文本解析后的结构化形式
   （requirements / behaviors / constraints / ambiguities）。

**设计思路**：

* **冗余字段优先**：dossier 设计时倾向把上游能算出的元数据全部
  保留（如 :attr:`ArtifactDossier.format_confidence` /
  :attr:`ArtifactDossier.observability_reason`），让下游 agent 不用
  反复再解析；
* **慢字段惰性**：除 ``elements`` / ``relations`` 等核心字段外，所有
  辅助字段都给空列表 / 空字符串默认值，缺失时不抛错；
* **不放业务方法**：dataclass 只装数据，不放计算方法（计算逻辑
  归 ``tools/`` 与 ``agents/``）。

**关键约束**：

* :attr:`ArtifactDossier.role` ∈ ``{"prediction", "reference"}``，
  在 ``score_composer`` 等位置用于路由；
* :attr:`EvidenceRegime.regime` 的取值会驱动 ``review_policy_builder``
  下发不同的 dimension weight 与 sanity bound（详见
  ``agents/score_composer.py``）。
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..schema import EvidenceItem, RequirementTraceResult


@dataclass(slots=True)
class ReviewContract:
    """从 prompt 推断出的评审契约 (上游 contract_router agent 输出)。

    :ivar task_summary: 一句话总结此次评审的目标
    :ivar requested_focus: 用户显式要求关注的方面列表
        （如 ``["coverage", "naming"]``）
    :ivar domain_knowledge: 领域知识提示（用于让 LLM 判分时考虑领域
        惯例）
    :ivar equivalence_rules: 用户级 equivalence 规则
        （如 "允许结构差异但行为一致")
    :ivar evidence_rules: evidence-discipline 相关的额外约束
    :ivar strictness: ``"strict"`` / ``"balanced"`` / ``"lenient"``，
        默认 ``"balanced"``
    :ivar notes: contract_router 自动产生的 routing 笔记
    """

    task_summary: str
    requested_focus: list[str] = field(default_factory=list)
    domain_knowledge: list[str] = field(default_factory=list)
    equivalence_rules: list[str] = field(default_factory=list)
    evidence_rules: list[str] = field(default_factory=list)
    strictness: str = "balanced"
    notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceRegime:
    """Pipeline 估计出的 evidence regime (上游 evidence_regime_estimator 输出)。

    Regime 决定了下游能给出什么粒度的评审：element-level / summary-only /
    protocol-only / mixed_evidence 等。例如 protocol-only regime 下不允
    许做 element-level 的 issue claim。

    :ivar regime: regime 标识符
    :ivar rationale: 估计该 regime 的理由（NL）
    :ivar pred_observability: 预测制品的可观测度
        ``"low" / "summary" / "element"``
    :ivar ref_observability: 参考制品的可观测度
    :ivar has_reference: 是否存在参考制品
    :ivar has_prediction: 是否存在预测制品
    :ivar caution_rules: 该 regime 下额外的注意事项
    """

    regime: str
    rationale: str
    pred_observability: str
    ref_observability: str
    has_reference: bool
    has_prediction: bool
    caution_rules: list[str] = field(default_factory=list)


@dataclass(slots=True)
class ArtifactElement:
    """制品中的单个元素 (state / event / variable / 等) dossier 条目。

    :ivar element_id: 元素唯一 id
    :ivar kind: 元素类型（``"state"`` / ``"event"`` / ``"variable"`` 等）
    :ivar label: 元素标签（短名）
    :ivar text: 元素完整文本
    :ivar evidence_text: 在原文中能定位元素的片段
    """

    element_id: str
    kind: str
    label: str
    text: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactRelation:
    """制品中的单个关系 (transition) dossier 条目。

    :ivar relation_id: 关系唯一 id
    :ivar kind: 关系类型（``"transition"`` / ``"contains"`` 等）
    :ivar source_label: 源端标签
    :ivar target_label: 目标端标签
    :ivar trigger: 触发事件
    :ivar condition: 守卫条件
    :ivar action: 动作
    :ivar description: NL 描述
    :ivar evidence_text: 在原文中能定位关系的片段
    """

    relation_id: str
    kind: str
    source_label: str
    target_label: str
    trigger: str
    condition: str
    action: str
    description: str
    evidence_text: str


@dataclass(slots=True)
class ArtifactDossier:
    """整个制品（pred / ref）的解析后 dossier。

    由 ``prediction_extractor`` / ``reference_extractor`` agent 输出，
    供下游 traceability / equivalence / pragmatic_quality / score_composer
    多个 agent 复用。

    :ivar role: ``"prediction"`` / ``"reference"``
    :ivar format_guess: 格式猜测（如 ``"plantuml"`` / ``"sysml_xml"``）
    :ivar artifact_family_guess: 制品家族猜测
    :ivar summary: 制品 NL 摘要
    :ivar elements: :class:`ArtifactElement` 列表
    :ivar relations: :class:`ArtifactRelation` 列表
    :ivar behaviors: 推断出的行为描述列表
    :ivar constraints: 推断出的约束列表
    :ivar ambiguities: 解析时的模糊点
    :ivar evidence: 关联的 :class:`EvidenceItem` 列表
    :ivar observability: 可观测度档位
    :ivar format_confidence: format_guess 的置信度 ∈ [0, 1]
    :ivar observability_reason: observability 判定的理由
    :ivar analysis_mode: ``"parser_only"`` / ``"llm_assisted"``
    :ivar surface_markers: 表层标记的 token 计数 dict
    :ivar structural_warnings: 结构性警告（如 "状态名是动作名" / ...）
    :ivar canonical_names: 制品中显式给出的状态名集合
    :ivar extraction_conflicts: 解析过程中发现的冲突
    :ivar parser_notes: 解析器内部备注（debug 用）
    """

    role: str
    format_guess: str
    artifact_family_guess: str
    summary: str
    elements: list[ArtifactElement] = field(default_factory=list)
    relations: list[ArtifactRelation] = field(default_factory=list)
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    format_confidence: float = 0.0
    observability_reason: str = ""
    analysis_mode: str = "parser_only"
    surface_markers: dict[str, int] = field(default_factory=dict)
    structural_warnings: list[str] = field(default_factory=list)
    canonical_names: list[str] = field(default_factory=list)
    extraction_conflicts: list[str] = field(default_factory=list)
    parser_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class InputDossier:
    """NL 需求文本解析后的 dossier (input_analyst 输出)。

    :ivar summary: NL 需求 summary
    :ivar requirements: 解析出的 :class:`RequirementTraceResult` 列表
    :ivar behaviors: 推断出的行为列表
    :ivar constraints: 推断出的约束列表
    :ivar ambiguities: 解析时的模糊点
    :ivar evidence: 关联的 evidence 列表
    :ivar observability: NL 需求的可观测度档位
    :ivar observability_reason: 判定理由
    :ivar entity_hints: 推断出的实体提示（state / event 名候选）
    :ivar context_clues: 上下文线索
    """

    summary: str
    requirements: list[RequirementTraceResult]
    behaviors: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    ambiguities: list[str] = field(default_factory=list)
    evidence: list[EvidenceItem] = field(default_factory=list)
    observability: str = "low"
    observability_reason: str = ""
    entity_hints: list[str] = field(default_factory=list)
    context_clues: list[str] = field(default_factory=list)


__all__ = [
    "ArtifactDossier",
    "ArtifactElement",
    "ArtifactRelation",
    "EvidenceRegime",
    "InputDossier",
    "ReviewContract",
]
