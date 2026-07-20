from __future__ import annotations

import copy
from typing import Any

from .exceptions import UnsupportedEvidence
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
    }
)


def _items(inspect: dict[str, Any], kind: str) -> list[dict[str, Any]]:
    raw = inspect.get(kind, [])
    if isinstance(raw, dict):
        values = raw.values()
    elif isinstance(raw, list):
        values = raw
    else:
        values = []
    return [copy.deepcopy(item) for item in values if isinstance(item, dict)]


def _matches_path(actual: str | None, expected: str | None) -> bool:
    if expected is None:
        return True
    if actual is None:
        return False
    return actual == expected or actual.endswith("." + expected)


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
    direct child-state structure.
    """

    family = "structure"

    def __init__(self, inspect: dict[str, Any]) -> None:
        self.inspect = copy.deepcopy(inspect)

    def states(self, *, parent: str | None = None, recursive: bool = True, name: str | None = None) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "states")
        out: list[FrozenView] = []
        for row in rows:
            path = row.get("path")
            if name is not None and row.get("name") != name and not _matches_path(path, name):
                continue
            if parent is not None:
                if recursive:
                    if not isinstance(path, str) or not path.startswith(parent + "."):
                        continue
                elif not _matches_path(row.get("parent_path"), parent):
                    continue
            out.append(FrozenView("state", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def events(self, *, name: str | None = None) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "events")
        out = []
        for row in rows:
            qn = row.get("qualified_name")
            if name is not None and row.get("name") != name and not _matches_path(qn, name):
                continue
            out.append(FrozenView("event", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def variables(self, *, name: str | None = None) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "variables")
        out = []
        for row in rows:
            qualified = row.get("qualified_name") or row.get("path")
            visible = row.get("name") or (
                str(qualified).rsplit(".", 1)[-1] if qualified else None
            )
            if name is not None and visible != name and qualified != name:
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
    ) -> tuple[FrozenView, ...]:
        rows = _items(self.inspect, "transitions") + _items(self.inspect, "forced_transitions")
        out = []
        for row in rows:
            if source is not None and not _matches_path(row.get("from_path"), source):
                continue
            if event is not None and not _matches_path(row.get("event"), event):
                continue
            if target is not None and not _matches_path(row.get("to_path"), target):
                continue
            if forced is not None and bool(row.get("is_forced")) is not forced:
                continue
            out.append(FrozenView("transition", row, allowed_fields=STRUCTURE_FIELDS))
        return tuple(out)

    def transition_exists(self, *, source: str | None = None, event: str | None = None, target: str | None = None) -> bool:
        return bool(self.transitions(source=source, event=event, target=target))

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
