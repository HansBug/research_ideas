"""Deterministic primary routing from typed contracts to frozen predicates.

This module is deliberately downstream of LLM grounding and upstream of
predicate compilation.  It may use one current pair's typed contracts, exact
grounding bindings, closed ``ModelIR`` references, and method-visible facts.
It never consumes ledger expectations, Judge output, another pair's result, or
candidate prose as an identity resolver.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from itertools import product
import json
import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from ..backends.fcstm_native import (
    all_events,
    all_states,
    all_transition_carriers,
    load_native_fcstm,
    parse_effect_operation,
    resolve_event,
    resolve_state,
    state_path,
    transition_by_ref,
)
from ..inputs.fcstm_native_projection import transition_carrier_reference
from ..inputs.models import PairInput, StateNode, Transition
from .binding import resolve_state_ref, resolve_transition_ref
from .obligations import CandidateIssue
from .workflow import GroundingResponse, NLContract


PredicateId = Literal[
    "S1", "S2", "S3", "S4", "S5", "S6",
    "G1", "G2", "G3", "G4",
    "R1", "R2", "R3", "R4",
    "V1", "V2", "V3", "V4", "V5",
]


_PROPERTY_PREDICATES: dict[str, tuple[PredicateId, ...]] = {
    "initial_entry": ("S2",),
    "transition_endpoints": ("S2",),
    "trigger_set": ("S3",),
    "state_action": ("S4",),
    "guard": ("S5",),
    "effect": ("S6",),
    "reachability": ("G1",),
    "coaccessibility": ("G4",),
    "event_consumption": ("R1",),
    "state_retention": ("R4",),
    "guard_disjointness": ("V1",),
    "deadlock_freedom": ("V4",),
    "termination": ("G4",),
}

_PREDICATE_BACKENDS: dict[PredicateId, str] = {
    "S1": "fcstm_model",
    "S2": "fcstm_model",
    "S3": "fcstm_model",
    "S4": "fcstm_model",
    "S5": "fcstm_model",
    "S6": "fcstm_model",
    "G1": "fcstm_topology",
    "G2": "fcstm_topology",
    "G3": "fcstm_topology",
    "G4": "fcstm_topology",
    "R1": "fcstm_runtime",
    "R2": "fcstm_runtime",
    "R3": "fcstm_runtime",
    "R4": "fcstm_runtime",
    "V1": "fbmcq",
    "V2": "fbmcq",
    "V3": "fbmcq",
    "V4": "fbmcq",
    "V5": "fbmcq",
}

_COLD_MACROSTEP_WINDOW = re.compile(r"^cold_macrosteps=(?P<count>[1-9][0-9]*)$")
_MAX_COLD_MACROSTEPS = 32
_MAX_R4_ENTRY_EVENTS = 3
_MAX_R4_EVENT_VOCABULARY = 12
_STRICT_REBIND_PREDICATES = frozenset({"S4", "S6"})


class PredicateRouteTelemetry(BaseModel):
    """Per-contract route state retained independently from evidence levels.

    The row exposes whether a frozen predicate could be selected and later
    receives compilation/execution outcomes in the runner.  A null selection
    is a precise input-closure result, not a claim that a frozen predicate lacks
    academic standing or a backend.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    contract_id: str = Field(min_length=1, description="Exact NLContract identifier assessed by this deterministic route stage.")
    applicable_predicates: tuple[PredicateId, ...] = Field(default_factory=tuple, description="Frozen predicates compatible with the contract's typed property before input closure.")
    route_attempted: bool = Field(description="Whether the deterministic binder evaluated this contract without consulting evaluation answers.")
    selected_predicate: PredicateId | None = Field(default=None, description="Frozen predicate selected after exact input closure, or null when no legal route closed.")
    binding_complete: bool = Field(default=False, description="Whether selected predicate inputs have exact current-pair identities before compilation.")
    backend: str | None = Field(default=None, description="Native backend family for the selected predicate, or null when no route is selected.")
    execution_state: Literal["not_attempted", "completed", "failed"] = Field(default="not_attempted", description="Execution state updated by the runner after predicate compilation and backend invocation.")
    final_W: Literal["W0", "W1", "W2"] | None = Field(default=None, description="Final deterministic witness level for the selected route after execution, or null before no evidence record exists.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the route decision or the exact missing closure.")
    basis: str = Field(min_length=1, description="Closed contract, binding, ModelIR, and method-visible-fact basis for the route decision.")


class PrimaryRouteProjection(BaseModel):
    """Candidate replacement and telemetry output of the primary route stage."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    candidates: tuple[CandidateIssue, ...] = Field(description="Candidates retaining their original semantic identity, with predicate inputs filled only where an exact route closes.")
    telemetry: tuple[PredicateRouteTelemetry, ...] = Field(description="One route row for every current typed contract.")
    reason: str = Field(min_length=1, description="Non-empty summary of the deterministic primary routing stage.")
    basis: str = Field(min_length=1, description="Allowed input authorities and frozen predicate compatibility basis.")


def _unique_strings(values: Sequence[object]) -> tuple[str, ...]:
    """Return non-empty strings in deterministic insertion order."""

    result: list[str] = []
    for value in values:
        if isinstance(value, str) and value.strip() and value not in result:
            result.append(value)
    return tuple(result)


def _state_for_ref(pair: PairInput, reference: str | None) -> StateNode | None:
    """Resolve one already exact owned-model state reference."""

    return next((item for item in pair.model.states if item.ref == reference), None)


def _state_for_roles(
    pair: PairInput,
    contract: NLContract,
    grounding: Sequence[GroundingResponse],
    roles: set[str],
) -> tuple[StateNode | None, str]:
    """Close one state argument through exact binding or unambiguous hint lookup."""

    relevant = [
        binding
        for response in grounding
        for binding in response.semantic_bindings
        if binding.contract_id == contract.contract_id and binding.role in roles
    ]
    exact_refs = {
        binding.model_element_ref
        for binding in relevant
        if binding.status == "exact" and binding.model_element_ref is not None
    }
    if exact_refs:
        if len(exact_refs) != 1:
            return None, "conflicting exact grounding state bindings"
        state = _state_for_ref(pair, next(iter(exact_refs)))
        return state, "exact grounding semantic binding" if state else "exact binding does not name a closed ModelIR state"
    if relevant:
        return None, "grounding explicitly left the required state role ambiguous or unbound"
    refs = {
        resolve_state_ref(hint.value, pair.model)
        for hint in contract.binding_hints
        if hint.role in roles
    }
    refs.discard(None)
    if len(refs) != 1:
        return None, "typed contract hints do not resolve to one exact closed ModelIR state"
    return _state_for_ref(pair, next(iter(refs))), "unique typed-contract hint and closed ModelIR resolution"


def _transition_for_candidate(
    pair: PairInput,
    contract: NLContract,
    candidate: CandidateIssue,
    grounding: Sequence[GroundingResponse],
) -> tuple[Transition | None, str]:
    """Close one carrier only through exact binding, typed hints, or one ref."""

    values: list[str] = []
    supplied = candidate.predicate_inputs.get("transition") or candidate.predicate_inputs.get("transition_ref")
    if isinstance(supplied, str):
        values.append(supplied)
    values.extend(
        binding.carrier_transition_ref
        for response in grounding
        for binding in response.semantic_bindings
        if binding.contract_id == contract.contract_id
        and binding.status == "exact"
        and binding.carrier_transition_ref is not None
    )
    values.extend(
        hint.value for hint in contract.binding_hints if hint.role == "transition"
    )
    values.extend(
        ref for ref in candidate.element_refs if ref in pair.model.transition_refs
    )
    refs = {
        resolve_transition_ref(value, pair.model)
        for value in _unique_strings(values)
    }
    refs.discard(None)
    if len(refs) != 1:
        return None, "the route requires one exact transition carrier but available bindings are absent or non-unique"
    transition = pair.model.transition(next(iter(refs)))
    return transition, "exact transition carrier closure" if transition else "resolved transition reference is absent from closed ModelIR"


def _contract_values(contract: NLContract, roles: set[str]) -> tuple[str, ...]:
    """Return source-side typed values without treating prose as a model ref."""

    return _unique_strings(
        [hint.value for hint in contract.binding_hints if hint.role in roles]
    )


def _scope_for_endpoint(pair: PairInput, contract: NLContract, source: StateNode) -> tuple[str | None, str]:
    """Close S2 owner scope from explicit typed owner or source ancestry."""

    explicit = _unique_strings(
        [
            hint.value
            for hint in contract.binding_hints
            if hint.role in {"owner", "scope"}
        ]
    )
    if explicit:
        refs = {resolve_state_ref(value, pair.model) for value in explicit}
        refs.discard(None)
        if len(refs) != 1:
            return None, "explicit owner/scope hints are not one exact state"
        scope = _state_for_ref(pair, next(iter(refs)))
        return (scope.canonical_path if scope else None), "explicit exact owner/scope binding"
    if source.parent_ref is None:
        return "closed_fcstm", "top-level source has closed-model owner scope"
    owner = _state_for_ref(pair, source.parent_ref)
    if owner is None:
        return None, "source state parent does not resolve to one closed owner state"
    return owner.canonical_path, "source state has one exact enclosing ModelIR owner"


def _carrier_endpoint_paths(carrier: object, endpoint: Literal["source", "target"]) -> frozenset[str]:
    """Return native carrier endpoint paths without resolving a local name globally."""

    value = getattr(carrier, endpoint, None)
    owner_path = getattr(carrier, "owner_path", None)
    if not isinstance(value, str) or value == "[*]":
        return frozenset()
    paths = {value}
    if isinstance(owner_path, str) and owner_path:
        paths.add(f"{owner_path}.{value}")
    return frozenset(paths)


def _carrier_starts_at(carrier: object, state: object) -> bool:
    """Check native carrier origin against one native canonical state path."""

    return state_path(state) in _carrier_endpoint_paths(carrier, "source")


def _carrier_ends_at(carrier: object, state: object) -> bool:
    """Check native carrier target against one native canonical state path."""

    return state_path(state) in _carrier_endpoint_paths(carrier, "target")


def _native_transition_refs_for_contract(
    pair: PairInput,
    contract: NLContract,
    candidate: CandidateIssue,
    grounding: Sequence[GroundingResponse],
) -> tuple[str, ...]:
    """Collect only exact current-pair transition carriers for native route closure."""

    values: list[str] = [
        reference
        for reference in candidate.element_refs
        if reference in pair.model.transition_refs
    ]
    supplied = candidate.predicate_inputs.get("transition") or candidate.predicate_inputs.get("transition_ref")
    if isinstance(supplied, str):
        values.append(supplied)
    values.extend(
        binding.carrier_transition_ref
        for response in grounding
        for binding in response.semantic_bindings
        if binding.contract_id == contract.contract_id
        and binding.status == "exact"
        and binding.carrier_transition_ref in pair.model.transition_refs
    )
    resolved = {
        resolve_transition_ref(value, pair.model)
        for value in _unique_strings(values)
    }
    resolved.discard(None)
    return tuple(sorted(resolved))


def build_r1_cold_runtime_scenario(
    pair: PairInput,
    transition: Transition,
    event_name: str,
) -> dict[str, object] | None:
    """Construct one method-owned R1 scenario only for a unique native cold path.

    The returned schedule is not a copied source trace.  It is a fresh input to
    ``SimulationRuntime`` whose root, event path, transition carrier, and
    before/after state paths all come from the loaded FCSTM model classes.
    """

    if pair.canonical_source_ir is None or pair.canonical_source_ir.model.concurrent_regions:
        return None
    try:
        native = load_native_fcstm(pair.model)
    except Exception:
        return None
    root = native.machine.root_state
    root_path = state_path(root)
    source_node = _state_for_ref(pair, transition.source_ref)
    target_node = _state_for_ref(pair, transition.target_ref)
    source = resolve_state(native, source_node.canonical_path) if source_node else None
    target = resolve_state(native, target_node.canonical_path) if target_node else None
    event_path = next(
        (
            item.canonical_path
            for item in pair.model.events
            if item.ref in transition.trigger_refs
        ),
        event_name,
    )
    event = resolve_event(native, event_path)
    carrier = transition_by_ref(native, transition.ref)
    if (
        source is None
        or target is None
        or event is None
        or carrier is None
        or getattr(source, "parent", None) is not root
        or getattr(target, "parent", None) is not root
        or carrier.event is not event
        or carrier.guard is not None
        or not _carrier_starts_at(carrier, source)
        or not _carrier_ends_at(carrier, target)
        or getattr(carrier, "owner_path", None) != root_path
    ):
        return None
    if any(getattr(state, "parent", None) is source for state in all_states(native)):
        return None
    initial_rows = [
        row
        for row in all_transition_carriers(native)
        if row.source == "[*]"
        and _carrier_ends_at(row, source)
        and row.event is None
        and row.guard is None
        and row.owner_path == root_path
    ]
    same_event_rows = [
        row
        for row in all_transition_carriers(native)
        if _carrier_starts_at(row, source)
        and row.event is event
        and row.guard is None
        and row.owner_path == root_path
    ]
    if len(initial_rows) != 1 or len(same_event_rows) != 1:
        return None
    event_path = event.path_name
    return {
        "schema": "evidence-discovery.fcstm-runtime-scenario.v2",
        "initialization": "cold",
        "root_state": root_path,
        "expected_active_before": state_path(source),
        "expected_active_after": state_path(target),
        "event_queue": [event_path],
        "schedule": [
            {"step": 0, "event_paths": []},
            {"step": 1, "event_paths": [event_path]},
        ],
        "selected_step": 1,
        "selected_event_path": event_path,
        "selected_transition_ref": transition.ref,
        "reason": "A unique native FCSTM cold entry and one exact unguarded event carrier determine the complete R1 macrostep schedule.",
        "basis": (
            f"native_root={root_path}; initial_transition_line={initial_rows[0].source_line}; "
            f"source={state_path(source)}; target={state_path(target)}; "
            f"event={event_path}; transition_ref={transition.ref}; "
            "pyfcstm.model.StateMachine native carrier identity"
        ),
    }


def _cold_retention_scenario(
    pair: PairInput,
    contract: NLContract,
    state: StateNode,
) -> tuple[dict[str, object] | None, list[int] | None, str]:
    """Build R4 from a typed cold window or one native cold-entry fragment.

    A ``window`` binding hint normally preserves the natural-language temporal
    qualification (for example, ``while nearing the destination``).  It is not
    itself a runtime input.  Only the method's exact ``cold`` /
    ``cold_macrosteps=N`` vocabulary opts into the source-declared runtime
    fragment.  Generic prose therefore cannot manufacture an interval, but it
    also cannot prevent the separate, conservative native cold-entry closure.
    """

    scenarios = _contract_values(contract, {"scenario"})
    windows = _contract_values(contract, {"window"})
    has_typed_cold_window = (
        "cold" in scenarios
        or any(value.startswith("cold_macrosteps=") for value in windows)
    )
    if has_typed_cold_window:
        if scenarios != ("cold",) or len(windows) != 1:
            return None, None, "R4 source-declared runtime execution requires exactly scenario=cold and window=cold_macrosteps=N; incomplete typed control hints cannot select a runtime interval."
        match = _COLD_MACROSTEP_WINDOW.fullmatch(windows[0])
        if match is None:
            return None, None, "R4 accepts only the explicit finite window spelling cold_macrosteps=N; malformed typed control hints cannot select a runtime interval."
        count = int(match.group("count"))
        if count > _MAX_COLD_MACROSTEPS:
            return None, None, f"R4 cold window exceeds the method-owned bounded scenario fragment of {_MAX_COLD_MACROSTEPS} macrosteps."
        try:
            native = load_native_fcstm(pair.model)
        except Exception as exc:
            return None, None, f"R4 could not load the current FCSTM native model for scenario closure: {type(exc).__name__}."
        native_state = resolve_state(native, state.canonical_path)
        if native_state is None:
            return None, None, "R4 exact state binding does not resolve to one native FCSTM state."
        root_path = state_path(native.machine.root_state)
        return (
            {
                "schema": "evidence-discovery.fcstm-runtime-scenario.v2",
                "initialization": "cold",
                "root_state": root_path,
                "event_queue": [],
                "schedule": [
                    {"step": step, "event_paths": []}
                    for step in range(count)
                ],
                "reason": "The requirement explicitly declares a finite cold-start observation window, so the method owns a no-injected-event native runtime scenario rather than reusing a source trace.",
                "basis": (
                    f"state_ref={state.ref}; native_state={state_path(native_state)}; "
                    f"native_root={root_path}; source_window={windows[0]!r}; "
                    "pyfcstm.model.StateMachine cold initialization"
                ),
            },
            [0, count - 1],
            "R4 closed cold-start scenario and inclusive interval are fully materialized from the declared finite source window.",
        )

    return _cold_entry_quiescence_scenario(pair, state)


def _native_active_paths(runtime: object) -> tuple[str, ...]:
    """Read canonical active paths from one native runtime configuration."""

    if bool(getattr(runtime, "is_ended", False)):
        return ()
    current_state = getattr(runtime, "current_state", None)
    path = getattr(current_state, "path", ())
    parts = tuple(str(item) for item in path)
    return tuple(".".join(parts[:index]) for index in range(1, len(parts) + 1))


def _run_native_event_prefix(native: object, event_paths: tuple[str, ...]) -> tuple[tuple[str, ...] | None, str | None]:
    """Run a cold native event prefix, rejecting unconsumed or failed inputs."""

    try:
        from pyfcstm.simulate import SimulationRuntime

        runtime = SimulationRuntime(native.machine, abstract_error_mode="log")
        runtime.cycle([])
        for event_path in event_paths:
            result = runtime.cycle([event_path])
            if tuple(result.consumed_events) != (event_path,) or result.unconsumed_events:
                return None, "an entry-prefix event was not uniquely consumed by native SimulationRuntime"
        if runtime.is_ended:
            return None, "the native cold entry prefix reached a terminal configuration"
        return _native_active_paths(runtime), None
    except Exception as exc:  # noqa: BLE001 - no runtime failure becomes a verdict.
        return None, f"native SimulationRuntime failed while replaying the cold entry prefix: {type(exc).__name__}"


def _cold_entry_quiescence_scenario(
    pair: PairInput,
    state: StateNode,
) -> tuple[dict[str, object] | None, list[int] | None, str]:
    """Close one bounded R4 trace from a unique native cold entry path.

    A retention contract supplies the target state.  This fragment searches only
    short, single-event native runtime prefixes, accepts exactly one shortest
    path that enters that state, and appends one empty macrostep.  The route
    never derives events from source text, a fixture, or an evaluation artifact.
    Multiple paths leave the scenario open instead of selecting a convenient
    counterexample.
    """

    try:
        native = load_native_fcstm(pair.model)
    except Exception as exc:
        return None, None, f"R4 could not load the current FCSTM native model for cold-entry closure: {type(exc).__name__}."
    native_state = resolve_state(native, state.canonical_path)
    if native_state is None:
        return None, None, "R4 exact state binding does not resolve to one native FCSTM state."
    event_paths = tuple(sorted(event.path_name for event in all_events(native)))
    if len(event_paths) > _MAX_R4_EVENT_VOCABULARY:
        return None, None, f"R4 cold-entry fragment refuses an event vocabulary larger than {_MAX_R4_EVENT_VOCABULARY}; no arbitrary schedule is selected."
    target_path = state_path(native_state)
    selected: tuple[str, ...] | None = None
    for length in range(_MAX_R4_ENTRY_EVENTS + 1):
        matches: list[tuple[str, ...]] = []
        for prefix in product(event_paths, repeat=length):
            active_paths, failure = _run_native_event_prefix(native, prefix)
            if failure is None and active_paths is not None and target_path in active_paths:
                matches.append(prefix)
        if len(matches) == 1:
            selected = matches[0]
            break
        if len(matches) > 1:
            return None, None, "R4 cold-entry fragment found multiple shortest native event prefixes for the retained state, so it cannot choose a schedule."
    if selected is None:
        return None, None, f"R4 cold-entry fragment found no unique native event prefix of at most {_MAX_R4_ENTRY_EVENTS} macrosteps for the exact retained state."
    active_after_entry, failure = _run_native_event_prefix(native, selected)
    if failure is not None or active_after_entry is None or target_path not in active_after_entry:
        return None, None, f"R4 native entry-prefix replay did not close the exact retained state: {failure or 'target absent'}"
    schedule = [
        {"step": 0, "event_paths": []},
        *(
            {"step": index, "event_paths": [event_path]}
            for index, event_path in enumerate(selected, start=1)
        ),
        {"step": len(selected) + 1, "event_paths": []},
    ]
    return (
        {
            "schema": "evidence-discovery.fcstm-runtime-scenario.v2",
            "initialization": "cold",
            "root_state": state_path(native.machine.root_state),
            "event_queue": list(selected),
            "schedule": schedule,
            "reason": "The exact retained state has one shortest native cold-entry event prefix, followed by one no-injected-event macrostep. This is a method-owned runtime input, not a source trace.",
            "basis": (
                f"state_ref={state.ref}; native_state={target_path}; native_root={state_path(native.machine.root_state)}; "
                f"entry_event_prefix={list(selected)}; prefix_bound={_MAX_R4_ENTRY_EVENTS}; "
                "pyfcstm SimulationRuntime cold replay and unique shortest-prefix enumeration"
            ),
        },
        [len(selected), len(selected) + 1],
        "R4 closed a unique native cold-entry prefix and one subsequent zero-event macrostep for the exact retained state.",
    )


def _finite_domain_from_contract(contract: NLContract) -> tuple[dict[str, object] | None, str]:
    """Read exactly one independently declared finite-domain JSON value."""

    domains = _contract_values(contract, {"domain"})
    if len(domains) != 1:
        return None, "V1 requires one independently requirement-declared finite domain; the backend must not infer a domain from guards or variables."
    try:
        domain = json.loads(domains[0])
    except json.JSONDecodeError:
        return None, "V1 finite domain must be one exact JSON object; prose or an unparsed token is not a typed domain."
    if not isinstance(domain, dict) or not domain:
        return None, "V1 finite domain JSON must be a non-empty object keyed by native variable name."
    return domain, "exact source-side finite-domain JSON"


def _v1_native_choice_inputs(
    pair: PairInput,
    contract: NLContract,
    candidate: CandidateIssue,
    grounding: Sequence[GroundingResponse],
    source: StateNode,
) -> tuple[dict[str, object] | None, tuple[str, ...], str]:
    """Close V1 through one native choice group and a source-declared domain."""

    domain, domain_basis = _finite_domain_from_contract(contract)
    if domain is None:
        return None, (), domain_basis
    trigger_values = _contract_values(contract, {"trigger", "event"})
    if len(trigger_values) > 1:
        return None, (), "V1 requires at most one exact shared trigger; competing source-side trigger hints leave the choice group open."
    refs = _native_transition_refs_for_contract(pair, contract, candidate, grounding)
    if len(refs) < 2:
        return None, (), "V1 requires at least two exact transition carriers from one grounded choice group."
    try:
        native = load_native_fcstm(pair.model)
    except Exception as exc:
        return None, (), f"V1 could not load the current FCSTM native model for choice-group closure: {type(exc).__name__}."
    native_source = resolve_state(native, source.canonical_path)
    if native_source is None:
        return None, (), "V1 exact source binding does not resolve to one native FCSTM state."
    event = resolve_event(native, trigger_values[0]) if trigger_values else None
    if trigger_values and event is None:
        return None, (), "V1 exact source-side trigger does not resolve to one native FCSTM event."
    rows = tuple(
        (ordinal, row)
        for ordinal, row in enumerate(all_transition_carriers(native), start=1)
        if _carrier_starts_at(row, native_source)
        and row.event is event
        and row.guard is not None
        and row.source_line is not None
    )
    group_refs = tuple(
        sorted(
            transition_carrier_reference(row, ordinal)
            for ordinal, row in rows
        )
    )
    if len(rows) < 2 or group_refs != refs:
        return None, (), "V1 requires the exact grounded carrier set to equal one complete native same-source/same-event guarded choice group."
    guards = tuple(str(row.guard.to_ast_node()) for _ordinal, row in rows)
    if len(guards) < 2:
        return None, (), "V1 native choice group has fewer than two exact guard ASTs."
    return (
        {
            "source": state_path(native_source),
            "trigger": event.path_name if event is not None else None,
            "domain": domain,
            "guards": list(guards),
        },
        (source.ref, *group_refs),
        (
            f"native_source={state_path(native_source)}; native_trigger={event.path_name if event is not None else None}; "
            f"transition_refs={list(group_refs)}; guards={list(guards)}; domain={domain_basis}"
        ),
    )


def _routed_candidate(
    candidate: CandidateIssue,
    predicate_id: PredicateId,
    inputs: Mapping[str, object],
    required_refs: Sequence[str],
    *,
    reason: str,
    basis: str,
) -> CandidateIssue:
    """Fill one candidate's executable fields without changing semantic identity."""

    refs = list(candidate.element_refs)
    for reference in required_refs:
        if reference not in refs:
            refs.append(reference)
    return candidate.model_copy(
        update={
            "predicate_id": predicate_id,
            "predicate_inputs": dict(inputs),
            "element_refs": refs,
            "reason": candidate.reason + " " + reason,
            "basis": candidate.basis + "; " + basis,
        }
    )


def _route_candidate(
    pair: PairInput,
    contract: NLContract,
    candidate: CandidateIssue,
    grounding: Sequence[GroundingResponse],
) -> tuple[CandidateIssue, PredicateId | None, str, str]:
    """Route one predicate-null primary candidate only when inputs close exactly."""

    if candidate.predicate_id is not None:
        return candidate, candidate.predicate_id, "The candidate already selected a frozen predicate before primary routing.", "existing typed candidate route"
    if candidate.property != contract.property:
        return candidate, None, "Candidate property differs from its typed contract, so routing cannot repair the mismatch.", "exact contract property equality"

    property_name = contract.property
    if property_name == "initial_entry":
        owner, owner_basis = _state_for_roles(pair, contract, grounding, {"owner", "scope"})
        target, target_basis = _state_for_roles(pair, contract, grounding, {"target", "state"})
        if owner is None or target is None:
            return candidate, None, "S2 initial-entry routing requires one exact owner and one exact target state.", f"owner={owner_basis}; target={target_basis}"
        return (
            _routed_candidate(candidate, "S2", {"source": "[*]", "target": target.canonical_path, "scope": owner.canonical_path}, (owner.ref, target.ref), reason="The primary route bound the required owner-local initial pseudo-state endpoint without inferring a carrier from prose.", basis=f"predicate=S2; owner_ref={owner.ref}; target_ref={target.ref}; owner={owner_basis}; target={target_basis}"),
            "S2",
            "S2 initial-entry inputs close through exact owner and target bindings.",
            f"owner_ref={owner.ref}; target_ref={target.ref}",
        )

    if property_name == "transition_endpoints":
        source, source_basis = _state_for_roles(pair, contract, grounding, {"source"})
        target, target_basis = _state_for_roles(pair, contract, grounding, {"target"})
        if source is None or target is None:
            return candidate, None, "S2 endpoint routing requires one exact source and one exact target state.", f"source={source_basis}; target={target_basis}"
        scope, scope_basis = _scope_for_endpoint(pair, contract, source)
        if scope is None:
            return candidate, None, "S2 endpoint routing requires one exact transition owner scope.", scope_basis
        return (
            _routed_candidate(candidate, "S2", {"source": source.canonical_path, "target": target.canonical_path, "scope": scope}, (source.ref, target.ref), reason="The primary route bound an exact source, target, and owner scope for the frozen transition-existence predicate.", basis=f"predicate=S2; source_ref={source.ref}; target_ref={target.ref}; scope={scope}; source={source_basis}; target={target_basis}; scope={scope_basis}"),
            "S2",
            "S2 endpoint inputs close through exact source, target, and owner scope bindings.",
            f"source_ref={source.ref}; target_ref={target.ref}; scope={scope}",
        )

    if property_name == "trigger_set":
        transition, transition_basis = _transition_for_candidate(pair, contract, candidate, grounding)
        triggers = _contract_values(contract, {"trigger", "event"})
        if transition is None or not triggers:
            return candidate, None, "S3 routing requires one exact carrier and an explicit required trigger set.", f"carrier={transition_basis}; trigger_values={list(triggers)}"
        return (
            _routed_candidate(candidate, "S3", {"transition": transition.ref, "triggers": list(triggers)}, (transition.ref,), reason="The primary route bound the exact transition carrier and requirement-side trigger set for native S3 equality.", basis=f"predicate=S3; transition_ref={transition.ref}; triggers={list(triggers)}; carrier={transition_basis}"),
            "S3",
            "S3 trigger-set inputs close through one carrier and explicit typed trigger values.",
            f"transition_ref={transition.ref}; triggers={list(triggers)}",
        )

    if property_name == "state_action":
        state, state_basis = _state_for_roles(pair, contract, grounding, {"state"})
        phases = _contract_values(contract, {"phase"})
        actions = _contract_values(contract, {"action"})
        if state is None or len(phases) != 1 or phases[0] not in {"entry", "do", "exit"} or len(actions) != 1:
            return candidate, None, "S4 routing requires one exact state, phase in entry/do/exit, and one exact action.", f"state={state_basis}; phases={list(phases)}; actions={list(actions)}"
        return (
            _routed_candidate(candidate, "S4", {"state": state.canonical_path, "phase": phases[0], "action": actions[0]}, (state.ref,), reason="The primary route admitted S4 only after state, lifecycle slot, and action each closed as separate typed inputs.", basis=f"predicate=S4; state_ref={state.ref}; phase={phases[0]}; action={actions[0]}; state={state_basis}"),
            "S4",
            "S4 lifecycle inputs close through separate exact state, phase, and action values.",
            f"state_ref={state.ref}; phase={phases[0]}; action={actions[0]}",
        )

    if property_name in {"guard", "effect"}:
        transition, transition_basis = _transition_for_candidate(pair, contract, candidate, grounding)
        values = _contract_values(contract, {property_name})
        if transition is None or len(values) != 1:
            predicate = "S5" if property_name == "guard" else "S6"
            return candidate, None, f"{predicate} routing requires one exact transition carrier and one exact required {property_name} value.", f"carrier={transition_basis}; values={list(values)}"
        predicate = "S5" if property_name == "guard" else "S6"
        input_key = "guard" if predicate == "S5" else "effect"
        value: object = values[0] if predicate == "S5" else [values[0]]
        if predicate == "S6":
            try:
                native = load_native_fcstm(pair.model)
            except Exception as exc:  # noqa: BLE001 - preserve the precise W1 path.
                return candidate, None, "S6 routing cannot close the native effect operation because the current FCSTM model did not load.", f"carrier={transition_basis}; native_load={type(exc).__name__}"
            if transition_by_ref(native, transition.ref) is None:
                return candidate, None, "S6 routing requires an exact transition carrier that resolves through native FCSTM provenance.", f"transition_ref={transition.ref}; native_transition_resolution=false"
            if parse_effect_operation(native, values[0]) is None:
                return candidate, None, "S6 routing retains the precise effect candidate because its requirement-side value is not one exact native FCSTM operation.", f"transition_ref={transition.ref}; input_contract_missing/out_of_fragment: native effect operation parser rejected {values[0]!r}"
        return (
            _routed_candidate(candidate, predicate, {"transition": transition.ref, input_key: value}, (transition.ref,), reason=f"The primary route bound one exact transition carrier and one requirement-side {property_name} value for native AST comparison.", basis=f"predicate={predicate}; transition_ref={transition.ref}; {property_name}={values[0]!r}; carrier={transition_basis}"),
            predicate,
            f"{predicate} inputs close through one exact carrier and one typed {property_name} value.",
            f"transition_ref={transition.ref}; {property_name}={values[0]!r}",
        )

    if property_name == "reachability":
        source_values = _contract_values(contract, {"source", "root"})
        target, target_basis = _state_for_roles(pair, contract, grounding, {"target", "state"})
        source: str | None = "[*]" if source_values == ("[*]",) else None
        if source is None and len(source_values) == 1:
            source_state, source_basis = _state_for_roles(pair, contract, grounding, {"source", "root"})
            source = source_state.canonical_path if source_state is not None else None
        else:
            source_basis = "explicit root pseudostate" if source is not None else "missing source"
        if source is None or target is None:
            return candidate, None, "G1 routing requires one exact source/root and one exact target state.", f"source={source_basis}; target={target_basis}"
        refs = [target.ref]
        if source != "[*]":
            source_ref = resolve_state_ref(source, pair.model)
            if source_ref is not None:
                refs.append(source_ref)
        return (
            _routed_candidate(candidate, "G1", {"source": source, "target": target.canonical_path}, refs, reason="The primary route bound exact finite reachability endpoints without converting labels or names into graph facts.", basis=f"predicate=G1; source={source}; target_ref={target.ref}; source={source_basis}; target={target_basis}"),
            "G1",
            "G1 finite reachability inputs close through exact endpoint bindings.",
            f"source={source}; target_ref={target.ref}",
        )

    if property_name == "event_consumption":
        transition, transition_basis = _transition_for_candidate(
            pair, contract, candidate, grounding
        )
        events = _contract_values(contract, {"event", "trigger"})
        event_rows = [
            event
            for event in pair.model.events
            if len(events) == 1 and events[0] in {event.name, event.display_name}
        ]
        if transition is None or len(event_rows) != 1:
            return candidate, None, "R1 routing requires one exact event requirement and one exact transition carrier.", f"carrier={transition_basis}; event_values={list(events)}; resolved_events={[event.ref for event in event_rows]}"
        scenario = build_r1_cold_runtime_scenario(pair, transition, event_rows[0].canonical_path)
        if scenario is None:
            return candidate, None, "R1 routing could not close a unique native cold-start macrostep without inventing a schedule, guard valuation, or event identity.", f"carrier={transition.ref}; event_ref={event_rows[0].ref}; pyfcstm native cold-runtime scenario fragment"
        return (
            _routed_candidate(candidate, "R1", {"scenario": scenario, "event": event_rows[0].canonical_path, "step": 1}, (transition.ref, event_rows[0].ref), reason="The primary route materialized a method-owned native FCSTM cold-start macrostep from the exact event and carrier.", basis=f"predicate=R1; transition_ref={transition.ref}; event_ref={event_rows[0].ref}; scenario_basis={scenario['basis']}"),
            "R1",
            "R1 event-consumption inputs close through one exact native event carrier and a unique cold-start runtime scenario.",
            f"transition_ref={transition.ref}; event_ref={event_rows[0].ref}",
        )

    if property_name == "state_retention":
        state, state_basis = _state_for_roles(pair, contract, grounding, {"state"})
        if state is None:
            return candidate, None, "R4 routing requires one exact state binding before constructing a finite runtime interval.", f"state={state_basis}"
        scenario, interval, scenario_reason = _cold_retention_scenario(pair, contract, state)
        if scenario is None or interval is None:
            return candidate, None, "R4 routing retains the precise temporal candidate because its method-owned scenario/interval input contract is not closed.", f"state_ref={state.ref}; input_contract_missing/out_of_fragment: {scenario_reason}"
        return (
            _routed_candidate(candidate, "R4", {"scenario": scenario, "state": state.canonical_path, "interval": interval}, (state.ref,), reason="The primary route materialized an explicit finite cold-start retention interval and delegates every trace point to native SimulationRuntime.", basis=f"predicate=R4; state_ref={state.ref}; interval={interval}; scenario_basis={scenario['basis']}"),
            "R4",
            "R4 state-retention inputs close through an explicit finite cold-start source window and native runtime scenario.",
            f"state_ref={state.ref}; interval={interval}",
        )

    if property_name == "guard_disjointness":
        source, source_basis = _state_for_roles(pair, contract, grounding, {"source"})
        if source is None:
            return candidate, None, "V1 routing requires one exact source state for the native same-choice-group closure.", f"source={source_basis}"
        inputs, refs, choice_basis = _v1_native_choice_inputs(
            pair, contract, candidate, grounding, source
        )
        if inputs is None:
            return candidate, None, "V1 routing retains the precise guard-disjointness candidate because an exact native choice group or independently declared finite domain is not closed.", f"source_ref={source.ref}; input_contract_missing/out_of_fragment: {choice_basis}"
        return (
            _routed_candidate(candidate, "V1", inputs, refs, reason="The primary route bound the complete native same-source/same-event guard group and a requirement-declared finite JSON domain without Python guard evaluation.", basis=f"predicate=V1; {choice_basis}"),
            "V1",
            "V1 guard-disjointness inputs close through one complete native choice group and an independent finite domain.",
            choice_basis,
        )

    if property_name == "deadlock_freedom":
        state_refs = [ref for ref in candidate.element_refs if _state_for_ref(pair, ref) is not None]
        if len(set(state_refs)) != 1:
            return candidate, None, "V4 routing requires one exact reachable nonterminal state scope; the candidate binds zero or multiple state loci.", f"state_refs={state_refs}"
        state = _state_for_ref(pair, state_refs[0])
        fact = next((item for item in (pair.inspection_facts.states if pair.inspection_facts else ()) if item.state_ref == state.ref), None)
        if state is None or fact is None or not fact.reachable_from_initial:
            return candidate, None, "V4 routing requires an exact state confirmed reachable in current closed-model facts.", f"state_ref={state_refs[0]}; inspection_reachable={fact.reachable_from_initial if fact else None}"
        return (
            _routed_candidate(candidate, "V4", {"initial_scope": state.canonical_path}, (state.ref,), reason="The primary route selected V4 only for one exact closed-model state that the method-visible finite inspection marks reachable.", basis=f"predicate=V4; initial_scope_ref={state.ref}; inspection_reachable=true"),
            "V4",
            "V4 deadlock-freedom inputs close through one exact reachable state scope.",
            f"initial_scope_ref={state.ref}",
        )

    return candidate, None, "No primary binder closes every typed input for this property in the current pair.", f"property={property_name}; applicable={list(_PROPERTY_PREDICATES.get(property_name, ()))}"


def route_primary_candidates(
    pair: PairInput,
    contracts_by_id: Mapping[str, NLContract],
    grounding: Sequence[GroundingResponse],
    candidates: Sequence[CandidateIssue],
) -> PrimaryRouteProjection:
    """Route current primary candidates without changing contract semantic keys.

    Predicate-null candidates are augmented only by a route whose full typed
    input set closes deterministically.  Existing S4/S6 selections are also
    rebuilt through that route: an LLM predicate label and its raw values never
    bypass native lifecycle-slot or operation parsing.  Unsupported properties
    retain their precise W1 path and a machine-readable reason.
    """

    updated: list[CandidateIssue] = []
    outcomes: dict[str, tuple[PredicateId | None, str, str]] = {}
    for candidate in candidates:
        contract = contracts_by_id.get(candidate.contract_id)
        if contract is None:
            updated.append(candidate)
            continue
        strict_rebind = candidate.predicate_id in _STRICT_REBIND_PREDICATES
        route_input = (
            candidate.model_copy(update={"predicate_id": None})
            if strict_rebind
            else candidate
        )
        routed, selected, reason, basis = _route_candidate(
            pair, contract, route_input, grounding
        )
        if strict_rebind and selected != candidate.predicate_id:
            selected_predicate = str(candidate.predicate_id)
            routed = candidate.model_copy(
                update={
                    "predicate_id": None,
                    "predicate_inputs": {},
                    "reason": (
                        candidate.reason
                        + " The preselected "
                        + selected_predicate
                        + " label was removed because strict primary rebinding did not close legal native inputs."
                    ),
                    "basis": (
                        candidate.basis
                        + "; strict-primary-rebinding="
                        + selected_predicate
                        + "; "
                        + basis
                    ),
                }
            )
            reason = (
                f"The preselected {selected_predicate} candidate remains a precise semantic candidate, "
                "but strict primary rebinding did not close executable native inputs: "
                + reason
            )
            basis = basis + "; raw selected predicate inputs were not admitted as an execution plan"
        updated.append(routed)
        if candidate.contract_id not in outcomes or selected is not None:
            outcomes[candidate.contract_id] = (selected, reason, basis)

    telemetry: list[PredicateRouteTelemetry] = []
    for contract_id, contract in sorted(contracts_by_id.items()):
        applicable = _PROPERTY_PREDICATES.get(contract.property, ())
        selected, reason, basis = outcomes.get(
            contract_id,
            (
                None,
                "No candidate for this typed contract reached the primary route stage.",
                "contract candidate set after grounding/frontier admission",
            ),
        )
        telemetry.append(
            PredicateRouteTelemetry(
                contract_id=contract_id,
                applicable_predicates=applicable,
                route_attempted=True,
                selected_predicate=selected,
                binding_complete=selected is not None,
                backend=_PREDICATE_BACKENDS.get(selected) if selected is not None else None,
                reason=reason,
                basis=basis,
            )
        )
    return PrimaryRouteProjection(
        candidates=tuple(updated),
        telemetry=tuple(telemetry),
        reason="The deterministic primary route evaluated each typed contract and filled a predicate only after its current-pair typed inputs closed exactly.",
        basis="typed NL contracts, exact grounding bindings, closed ModelIR, and method-visible deterministic facts; no ledger, Judge, answer, or cross-pair input",
    )


def finalize_route_telemetry(
    telemetry: Sequence[PredicateRouteTelemetry],
    prepared_candidates: Sequence[Mapping[str, object]],
    witness_levels: Mapping[str, str],
) -> tuple[PredicateRouteTelemetry, ...]:
    """Attach compiled execution state and W result to primary-route telemetry.

    The runner supplies only local prepared candidate objects and deterministic
    witness levels.  This function never changes a route decision or derives a
    semantic D/publication outcome.
    """

    prepared_by_contract: dict[str, Mapping[str, object]] = {}
    for item in prepared_candidates:
        candidate = item.get("candidate")
        if not isinstance(candidate, CandidateIssue):
            continue
        if candidate.predicate_id is None:
            continue
        prepared_by_contract.setdefault(candidate.contract_id, item)
    result: list[PredicateRouteTelemetry] = []
    for row in telemetry:
        prepared = prepared_by_contract.get(row.contract_id)
        if prepared is None or row.selected_predicate is None:
            result.append(row)
            continue
        plan = prepared.get("plan")
        receipt = prepared.get("receipt")
        execution_state = getattr(receipt, "execution_state", None)
        if execution_state is None:
            terminal_state = getattr(receipt, "terminal_state", "unsupported")
            execution_state = "completed" if terminal_state == "completed" else "failed" if terminal_state in {"error", "timeout"} else "not_attempted"
        witness = witness_levels.get(str(prepared.get("obligation_id")))
        result.append(
            row.model_copy(
                update={
                    "binding_complete": bool(getattr(plan, "binding_complete", False)),
                    "backend": str(getattr(receipt, "backend", row.backend)) if getattr(receipt, "backend", None) else row.backend,
                    "execution_state": execution_state,
                    "final_W": witness if witness in {"W0", "W1", "W2"} else None,
                    "reason": row.reason + " Execution telemetry was attached from the local compiled plan and terminal receipt.",
                    "basis": row.basis + "; PredicatePlan, RawReceipt, and deterministic witness-level calculation",
                }
            )
        )
    return tuple(result)


__all__ = [
    "PredicateRouteTelemetry",
    "PrimaryRouteProjection",
    "build_r1_cold_runtime_scenario",
    "finalize_route_telemetry",
    "route_primary_candidates",
]
