from __future__ import annotations

import contextvars

import pytest

from paper_stm_repair_loop.schemas.coverage_review import (
    CoverageImprovementStep,
    CoverageReviewFinding,
    CoverageReviewVerdict,
)
from paper_stm_repair_loop.tools.review_discovery_coverage import (
    CoverageReviewerContractError,
    CoverageReviewGate,
    LLMCoverageReviewRunner,
    RetryableCoverageReviewerError,
    _raise_classified_reviewer_error,
    _review_system_prompt,
)
from paper_stm_repair_loop.tools.register_coverage_plan import (
    RegisterCoveragePlanInput,
)

from v2_helpers import expressions_from_plan, make_controller, make_plan


def _steps(tools, related_id):
    suggested_arguments = {
        "query_model": {
            "query_kind": "transitions",
            "reason": f"检查 {related_id} 的精确结构范围。",
        },
        "observe_trace": {
            "question": f"{related_id} 的目标路径是否可执行？",
            "root_node_ids": ["ROOT-TO-RESOLVE"],
            "cycles": [[], ["Root.Trigger"]],
            "reason": f"补充 {related_id} 的路径证据。",
        },
        "lookup_source_trace": {
            "element_refs": ["state:Root.Target"],
            "direction": "fcstm_to_source",
            "reason": f"核对 {related_id} 的来源归因。",
        },
        "read_fbmcq_guide": {"reason": f"为 {related_id} 撰写合法性质。"},
        "register_coverage_plan": {
            "plan": {
                "segment_dispositions": [],
                "fact_dispositions": [],
                "coverage_units": [],
                "proposition_roots": [],
                "logical_assertions": [],
                "rationale": f"补充 {related_id} 的完整 CoveragePlan。",
            },
            "reason": f"闭合 {related_id}。",
        },
        "revise_assertion": {
            "assertion_chain_id": "ASSERT-001",
            "assert": "transition_exists(source='Root.A', event='Root.go', target='Root.B')",
            "reason": f"加强 {related_id} 的正向命题。",
        },
        "eval_assert": {
            "assert": "transition_exists(source='Root.A', event='Root.go', target='Root.B')",
            "reason": f"执行 {related_id} 的最新断言。",
        },
    }
    return [
        CoverageImprovementStep(
            tool=tool,
            related_ids=[related_id],
            objective=f"为 {related_id} 增加可执行覆盖证据并消除当前 finding。",
            suggested_arguments=suggested_arguments[tool],
            expected_observation=(
                f"{related_id} 对应的 assertion 得到 terminal bool 和可追溯执行记录。"
            ),
        )
        for tool in tools
    ]


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
                coverage_dimensions=["model_behavior", "assertion_strength"],
                problem="当前断言只检查局部迁移关系，没有证明完整触发路径和目标行为。",
                missed_behavior_risk="若其他合法入口或返回路径未检查，Discover 会错误发布零漏项结论。",
                recommended_action=(
                    f"针对 {requirement_ids[0]} 使用 observe_trace 构造补充路径，再用 "
                    "revise_assertion 修订断言，最后用 eval_assert 逐条重新执行。"
                ),
                recommended_tools=["observe_trace", "revise_assertion", "eval_assert"],
                recommended_steps=_steps(
                    ["observe_trace", "revise_assertion", "eval_assert"],
                    requirement_ids[0],
                ),
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


def test_nested_llm_reviewer_runs_in_fresh_callback_context(monkeypatch, tmp_path):
    marker = contextvars.ContextVar("parent_agent_callback", default="isolated")
    token = marker.set("outer-agent")
    observed: list[str] = []
    verdict = CoverageReviewVerdict(
        review_kind="semantic_coverage",
        passed=True,
        coverage_analysis=(
            "已逐项检查当前主要行为义务、断言与执行证据；此测试只验证嵌套 reviewer "
            "不会继承外层 Agent callback context，避免污染外层工具生命周期。"
        ),
        rationale="独立 reviewer 上下文必须与外层 Agent 审计上下文隔离。",
    )

    class FakeResult:
        status = "success"
        real_llm = True
        error = None

        def require_output(self):
            return verdict

    class FakeApp:
        def run(self, *_args, **_kwargs):
            observed.append(marker.get())
            return FakeResult()

    monkeypatch.setattr(
        "paper_stm_repair_loop.tools.review_discovery_coverage.AgentApp.from_registry",
        lambda *_args, **_kwargs: FakeApp(),
    )
    runner = LLMCoverageReviewRunner(
        llm_registry=object(),
        profiles={"semantic_coverage": "fake"},
        audit_root=tmp_path,
        content_language="zh-CN",
    )
    try:
        assert runner("semantic_coverage", {}, 1) == verdict
        assert observed == ["isolated"]
        assert marker.get() == "outer-agent"
    finally:
        marker.reset(token)


def test_review_verdict_cannot_pass_with_actionable_findings():
    finding = CoverageReviewFinding(
        finding_id="REVIEW-GAP-PASS-CONFLICT",
        category="possible_false_negative",
        related_requirement_ids=["REQ-001"],
        coverage_dimensions=["nl_semantics"],
        problem="当前主要行为义务仍有一个会影响结论的语义覆盖缺口。",
        missed_behavior_risk="若该缺口未补查，零问题结论会出现实质性的潜在漏报。",
        recommended_action="使用 query_model 补查 REQ-001 对应的精确模型行为。",
        recommended_tools=["query_model"],
        recommended_steps=_steps(["query_model"], "REQ-001"),
        pass_criteria="query_model 返回精确模型事实且后续断言产生 terminal bool 记录。",
    )

    with pytest.raises(ValueError, match="passed review cannot contain blocking findings"):
        CoverageReviewVerdict(
            review_kind="semantic_coverage",
            passed=True,
            findings=[finding],
            coverage_analysis=(
                "已检查主要行为及其证据链，但该结构化输出故意同时声明 passed "
                "并保留一个会影响主要结论的 finding，用于验证一致性门禁必须拒绝这种矛盾结果。"
            ),
            rationale="存在 actionable finding 时不得发布 reviewer-accepted coverage。",
        )


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
            coverage_dimensions=["assertion_strength"],
            problem="当前审查声称存在缺口，但没有指出台账中的任何受影响对象。",
            missed_behavior_risk="这种泛化意见无法指导补查，也无法证明漏报风险来自当前任务。",
            recommended_action="补充具体关联 ID 后，再给出针对该对象的检查与断言修订动作。",
            recommended_tools=["query_model"],
            recommended_steps=_steps(["query_model"], "REQ-001"),
            pass_criteria="至少绑定一个当前台账 ID，并给出该对象可机械复核的通过条件。",
        )


def test_review_schema_tells_reviewer_to_propose_coverage_improvements():
    schema = CoverageReviewFinding.model_json_schema()["properties"]

    assert "what additional" in schema["recommended_action"]["description"]
    assert "coverage gap is closed" in schema["pass_criteria"]["description"]
    assert "sentinel variables" in schema["coverage_dimensions"]["description"]
    assert "Every recommended tool" in schema["recommended_steps"]["description"]


@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        (
            "query_model",
            {"query_kind": "not_a_real_kind", "reason": "invalid enum"},
        ),
        (
            "query_model",
            {
                "query_kind": "states",
                "offset": -1,
                "limit": 501,
                "reason": "invalid deterministic range",
            },
        ),
        (
            "observe_trace",
            {
                "question": "check path",
                "root_node_ids": "ROOT-1",
                "cycles": "not-a-cycle-list",
                "reason": "invalid collection types",
            },
        ),
        (
            "lookup_source_trace",
            {
                "element_refs": "not-a-list",
                "direction": "sideways",
                "reason": "invalid direction and refs",
            },
        ),
        (
            "lookup_source_trace",
            {
                "element_refs": [],
                "direction": "fcstm_to_source",
                "reason": "empty refs are not executable",
            },
        ),
        (
            "lookup_source_trace",
            {
                "element_refs": [""],
                "direction": "fcstm_to_source",
                "reason": "blank refs are not executable",
            },
        ),
        (
            "lookup_source_trace",
            {
                "element_refs": ["   "],
                "direction": "fcstm_to_source",
                "reason": "whitespace refs are not executable",
            },
        ),
    ],
)
def test_coverage_improvement_step_reuses_strict_tool_argument_contracts(
    tool, arguments
):
    with pytest.raises(ValueError, match="invalid suggested_arguments"):
        CoverageImprovementStep(
            tool=tool,
            related_ids=["REQ-001"],
            objective="为 REQ-001 增加一项可以真正执行的覆盖检查。",
            suggested_arguments=arguments,
            expected_observation="REQ-001 对应断言产生 terminal bool 执行记录。",
        )


def test_register_plan_recommendation_uses_real_tool_input_contract():
    step = _steps(["register_coverage_plan"], "REQ-001")[0]

    validated = RegisterCoveragePlanInput.model_validate(step.suggested_arguments)

    assert validated.plan.rationale
    assert validated.reason


def test_provider_failure_returns_retry_action_without_raising(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)
    before_fingerprint = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=lambda *_args: None,
    ).state_fingerprint()

    def flaky_runner(kind, _payload, _attempt):
        raise RetryableCoverageReviewerError(
            "coverage_reviewer_failed:semantic_coverage:{'code': 'provider_error', "
            "'details': {'type': 'RemoteProtocolError', 'message': 'incomplete chunked read'}}"
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=flaky_runner,
    )
    registry.semantic_review_gate = gate

    reviewed = gate.review(reason="provider stream 临时失败时必须结构化重试。")

    assert reviewed["execution_status"] == "retryable_reviewer_failure"
    assert reviewed["passed"] is False
    assert reviewed["reviewed_state_fingerprint"] == before_fingerprint
    assert reviewed["required_actions"][0]["recommended_tools"] == [
        "review_discovery_coverage"
    ]
    assert reviewed["required_actions"][0]["coverage_dimensions"] == [
        "reviewer_infrastructure"
    ]
    assert gate.current_passed() is False
    assert gate.state_fingerprint() == before_fingerprint
    assert registry.records[-1]["record_type"] == "discovery_coverage_review_retry_required"


def test_second_retryable_reviewer_failure_terminates_same_fingerprint(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def flaky_runner(kind, _payload, _attempt):
        raise RetryableCoverageReviewerError(
            f"coverage_reviewer_failed:{kind}:RemoteProtocolError"
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=flaky_runner,
    )
    registry.semantic_review_gate = gate

    first = gate.review(reason="第一次 provider 中断允许同指纹重试。")
    second = gate.review(reason="第二次同指纹中断必须终止当前 attempt。")

    assert first["execution_status"] == "retryable_reviewer_failure"
    assert second["execution_status"] == "reviewer_contract_failure"
    assert gate.has_terminal_failure() is True
    assert second["required_actions"][0]["recommended_tools"] == []


def test_review_finding_rejects_fbmcq_as_nl_interpreter():
    with pytest.raises(ValueError, match="natural-language interpreter"):
        CoverageReviewFinding(
            finding_id="REVIEW-FBMCQ-NL",
            category="unsupported_issue_projection",
            related_requirement_ids=["REQ-001"],
            coverage_dimensions=["nl_semantics"],
            problem="审查意见试图用形式化工具解释 NL 原文含义，越过方法边界。",
            missed_behavior_risk="若把 FBMCQ 当自然语言裁判，会把工具能力误写成需求语义证据。",
            recommended_action="使用 read_fbmcq_guide 和 FBMCQ 解释 NL 原文是否要求变量递减。",
            recommended_tools=["read_fbmcq_guide"],
            recommended_steps=_steps(["read_fbmcq_guide"], "REQ-001"),
            pass_criteria="FBMCQ 对自然语言解释给出答案后再决定 issue projection。",
        )

    with pytest.raises(ValueError, match="natural-language interpreter"):
        CoverageReviewFinding(
            finding_id="REVIEW-FBMCQ-NL-REVERSED",
            category="unsupported_issue_projection",
            related_requirement_ids=["REQ-001"],
            coverage_dimensions=["nl_semantics"],
            problem="审查意见把形式化性质语法指南误当成自然语言语义裁判。",
            missed_behavior_risk="这种逆向用法会把工具语法能力错误升级成需求解释证据。",
            recommended_action="针对 NL 原文使用 read_fbmcq_guide 进行解释并决定其含义。",
            recommended_tools=["read_fbmcq_guide"],
            recommended_steps=_steps(["read_fbmcq_guide"], "REQ-001"),
            pass_criteria="read_fbmcq_guide 返回对 NL 原文的唯一语义解释。",
        )


def test_review_finding_rejects_direct_projection_state_mutation():
    with pytest.raises(ValueError, match="projection state directly"):
        CoverageReviewFinding(
            finding_id="REVIEW-PROJECTION-MUTATION",
            category="unsupported_issue_projection",
            related_root_ids=["ROOT-001"],
            coverage_dimensions=["issue_projection_evidence"],
            problem="审查建议绕过断言和证据链，直接操作 Controller 投影状态。",
            missed_behavior_risk="直接改投影会破坏 append-only 证据链和当前台账闭包。",
            recommended_action="将 issue projection 的 runtime_issue_assessment 调整为 confirmed。",
            recommended_tools=["query_model"],
            recommended_steps=_steps(["query_model"], "ROOT-001"),
            pass_criteria="Controller projection 状态从 ok 改为 confirmed。",
        )

    with pytest.raises(ValueError, match="projection state directly"):
        CoverageReviewFinding(
            finding_id="REVIEW-PROJECTION-MUTATION-REVERSED",
            category="unsupported_issue_projection",
            related_root_ids=["ROOT-001"],
            coverage_dimensions=["issue_projection_evidence"],
            problem="审查建议先写动作再写字段名，仍然是在绕过证据链直接修改投影。",
            missed_behavior_risk="若逆序措辞可绕过，错误 issue 会进入 Repair 并污染实验统计。",
            recommended_action=(
                "使用 query_model 检查 ROOT-001，然后把 confirmed 写入 "
                "runtime_issue_assessment。"
            ),
            recommended_tools=["query_model"],
            recommended_steps=_steps(["query_model"], "ROOT-001"),
            pass_criteria="ROOT-001 的 runtime_issue_assessment 记录为 confirmed。",
        )


def test_review_finding_rejects_generic_non_executable_guidance():
    with pytest.raises(ValueError, match="mechanically observable result"):
        CoverageReviewFinding(
            finding_id="REVIEW-GENERIC",
            category="evidence_gap",
            related_requirement_ids=["REQ-001"],
            coverage_dimensions=["assertion_strength"],
            problem="当前 finding 只有泛泛评价，没有给出能实际增加覆盖的具体检查动作。",
            missed_behavior_risk="主 Agent 无法从这种口号判断应补哪条路径、条件或证据。",
            recommended_action=(
                "使用 query_model 重新仔细检查 REQ-001 的当前需求和模型，并再次提交审查。"
            ),
            recommended_tools=["query_model"],
            recommended_steps=[
                CoverageImprovementStep(
                    tool="query_model",
                    related_ids=["REQ-001"],
                    objective="为 REQ-001 重新检查当前需求和模型并提高覆盖。",
                    suggested_arguments={
                        "query_kind": "states",
                        "reason": "重新仔细检查当前需求和模型。",
                    },
                    expected_observation="确认问题已经得到充分处理并形成一份完整总结说明。",
                )
            ],
            pass_criteria="确认模型状态问题已经得到处理并形成记录。",
        )


def test_review_gate_rejects_nl_strengthening_but_allows_explicit_universal_nl(
    tmp_path,
):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        contract = payload["review_contract"]
        finding = CoverageReviewFinding(
            finding_id="REVIEW-STRENGTHEN-ALL",
            category="missing_semantic_obligation",
            related_requirement_ids=contract["required_requirement_ids"][:1],
            coverage_dimensions=["nl_semantics"],
            problem="当前断言只检查一个状态，审查建议要求把范围扩展到 all states。",
            missed_behavior_risk="若原文没有全称量词，这种建议会制造 source-level false positive。",
            recommended_action=(
                f"针对 {contract['required_requirement_ids'][0]} 使用 revise_assertion "
                "将命题强化为 all states，再用 eval_assert 执行。"
            ),
            recommended_tools=["revise_assertion", "eval_assert"],
            recommended_steps=_steps(
                ["revise_assertion", "eval_assert"],
                contract["required_requirement_ids"][0],
            ),
            pass_criteria="eval_assert 对 all states 断言返回 terminal bool。",
        )
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=False,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[finding],
            coverage_analysis=(
                "已完整审查全部当前台账对象、全部最新断言及其执行记录，并故意提出可能"
                "强化原文的全称建议，以验证 Controller 会结合冻结 NL 拒绝越界建议。"
            ),
            rationale="若建议超出冻结 NL，Controller 必须拒绝该 reviewer finding。",
        )

    snapshot = controller.task_snapshot()
    gate = CoverageReviewGate(registry=registry, task_snapshot=snapshot, runner=runner)
    rejected = gate.review(reason="原文没有全称量词。")
    assert any("finding_nl_strengthening" in item for item in rejected["programmatic_errors"])

    snapshot["current_records"]["nl"]["content"] = (
        "All states shall handle Power_Off. Another clause contains the reviewed behavior."
    )
    gate = CoverageReviewGate(registry=registry, task_snapshot=snapshot, runner=runner)
    unrelated = gate.review(reason="无关子句的全称量词不得授权当前 finding。")
    assert any(
        "finding_nl_strengthening" in item
        for item in unrelated["programmatic_errors"]
    )

    first_requirement = snapshot["current_records"]["coverage_requirements"][0]
    first_requirement["clause_text"] = "All states shall handle Power_Off."
    gate = CoverageReviewGate(registry=registry, task_snapshot=snapshot, runner=runner)
    allowed = gate.review(reason="关联 requirement 子句明示全称量词。")
    assert not any("finding_nl_strengthening" in item for item in allowed["programmatic_errors"])


def test_reviewer_prompt_calibrates_positive_conditions_and_completion_semantics():
    prompt = _review_system_prompt("semantic_coverage", "zh-CN")
    assert "正向条件义务不自动产生排他性负义务" in prompt
    assert "不得建议包含 is False" in prompt
    assert "completion transition" in prompt
    assert "不等于每个普通 cycle 都立即无条件触发" in prompt
    assert "只能 revise 已注册 assertion chain" in prompt
    assert "True 表示现有 Root 得到满足" in prompt


def test_review_gate_filters_unlicensed_negative_obligation(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        contract = payload["review_contract"]
        requirement_id = contract["required_requirement_ids"][0]
        root_id = contract["required_root_ids"][0]
        expression = (
            "simulate(cycles=[[], ['Root.Power_Off']])."
            "final.is_active('Root.Off') is False"
        )
        finding = CoverageReviewFinding(
            finding_id="REVIEW-UNLICENSED-NEGATIVE",
            category="possible_false_negative",
            related_requirement_ids=[requirement_id],
            related_root_ids=[root_id],
            related_assertion_chain_ids=["ASSERT-001"],
            coverage_dimensions=["nl_semantics", "assertion_strength"],
            problem="审查意见把一个正向条件扩大成了其他上下文不得发生的负义务。",
            missed_behavior_risk="若执行该建议，会把满足原文的模型误报为 source-level issue。",
            recommended_action=(
                f"使用 revise_assertion 修订 ASSERT-001，要求 {requirement_id} "
                "在当前路径不应到达 Root.Off，再用 eval_assert 执行。"
            ),
            recommended_tools=["revise_assertion", "eval_assert"],
            recommended_steps=[
                CoverageImprovementStep(
                    tool="revise_assertion",
                    related_ids=["ASSERT-001", requirement_id],
                    objective=(
                        "向现有正向 Root 添加原文并未授权的排他性负向路径义务。"
                    ),
                    suggested_arguments={
                        "assertion_chain_id": "ASSERT-001",
                        "assert": expression,
                        "reason": "要求未授权上下文不应到达目标状态。",
                    },
                    expected_observation=(
                        "revise_assertion 返回 accepted=true 并保存该负向表达式。"
                    ),
                ),
                CoverageImprovementStep(
                    tool="eval_assert",
                    related_ids=["ASSERT-001", root_id],
                    objective="执行新增的负向义务并产生一条可审计的 latest 结果。",
                    suggested_arguments={
                        "assert": expression,
                        "reason": "执行 latest 负向断言。",
                    },
                    expected_observation=(
                        "eval_assert 返回 completed 和 terminal bool 的执行记录。"
                    ),
                ),
            ],
            pass_criteria="latest assertion 包含 is False 且 eval_assert 完成执行。",
        )
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=False,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[finding],
            coverage_analysis=(
                "已逐项审查全部冻结 Segment、Requirement、SourceFact、Root、"
                "latest assertion 和真实执行记录，并故意提出未授权负义务，"
                "用于验证程序化 gate 会阻止 reviewer 强化正向 NL。"
            ),
            rationale="程序化 gate 应过滤该 finding。",
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    reviewed = gate.review(reason="拒绝把正向条件强化成排他负义务。")

    assert any(
        "finding_nl_strengthening" in error
        for error in reviewed["programmatic_errors"]
    )
    assert all(
        action.get("finding_id") != "REVIEW-UNLICENSED-NEGATIVE"
        for action in reviewed["required_actions"]
    )
    assert all(
        action["recommended_tools"] == ["review_discovery_coverage"]
        for action in reviewed["required_actions"]
    )


def test_review_gate_filters_revision_of_unknown_assertion_chain(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        contract = payload["review_contract"]
        requirement_id = contract["required_requirement_ids"][0]
        root_id = contract["required_root_ids"][0]
        expression = (
            "transition_exists(source='Root.Active', "
            "event='Root.Power_Off', target='Root.Off')"
        )
        finding = CoverageReviewFinding(
            finding_id="REVIEW-UNKNOWN-CHAIN",
            category="evidence_gap",
            related_requirement_ids=[requirement_id],
            related_root_ids=[root_id],
            related_assertion_chain_ids=["ASSERT-001"],
            coverage_dimensions=["assertion_strength"],
            problem="审查意见要求 revise 一个没有注册的 assertion chain。",
            missed_behavior_risk="主 Agent 无法执行该建议，会在同一 finding 上反复失败。",
            recommended_action=(
                f"使用 revise_assertion 修改 ASSERT-NEW-CHAIN 以覆盖 {requirement_id}，"
                "再使用 eval_assert 执行。"
            ),
            recommended_tools=["revise_assertion", "eval_assert"],
            recommended_steps=[
                CoverageImprovementStep(
                    tool="revise_assertion",
                    related_ids=["ASSERT-001", requirement_id],
                    objective=(
                        "尝试使用 revise_assertion 修改当前计划中不存在的 chain。"
                    ),
                    suggested_arguments={
                        "assertion_chain_id": "ASSERT-NEW-CHAIN",
                        "assert": expression,
                        "reason": "测试 unknown chain 校验。",
                        },
                        expected_observation=(
                            "revise_assertion 返回 accepted=true 和新的 assertion_version_id。"
                        ),
                ),
                CoverageImprovementStep(
                    tool="eval_assert",
                    related_ids=["ASSERT-001", root_id],
                    objective="尝试执行尚未形成合法 latest 版本的建议表达式。",
                    suggested_arguments={
                        "assert": expression,
                        "reason": "测试 unknown chain 校验。",
                    },
                    expected_observation=(
                        "只有 revision 指向已注册 chain 时才可能形成 latest 执行记录。"
                    ),
                ),
            ],
            pass_criteria=(
                "revise_assertion 对 ASSERT-NEW-CHAIN 返回 accepted=true，随后 "
                "eval_assert 返回 execution_status=completed 和 terminal bool。"
            ),
        )
        return CoverageReviewVerdict(
            review_kind=kind,
            passed=False,
            reviewed_segment_ids=contract["required_segment_ids"],
            reviewed_requirement_ids=contract["required_requirement_ids"],
            reviewed_source_fact_ids=contract["required_source_fact_ids"],
            reviewed_root_ids=contract["required_root_ids"],
            findings=[finding],
            coverage_analysis=(
                "已逐项审查全部冻结 Segment、Requirement、SourceFact、Root、"
                "latest assertion 和真实执行记录，并故意让建议引用不存在的"
                " assertion chain，用于验证程序化 gate 会过滤不可执行动作。"
            ),
            rationale="程序化 gate 应过滤该 finding。",
        )

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    reviewed = gate.review(reason="拒绝不可执行的新 chain 建议。")

    assert any(
        "finding_unknown_revise_assertion_chain" in error
        for error in reviewed["programmatic_errors"]
    )
    assert all(
        action.get("finding_id") != "REVIEW-UNKNOWN-CHAIN"
        for action in reviewed["required_actions"]
    )


def test_anti_gaming_finding_requires_anti_gaming_dimension():
    with pytest.raises(ValueError, match="anti_gaming coverage_dimensions"):
        CoverageReviewFinding(
            finding_id="REVIEW-SENTINEL",
            category="anti_gaming_risk",
            related_assertion_chain_ids=["ASSERT-001"],
            coverage_dimensions=["assertion_strength"],
            problem="断言只检查硬编码候选变量名，可能用哨兵变量制造稳定 False。",
            missed_behavior_risk="硬编码候选名会把未穷尽搜索伪装成模型行为缺失。",
            recommended_action=(
                "针对 ASSERT-001 使用 query_model 枚举全部 variables() 和 effect 字段，再用 "
                "revise_assertion 与 eval_assert 检查完整范围。"
            ),
            recommended_tools=["query_model", "revise_assertion", "eval_assert"],
            recommended_steps=_steps(
                ["query_model", "revise_assertion", "eval_assert"],
                "ASSERT-001",
            ),
            pass_criteria="新断言报告未过滤全集、候选集和每个 effect 的实际覆盖情况。",
        )


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
                    coverage_dimensions=["reviewer_infrastructure"],
                    problem="该 finding 使用了并不存在于当前冻结台账中的 requirement ID。",
                    missed_behavior_risk="若接受虚构 ID，审查意见无法关联真实义务并会污染证据链。",
                        recommended_action=(
                            "使用 register_coverage_plan 将 REQ-NOT-IN-LEDGER 替换为 "
                            "review_contract 中的真实 ID。"
                        ),
                    recommended_tools=["register_coverage_plan"],
                    recommended_steps=_steps(
                        ["register_coverage_plan"], "REQ-NOT-IN-LEDGER"
                    ),
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


def test_repeated_programmatic_id_mismatch_terminates_same_fingerprint(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)
    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=lambda kind, payload, _attempt: _verdict(
            kind, payload, omit_requirement=True
        ),
    )
    registry.semantic_review_gate = gate

    first = gate.review(reason="第一次 reviewer ID 集不完整时允许复审。")
    second = gate.review(reason="第二次相同 ID mismatch 必须终止当前 attempt。")

    assert first["execution_status"] == "completed"
    assert first["programmatic_errors"]
    assert second["execution_status"] == "reviewer_contract_failure"
    assert gate.has_terminal_failure() is True


def test_nonretryable_reviewer_contract_failure_is_not_mislabeled_transient(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def broken_runner(_kind, _payload, _attempt):
        raise CoverageReviewerContractError("structured_output_schema_invalid")

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=broken_runner,
    )
    reviewed = gate.review(reason="确定性 schema 错误不得伪装成 provider 临时失败。")

    assert reviewed["execution_status"] == "reviewer_contract_failure"
    assert reviewed["passed"] is False
    assert reviewed["required_actions"][0]["recommended_action"].startswith(
        "Stop the current Discover attempt"
    )
    assert registry.records[-1]["record_type"] == "discovery_coverage_review_contract_failed"
    record_count = len(registry.records)
    repeated = gate.review(reason="同一 attempt 不得重复执行确定性失败的 reviewer。")
    assert repeated == reviewed
    assert len(registry.records) == record_count


def test_reviewer_error_classifier_prioritizes_structured_contract_codes():
    with pytest.raises(CoverageReviewerContractError):
        _raise_classified_reviewer_error(
            "semantic_coverage",
            {
                "code": "schema_invalid",
                "message": "recommended_action connection field is invalid",
            },
        )

    with pytest.raises(RetryableCoverageReviewerError):
        _raise_classified_reviewer_error(
            "semantic_coverage",
            {
                "code": "provider_error",
                "type": "RemoteProtocolError",
                "message": "incomplete chunked read",
            },
        )

    with pytest.raises(RetryableCoverageReviewerError):
        _raise_classified_reviewer_error(
            "semantic_coverage",
            ConnectionError("temporary network failure"),
        )


def test_retry_record_keeps_any_completed_reviewer_verdict(tmp_path):
    controller, registry, _plan = _ready_controller(tmp_path)

    def runner(kind, payload, _attempt):
        if kind == "semantic_coverage":
            return _verdict(kind, payload)
        raise RetryableCoverageReviewerError("RemoteProtocolError: incomplete read")

    gate = CoverageReviewGate(
        registry=registry,
        task_snapshot=controller.task_snapshot(),
        runner=runner,
    )
    reviewed = gate.review(reason="保留同轮已完成 reviewer 证据。")

    assert reviewed["execution_status"] == "retryable_reviewer_failure"
    assert len(reviewed["completed_review_verdicts"]) == 1
    assert reviewed["completed_review_verdicts"][0]["review_kind"] == "semantic_coverage"


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
    action = before_plan["required_actions"][0]
    assert action["action_id"] == "REVIEW-PREREQ-001"
    assert action["error"] == "coverage_plan_not_registered"
    assert action["recommended_tools"] == ["register_coverage_plan"]
    assert "Do not call review_discovery_coverage again" in action["recommended_action"]
    assert action["coverage_improvement"]
    assert action["pass_criteria"] == "register_coverage_plan returns accepted=true."
    assert calls == []

    plan = make_plan(controller)
    assert registry.register_plan(plan, reason="注册但不执行断言。")["accepted"]
    before_eval = gate.review(reason="断言尚未终态时不得审查。")
    assert before_eval["execution_status"] == "prerequisite_required"
    assert before_eval["required_actions"][0]["recommended_tools"] == ["eval_assert"]
    assert before_eval["required_actions"][0]["pass_criteria"]
    assert calls == []
