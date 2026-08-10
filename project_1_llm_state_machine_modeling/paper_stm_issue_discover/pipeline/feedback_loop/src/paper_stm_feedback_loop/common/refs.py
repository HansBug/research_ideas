"""Structured model-reference identity shared by evidence and attribution.

Attribution decides whether a False assertion may become a confirmed issue by
intersecting the frozen ``attribution_exclusions`` table with the references an
assertion actually touched.  Both sides of that intersection are produced in
different layers: ``assertions`` emits references while evaluating, and
``discover`` matches them afterwards.  Two independent matchers would drift, and
a drifted matcher fails silently -- a path that touches a compiler-owned element
would be reported clean.  Keep exactly one implementation here.
"""

from __future__ import annotations

REFERENCE_KINDS = frozenset(
    {
        "event",
        "state",
        "transition",
        "variable",
        "effect",
        "guard",
        "route_control",
    }
)


def reference_identity(value: str) -> tuple[str | None, str]:
    """Split a reference into ``(kind, path)`` using the known kind vocabulary.

    Source traces may qualify a reference with a producer namespace such as
    ``compiler:state:Root.Done``, while assertion call traces usually expose the
    bare full path ``Root.Done``.  Only the last two colon-separated segments are
    considered, and only when the second-to-last is a known kind, so a path that
    legitimately contains a colon is not mistaken for a namespace.
    """

    text = value.strip()
    parts = text.split(":")
    if len(parts) >= 2 and parts[-2] in REFERENCE_KINDS:
        return parts[-2], parts[-1]
    return None, text


def reference_matches(reference: str, observed: set[str] | frozenset[str]) -> bool:
    """Match exact structured references, never leaf-name suffixes.

    A leaf-only or suffix match would incorrectly bind unrelated regions such as
    ``Other.Idle`` or ``NotIdle``, so the kind and the complete path are compared
    after normalization.
    """

    ref_kind, ref_path = reference_identity(reference)
    for value in observed:
        text = value.strip()
        if not text:
            continue
        if text == reference:
            return True
        observed_kind, observed_path = reference_identity(text)
        if ref_kind is not None and observed_kind is not None:
            if ref_kind == observed_kind and ref_path == observed_path:
                return True
        elif ref_kind is not None and observed_kind is None:
            if ref_path == observed_path:
                return True
        elif ref_kind is None and observed_kind is not None:
            if ref_path == observed_path:
                return True
        elif ref_path == observed_path:
            return True
    return False


__all__ = ["REFERENCE_KINDS", "reference_identity", "reference_matches"]
