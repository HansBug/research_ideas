from __future__ import annotations

import copy

import pytest
from pydantic import ValidationError

from paper_stm_repair_loop.agents.discover import _build_submit_schema
from paper_stm_repair_loop.schemas.discovery import DiscoverOutcome

from v2_helpers import (
    attach_passing_review,
    expressions_from_plan,
    make_controller,
    make_plan,
)


def test_controller_builds_only_mechanical_inputs_and_registry_projects(tmp_path):
    controller = make_controller(tmp_path)
    frozen = controller.prepare()
    assert [item.text for item in frozen.input_segments] == [
        "While Active, Power_Off must move the controller to Off."
    ]
    assert all("semantic_role" not in fact.payload for fact in frozen.source_facts)
    assert any(fact.fact_kind == "transition" for fact in frozen.source_facts)

    plan = make_plan(controller)
    registry = controller.require_registry()
    registered = registry.register_plan(plan, reason="注册完整测试计划。")
    assert registered["accepted"] is True
    assert registry.eval_runtime.environment.mapping.bindings["CU-REQ-001"]

    for expression in expressions_from_plan(plan):
        evaluated = registry.eval_assert(
            expression, reason="逐条执行完整正向命题。"
        )
        assert evaluated["match_status"] == "matches"
    review = attach_passing_review(controller)
    assert review.review(reason="独立复核完整当前台账。")["passed"] is True
    outcome = DiscoverOutcome.model_validate(controller.projection())
    assert outcome.run_outcome == "reviewer_accepted_zero_issue"
    assert [root.node_id for root in outcome.regression_guard_projection] == [
        "ROOT-001"
    ]


def test_structured_submission_validation_does_not_append_duplicate_gate_records(
    tmp_path,
):
    controller = make_controller(tmp_path)
    plan = make_plan(controller)
    registry = controller.require_registry()
    assert registry.register_plan(plan, reason="注册完整测试计划。")["accepted"]
    for expression in expressions_from_plan(plan):
        assert registry.eval_assert(
            expression, reason="逐条执行完整正向命题。"
        )["match_status"] == "matches"
    review = attach_passing_review(controller)
    assert review.review(reason="独立复核完整当前台账。")["passed"]
    projection = controller.projection(record_gate=False)
    schema = _build_submit_schema(controller)
    gate_records_before = sum(
        item["record_type"] == "discovery_submit_gate_checked"
        for item in registry.records
    )

    payload = {
        "submission_type": "submit_discovery",
        "outcome": projection,
        "reason": "结构化输出可重复校验，但不重复写入 submit gate 记录。",
    }
    for _ in range(3):
        assert schema.model_validate(payload).outcome.run_outcome == (
            "reviewer_accepted_zero_issue"
        )

    shortened_projection = copy.deepcopy(projection)
    shortened_projection.pop("coverage_requirement_coverage")
    shortened_projection["major_behavior_coverage_review"].pop("required")
    with pytest.raises(ValidationError) as exc_info:
        schema.model_validate(
            {
                **payload,
                "outcome": shortened_projection,
            }
        )
    error_message = str(exc_info.value)
    assert "field_mismatches=" in error_message
    assert "outcome.coverage_requirement_coverage" in error_message
    assert "outcome.major_behavior_coverage_review.required" in error_message
    assert "expected=true" in error_message
    assert "do not submit a shortened projection" in error_message

    gate_records_after = sum(
        item["record_type"] == "discovery_submit_gate_checked"
        for item in registry.records
    )
    assert gate_records_after == gate_records_before


def test_controller_does_not_split_conjunction_semantically(tmp_path):
    controller = make_controller(tmp_path)
    controller.case = controller.case.__class__(
        **{
            **controller.case.__dict__,
            "nl": "The count decreases and the controller returns to Idle.",
        }
    )
    frozen = controller.prepare()
    assert len(frozen.input_segments) == 1
    assert " and " in frozen.input_segments[0].text
