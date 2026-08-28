from __future__ import annotations

from typing import Any

from .fired_trace import derive_fired_transitions


def _active_ancestry(runtime: Any) -> list[str]:
    """Return the active leaf and its ancestors, empty after termination."""

    if bool(runtime.is_ended):
        return []
    parts = ".".join(runtime.current_state.path).split(".")
    return [".".join(parts[:depth]) for depth in range(1, len(parts) + 1)]


def runtime_observation(runtime: Any, *, mode: str, state: str | None = None) -> dict[str, Any]:
    """Return terminal-safe active-state and variable facts for a runtime."""

    is_ended = bool(runtime.is_ended)
    if is_ended:
        active_states: list[str] = []
    else:
        current_path = ".".join(runtime.current_state.path)
        parts = current_path.split(".")
        active_states = [".".join(parts[:depth]) for depth in range(1, len(parts) + 1)]
    return {
        "mode": mode,
        "state": state,
        "is_ended": is_ended,
        "active_states": active_states,
        "variables": _jsonable(getattr(runtime, "vars", {})),
    }


def cycle_accounting(
    cycle: Any,
    runtime: Any,
    index: int,
    *,
    active_before: list[str] | None = None,
    transitions: list[dict[str, Any]] | None = None,
    excluded_refs: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Normalize one pyfcstm ``SimulationRuntime.cycle`` result.

    Parameters: ``cycle`` is a public pyfcstm cycle result and ``index`` is the
    controller-assigned cycle number.  ``active_before`` is the active ancestry
    captured before the cycle ran and ``transitions`` is the frozen inspect
    transition table; together they let the controller reconstruct which
    transitions fired, because the pyfcstm cycle result does not report them.
    ``excluded_refs`` is the frozen ``attribution_exclusions`` table, used to
    classify path taint.

    Returns: a JSON-like record with cycle index, terminal status, active-state
    ancestry, variables, input/consumed/unconsumed events, and the public raw
    result.

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
    is_ended = bool(runtime.is_ended)
    active_states = _active_ancestry(runtime)
    variables = _jsonable(getattr(runtime, "vars", {}))
    if not isinstance(raw, dict):
        return {
            "index": index,
            "is_ended": is_ended,
            "active_states": active_states,
            "variables": variables,
            "input_events": [],
            "consumed_events": [],
            "unconsumed_events": [],
            "fired_transitions": [],
            "path_refs": [],
            "path_taint": "ambiguous",
            "limitations": [
                "cycle_result_shape_unsupported",
                "fired_transitions_not_derivable_from_unsupported_cycle_result",
            ],
            "raw": raw,
        }
    consumed = list(raw.get("consumed_events") or [])
    record = {
        "index": index,
        "is_ended": is_ended,
        "active_states": active_states,
        "variables": variables,
        "input_events": list(raw.get("input_events") or []),
        "consumed_events": consumed,
        "unconsumed_events": list(raw.get("unconsumed_events") or []),
        "raw": raw,
    }
    if transitions is None:
        # No frozen transition table was bound, so transition identity is not
        # recoverable and the path cannot be attributed.  Say so explicitly
        # rather than reporting an empty, clean-looking path.
        record.update(
            {
                "fired_transitions": [],
                "path_refs": [],
                "path_taint": "ambiguous",
                "limitations": ["fired_transitions_require_frozen_transition_table"],
            }
        )
        return record
    derived = derive_fired_transitions(
        transitions=transitions,
        active_before=active_before or [],
        active_after=active_states,
        consumed_events=consumed,
        is_ended=is_ended,
        excluded=excluded_refs,
    )
    record.update(
        {
            "fired_transitions": list(derived["fired_transitions"]),
            "path_refs": list(derived["path_refs"]),
            "path_taint": derived["path_taint"],
            "limitations": list(derived["limitations"]),
        }
    )
    if derived["candidates"]:
        record["fired_transition_candidates"] = derived["candidates"]
    return record


def execute_cycles(
    model: Any,
    cycles: list[list[str]],
    *,
    initial_state: str | None = None,
    initial_vars: dict[str, int | float] | None = None,
    transitions: list[dict[str, Any]] | None = None,
    excluded_refs: tuple[str, ...] = (),
) -> tuple[str | None, list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    """Run event cycles with pyfcstm cycle semantics.

    Parameters: ``model`` is the controller-bound parsed FCSTM model and
    ``cycles`` is an ordered list of outer cycles, each containing zero or more
    event names.  Empty lists are explicit eventless stabilization cycles.

    Returns: ``(current_state, trace_cycles, requested_initialization, effective_initialization)`` where ``current_state`` is the
    final dotted active state path or ``None`` after model termination,
    ``trace_cycles`` contains exactly one observation for every caller-provided
    outer cycle, and initialization records show requested/effective cold or hot
    start state and variables. Every observation includes the terminal-safe
    ``is_ended`` fact.

    Execution: creates one fresh ``SimulationRuntime`` and invokes
    ``SimulationRuntime.cycle`` exactly once for each requested outer cycle. It
    never inserts an initialization or stabilization cycle. Callers must include
    an explicit leading ``[]`` when initialization is required. Events remain
    available for the whole cycle according to pyfcstm semantics; repeated
    consumed event names are transition accounting, not repeated inputs. Cold
    starts may override a subset of declared variables through ``initial_vars``;
    its keys must be exact declaration names, not qualified state-machine paths.
    Hot starts require an exact state and all declared variables.

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
    if initial_state is not None and initial_vars is None:
        raise ValueError(
            "hot start requires exact initial_state with complete initial_vars"
        )
    mode = "hot" if initial_state is not None else "cold"
    requested_initialization = {
        "mode": mode,
        "state": initial_state,
        "variables": _jsonable(initial_vars or {}),
    }
    if mode == "hot":
        declared = set(getattr(model, "defines", {}).keys())
        provided = set((initial_vars or {}).keys())
        missing = sorted(declared - provided)
        extra = sorted(provided - declared)
        if missing or extra:
            raise ValueError(
                "hot start requires complete exact initial_vars; "
                f"missing={missing}, extra={extra}"
            )
    elif initial_vars is not None:
        declared = set(getattr(model, "defines", {}).keys())
        extra = sorted(set(initial_vars) - declared)
        if extra:
            raise ValueError(
                "cold-start initial_vars may override only declared variables; "
                f"extra={extra}"
            )
    runtime = SimulationRuntime(
        model,
        abstract_error_mode="log",
        initial_state=initial_state,
        initial_vars=initial_vars,
    )
    effective_initialization = runtime_observation(runtime, mode=mode, state=initial_state)
    trace = []
    for index, events in enumerate(cycles):
        # Captured before the cycle runs: the derivation needs both endpoints and
        # the runtime only exposes the post-cycle configuration.
        active_before = _active_ancestry(runtime)
        result = runtime.cycle(events=list(events))
        trace.append(
            cycle_accounting(
                result,
                runtime,
                index,
                active_before=active_before,
                transitions=transitions,
                excluded_refs=excluded_refs,
            )
        )
    current_state = None if runtime.is_ended else ".".join(runtime.current_state.path)
    return current_state, trace, requested_initialization, effective_initialization


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
