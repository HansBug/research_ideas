from __future__ import annotations

from pipeline.evidence_discovery.reporting.paired_comparison import (
    DifferenceRow,
    PairedComparisonArtifact,
    _s2_changes,
    _s2_summary_line,
)


def _receipt(
    verdict: str,
    *,
    report_ids: list[str] | None = None,
    expected_ids: list[str] | None = None,
) -> dict[str, object]:
    """Build an S2 inventory row with canonical carrier and audit attribution."""

    return {
        "scope_type": "closed_fcstm",
        "verdict": verdict,
        "terminal_state": "completed",
        "carrier": {
            "scope": "closed_fcstm",
            "source": "Root::Source",
            "target": "Root::Target",
            "transition": None,
            "element_refs": ["state:Root::Source", "state:Root::Target"],
        },
        "report_ids": report_ids or [],
        "expected_ids": expected_ids or [],
        "reason": "Provider-free fixture receipt.",
        "basis": "Exact canonical carrier fixture.",
    }


def test_s2_comparison_counts_only_shared_carrier_verdict_changes_as_flips() -> None:
    """A changed verdict requires the same exact canonical carrier on both sides."""

    before = {"shared": _receipt("violation"), "removed": _receipt("satisfied")}
    after = {"shared": _receipt("satisfied"), "introduced": _receipt("violation")}

    flips, before_only, after_only, denominator = _s2_changes(before, after)

    assert [row.key for row in flips] == ["shared"]
    assert denominator == 1
    assert flips[0].before["verdict"] == "violation"
    assert flips[0].after["verdict"] == "satisfied"
    assert [row.key for row in before_only] == ["removed"]
    assert [row.key for row in after_only] == ["introduced"]


def test_s2_comparison_keeps_single_side_receipt_attribution_outside_flips() -> None:
    """Introduced and removed receipts retain audit links without becoming verdict flips."""

    before = {"removed": _receipt("violation", report_ids=["before-report"], expected_ids=["EIS-0001-01"])}
    after = {"introduced": _receipt("satisfied", report_ids=["after-report"], expected_ids=["EIS-0002-01"])}

    flips, before_only, after_only, denominator = _s2_changes(before, after)

    assert flips == []
    assert denominator == 0
    assert after_only[0].after["report_ids"] == ["after-report"]
    assert after_only[0].after["expected_ids"] == ["EIS-0002-01"]
    assert before_only[0].before["report_ids"] == ["before-report"]
    assert before_only[0].before["expected_ids"] == ["EIS-0001-01"]
    assert "not a same-input verdict comparison" in after_only[0].reason
    assert "not a same-input verdict comparison" in before_only[0].reason


def test_s2_comparison_ignores_same_verdict_metadata_differences() -> None:
    """Changed report attribution alone is not an S2 semantic verdict change."""

    before = {"shared": _receipt("violation", report_ids=["before-report"])}
    after = {"shared": _receipt("violation", report_ids=["after-report"])}

    flips, before_only, after_only, denominator = _s2_changes(before, after)

    assert flips == []
    assert denominator == 1
    assert before_only == []
    assert after_only == []


def test_s2_comparison_uses_the_intersection_as_the_same_input_denominator() -> None:
    """Only shared typed carrier keys contribute to the same-input denominator."""

    before = {"same": _receipt("violation"), "before": _receipt("satisfied")}
    after = {"same": _receipt("violation"), "after": _receipt("satisfied")}

    flips, before_only, after_only, denominator = _s2_changes(before, after)

    assert denominator == 1
    assert flips == []
    assert [row.key for row in before_only] == ["before"]
    assert [row.key for row in after_only] == ["after"]


def test_s2_summary_uses_the_json_category_counts_without_renaming_one_sided_rows() -> None:
    """The concise Chinese output mirrors the machine-readable three-way partition."""

    row = DifferenceRow(key="fixture", before=None, after=None, reason="fixture reason", basis="fixture basis")
    artifact = PairedComparisonArtifact.model_construct(
        matched_input_verdict_flips=[row],
        matched_input_carrier_count=3,
        before_only_carriers=[row, row],
        after_only_carriers=[row, row, row],
    )

    line = _s2_summary_line(artifact)

    assert "matched-input verdict flips: 1/3" in line
    assert "before-only carriers: 2" in line
    assert "after-only carriers: 3" in line
    assert "introduced" not in line
    assert "removed" not in line
