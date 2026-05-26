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
    model = parse_dsl_node_to_state_machine(ast)

    states_out: list[dict[str, Any]] = []
    hierarchical_out: list[dict[str, Any]] = []
    sid_counter = 0
    hid_counter = 0
    for s in model.walk_states():
        name = getattr(s, "name", None)
        if not name:
            continue
        path = _state_path_str(s)
        parent = None
        try:
            parent_obj = getattr(s, "parent", None)
            if parent_obj is not None:
                parent = getattr(parent_obj, "name", None)
        except Exception:
            parent = None
        # gather children
        children = []
        try:
            for c in getattr(s, "states", {}).values():
                children.append(getattr(c, "name", str(c)))
        except Exception:
            pass
        entry = {
            "id": f"s{sid_counter}",
            "name": name,
            "path": path,
            "parent": parent,
            "children": children,
            "text": f"state {path}" + (f" {{ ... }} (children: {children})" if children else ""),
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

    transitions_out: list[dict[str, Any]] = []
    guards_out: list[dict[str, Any]] = []
    actions_out: list[dict[str, Any]] = []
    tid = 0
    gid = 0
    aid = 0
    for s in model.walk_states():
        # transitions from this state
        for tr in (getattr(s, "transitions", None) or []):
            src = _state_path_str(s)
            tgt_obj = getattr(tr, "target", None) or getattr(tr, "to", None)
            if tgt_obj is None:
                tgt = "?"
            else:
                tgt = _state_path_str(tgt_obj) if hasattr(tgt_obj, "path") or hasattr(tgt_obj, "name") else str(tgt_obj)
            event = ""
            event_obj = getattr(tr, "event", None) or getattr(tr, "trigger", None)
            if event_obj is not None:
                event = getattr(event_obj, "name", None) or str(event_obj| 6 | `parallel_regions` | `||` 分隔的 region 块 | **pyfcstm 不直接支持**（A_full_ours 该项结构性为 0）|
| 7 | `history_states` | `.H` 标记（如 `Busy.H`） | **pyfcstm 不直接支持**（A_full_ours 该项结构性为 0）|
)
            guard_obj = getattr(tr, "guard", None) or getattr(tr, "condition", None)
            guard_expr = _expr_to_str(guard_obj)
            effect_obj = getattr(tr, "effect", None) or getattr(tr, "action", None)
            effect_code = _expr_to_str(effect_obj)
            is_forced = bool(getattr(tr, "is_forced", False) or getattr(tr, "forced", False))
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
        parallel_regions=[],   # pyfcstm 结构性不支持
        history_states=[],     # pyfcstm 结构性不支持
        source="pyfcstm",
        raw_text=dsl_text,
    )
