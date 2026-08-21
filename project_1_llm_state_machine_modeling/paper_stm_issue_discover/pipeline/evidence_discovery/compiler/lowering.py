from __future__ import annotations

import hashlib
import json
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.models import ModelIR
from ..registry.model import PredicateRegistry
from ..semantics.binding import BindingResult
from ..semantics.obligations import CandidateIssue


SUPPORTED_PREDICATES = frozenset(
    {"S1", "S2", "S3", "S4", "S5", "S6", "G1", "G2", "G3", "G4", "V1", "V4"}
)

# A source-catalog ``partial_pass`` is the current strict W2 entry state. All
# candidate or explicitly W1-only source states remain executable candidates,
# but cannot be represented as W2 until the catalog is independently updated.
W2_SOURCE_STATUSES = frozenset({"partial_pass"})

_INPUT_ALIASES: dict[str, str] = {
    "transition_ref": "transition",
    "transition_name": "transition",
    "expected_guard": "guard",
    "required_guard": "guard",
    "expected_triggers": "triggers",
    "required_triggers": "triggers",
    "trigger_set": "triggers",
    "expected_guards": "guards",
    "guard_set": "guards",
    "expected_effect": "effect",
    "expected_effects": "effect",
    "expected_element": "element",
    "expected_state": "state",
    "expected_action": "action",
    "expected_source": "source",
    "expected_target": "target",
    "required_source": "source",
    "required_target": "target",
}

_SEQUENCE_INPUTS = frozenset(
    {"triggers", "effect", "effects", "forbidden", "guards", "roots", "marked", "sources", "targets"}
)


def _hash_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


class PredicatePlan(BaseModel):
    """Compiled deterministic plan for one frozen predicate candidate."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    plan_id: str = Field(min_length=1, description="Stable plan identifier tied to the pair, round, and candidate obligation.")
    predicate_id: str | None = Field(default=None, description="Frozen predicate identifier, or null for a W1-only/unexpressed candidate.")
    registry_version: str = Field(min_length=1, description="Registry version used to compile this plan.")
    inputs: dict[str, Any] = Field(description="Canonical predicate inputs after alias normalization and binding enrichment.")
    soundness_fragment: str = Field(min_length=1, description="Registered soundness boundary for the planned check.")
    assumptions: tuple[str, ...] = Field(description="Closed-input and algorithm assumptions required by the plan.")
    formal_program: str | None = Field(default=None, description="Compiled assertion or formal-program source, present only for an executable supported plan.")
    formal_program_hash: str | None = Field(default=None, description="SHA-256 hash of formal_program, when compiled.")
    supported: bool = Field(description="Whether this plan passed deterministic backend, source, and input gates.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the plan support or downgrade decision.")
    basis: str = Field(min_length=1, description="Non-empty registry, source, binding, or capability basis for the plan decision.")
    predicate_name: str | None = Field(default=None, min_length=1, description="Registered predicate name, when predicate_id is present.")
    family: str | None = Field(default=None, min_length=1, description="Registered predicate family, when predicate_id is present.")
    semantics: str | None = Field(default=None, min_length=1, description="Registered predicate semantics, when predicate_id is present.")
    source_ids: tuple[str, ...] = Field(default=(), description="Registered source identifiers for this predicate.")
    source_audit_status: str | None = Field(default=None, min_length=1, description="Current source-catalog status used by the W2 admission gate.")
    source_gate_passed: bool = Field(default=False, description="Whether the source audit status passed the current W2 gate.")
    binding_complete: bool = Field(default=True, description="Whether all registry-minimal inputs are present after normalization.")
    missing_inputs: tuple[str, ...] = Field(default=(), description="Required registry inputs missing from the candidate binding.")

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def compile_plan(
    candidate: CandidateIssue,
    binding: BindingResult,
    registry: PredicateRegistry,
    *,
    obligation_id: str,
    round_index: int,
    model: ModelIR,
    model_hash: str | None = None,
) -> PredicatePlan:
    def normalize_inputs(values: dict[str, Any]) -> dict[str, Any]:
        normalized = dict(values)
        for alias, canonical in _INPUT_ALIASES.items():
            if canonical not in normalized and alias in normalized:
                normalized[canonical] = normalized.pop(alias)
        for key in _SEQUENCE_INPUTS:
            value = normalized.get(key)
            if isinstance(value, str):
                normalized[key] = [value]
        normalized.setdefault("element_refs", list(binding.element_refs))
        # The candidate is LLM output and cannot choose the provenance identity
        # of the closed model. Prefer the exact loader hash; the text hash is
        # retained only for direct unit callers without a file receipt.
        normalized["model_hash"] = model_hash or _hash_text(model.source_text)
        return normalized

    candidate_id = candidate.predicate_id
    predicate = registry.get(candidate_id)
    plan_id = f"{obligation_id}:r{round_index}:plan"
    if predicate is None:
        return PredicatePlan(
            plan_id=plan_id,
            predicate_id=None,
            registry_version=registry.version,
            inputs=normalize_inputs(dict(candidate.predicate_inputs)),
            soundness_fragment="none",
            assumptions=(),
            formal_program=None,
            formal_program_hash=None,
            supported=False,
            reason="The candidate has no usable frozen predicate ID; preserve a precise binding as W1.",
            basis="frozen registry lookup rejected missing or unknown predicate",
        )
    inputs = normalize_inputs(dict(candidate.predicate_inputs))
    source_audit = (registry.source_audit or {}).get(predicate.id, {})
    source_status = source_audit.get("status") if isinstance(source_audit, dict) else None
    source_status = str(source_status) if source_status is not None else None
    source_gate_passed = source_status in W2_SOURCE_STATUSES
    missing_inputs = tuple(
        input_name
        for input_name in predicate.inputs
        if input_name not in inputs or inputs[input_name] in (None, "", [])
    )
    binding_complete = not missing_inputs
    formal_program = (
        f"registry={registry.version}\n"
        f"ASSERT {predicate.id}:{predicate.name} family={predicate.family}\n"
        f"INPUTS {json.dumps(inputs, ensure_ascii=False, sort_keys=True)}\n"
        f"ASSUMPTION closed_fcstm=true algorithm={model.algorithm_version}"
    )
    backend_supported = predicate.id in SUPPORTED_PREDICATES
    supported = backend_supported and source_gate_passed and binding_complete
    if not binding_complete:
        reason = f"The predicate binding lacks required inputs {list(missing_inputs)}; this candidate is W0 coverage gap."
        basis = "registry minimal-input completeness check"
    elif not backend_supported:
        reason = "The predicate is registered but has no sound backend in the current runtime; a precise candidate is W1."
        basis = "registry lookup plus explicit backend capability table"
    elif not source_gate_passed:
        reason = "The backend exists, but the predicate source gate has not passed; a precise candidate remains W1."
        basis = f"predicate_audit status={source_status!r}; W2 requires one of {sorted(W2_SOURCE_STATUSES)}"
    else:
        reason = "The predicate passes the frozen registry, source gate, and deterministic backend capability checks."
        basis = f"registry lookup, source gate status={source_status!r}, and backend capability table"
    return PredicatePlan(
        plan_id=plan_id,
        predicate_id=predicate.id,
        registry_version=registry.version,
        inputs=inputs,
        soundness_fragment=predicate.soundness_fragment,
        assumptions=("closed_fcstm_input", model.algorithm_version),
        formal_program=formal_program if supported else None,
        formal_program_hash=_hash_text(formal_program) if supported else None,
        supported=supported,
        reason=reason,
        basis=basis,
        predicate_name=predicate.name,
        family=predicate.family,
        semantics=predicate.semantics,
        source_ids=predicate.sources,
        source_audit_status=source_status,
        source_gate_passed=source_gate_passed,
        binding_complete=binding_complete,
        missing_inputs=missing_inputs,
    )
