"""v27-shaped method stages for contract extraction and complementary grounding."""

from __future__ import annotations

import hashlib
import json
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
    normative_statement: str = Field(min_length=1, description="Atomic source obligation stated without judging whether the current model satisfies it.")
    locus_kind: ObligationLocusKind = Field(description="Typed semantic kind of the source obligation locus; choose the object whose property can be violated, not a nearby declared element.")
    locus_names: tuple[str, ...] = Field(min_length=1, description="Source-grounded names that identify the exact obligation locus before model binding; keep one independently violable semantic locus per contract.")
    property: ObligationProperty = Field(description="Atomic property required at the locus; this vocabulary includes the frozen predicate meanings and explicit unsupported semantic boundaries.")
    state_role: StateSemanticRole | None = Field(
        default=None,
        description=(
            "v27 semantic role of the state centered by this contract, or null "
            "when the locus is not one state concept. An operating state denotes "
            "active behavior that must retain a response/progress interpretation; "
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
    binding_hints: tuple[ContractBindingHint, ...] = Field(default_factory=tuple, description="Typed source-side argument hints used by both grounding branches; each hint remains distinct from an exact FCSTM binding. One transition-property contract may identify at most one source, one target, and one transition; split alternative endpoints into separate contracts.")
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

    contracts: list[NLContract] = Field(default_factory=list, description="Complete list of atomic contracts covering normative numbered NL segments; descriptive segments may be omitted with an explained top-level basis. A schema-correction turn must repeat every valid contract and return a complete replacement list, not only the corrected row.")
    segment_disposition: dict[str, Literal["covered", "context", "ambiguous"]] = Field(default_factory=dict, description="Disposition for supplied NL segment IDs only; every key must be an input segment ID.")
    reason: str = Field(min_length=1, description="LLM explanation of the overall contract extraction decision.")
    basis: str = Field(min_length=1, description="LLM basis identifying the supplied NL segments and source context used.")

    @model_validator(mode="after")
    def validate_unique_contract_ids(self) -> NLContractResponse:
        """Require one row per exact contract identity within the response."""

        contract_ids = [contract.contract_id for contract in self.contracts]
        if len(contract_ids) != len(set(contract_ids)):
            raise ValueError(
                "contracts must contain each contract_id at most once; return "
                "a complete replacement response with duplicate IDs removed"
            )
        return self


class GroundingDisposition(BaseModel):
    """One branch's explicit disposition for one atomic NL contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Exact supplied atomic contract ID reviewed by this grounding branch.")
    status: Literal["candidate_emitted", "satisfied", "unresolved", "not_applicable"] = Field(description="Branch result for this contract; unresolved preserves insufficient facts, while satisfied and not_applicable require a reason grounded in supplied branch facts.")
    candidate_count: int = Field(ge=0, description="Number of candidates in this same response carrying this exact contract ID; deterministic normalization audits this count.")
    reason: str = Field(min_length=1, description="LLM explanation of why this branch emitted candidates or assigned the stated non-candidate disposition for this contract.")
    basis: str = Field(min_length=1, description="LLM basis naming the branch-specific source or closed-model facts used for this one contract disposition.")


GroundingLens = Literal["contract_structure_contrast", "behavior_consequence"]


class GroundingResponse(BaseModel):
    """Structured LLM response for one v27 complementary discovery lens."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    lens: GroundingLens = Field(description="Exact v27 audit-lens identity; both lenses receive the same cross-view context and response contract.")
    candidates: list[CandidateIssue] = Field(default_factory=list, description="Candidate claims grounded across author source, closed FCSTM, and deterministic facts; each candidate must carry reason and basis and must not emit W/D/L levels.")
    contract_dispositions: list[GroundingDisposition] = Field(default_factory=list, description="One reasoned disposition per supplied atomic contract for this lens; missing rows are normalized to explicit unresolved receipts without semantic guessing.")
    reason: str = Field(min_length=1, description="LLM explanation of how this audit lens selected or rejected candidate claims.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied cross-view facts and contract IDs used by this lens.")


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
        "segment_disposition": contracts.segment_disposition,
        "reason": "Grounding receives each exact typed contract and source anchor while upstream LLM rationale remains in the hash-addressed contract stage output.",
        "basis": "contract-grounding-projection.v2 and full contract response hash",
    }


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


CONTRACT_SYSTEM_PROMPT = f"""You are the NL contract extraction stage of the paper1 evidence_discovery method. {COMMON_RULES} Extract atomic source obligations before inspecting model satisfaction. For every contract, fill the typed semantic key `(locus_kind, locus_names, property, state_role, expected_direction, violation_direction, evidence_types)` and typed binding hints. Split independently violable containment, initialization, transition endpoint, trigger, guard, effect, action, reachability, progress, event-consumer, region, variable-delta, and excess-behavior clauses instead of bundling them. Preserve qualifiers, ordering, initialization/operation/termination scope, and ambiguity. The violation direction says what later grounding must test; it does not claim that the defect exists. Keep each per-contract reason and basis concise and specific; do not restate the full input context.

Allowed `evidence_types` values are exactly: `source_identity`, `closed_model_inventory`, `transition_fact`, `initial_entry_fact`, `containment_fact`, `reachability_fact`, `deadlock_frontier_fact`, `event_consumer_fact`, `guard_fact`, `effect_fact`, `action_fact`, `trace_fact`, `verify_fact`, `smt_fact`, `semantic_comparison`, and `other`. Do not put a property name in this field: for example, `property=state_action` uses `evidence_types=[action_fact]`, never `state_action`.

Atomic contract shape:
- One contract represents one property at one independently violable locus. A transition-property row has at most one source, one target, and one transition hint.
- Alternative destinations are separate endpoint contracts. A guard conjunction for one exact transition remains one normalized guard hint; guards attached to different transitions are separate contracts.
- A bidirectional or dynamic A-to-B/B-to-A requirement is two endpoint contracts. Never place two source hints or two target hints in one contract.
- A conjunction such as `a and b and c` on one transition is one normalized guard hint with the complete conjunction as its value, not three guard hints. Alternative guards on different transitions remain separate contracts.
- Initialization, containment, endpoint, trigger, guard, effect, action, reachability/progress, event-consumer coverage, region structure, and variable delta never share one contract merely because the NL states them in one sentence.
- `wrong_target` belongs to `transition_endpoints`, `wrong_guard` to `guard`, `wrong_effect` to `effect` or `variable_delta`, `unreachable` to `reachability`, `dead_end` to `deadlock_freedom`, and `unconsumed` to `event_consumer_coverage`. Do not encode one property with another property's direction.
- When an event is semantically required to be accepted within a scope, emit a separate `event_consumer_coverage` contract in addition to any local endpoint/trigger contract. This is a semantic LLM judgment from the supplied NL, never a spelling or keyword rule.

v27 state-role and discourse discipline:
- Preserve the semantic role of every state-centered obligation in `state_role`. Use `operating_state` for an active control state or substate whose behavior must react, continue, or lead onward; use `termination_state` only when the NL explicitly establishes completion or intended terminal behavior. A name that sounds like stopping, emergency, final, or completion is not itself terminal evidence.
- For each semantically active operating state, emit one separate `deadlock_freedom` contract with `expected_direction=must_progress`, `violation_direction=dead_end`, and the exact state as its locus. This contract states the v27 progress/response obligation before model inspection. Grounding will decide from exact finite facts whether the state has an outgoing or inherited continuation, an explicit terminal route, or a dead-end frontier. Do not emit this contract for an explicitly intended terminal state.
- Treat an explicit "first transitions/enters" clause as `initial_entry` into the first state under the enclosing operating owner, not as an ordinary transition from a word such as system or controller. In an initial-entry contract, `owner` is the scope that owns the required initial pseudostate edge and `target` is the state entered by that edge. Thus "the system begins in Controller" yields owner=root/system and target=Controller, while a later "within Controller, first enter ModeA" yields owner=Controller and target=ModeA. Never make the entered target its own owner merely because it is described as a composite. Resolve later omitted sources and enclosing owners by discourse semantics. A sequence such as "first enter ModeA; it can then transition to ModeB; similarly it transitions to ModeC" yields owner initial-entry to ModeA, ModeA-to-ModeB, and ModeB-to-ModeC. By contrast, "from ModeA choose either ModeB or ModeC" yields two alternatives from ModeA. This is an LLM coreference and ordering judgment; never decide it by keywords or identifier spelling.
- Keep a state-owned action/effect independent from the endpoint that enters the state. The action may remain a precise unsupported W1 obligation even when the endpoint exists.
- Preserve containment depth from the NL. A state described only as being "within" or "under" a composite requires semantic descendant containment; an intermediate region or nested composite still satisfies that obligation. Require direct/immediate ownership only when the source meaning explicitly requires no intermediate owner. Region or wrapper structure is a separate contract only when the NL independently specifies that structure or its concurrency semantics.

Generic worked example: "Within Controller, start in Idle; on Begin transition from Idle to Running when enabled and set mode=active" yields separate contracts for Controller containment of Idle, Controller initial entry to Idle, the Idle-to-Running endpoint, its Begin trigger set, its enabled guard, and its mode=active effect. If the clause also requires Begin to be accepted throughout Controller, that coverage requirement is a separate event-consumer contract. Do not copy the whole sentence into one multi-property contract.

Return only the requested Pydantic structure."""


DISCOVERY_GROUNDING_SYSTEM_PROMPT = f"""You are one complementary discovery-grounding lens of the paper1 evidence_discovery method. {COMMON_RULES} In one cross-view response, use NL contracts, PlantUML, canonical source IR, exact source inventory, working contract, and source trace to locate author-source obligations, then use FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries to bind exact closed-model elements and propose candidates. PlantUML/canonical source is author localization, FCSTM is the closed model under test, and inspection/verify/SMT rows are deterministic facts; never substitute one role for another. Do not rewrite an NL contract to match the model, claim that source presence proves execution, or treat unknown/not-run facts as violations.

Every candidate must copy one exact `contract_id` and preserve that contract's
`locus_kind`, `locus_names`, `property`, and `violation_direction`. Evaluate the
contract property first, then select the minimal frozen predicate that decides
that same property. Do not substitute a nearby endpoint, declaration, or local
path property merely because it is executable. Record the evidence families
actually used in `evidence_types`.

Emit a candidate only for a possible violated obligation or a precisely bound
semantic gap that must remain W1. When the supplied source/model facts satisfy a
contract, return its disposition as `satisfied` and emit no candidate for that
contract. Predicate/backend unavailability does not turn a satisfied fact into
an issue and is not by itself semantic ambiguity.

Every candidate object must explicitly include `locus_kind` and `locus_names`
copied from its contract. `predicate_inputs` must always be a JSON object; use
an empty object when predicate_id is null, never a list or free-text value.
Every candidate and contract disposition must include its own non-empty reason
and basis. These are structural output obligations, not optional prose.

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

Interpret containment at the depth stated by the contract. Transitive descendant
containment through a region satisfies an ordinary within-scope containment
contract; do not emit a wrong-scope issue solely because the state is not a
direct child. Direct ownership and region/concurrency structure require their own
explicit source obligations.

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

When one NL sentence contains multiple obligations, split them before rejecting
the contract. A satisfied endpoint or declaration does not discharge an attached
ordering, guard, effect, action, containment, region, consumer, or progress clause.
For every such unsatisfied or unsupported conjunct, preserve the exact model
locus and emit one atomic candidate; do not mark it satisfied or not_applicable
merely because a different conjunct is satisfied. A missing registered predicate
is a precise W1 candidate when the model locus is exact.

Return only the requested Pydantic structure."""


DISCOVERY_GROUNDING_AUDIT_LENSES: dict[GroundingLens, str] = {
    "contract_structure_contrast": """Prioritize contract completeness, structure, and contrastive consistency. Resolve exact source and closed-model identities before emitting a candidate. Audit omitted or collapsed direct contracts, containment and default-entry defects, guard/effect conflicts, unauthorized edges, and cross-context inconsistencies. An authored fact may be contrastive evidence only after the NL establishes the shared semantic role; never infer equivalence from labels, identifiers, or textual overlap.""",
    "behavior_consequence": """Prioritize behavioral consequence while still completing exact source and closed-model binding. Audit finite reachability, event-consumer coverage, forbidden-scope entry, dead-end/frontier facts, stable termination, and bounded response or trace obligations. Prefer the deepest sound consequence and its author-source cause, but do not replace a distinct structural defect or promote a finite/trace result beyond its registered soundness fragment.""",
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
element but an intentional terminal or synthetic-lowering reading remains
competent, use grounding=established with a surviving typed defeater so the
method can produce D1. Use grounding=unresolved only when the exact element,
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
NLContractResponse: preserve and repeat every already valid contract, correct each
invalid row in place, and keep every segment disposition. Never return only the
row named by the latest validation error.
"""


def build_grounding_prompt(
    pair: PairInput,
    *,
    lens: GroundingLens,
    round_index: int,
    contracts: NLContractResponse,
) -> str:
    """Build one v27 lens prompt over the shared compact cross-view closure."""

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
its target; an initial edge in a different owner scope is a different fact.
Return exactly one `contract_dispositions` row for every supplied contract ID.
Use `candidate_emitted` when this response contains one or more candidates for
that ID; otherwise use `satisfied`, `unresolved`, or `not_applicable` with a
contract-specific reason and basis. Do not silently omit a contract.

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


def normalize_grounding_dispositions(
    response: GroundingResponse,
    contracts: NLContractResponse,
) -> GroundingResponse:
    """Close exact contract accounting without making semantic decisions."""

    allowed_contract_ids = {
        contract.contract_id for contract in contracts.contracts
    }
    supplied = {
        item.contract_id: item
        for item in response.contract_dispositions
        if item.contract_id in allowed_contract_ids
    }
    normalized: list[GroundingDisposition] = []
    changed = len(supplied) != len(response.contract_dispositions)
    for contract in contracts.contracts:
        candidate_count = sum(
            candidate.contract_id == contract.contract_id
            for candidate in response.candidates
        )
        item = supplied.get(contract.contract_id)
        if item is None:
            normalized.append(
                GroundingDisposition(
                    contract_id=contract.contract_id,
                    status="candidate_emitted" if candidate_count else "unresolved",
                    candidate_count=candidate_count,
                    reason=(
                        "Candidates carry this exact contract ID, but the branch omitted its disposition row."
                        if candidate_count
                        else "The branch omitted this exact contract ID; deterministic normalization preserves it as unresolved."
                    ),
                    basis="exact contract ID coverage normalization; no semantic text inference",
                )
            )
            changed = True
            continue
        status = item.status
        if candidate_count and status != "candidate_emitted":
            status = "candidate_emitted"
            changed = True
        elif not candidate_count and status == "candidate_emitted":
            status = "unresolved"
            changed = True
        if item.candidate_count != candidate_count:
            changed = True
        normalized.append(
            item.model_copy(
                update={
                    "status": status,
                    "candidate_count": candidate_count,
                    "basis": (
                        item.basis
                        + "; candidate_count/status audited by exact contract ID"
                    ),
                }
            )
        )
    if not changed:
        return response.model_copy(update={"contract_dispositions": normalized})
    return response.model_copy(
        update={
            "contract_dispositions": normalized,
            "reason": response.reason
            + " Exact contract accounting was normalized without changing candidate semantics.",
            "basis": response.basis
            + "; exact contract ID coverage normalization",
        }
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
        candidates=[],
        contract_dispositions=[
            GroundingDisposition(
                contract_id=contract.contract_id,
                status="unresolved",
                candidate_count=0,
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
    "CONTRACT_SYSTEM_PROMPT",
    "DISCOVERY_GROUNDING_SYSTEM_PROMPT",
    "DISCOVERY_GROUNDING_AUDIT_LENSES",
    "D_SYSTEM_PROMPT",
    "GroundingDisposition",
    "GroundingResponse",
    "NLContract",
    "NLContractResponse",
    "StageReceipt",
    "assemble_method_response",
    "build_contract_prompt",
    "build_grounding_prompt",
    "build_d_adjudication_prompt",
    "build_d_correction_prompt",
    "build_method_prompt",
    "fallback_contracts",
    "fallback_grounding",
    "fallback_d_adjudication",
    "normalize_grounding_dispositions",
]
