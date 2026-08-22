"""v27-shaped method stages for contract extraction and complementary grounding."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..inputs.context import prompt_context_payload
from ..inputs.models import PairInput
from .adjudication import DAdjudicationResponse, SemanticAdjudication
from .obligations import (
    CandidateIssue,
    ContractBindingHint,
    EvidenceType,
    ExpectedDirection,
    MethodResponse,
    ObligationLocusKind,
    ObligationProperty,
    ViolationDirection,
)

StateSemanticRole = Literal[
    "operating_state",
    "condition_state",
    "initial_state",
    "termination_state",
    "other_state",
]

SegmentDisposition = Literal["covered", "context", "ambiguous", "unreported"]
SegmentSemanticCategory = Literal[
    "containment",
    "initial_default_entry",
    "transition_endpoint",
    "transition_group",
    "guard_relation",
    "termination",
    "event_scope",
    "action",
    "effect",
    "reachability_progress",
    "other",
]

CardinalityMemberDomain = Literal[
    "direct_child_states",
    "concurrent_regions",
    "explicit_named_members",
    "unresolved",
]


class NLTransitionAlternative(BaseModel):
    """One normative target alternative in a v27-style transition group."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.transition-alternative.v1"] = Field(default="paper1.transition-alternative.v1", description="Transition alternative 的持久化 schema 版本；不参与语义条件比较。")
    alternative_id: str = Field(pattern=r"^ALT-[A-Za-z0-9_.-]+$", min_length=5, description="Stable response-local alternative ID copied by grounding when it discusses this exact member.")
    target_name: str = Field(
        min_length=1,
        description=(
            "当前编号 NL segment 直接陈述或经真实指代消解得到的规范目标概念；该值"
            "不是 observed model endpoint。后续 segment 只能解析真正未定的 anaphora，"
            "不能用稍后具名的 completion/termination state 改写当前已明确的 local-exit "
            "role。协调 alternatives 必须逐项保留原目标；例如 `LocalExitRole` 与后续"
            "的 `NamedCompletionState` 默认是两个概念，除非 supplied NL 明确等同。"
        ),
    )
    condition: str | None = Field(default=None, min_length=1, description="Complete condition semantically attached to this target alternative, or null when the NL states an unconditional relation. Preserve a trailing condition that semantically governs a coordinated target list on every governed alternative; never distribute its conjuncts one per target unless the NL explicitly pairs them that way.")
    condition_role: Literal["event", "qualified_guard", "unknown"] | None = Field(default=None, description="Semantic role of condition: event for a stimulus/event identity, qualified_guard for an independently constraining condition, unknown only when the supplied NL cannot decide, or null when no condition is stated.")
    observed_transition_ref: str | None = Field(default=None, min_length=1, description="Exact author-source or closed-model transition ref selected during cross-view grounding, or null in an NL-only group and whenever no exact transition realizes the relation.")
    source_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact supplied NL or author-source refs supporting this alternative; do not invent refs.")
    reason: str = Field(min_length=1, description="LLM explanation of why this target and condition form one member of the shared-source transition group.")
    basis: str = Field(min_length=1, description="LLM basis naming the numbered NL clause and, during grounding, any exact transition fact used for this member.")


class NLTransitionGroup(BaseModel):
    """One v27-style semantic transition group with a shared source."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.transition-group.v1"] = Field(default="paper1.transition-group.v1", description="Transition group 的持久化 schema 版本；用于 artifact/resume 审计。")
    group_id: str = Field(pattern=r"^NL-GROUP-[A-Za-z0-9_.-]+$", min_length=10, description="Stable group ID derived from one supplied numbered segment and reused only for this exact shared-source relation.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Exact numbered NL segment containing or completing this transition relation.")
    source_name: str = Field(min_length=1, description="Normative source concept after LLM discourse/coreference resolution; never default to the enclosing model merely because a later sentence omits its source or because an earlier introductory sentence says the enclosing scope can transition among substates.")
    alternatives: tuple[NLTransitionAlternative, ...] = Field(min_length=1, description="Complete ordered target alternatives sharing source_name; do not truncate a branch set or split alternatives into unrelated groups.")
    source_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact supplied NL/source refs supporting the shared source and group boundary.")
    reason: str = Field(min_length=1, description="LLM explanation of the discourse relation that makes these alternatives share one source.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied numbered clauses used to resolve the source, ordering, and alternative membership.")

    @model_validator(mode="after")
    def validate_alternative_ids(self) -> NLTransitionGroup:
        """Require response-local exact IDs without interpreting transition prose."""

        alternative_ids = [item.alternative_id for item in self.alternatives]
        if len(alternative_ids) != len(set(alternative_ids)):
            raise ValueError("transition group alternative_id values must be unique")
        return self


class SegmentCoverage(BaseModel):
    """一个编号 NL segment 的结构化提取覆盖审计。

    contract extraction 可产生该对象，runner 对缺失 segment 做确定性补齐，grounding
    只把它作为“哪些 typed semantic units 已出现”的观察面。它不证明语义完整，不是
    candidate、W/D/L、publish 或 judge gate；covered 也不表示该段没有遗漏义务。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.segment-coverage.v1"] = Field(
        default="paper1.segment-coverage.v1",
        description="SegmentCoverage 的持久化 schema 版本；用于 artifact/resume 审计。",
    )
    segment_id: str = Field(
        pattern=r"^NL[0-9]+(?:\.[0-9]+)?$",
        description="输入闭包中的精确编号 NL segment ID；不得使用 contract 或 ledger ID 代替。",
    )
    disposition: SegmentDisposition = Field(
        description="covered 表示至少提取一个 typed unit，context 表示仅作上下文，ambiguous 表示有未闭合读法，unreported 表示 provider 未给 disposition；任何值都不阻止后续 issue。",
    )
    semantic_categories: tuple[SegmentSemanticCategory, ...] = Field(
        default_factory=tuple,
        description="该 segment 已实际形成的 typed semantic unit 类别；空集合表示未提取，不等于没有规范义务。",
    )
    contract_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="该 segment 已产出的 exact atomic contract IDs；下游据此追踪生命周期，不据此判定满足或缺陷。",
    )
    transition_group_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="该 segment 已产出的 shared-source transition group IDs；空值表示没有结构化 group。",
    )
    unresolved_readings: tuple[str, ...] = Field(
        default_factory=tuple,
        description="provider 明确指出但尚未闭合的语义读法；空值只表示未报告 unresolved reading，不证明完整。",
    )
    reason: str = Field(
        min_length=1,
        description="解释该 coverage 行为何具有当前 disposition/categories，不能声称 ledger 命中。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 supplied segment、contract/group IDs 或 provider unresolved basis。",
    )


class CardinalityRequirement(BaseModel):
    """NL 对一个有限成员域建立的规范性数量要求。

    contract extraction 产生该对象，grounding/frontier 只在 scope 与成员域获得 exact
    typed binding 后把它同完整 inventory 比较。它不包含 observed count、满足结论、
    W/D/L 或 ledger 信息；`unresolved` 明确表示 NL 尚未决定按哪类成员计数。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.cardinality-requirement.v1"] = Field(
        default="paper1.cardinality-requirement.v1",
        description="CardinalityRequirement 的持久化 schema 版本；用于 artifact、canonical identity 与 resume 审计。",
    )
    required_count: int = Field(
        ge=0,
        description="编号 NL 明确要求的成员数量；它是规范值，不是从 PlantUML/FCSTM 反推的 observed count。",
    )
    member_domain: CardinalityMemberDomain = Field(
        description=(
            "NL 要计数的 typed 成员域：direct_child_states 表示一个 composite 的直接子状态，"
            "concurrent_regions 表示显式并发 region，explicit_named_members 表示 NL 逐项点名的"
            "有限集合，unresolved 表示多种称职读法尚未闭合。不得根据元素名称含 Region/State "
            "或关键词形状选择成员域；grounding 必须用 supplied 语义与 exact inventory 绑定。"
        ),
    )
    scope_concept: str = Field(
        min_length=1,
        description="NL 中承载该数量义务的规范性 owner/scope 概念；不是 observed model ref，后续需通过 SemanticBinding 或 exact candidate refs 绑定。",
    )
    member_concept: str = Field(
        min_length=1,
        description="NL 对被计数成员的规范性称呼，例如 state areas；它保留原语义，不授权按名称后缀筛选模型元素。",
    )
    alternative_reading: str | None = Field(
        default=None,
        min_length=1,
        description="与 primary member_domain 同样称职的另一种成员域读法；null 表示 supplied NL 未建立可陈述的竞争读法，不等于 observed model 已满足。D 用它审查 D1，但它不覆盖确定性 inventory。",
    )
    reason: str = Field(
        min_length=1,
        description="解释 NL 为什么建立该 required_count/member_domain；若存在另一种称职读法，必须在此明确保留。",
    )
    basis: str = Field(
        min_length=1,
        description="指出 supplied numbered NL 中支持数量、scope 与成员域读法的精确 clause；不得引用 ledger 或 observed defect。",
    )


class NLContract(BaseModel):
    """One typed, source-grounded obligation extracted from a numbered NL segment.

    The contract describes author intent only. Its typed semantic key keeps
    later grounding focused on the same locus, property, and direction without
    deciding whether the closed FCSTM satisfies or violates the obligation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Required stable identifier derived from the supplied segment identifier; every value must start with NL-CONTRACT-, including values returned during schema correction.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Exact numbered NL segment identifier carried from the input closure.")
    quote: str = Field(min_length=1, description="Exact or faithful quote of the supplied NL segment; do not invent an answer or expected defect.")
    normative_statement: str = Field(
        min_length=1,
        description=(
            "当前 numbered NL segment 建立的原子规范义务，不判断 closed model 是否满足。"
            "必须保留本段明确的 source、target、role 和 scope；后续上下文可消解真正"
            "未定的指代，但不能把本段的 local-exit 等目标改写成后来具名的 termination "
            "target，也不能从 PlantUML/FCSTM 的 observed endpoint 反推规范目标。"
        ),
    )
    locus_kind: ObligationLocusKind = Field(
        description=(
            "Typed semantic kind of the source obligation locus. Allowed values "
            "are exactly model, state, transition, composite, region, event, "
            "action, variable, path, scenario, scope, and other. Choose the "
            "object whose property can be violated, not the property name or a "
            "nearby declared element: effect and guard are property values, not "
            "locus_kind values."
        )
    )
    locus_names: tuple[str, ...] = Field(min_length=1, description="Source-grounded names that identify the exact obligation locus before model binding; keep one independently violable semantic locus per contract.")
    property: ObligationProperty = Field(description="Atomic property required at the locus; this vocabulary includes the frozen predicate meanings and explicit unsupported semantic boundaries. A transition's source/target requirement uses transition_endpoints, while any attached event, condition, or effect is also represented by its own trigger_set, guard, or effect contract instead of being hidden inside the endpoint row. A grammatical actor such as system/controller is not automatically a transition source: after discourse establishes an enclosing operating owner, a first entry into one of that owner's substates is initial_entry with owner/target hints, not system-to-substate transition_endpoints.")
    state_role: StateSemanticRole | None = Field(
        default=None,
        description=(
            "v27 semantic role of the state centered by this contract, or null "
            "when the locus is not one state concept. An operating state denotes "
            "active behavior that must retain a response/progress interpretation. "
            "A state required as the target of an operating transition may retain "
            "an operating role, but that role alone does not invent a separate "
            "progress contract. Progress requires an explicit continuation/response "
            "obligation or a later cross-view domain obligation. "
            "termination_state requires explicit completion or terminal semantics "
            "from the NL and must never be inferred from a suggestive identifier."
        ),
    )
    expected_direction: ExpectedDirection = Field(description="Positive requirement direction stated by the NL, such as required existence, entry, reachability, progress, coverage, or absence.")
    violation_direction: ViolationDirection = Field(description="Required defect direction on every contract that grounding must look for if the requirement is not met; it must not be omitted during schema correction or reversed into a nearby existence observation.")
    evidence_types: tuple[EvidenceType, ...] = Field(
        min_length=1,
        description=(
            "Evidence families needed to assess this obligation. Allowed values "
            "are exactly source_identity, closed_model_inventory, transition_fact, "
            "initial_entry_fact, containment_fact, reachability_fact, "
            "deadlock_frontier_fact, event_consumer_fact, guard_fact, effect_fact, "
            "action_fact, trace_fact, verify_fact, smt_fact, semantic_comparison, "
            "and other. These route context but do not assert that evidence exists "
            "or proves a violation; state_action is a property name and uses "
            "action_fact as its evidence family."
        ),
    )
    binding_hints: tuple[ContractBindingHint, ...] = Field(
        default_factory=tuple,
        description=(
            "供两个 grounding lens 使用的 typed source-side argument hints；每个 hint "
            "都与 exact FCSTM binding 分离，并保留当前 segment 的规范性角色和值。一个"
            "transition-property contract 最多包含一个 source、一个 target 和一个 "
            "transition；其中 property=transition_endpoints 时必须恰有一个 source 和"
            "一个 target，不能只把二者写进 locus_names，也不能用 owner 代替 source。"
            "正例是 source=enter_hwy、target=cruise；反例是仅有 source hint。"
            "alternatives 必须拆成独立 endpoint contracts，且不得用后续 segment 或"
            "observed model endpoint 统一原本不同的 target concepts。"
        ),
    )
    cardinality_requirement: CardinalityRequirement | None = Field(
        default=None,
        description=(
            "仅供 property=cardinality 的规范性数量 payload；必须记录 NL 的 required_count、"
            "member_domain、scope/member concepts。null 精确表示该 contract 不是数量义务；"
            "cardinality contract 缺失该字段属于可确定的 schema 错误，不能解析自由文本猜数量。"
            "该字段不含 observed count，也不决定 W/D。"
        ),
    )
    scope: str = Field(min_length=1, description="Human-readable source scope, phase, owner, or boundary retained for audit alongside the typed semantic key.")
    source_refs: tuple[str, ...] = Field(default_factory=tuple, description="Source references from the supplied NL, PlantUML, or source trace; do not invent references.")
    reason: str = Field(min_length=1, description="LLM explanation of why this contract follows from the supplied NL segment.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied segment and source facts used for this contract.")

    @model_validator(mode="after")
    def validate_atomic_contract_shape(self) -> NLContract:
        """Reject structurally bundled or property/direction-incoherent rows.

        This validator inspects only typed enum values and role cardinalities.
        It deliberately does not interpret free text, names, or source wording.
        """

        role_counts = {
            role: sum(hint.role == role for hint in self.binding_hints)
            for role in {hint.role for hint in self.binding_hints}
        }
        if self.property == "cardinality" and self.cardinality_requirement is None:
            raise ValueError(
                "property='cardinality' requires cardinality_requirement with "
                "required_count, member_domain, scope_concept, member_concept, "
                "reason, and basis; do not encode the count only in free text"
            )
        if self.property != "cardinality" and self.cardinality_requirement is not None:
            raise ValueError(
                "cardinality_requirement is only valid when property='cardinality'; "
                f"actual property={self.property!r}"
            )
        transition_properties = {
            "transition_endpoints",
            "trigger_set",
            "guard",
            "effect",
        }
        if self.property in transition_properties:
            repeated_roles = {
                role: role_counts.get(role, 0)
                for role in ("source", "target", "transition")
                if role_counts.get(role, 0) > 1
            }
            if repeated_roles:
                raise ValueError(
                    "one atomic transition-property contract may contain at most "
                    "one source, one target, and one transition hint; split "
                    f"independently violable endpoints into separate contracts: {repeated_roles}"
                )
        if self.property == "transition_endpoints":
            endpoint_role_counts = {
                role: role_counts.get(role, 0) for role in ("source", "target")
            }
            if endpoint_role_counts != {"source": 1, "target": 1}:
                raise ValueError(
                    "property='transition_endpoints' requires exactly one source "
                    "hint and exactly one target hint; locus_names do not replace "
                    "typed endpoint roles and owner does not replace source; "
                    f"actual role counts={endpoint_role_counts}"
                )
        if self.property == "guard" and role_counts.get("guard", 0) > 1:
            raise ValueError(
                "one atomic guard contract may contain one normalized guard "
                "expression; preserve a conjunction in one guard hint and split "
                "alternative transition guards into separate contracts"
            )
        if self.property == "effect" and role_counts.get("effect", 0) > 1:
            raise ValueError(
                "one atomic effect contract may contain one normalized effect; "
                "split independently violable effects into separate contracts"
            )

        direction_mismatches = {
            "initial_entry": {
                "dead_end", "unreachable", "unconsumed", "wrong_guard", "wrong_effect",
            },
            "transition_endpoints": {
                "dead_end", "unreachable", "unconsumed", "wrong_guard", "wrong_effect",
            },
            "trigger_set": {
                "dead_end", "unreachable", "unconsumed", "wrong_target", "wrong_guard", "wrong_effect",
            },
            "guard": {
                "dead_end", "unreachable", "unconsumed", "wrong_target", "wrong_effect",
            },
            "effect": {
                "dead_end", "unreachable", "unconsumed", "wrong_target", "wrong_guard",
            },
            "reachability": {
                "dead_end", "unconsumed", "wrong_target", "wrong_guard", "wrong_effect",
            },
            "deadlock_freedom": {
                "unreachable", "unconsumed", "wrong_target", "wrong_guard", "wrong_effect",
            },
            "event_consumer_coverage": {
                "dead_end", "wrong_target", "wrong_guard", "wrong_effect",
            },
        }
        invalid_directions = direction_mismatches.get(self.property, set())
        if self.violation_direction in invalid_directions:
            raise ValueError(
                f"property={self.property!r} cannot use "
                f"violation_direction={self.violation_direction!r}; create a "
                "separate contract for the endpoint, reachability, progress, "
                "event-consumer, guard, or effect property actually stated"
            )
        return self


class NLContractResponse(BaseModel):
    """Structured LLM response for the v27-style NL contract extraction stage."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contracts: list[NLContract] = Field(default_factory=list, description="Complete list of independently violable atomic contracts from normative numbered NL. Preserve containment, initial/default entry, transition endpoints, explicit progress/response, termination, event-consumer scope, and other distinct properties without manufacturing progress for every mentioned operating state. When prior discourse establishes an enclosing owner and a later clause says the system/controller first enters one of that owner's substates, represent the owner-local initial_entry; the grammatical actor does not become a root-to-substate endpoint. An explicitly continuous or repeated task is an independent operating state_action obligation and must survive alongside cardinality or structure obligations from the same segment; a merely mentioned activity is not. Descriptive segments may be omitted with an explained top-level basis. Every segment marked covered must retain at least one atomic contract carrying that exact segment_id, but covered never means all other obligations in the segment may be dropped. A schema-correction turn must return a complete replacement list containing every valid contract and semantic group, not only the corrected row or a summary placeholder.")
    transition_groups: list[NLTransitionGroup] = Field(default_factory=list, description="v27-style shared-source transition relations used for discourse binding and alternative comparison. A broad capability statement without exact alternatives is context, not an element_declaration contract or permission to force later sequential clauses into one owner-sourced group. Each endpoint remains an atomic contract; when alternatives semantically require distinguishability, add a separate guard_disjointness contract rather than hiding that property inside endpoint rows.")
    segment_disposition: dict[str, Literal["covered", "context", "ambiguous"]] = Field(default_factory=dict, description="Disposition for supplied NL segment IDs only; every key must be an input segment ID. Use covered only when at least one contract in this same response carries that exact segment_id; context and ambiguous may have no contract.")
    segment_coverage: list[SegmentCoverage] = Field(default_factory=list, description="Structured per-segment completeness audit. Return one row per segment when possible, preserving unresolved readings; runner deterministically fills missing rows without treating them as semantic failures. This list is observable audit only and never gates candidate generation or publication.")
    reason: str = Field(min_length=1, description="LLM explanation of the overall contract extraction decision.")
    basis: str = Field(min_length=1, description="LLM basis identifying the supplied NL segments and source context used.")

    @model_validator(mode="after")
    def validate_structural_contract_coverage(self) -> NLContractResponse:
        """Require unique contracts and exact coverage accounting by segment ID."""

        contract_ids = [contract.contract_id for contract in self.contracts]
        if len(contract_ids) != len(set(contract_ids)):
            raise ValueError(
                "contracts must contain each contract_id at most once; return "
                "a complete replacement response with duplicate IDs removed"
            )
        contract_segment_ids = {contract.segment_id for contract in self.contracts}
        uncovered_ids = sorted(
            segment_id
            for segment_id, disposition in self.segment_disposition.items()
            if disposition == "covered" and segment_id not in contract_segment_ids
        )
        if uncovered_ids:
            raise ValueError(
                "every segment_disposition=covered ID needs at least one contract "
                "with the same segment_id; repeat the complete atomic contract "
                f"list instead of replacing prior rows with a summary: {uncovered_ids}"
            )
        group_ids = [group.group_id for group in self.transition_groups]
        if len(group_ids) != len(set(group_ids)):
            raise ValueError("transition_groups must contain unique group_id values")
        coverage_ids = [item.segment_id for item in self.segment_coverage]
        if len(coverage_ids) != len(set(coverage_ids)):
            raise ValueError(
                "segment_coverage must contain each segment_id at most once; "
                f"duplicates={sorted(segment_id for segment_id in set(coverage_ids) if coverage_ids.count(segment_id) > 1)}"
            )
        known_contract_ids = set(contract_ids)
        known_group_ids = set(group_ids)
        for index, coverage in enumerate(self.segment_coverage):
            unknown_contracts = sorted(set(coverage.contract_ids) - known_contract_ids)
            unknown_groups = sorted(
                set(coverage.transition_group_ids) - known_group_ids
            )
            if unknown_contracts or unknown_groups:
                raise ValueError(
                    f"segment_coverage[{index}] references unknown typed units; "
                    f"unknown_contract_ids={unknown_contracts}; "
                    f"unknown_transition_group_ids={unknown_groups}"
                )
        return self


class GroundingUnresolved(BaseModel):
    """One exact contract that this grounding lens could not bind or assess.

    v27 returned sparse unresolved rows rather than forcing the model to restate
    every satisfied contract. A missing row therefore makes no semantic claim;
    this object is emitted only when the branch has a concrete unresolved unit.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Exact supplied atomic contract ID reviewed by this grounding branch.")
    reason: str = Field(min_length=1, description="LLM explanation of the exact missing identity, ambiguous source meaning, unavailable deterministic fact, or other uncertainty that prevents this branch from forming a candidate.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied source or closed-model facts checked before this contract remained unresolved.")


GroundingLens = Literal["contract_structure_contrast", "behavior_consequence"]


class SemanticBinding(BaseModel):
    """grounding 对一个 contract argument 的精确跨制品语义绑定。

    两个 grounding lens 可产生该对象，runner/frontier 消费其 exact refs。它表达
    “NL/source concept 对应哪个 supplied source/model element”，不表达满足、缺陷、
    W、D、L 或 judge 关系；ambiguous/unbound 绝不能被确定性代码猜成 exact。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.semantic-binding.v1"] = Field(
        default="paper1.semantic-binding.v1",
        description="SemanticBinding 的持久化 schema 版本；用于跨 lens/artifact 审计。",
    )
    binding_id: str = Field(
        pattern=r"^BIND-[A-Za-z0-9_.-]+$",
        description="本 grounding response 内唯一的 binding ID；不是 contract、element 或 ledger ID。",
    )
    contract_id: str = Field(
        pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$",
        description="被绑定的 supplied/branch-local atomic contract ID；runner 会随 derived identity 一并 canonicalize。",
    )
    role: Literal[
        "owner",
        "scope",
        "source",
        "target",
        "transition",
        "event",
        "state",
    ] = Field(
        description="该 concept 在 atomic contract 中的 typed argument role；target 不得用 nearby owner/source 代替。",
    )
    concept_name: str = Field(
        min_length=1,
        description="NL contract 中被解释的规范概念；它用于审计，不由 deterministic 代码做字符串匹配。",
    )
    status: Literal["exact", "ambiguous", "unbound"] = Field(
        description="exact 表示 supplied facts 支持唯一 ref；ambiguous/unbound 保留不确定性且不得进入 exact frontier。",
    )
    source_element_ref: str | None = Field(
        default=None,
        min_length=1,
        description="exact canonical/source-inventory element identity，若 source 侧没有唯一对应则为 null；不是文件行号泛称。",
    )
    model_element_ref: str | None = Field(
        default=None,
        min_length=1,
        description="该规范概念对应的 exact closed ModelIR element ref；null 表示没有唯一模型绑定，不能由名称补猜。",
    )
    carrier_transition_ref: str | None = Field(
        default=None,
        min_length=1,
        description="当该 role 由一个实际 closed transition 承载或反驳时给出其 exact ref；仅声明 state/event 时为 null。",
    )
    reason: str = Field(
        min_length=1,
        description="解释 supplied NL/source/model facts 为何支持当前 binding status 和 refs。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 exact segment、contract、source inventory 和 ModelIR refs；不得引用 ledger/judge。",
    )

    @model_validator(mode="after")
    def validate_exact_ref_presence(self) -> SemanticBinding:
        """Require a reproducible ref for exact status without semantic inference."""

        if self.status == "exact" and not (
            self.source_element_ref or self.model_element_ref
        ):
            raise ValueError(
                "SemanticBinding status='exact' requires source_element_ref or "
                "model_element_ref; use ambiguous/unbound when no exact ref exists"
            )
        return self


class CardinalityDomainBinding(BaseModel):
    """grounding 对数量义务的有限成员域和 exact owner 绑定。

    grounding lens 产生该对象，deterministic frontier 消费它并从完整 source
    inventory 枚举成员。它只裁定规范概念按哪一种 typed domain 计数以及该 domain
    属于哪个 supplied owner；不携带 observed count、满足结论、candidate、W/D/L
    或 ledger 信息。存在另一种称职读法时保留在 alternative_reading，由 D 审查。
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["paper1.cardinality-domain-binding.v1"] = Field(
        default="paper1.cardinality-domain-binding.v1",
        description="CardinalityDomainBinding 的持久化 schema 版本；用于跨 lens、artifact 与 resume 审计。",
    )
    binding_id: str = Field(
        pattern=r"^CARD-BIND-[A-Za-z0-9_.-]+$",
        description="本 grounding response 内唯一的数量域绑定 ID；不是 contract、source element、model element 或 ledger ID。",
    )
    contract_id: str = Field(
        pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$",
        description="被解释的 supplied 或 branch-local cardinality contract ID；runner 会随 derived identity 精确 canonicalize。",
    )
    status: Literal["exact", "ambiguous", "unbound"] = Field(
        description=(
            "member-domain 绑定状态：exact 表示 supplied NL/source facts 支持一个 primary typed domain；"
            "ambiguous 表示多种读法并立且无法选择 primary；unbound 表示缺少所需 source identity。"
            "另一种称职读法不自动使 exact 变成 ambiguous，应写入 alternative_reading 交给 D。"
        ),
    )
    member_domain: CardinalityMemberDomain = Field(
        description=(
            "规范成员概念的 primary typed domain；exact 时必须是 direct_child_states、"
            "concurrent_regions 或 explicit_named_members，ambiguous/unbound 时必须为 unresolved。"
            "不得根据 observed count、元素名称后缀或 ledger 选择该值。"
        ),
    )
    owner_source_id: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "exact_source_inventory.states 中承载该成员域的唯一 source_id；null 表示 owner source "
            "尚未闭合。它不是 raw line ref，也不能由 deterministic frontier 做字符串相似匹配。"
        ),
    )
    owner_model_ref: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "与 owner_source_id 语义对应的 exact owned closed ModelIR state ref，必须逐字复制 "
            "closed_model_inventory.states[].ref；working-contract 中 representation 层的 model_refs "
            "只能帮助 runner 做受控映射，不能直接冒充该字段。null 表示 closed-model owner 尚未闭合。"
            "frontier 只按 exact owned ref 定位，不按名称补猜。"
        ),
    )
    alternative_reading: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "与 primary member_domain 同样称职的竞争解释；null 表示 supplied facts 未建立竞争读法，"
            "不表示 observed model 已满足。frontier 将其保留为 strongest rebuttal，供 D1/D2 裁定。"
        ),
    )
    reason: str = Field(
        min_length=1,
        description="解释 supplied NL 与 author-source semantics 为什么支持该 domain/status/owner 绑定；不得用实际计数差异倒推读法。",
    )
    basis: str = Field(
        min_length=1,
        description="列出 exact contract、numbered NL、source inventory owner/member rows 和 ModelIR owner ref；不得引用 ledger、judge 或历史命中。",
    )

    @model_validator(mode="after")
    def validate_domain_binding_shape(self) -> CardinalityDomainBinding:
        """Enforce only closed enum/ref invariants, never semantic word matching."""

        owner_refs = (self.owner_source_id, self.owner_model_ref)
        if (owner_refs[0] is None) != (owner_refs[1] is None):
            raise ValueError(
                "owner_source_id and owner_model_ref must both be present or both be null; "
                f"actual owner_source_id={self.owner_source_id!r}, owner_model_ref={self.owner_model_ref!r}"
            )
        if self.status == "exact":
            if self.member_domain == "unresolved":
                raise ValueError(
                    "status='exact' requires a concrete member_domain, not 'unresolved'"
                )
            if self.owner_source_id is None:
                raise ValueError(
                    "status='exact' requires exact owner_source_id and owner_model_ref"
                )
        elif self.member_domain != "unresolved":
            raise ValueError(
                f"status={self.status!r} requires member_domain='unresolved'; "
                f"actual member_domain={self.member_domain!r}"
            )
        return self


class GroundingResponse(BaseModel):
    """Structured LLM response for one v27 complementary discovery lens."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lens: GroundingLens = Field(description="Exact v27 audit-lens identity; both lenses receive the same cross-view context and response contract.")
    additional_contracts: list[NLContract] = Field(default_factory=list, description="Sparse v27-style atomic obligations derived by this grounding lens when exact cross-view facts reveal a causal property absent from the NL-only contract plan. Each row must retain one supplied segment_id and source obligation, use a unique NL-CONTRACT-...-DERIVED-... ID containing this response's exact lens name, and carry its own reason/basis. Do not restate supplied contracts, enumerate satisfied checks, or derive obligations from labels, identifier shape, ledger data, or historical results.")
    additional_transition_groups: list[NLTransitionGroup] = Field(default_factory=list, description="Sparse v27-style transition groups omitted by NL-only extraction and established only after cross-view semantic grounding. Do not restate supplied groups; every target member needs exact reason/basis and any observed transition ref must come from the supplied inventories.")
    semantic_bindings: list[SemanticBinding] = Field(default_factory=list, description="Sparse exact cross-artifact argument bindings needed by candidates/frontiers. Emit them for concepts whose NL name alone cannot serve as a ModelIR ref, especially wrong-target/wrong-scope relations; ambiguous or unbound concepts remain explicit and are never repaired by text similarity.")
    cardinality_bindings: list[CardinalityDomainBinding] = Field(
        default_factory=list,
        description=(
            "Sparse typed member-domain bindings for cardinality contracts. Emit one row when this lens can "
            "select or explicitly cannot select a primary domain/owner from supplied NL and exact source/model "
            "facts. This row is not a candidate and never records observed count, W, D, L, or ledger data."
        ),
    )
    candidates: list[CandidateIssue] = Field(default_factory=list, description="Candidate claims grounded across author source, closed FCSTM, and deterministic facts. Every candidate list item must independently carry all CandidateIssue fields, including its own non-empty reason and basis; a top-level or unresolved basis does not satisfy a candidate. The contract_id must name either one supplied contract or one row in additional_contracts. A branch-local ID containing this response's exact lens marker after -DERIVED- must be defined in this same response's additional_contracts list; never mint a candidate-only derived ID. Candidates must not emit W/D/L levels.")
    unresolved: list[GroundingUnresolved] = Field(default_factory=list, description="Sparse exact contract rows that this lens could not bind or assess. Omit satisfied and not-applicable contracts instead of restating the full contract table. Every unresolved row must carry its own reason and basis.")
    reason: str = Field(min_length=1, description="LLM explanation of how this audit lens selected or rejected candidate claims.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied cross-view facts and contract IDs used by this lens.")

    @model_validator(mode="after")
    def validate_sparse_contract_accounting(self) -> GroundingResponse:
        """Require unique sparse rows without making cross-stage semantic claims."""

        additional_ids = [item.contract_id for item in self.additional_contracts]
        if len(additional_ids) != len(set(additional_ids)):
            raise ValueError("additional_contracts must contain unique contract_id values")
        additional_group_ids = [item.group_id for item in self.additional_transition_groups]
        if len(additional_group_ids) != len(set(additional_group_ids)):
            raise ValueError("additional_transition_groups must contain unique group_id values")
        binding_ids = [item.binding_id for item in self.semantic_bindings]
        if len(binding_ids) != len(set(binding_ids)):
            raise ValueError("semantic_bindings must contain unique binding_id values")
        cardinality_binding_ids = [item.binding_id for item in self.cardinality_bindings]
        if len(cardinality_binding_ids) != len(set(cardinality_binding_ids)):
            raise ValueError("cardinality_bindings must contain unique binding_id values")
        cardinality_contract_ids = [
            item.contract_id for item in self.cardinality_bindings
        ]
        if len(cardinality_contract_ids) != len(set(cardinality_contract_ids)):
            raise ValueError(
                "cardinality_bindings must contain at most one primary domain row per contract_id"
            )
        unresolved_ids = [item.contract_id for item in self.unresolved]
        if len(unresolved_ids) != len(set(unresolved_ids)):
            raise ValueError("unresolved must contain each contract_id at most once")
        candidate_ids = {candidate.contract_id for candidate in self.candidates}
        overlap = sorted(candidate_ids & set(unresolved_ids))
        if overlap:
            raise ValueError(
                "a contract cannot be both a candidate and unresolved in one lens: "
                f"{overlap}"
            )
        branch_marker = f"-DERIVED-{self.lens}-"
        branch_local_references = {
            "semantic_bindings": {
                item.contract_id
                for item in self.semantic_bindings
                if branch_marker in item.contract_id
            },
            "cardinality_bindings": {
                item.contract_id
                for item in self.cardinality_bindings
                if branch_marker in item.contract_id
            },
            "candidates": {
                item.contract_id
                for item in self.candidates
                if branch_marker in item.contract_id
            },
            "unresolved": {
                item.contract_id
                for item in self.unresolved
                if branch_marker in item.contract_id
            },
        }
        dangling_references = {
            collection: sorted(contract_ids - set(additional_ids))
            for collection, contract_ids in branch_local_references.items()
            if contract_ids - set(additional_ids)
        }
        if dangling_references:
            raise ValueError(
                "branch-local contract reference closure failed for "
                f"lens={self.lens!r}; every ID containing marker "
                f"{branch_marker!r} must appear in additional_contracts; "
                f"dangling_references={dangling_references}"
            )
        return self


class ContextBudgetReceipt(BaseModel):
    """Auditable prompt-size and projection decision for one method stage."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    mode: Literal["structured_llm", "provider_free_fixture", "deterministic"] = Field(
        description="Whether this stage consumed an LLM context budget or was deterministic."
    )
    projection_version: str = Field(
        min_length=1,
        description="Versioned stage projection used before prompt serialization."
    )
    prompt_characters: int | None = Field(
        default=None,
        ge=0,
        description="Exact serialized prompt character count, or null for deterministic stages."
    )
    estimated_prompt_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Conservative pre-provider prompt token estimate, or null for deterministic stages."
    )
    provider_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Actual provider-reported input tokens across audited attempts, or null when unavailable."
    )
    context_window_tokens: int | None = Field(
        default=None,
        gt=0,
        description="Configured provider context window, or null for a provider-free/deterministic stage."
    )
    max_output_tokens: int | None = Field(
        default=None,
        gt=0,
        description="Configured maximum output tokens for the structured call, or null for deterministic stages."
    )
    truncation_applied: bool = Field(
        description="Whether runtime text truncation removed any stage input."
    )
    projection_decision: str = Field(
        min_length=1,
        description="Explicit statement of structured projection, split-stage, or no-prompt handling."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of why the recorded context budget is valid."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty prompt, usage, profile, and projection basis for the budget receipt."
    )


class StageReceipt(BaseModel):
    """Auditable receipt for one deterministic or structured method stage."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    stage_id: str = Field(min_length=1, description="Stable stage identifier within one method cell.")
    stage_name: Literal[
        "prepare",
        "contract_extraction",
        "discovery_grounding",
        "execute_batch",
        "d_adjudication",
        "validate_d",
        "publish",
    ] = Field(description="Frozen v27 stage boundary represented by this receipt; candidate compiler/backend details remain nested audit records.")
    status: Literal["completed", "completed_with_diagnostics", "failed_with_receipt"] = Field(description="Terminal stage status; failure is retained as a receipt.")
    input_manifest_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Context manifest hash supplied to this stage.")
    input_artifact_roles: tuple[str, ...] = Field(min_length=1, description="Artifact roles consumed by this stage.")
    output_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the structured stage output or deterministic receipt payload.")
    llm_call_id: str | None = Field(default=None, description="Public runtime call identity when this stage used an LLM.")
    context_budget: ContextBudgetReceipt = Field(description="Prompt size, provider token, context window, and truncation decision for this stage.")
    diagnostics: tuple[dict[str, Any], ...] = Field(default_factory=tuple, description="Structured stage diagnostics; diagnostic text is not an outcome verdict.")
    reason: str = Field(min_length=1, description="Deterministic or LLM explanation of the stage outcome.")
    basis: str = Field(min_length=1, description="Concrete input, algorithm, schema, or runtime basis for the stage outcome.")


def _hash(value: Any) -> str:
    """Hash canonical JSON for prompt and receipt identity."""

    text = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def _compact_contract_plan(contracts: NLContractResponse) -> dict[str, Any]:
    """Project contract semantics once without repeating upstream rationale.

    Complete contract and hint rationale remains in the contract stage output.
    Grounding needs the typed key, source anchor, scope, and binding values; it
    can refer to the hash when auditing the exact upstream response.
    """

    full_payload = contracts.model_dump(mode="json")
    return {
        "projection_version": "contract-grounding-projection.v2",
        "full_contract_response_hash": _hash(full_payload),
        "contract_count": len(contracts.contracts),
        "contracts": [
            {
                "contract_id": contract.contract_id,
                "segment_id": contract.segment_id,
                "quote": contract.quote,
                "normative_statement": contract.normative_statement,
                "locus_kind": contract.locus_kind,
                "locus_names": contract.locus_names,
                "property": contract.property,
                "state_role": contract.state_role,
                "expected_direction": contract.expected_direction,
                "violation_direction": contract.violation_direction,
                "evidence_types": contract.evidence_types,
                "binding_hints": [
                    {
                        "role": hint.role,
                        "value": hint.value,
                        "source_ref": hint.source_ref,
                    }
                    for hint in contract.binding_hints
                ],
                "scope": contract.scope,
                "source_refs": contract.source_refs,
            }
            for contract in contracts.contracts
        ],
        "transition_groups": [
            {
                "group_id": group.group_id,
                "segment_id": group.segment_id,
                "source_name": group.source_name,
                "alternatives": [
                    {
                        "alternative_id": alternative.alternative_id,
                        "target_name": alternative.target_name,
                        "condition": alternative.condition,
                        "condition_role": alternative.condition_role,
                        "observed_transition_ref": alternative.observed_transition_ref,
                        "source_refs": alternative.source_refs,
                    }
                    for alternative in group.alternatives
                ],
                "source_refs": group.source_refs,
            }
            for group in contracts.transition_groups
        ],
        "segment_disposition": contracts.segment_disposition,
        "reason": "Grounding receives each exact typed contract and source anchor while upstream LLM rationale remains in the hash-addressed contract stage output.",
        "basis": "contract-grounding-projection.v2 and full contract response hash",
    }


def normalize_contract_state_roles(
    response: NLContractResponse,
) -> tuple[NLContractResponse, list[dict[str, Any]]]:
    """Collapse repeated v27 operating-state role contracts by exact identity.

    v27 assigned one stable concept ID to a required state and therefore
    expanded its operating-state role once. The atomic contract surface has no
    separate concept-ID table, so this restores that behavior only for exact
    typed progress identities. It never interprets prose, spelling similarity,
    or model/ledger contents.
    """

    progress_groups: dict[tuple[Any, ...], list[NLContract]] = {}
    for contract in response.contracts:
        if (
            contract.locus_kind == "state"
            and contract.property == "deadlock_freedom"
            and contract.state_role == "operating_state"
            and contract.expected_direction == "must_progress"
            and contract.violation_direction == "dead_end"
            and len(contract.locus_names) == 1
        ):
            key = (
                contract.locus_kind,
                contract.locus_names,
                contract.property,
                contract.state_role,
                contract.expected_direction,
                contract.violation_direction,
            )
            progress_groups.setdefault(key, []).append(contract)

    duplicate_ids = {
        contract.contract_id
        for group in progress_groups.values()
        for contract in group[1:]
    }
    if not duplicate_ids:
        return response, []

    merged_by_primary_id: dict[str, NLContract] = {}
    diagnostics: list[dict[str, Any]] = []
    for key, group in progress_groups.items():
        if len(group) == 1:
            continue
        primary = group[0]
        evidence_types = tuple(
            dict.fromkeys(
                evidence_type
                for contract in group
                for evidence_type in contract.evidence_types
            )
        )
        source_refs = tuple(
            dict.fromkeys(
                source_ref
                for contract in group
                for source_ref in contract.source_refs
            )
        )
        hints_by_identity: dict[
            tuple[str, str, str | None], ContractBindingHint
        ] = {}
        for contract in group:
            for hint in contract.binding_hints:
                hints_by_identity.setdefault(
                    (hint.role, hint.value, hint.source_ref), hint
                )
        merged_ids = [contract.contract_id for contract in group[1:]]
        merged_by_primary_id[primary.contract_id] = primary.model_copy(
            update={
                "evidence_types": evidence_types,
                "binding_hints": tuple(hints_by_identity.values()),
                "source_refs": source_refs,
                "reason": (
                    primary.reason
                    + " Repeated source mentions of this exact typed operating-state role were consolidated deterministically."
                ),
                "basis": (
                    primary.basis
                    + "; exact typed state-role identity merge over contract fields"
                ),
            }
        )
        diagnostics.append(
            {
                "stage": "contract_extraction",
                "class": "exact_typed_state_role_merge",
                "kept_contract_id": primary.contract_id,
                "merged_contract_ids": merged_ids,
                "semantic_key": {
                    "locus_kind": key[0],
                    "locus_names": list(key[1]),
                    "property": key[2],
                    "state_role": key[3],
                    "expected_direction": key[4],
                    "violation_direction": key[5],
                },
                "reason": "v27 represents one required operating-state role once even when several numbered clauses support it.",
                "basis": "exact typed contract fields only; no prose, similarity, model result, ledger, or judge input",
            }
        )

    contracts = [
        merged_by_primary_id.get(contract.contract_id, contract)
        for contract in response.contracts
        if contract.contract_id not in duplicate_ids
    ]
    return (
        response.model_copy(
            update={
                "contracts": contracts,
                "reason": (
                    response.reason
                    + " Exact repeated v27 operating-state roles were consolidated without changing other obligations."
                ),
                "basis": (
                    response.basis
                    + "; exact typed state-role normalization with raw provider output retained in the LLM audit"
                ),
            }
        ),
        diagnostics,
    )


_SEGMENT_CATEGORY_BY_PROPERTY: dict[
    ObligationProperty, SegmentSemanticCategory
] = {
    "containment": "containment",
    "cardinality": "containment",
    "region_structure": "containment",
    "initial_entry": "initial_default_entry",
    "transition_endpoints": "transition_endpoint",
    "guard": "guard_relation",
    "guard_disjointness": "guard_relation",
    "guard_completeness": "guard_relation",
    "termination": "termination",
    "trigger_set": "event_scope",
    "event_consumption": "event_scope",
    "event_consumer_coverage": "event_scope",
    "state_action": "action",
    "behavior_occurrence": "action",
    "effect": "effect",
    "variable_delta": "effect",
    "reachability": "reachability_progress",
    "universal_reachability": "reachability_progress",
    "route_avoidance": "reachability_progress",
    "coaccessibility": "reachability_progress",
    "bounded_response": "reachability_progress",
    "deadlock_freedom": "reachability_progress",
}


def materialize_segment_coverage(
    response: NLContractResponse,
    supplied_segment_ids: Sequence[str],
) -> NLContractResponse:
    """Reconcile observable coverage from exact typed units without a semantic gate."""

    existing = {item.segment_id: item for item in response.segment_coverage}
    contracts_by_segment: dict[str, list[NLContract]] = {}
    groups_by_segment: dict[str, list[NLTransitionGroup]] = {}
    for contract in response.contracts:
        contracts_by_segment.setdefault(contract.segment_id, []).append(contract)
    for group in response.transition_groups:
        groups_by_segment.setdefault(group.segment_id, []).append(group)

    coverage_rows: list[SegmentCoverage] = []
    for segment_id in supplied_segment_ids:
        prior = existing.get(segment_id)
        contracts = contracts_by_segment.get(segment_id, [])
        groups = groups_by_segment.get(segment_id, [])
        categories: list[SegmentSemanticCategory] = []
        for contract in contracts:
            category = _SEGMENT_CATEGORY_BY_PROPERTY.get(contract.property, "other")
            if category not in categories:
                categories.append(category)
        if groups and "transition_group" not in categories:
            categories.append("transition_group")
        disposition: SegmentDisposition = response.segment_disposition.get(
            segment_id,
            prior.disposition if prior else "unreported",
        )
        coverage_rows.append(
            SegmentCoverage(
                segment_id=segment_id,
                disposition=disposition,
                semantic_categories=tuple(categories),
                contract_ids=tuple(item.contract_id for item in contracts),
                transition_group_ids=tuple(item.group_id for item in groups),
                unresolved_readings=prior.unresolved_readings if prior else (),
                reason=(
                    "The runner reconciled this observable coverage row from exact typed contract/group membership; it makes no claim that extraction is complete."
                ),
                basis=(
                    f"segment_id={segment_id}; contract_ids={[item.contract_id for item in contracts]}; "
                    f"transition_group_ids={[item.group_id for item in groups]}; "
                    f"provider_coverage_basis={prior.basis if prior else 'not supplied'}"
                ),
            )
        )
    return response.model_copy(update={"segment_coverage": coverage_rows})


def _context_text(pair: PairInput, *, stage: Literal["nl_contract_extraction", "discovery_grounding", "d_adjudication"]) -> str:
    """Serialize the stage-scoped closure while retaining the complete manifest."""

    if pair.context_manifest is None or pair.exact_source_inventory is None:
        raise ValueError("formal method prompt requires a complete context manifest and source inventory")
    return json.dumps(
        prompt_context_payload(pair, stage=stage),
        ensure_ascii=False,
        sort_keys=True,
    )


COMMON_RULES = """Use only the supplied input closure. Never read, infer, or reproduce frozen ledger answers, baseline hit/FP results, independent judge examples, other pair payloads, or historical release outputs. PlantUML and canonical source IR locate author intent; FCSTM is the closed model evaluated by the deterministic backend; inspection-equivalent and verify/SMT summaries are deterministic facts only. Do not treat one source role as another. Do not emit W0/W1/W2, D0/D1/D2, L, or a release decision. Predicate IDs are closed to the frozen 19 IDs. A precise claim that is not expressible by a frozen predicate must remain a candidate with predicate_id=null, not disappear. Every object and every top-level response must contain non-empty reason and basis. Explain the judgment in the requested content language; English-only output is not required. Free-text source content may be interpreted by the LLM, never by deterministic keyword, substring, regex, spelling, identifier-shape, or similarity rules."""


# These are semantic routing rules for the frozen registry, not additional
# predicates. They keep the model from encoding a known structural fact as a
# merely related existence check or silently discarding a W1-only candidate.
PREDICATE_ROUTING_GUIDANCE = """Frozen predicate routing discipline:
- Use S1 only for closed-model declaration membership (kind, element, scope). It does not prove containment, cardinality, initial-entry semantics, or a runtime state.
- Use S2 for one exact transition endpoint pair, including an initial pseudo-state endpoint when the obligation is an initial edge. Use S3 for one exact transition trigger set, S4 for one state lifecycle action, S5 for one exact transition guard, and S6 for one exact transition effect.
- Use G1 for a finite path-existence or unreachable-target claim, G2 for universal eventual target reachability, G3 only when the forbidden node/edge set is explicit, and G4 only for the registered coaccessibility form.
- Use V4(initial_scope) for a supplied finite deadlock-frontier or reachable nonterminal-no-progress fact. V4 is currently W1-only under the source audit, so preserve a precise V4 candidate and its backend result without claiming W2. Do not replace V4 with S1/S2 or call termination, liveness, fairness, or concurrency semantics deadlock evidence.
- Use V1/V2 only for the declared guard-domain formulas. Use R1-R4 only when a concrete scenario, window, and trace are supplied; do not infer trajectory facts from static text.
- Route deterministic facts by property: LEAF_WITHOUT_OUTGOING/deadlock-frontier facts may yield one V4(initial_scope) candidate with exact leaf refs as supporting binding; failed finite reachability yields G1. A refuted initial-entry fact uses S2 only when the required exact pseudo-state edge is absent. If that endpoint edge exists but is conditional or fails broader default-owner semantics, S2 cannot decide the initial-entry property; preserve a predicate=null W1 candidate unless a separate explicit guard contract supports S5. Do not turn a leaf/deadlock fact into S1 or an arbitrary present S2 edge.
- Missing containment, region/consumer scope, initial-owner existence, or variable-delta semantics may remain a precise predicate=null W1 candidate. Preserve the exact owner/event/state refs and state the unsupported boundary; do not silently drop or rename it.
- A predicate that is registered but source-gated as candidate or W1-only is still a valid precise candidate. The downstream deterministic state machine decides W1/W2; the grounding branch must not drop it merely because it cannot reach W2.
- For a missing fact, bind the expected exact model/source element and the observed absence or counterexample. For a present fact, preserve it as a non-violation observation unless the supplied dossier identifies a distinct violated obligation."""


CONTRACT_SYSTEM_PROMPT = f"""You are the NL contract extraction stage of the paper1 evidence_discovery method. {COMMON_RULES} Extract atomic source obligations before inspecting model satisfaction. For every contract, fill the typed semantic key `(locus_kind, locus_names, property, state_role, expected_direction, violation_direction, evidence_types)` and typed binding hints. Preserve v27 transition relations in `transition_groups` so shared sources, all alternatives, ordering/coreference, and condition roles remain available to grounding; endpoint, guard-disjointness, and termination properties still require their own atomic contracts. Split independently violable containment, initialization, transition endpoint, trigger, guard, effect, action, reachability, progress, event-consumer, region, variable-delta, and excess-behavior clauses instead of bundling them. Preserve qualifiers, ordering, initialization/operation/termination scope, and ambiguity. The violation direction says what later grounding must test; it does not claim that the defect exists. Keep each per-object reason and basis concise and specific; do not restate the full input context. Mark a numbered segment covered only when at least one atomic contract carries that exact segment_id, but do not treat covered as proof that every independent relation in that segment was extracted. During schema correction, return the complete prior atomic list and transition group list with only the reported structural defect repaired; never replace valid contracts with an `other` summary row or a claim that earlier obligations are preserved elsewhere.

Every `transition_endpoints` contract must carry exactly one typed `source` hint and exactly one typed `target` hint, even when the same values already appear in `locus_names`. An enclosing `owner` is scope provenance and never substitutes for the transition source. For example, an endpoint from `enter_hwy` to `cruise` carries source=`enter_hwy` and target=`cruise`; a row with only source or only owner+target is structurally incomplete and must be repaired without dropping other contracts.

Allowed `evidence_types` values are exactly: `source_identity`, `closed_model_inventory`, `transition_fact`, `initial_entry_fact`, `containment_fact`, `reachability_fact`, `deadlock_frontier_fact`, `event_consumer_fact`, `guard_fact`, `effect_fact`, `action_fact`, `trace_fact`, `verify_fact`, `smt_fact`, `semantic_comparison`, and `other`. Do not put a property name in this field: for example, `property=state_action` uses `evidence_types=[action_fact]`, never `state_action`.

Atomic contract shape:
- One contract represents one property at one independently violable locus. A transition-property row has at most one source, one target, and one transition hint.
- Alternative destinations are separate endpoint contracts. A guard conjunction for one exact transition remains one normalized guard hint; guards attached to different transitions are separate contracts.
- A transition endpoint contract contains only the required source and target relation. Preserve an event or branch-selection condition on its `transition_groups` alternative instead of duplicating every mentioned qualifier into a standalone contract. Emit a separate trigger_set or guard contract at NL extraction only when the clause states that trigger/guard as an independently violable obligation beyond selecting that alternative. Grounding must derive a sparse atomic trigger/guard contract when exact cross-view comparison later reveals a mismatch. An independently required effect or state action remains its own atomic contract because transition_groups do not carry those properties. Do not leave a normative qualifier only inside an endpoint quote, locus name, or evidence_types list.
- When one trailing phrase semantically governs a coordinated target list, preserve the complete shared condition on every governed alternative. For example, "choose A or B based on x and y" normally gives both alternatives the condition `x and y`; it does not assign x only to A and y only to B unless the NL explicitly pairs them. This is semantic parsing by the LLM, never a string rule.
- A bidirectional or dynamic A-to-B/B-to-A requirement is two endpoint contracts. Never place two source hints or two target hints in one contract.
- A conjunction such as `a and b and c` on one transition is one normalized guard hint with the complete conjunction as its value, not three guard hints. Alternative guards on different transitions remain separate contracts.
- Initialization, containment, endpoint, trigger, guard, effect, action, reachability/progress, event-consumer coverage, region structure, and variable delta never share one contract merely because the NL states them in one sentence.
- `wrong_target` belongs to `transition_endpoints`, `wrong_guard` to `guard`, `wrong_effect` to `effect` or `variable_delta`, `unreachable` to `reachability`, `dead_end` to `deadlock_freedom`, and `unconsumed` to `event_consumer_coverage`. Do not encode one property with another property's direction.
- When an event is semantically required to be accepted within a scope, emit a separate `event_consumer_coverage` contract in addition to any local endpoint/trigger contract. This is a semantic LLM judgment from the supplied NL, never a spelling or keyword rule.

v27 state-role and discourse discipline:
- Preserve the semantic role of every state-centered obligation in `state_role`. Use `operating_state` for an active control state or substate whose behavior must react, continue, or lead onward; use `termination_state` only when the NL explicitly establishes completion or intended terminal behavior. A name that sounds like stopping, emergency, final, or completion is not itself terminal evidence.
- Emit `deadlock_freedom` only when the NL explicitly requires continuation, response availability, repeated operation, or onward progress for that exact state/scope. When the NL explicitly requires an activity to be performed continuously or repeatedly, emit a separate `state_action` contract for that exact operating state/scope even if the same segment also establishes cardinality, containment, or another structural property. Merely naming an activity, entering a state, or targeting an operating state does not create a progress contract or a `state_action` contract. Cross-view grounding may later add a domain-grounded reachability/progress obligation from exact source/inspection facts; NL-only extraction must not pre-enumerate one for every state.
- When the NL explicitly says that a mode ends, completes, or terminates at a state, set that state's role to `termination_state` and emit an independent `termination` contract with `expected_direction=must_terminate` and `violation_direction=not_completed`. Do not simultaneously manufacture a progress contract for that terminal role. Grounding will assess stable termination separately from endpoint existence.
- Treat an explicit "first transitions/enters" clause as `initial_entry` into the first state under the enclosing operating owner, not as an ordinary transition from a word such as system or controller. In an initial-entry contract, `owner` is the scope that owns the required initial pseudostate edge and `target` is the state entered by that edge. Thus "the system begins in Controller" yields owner=root/system and target=Controller, while a later "within Controller, first enter ModeA" yields owner=Controller and target=ModeA. The same owner-local reading applies when one sentence first establishes "Within Controller are ModeA, ModeB, and ModeC" and the next says "the system first transitions to the ModeA substate": `system` is the grammatical actor, while the endpoint owner remains Controller; do not emit a system-to-ModeA endpoint contract for that clause. Never make the entered target its own owner merely because it is described as a composite. Resolve later omitted sources and enclosing owners by discourse semantics. A sequence such as "first enter ModeA; the system can also transition to ModeB; similarly, it can transition to ModeC" continues the operating narrative as owner-initial-to-ModeA, ModeA-to-ModeB, and ModeB-to-ModeC unless the supplied discourse explicitly resets the source or defines alternatives. By contrast, "from ModeA choose either ModeB or ModeC" yields two alternatives from ModeA. This is an LLM coreference and ordering judgment; never decide it by keywords or identifier spelling.
- Preserve every explicit parent/child relation as a separate `containment` contract. A clause that a scope transitions into, contains, or uses a named substate may establish both an endpoint/initial-entry relation and child containment; one does not replace the other. In particular, covered segment accounting never licenses omission of the containment row.
- Preserve enclosing hierarchy across numbered-segment discourse when the supplied meaning, rather than identifier spelling or model layout, keeps a transition group inside one established owner. If an earlier clause establishes source `S` as a child of owner `P` and a later group presents `A` and `B` as sibling operating alternatives inside that same continuing scope, emit separate containment contracts `S in P`, `A in P`, and `B in P` alongside the endpoint/group contracts. Do not infer this merely because `S` transitions to `A`/`B`: when the discourse leaves `P`, is ambiguous, or only states an ordinary cross-scope transition, preserve that reading instead and do not manufacture containment.
- Put every direct-transition sentence in one `transition_groups` row with its semantically resolved shared source and complete target set. Sequential discourse continues from the preceding target when the supplied meaning supports that reading; it does not mechanically inherit the enclosing composite as source. When two alternatives from the same source are intended to be distinguishable or mutually exclusive, emit a separate `guard_disjointness` contract over that group. Two individually present guards do not establish disjointness.
- Treat the current numbered segment's explicit semantic target or role as authoritative. Later segments may resolve genuine anaphora, but they must not overwrite an earlier local role that is already semantically complete. In particular, “leave/exit a mode” remains a distinct local-exit target concept unless the supplied NL explicitly equates it with a later named completion or termination state. Preserve every coordinated alternative's target exactly as stated. Do not infer normative target identity from PlantUML, FCSTM, or apparent model satisfaction during contract extraction; grounding binds the preserved concept later.
- Keep semantically distinct control effects distinct even when both eventually leave a scope. A local mode exit under one condition and a later mode/system completion under another condition are different targets unless the NL explicitly identifies them. For example, an earlier `LocalExitRole` alternative must not become `NamedCompletionState` merely because a later segment names that state as the target of a different completion condition.
- An introductory statement that an enclosing controller "can transition to different substates" establishes context but no exact source-target relation until the later discourse supplies it. Do not turn that sentence into an `element_declaration` contract, and do not use it to override the sequential source resolved from later "first", "also", or "similarly" clauses. A common enclosing owner is not itself evidence of a common transition source.
- Keep a state-owned action/effect independent from the endpoint that enters the state. The action may remain a precise unsupported W1 obligation even when the endpoint exists. Do not create standalone trigger/guard contracts that merely repeat every transition-group condition; use the group as the compact normative relation and let grounding derive only actual mismatches.
- For every `property=cardinality` contract, fill `cardinality_requirement` from the numbered NL: preserve the literal required count, the normative scope/member concepts, and a typed primary member domain. Use `direct_child_states`, `concurrent_regions`, or `explicit_named_members` when the supplied language establishes that competent reading, and preserve another competent interpretation in `alternative_reading`; use `unresolved` only when no primary member domain can be selected. Never infer the required count or domain from the observed model, element names, or a ledger.
- Preserve containment depth from the NL. A state described only as being "within" or "under" a composite requires semantic descendant containment; an intermediate region or nested composite still satisfies that obligation. Require direct/immediate ownership only when the source meaning explicitly requires no intermediate owner. Region or wrapper structure is a separate contract only when the NL independently specifies that structure or its concurrency semantics.

Generic worked example: "Within Controller, start in Idle; on Begin transition from Idle to Running when enabled and set mode=active" yields separate contracts for Controller containment of Idle, Controller initial entry to Idle, the Idle-to-Running endpoint, its Begin trigger set, its enabled guard, and its mode=active effect. If the clause also requires Begin to be accepted throughout Controller, that coverage requirement is a separate event-consumer contract. Do not copy the whole sentence into one multi-property contract.

Before returning, perform one semantic completeness pass without adding a new stage or response object: (1) every explicit child/substate relation has its containment contract even when the same clause also states entry or transition, and every semantically continuing enclosing scope preserves separate containment contracts for the complete source-and-alternative group; (2) every explicit ending/completion role has one termination contract and no manufactured progress contract; (3) every exact transition clause has its discourse-resolved source and target; (4) every coordinated alternative keeps its complete shared condition and any independent disjointness obligation; (5) every explicitly continuous or repeated task has its independent operating `state_action` contract even when that segment already has a cardinality or structure contract; and (6) broad capability context has not been converted into a synthetic element or endpoint obligation. `segment_disposition=covered` never replaces this pass.

Return only the requested Pydantic structure."""


DISCOVERY_GROUNDING_SYSTEM_PROMPT = f"""You are one complementary discovery-grounding lens of the paper1 evidence_discovery method. {COMMON_RULES} In one cross-view response, use NL contracts, PlantUML, canonical source IR, exact source inventory, working contract, and source trace to locate author-source obligations, then use FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries to bind exact closed-model elements and propose candidates. PlantUML/canonical source is author localization, FCSTM is the closed model under test, and inspection/verify/SMT rows are deterministic facts; never substitute one role for another. Do not rewrite an NL contract to match the model, claim that source presence proves execution, or treat unknown/not-run facts as violations.

Every candidate must copy one exact `contract_id` and preserve that contract's
`locus_kind`, `locus_names`, `property`, and `violation_direction`. Evaluate the
contract property first, then select the minimal frozen predicate that decides
that same property. Do not substitute a nearby endpoint, declaration, or local
path property merely because it is executable. Record the evidence families
actually used in `evidence_types`.

Before returning, close every branch-local contract reference. If this lens
derives a new property and mints an ID containing its exact name after
`-DERIVED-`, return the complete typed contract in `additional_contracts` and
make every candidate/binding/unresolved row reference that exact row. Never
return a candidate-only derived ID. Schema correction must return the complete
response with all previously valid rows retained.

Emit a candidate only for a possible violated obligation or a precisely bound
semantic gap that must remain W1. When the supplied source/model facts satisfy a
contract, omit it from both `candidates` and `unresolved`. Predicate/backend
unavailability does not turn a satisfied fact into
an issue and is not by itself semantic ambiguity.

Complete-inventory absence protocol: when the contract supplies an exact source
and target and the complete closed transition inventory contains no such edge,
that absence is the candidate evidence, not an unresolved binding. Emit one S2
candidate with the required source/target inputs and bind the exact endpoint
state refs; a nonexistent transition cannot supply its own ref. Likewise, when
one exact existing transition is bound and its parsed guard/effect/action field
is empty while an atomic contract requires that field, emit the corresponding
S4/S5/S6 candidate. Use predicate_id=null and preserve W1 only when the semantic
value cannot be represented by the frozen predicate input. Use `unresolved`
only when the required locus, endpoint identities, or source meaning itself is
not exact; never use it merely because the required model fact is absent.

Negative-property carrier example: if a contract requires `A -> B`, both A and B
resolve to exact closed-model states, and the complete transition inventory has
no A-to-B edge, emit S2 with `source=A`, `target=B`, and both endpoint state refs
in `element_refs`; do not ask a missing edge for a transition ref. If an exact
state or transition carrier lacks a required action/effect value, bind that
carrier ref and emit the issue; use predicate_id=null for W1 when the frozen
predicate cannot represent the semantic value. Missing required content is the
negative fact under review, not missing binding to its existing carrier.

Every candidate object must explicitly include `locus_kind` and `locus_names`
copied from its contract. `predicate_inputs` must always be a JSON object; use
an empty object when predicate_id is null, never a list or free-text value.
Keep author-source and closed-model namespaces separate: `element_refs` contains
only exact FCSTM/ModelIR refs, while PlantUML, canonical, source, and macro refs
belong in `source_refs`. An unmapped source identity is provenance, not evidence
that an otherwise exact FCSTM binding is missing.
Every candidate, additional contract, and unresolved row must include its own
non-empty reason and basis. These are structural output obligations, not optional prose.
Before returning, inspect every candidate list item independently: copy the full
`NL-CONTRACT-...` ID without abbreviation and include both `reason` and `basis`
on that item.

Use `semantic_bindings` when a normative concept needs an exact cross-artifact
identity that cannot be represented by copying its NL name. For example, if the
NL target concept is an exit role while source/model inventories contain a
specific exit state, bind contract role=target to that exact source element and
ModelIR state. If one actual closed transition carries the conflicting endpoint,
put its exact ref in `carrier_transition_ref`. Emit status=exact only for a unique
supplied mapping; otherwise use ambiguous/unbound. Do not infer mappings from
substring, spelling, identifier shape, majority vote, or the current model target.

Return sparse v27-style output. Do not restate satisfied or not-applicable
contracts. Use `unresolved` only for an exact contract whose semantic source,
model identity, or necessary fact cannot be bound, and give that row its own
reason and basis. A contract absent from candidates and unresolved makes no
additional claim and remains fully preserved in the contract-stage receipt.

Like v27 `additional_contracts`, this branch may add a small number of causal
atomic obligations when the cross-view closure exposes a property that the NL-only
contract extraction could not see. This does not authorize arbitrary issue
invention. Every additional contract must retain one supplied numbered NL segment,
state the requirement-side semantic implication, bind exact source/model facts,
and use a unique ID under that segment's namespace with a distinct `-DERIVED-`
marker, such as `NL-CONTRACT-<segment>-<source-contract>-DERIVED-<lens>-...`.
Include this response's exact `lens` value in every additional-contract ID so the
two complementary branches cannot assign different meanings to one ID. A candidate using it must
copy its exact typed semantic key. Typical legitimate cases are: required operating
behavior whose exact consumer transitions are unreachable because an enclosing
source composite lacks an entry; an exact required operating state that is
unreachable from root; or an unqualified event-response obligation whose exact
consumer coverage is narrower than its semantically bound scope. Do not derive
these from keywords, names, or diagnostic prose, and do not add a contract when
the existing atomic contract already states the same locus/property.
The derived contract is the candidate's actual semantic obligation: give it a new
contract ID and the actual locus/property/direction. Never attach a reachability,
termination, containment, event-consumer, or transition-group claim to a weaker
initial-entry/endpoint/declaration contract. If cross-view grounding also recovers
a missing shared-source relation, put that relation in
`additional_transition_groups`; it does not replace the independent atomic issue
contract.
For a transition-group alternative, a supplied event or qualified condition is
part of the normative relation even when NL extraction did not duplicate it as a
standalone atomic contract. When exact source/model comparison shows the selected
transition has the wrong or missing trigger/guard, derive one atomic contract for
that actual mismatch and emit its candidate. Do not first enumerate standalone
qualifier contracts for every satisfied alternative.

Cross-view frontier discipline:
- A required active control state with exact ongoing action/response semantics and
  a deterministic reachable leaf/no-outgoing fact may justify one derived
  `deadlock_freedom` contract for that state. Do not enumerate progress for every
  state merely because it is named or entered.
- A source/model composite that semantically owns required behavior but has no
  exact owner-local default entry may justify one derived `initial_entry` contract
  for that owner. Keep this separate from entry edges inside child regions.
- A required composite, operating scope, or wrapper absent from root reachability
  may justify one derived `reachability` contract for that exact scope. Local
  initial edges or local endpoint existence do not satisfy root reachability.
- When exact event-consumer facts show declared consumers but no reachable consumer
  in the semantically required scope, derive one `event_consumer_coverage`
  contract at that scope. Aggregate supporting consumer refs in basis rather than
  emitting one issue per transition.
- When several required wrappers or regions are semantically sequential/concurrent
  but the exact source/model topology isolates them, derive the narrowest global
  reachability/region contract that states that relation; local leaf facts may be
  supporting evidence but are not a substitute for the global property.
- Treat owner default entry, root reachability, and reachable event-consumer
  coverage as three independent frontier properties. Discovering a deeper root
  reachability cause does not license omission of an exact missing owner entry or
  an exact declared-but-unreachable consumer. Conversely, a local entry edge or a
  declared consumer never discharges root reachability or operational coverage.
- For every supplied `termination` contract with `state_role=termination_state`,
  audit the exact target ancestry and all target/active-ancestor continuations.
  If the designated ending target can re-enter, cycle, or route into continued
  behavior, emit one termination candidate on that exact contract even when the
  endpoint transition exists. Predicate support affects W only.
- For every transition group with multiple target alternatives, compare the exact
  selected trigger/guard relations as a group. If distinct alternatives are
  operationally indistinguishable under the same condition, emit the independent
  `guard_disjointness` candidate (V1 only when its finite domain is supplied;
  otherwise predicate=null/W1). Individual S3/S5 successes cannot rebut it.
- When an NL endpoint denotes a semantic local exit or role rather than a literal
  state spelling, use the canonical author-source inventory to bind the exact
  intended target before comparing the closed FCSTM. A present edge to another
  exact target is evidence for a wrong-target candidate, not grounds to rewrite
  the normative target or mark it unresolved.

{PREDICATE_ROUTING_GUIDANCE}

Inspection-equivalent routing: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one V4(initial_scope) candidate,
for the exact `deadlock_freedom` operating-state contract and exact state locus,
with the exact leaf refs kept in element_refs/supporting facts; it is not an S1
existence claim. A failed finite reachability fact routes to G1 with its exact
source/target sets. A refuted initial-entry fact routes to an exact S2 initial
edge claim. A refuted event-consumer coverage fact may support a precise
predicate-null W1 candidate for the exact event/consumer scope; do not replace
consumer reachability with an event or transition existence claim. An unresolved
inspection fact remains unresolved. Missing
containment, region, consumer-scope, or variable-delta semantics may remain a
precisely bound predicate=null candidate for W1, but must not be disguised as
S1/S2/S3. Keep one atomic candidate per obligation/property and place repeated
observations in reason/basis rather than emitting a separate candidate for each
supporting fact.

Preserve the contract property through causal consequences. If an exact endpoint,
trigger, guard, action, retention, or local-progress property is satisfied, an
upstream initial-entry or reachability defect does not turn that satisfied contract
into another issue. Emit the upstream defect only against its own exact
initial-entry or reachability contract. In particular, an unreachable state that
has exact outgoing continuation is not a deadlock/dead-end violation, and a
present exact endpoint does not become a wrong-target violation because its source
is unreachable. Omit the satisfied original property instead of publishing one
downstream issue per state or transition.

For event-consumer coverage, distinguish declaration from operational coverage.
An exact declared consumer with no consumer reachable in the contract's exact
operating scope violates a reachable-consumer contract; the declaration is a
supporting structural fact, not satisfaction of the stronger property. For a
finite cardinality contract, once this lens semantically binds the exact owner
and member kind, use the complete exact inventory to compare the member count.
The absence of a dedicated frozen predicate changes W to W1; it does not make
the already bound finite comparison unresolved.

Cardinality grounding protocol: do not rewrite the NL contract or encode the
domain choice only in candidate prose. Return one `cardinality_bindings` row for
each cardinality contract this lens analyzes. Select a concrete primary domain
only from the supplied NL/source semantics and bind its exact
`owner_source_id` plus `owner_model_ref`; copy `owner_model_ref` exactly from the
owned `closed_model_inventory.states[].ref`, not from a working-contract
representation mapping. Never select the binding because the resulting observed
count would pass or fail. A competing competent interpretation belongs
in `alternative_reading` and is assessed later by D; its existence does not by
itself make the primary binding ambiguous. Use `status=ambiguous` and
`member_domain=unresolved` only when the supplied semantics genuinely do not
support one primary reading. Select `concurrent_regions` when the supplied NL
semantics establishes UML regions or concurrency as the primary member concept;
do not require the author artifact to already contain a region separator or
region object, because absence of a required construct is possible negative
evidence. Conversely, do not infer concurrency from names or from an observed
count. Use `direct_child_states` when the supplied discourse maps the member
concept to directly owned child scopes, even if another competent operating-state
reading remains. The deterministic frontier, not this response, enumerates the
complete members and computes the observed count.

For a supplied transition group, compare all alternatives as one relation before
checking each endpoint in isolation. When two semantically exclusive target
alternatives from the same exact source carry the same effective condition, emit
one `guard_disjointness` candidate whose locus names the shared source and target
set. Use V1 only when its source/trigger/domain inputs and finite guard semantics
are exact; otherwise preserve the precise relation as predicate-null W1. The
existence of each endpoint or each individual guard is a weaker property and does
not satisfy group distinguishability.

For stable termination, keep endpoint existence, local outgoing behavior, and
termination as distinct properties. An explicit NL termination role plus exact
source/model facts may establish an independent `termination` candidate when the
named completion state re-enters itself, exits to another operating scope, or
cannot stably reach formal completion. A present edge into that state does not
rebut the stronger termination property, and predicate support affects only W.

Interpret containment at the depth stated by the contract. Transitive descendant
containment through a region satisfies an ordinary within-scope containment
contract; do not emit a wrong-scope issue solely because the state is not a
direct child. Direct ownership and region/concurrency structure require their own
explicit source obligations.

Audit discourse-scoped transition groups for omitted containment contracts. When
the supplied NL semantically establishes one enclosing owner and keeps the exact
group source plus every alternative target inside that owner, preserve one atomic
containment contract per member if contract extraction omitted it. This is a
semantic scope judgment from supplied NL/source context, not a rule that every
transition target shares its source's parent. If the discourse can competently
mean a cross-scope transition, keep that ambiguity instead of inventing an owner.

Compiler-owned synthetic placeholders are not author-specified operating-state
loci. A synthetic invalid or unspecified initial target may support the exact
owner's `initial_entry` defect, but its zero-outgoing fact must not become a
separate `deadlock_freedom` issue unless the source contract itself establishes
that placeholder as an operating state. For an owner-level progress contract,
evaluate the exact author-grounded operating descendants and keep the synthetic
target as supporting initial-entry evidence only.

An authored initial pseudostate edge nested in an owner must target a valid child
in that same owner scope. If the exact source inventory and deterministic facts
show a self-target, synthetic invalid target, or out-of-owner target, preserve one
`initial_entry` candidate for that malformed owner-local edge. A separate valid
root initial edge is a different fact and does not satisfy or erase the malformed
nested edge. Use only the supplied structured source/inspection facts; do not
infer malformed syntax from text matching.

For every `initial_entry` contract, treat its typed `owner` binding hint and
target as one exact scoped obligation. An initial edge owned by a nested region,
sibling composite, or root cannot satisfy an entry contract owned by another
scope merely because it reaches a target with the same name. For example, a
`Region -> ModeA` initial edge does not satisfy a `Controller -> ModeA` first-entry
contract. If the required owner-local edge is absent or selects another exact
target, emit the scoped candidate (predicate=null when the registry cannot state
the full owner semantics); do not substitute the nearby local edge.

The converse owner rule is equally strict. If the exact initial edge owned by the
contract's owner reaches the required target, omit it from the sparse response and
do not emit a candidate for it. A malformed, synthetic, missing, or differently
targeted initial edge owned by the target state or any descendant/sibling scope is
a separate obligation and cannot turn the already-satisfied owner-local contract
into a violation. In particular, a satisfied `root/system -> Controller` contract
must not be reinterpreted as a `Controller -> child` default-entry contract.

When one NL sentence contains multiple obligations, split them before rejecting
the contract. A satisfied endpoint or declaration does not discharge an attached
ordering, guard, effect, action, containment, region, consumer, or progress clause.
For every such unsatisfied or unsupported conjunct, preserve the exact model
locus and emit one atomic candidate; do not mark it satisfied or not_applicable
merely because a different conjunct is satisfied. Omit only the independently
satisfied conjunct. A missing registered predicate
is a precise W1 candidate when the model locus is exact.

Return only the requested Pydantic structure."""


DISCOVERY_GROUNDING_AUDIT_LENSES: dict[GroundingLens, str] = {
    "contract_structure_contrast": """Prioritize contract completeness, structure, and contrastive consistency. Resolve exact source and closed-model identities before emitting a candidate. Audit omitted or collapsed direct contracts, containment and owner/root default-entry defects, transition-group guard collisions, wrong local-exit targets, unauthorized edges, and cross-context inconsistencies. A source/model composite that owns required downstream behavior but lacks an exact default entry needs its own derived initial-entry candidate even when no NL sentence separately says 'initial'. An authored fact may be contrastive evidence only after the NL establishes the shared semantic role; never infer equivalence from labels, identifiers, or textual overlap.""",
    "behavior_consequence": """Prioritize behavioral consequence while still completing exact source and closed-model binding. Audit root reachability, reachable event-consumer coverage, forbidden-scope entry, dead-end/frontier facts, cross-wrapper reachability, stable termination, and bounded response or trace obligations. For every supplied termination-state contract, inspect the exact target and active-ancestor continuations; endpoint existence is not stable termination. For every required event response, inspect both declared and reachable consumer sets; declaration-only presence cannot discharge operational coverage. Preserve separate derived candidates for owner entry, root reachability, and consumer coverage when each exact property fails. Prefer one candidate per distinct property and place repeated causal facts in its basis; do not replace a distinct structural defect or promote a finite/trace result beyond its registered soundness fragment.""",
}


D_SYSTEM_PROMPT = """You are the method's semantic D adjudication stage. Use only the supplied NL contracts, author-source facts, exact bindings, predicate plan, and backend receipt. Never read or infer frozen ledger answers, baseline hit/FP results, independent judge examples, other pair payloads, or historical release outputs. Do not output D0/D1/D2, W0/W1/W2, L, a hit, or a release decision. Instead return one SemanticAdjudication per supplied obligation using only the closed grounding and defeater enums. `reason` must explain the supplied NL clause, exact source/model facts, and strongest alternative reading; `basis` must identify the supplied artifacts. Free-text wording is for audit only: do not decide from keyword, substring, regex, spelling, identifier shape, or text similarity.

D boundary: an unsupported or W1-only predicate does not erase a precise issue. When exact supplied source/model facts establish the candidate's semantic obligation, use grounding=established and describe the surviving ambiguity as a typed defeater when appropriate; deterministic code will keep it at W1. Use grounding=unresolved only when the supplied dossier genuinely cannot decide. A completed predicate result that is true for the requirement is not a violation merely because the candidate text sounds concerning.

Predicate/backend availability is a W question, never a D defeater by itself. If
the supplied exact facts satisfy the candidate's expected property, use
grounding=not_established (or a surviving rebutting defeater when a first reading
was genuinely considered), not an undercutting D1 reading. Conversely, a precise
predicate-null candidate may still be D2 when the supplied semantic facts clearly
violate the obligation; deterministic publication will keep it at W1. Do not use
backend=unsupported or verdict=unknown as evidence either for or against the
semantic violation.

Property-preserving adjudication protocol:
- A supplied fact for a weaker or different property cannot rebut the exact
  contract. A declared event consumer does not rebut a contract requiring a
  reachable consumer in an exact operating scope when the deterministic coverage
  row has no reachable consumer.
- A local initial edge does not rebut owner/composite root unreachability; an
  existing endpoint does not rebut transition-group nondeterminism; and an
  outgoing edge does not by itself rebut failed stable termination. These require
  separate candidate properties and separate obligation IDs.
- Unreachability is not itself a wrong endpoint, missing trigger, missing guard,
  missing action, failed retention, or local dead end. If those exact properties
  are positively present, use grounding=not_established for those dossiers and
  leave the upstream reachability/initial-entry defect to its own dossier.
- Once the semantic locus and member kind are exactly bound, a complete finite
  source/model inventory can establish absence or cardinality. A missing dedicated
  predicate or precomputed cardinality receipt is only a W boundary. If two
  competent scope/member readings remain compatible, use established plus an
  undercutting-survives defeater (D1), not grounding=unresolved merely because the
  frozen registry lacks that predicate.

Initial-entry scope protocol: assess each authored initial pseudostate edge in
its exact owner. A malformed nested edge whose target is self-referential,
synthetic-invalid, or outside that owner remains a source defect even when a
different root-level initial edge correctly enters the owner. The separate root
edge does not rebut the owner-local malformed-edge claim. Apply this only when
the supplied exact source inventory or deterministic diagnostic establishes the
owner and target; never infer it from names or free-text syntax.

V4 frontier protocol: when predicate_id=V4, inspect the exact bound state refs,
the finite reachability facts, the outgoing-transition facts, and the formal
terminal-edge facts supplied in the dossier. A precise reachable non-final leaf
with zero outgoing transitions establishes a candidate progress/deadlock reading
even when the NL sentence does not literally use the word deadlock. Do not infer
terminality from a state name; accept terminality only from an exact formal edge
to [*] or an explicitly supplied terminal fact. If the leaf is an exact model
element, an intentional-terminal alternative is competent only when an exact NL
terminal clause, formal terminal edge, or explicitly supplied terminal fact
supports it. Zero outgoing transitions, a suggestive state name, or the bare
possibility that a designer intended termination does not support that alternative.
Likewise, a synthetic-lowering alternative survives only when supplied exact
mapping or behavior facts establish the equivalent required behavior. If an
explicit supplied continuation/progress contract contradicts the proposed
alternative and no such exact support exists, mark the defeater `defeated`; do
not output `rebutting+survives` while the reason admits that the contract excludes
the rebuttal. Use grounding=unresolved only when the exact element,
reachability, terminality, or obligation applicability genuinely cannot be
decided from the supplied dossier. Never turn an unsupported V4 plan into W2,
and never discard a precise W1 frontier issue."""


def build_contract_prompt(
    pair: PairInput,
    round_index: int,
) -> str:
    """Build the single whole-cell v27 contract-extraction prompt."""

    if not pair.nl_segments:
        raise ValueError("contract extraction requires at least one numbered NL segment")
    context = prompt_context_payload(pair, stage="nl_contract_extraction")
    context_text = json.dumps(context, ensure_ascii=False, sort_keys=True)

    return f"""Stage: contract-extraction
Round: {round_index}
Stage-scoped context projection and complete artifact manifest:
{context_text}

Extract one NLContract per independently violable normative obligation. The typed semantic key and binding hints are the contract plan consumed by both grounding branches. Mark every supplied numbered NL segment as covered, context, or ambiguous. Every contract_id must include its exact segment_id (for example, NL-CONTRACT-NL6-ENDPOINT-1) and must be unique within this whole-cell response. Do not include ledger IDs, baseline labels, judge examples, W/D/L values, or hidden expected answers.

If Pydantic schema feedback requests a correction, return the complete replacement
NLContractResponse: preserve and repeat every already valid contract and transition
group, correct each invalid row in place, and keep every segment disposition. Never
return only the row named by the latest validation error.
"""


def build_grounding_prompt(
    pair: PairInput,
    *,
    lens: GroundingLens,
    round_index: int,
    contracts: NLContractResponse,
) -> str:
    """Build one v27 lens prompt over the shared compact cross-view closure."""

    contract_ids = [contract.contract_id for contract in contracts.contracts]

    return f"""Stage: discovery-grounding
Round: {round_index}
Complementary audit lens: {lens}
Lens priority: {DISCOVERY_GROUNDING_AUDIT_LENSES[lens]}
Frozen predicate input spellings: S1={{kind, element, scope}} S2={{source, target, scope}} S3={{transition, triggers}} S4={{state, phase, action}} S5={{transition, guard}} S6={{transition, effect}} G1={{source, target}} G2={{source, target}} G3={{source, target, forbidden}} G4={{roots, marked}} R1={{scenario, event, step}} R2={{scenario, stimulus, state, window}} R3={{scenario, behavior, window}} R4={{scenario, state, interval}} V1={{source, trigger, domain}} V2={{source, trigger, domain}} V3={{p, q, bound, unit, scope}} V4={{initial_scope}} V5={{state, expected, initial_scope}}.
If a precise candidate cannot be expressed by the registry, set predicate_id to null. Do not silently drop it. Do not use W/D/L or L levels.
Copy `contract_id`, `locus_kind`, `locus_names`, `property`, and
`violation_direction` from the one atomic contract being evaluated. A candidate
may narrow source names to exact model identities through element_refs, but it
must not change the semantic key or reverse the defect direction. Put actual
evidence families used for the comparison in `evidence_types`.
For `initial_entry`, copy and enforce the contract's exact owner hint as well as
its target; an initial edge in a different owner scope is a different fact. When
the exact owner-local edge reaches the required target, emit no candidate for
that contract. Do not use an initial edge owned by the target or one of its
descendants to manufacture a defect in the satisfied outer entry contract.
The supplied contract IDs are:
{json.dumps(contract_ids, ensure_ascii=False)}
Candidates and unresolved rows may use these IDs. A branch-local derived
candidate must instead name one exact row returned in `additional_contracts`.
Every branch-local additional contract ID must include the exact lens name
`{lens}` after its `-DERIVED-` marker; do not reuse an ID from the complementary
lens even when both lenses discover related evidence.
Before selecting `unresolved`, distinguish missing evidence identity from an
exact negative inventory result: an exact required edge absent from the complete
transition inventory is a candidate, while an ambiguous source or target is
unresolved.
For negative facts, bind the existing carrier rather than the absent content:
missing edge -> exact endpoint state refs; missing action -> exact state ref;
missing guard/effect -> exact carrier transition ref. Predicate support controls
W2 versus W1 later and never licenses silent omission.

NL contracts:
{json.dumps(_compact_contract_plan(contracts), ensure_ascii=False, sort_keys=True)}

Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="discovery_grounding")}
    """


def build_d_adjudication_prompt(pair: PairInput, dossiers: list[dict[str, Any]]) -> str:
    """Build the whole-cell semantic D prompt without exposing evaluation answers."""

    compact_dossiers = [_compact_dossier(item) for item in dossiers]

    return f"""Stage: d_adjudication
Pair identity: {pair.pair_id}
Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="d_adjudication")}

Obligation dossiers. These contain exact method outputs and backend facts, but no
W/D/L labels. Assess every obligation exactly once and preserve its obligation_id:
{json.dumps(compact_dossiers, ensure_ascii=False, sort_keys=True)}

Required obligation IDs, exactly once each:
{json.dumps([item["obligation_id"] for item in compact_dossiers], ensure_ascii=False)}

Decision protocol:
- grounding=established only when the supplied NL/source/model dossier establishes a first violated-obligation reading;
- grounding=not_established when the supplied evidence does not establish that reading;
- grounding=unresolved when the dossier cannot decide;
- use defeater_kind=none and defeater_disposition=defeated only when no competent defeater applies;
- use undercutting with survives only when two competent readings remain compatible with the supplied facts (the method maps this to D1); an unresolved undercutting reading remains D_UNRESOLVED;
- use rebutting with survives when the alternative defeats the alleged violation or leaves a reasonable design choice (the method maps this to D0); unresolved rebutting evidence remains D_UNRESOLVED;
- do not turn execution uncertainty or an absent predicate into a semantic violation;
- backend or predicate unsupported status alone is not a competent undercutting
  reading; when exact facts satisfy expected behavior, use not_established/D0;
- a proposed intentional-terminal rebuttal survives only with an exact supplied
  terminal clause, formal terminal edge, or explicit terminal fact. If a supplied
  continuation/progress contract excludes it, use `defeated`; bare design
  possibility and zero-outgoing structure do not support `rebutting+survives`;
- keep owner-local initial-edge validity separate from a different valid root
  initial edge, using only supplied typed source/diagnostic facts;
- do not omit a dossier and do not create a new obligation;
- before returning, compare the decision obligation_id set with the required list and
  return one decision for every listed ID, including unresolved decisions.
"""


def _compact_dossier(dossier: dict[str, Any]) -> dict[str, Any]:
    """Project one D dossier to semantic facts without duplicating audit bytes."""

    candidate = dossier.get("candidate", {})
    binding = dossier.get("binding", {})
    plan = dossier.get("plan", {})
    receipt = dossier.get("receipt", {})
    attribution = dossier.get("source_attribution", {})
    compact_plan = {
        key: plan[key]
        for key in (
            "plan_id",
            "predicate_id",
            "predicate_name",
            "family",
            "semantics",
            "inputs",
            "soundness_fragment",
            "assumptions",
            "supported",
            "binding_complete",
            "missing_inputs",
            "source_audit_status",
            "source_gate_passed",
            "reason",
            "basis",
        )
        if key in plan
    }
    compact_receipt = {
        key: receipt[key]
        for key in (
            "receipt_id",
            "backend",
            "terminal_state",
            "verdict",
            "counterexample",
            "trace",
            "run_metadata",
            "reason",
            "basis",
        )
        if key in receipt
    }
    compact_attribution = {
        key: attribution[key]
        for key in ("requirement", "source", "model", "plan", "backend", "input_context")
        if key in attribution
    }
    return {
        "obligation_id": dossier.get("obligation_id"),
        "candidate": {
            key: candidate[key]
            for key in (
                "contract_id",
                "locus_kind",
                "locus_names",
                "property",
                "violation_direction",
                "evidence_types",
                "title",
                "requirement_quote",
                "predicate_id",
                "predicate_inputs",
                "element_refs",
                "source_refs",
                "expected",
                "observed",
                "strongest_rebuttal",
                "reason",
                "basis",
            )
            if key in candidate
        },
        "binding": binding,
        "plan": compact_plan,
        "receipt": compact_receipt,
        "source_attribution": compact_attribution,
        "reason": "D receives the exact candidate, binding, predicate semantics, and backend result; raw audit and retry payloads remain receipt-only.",
        "basis": "dossier-prompt-projection.v2",
    }


def build_d_correction_prompt(
    pair: PairInput,
    dossiers: list[dict[str, Any]],
    *,
    missing_ids: list[str],
    duplicate_ids: list[str],
    extra_ids: list[str],
    invalid_decisions: dict[str, list[str]] | None = None,
) -> str:
    """Build the one v27 targeted repair for missing or invalid D rows."""

    invalid_decisions = invalid_decisions or {}
    repair_ids = set(missing_ids) | set(duplicate_ids) | set(invalid_decisions)
    selected = [
        dossier
        for dossier in dossiers
        if dossier["obligation_id"] in repair_ids
    ]
    return f"""{D_SYSTEM_PROMPT}

Stage: d_adjudication_correction
The previous structured response violated the exact obligation coverage contract.
This is an in-node contract correction, not a new method round. Return decisions
only for the missing IDs below, preserving their exact spelling:

missing_ids:
{json.dumps(missing_ids, ensure_ascii=False)}
invalid_decisions:
{json.dumps(invalid_decisions, ensure_ascii=False, sort_keys=True)}
duplicate_ids_to_repair:
{json.dumps(duplicate_ids, ensure_ascii=False)}
extra_ids_to_ignore:
{json.dumps(extra_ids, ensure_ascii=False)}

Correction dossiers:
{json.dumps([_compact_dossier(item) for item in selected], ensure_ascii=False, sort_keys=True, indent=2)}

Return exactly one decision per repair ID (the union of missing_ids,
duplicate_ids_to_repair, and the keys of invalid_decisions). Do not repeat any
frozen valid decision or any extra ID. If the supplied dossier cannot decide,
use grounding=unresolved with a non-empty reason and basis. Do not emit W/D/L/L
levels, ledger answers, baseline results, or judge examples.
"""


def fallback_d_adjudication(obligation_ids: list[str], reason: str) -> DAdjudicationResponse:
    """Retain every D unit after provider/schema failure without guessing semantics."""

    decisions = [
        SemanticAdjudication(
            obligation_id=obligation_id,
            grounding="unresolved",
            violated_obligation="The supplied semantic dossier could not be adjudicated.",
            strongest_defeater=None,
            defeater_kind="none",
            defeater_disposition="defeated",
            reason="The D provider/schema result was unavailable; no semantic conclusion was guessed.",
            basis=f"{reason}; D fallback preserves the obligation without text-based adjudication",
        )
        for obligation_id in obligation_ids
    ]
    return DAdjudicationResponse(
        decisions=decisions,
        reason="The D provider/schema result was unavailable; every obligation remains explicitly unresolved.",
        basis="no-silent-drop semantic D fallback",
    )


def build_method_prompt(pair: PairInput, round_index: int, previous: list[dict[str, Any]]) -> str:
    """Compatibility prompt exposing the first v27 discovery lens."""

    del previous

    empty_contracts = NLContractResponse(
        contracts=tuple(
            NLContract(
                contract_id=f"NL-CONTRACT-{segment.segment_id}",
                segment_id=segment.segment_id,
                quote=segment.text,
                normative_statement=segment.text,
                locus_kind="scope",
                locus_names=(segment.segment_id,),
                property="other",
                expected_direction="other",
                violation_direction="other",
                evidence_types=("source_identity",),
                binding_hints=(),
                scope="source-supplied scope",
                source_refs=(f"nl:{segment.segment_id}",),
                reason="The compatibility prompt preserves the numbered source segment.",
                basis="numbered NL input closure",
            )
            for segment in pair.nl_segments
        ),
        segment_disposition={segment.segment_id: "covered" for segment in pair.nl_segments},
        reason="The compatibility prompt exposes the complete v27-shaped context.",
        basis="context-manifest.v1",
    )
    return build_grounding_prompt(
        pair,
        lens="contract_structure_contrast",
        round_index=round_index,
        contracts=empty_contracts,
    )


def fallback_contracts(
    pair: PairInput,
    reason: str,
) -> NLContractResponse:
    """Create an auditable deterministic contract fallback after provider/schema failure."""

    contracts = tuple(
        NLContract(
            contract_id=f"NL-CONTRACT-{segment.segment_id}",
            segment_id=segment.segment_id,
            quote=segment.text,
            normative_statement=segment.text,
            locus_kind="scope",
            locus_names=(segment.segment_id,),
            property="other",
            expected_direction="other",
            violation_direction="other",
            evidence_types=("source_identity",),
            binding_hints=(),
            scope="source-supplied scope; semantic scope requires review",
            source_refs=(f"nl:{segment.segment_id}",),
            reason="The structured contract response was unavailable, so the exact numbered source segment was preserved.",
            basis=f"{reason}; nl-segmentation.v2",
        )
        for segment in pair.nl_segments
    )
    return NLContractResponse(
        contracts=contracts,
        segment_disposition={
            segment.segment_id: "covered"
            for segment in pair.nl_segments
        },
        reason="Provider/schema failure was downgraded to a deterministic source-contract receipt.",
        basis="exact numbered NL artifact and no-silent-drop contract",
    )


def fallback_grounding(
    pair: PairInput,
    *,
    lens: GroundingLens,
    contracts: NLContractResponse,
    reason: str,
) -> GroundingResponse:
    """Preserve a failed lens as unresolved without fabricating an issue."""

    del pair
    return GroundingResponse(
        lens=lens,
        additional_contracts=[],
        candidates=[],
        unresolved=[
            GroundingUnresolved(
                contract_id=contract.contract_id,
                reason="The lens provider/schema result was unavailable; no semantic candidate was inferred from an unrelated model fact.",
                basis=f"{reason}; exact contract ID accounting and v27 no-fabricated-fallback rule",
            )
            for contract in contracts.contracts
        ],
        reason=f"{lens} grounding is explicitly unresolved after provider/schema failure.",
        basis=f"{reason}; no semantic issue was manufactured",
    )


def assemble_method_response(
    branches: list[GroundingResponse],
    *,
    reason: str,
    basis: str,
) -> MethodResponse:
    """Merge both v27 lens candidate surfaces by exact typed identity."""

    seen: set[str] = set()
    candidates: list[CandidateIssue] = []
    for branch in branches:
        for candidate in branch.candidates:
            key = _hash(
                {
                    "contract_id": candidate.contract_id,
                    "locus_kind": candidate.locus_kind,
                    "locus_names": candidate.locus_names,
                    "property": candidate.property,
                    "violation_direction": candidate.violation_direction,
                    "predicate_id": candidate.predicate_id,
                    "predicate_inputs": candidate.predicate_inputs,
                    "element_refs": candidate.element_refs,
                }
            )
            if key in seen:
                continue
            seen.add(key)
            candidates.append(candidate)
    return MethodResponse(
        issues=candidates,
        reason=reason,
        basis=f"{basis}; exact candidate identity merge without prose similarity",
    )


__all__ = [
    "CardinalityDomainBinding",
    "CardinalityRequirement",
    "CONTRACT_SYSTEM_PROMPT",
    "DISCOVERY_GROUNDING_AUDIT_LENSES",
    "DISCOVERY_GROUNDING_SYSTEM_PROMPT",
    "D_SYSTEM_PROMPT",
    "GroundingUnresolved",
    "GroundingResponse",
    "NLContract",
    "NLContractResponse",
    "NLTransitionAlternative",
    "NLTransitionGroup",
    "SegmentCoverage",
    "SemanticBinding",
    "StageReceipt",
    "assemble_method_response",
    "build_contract_prompt",
    "build_d_adjudication_prompt",
    "build_d_correction_prompt",
    "build_grounding_prompt",
    "build_method_prompt",
    "fallback_contracts",
    "fallback_d_adjudication",
    "fallback_grounding",
    "materialize_segment_coverage",
    "normalize_contract_state_roles",
]
