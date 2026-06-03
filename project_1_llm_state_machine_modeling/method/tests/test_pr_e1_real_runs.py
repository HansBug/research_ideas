from __future__ import annotations

import json
from pathlib import Path

from method.pr_e1_real_runs import (
    PrE1RunSummary,
    condition_specs,
    make_pr_e1_config,
    pr_e1_cases,
    render_matrix_summary,
    run_pr_e1_matrix,
)
from method.run_record import write_agent_loop_run_record
from method.schema import AgentLoopResult, AgentLoopRunRecord
from method.stages.ids import STAGE_SPECS_BY_ID, StageStatus


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
    executed = ["SC-0", "SL-1", "SD-2", "SD-3", "SD-4", "SD-8", "SL-9", "SD-10", "SC-11", "SC-12", "SC-13"]
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
                "repair_stage_ids": ["SD-8", "SL-9", "SD-10", "SC-11"],
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
                "repair_stage_ids": ["SD-8", "SL-9", "SD-10", "SC-11"],
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

    assert default_cfg.condition_id == "full_staged_v1"
    assert default_cfg.policy_profile == "experiment_default"
    assert iter8_cfg.condition_id == "pr_e1_iter8_v1"
    assert iter8_cfg.policy_profile == "pr_e1_exploratory"
    assert iter8_cfg.max_iterations == 8
    assert "max_iterations=8" in iter8_cfg.changed_factors


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
        assert "reproducibility.json" in text
        assert Path(summary.reproducibility_path).exists()
        assert summary.prompt_snapshot_hash
        assert summary.token_usage["total_tokens"] == 42
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
