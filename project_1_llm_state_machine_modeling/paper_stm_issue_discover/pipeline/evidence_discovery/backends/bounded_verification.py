"""Bounded predicates executed by the native FCSTM ``.fbmcq`` engine.

This module intentionally contains no graph projection, guard evaluator, or
finite-assignment enumerator. It obtains choice-group members, variable
references, state identities, and paths from ``pyfcstm.model.StateMachine``;
the truth value then comes exclusively from the public ``.fbmcq``
compile/solve/witness/replay pipeline.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Mapping, Sequence
import time
from typing import Any

from ..compiler.lowering import PredicatePlan
from ..inputs.models import ModelIR
from .fcstm_native import (
    NativeFCSTM,
    all_states,
    all_transition_carriers,
    execute_fbmcq,
    fbmcq_wall_clock_timeout_ms,
    load_native_fcstm,
    native_load_failure,
    native_receipt,
    resolve_event,
    resolve_state,
    state_path,
)


def _bound(native: NativeFCSTM) -> int:
    """Choose a documented finite BMC horizon from the native state space."""

    return max(1, len(all_states(native)))


def _transition_starts_at(transition: Any, source: Any) -> bool:
    """Check authored native carrier source identity for one state."""

    return transition.source in {source.name, state_path(source)}


def _choice_group(
    native: NativeFCSTM,
    source_value: object,
    trigger_value: object,
) -> tuple[tuple[Any, ...], str | None]:
    """Return one exact native same-source/same-event choice group."""

    source = resolve_state(native, source_value)
    if source is None:
        return (), "the exact choice-group source does not resolve to one native FCSTM state"
    event = None if trigger_value is None else resolve_event(native, trigger_value)
    if trigger_value is not None and event is None:
        return (), "the exact choice-group trigger does not resolve to one native FCSTM event"
    rows = tuple(
        transition
        for transition in all_transition_carriers(native)
        if _transition_starts_at(transition, source)
        and transition.event is event
        and transition.guard is not None
    )
    if len(rows) < 2:
        return (), "the exact native same-source/same-event (including eventless) group has fewer than two guarded transitions"
    return rows, None


def _guard_texts(rows: Sequence[Any]) -> tuple[str, ...]:
    """Render guards from native expression AST nodes without reparsing text."""

    return tuple(str(transition.guard.to_ast_node()) for transition in rows)


def _guard_variables(rows: Sequence[Any]) -> tuple[str, ...]:
    """Read free variables from native guard expression objects."""

    return tuple(
        sorted(
            {
                variable.name
                for transition in rows
                for variable in transition.guard.list_variables()
            }
        )
    )


def _fbmcq_literal(value: object) -> str | None:
    """Render one already typed finite-domain literal for FBMCQ source."""

    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float) and value == value and value not in {float("inf"), float("-inf")}:
        return repr(value)
    return None


def _domain_clause(
    native: NativeFCSTM,
    domain: object,
    required_variables: Sequence[str],
) -> tuple[tuple[str, ...], str | None, str | None]:
    """Compile a declared finite typed domain to an FBMCQ initial constraint.

    The finite set/range remains symbolic in the FCSTM BMC solver. This adapter
    does not enumerate assignments or evaluate guards in Python.
    """

    if not isinstance(domain, Mapping) or not domain:
        return (), None, "the predicate requires a non-empty independently declared finite domain"
    if any(name not in domain for name in required_variables):
        missing = sorted(set(required_variables) - set(domain))
        return (), None, f"the finite domain omits native guard variables {missing}"
    clauses: list[str] = []
    names: list[str] = []
    for name, specification in sorted(domain.items()):
        if not isinstance(name, str) or name not in native.machine.defines:
            return (), None, f"domain variable {name!r} is not a declared native FCSTM variable"
        if not isinstance(specification, Mapping):
            return (), None, f"domain variable {name!r} must use an explicit values or min/max object"
        raw_values = specification.get("values")
        if isinstance(raw_values, Sequence) and not isinstance(raw_values, (str, bytes)):
            values = tuple(_fbmcq_literal(value) for value in raw_values)
            if not values or any(value is None for value in values):
                return (), None, f"domain variable {name!r} has no finite FBMCQ-compatible values"
            clauses.append("(" + " || ".join(f"{name} == {value}" for value in values) + ")")
            names.append(name)
            continue
        lower = specification.get("min")
        upper = specification.get("max")
        if (
            isinstance(lower, int)
            and not isinstance(lower, bool)
            and isinstance(upper, int)
            and not isinstance(upper, bool)
            and lower <= upper
            and native.machine.defines[name].type == "int"
        ):
            clauses.append(f"({name} >= {lower} && {name} <= {upper})")
            names.append(name)
            continue
        return (), None, f"domain variable {name!r} is not a finite native integer range or literal-value set"
    return tuple(names), " && ".join(clauses), None


def _choice_query(
    native: NativeFCSTM,
    source_value: object,
    domain_names: Sequence[str],
    domain_condition: str,
    body: str,
) -> str | None:
    """Build a hot-start FBMCQ query for a native choice-group state."""

    source = resolve_state(native, source_value)
    if source is None:
        return None
    havoc = ", ".join(domain_names)
    return (
        f'init state("{state_path(source)}") havoc {{ {havoc} }} where {domain_condition};\n'
        f"check forbid <= 1: {body};"
    )


def _proposition(native: NativeFCSTM, value: object, *, response_trigger: bool) -> str | None:
    """Bind a V3 proposition to a native state or event observation atom."""

    if isinstance(value, Mapping):
        if set(value) == {"state"}:
            value = value["state"]
        elif set(value) == {"event"}:
            value = ("event", value["event"])
        else:
            return None
    if isinstance(value, tuple) and len(value) == 2 and value[0] == "event":
        event = resolve_event(native, value[1])
        return f'event("{event.path_name}", current)' if response_trigger and event else None
    state = resolve_state(native, value)
    if state is not None:
        return f'active("{state_path(state)}")'
    event = resolve_event(native, value)
    return f'event("{event.path_name}", current)' if response_trigger and event else None


def _scope_initialization(native: NativeFCSTM, scope: object) -> tuple[str, str | None]:
    """Bind a V3/V5 declared scope to native cold or hot initialization."""

    if scope in (None, "closed_fcstm", "cold"):
        return "init cold;", None
    candidate = scope.get("initial_scope") if isinstance(scope, Mapping) else scope
    state = resolve_state(native, candidate)
    if state is None:
        return "", "the declared finite verification scope does not resolve to one native FCSTM state"
    return f'init state("{state_path(state)}");', None


def _v4_scope_states(native: NativeFCSTM, initial_scope: object) -> tuple[tuple[Any, ...], str | None]:
    """Restrict V4 to reachable native stable leaves in its execution scope.

    Root-closed V4 must not turn a structurally unreachable dead-end into a
    violation. Reachability comes from pyfcstm's native leaf-level topology
    projection; FBMCQ still supplies the actual progress verdict for each
    retained configuration. An explicit state scope is a hot initial scope, so
    its exact leaf and its native topology-reachable leaves are included.
    """

    from pyfcstm.verify.topology import topological_reachable_set, unreachable_states

    if initial_scope in (None, "closed_fcstm", "cold"):
        anchor = native.machine.root_state
        excluded = set(unreachable_states(native.machine))
        reachable = {
            state_path(state)
            for state in all_states(native)
            if state_path(state) not in excluded
        }
    else:
        anchor = resolve_state(native, initial_scope)
        if anchor is None:
            return (), "the V4 initial_scope does not resolve to one native FCSTM state"
        anchor_path = state_path(anchor)
        reachable = {
            anchor_path,
            *topological_reachable_set(native.machine).get(anchor_path, ()),
        }
    prefix = state_path(anchor) + "."
    states = tuple(
        state
        for state in all_states(native)
        if state.is_stoppable
        and state_path(state) in reachable
        and (state is anchor or state_path(state).startswith(prefix))
    )
    if not states:
        return (), "the declared V4 scope contains no native stable leaf configurations"
    return states, None


def _v4_progress_query(state: Any) -> str:
    """Ask FBMCQ for one real post-step configuration change from a stable leaf."""

    path = state_path(state)
    return (
        f'init state("{path}");\n'
        f'check reach <= 1: !active("{path}") || terminated();'
    )


def _v5_invariant_query(initialization: str, condition: str, horizon: int) -> str:
    """Build a cold-safe native invariant query at a requested finite bound.

    ``init cold`` exposes the FCSTM cold-init sentinel at frame zero. The
    sentinel is not a reachable user configuration, so a direct FBMCQ
    ``invariant`` would reject every user-state occupancy assertion before the
    root initial descent. A response triggered on every executable macrostep
    checks frames ``1..horizon``: the cold-entry result and every following
    native macrostep. The requested horizon is unchanged.
    """

    return (
        f"{initialization}\n"
        f"check response <= {horizon}:\n"
        "    trigger cycle >= 0\n"
        f"    -> within 1 {condition};"
    )


def _v5_incremental_invariant(
    *,
    receipt_id: str,
    native: NativeFCSTM,
    initialization: str,
    condition: str,
) -> Any:
    """Check V5 from small bounds upward without weakening its target horizon.

    A replayed counterexample at a smaller bound is a valid counterexample for
    the requested invariant horizon. A smaller-bound satisfaction result is
    intentionally only progress evidence: checking continues until the exact
    requested horizon, or the shared full-chain deadline produces a failure.
    """

    requested_horizon = _bound(native)
    overall_budget_ms = fbmcq_wall_clock_timeout_ms()
    started_at = time.monotonic()
    attempts: list[dict[str, Any]] = []
    final_receipt: Any | None = None
    for horizon in range(1, requested_horizon + 1):
        elapsed_ms = (time.monotonic() - started_at) * 1000
        remaining_ms = max(1, int(overall_budget_ms - elapsed_ms))
        query = _v5_invariant_query(initialization, condition, horizon)
        probe = execute_fbmcq(
            receipt_id=f"{receipt_id}:bound:{horizon}",
            predicate="V5",
            native=native,
            query=query,
            reason="The native FBMCQ invariant checked the exact state occupancy condition over every reachable frame in this finite bound.",
            basis="native StateMachine state identity and .fbmcq invariant",
            wall_clock_timeout_ms=remaining_ms,
        )
        attempts.append(
            {
                "horizon": horizon,
                "terminal_state": probe.terminal_state,
                "verdict": probe.verdict,
                "query_hash": probe.run_metadata.get("fbmcq_query_hash"),
                "failure_stage": probe.run_metadata.get("fbmcq_execution", {}).get("failure_stage"),
                "elapsed_ms": probe.run_metadata.get("fbmcq_execution", {}).get("elapsed_ms"),
            }
        )
        final_receipt = probe
        if probe.terminal_state != "completed" or probe.verdict not in {"true", "false"}:
            break
        if probe.verdict == "false" or horizon == requested_horizon:
            break
    if final_receipt is None:
        raise RuntimeError("V5 incremental invariant did not create an FBMCQ attempt")
    completed_horizon = attempts[-1]["horizon"]
    early_counterexample = (
        final_receipt.terminal_state == "completed"
        and final_receipt.verdict == "false"
        and completed_horizon < requested_horizon
    )
    metadata = dict(final_receipt.run_metadata)
    metadata["v5_incremental"] = {
        "requested_horizon": requested_horizon,
        "completed_horizon": completed_horizon,
        "witness_horizon": completed_horizon if final_receipt.verdict == "false" else None,
        "counterexample_early_termination": early_counterexample,
        "overall_wall_clock_deadline_ms": overall_budget_ms,
        "overall_elapsed_ms": round((time.monotonic() - started_at) * 1000, 3),
        "attempts": attempts,
    }
    if early_counterexample:
        reason = (
            "The native FBMCQ invariant produced a replayed counterexample at "
            f"horizon {completed_horizon}; that trace is within the requested "
            f"horizon {requested_horizon}, so the exact invariant is false."
        )
        basis = (
            final_receipt.basis
            + "; lower-bound counterexample is a valid prefix witness for the requested V5 horizon"
        )
    elif final_receipt.terminal_state == "completed" and final_receipt.verdict == "true":
        reason = (
            "The native FBMCQ invariant completed through the exact requested "
            f"horizon {requested_horizon} without a counterexample."
        )
        basis = final_receipt.basis + "; all incremental lower bounds reached the requested V5 horizon"
    else:
        reason = final_receipt.reason
        basis = final_receipt.basis + "; V5 did not obtain a Boolean result before the requested horizon was closed"
    return final_receipt.model_copy(
        update={
            "receipt_id": receipt_id,
            "reason": reason,
            "basis": basis,
            "run_metadata": metadata,
        }
    )


def run_bounded_verification(plan: PredicatePlan, model: ModelIR, receipt_id: str):
    """Evaluate V1--V5 through native FCSTM objects and FBMCQ only."""

    predicate = plan.predicate_id or "unknown"
    try:
        native = load_native_fcstm(model)
    except Exception as exc:  # noqa: BLE001 - preserve loader failure in execution audit.
        return native_load_failure(receipt_id, predicate, model, exc)
    inputs = plan.inputs

    if predicate in {"V1", "V2"}:
        rows, group_error = _choice_group(native, inputs.get("source"), inputs.get("trigger"))
        if group_error is not None:
            return native_receipt(receipt_id, predicate, native, "unknown", "The bounded guard predicate requires one exact native same-source/same-event choice group.", group_error, backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        guards = _guard_texts(rows)
        variables = _guard_variables(rows)
        domain_names, domain_condition, domain_error = _domain_clause(native, inputs.get("domain"), variables)
        if domain_error is not None or domain_condition is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "The bounded guard predicate needs a complete finite domain for every native guard variable.", domain_error or "missing FBMCQ domain condition", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        if predicate == "V1":
            supplied = tuple(str(value) for value in (inputs.get("guards") or ()))
            if Counter(supplied) != Counter(guards):
                return native_receipt(receipt_id, predicate, native, "unknown", "V1 supplied guards must exactly equal the guards on the resolved native choice group.", "native Transition.guard AST multiset equality", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
            pairs = [f"(({left}) && ({right}))" for index, left in enumerate(guards) for right in guards[index + 1 :]]
            query = _choice_query(native, inputs.get("source"), domain_names, domain_condition, " || ".join(pairs))
            reason = "The native FBMCQ solver checked that no pair of exact same-choice-group guard ASTs is simultaneously satisfiable in the declared domain."
            basis = "native StateMachine transition group plus guard.list_variables and .fbmcq forbid"
        else:
            query = _choice_query(native, inputs.get("source"), domain_names, domain_condition, "!(" + " || ".join(f"({guard})" for guard in guards) + ")")
            reason = "The native FBMCQ solver checked that the exact same-choice-group guard disjunction covers the declared domain."
            basis = "native StateMachine transition group plus guard.list_variables and .fbmcq forbid"
        if query is None:
            return native_receipt(receipt_id, predicate, native, "unknown", "The native choice-group source could not be used as an FBMCQ hot start.", "native source-state resolution", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        return execute_fbmcq(receipt_id=receipt_id, predicate=predicate, native=native, query=query, reason=reason, basis=basis)

    if predicate == "V3":
        p = _proposition(native, inputs.get("p"), response_trigger=True)
        q = _proposition(native, inputs.get("q"), response_trigger=False)
        bound = inputs.get("bound")
        if p is None or q is None or not isinstance(bound, int) or isinstance(bound, bool) or bound <= 0 or inputs.get("unit") != "steps":
            return native_receipt(receipt_id, predicate, native, "unknown", "V3 requires native state/event propositions, a positive integer step bound, and unit=steps.", "V3 typed proposition/bound contract", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        initialization, scope_error = _scope_initialization(native, inputs.get("scope"))
        if scope_error is not None:
            return native_receipt(receipt_id, predicate, native, "unknown", "V3 requires a closed native FCSTM execution scope.", scope_error, backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        query_bound = max(_bound(native), bound)
        query = f"{initialization}\ncheck response <= {query_bound}:\n    trigger {p}\n    -> within {bound} {q};"
        return execute_fbmcq(receipt_id=receipt_id, predicate=predicate, native=native, query=query, reason="The native FBMCQ response property checked every bound p occurrence for an exact q response in the declared step window.", basis="native proposition bindings and .fbmcq response")

    if predicate == "V4":
        states, scope_error = _v4_scope_states(native, inputs.get("initial_scope"))
        if scope_error is not None:
            return native_receipt(receipt_id, predicate, native, "unknown", "V4 requires a closed scope of native stable nonterminal FCSTM configurations.", scope_error, backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        probes: list[dict[str, Any]] = []
        blocked: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []
        for state in states:
            probe = execute_fbmcq(
                receipt_id=f"{receipt_id}:{state_path(state)}",
                predicate=predicate,
                native=native,
                query=_v4_progress_query(state),
                reason="Native FBMCQ searched for a committed successor configuration from one exact stable leaf.",
                basis="native State.is_stoppable plus .fbmcq reach",
            )
            entry = {
                "state": state_path(state),
                "terminal_state": probe.terminal_state,
                "verdict": probe.verdict,
                "query": probe.run_metadata.get("fbmcq_query"),
                "solve": probe.run_metadata.get("fbmcq_solve"),
                "receipt": probe.to_dict(),
            }
            probes.append(entry)
            if probe.terminal_state != "completed" or probe.verdict not in {"true", "false"}:
                failures.append(entry)
            elif probe.verdict == "false":
                blocked.append(entry)
        metadata = {"v4_native_progress_probes": probes, "fbmcq_query_count": len(probes)}
        if failures:
            return native_receipt(receipt_id, predicate, native, "unknown", "At least one native V4 progress query did not reach a Boolean FBMCQ result; no deadlock verdict is claimed.", "per-state native V4 FBMCQ execution failure", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1", metadata=metadata)
        verdict = "false" if blocked else "true"
        return native_receipt(receipt_id, predicate, native, verdict, "Every native stable leaf in the declared scope was checked for a real one-step successor configuration through FBMCQ.", "native State.is_stoppable and per-state .fbmcq reachability", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1", counterexample=blocked, metadata=metadata)

    if predicate == "V5":
        state = resolve_state(native, inputs.get("state"))
        expected = inputs.get("expected")
        if state is None or expected not in {0, 1, False, True}:
            return native_receipt(receipt_id, predicate, native, "unknown", "V5 requires one exact native state and an expected occupancy value of 0 or 1.", "V5 typed state/occupancy contract", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        initialization, scope_error = _scope_initialization(native, inputs.get("initial_scope"))
        if scope_error is not None:
            return native_receipt(receipt_id, predicate, native, "unknown", "V5 requires a closed native FCSTM initial scope.", scope_error, backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")
        atom = f'active("{state_path(state)}")'
        condition = atom if bool(expected) else f"!{atom}"
        return _v5_incremental_invariant(
            receipt_id=receipt_id,
            native=native,
            initialization=initialization,
            condition=condition,
        )

    return native_receipt(receipt_id, predicate, native, "unknown", "The bounded backend received an unknown frozen predicate ID.", "explicit native bounded-verification dispatch boundary", backend_family="fbmcq", algorithm_version="pyfcstm.fbmcq.v1")


__all__ = ["run_bounded_verification"]
