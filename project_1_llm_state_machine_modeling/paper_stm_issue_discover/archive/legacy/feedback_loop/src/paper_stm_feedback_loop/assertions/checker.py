"""Checker for prefix-plus-terminal-assert LLM assertion scripts.

Ported pure evaluation ideas from legacy agent_loop eval_env at source commit
c8c1ccba.  This checker is self-contained and never imports
``paper_stm_repair_loop``.
"""

from __future__ import annotations

import ast
import copy
import signal
import threading
import traceback
from dataclasses import dataclass
from typing import Any

from .parser import AssertionScriptSyntaxError, ParsedAssertionScript, parse_assertion_script
from .provenance import FORBIDDEN_NAMES, FORBIDDEN_NODES, AuditIssue, AuditReport, audit_expression
from .runtime import ALLOWED_FUNCTION_FAMILIES, EvalEnvironment
from .sealed import SealedAssertionResult
from .views import FrozenView, stable_hash

PORTED_SOURCE_COMMIT = "c8c1ccba"


@dataclass(frozen=True)
class AssertionCheckResult:
    """Full script-check result with sealed/public outcome and trace."""

    sealed: SealedAssertionResult
    parsed: ParsedAssertionScript | None
    audit: dict[str, Any] | None
    function_call_trace: tuple[Any, ...] = ()
    actual_function_families: tuple[str, ...] = ()
    required_function_families: tuple[str, ...] = ()
    namespace_hash_before: str | None = None
    namespace_hash_after: str | None = None

    @property
    def outcome(self) -> str:
        return self.sealed.outcome

    @property
    def value(self) -> bool | None:
        return self.sealed.value

    @property
    def sealed_metadata(self) -> dict[str, Any]:
        """Metadata of the sealed result, or an empty dict when there is none.

        Callers need `verdict_basis` to tell a verdict read off the declaration
        table from one produced by a query, because the two must not be judged
        by the same downstream rules -- a bounded-causality check has no query
        to inspect when nothing was queried.
        """

        return dict(self.sealed.metadata or {})

    def to_json(self) -> dict[str, Any]:
        return {
            **self.sealed.to_json(),
            "parsed": self.parsed.to_json() if self.parsed else None,
            "audit": self.audit,
            "function_call_trace": [
                call.to_json() if hasattr(call, "to_json") else copy.deepcopy(call)
                for call in self.function_call_trace
            ],
            "actual_function_families": list(self.actual_function_families),
            "required_function_families": list(self.required_function_families),
            "namespace_hash_before": self.namespace_hash_before,
            "namespace_hash_after": self.namespace_hash_after,
            "ported_source_commit": PORTED_SOURCE_COMMIT,
        }


class AssertionChecker:
    """Evaluate LLM assertion scripts against a fresh sealed namespace.

    Parameters mirror :class:`EvalEnvironment`: either pass an existing
    self-contained environment or model/inspect artifacts for a new one.

    Execution contract: parse prefix statements plus one terminal ``assert``;
    statically reject unregistered dependencies; execute prefix in a fresh local
    namespace; evaluate the terminal assert expression as an expression; require
    a strict bool. Helper/backend exceptions, prefix ``AssertionError`` and
    terminal exceptions are invalid. Only strict terminal ``False`` produces
    ``sealed_false``.
    """

    def __init__(self, environment: EvalEnvironment | None = None, **environment_kwargs: Any) -> None:
        self.environment = environment or EvalEnvironment(**environment_kwargs)

    def check(
        self,
        script: str,
        reason: str = "",
        *,
        required_function_families: list[str] | tuple[str, ...] | None = None,
    ) -> AssertionCheckResult:
        required = tuple(required_function_families or ())
        invalid_required = [family for family in required if family not in ALLOWED_FUNCTION_FAMILIES]
        if invalid_required:
            return self._invalid(
                None,
                reason,
                "InvalidFunctionFamily",
                "required_function_families must use structure/relation/effect/simulation/formal/mapping",
                metadata={"invalid": invalid_required},
                required=required,
            )
        try:
            parsed = parse_assertion_script(script)
        except AssertionScriptSyntaxError as exc:
            return self._invalid(None, reason, type(exc).__name__, str(exc), required=required)

        local_names = _assigned_names(parsed.prefix_ast)
        prefix_audit = _audit_prefix_ast(parsed.prefix_ast, allowed_names=self.environment.allowed_names | local_names)
        terminal_audit = audit_expression(
            parsed.terminal_expression,
            allowed_names=self.environment.allowed_names | local_names,
            registered_objects=self.environment.registered_objects,
            registered_view_attrs=self.environment.registered_view_attrs,
        )
        audit = _merge_audits(prefix_audit, terminal_audit)
        if not audit.ok:
            return self._invalid(
                parsed,
                reason,
                "AuditRejected",
                "assertion script uses unregistered dependencies",
                audit=audit.to_json(),
                metadata={"issues": [issue.__dict__ for issue in audit.issues]},
                required=required,
            )

        self.environment.call_trace = []
        locals_map = dict(self.environment.locals)
        globals_map = {
            "__builtins__": self.environment.globals["__builtins__"],
            **{key: value for key, value in self.environment.globals.items() if key != "__builtins__"},
        }
        before = stable_hash(_namespace_snapshot(locals_map, self.environment._raw_functions))
        try:
            self._exec_prefix(parsed, globals_map, locals_map)
            value = self._eval_terminal(parsed, globals_map, locals_map)
        except Exception as exc:  # includes AssertionError by contract
            after = stable_hash(_namespace_snapshot(locals_map, self.environment._raw_functions))
            return self._invalid(
                parsed,
                reason,
                type(exc).__name__,
                str(exc),
                audit=audit.to_json(),
                metadata={"traceback": traceback.format_exc(limit=3)},
                before=before,
                after=after,
                required=required,
            )
        after = stable_hash(_namespace_snapshot(locals_map, self.environment._raw_functions))
        actual = tuple(sorted({record.family for record in self.environment.call_trace if record.status == "completed"}))
        missing = tuple(family for family in required if family not in actual)
        if not isinstance(value, bool):
            return self._invalid(
                parsed,
                reason,
                "NonBoolTerminalAssert",
                f"terminal assert expression must evaluate to strict bool, got {type(value).__name__}",
                audit=audit.to_json(),
                before=before,
                after=after,
                required=required,
                actual=actual,
            )
        if missing:
            return self._invalid(
                parsed,
                reason,
                "RequiredFamilyMissing",
                "required evidence family was not observed",
                audit=audit.to_json(),
                metadata={"missing": list(missing)},
                before=before,
                after=after,
                required=required,
                actual=actual,
            )
        outcome = "valid" if value is True else "sealed_false"
        sealed = SealedAssertionResult(
            outcome=outcome,
            value=value,
            terminal_expression=parsed.terminal_expression,
            reason=str(reason),
            metadata={
                "ported_source_commit": PORTED_SOURCE_COMMIT,
                "failure_message": parsed.failure_message,
            },
        )
        return AssertionCheckResult(
            sealed=sealed,
            parsed=parsed,
            audit=audit.to_json(),
            function_call_trace=tuple(self.environment.call_trace),
            actual_function_families=actual,
            required_function_families=required,
            namespace_hash_before=before,
            namespace_hash_after=after,
        )

    def _exec_prefix(self, parsed: ParsedAssertionScript, globals_map: dict[str, Any], locals_map: dict[str, Any]) -> None:
        if not parsed.prefix_ast.body:
            return
        code = compile(parsed.prefix_ast, "<assertion-prefix>", "exec")
        if not self.environment.timeout_seconds or threading.current_thread() is not threading.main_thread():
            exec(code, globals_map, locals_map)
            return

        def handler(_signum: int, _frame: Any) -> None:
            raise TimeoutError("assertion prefix timed out")

        previous = signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(self.environment.timeout_seconds))
        try:
            exec(code, globals_map, locals_map)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)

    def _eval_terminal(self, parsed: ParsedAssertionScript, globals_map: dict[str, Any], locals_map: dict[str, Any]) -> Any:
        code = compile(parsed.terminal_ast, "<terminal-assert-expression>", "eval")
        if not self.environment.timeout_seconds or threading.current_thread() is not threading.main_thread():
            return eval(code, globals_map, locals_map)

        def handler(_signum: int, _frame: Any) -> None:
            raise TimeoutError("terminal assert expression timed out")

        previous = signal.signal(signal.SIGALRM, handler)
        signal.alarm(int(self.environment.timeout_seconds))
        try:
            return eval(code, globals_map, locals_map)
        finally:
            signal.alarm(0)
            signal.signal(signal.SIGALRM, previous)

    def _invalid(
        self,
        parsed: ParsedAssertionScript | None,
        reason: str,
        error_type: str,
        message: str,
        *,
        audit: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        before: str | None = None,
        after: str | None = None,
        required: tuple[str, ...] = (),
        actual: tuple[str, ...] = (),
    ) -> AssertionCheckResult:
        sealed = SealedAssertionResult(
            outcome="invalid",
            value=None,
            terminal_expression=parsed.terminal_expression if parsed else None,
            reason=str(reason),
            error={"type": error_type, "message": message},
            metadata={"ported_source_commit": PORTED_SOURCE_COMMIT, **(metadata or {})},
        )
        return AssertionCheckResult(
            sealed=sealed,
            parsed=parsed,
            audit=audit,
            function_call_trace=tuple(self.environment.call_trace),
            actual_function_families=actual,
            required_function_families=required,
            namespace_hash_before=before,
            namespace_hash_after=after,
        )


def _assigned_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.add(node.name)
    return names


def _audit_prefix_ast(tree: ast.AST, *, allowed_names: set[str]) -> AuditReport:
    issues: list[AuditIssue] = []
    names: set[str] = set()
    calls: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            issues.append(AuditIssue("prefix_assert_forbidden", "only terminal assert is allowed"))
        if isinstance(node, FORBIDDEN_NODES):
            issues.append(AuditIssue("forbidden_ast_node", type(node).__name__))
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            issues.append(AuditIssue("dunder_attribute", node.attr))
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            names.add(node.id)
            if node.id in FORBIDDEN_NAMES:
                issues.append(AuditIssue("forbidden_name", node.id))
            elif node.id not in allowed_names:
                issues.append(AuditIssue("unknown_name", node.id))
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                calls.append(func.id)
                if func.id in FORBIDDEN_NAMES:
                    issues.append(AuditIssue("forbidden_call", func.id))
                elif func.id not in allowed_names:
                    issues.append(AuditIssue("unknown_call", func.id))
            elif isinstance(func, ast.Attribute):
                calls.append(func.attr)
                if func.attr.startswith("__"):
                    issues.append(AuditIssue("dunder_call", func.attr))
    return AuditReport(
        ok=not issues,
        expression_sha256=stable_hash(ast.dump(tree)),
        names=tuple(sorted(names)),
        function_calls=tuple(calls),
        issues=tuple(issues),
    )


def _merge_audits(left: AuditReport, right: AuditReport) -> AuditReport:
    return AuditReport(
        ok=left.ok and right.ok,
        expression_sha256=stable_hash({"prefix": left.expression_sha256, "terminal": right.expression_sha256}),
        names=tuple(sorted(set(left.names) | set(right.names))),
        function_calls=tuple(left.function_calls + right.function_calls),
        issues=tuple(left.issues + right.issues),
    )


def _namespace_snapshot(namespace: dict[str, Any], raw_functions: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in namespace.items():
        if key in raw_functions:
            continue
        if key.startswith("__"):
            continue
        if isinstance(value, FrozenView):
            out[key] = value.to_json()
        elif value is None or isinstance(value, (str, int, float, bool)):
            out[key] = value
        elif isinstance(value, (list, tuple, set, dict)):
            out[key] = repr(value)
        else:
            out[key] = repr(value)
    return out


def check_assertion_script(
    script: str,
    environment: EvalEnvironment | None = None,
    reason: str = "",
    *,
    required_function_families: list[str] | tuple[str, ...] | None = None,
    **environment_kwargs: Any,
) -> AssertionCheckResult:
    """Convenience wrapper for checking one assertion script."""

    checker = AssertionChecker(environment, **environment_kwargs)
    return checker.check(
        script,
        reason=reason,
        required_function_families=required_function_families,
    )


__all__ = [
    "AssertionCheckResult",
    "AssertionChecker",
    "PORTED_SOURCE_COMMIT",
    "check_assertion_script",
]
