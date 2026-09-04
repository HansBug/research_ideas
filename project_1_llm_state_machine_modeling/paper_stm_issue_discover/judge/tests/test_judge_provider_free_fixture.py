"""Provider-free smoke test shipped with the standalone Semantic Judge release."""

from __future__ import annotations

import json
import re
import sys

import pytest

from paper_stm_judge import cli
from paper_stm_judge.models import (
    A0Subtype,
    DefectAdjudication,
    DefectClass,
    DefectTier,
    FrozenValidityCertificate,
    ValidityGateStatus,
    ValidityResponse,
    a0_subtype_of,
    defect_tier_of,
    minimum_evidence_status_of,
)
from paper_stm_judge.protocol import (
    JUDGE_ALGORITHM_VERSION,
    PROMPT_VERSION,
    PROTOCOL_VERSION,
    VALIDITY_SYSTEM_PROMPT,
    verify_snapshot,
)
from paper_stm_judge.scale_audit import _algorithm_source_hash


def test_packaged_protocol_and_neutral_dependencies_load_without_method() -> None:
    """The independent Judge verifies its frozen protocol without importing method code."""

    method_modules_before = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    verify_snapshot()
    assert _algorithm_source_hash().startswith("sha256:")
    method_modules_after = {
        name for name in sys.modules if name == "paper_stm_method" or name.startswith("paper_stm_method.")
    }
    assert method_modules_after == method_modules_before


def test_release_code_provenance_fails_closed_without_git_or_manifest(monkeypatch) -> None:
    """A source-less Judge cannot begin a live run without verified package provenance."""

    monkeypatch.setattr(cli, "_source_repository_root", lambda: None)
    monkeypatch.setattr(cli, "_release_source_commit", lambda: None)
    with pytest.raises(RuntimeError, match="valid installed release manifest"):
        cli._code_commit()


def test_release_code_provenance_accepts_verified_embedded_manifest(monkeypatch) -> None:
    """A verified installed manifest supplies the exact Judge code commit offline."""

    commit = "a" * 40
    monkeypatch.setattr(cli, "_source_repository_root", lambda: None)
    monkeypatch.setattr(cli, "_release_source_commit", lambda: commit)
    assert cli._code_commit() == commit


def test_v38_prompt_states_author_source_basis_and_closed_defect_classes() -> None:
    """The current prompt makes author-source truth and the closed defect class explicit."""

    assert PROTOCOL_VERSION.endswith("issue-189-clarification.v3.11")
    assert JUDGE_ALGORITHM_VERSION == "semantic-judge.two-stage.v3.11"
    assert PROMPT_VERSION == "semantic-judge.two-stage-prompt.v11"
    for required in (
        "The author-source work product is exactly two artifacts",
        "A derived representation may corroborate a reading of the author source",
        "A0_FALSE_POSITIVE",
        "A0_NOT_A_DEFECT_CLAIM",
        "D2 and D1 satisfy it and D0 and both A0 classes refute it",
        "Classify a clause as INDISPENSABLE_MECHANISM only when the conclusion collapses without it",
        "is never A0_FALSE_POSITIVE",
        "Where obligations come from.",
        "Read a free-text or compound claim for its load-bearing concern",
        "it never creates structure",
        "Answer this question on the report's load-bearing concern, not on its literal wording",
        "can never be entered from the root",
    ):
        assert required in VALIDITY_SYSTEM_PROMPT, required


def test_prompts_carry_no_pair_ledger_or_arm_identifiers() -> None:
    """Anonymity: no frozen pair ID, ledger ID prefix, or arm name may leak into any prompt."""

    from paper_stm_judge.protocol import (
        RELATION_ARBITRATION_INSTRUCTION,
        RELATION_PRIMARY_INSTRUCTION,
        RELATION_SYSTEM_PROMPT,
        VALIDITY_ARBITRATION_INSTRUCTION,
        VALIDITY_PRIMARY_INSTRUCTION,
    )

    prompts = (
        VALIDITY_SYSTEM_PROMPT,
        VALIDITY_PRIMARY_INSTRUCTION,
        VALIDITY_ARBITRATION_INSTRUCTION,
        RELATION_SYSTEM_PROMPT,
        RELATION_PRIMARY_INSTRUCTION,
        RELATION_ARBITRATION_INSTRUCTION,
    )
    for text in prompts:
        assert re.search(r"\b00[0-5][0-9]\b", text) is None, "frozen pair ID leaked into a prompt"
        assert re.search(r"\b(EIS|INS|VU|DIFF)-\d", text) is None, "ledger ID leaked into a prompt"
        for banned in ("X1v2", "our method", "baseline arm", "R45"):
            assert banned not in text, banned


def test_defect_class_helpers_close_the_d_a_boundary() -> None:
    """D2/D1 satisfy the minimum-evidence gate; D0 and both A0 exits refute it."""

    assert minimum_evidence_status_of(DefectClass.D2) == ValidityGateStatus.SATISFIED
    assert minimum_evidence_status_of(DefectClass.D1) == ValidityGateStatus.SATISFIED
    for invalid in (
        DefectClass.D0,
        DefectClass.A0_FALSE_POSITIVE,
        DefectClass.A0_NOT_A_DEFECT_CLAIM,
    ):
        assert minimum_evidence_status_of(invalid) == ValidityGateStatus.REFUTED
    assert defect_tier_of(DefectClass.D0) == DefectTier.D0
    assert defect_tier_of(DefectClass.A0_FALSE_POSITIVE) is None
    assert a0_subtype_of(DefectClass.A0_NOT_A_DEFECT_CLAIM) == A0Subtype.NOT_A_DEFECT_CLAIM
    assert a0_subtype_of(DefectClass.D2) is None
    assert ValidityResponse.model_fields["defect_adjudication"].annotation is DefectAdjudication
    assert "minimum_evidence_gate" not in ValidityResponse.model_fields
    assert "defect_adjudication" in FrozenValidityCertificate.model_fields


def test_report_filter_restricts_reports_and_keeps_anonymous_ids() -> None:
    """The local allowlist keeps anonymous IDs stable and rejects unknown IDs."""

    from paper_stm_judge.models import AdapterAudit, AdapterIdMap, CandidateReport

    raw = json.dumps(
        {"0004": ["0004:r1:issue:5", "0004:r2:issue:1"], "0059": ["0059:r1:issue:10"]}
    ).encode("utf-8")
    report_filter = cli.load_report_filter(raw)
    assert cli.round_filter_ids(report_filter, "0004", 1) == frozenset({"0004:r1:issue:5"})
    assert cli.round_filter_ids(report_filter, "0004", 3) == frozenset()
    assert cli.round_filter_ids(report_filter, "0059", 1) == frozenset({"0059:r1:issue:10"})
    with pytest.raises(ValueError, match="matching pair/round prefix"):
        cli.load_report_filter(json.dumps({"0004": ["0059:r1:issue:1"]}).encode("utf-8"))

    def report(index: int) -> CandidateReport:
        return CandidateReport(
            report_id=f"R{index:04d}",
            claim=f"claim {index}",
            where=None,
            property=None,
            violated_obligation=None,
            expected=None,
            observed=None,
            reason=f"reason {index}",
            basis=None,
            source_refs=(),
            evidence=(),
        )

    reports = (report(1), report(2), report(3))
    audit = AdapterAudit(
        source_format="evidence_discovery_release",
        source_path="/dev/null",
        source_hash="sha256:" + "0" * 64,
        report_id_map=(
            AdapterIdMap(anonymous_id="R0001", original_id="0004:r1:issue:1"),
            AdapterIdMap(anonymous_id="R0002", original_id="0004:r1:issue:5"),
            AdapterIdMap(anonymous_id="R0003", original_id="0004:r1:issue:9"),
        ),
        expected_id_map=(),
        projected_field_names=("claim", "reason"),
        excluded_field_names=(),
        reason="fixture",
        basis="fixture",
    )
    kept, kept_audit = cli.apply_report_filter(
        reports, audit, cli.round_filter_ids(report_filter, "0004", 1)
    )
    assert tuple(item.report_id for item in kept) == ("R0002",)
    assert tuple(row.anonymous_id for row in kept_audit.report_id_map) == ("R0002",)
    assert "restricted judging to 1 of 3" in kept_audit.reason
    with pytest.raises(ValueError, match="absent from the adapted source"):
        cli.apply_report_filter(reports, audit, frozenset({"0004:r1:issue:99"}))


def test_majority_reading_selection_is_strict_and_earliest() -> None:
    """Strict-majority defect class wins and the earliest such reading is kept; ties fall back to arbitration."""

    from paper_stm_judge.runner import select_majority_reading

    assert select_majority_reading([DefectClass.D1, DefectClass.D0, DefectClass.D1]) == 0
    assert select_majority_reading([DefectClass.D0, DefectClass.D1, DefectClass.D1]) == 1
    assert select_majority_reading([DefectClass.D0, DefectClass.D1, DefectClass.D2]) is None
    assert select_majority_reading([DefectClass.D0, DefectClass.D1]) is None
    assert select_majority_reading([DefectClass.D2, DefectClass.D2, DefectClass.D2]) == 0
