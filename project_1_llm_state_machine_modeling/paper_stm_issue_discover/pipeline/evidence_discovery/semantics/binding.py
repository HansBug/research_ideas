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


def _label(value: str) -> str:
    return _endpoint(value).rstrip(" ;")


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

    raw = value.strip()
    if not raw.startswith("transition:") and "->" in raw:
        raw = "transition:" + raw
    if raw in model.transition_refs:
        return [raw]
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
                if _endpoint(item.source) == expected_source
                and _endpoint(item.target) == expected_target
                and (not expected_label or _label(item.label) == expected_label)
            ]
        else:
            candidates = []
    if source is not None:
        candidates = [item for item in candidates if _endpoint(item.source) == _endpoint(source)]
    if target is not None:
        candidates = [item for item in candidates if _endpoint(item.target) == _endpoint(target)]
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
            if (source is None or _endpoint(item.source) == _endpoint(source))
            and (target is None or _endpoint(item.target) == _endpoint(target))
        ]
    return matches[0] if len(matches) == 1 else None


def _resolve_ref(value: str, model: ModelIR) -> str | None:
    if value in model.all_refs:
        return value
    if value.startswith("state:"):
        name = _LINE_SUFFIX.sub("", value[len("state:") :])
        state = model.state(name)
        if state is not None:
            return state.ref
    if value.startswith("event:"):
        name = _LINE_SUFFIX.sub("", value[len("event:") :])
        event = model.event(name)
        if event is not None:
            return event.ref
    if value.startswith("transition:"):
        matches = _transition_matches(value, model)
        return matches[0] if len(matches) == 1 else None
    state = model.state(value)
    if state is not None:
        return state.ref
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
        hinted_transitions = [
            item.ref
            for item in model.transitions
            if _endpoint(item.source) == _endpoint(source_hint)
            and _endpoint(item.target) == _endpoint(target_hint)
        ]
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
