from __future__ import annotations

import re
from pathlib import Path

from ..models import ConversionResult, Loss, State, Transition

_TRANSITION_RE = re.compile(r"^(?P<src>.+?)\s*-+>\s*(?P<dst>.+?)(?:\s*:\s*(?P<label>.*))?$")
_STATE_BLOCK_RE = re.compile(r"^state\s+(?P<name>.+?)\s*\{\s*$")
_STATE_ALIAS_RE = re.compile(r"^state\s+(?P<name>.+?)(?:\s+as\s+(?P<alias>[A-Za-z_][\w.-]*))?\s*$")
_STATE_BODY_RE = re.compile(r"^(?P<name>[^:]+?)\s*:\s*(?P<body>.*)$")


def _clean_token(token: str) -> str:
    token = token.strip()
    if token.startswith('"') and token.endswith('"') and len(token) >= 2:
        token = token[1:-1]
    return token.strip()


def _state_id(label: str, parent: str | None = None) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z_]+", "_", label.strip()).strip("_") or "anon"
    if parent:
        return f"{parent}.{cleaned}"
    return cleaned


def _split_label(label: str | None) -> tuple[str | None, str | None, str | None]:
    if not label:
        return None, None, None
    raw = label.strip()
    event_part = raw
    action = None
    if "/" in event_part:
        event_part, action_part = event_part.split("/", 1)
        action = action_part.strip() or None
    guard = None
    event = event_part.strip() or None
    if event_part and "[" in event_part and "]" in event_part:
        before, rest = event_part.split("[", 1)
        guard_text, after = rest.split("]", 1)
        guard = guard_text.strip() or None
        event = (before + after).strip() or None
    return event, guard, action


def convert_plantuml(path: Path, *, example_id: str, seed_id: str, source_format: str = "plantuml") -> ConversionResult:
    text = path.read_text(encoding="utf-8")
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=source_format,
        adapter="plantuml",
        status="converted",
        canonical_model_name=example_id,
    )
    state_map: dict[str, State] = {}
    stack: list[str] = []
    transition_count = 0
    # Pre-scan top-level composite names so transitions inside a block can still
    # target an already/soon-to-be declared top-level state without inventing a
    # nested state with the same label. This is intentionally conservative and
    # only covers the smoke fixture subset.
    top_level_labels: set[str] = set()
    pre_stack_depth = 0
    for pre_line in text.splitlines():
        stripped = pre_line.strip()
        block = _STATE_BLOCK_RE.match(stripped)
        if block and pre_stack_depth == 0:
            top_level_labels.add(_clean_token(block.group("name")))
        pre_stack_depth += stripped.count("{") - stripped.count("}")

    def ensure_state(token: str, *, parent: str | None = None, kind: str = "state", raw_ref: str | None = None) -> str:
        label = _clean_token(token)
        effective_parent = parent
        if label == "[*]":
            base = "initial" if kind == "initial" else "final"
            sid = _state_id(base, effective_parent)
            label = base
        else:
            if parent and label in top_level_labels:
                effective_parent = None
            sid = _state_id(label, effective_parent)
        if sid not in state_map:
            state_map[sid] = State(id=sid, label=label, kind=kind, parent=effective_parent, raw_ref=raw_ref)
        elif kind in {"initial", "final"} and state_map[sid].kind == "state":
            state_map[sid].kind = kind
        return sid

    for lineno, original in enumerate(text.splitlines(), start=1):
        line = original.strip()
        if not line or line.startswith("'") or line.startswith("@start") or line.startswith("@end"):
            continue
        if line == "}":
            if stack:
                stack.pop()
            continue
        m_block = _STATE_BLOCK_RE.match(line)
        if m_block:
            label = _clean_token(m_block.group("name"))
            parent = stack[-1] if stack else None
            sid = ensure_state(label, parent=parent, kind="composite", raw_ref=f"{path.name}:{lineno}")
            if state_map[sid].kind == "state":
                state_map[sid].kind = "composite"
            stack.append(sid)
            continue
        m_transition = _TRANSITION_RE.match(line)
        if m_transition:
            parent = stack[-1] if stack else None
            src_token = _clean_token(m_transition.group("src"))
            dst_token = _clean_token(m_transition.group("dst"))
            src_kind = "initial" if src_token == "[*]" else "state"
            dst_kind = "final" if dst_token == "[*]" else "state"
            src = ensure_state(src_token, parent=parent, kind=src_kind, raw_ref=f"{path.name}:{lineno}")
            dst = ensure_state(dst_token, parent=parent, kind=dst_kind, raw_ref=f"{path.name}:{lineno}")
            label = m_transition.group("label")
            event, guard, action = _split_label(label)
            transition_count += 1
            result.transitions.append(
                Transition(
                    id=f"tr_{transition_count:04d}",
                    source=src,
                    target=dst,
                    event=event,
                    guard=guard,
                    action=action,
                    label=label.strip() if label else None,
                    scope=parent,
                    raw_ref=f"{path.name}:{lineno}",
                    attributes={"raw": original},
                )
            )
            if src_kind == "initial" and src not in result.initial_states:
                result.initial_states.append(src)
            if dst_kind == "final" and dst not in result.final_states:
                result.final_states.append(dst)
            continue
        m_state_alias = _STATE_ALIAS_RE.match(line)
        if m_state_alias:
            ensure_state(m_state_alias.group("alias") or m_state_alias.group("name"), parent=stack[-1] if stack else None, raw_ref=f"{path.name}:{lineno}")
            continue
        m_state_body = _STATE_BODY_RE.match(line)
        if m_state_body:
            state_id = ensure_state(m_state_body.group("name"), parent=stack[-1] if stack else None, raw_ref=f"{path.name}:{lineno}")
            body = (m_state_body.group("body") or "").strip()
            if body:
                state_map[state_id].attributes.setdefault("plantuml_state_body_lines", []).append({"body": body, "raw_ref": f"{path.name}:{lineno}"})
                result.diagnostics.append({
                    "code": "R3.PUML.STATE_BODY_PRESERVED",
                    "severity": "info",
                    "raw_ref": f"{path.name}:{lineno}",
                    "state_id": state_id,
                    "message": "PlantUML state body line preserved as state attribute; it is not interpreted as executable behavior in R3.",
                })
            continue
        result.diagnostics.append({"code": "R3.PUML.IGNORED_LINE", "severity": "info", "raw_ref": f"{path.name}:{lineno}", "message": line})

    result.states = list(state_map.values())
    result.hierarchy_level = "hierarchical" if any(state.parent for state in result.states) else "flat"
    result.timing_level = "none"
    if not result.states or not result.transitions:
        result.status = "blocked"
        result.blocking_reason = "PlantUML adapter could not extract states or transitions."
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:plantuml:blocking",
                example_id=example_id,
                source_ref=path.name,
                canonical_ref=None,
                loss_type="structure",
                severity="blocking",
                rationale=result.blocking_reason,
                needs_manual_review=True,
            )
        )
    return result
