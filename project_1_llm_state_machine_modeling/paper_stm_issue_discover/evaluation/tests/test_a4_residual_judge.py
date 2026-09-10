"""Residual export never sends oracle receipts or rejudges a completed report."""

import importlib.util
import json
from pathlib import Path

import pytest

from paper_stm_evaluation.a4_sources import checked_json
from paper_stm_judge.protocol import PROTOCOL_SHA256, PROTOCOL_VERSION, prompt_hash
from utils.artifact_io import write_json


PAPER = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location(
    "a4_residual_judge", PAPER / "discover_matrix/docs/generations/a4_20260910/residual_judge.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_residual_export_resume_and_protocol_guard(tmp_path, monkeypatch):
    monkeypatch.setattr(MODULE, "verify", lambda *args: {"eligible_cells": 162})
    write_json(tmp_path / "manifest.json", {"sources": {"cells": [{"pair": "0000", "round": 1}]}})
    cell = tmp_path / "cells/0000/round-1"
    write_json(cell / "tail.json", {
        "eligible": True, "errors": [], "report_issue_clusters": [
            {"issue_id": "r1", "expected": "expected", "observed": "observed",
             "receipt": {"verdict": "true"}, "oracle": "hidden"}
        ],
    })
    write_json(cell / "accounting.json", {
        "reports": [{"report_id": "r1", "route": "residual", "outcome": None}], "pending": 1,
    })
    assert MODULE.prepare(PAPER, tmp_path) == {1: {"0000": ["r1"]}, 2: {}, 3: {}}
    source_path = tmp_path / "judge_source/method/0000/round-1.json"
    source, source_hash = checked_json(source_path)
    assert source["report_issue_clusters"] == [{"issue_id": "r1", "expected": "expected", "observed": "observed"}]
    record = {
        "status": "completed", "model_profile": "gpt-5.6-luna", "k_closure": "relation_first",
        "validity_aggregation": "arbitration", "validity_arbitration_trigger": "any",
        "closure_profile": "full", "protocol_sha256": PROTOCOL_SHA256,
        "protocol_version": PROTOCOL_VERSION, "prompt_template_hash": prompt_hash(),
        "pair_id": "0000", "round": 1, "adapter_audit": {"source_hash": source_hash},
        "report_outcomes": [{"original_report_id": "r1", "validity": "INVALID"}],
    }
    destination = tmp_path / "judge/run/pairs/0000.json"
    write_json(destination, record)
    assert MODULE.prepare(PAPER, tmp_path) == {1: {}, 2: {}, 3: {}}
    final = json.loads((tmp_path / "final_accounting.json").read_text())
    assert final["pending"] == 0
    assert final["cells"][0]["reports"][0]["route"] == "newly_judged"
    record["prompt_template_hash"] = "changed"
    write_json(destination, record)
    with pytest.raises(ValueError, match="protocol"):
        MODULE.prepare(PAPER, tmp_path)


def test_analysis_counts_unique_expected_units_and_keeps_zero_cells():
    spec = importlib.util.spec_from_file_location(
        "a4_analysis", PAPER / "discover_matrix/docs/generations/a4_20260910/analyze_a4.py"
    )
    analysis = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(analysis)
    known = {"validity": "VALID_KNOWN", "round": 1, "full_ledger_ids": ["E1"],
             "partial_ledger_ids": [], "d_tier": "D0"}
    invalid = {"validity": "INVALID", "round": 1, "full_ledger_ids": [], "partial_ledger_ids": []}
    result = analysis.tally([known, known, invalid], 2, 6)
    assert result["precision"] == {"numerator": 2, "denominator": 3, "rate": 2 / 3}
    assert result["strict_precision"]["numerator"] == 0
    assert result["hit"]["numerator"] == 1
    assert result["invalid_per_cell"]["rate"] == .5
    assert analysis.tally([], 1, 3)["precision"]["rate"] is None
    oracle = analysis.report_row({**invalid, "original_report_id": "oracle"}, "0000", 1)
    novel = analysis.report_row({**invalid, "original_report_id": "novel", "validity": "VALID_NOVEL", "d_tier": "D1"}, "0000", 1)
    metrics = analysis.calculate_metrics([oracle, novel], {})
    assert metrics["D_A"] == {"NO_EXTERNAL_D_A_LABEL": 1, "D1": 1}
    assert metrics["precision"]["rate"] == metrics["strict"]["precision"]["rate"] == .5
    json.dumps(metrics, sort_keys=True)
