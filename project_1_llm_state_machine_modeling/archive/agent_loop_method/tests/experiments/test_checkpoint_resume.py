from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

import pytest

from archive.agent_loop_method.run_record import read_agent_loop_run_record
from archive.agent_loop_method.schema import (
    DesignDiagnosticItem,
    DesignFeedback,
    LoopConfig,
    ModelReviewFeedback,
    ParseFeedback,
    RepairReviewFeedback,
    SemanticFeedback,
    SimFeedback,
    StageContext,
    StageResultMeta,
    TestScenario,
)
from archive.agent_loop_method.staged_runtime import FullStagedRuntimeAdapters, RepairRequest, ScenarioGenerationRequest
from archive.agent_loop_method.stages.ids import STAGE_SPECS_BY_ID, StageId, StageStatus


def _meta(stage_id: StageId, *, ok: bool = True, status: StageStatus | None = None) -> StageResultMeta:
    spec = STAGE_SPECS_BY_ID[stage_id.value]
    return StageResultMeta(
        stage_id=stage_id.value,
        stage_kind=spec.kind,
        enabled=True,
        ran=True,
        status=status or (StageStatus.OK if ok else StageStatus.FAIL),
        ok=ok,
    )


def _stable_dsl() -> str:
    return """
state Root {
    state Idle;
    [*] -> Idle;
    Idle -> [*];
}
"""


def _ok_parse(_dsl: str, _context: StageContext) -> tuple[ParseFeedback, StageResultMeta]:
    return ParseFeedback(ok=True), _meta(StageId.SD_2_PARSE)


def _ok_semantic(_dsl: str, _context: StageContext) -> tuple[SemanticFeedback, StageResultMeta]:
    return SemanticFeedback(ok=True), _meta(StageId.SD_3_SEMANTIC)


def _blocking_design_once() -> Callable[[StageContext], tuple[DesignFeedback, StageResultMeta]]:
    calls = {"count": 0}

    def design(_context: StageContext) -> tuple[DesignFeedback, StageResultMeta]:
        calls["count"] += 1
        if calls["count"] == 1:
            return (
                DesignFeedback(
                    ok=False,
                    blocking_items=[
                        DesignDiagnosticItem(
                            code="LG_F1_FIXABLE_DESIGN_BLOCKER",
                            pyfcstm_severity="error",
                            policy_action="budgeted_repair",
                            instance_key="lg-f1:design-once",
                            rationale="force one repair path so the checkpoint contains repair ledgers",
                        )
                    ],
                ),
                _meta(StageId.SD_4_DESIGN, ok=False),
            )
        return DesignFeedback(ok=True), _meta(StageId.SD_4_DESIGN)

    return design


def _scenario_generate(_request: ScenarioGenerationRequest) -> list[TestScenario]:
    return [TestScenario(name="empty_smoke", steps=[])]


def _ok_coverage(_dsl: str, scenarios: list[TestScenario]) -> tuple[dict[str, Any], StageResultMeta]:
    return {"coverage_report": {"ok": True, "n_scenarios": len(scenarios)}, "coverage_gap": False}, _meta(
        StageId.SD_5A_SCENARIO_COVERAGE
    )


def _ok_sim(_dsl: str, scenarios_or_set: Any, _context: StageContext) -> tuple[SimFeedback, StageResultMeta]:
    n = len(getattr(scenarios_or_set, "scenarios", []) or [])
    return SimFeedback(ok=True, n_scenarios=n, n_scenarios_passed=n), _meta(StageId.SD_6_SIM)


def _ok_model_review(_dsl: str, _context: StageContext, _feedback: dict[str, Any]) -> tuple[ModelReviewFeedback, StageResultMeta]:
    return ModelReviewFeedback(ok=True, decision="pass", risk_level="none"), _meta(StageId.SL_7_MODEL_REVIEW)


def _ok_repair_review(_request: RepairRequest) -> tuple[RepairReviewFeedback, StageResultMeta]:
    return RepairReviewFeedback(ok=True, target_resolved=True, drift_risk="none"), _meta(StageId.SD_10_REPAIR_REVIEW)


def _repair_path_adapters() -> FullStagedRuntimeAdapters:
    return FullStagedRuntimeAdapters(
        parse=_ok_parse,
        semantic=_ok_semantic,
        design=_blocking_design_once(),
        scenario_generate=_scenario_generate,
        scenario_coverage=_ok_coverage,
        sim=_ok_sim,
        model_review=_ok_model_review,
        repair=lambda _request: _stable_dsl(),
        repair_review=_ok_repair_review,
    )


def _lg_f1_config(tmp_path: Path, *, run_id: str, condition_id: str | None = None) -> LoopConfig:
    return LoopConfig(
        condition_id=condition_id or run_id,
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock", "checkpoint_backend=sqlite", "resume_experiment=lg_f1"],
        llm_provider_mode="mock",
        academic_question="test-only LG-F1 durable checkpoint/resume contract; excluded from main results",
        output_dir=str(tmp_path / "records"),
        run_id=run_id,
        max_iterations=2,
        compatibility_mode="langgraph_stategraph",
    )


def _require_lg_f1_api() -> tuple[Callable[..., dict[str, Any]], Callable[..., dict[str, Any]]]:
    import archive.agent_loop_method.langgraph_runtime as lg

    run_experiment = getattr(lg, "run_lg_f1_resume_experiment", None)
    resume_from_checkpoint = getattr(lg, "resume_lg_f1_from_checkpoint", None)
    assert callable(run_experiment), "LG-F1 must expose run_lg_f1_resume_experiment(...)"
    assert callable(resume_from_checkpoint), "LG-F1 must expose resume_lg_f1_from_checkpoint(...)"
    return run_experiment, resume_from_checkpoint


def _create_interrupted_resume_report(
    tmp_path: Path,
    *,
    run_id: str = "lg-f1-resume-contract",
    include_uninterrupted_baseline: bool = True,
) -> dict[str, Any]:
    run_experiment, _resume_from_checkpoint = _require_lg_f1_api()
    return run_experiment(
        "The controller starts in Idle and should survive one durable resume.",
        config=_lg_f1_config(tmp_path, run_id=run_id),
        adapters=_repair_path_adapters(),
        uninterrupted_adapters=_repair_path_adapters() if include_uninterrupted_baseline else None,
        initial_dsl=_stable_dsl(),
        checkpoint_path=str(tmp_path / "checkpoints" / f"{run_id}.sqlite"),
        interrupt_after="repair_sl10_review",
    )


def test_lg_f1_durable_sqlite_resume_report_has_schema_and_append_only_evidence(tmp_path: Path) -> None:
    report = _create_interrupted_resume_report(tmp_path)

    assert report["schema_version"] == "lg-f1.resume-reconciliation.v1"
    assert report["checkpoint_backend"] == "sqlite"
    assert report["checkpoint_backend_type"] == "SqliteSaver"
    assert Path(report["checkpoint_path"]).exists()
    assert str(report["checkpoint_path_hash"]).startswith("sha256:")
    assert report["thread_id"] == "lg-f1-resume-contract"
    assert report["interrupt"]["requested_after"] == "repair_sl10_review"
    assert report["interrupt"]["checkpoint_id_hash"].startswith("sha256:")
    assert report["resume"]["resumed_from_checkpoint"] is True
    assert report["resume"]["checkpoint_id_hash"] == report["interrupt"]["checkpoint_id_hash"]
    assert report["graph_config_hash"].startswith("sha256:")
    assert report["real_agent_loop_resume_support_level"] == "controlled_parent_node_boundary_only"
    assert report["real_agent_loop_arbitrary_mid_node_resume_supported"] is False
    assert report["real_agent_loop_nested_subgraph_resume_supported"] is False
    assert report["mid_node_crash_supported"] is False
    assert report["transient_store_durable"] is False
    assert report["uninterrupted_baseline_available"] is True
    assert report["baseline_comparison_method"] == "independent_uninterrupted_baseline"
    assert report["baseline_comparison_verdict"] == "consistent"
    assert report["verdict_scope"] == "append_only_stage_replay_and_independent_baseline_comparison"
    assert report["uninterrupted_run_id"] == "lg-f1-resume-contract-uninterrupted"
    assert report["uninterrupted_run_record_path"]
    assert str(report["uninterrupted_artifact_hash"]).startswith("sha256:")
    assert report["artifact_hash_scope"] == "academic_evidence_snapshot"
    assert report["append_only_audit"]["stage_records_prefix_preserved"] is True
    assert report["append_only_audit"]["fix_log_prefix_preserved"] is True
    assert report["append_only_audit"]["llm_interactions_prefix_preserved"] is True
    assert report["append_only_audit"]["scenario_history_prefix_preserved"] is True
    assert report["append_only_audit"]["repair_history_prefix_preserved"] is True
    assert report["append_only_audit"]["duplicate_fix_log_entry_detected"] is False
    assert report["stage_replay_audit"]["post_repair_full_revalidation_expected"] is True
    assert report["stage_replay_audit"]["unexpected_stage_replay_detected"] is False
    assert report["stage_replay_audit"]["suffix_after_resume"][:3] == ["SD-2", "SD-3", "SD-4"]
    assert all(item["verdict"] == "consistent" for item in report["comparison_checks"])
    assert all(item["baseline_available"] is True for item in report["comparison_checks"])
    assert all(item["uninterrupted_baseline_available"] is True for item in report["comparison_checks"])
    assert all(item["comparison_basis"] == "independent_uninterrupted_baseline" for item in report["comparison_checks"])
    assert all(item["comparison_target"] == "uninterrupted_vs_resumed" for item in report["comparison_checks"])
    assert all(str(item["uninterrupted_value_hash"]).startswith("sha256:") for item in report["comparison_checks"])
    assert report["run_record_path"]

    record = read_agent_loop_run_record(report["run_record_path"])
    assert record.environment["checkpoint_backend"] == "sqlite"
    assert record.environment["resumed_from_checkpoint"] is True
    assert record.environment["resume_checkpoint_id_hash"] == report["resume"]["checkpoint_id_hash"]
    assert record.environment["real_agent_loop_resume_support_level"] == "controlled_parent_node_boundary_only"
    assert record.environment["real_agent_loop_arbitrary_mid_node_resume_supported"] is False
    assert record.environment["real_agent_loop_nested_subgraph_resume_supported"] is False
    assert record.environment["baseline_comparison_method"] == "independent_uninterrupted_baseline"
    assert record.environment["baseline_comparison_verdict"] == "consistent"
    assert record.environment["verdict_scope"] == "append_only_stage_replay_and_independent_baseline_comparison"
    assert record.environment["resume_cli_entrypoint"] == "python -m project_1_llm_state_machine_modeling.archive.agent_loop_method.experiments.checkpoint_resume"
    assert record.environment["resume_cli_pythonpath_entrypoint"] == "PYTHONPATH=project_1_llm_state_machine_modeling python -m archive.agent_loop_method.experiments.checkpoint_resume"
    assert record.environment["resume_cli_legacy_entrypoint"] == "PYTHONPATH=project_1_llm_state_machine_modeling python -m archive.agent_loop_method.pr_lg_f1_resume_experiment"
    assert record.environment["resume_cli_legacy_package_entrypoint"] == "python -m project_1_llm_state_machine_modeling.archive.agent_loop_method.pr_lg_f1_resume_experiment"
    assert record.environment["resume_cli_workdir"] == "repo_root"
    assert record.environment["resume_cli_requires_pythonpath"] is False
    assert "post-repair validation" in record.environment["lg_f1_stage_replay_explanation"]
    assert record.run_config["graph_config_hash"] == report["graph_config_hash"]
    assert record.run_config["baseline_comparison_method"] == "independent_uninterrupted_baseline"
    assert record.final_artifacts["lg_f1_baseline_comparison_verdict"] == "consistent"
    lg_e2_readiness = record.final_artifacts["lg_c1_graph_state_readiness"]["final_reducer_channel_summaries"][
        "lg_e2_send_parallel_events"
    ]
    lg_e2_trace = record.final_artifacts["lg_e2_send_parallel_trace"]
    assert record.environment["lg_e2_send_parallel_enabled"] is True
    assert record.environment["lg_e2_send_parallel_event_count"] == lg_e2_readiness["count"]
    assert record.environment["lg_e2_send_parallel_events_hash"] == lg_e2_trace["events_hash"]
    assert record.run_config["lg_e2_send_parallel_enabled"] is True
    assert record.run_config["lg_e2_send_parallel_contract"]
    assert lg_e2_trace["schema_version"] == "lg-e2.send-parallel-sd6.v1"
    assert lg_e2_trace["event_count"] == lg_e2_readiness["count"]
    assert lg_e2_trace["does_not_replace_academic_evidence"] is True


def test_lg_f1_without_uninterrupted_baseline_marks_comparison_not_applicable(tmp_path: Path) -> None:
    report = _create_interrupted_resume_report(
        tmp_path,
        run_id="lg-f1-no-baseline",
        include_uninterrupted_baseline=False,
    )

    assert report["verdict"] == "consistent"
    assert report["verdict_scope"] == "append_only_stage_replay_only_no_independent_baseline"
    assert report["uninterrupted_baseline_available"] is False
    assert report["baseline_comparison_method"] == "not_available"
    assert report["baseline_comparison_verdict"] == "not_applicable"
    assert "No independent uninterrupted baseline" in report["baseline_comparison_note"]
    assert report["uninterrupted_run_id"] is None
    assert report["uninterrupted_run_record_path"] is None
    assert report["uninterrupted_artifact_hash"] is None
    assert str(report["resumed_artifact_hash"]).startswith("sha256:")
    assert report["artifact_hash_scope"] == "academic_evidence_snapshot"
    assert not any(str(item).startswith("comparison:") for item in report["unacceptable_diff_findings"])
    assert all(item["verdict"] == "not_applicable" for item in report["comparison_checks"])
    assert all(item["baseline_available"] is False for item in report["comparison_checks"])
    assert all(item["uninterrupted_baseline_available"] is False for item in report["comparison_checks"])
    assert all(item["comparison_basis"] == "no_independent_baseline" for item in report["comparison_checks"])
    assert all(item["comparison_method"] == "not_available" for item in report["comparison_checks"])
    assert all(item["comparison_target"] == "baseline_unavailable" for item in report["comparison_checks"])
    assert all(item["uninterrupted_value_hash"] is None for item in report["comparison_checks"])

    record = read_agent_loop_run_record(report["run_record_path"])
    assert record.environment["baseline_comparison_method"] == "not_available"
    assert record.environment["baseline_comparison_verdict"] == "not_applicable"
    assert record.environment["verdict_scope"] == "append_only_stage_replay_only_no_independent_baseline"
    assert record.final_artifacts["lg_f1_baseline_comparison_method"] == "not_available"
    assert record.final_artifacts["lg_f1_baseline_comparison_verdict"] == "not_applicable"


def test_lg_f1_resume_fails_loud_when_thread_id_does_not_match_checkpoint(tmp_path: Path) -> None:
    report = _create_interrupted_resume_report(tmp_path, run_id="lg-f1-wrong-thread")
    _run_experiment, resume_from_checkpoint = _require_lg_f1_api()

    with pytest.raises((RuntimeError, ValueError), match="thread_id|checkpoint"):
        resume_from_checkpoint(
            checkpoint_path=report["checkpoint_path"],
            thread_id="lg-f1-wrong-thread-OTHER",
            expected_graph_config_hash=report["graph_config_hash"],
            config=_lg_f1_config(tmp_path, run_id="lg-f1-wrong-thread"),
            adapters=_repair_path_adapters(),
        )


def test_lg_f1_resume_fails_loud_when_checkpoint_file_is_missing(tmp_path: Path) -> None:
    _run_experiment, resume_from_checkpoint = _require_lg_f1_api()

    with pytest.raises((FileNotFoundError, RuntimeError, ValueError), match="checkpoint|missing|not found"):
        resume_from_checkpoint(
            checkpoint_path=str(tmp_path / "missing.sqlite"),
            thread_id="lg-f1-missing-checkpoint",
            expected_graph_config_hash="sha256:" + "0" * 64,
            config=_lg_f1_config(tmp_path, run_id="lg-f1-missing-checkpoint"),
            adapters=_repair_path_adapters(),
        )


def test_lg_f1_resume_fails_loud_when_graph_config_hash_mismatches(tmp_path: Path) -> None:
    report = _create_interrupted_resume_report(tmp_path, run_id="lg-f1-config-mismatch")
    _run_experiment, resume_from_checkpoint = _require_lg_f1_api()

    with pytest.raises((RuntimeError, ValueError), match="graph_config_hash|config hash"):
        resume_from_checkpoint(
            checkpoint_path=report["checkpoint_path"],
            thread_id="lg-f1-config-mismatch",
            expected_graph_config_hash="sha256:" + "f" * 64,
            config=_lg_f1_config(tmp_path, run_id="lg-f1-config-mismatch"),
            adapters=_repair_path_adapters(),
        )


def test_lg_f1_resumed_runs_are_not_main_result_eligible(tmp_path: Path) -> None:
    report = _create_interrupted_resume_report(tmp_path, run_id="lg-f1-main-result-ineligible")

    assert report["main_result_eligible"] is False
    record = read_agent_loop_run_record(report["run_record_path"])
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.final_artifacts["main_result_eligibility_reason"]
    assert "resume" in str(record.final_artifacts["main_result_eligibility_reason"]).lower()


def test_lg_f1_resume_experiment_cli_writes_machine_readable_artifacts(tmp_path: Path) -> None:
    from archive.agent_loop_method.experiments.checkpoint_resume import main

    out_dir = tmp_path / "cli"
    rc = main(
        [
            "--mode",
            "mock",
            "--case",
            "ABS",
            "--output-dir",
            str(out_dir),
            "--run-id",
            "lg-f1-cli-smoke",
            "--interrupt-after",
            "repair_sl10_review",
        ]
    )

    assert rc == 0
    summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["schema_version"] == "lg-f1.resume-reconciliation.v1"
    assert summary["verdict"] == "consistent"
    assert summary["resume_run_main_result_eligible"] is False
    assert Path(summary["resume_diff_report_path"]).exists()
    assert (out_dir / "SUMMARY.md").exists()
    assert (out_dir / "pr_comment.md").exists()


def test_lg_f1_resume_experiment_repo_root_module_entrypoints_are_reproducible() -> None:
    repo_root = Path(__file__).resolve().parents[5]
    import os

    env = dict(os.environ)
    env.pop("PYTHONPATH", None)

    for module_name in (
        "project_1_llm_state_machine_modeling.archive.agent_loop_method.experiments.checkpoint_resume",
        "project_1_llm_state_machine_modeling.archive.agent_loop_method.pr_lg_f1_resume_experiment",
    ):
        completed = subprocess.run(
            [sys.executable, "-m", module_name, "--help"],
            cwd=repo_root,
            env=env,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        assert completed.returncode == 0, completed.stderr
        assert "Run LG-F1 durable checkpoint/resume experiment." in completed.stdout
