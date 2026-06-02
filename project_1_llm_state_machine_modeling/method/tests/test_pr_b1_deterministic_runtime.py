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
    run_full_staged_deterministic_runtime,
)
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


def test_llm_retry_exhausted_in_sl10b_exits_provider_error_before_sc11(tmp_path: Path) -> None:
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
        "SL-10B provider exhausted",
        FullStagedRuntimeConfig(initial_dsl="needs-delta-review", run_id="pr-b1-sl10b-provider", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(
            design=design,
            repair=lambda _request: "candidate",
            delta_review=lambda _request, _review: _retry_exhausted_run(StageId.SL_10B_DELTA_REVIEW, "provider_error"),
        ),
    )

    assert result.status == "api_failed"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_10B_DELTA_REVIEW.value
    assert StageId.SD_10_REPAIR_REVIEW.value in stage_ids
    assert StageId.SC_11_ACCEPT_CANDIDATE.value not in stage_ids
    assert record.repair_history == []


def test_sl10b_audit_only_typed_feedback_does_not_override_acceptance(tmp_path: Path) -> None:
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

    def audit_delta(_request: RepairRequest, _review: RepairReviewFeedback) -> Any:
        meta = _meta(StageId.SL_10B_DELTA_REVIEW, ok=True)
        return SimpleNamespace(
            stage_id=StageId.SL_10B_DELTA_REVIEW.value,
            ok=True,
            parsed_output={"decision": "reject", "drift_risk": "major", "audit_only": True},
            feedback=RepairReviewFeedback(
                ok=True,
                target_resolved=True,
                regression_detected=False,
                drift_risk="major",
                delta_review={"decision": "reject", "drift_risk": "major", "audit_only": True},
                review_meta=_review_meta(StageId.SL_10B_DELTA_REVIEW),
                meta=meta,
            ),
            stage_meta=meta,
            interaction={
                "stage_id": StageId.SL_10B_DELTA_REVIEW.value,
                "schema_validation_ok": True,
                "retry_error": None,
            },
        )

    result = run_full_staged_deterministic_runtime(
        "SL-10B audit-only should not block SC-11",
        FullStagedRuntimeConfig(initial_dsl="needs-audit-delta", run_id="pr-b1-sl10b-audit", output_dir=tmp_path, max_iterations=2),
        adapters=_base_adapters(design=design, repair=lambda _request: "fixed", delta_review=audit_delta),
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = _stage_ids(record)
    assert record.repair_history[0]["accepted"] is True
    assert record.repair_history[0]["repair_review"]["delta_review"]["decision"] == "reject"
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
