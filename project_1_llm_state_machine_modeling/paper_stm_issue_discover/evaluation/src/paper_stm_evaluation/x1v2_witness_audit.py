"""Provider-free manual W0/W1/W2 audit support for frozen X1v2 findings.

This module deliberately never infers a witness level from text, Judge validity,
expected relations, field presence, or a predicate mapping.  It only materializes
the frozen review universe, validates two independent human reviews, and derives
report- and hit-level summaries from the submitted manual labels.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


WITNESS_AUDIT_SCHEMA = "paper1.x1v2-witness-level-audit.v3"
WITNESS_PACKET_SCHEMA = "paper1.x1v2-witness-review-packet.v2"
WITNESS_ADJUDICATION_SCHEMA = "paper1.x1v2-witness-adjudications.v2"
INPUT_CLOSURE_SCHEMA = "paper1.x1v2-input-closure.v1"
WitnessLevel = Literal["W0", "W1", "W2"]
MatchRelation = Literal["FULL", "PARTIAL", "NONE"]
Validity = Literal["VALID_KNOWN", "VALID_NOVEL", "INVALID"]

# This allowlist constrains a documented evaluator correction, not method behavior.
POST_REVIEW_CORRECTION_ALLOWLIST = frozenset({"0036:r1:0036:r1:baseline_issue_4"})


def _load_json(path: Path) -> dict[str, object]:
    """Load one JSON-object artifact without accepting an untyped top-level list."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: object) -> None:
    """Persist deterministic UTF-8 JSON for a derived, evaluator-only artifact."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    """Return a prefixed SHA-256 digest for an immutable source or record file."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def sha256_text(value: str) -> str:
    """Return a prefixed SHA-256 digest for one frozen finding text field."""

    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


class SourceArtifactReference(BaseModel):
    """Stable archive-relative reference to a frozen source input used in review."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(description="Repository-relative path to the copied immutable input artifact.")
    sha256: str = Field(description="SHA-256 of the exact input bytes checked against the frozen method record.")
    reason: str = Field(description="Why this source artifact is required to review the finding's localization.")
    basis: str = Field(description="Frozen record field and integrity relationship supporting this reference.")


class JudgeAssociation(BaseModel):
    """Frozen Judge linkage attached only after a blinded manual W review completes."""

    model_config = ConfigDict(extra="forbid")

    validity: Validity = Field(description="Frozen Judge report validity, retained only as an orthogonal association.")
    full_ledger_ids: tuple[str, ...] = Field(description="Ledger IDs for which the frozen Judge named this report as FULL support.")
    partial_ledger_ids: tuple[str, ...] = Field(description="Ledger IDs for which the frozen Judge named this report as PARTIAL support.")
    judge_pair_result_path: str = Field(description="Repository-relative path to the composite-selected PairJudgeResult JSON.")
    judge_pair_result_sha256: str = Field(description="SHA-256 that the composite receipt declares for the selected PairJudgeResult.")
    reason: str = Field(description="Why Judge fields are linkage-only and cannot determine the method's W level.")
    basis: str = Field(description="Frozen composite selection and PairJudgeResult fields used for the association.")


class ReviewWorkItem(BaseModel):
    """One frozen X1v2 finding with the complete context required for manual review."""

    model_config = ConfigDict(extra="forbid")

    audit_key: str = Field(description="Stable key composed from pair, round, and original method report ID.")
    pair_id: str = Field(description="Frozen benchmark pair identifier.")
    round: int = Field(description="Frozen X1v2 method round number.", ge=1, le=3)
    original_report_id: str = Field(description="Original arm-generated report identifier used by the frozen Judge.")
    original_finding_index: int = Field(description="Zero-based index of the finding in parsed_output.issues.", ge=0)
    method_record_repository_path: str = Field(description="Repository-relative path to the immutable X1v2 method record JSON.")
    method_record_sha256: str = Field(description="SHA-256 of the exact immutable method record bytes.")
    issue: str = Field(description="Original arm-generated finding claim, preserved for semantic review.")
    where: str = Field(description="Original arm-generated localization text, preserved for semantic review.")
    finding_reason: str = Field(description="Original arm-generated explanation, preserved for semantic review.")
    issue_sha256: str = Field(description="SHA-256 of the original issue text.")
    where_sha256: str = Field(description="SHA-256 of the original where text.")
    finding_reason_sha256: str = Field(description="SHA-256 of the original reason text.")
    finding_json_pointer: str = Field(description="JSON Pointer to this exact finding inside the immutable method record.")
    natural_language: SourceArtifactReference = Field(description="Frozen natural-language requirement artifact available to both human reviewers.")
    plantuml: SourceArtifactReference = Field(description="Frozen PlantUML artifact available to both human reviewers.")
    judge_association: JudgeAssociation | None = Field(
        default=None,
        description="Judge linkage attached after blinded review for hit aggregation; absent from every review packet and decision batch.",
    )
    reason: str = Field(description="Why this work item is an exhaustive, read-only manual-review unit.")
    basis: str = Field(description="Record, input-hash, and composite-selection evidence that identifies this unit.")


class ManualWitnessReview(BaseModel):
    """A single independent human W-level assessment of one frozen finding."""

    model_config = ConfigDict(extra="forbid")

    reviewer_id: str = Field(description="Stable identity of the independent reviewer producing this assessment.", min_length=1)
    witness_level: WitnessLevel = Field(description="Human-assessed W0, W1, or W2 level under the issue #189 semantic definition.")
    concrete_locations: tuple[str, ...] = Field(description="Concrete states, transitions, guards, actions, paths, or source fragments recognized by this reviewer.")
    executable_object: str | None = Field(description="Method-produced executable witness object, required only for a defensible W2 assessment.")
    evaluation_receipt: str | None = Field(description="Original X1v2 runtime receipt proving terminal evaluation, required only for W2.")
    evaluated_artifact_hash: str | None = Field(description="Exact evaluated input-artifact hash, required only for W2.")
    terminal_result: str | None = Field(description="Terminal true/false or equivalent deterministic result, required only for W2.")
    reason: str = Field(description="Finding-specific explanation of the selected level and why the next stronger level is not justified.", min_length=1)
    basis: str = Field(description="Finding-specific raw JSON pointer, input anchor, and artifact-hash evidence supporting the assessment.", min_length=1)

    @model_validator(mode="after")
    def validate_semantic_shape(self) -> "ManualWitnessReview":
        """Enforce only structural consequences of a reviewer-selected witness level."""

        w2_values = (
            self.executable_object,
            self.evaluation_receipt,
            self.evaluated_artifact_hash,
            self.terminal_result,
        )
        if self.witness_level == "W2":
            if not self.concrete_locations or any(value is None or not value.strip() for value in w2_values):
                raise ValueError("W2 requires a location, executable object, receipt, artifact hash, and terminal result")
        elif any(value is not None for value in w2_values):
            raise ValueError("W0/W1 cannot claim a missing X1v2 executable-evaluation witness")
        if self.witness_level == "W1" and not self.concrete_locations:
            raise ValueError("W1 requires at least one reviewer-identified concrete location")
        return self


class PostReviewCorrection(BaseModel):
    """A bounded pane5 correction discovered after two agreeing blind reviews."""

    model_config = ConfigDict(extra="forbid")

    audit_key: str = Field(description="Stable finding key for the one final record corrected after independent post-review.")
    independent_review_path: str = Field(description="Archive-relative reviews/ path to the independent review that identified the consensus-label defect.", min_length=1)
    adjudicator_id: str = Field(description="Pane5 identity responsible for accepting the documented post-review correction.", min_length=1)
    original_consensus_witness_level: WitnessLevel = Field(description="Shared primary and secondary W level before the correction.")
    corrected_final_witness_level: WitnessLevel = Field(description="Final W level accepted after checking the independent review and frozen source evidence.")
    final_concrete_locations: tuple[str, ...] = Field(description="Concrete locations retained in the corrected final decision; empty only for W0.")
    executable_object: str | None = Field(description="Original X1v2 executable object only when the corrected final level is W2.")
    evaluation_receipt: str | None = Field(description="Original terminal-evaluation receipt only when the corrected final level is W2.")
    evaluated_artifact_hash: str | None = Field(description="Exact evaluated-artifact hash only when the corrected final level is W2.")
    terminal_result: str | None = Field(description="Original terminal result only when the corrected final level is W2.")
    reason: str = Field(description="Finding-specific explanation of why the shared review label was corrected under the W definition.", min_length=1)
    basis: str = Field(description="Frozen record/source pointers and independent-review evidence supporting the correction without Judge-derived W evidence.", min_length=1)

    @model_validator(mode="after")
    def validate_correction_shape(self) -> "PostReviewCorrection":
        """Require a real semantic correction and the evidence shape appropriate to its final W level."""

        review_path = Path(self.independent_review_path)
        if review_path.is_absolute() or not review_path.parts or review_path.parts[0] != "reviews" or ".." in review_path.parts:
            raise ValueError("independent_review_path must be an archive-relative reviews/ path")
        if self.original_consensus_witness_level == self.corrected_final_witness_level:
            raise ValueError("post-review correction must change the consensus witness level")
        if self.independent_review_path not in self.basis:
            raise ValueError("post-review correction basis must cite its independent review path")
        values = (self.executable_object, self.evaluation_receipt, self.evaluated_artifact_hash, self.terminal_result)
        if self.corrected_final_witness_level == "W2":
            if not self.final_concrete_locations or any(value is None or not value.strip() for value in values):
                raise ValueError("corrected W2 requires location, object, receipt, artifact hash, and terminal result")
        elif any(value is not None for value in values):
            raise ValueError("corrected W0/W1 cannot carry W2-only execution fields")
        if self.corrected_final_witness_level == "W1" and not self.final_concrete_locations:
            raise ValueError("corrected W1 requires concrete localization")
        return self


class FindingWitnessAudit(BaseModel):
    """Final dual-reviewed and, when necessary, adjudicated W assessment for one finding."""

    model_config = ConfigDict(extra="forbid")

    work_item: ReviewWorkItem = Field(description="Frozen finding context shared by both independent human reviews.")
    primary_review: ManualWitnessReview = Field(description="First independent manual review of the frozen finding.")
    secondary_review: ManualWitnessReview = Field(description="Second independent manual review performed without using the primary verdict as a rule.")
    disagreement: bool = Field(description="Whether primary and secondary reviews selected different W levels.")
    disagreement_detail: str | None = Field(description="Concrete difference between independent assessments, required when disagreement is true.")
    final_witness_level: WitnessLevel = Field(description="Pane5 final level after agreement confirmation or explicit adjudication.")
    final_concrete_locations: tuple[str, ...] = Field(description="Concrete localization accepted in the final audit decision.")
    executable_object: str | None = Field(description="Adjudicated X1v2 executable witness, present only for final W2.")
    evaluation_receipt: str | None = Field(description="Adjudicated original runtime receipt, present only for final W2.")
    evaluated_artifact_hash: str | None = Field(description="Adjudicated evaluated artifact hash, present only for final W2.")
    terminal_result: str | None = Field(description="Adjudicated terminal evaluation result, present only for final W2.")
    final_reason: str = Field(description="Finding-specific final explanation of the W decision and any disagreement resolution.", min_length=1)
    final_basis: str = Field(description="Finding-specific audit pointers and hashes supporting the final decision.", min_length=1)
    adjudicator_id: str | None = Field(description="Pane5 adjudicator identity for a W-level disagreement or documented post-review correction; otherwise null.")
    post_review_correction: PostReviewCorrection | None = Field(
        default=None,
        description="Documented correction allowed only when two agreeing reviews were later shown wrong by an independent frozen-evidence review.",
    )

    @model_validator(mode="after")
    def validate_dual_review_and_final_shape(self) -> "FindingWitnessAudit":
        """Reject missing second reviews, copied reviewers, and incomplete W2 claims."""

        if self.primary_review.reviewer_id == self.secondary_review.reviewer_id:
            raise ValueError("primary and secondary reviewer identifiers must differ")
        if self.primary_review.reason == self.secondary_review.reason and self.primary_review.basis == self.secondary_review.basis:
            raise ValueError("primary and secondary reviews must retain independently written reason and basis")
        levels_differ = self.primary_review.witness_level != self.secondary_review.witness_level
        if self.disagreement != levels_differ:
            raise ValueError("disagreement must exactly reflect whether reviewer witness levels differ")
        if self.disagreement:
            if not self.disagreement_detail or not self.adjudicator_id:
                raise ValueError("a disagreement requires detail and a pane5 adjudicator")
            if self.post_review_correction is not None:
                raise ValueError("a disagreement cannot also use a post-review correction")
        elif self.post_review_correction is None:
            if self.adjudicator_id is not None:
                raise ValueError("an uncorrected agreement must not claim an adjudicator")
            if self.final_witness_level != self.primary_review.witness_level:
                raise ValueError("an uncorrected agreement must retain its shared witness level")
        else:
            correction = self.post_review_correction
            if correction.audit_key != self.work_item.audit_key:
                raise ValueError("post-review correction key must match its final audit record")
            if correction.original_consensus_witness_level != self.primary_review.witness_level:
                raise ValueError("post-review correction must state the shared primary/secondary witness level")
            if correction.corrected_final_witness_level != self.final_witness_level:
                raise ValueError("post-review correction level must equal the final audit level")
            if correction.final_concrete_locations != self.final_concrete_locations:
                raise ValueError("post-review correction locations must equal final audit locations")
            if correction.adjudicator_id != self.adjudicator_id:
                raise ValueError("post-review correction adjudicator must equal final audit adjudicator")
        final_w2_values = (
            self.executable_object,
            self.evaluation_receipt,
            self.evaluated_artifact_hash,
            self.terminal_result,
        )
        if self.final_witness_level == "W2":
            if not self.final_concrete_locations or any(value is None or not value.strip() for value in final_w2_values):
                raise ValueError("final W2 requires location, object, receipt, artifact hash, and terminal result")
        elif any(value is not None for value in final_w2_values):
            raise ValueError("final W0/W1 cannot carry an executable-evaluation witness")
        if self.final_witness_level == "W1" and not self.final_concrete_locations:
            raise ValueError("final W1 requires concrete localization")
        return self


class X1v2WitnessLevelAudit(BaseModel):
    """Complete manual dual-review audit of every frozen X1v2 arm-generated finding."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal[WITNESS_AUDIT_SCHEMA] = Field(default=WITNESS_AUDIT_SCHEMA, description="Stable schema identifier for this dual-reviewed audit artifact.")
    issue_189_definition: str = Field(description="Applied semantic W0/W1/W2 definition, including why no tool does not collapse W1 into W0.")
    decision_rules: tuple[str, ...] = Field(description="Human-review boundary rules that constrain but do not automatically infer W labels.")
    data_sources: tuple[str, ...] = Field(description="Archive-relative frozen source, method, and Judge artifacts used during review.")
    finding_count: int = Field(description="Number of frozen X1v2 findings covered by the audit.", ge=0)
    primary_review_coverage: int = Field(description="Number of findings with a completed primary review.", ge=0)
    secondary_review_coverage: int = Field(description="Number of findings with a completed independent secondary review.", ge=0)
    disagreement_count: int = Field(description="Number of findings requiring pane5 W-level adjudication.", ge=0)
    post_review_correction_count: int = Field(description="Number of bounded corrections applied after two agreeing independent reviews.", ge=0)
    final_witness_counts: dict[WitnessLevel, int] = Field(description="Final W0/W1/W2 distribution computed from every finalized finding.")
    records: tuple[FindingWitnessAudit, ...] = Field(description="One final dual-reviewed audit record for each frozen X1v2 finding.")
    reason: str = Field(description="Why this is a manual evidence-strength audit rather than a method or Judge rerun.")
    basis: str = Field(description="Completeness and provenance basis for the full audit universe.")

    @model_validator(mode="after")
    def validate_complete_counts(self) -> "X1v2WitnessLevelAudit":
        """Enforce internal coverage and final-distribution closure without choosing labels."""

        keys = [record.work_item.audit_key for record in self.records]
        if len(keys) != len(set(keys)):
            raise ValueError("witness audit contains duplicate finding audit keys")
        if self.finding_count != len(self.records):
            raise ValueError("finding_count must equal the number of final records")
        if self.primary_review_coverage != self.finding_count or self.secondary_review_coverage != self.finding_count:
            raise ValueError("both independent review coverages must equal finding_count")
        if self.disagreement_count != sum(record.disagreement for record in self.records):
            raise ValueError("disagreement_count must equal finalized disagreement records")
        if self.post_review_correction_count != sum(record.post_review_correction is not None for record in self.records):
            raise ValueError("post_review_correction_count must equal finalized correction records")
        actual = Counter(record.final_witness_level for record in self.records)
        expected = {level: actual[level] for level in ("W0", "W1", "W2")}
        if self.final_witness_counts != expected:
            raise ValueError("final_witness_counts must equal the finalized record distribution")
        return self


class FindingWitnessAdjudication(BaseModel):
    """Pane5 resolution for a finding whose two human W reviews disagree."""

    model_config = ConfigDict(extra="forbid")

    audit_key: str = Field(description="Stable key of the finding with different primary and secondary W levels.")
    adjudicator_id: str = Field(description="Pane5 identity responsible for the final semantic resolution.", min_length=1)
    final_witness_level: WitnessLevel = Field(description="Final pane5 W level after reading both reviews and frozen evidence.")
    final_concrete_locations: tuple[str, ...] = Field(description="Concrete locations retained by pane5 for the final decision.")
    executable_object: str | None = Field(description="Original X1v2 executable object only for a final W2 decision.")
    evaluation_receipt: str | None = Field(description="Original X1v2 terminal-evaluation receipt only for a final W2 decision.")
    evaluated_artifact_hash: str | None = Field(description="Exact evaluated-artifact hash only for a final W2 decision.")
    terminal_result: str | None = Field(description="Original terminal result only for a final W2 decision.")
    reason: str = Field(description="Finding-specific explanation of why pane5 selected the final W boundary.", min_length=1)
    basis: str = Field(description="Both review positions plus raw-record/source anchors used by pane5.", min_length=1)

    @model_validator(mode="after")
    def validate_final_shape(self) -> "FindingWitnessAdjudication":
        """Check structural evidence fields only for a claimed W2 adjudication."""

        values = (self.executable_object, self.evaluation_receipt, self.evaluated_artifact_hash, self.terminal_result)
        if self.final_witness_level == "W2":
            if not self.final_concrete_locations or any(value is None or not value.strip() for value in values):
                raise ValueError("W2 adjudication requires location, object, receipt, artifact hash, and terminal result")
        elif any(value is not None for value in values):
            raise ValueError("W0/W1 adjudication cannot carry W2-only execution fields")
        if self.final_witness_level == "W1" and not self.final_concrete_locations:
            raise ValueError("W1 adjudication requires concrete localization")
        return self


class X1v2WitnessAdjudicationLog(BaseModel):
    """Complete pane5 log for W-level disagreements and bounded post-review corrections."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal[WITNESS_ADJUDICATION_SCHEMA] = Field(default=WITNESS_ADJUDICATION_SCHEMA, description="Stable schema identifier for the pane5 disagreement-decision artifact.")
    finding_count: int = Field(description="Number of frozen findings compared across the two complete manual review passes.", ge=0)
    disagreement_count: int = Field(description="Number of W-level disagreements that required pane5 adjudication.", ge=0)
    adjudications: tuple[FindingWitnessAdjudication, ...] = Field(description="One pane5 resolution for every and only W-level disagreement.")
    post_review_correction_count: int = Field(default=0, description="Number of bounded corrections that override two agreeing reviews after an independent semantic review.", ge=0)
    post_review_corrections: tuple[PostReviewCorrection, ...] = Field(default=(), description="Every and only documented post-review correction accepted into the final audit.")
    reason: str = Field(description="Why final W labels cannot silently override disagreement or agreement without an explicit preserved decision record.", min_length=1)
    basis: str = Field(description="Preview artifact, both decision passes, and frozen source evidence used for the decisions.", min_length=1)

    @model_validator(mode="after")
    def validate_decision_count(self) -> "X1v2WitnessAdjudicationLog":
        """Require one unique decision record for each declared disagreement."""

        keys = [item.audit_key for item in self.adjudications]
        if self.disagreement_count != len(self.adjudications) or len(keys) != len(set(keys)):
            raise ValueError("adjudication log must contain one unique decision for every disagreement")
        correction_keys = [item.audit_key for item in self.post_review_corrections]
        if self.post_review_correction_count != len(self.post_review_corrections) or len(correction_keys) != len(set(correction_keys)):
            raise ValueError("adjudication log must contain one unique post-review correction for every declared correction")
        if set(keys) & set(correction_keys):
            raise ValueError("one finding cannot be both a review disagreement and a post-review correction")
        return self


class SupportingReportWitness(BaseModel):
    """One manually audited report used by a FULL expected-row witness aggregation."""

    model_config = ConfigDict(extra="forbid")

    original_report_id: str = Field(description="Frozen report ID listed in the expected outcome's full_report_ids.")
    witness_level: WitnessLevel = Field(description="Final manual W level for this supporting report.")
    audit_key: str = Field(description="Stable final-audit key from which the supporting report level was read.")
    reason: str = Field(description="Why this report is eligible only because the frozen expected outcome lists it as FULL support.")
    basis: str = Field(description="PairJudgeResult expected_outcomes full_report_ids field and final audit key.")


class FullHitWitnessRow(BaseModel):
    """One expected issue-round relation with a max W derived from FULL reports only."""

    model_config = ConfigDict(extra="forbid")

    pair_id: str = Field(description="Frozen benchmark pair identifier for this expected relation row.")
    round: int = Field(description="Frozen round number for this expected relation row.", ge=1, le=3)
    expected_id: str = Field(description="Frozen ledger expected issue identifier.")
    relation: MatchRelation = Field(description="FULL, PARTIAL, or NONE materialized by the frozen Judge.")
    full_report_ids: tuple[str, ...] = Field(description="Only frozen reports named as FULL support for this expected row.")
    supporting_reports: tuple[SupportingReportWitness, ...] = Field(description="Manual W labels for full_report_ids only; partial support is never included.")
    max_witness_level: WitnessLevel | None = Field(description="Maximum W2 > W1 > W0 over FULL supporting reports, null for PARTIAL/NONE.")
    reason: str = Field(description="Why this row did or did not enter the FULL-hit W denominator.")
    basis: str = Field(description="Selected PairJudgeResult expected outcome and final manual-audit record references.")

    @model_validator(mode="after")
    def validate_relation_shape(self) -> "FullHitWitnessRow":
        """Ensure only FULL rows receive a maximum based on full_report_ids."""

        if self.relation == "FULL":
            if not self.full_report_ids or len(self.supporting_reports) != len(self.full_report_ids) or self.max_witness_level is None:
                raise ValueError("FULL row requires full reports and a nonempty max W")
        elif self.supporting_reports or self.max_witness_level is not None:
            raise ValueError("PARTIAL/NONE rows cannot enter FULL-hit witness aggregation")
        return self


class X1v2FullHitMaxWitnessAudit(BaseModel):
    """Expected-row aggregation of manual report W labels over frozen FULL relations."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal["paper1.x1v2-full-hit-max-witness-audit.v1"] = Field(default="paper1.x1v2-full-hit-max-witness-audit.v1", description="Stable schema identifier for the X1v2 expected-row max-W audit.")
    expected_row_count: int = Field(description="All retained expected issue-round rows, including FULL/PARTIAL/NONE.", ge=0)
    full_row_count: int = Field(description="Number of FULL rows in the max-W denominator.", ge=0)
    overall_full_hit_max_counts: dict[WitnessLevel, int] = Field(description="FULL rows by maximum W0/W1/W2 over FULL supporting reports.")
    l2_full_hit_max_counts: dict[WitnessLevel, int] = Field(description="Same maximum-W counts restricted to ledger L2 expected rows.")
    w2_all_expected_count: int = Field(description="All-expected numerator for FULL-only max W2.", ge=0)
    rows: tuple[FullHitWitnessRow, ...] = Field(description="Every frozen expected relation row with manual W linkage.")
    reason: str = Field(description="Why partial_report_ids cannot raise a FULL hit's witness level.")
    basis: str = Field(description="Selected expected outcomes, ledger L2 labels, and complete manual audit records.")

    @model_validator(mode="after")
    def validate_counts(self) -> "X1v2FullHitMaxWitnessAudit":
        """Check expected-row completeness and the FULL-hit max-W accounting identity."""

        full_rows = [row for row in self.rows if row.relation == "FULL"]
        if self.expected_row_count != len(self.rows) or self.full_row_count != len(full_rows):
            raise ValueError("expected-row or FULL-row count does not match retained rows")
        counts = Counter(str(row.max_witness_level) for row in full_rows)
        expected = {level: counts[level] for level in ("W0", "W1", "W2")}
        if self.overall_full_hit_max_counts != expected:
            raise ValueError("overall max-W counts must equal the FULL-row distribution")
        if sum(self.overall_full_hit_max_counts.values()) != self.full_row_count:
            raise ValueError("FULL-hit max-W counts must close over the FULL denominator")
        if self.w2_all_expected_count != counts["W2"]:
            raise ValueError("W2/all-expected numerator must be the all-row count of FULL-only max W2")
        return self


class WitnessMergePreview(BaseModel):
    """Comparison of two exhaustive manual passes before pane5 resolves disagreements."""

    model_config = ConfigDict(extra="forbid")

    finding_count: int = Field(description="Number of frozen findings compared across both review passes.", ge=0)
    agreement_count: int = Field(description="Number of findings whose independent reviews chose the same W level.", ge=0)
    disagreement_keys: tuple[str, ...] = Field(description="Stable keys requiring pane5 resolution before final audit materialization.")
    reason: str = Field(description="Why an unresolved disagreement cannot be silently collapsed into a final W label.")
    basis: str = Field(description="Exact primary and secondary decision files checked against the label-free review packet.")


class X1v2WitnessReviewPacket(BaseModel):
    """Exhaustive read-only work packet used to obtain independent manual reviews."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal[WITNESS_PACKET_SCHEMA] = Field(default=WITNESS_PACKET_SCHEMA, description="Stable schema identifier for the manual-review work packet.")
    finding_count: int = Field(description="Number of exhaustive frozen findings in the work packet.", ge=0)
    work_items: tuple[ReviewWorkItem, ...] = Field(description="Frozen context for each finding; this packet intentionally contains no W label.")
    reason: str = Field(description="Why reviewers must read each finding, its source inputs, and its immutable record manually.")
    basis: str = Field(description="Record enumeration and input-hash evidence for the blinded review packet.")

    @model_validator(mode="after")
    def validate_count(self) -> "X1v2WitnessReviewPacket":
        """Require exact item-count and key uniqueness for manual review work."""

        keys = [item.audit_key for item in self.work_items]
        if self.finding_count != len(self.work_items) or len(keys) != len(set(keys)):
            raise ValueError("review packet must declare every unique frozen finding exactly once")
        if any(item.judge_association is not None for item in self.work_items):
            raise ValueError("the manual-review packet must not expose a Judge association")
        return self


class X1v2WitnessReviewBatch(BaseModel):
    """A deterministic, label-free subset of the exhaustive manual review packet."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal[WITNESS_PACKET_SCHEMA] = Field(default=WITNESS_PACKET_SCHEMA, description="Stable schema identifier shared with the parent manual-review packet.")
    batch_id: str = Field(description="Stable zero-padded identifier for this mutually exclusive manual-review batch.")
    finding_count: int = Field(description="Number of frozen findings assigned to this batch.", ge=1)
    work_items: tuple[ReviewWorkItem, ...] = Field(description="Label-free frozen review units assigned only to this deterministic batch.")
    reason: str = Field(description="Why this batch remains label-free for both independent reviews.")
    basis: str = Field(description="Parent packet and deterministic item-range basis for this batch.")

    @model_validator(mode="after")
    def validate_count(self) -> "X1v2WitnessReviewBatch":
        """Reject a batch with duplicated or incorrectly counted frozen work items."""

        keys = [item.audit_key for item in self.work_items]
        if self.finding_count != len(self.work_items) or len(keys) != len(set(keys)):
            raise ValueError("review batch must contain each assigned work item exactly once")
        return self


class ReviewedFindingDecision(BaseModel):
    """One reviewer decision keyed to one label-free work item from a fixed batch."""

    model_config = ConfigDict(extra="forbid")

    audit_key: str = Field(description="Stable work-item key selected from the matching label-free batch.")
    review: ManualWitnessReview = Field(description="Independent manual W-level review for this exact frozen finding.")


class ManualReviewDecisionBatch(BaseModel):
    """A reviewer-authored, exhaustive decision file for one assigned manual-review batch."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal["paper1.x1v2-witness-review-decisions.v2"] = Field(default="paper1.x1v2-witness-review-decisions.v2", description="Stable schema identifier for a reviewer-authored blinded decision batch.")
    batch_id: str = Field(description="Stable identifier of the label-free review batch assessed here.")
    reviewer_id: str = Field(description="Identity of the person or independent reviewer who made every decision in this file.", min_length=1)
    review_pass: Literal["primary", "secondary"] = Field(description="Whether this is the first or independent second review pass.")
    decisions: tuple[ReviewedFindingDecision, ...] = Field(description="One semantic decision for every assigned finding without omitted or duplicated audit keys.")
    reason: str = Field(description="Why this is a human semantic review rather than an automated W-level classifier.")
    basis: str = Field(description="Batch path, frozen source inputs, and finding record references examined by the reviewer.")

    @model_validator(mode="after")
    def validate_reviewer_coverage(self) -> "ManualReviewDecisionBatch":
        """Ensure a submitted batch does not mix reviewer identities or duplicate keys."""

        keys = [decision.audit_key for decision in self.decisions]
        if len(keys) != len(set(keys)):
            raise ValueError("manual review decision batch contains duplicate audit keys")
        if any(decision.review.reviewer_id != self.reviewer_id for decision in self.decisions):
            raise ValueError("each decision review.reviewer_id must equal the batch reviewer_id")
        return self


class X1v2InputClosure(BaseModel):
    """Archived NL and PlantUML inputs needed for an offline manual witness audit."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal[INPUT_CLOSURE_SCHEMA] = Field(default=INPUT_CLOSURE_SCHEMA, description="Stable schema identifier for the copied X1v2 source-input closure.")
    pair_count: int = Field(description="Number of pair-level NL and PlantUML input closures copied after frozen-hash verification.", ge=0)
    inputs: dict[str, tuple[SourceArtifactReference, SourceArtifactReference]] = Field(description="Per-pair natural-language and PlantUML archive references in that order.")
    reason: str = Field(description="Why manual review needs frozen source text in addition to original finding prose.")
    basis: str = Field(description="Raw X1v2 input hashes checked before each source input was copied into the archive.")


def _archive_repository_path(archive_root: Path, path: Path, repository_root: Path) -> str:
    """Convert one archive-owned path to a stable repository-relative reference."""

    return str(path.resolve().relative_to(repository_root.resolve()))


def _sha_from_record(value: object) -> str:
    """Normalize an unprefixed frozen record digest into the archive digest notation."""

    if not isinstance(value, str) or not value:
        raise ValueError("missing frozen input SHA-256")
    return value if value.startswith("sha256:") else "sha256:" + value


def _selected_pair_results(archive_root: Path) -> dict[tuple[str, int], tuple[Path, dict[str, object], str]]:
    """Resolve each composite-selected baseline Judge result and verify its receipt hash."""

    baseline = archive_root / "raw" / "x1v2_baseline"
    composite_path = baseline / "judge" / "composite-summary.json"
    composite = _load_json(composite_path)
    selected: dict[tuple[str, int], tuple[Path, dict[str, object], str]] = {}
    receipts = composite.get("pair_receipts")
    if not isinstance(receipts, list):
        raise ValueError("baseline composite lacks pair_receipts")
    for receipt in receipts:
        if not isinstance(receipt, dict):
            raise ValueError("baseline composite has an invalid pair receipt")
        pair_id, round_number = str(receipt["pair_id"]), int(receipt["round"])
        result_path = baseline / "judge" / "source_runs" / str(receipt["source_run_id"]) / "pairs" / f"{pair_id}.json"
        if sha256_file(result_path) != receipt.get("result_hash"):
            raise ValueError(f"selected Judge result hash mismatch: {result_path}")
        key = (pair_id, round_number)
        if key in selected:
            raise ValueError(f"duplicate composite selection for {key}")
        selected[key] = (result_path, _load_json(result_path), str(receipt["result_hash"]))
    if len(selected) != 162:
        raise ValueError(f"expected 162 selected baseline Judge results, found {len(selected)}")
    return selected


def _judge_associations(archive_root: Path) -> dict[str, JudgeAssociation]:
    """Join frozen Judge fields only after the blinded W reviews have completed."""

    repository_root = archive_root.resolve().parents[3]
    associations: dict[str, JudgeAssociation] = {}
    for (pair_id, round_number), (judge_path, judge_result, judge_hash) in _selected_pair_results(archive_root).items():
        report_outcomes = judge_result.get("report_outcomes")
        expected_outcomes = judge_result.get("expected_outcomes")
        if not isinstance(report_outcomes, list) or not isinstance(expected_outcomes, list):
            raise ValueError(f"invalid selected Judge result: {judge_path}")
        full_ids: dict[str, list[str]] = defaultdict(list)
        partial_ids: dict[str, list[str]] = defaultdict(list)
        for expected in expected_outcomes:
            if not isinstance(expected, dict):
                raise ValueError(f"invalid expected outcome: {judge_path}")
            ledger_id = str(expected["ledger_id"])
            for report_id in expected.get("full_report_ids", []):
                full_ids[str(report_id)].append(ledger_id)
            for report_id in expected.get("partial_report_ids", []):
                partial_ids[str(report_id)].append(ledger_id)
        judge_repository_path = _archive_repository_path(archive_root, judge_path, repository_root)
        for report_outcome in report_outcomes:
            if not isinstance(report_outcome, dict):
                raise ValueError(f"invalid report outcome: {judge_path}")
            report_id = str(report_outcome["original_report_id"])
            audit_key = f"{pair_id}:r{round_number}:{report_id}"
            if audit_key in associations:
                raise ValueError(f"duplicate selected Judge report association: {audit_key}")
            associations[audit_key] = JudgeAssociation(
                validity=str(report_outcome["validity"]),
                full_ledger_ids=tuple(sorted(full_ids[report_id])),
                partial_ledger_ids=tuple(sorted(partial_ids[report_id])),
                judge_pair_result_path=judge_repository_path,
                judge_pair_result_sha256=judge_hash,
                reason="This linkage is attached after blinded W review for evaluator aggregation only; it was not exposed to either reviewer and cannot determine W0/W1/W2.",
                basis=f"{judge_repository_path}; report_outcomes original_report_id={report_id}; expected_outcomes full_report_ids and partial_report_ids",
            )
    if len(associations) != 512:
        raise ValueError(f"expected 512 selected Judge report associations, found {len(associations)}")
    return associations


def archive_x1v2_input_closure(archive_root: Path, repository_root: Path) -> X1v2InputClosure:
    """Copy source inputs only after their bytes match every frozen X1v2 record hash."""

    baseline_root = archive_root / "raw" / "x1v2_baseline" / "method"
    records = sorted(baseline_root.rglob("record.json"))
    if len(records) != 162:
        raise ValueError(f"expected 162 X1v2 method records, found {len(records)}")
    copied: dict[str, tuple[SourceArtifactReference, SourceArtifactReference]] = {}
    for record_path in records:
        record = _load_json(record_path)
        pair_id = str(record["case"])
        inputs = record.get("inputs")
        if not isinstance(inputs, dict):
            raise ValueError(f"record has no inputs: {record_path}")
        nl_source = Path(str(inputs["nl_path"])).resolve()
        plantuml_source = Path(str(inputs["plantuml_path"])).resolve()
        nl_hash, plantuml_hash = _sha_from_record(inputs.get("nl_sha256")), _sha_from_record(inputs.get("plantuml_sha256"))
        if sha256_file(nl_source) != nl_hash or sha256_file(plantuml_source) != plantuml_hash:
            raise ValueError(f"current source bytes do not match the frozen record for pair {pair_id}")
        pair_dir = archive_root / "reference" / "x1v2_input_closure" / "pairs" / pair_id
        nl_target, plantuml_target = pair_dir / "nl.txt", pair_dir / "plantuml.puml"
        pair_dir.mkdir(parents=True, exist_ok=True)
        if not nl_target.exists():
            shutil.copy2(nl_source, nl_target)
        if not plantuml_target.exists():
            shutil.copy2(plantuml_source, plantuml_target)
        if sha256_file(nl_target) != nl_hash or sha256_file(plantuml_target) != plantuml_hash:
            raise ValueError(f"copied input closure hash mismatch for pair {pair_id}")
        nl_reference = SourceArtifactReference(
            repository_path=_archive_repository_path(archive_root, nl_target, repository_root),
            sha256=nl_hash,
            reason="The frozen natural-language requirement is necessary to assess whether the original finding localizes an asserted defect.",
            basis=f"record.inputs.nl_sha256={nl_hash}; copied archive reference/x1v2_input_closure/pairs/{pair_id}/nl.txt",
        )
        plantuml_reference = SourceArtifactReference(
            repository_path=_archive_repository_path(archive_root, plantuml_target, repository_root),
            sha256=plantuml_hash,
            reason="The frozen PlantUML source is necessary to assess whether the original finding names a checkable carrier or path.",
            basis=f"record.inputs.plantuml_sha256={plantuml_hash}; copied archive reference/x1v2_input_closure/pairs/{pair_id}/plantuml.puml",
        )
        previous = copied.get(pair_id)
        if previous is not None and previous != (nl_reference, plantuml_reference):
            raise ValueError(f"same pair has inconsistent frozen source inputs: {pair_id}")
        copied[pair_id] = (nl_reference, plantuml_reference)
    closure = X1v2InputClosure(
        pair_count=len(copied),
        inputs=dict(sorted(copied.items())),
        reason="The legacy method records retain source paths and hashes but not source text; this closure preserves the hash-verified NL and PlantUML needed for offline manual review.",
        basis="Every copied input is byte-checked against inputs.nl_sha256 or inputs.plantuml_sha256 in all 162 frozen X1v2 records.",
    )
    _write_json(archive_root / "reference" / "x1v2_input_closure" / "manifest.json", closure.model_dump(mode="json"))
    return closure


def build_x1v2_review_packet(archive_root: Path, repository_root: Path) -> X1v2WitnessReviewPacket:
    """Enumerate every frozen X1v2 finding into a Judge-blinded review packet."""

    closure = archive_x1v2_input_closure(archive_root, repository_root)
    method_root = archive_root / "raw" / "x1v2_baseline" / "method"
    work_items: list[ReviewWorkItem] = []
    for record_path in sorted(method_root.rglob("record.json")):
        record = _load_json(record_path)
        pair_id, round_number = str(record["case"]), int(record["round"])
        parsed_output = record.get("parsed_output")
        if not isinstance(parsed_output, dict) or not isinstance(parsed_output.get("issues"), list):
            raise ValueError(f"record has no parsed issue list: {record_path}")
        record_repository_path = _archive_repository_path(archive_root, record_path, repository_root)
        for index, finding in enumerate(parsed_output["issues"]):
            if not isinstance(finding, dict):
                raise ValueError(f"invalid finding at {record_path} index {index}")
            report_id = f"{pair_id}:r{round_number}:baseline_issue_{index + 1}"
            issue, where, finding_reason = (str(finding.get(key, "")) for key in ("issue", "where", "reason"))
            if not issue or not where or not finding_reason:
                raise ValueError(f"finding lacks issue/where/reason: {record_path} index {index}")
            work_items.append(ReviewWorkItem(
                audit_key=f"{pair_id}:r{round_number}:{report_id}",
                pair_id=pair_id,
                round=round_number,
                original_report_id=report_id,
                original_finding_index=index,
                method_record_repository_path=record_repository_path,
                method_record_sha256=sha256_file(record_path),
                issue=issue,
                where=where,
                finding_reason=finding_reason,
                issue_sha256=sha256_text(issue),
                where_sha256=sha256_text(where),
                finding_reason_sha256=sha256_text(finding_reason),
                finding_json_pointer=f"/parsed_output/issues/{index}",
                natural_language=closure.inputs[pair_id][0],
                plantuml=closure.inputs[pair_id][1],
                reason="This item preserves the complete original X1v2 finding and its hash-verified NL/PlantUML inputs for one individual manual review.",
                basis=f"{record_repository_path}#/parsed_output/issues/{index}; legacy sample_id={record['pair_id']}; sha256={sha256_file(record_path)}; source inputs verified by reference/x1v2_input_closure/manifest.json",
            ))
    packet = X1v2WitnessReviewPacket(
        finding_count=len(work_items),
        work_items=tuple(work_items),
        reason="No W label, Judge path, Judge hash, validity, expected relation, or ledger identifier appears in this packet. Reviewers must make a semantic judgment from each original finding together with the hash-verified NL and PlantUML inputs.",
        basis="162 frozen X1v2 record.json files and the hash-verified NL/PlantUML input closure. No Judge artifact is read while materializing this packet.",
    )
    if packet.finding_count != 512:
        raise ValueError(f"expected 512 X1v2 findings, found {packet.finding_count}")
    _write_json(archive_root / "derived" / "x1v2_witness_review_packet.json", packet.model_dump(mode="json", exclude_none=True))
    return packet


def work_items_by_batch(packet: X1v2WitnessReviewPacket, batch_count: int) -> tuple[tuple[ReviewWorkItem, ...], ...]:
    """Split label-free manual-review work into deterministic, mutually exclusive batches."""

    if batch_count <= 0:
        raise ValueError("batch_count must be positive")
    size, remainder = divmod(len(packet.work_items), batch_count)
    batches: list[tuple[ReviewWorkItem, ...]] = []
    start = 0
    for batch_index in range(batch_count):
        stop = start + size + (1 if batch_index < remainder else 0)
        batches.append(packet.work_items[start:stop])
        start = stop
    return tuple(batches)


def write_x1v2_review_batches(archive_root: Path, packet: X1v2WitnessReviewPacket, batch_count: int = 12) -> tuple[Path, ...]:
    """Persist mutually exclusive label-free review batches for independent human reviewers."""

    output_root = archive_root / "derived" / "x1v2_witness_review_batches"
    output_root.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []
    for batch_index, items in enumerate(work_items_by_batch(packet, batch_count)):
        batch_id = f"batch-{batch_index:02d}"
        batch = X1v2WitnessReviewBatch(
            batch_id=batch_id,
            finding_count=len(items),
            work_items=items,
            reason="The batch contains no primary, secondary, final, or Judge-derived W label; an assigned reviewer must inspect every original finding and its hash-verified source inputs independently.",
            basis=f"derived/x1v2_witness_review_packet.json; contiguous deterministic work-item range {sum(len(group) for group in work_items_by_batch(packet, batch_count)[:batch_index])}:{sum(len(group) for group in work_items_by_batch(packet, batch_count)[:batch_index + 1])}",
        )
        output_path = output_root / f"{batch_id}.json"
        _write_json(output_path, batch.model_dump(mode="json"))
        output_paths.append(output_path)
    return tuple(output_paths)


def _load_packet(archive_root: Path) -> X1v2WitnessReviewPacket:
    """Load and validate the single exhaustive label-free review packet."""

    return X1v2WitnessReviewPacket.model_validate(_load_json(archive_root / "derived" / "x1v2_witness_review_packet.json"))


def _decision_maps(
    archive_root: Path,
    packet: X1v2WitnessReviewPacket,
    review_pass: Literal["primary", "secondary"],
) -> dict[str, ManualWitnessReview]:
    """Load reviewer-authored decision batches and prove exact packet coverage."""

    batch_root = archive_root / "derived" / "x1v2_witness_review_decisions" / review_pass
    paths = sorted(batch_root.glob("batch-*.json"))
    if len(paths) != 12:
        raise ValueError(f"expected 12 {review_pass} decision batches, found {len(paths)}")
    expected_by_batch = {
        batch.batch_id: {item.audit_key for item in batch.work_items}
        for batch in (
            X1v2WitnessReviewBatch.model_validate(_load_json(path))
            for path in sorted((archive_root / "derived" / "x1v2_witness_review_batches").glob("batch-*.json"))
        )
    }
    if len(expected_by_batch) != 12:
        raise ValueError("expected 12 label-free manual review batches")
    decisions: dict[str, ManualWitnessReview] = {}
    for path in paths:
        batch = ManualReviewDecisionBatch.model_validate(_load_json(path))
        if batch.review_pass != review_pass:
            raise ValueError(f"wrong review pass in {path}")
        expected_keys = expected_by_batch.get(batch.batch_id)
        actual_keys = {decision.audit_key for decision in batch.decisions}
        if expected_keys is None or actual_keys != expected_keys:
            raise ValueError(f"review batch does not exactly cover its packet: {path}")
        for decision in batch.decisions:
            if decision.audit_key in decisions:
                raise ValueError(f"duplicate {review_pass} decision for {decision.audit_key}")
            decisions[decision.audit_key] = decision.review
    packet_keys = {item.audit_key for item in packet.work_items}
    if set(decisions) != packet_keys:
        raise ValueError(f"{review_pass} decisions do not exactly cover the complete review packet")
    return decisions


def preview_x1v2_manual_reviews(archive_root: Path) -> WitnessMergePreview:
    """Compare independent manual passes without choosing an outcome for any disagreement."""

    packet = _load_packet(archive_root)
    primary = _decision_maps(archive_root, packet, "primary")
    secondary = _decision_maps(archive_root, packet, "secondary")
    disagreement_keys = tuple(sorted(
        key for key in primary if primary[key].witness_level != secondary[key].witness_level
    ))
    return WitnessMergePreview(
        finding_count=packet.finding_count,
        agreement_count=packet.finding_count - len(disagreement_keys),
        disagreement_keys=disagreement_keys,
        reason="The preview preserves independent primary and secondary decisions. Pane5 must resolve every listed W-level disagreement before a final audit can be written.",
        basis="derived/x1v2_witness_review_packet.json and all twelve primary plus all twelve secondary decision batches, checked for exact key coverage.",
    )


def _union_locations(primary: ManualWitnessReview, secondary: ManualWitnessReview) -> tuple[str, ...]:
    """Retain reviewer-identified locations without collapsing their independent reasoning."""

    return tuple(dict.fromkeys((*primary.concrete_locations, *secondary.concrete_locations)))


def validate_post_review_correction_keys(
    post_review_corrections: dict[str, PostReviewCorrection],
    agreement_keys: set[str],
) -> None:
    """Restrict consensus corrections to the independently audited, agreeing record."""

    if not set(post_review_corrections) <= agreement_keys:
        raise ValueError("post-review corrections can apply only to agreeing reviews")
    if not set(post_review_corrections) <= POST_REVIEW_CORRECTION_ALLOWLIST:
        raise ValueError("post-review correction key is not in the accepted correction allowlist")


def materialize_x1v2_witness_audit(
    archive_root: Path,
    adjudications: dict[str, FindingWitnessAdjudication],
    post_review_corrections: dict[str, PostReviewCorrection],
) -> X1v2WitnessLevelAudit:
    """Create the final audit after every disagreement and bounded correction is documented."""

    packet = _load_packet(archive_root)
    primary = _decision_maps(archive_root, packet, "primary")
    secondary = _decision_maps(archive_root, packet, "secondary")
    preview = preview_x1v2_manual_reviews(archive_root)
    if set(adjudications) != set(preview.disagreement_keys):
        raise ValueError("adjudications must cover every and only W-level disagreement")
    agreement_keys = {item.audit_key for item in packet.work_items} - set(preview.disagreement_keys)
    validate_post_review_correction_keys(post_review_corrections, agreement_keys)
    associations = _judge_associations(archive_root)
    records: list[FindingWitnessAudit] = []
    for item in packet.work_items:
        first, second = primary[item.audit_key], secondary[item.audit_key]
        disagreement = first.witness_level != second.witness_level
        if disagreement:
            resolution = adjudications[item.audit_key]
            final_level = resolution.final_witness_level
            final_locations = resolution.final_concrete_locations
            executable_object = resolution.executable_object
            evaluation_receipt = resolution.evaluation_receipt
            artifact_hash = resolution.evaluated_artifact_hash
            terminal_result = resolution.terminal_result
            final_reason = resolution.reason
            final_basis = resolution.basis
            adjudicator_id = resolution.adjudicator_id
            disagreement_detail = f"primary={first.witness_level}: {first.reason}; secondary={second.witness_level}: {second.reason}"
            post_review_correction = None
        elif item.audit_key in post_review_corrections:
            correction = post_review_corrections[item.audit_key]
            final_level = correction.corrected_final_witness_level
            final_locations = correction.final_concrete_locations
            executable_object = correction.executable_object
            evaluation_receipt = correction.evaluation_receipt
            artifact_hash = correction.evaluated_artifact_hash
            terminal_result = correction.terminal_result
            final_reason = correction.reason
            final_basis = correction.basis
            adjudicator_id = correction.adjudicator_id
            disagreement_detail = None
            post_review_correction = correction
        else:
            final_level = first.witness_level
            final_locations = _union_locations(first, second)
            executable_object = first.executable_object
            evaluation_receipt = first.evaluation_receipt
            artifact_hash = first.evaluated_artifact_hash
            terminal_result = first.terminal_result
            final_reason = f"Primary and independent secondary reviews both selected {final_level}. Primary: {first.reason} Secondary: {second.reason}"
            final_basis = f"Primary basis: {first.basis} Secondary basis: {second.basis}"
            adjudicator_id = None
            disagreement_detail = None
            post_review_correction = None
        associated_item = item.model_copy(update={"judge_association": associations[item.audit_key]})
        records.append(FindingWitnessAudit(
            work_item=associated_item,
            primary_review=first,
            secondary_review=second,
            disagreement=disagreement,
            disagreement_detail=disagreement_detail,
            final_witness_level=final_level,
            final_concrete_locations=final_locations,
            executable_object=executable_object,
            evaluation_receipt=evaluation_receipt,
            evaluated_artifact_hash=artifact_hash,
            terminal_result=terminal_result,
            final_reason=final_reason,
            final_basis=final_basis,
            adjudicator_id=adjudicator_id,
            post_review_correction=post_review_correction,
        ))
    counts = Counter(record.final_witness_level for record in records)
    audit = X1v2WitnessLevelAudit(
        issue_189_definition="W0 is prose without a checkable concrete carrier or path. W1 concretely localizes a state, transition, guard, action, missing edge, model fragment, or finite path but has no method-produced terminal executable witness. W2 additionally requires an X1v2-produced executable object, original runtime terminal evaluation receipt, exact evaluated-artifact hash, and terminal result. A lack of tools prevents W2 but does not collapse concretely located W1 findings into W0.",
        decision_rules=(
            "Manual reviewers read issue, where, reason, frozen NL, frozen PlantUML, and source hashes for every finding; no text heuristic assigns a W label.",
            "Both reviewer packets omit every Judge path, hash, validity, expected relation, and ledger identifier; those fields are attached only after review for evaluator aggregation.",
            "A missing carrier may still be W1 when its enclosing scope and concrete endpoint(s) are explicitly localized.",
            "Judge inspection facts, later backend checks, and current predicates cannot be retrofitted as X1v2 W2 evidence.",
        ),
        data_sources=(
            "raw/x1v2_baseline/method/run{1,2,3}/*/record.json",
            "reference/x1v2_input_closure/pairs/*/{nl.txt,plantuml.puml}",
            "raw/x1v2_baseline/judge/composite-summary.json",
            "raw/x1v2_baseline/judge/source_runs/*/pairs/*.json",
        ),
        finding_count=len(records),
        primary_review_coverage=len(records),
        secondary_review_coverage=len(records),
        disagreement_count=sum(record.disagreement for record in records),
        post_review_correction_count=sum(record.post_review_correction is not None for record in records),
        final_witness_counts={level: counts[level] for level in ("W0", "W1", "W2")},
        records=tuple(records),
        reason="This evaluator-only artifact adds a human retrospective evidence-strength label to every frozen baseline finding. It neither reruns X1v2 nor lets later Judge/current capabilities create baseline W2 evidence.",
        basis="The Judge-blinded review packet proves 512 frozen finding keys. Every final record retains two independent review decisions and, for each W-level disagreement or bounded post-review correction, a pane5 decision tied to raw record and source references.",
    )
    _write_json(archive_root / "derived" / "x1v2_witness_level_audit.json", audit.model_dump(mode="json"))
    return audit


def materialize_x1v2_witness_adjudication_log(
    archive_root: Path,
    adjudications: dict[str, FindingWitnessAdjudication],
    post_review_corrections: dict[str, PostReviewCorrection],
) -> X1v2WitnessAdjudicationLog:
    """Persist every pane5 disagreement resolution and bounded consensus correction."""

    preview = preview_x1v2_manual_reviews(archive_root)
    if set(adjudications) != set(preview.disagreement_keys):
        raise ValueError("adjudication log must cover every and only W-level disagreement")
    agreement_keys = {item.audit_key for item in _load_packet(archive_root).work_items} - set(preview.disagreement_keys)
    validate_post_review_correction_keys(post_review_corrections, agreement_keys)
    log = X1v2WitnessAdjudicationLog(
        finding_count=preview.finding_count,
        disagreement_count=len(preview.disagreement_keys),
        adjudications=tuple(adjudications[key] for key in preview.disagreement_keys),
        post_review_correction_count=len(post_review_corrections),
        post_review_corrections=tuple(post_review_corrections[key] for key in sorted(post_review_corrections)),
        reason="The two human reviews are retained independently. Pane5 records every W-level disagreement and the separately evidenced correction of any consensus error found by an independent frozen-evidence review.",
        basis="derived/x1v2_witness_review_packet.json, all primary and secondary blinded decision batches, and the frozen raw record/NL/PlantUML evidence cited by each FindingWitnessAdjudication or PostReviewCorrection.",
    )
    _write_json(archive_root / "derived" / "x1v2_witness_adjudications.json", log.model_dump(mode="json"))
    return log


def _ledger_levels(archive_root: Path) -> dict[str, str]:
    """Read ledger L labels only for evaluator-side hit stratification."""

    items = _load_json(archive_root / "reference" / "ledger.json").get("items")
    if not isinstance(items, dict):
        raise ValueError("ledger has no items object")
    return {str(key): str(value.get("L")) for key, value in items.items() if isinstance(value, dict)}


def derive_x1v2_full_hit_witness_audit(archive_root: Path, audit: X1v2WitnessLevelAudit) -> X1v2FullHitMaxWitnessAudit:
    """Mechanically derive manual W aggregation over frozen full_report_ids without writing."""

    by_report_id = {record.work_item.original_report_id: record for record in audit.records}
    selected = _selected_pair_results(archive_root)
    levels = _ledger_levels(archive_root)
    rank = {"W0": 0, "W1": 1, "W2": 2}
    rows: list[FullHitWitnessRow] = []
    l2_full_levels: list[WitnessLevel] = []
    for (pair_id, round_number), (result_path, result, _) in sorted(selected.items()):
        expected_outcomes = result.get("expected_outcomes")
        if not isinstance(expected_outcomes, list):
            raise ValueError(f"selected Judge result lacks expected outcomes: {result_path}")
        for expected in expected_outcomes:
            if not isinstance(expected, dict):
                raise ValueError(f"invalid expected outcome in {result_path}")
            expected_id = str(expected["ledger_id"])
            relation: MatchRelation = "FULL" if bool(expected.get("hit")) else "PARTIAL" if bool(expected.get("supported")) else "NONE"
            full_ids = tuple(str(item) for item in expected.get("full_report_ids", []))
            if relation == "FULL":
                reports: list[SupportingReportWitness] = []
                for report_id in full_ids:
                    record = by_report_id.get(report_id)
                    if record is None:
                        raise ValueError(f"FULL expected row references an unaudited report: {report_id}")
                    reports.append(SupportingReportWitness(
                        original_report_id=report_id,
                        witness_level=record.final_witness_level,
                        audit_key=record.work_item.audit_key,
                        reason="This report is included because the frozen expected outcome lists it in full_report_ids; its manual W label is read unchanged from the final X1v2 witness audit.",
                        basis=f"{record.work_item.judge_association.judge_pair_result_path}; expected_outcomes ledger_id={expected_id}; full_report_ids includes {report_id}; derived/x1v2_witness_level_audit.json#{record.work_item.audit_key}",
                    ))
                max_level = max((report.witness_level for report in reports), key=rank.__getitem__)
                rows.append(FullHitWitnessRow(
                    pair_id=pair_id,
                    round=round_number,
                    expected_id=expected_id,
                    relation=relation,
                    full_report_ids=full_ids,
                    supporting_reports=tuple(reports),
                    max_witness_level=max_level,
                    reason="FULL row: maximum witness is computed only across frozen full_report_ids, never partial_report_ids.",
                    basis=f"{_archive_pair_result_pointer(archive_root, result_path)}#/expected_outcomes; ledger_id={expected_id}; final manual report records listed above",
                ))
                if levels.get(expected_id) == "L2":
                    l2_full_levels.append(max_level)
            else:
                rows.append(FullHitWitnessRow(
                    pair_id=pair_id,
                    round=round_number,
                    expected_id=expected_id,
                    relation=relation,
                    full_report_ids=full_ids,
                    supporting_reports=(),
                    max_witness_level=None,
                    reason=f"{relation} row: it remains in the complete expected-row audit but does not enter the FULL-hit W denominator.",
                    basis=f"{_archive_pair_result_pointer(archive_root, result_path)}#/expected_outcomes; ledger_id={expected_id}; frozen hit={expected.get('hit')}; supported={expected.get('supported')}",
                ))
    counts = Counter(row.max_witness_level for row in rows if row.relation == "FULL")
    l2_counts = Counter(l2_full_levels)
    hit_audit = X1v2FullHitMaxWitnessAudit(
        expected_row_count=len(rows),
        full_row_count=sum(row.relation == "FULL" for row in rows),
        overall_full_hit_max_counts={level: counts[level] for level in ("W0", "W1", "W2")},
        l2_full_hit_max_counts={level: l2_counts[level] for level in ("W0", "W1", "W2")},
        w2_all_expected_count=counts["W2"],
        rows=tuple(rows),
        reason="The hit-level W axis is a report-evidence aggregation. Only a frozen FULL supporting report may contribute to a FULL expected row's maximum W.",
        basis="162 composite-selected PairJudgeResult files and all 512 finalized manual witness labels; L2 uses reference/ledger.json.",
    )
    if hit_audit.expected_row_count != 435 or hit_audit.full_row_count != 211:
        raise ValueError(f"unexpected frozen expected universe: rows={hit_audit.expected_row_count}, FULL={hit_audit.full_row_count}")
    return hit_audit


def materialize_x1v2_full_hit_witness_audit(archive_root: Path, audit: X1v2WitnessLevelAudit) -> X1v2FullHitMaxWitnessAudit:
    """Persist the deterministic expected-row aggregation of finalized manual W labels."""

    hit_audit = derive_x1v2_full_hit_witness_audit(archive_root, audit)
    _write_json(archive_root / "derived" / "x1v2_full_hit_max_witness_audit.json", hit_audit.model_dump(mode="json"))
    return hit_audit


def _archive_pair_result_pointer(archive_root: Path, path: Path) -> str:
    """Render a repository-relative PairJudgeResult reference for an audit basis string."""

    repository_root = archive_root
    while not (repository_root / ".git").exists():
        if repository_root.parent == repository_root:
            raise ValueError("could not locate repository root")
        repository_root = repository_root.parent
    return str(path.resolve().relative_to(repository_root.resolve()))


def witness_audit_statistics(audit: X1v2WitnessLevelAudit, hit_audit: X1v2FullHitMaxWitnessAudit) -> dict[str, object]:
    """Derive report, round, validity, and hit W counts from manually finalized records."""

    levels = ("W0", "W1", "W2")
    final_counts = Counter(record.final_witness_level for record in audit.records)
    by_round: dict[str, dict[str, int]] = {}
    by_validity: dict[str, dict[str, int]] = {}
    for round_number in (1, 2, 3):
        counts = Counter(record.final_witness_level for record in audit.records if record.work_item.round == round_number)
        by_round[str(round_number)] = {level: counts[level] for level in levels}
    for validity in ("VALID_KNOWN", "VALID_NOVEL", "INVALID"):
        counts = Counter(
            record.final_witness_level
            for record in audit.records
            if record.work_item.judge_association.validity == validity
        )
        by_validity[validity] = {level: counts[level] for level in levels}
    return {
        "finding_level": {
            "counts": {level: final_counts[level] for level in levels},
            "denominator": audit.finding_count,
        },
        "finding_level_by_round": by_round,
        "finding_level_by_validity": by_validity,
        "full_hit_max_witness": {
            "denominator": hit_audit.full_row_count,
            "counts": hit_audit.overall_full_hit_max_counts,
        },
        "l2_full_hit_max_witness": {
            "denominator": sum(hit_audit.l2_full_hit_max_counts.values()),
            "counts": hit_audit.l2_full_hit_max_counts,
        },
        "w2_all_expected": {
            "count": hit_audit.w2_all_expected_count,
            "denominator": hit_audit.expected_row_count,
            "rate": hit_audit.w2_all_expected_count / hit_audit.expected_row_count if hit_audit.expected_row_count else None,
        },
        "dual_review": {
            "primary_coverage": audit.primary_review_coverage,
            "secondary_coverage": audit.secondary_review_coverage,
            "disagreement_count": audit.disagreement_count,
            "post_review_correction_count": audit.post_review_correction_count,
        },
    }


def validate_x1v2_witness_audit_artifacts(archive_root: Path, repository_root: Path) -> dict[str, object]:
    """Validate complete dual review, raw hashes, and hit aggregation without assigning labels."""

    packet = _load_packet(archive_root)
    primary = _decision_maps(archive_root, packet, "primary")
    secondary = _decision_maps(archive_root, packet, "secondary")
    input_closure = X1v2InputClosure.model_validate(
        _load_json(archive_root / "reference" / "x1v2_input_closure" / "manifest.json")
    )
    audit_path = archive_root / "derived" / "x1v2_witness_level_audit.json"
    hit_path = archive_root / "derived" / "x1v2_full_hit_max_witness_audit.json"
    adjudication_path = archive_root / "derived" / "x1v2_witness_adjudications.json"
    audit = X1v2WitnessLevelAudit.model_validate(_load_json(audit_path))
    hit_audit = X1v2FullHitMaxWitnessAudit.model_validate(_load_json(hit_path))
    adjudication_log = X1v2WitnessAdjudicationLog.model_validate(_load_json(adjudication_path))
    if input_closure.pair_count != 54 or packet.finding_count != 512 or audit.finding_count != 512:
        raise ValueError("input closure, review packet, and final audit must cover the frozen 54-pair/512-finding universe")
    packet_by_key = {item.audit_key: item for item in packet.work_items}
    preview = preview_x1v2_manual_reviews(archive_root)
    if adjudication_log.finding_count != packet.finding_count or adjudication_log.disagreement_count != len(preview.disagreement_keys):
        raise ValueError("adjudication log count does not match the reviewed finding universe")
    if {item.audit_key for item in adjudication_log.adjudications} != set(preview.disagreement_keys):
        raise ValueError("adjudication log keys do not exactly match W-level disagreements")
    correction_by_key = {item.audit_key: item for item in adjudication_log.post_review_corrections}
    if set(correction_by_key) - POST_REVIEW_CORRECTION_ALLOWLIST:
        raise ValueError("adjudication log contains a post-review correction outside the accepted allowlist")
    if adjudication_log.post_review_correction_count != len(correction_by_key):
        raise ValueError("adjudication log correction count is inconsistent")
    if {record.work_item.audit_key for record in audit.records} != set(packet_by_key):
        raise ValueError("final audit keys do not exactly match the label-free review packet")
    audit_correction_by_key = {
        record.work_item.audit_key: record.post_review_correction
        for record in audit.records
        if record.post_review_correction is not None
    }
    if set(audit_correction_by_key) != set(correction_by_key):
        raise ValueError("final audit and adjudication log post-review correction keys differ")
    if audit.post_review_correction_count != len(audit_correction_by_key):
        raise ValueError("final audit correction count is inconsistent")
    for correction in correction_by_key.values():
        review_path = archive_root / correction.independent_review_path
        if not review_path.is_file():
            raise ValueError(f"post-review correction review path is missing: {correction.independent_review_path}")
        if correction.audit_key not in review_path.read_text(encoding="utf-8"):
            raise ValueError(f"post-review correction review does not identify its audit key: {correction.independent_review_path}")
    associations = _judge_associations(archive_root)
    for record in audit.records:
        packet_item = packet_by_key[record.work_item.audit_key]
        blinded_item = record.work_item.model_copy(update={"judge_association": None})
        if blinded_item != packet_item:
            raise ValueError(f"final audit altered frozen work-item context: {record.work_item.audit_key}")
        if record.work_item.judge_association != associations[record.work_item.audit_key]:
            raise ValueError(f"final audit Judge association differs from the selected frozen result: {record.work_item.audit_key}")
        if record.primary_review != primary[record.work_item.audit_key]:
            raise ValueError(f"final audit primary review differs from the submitted decision: {record.work_item.audit_key}")
        if record.secondary_review != secondary[record.work_item.audit_key]:
            raise ValueError(f"final audit secondary review differs from the submitted decision: {record.work_item.audit_key}")
        if record.disagreement:
            adjudication = next(item for item in adjudication_log.adjudications if item.audit_key == record.work_item.audit_key)
            if record.adjudicator_id != adjudication.adjudicator_id or record.final_witness_level != adjudication.final_witness_level:
                raise ValueError(f"final audit disagreement resolution differs from adjudication log: {record.work_item.audit_key}")
        elif record.post_review_correction is not None:
            correction = correction_by_key.get(record.work_item.audit_key)
            if correction != record.post_review_correction:
                raise ValueError(f"final audit post-review correction differs from adjudication log: {record.work_item.audit_key}")
            if correction.audit_key not in POST_REVIEW_CORRECTION_ALLOWLIST:
                raise ValueError(f"final audit post-review correction is not allowed: {record.work_item.audit_key}")
        record_path = repository_root / record.work_item.method_record_repository_path
        if sha256_file(record_path) != record.work_item.method_record_sha256:
            raise ValueError(f"final audit method-record hash mismatch: {record.work_item.audit_key}")
        for source in (record.work_item.natural_language, record.work_item.plantuml):
            source_path = repository_root / source.repository_path
            if sha256_file(source_path) != source.sha256:
                raise ValueError(f"final audit source-input hash mismatch: {record.work_item.audit_key}")
    regenerated_hit = derive_x1v2_full_hit_witness_audit(archive_root, audit)
    if regenerated_hit != hit_audit:
        raise ValueError("recorded X1v2 full-hit witness audit differs from manual labels and frozen full_report_ids")
    return witness_audit_statistics(audit, hit_audit)
