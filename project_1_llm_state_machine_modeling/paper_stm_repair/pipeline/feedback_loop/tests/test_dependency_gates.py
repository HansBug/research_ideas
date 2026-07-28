"""The six gates over the assertion dependency graph (issue #170 §11.6).

Each gate closes a state that would otherwise look plausible downstream while
being wrong.  That is the property worth testing, so every gate gets a case that
trips it and a case that must not.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.dependencies import (  # noqa: E402
    blocked_by,
    cross_requirement_dependencies,
    dependency_cycles,
    execution_order,
    missing_dependency_references,
    orphan_preconditions,
)


class A:
    """A stand-in carrying only the fields the gates read."""

    def __init__(self, aid, rid="REQ-001", role="primary", depends_on=()):
        self.assertion_id = aid
        self.requirement_id = rid
        self.role = role
        self.depends_on = tuple(depends_on)


#: Pair 0006's shape: existence precondition, then the delta that needs it.
PAIR_0006 = (
    A("AST-REQ-007-0", "REQ-007", "precondition"),
    A("AST-REQ-007-1", "REQ-007", "primary", ("AST-REQ-007-0",)),
)


# --------------------------------------------------------------------------
# Gate 2: reference completeness
# --------------------------------------------------------------------------


def test_a_dangling_dependency_is_reported():
    """Only expressible since `depends_on` exists; arises on revision.

    A producer rewrites the script, drops one assertion, and leaves the reference
    behind.  Without a gate that is a runtime `KeyError` in the executor.
    """

    bad = (A("AST-1"), A("AST-2", depends_on=("AST-GONE",)))
    assert missing_dependency_references(bad) == ("AST-2 -> AST-GONE",)


def test_a_complete_graph_reports_nothing():
    assert missing_dependency_references(PAIR_0006) == ()


# --------------------------------------------------------------------------
# Gate 4: cross-requirement dependencies are refused for now
# --------------------------------------------------------------------------


def test_a_cross_requirement_dependency_is_reported():
    """A verdict for one requirement must not hinge on another's assertion.

    Imaginable — pair 0029 checks the initial substate of both `HighwayMode` and
    `UrbanMode` — but it makes per-requirement accounting non-local, so start
    closed.
    """

    bad = (
        A("AST-A", "REQ-001", "precondition"),
        A("AST-B", "REQ-002", "primary", ("AST-A",)),
    )
    assert cross_requirement_dependencies(bad) == (
        "AST-B (REQ-002) -> AST-A (REQ-001)",
    )


def test_a_within_requirement_dependency_is_allowed():
    assert cross_requirement_dependencies(PAIR_0006) == ()


# --------------------------------------------------------------------------
# Gate 1: the graph must be acyclic
# --------------------------------------------------------------------------


def test_a_self_loop_is_reported():
    assert dependency_cycles((A("AST-1", depends_on=("AST-1",)),)) == (("AST-1",),)


def test_a_two_node_cycle_is_reported():
    cyc = (A("AST-1", depends_on=("AST-2",)), A("AST-2", depends_on=("AST-1",)))
    assert dependency_cycles(cyc) == (("AST-1", "AST-2"),)


def test_a_three_node_cycle_is_reported_once():
    cyc = (
        A("AST-1", depends_on=("AST-3",)),
        A("AST-2", depends_on=("AST-1",)),
        A("AST-3", depends_on=("AST-2",)),
    )
    assert dependency_cycles(cyc) == (("AST-1", "AST-2", "AST-3"),)


def test_a_diamond_is_not_a_cycle():
    """Two paths to the same prerequisite is legitimate, not circular."""

    diamond = (
        A("AST-0", role="precondition"),
        A("AST-1", depends_on=("AST-0",)),
        A("AST-2", depends_on=("AST-0",)),
        A("AST-3", depends_on=("AST-1", "AST-2")),
    )
    assert dependency_cycles(diamond) == ()


def test_an_acyclic_graph_reports_nothing():
    assert dependency_cycles(PAIR_0006) == ()


# --------------------------------------------------------------------------
# Gate 5: a precondition must be depended upon
# --------------------------------------------------------------------------


def test_an_unreferenced_precondition_is_reported():
    """The primary forgot the dependency, and the resulting state is contradictory.

    The primary runs anyway, raises on the element it needs, and enters the repair
    loop -- while the precondition's `False` reports the very defect that loop is
    failing to work around.
    """

    orphan = (
        A("AST-0", "REQ-001", "precondition"),
        A("AST-1", "REQ-001", "primary"),  # forgot depends_on
    )
    assert orphan_preconditions(orphan) == ("AST-0",)


def test_a_referenced_precondition_reports_nothing():
    assert orphan_preconditions(PAIR_0006) == ()


def test_a_primary_without_dependents_is_not_an_orphan():
    """The rule is about preconditions; ordinary assertions need no dependents."""

    assert orphan_preconditions((A("AST-1"), A("AST-2"))) == ()


# --------------------------------------------------------------------------
# Execution order
# --------------------------------------------------------------------------


def test_dependencies_precede_dependents():
    order = execution_order(PAIR_0006)
    assert order.index("AST-REQ-007-0") < order.index("AST-REQ-007-1")


def test_order_is_deterministic_across_input_orderings():
    """The sealed result is hashed, so two identical scripts must order alike."""

    chain = (
        A("AST-3", depends_on=("AST-2",)),
        A("AST-1", role="precondition"),
        A("AST-2", depends_on=("AST-1",)),
    )
    assert execution_order(chain) == execution_order(tuple(reversed(chain)))
    assert execution_order(chain) == ("AST-1", "AST-2", "AST-3")


def test_independent_assertions_are_ordered_by_id():
    assert execution_order((A("AST-B"), A("AST-A"))) == ("AST-A", "AST-B")


def test_a_multi_level_chain_is_fully_ordered():
    chain = tuple(
        A(f"AST-{i}", depends_on=(f"AST-{i-1}",) if i else ())
        for i in range(5)
    )
    assert execution_order(chain) == tuple(f"AST-{i}" for i in range(5))


# --------------------------------------------------------------------------
# Blocking
# --------------------------------------------------------------------------


def test_a_false_prerequisite_blocks():
    dependent = A("AST-1", depends_on=("AST-0",))
    assert blocked_by(dependent, {"AST-0": False}) == ("AST-0",)


def test_a_true_prerequisite_does_not_block():
    dependent = A("AST-1", depends_on=("AST-0",))
    assert blocked_by(dependent, {"AST-0": True}) == ()


@pytest.mark.parametrize("value", [None, "True", 1, 0])
def test_only_exactly_true_counts_as_satisfied(value):
    """A prerequisite that is absent, or truthy-but-not-True, is not satisfied.

    Absent means it was itself blocked or non-executable.  Either way the claim
    downstream cannot be evaluated meaningfully -- with no variable declared there
    is no delta to judge -- so block rather than run.
    """

    dependent = A("AST-1", depends_on=("AST-0",))
    assert blocked_by(dependent, {"AST-0": value}) == ("AST-0",)


def test_a_missing_prerequisite_blocks():
    dependent = A("AST-1", depends_on=("AST-0",))
    assert blocked_by(dependent, {}) == ("AST-0",)


def test_all_unmet_prerequisites_are_named():
    dependent = A("AST-2", depends_on=("AST-0", "AST-1"))
    assert blocked_by(dependent, {"AST-0": True, "AST-1": False}) == ("AST-1",)
    assert blocked_by(dependent, {}) == ("AST-0", "AST-1")


# --------------------------------------------------------------------------
# End to end through the node, so the gates are not merely importable
# --------------------------------------------------------------------------


def _run_node(assertions, requirement_kwargs=None):
    """Drive `convert_assertions` with a canned script and return its feedback."""

    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.schemas import (
        AssertionScript,
        FrozenDiscoverInputs,
        Requirement,
        RequirementSet,
    )

    req = dict(
        requirement_id="REQ-007",
        statement="After completing the attack the swarm count decreases.",
        predicate="variable_delta_after",
        predicate_bindings={
            "source": "R.Attack",
            "trigger": "R.Attack_Complete",
            "variable": "uav_count",
            "sign": "negative",
        },
        verification_kind="behavior",
    )
    req.update(requirement_kwargs or {})
    requirements = RequirementSet(revision=1, requirements=(Requirement(**req),))
    script = AssertionScript(
        revision=1,
        assertions=tuple(assertions),
        requirement_mapping={
            "REQ-007": tuple(a.assertion_id for a in assertions)
        },
        strategies={
            "REQ-007": (
                "拆两条：数量变量的存在性是效果可判定的前提，二者修复方式不同。"
            )
        },
    )

    class Responder:
        def invoke_structured(self, *args, **kwargs):
            return script

    frozen = FrozenDiscoverInputs(
        run_id="dep-gate",
        natural_language="nl",
        stm_text="stm",
        input_hashes={"nl": "0" * 64},
        tool_env_hash="0" * 64,
        profile="dep-gate",
        language="en-US",
    )
    out = nodes.convert_assertions(
        {
            "requirement_set": requirements,
            "node_execution_records": (),
            "frozen_inputs": frozen,
        },
        Responder(),
    )
    feedback = out.get("_assertion_conversion_contract_feedback")
    return "" if feedback is None else str(feedback.reason) + " " + " ".join(
        str(f) for f in (feedback.findings or ())
    )


def _spec(aid, role, expr, depends_on=(), family="structure"):
    from paper_stm_feedback_loop.discover.schemas import AssertionSpec

    return AssertionSpec(
        assertion_id=aid,
        requirement_id="REQ-007",
        role=role,
        coverage_key=f"key-{aid}",
        aggregation_group="REQ-007:all",
        rationale="Fixture; the NL clause is not under test here.",
        evidence_family=family,
        description="d",
        expression=expr,
        failure_message=f"[REQ-007][{aid}] m",
        depends_on=tuple(depends_on),
    )


EXISTS = 'variable_declared(variable="uav_count") is True'
DELTA = (
    'variable_delta_after(source="R.Attack", trigger="R.Attack_Complete", '
    'variable="uav_count", sign="negative") is True'
)


def test_the_intended_shape_passes_every_gate():
    """Pair 0006's shape must be accepted, or the design is unusable."""

    reason = _run_node(
        (
            _spec("AST-REQ-007-0", "precondition", EXISTS),
            _spec("AST-REQ-007-1", "primary", DELTA, ("AST-REQ-007-0",), "simulation"),
        )
    )
    assert reason == "", reason


def test_a_dangling_reference_is_reported_through_the_node():
    reason = _run_node(
        (_spec("AST-REQ-007-1", "primary", DELTA, ("AST-GONE",), "simulation"),)
    )
    assert "does not contain" in reason, reason


def test_a_cycle_is_reported_through_the_node():
    reason = _run_node(
        (
            _spec("AST-REQ-007-0", "precondition", EXISTS, ("AST-REQ-007-1",)),
            _spec("AST-REQ-007-1", "primary", DELTA, ("AST-REQ-007-0",), "simulation"),
        )
    )
    assert "cycles" in reason, reason


def test_an_orphan_precondition_is_reported_through_the_node():
    reason = _run_node(
        (
            _spec("AST-REQ-007-0", "precondition", EXISTS),
            _spec("AST-REQ-007-1", "primary", DELTA, (), "simulation"),
        )
    )
    assert "nothing depends on" in reason, reason


def test_an_undeclared_literal_in_an_assertion_is_reported_through_the_node():
    """It states a fact about the requirement, not a check.

    Before §11 it was passed all the way to the predicate, which read the
    declaration table and sealed a false.  On this corpus every author variable
    table is empty, so that judgement fired for any pair at all -- a false
    positive channel with every gate green (§11.1).
    """

    reason = _run_node(
        (
            _spec(
                "AST-REQ-007-1",
                "primary",
                DELTA.replace('"uav_count"', '"<undeclared>"'),
                (),
                "simulation",
            ),
        )
    )
    assert "proposed name" in reason, reason


def test_gate_d_does_not_apply_to_a_precondition():
    """The precondition calls `variable_declared`, the requirement names
    `variable_delta_after`.  Checking Gate D against it would reject the very
    shape §11.2 prescribes."""

    reason = _run_node(
        (
            _spec("AST-REQ-007-0", "precondition", EXISTS),
            _spec("AST-REQ-007-1", "primary", DELTA, ("AST-REQ-007-0",), "simulation"),
        )
    )
    assert "must be discharged by calling" not in reason, reason
