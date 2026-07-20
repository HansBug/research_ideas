from __future__ import annotations

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
    assert outcome.run_outcome == "complete_coverage_zero_issue"
    assert [root.node_id for root in outcome.regression_guard_projection] == [
        "ROOT-001"
    ]


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
