"""The two step gates against the real corpus, on the requirements that misfired.

The unit tests above drive these gates through synthetic fixtures, which is the
right way to pin their branches.  It is not enough here: the gates read a
*derived* view of the model (`_pseudo_state_facts`), and a derivation that
silently produces nothing passes every fixture test while making the gate inert
on real input.  That happened once in this project already -- a gate whose
docstring described an active check had been matching a function name the
predicate vocabulary removed, so it protected nothing for three redesigns.

So these cases replay the exact requirement shapes matrix-v11 produced, against
the exact models it ran on.  Each was a confirmed false positive published as an
issue in that matrix, and each must now be refused before the assertion layer
ever sees it.  The pairs are repository content, so this is reproducible without
the run directory.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions.pyfcstm_adapter import check_fcstm  # noqa: E402
from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    redundant_proposal_findings,
    termination_proposal_findings,
)
from paper_stm_feedback_loop.discover.nodes import (  # noqa: E402
    _model_vocabulary,
    _pseudo_state_facts,
)

PAIRS = (
    ROOT.parent / "representation/reports/llms_emp_r45_java_60/pairs"
)


class Req:
    def __init__(self, rid, predicate, bindings, limitations=()):
        self.requirement_id = rid
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.limitations = tuple(limitations)


def _frozen(case: str):
    """Return `(known_paths, pseudo_state_facts)` exactly as `prepare` would."""

    inspected = check_fcstm((PAIRS / case / "fcstm.fcstm").read_text())
    vocabulary = _model_vocabulary(inspected.get("inspect") or {}, ())
    known = frozenset(path for paths in vocabulary.values() for path in paths)
    return known, _pseudo_state_facts(inspected)


def _step1(case, requirements):
    known, facts = _frozen(case)
    return termination_proposal_findings(
        requirements, known, facts["terminating_transitions"]
    )


def _step2(case, requirements):
    known, _ = _frozen(case)
    return redundant_proposal_findings(requirements, known)


# --------------------------------------------------------------------------
# The derivation itself: a gate reading an empty view is a gate that does nothing


def test_termination_is_derived_only_where_the_run_really_ends():
    """`-> [*]` leaves whatever scope owns the source, which is not always the run.

    Pair 0050 ends the run twice -- directly from `HumanDrivingMode` on `Power_Off`,
    and from `AutonomousMode` through the guarded completion edge the lowering
    generates.  Pair 0029's `enter_urban -> [*]` looks identical and is not
    termination at all: it exits UrbanMode and routes onward to a declared state, so
    a completion claim there is a reachability question.  Getting that wrong in
    either direction breaks a gate: too eager refuses real reachability claims, too
    shy leaves the fabricated terminal states it exists to stop.
    """

    _, facts = _frozen("0050")
    ends = [row for row in facts["terminating_transitions"] if row["ends_run"]]
    sources = {row["source"].rsplit(".", 1)[-1] for row in ends}
    assert sources == {"HumanDrivingMode", "AutonomousMode"}, ends

    _, urban = _frozen("0029")
    assert [row for row in urban["terminating_transitions"] if row["ends_run"]] == []
    # ...but the exit edges are still seen, which is what the note explains.
    assert any(
        row["source"].endswith("UrbanMode.enter_urban")
        for row in urban["terminating_transitions"]
    )


def test_initial_entries_are_derived_for_every_composite_that_declares_one():
    """`initial_target` claims are decided against these, so an empty list is a
    silent loss of the only evidence the producer has for that question."""

    for case, at_least in (("0000", 3), ("0029", 9), ("0050", 2)):
        _, facts = _frozen(case)
        entries = facts["initial_entries"]
        assert len(entries) >= at_least, (case, entries)
        # The flag is the whole point: entry takes an unconditional edge when one
        # exists, and on 0029 that is the converter's synthetic default rather than
        # the state the NL names.
        assert any(row["unconditional"] for row in entries), case


# --------------------------------------------------------------------------
# The three findings matrix-v11 published that should not have been findings


def test_pair_0050_fabricated_terminal_states_are_refused():
    """Both were published as confirmed issues against a model that terminates.

    `HumanDrivingMode -> [*] : /Power_Off` is how termination is written, so no
    correct model declares a `FinalState`, and `state_declared` answering False
    about one is not a defect -- it is the requirement asking the wrong question.
    The second one is the reason the gate walks the lowering chain: `AutonomousMode`
    terminates through a token, not a direct edge.
    """

    prefix = "llms_emp_feedback_final_0050"
    fired = _step1(
        "0050",
        (
            Req(
                "REQ-007",
                "occupancy_after",
                {
                    "source": f"{prefix}.HumanDrivingMode",
                    "trigger": f"{prefix}.Power_Off",
                    "target": f"{prefix}.FinalState",
                },
            ),
            Req(
                "REQ-008",
                "occupancy_after",
                {
                    "source": f"{prefix}.AutonomousMode",
                    "trigger": f"{prefix}.Power_Off",
                    "target": f"{prefix}.FinalState",
                },
            ),
        ),
    )
    assert len(fired) == 2, fired
    assert all("terminates" in text for text in fired)


def test_pair_0029_shared_completion_state_is_refused():
    """`FinishState` is declared once, inside HighwayMode, and UrbanMode's finish
    routes into it on the token the lowering sets.  Proposing
    `UrbanMode.FinishState` reports a missing state that is present."""

    prefix = "llms_emp_feedback_final_0029"
    fired = _step2(
        "0029",
        (
            Req(
                "REQ-025",
                "occupancy_after",
                {
                    "source": f"{prefix}.UrbanMode",
                    "trigger": f"{prefix}.auto_finished_true",
                    "target": f"{prefix}.UrbanMode.FinishState",
                },
            ),
        ),
    )
    assert len(fired) == 1, fired
    assert f"{prefix}.HighwayMode.FinishState" in fired[0]


# --------------------------------------------------------------------------
# And the requirements that were right must stay untouched


@pytest.mark.parametrize(
    "case,requirements",
    [
        # Pair 0000 declares a real `FinalState`, so the same sentence shape is a
        # reachability claim about a declared state and neither gate applies.
        (
            "0000",
            (
                Req(
                    "REQ-006",
                    "response_within",
                    {
                        "trigger": "llms_emp_feedback_final_0000.Power_Off",
                        "response": "llms_emp_feedback_final_0000.FinalState",
                        "bound": "5",
                        "source": "llms_emp_feedback_final_0000.HumanDrivingMode",
                    },
                ),
            ),
        ),
        # The credited hit on 0029: an initial-target claim binding a declared
        # state.  Refusing this would lose an expected defect.
        (
            "0029",
            (
                Req(
                    "REQ-005",
                    "initial_target",
                    {
                        "composite": "llms_emp_feedback_final_0029.HighwayMode",
                        "child": "llms_emp_feedback_final_0029.HighwayMode.enter_hwy",
                    },
                ),
            ),
        ),
        # Pair 0006's genuine gap: the NL's completion boundary has no counterpart
        # anywhere in the model, so step 4 is correct and the proposal survives.
        (
            "0006",
            (
                Req(
                    "REQ-001",
                    "persists_until",
                    {
                        "state": "llms_emp_feedback_final_0006.UAVSwarmStateMachine.Searching",
                        "release": 'active("llms_emp_feedback_final_0006.UAVSwarmStateMachine.MissionCompleted")',
                        "bound": "5",
                    },
                ),
            ),
        ),
    ],
)
def test_correct_requirements_are_not_refused(case, requirements):
    assert _step1(case, requirements) == ()
    assert _step2(case, requirements) == ()
