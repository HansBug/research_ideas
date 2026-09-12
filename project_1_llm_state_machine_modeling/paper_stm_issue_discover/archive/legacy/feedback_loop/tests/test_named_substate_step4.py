"""A substate the specification points at must exist, whatever the surrounding clause means.

Pair 0050's specification says takeover happens `in (auto final)`. The model declares three
substates named `SubState1`, `SubState2`, `SubState3` and a compiler-owned `FinalWaittr_0005`
-- nothing called `auto_final`. The splitter bound the requirement to what was there and
filed the difference under `limitations`, the reviewer accepted, and the defect was published
as a known limitation rather than as an obligation. That is `EIS-0050-01`, and it is one of
the three eight-cell misses attributed to `split_requirements`.

The narrow shape of the fix matters. An earlier version of this change would have had the
splitter propose the *events* the sentence lists -- `human_steering_cmd`, `brake_pressed` --
but that reading was ruled out on 2026-07-30: the specification writes a comma-separated
list with neither "any of" nor "and", so it does not authorise reading the conditions as
independently triggerable, and `EIS-0000-02`/`EIS-0050-01` both record
`event_declared(...human_steering_cmd)` as a *superseded* basis. Steering the splitter toward
it would manufacture attributions the ledger has already rejected.

What survives that ruling is the state. Whether the clause is read as a conjunction or a
disjunction, and at whatever granularity, a substate the sentence names by name has to be
declared. `state_declared(...auto_final, kind="leaf")` is False on the artefact, is inside
the closed predicate vocabulary, and depends on no reading of the punctuation at all.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import capability, prompts  # noqa: E402

#: Pair 0050's declared states. `FinalWaittr_0005` is injected by the R4.5 projection and is
#: listed in `attribution_exclusions`, but it is in the vocabulary the splitter reads -- so
#: it is exactly the sibling a "same referent" reading would reach for.
PAIR_0050_STATES = (
    "llms_emp_feedback_final_0050",
    "llms_emp_feedback_final_0050.HumanDrivingMode",
    "llms_emp_feedback_final_0050.AutonomousMode",
    "llms_emp_feedback_final_0050.AutonomousMode.SubState1",
    "llms_emp_feedback_final_0050.AutonomousMode.SubState2",
    "llms_emp_feedback_final_0050.AutonomousMode.SubState3",
    "llms_emp_feedback_final_0050.AutonomousMode.FinalWaittr_0005",
)


def test_the_named_substate_rule_is_stated_as_a_step_4_case() -> None:
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "names a specific substate" in text
    assert "step 4, not step 3" in text


def test_the_rule_names_the_sibling_it_forbids_binding_to() -> None:
    """Naming the failure mode, because "a differently-named sibling" alone is abstract.

    The whole point is that `FinalWaittr` and "auto final" read as near-synonyms; a rule that
    does not say so leaves the reader to decide whether this is the case it covers.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "sibling" in text
    assert "same region" in text


def test_the_rule_does_not_reopen_the_superseded_disjunctive_reading() -> None:
    """Guarding the boundary the 2026-07-30 ruling drew.

    A rule phrased over triggers rather than states would send the splitter back to proposing
    `human_steering_cmd`, which the ledger records as a basis it withdrew.
    """
    text = prompts.REQUIREMENT_SPLITTER_PROMPT
    start = text.find("names a specific substate")
    assert start != -1
    rule = text[max(0, start - 400) : start + 900]
    for forbidden in ("disjunct", "independently triggerable", "atomic event"):
        assert forbidden not in rule.lower(), (
            f"the substate rule must not reintroduce {forbidden!r}; "
            "that reading was superseded by parent ruling"
        )


def test_step_2_gate_does_not_intercept_a_substate_the_model_lacks() -> None:
    """The prompt rule is only reachable if the deterministic gate stays silent.

    `redundant_proposal_findings` matches on the *last* path segment within a namespace. Pair
    0050 declares no state whose final segment is `auto_final`, so a step-4 proposal there is
    not refused before the reviewer ever sees it.
    """

    class _Req:
        requirement_id = "REQ-005"
        predicate = "state_declared"
        predicate_bindings = {
            "state": "llms_emp_feedback_final_0050.AutonomousMode.auto_final"
        }
        limitations: tuple[str, ...] = ()

    findings = capability.redundant_proposal_findings(
        (_Req(),),
        frozenset(PAIR_0050_STATES),
        vocabulary={"states": PAIR_0050_STATES},
    )
    assert findings == (), findings


def test_step_2_gate_still_intercepts_a_substate_the_model_does_declare() -> None:
    """The mirror case, so the test above is measuring the gate rather than a typo.

    Proposing `SubState1` under a different scope must still be refused -- that is step 2's
    job, and the new rule is written as an exception to step 3, not to step 2.
    """

    class _Req:
        requirement_id = "REQ-006"
        predicate = "state_declared"
        predicate_bindings = {
            "state": "llms_emp_feedback_final_0050.HumanDrivingMode.SubState1"
        }
        limitations: tuple[str, ...] = ()

    findings = capability.redundant_proposal_findings(
        (_Req(),),
        frozenset(PAIR_0050_STATES),
        vocabulary={"states": PAIR_0050_STATES},
    )
    assert findings, "a declared last segment must still be routed to the declared path"


def test_reviewer_does_not_treat_the_missing_substate_as_an_unobservable_distinction() -> (
    None
):
    """Without this the accept survives the splitter fix.

    The reviewer is told to retain limitations rather than demand distinctions the frozen
    artefacts cannot expose. A substate that is simply absent is not such a distinction --
    `state_declared` observes it directly -- so the rule needs an explicit carve-out.
    """
    text = prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "state_declared" in text
    assert "unobservable" in text.lower()
    start = text.lower().find("unobservable")
    assert "names by name" in text[start : start + 900]
