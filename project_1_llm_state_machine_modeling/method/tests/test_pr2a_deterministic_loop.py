from __future__ import annotations

import gzip
import json
from pathlib import Path

from method.pr2a_loop import DeterministicLoopConfig, run_pr2a_deterministic_loop
from method.run_record import is_path_result_eligible, read_agent_loop_run_record
from method.schema import AgentLoopRunRecord, GroundedElement, GroundingMap, TestScenario
from method.stages.ids import StageId


DEADLOCK_DSL = """
state Root {
    state Idle;
    state Active;
    state Done;
    [*] -> Idle;
    Idle -> Active;
    Idle -> Done;
    Done -> Idle;
    Done -> [*];
}
"""


FIXED_DSL = """
state Root {
    state Idle;
    state Active;
    state Done;
    [*] -> Idle;
    Idle -> Active;
    Active -> Idle;
    Idle -> Done;
    Done -> Idle;
    Done -> [*];
}
"""


INFO_ONLY_DSL = """
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active;
    Active -> Idle;
}
"""


DRIFT_CANDIDATE_DSL = """
state Root {
    state Idle;
    [*] -> Idle;
    Idle -> [*];
}
"""


def _empty_scenarios() -> list[TestScenario]:
    return [TestScenario(name="hot_start_smoke", steps=[])]


def _grounding() -> GroundingMap:
    return GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Root.Active",
                element_kind="state",
                element_ref="Root.Active",
                source_stage="SL-1",
                evidence_text="The Active state is required by the NL requirement.",
                requiredness="required",
            )
        ],
        source_summary={"nl": "Active is required."},
    )


def _load_raw_gzip_json(path: str | Path) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        return json.load(f)


def test_pr2a_loop_repairs_design_warning_and_writes_single_file_run_record(tmp_path: Path) -> None:
    result = run_pr2a_deterministic_loop(
        "The controller starts Idle, can become Active, and must continue operating.",
        DeterministicLoopConfig(
            initial_dsl=DEADLOCK_DSL,
            scenarios=_empty_scenarios(),
            repair_candidates=[FIXED_DSL],
            grounding_map=_grounding(),
            run_id="pr2a-design-repair",
            output_dir=tmp_path,
            max_iterations=3,
        ),
    )

    assert result.status == "converged"
    assert result.final_dsl == FIXED_DSL
    assert result.run_record_path is not None
    assert result.run_record_path.endswith("pr2a-design-repair.agent_loop.json.gz")

    record = read_agent_loop_run_record(result.run_record_path)
    assert isinstance(record, AgentLoopRunRecord)
    assert record.status == "success"
    assert is_path_result_eligible(record)
    assert record.final_artifacts["main_result_eligible"] is True
    assert record.final_artifacts["final_dsl"] == FIXED_DSL
    assert record.llm_interactions[0]["provider"] == "fake"
    assert record.llm_interactions[0]["stage_id"] == StageId.SL_9_REPAIR.value

    stage_ids = [row["stage_id"] for row in record.stage_records]
    assert stage_ids[:8] == [
        StageId.SC_0_START.value,
        StageId.SD_2_PARSE.value,
        StageId.SD_3_SEMANTIC.value,
        StageId.SD_4_DESIGN.value,
        StageId.SL_5_SCENARIO_GENERATION.value,
        StageId.SD_5A_SCENARIO_COVERAGE.value,
        StageId.SC_5F_SCENARIO_FREEZE.value,
        StageId.SD_6_SIM.value,
    ]
    assert StageId.SD_8_FIX_PLAN.value in stage_ids
    assert StageId.SL_9_REPAIR.value in stage_ids
    assert StageId.SD_10_REPAIR_REVIEW.value in stage_ids
    assert StageId.SC_11_ACCEPT_CANDIDATE.value in stage_ids
    assert stage_ids[-2:] == [StageId.SC_12_EXIT.value, StageId.SC_13_TRACE_AUDIT.value]

    assert record.iteration_records[0]["selected_feedback"]["source"] == "design"
    assert record.iteration_records[0]["repair_review"]["ok"] is True
    assert record.repair_history[0]["fix_plan"]["target"] == "design"
    assert record.scenario_history[0]["epoch"] == 0
    assert _load_raw_gzip_json(result.run_record_path)["run_id"] == "pr2a-design-repair"


def test_pr2a_loop_does_not_repair_info_only_design_diagnostics(tmp_path: Path) -> None:
    result = run_pr2a_deterministic_loop(
        "The controller may move between Idle and Active without external events.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            repair_candidates=["state Root { state ShouldNotAppear; }"],
            run_id="pr2a-info-only",
            output_dir=tmp_path,
            max_iterations=2,
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = [row["stage_id"] for row in record.stage_records]

    assert result.status == "converged"
    assert result.final_dsl == INFO_ONLY_DSL
    assert record.status == "success"
    assert StageId.SD_8_FIX_PLAN.value not in stage_ids
    assert StageId.SL_9_REPAIR.value not in stage_ids
    assert StageId.SD_10_REPAIR_REVIEW.value not in stage_ids
    assert record.iteration_records[0]["selected_feedback"] is None
    assert record.deterministic_feedback["iterations"][0]["design"]["info_items"]


def test_pr2a_repair_review_rejects_drift_and_keeps_old_dsl(tmp_path: Path) -> None:
    result = run_pr2a_deterministic_loop(
        "The Active state is required and must not be deleted.",
        DeterministicLoopConfig(
            initial_dsl=DEADLOCK_DSL,
            scenarios=_empty_scenarios(),
            repair_candidates=[DRIFT_CANDIDATE_DSL],
            grounding_map=_grounding(),
            run_id="pr2a-reject-drift",
            output_dir=tmp_path,
            max_iterations=2,
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")

    assert result.status == "not_converged"
    assert result.final_dsl == DEADLOCK_DSL
    assert record.status == "rejected"
    assert not is_path_result_eligible(record)
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.final_artifacts["final_dsl"] == DEADLOCK_DSL
    assert record.iteration_records[0]["repair_review"]["ok"] is False
    assert "missing_required_grounding" in record.repair_history[0]["repair_review"]["local_rejection"]["reason"]


def test_pr2a_invalid_run_record_status_is_allowed_but_filtered_from_path_results() -> None:
    record = AgentLoopRunRecord(
        schema_version="pr2a.agent-loop-run-record.v1",
        run_id="invalid-run",
        created_at="2026-06-02T00:00:00Z",
        status="invalid",
        input_bundle={},
        run_config={},
        environment={},
        stage_graph={},
        stage_records=[],
        iteration_records=[],
        final_artifacts={"main_result_eligible": False},
    )

    assert not is_path_result_eligible(record)


def test_pr2a_loop_writes_failed_parse_run_record_without_scenario_epoch_crash(tmp_path: Path) -> None:
    result = run_pr2a_deterministic_loop(
        "Broken DSL should still produce an audit record.",
        DeterministicLoopConfig(
            initial_dsl="state Root {",
            scenarios=_empty_scenarios(),
            run_id="pr2a-parse-fail",
            output_dir=tmp_path,
            max_iterations=1,
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")

    assert result.status == "not_converged"
    assert record.status == "failed"
    assert not is_path_result_eligible(record)
    assert record.iteration_records[0]["scenario_epoch"] is None
    assert record.final_artifacts["main_result_eligible"] is False


def test_pr2a_reader_rejects_schema_invalid_raw_run_record(tmp_path: Path) -> None:
    path = tmp_path / "bad.agent_loop.json.gz"
    payload = {
        "schema_version": "pr2a.agent-loop-run-record.v1",
        "run_id": "bad",
        "created_at": "2026-06-02T00:00:00Z",
        "status": "success",
        "input_bundle": {},
        "run_config": {},
        "environment": {},
        "stage_graph": {},
        "stage_records": [
            {
                "stage_id": "SD-404",
                "stage_kind": "deterministic",
                "enabled": True,
                "ran": True,
                "status": "ok",
                "ok": True,
            }
        ],
        "iteration_records": [],
    }
    with gzip.open(path, "wt", encoding="utf-8") as f:
        json.dump(payload, f)

    import pytest

    with pytest.raises(ValueError, match="stage_records invalid"):
        read_agent_loop_run_record(path)
