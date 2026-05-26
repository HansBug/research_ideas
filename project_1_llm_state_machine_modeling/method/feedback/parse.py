"""ParseFeedback wrapper around ``pyfcstm.dsl.parse_with_grammar_entry``.

The first deterministic feedback source in the agent loop. Returns a structured
``ParseFeedback`` with line / col / token info extracted from
``GrammarParseError``.
"""

from __future__ import annotations

import re

from method.schema import ParseFeedback


_LINE_COL_NEAR_RE = re.compile(r"line (\d+), column (\d+), near '([^']*)'")
_UNEXPECTED_TOKEN_RE = re.compile(r"Unexpected token '([^']+)'")


def _extract_snippet(dsl_text: str, line: int, col: int, ctx_chars: int = 40) -> str:
    """Return the source line + a `^` pointer at the error column."""
    lines = dsl_text.split("\n")
    if line < 1 or line > len(lines):
        return ""
    target_line = lines[line - 1]
    # Trim to a window around the column
    start = max(0, (col - 1) - ctx_chars)
    end = min(len(target_line), (col - 1) + ctx_chars)
    window = target_line[start:end]
    pointer_offset = max(0, (col - 1) - start)
    pointer = " " * pointer_offset + "^"
    prefix = "..." if start > 0 else ""
    return f"{prefix}{window}\n{prefix}{pointer}"


def check_parse(dsl_text: str) -> ParseFeedback:
    """Run pyfcstm grammar parse and return structured feedback.

    Returns ``ParseFeedback(ok=True)`` on success, otherwise populates
    ``line / col / got / snippet / expected_tokens / error_class / error_message``.
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry  # local import to keep schema-only callers light
        from pyfcstm.dsl.error import GrammarParseError
    except ImportError as e:
        return ParseFeedback(
            ok=False,
            error_class="ImportError",
            error_message=f"pyfcstm not installed: {e}",
        )

    try:
        parse_with_grammar_entry(dsl_text, "state_machine_dsl")
        return ParseFeedback(ok=True)
    except GrammarParseError as e:
        errors_list = getattr(e, "errors", None) or []
        first_msg = str(errors_list[0]) if errors_list else str(e)

        m = _LINE_COL_NEAR_RE.search(first_msg)
        line = col = None
        got = None
        snippet = None
        if m:
            line = int(m.group(1))
            col = int(m.group(2))
            got = m.group(3)
            snippet = _extract_snippet(dsl_text, line, col)

        # try to harvest "Unexpected token 'X'" / "Expected ..."
        tok_match = _UNEXPECTED_TOKEN_RE.search(first_msg)
        expected_tokens: list[str] = []
        if tok_match:
            # GrammarParseError typically only says "Unexpected", not "Expected".
            # Leave expected_tokens empty unless extracted from another source.
            pass

        return ParseFeedback(
            ok=False,
            line=line,
            col=col,
            got=got,
            snippet=snippet,
            expected_tokens=expected_tokens,
            error_class="GrammarParseError",
            error_message=first_msg[:500],
        )
    except Exception as e:
        return ParseFeedback(
            ok=False,
            error_class=type(e).__name__,
            error_message=str(e)[:500],
        )
