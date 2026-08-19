from __future__ import annotations

import json
from pathlib import Path

import pytest
from paper_stm_feedback_loop.common.inputs import clean_path, load_feedback_loop_inputs
from paper_stm_feedback_loop.common.records import (
    ImmutableRecordStore,
    append_jsonl_record,
    load_jsonl_records,
    summarize_records,
)
from paper_stm_feedback_loop.common.telemetry import NodeExecution


def _fixture_report_root() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "representation"
        / "reports"
        / "llms_emp_r45_java_60"
    )


def test_load_feedback_loop_inputs_from_representation_pair() -> None:
    root = _fixture_report_root()
    bundle = load_feedback_loop_inputs(pair_dir=root / "pairs" / "0000")

    assert bundle.pair_id == "llms_emp_feedback_final_0000"
    assert "human driving mode" in bundle.nl_text.lower()
    assert "state llms_emp_feedback_final_0000" in bundle.fcstm_text
    assert bundle.source_trace.entry_count > 0
    assert (
        bundle.working_contract.data["schema_version"]
        == "paper1.working_fcstm_contract.v2"
    )
    summary = bundle.summary()
    assert summary["sha256"]["nl"].startswith("sha256:")
    assert summary["source_trace_entries"] == bundle.source_trace.entry_count


def test_cli_formal_pair_default_root_is_independent_of_cwd() -> None:
    from paper_stm_feedback_loop.discover.cli import (
        REPORT_ROOT,
        _formal_pair,
        build_parser,
    )
    from paper_stm_feedback_loop.discover.responder import DEFAULT_TRANSPORT_RETRIES

    args = build_parser().parse_args(
        ["--pair-id", "0000", "--profile", "test-profile", "--output-dir", "out"]
    )
    bundle = _formal_pair(args)

    assert bundle.report_root == REPORT_ROOT
    assert bundle.pair_id == "llms_emp_feedback_final_0000"
    assert bundle.fcstm.path.name == "fcstm.fcstm"
    assert args.transport_retries == DEFAULT_TRANSPORT_RETRIES == 8
    assert args.streaming is None

    assert (
        build_parser()
        .parse_args(
            [
                "--pair-id",
                "0000",
                "--profile",
                "test-profile",
                "--output-dir",
                "out",
                "--stream",
            ]
        )
        .streaming
        is True
    )
    assert (
        build_parser()
        .parse_args(
            [
                "--pair-id",
                "0000",
                "--profile",
                "test-profile",
                "--output-dir",
                "out",
                "--no-stream",
            ]
        )
        .streaming
        is False
    )

    with pytest.raises(SystemExit):
        build_parser().parse_args(
            [
                "--pair-id",
                "0000",
                "--profile",
                "test-profile",
                "--output-dir",
                "out",
                "--stream",
                "--no-stream",
            ]
        )


def test_load_feedback_loop_inputs_from_custom_files(tmp_path: Path) -> None:
    nl = tmp_path / "nl.txt"
    fcstm = tmp_path / "model.fcstm"
    trace = tmp_path / "trace.json"
    contract = tmp_path / "contract.json"
    nl.write_text("Natural language requirement", encoding="utf-8")
    fcstm.write_text("state Root { }", encoding="utf-8")
    trace.write_text(
        json.dumps(
            {"entries": [], "attribution_exclusions": [], "schema_version": "x"}
        ),
        encoding="utf-8",
    )
    contract.write_text(json.dumps({"schema_version": "contract.v1"}), encoding="utf-8")

    bundle = load_feedback_loop_inputs(
        pair_id="custom_case",
        nl_path=nl,
        fcstm_path=fcstm,
        source_trace_path=trace,
        working_contract_path=contract,
    )

    assert bundle.pair_id == "custom_case"
    assert bundle.nl.text == "Natural language requirement"
    assert bundle.source_trace.entry_count == 0


def test_clean_path_rejects_base_escape(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside.txt"
    outside.write_text("x", encoding="utf-8")
    try:
        clean_path(outside, base_dir=tmp_path)
    except ValueError as exc:
        assert "escapes base" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected base escape rejection")


def test_append_only_jsonl_records_redact_and_summarize(tmp_path: Path) -> None:
    records = tmp_path / "records.jsonl"
    append_jsonl_record(
        records, {"kind": "custom", "status": "ok", "api_key": "sk-secretsecretsecret"}
    )
    append_jsonl_record(
        records,
        NodeExecution(
            node_id="n1",
            node_type="unit",
            started_at="2026-07-24T00:00:00Z",
            status="error",
            error_message="Bearer abcdefghijklmnopqrstuvwxyz123456",
            outputs={"answer": 1},
        ),
    )

    loaded = load_jsonl_records(records)
    assert len(loaded) == 2
    assert loaded[0]["api_key"] == "[REDACTED]"
    assert loaded[1]["error_message"] == "[REDACTED]"
    assert loaded[1]["error_message_sha256"].startswith("sha256:")
    assert summarize_records(loaded)["error_count"] == 1


def test_redaction_preserves_academic_token_usage_fields(tmp_path: Path) -> None:
    store = ImmutableRecordStore(tmp_path / "records")
    ref = store.append(
        "llm-call-completed",
        {
            "api_key": "sk-this-is-a-secret-value",
            "input_tokens": 123,
            "output_tokens": 45,
            "cache_read_input_tokens": 67,
        },
    )
    payload = json.loads(ref.path.read_text(encoding="utf-8"))
    assert payload["api_key"] == "[REDACTED]"
    assert payload["input_tokens"] == 123
    assert payload["output_tokens"] == 45
    assert payload["cache_read_input_tokens"] == 67
