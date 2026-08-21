"""v27-shaped method stages for contract extraction and complementary grounding."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.context import prompt_context_payload
from ..inputs.models import PairInput
from .adjudication import DAdjudicationResponse, SemanticAdjudication
from .obligations import CandidateIssue, MethodResponse, PredicateId


class NLContract(BaseModel):
    """One source-grounded normative contract extracted from a numbered NL segment."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(pattern=r"^NL-CONTRACT-[A-Za-z0-9_.-]+$", min_length=14, description="Stable contract identifier derived from the supplied segment identifier.")
    segment_id: str = Field(pattern=r"^NL[0-9]+(?:\.[0-9]+)?$", min_length=3, description="Exact numbered NL segment identifier carried from the input closure.")
    quote: str = Field(min_length=1, description="Exact or faithful quote of the supplied NL segment; do not invent an answer or expected defect.")
    normative_statement: str = Field(min_length=1, description="Atomic source obligation stated without judging whether the current model satisfies it.")
    scope: str = Field(min_length=1, description="Source-grounded scope of the obligation, such as a named state or initialization boundary.")
    source_refs: tuple[str, ...] = Field(default_factory=tuple, description="Source references from the supplied NL, PlantUML, or source trace; do not invent references.")
    reason: str = Field(min_length=1, description="LLM explanation of why this contract follows from the supplied NL segment.")
    basis: str = Field(min_length=1, description="LLM basis naming the supplied segment and source facts used for this contract.")


class NLContractResponse(BaseModel):
    """Structured LLM response for the v27-style NL contract extraction stage."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    contracts: list[NLContract] = Field(default_factory=list, description="Atomic contracts covering normative numbered NL segments; descriptive segments may be omitted with an explained top-level basis.")
    segment_disposition: dict[str, Literal["covered", "context", "ambiguous"]] = Field(default_factory=dict, description="Disposition for supplied NL segment IDs only; every key must be an input segment ID.")
    reason: str = Field(min_length=1, description="LLM explanation of the overall contract extraction decision.")
    basis: str = Field(min_length=1, description="LLM basis identifying the supplied NL segments and source context used.")


class GroundingResponse(BaseModel):
    """Structured LLM response for one complementary grounding branch."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    branch: Literal["source", "model"] = Field(description="Grounding branch identity: author-source localization or closed-model/fact binding.")
    candidates: list[CandidateIssue] = Field(default_factory=list, description="Candidate claims grounded by this branch; each candidate must carry reason and basis and must not emit W/D/L levels.")
    rejected_contract_ids: list[str] = Field(default_factory=list, description="Contract IDs this branch could not ground; preserve the reason in the top-level fields instead of silently dropping them.")
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


COMMON_RULES = """Use only the supplied input closure. Never read, infer, or reproduce frozen ledger answers, baseline hit/FP results, independent judge examples, other pair payloads, or historical release outputs. PlantUML and canonical source IR locate author intent; FCSTM is the closed model evaluated by the deterministic backend; inspection-equivalent and verify/SMT summaries are deterministic facts only. Do not treat one source role as another. Do not emit W0/W1/W2, D0/D1/D2, L, or a release decision. Predicate IDs are closed to the frozen 19 IDs. A precise claim that is not expressible by a frozen predicate must remain a candidate with predicate_id=null, not disappear. Every object and every top-level response must contain non-empty reason and basis. Explain the judgment in the requested content language; English-only output is not required."""


CONTRACT_SYSTEM_PROMPT = f"""You are the NL contract extraction stage of the paper1 evidence_discovery method. {COMMON_RULES} Extract atomic source obligations before inspecting model satisfaction. Preserve qualifiers, ordering, initialization/operation/termination scope, and ambiguity. Return only the requested Pydantic structure."""


SOURCE_GROUNDING_SYSTEM_PROMPT = f"""You are the author-source grounding branch of the paper1 evidence_discovery method. {COMMON_RULES} Use NL contracts, PlantUML, canonical source IR, exact source inventory, working contract, and source trace to locate source-scoped obligations and exact source identities. FCSTM facts may be compared only as a separate closed-model role. Do not claim that source presence proves execution or a violation. Return only the requested Pydantic structure."""


MODEL_GROUNDING_SYSTEM_PROMPT = f"""You are the closed-model grounding branch of the paper1 evidence_discovery method. {COMMON_RULES} Use FCSTM, owned ModelIR, reference inspection facts, owned inspection-equivalent facts, finite verify facts, and SMT formula summaries to bind exact model elements and propose predicate candidates. Do not rewrite an NL contract to match the model and do not treat unknown/not-run facts as violations. Return only the requested Pydantic structure."""


D_SYSTEM_PROMPT = """You are the method's semantic D adjudication stage. Use only the supplied NL contracts, author-source facts, exact bindings, predicate plan, and backend receipt. Never read or infer frozen ledger answers, baseline hit/FP results, independent judge examples, other pair payloads, or historical release outputs. Do not output D0/D1/D2, W0/W1/W2, L, a hit, or a release decision. Instead return one SemanticAdjudication per supplied obligation using only the closed grounding and defeater enums. `reason` must explain the supplied NL clause, exact source/model facts, and strongest alternative reading; `basis` must identify the supplied artifacts. Free-text wording is for audit only: do not decide from keyword, substring, regex, spelling, identifier shape, or text similarity."""


def build_contract_prompt(pair: PairInput, round_index: int, previous: list[dict[str, Any]]) -> str:
    """Build the contract prompt with the complete context manifest."""

    return f"""{COMMON_RULES}

Stage: nl_contract_extraction
Round: {round_index}
Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="nl_contract_extraction")}

Prior method candidates from this pair's earlier round only:
{json.dumps(_safe_previous(previous), ensure_ascii=False, sort_keys=True, indent=2)}

Extract one NLContract per independently violable normative obligation. Mark each supplied segment as covered, context, or ambiguous. Do not include ledger IDs, baseline labels, judge examples, W/D/L values, or hidden expected answers.
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
    return f"""{COMMON_RULES}

Stage: {branch}_grounding
Round: {round_index}
Branch rule: {branch_rules}
Frozen predicate input spellings: S1={{kind, element, scope}} S2={{source, target, scope}} S3={{transition, triggers}} S4={{state, phase, action}} S5={{transition, guard}} S6={{transition, effect}} G1={{source, target}} G2={{source, target}} G3={{source, target, forbidden}} G4={{roots, marked}} R1={{scenario, event, step}} R2={{scenario, stimulus, state, window}} R3={{scenario, behavior, window}} R4={{scenario, state, interval}} V1={{source, trigger, domain}} V2={{source, trigger, domain}} V3={{p, q, bound, unit, scope}} V4={{initial_scope}} V5={{state, expected, initial_scope}}.
If a precise candidate cannot be expressed by the registry, set predicate_id to null. Do not silently drop it. Do not use W/D/L or L levels.

NL contracts:
{json.dumps(contracts.model_dump(mode="json"), ensure_ascii=False, sort_keys=True, indent=2)}

Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="source_grounding" if branch == "source" else "model_grounding")}

Prior method candidates from this pair's earlier round only:
{json.dumps(_safe_previous(previous), ensure_ascii=False, sort_keys=True, indent=2)}
    """


def build_d_adjudication_prompt(pair: PairInput, dossiers: list[dict[str, Any]]) -> str:
    """Build the whole-cell semantic D prompt without exposing evaluation answers."""

    return f"""{D_SYSTEM_PROMPT}

Stage: d_adjudication
Pair identity: {pair.pair_id}
Stage-scoped context projection and complete artifact manifest:
{_context_text(pair, stage="d_adjudication")}

Obligation dossiers. These contain exact method outputs and backend facts, but no
W/D/L labels. Assess every obligation exactly once and preserve its obligation_id:
{json.dumps(dossiers, ensure_ascii=False, sort_keys=True, indent=2)}

Required obligation IDs, exactly once each:
{json.dumps([item["obligation_id"] for item in dossiers], ensure_ascii=False)}

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
{json.dumps(selected, ensure_ascii=False, sort_keys=True, indent=2)}

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


def build_method_prompt(pair: PairInput, round_index: int, previous: list[dict[str, Any]]) -> str:
    """Compatibility prompt exposing the source-grounding surface for tests/tools."""

    empty_contracts = NLContractResponse(
        contracts=tuple(
            NLContract(
                contract_id=f"NL-CONTRACT-{segment.segment_id}",
                segment_id=segment.segment_id,
                quote=segment.text,
                normative_statement=segment.text,
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
    """Create one conservative candidate from exact closed-model facts."""

    transition = pair.model.transitions[0] if pair.model.transitions else None
    state = pair.model.states[0] if pair.model.states else None
    candidate: CandidateIssue | None = None
    if transition is not None:
        candidate = CandidateIssue(
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
        )
    elif state is not None:
        candidate = CandidateIssue(
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
        )
    return GroundingResponse(
        branch=branch,
        candidates=[candidate] if candidate is not None else [],
        rejected_contract_ids=[],
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
    """Merge complementary branch candidates without semantic adjudication."""

    seen: set[str] = set()
    candidates: list[CandidateIssue] = []
    for candidate in (*source.candidates, *model.candidates):
        key = _hash(
            {
                "predicate_id": candidate.predicate_id,
                "predicate_inputs": candidate.predicate_inputs,
                "element_refs": candidate.element_refs,
                "requirement_quote": candidate.requirement_quote,
            }
        )
        if key in seen:
            continue
        seen.add(key)
        candidates.append(candidate)
    return MethodResponse(issues=candidates, reason=reason, basis=basis)


__all__ = [
    "CONTRACT_SYSTEM_PROMPT",
    "SOURCE_GROUNDING_SYSTEM_PROMPT",
    "MODEL_GROUNDING_SYSTEM_PROMPT",
    "D_SYSTEM_PROMPT",
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
]
