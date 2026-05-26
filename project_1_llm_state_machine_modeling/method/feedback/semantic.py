"""SemanticFeedback wrapper around ``pyfcstm.model.parse_dsl_node_to_state_machine``.

Second deterministic feedback source. Runs after a successful parse and
categorizes the semantic-level error (missing state, undefined variable,
dangling transition, type mismatch) using regex on the error message
(pyfcstm raises Python ``SyntaxError`` instances with descriptive ``.msg``).
"""

from __future__ import annotations

import re

from method.schema import SemanticFeedback


# Patterns based on pyfcstm/model error messages
_UNK_VAR_RE = re.compile(
    r"Unknown\s+(?:guard|during|effect|init|action|operation)?\s*variable\s+(\w+)"
)
_MISSING_STATE_RE = re.compile(r"Cannot find state ([\w./]+)")
_DANGLING_TRANSITION_RE = re.compile(r"(?:dangling|orphan) transition[^:]*:?\s*(.+?)(?:;|$)", re.IGNORECASE)
_TYPE_MISMATCH_RE = re.compile(r"type mismatch[^:]*:?\s*(.+?)(?:;|$)", re.IGNORECASE)


def check_semantic(dsl_text: str) -> SemanticFeedback:
    """Run pyfcstm AST → model conversion and return structured feedback.

    Assumes the input has already passed parse. If parse fails here, that is
    surfaced as a SemanticFeedback with ``error_class="ParseFailedFirst"``
    (the loop driver should never call this without parse passing first, but
    we guard against misuse).
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.model import parse_dsl_node_to_state_machine
    except ImportError as e:
        return SemanticFeedback(
            ok=False,
            error_class="ImportError",
            error_message=f"pyfcstm not installed: {e}",
        )

    # Try parse first (silently — if it fails this is a misuse)
    try:
        ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    except Exception as e:
        return SemanticFeedback(
            ok=False,
            error_class="ParseFailedFirst",
            error_message=f"Parse failed before semantic check could run: {str(e)[:300]}",
        )

    try:
        parse_dsl_node_to_state_machine(ast)
        return SemanticFeedback(ok=True)
    except Exception as e:
        msg = str(e)
        fb = SemanticFeedback(
            ok=False,
            error_class=type(e).__name__,
            error_message=msg[:500],
        )
        # Categorize via regex; collect all matches
        for m in _UNK_VAR_RE.finditer(msg):
            fb.undefined_vars.append(m.group(1))
        for m in _MISSING_STATE_RE.finditer(msg):
            fb.missing_states.append(m.group(1))
        for m in _DANGLING_TRANSITION_RE.finditer(msg):
            fb.dangling_transitions.append({"raw": m.group(1).strip()})
        for m in _TYPE_MISMATCH_RE.finditer(msg):
            fb.type_mismatches.append({"raw": m.group(1).strip()})
        # Deduplicate undefined_vars / missing_states
        fb.undefined_vars = list(dict.fromkeys(fb.undefined_vars))
        fb.missing_states = list(dict.fromkeys(fb.missing_states))
        return fb
