from __future__ import annotations

import json
from pathlib import Path

from method.handoff_smoke.runner import load_handoff_config, run_handoff_smoke
from method.run_record import read_agent_loop_run_record
from method.stages.ids import StageId


CONFIG_ROOT = Path(__file__).resolve().parents[1] / "handoff_smoke" / "configs"


def _configs():
    return [
        load_handoff_config(CONFIG_ROOT / "path1_representative.json"),
        load_handoff_config(CONFIG_ROOT / "path2_representative.json"),
    ]


def test_pr3_handoff_configs_cover_issue14_requirements() -> None:
    configs = _configs()
    assert {cfg.path for cfg in configs} == {"path1", "path2"}
    for cfg in configs:
        assert cfg.schema_version == "agent-loop-pr3-handoff-config.v1"
        assert cfg.source_snapshot["commit"]
        assert cfg.source_snapshot["parquet_path"].endswith(".parquet")
        assert cfg.source_snapshot["fcstm_path"].endswith(".fcstm")
        assert cfg.loop["policy_profile"] == "path_smoke"
        assert cfg.loop["review_policy"]["enable_model_review"] is True
        assert cfg.loop["review_policy"]["model_review_mode"] == "audit_only"
        assert cfg.scenario["steps"] == []
        assert "schema_valid_agent_loop_run_record" in cfg.compatibility_checks
        assert "sl7_real_llm_interaction_recorded" in cfg.compatibility_checks


def test_pr3_handoff_smoke_runs_path1_path2_with_fake_replay(tmp_path: Path) -> None:
    summaries = [run_handoff_smoke(cfg, output_dir=tmp_path) for cfg in _configs()]

    assert {summary.path for summary in summaries} == {"path1", "path2"}
    for summary in summaries:
        assert summary.record_status == "success"
        assert summary.main_result_eligible is True
        assert all(summary.checks.values())
        assert summary.llm_review_provider == "fake-replay"
        assert summary.llm_review_decision == "audit_only"
        assert Path(summary.run_record_path).name == f"{summary.run_id}.agent_loop.json.gz"

        record = read_agent_loop_run_record(summary.run_record_path)
        assert record.input_bundle["path_context"]["path"] == summary.path
        assert record.input_bundle["path_context"]["not_formal_path_metric"] is True
        assert record.run_config["policy_profile"] == "path_smoke"
        assert record.run_config["review_mode"] == "fake_replay"
        assert record.run_config["real_llm_provider_api"] is False
        assert StageId.SL_7_MODEL_REVIEW.value in summary.stage_ids
        assert StageId.SC_13_TRACE_AUDIT.value in summary.stage_ids
        assert record.llm_interactions
        sl7 = [item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value][0]
        assert sl7["schema_validation_ok"] is True
        assert sl7["prompt_messages"]
        assert sl7["raw_output"]


def test_pr3_handoff_real_llm_mode_requires_env_without_reading_dotenv(tmp_path: Path, monkeypatch) -> None:
    cfg = load_handoff_config(CONFIG_ROOT / "path1_representative.json")
    for key in ["LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"]:
        monkeypatch.delenv(key, raising=False)

    import pytest

    with pytest.raises(KeyError, match="source .env"):
        run_handoff_smoke(cfg, output_dir=tmp_path, real_llm=True)


def test_pr3_handoff_real_llm_mode_records_provider_metadata(tmp_path: Path, monkeypatch) -> None:
    cfg = load_handoff_config(CONFIG_ROOT / "path1_representative.json")
    monkeypatch.setenv("LLM_ENDPOINT", "https://example.invalid/")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-do-not-persist-12345678")
    monkeypatch.setenv("LLM_MODEL", "env-model")

    def fake_chat(**kwargs):
        assert kwargs["model"] == "mock-review-model"
        assert kwargs["response_format"] == {"type": "json_object"}
        return (
            json.dumps(
                {
                    "decision": "audit_only",
                    "risk_level": "none",
                    "findings": [],
                    "blocking_findings": [],
                },
                ensure_ascii=False,
            ),
            {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12, "model": "mock-review-model"},
        )

    monkeypatch.setattr("method.pr2a_loop.llm_chat", fake_chat)

    summary = run_handoff_smoke(
        cfg,
        output_dir=tmp_path,
        real_llm=True,
        llm_model="mock-review-model",
        max_tokens=128,
    )
    record = read_agent_loop_run_record(summary.run_record_path)
    sl7 = [item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value][0]

    assert summary.checks["sl7_real_llm_interaction_recorded"] is True
    assert record.run_config["real_llm_provider_api"] is True
    assert record.run_config["review_mode"] == "real_env"
    assert sl7["provider"] == "openai-compatible-env"
    assert sl7["model_id"] == "mock-review-model"
    assert sl7["usage"]["total_tokens"] == 12
    assert sl7["retry_count"] == 0
    assert sl7["attempts"] == [
        {
            "stage_id": StageId.SL_7_MODEL_REVIEW.value,
            "attempt_index": 0,
            "status": "ok",
            "schema_validation_ok": True,
            "error_kind": None,
            "error_message": None,
            "raw_output_hash": sl7["raw_output_hash"],
            "raw_output": sl7["raw_output"],
            "parsed_output": sl7["parsed_output"],
            "usage": sl7["usage"],
            "model_id": "mock-review-model",
            "provider": "openai-compatible-env",
        }
    ]
    assert "sk-test-do-not-persist-12345678" not in json.dumps(record.__dict__, default=str)


def test_pr3_handoff_real_llm_mode_retries_schema_invalid_output(tmp_path: Path, monkeypatch) -> None:
    cfg = load_handoff_config(CONFIG_ROOT / "path1_representative.json")
    monkeypatch.setenv("LLM_ENDPOINT", "https://example.invalid/")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-do-not-persist-12345678")
    monkeypatch.setenv("LLM_MODEL", "env-model")
    calls = {"n": 0}

    def fake_chat(**kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            return ("provider preface\nnot-json", {"total_tokens": 3, "model": "mock-review-model"})
        return (
            json.dumps(
                {
                    "decision": "audit_only",
                    "risk_level": "none",
                    "findings": [],
                    "blocking_findings": [],
                },
                ensure_ascii=False,
            ),
            {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12, "model": "mock-review-model"},
        )

    monkeypatch.setattr("method.pr2a_loop.llm_chat", fake_chat)

    summary = run_handoff_smoke(
        cfg,
        output_dir=tmp_path,
        real_llm=True,
        llm_model="mock-review-model",
        max_tokens=128,
        max_retries=2,
    )
    record = read_agent_loop_run_record(summary.run_record_path)
    sl7 = [item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value][0]

    assert calls["n"] == 2
    assert record.status == "success"
    assert summary.llm_review_retry_count == 1
    assert summary.llm_review_attempt_statuses == ["schema_invalid", "ok"]
    assert sl7["retry_count"] == 1
    assert sl7["review_meta"]["retry_count"] == 1
    assert [attempt["status"] for attempt in sl7["attempts"]] == ["schema_invalid", "ok"]
    assert sl7["attempts"][0]["raw_output_hash"].startswith("sha256:")
    assert any(log["event"] == "llm_review_attempt_failed" for log in record.logs)
    assert any(log["event"] == "llm_review_retry_recovered" for log in record.logs)


def test_pr3_handoff_real_llm_mode_retries_provider_error(tmp_path: Path, monkeypatch) -> None:
    cfg = load_handoff_config(CONFIG_ROOT / "path1_representative.json")
    monkeypatch.setenv("LLM_ENDPOINT", "https://example.invalid/")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-do-not-persist-12345678")
    monkeypatch.setenv("LLM_MODEL", "env-model")
    calls = {"n": 0}

    def fake_chat(**kwargs):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("502 Bad Gateway")
        return (
            json.dumps(
                {
                    "decision": "audit_only",
                    "risk_level": "none",
                    "findings": [],
                    "blocking_findings": [],
                },
                ensure_ascii=False,
            ),
            {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12, "model": "mock-review-model"},
        )

    monkeypatch.setattr("method.pr2a_loop.llm_chat", fake_chat)

    summary = run_handoff_smoke(
        cfg,
        output_dir=tmp_path,
        real_llm=True,
        llm_model="mock-review-model",
        max_tokens=128,
        max_retries=2,
    )
    record = read_agent_loop_run_record(summary.run_record_path)
    sl7 = [item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value][0]

    assert calls["n"] == 2
    assert record.status == "success"
    assert summary.llm_review_retry_count == 1
    assert summary.llm_review_attempt_statuses == ["provider_error", "ok"]
    assert [attempt["status"] for attempt in sl7["attempts"]] == ["provider_error", "ok"]
    assert "502 Bad Gateway" in sl7["attempts"][0]["error_message"]


def test_pr3_handoff_real_llm_mode_marks_invalid_after_retry_exhausted(tmp_path: Path, monkeypatch) -> None:
    cfg = load_handoff_config(CONFIG_ROOT / "path1_representative.json")
    monkeypatch.setenv("LLM_ENDPOINT", "https://example.invalid/")
    monkeypatch.setenv("LLM_API_KEY", "sk-test-do-not-persist-12345678")
    monkeypatch.setenv("LLM_MODEL", "env-model")

    def fake_chat(**kwargs):
        return ("not-json", {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2, "model": "mock-review-model"})

    monkeypatch.setattr("method.pr2a_loop.llm_chat", fake_chat)

    summary = run_handoff_smoke(
        cfg,
        output_dir=tmp_path,
        real_llm=True,
        llm_model="mock-review-model",
        max_tokens=128,
        max_retries=1,
    )
    record = read_agent_loop_run_record(summary.run_record_path)
    sl7 = [item for item in record.llm_interactions if item["stage_id"] == StageId.SL_7_MODEL_REVIEW.value][0]

    assert record.status == "invalid"
    assert summary.main_result_eligible is False
    assert summary.checks["status_success_and_path_eligible"] is False
    assert summary.checks["sl7_real_llm_interaction_recorded"] is False
    assert summary.llm_review_retry_count == 1
    assert [attempt["status"] for attempt in sl7["attempts"]] == ["schema_invalid", "schema_invalid"]
    assert sl7["attempts"][-1]["retry_exhausted"] is True
    assert "retry exhausted" in sl7["schema_validation_error"]
    assert any(log["event"] == "llm_review_retry_exhausted" for log in record.logs)


def test_pr3_handoff_summary_json_shape_is_stable(tmp_path: Path) -> None:
    summary = run_handoff_smoke(load_handoff_config(CONFIG_ROOT / "path2_representative.json"), output_dir=tmp_path)
    payload = json.loads(json.dumps(summary.__dict__, ensure_ascii=False))

    assert payload["path"] == "path2"
    assert payload["case_id"]
    assert payload["run_record_path"].endswith(".agent_loop.json.gz")
    assert isinstance(payload["llm_review_retry_count"], int)
    assert isinstance(payload["llm_review_attempt_statuses"], list)
    assert isinstance(payload["checks"], dict)
