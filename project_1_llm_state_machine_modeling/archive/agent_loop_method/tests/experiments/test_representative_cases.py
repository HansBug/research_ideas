from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from archive.agent_loop_method.experiments.representative_cases import (
    FULL_STAGED_REQUIRED_STAGE_IDS,
    RepresentativeCase,
    _schema_validation_error,
    assert_pr_d_provider_env,
    make_pr_d_config,
    missing_provider_env,
    render_issue_comment,
    representative_cases,
    run_representative_cases,
    summarize_run,
    summaries_to_jsonable,
)
from archive.agent_loop_method.run_record import write_agent_loop_run_record
from archive.agent_loop_method.schema import AgentLoopResult, AgentLoopRunRecord
from archive.agent_loop_method.stages.ids import STAGE_SPECS_BY_ID, StageStatus


def _case() -> RepresentativeCase:
    return representative_cases()[0]


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


def _record(*, run_id: str = "pr-d-path1_cara", final_dsl: str = "state Root { [*] -> Idle; state Idle; }") -> AgentLoopRunRecord:
    executed_stage_ids = ["SC-0", "SL-1", "SD-2", "SD-8", "SL-9", "SD-10", "SC-11", "SC-12", "SC-13"]
    return AgentLoopRunRecord(
        schema_version="pr-c.default-full-staged-runtime.v1",
        run_id=run_id,
        created_at="2026-06-02T12:00:00Z",
        status="budget_exhausted",
        input_bundle={
            "nl": "<redacted-by-test>",
            "nl_hash": "sha256:nl",
            "path_context": {"case_key": "path1_cara"},
            "default_loop_config_entry_integrated": True,
        },
        run_config={
            "condition_id": "full_staged_v1",
            "policy_profile": "experiment_default",
            "adapter_mode": "real_env",
            "allow_main_result_eligible": True,
        },
        environment={
            "git_commit": "abcdef123456",
            "provider_mode": "real_env",
            "real_llm_provider_api": True,
            "provider_config_read": True,
            "provider_model_redacted": "gpt-test",
            "config_hash": "hash-config",
            "resolved_config": {
                "condition_id": "full_staged_v1",
                "policy_profile": "experiment_default",
                "condition_hash": "hash-config",
                "llm_provider_mode": "real_env",
            },
        },
        stage_graph={
            "planned": FULL_STAGED_REQUIRED_STAGE_IDS,
            "executed": executed_stage_ids,
        },
        stage_records=[_stage_meta(stage_id, ok=stage_id not in {"SC-12"}) for stage_id in executed_stage_ids],
        iteration_records=[
            {
                "iteration": 0,
                "stage_ids": executed_stage_ids,
                "selected_feedback": {"source": "parse"},
                "exit_reason": "candidate semantic failed before scenario generation",
            }
        ],
        llm_interactions=[
            {"stage_id": "SL-1", "provider": "real-env", "model_id": "gpt-test"},
            {"stage_id": "SL-9", "provider": "real-env", "model_id": "gpt-test"},
        ],
        deterministic_feedback={"iterations": [{"parse": {"ok": True}, "semantic": {"ok": True}}]},
        repair_history=[{"iteration": 0, "accepted": True}],
        scenario_history=[],
        final_artifacts={
            "final_dsl": final_dsl,
            "final_dsl_hash": "sha256:final",
            "verdict": "not_converged",
            "verdict_source_stage_id": "SC-11",
            "verdict_reason": "candidate semantic failed",
            "agent_loop_result_status": "not_converged",
            "oracle_weak": False,
            "main_result_eligible": False,
            "inclusion_reason": None,
            "exclusion_reason": "verdict_not_success",
            "error_message": "candidate semantic failed before scenario generation",
        },
        logs=[{"event": "sc12_verdict", "verdict": "not_converged", "reason": "candidate semantic failed"}],
        replay_index={"iteration_count": 1, "repair_count": 1, "scenario_history_count": 0},
        redaction_report=[{"field_path": "input_bundle.nl", "reason": "test_redacted"}],
    )


def _full_record() -> AgentLoopRunRecord:
    record = _record()
    return replace(
        record,
        stage_graph={
            "planned": FULL_STAGED_REQUIRED_STAGE_IDS,
            "executed": FULL_STAGED_REQUIRED_STAGE_IDS,
        },
        stage_records=[_stage_meta(stage_id, ok=stage_id not in {"SC-12"}) for stage_id in FULL_STAGED_REQUIRED_STAGE_IDS],
        llm_interactions=[
            {"stage_id": "SL-1", "provider": "real-env", "model_id": "gpt-test"},
            {"stage_id": "SL-5", "provider": "real-env", "model_id": "gpt-test"},
            {"stage_id": "SL-9", "provider": "real-env", "model_id": "gpt-test"},
            {"stage_id": "SL-7", "provider": "real-env", "model_id": "gpt-test"},
        ],
        scenario_history=[{"scenario_set_id": "scenario-pr-d-path1", "epoch": 0, "n_scenarios": 1}],
        replay_index={"iteration_count": 1, "repair_count": 1, "scenario_history_count": 1},
    )


def test_pr_d_representative_cases_embed_issue14_nl() -> None:
    cases = representative_cases()

    assert [case.case_key for case in cases] == ["path1_cara", "path2_lng_ems"]
    assert "CARA coordinates the Caregiver Interface" in cases[0].nl
    assert "LNG-ship EMS manages a ship energy system" in cases[1].nl
    assert "issuecomment-4598890685" in cases[0].issue14_comment_url
    assert "issuecomment-4598890799" in cases[1].issue14_comment_url


def test_pr_d_provider_env_check_does_not_read_dotenv(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_ENDPOINT", raising=False)
    monkeypatch.setenv("LLM_API_KEY", "sk-test-secret-123456")
    monkeypatch.setenv("LLM_MODEL", "gpt-test")

    assert missing_provider_env() == ["LLM_ENDPOINT"]
    with pytest.raises(RuntimeError, match="LLM_ENDPOINT"):
        assert_pr_d_provider_env()


def test_pr_d_config_uses_default_real_full_staged_entry(tmp_path: Path) -> None:
    cfg = make_pr_d_config(_case(), tmp_path)

    assert cfg.condition_id == "full_staged_v1"
    assert cfg.llm_provider_mode == "real_env"
    assert cfg.output_dir == str(tmp_path)
    assert cfg.run_id == "pr-d-path1_cara"
    assert cfg.write_run_record is True


def test_pr_d_summary_and_comment_are_secret_safe(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_API_KEY", "sk-prd-secret-000000")
    record = _record()
    path = write_agent_loop_run_record(record, tmp_path / "pr-d-path1_cara.agent_loop.json.gz")
    result = AgentLoopResult(
        final_dsl=record.final_artifacts["final_dsl"],
        status="not_converged",
        error_message="not converged in default budget",
        run_record_id=record.run_id,
        run_record_path=str(path),
    )

    summary = summarize_run(_case(), result, record, path)
    comment = render_issue_comment([summary])
    payload = summaries_to_jsonable([summary])

    assert summary.schema_valid is True
    assert summary.secret_redacted is True
    assert summary.planned_stage_graph_full_staged is True
    assert summary.executed_trace_full_staged is False
    assert {"SL-5", "SD-5A", "SC-5F", "SD-6", "SL-7", "SL-10B"}.issubset(summary.executed_missing_stage_ids)
    assert summary.no_legacy_scenario_unavailable is True
    assert summary.main_result_eligible is False
    assert summary.provider_mode == "real_env"
    assert summary.provider_config_read is True
    assert summary.scenario_set_id is None
    assert summary.scenario_epoch is None
    assert "Path1 CARA representative NL" in comment
    assert "not_converged" in comment
    assert "planned graph" in comment
    assert "executed trace" in comment
    assert "missing_required=`SD-3, SD-4, SL-5" in comment
    assert "scenario generation unavailable because initial DSL parse failed" in comment
    assert "sk-prd-secret" not in comment
    assert payload[0]["case_key"] == "path1_cara"
    assert payload[0]["planned_stage_graph_full_staged"] is True
    assert payload[0]["executed_trace_full_staged"] is False
    assert "stage_graph_full_staged" not in payload[0]


def test_pr_d_full_trace_summary_requires_executed_stage_ids(tmp_path: Path) -> None:
    record = _full_record()
    path = write_agent_loop_run_record(record, tmp_path / "pr-d-path1_cara.agent_loop.json.gz")
    result = AgentLoopResult(
        final_dsl=record.final_artifacts["final_dsl"],
        status="not_converged",
        error_message="not converged in default budget",
        run_record_id=record.run_id,
        run_record_path=str(path),
    )

    summary = summarize_run(_case(), result, record, path)

    assert summary.planned_stage_graph_full_staged is True
    assert summary.executed_trace_full_staged is True
    assert summary.executed_missing_stage_ids == []
    assert summary.scenario_set_id == "scenario-pr-d-path1"
    assert summary.scenario_epoch == 0


def test_pr_d_schema_validation_negative_case() -> None:
    valid = _record()
    invalid = _record()
    invalid.stage_records = [{**invalid.stage_records[0], "ok": "yes"}]

    assert _schema_validation_error(valid) is None
    assert "StageResultMeta.ok must be a bool" in (_schema_validation_error(invalid) or "")


def test_pr_d_runner_uses_injected_entry_and_writes_summary(tmp_path: Path) -> None:
    case = _case()

    def fake_run(nl: str, config) -> AgentLoopResult:
        assert nl == case.nl
        assert config.condition_id == "full_staged_v1"
        record = _record(run_id=config.run_id)
        path = write_agent_loop_run_record(record, Path(config.output_dir) / f"{config.run_id}.agent_loop.json.gz")
        return AgentLoopResult(
            final_dsl=record.final_artifacts["final_dsl"],
            status="not_converged",
            error_message="not converged in default budget",
            run_record_id=record.run_id,
            run_record_path=str(path),
        )

    summaries = run_representative_cases(
        output_dir=tmp_path,
        run_agent_loop_fn=fake_run,
        cases=[case],
        require_provider_env=False,
    )

    assert len(summaries) == 1
    assert summaries[0].run_record_id == "pr-d-path1_cara"
    assert Path(summaries[0].run_record_path).exists()
