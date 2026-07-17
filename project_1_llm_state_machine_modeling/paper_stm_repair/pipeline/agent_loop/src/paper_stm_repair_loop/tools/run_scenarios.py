from __future__ import annotations

from typing import Any

from ..pyfcstm_adapter import load_model_for_simulation, sha256_text

_LIMITATIONS = [
    "bounded_scenario_observation_only",
    "single_trace_cannot_prove_correctness",
    "expected_outcome_is_check_internal_not_semantic_oracle",
]


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v) for v in value]
    if hasattr(value, "model_dump"):
        try:
            return _jsonable(value.model_dump(mode="json"))
        except Exception:
            pass
    if hasattr(value, "to_json"):
        try:
            return _jsonable(value.to_json())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        return {str(k): _jsonable(v) for k, v in vars(value).items() if not str(k).startswith("_")}
    return str(value)


def _cycle_accounting(cycle: Any, index: int) -> dict[str, Any]:
    raw = _jsonable(cycle)
    if isinstance(raw, dict):
        return {
            "cycle_index": index,
            "input_events": list(raw.get("input_events") or []),
            "consumed_events": list(raw.get("consumed_events") or []),
            "unconsumed_events": list(raw.get("unconsumed_events") or []),
            "raw": raw,
        }
    return {"cycle_index": index, "input_events": [], "consumed_events": [], "unconsumed_events": [], "raw": raw}


def _events_from(spec: dict[str, Any]) -> tuple[list[str] | None, str | None]:
    unbound = spec.get("unbound_event_labels")
    if isinstance(unbound, list) and unbound:
        return None, "executable_spec contains unbound_event_labels and cannot run a partial scenario"
    events = spec.get("events")
    if events is None:
        event = spec.get("event")
        events = [event] if event else []
    if not isinstance(events, list) or not all(isinstance(event, str) and event for event in events):
        return None, "executable_spec.events must be a list of non-empty strings"
    return list(events), None


def _match_expected(expected: Any, actual: dict[str, Any]) -> str:
    if not isinstance(expected, dict) or not expected:
        return "inconclusive"
    checks: list[bool] = []
    for key, value in expected.items():
        if key in {"current_state", "final_state", "state"}:
            checks.append(actual.get("current_state") == value)
        elif key == "state_in":
            current = actual.get("current_state")
            checks.append(isinstance(current, str) and isinstance(value, str) and (current == value or current.startswith(value + ".")))
        elif key in {"consumed_events", "unconsumed_events", "input_events"}:
            checks.append(actual.get(key) == value)
        else:
            return "inconclusive"
    if all(checks):
        return "matches"
    if any(not item for item in checks):
        return "contradicts"
    return "inconclusive"


def execute(model_text: str, checks: list[dict[str, Any]], model_path: str = "<memory>") -> dict[str, Any]:
    """Purpose: execute Discover/Confirm scenario checks on the frozen current FCSTM and record bounded trace evidence.

    Parameters: ``model_text`` and ``model_path`` are controller-bound current
    model artifacts; Agents must not supply alternate text, arbitrary paths, run
    ids, case ids, URLs, shell commands, Python/Z3, or reference/gold data.
    ``checks`` is the immutable root-initializer check list selected by the
    Controller. Scenario items use ``check_kind="scenario"`` and an
    ``executable_spec`` containing either ``events`` as a JSON list of qualified
    event names or ``event`` as binder shorthand for a one-event list. Optional
    ``expected_outcome`` may contain typed fields such as ``current_state`` or
    ``consumed_events`` for three-valued comparison.

    Returns: ``execution_status``, ``model_sha256``, ``scenario_results``,
    ``errors``, ``not_applicable``, and ``limitations``. Each scenario result
    contains ``check_id``, ``status`` (``passed``, ``failed``, ``observed``, or
    ``error``), ``expected``, ``actual``, ``expected_outcome_match_status``
    (``matches``, ``contradicts``, or ``inconclusive``), and ``trace.cycles`` with
    per-cycle ``input_events``, ``consumed_events``, and ``unconsumed_events``.

    Execution: loads the model through the pyfcstm simulation facade, creates a
    fresh ``SimulationRuntime`` for each scenario, performs the initial empty
    cycle, runs each event in the ordered bounded sequence as one public runtime
    cycle, records every ``CycleResult`` event accounting, aggregates
    input/consumed/unconsumed events, normalizes the final state, and compares
    only against the check's own typed expectation. The function does not infer
    missing checks, mutate the model, call an LLM, or read mutable state.

    Failure semantics: malformed scenario specs produce per-check ``error``
    results and a completed tool result with ``errors``; model load or simulator
    construction failure returns ``execution_status=failed``. A scenario whose
    observed behavior contradicts its typed expectation is ``status=failed`` but
    remains a normal model-behavior fact, not a tool crash. ``unknown``,
    ``timeout``, ``incomplete``, and replay-mismatch-like observations must not be
    upgraded to pass.

    Evidence limitations: one bounded trace, even with all events consumed and a
    matching final state, cannot prove global correctness, NL alignment, source
    closure, absence of bugs, property satisfaction, or Confirm acceptance. The
    comparison only answers whether this run matches the check's sealed typed
    expectation; that expectation is not an independent semantic oracle.

    Permissions: read-only against the controller-bound model and check list; no
    arbitrary paths from an Agent, alternate model/run/case selection, shell,
    Python/Z3, network, writes, mutation, or seed/reference/gold access.

    Example: ``execute(model, [{"check_id":"SC1","check_kind":"scenario","executable_spec":{"events":["Root.start","Root.go"]},"expected_outcome":{"state_in":"Root.Done"}}])`` executes the two events in order and returns per-cycle accounting with ``expected_outcome_match_status=matches`` when the final state is ``Root.Done`` or one of its descendants.
    """

    scenario_checks = [c for c in checks if c.get("check_kind") == "scenario"]
    if not scenario_checks:
        return {"execution_status": "completed", "model_sha256": sha256_text(model_text), "scenario_results": [], "errors": [], "not_applicable": True, "limitations": list(_LIMITATIONS)}
    try:
        model = load_model_for_simulation(model_text, model_path)
        from pyfcstm.simulate import SimulationRuntime

        results: list[dict[str, Any]] = []
        errors: list[dict[str, Any]] = []
        for check in scenario_checks:
            check_id = check.get("check_id")
            spec = check.get("executable_spec") or {}
            if not isinstance(spec, dict):
                error = {"check_id": check_id, "type": "InvalidScenarioSpec", "message": "executable_spec must be an object"}
                errors.append(error)
                results.append({"check_id": check_id, "status": "error", "expected_outcome_match_status": "inconclusive", "error": error})
                continue
            events, problem = _events_from(spec)
            if problem is not None or events is None:
                error = {"check_id": check_id, "type": "InvalidScenarioEvents", "message": problem or "invalid events"}
                errors.append(error)
                results.append({"check_id": check_id, "status": "error", "expected_outcome_match_status": "inconclusive", "error": error})
                continue
            runtime = SimulationRuntime(model, abstract_error_mode="log")
            try:
                cycles = [_cycle_accounting(runtime.cycle(), 0)]
                for index, event in enumerate(events, start=1):
                    cycles.append(_cycle_accounting(runtime.cycle(events=[event]), index))
                current_state = ".".join(runtime.current_state.path)
                input_events = [event for cycle in cycles[1:] for event in cycle["input_events"]]
                consumed_events = [event for cycle in cycles[1:] for event in cycle["consumed_events"]]
                unconsumed_events = [event for cycle in cycles[1:] for event in cycle["unconsumed_events"]]
                actual = {
                    "current_state": current_state,
                    "input_events": input_events,
                    "consumed_events": consumed_events,
                    "unconsumed_events": unconsumed_events,
                }
                match = _match_expected(check.get("expected_outcome"), actual)
                status = "passed" if match == "matches" else "failed" if match == "contradicts" else "observed"
                results.append({
                    "check_id": check_id,
                    "status": status,
                    "current_state": current_state,
                    "input_events": actual["input_events"],
                    "consumed_events": actual["consumed_events"],
                    "unconsumed_events": actual["unconsumed_events"],
                    "expected": check.get("expected_outcome"),
                    "actual": actual,
                    "expected_outcome_match_status": match,
                    "trace": {"cycles": cycles},
                })
            except Exception as exc:
                error = {"check_id": check_id, "type": type(exc).__name__, "message": str(exc)}
                errors.append(error)
                results.append({"check_id": check_id, "status": "error", "expected_outcome_match_status": "inconclusive", "error": error})
        return {"execution_status": "completed", "model_sha256": sha256_text(model_text), "scenario_results": results, "errors": errors, "not_applicable": False, "limitations": list(_LIMITATIONS)}
    except Exception as exc:
        return {"execution_status": "failed", "model_sha256": sha256_text(model_text), "scenario_results": [], "errors": [{"type": type(exc).__name__, "message": str(exc)}], "not_applicable": False, "limitations": [*_LIMITATIONS, "model_load_or_simulator_unavailable"]}
