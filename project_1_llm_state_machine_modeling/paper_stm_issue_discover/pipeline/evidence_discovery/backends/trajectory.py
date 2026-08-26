"""Trajectory predicates executed by native FCSTM runtime and ``.fbmcq``."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from .fcstm_native import (
    NativeFCSTM,
    all_states,
    execute_fbmcq,
    load_native_fcstm,
    native_load_failure,
    native_receipt,
    resolve_state,
    state_path,
    transition_by_ref,
)


class RuntimeMacrostep(BaseModel):
    """One fully specified native FCSTM runtime cycle in a closed scenario."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    step: int = Field(ge=0, description="Zero-based contiguous macrostep index supplied to the native FCSTM runtime.")
    event_paths: tuple[str, ...] = Field(default_factory=tuple, description="Complete exact FCSTM event paths dispatched during this macrostep; omitted events are not silently inferred.")


class FCSTMRuntimeScenario(BaseModel):
    """Method-owned, fully instantiated scenario for native FCSTM execution.

    The scenario is an input, never a copied source trace.  The backend loads
    the closed FCSTM model and obtains all active states and consumption facts
    afresh through ``SimulationRuntime``.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema: Literal[
        "evidence-discovery.fcstm-runtime-scenario.v1",
        "evidence-discovery.fcstm-runtime-scenario.v2",
    ] = Field(description="Versioned closed FCSTM runtime scenario schema.")
    initialization: Literal["cold"] = Field(description="The runtime always begins from the closed model's cold initial configuration.")
    root_state: str = Field(min_length=1, description="Exact native FCSTM root state path expected by this scenario.")
    event_queue: tuple[str, ...] = Field(default_factory=tuple, description="Complete finite multiset of event paths authorized across the schedule.")
    schedule: tuple[RuntimeMacrostep, ...] = Field(min_length=1, description="Complete ordered macrostep schedule executed by the native runtime.")
    selected_step: int | None = Field(default=None, ge=0, description="Optional exact macrostep used by R1 event-consumption attribution.")
    selected_event_path: str | None = Field(default=None, min_length=1, description="Optional exact queued event observed by R1.")
    selected_transition_ref: str | None = Field(default=None, min_length=1, description="Optional exact transition:line:<n> carrier for R1 local attribution.")
    expected_active_before: str | None = Field(default=None, min_length=1, description="Optional exact active state before the selected R1 macrostep.")
    expected_active_after: str | None = Field(default=None, min_length=1, description="Optional exact active state after the selected R1 macrostep.")
    reason: str = Field(min_length=1, description="Non-empty explanation of how the current pair's requirement and closed model determine this scenario.")
    basis: str = Field(min_length=1, description="Non-empty FCSTM/native-runtime basis for the scenario closure.")

    @model_validator(mode="after")
    def validate_closed_schedule(self) -> "FCSTMRuntimeScenario":
        """Reject non-contiguous schedules and unauthorised event injections."""

        steps = tuple(row.step for row in self.schedule)
        if steps != tuple(range(len(steps))):
            raise ValueError("runtime schedule steps must be contiguous from zero")
        scheduled_events = tuple(event for row in self.schedule for event in row.event_paths)
        if any(event not in self.event_queue for event in scheduled_events):
            raise ValueError("every scheduled event must occur in the closed event_queue")
        selected_values = (
            self.selected_step,
            self.selected_event_path,
            self.selected_transition_ref,
            self.expected_active_before,
            self.expected_active_after,
        )
        if any(value is not None for value in selected_values) and any(value is None for value in selected_values):
            raise ValueError("R1 scenario attribution requires selected step/event/carrier and before/after states together")
        if self.selected_step is not None:
            if self.selected_step >= len(self.schedule):
                raise ValueError("selected_step is outside the closed schedule")
            row = self.schedule[self.selected_step]
            if self.selected_event_path not in row.event_paths or self.selected_event_path not in self.event_queue:
                raise ValueError("selected R1 event must be queued and dispatched in selected_step")
        return self


def _scenario(value: object) -> FCSTMRuntimeScenario | None:
    """Validate a scenario input without treating a saved trace as runtime data."""

    if not isinstance(value, Mapping):
        return None
    try:
        return FCSTMRuntimeScenario.model_validate(value)
    except ValidationError:
        return None


def _active_paths(runtime: Any) -> list[str]:
    """Read the public native runtime active-state path after one macrostep."""

    if runtime.is_ended:
        return []
    path = tuple(str(item) for item in runtime.current_state.path)
    return [".".join(path[:index]) for index in range(1, len(path) + 1)]


def _run_scenario(native: NativeFCSTM, scenario: FCSTMRuntimeScenario) -> tuple[list[dict[str, Any]], str | None]:
    """Execute the complete typed schedule through native ``SimulationRuntime``."""

    from pyfcstm.simulate import SimulationRuntime

    if scenario.root_state != state_path(native.machine.root_state):
        return [], "scenario root_state does not equal the native FCSTM root path"
    runtime = SimulationRuntime(native.machine, abstract_error_mode="log")
    trace: list[dict[str, Any]] = []
    try:
        for macrostep in scenario.schedule:
            before = _active_paths(runtime)
            result = runtime.cycle(list(macrostep.event_paths))
            trace.append(
                {
                    "step": macrostep.step,
                    "input_events": list(result.input_events),
                    "consumed_events": list(result.consumed_events),
                    "unconsumed_events": list(result.unconsumed_events),
                    "active_states_before": before,
                    "active_states": _active_paths(runtime),
                    "is_ended": bool(runtime.is_ended),
                    "delta": bool(result.delta),
                }
            )
    except Exception as exc:  # noqa: BLE001 - a runtime failure becomes execution audit data.
        return trace, f"native SimulationRuntime error: {type(exc).__name__}: {exc}"
    return trace, None


def _window(value: object, length: int) -> tuple[int, int] | None:
    """Validate one closed inclusive macrostep interval against the schedule."""

    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or len(value) != 2:
        return None
    start, end = value
    if isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, int) or not isinstance(end, int):
        return None
    if start < 0 or end < start or end >= length:
        return None
    return start, end


def _event_assumptions(native: NativeFCSTM, scenario: FCSTMRuntimeScenario) -> str:
    """Freeze every native event input for the ``.fbmcq`` execution schedule."""

    all_events = tuple(event.path_name for state in all_states(native) for event in state.events.values())
    lines: list[str] = []
    for row in scenario.schedule:
        selected = set(row.event_paths)
        for event_path in all_events:
            value = "true" if event_path in selected else "false"
            lines.append(f'assume event("{event_path}", {row.step}) == {value};')
    return "\n".join(lines)


def _behavior_path(native: NativeFCSTM, behavior: object) -> str | None:
    """Resolve one named abstract native lifecycle action for R3.

    FBMCQ's public ``called()`` observation records named abstract lifecycle
    calls. Concrete operation blocks are real FCSTM behavior, but they are not
    a callable action record in that solver fragment and must be retained as an
    out-of-fragment W1 rather than sent to FBMCQ as a backend error.
    """

    def abstract_actions(actions: Sequence[Any]) -> list[Any]:
        return [action for action in actions if action.is_abstract and action.name]

    if isinstance(behavior, str):
        wanted = behavior
        candidates = [
            action.func_name
            for state in all_states(native)
            for actions in (state.on_enters, state.on_durings, state.on_exits)
            for action in abstract_actions(actions)
            if action.func_name == wanted
        ]
        return candidates[0] if len(candidates) == 1 else None
    if not isinstance(behavior, Mapping):
        return None
    owner = resolve_state(native, behavior.get("owner"))
    phase = behavior.get("phase")
    action_name = behavior.get("action")
    if owner is None or phase not in {"entry", "do", "exit"} or not isinstance(action_name, str):
        return None
    actions = {"entry": owner.on_enters, "do": owner.on_durings, "exit": owner.on_exits}[phase]
    matches = [
        action.func_name
        for action in abstract_actions(actions)
        if action.name == action_name or action.func_name == action_name
    ]
    return matches[0] if len(matches) == 1 else None


def run_trajectory(plan: PredicatePlan, model: ModelIR, receipt_id: str):
    """Evaluate R1--R4 through actual FCSTM execution, never supplied traces."""

    predicate = plan.predicate_id or "unknown"
    try:
        native = load_native_fcstm(model)
    except Exception as exc:  # noqa: BLE001 - preserve as an execution failure.
        return native_load_failure(receipt_id, predicate, model, exc)
    scenario = _scenario(plan.inputs.get("scenario"))
    if scenario is None:
        return native_receipt(receipt_id, predicate, native, "unknown", "The trajectory predicate requires a valid method-owned closed FCSTM runtime scenario; a source trace is not an executable scenario.", "FCSTMRuntimeScenario Pydantic validation", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1")
    if scenario.root_state != state_path(native.machine.root_state):
        return native_receipt(receipt_id, predicate, native, "unknown", "The trajectory scenario root does not match the loaded native FCSTM root, so the execution scope is not closed.", "FCSTMRuntimeScenario.root_state and pyfcstm StateMachine.root_state identity", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", failure_kind="invalid_input")

    if predicate == "R3":
        behavior_path = _behavior_path(native, plan.inputs.get("behavior"))
        window = _window(plan.inputs.get("window"), len(scenario.schedule))
        if behavior_path is None or window is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "R3 requires one exact named abstract native lifecycle action and a closed macrostep observation window; concrete operation blocks are outside FBMCQ called()'s action-record fragment.", "R3 typed named-abstract behavior/window contract", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1", failure_kind="invalid_input")
        start, end = window
        query = "\n".join(
            ["init cold;", _event_assumptions(native, scenario), f'check reach <= {len(scenario.schedule)}: called("{behavior_path}", step={start}..{end});']
        )
        return execute_fbmcq(receipt_id=receipt_id, predicate=predicate, native=native, query=query, reason="The native .fbmcq execution checked the exact lifecycle behavior over the fully instantiated FCSTM event schedule.", basis="R3 typed scenario/behavior/window plus pyfcstm .fbmcq called()", timeout_ms=5_000)

    trace, error = _run_scenario(native, scenario)
    if error is not None:
        return native_receipt(receipt_id, predicate, native, "unknown", "The native FCSTM runtime did not complete the closed scenario; no trajectory verdict is claimed.", error, backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", terminal_state="error", trace=trace, metadata={"runtime_scenario_schema": scenario.schema})

    if predicate == "R1":
        event = plan.inputs.get("event")
        if not isinstance(event, str) or scenario.selected_step is None or scenario.selected_event_path is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "R1 requires an exact event and complete selected-step native runtime attribution.", "R1 typed event/scenario contract", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", trace=trace)
        carrier = transition_by_ref(native, scenario.selected_transition_ref)
        selected = trace[scenario.selected_step]
        event_matches = scenario.selected_event_path.rsplit(".", 1)[-1] == event
        carrier_matches = carrier is not None and carrier.event is not None and carrier.event.path_name == scenario.selected_event_path
        before_matches = scenario.expected_active_before in selected["active_states_before"]
        after_matches = scenario.expected_active_after in selected["active_states"]
        consumed = scenario.selected_event_path in selected["consumed_events"]
        unconsumed = scenario.selected_event_path in selected["unconsumed_events"]
        verdict = "true" if event_matches and carrier_matches and before_matches and after_matches and consumed and not unconsumed else "false"
        return native_receipt(receipt_id, predicate, native, verdict, "The exact queued event was checked against native FCSTM runtime consumption, carrier identity, and before/after state observations.", "pyfcstm SimulationRuntime.cycle and native transition grammar-span carrier", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", counterexample=[] if verdict == "true" else [{"event_matches": event_matches, "carrier_matches": carrier_matches, "before_matches": before_matches, "after_matches": after_matches, "consumed": consumed, "unconsumed": unconsumed}], trace=trace, metadata={"runtime_scenario_schema": scenario.schema, "selected_transition_ref": scenario.selected_transition_ref})

    if predicate == "R2":
        stimulus = plan.inputs.get("stimulus")
        target = resolve_state(native, plan.inputs.get("state"))
        window = _window(plan.inputs.get("window"), len(trace))
        if not isinstance(stimulus, str) or target is None or window is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "R2 requires one exact stimulus, native target state, and closed observation window.", "R2 typed runtime contract", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", trace=trace)
        start, end = window
        rows = trace[start : end + 1]
        occurrences = [index for index, row in enumerate(rows) if stimulus in row["input_events"]]
        trailing = rows[occurrences[-1] + 1 :] if occurrences else []
        target_path = state_path(target)
        holds = bool(trailing) and all(target_path in row["active_states"] for row in trailing)
        verdict = "true" if occurrences and holds else "false"
        return native_receipt(receipt_id, predicate, native, verdict, "The actual native FCSTM runtime trace was checked for the exact stimulus followed by target-state activity in every trailing observation.", "pyfcstm SimulationRuntime.cycle trace", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", counterexample=[] if verdict == "true" else [{"stimulus_seen": bool(occurrences), "trailing_rows": len(trailing), "target_path": target_path, "holds": holds}], trace=trace)

    if predicate == "R4":
        target = resolve_state(native, plan.inputs.get("state"))
        interval = _window(plan.inputs.get("interval"), len(trace))
        if target is None or interval is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "R4 requires one exact native state and a closed inclusive runtime interval.", "R4 typed runtime contract", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", trace=trace)
        start, end = interval
        target_path = state_path(target)
        missing = [row for row in trace[start : end + 1] if target_path not in row["active_states"]]
        verdict = "false" if missing else "true"
        return native_receipt(receipt_id, predicate, native, verdict, "Every point of the closed interval was obtained from and checked against the actual native FCSTM runtime trace.", "pyfcstm SimulationRuntime.cycle trace", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1", counterexample=missing, trace=trace)

    return native_receipt(receipt_id, predicate, native, "unknown", "The native trajectory backend has no branch for this predicate.", "explicit native trajectory dispatch boundary", backend_family="fcstm_runtime", algorithm_version="pyfcstm.runtime.v1")


__all__ = ["FCSTMRuntimeScenario", "RuntimeMacrostep", "run_trajectory"]
