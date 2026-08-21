from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from .binding import BindingResult
from .obligations import CandidateIssue


class SemanticAdjudication(BaseModel):
    """Typed semantic facts returned by the method's D adjudication call.

    This model intentionally has no ``d_level``, ``witness_level``, or ledger
    field. The LLM supplies an auditable semantic reading and defeater state;
    the method maps these closed enums to D after exact binding is checked.
    Free-text fields are retained for audit and are never compared by code.
    """

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, frozen=True)

    obligation_id: str = Field(
        min_length=1,
        description="Exact method obligation ID from the supplied dossier; do not invent or merge IDs.",
    )
    grounding: Literal["established", "not_established", "unresolved"] = Field(
        description=(
            "Whether the supplied NL/source/model dossier establishes a first violated-obligation reading. "
            "Use unresolved when the supplied facts cannot decide; do not infer it from words or identifiers."
        )
    )
    violated_obligation: str = Field(
        min_length=1,
        description="Concise semantic statement of the obligation under review, grounded only in supplied inputs.",
    )
    strongest_defeater: str | None = Field(
        default=None,
        description="Strongest supplied alternative reading or rebuttal; null only when none is applicable.",
    )
    defeater_kind: Literal["none", "undercutting", "rebutting"] = Field(
        description="Typed kind of the strongest defeater: none, undercutting the reading, or rebutting its conclusion."
    )
    defeater_disposition: Literal["defeated", "survives", "unresolved"] = Field(
        description="Whether the typed defeater is defeated by supplied facts, survives, or remains unresolved."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty LLM explanation citing the supplied NL clause, exact formal facts, and defeater reasoning.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty input basis for this semantic assessment; do not cite ledger, baseline, or judge data.",
    )


class DAdjudicationResponse(BaseModel):
    """Complete typed semantic assessment for all supplied method obligations."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    decisions: list[SemanticAdjudication] = Field(
        default_factory=list,
        description="Exactly one typed semantic assessment for each supplied obligation ID; do not omit unresolved units.",
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the whole-pair semantic adjudication outcome.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty basis naming the supplied dossier and source/model facts used by the call.",
    )


def adjudicate_disposition(
    candidate: CandidateIssue,
    binding: BindingResult,
    semantic: SemanticAdjudication | None = None,
    receipt: Any | None = None,
) -> dict[str, object]:
    """Map exact binding plus closed semantic enums to the method-owned D level.

    The method never compares ``expected``, ``observed`` or rebuttal prose. A
    missing or internally inconsistent semantic assessment remains unresolved;
    it cannot become a release issue merely because the text looks different.
    """

    semantic_payload = semantic.model_dump(mode="json") if semantic is not None else None
    if not binding.precise:
        return {
            "d_level": "D_UNRESOLVED",
            "reason": "The binding is insufficient for the method to state a reproducible violation.",
            "basis": binding.basis,
            "strongest_rebuttal": candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }
    if (
        receipt is not None
        and getattr(receipt, "terminal_state", None) == "completed"
        and getattr(receipt, "verdict", None) == "true"
    ):
        return {
            "d_level": "D0",
            "reason": "The deterministic predicate completed with a true result for the supplied obligation, so the candidate does not establish a violation.",
            "basis": "precise binding plus completed backend verdict=true; deterministic satisfaction overrides a conflicting semantic candidate reading",
            "strongest_rebuttal": getattr(receipt, "reason", None) or candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }
    if semantic is None:
        return {
            "d_level": "D_UNRESOLVED",
            "reason": "No typed semantic adjudication was available; free-text candidate fields cannot decide D.",
            "basis": "missing D semantic receipt; deterministic text comparison is forbidden",
            "strongest_rebuttal": candidate.strongest_rebuttal,
            "semantic_adjudication": None,
        }
    if semantic.grounding == "unresolved":
        return {
            "d_level": "D_UNRESOLVED",
            "reason": "The typed semantic adjudication could not establish a reproducible first reading.",
            "basis": "semantic grounding enum=unresolved",
            "strongest_rebuttal": semantic.strongest_defeater or candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }
    if semantic.grounding == "not_established":
        return {
            "d_level": "D0",
            "reason": "The typed semantic adjudication did not establish a violated obligation; retain the candidate for audit.",
            "basis": "semantic grounding enum=not_established",
            "strongest_rebuttal": semantic.strongest_defeater or candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }

    # A no-defeater assessment is only coherent when that defeater is marked
    # defeated. This is a closed enum consistency check, not a text heuristic.
    if semantic.defeater_kind == "none" and semantic.defeater_disposition != "defeated":
        return {
            "d_level": "D_UNRESOLVED",
            "reason": "The typed semantic assessment has an inconsistent no-defeater disposition.",
            "basis": "closed enum consistency rule: defeater_kind=none requires disposition=defeated",
            "strongest_rebuttal": semantic.strongest_defeater or candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }
    if semantic.defeater_disposition in {"survives", "unresolved"}:
        return {
            "d_level": "D1",
            "reason": "A grounded first reading remains compatible with a surviving or unresolved typed defeater.",
            "basis": "precise binding plus semantic grounding=established and defeater disposition in {survives, unresolved}",
            "strongest_rebuttal": semantic.strongest_defeater or candidate.strongest_rebuttal,
            "semantic_adjudication": semantic_payload,
        }
    return {
        "d_level": "D2",
        "reason": "A grounded violated obligation has no surviving competent typed defeater.",
        "basis": "precise binding plus semantic grounding=established and defeater disposition=defeated",
        "strongest_rebuttal": semantic.strongest_defeater or candidate.strongest_rebuttal,
        "semantic_adjudication": semantic_payload,
    }


__all__ = ["DAdjudicationResponse", "SemanticAdjudication", "adjudicate_disposition"]
