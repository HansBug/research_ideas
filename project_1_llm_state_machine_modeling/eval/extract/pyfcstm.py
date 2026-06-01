"""pyfcstm DSL → ComponentSet via ``pyfcstm.diagnostics.inspect_model``.

This extractor deliberately avoids walking pyfcstm's internal model objects.
The stable contract is the v0.4.0 ``inspect_model().to_json()`` payload.
Evaluation still follows ``eval/PROTOCOL.md``: ``actions`` means transition
``effect { ... }`` only, not lifecycle ``enter`` / ``during`` / ``exit`` or
aspect actions.

pyfcstm does not directly support ``parallel_regions`` / ``history_states``;
this project evaluates the 5 supported component classes only.
"""
from __future__ import annotations

from typing import Any

from .schema import ComponentSet


def _last_path_segment(path: str | None) -> str:
    if not path:
        return ""
    return str(path).split(".")[-1]


def _transition_text(t: dict[str, Any]) -> str:
    src = t.get("from_path") or "?"
    tgt = t.get("to_path") or "?"
    text = f"{src} -> {tgt}"
    if t.get("event"):
        text += f" :: {t['event']}"
    if t.get("guard"):
        text += f" : if [{t['guard']}]"
    if t.get("effect"):
        text += f" effect {{ {t['effect']} }}"
    if t.get("is_forced"):
        text = "!" + text
    return text


def extract_pyfcstm(dsl_text: str) -> ComponentSet:
    """Parse DSL, inspect the model, and build a 5-component IR.

    Raises if DSL fails parse / sem. Callers using potentially broken DSL
    should pre-gate with ``method.feedback.parse`` / ``semantic``.
    """
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine
    from pyfcstm.diagnostics import inspect_model

    ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    model = parse_dsl_node_to_state_machine(ast)
    data = inspect_model(model).to_json()

    states_out: list[dict[str, Any]] = []
    hierarchical_out: list[dict[str, Any]] = []
    for sid, s in enumerate(data.get("states", [])):
        path = s.get("path") or ""
        children = list(s.get("substates") or [])
        entry = {
            "id": f"s{sid}",
            "name": s.get("name") or _last_path_segment(path),
            "path": path,
            "parent": s.get("parent_path"),
            "children": children,
            "text": f"state {path}" + (f" {{ ... }} (children: {children})" if children else ""),
        }
        states_out.append(entry)
        if children:
            hierarchical_out.append({
                "id": f"hs{len(hierarchical_out)}",
                "name": entry["name"],
                "path": path,
                "children": children,
                "text": entry["text"],
            })

    transitions_out: list[dict[str, Any]] = []
    guards_out: list[dict[str, Any]] = []
    actions_out: list[dict[str, Any]] = []
    for tid, t in enumerate(data.get("transitions", [])):
        text = _transition_text(t)
        tr_id = f"t{tid}"
        guard_expr = t.get("guard") or ""
        effect_code = t.get("effect") or ""
        transitions_out.append({
            "id": tr_id,
            "src": t.get("from_path"),
            "tgt": t.get("to_path"),
            "from_path": t.get("from_path"),
            "to_path": t.get("to_path"),
            "event": t.get("event") or "",
            "event_scope": t.get("event_scope"),
            "guard": guard_expr,
            "action": effect_code,
            "effect": effect_code,
            "is_forced": bool(t.get("is_forced", False)),
            "forced_origin": t.get("forced_origin"),
            "text": text,
        })
        if guard_expr:
            guards_out.append({
                "id": f"g{len(guards_out)}",
                "transition_id": tr_id,
                "expr": guard_expr,
                "text": text,
            })
        if effect_code:
            actions_out.append({
                "id": f"a{len(actions_out)}",
                "transition_id": tr_id,
                "kind": "transition_effect",
                "code": effect_code,
                "text": text,
            })

    return ComponentSet(
        states=states_out,
        transitions=transitions_out,
        guards=guards_out,
        actions=actions_out,
        hierarchical_states=hierarchical_out,
        source="pyfcstm",
        raw_text=dsl_text,
    )
