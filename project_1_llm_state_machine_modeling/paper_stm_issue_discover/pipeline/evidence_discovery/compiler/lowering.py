from __future__ import annotations

import hashlib
import json
from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from ..inputs.models import ModelIR
from ..registry.model import PredicateRegistry
from ..semantics.binding import BindingResult
from ..semantics.obligations import CandidateIssue
from .inputs import (
    PredicateInputs,
    UnsupportedPredicateInputs,
    project_predicate_input_values,
    validate_predicate_inputs,
)

SUPPORTED_PREDICATES = frozenset(
    {
        "S1", "S2", "S3", "S4", "S5", "S6",
        "G1", "G2", "G3", "G4",
        "R1", "R2", "R3", "R4",
        "V1", "V2", "V3", "V4", "V5",
    }
)

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
    """Deterministic compilation plan for one frozen-predicate candidate.

    The compiler produces this object for the backend and W state machine. It
    is authoritative for normalized inputs, formal program, and capability
    gates, but it does not decide candidate D or any Judge relation.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    plan_id: str = Field(min_length=1, description="Stable plan identifier tied to the pair, round, and candidate obligation.")
    predicate_id: str | None = Field(default=None, description="Frozen predicate identifier, or null when the precise candidate has no applicable frozen predicate route.")
    registry_version: str = Field(min_length=1, description="Registry version used to compile this plan.")
    inputs: PredicateInputs = Field(description="Typed canonical inputs discriminated by frozen predicate ID; the unsupported variant represents null or invalid inputs, forces downgrade, and cannot execute as W2.")
    soundness_fragment: str = Field(min_length=1, description="Registered soundness boundary for the planned check.")
    assumptions: tuple[str, ...] = Field(description="Closed-input and algorithm assumptions required by the plan.")
    formal_program: str | None = Field(default=None, description="Compiled assertion or formal-program source, present only for an executable supported plan.")
    formal_program_hash: str | None = Field(default=None, description="SHA-256 hash of formal_program, when compiled.")
    predicate_registered: bool = Field(default=False, description="Whether predicate_id resolves to one of the frozen 19 registry predicates; bibliography review status never changes this field.")
    binding_precise: bool = Field(default=False, description="Whether the candidate has an exact reliable semantic and element binding before execution.")
    input_shape_valid: bool = Field(default=False, description="Whether normalized typed inputs satisfy the predicate-specific Pydantic schema.")
    binding_complete: bool = Field(default=False, description="Whether every registry-minimal typed input is present after normalization.")
    backend_available: bool = Field(default=False, description="Whether the frozen predicate has a deterministic backend dispatch implementation.")
    soundness_fragment_satisfied: bool = Field(default=False, description="Whether the plan meets the predicate's local finite-model, scope, carrier, and input-fragment preconditions.")
    artifact_attribution_complete: bool = Field(default=False, description="Whether the compiled plan carries the closed executed-model identity and program hash required for later artifact attribution.")
    execution_state: str = Field(default="not_attempted", description="Compilation-time execution state. Runtime receipts independently record not_attempted, completed, or failed outcomes.")
    predicate_verdict: str | None = Field(default=None, description="Compilation-time predicate verdict, always null before a backend receipt is produced.")
    supported: bool = Field(default=False, description="Deprecated compatibility synonym for execution readiness. It is derived only from executable typed/backend conditions and never from bibliography provenance.")
    executable: bool = Field(default=False, description="Whether typed inputs and a deterministic backend are sufficient to run under the frozen predicate contract.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the plan support or downgrade decision.")
    basis: str = Field(min_length=1, description="Non-empty registry, source, binding, or capability basis for the plan decision.")
    predicate_name: str | None = Field(default=None, min_length=1, description="Registered predicate name, when predicate_id is present.")
    family: str | None = Field(default=None, min_length=1, description="Registered predicate family, when predicate_id is present.")
    semantics: str | None = Field(default=None, min_length=1, description="Registered predicate semantics, when predicate_id is present.")
    source_ids: tuple[str, ...] = Field(default=(), description="Registered source identifiers for this predicate.")
    missing_inputs: tuple[str, ...] = Field(default=(), description="Required registry inputs missing from the candidate binding.")

    @model_validator(mode="before")
    @classmethod
    def add_input_discriminator(cls, value: Any) -> Any:
        """Tag legacy direct-constructor input maps from the explicit plan predicate ID."""

        if not isinstance(value, Mapping):
            return value
        inputs = value.get("inputs")
        if not isinstance(inputs, Mapping) or "predicate_id" in inputs:
            return value
        tagged_inputs = dict(inputs)
        tagged_inputs["predicate_id"] = value.get("predicate_id") or "unsupported"
        updated = dict(value)
        updated["inputs"] = tagged_inputs
        return updated

    @model_validator(mode="after")
    def validate_input_support_consistency(self) -> PredicatePlan:
        """Prevent an invalid typed input object from entering a W2 backend."""

        if isinstance(self.inputs, UnsupportedPredicateInputs) and self.executable:
            raise ValueError(
                "PredicatePlan.inputs is unsupported/invalid but executable=true; "
                "typed input failures must deterministically downgrade to W1"
            )
        return self

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")


def assess_soundness_fragment(
    predicate_id: str,
    inputs: Mapping[str, Any],
    *,
    model_hash: str | None,
) -> tuple[bool, str]:
    """Check local executable-fragment preconditions without bibliography state.

    This function intentionally verifies only deterministic input shape and
    ownership facts. It does not infer a requirement, a verdict, or any
    academic eligibility from historical provenance metadata.
    """

    if not model_hash:
        return False, "the closed ModelIR hash is missing"
    if predicate_id == "S4" and inputs.get("phase") not in {"entry", "do", "exit"}:
        return False, "S4 phase must be one of entry, do, or exit"
    if predicate_id == "S2" and not isinstance(inputs.get("scope"), str):
        return False, "S2 requires one exact owner scope"
    if predicate_id in {"S3", "S5", "S6"} and not isinstance(inputs.get("transition"), str):
        return False, f"{predicate_id} requires one exact transition carrier"
    if predicate_id == "V1":
        domain = inputs.get("domain")
        guards = inputs.get("guards")
        if not isinstance(inputs.get("source"), str) or domain is None:
            return False, "V1 requires an exact choice source and a declared finite domain"
        if not isinstance(guards, (list, tuple)) or len(guards) < 2:
            return False, "V1 requires at least two exact guards from one choice group"
    return True, "typed inputs satisfy the local executable soundness fragment"


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
            if alias in normalized:
                normalized.setdefault(canonical, normalized[alias])
                normalized.pop(alias)
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
        typed_inputs = validate_predicate_inputs(
            None,
            normalize_inputs(dict(candidate.predicate_inputs)),
        )
        return PredicatePlan(
            plan_id=plan_id,
            predicate_id=None,
            registry_version=registry.version,
            inputs=typed_inputs,
            soundness_fragment="none",
            assumptions=(),
            formal_program=None,
            formal_program_hash=None,
            predicate_registered=False,
            binding_precise=binding.precise,
            input_shape_valid=False,
            binding_complete=False,
            backend_available=False,
            soundness_fragment_satisfied=False,
            artifact_attribution_complete=False,
            supported=False,
            executable=False,
            reason="The candidate has no usable frozen predicate ID; preserve a precise binding as W1.",
            basis="frozen registry lookup rejected missing or unknown predicate",
        )
    normalized_inputs = normalize_inputs(dict(candidate.predicate_inputs))
    inputs = project_predicate_input_values(predicate.id, normalized_inputs)
    typed_inputs = validate_predicate_inputs(predicate.id, inputs)
    missing_inputs = tuple(
        input_name
        for input_name in predicate.inputs
        if (
            input_name not in inputs
            or (
                inputs[input_name] in (None, "")
                and not (
                    predicate.id in {"V1", "V2"}
                    and input_name == "trigger"
                    and input_name in inputs
                )
            )
            or (
                inputs[input_name] == []
                and not (predicate.id == "S3" and input_name == "triggers")
            )
        )
    )
    binding_complete = not missing_inputs
    formal_program = (
        f"registry={registry.version}\n"
        f"ASSERT {predicate.id}:{predicate.name} family={predicate.family}\n"
        f"INPUTS {json.dumps(inputs, ensure_ascii=False, sort_keys=True)}\n"
        f"ASSUMPTION closed_fcstm=true algorithm={model.algorithm_version}"
    )
    backend_supported = predicate.id in SUPPORTED_PREDICATES
    input_shape_valid = not isinstance(typed_inputs, UnsupportedPredicateInputs)
    soundness_fragment_satisfied, fragment_reason = assess_soundness_fragment(
        predicate.id,
        inputs,
        model_hash=normalized_inputs.get("model_hash") if isinstance(normalized_inputs.get("model_hash"), str) else None,
    )
    artifact_attribution_complete = bool(
        normalized_inputs.get("model_hash") and formal_program
    )
    executable = (
        backend_supported
        and binding_complete
        and input_shape_valid
        and soundness_fragment_satisfied
    )
    # ``supported`` remains only as a backward-compatible serialization field.
    # It is exactly execution readiness and bibliography provenance cannot
    # modify it. W calculation reads the explicit readiness dimensions below.
    supported = executable
    if not input_shape_valid:
        reason = "The normalized predicate inputs violate the exact discriminated Pydantic variant; the candidate remains auditable W1 and is not executed."
        basis = f"typed predicate input validation errors={list(typed_inputs.validation_errors)}"
    elif not binding_complete:
        reason = f"The predicate execution binding lacks required inputs {list(missing_inputs)}; an exact semantic element binding remains W1, while an imprecise semantic binding remains W0."
        basis = "registry minimal-input completeness check; deterministic W state machine retains the independent semantic binding boundary"
    elif not backend_supported:
        reason = "The predicate is registered but its deterministic backend dispatch is unavailable; a precise candidate remains W1 with an execution audit."
        basis = "registry lookup plus explicit backend capability table"
    elif not soundness_fragment_satisfied:
        reason = "The predicate binding is typed but does not meet this frozen predicate's executable soundness fragment; retain the precise semantic candidate as W1."
        basis = f"local executable-fragment validation: {fragment_reason}"
    else:
        reason = "The frozen predicate, exact typed binding, executable fragment, and deterministic backend are ready for one real evaluation."
        basis = "frozen registry lookup, typed input validation, executable fragment, and deterministic backend capability table"
    return PredicatePlan(
        plan_id=plan_id,
        predicate_id=predicate.id,
        registry_version=registry.version,
        inputs=typed_inputs,
        soundness_fragment=predicate.soundness_fragment,
        assumptions=("closed_fcstm_input", model.algorithm_version),
        formal_program=formal_program if executable else None,
        formal_program_hash=_hash_text(formal_program) if executable else None,
        predicate_registered=True,
        binding_precise=binding.precise,
        input_shape_valid=input_shape_valid,
        binding_complete=binding_complete,
        backend_available=backend_supported,
        soundness_fragment_satisfied=soundness_fragment_satisfied,
        artifact_attribution_complete=artifact_attribution_complete and executable,
        supported=supported,
        executable=executable,
        reason=reason,
        basis=basis,
        predicate_name=predicate.name,
        family=predicate.family,
        semantics=predicate.semantics,
        source_ids=predicate.sources,
        missing_inputs=missing_inputs,
    )
