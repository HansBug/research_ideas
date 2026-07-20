from __future__ import annotations

import ast
import re
from typing import Any, Iterable

ERROR_SYNTAX_INVALID = "ASSERT_SYNTAX_INVALID"
ERROR_SIMULATE_FIRST_CYCLE_REQUIRED = "ASSERT_SIMULATE_FIRST_CYCLE_REQUIRED"
ERROR_EFFECT_DELTA_DIRECTION_REQUIRED = "ASSERT_EFFECT_DELTA_DIRECTION_REQUIRED"
ERROR_EFFECTS_BOOL_SUBSTITUTE = "ASSERT_EFFECTS_BOOL_SUBSTITUTE"
ERROR_CONTINUITY_EVIDENCE_REQUIRED = "ASSERT_CONTINUITY_EVIDENCE_REQUIRED"
ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK = (
    "ASSERT_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK"
)
ERROR_CARDINALITY_COMPARISON_REQUIRED = "ASSERT_CARDINALITY_COMPARISON_REQUIRED"
ERROR_TRANSITION_TARGET_REQUIRED = "ASSERT_TRANSITION_TARGET_REQUIRED"
ERROR_CONDITION_TRIGGER_REQUIRED = "ASSERT_CONDITION_TRIGGER_REQUIRED"

_STRUCTURE_FUNCTIONS = frozenset(
    {"states", "events", "variables", "transitions", "bound_model_refs"}
)
_DECREASE_RE = re.compile(r"\b(?:decrease|decreases|decreased|decrement|decrements|decremented)\b|(?:减少|递减)", re.I)
_INCREASE_RE = re.compile(r"\b(?:increase|increases|increased|increment|increments|incremented)\b|(?:增加|递增)", re.I)
_AT_LEAST_RE = re.compile(r"\b(?:at\s+least|no\s+fewer\s+than|not\s+less\s+than)\b|(?:至少|不少于)", re.I)
_AT_MOST_RE = re.compile(r"\b(?:at\s+most|no\s+more\s+than|not\s+more\s+than)\b|(?:至多|不多于)", re.I)
_EXACTLY_RE = re.compile(r"\b(?:exactly|equal(?:s)?\s+to)\b|(?:恰好|正好)", re.I)
_NUMBER_WORDS = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "零": 0,
    "一": 1,
    "二": 2,
    "两": 2,
    "三": 3,
    "四": 4,
    "五": 5,
    "六": 6,
    "七": 7,
    "八": 8,
    "九": 9,
    "十": 10,
}


def validate_assertion_semantic_policy(
    assertion_expression: str, coverage_requirements: Iterable[dict[str, Any]]
) -> list[str]:
    """Return stable semantic-policy error codes for one assertion expression.

    This checker is intentionally read-only and AST-only: it never evaluates the
    assertion and never imports the runtime eval environment.
    """

    try:
        tree = ast.parse(assertion_expression, mode="eval")
    except SyntaxError:
        return [ERROR_SYNTAX_INVALID]

    errors: list[str] = []
    calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call)]
    simulate_calls = [call for call in calls if _call_name(call) == "simulate"]

    for call in simulate_calls:
        if not _simulate_has_empty_first_cycle(call):
            _add_error(errors, ERROR_SIMULATE_FIRST_CYCLE_REQUIRED)

    requirements = list(coverage_requirements)
    for requirement in requirements:
        dimension = str(requirement.get("dimension", ""))
        cue = str(requirement.get("cue_text", ""))
        requirement_id = str(requirement.get("requirement_id", ""))

        if dimension == "effect":
            direction = _effect_direction(cue)
            if direction:
                if _uses_bool_effects_substitute(tree):
                    _add_error(errors, _format_error(ERROR_EFFECTS_BOOL_SUBSTITUTE, requirement_id))
                if not _has_effect_delta_zero_compare(tree, direction):
                    _add_error(
                        errors,
                        _format_error(ERROR_EFFECT_DELTA_DIRECTION_REQUIRED, requirement_id),
                    )

        if dimension == "continuity":
            formal_kinds = _fbmcq_property_kinds(calls)
            existential_too_weak = "exists_always" in formal_kinds
            if existential_too_weak:
                _add_error(
                    errors,
                    _format_error(
                        ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK,
                        requirement_id,
                    ),
                )
            if not existential_too_weak and not _has_continuity_evidence(
                formal_kinds=formal_kinds,
                calls=calls,
                simulate_calls=simulate_calls,
            ):
                _add_error(
                    errors,
                    _format_error(ERROR_CONTINUITY_EVIDENCE_REQUIRED, requirement_id),
                )

        if dimension == "cardinality":
            target = _parse_cardinality_target(cue)
            if target is not None and not _has_cardinality_compare(tree, cue, target):
                _add_error(
                    errors,
                    _format_error(ERROR_CARDINALITY_COMPARISON_REQUIRED, requirement_id),
                )

        if dimension == "transition" and not _has_transition_target_evidence(
            tree, calls, simulate_calls
        ):
            _add_error(
                errors,
                _format_error(ERROR_TRANSITION_TARGET_REQUIRED, requirement_id),
            )

        if dimension == "condition" and not _has_condition_trigger_evidence(
            tree, calls, simulate_calls
        ):
            _add_error(
                errors,
                _format_error(ERROR_CONDITION_TRIGGER_REQUIRED, requirement_id),
            )

    return errors


def _format_error(code: str, requirement_id: str) -> str:
    return f"{code}:{requirement_id}" if requirement_id else code


def _add_error(errors: list[str], error: str) -> None:
    if error not in errors:
        errors.append(error)


def _call_name(call: ast.Call) -> str | None:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    return None


def _simulate_has_empty_first_cycle(call: ast.Call) -> bool:
    cycles: ast.AST | None = None
    for keyword in call.keywords:
        if keyword.arg == "cycles":
            cycles = keyword.value
            break
    if cycles is None and call.args:
        cycles = call.args[0]
    if cycles is None:
        return False
    if not isinstance(cycles, (ast.List, ast.Tuple)):
        return False
    if not cycles.elts:
        return False
    first = cycles.elts[0]
    return isinstance(first, (ast.List, ast.Tuple)) and not first.elts


def _effect_direction(cue: str) -> str | None:
    if _DECREASE_RE.search(cue):
        return "decrease"
    if _INCREASE_RE.search(cue):
        return "increase"
    return None


def _uses_bool_effects_substitute(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _call_name(node) == "bool":
            if node.args and _contains_call(node.args[0], "effects"):
                return True
        if isinstance(node, ast.Call) and _call_name(node) == "effects":
            parent_context = _node_parent_context(tree, node)
            if parent_context in {"compare", "boolop", "unary_not"}:
                return True
    return False


def _node_parent_context(tree: ast.AST, target: ast.AST) -> str | None:
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            if child is not target:
                continue
            if isinstance(parent, ast.Compare):
                return "compare"
            if isinstance(parent, ast.BoolOp):
                return "boolop"
            if isinstance(parent, ast.UnaryOp) and isinstance(parent.op, ast.Not):
                return "unary_not"
            return None
    return None


def _has_effect_delta_zero_compare(tree: ast.AST, direction: str) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        left = node.left
        for op, right in zip(node.ops, node.comparators):
            left_effect = _contains_call(left, "effect_delta")
            right_effect = _contains_call(right, "effect_delta")
            left_zero = _is_numeric_literal(left, 0)
            right_zero = _is_numeric_literal(right, 0)
            if left_effect and right_zero and _operator_matches_direction(op, direction):
                return True
            if left_zero and right_effect and _operator_matches_direction(_reverse_op(op), direction):
                return True
            left = right
    return False


def _operator_matches_direction(op: ast.cmpop, direction: str) -> bool:
    if direction == "decrease":
        return isinstance(op, ast.Lt)
    return isinstance(op, ast.Gt)


def _reverse_op(op: ast.cmpop) -> ast.cmpop:
    if isinstance(op, ast.Lt):
        return ast.Gt()
    if isinstance(op, ast.LtE):
        return ast.GtE()
    if isinstance(op, ast.Gt):
        return ast.Lt()
    if isinstance(op, ast.GtE):
        return ast.LtE()
    return op


def _fbmcq_property_kinds(calls: list[ast.Call]) -> set[str]:
    kinds: set[str] = set()
    for call in calls:
        if _call_name(call) != "fbmcq" or not call.args:
            continue
        query = call.args[0]
        if not isinstance(query, ast.Constant) or not isinstance(query.value, str):
            continue
        match = re.search(
            r"\bcheck\s+(reach|forbid|invariant|must_reach|exists_always|response|cover)\b",
            query.value,
            re.IGNORECASE,
        )
        if match:
            kinds.add(match.group(1).lower())
    return kinds


def _has_continuity_evidence(
    *, formal_kinds: set[str], calls: list[ast.Call], simulate_calls: list[ast.Call]
) -> bool:
    if sum(
        1
        for call in calls
        if _call_name(call) == "fbmcq"
    ) >= 2 and formal_kinds == {"response"}:
        return True
    serialized = {ast.dump(call, include_attributes=False) for call in simulate_calls}
    return (
        len(serialized) >= 2
        and all(_simulate_has_progress_after_initialization(call) for call in simulate_calls)
    )


def _simulate_has_progress_after_initialization(call: ast.Call) -> bool:
    cycles: ast.AST | None = None
    for keyword in call.keywords:
        if keyword.arg == "cycles":
            cycles = keyword.value
            break
    if cycles is None and call.args:
        cycles = call.args[0]
    return isinstance(cycles, (ast.List, ast.Tuple)) and len(cycles.elts) >= 2


def _has_transition_target_evidence(
    tree: ast.AST, calls: list[ast.Call], simulate_calls: list[ast.Call]
) -> bool:
    if any(
        _call_name(call) in {"transition_exists", "transitions"}
        and _call_has_nonempty_string_keyword(call, "source")
        and _call_has_nonempty_string_keyword(call, "target")
        for call in calls
    ):
        return True
    if simulate_calls and any(
        isinstance(node, ast.Call)
        and _call_name(node) == "is_active"
        and bool(node.args)
        and isinstance(node.args[0], ast.Constant)
        and isinstance(node.args[0].value, str)
        for node in ast.walk(tree)
    ):
        return True
    return any(
        kind in {"reach", "must_reach", "response", "forbid", "invariant"}
        for kind in _fbmcq_property_kinds(calls)
    ) and "active(" in " ".join(_fbmcq_query_texts(calls))


def _has_condition_trigger_evidence(
    tree: ast.AST, calls: list[ast.Call], simulate_calls: list[ast.Call]
) -> bool:
    if any(
        _call_name(call) in {"transition_exists", "transitions", "effects", "effect_delta"}
        and _call_has_nonempty_string_keyword(call, "event")
        for call in calls
    ):
        return True
    if any(_simulate_has_nonempty_event_cycle(call) for call in simulate_calls):
        return True
    queries = " ".join(_fbmcq_query_texts(calls))
    if queries and ("event(" in queries or "response" in queries):
        return True
    return any(
        isinstance(node, ast.Attribute) and node.attr == "guard"
        for node in ast.walk(tree)
    )


def _call_has_nonempty_string_keyword(call: ast.Call, name: str) -> bool:
    return any(
        keyword.arg == name
        and isinstance(keyword.value, ast.Constant)
        and isinstance(keyword.value.value, str)
        and bool(keyword.value.value)
        for keyword in call.keywords
    )


def _simulate_has_nonempty_event_cycle(call: ast.Call) -> bool:
    cycles: ast.AST | None = None
    for keyword in call.keywords:
        if keyword.arg == "cycles":
            cycles = keyword.value
            break
    if cycles is None and call.args:
        cycles = call.args[0]
    if not isinstance(cycles, (ast.List, ast.Tuple)):
        return False
    return any(
        isinstance(cycle, (ast.List, ast.Tuple)) and bool(cycle.elts)
        for cycle in cycles.elts[1:]
    )


def _fbmcq_query_texts(calls: list[ast.Call]) -> list[str]:
    return [
        str(call.args[0].value)
        for call in calls
        if _call_name(call) == "fbmcq"
        and call.args
        and isinstance(call.args[0], ast.Constant)
        and isinstance(call.args[0].value, str)
    ]


def _parse_cardinality_target(cue: str) -> int | None:
    digit = re.search(r"(?<![A-Za-z])\d+(?![A-Za-z])", cue)
    if digit:
        return int(digit.group(0))
    lowered = cue.lower()
    for word, value in _NUMBER_WORDS.items():
        if re.search(rf"\b{re.escape(word)}\b", lowered) or word in cue:
            return value
    return None


def _cardinality_direction(cue: str) -> str:
    if _AT_LEAST_RE.search(cue):
        return "at_least"
    if _AT_MOST_RE.search(cue):
        return "at_most"
    if _EXACTLY_RE.search(cue):
        return "exactly"
    return "exactly"


def _has_cardinality_compare(tree: ast.AST, cue: str, target: int) -> bool:
    direction = _cardinality_direction(cue)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Compare):
            continue
        left = node.left
        for op, right in zip(node.ops, node.comparators):
            left_structural = _contains_structure_call(left)
            right_structural = _contains_structure_call(right)
            left_target = _is_numeric_literal(left, target)
            right_target = _is_numeric_literal(right, target)
            if left_structural and right_target and _cardinality_op_matches(op, direction):
                return True
            if left_target and right_structural and _cardinality_op_matches(
                _reverse_op(op), direction
            ):
                return True
            left = right
    return False


def _cardinality_op_matches(op: ast.cmpop, direction: str) -> bool:
    if direction == "at_least":
        return isinstance(op, (ast.Gt, ast.GtE, ast.Eq))
    if direction == "at_most":
        return isinstance(op, (ast.Lt, ast.LtE, ast.Eq))
    return isinstance(op, ast.Eq)


def _contains_structure_call(node: ast.AST) -> bool:
    return any(
        isinstance(child, ast.Call) and _call_name(child) in _STRUCTURE_FUNCTIONS
        for child in ast.walk(node)
    )


def _contains_call(node: ast.AST, name: str) -> bool:
    return any(
        isinstance(child, ast.Call) and _call_name(child) == name
        for child in ast.walk(node)
    )


def _is_numeric_literal(node: ast.AST, value: int) -> bool:
    return isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and node.value == value


__all__ = [
    "ERROR_CARDINALITY_COMPARISON_REQUIRED",
    "ERROR_CONDITION_TRIGGER_REQUIRED",
    "ERROR_CONTINUITY_EVIDENCE_REQUIRED",
    "ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK",
    "ERROR_EFFECTS_BOOL_SUBSTITUTE",
    "ERROR_EFFECT_DELTA_DIRECTION_REQUIRED",
    "ERROR_SIMULATE_FIRST_CYCLE_REQUIRED",
    "ERROR_SYNTAX_INVALID",
    "ERROR_TRANSITION_TARGET_REQUIRED",
    "validate_assertion_semantic_policy",
]
