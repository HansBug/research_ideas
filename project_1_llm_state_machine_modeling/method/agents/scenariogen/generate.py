"""Single-step scenario generation: NL + model elements -> JSON test scenarios.

Simplified from MTI 3-step pipeline for sprint speed. Future ablation can
restore the 3-step variant (elements_mapping -> Gherkin -> structured triple).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

from method.gpt_client import chat
from method.schema import TestScenario


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
    # event paths: walk every state, collect events
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
    # variables (with init values + types)
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
                # Some pyfcstm versions wrap init in an Expr node; reduce best-effort
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


def generate_scenarios(
    requirements: str,
    dsl_text: str,
    *,
    seed: Optional[int] = None,
    model: Optional[str] = None,
) -> tuple[list[TestScenario], dict, dict]:
    """Generate test scenarios from NL + a (just-built) pyfcstm DSL.

    Parameters
    ----------
    requirements
        Original NL requirements text used to build the model.
    dsl_text
        The pyfcstm DSL text from Modeler / multistep build_pyfcstm. Must
        parse + sem cleanly (this function calls pyfcstm to extract the
        model element summary).

    Returns
    -------
    (scenarios, elements, usage)
        ``scenarios``: list of ``TestScenario`` dataclass instances.
        ``elements``: the compact model element summary fed to the LLM
        (for traceability / debug).
        ``usage``: token usage dict.
    """
    elements = _extract_model_elements(dsl_text)
    system_prompt = _load_prompt()
    elements_json = json.dumps(elements, ensure_ascii=False, indent=2, default=str)
    user_msg = (
        f"Requirements:\n{requirements.strip()}\n\n"
        f"Model elements:\n{elements_json}\n\n"
        f"Generate test scenarios. Output JSON only."
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

    scenarios = []
    for raw in raw_list:
        sc = TestScenario(
            name=str(raw.get("name", "")),
            description=str(raw.get("description", "")),
            initial_vars=dict(raw.get("initial_vars", {})),
            events=list(raw.get("events", [])),
            cycles_between_events=int(raw.get("cycles_between_events", 1)),
            extra_cycles_after_events=int(raw.get("extra_cycles_after_events", 0)),
            expected_final_state=str(raw.get("expected_final_state", "")),
            expected_vars=dict(raw.get("expected_vars", {})),
        )
        scenarios.append(sc)

    return scenarios, elements, usage
