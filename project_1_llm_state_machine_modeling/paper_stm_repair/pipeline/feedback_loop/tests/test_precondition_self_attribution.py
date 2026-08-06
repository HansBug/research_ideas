"""A precondition is attributed by what it asserts, not by what it guards.

Attribution keys off the predicate and the bound paths, and both are read from the assertion's
*requirement*. For a primary that is right -- the requirement's predicate is what the primary
checks. For a precondition it is not: the precondition asserts that some name exists, while
its requirement describes the obligation that name is needed for. The two are different
claims, and taking the key from the requirement means a precondition whose own expression is
`state_declared(...)` gets classified by whatever predicate the requirement happened to use.

Measured on one generation: a precondition asserting `state_declared` belonged to a
requirement whose predicate is `reaches`. `_declared_ancestor_refs` refuses behavioural
predicates -- correctly, since a run through a state that does not exist is not made
author-owned by its parent being declared -- so it short-circuited before looking at anything,
and a finding the ledger says should have been published landed `unattributed`. Its bound
paths came from the same wrong place: the requirement's `source`/`target`, not the state the
precondition names.

The same round shows the effect is not stable, which is worse than it being wrong. In one
round the precondition had a dependent and inherited its refs, so the claim was published; in
another the converter rewrote that dependent away and the orphaned precondition, asserting the
identical thing, was refused. Whether a finding surfaces turned on a revision history nobody
was reasoning about.

`nodes.py` already states the principle this extends: "Attribution that turns on the role
rather than on the evidence is not attribution." Reading the key off the wrong layer is the
same failure with a different name.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.nodes import _assertion_claim_key  # noqa: E402


class _Req:
    def __init__(self, predicate: str, bindings: dict):
        self.requirement_id = "REQ-001"
        self.predicate = predicate
        self.predicate_bindings = bindings


class _Assertion:
    def __init__(self, role: str, expression: str):
        self.assertion_id = "AST-REQ-001-0"
        self.requirement_id = "REQ-001"
        self.role = role
        self.expression = expression


#: The shape from the generation: a `reaches` requirement guarded by a `state_declared`
#: precondition on a name the model does not declare.
REQUIREMENT = _Req(
    "reaches", {"source": "Sys.Missing", "target": "Sys.Elsewhere", "within_cycles": "2"}
)


def test_a_precondition_is_keyed_by_its_own_predicate() -> None:
    """Not by the requirement's. `reaches` would short-circuit a declarative claim."""
    precondition = _Assertion("precondition", 'state_declared(state="Sys.Missing")')
    predicate, _ = _assertion_claim_key(precondition, REQUIREMENT)
    assert predicate == "state_declared"


def test_a_precondition_is_keyed_by_its_own_bound_paths() -> None:
    """The requirement's `source`/`target` describe the guarded obligation, not this claim."""
    precondition = _Assertion("precondition", 'state_declared(state="Sys.Missing")')
    _, bindings = _assertion_claim_key(precondition, REQUIREMENT)
    assert ("state", "Sys.Missing") in bindings
    assert not any(name == "target" for name, _ in bindings)


def test_a_primary_still_reads_from_its_requirement() -> None:
    """Primaries were never the problem, and the requirement carries the frozen bindings.

    A primary's expression and its requirement's predicate agree by construction; the
    requirement is the authoritative copy, so nothing here should change for it.
    """
    primary = _Assertion("primary", 'reaches(source="Sys.Missing", target="Sys.Elsewhere")')
    predicate, bindings = _assertion_claim_key(primary, REQUIREMENT)
    assert predicate == "reaches"
    assert ("within_cycles", "2") in bindings


def test_an_unparseable_precondition_falls_back_to_its_requirement() -> None:
    """A malformed expression is another gate's business; this one must not lose the key.

    Returning nothing would silently make the assertion unattributable for a reason that has
    nothing to do with attribution.
    """
    broken = _Assertion("precondition", "state_declared(state=")
    predicate, bindings = _assertion_claim_key(broken, REQUIREMENT)
    assert predicate == "reaches"
    assert ("source", "Sys.Missing") in bindings


def test_a_precondition_with_no_requirement_still_yields_its_own_key() -> None:
    """Orphaned by a rewrite, it must not depend on the requirement having survived."""
    precondition = _Assertion("precondition", 'event_declared(event="Sys.absent")')
    predicate, bindings = _assertion_claim_key(precondition, None)
    assert predicate == "event_declared"
    assert ("event", "Sys.absent") in bindings


def test_the_key_does_not_depend_on_whether_a_dependent_survived() -> None:
    """The invariant the change exists to establish.

    Two assertions with identical expressions must produce identical keys whatever happened
    to the rest of the script -- otherwise attribution turns on revision history.
    """
    linked = _Assertion("precondition", 'state_declared(state="Sys.Missing")')
    orphan = _Assertion("precondition", 'state_declared(state="Sys.Missing")')
    assert _assertion_claim_key(linked, REQUIREMENT) == _assertion_claim_key(orphan, None)
