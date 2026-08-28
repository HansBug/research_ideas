from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .fcstm_native_projection import (
    NativeFCSTMDocument,
    NativeTransitionCarrier,
    all_events,
    all_states,
    all_transition_carriers,
    load_native_document,
    state_path,
    transition_carrier_reference,
)


def _sha(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


class StateNode(BaseModel):
    """Native pyfcstm state projection with canonical and compatibility identities."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Native FCSTM local state identifier.")
    display_name: str = Field(min_length=1, description="Native FCSTM display label or the local state identifier.")
    canonical_path: str = Field(min_length=1, description="Native pyfcstm canonical dotted state path, which distinguishes local-name collisions.")
    parent: str | None = Field(default=None, min_length=1, description="Immediate native parent local name retained for compatibility displays, or null for the root state.")
    parent_ref: str | None = Field(default=None, min_length=1, description="Exact projected parent state reference, or null for the root state.")
    is_pseudo: bool = Field(description="Whether pyfcstm classifies this native state as a pseudo-state.")
    line: int = Field(ge=1, description="One-based native AST source line where this state declaration starts.")
    ref: str = Field(min_length=1, description="Stable canonical projection reference for binding and audit attribution.")
    legacy_refs: tuple[str, ...] = Field(default_factory=tuple, description="Historical state references that map uniquely and semantically identically to this native state.")
    actions: dict[str, tuple[str, ...]] = Field(default_factory=dict, description="Native lifecycle action identities grouped by entry, do, and exit slots.")


class EventNode(BaseModel):
    """Native pyfcstm event projection with canonical ownership identity."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Native FCSTM local event identifier.")
    display_name: str = Field(min_length=1, description="Native FCSTM display label or the local event identifier.")
    canonical_path: str = Field(min_length=1, description="Native pyfcstm canonical event path including its declaring state path.")
    line: int = Field(ge=1, description="One-based native AST source line where this event declaration starts.")
    ref: str = Field(min_length=1, description="Stable canonical projection reference for binding and audit attribution.")
    legacy_refs: tuple[str, ...] = Field(default_factory=tuple, description="Historical event references that map uniquely and semantically identically to this native event.")


class Transition(BaseModel):
    """Native authored-transition carrier projection with exact provenance."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source: str = Field(min_length=1, description="Native authored-carrier source endpoint name, or [*] for an initial marker.")
    target: str = Field(min_length=1, description="Native authored-carrier target endpoint name, or [*] for an exit marker.")
    source_ref: str | None = Field(default=None, min_length=1, description="Exact native-projected source state reference, or null for [*].")
    target_ref: str | None = Field(default=None, min_length=1, description="Exact native-projected target state reference, or null for [*].")
    label: str = Field(description="Deterministic presentation rendering from native event, guard, and effect AST objects; it is never reparsed as FCSTM.")
    triggers: tuple[str, ...] = Field(description="Exact native event local names carried by this authored transition.")
    trigger_refs: tuple[str, ...] = Field(default_factory=tuple, description="Exact native-projected event references carried by this authored transition.")
    guard: str | None = Field(default=None, min_length=1, description="Rendering of the native guard AST, or null when the carrier has no guard.")
    effects: tuple[str, ...] = Field(description="Renderings of native effect operation AST nodes in authored-carrier order.")
    line: int = Field(ge=1, description="One-based native provenance source line for this authored carrier.")
    ref: str = Field(min_length=1, description="Stable canonical projection reference for binding and audit attribution.")
    legacy_refs: tuple[str, ...] = Field(default_factory=tuple, description="Historical transition references that map uniquely and semantically identically to this native authored carrier.")
    scope: str | None = Field(default=None, min_length=1, description="Immediate native owner local name retained for compatibility displays, or null only when unavailable.")
    owner_ref: str | None = Field(default=None, min_length=1, description="Exact native-projected owner state reference for scope-sensitive predicates.")
    owner_path: str = Field(min_length=1, description="Canonical native owner state path for the authored carrier.")
    is_forced: bool = Field(default=False, description="Whether the carrier is an authored native forced-transition declaration.")
    combo_origin_id: str | None = Field(default=None, min_length=1, description="Native combo-origin group identity, or null for a non-combo carrier.")
    native_transition_count: int = Field(ge=1, description="Number of native implementation edges represented by this authored carrier.")


class ModelIR(BaseModel):
    """Compatibility projection derived exclusively from one native pyfcstm document."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    states: tuple[StateNode, ...] = Field(description="All native-projected states, including pseudo-states, in pyfcstm traversal order.")
    events: tuple[EventNode, ...] = Field(description="All native-projected event objects in pyfcstm traversal order.")
    transitions: tuple[Transition, ...] = Field(description="All authored native transition carriers in stable provenance order.")
    source_text: str = Field(description="Exact FCSTM source text accepted by pyfcstm; retained only for attribution and isolated native execution.")
    algorithm_version: str = Field(default="pyfcstm-native-projection.v1", min_length=1, description="Versioned native pyfcstm projection algorithm identifier used in evidence receipts.")

    @property
    def state_names(self) -> set[str]:
        return {state.name for state in self.states}

    @property
    def event_names(self) -> set[str]:
        return {event.name for event in self.events}

    @property
    def transition_refs(self) -> set[str]:
        return {transition.ref for transition in self.transitions}

    @property
    def all_refs(self) -> set[str]:
        return (
            {state.ref for state in self.states}
            | {event.ref for event in self.events}
            | self.transition_refs
        )

    @property
    def legacy_ref_map(self) -> dict[str, str]:
        """Return only one-to-one historical-reference compatibility mappings."""

        candidates: dict[str, list[str]] = {}
        for item in (*self.states, *self.events, *self.transitions):
            for legacy_ref in item.legacy_refs:
                candidates.setdefault(legacy_ref, []).append(item.ref)
        return {
            legacy_ref: refs[0]
            for legacy_ref, refs in candidates.items()
            if len(set(refs)) == 1
        }

    def normalize_ref(self, reference: str | None) -> str | None:
        """Resolve a canonical ref or a unique historical native-equivalent ref."""

        if reference in self.all_refs:
            return reference
        return self.legacy_ref_map.get(reference or "")

    def state(self, name: str) -> StateNode | None:
        exact = [state for state in self.states if name in {state.ref, state.canonical_path}]
        if len(exact) == 1:
            return exact[0]
        matches = [state for state in self.states if name in {state.name, state.display_name}]
        return matches[0] if len(matches) == 1 else None

    def event(self, name: str) -> EventNode | None:
        exact = [event for event in self.events if name in {event.ref, event.canonical_path}]
        if len(exact) == 1:
            return exact[0]
        matches = [event for event in self.events if name in {event.name, event.display_name}]
        return matches[0] if len(matches) == 1 else None

    def transition(self, ref: str | None) -> Transition | None:
        if not ref:
            return None
        normalized = self.normalize_ref(ref) or ref
        return next((item for item in self.transitions if item.ref == normalized), None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithm_version": self.algorithm_version,
            "source_hash": _sha(self.source_text),
            "states": [state.model_dump(mode="json") for state in self.states],
            "events": [event.model_dump(mode="json") for event in self.events],
            "transitions": [transition.model_dump(mode="json") for transition in self.transitions],
        }


class PairInput(BaseModel):
    """One frozen pair's complete method-visible input closure and native projection.

    The source text and closed FCSTM are kept as separate fields because they
    have different authority.  The additional context fields are populated by
    ``load_pair`` from the published representation artifacts and owned deterministic
    fact builders; a formal method run must not silently fall back to the old
    three-file input surface.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, arbitrary_types_allowed=True)

    pair_id: str = Field(min_length=1, description="Frozen pair identifier used for run partitioning and audit joins.")
    pair_dir: Path = Field(description="Resolved directory containing the pair's source artifacts.")
    nl_text: str = Field(description="Exact natural-language requirement artifact supplied to method generation.")
    fcstm_text: str = Field(description="Exact FCSTM artifact supplied to the pyfcstm native loader and method generation.")
    plantuml_text: str = Field(description="Exact PlantUML artifact supplied for source localization, if present.")
    model: ModelIR = Field(description="Compatibility projection derived only from the pyfcstm native FCSTM document.")
    hashes: dict[str, str] = Field(description="SHA-256 hashes for the source artifacts used by this pair.")
    nl_segments: tuple["NumberedNLSegment", ...] = Field(default_factory=tuple, description="Deterministically numbered NL segments supplied to contract extraction.")
    canonical_source_ir: "CanonicalSourceIR | None" = Field(default=None, description="Canonical author-source IR supplied for source localization; never treated as the FCSTM execution model.")
    exact_source_inventory: "ExactSourceInventory | None" = Field(default=None, description="Exact source state/transition inventory projected from canonical source IR.")
    working_contract: "StructuredArtifact | None" = Field(default=None, description="Published working contract containing mapping, ownership, and capability boundaries.")
    source_trace: "StructuredArtifact | None" = Field(default=None, description="Published source trace and attribution boundary artifact.")
    case_report: "StructuredArtifact | None" = Field(default=None, description="Published case report identity and artifact-hash record, excluding evaluation answers.")
    reference_inspection: "StructuredArtifact | None" = Field(default=None, description="Read-only inspection-derived fact artifact; it is context, never a new backend dependency.")
    inspection_facts: "InspectionEquivalentFacts | None" = Field(default=None, description="Owned deterministic inspection-equivalent inventory and diagnostics computed from the closed FCSTM.")
    verify_facts: "VerificationFacts | None" = Field(default=None, description="Owned finite verification fact summary supplied to grounding.")
    smt_facts: "SMTFacts | None" = Field(default=None, description="Owned normalized bounded-formula summary with an explicit no-solver boundary.")
    context_manifest: "ContextManifest | None" = Field(default=None, description="Hash- and versioned manifest of every artifact supplied to method/grounding.")

    def to_dict(self) -> dict[str, Any]:
        value: dict[str, Any] = {
            "pair_id": self.pair_id,
            "pair_dir": str(self.pair_dir),
            "hashes": dict(self.hashes),
            "model": self.model.to_dict(),
            "nl_segments": [item.model_dump(mode="json") for item in self.nl_segments],
            "context_manifest": self.context_manifest.model_dump(mode="json") if self.context_manifest else None,
        }
        if self.exact_source_inventory is not None:
            value["exact_source_inventory"] = self.exact_source_inventory.model_dump(mode="json")
        if self.inspection_facts is not None:
            value["inspection_facts"] = self.inspection_facts.model_dump(mode="json")
        if self.verify_facts is not None:
            value["verify_facts"] = self.verify_facts.model_dump(mode="json")
        if self.smt_facts is not None:
            value["smt_facts"] = self.smt_facts.model_dump(mode="json")
        return value


def _span_line(value: Any) -> int:
    """Return a native AST line with a non-zero audit fallback."""

    line = getattr(getattr(value, "_span", None), "line", None)
    return line if isinstance(line, int) and line >= 1 else 1


def _native_text(value: Any) -> str:
    """Render a native AST node for display without reparsing FCSTM source."""

    node = value.to_ast_node() if hasattr(value, "to_ast_node") else value
    return " ".join(str(node).strip().rstrip(";").split())


def _native_action_texts(actions: tuple[Any, ...] | list[Any]) -> tuple[str, ...]:
    """Project exact native lifecycle action identities for S4-facing context."""

    values: list[str] = []
    for action in actions:
        if getattr(action, "name", None):
            values.append(str(action.name))
        if not getattr(action, "is_abstract", False) and not getattr(action, "is_ref", False):
            values.extend(_native_text(operation) for operation in getattr(action, "operations", ()))
    return tuple(dict.fromkeys(value for value in values if value))


def _state_ref(state: Any) -> str:
    """Create a span-stable reference whose canonical path remains separately recorded."""

    return f"state:{state.name}:line:{_span_line(state)}"


def _event_ref(event: Any) -> str:
    """Create a span-stable event reference from one native event object."""

    return f"event:{event.name}:line:{_span_line(event)}"


def _carrier_label(triggers: tuple[str, ...], guard: str | None, effects: tuple[str, ...]) -> str:
    """Render native transition components for human context without source parsing."""

    parts = list(triggers)
    if guard:
        parts.append(f"[{guard}]")
    if effects:
        parts.append("effect { " + ", ".join(effects) + " }")
    return " ".join(parts)


def _project_native_document(document: NativeFCSTMDocument) -> ModelIR:
    """Project one native FCSTM document into the compatibility Pydantic interface."""

    native_states = all_states(document)
    state_refs_by_path = {state_path(state): _state_ref(state) for state in native_states}
    states = tuple(
        StateNode(
            name=str(state.name),
            display_name=str(state.extra_name or state.name),
            canonical_path=state_path(state),
            parent=str(state.parent.name) if state.parent is not None else None,
            parent_ref=state_refs_by_path.get(state_path(state.parent)) if state.parent is not None else None,
            is_pseudo=bool(state.is_pseudo),
            line=_span_line(state),
            ref=state_refs_by_path[state_path(state)],
            legacy_refs=(f"state:{state.name}:line:{_span_line(state)}",),
            actions={
                "entry": _native_action_texts(state.on_enters),
                "do": _native_action_texts(tuple(state.on_durings) + tuple(state.on_during_aspects)),
                "exit": _native_action_texts(state.on_exits),
            },
        )
        for state in native_states
    )
    native_events = all_events(document)
    event_refs_by_path = {event.path_name: _event_ref(event) for event in native_events}
    events = tuple(
        EventNode(
            name=str(event.name),
            display_name=str(event.extra_name or event.name),
            canonical_path=event.path_name,
            line=_span_line(event),
            ref=event_refs_by_path[event.path_name],
            legacy_refs=(f"event:{event.name}:line:{_span_line(event)}",),
        )
        for event in native_events
    )
    carriers = all_transition_carriers(document)
    line_counts: dict[int, int] = {}
    for carrier in carriers:
        line = carrier.source_line if isinstance(carrier.source_line, int) and carrier.source_line >= 1 else 0
        line_counts[line] = line_counts.get(line, 0) + 1
    transitions: list[Transition] = []
    for ordinal, carrier in enumerate(carriers, start=1):
        line = carrier.source_line if isinstance(carrier.source_line, int) and carrier.source_line >= 1 else ordinal
        ref = transition_carrier_reference(carrier, ordinal)
        owner_ref = state_refs_by_path.get(carrier.owner_path)
        owner = next((state for state in native_states if state_path(state) == carrier.owner_path), None)
        source_path = f"{carrier.owner_path}.{carrier.source}"
        target_path = f"{carrier.owner_path}.{carrier.target}"
        source_ref = None if carrier.source == "[*]" else state_refs_by_path.get(source_path)
        target_ref = None if carrier.target == "[*]" else state_refs_by_path.get(target_path)
        triggers = tuple(str(event.name) for event in carrier.events)
        trigger_refs = tuple(event_refs_by_path[event.path_name] for event in carrier.events if event.path_name in event_refs_by_path)
        guard = _native_text(carrier.guard) if carrier.guard is not None else None
        effects = tuple(_native_text(effect) for effect in carrier.effects)
        legacy_refs = (f"transition:line:{line}",) if line_counts.get(line) == 1 else ()
        transitions.append(
            Transition(
                source=carrier.source,
                target=carrier.target,
                source_ref=source_ref,
                target_ref=target_ref,
                label=_carrier_label(triggers, guard, effects),
                triggers=triggers,
                trigger_refs=trigger_refs,
                guard=guard,
                effects=effects,
                line=line,
                ref=ref,
                legacy_refs=legacy_refs,
                scope=str(owner.name) if owner is not None else None,
                owner_ref=owner_ref,
                owner_path=carrier.owner_path,
                is_forced=carrier.forced_origin is not None,
                combo_origin_id=carrier.combo_origin_id,
                native_transition_count=len(carrier.native_transitions),
            )
        )
    return ModelIR(states=states, events=events, transitions=tuple(transitions), source_text=document.source_text)


def parse_fcstm(text: str) -> ModelIR:
    """Compatibility entry point that projects only a native pyfcstm load."""

    return _project_native_document(load_native_document(text))


# The context models are kept in a separate module to keep the owned FCSTM
# parser readable.  Resolve the forward references only after all parser and
# IR classes above have been defined; context.py imports ModelIR, not PairInput.
from .context import (  # noqa: E402  (late import is intentional for model rebuilding)
    CanonicalSourceIR,
    ContextManifest,
    ExactSourceInventory,
    InspectionEquivalentFacts,
    NumberedNLSegment,
    SMTFacts,
    StructuredArtifact,
    VerificationFacts,
)

PairInput.model_rebuild()
