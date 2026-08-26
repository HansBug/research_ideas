from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.models import ModelIR


class RuntimeMacrostep(BaseModel):
    """One closed public-runtime cycle supplied to a trajectory predicate."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    step: int = Field(ge=0, description="Zero-based macrostep position in the closed runtime schedule.")
    event_paths: tuple[str, ...] = Field(description="Exact fully-qualified FCSTM event paths supplied to this macrostep.")


class FCSTMRuntimeScenario(BaseModel):
    """Restricted cold-start FCSTM execution contract for a real R1 receipt.

    The contract deliberately admits one sequential, unguarded macrostep only.
    It preserves the runtime input independently from the resulting trace, so a
    static source trace can never be presented as an execution receipt.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema: Literal["evidence-discovery.fcstm-runtime-scenario.v1"] = Field(
        description="Versioned schema identifier for the closed FCSTM runtime scenario."
    )
    initialization: Literal["cold"] = Field(description="The runtime starts only from the frozen model's cold initial configuration.")
    root_state: str = Field(min_length=1, description="Exact closed-FCSTM root state name used to qualify queued events.")
    expected_active_before: str = Field(min_length=1, description="Exact active state path required after initialization and before the selected macrostep.")
    expected_active_after: str = Field(min_length=1, description="Exact active state path required after the selected macrostep for carrier attribution.")
    event_queue: tuple[str, ...] = Field(min_length=1, description="Complete finite queue of fully-qualified event paths supplied by the scenario.")
    schedule: tuple[RuntimeMacrostep, ...] = Field(min_length=2, description="Complete ordered runtime schedule, including explicit initialization and selected macrosteps.")
    selected_step: int = Field(ge=0, description="Macrostep whose event-consumption result is the R1 observation window.")
    selected_event_path: str = Field(min_length=1, description="Exact queued event path expected to be consumed in selected_step.")
    selected_transition_ref: str = Field(min_length=1, description="Exact ModelIR transition carrier used only for local runtime attribution.")
    reason: str = Field(min_length=1, description="Non-empty explanation of why this closed runtime scenario is admissible.")
    basis: str = Field(min_length=1, description="Non-empty exact ModelIR and transition-group basis for this scenario.")

    @model_validator(mode="after")
    def validate_closed_schedule(self) -> "FCSTMRuntimeScenario":
        """Reject incomplete or ambiguous runtime schedule identities deterministically."""

        steps = tuple(item.step for item in self.schedule)
        if steps != tuple(sorted(steps)) or len(set(steps)) != len(steps):
            raise ValueError("runtime schedule steps must be strictly increasing")
        selected = [item for item in self.schedule if item.step == self.selected_step]
        if len(selected) != 1:
            raise ValueError("runtime scenario must contain exactly one selected_step row")
        if self.selected_event_path not in self.event_queue:
            raise ValueError("selected_event_path must be present in the closed event_queue")
        if self.selected_event_path not in selected[0].event_paths:
            raise ValueError("selected_event_path must be dispatched in selected_step")
        return self


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _rows(value: Any) -> list[Mapping[str, Any]]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        return []
    return [item for item in value if isinstance(item, Mapping)]


def _same_step(value: Any, expected: Any) -> bool:
    return value == expected or str(value) == str(expected)


def _receipt(
    receipt_id: str,
    predicate: str,
    model: ModelIR,
    verdict: str,
    reason: str,
    basis: str,
    *,
    counterexample: list[dict[str, Any]] | None = None,
    trace: list[dict[str, Any]] | None = None,
    metadata: dict[str, Any] | None = None,
) -> RawReceipt:
    run_metadata = {
        "algorithm_version": "trajectory-closed-window.v1",
        "model_hash": plan_model_hash(model),
        "closed_trace_contract": True,
    }
    if metadata:
        run_metadata.update(metadata)
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"trajectory:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        trace=trace or [],
        run_metadata=run_metadata,
    )


def plan_model_hash(model: ModelIR) -> str:
    """Return the same source-text identity used by the other deterministic backends."""

    import hashlib

    return "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest()


def _active_state_paths(runtime: Any) -> list[str]:
    """Return the public runtime's active leaf ancestry without reflection."""

    if bool(runtime.is_ended):
        return []
    path = tuple(str(item) for item in runtime.current_state.path)
    return [".".join(path[:index]) for index in range(1, len(path) + 1)]


def _run_fcstm_runtime_r1(
    plan: PredicatePlan,
    model: ModelIR,
    receipt_id: str,
    scenario: Mapping[str, Any],
) -> RawReceipt:
    """Execute one restricted R1 macrostep through public pyfcstm APIs.

    No inspection API or historical source trace is used here.  A failed parse,
    runtime rejection, or incomplete result is retained as an unsupported
    trajectory boundary rather than causing a method-cell failure.
    """

    predicate = plan.predicate_id or "unknown"
    try:
        spec = FCSTMRuntimeScenario.model_validate(scenario)
    except ValidationError as exc:
        return _receipt(
            receipt_id,
            predicate,
            model,
            "unknown",
            "The FCSTM runtime scenario does not satisfy the closed macrostep contract.",
            f"FCSTMRuntimeScenario validation errors={exc.error_count()}",
            metadata={"algorithm_version": "trajectory-fcstm-runtime.v1"},
        )
    if predicate != "R1":
        return _receipt(
            receipt_id,
            predicate,
            model,
            "unknown",
            "The FCSTM runtime scenario is currently defined only for R1 event-consumption execution.",
            "runtime scenario schema boundary",
            metadata={"algorithm_version": "trajectory-fcstm-runtime.v1"},
        )
    event = plan.inputs.get("event")
    if not isinstance(event, str) or not event:
        return _receipt(
            receipt_id,
            predicate,
            model,
            "unknown",
            "R1 requires one exact canonical event identity in addition to the runtime event path.",
            "R1 typed event input",
            metadata={"algorithm_version": "trajectory-fcstm-runtime.v1"},
        )
    if spec.selected_event_path.rsplit(".", 1)[-1] != event:
        return _receipt(
            receipt_id,
            predicate,
            model,
            "unknown",
            "The canonical R1 event does not match the selected fully-qualified runtime event path.",
            "exact event identity versus runtime path suffix",
            metadata={"algorithm_version": "trajectory-fcstm-runtime.v1"},
        )
    try:
        from pyfcstm.model import load_state_machine_from_text
        from pyfcstm.simulate import SimulationRuntime

        state_machine = load_state_machine_from_text(model.source_text)
        runtime = SimulationRuntime(state_machine, abstract_error_mode="log")
        trace: list[dict[str, Any]] = []
        for macrostep in spec.schedule:
            active_before = _active_state_paths(runtime)
            result = runtime.cycle(events=list(macrostep.event_paths))
            trace.append(
                {
                    "step": macrostep.step,
                    "input_events": list(result.input_events),
                    "consumed_events": list(result.consumed_events),
                    "unconsumed_events": list(result.unconsumed_events),
                    "active_states_before": active_before,
                    "active_states": _active_state_paths(runtime),
                    "is_ended": bool(runtime.is_ended),
                }
            )
    except Exception as exc:  # noqa: BLE001 - backend boundaries must preserve the cell.
        return _receipt(
            receipt_id,
            predicate,
            model,
            "unknown",
            "The public FCSTM runtime could not complete the closed R1 macrostep; no execution claim is made.",
            f"pyfcstm public simulation boundary; exception_type={type(exc).__name__}",
            metadata={"algorithm_version": "trajectory-fcstm-runtime.v1"},
        )
    selected = next(item for item in trace if item["step"] == spec.selected_step)
    queued = spec.selected_event_path in spec.event_queue
    consumed = spec.selected_event_path in selected["consumed_events"]
    unconsumed = spec.selected_event_path in selected["unconsumed_events"]
    actual_root = selected["active_states_before"][0] if selected["active_states_before"] else None
    root_matches = actual_root == spec.root_state
    source_matches = spec.expected_active_before in selected["active_states_before"]
    target_matches = spec.expected_active_after in selected["active_states"]
    verdict = "true" if queued and consumed and not unconsumed and root_matches and source_matches and target_matches else "false"
    return _receipt(
        receipt_id,
        predicate,
        model,
        verdict,
        "The frozen FCSTM was cold-started and the selected queued event was checked against actual public-runtime consumption and state observations.",
        "public pyfcstm load_state_machine_from_text and SimulationRuntime.cycle; no inspect API or static source trace",
        counterexample=[] if verdict == "true" else [{
            "queued": queued,
            "consumed": consumed,
            "unconsumed": unconsumed,
            "root_matches": root_matches,
            "source_matches": source_matches,
            "target_matches": target_matches,
        }],
        trace=trace,
        metadata={
            "algorithm_version": "trajectory-fcstm-runtime.v1",
            "runtime_engine": "pyfcstm.SimulationRuntime",
            "runtime_scenario_schema": spec.schema,
            "actual_root_state": actual_root,
            "selected_transition_ref": spec.selected_transition_ref,
        },
    )


def run_trajectory(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    predicate = plan.predicate_id or "unknown"
    scenario = _mapping(plan.inputs.get("scenario"))
    if scenario is None:
        return _receipt(receipt_id, predicate, model, "unknown", "The trajectory predicate lacks a structured scenario contract.", "scenario must be a closed JSON object")

    if predicate == "R1":
        if scenario.get("schema") == "evidence-discovery.fcstm-runtime-scenario.v1":
            return _run_fcstm_runtime_r1(plan, model, receipt_id, scenario)
        event = plan.inputs.get("event")
        step = plan.inputs.get("step")
        queue = scenario.get("event_queue")
        schedule = scenario.get("schedule")
        macrosteps = _rows(scenario.get("macrosteps"))
        if not isinstance(event, str) or not event or queue is None or schedule is None or not macrosteps:
            return _receipt(receipt_id, predicate, model, "unknown", "R1 requires event_queue, schedule, and a closed macrosteps list.", "event-consumption input contract")
        step_rows = [row for row in macrosteps if step is None or _same_step(row.get("step", row.get("id")), step)]
        if not step_rows:
            return _receipt(receipt_id, predicate, model, "unknown", "The requested R1 macrostep is not present in the closed trace window.", "exact macrostep identity")
        queued = any(
            item == event or (isinstance(item, Mapping) and item.get("event") == event)
            for item in queue if isinstance(queue, Sequence) and not isinstance(queue, (str, bytes))
        )
        consumed = any(
            event in set(row.get("consumed_events", ()))
            or any(item.get("event") == event for item in _rows(row.get("dispatch")))
            for row in step_rows
        )
        verdict = "true" if queued and consumed else "false"
        return _receipt(receipt_id, predicate, model, verdict, "The exact queued event was checked against the selected macrostep dispatch records.", "closed event queue, schedule, macrostep, and dispatch facts", counterexample=[] if verdict == "true" else [{"event": event, "queued": queued, "consumed": consumed}])

    trace = _rows(scenario.get("trace"))
    if not trace:
        return _receipt(receipt_id, predicate, model, "unknown", "The trajectory scenario has no closed trace window.", "trace window is required for R2/R4")

    if predicate == "R2":
        stimulus = plan.inputs.get("stimulus")
        state = plan.inputs.get("state")
        window = plan.inputs.get("window")
        if stimulus is None or not isinstance(state, str) or not isinstance(window, Sequence) or len(window) != 2:
            return _receipt(receipt_id, predicate, model, "unknown", "R2 requires stimulus, target state, and a two-ended trace window.", "state-after-stimulus input contract")
        start, end = window
        rows = [row for row in trace if start <= row.get("step", row.get("time", start)) <= end]
        stimulus_seen = any(row.get("stimulus") == stimulus or row.get("event") == stimulus for row in rows)
        state_seen = any(state in set(row.get("active_states", ())) or row.get("state") == state for row in rows)
        verdict = "true" if stimulus_seen and state_seen else "false"
        return _receipt(receipt_id, predicate, model, verdict, "The closed trace window was checked for the exact stimulus followed by the requested state.", "finite trace rows and exact stimulus/state identity", counterexample=[] if verdict == "true" else [{"stimulus_seen": stimulus_seen, "state_seen": state_seen}])

    if predicate == "R4":
        state = plan.inputs.get("state")
        interval = plan.inputs.get("interval")
        if not isinstance(state, str) or not isinstance(interval, Sequence) or len(interval) != 2:
            return _receipt(receipt_id, predicate, model, "unknown", "R4 requires a retained state and a two-ended closed interval.", "state-retention input contract")
        start, end = interval
        rows = [row for row in trace if start <= row.get("step", row.get("time", start)) <= end]
        if not rows:
            return _receipt(receipt_id, predicate, model, "unknown", "The closed interval contains no trace observations.", "non-empty closed trace interval")
        missing = [row for row in rows if not (state in set(row.get("active_states", ())) or row.get("state") == state)]
        verdict = "false" if missing else "true"
        return _receipt(receipt_id, predicate, model, verdict, "Every recorded point in the closed interval was checked for the exact retained state.", "finite trace window with exact active-state observations", counterexample=missing)

    return _receipt(receipt_id, predicate, model, "unknown", "The trajectory backend has no branch for this frozen predicate.", "explicit trajectory capability boundary")
