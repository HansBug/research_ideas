import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
OVERLAY = ROOT / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/derived/conversion_attribution_v1"


def test_overlay_closes_current_invalid_and_nadc_sets():
    records = json.loads((OVERLAY / "report_attribution_v1.json").read_text())['records']
    assert len(records) == 291
    assert len({r['report_id'] for r in records}) == 291
    assert sum(r.get('a0_subtype') == 'NOT_A_DEFECT_CLAIM' for r in records) == 118
    assert sum(r['primary_attribution'] == 'CONVERSION_LOWERING_CONFIRMED' for r in records) == 0


def test_overlay_preserves_frozen_headline_and_rerun_gate():
    inventory = json.loads((OVERLAY / "baseline_inventory.json").read_text())
    decision = json.loads((OVERLAY / "rerun_decision.json").read_text())
    assert inventory['counts']['current_reports'] == 1271
    assert inventory['counts']['current_invalid'] == 291
    assert inventory['counts']['current_nadc'] == 118
    assert inventory['counts']['baseline_reports'] == 512
    assert inventory['counts']['baseline_kni'] == {'K': 312, 'N': 105, 'I': 95}
    assert inventory['headline']['current_precision']['numerator'] == 980
    assert inventory['headline']['current_precision']['denominator'] == 1271
    assert decision['decision'] == 'NO_RERUN'
    assert decision['method_judge_provider_executed'] is False


def test_overlay_keeps_nadc_baseline_boundary_explicit():
    """Baseline v3 lacks the current-only NADC subtype; zero is bookkeeping only."""

    summary = json.loads((OVERLAY / "i_attribution_summary_v1.json").read_text())
    nadc = summary["precision_gap"]["component_rates"]["NADC"]
    assert nadc["baseline_classification_status"] == (
        "not_classified_in_baseline_v3_current_only_subtype"
    )
    assert nadc["baseline_rate_percent"] is None
    assert nadc["delta_rate_pp"] is None
    assert nadc["mechanical_zero_assumption"]["delta_rate_pp"] == 9.284
    assert summary["aggregate_metrics"]["confirmed_method_owned_invalid_total"]["numerator"] == 110
    assert summary["counts"].get("ATTRIBUTION_INDETERMINATE") == 8
    assert summary["counts"].get("CONVERSION_LOWERING_CONFIRMED", 0) == 0
