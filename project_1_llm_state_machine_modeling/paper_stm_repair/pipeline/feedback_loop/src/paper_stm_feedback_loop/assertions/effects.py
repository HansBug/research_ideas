from __future__ import annotations

import ast
import re
from collections.abc import Iterable
from .exceptions import UnsupportedEvidence
from .structure import StructureAPI


_ASSIGNMENT_RE = re.compile(r"(?P<var>[A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?P<expr>[^;]+)")


class EffectAPI:
    """Deterministic effect-query facade for direct eval assertions.

    Parameters: ``structure`` is the frozen ``StructureAPI`` bound to the current
    model inspect.

    Returns: ``effect_deltas`` returns a stable tuple of ``(variable, delta)``
    pairs for all parseable numeric assignments on matching transitions, and an
    empty tuple when no matching transition/effect/assignment exists. When
    ``variable`` is supplied, only assignments to that exact declaration name
    are considered; absence remains an empty tuple rather than an invented
    variable probe.
    ``effect_delta`` remains the variable-specific compatibility helper: it
    returns one numeric delta, ``None`` when the selected transition has no
    assignment for that variable, and raises ``UnsupportedEvidence`` when the
    relevant transition/effect is ambiguous or not parseable.

    Execution: reuses pyfcstm structured transition inspect ``effect`` strings
    and ``variables`` initial values.  It does not parse exception text, execute
    arbitrary code, call an LLM, mutate variables, or infer hidden semantics.

    Failure semantics: no matching transition/effect yields ``()`` from
    ``effect_deltas`` and ``None`` from ``effect_delta`` for stable absence.
    ``effect_delta`` still requires exactly one matching transition; unsupported
    effect expressions raise ``UnsupportedEvidence`` so the assertion becomes
    ``unsupported`` rather than guessed.

    Evidence limitations: only simple assignments such as ``x = x - 1`` or
    ``x = 1`` with numeric variable initial values are interpreted.  Complex
    expressions, side effects outside structured inspect, and temporal semantics
    remain unsupported.

    Permissions: read-only in-memory inspect access; no paths, shell, imports,
    environment, network, mutation, or reference/gold data.

    Example: ``any(delta < 0 for _, delta in effect_deltas(source="Root.A",
    event="Root.done", target="Root.B"))`` returns ``False`` for missing
    variables/effects and ``True`` for ``count = count - 1`` without inventing a
    variable-name probe.  The legacy ``(effect_delta(..., variable="count") or
    0) < 0`` form remains supported.
    """

    family = "effect"

    def __init__(
        self,
        structure: StructureAPI,
        *,
        excluded_variables: Iterable[str] = (),
    ) -> None:
        self.structure = structure
        self.excluded_variables = frozenset(excluded_variables)

    def effect_deltas(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        variable: str | None = None,
    ) -> tuple[tuple[str, int | float], ...]:
        """Return parseable assignment deltas for matching transitions.

        Absence is represented by an empty tuple, not by a sentinel variable or
        invented probe.  This makes expressions such as ``any(delta < 0 for _,
        delta in effect_deltas(...))`` deterministically ``False`` when the
        model has no variables, no matching effects, or no assignments. Supplying
        ``variable=`` keeps the query tied to the named declaration instead of
        treating a different variable's effect as a match.
        """

        deltas: list[tuple[str, int | float]] = []
        for transition in self.structure.transitions(
            source=source, event=event, target=target
        ):
            effect = str(transition.effect or "")
            if not effect:
                continue
            for variable_name, expr in _assignments(effect):
                if variable_name in self.excluded_variables:
                    continue
                if variable is not None and variable_name != variable:
                    continue
                before = self._initial_value(variable_name)
                after = self._eval_simple_expr(
                    expr, variable=variable_name, before=before
                )
                deltas.append((variable_name, after - before))
        return tuple(deltas)

    def effect_delta(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        variable: str,
    ) -> int | float | None:
        transitions = self.structure.transitions(source=source, event=event, target=target)
        if not transitions:
            return None
        if len(transitions) > 1:
            raise UnsupportedEvidence("effect_delta requires exactly one matching transition")
        effect = transitions[0].effect
        if not effect:
            return None
        if variable in self.excluded_variables:
            return None
        assignments = _assignments(str(effect))
        matches = [expr for var, expr in assignments if var == variable]
        if not matches:
            return None
        if len(matches) > 1:
            raise UnsupportedEvidence(f"multiple assignments for {variable}")
        before = self._initial_value(variable)
        after = self._eval_simple_expr(matches[0], variable=variable, before=before)
        return after - before

    def effects(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        variable: str | None = None,
    ):
        """Return transitions carrying an effect, optionally assigning a variable."""

        matches = []
        for transition in self.structure.transitions(
            source=source, event=event, target=target
        ):
            effect = str(transition.effect or "")
            if not effect:
                continue
            assignments = [
                assigned
                for assigned, _expr in _assignments(effect)
                if assigned not in self.excluded_variables
            ]
            if not assignments:
                continue
            if variable is not None and variable not in assignments:
                continue
            matches.append(transition)
        return tuple(matches)

    def effect_assigns(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        variable: str,
    ) -> bool:
        transitions = self.structure.transitions(source=source, event=event, target=target)
        if len(transitions) > 1:
            raise UnsupportedEvidence("effect_assigns requires an unambiguous transition")
        if not transitions:
            return False
        if variable in self.excluded_variables:
            return False
        return any(
            var == variable
            for var, _expr in _assignments(str(transitions[0].effect or ""))
        )

    def _initial_value(self, variable: str) -> int | float:
        matches = self.structure.variables(name=variable)
        if len(matches) != 1:
            raise UnsupportedEvidence(f"variable {variable!r} is missing or ambiguous")
        raw = matches[0].init_value
        try:
            if isinstance(raw, str) and "." in raw:
                return float(raw)
            return int(raw)
        except Exception as exc:
            raise UnsupportedEvidence(f"non-numeric initial value for {variable!r}") from exc

    def _eval_simple_expr(self, expr: str, *, variable: str, before: int | float) -> int | float:
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError as exc:
            raise UnsupportedEvidence(f"unsupported effect expression: {expr}") from exc

        def walk(node: ast.AST) -> int | float:
            if isinstance(node, ast.Expression):
                return walk(node.body)
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node, ast.Name) and node.id == variable:
                return before
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                return -walk(node.operand)
            if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub)):
                left = walk(node.left)
                right = walk(node.right)
                return left + right if isinstance(node.op, ast.Add) else left - right
            raise UnsupportedEvidence(f"unsupported effect expression: {expr}")

        return walk(tree)



def _assignments(effect: str) -> list[tuple[str, str]]:
    return [
        (match.group("var"), match.group("expr").strip())
        for match in _ASSIGNMENT_RE.finditer(effect)
    ]


__all__ = ["EffectAPI"]
