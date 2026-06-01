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


def _short_path(path: str | None) -> str | None:
    if path is None:
        return None
    text = str(path)
    if text in {"", "*", "[*]", "?"}:
        return text
    return text.split(".")[-1]


def _event_leaf(event: str | None) -> str:
    if not event:
        return ""
    return str(event).split(".")[-1]


def _event_text(event: str | None, event_scope: str | None) -> str:
    """Render an inspect_model event back into a human-facing DSL fragment.

    ``event`` keeps the fully-qualified path for machine comparison, while the
    text snippet mirrors Path 1 signed refs: leaf event names plus the original
    scope operator. Absolute events are rendered as root-relative ``:/...``.
    """
    if not event:
        return ""
    text = str(event)
    leaf = _event_leaf(text)
    if event_scope == "local":
        return f" :: {leaf}"
    if event_scope == "absolute":
        parts = text.split(".")
        rel = ".".join(parts[1:]) if len(parts) > 1 else leaf
        return f" : /{rel}"
    # pyfcstm reports parent-relative events as ``chain``.  Unknown future
    # scope values stay conservative and render with the normal ':' operator.
    return f" : {leaf}"


def _transition_text(t: dict[str, Any]) -> str:
    src = t.get("from_path") or "?"
    tgt = t.get("to_path") or "?"
    text = f"{src} -> {tgt}"
    text += _event_text(t.get("event"), t.get("event_scope"))
    if t.get("guard"):
        text += f" : if [{t['guard']}]"
    if t.get("effect"):
        text += f" effect {{ {t['effect']} }}"
    if t.get("is_forced"):
        text = "! " + text
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
        children_paths = list(s.get("substates") or [])
        children = [_last_path_segment(child) for child in children_paths]
        parent_path = s.get("parent_path")
        entry = {
            "id": f"s{sid}",
            "name": s.get("name") or _last_path_segment(path),
            "path": path,
            "parent": _short_path(parent_path),
            "parent_path": parent_path,
            "children": children,
            "children_paths": children_paths,
            "text": f"state {path}" + (f" {{ ... }} (children: {children})" if children else ""),
        }
        states_out.append(entry)
        if children:
            hierarchical_out.append({
                "id": f"hs{len(hierarchical_out)}",
                "name": entry["name"],
                "path": path,
                "children": children,
                "children_paths": children_paths,
                "text": entry["text"],
            })

    transitions_out: list[dict[str, Any]] = []
    guards_out: list[dict[str, Any]] = []
    actions_out: list[dict[str, Any]] = []

    def append_transition(t: dict[str, Any]) -> str:
        text = _transition_text(t)
        tr_id = f"t{len(transitions_out)}"
        guard_expr = t.get("guard") or ""
        effect_code = t.get("effect") or ""
        transitions_out.append({
            "id": tr_id,
            # Keep short src/tgt/event fields aligned with legacy signed
            # ComponentSet JSON and the Umple extractor.  Full paths remain
            # available in *_path / event_path for audit and debugging.
            "src": _short_path(t.get("from_path")),
            "tgt": _short_path(t.get("to_path")),
            "from_path": t.get("from_path"),
            "to_path": t.get("to_path"),
            "event": _event_leaf(t.get("event")),
            "event_path": t.get("event") or "",
            "event_scope": t.get("event_scope"),
            "guard": guard_expr,
            "action": effect_code,
            "effect": effect_code,
            "is_forced": bool(t.get("is_forced", False)),
            "forced_origin": t.get("forced_origin") or t.get("original_raw"),
            "expansion_count": t.get("expansion_count"),
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
        return tr_id

    # ``inspect_model().to_json()['transitions']`` is behavioral: it includes
    # leaf-level expansions for ``!`` forced transitions.  Path 1/2 eval IR is
    # declaration-level, so skip expanded forced rows and add one component per
    # original declaration from ``forced_transitions`` below.
    for forced in data.get("forced_transitions", []):
        append_transition({
            "from_path": forced.get("from_path") or "*",
            "to_path": forced.get("to_path"),
            "event": forced.get("event"),
            "event_scope": forced.get("event_scope"),
            "guard": forced.get("guard") or "",
            "effect": "",  # pyfcstm forced declarations cannot carry effects.
            "is_forced": True,
            "forced_origin": forced.get("original_raw"),
            "original_raw": forced.get("original_raw"),
            "expansion_count": forced.get("expansion_count"),
        })

    for t in data.get("transitions", []):
        if t.get("is_forced"):
            continue
        append_transition(t)

    return ComponentSet(
        states=states_out,
        transitions=transitions_out,
        guards=guards_out,
        actions=actions_out,
        hierarchical_states=hierarchical_out,
        source="pyfcstm",
        raw_text=dsl_text,
    )
