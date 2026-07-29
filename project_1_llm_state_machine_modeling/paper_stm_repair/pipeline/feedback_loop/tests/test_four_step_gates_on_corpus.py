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
    by_trigger = {
        (row["source"].rsplit(".", 1)[-1], (row["trigger"] or "").rsplit(".", 1)[-1])
        for row in ends
    }
    # Direct: the root's own child exits on the event.
    assert ("HumanDrivingMode", "Power_Off") in by_trigger
    # Chain: the substates exit on the event setting the run-ending token, and the
    # composite is reported too -- a requirement says "while in autonomous mode",
    # naming the mode rather than whichever substate happened to be active.
    assert ("SubState1", "Power_Off") in by_trigger
    assert ("AutonomousMode", "Power_Off") in by_trigger
    # And the event that leaves the same composite on the *mode-switch* token is
    # not termination.  Ancestry cannot tell the two apart; the token can, and
    # calling this one a termination is what fabricated 16 defects across three
    # pairs.
    assert not any(
        "human_steering" in (row["trigger"] or "") for row in ends
    ), [row for row in ends if "human_steering" in (row["trigger"] or "")]

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


def test_a_mode_switch_through_the_lowering_is_not_termination():
    """The distinction the gate got wrong, on the pair that exposed it.

    Pair 0050 leaves `AutonomousMode` on two events.  `Power_Off` sets the token
    whose outer edge goes to `[*]`; the mode-switch event sets a token whose outer
    edge goes to `HumanDrivingMode`.  Both inner edges are `-> [*]`, both sit under
    a state that ends the run on *some* token, so ancestry calls both terminations
    and the gate told the producer to assert `terminates` for a mode switch --
    False on a correct model, i.e. a published defect the model does not have.

    16 requirements across pairs 0020, 0050 and 0056 tripped it, on triggers that
    are central to their NL.  So both directions are pinned here: the real
    termination must still be refused when a terminal state is proposed for it, and
    the mode switch must be left alone.
    """

    prefix = "llms_emp_feedback_final_0050"
    switch = f"{prefix}.human_steering_cmd_nor_brake_pressed_nor_in_auto_final"
    for source in (f"{prefix}.AutonomousMode", f"{prefix}.AutonomousMode.SubState1"):
        assert _step1(
            "0050",
            (
                Req(
                    "REQ-SWITCH",
                    "occupancy_after",
                    {"source": source, "trigger": switch, "target": f"{prefix}.Proposed"},
                ),
            ),
        ) == (), source
        # The same shape on the terminating event is refused, at both levels.
        assert len(
            _step1(
                "0050",
                (
                    Req(
                        "REQ-END",
                        "occupancy_after",
                        {
                            "source": source,
                            "trigger": f"{prefix}.Power_Off",
                            "target": f"{prefix}.FinalState",
                        },
                    ),
                ),
            )
        ) == 1, source


def test_a_converter_generated_entry_is_marked_so_it_is_not_mistaken_for_the_answer():
    """Otherwise the note that explains `initial_entries` loses a credited defect.

    Pair 0029 declares `[*] -> enter_hwy if [R45RouteToken == 5]` next to a bare
    `[*] -> UnspecifiedInitial`.  The unconditional one is the converter's fallback,
    inserted *because* no author entry was unconditional, and `initial_target`
    answers True for it and False for `enter_hwy` -- where the False is the expected
    defect matrix-v11 was credited with finding.  A producer told only "entry takes
    the unconditional edge" binds the synthetic target and the defect vanishes.

    37 of the corpus's 157 unconditional entries, across 20 pairs, land on such a
    state, so the marking is what the note rests on.
    """

    import json

    trace = json.loads(
        (
            ROOT.parent
            / "representation/reports/llms_emp_r45_java_60/source_traces"
            / "llms_emp_feedback_final_0029.json"
        ).read_text()
    )
    inspected = check_fcstm((PAIRS / "0029" / "fcstm.fcstm").read_text())
    facts = _pseudo_state_facts(inspected, trace["attribution_exclusions"])
    entries = {
        (row["composite"].rsplit(".", 1)[-1], row["target"].rsplit(".", 1)[-1]): row
        for row in facts["initial_entries"]
    }
    synthetic = entries[("HighwayMode", "UnspecifiedInitial")]
    assert synthetic["unconditional"] is True
    assert synthetic["converter_generated"] is True
    authored = entries[("HighwayMode", "enter_hwy")]
    assert authored["unconditional"] is False
    assert authored["converter_generated"] is False


def test_a_missing_variable_claim_survives_a_state_of_the_same_leaf_name():
    """The three namespaces are flat lists that share leaf names.

    Pair 0029 declares a *state* called `intersection`, and its NL line 7 writes
    `intersection=true` -- a genuine missing-variable claim.  Compared against one
    merged index that claim was refused and told to bind
    `<root>.UrbanMode.intersection`, which `variable_declared` then refuses outright
    ("variables take no path prefix").  No legal answer, five rounds, dead run.
    """

    known, _ = _frozen("0029")
    vocabulary = dict(
        _model_vocabulary(check_fcstm((PAIRS / "0029" / "fcstm.fcstm").read_text()).get("inspect") or {}, ())
    )
    prefix = "llms_emp_feedback_final_0029"
    assert any(p.endswith(".intersection") for p in vocabulary["states"])

    def fired(bindings, predicate):
        return redundant_proposal_findings(
            (Req("RX", predicate, bindings),), known, vocabulary
        )

    assert fired({"variable": "intersection"}, "variable_declared") == ()
    assert fired({"event": f"{prefix}.lane_change"}, "event_declared") == ()
    # The shared-state case it exists for still fires, and a non-name binding is
    # none of its business.
    assert len(
        fired(
            {
                "source": f"{prefix}.UrbanMode",
                "trigger": f"{prefix}.auto_finished_true",
                "target": f"{prefix}.UrbanMode.FinishState",
            },
            "occupancy_after",
        )
    ) == 1
    assert fired(
        {"state": f"{prefix}.HighwayMode.cruise", "phase": "entry"}, "action_declared"
    ) == ()


def test_a_running_phase_claim_may_not_be_anchored_at_the_pseudo_initial():
    """Pair 0000's expected defect *is* an edge leaving the pseudo-initial.

    The model declares `[*] -> FinalState : /Power_Off`, and that is the mistake --
    power-off should terminate the running mode.  So a termination requirement bound
    to `source="[*]"` asks whether that very edge exists: true because of the defect,
    and the pair's one expected issue goes unreported.  matrix-v13's 0000-claude
    wrote exactly that and published zero issues where matrix-v11 published the
    credited hit.

    The same binding on an initialization requirement is correct and must survive --
    that is how a power-on claim is written, and the two live side by side in the
    same requirement set.
    """

    from paper_stm_feedback_loop.discover.capability import (
        initialization_anchored_findings,
    )

    prefix = "llms_emp_feedback_final_0000"

    def req(rid, phase, bindings):
        item = Req(rid, "occupancy_after", bindings)
        item.source_context = {"basis": "explicit_nl", "behavior_phase": phase}
        return item

    power_on = req(
        "REQ-003",
        "initialization",
        {
            "source": "[*]",
            "trigger": f"{prefix}.Power_On",
            "target": f"{prefix}.HumanDrivingMode",
        },
    )
    power_off = req(
        "REQ-006",
        "termination",
        {
            "source": "[*]",
            "trigger": f"{prefix}.Power_Off",
            "target": f"{prefix}.FinalState",
        },
    )
    fired = initialization_anchored_findings((power_on, power_off))
    assert len(fired) == 1, fired
    assert "REQ-006" in fired[0]
    assert "termination" in fired[0]
    # A named running source is what the gate is asking for, and it passes.
    pinned = req(
        "REQ-006",
        "termination",
        {
            "source": f"{prefix}.HumanDrivingMode",
            "trigger": f"{prefix}.Power_Off",
            "target": f"{prefix}.FinalState",
        },
    )
    assert initialization_anchored_findings((pinned,)) == ()
    # And `operation` is source-sensitive too, not just termination.
    operating = req(
        "REQ-009",
        "operation",
        {"source": "[*]", "trigger": f"{prefix}.Condition_Met", "target": f"{prefix}.AutonomousMode"},
    )
    assert len(initialization_anchored_findings((operating,))) == 1

    # An omitted phase must be refused too, which is why the rule is a whitelist.
    # matrix-v15's 0000-claude emitted no `behavior_phase` on any requirement; keyed
    # as "refuse when the phase is operation or termination", the gate never fired
    # and the vacuous termination claim went through exactly as before it existed.
    unset = Req(
        "REQ-006",
        "occupancy_after",
        {
            "source": "[*]",
            "trigger": f"{prefix}.Power_Off",
            "target": f"{prefix}.FinalState",
        },
    )
    unset.source_context = {"basis": "explicit_nl"}
    fired_unset = initialization_anchored_findings((unset,))
    assert len(fired_unset) == 1, fired_unset
    assert "unset" in fired_unset[0]
    # Same when there is no source_context at all.
    bare = Req("REQ-007", "occupancy_after", dict(unset.predicate_bindings))
    bare.source_context = {}
    assert len(initialization_anchored_findings((bare,))) == 1


def test_the_phase_judgement_is_a_permission_and_has_exactly_one_owner():
    """The sibling gate was keyed the other way, and a third value switched it off.

    `initialization_anchored_findings` learned this already: `behavior_phase` is
    optional, so a rule keyed on the phases it *forbids* is dodged by silence.  The
    gate on source-blind `response_within` was still keyed that way -- it fired only
    for the literals `operation` and `termination` -- while the splitter prompt
    offered `unspecified` as a fourth value and `structure` as a fifth, and stated
    that omitting the field means "not initialization".

    What that costs is pair 0000's expected issue.  Its only `Power_Off` edge leaves
    the pseudo-initial, so a `response_within` without `source` falls back to the
    default initial configuration, finds the edge, and reports the requirement
    satisfied -- true *because* of the defect.  The gate exists to stop precisely
    that, and any phase value outside two spellings turned it off silently.

    So both gates now ask one function, and it answers as a permission.
    """

    from paper_stm_feedback_loop.discover import capability, nodes
    from paper_stm_feedback_loop.discover.capability import (
        anchors_at_initialization,
        source_omitting_response_calls,
    )

    # Only the claimed permission is granted; everything else, including silence
    # and the values the prompt offers, needs an anchored source.
    assert anchors_at_initialization({"behavior_phase": "initialization"}) is True
    assert anchors_at_initialization({"behavior_phase": "Initialization"}) is True
    for dodge in ("operation", "termination", "structure", "unspecified", "", None):
        assert anchors_at_initialization({"behavior_phase": dodge}) is False, dodge
    assert anchors_at_initialization({}) is False
    assert anchors_at_initialization(None) is False

    # The call the gate is about is still recognised, so the permission is the only
    # thing that changed.
    prefix = "llms_emp_feedback_final_0000"
    blind = (
        f'response_within(trigger="{prefix}.Power_Off", '
        f'response="{prefix}.FinalState", bound=5) is True'
    )
    assert source_omitting_response_calls(blind) == ("response_within",)
    anchored = (
        f'response_within(source="{prefix}.HumanDrivingMode", '
        f'trigger="{prefix}.Power_Off", response="{prefix}.FinalState", bound=5) is True'
    )
    assert source_omitting_response_calls(anchored) == ()

    # One owner, not two: the blacklist constant is gone rather than left beside the
    # function for someone to reach for again.
    assert not hasattr(capability, "SOURCE_SENSITIVE_PHASES")
    assert nodes.anchors_at_initialization is anchors_at_initialization
