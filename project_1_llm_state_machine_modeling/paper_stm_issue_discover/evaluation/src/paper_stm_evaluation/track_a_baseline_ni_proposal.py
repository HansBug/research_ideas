"""Pydantic contracts for the blind Track A baseline proposal artifact."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ProposalSourceRef(BaseModel):
    """Archive-relative source pointer retained by one independent proposal."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="Repository-relative frozen source path.", min_length=1)
    line_or_pointer: str = Field(description="Stable line or pointer description into the source.", min_length=1)
    sha256: str = Field(description="SHA-256 of the referenced source bytes.", pattern=r"^sha256:[0-9a-f]{64}$")


class ProposalBlindness(BaseModel):
    """Visibility and execution attestations for the raw-first pass."""

    model_config = ConfigDict(extra="forbid")

    v2_decisions_read: Literal[False] = Field(description="False because frozen v2 decisions are forbidden inputs.")
    old_labels_read: Literal[False] = Field(description="False because old labels are forbidden inputs.")
    track_b_read: Literal[False] = Field(description="False because Track B conclusions are forbidden inputs.")
    other_reviewer_conclusions_read: Literal[False] = Field(description="False because other reviewer conclusions are forbidden inputs.")
    judge_outputs_used_for_semantic_decision: Literal[False] = Field(description="False because Judge outputs cannot supply semantic labels.")
    provider_called: Literal[False] = Field(description="False because this proposal must be provider-free.")


class RawProposalFinding(BaseModel):
    """Exact raw finding text and pointer copied from one frozen record."""

    model_config = ConfigDict(extra="forbid")

    method_record_path: str = Field(description="Repository-relative frozen raw method record path.", min_length=1)
    json_pointer: str = Field(description="JSON pointer to the exact raw finding object.", min_length=1)
    raw_sha256: str = Field(description="SHA-256 of the complete raw method record.", pattern=r"^sha256:[0-9a-f]{64}$")
    issue: str = Field(description="Exact raw issue text, without semantic rewriting.")
    where: str = Field(description="Exact raw where text, without semantic rewriting.")
    reason: str = Field(description="Exact raw reason text, without semantic rewriting.")
    basis: str | None = Field(description="Exact raw basis text, or null when the raw finding omitted basis.")
    claim_pointer: str = Field(description="JSON pointer to the raw issue field.", min_length=1)
    where_pointer: str = Field(description="JSON pointer to the raw where field.", min_length=1)


class AuthorSourceProposal(BaseModel):
    """Hashes and source-locus statement for the complete author source read."""

    model_config = ConfigDict(extra="forbid")

    nl_path: str = Field(description="Repository-relative archived author NL path.", min_length=1)
    nl_sha256: str = Field(description="SHA-256 of the archived NL file.", pattern=r"^sha256:[0-9a-f]{64}$")
    plantuml_path: str = Field(description="Repository-relative archived author PlantUML path.", min_length=1)
    plantuml_sha256: str = Field(description="SHA-256 of the archived PlantUML file.", pattern=r"^sha256:[0-9a-f]{64}$")
    full_files_read: Literal[True] = Field(description="True when both complete author source files were read.")
    pair_source_profile: str = Field(description="Human source-obligation summary for this pair.", min_length=1)
    source_locus: str = Field(description="Exact raw where locus used to locate the source evidence.", min_length=1)


class ObservedFactProposal(BaseModel):
    """Raw-first fact finding against the author NL and PlantUML."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ESTABLISHED", "REFUTED"] = Field(description="Whether the reported author-source fact is established.")
    statement: str = Field(description="Fact finding statement, separate from the raw report text.", min_length=1)
    proposal_reason: str = Field(description="Report-specific source fact reason.", min_length=1)
    source_refs: tuple[ProposalSourceRef, ...] = Field(description="Raw, NL, PlantUML, and ledger evidence pointers.", min_length=4)


class DAProposal(BaseModel):
    """Independent D/A and normative-obligation proposal."""

    model_config = ConfigDict(extra="forbid")

    d_tier: Literal["D2", "D1", "D0", "A0"] = Field(description="Proposed D/A tier under the frozen protocol.")
    a0_type: Literal["FALSE_POSITIVE"] | None = Field(description="Only permitted baseline A0 subtype, or null for D tiers.")
    normative_violation_status: Literal["ESTABLISHED", "NOT_ESTABLISHED"] = Field(description="Whether a source-backed obligation is proposed as violated.")
    defect_claim_status: Literal["DEFECT_CLAIM", "NO_DEFECT_CLAIM"] = Field(description="Whether the raw report is proposed as an author-source defect claim.")
    reason: str = Field(description="Report-specific D/A reason.", min_length=1)
    basis: str = Field(description="Report-specific D/A evidence basis.", min_length=1)
    source_refs: tuple[ProposalSourceRef, ...] = Field(description="Source pointers supporting the D/A proposal.", min_length=2)

    @model_validator(mode="after")
    def validate_da(self) -> "DAProposal":
        if self.d_tier == "A0" and self.a0_type != "FALSE_POSITIVE":
            raise ValueError("baseline A0 proposal requires FALSE_POSITIVE")
        if self.d_tier != "A0" and self.a0_type is not None:
            raise ValueError("D tiers cannot carry A0 subtype")
        if self.d_tier in {"D2", "D1"}:
            if self.normative_violation_status != "ESTABLISHED" or self.defect_claim_status != "DEFECT_CLAIM":
                raise ValueError("D2/D1 require an established defect claim")
        else:
            if self.normative_violation_status != "NOT_ESTABLISHED" or self.defect_claim_status != "NO_DEFECT_CLAIM":
                raise ValueError("D0/A0 require no established defect claim")
        return self


class DenseRelationProposalRow(BaseModel):
    """One expected-specific relation value in the dense proposal matrix."""

    model_config = ConfigDict(extra="forbid")

    expected_id: str = Field(description="Ledger expected ID evaluated by the proposal.", min_length=1)
    relation: Literal["FULL_MATCH", "PARTIAL_MATCH", "NO_MATCH"] = Field(description="Proposed relation to this expected item.")
    ledger_json_pointer: str = Field(description="JSON pointer to the expected ledger item.", min_length=1)
    basis: str = Field(description="Relation evidence basis or digest-level basis.", min_length=1)


class RelationProposal(BaseModel):
    """Complete expected-relation proposal and deterministic digest."""

    model_config = ConfigDict(extra="forbid")

    expected_count: int = Field(description="Expected-row count read from the frozen ledger; units are ledger items.", ge=0)
    rows: tuple[DenseRelationProposalRow, ...] = Field(description="All expected IDs in canonical ledger order.", min_length=1)
    full_match_ids: tuple[str, ...] = Field(description="Expected IDs proposed FULL_MATCH.")
    partial_match_ids: tuple[str, ...] = Field(description="Expected IDs proposed PARTIAL_MATCH.")
    no_match_count: int = Field(description="Number of dense rows proposed NO_MATCH; units are ledger rows.", ge=0)
    canonical_value_digest: str = Field(description="SHA-256 of canonical all-row expected_id/relation values.", pattern=r"^sha256:[0-9a-f]{64}$")
    digest_algorithm: str = Field(description="Deterministic digest algorithm description.", min_length=1)

    @model_validator(mode="after")
    def validate_relation_counts(self) -> "RelationProposal":
        if self.expected_count != len(self.rows):
            raise ValueError("relation expected_count does not equal dense row count")
        if self.no_match_count != sum(row.relation == "NO_MATCH" for row in self.rows):
            raise ValueError("dense relation NO_MATCH count mismatch")
        if tuple(row.expected_id for row in self.rows) != tuple(dict.fromkeys(row.expected_id for row in self.rows)):
            raise ValueError("dense relation IDs must be unique")
        if set(self.full_match_ids) & set(self.partial_match_ids):
            raise ValueError("FULL and PARTIAL relation IDs overlap")
        if set(self.full_match_ids) != {row.expected_id for row in self.rows if row.relation == "FULL_MATCH"}:
            raise ValueError("FULL relation ID mirror mismatch")
        if set(self.partial_match_ids) != {row.expected_id for row in self.rows if row.relation == "PARTIAL_MATCH"}:
            raise ValueError("PARTIAL relation ID mirror mismatch")
        return self


class TrackAReportProposal(BaseModel):
    """One independent raw-first proposal for one baseline raw report."""

    model_config = ConfigDict(extra="forbid")

    report_id: str = Field(description="Stable archived report identity.", min_length=1)
    pair_id: str = Field(description="Four-digit baseline pair ID.", pattern=r"^[0-9]{4}$")
    round: int = Field(description="Frozen baseline round number.", ge=1, le=3)
    finding_index: int = Field(description="Zero-based issue index in the raw record.", ge=0)
    review_status: Literal["PROPOSAL"] = Field(description="Proposal is not a final adjudication.")
    reviewer_id: str = Field(description="Independent Track A proposal identity.", min_length=1)
    blindness: ProposalBlindness = Field(description="Blind-input and no-provider attestations.")
    raw: RawProposalFinding = Field(description="Exact raw finding evidence.")
    author_source: AuthorSourceProposal = Field(description="Complete author-source evidence closure.")
    observed_fact: ObservedFactProposal = Field(description="Source fact finding.")
    d_a_proposal: DAProposal = Field(description="Proposed D/A and obligation finding.")
    relation_proposal: RelationProposal = Field(description="Complete dense ledger relation proposal.")
    evidence_gaps: tuple[str, ...] = Field(description="Explicit evidence gaps retained for later adjudication.", min_length=1)
    coverage_note: str = Field(description="Why this row is retained in the raw candidate universe.", min_length=1)

    @model_validator(mode="after")
    def validate_raw_basis_gap(self) -> "TrackAReportProposal":
        if self.raw.basis is None and "raw_basis_field_absent_in_record" not in self.evidence_gaps:
            raise ValueError("raw basis absence must be recorded as an evidence gap")
        return self


class TrackAScope(BaseModel):
    """Scope declaration and unresolved pre-v3 K-membership evidence."""

    model_config = ConfigDict(extra="forbid")

    requested: str = Field(description="User-requested baseline non-K pair range.", min_length=1)
    scope_gate: Literal["OPEN_EVIDENCE_GAP"] = Field(description="Machine-readable scope gate; this proposal cannot enter final adjudication until historical non-K membership is evidenced.")
    raw_candidate_count: int = Field(description="Count of raw reports retained as conservative candidates.", ge=0)
    pair_ids: tuple[str, ...] = Field(description="Requested pair IDs, including zero-report pairs.", min_length=20, max_length=20)
    preexisting_non_k_membership_available_from_allowed_inputs: Literal[False] = Field(description="False because allowed raw artifacts contain no frozen K membership map.")
    coverage_policy: str = Field(description="Conservative retention policy for unresolved scope membership.", min_length=1)
    missing_evidence: tuple[str, ...] = Field(description="Specific missing evidence items.", min_length=1)


class TrackAInputs(BaseModel):
    """Input archive paths and hashes used to materialize the proposal."""

    model_config = ConfigDict(extra="forbid")

    inventory_path: str = Field(description="Inventory path used for stable report identities.", min_length=1)
    inventory_sha256: str = Field(description="Inventory SHA-256.", pattern=r"^sha256:[0-9a-f]{64}$")
    ledger_path: Literal["reference/ledger.json"] = Field(description="Frozen reference ledger path.")
    ledger_sha256: str = Field(description="Ledger SHA-256.", pattern=r"^sha256:[0-9a-f]{64}$")
    ledger_expected_count: int = Field(description="Expected item count read from the frozen ledger; units are ledger items.", ge=0)


class TrackACoverage(BaseModel):
    """Deterministic batch coverage counters."""

    model_config = ConfigDict(extra="forbid")

    reports_materialized: int = Field(description="Reports written to the proposal.", ge=0)
    reports_with_explicit_annotations: int = Field(description="Reports with explicit human annotation table entries.", ge=0)
    reports_with_missing_annotations: tuple[str, ...] = Field(description="Report IDs lacking explicit annotation entries.")
    reports_with_145_relation_rows: int = Field(description="Reports with complete dense relation rows.", ge=0)
    source_full_read_claims: int = Field(description="Reports whose complete author source files were read.", ge=0)
    by_pair: dict[str, int] = Field(description="Report count by pair ID.")
    by_round: dict[str, int] = Field(description="Report count by round.")
    pair_coverage: dict[str, int] = Field(description="Report count for every requested pair ID, including zero.")


class TrackAProposal(BaseModel):
    """Canonical blind Track A proposal envelope for baseline pairs 0000-0019."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    schema_id: Literal["paper1.manual-adjudication.v3-baseline-ni.track-a-proposal.v1"] = Field(alias="schema", description="Versioned Track A proposal schema.")
    protocol_version: str = Field(description="Frozen D/A/relation protocol identifier.", min_length=1)
    proposal_role: str = Field(description="Proposal-only role statement.", min_length=1)
    generated_at_utc: str = Field(description="UTC materialization timestamp.", min_length=1)
    archive_relative_root: str = Field(description="Archive-relative root for all paths.", min_length=1)
    blind_input_policy: dict[str, tuple[str, ...]] = Field(description="Allowed and forbidden input declarations.")
    scope: TrackAScope = Field(description="Scope and evidence-gap declaration.")
    inputs: TrackAInputs = Field(description="Frozen input closure hashes.")
    coverage: TrackACoverage = Field(description="Provider-free deterministic coverage counters.")
    reports: tuple[TrackAReportProposal, ...] = Field(description="All retained raw report proposals.", min_length=1)

    @model_validator(mode="after")
    def validate_envelope(self) -> "TrackAProposal":
        if self.scope.raw_candidate_count != len(self.reports):
            raise ValueError("scope candidate count does not equal reports")
        if self.coverage.reports_materialized != len(self.reports):
            raise ValueError("coverage report count does not equal reports")
        if self.coverage.reports_with_explicit_annotations != len(self.reports):
            raise ValueError("proposal contains an implicit annotation")
        if self.coverage.reports_with_145_relation_rows != len(self.reports):
            raise ValueError("proposal is not densely closed")
        if any(report.relation_proposal.expected_count != self.inputs.ledger_expected_count for report in self.reports):
            raise ValueError("report relation count does not match input ledger count")
        return self
