"""Machine-checkable execution fragments for the frozen predicate registry.

The registry's scholarly qualification, a predicate's executable fragment, and
one backend truth value are deliberately separate.  This module checks only
the middle dimension using native pyfcstm identities; it never creates a
candidate or decides a backend verdict.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.fcstm_native_projection import (
    all_transition_carriers,
    load_native_document,
    resolve_event,
    resolve_state,
    state_path,
    transition_carrier_reference,
)
from ..inputs.models import ModelIR


class SoundnessAssessment(BaseModel):
    """One deterministic executable-fragment decision for a frozen predicate."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    predicate_id: str = Field(min_length=1, description="Frozen predicate whose executable fragment was assessed.")
    satisfied: bool = Field(description="Whether this exact typed plan lies within the predicate's executable fragment.")
    boundary_id: str = Field(min_length=1, description="Stable predicate-specific executable-boundary identifier.")
    model_boundary: str = Field(min_length=1, description="Closed native model and finite-algorithm boundary applied to this plan.")
    required_inputs: tuple[str, ...] = Field(description="Typed inputs that the boundary requires for this predicate.")
    reason: str = Field(min_length=1, description="Non-empty decision explanation.")
    basis: str = Field(min_length=1, description="Native identity, typed input, and backend-boundary basis.")


_REQUIRED: dict[str, tuple[str, ...]] = {
    "S1": ("kind", "element", "scope"), "S2": ("source", "target", "scope"),
    "S3": ("transition", "triggers"), "S4": ("state", "phase", "action"),
    "S5": ("transition", "guard"), "S6": ("transition", "effect"),
    "G1": ("source", "target"), "G2": ("source", "target"),
    "G3": ("source", "target", "forbidden"), "G4": ("roots", "marked"),
    "R1": ("scenario", "event", "step"), "R2": ("scenario", "stimulus", "state", "window"),
    "R3": ("scenario", "behavior", "window"), "R4": ("scenario", "state", "interval"),
    "V1": ("source", "trigger", "domain"), "V2": ("source", "trigger", "domain"),
    "V3": ("p", "q", "bound", "unit", "scope"), "V4": ("initial_scope",),
    "V5": ("state", "expected", "initial_scope"),
}


def _assessment(predicate_id: str, ok: bool, reason: str, basis: str) -> SoundnessAssessment:
    """Create a complete per-predicate assessment without a fallback default."""

    return SoundnessAssessment(
        predicate_id=predicate_id,
        satisfied=ok,
        boundary_id=f"frozen-{predicate_id.lower()}-native-fragment.v1",
        model_boundary="one pyfcstm-loaded closed FCSTM plus the registered finite native backend algorithm",
        required_inputs=_REQUIRED[predicate_id],
        reason=reason,
        basis=basis,
    )


def _nonempty(value: object) -> bool:
    return value is not None and value != "" and value != () and value != [] and value != {}


def _state_set(document: Any, value: object, *, allow_initial: bool = False) -> bool:
    values = value if isinstance(value, Sequence) and not isinstance(value, (str, bytes)) else (value,)
    return bool(values) and all(raw == "[*]" and allow_initial or resolve_state(document, raw) is not None for raw in values)


def _carrier(document: Any, value: object) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    return sum(transition_carrier_reference(row, index) == value for index, row in enumerate(all_transition_carriers(document), start=1)) == 1


def assess_soundness(
    predicate_id: str,
    inputs: Mapping[str, Any],
    *,
    model: ModelIR | None,
    model_hash: str | None,
) -> SoundnessAssessment:
    """Assess all 19 frozen predicate fragments through native model identities.

    Missing model identity, malformed typed values, ambiguous carriers, and
    unsupported finite domains are explicit fragment failures.  A missing
    *required model element* is intentionally not a failure for predicates
    whose native backend can soundly return ``false`` for absence.
    """

    if predicate_id not in _REQUIRED:
        return SoundnessAssessment(predicate_id=predicate_id or "unknown", satisfied=False, boundary_id="unregistered-fragment.v1", model_boundary="no frozen backend boundary", required_inputs=(), reason="No frozen predicate-specific soundness validator is registered.", basis="explicit 19-predicate registry closure")
    if not model_hash or model is None:
        return _assessment(predicate_id, False, "The closed native model identity is missing.", "model hash and ModelIR are required before native fragment assessment")
    missing = tuple(name for name in _REQUIRED[predicate_id] if name not in inputs or inputs[name] is None)
    # S3's deliberate empty trigger set and S5's deliberate empty guard are
    # legal typed values, while every other empty required collection is not.
    if missing:
        return _assessment(predicate_id, False, f"The typed plan lacks required inputs {list(missing)}.", "predicate-specific frozen input boundary")
    try:
        document = load_native_document(model.source_text)
    except Exception as exc:  # noqa: BLE001 - becomes an auditable fragment failure.
        return _assessment(predicate_id, False, "The closed FCSTM could not be loaded through pyfcstm.", f"native loader failure: {type(exc).__name__}: {exc}")
    if document.source_hash != model_hash:
        return _assessment(predicate_id, False, "The typed model hash does not attribute the loaded native FCSTM.", f"typed={model_hash}; native={document.source_hash}")

    scope = inputs.get("scope")
    closed_scope = scope == "closed_fcstm"
    if predicate_id == "S1":
        ok = isinstance(inputs["kind"], str) and isinstance(inputs["element"], str) and closed_scope
    elif predicate_id == "S2":
        ok = _state_set(document, inputs["source"], allow_initial=True) and _state_set(document, inputs["target"]) and (closed_scope or resolve_state(document, scope) is not None)
    elif predicate_id in {"S3", "S5", "S6"}:
        ok = _carrier(document, inputs["transition"])
        if predicate_id == "S3": ok = ok and isinstance(inputs["triggers"], Sequence) and not isinstance(inputs["triggers"], (str, bytes)) and all(isinstance(value, str) and value.strip() for value in inputs["triggers"])
        if predicate_id == "S5": ok = ok and isinstance(inputs["guard"], str)
        if predicate_id == "S6": ok = ok and isinstance(inputs["effect"], Sequence) and len(inputs["effect"]) == 1 and isinstance(inputs["effect"][0], str) and bool(inputs["effect"][0].strip())
    elif predicate_id == "S4":
        ok = resolve_state(document, inputs["state"]) is not None and inputs["phase"] in {"entry", "do", "exit"} and isinstance(inputs["action"], str) and bool(inputs["action"].strip())
    elif predicate_id in {"G1", "G2"}:
        ok = _state_set(document, inputs["source"], allow_initial=True) and _state_set(document, inputs["target"])
    elif predicate_id == "G3":
        ok = _state_set(document, inputs["source"]) and _state_set(document, inputs["target"]) and _state_set(document, inputs["forbidden"])
    elif predicate_id == "G4":
        ok = _state_set(document, inputs["roots"], allow_initial=True) and _state_set(document, inputs["marked"])
    elif predicate_id in {"R1", "R2", "R3", "R4"}:
        scenario = inputs["scenario"]
        ok = isinstance(scenario, Mapping) and _nonempty(scenario.get("schedule")) and scenario.get("initialization") == "cold" and scenario.get("root_state") == state_path(document.machine.root_state)
        if predicate_id == "R1": ok = ok and resolve_event(document, inputs["event"]) is not None
        if predicate_id in {"R2", "R4"}: ok = ok and resolve_state(document, inputs["state"]) is not None
    elif predicate_id in {"V1", "V2"}:
        trigger = inputs["trigger"]
        ok = resolve_state(document, inputs["source"]) is not None and (trigger is None or resolve_event(document, trigger) is not None) and isinstance(inputs["domain"], Mapping) and bool(inputs["domain"])
        if predicate_id == "V1": ok = ok and isinstance(inputs.get("guards"), Sequence) and len(inputs["guards"]) >= 2
    elif predicate_id == "V3":
        # The native V3 backend only compiles a discrete FBMCQ step bound.
        # Treating milliseconds as executable here would promote a plan that
        # the backend must return as unknown.
        ok = isinstance(inputs["bound"], int) and not isinstance(inputs["bound"], bool) and inputs["bound"] > 0 and inputs["unit"] == "steps" and (scope in {"closed_fcstm", "cold"} or resolve_state(document, scope) is not None)
    elif predicate_id == "V4":
        initial_scope = inputs["initial_scope"]
        ok = initial_scope in {"closed_fcstm", "cold"} or resolve_state(document, initial_scope) is not None
    else:  # V5
        initial_scope = inputs["initial_scope"]
        ok = resolve_state(document, inputs["state"]) is not None and isinstance(inputs["expected"], (bool, int)) and (initial_scope in {"closed_fcstm", "cold"} or resolve_state(document, initial_scope) is not None)
    reason = "The typed plan satisfies this predicate's native executable fragment." if ok else "The typed plan is outside this predicate's native executable fragment."
    return _assessment(predicate_id, ok, reason, f"predicate={predicate_id}; native_source_hash={document.source_hash}; pyfcstm identity and finite backend boundary")
