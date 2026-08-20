"""Regression tests for the final-output semantic-judge boundary."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest

MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "experiments/luna_full_x3_20260819/semantic_judge.py"
)
SPEC = importlib.util.spec_from_file_location("paper1_semantic_judge_test", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
semantic_judge = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = semantic_judge
SPEC.loader.exec_module(semantic_judge)

AGGREGATE_PATH = MODULE_PATH.with_name("aggregate.py")
AGGREGATE_SPEC = importlib.util.spec_from_file_location(
    "paper1_semantic_aggregate_test", AGGREGATE_PATH
)
assert AGGREGATE_SPEC is not None and AGGREGATE_SPEC.loader is not None
aggregate = importlib.util.module_from_spec(AGGREGATE_SPEC)
sys.modules[AGGREGATE_SPEC.name] = aggregate
AGGREGATE_SPEC.loader.exec_module(aggregate)


def test_judge_response_schemas_have_prompt_guidance_for_every_field() -> None:
    for model in (
        semantic_judge.PairJudgement,
        semantic_judge.AtomicMatchDecision,
    ):
        schema = model.model_json_schema()
        documented_models = [(model.__name__, schema), *schema.get("$defs", {}).items()]
        for model_name, model_schema in documented_models:
            if "properties" not in model_schema:
                continue
            assert model_schema.get("description"), model_name
            for field_name, field_schema in model_schema["properties"].items():
                assert field_schema.get("description"), f"{model_name}.{field_name}"


def test_method_judge_input_contains_only_final_d1_d2_clusters(tmp_path: Path) -> None:
    record_path = tmp_path / "run1" / "0000-luna" / "record.json"
    record_path.parent.mkdir(parents=True)
    record_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "finding_records": [{"finding_key": "raw-d0-must-not-leak"}],
                "report_issue_clusters": [
                    {
                        "report_issue_id": "audit-d0",
                        "cause_key": "audit-d0",
                        "d_level": "D0",
                    },
                    {
                        "report_issue_id": "published-d1",
                        "cause_key": "published-d1",
                        "d_level": "D1",
                        "claims": ["D1 claim"],
                    },
                    {
                        "report_issue_id": "published-d2",
                        "cause_key": "published-d2",
                        "d_level": "D2",
                        "claims": ["D2 claim"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    payload = semantic_judge._cell_payload(tmp_path, "method", "0000", 1)

    assert payload["status"] == "ok"
    assert [item["finding_id"] for item in payload["findings"]] == [
        "published-d1",
        "published-d2",
    ]


def test_semantic_judge_cli_defaults_to_stream_and_allows_only_explicit_opt_out() -> None:
    required = [
        "--method-root",
        "method",
        "--baseline-root",
        "baseline",
        "--output-dir",
        "out",
    ]

    assert semantic_judge.build_parser().parse_args(required).streaming is True
    assert semantic_judge.build_parser().parse_args(required).effort is None
    assert (
        semantic_judge.build_parser()
        .parse_args([*required, "--effort", "medium"])
        .effort
        == "medium"
    )
    assert (
        semantic_judge.build_parser().parse_args([*required, "--no-stream"]).streaming
        is False
    )

    with pytest.raises(SystemExit):
        semantic_judge.build_parser().parse_args([*required, "--stream", "--no-stream"])


def test_baseline_judge_reads_the_frozen_x1v2_cell_layout(tmp_path: Path) -> None:
    record_path = tmp_path / "run1" / "0000-luna-x1v2" / "record.json"
    record_path.parent.mkdir(parents=True)
    record_path.write_text(
        json.dumps(
            {
                "status": "ok",
                "parsed_output": {
                    "issues": [
                        {"issue": "missing transition", "where": "Root", "reason": "fixture"}
                    ]
                },
            }
        ),
        encoding="utf-8",
    )

    payload = semantic_judge._cell_payload(tmp_path, "baseline", "0000", 1)

    assert payload["status"] == "ok"
    assert len(payload["findings"]) == 1


def test_aggregate_preserves_latest_successful_judgement(tmp_path: Path) -> None:
    successful = tmp_path / "judge-v1" / "worker" / "0000.json"
    failed = tmp_path / "judge-v2" / "worker" / "0000.json"
    successful.parent.mkdir(parents=True)
    failed.parent.mkdir(parents=True)
    successful.write_text(json.dumps({"status": "ok", "judgement": {}}), encoding="utf-8")
    failed.write_text(json.dumps({"status": "failed", "failure": {}}), encoding="utf-8")

    selected = aggregate.load_judgements(tmp_path, ["0000"])

    assert selected["0000"]["status"] == "ok"


def test_aggregate_normalizes_prototype_completed_status(tmp_path: Path) -> None:
    record = tmp_path / "run1" / "0000-luna" / "record.json"
    record.parent.mkdir(parents=True)
    record.write_text(json.dumps({"status": "completed"}), encoding="utf-8")

    status, payload = aggregate.cell_status(tmp_path, "method", "0000", 1)

    assert status == "ok"
    assert payload["status"] == "completed"


def _hit(*, hit: bool, supporting_ids: list[str]) -> semantic_judge.HitAssessment:
    return semantic_judge.HitAssessment(
        hit=hit,
        supporting_finding_ids=supporting_ids,
        reason="fixture",
        confidence="high",
    )


def _pair_judgement(
    *,
    method_hit: semantic_judge.HitAssessment,
    matched_ledger_ids: list[str],
    false_positive: bool,
) -> semantic_judge.PairJudgement:
    miss = _hit(hit=False, supporting_ids=[])
    return semantic_judge.PairJudgement(
        pair="0000",
        ledger_assessments=[
            semantic_judge.LedgerAssessment(
                ledger_id="LEDGER-1",
                method_run1=method_hit,
                method_run2=miss,
                method_run3=miss,
                baseline_run1=miss,
                baseline_run2=miss,
                baseline_run3=miss,
            )
        ],
        emission_assessments=[
            semantic_judge.EmissionAssessment(
                cell="method_run1",
                emitted_id="published-d2",
                matched_ledger_ids=matched_ledger_ids,
                false_positive=false_positive,
                reason="fixture",
                confidence="high",
            )
        ],
        pair_reason="fixture",
    )


def test_shape_rejects_supporting_id_outside_the_cell_release_set() -> None:
    result = _pair_judgement(
        method_hit=_hit(hit=True, supporting_ids=["raw-d0-must-not-leak"]),
        matched_ledger_ids=["LEDGER-1"],
        false_positive=False,
    )
    ledger = [{"ledger_id": "LEDGER-1"}]
    cells = [
        {"cell": "method_run1", "findings": [{"finding_id": "published-d2"}]},
        *[
            {"cell": cell, "findings": []}
            for cell in (
                "method_run2",
                "method_run3",
                "baseline_run1",
                "baseline_run2",
                "baseline_run3",
            )
        ],
    ]

    errors = semantic_judge._validate_shape(result, ledger, cells)

    assert any("unknown supporting ids" in error for error in errors)


def test_shape_requires_hit_and_fp_receipts_to_be_consistent() -> None:
    result = _pair_judgement(
        method_hit=_hit(hit=True, supporting_ids=[]),
        matched_ledger_ids=["LEDGER-1"],
        false_positive=True,
    )
    ledger = [{"ledger_id": "LEDGER-1"}]
    cells = [
        {"cell": "method_run1", "findings": [{"finding_id": "published-d2"}]},
        *[
            {"cell": cell, "findings": []}
            for cell in (
                "method_run2",
                "method_run3",
                "baseline_run1",
                "baseline_run2",
                "baseline_run3",
            )
        ],
    ]

    errors = semantic_judge._validate_shape(result, ledger, cells)

    assert any("hit requires a supporting id" in error for error in errors)
    assert any("false_positive must equal" in error for error in errors)


def test_structural_normalization_drops_only_unknown_placeholder_emissions() -> None:
    result = _pair_judgement(
        method_hit=_hit(hit=True, supporting_ids=["published-d2"]),
        matched_ledger_ids=["LEDGER-1"],
        false_positive=False,
    )
    result.emission_assessments.append(
        semantic_judge.EmissionAssessment(
            cell="method_run2",
            emitted_id="(no findings)",
            matched_ledger_ids=[],
            false_positive=True,
            reason="fixture placeholder",
            confidence="high",
        )
    )
    cells = [
        {"cell": "method_run1", "findings": [{"finding_id": "published-d2"}]},
        *[
            {"cell": cell, "findings": []}
            for cell in (
                "method_run2",
                "method_run3",
                "baseline_run1",
                "baseline_run2",
                "baseline_run3",
            )
        ],
    ]

    normalized = semantic_judge._drop_unknown_emission_rows(result, cells)

    assert [(row.cell, row.emitted_id) for row in normalized.emission_assessments] == [
        ("method_run1", "published-d2")
    ]
    assert semantic_judge._validate_shape(normalized, [{"ledger_id": "LEDGER-1"}], cells) == []


def test_pair_shape_failure_falls_back_to_atomic_llm_judgement(tmp_path: Path) -> None:
    method_record = tmp_path / "method" / "run1" / "0000-luna" / "record.json"
    method_record.parent.mkdir(parents=True)
    method_record.write_text(
        json.dumps(
            {
                "status": "ok",
                "report_issue_clusters": [
                    {
                        "report_issue_id": "published-d2",
                        "d_level": "D2",
                        "claims": ["The required target state is absent."],
                        "locations": ["NL1", "PUML:L2"],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    class AtomicFallbackResponder:
        def __init__(self) -> None:
            self.pair_calls = 0
            self.atomic_calls = 0

        def invoke_structured(self, *, role, schema, system_prompt, user_input):
            if schema is semantic_judge.PairJudgement:
                self.pair_calls += 1
                raise semantic_judge.StructuredOutputValidationError(
                    "pair-wide shape fixture"
                )
            assert schema is semantic_judge.AtomicMatchDecision
            self.atomic_calls += 1
            return semantic_judge.AtomicMatchDecision(
                matches=True,
                reason="The issue names the same missing target required by the ledger.",
                confidence="high",
            )

        def take_last_observation(self):
            return None

    ledger_items = {
        "LEDGER-1": {
            "id": "LEDGER-1",
            "pair": "0000",
            "D": "D2",
            "L": "L0",
            "summary": "The required target state is absent.",
            "detail": "NL1 requires the target and PUML:L2 omits it.",
            "D_basis": "Direct requirement violation.",
            "L_basis": "Direct name comparison.",
        }
    }
    responder = AtomicFallbackResponder()

    result, observations = semantic_judge.judge_pair(
        "0000",
        ledger_items,
        tmp_path / "method",
        tmp_path / "baseline",
        responder,
    )

    assert observations == []
    assert result["status"] == "ok"
    assert result["adjudication_mode"] == "atomic_llm_fallback"
    assert responder.pair_calls == 3
    assert responder.atomic_calls == 1
    assessment = result["judgement"]["ledger_assessments"][0]["method_run1"]
    assert assessment["hit"] is True
    assert assessment["supporting_finding_ids"] == ["published-d2"]
    assert result["judgement"]["emission_assessments"][0]["false_positive"] is False


def test_provider_exhaustion_retries_same_judge_request_until_success(monkeypatch) -> None:
    completed = semantic_judge.AtomicMatchDecision(
        matches=True,
        reason="same place and property",
        confidence="high",
    )

    class RecoveringResponder:
        def __init__(self) -> None:
            self.calls = 0
            self.observation = None

        def invoke_structured(self, **_kwargs):
            self.calls += 1
            if self.calls == 1:
                now = datetime.now(timezone.utc)
                self.observation = SimpleNamespace(
                    llm_call_id="provider-failure",
                    role="judge",
                    profile="gpt-5.6-sol",
                    adapter="openai",
                    provider="fixture",
                    configured_model="gpt-5.6-sol",
                    observed_model=None,
                    started_at=now,
                    finished_at=now,
                    elapsed_ms=1.0,
                    status="failed",
                    usage={},
                    attempts=(
                        {
                            "attempt_index": 1,
                            "status": "failed",
                            "failure_phase": "provider_response",
                            "retryable": True,
                            "cost_counted": True,
                            "billing_disposition": "counted",
                        },
                    ),
                    structured_schema_sha256="fixture",
                    prompt_cache={},
                    pricing=None,
                    failure="provider unavailable",
                )
                raise RuntimeError("provider unavailable")
            self.observation = None
            return completed

        def take_last_observation(self):
            value = self.observation
            self.observation = None
            return value

    responder = RecoveringResponder()
    observations = []
    monkeypatch.setattr(semantic_judge.time, "sleep", lambda _seconds: None)

    result = semantic_judge._invoke_judge(
        responder=responder,
        role="judge",
        schema=semantic_judge.AtomicMatchDecision,
        system_prompt="system",
        user_input="user",
        observations=observations,
    )

    assert result == completed
    assert responder.calls == 2
    assert observations[0]["attempts"][-1]["billing_disposition"] == (
        "provider_error_retry_exempt"
    )
    assert observations[0]["attempts"][-1]["cost_counted"] is False
