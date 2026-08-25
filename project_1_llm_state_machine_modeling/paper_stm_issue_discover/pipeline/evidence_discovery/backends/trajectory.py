from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..evidence.receipts import RawReceipt
from ..inputs.models import ModelIR


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
) -> RawReceipt:
    return RawReceipt(
        receipt_id=receipt_id,
        backend=f"trajectory:{predicate}",
        terminal_state="completed" if verdict in {"true", "false"} else "unknown",
        verdict=verdict,
        reason=reason,
        basis=basis,
        counterexample=counterexample or [],
        trace=trace or [],
        run_metadata={
            "algorithm_version": "trajectory-closed-window.v1",
            "model_hash": plan_model_hash(model),
            "closed_trace_contract": True,
        },
    )


def plan_model_hash(model: ModelIR) -> str:
    """Return the same source-text identity used by the other deterministic backends."""

    import hashlib

    return "sha256:" + hashlib.sha256(model.source_text.encode("utf-8")).hexdigest()


def run_trajectory(plan: PredicatePlan, model: ModelIR, receipt_id: str) -> RawReceipt:
    predicate = plan.predicate_id or "unknown"
    scenario = _mapping(plan.inputs.get("scenario"))
    if scenario is None:
        return _receipt(receipt_id, predicate, model, "unknown", "The trajectory predicate lacks a structured scenario contract.", "scenario must be a closed JSON object")

    if predicate == "R1":
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
