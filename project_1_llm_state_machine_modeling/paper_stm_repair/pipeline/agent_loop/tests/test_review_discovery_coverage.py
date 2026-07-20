from __future__ import annotations

import pytest

from paper_stm_repair_loop.schemas.coverage_review import (
    CoverageReviewFinding,
    CoverageReviewVerdict,
)
from paper_stm_repair_loop.tools.review_discovery_coverage import CoverageReviewGate

from v2_helpers import expressions_from_plan, make_controller, make_plan


def _verdict(kind, payload, *, passed=True, omit_requirement=False):
    contract = payload["review_contract"]
    requirement_ids = list(contract["required_requirement_ids"])
    if omit_requirement:
        requirement_ids = requirement_ids[1:]
    findings = []
    if not passed:
        findings = [
            CoverageReviewFinding(
                finding_id="REVIEW-GAP-001",
                category="possible_false_negative",
                related_requirement_ids=requirement_ids[:1],
                related_source_fact_ids=contract["required_source_fact_ids"][:1],
                related_root_ids=contract["required_root_ids"][:1],
                related_assertion_chain_ids=["ASSERT-001"],
                problem="当前断言只检查局部迁移关系，没有证明完整触发路径和目标行为。",
                missed_behavior_risk="若其他合法入口或返回路径未检查，Discover 会错误发布零漏项结论。",
                recommended_action="使用 observe_trace 构造补充路径，再修订断言并逐条重新执行。",
                recommended_tools=["observe_trace", "revise_assertion", "eval_assert"],
                pass_criteria="新增证据必须覆盖遗漏路径，最新断言终态执行后再次通过双重审查。",
            )
        ]
    return CoverageReviewVerdict(
        review_kind=kind,
        passed=passed,
        reviewed_segment_ids=contract["required_segment_ids"],
        reviewed_requirement_ids=requirement_ids,
        reviewed_source_fact_ids=contract["required_source_fact_ids"],
        reviewed_root_ids=contract["required_root_ids"],
        findings=findings,
        coverage_analysis=(
            "已逐条审计全部 NL 原子义务、行为事实、断言、真实执行和 issue 投影，"
            "并主动检查弱命题、遗漏路径、潜在误报和潜在漏报。"
        ),
        rationale=(
            "当前完整证据台账满足逐项覆盖、语义强度和对抗反例审查的严格通过条件。"
            if passed
            else "当前证据存在必须补查的覆盖缺口，不能支持全覆盖或零漏项结论。"
        ),
    )


def _ready_controller(tmp_path):
    controller = make_controller(tmp_path)
    plan = make_plan(controller)
    registry = controller.require_registry()
    assert registry.register_plan(plan, reason="注册完整测试计划。")["accepted"]
    for expression in expressions_from_plan(plan):
        assert (
            registry.eval_assert(expression, reason="逐条执行当前最新断言。")[
                "match_status"
            ]
            == "matches"
        )
    return controller, registry, plan


def test_dual_review_failure_blocks_submit_and_returns_actionable_guidance(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        return _verdict(
            kind,
            payload,
            passed=kind != "adversarial_falsification",
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    registry.semantic_review_gate = gate
    reviewed = gate.review(reason="主动寻找漏报并给出补查动作。")

    assert reviewed["passed"] is False
    assert reviewed["required_actions"][0]["recommended_tools"] == [
        "observe_trace",
        "revise_assertion",
        "eval_assert",
    ]
    assert reviewed["required_actions"][0]["pass_criteria"]
    assert registry.assert_submit_allowed()["submit_allowed"] is False


def test_failed_review_finding_requires_a_ledger_id():
    with pytest.raises(
        ValueError,
        match="coverage review finding must reference a current ledger ID",
    ):
        CoverageReviewFinding(
            finding_id="REVIEW-GAP-UNGROUNDED",
            category="evidence_gap",
            problem="当前审查声称存在缺口，但没有指出台账中的任何受影响对象。",
            missed_behavior_risk="这种泛化意见无法指导补查，也无法证明漏报风险来自当前任务。",
            recommended_action="补充具体关联 ID 后，再给出针对该对象的检查与断言修订动作。",
            recommended_tools=["query_model"],
            pass_criteria="至少绑定一个当前台账 ID，并给出该对象可机械复核的通过条件。",
        )


def test_review_schema_tells_reviewer_to_propose_coverage_improvements():
    schema = CoverageReviewFinding.model_json_schema()["properties"]

    assert "what additional" in schema["recommended_action"]["description"]
    assert "coverage gap is closed" in schema["pass_criteria"]["description"]


def test_review_rejects_finding_that_invents_unknown_ledger_ids(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        contract = payload["review_contract"]
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=False,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[
                CoverageReviewFinding(
                    finding_id="REVIEW-GAP-UNKNOWN",
                    category="evidence_gap",
                    related_requirement_ids=["REQ-NOT-IN-LEDGER"],
                    problem="该 finding 使用了并不存在于当前冻结台账中的 requirement ID。",
                    missed_behavior_risk="若接受虚构 ID，审查意见无法关联真实义务并会污染证据链。",
                    recommended_action="仅使用 review_contract 中的真实 ID 重写审查意见。",
                    recommended_tools=["register_coverage_plan"],
                    pass_criteria="所有 finding 关联 ID 都必须属于当前冻结台账。",
                )
            ],
            coverage_analysis=(
                "已逐条审查当前台账中的 Segment、Requirement、SourceFact、Root 和"
                "断言执行结果，但故意构造一个未知 requirement ID 以验证门禁会失败关闭。"
            ),
            rationale=(
                "未知 ID 无法关联当前冻结任务中的真实义务，因此不得被当作可执行覆盖建议。"
            ),
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    registry.semantic_review_gate = gate
    reviewed = gate.review(reason="拒绝虚构关联 ID。")

    assert reviewed["passed"] is False
    assert any(
        "finding_unknown_requirement_ids" in error
        for error in reviewed["programmatic_errors"]
    )


def test_reviewer_cannot_pass_while_omitting_any_controller_required_id(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=lambda kind, payload, _attempt: _verdict(
            kind, payload, omit_requirement=True
        ),
    )
    registry.semantic_review_gate = gate
    reviewed = gate.review(reason="尝试漏掉一个 requirement ID。")

    assert reviewed["passed"] is False
    assert any(
        "requirement_review_set_mismatch" in error
        for error in reviewed["programmatic_errors"]
    )
    assert reviewed["required_actions"]
    assert reviewed["required_actions"][0]["recommended_tools"] == [
        "review_discovery_coverage"
    ]
    assert reviewed["required_actions"][0]["recommended_action"]
    assert reviewed["required_actions"][0]["pass_criteria"]
    assert registry.assert_submit_allowed()["submit_allowed"] is False


def test_review_pass_is_invalidated_by_any_later_evaluation(tmp_path):
    controller, registry, plan = _ready_controller(tmp_path)
    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=lambda kind, payload, _attempt: _verdict(kind, payload),
    )
    registry.semantic_review_gate = gate
    reviewed = gate.review(reason="对当前完整台账执行双重审查。")
    assert reviewed["passed"] is True
    assert registry.assert_submit_allowed()["submit_allowed"] is True

    registry.eval_assert(
        expressions_from_plan(plan)[0],
        reason="review 后新增一次执行，必须使旧审查指纹失效。",
    )

    assert gate.current_passed() is False
    blocked = registry.assert_submit_allowed()
    assert blocked["submit_allowed"] is False
    assert "current_semantic_coverage_review_must_pass" in blocked["limitations"]


def test_review_rejects_nonterminal_or_unregistered_ledger_without_llm_call(tmp_path):
    controller = make_controller(tmp_path)
    registry = controller.require_registry()
    calls = []
    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=lambda *args: calls.append(args),
    )
    registry.semantic_review_gate = gate

    before_plan = gate.review(reason="尚未注册时不得审查。")
    assert before_plan["execution_status"] == "prerequisite_required"
    assert before_plan["required_actions"] == [
        {
            "action_id": "REVIEW-PREREQ-001",
            "error": "coverage_plan_not_registered",
            "recommended_tools": ["register_coverage_plan"],
            "recommended_action": (
                "Register the complete coverage plan, preserving every frozen NL "
                "obligation and behavior SourceFact, before requesting review."
            ),
            "pass_criteria": "register_coverage_plan returns accepted=true.",
        }
    ]
    assert calls == []

    plan = make_plan(controller)
    assert registry.register_plan(plan, reason="注册但不执行断言。")["accepted"]
    before_eval = gate.review(reason="断言尚未终态时不得审查。")
    assert before_eval["execution_status"] == "prerequisite_required"
    assert before_eval["required_actions"][0]["recommended_tools"] == ["eval_assert"]
    assert before_eval["required_actions"][0]["pass_criteria"]
    assert calls == []
