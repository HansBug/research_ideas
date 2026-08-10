from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

from archive.agent_loop_method.experiments.real_run_matrix import (
    PrE1RunSummary,
    condition_specs,
    make_pr_e1_config,
    pr_e1_cases,
    render_matrix_summary,
    render_pr_comment,
    render_run_report,
    run_pr_e1_matrix,
    summarize_pr_e1_run,
)
from archive.agent_loop_method.run_record import write_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult, AgentLoopRunRecord
from archive.agent_loop_method.stages.ids import STAGE_SPECS_BY_ID, StageStatus


def _stage_meta(stage_id: str, *, ok: bool = True) -> dict[str, object]:
    spec = STAGE_SPECS_BY_ID[stage_id]
    return {
        "stage_id": stage_id,
        "stage_kind": spec.kind.value,
        "enabled": True,
        "ran": True,
        "status": StageStatus.OK.value if ok else StageStatus.FAIL.value,
        "ok": ok,
    }


def _record(run_id: str, *, condition_id: str = "full_staged_v1") -> AgentLoopRunRecord:
    executed = ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SD-8", "SL-9", "SL-10", "SC-11", "SC-12", "SC-13"]
    return AgentLoopRunRecord(
        schema_version="pr-c.default-full-staged-runtime.v1",
        run_id=run_id,
        created_at="2026-06-02T12:00:00Z",
        status="rejected",
        input_bundle={"nl": "test NL", "nl_hash": "sha256:nl", "default_loop_config_entry_integrated": True},
        run_config={"condition_id": condition_id, "llm_provider_mode": "real_env"},
        environment={
            "git_commit": "abcdef",
            "provider_mode": "real_env",
            "provider_model_redacted": "gpt-test",
            "real_llm_provider_api": True,
            "provider_config_read": True,
            "resolved_config": {"condition_id": condition_id, "policy_profile": "experiment_default"},
        },
        stage_graph={"planned": [spec.stage_id for spec in STAGE_SPECS_BY_ID.values()], "executed": executed},
        stage_records=[_stage_meta(stage_id, ok=stage_id not in {"SC-11", "SC-12"}) for stage_id in executed],
        iteration_records=[
            {
                "iteration": 0,
                "stage_ids": ["SD-2", "SD-3", "SD-4"],
                "selected_feedback": {"source": "design", "source_stage": "SD-4", "blocking": True},
                "repair_stage_ids": ["SD-8", "SL-9", "SL-10", "SC-11"],
                "repair_review": {"ok": False, "target_resolved": False, "drift_risk": "none", "delta_review": None},
                "accepted_candidate": False,
                "exit_reason": "design_target_unresolved",
            }
        ],
        llm_interactions=[
            {
                "stage_id": "SL-1",
                "provider": "openai-compatible-env",
                "model_id": "gpt-test",
                "resolved_model_id": "gpt-test",
                "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
                "retry_count": 0,
                "schema_validation_ok": True,
                "attempts": [{"attempt_index": 0, "error_kind": None, "model_id": "gpt-test"}],
                "parsed_output": {"candidate_dsl": "state Root { [*] -> Idle; state Idle; }"},
            },
            {
                "stage_id": "SL-9",
                "provider": "openai-compatible-env",
                "model_id": "gpt-test",
                "usage": {"prompt_tokens": 20, "completion_tokens": 7, "total_tokens": 27},
                "retry_count": 0,
                "schema_validation_ok": True,
                "attempts": [{"attempt_index": 0, "error_kind": None, "model_id": "gpt-test"}],
                "parsed_output": {"candidate_dsl": "state Root { [*] -> Idle; state Idle; }"},
            },
        ],
        deterministic_feedback={
            "iterations": [
                {
                    "parse": {"ok": True, "diagnostics": []},
                    "semantic": {"ok": True, "diagnostics": []},
                    "design": {"blocking_items": [{"code": "W_UNWRITTEN_READ_VAR"}], "advisory_items": [], "info_items": []},
                    "sim": None,
                }
            ]
        },
        repair_history=[
            {
                "iteration": 0,
                "selected_feedback": {"source": "design", "source_stage": "SD-4"},
                "candidate_dsl": "state Root { [*] -> Idle; state Idle; }",
                "repair_review": {"ok": False, "target_resolved": False, "drift_risk": "none"},
                "accepted": False,
                "repair_stage_ids": ["SD-8", "SL-9", "SL-10", "SC-11"],
            }
        ],
        scenario_history=[],
        final_artifacts={
            "final_dsl": "state Root { [*] -> Idle; state Idle; }",
            "final_dsl_hash": "sha256:final",
            "verdict": "not_converged",
            "verdict_source_stage_id": "SC-11",
            "verdict_reason": "design_target_unresolved",
            "agent_loop_result_status": "not_converged",
            "oracle_weak": False,
            "main_result_eligible": False,
            "inclusion_reason": None,
            "exclusion_reason": "verdict_not_success",
            "error_message": "design_target_unresolved",
        },
        logs=[{"event": "sc12_verdict", "verdict": "not_converged"}],
        replay_index={"iteration_count": 1, "repair_count": 1, "scenario_history_count": 0},
        redaction_report=[],
    )


def test_pr_e1_conditions_make_default_vs_exploratory_configs(tmp_path: Path) -> None:
    specs = condition_specs()

    default_cfg = make_pr_e1_config(specs["default"], output_dir=tmp_path, run_id="default-run")
    iter8_cfg = make_pr_e1_config(specs["iter8"], output_dir=tmp_path, run_id="iter8-run")
    postaccept_cfg = make_pr_e1_config(specs["postaccept1"], output_dir=tmp_path, run_id="postaccept-run")

    assert default_cfg.condition_id == "full_staged_v1"
    assert default_cfg.policy_profile == "experiment_default"
    assert iter8_cfg.condition_id == "pr_e1_iter8_v1"
    assert iter8_cfg.policy_profile == "pr_e1_exploratory"
    assert iter8_cfg.max_iterations == 8
    assert "max_iterations=8" in iter8_cfg.changed_factors
    assert postaccept_cfg.condition_id == "pr_e1_postaccept1_v1"
    assert postaccept_cfg.policy_profile == "pr_e1_exploratory"
    assert postaccept_cfg.max_iterations == 1
    assert "post_accept_boundary_stress=true" in postaccept_cfg.changed_factors


def test_pr_e1_cases_include_mandatory_and_e2_aligned_screening_set() -> None:
    mandatory = pr_e1_cases("mandatory")
    e2_aligned = pr_e1_cases("e2-aligned")

    assert [case.case_key for case in mandatory] == ["path1_cara", "path2_lng_ems"]
    assert {case.case_key for case in e2_aligned} == {
        "path1_abs",
        "path1_elevator",
        "path1_cara",
        "path2_lng_ems",
    }
    assert all(case.source_path and case.selection_rationale for case in e2_aligned)


def test_pr_e1_runner_writes_report_artifacts_with_fake_entry(tmp_path: Path) -> None:
    case = pr_e1_cases()[0]

    def fake_run(nl: str, cfg) -> AgentLoopResult:
        assert nl in {item.nl for item in pr_e1_cases()}
        record = _record(cfg.run_id, condition_id=cfg.condition_id)
        path = write_agent_loop_run_record(record, Path(cfg.output_dir) / f"{cfg.run_id}.agent_loop.json.gz")
        return AgentLoopResult(
            final_dsl=record.final_artifacts["final_dsl"],
            status="not_converged",
            error_message="design_target_unresolved",
            run_record_id=cfg.run_id,
            run_record_path=str(path),
        )

    summaries = run_pr_e1_matrix(
        output_dir=tmp_path,
        case_set="mandatory",
        condition_set=["default"],
        run_agent_loop_fn=fake_run,
        require_provider_env=False,
        run_tag="testtag",
    )

    assert len(summaries) == 2
    assert all(isinstance(item, PrE1RunSummary) for item in summaries)
    for summary in summaries:
        report = Path(summary.report_path)
        assert report.exists()
        text = report.read_text(encoding="utf-8")
        assert "输入 NL 中文翻译" in text
        assert "最终产出的 FCSTM DSL" in text
        assert "Iteration / repair / review 摘要" in text
        assert "完整流程日志" in text
        assert "stage/control-flow replay ledger" in text
        assert "flow_log.json" in text
        assert "Repair / blocking feedback 明细" in text
        assert "为什么进入修复" in text
        assert "Candidate diff" in text
        assert "SL-10 审查结果" in text
        assert "reproducibility.json" in text
        assert Path(summary.reproducibility_path).exists()
        assert (report.parent / "flow_log.json").exists()
        assert (report.parent / "fix_log.json").exists()
        assert summary.prompt_snapshot_hash
        assert summary.token_usage["total_tokens"] == 42
        assert summary.token_usage["token_usage_available"] is True
        assert summary.primary_failure_class == "design_or_variable_dynamics"
    assert (tmp_path / "SUMMARY.md").exists()
    assert (tmp_path / "pr_comment.md").exists()
    payload = json.loads((tmp_path / "summary.json").read_text(encoding="utf-8"))
    assert payload[0]["config_id"] == "default"


def test_pr_e1_matrix_summary_marks_exploratory_and_sample_screening() -> None:
    text = render_matrix_summary([])

    assert "非 default 条件均为显式 exploratory condition" in text
    assert "吉祥物变量" in text
    assert "先定义标准，再筛样本" in text
    assert "可复现性边界" in text


def test_pr_e1_failure_class_is_trace_driven_for_sd6_sl10_rework() -> None:
    record = _record("trace-classifier")
    record.status = "rejected"
    record.iteration_records = [
        {
            "iteration": 4,
            "selected_feedback": {"source": "sim", "source_stage": "SD-6", "n_scenarios": 15, "n_scenarios_passed": 10},
            "exit_reason": "SD-6 sim failure: 10/15 scenarios passed",
        }
    ]
    record.repair_history = [
        {
            "iteration": 4,
            "selected_feedback": {"source": "sim", "source_stage": "SD-6"},
            "candidate_dsl_hash": "sha256:rejected",
            "accepted": False,
            "sl10_repair_review": {"decision": "rework", "rework_instructions": ["semantic sounding text"]},
        }
    ]
    record.final_artifacts["verdict"] = "not_converged"
    record.final_artifacts["verdict_reason"] = "semantic transition text from last rejected candidate"

    from archive.agent_loop_method.experiments.real_run_matrix import classify_primary_failure

    assert classify_primary_failure(record) == "repair_review_rework_budget"


def test_pr_e1_success_with_weak_oracle_is_not_plain_success() -> None:
    record = _record("weak-success")
    record.status = "success"
    record.final_artifacts["verdict"] = "success"
    record.final_artifacts["verdict_reason"] = "full_pass_all_required_feedback_ok"
    record.final_artifacts["oracle_weak"] = True
    record.final_artifacts["main_result_eligible"] = False
    record.final_artifacts["exclusion_reason"] = "weak_oracle"

    from archive.agent_loop_method.experiments.real_run_matrix import classify_primary_failure

    assert classify_primary_failure(record) == "success_but_weak_oracle_ineligible"


def test_pr_e1_missing_required_stages_do_not_require_legacy_sd10_sl10b(tmp_path: Path) -> None:
    record = _record("pr-e1-required")
    record.status = "success"
    record.stage_records = [_stage_meta(stage_id, ok=True) for stage_id in ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SC-12", "SC-13"]]
    record.final_artifacts["verdict"] = "success"
    record.final_artifacts["main_result_eligible"] = True
    path = write_agent_loop_run_record(record, tmp_path / "required.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=record.final_artifacts["final_dsl"], status="converged", run_record_id="required", run_record_path=str(path))

    from archive.agent_loop_method.experiments.real_run_matrix import summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case=pr_e1_cases()[0],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert "SD-10" not in summary.missing_required_stage_ids
    assert "SL-10B" not in summary.missing_required_stage_ids
    assert "SD-8" not in summary.missing_required_stage_ids
    assert "SL-9" not in summary.missing_required_stage_ids
    assert "SC-11" not in summary.missing_required_stage_ids



def test_pr_e1_waiver_continue_does_not_require_sl10_sc11(tmp_path: Path) -> None:
    record = _record("waiver-required")
    record.status = "success"
    executed = ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SD-8", "SL-9", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SC-12", "SC-13"]
    record.stage_graph["executed"] = executed
    record.stage_records = [_stage_meta(stage_id, ok=True) for stage_id in executed]
    record.fix_log = [
        {"next_action": "sl9_decision_and_repair"},
        {"next_action": "reject_or_waiver"},
        {"next_action": "continue_after_waiver"},
    ]
    record.iteration_records = [
        {
            "iteration": 0,
            "stage_ids": executed[2:-2],
            "selected_feedback": {"source": "design", "source_stage": "SD-4", "blocking": True},
            "post_waiver_stage_ids": ["SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7"],
            "exit_reason": "full_pass_all_required_feedback_ok_after_waiver_continue",
        }
    ]
    record.final_artifacts["verdict"] = "success"
    record.final_artifacts["verdict_reason"] = "full_pass_all_required_feedback_ok_after_waiver_continue"
    record.final_artifacts["main_result_eligible"] = True
    path = write_agent_loop_run_record(record, tmp_path / "waiver-required.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=record.final_artifacts["final_dsl"], status="converged", run_record_id="waiver-required", run_record_path=str(path))

    from archive.agent_loop_method.experiments.real_run_matrix import summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case=pr_e1_cases(case_keys=["path2_lng_ems"])[0],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert "SD-8" not in summary.missing_required_stage_ids
    assert "SL-9" not in summary.missing_required_stage_ids
    assert "SL-10" not in summary.missing_required_stage_ids
    assert "SC-11" not in summary.missing_required_stage_ids


def test_pr_e1_summary_records_fixlog_and_final_dsl_source(tmp_path: Path) -> None:
    record = _record("source-summary")
    final_hash = "sha256:accepted"
    record.final_artifacts["final_dsl_hash"] = final_hash
    record.repair_history = [
        {"iteration": 0, "candidate_dsl_hash": final_hash, "accepted": True, "sl10_repair_review": {"decision": "pass"}, "selected_feedback": {"source_stage": "SL-7"}},
        {"iteration": 1, "candidate_dsl_hash": "sha256:rejected", "accepted": False, "sl10_repair_review": {"decision": "rework", "rework_instructions": ["do not use"]}},
    ]
    record.fix_log = [
        {"next_action": "sl10_review"},
        {"next_action": "sc11_accept_then_sd2"},
        {"next_action": "exit_rejected_rework_budget_exhausted"},
    ]
    record.iteration_records = [
        {"iteration": 0, "exit_reason": "candidate_accepted_for_next_full_pass"},
        {
            "iteration": 1,
            "exit_reason": "SD-6 sim failure: 1/2 scenarios passed",
            "budget_gate": {
                "post_accept_validation_attempted": True,
                "post_accept_validation_success": False,
            },
        },
    ]
    path = write_agent_loop_run_record(record, tmp_path / "source-summary.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=record.final_artifacts["final_dsl"], status="not_converged", run_record_id="source-summary", run_record_path=str(path))
    case = pr_e1_cases()[0]
    spec = condition_specs()["default"]

    from archive.agent_loop_method.experiments.real_run_matrix import summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case=case,
        spec=spec,
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert summary.fix_log_next_actions[-1] == "exit_rejected_rework_budget_exhausted"
    assert summary.iteration_exit_reasons[-1].startswith("SD-6 sim failure")
    assert summary.final_dsl_source["repair_history_index"] == 0
    assert summary.final_dsl_source["last_rejected_candidate"]["candidate_dsl_hash"] == "sha256:rejected"
    assert summary.post_accept_validation_attempted is True
    assert summary.post_accept_validation_attempt_count == 1
    assert summary.post_accept_validation_success_count == 0
    assert summary.post_accept_validation_failure_count == 1


def test_pr_e1_report_and_matrix_show_post_accept_coverage(tmp_path: Path) -> None:
    record = _record("post-accept-summary")
    record.status = "success"
    record.stage_records = [_stage_meta(stage_id, ok=True) for stage_id in ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SD-8", "SL-9", "SL-10", "SC-11", "SD-2", "SD-3", "SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SC-12", "SC-13"]]
    record.iteration_records = [
        {
            "iteration": 0,
            "selected_feedback": {"source": "design", "source_stage": "SD-4"},
            "repair_stage_ids": ["SD-8", "SL-9", "SL-10", "SC-11"],
            "accepted_candidate": True,
            "post_accept_stage_ids": ["SD-2", "SD-3", "SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7"],
            "post_accept_selected_feedback": None,
            "exit_reason": "full_pass_all_required_feedback_ok_after_sc11_post_accept_validation",
            "budget_gate": {
                "post_accept_validation_attempted": True,
                "post_accept_validation_success": True,
            },
        }
    ]
    record.final_artifacts.update(
        {
            "verdict": "success",
            "verdict_reason": "full_pass_all_required_feedback_ok_after_sc11_post_accept_validation",
            "main_result_eligible": True,
            "exclusion_reason": None,
        }
    )
    path = write_agent_loop_run_record(record, tmp_path / "post-accept.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=record.final_artifacts["final_dsl"], status="success", run_record_id=record.run_id, run_record_path=str(path))
    case = pr_e1_cases()[0]
    summary = summarize_pr_e1_run(
        case=case,
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    report = render_run_report(case, condition_specs()["default"], record, summary)
    matrix = render_matrix_summary([summary])
    comment = render_pr_comment([summary], output_dir=tmp_path)

    assert summary.post_accept_validation_attempted is True
    assert summary.post_accept_validation_attempt_count == 1
    assert summary.post_accept_validation_success_count == 1
    assert "SC-11 post-accept validation" in report
    assert "attempted=`true`" in report
    assert "post-accept" in matrix
    assert "triggered=1/1" in matrix
    assert "✅ 1/1; ❌ 0" in comment


def test_pr_e1_final_dsl_source_prefers_later_accepted_same_hash(tmp_path: Path) -> None:
    record = _record("source-accepted-after-rework")
    final_hash = "sha256:repeat"
    record.final_artifacts["final_dsl_hash"] = final_hash
    record.repair_history = [
        {
            "iteration": 0,
            "candidate_dsl_hash": final_hash,
            "accepted": False,
            "sl10_repair_review": {"decision": "rework", "rework_instructions": ["add explicit mapping"]},
            "selected_feedback": {"source_stage": "SD-6"},
        },
        {
            "iteration": 0,
            "candidate_dsl_hash": final_hash,
            "accepted": True,
            "sl10_repair_review": {"decision": "pass"},
            "selected_feedback": {"source_stage": "SD-6"},
        },
    ]
    path = write_agent_loop_run_record(record, tmp_path / "source-repeat.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=record.final_artifacts["final_dsl"], status="converged", run_record_id="source-repeat", run_record_path=str(path))

    from archive.agent_loop_method.experiments.real_run_matrix import summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case=pr_e1_cases()[0],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert summary.final_dsl_source["accepted"] is True
    assert summary.final_dsl_source["sl10_decision"] == "pass"
    assert summary.final_dsl_source["repair_history_index"] == 1
    assert summary.final_dsl_source["matching_repair_history_indices"] == [0, 1]
    assert summary.final_dsl_source["accepted_after_rework"] is True
    assert summary.final_dsl_source["last_rejected_candidate"]["same_as_final"] is True


def test_pr_e1_case_metadata_marks_external_inputs_outputs_and_state_mode_policy() -> None:
    cases = {case.case_key: case for case in pr_e1_cases("all")}

    assert "外部" in cases["path1_abs"].variable_participation_note
    assert "只读" in cases["path1_abs"].variable_participation_note
    assert "纯输出" in cases["path1_elevator"].variable_participation_note
    assert "state_mode_decorative" in cases["path2_lng_ems"].state_mode_participation_note



def test_pr_e1_path2_blueprint_eligibility_is_stricter_than_main_result(tmp_path: Path) -> None:
    record = _record("path2-blueprint")
    record.status = "success"
    record.stage_records = [_stage_meta(stage_id, ok=True) for stage_id in ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SC-12", "SC-13"]]
    forced_classifier_dsl = """def float load_demand = 0.0;
def float supply_capacity = 0.0;

state DispatchClassifier {
    ! * -> Surplus : if [supply_capacity >= load_demand];
    ! * -> Balanced : if [supply_capacity == load_demand];
    ! * -> BatteryAssist : if [supply_capacity < load_demand];
    ! * -> EngineAssist : if [supply_capacity + 10 >= load_demand];
    ! * -> ShedLoad : if [supply_capacity + 10 < load_demand];
    ! * -> Recovery : if [load_demand == 0];
    [*] -> Surplus;
    state Surplus;
    state Balanced;
    state BatteryAssist;
    state EngineAssist;
    state ShedLoad;
    state Recovery;
}
"""
    record.final_artifacts.update(
        {
            "final_dsl": forced_classifier_dsl,
            "final_dsl_hash": "sha256:path2",
            "verdict": "success",
            "verdict_reason": "full_pass_all_required_feedback_ok",
            "agent_loop_result_status": "success",
            "main_result_eligible": True,
            "exclusion_reason": None,
        }
    )
    path = write_agent_loop_run_record(record, tmp_path / "path2-blueprint.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=forced_classifier_dsl, status="success", run_record_id="path2-blueprint", run_record_path=str(path))

    from archive.agent_loop_method.experiments.real_run_matrix import render_matrix_summary, summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case={case.case_key: case for case in pr_e1_cases("all")}["path2_lng_ems"],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert summary.main_result_eligible is True
    assert summary.state_mode_decorative_detected is True
    assert summary.path2_ref_model_blueprint_eligible is False
    assert "dispatch-classifier" in summary.path2_ref_model_blueprint_reason
    rendered = render_matrix_summary([summary])
    assert "Path2 ref-model blueprint" in rendered
    assert "main_result_eligible=`true`" in rendered
    assert "path2_ref_model_blueprint_eligible=`false`" in rendered


def test_pr_e1_path2_blueprint_allows_non_decorative_mode_model(tmp_path: Path) -> None:
    record = _record("path2-modeful")
    record.status = "success"
    modeful_dsl = """state ModefulDispatch {
    [*] -> Standby;
    state Standby;
    state Dispatching;
    state Faulted;
    Standby -> Dispatching :: StartDispatch;
    Dispatching -> Standby :: StopDispatch;
    ! * -> Faulted :: FaultDetected;
}
"""
    record.final_artifacts.update(
        {
            "final_dsl": modeful_dsl,
            "final_dsl_hash": "sha256:modeful",
            "verdict": "success",
            "agent_loop_result_status": "success",
            "main_result_eligible": True,
            "exclusion_reason": None,
        }
    )
    path = write_agent_loop_run_record(record, tmp_path / "path2-modeful.agent_loop.json.gz")
    result = AgentLoopResult(final_dsl=modeful_dsl, status="success", run_record_id="path2-modeful", run_record_path=str(path))

    from archive.agent_loop_method.experiments.real_run_matrix import summarize_pr_e1_run

    summary = summarize_pr_e1_run(
        case={case.case_key: case for case in pr_e1_cases("all")}["path2_lng_ems"],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    assert summary.main_result_eligible is True
    assert summary.state_mode_decorative_detected is False
    assert summary.path2_ref_model_blueprint_eligible is True


def test_pr_e1_reproducibility_payload_records_env_loading_command(tmp_path: Path) -> None:
    from archive.agent_loop_method.experiments.real_run_matrix import build_reproducibility_payload

    case = pr_e1_cases("all", case_keys=["path1_abs"])[0]
    spec = condition_specs()["default"]
    cfg = make_pr_e1_config(spec, output_dir=tmp_path / "run", run_id="repro-env")

    payload = build_reproducibility_payload(
        case=case,
        spec=spec,
        cfg=cfg,
        run_id="repro-env",
        output_root=tmp_path,
        started_at="2026-06-06T00:00:00Z",
    )

    command = payload["command"]
    assert command["env_loading_command"] == "set -a; source .env; set +a"
    assert "source .env" in command["canonical_example"]
    assert command["canonical_example"].startswith("bash -lc '")
    assert "raw endpoint path/API key are never stored" in command["secret_policy"]


def test_pr_e1_quality_boundary_is_persisted_in_canonical_record(tmp_path: Path) -> None:
    from archive.agent_loop_method.experiments.real_run_matrix import _inject_pr_e1_quality_boundary, summarize_pr_e1_run
    from archive.agent_loop_method.run_record import read_agent_loop_run_record

    record = _record("path2-boundary-canonical")
    record.status = "success"
    forced_classifier_dsl = """def float load_demand = 0.0;
def float supply_capacity = 0.0;

state DispatchClassifier {
    ! * -> Surplus : if [supply_capacity >= load_demand];
    ! * -> Balanced : if [supply_capacity == load_demand];
    ! * -> BatteryAssist : if [supply_capacity < load_demand];
    ! * -> EngineAssist : if [supply_capacity + 10 >= load_demand];
    ! * -> ShedLoad : if [supply_capacity + 10 < load_demand];
    ! * -> Recovery : if [load_demand == 0];
    [*] -> Surplus;
    state Surplus;
    state Balanced;
    state BatteryAssist;
    state EngineAssist;
    state ShedLoad;
    state Recovery;
}
"""
    record.final_artifacts.update(
        {
            "final_dsl": forced_classifier_dsl,
            "final_dsl_hash": "sha256:path2-boundary",
            "verdict": "success",
            "verdict_reason": "full_pass_all_required_feedback_ok",
            "agent_loop_result_status": "success",
            "main_result_eligible": True,
            "exclusion_reason": None,
        }
    )
    path = write_agent_loop_run_record(record, tmp_path / "path2-boundary.agent_loop.json.gz")
    result = AgentLoopResult(
        final_dsl=forced_classifier_dsl,
        status="success",
        run_record_id="path2-boundary-canonical",
        run_record_path=str(path),
    )
    summary = summarize_pr_e1_run(
        case={case.case_key: case for case in pr_e1_cases("all")}["path2_lng_ems"],
        spec=condition_specs()["default"],
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    _inject_pr_e1_quality_boundary(record, summary)
    write_agent_loop_run_record(record, path)
    persisted = read_agent_loop_run_record(path)

    assert persisted.final_artifacts["state_mode_decorative_detected"] is True
    assert persisted.final_artifacts["path2_ref_model_blueprint_eligible"] is False
    assert "dispatch-classifier" in persisted.final_artifacts["path2_ref_model_blueprint_reason"]
    boundary = persisted.final_artifacts["pr_e1_quality_boundary"]
    assert boundary["schema_version"] == "pr-e1.quality-boundary.v1"
    assert boundary["main_result_eligible_unchanged"] is True
    assert persisted.run_config["pr_e1_quality_boundary"] == boundary
    assert any(item.get("event") == "pr_e1_quality_boundary" for item in persisted.logs)

def test_pr_e1_matrix_summary_separates_provider_invalid_denominator() -> None:
    ok = PrE1RunSummary(
        case_key="path1_abs",
        path="path1",
        case_id="abs",
        config_id="default",
        condition_id="full_staged_v1",
        run_id="ok-run",
        result_status="success",
        record_status="success",
        verdict="success",
        verdict_reason="ok",
        verdict_source_stage_id="SC-12",
        main_result_eligible=True,
        oracle_weak=False,
        schema_valid=True,
        schema_error=None,
        secret_redacted=True,
        redaction_report_count=0,
        provider_mode="real_env",
        provider_model_redacted="model",
        real_llm_provider_api=True,
        provider_config_read=True,
        git_commit="abc",
        git_dirty=False,
        git_diff_hash="sha256:diff",
        prompt_snapshot_hash="sha256:prompt",
        reproducibility_path="reproducibility.json",
        clean_commit_bound=True,
        elapsed_seconds=1.0,
        token_usage={"total_tokens": 10, "token_usage_available": True},
        stage_count=1,
        executed_stage_ids=["SC-0"],
        missing_required_stage_ids=[],
        llm_stage_ids=[],
        iteration_count=1,
        repair_count=0,
        accepted_repair_count=0,
        scenario_history_count=0,
        final_dsl_length=1,
        final_dsl_hash="sha256:ok",
        run_record_path="ok.agent_loop.json.gz",
        report_path="ok/report.md",
        summary_path="ok/summary.json",
        final_dsl_path="ok/final.fcstm",
        checks_path="ok/checks.json",
        stdout_path="ok/stdout.txt",
        stderr_path="ok/stderr.txt",
        primary_failure_class="success",
    )
    invalid = replace(
        ok,
        run_id="provider-run",
        result_status="error",
        record_status="error",
        verdict="provider_error",
        main_result_eligible=False,
        primary_failure_class="provider_or_retry",
        final_dsl_hash="sha256:provider",
    )

    from archive.agent_loop_method.experiments.real_run_matrix import render_matrix_summary

    text = render_matrix_summary([ok, invalid])
    assert "1/1 effective success" in text
    assert "provider/network invalid=1/2" in text
    assert "当前 1/1 个非 infrastructure run" in text


def test_pr_e1_reports_render_langgraph_runtime_metadata(tmp_path: Path) -> None:
    record = _record("langgraph-metadata")
    record.environment.update(
        {
            "graph_runtime_backend": "langgraph",
            "graph_runtime_status": "enabled",
            "langgraph_version": "1.2.4",
            "langgraph_checkpoint_version": "4.1.1",
            "graph_config_hash": "sha256:graph",
            "node_edge_schema_version": "pr-langgraph.stage-nodes.v1",
            "checkpoint_backend": "memory",
            "checkpoint_serde": "pickle",
            "resumed_from_checkpoint": False,
            "instrumentation_layer": "langgraph",
            "stage_semantics_module": "archive.agent_loop_method.staged_runtime",
            "langgraph_node_trace_count": 3,
            "checkpoint_resume_smoke": {
                "scope": "toy_ledger_langgraph_api_smoke",
                "real_agent_loop_resume_supported": False,
                "resume_append_only": True,
                "academic_claim": "toy checkpoint smoke only; not evidence for real agent-loop resume",
            },
            "langgraph_compat_smoke": {"ok": True},
        }
    )
    record.final_artifacts["langgraph_runtime_trace"] = {
        "delegated_monolithic_runtime": False,
        "node_trace_count": 3,
    }
    path = write_agent_loop_run_record(record, tmp_path / "langgraph.agent_loop.json.gz")
    result = AgentLoopResult(
        final_dsl=record.final_artifacts["final_dsl"],
        status="not_converged",
        run_record_id=record.run_id,
        run_record_path=str(path),
    )
    case = pr_e1_cases()[0]
    spec = condition_specs()["default"]
    summary = summarize_pr_e1_run(
        case=case,
        spec=spec,
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )

    report = render_run_report(case, spec, record, summary)
    matrix = render_matrix_summary([summary])
    comment = render_pr_comment([summary], output_dir=tmp_path)

    assert "LangGraph runtime metadata / checkpoint 口径" in report
    assert "`graph_runtime_backend` | `langgraph`" in report
    assert "real_agent_loop_resume_supported=false" in report
    assert "graph_runtime_status：`enabled`" in matrix
    assert "checkpoint/resume 口径：scope=`toy_ledger_langgraph_api_smoke`" in comment


def test_pr_e1_matrix_summary_reports_missing_langgraph_metadata_without_crash(tmp_path: Path) -> None:
    record = _record("metadata-present")
    record.environment.update(
        {
            "graph_runtime_backend": "langgraph",
            "graph_runtime_status": "enabled",
            "langgraph_node_trace_count": 2,
        }
    )
    record.final_artifacts["langgraph_runtime_trace"] = {
        "delegated_monolithic_runtime": False,
        "node_trace_count": 2,
    }
    path = write_agent_loop_run_record(record, tmp_path / "metadata-present.agent_loop.json.gz")
    result = AgentLoopResult(
        final_dsl=record.final_artifacts["final_dsl"],
        status="not_converged",
        run_record_id=record.run_id,
        run_record_path=str(path),
    )
    case = pr_e1_cases()[0]
    spec = condition_specs()["default"]
    present = summarize_pr_e1_run(
        case=case,
        spec=spec,
        result=result,
        record=record,
        elapsed_seconds=1.0,
        run_dir=tmp_path,
        stdout_path=tmp_path / "stdout.txt",
        stderr_path=tmp_path / "stderr.txt",
        reproducibility_payload={},
        reproducibility_path=tmp_path / "reproducibility.json",
    )
    missing = replace(
        present,
        run_id="metadata-missing",
        run_record_path=str(tmp_path / "missing.agent_loop.json.gz"),
        report_path="missing/report.md",
        final_dsl_hash="sha256:missing",
    )

    matrix = render_matrix_summary([present, missing])

    assert "graph_runtime_backend：`langgraph`" in matrix
    assert "metadata 缺失 run：`metadata-missing`" in matrix
