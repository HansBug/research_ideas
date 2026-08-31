"""Blind source packet generation for predicate-gold review tracks."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from pydantic import Field, JsonValue, model_validator

from .predicate_gold import (
    INVENTORY_SCHEMA_VERSION,
    SHA256_PATTERN,
    AlternativeReading,
    ArbitrationRecord,
    CandidateProperty,
    Confidence,
    ConflictRecord,
    ExactnessRelation,
    GoldMode,
    GoldStatus,
    NormalizedObligation,
    SourceRef,
    StrictModel,
    canonical_sha256,
    sha256_path,
    write_json,
)

PACKET_SCHEMA_VERSION = "paper1.predicate-gold.review-input-packet.v1"
PACKET_MANIFEST_SCHEMA_VERSION = "paper1.predicate-gold.review-input-manifest.v1"
TRACK_A_SCHEMA_VERSION = "paper1.predicate-gold.track-a-proposal.v1"
TRACK_B_SCHEMA_VERSION = "paper1.predicate-gold.track-b-proposal.v1"
TRACK_C_SCHEMA_VERSION = "paper1.predicate-gold.track-c-execution-review.v1"
HIGH_RISK_SCHEMA_VERSION = "paper1.predicate-gold.high-risk-review.v1"
TRACK_C_PACKET_SCHEMA_VERSION = "paper1.predicate-gold.track-c-input-packet.v1"
TRACK_C_MANIFEST_SCHEMA_VERSION = "paper1.predicate-gold.track-c-input-manifest.v1"
BATCH_ASSIGNMENT_SCHEMA_VERSION = "paper1.predicate-gold.review-batch-assignment.v1"
ARBITRATION_SCHEMA_VERSION = "paper1.predicate-gold.pane5-arbitration.v1"


class PreExecutionDisposition(str, Enum):
    """Track B disposition frozen before any property execution result is visible."""

    EXACT_EXECUTION_CANDIDATE = "EXACT_EXECUTION_CANDIDATE"
    COMPOSITE_EXACT_EXECUTION_CANDIDATE = "COMPOSITE_EXACT_EXECUTION_CANDIDATE"
    PROXY_EXECUTION_CANDIDATE = "PROXY_EXECUTION_CANDIDATE"
    UNSUPPORTED_EXACT_CANDIDATE = "UNSUPPORTED_EXACT_CANDIDATE"


class NumberedLine(StrictModel):
    """One exact physical source line retained for blind semantic review."""

    number: int = Field(description="One-based physical line number.", ge=1)
    text: str = Field(description="Exact line text without the trailing newline; an empty string represents a blank line.")


class LedgerAxes(StrictModel):
    """Frozen defect-axis fields copied from one current ledger item."""

    defect_locus: str = Field(description="Frozen defect locus from ledger.json.", min_length=1)
    defect_element: str | None = Field(description="Frozen defect element from ledger.json, or null for relation-level items without one element.")
    defect_qualifier: str | None = Field(description="Frozen defect qualifier from ledger.json, or null when the ledger does not define one.")
    defect_logic_kind: str | None = Field(description="Frozen logic-kind qualifier, or null when absent from the ledger.")
    defect_reference: str = Field(description="Frozen reference axis from ledger.json.", min_length=1)


class LedgerSourceText(StrictModel):
    """Original pre-rewrite ledger provenance fields retained for comparison."""

    statement: str = Field(description="Original ledger statement retained in _source_text.", min_length=1)
    verdict_reason: str | None = Field(description="Original verdict reason, or null when absent.")
    meta_review: str | None = Field(description="Original meta-review text, or null when absent.")
    l_basis_rule: str | None = Field(description="Original L-tier basis rule, or null when absent.")
    l_decided_by: str | None = Field(description="Original L-tier decision provenance, or null when absent.")


class BlindLedgerItem(StrictModel):
    """Current ledger item projected without any planned or actual predicate data."""

    ledger_id: str = Field(description="Immutable current ledger identity.", min_length=1)
    pair_id: str = Field(description="Four-digit source pair identity.", pattern=r"^[0-9]{4}$")
    d_tier: Literal["D2", "D1"] = Field(description="Frozen current-ledger D tier.")
    d_basis: str = Field(description="Complete current-ledger D-tier basis.", min_length=1)
    l_tier: Literal["L2", "L1", "L0"] = Field(description="Frozen current-ledger L tier.")
    l_basis: str = Field(description="Complete current-ledger L-tier basis.", min_length=1)
    summary: str = Field(description="Current-ledger one-paragraph issue summary.", min_length=1)
    detail: str = Field(description="Current-ledger detailed source-first issue statement.", min_length=1)
    axes: LedgerAxes = Field(description="Frozen ledger defect axes.")
    origin_family: str = Field(description="Frozen issue-origin family text.", min_length=1)
    worksheet_ref: SourceRef = Field(description="Stable provenance worksheet reference.")
    ledger_json_pointer: str = Field(description="RFC 6901 pointer to this ledger item.", min_length=1)
    source_text: LedgerSourceText = Field(description="Original source-text fields preserved by ledger v2.")


class SourceDocument(StrictModel):
    """Hash-bound NL or PlantUML source document with exact numbered lines."""

    role: Literal["AUTHOR_NL", "AUTHOR_PLANTUML"] = Field(description="Author-source role of this document.")
    repository_path: str = Field(description="Repository-relative source path.", min_length=1)
    sha256: str = Field(description="SHA-256 of the exact file bytes.", pattern=SHA256_PATTERN)
    lines: tuple[NumberedLine, ...] = Field(description="Complete ordered physical lines from the source file.", min_length=1)


class FrozenMetadataRef(StrictModel):
    """Hash-bound source or FCSTM metadata supplied as provenance, not truth."""

    role: Literal["SOURCE_META", "FCSTM_META"] = Field(description="Metadata role.")
    repository_path: str = Field(description="Repository-relative metadata path.", min_length=1)
    sha256: str = Field(description="SHA-256 of the metadata file bytes.", pattern=SHA256_PATTERN)
    selected_fields: dict[str, JsonValue] = Field(description="Non-semantic provenance and eligibility fields selected mechanically from frozen metadata.")


class ReviewVisibility(StrictModel):
    """Information intentionally hidden from blind Track A and B review."""

    planned_predicate_mapping_visible: Literal[False] = Field(description="Frozen registry planned mapping is hidden during issue-level blind review.")
    v60_actual_predicate_visible: Literal[False] = Field(description="Frozen v60 actual predicate/input outputs are hidden during issue-level blind review.")
    other_track_conclusions_visible: Literal[False] = Field(description="Other review-track conclusions are hidden before this packet is answered.")
    execution_results_visible: Literal[False] = Field(description="Property execution results are hidden until O/P proposals are hashed.")


class BlindReviewInputPacket(StrictModel):
    """Complete source-first blind input for one pair's Track A or Track B review."""

    schema_version: Literal[PACKET_SCHEMA_VERSION] = Field(default=PACKET_SCHEMA_VERSION, description="Blind review packet schema version.")
    pair_id: str = Field(description="Four-digit pair identity.", pattern=r"^[0-9]{4}$")
    ledger_sha256: str = Field(description="Hash of the complete current ledger bytes.", pattern=SHA256_PATTERN)
    ledger_items: tuple[BlindLedgerItem, ...] = Field(description="All current ledger issues belonging to this pair.", min_length=1)
    nl: SourceDocument = Field(description="Complete author NL with physical line numbers.")
    plantuml: SourceDocument = Field(description="Complete author PlantUML with physical line numbers.")
    metadata_refs: tuple[FrozenMetadataRef, ...] = Field(description="Frozen source and FCSTM metadata refs supplied only for provenance and capability boundaries.", min_length=2)
    visibility: ReviewVisibility = Field(description="Blind-review information boundary.")
    instructions: tuple[str, ...] = Field(description="Track-neutral source-first instructions that forbid semantic shortcuts.", min_length=1)
    packet_sha256: str = Field(description="Canonical digest of every packet field except this digest.", pattern=SHA256_PATTERN)


class PacketManifestEntry(StrictModel):
    """One packet path and digest in the blind review input manifest."""

    pair_id: str = Field(description="Four-digit pair identity.", pattern=r"^[0-9]{4}$")
    packet_path: str = Field(description="Gold-root-relative packet path.", min_length=1)
    packet_sha256: str = Field(description="Canonical packet digest stored inside the packet.", pattern=SHA256_PATTERN)
    file_sha256: str = Field(description="SHA-256 of serialized packet bytes.", pattern=SHA256_PATTERN)
    ledger_ids: tuple[str, ...] = Field(description="Ledger IDs included in the packet.", min_length=1)


class PacketManifest(StrictModel):
    """Manifest proving complete one-packet-per-pair blind input coverage."""

    schema_version: Literal[PACKET_MANIFEST_SCHEMA_VERSION] = Field(default=PACKET_MANIFEST_SCHEMA_VERSION, description="Blind packet manifest schema version.")
    inventory_schema_version: Literal[INVENTORY_SCHEMA_VERSION] = Field(description="Frozen inventory schema used to locate source artifacts.")
    generated_at: str = Field(description="UTC packet generation time supplied by the caller.", min_length=1)
    ledger_sha256: str = Field(description="Hash of the complete current ledger bytes.", pattern=SHA256_PATTERN)
    pair_count: int = Field(description="Number of packet entries.", ge=1)
    ledger_item_count: int = Field(description="Number of ledger IDs covered by all packets.", ge=1)
    entries: tuple[PacketManifestEntry, ...] = Field(description="One entry per current-ledger pair.", min_length=1)
    notes: tuple[str, ...] = Field(description="Blindness and non-truth status of the packet contents.", min_length=1)


class ReviewBatchAssignment(StrictModel):
    """One mutually exclusive pair batch shared by independent review tracks."""

    batch_id: str = Field(description="Stable batch identity.", pattern=r"^batch_[0-9]{2}$")
    pair_ids: tuple[str, ...] = Field(description="Ordered pair IDs assigned to this batch.", min_length=1)
    ledger_ids: tuple[str, ...] = Field(description="All ledger IDs owned by the assigned pairs.", min_length=1)
    item_count: int = Field(description="Mechanically derived number of assigned ledger IDs.", ge=1)


class ReviewBatchManifest(StrictModel):
    """Complete non-overlapping assignment of 145 ledger issues to review batches."""

    schema_version: Literal[BATCH_ASSIGNMENT_SCHEMA_VERSION] = Field(default=BATCH_ASSIGNMENT_SCHEMA_VERSION, description="Review batch assignment schema version.")
    input_manifest_path: str = Field(description="Gold-root-relative blind packet manifest path.", min_length=1)
    input_manifest_sha256: str = Field(description="File hash of the blind packet manifest.", pattern=SHA256_PATTERN)
    batches: tuple[ReviewBatchAssignment, ...] = Field(description="Mutually exclusive review batches covering all current ledger IDs.", min_length=1)
    pair_count: int = Field(description="Total assigned pair count.", ge=1)
    ledger_item_count: int = Field(description="Total assigned ledger item count.", ge=1)
    track_a_visibility: str = Field(description="Information boundary for Track A.", min_length=1)
    track_b_visibility: str = Field(description="Information boundary for Track B.", min_length=1)
    track_c_visibility: str = Field(description="Information boundary and sequencing for Track C.", min_length=1)


class TrackAProposalRow(StrictModel):
    """Blind Track A recovery of one normalized obligation without predicate visibility."""

    ledger_id: str = Field(description="Immutable current ledger identity.", min_length=1)
    packet_sha256: str = Field(description="Digest of the blind pair packet read by this reviewer.", pattern=SHA256_PATTERN)
    normalized_obligation: NormalizedObligation = Field(description="Independent source-first reconstruction of obligation O.")
    alternative_readings: tuple[AlternativeReading, ...] = Field(description="All source-compatible and rejected adjacent readings considered independently.")
    reason: str = Field(description="Issue-specific Track A obligation-normalization reason.", min_length=1)
    basis: str = Field(description="Issue-specific Track A NL, PlantUML, ledger, and formal-semantics basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Evidence actually read for this Track A row.", min_length=2)
    confidence: Confidence = Field(description="Track A confidence; it does not replace evidence.")
    other_tracks_visible: Literal[False] = Field(description="Track B/C conclusions were not visible before this row was frozen.")
    v60_actual_visible: Literal[False] = Field(description="v60 actual predicate/input output was not visible before this row was frozen.")
    reviewed_at: str = Field(description="UTC row freeze time.", min_length=1)
    proposal_sha256: str = Field(description="Canonical digest of this row excluding this field.", pattern=SHA256_PATTERN)

    def expected_proposal_sha256(self) -> str:
        """Return the canonical hash expected for this persisted proposal row."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"proposal_sha256"}))

    @model_validator(mode="after")
    def validate_proposal_sha256(self) -> TrackAProposalRow:
        """Reject a Track A row whose payload changed after review."""

        if self.proposal_sha256 != self.expected_proposal_sha256():
            raise ValueError("Track A proposal_sha256 does not match the row payload")
        return self


class TrackAProposalBatch(StrictModel):
    """One hash-bound Track A batch covering mutually exclusive ledger pairs."""

    schema_version: Literal[TRACK_A_SCHEMA_VERSION] = Field(default=TRACK_A_SCHEMA_VERSION, description="Track A proposal schema version.")
    batch_id: str = Field(description="Stable batch identity from the frozen assignment manifest.", min_length=1)
    reviewer_id: str = Field(description="Internal Track A reviewer identity.", min_length=1)
    input_manifest_sha256: str = Field(description="File hash of the blind input packet manifest.", pattern=SHA256_PATTERN)
    pair_ids: tuple[str, ...] = Field(description="Mutually exclusive pair identities assigned to this batch.", min_length=1)
    rows: tuple[TrackAProposalRow, ...] = Field(description="Exactly one blind obligation proposal per assigned ledger ID.", min_length=1)
    submitted_at: str = Field(description="UTC batch submission time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical hash expected for this persisted Track A batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> TrackAProposalBatch:
        """Reject duplicate ledger rows or a changed Track A batch payload."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("Track A batch contains duplicate ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("Track A batch_sha256 does not match the batch payload")
        return self


class TrackBProposalRow(StrictModel):
    """Blind Track B predicate, typed-input, and exactness proposal before execution."""

    ledger_id: str = Field(description="Immutable current ledger identity.", min_length=1)
    packet_sha256: str = Field(description="Digest of the blind pair packet read by this reviewer.", pattern=SHA256_PATTERN)
    fcstm_sha256: str = Field(description="Hash of the executable FCSTM snapshot inspected only for native binding.", pattern=SHA256_PATTERN)
    normalized_obligation: NormalizedObligation = Field(description="Track B's independent source-first reconstruction of O, not copied from Track A.")
    alternative_readings: tuple[AlternativeReading, ...] = Field(description="Track B's independently considered adjacent readings.")
    candidate_properties: tuple[CandidateProperty, ...] = Field(description="All semantically credible candidates with explicit O/P direction.", min_length=1)
    selected_candidate_id: str | None = Field(description="Candidate selected as exact gold or nearest proxy; null only when none is sound.")
    rejected_candidate_ids: tuple[str, ...] = Field(description="Candidates rejected as exact gold after semantic comparison.")
    proposed_disposition: PreExecutionDisposition = Field(description="Exact, composite, proxy, or unsupported candidate disposition before any execution verdict.")
    proposed_mode: GoldMode = Field(description="Pre-execution frozen predicate, composite, evaluation-only, proxy, or unsupported mode.")
    proposed_exactness_relation: ExactnessRelation = Field(description="Pre-execution O/P relation for the selected candidate.")
    unsupported_reason: str | None = Field(description="Pre-execution reason no exact property can be expressed; null when exact execution is proposed.")
    capability_gaps: tuple[str, ...] = Field(description="Specific backend/pyfcstm semantic gaps after checking predicates, composites, and evaluation-only oracles.")
    reason: str = Field(description="Issue-specific Track B selection and rejected-candidate reason.", min_length=1)
    basis: str = Field(description="Issue-specific Track B source, backend, typed-input, and semantics basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Source and backend evidence actually read for this proposal.", min_length=2)
    confidence: Confidence = Field(description="Track B confidence; it does not replace source and backend evidence.")
    other_tracks_visible: Literal[False] = Field(description="Track A/C conclusions were not visible before this row was frozen.")
    v60_actual_visible: Literal[False] = Field(description="v60 actual predicate/input output was not visible before this row was frozen.")
    execution_results_visible: Literal[False] = Field(description="No candidate execution result was visible before this proposal hash was frozen.")
    reviewed_at: str = Field(description="UTC row freeze time.", min_length=1)
    proposal_sha256: str = Field(description="Canonical digest of this row excluding this field.", pattern=SHA256_PATTERN)

    def expected_proposal_sha256(self) -> str:
        """Return the canonical hash expected for this persisted proposal row."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"proposal_sha256"}))

    @model_validator(mode="after")
    def validate_proposal_sha256(self) -> TrackBProposalRow:
        """Reject candidate identity errors or a post-freeze Track B mutation."""

        candidate_ids = [candidate.candidate_id for candidate in self.candidate_properties]
        if len(candidate_ids) != len(set(candidate_ids)):
            raise ValueError("Track B candidate IDs must be unique within one ledger row")
        selected = [candidate.candidate_id for candidate in self.candidate_properties if candidate.selected]
        if self.selected_candidate_id is None:
            if selected:
                raise ValueError("Track B selected flags exist while selected_candidate_id is null")
        elif selected != [self.selected_candidate_id]:
            raise ValueError("Track B selected_candidate_id must identify exactly one selected candidate")
        if not set(self.rejected_candidate_ids).issubset(set(candidate_ids)):
            raise ValueError("Track B rejected_candidate_ids contains an unknown candidate")
        if self.proposal_sha256 != self.expected_proposal_sha256():
            raise ValueError("Track B proposal_sha256 does not match the row payload")
        return self


class TrackBProposalBatch(StrictModel):
    """One hash-bound Track B batch covering mutually exclusive ledger pairs."""

    schema_version: Literal[TRACK_B_SCHEMA_VERSION] = Field(default=TRACK_B_SCHEMA_VERSION, description="Track B proposal schema version.")
    batch_id: str = Field(description="Stable batch identity from the frozen assignment manifest.", min_length=1)
    reviewer_id: str = Field(description="Internal Track B reviewer identity.", min_length=1)
    input_manifest_sha256: str = Field(description="File hash of the blind input packet manifest.", pattern=SHA256_PATTERN)
    capability_audit_sha256: str = Field(description="Hash of the source-level 19-predicate capability audit used by Track B.", pattern=SHA256_PATTERN)
    pair_ids: tuple[str, ...] = Field(description="Mutually exclusive pair identities assigned to this batch.", min_length=1)
    rows: tuple[TrackBProposalRow, ...] = Field(description="Exactly one independent property proposal per assigned ledger ID.", min_length=1)
    submitted_at: str = Field(description="UTC batch submission time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical hash expected for this persisted Track B batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> TrackBProposalBatch:
        """Reject duplicate ledger rows or a changed Track B batch payload."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("Track B batch contains duplicate ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("Track B batch_sha256 does not match the batch payload")
        return self


class TrackCInputArtifact(StrictModel):
    """One hash-bound artifact intentionally visible to post-execution Track C."""

    role: str = Field(description="Source, proposal, query, receipt, replay, control, runtime, or formal-semantics role.", min_length=1)
    repository_path: str = Field(description="Repository-relative artifact path.", min_length=1)
    sha256: str = Field(description="Hash of exact visible artifact bytes.", pattern=SHA256_PATTERN)
    json_pointer: str | None = Field(description="Issue-local JSON pointer when only one row is relevant; otherwise null.")
    reason: str = Field(description="Why Track C needs this artifact to assess O/P or execution closure.", min_length=1)


class TrackCInputPacket(StrictModel):
    """Issue-local post-execution packet that excludes v60 actual output."""

    schema_version: Literal[TRACK_C_PACKET_SCHEMA_VERSION] = Field(default=TRACK_C_PACKET_SCHEMA_VERSION, description="Track C packet schema version.")
    ledger_id: str = Field(description="Immutable ledger issue reviewed by this packet.", min_length=1)
    pair_id: str = Field(description="Four-digit source pair identity.", pattern=r"^[0-9]{4}$")
    track_a_proposal_sha256: str = Field(description="Hash of the blind Track A row.", pattern=SHA256_PATTERN)
    track_b_proposal_sha256: str = Field(description="Hash of the blind pre-execution Track B row.", pattern=SHA256_PATTERN)
    selected_candidate_id: str = Field(description="Frozen Track B candidate reviewed after execution.", min_length=1)
    proposed_exactness_relation: ExactnessRelation = Field(description="Pre-execution O/P direction that Track C must independently verify.")
    artifacts: tuple[TrackCInputArtifact, ...] = Field(description="Complete visible source/proposal/execution/control/replay artifact set.", min_length=10)
    prior_tracks_visible: Literal[True] = Field(description="Track C intentionally sees frozen Track A and Track B proposals.")
    execution_results_visible: Literal[True] = Field(description="Track C intentionally sees defective/control receipts and replay audits.")
    v60_actual_visible: Literal[False] = Field(description="Frozen method actual predicate/input output remains excluded.")
    created_at: str = Field(description="UTC packet creation time.", min_length=1)
    packet_sha256: str = Field(description="Canonical packet digest excluding this field.", pattern=SHA256_PATTERN)

    def expected_packet_sha256(self) -> str:
        """Return the canonical digest expected for this Track C packet."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"packet_sha256"}))

    @model_validator(mode="after")
    def validate_packet_sha256(self) -> TrackCInputPacket:
        """Reject duplicate artifact roles/paths or a changed input packet."""

        keys = [(item.role, item.repository_path, item.json_pointer) for item in self.artifacts]
        if len(keys) != len(set(keys)):
            raise ValueError("Track C packet contains duplicate artifact entries")
        if self.packet_sha256 != self.expected_packet_sha256():
            raise ValueError("Track C packet_sha256 does not match the packet payload")
        return self


class TrackCInputManifest(StrictModel):
    """Manifest of issue-local Track C packets for one execution-review batch."""

    schema_version: Literal[TRACK_C_MANIFEST_SCHEMA_VERSION] = Field(default=TRACK_C_MANIFEST_SCHEMA_VERSION, description="Track C packet manifest schema version.")
    batch_id: str = Field(description="Stable Track C batch identity.", min_length=1)
    packet_paths: tuple[str, ...] = Field(description="Gold-root-relative packet paths.", min_length=1)
    packet_file_sha256: tuple[str, ...] = Field(description="File hashes in packet_paths order.", min_length=1)
    packet_payload_sha256: tuple[str, ...] = Field(description="Canonical packet hashes in packet_paths order.", min_length=1)
    ledger_ids: tuple[str, ...] = Field(description="Ledger IDs in packet_paths order.", min_length=1)
    created_at: str = Field(description="UTC manifest creation time.", min_length=1)
    notes: tuple[str, ...] = Field(description="Visibility, independence, and non-truth boundaries.", min_length=1)
    manifest_sha256: str = Field(description="Canonical manifest digest excluding this field.", pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def validate_manifest_sha256(self) -> TrackCInputManifest:
        """Require aligned unique entries and a sealed manifest payload."""

        lengths = {len(self.packet_paths), len(self.packet_file_sha256), len(self.packet_payload_sha256), len(self.ledger_ids)}
        if len(lengths) != 1:
            raise ValueError("Track C manifest arrays must have equal lengths")
        if len(self.ledger_ids) != len(set(self.ledger_ids)):
            raise ValueError("Track C manifest contains duplicate ledger IDs")
        expected = canonical_sha256(self.model_dump(mode="json", exclude={"manifest_sha256"}))
        if self.manifest_sha256 != expected:
            raise ValueError("Track C manifest_sha256 does not match the manifest payload")
        return self


class TrackCReviewRow(StrictModel):
    """Independent post-execution review of O/P direction, binding, controls, and replay."""

    ledger_id: str = Field(description="Immutable current ledger identity.", min_length=1)
    input_packet_sha256: str = Field(description="Digest of the issue-local Track C packet and every visible artifact hash.", pattern=SHA256_PATTERN)
    track_a_proposal_sha256: str = Field(description="Hash of the independently frozen Track A obligation proposal.", pattern=SHA256_PATTERN)
    track_b_proposal_sha256: str = Field(description="Hash of the independently frozen pre-execution Track B property proposal.", pattern=SHA256_PATTERN)
    normalized_obligation_sha256: str = Field(description="Hash of the normalized obligation reviewed by Track C.", pattern=SHA256_PATTERN)
    property_proposal_sha256: str = Field(description="Hash that bound the selected property before execution.", pattern=SHA256_PATTERN)
    proposed_status: GoldStatus = Field(description="Track C's proposed exact, composite, proxy, or unsupported final disposition.")
    proposed_exactness_relation: ExactnessRelation = Field(description="Track C's independently checked logical relation between O and the selected P.")
    obligation_accepted: bool = Field(description="Whether Track A/B obligation differences are resolved by the cited author source.")
    property_relation_accepted: bool = Field(description="Whether the selected property's quantifier, scope, timing, and implication direction are justified.")
    typed_inputs_accepted: bool = Field(description="Whether every input value and native binding is source-provenanced and non-invented.")
    completed_false_accepted: bool = Field(description="Whether the defective execution ended in a completed Boolean false rather than failure or unknown.")
    positive_control_accepted: bool = Field(description="Whether the independent control is justified, completed true, and unpolluted by result selection.")
    replay_accepted: bool = Field(description="Whether the saved provider-free semantic replay matches the original receipt.")
    counterexample_accepted: bool = Field(description="Whether persisted constituent observations or traces explain the false result without overclaiming exactness.")
    vacuity_check: Literal["PASS", "FAIL", "NOT_APPLICABLE"] = Field(description="Vacuity, empty-domain, unreachable-antecedent, and empty-inventory review disposition.")
    contamination_check: Literal["PASS", "FAIL"] = Field(description="Whether proposal and control bytes were frozen without consulting same-issue execution results or v60 actual output.")
    conflicts: tuple[str, ...] = Field(description="A/B/execution disagreements requiring pane5 arbitration; empty only when evidence is aligned.")
    reason: str = Field(description="Issue-specific Track C judgment; false alone is never treated as exactness proof.", min_length=1)
    basis: str = Field(description="Issue-specific O/P, typed-input, receipt, control, counterexample, and replay basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Track A/B, source, query, receipt, control, and replay evidence actually checked.", min_length=4)
    prior_tracks_visible: Literal[True] = Field(description="Track C intentionally reviews frozen Track A/B proposals after execution.")
    v60_actual_visible: Literal[False] = Field(description="v60 actual predicate/input output remains hidden from Track C gold review.")
    confidence: Confidence = Field(description="Track C confidence; it does not replace source and execution evidence.")
    reviewed_at: str = Field(description="UTC opinion freeze time.", min_length=1)
    opinion_sha256: str = Field(description="Canonical digest of this row excluding this field.", pattern=SHA256_PATTERN)

    def expected_opinion_sha256(self) -> str:
        """Return the canonical digest expected for this persisted Track C row."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"opinion_sha256"}))

    @model_validator(mode="after")
    def validate_opinion_sha256(self) -> TrackCReviewRow:
        """Reject a Track C opinion whose reviewed payload changed after freeze."""

        if self.opinion_sha256 != self.expected_opinion_sha256():
            raise ValueError("Track C opinion_sha256 does not match the row payload")
        return self


class TrackCReviewBatch(StrictModel):
    """Hash-bound independent Track C review batch after execution and replay."""

    schema_version: Literal[TRACK_C_SCHEMA_VERSION] = Field(default=TRACK_C_SCHEMA_VERSION, description="Track C review schema version.")
    batch_id: str = Field(description="Stable Track C batch identity.", min_length=1)
    reviewer_id: str = Field(description="Internal Track C reviewer identity.", min_length=1)
    input_manifest_path: str = Field(description="Gold-root-relative Track C packet manifest path.", min_length=1)
    input_manifest_sha256: str = Field(description="Hash of the Track C packet manifest bytes.", pattern=SHA256_PATTERN)
    pair_ids: tuple[str, ...] = Field(description="Pair identities reviewed by this batch.", min_length=1)
    rows: tuple[TrackCReviewRow, ...] = Field(description="One independent post-execution opinion per ledger issue.", min_length=1)
    submitted_at: str = Field(description="UTC batch submission time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical digest expected for this persisted Track C batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> TrackCReviewBatch:
        """Reject duplicate opinions or a changed Track C batch payload."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("Track C batch contains duplicate ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("Track C batch_sha256 does not match the batch payload")
        return self


class HighRiskReviewRow(StrictModel):
    """Independent fourth opinion for exactness-sensitive and disputed rows."""

    ledger_id: str = Field(description="Immutable current ledger identity.", min_length=1)
    input_sha256: str = Field(description="Digest binding all source, A/B/C, proposal, receipt, control, and replay inputs visible to this review.", pattern=SHA256_PATTERN)
    track_a_opinion_sha256: str = Field(description="Hash of the blind Track A opinion reviewed.", pattern=SHA256_PATTERN)
    track_b_opinion_sha256: str = Field(description="Hash of the blind pre-execution Track B opinion reviewed.", pattern=SHA256_PATTERN)
    track_c_opinion_sha256: str = Field(description="Hash of the post-execution Track C opinion reviewed.", pattern=SHA256_PATTERN)
    normalized_obligation_sha256: str = Field(description="Hash of normalized obligation O checked against author source.", pattern=SHA256_PATTERN)
    property_proposal_sha256: str = Field(description="Hash of the selected or nearest property proposal reviewed.", pattern=SHA256_PATTERN)
    proposed_status: GoldStatus = Field(description="Fourth reviewer's evidence-based final-status proposal.")
    proposed_exactness_relation: ExactnessRelation = Field(description="Fourth reviewer's independently checked O/P relation.")
    proposed_predicate_ids: tuple[str, ...] = Field(description="Frozen predicate IDs supported by this opinion; empty for evaluation-only or unsupported rows.")
    obligation_accepted: bool = Field(description="Whether the normalized obligation preserves source quantifier, scope, timing, and alternatives.")
    property_relation_accepted: bool = Field(description="Whether the proposed O/P implication direction is justified independently of the Boolean result.")
    typed_inputs_accepted: bool = Field(description="Whether every bound input is source-provenanced and non-invented.")
    execution_closure_accepted: bool = Field(description="Whether completed false, positive control, counterexample, and replay evidence close for executable rows.")
    conflicts: tuple[str, ...] = Field(description="Specific disagreements or sensitivities that pane5 must arbitrate.")
    reason: str = Field(description="Issue-specific independent status and exactness judgment.", min_length=1)
    basis: str = Field(description="Issue-specific source, semantics, backend, receipt, control, and replay basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Evidence actually read by the fourth reviewer.", min_length=4)
    prior_tracks_visible: Literal[True] = Field(description="The fourth reviewer intentionally sees frozen A/B/C opinions after they are sealed.")
    v60_actual_visible: Literal[False] = Field(description="Frozen v60 actual predicate/input output remains hidden.")
    confidence: Confidence = Field(description="Reviewer confidence; evidence and arbitration remain controlling.")
    reviewed_at: str = Field(description="UTC opinion freeze time.", min_length=1)
    opinion_sha256: str = Field(description="Canonical digest of this row excluding this field.", pattern=SHA256_PATTERN)

    def expected_input_sha256(self) -> str:
        """Return the digest of all declared fourth-review inputs."""

        return canonical_sha256(
            {
                "track_a": self.track_a_opinion_sha256,
                "track_b": self.track_b_opinion_sha256,
                "track_c": self.track_c_opinion_sha256,
                "normalized_obligation": self.normalized_obligation_sha256,
                "property_proposal": self.property_proposal_sha256,
                "source_refs": [
                    item.model_dump(mode="json") for item in self.source_refs
                ],
            }
        )

    def expected_opinion_sha256(self) -> str:
        """Return the canonical digest expected for this fourth-review row."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"opinion_sha256"}))

    @model_validator(mode="after")
    def validate_opinion_sha256(self) -> HighRiskReviewRow:
        """Reject a fourth-review opinion whose payload changed after freeze."""

        if self.input_sha256 != self.expected_input_sha256():
            raise ValueError("high-risk input_sha256 does not bind declared inputs")
        if self.opinion_sha256 != self.expected_opinion_sha256():
            raise ValueError("high-risk opinion_sha256 does not match the row payload")
        return self


class HighRiskReviewBatch(StrictModel):
    """Hash-bound fourth-review batch covering a disjoint ledger slice."""

    schema_version: Literal[HIGH_RISK_SCHEMA_VERSION] = Field(default=HIGH_RISK_SCHEMA_VERSION, description="High-risk review schema version.")
    batch_id: str = Field(description="Stable high-risk review batch identity.", min_length=1)
    reviewer_id: str = Field(description="Internal fourth-reviewer identity.", min_length=1)
    pair_ids: tuple[str, ...] = Field(description="Pair identities reviewed by this batch.", min_length=1)
    rows: tuple[HighRiskReviewRow, ...] = Field(description="One independent fourth opinion per included ledger issue.", min_length=1)
    submitted_at: str = Field(description="UTC batch submission time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical digest expected for this fourth-review batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> HighRiskReviewBatch:
        """Require unique rows, matching pairs, and an unchanged batch payload."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("high-risk review batch contains duplicate ledger IDs")
        if {ledger_id.split("-")[1] for ledger_id in ledger_ids} != set(self.pair_ids):
            raise ValueError("high-risk review pair_ids do not match row ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("high-risk batch_sha256 does not match the batch payload")
        return self


class Pane5ArbitrationRow(StrictModel):
    """One final source-based arbitration bound to all four review opinions."""

    ledger_id: str = Field(description="Immutable current ledger issue being arbitrated.", min_length=1)
    track_a_opinion_sha256: str = Field(description="Hash of the blind Track A row.", pattern=SHA256_PATTERN)
    track_b_opinion_sha256: str = Field(description="Hash of the blind pre-execution Track B row.", pattern=SHA256_PATTERN)
    track_c_opinion_sha256: str = Field(description="Hash of the post-proposal Track C row.", pattern=SHA256_PATTERN)
    high_risk_opinion_sha256: str = Field(description="Hash of the independent fourth-review row.", pattern=SHA256_PATTERN)
    conflicts: tuple[ConflictRecord, ...] = Field(description="All retained A/B/C/fourth-review disagreements and their evidence-based resolutions.")
    arbitration: ArbitrationRecord = Field(description="Pane5 final status, relation, reason, basis and sensitivity decision.")
    row_sha256: str = Field(description="Canonical digest of this row excluding this field.", pattern=SHA256_PATTERN)

    def expected_row_sha256(self) -> str:
        """Return the canonical digest expected for this arbitration row."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"row_sha256"}))

    @model_validator(mode="after")
    def validate_row_sha256(self) -> Pane5ArbitrationRow:
        """Require identity/status closure and reject a changed arbitration row."""

        if self.arbitration.arbitration_id != f"predicate-gold-v1:{self.ledger_id}":
            raise ValueError("arbitration_id must be derived from ledger_id")
        if self.row_sha256 != self.expected_row_sha256():
            raise ValueError("row_sha256 does not match arbitration payload")
        return self


class Pane5ArbitrationBatch(StrictModel):
    """Hash-bound pane5 arbitration batch for one or more reviewed pairs."""

    schema_version: Literal[ARBITRATION_SCHEMA_VERSION] = Field(default=ARBITRATION_SCHEMA_VERSION, description="Pane5 arbitration batch schema version.")
    batch_id: str = Field(description="Stable arbitration batch identity.", min_length=1)
    pair_ids: tuple[str, ...] = Field(description="Pair identities closed by this batch.", min_length=1)
    rows: tuple[Pane5ArbitrationRow, ...] = Field(description="One final arbitration per included ledger issue.", min_length=1)
    arbitrated_at: str = Field(description="UTC batch completion time.", min_length=1)
    batch_sha256: str = Field(description="Canonical digest of this batch excluding this field.", pattern=SHA256_PATTERN)

    def expected_batch_sha256(self) -> str:
        """Return the canonical digest expected for this arbitration batch."""

        return canonical_sha256(self.model_dump(mode="json", exclude={"batch_sha256"}))

    @model_validator(mode="after")
    def validate_batch_sha256(self) -> Pane5ArbitrationBatch:
        """Require unique rows, matching pair IDs and a correct batch digest."""

        ledger_ids = [row.ledger_id for row in self.rows]
        if len(ledger_ids) != len(set(ledger_ids)):
            raise ValueError("arbitration batch contains duplicate ledger IDs")
        if {ledger_id.split("-")[1] for ledger_id in ledger_ids} != set(self.pair_ids):
            raise ValueError("arbitration pair_ids do not match row ledger IDs")
        if self.batch_sha256 != self.expected_batch_sha256():
            raise ValueError("batch_sha256 does not match arbitration payload")
        return self


def _repo_relative(repo_root: Path, path: Path) -> str:
    """Return a normalized repository-relative path."""

    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def _numbered_lines(path: Path) -> tuple[NumberedLine, ...]:
    """Read one complete UTF-8 source document into numbered physical lines."""

    return tuple(NumberedLine(number=index, text=text) for index, text in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1))


def _source_ref(repo_root: Path, path: Path) -> SourceRef:
    """Create a file-level source reference for one frozen provenance file."""

    return SourceRef(
        repository_path=_repo_relative(repo_root, path),
        sha256=sha256_path(path),
        json_pointer=None,
        line_start=None,
        line_end=None,
        model_element=None,
        excerpt=None,
    )


def build_blind_packets(*, repo_root: Path, paper_root: Path) -> tuple[BlindReviewInputPacket, ...]:
    """Build pair-local packets without planned predicates, actual outputs, or verdicts."""

    ledger_path = paper_root / "discover_matrix" / "ledger_v2" / "ledger.json"
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    ledger_hash = sha256_path(ledger_path)
    pair_items: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for ledger_id, item in ledger["items"].items():
        pair_items[item["pair"]].append((ledger_id, item))

    packets: list[BlindReviewInputPacket] = []
    for pair_id in sorted(pair_items):
        first_item = pair_items[pair_id][0][1]
        nl_path = (ledger_path.parent / first_item["pair_context"]["nl_file"]).resolve()
        plantuml_path = (ledger_path.parent / first_item["pair_context"]["stm0_file"]).resolve()
        source_meta_path = nl_path.parent / "source_meta.json"
        fcstm_meta_path = nl_path.parent / "fcstm_meta.json"
        source_meta = json.loads(source_meta_path.read_text(encoding="utf-8"))
        fcstm_meta = json.loads(fcstm_meta_path.read_text(encoding="utf-8"))
        projected_items: list[BlindLedgerItem] = []
        for ledger_id, item in pair_items[pair_id]:
            worksheet_path = (ledger_path.parent / item["worksheet"]).resolve()
            source_text = item["_source_text"]
            projected_items.append(
                BlindLedgerItem(
                    ledger_id=ledger_id,
                    pair_id=pair_id,
                    d_tier=item["D"],
                    d_basis=item["D_basis"],
                    l_tier=item["L"],
                    l_basis=item["L_basis"],
                    summary=item["summary"],
                    detail=item["detail"],
                    axes=LedgerAxes(**item["axes"]),
                    origin_family=item["origin_family"],
                    worksheet_ref=_source_ref(repo_root, worksheet_path),
                    ledger_json_pointer=f"/items/{ledger_id.replace('~', '~0').replace('/', '~1')}",
                    source_text=LedgerSourceText(
                        statement=source_text["statement"],
                        verdict_reason=source_text.get("verdict_reason"),
                        meta_review=source_text.get("meta_review"),
                        l_basis_rule=source_text.get("L_basis_rule"),
                        l_decided_by=source_text.get("L_decided_by"),
                    ),
                )
            )
        unsigned: dict[str, Any] = {
            "schema_version": PACKET_SCHEMA_VERSION,
            "pair_id": pair_id,
            "ledger_sha256": ledger_hash,
            "ledger_items": [item.model_dump(mode="json") for item in projected_items],
            "nl": SourceDocument(role="AUTHOR_NL", repository_path=_repo_relative(repo_root, nl_path), sha256=sha256_path(nl_path), lines=_numbered_lines(nl_path)).model_dump(mode="json"),
            "plantuml": SourceDocument(role="AUTHOR_PLANTUML", repository_path=_repo_relative(repo_root, plantuml_path), sha256=sha256_path(plantuml_path), lines=_numbered_lines(plantuml_path)).model_dump(mode="json"),
            "metadata_refs": [
                FrozenMetadataRef(role="SOURCE_META", repository_path=_repo_relative(repo_root, source_meta_path), sha256=sha256_path(source_meta_path), selected_fields={"source_pair_id": source_meta["source_pair_id"], "source_locator": source_meta["source_locator"], "selected_stage": source_meta["selected_stage"], "stm0_role": source_meta["stm0_role"]}).model_dump(mode="json"),
                FrozenMetadataRef(role="FCSTM_META", repository_path=_repo_relative(repo_root, fcstm_meta_path), sha256=sha256_path(fcstm_meta_path), selected_fields={"artifact_role": fcstm_meta["artifact_role"], "parse_status": fcstm_meta["parse_status"], "source_static_discover_eligible": fcstm_meta["source_static_discover_eligible"], "simulation_status": fcstm_meta["simulation_status"], "academic_eligible": fcstm_meta["academic_eligible"], "academic_ineligibility_reason": fcstm_meta.get("academic_ineligibility_reason")}).model_dump(mode="json"),
            ],
            "visibility": ReviewVisibility(planned_predicate_mapping_visible=False, v60_actual_predicate_visible=False, other_track_conclusions_visible=False, execution_results_visible=False).model_dump(mode="json"),
            "instructions": [
                "Recover obligation O from the complete NL, author PlantUML, ledger reasoning, and cited formal semantics before proposing any executable property.",
                "Do not infer inputs from state-name similarity, old planned mappings, v60 actual outputs, reference models, or execution results.",
                "State missing quantifier, scope, timing, domain, bound, or environment information explicitly instead of inventing it.",
            ],
        }
        packets.append(BlindReviewInputPacket(**unsigned, packet_sha256=canonical_sha256(unsigned)))
    return tuple(packets)


def write_blind_packets(*, repo_root: Path, paper_root: Path, output_root: Path, generated_at: str) -> PacketManifest:
    """Write all blind pair packets and their complete coverage manifest."""

    packets = build_blind_packets(repo_root=repo_root, paper_root=paper_root)
    entries: list[PacketManifestEntry] = []
    for packet in packets:
        path = output_root / "pairs" / f"{packet.pair_id}.json"
        write_json(path, packet.model_dump(mode="json"))
        entries.append(
            PacketManifestEntry(
                pair_id=packet.pair_id,
                packet_path=path.relative_to(output_root.parent.parent).as_posix(),
                packet_sha256=packet.packet_sha256,
                file_sha256=sha256_path(path),
                ledger_ids=tuple(item.ledger_id for item in packet.ledger_items),
            )
        )
    ledger_ids = [ledger_id for entry in entries for ledger_id in entry.ledger_ids]
    manifest = PacketManifest(
        inventory_schema_version=INVENTORY_SCHEMA_VERSION,
        generated_at=generated_at,
        ledger_sha256=packets[0].ledger_sha256,
        pair_count=len(entries),
        ledger_item_count=len(ledger_ids),
        entries=tuple(entries),
        notes=(
            "Packets intentionally exclude registry planned mappings, v60 actual predicate/input outputs, other-track conclusions, and all execution results.",
            "Ledger D/L and reasoning are frozen inputs; packets are review material and do not themselves constitute predicate gold.",
        ),
    )
    write_json(output_root / "manifest.json", manifest.model_dump(mode="json"))
    return manifest


def _parser() -> argparse.ArgumentParser:
    """Build the blind packet generation parser."""

    parser = argparse.ArgumentParser(description="Generate hash-bound blind predicate-gold review packets.")
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--generated-at", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Write blind input packets without executing predicates or providers."""

    args = _parser().parse_args(argv)
    manifest = write_blind_packets(
        repo_root=args.repo_root,
        paper_root=args.paper_root,
        output_root=args.output_root,
        generated_at=args.generated_at,
    )
    print(json.dumps({"pair_count": manifest.pair_count, "ledger_item_count": manifest.ledger_item_count, "output_root": str(args.output_root)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
