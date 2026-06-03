from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

import method.llm_stages as llm_stages
import method.loop as loop
import method.schema as schema
from method.llm_stages import MockLLMProvider
from method.run_record import is_path_result_eligible, read_agent_loop_run_record
from method.stages.ids import StageId


def _good_dsl() -> str:
    return """
state Root {
    state Idle;
    state Active;
    [*] -> Idle;
    Idle -> Active;
    Active -> [*];
}
"""


def _sl1_ok_raw() -> str:
    return json.dumps(
        {
            "candidate_dsl": _good_dsl(),
            "grounding_seeds": [
                {
                    "element_id": "state:Root.Idle",
                    "element_kind": "state",
                    "element_ref": "Root.Idle",
                    "source_stage": "SL-1",
                    "evidence_text": "The controller starts in Idle.",
                    "requiredness": "required",
                    "confidence": 1.0,
                }
            ],
            "assumptions": [],
        },
        ensure_ascii=False,
    )


def _sl5_ok_raw() -> str:
    return json.dumps(
        {
            "scenarios": [
                {
                    "name": "start_reaches_active",
                    "initial_state": None,
                    "steps": [
                        {"events": [], "expected_state": "Root.Idle"},
                        {"events": [], "expected_state": "Root.Active"},
                    ],
                }
            ]
        },
        ensure_ascii=False,
    )


def _sl7_pass_raw() -> str:
    return json.dumps(
        {
            "decision": "pass",
            "risk_level": "none",
            "findings": [],
            "blocking_findings": [],
        },
        ensure_ascii=False,
    )


def _sl10b_accept_raw() -> str:
    return json.dumps(
        {
            "decision": "accept",
            "drift_risk": "none",
            "drift_evidence": [],
        },
        ensure_ascii=False,
    )


def _mock_loop_config(tmp_path: Path, *, run_id: str = "pr-c-mock-success") -> schema.LoopConfig:
    return schema.LoopConfig(
        condition_id="mock_profile_v1",
        condition_family="test_profile",
        base_condition_id="full_staged_v1",
        changed_factors=["llm_provider_mode=mock"],
        llm_provider_mode="mock",
        llm_policy={**schema._default_llm_policy(), "provider_mode": "mock"},
        academic_question="mock profile only validates PR-C wiring and is excluded from main results",
        output_dir=str(tmp_path),
        run_id=run_id,
        llm_model="mock-model",
        max_iterations=1,
    )


def _assert_redaction_stage_failure_record(record: schema.AgentLoopRunRecord, *, stage_id: str, secret: str) -> dict[str, object]:
    payload = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)
    interaction = next(item for item in record.llm_interactions if item["stage_id"] == stage_id)

    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.final_artifacts["exclusion_reason"] == "verdict_not_success"
    assert record.final_artifacts["verdict_source_stage_id"] == stage_id
    assert "redaction_failed" in record.final_artifacts["verdict_reason"]
    assert interaction["retry_error"]["error_kind"] == "redaction_failed"
    assert interaction["omitted"] == "redaction_failed"
    assert interaction["redaction_failure_path"].startswith("llm_interaction")
    assert secret not in payload
    assert not is_path_result_eligible(record)
    return interaction


def test_pr_c_default_entry_missing_real_env_provider_writes_provider_error_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(key, raising=False)

    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-missing-provider")
    result = loop.run_agent_loop("The controller starts in Idle and Start moves it to Active.", cfg)

    assert result.status == "api_failed"
    assert result.run_record_path is not None
    record = read_agent_loop_run_record(result.run_record_path)
    stage_ids = [row["stage_id"] for row in record.stage_records]

    assert record.status == "error"
    assert record.final_artifacts["verdict"] == "provider_error"
    assert record.final_artifacts["verdict_source_stage_id"] == StageId.SL_1_INITIAL_MODELING.value
    assert record.final_artifacts["main_result_eligible"] is False
    assert not is_path_result_eligible(record)
    assert stage_ids[:2] == [StageId.SC_0_START.value, StageId.SL_1_INITIAL_MODELING.value]
    assert StageId.SD_2_PARSE.value not in stage_ids
    assert stage_ids[-2:] == [StageId.SC_12_EXIT.value, StageId.SC_13_TRACE_AUDIT.value]
    assert record.run_config["condition_id"] == "full_staged_v1"
    assert record.run_config["default_loop_config_entry_integrated"] is True
    assert record.run_config["real_llm_provider_api"] is True
    assert record.run_config["contract_only"] is False
    assert record.environment["provider_mode"] == "real_env"
    assert record.environment["real_llm_provider_api"] is True
    assert record.environment["provider_config_read"] is False
    assert record.environment["provider_model_redacted"]
    assert record.environment["config_hash"] == record.run_config["condition_hash"]
    assert "pyfcstm_version" in record.environment
    assert "dependency_versions" in record.environment
    assert isinstance(record.redaction_report, list)
    assert record.llm_interactions[-1]["retry_error"]["error_kind"] == "provider_error"


def test_pr_c_default_run_id_is_unique_per_run_and_does_not_overwrite(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    for key in ("LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"):
        monkeypatch.delenv(key, raising=False)

    nl = "Same NL and same LoopConfig should still produce independently auditable records."
    first = loop.run_agent_loop(nl, schema.LoopConfig(output_dir=str(tmp_path)))
    second = loop.run_agent_loop(nl, schema.LoopConfig(output_dir=str(tmp_path)))

    assert first.run_record_path is not None
    assert second.run_record_path is not None
    assert first.run_record_path != second.run_record_path
    assert first.run_record_id != second.run_record_id
    assert len(list(tmp_path.glob("*.agent_loop.json.gz"))) == 2
    assert read_agent_loop_run_record(first.run_record_path).run_id == first.run_record_id
    assert read_agent_loop_run_record(second.run_record_path).run_id == second.run_record_id


def test_pr_c_default_config_post_init_mutation_is_revalidated_at_run(tmp_path: Path) -> None:
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="mutated-default-budget")
    cfg.max_iterations = 0

    with pytest.raises(ValueError, match="default path cannot silently change budget_policy"):
        loop.run_agent_loop("Mutated config must not masquerade as full_staged_v1.", cfg)


def test_pr_c_explicit_mock_profile_runs_full_staged_path_but_is_not_main_result(tmp_path: Path) -> None:
    provider = MockLLMProvider(responses=[_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()])
    cfg = _mock_loop_config(tmp_path)

    result = loop.run_agent_loop(
        "The controller starts in Idle and Start moves it to Active.",
        cfg,
        llm_provider=provider,
    )

    assert result.status == "converged"
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = [row["stage_id"] for row in record.stage_records]

    assert StageId.SL_1_INITIAL_MODELING.value in stage_ids
    assert StageId.SD_2_PARSE.value in stage_ids
    assert StageId.SD_4_DESIGN.value in stage_ids
    assert StageId.SL_5_SCENARIO_GENERATION.value in stage_ids
    assert StageId.SL_7_MODEL_REVIEW.value in stage_ids
    assert stage_ids[-2:] == [StageId.SC_12_EXIT.value, StageId.SC_13_TRACE_AUDIT.value]
    assert result.resolved_config["condition_id"] == "mock_profile_v1"
    assert record.status == "success"
    assert record.final_artifacts["verdict"] == "success"
    assert record.final_artifacts["oracle_weak"] is False
    assert record.final_artifacts["main_result_eligible"] is False
    assert "non_default_condition" in record.final_artifacts["exclusion_reason"]
    assert not is_path_result_eligible(record)
    assert record.run_config["llm_provider_mode"] == "mock"
    assert record.run_config["default_loop_config_entry_integrated"] is True
    assert record.run_config["real_llm_provider_api"] is False
    assert record.environment["provider_mode"] == "mock"
    assert record.environment["provider_model_redacted"] == "mock-model"
    assert record.redaction_report == []
    assert len(record.llm_interactions) == 3
    assert all(item["provider"] == "mock" for item in record.llm_interactions)
    assert all(item["real_llm_provider_api"] is False for item in record.llm_interactions)


def test_pr_c_explicit_mock_profile_preserves_review_meta_environment_and_eligibility(tmp_path: Path) -> None:
    provider = MockLLMProvider(responses=[_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()])
    cfg = _mock_loop_config(tmp_path, run_id="pr-c-record-fields")

    result = loop.run_agent_loop("Start moves Idle to Active.", cfg, llm_provider=provider)
    record = read_agent_loop_run_record(result.run_record_path or "")

    assert record.run_id == "pr-c-record-fields"
    assert record.run_config["condition_hash"] == cfg.resolved_config()["condition_hash"]
    assert record.environment["resolved_config"]["condition_id"] == "mock_profile_v1"
    assert record.environment["config_hash"] == record.run_config["condition_hash"]
    assert record.environment["pyfcstm_version"]
    assert record.environment["dependency_versions"]["python"]
    assert record.final_artifacts["inclusion_reason"] is None
    assert record.final_artifacts["exclusion_reason"]
    assert record.input_bundle["pr_b1_control_flow_only"] is False
    assert record.input_bundle["default_loop_config_entry_integrated"] is True
    assert record.deterministic_feedback["iterations"][0]["parse"]["ok"] is True
    assert record.deterministic_feedback["iterations"][0]["design"]["info_items"]
    assert record.scenario_history[0]["scenario_set_id"] == record.iteration_records[0]["scenario_set_id"]
    sl5 = next(item for item in record.llm_interactions if item["stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value)
    assert sl5["scenario_hot_start_policy"] == "preserve_explicit_hot_start_add_default_init_cycle"
    assert sl5["parsed_output"]["scenarios"][0]["initial_state"] is None
    sl7 = next(item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value)
    assert sl7["review_meta"]["provider"] == "mock"
    assert sl7["review_meta"]["parsed_schema_version"] == "ModelReviewFeedback.v1"
    assert sl7["review_meta"]["schema_validation_ok"] is True
    assert record.stage_graph["planned"][0] == StageId.SC_0_START.value
    assert record.stage_graph["executed"][-1] == StageId.SC_13_TRACE_AUDIT.value


def test_pr_c_default_entry_rejects_provider_injection_to_protect_real_env_path(tmp_path: Path) -> None:
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-no-provider-injection")
    provider = MockLLMProvider(responses=[_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()])

    with pytest.raises(ValueError, match="default full_staged_v1 must use real_env provider"):
        loop.run_agent_loop("Start moves Idle to Active.", cfg, llm_provider=provider)


def test_pr_c_pre_scenario_repair_uses_main_sd8_sl9_sd10_sl10b_chain_before_scenariogen(tmp_path: Path) -> None:
    bad_initial = json.dumps({"candidate_dsl": "state Root {", "grounding_seeds": [], "assumptions": []}, ensure_ascii=False)
    provider = MockLLMProvider(responses=[bad_initial, _good_dsl(), _sl10b_accept_raw(), _sl5_ok_raw(), _sl7_pass_raw()])
    cfg = _mock_loop_config(tmp_path, run_id="pr-c-pre-scenario-repair")
    cfg.max_iterations = 2

    result = loop.run_agent_loop("Start moves Idle to Active.", cfg, llm_provider=provider)
    record = read_agent_loop_run_record(result.run_record_path or "")
    stage_ids = [row["stage_id"] for row in record.stage_records]

    assert result.status == "converged"
    first_sd8 = stage_ids.index(StageId.SD_8_FIX_PLAN.value)
    assert StageId.SL_5_SCENARIO_GENERATION.value not in stage_ids[:first_sd8]
    assert record.iteration_records[0]["selected_feedback"]["is_pre_scenario"] is True
    assert record.replay_index["pre_scenario_repair_count"] == 1
    assert record.repair_history[0]["repair_stage_ids"] == [
        StageId.SD_8_FIX_PLAN.value,
        StageId.SL_9_REPAIR.value,
        StageId.SD_10_REPAIR_REVIEW.value,
        StageId.SL_10B_DELTA_REVIEW.value,
        StageId.SC_11_ACCEPT_CANDIDATE.value,
    ]
    assert record.repair_history[0]["repair_review_input_summary"]["inputs"] == [
        "NL",
        "GroundingMap",
        "old_dsl",
        "candidate_dsl",
        "FixPlan",
        "ScenarioSet",
    ]
    assert record.repair_history[0]["sd10_repair_review"]["review_meta"] is None
    sc11_index = stage_ids.index(StageId.SC_11_ACCEPT_CANDIDATE.value)
    assert stage_ids.index(StageId.SD_2_PARSE.value, sc11_index + 1) < stage_ids.index(StageId.SL_5_SCENARIO_GENERATION.value)
    sl10b = next(item for item in record.llm_interactions if item["stage_id"] == StageId.SL_10B_DELTA_REVIEW.value)
    assert sl10b["review_meta"]["parsed_schema_version"] == "RepairReviewFeedback.delta_review.v1"
    assert sl10b["review_meta"]["schema_validation_ok"] is True
    assert record.repair_history[0]["repair_review"]["review_meta"]["parsed_schema_version"] == "RepairReviewFeedback.delta_review.v1"


def test_pr_c_run_record_redacts_secrets_from_nl_and_llm_interactions(tmp_path: Path) -> None:
    secret = "sk-prcsecret123456789"
    provider = MockLLMProvider(responses=[_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()])
    cfg = _mock_loop_config(tmp_path, run_id="pr-c-redaction")

    result = loop.run_agent_loop(
        f"Start moves Idle to Active. Operator accidentally pasted LLM_API_KEY={secret}.",
        cfg,
        llm_provider=provider,
    )
    record = read_agent_loop_run_record(result.run_record_path or "")
    payload = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)

    assert secret not in payload
    assert "<redacted:" in payload
    assert record.redaction_report
    assert any(item["field_path"].startswith("run_record.input_bundle.nl") for item in record.redaction_report)


def test_pr_c_run_record_redaction_failure_fails_closed_without_secret(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    secret = "sk-pr26redactionleak12345"
    responses = [_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()]

    class FakeRealProvider:
        provider_name = "fake-real-for-redaction-failure"
        model_id = "fake-real-model"

        def chat(self, **_kwargs: object) -> tuple[str, dict[str, int | str], str]:
            return responses.pop(0), {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
                "model": self.model_id,
            }, self.model_id

    def broken_redactor(*_args: object, **_kwargs: object) -> tuple[object, list[dict[str, object]]]:
        raise RuntimeError("simulated redaction crash")

    monkeypatch.setattr(loop, "RealEnvLLMProvider", lambda: FakeRealProvider())
    monkeypatch.setattr("method.llm_stages.redact_run_record_payload", broken_redactor)
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-redaction-fail-closed")

    result = loop.run_agent_loop(f"Start moves Idle to Active. leaked token LLM_API_KEY={secret}", cfg)

    assert result.status == "spec_failed"
    assert result.run_record_path is not None
    record = read_agent_loop_run_record(result.run_record_path)
    payload = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)

    assert record.status == "invalid"
    assert record.final_artifacts["verdict"] == "invalid"
    assert record.final_artifacts["main_result_eligible"] is False
    assert record.final_artifacts["exclusion_reason"] == "redaction_failed"
    assert record.final_artifacts["redaction_failed"] is True
    assert record.input_bundle["nl"] == "<omitted:redaction_failed>"
    assert secret not in payload
    assert not is_path_result_eligible(record)
    assert any(log.get("event") == "run_record_payload_redaction_failed" for log in record.logs)
    assert record.llm_interactions[0]["omitted"] == "redaction_failed"


def test_pr_c_sl5_parsed_output_redaction_failure_writes_invalid_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    secret = "sk-pr26sl5redaction12345"
    responses = [_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()]
    original_redactor = loop.redact_run_record_payload

    class FakeRealProvider:
        provider_name = "fake-real-for-sl5-redaction-failure"
        model_id = "fake-real-model"

        def chat(self, **_kwargs: object) -> tuple[str, dict[str, int | str], str]:
            return responses.pop(0), {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
                "model": self.model_id,
            }, self.model_id

    def broken_sl5_redactor(
        value: object,
        *,
        path: str = "run_record",
        affects_replay: bool = True,
    ) -> tuple[object, list[dict[str, object]]]:
        if path == "llm_interaction.parsed_output":
            raise RuntimeError("redactor crashed early")
        return original_redactor(value, path=path, affects_replay=affects_replay)

    monkeypatch.setattr(loop, "RealEnvLLMProvider", lambda: FakeRealProvider())
    monkeypatch.setattr(loop, "redact_run_record_payload", broken_sl5_redactor)
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-sl5-redaction-fail-closed")

    result = loop.run_agent_loop(f"Start moves Idle to Active. leaked token LLM_API_KEY={secret}", cfg)

    assert result.status == "spec_failed"
    assert result.run_record_path is not None
    record = read_agent_loop_run_record(result.run_record_path)
    payload = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True)
    sl5 = next(item for item in record.llm_interactions if item["stage_id"] == StageId.SL_5_SCENARIO_GENERATION.value)

    _assert_redaction_stage_failure_record(record, stage_id=StageId.SL_5_SCENARIO_GENERATION.value, secret=secret)
    assert sl5["redaction_failure_path"] == "llm_interaction.parsed_output"
    assert len(list(tmp_path.glob("*.agent_loop.json.gz"))) == 1


def test_pr_c_sl5_adapter_internal_redaction_failure_writes_invalid_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    secret = "sk-pr26sl5internalredaction12345"
    responses = [_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()]
    original_private_redactor = llm_stages._redact_payload

    class FakeRealProvider:
        provider_name = "fake-real-for-sl5-internal-redaction-failure"
        model_id = "fake-real-model"

        def chat(self, **_kwargs: object) -> tuple[str, dict[str, int | str], str]:
            return responses.pop(0), {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
                "model": self.model_id,
            }, self.model_id

    def broken_private_redactor(
        value: object,
        path: str,
        report: list[dict[str, object]],
        *,
        affects_replay: bool = True,
    ) -> object:
        if path == "llm_interaction.parsed_output" and isinstance(value, dict) and "scenarios" in value:
            raise RuntimeError("simulated SL-5 llm_stages parsed_output redaction crash")
        return original_private_redactor(value, path, report, affects_replay=affects_replay)

    monkeypatch.setattr(loop, "RealEnvLLMProvider", lambda: FakeRealProvider())
    monkeypatch.setattr(llm_stages, "_redact_payload", broken_private_redactor)
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-sl5-internal-redaction-fail-closed")

    result = loop.run_agent_loop(f"Start moves Idle to Active. leaked token LLM_API_KEY={secret}", cfg)

    assert result.status == "spec_failed"
    assert result.run_record_path is not None
    record = read_agent_loop_run_record(result.run_record_path)
    sl5 = _assert_redaction_stage_failure_record(record, stage_id=StageId.SL_5_SCENARIO_GENERATION.value, secret=secret)

    assert sl5["redaction_failure_path"] == "llm_interaction.parsed_output"
    assert len(list(tmp_path.glob("*.agent_loop.json.gz"))) == 1


def test_pr_c_sl9_adapter_internal_redaction_failure_writes_invalid_record(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    secret = "sk-pr26sl9internalredaction12345"
    bad_initial = json.dumps({"candidate_dsl": "state Root {", "grounding_seeds": [], "assumptions": []}, ensure_ascii=False)
    responses = [bad_initial, _good_dsl()]
    original_private_redactor = llm_stages._redact_payload
    candidate_seen = {"count": 0}

    class FakeRealProvider:
        provider_name = "fake-real-for-sl9-internal-redaction-failure"
        model_id = "fake-real-model"

        def chat(self, **_kwargs: object) -> tuple[str, dict[str, int | str], str]:
            return responses.pop(0), {
                "prompt_tokens": 1,
                "completion_tokens": 1,
                "total_tokens": 2,
                "model": self.model_id,
            }, self.model_id

    def broken_private_redactor(
        value: object,
        path: str,
        report: list[dict[str, object]],
        *,
        affects_replay: bool = True,
    ) -> object:
        if (
            path == "llm_interaction.parsed_output"
            and isinstance(value, dict)
            and str(value.get("candidate_dsl") or "").strip() == _good_dsl().strip()
        ):
            candidate_seen["count"] += 1
            if candidate_seen["count"] >= 2:
                raise RuntimeError("simulated SL-9 parsed_output redaction crash")
        return original_private_redactor(value, path, report, affects_replay=affects_replay)

    monkeypatch.setattr(loop, "RealEnvLLMProvider", lambda: FakeRealProvider())
    monkeypatch.setattr(llm_stages, "_redact_payload", broken_private_redactor)
    cfg = schema.LoopConfig(output_dir=str(tmp_path), run_id="pr-c-sl9-internal-redaction-fail-closed")

    result = loop.run_agent_loop(f"Start moves Idle to Active. leaked token LLM_API_KEY={secret}", cfg)

    assert result.status == "spec_failed"
    assert result.run_record_path is not None
    record = read_agent_loop_run_record(result.run_record_path)
    sl9 = _assert_redaction_stage_failure_record(record, stage_id=StageId.SL_9_REPAIR.value, secret=secret)

    assert sl9["redaction_failure_path"] == "llm_interaction.parsed_output"
    assert len(list(tmp_path.glob("*.agent_loop.json.gz"))) == 1


def test_pr_c_run_record_write_failure_does_not_return_success(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    provider = MockLLMProvider(responses=[_sl1_ok_raw(), _sl5_ok_raw(), _sl7_pass_raw()])
    cfg = _mock_loop_config(tmp_path, run_id="pr-c-write-failure")

    def fail_write(*_args: object, **_kwargs: object) -> None:
        raise OSError("simulated disk failure")

    monkeypatch.setattr("method.staged_runtime.write_agent_loop_run_record", fail_write)
    result = loop.run_agent_loop("Start moves Idle to Active.", cfg, llm_provider=provider)

    assert result.status == "spec_failed"
    assert result.run_record_path is None
    assert result.error_message is not None
    assert "run record write failed" in result.error_message
