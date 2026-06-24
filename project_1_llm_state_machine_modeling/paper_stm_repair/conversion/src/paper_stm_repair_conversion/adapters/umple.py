from __future__ import annotations

import re
from pathlib import Path

from ..models import ConversionResult, Loss, State, Transition

_CLASS_RE = re.compile(r"^class\s+(?P<name>[A-Za-z_][\w]*)\s*\{")
_STATE_START_RE = re.compile(r"^(?P<name>[A-Za-z_][\w]*)\s*\{\s*$")
_TRANSITION_RE = re.compile(
    r"^(?P<event>[A-Za-z_][\w]*(?:\([^)]*\))?)?\s*"
    r"(?:\[(?P<guard>[^\]]+)\])?\s*->\s*"
    r"(?:(?:/\{(?P<action>.*?)\}\s*)|(?:/(?P<action2>.*?)\s+))?"
    r"(?P<target>[A-Za-z_][\w]*)\s*;\s*$"
)
_ENTRY_RE = re.compile(r"^entry\s*/\{(?P<action>.*?)\}\s*$")


def convert_umple(path: Path, *, example_id: str, seed_id: str, source_format: str = "umple") -> ConversionResult:
    text = path.read_text(encoding="utf-8")
    result = ConversionResult(
        example_id=example_id,
        seed_id=seed_id,
        source_format=source_format,
        adapter="umple",
        status="converted",
        canonical_model_name=example_id,
    )
    state_map: dict[str, State] = {}
    current_state: str | None = None
    brace_depth = 0
    in_sm = False
    class_name = None
    transition_count = 0
    timing_seen = False

    def ensure_state(label: str, raw_ref: str | None = None) -> str:
        sid = label.strip()
        if sid not in state_map:
            state_map[sid] = State(id=sid, label=sid, kind="state", raw_ref=raw_ref)
        return sid

    for lineno, original in enumerate(text.splitlines(), start=1):
        line = original.strip()
        if not line:
            continue
        m_class = _CLASS_RE.match(line)
        if m_class:
            class_name = m_class.group("name")
            brace_depth += line.count("{") - line.count("}")
            continue
        if line == "sm {":
            in_sm = True
            brace_depth += 1
            continue
        if not in_sm:
            brace_depth += line.count("{") - line.count("}")
            continue
        if line == "}":
            if current_state is not None:
                current_state = None
            else:
                in_sm = False
            continue
        m_state = _STATE_START_RE.match(line)
        if m_state:
            current_state = ensure_state(m_state.group("name"), raw_ref=f"{path.name}:{lineno}")
            if not result.initial_states:
                result.initial_states.append(current_state)
            continue
        if current_state is None:
            result.diagnostics.append({"code": "R3.UMPLE.OUTSIDE_STATE", "severity": "info", "raw_ref": f"{path.name}:{lineno}", "message": line})
            continue
        m_entry = _ENTRY_RE.match(line)
        if m_entry:
            state_map[current_state].attributes.setdefault("entry_actions", []).append(m_entry.group("action"))
            continue
        m_transition = _TRANSITION_RE.match(line)
        if m_transition:
            target = ensure_state(m_transition.group("target"), raw_ref=f"{path.name}:{lineno}")
            event = (m_transition.group("event") or "").strip() or None
            action = (m_transition.group("action") or m_transition.group("action2") or "").strip() or None
            guard = (m_transition.group("guard") or "").strip() or None
            if event and event.startswith("after("):
                timing_seen = True
            transition_count += 1
            result.transitions.append(
                Transition(
                    id=f"tr_{transition_count:04d}",
                    source=current_state,
                    target=target,
                    event=event,
                    guard=guard,
                    action=action,
                    label=line.rstrip(";"),
                    raw_ref=f"{path.name}:{lineno}",
                    attributes={"raw": original},
                )
            )
            continue
        result.diagnostics.append({"code": "R3.UMPLE.IGNORED_LINE", "severity": "info", "raw_ref": f"{path.name}:{lineno}", "message": line})

    result.states = list(state_map.values())
    result.hierarchy_level = "flat"
    result.timing_level = "qualitative" if timing_seen else "none"
    result.metadata["class_name"] = class_name
    if timing_seen:
        result.status = "partial"
        result.blocking_reason = "Umple adapter preserved after(...) timer-like transitions but R3 canonical T0 semantics does not execute timing."
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:umple:timing_after",
                example_id=example_id,
                source_ref=f"{path.name}:after(...) transition",
                canonical_ref=None,
                loss_type="timing",
                severity="medium",
                rationale="after(...) timing construct is recorded as qualitative timing and not interpreted as timed automata clock semantics in R3.",
                needs_manual_review=True,
            )
        )
    if not result.states or not result.transitions:
        result.status = "blocked"
        result.blocking_reason = "Umple adapter could not extract states or transitions."
        result.losses.append(
            Loss(
                loss_id=f"{example_id}:umple:blocking",
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
