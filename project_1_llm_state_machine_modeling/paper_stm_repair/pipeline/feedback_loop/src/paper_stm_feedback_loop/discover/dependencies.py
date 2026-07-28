"""Validation and ordering for the assertion dependency graph (issue #170 §11.6).

Why a graph at all
------------------
A requirement drawn from the NL can name a term the model does not declare --
pair 0006's NL requires the swarm count to drop and the model declares no
variable that could.  The obligation is real, so it has to be checked; but
`variable_delta_after` on a variable that does not exist has nothing to compute,
and forcing it to answer produced either a false built on the converter's own
route token or an unrepairable refusal (§11.1).

Splitting it fixes both halves: one assertion asks whether the variable exists,
the other asks whether its value drops, and the second only runs if the first
holds.  That gives the repair stage a named target and two independent verdicts
to verify against -- which `variable="<undeclared>"` never did.

Kept in its own module because these are pure functions over the script: they
need no evidence environment, so they are cheap to test exhaustively, and the
node code stays about orchestration.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Protocol


class _Spec(Protocol):
    """The fields of an ``AssertionSpec`` this module reads."""

    assertion_id: str
    requirement_id: str
    role: str
    depends_on: tuple[str, ...]


def missing_dependency_references(
    assertions: Iterable[_Spec],
) -> tuple[str, ...]:
    """Dependencies naming an assertion the script does not contain.

    Only a correctness problem since `depends_on` exists: a dangling id used to
    be impossible to express.  It arises in practice on revision -- a producer
    rewrites the script, drops one assertion and leaves the reference behind --
    so it needs its own gate rather than a runtime `KeyError`.
    """

    items = tuple(assertions)
    known = {item.assertion_id for item in items}
    return tuple(
        sorted(
            f"{item.assertion_id} -> {ref}"
            for item in items
            for ref in item.depends_on
            if ref not in known
        )
    )


def cross_requirement_dependencies(
    assertions: Iterable[_Spec],
) -> tuple[str, ...]:
    """Dependencies crossing a requirement boundary.

    Refused for now.  A shared prerequisite across requirements is imaginable --
    pair 0029 checks the initial substate of both `HighwayMode` and `UrbanMode`
    and might want one existence check for a state they share -- but allowing it
    means a requirement's verdict can hinge on an assertion filed under another,
    which makes the per-requirement accounting non-local.  Start closed; open it
    when a real case needs it.
    """

    items = tuple(assertions)
    owner = {item.assertion_id: item.requirement_id for item in items}
    return tuple(
        sorted(
            f"{item.assertion_id} ({item.requirement_id}) -> {ref} ({owner[ref]})"
            for item in items
            for ref in item.depends_on
            if ref in owner and owner[ref] != item.requirement_id
        )
    )


def dependency_cycles(assertions: Iterable[_Spec]) -> tuple[tuple[str, ...], ...]:
    """Cycles in the dependency graph, each as the ids involved.

    A cycle cannot be executed at all: every member waits on another member.
    Without this gate the topological pass would silently leave all of them
    unrun, which reads downstream as "these were blocked" -- a plausible-looking
    state with no prerequisite actually false anywhere.
    """

    items = tuple(assertions)
    known = {item.assertion_id for item in items}
    edges = {
        item.assertion_id: tuple(r for r in item.depends_on if r in known)
        for item in items
    }
    found: list[tuple[str, ...]] = []
    seen: set[str] = set()
    stack: list[str] = []
    on_stack: set[str] = set()

    def walk(node: str) -> None:
        seen.add(node)
        stack.append(node)
        on_stack.add(node)
        for nxt in edges.get(node, ()):
            if nxt in on_stack:
                cycle = stack[stack.index(nxt) :]
                found.append(tuple(cycle))
            elif nxt not in seen:
                walk(nxt)
        on_stack.discard(node)
        stack.pop()

    for item in items:
        if item.assertion_id not in seen:
            walk(item.assertion_id)
    # Normalise so the same cycle reported from two entry points collapses.
    unique = {tuple(sorted(c)) for c in found}
    return tuple(sorted(unique))


def orphan_preconditions(assertions: Iterable[_Spec]) -> tuple[str, ...]:
    """Preconditions no assertion in the same requirement depends on.

    An unreferenced precondition means the primary forgot to declare the
    dependency.  The primary then runs anyway, raises on the element it needs,
    and goes into the repair loop -- while the precondition's own `False` reports
    the very defect that repair loop is failing to work around.  Reporting a
    finding and asking for repairs at the same time is a contradictory state, so
    catch the omission instead.
    """

    items = tuple(assertions)
    referenced: set[str] = set()
    by_requirement: dict[str, set[str]] = defaultdict(set)
    for item in items:
        by_requirement[item.requirement_id].add(item.assertion_id)
        referenced.update(item.depends_on)
    return tuple(
        sorted(
            item.assertion_id
            for item in items
            if item.role == "precondition" and item.assertion_id not in referenced
        )
    )


def execution_order(assertions: Iterable[_Spec]) -> tuple[str, ...]:
    """Assertion ids in an order where every dependency precedes its dependent.

    Ties are broken by id so a script's execution order is reproducible -- the
    sealed result carries a hash, and an order that varied per run would make two
    identical scripts hash differently.

    Assumes the graph is acyclic and complete; call the gates first.
    """

    items = tuple(assertions)
    known = {item.assertion_id for item in items}
    pending = {
        item.assertion_id: {r for r in item.depends_on if r in known} for item in items
    }
    done: list[str] = []
    while pending:
        ready = sorted(k for k, deps in pending.items() if not deps - set(done))
        if not ready:  # pragma: no cover - the cycle gate runs first
            raise ValueError(f"dependency cycle among {sorted(pending)}")
        for node in ready:
            done.append(node)
            pending.pop(node)
    return tuple(done)


def blocked_by(
    assertion: _Spec, truth: dict[str, Any]
) -> tuple[str, ...]:
    """Which of this assertion's prerequisites did not evaluate to ``True``.

    A prerequisite counts as unmet whenever it is not exactly ``True``: `False`,
    or absent because it was itself blocked or non-executable.  Anything other
    than a satisfied prerequisite means the claim this assertion makes cannot be
    evaluated meaningfully -- with no variable declared there is no delta to
    judge -- so it is recorded as blocked rather than run.
    """

    return tuple(
        sorted(ref for ref in assertion.depends_on if truth.get(ref) is not True)
    )


__all__ = [
    "blocked_by",
    "cross_requirement_dependencies",
    "dependency_cycles",
    "execution_order",
    "missing_dependency_references",
    "orphan_preconditions",
]
