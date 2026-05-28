"""pyfcstm DSL → ComponentSet。

复用 ``pyfcstm.model.parse_dsl_node_to_state_machine``，walk states/transitions/
actions/vars 抽 7 类组件。

注意：pyfcstm 不直接支持 parallel_regions / history_states — 这两类返回空 list，
与 PROTOCOL.md §2 confounder 段对齐。
"""
from __future__ import annotations

from typing import Any

from .schema import ComponentSet


def _state_path_str(s: Any) -> str:
    p = getattr(s, "path", None)
    if isinstance(p, (tuple, list)) and len(p) > 0:
        return ".".join(str(x) for x in p)
    return str(getattr(s, "name", ""))


def _expr_to_str(node: Any) -> str:
    if node is None:
        return ""
    for attr in ("source", "text", "raw"):
        v = getattr(node, attr, None)
        if isinstance(v, str) and v:
            return v
    try:
        return str(node)
    except Exception:
        return ""


def extract_pyfcstm(dsl_text: str) -> ComponentSet:
    """Parse DSL, walk model, build ComponentSet.

    Raises if DSL fails parse / sem. (Callers using this on potentially-broken
    DSL should pre-gate with eval feedback.parse/semantic.)
    """
    from pyfcstm.dsl import parse_with_grammar_entry
    from pyfcstm.model import parse_dsl_node_to_state_machine

    ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    parse_dsl_node_to_state_machine(ast)

    states_out: list[dict[str, Any]] = []
    hierarchical_out: list[dict[str, Any]] = []
    sid_counter = 0
    hid_counter = 0
    transition_defs: list[tuple[tuple[str, ...], Any, bool]] = []

    def _path_str(path: tuple[str, ...]) -> str:
        return ".".join(path)

    def _walk_state_defs(s: Any, path: tuple[str, ...], parent: str | None) -> None:
        nonlocal sid_counter, hid_counter
        name = getattr(s, "name", None)
        if not name:
            return
        children = [getattr(c, "name", str(c)) for c in getattr(s, "substates", [])]
        entry = {
            "id": f"s{sid_counter}",
            "name": name,
            "path": _path_str(path),
            "parent": parent,
            "children": children,
            "text": f"state {_path_str(path)}" + (f" {{ ... }} (children: {children})" if children else ""),
        }
        states_out.append(entry)
        sid_counter += 1
        if children:
            hierarchical_out.append({
                "id": f"hs{hid_counter}",
                "name": name,
                "children": children,
                "text": entry["text"],
            })
            hid_counter += 1
        for tr in getattr(s, "force_transitions", []) or []:
            transition_defs.append((path, tr, True))
        for tr in getattr(s, "transitions", []) or []:
            transition_defs.append((path, tr, False))
        for child in getattr(s, "substates", []) or []:
            child_name = getattr(child, "name", str(child))
            _walk_state_defs(child, (*path, child_name), name)

    root = getattr(ast, "root_state", None)
    if root is not None:
        root_name = getattr(root, "name", "")
        _walk_state_defs(root, (root_name,), None)

    transitions_out: list[dict[str, Any]] = []
    guards_out: list[dict[str, Any]] = []
    actions_out: list[dict[str, Any]] = []
    tid = 0
    gid = 0
    aid = 0
    def _state_ref_to_path(context_path: tuple[str, ...], ref: Any, *, is_source: bool) -> str:
        marker = str(ref)
        if marker == "INIT_STATE":
            return "[*]"
        if marker == "EXIT_STATE":
            return "[*]"
        if marker == "ALL":
            return "*"
        return _path_str((*context_path, marker))

    def _event_name(event_id: Any) -> str:
        if event_id is None:
            return ""
        path = getattr(event_id, "path", None)
        if isinstance(path, (tuple, list)) and path:
            return str(path[-1])
        return str(event_id)

    def _effect_code(ops: Any) -> str:
        if not ops:
            return ""
        return " ".join(str(op) for op in ops)

    for context_path, tr, is_forced in transition_defs:
        src = _state_ref_to_path(context_path, getattr(tr, "from_state", ""), is_source=True)
        tgt = _state_ref_to_path(context_path, getattr(tr, "to_state", ""), is_source=False)
        event = _event_name(getattr(tr, "event_id", None))
        guard_expr = _expr_to_str(getattr(tr, "condition_expr", None))
        effect_code = _effect_code(getattr(tr, "post_operations", None))
        text = f"{src} -> {tgt}"
        if event:
            text += f" :: {event}"
        if guard_expr:
            text += f" : if [{guard_expr}]"
        if effect_code:
            text += f" effect {{ {effect_code} }}"
        transitions_out.append({
            "id": f"t{tid}",
            "src": src,
            "tgt": tgt,
            "event": event,
            "guard": guard_expr,
            "action": effect_code,
            "is_forced": is_forced,
            "text": text,
        })
        if guard_expr:
            guards_out.append({"id": f"g{gid}", "transition_id": f"t{tid}", "expr": guard_expr, "text": text})
            gid += 1
        if effect_code:
            actions_out.append({"id": f"a{aid}", "transition_id": f"t{tid}", "code": effect_code, "text": text})
            aid += 1
        tid += 1

    return ComponentSet(
        states=states_out,
        transitions=transitions_out,
        guards=guards_out,
        actions=actions_out,
        hierarchical_states=hierarchical_out,
        source="pyfcstm",
        raw_text=dsl_text,
    )
