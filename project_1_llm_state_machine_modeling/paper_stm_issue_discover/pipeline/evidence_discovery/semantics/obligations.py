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

class CandidateIssue(BaseModel):
    """One LLM-generated candidate with explicit audit rationale.

    The model deliberately excludes W, D, and L. Evidence and disposition
    levels are computed by deterministic method code after this response is
    parsed. ``reason`` explains the model's judgment and ``basis`` names the
    supplied requirement/model facts used for it. The raw value is preserved so
    an auditor can review the model's own explanation without translation.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    title: str = Field(min_length=1, description="Short human-readable issue title; do not include a verdict level.")
    requirement_quote: str = Field(min_length=1, description="Exact or faithful quote of the supplied requirement supporting this candidate.")
    predicate_id: PredicateId | None = Field(default=None, description="One frozen predicate ID, or null when the precise claim is not expressible by the registry.")
    predicate_inputs: dict[str, Any] = Field(default_factory=dict, description="Only the frozen predicate's named inputs; do not invent semantic fields or answer data.")
    element_refs: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list, description="Stable FCSTM element references that bind the candidate to the supplied model.")
    source_refs: list[Annotated[str, Field(min_length=1)]] = Field(default_factory=list, description="Requirement or supplied-artifact source locations used for the candidate.")
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

def fallback_candidates(pair: PairInput, round_index: int) -> MethodResponse:
    first_state = pair.model.states[0] if pair.model.states else None
    first_transition = pair.model.transitions[0] if pair.model.transitions else None
    refs = [first_transition.ref] if first_transition else ([first_state.ref] if first_state else [])
    predicate_id = "S2" if first_transition else ("S1" if first_state else None)
    inputs: dict[str, Any] = {}
    if first_transition:
        inputs = {"source": first_transition.source, "target": first_transition.target, "scope": "closed_fcstm"}
    elif first_state:
        inputs = {"kind": "state", "element": first_state.name, "scope": "closed_fcstm"}
    candidate = CandidateIssue(
        title="Deterministic fallback candidate preserving a checkable model fact",
        requirement_quote="No structured model candidate was available; preserve the first checkable supplied fact.",
        predicate_id=predicate_id,
        predicate_inputs=inputs,
        element_refs=refs,
        source_refs=[f"fcstm:line:{first_transition.line if first_transition else first_state.line if first_state else 1}"],
        expected="The model fact is checkable in the closed FCSTM input.",
        observed="The model fact was parsed and preserved.",
        strongest_rebuttal="No violation claim is asserted; this is an audit fallback after provider or schema failure.",
        reason=f"Round {round_index} lacked a usable provider/schema response, so deterministic input facts were preserved.",
        basis="Closed input facts from fcstm-line-parser.v1 and the recorded failure receipt.",
    )
    return MethodResponse(
        issues=[candidate],
        reason="The structured model output was unavailable, so a deterministic fallback candidate was generated.",
        basis="provider/schema failure fallback; no ledger or judge data was read.",
    )
