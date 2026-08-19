"""Regression tests for the final-output semantic-judge boundary."""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


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


def test_aggregate_preserves_latest_successful_judgement(tmp_path: Path) -> None:
    successful = tmp_path / "judge-v1" / "worker" / "0000.json"
    failed = tmp_path / "judge-v2" / "worker" / "0000.json"
    successful.parent.mkdir(parents=True)
    failed.parent.mkdir(parents=True)
    successful.write_text(json.dumps({"status": "ok", "judgement": {}}), encoding="utf-8")
    failed.write_text(json.dumps({"status": "failed", "failure": {}}), encoding="utf-8")

    selected = aggregate.load_judgements(tmp_path, ["0000"])

    assert selected["0000"]["status"] == "ok"


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
