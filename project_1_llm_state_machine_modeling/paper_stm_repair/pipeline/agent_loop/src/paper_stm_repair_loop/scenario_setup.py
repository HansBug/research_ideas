from __future__ import annotations

from typing import Any


def cycle_accounting(cycle: Any, runtime: Any, index: int) -> dict[str, Any]:
    """Normalize one pyfcstm ``SimulationRuntime.cycle`` result.

    Parameters: ``cycle`` is a public pyfcstm cycle result and ``index`` is the
    controller-assigned cycle number.

    Returns: a JSON-like record with cycle index, active-state ancestry,
    variables, input/consumed/unconsumed events, and the public raw result.

    Execution: converts public ``to_json``/``model_dump``/``__dict__`` payloads
    without parsing exception strings or inferring semantic verdicts.

    Failure semantics: unknown shapes are preserved in ``raw`` with empty event
    accounting, allowing the caller to classify the assertion as unsupported or
    incomplete rather than guessing.

    Evidence limitations: per-cycle accounting shows one bounded trace only; it
    is not global correctness, NL coverage, or source attribution evidence.

    Permissions: read-only in-memory conversion; no filesystem, shell, import,
    environment, network, mutation, or reference/gold access.

    Example: ``cycle_accounting(runtime.cycle(events=["Root.go"]), 1)`` records
    exactly the events consumed during that outer cycle.
    """

    raw = _jsonable(cycle)
    current_path = ".".join(runtime.current_state.path)
    parts = current_path.split(".")
    active_states = [".".join(parts[:index]) for index in range(1, len(parts) + 1)]
    variables = _jsonable(getattr(runtime, "vars", {}))
    if isinstance(raw, dict):
        return {
            "index": index,
            "active_states": active_states,
            "variables": variables,
            "input_events": list(raw.get("input_events") or []),
            "consumed_events": list(raw.get("consumed_events") or []),
            "unconsumed_events": list(raw.get("unconsumed_events") or []),
            "fired_transitions": [],
            "limitations": ["fired_transitions_not_exposed_by_pyfcstm_cycle_result"],
            "raw": raw,
        }
    return {
        "index": index,
        "active_states": active_states,
        "variables": variables,
        "input_events": [],
        "consumed_events": [],
        "unconsumed_events": [],
        "fired_transitions": [],
        "limitations": [
            "cycle_result_shape_unsupported",
            "fired_transitions_not_exposed_by_pyfcstm_cycle_result",
        ],
        "raw": raw,
    }


def execute_cycles(model: Any, cycles: list[list[str]]) -> tuple[str, list[dict[str, Any]]]:
    """Run event cycles with pyfcstm cycle semantics.

    Parameters: ``model`` is the controller-bound parsed FCSTM model and
    ``cycles`` is an ordered list of outer cycles, each containing zero or more
    event names.  Empty lists are explicit eventless stabilization cycles.

    Returns: ``(current_state, trace_cycles)`` where ``current_state`` is the
    final dotted active state path and ``trace_cycles`` contains exactly one
    observation for every caller-provided outer cycle.

    Execution: creates one fresh ``SimulationRuntime`` and invokes
    ``SimulationRuntime.cycle`` exactly once for each requested outer cycle. It
    never inserts an initialization or stabilization cycle. Callers must include
    an explicit leading ``[]`` when initialization is required. Events remain
    available for the whole cycle according to pyfcstm semantics; repeated
    consumed event names are transition accounting, not repeated inputs.

    Failure semantics: pyfcstm load/runtime exceptions propagate to the caller so
    direct eval can return ``exception``/``unsupported`` precisely.

    Evidence limitations: a bounded trace cannot prove global correctness,
    source closure, or NL alignment.

    Permissions: read-only simulation against the in-memory model; no arbitrary
    paths, shell, environment, network, mutation, or reference/gold data.

    Example: ``execute_cycles(model, [[], ["Root.go"]])`` records exactly the
    explicit empty initialization cycle and the ``Root.go`` cycle.
    """

    from pyfcstm.simulate import SimulationRuntime

    if not isinstance(cycles, list) or not cycles:
        raise ValueError("cycles must contain at least one explicit cycle")
    runtime = SimulationRuntime(model, abstract_error_mode="log")
    trace = []
    for index, events in enumerate(cycles):
        result = runtime.cycle(events=list(events))
        trace.append(cycle_accounting(result, runtime, index))
    return ".".join(runtime.current_state.path), trace


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(item) for item in value]
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
