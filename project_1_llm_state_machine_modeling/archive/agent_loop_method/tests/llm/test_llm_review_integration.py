from __future__ import annotations

import json
from pathlib import Path

from archive.agent_loop_method.experiments.ablation.deterministic_loop import DeterministicLoopConfig, ReviewPolicy, run_deterministic_ablation_loop
from archive.agent_loop_method.run_record import is_path_result_eligible, read_agent_loop_run_record
from archive.agent_loop_method.schema import GroundedElement, GroundingMap, TestScenario
from archive.agent_loop_method.stages.ids import StageId


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


def _sl7_raw(decision: str = "pass") -> str:
    finding = {
        "category": "nl_fidelity",
        "severity": "major",
        "summary": "NL says Active must remain explicitly reachable.",
        "evidence": ["Active state requirement"],
    }
    return json.dumps(
        {
            "decision": decision,
            "risk_level": "major" if decision == "fail" else "none",
            "findings": [finding] if decision == "fail" else [],
            "blocking_findings": [finding] if decision == "fail" else [],
        },
        ensure_ascii=False,
    )


def _sl10b_raw(decision: str = "accept") -> str:
    return json.dumps(
        {
            "decision": decision,
            "drift_risk": "major" if decision != "accept" else "none",
            "drift_evidence": [{"summary": "candidate may remove an NL-grounded behavior"}] if decision != "accept" else [],
            "required_revision": ["preserve NL-grounded behavior"] if decision != "accept" else [],
        },
        ensure_ascii=False,
    )


def _interaction(record, stage_id: StageId | str, index: int = 0) -> dict:
    matches = [item for item in record.llm_interactions if item["stage_id"] == (stage_id.value if isinstance(stage_id, StageId) else stage_id)]
    assert len(matches) > index
    return matches[index]


def test_pr2b_sl7_audit_only_records_review_without_changing_main_result(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "The controller may move between Idle and Active without external events.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            grounding_map=_grounding(),
            run_id="pr2b-sl7-audit-only",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(enable_model_review=True, model_review_mode="audit_only"),
            review_replay_responses={"SL-7:0": _sl7_raw("fail")},
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = [row["stage_id"] for row in record.stage_records]
    sl7 = _interaction(record, StageId.SL_7_MODEL_REVIEW)

    assert result.status == "converged"
    assert record.status == "success"
    assert is_path_result_eligible(record)
    assert record.final_artifacts["final_dsl"] == INFO_ONLY_DSL
    assert StageId.SL_7_MODEL_REVIEW.value in stage_ids
    assert StageId.SD_8_FIX_PLAN.value not in stage_ids
    assert sl7["provider"] == "fake-replay"
    assert sl7["prompt_messages"]
    assert sl7["raw_output"] == _sl7_raw("fail")
    assert sl7["parsed_output"]["decision"] == "fail"
    assert sl7["review_meta"]["schema_validation_ok"] is True
    assert sl7["review_meta"]["failure_policy"] == "audit_only"
    assert record.deterministic_feedback["iterations"][0]["model_review"]["decision"] == "fail"
    assert record.redaction_report == []


def test_pr2b_blocking_sl7_failure_enters_model_review_fix_plan(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "The reviewer should be allowed to request a holistic model-review repair.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            grounding_map=_grounding(),
            repair_candidates=[INFO_ONLY_DSL],
            run_id="pr2b-sl7-blocking-fix-plan",
            output_dir=tmp_path,
            max_iterations=2,
            review_policy=ReviewPolicy(enable_model_review=True, model_review_mode="blocking"),
            review_replay_responses={"SL-7:0": _sl7_raw("fail"), "SL-7:1": _sl7_raw("pass")},
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = [row["stage_id"] for row in record.stage_records]

    assert result.status == "converged"
    assert record.status == "success"
    assert is_path_result_eligible(record)
    assert StageId.SD_8_FIX_PLAN.value in stage_ids
    assert StageId.SL_9_REPAIR.value in stage_ids
    assert record.iteration_records[0]["selected_feedback"] == {
        "source": "model_review",
        "source_stage": StageId.SL_7_MODEL_REVIEW.value,
    }
    assert record.repair_history[0]["fix_plan"]["target"] == "model_review"
    assert record.repair_history[0]["fix_plan"]["severity"] == "review_fail"
    assert _interaction(record, StageId.SL_7_MODEL_REVIEW, 1)["parsed_output"]["decision"] == "pass"


def test_pr2b_sl7_replay_miss_marks_record_invalid_and_filters_path_result(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "Replay miss must not silently enter Path1/Path2 main results.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            run_id="pr2b-sl7-replay-miss",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(
                enable_model_review=True,
                model_review_mode="blocking",
                failure_policy="fail_closed",
                require_replay=True,
            ),
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    sl7 = _interaction(record, StageId.SL_7_MODEL_REVIEW)

    assert record.status == "invalid"
    assert not is_path_result_eligible(record)
    assert record.final_artifacts["main_result_eligible"] is False
    assert sl7["schema_validation_ok"] is False
    assert sl7["review_meta"]["schema_validation_error"] == "replay miss"
    assert any(log["event"] == "llm_review_replay_miss" for log in record.logs)



def test_pr2b_invalid_sl7_output_marks_record_invalid(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "Invalid review JSON must be visible and excluded from main results.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            run_id="pr2b-sl7-invalid-output",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(enable_model_review=True),
            review_replay_responses={"SL-7:0": "not-json"},
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    sl7 = _interaction(record, StageId.SL_7_MODEL_REVIEW)

    assert record.status == "invalid"
    assert not is_path_result_eligible(record)
    assert sl7["schema_validation_ok"] is False
    assert sl7["parsed_output"]["decision"] == "invalid_output"
    assert "response is not valid JSON" in sl7["review_meta"]["schema_validation_error"]

def test_pr2b_sl7_provider_failure_marks_record_invalid(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "Provider failure must be auditable and excluded from main results.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            run_id="pr2b-sl7-provider-failure",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(enable_model_review=True, failure_policy="fail_closed"),
            review_provider_failures=[StageId.SL_7_MODEL_REVIEW.value],
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")

    assert record.status == "invalid"
    assert not is_path_result_eligible(record)
    assert _interaction(record, StageId.SL_7_MODEL_REVIEW)["review_meta"]["schema_validation_error"] == "provider failure"
    assert any(log["event"] == "llm_review_provider_failure" for log in record.logs)



def test_pr2b_run_record_redacts_secrets_and_reports_paths(tmp_path: Path) -> None:
    secret_nl = "Requirement accidentally contains sk-test-1234567890abcdef and gho_deadbeef12345678."
    raw_with_secret = json.dumps(
        {
            "decision": "pass",
            "risk_level": "none",
            "findings": [{"category": "nl_fidelity", "severity": "info", "summary": "saw github_pat_deadbeef12345678", "evidence": []}],
            "blocking_findings": [],
        },
        ensure_ascii=False,
    )

    result = run_deterministic_ablation_loop(
        secret_nl,
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            run_id="pr2b-redaction",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(enable_model_review=True),
            review_replay_responses={"SL-7:0": raw_with_secret},
            path_context={"api_key": "sk-context-1234567890abcdef"},
        ),
    )

    raw_record = Path(result.run_record_path or "").read_bytes()
    # gzip bytes can contain compressed substrings only by chance, so inspect decoded record too.
    record = read_agent_loop_run_record(result.run_record_path or "")
    record_json = json.dumps(record.__dict__, ensure_ascii=False, default=str)

    assert b"sk-test-1234567890abcdef" not in raw_record
    assert "sk-test-1234567890abcdef" not in record_json
    assert "gho_deadbeef12345678" not in record_json
    assert "github_pat_deadbeef12345678" not in record_json
    assert "sk-context-1234567890abcdef" not in record_json
    assert record.redaction_report
    assert {item["reason"] for item in record.redaction_report} >= {"openai_api_key", "github_oauth_token", "github_pat", "secret_field"}
    assert any(item["field_path"].startswith("llm_interactions") for item in record.redaction_report)
    assert any(item["field_path"] == "input_bundle.path_context.api_key" for item in record.redaction_report)
    assert "<redacted:" in record.input_bundle["nl"]
    assert "<redacted:" in record.llm_interactions[0]["raw_output"]


def test_pr2b_invalid_review_secret_is_redacted_from_logs_and_stage_meta(tmp_path: Path) -> None:
    secret = "sk-invalid-1234567890abcdef"
    result = run_deterministic_ablation_loop(
        "Invalid output with secret must still redact every record surface.",
        DeterministicLoopConfig(
            initial_dsl=INFO_ONLY_DSL,
            scenarios=_empty_scenarios(),
            run_id="pr2b-redact-invalid-output",
            output_dir=tmp_path,
            max_iterations=1,
            review_policy=ReviewPolicy(enable_model_review=True),
            review_replay_responses={"SL-7:0": f"not-json {secret}"},
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    record_json = json.dumps(record.__dict__, ensure_ascii=False, default=str)

    assert record.status == "invalid"
    assert secret not in record_json
    assert record.redaction_report
    assert any(item["field_path"].startswith("logs") for item in record.redaction_report)
    assert any(item["field_path"].startswith("stage_records") for item in record.redaction_report)
    assert any(item["field_path"].startswith("llm_interactions") for item in record.redaction_report)

def test_pr2b_sl10b_delta_review_can_reject_sd10_accepted_candidate(tmp_path: Path) -> None:
    result = run_deterministic_ablation_loop(
        "The Active state is required and delta review may reject semantic drift.",
        DeterministicLoopConfig(
            initial_dsl=DEADLOCK_DSL,
            scenarios=_empty_scenarios(),
            repair_candidates=[FIXED_DSL],
            grounding_map=_grounding(),
            run_id="pr2b-sl10b-delta-reject",
            output_dir=tmp_path,
            max_iterations=2,
            review_policy=ReviewPolicy(enable_delta_review=True, delta_review_mode="blocking"),
            review_replay_responses={"SL-10B:0": _sl10b_raw("reject")},
        ),
    )

    record = read_agent_loop_run_record(result.run_record_path or "")
    sl10b = _interaction(record, StageId.SL_10B_DELTA_REVIEW)
    repair_review = record.repair_history[0]["repair_review"]

    assert result.status == "not_converged"
    assert record.status == "rejected"
    assert not is_path_result_eligible(record)
    assert record.final_artifacts["final_dsl"] == DEADLOCK_DSL
    assert sl10b["parsed_output"]["decision"] == "reject"
    assert sl10b["review_meta"]["schema_validation_ok"] is True
    assert repair_review["ok"] is False
    assert repair_review["delta_review"]["decision"] == "reject"
    assert repair_review["local_rejection"]["rejected_by_stage"] == StageId.SL_10B_DELTA_REVIEW.value
