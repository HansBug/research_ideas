from __future__ import annotations

import ast
import builtins
from dataclasses import dataclass, field
from typing import Any

from .views import FrozenView


SAFE_BUILTINS: dict[str, Any] = {
    "abs": builtins.abs,
    "all": builtins.all,
    "any": builtins.any,
    "bool": builtins.bool,
    "float": builtins.float,
    "int": builtins.int,
    "iter": builtins.iter,
    "len": builtins.len,
    "list": builtins.list,
    "max": builtins.max,
    "min": builtins.min,
    "round": builtins.round,
    "set": builtins.set,
    "sorted": builtins.sorted,
    "str": builtins.str,
    "sum": builtins.sum,
    "tuple": builtins.tuple,
}

FORBIDDEN_NAMES = {
    "__builtins__",
    "__import__",
    "compile",
    "eval",
    "exec",
    "globals",
    "locals",
    "open",
    "input",
    "help",
    "dir",
    "vars",
    "getattr",
    "setattr",
    "delattr",
    "os",
    "sys",
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "pathlib",
    "time",
    "datetime",
    "random",
    "secrets",
    "env",
    "environ",
}

FORBIDDEN_NODES = (
    ast.AsyncFunctionDef,
    ast.Await,
    ast.ClassDef,
    ast.Delete,
    ast.FunctionDef,
    ast.Global,
    ast.Import,
    ast.ImportFrom,
    ast.Nonlocal,
    ast.Try,
    ast.While,
    ast.With,
    ast.Yield,
    ast.YieldFrom,
)


@dataclass(frozen=True)
class AuditIssue:
    code: str
    detail: str


@dataclass(frozen=True)
class AuditReport:
    ok: bool
    expression_sha256: str
    names: tuple[str, ...]
    function_calls: tuple[str, ...]
    issues: tuple[AuditIssue, ...] = field(default_factory=tuple)

    def to_json(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "expression_sha256": self.expression_sha256,
            "names": list(self.names),
            "function_calls": list(self.function_calls),
            "issues": [issue.__dict__ for issue in self.issues],
        }


def _sha256_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def audit_expression(
    expression: str,
    *,
    allowed_names: set[str],
    registered_objects: dict[str, Any] | None = None,
    registered_view_attrs: set[str] | None = None,
) -> AuditReport:
    """Audit a Python bool expression before direct eval.

    Parameters: ``expression`` is the exact Agent-authored positive Python
    expression; ``allowed_names`` is the closed eval namespace; ``registered_objects``
    maps known view variable names to frozen observations; ``registered_view_attrs``
    permits attributes returned by registered function views such as
    ``simulate(...).final.is_active(...)``.

    Returns: ``AuditReport`` with expression hash, observed names, function call
    names, and structured issues.  ``ok`` is true only when all names and
    attributes are registered.

    Execution: parses the expression with Python ``ast`` and rejects imports,
    definitions, lambdas, dunder attributes, forbidden dependency names, unknown
    names, calls to non-registered functions, and unregistered fields/methods on
    known ``FrozenView`` objects. Comprehension target names are recognized as
    expression-local bindings; they do not become global eval variables. It does
    not execute the expression or convert it into a JSON predicate DSL.

    Failure semantics: syntax errors, unknown names, forbidden names/nodes,
    dunder attrs, and unregistered view fields/methods are reported as issues so
    the caller can return ``untracked_dependency``.  Unsupported domain APIs must
    be reported by the registered function at execution time via
    ``UnsupportedEvidence``.

    Evidence limitations: static AST audit is a provenance gate, not a Python
    security sandbox.  It verifies registered dependencies before trusted local
    academic eval; it does not claim isolation against malicious code.

    Permissions: read-only AST inspection; no eval, import, filesystem,
    environment, time/random, shell, network, mutation, or hidden gold access.

    Example: ``audit_expression("any(check(x) for x in values)",
    allowed_names={"any", "check", "values"})`` accepts local ``x``; ``open``
    and ``view.__class__`` fail.
    """

    issues: list[AuditIssue] = []
    names: set[str] = set()
    calls: list[str] = []
    registered_objects = registered_objects or {}
    registered_view_attrs = registered_view_attrs or set()
    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        return AuditReport(
            ok=False,
            expression_sha256=_sha256_text(expression),
            names=(),
            function_calls=(),
            issues=(AuditIssue("syntax_error", str(exc)),),
        )

    local_bindings: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.comprehension):
            targets = (
                node.target.elts
                if isinstance(node.target, (ast.Tuple, ast.List))
                else [node.target]
            )
            local_bindings.update(
                target.id for target in targets if isinstance(target, ast.Name)
            )
        elif isinstance(node, ast.Lambda):
            local_bindings.update(arg.arg for arg in node.args.args)
            local_bindings.update(arg.arg for arg in node.args.posonlyargs)
            local_bindings.update(arg.arg for arg in node.args.kwonlyargs)
            if node.args.vararg is not None:
                local_bindings.add(node.args.vararg.arg)
            if node.args.kwarg is not None:
                local_bindings.add(node.args.kwarg.arg)

    for node in ast.walk(tree):
        if isinstance(node, FORBIDDEN_NODES):
            issues.append(AuditIssue("forbidden_ast_node", type(node).__name__))
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
            names.add(node.id)
            if node.id in FORBIDDEN_NAMES:
                issues.append(AuditIssue("forbidden_name", node.id))
            elif node.id not in allowed_names and node.id not in local_bindings:
                issues.append(AuditIssue("unknown_name", node.id))
        if isinstance(node, ast.Attribute):
            if node.attr.startswith("__"):
                issues.append(AuditIssue("dunder_attribute", node.attr))
            base = node.value
            if isinstance(base, ast.Name):
                obj = registered_objects.get(base.id)
                if isinstance(obj, FrozenView):
                    if node.attr not in obj.allowed_fields and node.attr not in obj.allowed_methods:
                        issues.append(AuditIssue("unregistered_object_attribute", f"{base.id}.{node.attr}"))
            elif node.attr not in registered_view_attrs and not node.attr.startswith("__"):
                # Attribute chains from registered function results are allowed
                # only through the shared view registry.
                issues.append(AuditIssue("unregistered_dynamic_attribute", node.attr))
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
                base = func.value
                if isinstance(base, ast.Name):
                    obj = registered_objects.get(base.id)
                    if isinstance(obj, FrozenView) and func.attr not in obj.allowed_methods:
                        issues.append(AuditIssue("unregistered_object_method", f"{base.id}.{func.attr}"))
                elif func.attr not in registered_view_attrs:
                    issues.append(AuditIssue("unregistered_dynamic_method", func.attr))

    return AuditReport(
        ok=not issues,
        expression_sha256=_sha256_text(expression),
        names=tuple(sorted(names)),
        function_calls=tuple(calls),
        issues=tuple(issues),
    )


__all__ = ["AuditIssue", "AuditReport", "FORBIDDEN_NAMES", "SAFE_BUILTINS", "audit_expression"]
