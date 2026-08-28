"""Typed semantic-frontier materialization.

The LLM establishes normative contracts and semantic transition groups.  This
module then expands those typed obligations against exact source, ModelIR, and
inspection-equivalent facts.  It never reads ledger data and never interprets
free text with keyword, regular-expression, or similarity rules.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from collections.abc import Mapping, Sequence
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.context import (
    InspectionStateFact,
    InspectionTransitionFact,
    SourceInventoryState,
    SourceInventoryTransition,
)
from ..inputs.models import PairInput, StateNode, Transition
from .binding import bind_candidate, resolve_state_ref
from .obligations import (
    CandidateIssue,
    ContractBindingHint,
    EvidenceType,
    ExpectedDirection,
    ObligationLocusKind,
    ObligationProperty,
    ViolationDirection,
)
from .workflow import (
    CardinalityDomainBinding,
    CardinalityRequirement,
    GroundingResponse,
    NLContract,
    NLContractResponse,
    NLTransitionGroup,
    SemanticBinding,
    StateSemanticRole,
)

FrontierKind = Literal[
    "containment",
    "aggregate_containment",
    "cardinality",
    "owner_initial_entry",
    "aggregate_initial_entry",
    "root_reachability",
    "event_consumer_coverage",
    "stable_termination",
    "aggregate_stable_termination",
    "transition_group_collision",
    "wrong_target",
    "reachable_dead_end",
    "cross_wrapper_reachability",
    "aggregate_zero_behavior",
    "transition_guard_presence",
    "state_after_stimulus",
    "initial_entry_trigger_set",
    "aggregate_data_semantics",
]


class ContractSemanticKey(BaseModel):
    """Typed key identifying one normative obligation across contract and grounding.

    This object expresses only obligation identity. It says nothing about model
    satisfaction and carries no W, D, L, or Judge information. The runner uses
    its normalized JSON to generate the authoritative derived-contract ID.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.contract-semantic-key.v2"] = Field(
        default="evidence-discovery.contract-semantic-key.v2",
        description="Schema version of this typed identity, used for artifact and resume audit and never for semantic adjudication.",
    )
    segment_id: str = Field(
        pattern=r"^NL[0-9]+(?:\.[0-9]+)?$",
        description="Numbered NL segment grounding the obligation; it supplies normative provenance and is not a ledger identity.",
    )
    locus_kind: ObligationLocusKind = Field(
        min_length=1,
        description="Domain-locus type that can be violated, separate from property; a property name cannot substitute for an object type.",
    )
    locus_names: tuple[str, ...] = Field(
        min_length=1,
        description="Exact semantic locus-name sequence established by the LLM; order is part of identity and no text-similarity merging is allowed.",
    )
    property: ObligationProperty = Field(
        min_length=1,
        description="Single atomic property examined by the obligation; different properties retain different identities even when they share a cause.",
    )
    state_role: StateSemanticRole | None = Field(
        default=None,
        description="State role established by NL; null means the obligation is not centered on one state role, and a role may not be inferred from a name.",
    )
    expected_direction: ExpectedDirection = Field(
        min_length=1,
        description="Positive normative requirement used to distinguish nearby obligations such as must-enter, must-reach, and must-progress.",
    )
    violation_direction: ViolationDirection = Field(
        min_length=1,
        description="Defect direction the candidate must inspect; missing, wrong-scope, unreachable, and other directions cannot cover one another.",
    )
    cardinality_requirement: CardinalityRequirement | None = Field(
        default=None,
        description="Normative required count and typed member domain for a cardinality obligation; null for non-cardinality identity and never populated from free text.",
    )


class TransitionAlternativeSemanticKey(BaseModel):
    """Typed identity of one transition-group member without a provider string ID."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.transition-alternative-key.v2"] = Field(default="evidence-discovery.transition-alternative-key.v2", description="Schema version of the alternative semantic key; v2 separates event from guard.")
    target_name: str = Field(min_length=1, description="Normative target after LLM discourse binding; sequence and exact value participate in identity.")
    event: str | None = Field(default=None, min_length=1, description="Independent normative event identity; null means the relation establishes no event and is not an observed-trigger conclusion.")
    guard: str | None = Field(default=None, min_length=1, description="Independent normative guard that may coexist with event; null means the relation establishes no guard.")


class TransitionGroupSemanticKey(BaseModel):
    """Authoritative typed identity used by the runner to merge base and grounding transition groups."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.transition-group-key.v3"] = Field(default="evidence-discovery.transition-group-key.v3", description="Schema version of the transition-group semantic key; v3 replaces one condition role with separate event/guard member identity.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", description="Exact numbered NL segment establishing the relation.")
    source_name: str = Field(min_length=1, description="Shared source resolved by LLM discourse analysis; the enclosing owner may not substitute automatically.")
    common_enclosing_owner_name: str | None = Field(default=None, min_length=1, description="Complete sibling-group owner explicitly established by the LLM; null means the relation does not authorize containment expansion.")
    alternatives: tuple[TransitionAlternativeSemanticKey, ...] = Field(min_length=1, description="Complete ordered alternatives; a different target, condition, or order creates a different relation.")


class IdentityNormalizationReceipt(BaseModel):
    """Deterministic normalization receipt for one grounding branch-local identity.

    The runner produces this object at the discovery-grounding boundary and
    replaces an LLM-generated string ID with a typed semantic key. It proves only
    reference rewriting and provenance, not a frontier check, model satisfaction,
    W, D, L, or a Judge conclusion.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.identity-normalization.v4"] = Field(
        default="evidence-discovery.identity-normalization.v4",
        description="Persistence schema version of the identity-normalization receipt.",
    )
    algorithm_version: Literal["typed-contract-identity.v4"] = Field(
        default="typed-contract-identity.v4",
        description="Deterministic algorithm version that creates canonical IDs, rewrites exact branch-local references, and recovers unique typed candidate references.",
    )
    lens: Literal["contract_structure_contrast", "behavior_consequence"] = Field(
        description="Grounding lens that produced the raw additional contract; used only for provenance.",
    )
    raw_contract_id: str = Field(
        min_length=1,
        description="Branch-local ID returned by the provider; retained only for audit and never authoritative for semantic identity.",
    )
    canonical_contract_id: str = Field(
        min_length=1,
        description="Authoritative derived-contract ID generated by the runner from the complete ContractSemanticKey.",
    )
    semantic_key: ContractSemanticKey = Field(
        description="Complete typed identity used for the canonical ID; contains no satisfaction, W, D, or ledger information.",
    )
    rewritten_candidate_count: int = Field(
        ge=0,
        description="Number of candidate references rewritten exactly from raw to canonical ID in this lens.",
    )
    projected_candidate_identity_count: int = Field(
        ge=0,
        description="Number of candidates whose locus/property/direction was projected from the referenced contract's authoritative typed key in this lens; raw provider payload remains in call audit.",
    )
    recovered_candidate_reference_count: int = Field(
        default=0,
        ge=0,
        description="Number of candidates recovered to this contract when provider-derived local-reference spelling drifted, using only a unique typed projection of locus kind/names, property, direction, and evidence family; zero means no such recovery occurred.",
    )
    rewritten_unresolved_count: int = Field(
        ge=0,
        description="Number of unresolved references rewritten exactly from raw to canonical ID in this lens.",
    )
    rewritten_binding_count: int = Field(
        ge=0,
        description="Number of SemanticBinding references rewritten exactly from raw to canonical ID in this lens.",
    )
    rewritten_cardinality_binding_count: int = Field(
        ge=0,
        description="Number of CardinalityDomainBinding references rewritten exactly from raw to canonical ID in this lens.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why the runner must replace branch-local string identity with typed identity.",
    )
    basis: str = Field(
        min_length=1,
        description="Auditable basis listing lens, raw/canonical IDs, and ContractSemanticKey.",
    )


class GroupIdentityNormalizationReceipt(BaseModel):
    """Runner canonicalization receipt for one grounding branch-local transition group."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.group-identity-normalization.v3"] = Field(default="evidence-discovery.group-identity-normalization.v3", description="Group identity-normalization receipt schema version; v3 records event/guard-separated member identity.")
    algorithm_version: Literal["typed-transition-group-identity.v3"] = Field(default="typed-transition-group-identity.v3", description="Deterministic algorithm version for canonical group/alternative IDs; v3 uses target, event, guard, and common owner.")
    lens: Literal["contract_structure_contrast", "behavior_consequence"] = Field(description="Grounding lens that produced the raw additional group; used only for provenance.")
    raw_group_id: str = Field(min_length=1, description="Branch-local group ID returned by the provider; it no longer determines downstream identity.")
    canonical_group_id: str = Field(min_length=1, description="Authoritative group ID generated by the runner from TransitionGroupSemanticKey.")
    semantic_key: TransitionGroupSemanticKey = Field(description="Complete typed relation identity used to generate the canonical group ID.")
    alternative_id_map: dict[str, str] = Field(description="Exact rewrite map from branch-local alternative ID to canonical ordered-member ID; an empty map would mean a structurally invalid memberless group.")
    reason: str = Field(min_length=1, description="Explains why runner canonical identity replaces branch-local string identity.")
    basis: str = Field(min_length=1, description="Lists lens, raw/canonical group IDs, and typed semantic key.")


class FrontierCheckReceipt(BaseModel):
    """Deterministic receipt for one typed frontier check from the execute batch.

    The receipt records expansion of a typed obligation against exact facts. It
    is not an issue release and does not decide D. candidate status means only
    that an exact claim now awaits D adjudication.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.frontier-check.v2"] = Field(
        default="evidence-discovery.frontier-check.v2",
        description="Schema version of the frontier-check receipt.",
    )
    algorithm_version: Literal[
        "typed-domain-frontier.v24", "typed-domain-frontier.v25"
    ] = Field(
        default="typed-domain-frontier.v25",
        description="Deterministic algorithm version that produced the check. The current value adds event/post-state projection only when one typed transition alternative, one canonical author-source carrier, and one native FCSTM event identity close exactly; the previous accepted value remains readable for immutable replay artifacts.",
    )
    check_id: str = Field(
        min_length=1,
        description="Stable check ID calculated from frontier kind, typed contract identity, and exact references.",
    )
    kind: FrontierKind = Field(
        description="Domain-frontier type being systematically expanded; it is not a frozen predicate ID.",
    )
    source_contract_ids: tuple[str, ...] = Field(
        min_length=1,
        description="Base or derived contract IDs establishing the check's normativity; must contain no ledger ID.",
    )
    canonical_contract_id: str | None = Field(
        default=None,
        description="Authoritative runner-generated contract ID when the check forms a candidate; otherwise null.",
    )
    status: Literal["candidate", "satisfied", "unresolved", "not_applicable"] = Field(
        description="Deterministic expansion status; candidate still requires D, satisfied is not published, and unresolved is not disguised as a miss.",
    )
    model_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Closed ModelIR references actually used by the check; author-source references may not be mixed in.",
    )
    root_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact closed-model root references for a topology projection, when the frontier check has a typed root role; empty for other frontier kinds or incomplete identity.",
    )
    marked_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Exact closed-model marked-target references for a topology projection, when the frontier check has a typed marked role; empty for other frontier kinds or incomplete identity.",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="NL, PlantUML, or canonical-source references used by the check; they provide only normativity and source localization.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why the typed obligation and exact facts produce the current frontier status.",
    )
    basis: str = Field(
        min_length=1,
        description="Auditable basis listing contract key, ModelIR, inspection, source inventory, and algorithm version.",
    )


class FrontierObligation(BaseModel):
    """Domain property awaiting adjudication, triggered by a normative obligation and exact facts.

    The runner produces this object in the execute batch and sends its candidate
    to the compiler/backend for the frozen 19 predicates. It is not a new
    predicate and has no authoritative D, W, or L level.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.frontier-obligation.v1"] = Field(
        default="evidence-discovery.frontier-obligation.v1",
        description="Persistence schema version for a frontier obligation.",
    )
    frontier_id: str = Field(
        min_length=1,
        description="Stable frontier identity generated from frontier kind, canonical contract, and exact references.",
    )
    kind: FrontierKind = Field(
        description="Domain candidate-frontier type; downstream stages may still choose only one of the frozen 19 predicates or null/W1.",
    )
    source_contract_ids: tuple[str, ...] = Field(
        min_length=1,
        description="Contract IDs providing normative support for the derived obligation; multiple IDs denote a cross-contract relation.",
    )
    contract: NLContract = Field(
        description="Authoritative typed contract actually bound to the candidate; the runner generates the derived ID rather than the LLM.",
    )
    candidate: CandidateIssue = Field(
        description="Atomic falsifiable claim under one locus/property/scope; contains no W, D, or L.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why this domain obligation must be expanded from existing contracts and exact facts.",
    )
    basis: str = Field(
        min_length=1,
        description="Lists typed contract, source/model/inspection facts, and deterministic expansion rule.",
    )


class FrontierBatch(BaseModel):
    """Complete typed frontier output of one execute batch for runner and artifact audit."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.frontier-batch.v1"] = Field(
        default="evidence-discovery.frontier-batch.v1",
        description="Schema version of this frontier-batch artifact.",
    )
    algorithm_version: Literal[
        "typed-domain-frontier.v24", "typed-domain-frontier.v25"
    ] = Field(
        default="typed-domain-frontier.v25",
        description="Deterministic algorithm version used by every check and obligation in this batch. The current value preserves prior behavior and adds exact transition-group event/post-state projection through canonical source and native FCSTM identities; the previous accepted value remains readable for historical replay.",
    )
    obligations: tuple[FrontierObligation, ...] = Field(
        default_factory=tuple,
        description="Domain obligations that actually formed candidates; each still requires compiler/backend, D, and publish processing.",
    )
    checks: tuple[FrontierCheckReceipt, ...] = Field(
        default_factory=tuple,
        description="Complete receipts for candidate, satisfied, and unresolved checks so audit does not retain only published results.",
    )
    superseded_candidate_contract_ids: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Provisional LLM candidate contract IDs superseded by complete exact typed frontier expansion of the same contract/property; raw grounding output remains in audit and downstream processing skips only duplicate D dossiers.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains how the batch expands the typed discovery frontier while keeping the 19 predicates responsible only for W evidence.",
    )
    basis: str = Field(
        min_length=1,
        description="Version basis for contracts/groups, ModelIR, source inventory, and inspection facts used by this batch.",
    )


def contract_semantic_key(contract: NLContract) -> ContractSemanticKey:
    """Return the exact typed identity of one contract without interpreting prose."""

    return ContractSemanticKey(
        segment_id=contract.segment_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        state_role=contract.state_role,
        expected_direction=contract.expected_direction,
        violation_direction=contract.violation_direction,
        cardinality_requirement=contract.cardinality_requirement,
    )


def canonical_contract_id(contract: NLContract) -> str:
    """Generate the runner-authoritative derived ID from the typed semantic key."""

    payload = contract_semantic_key(contract).model_dump(mode="json")
    encoded = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    digest = hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]
    return f"NL-CONTRACT-{contract.segment_id}-DERIVED-{digest}"


def transition_group_semantic_key(
    group: NLTransitionGroup,
) -> TransitionGroupSemanticKey:
    """Return one exact ordered group identity without interpreting prose."""

    return TransitionGroupSemanticKey(
        segment_id=group.segment_id,
        source_name=group.source_name,
        common_enclosing_owner_name=group.common_enclosing_owner_name,
        alternatives=tuple(
            TransitionAlternativeSemanticKey(
                target_name=item.target_name,
                event=item.event,
                guard=item.guard,
            )
            for item in group.alternatives
        ),
    )


def canonical_transition_group_id(group: NLTransitionGroup) -> str:
    """Generate a runner-authoritative ID for one typed transition relation."""

    payload = transition_group_semantic_key(group).model_dump(mode="json")
    digest = _hash_payload(payload)
    return f"NL-GROUP-{group.segment_id}-DERIVED-{digest}"


def _canonicalize_transition_group(
    group: NLTransitionGroup,
) -> tuple[NLTransitionGroup, dict[str, str]]:
    canonical_group_id = canonical_transition_group_id(group)
    alternatives = []
    alternative_id_map: dict[str, str] = {}
    for index, alternative in enumerate(group.alternatives, start=1):
        alternative_payload = TransitionAlternativeSemanticKey(
            target_name=alternative.target_name,
            event=alternative.event,
            guard=alternative.guard,
        ).model_dump(mode="json")
        canonical_alternative_id = (
            f"ALT-{index}-{_hash_payload([canonical_group_id, alternative_payload])}"
        )
        alternative_id_map[alternative.alternative_id] = canonical_alternative_id
        alternatives.append(
            alternative.model_copy(
                update={"alternative_id": canonical_alternative_id}
            )
        )
    return (
        group.model_copy(
            update={
                "group_id": canonical_group_id,
                "alternatives": tuple(alternatives),
            }
        ),
        alternative_id_map,
    )


def _candidate_contract_reference_key(candidate: CandidateIssue) -> tuple[object, ...]:
    """Return the exact typed candidate fields shared with its contract."""

    return (
        candidate.locus_kind,
        candidate.locus_names,
        candidate.property,
        candidate.violation_direction,
        candidate.evidence_types,
    )


def _contract_candidate_reference_key(contract: NLContract) -> tuple[object, ...]:
    """Return the contract projection available on a grounding candidate."""

    return (
        contract.locus_kind,
        contract.locus_names,
        contract.property,
        contract.violation_direction,
        contract.evidence_types,
    )


def canonicalize_grounding_response(
    response: GroundingResponse,
) -> tuple[
    GroundingResponse,
    tuple[IdentityNormalizationReceipt | GroupIdentityNormalizationReceipt, ...],
]:
    """Replace LLM branch-local derived IDs with typed canonical identities.

    Raw provider output remains in the runtime audit.  This normalized response
    is the only branch payload admitted to downstream contract/candidate joins.
    """

    raw_to_canonical: dict[str, str] = {}
    contracts_by_id: dict[str, NLContract] = {}
    raw_contracts: dict[str, NLContract] = {}
    receipts: list[
        IdentityNormalizationReceipt | GroupIdentityNormalizationReceipt
    ] = []
    for contract in response.additional_contracts:
        canonical_id = canonical_contract_id(contract)
        raw_to_canonical[contract.contract_id] = canonical_id
        raw_contracts[contract.contract_id] = contract
        canonical = contract.model_copy(update={"contract_id": canonical_id})
        contracts_by_id.setdefault(canonical_id, canonical)

    recovered_candidate_contracts: dict[int, NLContract] = {}
    for index, candidate in enumerate(response.candidates):
        if candidate.contract_id in raw_contracts:
            continue
        if "-DERIVED-" not in candidate.contract_id:
            continue
        candidate_key = _candidate_contract_reference_key(candidate)
        matches = [
            contract
            for contract in response.additional_contracts
            if _contract_candidate_reference_key(contract) == candidate_key
        ]
        if len(matches) == 1:
            recovered_candidate_contracts[index] = matches[0]

    for contract in response.additional_contracts:
        canonical_id = raw_to_canonical[contract.contract_id]
        recovered_count = sum(
            recovered.contract_id == contract.contract_id
            for recovered in recovered_candidate_contracts.values()
        )
        receipts.append(
            IdentityNormalizationReceipt(
                lens=response.lens,
                raw_contract_id=contract.contract_id,
                canonical_contract_id=canonical_id,
                semantic_key=contract_semantic_key(contract),
                rewritten_candidate_count=sum(
                    candidate.contract_id == contract.contract_id
                    for candidate in response.candidates
                ),
                projected_candidate_identity_count=sum(
                    candidate.contract_id == contract.contract_id
                    for candidate in response.candidates
                ) + recovered_count,
                recovered_candidate_reference_count=recovered_count,
                rewritten_unresolved_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.unresolved
                ),
                rewritten_binding_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.semantic_bindings
                ),
                rewritten_cardinality_binding_count=sum(
                    item.contract_id == contract.contract_id
                    for item in response.cardinality_bindings
                ),
                reason="The runner replaced a branch-local derived identifier and projected referenced candidates onto the contract-authoritative typed semantic identity.",
                basis=f"lens={response.lens}; semantic_key={contract_semantic_key(contract).model_dump(mode='json')}",
            )
        )

    candidates = []
    contracts_by_raw_id = {
        raw_id: contracts_by_id[canonical_id]
        for raw_id, canonical_id in raw_to_canonical.items()
    }
    for index, candidate in enumerate(response.candidates):
        recovered_contract = recovered_candidate_contracts.get(index)
        contract = contracts_by_raw_id.get(candidate.contract_id)
        if contract is None and recovered_contract is not None:
            contract = contracts_by_id[raw_to_canonical[recovered_contract.contract_id]]
        update: dict[str, object] = {
            "contract_id": (
                contract.contract_id if contract is not None else candidate.contract_id
            )
        }
        if contract is not None:
            update.update(
                {
                    "locus_kind": contract.locus_kind,
                    "locus_names": contract.locus_names,
                    "property": contract.property,
                    "violation_direction": contract.violation_direction,
                    "evidence_types": contract.evidence_types,
                }
            )
        candidates.append(candidate.model_copy(update=update))
    unresolved = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.unresolved
    ]
    semantic_bindings = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.semantic_bindings
    ]
    cardinality_bindings = [
        item.model_copy(
            update={"contract_id": raw_to_canonical.get(item.contract_id, item.contract_id)}
        )
        for item in response.cardinality_bindings
    ]
    groups_by_id: dict[str, NLTransitionGroup] = {}
    for group in response.additional_transition_groups:
        canonical_group, alternative_id_map = _canonicalize_transition_group(group)
        groups_by_id.setdefault(canonical_group.group_id, canonical_group)
        receipts.append(
            GroupIdentityNormalizationReceipt(
                lens=response.lens,
                raw_group_id=group.group_id,
                canonical_group_id=canonical_group.group_id,
                semantic_key=transition_group_semantic_key(group),
                alternative_id_map=alternative_id_map,
                reason="The runner replaced branch-local transition-group and alternative IDs with one typed ordered relation identity.",
                basis=f"lens={response.lens}; semantic_key={transition_group_semantic_key(group).model_dump(mode='json')}",
            )
        )
    normalized = response.model_copy(
        update={
            "additional_contracts": list(contracts_by_id.values()),
            "additional_transition_groups": list(groups_by_id.values()),
            "candidates": candidates,
            "unresolved": unresolved,
            "semantic_bindings": semantic_bindings,
            "cardinality_bindings": cardinality_bindings,
        }
    )
    return normalized, tuple(receipts)


def _hash_payload(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()[:20]


def _hint(contract: NLContract, *roles: str) -> ContractBindingHint | None:
    matches = [item for item in contract.binding_hints if item.role in roles]
    return matches[0] if len(matches) == 1 else None


def _state_by_ref(pair: PairInput, ref: str | None) -> StateNode | None:
    return next((item for item in pair.model.states if item.ref == ref), None)


def _state_for_value(pair: PairInput, value: str | None) -> StateNode | None:
    return _state_by_ref(pair, resolve_state_ref(value, pair.model) if value else None)


def _state_by_name(pair: PairInput, name: str | None) -> StateNode | None:
    if not name:
        return None
    matches = [
        item
        for item in pair.model.states
        if name in {item.name, item.canonical_path}
    ]
    return matches[0] if len(matches) == 1 else None


def _source_state_by_name(
    pair: PairInput, name: str | None
) -> SourceInventoryState | None:
    if not name or pair.exact_source_inventory is None:
        return None
    matches = [
        item for item in pair.exact_source_inventory.states if item.name == name
    ]
    return matches[0] if len(matches) == 1 else None


def _source_state_by_id(
    pair: PairInput, source_id: str | None
) -> SourceInventoryState | None:
    if not source_id or pair.exact_source_inventory is None:
        return None
    matches = [
        item
        for item in pair.exact_source_inventory.states
        if item.source_id == source_id
    ]
    return matches[0] if len(matches) == 1 else None


def _source_direct_children(
    pair: PairInput, owner: SourceInventoryState
) -> list[SourceInventoryState]:
    if pair.exact_source_inventory is None:
        return []
    return [
        item
        for item in pair.exact_source_inventory.states
        if item.parent == owner.source_id
    ]


def _source_is_descendant(
    pair: PairInput,
    child: SourceInventoryState,
    owner: SourceInventoryState,
) -> bool:
    """Return exact canonical-source ancestry without interpreting names."""

    inventory = pair.exact_source_inventory
    if inventory is None or child.source_id == owner.source_id:
        return False
    states = {item.source_id: item for item in inventory.states}
    cursor = child.parent
    seen: set[str] = set()
    while cursor and cursor not in seen:
        if cursor == owner.source_id:
            return True
        seen.add(cursor)
        parent = states.get(cursor)
        cursor = parent.parent if parent is not None else None
    return False


def _source_initial_transitions(
    pair: PairInput, owner: SourceInventoryState
) -> list[SourceInventoryTransition]:
    if pair.exact_source_inventory is None:
        return []
    initial_source = f"@initial:{owner.source_id}"
    return [
        item
        for item in pair.exact_source_inventory.transitions
        if item.source == initial_source
    ]


def _inspection_state(pair: PairInput, ref: str) -> InspectionStateFact | None:
    facts = pair.inspection_facts
    return next((item for item in facts.states if item.state_ref == ref), None) if facts else None


def _machine_root(pair: PairInput) -> StateNode | None:
    if pair.inspection_facts and pair.inspection_facts.machine_root_ref:
        return _state_by_ref(pair, pair.inspection_facts.machine_root_ref)
    roots = [item for item in pair.model.states if item.parent is None]
    return roots[0] if len(roots) == 1 else None


def _ancestor_chain(pair: PairInput, state: StateNode) -> list[StateNode]:
    chain = [state]
    cursor = state
    seen = {state.ref}
    while cursor.parent_ref:
        parent = _state_by_ref(pair, cursor.parent_ref)
        if parent is None or parent.ref in seen:
            break
        chain.append(parent)
        seen.add(parent.ref)
        cursor = parent
    return chain


def _is_descendant(pair: PairInput, child: StateNode, owner: StateNode) -> bool:
    return owner.ref in {item.ref for item in _ancestor_chain(pair, child)[1:]}


def _highest_unreachable_scope(pair: PairInput, state: StateNode) -> StateNode | None:
    root = _machine_root(pair)
    candidates = []
    for item in _ancestor_chain(pair, state):
        fact = _inspection_state(pair, item.ref)
        if (
            fact
            and fact.is_composite
            and not fact.reachable_from_initial
            and (root is None or item.ref != root.ref)
        ):
            candidates.append(item)
    return candidates[-1] if candidates else None


def _direct_child_under(pair: PairInput, descendant: StateNode, owner: StateNode) -> StateNode | None:
    chain = _ancestor_chain(pair, descendant)
    for index, item in enumerate(chain):
        if item.ref == owner.ref:
            return chain[index - 1] if index > 0 else None
    return None


def _initial_transitions(pair: PairInput, owner: StateNode | None) -> list[Transition]:
    root = _machine_root(pair)
    owner_refs = {owner.ref} if owner is not None else ({root.ref} if root else set())
    return [
        item
        for item in pair.model.transitions
        if item.source == "[*]" and item.owner_ref in owner_refs
    ]


def _transition_target_ref(pair: PairInput, transition: Transition) -> str | None:
    if pair.inspection_facts:
        row = next(
            (
                item
                for item in pair.inspection_facts.transitions
                if item.transition_ref == transition.ref
            ),
            None,
        )
        if row:
            return row.resolved_target_ref
    target = _state_for_value(pair, transition.target)
    return target.ref if target else None


def _source_refs(contracts: Sequence[NLContract]) -> list[str]:
    return list(dict.fromkeys(ref for contract in contracts for ref in contract.source_refs))


def _derived_contract(
    base: NLContract,
    *,
    locus_kind: ObligationLocusKind,
    locus_names: Sequence[str],
    property_name: ObligationProperty,
    state_role: StateSemanticRole | None,
    expected_direction: ExpectedDirection,
    violation_direction: ViolationDirection,
    evidence_types: Sequence[EvidenceType],
    normative_statement: str,
    scope: str,
    source_refs: Sequence[str],
    reason: str,
    basis: str,
    cardinality_requirement: CardinalityRequirement | None = None,
    quote: str | None = None,
    binding_hints: Sequence[ContractBindingHint] | None = None,
) -> NLContract:
    resolved_hints = (
        tuple(binding_hints)
        if binding_hints is not None
        else base.binding_hints
    )
    contract = NLContract(
        contract_id=f"NL-CONTRACT-{base.segment_id}-DERIVED-PENDING",
        segment_id=base.segment_id,
        quote=quote if quote is not None else base.quote,
        normative_statement=normative_statement,
        locus_kind=locus_kind,
        locus_names=tuple(locus_names),
        property=property_name,
        state_role=state_role,
        expected_direction=expected_direction,
        violation_direction=violation_direction,
        evidence_types=tuple(dict.fromkeys(evidence_types)),
        binding_hints=resolved_hints,
        cardinality_requirement=cardinality_requirement,
        scope=scope,
        source_refs=tuple(
            dict.fromkeys(
                [
                    *source_refs,
                    *[
                        hint.source_ref
                        for hint in resolved_hints
                        if hint.source_ref
                    ],
                ]
            )
        ),
        reason=reason,
        basis=basis,
    )
    return contract.model_copy(update={"contract_id": canonical_contract_id(contract)})


def _candidate(
    contract: NLContract,
    *,
    title: str,
    predicate_id: str | None,
    predicate_inputs: dict[str, object],
    element_refs: Sequence[str],
    source_refs: Sequence[str],
    expected: str,
    observed: str,
    strongest_rebuttal: str,
    reason: str,
    basis: str,
) -> CandidateIssue:
    return CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title=title,
        requirement_quote=contract.quote,
        predicate_id=predicate_id,
        predicate_inputs=predicate_inputs,
        element_refs=list(dict.fromkeys(element_refs)),
        source_refs=list(dict.fromkeys(source_refs)),
        expected=expected,
        observed=observed,
        strongest_rebuttal=strongest_rebuttal,
        reason=reason,
        basis=basis,
    )


class _Builder:
    def __init__(
        self,
        pair: PairInput,
        existing: Sequence[CandidateIssue],
        contracts_by_id: Mapping[str, NLContract],
    ) -> None:
        self.pair = pair
        self.obligations: list[FrontierObligation] = []
        self.checks: list[FrontierCheckReceipt] = []
        self.seen = {
            contract_semantic_key_from_candidate(candidate)
            for candidate in existing
            if (
                (contract := contracts_by_id.get(candidate.contract_id)) is not None
                and candidate_preserves_contract_identity(candidate, contract)
            )
        }
        self.obligation_index: dict[tuple[object, ...], int] = {}
        self.superseded_candidate_contract_ids: list[str] = []

    def add(
        self,
        kind: FrontierKind,
        source_contract_ids: Sequence[str],
        contract: NLContract,
        candidate: CandidateIssue,
        *,
        reason: str,
        basis: str,
        root_refs: Sequence[str] = (),
        marked_refs: Sequence[str] = (),
    ) -> None:
        identity = contract_semantic_key_from_candidate(candidate)
        if identity in self.seen:
            existing_index = self.obligation_index.get(identity)
            if existing_index is not None:
                existing = self.obligations[existing_index]
                merged_candidate = existing.candidate.model_copy(
                    update={
                        "element_refs": list(
                            dict.fromkeys(
                                [*existing.candidate.element_refs, *candidate.element_refs]
                            )
                        ),
                        "source_refs": list(
                            dict.fromkeys(
                                [*existing.candidate.source_refs, *candidate.source_refs]
                            )
                        ),
                        "basis": (
                            f"{existing.candidate.basis}; supporting_contract_ids="
                            f"{list(dict.fromkeys([*existing.source_contract_ids, *source_contract_ids]))}"
                        ),
                    }
                )
                self.obligations[existing_index] = existing.model_copy(
                    update={
                        "source_contract_ids": tuple(
                            dict.fromkeys(
                                [*existing.source_contract_ids, *source_contract_ids]
                            )
                        ),
                        "candidate": merged_candidate,
                        "basis": (
                            f"{existing.basis}; merged duplicate typed frontier "
                            f"from {list(source_contract_ids)}"
                        ),
                    }
                )
            self.checks.append(
                self.receipt(
                    kind,
                    source_contract_ids,
                    status="not_applicable",
                    contract=contract,
                    model_refs=candidate.element_refs,
                    source_refs=candidate.source_refs,
                    root_refs=root_refs,
                    marked_refs=marked_refs,
                    reason="An existing candidate or frontier obligation already carries this exact typed semantic identity.",
                    basis="typed locus kind, locus names, property, and violation direction equality; duplicate refs remain supporting evidence",
                )
            )
            return
        self.seen.add(identity)
        frontier_id = f"frontier:{kind}:{_hash_payload([contract.contract_id, candidate.element_refs])}"
        obligation = FrontierObligation(
            frontier_id=frontier_id,
            kind=kind,
            source_contract_ids=tuple(source_contract_ids),
            contract=contract,
            candidate=candidate,
            reason=reason,
            basis=basis,
        )
        self.obligations.append(obligation)
        self.obligation_index[identity] = len(self.obligations) - 1
        self.checks.append(
            self.receipt(
                kind,
                source_contract_ids,
                status="candidate",
                contract=contract,
                model_refs=candidate.element_refs,
                source_refs=candidate.source_refs,
                root_refs=root_refs,
                marked_refs=marked_refs,
                reason=reason,
                basis=basis,
            )
        )

    def receipt(
        self,
        kind: FrontierKind,
        source_contract_ids: Sequence[str],
        *,
        status: Literal["candidate", "satisfied", "unresolved", "not_applicable"],
        contract: NLContract | None = None,
        model_refs: Sequence[str] = (),
        source_refs: Sequence[str] = (),
        root_refs: Sequence[str] = (),
        marked_refs: Sequence[str] = (),
        reason: str,
        basis: str,
    ) -> FrontierCheckReceipt:
        return FrontierCheckReceipt(
            check_id=f"frontier-check:{kind}:{_hash_payload([list(source_contract_ids), list(model_refs), list(root_refs), list(marked_refs), status])}",
            kind=kind,
            source_contract_ids=tuple(source_contract_ids),
            canonical_contract_id=contract.contract_id if contract else None,
            status=status,
            model_refs=tuple(dict.fromkeys(model_refs)),
            root_refs=tuple(dict.fromkeys(root_refs)),
            marked_refs=tuple(dict.fromkeys(marked_refs)),
            source_refs=tuple(dict.fromkeys(source_refs)),
            reason=reason,
            basis=basis,
        )


def contract_semantic_key_from_candidate(candidate: CandidateIssue) -> tuple[object, ...]:
    return (
        candidate.locus_kind,
        candidate.locus_names,
        candidate.property,
        candidate.violation_direction,
    )


def candidate_preserves_contract_identity(
    candidate: CandidateIssue,
    contract: NLContract,
) -> bool:
    """Return whether a candidate exactly preserves its referenced contract key."""

    return (
        candidate.locus_kind == contract.locus_kind
        and tuple(candidate.locus_names) == tuple(contract.locus_names)
        and candidate.property == contract.property
        and candidate.violation_direction == contract.violation_direction
    )


def _materialize_containment(
    builder: _Builder,
    contracts: Sequence[NLContract],
    groups: Sequence[NLTransitionGroup],
) -> None:
    pair = builder.pair
    violations: list[tuple[NLContract, CandidateIssue, StateNode, StateNode]] = []
    for contract in contracts:
        if contract.property != "containment":
            continue
        owner = _state_for_value(pair, (_hint(contract, "owner") or _hint(contract, "scope")).value if (_hint(contract, "owner") or _hint(contract, "scope")) else None)
        child_hint = _hint(contract, "target") or _hint(contract, "state")
        child = _state_for_value(pair, child_hint.value if child_hint else None)
        if owner is None or child is None:
            builder.checks.append(
                builder.receipt(
                    "containment",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The typed owner or child does not resolve to one exact closed-model state.",
                    basis="contract binding_hints and exact ModelIR state identity",
                )
            )
            continue
        if _is_descendant(pair, child, owner):
            builder.checks.append(
                builder.receipt(
                    "containment",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=(owner.ref, child.ref),
                    source_refs=contract.source_refs,
                    reason="The exact child ancestry contains the required owner.",
                    basis="owned ModelIR parent chain",
                )
            )
            continue
        actual_chain = [item.name for item in _ancestor_chain(pair, child)]
        candidate = _candidate(
            contract,
            title=f"{child.name} is outside required owner {owner.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(child.ref, owner.ref),
            source_refs=contract.source_refs,
            expected=contract.normative_statement,
            observed=f"The exact closed-model ancestry of {child.name} is {actual_chain}, which does not include {owner.name}.",
            strongest_rebuttal="A transition between the two states would not establish the required containment relation.",
            reason="The LLM-established containment contract binds both states exactly, and the complete parent chain refutes the required owner relation.",
            basis=f"contract={contract.contract_id}; child_ref={child.ref}; owner_ref={owner.ref}; model={pair.model.algorithm_version}",
        )
        violations.append((contract, candidate, owner, child))

    violations_by_relation: dict[
        tuple[str, str], list[tuple[NLContract, CandidateIssue, StateNode, StateNode]]
    ] = defaultdict(list)
    for row in violations:
        violations_by_relation[(row[2].ref, row[3].ref)].append(row)

    consumed_contract_ids: set[str] = set()
    seen_aggregate_relations: set[tuple[str, tuple[str, ...]]] = set()
    for group in groups:
        if len(group.alternatives) < 2:
            continue
        member_names = tuple(
            dict.fromkeys(
                [group.source_name, *[item.target_name for item in group.alternatives]]
            )
        )
        if len(member_names) < 3:
            continue
        members = [_state_for_value(pair, name) for name in member_names]
        if any(member is None for member in members):
            continue
        exact_members = [member for member in members if member is not None]
        owner_sets = [
            {
                owner_ref
                for owner_ref, child_ref in violations_by_relation
                if child_ref == member.ref
            }
            for member in exact_members
        ]
        if not owner_sets or any(not owner_refs for owner_refs in owner_sets):
            continue
        common_owner_refs = set.intersection(*owner_sets)
        for owner_ref in sorted(common_owner_refs):
            relation_key = (owner_ref, tuple(member.ref for member in exact_members))
            if relation_key in seen_aggregate_relations:
                continue
            owner = _state_by_ref(pair, owner_ref)
            if owner is None or any(member.ref == owner.ref for member in exact_members):
                continue
            relation_rows = [
                violations_by_relation[(owner_ref, member.ref)]
                for member in exact_members
            ]
            primary_rows = [rows[0] for rows in relation_rows]
            source_contract_ids = tuple(
                dict.fromkeys(
                    row[0].contract_id
                    for rows in relation_rows
                    for row in rows
                )
            )
            base = primary_rows[0][0]
            source_refs = tuple(
                dict.fromkeys(
                    [
                        *_source_refs([row[0] for row in primary_rows]),
                        *group.source_refs,
                    ]
                )
            )
            aggregate_contract = _derived_contract(
                base,
                locus_kind="scope",
                locus_names=(owner.name, *[member.name for member in exact_members]),
                property_name="containment",
                state_role=None,
                expected_direction="must_be_contained",
                violation_direction="wrong_scope",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "containment_fact",
                    "semantic_comparison",
                ),
                normative_statement=(
                    f"The complete transition group rooted at {group.source_name} must remain "
                    f"inside enclosing owner {owner.name}: "
                    f"{[member.name for member in exact_members]}."
                ),
                scope=(
                    f"Complete containment scope of transition group {group.group_id} "
                    f"under {owner.name}"
                ),
                source_refs=source_refs,
                reason=(
                    "Separate typed containment contracts place the transition-group "
                    "source and every alternative target under one exact enclosing owner; "
                    "the group supplies the complete enumerated member boundary."
                ),
                basis=(
                    f"transition_group_id={group.group_id}; owner_ref={owner.ref}; "
                    f"source_contract_ids={list(source_contract_ids)}; "
                    f"member_refs={[member.ref for member in exact_members]}"
                ),
            ).model_copy(
                update={
                    "quote": "\n".join(
                        f"[{row[0].segment_id}] {row[0].quote}"
                        for row in primary_rows
                    ),
                    "binding_hints": tuple(
                        hint
                        for row in primary_rows
                        for hint in row[0].binding_hints
                    ),
                }
            )
            aggregate_candidate = _candidate(
                aggregate_contract,
                title=f"{owner.name} is missing its complete required state hierarchy",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(
                    owner.ref,
                    *[member.ref for member in exact_members],
                ),
                source_refs=source_refs,
                expected=aggregate_contract.normative_statement,
                observed=" ".join(row[1].observed for row in primary_rows),
                strongest_rebuttal=(
                    "A transition among root-level states does not establish that the "
                    "complete source-and-alternative set is contained by the required owner."
                ),
                reason=(
                    "Every independently established member of one complete transition "
                    "group has an exact ancestry that excludes the same required owner."
                ),
                basis=aggregate_contract.basis,
            )
            builder.add(
                "aggregate_containment",
                source_contract_ids,
                aggregate_contract,
                aggregate_candidate,
                reason=(
                    "A typed transition group and complete same-owner containment contracts "
                    "establish one full-scope hierarchy violation."
                ),
                basis=(
                    f"transition_group_id={group.group_id}; exact owner/member ModelIR "
                    "ancestry for every explicitly contracted group member"
                ),
            )
            consumed_contract_ids.update(source_contract_ids)
            seen_aggregate_relations.add(relation_key)

    for contract, candidate, _owner, _child in violations:
        if contract.contract_id in consumed_contract_ids:
            continue
        builder.add(
            "containment",
            (contract.contract_id,),
            contract,
            candidate,
            reason="A typed containment obligation is refuted by the exact ModelIR parent chain.",
            basis="contract binding hints plus complete owned hierarchy",
        )


def _materialize_cardinality(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
    existing: Sequence[CandidateIssue],
) -> None:
    pair = builder.pair
    for contract in contracts:
        if contract.property != "cardinality":
            continue
        requirement = contract.cardinality_requirement
        if requirement is None:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The cardinality contract has no typed required count and member domain, so free text is not parsed to manufacture them.",
                    basis="NLContract.cardinality_requirement is null",
                )
            )
            continue

        binding_rows = [
            binding
            for response in grounding_responses
            for binding in response.cardinality_bindings
            if binding.contract_id == contract.contract_id
        ]
        exact_bindings = [
            binding for binding in binding_rows if binding.status == "exact"
        ]
        exact_binding_keys = {
            (
                binding.member_domain,
                binding.owner_source_id,
                binding.owner_model_ref,
            )
            for binding in exact_bindings
        }
        selected_binding: CardinalityDomainBinding | None = None
        effective_requirement = requirement
        if requirement.member_domain == "unresolved":
            if not exact_bindings:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="No grounding lens selected one exact primary cardinality member domain and owner.",
                        basis=(
                            "member_domain=unresolved; cardinality_binding_statuses="
                            f"{[item.status for item in binding_rows]}; no free-text or name-shape fallback is permitted"
                        ),
                    )
                )
                continue
            if len(exact_binding_keys) != 1:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="The grounding lenses selected conflicting exact cardinality domains or owners, so the frontier cannot choose one by branch order.",
                        basis=f"exact_binding_keys={sorted(exact_binding_keys)}",
                    )
                )
                continue
            selected_binding = exact_bindings[0]
            alternative_reading = next(
                (
                    binding.alternative_reading
                    for binding in exact_bindings
                    if binding.alternative_reading is not None
                ),
                requirement.alternative_reading,
            )
            effective_requirement = requirement.model_copy(
                update={
                    "member_domain": selected_binding.member_domain,
                    "alternative_reading": alternative_reading,
                    "reason": "Grounding selected one primary typed member domain from supplied NL/source semantics while retaining any competing competent reading for D.",
                    "basis": "numbered NL CardinalityRequirement plus exact CardinalityDomainBinding; observed count was not used to choose the domain",
                }
            )
        else:
            agreeing_bindings = [
                binding
                for binding in exact_bindings
                if binding.member_domain == requirement.member_domain
            ]
            agreeing_keys = {
                (binding.owner_source_id, binding.owner_model_ref)
                for binding in agreeing_bindings
            }
            if agreeing_bindings and len(agreeing_keys) != 1:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        source_refs=contract.source_refs,
                        reason="The grounding lenses disagree about the exact owner of the contract-selected cardinality domain.",
                        basis=f"member_domain={requirement.member_domain}; agreeing_owner_keys={sorted(agreeing_keys)}",
                    )
                )
                continue
            if len(agreeing_keys) == 1:
                selected_binding = agreeing_bindings[0]
                if (
                    effective_requirement.alternative_reading is None
                    and any(
                        binding.alternative_reading is not None
                        for binding in agreeing_bindings
                    )
                ):
                    effective_requirement = requirement.model_copy(
                        update={
                            "alternative_reading": next(
                                binding.alternative_reading
                                for binding in agreeing_bindings
                                if binding.alternative_reading is not None
                            )
                        }
                    )

        if effective_requirement.member_domain not in {
            "direct_child_states",
            "concurrent_regions",
            "explicit_named_members",
        }:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="This frontier currently has no exact inventory projection for the contract's selected member domain.",
                    basis=f"member_domain={effective_requirement.member_domain}; no free-text or name-shape fallback is permitted",
                )
            )
            continue

        if selected_binding is not None:
            bound_owner = _state_by_ref(pair, selected_binding.owner_model_ref)
            source_owner = _source_state_by_id(
                pair, selected_binding.owner_source_id
            )
            owner_rows = (
                [
                    (
                        bound_owner,
                        source_owner,
                        _source_direct_children(pair, source_owner),
                    )
                ]
                if bound_owner is not None and source_owner is not None
                else []
            )
            bound_states = [bound_owner] if bound_owner is not None else []
        else:
            bound_states = _contract_state_refs(pair, contract)
            for candidate in existing:
                if (
                    candidate.contract_id == contract.contract_id
                    and candidate.property == "cardinality"
                ):
                    bound_states.extend(_candidate_state_refs(pair, candidate))
            bound_states = list({item.ref: item for item in bound_states}.values())

            structural_owner_rows: list[
                tuple[StateNode, SourceInventoryState, list[SourceInventoryState]]
            ] = []
            bound_source_ids = {
                source_state.source_id
                for state in bound_states
                if (source_state := _source_state_by_name(pair, state.name))
                is not None
            }
            for state in bound_states:
                source_owner = _source_state_by_name(pair, state.name)
                if source_owner is None:
                    continue
                children = _source_direct_children(pair, source_owner)
                if children:
                    structural_owner_rows.append((state, source_owner, children))
            linked_owner_rows = [
                row
                for row in structural_owner_rows
                if any(child.source_id in bound_source_ids for child in row[2])
            ]
            owner_rows = (
                linked_owner_rows
                if linked_owner_rows
                else structural_owner_rows
                if len(structural_owner_rows) == 1
                else []
            )
        if len(owner_rows) != 1:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="unresolved",
                    model_refs=[item.ref for item in bound_states],
                    source_refs=contract.source_refs,
                    reason="The typed binding does not identify one exact source/model owner for the selected finite cardinality member domain.",
                    basis=(
                        f"owner_candidate_count={len(owner_rows)}; "
                        f"cardinality_binding_id={selected_binding.binding_id if selected_binding else None}; "
                        f"member_domain={effective_requirement.member_domain}; exact source parent relations only"
                    ),
                )
            )
            continue

        owner, source_owner, direct_children = owner_rows[0]
        member_domain = effective_requirement.member_domain
        if member_domain == "concurrent_regions":
            source_ir = pair.canonical_source_ir
            if source_ir is None:
                builder.checks.append(
                    builder.receipt(
                        "cardinality",
                        (contract.contract_id,),
                        status="unresolved",
                        model_refs=(owner.ref,),
                        source_refs=contract.source_refs,
                        reason="The exact owner is bound, but canonical concurrent-region inventory is unavailable.",
                        basis=(
                            f"owner={source_owner.source_id}; member_domain=concurrent_regions; "
                            "canonical_source_ir=null"
                        ),
                    )
                )
                continue
            region_rows = [
                region
                for region in source_ir.model.concurrent_regions
                if region.owner_scope == source_owner.source_id
            ]
            if region_rows:
                actual_count = len(region_rows)
                source_member_ids = tuple(
                    dict.fromkeys(
                        state_id
                        for region in region_rows
                        for state_id in region.state_ids
                    )
                )
                source_members = [
                    member
                    for source_id in source_member_ids
                    if (member := _source_state_by_id(pair, source_id)) is not None
                ]
                region_source_refs = tuple(
                    dict.fromkeys(
                        ref
                        for region in region_rows
                        for ref in (
                            *region.separator_before_raw_refs,
                            *region.separator_after_raw_refs,
                        )
                    )
                )
                inventory_ids = [region.id for region in region_rows]
                observed = (
                    f"For the normative scope '{contract.scope}', the primary "
                    f"concurrent-region reading has {actual_count} explicit canonical "
                    f"UML regions under {source_owner.source_id}: {inventory_ids}."
                )
                inventory_basis = (
                    f"explicit_region_ids={inventory_ids}; "
                    f"separator_refs={list(region_source_refs)}"
                )
            else:
                actual_count = 1 if direct_children else 0
                source_members = direct_children
                region_source_refs = ()
                inventory_ids = (
                    [f"implicit-region:{source_owner.source_id}"]
                    if direct_children
                    else []
                )
                observed = (
                    f"For the normative scope '{contract.scope}', the primary "
                    f"concurrent-region reading has {actual_count} implicit UML region "
                    f"under {source_owner.source_id}: no exact separator-derived region "
                    f"rows exist and direct_children={[item.source_id for item in direct_children]}."
                )
                inventory_basis = (
                    "explicit_region_ids=[]; implicit_region_count="
                    f"{actual_count}; direct_children="
                    f"{[item.source_id for item in direct_children]}"
                )
            domain_phrase = "canonical UML concurrent regions"
            scope_phrase = (
                f"the authored UML region partition of {owner.name}; a non-empty "
                "composite without separators has one implicit region"
            )
            requirement_reason = (
                "The NL contract establishes a finite structural-region member-domain "
                "reading whose count can be compared with exact canonical separators "
                "and the implicit single-region rule."
            )
            requirement_basis = (
                "typed CardinalityRequirement plus exact canonical concurrent-region "
                "rows and source direct-child inventory"
            )
            satisfied_reason = (
                "The exact canonical UML region inventory, including the implicit "
                "single-region rule when no separators exist, has the required finite cardinality."
            )
            candidate_reason = (
                "The contract's scope, required count, and primary structural-region "
                "domain are preserved, while canonical separators plus the implicit "
                "single-region rule establish a different finite count and D retains "
                "the operating-state alternative reading."
            )
            frontier_basis = (
                "CardinalityRequirement and canonical source concurrent-region inventory"
            )
        elif member_domain == "explicit_named_members":
            actual_count = len(direct_children)
            source_members = direct_children
            region_source_refs = ()
            inventory_ids = [item.name for item in direct_children]
            observed = (
                f"For the normative scope '{contract.scope}', the primary "
                f"explicitly named-member reading has {actual_count} exact "
                f"source members under {source_owner.source_id}: {inventory_ids}."
            )
            inventory_basis = (
                f"member_names={inventory_ids}; "
                f"source_ids={[item.source_id for item in direct_children]}"
            )
            domain_phrase = "exact explicitly named members"
            scope_phrase = (
                f"the exact source members under {owner.name} enumerated by the "
                "normative contract"
            )
            requirement_reason = (
                "The NL contract explicitly enumerates a finite named member "
                "domain, and the complete exact source inventory supplies the "
                "owner's members for deterministic comparison."
            )
            requirement_basis = (
                "typed CardinalityRequirement plus exact source owner/member "
                "rows for the explicit named-member domain"
            )
            satisfied_reason = (
                "The complete exact source inventory for the explicitly named "
                "member domain has the required finite cardinality."
            )
            candidate_reason = (
                "The contract's exact owner, required count, and explicit named "
                "member domain are preserved, while the complete source "
                "inventory exposes the observed extra or missing member."
            )
            frontier_basis = (
                "CardinalityRequirement and exact source inventory for explicit "
                "named members"
            )
        else:
            actual_count = len(direct_children)
            source_members = direct_children
            region_source_refs = ()
            inventory_ids = [item.source_id for item in direct_children]
            observed = (
                f"For the normative scope '{contract.scope}', the primary direct-child "
                f"reading has {actual_count} exact author-source children under "
                f"{source_owner.source_id}: {inventory_ids}."
            )
            inventory_basis = f"members={inventory_ids}"
            domain_phrase = "exact direct child states"
            scope_phrase = f"the direct authored children of {owner.name}"
            requirement_reason = (
                "The NL contract establishes a finite direct-child member-domain reading "
                "whose count can be compared with the complete exact source inventory."
            )
            requirement_basis = (
                "typed CardinalityRequirement plus exact source parent/member rows"
            )
            satisfied_reason = (
                "The complete exact author-source direct-child inventory has the required finite cardinality."
            )
            candidate_reason = (
                "The contract's operating scope, required count, and primary direct-child "
                "member domain are preserved, while the complete source inventory "
                "establishes a different finite count and D retains any alternative reading."
            )
            frontier_basis = (
                "CardinalityRequirement and canonical source direct-parent inventory"
            )

        source_refs = tuple(
            dict.fromkeys(
                [
                    *contract.source_refs,
                    source_owner.raw_ref,
                    *[member.raw_ref for member in source_members],
                    *region_source_refs,
                ]
            )
        )
        model_members = [
            state
            for member in source_members
            if (state := _state_by_name(pair, member.name)) is not None
        ]
        model_refs = [owner.ref, *[item.ref for item in model_members]]
        if actual_count == effective_requirement.required_count:
            builder.checks.append(
                builder.receipt(
                    "cardinality",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=model_refs,
                    source_refs=source_refs,
                    reason=satisfied_reason,
                    basis=(
                        f"owner={source_owner.source_id}; member_domain={member_domain}; "
                        f"required={effective_requirement.required_count}; actual={actual_count}; "
                        f"{inventory_basis}"
                    ),
                )
            )
            continue

        mismatch_direction: ViolationDirection = (
            "missing"
            if actual_count < effective_requirement.required_count
            else "extra"
        )
        derived = _derived_contract(
            contract,
            locus_kind="composite",
            locus_names=(owner.name,),
            property_name="cardinality",
            state_role=contract.state_role,
            expected_direction="must_cover",
            violation_direction=mismatch_direction,
            evidence_types=("source_identity", "closed_model_inventory", "containment_fact", "semantic_comparison"),
            normative_statement=(
                f"Within {contract.scope}, {owner.name} must realize "
                f"{effective_requirement.required_count} {effective_requirement.member_concept}; "
                f"the primary typed reading counts {domain_phrase}."
            ),
            scope=f"{contract.scope}; primary member domain is {scope_phrase}",
            source_refs=source_refs,
            reason=requirement_reason,
            basis=requirement_basis,
            cardinality_requirement=effective_requirement,
        )
        candidate = _candidate(
            derived,
            title=(
                f"{owner.name} realizes {actual_count}, not "
                f"{effective_requirement.required_count}, {effective_requirement.member_concept} "
                f"under the {member_domain} reading"
            ),
            predicate_id=None,
            predicate_inputs={},
            element_refs=model_refs,
            source_refs=source_refs,
            expected=derived.normative_statement,
            observed=observed,
            strongest_rebuttal=(
                effective_requirement.alternative_reading
                or "No competing member-domain reading is recorded in the supplied cardinality contract."
            ),
            reason=candidate_reason,
            basis=(
                f"contract={contract.contract_id}; owner={source_owner.source_id}; "
                f"member_domain={member_domain}; violation_direction={mismatch_direction}; "
                f"required={effective_requirement.required_count}; actual={actual_count}; "
                f"cardinality_binding_id={selected_binding.binding_id if selected_binding else None}; "
                f"{inventory_basis}"
            ),
        )
        builder.add(
            "cardinality",
            (contract.contract_id,),
            derived,
            candidate,
            reason="A typed finite cardinality requirement differs from the complete exact source member inventory.",
            basis=frontier_basis,
        )
        if contract.contract_id not in builder.superseded_candidate_contract_ids:
            builder.superseded_candidate_contract_ids.append(contract.contract_id)


def _materialize_malformed_source_initial_entries(
    builder: _Builder,
    contracts: Sequence[NLContract],
) -> None:
    """Materialize exact self-targeting or out-of-owner source initial edges."""

    pair = builder.pair
    if pair.exact_source_inventory is None:
        return
    for base in contracts:
        if base.property != "initial_entry":
            continue
        target_hint = _hint(base, "target") or _hint(base, "state")
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        source_owner = _source_state_by_name(pair, target.name if target else None)
        if (
            target is None
            or source_owner is None
            or source_owner.kind != "composite"
        ):
            continue
        source_initial = _source_initial_transitions(pair, source_owner)
        invalid_rows: list[
            tuple[SourceInventoryTransition, SourceInventoryState]
        ] = []
        for transition in source_initial:
            source_target = _source_state_by_id(pair, transition.target)
            if source_target is None:
                continue
            if not _source_is_descendant(pair, source_target, source_owner):
                invalid_rows.append((transition, source_target))
        if not invalid_rows:
            continue

        model_initial = _initial_transitions(pair, target)
        model_target_refs = tuple(
            ref
            for transition in model_initial
            if (ref := _transition_target_ref(pair, transition))
        )
        owner_hint = ContractBindingHint(
            role="owner",
            value=target.name,
            source_ref=base.segment_id,
            reason="The NL initial-state contract binds the exact composite whose owner-local source entry is audited.",
            basis=f"anchor_contract={base.contract_id}; owner_ref={target.ref}; source_owner={source_owner.source_id}",
        )
        source_refs = tuple(
            dict.fromkeys(
                [
                    *base.source_refs,
                    source_owner.raw_ref,
                    *[transition.raw_ref for transition, _ in invalid_rows],
                ]
            )
        )
        derived = _derived_contract(
            base,
            locus_kind="composite",
            locus_names=(target.name,),
            property_name="initial_entry",
            state_role="initial_state",
            expected_direction="must_enter",
            violation_direction="wrong_target",
            evidence_types=(
                "source_identity",
                "closed_model_inventory",
                "initial_entry_fact",
                "transition_fact",
                "containment_fact",
            ),
            normative_statement=(
                f"The owner-local initial edge of composite {target.name} must enter "
                "a state strictly inside that composite, never the owner itself or "
                "a state outside its subtree."
            ),
            scope=f"Owner-local initialization of {target.name}",
            source_refs=source_refs,
            reason=(
                "The NL activates this exact composite, and the canonical author "
                "source exposes its complete owner-local initial relation."
            ),
            basis=(
                "typed initial-state anchor plus exact canonical-source owner, target, "
                "and parent identities"
            ),
        ).model_copy(update={"binding_hints": (owner_hint,)})
        derived = derived.model_copy(
            update={"contract_id": canonical_contract_id(derived)}
        )
        source_relations = [
            f"{transition.source}->{source_target.source_id}"
            for transition, source_target in invalid_rows
        ]
        model_targets = [transition.target for transition in model_initial]
        candidate = _candidate(
            derived,
            title=f"{target.name} has a malformed owner-local initial target",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                target.ref,
                *[transition.ref for transition in model_initial],
                *model_target_refs,
            ),
            source_refs=source_refs,
            expected=derived.normative_statement,
            observed=(
                f"Canonical source owner-local initial relations are {source_relations}; "
                f"the closed model records owner-local targets {model_targets}."
            ),
            strongest_rebuttal=(
                "A separate root entry into the composite activates only the outer "
                "state and cannot repair a self-targeting or out-of-subtree owner-local entry."
            ),
            reason=(
                "At least one exact owner-local source initial edge targets the owner "
                "itself or another state that is not its descendant."
            ),
            basis=(
                f"source_owner={source_owner.source_id}; "
                f"source_initial_refs={[row.raw_ref for row, _ in invalid_rows]}; "
                f"model_initial_refs={[row.ref for row in model_initial]}; "
                f"model_target_refs={list(model_target_refs)}"
            ),
        )
        builder.add(
            "owner_initial_entry",
            (base.contract_id,),
            derived,
            candidate,
            reason="An exact canonical-source owner-local initial edge leaves the strict descendant target domain.",
            basis="typed composite activation anchor and exact source/model initial inventories",
        )


def _materialize_initial_entries(
    builder: _Builder,
    contracts: Sequence[NLContract],
    groups: Sequence[NLTransitionGroup],
) -> None:
    _materialize_malformed_source_initial_entries(builder, contracts)
    pair = builder.pair
    violations: list[
        tuple[NLContract, NLContract, CandidateIssue, StateNode | None, StateNode]
    ] = []
    for contract in contracts:
        if contract.property != "initial_entry":
            continue
        target_hint = _hint(contract, "target") or _hint(contract, "state")
        owner_hint = _hint(contract, "owner") or _hint(contract, "scope")
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        owner = _state_for_value(pair, owner_hint.value if owner_hint else None)
        owner_is_root = contract.locus_kind == "model"
        if target is None or (owner is None and not owner_is_root):
            builder.checks.append(
                builder.receipt(
                    "owner_initial_entry",
                    (contract.contract_id,),
                    status="unresolved",
                    source_refs=contract.source_refs,
                    reason="The typed initial-entry target or owner does not resolve exactly.",
                    basis="contract owner/target binding hints and ModelIR identity",
                )
            )
            continue
        initial = _initial_transitions(pair, owner)
        matching = [item for item in initial if _transition_target_ref(pair, item) == target.ref]
        unconditional = [item for item in matching if not item.triggers and not item.guard]
        refs = [target.ref]
        if owner:
            refs.append(owner.ref)
        refs.extend(item.ref for item in initial)
        refs.extend(ref for item in initial if (ref := _transition_target_ref(pair, item)))
        if unconditional:
            builder.checks.append(
                builder.receipt(
                    "owner_initial_entry",
                    (contract.contract_id,),
                    status="satisfied",
                    contract=contract,
                    model_refs=refs,
                    source_refs=contract.source_refs,
                    reason="An unconditional initial pseudostate edge enters the exact required target in the required owner scope.",
                    basis="owned scoped transition inventory",
                )
            )
            continue
        observed_targets = [item.target for item in initial]
        normalized_contract = _derived_contract(
            contract,
            locus_kind="model" if owner_is_root else "composite",
            locus_names=(target.name,) if owner_is_root else (owner.name, target.name),
            property_name="initial_entry",
            state_role=contract.state_role,
            expected_direction="must_enter",
            violation_direction="missing",
            evidence_types=contract.evidence_types,
            normative_statement=contract.normative_statement,
            scope=contract.scope,
            source_refs=contract.source_refs,
            reason="The deterministic frontier normalizes owner-level missing-edge and wrong-current-target observations to one exact required default-entry obligation.",
            basis="typed owner/target binding and complete owner-local initial-transition inventory",
        )
        candidate = _candidate(
            normalized_contract,
            title=(
                f"Required entry to {target.name} is not the unconditional default "
                f"for {owner.name if owner else 'Model'}"
                if matching
                else f"{owner.name if owner else 'Model'} lacks default entry to {target.name}"
            ),
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=contract.source_refs,
            expected=contract.normative_statement,
            observed=(
                f"The exact owner-local initial transitions target {observed_targets}; "
                f"matching edges to {target.name} are conditional={bool(matching)}."
            ),
            strongest_rebuttal="A child-region initial edge or a guarded routing edge does not satisfy this exact owner-local default-entry contract.",
            reason="The typed owner and target resolve exactly, but no unconditional owner-local initial edge enters the required target.",
            basis=f"contract={contract.contract_id}; target_ref={target.ref}; owner_ref={owner.ref if owner else 'root'}; initial_refs={[item.ref for item in initial]}",
        )
        violations.append(
            (contract, normalized_contract, candidate, owner, target)
        )

    rows_by_owner_ref: dict[
        str,
        list[tuple[NLContract, NLContract, CandidateIssue, StateNode, StateNode]],
    ] = defaultdict(list)
    individual: list[
        tuple[NLContract, NLContract, CandidateIssue, StateNode | None, StateNode]
    ] = [row for row in violations if row[3] is None]
    for contract, normalized_contract, candidate, owner, target in violations:
        if owner is not None:
            rows_by_owner_ref[owner.ref].append(
                (contract, normalized_contract, candidate, owner, target)
            )

    aggregate_owner_sets: list[tuple[tuple[str, ...], NLTransitionGroup]] = []
    for group in groups:
        owners = [
            _state_for_value(pair, alternative.target_name)
            for alternative in group.alternatives
        ]
        if any(owner is None for owner in owners):
            continue
        owner_refs = tuple(
            dict.fromkeys(owner.ref for owner in owners if owner is not None)
        )
        if len(owner_refs) < 2 or any(
            owner_ref not in rows_by_owner_ref for owner_ref in owner_refs
        ):
            continue
        parents = {
            row[3].parent
            for owner_ref in owner_refs
            for row in rows_by_owner_ref[owner_ref]
        }
        if len(parents) != 1:
            continue
        aggregate_owner_sets.append((owner_refs, group))

    aggregate_owner_sets.sort(
        key=lambda item: (-len(item[0]), item[0], item[1].group_id)
    )
    consumed_contract_ids: set[str] = set()
    for owner_refs, group in aggregate_owner_sets:
        rows = [
            row
            for owner_ref in owner_refs
            for row in rows_by_owner_ref[owner_ref]
            if row[0].contract_id not in consumed_contract_ids
        ]
        if {row[3].ref for row in rows} != set(owner_refs):
            continue
        source_contract_ids = tuple(
            dict.fromkeys(row[0].contract_id for row in rows)
        )
        owner_target_rows = list(
            {
                (row[3].ref, row[4].ref): row
                for row in rows
            }.values()
        )
        locus_names = tuple(
            name
            for row in owner_target_rows
            for name in (row[3].name, row[4].name)
        )
        source_refs = tuple(
            dict.fromkeys(
                [
                    *[ref for row in rows for ref in row[2].source_refs],
                    *group.source_refs,
                ]
            )
        )
        element_refs = tuple(
            dict.fromkeys(
                ref
                for row in owner_target_rows
                for ref in row[2].element_refs
            )
        )
        expected_rows = [
            f"{row[3].name} -> {row[4].name}"
            for row in owner_target_rows
        ]
        observed_rows = [row[2].observed for row in owner_target_rows]
        base = owner_target_rows[0][1]
        aggregate_contract = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=locus_names,
            property_name="initial_entry",
            state_role="initial_state",
            expected_direction="must_enter",
            violation_direction="missing",
            evidence_types=tuple(
                dict.fromkeys(
                    evidence
                    for row in owner_target_rows
                    for evidence in row[1].evidence_types
                )
            ),
            normative_statement=(
                f"The alternatives from {group.source_name} enter sibling operating "
                "composites that must each provide their exact "
                f"owner-local unconditional default entry: {expected_rows}."
            ),
            scope=(
                f"Transition group {group.group_id} from {group.source_name}; sibling "
                "composite default-entry obligations under common parent "
                f"{owner_target_rows[0][3].parent or 'model root'}"
            ),
            source_refs=source_refs,
            reason=(
                "One typed transition group enumerates multiple sibling operating "
                "owners with explicit initial-state contracts, forming one complete "
                "same-property scope; each atomic contract remains supporting evidence."
            ),
            basis=(
                f"transition_group_id={group.group_id}; "
                f"transition_group_source={group.source_name}; "
                f"source_contract_ids={list(source_contract_ids)}; "
                f"owner_target_refs={[(row[3].ref, row[4].ref) for row in owner_target_rows]}"
            ),
        ).model_copy(
            update={
                "quote": "\n".join(
                    f"[{row[0].segment_id}] {row[0].quote}"
                    for row in owner_target_rows
                ),
                "binding_hints": tuple(
                    hint
                    for row in owner_target_rows
                    for hint in row[0].binding_hints
                ),
            }
        )
        aggregate_candidate = _candidate(
            aggregate_contract,
            title="Sibling operating composites lack their required default entries",
            predicate_id=None,
            predicate_inputs={},
            element_refs=element_refs,
            source_refs=source_refs,
            expected=aggregate_contract.normative_statement,
            observed=" ".join(observed_rows),
            strongest_rebuttal=(
                "A guarded parent-to-child route in one sibling does not establish "
                "an unconditional owner-local default entry in that sibling or any other."
            ),
            reason=(
                "Each supplied initial-state contract resolves to a different sibling "
                "composite, and every exact owner-local inventory independently lacks "
                "the required unconditional default entry."
            ),
            basis=aggregate_contract.basis,
        )
        builder.add(
            "aggregate_initial_entry",
            source_contract_ids,
            aggregate_contract,
            aggregate_candidate,
            reason=(
                "A typed alternatives group establishes the complete sibling scope, "
                "and each explicit default-entry obligation is refuted by its complete "
                "owner-local transition inventory."
            ),
            basis=(
                f"transition_group_id={group.group_id}; typed sibling owner/target "
                "bindings and owned ModelIR initial edges"
            ),
        )
        for contract_id in source_contract_ids:
            consumed_contract_ids.add(contract_id)
            if contract_id not in builder.superseded_candidate_contract_ids:
                builder.superseded_candidate_contract_ids.append(contract_id)

    for rows in rows_by_owner_ref.values():
        individual.extend(
            row for row in rows if row[0].contract_id not in consumed_contract_ids
        )

    for contract, normalized_contract, candidate, _owner, _target in individual:
        builder.add(
            "owner_initial_entry",
            (contract.contract_id,),
            normalized_contract,
            candidate,
            reason="The exact scoped initial-transition inventory refutes the typed default-entry obligation.",
            basis="typed owner/target binding and owned ModelIR initial edges",
        )


def _candidate_state_refs(pair: PairInput, candidate: CandidateIssue) -> list[StateNode]:
    binding = bind_candidate(candidate, pair.model)
    return [item for item in pair.model.states if item.ref in binding.element_refs]


def _contract_state_refs(pair: PairInput, contract: NLContract) -> list[StateNode]:
    states: list[StateNode] = []
    for hint in contract.binding_hints:
        if hint.role not in {"owner", "scope", "source", "target", "state"}:
            continue
        state = _state_for_value(pair, hint.value)
        if state and state.ref not in {item.ref for item in states}:
            states.append(state)
    return states


def _materialize_root_reachability(
    builder: _Builder,
    contracts: Sequence[NLContract],
    existing: Sequence[CandidateIssue],
) -> dict[str, tuple[StateNode, StateNode, NLContract]]:
    pair = builder.pair
    relevant_by_contract: dict[str, list[StateNode]] = {
        contract.contract_id: _contract_state_refs(pair, contract) for contract in contracts
    }
    for candidate in existing:
        relevant_by_contract.setdefault(candidate.contract_id, []).extend(
            _candidate_state_refs(pair, candidate)
        )
    groups: dict[str, list[tuple[NLContract, StateNode]]] = defaultdict(list)
    contracts_by_id = {item.contract_id: item for item in contracts}
    for contract_id, states in relevant_by_contract.items():
        contract = contracts_by_id.get(contract_id)
        if contract is None or contract.state_role not in {"operating_state", "initial_state"}:
            continue
        for state in states:
            fact = _inspection_state(pair, state.ref)
            if fact is None or fact.reachable_from_initial:
                continue
            scope = _highest_unreachable_scope(pair, state)
            if scope:
                groups[scope.ref].append((contract, state))

    scopes: dict[str, tuple[StateNode, StateNode, NLContract]] = {}
    for scope_ref, rows in groups.items():
        scope = _state_by_ref(pair, scope_ref)
        if scope is None:
            continue
        descendant_rows = [
            row
            for row in rows
            if row[1].ref != scope.ref and _is_descendant(pair, row[1], scope)
        ]
        base, descendant = descendant_rows[0] if descendant_rows else rows[0]
        scopes[scope_ref] = (scope, descendant, base)
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=(scope.name,),
            property_name="reachability",
            state_role="operating_state",
            expected_direction="must_reach",
            violation_direction="unreachable",
            evidence_types=("source_identity", "closed_model_inventory", "reachability_fact", "verify_fact"),
            normative_statement=f"The required operating scope {scope.name} must be reachable from the model root.",
            scope=f"Root reachability of {scope.name}",
            source_refs=_source_refs([row[0] for row in rows]),
            reason="Typed operating contracts bind behavior inside this exact scope, so root reachability is a causal prerequisite rather than a new textual obligation.",
            basis="contract state roles, exact ancestor chain, and inspection-equivalent reachability facts",
        )
        supporting_refs = [scope.ref]
        supporting_refs.extend(row[1].ref for row in rows)
        candidate = _candidate(
            derived,
            title=f"Required operating scope {scope.name} is unreachable from root",
            predicate_id="G1",
            predicate_inputs={"source": "[*]", "target": scope.name},
            element_refs=supporting_refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"The exact inspection-equivalent facts mark {scope.ref} and its bound required behavior as unreachable from the top-level initial entry.",
            strongest_rebuttal="Owner-local declarations or transitions do not establish a path from the model root.",
            reason="At least one LLM-established operating obligation is bound below this exact composite, while finite root reachability excludes the composite.",
            basis=f"scope_ref={scope.ref}; supporting_contracts={[row[0].contract_id for row in rows]}; inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}",
        )
        builder.add(
            "root_reachability",
            tuple(dict.fromkeys(row[0].contract_id for row in rows)),
            derived,
            candidate,
            reason="A required operating scope is excluded from finite root reachability.",
            basis="typed operating contracts plus exact ancestor and reachability facts",
        )
    return scopes


def _source_state_contracts(
    pair: PairInput,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
) -> dict[str, list[NLContract]]:
    """Index exact state anchors without interpreting contract prose.

    Operating-state contracts may use their exact typed hints. Other contract
    kinds enter this index only through an exact grounding binding, so a broad
    transition contract cannot turn a prose name into a state identity.
    """

    exact_bindings: dict[tuple[str, str], list[SemanticBinding]] = defaultdict(list)
    for response in grounding_responses:
        for binding in response.semantic_bindings:
            if binding.status == "exact" and binding.role in {"state", "target"}:
                exact_bindings[(binding.contract_id, binding.role)].append(binding)

    result: dict[str, list[NLContract]] = defaultdict(list)
    for contract in contracts:
        hints = [
            hint
            for hint in contract.binding_hints
            if hint.role in {"state", "target"}
        ]
        states: dict[str, StateNode] = {}
        has_exact_binding = False
        for role in {hint.role for hint in hints}:
            bindings = exact_bindings.get((contract.contract_id, role), [])
            if bindings:
                has_exact_binding = True
                refs = {binding.model_element_ref for binding in bindings}
                if len(refs) != 1 or None in refs:
                    continue
                state = _state_by_ref(pair, next(iter(refs)))
                if state is not None:
                    states[state.ref] = state
                continue
            if contract.state_role != "operating_state":
                continue
            for hint in (item for item in hints if item.role == role):
                state = _state_for_value(pair, hint.value)
                if state is not None:
                    states[state.ref] = state
        if (
            contract.state_role == "operating_state"
            and not states
            and not has_exact_binding
            and len(contract.locus_names) == 1
        ):
            state = _state_for_value(pair, contract.locus_names[0])
            if state is not None:
                states[state.ref] = state
        for state_ref in states:
            result[state_ref].append(contract)
    return result


def _source_dead_end_anchors(
    pair: PairInput,
    state: StateNode,
    source_path: tuple[tuple[str, ...], tuple[str, ...]],
    anchors_by_ref: Mapping[str, Sequence[NLContract]],
) -> tuple[list[NLContract], bool]:
    """Choose a typed domain context for one exact source dead-end state.

    Direct state identity remains strongest. When the authored target is not
    named by NL, the nearest already-bound source-path state supplies only the
    surrounding domain context. A stable context fallback is allowed only when
    another contract in the same pair already resolves to an exact state; this
    prevents an unresolved or empty extraction from licensing source-wide
    candidate generation.
    """

    direct = list(anchors_by_ref.get(state.ref, ()))
    if direct:
        return direct, True

    inventory = pair.exact_source_inventory
    if inventory is not None:
        source_states = {item.source_id: item for item in inventory.states}
        for source_state_id in reversed(source_path[0][:-1]):
            source_state = source_states.get(source_state_id)
            if source_state is None:
                continue
            path_state = _state_by_name(pair, source_state.name)
            if path_state is None:
                continue
            nearest = list(anchors_by_ref.get(path_state.ref, ()))
            if nearest:
                return nearest, False

    context = {
        contract.contract_id: contract
        for rows in anchors_by_ref.values()
        for contract in rows
    }
    if not context:
        return [], False
    return [
        min(
            context.values(),
            key=lambda contract: (contract.segment_id, contract.contract_id),
        )
    ], False


def _materialize_source_dead_ends(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
) -> None:
    """Materialize the source-certified reachable non-final deadlock frontier.

    The closed-model inspection fact identifies a reachable leaf. The canonical
    author source independently closes the sequential soundness fragment. A
    typed NL contract supplies domain context, but need not name every authored
    target state. Exact state identity and the no-continuation claim come only
    from the source inventory and closed-model facts; the contract is not
    rewritten into a literal NL progress statement.
    """

    pair = builder.pair
    facts = pair.inspection_facts
    source_ir = pair.canonical_source_ir
    if facts is None or source_ir is None or pair.exact_source_inventory is None:
        return
    anchors_by_ref = _source_state_contracts(
        pair,
        contracts,
        grounding_responses,
    )
    source_states = {item.id: item for item in source_ir.model.states}
    source_transitions = {item.id: item for item in source_ir.model.transitions}
    final_states = set(source_ir.model.final_states)

    for state_fact in facts.states:
        if (
            not state_fact.reachable_from_initial
            or state_fact.outgoing_transition_refs
            or state_fact.is_composite
        ):
            continue
        state = _state_by_ref(pair, state_fact.state_ref)
        if state is None:
            continue
        source_matches = [
            item
            for item in pair.exact_source_inventory.states
            if item.name == state.name
        ]
        if len(source_matches) != 1:
            continue
        source_state = source_matches[0]
        canonical_state = source_states.get(source_state.source_id)
        source_path = _source_path(pair, source_state.source_id)
        if canonical_state is None or source_path is None:
            continue
        anchors, direct_anchor = _source_dead_end_anchors(
            pair,
            state,
            source_path,
            anchors_by_ref,
        )
        if not anchors:
            continue

        ancestor_ids: list[str] = []
        cursor: str | None = source_state.source_id
        while cursor and cursor in source_states:
            ancestor_ids.append(cursor)
            cursor = source_states[cursor].parent
        inherited_outgoing = [
            transition
            for transition in source_transitions.values()
            if transition.source in ancestor_ids
            and transition.attributes.get("transition_kind") != "initial"
        ]
        path_transitions = [
            source_transitions[transition_id]
            for transition_id in source_path[1]
            if transition_id in source_transitions
        ]
        assumptions = {
            "target_identity_resolved_exactly": True,
            "target_is_root_level": canonical_state.parent is None,
            "path_has_no_guards": len(path_transitions) == len(source_path[1])
            and all(item.guard is None for item in path_transitions),
            "no_concurrent_regions": not source_ir.model.concurrent_regions,
        }
        explicit_final = source_state.source_id in final_states
        sound_for_claim = all(assumptions.values())
        if not sound_for_claim or explicit_final or inherited_outgoing:
            continue

        base = anchors[0]
        state_hint = ContractBindingHint(
            role="state",
            value=state.name,
            source_ref=base.segment_id,
            reason=(
                "The supplied contract binds this exact author/source and closed-model state identity."
                if direct_anchor
                else "The supplied contract establishes domain context; exact state identity comes only from the author-source inventory and closed model."
            ),
            basis=(
                f"anchor_contract={base.contract_id}; "
                f"anchor_kind={'direct_state' if direct_anchor else 'domain_context'}; "
                f"state_ref={state.ref}; source_id={source_state.source_id}"
            ),
        )
        derived = _derived_contract(
            base,
            locus_kind="state",
            locus_names=(state.name,),
            property_name="deadlock_freedom",
            state_role="operating_state",
            expected_direction="must_progress",
            violation_direction="dead_end",
            evidence_types=(
                "source_identity",
                "closed_model_inventory",
                "reachability_fact",
                "deadlock_frontier_fact",
                "verify_fact",
            ),
            normative_statement=(
                f"The author-specified reachable non-final operating state {state.name} "
                "must not terminate without an inherited continuation."
            ),
            scope=f"Source-certified operational continuation of {state.name}",
            source_refs=tuple(
                dict.fromkeys(
                    [
                        *_source_refs(anchors),
                        source_state.raw_ref,
                        *[item.raw_ref for item in path_transitions],
                    ]
                )
            ),
            reason=(
                "The typed domain context and sequential source "
                "certificate establish a domain deadlock obligation independently "
                "of an NL-only progress contract."
            ),
            basis=(
                "exact inspection reachable-leaf fact plus canonical source "
                "reachability, final-state, inherited-outgoing, guard, and concurrency inventory"
            ),
        ).model_copy(update={"binding_hints": (state_hint,)})
        derived = derived.model_copy(update={"contract_id": canonical_contract_id(derived)})
        candidate = _candidate(
            derived,
            title=f"{state.name} is a source-certified reachable dead end",
            predicate_id="V4",
            predicate_inputs={"initial_scope": state.name},
            element_refs=(state.ref,),
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=(
                f"{state.ref} is reachable_from_initial=true with outgoing_transition_refs=[]; "
                f"source target {source_state.source_id} is reachable, explicit_final=false, "
                "and inherited_outgoing=[]."
            ),
            strongest_rebuttal=(
                "A terminal reading is not supported by an explicit final declaration, "
                "guarded-only path, concurrent region, inherited transition, or unresolved identity."
            ),
            reason=(
                "The exact closed-model leaf and independent author-source certificate "
                "establish the same reachable non-final no-continuation claim."
            ),
            basis=(
                f"state_ref={state.ref}; source_id={source_state.source_id}; "
                f"source_path={source_path}; assumptions={assumptions}; "
                f"inspection={facts.algorithm_version}"
            ),
        )
        builder.add(
            "reachable_dead_end",
            tuple(contract.contract_id for contract in anchors),
            derived,
            candidate,
            reason="A source certificate closes one exact reachable non-final deadlock fragment.",
            basis="typed domain context and exact source/inspection finite-graph facts",
        )


def _materialize_dead_ends(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
) -> None:
    pair = builder.pair
    for contract in contracts:
        if (
            contract.state_role != "operating_state"
            or contract.property != "deadlock_freedom"
        ):
            continue
        state_hint = _hint(contract, "state") or _hint(contract, "target") or _hint(contract, "owner")
        state = _state_for_value(pair, state_hint.value if state_hint else None)
        if state is None and len(contract.locus_names) == 1:
            state = _state_for_value(pair, contract.locus_names[0])
        fact = _inspection_state(pair, state.ref) if state else None
        if not state or not fact or not fact.reachable_from_initial or fact.outgoing_transition_refs:
            continue
        candidate = _candidate(
            contract,
            title=f"{state.name} has no operational continuation",
            predicate_id="V4",
            predicate_inputs={"initial_scope": state.name},
            element_refs=(state.ref,),
            source_refs=contract.source_refs,
            expected=contract.normative_statement,
            observed=f"{state.ref} is reachable_from_initial=true and outgoing_transition_refs=[].",
            strongest_rebuttal="No explicit terminal role or final edge is supplied for this typed operating state.",
            reason="An explicit operating-state contract and the deterministic reachable leaf frontier establish a reproducible no-continuation candidate.",
            basis=f"state_ref={state.ref}; inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}",
        )
        builder.add(
            "reachable_dead_end",
            (contract.contract_id,),
            contract,
            candidate,
            reason="An explicit deadlock-freedom obligation is bound to a reachable leaf with no outgoing transition.",
            basis="typed deadlock-freedom contract plus inspection-equivalent deadlock frontier",
        )
    _materialize_source_dead_ends(builder, contracts, grounding_responses)


def _source_state_id(pair: PairInput, state: StateNode) -> str | None:
    inventory = pair.exact_source_inventory
    if inventory is None:
        return None
    matches = [item.source_id for item in inventory.states if item.name == state.name]
    return matches[0] if len(matches) == 1 else None


def _source_path(
    pair: PairInput, target_id: str
) -> tuple[tuple[str, ...], tuple[str, ...]] | None:
    source_ir = pair.canonical_source_ir
    if source_ir is None:
        return None
    transitions = source_ir.model.transitions
    graph: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for transition in transitions:
        graph[transition.source].append((transition.target, transition.id))
    roots = tuple(source_ir.model.initial_states)
    queue: list[tuple[str, tuple[str, ...], tuple[str, ...]]] = [
        (root, (root,), ()) for root in roots
    ]
    seen: set[str] = set()
    while queue:
        node, states, transition_ids = queue.pop(0)
        if node in seen:
            continue
        seen.add(node)
        if node == target_id:
            return states, transition_ids
        for next_state, transition_id in graph.get(node, ()):
            queue.append(
                (
                    next_state,
                    (*states, next_state),
                    (*transition_ids, transition_id),
                )
            )
    return None


def _materialize_termination(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    stable_rows: list[
        tuple[
            NLContract,
            CandidateIssue,
            StateNode,
            StateNode | None,
            tuple[SourceInventoryTransition, ...],
        ]
    ] = []
    for contract in contracts:
        if contract.property != "termination" or contract.state_role != "termination_state":
            continue
        explicit_target_hint = _hint(contract, "target")
        state_hint = _hint(contract, "state")
        owner_hint = (
            _hint(contract, "owner")
            or _hint(contract, "scope")
            or _hint(contract, "source")
        )
        if (
            owner_hint is None
            and explicit_target_hint is not None
            and state_hint is not None
            and state_hint.value != explicit_target_hint.value
        ):
            owner_hint = state_hint
        endpoint_contract: NLContract | None = None
        if explicit_target_hint is None:
            completion_owner_hint = owner_hint or state_hint
            matching_endpoints = [
                endpoint
                for endpoint in contracts
                if endpoint.segment_id == contract.segment_id
                and endpoint.property == "transition_endpoints"
                and endpoint.state_role == "termination_state"
                and completion_owner_hint is not None
                and _hint(endpoint, "source") is not None
                and _hint(endpoint, "source").value == completion_owner_hint.value
                and _hint(endpoint, "target") is not None
            ]
            target_values = {
                _hint(endpoint, "target").value for endpoint in matching_endpoints
            }
            if len(target_values) == 1:
                endpoint_contract = matching_endpoints[0]
                explicit_target_hint = _hint(endpoint_contract, "target")
                if owner_hint is None:
                    owner_hint = completion_owner_hint
        target_hint = explicit_target_hint or state_hint
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        owner = _state_for_value(pair, owner_hint.value if owner_hint else None)
        if target is None:
            continue
        source_ir = pair.canonical_source_ir
        source_target_id = _source_state_id(pair, target)
        source_states = {
            item.id: item for item in source_ir.model.states
        } if source_ir else {}
        source_ancestors: list[str] = []
        cursor = source_target_id
        while cursor and cursor in source_states:
            source_ancestors.append(cursor)
            cursor = source_states[cursor].parent
        source_path = _source_path(pair, source_target_id) if source_target_id else None
        source_transitions = {
            item.id: item for item in source_ir.model.transitions
        } if source_ir else {}
        path_unguarded = bool(source_path) and all(
            source_transitions[transition_id].guard is None
            for transition_id in source_path[1]
            if transition_id in source_transitions
        )
        continuing = [
            item
            for item in source_transitions.values()
            if item.source in source_ancestors
            and item.attributes.get("transition_kind") not in {"initial", "final"}
            and item.guard is None
        ]
        explicit_final = bool(
            source_ir
            and source_target_id in set(source_ir.model.final_states)
        )
        sound_for_claim = bool(
            source_ir
            and source_target_id
            and source_path
            and path_unguarded
            and not source_ir.model.concurrent_regions
        )
        if sound_for_claim and continuing and not explicit_final:
            candidate = _candidate(
                contract,
                title=f"Termination target {target.name} admits continued behavior",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(target.ref,),
                source_refs=(
                    *contract.source_refs,
                    *[item.raw_ref for item in continuing],
                ),
                expected=contract.normative_statement,
                observed=f"The exact reachable author-source target is not explicit-final and its ancestor chain admits guard-free continuations {[item.id for item in continuing]}.",
                strongest_rebuttal="Endpoint existence alone does not prove that the designated ending target is stable.",
                reason="The NL marks the exact target as a termination state, while the closed author-source soundness fragment establishes reachable non-final continuation.",
                basis=f"contract={contract.contract_id}; target_binding_contract={endpoint_contract.contract_id if endpoint_contract else contract.contract_id}; source_target_id={source_target_id}; source_path={source_path}; continuation_ids={[item.id for item in continuing]}",
            )
            stable_rows.append(
                (
                    contract,
                    candidate,
                    target,
                    owner,
                    tuple(continuing),
                )
            )
        # A termination contract's source/owner identifies the scope that
        # completes; its explicit target is an independent endpoint. A named
        # completion target may intentionally be an ancestor, sibling, or
        # root-level state, so target ancestry alone cannot manufacture a
        # route-avoidance obligation or contradict the completion relation.

    grouped: dict[
        str,
        list[
            tuple[
                NLContract,
                CandidateIssue,
                StateNode,
                StateNode | None,
                tuple[SourceInventoryTransition, ...],
            ]
        ],
    ] = defaultdict(list)
    ownerless_rows: list[
        tuple[
            NLContract,
            CandidateIssue,
            StateNode,
            StateNode | None,
            tuple[SourceInventoryTransition, ...],
        ]
    ] = []
    for row in stable_rows:
        if row[3] is None:
            ownerless_rows.append(row)
        else:
            grouped[row[2].ref].append(row)

    for contract, candidate, _target, _owner, _continuing in ownerless_rows:
        builder.add(
            "stable_termination",
            (contract.contract_id,),
            contract,
            candidate,
            reason="A typed termination target has exact continuing behavior and is not an explicit stable sink.",
            basis="termination state role plus canonical author-source reachability, final-state, hierarchy, and transition inventory",
        )

    for rows in grouped.values():
        owner_rows = rows
        distinct_owner_refs = {row[3].ref for row in owner_rows if row[3] is not None}
        if len(distinct_owner_refs) < 2:
            for contract, candidate, _target, _owner, _continuing in rows:
                builder.add(
                    "stable_termination",
                    (contract.contract_id,),
                    contract,
                    candidate,
                    reason="A typed termination target has exact continuing behavior and is not an explicit stable sink.",
                    basis="termination state role plus canonical author-source reachability, final-state, hierarchy, and transition inventory",
                )
            continue

        target = rows[0][2]
        source_contract_ids = tuple(
            dict.fromkeys(row[0].contract_id for row in rows)
        )
        owners = list(
            {
                row[3].ref: row[3]
                for row in owner_rows
                if row[3] is not None
            }.values()
        )
        continuing = list(
            {
                transition.id: transition
                for row in rows
                for transition in row[4]
            }.values()
        )
        source_refs = tuple(
            dict.fromkeys(
                [
                    *[
                        ref
                        for row in rows
                        for ref in row[0].source_refs
                    ],
                    *[item.raw_ref for item in continuing],
                ]
            )
        )
        aggregate_contract = _derived_contract(
            rows[0][0],
            locus_kind="scope",
            locus_names=(*[owner.name for owner in owners], target.name),
            property_name="termination",
            state_role="termination_state",
            expected_direction="must_terminate",
            violation_direction="not_completed",
            evidence_types=tuple(
                dict.fromkeys(
                    evidence
                    for row in rows
                    for evidence in row[0].evidence_types
                )
            ),
            normative_statement=(
                f"The completion obligations for {[owner.name for owner in owners]} "
                f"must reach shared target {target.name} as a stable termination boundary."
            ),
            scope=(
                f"Shared termination target {target.name} across explicit operating scopes"
            ),
            source_refs=source_refs,
            reason=(
                "Multiple explicit termination contracts bind the same exact target, "
                "so one same-property shared-target obligation preserves their full scope."
            ),
            basis=(
                f"source_contract_ids={list(source_contract_ids)}; "
                f"owner_refs={[owner.ref for owner in owners]}; target_ref={target.ref}; "
                f"continuation_ids={[item.id for item in continuing]}"
            ),
        ).model_copy(
            update={
                "quote": "\n".join(
                    f"[{row[0].segment_id}] {row[0].quote}" for row in rows
                ),
                "binding_hints": tuple(
                    hint for row in rows for hint in row[0].binding_hints
                ),
            }
        )
        aggregate_candidate = _candidate(
            aggregate_contract,
            title=f"Shared termination target {target.name} does not terminate its operating scopes",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(*[owner.ref for owner in owners], target.ref),
            source_refs=source_refs,
            expected=aggregate_contract.normative_statement,
            observed=(
                f"The exact reachable author-source target {target.name} is not "
                "explicit-final, and its ancestor chain admits guard-free "
                f"continuations {[item.id for item in continuing]}; therefore none "
                f"of the bound completion scopes {[owner.name for owner in owners]} "
                "obtains a stable termination boundary at that shared target."
            ),
            strongest_rebuttal=(
                "The existence of each completion endpoint does not establish stable "
                "termination when their shared target remains non-final and continuing."
            ),
            reason=(
                "Every explicit termination contract binds the same exact target, and "
                "the complete author-source soundness fragment establishes one shared "
                "non-final continuation cause across all of them."
            ),
            basis=aggregate_contract.basis,
        )
        builder.add(
            "aggregate_stable_termination",
            source_contract_ids,
            aggregate_contract,
            aggregate_candidate,
            reason=(
                "A shared exact target refutes multiple explicit termination obligations "
                "through one complete non-final continuation certificate."
            ),
            basis="typed termination owners, shared target identity, and canonical author-source continuation inventory",
            root_refs=tuple(owner.ref for owner in owners),
            marked_refs=(target.ref,),
        )
        for contract_id in source_contract_ids:
            if contract_id not in builder.superseded_candidate_contract_ids:
                builder.superseded_candidate_contract_ids.append(contract_id)


def _group_operating_source(
    pair: PairInput,
    group: NLTransitionGroup,
    contracts: Sequence[NLContract],
) -> StateNode | None:
    target_refs = {
        target.ref
        for item in group.alternatives
        if (target := _state_for_value(pair, item.target_name)) is not None
    }

    def matching_target_count(source: StateNode) -> int:
        return len(
            {
                item.target_ref
                for item in pair.model.transitions
                if item.source_ref == source.ref and item.target_ref in target_refs
            }
        )

    declared_source = _state_for_value(pair, group.source_name)
    if declared_source is not None and matching_target_count(declared_source) >= 2:
        return declared_source

    entry_targets: list[StateNode] = []
    for contract in contracts:
        if contract.segment_id != group.segment_id or contract.property != "initial_entry":
            continue
        owner_hint = _hint(contract, "owner")
        target_hint = _hint(contract, "target")
        if (
            owner_hint is None
            or target_hint is None
            or owner_hint.value != group.source_name
        ):
            continue
        target = _state_for_value(pair, target_hint.value)
        if target is not None and matching_target_count(target) >= 2:
            entry_targets.append(target)
    unique_targets = {item.ref: item for item in entry_targets}
    return next(iter(unique_targets.values())) if len(unique_targets) == 1 else None


def _group_transitions(
    pair: PairInput,
    group: NLTransitionGroup,
    contracts: Sequence[NLContract],
) -> tuple[StateNode | None, list[tuple[object, Transition]]]:
    source = _group_operating_source(pair, group, contracts)
    if source is None:
        return None, []
    rows: list[tuple[object, Transition]] = []
    for alternative in group.alternatives:
        target = _state_for_value(pair, alternative.target_name)
        if target is None:
            continue
        matches = [
            item
            for item in pair.model.transitions
            if item.source_ref == source.ref and item.target_ref == target.ref
        ]
        if len(matches) == 1:
            rows.append((alternative, matches[0]))
    return source, rows


def _group_base_contract(
    group: NLTransitionGroup,
    source: StateNode,
    contracts: Sequence[NLContract],
) -> NLContract | None:
    target_names = {item.target_name for item in group.alternatives}
    endpoint_contracts = []
    relation_contracts = []
    for contract in contracts:
        if contract.segment_id != group.segment_id:
            continue
        source_hint = _hint(contract, "source")
        target_hints = [item for item in contract.binding_hints if item.role == "target"]
        if (
            contract.property == "transition_endpoints"
            and source_hint is not None
            and source_hint.value in {group.source_name, source.name}
            and any(item.value in target_names for item in target_hints)
        ):
            endpoint_contracts.append(contract)
        scope_hints = [
            item
            for item in contract.binding_hints
            if item.role in {"source", "scope", "owner"}
        ]
        if (
            len({item.value for item in target_hints if item.value in target_names}) >= 2
            and any(item.value == group.source_name for item in scope_hints)
        ):
            relation_contracts.append(contract)
    candidates = endpoint_contracts or relation_contracts
    return candidates[0] if candidates else None


def _materialize_group_collisions(
    builder: _Builder,
    groups: Sequence[NLTransitionGroup],
    contracts: Sequence[NLContract],
) -> None:
    pair = builder.pair
    for group in groups:
        if len(group.alternatives) < 2:
            continue
        if len({alternative.target_name for alternative in group.alternatives}) < 2:
            continue
        source, rows = _group_transitions(pair, group, contracts)
        if len(rows) < 2:
            continue
        normative_conditions = {
            (item.event, item.guard) for item, _transition in rows
        }
        signatures = {
            (transition.triggers, transition.guard) for _item, transition in rows
        }
        if len(signatures) != 1:
            continue
        base = _group_base_contract(group, source, contracts) if source else None
        if base is None or source is None:
            continue
        targets = [_state_for_value(pair, item.target_name) for item, _ in rows]
        targets = [item for item in targets if item]
        derived = _derived_contract(
            base,
            locus_kind="transition",
            locus_names=(source.name, *[item.target_name for item, _ in rows]),
            property_name="guard_disjointness",
            state_role=base.state_role,
            expected_direction="must_cover",
            violation_direction="wrong_guard",
            evidence_types=("source_identity", "closed_model_inventory", "transition_fact", "guard_fact", "semantic_comparison"),
            normative_statement=f"Distinct alternatives in {group.group_id} must have distinguishable selection conditions.",
            scope=f"Transition group {group.group_id}",
            source_refs=group.source_refs,
            reason="The LLM transition group establishes distinct alternatives, and a typed owner-entry relation resolves the operational source when the group is stated at composite scope.",
            basis="typed transition group alternatives and exact ModelIR trigger/guard fields",
        )
        refs = [transition.ref for _, transition in rows]
        refs.extend(item.ref for item in ([source] if source else []) + targets)
        candidate = _candidate(
            derived,
            title=f"Alternatives in {group.group_id} compete under the same selection conditions",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"The exact transitions {[transition.ref for _, transition in rows]} share trigger/guard signature {next(iter(signatures))} while targeting distinct states {[transition.target for _, transition in rows]}.",
            strongest_rebuttal="Distinct targets preserve different post-transition behavior, but they do not disambiguate simultaneous enablement at the shared source.",
            reason="Distinct alternatives map to different exact targets but have identical typed trigger/guard signatures, so their selection conditions overlap.",
            basis=f"group={group.group_id}; normative_conditions={sorted(map(str, normative_conditions))}; transition_refs={[transition.ref for _, transition in rows]}",
        )
        builder.add(
            "transition_group_collision",
            tuple(
                item.contract_id
                for item in contracts
                if item.segment_id == group.segment_id
                and any(
                    hint.role == "target"
                    and hint.value
                    in {alternative.target_name for alternative in group.alternatives}
                    for hint in item.binding_hints
                )
            )
            or (base.contract_id,),
            derived,
            candidate,
            reason="A typed multi-target relation has distinct exact targets but identical trigger/guard signatures, creating overlapping selection conditions without claiming identical post-transition behavior.",
            basis="transition group semantic identity and exact closed-model signatures",
        )


def _materialize_group_guards(
    builder: _Builder,
    groups: Sequence[NLTransitionGroup],
    contracts: Sequence[NLContract],
) -> None:
    """Materialize missing guards from the typed event+guard group projection."""

    pair = builder.pair
    for group in groups:
        source = _state_for_value(pair, group.source_name)
        if source is None:
            continue
        for alternative in group.alternatives:
            if alternative.guard is None:
                continue
            target = _state_for_value(pair, alternative.target_name)
            if target is None:
                continue
            matches = [
                item
                for item in pair.model.transitions
                if item.source_ref == source.ref and item.target_ref == target.ref
            ]
            if len(matches) != 1:
                continue
            transition = matches[0]
            base = _group_base_contract(group, source, contracts)
            if base is None:
                continue
            if transition.guard is not None:
                builder.checks.append(
                    builder.receipt(
                        "transition_guard_presence",
                        (base.contract_id,),
                        status="not_applicable",
                        contract=base,
                        model_refs=(source.ref, target.ref, transition.ref),
                        source_refs=(*group.source_refs, *alternative.source_refs),
                        reason="The exact carrier has a guard, so the deterministic missing-guard frontier does not emit a candidate; semantic guard equivalence remains a separate grounding question.",
                        basis=f"transition_ref={transition.ref}; guard={transition.guard!r}",
                    )
                )
                continue

            hints = [
                ContractBindingHint(
                    role="source",
                    value=source.name,
                    source_ref=group.segment_id,
                    reason="The typed transition group binds the exact shared source.",
                    basis=f"group={group.group_id}; source_ref={source.ref}",
                ),
                ContractBindingHint(
                    role="target",
                    value=target.name,
                    source_ref=group.segment_id,
                    reason="This typed alternative binds one exact normative target.",
                    basis=f"alternative={alternative.alternative_id}; target_ref={target.ref}",
                ),
                ContractBindingHint(
                    role="guard",
                    value=alternative.guard,
                    source_ref=group.segment_id,
                    reason="The alternative carries an independent normative guard in addition to any event.",
                    basis=f"alternative={alternative.alternative_id}; supplied transition-group guard field",
                ),
            ]
            if alternative.event is not None:
                hints.append(
                    ContractBindingHint(
                        role="event",
                        value=alternative.event,
                        source_ref=group.segment_id,
                        reason="The alternative carries this event independently from its guard.",
                        basis=f"alternative={alternative.alternative_id}; supplied transition-group event field",
                    )
                )
            derived = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source.name, target.name),
                property_name="guard",
                state_role=base.state_role,
                expected_direction="must_exist",
                violation_direction="missing",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "guard_fact",
                ),
                normative_statement=(
                    f"The exact {source.name} to {target.name} alternative must retain "
                    f"the independent guard {alternative.guard!r}."
                ),
                scope=f"Guard carrier {source.name} -> {target.name}",
                source_refs=tuple(
                    dict.fromkeys([*group.source_refs, *alternative.source_refs])
                ),
                reason="The typed relation separately establishes an event and guard, allowing exact carrier guard-presence audit.",
                basis="NLTransitionAlternative.guard and exact ModelIR transition endpoint identity",
                binding_hints=tuple(hints),
            )
            derived = derived.model_copy(
                update={"contract_id": canonical_contract_id(derived)}
            )
            candidate = _candidate(
                derived,
                title=f"{source.name} to {target.name} omits its required guard",
                predicate_id="S5",
                predicate_inputs={
                    "transition_ref": transition.ref,
                    "expected_guard": alternative.guard,
                },
                element_refs=(source.ref, target.ref, transition.ref),
                source_refs=derived.source_refs,
                expected=derived.normative_statement,
                observed=f"The exact carrier {transition.ref} has guard=null.",
                strongest_rebuttal="The event/trigger carrier is a different typed field and cannot satisfy the independent guard.",
                reason="The normative alternative has an independent guard while its one exact closed-model carrier has none.",
                basis=(
                    f"group={group.group_id}; alternative={alternative.alternative_id}; "
                    f"transition_ref={transition.ref}; model_guard=null"
                ),
            )
            builder.add(
                "transition_guard_presence",
                (base.contract_id,),
                derived,
                candidate,
                reason="A typed normative guard is absent from its exact endpoint carrier.",
                basis="event/guard-separated transition-group semantics and exact ModelIR guard field",
            )


def _source_endpoint_name(value: str) -> str:
    """Return the exact leaf identifier from a canonical qualified source endpoint."""

    return value.rsplit(".", 1)[-1]


def _materialize_group_post_states(
    builder: _Builder,
    groups: Sequence[NLTransitionGroup],
    contracts: Sequence[NLContract],
) -> None:
    """Project exact typed event alternatives into native R2 input contracts.

    The transition group establishes the normative event/post-state relation.
    Canonical author source supplies the event identity for the unique exact
    source-target carrier, and the closed FCSTM projection must resolve that
    identity to one native Event. No event spelling or target verdict is
    inferred from the inspected model.
    """

    pair = builder.pair
    inventory = pair.exact_source_inventory
    if inventory is None:
        return
    for group in groups:
        source = _state_for_value(pair, group.source_name)
        if source is None:
            continue
        for alternative in group.alternatives:
            if alternative.event is None:
                continue
            target = _state_for_value(pair, alternative.target_name)
            if target is None:
                continue
            bases = [
                contract
                for contract in contracts
                if contract.segment_id == group.segment_id
                and contract.property == "transition_endpoints"
                and (source_hint := _hint(contract, "source")) is not None
                and source_hint.value in {group.source_name, source.name}
                and (target_hint := _hint(contract, "target")) is not None
                and target_hint.value in {alternative.target_name, target.name}
            ]
            if len(bases) != 1:
                continue
            source_rows = [
                row
                for row in inventory.transitions
                if _source_endpoint_name(row.source) == source.name
                and _source_endpoint_name(row.target) == target.name
                and row.event is not None
            ]
            if len(source_rows) != 1:
                continue
            source_row = source_rows[0]
            event = pair.model.event(source_row.event or "")
            if event is None:
                continue
            hints = (
                ContractBindingHint(
                    role="event",
                    value=event.display_name,
                    source_ref=source_row.raw_ref,
                    reason="The typed alternative has an event, and its unique canonical author-source carrier supplies the exact native event identity.",
                    basis=f"group={group.group_id}; source_transition={source_row.transition_id}; event_ref={event.ref}",
                ),
                ContractBindingHint(
                    role="target",
                    value=target.canonical_path,
                    source_ref=source_row.raw_ref,
                    reason="The typed alternative and unique canonical author-source carrier bind the exact required post-stimulus target.",
                    basis=f"alternative={alternative.alternative_id}; target_ref={target.ref}",
                ),
            )
            base = bases[0]
            derived = _derived_contract(
                base,
                locus_kind="scenario",
                locus_names=(event.display_name, target.name),
                property_name="state_after_stimulus",
                state_role=base.state_role,
                expected_direction="must_reach",
                violation_direction="wrong_target",
                evidence_types=("source_identity", "transition_fact", "trace_fact"),
                normative_statement=(
                    f"After the exact {event.display_name!r} stimulus, the current "
                    f"artifact must enter {target.name}."
                ),
                scope=f"Transition alternative {source.name} -> {target.name}",
                source_refs=tuple(
                    dict.fromkeys(
                        [
                            *group.source_refs,
                            *alternative.source_refs,
                            source_row.raw_ref,
                        ]
                    )
                ),
                reason="One typed event alternative and one unique canonical author-source carrier establish an executable event/post-state obligation.",
                basis=(
                    f"group={group.group_id}; alternative={alternative.alternative_id}; "
                    f"source_transition={source_row.transition_id}; event_ref={event.ref}; "
                    f"target_ref={target.ref}"
                ),
                binding_hints=hints,
            )
            candidate = _candidate(
                derived,
                title=f"{event.display_name} may not leave the system in {target.name}",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(source.ref, event.ref, target.ref),
                source_refs=derived.source_refs,
                expected=derived.normative_statement,
                observed="The exact post-stimulus state is delegated to a fresh native FCSTM runtime scenario.",
                strongest_rebuttal="A native runtime execution may establish that the exact stimulus reaches and retains the required target.",
                reason="The event and target identities close independently of runtime truth, so R2 can evaluate the current artifact without a source trace or expected answer.",
                basis=derived.basis,
            )
            builder.add(
                "state_after_stimulus",
                (base.contract_id,),
                derived,
                candidate,
                reason="A typed event alternative, unique canonical source carrier, and native Event identity close one R2 candidate.",
                basis="NLTransitionGroup plus ExactSourceInventory transition identity and native FCSTM event projection",
            )


def _source_carrier_for_contract(
    pair: PairInput,
    contract: NLContract,
    source_state: StateNode,
    groups: Sequence[NLTransitionGroup] = (),
) -> SourceInventoryTransition | None:
    inventory = pair.exact_source_inventory
    if inventory is None:
        return None
    condition_values = {
        hint.role: hint.value
        for hint in contract.binding_hints
        if hint.role in {"guard", "event", "trigger"}
    }
    source_hint = _hint(contract, "source")
    target_hint = _hint(contract, "target")
    if source_hint is not None and target_hint is not None:
        group_alternatives = [
            alternative
            for group in groups
            if group.source_name == source_hint.value
            for alternative in group.alternatives
            if alternative.target_name == target_hint.value
        ]
        if len(group_alternatives) == 1:
            alternative = group_alternatives[0]
            if alternative.event is not None:
                condition_values.setdefault("event", alternative.event)
            if alternative.guard is not None:
                condition_values.setdefault("guard", alternative.guard)
    if not condition_values:
        return None
    rows = [
        item
        for item in inventory.transitions
        if _source_endpoint_name(item.source) == source_state.name
        and all(
            value in {item.event, item.guard}
            for value in condition_values.values()
        )
    ]
    return rows[0] if len(rows) == 1 else None


def _model_carrier_for_source_row(
    pair: PairInput,
    source_row: SourceInventoryTransition,
) -> Transition | None:
    source = _state_for_value(pair, _source_endpoint_name(source_row.source))
    target = _state_for_value(pair, _source_endpoint_name(source_row.target))
    if source is None or target is None:
        return None
    rows = [
        item
        for item in pair.model.transitions
        if item.source_ref == source.ref and item.target_ref == target.ref
    ]
    return rows[0] if len(rows) == 1 else None


def _materialize_wrong_targets(
    builder: _Builder,
    contracts: Sequence[NLContract],
    groups: Sequence[NLTransitionGroup],
    grounding_responses: Sequence[GroundingResponse],
) -> None:
    pair = builder.pair
    contracts_by_id = {item.contract_id: item for item in contracts}
    exact_target_bindings = [
        binding
        for response in grounding_responses
        for binding in response.semantic_bindings
        if binding.status == "exact"
        and binding.role == "target"
        and binding.model_element_ref
        and binding.carrier_transition_ref
    ]
    for binding in exact_target_bindings:
        base = contracts_by_id.get(binding.contract_id)
        expected_state = _state_by_ref(pair, binding.model_element_ref)
        carrier = pair.model.transition(binding.carrier_transition_ref)
        if (
            base is None
            or base.property != "transition_endpoints"
            or expected_state is None
            or carrier is None
        ):
            continue
        source_hint = _hint(base, "source")
        source_state = _state_for_value(pair, source_hint.value if source_hint else None)
        actual_source = _state_for_value(pair, carrier.source)
        actual_target_ref = _transition_target_ref(pair, carrier)
        actual_target = _state_by_ref(pair, actual_target_ref)
        if (
            source_state is None
            or actual_source is None
            or actual_target is None
            or actual_source.ref != source_state.ref
            or actual_target.ref == expected_state.ref
        ):
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, expected_state.name),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="An exact grounding binding identifies the normative target and its conflicting closed transition carrier.",
                basis="SemanticBinding target/model refs and exact ModelIR transition endpoints",
            )
        candidate = _candidate(
            target_contract,
            title=f"{source_state.name} routes to {actual_target.name} instead of {expected_state.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                *([binding.source_element_ref] if binding.source_element_ref else []),
            ),
            expected=target_contract.normative_statement,
            observed=f"Exact carrier {carrier.ref} leaves {source_state.ref} but targets {actual_target.ref}, while the normative target binding is {expected_state.ref}.",
            strongest_rebuttal="A transition to a different exact target cannot satisfy this condition-scoped endpoint obligation.",
            reason="The target SemanticBinding is exact and the supplied carrier transition has a different resolved target under the same source contract.",
            basis=f"binding_id={binding.binding_id}; source_ref={source_state.ref}; expected_target_ref={expected_state.ref}; carrier_ref={carrier.ref}; actual_target_ref={actual_target.ref}",
        )
        builder.add(
            "wrong_target",
            (base.contract_id,),
            target_contract,
            candidate,
            reason="One exact target binding is refuted by the resolved endpoint of its supplied closed transition carrier.",
            basis="typed SemanticBinding plus exact ModelIR transition source/target refs",
        )

    target_refs_by_concept: dict[str, set[str]] = defaultdict(set)
    bindings_by_concept: dict[str, list[SemanticBinding]] = defaultdict(list)
    for binding in exact_target_bindings:
        target_refs_by_concept[binding.concept_name].add(binding.model_element_ref)
        bindings_by_concept[binding.concept_name].append(binding)
    for base in contracts:
        if base.property != "transition_endpoints":
            continue
        source_hint = _hint(base, "source")
        target_hint = _hint(base, "target")
        if source_hint is None or target_hint is None:
            continue
        expected_refs = target_refs_by_concept.get(target_hint.value, set())
        if len(expected_refs) != 1:
            continue
        expected_state = _state_by_ref(pair, next(iter(expected_refs)))
        source_state = _state_for_value(pair, source_hint.value)
        source_carrier = (
            _source_carrier_for_contract(pair, base, source_state, groups)
            if source_state is not None
            else None
        )
        model_carrier = (
            _model_carrier_for_source_row(pair, source_carrier)
            if source_carrier is not None
            else None
        )
        actual_target = (
            _state_for_value(pair, _source_endpoint_name(source_carrier.target))
            if source_carrier is not None
            else None
        )
        if (
            expected_state is None
            or source_state is None
            or source_carrier is None
            or model_carrier is None
            or actual_target is None
            or actual_target.ref == expected_state.ref
        ):
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, expected_state.name),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="A unique exact target-concept binding is reused across contracts carrying the same typed target concept.",
                basis="SemanticBinding concept identity plus exact source transition inventory",
            )
        concept_bindings = bindings_by_concept[target_hint.value]
        candidate = _candidate(
            target_contract,
            title=f"{source_state.name} routes to {actual_target.name} instead of {expected_state.name}",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                model_carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                source_carrier.raw_ref,
                *[
                    item.source_element_ref
                    for item in concept_bindings
                    if item.source_element_ref
                ],
            ),
            expected=target_contract.normative_statement,
            observed=(
                f"Exact author-source carrier {source_carrier.transition_id} "
                f"targets {source_carrier.target}; its closed-model carrier "
                f"{model_carrier.ref} targets {actual_target.ref}, while the unique "
                f"normative concept binding is {expected_state.ref}."
            ),
            strongest_rebuttal="A condition-scoped transition to a different exact target cannot satisfy the bound target concept.",
            reason="The same typed target concept has one exact cross-artifact binding, and the exact source+condition carrier resolves to a different target.",
            basis=(
                f"concept={target_hint.value}; source_transition_id={source_carrier.transition_id}; "
                f"source_ref={source_state.ref}; expected_target_ref={expected_state.ref}; "
                f"carrier_ref={model_carrier.ref}; actual_target_ref={actual_target.ref}"
            ),
        )
        builder.add(
            "wrong_target",
            (base.contract_id,),
            target_contract,
            candidate,
            reason="One exact shared target-concept binding is refuted by the exact source+condition carrier endpoint.",
            basis="typed concept identity, exact source transition inventory, and exact ModelIR endpoints",
        )

    contract_carriers: list[
        tuple[
            NLContract,
            ContractBindingHint,
            StateNode,
            SourceInventoryTransition,
            Transition,
            StateNode,
        ]
    ] = []
    direct_target_roles: dict[str, list[tuple[NLContract, ContractBindingHint]]] = (
        defaultdict(list)
    )
    for contract in contracts:
        target_hint = _hint(contract, "target")
        if target_hint is not None:
            direct_target = _state_for_value(pair, target_hint.value)
            if direct_target is not None:
                direct_target_roles[direct_target.ref].append((contract, target_hint))
        if contract.property != "transition_endpoints" or target_hint is None:
            continue
        source_hint = _hint(contract, "source")
        source_state = _state_for_value(pair, source_hint.value if source_hint else None)
        source_carrier = (
            _source_carrier_for_contract(pair, contract, source_state, groups)
            if source_state is not None
            else None
        )
        model_carrier = (
            _model_carrier_for_source_row(pair, source_carrier)
            if source_carrier is not None
            else None
        )
        actual_target = (
            _state_for_value(pair, _source_endpoint_name(source_carrier.target))
            if source_carrier is not None
            else None
        )
        if (
            source_state is not None
            and source_carrier is not None
            and model_carrier is not None
            and actual_target is not None
        ):
            contract_carriers.append(
                (
                    contract,
                    target_hint,
                    source_state,
                    source_carrier,
                    model_carrier,
                    actual_target,
                )
            )

    for (
        base,
        target_hint,
        source_state,
        source_carrier,
        model_carrier,
        actual_target,
    ) in contract_carriers:
        foreign_roles = [
            (contract, hint)
            for contract, hint in direct_target_roles.get(actual_target.ref, [])
            if contract.contract_id != base.contract_id
            and hint.value != target_hint.value
        ]
        if not foreign_roles:
            continue
        sibling_rows = [
            row
            for row in contract_carriers
            if row[0].contract_id != base.contract_id
            and row[1].value == target_hint.value
            and row[5].ref != actual_target.ref
        ]
        sibling_target_refs = {row[5].ref for row in sibling_rows}
        foreign_role_names = {hint.value for _contract, hint in foreign_roles}
        if len(sibling_target_refs) != 1 or len(foreign_role_names) != 1:
            continue
        expected_state = _state_by_ref(pair, next(iter(sibling_target_refs)))
        if expected_state is None:
            continue
        target_contract = base
        if base.violation_direction != "wrong_target":
            target_contract = _derived_contract(
                base,
                locus_kind="transition",
                locus_names=(source_state.name, target_hint.value),
                property_name="transition_endpoints",
                state_role=base.state_role,
                expected_direction=base.expected_direction,
                violation_direction="wrong_target",
                evidence_types=(
                    "source_identity",
                    "closed_model_inventory",
                    "transition_fact",
                    "semantic_comparison",
                ),
                normative_statement=base.normative_statement,
                scope=base.scope,
                source_refs=base.source_refs,
                reason="Cross-contract target roles distinguish the required concept from the carrier's actual target.",
                basis="typed target concepts and exact source+condition carriers",
            )
        supporting_source_refs = [
            row[3].raw_ref for row in sibling_rows if row[5].ref == expected_state.ref
        ]
        supporting_source_refs.extend(
            ref
            for contract, _hint_value in foreign_roles
            for ref in contract.source_refs
        )
        foreign_role = next(iter(foreign_role_names))
        candidate = _candidate(
            target_contract,
            title=(
                f"{source_state.name} routes to {actual_target.name} instead of "
                f"the required {target_hint.value} target"
            ),
            predicate_id=None,
            predicate_inputs={},
            element_refs=(
                source_state.ref,
                expected_state.ref,
                actual_target.ref,
                model_carrier.ref,
            ),
            source_refs=(
                *target_contract.source_refs,
                source_carrier.raw_ref,
                *supporting_source_refs,
            ),
            expected=target_contract.normative_statement,
            observed=(
                f"Exact author-source carrier {source_carrier.transition_id} targets "
                f"{source_carrier.target}; sibling carriers for target concept "
                f"{target_hint.value!r} uniquely target {expected_state.ref}, while "
                f"{actual_target.ref} is independently bound as {foreign_role!r}."
            ),
            strongest_rebuttal=(
                "Treating the actual target as an alias for the required concept would "
                "conflict with its independent typed target role and the unique sibling "
                "carrier target."
            ),
            reason="Exact source carriers map one typed target concept inconsistently, and the divergent target has a distinct independently established role.",
            basis=(
                f"concept={target_hint.value}; source_transition_id={source_carrier.transition_id}; "
                f"expected_target_ref={expected_state.ref}; actual_target_ref={actual_target.ref}; "
                f"foreign_role={foreign_role}; sibling_transition_ids="
                f"{[row[3].transition_id for row in sibling_rows]}"
            ),
        )
        builder.add(
            "wrong_target",
            tuple(
                dict.fromkeys(
                    [
                        base.contract_id,
                        *[row[0].contract_id for row in sibling_rows],
                        *[contract.contract_id for contract, _hint_value in foreign_roles],
                    ]
                )
            ),
            target_contract,
            candidate,
            reason="A condition-scoped carrier diverges from the unique sibling target for the same concept and instead reaches a separately typed target role.",
            basis="typed cross-contract relation plus exact source and ModelIR transition identities",
        )


def _missing_endpoint_rows(
    pair: PairInput, contracts: Sequence[NLContract]
) -> list[tuple[NLContract, StateNode, StateNode]]:
    rows = []
    for contract in contracts:
        if (
            contract.property != "transition_endpoints"
            or contract.expected_direction
            not in {"must_exist", "must_reach", "must_eventually_reach"}
        ):
            continue
        source_hint = _hint(contract, "source")
        target_hint = _hint(contract, "target")
        source = _state_for_value(pair, source_hint.value if source_hint else None)
        target = _state_for_value(pair, target_hint.value if target_hint else None)
        if not source or not target:
            continue
        if any(
            item.source_ref == source.ref and item.target_ref == target.ref
            for item in pair.model.transitions
        ):
            continue
        rows.append((contract, source, target))
    return rows


def _wrapper_under(pair: PairInput, state: StateNode, owner: StateNode) -> StateNode | None:
    return _direct_child_under(pair, state, owner)


def _operating_contracts_for_state(
    pair: PairInput,
    contracts: Sequence[NLContract],
    state: StateNode,
) -> list[NLContract]:
    matches: list[NLContract] = []
    for contract in contracts:
        if contract.state_role != "operating_state":
            continue
        state_hint = (
            _hint(contract, "state")
            or _hint(contract, "target")
            or _hint(contract, "owner")
        )
        bound_state = _state_for_value(
            pair, state_hint.value if state_hint else None
        )
        if bound_state is not None and bound_state.ref == state.ref:
            matches.append(contract)
    return matches


def _owner_transition_inventory(
    pair: PairInput, owner: StateNode
) -> tuple[list[str], list[str]]:
    facts = pair.inspection_facts
    if facts is None:
        return [], []
    scoped_transition_refs: list[str] = []
    named_source_refs: list[str] = []
    for transition in facts.transitions:
        source_state = _state_by_ref(pair, transition.resolved_source_ref)
        scope_state = _state_for_value(pair, transition.scope)
        in_owner_scope = bool(
            (
                source_state
                and (
                    source_state.ref == owner.ref
                    or _is_descendant(pair, source_state, owner)
                )
            )
            or (
                scope_state
                and (
                    scope_state.ref == owner.ref
                    or _is_descendant(pair, scope_state, owner)
                )
            )
        )
        if not in_owner_scope:
            continue
        scoped_transition_refs.append(transition.transition_ref)
        if transition.source != "[*]":
            named_source_refs.append(transition.transition_ref)
    return scoped_transition_refs, named_source_refs


def _materialize_aggregate_zero_behavior(
    builder: _Builder,
    contracts: Sequence[NLContract],
    chain: Sequence[tuple[NLContract, StateNode, StateNode]],
    states: Sequence[StateNode],
    owner: StateNode,
    wrappers: Sequence[StateNode],
) -> None:
    pair = builder.pair
    facts = pair.inspection_facts
    if facts is None:
        return

    direct_sibling_chain = all(
        wrapper.ref == state.ref for wrapper, state in zip(wrappers, states)
    )
    composite_wrapper_chain = all(
        wrapper.ref != state.ref for wrapper, state in zip(wrappers, states)
    )
    if not direct_sibling_chain and not composite_wrapper_chain:
        return
    wrapper_facts = [_inspection_state(pair, wrapper.ref) for wrapper in wrappers]
    if composite_wrapper_chain and any(
        fact is None or not fact.is_composite for fact in wrapper_facts
    ):
        return

    operating_contracts: list[NLContract] = []
    state_facts: list[InspectionStateFact] = []
    for state in states:
        state_contracts = _operating_contracts_for_state(pair, contracts, state)
        state_fact = _inspection_state(pair, state.ref)
        if (
            not state_contracts
            or state_fact is None
            or state_fact.outgoing_transition_refs
        ):
            return
        if direct_sibling_chain and not state_fact.reachable_from_initial:
            return
        operating_contracts.extend(state_contracts)
        state_facts.append(state_fact)

    scoped_transition_refs, named_source_refs = _owner_transition_inventory(
        pair, owner
    )
    if named_source_refs:
        return

    chain_contracts = [item[0] for item in chain]
    source_contracts = list(
        dict.fromkeys(
            [
                *[item.contract_id for item in chain_contracts],
                *[item.contract_id for item in operating_contracts],
            ]
        )
    )
    base = chain_contracts[0]
    derived = _derived_contract(
        base,
        locus_kind="scope",
        locus_names=tuple(state.name for state in states),
        property_name="deadlock_freedom",
        state_role="operating_state",
        expected_direction="must_progress",
        violation_direction="dead_end",
        evidence_types=(
            "source_identity",
            "closed_model_inventory",
            "transition_fact",
            "deadlock_frontier_fact",
            "verify_fact",
            "semantic_comparison",
        ),
        normative_statement=(
            f"The required operating sequence under {owner.name} must contain "
            "named-state behavior that continues across its operating states."
        ),
        scope=f"Aggregate operating continuation under {owner.name}",
        source_refs=_source_refs([*chain_contracts, *operating_contracts]),
        reason=(
            "Exact endpoint contracts establish one sequence across distinct "
            "operating loci, and exact operating contracts establish every member "
            "as an active operating state."
        ),
        basis=(
            "typed operating sequence plus exact operating-state bindings and "
            "complete owner-subtree transition inventory"
        ),
    )
    element_refs = [
        owner.ref,
        *[wrapper.ref for wrapper in wrappers],
        *[state.ref for state in states],
        *scoped_transition_refs,
    ]
    candidate = _candidate(
        derived,
        title=f"Operating scope {owner.name} is a zero-behavior stub",
        predicate_id=None,
        predicate_inputs={},
        element_refs=element_refs,
        source_refs=derived.source_refs,
        expected=derived.normative_statement,
        observed=(
            f"The complete closed transition inventory under {owner.name} has "
            f"named_source_transition_refs=[]; operating states "
            f"{[state.name for state in states]} each have "
            f"outgoing_transition_refs=[] with reachable_from_initial="
            f"{[item.reachable_from_initial for item in state_facts]}. All scoped "
            f"transitions are pseudo-state entries {scoped_transition_refs}."
        ),
        strongest_rebuttal=(
            "Pseudo-state entries make the states reachable, but an entry from [*] "
            "is not named-state continuation and cannot realize the required "
            "operating sequence."
        ),
        reason=(
            "Every named state in the exact operating chain has no outgoing behavior, "
            "and the complete owner subtree contains no transition sourced from any "
            "named state; unreachable wrapper-local states remain part of this global "
            "zero-behavior defect without becoming reachable-deadlock findings."
        ),
        basis=(
            f"owner_ref={owner.ref}; state_refs={[item.state_ref for item in state_facts]}; "
            f"wrapper_refs={[item.ref for item in wrappers]}; "
            f"scoped_transition_refs={scoped_transition_refs}; "
            f"named_source_transition_refs={named_source_refs}; "
            f"inspection={facts.algorithm_version}"
        ),
    )
    builder.add(
        "aggregate_zero_behavior",
        source_contracts,
        derived,
        candidate,
        reason=(
            "One typed operating sequence shares a complete zero-named-source "
            "transition cause across all of its named operating states."
        ),
        basis=(
            "exact multi-contract chain, common-owner ancestry, operating-state "
            "contracts, and complete inspection-equivalent transition inventory"
        ),
    )


def _materialize_aggregate_data_semantics(
    builder: _Builder,
    contracts: Sequence[NLContract],
) -> None:
    """Aggregate complete action/effect gaps sharing one typed data subject."""

    pair = builder.pair
    source_ir = pair.canonical_source_ir
    source_inventory = pair.exact_source_inventory
    if source_ir is None or source_inventory is None:
        return
    by_variable: dict[str, list[NLContract]] = defaultdict(list)
    for contract in contracts:
        if contract.property not in {"state_action", "effect", "variable_delta"}:
            continue
        variable_hints = [
            hint for hint in contract.binding_hints if hint.role == "variable"
        ]
        if len(variable_hints) == 1:
            by_variable[variable_hints[0].value].append(contract)

    source_variables = tuple(source_ir.model.variables)
    source_transition_actions = tuple(
        transition
        for transition in source_ir.model.transitions
        if transition.action is not None
    )
    model_state_actions = tuple(
        state
        for state in pair.model.states
        if any(state.actions.values())
    )
    model_transition_effects = tuple(
        transition for transition in pair.model.transitions if transition.effects
    )
    if (
        source_variables
        or source_transition_actions
        or model_state_actions
        or model_transition_effects
    ):
        return

    for variable_name, rows in by_variable.items():
        properties = {contract.property for contract in rows}
        segment_ids = {contract.segment_id for contract in rows}
        if (
            len(segment_ids) < 2
            or "state_action" not in properties
            or not properties.intersection({"effect", "variable_delta"})
        ):
            continue
        rows = sorted(rows, key=lambda item: (item.segment_id, item.contract_id))
        base = rows[0]
        variable_hint = next(
            hint for hint in base.binding_hints if hint.role == "variable"
        )
        hints_by_key: dict[tuple[str, str], ContractBindingHint] = {
            ("variable", variable_name): variable_hint
        }
        for contract in rows:
            for hint in contract.binding_hints:
                if hint.role in {
                    "state",
                    "source",
                    "target",
                    "transition",
                    "action",
                    "effect",
                }:
                    hints_by_key.setdefault((hint.role, hint.value), hint)
        bound_states = {
            state.ref: state
            for contract in rows
            for hint in contract.binding_hints
            if hint.role in {"state", "source", "target"}
            if (state := _state_for_value(pair, hint.value)) is not None
        }
        for contract in rows:
            if contract.locus_kind != "state" or len(contract.locus_names) != 1:
                continue
            locus_name = contract.locus_names[0]
            state = _state_for_value(pair, locus_name)
            if state is None:
                continue
            bound_states.setdefault(state.ref, state)
            hints_by_key.setdefault(
                ("state", locus_name),
                ContractBindingHint(
                    role="state",
                    value=locus_name,
                    source_ref=contract.segment_id,
                    reason=(
                        "The atomic contract's typed state locus is the exact "
                        "carrier for this data-side obligation."
                    ),
                    basis=(
                        f"contract_id={contract.contract_id}; locus_kind=state; "
                        f"locus_names={[locus_name]}"
                    ),
                ),
            )
        if not bound_states:
            continue
        bound_source_refs = [
            source_state.raw_ref
            for state in bound_states.values()
            for source_state in source_inventory.states
            if source_state.name == state.name
        ]
        source_refs = tuple(
            dict.fromkeys([*_source_refs(rows), *bound_source_refs])
        )
        aggregate_hints = tuple(hints_by_key.values())
        aggregate_property: ObligationProperty = (
            "variable_delta"
            if sum(hint.role == "effect" for hint in aggregate_hints) > 1
            else "effect"
        )
        derived = _derived_contract(
            base,
            locus_kind="variable",
            locus_names=(variable_name,),
            property_name=aggregate_property,
            state_role="operating_state",
            expected_direction="must_exist",
            violation_direction="wrong_effect",
            evidence_types=(
                "source_identity",
                "closed_model_inventory",
                "action_fact",
                "effect_fact",
                "semantic_comparison",
            ),
            normative_statement=(
                f"The required data subject {variable_name!r} must have its complete "
                "declared state-action and transition-effect behavior represented."
            ),
            scope=f"Cross-contract data behavior for {variable_name}",
            source_refs=source_refs,
            reason=(
                "Multiple independent action/effect contracts share one exact typed "
                "variable concept and jointly establish its complete data-side behavior."
            ),
            basis="exact variable-role equality across contracts; no prose similarity or ledger data",
            quote=" | ".join(
                f"[{contract.segment_id}] {contract.quote}" for contract in rows
            ),
            binding_hints=aggregate_hints,
        )
        candidate = _candidate(
            derived,
            title=f"{variable_name} has no data-side representation",
            predicate_id=None,
            predicate_inputs={},
            element_refs=tuple(bound_states),
            source_refs=source_refs,
            expected=derived.normative_statement,
            observed=(
                "The complete typed inventories contain source_variables=[], "
                "source_transition_actions=[], model_state_actions=[], and "
                "model_transition_effects=[]."
            ),
            strongest_rebuttal=(
                "A consistent control-skeleton abstraction can carry some behavior "
                "implicitly, but it does not provide a declared data value or an "
                "observable carrier for all supplied display/update/cancel obligations."
            ),
            reason=(
                "Every action/effect obligation for the same typed data subject lacks "
                "a variable, state-action, or transition-effect carrier in the complete inventories."
            ),
            basis=(
                f"source_contract_ids={[item.contract_id for item in rows]}; "
                f"variable={variable_name!r}; canonical_source={source_ir.schema_version}; "
                f"bound_state_refs={list(bound_states)}; closed_model={pair.model.algorithm_version}"
            ),
        )
        builder.add(
            "aggregate_data_semantics",
            tuple(contract.contract_id for contract in rows),
            derived,
            candidate,
            reason="One typed data subject joins independent action/effect obligations whose complete carrier inventories are empty.",
            basis="typed variable binding plus complete canonical-source and closed-model action/effect inventories",
        )


def _materialize_cross_wrapper(builder: _Builder, contracts: Sequence[NLContract]) -> None:
    pair = builder.pair
    rows = _missing_endpoint_rows(pair, contracts)
    by_source = {source.ref: (contract, source, target) for contract, source, target in rows}
    chains: list[list[tuple[NLContract, StateNode, StateNode]]] = []
    for row in rows:
        chain = [row]
        seen = {row[1].ref}
        cursor = row[2]
        while cursor.ref in by_source and cursor.ref not in seen:
            seen.add(cursor.ref)
            next_row = by_source[cursor.ref]
            chain.append(next_row)
            cursor = next_row[2]
        if len(chain) >= 2:
            chains.append(chain)
    seen_chains: set[tuple[str, ...]] = set()
    for chain in chains:
        ids = tuple(item[0].contract_id for item in chain)
        if ids in seen_chains:
            continue
        seen_chains.add(ids)
        states = [chain[0][1], *[item[2] for item in chain]]
        ancestor_sets = [
            {item.ref: item for item in _ancestor_chain(pair, state)} for state in states
        ]
        common_refs = set.intersection(*(set(item) for item in ancestor_sets))
        owners = [
            item
            for item in _ancestor_chain(pair, states[0])
            if item.ref in common_refs and item.ref != states[0].ref
        ]
        owner = owners[0] if owners else None
        if owner is None:
            continue
        wrappers = [_wrapper_under(pair, state, owner) for state in states]
        if any(item is None for item in wrappers) or len(
            {item.ref for item in wrappers if item}
        ) < 2:
            continue
        exact_wrappers = tuple(item for item in wrappers if item is not None)
        wrapper_facts = [
            _inspection_state(pair, wrapper.ref) for wrapper in exact_wrappers
        ]
        direct_sibling_chain = all(
            wrapper.ref == state.ref
            for wrapper, state in zip(exact_wrappers, states)
        )
        if direct_sibling_chain:
            _materialize_aggregate_zero_behavior(
                builder,
                contracts,
                chain,
                states,
                owner,
                exact_wrappers,
            )
            continue
        if any(
            wrapper.ref == state.ref
            for wrapper, state in zip(exact_wrappers, states)
        ) or any(fact is None or not fact.is_composite for fact in wrapper_facts):
            continue
        scoped_transition_refs, named_source_refs = _owner_transition_inventory(
            pair, owner
        )
        globally_disconnected = not named_source_refs
        base = chain[0][0]
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=tuple(state.name for state in states),
            property_name="reachability",
            state_role="operating_state",
            expected_direction="must_reach",
            violation_direction="unreachable",
            evidence_types=("source_identity", "closed_model_inventory", "transition_fact", "reachability_fact", "semantic_comparison"),
            normative_statement=f"The required operating states under {owner.name} must have cross-wrapper reachability sufficient to realize the stated operating sequence.",
            scope=f"Cross-wrapper operating relation under {owner.name}",
            source_refs=_source_refs([item[0] for item in chain]),
            reason="Multiple typed endpoint contracts form one exact sequential chain across distinct wrappers under a common owner.",
            basis="contract source/target bindings, exact parent chains, and complete missing-edge inventory",
        )
        refs = [
            owner.ref,
            *[state.ref for state in states],
            *[item.ref for item in exact_wrappers],
        ]
        candidate = _candidate(
            derived,
            title=(
                f"Operating wrappers under {owner.name} are mutually disconnected"
                if globally_disconnected
                else f"Required cross-wrapper sequence under {owner.name} is disconnected"
            ),
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=(
                f"The complete closed transition inventory under {owner.name} has "
                f"named_source_transition_refs=[] and only pseudo-state entries "
                f"{scoped_transition_refs}; therefore operating states "
                f"{[state.name for state in states]} in wrappers "
                f"{[item.name for item in exact_wrappers]} cannot reach one another "
                "in any direction after entry."
                if globally_disconnected
                else (
                    "The complete closed transition inventory contains none of "
                    "the required chain edges "
                    f"{[f'{item[1].name}->{item[2].name}' for item in chain]} "
                    "across wrappers "
                    f"{[item.name for item in exact_wrappers]}."
                )
            ),
            strongest_rebuttal="Independent region-local initial edges do not establish the required cross-wrapper sequence.",
            reason=(
                "The LLM-established endpoint chain is exact, and the complete "
                "owner-subtree inventory has no transition sourced from any named "
                "state, which makes every participating wrapper mutually unreachable."
                if globally_disconnected
                else (
                    "The LLM-established endpoint chain is exact, and the complete "
                    "model contains none of its required links between distinct "
                    "wrapper scopes."
                )
            ),
            basis=(
                f"owner_ref={owner.ref}; contracts={list(ids)}; "
                f"state_refs={[state.ref for state in states]}; "
                f"wrapper_refs={[item.ref for item in exact_wrappers]}; "
                f"scoped_transition_refs={scoped_transition_refs}; "
                f"named_source_transition_refs={named_source_refs}"
            ),
        )
        builder.add(
            "cross_wrapper_reachability",
            ids,
            derived,
            candidate,
            reason="A typed multi-contract sequence spans distinct wrappers with no exact connecting transitions.",
            basis="exact contract chain, hierarchy, and complete transition inventory",
        )
        _materialize_aggregate_zero_behavior(
            builder,
            contracts,
            chain,
            states,
            owner,
            exact_wrappers,
        )


def _materialize_event_consumers(
    builder: _Builder,
    contracts: Sequence[NLContract],
    scopes: dict[str, tuple[StateNode, StateNode, NLContract]],
) -> None:
    pair = builder.pair
    if pair.inspection_facts is None:
        return
    grouped: dict[str, list[tuple[NLContract, str, tuple[str, ...]]]] = defaultdict(list)
    facts_by_event = {
        item.event: item for item in pair.inspection_facts.event_consumers
    }
    for scope, _descendant, base in scopes.values():
        for fact in pair.inspection_facts.event_consumers:
            if (
                not fact.consumer_transition_refs
                or fact.reachable_consumer_transition_refs
            ):
                continue
            refs: list[str] = [scope.ref]
            for transition_ref in fact.consumer_transition_refs:
                transition = pair.model.transition(transition_ref)
                source = _state_for_value(pair, transition.source) if transition else None
                if source is None or not (
                    source.ref == scope.ref or _is_descendant(pair, source, scope)
                ):
                    continue
                refs.extend((transition_ref, source.ref))
            if len(refs) > 1:
                grouped[scope.ref].append(
                    (base, fact.event, tuple(dict.fromkeys(refs)))
                )
    for contract in contracts:
        event_hints = [hint for hint in contract.binding_hints if hint.role == "event"]
        for hint in event_hints:
            fact = facts_by_event.get(hint.value)
            if (
                fact is None
                or not fact.consumer_transition_refs
                or fact.reachable_consumer_transition_refs
            ):
                continue
            refs_by_scope: dict[str, list[str]] = defaultdict(list)
            for transition_ref in fact.consumer_transition_refs:
                transition = pair.model.transition(transition_ref)
                source = _state_for_value(pair, transition.source) if transition else None
                scope = _highest_unreachable_scope(pair, source) if source else None
                if scope is None:
                    continue
                refs_by_scope[scope.ref].extend((transition_ref, source.ref))
            for scope_ref, consumer_refs in refs_by_scope.items():
                refs = tuple(
                    dict.fromkeys((scope_ref, *consumer_refs))
                )
                grouped[scope_ref].append((contract, fact.event, refs))
    for scope_ref, rows in grouped.items():
        scope = _state_by_ref(pair, scope_ref)
        if scope is None:
            continue
        base = rows[0][0]
        events = tuple(dict.fromkeys(item[1] for item in rows))
        refs = tuple(dict.fromkeys(ref for item in rows for ref in item[2]))
        derived = _derived_contract(
            base,
            locus_kind="scope",
            locus_names=(scope.name,),
            property_name="event_consumer_coverage",
            state_role="operating_state",
            expected_direction="must_cover",
            violation_direction="unconsumed",
            evidence_types=("source_identity", "closed_model_inventory", "event_consumer_fact", "reachability_fact", "verify_fact"),
            normative_statement=f"Required events {list(events)} must have reachable consumers in operating scope {scope.name}.",
            scope=f"Reachable event-consumer coverage of {scope.name}",
            source_refs=_source_refs([item[0] for item in rows]),
            reason="Typed event-response contracts bind exact consumer transitions below one unreachable operating scope.",
            basis="contract event roles, exact transition refs, and inspection-equivalent consumer reachability rows",
        )
        candidate = _candidate(
            derived,
            title=f"{scope.name} has declared but unreachable event consumers",
            predicate_id=None,
            predicate_inputs={},
            element_refs=refs,
            source_refs=derived.source_refs,
            expected=derived.normative_statement,
            observed=f"Events {list(events)} have declared consumer transitions, but their reachable_consumer_transition_refs are empty.",
            strongest_rebuttal="Declaration-only consumer existence does not satisfy operational reachable-consumer coverage.",
            reason="Exact event-consumer rows show consumers exist but none can execute from the model root.",
            basis=f"scope_ref={scope.ref}; events={list(events)}; consumer_refs={list(refs)}",
        )
        builder.add(
            "event_consumer_coverage",
            tuple(dict.fromkeys(item[0].contract_id for item in rows)),
            derived,
            candidate,
            reason="One exact operating scope contains required declared consumers that are all unreachable.",
            basis="typed event contracts and exact inspection-equivalent event-consumer coverage",
        )


def _inspection_scope_state(pair: PairInput, fact: InspectionTransitionFact) -> StateNode | None:
    """Resolve one transition's exact enclosing scope from owned facts."""

    return _state_for_value(pair, fact.scope) if fact.scope else None


def _inspection_target_state(pair: PairInput, fact: InspectionTransitionFact) -> StateNode | None:
    """Resolve an inspection transition target without interpreting display text."""

    return _state_by_ref(pair, fact.resolved_target_ref)


def _inspection_initial_contract(
    pair: PairInput,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
    fact: InspectionTransitionFact,
) -> NLContract | None:
    """Choose an exact initial-entry contract for one conditional edge."""

    owner = _inspection_scope_state(pair, fact)
    target = _inspection_target_state(pair, fact)
    if owner is None or target is None:
        return None
    matches: list[tuple[int, NLContract]] = []
    for contract in contracts:
        if contract.property != "initial_entry":
            continue
        exact_owner_refs = {
            binding.model_element_ref
            for response in grounding_responses
            for binding in response.semantic_bindings
            if (
                binding.contract_id == contract.contract_id
                and binding.status == "exact"
                and binding.role in {"owner", "scope"}
                and binding.model_element_ref is not None
            )
        }
        exact_target_refs = {
            binding.model_element_ref
            for response in grounding_responses
            for binding in response.semantic_bindings
            if (
                binding.contract_id == contract.contract_id
                and binding.status == "exact"
                and binding.role in {"target", "state"}
                and binding.model_element_ref is not None
            )
        }
        owner_hints = [
            hint for hint in contract.binding_hints if hint.role in {"owner", "scope"}
        ]
        target_hints = [
            hint for hint in contract.binding_hints if hint.role in {"target", "state"}
        ]
        owner_match = owner.ref in exact_owner_refs or any(
            (_state_for_value(pair, hint.value) is not None)
            and _state_for_value(pair, hint.value).ref == owner.ref
            for hint in owner_hints
        )
        target_match = target.ref in exact_target_refs or any(
            (_state_for_value(pair, hint.value) is not None)
            and _state_for_value(pair, hint.value).ref == target.ref
            for hint in target_hints
        )
        if target_match and owner_match:
            matches.append((0, contract))
        elif target_match:
            matches.append((1, contract))
    if not matches:
        return None
    matches.sort(key=lambda item: (item[0], item[1].contract_id))
    return matches[0][1]


def _inspection_scope_contract(
    pair: PairInput,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
    scope: StateNode,
    *,
    allowed_properties: frozenset[str] | None = None,
) -> NLContract | None:
    """Find one supplied contract that exactly anchors a model scope."""

    exact_bindings = {
        binding.contract_id
        for response in grounding_responses
        for binding in response.cardinality_bindings
        if binding.status == "exact" and binding.owner_model_ref == scope.ref
    }
    exact_bindings.update(
        binding.contract_id
        for response in grounding_responses
        for binding in response.semantic_bindings
        if (
            binding.status == "exact"
            and binding.role in {"owner", "scope"}
            and binding.model_element_ref == scope.ref
        )
    )
    candidates: list[NLContract] = []
    for contract in contracts:
        if allowed_properties is not None and contract.property not in allowed_properties:
            continue
        if contract.contract_id in exact_bindings:
            candidates.append(contract)
            continue
        for hint in contract.binding_hints:
            if hint.role not in {"owner", "scope", "state"}:
                continue
            bound = _state_for_value(pair, hint.value)
            if bound is not None and bound.ref == scope.ref:
                candidates.append(contract)
                break
    if not candidates:
        return None
    return min(candidates, key=lambda item: item.contract_id)


def _materialize_inspection_diagnostics(
    builder: _Builder,
    contracts: Sequence[NLContract],
    grounding_responses: Sequence[GroundingResponse],
) -> None:
    """Project exact inspection diagnostics only through supplied norm anchors.

    Inspection facts identify a carrier and a deterministic structural fact; they
    do not create a normative obligation by themselves.  A candidate is therefore
    emitted only when an existing typed contract binds the same owner, state, or
    scope.  The projection keeps the real leaf/transition refs so a parent entry
    or display label cannot substitute for the observed carrier.
    """

    pair = builder.pair
    facts = pair.inspection_facts
    if facts is None:
        return

    for diagnostic in facts.diagnostics:
        if diagnostic.code == "INITIAL_ENTRY_CONDITIONAL":
            transition_ref = next(
                (ref for ref in diagnostic.refs if ref.startswith("transition:")),
                None,
            )
            fact = next(
                (
                    item
                    for item in facts.transitions
                    if item.transition_ref == transition_ref
                ),
                None,
            )
            contract = (
                _inspection_initial_contract(
                    pair, contracts, grounding_responses, fact
                )
                if fact
                else None
            )
            if fact is None:
                continue
            owner = _inspection_scope_state(pair, fact)
            target = _inspection_target_state(pair, fact)
            if owner is None or target is None:
                continue
            if contract is None:
                # An inspection diagnostic is an observed FCSTM fact, not a
                # source-side initial-entry obligation.  A containment, action,
                # cardinality, or generic scope contract cannot be relabelled
                # as an unconditional owner-local entry requirement.
                continue
            if any(
                item.kind == "owner_initial_entry"
                and contract.contract_id in item.source_contract_ids
                for item in builder.obligations
            ):
                # The typed initial-entry frontier already owns this contract;
                # the inspection diagnostic is supporting evidence, not a
                # second report for the same atomic obligation.
                continue
            derived = _derived_contract(
                contract,
                locus_kind="composite",
                locus_names=(owner.name, target.name),
                property_name="initial_entry",
                state_role=contract.state_role,
                expected_direction="must_enter",
                violation_direction="missing",
                evidence_types=tuple(
                    dict.fromkeys(
                        [
                            *contract.evidence_types,
                            "initial_entry_fact",
                            "transition_fact",
                        ]
                    )
                ),
                normative_statement=contract.normative_statement,
                scope=contract.scope,
                source_refs=contract.source_refs,
                reason="An exact initial-entry carrier is conditional, so it does not establish the required unconditional owner-local entry.",
                basis=(
                    "typed initial-entry contract plus inspection-equivalent "
                    "INITIAL_ENTRY_CONDITIONAL fact"
                ),
            )
            derived = derived.model_copy(
                update={"contract_id": canonical_contract_id(derived)}
            )
            candidate = _candidate(
                derived,
                title=f"{owner.name} initial entry to {target.name} is conditional",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(owner.ref, target.ref, fact.transition_ref),
                source_refs=contract.source_refs,
                expected=derived.normative_statement,
                observed=(
                    f"Exact initial carrier {fact.transition_ref} has triggers={list(fact.triggers)} "
                    f"and guard={fact.guard!r}."
                ),
                strongest_rebuttal="A separate ordinary transition or display label cannot replace the owner-local initial carrier's unconditional entry semantics.",
                reason=diagnostic.reason,
                basis=f"diagnostic={diagnostic.code}; refs={list(diagnostic.refs)}; scope={owner.ref}; target={target.ref}",
            )
            builder.add(
                "owner_initial_entry",
                (contract.contract_id,),
                derived,
                candidate,
                reason="The supplied initial-entry contract is joined to one exact conditional pseudostate edge.",
                basis="inspection-equivalent INITIAL_ENTRY_CONDITIONAL and exact ModelIR transition ref",
            )
            # The broader owner-local default-entry obligation is not an S3
            # claim.  A non-empty trigger on the same exact initial carrier is
            # independently expressible as S3 with an empty required set and
            # is separately supported by the restricted UML source admission.
            if fact.triggers:
                trigger_hints = (
                    ContractBindingHint(
                        role="owner",
                        value=owner.name,
                        source_ref=contract.segment_id,
                        reason="The scoped initial carrier belongs to this exact composite owner.",
                        basis=f"owner_ref={owner.ref}; diagnostic={diagnostic.code}",
                    ),
                    ContractBindingHint(
                        role="target",
                        value=target.name,
                        source_ref=contract.segment_id,
                        reason="The initial carrier enters this exact parser-resolved target.",
                        basis=f"target_ref={target.ref}; transition_ref={fact.transition_ref}",
                    ),
                    ContractBindingHint(
                        role="transition",
                        value=fact.transition_ref,
                        source_ref=contract.segment_id,
                        reason="The inspection fact names one exact conditional initial transition carrier.",
                        basis=f"diagnostic={diagnostic.code}; transition_ref={fact.transition_ref}",
                    ),
                )
                trigger_contract = _derived_contract(
                    derived,
                    locus_kind="transition",
                    locus_names=(owner.name, target.name),
                    property_name="trigger_set",
                    state_role=derived.state_role,
                    expected_direction="must_equal",
                    violation_direction="mismatched",
                    evidence_types=tuple(
                        dict.fromkeys(
                            [
                                *derived.evidence_types,
                                "trigger_fact",
                            ]
                        )
                    ),
                    normative_statement=(
                        f"The exact initial transition {fact.transition_ref} from "
                        f"{owner.name} to {target.name} must have an empty trigger set."
                    ),
                    scope=f"Initial pseudostate transition {fact.transition_ref}",
                    source_refs=derived.source_refs,
                    reason=(
                        "The exact initial transition carries a non-empty parsed "
                        "trigger set, which is independently checked without "
                        "relabeling the broader owner-local entry obligation."
                    ),
                    basis=(
                        f"diagnostic={diagnostic.code}; transition_ref={fact.transition_ref}; "
                        f"parsed_triggers={list(fact.triggers)}; "
                        "UML 2.5.1 14.5.6.7 Pseudostate::outgoing_from_initial"
                    ),
                    binding_hints=trigger_hints,
                )
                trigger_candidate = _candidate(
                    trigger_contract,
                    title=f"Initial transition {fact.transition_ref} has a trigger",
                    predicate_id="S3",
                    predicate_inputs={
                        "transition": fact.transition_ref,
                        "triggers": [],
                    },
                    element_refs=(owner.ref, target.ref, fact.transition_ref),
                    source_refs=trigger_contract.source_refs,
                    expected=trigger_contract.normative_statement,
                    observed=(
                        f"The exact initial carrier {fact.transition_ref} has "
                        f"parsed triggers={list(fact.triggers)}."
                    ),
                    strongest_rebuttal=(
                        "The admission checks only this exact initial transition's "
                        "trigger field; a guard-only defect or an ordinary transition "
                        "does not satisfy its typed source boundary."
                    ),
                    reason=(
                        "The inspection-equivalent fact proves that one exact initial "
                        "transition has a non-empty trigger set."
                    ),
                    basis=(
                        f"diagnostic={diagnostic.code}; transition_ref={fact.transition_ref}; "
                        f"owner_ref={owner.ref}; target_ref={target.ref}; "
                        f"parsed_triggers={list(fact.triggers)}"
                    ),
                )
                builder.add(
                    "initial_entry_trigger_set",
                    (contract.contract_id,),
                    trigger_contract,
                    trigger_candidate,
                    reason=(
                        "The conditional initial-entry diagnostic contains a non-empty "
                        "trigger field that is independently expressible by S3."
                    ),
                    basis=(
                        "inspection-equivalent INITIAL_ENTRY_CONDITIONAL, exact "
                        "ModelIR transition, and restricted UML initial-transition rule"
                    ),
                )
            continue

        if diagnostic.code == "LEAF_WITHOUT_OUTGOING":
            state_ref = next(
                (ref for ref in diagnostic.refs if ref.startswith("state:")),
                None,
            )
            state = _state_by_ref(pair, state_ref)
            if state is None:
                continue
            contract = next(
                (
                    item
                    for item in contracts
                    if item.property == "deadlock_freedom"
                    and (
                        any(
                            binding.contract_id == item.contract_id
                            and binding.status == "exact"
                            and binding.role in {"state", "owner", "scope", "target"}
                            and binding.model_element_ref == state.ref
                            for response in grounding_responses
                            for binding in response.semantic_bindings
                        )
                        or any(
                            (bound := _state_for_value(pair, hint.value)) is not None
                            and bound.ref == state.ref
                            for hint in item.binding_hints
                            if hint.role in {"state", "owner", "scope", "target"}
                        )
                    )
                ),
                None,
            )
            source_contract_ids: tuple[str, ...]
            if contract is None and state.parent_ref:
                owner = _state_by_ref(pair, state.parent_ref)
                anchor = (
                    _inspection_scope_contract(
                        pair,
                        contracts,
                        grounding_responses,
                        owner,
                        allowed_properties=frozenset({"cardinality"}),
                    )
                    if owner is not None
                    else None
                )
                if anchor is not None and owner is not None:
                    contract = _derived_contract(
                        anchor,
                        locus_kind="state",
                        locus_names=(state.name,),
                        property_name="deadlock_freedom",
                        state_role="operating_state",
                        expected_direction="must_progress",
                        violation_direction="dead_end",
                        evidence_types=(
                            *anchor.evidence_types,
                            "closed_model_inventory",
                            "reachability_fact",
                            "deadlock_frontier_fact",
                        ),
                        normative_statement=(
                            f"The exact reachable leaf {state.name} under "
                            f"operating scope {owner.name} must retain an "
                            "operational continuation."
                        ),
                        scope=f"Exact leaf continuation in {owner.name}",
                        source_refs=anchor.source_refs,
                        reason=(
                            "The inspection fact identifies an exact reachable "
                            "leaf, while the enclosing operating-scope contract "
                            "supplies the normative anchor; no state identity "
                            "was inferred from display text."
                        ),
                        basis=(
                            "exact StateNode.parent binding plus inspection-equivalent "
                            "LEAF_WITHOUT_OUTGOING fact"
                        ),
                        binding_hints=(
                            ContractBindingHint(
                                role="state",
                                value=state.name,
                                source_ref=anchor.segment_id,
                                reason="The parser-resolved leaf state is the exact carrier.",
                                basis=f"owner_ref={owner.ref}; state_ref={state.ref}",
                            ),
                        ),
                    )
                    source_contract_ids = (anchor.contract_id,)
                else:
                    source_contract_ids = ()
            else:
                source_contract_ids = (contract.contract_id,) if contract else ()
            if contract is None:
                continue
            candidate = _candidate(
                contract,
                title=f"{state.name} is a reachable leaf without outgoing transition",
                predicate_id=None,
                predicate_inputs={},
                element_refs=(state.ref,),
                source_refs=contract.source_refs,
                expected=contract.normative_statement,
                observed=f"Exact reachable leaf {state.ref} has no outgoing transition refs.",
                strongest_rebuttal="A transition owned by another state cannot provide continuation for this exact leaf carrier.",
                reason=(
                    diagnostic.reason
                    if source_contract_ids == (contract.contract_id,)
                    else contract.reason
                ),
                basis=(
                    f"diagnostic={diagnostic.code}; refs={list(diagnostic.refs)}; "
                    f"state={state.ref}; source_contract_ids={list(source_contract_ids)}"
                ),
            )
            builder.add(
                "reachable_dead_end",
                source_contract_ids,
                contract,
                candidate,
                reason="The supplied deadlock-freedom contract is joined to the exact reachable leaf reported by inspection facts.",
                basis="inspection-equivalent LEAF_WITHOUT_OUTGOING and exact state inventory",
            )
            continue

    grouped: dict[tuple[str, tuple[str, ...], str | None], list[InspectionTransitionFact]] = defaultdict(list)
    for fact in facts.transitions:
        # V1 and its guard-disjointness frontier are defined over one exact
        # native choice source.  A concurrent owner may contain multiple active
        # regions, but it is not itself the StateMachine source of every child
        # transition and cannot merge their event consumers into a synthetic
        # same-source nondeterministic choice.
        if not fact.resolved_source_ref or not fact.triggers:
            continue
        grouped[(fact.resolved_source_ref, tuple(fact.triggers), fact.guard)].append(fact)
    for (source_key, triggers, guard), rows in sorted(grouped.items()):
        target_keys = {fact.resolved_target_ref or "[*]" for fact in rows}
        if len(rows) < 2 or len(target_keys) < 2:
            continue
        scope = _state_by_ref(pair, source_key)
        if scope is None:
            continue
        contract = _inspection_scope_contract(
            pair,
            contracts,
            grounding_responses,
            scope,
            allowed_properties=frozenset({"guard_disjointness"}),
        )
        if contract is None:
            continue
        targets = [
            _state_by_ref(pair, fact.resolved_target_ref)
            for fact in rows
            if fact.resolved_target_ref is not None
        ]
        targets = [item for item in targets if item is not None]
        derived = _derived_contract(
            contract,
            locus_kind="scope",
            locus_names=(scope.name, *[item.name for item in targets]),
            property_name="guard_disjointness",
            state_role=contract.state_role,
            expected_direction="must_cover",
            violation_direction="wrong_guard",
            evidence_types=(
                "closed_model_inventory",
                "transition_fact",
                "trigger_fact",
                "guard_fact",
            ),
            normative_statement=(
                f"Transitions in {scope.name} selected by the same event/guard "
                "must not expose competing target outcomes."
            ),
            scope=f"Inspection event/guard frontier in {scope.name}",
            source_refs=contract.source_refs,
            reason="Exact transitions from one native source share an event/guard signature while exposing different target outcomes.",
            basis="inspection-equivalent native source ref, trigger, guard, and resolved-target refs",
        )
        derived = derived.model_copy(
            update={"contract_id": canonical_contract_id(derived)}
        )
        element_refs = tuple(
            dict.fromkeys(
                [scope.ref, *[fact.transition_ref for fact in rows], *[item.ref for item in targets]]
            )
        )
        candidate = _candidate(
            derived,
            title=f"{scope.name} has competing targets for the same event/guard",
            predicate_id=None,
            predicate_inputs={},
            element_refs=element_refs,
            source_refs=contract.source_refs,
            expected=derived.normative_statement,
            observed=(
                f"Exact transitions {[fact.transition_ref for fact in rows]} share "
                f"triggers={list(triggers)} and guard={guard!r}, with targets={sorted(target_keys)}."
            ),
            strongest_rebuttal="Different native source states or different event/guard signatures separate the alternatives; this candidate is limited to one exact source-state signature.",
            reason="The deterministic inspection inventory found one exact native-source event/guard group with more than one target outcome.",
            basis=f"source_ref={scope.ref}; triggers={list(triggers)}; guard={guard!r}; transition_refs={[fact.transition_ref for fact in rows]}",
        )
        builder.add(
            "transition_group_collision",
            (contract.contract_id,),
            derived,
            candidate,
            reason="The explicit guard-disjointness contract anchors a deterministic native-same-source event/guard collision frontier.",
            basis="native-source inspection transition grouping; no ledger or expected-specific input",
        )

    # A zero-trigger edge into an exact leaf is a completion transition.  It is
    # only a publishable frontier fact when an existing typed operating or
    # termination contract supplies the lifecycle anchor; inspection facts do
    # not create a norm by themselves.
    anchors = sorted(
        (
            contract
            for contract in contracts
            if contract.state_role in {"operating_state", "termination_state"}
        ),
        key=lambda item: item.contract_id,
    )
    if not anchors:
        return
    for fact in facts.transitions:
        if (
            fact.resolved_source_ref is None
            or fact.resolved_target_ref is None
            or fact.triggers
            or fact.guard is not None
        ):
            continue
        target_fact = _inspection_state(pair, fact.resolved_target_ref)
        if target_fact is None or target_fact.outgoing_transition_refs:
            continue
        source = _state_by_ref(pair, fact.resolved_source_ref)
        target = _state_by_ref(pair, fact.resolved_target_ref)
        if source is None or target is None:
            continue
        anchor = anchors[0]
        derived = _derived_contract(
            anchor,
            locus_kind="transition",
            locus_names=(source.name, target.name),
            property_name="trigger_set",
            state_role=anchor.state_role,
            expected_direction="must_exist",
            violation_direction="missing",
            evidence_types=(
                "source_identity",
                "closed_model_inventory",
                "transition_fact",
                "trigger_fact",
                "deadlock_frontier_fact",
            ),
            normative_statement=(
                f"The lifecycle transition from {source.name} to {target.name} "
                "must remain event-controlled rather than an untriggered completion edge."
            ),
            scope=f"Completion-edge control from {source.name} to {target.name}",
            source_refs=anchor.source_refs,
            reason="An exact zero-trigger transition enters a reachable leaf target under an existing lifecycle obligation.",
            basis="typed operating/termination anchor plus inspection-equivalent zero-trigger leaf-transition fact",
        )
        derived = derived.model_copy(
            update={"contract_id": canonical_contract_id(derived)}
        )
        candidate = _candidate(
            derived,
            title=f"{source.name} reaches {target.name} without a trigger",
            predicate_id=None,
            predicate_inputs={},
            element_refs=(source.ref, target.ref, fact.transition_ref),
            source_refs=anchor.source_refs,
            expected=derived.normative_statement,
            observed=(
                f"Exact transition {fact.transition_ref} has source={fact.source!r}, "
                f"target={fact.target!r}, triggers=[], guard=null; target {target.ref} "
                "has no outgoing transition refs."
            ),
            strongest_rebuttal="A deliberate terminal boundary would need an explicit typed termination reading; this candidate preserves the exact lifecycle carrier and leaves that distinction for D.",
            reason=(
                "The exact inspection fact records a zero-trigger transition into a leaf target. "
                + fact.reason
            ),
            basis=(
                f"diagnostic-free transition fact={fact.transition_ref}; "
                f"source_ref={source.ref}; target_ref={target.ref}; "
                f"anchor_contract={anchor.contract_id}; triggers=[]; guard=null; "
                "target_outgoing_transition_refs=[]"
            ),
        )
        builder.add(
            "stable_termination",
            (anchor.contract_id,),
            derived,
            candidate,
            reason="The exact lifecycle anchor is joined to one untriggered transition into a leaf target.",
            basis="owned ModelIR transition fields and inspection-equivalent leaf inventory",
        )


def materialize_typed_frontier(
    pair: PairInput,
    contracts: NLContractResponse,
    contracts_by_id: dict[str, NLContract],
    grounding_responses: Sequence[GroundingResponse],
    llm_candidates: Sequence[CandidateIssue],
) -> FrontierBatch:
    """Expand established typed obligations into systematic frontier candidates."""

    all_contracts = list(contracts_by_id.values())
    all_groups: list[NLTransitionGroup] = []
    seen_group_keys: set[str] = set()
    for group in [
        *contracts.transition_groups,
        *[
            item
            for response in grounding_responses
            for item in response.additional_transition_groups
        ],
    ]:
        encoded_key = json.dumps(
            transition_group_semantic_key(group).model_dump(mode="json"),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if encoded_key in seen_group_keys:
            continue
        seen_group_keys.add(encoded_key)
        all_groups.append(group)
    builder = _Builder(pair, llm_candidates, contracts_by_id)
    _materialize_containment(builder, all_contracts, all_groups)
    _materialize_cardinality(
        builder, all_contracts, grounding_responses, llm_candidates
    )
    _materialize_initial_entries(builder, all_contracts, all_groups)
    scopes = _materialize_root_reachability(builder, all_contracts, llm_candidates)
    _materialize_dead_ends(builder, all_contracts, grounding_responses)
    _materialize_termination(builder, all_contracts)
    _materialize_group_guards(builder, all_groups, all_contracts)
    _materialize_group_post_states(builder, all_groups, all_contracts)
    _materialize_group_collisions(builder, all_groups, all_contracts)
    _materialize_wrong_targets(builder, all_contracts, all_groups, grounding_responses)
    _materialize_aggregate_data_semantics(builder, all_contracts)
    _materialize_cross_wrapper(builder, all_contracts)
    _materialize_event_consumers(builder, all_contracts, scopes)
    _materialize_inspection_diagnostics(builder, all_contracts, grounding_responses)
    return FrontierBatch(
        obligations=tuple(builder.obligations),
        checks=tuple(builder.checks),
        superseded_candidate_contract_ids=tuple(
            builder.superseded_candidate_contract_ids
        ),
        reason="The runner systematically expanded LLM-established typed obligations through the typed domain frontier before predicate selection.",
        basis=(
            "NLContractResponse and grounding semantic identities; owned ModelIR; "
            f"source_inventory={pair.exact_source_inventory.algorithm_version if pair.exact_source_inventory else 'unavailable'}; "
            f"inspection={pair.inspection_facts.algorithm_version if pair.inspection_facts else 'unavailable'}"
        ),
    )


__all__ = [
    "ContractSemanticKey",
    "FrontierBatch",
    "FrontierCheckReceipt",
    "FrontierObligation",
    "GroupIdentityNormalizationReceipt",
    "IdentityNormalizationReceipt",
    "TransitionAlternativeSemanticKey",
    "TransitionGroupSemanticKey",
    "canonical_contract_id",
    "canonical_transition_group_id",
    "canonicalize_grounding_response",
    "contract_semantic_key",
    "materialize_typed_frontier",
    "transition_group_semantic_key",
]
