"""Versioned, provider-free data contracts for final manual adjudication.

This module deliberately does not infer semantic labels from report text.  It
validates decisions made by a human reviewer and derives only the deterministic
validity/K-N-I closure required by issue #189/#195.
"""

from __future__ import annotations

import csv
import hashlib
import json
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Literal, Mapping, Sequence

from pydantic import BaseModel, ConfigDict, Field, model_validator


SCHEMA = "paper1.manual-adjudication.v2"
FINAL_STATUSES = {"ARBITRATED", "FINAL"}


class AdjudicationStatus(str, Enum):
    """Workflow status of one human adjudication record."""

    PROPOSAL = "PROPOSAL"
    INDEPENDENT_REVIEW = "INDEPENDENT_REVIEW"
    ARBITRATED = "ARBITRATED"
    FINAL = "FINAL"


class Side(str, Enum):
    """Frozen experiment arm owning a report."""

    V60_CURRENT = "v60_current"
    X1V2_BASELINE = "x1v2_baseline"


class FactStatus(str, Enum):
    """Result of checking the report's core fact against author-source evidence."""

    ESTABLISHED = "ESTABLISHED"
    REFUTED = "REFUTED"
    BLOCKED = "BLOCKED"


class StrictDA(str, Enum):
    """Final author-source defect/adjudication tier."""

    D2 = "D2"
    D1 = "D1"
    D0 = "D0"
    A0 = "A0"


class A0Type(str, Enum):
    """Allowed explanation when the report's author-source fact fails."""

    FALSE_POSITIVE = "FALSE_POSITIVE"
    NOT_A_DEFECT_CLAIM = "NOT_A_DEFECT_CLAIM"


class ReportValidity(str, Enum):
    """Deterministic report validity axis, independent from relation strength."""

    VALID_KNOWN = "VALID_KNOWN"
    VALID_NOVEL = "VALID_NOVEL"
    INVALID = "INVALID"


class Relation(str, Enum):
    """Relation between one report and one expected issue."""

    FULL_MATCH = "FULL_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"


class WitnessLevel(str, Enum):
    """Finding-level evidence strength."""

    W0 = "W0"
    W1 = "W1"
    W2 = "W2"


class BlockerStatus(str, Enum):
    """Lifecycle state for a review blocker."""

    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


class ReviewBlocker(BaseModel):
    """Structured evidence or process blocker that prevents final labeling."""

    model_config = ConfigDict(extra="forbid")

    blocker_id: str = Field(min_length=1, description="Stable blocker identifier.")
    reason: str = Field(min_length=1, description="Why the evidence or review is blocked.")
    opened_by: str = Field(min_length=1, description="Reviewer who opened the blocker.")
    opened_at: str = Field(min_length=1, description="UTC timestamp when the blocker opened.")
    status: BlockerStatus = Field(description="Whether the blocker remains open.")
    resolved_by: str | None = Field(default=None, description="Reviewer who resolved the blocker, if resolved.")
    resolved_at: str | None = Field(default=None, description="UTC resolution timestamp, if resolved.")
    resolution_refs: tuple[str, ...] = Field(default=(), description="Repository-relative evidence refs supporting closure.")

    @model_validator(mode="after")
    def validate_resolution(self) -> "ReviewBlocker":
        if self.status == BlockerStatus.OPEN and (self.resolved_by or self.resolved_at or self.resolution_refs):
            raise ValueError("open blocker cannot carry resolution fields")
        if self.status == BlockerStatus.RESOLVED and not (self.resolved_by and self.resolved_at and self.resolution_refs):
            raise ValueError("resolved blocker requires resolver, timestamp, and resolution_refs")
        return self


class SourceRef(BaseModel):
    """Stable repository-relative pointer to evidence used by an adjudicator."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(min_length=1, description="Repository-relative source or archived artifact path.")
    json_pointer: str | None = Field(default=None, description="JSON Pointer into the source, when applicable.")
    line: int | None = Field(default=None, ge=1, description="1-based source line, when applicable.")
    sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the referenced file or artifact fragment.")


class EvaluationReceipt(BaseModel):
    """Original terminal execution receipt required to classify a finding as W2."""

    model_config = ConfigDict(extra="forbid")

    artifact_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Exact evaluated artifact hash in the receipt.")
    artifact_repository_path: str = Field(min_length=1, description="Repository-relative path of the exact evaluated artifact.")
    receipt_id: str = Field(min_length=1, description="Stable original execution receipt identifier.")
    receipt_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the archived receipt file containing this receipt object.")
    terminal_result: Literal["true", "false"] = Field(description="Recorded terminal Boolean result; W2 cannot use timeout, unknown, or error.")
    repository_path: str = Field(min_length=1, description="Repository-relative path of the original receipt.")
    json_pointer: str = Field(min_length=1, description="JSON Pointer to the receipt object.")


class ExecutableObject(BaseModel):
    """Typed serialization of the original executable witness object."""

    model_config = ConfigDict(extra="forbid")

    object_type: str = Field(min_length=1, description="Stable executable witness object type.")
    predicate_id: str | None = Field(default=None, description="Frozen predicate ID, or null for a non-predicate executable witness.")
    typed_inputs_json: str = Field(min_length=2, description="Canonical JSON serialization of the complete typed input object.")
    typed_inputs_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of typed_inputs_json UTF-8 bytes.")
    artifact_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Exact artifact hash used by the executable witness.")
    program: str = Field(min_length=1, description="Original compiled or executable program representation.")
    program_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of program UTF-8 bytes.")
    backend: str = Field(min_length=1, description="Backend that produced the terminal result.")
    payload_json: str = Field(min_length=2, description="Canonical JSON serialization of the complete original witness object.")
    payload_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of payload_json UTF-8 bytes.")

    @model_validator(mode="after")
    def validate_serialized_payloads(self) -> "ExecutableObject":
        for field_name, value, digest in (
            ("typed_inputs_json", self.typed_inputs_json, self.typed_inputs_sha256),
            ("program", self.program, self.program_sha256),
            ("payload_json", self.payload_json, self.payload_sha256),
        ):
            if field_name != "program":
                try:
                    parsed = json.loads(value)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"{field_name} must contain valid JSON") from exc
                if not isinstance(parsed, (dict, list)):
                    raise ValueError(f"{field_name} must contain a JSON object or array")
                canonical = json.dumps(parsed, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                if value != canonical:
                    raise ValueError(f"{field_name} must use canonical JSON serialization")
            if "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest() != digest:
                raise ValueError(f"{field_name} hash does not match its serialized value")
        return self


class Witness(BaseModel):
    """Finding-level W evidence with W2 fields explicitly required when applicable."""

    model_config = ConfigDict(extra="forbid")

    level: WitnessLevel = Field(description="Human-audited finding-level evidence strength.")
    concrete_location: str = Field(min_length=1, description="Specific model/report location supporting W1 or W2.")
    executable_object: ExecutableObject | None = Field(default=None, description="Original typed executable object; required only for W2.")
    receipt: EvaluationReceipt | None = Field(default=None, description="Original terminal receipt; required only for W2.")
    degradation_reason: str | None = Field(default=None, description="Why a candidate was retained at W0/W1, if applicable.")

    @model_validator(mode="after")
    def validate_w2(self) -> "Witness":
        if self.level == WitnessLevel.W2:
            if self.executable_object is None or self.receipt is None:
                raise ValueError("W2 requires executable_object and receipt")
            if self.executable_object.artifact_sha256 != self.receipt.artifact_sha256:
                raise ValueError("W2 executable object and receipt must use the same artifact hash")
        elif self.receipt is not None or self.executable_object is not None:
            raise ValueError("W0/W1 cannot carry W2 executable evidence")
        return self


class RelationDecision(BaseModel):
    """One dense, expected-specific relation judgment for a report."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(min_length=1, description="Expected ledger issue ID being evaluated exactly once.")
    relation: Relation = Field(description="Human-adjudicated relation for this expected issue.")
    reason: str = Field(min_length=1, description="Expected-specific explanation of the relation.")
    basis: str = Field(min_length=1, description="Evidence basis for this relation, not a generic label.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Resolvable source refs for the expected-specific relation.")
    report_owned_field_refs: tuple[str, ...] = Field(min_length=1, description="Pointers to the report fields used in this relation decision.")


class RelationAuditRow(BaseModel):
    """Canonical row in the archive-level dense relation audit."""

    model_config = ConfigDict(extra="forbid")

    side: Side = Field(description="Frozen experiment side owning the report.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Four-digit pair owning the report.")
    round: int = Field(ge=1, le=3, description="Frozen round owning the report.")
    report_id: str = Field(min_length=1, description="Exact report decision identity.")
    expected_id: str = Field(min_length=1, description="Expected issue evaluated by this relation row.")
    relation: Relation = Field(description="Expected-specific human relation.")
    reason: str = Field(min_length=1, description="Expected-specific relation reason.")
    basis: str = Field(min_length=1, description="Expected-specific relation basis.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Resolvable relation evidence references.")
    report_owned_field_refs: tuple[str, ...] = Field(min_length=1, description="Report field references used for this relation.")


class RelationAuditSet(BaseModel):
    """Canonical envelope for all report-by-expected relation rows."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned manual adjudication schema identifier.")
    rows: tuple[RelationAuditRow, ...] = Field(min_length=1, description="Exactly one row for every report and expected issue pair.")

    @model_validator(mode="after")
    def validate_schema(self) -> "RelationAuditSet":
        if self.schema != SCHEMA:
            raise ValueError("unexpected relation audit schema")
        return self


class GroupDecision(BaseModel):
    """Human-assigned substantive group confined to one side and one pair."""

    model_config = ConfigDict(extra="forbid")

    side: Side = Field(description="Frozen experiment side owning every grouped report.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Single pair boundary for this group.")
    canonical_group_key: str = Field(min_length=1, description="Human-assigned group identity; never generated from text similarity.")
    report_ids: tuple[str, ...] = Field(min_length=1, description="Reports manually judged homogeneous for this group.")
    substantive_property: str = Field(min_length=1, description="Homogeneous substantive property supporting the merge.")
    author_source_locus: str = Field(min_length=1, description="Homogeneous author-source locus supporting the merge.")
    repair_obligation: str = Field(min_length=1, description="Homogeneous repair obligation supporting the merge.")
    substantive_cause: str = Field(min_length=1, description="Homogeneous substantive cause supporting the merge.")
    group_verdict: str = Field(pattern=r"^[NI]$", description="Only VALID_NOVEL or INVALID reports may form publication N/I groups.")
    reason: str = Field(min_length=1, description="Dedicated explanation for this human merge decision.")
    basis: str = Field(min_length=1, description="Evidence basis for homogeneous grouping.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Resolvable evidence refs for the group.")

    @model_validator(mode="after")
    def validate_identity(self) -> "GroupDecision":
        if not self.canonical_group_key.strip():
            raise ValueError("group identity is empty")
        if any(not report_id.strip() for report_id in self.report_ids):
            raise ValueError("group contains an empty report ID")
        return self


class HumanReview(BaseModel):
    """Primary, independent, and arbitrator attestations for one final decision."""

    model_config = ConfigDict(extra="forbid")

    primary_reviewer_id: str = Field(min_length=1, description="Human primary reviewer identity.")
    independent_reviewer_id: str = Field(min_length=1, description="Human independent reviewer identity.")
    final_adjudicator_id: str = Field(min_length=1, description="Human final adjudicator identity.")
    human_confirmation: bool = Field(description="Explicit human confirmation; subagents cannot set this true.")
    human_supervised_session: bool = Field(
        description="Whether the authorized pane5 session directly read and confirmed this record; this is not a second-human identity."
    )
    authorization_reference: str = Field(
        min_length=1,
        description="Stable repository reference to the user authorization for this human-supervised adjudication session."
    )
    authorization_message_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the persisted user authorization message; it proves authorization provenance without duplicating the prompt."
    )
    authorization_time_utc: str = Field(
        min_length=1,
        description="UTC time at which the user authorization was recorded."
    )
    attestation: str = Field(
        min_length=1,
        description="Human-supervised attestation that the primary session read the cited raw/source evidence and confirmed this final record."
    )
    independent_is_subagent_proposal: bool = Field(
        description="True when independent_reviewer_id identifies a subagent proposal rather than a human reviewer."
    )
    confirmed_at: str | None = Field(default=None, description="UTC timestamp of final human confirmation; absent while this record is a proposal.")
    confirmation_basis: str | None = Field(default=None, description="How the human read and confirmed the evidence; required only for a final record.")
    primary_reason: str = Field(min_length=1, description="Primary review reason.")
    primary_basis: str = Field(min_length=1, description="Primary review evidence basis.")
    independent_reason: str = Field(min_length=1, description="Independent review reason.")
    independent_basis: str = Field(min_length=1, description="Independent review evidence basis.")
    disagreement: str | None = Field(default=None, description="Recorded disagreement, if any.")
    arbitration_reason: str = Field(min_length=1, description="Final arbitration reason, including no-disagreement rationale.")
    arbitration_basis: str = Field(min_length=1, description="Final arbitration evidence basis.")
    reviewer_ids: tuple[str, ...] = Field(min_length=2, description="All reviewer identities participating in this decision.")
    review_status: AdjudicationStatus = Field(description="Decision workflow status.")
    review_blockers: tuple[ReviewBlocker, ...] = Field(default=(), description="Structured blockers; empty is required for FINAL.")
    reference_visible: bool = Field(description="Whether calibration reference labels were visible before first submission.")
    primary_visible: bool = Field(description="Whether primary decisions were visible before independent submission.")
    submission_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the blind first-submission payload.")
    independent_submission_at: str | None = Field(
        default=None,
        description="UTC time of the independent raw-first proposal submission; required for final records.",
    )
    primary_submission_at: str | None = Field(
        default=None,
        description="UTC time of the primary raw-first submission; required for final records.",
    )
    blind_event_sequence: tuple[str, ...] = Field(
        default=(),
        description="Ordered blind-review event IDs proving independent and primary submissions preceded unblinding.",
    )
    unblinded_at: str | None = Field(default=None, description="UTC time when reference/primary decisions became visible.")

    @model_validator(mode="after")
    def validate_workflow(self) -> "HumanReview":
        if self.review_status in FINAL_STATUSES and not self.human_confirmation:
            raise ValueError("ARBITRATED or FINAL status requires human confirmation")
        if self.review_status in FINAL_STATUSES:
            if not self.human_supervised_session:
                raise ValueError("final status requires the authorized human-supervised session")
            if not self.authorization_reference or not self.authorization_message_sha256 or not self.authorization_time_utc:
                raise ValueError("final status requires persisted user authorization provenance")
            if not self.attestation:
                raise ValueError("final status requires an attestation")
            if not self.confirmed_at or not self.confirmation_basis:
                raise ValueError("final status requires confirmation time and basis")
        if self.independent_is_subagent_proposal and not self.independent_reviewer_id.startswith("subagent:"):
            raise ValueError("subagent proposal reviewer IDs must use the subagent: prefix")
        if self.review_status == AdjudicationStatus.FINAL and self.review_blockers:
            raise ValueError("FINAL decision cannot retain review blockers")
        if self.review_status in FINAL_STATUSES and not self.reference_visible and not self.primary_visible and not self.unblinded_at:
            raise ValueError("blind review must record an unblinding time before finalization")
        if self.review_status in FINAL_STATUSES:
            if not self.independent_submission_at or not self.primary_submission_at:
                raise ValueError("final status requires blind submission timestamps")
            if len(self.blind_event_sequence) < 3:
                raise ValueError("final status requires the blind submission/unblinding event sequence")
        if self.primary_reviewer_id == self.independent_reviewer_id:
            raise ValueError("primary and independent reviewers must be distinct")
        return self


class Pane5ManualInput(BaseModel):
    """Explicit per-report input signed by the authorized pane5 session.

    This contract is intentionally separate from proposal records.  A producer
    must supply the semantic labels and expected-specific relation evidence;
    the confirmation backend may validate and derive closure, but cannot invent
    these fields from a legacy Judge or a proposal.
    """

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default="paper1.manual-adjudication.pane5-manual-input.v2", description="Explicit pane5 input schema version.")
    report_id: str = Field(min_length=1, description="Exact frozen report/finding ID being confirmed.")
    side: Side = Field(description="Frozen side owning this report.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Frozen four-digit pair ID.")
    round: int = Field(ge=1, le=3, description="Frozen round number.")
    raw_method_path: str = Field(min_length=1, description="Repository-relative raw method record path.")
    raw_json_pointer: str = Field(min_length=1, description="JSON Pointer to the exact raw report/finding.")
    raw_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the exact raw method record.")
    claim_pointer: str = Field(min_length=1, description="JSON Pointer to the report claim field.")
    where_pointer: str = Field(min_length=1, description="JSON Pointer to the report location field.")
    fact_status: FactStatus = Field(description="Pane5's fact finding before the D/A tier.")
    strict_da: StrictDA = Field(description="Pane5's final fact/obligation adjudication.")
    a0_type: A0Type | None = Field(default=None, description="A0 subtype, or null for D2/D1/D0.")
    relation_rows: tuple[RelationDecision, ...] = Field(min_length=1, description="Explicit expected-specific relation decisions; confirmation requires dense closure.")
    witness: Witness = Field(description="Pane5's independently confirmed finding-level W evidence.")
    canonical_group_key: str | None = Field(default=None, description="Explicit human group key for same-side, same-pair N/I grouping, or null for K.")
    reason: str = Field(min_length=1, description="Dedicated report reason stating fact, obligation, D/A, and validity implication.")
    basis: str = Field(min_length=1, description="Dedicated report evidence basis with resolvable source references.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Source references actually read by pane5 for this report.")
    evidence_digest: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Digest of the independently recorded raw/source evidence read.")
    raw_source_read: bool = Field(description="Pane5 confirms the exact raw target was read.")
    author_source_read: bool = Field(description="Pane5 confirms author NL and PlantUML were read.")
    human_confirmation: bool = Field(description="Must be true only for an explicit authorized pane5 confirmation.")
    human_supervised_session: bool = Field(description="Must be true only for the authorized pane5 session.")
    reviewer_id: str = Field(min_length=1, description="Authorized pane5 reviewer identity.")
    authorization_reference: str = Field(min_length=1, description="Stable user authorization reference.")
    authorization_message_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the persisted authorization payload.")
    attestation: str = Field(min_length=1, description="Per-report attestation of actual raw/source reading and confirmation.")
    confirmation_basis: str = Field(min_length=1, description="Per-report confirmation basis; must identify the actual evidence read.")
    confirmed_at: str = Field(min_length=1, description="UTC timestamp of this report's pane5 confirmation.")
    independent_submission_at: str = Field(min_length=1, description="UTC timestamp of the blind independent proposal submission.")
    primary_submission_at: str = Field(min_length=1, description="UTC timestamp of the blind primary submission.")
    blind_event_sequence: tuple[str, ...] = Field(min_length=3, description="Ordered event IDs for independent submission, primary submission, and unblinding.")
    unblinded_at: str = Field(min_length=1, description="UTC timestamp when blind submissions could be compared.")
    reference_visible: bool = Field(description="Must be false at first submission.")
    primary_visible: bool = Field(description="Must be false at independent first submission.")
    proposal_submission_hash: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the independent proposal retained as proposal-only evidence.")
    primary_reason: str = Field(min_length=1, description="Per-report primary review reason recorded before unblinding.")
    primary_basis: str = Field(min_length=1, description="Per-report primary review evidence basis recorded before unblinding.")
    independent_reason: str = Field(min_length=1, description="Per-report independent subagent proposal reason.")
    independent_basis: str = Field(min_length=1, description="Per-report independent subagent proposal basis.")
    disagreement: str | None = Field(default=None, description="Per-report disagreement observed after unblinding, if any.")
    arbitration_reason: str = Field(min_length=1, description="Per-report pane5 arbitration reason after comparing proposals.")
    arbitration_basis: str = Field(min_length=1, description="Per-report pane5 arbitration evidence basis.")
    review_status: AdjudicationStatus = Field(description="Explicit pane5 input workflow status.")

    @model_validator(mode="after")
    def validate_explicit_confirmation(self) -> "Pane5ManualInput":
        if self.schema != "paper1.manual-adjudication.pane5-manual-input.v2":
            raise ValueError("unexpected pane5 manual input schema")
        if not self.raw_source_read or not self.author_source_read:
            raise ValueError("pane5 input requires raw and author-source read flags")
        if not self.human_confirmation or not self.human_supervised_session:
            raise ValueError("pane5 input must be explicitly human-supervised")
        if not self.reference_visible and not self.primary_visible and len(self.blind_event_sequence) < 3:
            raise ValueError("pane5 input is missing blind event sequence")
        if self.strict_da == StrictDA.A0 and self.a0_type is None:
            raise ValueError("A0 pane5 input requires an A0 subtype")
        if self.strict_da != StrictDA.A0 and self.a0_type is not None:
            raise ValueError("only A0 pane5 input may carry an A0 subtype")
        if self.side == Side.X1V2_BASELINE and self.a0_type == A0Type.NOT_A_DEFECT_CLAIM:
            raise ValueError("X1v2 pane5 input cannot use NOT_A_DEFECT_CLAIM")
        if self.review_status not in {AdjudicationStatus.ARBITRATED, AdjudicationStatus.FINAL}:
            raise ValueError("pane5 manual input must be ARBITRATED or FINAL")
        if self.reviewer_id != "human:pane5-supervised-adjudicator":
            raise ValueError("pane5 manual input has an unauthorized reviewer")
        if self.report_id not in self.attestation or self.report_id not in self.confirmation_basis:
            raise ValueError("pane5 attestation and confirmation basis must be report-specific")
        for field_name in ("reason", "basis", "primary_reason", "primary_basis", "independent_reason", "independent_basis", "arbitration_reason", "arbitration_basis"):
            if self.report_id not in getattr(self, field_name):
                raise ValueError(f"pane5 {field_name} must be report-specific")
        return self


class ReportDecision(BaseModel):
    """Canonical human decision for exactly one frozen report/finding."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned manual adjudication schema identifier.")
    side: Side = Field(description="Frozen experiment side owning this report.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Four-digit frozen pair identifier.")
    round: int = Field(ge=1, le=3, description="Frozen method round number.")
    report_id: str = Field(min_length=1, description="Exact stable report/finding identity from raw artifact.")
    report_index: int = Field(ge=0, description="Zero-based report/finding index within the frozen raw record.")
    raw_method_path: str = Field(min_length=1, description="Repository-relative raw method record path.")
    raw_json_pointer: str = Field(min_length=1, description="JSON Pointer to the exact raw report/finding.")
    raw_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the raw method record.")
    claim_pointer: str = Field(min_length=1, description="Pointer or stable hash for the original claim/issue text.")
    where_pointer: str = Field(min_length=1, description="Pointer or stable hash for the original where/location text.")
    fact_status: FactStatus = Field(description="Author-source fact status before D/A classification.")
    strict_da: StrictDA = Field(description="Human D/A classification under the frozen protocol.")
    a0_type: A0Type | None = Field(default=None, description="A0 subtype; null for D2/D1/D0 and unavailable on X1v2.")
    validity: ReportValidity = Field(description="Final validity axis, closed against D/A and relations.")
    corrected_kni: str = Field(pattern=r"^[KNI]$", description="Deterministically derived report-level K/N/I closure.")
    relations: tuple[RelationDecision, ...] = Field(min_length=1, description="Dense relation decisions, exactly one per expected issue.")
    ledger_ids: tuple[str, ...] = Field(description="Expected ledger IDs with FULL relation; empty for no FULL relation.")
    witness: Witness = Field(description="Finding-level W audit, separate from validity and relation.")
    canonical_group_key: str | None = Field(default=None, description="Human-assigned same-side, same-pair substantive group key.")
    reason: str = Field(min_length=1, description="Dedicated explanation of fact, obligation, D/A, and validity.")
    basis: str = Field(min_length=1, description="Dedicated evidence basis for the final decision.")
    source_refs: tuple[SourceRef, ...] = Field(min_length=1, description="Resolvable author-source and artifact evidence refs.")
    review: HumanReview = Field(description="Primary, independent, arbitration, and blind-review attestations.")
    historical_compatibility: bool = Field(default=False, description="Whether a field is retained only for historical compatibility.")
    scoring: bool = Field(description="Whether this final report participates in the declared publication aggregate.")
    diagnostic_only: bool = Field(description="Whether this row is diagnostic-only and excluded from publication aggregates.")

    @model_validator(mode="after")
    def validate_closure(self) -> "ReportDecision":
        if self.schema != SCHEMA:
            raise ValueError(f"unexpected manual adjudication schema: {self.schema}")
        if not self.report_id.startswith(f"{self.pair_id}:r{self.round}:") and self.side == Side.V60_CURRENT:
            raise ValueError("v60 report_id does not close over pair and round")
        if self.side == Side.X1V2_BASELINE and self.a0_type == A0Type.NOT_A_DEFECT_CLAIM:
            raise ValueError("X1v2 cannot use NOT_A_DEFECT_CLAIM")
        if self.strict_da == StrictDA.A0 and self.a0_type is None:
            raise ValueError("A0 requires an A0 subtype")
        if self.strict_da != StrictDA.A0 and self.a0_type is not None:
            raise ValueError("only A0 may carry an A0 subtype")
        if self.strict_da == StrictDA.A0 and self.fact_status != FactStatus.REFUTED:
            raise ValueError("A0 requires a refuted author-source fact")
        if self.strict_da in {StrictDA.D2, StrictDA.D1, StrictDA.D0} and self.fact_status != FactStatus.ESTABLISHED:
            raise ValueError("D2/D1/D0 require an established author-source fact")
        if self.fact_status == FactStatus.BLOCKED:
            raise ValueError("a blocked fact cannot receive a final D/A label")
        positive = {item.relation for item in self.relations if item.relation != Relation.NO_MATCH}
        expected_kni = "I" if self.strict_da in {StrictDA.D0, StrictDA.A0} else ("K" if positive else "N")
        expected_validity = (
            ReportValidity.INVALID
            if self.strict_da in {StrictDA.D0, StrictDA.A0}
            else (ReportValidity.VALID_KNOWN if positive else ReportValidity.VALID_NOVEL)
        )
        if self.corrected_kni != expected_kni or self.validity != expected_validity:
            raise ValueError("D/A, validity, relation, and K/N/I do not close")
        if self.strict_da in {StrictDA.D0, StrictDA.A0} and positive:
            raise ValueError("D0/A0 must force all relations to NO_MATCH")
        full_ids = {row.expected_id for row in self.relations if row.relation == Relation.FULL_MATCH}
        if set(self.ledger_ids) != full_ids:
            raise ValueError("ledger_ids must exactly list FULL relation expected IDs")
        if self.review.review_status in FINAL_STATUSES and self.review.human_confirmation is not True:
            raise ValueError("final report decisions require human confirmation")
        return self


class ReportDecisionSet(BaseModel):
    """Canonical JSON envelope for one side's complete final report decisions."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned manual adjudication schema identifier.")
    side: Side = Field(description="Side shared by every decision in this file.")
    decisions: tuple[ReportDecision, ...] = Field(min_length=1, description="One final human decision for every raw report on this side.")

    @model_validator(mode="after")
    def validate_side(self) -> "ReportDecisionSet":
        if self.schema != SCHEMA:
            raise ValueError("unexpected decision-set schema")
        if any(item.side != self.side for item in self.decisions):
            raise ValueError("decision set contains another side")
        return self


class GroupDecisionSet(BaseModel):
    """Canonical envelope for manually assigned same-side, same-pair N/I groups."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned manual adjudication schema identifier.")
    groups: tuple[GroupDecision, ...] = Field(description="All manually confirmed publication groups.")

    @model_validator(mode="after")
    def validate_schema(self) -> "GroupDecisionSet":
        if self.schema != SCHEMA:
            raise ValueError("unexpected group decision schema")
        return self


class ManualAdjudicationManifest(BaseModel):
    """Machine-readable manifest binding canonical JSON, TSV, and raw input hashes."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Manual adjudication schema identifier.")
    generated_at_utc: str = Field(min_length=1, description="UTC generation time for this manifest.")
    protocol_version: str = Field(min_length=1, description="Frozen protocol version used by human reviewers.")
    raw_input_hashes: dict[str, str] = Field(min_length=1, description="Repository-relative immutable input path to SHA-256 map.")
    canonical_files: dict[str, str] = Field(min_length=1, description="Canonical JSON/TSV path to SHA-256 map.")
    report_counts: dict[str, int] = Field(min_length=1, description="Side-specific final decision counts.")
    status: AdjudicationStatus = Field(description="Aggregate workflow status; FINAL requires human-signed complete data.")
    review_blockers: tuple[ReviewBlocker, ...] = Field(default=(), description="Aggregate blockers preventing final use.")

    @model_validator(mode="after")
    def validate_manifest_status(self) -> "ManualAdjudicationManifest":
        if self.status == AdjudicationStatus.FINAL and self.review_blockers:
            raise ValueError("FINAL manifest cannot retain blockers")
        return self


class RawReportRef(BaseModel):
    """Immutable raw report index entry used to drive raw-first human review."""

    model_config = ConfigDict(extra="forbid")

    side: Side = Field(description="Frozen experiment side owning the raw report.")
    pair_id: str = Field(pattern=r"^[0-9]{4}$", description="Four-digit pair identity from the frozen record.")
    round: int = Field(ge=1, le=3, description="Frozen round number from the raw record.")
    report_id: str = Field(min_length=1, description="Exact report identity or archived baseline identity mapping.")
    report_index: int = Field(ge=0, description="Zero-based issue index within the raw record.")
    raw_method_path: str = Field(min_length=1, description="Repository-relative raw method record path.")
    raw_json_pointer: str = Field(min_length=1, description="JSON Pointer to the report/finding in the raw record.")
    raw_sha256: str = Field(pattern=r"^sha256:[0-9a-f]{64}$", description="SHA-256 of the raw method record.")
    claim_pointer: str = Field(min_length=1, description="JSON Pointer to the original issue/claim field.")
    where_pointer: str = Field(min_length=1, description="JSON Pointer to the original where/location field.")
    identity_basis: str = Field(min_length=1, description="Why this report ID closes over the raw record.")


class RawInventory(BaseModel):
    """Provider-free inventory of all frozen report/finding identities and source hashes."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default="paper1.manual-adjudication-raw-inventory.v1", description="Versioned raw inventory schema.")
    archive_relative_root: str = Field(min_length=1, description="Archive root used for all relative paths.")
    generated_at_utc: str = Field(min_length=1, description="UTC inventory generation timestamp.")
    source_manifests: dict[str, str] = Field(min_length=1, description="Immutable manifest path to SHA-256 map.")
    cells: dict[str, int] = Field(min_length=1, description="Side-specific frozen method cell counts.")
    reports: dict[str, int] = Field(min_length=1, description="Side-specific frozen report/finding counts.")
    by_round: dict[str, dict[str, int]] = Field(min_length=1, description="Side and round report counts.")
    items: tuple[RawReportRef, ...] = Field(min_length=1, description="All raw report references in deterministic path order.")

    @model_validator(mode="after")
    def validate_counts(self) -> "RawInventory":
        if sum(self.reports.values()) != len(self.items):
            raise ValueError("raw inventory report counts do not equal item count")
        ids = [item.report_id for item in self.items]
        if len(ids) != len(set(ids)):
            raise ValueError("raw inventory contains duplicate report IDs")
        return self


def derive_kni(strict_da: StrictDA, relations: Iterable[Relation]) -> tuple[str, ReportValidity]:
    """Derive K/N/I and validity without trusting a model-supplied aggregate label."""

    positive = any(relation in {Relation.FULL_MATCH, Relation.PARTIAL_MATCH} for relation in relations)
    if strict_da in {StrictDA.D0, StrictDA.A0}:
        return "I", ReportValidity.INVALID
    return ("K", ReportValidity.VALID_KNOWN) if positive else ("N", ReportValidity.VALID_NOVEL)


def validate_decision_set(
    decisions: Sequence[ReportDecision],
    *,
    expected_ids: Sequence[str],
    raw_report_index: Mapping[str, Mapping[str, Any]],
    require_final: bool = True,
) -> None:
    """Validate exact report closure, dense relation closure, and review blockers."""

    if not decisions:
        raise ValueError("manual decision set is empty")
    seen: set[str] = set()
    expected = set(expected_ids)
    for decision in decisions:
        if decision.report_id in seen:
            raise ValueError(f"duplicate final report decision: {decision.report_id}")
        seen.add(decision.report_id)
        raw = raw_report_index.get(decision.report_id)
        if raw is None:
            raise ValueError(f"report decision is not present in raw index: {decision.report_id}")
        closure_fields = (
            ("side", decision.side.value, raw["side"]),
            ("pair_id", decision.pair_id, raw["pair_id"]),
            ("round", decision.round, raw["round"]),
            ("report_index", decision.report_index, raw["report_index"]),
            ("raw_method_path", decision.raw_method_path, raw["raw_method_path"]),
            ("raw_json_pointer", decision.raw_json_pointer, raw["raw_json_pointer"]),
            ("raw_sha256", decision.raw_sha256, raw["raw_sha256"]),
        )
        if any(actual != expected_value for _, actual, expected_value in closure_fields):
            raise ValueError(f"raw closure mismatch: {decision.report_id}")
        if decision.claim_pointer != raw["claim_pointer"] or decision.where_pointer != raw["where_pointer"]:
            raise ValueError(f"raw claim/where pointer mismatch: {decision.report_id}")
        relation_ids = [row.expected_id for row in decision.relations]
        if set(relation_ids) != expected or len(relation_ids) != len(expected):
            raise ValueError(f"relation matrix is not dense for {decision.report_id}")
        if require_final:
            if decision.review.review_blockers:
                raise ValueError(f"open review blocker remains: {decision.report_id}")
            if decision.review.review_status not in FINAL_STATUSES or not decision.review.human_confirmation:
                raise ValueError(f"human final confirmation is missing: {decision.report_id}")
    if seen != set(raw_report_index):
        missing = sorted(set(raw_report_index) - seen)
        extra = sorted(seen - set(raw_report_index))
        raise ValueError(f"raw exact report closure failed; missing={missing[:3]} extra={extra[:3]}")


def json_sha256(value: Any) -> str:
    """Hash canonical JSON values using the same stable UTF-8 serialization everywhere."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def decisions_to_tsv_rows(decisions: Sequence[ReportDecision]) -> list[dict[str, str]]:
    """Render a fixed-column TSV mirror without changing the JSON source of truth."""

    columns = (
        "side", "pair_id", "round", "report_id", "report_index", "raw_method_path", "raw_json_pointer",
        "raw_sha256", "fact_status", "strict_da", "a0_type", "validity", "corrected_kni",
        "relation_summary", "ledger_ids", "witness_level", "canonical_group_key", "reason", "basis",
        "review_status", "human_confirmation",
    )
    rows: list[dict[str, str]] = []
    for decision in decisions:
        relation_summary = ";".join(f"{row.expected_id}={row.relation.value}" for row in decision.relations)
        rows.append({
            "side": decision.side.value,
            "pair_id": decision.pair_id,
            "round": str(decision.round),
            "report_id": decision.report_id,
            "report_index": str(decision.report_index),
            "raw_method_path": decision.raw_method_path,
            "raw_json_pointer": decision.raw_json_pointer,
            "raw_sha256": decision.raw_sha256,
            "fact_status": decision.fact_status.value,
            "strict_da": decision.strict_da.value,
            "a0_type": decision.a0_type.value if decision.a0_type else "",
            "validity": decision.validity.value,
            "corrected_kni": decision.corrected_kni,
            "relation_summary": relation_summary,
            "ledger_ids": ";".join(decision.ledger_ids),
            "witness_level": decision.witness.level.value,
            "canonical_group_key": decision.canonical_group_key or "",
            "reason": decision.reason,
            "basis": decision.basis,
            "review_status": decision.review.review_status.value,
            "human_confirmation": str(decision.review.human_confirmation).lower(),
        })
    return rows


def write_tsv_mirror(path: Path, decisions: Sequence[ReportDecision]) -> None:
    """Write the fixed-column TSV mirror from canonical Pydantic decisions."""

    rows = decisions_to_tsv_rows(decisions)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def validate_tsv_mirror(path: Path, decisions: Sequence[ReportDecision]) -> None:
    """Require a TSV mirror to equal the canonical fixed-column projection exactly."""

    expected = decisions_to_tsv_rows(decisions)
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        actual = list(reader)
        if reader.fieldnames != list(expected[0]):
            raise ValueError(f"TSV header does not match canonical columns: {path}")
    if actual != expected:
        raise ValueError(f"TSV mirror differs from canonical JSON projection: {path}")


def validate_group_decisions(
    groups: Sequence[GroupDecision],
    decisions: Sequence[ReportDecision],
) -> None:
    """Validate group membership against final N/I decisions and boundaries."""

    decision_by_id = {decision.report_id: decision for decision in decisions}
    grouped: set[str] = set()
    for group in groups:
        for report_id in group.report_ids:
            if report_id in grouped:
                raise ValueError(f"report belongs to multiple groups: {report_id}")
            decision = decision_by_id.get(report_id)
            if decision is None:
                raise ValueError(f"group references unknown report: {report_id}")
            if decision.side != group.side or decision.pair_id != group.pair_id:
                raise ValueError(f"group crosses side or pair boundary: {report_id}")
            if decision.corrected_kni != group.group_verdict:
                raise ValueError(f"group verdict does not match report decision: {report_id}")
            if decision.canonical_group_key != group.canonical_group_key:
                raise ValueError(f"group key does not match report decision: {report_id}")
            grouped.add(report_id)
    expected = {decision.report_id for decision in decisions if decision.corrected_kni in {"N", "I"}}
    if grouped != expected:
        missing = sorted(expected - grouped)
        extra = sorted(grouped - expected)
        raise ValueError(f"N/I group closure failed; missing={missing[:3]} extra={extra[:3]}")
