"""Method stages for typed contract extraction and complementary grounding."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Callable, Mapping, Sequence
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
    """One normative target alternative in a typed transition group.

    Contract extraction produces this object and grounding/frontier consumes
    its separate event and guard projections. It expresses an NL relation, not
    an observed transition, and has no authority over satisfaction, W, D, L,
    or Judge relations. Event and guard may coexist and must not be compressed
    into one free-form condition string with a role label.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.transition-alternative.v3"] = Field(default="evidence-discovery.transition-alternative.v3", description="Persistence schema version for a transition alternative; this version keeps event and guard separate and classifies transition-causing signals as events.")
    alternative_id: str = Field(pattern=r"^ALT-[A-Za-z0-9_.-]+$", min_length=5, description="Stable response-local alternative ID copied by grounding when it discusses this exact member.")
    target_name: str = Field(
        min_length=1,
        description=(
            "Normative target concept stated directly by the current numbered "
            "NL segment or obtained through genuine anaphora resolution; this "
            "is not an observed-model endpoint. Later segments may resolve only "
            "genuinely open anaphora and may not rewrite an explicit local-exit "
            "role into a later named completion or termination state. Coordinated "
            "alternatives retain each original target; LocalExitRole and a later "
            "NamedCompletionState remain distinct unless supplied NL explicitly "
            "equates them."
        ),
    )
    event: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Stimulus or event identity established by NL for this exact "
            "alternative; null means NL establishes no independent event, not "
            "that an observed transition lacks a trigger. Event and guard may "
            "both be non-null: for example, `door is closed with zero time set` "
            "projects event=`door closed` and guard=`cooking time equals zero`, "
            "rather than labeling the whole conjunction as only an event. A "
            "named indicator, alarm, notification, or signal that causes the "
            "transition is an event/trigger unless NL separately states a data "
            "predicate that must also hold."
        ),
    )
    guard: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Normative guard or qualifier that NL independently imposes on this "
            "exact alternative; null means NL establishes no guard, not that a "
            "model guard is satisfied or absent. Preserve the complete guard "
            "conjunction. A shared guard over coordinated targets applies to "
            "every constrained alternative unless NL explicitly pairs them. A "
            "transition-causing indicator or signal is not itself a guard; use "
            "this field for an independently evaluated data condition or predicate."
        ),
    )
    observed_transition_ref: str | None = Field(default=None, min_length=1, description="Exact author-source or closed-model transition ref selected during cross-view grounding, or null in an NL-only group and whenever no exact transition realizes the relation.")
    source_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact supplied NL or author-source refs supporting this alternative; do not invent refs.")
    reason: str = Field(min_length=1, description="Explains why this target, event, and guard together form one exact member of a shared-source group; every item requires a non-empty value.")
    basis: str = Field(min_length=1, description="Cites the supplied numbered NL clause; even when grounding adds an exact transition fact, observed values must not be written back into normative fields.")


class NLTransitionGroup(BaseModel):
    """One typed semantic transition group with a shared source."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.transition-group.v2"] = Field(default="evidence-discovery.transition-group.v2", description="Persistence schema version for a transition group; v2 adds explicit common_enclosing_owner_name for artifact and resume audit.")
    group_id: str = Field(pattern=r"^NL-GROUP-[A-Za-z0-9_.-]+$", min_length=10, description="Stable group ID derived from one supplied numbered segment and reused only for this exact shared-source relation.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Exact numbered NL segment containing or completing this transition relation.")
    source_name: str = Field(min_length=1, description="Normative source concept after LLM discourse/coreference resolution; never default to the enclosing model merely because a later sentence omits its source or because an earlier introductory sentence says the enclosing scope can transition among substates.")
    common_enclosing_owner_name: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Normative owner concept when supplied NL discourse explicitly "
            "places the source and all alternatives as sibling members under "
            "one owner, such as InitialState, HighwayMode, and UrbanMode under "
            "AutonomousMode. This field preserves semantic scope provenance for "
            "group interpretation; it does not create containment contracts and is not an "
            "observed-model parent. Explicit containment obligations require their "
            "own typed contracts. It must be null when the source itself is the "
            "owner, the relation crosses scopes, only some members belong to the "
            "owner, or the reading remains ambiguous. Never infer it from names, "
            "FCSTM layout, or transition existence."
        ),
    )
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
    """Structured extraction-coverage audit for one numbered NL segment.

    Contract extraction may produce this object, and the runner deterministically
    fills missing segments. Grounding uses it only to observe which typed semantic
    units appeared. It does not prove semantic completeness and is not a candidate,
    W/D/L, publish, or Judge gate. covered does not mean the segment has no omitted
    obligations.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.segment-coverage.v1"] = Field(
        default="evidence-discovery.segment-coverage.v1",
        description="Persistence schema version for SegmentCoverage, used for artifact and resume audit.",
    )
    segment_id: str = Field(
        pattern=r"^NL[0-9]+(?:\.[0-9]+)?$",
        description="Exact numbered NL segment ID from the input closure; a contract or ledger ID may not substitute for it.",
    )
    disposition: SegmentDisposition = Field(
        description="covered means at least one typed unit was extracted, context means context-only, ambiguous means a reading remains open, and unreported means the provider supplied no disposition; no value blocks a later issue.",
    )
    semantic_categories: tuple[SegmentSemanticCategory, ...] = Field(
        default_factory=tuple,
        description="Typed semantic-unit categories actually formed for this segment; an empty tuple means none were extracted, not that no normative obligation exists.",
    )
    contract_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact atomic contract IDs produced for this segment; downstream stages track lifecycle from them but do not infer satisfaction or defect.",
    )
    transition_group_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Shared-source transition-group IDs produced for this segment; an empty tuple means no structured group was extracted.",
    )
    unresolved_readings: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Semantic readings explicitly identified but not closed by the provider; empty means no unresolved reading was reported and does not prove completeness.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why this coverage row has its disposition and categories; it may not claim a ledger hit.",
    )
    basis: str = Field(
        min_length=1,
        description="Lists the supplied segment, contract/group IDs, or provider basis for an unresolved reading.",
    )


class CardinalityRequirement(BaseModel):
    """Normative cardinality requirement that NL establishes over a finite member domain.

    Contract extraction produces this object. Grounding/frontier compares it
    with the complete inventory only after obtaining exact typed bindings for
    scope and member domain. It contains no observed count, satisfaction result,
    W/D/L, or ledger information. unresolved explicitly means NL has not fixed
    which member domain to count.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.cardinality-requirement.v1"] = Field(
        default="evidence-discovery.cardinality-requirement.v1",
        description="Persistence schema version for CardinalityRequirement, used for artifact, canonical-identity, and resume audit.",
    )
    required_count: int = Field(
        ge=0,
        description="Member count explicitly required by numbered NL; this is a normative value, not an observed count inferred from PlantUML or FCSTM.",
    )
    member_domain: CardinalityMemberDomain = Field(
        description=(
            "Typed member domain counted by NL. direct_child_states means direct "
            "child states of one composite. concurrent_regions means UML structural "
            "region partitions: explicit separators create multiple regions, while "
            "a composite with direct child states but no separator has one implicit "
            "region. explicit_named_members is a finite set enumerated by NL, and "
            "unresolved means several competent readings remain open. Select "
            "concurrent_regions only when NL explicitly establishes parallel or "
            "orthogonal regions, simultaneously active partitions, or UML region "
            "structure; the observed artifact need not already contain a separator. "
            "Generic words such as area, section, or part do not establish concurrent "
            "region semantics by themselves. Select "
            "direct_child_states only when NL directly requires a fixed number of "
            "child states or modes. Do not rebind an area/partition primary to "
            "direct_child_states because child states exist under the owner, because "
            "an observed count is closer to required_count, or because element names "
            "contain Region/State-like text."
        ),
    )
    scope_concept: str = Field(
        min_length=1,
        description="Normative owner or scope concept carrying the cardinality obligation in NL; it is not an observed-model reference and later requires SemanticBinding or exact candidate references.",
    )
    member_concept: str = Field(
        min_length=1,
        description="Normative NL term for the counted members, such as state areas; it preserves source semantics and does not authorize filtering model elements by name suffix.",
    )
    alternative_reading: str | None = Field(
        default=None,
        min_length=1,
        description="Alternative member-domain reading as competent as the primary; null means supplied NL establishes no articulable competing reading, not that the observed model is satisfied. D uses it to review D1, but it never overrides deterministic inventory.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why NL establishes this required_count and member_domain; any equally competent alternative reading must be preserved explicitly.",
    )
    basis: str = Field(
        min_length=1,
        description="Cites the exact supplied numbered-NL clause supporting count, scope, and member-domain reading; never cites a ledger item or observed defect.",
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
            "Atomic normative obligation established by the current numbered NL "
            "segment without deciding closed-model satisfaction. Preserve the "
            "segment's explicit source, target, role, and scope. Later context may "
            "resolve genuinely open references but may not rewrite a local-exit "
            "target into a later named termination target or infer a normative "
            "target backward from an observed PlantUML/FCSTM endpoint."
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
    property: ObligationProperty = Field(description="Atomic property required at the locus; this vocabulary includes the frozen predicate meanings and explicit unsupported semantic boundaries. A transition's source/target requirement uses transition_endpoints. An event or condition used only to select a transition-group alternative stays in that typed group; emit a separate trigger_set or guard contract only when the NL independently requires that exact formal property. Independently required effects/actions remain separate contracts. A grammatical actor such as system/controller is not automatically a transition source: after discourse establishes an enclosing operating owner, a first entry into one of that owner's substates is initial_entry with owner/target hints, not system-to-substate transition_endpoints.")
    state_role: StateSemanticRole | None = Field(
        default=None,
        description=(
            "Semantic role of the state centered by this contract, or null "
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
            "are exactly source_identity, closed_model_inventory, transition_fact, trigger_fact, "
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
            "Typed source-side argument hints for both grounding lenses. Every "
            "hint remains separate from exact FCSTM binding and preserves the "
            "current segment's normative role and value. A transition-property "
            "contract contains at most one source, one target, and one transition. "
            "property=transition_endpoints requires exactly one source and one "
            "target; locus_names alone is insufficient, and owner cannot substitute "
            "for source. source=enter_hwy,target=cruise is valid; a source-only hint "
            "is not. Alternatives require separate endpoint contracts, and later "
            "segments or observed endpoints may not collapse distinct target concepts."
        ),
    )
    cardinality_requirement: CardinalityRequirement | None = Field(
        default=None,
        description=(
            "Normative cardinality payload only for property=cardinality. It must "
            "record NL required_count, member_domain, and scope/member concepts. "
            "null means exactly that this contract is not a cardinality obligation. "
            "A cardinality contract without this field is a deterministic schema "
            "error; do not guess a count from free text. This field contains no "
            "observed count and decides neither W nor D."
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
    """Structured LLM response for the typed NL contract-extraction stage."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contracts: list[NLContract] = Field(default_factory=list, description="Complete list of independently violable atomic contracts from normative numbered NL. Preserve containment, initial/default entry, transition endpoints, explicit progress/response, termination, event-consumer scope, and other distinct properties without manufacturing progress for every mentioned operating state. When prior discourse establishes an enclosing owner and a later clause says the system/controller first enters one of that owner's substates, represent the owner-local initial_entry; the grammatical actor does not become a root-to-substate endpoint. An explicitly continuous or repeated task is an independent operating state_action obligation and must survive alongside cardinality or structure obligations from the same segment; a merely mentioned activity is not. Descriptive segments may be omitted with an explained top-level basis. Every segment marked covered must retain at least one atomic contract carrying that exact segment_id, but covered never means all other obligations in the segment may be dropped. A schema-correction turn must return a complete replacement list containing every valid contract and semantic group, not only the corrected row or a summary placeholder.")
    transition_groups: list[NLTransitionGroup] = Field(default_factory=list, description="Typed shared-source transition relations used for discourse binding and alternative comparison. A broad capability statement without exact alternatives is context, not an element_declaration contract or permission to force later sequential clauses into one owner-sourced group. Each endpoint remains an atomic contract; when alternatives semantically require distinguishability, add a separate guard_disjointness contract rather than hiding that property inside endpoint rows.")
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


class ContractCompletionResponse(BaseModel):
    """Typed additions emitted by one bounded contract property-coverage pass.

    The response never replaces the primary NL contract plan. It can only add
    independently violable obligations or transition groups which the current
    numbered NL establishes and the primary response omitted. The runner
    derives authoritative identities and rejects semantic duplicates before the
    additions enter grounding.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    additional_contracts: list[NLContract] = Field(
        default_factory=list,
        description=(
            "Only independently violable NL contracts absent from the supplied "
            "primary plan. Do not repeat, revise, weaken, or replace a primary "
            "contract. Each row retains the exact numbered segment, typed roles, "
            "cardinality/member information where applicable, reason, and basis."
        ),
    )
    additional_transition_groups: list[NLTransitionGroup] = Field(
        default_factory=list,
        description=(
            "Only complete typed transition groups absent from the supplied primary "
            "plan. Preserve the shared source, owner, ordered alternatives, event, "
            "guard, and source references; do not restate an existing group."
        ),
    )
    reason: str = Field(
        min_length=1,
        description=(
            "Non-empty explanation of the completeness comparison over the supplied "
            "numbered NL and primary typed plan."
        ),
    )
    basis: str = Field(
        min_length=1,
        description=(
            "Non-empty basis naming only the supplied NL, context manifest, and "
            "primary plan; never cite a ledger, Judge, score, historical report, or "
            "other pair."
        ),
    )

    @model_validator(mode="after")
    def validate_completion_ids(self) -> ContractCompletionResponse:
        """Reject only duplicate response-local IDs without interpreting prose."""

        contract_ids = [item.contract_id for item in self.additional_contracts]
        if len(contract_ids) != len(set(contract_ids)):
            raise ValueError("additional_contracts must contain unique contract_id values")
        group_ids = [item.group_id for item in self.additional_transition_groups]
        if len(group_ids) != len(set(group_ids)):
            raise ValueError(
                "additional_transition_groups must contain unique group_id values"
            )
        return self


class GroundingUnresolved(BaseModel):
    """One exact contract that this grounding lens could not bind or assess.

    The protocol uses sparse unresolved rows rather than forcing the model to restate
    every satisfied contract. A missing row therefore makes no semantic claim;
    this object is emitted only when the branch has a concrete unresolved unit.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Exact supplied atomic contract ID reviewed by this grounding branch.")
    reason: str = Field(min_length=1, description="LLM explanation of the exact missing identity, ambiguous source meaning, unavailable deterministic fact, or other uncertainty that prevents this branch from forming a candidate.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied source or closed-model facts checked before this contract remained unresolved.")


GroundingLens = Literal["contract_structure_contrast", "behavior_consequence"]


class SemanticBinding(BaseModel):
    """Exact cross-artifact semantic binding for one contract argument.

    Either grounding lens may produce this object, and runner/frontier consumes
    its exact references. It states which supplied source/model element corresponds
    to an NL/source concept. It expresses no satisfaction, defect, W, D, L, or
    Judge relation. Deterministic code must never guess ambiguous/unbound as exact.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.semantic-binding.v1"] = Field(
        default="evidence-discovery.semantic-binding.v1",
        description="Persistence schema version for SemanticBinding, used for cross-lens and cross-artifact audit.",
    )
    binding_id: str = Field(
        pattern=r"^BIND-[A-Za-z0-9_.-]+$",
        description="Binding ID unique within this grounding response; it is not a contract, element, or ledger ID.",
    )
    contract_id: str = Field(
        pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$",
        description="Supplied or branch-local atomic contract ID being bound; the runner canonicalizes it together with derived identity.",
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
        description="Typed argument role of the concept in the atomic contract; a nearby owner or source may not substitute for target.",
    )
    concept_name: str = Field(
        min_length=1,
        description="Normative concept interpreted from the NL contract; used for audit and never for deterministic string matching.",
    )
    status: Literal["exact", "ambiguous", "unbound"] = Field(
        description="exact means supplied facts support one unique reference; ambiguous and unbound preserve uncertainty and cannot enter an exact frontier.",
    )
    source_element_ref: str | None = Field(
        default=None,
        min_length=1,
        description="Exact canonical or source-inventory element identity; null when the source side has no unique match, and never a generic file-line label.",
    )
    model_element_ref: str | None = Field(
        default=None,
        min_length=1,
        description="Exact closed ModelIR element reference corresponding to the normative concept; null means no unique model binding and forbids name-based guessing.",
    )
    carrier_transition_ref: str | None = Field(
        default=None,
        min_length=1,
        description="Exact reference when an actual closed transition carries or rebuts this role; null when only a state or event declaration is involved.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why supplied NL, source, and model facts support the current binding status and references.",
    )
    basis: str = Field(
        min_length=1,
        description="Lists exact segment, contract, source-inventory, and ModelIR references; never cites ledger or Judge data.",
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
    """Finite member-domain and exact-owner binding for a cardinality obligation.

    A grounding lens produces this object. The deterministic frontier consumes
    it and enumerates members from the complete source inventory. It decides only
    which typed domain counts the normative concept and which supplied owner owns
    that domain. It carries no observed count, satisfaction result, candidate,
    W/D/L, or ledger data. Any equally competent reading remains in
    alternative_reading for D review.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.cardinality-domain-binding.v1"] = Field(
        default="evidence-discovery.cardinality-domain-binding.v1",
        description="Persistence schema version for CardinalityDomainBinding, used for cross-lens, artifact, and resume audit.",
    )
    binding_id: str = Field(
        pattern=r"^CARD-BIND-[A-Za-z0-9_.-]+$",
        description="Cardinality-domain binding ID unique within this grounding response; it is not a contract, source-element, model-element, or ledger ID.",
    )
    contract_id: str = Field(
        pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$",
        description="Supplied or branch-local cardinality contract ID being interpreted; the runner canonicalizes it exactly with derived identity.",
    )
    status: Literal["exact", "ambiguous", "unbound"] = Field(
        description=(
            "Member-domain binding status: exact means supplied NL/source facts "
            "support one primary typed domain; ambiguous means multiple readings "
            "remain and no primary can be selected; unbound means the required "
            "source identity is missing. Another competent reading does not "
            "automatically turn exact into ambiguous; record it in "
            "alternative_reading for D."
        ),
    )
    member_domain: CardinalityMemberDomain = Field(
        description=(
            "Primary typed domain of the normative member concept. exact requires "
            "direct_child_states, concurrent_regions, or explicit_named_members; "
            "ambiguous/unbound requires unresolved. Use concurrent_regions only when "
            "the obligation explicitly describes parallel or orthogonal regions, "
            "simultaneously active partitions, or UML region structure, even when "
            "the observed source has no separator. A non-empty "
            "composite without a separator has one implicit region. Direct-child "
            "operating phases/states may remain an alternative_reading but cannot "
            "replace an explicitly established primary. Use direct_child_states only when "
            "normative text directly counts a composite's child states or modes. "
            "Never choose from observed count, element-name suffix, or ledger data."
        ),
    )
    owner_source_id: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Unique source_id in exact_source_inventory.states that owns this "
            "member domain; null means the owner source is not closed. The owner "
            "must realize the cardinality contract's normative scope_concept and "
            "owner/scope binding hint. Do not descend to a deeper child composite "
            "merely because an activity occurs there. Both lenses must choose from "
            "the same contract-level scope: if a contract counts regions of "
            "Controller operation while an action executes in TaskRegion, the "
            "owner remains Controller unless supplied NL/source semantics equates "
            "the counted scope with TaskRegion. This is not a raw line reference "
            "and deterministic frontier may not use string similarity."
        ),
    )
    owner_model_ref: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Exact owned closed-ModelIR state reference semantically corresponding "
            "to owner_source_id, copied exactly from "
            "closed_model_inventory.states[].ref. Representation-layer model_refs "
            "in the working contract may assist controlled runner mapping but may "
            "not substitute for this field. null means the closed-model owner is "
            "not closed. Frontier localizes only by exact owned reference, never by name."
        ),
    )
    alternative_reading: str | None = Field(
        default=None,
        min_length=1,
        description=(
            "Competing interpretation as competent as the primary member_domain; "
            "null means supplied facts establish no competing reading, not that "
            "the observed model is satisfied. Frontier preserves it as the "
            "strongest rebuttal for D1/D2 adjudication."
        ),
    )
    reason: str = Field(
        min_length=1,
        description="Explains why supplied NL and author-source semantics support this domain/status/owner binding; never infer the reading backward from an observed count difference.",
    )
    basis: str = Field(
        min_length=1,
        description="Lists the exact contract, numbered NL, source-inventory owner/member rows, and ModelIR owner reference; never cites ledger, Judge, or historical hits.",
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
    """Structured LLM response for one complementary discovery lens.

    Additional-contract IDs are response-local references only. The runner
    derives their persistent identities from typed semantic payloads before
    cross-lens merge; provider spelling never has semantic authority.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lens: GroundingLens = Field(description="Exact audit-lens identity; both lenses receive the same cross-view context and response contract.")
    additional_contracts: list[NLContract] = Field(default_factory=list, description="Sparse atomic obligations derived by this grounding lens when exact cross-view facts reveal a causal property absent from the NL-only contract plan. Each row must retain one supplied segment_id and source obligation, use a response-local NL-CONTRACT-...-DERIVED-... reference, and carry its own reason/basis plus complete binding_hints reason/basis. The local string only joins rows inside this response; the runner computes the persistent canonical ID from the typed semantic payload. Do not restate supplied contracts, enumerate satisfied checks, or derive obligations from labels, identifier shape, ledger data, or historical results.")
    additional_transition_groups: list[NLTransitionGroup] = Field(default_factory=list, description="Sparse transition groups omitted by NL-only extraction and established only after cross-view semantic grounding. Do not restate supplied groups; every target member needs exact reason/basis and any observed transition ref must come from the supplied inventories.")
    semantic_bindings: list[SemanticBinding] = Field(default_factory=list, description="Sparse exact cross-artifact argument bindings needed by candidates/frontiers. Every contract_id must name either one supplied contract or one additional_contracts row in this same response; never invent a placeholder ID for an unextracted obligation. Emit bindings for concepts whose NL name alone cannot serve as a ModelIR ref, especially wrong-target/wrong-scope relations; ambiguous or unbound concepts remain explicit and are never repaired by text similarity.")
    cardinality_bindings: list[CardinalityDomainBinding] = Field(
        default_factory=list,
        description=(
            "Typed member-domain accounting for cardinality contracts. Unlike other sparse grounding rows, "
            "every supplied property=cardinality contract must have exactly one row in each lens: use exact "
            "when one primary domain and owner close, ambiguous when competent domains cannot be ordered, or "
            "unbound when exact owner identity is unavailable. Every additional property=cardinality contract "
            "in this response also needs one row. Every contract_id must name either one supplied contract or "
            "one additional_contracts row in this same response; non-cardinality contracts are invalid targets. "
            "Schema correction returns a complete replacement preserving all valid rows. This row is not a "
            "candidate and never records observed count, W, D, L, or ledger data. For a supplied cardinality "
            "contract, emit this binding row only; deterministic frontier computes the complete count after both "
            "lenses, so neither lens may emit its own cardinality CandidateIssue from a primary or alternative reading."
        ),
    )
    candidates: list[CandidateIssue] = Field(default_factory=list, description="Candidate claims grounded across author source, closed FCSTM, and deterministic facts. Every list item must independently include requirement_quote, reason, basis, locus_kind, locus_names, property, violation_direction, evidence_types, expected, observed, and strongest_rebuttal; no top-level field substitutes for an item field. contract_id names either one supplied contract or one response-local additional_contracts row. The runner canonicalizes derived identity from the unique typed payload and records any exact reference recovery. Candidates must not emit W/D/L levels.")
    unresolved: list[GroundingUnresolved] = Field(default_factory=list, description="Sparse exact contract rows that this lens could not bind or assess. contract_id must name either one supplied contract or one additional_contracts row in this same response. If no such contract exists, omit the row; never invent an *-UNDECLARED, *-UNKNOWN, or other placeholder ID merely to say that no unresolved row is needed. Omit satisfied and not-applicable contracts instead of restating the full contract table. Every unresolved row must carry its own reason and basis.")
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
        "contract_completion",
        "discovery_grounding",
        "execute_batch",
        "d_adjudication",
        "validate_d",
        "publish",
    ] = Field(description="Frozen method-stage boundary represented by this receipt; candidate compiler/backend details remain nested audit records.")
    status: Literal["completed", "completed_with_diagnostics", "failed_with_receipt"] = Field(description="Terminal stage status; failure is retained as a receipt.")
    input_manifest_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Context manifest hash supplied to this stage.")
    input_artifact_roles: tuple[str, ...] = Field(min_length=1, description="Artifact roles consumed by this stage.")
    output_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the structured stage output or deterministic receipt payload.")
    llm_call_id: str | None = Field(default=None, description="Public runtime call identity when this stage used an LLM.")
    context_budget: ContextBudgetReceipt = Field(description="Prompt size, provider token, context window, and truncation decision for this stage.")
    diagnostics: tuple[dict[str, Any], ...] = Field(default_factory=tuple, description="Structured stage diagnostics; diagnostic text is not an outcome verdict.")
    reason: str = Field(min_length=1, description="Deterministic or LLM explanation of the stage outcome.")
    basis: str = Field(min_length=1, description="Concrete input, algorithm, schema, or runtime basis for the stage outcome.")


class DAdjudicationPromptBatch(BaseModel):
    """One stable, complete-dossier D prompt bounded before provider execution."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    kind: Literal["initial", "correction"] = Field(
        description="Whether this batch performs initial D adjudication or targeted contract correction."
    )
    batch_index: int = Field(
        ge=1,
        description="One-based stable batch position after sorting exact obligation IDs.",
    )
    obligation_ids: tuple[str, ...] = Field(
        min_length=1,
        description="Exact obligation IDs included once in this prompt, in stable lexical order.",
    )
    prompt: str = Field(
        min_length=1,
        description="Complete serialized D prompt for these obligation dossiers without dossier truncation.",
    )
    prompt_characters: int = Field(
        ge=1,
        description="Exact character count of the serialized prompt supplied to the runtime.",
    )
    character_budget: int = Field(
        ge=1,
        description="Pre-provider character budget used to form this stable batch.",
    )
    exceeds_budget: bool = Field(
        description="Whether one indivisible dossier alone exceeds the configured prompt budget."
    )
    reason: str = Field(
        min_length=1,
        description="Why these obligations form one complete and deterministic prompt batch.",
    )
    basis: str = Field(
        min_length=1,
        description="Exact ordering, projection, and serialized-size basis for this batch.",
    )


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
                "common_enclosing_owner_name": group.common_enclosing_owner_name,
                "alternatives": [
                    {
                        "alternative_id": alternative.alternative_id,
                        "target_name": alternative.target_name,
                        "event": alternative.event,
                        "guard": alternative.guard,
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
    """Collapse repeated operating-state role contracts by exact identity.

    The protocol assigns one stable concept ID to a required state and therefore
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
                "reason": "One required operating-state role is represented once even when several numbered clauses support it.",
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
                    + " Exact repeated operating-state roles were consolidated without changing other obligations."
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


COMMON_RULES = """Use only the supplied input closure. Never read, infer, or reproduce evaluation ground truth, scores, reviewer examples, artifacts from other evaluation cases, or previously generated reports. PlantUML and canonical source IR locate author intent; FCSTM is the closed model evaluated by the deterministic backend; inspection-equivalent and verify/SMT summaries are deterministic facts only. Do not treat one source role as another. Do not emit W0/W1/W2, D0/D1/D2, L, or a release decision. Predicate IDs are closed to the selected 12 IDs. A precise claim that is not expressible by a frozen predicate must remain a candidate with predicate_id=null, not disappear. Every object and every top-level response must contain non-empty reason and basis. Write every generated title, statement, summary, reason, basis, unresolved reading, and audit explanation in English. Preserve non-English text only inside exact quotations or identifiers copied from supplied artifacts, and explain each quotation in English. Free-text source content may be interpreted by the LLM, never by deterministic keyword, substring, regex, spelling, identifier-shape, or similarity rules."""


# These are semantic routing rules for the frozen registry, not additional
# predicates. They keep the model from encoding a known structural fact as a
# merely related existence check or silently discarding a precise unexecuted
# candidate.
PREDICATE_ROUTING_GUIDANCE = """Frozen predicate routing discipline:
- Use S1 only for closed-model declaration membership (kind, element, scope). It does not prove containment, cardinality, initial-entry semantics, or a runtime state.
- Use S2 for one exact transition endpoint pair, including an initial pseudo-state endpoint when the obligation is an initial edge. Use S3 for one exact transition trigger set, S4 for one state lifecycle action, and S5 for one exact transition guard. Preserve transition-effect claims as predicate-null W1 candidates. A `state_action` is executable as S4 only when the NL itself supplies all three separate hints: exact `state`, one lifecycle `phase` exactly equal to `entry`, `do`, or `exit`, and exact `action`. For example, `Entry/Accelerate` on entry to `Accelerating` produces phase=`entry` and action=`Accelerate`. A state name, operating/business phase, event name, or generic wording such as "includes actions" is not an S4 phase; keep the precise state_action contract but omit phase rather than inventing one.
- Use G1 for a finite path-existence or unreachable-target claim, G2 for target reachability on every admissible execution within its declared bound, and G3 for the registered root-to-marked coaccessibility form. Preserve route-avoidance claims as predicate-null W1 candidates.
- Use V1(initial_scope) for a supplied finite deadlock-frontier or reachable nonterminal-no-progress fact. Do not replace V1 with S1/S2 or call termination, liveness, fairness, or concurrency semantics deadlock evidence.
- Extract `event_consumption` and `state_retention` contracts whenever the supplied NL states one exact event-consumer or state-retention obligation, even though the NL does not itself contain an executable trace. Do not invent a scenario, queue, schedule, macrostep, interval, guard valuation, or verdict: the downstream native binder alone may materialize such an input after exact current-pair closure. If that closure fails, retain the precise candidate as W1.
- Preserve guard-disjointness, guard-completeness, behavior-occurrence, bounded-response, and state-invariant claims as predicate-null W1 candidates when they describe a precise possible violation. Do not substitute a related predicate that checks a different property.
- Route deterministic facts by property: LEAF_WITHOUT_OUTGOING/deadlock-frontier facts may yield one V1(initial_scope) candidate with exact leaf refs as supporting binding; failed finite reachability yields G1. A refuted initial-entry fact uses S2 only when the required exact pseudo-state edge is absent. If that endpoint edge exists but is conditional or fails broader default-owner semantics, S2 cannot decide the initial-entry property; preserve a predicate=null W1 candidate unless a separate explicit guard contract supports S5. Do not turn a leaf/deadlock fact into S1 or an arbitrary present S2 edge.
- Missing containment, region/consumer scope, initial-owner existence, or variable-delta semantics may remain a precise predicate=null W1 candidate. Preserve the exact owner/event/state refs and state the unsupported boundary; do not silently drop or rename it.
- Every frozen predicate has scholarly eligibility. The downstream deterministic state machine decides W1/W2 from exact typed binding, executable fragment, artifact attribution, and the actual receipt; grounding must never use bibliography metadata as a routing condition.
- For a missing fact, bind the expected exact model/source element and the observed absence or counterexample. For a present fact, preserve it as a non-violation observation unless the supplied dossier identifies a distinct violated obligation."""


CONTRACT_SYSTEM_PROMPT = f"""You are the NL contract-extraction stage of an evidence-discovery method. {COMMON_RULES} Extract atomic source obligations before inspecting model satisfaction. For every contract, fill the typed semantic key `(locus_kind, locus_names, property, state_role, expected_direction, violation_direction, evidence_types)` and typed binding hints. Preserve typed transition relations in `transition_groups` so shared sources, all alternatives, ordering/coreference, and condition roles remain available to grounding; endpoint, guard-disjointness, and termination properties still require their own atomic contracts. Split independently violable containment, initialization, transition endpoint, trigger, guard, effect, action, reachability, progress, event-consumer, region, variable-delta, and excess-behavior clauses instead of bundling them. Preserve qualifiers, ordering, initialization/operation/termination scope, and ambiguity. The violation direction says what later grounding must test; it does not claim that the defect exists. Keep each per-object reason and basis concise and specific; do not restate the full input context. Mark a numbered segment covered only when at least one atomic contract carries that exact segment_id, but do not treat covered as proof that every independent relation in that segment was extracted. During schema correction, return the complete prior atomic list and transition group list with only the reported structural defect repaired; never replace valid contracts with an `other` summary row or a claim that earlier obligations are preserved elsewhere.

Extract `event_consumption` and `state_retention` contracts when supplied NL establishes the exact semantic obligation, even when it does not provide an executable scenario, trace, or interval. Do not invent any scenario, queue, schedule, macrostep, interval, guard valuation, finite domain, or verdict: a downstream native binder may only construct those execution inputs after exact current-pair closure, and an unclosed input remains a precise W1 boundary.

Extract `guard_disjointness` only when supplied NL requires distinguishable or mutually exclusive alternatives. Preserve an independently declared finite domain only when the NL actually declares it; do not synthesize that domain from guards, observed values, fixtures, or evaluation data.

Every `transition_endpoints` contract must carry exactly one typed `source` hint and exactly one typed `target` hint, even when the same values already appear in `locus_names`. An enclosing `owner` is scope provenance and never substitutes for the transition source. For example, an endpoint from `enter_hwy` to `cruise` carries source=`enter_hwy` and target=`cruise`; when `OperatingMode` completes by transitioning to `FinishState`, use source=`OperatingMode` and target=`FinishState`, not owner=`OperatingMode` plus target. A row with only source or only owner+target is structurally incomplete and must be repaired without dropping other contracts.

Allowed `evidence_types` values are exactly: `source_identity`, `closed_model_inventory`, `transition_fact`, `trigger_fact`, `initial_entry_fact`, `containment_fact`, `reachability_fact`, `deadlock_frontier_fact`, `event_consumer_fact`, `guard_fact`, `effect_fact`, `action_fact`, `trace_fact`, `verify_fact`, `smt_fact`, `semantic_comparison`, and `other`. Use `trigger_fact` for an exact transition trigger observation and `guard_fact` only for a guard/condition fact; neither value is a property or frozen predicate ID. Do not put a property name in this field: for example, `property=state_action` uses `evidence_types=[action_fact]`, never `state_action`.

Atomic contract shape:
- One contract represents one property at one independently violable locus. A transition-property row has at most one source, one target, and one transition hint.
- Alternative destinations are separate endpoint contracts. A guard conjunction for one exact transition remains one normalized guard hint; guards attached to different transitions are separate contracts.
- A transition endpoint contract contains only the required source and target relation. Preserve an event or branch-selection condition on its `transition_groups` alternative instead of duplicating every mentioned qualifier into a standalone contract. Words such as "when", "if", or "based on" normally attach the condition to that alternative and do not by themselves establish a separate formal guard obligation. Emit a separate trigger_set or guard contract at NL extraction only when the clause independently requires that exact trigger/guard property beyond selecting the alternative. Grounding must derive a sparse atomic trigger/guard contract when exact cross-view comparison later reveals a mismatch. An independently required effect or state action remains its own atomic contract because transition_groups do not carry those properties. Do not leave a normative qualifier only inside an endpoint quote, locus name, or evidence_types list.
- Project each transition-group alternative into independent `event` and `guard` fields. Both may be non-null: "on Door Closed when cooking time is zero" has event=`Door Closed` and guard=`cooking time is zero`; neither field may swallow the other. When one trailing qualifier semantically governs a coordinated target list, preserve the complete shared guard on every governed alternative. For example, "choose A or B based on x and y" normally gives both alternatives guard=`x and y`; it does not assign x only to A and y only to B unless the NL explicitly pairs them. This is semantic parsing by the LLM, never a string rule.
- Treat a named indicator, alarm, notification, or signal as an `event` when it causes the transition. Do not relabel that stimulus as a guard merely because its name describes a status. Use `guard` only for a separately stated data condition or predicate that is evaluated in addition to the event. This remains a semantic reading of the supplied clause, not a keyword or identifier-shape rule.
- A bidirectional or dynamic A-to-B/B-to-A requirement is two endpoint contracts. Never place two source hints or two target hints in one contract.
- A conjunction such as `a and b and c` on one transition is one normalized guard hint with the complete conjunction as its value, not three guard hints. Alternative guards on different transitions remain separate contracts.
- Initialization, containment, endpoint, trigger, guard, effect, action, reachability/progress, event-consumer coverage, region structure, and variable delta never share one contract merely because the NL states them in one sentence.
- `wrong_target` belongs to `transition_endpoints`, `wrong_guard` to `guard`, `wrong_effect` to `effect` or `variable_delta`, `unreachable` to `reachability`, `dead_end` to `deadlock_freedom`, and `unconsumed` to `event_consumer_coverage`. Do not encode one property with another property's direction.
- When an event is semantically required to be accepted within a scope, emit a separate `event_consumer_coverage` contract in addition to any local endpoint/trigger contract. This is a semantic LLM judgment from the supplied NL, never a spelling or keyword rule.

State-role and discourse discipline:
- Preserve the semantic role of every state-centered obligation in `state_role`. Use `operating_state` for an active control state or substate whose behavior must react, continue, or lead onward; use `termination_state` only when the NL explicitly establishes completion or intended terminal behavior. A name that sounds like stopping, emergency, final, or completion is not itself terminal evidence.
- Emit `deadlock_freedom` only when the NL explicitly requires continuation, response availability, repeated operation, or onward progress for that exact state/scope. When the NL explicitly requires an activity to be performed continuously or repeatedly, emit a separate `state_action` contract for that exact operating state/scope even if the same segment also establishes cardinality, containment, or another structural property. Merely naming an activity, entering a state, or targeting an operating state does not create a progress contract or a `state_action` contract. Cross-view grounding may later add a domain-grounded reachability/progress obligation from exact source/inspection facts; NL-only extraction must not pre-enumerate one for every state.
- When the NL explicitly says that a mode ends, completes, or terminates at a state, set that state's role to `termination_state` and emit an independent `termination` contract with `expected_direction=must_terminate` and `violation_direction=not_completed`. Do not simultaneously manufacture a progress contract for that terminal role. Grounding will assess stable termination separately from endpoint existence.
- Treat an explicit "first transitions/enters" clause as `initial_entry` into the first state under the enclosing operating owner, not as an ordinary transition from a word such as system or controller. In an initial-entry contract, `owner` is the scope that owns the required initial pseudostate edge and `target` is the state entered by that edge. Thus "the system begins in Controller" yields owner=root/system and target=Controller, while a later "within Controller, first enter ModeA" yields owner=Controller and target=ModeA. The same owner-local reading applies when one sentence first establishes "Within Controller are ModeA, ModeB, and ModeC" and the next says "the system first transitions to the ModeA substate": `system` is the grammatical actor, while the endpoint owner remains Controller; do not emit a system-to-ModeA endpoint contract for that clause. Never make the entered target its own owner merely because it is described as a composite. Resolve later omitted sources and enclosing owners by discourse semantics. A sequence such as "first enter ModeA; the system can also transition to ModeB; similarly, it can transition to ModeC" continues the operating narrative as owner-initial-to-ModeA, ModeA-to-ModeB, and ModeB-to-ModeC unless the supplied discourse explicitly resets the source or defines alternatives. By contrast, "from ModeA choose either ModeB or ModeC" yields two alternatives from ModeA. This is an LLM coreference and ordering judgment; never decide it by keywords or identifier spelling.
- Preserve every explicit parent/child relation as a separate `containment` contract. A clause that a scope transitions into, contains, or uses a named substate may establish both an endpoint/initial-entry relation and child containment; one does not replace the other. In particular, covered segment accounting never licenses omission of the containment row.
- Preserve enclosing hierarchy across numbered-segment discourse when the supplied meaning, rather than identifier spelling or model layout, keeps a transition group inside one established owner. If an earlier clause explicitly establishes source `S` as a child of owner `P` and a later group explicitly presents `A` and `B` as sibling operating alternatives inside that same continuing scope, set `common_enclosing_owner_name=P` and emit separate containment contracts `S in P`, `A in P`, and `B in P` alongside the endpoint/group contracts. The owner field records provenance only: the backend does not synthesize missing containment rows from it. Set it to null when source is itself the owner, the relation crosses scopes, only some members share an owner, or the reading is ambiguous. Do not infer it merely because `S` transitions to `A`/`B`.
- Put every direct-transition sentence in one `transition_groups` row with its semantically resolved shared source and complete target set. Sequential discourse continues from the preceding target when the supplied meaning supports that reading; it does not mechanically inherit the enclosing composite as source. When two alternatives from the same source are intended to be distinguishable or mutually exclusive, emit a separate `guard_disjointness` contract over that group. Two individually present guards do not establish disjointness.
- Treat the current numbered segment's explicit semantic target or role as authoritative. Later segments may resolve genuine anaphora, but they must not overwrite an earlier local role that is already semantically complete. In particular, "leave/exit a mode" remains a distinct local-exit target concept unless the supplied NL explicitly equates it with a later named completion or termination state. Preserve every coordinated alternative's target exactly as stated. Do not infer normative target identity from PlantUML, FCSTM, or apparent model satisfaction during contract extraction; grounding binds the preserved concept later.
- Keep semantically distinct control effects distinct even when both eventually leave a scope. A local mode exit under one condition and a later mode/system completion under another condition are different targets unless the NL explicitly identifies them. For example, an earlier `LocalExitRole` alternative must not become `NamedCompletionState` merely because a later segment names that state as the target of a different completion condition.
- An introductory statement that an enclosing controller "can transition to different substates" establishes context but no exact source-target relation until the later discourse supplies it. Do not turn that sentence into an `element_declaration` contract, and do not use it to override the sequential source resolved from later "first", "also", or "similarly" clauses. A common enclosing owner is not itself evidence of a common transition source.
- Keep a state-owned action/effect independent from the endpoint that enters the state. The action may remain a precise unsupported W1 obligation even when the endpoint exists. Do not create standalone trigger/guard contracts that merely repeat every transition-group condition; use the group as the compact normative relation and let grounding derive only actual mismatches.
- When an action, effect, display, update, reset, or cancellation obligation reads or writes one named data subject, add a separate `variable` binding hint whose value is only that subject concept. Preserve the action/effect itself in its own `action` or `effect` hint. Independent contracts that act on the same data subject must use the same exact variable concept so deterministic frontier code can audit their complete carrier surface. Different subjects remain different even when their prose is related: for example, display/update of `setpoint` and cancel/update of `setpoint` share variable=`setpoint`, while start/stop of `timer` uses variable=`timer` and must not be merged with `setpoint`.
- For every `property=cardinality` contract, fill `cardinality_requirement` from the numbered NL: preserve the literal required count, the normative scope/member concepts, and a typed primary member domain. Use `direct_child_states`, `concurrent_regions`, or `explicit_named_members` when the supplied language establishes that competent reading, and preserve another competent interpretation in `alternative_reading`; use `unresolved` only when no primary member domain can be selected. Never infer the required count or domain from the observed model, element names, or a ledger.
- For cardinality domain selection, use `concurrent_regions` only when the supplied meaning explicitly establishes parallel or orthogonal regions, simultaneously active partitions, or UML region structure. Generic words such as area, section, or part do not establish concurrency by themselves. Use `direct_child_states` only when NL directly counts child states or modes owned by one composite; use `explicit_named_members` for an explicit finite list, and preserve `unresolved` when no typed domain is semantically established. Missing separators or region objects are possible negative evidence only after concurrent-region semantics is established.
- Preserve containment depth from the NL. A state described only as being "within" or "under" a composite requires semantic descendant containment; an intermediate region or nested composite still satisfies that obligation. Require direct/immediate ownership only when the source meaning explicitly requires no intermediate owner. Region or wrapper structure is a separate contract only when the NL independently specifies that structure or its concurrency semantics.

Generic worked example: "Within Controller, start in Idle; on Begin transition from Idle to Running when enabled and set mode=active" yields contracts for Controller containment of Idle, Controller initial entry to Idle, the Idle-to-Running endpoint, and its mode=active effect. Preserve Begin and enabled on the transition-group alternative; do not duplicate them as trigger/guard contracts unless supplied wording independently requires those exact formal properties. If the clause also requires Begin to be accepted throughout Controller, that coverage requirement is a separate event-consumer contract. Do not copy the whole sentence into one multi-property contract.

Before returning, perform one semantic completeness pass without adding a new stage or response object: (1) every explicit child/substate relation has its containment contract even when the same clause also states entry or transition, and every semantically continuing enclosing scope preserves separate containment contracts for the complete source-and-alternative group; (2) every explicit ending/completion role has one termination contract and no manufactured progress contract; (3) every exact transition clause has its discourse-resolved source and target; (4) every coordinated alternative keeps its complete event and guard projections plus any independent disjointness obligation; (5) every explicitly continuous or repeated task has its independent operating `state_action` contract even when that segment already has a cardinality or structure contract; and (6) broad capability context has not been converted into a synthetic element or endpoint obligation. `segment_disposition=covered` never replaces this pass.

Return only the requested Pydantic structure."""

CONTRACT_SYSTEM_PROMPT += "\n\n" + PREDICATE_ROUTING_GUIDANCE


DISCOVERY_GROUNDING_SYSTEM_PROMPT = f"""You are one complementary discovery-grounding lens of an evidence-discovery method. {COMMON_RULES} In one cross-view response, use NL contracts, PlantUML, canonical source IR, exact source inventory, working contract, and source trace to locate author-source obligations, then use FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries to bind exact closed-model elements and propose candidates. PlantUML/canonical source is author localization, FCSTM is the closed model under test, and inspection/verify/SMT rows are deterministic facts; never substitute one role for another. Do not rewrite an NL contract to match the model, claim that source presence proves execution, or treat unknown/not-run facts as violations.

Every candidate must copy one exact `contract_id` and preserve that contract's
`locus_kind`, `locus_names`, `property`, and `violation_direction`. Evaluate the
contract property first, then select the minimal frozen predicate that decides
that same property. Do not substitute a nearby endpoint, declaration, or local
path property merely because it is executable. Record the evidence families
actually used in `evidence_types`.

Before returning, close every branch-local contract reference. If this lens
derives a new property, return the complete typed contract in
`additional_contracts` and use one response-local `NL-CONTRACT-...-DERIVED-...`
reference consistently in candidate/binding/unresolved rows. That provider
string is only a response-local join key: the runner computes the persistent ID
from the typed segment/locus/property/role/direction payload and merges lenses by
that key. Never return a candidate-only derived reference. Schema correction
must return the complete response with all previously valid rows retained.

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
S4/S5 candidate for a lifecycle action/guard, or a predicate-null W1 candidate
for an effect. Preserve W1 whenever the precise claim has no applicable
predicate input. Use `unresolved`
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
Every candidate, additional contract, binding hint, semantic binding, and
unresolved row must include its own non-empty reason and basis. These are
structural output obligations, not optional prose. Before returning, inspect
every candidate list item independently: include its full contract reference,
`requirement_quote`, `reason`, and `basis`. Inspect every
`additional_contracts[].binding_hints[]` item independently and include its own
`reason` and `basis`; parent contract prose does not fill nested fields.

Use `semantic_bindings` when a normative concept needs an exact cross-artifact
identity that cannot be represented by copying its NL name. For example, if the
NL target concept is an exit role while source/model inventories contain a
specific exit state, bind contract role=target to that exact source element and
ModelIR state. If one actual closed transition carries the conflicting endpoint,
put its exact ref in `carrier_transition_ref`. Emit status=exact only for a unique
supplied mapping; otherwise use ambiguous/unbound. Do not infer mappings from
substring, spelling, identifier shape, majority vote, or the current model target.

Return sparse structured output. Do not restate satisfied or not-applicable
contracts. Use `unresolved` only for an exact contract whose semantic source,
model identity, or necessary fact cannot be bound, and give that row its own
reason and basis. A contract absent from candidates and unresolved makes no
additional claim and remains fully preserved in the contract-stage receipt.

`additional_contracts` may add a small number of causal
atomic obligations when the cross-view closure exposes a property that the NL-only
contract extraction could not see. This does not authorize arbitrary issue
invention. Every additional contract must retain one supplied numbered NL segment,
state the requirement-side semantic implication, bind exact source/model facts,
and use a unique response-local ID under that segment's namespace with a
distinct `-DERIVED-` marker. The string is not a cross-lens semantic identity;
the runner derives that identity from the complete typed payload. A candidate
using the local reference must copy the contract's exact typed semantic fields.
Typical legitimate cases are: required operating
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
For a transition-group alternative, supplied `event` and `guard` fields are
independent parts of the normative relation even when NL extraction did not duplicate them as a
standalone atomic contract. When exact source/model comparison shows the selected
transition has the wrong or missing trigger/guard, derive one atomic contract for
that actual mismatch and emit its candidate. Do not first enumerate standalone
qualifier contracts for every satisfied alternative.

Cross-view frontier discipline:
- A `state_action` obligation and a deterministic reachable leaf/no-outgoing fact
  do not by themselves establish `deadlock_freedom`; action content and operational
  continuation are independent properties. Emit a deadlock candidate only from an
  explicit progress/response obligation or an independent deterministic source
  certificate that closes reachable, non-final, sequential no-continuation
  semantics. Do not enumerate progress for every state merely because it is named,
  entered, or assigned an action.
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
  `guard_disjointness` candidate with predicate=null/W1. Individual S3/S5
  successes cannot rebut it.
- When an NL endpoint denotes a semantic local exit or role rather than a literal
  state spelling, use the canonical author-source inventory to bind the exact
  intended target before comparing the closed FCSTM. A present edge to another
  exact target is evidence for a wrong-target candidate, not grounds to rewrite
  the normative target or mark it unresolved.

{PREDICATE_ROUTING_GUIDANCE}

Inspection-equivalent routing: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one V1(initial_scope) candidate,
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

Respect protected compiler-macro boundaries. When the working contract maps one
exact author transition to a source-owned macro root and a complete protected
member inventory, assess the endpoint through the whole macro rather than treating
one generated segment as an independent author transition. A complete macro may
satisfy an endpoint only when the source endpoints, member digest, protected
ownership, exact closed-model lines, and target-entry segment all close. If any
join is missing or ambiguous, retain the endpoint candidate for downstream
adjudication; never infer macro satisfaction from generated names or one segment.

For event-consumer coverage, distinguish declaration from operational coverage.
An exact declared consumer with no consumer reachable in the contract's exact
operating scope violates a reachable-consumer contract; the declaration is a
supporting structural fact, not satisfaction of the stronger property. For a
finite cardinality contract, once this lens semantically binds the exact owner
and member kind, use the complete exact inventory to compare the member count.
The absence of a dedicated frozen predicate changes W to W1; it does not make
the already bound finite comparison unresolved.

Cardinality grounding protocol: do not rewrite the NL contract or encode the
domain choice only in candidate prose. For every supplied `property=cardinality`
contract, this lens must return exactly one `cardinality_bindings` row; it cannot
silently skip the row by deciding not to analyze the contract. Return an
`ambiguous` or `unbound` row with `member_domain=unresolved` and null owner refs
when no exact primary reading or owner closes. Every branch-local additional
cardinality contract also requires one row. On schema correction, return the
complete replacement response and retain all previously valid rows while adding
any missing required IDs. This lens must not emit a cardinality CandidateIssue:
the deterministic frontier combines the two typed bindings, enumerates the
complete member inventory, and materializes the sole cardinality candidate or
satisfaction receipt. Do not turn an alternative reading into a second candidate.
Select a concrete primary domain only from the supplied NL/source semantics.
Select `concurrent_regions` only when the supplied meaning explicitly establishes
parallel or orthogonal regions, simultaneously active partitions, or UML region
structure. Generic area, section, or part language is insufficient by itself.
Missing separators or region objects are possible negative evidence only after
that semantic domain is established; absence of a required construct is possible
negative evidence, not grounds to reinterpret the obligation. A non-empty composite without separators
has one implicit UML region, not one region per child state. Use `direct_child_states` only when the NL
directly counts child states or modes owned by one composite. Named operating
phases/states remain a competent `alternative_reading` when another domain is
explicitly primary; their existence and count must not replace that primary reading. Never choose a domain because
the resulting observed count would pass or fail, or infer it from element names.

Bind the exact `owner_source_id` plus `owner_model_ref`; copy `owner_model_ref`
exactly from the owned `closed_model_inventory.states[].ref`, not from a
working-contract representation mapping. The owner realizes the cardinality
contract's normative `scope_concept` and owner/scope binding hints. Bind it to the
contract-level scope, not to a descendant action carrier merely because an activity
in the same clause executes there. When a clause explicitly assigns orthogonal
regions to an enclosing controller while locating tasks in one descendant region,
bind the region domain to the enclosing controller unless the supplied meaning
explicitly makes the descendant the counted scope. Both lenses apply this same
contract-level owner rule.
A competing competent interpretation belongs in `alternative_reading` and is
assessed later by D; its existence does not by itself make the primary binding
ambiguous. Use `status=ambiguous` and `member_domain=unresolved` only when supplied
semantics genuinely do not support one primary reading. The deterministic frontier,
not this response, enumerates the complete members and computes the observed count.

For a supplied transition group, compare all alternatives as one relation before
checking each endpoint in isolation. When two semantically exclusive target
alternatives from the same exact source carry the same effective condition, emit
one `guard_disjointness` candidate whose locus names the shared source and target
set. Preserve the precise relation as predicate-null W1. The
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

Ground containment only from explicit typed containment contracts. A transition
group's common owner records discourse provenance but does not authorize this
stage or the backend to synthesize omitted sibling-containment obligations. If
contract extraction omitted such a relation, preserve that omission in the audit
instead of inventing an owner from transition membership. Cross-scope or ambiguous
relations must remain unexpanded.

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


D_SYSTEM_PROMPT = """You are the method's semantic D adjudication stage. Use only the supplied NL contracts, author-source facts, exact bindings, predicate plan, and backend receipt. Never read or infer evaluation ground truth, scores, reviewer examples, artifacts from other evaluation cases, or previously generated reports. Do not output D0/D1/D2, W0/W1/W2, L, a hit, or a release decision. Instead return one SemanticAdjudication per supplied obligation using only the closed grounding and defeater enums. `reason` must explain the supplied NL clause, exact source/model facts, and strongest alternative reading; `basis` must identify the supplied artifacts. Write every generated decision, violated-obligation summary, defeater, reason, and basis in English. Preserve non-English text only inside exact quotations or identifiers copied from supplied artifacts, and explain each quotation in English. Free-text wording is for audit only: do not decide from keyword, substring, regex, spelling, identifier shape, or text similarity.

D boundary: a predicate-null route, incomplete typed input, or unavailable execution does not erase a precise issue. When exact supplied source/model facts establish the candidate's semantic obligation, use grounding=established and describe the surviving ambiguity as a typed defeater when appropriate; deterministic code will keep it at W1. Use grounding=unresolved only when the supplied dossier genuinely cannot decide. A completed predicate result that is true for the requirement is not a violation merely because the candidate text sounds concerning.

Every supplied dossier includes `defeater_evidence_reference_catalog`. When an
undercutting or rebutting defeater survives, copy one or more exact catalog
tokens into `defeater_evidence_refs`; a conceivable hidden mechanism, an
unbound label, or free-text assertion is not evidence. Keep the list empty for
defeater_kind=none, and never invent an identifier absent from that obligation's
catalog.

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

V1 frontier protocol: when predicate_id=V1, inspect the exact bound state refs,
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
decided from the supplied dossier. Never turn an unsupported V1 plan into W2,
and never discard a precise W1 frontier issue."""


def build_contract_prompt(
    pair: PairInput,
    round_index: int,
) -> str:
    """Build the single whole-cell typed contract-extraction prompt."""

    if not pair.nl_segments:
        raise ValueError("contract extraction requires at least one numbered NL segment")
    context = prompt_context_payload(pair, stage="nl_contract_extraction")
    context_text = json.dumps(context, ensure_ascii=False, sort_keys=True)

    return f"""Stage: contract-extraction
Round: {round_index}
Stage-scoped context projection and complete artifact manifest:
{context_text}

Extract one NLContract per independently violable normative obligation. The typed semantic key and binding hints are the contract plan consumed by both grounding branches. Mark every supplied numbered NL segment as covered, context, or ambiguous. Every contract_id must include its exact segment_id (for example, NL-CONTRACT-NL6-ENDPOINT-1) and must be unique within this whole-cell response. Do not include evaluation identifiers, scores, reviewer examples, W/D/L values, or hidden expected answers.

If Pydantic schema feedback requests a correction, return the complete replacement
NLContractResponse: preserve and repeat every already valid contract and transition
group, correct each invalid row in place, and keep every segment disposition. Never
return only the row named by the latest validation error.
"""


def build_contract_completion_prompt(
    pair: PairInput,
    round_index: int,
    primary_contracts: NLContractResponse,
) -> str:
    """Build one bounded in-node correction prompt for property coverage.

    This prompt asks only for additions, preserving the successful primary
    response rather than asking a second model call to regenerate it.
    """

    context = prompt_context_payload(pair, stage="nl_contract_extraction")
    return f"""{CONTRACT_SYSTEM_PROMPT}

Stage: contract-completion-correction
Round: {round_index}
This is one bounded in-node property-coverage correction, not a new method
round and not a model-satisfaction check. A numbered NL segment may establish
multiple independently violable obligations even when the primary typed plan
already has many contracts. Use only the supplied numbered NL, source context,
and primary typed plan. Do not read or infer a ledger, expected issue, Judge
result, historical report, score, W/D/L level, or another pair.

Return only independently violable obligations or complete transition groups
that the current NL establishes but the primary plan omitted. Do not repeat,
edit, merge, weaken, or replace any existing contract/group. Preserve complete
source, target, owner/scope, event, guard, effect/output, lifecycle role,
member set/count, and transition-group roles where the NL establishes them.
Check independently whether the current NL establishes cardinality/member-set,
owner-local entry, source/target endpoint, event, guard, effect/output,
lifecycle action, event-consumer coverage, transition group, progress, or
termination obligations not already represented by the primary typed identity.
One retained property never substitutes for another merely because the carrier
or domain vocabulary is similar.
When no additional typed obligation is justified, return empty lists with a
non-empty reason and basis. A coarse satisfied predicate check cannot erase an
exact obligation retained here.

Primary typed plan:
{json.dumps(_compact_contract_plan(primary_contracts), ensure_ascii=False, sort_keys=True, indent=2)}

Stage-scoped context projection and complete artifact manifest:
{json.dumps(context, ensure_ascii=False, sort_keys=True, indent=2)}
"""


def build_grounding_prompt(
    pair: PairInput,
    *,
    lens: GroundingLens,
    round_index: int,
    contracts: NLContractResponse,
    contract_reference_aliases: Mapping[str, str] | None = None,
) -> str:
    """Build one complementary-lens prompt over the shared compact cross-view closure."""

    contract_ids = [contract.contract_id for contract in contracts.contracts]
    aliases = dict(contract_reference_aliases or {})
    reference_protocol = (
        "The supplied contract IDs are:\n"
        f"{json.dumps(contract_ids, ensure_ascii=False)}\n"
        "Candidates, bindings, cardinality rows, and unresolved rows may use these IDs."
        if not aliases
        else (
            "The primary typed plan below retains persistent canonical contract IDs. "
            "For every response-side `contract_id` that refers to a supplied contract, "
            "use the exact short alias key from this closed table, not the long canonical "
            "value. The runner deterministically maps only these listed aliases back to "
            "their paired canonical IDs before semantic validation and records that map in "
            "the audit; it never repairs near matches. Do not use aliases for a "
            "branch-local `additional_contracts` row:\n"
            f"{json.dumps(aliases, ensure_ascii=False, sort_keys=True)}"
        )
    )

    return f"""Stage: discovery-grounding
Round: {round_index}
Complementary audit lens: {lens}
Lens priority: {DISCOVERY_GROUNDING_AUDIT_LENSES[lens]}
Frozen predicate input spellings: S1={{kind, element, scope}} S2={{source, target, scope}} S3={{transition, triggers}} S4={{state, phase, action}} S5={{transition, guard}} G1={{source, target}} G2={{source, target}} G3={{roots, marked}} R1={{scenario, event, step}} R2={{scenario, stimulus, state, window}} R3={{scenario, state, interval}} V1={{initial_scope}}.
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
{reference_protocol}
A branch-local derived
candidate must instead name one exact row returned in `additional_contracts`.
Every branch-local additional contract reference must be unique within this
response. It need not predict the runner's canonical ID and must never be used
to decide semantic equivalence across lenses.
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


def _compact_d_receipt_run_metadata(value: Any) -> Any:
    """Keep semantic execution facts while leaving raw FBMCQ formula text receipt-only."""

    if not isinstance(value, dict):
        return value
    projected = dict(value)
    fbmcq_formula = projected.get("fbmcq_formula")
    if not isinstance(fbmcq_formula, dict):
        return projected
    formulas = fbmcq_formula.get("formulas")
    if not isinstance(formulas, dict):
        return projected
    serialized = json.dumps(
        formulas,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    compact_formula = dict(fbmcq_formula)
    compact_formula["formulas"] = {
        "formula_keys": sorted(str(key) for key in formulas),
        "formula_hash": _hash(formulas),
        "serialized_characters": len(serialized),
        "prompt_included": False,
        "reason": "Raw solver formulas remain in the immutable backend receipt; D receives their exact hash and semantic execution result.",
        "basis": "dossier-prompt-projection.v4 and canonical JSON hashing",
    }
    projected["fbmcq_formula"] = compact_formula
    return projected


def _compact_dossier(dossier: dict[str, Any]) -> dict[str, Any]:
    """Project one D dossier to semantic facts without duplicating audit bytes."""

    candidate = dossier.get("candidate", {})
    binding = dossier.get("binding", {})
    plan = dossier.get("plan", {})
    receipt = dossier.get("receipt", {})
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
            "reason",
            "basis",
        )
        if key in receipt
    }
    if "run_metadata" in receipt:
        compact_receipt["run_metadata"] = _compact_d_receipt_run_metadata(
            receipt["run_metadata"]
        )
    return {
        "obligation_id": dossier.get("obligation_id"),
        "defeater_evidence_reference_catalog": dossier.get(
            "defeater_evidence_reference_catalog", []
        ),
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
        "reason": "D receives the exact candidate, binding, predicate semantics, and backend result; repeated paths, attribution metadata, raw audit, and retry payloads remain receipt-only.",
        "basis": "dossier-prompt-projection.v4",
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
    """Build one targeted repair prompt for missing or invalid D rows."""

    invalid_decisions = invalid_decisions or {}
    repair_ids = set(missing_ids) | set(duplicate_ids) | set(invalid_decisions)
    ordered_repair_ids = sorted(repair_ids)
    selected = [
        dossier
        for dossier in dossiers
        if dossier["obligation_id"] in repair_ids
    ]
    return f"""{D_SYSTEM_PROMPT}

Stage: d_adjudication_correction
The previous structured response violated the exact obligation coverage contract.
This is an in-node contract correction, not a new method round. Return decisions
only for the repair IDs below, preserving their exact spelling. A duplicate ID
requires a replacement decision just as a missing ID does.

repair_ids:
{json.dumps(ordered_repair_ids, ensure_ascii=False)}

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

Return exactly one decision for every ID in repair_ids and no decision for any
other ID. Do not repeat any frozen valid decision or any extra ID. If the
supplied dossier cannot decide, use grounding=unresolved with a non-empty reason
and basis. Do not emit W/D/L levels, evaluation ground truth, scores, or
reviewer examples.
"""


def _partition_d_prompt_batches(
    dossiers: list[dict[str, Any]],
    *,
    kind: Literal["initial", "correction"],
    character_budget: int,
    prompt_factory: Callable[[list[dict[str, Any]]], str],
) -> tuple[DAdjudicationPromptBatch, ...]:
    """Partition complete dossiers by exact serialized prompt size."""

    if character_budget <= 0:
        raise ValueError("D prompt character budget must be positive")
    ordered = sorted(dossiers, key=lambda item: str(item.get("obligation_id", "")))
    obligation_ids = [str(item.get("obligation_id", "")) for item in ordered]
    if any(not obligation_id for obligation_id in obligation_ids):
        raise ValueError("every D dossier requires a non-empty obligation_id")
    if len(obligation_ids) != len(set(obligation_ids)):
        raise ValueError("D dossiers require unique obligation_id values")

    groups: list[tuple[list[dict[str, Any]], str]] = []
    current: list[dict[str, Any]] = []
    current_prompt = ""
    for dossier in ordered:
        tentative = [*current, dossier]
        tentative_prompt = prompt_factory(tentative)
        if current and len(tentative_prompt) > character_budget:
            groups.append((current, current_prompt))
            current = [dossier]
            current_prompt = prompt_factory(current)
        else:
            current = tentative
            current_prompt = tentative_prompt
    if current:
        groups.append((current, current_prompt))

    return tuple(
        DAdjudicationPromptBatch(
            kind=kind,
            batch_index=index,
            obligation_ids=tuple(
                str(dossier["obligation_id"]) for dossier in batch_dossiers
            ),
            prompt=prompt,
            prompt_characters=len(prompt),
            character_budget=character_budget,
            exceeds_budget=len(prompt) > character_budget,
            reason=(
                "The stable obligation-ID batch retains every selected semantic dossier in full."
            ),
            basis=(
                f"dossier-prompt-projection.v4; kind={kind}; "
                f"prompt_characters={len(prompt)}; character_budget={character_budget}"
            ),
        )
        for index, (batch_dossiers, prompt) in enumerate(groups, start=1)
    )


def build_d_adjudication_batches(
    pair: PairInput,
    dossiers: list[dict[str, Any]],
    *,
    character_budget: int,
) -> tuple[DAdjudicationPromptBatch, ...]:
    """Build stable initial D batches without splitting or truncating a dossier."""

    return _partition_d_prompt_batches(
        dossiers,
        kind="initial",
        character_budget=character_budget,
        prompt_factory=lambda selected: build_d_adjudication_prompt(pair, selected),
    )


def build_d_correction_batches(
    pair: PairInput,
    dossiers: list[dict[str, Any]],
    *,
    missing_ids: list[str],
    duplicate_ids: list[str],
    extra_ids: list[str],
    invalid_decisions: dict[str, list[str]] | None = None,
    character_budget: int,
) -> tuple[DAdjudicationPromptBatch, ...]:
    """Build stable targeted-correction batches over only defective obligation IDs."""

    invalid_decisions = invalid_decisions or {}
    repair_ids = set(missing_ids) | set(duplicate_ids) | set(invalid_decisions)
    selected = [
        dossier
        for dossier in dossiers
        if str(dossier.get("obligation_id", "")) in repair_ids
    ]

    def correction_prompt(batch: list[dict[str, Any]]) -> str:
        batch_ids = {str(item["obligation_id"]) for item in batch}
        return build_d_correction_prompt(
            pair,
            batch,
            missing_ids=sorted(batch_ids & set(missing_ids)),
            duplicate_ids=sorted(batch_ids & set(duplicate_ids)),
            extra_ids=sorted(extra_ids),
            invalid_decisions={
                obligation_id: invalid_decisions[obligation_id]
                for obligation_id in sorted(batch_ids & set(invalid_decisions))
            },
        )

    return _partition_d_prompt_batches(
        selected,
        kind="correction",
        character_budget=character_budget,
        prompt_factory=correction_prompt,
    )


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
    """Compatibility prompt exposing the first complementary discovery lens."""

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
        reason="The compatibility prompt exposes the complete typed context.",
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
        cardinality_bindings=[
            CardinalityDomainBinding(
                binding_id=f"CARD-BIND-FALLBACK-{lens}-{index}",
                contract_id=contract.contract_id,
                status="unbound",
                member_domain="unresolved",
                owner_source_id=None,
                owner_model_ref=None,
                alternative_reading=None,
                reason="The failed grounding lens cannot select a semantic member domain or exact owner.",
                basis=f"{reason}; deterministic lens-local failure receipt",
            )
            for index, contract in enumerate(contracts.contracts, start=1)
            if contract.property == "cardinality"
        ],
        candidates=[],
        unresolved=[
            GroundingUnresolved(
                contract_id=contract.contract_id,
                reason="The lens provider/schema result was unavailable; no semantic candidate was inferred from an unrelated model fact.",
                basis=f"{reason}; exact contract ID accounting and no-fabricated-fallback rule",
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
    """Merge both complementary-lens candidate surfaces by exact typed identity."""

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
    "CONTRACT_SYSTEM_PROMPT",
    "DISCOVERY_GROUNDING_AUDIT_LENSES",
    "DISCOVERY_GROUNDING_SYSTEM_PROMPT",
    "D_SYSTEM_PROMPT",
    "CardinalityDomainBinding",
    "CardinalityRequirement",
    "ContractCompletionResponse",
    "DAdjudicationPromptBatch",
    "GroundingResponse",
    "GroundingUnresolved",
    "NLContract",
    "NLContractResponse",
    "NLTransitionAlternative",
    "NLTransitionGroup",
    "SegmentCoverage",
    "SemanticBinding",
    "StageReceipt",
    "assemble_method_response",
    "build_contract_prompt",
    "build_contract_completion_prompt",
    "build_d_adjudication_batches",
    "build_d_adjudication_prompt",
    "build_d_correction_batches",
    "build_d_correction_prompt",
    "build_grounding_prompt",
    "build_method_prompt",
    "fallback_contracts",
    "fallback_d_adjudication",
    "fallback_grounding",
    "materialize_segment_coverage",
    "normalize_contract_state_roles",
]
