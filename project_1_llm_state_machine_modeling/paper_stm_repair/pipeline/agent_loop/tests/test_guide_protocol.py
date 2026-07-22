from __future__ import annotations

import json

import pytest

from paper_stm_repair_loop.agents.discover import _build_tools
from paper_stm_repair_loop.tools.review_discovery_coverage import (
    CoverageReviewGate,
    RetryableCoverageReviewerError,
)

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
    assert blocked["required_actions"][0]["recommended_tools"] == [
        "read_fcstm_guide"
    ]
    assert "Do not repeat read_task" in blocked["required_actions"][0][
        "recommended_action"
    ]
    assert blocked["required_actions"][0]["pass_criteria"]
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


def test_inconclusive_eval_finishes_missing_worklist_before_revision(tmp_path):
    controller = make_controller(tmp_path)
    tools, resolver = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    first = plan["logical_assertions"][0]
    first["required_function_families"] = ["relation", "structure"]
    assert tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "注册含一个证据家族不足断言的完整计划。"}
    )["accepted"]

    first_result = tools["eval_assert"].invoke(
        {"assert": first["assert"], "reason": "首次执行后应为 inconclusive。"}
    )
    assert first_result["match_status"] == "inconclusive"
    assert resolver() == "eval_assert"
    action = first_result["required_actions"][0]
    assert action["recommended_tools"] == ["eval_assert"]
    assert "Do not repeat" in action["recommended_action"]
    assert plan["logical_assertions"][1]["assert"] in action["recommended_action"]
    assert "will select revise_assertion" in action["recommended_action"]

    for item in plan["logical_assertions"][1:]:
        result = tools["eval_assert"].invoke(
            {"assert": item["assert"], "reason": "完成剩余断言的首次执行。"}
        )
        assert result["match_status"] in {"matches", "contradicts"}
    assert resolver() == "revise_assertion"

    revised_expression = (
        "states(name='Root.Active')[0].is_leaf is True and " + str(first["assert"])
    )
    revised = tools["revise_assertion"].invoke(
        {
            "assertion_chain_id": first["assertion_chain_id"],
            "assert": revised_expression,
            "reason": "补齐缺失的 structure 证据家族。",
        }
    )
    assert revised["accepted"] is True
    assert resolver() == "eval_assert"


def test_review_prerequisite_rejection_guides_registration_without_resolver_takeover(
    tmp_path,
):
    controller = make_controller(tmp_path)
    attempt_log = []
    tools, resolver = _build_tools(
        controller, controller.task_snapshot(), attempt_log
    )
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})

    rejected = tools["review_discovery_coverage"].invoke(
        {"reason": "错误地在计划注册前发起审查。"}
    )
    assert rejected["execution_status"] == "prerequisite_required"
    assert resolver() is None
    action = rejected["required_actions"][0]
    assert action["recommended_tools"] == ["register_coverage_plan"]
    assert "Do not call review_discovery_coverage again" in action[
        "recommended_action"
    ]
    assert action["pass_criteria"] == "register_coverage_plan returns accepted=true."


def test_agent_tool_schema_and_domain_rejections_return_recovery_guidance(tmp_path):
    controller = make_controller(tmp_path)
    tools, resolver = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    assert resolver() is None

    schema_rejected = json.loads(
        tools["query_model"].invoke(
            {
                "query_kind": "states",
                "offset": 0,
                "limit": 50,
                "root_node_ids": [],
            }
        )
    )
    assert schema_rejected["execution_status"] == "invalid_arguments"
    assert schema_rejected["required_actions"][0]["recommended_tools"] == [
        "query_model"
    ]
    assert "Do not repeat the rejected JSON unchanged" in schema_rejected[
        "required_actions"
    ][0]["recommended_action"]

    request = {
        "query_kind": "states",
        "name_contains": None,
        "offset": 0,
        "limit": 500,
        "root_node_ids": [],
        "reason": "读取一次完整状态页。",
    }
    assert tools["query_model"].invoke(request)["execution_status"] == "completed"
    domain_rejected = tools["query_model"].invoke(request)
    assert domain_rejected["execution_status"] == "invalid_arguments"
    assert domain_rejected["required_actions"][0]["recommended_tools"] == [
        "query_model"
    ]
    assert "materially changed request" in domain_rejected["required_actions"][0][
        "recommended_action"
    ]


def test_unknown_eval_expression_guides_exact_retry_not_assertion_revision(tmp_path):
    controller = make_controller(tmp_path)
    tools, _ = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    assert tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "注册完整计划。"}
    )["accepted"]

    rejected = tools["eval_assert"].invoke(
        {"assert": "states() == ()", "reason": "故意提交未注册表达式。"}
    )
    assert rejected["execution_status"] == "invalid_arguments"
    action = rejected["required_actions"][0]
    assert action["recommended_tools"] == ["eval_assert"]
    assert "copy one latest assertion expression exactly" in action[
        "recommended_action"
    ]
    assert "Do not revise" in action["recommended_action"]


def test_failed_review_allows_all_actions_before_next_review(tmp_path):
    controller = make_controller(tmp_path)
    review_gate = attach_passing_review(controller)
    tools, resolver = _build_tools(
        controller, controller.task_snapshot(), [], review_gate
    )
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    assert tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "注册完整计划。"}
    )["accepted"]
    expressions = expressions_from_plan(plan)
    for expression in expressions:
        assert tools["eval_assert"].invoke(
            {"assert": expression, "reason": "执行初始断言。"}
        )["match_status"] == "matches"
    expression = expressions[0]

    review_gate.latest_result = {
        "execution_status": "completed",
        "passed": False,
        "reviewed_state_fingerprint": review_gate.state_fingerprint(),
        "programmatic_errors": [],
        "required_actions": [{"finding_id": "F-001"}, {"finding_id": "F-002"}],
    }
    assert resolver() is None

    revised_expression = f"({expression})"
    assert tools["revise_assertion"].invoke(
        {
            "assertion_chain_id": "ASSERT-001",
            "assert": revised_expression,
            "reason": "处理第一轮 review 的一项行动，同时保留其他待办。",
        }
    )["accepted"]
    assert resolver() == "eval_assert"
    assert tools["eval_assert"].invoke(
        {"assert": revised_expression, "reason": "执行最新修订。"}
    )["match_status"] == "matches"
    assert resolver() is None


def test_terminal_reviewer_failure_stops_before_another_model_turn(tmp_path):
    controller = make_controller(tmp_path)

    def failing_runner(kind, _payload, _attempt):
        raise RetryableCoverageReviewerError(
            f"coverage_reviewer_failed:{kind}:RemoteProtocolError"
        )

    gate = CoverageReviewGate(
        registry=controller.require_registry(),
        task_snapshot=controller.task_snapshot(),
        runner=failing_runner,
    )
    tools, resolver = _build_tools(
        controller,
        controller.task_snapshot(),
        [],
        gate,
    )
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    accepted = tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "注册完整计划。"}
    )
    assert accepted["accepted"] is True
    for expression in expressions_from_plan(plan):
        tools["eval_assert"].invoke(
            {"assert": expression, "reason": "逐条执行完整断言。"}
        )

    first = tools["review_discovery_coverage"].invoke(
        {"reason": "第一次 reviewer 传输失败允许重试。"}
    )
    assert first["execution_status"] == "retryable_reviewer_failure"
    assert resolver() == "review_discovery_coverage"
    second = tools["review_discovery_coverage"].invoke(
        {"reason": "第二次相同失败终止当前 attempt。"}
    )
    assert second["execution_status"] == "reviewer_contract_failure"
    with pytest.raises(RuntimeError, match="discover_reviewer_contract_failure"):
        resolver()


def test_registration_schema_reject_explains_how_to_recover(tmp_path):
    controller = make_controller(tmp_path)
    tools, _ = _build_tools(controller, controller.task_snapshot(), [])
    tools = {tool.name: tool for tool in tools}
    tools["read_fcstm_guide"].invoke({"reason": "先读取官方语法。"})
    tools["read_task"].invoke({"reason": "读取冻结任务。"})
    plan = make_plan(controller)
    duplicate = dict(plan["logical_assertions"][0])
    duplicate["assertion_chain_id"] = "ASSERT-DUPLICATE"
    plan["logical_assertions"].append(duplicate)

    rejected = tools["register_coverage_plan"].invoke(
        {"plan": plan, "reason": "提交一个重复表达式以检查纠错引导。"}
    )
    payload = json.loads(rejected)
    assert payload["execution_status"] == "invalid_arguments"
    assert "ASSERT-001" in payload["errors"][0]
    assert "ASSERT-DUPLICATE" in payload["errors"][0]
    assert "ROOT-001" in payload["errors"][0]
    assert "CU-REQ-001" in payload["errors"][0]
    assert payload["required_actions"][0]["recommended_tools"] == [
        "register_coverage_plan"
    ]
    action = payload["required_actions"][0]
    assert "keep one chain and union the necessary basis IDs" in action[
        "recommended_action"
    ]
    assert "distinct positive predicates" in action["recommended_action"]
    assert "Do not change only whitespace" in action["recommended_action"]
    assert "Do not call review_discovery_coverage" in action["recommended_action"]
    assert "Every logical_assertion.assert string is unique" in action[
        "pass_criteria"
    ]
