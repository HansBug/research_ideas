from __future__ import annotations

from pipeline.evidence_discovery.reporting.paired_comparison import _s2_changes


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

    flips, introduced, removed = _s2_changes(before, after)

    assert [row.key for row in flips] == ["shared"]
    assert flips[0].before["verdict"] == "violation"
    assert flips[0].after["verdict"] == "satisfied"
    assert [row.key for row in introduced] == ["introduced"]
    assert [row.key for row in removed] == ["removed"]


def test_s2_comparison_keeps_single_side_receipt_attribution_outside_flips() -> None:
    """Introduced and removed receipts retain audit links without becoming verdict flips."""

    before = {"removed": _receipt("violation", report_ids=["before-report"], expected_ids=["EIS-0001-01"])}
    after = {"introduced": _receipt("satisfied", report_ids=["after-report"], expected_ids=["EIS-0002-01"])}

    flips, introduced, removed = _s2_changes(before, after)

    assert flips == []
    assert introduced[0].after["report_ids"] == ["after-report"]
    assert introduced[0].after["expected_ids"] == ["EIS-0002-01"]
    assert removed[0].before["report_ids"] == ["before-report"]
    assert removed[0].before["expected_ids"] == ["EIS-0001-01"]


def test_s2_comparison_ignores_same_verdict_metadata_differences() -> None:
    """Changed report attribution alone is not an S2 semantic verdict change."""

    before = {"shared": _receipt("violation", report_ids=["before-report"])}
    after = {"shared": _receipt("violation", report_ids=["after-report"])}

    flips, introduced, removed = _s2_changes(before, after)

    assert flips == []
    assert introduced == []
    assert removed == []
