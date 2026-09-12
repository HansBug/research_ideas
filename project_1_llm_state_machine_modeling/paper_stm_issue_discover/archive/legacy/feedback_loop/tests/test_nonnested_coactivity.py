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


@pytest.mark.parametrize(
    "left,right",
    [("M", "Sys.M.A"), ("Sys.M.A", "M"), ("A", "Sys.M.B")],
)
def test_a_bare_name_against_a_path_is_left_alone(left: str, right: str) -> None:
    """One side without hierarchy is a case this rule cannot decide, so it does not.

    `M` may be an unqualified reference to `Sys.M`, which contains `Sys.M.A` and is co-active
    with it -- refusing would cost a real check on a guess. The old rule required a dot on
    the pair it compared, and generalising the *other* half of the test must not quietly
    drop that: `"." not in left or "." not in right` keeps it, `and` would have lost it.
    """
    assert capability.vacuous_sibling_conjunction(_query(left, right)) is None


def test_the_finding_does_not_call_cousins_siblings() -> None:
    """This string goes back to the producer as revision feedback.

    A cousin pair described as "siblings of one sequential region" is simply untrue, and a
    wrong reason invites the producer to argue with the gate instead of fixing the query.
    """
    cousins = (
        'invariant(scope="Sys", condition=\'!(active("Sys.M1.A") && active("Sys.M2.B"))\')'
    )
    finding = capability.condition_non_vacuity_findings(cousins)[0]
    assert "siblings" not in finding, finding
    assert "neither containing the other" in finding

    siblings = (
        'invariant(scope="Sys", condition=\'!(active("Sys.M.A") && active("Sys.M.B"))\')'
    )
    assert "siblings of one sequential region" in capability.condition_non_vacuity_findings(siblings)[0]


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

# --- 运行前 review 补的三条 ---


@pytest.mark.parametrize("left,right", [("Sys.M1", "Sys.M10"), ("Sys.M10", "Sys.M1")])
def test_numeric_siblings_are_not_mistaken_for_nesting(left: str, right: str) -> None:
    """`Sys.M10` starts with `Sys.M1` as a *string* but is not inside it.

    A prefix test written without the separator reads them as nested and lets the pair
    through -- a regression on a case the same-parent rule already caught. The corpus has
    exactly these shapes (`fork1`/`fork2`, `Join1`/`Join2`), so this is a live trap.
    """
    assert capability.vacuous_sibling_conjunction(_query(left, right)) == (left, right)


def test_a_negated_operand_makes_the_conjunction_satisfiable() -> None:
    """`!active(A) && active(B)` says "in B and not in A", which two siblings satisfy easily.

    The detector matches on the inner `active(...)` substring, so the leading `!` is invisible
    to it and the pair is refused on a reading that is the opposite of what was written.
    Pre-existing, but generalising from siblings to every non-nested pair widens who it can
    hit, and the refusal is fatal in `convert_assertions`.
    """
    assert capability.vacuous_sibling_conjunction(
        '!(!active("Sys.M.A") && active("Sys.M.B"))'
    ) is None
    # The unnegated form must still be caught, or the fix has simply disabled the rule.
    assert capability.vacuous_sibling_conjunction(
        '!(active("Sys.M.A") && active("Sys.M.B"))'
    ) == ("Sys.M.A", "Sys.M.B")


def test_every_pair_of_a_multi_term_conjunction_is_examined() -> None:
    """`findall` is non-overlapping, so a three-term conjunction was only half-checked.

    `active(M) && active(M.A) && active(N.B)` matched `(M, M.A)` -- nested, admissible -- and
    the vacuous `(M.A, N.B)` pair was never looked at. Pair 0047 contains a real three-term
    condition, so this is not hypothetical.
    """
    query = (
        '!(active("Sys.M") && active("Sys.M.A") && active("Sys.N.B"))'
    )
    found = capability.vacuous_sibling_conjunction(query)
    assert found is not None, "the non-nested pair in a three-term conjunction must be found"
    assert set(found) <= {"Sys.M", "Sys.M.A", "Sys.N.B"}
    assert not (found[0].startswith(found[1] + ".") or found[1].startswith(found[0] + "."))

