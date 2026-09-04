from __future__ import annotations

from pathlib import Path

from paper_stm_evaluation.publication_w_audit import recompute_publication_w


PAPER_ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = PAPER_ROOT / "final_results" / "v60_current_vs_x1v2_baseline"
CATALOG = PAPER_ROOT / "related_work" / "provenance" / "current_source_catalog.json"


def test_publication_w_is_report_level_and_preserves_frozen_hit_membership() -> None:
    """Only publication W changes; reports and FULL-hit membership stay frozen."""

    audit = recompute_publication_w(ARCHIVE, CATALOG)

    assert audit["execution"] == {
        "provider_calls": 0,
        "backend_reexecutions": 0,
        "method_reruns": 0,
        "judge_reruns": 0,
        "frozen_result_mutations": 0,
    }
    assert audit["report_level"]["final_publication_distribution"] == {"W0": 0, "W1": 854, "W2": 417}
    assert audit["full_hit_projection"]["historical_runtime_distribution"] == {"W0": 0, "W1": 113, "W2": 197}
    assert audit["full_hit_projection"]["source_binding_only_projection"] == {"W0": 0, "W1": 142, "W2": 168}
    assert audit["full_hit_projection"]["final_publication_projection"] == {"W0": 0, "W1": 142, "W2": 168}
    assert audit["full_hit_projection"]["final_publication_projection"]["W2"] >= 150
    assert audit["invariants"] == {
        "report_count_unchanged": True,
        "full_hit_count_unchanged": True,
        "semantic_fields_unchanged": True,
        "full_membership_unchanged": True,
        "publication_w2_full_hit_floor": True,
    }
