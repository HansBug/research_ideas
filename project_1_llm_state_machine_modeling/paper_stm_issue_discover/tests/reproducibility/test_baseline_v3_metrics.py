"""Regression tests for provider-free baseline v3 metric units."""

from __future__ import annotations

import importlib.util
import copy
import json
from pathlib import Path

import pytest

import sys


SRC = Path(__file__).parents[2] / "evaluation/src"
sys.path.insert(0, str(SRC))
from paper_stm_evaluation.manual_adjudication_v3_baseline_ni import GroupSetV3


SCRIPT = (
    Path(__file__).parents[2]
    / "scripts/evaluation/recompute_baseline_v3_summary.py"
)


def load_module():
    """Load the standalone provider-free recompute module."""
    spec = importlib.util.spec_from_file_location("baseline_v3_recompute", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def toy_rows():
    """Create duplicate report support for one expected-round unit."""
    relations = [
        {"expected_id": "E-1", "relation": "FULL_MATCH"},
        {"expected_id": "E-2", "relation": "NO_MATCH"},
    ]
    return [
        {"pair_id": "0001", "round": 1, "validity": "VALID_KNOWN", "corrected_kni": "K", "d_tier": "D2", "witness": {"level": "W2"}, "relations": relations},
        {"pair_id": "0001", "round": 1, "validity": "VALID_KNOWN", "corrected_kni": "K", "d_tier": "D2", "witness": {"level": "W2"}, "relations": relations},
        {"pair_id": "0001", "round": 2, "validity": "VALID_KNOWN", "corrected_kni": "K", "d_tier": "D2", "witness": {"level": "W1"}, "relations": relations},
    ]


def toy_ledger():
    """Return two expected rows with one L2 item."""
    return {"items": {"E-1": {"pair": "0001", "L": "L2"}, "E-2": {"pair": "0001", "L": "L1"}}}


def test_hit_at_one_and_w2_use_unique_expected_round_units():
    """Duplicate reports must not inflate all-round hit or W2/all-expected."""
    module = load_module()
    rows = toy_rows()
    metrics = module.project_metrics(rows, toy_ledger(), 0, 0, 0, {})
    assert metrics["hit_at_1_full"] == {
        "numerator": 2,
        "denominator": 6,
        "percentage": 2 / 6,
        "unit": "expected-round units across all 3 rounds",
        "reason": "One deduplicated expected-round unit per expected and round; denominator is 145 x 3",
    }
    assert metrics["w2_all_expected"]["numerator"] == 1
    assert metrics["w2_all_expected"]["denominator"] == 6


def test_baseline_l2_ledger_precision_is_explicitly_not_applicable():
    """Baseline N/I groups must not receive a fabricated L2 denominator."""
    module = load_module()
    metrics = module.project_metrics(toy_rows(), toy_ledger(), 0, 0, 0, {})
    assert metrics["l2_ledger_based"]["status"] == "not_applicable"
    assert metrics["l2_ledger_based"]["reason"]


def load_group_set():
    """Load the canonical v3 group set for structural regression tests."""
    path = Path(__file__).parents[2] / "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/baseline_n_groups_v3.json"
    return json.loads(path.read_text(encoding="utf-8"))["groups"]


@pytest.mark.parametrize("mutation", ["duplicate_member", "wrong_pair", "cross_pair_member", "map_mismatch"])
def test_group_set_rejects_membership_and_boundary_corruption(mutation):
    """Canonical grouping constraints must be enforced by Pydantic itself."""
    document = copy.deepcopy(load_group_set())
    first = document["n_groups"][0]
    if mutation == "duplicate_member":
        first["member_report_ids"].append(first["member_report_ids"][0])
    elif mutation == "wrong_pair":
        first["pair_id"] = "9999"
    elif mutation == "cross_pair_member":
        first["member_report_ids"] = ["0004:r2:baseline_issue_2"]
    else:
        document["report_to_group"][first["member_report_ids"][0]] = "bogus"
    with pytest.raises(ValueError):
        GroupSetV3.model_validate(document)
