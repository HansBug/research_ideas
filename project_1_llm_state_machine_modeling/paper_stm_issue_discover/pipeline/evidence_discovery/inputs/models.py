from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


_STATE_RE = re.compile(r"^\s*state\s+([^\s{]+)(?:\s+named\s+\"([^\"]*)\")?")
_EVENT_RE = re.compile(r"^\s*event\s+([^\s{]+)(?:\s+named\s+\"([^\"]*)\")?")
_TRANSITION_RE = re.compile(
    r"^\s*(\[\s*\*\s*\]|[A-Za-z_][\w.-]*)\s*->\s*"
    r"(\[\s*\*\s*\]|[A-Za-z_][\w.-]*)(?:\s*:\s*(.*?))?\s*;?\s*$"
)
_ACTION_RE = re.compile(r"^\s*(entry|exit|do)\s*/\s*(.+?)\s*;?\s*$", re.I)
_GUARD_RE = re.compile(r"\[([^\]]+)\]")
_EFFECT_RE = re.compile(r"effect\s*\{([^}]*)\}", re.I)


def _clean_name(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().strip('"'))


def _sha(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


class StateNode(BaseModel):
    """Parsed state declaration with stable source-location identity."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Canonical state identifier parsed from the FCSTM source.")
    display_name: str = Field(min_length=1, description="Human-facing state name parsed from the optional quoted label.")
    parent: str | None = Field(default=None, min_length=1, description="Canonical enclosing state identifier, or null for a top-level state.")
    line: int = Field(ge=1, description="One-based source line where this state declaration starts.")
    ref: str = Field(min_length=1, description="Stable source reference for binding and audit attribution.")
    actions: dict[str, tuple[str, ...]] = Field(default_factory=dict, description="Lifecycle action text grouped by entry, exit, and do slots.")


class EventNode(BaseModel):
    """Parsed event declaration with stable source-location identity."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    name: str = Field(min_length=1, description="Canonical event identifier parsed from the FCSTM source.")
    display_name: str = Field(min_length=1, description="Human-facing event name parsed from the optional quoted label.")
    line: int = Field(ge=1, description="One-based source line where this event declaration starts.")
    ref: str = Field(min_length=1, description="Stable source reference for binding and audit attribution.")


class Transition(BaseModel):
    """Parsed transition with normalized trigger, guard, and effect fragments."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    source: str = Field(min_length=1, description="Canonical source state or initial pseudo-state identifier.")
    target: str = Field(min_length=1, description="Canonical target state identifier.")
    label: str = Field(description="Original normalized transition label, possibly empty.")
    triggers: tuple[str, ...] = Field(description="Normalized trigger/event names parsed from the label.")
    guard: str | None = Field(default=None, min_length=1, description="Normalized guard expression, or null when no guard is present.")
    effects: tuple[str, ...] = Field(description="Normalized effect fragments parsed from the label.")
    line: int = Field(ge=1, description="One-based source line where this transition starts.")
    ref: str = Field(min_length=1, description="Stable source reference for binding and audit attribution.")


class ModelIR(BaseModel):
    """Closed intermediate representation produced by the owned FCSTM parser."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    states: tuple[StateNode, ...] = Field(description="All parsed state declarations in source order.")
    events: tuple[EventNode, ...] = Field(description="All parsed event declarations in source order.")
    transitions: tuple[Transition, ...] = Field(description="All parsed transitions in source order.")
    source_text: str = Field(description="Exact FCSTM source text consumed by the parser.")
    algorithm_version: str = Field(default="fcstm-line-parser.v1", min_length=1, description="Versioned parser algorithm identifier used in evidence receipts.")

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

    def state(self, name: str) -> StateNode | None:
        for state in self.states:
            if state.name == name or state.display_name == name:
                return state
        return None

    def event(self, name: str) -> EventNode | None:
        for event in self.events:
            if event.name == name or event.display_name == name:
                return event
        return None

    def transition(self, ref: str | None) -> Transition | None:
        if not ref:
            return None
        return next((item for item in self.transitions if item.ref == ref), None)

    def to_dict(self) -> dict[str, Any]:
        return {
            "algorithm_version": self.algorithm_version,
            "source_hash": _sha(self.source_text),
            "states": [state.model_dump(mode="json") for state in self.states],
            "events": [event.model_dump(mode="json") for event in self.events],
            "transitions": [transition.model_dump(mode="json") for transition in self.transitions],
        }


class PairInput(BaseModel):
    """One frozen pair's complete method-visible input closure and parsed model IR.

    The source text and closed FCSTM are kept as separate fields because they
    have different authority.  The additional context fields are populated by
    ``load_pair`` from the v27 representation artifacts and owned deterministic
    fact builders; a formal method run must not silently fall back to the old
    three-file input surface.
    """

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True, arbitrary_types_allowed=True)

    pair_id: str = Field(min_length=1, description="Frozen pair identifier used for run partitioning and audit joins.")
    pair_dir: Path = Field(description="Resolved directory containing the pair's source artifacts.")
    nl_text: str = Field(description="Exact natural-language requirement artifact supplied to method generation.")
    fcstm_text: str = Field(description="Exact FCSTM artifact supplied to the owned parser and method generation.")
    plantuml_text: str = Field(description="Exact PlantUML artifact supplied for source localization, if present.")
    model: ModelIR = Field(description="Owned-parser IR derived only from fcstm_text.")
    hashes: dict[str, str] = Field(description="SHA-256 hashes for the source artifacts used by this pair.")
    nl_segments: tuple["NumberedNLSegment", ...] = Field(default_factory=tuple, description="Deterministically numbered NL segments supplied to contract extraction.")
    canonical_source_ir: "CanonicalSourceIR | None" = Field(default=None, description="Canonical author-source IR supplied for source localization; never treated as the FCSTM execution model.")
    exact_source_inventory: "ExactSourceInventory | None" = Field(default=None, description="Exact source state/transition inventory projected from canonical source IR.")
    working_contract: "StructuredArtifact | None" = Field(default=None, description="Published working contract containing mapping, ownership, and capability boundaries.")
    source_trace: "StructuredArtifact | None" = Field(default=None, description="Published source trace and attribution boundary artifact.")
    case_report: "StructuredArtifact | None" = Field(default=None, description="Published case report identity and artifact-hash record, excluding evaluation answers.")
    reference_inspection: "StructuredArtifact | None" = Field(default=None, description="Read-only v27 inspection-derived fact artifact; it is context, never a new backend dependency.")
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


def parse_fcstm(text: str) -> ModelIR:
    """Parse the stable line-oriented FCSTM subset without Python reflection."""

    states: list[StateNode] = []
    events: list[EventNode] = []
    transitions: list[Transition] = []
    state_stack: list[tuple[str, int, str, dict[str, list[str]]]] = []
    pending_state: tuple[str, str, int, str | None] | None = None

    for line_no, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("//"):
            continue
        while line.startswith("}") and state_stack:
            state_stack.pop()
            line = line[1:].strip()
        state_match = _STATE_RE.match(raw_line)
        if state_match:
            name = _clean_name(state_match.group(1))
            display = _clean_name(state_match.group(2) or name)
            parent = state_stack[-1][0] if state_stack else None
            actions: dict[str, list[str]] = {"entry": [], "exit": [], "do": []}
            state = StateNode(
                name=name,
                display_name=display,
                parent=parent,
                line=line_no,
                ref=f"state:{name}:line:{line_no}",
                actions={key: tuple(value) for key, value in actions.items()},
            )
            states.append(state)
            if "{" in raw_line:
                state_stack.append((name, line_no, state.ref, actions))
            continue
        event_match = _EVENT_RE.match(raw_line)
        if event_match:
            name = _clean_name(event_match.group(1))
            display = _clean_name(event_match.group(2) or name)
            events.append(
                EventNode(
                    name=name,
                    display_name=display,
                    line=line_no,
                    ref=f"event:{name}:line:{line_no}",
                )
            )
            continue
        action_match = _ACTION_RE.match(raw_line)
        if action_match and state_stack:
            phase, action = action_match.groups()
            state_name, state_line, state_ref, actions = state_stack[-1]
            actions[phase.lower()].append(_clean_name(action))
            for index, state in enumerate(states):
                if state.ref == state_ref:
                    states[index] = StateNode(
                        name=state.name,
                        display_name=state.display_name,
                        parent=state.parent,
                        line=state.line,
                        ref=state.ref,
                        actions={key: tuple(value) for key, value in actions.items()},
                    )
            continue
        transition_match = _TRANSITION_RE.match(raw_line)
        if transition_match:
            source, target, label = transition_match.groups()
            source = _clean_name(source).replace("[ * ]", "[*]")
            target = _clean_name(target).replace("[ * ]", "[*]")
            label = _clean_name(label or "")
            guards = _GUARD_RE.findall(label)
            effect_match = _EFFECT_RE.search(label)
            effect_values = tuple(_clean_name(value) for value in (effect_match.group(1).split(",") if effect_match else ()))
            label_without_meta = _EFFECT_RE.sub("", _GUARD_RE.sub("", label)).strip()
            label_without_meta = re.sub(r"^if\s*", "", label_without_meta, flags=re.I)
            label_without_meta = label_without_meta.strip(" /")
            triggers = tuple(
                _clean_name(value)
                for value in re.split(r"\s*,\s*", label_without_meta)
                if _clean_name(value)
            )
            transitions.append(
                Transition(
                    source=source,
                    target=target,
                    label=label,
                    triggers=triggers,
                    guard=_clean_name(guards[0]) if guards else None,
                    effects=effect_values,
                    line=line_no,
                    ref=f"transition:line:{line_no}",
                )
            )
        if "{" in raw_line and state_match is None:
            pending_state = pending_state
        if "}" in raw_line:
            for _ in range(raw_line.count("}")):
                if state_stack:
                    state_stack.pop()

    return ModelIR(
        states=tuple(states),
        events=tuple(events),
        transitions=tuple(transitions),
        source_text=text,
    )


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
