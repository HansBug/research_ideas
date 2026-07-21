from __future__ import annotations

import pytest

from paper_stm_repair_loop.schemas.coverage_review import (
    CoverageImprovementStep,
    CoverageReviewFinding,
    CoverageReviewVerdict,
)
from paper_stm_repair_loop.tools.review_discovery_coverage import (
    CoverageReviewerContractError,
    CoverageReviewGate,
    RetryableCoverageReviewerError,
    _raise_classified_reviewer_error,
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
            "assertion_chain_id": "ASSERT-TO-RESOLVE",
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
