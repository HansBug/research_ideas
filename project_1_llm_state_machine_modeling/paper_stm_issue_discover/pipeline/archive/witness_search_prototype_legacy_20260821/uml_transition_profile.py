"""Fail-closed parser for the declared UML-derived transition-label fragment."""

from __future__ import annotations

from dataclasses import dataclass

PROFILE_ID = "paper1.uml251_transition_label.guard_only.v1"


@dataclass(frozen=True)
class GuardOnlyLabel:
    """One label whose complete formal shape is ``[ guard ]``."""

    guard: str
    explicit_trigger: None = None
    effect: None = None
    implicit_trigger: str = "completion"
    profile_id: str = PROFILE_ID


def parse_guard_only_label(raw_label: object) -> GuardOnlyLabel | None:
    """Parse only the profile's guard-only production; reject everything else.

    Grammar (whitespace omitted around the production)::

        guard_only_label ::= "[" guard_body "]"
        guard_body       ::= guard_atom+
        guard_atom       ::= quoted | escaped | any scalar except "[" and "]"

    The guard body is retained as opaque formal-language payload. This parser
    never interprets its words and never reads natural-language requirements.
    """

    if not isinstance(raw_label, str):
        return None
    text = raw_label.strip()
    if len(text) < 3 or text[0] != "[":
        return None

    cursor = 1
    quote: str | None = None
    escaped = False
    closing_index: int | None = None
    while cursor < len(text):
        character = text[cursor]
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif quote is not None:
            if character == quote:
                quote = None
        elif character in {'"', "'"}:
            quote = character
        elif character == "[":
            return None
        elif character == "]":
            closing_index = cursor
            break
        cursor += 1

    if escaped or quote is not None or closing_index is None:
        return None
    if text[closing_index + 1 :].strip():
        return None
    guard = text[1:closing_index].strip()
    if not guard:
        return None
    return GuardOnlyLabel(guard=guard)
