"""A requirement cannot exempt itself from a gate by filling in the gate's own input field.

`initialization_anchored_findings` refuses a behavioural claim anchored at `[*]`, because `[*]`
is the configuration before the machine has entered anything -- and on a model whose defect is an
edge leaving the pseudo-initial, such a claim comes back true *because of* the defect. It permits
one exception: a requirement whose `source_context.behavior_phase` says `initialization`, since a
power-on claim legitimately is about that configuration.

`v6run3/0000-claude` took the exception:

    REQ-M006  occupancy_after(source="[*]", trigger=Power_Off, target=FinalState)   -> True
              source_context = {"basis": "explicit_nl", "behavior_phase": "initialization"}

The gate stepped aside, the assertion came back True -- the model's `Power_Off` edge really is
misanchored at `[*]`, which is the one defect pair 0000 exists to find -- and the cell published
nothing. The splitter had even written the misanchoring into its own rationale.

The field the permission keys on is filled in by the splitter the gate constrains, and saying
`initialization` costs it nothing. So the permission is now checked against something it cannot
restate: a run starting at `[*]` can only be fired by a power-on event.

Corpus over all 19 rounds: 123 pseudo-initial bindings carry a power-on trigger or none and stay
permitted; 23 carry `Power_Off`. Twenty-one of those spell the phase `termination` and were
already refused -- this changes the answer only for the two that spelled it `initialization`.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    initialization_anchored_findings,
)

NS = "llms_emp_feedback_final_0000"


class _Req:
    def __init__(self, requirement_id: str, predicate: str, bindings: dict, phase: str | None):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.source_context = {"behavior_phase": phase} if phase else {}
        self.limitations: tuple[str, ...] = ()


def test_power_off_from_the_pseudo_initial_is_refused_despite_the_phase_claim() -> None:
    """The `v6run3` requirement verbatim. Claiming `initialization` must no longer exempt it."""
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M006",
                "occupancy_after",
                {"source": "[*]", "trigger": f"{NS}.Power_Off", "target": f"{NS}.FinalState"},
                "initialization",
            ),
        )
    )
    assert len(findings) == 1
    assert "REQ-M006" in findings[0]


def test_the_refusal_explains_why_the_permission_did_not_apply() -> None:
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M006",
                "terminates",
                {"scope": "[*]", "trigger": f"{NS}.Power_Off"},
                "initialization",
            ),
        )
    )
    assert "power-off" in findings[0].lower()
    assert "true because of the defect" in findings[0]


def test_a_genuine_power_on_claim_is_still_permitted() -> None:
    """The common case in every pair: `[*]` plus the power-on event. Must stay silent."""
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M003",
                "occupancy_after",
                {"source": "[*]", "trigger": f"{NS}.Power_On", "target": f"{NS}.HumanDrivingMode"},
                "initialization",
            ),
        )
    )
    assert findings == ()


def test_an_initialization_claim_with_no_trigger_is_still_permitted() -> None:
    """`initial_target`-shaped claims name no event; refusing them would block real work."""
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M002",
                "reaches",
                {"source": "[*]", "target": f"{NS}.HumanDrivingMode"},
                "initialization",
            ),
        )
    )
    assert findings == ()


def test_the_permission_is_matched_on_the_trigger_tail_not_the_full_path() -> None:
    """Triggers arrive namespace-qualified; the permission must survive that."""
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-X",
                "stays_in",
                {"source": "[*]", "trigger": f"{NS}.system_reset"},
                "initialization",
            ),
        )
    )
    assert findings == ()


def test_power_off_with_a_termination_phase_is_refused_as_before() -> None:
    """The 21 corpus instances that were already refused must keep being refused."""
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M006",
                "terminates",
                {"scope": "[*]", "trigger": f"{NS}.Power_Off"},
                "termination",
            ),
        )
    )
    assert len(findings) == 1


def test_a_requirement_not_anchored_at_the_pseudo_initial_is_untouched() -> None:
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-M007",
                "occupancy_after",
                {
                    "source": f"{NS}.HumanDrivingMode",
                    "trigger": f"{NS}.Power_Off",
                    "target": f"{NS}.FinalState",
                },
                "termination",
            ),
        )
    )
    assert findings == ()


def test_every_offending_requirement_gets_its_own_finding() -> None:
    findings = initialization_anchored_findings(
        (
            _Req(
                "REQ-A",
                "occupancy_after",
                {"source": "[*]", "trigger": f"{NS}.Power_Off"},
                "initialization",
            ),
            _Req(
                "REQ-B",
                "terminates",
                {"scope": "[*]", "trigger": f"{NS}.Power_Off"},
                "termination",
            ),
        )
    )
    assert len(findings) == 2
