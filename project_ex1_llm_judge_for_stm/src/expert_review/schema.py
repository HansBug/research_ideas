"""``expert_review`` 评审制品的核心数据契约 (schema)。

本模块定义整个 LLM-as-STM-Judge pipeline 在内部传递与对外发布所用的全部
dataclass 与离散化辅助函数，是上游 ``agents/`` 与下游 ``benchmark.py`` /
``compatibility/`` / ``batch.py`` 之间的统一类型边界。

**作用**：

1. 提供 :class:`ExpertReviewRequest` / :class:`ExpertReviewResult` 这一对
   "评审请求 / 评审结果" 双 dataclass，作为整个 pipeline 的 I/O 契约；
2. 提供 :class:`DimensionReviewResult` 与 :class:`DimensionDefinition`
   等子结构，让 6 维 rubric 的输入维度与输出评分逐维成对落地；
3. 提供 :class:`EvidenceItem` / :class:`TraceLink` /
   :class:`RequirementTraceResult` / :class:`ElementIssue` 等附属数据类，
   保证 evidence locator、需求可追溯性、不被支持的预测元素等信息
   在跨 agent 调用之间不丢字段；
4. 提供 :func:`judgement_from_score` 这一连续分数到 5 档离散标签
   ("excellent" / "good" / "acceptable" / "weak" / "poor") 的
   **顶层离散化函数**；
5. 提供 :func:`to_dict` / :func:`to_json` 与各 ``*_from_dict`` 反序列化
   helper，让 JSON 化与回读对称；
6. 提供 :func:`result_to_flat_row` 把 :class:`ExpertReviewResult`
   摊平为行式 dict，专门服务 ``benchmark.py`` 写入 parquet / 报表。

**设计思路**：

1. **dataclass + slots**：所有数据结构使用 ``@dataclass(slots=True)``，
   保证字段访问轻量、内存占用可控；
2. **可选字段宽容**：所有 ``*_from_dict`` 反序列化函数对缺失字段都给
   合理 default（空字符串 / 空列表 / 0.5 confidence），不会因历史
   checkpoint JSON 缺一两个新字段而抛 ``KeyError``；
3. **score 是连续 [0, 1]**：``score`` / ``confidence`` 字段均为
   ``float``，由 :func:`judgement_from_score` 在需要 label 时离散化。
   注意此处阈值 ``≥0.90 / ≥0.75 / ≥0.55 / ≥0.35`` **与**
   ``agents/rubric_scorer.py::_band_from_score`` 的
   ``≥0.85 / ≥0.65 / ≥0.45 / ≥0.25`` 不一致——见 issue I-13；
4. **不放业务逻辑**：本模块只做"装数据 + 离散化 + 序列化"，不做
   "如何生成 score / 如何聚合"——后者归 ``agents/score_composer.py``。

**关键约束**：

* :class:`ExpertReviewResult.overall_score` 由 ``score_composer`` 经过
  mode-specific blend / penalty / rescue 计算得到（见
  ``agents/score_composer.py``），**不是** 6 维分的简单平均；
* :class:`EvidenceItem.locator` 必须在原文（NL requirements 或
  artifact 文本）中可定位，否则 ``EvidenceDiscipline`` metric 会扣分；
* 所有 dataclass 中的可变 default（list / dict）必须使用
  ``field(default_factory=...)``，否则 dataclass 会拒绝实例化。

参考：

* 总体方法学：``discussions/2026-05-08-19-20-31-...-综述.md`` §1 & §3
* 实现疑点 I-13（两套阈值不一致）：``discussions/2026-05-09-12-58-25-...-清单.md``
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any

from .llm_telemetry import LLMUsageSummary


@dataclass(slots=True)
class DimensionDefinition:
    """单个评审维度的元数据声明 (输入侧)。

    **作用**：在 ``review_policy_builder`` 构造 ``policy_packet`` 时被
    创建并下发到 ``rubric_scorer``——告诉 scorer "这一维度叫什么、占多少
    权重、用什么类型的尺度"。

    **设计思路**：与 :class:`DimensionReviewResult`（输出侧）成对——
    前者是评审 *请求* 阶段的维度声明，后者是评审 *结果* 阶段的维度
    打分。两者通过 ``name`` / ``dimension_name`` 字段关联。

    :ivar name: 维度内部标识符（如 ``"notation_syntax"``），
        必须与 ``prompts/rubric_dim_score.py::SUPPORTED_DIMS`` 一致
    :ivar title: 显示标题（用于 final_synthesizer 渲染 NL feedback）
    :ivar description: 维度描述（自然语言，3-5 句）
    :ivar weight: 在 overall_score 加权聚合时的权重（默认 1.0）
    :ivar scoring_mode: 评分模式标识，目前固定为 ``"continuous_0_1"``
    :ivar positive_examples: 正例（高分 case 描述），用于 prompt 拼接
    :ivar negative_examples: 反例（低分 case 描述）
    :ivar scoring_notes: 评分注意事项（如 pitfalls）

    Examples::

        >>> dim = DimensionDefinition(
        ...     name="notation_syntax",
        ...     title="语法规范性",
        ...     description="制品是否使用规范状态机语法",
        ...     weight=1.0,
        ... )
        >>> dim.weight
        1.0
        >>> dim.positive_examples
        []
    """

    name: str
    title: str
    description: str
    weight: float = 1.0
    scoring_mode: str = "continuous_0_1"
    positive_examples: list[str] = field(default_factory=list)
    negative_examples: list[str] = field(default_factory=list)
    scoring_notes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EvidenceItem:
    """单条 evidence quote（来自 NL requirements 或 artifact 文本）。

    **作用**：把"为什么打这个分"变成可在原文定位的具体片段，是
    EvidenceDiscipline metric 的最小计算单元。

    :ivar source: evidence 来源类型（如 ``"prediction"`` /
        ``"requirement"`` / ``"reference"``）
    :ivar snippet: 原文短片段（建议 < 200 字符）
    :ivar explanation: 为何此片段支撑当前判定的简短说明
    :ivar locator: 可定位的索引（如 ``"prediction:transition:5"``），
        若为 ``None`` 则视为不可定位（会被 EvidenceDiscipline 扣分）

    Examples::

        >>> ev = EvidenceItem(
        ...     source="prediction",
        ...     snippet="state Idle --> Running : start",
        ...     explanation="主流程进入 Running 状态",
        ...     locator="prediction:transition:0",
        ... )
        >>> ev.locator
        'prediction:transition:0'
    """

    source: str
    snippet: str
    explanation: str
    locator: str | None = None


@dataclass(slots=True)
class TraceLink:
    """需求 → 制品元素的可追溯连接 (一条 link)。

    **作用**：在 ``traceability`` agent 的输出中，每条 :class:`TraceLink`
    表示"需求 X 在制品中由元素 Y 通过关系 R 承接"，是
    ``requirement_traceability`` 维度评分与 ReasonAlign metric 的依据。

    :ivar source_id: 需求侧 id（NL requirement item 的 id）
    :ivar target_id: 制品侧 id（element / transition 的 id）
    :ivar relation: 关系类型（如 ``"matched"`` / ``"partial"`` /
        ``"missing"``）
    :ivar reason_text: 关系成立或不成立的简短理由

    Examples::

        >>> link = TraceLink(
        ...     source_id="R1",
        ...     target_id="state:Idle",
        ...     relation="matched",
        ...     reason_text="R1 'system idle' 直接对应 Idle 状态",
        ... )
        >>> link.relation
        'matched'
    """

    source_id: str
    target_id: str
    relation: str
    reason_text: str


@dataclass(slots=True)
class RequirementTraceResult:
    """单条需求的 traceability 结果 (聚合多个 :class:`TraceLink` 后)。

    **作用**：``traceability`` agent 输出列表的元素；
    ``requirement_traceability`` 维度的评分基于所有
    :class:`RequirementTraceResult` 的 ``status`` 分布
    (matched / partial / missing 占比)。

    :ivar requirement_id: 需求 id（如 ``"R1"``）
    :ivar requirement_text: 需求原文（已截断）
    :ivar status: ``"matched"`` / ``"partial"`` / ``"missing"`` /
        ``"unsupported"``
    :ivar reason_text: 状态判定的理由
    :ivar matched_element_ids: 命中的制品元素 id 列表
    :ivar confidence: 本条 trace 的置信度 ∈ [0, 1]

    Examples::

        >>> tr = RequirementTraceResult(
        ...     requirement_id="R1",
        ...     requirement_text="系统启动后进入空闲状态",
        ...     status="matched",
        ...     reason_text="Idle 状态被 [*] 进入直接覆盖",
        ...     matched_element_ids=["state:Idle"],
        ...     confidence=0.9,
        ... )
        >>> tr.status, tr.confidence
        ('matched', 0.9)
    """

    requirement_id: str
    requirement_text: str
    status: str
    reason_text: str
    matched_element_ids: list[str] = field(default_factory=list)
    confidence: float = 0.5


@dataclass(slots=True)
class ElementIssue:
    """制品中某个元素被识别出的问题 (一条 issue)。

    **作用**：``equivalence`` / ``pragmatic_quality`` /
    ``score_composer`` 等 agent 把"找到的具体问题"打包为
    :class:`ElementIssue`，最终汇入
    :attr:`ExpertReviewResult.unsupported_model_elements` 与
    :attr:`DimensionReviewResult.issues`。Benchmark 用这些 issue 与
    人评 issue 集做 IssueF1 / ReasonAlign 计算。

    :ivar element_id: 问题元素 id
    :ivar element_kind: 元素类型（``"state"`` / ``"transition"`` 等）
    :ivar element_text: 元素文本片段
    :ivar issue_type: 问题分类（``"unsupported_extra"`` /
        ``"naming_generic"`` / ``"contradiction"`` 等）
    :ivar reason_text: 问题描述

    Examples::

        >>> issue = ElementIssue(
        ...     element_id="state:Foo",
        ...     element_kind="state",
        ...     element_text="state Foo",
        ...     issue_type="unsupported_extra",
        ...     reason_text="需求未提及 Foo 状态",
        ... )
        >>> issue.issue_type
        'unsupported_extra'
    """

    element_id: str
    element_kind: str
    element_text: str
    issue_type: str
    reason_text: str


@dataclass(slots=True)
class DimensionReviewResult:
    """单维度评审结果 (输出侧，与 :class:`DimensionDefinition` 成对)。

    **作用**：``rubric_scorer`` 跑完一个维度后产出该 dataclass；
    所有维度结果汇总到 :attr:`ExpertReviewResult.dimension_results`。

    :ivar dimension_name: 维度内部标识（如 ``"notation_syntax"``）
    :ivar title: 显示标题
    :ivar score: 评分 ∈ [0, 1]（连续，非离散）
    :ivar judgement: 离散化标签，由
        :func:`agents.rubric_scorer._band_from_score` 计算得出（**注意
        阈值与 :func:`judgement_from_score` 不一致**——见 issue I-13）
    :ivar reason_text: 评分理由（一句话）
    :ivar evidence: 该维度引用的 :class:`EvidenceItem` 列表
    :ivar trace_links: 该维度产生的 :class:`TraceLink` 列表
    :ivar issues: 该维度发现的 :class:`ElementIssue` 列表
    :ivar metric_payload: 自由 dict，供存放 deterministic_estimate /
        sanity_clipped 等元信息
    :ivar confidence: LLM 自报置信度 ∈ [0, 1]

    Examples::

        >>> dim = DimensionReviewResult(
        ...     dimension_name="notation_syntax",
        ...     title="语法规范性",
        ...     score=0.7,
        ...     judgement="good",
        ...     reason_text="主体合法但有命名争议",
        ...     confidence=0.8,
        ... )
        >>> dim.score
        0.7
    """

    dimension_name: str
    title: str
    score: float
    judgement: str
    reason_text: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    trace_links: list[TraceLink] = field(default_factory=list)
    issues: list[ElementIssue] = field(default_factory=list)
    metric_payload: dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.5


@dataclass(slots=True)
class ExpertReviewRequest:
    """评审请求 — pipeline 的输入契约。

    **作用**：上游 (``run_expert_review.py`` CLI / ``batch.py`` /
    ``benchmark.py``) 把"想让 LLM 评的一对 (需求, 制品)"打包为本
    dataclass 后，交给 :class:`agent.ExpertReviewAgent` 跑。

    :ivar prompt: 评审指令（如 "请评估状态机是否覆盖需求"）
    :ivar input_text: NL 需求文本
    :ivar pred_output: 待评制品文本（PlantUML / SysML XML / 等）
    :ivar ref_output: 参考制品文本，可选（无 ref 时
        ``behavioral_consistency`` 等维度 cap 在 0.5）
    :ivar metadata: 任意元数据（如 ``case_id`` / ``llm_name`` /
        ``regime_label`` / iter-A/B/C ablation flag 等），影响 policy
        packet 与 sanity bound 选取

    Examples::

        >>> req = ExpertReviewRequest(
        ...     prompt="请评估状态机覆盖需求情况",
        ...     input_text="R1: 启动后进入空闲态",
        ...     pred_output="@startuml\\n[*] --> Idle\\n@enduml",
        ... )
        >>> req.ref_output is None
        True
    """

    prompt: str
    input_text: str
    pred_output: str
    ref_output: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExpertReviewResult:
    """评审结果 — pipeline 的输出契约。

    **作用**：``run_expert_review_workflow`` 跑完后返回的最终结果；
    所有下游评估 (benchmark / batch) 与序列化 (parquet / JSON) 都基于
    本 dataclass。

    :ivar prompt: 回填的评审 prompt
    :ivar overall_score: 顶层 overall ∈ [0, 1]，**已经过 mode-specific
        shaping**（不是 6 维分的简单平均；详见
        ``agents/score_composer.py``）
    :ivar overall_judgement: overall_score 离散化为 5 档之一
    :ivar overall_reason_text: 综合 NL 评语（由 final_synthesizer 拼装，
        若 LLM 可用则会精化）
    :ivar used_review_backend: 实际走的 backend 标识（``"rubric_llm"`` /
        ``"rubric_fallback_deterministic"`` 等）
    :ivar dimension_results: 6 个 :class:`DimensionReviewResult` 列表
    :ivar requirement_trace_results: 需求 → 制品追溯结果列表
    :ivar unsupported_model_elements: 不被需求支撑的"多余"制品元素列表
    :ivar evidence_summary: 整次评审的 evidence 摘要（去重后）
    :ivar notes: pipeline 记录的过程笔记（debug / audit 用）
    :ivar llm_model_name: 实际使用的 LLM model 名
    :ivar llm_provider: 实际命中的 provider key
    :ivar llm_usage_summary: LLM 调用次数 / 时延 / token 使用摘要
    :ivar confidence: 顶层置信度 ∈ [0, 1]，由 score_composer 按
        mode 计算（不是各维 confidence 简单平均）
    """

    prompt: str
    overall_score: float
    overall_judgement: str
    overall_reason_text: str
    used_review_backend: str
    dimension_results: list[DimensionReviewResult] = field(default_factory=list)
    requirement_trace_results: list[RequirementTraceResult] = field(default_factory=list)
    unsupported_model_elements: list[ElementIssue] = field(default_factory=list)
    evidence_summary: list[EvidenceItem] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    llm_model_name: str | None = None
    llm_provider: str | None = None
    llm_usage_summary: LLMUsageSummary = field(default_factory=LLMUsageSummary)
    confidence: float = 0.5


def judgement_from_score(score: float) -> str:
    """把连续 ∈ [0, 1] 的 score 离散化为 5 档评审标签。

    本函数是 **顶层 overall_score / human_score / dim_score** 转 label
    时使用的离散化阈值；与
    :func:`agents.rubric_scorer._band_from_score` (per-dim 内部阈值)
    **不一致**——后者使用 ``≥0.85 / 0.65 / 0.45 / 0.25``，本函数使用
    ``≥0.90 / 0.75 / 0.55 / 0.35``。这种不一致已记录为 issue I-13，
    待统一前请按当前层级正确选择函数。

    :param score: 评分 ∈ [0, 1]
    :return: 5 档之一: ``"excellent"`` / ``"good"`` / ``"acceptable"`` /
        ``"weak"`` / ``"poor"``
    :rtype: str

    Examples::

        >>> judgement_from_score(0.95)
        'excellent'
        >>> judgement_from_score(0.80)
        'good'
        >>> judgement_from_score(0.60)
        'acceptable'
        >>> judgement_from_score(0.40)
        'weak'
        >>> judgement_from_score(0.10)
        'poor'
    """
    if score >= 0.9:
        return "excellent"
    if score >= 0.75:
        return "good"
    if score >= 0.55:
        return "acceptable"
    if score >= 0.35:
        return "weak"
    return "poor"


def to_dict(value: Any) -> Any:
    """把任意 dataclass 实例递归转为 dict。

    :param value: 任意 dataclass 实例
    :return: 嵌套 dict（可直接 JSON 序列化）
    :rtype: dict

    Examples::

        >>> ev = EvidenceItem(source="x", snippet="y", explanation="z")
        >>> d = to_dict(ev)
        >>> d["source"]
        'x'
    """
    return asdict(value)


def to_json(value: Any) -> str:
    """把任意 dataclass 实例转为 JSON 字符串 (UTF-8, indent=2)。

    :param value: 任意 dataclass 实例
    :return: 缩进 2 空格的 JSON 字符串，``ensure_ascii=False``
        以保留中文
    :rtype: str

    Examples::

        >>> ev = EvidenceItem(source="x", snippet="片段", explanation="说明")
        >>> "片段" in to_json(ev)
        True
    """
    return json.dumps(asdict(value), ensure_ascii=False, indent=2)


def evidence_item_from_dict(payload: dict[str, Any]) -> EvidenceItem:
    """从 dict 反序列化为 :class:`EvidenceItem`，缺字段时给安全默认值。

    :param payload: dict（通常来自 JSON checkpoint）
    :return: :class:`EvidenceItem`
    :rtype: EvidenceItem

    Examples::

        >>> ev = evidence_item_from_dict({"source": "x", "snippet": "s"})
        >>> ev.explanation
        ''
    """
    return EvidenceItem(
        source=str(payload.get("source", "")),
        locator=payload.get("locator"),
        snippet=str(payload.get("snippet", "")),
        explanation=str(payload.get("explanation", "")),
    )


def trace_link_from_dict(payload: dict[str, Any]) -> TraceLink:
    """从 dict 反序列化为 :class:`TraceLink`。

    :param payload: dict
    :return: :class:`TraceLink`

    Examples::

        >>> tl = trace_link_from_dict({
        ...     "source_id": "R1", "target_id": "S1",
        ...     "relation": "matched", "reason_text": "ok",
        ... })
        >>> tl.relation
        'matched'
    """
    return TraceLink(
        source_id=str(payload.get("source_id", "")),
        target_id=str(payload.get("target_id", "")),
        relation=str(payload.get("relation", "")),
        reason_text=str(payload.get("reason_text", "")),
    )


def element_issue_from_dict(payload: dict[str, Any]) -> ElementIssue:
    """从 dict 反序列化为 :class:`ElementIssue`。

    :param payload: dict
    :return: :class:`ElementIssue`

    Examples::

        >>> issue = element_issue_from_dict({
        ...     "element_id": "x", "element_kind": "state",
        ...     "element_text": "state Foo", "issue_type": "extra",
        ...     "reason_text": "no req",
        ... })
        >>> issue.issue_type
        'extra'
    """
    return ElementIssue(
        element_id=str(payload.get("element_id", "")),
        element_kind=str(payload.get("element_kind", "")),
        element_text=str(payload.get("element_text", "")),
        issue_type=str(payload.get("issue_type", "")),
        reason_text=str(payload.get("reason_text", "")),
    )


def requirement_trace_from_dict(payload: dict[str, Any]) -> RequirementTraceResult:
    """从 dict 反序列化为 :class:`RequirementTraceResult`。

    :param payload: dict
    :return: :class:`RequirementTraceResult`

    Examples::

        >>> tr = requirement_trace_from_dict({
        ...     "requirement_id": "R1",
        ...     "requirement_text": "txt",
        ...     "status": "matched",
        ...     "reason_text": "ok",
        ... })
        >>> tr.confidence
        0.5
    """
    return RequirementTraceResult(
        requirement_id=str(payload.get("requirement_id", "")),
        requirement_text=str(payload.get("requirement_text", "")),
        status=str(payload.get("status", "")),
        matched_element_ids=[str(item) for item in payload.get("matched_element_ids", [])],
        reason_text=str(payload.get("reason_text", "")),
        confidence=float(payload.get("confidence", 0.5)),
    )


def dimension_review_from_dict(payload: dict[str, Any]) -> DimensionReviewResult:
    """从 dict 反序列化为 :class:`DimensionReviewResult`，
    递归还原嵌套的 evidence / trace_links / issues。

    :param payload: dict
    :return: :class:`DimensionReviewResult`

    Examples::

        >>> d = dimension_review_from_dict({
        ...     "dimension_name": "notation_syntax",
        ...     "title": "Syntax",
        ...     "score": 0.7,
        ...     "judgement": "good",
        ...     "reason_text": "ok",
        ... })
        >>> d.evidence
        []
    """
    return DimensionReviewResult(
        dimension_name=str(payload.get("dimension_name", "")),
        title=str(payload.get("title", "")),
        score=float(payload.get("score", 0.0)),
        judgement=str(payload.get("judgement", "")),
        reason_text=str(payload.get("reason_text", "")),
        evidence=[evidence_item_from_dict(item) for item in payload.get("evidence", [])],
        trace_links=[trace_link_from_dict(item) for item in payload.get("trace_links", [])],
        issues=[element_issue_from_dict(item) for item in payload.get("issues", [])],
        metric_payload=dict(payload.get("metric_payload", {})),
        confidence=float(payload.get("confidence", 0.5)),
    )


def result_to_flat_row(result: ExpertReviewResult) -> dict[str, Any]:
    """把 :class:`ExpertReviewResult` 摊平为单行 dict (parquet 友好)。

    嵌套的 list[dataclass] 字段会被 ``json.dumps`` 序列化为字符串字段
    （``*_json`` 后缀），方便存入 parquet 或 CSV 作为单元格内容。

    :param result: :class:`ExpertReviewResult` 实例
    :return: 摊平后的 dict，所有顶层字段都是标量或 JSON 字符串

    Examples::

        >>> from .llm_telemetry import LLMUsageSummary
        >>> r = ExpertReviewResult(
        ...     prompt="p", overall_score=0.7,
        ...     overall_judgement="good", overall_reason_text="ok",
        ...     used_review_backend="rubric_llm",
        ... )
        >>> row = result_to_flat_row(r)
        >>> row["overall_score"]
        0.7
        >>> row["dimension_results_json"]
        '[]'
    """
    return {
        "prompt": result.prompt,
        "used_review_backend": result.used_review_backend,
        "llm_model_name": result.llm_model_name,
        "llm_provider": result.llm_provider,
        "llm_usage_summary_json": json.dumps(asdict(result.llm_usage_summary), ensure_ascii=False, sort_keys=True),
        "overall_score": result.overall_score,
        "overall_judgement": result.overall_judgement,
        "overall_reason_text": result.overall_reason_text,
        "dimension_results_json": json.dumps(
            [asdict(item) for item in result.dimension_results],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "requirement_trace_results_json": json.dumps(
            [asdict(item) for item in result.requirement_trace_results],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "unsupported_model_elements_json": json.dumps(
            [asdict(item) for item in result.unsupported_model_elements],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "evidence_summary_json": json.dumps(
            [asdict(item) for item in result.evidence_summary],
            ensure_ascii=False,
            sort_keys=True,
        ),
        "notes_json": json.dumps(result.notes, ensure_ascii=False, sort_keys=True),
        "confidence": result.confidence,
    }
