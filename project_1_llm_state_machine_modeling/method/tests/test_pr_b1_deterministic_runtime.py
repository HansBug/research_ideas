from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

import method.schema as schema
from method.run_record import is_path_result_eligible, read_agent_loop_run_record
from method.schema import (
    DesignDiagnosticItem,
    DesignFeedback,
    GroundingMap,
    ModelReviewFeedback,
    ParseFeedback,
    RepairRejection,
    RepairReviewFeedback,
    ReviewRunMeta,
    SL10RepairReviewOutput,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from method.staged_runtime import (
    FullStagedRuntimeAdapters,
    FullStagedRuntimeConfig,
    RepairRequest,
    ScenarioGenerationRequest,
    build_full_staged_runtime_adapters,
    _compact_sl9_input_for_prompt,
    run_full_staged_deterministic_runtime,
)
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.ids import STAGE_SPECS_BY_ID, StageId, StageStatus


def _meta(
    stage_id: StageId,
    *,
    ok: bool = True,
    status: StageStatus | None = None,
    stage_error: str | None = None,
) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
        stage_error=stage_error,
    )


def _retry_exhausted_run(stage_id: StageId, error_kind: str = "provider_error") -> Any:
    message = f"{stage_id.value} {error_kind} exhausted"
    return SimpleNamespace(
        stage_id=stage_id.value,
        ok=False,
        parsed_output={},
        feedback=None,
        stage_meta=_meta(stage_id, ok=False, status=StageStatus.ERROR, stage_error=message),
        interaction={
            "stage_id": stage_id.value,
            "provider": "test-adapter",
            "model_id": "none",
            "schema_validation_ok": False,
            "retry_error": {"error_kind": error_kind, "error_message": message},
            "attempts": [{"status": error_kind, "error_kind": error_kind, "error_message": message}],
        },
    )


def _ok_parse(_dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
    return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)


def _ok_semantic(_dsl: str, _context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
    return SemanticFeedback(ok=True), _meta(StageId.SD_3_SEMANTIC)


def _ok_design(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
    return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)


def _ok_coverage(_dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
    return {
        "coverage_report": {"n_scenarios": len(scenarios), "ok": True},
        "retry_directive": None,
        "coverage_gap": False,
    }, _meta(StageId.SD_5A_SCENARIO_COVERAGE)


def _gap_coverage(_dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
    return {
        "coverage_report": {"n_scenarios": len(scenarios), "ok": False},
        "retry_directive": {"missing": ["transition_event_mutation"]},
        "coverage_gap": True,
    }, _meta(StageId.SD_5A_SCENARIO_COVERAGE, ok=False, status=StageStatus.ADVISORY)


def _ok_sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
    n = len(getattr(scenarios_or_set, "scenarios", []) or [])
    return SimFeedback(ok=True, n_scenarios=n, n_scenarios_passed=n), _meta(StageId.SD_6_SIM)


def _review_meta(stage: StageId = StageId.SL_7_MODEL_REVIEW) -> ReviewRunMeta:
    return ReviewRunMeta(
        provider="test-adapter",
        model_id="none",
        prompt_template_version=f"{stage.value}.test",
        schema_validation_ok=True,
        parsed_schema_version="test.v1",
        failure_policy="audit_only",
        replay_key=f"{stage.value}:test",
    )


def _ok_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    meta = _meta(StageId.SL_7_MODEL_REVIEW)
    return ModelReviewFeedback(ok=True, decision="pass", risk_level="none", review_meta=_review_meta(), meta=meta), meta


def _audit_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    meta = _meta(StageId.SL_7_MODEL_REVIEW, ok=True, status=StageStatus.ADVISORY)
    return ModelReviewFeedback(
        ok=True,
        decision="audit_only",
        risk_level="minor",
        findings=[{"id": "style-note", "message": "audit-only finding"}],
        blocking_findings=[],
        review_meta=_review_meta(),
        meta=meta,
    ), meta


def _blocking_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    meta = _meta(StageId.SL_7_MODEL_REVIEW, ok=False, status=StageStatus.FAIL)
    return ModelReviewFeedback(
        ok=False,
        decision="fail",
        risk_level="major",
        findings=[{"id": "MR-1", "message": "major fidelity issue"}],
        blocking_findings=[{"id": "MR-1", "message": "major fidelity issue"}],
        review_meta=_review_meta(),
        meta=meta,
    ), meta


def _accept_repair_review(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
    assert request.nl
    assert isinstance(request.grounding_map, GroundingMap) or request.grounding_map is None
    assert request.old_dsl
    assert request.candidate_dsl
    assert request.fix_plan is not None
    feedback = RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="none")
    meta = _meta(StageId.SD_10_REPAIR_REVIEW)
    feedback.meta = meta
    return feedback, meta


def _base_adapters(**overrides: Any) -> FullStagedRuntimeAdapters:
    scenario_calls: list[ScenarioGenerationRequest] = overrides.pop("scenario_calls", [])

    def scenario_generate(request: ScenarioGenerationRequest) -> list[TestScenario]:
        scenario_calls.append(request)
        return [TestScenario(name=f"smoke_{request.attempt_index}", steps=[])]

    def repair(request: RepairRequest) -> str:
        return "fixed"

    adapters = FullStagedRuntimeAdapters(
        parse=_ok_parse,
        semantic=_ok_semantic,
        design=_ok_design,
        scenario_generate=scenario_generate,
        scenario_coverage=_ok_coverage,
        sim=_ok_sim,
        model_review=_ok_model_review,
        repair=repair,
        repair_review=_accept_repair_review,
    )
    for name, value in overrides.items():
        setattr(adapters, name, value)
    adapters._scenario_calls = scenario_calls  # type: ignore[attr-defined]
    return adapters


def _stage_ids(record: Any) -> list[str]:
    return [row["stage_id"] for row in record.stage_records]


def test_pre_scenario_parse_failure_repairs_before_scenario_generation(tmp_path: Path) -> None:
    calls: list[str] = []

    def parse(dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
        calls.append(f"parse:{dsl}")
        if dsl == "bad":
            return ParseFeedback(ok=False, error_message="syntax broken", diagnostics=[{"code": "parse"}]), _meta(StageId.SD_2_PARSE, ok=False)
        return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)

    def repair(request: RepairRequest) -> str:
        calls.append(f"repair:{request.selected_feedback_trace['source']}")
        assert request.scenario_set is None, "pre-scenario repair must not receive a frozen oracle"
        return "fixed"

    scenario_calls: list[ScenarioGenerationRequest] = []
    adapters = _base_adapters(parse=parse, repair=repair, scenario_calls=scenario_calls)
    result = run_full_staged_deterministic_runtime(
        "parse-fail before scenario",
        FullStagedRuntimeConfig(initial_dsl="bad", run_id="pr-b1-pre-scenario-parse", output_dir=tmp_path, max_iterations=2),
        adapters=adapters,
    )

    assert result.status == "converged"
    assert calls[:3] == ["parse:bad", "repair:parse", "parse:fixed"]
    assert len(scenario_calls) == 1
    assert scenario_calls[0].current_dsl == "fixed"

    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert StageId.SL_5_SCENARIO_GENERATION.value not in stage_ids[: stage_ids.index(StageId.SD_8_FIX_PLAN.value)]
    assert record.iteration_records[0]["selected_feedback"]["source"] == "parse"
    assert record.iteration_records[0]["selected_feedback"]["pre_scenario"] is True
    assert record.iteration_records[0]["selected_feedback"]["is_pre_scenario"] is True
    assert all("-pre" not in stage_id for stage_id in stage_ids)


def test_repair_accept_returns_to_sd2_before_success(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-design-fix":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
                message="Idle is a deadlock leaf",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    adapters = _base_adapters(design=design, repair=lambda request: "fixed")
    result = run_full_staged_deterministic_runtime(
        "repair must be revalidated",
        FullStagedRuntimeConfig(initial_dsl="needs-design-fix", run_id="pr-b1-return-sd2", output_dir=tmp_path, max_iterations=2),
        adapters=adapters,
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    sc11_index = stage_ids.index(StageId.SC_11_ACCEPT_CANDIDATE.value)
    second_sd2_index = stage_ids.index(StageId.SD_2_PARSE.value, sc11_index + 1)
    sc12_index = stage_ids.index(StageId.SC_12_EXIT.value)
    assert sc11_index < second_sd2_index < sc12_index
    assert record.iteration_records[0]["exit_reason"] == "candidate_accepted_for_next_full_pass"
    assert record.repair_history[0]["accepted"] is True


def test_repair_request_carries_generic_variable_role_summary(tmp_path: Path) -> None:
    captured: dict[str, Any] = {}

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_UNWRITTEN_READ_VAR",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="W_UNWRITTEN_READ_VAR:var_name=plant_input",
            refs={"var_name": "plant_input", "guard_vars": ["plant_input"]},
            message="plant_input is read by guards but never written",
            rationale="Downgraded because `plant_input` is NL-grounded as an external sensor/environment input.",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> str:
        captured["trace"] = request.selected_feedback_trace
        return "fixed"

    result = run_full_staged_deterministic_runtime(
        "The controller reads plant_input from external input signals before selecting Active.",
        FullStagedRuntimeConfig(initial_dsl="needs-variable-role", run_id="pr-b1-var-role", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=repair),
    )

    assert result.status in {"not_converged", "converged"}
    summary = captured["trace"]["variable_role_summary"]
    assert summary["variables"]["plant_input"]["role_hint"] == "external_input_candidate"
    assert summary["variables"]["plant_input"]["nl_token_present"] is True
    rendered = str(summary)
    for sample_token in ["ABS", "CARA", "Elevator", "LNG", "PS2", "StartAC"]:
        assert sample_token not in rendered


def test_design_fix_request_batch_is_bounded_for_prompt_safety(tmp_path: Path) -> None:
    captured: dict[str, Any] = {}
    long_text = "very long diagnostic evidence " * 200

    def design(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        items = [
            DesignDiagnosticItem(
                code=f"W_MANY_{i % 5}",
                pyfcstm_severity="warning",
                message=f"{long_text} #{i}",
                instance_key=f"diag-{i}",
                policy_action="budgeted_repair",
                suggested_fix_hints=[{"hint": long_text, "index": i}],
            )
            for i in range(100)
        ]
        return DesignFeedback(ok=False, blocking_items=items), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> dict[str, object]:
        assert request.fix_request_batch is not None
        captured["batch"] = request.fix_request_batch
        compact = _compact_sl9_input_for_prompt(
            fix_plan=request.fix_plan,
            fix_request_batch=request.fix_request_batch,
            fix_log=request.fix_log,
            grounding_map=request.grounding_map,
            selected_diagnostics=[request.selected_feedback_trace],
            preserve_list=[],
            scenario_summary={"pre_scenario": True},
        )
        prompt = build_sl9_repair_prompt(
            nl=request.nl,
            current_dsl=request.old_dsl,
            fix_plan=compact["fix_plan_summary"],
            fix_request_batch=compact["fix_request_batch"],
            fix_log=compact["fix_log"],
            selected_diagnostics=compact["selected_diagnostics"],
            grounding_map=compact["grounding_map_summary"],
            preserve_list=compact["preserve_list"],
            scenario_summary=compact["scenario_summary"],
        )
        captured["prompt_len"] = sum(len(message["content"]) for message in prompt)
        decisions = [{"request_id": item.request_id, "decision": "reject", "rationale": "external warning", "waiver": True} for item in request.fix_request_batch.requests]
        return {"decisions": decisions, "candidate_dsl": "", "repair_rationale": ["waived compact warning batch"]}

    result = run_full_staged_deterministic_runtime(
        "prompt-safe bounded repair batch",
        FullStagedRuntimeConfig(initial_dsl="stable", run_id="pr-b1-prompt-safe-fixbatch", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=repair),
    )

    assert result.status in {"converged", "not_converged"}
    batch = captured["batch"]
    assert len(batch.requests) <= 12
    assert batch.selected_feedback_trace["fix_request_compaction"]["raw_request_candidates"] == 100
    assert batch.selected_feedback_trace["fix_request_compaction"]["emitted_requests"] == len(batch.requests)
    assert captured["prompt_len"] < 200_000


def test_coverage_retry_exhaustion_marks_weak_oracle_and_excludes_main_result(tmp_path: Path) -> None:
    scenario_calls: list[ScenarioGenerationRequest] = []
    adapters = _base_adapters(scenario_coverage=_gap_coverage, scenario_calls=scenario_calls)

    result = run_full_staged_deterministic_runtime(
        "coverage weak oracle",
        FullStagedRuntimeConfig(
            initial_dsl="stable",
            run_id="pr-b1-weak-oracle",
            output_dir=tmp_path,
            max_iterations=1,
            scenario_max_retries=1,
        ),
        adapters=adapters,
    )

    assert result.status == "converged"
    assert len(scenario_calls) == 2  # initial generation + one targeted retry
    assert [call.coverage_directive for call in scenario_calls] == [None, {"missing": ["transition_event_mutation"]}]

    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "success"
    assert record.final_artifacts["oracle_weak"] is True
    assert record.final_artifacts["main_result_eligible"] is False
    assert "weak_oracle" in record.final_artifacts["exclusion_reason"]
    assert not is_path_result_eligible(record)
    assert record.scenario_history[-1]["oracle_weak"] is True


def test_frozen_scenario_gap_uses_targeted_retry_before_weak_oracle(tmp_path: Path) -> None:
    scenario_calls: list[ScenarioGenerationRequest] = []
    coverage_calls: list[tuple[str, list[str]]] = []
    fixed_coverage_attempts = {"n": 0}

    def scenario_generate(request: ScenarioGenerationRequest) -> list[TestScenario]:
        scenario_calls.append(request)
        suffix = "retry" if request.coverage_directive else "initial"
        return [TestScenario(name=f"{request.current_dsl}_{suffix}_{len(scenario_calls)}", steps=[])]

    def scenario_coverage(dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
        coverage_calls.append((dsl, [scenario.name for scenario in scenarios]))
        if dsl == "fixed":
            fixed_coverage_attempts["n"] += 1
            if fixed_coverage_attempts["n"] == 1:
                return {
                    "coverage_report": {"ok": False},
                    "coverage_gap": True,
                    "retry_directive": {"missing": ["fixed_transition"]},
                }, _meta(StageId.SD_5A_SCENARIO_COVERAGE, ok=False, status=StageStatus.ADVISORY)
        return {
            "coverage_report": {"ok": True},
            "coverage_gap": False,
            "retry_directive": None,
        }, _meta(StageId.SD_5A_SCENARIO_COVERAGE)

    def sim(dsl: str, scenario_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        if dsl == "needs-sim-repair":
            return SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, setup_error="needs repair"), _meta(StageId.SD_6_SIM, ok=False)
        return SimFeedback(ok=True, n_scenarios=1, n_scenarios_passed=1), _meta(StageId.SD_6_SIM)

    result = run_full_staged_deterministic_runtime(
        "frozen oracle gap should retry before weak oracle",
        FullStagedRuntimeConfig(
            initial_dsl="needs-sim-repair",
            run_id="pr-b1-frozen-gap-retry",
            output_dir=tmp_path,
            max_iterations=2,
            scenario_max_retries=1,
        ),
        adapters=_base_adapters(
            scenario_generate=scenario_generate,
            scenario_coverage=scenario_coverage,
            sim=sim,
            repair=lambda _request: "fixed",
        ),
    )

    assert result.status == "converged"
    assert len(scenario_calls) == 2
    assert scenario_calls[1].current_dsl == "fixed"
    assert scenario_calls[1].attempt_index == 1
    assert scenario_calls[1].coverage_directive == {"missing": ["fixed_transition"]}
    assert coverage_calls == [
        ("needs-sim-repair", ["needs-sim-repair_initial_1"]),
        ("fixed", ["needs-sim-repair_initial_1"]),
        ("fixed", ["fixed_retry_2"]),
    ]

    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.final_artifacts["oracle_weak"] is False
    assert record.final_artifacts["verdict"] == "success"
    assert record.scenario_history[-1]["targeted_retry_after_frozen_gap"] is True
    assert record.scenario_history[-1]["oracle_weak"] is False


def test_historical_weak_oracle_is_cleared_after_successful_targeted_refresh(tmp_path: Path) -> None:
    scenario_calls: list[ScenarioGenerationRequest] = []
    coverage_calls: list[tuple[str, list[str]]] = []
    fixed_attempts = {"n": 0}

    def scenario_generate(request: ScenarioGenerationRequest) -> list[TestScenario]:
        scenario_calls.append(request)
        return [TestScenario(name=f"{request.current_dsl}_scenario_{request.attempt_index}", steps=[])]

    def scenario_coverage(dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
        coverage_calls.append((dsl, [scenario.name for scenario in scenarios]))
        if dsl == "needs-sim-repair":
            return {
                "coverage_report": {"ok": False},
                "coverage_gap": True,
                "retry_directive": {"missing": ["initial_model_mutation"]},
            }, _meta(StageId.SD_5A_SCENARIO_COVERAGE, ok=False, status=StageStatus.ADVISORY)
        if dsl == "fixed":
            fixed_attempts["n"] += 1
            if fixed_attempts["n"] == 1:
                return {
                    "coverage_report": {"ok": True},
                    "coverage_gap": False,
                    "retry_directive": None,
                }, _meta(StageId.SD_5A_SCENARIO_COVERAGE)
        return {
            "coverage_report": {"ok": True},
            "coverage_gap": False,
            "retry_directive": None,
        }, _meta(StageId.SD_5A_SCENARIO_COVERAGE)

    def sim(dsl: str, scenario_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        if dsl == "needs-sim-repair":
            return SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, setup_error="needs repair"), _meta(StageId.SD_6_SIM, ok=False)
        return SimFeedback(ok=True, n_scenarios=1, n_scenarios_passed=1), _meta(StageId.SD_6_SIM)

    result = run_full_staged_deterministic_runtime(
        "historical weak oracle should not poison refreshed current oracle",
        FullStagedRuntimeConfig(
            initial_dsl="needs-sim-repair",
            run_id="pr-b1-weak-cleared-after-refresh",
            output_dir=tmp_path,
            max_iterations=2,
            scenario_max_retries=1,
            allow_main_result_eligible=True,
            adapter_mode="real_env",
        ),
        adapters=_base_adapters(
            scenario_generate=scenario_generate,
            scenario_coverage=scenario_coverage,
            sim=sim,
            repair=lambda _request: "fixed",
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    assert result.status == "converged"
    assert record.scenario_history[1]["oracle_weak"] is True
    assert record.scenario_history[-1]["targeted_retry_after_dsl_change"] is True
    assert record.scenario_history[-1]["oracle_weak"] is False
    assert record.final_artifacts["oracle_weak"] is False
    assert record.final_artifacts["main_result_eligible"] is True
    assert is_path_result_eligible(record)


def test_model_review_blocking_enters_sd8_but_audit_only_does_not(tmp_path: Path) -> None:
    review_calls = {"blocking": 0}

    def model_review(dsl: str, context: StageContext, feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
        if dsl == "stable-but-review-fails":
            review_calls["blocking"] += 1
            return _blocking_model_review(dsl, context, feedback)
        return _ok_model_review(dsl, context, feedback)

    blocking = run_full_staged_deterministic_runtime(
        "model review blocking",
        FullStagedRuntimeConfig(initial_dsl="stable-but-review-fails", run_id="pr-b1-review-block", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(model_review=model_review, repair=lambda request: "fixed"),
    )
    blocking_record = read_agent_loop_run_record(blocking.run_record_path or "")
    assert blocking.status == "converged"
    assert blocking_record.iteration_records[0]["selected_feedback"]["source"] == "model_review"
    assert StageId.SD_8_FIX_PLAN.value in blocking_record.iteration_records[0]["repair_stage_ids"]

    audit = run_full_staged_deterministic_runtime(
        "audit-only model review",
        FullStagedRuntimeConfig(initial_dsl="stable-audit", run_id="pr-b1-review-audit", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(model_review=_audit_model_review, repair=lambda request: "should-not-run"),
    )
    audit_record = read_agent_loop_run_record(audit.run_record_path or "")
    assert audit.status == "converged"
    assert audit_record.iteration_records[0]["selected_feedback"] is None
    assert StageId.SD_8_FIX_PLAN.value not in _stage_ids(audit_record)


def test_unknown_warning_requires_policy_classification_and_blocks(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "unknown-warning":
            item = DesignDiagnosticItem(
                code="W_UNKNOWN_NEW_CHECK",
                pyfcstm_severity="warning",
                policy_action="requires_policy_classification",
                instance_key="W_UNKNOWN_NEW_CHECK:state=Root.Idle",
                message="new warning code has no mapped policy",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    result = run_full_staged_deterministic_runtime(
        "unknown warning policy",
        FullStagedRuntimeConfig(initial_dsl="unknown-warning", run_id="pr-b1-unknown-warning", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=lambda request: "fixed"),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    selected = record.iteration_records[0]["selected_feedback"]
    assert selected["source"] == "design"
    assert selected["policy_actions"] == ["requires_policy_classification"]
    assert "advisory" not in selected["policy_actions"]
    assert record.deterministic_feedback["iterations"][0]["design"]["blocking_items"][0]["policy_action"] == "requires_policy_classification"


def test_sl9_can_reject_waiver_allowed_design_warning_and_continue_next_stage(tmp_path: Path) -> None:
    calls = {"design": 0, "repair": 0}

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        calls["design"] += 1
        if calls["design"] == 1:
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> dict[str, object]:
        calls["repair"] += 1
        assert request.fix_request_batch is not None
        assert request.fix_request_batch.requests[0].waiver_allowed is True
        return {
            "decisions": [
                {
                    "request_id": request.fix_request_batch.requests[0].request_id,
                    "decision": "reject",
                    "waiver": True,
                    "rationale": "warning already reviewed as acceptable external/input-style issue",
                }
            ],
            "candidate_dsl": "",
            "repair_rationale": ["no edit needed"],
            "diff_summary": {"summary": "no-op waiver"},
        }

    result = run_full_staged_deterministic_runtime(
        "warning can be waived and flow should continue",
        FullStagedRuntimeConfig(initial_dsl="warning-only", run_id="pr-b1-sl9-waiver-continue", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=repair),
    )

    assert result.status == "converged"
    assert result.final_dsl == "warning-only"
    assert calls["repair"] == 1
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.repair_history[0]["waiver_continue"] is True
    assert record.repair_history[0]["accepted"] is False
    assert record.iteration_records[0]["waiver_continue"] is True
    assert record.iteration_records[0]["exit_reason"] == "full_pass_all_required_feedback_ok_after_waiver_continue"
    assert record.iteration_records[0]["post_waiver_selected_feedback"] is None
    assert record.fix_log[-1]["next_action"] == "continue_after_waiver"


def test_last_iteration_waiver_continue_does_not_consume_sc11_budget(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_UNWRITTEN_READ_VAR",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="W_UNWRITTEN_READ_VAR:var_name=EnvCapacity",
            refs={"var_name": "EnvCapacity"},
            message="EnvCapacity is read but never written",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> dict[str, object]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {
                    "request_id": request.fix_request_batch.requests[0].request_id,
                    "decision": "reject",
                    "waiver": True,
                    "rationale": "EnvCapacity is an NL-grounded external input; no DSL edit is safe.",
                }
            ],
            "candidate_dsl": "",
            "repair_rationale": ["no edit; continue validation after waiver"],
            "diff_summary": {"summary": "no-op waiver"},
        }

    result = run_full_staged_deterministic_runtime(
        "controller reads EnvCapacity as an external input and then validates downstream behavior",
        FullStagedRuntimeConfig(initial_dsl="warning-only", run_id="pr-b1-last-waiver", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=repair),
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "success"
    assert len(record.iteration_records) == 1
    only_iter = record.iteration_records[0]
    assert only_iter["waiver_continue"] is True
    assert only_iter["accepted_candidate"] is False
    assert only_iter["post_waiver_selected_feedback"] is None
    assert only_iter["exit_reason"] == "full_pass_all_required_feedback_ok_after_waiver_continue"
    assert "budget_gate" not in only_iter
    stage_ids = _stage_ids(record)
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in stage_ids
    assert StageId.SL_5_SCENARIO_GENERATION.value in stage_ids
    assert StageId.SD_6_SIM.value in stage_ids
    assert StageId.SL_7_MODEL_REVIEW.value in stage_ids
    assert record.fix_log[-1]["next_action"] == "continue_after_waiver"


def test_waiver_continue_reveals_downstream_block_without_sc11_candidate(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_UNWRITTEN_READ_VAR",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key="W_UNWRITTEN_READ_VAR:var_name=EnvCapacity",
            refs={"var_name": "EnvCapacity"},
            message="EnvCapacity is read but never written",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def repair(request: RepairRequest) -> dict[str, object]:
        assert request.fix_request_batch is not None
        return {
            "decisions": [
                {
                    "request_id": request.fix_request_batch.requests[0].request_id,
                    "decision": "reject",
                    "waiver": True,
                    "rationale": "external input warning waived",
                }
            ],
            "candidate_dsl": "",
            "repair_rationale": ["no edit"],
        }

    def sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        n = len(getattr(scenarios_or_set, "scenarios", []) or [])
        return SimFeedback(ok=False, n_scenarios=n, n_scenarios_passed=0, setup_error="downstream scenario failed"), _meta(StageId.SD_6_SIM, ok=False)

    result = run_full_staged_deterministic_runtime(
        "warning waiver should continue and expose downstream simulation failure",
        FullStagedRuntimeConfig(initial_dsl="warning-then-sim-fails", run_id="pr-b1-waiver-downstream", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=repair, sim=sim),
    )

    assert result.status == "not_converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "budget_exhausted"
    only_iter = record.iteration_records[0]
    assert only_iter["waiver_continue"] is True
    assert only_iter["post_waiver_selected_feedback"]["source"] == "sim"
    assert only_iter["exit_reason"] == "waiver_continue_revealed_downstream_blocking_feedback"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SD_6_SIM.value
    assert "SD-6 sim failure" in record.final_artifacts["verdict_reason"]
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in _stage_ids(record)

def test_repair_review_rejection_records_regression_without_accepting_candidate(tmp_path: Path) -> None:
    def sim(_dsl: str, scenario_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, setup_error="scenario failed"), _meta(StageId.SD_6_SIM, ok=False)

    def reject(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        assert request.scenario_set is not None
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="scenario_regression",
            regression_detected=True,
            drift_risk="minor",
            evidence=[{"kind": "scenario_regression"}],
        )
        feedback = RepairReviewFeedback(
            ok=False,
            target_resolved=False,
            regression_detected=True,
            drift_risk="minor",
            local_rejection=rejection,
        )
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        feedback.meta = meta
        return feedback, meta

    result = run_full_staged_deterministic_runtime(
        "repair regression rejection",
        FullStagedRuntimeConfig(initial_dsl="stable", run_id="pr-b1-repair-reject", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(sim=sim, repair=lambda request: "regressed", repair_review=reject),
    )

    assert result.status == "not_converged"
    assert result.final_dsl == "stable"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "rejected"
    assert record.repair_history[0]["accepted"] is False
    assert record.repair_history[0]["repair_review"]["local_rejection"]["reason"] == "scenario_regression"
    assert not any(
        row["stage_id"] == StageId.SC_11_ACCEPT_CANDIDATE.value and row["status"] == StageStatus.OK.value
        for row in record.stage_records
    )
    assert record.final_artifacts["main_result_eligible"] is False



def test_repair_review_rejection_retries_with_revised_fix_plan_until_budget(tmp_path: Path) -> None:
    repair_candidates = ["drift", "fixed"]
    repair_calls: list[str] = []

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-fix":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def repair(request: RepairRequest) -> str:
        repair_calls.append(type(request.fix_plan).__name__)
        return repair_candidates[len(repair_calls) - 1]

    def review(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        if request.candidate_dsl == "drift":
            rejection = RepairRejection(
                rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
                reason="missing_required_grounding",
                drift_risk="major",
                evidence=[{"kind": "missing_grounding"}],
            )
            feedback = RepairReviewFeedback(
                ok=False,
                target_resolved=False,
                drift_risk="major",
                local_rejection=rejection,
            )
            meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        else:
            feedback = RepairReviewFeedback(ok=True, target_resolved=True, regression_detected=False, drift_risk="none")
            meta = _meta(StageId.SD_10_REPAIR_REVIEW)
        feedback.meta = meta
        return feedback, meta

    result = run_full_staged_deterministic_runtime(
        "repair rejection should consume another full iteration with revised plan",
        FullStagedRuntimeConfig(initial_dsl="needs-fix", run_id="pr-b1-reject-retry-revised", output_dir=tmp_path, max_iterations=3),
        adapters=_base_adapters(design=design, repair=repair, repair_review=review),
    )

    assert result.status == "converged"
    assert result.final_dsl == "fixed"
    assert repair_calls == ["FixPlan", "FixPlan"]
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "success"
    assert [entry["accepted"] for entry in record.repair_history] == [False, True]
    assert record.repair_history[0]["rework_attempt"] == 0
    assert record.repair_history[1]["rework_attempt"] == 1
    assert record.repair_history[1]["repair_review_input_summary"]["rework_locked"] is True
    assert record.iteration_records[0]["exit_reason"] == "candidate_accepted_for_next_full_pass"
    assert record.iteration_records[0]["rework_attempts_used"] == 2
    assert record.iteration_records[1]["exit_reason"] == "full_pass_all_required_feedback_ok"
    assert record.replay_index["fix_log_count"] >= 5


def test_repair_review_rejection_uses_full_budget_before_final_rejected(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        item = DesignDiagnosticItem(
            code="W_DEADLOCK_LEAF",
            pyfcstm_severity="warning",
            policy_action="budgeted_repair",
            instance_key=f"W_DEADLOCK_LEAF:state={context.current_dsl or 'Root'}",
        )
        return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)

    def reject(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason=f"still_bad_attempt_{request.repair_attempt}",
            drift_risk="major",
        )
        feedback = RepairReviewFeedback(ok=False, target_resolved=False, drift_risk="major", local_rejection=rejection)
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        feedback.meta = meta
        return feedback, meta

    result = run_full_staged_deterministic_runtime(
        "repair rejection should not stop after one try when max_iterations allows retries",
        FullStagedRuntimeConfig(initial_dsl="needs-fix", run_id="pr-b1-reject-uses-budget", output_dir=tmp_path, max_iterations=3),
        adapters=_base_adapters(design=design, repair=lambda request: f"bad-{request.repair_attempt}", repair_review=reject),
    )

    assert result.status == "not_converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "rejected"
    assert len(record.iteration_records) == 1
    assert len(record.repair_history) == 3
    assert [entry["rework_attempt"] for entry in record.repair_history] == [0, 1, 2]
    assert record.iteration_records[0]["exit_reason"] == "SD-4 design diagnostics: W_DEADLOCK_LEAF"
    assert record.iteration_records[0]["retryable_repair_rejection"] is False
    assert record.iteration_records[0]["rework_attempts_used"] == 3
    assert record.repair_history[-1]["repair_review"]["local_rejection"]["reason"] == "still_bad_attempt_2"
    assert record.replay_index["fix_log_count"] >= 7
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_10_REPAIR_REVIEW.value

def test_weak_oracle_sim_failure_stops_without_repair_and_excludes_main_result(tmp_path: Path) -> None:
    repair_calls = {"n": 0}

    def weak_sim(_dsl: str, scenario_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        return (
            SimFeedback(
                ok=False,
                n_scenarios=1,
                n_scenarios_passed=0,
                oracle_weak=True,
                weak_oracle_reason="normalized_hot_start_scenario_failed",
                weak_oracle_evidence={"scenario_names": ["hot_start_probe"]},
            ),
            _meta(StageId.SD_6_SIM, ok=False),
        )

    def repair(_request: RepairRequest) -> str:
        repair_calls["n"] += 1
        return "should-not-run"

    result = run_full_staged_deterministic_runtime(
        "weak sim oracle should not drive repair",
        FullStagedRuntimeConfig(initial_dsl="stable", run_id="pr-b1-weak-sim-no-repair", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(sim=weak_sim, repair=repair),
    )

    assert result.status == "not_converged"
    assert repair_calls["n"] == 0
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.status == "failed"
    assert record.final_artifacts["verdict"] == "not_converged"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SD_6_SIM.value
    assert record.final_artifacts["oracle_weak"] is True
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.iteration_records[0]["selected_feedback"] is None
    assert StageId.SD_8_FIX_PLAN.value not in _stage_ids(record)


def test_pre_scenario_semantic_failure_repairs_before_scenario_generation(tmp_path: Path) -> None:
    scenario_calls: list[ScenarioGenerationRequest] = []
    semantic_calls: list[str] = []

    def semantic(dsl: str, _context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
        semantic_calls.append(dsl)
        if dsl == "sem-bad":
            return SemanticFeedback(ok=False, error_message="undefined var", diagnostics=[{"code": "undefined_var"}]), _meta(StageId.SD_3_SEMANTIC, ok=False)
        return SemanticFeedback(ok=True), _meta(StageId.SD_3_SEMANTIC)

    def repair(request: RepairRequest) -> str:
        assert request.selected_feedback_trace["source"] == "semantic"
        assert request.selected_feedback_trace["pre_scenario"] is True
        assert request.scenario_set is None
        return "sem-fixed"

    result = run_full_staged_deterministic_runtime(
        "semantic fail before scenario",
        FullStagedRuntimeConfig(initial_dsl="sem-bad", run_id="pr-b1-pre-scenario-sem", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(semantic=semantic, repair=repair, scenario_calls=scenario_calls),
    )

    assert result.status == "converged"
    assert semantic_calls[:2] == ["sem-bad", "sem-fixed"]
    assert len(scenario_calls) == 1
    assert scenario_calls[0].current_dsl == "sem-fixed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.iteration_records[0]["selected_feedback"]["source"] == "semantic"
    assert record.iteration_records[0]["selected_feedback"]["is_pre_scenario"] is True
    assert StageId.SL_5_SCENARIO_GENERATION.value not in record.iteration_records[0]["stage_ids"]
    assert all("-pre" not in stage_id for stage_id in _stage_ids(record))


def test_accept_candidate_with_parse_regression_is_revalidated_not_direct_success(tmp_path: Path) -> None:
    def parse(dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
        if dsl == "parse-regressed":
            return ParseFeedback(ok=False, error_message="candidate parse regression", diagnostics=[{"code": "parse_regression"}]), _meta(StageId.SD_2_PARSE, ok=False)
        return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-fix":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    result = run_full_staged_deterministic_runtime(
        "accepted repair may still regress parse",
        FullStagedRuntimeConfig(initial_dsl="needs-fix", run_id="pr-b1-accepted-parse-regression", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(parse=parse, design=design, repair=lambda request: "parse-regressed"),
    )

    assert result.status == "not_converged"
    assert result.final_dsl == "parse-regressed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    sc11_index = stage_ids.index(StageId.SC_11_ACCEPT_CANDIDATE.value)
    sd2_after_accept = stage_ids.index(StageId.SD_2_PARSE.value, sc11_index + 1)
    sc12_index = stage_ids.index(StageId.SC_12_EXIT.value)
    assert sc11_index < sd2_after_accept < sc12_index
    assert record.iteration_records[0]["accepted_candidate"] is True
    assert record.iteration_records[1]["selected_feedback"]["source"] == "parse"
    assert record.status == "budget_exhausted"
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.final_artifacts["verdict"] == "not_converged"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SC_11_ACCEPT_CANDIDATE.value


def test_sc11_budget_gate_emits_not_converged_without_direct_success(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-one-repair":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    result = run_full_staged_deterministic_runtime(
        "SC-11 budget gate",
        FullStagedRuntimeConfig(initial_dsl="needs-one-repair", run_id="pr-b1-sc11-budget", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=lambda request: "fixed-but-unvalidated"),
    )

    assert result.status == "not_converged"
    assert result.final_dsl == "fixed-but-unvalidated"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    sc11_index = stage_ids.index(StageId.SC_11_ACCEPT_CANDIDATE.value)
    sc12_index = stage_ids.index(StageId.SC_12_EXIT.value)
    assert sc11_index < sc12_index
    assert StageId.SD_2_PARSE.value not in stage_ids[sc11_index + 1 : sc12_index]
    assert record.status == "budget_exhausted"
    assert record.final_artifacts["verdict"] == "not_converged"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SC_11_ACCEPT_CANDIDATE.value
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.iteration_records[0]["budget_gate"] == {
        "source_stage_id": StageId.SC_11_ACCEPT_CANDIDATE.value,
        "iter_plus_one": 1,
        "max_iterations": 1,
        "next_stage_allowed": False,
    }


def test_llm_retry_exhausted_in_sl7_exits_provider_error_without_repair(tmp_path: Path) -> None:
    result = run_full_staged_deterministic_runtime(
        "SL-7 provider exhausted",
        FullStagedRuntimeConfig(initial_dsl="stable", run_id="pr-b1-sl7-provider-error", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(model_review=lambda _dsl, _context, _feedback: _retry_exhausted_run(StageId.SL_7_MODEL_REVIEW, "provider_error")),
    )

    assert result.status == "api_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_7_MODEL_REVIEW.value
    assert StageId.SD_8_FIX_PLAN.value not in stage_ids
    assert StageId.SL_9_REPAIR.value not in stage_ids
    assert record.repair_history == []
    assert record.llm_interactions[-1]["retry_error"]["error_kind"] == "provider_error"


def test_llm_retry_exhausted_in_sl5_exits_invalid_before_coverage_or_repair(tmp_path: Path) -> None:
    result = run_full_staged_deterministic_runtime(
        "SL-5 invalid exhausted",
        FullStagedRuntimeConfig(initial_dsl="stable", run_id="pr-b1-sl5-invalid", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(scenario_generate=lambda _request: _retry_exhausted_run(StageId.SL_5_SCENARIO_GENERATION, "empty_output")),
    )

    assert result.status == "spec_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value
    assert StageId.SD_5A_SCENARIO_COVERAGE.value not in stage_ids
    assert StageId.SD_8_FIX_PLAN.value not in stage_ids
    assert record.repair_history == []
    assert record.llm_interactions[-1]["retry_error"]["error_kind"] == "empty_output"


def test_llm_retry_exhausted_in_sl9_exits_invalid_without_sd10_or_sc11(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-repair":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    result = run_full_staged_deterministic_runtime(
        "SL-9 schema exhausted",
        FullStagedRuntimeConfig(initial_dsl="needs-repair", run_id="pr-b1-sl9-invalid", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=lambda _request: _retry_exhausted_run(StageId.SL_9_REPAIR, "schema_invalid")),
    )

    assert result.status == "spec_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_9_REPAIR.value
    assert StageId.SD_8_FIX_PLAN.value in stage_ids
    assert StageId.SD_10_REPAIR_REVIEW.value not in stage_ids
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in stage_ids
    assert record.repair_history == []


def test_llm_retry_exhausted_in_sl10_exits_provider_error_before_sc11(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-delta-review":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    result = run_full_staged_deterministic_runtime(
        "SL-10 provider exhausted",
        FullStagedRuntimeConfig(initial_dsl="needs-delta-review", run_id="pr-b1-sl10-provider", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(
            design=design,
            repair=lambda _request: "candidate",
            sl10_review=lambda _request, _local_review: _retry_exhausted_run(StageId.SL_10_REPAIR_REVIEW, "provider_error"),
        ),
    )

    assert result.status == "api_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_10_REPAIR_REVIEW.value
    assert StageId.SL_10_REPAIR_REVIEW.value in stage_ids
    assert StageId.SD_10_REPAIR_REVIEW.value not in stage_ids
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in stage_ids
    assert record.repair_history == []


def test_sl10_typed_pass_feedback_controls_candidate_acceptance(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-audit-delta":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def sl10_pass(_request: RepairRequest, _local_review: RepairReviewFeedback) -> Any:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW, ok=True)
        return SimpleNamespace(
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            ok=True,
            parsed_output={"decision": "pass", "drift_risk": "minor"},
            feedback=SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"kind": "typed-sl10-pass"}],
                review_meta=_review_meta(StageId.SL_10_REPAIR_REVIEW),
                meta=meta,
            ),
            stage_meta=meta,
            interaction={
                "stage_id": StageId.SL_10_REPAIR_REVIEW.value,
                "schema_validation_ok": True,
                "retry_error": None,
            },
        )

    result = run_full_staged_deterministic_runtime(
        "SL-10 typed pass should control SC-11",
        FullStagedRuntimeConfig(initial_dsl="needs-audit-delta", run_id="pr-b1-sl10-pass", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=lambda _request: "fixed", sl10_review=sl10_pass),
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.repair_history[0]["accepted"] is True
    assert record.repair_history[0]["sl10_repair_review"]["decision"] == "pass"
    assert record.repair_history[0]["repair_review"]["delta_review"]["decision"] == "pass"
    assert record.repair_history[0]["repair_review"].get("local_rejection") is None
    assert StageId.SC_11_ACCEPT_CANDIDATE.value in stage_ids
    assert record.final_artifacts["verdict"] == "success"


def test_optional_sl1_retry_exhaustion_exits_provider_error_before_validation(tmp_path: Path) -> None:
    result = run_full_staged_deterministic_runtime(
        "SL-1 provider exhausted",
        FullStagedRuntimeConfig(initial_dsl="seed", run_id="pr-b1-sl1-provider", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(initial_modeling=lambda _nl, _context: _retry_exhausted_run(StageId.SL_1_INITIAL_MODELING, "provider_error")),
    )

    assert result.status == "api_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_1_INITIAL_MODELING.value
    assert StageId.SD_2_PARSE.value not in stage_ids
    assert record.iteration_records == []


def test_pre_scenario_max_repairs_removed_from_loop_config_and_runtime_config() -> None:
    cfg = schema.LoopConfig()
    resolved = cfg.resolved_config()
    runtime_cfg = FullStagedRuntimeConfig(initial_dsl="stable")

    assert not hasattr(cfg, "pre_scenario_max_repairs")
    assert "pre_scenario_max_repairs" not in schema._default_budget_policy()
    assert "pre_scenario_max_repairs" not in cfg.budget_policy
    assert "pre_scenario_max_repairs" not in resolved
    assert "pre_scenario_max_repairs" not in resolved["budget_policy"]
    assert not hasattr(runtime_cfg, "pre_scenario_max_repairs")


def test_default_adapter_helper_design_policy_matches_run_record(tmp_path: Path) -> None:
    stable_dsl = """
state Root {
    state Idle;
    [*] -> Idle;
    Idle -> [*];
}
"""

    adapters = build_full_staged_runtime_adapters(
        scenario_generate=lambda _request: [TestScenario(name="smoke", steps=[])],
        repair=lambda _request: stable_dsl,
        model_review=_ok_model_review,
    )
    result = run_full_staged_deterministic_runtime(
        "policy profile should be auditable",
        FullStagedRuntimeConfig(
            initial_dsl=stable_dsl,
            run_id="pr-b1-policy-profile",
            output_dir=tmp_path,
            max_iterations=1,
        ),
        adapters=adapters,
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    design = record.deterministic_feedback["iterations"][0]["design"]
    assert record.run_config["policy_profile"] == "experiment_default"
    assert design["policy_profile"] == record.run_config["policy_profile"]
    assert design["inspect_summary"]["policy_profile"] == record.run_config["policy_profile"]


def test_sl10_pass_without_major_local_evidence_ack_is_downgraded(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-major-local-review":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def local_major(request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="missing_required_grounding",
            target_resolved=False,
            regression_detected=False,
            drift_risk="major",
            evidence=[{"kind": "missing_required_grounding", "element_ids": ["state:Required"]}],
        )
        feedback = RepairReviewFeedback(
            ok=False,
            target_resolved=False,
            regression_detected=False,
            drift_risk="major",
            local_rejection=rejection,
        )
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        feedback.meta = meta
        return feedback, meta

    def silent_sl10_pass(_request: RepairRequest, _local_review: RepairReviewFeedback) -> Any:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW, ok=True)
        return SimpleNamespace(
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            ok=True,
            parsed_output={"decision": "pass", "target_resolved": True, "regression_detected": False, "drift_risk": "minor"},
            feedback=SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"summary": "looks acceptable without naming the local rejection"}],
                review_meta=_review_meta(StageId.SL_10_REPAIR_REVIEW),
                meta=meta,
            ),
            stage_meta=meta,
            interaction={"stage_id": StageId.SL_10_REPAIR_REVIEW.value, "schema_validation_ok": True},
        )

    result = run_full_staged_deterministic_runtime(
        "SL-10 pass must acknowledge major local drift",
        FullStagedRuntimeConfig(initial_dsl="needs-major-local-review", run_id="pr-b1-sl10-major-local-gate", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=lambda _request: "candidate", repair_review=local_major, sl10_review=silent_sl10_pass),
    )

    assert result.status == "not_converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.repair_history[0]["accepted"] is False
    sl10 = record.repair_history[0]["sl10_repair_review"]
    assert sl10["ok"] is False
    assert sl10["decision"] == "rework"
    assert any("local_override_rationale" in text for text in sl10["rework_instructions"])
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in _stage_ids(record)



def test_reused_scenarios_are_refreshed_after_candidate_dsl_changes(tmp_path: Path) -> None:
    scenario_calls: list[ScenarioGenerationRequest] = []
    coverage_calls: list[tuple[str, list[str]]] = []

    def scenario_generate(request: ScenarioGenerationRequest) -> list[TestScenario]:
        scenario_calls.append(request)
        return [TestScenario(name=f"{request.current_dsl}_scenario_{request.attempt_index}", steps=[])]

    def scenario_coverage(dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
        coverage_calls.append((dsl, [scenario.name for scenario in scenarios]))
        return {"coverage_report": {"ok": True}, "coverage_gap": False, "retry_directive": None}, _meta(StageId.SD_5A_SCENARIO_COVERAGE)

    def sim(dsl: str, _scenario_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
        if dsl == "needs-refresh-repair":
            return SimFeedback(ok=False, n_scenarios=1, n_scenarios_passed=0, setup_error="needs repair"), _meta(StageId.SD_6_SIM, ok=False)
        return SimFeedback(ok=True, n_scenarios=1, n_scenarios_passed=1), _meta(StageId.SD_6_SIM)

    result = run_full_staged_deterministic_runtime(
        "accepted candidate should refresh stale scenario oracle",
        FullStagedRuntimeConfig(initial_dsl="needs-refresh-repair", run_id="pr-b1-refresh-stale-scenarios", output_dir=tmp_path, max_iterations=2, scenario_max_retries=1),
        adapters=_base_adapters(scenario_generate=scenario_generate, scenario_coverage=scenario_coverage, sim=sim, repair=lambda _request: "fixed"),
    )

    assert result.status == "converged"
    assert [call.current_dsl for call in scenario_calls] == ["needs-refresh-repair", "fixed"]
    assert scenario_calls[1].previous_scenarios[0].name == "needs-refresh-repair_scenario_0"
    assert scenario_calls[1].coverage_directive["retry_reason"] == "dsl_changed_since_scenario_freeze"
    assert coverage_calls == [
        ("needs-refresh-repair", ["needs-refresh-repair_scenario_0"]),
        ("fixed", ["needs-refresh-repair_scenario_0"]),
        ("fixed", ["fixed_scenario_1"]),
    ]
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.scenario_history[-1]["targeted_retry_after_dsl_change"] is True
    assert record.scenario_history[-1]["previous_scenario_set_id"] != record.iteration_records[-1]["scenario_set_id"]


def test_sl10_major_local_override_requires_structured_rationale(tmp_path: Path) -> None:
    """Mentioning local drift in evidence alone must not silently pass SL-10."""

    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-override":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def local_major(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="forced_transition_count_drift; missing_required_grounding",
            target_resolved=False,
            regression_detected=False,
            drift_risk="major",
            evidence=[{"kind": "forced_transition_count_drift"}, {"kind": "missing_required_grounding"}],
        )
        feedback = RepairReviewFeedback(ok=False, target_resolved=False, drift_risk="major", local_rejection=rejection)
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        feedback.meta = meta
        return feedback, meta

    def superficial_sl10_pass(_request: RepairRequest, _local_review: RepairReviewFeedback) -> Any:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW, ok=True)
        return SimpleNamespace(
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            ok=True,
            parsed_output={"decision": "pass", "target_resolved": True, "regression_detected": False, "drift_risk": "minor"},
            feedback=SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"summary": "forced_transition_count_drift and missing_required_grounding are acceptable"}],
                # Empty local_override_rationale is the regression: evidence mentions anchors, but no structured override.
                local_override_rationale=[],
                review_meta=_review_meta(StageId.SL_10_REPAIR_REVIEW),
                meta=meta,
            ),
            stage_meta=meta,
            interaction={"stage_id": StageId.SL_10_REPAIR_REVIEW.value, "schema_validation_ok": True},
        )

    result = run_full_staged_deterministic_runtime(
        "SL-10 needs structured override rationale for major local drift",
        FullStagedRuntimeConfig(initial_dsl="needs-override", run_id="pr-b1-sl10-structured-override", output_dir=tmp_path, max_iterations=1),
        adapters=_base_adapters(design=design, repair=lambda _request: "candidate", repair_review=local_major, sl10_review=superficial_sl10_pass),
    )

    assert result.status == "not_converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.repair_history[0]["accepted"] is False
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_10_REPAIR_REVIEW.value
    assert any("local_override_rationale" in text for text in record.repair_history[0]["sl10_repair_review"]["rework_instructions"])
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in _stage_ids(record)


def test_sl10_major_local_override_can_pass_when_structured_and_grounded(tmp_path: Path) -> None:
    def design(context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        if context.current_dsl == "needs-override-pass":
            item = DesignDiagnosticItem(
                code="W_DEADLOCK_LEAF",
                pyfcstm_severity="warning",
                policy_action="budgeted_repair",
                instance_key="W_DEADLOCK_LEAF:state=Idle",
            )
            return DesignFeedback(ok=False, blocking_items=[item]), _meta(StageId.SD_4_DESIGN, ok=False)
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    def local_major(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
        rejection = RepairRejection(
            rejected_by_stage=StageId.SD_10_REPAIR_REVIEW.value,
            reason="forced_transition_count_drift; missing_required_grounding",
            target_resolved=False,
            regression_detected=False,
            drift_risk="major",
            evidence=[{"kind": "forced_transition_count_drift"}, {"kind": "missing_required_grounding"}],
        )
        feedback = RepairReviewFeedback(ok=False, target_resolved=False, drift_risk="major", local_rejection=rejection)
        meta = _meta(StageId.SD_10_REPAIR_REVIEW, ok=False)
        feedback.meta = meta
        return feedback, meta

    def grounded_sl10_pass(_request: RepairRequest, _local_review: RepairReviewFeedback) -> Any:
        meta = _meta(StageId.SL_10_REPAIR_REVIEW, ok=True)
        return SimpleNamespace(
            stage_id=StageId.SL_10_REPAIR_REVIEW.value,
            ok=True,
            parsed_output={"decision": "pass", "target_resolved": True, "regression_detected": False, "drift_risk": "minor"},
            feedback=SL10RepairReviewOutput(
                ok=True,
                decision="pass",
                target_resolved=True,
                regression_detected=False,
                drift_risk="minor",
                evidence=[{"summary": "forced_transition_count_drift and missing_required_grounding are explained by a required structural expansion"}],
                local_override_rationale=[
                    "forced_transition_count_drift is expected because one NL-required transition expands over wildcard sources",
                    "missing_required_grounding is a matcher limitation; the required grounding IDs remain textually preserved",
                ],
                review_meta=_review_meta(StageId.SL_10_REPAIR_REVIEW),
                meta=meta,
            ),
            stage_meta=meta,
            interaction={"stage_id": StageId.SL_10_REPAIR_REVIEW.value, "schema_validation_ok": True},
        )

    result = run_full_staged_deterministic_runtime(
        "SL-10 may override major local drift only with structured grounded rationale",
        FullStagedRuntimeConfig(initial_dsl="needs-override-pass", run_id="pr-b1-sl10-structured-override-pass", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=lambda _request: "fixed", repair_review=local_major, sl10_review=grounded_sl10_pass),
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.repair_history[0]["accepted"] is True
    assert record.repair_history[0]["sl10_repair_review"]["local_override_rationale"]
    assert StageId.SC_11_ACCEPT_CANDIDATE.value in _stage_ids(record)


def test_sl7_grounding_update_hints_are_recorded_and_forwarded(tmp_path: Path) -> None:
    seen_grounding_maps: list[GroundingMap | None] = []

    def model_review(dsl: str, context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
        if dsl == "needs-grounding-repair":
            meta = _meta(StageId.SL_7_MODEL_REVIEW, ok=False, status=StageStatus.FAIL)
            return ModelReviewFeedback(
                ok=False,
                decision="fail",
                risk_level="major",
                findings=[{"category": "nl_fidelity", "severity": "major", "summary": "GroundingMap admitted abstraction is insufficient", "evidence": ["missing required grounding for explicit command"]}],
                blocking_findings=[{"category": "nl_fidelity", "severity": "major", "summary": "GroundingMap admitted abstraction is insufficient", "evidence": ["missing required grounding for explicit command"]}],
                review_meta=_review_meta(),
                meta=meta,
            ), meta
        return _ok_model_review(dsl, context, _feedback)

    def repair(request: RepairRequest) -> str:
        seen_grounding_maps.append(request.grounding_map)
        return "fixed"

    grounding = GroundingMap(source_summary={"source_stage": "test"})
    result = run_full_staged_deterministic_runtime(
        "GroundingMap should carry SL-7 discovered grounding gaps into repair context.",
        FullStagedRuntimeConfig(initial_dsl="needs-grounding-repair", grounding_map=grounding, run_id="pr-b1-grounding-hints", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(model_review=model_review, repair=repair),
    )

    assert result.status == "converged"
    assert seen_grounding_maps
    runtime_hints = seen_grounding_maps[0].source_summary.get("runtime_grounding_update_hints") if seen_grounding_maps[0] else ""
    assert runtime_hints and "missing required grounding" in runtime_hints.lower()
    record = read_agent_loop_run_record(result.run_record_path or "")
    assert record.final_artifacts["grounding_update_hints"]
    assert record.replay_index["grounding_update_hint_count"] >= 1
    assert any(entry["phase"] == "request_batch" for entry in record.fix_log)
