"""SemanticFeedback wrapper around pyfcstm structured diagnostics.

Second deterministic feedback source. Runs after a successful grammar parse
and consumes pyfcstm v0.4.0 Layer-1 ``ModelDiagnostic`` objects directly.
Diagnostic ``message`` remains human-readable context only; categorization is
based on stable ``code`` and ``refs`` payloads, not regex over exception text.
"""

from __future__ import annotations

from typing import Any, Iterable

from method.schema import SemanticFeedback


def _span_to_dict(span: Any) -> dict[str, Any] | None:
    if span is None:
        return None
    return {
        "line": getattr(span, "line", None),
        "column": getattr(span, "column", None),
        "end_line": getattr(span, "end_line", None),
        "end_column": getattr(span, "end_column", None),
    }


def _normalize_ref(value: Any) -> Any:
    """Convert pyfcstm diagnostic refs into JSON-friendly primitives."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "line") and hasattr(value, "column"):
        return _span_to_dict(value)
    if isinstance(value, dict):
        return {str(k): _normalize_ref(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_normalize_ref(v) for v in value]
    return str(value)


def _diag_to_dict(diag: Any) -> dict[str, Any]:
    return {
        "code": getattr(diag, "code", None),
        "severity": getattr(diag, "severity", None),
        "message": getattr(diag, "message", None),
        "span": _span_to_dict(getattr(diag, "span", None)),
        "refs": _normalize_ref(dict(getattr(diag, "refs", {}) or {})),
    }


def _summary_message(diags: Iterable[Any]) -> str:
    lines = []
    for diag in diags:
        code = getattr(diag, "code", "UNKNOWN")
        message = str(getattr(diag, "message", ""))
        lines.append(f"[{code}] {message}")
    return "\n".join(lines)[:500]


def _populate_from_diag(fb: SemanticFeedback, diag: Any) -> None:
    code = getattr(diag, "code", "")
    refs = dict(getattr(diag, "refs", {}) or {})
    span = _span_to_dict(getattr(diag, "span", None))
    message = getattr(diag, "message", None)

    if code == "E_UNDEFINED_VAR":
        var_name = refs.get("var_name")
        if isinstance(var_name, list):
            fb.undefined_vars.extend(str(v) for v in var_name)
        elif var_name is not None:
            fb.undefined_vars.append(str(var_name))
    elif code == "E_MISSING_STATE":
        if refs.get("reason") == "event_path_not_found":
            fb.unresolved_event_refs.append({
                "code": code,
                "event_ref": refs.get("event_ref"),
                "state_path": refs.get("state_path"),
                "referenced_from": refs.get("referenced_from"),
                "reason": refs.get("reason"),
                "span": span,
                "message": message,
                "refs": _normalize_ref(refs),
            })
            return
        state_path = refs.get("state_path")
        if state_path is not None:
            fb.missing_states.append(str(state_path))
        fb.dangling_transitions.append({
            "src": refs.get("referenced_from"),
            "tgt": state_path,
            "reason": refs.get("reason"),
            "span": span,
            "message": message,
        })
    elif code in {"E_EVENT_REF_INVALID", "E_EVENT_NOT_FOUND"}:
        fb.unresolved_event_refs.append({
            "code": code,
            "event_ref": refs.get("event_ref"),
            "scope": refs.get("scope"),
            "searched_from": refs.get("searched_from"),
            "reason": refs.get("reason"),
            "span": span,
            "message": message,
            "refs": _normalize_ref(refs),
        })
    elif code == "E_DANGLING_TRANSITION":
        fb.dangling_transitions.append({
            "src": refs.get("src"),
            "tgt": refs.get("tgt"),
            "reason": refs.get("reason"),
            "span": span,
            "message": message,
        })
    elif code == "E_TYPE_MISMATCH":
        fb.type_mismatches.append({
            "expected": refs.get("expected"),
            "actual": refs.get("actual"),
            "expr_text": refs.get("expr_text"),
            "span": span,
            "message": message,
        })
    else:
        fb.other_errors.append(_diag_to_dict(diag))


def _dedupe_preserve_order(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def check_semantic(dsl_text: str) -> SemanticFeedback:
    """Run pyfcstm AST → model conversion and return structured feedback.

    The model is built in pyfcstm collect mode so multiple semantic diagnostics
    can be surfaced in one LLM repair prompt. ``ok=True`` means no error-level
    semantic diagnostic was emitted. Design-health warnings from
    ``inspect_model()`` are intentionally out of scope for this gate.
    """
    try:
        from pyfcstm.dsl import parse_with_grammar_entry
        from pyfcstm.dsl.error import GrammarParseError
        from pyfcstm.model import parse_dsl_node_to_state_machine
        from pyfcstm.utils.validate import ModelValidationError
    except ImportError as e:
        return SemanticFeedback(
            ok=False,
            error_class="ImportError",
            error_message=f"pyfcstm not installed: {e}",
        )

    try:
        ast = parse_with_grammar_entry(dsl_text, "state_machine_dsl")
    except GrammarParseError as e:
        return SemanticFeedback(
            ok=False,
            error_class="ParseFailedFirst",
            error_message=f"Parse failed before semantic check could run: {str(e)[:300]}",
        )

    try:
        _model, diagnostics = parse_dsl_node_to_state_machine(ast, collect=True)
    except ModelValidationError as e:
        diagnostics = list(getattr(e, "diagnostics", []) or [])
        if not diagnostics:
            return SemanticFeedback(
                ok=False,
                error_class=type(e).__name__,
                error_message=str(e)[:500],
            )

    diagnostics = list(diagnostics or [])
    error_diags = [d for d in diagnostics if getattr(d, "severity", None) == "error"]
    if not error_diags:
        return SemanticFeedback(
            ok=True,
            diagnostics=[_diag_to_dict(d) for d in diagnostics],
        )

    fb = SemanticFeedback(
        ok=False,
        error_class="ModelValidationError",
        error_message=_summary_message(error_diags),
        diagnostics=[_diag_to_dict(d) for d in diagnostics],
    )
    for diag in error_diags:
        _populate_from_diag(fb, diag)
    fb.undefined_vars = _dedupe_preserve_order(fb.undefined_vars)
    fb.missing_states = _dedupe_preserve_order(fb.missing_states)
    return fb
