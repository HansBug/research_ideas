"""A behavioural claim anchored at the model root asks about power-on, not about the run.

Binding `source` or `scope` to the root starts the machine from its own initial
configuration, so the claim is answered by what happens at start-up -- the same question
`[*]` asks, and `initialization_anchored_findings` already refuses that. Pair 0000 round 1
took the other spelling: `occupancy_after(source=<root>, target=FinalState,
trigger=Power_Off)` returned True because `[*] -> FinalState : /Power_Off` fires on the first
tick, so the claim was true *because of* the defect it was written to catch, and the cell
published nothing. Rounds 2 and 3 bound the running modes and found it.

Decided here rather than in prose. The same rule was first written into the splitter prompt,
and prose fires at a rate the previous three rounds measured at two times in four -- treating
run-to-run variance with an instrument that is itself a random variable. The prompt keeps the
explanation; this decides.

Two boundaries matter as much as the rule. It applies only to predicates whose subject is a
*run*, because for `cardinality`, `containment` and `initial_target` the root is the
legitimate subject -- twelve ledger assertions bind it that way and are correct to. And it
fires at split time rather than at conversion, because `predicate_bindings` freeze when the
requirement is accepted; a gate after the freeze leaves the item no legal move, which is how
two earlier runs died.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import capability  # noqa: E402

MODEL_ROOT = "llms_emp_feedback_final_0000"


class _Req:
    """Just the attributes the gate reads."""

    limitations: tuple[str, ...] = ()

    def __init__(self, requirement_id: str, predicate: str, bindings: dict[str, str]):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings


def _findings(*requirements: _Req) -> tuple[str, ...]:
    return capability.root_anchored_findings(requirements, MODEL_ROOT)


def test_a_behavioural_source_bound_to_the_root_is_refused() -> None:
    """The exact shape that lost pair 0000's expected defect in round 1."""
    findings = _findings(
        _Req(
            "REQ-006",
            "occupancy_after",
            {"source": MODEL_ROOT, "target": f"{MODEL_ROOT}.FinalState", "trigger": f"{MODEL_ROOT}.Power_Off"},
        )
    )
    assert len(findings) == 1
    assert "REQ-006" in findings[0]
    assert "source" in findings[0]


def test_the_finding_names_the_legal_move() -> None:
    """A refusal with no way out is how the no-progress gate turns into a dead cell.

    `nodes.py` stops a requirement loop when a revision repeats a fingerprint, and that stop
    is fatal -- `can_revise` goes False. A gate that says only "no" invites exactly that
    repeat, so this one says what to bind instead.

    What is asserted is that a legal move is named, not how many requirements it takes. An
    earlier version required the words "one requirement per", which is a prescription about
    the *cardinality of the answer* -- and pinning it here is what kept that prescription in
    the gate's message across generations. The way out the gate owes the splitter is which
    subject to bind; how many requirements the sentence needs is the splitter's to decide.
    """
    findings = _findings(
        _Req("REQ-006", "occupancy_after", {"source": MODEL_ROOT, "target": "x", "trigger": "y"})
    )
    assert "Name the running state" in findings[0]
    # And the refusal must still say which subjects remain legal, or the splitter cannot
    # tell a refused binding from a refused predicate.
    assert "cardinality, containment and initial_target" in findings[0]


def test_a_behavioural_scope_bound_to_the_root_is_refused_too() -> None:
    """`terminates` names its subject `scope`; the question it asks is the same one."""
    findings = _findings(
        _Req("REQ-007", "terminates", {"scope": MODEL_ROOT, "trigger": f"{MODEL_ROOT}.Power_Off"})
    )
    assert len(findings) == 1
    assert "scope" in findings[0]


def test_a_running_state_is_not_refused() -> None:
    findings = _findings(
        _Req(
            "REQ-006A",
            "occupancy_after",
            {"source": f"{MODEL_ROOT}.HumanDrivingMode", "target": "x", "trigger": "y"},
        )
    )
    assert findings == ()


def test_structural_predicates_may_bind_the_root() -> None:
    """Twelve ledger assertions do, and the root is the right subject for all of them.

    `cardinality(scope=<root>, count=3)` asks how many regions the machine declares --
    a question about the model, not about a run, so no configuration is being assumed.
    """
    findings = _findings(
        _Req("REQ-001", "cardinality", {"scope": MODEL_ROOT, "count": "3"}),
        _Req("REQ-002", "containment", {"parent": MODEL_ROOT, "child": f"{MODEL_ROOT}.Junction3"}),
        _Req("REQ-003", "initial_target", {"composite": MODEL_ROOT, "child": f"{MODEL_ROOT}.DoorShut"}),
        _Req("REQ-004", "edge_declared", {"source": MODEL_ROOT, "target": "x", "trigger": "y"}),
    )
    assert findings == (), findings


def test_the_pseudo_initial_is_left_to_its_own_gate() -> None:
    """`initialization_anchored_findings` owns `[*]`; two findings for one binding would
    give the splitter contradictory instructions in the same feedback round."""
    findings = _findings(
        _Req("REQ-006", "occupancy_after", {"source": "[*]", "target": "x", "trigger": "y"})
    )
    assert findings == ()


def test_an_empty_or_absent_binding_is_not_a_finding() -> None:
    findings = _findings(
        _Req("REQ-008", "occupancy_after", {"source": "", "target": "x", "trigger": "y"}),
        _Req("REQ-009", "reaches", {"target": "x", "within_cycles": "1"}),
    )
    assert findings == ()


def test_every_offending_requirement_gets_its_own_finding() -> None:
    findings = _findings(
        _Req("REQ-006", "occupancy_after", {"source": MODEL_ROOT, "target": "x", "trigger": "y"}),
        _Req("REQ-007", "stays_in", {"source": MODEL_ROOT, "trigger": "y"}),
    )
    assert len(findings) == 2
    assert {"REQ-006", "REQ-007"} == {f.split()[0] for f in findings}


def test_no_model_root_means_no_gate() -> None:
    """A pair whose root cannot be determined must not have every binding refused."""
    assert capability.root_anchored_findings(
        (_Req("REQ-006", "occupancy_after", {"source": MODEL_ROOT, "target": "x", "trigger": "y"}),),
        "",
    ) == ()
