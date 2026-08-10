"""Umple state-machine 文本 → ComponentSet。

Umple sm block 简化语法：

::

    class Foo {
      sm {
        StateA {
          event1 [guard1] / action1 -> StateB;
          StateChild { ... }
        }
        ||
        Region2 { ... }
        OuterState.H  // history state ref via .H suffix
      }
    }

约定：
- 仅解析 ``sm { ... }`` / ``status { ... }`` / 第一层 brace 嵌套的 state 块
- 不严格 lex，使用基于 brace 平衡的简易扫描器（baseline 论文 reproduction 协议复用 regex 思路，
  这里改成 instance-level 抽取）
- 与 `reproduction/baselines/baseline_structure_event.py:parse_umple_counts` 大致同口径，
  但输出的是 list[dict] 而非纯计数

边界：作者级 Umple 文本（baseline GT）格式不算严格，本 extractor 在常见情形上工作；遇到
难解析样例可手工标注或在 PROTOCOL.md 中标记 known-issue。
"""
from __future__ import annotations

import re
from typing import Any

from .schema import ComponentSet


_STATE_HEADER_RE = re.compile(r"^\s*([A-Za-z_][\w]*)\s*\{\s*$")
_TRANSITION_RE = re.compile(
    r"^\s*"
    r"(?P<event>[A-Za-z_][\w]*(?:\([^)]*\))?)?"  # event, optional params
    r"\s*(?:\[(?P<guard>[^\]]*)\])?"  # [guard]
    r"\s*(?:/\s*\{?(?P<action>[^}]*?)\}?\s*)?"  # /action or /{action;}
    r"\s*->\s*(?P<target>[A-Za-z_][\w.]*)(?:\s*\.\s*H)?"
    r"\s*;?\s*$"
)


def _strip_comments(text: str) -> str:
    """Remove // line and /* */ block comments."""
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r"//[^\n]*", "", text)
    return text


def _is_state_name(name: str) -> bool:
    """Skip Umple top-level scaffolding tokens that aren't states."""
    return name not in {"class", "sm", "status", "interface", "namespace", "use"}


def _scan_states(text: str) -> list[dict[str, Any]]:
    """Walk text, find every Name { ... } block whose name is a candidate state.

    Returns list of {id, name, parent, start, end, text, depth}.
    Depth >=1 means inside another state (hierarchical).
    """
    states: list[dict[str, Any]] = []
    stack: list[dict[str, Any]] = []
    i = 0
    n = len(text)
    state_id = 0
    while i < n:
        # Look for header
        m = re.match(r"\s*([A-Za-z_][\w]*)\s*\{", text[i:])
        if m and _is_state_name(m.group(1)):
            name = m.group(1)
            start = i + m.end() - 1  # position of '{'
            # Find matching brace
            depth = 1
            j = start + 1
            while j < n and depth > 0:
                c = text[j]
                if c == "{":
                    depth += 1
                elif c == "}":
                    depth -= 1
                j += 1
            end = j  # one past matching '}'
            parent = stack[-1]["name"] if stack else None
            depth_in_stack = len(stack)
            # Only treat as a state if depth_in_stack >= 1 (inside sm/status) OR explicitly a top-level
            # we keep all candidates and let post-filter decide
            entry = {
                "id": f"s{state_id}",
                "name": name,
                "parent": parent,
                "start": start,
                "end": end,
                "text": text[i + m.start() : end].strip(),
                "depth": depth_in_stack,
            }
            state_id += 1
            states.append(entry)
            stack.append(entry)
            # Recurse into body by advancing i past opening brace
            i = start + 1
            # When we exit naturally (no more matches), we'll need to pop. Use a sentinel — easier: do recursive scan
            # Use a queue of end positions:
            break
        else:
            i += 1
    # The above is too tricky as flat loop. Re-do recursively.
    return states


def _scan_states_recursive(text: str, parent: str | None, depth: int, state_id_counter: list[int]) -> list[dict[str, Any]]:
    """Find all top-level Name { ... } blocks in `text`, recurse into their bodies."""
    out: list[dict[str, Any]] = []
    i = 0
    n = len(text)
    while i < n:
        m = re.match(r"[\s\S]*?([A-Za-z_][\w]*)\s*\{", text[i:])
        # Use search instead of match to skip non-state tokens
        m2 = re.search(r"([A-Za-z_][\w]*)\s*\{", text[i:])
        if not m2:
            break
        name = m2.group(1)
        local_start = i + m2.start()
        brace_pos = i + m2.end() - 1
        if not _is_state_name(name):
            # advance past the brace
            i = brace_pos + 1
            continue
        # Find matching brace
        d = 1
        j = brace_pos + 1
        while j < n and d > 0:
            c = text[j]
            if c == "{":
                d += 1
            elif c == "}":
                d -= 1
            j += 1
        body_start = brace_pos + 1
        body_end = j - 1  # position of matching '}'
        body = text[body_start:body_end]
        sid = f"s{state_id_counter[0]}"
        state_id_counter[0] += 1
        entry = {
            "id": sid,
            "name": name,
            "parent": parent,
            "text": text[local_start:j].strip(),
            "depth": depth,
            "body": body,
            "_body_offset": body_start,
        }
        out.append(entry)
        # Recurse with this state as parent (depth + 1)
        children = _scan_states_recursive(body, name, depth + 1, state_id_counter)
        out.extend(children)
        i = j
    return out


def _extract_transitions(states: list[dict[str, Any]], full_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    """For each state's body, scan transition lines.

    Returns (transitions, guards, actions). guard/action are split out so they
    can be counted as separate components per paper §IV.
    """
    transitions: list[dict[str, Any]] = []
    guards: list[dict[str, Any]] = []
    actions: list[dict[str, Any]] = []
    tid = 0
    gid = 0
    aid = 0
    for st in states:
        body = st.get("body", "")
        # Strip nested state blocks from body (so we don't re-pickup transitions inside children)
        # Easiest: brace-balance subtraction
        stripped = _strip_nested_states(body)
        for raw_line in stripped.split("\n"):
            line = raw_line.strip()
            if not line or "->" not in line:
                continue
            m = _TRANSITION_RE.match(line)
            if not m:
                # fallback: still record presence of transition
                target_match = re.search(r"->\s*([A-Za-z_][\w.]*)", line)
                target = target_match.group(1) if target_match else "?"
                guard = ""
                action = ""
                event = ""
            else:
                event = (m.group("event") or "").strip()
                guard = (m.group("guard") or "").strip()
                action = (m.group("action") or "").strip()
                target = m.group("target")
            transitions.append({
                "id": f"t{tid}",
                "src": st["name"],
                "tgt": target,
                "event": event,
                "guard": guard,
                "action": action,
                "is_forced": False,
                "text": line,
            })
            if guard:
                guards.append({"id": f"g{gid}", "transition_id": f"t{tid}", "expr": guard, "text": line})
                gid += 1
            if action:
                actions.append({"id": f"a{aid}", "transition_id": f"t{tid}", "code": action, "text": line})
                aid += 1
            tid += 1
    return transitions, guards, actions


def _strip_nested_states(body: str) -> str:
    """Remove inner Name { ... } blocks from a state body so we don't double-count transitions."""
    out: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        m = re.search(r"([A-Za-z_][\w]*)\s*\{", body[i:])
        if not m:
            out.append(body[i:])
            break
        local_brace = i + m.end() - 1
        name = m.group(1)
        if not _is_state_name(name):
            out.append(body[i:local_brace + 1])
            i = local_brace + 1
            continue
        # Keep text up to here
        out.append(body[i:i + m.start()])
        # Skip the nested block
        d = 1
        j = local_brace + 1
        while j < n and d > 0:
            c = body[j]
            if c == "{":
                d += 1
            elif c == "}":
                d -= 1
            j += 1
        i = j
    return "".join(out)


def extract_umple(text: str) -> ComponentSet:
    """Parse Umple text into a ComponentSet."""
    cleaned = _strip_comments(text)
    state_id_counter = [0]
    all_blocks = _scan_states_recursive(cleaned, parent=None, depth=0, state_id_counter=state_id_counter)
    # Filter out top-level wrappers (class / sm / status) — they have depth 0 and special names
    states = [s for s in all_blocks if _is_state_name(s["name"])]
    # Hierarchical states = states that have children
    parent_names = {s["parent"] for s in states if s["parent"]}
    hierarchical = []
    hid = 0
    for s in states:
        if s["name"] in parent_names:
            children = [c["name"] for c in states if c["parent"] == s["name"]]
            hierarchical.append({
                "id": f"hs{hid}",
                "name": s["name"],
                "children": children,
                "text": s["text"][:200],
            })
            hid += 1
    transitions, guards, actions = _extract_transitions(states, cleaned)
    # Drop internal _body_offset / body fields from public output
    public_states = [{k: v for k, v in s.items() if not k.startswith("_") and k != "body"} for s in states]
    cs = ComponentSet(
        states=public_states,
        transitions=transitions,
        guards=guards,
        actions=actions,
        hierarchical_states=hierarchical,
        source="umple",
        raw_text=text,
    )
    return cs
