"""ParseFeedback wrapper around ``pyfcstm.dsl.parse_with_grammar_entry``.

The first deterministic feedback source in the agent loop. Since pyfcstm
already exposes structured ``GrammarParseError.errors`` entries, this module
reads those entries directly instead of regex-matching ``str(e)``. The human
message remains available as ``error_message``, but downstream repair logic is
anchored on stable fields: line / column / offending token / snippet.
"""

from __future__ import annotations

import re
from typing import Any

from method.schema import ParseFeedback


_EXPECTING_RE = re.compile(r"expecting\s+(?P<expected>.+)$", re.IGNORECASE)


def _extract_snippet(dsl_text: str, line: int, col: int, ctx_chars: int = 40) -> str:
    """Return the source line plus a ``^`` pointer at a 0-based column.

    ``pyfcstm`` forwards ANTLR's column value, which is 0-based. Keep the
    reported ``col`` unchanged for traceability and convert only when slicing.
    """
    lines = dsl_text.split("\n")
    if line < 1 or line > len(lines):
        return ""
    target_line = lines[line - 1]
    col0 = max(0, col)
    start = max(0, col0 - ctx_chars)
    end = min(len(target_line), col0 + ctx_chars)
    window = target_line[start:end]
    pointer_offset = max(0, col0 - start)
    pointer = " " * pointer_offset + "^"
    prefix = "..." if start > 0 else ""
    return f"{prefix}{window}\n{prefix}{pointer}"


def _error_attr(err: Any, *names: str) -> Any:
    for name in names:
        if hasattr(err, name):
            return getattr(err, name)
    return None


def _expected_tokens(err: Any) -> list[str]:
    """Best-effort extraction from ANTLR raw messages.

    This is intentionally not a correctness-critical regex. Structured
    positioning comes from ``GrammarParseError.errors``; this only enriches the
    prompt when ANTLR happens to render an ``expecting ...`` suffix.
    """
    raw_msg = str(_error_attr(err, "raw_msg") or "")
    m = _EXPECTING_RE.search(raw_msg)
    if not m:
        return []
    raw = m.group("expected").strip()
    return [t.strip().strip("{}'") for t in re.split(r",|\bor\b", raw) if t.strip()]


def _error_to_diagnostic(err: Any) -> dict[str, Any]:
    line = _error_attr(err, "line", "lineno")
    col = _error_attr(err, "column")
    got = _error_attr(err, "offending_symbol_text", "offending_text")
    msg = _error_attr(err, "msg") or str(err)
    return {
        "code": type(err).__name__,
        "line": line,
        "col": col,
        "got": got,
        "message": msg,
        "raw_message": _error_attr(err, "raw_msg"),
    }


def check_parse(dsl_text: str) -> ParseFeedback:
    """Run pyfcstm grammar parse and return structured feedback.

    Returns ``ParseFeedback(ok=True)`` on success, otherwise populates
    ``line / col / got / snippet / expected_tokens / error_class /
    error_message / diagnostics`` from ``GrammarParseError.errors``.
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
        errors_list = list(getattr(e, "filtered_errors", None) or getattr(e, "errors", None) or [])
        first = errors_list[0] if errors_list else None
        first_msg = str(first) if first is not None else str(e)

        line = col = None
        got = None
        snippet = None
        expected_tokens: list[str] = []
        if first is not None:
            line = _error_attr(first, "line", "lineno")
            col = _error_attr(first, "column")
            got = _error_attr(first, "offending_symbol_text", "offending_text")
            if isinstance(line, int) and isinstance(col, int):
                snippet = _extract_snippet(dsl_text, line, col)
            expected_tokens = _expected_tokens(first)

        return ParseFeedback(
            ok=False,
            line=line,
            col=col,
            got=got,
            snippet=snippet,
            expected_tokens=expected_tokens,
            error_class="GrammarParseError",
            error_message=first_msg[:500],
            diagnostics=[_error_to_diagnostic(err) for err in errors_list],
        )
    except Exception as e:
        return ParseFeedback(
            ok=False,
            error_class=type(e).__name__,
            error_message=str(e)[:500],
        )
