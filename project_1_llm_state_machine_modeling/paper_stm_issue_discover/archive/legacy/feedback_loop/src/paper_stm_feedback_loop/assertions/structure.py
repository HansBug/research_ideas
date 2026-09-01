from __future__ import annotations

import copy
from typing import Any

from .exceptions import UnsupportedEvidence
from .topology import event_ref, is_within, items as _topology_items, ref_matches
from .views import FrozenView


STRUCTURE_FIELDS = frozenset(
    {
        "path",
        "name",
        "parent_path",
        "is_leaf",
        "is_pseudo",
        "is_composite",
        "substates",
        "initial_targets",
        "qualified_name",
        "scope",
        "used_by",
        "is_declared",
        "is_used",
        "type",
        "init_value",
        "read_in_states",
        "written_in_states",
        "read_in_guards",
        "written_in_effects",
        "from_path",
        "to_path",
        "event",
        "event_scope",
        "guard",
        "effect",
        "effect_self_assigns",
        "is_forced",
        "forced_origin",
        "transition_index",
        # Declared actions per lifecycle stage.  pyfcstm has always reported
        # these on each state; they were simply absent from this whitelist, so
        # the frozen view rejected them and the `action_declared` predicate had
        # no way to be checked at all.  Issue #170 C0.
        "entry_actions",
        "exit_actions",
        "during_actions",
        "has_abstract_action",
        "aspect_before",
        "aspect_after",
    }
)


def _items(inspect: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    return _topology_items(inspect, kind)


def _matches_path(actual: str | None, expected: str | None, *, exact: bool = False) -> bool:
    return ref_matches(actual, expected, exact=exact)


class StructureAPI:
    """Read-only structured inspect facade for direct eval assertions.

    Parameters: ``inspect`` is the controller-frozen pyfcstm structured inspect
    dictionary.  The facade is normally constructed by ``EvalEnvironment`` and
    closed over before eval.

    Returns: methods return immutable tuples of ``FrozenView`` records or bools.

    Execution: queries only pyfcstm inspect facts already present in memory:
    states, events, variables, transitions, guards/effects and forced transition
    flags.  No parsing, simulation, BMC, LLM, filesystem, or network access is
    performed here.

    Failure semantics: unavailable categories simply return empty tuples; unknown
    fields/methods on returned views are rejected by ``FrozenView`` as
    ``untracked_dependency``.

    Evidence limitations: structural presence/absence is model evidence for the
    declared scope only; it is not NL semantic coverage or source confirmation.

    Permissions: read-only in-memory inspect access; no arbitrary paths, shell,
    imports, environment, mutation, network, or reference/gold data.

    Example: ``len(api.states(parent="Root", recursive=False)) >= 2`` checks
    direct child-state structure. ``initial_targets`` on a returned state is a
    tuple of mapping views, not a tuple of target strings; use
    ``initial_child("Root.Composite")`` for a single initial child.
    """

    family = "structure"

    def __init__(self, inspect: dict[str, Any]) -> None:
        self.inspect = copy.deepcopy(inspect)

    def states(
        self,
        *,
        parent: str | None = None,
        recursive: bool = True,
        name: str | None = None,
        path: str | None = None,
        within: str | None = None,
        kind: str | None = None,
        exact: bool = False,
    ) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "states")
        out: list[FrozenView] = []
        for row in rows:
            row_path = row.get("path")
            if path is not None and not _matches_path(row_path, path, exact=exact):
                continue
            if name is not None:
                name_ok = row.get("name") == name
                path_ok = _matches_path(row_path, name, exact=exact)
                if not name_ok and not path_ok:
                    continue
            if within is not None and not is_within(row_path, within):
                continue
            if kind == "leaf" and not bool(row.get("is_leaf")):
                continue
            if kind == "composite" and not bool(row.get("is_composite")):
                continue
            if kind == "pseudo" and not bool(row.get("is_pseudo")):
                continue
            if parent is not None:
                if recursive:
                    if exact:
                        if not is_within(row_path, parent, include_self=False):
                            continue
                    elif not isinstance(row_path, str) or not row_path.startswith(parent + "."):
                        continue
                elif not _matches_path(row.get("parent_path"), parent, exact=exact):
                    continue
            out.append(FrozenView("state", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def events(
        self,
        *,
        name: str | None = None,
        path: str | None = None,
        within: str | None = None,
        scope: str | None = None,
        declared: bool | None = None,
        used: bool | None = None,
        exact: bool = False,
    ) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "events")
        out = []
        for row in rows:
            ref = event_ref(row)
            if path is not None and not _matches_path(ref, path, exact=exact):
                continue
            if name is not None and row.get("name") != name and not _matches_path(ref, name, exact=exact):
                continue
            if within is not None and not is_within(ref, within):
                continue
            if scope is not None and not _matches_path(
                row.get("scope"), scope, exact=exact
            ):
                continue
            if declared is not None and bool(row.get("is_declared")) is not declared:
                continue
            if used is not None and bool(row.get("is_used")) is not used:
                continue
            out.append(FrozenView("event", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def variables(
        self,
        *,
        name: str | None = None,
        path: str | None = None,
        within: str | None = None,
        type: str | None = None,
        read_in: str | None = None,
        written_in: str | None = None,
        exact: bool = False,
    ) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "variables")
        out = []
        for row in rows:
            qualified = row.get("qualified_name") or row.get("path")
            visible = row.get("name") or (
                str(qualified).rsplit(".", 1)[-1] if qualified else None
            )
            if path is not None and not _matches_path(str(qualified) if qualified else None, path, exact=exact):
                continue
            if name is not None and visible != name and not _matches_path(str(qualified) if qualified else None, name, exact=exact):
                continue
            if within is not None and not is_within(str(qualified) if qualified else None, within):
                continue
            if type is not None and row.get("type") != type:
                continue
            if read_in is not None and not any(
                _matches_path(str(ref), read_in, exact=exact)
                for key in ("read_in_states", "read_in_guards")
                for ref in (row.get(key) or [])
            ):
                continue
            if written_in is not None and not any(
                _matches_path(str(ref), written_in, exact=exact)
                for key in ("written_in_states", "written_in_effects")
                for ref in (row.get(key) or [])
            ):
                continue
            out.append(FrozenView("variable", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def transitions(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        forced: bool | None = None,
        within: str | None = None,
        has_event: bool | None = None,
        has_guard: bool | None = None,
        has_effect: bool | None = None,
        self_loop: bool | None = None,
        source_within: str | None = None,
        target_within: str | None = None,
        exact: bool = False,
    ) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "transitions") + _items(self.inspect, "forced_transitions")
        out = []
        for row in rows:
            if source is not None and not _matches_path(row.get("from_path"), source, exact=exact):
                continue
            if event is not None and not _matches_path(row.get("event"), event, exact=exact):
                continue
            if target is not None and not _matches_path(row.get("to_path"), target, exact=exact):
                continue
            if within is not None and not (is_within(row.get("from_path"), within) or is_within(row.get("to_path"), within)):
                continue
            if source_within is not None and not is_within(
                row.get("from_path"), source_within
            ):
                continue
            if target_within is not None and not is_within(
                row.get("to_path"), target_within
            ):
                continue
            if has_event is not None and bool(row.get("event")) is not has_event:
                continue
            if has_guard is not None and bool(row.get("guard")) is not has_guard:
                continue
            if has_effect is not None and bool(row.get("effect")) is not has_effect:
                continue
            if self_loop is not None and (
                row.get("from_path") == row.get("to_path")
            ) is not self_loop:
                continue
            if forced is not None and bool(row.get("is_forced")) is not forced:
                continue
            out.append(FrozenView("transition", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def transition_exists(
        self,
        *,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        within: str | None = None,
        exact: bool = False,
    ) -> bool:
        return bool(self.transitions(source=source, event=event, target=target, within=within, exact=exact))

    def initial_child(self, state: str) -> str | None:
        """Return one structured initial target for a composite, or ``None``."""

        matches = [row for row in _items(self.inspect, "states") if row.get("path") == state]
        if not matches:
            return None
        targets = matches[0].get("initial_targets") or []
        if not targets:
            return None
        if len(targets) != 1 or not isinstance(targets[0], dict):
            raise UnsupportedEvidence(
                f"initial_child requires exactly one structured initial target for {state!r}"
            )
        target = targets[0].get("target")
        if target is None:
            raise UnsupportedEvidence(
                f"initial_child target is missing for {state!r}"
            )
        return str(target)


__all__ = ["STRUCTURE_FIELDS", "StructureAPI"]
