"""`reaches` on a declared event answers from the compiler's routing, not the author's edge.

Pair 0000's specification says power off shall reach the final state. Written as
`occupancy_after(source=HumanDrivingMode, trigger=Power_Off, target=FinalState)` the question is
answered by the edge the author wrote, and the cell publishes its one expected issue. Written as
`reaches(source=HumanDrivingMode, target=FinalState, within_cycles=3)` there is no trigger slot,
so the question becomes "is the target reachable at all" -- and on a projected model the path
that answers yes runs through `R45RouteToken`. The attribution layer rules that evidence
compiler-owned, marks the finding `representation_debt`, and nothing is published.

The cell has lost rounds to this twice on the same sentence: `v6run2` and `v10run3`. The latter
was the only sub-70% round in the first fixed-configuration sample of six.

Width is what makes this usable. Refusing every behavioural predicate without a `trigger` slot
matched 109 requirements across the corpus, 62 of them in pair 0050 -- which scores 1/1/1 every
round -- because `terminates` legitimately has no such slot. Requiring `reaches` *and* a trigger
the model declares brings it to 5 matches, all in pair 0000, all `Power_Off`, all inside the
three rounds already known to have lost or nearly lost the cell this way.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    trigger_consuming_predicate_findings,
)

NS = "llms_emp_feedback_final_0000"
DECLARED = (NS, f"{NS}.HumanDrivingMode", f"{NS}.AutonomousMode", f"{NS}.FinalState", f"{NS}.Power_Off")


class _Req:
    def __init__(self, requirement_id, predicate, bindings, trigger=""):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.trigger = trigger
        self.limitations: tuple[str, ...] = ()


def test_reaches_on_a_declared_event_is_refused() -> None:
    """The `v10run3` requirement verbatim."""
    findings = trigger_consuming_predicate_findings(
        (
            _Req(
                "REQ-M006",
                "reaches",
                {"source": f"{NS}.HumanDrivingMode", "target": f"{NS}.FinalState", "within_cycles": "3"},
                f"{NS}.Power_Off",
            ),
        ),
        DECLARED,
    )
    assert len(findings) == 1
    assert "occupancy_after" in findings[0]
    assert "representation_debt" in findings[0]


def test_occupancy_after_is_what_it_asks_for() -> None:
    """The form that publishes. Must stay silent."""
    findings = trigger_consuming_predicate_findings(
        (
            _Req(
                "REQ-M007",
                "occupancy_after",
                {"source": f"{NS}.HumanDrivingMode", "trigger": f"{NS}.Power_Off", "target": f"{NS}.FinalState"},
                f"{NS}.Power_Off",
            ),
        ),
        DECLARED,
    )
    assert findings == ()


def test_reaches_without_a_trigger_is_legitimate() -> None:
    """A sentence naming no event has nothing to consume; `reaches` is the right predicate."""
    findings = trigger_consuming_predicate_findings(
        (_Req("REQ-M008", "reaches", {"source": f"{NS}.HumanDrivingMode", "target": f"{NS}.FinalState"}),),
        DECLARED,
    )
    assert findings == ()


def test_an_undeclared_trigger_leaves_it_alone() -> None:
    """If the model never declared the event, `occupancy_after` cannot bind it either.

    That case belongs to the step-4 proposal rules, not here.
    """
    findings = trigger_consuming_predicate_findings(
        (
            _Req(
                "REQ-M009",
                "reaches",
                {"source": f"{NS}.HumanDrivingMode", "target": f"{NS}.FinalState"},
                f"{NS}.Emergency_Stop",
            ),
        ),
        DECLARED,
    )
    assert findings == ()


def test_terminates_is_not_touched() -> None:
    """`terminates` has no trigger slot by design -- 62 of pair 0050's requirements use it."""
    findings = trigger_consuming_predicate_findings(
        (_Req("REQ-M010", "terminates", {"scope": f"{NS}.AutonomousMode"}, f"{NS}.Power_Off"),),
        DECLARED,
    )
    assert findings == ()


def test_no_declared_paths_disables_the_gate() -> None:
    findings = trigger_consuming_predicate_findings(
        (_Req("REQ-M006", "reaches", {"source": f"{NS}.HumanDrivingMode"}, f"{NS}.Power_Off"),),
        (),
    )
    assert findings == ()


def test_every_offending_requirement_gets_its_own_finding() -> None:
    findings = trigger_consuming_predicate_findings(
        (
            _Req("REQ-A", "reaches", {"source": f"{NS}.HumanDrivingMode"}, f"{NS}.Power_Off"),
            _Req("REQ-B", "reaches", {"source": f"{NS}.AutonomousMode"}, f"{NS}.Power_Off"),
        ),
        DECLARED,
    )
    assert len(findings) == 2
