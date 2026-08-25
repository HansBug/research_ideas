from __future__ import annotations

import json
from pathlib import Path

from pipeline.evidence_discovery.reporting.applicability import (
    DEFAULT_DIAGNOSTIC_PAIRS,
    GLOBAL_PLANNED_PREDICATES,
    build_applicability_matrix,
)
from pipeline.evidence_discovery.orchestration.runner import _load_selection_preflight


PAPER_ROOT = Path(__file__).parents[3]
REPORT_ROOT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"


def test_applicability_preflight_is_fixed_15_by_15_and_has_twelve_e15_predicates() -> None:
    payload = build_applicability_matrix(report_root=REPORT_ROOT)

    assert tuple(payload["selected_pair_ids"]) == DEFAULT_DIAGNOSTIC_PAIRS
    assert payload["pair_count"] == 15
    assert len(payload["rows"]) == 15 * len(GLOBAL_PLANNED_PREDICATES)
    assert payload["candidate_predicates_e15"] == [
        "G1", "G4", "R1", "R4", "S1", "S2", "S3", "S4", "S5", "S6", "V1", "V4"
    ]
    assert payload["candidate_predicate_count_e15"] == 12
    assert all(item["input_manifest_hash"] for item in payload["pairs"].values())
    assert all(item["input_hashes"] for item in payload["pairs"].values())


def test_applicability_rows_expose_typed_schema_without_execution_or_evaluation_data() -> None:
    payload = build_applicability_matrix(report_root=REPORT_ROOT)
    rows = payload["rows"]

    s1 = next(item for item in rows if item["pair_id"] == "0002" and item["predicate_id"] == "S1")
    assert s1["status"] == "applicable"
    assert s1["typed_input_contract"]["predicate_id"] == "S1"
    assert {field["name"] for field in s1["typed_input_contract"]["fields"]} == {
        "kind", "element", "scope"
    }
    assert s1["predicate_ledger_ids"] == []
    assert s1["ledger_mapping_status"] == "pair_only_no_predicate_column"
    assert "method candidate" in s1["reason"]

    g2 = next(item for item in rows if item["pair_id"] == "0002" and item["predicate_id"] == "G2")
    assert g2["status"] == "not_applicable"
    assert g2["feasibility"] == "not_applicable"
    forbidden = {"judge", "expected", "answer", "hit", "fp", "precision"}
    assert not forbidden.intersection(payload.keys())
    assert not forbidden.intersection(g2.keys())


def test_selection_preflight_reference_validates_hash_and_pair_order(tmp_path: Path) -> None:
    payload = build_applicability_matrix(report_root=REPORT_ROOT)
    path = tmp_path / "pair_predicate_applicability.json"
    path.write_text(
        json.dumps(payload, ensure_ascii=False),
        encoding="utf-8",
    )

    reference = _load_selection_preflight(
        path,
        selected_pair_ids=DEFAULT_DIAGNOSTIC_PAIRS,
    )

    assert reference is not None
    assert reference["artifact_hash"] == payload["artifact_hash"]
    assert tuple(reference["selected_pair_ids"]) == DEFAULT_DIAGNOSTIC_PAIRS
    assert tuple(reference["candidate_predicates_e15"]) == tuple(
        payload["candidate_predicates_e15"]
    )
