"""Two states that cannot be active together make a query that proves nothing.

`vacuous_sibling_conjunction` already refuses `active(A) && active(B)` when `A` and `B` sit
directly under one parent: a sequential region holds one child at a time, so the conjunction
is unsatisfiable, its negation is a tautology, and the query's verdict cannot move when the
defect is present or absent.

The rule stopped at *siblings*, and the reason it can go further is a property of the object
language rather than of any sample. paper1's modelling scope is `M = (S, E, V, Tr, A)` with
orthogonal regions explicitly excluded, so exactly one leaf is active at a time and the
active set is the chain from the root down to it. Two states are therefore co-active if and
only if one contains the other. Siblings are just the shortest case; cousins across two
top-level modes are the same impossibility written with a longer prefix, and the old
same-parent test let every one of them through.

Nesting is the part that must keep working. `active(Root.M) && active(Root.M.A)` is perfectly
satisfiable -- being in a leaf means being in its ancestors too -- and refusing it would
throw away the conjunctions that do carry information.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import capability  # noqa: E402


def _query(left: str, right: str) -> str:
    return f'!(active("{left}") && active("{right}"))'


@pytest.mark.parametrize(
    "left,right,why",
    [
        ("Sys.M.A", "Sys.M.B", "siblings -- the case the old rule already caught"),
        ("Sys.M1.A", "Sys.M2.B", "cousins under two top-level modes"),
        ("Sys.M1.A", "Sys.M2.C.D", "cousins at different depths"),
        ("Sys.M1", "Sys.M2", "two top-level modes"),
        ("Sys.M1.A.X", "Sys.M1.B.Y", "cousins sharing a grandparent"),
    ],
)
def test_states_that_cannot_be_co_active_are_refused(left: str, right: str, why: str) -> None:
    found = capability.vacuous_sibling_conjunction(_query(left, right))
    assert found == (left, right), f"{why}: got {found!r}"


@pytest.mark.parametrize(
    "left,right,why",
    [
        ("Sys.M", "Sys.M.A", "a leaf and its parent are active together"),
        ("Sys.M.A", "Sys.M", "the same pair written the other way round"),
        ("Sys", "Sys.M.A.X", "the root is active whenever anything is"),
        ("Sys.M.A", "Sys.M.A", "the same state twice is a different problem"),
    ],
)
def test_nested_pairs_are_left_alone(left: str, right: str, why: str) -> None:
    assert capability.vacuous_sibling_conjunction(_query(left, right)) is None, why


def test_a_bare_pair_with_no_hierarchy_is_left_alone() -> None:
    """Without a dotted path there is nothing to reason about, so no claim is made.

    The old rule required a dot for the same reason and it is kept: a name with no parent
    could be a top-level state or could be something the query invented, and refusing on a
    guess would cost real checks.
    """
    assert capability.vacuous_sibling_conjunction(_query("A", "B")) is None


def test_the_generalisation_catches_what_the_sibling_rule_missed() -> None:
    """The regression this exists to prevent, stated as a contrast.

    Under the same-parent test `Sys.M1.A` and `Sys.M2.B` compared unequal prefixes and passed,
    so an unsatisfiable conjunction became a mandatory primary that could not fail -- the
    requirement was reported satisfied and its expected issue silently lost.
    """
    cousins = _query("Sys.M1.A", "Sys.M2.B")
    assert capability.vacuous_sibling_conjunction(cousins) is not None
    # And the old same-parent computation would have said otherwise:
    assert "Sys.M1".split(".") != "Sys.M2".split(".")


def test_condition_findings_report_the_cousin_case() -> None:
    """The gate that consumes the detector has to surface the new case too."""
    expression = (
        'invariant(scope="Sys", condition=\'!(active("Sys.M1.A") && active("Sys.M2.B"))\')'
    )
    findings = capability.condition_non_vacuity_findings(expression)
    assert findings, "a cousin conjunction must produce a finding"
    assert any("Sys.M1.A" in f and "Sys.M2.B" in f for f in findings), findings
