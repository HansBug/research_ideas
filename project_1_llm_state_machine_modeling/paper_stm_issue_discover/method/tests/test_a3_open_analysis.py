"""Zero expected issues skip relations; nonempty denominators still require coverage."""
from pathlib import Path
import pytest


def test_relation_coverage_accepts_only_the_empty_denominator_skip(monkeypatch):
    scripts = Path(__file__).resolve().parents[2] / "discover_matrix/docs/generations/a3_20260910"
    monkeypatch.syspath_prepend(str(scripts))
    from analyze_open_judge import verify_relation_coverage

    empty = {"responses": [], "backend_invalid_report_ids": []}
    verify_relation_coverage(empty, {"R0001"}, set())
    with pytest.raises(AssertionError):
        verify_relation_coverage(empty, {"R0001"}, {"E1"})
    covered = {"responses": [{"report_id": "R0001"}], "backend_invalid_report_ids": ["R0002"]}
    verify_relation_coverage(covered, {"R0001", "R0002"}, {"E1"})
    with pytest.raises(AssertionError):
        verify_relation_coverage(covered, {"R0001"}, {"E1"})
