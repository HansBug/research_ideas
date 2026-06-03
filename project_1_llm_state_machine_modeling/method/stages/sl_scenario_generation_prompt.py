"""SL-5 prompt generator and fake-response parser for scenario generation."""

from __future__ import annotations

from typing import Any

from method.schema import ScenarioStep, TestScenario
from method.stages.sl_prompt_common import (
    PROMPTS_ROOT,
    fenced_json,
    fenced_text,
    message_pack,
    parse_json_response,
    read_text_if_exists,
)

SCENARIO_PROMPT_PATH = PROMPTS_ROOT / "scenariogen" / "generate_scenarios.txt"


def build_sl5_scenario_generation_prompt(
    *,
    nl: str,
    current_dsl: str,
    inspect_json: dict[str, Any] | None = None,
    design_summary: dict[str, Any] | None = None,
    grounding_map: Any | None = None,
    coverage_directive: str | None = None,
    previous_scenarios: list[Any] | None = None,
    prompt_template_version: str = "sl5-scenario-generation.v2",
) -> list[dict[str, str]]:
    base_prompt = read_text_if_exists(SCENARIO_PROMPT_PATH)
    system = f"""
You are SL-5 ScenarioGen for the project-1 agent loop.
Template version: {prompt_template_version}.

Goal: generate grounded multi-step TestScenario candidates before ScenarioSet
freeze.  This is prompt generation only; do not call any provider.

{base_prompt}

Additional PR-1B contract:
- Use NL + current DSL + inspect JSON + design summary + GroundingMap.
- Output strict JSON with a top-level `scenarios` list compatible with
  method.schema.TestScenario / ScenarioStep.
- Do not change the DSL and do not invent requirements not grounded in NL.
- Respect pyfcstm simulation semantics: when `initial_state` is omitted, the
  runtime starts at the root and the first empty `cycle()` dispatches the
  `[*] -> ...` initial transition. Therefore, scenarios that fire an event from
  the default initial leaf should normally set `before_cycles: 1` before the
  first event step. Do not expect a leaf state immediately at step 0 unless you
  explicitly hot-start that leaf.
- Prefer NL/DSL-grounded local event names, for example `StartEvent` or
  `ResetEvent`, once the runtime is already in the source state. If you use a
  qualified event path, use either
  the full root-qualified path (e.g. `Root.Region.Source.Event`) or an absolute
  path understood by pyfcstm; do not repeat the root twice and do not use a
  parent-relative path from inside the source leaf such as `Region.Source.Event`.
- Avoid over-asserting weak or incidental variables. Only set
  `expected_vars` for state/action outputs explicitly grounded in the NL/DSL;
  leave sensor/environment inputs as don't-care unless the NL gives a concrete
  value and the scenario sets it in `initial_vars`.
- If `previous_scenarios` is non-empty, treat them as the current oracle draft:
  preserve their names, intent, and already-covered probes unless they are
  impossible under the DSL. Add or strengthen only the gaps named in
  `coverage_directive`; do not replace a previously useful probe with an
  unrelated happy-path scenario.
- For every scenario, make initial-state provenance explicit in `description`:
  say `default-init` when `initial_state` is omitted, or `explicit-hot-start`
  when a non-default `initial_state` is intentionally used. Hot starts are
  allowed only when they are needed to target a nested source state and must not
  hide failures that are reproducible from the default initial state.
"""
    payload = {
        "nl": nl,
        "current_dsl": current_dsl,
        "inspect_json": inspect_json or {},
        "design_summary": design_summary or {},
        "grounding_map": grounding_map,
        "coverage_directive": coverage_directive,
        "previous_scenarios": previous_scenarios or [],
    }
    user = f"""
## SL-5 input bundle
{fenced_json(payload)}

## DSL under test
{fenced_text(current_dsl, "pyfcstm")}

Generate TestScenario candidates. Output JSON only.
"""
    return message_pack(system, user)


def _parse_step(raw: dict[str, Any]) -> ScenarioStep:
    events_raw = raw.get("events")
    if events_raw is None:
        events = None
    elif isinstance(events_raw, list):
        events = [str(e) for e in events_raw]
    else:
        events = [str(events_raw)]

    expected_state_raw = raw.get("expected_state")
    expected_state = None if expected_state_raw is None else str(expected_state_raw)
    expected_vars_raw = raw.get("expected_vars")
    if expected_vars_raw is None:
        expected_vars = None
    elif isinstance(expected_vars_raw, dict):
        expected_vars = dict(expected_vars_raw)
    else:
        expected_vars = None

    before_cycles_raw = raw.get("before_cycles", 0)
    if before_cycles_raw is None:
        before_cycles: int | bool = 0
    elif isinstance(before_cycles_raw, bool):
        # Preserve fail-loudly behavior in ScenarioStep instead of accepting
        # bool as int via Python's int subclassing.
        before_cycles = before_cycles_raw
    else:
        try:
            before_cycles = int(before_cycles_raw)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"SL-5 ScenarioStep.before_cycles must be int-compatible, got {before_cycles_raw!r}"
            ) from exc

    return ScenarioStep(
        before_cycles=before_cycles,
        events=events,
        expected_state=expected_state,
        expected_vars=expected_vars,
        name=str(raw.get("name", "")),
    )


def _parse_scenario(raw: dict[str, Any]) -> TestScenario:
    if not isinstance(raw, dict):
        raise ValueError(f"SL-5 scenario item must be an object, got {type(raw).__name__}")

    steps_raw = raw.get("steps", [])
    if not isinstance(steps_raw, list):
        raise ValueError("SL-5 scenario.steps must be a list when provided")
    for index, step in enumerate(steps_raw):
        if not isinstance(step, dict):
            raise ValueError(f"SL-5 scenario.steps[{index}] must be an object")

    initial_state_raw = raw.get("initial_state")
    initial_vars = raw.get("initial_vars") or {}
    if not isinstance(initial_vars, dict):
        raise ValueError("SL-5 scenario.initial_vars must be an object when provided")
    return TestScenario(
        name=str(raw.get("name", "")),
        description=str(raw.get("description", "")),
        initial_state=None if initial_state_raw is None else str(initial_state_raw),
        initial_vars=dict(initial_vars),
        steps=[_parse_step(step) for step in steps_raw],
    )


def parse_sl5_scenario_generation_response(content: str) -> list[TestScenario]:
    parsed = parse_json_response(content, context="SL-5")
    raw_list = parsed.get("scenarios", [])
    if not isinstance(raw_list, list):
        raise ValueError("SL-5 scenarios must be a list")
    return [_parse_scenario(item) for item in raw_list]
