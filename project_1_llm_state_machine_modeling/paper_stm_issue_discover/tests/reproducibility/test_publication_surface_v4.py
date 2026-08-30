"""Provider-free checks for the converged Paper1 v4 publication surface."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[4]
PAPER = REPOSITORY / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
ARCHIVE = PAPER / "final_results/v60_current_vs_x1v2_baseline"


def _load(path: Path) -> dict[str, object]:
    """Load one JSON object used by the publication checks."""

    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _sha256(path: Path) -> str:
    """Return the archive-style SHA-256 for one file."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def test_publication_manifest_excludes_proposals_and_archive_only_provenance() -> None:
    """The current publication allowlist omits excluded proposals and absolute provenance records."""

    manifest = _load(ARCHIVE / "publication_manifest.json")
    paths = {str(item["path"]) for item in manifest["included_files"]}
    assert "report/v60_current_vs_x1v2_baseline_v4_cn.md" in paths
    assert not any("manual_adjudication_v3_baseline_ni/proposals/" in path for path in paths)
    assert "derived/manual_adjudication_v3_baseline_ni/reviews/academic_citation_review.md" not in paths
    assert "derived/manual_adjudication_v3_baseline_ni/reviews/numeric_recompute_review_v3.md" not in paths


def test_fair_manifest_hashes_every_publication_surface_file() -> None:
    """Fair validation cannot pass while a paper-facing document hash is stale."""

    manifest = _load(ARCHIVE / "derived/fair_comparison_v4/fair_comparison_manifest_v4.json")
    for relative_path, digest in manifest["publication_surface"].items():
        assert _sha256(ARCHIVE / relative_path) == digest


def test_current_i_diagnostic_clusters_are_traceable_but_not_defects() -> None:
    """All current invalid reports map once to diagnostic IDs excluded from precision."""

    document = _load(
        ARCHIVE
        / "derived/manual_adjudication_v4_current_reaudit/current_i_diagnostic_clusters_v4.json"
    )
    assert document["report_count"] == len(document["report_to_cluster"]) == 291
    assert document["diagnostic_cluster_count"] == len(document["clusters"]) == 189
    members = [report_id for cluster in document["clusters"] for report_id in cluster["member_report_ids"]]
    assert len(members) == len(set(members)) == 291
    assert all(not cluster["substantive_defect"] for cluster in document["clusters"])
    assert all(not cluster["grouped_precision_unit"] for cluster in document["clusters"])


def test_inventory_treats_current_protocol_and_absolute_reviews_correctly() -> None:
    """The current protocol is active while two absolute-path reviews remain archive provenance."""

    inventory = _load(ARCHIVE / "reviews/publication_docs_inventory_v4.json")
    rows = {str(row["path"]): row for row in inventory["rows"]}
    current_protocol = rows[
        "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v4_current_reaudit/protocol_freeze_v4_current_reaudit.md"
    ]
    assert "issue-189-195-manual-evidence-v2" not in current_protocol["old_protocols_found"]
    for relative_path in (
        "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/reviews/academic_citation_review.md",
        "final_results/v60_current_vs_x1v2_baseline/derived/manual_adjudication_v3_baseline_ni/reviews/numeric_recompute_review_v3.md",
    ):
        row = rows[relative_path]
        assert row["historical_or_archive"] is True
        assert row["publication_surface"] is False
        assert row["recommended_action"] == "archive provenance"


def test_tracked_document_inventory_has_no_broken_relative_links() -> None:
    """Code examples are ignored and every real tracked Markdown target resolves."""

    inventory = _load(ARCHIVE / "reviews/publication_docs_inventory_v4.json")
    broken = {
        str(row["path"]): row["broken_relative_links"]
        for row in inventory["rows"]
        if row["broken_relative_links"]
    }
    assert broken == {}


def test_only_current_predicate_and_n_counts_appear_in_the_headline_report() -> None:
    """Historical v2 and witness-audit counts stay out of the sole paper headline."""

    report = (ARCHIVE / "report/v60_current_vs_x1v2_baseline_v4_cn.md").read_text(
        encoding="utf-8"
    )
    assert "| N reports | 231 | 105 |" in report
    assert "132 / 105" not in report
    assert "12/15 个 planned-scope" not in report
    assert "1237 条 terminal receipt" not in report
    assert "| **合计** |  | **118**" not in report
    assert "825/1271 = 64.91%" in report
    assert "303/825 = 36.73%" in report


def test_publication_summaries_exclude_historical_witness_audit_fields() -> None:
    """Current and fair summaries expose only the two report-bound predicate ratios."""

    current = _load(
        ARCHIVE / "derived/manual_adjudication_v4_current_reaudit/summary_v4.json"
    )["metrics"]["predicate_usage"]
    fair = _load(ARCHIVE / "derived/fair_comparison_v4/combined_summary_v4.json")
    fair_current = fair["sides"]["v60_current"]["predicate"]
    expected_fields = {
        "status",
        "report_bound_binding",
        "legacy_semantic_hit_marker_among_report_bound_bindings",
        "naming_boundary",
    }
    assert set(current) == expected_fields
    assert set(fair_current) == expected_fields
    assert fair["sides"]["x1v2_baseline"]["predicate"]["status"] == "not_applicable"

    for path in (
        ARCHIVE / "derived/manual_adjudication_v4_current_reaudit/summary_v4.json",
        ARCHIVE / "derived/manual_adjudication_v4_current_reaudit/recomputed_summary_v4.json",
        ARCHIVE / "derived/fair_comparison_v4/combined_summary_v4.json",
        ARCHIVE / "derived/fair_comparison_v4/recomputed_summary_v4.json",
    ):
        text = path.read_text(encoding="utf-8")
        assert "method_terminal_execution" not in text
        assert "registered_report_bound_predicate_ids" not in text
        assert "report_bound_completed_receipts" not in text
