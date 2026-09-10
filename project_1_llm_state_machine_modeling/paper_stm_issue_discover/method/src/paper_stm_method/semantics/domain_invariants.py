"""Frozen domain-invariant contracts projected from native FCSTM facts.

These contracts are separate from NL contracts.  They encode stable UML/state-machine
language rules whose normative authority is frozen before a method run, while native
FCSTM facts bind one exact carrier in the current artifact.
"""

from __future__ import annotations

import hashlib
import json
from typing import Literal, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..inputs import PairInput
from .author_source import AUTHOR_OWNED_SEGMENT_ROLES, build_author_index
from .obligations import CandidateIssue


class DomainInvariantContract(BaseModel):
    """One frozen language-rule obligation bound to an exact native FCSTM carrier.

    This model never substitutes for an NL requirement contract.  It records a
    language-level invariant, its fixed authority, the exact native transition
    carrier, and the one frozen predicate assertion that can evaluate it.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: Literal["evidence-discovery.domain-invariant-contract.v1"] = Field(
        default="evidence-discovery.domain-invariant-contract.v1",
        description="Persistence schema version for a frozen domain-invariant contract.",
    )
    contract_id: str = Field(
        pattern=r"^DOMAIN-INVARIANT-[A-Za-z0-9_.-]+$",
        description="Stable domain-contract identifier derived from invariant ID, exact carrier ref, and property.",
    )
    invariant_id: Literal["uml_initial_pseudostate_outgoing_unconditional"] = Field(
        description="Frozen UML/state-machine language invariant applied to this exact carrier.",
    )
    authority_ref: Literal["UML-2.5.1-14.5.6.7-Pseudostate-outgoing-from-initial"] = Field(
        description="Frozen normative authority for the invariant, retained independently of bibliography workflow status.",
    )
    locus_kind: Literal["transition"] = Field(
        default="transition",
        description="The invariant is evaluated on one authored native transition carrier.",
    )
    locus_names: tuple[str, str] = Field(
        description="Native-projection source and target display identities for audit presentation; transition_ref remains the executable identity.",
    )
    property: Literal["trigger_set", "guard"] = Field(
        description="Exact frozen predicate property enforced by this invariant.",
    )
    violation_direction: Literal["mismatched", "wrong_guard"] = Field(
        description="Typed direction of the observed initial-transition violation.",
    )
    predicate_id: Literal["S3", "S5"] = Field(
        description="Existing frozen predicate used for the invariant; this contract never introduces a predicate.",
    )
    transition_ref: str = Field(
        pattern=r"^transition:(?:line:[0-9]+|combo:[A-Za-z0-9_.-]+:line:[0-9]+)$",
        description="Exact pyfcstm-native-projection authored transition reference evaluated by the backend, including a provenance-grouped combo carrier when one source declaration expands to native implementation edges.",
    )
    owner_scope: str = Field(
        min_length=1,
        description="Native owner scope of the initial pseudostate transition, retained for attribution and review.",
    )
    target_ref: str | None = Field(
        default=None,
        description="Resolved exact target state ref when native projection supplies one; null is retained rather than guessed.",
    )
    expected_trigger_set: tuple[str, ...] | None = Field(
        default=None,
        description="Required trigger set. For S3 initial-transition invariants this is the deliberate empty tuple; null for S5.",
    )
    expected_guard: Literal[""] | None = Field(
        default=None,
        description="Required guard equality value. Empty string explicitly denotes the absence of a guard; null for S3.",
    )
    observed_triggers: tuple[str, ...] = Field(
        default_factory=tuple,
        description="Native trigger names observed on the exact carrier; retained for audit and never inferred from prose.",
    )
    observed_guard: str | None = Field(
        default=None,
        description="Native guard rendering observed on the exact carrier, or null when no guard is attached.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Frozen authority and native-projection provenance refs supporting the contract.",
    )
    reason: str = Field(
        min_length=1,
        description="Explains why the frozen invariant applies to this exact initial transition.",
    )
    basis: str = Field(
        min_length=1,
        description="Lists the native fact, exact carrier, and frozen authority used to close the invariant.",
    )

    @model_validator(mode="after")
    def validate_predicate_shape(self) -> "DomainInvariantContract":
        """Require one predicate/input shape for each invariant property."""

        if self.property == "trigger_set":
            if (
                self.predicate_id != "S3"
                or self.violation_direction != "mismatched"
                or self.expected_trigger_set != ()
                or not self.observed_triggers
                or self.expected_guard is not None
            ):
                raise ValueError("trigger-set invariant requires S3, empty required set, and observed native triggers")
        elif (
            self.predicate_id != "S5"
            or self.violation_direction != "wrong_guard"
            or self.expected_guard != ""
            or not self.observed_guard
            or self.expected_trigger_set is not None
        ):
            raise ValueError("guard invariant requires S5, explicit empty required guard, and an observed native guard")
        return self

    def candidate(self) -> CandidateIssue:
        """Project this exact frozen invariant into one executable candidate."""

        predicate_inputs: dict[str, object]
        observed: str
        if self.property == "trigger_set":
            predicate_inputs = {"transition": self.transition_ref, "triggers": []} if self.predicate_id else {}
            observed = (
                f"The exact initial transition {self.transition_ref} has native "
                f"triggers={list(self.observed_triggers)!r}."
            )
        else:
            predicate_inputs = {"transition": self.transition_ref, "guard": ""} if self.predicate_id else {}
            observed = (
                f"The exact initial transition {self.transition_ref} has native "
                f"guard={self.observed_guard!r}."
            )
        element_refs = [self.transition_ref]
        if self.target_ref:
            element_refs.append(self.target_ref)
        requirement = (
            f"Frozen UML initial-pseudostate invariant: transition {self.transition_ref} "
            "must have neither trigger nor guard."
        )
        return CandidateIssue(
            contract_id=self.contract_id,
            locus_kind=self.locus_kind,
            locus_names=self.locus_names,
            property=self.property,
            violation_direction=self.violation_direction,
            evidence_types=(
                "source_identity",
                "closed_model_inventory",
                "initial_entry_fact",
                "transition_fact",
                "trigger_fact" if self.property == "trigger_set" else "guard_fact",
            ),
            title=(
                f"Initial transition {self.transition_ref} has a trigger"
                if self.property == "trigger_set"
                else f"Initial transition {self.transition_ref} has a guard"
            ),
            requirement_quote=requirement,
            predicate_id=self.predicate_id,
            predicate_inputs=predicate_inputs,
            element_refs=element_refs,
            source_refs=list(self.source_refs),
            expected=requirement,
            observed=observed,
            strongest_rebuttal=(
                "Only the exact native initial transition carrier is evaluated; "
                "an ordinary transition elsewhere cannot satisfy this language invariant."
            ),
            reason=self.reason,
            basis=self.basis,
        )

    def candidate_mismatches(self, candidate: CandidateIssue) -> tuple[str, ...]:
        """Return semantic-key mismatches for deterministic candidate validation."""

        mismatches: list[str] = []
        if candidate.locus_kind != self.locus_kind:
            mismatches.append("locus_kind")
        if tuple(candidate.locus_names) != self.locus_names:
            mismatches.append("locus_names")
        if candidate.property != self.property:
            mismatches.append("property")
        if candidate.violation_direction != self.violation_direction:
            mismatches.append("violation_direction")
        if candidate.predicate_id != self.predicate_id:
            mismatches.append("predicate_id")
        if self.predicate_id is None:
            if self.transition_ref not in candidate.element_refs:
                mismatches.append("transition")
            if candidate.predicate_inputs:
                mismatches.append("predicate_inputs")
            return tuple(mismatches)
        if candidate.predicate_inputs.get("transition") != self.transition_ref:
            mismatches.append("transition")
        if self.property == "trigger_set":
            if tuple(candidate.predicate_inputs.get("triggers") or ()) != ():
                mismatches.append("triggers")
        elif candidate.predicate_inputs.get("guard") != "":
            mismatches.append("guard")
        return tuple(mismatches)


class SemanticDomainInvariantContract(DomainInvariantContract):
    """The same native language-rule facts without an execution assertion."""

    schema_version: Literal["evidence-discovery.semantic-domain-invariant-contract.v1"] = Field(
        default="evidence-discovery.semantic-domain-invariant-contract.v1",
        description="Persistence version for the semantic language invariant without an execution assertion.",
    )
    predicate_id: None = Field(default=None, description="Predicate mechanism disabled by A2.")

    @model_validator(mode="after")
    def validate_predicate_shape(self) -> "SemanticDomainInvariantContract":
        if self.property == "trigger_set":
            if (
                self.violation_direction != "mismatched"
                or self.expected_trigger_set != ()
                or not self.observed_triggers
                or self.expected_guard is not None
            ):
                raise ValueError("trigger-set invariant requires an empty required set and observed native triggers")
        elif (
            self.violation_direction != "wrong_guard"
            or self.expected_guard != ""
            or not self.observed_guard
            or self.expected_trigger_set is not None
        ):
            raise ValueError("guard invariant requires an empty required guard and an observed native guard")
        return self


def _contract_id(*, transition_ref: str, property_name: str) -> str:
    """Build a stable invariant ID without relying on source-text parsing."""

    payload = json.dumps(
        {
            "invariant": "uml_initial_pseudostate_outgoing_unconditional",
            "transition_ref": transition_ref,
            "property": property_name,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"DOMAIN-INVARIANT-UML-INITIAL-{property_name.upper()}-{digest}"


def materialize_domain_invariant_contracts(
    pair: PairInput,
    *,
    existing_candidates: Sequence[CandidateIssue] = (),
) -> tuple[tuple[DomainInvariantContract, ...], tuple[CandidateIssue, ...], tuple[dict[str, object], ...]]:
    """Project frozen initial-transition invariants from native inspection facts.

    The function consumes only pyfcstm-native projection facts from the current
    pair. It never reads requirements, ledger rows, Judge results, or another
    pair's artifact.
    """

    facts = pair.inspection_facts
    if facts is None:
        return (), (), ()
    author_index = build_author_index(pair)
    predicates_enabled = getattr(pair, "ablation_mode", "none") != "no-predicates"

    existing = {
        (
            candidate.predicate_id,
            candidate.property,
            candidate.predicate_inputs.get("transition"),
        )
        for candidate in existing_candidates
    }
    if not predicates_enabled:
        existing = {
            (None, candidate.property, ref)
            for candidate in existing_candidates
            for ref in candidate.element_refs
            if ref.startswith("transition:")
        }
    contracts: list[DomainInvariantContract] = []
    candidates: list[CandidateIssue] = []
    dispositions: list[dict[str, object]] = []
    authority_ref = "UML-2.5.1-14.5.6.7-Pseudostate-outgoing-from-initial"
    for fact in sorted(facts.transitions, key=lambda item: item.transition_ref):
        if fact.source != "[*]":
            continue
        # v61 carrier-attribution gate: the UML initial-pseudostate invariant is a
        # statement about the author's initial transition.  A lowering-synthesised
        # entry hop (cross-scope / composite-source target entry segment guarded by
        # the route token) is not an author transition, so the invariant does not
        # apply to it; see author_source.AUTHOR_OWNED_SEGMENT_ROLES.
        if author_index is not None and author_index.is_compiler_owned_carrier(
            pair.model.transition(fact.transition_ref)
        ):
            dispositions.append(
                {
                    "contract_id": None,
                    "status": "skipped_compiler_owned_carrier",
                    "transition_ref": fact.transition_ref,
                    "predicate_id": None,
                    "reason": "The initial carrier is a lowering-synthesised entry segment, not the author's initial transition; the UML initial-pseudostate invariant is not evaluated on compiler-owned hops.",
                    "basis": f"working-contract segment generated_role={author_index.segment_role_for_carrier(pair.model.transition(fact.transition_ref))!r}; author-owned roles={sorted(AUTHOR_OWNED_SEGMENT_ROLES)}",
                }
            )
            continue
        owner_scope = fact.scope or "closed_fcstm"
        common = {
            "invariant_id": "uml_initial_pseudostate_outgoing_unconditional",
            "authority_ref": authority_ref,
            "locus_names": (fact.source, fact.target),
            "transition_ref": fact.transition_ref,
            "owner_scope": owner_scope,
            "target_ref": fact.resolved_target_ref,
            "source_refs": (
                f"domain-invariant:{authority_ref}",
                f"native-projection:{fact.transition_ref}",
            ),
            "reason": "The frozen UML invariant applies because native FCSTM projection identifies this exact carrier as an outgoing initial-pseudostate transition.",
            "basis": (
                f"authority={authority_ref}; transition_ref={fact.transition_ref}; "
                f"owner_scope={owner_scope}; native_projection={facts.algorithm_version}"
            ),
        }
        definitions = []
        if fact.triggers:
            definitions.append(
                {
                    "contract_id": _contract_id(
                        transition_ref=fact.transition_ref, property_name="trigger"
                    ),
                    "property": "trigger_set",
                    "violation_direction": "mismatched",
                    "predicate_id": "S3" if predicates_enabled else None,
                    "expected_trigger_set": (),
                    "observed_triggers": tuple(fact.triggers),
                }
            )
        if fact.guard is not None and str(fact.guard).strip():
            definitions.append(
                {
                    "contract_id": _contract_id(
                        transition_ref=fact.transition_ref, property_name="guard"
                    ),
                    "property": "guard",
                    "violation_direction": "wrong_guard",
                    "predicate_id": "S5" if predicates_enabled else None,
                    "expected_guard": "",
                    "observed_guard": str(fact.guard),
                }
            )
        for definition in definitions:
            schema = DomainInvariantContract if predicates_enabled else SemanticDomainInvariantContract
            contract = schema.model_validate({**common, **definition})
            candidate = contract.candidate()
            key = (candidate.predicate_id, candidate.property, contract.transition_ref)
            if key in existing:
                dispositions.append(
                    {
                        "contract_id": contract.contract_id,
                        "status": "duplicate_exact_candidate",
                        "transition_ref": fact.transition_ref,
                        "predicate_id": contract.predicate_id,
                        "reason": "An existing candidate already binds the same predicate property and exact native transition carrier." if predicates_enabled else "An existing candidate already binds the same property and exact native transition carrier.",
                        "basis": "predicate ID, property, and exact transition-ref equality" if predicates_enabled else "property and exact transition-ref equality",
                    }
                )
                continue
            existing.add(key)
            contracts.append(contract)
            candidates.append(candidate)
            dispositions.append(
                {
                    "contract_id": contract.contract_id,
                    "status": "admitted",
                    "transition_ref": fact.transition_ref,
                    "predicate_id": contract.predicate_id,
                    "reason": candidate.reason,
                    "basis": candidate.basis,
                }
            )
    return tuple(contracts), tuple(candidates), tuple(dispositions)


__all__ = ["DomainInvariantContract", "materialize_domain_invariant_contracts"]
