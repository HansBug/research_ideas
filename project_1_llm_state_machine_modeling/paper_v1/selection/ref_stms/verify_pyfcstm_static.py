"""Static pyfcstm design-health verifier backed by ``inspect_model``.

This replaces the historical DSL-regex analyzer used in early Path 1
reference-STM drafting. pyfcstm v0.4.0 exposes the same checks as structured
``ModelDiagnostic`` codes via ``pyfcstm.diagnostics.inspect_model()``.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Iterable

from pyfcstm.dsl import parse_with_grammar_entry
from pyfcstm.dsl.error import GrammarParseError
from pyfcstm.model import parse_dsl_node_to_state_machine
from pyfcstm.utils.validate import ModelDiagnostic, ModelValidationError
from pyfcstm.diagnostics import inspect_model


# Old downstream static verifier treated these as hard failures even though
# pyfcstm reports them as warnings. Keep that strict drafting semantics.
DOWNSTREAM_STRICT_ERROR_CODES = {
    "W_UNWRITTEN_READ_VAR",
    "W_FORCED_NEVER_EXPANDS",
    "W_GUARD_CONST_FALSE",
}

# Backward-compatible bridge for legacy reference models that marked external
# inputs in comments before pyfcstm grew first-class abstract-action guidance.
_EXTERNAL_RE = re.compile(r"\bdef\s+\w+\s+(\w+)\s*=[^;]*;\s*//[^\n]*@(?:external|input)")
_EXTERNAL_SUPPRESSED_CODES = {"W_UNWRITTEN_READ_VAR", "W_GUARD_VARS_NEVER_CHANGE"}


def _grammar_error_diag(err: object) -> tuple[str, str, str]:
    return ("error", type(err).__name__, str(err))


def _is_external_suppressed(src_text: str, diag: ModelDiagnostic) -> bool:
    if diag.code not in _EXTERNAL_SUPPRESSED_CODES:
        return False
    external_vars = set(_EXTERNAL_RE.findall(src_text))
    if diag.code == "W_UNWRITTEN_READ_VAR":
        return bool(diag.refs.get("var_name") in external_vars)
    if diag.code == "W_GUARD_VARS_NEVER_CHANGE":
        guard_vars = diag.refs.get("guard_vars") or []
        return bool(guard_vars) and all(str(var) in external_vars for var in guard_vars)
    return False


def _severity(diag: ModelDiagnostic) -> str:
    if diag.code in DOWNSTREAM_STRICT_ERROR_CODES:
        return "error"
    return str(diag.severity)


def analyze(src_text: str) -> list[tuple[str, str, str]]:
    """Return ``(severity, code, message)`` entries for a DSL text."""
    try:
        ast = parse_with_grammar_entry(src_text, "state_machine_dsl")
    except GrammarParseError as e:
        return [_grammar_error_diag(err) for err in (getattr(e, "errors", None) or [e])]

    try:
        machine = parse_dsl_node_to_state_machine(ast)
    except ModelValidationError as e:
        return [("error", d.code, d.message) for d in getattr(e, "diagnostics", [])]

    report = inspect_model(machine)
    out: list[tuple[str, str, str]] = []
    for d in report.diagnostics:
        if _is_external_suppressed(src_text, d):
            continue
        out.append((_severity(d), d.code, d.message))
    return out


def _print_entries(entries: Iterable[tuple[str, str, str]]) -> bool:
    has_error = False
    for sev, code, msg in entries:
        print(f"{sev.upper():7} {code:30s} {msg}")
        if sev == "error":
            has_error = True
    return has_error


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("usage: verify_pyfcstm_static.py <path.fcstm> [--strict]", file=sys.stderr)
        return 2
    strict = "--strict" in args
    paths = [arg for arg in args if arg != "--strict"]
    if len(paths) != 1:
        print("usage: verify_pyfcstm_static.py <path.fcstm> [--strict]", file=sys.stderr)
        return 2

    src = Path(paths[0]).read_text(encoding="utf-8")
    entries = analyze(src)
    has_error = _print_entries(entries)
    if strict and any(sev == "warning" for sev, _, _ in entries):
        has_error = True
    return 1 if has_error else 0


if __name__ == "__main__":
    raise SystemExit(main())
