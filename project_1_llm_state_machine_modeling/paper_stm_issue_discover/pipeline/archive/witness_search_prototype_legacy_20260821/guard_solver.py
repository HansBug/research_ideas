"""Deterministic SMT solver for the supported PlantUML condition fragment."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import z3

TOKEN_RE = re.compile(
    r"\s*(?:"
    r"(?P<number>-?(?:\d+(?:\.\d*)?|\.\d+))|"
    r"(?P<bool>true|false)\b|"
    r"(?P<ident>[A-Za-z_][A-Za-z0-9_]*)|"
    r"(?P<op>\&\&|\|\||\&|\||<=|>=|==|!=|=|<|>|!|\(|\))"
    r")",
    re.IGNORECASE,
)


class UnsupportedGuard(ValueError):
    """Raised when a condition lies outside the intentionally small fragment."""


@dataclass(frozen=True)
class Token:
    kind: str
    value: str


def _tokens(text: str) -> list[Token]:
    stripped = text.strip()
    if stripped.startswith("[") and stripped.endswith("]"):
        stripped = stripped[1:-1]
    result: list[Token] = []
    cursor = 0
    while cursor < len(stripped):
        match = TOKEN_RE.match(stripped, cursor)
        if match is None:
            raise UnsupportedGuard(
                f"unsupported token near {stripped[cursor : cursor + 24]!r}"
            )
        kind = next(
            name for name, value in match.groupdict().items() if value is not None
        )
        result.append(Token(kind, match.group(kind)))
        cursor = match.end()
    return result


class GuardParser:
    def __init__(self, symbols: dict[str, z3.ExprRef]) -> None:
        self.symbols = symbols
        self.tokens: list[Token] = []
        self.index = 0

    def parse(self, text: str) -> z3.BoolRef:
        self.tokens = _tokens(text)
        self.index = 0
        value = self._parse_or()
        if self.index != len(self.tokens):
            raise UnsupportedGuard(
                f"unexpected token {self.tokens[self.index].value!r}"
            )
        if not z3.is_bool(value):
            raise UnsupportedGuard("guard must evaluate to bool")
        return value

    def _peek(self, *values: str) -> bool:
        return (
            self.index < len(self.tokens)
            and self.tokens[self.index].value.lower() in values
        )

    def _take(self) -> Token:
        if self.index >= len(self.tokens):
            raise UnsupportedGuard("unexpected end of guard")
        token = self.tokens[self.index]
        self.index += 1
        return token

    def _parse_or(self) -> z3.ExprRef:
        left = self._parse_and()
        values = [left]
        while self._peek("||", "|"):
            self._take()
            values.append(self._parse_and())
        return z3.Or(*values) if len(values) > 1 else left

    def _parse_and(self) -> z3.ExprRef:
        left = self._parse_not()
        values = [left]
        while self._peek("&&", "&"):
            self._take()
            values.append(self._parse_not())
        return z3.And(*values) if len(values) > 1 else left

    def _parse_not(self) -> z3.ExprRef:
        if self._peek("!"):
            self._take()
            value = self._parse_not()
            if not z3.is_bool(value):
                raise UnsupportedGuard("! requires a boolean operand")
            return z3.Not(value)
        return self._parse_atom()

    def _parse_atom(self) -> z3.ExprRef:
        if self._peek("("):
            self._take()
            value = self._parse_or()
            if not self._peek(")"):
                raise UnsupportedGuard("missing closing parenthesis")
            self._take()
            return value
        token = self._take()
        if token.kind == "bool":
            return z3.BoolVal(token.value.lower() == "true")
        if token.kind != "ident":
            raise UnsupportedGuard(f"expected identifier, got {token.value!r}")
        name = token.value
        if self.index < len(self.tokens) and self.tokens[self.index].value in {
            "<",
            "<=",
            ">",
            ">=",
            "=",
            "==",
            "!=",
        }:
            operator = self._take().value
            right = self._take()
            if right.kind == "number":
                left_expr = self._symbol(name, "real")
                right_expr: z3.ExprRef = z3.RealVal(right.value)
            elif right.kind == "bool":
                left_expr = self._symbol(name, "bool")
                right_expr = z3.BoolVal(right.value.lower() == "true")
            elif right.kind == "ident":
                left_expr = self._symbol(name, "real")
                right_expr = self._symbol(right.value, "real")
            else:
                raise UnsupportedGuard(f"unsupported comparison value {right.value!r}")
            return self._compare(left_expr, operator, right_expr)
        return self._symbol(name, "bool")

    def _symbol(self, name: str, kind: str) -> z3.ExprRef:
        value = self.symbols.get(name)
        if value is None:
            value = z3.Bool(name) if kind == "bool" else z3.Real(name)
            self.symbols[name] = value
        if kind == "bool" and not z3.is_bool(value):
            raise UnsupportedGuard(f"{name} is used as both boolean and numeric")
        if kind == "real" and not z3.is_arith(value):
            raise UnsupportedGuard(f"{name} is used as both numeric and boolean")
        return value

    @staticmethod
    def _compare(left: z3.ExprRef, operator: str, right: z3.ExprRef) -> z3.BoolRef:
        if operator in {"=", "=="}:
            return left == right
        if operator == "!=":
            return left != right
        if operator == "<":
            return left < right
        if operator == "<=":
            return left <= right
        if operator == ">":
            return left > right
        if operator == ">=":
            return left >= right
        raise UnsupportedGuard(f"unsupported comparison operator {operator!r}")


def pairwise_overlaps(
    conditions: list[str], *, timeout_ms: int = 3_000
) -> dict[str, Any]:
    """Return exact overlap witnesses for the supported condition fragment."""

    symbols: dict[str, z3.ExprRef] = {}
    parser = GuardParser(symbols)
    formulas = [parser.parse(condition) for condition in conditions]
    pairs = []
    for left_index, left in enumerate(formulas):
        for right_index in range(left_index + 1, len(formulas)):
            solver = z3.Solver()
            solver.set(timeout=timeout_ms)
            solver.add(left, formulas[right_index])
            status = solver.check()
            witness = None
            if status == z3.sat:
                model = solver.model()
                witness = {
                    name: str(model.eval(symbol, model_completion=True))
                    for name, symbol in sorted(symbols.items())
                }
            pairs.append(
                {
                    "left_index": left_index,
                    "right_index": right_index,
                    "status": str(status),
                    "witness": witness,
                }
            )
    return {
        "conditions": conditions,
        "pairs": pairs,
        "overlap_found": any(item["status"] == "sat" for item in pairs),
        "all_terminal": all(item["status"] in {"sat", "unsat"} for item in pairs),
        "symbol_sorts": {
            name: str(symbol.sort()) for name, symbol in sorted(symbols.items())
        },
        "semantics": "quantifier_free_boolean_linear_real_fragment",
    }


__all__ = ["UnsupportedGuard", "pairwise_overlaps"]
