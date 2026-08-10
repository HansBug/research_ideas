"""Shared deterministic stage context helpers for PR-1A.

These helpers are deliberately local and LLM-free. They centralize the
pyfcstm parse/build path so SD-3 can hand a built model to SD-4/SD-6 without
introducing a second hidden parse/semantic implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from method.feedback.semantic import _diag_to_dict
from method.schema import StageContext


@dataclass
class BuildResult:
    """Result of the canonical parse/build helper used by SD tools."""

    ok: bool
    ast: Any | None = None
    model: Any | None = None
    diagnostics: list[dict[str, Any]] = field(default_factory=list)
    error_class: str | None = None
    error_message: str | None = None


def build_model_from_dsl(dsl_text: str) -> BuildResult:
    """Parse DSL and build a pyfcstm model in collect mode.

    The returned diagnostics are JSON-friendly dictionaries derived from the
    same structured pyfcstm ``ModelDiagnostic`` objects consumed by
    ``method.feedback.semantic``. ``ok`` means grammar parse succeeded and no
    error-severity semantic diagnostic was emitted.
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.dsl.error import GrammarParseError
        from pyfcstm.model import parse_dsl_node_to_state_machine
        from pyfcstm.utils.validate import ModelValidationError
    except ImportError as e:  # pragma: no cover - covered by environment smoke
        return BuildResult(ok=False, error_class="ImportError", error_message=f"pyfcstm not installed: {e}")

    try:
        ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    except GrammarParseError as e:
        return BuildResult(ok=False, error_class="GrammarParseError", error_message=str(e)[:500])

    try:
        model, diagnostics = parse_dsl_node_to_state_machine(ast, collect=True)
    except ModelValidationError as e:
        diagnostics = list(getattr(e, "diagnostics", []) or [])
        return BuildResult(
            ok=False,
            ast=ast,
            model=None,
            diagnostics=[_diag_to_dict(d) for d in diagnostics],
            error_class=type(e).__name__,
            error_message=str(e)[:500],
        )

    diagnostics = list(diagnostics or [])
    error_diags = [d for d in diagnostics if getattr(d, "severity", None) == "error"]
    return BuildResult(
        ok=not error_diags,
        ast=ast,
        model=model if not error_diags else None,
        diagnostics=[_diag_to_dict(d) for d in diagnostics],
        error_class="ModelValidationError" if error_diags else None,
        error_message="\n".join(getattr(d, "message", str(d)) for d in error_diags)[:500] if error_diags else None,
    )


def update_context_with_build(context: StageContext, dsl_text: str) -> BuildResult:
    """Populate ``StageContext.ast`` / ``model`` from the canonical build path."""
    result = build_model_from_dsl(dsl_text)
    context.current_dsl = dsl_text
    context.ast = result.ast
    context.model = result.model
    return result
