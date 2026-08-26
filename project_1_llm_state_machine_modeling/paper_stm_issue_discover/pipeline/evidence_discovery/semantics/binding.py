from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field

from ..inputs.models import ModelIR
from .obligations import CandidateIssue


class BindingResult(BaseModel):
    """Deterministic result of resolving a candidate against the closed model IR."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    precise: bool = Field(description="Whether every candidate model reference resolved without ambiguity.")
    element_refs: tuple[str, ...] = Field(description="Stable model references resolved from the candidate.")
    source_refs: tuple[str, ...] = Field(description="Requirement/source references carried by the candidate binding.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the deterministic binding result.")
    basis: str = Field(min_length=1, description="Non-empty rule or input basis used for the deterministic binding result.")


_LINE_SUFFIX = re.compile(r":line:\d+$")
_TRANSITION_SIGNATURE = re.compile(
    r"^(?P<source>\[\s*\*\s*\]|[^-]+?)\s*->\s*"
    r"(?P<target>\[\s*\*\s*\]|[^:]+?)(?:\s*:\s*(?P<label>.*))?$"
)


def _endpoint(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip()).replace("[ * ]", "[*]")


def _endpoint_aliases(value: str) -> set[str]:
    """Return closed-model aliases for source/compiler endpoint spellings.

    The representation compiler preserves source boundary markers such as
    ``!State`` and qualified source paths such as ``Root.Region.State``.  The
    owned FCSTM IR intentionally stores the executable endpoint name at its
    declaration level.  These aliases are structural normalization only; no
    text similarity or semantic inference is involved.
    """

    normalized = _endpoint(value)
    aliases = {normalized}
    if normalized.startswith("@initial:"):
        aliases.add("[*]")
        normalized = normalized[len("@initial:") :]
    if normalized.startswith("!"):
        aliases.add(normalized[1:])
        normalized = normalized[1:]
    if normalized.startswith("state:"):
        normalized = normalized[len("state:") :]
    if "." in normalized:
        aliases.add(normalized.rsplit(".", 1)[-1])
    aliases.add(normalized)
    return {item for item in aliases if item}


def _label(value: str) -> str:
    """Normalize a typed display label without interpreting FCSTM source text."""

    return _endpoint(value).strip(" /;")


def _transition_matches(
    value: str,
    model: ModelIR,
    *,
    source: str | None = None,
    target: str | None = None,
) -> list[str]:
    """Resolve a typed transition reference without trusting its display line.

    The parser's canonical ref remains the output. A typed ref may carry a
    model-generated line number or a source/target signature; only a unique
    endpoint/signature match is accepted. This keeps line-addressable model
    output useful while preventing an arbitrary first-edge selection.
    """

    def endpoint_matches(item: object, endpoint: str, field: str) -> bool:
        """Prefer one canonical native-derived state ref over display aliases."""

        resolved_ref = resolve_state_ref(endpoint, model)
        if resolved_ref is not None:
            return getattr(item, f"{field}_ref", None) == resolved_ref
        return bool(
            _endpoint_aliases(getattr(item, field))
            & _endpoint_aliases(endpoint)
        )

    raw = value.strip()
    if not raw.startswith("transition:") and "->" in raw:
        raw = "transition:" + raw
    normalized_ref = model.normalize_ref(raw)
    if normalized_ref in model.transition_refs:
        return [normalized_ref]
    if not raw.startswith("transition:"):
        return []
    body = raw[len("transition:") :]
    body_without_line = _LINE_SUFFIX.sub("", body)
    candidates = list(model.transitions)
    if body_without_line and body_without_line != "line":
        match = _TRANSITION_SIGNATURE.match(body_without_line)
        if match is not None:
            expected_source = _endpoint(match.group("source"))
            expected_target = _endpoint(match.group("target"))
            expected_label = _label(match.group("label") or "")
            candidates = [
                item
                for item in candidates
                if endpoint_matches(item, expected_source, "source")
                and endpoint_matches(item, expected_target, "target")
                and (not expected_label or _label(item.label) == expected_label)
            ]
        else:
            candidates = []
    if source is not None:
        candidates = [
            item
            for item in candidates
            if endpoint_matches(item, source, "source")
        ]
    if target is not None:
        candidates = [
            item
            for item in candidates
            if endpoint_matches(item, target, "target")
        ]
    return [item.ref for item in candidates]


def resolve_transition_ref(
    value: str | None,
    model: ModelIR,
    *,
    source: str | None = None,
    target: str | None = None,
) -> str | None:
    """Return a canonical transition ref only when the binding is unique."""

    if value:
        matches = _transition_matches(value, model, source=source, target=target)
    else:
        matches = [
            item.ref
            for item in model.transitions
            if (
                source is None
                or (
                    item.source_ref == resolve_state_ref(source, model)
                    if resolve_state_ref(source, model) is not None
                    else bool(_endpoint_aliases(item.source) & _endpoint_aliases(source))
                )
            )
            and (
                target is None
                or (
                    item.target_ref == resolve_state_ref(target, model)
                    if resolve_state_ref(target, model) is not None
                    else bool(_endpoint_aliases(item.target) & _endpoint_aliases(target))
                )
            )
        ]
    return matches[0] if len(matches) == 1 else None


def resolve_state_ref(value: str, model: ModelIR) -> str | None:
    """Resolve one typed state identity only when the ModelIR match is unique."""

    normalized_ref = model.normalize_ref(value)
    if normalized_ref in {state.ref for state in model.states}:
        return normalized_ref
    name = value
    if value.startswith("state:"):
        name = _LINE_SUFFIX.sub("", value[len("state:") :])
    canonical_matches = [
        state
        for state in model.states
        if name == state.canonical_path
    ]
    if len(canonical_matches) == 1:
        return canonical_matches[0].ref
    matches = [
        state
        for state in model.states
        if _endpoint_aliases(state.name) & _endpoint_aliases(name)
        or _endpoint_aliases(state.display_name) & _endpoint_aliases(name)
    ]
    return matches[0].ref if len(matches) == 1 else None


def _resolve_ref(value: str, model: ModelIR) -> str | None:
    normalized_ref = model.normalize_ref(value)
    if normalized_ref is not None:
        return normalized_ref
    if value.startswith("state:"):
        state_ref = resolve_state_ref(value, model)
        if state_ref is not None:
            return state_ref
    if value.startswith("event:"):
        name = _LINE_SUFFIX.sub("", value[len("event:") :])
        event = model.event(name)
        if event is not None:
            return event.ref
    if value.startswith("transition:"):
        matches = _transition_matches(value, model)
        return matches[0] if len(matches) == 1 else None
    state_ref = resolve_state_ref(value, model)
    if state_ref is not None:
        return state_ref
    event = model.event(value)
    if event is not None:
        return event.ref
    matches = [
        transition.ref
        for transition in model.transitions
        if value in {transition.source, transition.target, transition.label}
    ]
    if len(matches) == 1:
        return matches[0]
    return None


def bind_candidate(candidate: CandidateIssue, model: ModelIR) -> BindingResult:
    resolved: list[str] = []
    unresolved: list[str] = []
    input_values = candidate.predicate_inputs
    transition_hint = input_values.get("transition") or input_values.get("transition_ref")
    source_hint = input_values.get("source")
    target_hint = input_values.get("target")
    hinted_transitions: list[str] = []
    if isinstance(transition_hint, str) and transition_hint.strip():
        hinted_transitions = _transition_matches(
            transition_hint,
            model,
            source=source_hint if isinstance(source_hint, str) else None,
            target=target_hint if isinstance(target_hint, str) else None,
        )
    elif isinstance(source_hint, str) and isinstance(target_hint, str):
        hinted_transitions = _transition_matches(
            f"transition:{source_hint}->{target_hint}",
            model,
            source=source_hint,
            target=target_hint,
        )

    # S1/S4 candidates frequently identify their exact model element through
    # the registry input rather than duplicating it in element_refs.  Resolve
    # those typed inputs before deciding whether binding is precise.
    for key in ("element", "state", "event"):
        value = input_values.get(key)
        if not isinstance(value, str) or not value.strip():
            continue
        ref = _resolve_ref(value, model)
        if ref is not None and ref not in resolved:
            resolved.append(ref)
    for value in candidate.element_refs:
        ref = _resolve_ref(value, model)
        if ref is None and value.startswith("transition:") and len(hinted_transitions) == 1:
            # A line-only transition ref can be corrected by a unique
            # predicate input binding; ambiguous endpoint matches stay W0.
            ref = hinted_transitions[0]
        if ref is None:
            unresolved.append(value)
        elif ref not in resolved:
            resolved.append(ref)
    if len(hinted_transitions) == 1 and hinted_transitions[0] not in resolved:
        resolved.append(hinted_transitions[0])
    if not candidate.element_refs and len(hinted_transitions) == 1:
        resolved.append(hinted_transitions[0])
    precise = bool(resolved) and not unresolved
    if precise:
        reason = "All candidate model elements resolve to stable references in the closed FCSTM input."
        basis = "exact element reference/name resolution over ModelIR"
    elif unresolved:
        reason = "One or more candidate model elements cannot be reproduced in the closed FCSTM input."
        basis = "unresolved model binding; W0 is required"
    else:
        reason = "The candidate provides no reproducible model element reference."
        basis = "empty model binding; W0 is required"
    return BindingResult(
        precise=precise,
        element_refs=tuple(resolved),
        source_refs=tuple(candidate.source_refs),
        reason=reason,
        basis=basis,
    )
