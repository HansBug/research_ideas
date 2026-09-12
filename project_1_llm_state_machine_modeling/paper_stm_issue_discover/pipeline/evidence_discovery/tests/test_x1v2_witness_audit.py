from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.reporting.x1v2_witness_audit import (
    FindingWitnessAudit,
    FindingWitnessAdjudication,
    FullHitWitnessRow,
    ManualWitnessReview,
    PostReviewCorrection,
    SupportingReportWitness,
    X1v2FullHitMaxWitnessAudit,
    X1v2WitnessAdjudicationLog,
    X1v2WitnessLevelAudit,
    X1v2WitnessReviewPacket,
    sha256_text,
    validate_post_review_correction_keys,
    validate_x1v2_witness_audit_artifacts,
)


def _review(level: str, *, reviewer: str = "reviewer") -> dict[str, object]:
    """Build a finding-specific manual-review fixture without any automated label inference."""

    return {
        "reviewer_id": reviewer,
        "witness_level": level,
        "concrete_locations": ["StateA --> StateB : event"] if level != "W0" else [],
        "executable_object": None,
        "evaluation_receipt": None,
        "evaluated_artifact_hash": None,
        "terminal_result": None,
        "reason": f"{reviewer} independently reviewed a concrete fixture for {level}.",
        "basis": f"raw fixture pointer for {reviewer} and {level}.",
    }


def _support(level: str = "W1") -> SupportingReportWitness:
    """Create one FULL-supporting report witness fixture."""

    return SupportingReportWitness(
        original_report_id="0000:r1:baseline_issue_1",
        witness_level=level,
        audit_key="0000:r1:0000:r1:baseline_issue_1",
        reason="The fixture Judge outcome lists this report as FULL support.",
        basis="frozen expected_outcomes[0].full_report_ids fixture.",
    )


def test_manual_w1_requires_human_identified_concrete_location() -> None:
    """A W1 record is structurally incomplete without a reviewer-supplied location."""

    with pytest.raises(ValueError, match="W1 requires"):
        ManualWitnessReview.model_validate({**_review("W1"), "concrete_locations": []})


def test_manual_w2_requires_original_execution_evidence() -> None:
    """A claimed W2 cannot omit the original object, receipt, artifact hash, or result."""

    with pytest.raises(ValueError, match="W2 requires"):
        ManualWitnessReview.model_validate(_review("W2"))


def test_manual_w0_w1_cannot_smuggle_a_post_hoc_execution_receipt() -> None:
    """A non-W2 manual label must not carry W2-only execution evidence fields."""

    with pytest.raises(ValueError, match="W0/W1 cannot"):
        ManualWitnessReview.model_validate({**_review("W1"), "evaluation_receipt": "later Judge receipt"})


def test_full_hit_witness_row_excludes_partial_and_none_rows_from_max_witness() -> None:
    """Only FULL relations may retain a max W derived from full_report_ids."""

    with pytest.raises(ValueError, match="PARTIAL/NONE"):
        FullHitWitnessRow(
            pair_id="0000",
            round=1,
            expected_id="EIS-0000-01",
            relation="PARTIAL",
            full_report_ids=(),
            supporting_reports=(_support(),),
            max_witness_level="W1",
            reason="Invalid fixture.",
            basis="Invalid fixture.",
        )


def test_full_hit_max_counts_close_over_full_denominator() -> None:
    """The hit-level summary must count every and only FULL expected row exactly once."""

    full = FullHitWitnessRow(
        pair_id="0000",
        round=1,
        expected_id="EIS-0000-01",
        relation="FULL",
        full_report_ids=("0000:r1:baseline_issue_1",),
        supporting_reports=(_support(),),
        max_witness_level="W1",
        reason="FULL fixture uses only its listed full_report_ids.",
        basis="frozen expected_outcomes[0].full_report_ids fixture.",
    )
    none = FullHitWitnessRow(
        pair_id="0000",
        round=1,
        expected_id="EIS-0000-02",
        relation="NONE",
        full_report_ids=(),
        supporting_reports=(),
        max_witness_level=None,
        reason="NONE fixture stays outside the FULL-hit denominator.",
        basis="frozen expected_outcomes[1] fixture.",
    )
    audit = X1v2FullHitMaxWitnessAudit(
        expected_row_count=2,
        full_row_count=1,
        overall_full_hit_max_counts={"W0": 0, "W1": 1, "W2": 0},
        l2_full_hit_max_counts={"W0": 0, "W1": 1, "W2": 0},
        w2_all_expected_count=0,
        rows=(full, none),
        reason="Fixture follows the FULL-only aggregation rule.",
        basis="Frozen expected-outcome fixture and manual report review fixture.",
    )

    assert audit.full_row_count == 1
    assert audit.overall_full_hit_max_counts == {"W0": 0, "W1": 1, "W2": 0}


def test_final_audit_requires_independent_reviewer_identity() -> None:
    """A second pass cannot be presented as independent when it uses the primary reviewer ID."""

    with pytest.raises(ValueError, match="reviewer identifiers must differ"):
        FindingWitnessAudit.model_validate({
            "work_item": {
                "audit_key": "0000:r1:0000:r1:baseline_issue_1",
                "pair_id": "0000",
                "round": 1,
                "original_report_id": "0000:r1:baseline_issue_1",
                "original_finding_index": 0,
                "method_record_repository_path": "raw/record.json",
                "method_record_sha256": "sha256:fixture",
                "issue": "specific finding",
                "where": "StateA",
                "finding_reason": "fixture reason",
                "issue_sha256": "sha256:issue",
                "where_sha256": "sha256:where",
                "finding_reason_sha256": "sha256:reason",
                "finding_json_pointer": "/parsed_output/issues/0",
                "natural_language": {"repository_path": "reference/nl.txt", "sha256": "sha256:nl", "reason": "fixture", "basis": "fixture"},
                "plantuml": {"repository_path": "reference/model.puml", "sha256": "sha256:model", "reason": "fixture", "basis": "fixture"},
                "judge_association": {"validity": "VALID_KNOWN", "full_ledger_ids": [], "partial_ledger_ids": [], "judge_pair_result_path": "raw/judge.json", "judge_pair_result_sha256": "sha256:judge", "reason": "link only", "basis": "fixture"},
                "reason": "fixture work item",
                "basis": "fixture work item",
            },
            "primary_review": _review("W1", reviewer="same-reviewer"),
            "secondary_review": _review("W1", reviewer="same-reviewer"),
            "disagreement": False,
            "disagreement_detail": None,
            "final_witness_level": "W1",
            "final_concrete_locations": ["StateA --> StateB : event"],
            "executable_object": None,
            "evaluation_receipt": None,
            "evaluated_artifact_hash": None,
            "terminal_result": None,
            "final_reason": "Both fixture reviews agree on W1.",
            "final_basis": "Fixture decisions.",
            "adjudicator_id": None,
        })


def test_manual_review_packet_rejects_judge_association() -> None:
    """A blinded packet cannot carry Judge linkage even when it carries no W label."""

    work_item = {
        "audit_key": "0000:r1:0000:r1:baseline_issue_1",
        "pair_id": "0000",
        "round": 1,
        "original_report_id": "0000:r1:baseline_issue_1",
        "original_finding_index": 0,
        "method_record_repository_path": "raw/record.json",
        "method_record_sha256": "sha256:fixture",
        "issue": "specific finding",
        "where": "StateA",
        "finding_reason": "fixture reason",
        "issue_sha256": "sha256:issue",
        "where_sha256": "sha256:where",
        "finding_reason_sha256": "sha256:reason",
        "finding_json_pointer": "/parsed_output/issues/0",
        "natural_language": {"repository_path": "reference/nl.txt", "sha256": "sha256:nl", "reason": "fixture", "basis": "fixture"},
        "plantuml": {"repository_path": "reference/model.puml", "sha256": "sha256:model", "reason": "fixture", "basis": "fixture"},
        "judge_association": {"validity": "VALID_KNOWN", "full_ledger_ids": [], "partial_ledger_ids": [], "judge_pair_result_path": "raw/judge.json", "judge_pair_result_sha256": "sha256:judge", "reason": "link only", "basis": "fixture"},
        "reason": "fixture work item",
        "basis": "fixture work item",
    }
    with pytest.raises(ValueError, match="must not expose a Judge association"):
        X1v2WitnessReviewPacket(
            finding_count=1,
            work_items=(work_item,),
            reason="Fixture packet.",
            basis="Fixture records.",
        )


def test_adjudication_log_rejects_duplicate_decisions() -> None:
    """Pane5's decision log cannot hide duplicated resolutions under one count."""

    adjudication = FindingWitnessAdjudication(
        audit_key="0000:r1:0000:r1:baseline_issue_1",
        adjudicator_id="pane5",
        final_witness_level="W1",
        final_concrete_locations=("StateA --> StateB : event",),
        executable_object=None,
        evaluation_receipt=None,
        evaluated_artifact_hash=None,
        terminal_result=None,
        reason="The fixture retains a concrete transition but no runtime witness.",
        basis="Primary and secondary fixture decisions plus raw fixture pointer.",
    )
    with pytest.raises(ValueError, match="one unique decision"):
        X1v2WitnessAdjudicationLog(
            finding_count=1,
            disagreement_count=2,
            adjudications=(adjudication, adjudication),
            reason="Fixture log.",
            basis="Fixture decisions.",
        )


def test_post_review_correction_requires_a_changed_consensus_level() -> None:
    """A post-review record cannot be used to decorate an unchanged agreement."""

    with pytest.raises(ValueError, match="must change"):
        PostReviewCorrection(
            audit_key="0036:r1:0036:r1:baseline_issue_4",
            independent_review_path="reviews/09_x1v2_witness_blind_semantic_metric_review.md",
            adjudicator_id="pane5-main",
            original_consensus_witness_level="W1",
            corrected_final_witness_level="W1",
            final_concrete_locations=("StateA",),
            executable_object=None,
            evaluation_receipt=None,
            evaluated_artifact_hash=None,
            terminal_result=None,
            reason="Fixture correction.",
            basis="reviews/09_x1v2_witness_blind_semantic_metric_review.md; fixture evidence.",
        )


def test_post_review_correction_allowlist_rejects_an_unreviewed_key() -> None:
    """No agreeing finding can be silently relabelled outside the documented correction key."""

    correction = PostReviewCorrection(
        audit_key="0000:r1:0000:r1:baseline_issue_1",
        independent_review_path="reviews/fixture.md",
        adjudicator_id="pane5-main",
        original_consensus_witness_level="W1",
        corrected_final_witness_level="W0",
        final_concrete_locations=(),
        executable_object=None,
        evaluation_receipt=None,
        evaluated_artifact_hash=None,
        terminal_result=None,
        reason="Fixture correction.",
        basis="reviews/fixture.md; fixture evidence.",
    )
    with pytest.raises(ValueError, match="allowlist"):
        validate_post_review_correction_keys(
            {correction.audit_key: correction},
            {correction.audit_key},
        )


def test_post_review_correction_rejects_non_archive_review_path() -> None:
    """A correction cannot cite an arbitrary path instead of a stable archive review."""

    with pytest.raises(ValueError, match="archive-relative reviews/"):
        PostReviewCorrection(
            audit_key="0036:r1:0036:r1:baseline_issue_4",
            independent_review_path="/tmp/review.md",
            adjudicator_id="pane5-main",
            original_consensus_witness_level="W1",
            corrected_final_witness_level="W0",
            final_concrete_locations=(),
            executable_object=None,
            evaluation_receipt=None,
            evaluated_artifact_hash=None,
            terminal_result=None,
            reason="Fixture correction.",
            basis="/tmp/review.md; fixture evidence.",
        )


def test_archived_x1v2_manual_witness_audit_is_complete_and_full_only() -> None:
    """The committed archive keeps the dual-reviewed baseline W axis reproducible offline."""

    repository_root = Path(__file__).resolve().parents[5]
    archive = repository_root / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover" / "final_results" / "v60_current_vs_x1v2_baseline"
    statistics = validate_x1v2_witness_audit_artifacts(archive, repository_root)
    assert statistics["finding_level"] == {
        "counts": {"W0": 1, "W1": 511, "W2": 0},
        "denominator": 512,
    }
    assert statistics["full_hit_max_witness"] == {
        "counts": {"W0": 0, "W1": 211, "W2": 0},
        "denominator": 211,
    }
    assert statistics["l2_full_hit_max_witness"] == {
        "counts": {"W0": 0, "W1": 46, "W2": 0},
        "denominator": 46,
    }
    assert statistics["w2_all_expected"] == {"count": 0, "denominator": 435, "rate": 0.0}
    audit = X1v2WitnessLevelAudit.model_validate_json((archive / "derived" / "x1v2_witness_level_audit.json").read_text(encoding="utf-8"))
    hit_audit = X1v2FullHitMaxWitnessAudit.model_validate_json((archive / "derived" / "x1v2_full_hit_max_witness_audit.json").read_text(encoding="utf-8"))
    assert audit.primary_review_coverage == audit.secondary_review_coverage == audit.finding_count == 512
    assert audit.disagreement_count == 0
    assert audit.post_review_correction_count == 1
    assert all(record.final_witness_level != "W2" for record in audit.records)
    assert hit_audit.expected_row_count == 435
    assert hit_audit.full_row_count == 211
    assert all(row.max_witness_level is None for row in hit_audit.rows if row.relation != "FULL")


def test_archived_review_packet_preserves_raw_finding_text_byte_for_value() -> None:
    """Reviewer-visible issue, where, and reason text remain byte-identical to the frozen raw record."""

    repository_root = Path(__file__).resolve().parents[5]
    archive = repository_root / "project_1_llm_state_machine_modeling" / "paper_stm_issue_discover" / "final_results" / "v60_current_vs_x1v2_baseline"
    packet = X1v2WitnessReviewPacket.model_validate_json(
        (archive / "derived" / "x1v2_witness_review_packet.json").read_text(encoding="utf-8")
    )
    item = next(work_item for work_item in packet.work_items if work_item.audit_key == "0050:r3:0050:r3:baseline_issue_1")
    raw = json.loads((archive / "raw" / "x1v2_baseline" / "method" / "run3" / "0050-luna" / "record.json").read_text(encoding="utf-8"))
    finding = raw["parsed_output"]["issues"][item.original_finding_index]
    assert item.issue == finding["issue"]
    assert item.where == finding["where"]
    assert item.finding_reason == finding["reason"]
    assert item.issue_sha256 == sha256_text(finding["issue"])
    assert item.where_sha256 == sha256_text(finding["where"])
    assert item.finding_reason_sha256 == sha256_text(finding["reason"])
