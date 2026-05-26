"""Sim feedback wrapper: run pyfcstm ``SimulationRuntime`` against multi-step test scenarios.

Each TestScenario contains a sequence of ScenarioStep entries; each step is
(before_cycles, events, expected_state, expected_vars). The sim wrapper:

1. Parses + builds the model from the supplied DSL.
2. For each scenario:
   a. Constructs ``SimulationRuntime`` with ``abstract_error_mode='log'`` and
      passes ``initial_state`` / ``initial_vars`` for hot-start. **Does NOT
      auto-run an initial cycle** — full control of cycle execution belongs
      to the steps.
   b. For each step in scenario.steps:
        - run ``cycle()`` × ``before_cycles`` (empty cycles)
        - depending on ``events``:
            * ``None``: skip the cycle entirely
            * ``[]``:   ``cycle()`` once (no events injected)
            * list:    ``cycle(events=list)`` once (all events triggered together)
        - capture ``runtime.current_state`` + ``runtime.vars`` post-step
        - assert against ``expected_state`` / ``expected_vars`` if non-None
        - record StepResult with status ('pass' / 'fail' / 'error')
   c. Continue to next step on 'fail' (record violation; keep going); stop on
      'error' (runtime exception, scenario can't continue)
3. Aggregate into SimFeedback (per-scenario ScenarioResult list).
"""

from __future__ import annotations

from typing import Any, Optional

from method.schema import (
    ScenarioResult,
    ScenarioStep,
    SimFeedback,
    StepResult,
    TestScenario,
)


def _state_path_str(state: Any) -> str:
    if state is None:
        return ""
    p = getattr(state, "path", None)
    if isinstance(p, (tuple, list)) and len(p) > 0:
        return ".".join(str(x) for x in p)
    name = getattr(state, "name", None)
    return str(name) if name is not None else str(state)


def _vars_to_dict(runtime_vars: Any) -> dict[str, Any]:
    try:
        return dict(runtime_vars)
    except Exception:
        return {k: runtime_vars[k] for k in getattr(runtime_vars, "keys", lambda: [])()}


def _numeric_equal(a: Any, b: Any) -> bool:
    """Treat int/float numeric equality as equal (1 == 1.0)."""
    if a == b:
        return True
    try:
        return float(a) == float(b)
    except (TypeError, ValueError):
        return False


def _execute_step(runtime: Any, step: ScenarioStep, step_index: int) -> StepResult:
    """Execute one ScenarioStep and produce a StepResult.

    May raise SimulationRuntimeDfsError or other runtime exceptions — caller
    catches them and converts to error status.
    """
    from pyfcstm.simulate import SimulationRuntime  # noqa: F401 (kept for clarity)

    sr = StepResult(
        step_index=step_index,
        step_name=step.name or f"step_{step_index}",
    )

    # 1. before_cycles empty cycles
    for _ in range(step.before_cycles):
        runtime.cycle()

    # 2. events handling
    if step.events is None:
        pass  # skip cycle entirely
    elif step.events == []:
        runtime.cycle()
    else:
        # All events triggered together in a single cycle (supports pseudo-state chained jumps)
        runtime.cycle(events=list(step.events))

    # 3. capture actual state + vars
    sr.actual_state = _state_path_str(runtime.current_state)
    sr.actual_vars = _vars_to_dict(runtime.vars)

    # 4. state assertion (if non-None)
    if step.expected_state is not None:
        sr.state_assertion_ok = (sr.actual_state == step.expected_state)

    # 5. var assertions (None or empty dict => don't care; otherwise check only listed keys)
    expected_vars = step.expected_vars
    if expected_vars is not None and len(expected_vars) > 0:
        mismatches: dict[str, dict[str, Any]] = {}
        for k, v_expected in expected_vars.items():
            v_actual = sr.actual_vars.get(k)
            if not _numeric_equal(v_actual, v_expected):
                mismatches[k] = {"expected": v_expected, "actual": v_actual}
        sr.var_mismatches = mismatches
        sr.var_assertion_ok = (len(mismatches) == 0)

    # 6. step status
    if sr.state_assertion_ok is False or sr.var_assertion_ok is False:
        sr.status = "fail"
    else:
        sr.status = "pass"

    return sr


def _run_one_scenario(model: Any, scenario: TestScenario) -> ScenarioResult:
    """Execute one full TestScenario; produce a ScenarioResult.

    Continues on 'fail' (collects all step violations); stops immediately on
    'error' (runtime exception).
    """
    from pyfcstm.simulate import SimulationRuntime, SimulationRuntimeDfsError

    sresult = ScenarioResult(name=scenario.name, description=scenario.description)

    try:
        # Hot-start: pass initial_state + initial_vars to constructor (pyfcstm native).
        # Note: pyfcstm requires initial_vars (even if empty dict) whenever initial_state
        # is specified. Default-init (no initial_state) leaves the runtime at the root
        # state — the first cycle() then dispatches into the initial leaf via [*] -> X.
        kwargs: dict[str, Any] = {"abstract_error_mode": "log"}
        if scenario.initial_state is not None:
            kwargs["initial_state"] = scenario.initial_state
            kwargs["initial_vars"] = dict(scenario.initial_vars) if scenario.initial_vars else {}
        elif scenario.initial_vars:
            kwargs["initial_vars"] = dict(scenario.initial_vars)
        runtime = SimulationRuntime(model, **kwargs)
    except SimulationRuntimeDfsError as e:
        sresult.status = "error"
        sresult.setup_error = f"SimulationRuntimeDfsError on construct: {str(e)[:300]}"
        return sresult
    except Exception as e:
        sresult.status = "error"
        sresult.setup_error = f"{type(e).__name__} on construct: {str(e)[:300]}"
        return sresult

    # Empty steps list is valid — just a hot-start sanity check (no cycle, no assertion)
    if not scenario.steps:
        sresult.status = "pass"
        return sresult

    # Execute each step
    hit_runtime_error = False
    for i, step in enumerate(scenario.steps):
        try:
            sr = _execute_step(runtime, step, i)
        except SimulationRuntimeDfsError as e:
            sr = StepResult(
                step_index=i,
                step_name=step.name or f"step_{i}",
                status="error",
                runtime_error=f"SimulationRuntimeDfsError: {str(e)[:300]}",
                actual_state=_state_path_str(getattr(runtime, "current_state", None)),
                actual_vars=_vars_to_dict(getattr(runtime, "vars", {})),
            )
            sresult.step_results.append(sr)
            hit_runtime_error = True
            break
        except Exception as e:
            sr = StepResult(
                step_index=i,
                step_name=step.name or f"step_{i}",
                status="error",
                runtime_error=f"{type(e).__name__}: {str(e)[:300]}",
                actual_state=_state_path_str(getattr(runtime, "current_state", None)),
                actual_vars=_vars_to_dict(getattr(runtime, "vars", {})),
            )
            sresult.step_results.append(sr)
            hit_runtime_error = True
            break
        sresult.step_results.append(sr)

    # Aggregate scenario status
    if hit_runtime_error:
        sresult.status = "error"
    elif any(s.status == "fail" for s in sresult.step_results):
        sresult.status = "fail"
    else:
        sresult.status = "pass"

    return sresult


def check_sim(
    dsl_text: str,
    scenarios: Optional[list[TestScenario]] = None,
) -> SimFeedback:
    """Run pyfcstm sim against a list of multi-step test scenarios.

    Returns a SimFeedback with per-scenario, per-step detailed results
    (status, actual state/vars, var mismatches, runtime error). The downstream
    Repair agent consumes this directly as feedback.

    If ``scenarios`` is empty/None, returns a setup-only result (no scenarios
    fired); ``ok=True`` if parse+sem succeeds. This matches the agent loop
    contract where scenario generation may produce 0 scenarios in edge cases.
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.model import parse_dsl_node_to_state_machine
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
        # No scenarios provided — model parsed OK so this is a passing setup-check.
        feedback.ok = True
        return feedback

    passes = 0
    for scenario in scenarios:
        sresult = _run_one_scenario(model, scenario)
        feedback.scenario_results.append(sresult)
        if sresult.status == "pass":
            passes += 1

    feedback.n_scenarios_passed = passes
    feedback.ok = (passes == len(scenarios))
    return feedback
