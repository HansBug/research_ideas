"""Structural predicates evaluated over native ``pyfcstm.model`` objects."""

from __future__ import annotations

import re
from typing import Any, Iterable

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from .fcstm_native import (
    NativeFCSTM,
    all_transition_carriers,
    load_native_fcstm,
    native_load_failure,
    native_receipt,
    native_transition_endpoints,
    resolve_event,
    resolve_state,
    state_path,
    transition_by_ref,
    transition_owner_path,
)


def _normal(value: object) -> str:
    """Normalize presentation whitespace without rewriting FCSTM semantics."""

    return re.sub(r"\s+", " ", str(value or "").strip()).rstrip(";")


def _scope_matches(native: NativeFCSTM, transition: Any, scope: object) -> bool:
    """Apply the frozen S2 global or exact-owner transition scope contract."""

    if not isinstance(scope, str) or not scope.strip():
        return False
    requested = scope.strip()
    owner_path = transition_owner_path(transition)
    if requested == "closed_fcstm":
        # A closed FCSTM inventory ranges over every native authored carrier,
        # including nested owners.  It is not a synonym for the root owner.
        return True
    owner = resolve_state(native, requested)
    return owner is not None and owner_path == state_path(owner)


def _endpoint_matches(native: NativeFCSTM, transition: Any, source: object, target: object) -> bool:
    """Match one exact native transition endpoint pair."""

    observed_source, observed_target = native_transition_endpoints(transition)
    if not isinstance(source, str) or not isinstance(target, str):
        return False
    owner_path = transition_owner_path(transition)

    def endpoint_paths(observed: str) -> frozenset[str]:
        if observed == "[*]":
            return frozenset()
        return frozenset({observed, f"{owner_path}.{observed}"})

    source_ok = source == "[*]" and observed_source == "[*]"
    target_ok = target == "[*]" and observed_target == "[*]"
    if observed_source != "[*]":
        source_state = resolve_state(native, source)
        source_ok = (
            source_state is not None
            and state_path(source_state) in endpoint_paths(observed_source)
        )
    if observed_target != "[*]":
        target_state = resolve_state(native, target)
        target_ok = (
            target_state is not None
            and state_path(target_state) in endpoint_paths(observed_target)
        )
    return source_ok and target_ok


def _native_transition(plan: PredicatePlan, native: NativeFCSTM) -> Any | None:
    """Resolve an exact carrier only through the native FCSTM grammar span."""

    return transition_by_ref(native, plan.inputs.get("transition"))


def _action_texts(actions: Iterable[Any]) -> set[str]:
    """Collect the canonical names and operations exposed by native actions."""

    values: set[str] = set()
    for action in actions:
        if action.name:
            values.add(_normal(action.name))
        values.add(_normal(action.func_name))
        if not action.is_abstract and not action.is_ref:
            values.update(_normal(operation.to_ast_node()) for operation in action.operations)
    return values


def _parse_required_guard(value: object) -> Any | None:
    """Parse one required guard through the public FCSTM expression parser.

    S5 compares syntax-tree identity, not a hand-written string approximation.
    The candidate-side expression is parsed with the same FCSTM expression
    grammar that created ``Transition.guard`` before either AST is compared.
    """

    if not isinstance(value, str) or not value.strip():
        return None
    try:
        from pyfcstm.model import parse_expr_from_string

        return parse_expr_from_string(value, mode="logical").to_ast_node()
    except Exception:  # noqa: BLE001 - malformed typed input is an execution audit fact.
        return None


def run_source_static(plan: PredicatePlan, model: ModelIR, receipt_id: str):
    """Evaluate S1--S5 only through native FCSTM model classes."""

    predicate = plan.predicate_id or "unknown"
    try:
        native = load_native_fcstm(model)
    except Exception as exc:  # noqa: BLE001 - recorded as a failed backend execution.
        return native_load_failure(receipt_id, predicate, model, exc)
    inputs = plan.inputs

    if predicate == "S1":
        kind = inputs.get("kind")
        element = inputs.get("element")
        scope = inputs.get("scope")
        if not isinstance(kind, str) or not isinstance(element, str) or not isinstance(scope, str):
            return native_receipt(receipt_id, predicate, native, "unknown", "S1 requires exact kind, element, and declaration scope inputs.", "S1 typed input contract", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        root_path = state_path(native.machine.root_state)
        if scope not in {"closed_fcstm", root_path, native.machine.root_state.name}:
            return native_receipt(receipt_id, predicate, native, "unknown", "S1 currently admits only the exact closed-model declaration scope; a narrower scope needs a typed owner binding.", "native StateMachine declaration scope boundary", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        if kind == "state":
            found = resolve_state(native, element) is not None
        elif kind == "event":
            found = resolve_event(native, element) is not None
        elif kind in {"transition", "edge"}:
            found = transition_by_ref(native, element) is not None
        else:
            return native_receipt(receipt_id, predicate, native, "unknown", "S1 kind is outside the frozen native FCSTM state/event/transition vocabulary.", "native StateMachine vocabulary boundary", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        return native_receipt(receipt_id, predicate, native, "true" if found else "false", f"The native FCSTM declaration inventory {'contains' if found else 'does not contain'} the exact requested {kind}.", "pyfcstm.model.StateMachine native declaration objects", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", counterexample=[] if found else [{"kind": kind, "element": element, "scope": scope}])

    if predicate == "S2":
        source, target, scope = inputs.get("source"), inputs.get("target"), inputs.get("scope")
        if not isinstance(source, str) or not isinstance(target, str) or not isinstance(scope, str):
            return native_receipt(receipt_id, predicate, native, "unknown", "S2 requires exact source, target, and owner scope inputs.", "S2 typed input contract", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        if scope != "closed_fcstm" and resolve_state(native, scope) is None:
            return native_receipt(
                receipt_id,
                predicate,
                native,
                "unknown",
                "S2 cannot evaluate an exact owner-local transition because the declared owner scope does not resolve to one native FCSTM state.",
                "S2 typed owner-scope binding and pyfcstm.model.StateMachine state resolution",
                backend_family="fcstm_model",
                algorithm_version="pyfcstm.model.v1",
                failure_kind="invalid_input",
            )
        carrier = _native_transition(plan, native)
        candidates = (carrier,) if carrier is not None else all_transition_carriers(native)
        found = any(_scope_matches(native, transition, scope) and _endpoint_matches(native, transition, source, target) for transition in candidates)
        scope_kind = "closed-model" if scope == "closed_fcstm" else "exact-owner-local"
        return native_receipt(receipt_id, predicate, native, "true" if found else "false", f"The native FCSTM model {'contains' if found else 'does not contain'} the exact {scope_kind} transition.", "pyfcstm Transition owner, canonical endpoint identity, and grammar-span carrier", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", counterexample=[] if found else [{"source": source, "target": target, "scope": scope}])

    transition = _native_transition(plan, native)
    if predicate in {"S3", "S5"} and transition is None:
        return native_receipt(receipt_id, predicate, native, "unknown", f"{predicate} requires an exact transition:line:<n> carrier that resolves to exactly one native FCSTM transition.", "native transition grammar-span binding", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")

    if predicate == "S3":
        expected_values = inputs.get("triggers") or ()
        if not isinstance(expected_values, (list, tuple)):
            return native_receipt(receipt_id, predicate, native, "unknown", "S3 requires one typed trigger tuple.", "S3 typed input contract", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        if any(not isinstance(value, str) or not value.strip() for value in expected_values):
            return native_receipt(receipt_id, predicate, native, "unknown", "S3 requires every required trigger to be one exact non-empty trigger token; the empty tuple remains the deliberate no-trigger value.", "S3 typed trigger-token contract", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", failure_kind="invalid_input")
        # The expected side is a requirement binding and may deliberately name
        # an event absent from the model.  The observed side must therefore be
        # read directly from the exact native carrier, rather than resolving
        # expected names through the current model and making a missing-trigger
        # violation uncheckable.
        expected = set(expected_values)
        observed = {event.name for event in transition.events}
        verdict = "true" if expected == observed else "false"
        return native_receipt(receipt_id, predicate, native, verdict, "The required exact trigger token set was compared with the event identity on the native FCSTM transition carrier.", "pyfcstm Transition.event native event identity plus typed requirement trigger tokens", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", counterexample=[] if verdict == "true" else [{"expected": sorted(expected), "observed": sorted(observed)}])

    if predicate == "S4":
        state = resolve_state(native, inputs.get("state"))
        phase = inputs.get("phase")
        action = inputs.get("action")
        if state is None or phase not in {"entry", "do", "exit"} or not isinstance(action, str):
            return native_receipt(receipt_id, predicate, native, "unknown", "S4 requires one native state, one of entry/do/exit, and one exact action identity.", "strict S4 typed lifecycle binding", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")
        actions = {"entry": state.on_enters, "do": state.on_durings, "exit": state.on_exits}[phase]
        found = _normal(action) in _action_texts(actions)
        return native_receipt(receipt_id, predicate, native, "true" if found else "false", f"The exact action {'is' if found else 'is not'} attached to the native FCSTM {phase} lifecycle slot.", "pyfcstm State lifecycle action collections", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", counterexample=[] if found else [{"state": state_path(state), "phase": phase, "action": action}])

    if predicate == "S5":
        required_guard = inputs.get("guard")
        if required_guard == "":
            expected_ast = None
        elif not isinstance(required_guard, str):
            return native_receipt(receipt_id, predicate, native, "unknown", "S5 requires either an explicit empty guard or one guard that parses through the FCSTM logical-expression grammar.", "S5 native typed guard parser", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", failure_kind="invalid_input")
        else:
            expected_ast = _parse_required_guard(required_guard)
            if expected_ast is None:
                return native_receipt(receipt_id, predicate, native, "unknown", "S5 requires either an explicit empty guard or one guard that parses through the FCSTM logical-expression grammar.", "S5 native typed guard parser", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", failure_kind="invalid_input")
        observed_ast = transition.guard.to_ast_node() if transition.guard is not None else None
        verdict = "true" if expected_ast == observed_ast else "false"
        return native_receipt(receipt_id, predicate, native, verdict, "The required guard AST was compared with the exact native FCSTM transition guard AST.", "pyfcstm.model.parse_expr_from_string and Transition.guard.to_ast_node", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1", counterexample=[] if verdict == "true" else [{"expected": str(expected_ast), "observed": str(observed_ast) if observed_ast is not None else None}])

    return native_receipt(receipt_id, predicate, native, "unknown", "The native structural backend has no branch for this predicate.", "explicit native structural backend dispatch boundary", backend_family="fcstm_model", algorithm_version="pyfcstm.model.v1")


__all__ = ["run_source_static"]
