"""Deterministic author-source index for the PlantUML pair artifacts.

The closed FCSTM model is a lowering of the author's PlantUML text.  Several
facts that predicates observe on the closed model are artifacts of that
lowering rather than statements the author made: compiler-owned continuation
segments guarded by the route token, opaque event identifiers that fold a
``event [guard] / effect`` label into one name, and states whose parent is
whatever block first mentioned them.  This module gives frontier code and
publication gates one place to ask "what did the author write for this
carrier?" without re-parsing PlantUML: it joins the canonical source IR
(author lines and raw labels), the working contract (compiler segments with
``source_refs`` back to author lines) and the closed model text.

Provenance policy (repo CLAUDE.md §3.5.-1): every rule here is a statement
about PlantUML / UML 2.5.1 semantics, never about a sample.  The label
grammar follows the UML transition label convention ``trigger [guard] /
effect`` (UML 2.5.1 §14.2.4.9) which PlantUML renders verbatim; the
lowering keeps the whole label as one opaque event (see
``plantuml_source_lowering.py`` ``R45.DEBT.opaque_transition_label_semantics``).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping, Sequence

from ..inputs import PairInput
from ..inputs.models import ModelIR, StateNode, Transition

# Compiler segment roles that carry the author's own transition statement.  Every
# other generated_role is a continuation / entry / exit hop the lowering
# synthesised (UML has no such transition; it exists only because FCSTM needs a
# flat scope-local edge).  Source: plantuml_working_contract.py generated_role
# vocabulary.
AUTHOR_OWNED_SEGMENT_ROLES = frozenset(
    {
        "source_direct_transition",
        "source_initial_transition",
        "composite_source_leaf_trigger",
    }
)

_LABEL_RE = re.compile(
    r"^\s*(?P<event>[^\[/]*?)\s*(?:\[(?P<guard>[^\]]*)\])?\s*(?:/\s*(?P<effect>.*?))?\s*$",
    re.S,
)
_COMPOUND_RE = re.compile(r",|\bor\b|\\n|\n|\[\*\]", re.I)
_LIFECYCLE_DESCRIPTION_RE = re.compile(
    r"^\s*(?P<phase>entry|enter|exit|do|during)\s*[:：]\s*(?P<action>.+?)\s*$", re.I
)
_STEREOTYPE_RE = re.compile(r"<<\s*([A-Za-z_][\w\s-]*)\s*>>")


def normalize_text(value: str | None) -> str:
    """Collapse a label to a comparison key: lowercase alphanumerics only."""

    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


@dataclass(frozen=True)
class LabelParts:
    """UML ``trigger [guard] / effect`` reading of one PlantUML label."""

    raw: str | None
    event: str | None
    guard: str | None
    effect: str | None

    @property
    def unlabeled(self) -> bool:
        return self.raw is None or not self.raw.strip()

    @property
    def guard_only(self) -> bool:
        return not self.unlabeled and not (self.event or "").strip() and self.guard is not None

    @property
    def compound_event(self) -> bool:
        return bool(self.event) and _COMPOUND_RE.search(self.event) is not None


def parse_label(raw: str | None) -> LabelParts:
    if raw is None or not raw.strip():
        return LabelParts(raw=raw, event=None, guard=None, effect=None)
    match = _LABEL_RE.match(raw)
    if match is None:
        return LabelParts(raw=raw, event=raw.strip(), guard=None, effect=None)
    event = (match.group("event") or "").strip() or None
    guard = match.group("guard")
    guard = guard.strip() if guard is not None else None
    effect = match.group("effect")
    effect = effect.strip() if effect else None
    return LabelParts(raw=raw, event=event, guard=guard, effect=effect)


@dataclass(frozen=True)
class AuthorTransition:
    transition_id: str
    raw_ref: str
    line: int | None
    raw_line: str | None
    raw_source: str
    raw_target: str
    source_qid: str
    target_qid: str
    lexical_scope: str | None
    region_index: int | None
    label: LabelParts

    @property
    def is_initial(self) -> bool:
        return self.raw_source == "[*]"

    @property
    def is_final(self) -> bool:
        return self.raw_target == "[*]"

    def anchor(self) -> str:
        line = f"line {self.line}" if self.line is not None else self.raw_ref
        text = self.raw_line or (
            f"{self.raw_source} --> {self.raw_target}" + (f" : {self.label.raw}" if self.label.raw else "")
        )
        return f"PlantUML {line}: `{text.strip()}`"


@dataclass(frozen=True)
class AuthorState:
    qualified_id: str
    short_name: str
    parent_qid: str | None
    explicit_declaration: bool
    declared_with_block: bool
    declaration_lines: tuple[int, ...]
    declaration_raws: tuple[str, ...]
    body_lines: tuple[tuple[int | None, str], ...]
    parent_region_indices: tuple[int, ...]
    kind: str
    raw_ref: str | None

    @property
    def first_line(self) -> int | None:
        return self.declaration_lines[0] if self.declaration_lines else None

    def stereotypes(self) -> tuple[str, ...]:
        found: list[str] = []
        for raw in (*self.declaration_raws, *(text for _, text in self.body_lines)):
            found.extend(m.group(1).strip().lower() for m in _STEREOTYPE_RE.finditer(raw or ""))
        return tuple(dict.fromkeys(found))


@dataclass
class AuthorSourceIndex:
    """Joined author-level view of one pair.  Build with :func:`build_author_index`."""

    pair_id: str
    transitions: tuple[AuthorTransition, ...]
    states: dict[str, AuthorState]
    segments: tuple[Mapping[str, Any], ...]
    fcstm_lines: tuple[str, ...]
    _by_id: dict[str, AuthorTransition] = field(default_factory=dict, repr=False)
    _segments_by_text: dict[str, list[Mapping[str, Any]]] = field(default_factory=dict, repr=False)
    _segments_by_transition: dict[str, list[Mapping[str, Any]]] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        self._by_id = {item.transition_id: item for item in self.transitions}
        for segment in self.segments:
            text = str((segment.get("metadata") or {}).get("line") or "").strip()
            if text:
                self._segments_by_text.setdefault(text, []).append(segment)
            source_id = str((segment.get("metadata") or {}).get("source_transition_id") or "")
            if source_id:
                self._segments_by_transition.setdefault(source_id, []).append(segment)

    # ------------------------------------------------------------------ carriers
    def segment_for_carrier(self, transition: Transition | None) -> Mapping[str, Any] | None:
        """Working-contract segment that emitted this closed-model carrier, or None."""

        if transition is None or transition.line < 1 or transition.line > len(self.fcstm_lines):
            return None
        text = self.fcstm_lines[transition.line - 1].strip()
        rows = self._segments_by_text.get(text) or []
        if len(rows) == 1:
            return rows[0]
        if not rows:
            return None
        owner_leaf = transition.owner_path.rsplit(".", 1)[-1]
        scoped = [
            row
            for row in rows
            if str((row.get("metadata") or {}).get("scope") or "").rsplit(".", 1)[-1] in {owner_leaf, "__root__" if owner_leaf == transition.owner_path else ""}
        ]
        return scoped[0] if len(scoped) == 1 else None

    def segment_role_for_carrier(self, transition: Transition | None) -> str | None:
        segment = self.segment_for_carrier(transition)
        if segment is None:
            return None
        return str((segment.get("metadata") or {}).get("generated_role") or "") or None

    def is_compiler_owned_carrier(self, transition: Transition | None) -> bool | None:
        """True when the carrier is a lowering-synthesised hop, False when it is the
        author's statement, None when the carrier cannot be attributed."""

        role = self.segment_role_for_carrier(transition)
        if role is None:
            return None
        return role not in AUTHOR_OWNED_SEGMENT_ROLES

    def author_transition_for_carrier(self, transition: Transition | None) -> AuthorTransition | None:
        segment = self.segment_for_carrier(transition)
        if segment is None:
            return None
        source_id = str((segment.get("metadata") or {}).get("source_transition_id") or "")
        return self._by_id.get(source_id)

    def carriers_for_author_transition(self, model: ModelIR, transition_id: str) -> tuple[Transition, ...]:
        """Closed-model carriers emitted for one author transition (all segments)."""

        texts = {
            str((segment.get("metadata") or {}).get("line") or "").strip()
            for segment in self._segments_by_transition.get(transition_id, [])
        }
        texts.discard("")
        found: list[Transition] = []
        for carrier in model.transitions:
            if 1 <= carrier.line <= len(self.fcstm_lines) and self.fcstm_lines[carrier.line - 1].strip() in texts:
                found.append(carrier)
        return tuple(found)

    # -------------------------------------------------------------------- states
    def state(self, name: str | None) -> AuthorState | None:
        if not name:
            return None
        exact = self.states.get(name)
        if exact is not None:
            return exact
        matches = [item for item in self.states.values() if item.short_name == name]
        return matches[0] if len(matches) == 1 else None

    def children(self, qid: str) -> tuple[AuthorState, ...]:
        return tuple(item for item in self.states.values() if item.parent_qid == qid)

    def is_within(self, qid: str | None, ancestor_qid: str) -> bool:
        current = qid
        while current is not None:
            if current == ancestor_qid:
                return True
            current = self.states[current].parent_qid if current in self.states else None
        return False

    def transitions_touching(self, short_name: str) -> tuple[AuthorTransition, ...]:
        return tuple(
            item
            for item in self.transitions
            if short_name in {item.raw_source, item.raw_target, item.source_qid.rsplit(".", 1)[-1], item.target_qid.rsplit(".", 1)[-1]}
        )


def _canonical_model(pair: PairInput) -> Mapping[str, Any] | None:
    ir = pair.canonical_source_ir
    if ir is None:
        return None
    dumped = ir.model_dump(mode="json") if hasattr(ir, "model_dump") else ir
    model = dumped.get("model") if isinstance(dumped, Mapping) else None
    return model if isinstance(model, Mapping) else None


def _line_from_ref(raw_ref: str | None) -> int | None:
    match = re.search(r":line:(\d+)$", raw_ref or "")
    return int(match.group(1)) if match else None


def build_author_index(pair: PairInput) -> AuthorSourceIndex | None:
    """Join canonical source IR, working contract and closed model text; None when
    the pair lacks the canonical IR (fixture pairs)."""

    model = _canonical_model(pair)
    if model is None:
        return None
    transitions: list[AuthorTransition] = []
    for row in model.get("transitions") or []:
        attributes = row.get("attributes") or {}
        raw_label = attributes.get("raw_label") if attributes.get("raw_label") is not None else row.get("label")
        line = attributes.get("raw_line_number") or _line_from_ref(row.get("raw_ref"))
        transitions.append(
            AuthorTransition(
                transition_id=str(row.get("id")),
                raw_ref=str(row.get("raw_ref") or ""),
                line=int(line) if line is not None else None,
                raw_line=attributes.get("raw_line"),
                raw_source=str(attributes.get("raw_source") or row.get("source") or ""),
                raw_target=str(attributes.get("raw_target") or row.get("target") or ""),
                source_qid=str(row.get("source") or ""),
                target_qid=str(row.get("target") or ""),
                lexical_scope=row.get("scope"),
                region_index=attributes.get("region_index"),
                label=parse_label(raw_label),
            )
        )
    states: dict[str, AuthorState] = {}
    for row in model.get("states") or []:
        attributes = row.get("attributes") or {}
        declarations = attributes.get("declarations") or []
        body = attributes.get("body_lines") or []
        qid = str(row.get("id"))
        states[qid] = AuthorState(
            qualified_id=qid,
            short_name=str(attributes.get("short_name") or row.get("label") or qid.rsplit(".", 1)[-1]),
            parent_qid=attributes.get("official_parent") or row.get("parent"),
            explicit_declaration=bool(attributes.get("explicit_declaration", True)),
            declared_with_block=bool(attributes.get("declared_with_block", False)),
            declaration_lines=tuple(int(d["line"]) for d in declarations if isinstance(d, Mapping) and d.get("line") is not None),
            declaration_raws=tuple(str(d.get("raw") or "") for d in declarations if isinstance(d, Mapping)),
            body_lines=tuple((b.get("line"), str(b.get("text") or "")) for b in body if isinstance(b, Mapping)),
            parent_region_indices=tuple(int(i) for i in attributes.get("parent_region_indices") or ()),
            kind=str(row.get("kind") or "state"),
            raw_ref=row.get("raw_ref"),
        )
    segments: tuple[Mapping[str, Any], ...] = ()
    if pair.working_contract is not None:
        payload = pair.working_contract.payload
        segments = tuple(
            item
            for item in payload.get("elements", [])
            if isinstance(item, Mapping) and item.get("kind") == "transition_segment"
        )
    return AuthorSourceIndex(
        pair_id=pair.pair_id,
        transitions=tuple(transitions),
        states=states,
        segments=segments,
        fcstm_lines=tuple(pair.fcstm_text.splitlines()),
    )


# ------------------------------------------------------------------ hierarchy
def ancestor_refs(model: ModelIR, state_ref: str | None) -> tuple[str, ...]:
    """Refs of every enclosing state of ``state_ref`` (nearest first), root included."""

    by_ref = {state.ref: state for state in model.states}
    found: list[str] = []
    current = by_ref.get(state_ref or "")
    while current is not None and current.parent_ref is not None:
        found.append(current.parent_ref)
        current = by_ref.get(current.parent_ref)
    return tuple(found)


def enclosing_endpoint_carriers(
    model: ModelIR, source_ref: str | None, target_ref: str | None
) -> tuple[Transition, ...]:
    """Carriers that realise ``source -> target`` under UML composite-state semantics.

    A transition whose source is an enclosing composite of the required source
    applies whenever any of that composite's substates is active (UML 2.5.1
    §14.2.3.9), so it realises the required edge for the child.  The target must
    match exactly.
    """

    if source_ref is None or target_ref is None:
        return ()
    sources = {source_ref, *ancestor_refs(model, source_ref)}
    return tuple(
        carrier
        for carrier in model.transitions
        if carrier.source_ref in sources and carrier.target_ref == target_ref
    )


def lifecycle_description(text: str) -> tuple[str, str] | None:
    """``Entry: X`` style description lines that read as a lifecycle action."""

    match = _LIFECYCLE_DESCRIPTION_RE.match(text or "")
    if match is None:
        return None
    phase = match.group("phase").lower()
    phase = {"enter": "entry", "during": "do"}.get(phase, phase)
    return phase, match.group("action").strip()
