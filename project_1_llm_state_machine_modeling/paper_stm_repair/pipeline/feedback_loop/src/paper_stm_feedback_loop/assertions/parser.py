"""Parser for LLM assertion scripts.

Ported pure assertion-script execution semantics from legacy agent_loop eval_env
at source commit c8c1ccba and adapted to require a prefix plus terminal assert
shape.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Any

from .pyfcstm_adapter import sha256_text


@dataclass(frozen=True)
class ParsedAssertionScript:
    """Parsed prefix statements plus terminal assert expression."""

    source: str
    prefix_source: str
    terminal_expression: str
    failure_message: str
    source_sha256: str
    terminal_sha256: str
    prefix_ast: ast.Module
    terminal_ast: ast.Expression

    def to_json(self) -> dict[str, Any]:
        return {
            "source_sha256": self.source_sha256,
            "prefix_source": self.prefix_source,
            "terminal_expression": self.terminal_expression,
            "failure_message": self.failure_message,
            "terminal_sha256": self.terminal_sha256,
        }


class AssertionScriptSyntaxError(ValueError):
    """Raised when a script is not prefix statements plus one terminal assert."""


def parse_assertion_script(source: str) -> ParsedAssertionScript:
    """Parse a script whose last statement is `assert <expr>`.

    The terminal assert is not executed as a Python assert statement. Its test
    expression is extracted for strict-bool evaluation so strict `False` can be
    reported as sealed contradiction while `AssertionError` from prefix code is
    invalid.
    """

    if not isinstance(source, str) or not source.strip():
        raise AssertionScriptSyntaxError("assertion script must be a non-empty string")
    try:
        module = ast.parse(source, mode="exec")
    except SyntaxError as exc:
        raise AssertionScriptSyntaxError(str(exc)) from exc
    if not module.body or not isinstance(module.body[-1], ast.Assert):
        raise AssertionScriptSyntaxError("assertion script must end with a terminal assert statement")
    if any(isinstance(stmt, ast.Assert) for stmt in module.body[:-1]):
        raise AssertionScriptSyntaxError("only the final statement may be an assert")
    terminal = module.body[-1]
    if not isinstance(terminal.msg, ast.Constant) or not isinstance(
        terminal.msg.value, str
    ):
        raise AssertionScriptSyntaxError(
            "terminal assert must use a literal string failure message"
        )
    expr_source = ast.get_source_segment(source, terminal.test) or ast.unparse(terminal.test)
    prefix_module = ast.Module(body=module.body[:-1], type_ignores=[])
    ast.fix_missing_locations(prefix_module)
    terminal_expr = ast.Expression(body=terminal.test)
    ast.fix_missing_locations(terminal_expr)
    prefix_source = "\n".join(ast.unparse(stmt) for stmt in module.body[:-1])
    return ParsedAssertionScript(
        source=source,
        prefix_source=prefix_source,
        terminal_expression=expr_source.strip(),
        failure_message=terminal.msg.value,
        source_sha256=sha256_text(source),
        terminal_sha256=sha256_text(expr_source.strip()),
        prefix_ast=prefix_module,
        terminal_ast=terminal_expr,
    )


__all__ = ["AssertionScriptSyntaxError", "ParsedAssertionScript", "parse_assertion_script"]
