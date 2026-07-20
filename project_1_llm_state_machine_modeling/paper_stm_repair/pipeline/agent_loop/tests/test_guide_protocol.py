from __future__ import annotations

from paper_stm_repair_loop.agents.discover import _build_tools

from v2_helpers import (
    attach_passing_review,
    expressions_from_plan,
    make_controller,
    make_plan,
)


def test_guide_first_and_task_second_are_runtime_enforced(tmp_path):
    controller = make_controller(tmp_path)
    tools, resolver = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    blocked = tools["read_task"].invoke({"reason": "过早读取任务。"})
    assert blocked["execution_status"] == "mandatory_tool_rejected"
    assert blocked["required_tool"] == "read_fcstm_guide"
    assert resolver() == "read_fcstm_guide"

    guide = tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    assert guide["sha256"]
    assert resolver() == "read_task"
    task = tools["read_task"].invoke({"reason": "读取冻结任务。"})
    assert tuple(task) == (
        "stage",
        "loop_no",
        "model",
        "targets",
        "current_records",
        "readable_history",
    )


def test_registered_assertions_are_forced_one_by_one(tmp_path):
    controller = make_controller(tmp_path)
    review_gate = attach_passing_review(controller)
    tools, resolver = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    accepted = tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "注册完整计划。"}
    )
    assert accepted["accepted"] is True
    assert resolver() == "eval_assert"
    blocked = tools["query_model"].invoke(
        {
            "query_kind": "states",
            "root_node_ids": ["ROOT-001"],
            "reason": "错误地绕过待执行断言。",
        }
    )
    assert blocked["execution_status"] == "mandatory_tool_rejected"
    for expression in expressions_from_plan(plan):
        evaluated = tools["eval_assert"].invoke(
            {
                "assert": expression,
                "reason": "逐条执行完整断言。",
            }
        )
        assert evaluated["match_status"] == "matches"
    assert resolver() == "review_discovery_coverage"
    reviewed = tools["review_discovery_coverage"].invoke(
        {"reason": "全部最新断言已执行，开始独立覆盖审查。"}
    )
    assert reviewed["passed"] is True
    assert review_gate.current_passed() is True
    assert resolver() is None
