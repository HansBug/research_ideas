"""Single-step scenario generation: NL + model elements -> JSON test scenarios.

Each scenario contains hot-start setup (initial_state + initial_vars) plus a
list of ScenarioStep objects. Schema v2 (2026-05-26) — replaces the earlier
single-checkpoint TestScenario with the multi-step model.

Simplified from MTI 3-step pipeline for sprint speed. Future ablation can
restore the 3-step variant (elements_mapping -> Gherkin -> structured).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from method.gpt_client import chat
from method.schema import ScenarioStep, TestScenario


_PROMPT_PATH = Path(__file__).resolve().parent.parent.parent / "prompts" / "scenariogen" / "generate_scenarios.txt"


def _load_prompt() -> str:
    if not _PROMPT_PATH.exists():
        raise FileNotFoundError(f"scenariogen prompt not found: {_PROMPT_PATH}")
    return _PROMPT_PATH.read_text(encoding="utf-8")


def _extract_model_elements(dsl_text: str) -> dict[str, Any]:
    """Extract a compact summary of model elements from a pyfcstm DSL.

    Run parse + sem first; if either fails, raise.
    """
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine

    ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast)

    root_name = model.root_state.name
    state_paths: list[str] = []
    for s in model.walk_states():
        if isinstance(s.path, tuple) and len(s.path) > 0:
            state_paths.append(".".join(s.path))

    event_paths: list[str] = []
    seen_events: set[str] = set()
    for s in model.walk_states():
        events = getattr(s, "events", None) or {}
        for ev_name, ev in events.items():
            ev_path_tuple = getattr(ev, "path", None)
            if ev_path_tuple is not None:
                ev_full = ".".join(ev_path_tuple)
                if ev_full not in seen_events:
                    seen_events.add(ev_full)
                    event_paths.append(ev_full)

    variables: list[dict[str, Any]] = []
    for var_name, var_def in (model.defines or {}).items():
        var_type = "int"
        init_val: Any = 0
        if var_def is not None:
            t_attr = getattr(var_def, "type", None) or getattr(var_def, "var_type", None)
            if t_attr is not None:
                var_type = str(t_attr).lower()
            init_attr = getattr(var_def, "init", None) or getattr(var_def, "init_value", None) or getattr(var_def, "value", None)
            if init_attr is not None:
                init_val = getattr(init_attr, "value", init_attr)
        variables.append({"name": var_name, "type": var_type, "init": init_val})

    return {
        "root": root_name,
        "states": state_paths,
        "events": event_paths,
        "variables": variables,
    }


def _strip_json_fence(content: str) -> str:
    s = content.strip()
    if not s.startswith("```"):
        return s
    parts = s.split("```")
    if len(parts) >= 2:
        body = parts[1]
        if body.startswith("json"):
            body = body[4:]
        elif body.startswith("JSON"):
            body = body[4:]
        return body.strip()
    return s


def _parse_step(raw: dict[str, Any]) -> ScenarioStep:
    """Parse a single step dict (with None-aware handling for events / expected_*)."""
    # events: None / [] / list[str]
    events_raw = raw.get("events")
    if events_raw is None:
        events: Optional[list[str]] = None
    elif isinstance(events_raw, list):
        events = [str(e) for e in events_raw]
    else:
        # malformed — try to recover: treat as single-element
        events = [str(events_raw)]

    # expected_state: None / str
    expected_state_raw = raw.get("expected_state")
    expected_state: Optional[str] = None if expected_state_raw is None else str(expected_state_raw)

    # expected_vars: None / dict
    expected_vars_raw = raw.get("expected_vars")
    if expected_vars_raw is None:
        expected_vars: Optional[dict[str, Any]] = None
    elif isinstance(expected_vars_raw, dict):
        expected_vars = dict(expected_vars_raw)
    else:
        expected_vars = None  # malformed, treat as "don't care"

    return ScenarioStep(
        before_cycles=int(raw.get("before_cycles", 0)),
        events=events,
        expected_state=expected_state,
        expected_vars=expected_vars,
        name=str(raw.get("name", "")),
    )


def _parse_scenario(raw: dict[str, Any]) -> TestScenario:
    """Parse a single scenario dict into a TestScenario with ScenarioStep list."""
    initial_state_raw = raw.get("initial_state")
    initial_state: Optional[str] = None if initial_state_raw is None else str(initial_state_raw)
    initial_vars = raw.get("initial_vars") or {}
    if not isinstance(initial_vars, dict):
        initial_vars = {}

    steps_raw = raw.get("steps", [])
    if not isinstance(steps_raw, list):
        steps_raw = []
    steps = [_parse_step(s) for s in steps_raw if isinstance(s, dict)]

    return TestScenario(
        name=str(raw.get("name", "")),
        description=str(raw.get("description", "")),
        initial_state=initial_state,
        initial_vars=dict(initial_vars),
        steps=steps,
    )


def generate_scenarios(
    requirements: str,
    dsl_text: str,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
    extra_directive: Optional[str] = None,
) -> tuple[list[TestScenario], dict, dict]:
    """Generate multi-step test scenarios from NL + pyfcstm DSL.

    Returns
    -------
    (scenarios, elements, usage)
        ``scenarios``: list of TestScenario dataclass instances, each with a
        ``steps`` list of ScenarioStep entries.
        ``elements``: compact model element summary fed to the LLM.
        ``usage``: token usage dict.
    """
    elements = _extract_model_elements(dsl_text)
    system_prompt = _load_prompt()
    elements_json = json.dumps(elements, ensure_ascii=False, indent=2, default=str)
    directive_block = ""
    if extra_directive:
        directive_block = (
            f"## Mandatory revision directive (overrides default behavior)\n\n"
            f"{extra_directive.strip()}\n\n"
        )
    user_msg = (
        f"Requirements:\n{requirements.strip()}\n\n"
        f"Model elements:\n{elements_json}\n\n"
        f"DSL:\n```\n{dsl_text}\n```\n\n"
        f"{directive_block}"
        f"Generate multi-step test scenarios. Output JSON only."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
        response_format={"type": "json_object"},
    )
    raw_text = _strip_json_fence(content)
    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"scenariogen: non-JSON response: {raw_text[:300]}") from e

    raw_list = parsed.get("scenarios", [])
    if not isinstance(raw_list, list):
        raise ValueError(f"scenariogen: 'scenarios' must be a list, got {type(raw_list).__name__}")

    scenarios = [_parse_scenario(s) for s in raw_list if isinstance(s, dict)]
    return scenarios, elements, usage
