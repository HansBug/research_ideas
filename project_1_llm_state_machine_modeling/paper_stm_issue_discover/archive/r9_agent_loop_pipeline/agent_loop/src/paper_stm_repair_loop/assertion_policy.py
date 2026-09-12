from __future__ import annotations

import ast
import re
from typing import Any, Iterable

ERROR_SYNTAX_INVALID = "ASSERT_SYNTAX_INVALID"
ERROR_ASSERTION_DIRECT_SHAPE_REQUIRED = "ASSERT_DIRECT_POSITIVE_SHAPE_REQUIRED"
ERROR_SIMULATE_FIRST_CYCLE_REQUIRED = "ASSERT_SIMULATE_FIRST_CYCLE_REQUIRED"
ERROR_EFFECT_DELTA_DIRECTION_REQUIRED = "ASSERT_EFFECT_DELTA_DIRECTION_REQUIRED"
ERROR_EFFECT_DELTA_SENTINEL_VARIABLE = "ASSERT_EFFECT_DELTA_SENTINEL_VARIABLE"
ERROR_EFFECT_DELTA_LITERAL_VARIABLE_REQUIRED = (
    "ASSERT_EFFECT_DELTA_LITERAL_VARIABLE_REQUIRED"
)
ERROR_EFFECT_DELTAS_TRANSITION_BINDING_REQUIRED = (
    "ASSERT_EFFECT_DELTAS_TRANSITION_BINDING_REQUIRED"
)
ERROR_EFFECTS_BOOL_SUBSTITUTE = "ASSERT_EFFECTS_BOOL_SUBSTITUTE"
ERROR_CONTINUITY_EVIDENCE_REQUIRED = "ASSERT_CONTINUITY_EVIDENCE_REQUIRED"
ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK = (
    "ASSERT_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK"
)
ERROR_CARDINALITY_COMPARISON_REQUIRED = "ASSERT_CARDINALITY_COMPARISON_REQUIRED"
ERROR_CARDINALITY_OBJECT_SCOPE_REQUIRED = "ASSERT_CARDINALITY_OBJECT_SCOPE_REQUIRED"
ERROR_CARDINALITY_STABLE_SCOPE_REQUIRED = "ASSERT_CARDINALITY_STABLE_SCOPE_REQUIRED"
ERROR_TRANSITION_TARGET_REQUIRED = "ASSERT_TRANSITION_TARGET_REQUIRED"
ERROR_CONDITION_TRIGGER_REQUIRED = "ASSERT_CONDITION_TRIGGER_REQUIRED"

_STRUCTURE_FUNCTIONS = frozenset(
    {"states", "events", "variables", "transitions", "bound_model_refs"}
)
_CARDINALITY_SCOPE_FUNCTIONS = frozenset(
    {"states", "events", "variables", "transitions"}
)
_SENTINEL_VARIABLE_RE = re.compile(
    r"(?:sentinel|probe|dummy|placeholder|non[-_ ]?existent|does[-_ ]?not[-_ ]?exist|missing|future[-_ ]?model|only[-_ ]?for[-_ ]?test)",
    re.I,
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
        if _simulate_has_invalid_hot_start_request(call) or not _simulate_has_empty_first_cycle(call):
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
                if _uses_sentinel_effect_delta_variable(tree):
                    _add_error(
                        errors,
                        _format_error(ERROR_EFFECT_DELTA_SENTINEL_VARIABLE, requirement_id),
                    )
                if not _effect_delta_calls_use_literal_variables(calls):
                    _add_error(
                        errors,
                        _format_error(
                            ERROR_EFFECT_DELTA_LITERAL_VARIABLE_REQUIRED,
                            requirement_id,
                        ),
                    )
                if not _effect_deltas_calls_are_transition_bound(calls):
                    _add_error(
                        errors,
                        _format_error(
                            ERROR_EFFECT_DELTAS_TRANSITION_BINDING_REQUIRED,
                            requirement_id,
                        ),
                    )
                if _has_effect_delta_zero_compare(
                    tree, direction
                ) and not _has_direct_effect_direction_expression(tree, direction):
                    _add_error(
                        errors,
                        _format_error(
                            ERROR_ASSERTION_DIRECT_SHAPE_REQUIRED,
                            requirement_id,
                        ),
                    )
                elif not _has_effect_delta_zero_compare(tree, direction):
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
            if target is not None:
                if not _has_cardinality_compare(tree, cue, target):
                    _add_error(
                        errors,
                        _format_error(ERROR_CARDINALITY_COMPARISON_REQUIRED, requirement_id),
                    )
                elif not isinstance(tree.body, ast.Compare):
                    _add_error(
                        errors,
                        _format_error(
                            ERROR_ASSERTION_DIRECT_SHAPE_REQUIRED,
                            requirement_id,
                        ),
                    )
                else:
                    actual_object = _direct_cardinality_scope_function(
                        tree.body, cue, target
                    )
                    cardinality_text = "\n".join(
                        [
                            str(requirement.get("clause_text", "")),
                            cue,
                        ]
                    )
                    expected_object = _cardinality_object_function(cardinality_text)
                    if actual_object is None:
                        _add_error(
                            errors,
                            _format_error(
                                ERROR_CARDINALITY_STABLE_SCOPE_REQUIRED,
                                requirement_id,
                            ),
                        )
                    elif (
                        expected_object is None
                        or actual_object not in _CARDINALITY_SCOPE_FUNCTIONS
                        or actual_object != expected_object
                    ):
                        _add_error(
                            errors,
                            _format_error(
                                ERROR_CARDINALITY_OBJECT_SCOPE_REQUIRED,
                                requirement_id,
                            ),
                        )
                    elif (
                        not _has_stable_cardinality_scope_compare(tree, cue, target)
                        or (
                            expected_object == "states"
                            and _cardinality_requires_parent_scope(cardinality_text)
                            and not _direct_cardinality_states_parent_bound(tree.body)
                        )
                    ):
                        _add_error(
                            errors,
                            _format_error(
                                ERROR_CARDINALITY_STABLE_SCOPE_REQUIRED,
                                requirement_id,
                            ),
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
    if _simulate_has_exact_hot_start_literal_request(call):
        return True
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


def _simulate_has_exact_hot_start_literal_request(call: ast.Call) -> bool:
    initial_state, initial_vars = _simulate_hot_start_keywords(call)
    return _is_nonempty_string_literal(initial_state) and _is_literal_initial_vars_dict(
        initial_vars
    )


def _simulate_has_invalid_hot_start_request(call: ast.Call) -> bool:
    initial_state, initial_vars = _simulate_hot_start_keywords(call)
    if _is_absent_or_none_literal(initial_state):
        return not (
            _is_absent_or_none_literal(initial_vars)
            or _is_literal_initial_vars_dict(initial_vars)
        )
    if _is_nonempty_string_literal(initial_state):
        return not _is_literal_initial_vars_dict(initial_vars)
    return True


def _is_absent_or_none_literal(node: ast.AST | None) -> bool:
    return node is None or (
        isinstance(node, ast.Constant) and node.value is None
    )


def _simulate_hot_start_keywords(call: ast.Call) -> tuple[ast.AST | None, ast.AST | None]:
    initial_state = None
    initial_vars = None
    for keyword in call.keywords:
        if keyword.arg == "initial_state":
            initial_state = keyword.value
        if keyword.arg == "initial_vars":
            initial_vars = keyword.value
    return initial_state, initial_vars


def _is_nonempty_string_literal(node: ast.AST | None) -> bool:
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, str)
        and bool(node.value.strip())
    )


def _is_literal_initial_vars_dict(node: ast.AST | None) -> bool:
    if not isinstance(node, ast.Dict):
        return False
    for key, value in zip(node.keys, node.values):
        if not _is_nonempty_string_literal(key):
            return False
        if not _is_literal_initial_var_number(value):
            return False
    return True


def _is_literal_initial_var_number(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return isinstance(node.value, (int, float)) and not isinstance(node.value, bool)
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _is_literal_initial_var_number(node.operand)
    return False


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


def _uses_sentinel_effect_delta_variable(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or _call_name(node) != "effect_delta":
            continue
        variable = _call_keyword_constant_string(node, "variable")
        if variable is not None and _SENTINEL_VARIABLE_RE.search(variable):
            return True
    return False


def _effect_delta_calls_use_literal_variables(calls: list[ast.Call]) -> bool:
    for call in calls:
        if _call_name(call) != "effect_delta":
            continue
        if _call_keyword_constant_string(call, "variable") is None:
            return False
    return True


def _effect_deltas_calls_are_transition_bound(calls: list[ast.Call]) -> bool:
    for call in calls:
        if _call_name(call) != "effect_deltas":
            continue
        if not _call_has_nonempty_string_keyword(call, "source"):
            return False
        if not _call_has_nonempty_string_keyword(call, "target"):
            return False
        event = next(
            (keyword.value for keyword in call.keywords if keyword.arg == "event"),
            None,
        )
        if event is None:
            return False
        if not (
            _is_none_literal(event)
            or (isinstance(event, ast.Constant) and isinstance(event.value, str) and event.value)
        ):
            return False
    return True


def _has_direct_effect_direction_expression(tree: ast.Expression, direction: str) -> bool:
    body = tree.body
    if isinstance(body, ast.Compare) and len(body.ops) == len(body.comparators) == 1:
        left, right = body.left, body.comparators[0]
        op = body.ops[0]
        if _is_effect_delta_value(left) and _is_numeric_literal(right, 0):
            return _operator_matches_direction(op, direction)
        if _is_numeric_literal(left, 0) and _is_effect_delta_value(right):
            return _operator_matches_direction(_reverse_op(op), direction)
        return False
    return _is_direct_open_effect_any(body, direction)


def _is_effect_delta_value(node: ast.AST) -> bool:
    if isinstance(node, ast.Call) and _call_name(node) == "effect_delta":
        return True
    if not isinstance(node, ast.BoolOp) or not isinstance(node.op, ast.Or):
        return False
    if len(node.values) != 2:
        return False
    first, second = node.values
    return (
        isinstance(first, ast.Call)
        and _call_name(first) == "effect_delta"
        and _is_numeric_literal(second, 0)
    )


def _is_direct_open_effect_any(node: ast.AST, direction: str) -> bool:
    if not isinstance(node, ast.Call) or _call_name(node) != "any":
        return False
    if len(node.args) != 1 or node.keywords:
        return False
    comprehension = node.args[0]
    if not isinstance(comprehension, ast.GeneratorExp):
        return False
    if len(comprehension.generators) != 1:
        return False
    generator = comprehension.generators[0]
    if generator.ifs or generator.is_async:
        return False
    if not isinstance(generator.iter, ast.Call):
        return False
    if _call_name(generator.iter) != "effect_deltas":
        return False
    if not isinstance(generator.target, (ast.Tuple, ast.List)):
        return False
    names = [
        item.id for item in generator.target.elts if isinstance(item, ast.Name)
    ]
    if len(names) != 2:
        return False
    return _has_named_direction_compare(
        comprehension.elt,
        {names[1]},
        direction,
        direct_only=True,
    )


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
    return _has_effect_deltas_zero_compare(tree, direction)


def _has_effect_deltas_zero_compare(tree: ast.AST, direction: str) -> bool:
    """Recognize a directional comparison over tuple-unpacked effect_deltas."""

    for comprehension in ast.walk(tree):
        if not isinstance(comprehension, (ast.GeneratorExp, ast.ListComp)):
            continue
        delta_names: set[str] = set()
        for generator in comprehension.generators:
            if not _contains_call(generator.iter, "effect_deltas"):
                continue
            if isinstance(generator.target, (ast.Tuple, ast.List)):
                names = [
                    item.id
                    for item in generator.target.elts
                    if isinstance(item, ast.Name)
                ]
                if len(names) >= 2:
                    delta_names.add(names[-1])
        if delta_names and _has_named_direction_compare(
            comprehension.elt, delta_names, direction
        ):
            return True
    return False


def _has_named_direction_compare(
    node: ast.AST,
    names: set[str],
    direction: str,
    *,
    direct_only: bool = False,
) -> bool:
    comparisons = [node] if direct_only else ast.walk(node)
    for comparison in comparisons:
        if not isinstance(comparison, ast.Compare):
            continue
        left = comparison.left
        for op, right in zip(comparison.ops, comparison.comparators):
            left_name = isinstance(left, ast.Name) and left.id in names
            right_name = isinstance(right, ast.Name) and right.id in names
            left_zero = _is_numeric_literal(left, 0)
            right_zero = _is_numeric_literal(right, 0)
            if left_name and right_zero and _operator_matches_direction(op, direction):
                return True
            if left_zero and right_name and _operator_matches_direction(
                _reverse_op(op), direction
            ):
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


def _call_keyword_constant_string(call: ast.Call, name: str) -> str | None:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return keyword.value.value if isinstance(keyword.value.value, str) else None
    return None


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
    first_event_cycle = (
        0 if _simulate_has_exact_hot_start_literal_request(call) else 1
    )
    return any(
        isinstance(cycle, (ast.List, ast.Tuple)) and bool(cycle.elts)
        for cycle in cycles.elts[first_event_cycle:]
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


def _has_stable_cardinality_scope_compare(tree: ast.AST, cue: str, target: int) -> bool:
    direction = _cardinality_direction(cue)
    node = tree.body if isinstance(tree, ast.Expression) else tree
    if not isinstance(node, ast.Compare):
        return False
    if len(node.ops) != 1 or len(node.comparators) != 1:
        return False
    left, right = node.left, node.comparators[0]
    op = node.ops[0]
    if (
        _is_stable_cardinality_count(left)
        and _is_numeric_literal(right, target)
        and _cardinality_op_matches(op, direction)
    ):
        return True
    if (
        _is_numeric_literal(left, target)
        and _is_stable_cardinality_count(right)
        and _cardinality_op_matches(_reverse_op(op), direction)
    ):
        return True
    return False


def _direct_cardinality_scope_function(
    node: ast.Compare, cue: str, target: int
) -> str | None:
    direction = _cardinality_direction(cue)
    if len(node.ops) != 1 or len(node.comparators) != 1:
        return None
    left, right = node.left, node.comparators[0]
    op = node.ops[0]
    if _is_numeric_literal(right, target) and _cardinality_op_matches(op, direction):
        return _cardinality_count_function(left)
    if _is_numeric_literal(left, target) and _cardinality_op_matches(
        _reverse_op(op), direction
    ):
        return _cardinality_count_function(right)
    return None


def _cardinality_count_function(node: ast.AST) -> str | None:
    if not isinstance(node, ast.Call) or _call_name(node) != "len":
        return None
    if len(node.args) != 1 or node.keywords:
        return None
    counted = node.args[0]
    if not isinstance(counted, ast.Call):
        return None
    return _call_name(counted)


def _cardinality_object_function(text: str) -> str | None:
    lowered = text.lower()
    if re.search(r"\bstate[- ]transitions?\b", lowered):
        return "transitions"
    candidates: set[str] = set()
    patterns = {
        "states": (
            r"\b(?:states?|sub[- ]?states?|areas?|regions?|modes?|phases?|branches?)\b",
            r"(?:状态|子状态|区域|模式|阶段|分支)",
        ),
        "events": (r"\b(?:events?|signals?|triggers?)\b", r"(?:事件|信号|触发器)"),
        "variables": (
            r"\b(?:variables?|counters?|registers?)\b",
            r"(?:变量|计数器|寄存器)",
        ),
        "transitions": (
            r"\b(?:transitions?|edges?|arcs?)\b",
            r"(?:迁移|转移|边)",
        ),
    }
    for function_name, alternatives in patterns.items():
        if any(re.search(pattern, lowered, re.I) for pattern in alternatives):
            candidates.add(function_name)
    return next(iter(candidates)) if len(candidates) == 1 else None


def _cardinality_requires_parent_scope(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:sub[- ]?states?|areas?|regions?|modes?|phases?|branches?)\b|"
            r"(?:子状态|区域|模式|阶段|分支)",
            text,
            re.I,
        )
    )


def _direct_cardinality_states_parent_bound(node: ast.AST) -> bool:
    if not isinstance(node, ast.Compare) or len(node.comparators) != 1:
        return False
    candidates = (node.left, node.comparators[0])
    for candidate in candidates:
        if not isinstance(candidate, ast.Call) or _call_name(candidate) != "len":
            continue
        if len(candidate.args) != 1 or not isinstance(candidate.args[0], ast.Call):
            continue
        states_call = candidate.args[0]
        if _call_name(states_call) != "states":
            continue
        if _call_has_nonempty_string_keyword(
            states_call, "parent"
        ) and _call_keyword_constant_bool(states_call, "recursive") is False:
            return True
    return False


def _is_stable_cardinality_count(node: ast.AST) -> bool:
    if not isinstance(node, ast.Call) or _call_name(node) != "len" or len(node.args) != 1:
        return False
    counted = node.args[0]
    if any(
        isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp))
        for child in ast.walk(counted)
    ):
        return False
    if not isinstance(counted, ast.Call):
        return False
    function_name = _call_name(counted)
    if function_name not in _STRUCTURE_FUNCTIONS:
        return False
    if (
        function_name in {"states", "events", "variables"}
        and _call_keyword_constant_string(counted, "name") is not None
    ):
        return False
    if function_name == "states" and _call_keyword_constant_string(counted, "parent") is not None:
        return _call_keyword_constant_bool(counted, "recursive") is False
    return True


def _call_keyword_constant_bool(call: ast.Call, name: str) -> bool | None:
    for keyword in call.keywords:
        if keyword.arg == name and isinstance(keyword.value, ast.Constant):
            return keyword.value.value if isinstance(keyword.value.value, bool) else None
    return None


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


def _is_none_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is None


__all__ = [
    "ERROR_ASSERTION_DIRECT_SHAPE_REQUIRED",
    "ERROR_CARDINALITY_COMPARISON_REQUIRED",
    "ERROR_CARDINALITY_OBJECT_SCOPE_REQUIRED",
    "ERROR_CARDINALITY_STABLE_SCOPE_REQUIRED",
    "ERROR_CONDITION_TRIGGER_REQUIRED",
    "ERROR_CONTINUITY_EVIDENCE_REQUIRED",
    "ERROR_CONTINUITY_EXISTENTIAL_FORMAL_TOO_WEAK",
    "ERROR_EFFECTS_BOOL_SUBSTITUTE",
    "ERROR_EFFECT_DELTA_LITERAL_VARIABLE_REQUIRED",
    "ERROR_EFFECT_DELTAS_TRANSITION_BINDING_REQUIRED",
    "ERROR_EFFECT_DELTA_SENTINEL_VARIABLE",
    "ERROR_EFFECT_DELTA_DIRECTION_REQUIRED",
    "ERROR_SIMULATE_FIRST_CYCLE_REQUIRED",
    "ERROR_SYNTAX_INVALID",
    "ERROR_TRANSITION_TARGET_REQUIRED",
    "validate_assertion_semantic_policy",
]
