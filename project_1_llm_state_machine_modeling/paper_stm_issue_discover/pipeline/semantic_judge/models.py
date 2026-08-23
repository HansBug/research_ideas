"""Pydantic protocols for the arm-neutral issue #195 semantic Judge."""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    """Base for immutable cross-stage Judge records with no implicit fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class MatchStrength(str, Enum):
    """Issue #195 dimension A: semantic relation between one report and expected issue."""

    FULL_MATCH = "FULL_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"


class ReportValidity(str, Enum):
    """Issue #195 dimension B: report truth and known/novel ownership."""

    VALID_KNOWN = "VALID_KNOWN"
    VALID_NOVEL = "VALID_NOVEL"
    INVALID = "INVALID"


class ArtifactAuthority(str, Enum):
    """Closed roles that prevent author source, lowered model, and facts being conflated."""

    NORMATIVE_SOURCE = "normative_source"
    AUTHOR_SOURCE = "author_source"
    CLOSED_MODEL = "closed_model"
    DETERMINISTIC_FACT = "deterministic_fact"
    MAPPING = "mapping"
    PROVENANCE = "provenance"


class ArtifactRole(str, Enum):
    """Complete common pair artifact roles exposed identically to both input adapters."""

    NATURAL_LANGUAGE = "natural_language"
    PLANTUML_SOURCE = "plantuml_source"
    FCSTM_MODEL = "fcstm_model"
    CANONICAL_SOURCE_IR = "canonical_source_ir"
    EXACT_SOURCE_INVENTORY = "exact_source_inventory"
    REFERENCE_INSPECTION = "reference_inspection"
    INSPECTION_EQUIVALENT_FACTS = "inspection_equivalent_facts"
    VERIFY_FACTS = "verify_facts"
    SMT_FACTS = "smt_facts"
    WORKING_CONTRACT = "working_contract"
    SOURCE_TRACE = "source_trace"
    CASE_REPORT = "case_report"


class CandidateEvidence(FrozenModel):
    """One report-owned evidence statement, never a method-only W/D/predicate verdict."""

    evidence_ref: str = Field(
        min_length=1,
        description="报告自身引用的匿名 evidence ID；来源臂没有证据时列表为空，下游只用它审计主张，不作参评门槛。",
    )
    statement: str = Field(
        min_length=1,
        description="报告实际给出的技术证据陈述；它是候选性材料，不代表 Judge 已确认真实性。",
    )


class CandidateReport(FrozenModel):
    """Arm-neutral projection of one actually published atomic technical report.

    Adapters produce this object and the unified Judge consumes it. It owns only
    semantic content present in the final report; it has no authority over truth,
    matching, W/D/L, predicates, or historical scores.
    """

    schema_version: Literal["paper1.semantic-judge.candidate-report.v1"] = Field(
        default="paper1.semantic-judge.candidate-report.v1",
        description="候选报告协议版本；用于持久化兼容，不表达报告质量。",
    )
    report_id: str = Field(
        pattern=r"^R\d{4}$",
        description="pair 内匿名报告 ID，只用于 exact closure；不得从编号、顺序或前缀推断实验臂或语义。",
    )
    claim: str = Field(
        min_length=1,
        description="报告实际发布的原子技术主张；它是候选性陈述，Judge 必须另行验证，不能直接采信。",
    )
    where: str | None = Field(
        default=None,
        description="报告自身给出的 locus/where；null 表示原报告未提供，不能由适配器替该臂补写。",
    )
    property: str | None = Field(
        default=None,
        description="报告自身明确声称被违反的 property；null 表示原报告没有 typed property，绝不构成 FULL 或 validity 的阻断。",
    )
    violated_obligation: str | None = Field(
        default=None,
        description="报告自身表述的规范义务；null 表示没有独立字段，下游可从 claim/reason 审计但适配器不得合成。",
    )
    expected: str | None = Field(
        default=None,
        description="报告自身描述的应然行为；null 表示原报告未拆分 expected/observed，而非没有语义内容。",
    )
    observed: str | None = Field(
        default=None,
        description="报告自身描述的实然行为；null 表示原报告未单列观察，不得以缺字段惩罚报告。",
    )
    reason: str = Field(
        min_length=1,
        description="报告发布时实际拥有的因果解释；属于候选证据，Judge 用公共制品独立复核。",
    )
    basis: str | None = Field(
        default=None,
        description="报告实际拥有的制品依据；null 表示原臂没有 basis 字段，不能推导或补写 method-only dossier。",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="报告实际携带的 NL/source/model/fact refs；空集合表示原报告没有结构化 refs，不影响参评资格。",
    )
    evidence: tuple[CandidateEvidence, ...] = Field(
        default_factory=tuple,
        description="报告自身可公开审计的证据陈述；不包含 W/D/L、predicate、编译计划或隐藏中间推理。",
    )


class ExpectedAxisHints(FrozenModel):
    """Optional frozen-ledger taxonomy hints that describe but never gate semantic FULL."""

    defect_locus: str | None = Field(
        default=None,
        description="台账描述的缺陷 locus 提示；null 表示未标注，Judge 不得要求报告逐字段相同。",
    )
    defect_element: str | None = Field(
        default=None,
        description="台账描述的 element 提示；只辅助理解 expected，不是 exact-field hit gate。",
    )
    defect_qualifier: str | None = Field(
        default=None,
        description="台账描述的 qualifier 提示；null 不影响 expected 身份。",
    )
    defect_logic_kind: str | None = Field(
        default=None,
        description="台账描述的 logic kind；只作语义背景，不是报告资格条件。",
    )
    defect_reference: str | None = Field(
        default=None,
        description="台账描述的 reference authority；与报告证据强度或 W 无关。",
    )


class ExpectedIssue(FrozenModel):
    """One D2/D1 frozen expected issue after removing D/L and scoring metadata.

    The ledger adapter produces this expected-denominator object. It defines the
    semantic target for recall, but does not decide any report's truth or match.
    """

    schema_version: Literal["paper1.semantic-judge.expected-issue.v1"] = Field(
        default="paper1.semantic-judge.expected-issue.v1",
        description="匿名 expected issue 投影版本；不暴露 ledger 的 D/L。",
    )
    expected_id: str = Field(
        pattern=r"^E\d{4}$",
        description="pair 内匿名 expected ID，只用于完整关系矩阵；原 ledger ID 仅保存在 provider 外 mapping。",
    )
    summary: str = Field(
        min_length=1,
        description="冻结台账的核心缺陷摘要，是 expected 语义身份的一部分。",
    )
    detail: str = Field(
        min_length=1,
        description="冻结台账的完整缺陷机制、locus、后果和边界；用于宽语义 FULL/PARTIAL 裁定。",
    )
    source_statement: str | None = Field(
        default=None,
        description="台账 provenance 中的原始/复核技术陈述；null 表示没有该字段，不改变 expected 分母。",
    )
    axes: ExpectedAxisHints = Field(
        description="台账 taxonomy 提示；只辅助理解，不得退化成 exact locus/property/scope/direction gate。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="expected 可回溯的 ledger/NL 制品引用；Judge basis 应结合公共 closure 复核。",
    )


class ArtifactDocument(FrozenModel):
    """One immutable common artifact with explicit authority and exact content hash."""

    artifact_id: str = Field(
        pattern=r"^artifact:[a-z0-9_-]+$",
        description="pair 内稳定 artifact 引用，供 Judge basis/source_refs 精确引用。",
    )
    role: ArtifactRole = Field(
        description="制品在统一闭包中的闭集角色；同一 pair 对所有实验臂完全相同。"
    )
    authority: ArtifactAuthority = Field(
        description="制品权威边界；防止作者源、closed model、deterministic facts 和 provenance 相互冒充。"
    )
    sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="该制品投影内容的 SHA-256，用于两臂公共闭包 identity 检查。",
    )
    schema_version: str = Field(
        min_length=1, description="制品自身 schema/version；纯文本使用明确 text 版本。"
    )
    content: str = Field(
        min_length=1,
        description="完整 UTF-8 文本或稳定 JSON 文本；事实性权威由 role/authority 决定，不由报告决定。",
    )
    reason: str = Field(
        min_length=1, description="为何该制品属于真实性仲裁所需公共闭包。"
    )
    basis: str = Field(
        min_length=1, description="制品来源和构建算法依据，不含实验臂或历史分数。"
    )


class JudgeArtifactClosure(FrozenModel):
    """Arm-independent pair evidence closure used for report validity arbitration."""

    schema_version: Literal["paper1.semantic-judge.artifact-closure.v2"] = Field(
        default="paper1.semantic-judge.artifact-closure.v2",
        description="公共制品闭包 schema 版本；任何内容/截断策略变化都必须改变版本或 hash。",
    )
    pair_id: str = Field(
        pattern=r"^\d{4}$",
        description="冻结 pair 身份；仅用于选择同一公共制品，不表示实验臂。",
    )
    artifacts: tuple[ArtifactDocument, ...] = Field(
        min_length=1,
        description="按固定 role 顺序排列的完整公共制品；不得按报告来源臂增删、重排或截断。",
    )
    closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="除本字段外整个闭包稳定 JSON 的 SHA-256，用于 apples-to-apples 证明。",
    )
    reason: str = Field(
        min_length=1, description="公共闭包为何足以审计真实性且对两臂公平。"
    )
    basis: str = Field(
        min_length=1, description="闭包 builder 版本、PairInput 和逐制品 hash 依据。"
    )

    @model_validator(mode="after")
    def unique_artifact_roles_and_ids(self) -> JudgeArtifactClosure:
        ids = [item.artifact_id for item in self.artifacts]
        roles = [item.role for item in self.artifacts]
        if len(ids) != len(set(ids)):
            raise ValueError(
                f"artifact_closure.artifacts has duplicate artifact_id values: {ids}"
            )
        if len(roles) != len(set(roles)):
            raise ValueError(
                f"artifact_closure.artifacts has duplicate role values: {roles}"
            )
        return self


class UnifiedJudgeInput(FrozenModel):
    """Complete arm-neutral provider input shared after source-specific adaptation."""

    schema_version: Literal["paper1.semantic-judge.input.v1"] = Field(
        default="paper1.semantic-judge.input.v1",
        description="统一 Judge 输入协议版本；两臂必须进入同一 class 和 serialization。",
    )
    protocol_version: str = Field(
        min_length=1,
        description="冻结 issue #195 protocol version；语义变化会使旧分数失效。",
    )
    pair_id: str = Field(
        pattern=r"^\d{4}$",
        description="被裁 pair；输入不含 arm 名称、历史结果或方法标签。",
    )
    reports: tuple[CandidateReport, ...] = Field(
        description="实际发布报告的匿名 arm-neutral 投影；允许为空，禁止补写原臂没有的语义。"
    )
    expected_issues: tuple[ExpectedIssue, ...] = Field(
        min_length=1,
        description="该 pair 冻结 D2+D1 expected 分母的匿名投影；不含 D/L。",
    )
    artifact_closure: JudgeArtifactClosure = Field(
        description="对所有实验臂逐字相同的公共真实性审计闭包。"
    )
    reason: str = Field(
        min_length=1, description="输入如何由匿名报告、冻结 expected 和公共闭包组成。"
    )
    basis: str = Field(
        min_length=1,
        description="adapter、ledger projection、artifact builder 和 protocol hash 依据。",
    )

    @model_validator(mode="after")
    def exact_input_identity(self) -> UnifiedJudgeInput:
        if self.artifact_closure.pair_id != self.pair_id:
            raise ValueError(
                "artifact_closure.pair_id conflicts with input pair_id: "
                f"expected {self.pair_id}, actual {self.artifact_closure.pair_id}"
            )
        report_ids = [item.report_id for item in self.reports]
        expected_ids = [item.expected_id for item in self.expected_issues]
        if len(report_ids) != len(set(report_ids)):
            raise ValueError(
                f"reports contains duplicate report_id values: {report_ids}"
            )
        if len(expected_ids) != len(set(expected_ids)):
            raise ValueError(
                f"expected_issues contains duplicate expected_id values: {expected_ids}"
            )
        return self


class RelationAssessment(FrozenModel):
    """One required dimension-A decision for an exact report/expected pair."""

    report_id: str = Field(
        min_length=1, description="被比较的匿名 report ID；必须来自输入 exact closure。"
    )
    expected_id: str = Field(
        min_length=1,
        description="被比较的匿名 expected ID；必须来自输入 exact closure。",
    )
    match: MatchStrength = Field(
        description="issue #195 维度 A；与报告 validity 分开，PARTIAL 既不 hit 也不 FP。"
    )
    reason: str = Field(
        min_length=1,
        description="为什么两者是 FULL/PARTIAL/NO；需说明 root cause、义务、症状或修复重叠边界。",
    )
    basis: str = Field(
        min_length=1,
        description="支持关系判断的 supplied report、expected 与公共 artifact 事实。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="关系判断实际引用的 report/expected/artifact refs；不得为空。",
    )


class ReportJudgment(FrozenModel):
    """LLM-authored dimension-B and root-cause judgment without derived ID sets."""

    report_id: str = Field(
        min_length=1, description="被裁报告的匿名 ID；在 response 中必须 exactly once。"
    )
    validity: ReportValidity = Field(
        description="issue #195 维度 B；只有 INVALID 是 semantic FP。"
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="基于可行动技术根因的稳定短语 key；不得使用 report ID/顺序，邻近但不同 property/source 不合并。",
    )
    reason: str = Field(
        min_length=1,
        description="为什么报告主张成立/不成立以及 KNOWN/NOVEL 归属；不得由 unmatched 自动推出。",
    )
    basis: str = Field(
        min_length=1,
        description="真实性裁定引用的 NL、PlantUML、FCSTM、facts 或完整语义审计依据。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="报告 validity 实际引用的 supplied source refs；不得为空。",
    )


class ExpectedJudgment(FrozenModel):
    """LLM-authored expected-side semantic explanation without derived coverage fields."""

    expected_id: str = Field(
        min_length=1,
        description="被解释 expected 的匿名 ID；在 response 中必须 exactly once。",
    )
    reason: str = Field(
        min_length=1,
        description="该 expected 与所有报告关系的语义总结；hit/support 由后端矩阵确定性派生。",
    )
    basis: str = Field(
        min_length=1,
        description="逐 relation、validity 和公共制品依据；不得自报计分数字。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="expected judgment 实际引用的 expected/report/artifact refs。",
    )


class JudgeResponse(FrozenModel):
    """LLM response containing only semantic judgments, never deterministic summaries."""

    schema_version: Literal["paper1.semantic-judge.response.v2"] = Field(
        default="paper1.semantic-judge.response.v2",
        description="provider structured-output schema 版本；derived sets/hit/support 从 v2 起由后端唯一生成。",
    )
    relations: tuple[RelationAssessment, ...] = Field(
        description="report x expected 完整矩阵，包含所有 NO_MATCH，不能稀疏省略。"
    )
    report_judgments: tuple[ReportJudgment, ...] = Field(
        description="每条 report exactly once 的 validity/root-cause/reason/basis。"
    )
    expected_judgments: tuple[ExpectedJudgment, ...] = Field(
        description="每条 expected exactly once 的语义 reason/basis；不重复填写可派生集合。"
    )
    reason: str = Field(
        min_length=1, description="本次完整判读的总体语义结论，不得只复述计数。"
    )
    basis: str = Field(
        min_length=1,
        description="本次判读使用的协议、匿名输入和公共 artifact closure 依据。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="顶层判读实际依赖的 supplied artifact/report/expected refs。",
    )


class ReportAssessment(FrozenModel):
    """One dimension-B validity decision plus exhaustive relation-derived ownership."""

    report_id: str = Field(
        min_length=1, description="被裁报告的匿名 ID；在响应中必须 exactly once。"
    )
    validity: ReportValidity = Field(
        description="issue #195 维度 B；只有 INVALID 是 semantic FP。"
    )
    full_expected_ids: tuple[str, ...] = Field(
        description="该报告 FULL_MATCH 的全部 expected IDs；由 relation matrix 精确派生。"
    )
    partial_expected_ids: tuple[str, ...] = Field(
        description="该报告 PARTIAL_MATCH 的全部 expected IDs；只支持 coverage，不算 hit/FP。"
    )
    no_match_expected_ids: tuple[str, ...] = Field(
        description="该报告 NO_MATCH 的全部 expected IDs；三组必须精确覆盖 expected closure。"
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="基于可行动技术根因的稳定短语 key，用于重复率和 cluster precision；不得使用 report ID/顺序。",
    )
    reason: str = Field(
        min_length=1,
        description="为什么报告主张成立/不成立以及 KNOWN/NOVEL 归属；不得由 unmatched 自动推出。",
    )
    basis: str = Field(
        min_length=1,
        description="真实性裁定引用的 NL、PlantUML、FCSTM、facts 或完整语义审计依据。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="报告 validity 实际引用的 supplied source refs；不得为空。",
    )


class ExpectedAssessment(FrozenModel):
    """One exhaustive expected-side coverage decision derived from valid reports."""

    expected_id: str = Field(
        min_length=1, description="被汇总 expected 的匿名 ID；响应中必须 exactly once。"
    )
    full_report_ids: tuple[str, ...] = Field(
        description="对该 expected 为 FULL 且报告 validity=VALID_KNOWN 的报告 IDs。"
    )
    partial_report_ids: tuple[str, ...] = Field(
        description="对该 expected 为 PARTIAL 且报告 validity=VALID_KNOWN 的报告 IDs。"
    )
    no_support_report_ids: tuple[str, ...] = Field(
        description="未形成有效 FULL/PARTIAL 支持的其余全部报告 IDs。"
    )
    hit: bool = Field(
        description="是否存在 VALID_KNOWN + FULL_MATCH；仅该值贡献主 hit。"
    )
    supported: bool = Field(
        description="是否存在 VALID_KNOWN + FULL/PARTIAL；INVALID 不贡献支持。"
    )
    reason: str = Field(
        min_length=1,
        description="该 expected hit/support 状态的语义解释，重复报告只计一次 expected。",
    )
    basis: str = Field(
        min_length=1, description="对应 relation 和 validity 以及公共制品依据。"
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="expected assessment 实际引用的 expected/report/artifact refs。",
    )


class JudgeReading(FrozenModel):
    """One complete independent or arbitrated issue #195 reading of a pair."""

    schema_version: Literal["paper1.semantic-judge.reading.v1"] = Field(
        default="paper1.semantic-judge.reading.v1",
        description="完整判读 schema 版本；不编码 primary/arbitration 身份。",
    )
    relations: tuple[RelationAssessment, ...] = Field(
        description="report x expected 完整矩阵，包含所有 NO_MATCH，不能稀疏省略。"
    )
    report_assessments: tuple[ReportAssessment, ...] = Field(
        description="每条 report exactly once 的 dimension-B 与聚类裁定。"
    )
    expected_assessments: tuple[ExpectedAssessment, ...] = Field(
        description="每条 expected exactly once 的 hit/support 审计。"
    )
    reason: str = Field(
        min_length=1, description="本次完整判读的总体语义结论，不得只复述计数。"
    )
    basis: str = Field(
        min_length=1,
        description="本次判读使用的协议、匿名输入和公共 artifact closure 依据。",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="顶层判读实际依赖的 supplied artifact/report/expected refs。",
    )


class ConflictKind(str, Enum):
    """Deterministically detectable disagreements requiring semantic arbitration."""

    RELATION = "relation"
    VALIDITY = "validity"
    ROOT_CAUSE_CLUSTER = "root_cause_cluster"


class ConflictRecord(FrozenModel):
    """Audit trail for one primary-reading disagreement and arbitrated outcome."""

    kind: ConflictKind = Field(
        description="冲突属于 relation、validity 或 root-cause clustering。"
    )
    object_ref: str = Field(
        min_length=1,
        description="冲突对象的稳定匿名引用，例如 report:R0001/expected:E0002。",
    )
    reading_1_value: str = Field(
        min_length=1, description="第一次独立判读的枚举或 cluster value。"
    )
    reading_2_value: str = Field(
        min_length=1, description="第二次独立判读的枚举或 cluster value。"
    )
    final_value: str = Field(
        min_length=1, description="重新查看完整制品后仲裁采用的最终值，不能是 UNKNOWN。"
    )
    reason: str = Field(
        min_length=1, description="最终为何选择该值，而非按多数投票或按实验臂补票。"
    )
    basis: str = Field(
        min_length=1, description="最终 reading 中对应 relation/report 的制品依据。"
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="仲裁冲突实际引用的 supplied refs。"
    )


class ReadingDisagreement(FrozenModel):
    """Provider-visible primary disagreement before a final value is selected."""

    kind: ConflictKind = Field(
        description="需要仲裁的 relation、validity 或 root-cause clustering 冲突类型。"
    )
    object_ref: str = Field(
        min_length=1,
        description="冲突的匿名 report/expected 对象引用；不暴露原始臂 ID。",
    )
    reading_1_value: str = Field(min_length=1, description="第一次独立判读的结构化值。")
    reading_2_value: str = Field(min_length=1, description="第二次独立判读的结构化值。")


class ArbitrationInput(FrozenModel):
    """Complete typed arbitration input containing no arm or method-only metadata."""

    schema_version: Literal["paper1.semantic-judge.arbitration-input.v1"] = Field(
        default="paper1.semantic-judge.arbitration-input.v1",
        description="统一仲裁输入版本；只在两次独立判读发生实质冲突时构建。",
    )
    judge_input: UnifiedJudgeInput = Field(
        description="与 primary 完全相同的匿名 reports、expected 和公共 artifact closure。"
    )
    primary_reading_1: JudgeReading = Field(
        description="第一次完整独立判读及其 reason/basis/source refs。"
    )
    primary_reading_2: JudgeReading = Field(
        description="第二次完整独立判读及其 reason/basis/source refs。"
    )
    disagreements: tuple[ReadingDisagreement, ...] = Field(
        min_length=1,
        description="确定性比较枚举/validity/cluster 后得到的全部实质冲突；文本措辞差异不列入。",
    )
    reason: str = Field(
        min_length=1, description="为什么必须重新查看完整制品而不能投票或保留 UNKNOWN。"
    )
    basis: str = Field(
        min_length=1, description="issue #195 双读仲裁合同和 exact conflict detection。"
    )


class UsageReceipt(FrozenModel):
    """Normalized provider usage for one Judge model call, including cache accounting."""

    model_call_id: str | None = Field(
        default=None,
        description="provider/public runtime call ID；null 表示 provider error 未暴露 ID。",
    )
    status: str = Field(min_length=1, description="该调用 attempt 的完成/失败状态。")
    model: str | None = Field(
        default=None, description="provider 实际报告的 model ID；null 表示不可观测。"
    )
    input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="规范化总 input tokens；null 表示 provider 未提供。",
    )
    output_tokens: int | None = Field(
        default=None,
        ge=0,
        description="规范化 output tokens；null 表示 provider 未提供。",
    )
    cache_read_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="input_token_details.cache_read 的规范化值；null 表示未报告。",
    )
    cache_write_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="provider cache creation/write tokens；null 表示未报告。",
    )
    cost_counted: bool = Field(
        description="该 usage 是否按既定 provider-error exemption 计费。"
    )
    billing_disposition: str = Field(
        min_length=1,
        description="billable、provider_error_retry_exempt 或明确不可观测状态。",
    )
    raw_usage_json: str = Field(
        min_length=1,
        description="完整规范化 usage row 的稳定 JSON，保留未知 provider 字段而不以自由 dict 跨阶段传递。",
    )


class RetryRecord(FrozenModel):
    """One outer or transport retry audit row for a Judge call."""

    attempt_no: int = Field(
        ge=1, description="本 Judge cell 内从 1 开始的 attempt 序号。"
    )
    status: str = Field(
        min_length=1,
        description="attempt 终态，例如 success、exception、provider_error。",
    )
    provider_error: bool = Field(
        description="是否为 provider 侧错误；仅该类 retry 可费用豁免。"
    )
    error_code: str | None = Field(
        default=None, description="结构化错误 code；null 表示成功或 provider 未提供。"
    )
    error_message: str | None = Field(
        default=None, description="可审计错误消息；null 表示无错误，禁止包含 secret。"
    )
    billing_disposition: str = Field(
        min_length=1, description="该 attempt 的费用处理口径。"
    )
    raw_attempt_json: str = Field(
        min_length=1, description="完整脱敏 attempt/retry 元数据的稳定 JSON。"
    )


class JudgeCallReceipt(FrozenModel):
    """Persistent receipt for one primary or arbitration structured Judge call."""

    call_id: str = Field(
        min_length=1,
        description="pair 内稳定 call ID；只标识审计文件，不承载判决语义。",
    )
    phase: Literal["primary_1", "primary_2", "arbitration"] = Field(
        description="调用在双读仲裁流程中的角色。"
    )
    status: Literal["success", "failed"] = Field(
        description="结构化调用是否得到完整、已验证 reading。"
    )
    profile: str = Field(
        min_length=1, description="统一 Judge 使用的 utils.llm profile；两臂必须相同。"
    )
    schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="本 pair exact-closure response schema hash。",
    )
    prompt_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="实际 system+user prompt hash；用于协议冻结审计。",
    )
    usage: tuple[UsageReceipt, ...] = Field(
        description="所有成功、失败和 retry usage；provider error 豁免逐 row 保存。"
    )
    retries: tuple[RetryRecord, ...] = Field(
        description="outer/transport retry 记录；空集合表示没有 retry。"
    )
    cost_usd: float = Field(
        ge=0,
        description="runtime 按 normalized usage 计算的本 call Judge cost；不作为优化目标。",
    )
    cost_eligible: bool = Field(
        description="所有计费 usage 是否都有完整 pricing/token 数据。"
    )
    artifact_paths: tuple[str, ...] = Field(
        description="public runtime prompt/raw/result/audit 路径；只用于复核，不发送回 provider。"
    )
    reason: str = Field(min_length=1, description="调用为何成功/失败及是否需要仲裁。")
    basis: str = Field(
        min_length=1, description="utils.llm/AgentApp、profile、schema 和 retry 依据。"
    )


class ExpectedOutcome(FrozenModel):
    """Deterministic decoded expected outcome using the original frozen ledger ID."""

    ledger_id: str = Field(
        min_length=1, description="provider 外恢复的冻结 ledger ID，用于正式逐条汇总。"
    )
    hit: bool = Field(description="是否存在 final VALID_KNOWN + FULL_MATCH。")
    supported: bool = Field(description="是否存在 final VALID_KNOWN + FULL/PARTIAL。")
    full_report_ids: tuple[str, ...] = Field(
        description="命中该 expected 的原始发布报告 IDs；重复只计一次 expected。"
    )
    partial_report_ids: tuple[str, ...] = Field(
        description="仅支持该 expected 的原始发布报告 IDs。"
    )
    reason: str = Field(
        min_length=1, description="final expected assessment 的原始语义解释。"
    )
    basis: str = Field(
        min_length=1, description="final expected assessment 的制品与 relation 依据。"
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="final expected assessment 的 supplied refs。"
    )


class ReportOutcome(FrozenModel):
    """Deterministic decoded report outcome using the source artifact's original ID."""

    original_report_id: str = Field(
        min_length=1, description="provider 外 adapter mapping 恢复的原始 report ID。"
    )
    validity: ReportValidity = Field(
        description="final dimension-B classification；只有 INVALID 计 semantic FP。"
    )
    full_ledger_ids: tuple[str, ...] = Field(
        description="final FULL_MATCH 的原始 ledger IDs。"
    )
    partial_ledger_ids: tuple[str, ...] = Field(
        description="final PARTIAL_MATCH 的原始 ledger IDs。"
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="final root-cause cluster key，用于 cluster metrics 与 redundancy。",
    )
    reason: str = Field(min_length=1, description="final report validity 的 reason。")
    basis: str = Field(
        min_length=1, description="final report validity 的 artifact basis。"
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="final report validity 的 supplied refs。"
    )


class SemanticMetrics(FrozenModel):
    """Issue #195 deterministic pair/run metrics; no LLM may self-report these values."""

    schema_version: Literal["paper1.semantic-judge.metrics.v1"] = Field(
        default="paper1.semantic-judge.metrics.v1",
        description="确定性计分器 schema 版本。",
    )
    expected_count: int = Field(ge=0, description="冻结 D2+D1 expected 分母。")
    full_hit_count: int = Field(
        ge=0, description="unique VALID_KNOWN+FULL hit expected 数。"
    )
    fn_count: int = Field(ge=0, description="expected_count - full_hit_count。")
    supported_count: int = Field(
        ge=0, description="被 valid FULL 或 PARTIAL 覆盖的 unique expected 数。"
    )
    hit_rate: float = Field(ge=0, le=1, description="full_hit_count / expected_count。")
    supported_rate: float = Field(
        ge=0, le=1, description="supported_count / expected_count。"
    )
    report_count: int = Field(
        ge=0, description="全部 final 已裁定发布报告数；最终无 UNKNOWN。"
    )
    valid_known_count: int = Field(ge=0, description="VALID_KNOWN raw report 数。")
    valid_novel_count: int = Field(
        ge=0, description="VALID_NOVEL raw report 数；不 hit、不 FP。"
    )
    invalid_count: int = Field(
        ge=0, description="INVALID raw report 数，也是唯一 Semantic FP。"
    )
    semantic_precision: float = Field(
        ge=0, le=1, description="(VALID_KNOWN+VALID_NOVEL)/report_count。"
    )
    ledger_unmatched_count: int = Field(
        ge=0,
        description="只有 PARTIAL 的 known + novel + invalid；仅 legacy 诊断，禁止命名 FP。",
    )
    cluster_count: int = Field(
        ge=0, description="按 final actionable root-cause key 去重后的全部 cluster 数。"
    )
    valid_cluster_count: int = Field(
        ge=0, description="valid known/novel root-cause cluster 数。"
    )
    invalid_cluster_count: int = Field(
        ge=0, description="invalid root-cause cluster 数。"
    )
    root_cause_cluster_precision: float = Field(
        ge=0, le=1, description="valid_cluster_count / cluster_count。"
    )
    redundancy_rate: float = Field(
        ge=0,
        le=1,
        description="(report_count-cluster_count)/report_count；重复 valid 不计 FP。",
    )
    valid_redundancy_rate: float = Field(
        ge=0, le=1, description="仅 valid reports 的 cluster 重复率。"
    )
    reason: str = Field(
        min_length=1,
        description="计分器对 hit/support/FP/precision/cluster 的确定性说明。",
    )
    basis: str = Field(
        min_length=1, description="issue #195 公式与 final exact-closure reading。"
    )


class AdapterIdMap(FrozenModel):
    """Provider-external reversible mapping between anonymous and source IDs."""

    anonymous_id: str = Field(min_length=1, description="进入 provider 的匿名 R/E ID。")
    original_id: str = Field(
        min_length=1,
        description="原始 artifact 或 frozen ledger ID；绝不进入 provider payload。",
    )


class AdapterAudit(FrozenModel):
    """Evidence that source-specific adaptation ended before the shared Judge path."""

    schema_version: Literal["paper1.semantic-judge.adapter-audit.v1"] = Field(
        default="paper1.semantic-judge.adapter-audit.v1",
        description="provider 外 adapter 审计 schema。",
    )
    source_format: Literal["x1v2_record", "evidence_discovery_release"] = Field(
        description="仅写入本地 audit；该字段及 arm identity 不进入 UnifiedJudgeInput。",
    )
    source_path: str = Field(
        min_length=1, description="被重判原始结果路径；用于 provenance，不输入 Judge。"
    )
    source_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="原始结果 bytes hash。"
    )
    report_id_map: tuple[AdapterIdMap, ...] = Field(
        description="匿名 report IDs 到原始 release IDs 的 exact mapping。"
    )
    expected_id_map: tuple[AdapterIdMap, ...] = Field(
        description="匿名 expected IDs 到 ledger IDs 的 exact mapping。"
    )
    projected_field_names: tuple[str, ...] = Field(
        description="两臂统一 CandidateReport schema 的字段名，用于字段级公平性 diff。"
    )
    excluded_field_names: tuple[str, ...] = Field(
        description="明确排除的 arm/W/D/L/predicate/history 字段审计。"
    )
    reason: str = Field(
        min_length=1, description="适配器如何只投影原报告实际拥有的语义。"
    )
    basis: str = Field(
        min_length=1, description="source artifact、adapter version 和匿名化规则。"
    )


class PairJudgeResult(FrozenModel):
    """Self-contained pair result with two readings, arbitration, metrics, and audit."""

    schema_version: Literal["paper1.semantic-judge.pair-result.v1"] = Field(
        default="paper1.semantic-judge.pair-result.v1",
        description="统一 pair Judge 持久化协议版本。",
    )
    run_id: str = Field(
        min_length=1, description="本次 Judge run ID；不同 protocol/code 输入不得复用。"
    )
    pair_id: str = Field(pattern=r"^\d{4}$", description="被重判 pair。")
    round: int = Field(ge=1, description="原发布报告所属实验轮次；不影响语义判决。")
    protocol_version: str = Field(
        min_length=1, description="issue #195 冻结 protocol version。"
    )
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="issue #195 正文原始 bytes SHA-256。"
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="统一 runner/仲裁/持久化算法版本。"
    )
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="实际执行 Judge 的 git commit。"
    )
    model_profile: str = Field(
        min_length=1, description="两次独立判读及仲裁共用的 gpt-5.6-luna profile。"
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="两臂同 pair 必须完全相同的公共 artifact hash。",
    )
    serialized_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="匿名统一 Judge input 的稳定 JSON hash。",
    )
    response_schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="该 pair exact closure dynamic schema hash。",
    )
    prompt_template_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="冻结 system/primary/arbitration prompt template hash。",
    )
    adapter_audit: AdapterAudit = Field(
        description="provider 外 source adaptation/匿名映射证据。"
    )
    primary_reading_1: JudgeReading = Field(description="第一次独立完整判读。")
    primary_reading_2: JudgeReading = Field(description="第二次独立完整判读。")
    arbitration_reading: JudgeReading | None = Field(
        default=None,
        description="存在枚举/validity/cluster 冲突时的完整仲裁判读；无冲突为 null。",
    )
    conflicts: tuple[ConflictRecord, ...] = Field(
        description="两次 primary 的全部实质冲突及 final 选择；文本措辞差异不算冲突。"
    )
    final_reading: JudgeReading = Field(
        description="无 UNKNOWN 的最终权威 reading；有冲突时必须来自 arbitration。"
    )
    report_outcomes: tuple[ReportOutcome, ...] = Field(
        description="provider 外解码后的逐原始报告 K/N/I、关系与聚类审计。"
    )
    expected_outcomes: tuple[ExpectedOutcome, ...] = Field(
        description="provider 外解码后的逐 ledger hit/support 审计。"
    )
    metrics: SemanticMetrics = Field(
        description="从 final reading 确定性重算的 pair metrics。"
    )
    call_receipts: tuple[JudgeCallReceipt, ...] = Field(
        description="两次 primary 及可选 arbitration 的完整 usage/cost/retry receipts。"
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="只有完整双读、必要仲裁和 exact accounting 后才能 completed。",
    )
    reason: str = Field(
        min_length=1, description="pair 完整性、冲突处理和最终分类概述。"
    )
    basis: str = Field(
        min_length=1,
        description="protocol、input/schema/prompt hash、public runtime 与 deterministic metrics 依据。",
    )


class RunPairReceipt(FrozenModel):
    """One pair/round location and terminal status in a semantic Judge run."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="冻结 pair ID。")
    round: int = Field(ge=1, description="原始发布轮次。")
    result_path: str = Field(
        min_length=1, description="完整 PairJudgeResult JSON 路径。"
    )
    result_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="PairJudgeResult bytes hash。"
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="该 pair 公共制品闭包 hash。"
    )
    report_count: int = Field(ge=0, description="被裁发布报告数。")
    expected_count: int = Field(ge=0, description="冻结 expected 分母数。")
    status: Literal["completed"] = Field(
        default="completed", description="无 crash、漏项或 UNKNOWN 的终态。"
    )


class RunPairFailure(FrozenModel):
    """Typed terminal diagnostic for a pair without a complete Judge result.

    The CLI emits this after preserving all available input, adapter, and public
    runtime artifacts. It is never eligible for aggregation and never substitutes
    for a completed PairJudgeResult.
    """

    schema_version: Literal["paper1.semantic-judge.pair-failure.v1"] = Field(
        default="paper1.semantic-judge.pair-failure.v1",
        description="失败诊断持久化版本；它不是 Judge 语义结果，也不能进入指标。",
    )
    pair_id: str = Field(pattern=r"^\d{4}$", description="失败的冻结 pair ID。")
    round: int = Field(ge=1, description="失败报告所属原始轮次。")
    source_path: str = Field(
        min_length=1, description="本格实际读取的原始发布报告路径。"
    )
    input_path: str | None = Field(
        default=None,
        description="若 unified input 已成功持久化则为其路径；null 表示失败发生在输入构建前。",
    )
    adapter_audit_path: str | None = Field(
        default=None,
        description="若 adapter audit 已成功持久化则为其路径；null 表示失败发生在适配前。",
    )
    llm_artifact_path: str = Field(
        min_length=1,
        description="该 pair 的 public runtime audit 根；provider/schema 失败时用于恢复 usage/retry 证据。",
    )
    error_type: str = Field(
        min_length=1,
        description="终端异常 class 名，用于区分 provider/schema/local bug。",
    )
    error_message: str = Field(
        min_length=1, description="可定位的终端错误信息；不得吞掉 schema/runtime 原因。"
    )
    status: Literal["failed"] = Field(
        default="failed", description="本格未形成完整 Judge result，禁止聚合。"
    )
    reason: str = Field(
        min_length=1, description="为什么该格不能被视为 completed 或用于论文指标。"
    )
    basis: str = Field(
        min_length=1,
        description="输入、adapter、runtime audit 和捕获异常的持久化依据。",
    )


class RunManifest(FrozenModel):
    """Frozen provenance and input contract for one unified semantic Judge run."""

    schema_version: Literal["paper1.semantic-judge.run-manifest.v1"] = Field(
        default="paper1.semantic-judge.run-manifest.v1",
        description="统一 Judge run manifest 版本。",
    )
    run_id: str = Field(min_length=1, description="不可复用的 Judge run ID。")
    source_format: Literal["x1v2_record", "evidence_discovery_release"] = Field(
        description="本地 source adapter 类型；不进入 provider payload。"
    )
    source_root: str = Field(
        min_length=1, description="现有原始发布结果根目录；Judge 不重新生成 issue。"
    )
    source_root_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="本次实际选择源文件清单和 bytes 的 hash。",
    )
    report_root: str = Field(
        min_length=1, description="54 pair 公共 representation report 根。"
    )
    ledger_path: str = Field(min_length=1, description="冻结 145 条 ledger 真源路径。")
    ledger_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="完整 frozen ledger bytes hash。"
    )
    protocol_version: str = Field(
        min_length=1, description="冻结 issue #195 protocol version。"
    )
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="issue #195 snapshot bytes hash。"
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="统一 Judge runner version。"
    )
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="run 启动时 clean tracked git commit。"
    )
    model_profile: str = Field(
        min_length=1, description="所有 Judge reading/arbitration 统一 profile。"
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="run 前冻结的 pair selection。"
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="run 前冻结的轮次 selection。"
    )
    workers: int = Field(
        ge=1, description="pair-level 并行 worker 数；不改变单 pair Judge 语义。"
    )
    transport_retries: int = Field(
        ge=0, description="provider error 就地 retry 上限；两臂必须相同。"
    )
    reason: str = Field(
        min_length=1,
        description="本次是 baseline 重判或 current method 重判的本地 provenance；不发送给 provider。",
    )
    basis: str = Field(
        min_length=1,
        description="CLI selection、source hash、protocol/code/model version。",
    )


class RunSummary(FrozenModel):
    """Deterministically aggregatable semantic Judge run summary and completeness proof."""

    schema_version: Literal["paper1.semantic-judge.run-summary.v1"] = Field(
        default="paper1.semantic-judge.run-summary.v1",
        description="统一 Judge 汇总 schema 版本。",
    )
    run_id: str = Field(min_length=1, description="对应 RunManifest.run_id。")
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="冻结 RunManifest bytes hash。"
    )
    pair_receipts: tuple[RunPairReceipt, ...] = Field(
        description="每个 selected pair x round exactly once 的结果闭包。"
    )
    overall: SemanticMetrics = Field(
        description="所有格子的 raw reports 与 expected positions 聚合指标。"
    )
    l2_expected_count: int = Field(
        ge=0,
        description="仅用于台账侧分组的 L2 expected positions；L 不进入 provider。",
    )
    l2_full_hit_count: int = Field(
        ge=0, description="final FULL-hit L2 expected positions。"
    )
    l2_hit_rate: float = Field(
        ge=0, le=1, description="l2_full_hit_count/l2_expected_count。"
    )
    total_judge_cost_usd: float = Field(
        ge=0, description="所有 primary/arbitration Judge calls 的完整 cost；不做优化。"
    )
    cost_eligible: bool = Field(
        description="所有 call receipt 均可按 normalized usage 计费。"
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="所有选定格子完整、无 UNKNOWN/漏 report/漏 ledger 才 completed。",
    )
    reason: str = Field(
        min_length=1, description="run 完整性与主要 hit/support/K/N/I/precision 结论。"
    )
    basis: str = Field(
        min_length=1,
        description="逐条 PairJudgeResult 的确定性重算和 issue #195 公式。",
    )


class RunFailureSummary(FrozenModel):
    """Incomplete-run receipt that prevents partial pair results becoming a score."""

    schema_version: Literal["paper1.semantic-judge.run-failure.v1"] = Field(
        default="paper1.semantic-judge.run-failure.v1",
        description="不完整 run 终态版本；与 completed RunSummary 物理分离。",
    )
    run_id: str = Field(min_length=1, description="对应失败 Judge run 的不可复用 ID。")
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="冻结 RunManifest bytes hash。"
    )
    completed_pair_receipts: tuple[RunPairReceipt, ...] = Field(
        description="失败前或并发期间完整完成的 pair；仅供审计，禁止拼接汇总。"
    )
    failures: tuple[RunPairFailure, ...] = Field(
        min_length=1,
        description="每个未完成 pair 的 typed terminal diagnostic；至少一条。",
    )
    status: Literal["failed"] = Field(
        default="failed", description="选定格子未全部完成，因此没有正式指标。"
    )
    reason: str = Field(
        min_length=1, description="run 未生成 completed summary 的直接原因。"
    )
    basis: str = Field(
        min_length=1,
        description="manifest、成功 receipts、失败 artifacts 与 no-partial-summary 规则。",
    )
