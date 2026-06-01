"""Single-step scenario generation: NL + model elements -> JSON test scenarios.

Each scenario contains hot-start setup (initial_state + initial_vars) plus a
list of ScenarioStep objects. Schema v2 (2026-05-26) — replaces the earlier
single-checkpoint TestScenario with the multi-step model.

Simplified from MTI 3-step pipeline for sprint speed. Future ablation can
restore the 3-step variant (elements_mapping -> Gherkin -> structured).
"""

from __future__ import annotations

from typing import Any, Optional

from method.gpt_client import chat
from method.schema import TestScenario
from method.stages.sl_scenario_generation_prompt import (
    build_sl5_scenario_generation_prompt,
    parse_sl5_scenario_generation_response,
)


def _extract_model_elements(dsl_text: str) -> dict[str, Any]:
    """Extract a compact summary of model elements from a pyfcstm DSL.

    Uses the stable ``inspect_model().to_json()`` contract instead of direct
    pyfcstm model attribute access.
    """
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine
    from pyfcstm.diagnostics import inspect_model

    ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast)
    data = inspect_model(model).to_json()

    variables: list[dict[str, Any]] = []
    for var in data.get("variables", []):
        variables.append({
            "name": var.get("name"),
            "type": var.get("type") or "int",
            "init": var.get("init_value"),
            "read_in_guards": var.get("read_in_guards", []),
            "written_in_effects": var.get("written_in_effects", []),
        })

    transitions: list[dict[str, Any]] = []

    # ``inspect_model().to_json()["transitions"]`` is a behavioral view that
    # expands each ``!`` forced transition into concrete leaf-level edges.
    # Scenario generation should see the same declaration-level artifact view as
    # eval/PROTOCOL.md §3.5, otherwise one HSM recovery rule can dominate the
    # LLM prompt with many leaf-specific duplicates.  Keep expansion_count and
    # forced_origin as audit fields.
    for forced in data.get("forced_transitions", []):
        transitions.append({
            "from": forced.get("from_path") or "*",
            "to": forced.get("to_path"),
            "event": forced.get("event"),
            "event_scope": forced.get("event_scope"),
            "guard": forced.get("guard"),
            "effect": None,
            "is_forced": True,
            "forced_origin": forced.get("original_raw"),
            "expansion_count": forced.get("expansion_count"),
        })

    for t in data.get("transitions", []):
        if t.get("is_forced"):
            continue
        transitions.append({
            "from": t.get("from_path"),
            "to": t.get("to_path"),
            "event": t.get("event"),
            "event_scope": t.get("event_scope"),
            "guard": t.get("guard"),
            "effect": t.get("effect"),
            "is_forced": False,
        })

    return {
        "root": data.get("root_state_path"),
        "states": [s.get("path") for s in data.get("states", []) if s.get("path")],
        "events": [e.get("qualified_name") for e in data.get("events", []) if e.get("qualified_name")],
        "variables": variables,
        "transitions": transitions,
        "metrics": data.get("metrics", {}),
    }


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
    messages = build_sl5_scenario_generation_prompt(
        nl=requirements,
        current_dsl=dsl_text,
        inspect_json=elements,
        design_summary={},
        grounding_map=None,
        coverage_directive=extra_directive,
    )
    content, usage = chat(
        messages=messages,
        model=model,
        temperature=0.0,
        seed=seed,
        response_format={"type": "json_object"},
    )
    scenarios = parse_sl5_scenario_generation_response(content)
    return scenarios, elements, usage
