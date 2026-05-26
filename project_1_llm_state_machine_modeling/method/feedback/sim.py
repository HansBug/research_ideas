"""Sim feedback wrapper: run pyfcstm SimulationRuntime against test scenarios.

A scenario is a (initial_vars, events, expected_final_state, expected_vars)
quadruple. The sim wrapper:

1. Parses + builds the model from the supplied DSL.
2. For each scenario:
   a. Constructs a fresh ``SimulationRuntime`` with ``abstract_error_mode='log'``.
   b. Optionally seeds initial vars (post-init, since pyfcstm doesn't expose
      a clean "hot-start with initial vars" knob in this main-branch snapshot;
      we mutate ``runtime.vars`` after the first cycle, which is acceptable
      because the cycle has already established a valid stable boundary).
   c. Runs ``cycles_between_events`` cycles, injects an event, repeats for
      each event in the list.
   d. Runs ``extra_cycles_after_events`` cycles after the last event.
   e. Compares actual ``runtime.current_state`` path + ``runtime.vars`` to
      the scenario's ``expected_final_state`` / ``expected_vars``.
3. Aggregates per-scenario pass/fail into a single ``SimFeedback``.

The wrapper is the third deterministic feedback source in Phase G of the
agent loop, paired with the test-scenario generation step.
"""

from __future__ import annotations

from typing import Any, Optional

from method.schema import ScenarioViolation, SimFeedback, TestScenario


def _state_path_str(state: Any) -> str:
    """Reduce a pyfcstm runtime state object to its dotted path string."""
    if state is None:
        return ""
    p = getattr(state, "path", None)
    if isinstance(p, (tuple, list)) and len(p) > 0:
        return ".".join(str(x) for x in p)
    name = getattr(state, "name", None)
    return str(name) if name is not None else str(state)


def _vars_to_dict(runtime_vars: Any) -> dict[str, Any]:
    """Convert ``runtime.vars`` (a mapping-like) to a plain dict."""
    try:
        return dict(runtime_vars)
    except Exception:
        return {k: runtime_vars[k] for k in getattr(runtime_vars, "keys", lambda: [])()}


def _run_one_scenario(
    model: Any,
    scenario: TestScenario,
    *,
    cycle_safety_cap: int = 2000,
) -> ScenarioViolation:
    """Execute one scenario against a freshly-constructed runtime.

    Returns a ``ScenarioViolation`` regardless of pass/fail — the caller
    inspects ``state_matches`` + ``var_mismatches`` + ``runtime_error`` to
    decide.
    """
    from pyfcstm.simulate import SimulationRuntime, SimulationRuntimeDfsError

    violation = ScenarioViolation(
        scenario_name=scenario.name,
        expected_state=scenario.expected_final_state,
        expected_vars=dict(scenario.expected_vars),
    )

    try:
        runtime = SimulationRuntime(model, abstract_error_mode="log")
        # Run initial cycle to establish stable boundary
        runtime.cycle()
        # Seed initial vars (mutate after the first cycle to override defaults)
        if scenario.initial_vars:
            for k, v in scenario.initial_vars.items():
                try:
                    runtime.vars[k] = v
                except Exception:
                    # vars might be a custom mapping; try setattr fallback
                    try:
                        setattr(runtime, k, v)
                    except Exception:
                        pass
        # Inject events one at a time
        total_cycles = 1
        for event_path in scenario.events:
            for _ in range(scenario.cycles_between_events):
                if total_cycles >= cycle_safety_cap:
                    break
                runtime.cycle()
                total_cycles += 1
            if total_cycles >= cycle_safety_cap:
                break
            try:
                runtime.cycle(events=[event_path])
            except LookupError as e:
                # event path could not be resolved — try short name fallback
                short_name = event_path.split(".")[-1]
                try:
                    runtime.cycle(events=[short_name])
                except Exception:
                    raise e
            total_cycles += 1
        # Extra cycles after the last event
        for _ in range(scenario.extra_cycles_after_events):
            if total_cycles >= cycle_safety_cap:
                break
            runtime.cycle()
            total_cycles += 1

        actual_state = _state_path_str(runtime.current_state)
        actual_vars = _vars_to_dict(runtime.vars)
        violation.actual_state = actual_state
        violation.actual_vars = actual_vars
        violation.state_matches = (actual_state == scenario.expected_final_state)
        # var diff
        for var_name, expected_val in scenario.expected_vars.items():
            actual_val = actual_vars.get(var_name)
            if actual_val != expected_val:
                # Tolerate int vs float numeric equality (1 == 1.0)
                try:
                    if float(actual_val) == float(expected_val):
                        continue
                except (TypeError, ValueError):
                    pass
                violation.var_mismatches[var_name] = {
                    "expected": expected_val,
                    "actual": actual_val,
                }

    except SimulationRuntimeDfsError as e:
        violation.runtime_error = f"SimulationRuntimeDfsError: {str(e)[:300]}"
    except Exception as e:
        violation.runtime_error = f"{type(e).__name__}: {str(e)[:300]}"

    return violation


def check_sim(
    dsl_text: str,
    scenarios: Optional[list[TestScenario]] = None,
    *,
    fallback_cycles: int = 3,
) -> SimFeedback:
    """Run pyfcstm sim against a list of test scenarios.

    If ``scenarios`` is empty or None, falls back to a basic sanity check:
    parse + sem + run ``fallback_cycles`` cycles to verify the model doesn't
    immediately deadlock or trigger ``SimulationRuntimeDfsError``.
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.model import parse_dsl_node_to_state_machine
        from pyfcstm.simulate import SimulationRuntime, SimulationRuntimeDfsError
    except ImportError as e:
        return SimFeedback(
            ok=False,
            setup_error=f"pyfcstm not installed: {e}",
        )

    # Parse + sem setup
    try:
        ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
        model = parse_dsl_node_to_state_machine(ast)
    except Exception as e:
        return SimFeedback(
            ok=False,
            setup_error=f"{type(e).__name__}: {str(e)[:300]}",
        )

    feedback = SimFeedback()
    scenarios = scenarios or []
    feedback.n_scenarios = len(scenarios)

    if not scenarios:
        # Fallback: just verify a few cycles run without DfsError
        try:
            runtime = SimulationRuntime(model, abstract_error_mode="log")
            for _ in range(fallback_cycles):
                runtime.cycle()
                feedback.cycles_completed += 1
            feedback.ok = True
        except SimulationRuntimeDfsError as e:
            feedback.dfs_error_class = "SimulationRuntimeDfsError"
            feedback.dfs_error_message = str(e)[:500]
            feedback.safety_limit_hit = True
        except Exception as e:
            feedback.setup_error = f"{type(e).__name__}: {str(e)[:300]}"
        return feedback

    # Run each scenario
    passes = 0
    for scenario in scenarios:
        violation = _run_one_scenario(model, scenario)
        passed = (
            violation.runtime_error is None
            and violation.state_matches
            and not violation.var_mismatches
        )
        if passed:
            passes += 1
        else:
            feedback.scenario_violations.append(violation)
        feedback.cycles_completed += 1  # at least one cycle attempted per scenario

    feedback.n_scenarios_passed = passes
    feedback.ok = (passes == len(scenarios))
    return feedback
