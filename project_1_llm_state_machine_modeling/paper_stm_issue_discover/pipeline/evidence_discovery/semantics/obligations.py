from __future__ import annotations

from typing import Annotated, Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.models import PairInput


PredicateId = Literal[
    "S1", "S2", "S3", "S4", "S5", "S6",
    "G1", "G2", "G3", "G4",
    "R1", "R2", "R3", "R4",
    "V1", "V2", "V3", "V4", "V5",
]

ObligationLocusKind = Literal[
    "model",
    "state",
    "transition",
    "composite",
    "region",
    "event",
    "action",
    "variable",
    "path",
    "scenario",
    "scope",
    "other",
]

ObligationProperty = Literal[
    "element_declaration",
    "containment",
    "cardinality",
    "initial_entry",
    "transition_endpoints",
    "trigger_set",
    "state_action",
    "guard",
    "effect",
    "reachability",
    "universal_reachability",
    "route_avoidance",
    "coaccessibility",
    "event_consumption",
    "state_after_stimulus",
    "behavior_occurrence",
    "state_retention",
    "guard_disjointness",
    "guard_completeness",
    "bounded_response",
    "deadlock_freedom",
    "state_invariant",
    "event_consumer_coverage",
    "region_structure",
    "variable_delta",
    "termination",
    "excess_behavior",
    "other",
]

ExpectedDirection = Literal[
    "must_exist",
    "must_not_exist",
    "must_equal",
    "must_reach",
    "must_eventually_reach",
    "must_avoid",
    "must_occur",
    "must_remain",
    "must_progress",
    "must_cover",
    "must_be_contained",
    "must_enter",
    "must_terminate",
    "other",
]

ViolationDirection = Literal[
    "missing",
    "extra",
    "mismatched",
    "unreachable",
    "dead_end",
    "unconsumed",
    "wrong_scope",
    "wrong_target",
    "wrong_guard",
    "wrong_effect",
    "not_retained",
    "not_completed",
    "unsupported_expression",
    "other",
]

EvidenceType = Literal[
    "source_identity",
    "closed_model_inventory",
    "transition_fact",
    "initial_entry_fact",
    "containment_fact",
    "reachability_fact",
    "deadlock_frontier_fact",
    "event_consumer_fact",
    "guard_fact",
    "effect_fact",
    "action_fact",
    "trace_fact",
    "verify_fact",
    "smt_fact",
    "semantic_comparison",
    "other",
]


class ContractBindingHint(BaseModel):
    """One source-side binding hint carried from an atomic NL contract.

    A hint is not a model binding and does not prove satisfaction or violation.
    It preserves a role and source phrase so the grounding branches can locate
    exact author-source and closed-model identities without reversing the
    requirement direction.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    role: Literal[
        "owner",
        "scope",
        "source",
        "target",
        "transition",
        "event",
        "state",
        "action",
        "phase",
        "guard",
        "effect",
        "variable",
        "root",
        "marked",
        "forbidden",
        "scenario",
        "window",
        "bound",
        "unit",
        "other",
    ] = Field(description="Semantic argument role of this source-side hint; this is not a frozen predicate input name unless grounding later binds it exactly. For initial_entry, owner is the scope that owns the required initial pseudostate edge and target is the state entered by that edge; the entered state is not its own owner unless the NL explicitly states a nested self-owned obligation.")
    value: str = Field(min_length=1, description="Source-grounded name, phrase, expression, or scope value copied or faithfully normalized from the supplied NL.")
    source_ref: str | None = Field(default=None, description="Exact supplied NL or author-source reference supporting this hint, or null when only the parent contract source refs apply.")
    reason: str = Field(min_length=1, description="LLM explanation of why this value has the declared semantic role in the atomic contract.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied NL clause or author-source fact used for this hint.")

class CandidateIssue(BaseModel):
    """One LLM-generated candidate with explicit audit rationale.

    The model deliberately excludes W, D, and L. Evidence and disposition
    levels are computed by deterministic method code after this response is
    parsed. ``reason`` explains the model's judgment and ``basis`` names the
    supplied requirement/model facts used for it. The raw value is preserved so
    an auditor can review the model's own explanation without translation.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Exact atomic NL contract ID evaluated by this candidate; copy it from the supplied contract plan and never invent, merge, or omit it.")
    locus_kind: ObligationLocusKind = Field(description="Typed semantic kind of the requirement locus; preserve the contract's locus kind rather than substituting a nearby declared element.")
    locus_names: tuple[Annotated[str, Field(min_length=1)], ...] = Field(min_length=1, description="One or more source-grounded names identifying the exact semantic locus; these are semantic identities, while element_refs carry exact FCSTM refs.")
    property: ObligationProperty = Field(description="Exact atomic property being evaluated; preserve the contract property even when no frozen predicate fully expresses it.")
    violation_direction: ViolationDirection = Field(description="Observed defect direction for this candidate; do not reverse a missing/dead-end/unreachable obligation into an unrelated existence claim.")
    evidence_types: tuple[EvidenceType, ...] = Field(
        min_length=1,
        description=(
            "Structured evidence families actually used to form this candidate. "
            "Allowed values are exactly source_identity, closed_model_inventory, "
            "transition_fact, initial_entry_fact, containment_fact, "
            "reachability_fact, deadlock_frontier_fact, event_consumer_fact, "
            "guard_fact, effect_fact, action_fact, trace_fact, verify_fact, "
            "smt_fact, semantic_comparison, and other. Unknown, error, or not-run "
            "facts are not violation evidence; state_action is a property name, "
            "not an evidence type."
        ),
    )
    title: str = Field(min_length=1, description="Short human-readable issue title; do not include a verdict level.")
    requirement_quote: str = Field(min_length=1, description="Exact or faithful quote of the supplied requirement supporting this candidate.")
    predicate_id: PredicateId | None = Field(default=None, description="One frozen predicate ID, or null when the precise claim is not expressible by the registry.")
    predicate_inputs: dict[str, Any] = Field(default_factory=dict, description="Only the frozen predicate's named inputs; do not invent semantic fields or answer data.")
    element_refs: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list, description="Stable closed-FCSTM element references that bind the candidate to the executable model. Put PlantUML/canonical/source/macro identities in source_refs, not here. A source identity is provenance and must not masquerade as a closed-model element.")
    source_refs: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list, description="Exact requirement, PlantUML, canonical-source, mapping, or supplied-artifact locations used for provenance. These refs localize author source and do not by themselves prove closed-model satisfaction or violation.")
    expected: str = Field(min_length=1, description="Requirement-side expected behavior or structural fact.")
    observed: str = Field(min_length=1, description="Observed supplied-model fact that may conflict with the requirement.")
    strongest_rebuttal: str = Field(min_length=1, description="Strongest fact-based alternative interpretation that could defeat the issue.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this candidate was generated from the supplied inputs.")
    basis: str = Field(min_length=1, description="Non-empty evidence basis naming the supplied requirement/model facts used by the LLM.")


class MethodResponse(BaseModel):
    """Complete structured response emitted by one method-generation cell.

    ``reason`` and ``basis`` explain the overall generation decision even when
    no issue is returned. The response has no access to ledger answers,
    baseline results, or judge examples.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    issues: list[CandidateIssue] = Field(default_factory=list, description="Candidate issues generated only from the supplied requirement and model artifacts.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the overall method-generation decision for this cell.")
    basis: str = Field(min_length=1, description="Non-empty basis identifying the supplied inputs used by the method for this cell.")


def build_method_prompt(pair: PairInput, round_index: int, previous: list[dict[str, Any]]) -> str:
    """Build the staged v27-shaped compatibility prompt.

    The implementation lives in ``workflow.py`` so the legacy obligation
    models remain importable without creating a module cycle.
    """

    from .workflow import build_method_prompt as build_staged_method_prompt

    return build_staged_method_prompt(pair, round_index, previous)
