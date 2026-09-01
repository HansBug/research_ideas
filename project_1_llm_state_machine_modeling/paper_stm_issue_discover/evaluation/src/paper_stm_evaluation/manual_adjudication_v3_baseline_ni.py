"""Typed contracts for the X1v2 baseline non-K manual re-review layer.

The v3 layer is intentionally separate from the frozen v2 archive.  It stores
only the re-reviewed non-K reports and derives report validity and K/N/I from
the human D/A decision plus the dense expected-relation rows.
"""

from __future__ import annotations

import hashlib
import json
from enum import Enum
from typing import Iterable, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


SCHEMA = "paper1.manual-adjudication.v3-baseline-ni"
PROTOCOL = "issue-189-195-baseline-ni-v3"
ARBITRATION_LOG_PATH = "reviews/arbitration_log_v3.json"


def arbitration_record_pointer(report_id: str) -> str:
    """Return the stable archive-relative pointer for one pane5 arbitration."""

    return f"{ARBITRATION_LOG_PATH}#/entries_by_report_id/{report_id}"


class ReviewStatus(str, Enum):
    """Workflow status of a v3 review record."""

    PROPOSAL = "PROPOSAL"
    INDEPENDENT_REVIEW = "INDEPENDENT_REVIEW"
    ARBITRATED = "ARBITRATED"
    FINAL = "FINAL"


class FactStatus(str, Enum):
    """Whether the report's author-source fact is established or refuted."""

    ESTABLISHED = "ESTABLISHED"
    REFUTED = "REFUTED"


class NormativeStatus(str, Enum):
    """Whether a source-backed normative violation is established."""

    ESTABLISHED = "ESTABLISHED"
    NOT_ESTABLISHED = "NOT_ESTABLISHED"


class DefectClaimStatus(str, Enum):
    """Whether the report makes an author-source defect claim."""

    DEFECT_CLAIM = "DEFECT_CLAIM"
    NO_DEFECT_CLAIM = "NO_DEFECT_CLAIM"


class DATier(str, Enum):
    """Final D/A tier assigned after fact and obligation review."""

    D2 = "D2"
    D1 = "D1"
    D0 = "D0"
    A0 = "A0"


class A0Type(str, Enum):
    """Reason an author-source fact or defect attribution is false."""

    FALSE_POSITIVE = "FALSE_POSITIVE"
    NOT_A_DEFECT_CLAIM = "NOT_A_DEFECT_CLAIM"


class Validity(str, Enum):
    """Final report validity derived from D/A and relation rows."""

    VALID_KNOWN = "VALID_KNOWN"
    VALID_NOVEL = "VALID_NOVEL"
    INVALID = "INVALID"


class Relation(str, Enum):
    """Expected-specific relation assigned to one report."""

    FULL_MATCH = "FULL_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"


class WitnessLevel(str, Enum):
    """Independent evidence strength of a baseline finding."""

    W0 = "W0"
    W1 = "W1"
    W2 = "W2"


class BlockerStatus(str, Enum):
    """Lifecycle state of one structured review blocker."""

    OPEN = "OPEN"
    RESOLVED = "RESOLVED"


class GroupKind(str, Enum):
    """Whether a group represents a novel issue or an invalid-claim cluster."""

    SUBSTANTIVE_N = "SUBSTANTIVE_N"
    INVALID_DIAGNOSTIC_CLUSTER = "INVALID_DIAGNOSTIC_CLUSTER"


class GroupingCriterion(str, Enum):
    """Homogeneity criterion that was not established for a non-merge."""

    NORMATIVE_OBLIGATION = "NORMATIVE_OBLIGATION"
    SOURCE_LOCUS = "SOURCE_LOCUS"
    ROOT_CAUSE = "ROOT_CAUSE"
    REPAIR_INTENT = "REPAIR_INTENT"
    DIAGNOSTIC_PRESERVATION = "DIAGNOSTIC_PRESERVATION"


class RawFindingText(BaseModel):
    """Immutable text copied from the exact baseline finding target."""

    model_config = ConfigDict(extra="forbid")

    issue: str = Field(description="Original raw issue text, copied without semantic rewriting.", min_length=1)
    where: str = Field(description="Original raw where/location text, copied without semantic rewriting.", min_length=1)
    reason: str = Field(description="Original raw reason text; may be empty only when raw omitted it.")
    basis: str | None = Field(description="Original raw basis text, or null when the frozen producer omitted it.")


class SourceRef(BaseModel):
    """Archive-relative evidence pointer used by a final v3 decision."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(description="Repository-relative frozen input or v3 evidence path.", min_length=1)
    json_pointer: str | None = Field(description="RFC 6901 pointer into a JSON evidence file, if applicable.")
    line: int | None = Field(description="One-based source line, if the evidence is line-addressable.", ge=1)
    sha256: str = Field(description="SHA-256 of the referenced file bytes.", pattern=r"^sha256:[0-9a-f]{64}$")


class NonMergeReasonV3(BaseModel):
    """Pair-local evidence explaining one conservative N non-merge."""

    model_config = ConfigDict(extra="forbid")

    neighbor_report_id: str = Field(description="The other final-N report considered for this pair-local non-merge.", min_length=1)
    decision: Literal["CONSERVATIVE_NO_MERGE"] = Field(description="Conservative non-merge decision; it is not proof that either report is a distinct defect.")
    unestablished_criteria: tuple[GroupingCriterion, ...] = Field(description="Homogeneity criteria not established by the recorded evidence for this neighbor.", min_length=1)
    reason: str = Field(description="Dedicated report-pair reason for retaining two final-N reports separately.", min_length=1)
    basis: str = Field(description="Evidence basis naming the compared report/source records and the conservative limitation.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Archive-relative refs for both reports used in this non-merge assessment.", min_length=1)


class ReviewBlocker(BaseModel):
    """Structured blocker that must be resolved before a final label is allowed."""

    model_config = ConfigDict(extra="forbid")

    blocker_id: str = Field(description="Stable blocker identifier.", min_length=1)
    reason: str = Field(description="Evidence or process reason for the blocker.", min_length=1)
    opened_by: str = Field(description="Reviewer opening the blocker.", min_length=1)
    opened_at: str = Field(description="UTC time when the blocker opened.", min_length=1)
    status: BlockerStatus = Field(description="Open or resolved blocker status.")
    resolved_by: str | None = Field(description="Reviewer closing the blocker, when resolved.")
    resolved_at: str | None = Field(description="UTC close time, when resolved.")
    resolution_refs: tuple[str, ...] = Field(description="Evidence refs proving blocker closure.")

    @model_validator(mode="after")
    def validate_lifecycle(self) -> "ReviewBlocker":
        if self.status == BlockerStatus.OPEN and (self.resolved_by or self.resolved_at or self.resolution_refs):
            raise ValueError("open blocker cannot carry resolution fields")
        if self.status == BlockerStatus.RESOLVED and not (self.resolved_by and self.resolved_at and self.resolution_refs):
            raise ValueError("resolved blocker requires resolver, timestamp, and resolution refs")
        return self


class RelationDecision(BaseModel):
    """One expected-specific relation row with its own evidence explanation."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="One of the 145 ledger expected IDs, evaluated exactly once.", min_length=1)
    relation: Relation = Field(description="Human relation for this expected issue.")
    reason: str = Field(description="Dedicated expected-specific relation reason.", min_length=1)
    basis: str = Field(description="Evidence basis for this relation, not a generic report label.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Resolvable raw/source/ledger refs supporting this row.", min_length=1)
    report_owned_field_refs: tuple[str, ...] = Field(description="Raw report pointers used for this relation.", min_length=1)


class Witness(BaseModel):
    """Baseline finding W evidence kept separate from semantic validity."""

    model_config = ConfigDict(extra="forbid")

    level: WitnessLevel = Field(description="Human-audited W0/W1/W2 evidence level.")
    concrete_locations: tuple[str, ...] = Field(description="Specific source/model locations supporting the W level.")
    executable_object: str | None = Field(description="Typed executable witness serialization; required for W2.")
    receipt: SourceRef | None = Field(description="Original terminal receipt ref; required for W2.")
    artifact_sha256: str | None = Field(description="Exact evaluated artifact hash; required for W2.", pattern=r"^sha256:[0-9a-f]{64}$")
    terminal_result: Literal["true", "false"] | None = Field(description="Terminal result from the original baseline run; required for W2.")
    reason: str = Field(description="Finding-specific reason for the W level and any degradation.", min_length=1)
    basis: str = Field(description="Finding-specific W evidence basis.", min_length=1)

    @model_validator(mode="after")
    def validate_level(self) -> "Witness":
        if self.level == WitnessLevel.W2:
            if not (self.executable_object and self.receipt and self.artifact_sha256 and self.terminal_result):
                raise ValueError("W2 requires executable object, receipt, artifact hash, and terminal result")
        elif self.executable_object or self.receipt or self.artifact_sha256 or self.terminal_result:
            raise ValueError("W0/W1 cannot carry W2-only fields")
        return self


class ReviewOpinion(BaseModel):
    """One independent raw-first opinion retained as proposal evidence."""

    model_config = ConfigDict(extra="forbid")

    reviewer_id: str = Field(description="Independent reviewer or pane5 reviewer identity.", min_length=1)
    review_status: ReviewStatus = Field(description="Proposal/review status; this opinion is not itself final.")
    fact_status: FactStatus = Field(description="Reviewer fact finding from author source.")
    d_tier: DATier = Field(description="Reviewer D/A proposal.")
    relation_digest: str = Field(description="Hash of the reviewer's complete 145-row relation proposal.", pattern=r"^sha256:[0-9a-f]{64}$")
    positive_expected_ids: tuple[str, ...] = Field(description="Expected IDs proposed as FULL or PARTIAL, possibly empty.")
    reason: str = Field(description="Reviewer-specific reason.", min_length=1)
    basis: str = Field(description="Reviewer-specific source basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Raw/source refs read by this reviewer.", min_length=1)
    submitted_at: str = Field(description="UTC proposal submission time.", min_length=1)
    submission_hash: str = Field(description="Hash of this blind opinion payload.", pattern=r"^sha256:[0-9a-f]{64}$")
    reference_visible: bool = Field(description="Whether frozen reference labels were visible before submission.")
    primary_visible: bool = Field(description="Whether another primary decision was visible before submission.")


class ReviewChain(BaseModel):
    """Primary, two independent proposals, and pane5 arbitration evidence."""

    model_config = ConfigDict(extra="forbid")

    primary_reviewer_id: str = Field(description="Authorized pane5 primary reviewer identity.", min_length=1)
    independent_reviewer_ids: tuple[str, ...] = Field(description="At least two independent raw-first proposal identities.", min_length=2)
    independent_opinions: tuple[ReviewOpinion, ...] = Field(description="Independent raw-first proposal opinions.", min_length=2)
    primary_reason: str = Field(description="Pane5 primary raw/source reread reason.", min_length=1)
    primary_basis: str = Field(description="Pane5 primary evidence basis.", min_length=1)
    disagreement_flag: bool = Field(description="Whether independent opinions disagreed with one another or pane5.")
    disagreement_details: str | None = Field(description="Dedicated disagreement record, required when disagreement_flag is true.")
    arbitration_reason: str = Field(description="Pane5 final arbitration reason.", min_length=1)
    arbitration_basis: str = Field(description="Pane5 final arbitration source basis.", min_length=1)
    arbitration_record_pointer: str = Field(description="Archive-relative JSON pointer to the persisted pane5 arbitration record for this report.", min_length=1)
    final_adjudicator_id: str = Field(description="Authorized pane5 final adjudicator identity.", min_length=1)
    human_confirmation: bool = Field(description="Explicit pane5 human-supervised confirmation.")
    confirmation_time_utc: str = Field(description="UTC final confirmation time.", min_length=1)
    confirmation_basis: str = Field(description="Evidence actually read before confirmation.", min_length=1)
    human_session_reference: str = Field(description="Auditable pane5 session/attestation reference.", min_length=1)
    review_status: ReviewStatus = Field(description="Final workflow status for this report.")
    review_blockers: tuple[ReviewBlocker, ...] = Field(description="Structured blockers; empty for FINAL.")
    reference_visible: bool = Field(description="Frozen reference labels visible before blind submission.")
    primary_visible: bool = Field(description="Primary label visible before independent submissions.")
    unblinded_at: str = Field(description="UTC unblind time after all blind submissions.", min_length=1)
    blind_event_sequence: tuple[str, ...] = Field(description="Ordered independent/primary/unblind event IDs.", min_length=3)

    @model_validator(mode="after")
    def validate_chain(self) -> "ReviewChain":
        if self.primary_reviewer_id != "human:pane5-supervised-adjudicator":
            raise ValueError("v3 primary reviewer must be the authorized pane5 adjudicator")
        if self.final_adjudicator_id != self.primary_reviewer_id:
            raise ValueError("v3 final adjudicator must be pane5")
        if len(set(self.independent_reviewer_ids)) != len(self.independent_reviewer_ids):
            raise ValueError("independent reviewer identities must be distinct")
        if set(self.independent_reviewer_ids) != {op.reviewer_id for op in self.independent_opinions}:
            raise ValueError("independent reviewer IDs do not match retained opinions")
        if any(not reviewer.startswith("subagent:") for reviewer in self.independent_reviewer_ids):
            raise ValueError("independent v3 reviewers must be explicit subagent proposals")
        if self.disagreement_flag and not self.disagreement_details:
            raise ValueError("disagreement details are required when disagreement_flag is true")
        if not self.arbitration_record_pointer.startswith(f"{ARBITRATION_LOG_PATH}#/entries_by_report_id/"):
            raise ValueError("arbitration record pointer must target the v3 arbitration log")
        if self.review_status == ReviewStatus.FINAL and (not self.human_confirmation or self.review_blockers):
            raise ValueError("FINAL review requires human confirmation and no blockers")
        if not self.reference_visible and not self.primary_visible and len(self.blind_event_sequence) < 3:
            raise ValueError("blind review event sequence is incomplete")
        return self


class BaselineReportDecisionV3(BaseModel):
    """Canonical pane5 decision for exactly one originally non-K baseline report."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned v3 baseline non-K decision schema.")
    protocol_version: str = Field(default=PROTOCOL, description="Frozen D/A/relation/grouping protocol version.")
    side: Literal["x1v2_baseline"] = Field(description="Only X1v2 baseline is in this v3 layer.")
    pair_id: str = Field(description="Four-digit baseline pair ID.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen baseline round.", ge=1, le=3)
    original_report_id: str = Field(description="Stable archived report identity.", min_length=1)
    finding_index: int = Field(description="Zero-based index in parsed_output.issues.", ge=0)
    raw_method_path: str = Field(description="Repository-relative frozen method record path.", min_length=1)
    raw_json_pointer: str = Field(description="Pointer to exact frozen finding object.", min_length=1)
    raw_sha256: str = Field(description="SHA-256 of exact raw method record.", pattern=r"^sha256:[0-9a-f]{64}$")
    claim_pointer: str = Field(description="Pointer to raw issue text.", min_length=1)
    where_pointer: str = Field(description="Pointer to raw where text.", min_length=1)
    raw_text: RawFindingText = Field(description="Original finding text preserved for audit.")
    observed_source_fact_status: FactStatus = Field(description="Pane5 fact finding against NL and author PlantUML.")
    normative_violation_status: NormativeStatus = Field(description="Whether a source-backed obligation is violated.")
    defect_claim_status: DefectClaimStatus = Field(description="Whether this is an author-source defect claim.")
    d_tier: DATier = Field(description="Final D2/D1/D0/A0 tier.")
    a0_type: A0Type | None = Field(description="Baseline A0 subtype; NOT_A_DEFECT_CLAIM is normally disallowed.")
    validity: Validity = Field(description="Deterministically closed report validity.")
    corrected_kni: Literal["K", "N", "I"] = Field(description="Deterministically derived K/N/I label.")
    relations: tuple[RelationDecision, ...] = Field(description="Dense 145 expected relation rows.", min_length=1)
    full_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with FULL relation only.")
    partial_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with PARTIAL relation only.")
    no_match_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with NO_MATCH relation.")
    witness: Witness = Field(description="Independent baseline W evidence axis.")
    source_loci: tuple[str, ...] = Field(description="Concrete author-source states/transitions/guards/actions/paths.")
    reason: str = Field(description="Dedicated pane5 reason covering fact, obligation, D/A, and validity.", min_length=1)
    basis: str = Field(description="Dedicated pane5 evidence basis with source anchors.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Source refs actually read by pane5.", min_length=1)
    original_category: Literal["N", "I"] = Field(description="Frozen pre-v3 non-K category used for migration accounting.")
    reclassification_from: Literal["N", "I"] = Field(description="Category before this v3 re-review.")
    reclassification_to: Literal["K", "N", "I"] = Field(description="Category after this v3 re-review.")
    reclassified_from_non_k: Literal[True] = Field(description="True for every row in this v3 non-K review layer.")
    reclassification_reason: str = Field(description="Dedicated explanation of category movement or retention.", min_length=1)
    canonical_group_key: str | None = Field(description="Pane5 group key for final N or I cluster, null for K.")
    review: ReviewChain = Field(description="Independent raw-first reviews and pane5 final adjudication.")
    scoring: Literal[True] = Field(description="All 233 rows remain in the final report denominator.")
    diagnostic_only: Literal[False] = Field(description="Non-K re-reviewed rows are not silently dropped.")

    @model_validator(mode="after")
    def validate_closure(self) -> "BaselineReportDecisionV3":
        if self.schema != SCHEMA or self.protocol_version != PROTOCOL:
            raise ValueError("unexpected v3 schema or protocol")
        if self.d_tier == DATier.A0:
            if self.observed_source_fact_status != FactStatus.REFUTED or self.a0_type is None:
                raise ValueError("A0 requires refuted fact and an A0 subtype")
            if self.a0_type == A0Type.NOT_A_DEFECT_CLAIM:
                raise ValueError("baseline v3 does not permit NOT_A_DEFECT_CLAIM")
        elif self.a0_type is not None or self.observed_source_fact_status != FactStatus.ESTABLISHED:
            raise ValueError("D2/D1/D0 require established fact and no A0 subtype")
        if self.d_tier in {DATier.D2, DATier.D1}:
            if self.normative_violation_status != NormativeStatus.ESTABLISHED or self.defect_claim_status != DefectClaimStatus.DEFECT_CLAIM:
                raise ValueError("D2/D1 require an established normative defect claim")
        else:
            if self.normative_violation_status != NormativeStatus.NOT_ESTABLISHED or self.defect_claim_status != DefectClaimStatus.NO_DEFECT_CLAIM:
                raise ValueError("D0/A0 require no established normative defect claim")
        if len(self.relations) != 145 or len({row.expected_id for row in self.relations}) != 145:
            raise ValueError("v3 decision must contain 145 unique expected relations")
        relation_values = [row.relation for row in self.relations]
        positive = any(value in {Relation.FULL_MATCH, Relation.PARTIAL_MATCH} for value in relation_values)
        expected_validity = Validity.INVALID if self.d_tier in {DATier.D0, DATier.A0} else (Validity.VALID_KNOWN if positive else Validity.VALID_NOVEL)
        expected_kni = "I" if expected_validity == Validity.INVALID else ("K" if positive else "N")
        if self.validity != expected_validity or self.corrected_kni != expected_kni or self.reclassification_to != expected_kni:
            raise ValueError("D/A, relation, validity, and K/N/I do not close")
        if self.d_tier in {DATier.D0, DATier.A0} and positive:
            raise ValueError("D0/A0 must have only NO_MATCH relations")
        if set(self.full_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.FULL_MATCH}:
            raise ValueError("full_ledger_ids do not match relation rows")
        if set(self.partial_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.PARTIAL_MATCH}:
            raise ValueError("partial_ledger_ids do not match relation rows")
        if set(self.no_match_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.NO_MATCH}:
            raise ValueError("no_match_ledger_ids do not match relation rows")
        if self.corrected_kni == "K" and self.canonical_group_key is not None:
            raise ValueError("K report cannot carry an N/I grouping key")
        if self.corrected_kni in {"N", "I"} and not self.canonical_group_key:
            raise ValueError("final N/I report requires a human group key")
        for field_name in ("reason", "basis", "reclassification_reason"):
            if self.original_report_id not in getattr(self, field_name):
                raise ValueError(f"{field_name} must be report-specific")
        return self


class RelationAuditRowV3(BaseModel):
    """Archive-level dense relation row mirrored from one report decision."""

    model_config = ConfigDict(extra="forbid")

    side: Literal["x1v2_baseline"] = Field(description="Baseline side owning this relation.")
    pair_id: str = Field(description="Four-digit pair ID.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Round number.", ge=1, le=3)
    report_id: str = Field(description="Report identity.", min_length=1)
    expected_id: str = Field(description="Expected ledger identity.", min_length=1)
    relation: Relation = Field(description="Expected-specific relation.")
    reason: str = Field(description="Expected-specific relation reason.", min_length=1)
    basis: str = Field(description="Expected-specific relation basis.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Relation evidence refs.", min_length=1)
    report_owned_field_refs: tuple[str, ...] = Field(description="Raw report field refs.", min_length=1)


class Pane5RegisterRowV3(BaseModel):
    """One explicit pane5 source-backed adjudication input for a non-K report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(description="Stable report identity being adjudicated.", min_length=1)
    pair_id: str = Field(description="Four-digit baseline pair ID.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen baseline round.", ge=1, le=3)
    finding_index: int = Field(description="Zero-based raw finding index.", ge=0)
    observed_source_fact_status: FactStatus = Field(description="Pane5 finding about whether the burden-bearing author fact exists.")
    normative_violation_status: NormativeStatus = Field(description="Pane5 finding about whether a source-backed obligation is violated.")
    defect_claim_status: DefectClaimStatus = Field(description="Pane5 finding about whether the report claims an author-source defect.")
    d_tier: DATier = Field(description="Pane5 final D2/D1/D0/A0 adjudication.")
    a0_type: A0Type | None = Field(description="Baseline A0 subtype; only FALSE_POSITIVE is allowed.")
    validity: Validity = Field(description="Stored closure check value; recomputed from D/A and relations.")
    corrected_kni: Literal["K", "N", "I"] = Field(description="Stored closure check value; recomputed from D/A and relations.")
    relations: tuple[RelationDecision, ...] = Field(description="All 145 expected-specific relation rows.", min_length=145, max_length=145)
    full_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with FULL_MATCH, mirrored from relations.")
    partial_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with PARTIAL_MATCH, mirrored from relations.")
    no_match_ledger_ids: tuple[str, ...] = Field(description="Expected IDs with NO_MATCH, mirrored from relations.")
    source_loci: tuple[str, ...] = Field(description="Author-source states, transitions, guards, actions, or paths reviewed.", min_length=1)
    reason: str = Field(description="Pane5 report-specific reason grounded in the source reread.", min_length=1)
    basis: str = Field(description="Pane5 report-specific basis naming the source evidence and digest.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Raw, NL, PlantUML, and ledger evidence refs.", min_length=4)
    evidence_digest: str = Field(description="Digest of the raw/source/all-ledger evidence read for this report.", pattern=r"^sha256:[0-9a-f]{64}$")
    original_category: Literal["N", "I"] = Field(description="Frozen pre-v3 category used only for migration accounting.")
    canonical_group_key: str | None = Field(description="Final N or I diagnostic group key; null for new K.")
    review: ReviewChain = Field(description="Two independent proposals and pane5 final confirmation.")

    @model_validator(mode="after")
    def validate_register_row(self) -> "Pane5RegisterRowV3":
        ids = [row.expected_id for row in self.relations]
        if len(ids) != 145 or len(set(ids)) != 145:
            raise ValueError("pane5 register row must contain 145 unique expected IDs")
        positive = {row.expected_id for row in self.relations if row.relation in {Relation.FULL_MATCH, Relation.PARTIAL_MATCH}}
        expected_validity = Validity.INVALID if self.d_tier in {DATier.D0, DATier.A0} else (Validity.VALID_KNOWN if positive else Validity.VALID_NOVEL)
        expected_kni = "I" if expected_validity == Validity.INVALID else ("K" if positive else "N")
        if self.validity != expected_validity or self.corrected_kni != expected_kni:
            raise ValueError("pane5 register D/A and relation closure mismatch")
        if self.d_tier == DATier.A0 and (self.observed_source_fact_status != FactStatus.REFUTED or self.a0_type != A0Type.FALSE_POSITIVE):
            raise ValueError("baseline A0 register rows require FALSE_POSITIVE")
        if self.d_tier != DATier.A0 and (self.observed_source_fact_status != FactStatus.ESTABLISHED or self.a0_type is not None):
            raise ValueError("non-A0 register rows require established fact and no A0 subtype")
        if self.d_tier in {DATier.D0, DATier.A0} and positive:
            raise ValueError("invalid pane5 register row cannot carry a positive relation")
        if set(self.full_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.FULL_MATCH}:
            raise ValueError("pane5 register FULL IDs do not mirror relations")
        if set(self.partial_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.PARTIAL_MATCH}:
            raise ValueError("pane5 register PARTIAL IDs do not mirror relations")
        if set(self.no_match_ledger_ids) != {row.expected_id for row in self.relations if row.relation == Relation.NO_MATCH}:
            raise ValueError("pane5 register NO IDs do not mirror relations")
        return self


class Pane5RegisterV3(BaseModel):
    """Versioned pane5 register and source-read evidence contract."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal["paper1.manual-adjudication.v3-baseline-ni.pane5-register"] = Field(description="Versioned pane5 register schema.")
    protocol_version: str = Field(description="Frozen semantic protocol identifier.", min_length=1)
    side: Literal["x1v2_baseline"] = Field(description="Only X1v2 baseline rows are in this register.")
    scope: str = Field(description="The register covers all 233 frozen non-K reports and does not alter frozen K rows.", min_length=1)
    source_evidence_path: str = Field(description="Archive-relative evidence-read artifact path.", min_length=1)
    source_evidence_sha256: str = Field(description="Hash of the evidence-read artifact used by this register.", pattern=r"^sha256:[0-9a-f]{64}$")
    rows: tuple[Pane5RegisterRowV3, ...] = Field(description="One explicit final pane5 input per non-K report.", min_length=233, max_length=233)
    human_adjudicator_id: Literal["human:pane5-supervised-adjudicator"] = Field(description="Authorized pane5 final adjudicator.")
    human_confirmation: Literal[True] = Field(description="Explicit user-authorized pane5 confirmation for this input register.")
    confirmation_time_utc: str = Field(description="UTC time at which pane5 confirmed the register.", min_length=1)
    session_reference: str = Field(description="Auditable pane5 session/attestation reference.", min_length=1)

    @model_validator(mode="after")
    def validate_register(self) -> "Pane5RegisterV3":
        ids = [row.report_id for row in self.rows]
        if len(set(ids)) != len(ids):
            raise ValueError("pane5 register contains duplicate report IDs")
        if any(row.review.final_adjudicator_id != self.human_adjudicator_id or not row.review.human_confirmation for row in self.rows):
            raise ValueError("every pane5 row must carry the authorized human confirmation")
        return self


class LegacyProposalPositiveRelation(BaseModel):
    """A positive relation proposed by one blind raw-first reviewer."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="Ledger expected ID proposed as a positive relation.", min_length=1)
    relation: Relation = Field(description="Proposed FULL_MATCH or PARTIAL_MATCH relation.")
    reason: str = Field(description="Report-specific semantic reason for the proposed positive relation.", min_length=1)
    basis: str = Field(description="Source and ledger basis for the proposed positive relation.", min_length=1)


class LegacyRawFirstProposalReport(BaseModel):
    """Compatibility model for the original compact Track-A proposal format."""

    model_config = ConfigDict(extra="forbid")

    side: Literal["x1v2_baseline"] = Field(description="Baseline side reviewed by this proposal.")
    pair_id: str = Field(description="Four-digit pair ID in the requested raw range.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen baseline round number.", ge=1, le=3)
    original_report_id: str = Field(description="Stable report identity from raw inventory provenance.", min_length=1)
    finding_index: int = Field(description="Zero-based index in parsed_output.issues.", ge=0)
    raw_method_path: str = Field(description="Archive-relative frozen method record path.", min_length=1)
    raw_json_pointer: str = Field(description="Pointer to the exact raw finding object.", min_length=1)
    raw_sha256: str = Field(description="SHA-256 of the exact raw record.", pattern=r"^sha256:[0-9a-f]{64}$")
    raw_text: RawFindingText = Field(description="Exact issue, where, reason and basis text from raw.")
    source_paths: tuple[str, ...] = Field(description="Archive-relative NL and PlantUML source paths read for this pair.", min_length=2)
    source_hashes: tuple[SourceRef, ...] = Field(description="Hashes and pointers for the author source files read.", min_length=2)
    observed_fact_status: FactStatus = Field(description="Raw-first finding about whether the claimed author-source fact is established.")
    observed_fact_reason: str = Field(description="Report-specific explanation of the fact finding against author source.", min_length=1)
    d_tier: DATier = Field(description="Independent D2/D1/D0/A0 proposal; not a final adjudication.")
    a0_type: A0Type | None = Field(description="A0 subtype; baseline proposals may use only FALSE_POSITIVE.")
    normative_violation_status: NormativeStatus = Field(description="Whether the source-backed obligation is proposed as violated.")
    proposed_validity: Validity = Field(description="Validity mechanically derived from this proposal's D/A and relation vector.")
    proposed_kni: Literal["K", "N", "I"] = Field(description="K/N/I mechanically derived from this proposal.")
    source_loci: tuple[str, ...] = Field(description="Concrete states, transitions, guards, actions, paths or source fragments named by the finding.", min_length=1)
    relation_vector: str = Field(description="Canonical 145-position vector in top-level ledger ID order: F=FULL, P=PARTIAL, N=NO_MATCH.", min_length=145, max_length=145, pattern=r"^[FPN]{145}$")
    relation_digest: str = Field(description="SHA-256 of the canonical relation vector and ledger order.", pattern=r"^sha256:[0-9a-f]{64}$")
    positive_relations: tuple[LegacyProposalPositiveRelation, ...] = Field(description="Positive same-pair relation proposals represented in the vector.")
    reason: str = Field(description="Dedicated raw-first proposal reason for this report.", min_length=1)
    basis: str = Field(description="Dedicated raw-first proposal basis naming exact source evidence.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Raw record, author source and ledger refs read by the reviewer.", min_length=3)
    evidence_gaps: tuple[str, ...] = Field(description="Evidence gaps remaining in this proposal; empty means no recorded gap.")
    reviewer_id: str = Field(description="Blind Track A proposal reviewer identity.", min_length=1)
    review_status: Literal["PROPOSAL"] = Field(description="This artifact is only an independent proposal, never a final label.")
    reference_visible: Literal[False] = Field(description="Frozen v2/reference labels were not visible before this proposal.")
    other_reviewers_visible: Literal[False] = Field(description="Track B and other reviewer conclusions were not visible before this proposal.")


class RawFirstProposalSet(BaseModel):
    """Versioned raw-first Track A proposal set for one pair-range batch."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(description="Versioned raw-first proposal schema identifier.", min_length=1)
    protocol_version: str = Field(description="Protocol identifier used for D/A and relation proposals.", min_length=1)
    side: Literal["x1v2_baseline"] = Field(description="Only baseline reports are in this proposal set.")
    reviewer_id: str = Field(description="Blind Track A reviewer identity.", min_length=1)
    requested_pair_range: tuple[str, str] = Field(description="Inclusive requested pair range as zero-padded IDs.", min_length=2, max_length=2)
    selection_scope: str = Field(description="Explicit statement of the current non-K selection evidence boundary.", min_length=1)
    selection_evidence_gap: str = Field(description="Why this proposal does not claim to have read the prohibited old selector.", min_length=1)
    input_ledger_path: str = Field(description="Archive-relative frozen ledger path.", min_length=1)
    input_ledger_sha256: str = Field(description="SHA-256 of the frozen ledger bytes.", pattern=r"^sha256:[0-9a-f]{64}$")
    ledger_ids: tuple[str, ...] = Field(description="All 145 ledger IDs defining relation-vector order.", min_length=145, max_length=145)
    reports: tuple[LegacyRawFirstProposalReport, ...] = Field(description="Every raw report enumerated in the requested pair range.", min_length=1)
    coverage_statement: str = Field(description="Provider-free report and source coverage statement.", min_length=1)
    missing_evidence: tuple[str, ...] = Field(description="Structured batch-level missing evidence statements.")
    generated_by: str = Field(description="Deterministic generator version and source code path.", min_length=1)

    @model_validator(mode="after")
    def validate_proposal_set(self) -> "RawFirstProposalSet":
        start, end = self.requested_pair_range
        if not (start.isdigit() and end.isdigit() and int(start) <= int(end)):
            raise ValueError("requested pair range must contain ordered numeric IDs")
        if len(set(self.ledger_ids)) != 145:
            raise ValueError("ledger IDs must be unique and contain all 145 items")
        identities = {(r.pair_id, r.round, r.original_report_id) for r in self.reports}
        if len(identities) != len(self.reports):
            raise ValueError("duplicate raw-first report identity")
        for report in self.reports:
            if not (int(start) <= int(report.pair_id) <= int(end)):
                raise ValueError("proposal report is outside requested pair range")
            if report.reviewer_id != self.reviewer_id:
                raise ValueError("report reviewer does not match proposal reviewer")
            if report.d_tier == DATier.A0 and report.a0_type != A0Type.FALSE_POSITIVE:
                raise ValueError("baseline raw-first A0 proposals may only use FALSE_POSITIVE")
            if report.d_tier != DATier.A0 and report.a0_type is not None:
                raise ValueError("non-A0 proposal cannot carry an A0 subtype")
            positive = any(code in "FP" for code in report.relation_vector)
            expected_validity = Validity.INVALID if report.d_tier in {DATier.D0, DATier.A0} else (Validity.VALID_KNOWN if positive else Validity.VALID_NOVEL)
            expected_kni = "I" if expected_validity == Validity.INVALID else ("K" if positive else "N")
            if report.proposed_validity != expected_validity or report.proposed_kni != expected_kni:
                raise ValueError(f"proposal closure failed for {report.original_report_id}")
            if report.d_tier in {DATier.D0, DATier.A0} and positive:
                raise ValueError(f"invalid proposal has positive relation: {report.original_report_id}")
        return self


class NGroupV3(BaseModel):
    """Human-assigned substantive N group constrained to one baseline pair."""

    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(description="Stable v3 N group identifier.", min_length=1)
    group_kind: Literal[GroupKind.SUBSTANTIVE_N] = Field(description="This group represents a substantive VALID_NOVEL issue.")
    side: Literal["x1v2_baseline"] = Field(description="Baseline side; groups cannot cross sides.")
    pair_id: str = Field(description="Single pair boundary; groups cannot cross pairs.", pattern=r"^[0-9]{4}$")
    canonical_group_key: str = Field(description="Human-assigned semantic identity, not text similarity.", min_length=1)
    member_report_ids: tuple[str, ...] = Field(description="Each final N member exactly once.", min_length=1)
    cross_round_merge: bool = Field(description="Whether members span multiple rounds.")
    normative_obligation: str = Field(description="Common normative obligation/property.", min_length=1)
    author_source_locus: str = Field(description="Common source locus or inseparable source cause.", min_length=1)
    substantive_root_cause: str = Field(description="Common substantive root cause.", min_length=1)
    repair_intent: str = Field(description="Common minimal repair intention.", min_length=1)
    d_tiers: tuple[DATier, ...] = Field(description="D2/D1 tiers represented by members.", min_length=1)
    reason: str = Field(description="Dedicated merge reason.", min_length=1)
    basis: str = Field(description="Evidence for homogeneity and non-merges.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Resolvable source refs for the group.", min_length=1)
    member_source_refs: dict[str, tuple[SourceRef, ...]] = Field(description="Complete source refs partitioned by every member report ID.")
    non_merge_reasons: tuple[NonMergeReasonV3, ...] = Field(description="Pair-local conservative non-merge records for singleton or otherwise unmerged neighbors; empty for a fully documented merge.")

    @model_validator(mode="after")
    def validate_group_shape(self) -> "NGroupV3":
        """Enforce local membership, pair, round, and source-ref closure."""
        if len(set(self.member_report_ids)) != len(self.member_report_ids):
            raise ValueError(f"duplicate N group member: {self.group_id}")
        if set(self.member_source_refs) != set(self.member_report_ids):
            raise ValueError(f"member source-ref keys do not close for {self.group_id}")
        member_refs = {
            (ref.repository_path, ref.json_pointer, ref.line, ref.sha256)
            for refs in self.member_source_refs.values()
            for ref in refs
        }
        group_refs = {(ref.repository_path, ref.json_pointer, ref.line, ref.sha256) for ref in self.source_refs}
        if member_refs != group_refs:
            raise ValueError(f"group source refs are not the union of member refs: {self.group_id}")
        rounds: set[int] = set()
        for report_id in self.member_report_ids:
            if not report_id.startswith(self.pair_id + ":"):
                raise ValueError(f"N group member crosses pair boundary: {self.group_id}/{report_id}")
            parts = report_id.split(":")
            if len(parts) < 2 or not parts[1].startswith("r") or not parts[1][1:].isdigit():
                raise ValueError(f"N group member has no parseable round: {self.group_id}/{report_id}")
            rounds.add(int(parts[1][1:]))
        if self.cross_round_merge != (len(rounds) > 1):
            raise ValueError(f"cross-round flag mismatch: {self.group_id}")
        if len(self.member_report_ids) == 1 and self.non_merge_reasons:
            expected = {item.neighbor_report_id for item in self.non_merge_reasons}
            if self.member_report_ids[0] in expected:
                raise ValueError(f"singleton non-merge points to itself: {self.group_id}")
        return self


class InvalidClusterV3(BaseModel):
    """Diagnostic invalid-claim cluster, kept separate from substantive N groups."""

    model_config = ConfigDict(extra="forbid")

    group_id: str = Field(description="Stable invalid diagnostic cluster ID.", min_length=1)
    group_kind: Literal[GroupKind.INVALID_DIAGNOSTIC_CLUSTER] = Field(description="This is not a real defect group.")
    side: Literal["x1v2_baseline"] = Field(description="Baseline side.")
    pair_id: str = Field(description="Single pair boundary.", pattern=r"^[0-9]{4}$")
    canonical_group_key: str = Field(description="Human invalid-claim cluster key.", min_length=1)
    member_report_ids: tuple[str, ...] = Field(description="Invalid reports in this diagnostic cluster.", min_length=1)
    reason: str = Field(description="Why these invalid claims share a diagnostic cause.", min_length=1)
    basis: str = Field(description="Evidence for diagnostic clustering.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Resolvable source refs.", min_length=1)
    member_source_refs: dict[str, tuple[SourceRef, ...]] = Field(description="Complete source refs partitioned by every invalid member report ID.")

    @model_validator(mode="after")
    def validate_cluster_shape(self) -> "InvalidClusterV3":
        """Enforce local invalid-cluster membership and provenance closure."""
        if len(set(self.member_report_ids)) != len(self.member_report_ids):
            raise ValueError(f"duplicate invalid-cluster member: {self.group_id}")
        if set(self.member_source_refs) != set(self.member_report_ids):
            raise ValueError(f"invalid-cluster source-ref keys do not close: {self.group_id}")
        member_refs = {
            (ref.repository_path, ref.json_pointer, ref.line, ref.sha256)
            for refs in self.member_source_refs.values()
            for ref in refs
        }
        group_refs = {(ref.repository_path, ref.json_pointer, ref.line, ref.sha256) for ref in self.source_refs}
        if member_refs != group_refs:
            raise ValueError(f"invalid-cluster source refs are not the union: {self.group_id}")
        for report_id in self.member_report_ids:
            if not report_id.startswith(self.pair_id + ":"):
                raise ValueError(f"invalid cluster member crosses pair boundary: {self.group_id}/{report_id}")
        return self


class DecisionSetV3(BaseModel):
    """Canonical envelope for all 233 baseline non-K re-review decisions."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned v3 decision-set schema.")
    protocol_version: str = Field(default=PROTOCOL, description="Frozen protocol version.")
    side: Literal["x1v2_baseline"] = Field(description="Only baseline decisions are stored here.")
    raw_non_k_count: int = Field(description="Count of frozen pre-v3 N/I reports included in this layer.", ge=0)
    decisions: tuple[BaselineReportDecisionV3, ...] = Field(description="One final decision per original non-K report.", min_length=1)
    input_inventory_sha256: str = Field(description="Hash of the v3 inventory input.", pattern=r"^sha256:[0-9a-f]{64}$")
    frozen_k_snapshot_sha256: str = Field(description="Hash of the frozen K comparison snapshot.", pattern=r"^sha256:[0-9a-f]{64}$")
    reviewer_coverage: str = Field(description="Human-readable coverage statement backed by review records.", min_length=1)
    generated_by: str = Field(description="Deterministic generator version.", min_length=1)

    @model_validator(mode="after")
    def validate_envelope(self) -> "DecisionSetV3":
        if self.schema != SCHEMA or self.protocol_version != PROTOCOL:
            raise ValueError("unexpected v3 decision-set schema")
        if self.raw_non_k_count != len(self.decisions):
            raise ValueError("raw non-K count does not equal decisions")
        if len({decision.original_report_id for decision in self.decisions}) != len(self.decisions):
            raise ValueError("duplicate non-K report decision")
        return self


class GroupSetV3(BaseModel):
    """Canonical envelope for substantive N groups and separate I clusters."""

    model_config = ConfigDict(extra="forbid")

    schema: str = Field(default=SCHEMA, description="Versioned v3 group-set schema.")
    n_groups: tuple[NGroupV3, ...] = Field(description="Conservative substantive N groups.")
    invalid_clusters: tuple[InvalidClusterV3, ...] = Field(description="Diagnostic I clusters, never reported as true defects.")
    report_to_group: dict[str, str] = Field(description="Map in which every final N/I report ID occurs exactly once and points to its declared group or diagnostic cluster.")
    grouping_basis: str = Field(description="Operational same-pair same-obligation grouping statement.", min_length=1)

    @model_validator(mode="after")
    def validate_membership_closure(self) -> "GroupSetV3":
        """Enforce global group IDs, one-membership closure, and map consistency."""
        groups = tuple(self.n_groups) + tuple(self.invalid_clusters)
        group_ids = [group.group_id for group in groups]
        if len(set(group_ids)) != len(group_ids):
            raise ValueError("duplicate group or cluster ID")
        membership: dict[str, str] = {}
        for group in groups:
            for report_id in group.member_report_ids:
                if report_id in membership:
                    raise ValueError(f"report appears in multiple groups: {report_id}")
                membership[report_id] = group.group_id
        if membership != self.report_to_group:
            raise ValueError("report_to_group does not exactly match declared membership")
        return self


class Metric(BaseModel):
    """A metric with explicit numerator, denominator, and percentage."""

    model_config = ConfigDict(extra="forbid")

    numerator: int = Field(description="Metric numerator in the declared unit.", ge=0)
    denominator: int = Field(description="Metric denominator in the declared unit.", ge=0)
    percentage: float | None = Field(description="Numerator divided by denominator, or null for not applicable.", ge=0.0, le=1.0)
    unit: str = Field(description="Metric unit and deduplication universe.", min_length=1)
    reason: str = Field(description="Why this denominator applies.", min_length=1)

    @model_validator(mode="after")
    def validate_percentage(self) -> "Metric":
        if self.denominator == 0 and self.percentage is not None:
            raise ValueError("zero-denominator metric must have null percentage")
        if self.denominator and self.percentage != self.numerator / self.denominator:
            raise ValueError("metric percentage is not deterministic")
        if self.numerator > self.denominator:
            raise ValueError("metric numerator exceeds denominator")
        return self


class ProposalPositiveRelation(BaseModel):
    """One manually proposed positive relation retained in a dense digest."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="One ledger expected ID represented in the 145-row dense relation.", min_length=1)
    relation: Relation = Field(description="Manual raw-first FULL_MATCH or PARTIAL_MATCH proposal.")
    reason: str = Field(description="Report- and expected-specific reason for the proposed positive relation.", min_length=1)
    basis: str = Field(description="Archive-relative raw/source/ledger basis for the proposed positive relation.", min_length=1)

    @model_validator(mode="after")
    def positive_only(self) -> "ProposalPositiveRelation":
        if self.relation == Relation.NO_MATCH:
            raise ValueError("positive relation rows cannot be NO_MATCH")
        return self


class ProposalRelationDigest(BaseModel):
    """Deterministic reconstruction contract for all 145 expected relations."""

    model_config = ConfigDict(extra="forbid")

    kind: Literal["canonical_dense_relation_digest"] = Field(description="Stable digest representation of all expected-specific rows.")
    row_count: int = Field(description="Number of dense rows represented by this digest; the unit is report by expected item.", ge=0)
    ordered_expected_ids: tuple[str, ...] = Field(description="All ledger expected IDs in canonical ledger order.", min_length=1)
    default_relation: Literal["NO_MATCH"] = Field(description="Relation assigned to an expected ID omitted from positive_rows.")
    positive_rows: tuple[ProposalPositiveRelation, ...] = Field(description="Explicit manually proposed FULL/PARTIAL rows; omitted IDs reconstruct as NO_MATCH.")
    rows_sha256: str = Field(description="SHA-256 of the complete reconstructed dense rows.", pattern=r"^sha256:[0-9a-f]{64}$")
    reconstruction: str = Field(description="Provider-free reconstruction rule for the complete dense relation.", min_length=1)

    @model_validator(mode="after")
    def validate_dense_contract(self) -> "ProposalRelationDigest":
        if self.row_count != len(self.ordered_expected_ids):
            raise ValueError("dense row count does not equal ordered expected ID count")
        if len(set(self.ordered_expected_ids)) != len(self.ordered_expected_ids):
            raise ValueError("dense expected ID order contains duplicates")
        positive_ids = [row.expected_id for row in self.positive_rows]
        if len(set(positive_ids)) != len(positive_ids):
            raise ValueError("dense positive rows contain duplicate expected IDs")
        if not set(positive_ids).issubset(set(self.ordered_expected_ids)):
            raise ValueError("dense positive row references an unknown expected ID")
        return self


class ProposalArtifactDigest(BaseModel):
    """Hash closure for the raw record, author sources, and frozen ledger."""

    model_config = ConfigDict(extra="forbid")

    raw_sha256: str = Field(description="SHA-256 of the exact raw method record.", pattern=r"^sha256:[0-9a-f]{64}$")
    nl_sha256: str = Field(description="SHA-256 of the archived author NL source.", pattern=r"^sha256:[0-9a-f]{64}$")
    plantuml_sha256: str = Field(description="SHA-256 of the archived author PlantUML source.", pattern=r"^sha256:[0-9a-f]{64}$")
    ledger_sha256: str = Field(description="SHA-256 of the frozen 145-item ledger.", pattern=r"^sha256:[0-9a-f]{64}$")


class RawFirstProposalReport(BaseModel):
    """One dedicated blind raw-first proposal for one pair-range report."""

    model_config = ConfigDict(extra="forbid")

    pair_id: str = Field(description="Four-digit pair ID from the raw record.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen baseline round number.", ge=1, le=3)
    original_report_id: str = Field(description="Stable raw report identity.", min_length=1)
    finding_index: int = Field(description="Zero-based index in parsed_output.issues.", ge=0)
    raw_method_path: str = Field(description="Archive-relative exact raw record path.", min_length=1)
    raw_json_pointer: str = Field(description="JSON pointer to the exact raw finding object.", min_length=1)
    raw_sha256: str = Field(description="SHA-256 of the exact raw record.", pattern=r"^sha256:[0-9a-f]{64}$")
    raw_text: RawFindingText = Field(description="Verbatim issue, where, reason, and basis from the raw record.")
    observed_source_fact_status: FactStatus = Field(description="Raw-first finding about whether the author-source fact is established or refuted.")
    observed_fact: str = Field(description="Dedicated prose statement of the observed source fact and its evidence status.", min_length=1)
    normative_violation_status: NormativeStatus = Field(description="Raw-first proposal about whether a source-backed obligation is violated.")
    d_tier: DATier = Field(description="Proposed D2/D1/D0/A0 tier; this is not a final pane5 label.")
    a0_type: A0Type | None = Field(description="A0 subtype; baseline proposal permits only FALSE_POSITIVE.")
    alternative_reading: str | None = Field(description="Concrete competent alternative reading for D1/D0, or null for A0.")
    source_loci: tuple[str, ...] = Field(description="Exact report-named source loci read during the proposal.", min_length=1)
    source_refs: tuple[SourceRef, ...] = Field(description="Raw record, NL, and PlantUML evidence refs read by this proposal.", min_length=3)
    relation_digest: ProposalRelationDigest = Field(description="Complete 145-expected relation digest.")
    positive_expected_ids: tuple[str, ...] = Field(description="Expected IDs explicitly proposed as FULL/PARTIAL in the digest.")
    reason: str = Field(description="Dedicated report-specific D/A proposal reason.", min_length=1)
    basis: str = Field(description="Dedicated report-specific source/hash basis.", min_length=1)
    reviewer_id: str = Field(description="Independent proposal reviewer identity.", min_length=1)
    review_status: Literal["PROPOSAL"] = Field(description="This record is proposal-only and cannot be treated as final.")
    reference_visible: Literal[False] = Field(description="Frozen adjudication labels were not visible before submission.")
    primary_visible: Literal[False] = Field(description="Another primary decision was not visible before submission.")
    submitted_at_utc: str = Field(description="UTC proposal generation timestamp.", min_length=1)
    human_confirmation: Literal[False] = Field(description="False because this is not a pane5 final confirmation.")
    provider_calls: Literal[0] = Field(description="Provider calls attributable to this proposal; must remain zero.")
    source_artifact_digest: ProposalArtifactDigest = Field(description="Hash closure for all permitted evidence artifacts.")

    @model_validator(mode="after")
    def validate_proposal_closure(self) -> "RawFirstProposalReport":
        if self.d_tier == DATier.A0:
            if self.observed_source_fact_status != FactStatus.REFUTED or self.a0_type != A0Type.FALSE_POSITIVE:
                raise ValueError("baseline A0 proposal requires a refuted fact and FALSE_POSITIVE")
        else:
            if self.observed_source_fact_status != FactStatus.ESTABLISHED or self.a0_type is not None:
                raise ValueError("non-A0 proposal requires established fact and no A0 subtype")
        if self.d_tier in {DATier.D2, DATier.D1} and self.normative_violation_status != NormativeStatus.ESTABLISHED:
            raise ValueError("D2/D1 proposal requires an established normative violation")
        if self.d_tier == DATier.D0 and self.normative_violation_status != NormativeStatus.NOT_ESTABLISHED:
            raise ValueError("D0 proposal requires no established normative violation")
        digest_ids = {row.expected_id for row in self.relation_digest.positive_rows}
        if digest_ids != set(self.positive_expected_ids):
            raise ValueError("positive_expected_ids does not match the dense relation digest")
        if self.relation_digest.row_count != 145:
            raise ValueError("baseline proposal must carry all 145 ledger rows")
        if self.d_tier in {DATier.D0, DATier.A0} and digest_ids:
            raise ValueError("D0/A0 proposal cannot carry a positive expected relation")
        return self


class RawFirstProposalCoverage(BaseModel):
    """Coverage and explicit evidence gaps for a blind proposal batch."""

    model_config = ConfigDict(extra="forbid")

    raw_candidate_reports: int = Field(description="Number of raw reports enumerated in the requested pair range.", ge=0)
    dedicated_proposals: int = Field(description="Number of dedicated proposal records written.", ge=0)
    missing_pair_ids_without_raw_reports: tuple[str, ...] = Field(description="Requested pair IDs with no frozen raw record.")
    source_closure_missing_for_reports: tuple[str, ...] = Field(description="Pairs whose reports lacked permitted author-source closure.")
    pairs_with_zero_reports: tuple[str, ...] = Field(description="Requested pair IDs with zero raw reports.")
    non_k_target_reports: int | None = Field(description="Known non-K target count; null when blind membership evidence is absent.", ge=0)
    non_k_membership_evidence_gap: str = Field(description="Reason the blind proposal cannot assert membership in the frozen non-K target set.", min_length=1)
    all_145_relation_digests: bool = Field(description="Whether every proposal has a 145-row dense digest contract.")
    missing_evidence: tuple[str, ...] = Field(description="Evidence intentionally absent or unavailable in this proposal pass.")


class RawFirstProposalLedger(BaseModel):
    """Ledger identity and canonical ordering used by a proposal batch."""

    model_config = ConfigDict(extra="forbid")

    repository_path: str = Field(description="Archive-relative reference ledger path.", min_length=1)
    sha256: str = Field(description="SHA-256 of reference/ledger.json.", pattern=r"^sha256:[0-9a-f]{64}$")
    expected_count: Literal[145] = Field(description="Frozen expected issue count.")
    ordered_expected_ids_sha256: str = Field(description="Hash of the ordered ledger expected ID list.", pattern=r"^sha256:[0-9a-f]{64}$")


class RawFirstProposalEnvelope(BaseModel):
    """Canonical provider-free envelope for one independent Track-A batch."""

    model_config = ConfigDict(extra="forbid")

    schema: Literal["paper1.manual-adjudication-raw-first-proposal.v3-baseline-ni"] = Field(description="Versioned raw-first proposal schema.")
    protocol_version: str = Field(description="Frozen D/A and relation protocol identifier.", min_length=1)
    proposal_status: Literal["PROPOSAL_ONLY"] = Field(description="Envelope cannot be used as final adjudication data.")
    reviewer_id: str = Field(description="Independent Track-A proposal reviewer identity.", min_length=1)
    scope: dict[str, object] = Field(description="Requested side/range and blind membership status; not a semantic label map.")
    input_allowlist: tuple[str, ...] = Field(description="Permitted input artifact patterns.", min_length=1)
    forbidden_inputs_read: tuple[str, ...] = Field(description="Forbidden review artifacts read by this proposal; must be empty.")
    coverage: RawFirstProposalCoverage = Field(description="Machine-checkable coverage and evidence-gap statement.")
    ledger: RawFirstProposalLedger = Field(description="Frozen ledger hash and order closure.")
    reports: tuple[RawFirstProposalReport, ...] = Field(description="Dedicated raw-first proposal for each enumerated report.", min_length=1)
    generation: dict[str, object] = Field(description="Provider-free generation metadata and call counters.")

    @model_validator(mode="after")
    def validate_envelope(self) -> "RawFirstProposalEnvelope":
        if self.reviewer_id != "subagent:track-a-raw-first-0020-0039":
            raise ValueError("unexpected Track-A reviewer identity")
        if self.forbidden_inputs_read:
            raise ValueError("forbidden input artifacts must not be read")
        if self.coverage.raw_candidate_reports != len(self.reports) or self.coverage.dedicated_proposals != len(self.reports):
            raise ValueError("proposal coverage does not equal report records")
        if self.coverage.all_145_relation_digests is not True:
            raise ValueError("proposal envelope must assert 145-row digest coverage")
        if self.ledger.expected_count != 145:
            raise ValueError("unexpected ledger count")
        return self


def derive_kni(d_tier: DATier, relations: Iterable[Relation]) -> tuple[Validity, str]:
    """Derive validity/K/N/I from D/A and relations without trusting a label."""

    positive = any(value in {Relation.FULL_MATCH, Relation.PARTIAL_MATCH} for value in relations)
    if d_tier in {DATier.D0, DATier.A0}:
        return Validity.INVALID, "I"
    return (Validity.VALID_KNOWN, "K") if positive else (Validity.VALID_NOVEL, "N")


def canonical_json_sha256(value: object) -> str:
    """Hash a JSON value with the archive's deterministic serialization."""

    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()
