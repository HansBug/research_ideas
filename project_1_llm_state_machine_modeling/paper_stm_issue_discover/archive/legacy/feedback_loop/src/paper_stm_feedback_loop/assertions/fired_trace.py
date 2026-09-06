"""Reconstruct which transitions a simulation cycle fired, and taint the path.

Why this exists
---------------
``pyfcstm``'s cycle result reports the events a cycle consumed but not the
transitions that carried them.  Without transition identity a state observation
cannot be attributed: knowing the machine ended in ``Root.Done`` does not prove
the path there avoided compiler-owned lowering, so the frozen working contract
declares simulation ineligible for source-level attribution (reason codes
``runtime_has_no_stable_fired_transition_id`` and
``runtime_path_taint_not_computable``).

What it does
------------
Under the single-active semantics this evaluation scope uses (T0: no parallel
regions, no history states), a cycle's before/after active ancestry plus its
consumed events determine the fired transitions in the large majority of cases.
This module recovers them and classifies the path:

``clean``      every element on the path resolves to a positively traced source
               transition
``tainted``    some element on the path is compiler-owned or lowering-excluded
``no_path``    nothing fired -- the event was not consumed and no state changed
``ambiguous``  resolution is not unique and the candidates disagree on taint

Soundness rule
--------------
Reporting only the resolved prefix of a partially resolved path would be
unsound: an unresolved segment may be tainted, and dropping it silently would
turn a debt-bearing path into a clean one.  Every unresolved segment therefore
either resolves to a bounded set of bridge candidates whose taint agrees, or the
whole path is reported ``ambiguous``.
"""

from __future__ import annotations

from typing import Any

from ..common.refs import reference_matches

PSEUDO_INITIAL = "[*]"

TAINT_CLEAN = "clean"
TAINT_TAINTED = "tainted"
TAINT_NO_PATH = "no_path"
TAINT_AMBIGUOUS = "ambiguous"

DERIVED = "fired_transitions_derived"
AMBIGUOUS = "fired_transitions_ambiguous"
UNRESOLVED_SEGMENT = "fired_transitions_unresolved_segment"


def _leaf(active_states: list[str] | tuple[str, ...]) -> str | None:
    """Return the deepest active path, or ``None`` for a terminated runtime."""

    return active_states[-1] if active_states else None


def _covers(state: str, leaf: str | None) -> bool:
    """Return whether ``state`` is the active leaf or one of its ancestors.

    Entering a composite state and descending to its initial child is declared
    structure, not a path element, so a transition targeting the composite
    explains an active leaf inside it.
    """

    if leaf is None:
        return False
    return state == leaf or leaf.startswith(f"{state}.")


def transition_refs(transition: dict[str, Any], *, excluded: tuple[str, ...]) -> tuple[str, ...]:
    """Return the model references a fired transition puts on the path.

    The reference vocabulary matches what relation queries already emit, so the
    attribution matcher intersects both against the same exclusion table.
    Route-control variables appearing in a fired guard or effect are reported as
    ``route_control:<name>``: on the path they are genuine evidence that the
    segment exists only because of converter lowering.
    """

    refs: set[str] = set()
    for key in ("from_path", "to_path", "event"):
        value = transition.get(key)
        if isinstance(value, str) and value and value != PSEUDO_INITIAL:
            refs.add(value)
    index = transition.get("transition_index")
    if isinstance(index, int):
        refs.add(f"transition:{index}")
    text = " ".join(
        str(transition.get(key) or "") for key in ("guard", "effect")
    )
    for item in excluded:
        prefix = "compiler:route_control:"
        if item.startswith(prefix):
            variable = item.removeprefix(prefix)
            if variable and variable in text:
                refs.add(f"route_control:{variable}")
    return tuple(sorted(refs))


def _is_tainted(transition: dict[str, Any], excluded: tuple[str, ...]) -> bool:
    observed = set(transition_refs(transition, excluded=excluded))
    return any(reference_matches(item, observed) for item in excluded)


def _sourced_here(transition: dict[str, Any], cursors: frozenset[str] | None) -> bool:
    """Return whether a transition could fire from any currently possible state.

    ``cursors`` holds every state the runtime might occupy at this point, so an
    ambiguous earlier step widens the set instead of erasing it.  ``None`` means
    the position is genuinely unknown and no source filtering is justified.
    """

    if cursors is None:
        return True
    source = str(transition.get("from_path"))
    if source == PSEUDO_INITIAL:
        return True
    return any(_covers(source, cursor) for cursor in cursors)


def _event_candidates(
    transitions: list[dict[str, Any]],
    event: str,
    *,
    cursors: frozenset[str] | None,
    target_leaf: str | None,
    constrain_target: bool,
) -> list[dict[str, Any]]:
    """Narrow the transitions that could have carried ``event``.

    Filters only ever narrow: when a filter would empty the candidate set the
    wider set is kept, so a filter never manufactures a unique answer.
    """

    candidates = [item for item in transitions if item.get("event") == event]
    if len(candidates) <= 1:
        return candidates
    narrowed = [item for item in candidates if _sourced_here(item, cursors)]
    candidates = narrowed or candidates
    if constrain_target and len(candidates) > 1:
        narrowed = [
            item for item in candidates if _covers(str(item.get("to_path")), target_leaf)
        ]
        candidates = narrowed or candidates
    return candidates


def _targets_of(candidates: list[dict[str, Any]]) -> frozenset[str] | None:
    """Return the states a candidate set could leave the runtime in."""

    targets = {
        str(item.get("to_path"))
        for item in candidates
        if isinstance(item.get("to_path"), str)
        and item.get("to_path") != PSEUDO_INITIAL
    }
    return frozenset(targets) if targets else None


MAX_BRIDGE_HOPS = 3


def _bridge_candidates(
    transitions: list[dict[str, Any]],
    *,
    cursors: frozenset[str] | None,
    target_leaf: str | None,
    is_ended: bool = False,
) -> list[dict[str, Any]]:
    """Return the eventless transitions that could bridge an unresolved segment.

    Completion transitions carry no event, and pyfcstm may chain several of them
    inside one cycle, so a single hop is not enough: a two-hop chain would be
    reported as an unexplained segment and the whole path would go unattributed.
    The search is a breadth-first walk bounded by ``MAX_BRIDGE_HOPS``, and it
    returns the union of the transitions on every path that reaches the target --
    any of them may be the one that fired, so none may be dropped.

    A terminated runtime has no active leaf to aim at.  There the criterion is
    simply "eventless and reachable from a possible cursor": whatever fired led
    to termination, and the union keeps the answer sound.
    """

    eventless = [item for item in transitions if item.get("event") in (None, "")]
    if not eventless:
        return []
    if is_ended:
        return [item for item in eventless if _sourced_here(item, cursors)]

    found: list[dict[str, Any]] = []
    seen_states: set[str] = set()
    frontier: list[tuple[frozenset[str] | None, list[dict[str, Any]]]] = [(cursors, [])]
    for _hop in range(MAX_BRIDGE_HOPS):
        next_frontier: list[tuple[frozenset[str] | None, list[dict[str, Any]]]] = []
        for position, chain in frontier:
            for item in eventless:
                if not _sourced_here(item, position):
                    continue
                target = str(item.get("to_path"))
                if _covers(target, target_leaf):
                    found.extend([*chain, item])
                    continue
                if target in seen_states or target == PSEUDO_INITIAL:
                    continue
                seen_states.add(target)
                next_frontier.append((frozenset({target}), [*chain, item]))
        if found or not next_frontier:
            break
        frontier = next_frontier
    return found


def derive_fired_transitions(
    *,
    transitions: list[dict[str, Any]] | None,
    active_before: list[str] | tuple[str, ...],
    active_after: list[str] | tuple[str, ...],
    consumed_events: list[str] | tuple[str, ...],
    is_ended: bool,
    excluded: tuple[str, ...] = (),
) -> dict[str, Any]:
    """Reconstruct the fired transitions of one cycle and classify path taint.

    Returns a record with ``fired_transitions`` (stable ``transition:<index>``
    refs in consumption order), ``path_refs`` (every model reference on the
    path, for attribution), ``path_taint``, ``limitations`` and, when resolution
    is not unique, ``candidates``.
    """

    if not transitions:
        return {
            "fired_transitions": (),
            "path_refs": (),
            "path_taint": TAINT_AMBIGUOUS,
            "limitations": ("fired_transitions_require_frozen_transition_table",),
            "candidates": {},
        }

    before_leaf = _leaf(active_before)
    after_leaf = _leaf(active_after)
    moved = list(active_before) != list(active_after)
    fired: list[str] = []
    path_refs: set[str] = set()
    candidates: dict[str, list[str]] = {}
    limitations: list[str] = []
    taints: list[bool] = []
    ambiguous = False
    cursors: frozenset[str] | None = (
        frozenset({before_leaf}) if before_leaf else None
    )

    events = [str(item) for item in consumed_events]
    for position, event in enumerate(events):
        is_last = position == len(events) - 1
        matches = _event_candidates(
            transitions,
            event,
            cursors=cursors,
            target_leaf=after_leaf,
            constrain_target=is_last and not is_ended,
        )
        if not matches:
            ambiguous = True
            limitations.append(f"{UNRESOLVED_SEGMENT}:event:{event}")
            continue
        if len(matches) == 1:
            chosen = matches[0]
            index = chosen.get("transition_index")
            if isinstance(index, int):
                fired.append(f"transition:{index}")
            path_refs.update(transition_refs(chosen, excluded=excluded))
            taints.append(_is_tainted(chosen, excluded))
            cursors = _targets_of([chosen]) or cursors
            continue
        # Ambiguous carrier.  Union the candidate references so no element of any
        # possible path is dropped, and let taint agreement decide usability.
        candidates[event] = sorted(
            f"transition:{item['transition_index']}"
            for item in matches
            if isinstance(item.get("transition_index"), int)
        )
        for item in matches:
            path_refs.update(transition_refs(item, excluded=excluded))
        candidate_taints = {_is_tainted(item, excluded) for item in matches}
        if len(candidate_taints) == 1:
            taints.append(candidate_taints.pop())
            limitations.append(f"{AMBIGUOUS}:event:{event}:taint_agrees")
        else:
            ambiguous = True
            limitations.append(f"{AMBIGUOUS}:event:{event}")
        cursors = _targets_of(matches)

    # An unexplained state change means an element of the path was never
    # accounted for.  Try one eventless hop; otherwise report ambiguity.
    if is_ended:
        # A terminated runtime has no active leaf to compare against; the move is
        # explained exactly when some transition was resolved for it.
        explained = bool(fired) or bool(candidates)
    elif cursors is None:
        explained = not moved
    else:
        explained = any(_covers(cursor, after_leaf) for cursor in cursors)
    if moved and not explained:
        bridges = _bridge_candidates(
            transitions,
            cursors=cursors,
            target_leaf=after_leaf,
            is_ended=is_ended,
        )
        if bridges:
            for item in bridges:
                path_refs.update(transition_refs(item, excluded=excluded))
            if len(bridges) == 1:
                index = bridges[0].get("transition_index")
                if isinstance(index, int):
                    fired.append(f"transition:{index}")
            else:
                candidates["<eventless>"] = sorted(
                    f"transition:{item['transition_index']}"
                    for item in bridges
                    if isinstance(item.get("transition_index"), int)
                )
            bridge_taints = {_is_tainted(item, excluded) for item in bridges}
            if len(bridge_taints) == 1:
                taints.append(bridge_taints.pop())
                limitations.append(f"{DERIVED}:eventless_bridge")
            else:
                ambiguous = True
                limitations.append(f"{AMBIGUOUS}:eventless_bridge")
        else:
            ambiguous = True
            limitations.append(f"{UNRESOLVED_SEGMENT}:state_change_unexplained")

    if any(taints):
        taint = TAINT_TAINTED
    elif ambiguous:
        taint = TAINT_AMBIGUOUS
    elif not events and not moved:
        taint = TAINT_NO_PATH
    elif not taints:
        taint = TAINT_NO_PATH
    else:
        taint = TAINT_CLEAN
    if fired and not ambiguous:
        limitations.append(DERIVED)
    return {
        "fired_transitions": tuple(fired),
        "path_refs": tuple(sorted(path_refs)),
        "path_taint": taint,
        "limitations": tuple(dict.fromkeys(limitations)),
        "candidates": candidates,
    }


__all__ = [
    "AMBIGUOUS",
    "DERIVED",
    "PSEUDO_INITIAL",
    "TAINT_AMBIGUOUS",
    "TAINT_CLEAN",
    "TAINT_NO_PATH",
    "TAINT_TAINTED",
    "UNRESOLVED_SEGMENT",
    "derive_fired_transitions",
    "transition_refs",
]
