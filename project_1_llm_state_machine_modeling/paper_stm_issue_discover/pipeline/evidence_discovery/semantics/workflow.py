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


class NLContract(BaseModel):
    """One typed, source-grounded obligation extracted from a numbered NL segment.

    The contract describes author intent only. Its typed semantic key keeps
    later grounding focused on the same locus, property, and direction without
    deciding whether the closed FCSTM satisfies or violates the obligation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Stable contract identifier derived from the supplied segment identifier.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Exact numbered NL segment identifier carried from the input closure.")
    quote: str = Field(min_length=1, description="Exact or faithful quote of the supplied NL segment; do not invent an answer or expected defect.")
    normative_statement: str = Field(min_length=1, description="Atomic source obligation stated without judging whether the current model satisfies it.")
    locus_kind: ObligationLocusKind = Field(description="Typed semantic kind of the source obligation locus; choose the object whose property can be violated, not a nearby declared element.")
    locus_names: tuple[str, ...] = Field(min_length=1, description="Source-grounded names that identify the exact obligation locus before model binding; keep one independently violable semantic locus per contract.")
    property: ObligationProperty = Field(description="Atomic property required at the locus; this vocabulary includes the frozen predicate meanings and explicit unsupported semantic boundaries.")
    expected_direction: ExpectedDirection = Field(description="Positive requirement direction stated by the NL, such as required existence, entry, reachability, progress, coverage, or absence.")
    violation_direction: ViolationDirection = Field(description="Defect direction that grounding must look for if the requirement is not met; it must not be reversed into a nearby existence observation.")
    evidence_types: tuple[EvidenceType, ...] = Field(min_length=1, description="Evidence families needed to assess this obligation; these route context but do not assert that evidence exists or proves a violation.")
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

    contracts: list[NLContract] = Field(default_factory=list, description="Atomic contracts covering normative numbered NL segments; descriptive segments may be omitted with an explained top-level basis.")
    segment_disposition: dict[str, Literal["covered", "context", "ambiguous"]] = Field(default_factory=dict, description="Disposition for supplied NL segment IDs only; every key must be an input segment ID.")
    reason: str = Field(min_length=1, description="LLM explanation of the overall contract extraction decision.")
    basis: str = Field(min_length=1, description="LLM basis identifying the supplied NL segments and source context used.")


class GroundingDisposition(BaseModel):
    """One branch's explicit disposition for one atomic NL contract."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Exact supplied atomic contract ID reviewed by this grounding branch.")
    status: Literal["candidate_emitted", "satisfied", "unresolved", "not_applicable"] = Field(description="Branch result for this contract; unresolved preserves insufficient facts, while satisfied and not_applicable require a reason grounded in supplied branch facts.")
    candidate_count: int = Field(ge=0, description="Number of candidates in this same response carrying this exact contract ID; deterministic normalization audits this count.")
    reason: str = Field(min_length=1, description="LLM explanation of why this branch emitted candidates or assigned the stated non-candidate disposition for this contract.")
    basis: str = Field(min_length=1, description="LLM basis naming the branch-specific source or closed-model facts used for this one contract disposition.")


class GroundingResponse(BaseModel):
    """Structured LLM response for one complementary grounding branch."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    branch: Literal["source", "model"] = Field(description="Grounding branch identity: author-source localization or closed-model/fact binding.")
    candidates: list[CandidateIssue] = Field(default_factory=list, description="Candidate claims grounded by this branch; each candidate must carry reason and basis and must not emit W/D/L levels.")
    contract_dispositions: list[GroundingDisposition] = Field(default_factory=list, description="One reasoned disposition per supplied atomic contract; missing rows are normalized to explicit unresolved receipts without semantic guessing.")
    reason: str = Field(min_length=1, description="LLM explanation of how this branch selected or rejected candidate claims.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied branch-specific facts and contract IDs used.")


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
        "nl_contract_extraction",
        "source_grounding",
        "model_grounding",
        "exact_binding",
        "predicate_compilation",
        "backend_execution",
        "d_adjudication",
        "w_publication",
    ] = Field(description="Frozen stage boundary represented by this receipt.")
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


def _safe_previous(previous: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep only the method's own prior candidate surface for iterative rounds."""

    rows: list[dict[str, Any]] = []
    for item in previous[-8:]:
        rows.append(
            {
                key: item[key]
                for key in (
                    "issue_id",
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
                    "candidate_reason",
                    "candidate_basis",
                )
                if key in item
            }
        )
    return rows


def _compact_contract_plan(contracts: NLContractResponse) -> dict[str, Any]:
    """Project contract semantics once without repeating upstream rationale.

    Complete contract and hint rationale remains in the contract stage output.
    Grounding needs the typed key, source anchor, scope, and binding values; it
    can refer to the hash when auditing the exact upstream response.
    """

    full_payload = contracts.model_dump(mode="json")
    return {
        "projection_version": "contract-grounding-projection.v1",
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
        "basis": "contract-grounding-projection.v1 and full contract response hash",
    }


def _context_text(pair: PairInput, *, stage: Literal["nl_contract_extraction", "source_grounding", "model_grounding", "d_adjudication"]) -> str:
    """Serialize the stage-scoped closure while retaining the complete manifest."""

    if pair.context_manifest is None or pair.exact_source_inventory is None:
        raise ValueError("formal method prompt requires a complete context manifest and source inventory")
    return json.dumps(
        prompt_context_payload(pair, stage=stage),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
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
- Route deterministic facts by property: LEAF_WITHOUT_OUTGOING/deadlock-frontier facts may yield one V4(initial_scope) candidate with exact leaf refs as supporting binding; failed finite reachability yields G1; a refuted initial-entry fact yields an exact S2 initial-edge claim. Do not turn a leaf/deadlock fact into S1 or an arbitrary present S2 edge.
- Missing containment, region/consumer scope, initial-owner existence, or variable-delta semantics may remain a precise predicate=null W1 candidate. Preserve the exact owner/event/state refs and state the unsupported boundary; do not silently drop or rename it.
- A predicate that is registered but source-gated as candidate or W1-only is still a valid precise candidate. The downstream deterministic state machine decides W1/W2; the grounding branch must not drop it merely because it cannot reach W2.
- For a missing fact, bind the expected exact model/source element and the observed absence or counterexample. For a present fact, preserve it as a non-violation observation unless the supplied dossier identifies a distinct violated obligation."""


CONTRACT_SYSTEM_PROMPT = f"""You are the NL contract extraction stage of the paper1 evidence_discovery method. {COMMON_RULES} Extract atomic source obligations before inspecting model satisfaction. For every contract, fill the typed semantic key `(locus_kind, locus_names, property, expected_direction, violation_direction, evidence_types)` and typed binding hints. Split independently violable containment, initialization, transition endpoint, trigger, guard, effect, action, reachability, progress, event-consumer, region, variable-delta, and excess-behavior clauses instead of bundling them. Preserve qualifiers, ordering, initialization/operation/termination scope, and ambiguity. The violation direction says what later grounding must test; it does not claim that the defect exists.

Atomic contract shape:
- One contract represents one property at one independently violable locus. A transition-property row has at most one source, one target, and one transition hint.
- Alternative destinations are separate endpoint contracts. A guard conjunction for one exact transition remains one normalized guard hint; guards attached to different transitions are separate contracts.
- Initialization, containment, endpoint, trigger, guard, effect, action, reachability/progress, event-consumer coverage, region structure, and variable delta never share one contract merely because the NL states them in one sentence.
- `wrong_target` belongs to `transition_endpoints`, `wrong_guard` to `guard`, `wrong_effect` to `effect` or `variable_delta`, `unreachable` to `reachability`, `dead_end` to `deadlock_freedom`, and `unconsumed` to `event_consumer_coverage`. Do not encode one property with another property's direction.
- When an event is semantically required to be accepted within a scope, emit a separate `event_consumer_coverage` contract in addition to any local endpoint/trigger contract. This is a semantic LLM judgment from the supplied NL, never a spelling or keyword rule.

Generic worked example: "Within Controller, start in Idle; on Begin transition from Idle to Running when enabled and set mode=active" yields separate contracts for Controller containment of Idle, Controller initial entry to Idle, the Idle-to-Running endpoint, its Begin trigger set, its enabled guard, and its mode=active effect. If the clause also requires Begin to be accepted throughout Controller, that coverage requirement is a separate event-consumer contract. Do not copy the whole sentence into one multi-property contract.

Return only the requested Pydantic structure."""


SOURCE_GROUNDING_SYSTEM_PROMPT = f"""You are the author-source grounding branch of the paper1 evidence_discovery method. {COMMON_RULES} Use NL contracts, PlantUML, canonical source IR, exact source inventory, working contract, and source trace to locate source-scoped obligations and exact source identities. FCSTM facts may be compared only as a separate closed-model role. Do not claim that source presence proves execution or a violation. Return only the requested Pydantic structure."""


MODEL_GROUNDING_SYSTEM_PROMPT = f"""You are the closed-model grounding branch of the paper1 evidence_discovery method. {COMMON_RULES} Use FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries to bind exact model elements and propose predicate candidates. Do not rewrite an NL contract to match the model and do not treat unknown/not-run facts as violations.

Every candidate must copy one exact `contract_id` and preserve that contract's
`locus_kind`, `locus_names`, `property`, and `violation_direction`. Evaluate the
contract property first, then select the minimal frozen predicate that decides
that same property. Do not substitute a nearby endpoint, declaration, or local
path property merely because it is executable. Record the evidence families
actually used in `evidence_types`.

{PREDICATE_ROUTING_GUIDANCE}

Inspection-equivalent routing: a deterministic `LEAF_WITHOUT_OUTGOING` or finite
deadlock-frontier fact is a reason to consider one V4(initial_scope) candidate,
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

When one NL sentence contains multiple obligations, split them before rejecting
the contract. A satisfied endpoint or declaration does not discharge an attached
ordering, guard, effect, action, containment, region, consumer, or progress clause.
For every such unsatisfied or unsupported conjunct, preserve the exact model
locus and emit one atomic candidate; do not mark it satisfied or not_applicable
merely because a different conjunct is satisfied. A missing registered predicate
is a precise W1 candidate when the model locus is exact.

Return only the requested Pydantic structure."""


D_SYSTEM_PROMPT = f"""You are the method's semantic D adjudication stage. Use only the supplied NL contracts, author-source facts, exact bindings, predicate plan, and backend receipt. Never read or infer frozen ledger answers, baseline hit/FP results, independent judge examples, other pair payloads, or historical release outputs. Do not output D0/D1/D2, W0/W1/W2, L, a hit, or a release decision. Instead return one SemanticAdjudication per supplied obligation using only the closed grounding and defeater enums. `reason` must explain the supplied NL clause, exact source/model facts, and strongest alternative reading; `basis` must identify the supplied artifacts. Free-text wording is for audit only: do not decide from keyword, substring, regex, spelling, identifier shape, or text similarity.

D boundary: an unsupported or W1-only predicate does not erase a precise issue. When exact supplied source/model facts establish the candidate's semantic obligation, use grounding=established and describe the surviving ambiguity as a typed defeater when appropriate; deterministic code will keep it at W1. Use grounding=unresolved only when the supplied dossier genuinely cannot decide. A completed predicate result that is true for the requirement is not a violation merely because the candidate text sounds concerning.

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


def build_contract_prompt(pair: PairInput, round_index: int, previous: list[dict[str, Any]]) -> str:
    """Build the contract prompt with the complete context manifest."""

    return f"""{COMMON_RULES}

Stage: nl_contract_extraction
Round: {round_index}
Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="nl_contract_extraction")}

Prior method candidates from this pair's earlier round only:
{json.dumps(_safe_previous(previous), ensure_ascii=False, sort_keys=True, indent=2)}

Extract one NLContract per independently violable normative obligation. The typed semantic key and binding hints are the contract plan consumed by both grounding branches. Mark each supplied segment as covered, context, or ambiguous. Do not include ledger IDs, baseline labels, judge examples, W/D/L values, or hidden expected answers.
"""


def build_grounding_prompt(
    pair: PairInput,
    *,
    branch: Literal["source", "model"],
    round_index: int,
    contracts: NLContractResponse,
    previous: list[dict[str, Any]],
) -> str:
    """Build one branch prompt while retaining the full shared input closure."""

    branch_rules = (
        "Source branch priority: source identity, author scope, exact source line and transition mapping. Keep execution conclusions for the model branch and deterministic backend."
        if branch == "source"
        else "Model branch priority: exact FCSTM binding, deterministic inventory/diagnostic facts, and registry-minimal predicate inputs. Keep author-source identity for the source branch."
    )
    routing_guidance = (
        "Source branch must stay within author-source localization; do not use FCSTM facts or backend outcomes to assert satisfaction or violation."
        if branch == "source"
        else PREDICATE_ROUTING_GUIDANCE
    )
    return f"""{COMMON_RULES}

Stage: {branch}_grounding
Round: {round_index}
Branch rule: {branch_rules}
{routing_guidance}
Frozen predicate input spellings: S1={{kind, element, scope}} S2={{source, target, scope}} S3={{transition, triggers}} S4={{state, phase, action}} S5={{transition, guard}} S6={{transition, effect}} G1={{source, target}} G2={{source, target}} G3={{source, target, forbidden}} G4={{roots, marked}} R1={{scenario, event, step}} R2={{scenario, stimulus, state, window}} R3={{scenario, behavior, window}} R4={{scenario, state, interval}} V1={{source, trigger, domain}} V2={{source, trigger, domain}} V3={{p, q, bound, unit, scope}} V4={{initial_scope}} V5={{state, expected, initial_scope}}.
If a precise candidate cannot be expressed by the registry, set predicate_id to null. Do not silently drop it. Do not use W/D/L or L levels.
Copy `contract_id`, `locus_kind`, `locus_names`, `property`, and
`violation_direction` from the one atomic contract being evaluated. A candidate
may narrow source names to exact model identities through element_refs, but it
must not change the semantic key or reverse the defect direction. Put actual
evidence families used for the comparison in `evidence_types`.
Return exactly one `contract_dispositions` row for every supplied contract ID.
Use `candidate_emitted` when this response contains one or more candidates for
that ID; otherwise use `satisfied`, `unresolved`, or `not_applicable` with a
contract-specific reason and basis. Do not silently omit a contract.

NL contracts:
{json.dumps(_compact_contract_plan(contracts), ensure_ascii=False, sort_keys=True, indent=2)}

Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="source_grounding" if branch == "source" else "model_grounding")}

Prior method candidates from this pair's earlier round only:
{json.dumps(_safe_previous(previous), ensure_ascii=False, sort_keys=True, indent=2)}
    """


def build_d_adjudication_prompt(pair: PairInput, dossiers: list[dict[str, Any]]) -> str:
    """Build the whole-cell semantic D prompt without exposing evaluation answers."""

    compact_dossiers = [_compact_dossier(item) for item in dossiers]

    return f"""{D_SYSTEM_PROMPT}

Stage: d_adjudication
Pair identity: {pair.pair_id}
Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="d_adjudication")}

Obligation dossiers. These contain exact method outputs and backend facts, but no
W/D/L labels. Assess every obligation exactly once and preserve its obligation_id:
{json.dumps(compact_dossiers, ensure_ascii=False, sort_keys=True, indent=2)}

Required obligation IDs, exactly once each:
{json.dumps([item["obligation_id"] for item in compact_dossiers], ensure_ascii=False)}

Decision protocol:
- grounding=established only when the supplied NL/source/model dossier establishes a first violated-obligation reading;
- grounding=not_established when the supplied evidence does not establish that reading;
- grounding=unresolved when the dossier cannot decide;
- use defeater_kind=none and defeater_disposition=defeated only when no competent defeater applies;
- use undercutting or rebutting with survives/unresolved when a competent alternative remains;
- do not turn execution uncertainty or an absent predicate into a semantic violation;
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
) -> str:
    """Build a billed in-node correction prompt for a dynamic D coverage violation."""

    selected = [
        dossier
        for dossier in dossiers
        if dossier["obligation_id"] in set(missing_ids)
    ]
    return f"""{D_SYSTEM_PROMPT}

Stage: d_adjudication_correction
The previous structured response violated the exact obligation coverage contract.
This is an in-node contract correction, not a new method round. Return decisions
only for the missing IDs below, preserving their exact spelling:

missing_ids:
{json.dumps(missing_ids, ensure_ascii=False)}
duplicate_ids_to_ignore:
{json.dumps(duplicate_ids, ensure_ascii=False)}
extra_ids_to_ignore:
{json.dumps(extra_ids, ensure_ascii=False)}

Correction dossiers:
{json.dumps([_compact_dossier(item) for item in selected], ensure_ascii=False, sort_keys=True, indent=2)}

Return exactly one decision per missing ID. If the supplied dossier cannot decide,
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
    """Compatibility prompt exposing the source-grounding surface for tests/tools."""

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
        branch="source",
        round_index=round_index,
        contracts=empty_contracts,
        previous=previous,
    )


def fallback_contracts(pair: PairInput, reason: str) -> NLContractResponse:
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
            basis=f"{reason}; nl-segmentation.v1",
        )
        for segment in pair.nl_segments
    )
    return NLContractResponse(
        contracts=contracts,
        segment_disposition={segment.segment_id: "covered" for segment in pair.nl_segments},
        reason="Provider/schema failure was downgraded to a deterministic source-contract receipt.",
        basis="exact numbered NL artifact and no-silent-drop contract",
    )


def fallback_grounding(
    pair: PairInput,
    *,
    branch: Literal["source", "model"],
    contracts: NLContractResponse,
    reason: str,
) -> GroundingResponse:
    """Create conservative candidates from exact closed-model facts.

    This path is used only after the public structured runtime cannot return a
    grounding response. It does not decide whether a fact is a violation. It
    preserves an exact finite leaf-frontier observation for the D stage and one
    ordinary model fact for audit continuity, so a provider/schema failure does
    not erase the deterministic context or substitute an unrelated semantic
    claim. The independent D stage still decides whether either observation is
    an established issue.
    """

    transition = pair.model.transitions[0] if pair.model.transitions else None
    state = pair.model.states[0] if pair.model.states else None
    candidates: list[CandidateIssue] = []
    if branch == "model" and pair.inspection_facts is not None:
        leaf_refs = tuple(
            diagnostic.refs[0]
            for diagnostic in pair.inspection_facts.diagnostics
            if diagnostic.code == "LEAF_WITHOUT_OUTGOING" and diagnostic.refs
        )
        if leaf_refs:
            quote = (
                contracts.contracts[0].quote
                if contracts.contracts
                else "The supplied state-machine contract is retained for semantic review."
            )
            leaf_names = tuple(
                state_item.name
                for state_item in pair.inspection_facts.states
                if state_item.state_ref in set(leaf_refs)
            )
            candidates.append(
                CandidateIssue(
                    contract_id=(contracts.contracts[0].contract_id if contracts.contracts else "NL-CONTRACT-UNRESOLVED"),
                    locus_kind="state",
                    locus_names=leaf_names or leaf_refs,
                    property="deadlock_freedom",
                    violation_direction="dead_end",
                    evidence_types=("deadlock_frontier_fact", "verify_fact"),
                    title="Deterministic finite leaf frontier requires semantic review",
                    requirement_quote=quote,
                    predicate_id="V4",
                    predicate_inputs={"initial_scope": "closed_fcstm_initial_scope"},
                    element_refs=list(leaf_refs),
                    source_refs=[item.segment_id for item in contracts.contracts[:1]],
                    expected="The supplied finite model should not end an applicable operational scope at a non-final leaf without progress.",
                    observed=(
                        "Owned inspection-equivalent facts report LEAF_WITHOUT_OUTGOING for exact state refs "
                        + ", ".join(leaf_refs)
                        + (f" ({', '.join(leaf_names)})." if leaf_names else ".")
                    ),
                    strongest_rebuttal="The leaf may be an intentional terminal or synthetic lowering artifact; the D stage must assess that alternative from supplied facts.",
                    reason="The provider/schema response was unavailable, so the exact deterministic leaf-frontier fact was preserved as the registered V4 candidate surface.",
                    basis="inspection-equivalent.fcstm-graph.v2 LEAF_WITHOUT_OUTGOING diagnostics; no semantic violation was decided by fallback code.",
                )
            )
    if transition is not None:
        candidates.append(CandidateIssue(
            contract_id=(contracts.contracts[0].contract_id if contracts.contracts else "NL-CONTRACT-UNRESOLVED"),
            locus_kind="transition",
            locus_names=(transition.source, transition.target),
            property="transition_endpoints",
            violation_direction="other",
            evidence_types=("closed_model_inventory", "transition_fact"),
            title="Deterministic fallback preserving an exact transition fact",
            requirement_quote=contracts.contracts[0].quote if contracts.contracts else "The supplied NL contract is retained for audit.",
            predicate_id="S2",
            predicate_inputs={"source": transition.source, "target": transition.target, "scope": "closed_fcstm"},
            element_refs=[transition.ref],
            source_refs=[contracts.contracts[0].segment_id if contracts.contracts else "nl:unknown"],
            expected="The source-grounded transition contract is checkable in the closed model.",
            observed=f"The owned FCSTM parser found {transition.ref}.",
            strongest_rebuttal="No violation claim is asserted; this is a fallback candidate.",
            reason="The provider/schema response was unavailable, so an exact transition fact was preserved for deterministic binding.",
            basis=f"{reason}; {pair.model.algorithm_version}",
        ))
    elif state is not None:
        candidates.append(CandidateIssue(
            contract_id=(contracts.contracts[0].contract_id if contracts.contracts else "NL-CONTRACT-UNRESOLVED"),
            locus_kind="state",
            locus_names=(state.name,),
            property="element_declaration",
            violation_direction="other",
            evidence_types=("closed_model_inventory",),
            title="Deterministic fallback preserving an exact state fact",
            requirement_quote=contracts.contracts[0].quote if contracts.contracts else "The supplied NL contract is retained for audit.",
            predicate_id="S1",
            predicate_inputs={"kind": "state", "element": state.name, "scope": "closed_fcstm"},
            element_refs=[state.ref],
            source_refs=[contracts.contracts[0].segment_id if contracts.contracts else "nl:unknown"],
            expected="The source-grounded state contract is checkable in the closed model.",
            observed=f"The owned FCSTM parser found {state.ref}.",
            strongest_rebuttal="No violation claim is asserted; this is a fallback candidate.",
            reason="The provider/schema response was unavailable, so an exact state fact was preserved for deterministic binding.",
            basis=f"{reason}; {pair.model.algorithm_version}",
        ))
    return GroundingResponse(
        branch=branch,
        candidates=candidates,
        contract_dispositions=[
            GroundingDisposition(
                contract_id=contract.contract_id,
                status=(
                    "candidate_emitted"
                    if any(item.contract_id == contract.contract_id for item in candidates)
                    else "unresolved"
                ),
                candidate_count=sum(
                    item.contract_id == contract.contract_id for item in candidates
                ),
                reason=(
                    "The deterministic fallback preserved exact facts for this contract after the branch provider/schema result was unavailable."
                    if any(item.contract_id == contract.contract_id for item in candidates)
                    else "The branch provider/schema result was unavailable and deterministic code did not infer a semantic disposition for this contract."
                ),
                basis=f"{reason}; exact contract ID accounting without free-text semantic inference",
            )
            for contract in contracts.contracts
        ],
        reason=f"{branch} grounding used a deterministic fallback after provider/schema failure.",
        basis=f"{reason}; exact closed-model input closure",
    )


def assemble_method_response(
    source: GroundingResponse,
    model: GroundingResponse,
    *,
    reason: str,
    basis: str,
) -> MethodResponse:
    """Join source attribution onto model candidates without widening execution.

    The source branch is a localization index, not a second closed-model
    candidate surface. A source row is joined only when it shares an exact
    supplied source reference with a model row; free-text similarity is never
    used for this join.
    """

    seen: set[str] = set()
    candidates: list[CandidateIssue] = []
    for candidate in model.candidates:
        source_refs = set(candidate.source_refs)
        matched_source_refs: set[str] = set()
        for source_candidate in source.candidates:
            shared_refs = source_refs.intersection(source_candidate.source_refs)
            if shared_refs:
                matched_source_refs.update(shared_refs)
        if matched_source_refs:
            candidate = candidate.model_copy(
                update={
                    "source_refs": list(dict.fromkeys([*candidate.source_refs, *sorted(matched_source_refs)])),
                    "basis": f"{candidate.basis}; source-localization refs joined by exact source IDs",
                }
            )
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
        reason=f"{reason} Source-only rows were retained in the stage receipt and excluded from backend execution.",
        basis=f"{basis}; model-grounding is the sole closed-model candidate surface",
    )


__all__ = [
    "CONTRACT_SYSTEM_PROMPT",
    "SOURCE_GROUNDING_SYSTEM_PROMPT",
    "MODEL_GROUNDING_SYSTEM_PROMPT",
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
