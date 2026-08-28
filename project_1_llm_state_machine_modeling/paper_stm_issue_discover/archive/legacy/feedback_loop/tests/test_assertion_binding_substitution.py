"""An assertion has to test the element its Requirement bound, not one it invented.

Gate D already checks that the assertion calls the predicate the Requirement named. It does
not check *what the predicate is called on*, and that gap let pair 0050 publish a finding the
ledger had explicitly withdrawn.

The requirement bound the composite event the model actually declares:

    REQ-M005b  guard_distinguishable
      trigger = llms_emp_feedback_final_0050.human_steering_cmd_nor_brake_pressed_nor_in_auto_final
      limitations = ["模型将三条件合并为一个复合事件 … 其可辨识性缺失即为发现"]

The converter then wrote two assertions against an atom nobody bound:

    AST-REQ-M005b-0a  precondition  event_declared(event="…human_steering_cmd")     → False
    AST-REQ-M005b-1   primary       guard_distinguishable(source=…, trigger="…human_steering_cmd")

`human_steering_cmd` is a prefix of the bound composite name, not a declared element and not
a proposed name the requirement recorded. So the precondition asks whether the model declares
a separately-triggerable atom -- which is exactly the basis parent ruling withdrew on
2026-07-30, because the specification's comma list does not authorise reading the three
conditions as independently triggerable. The primary then depended on that precondition, was
blocked, and the withdrawn claim became the published issue.

Substituting a bound element is a different failure from calling the wrong procedure, and it
is decidable here: an element an assertion names must be one the Requirement bound, one the
model declares, or one the Requirement proposed and recorded. Anything else is the converter
changing the question.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.capability import (  # noqa: E402
    substituted_binding_findings,
)


class _Req:
    """Just the attributes the gate reads."""

    def __init__(
        self,
        requirement_id: str,
        predicate: str,
        bindings: dict[str, str],
        limitations: tuple[str, ...] = (),
    ):
        self.requirement_id = requirement_id
        self.predicate = predicate
        self.predicate_bindings = bindings
        self.limitations = limitations


class _Ast:
    def __init__(self, assertion_id: str, requirement_id: str, expression: str, role: str = "primary"):
        self.assertion_id = assertion_id
        self.requirement_id = requirement_id
        self.expression = expression
        self.role = role


ROOT_NS = "llms_emp_feedback_final_0050"
COMPOSITE = f"{ROOT_NS}.human_steering_cmd_nor_brake_pressed_nor_in_auto_final"
DECLARED = frozenset(
    {
        ROOT_NS,
        f"{ROOT_NS}.AutonomousMode",
        f"{ROOT_NS}.HumanDrivingMode",
        COMPOSITE,
    }
)


def _findings(*, expression: str, role: str = "primary", limitations: tuple[str, ...] = ()):
    requirement = _Req(
        "REQ-M005b",
        "guard_distinguishable",
        {"source": f"{ROOT_NS}.AutonomousMode", "trigger": COMPOSITE},
        limitations,
    )
    assertion = _Ast("AST-REQ-M005b-0a", "REQ-M005b", expression, role)
    return substituted_binding_findings((requirement,), (assertion,), DECLARED)


def test_an_invented_prefix_of_the_bound_name_is_refused() -> None:
    """Pair 0050's actual failure. `human_steering_cmd` is a prefix, not an element."""
    findings = _findings(
        expression=f'event_declared(event="{ROOT_NS}.human_steering_cmd") is True',
        role="precondition",
    )
    assert len(findings) == 1
    assert "REQ-M005b" in findings[0]
    assert "human_steering_cmd" in findings[0]


def test_the_finding_names_what_was_bound_so_the_producer_has_a_move() -> None:
    """A refusal with no way out is how the no-progress gate turns into a dead cell."""
    findings = _findings(
        expression=f'event_declared(event="{ROOT_NS}.human_steering_cmd") is True',
        role="precondition",
    )
    assert COMPOSITE in findings[0]


def test_the_primary_is_refused_for_the_same_substitution() -> None:
    """Both assertions in pair 0050 substituted; the gate must not stop at preconditions."""
    findings = _findings(
        expression=(
            f'guard_distinguishable(source="{ROOT_NS}.AutonomousMode", '
            f'trigger="{ROOT_NS}.human_steering_cmd") is True'
        )
    )
    assert len(findings) == 1


def test_asserting_exactly_what_was_bound_passes() -> None:
    findings = _findings(
        expression=(
            f'guard_distinguishable(source="{ROOT_NS}.AutonomousMode", '
            f'trigger="{COMPOSITE}") is True'
        )
    )
    assert findings == ()


def test_a_declared_element_the_requirement_did_not_bind_passes() -> None:
    """Assertions legitimately name context the bindings do not repeat.

    `HumanDrivingMode` is declared by the model, so naming it is reading the artefact rather
    than inventing an element -- refusing that would reject valid work.
    """
    findings = _findings(
        expression=(
            f'guard_distinguishable(source="{ROOT_NS}.AutonomousMode", '
            f'trigger="{COMPOSITE}") is True and '
            f'state_declared(state="{ROOT_NS}.HumanDrivingMode", kind="any") is True'
        )
    )
    assert findings == ()


def test_a_proposed_name_the_requirement_recorded_passes() -> None:
    """Step 4 is the sanctioned way to name something the model lacks.

    The gate has to let it through, or the whole proposed-name mechanism dies -- but only when
    the Requirement wrote the name down, which is what makes it reviewable.
    """
    findings = _findings(
        expression=f'state_declared(state="{ROOT_NS}.AutonomousMode.auto_final", kind="any") is True',
        role="precondition",
        limitations=(
            "NL 点名 auto final 子状态；模型未声明 "
            f"{ROOT_NS}.AutonomousMode.auto_final",
        ),
    )
    assert findings == ()


def test_a_requirement_without_a_predicate_is_left_alone() -> None:
    """v1/v2 artefacts have no `predicate`; the pre-vocabulary path must keep running."""
    requirement = _Req("REQ-001", "", {}, ())
    assertion = _Ast(
        "AST-REQ-001-1",
        "REQ-001",
        f'event_declared(event="{ROOT_NS}.invented") is True',
    )
    assert substituted_binding_findings((requirement,), (assertion,), DECLARED) == ()


def test_every_substituting_assertion_gets_its_own_finding() -> None:
    requirement = _Req(
        "REQ-M005b",
        "guard_distinguishable",
        {"source": f"{ROOT_NS}.AutonomousMode", "trigger": COMPOSITE},
    )
    assertions = (
        _Ast("A1", "REQ-M005b", f'event_declared(event="{ROOT_NS}.human_steering_cmd") is True'),
        _Ast("A2", "REQ-M005b", f'event_declared(event="{ROOT_NS}.brake_pressed") is True'),
    )
    findings = substituted_binding_findings((requirement,), assertions, DECLARED)
    assert len(findings) == 2


def test_an_element_embedded_in_a_binding_expression_counts_as_bound() -> None:
    """`persists_until` binds `release=active("<path>")`, so the element is inside an expression.

    Reading only bare binding values refused a Requirement that had bound the very element its
    assertion asserted, and the repeat killed `v4run3/0006-claude` on the no-progress gate.
    """
    root = "llms_emp_feedback_final_0006"
    declared = frozenset({root, f"{root}.UAVSwarmStateMachine", f"{root}.UAVSwarmStateMachine.Searching"})
    requirement = _Req(
        "REQ-001",
        "persists_until",
        {
            "bound": "5",
            "release": f'active("{root}.UAVSwarmStateMachine.MissionComplete")',
            "state": f"{root}.UAVSwarmStateMachine.Searching",
        },
    )
    assertion = _Ast(
        "AST-REQ-001-0",
        "REQ-001",
        f'state_declared(state="{root}.UAVSwarmStateMachine.MissionComplete", kind="any") is True',
        "precondition",
    )
    assert substituted_binding_findings((requirement,), (assertion,), declared) == ()


def test_a_proposed_name_recorded_by_last_segment_counts() -> None:
    """`limitations` is prose, so it names the element, not the path it will be bound as.

    The real entry reads「MissionComplete 是按 NL 措辞提出的名称（step 4）」-- no namespace
    prefix. Comparing last segments is the same comparison the step-2 gate performs.
    """
    root = "llms_emp_feedback_final_0006"
    declared = frozenset({root, f"{root}.UAVSwarmStateMachine"})
    requirement = _Req(
        "REQ-001",
        "state_declared",
        {"state": f"{root}.UAVSwarmStateMachine.Searching", "kind": "any"},
        limitations=("模型未声明任何对应『任务完成』的状态；MissionComplete 是按 NL 措辞提出的名称（step 4）",),
    )
    assertion = _Ast(
        "AST-REQ-001-0",
        "REQ-001",
        f'state_declared(state="{root}.UAVSwarmStateMachine.MissionComplete", kind="any") is True',
        "precondition",
    )
    assert substituted_binding_findings((requirement,), (assertion,), declared) == ()


def test_the_invented_prefix_is_still_refused_after_the_relaxation() -> None:
    """The relaxations must not let pair 0050's substitution back through.

    `human_steering_cmd` is a prefix of the bound composite, so its *last segment* differs
    (`human_steering_cmd` vs `human_steering_cmd_nor_brake_pressed_nor_in_auto_final`) and no
    `limitations` entry names it on its own.
    """
    findings = _findings(
        expression=f'event_declared(event="{ROOT_NS}.human_steering_cmd") is True',
        role="precondition",
        limitations=("模型将三条件合并为一个复合事件，未为 human steering cmd / brake pressed 声明独立事件",),
    )
    assert len(findings) == 1, findings
