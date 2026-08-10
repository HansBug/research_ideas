"""Schema for preconditions and dependencies (issue #170 §11.4).

The three fields added here exist to make a missing model element *repairable*.
`variable="<undeclared>"` is dead to the repair stage: it names no target and
offers no way to verify a fix.  A proposed name plus an existence assertion gives
repair both, and splitting "the variable should exist" from "its value should
drop" separates two defects whose fixes differ (add a declaration vs add an
effect) so each can be verified on its own.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionCheckPublic,
    AssertionExecutionPublic,
    AssertionScript,
    AssertionSpec,
)


def spec(**overrides):
    base = dict(
        assertion_id="AST-REQ-001-1",
        requirement_id="REQ-001",
        description="检查模型是否声明了表示机群数量的变量",
        expression='variable_declared(variable="uav_count") is True',
        failure_message="[REQ-001][AST-REQ-001-1] 模型未声明承载机群数量的变量",
        evidence_family="structure",
        role="precondition",
        coverage_key="uav-count-declared",
        aggregation_group="REQ-001:all",
        rationale=(
            "NL 第 4 行 the number of UAVs in the swarm decreases accordingly 要求一个"
            "机群数量；declared_model_vocabulary 的 variables 为空，故提议以 uav_count 承载。"
        ),
    )
    base.update(overrides)
    return AssertionSpec(**base)


# --------------------------------------------------------------------------
# The three new fields
# --------------------------------------------------------------------------


def test_precondition_is_a_legal_role():
    assert spec().role == "precondition"


def test_depends_on_is_a_plain_list_of_ids():
    """Not a mapping keyed on a required truth value.

    A "run only when the prerequisite is false" branch was considered and
    dropped: it is expressible as two unconditional assertions, and carrying a
    truth value in the edge makes both the graph semantics and the repair stage's
    reading of it harder.
    """

    s = spec(depends_on=("AST-REQ-001-0",))
    assert s.depends_on == ("AST-REQ-001-0",)
    assert isinstance(s.depends_on, tuple)
    # Default is empty, so an ordinary assertion needs no change.
    assert spec().depends_on == ()


def test_rationale_is_required():
    """A precondition standing in for an absent term must cite its NL ground.

    That citation is what the reviewer checks; without it the field would be a
    restatement of `description` and the check would have nothing to verify.
    """

    with pytest.raises(ValidationError):
        spec(rationale="")
    payload = {k: v for k, v in spec().__dict__.items() if k != "rationale"}
    payload.pop("schema_name", None)
    payload.pop("schema_version", None)
    with pytest.raises(ValidationError):
        AssertionSpec(**payload)


def test_description_and_rationale_are_separate_fields():
    """One says what is checked, the other why -- a producer given one writes only the first."""

    s = spec()
    assert "声明" in s.description
    assert "NL 第 4 行" in s.rationale
    assert s.description != s.rationale


def test_strategies_maps_requirement_to_its_decomposition_intent():
    script = AssertionScript(
        revision=1,
        assertions=(spec(),),
        strategies={
            "REQ-001": (
                "拆两条：数量变量的存在性是效果可判定的前提，二者修复方式不同"
                "（加声明 vs 加 effect），故分开以便逐条验收。"
            )
        },
    )
    assert "REQ-001" in script.strategies
    # Optional, so existing artifacts keep validating.
    assert AssertionScript(revision=1, assertions=(spec(),)).strategies == {}


# --------------------------------------------------------------------------
# `blocked` as an execution status
# --------------------------------------------------------------------------


def test_blocked_is_a_legal_execution_status():
    e = AssertionExecutionPublic(
        assertion_id="AST-REQ-001-2",
        requirement_id="REQ-001",
        role="primary",
        status="blocked",
    )
    assert e.status == "blocked"


def test_a_blocked_item_does_not_make_the_script_invalid():
    """The script ran fine; one item simply had an unmet prerequisite.

    Treating it as invalid would send the whole script back for a repair nobody
    can make -- the deadlock class §10.9 records.  The prerequisite's own `False`
    is the finding, and it is reported on its own.
    """

    check = AssertionCheckPublic(
        script_hash="h" * 8,
        tool_env_hash="t" * 8,
        status="executable",
        executions=(
            AssertionExecutionPublic(
                assertion_id="AST-REQ-001-0",
                requirement_id="REQ-001",
                role="precondition",
                status="executable",
            ),
            AssertionExecutionPublic(
                assertion_id="AST-REQ-001-1",
                requirement_id="REQ-001",
                role="primary",
                status="blocked",
            ),
        ),
    )
    assert check.status == "executable"


def test_an_invalid_item_still_makes_the_script_invalid():
    """Control: relaxing the rule for `blocked` must not relax it for `invalid`."""

    with pytest.raises(ValidationError):
        AssertionCheckPublic(
            script_hash="h" * 8,
            tool_env_hash="t" * 8,
            status="executable",
            executions=(
                AssertionExecutionPublic(
                    assertion_id="AST-REQ-001-1",
                    requirement_id="REQ-001",
                    status="invalid",
                    error="boom",
                ),
            ),
        )


def test_an_invalid_check_still_requires_an_invalid_item():
    """And a `blocked` item alone does not satisfy that requirement."""

    with pytest.raises(ValidationError):
        AssertionCheckPublic(
            script_hash="h" * 8,
            tool_env_hash="t" * 8,
            status="invalid",
            executions=(
                AssertionExecutionPublic(
                    assertion_id="AST-REQ-001-1",
                    requirement_id="REQ-001",
                    status="blocked",
                ),
            ),
        )
