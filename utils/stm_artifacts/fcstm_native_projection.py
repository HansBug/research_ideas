"""Native FCSTM loading and provenance-preserving projection primitives.

This module is the only FCSTM DSL entry point used by evidence discovery.
It deliberately delegates syntax, hierarchy, pseudo-state, transition, action,
and expression semantics to ``pyfcstm``.  Method code may project the native
objects into Pydantic records or run domain algorithms over their identities,
but it must not parse FCSTM source a second time.
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from typing import Any, Iterable

from pydantic import BaseModel, ConfigDict, Field


class NativeFCSTMDocument(BaseModel):
    """One pyfcstm-loaded FCSTM artifact with immutable source attribution."""

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    source_text: str = Field(min_length=1, description="Exact FCSTM text accepted by the native pyfcstm loader.")
    source_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 identity of the exact FCSTM source text.")
    algorithm_version: str = Field(default="pyfcstm.native-projection.v1", min_length=1, description="Version of the method-side projection over public pyfcstm objects.")
    machine: Any = Field(exclude=True, description="Native pyfcstm StateMachine; excluded from JSON artifacts because it is not a serializable method record.")


class NativeSourceLineAttribution(BaseModel):
    """Non-semantic source-line attribution joined to native FCSTM provenance.

    The working contract may retain an emitted source line for audit.  This
    record never parses that line as FCSTM; it only proves whether the exact
    text occurs once and which pyfcstm-authored carriers already expose that
    native source span.  A caller must still require one native carrier ref
    before using the result for a semantic decision.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    declared_line_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 hash of the working-contract source-line excerpt used only for attribution.")
    matching_source_lines: tuple[int, ...] = Field(default_factory=tuple, description="All one-based exact-text source lines in the native-loaded FCSTM artifact; semantic identity is not inferred from this tuple.")
    resolved_source_line: int | None = Field(default=None, ge=1, description="The sole exact-text source line when attribution is unique, otherwise null.")
    native_carrier_refs: tuple[str, ...] = Field(default_factory=tuple, description="Canonical refs of native authored carriers whose pyfcstm source span equals resolved_source_line.")
    reason: str = Field(min_length=1, description="Explanation of whether the source excerpt has unique non-semantic attribution and native provenance.")
    basis: str = Field(min_length=1, description="Native source hash, exact-text attribution count, and native carrier provenance basis.")


class NativeTransitionCarrier(BaseModel):
    """One authored transition carrier reconstructed solely from native provenance.

    Native objects remain excluded from JSON because this record is a live
    adapter for backend and binding code.  The serializable fields preserve the
    authored carrier identity, while all FCSTM semantics stay with pyfcstm.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, arbitrary_types_allowed=True)

    native_transitions: tuple[Any, ...] = Field(
        exclude=True,
        description="Native pyfcstm implementation transitions belonging to this one authored carrier; excluded from JSON audit projections.",
    )
    source: str = Field(min_length=1, description="Native authored-carrier source endpoint name, or [*] for an initial marker.")
    target: str = Field(min_length=1, description="Native authored-carrier target endpoint name, or [*] for an exit marker.")
    owner_path: str = Field(min_length=1, description="Canonical native owner-state path that scopes this authored carrier.")
    events: tuple[Any, ...] = Field(
        default_factory=tuple,
        exclude=True,
        description="Native pyfcstm event objects carried by the authored transition; excluded from JSON audit projections.",
    )
    guard: Any | None = Field(
        default=None,
        exclude=True,
        description="Native pyfcstm guard AST object, or null when the authored carrier has no guard.",
    )
    effects: tuple[Any, ...] = Field(
        default_factory=tuple,
        exclude=True,
        description="Native pyfcstm operation AST objects attached as exact effects; excluded from JSON audit projections.",
    )
    source_line: int | None = Field(default=None, ge=1, description="One-based native AST source span line for attribution, or null when unavailable.")
    combo_origin_id: str | None = Field(default=None, min_length=1, description="Native combo-transition origin identity, or null for a non-combo authored carrier.")
    forced_origin: str | None = Field(default=None, min_length=1, description="Native forced-transition provenance identity, or null for a non-forced authored carrier.")

    @property
    def event(self) -> Any | None:
        """Return the sole event only for a single-event carrier."""

        return self.events[0] if len(self.events) == 1 else None


class NativeFCSTMError(RuntimeError):
    """Raised when pyfcstm cannot form a native model for a closed artifact."""


@lru_cache(maxsize=256)
def _load_machine(source_text: str) -> Any:
    """Load exact FCSTM text through the public pyfcstm model loader."""

    from pyfcstm.model import load_state_machine_from_text

    return load_state_machine_from_text(source_text)


def load_native_document(source_text: str) -> NativeFCSTMDocument:
    """Load one FCSTM artifact once through pyfcstm without a local DSL parser."""

    if not isinstance(source_text, str) or not source_text.strip():
        raise NativeFCSTMError("FCSTM source must be a non-empty string")
    try:
        machine = _load_machine(source_text)
    except Exception as exc:  # noqa: BLE001 - callers record a structured input failure.
        raise NativeFCSTMError(
            f"pyfcstm could not load the closed FCSTM model: {type(exc).__name__}: {exc}"
        ) from exc
    return NativeFCSTMDocument(
        source_text=source_text,
        source_hash="sha256:" + hashlib.sha256(source_text.encode("utf-8")).hexdigest(),
        machine=machine,
    )


def state_path(state: Any) -> str:
    """Return one native state's canonical dotted path."""

    return ".".join(str(part) for part in state.path)


def all_states(document: NativeFCSTMDocument) -> tuple[Any, ...]:
    """Return all native states, including pseudo-states, in native traversal order."""

    return tuple(document.machine.walk_states())


def all_events(document: NativeFCSTMDocument) -> tuple[Any, ...]:
    """Return distinct declared native event objects in traversal order."""

    events: list[Any] = []
    seen: set[int] = set()
    for state in all_states(document):
        for event in state.events.values():
            if id(event) not in seen:
                events.append(event)
                seen.add(id(event))
    return tuple(events)


def all_transitions(document: NativeFCSTMDocument) -> tuple[Any, ...]:
    """Return native implementation transitions with their native owners intact."""

    return tuple(transition for state in all_states(document) for transition in state.transitions)


def transition_owner_path(transition: Any) -> str:
    """Return the canonical native owner path of one transition or carrier."""

    if isinstance(transition, NativeTransitionCarrier):
        return transition.owner_path
    if transition.parent is None:
        raise NativeFCSTMError("native transition has no owner state")
    return state_path(transition.parent)


def native_transition_endpoints(transition: Any) -> tuple[str, str]:
    """Render native transition endpoints while preserving initial/final markers."""

    if isinstance(transition, NativeTransitionCarrier):
        return transition.source, transition.target
    from pyfcstm.dsl import EXIT_STATE, INIT_STATE

    if transition.parent is None:
        raise NativeFCSTMError("native transition has no owner state")
    source = "[*]" if transition.from_state is INIT_STATE else str(transition.from_state)
    target = "[*]" if transition.to_state is EXIT_STATE else str(transition.to_state)
    return source, target


def _regular_transition_carrier(transition: Any) -> NativeTransitionCarrier:
    """Wrap one non-combo native transition as a provenance-preserving carrier."""

    source, target = native_transition_endpoints(transition)
    return NativeTransitionCarrier(
        native_transitions=(transition,),
        source=source,
        target=target,
        owner_path=transition_owner_path(transition),
        events=(transition.event,) if transition.event is not None else (),
        guard=transition.guard,
        effects=tuple(transition.effects),
        source_line=getattr(getattr(transition, "_span", None), "line", None),
        forced_origin=getattr(transition, "forced_origin", None),
    )


def _combo_transition_carriers(document: NativeFCSTMDocument) -> tuple[NativeTransitionCarrier, ...]:
    """Group generated combo edges by their public native origin provenance."""

    grouped: dict[str, list[Any]] = {}
    first_refs: dict[str, Any] = {}
    for transition in all_transitions(document):
        for origin_ref in getattr(transition, "combo_origin_refs", ()):
            grouped.setdefault(origin_ref.origin_id, []).append(transition)
            first_refs.setdefault(origin_ref.origin_id, origin_ref)
    carriers: list[NativeTransitionCarrier] = []
    for origin_id, transitions in grouped.items():
        terminal_edges = [
            transition
            for transition in transitions
            if any(
                ref.origin_id == origin_id and ref.role == "terminal"
                for ref in getattr(transition, "combo_origin_refs", ())
            )
        ]
        starts = [
            transition
            for transition in transitions
            if any(
                ref.origin_id == origin_id and ref.role == "prefix" and ref.term_index == 0
                for ref in getattr(transition, "combo_origin_refs", ())
            )
        ]
        if len(terminal_edges) != 1 or len(starts) != 1:
            continue
        terminal = terminal_edges[0]
        source, _ = native_transition_endpoints(starts[0])
        _, target = native_transition_endpoints(terminal)
        unique: list[Any] = []
        seen_transitions: set[int] = set()
        events: list[Any] = []
        seen_events: set[int] = set()
        for transition in transitions:
            if id(transition) not in seen_transitions:
                unique.append(transition)
                seen_transitions.add(id(transition))
            if transition.event is not None and id(transition.event) not in seen_events:
                events.append(transition.event)
                seen_events.add(id(transition.event))
        origin = first_refs[origin_id]
        carriers.append(
            NativeTransitionCarrier(
                native_transitions=tuple(unique),
                source=source,
                target=target,
                owner_path=transition_owner_path(terminal),
                events=tuple(events),
                guard=terminal.guard,
                effects=tuple(terminal.effects),
                source_line=getattr(origin.transition_span, "line", None),
                combo_origin_id=origin_id,
            )
        )
    return tuple(carriers)


def _forced_transition_carriers(document: NativeFCSTMDocument) -> tuple[NativeTransitionCarrier, ...]:
    """Recover one authored forced declaration from native forced provenance."""

    carriers: list[NativeTransitionCarrier] = []
    for declaration in document.machine.forced_transitions:
        from_path = declaration.get("from_path")
        to_path = declaration.get("to_path")
        original_raw = declaration.get("original_raw")
        span = declaration.get("span")
        if not all(isinstance(value, str) and value for value in (from_path, to_path, original_raw)):
            continue
        owner_path, _, source = from_path.rpartition(".")
        target = to_path.rsplit(".", 1)[-1]
        matches = [
            transition
            for transition in all_transitions(document)
            if getattr(transition, "is_forced", False)
            and getattr(transition, "forced_origin", None) == original_raw
            and transition_owner_path(transition) == owner_path
            and native_transition_endpoints(transition) == (source, target)
        ]
        if len(matches) != 1:
            continue
        transition = matches[0]
        carriers.append(
            NativeTransitionCarrier(
                native_transitions=(transition,),
                source=source,
                target=target,
                owner_path=owner_path,
                events=(transition.event,) if transition.event is not None else (),
                guard=transition.guard,
                effects=tuple(transition.effects),
                source_line=getattr(span, "line", None),
                forced_origin=original_raw,
            )
        )
    return tuple(carriers)


def all_transition_carriers(document: NativeFCSTMDocument) -> tuple[NativeTransitionCarrier, ...]:
    """Return native-authored transition carriers without flattening combo provenance."""

    regular = tuple(
        _regular_transition_carrier(transition)
        for transition in all_transitions(document)
        if not getattr(transition, "combo_origin_refs", ())
        and not getattr(transition, "is_forced", False)
    )
    return regular + _forced_transition_carriers(document) + _combo_transition_carriers(document)


def attribute_declared_source_line(
    document: NativeFCSTMDocument,
    declared_line: object,
) -> NativeSourceLineAttribution | None:
    """Bind one working-contract excerpt to native spans without DSL parsing.

    Exact text comparison is retained solely to attribute a published compiler
    member to the immutable source artifact.  The returned carrier refs are
    obtained from pyfcstm provenance; callers must reject zero or multiple refs
    instead of treating a source line as an FCSTM semantic identity.
    """

    if not isinstance(declared_line, str) or not declared_line.strip():
        return None
    source_lines = document.source_text.splitlines()
    matching_lines = tuple(
        line_no
        for line_no, line_text in enumerate(source_lines, start=1)
        if line_text.strip() == declared_line.strip()
    )
    resolved_line = matching_lines[0] if len(matching_lines) == 1 else None
    carriers = all_transition_carriers(document)
    carrier_refs = tuple(
        transition_carrier_reference(carrier, ordinal)
        for ordinal, carrier in enumerate(carriers, start=1)
        if resolved_line is not None and carrier.source_line == resolved_line
    )
    if resolved_line is None:
        reason = "The working-contract source excerpt is not uniquely attributable in the native-loaded FCSTM artifact."
    elif len(carrier_refs) == 1:
        reason = "The source excerpt is uniquely attributable and resolves to one pyfcstm-authored carrier ref."
    elif carrier_refs:
        reason = "The source excerpt is attributable but maps to multiple native carriers, so it is not a unique semantic identity."
    else:
        reason = "The source excerpt is attributable but does not name a native authored transition carrier."
    return NativeSourceLineAttribution(
        declared_line_sha256="sha256:" + hashlib.sha256(declared_line.encode("utf-8")).hexdigest(),
        matching_source_lines=matching_lines,
        resolved_source_line=resolved_line,
        native_carrier_refs=carrier_refs,
        reason=reason,
        basis=(
            f"fcstm_source_hash={document.source_hash}; matching_source_lines={list(matching_lines)}; "
            f"native_carrier_refs={list(carrier_refs)}"
        ),
    )


def native_variable_names(document: NativeFCSTMDocument) -> frozenset[str]:
    """Return declared FCSTM variable identities from the native StateMachine."""

    return frozenset(str(name) for name in document.machine.defines)


def resolve_state(document: NativeFCSTMDocument, value: object) -> Any | None:
    """Resolve a canonical path or an unambiguous local native state identity."""

    if not isinstance(value, str) or not value.strip():
        return None
    requested = value.strip()
    states = all_states(document)
    exact = [state for state in states if state_path(state) == requested]
    if len(exact) == 1:
        return exact[0]
    local = [state for state in states if state.name == requested]
    return local[0] if len(local) == 1 else None


def resolve_event(document: NativeFCSTMDocument, value: object) -> Any | None:
    """Resolve a canonical path or an unambiguous native event identity."""

    if not isinstance(value, str) or not value.strip():
        return None
    requested = value.strip()
    matches = [event for event in all_events(document) if requested in {event.name, event.path_name}]
    return matches[0] if len(matches) == 1 else None


def resolve_state_paths(document: NativeFCSTMDocument, values: Iterable[object]) -> tuple[str, ...] | None:
    """Resolve all state inputs without guessing a local-name collision."""

    resolved: list[str] = []
    for value in values:
        state = resolve_state(document, value)
        if state is None:
            return None
        resolved.append(state_path(state))
    return tuple(dict.fromkeys(resolved))


def transition_carrier_reference(carrier: NativeTransitionCarrier, ordinal: int) -> str:
    """Return the canonical method ref for one native authored carrier."""

    line = carrier.source_line if isinstance(carrier.source_line, int) and carrier.source_line >= 1 else ordinal
    if carrier.forced_origin:
        token = hashlib.sha256(carrier.forced_origin.encode("utf-8")).hexdigest()[:16]
        return f"transition:forced:{token}:line:{line}"
    if carrier.combo_origin_id:
        token = hashlib.sha256(carrier.combo_origin_id.encode("utf-8")).hexdigest()[:16]
        return f"transition:combo:{token}:line:{line}"
    return f"transition:line:{line}"


def transition_by_reference(document: NativeFCSTMDocument, reference: object) -> NativeTransitionCarrier | None:
    """Resolve a canonical or one-to-one legacy transition ref without guessing."""

    if not isinstance(reference, str) or not reference.startswith("transition:"):
        return None
    carriers = all_transition_carriers(document)
    canonical = [
        carrier
        for ordinal, carrier in enumerate(carriers, start=1)
        if transition_carrier_reference(carrier, ordinal) == reference
    ]
    if len(canonical) == 1:
        return canonical[0]
    if not reference.startswith("transition:line:"):
        return None
    line_text = reference.removeprefix("transition:line:")
    if not line_text.isdecimal():
        return None
    line = int(line_text)
    legacy = [carrier for carrier in carriers if carrier.source_line == line]
    return legacy[0] if len(legacy) == 1 else None


def native_assignment_pairs(carrier: NativeTransitionCarrier) -> frozenset[tuple[str, str]]:
    """Return literal assignment facts from native effect operation objects only."""

    pairs: set[tuple[str, str]] = set()
    for operation in carrier.effects:
        name = getattr(operation, "var_name", None)
        expression = getattr(operation, "expr", None)
        value = getattr(expression, "value", None)
        if isinstance(name, str) and isinstance(value, int):
            pairs.add((name, str(value)))
    return frozenset(pairs)


def native_guard_equality_pairs(carrier: NativeTransitionCarrier) -> frozenset[tuple[str, str]]:
    """Return variable-equals-integer facts from a native guard expression tree."""

    guard = carrier.guard
    left = getattr(guard, "x", None)
    right = getattr(guard, "y", None)
    operator = getattr(guard, "op", None)
    name = getattr(left, "name", None)
    value = getattr(right, "value", None)
    if operator == "==" and isinstance(name, str) and isinstance(value, int):
        return frozenset({(name, str(value))})
    return frozenset()
