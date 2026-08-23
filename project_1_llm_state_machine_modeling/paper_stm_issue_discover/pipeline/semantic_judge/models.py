"""Pydantic protocols for the arm-neutral issue #195 semantic Judge."""

from __future__ import annotations

import hashlib
from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class FrozenModel(BaseModel):
    """Base for immutable cross-stage Judge records with no implicit fields."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)


class MatchStrength(str, Enum):
    """Issue #195 dimension A: semantic relation between one report and expected issue."""

    FULL_MATCH = "FULL_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"
    NO_MATCH = "NO_MATCH"


class PositiveMatchStrength(str, Enum):
    """Provider-visible semantic relations that can support a valid report."""

    FULL_MATCH = "FULL_MATCH"
    PARTIAL_MATCH = "PARTIAL_MATCH"


class CoreClaimTruth(str, Enum):
    """Artifact-audited truth of a report before ledger ownership is derived."""

    VALID = "VALID"
    INVALID = "INVALID"


class ReportValidity(str, Enum):
    """Backend-derived issue #195 report truth and known/novel ownership."""

    VALID_KNOWN = "VALID_KNOWN"
    VALID_NOVEL = "VALID_NOVEL"
    INVALID = "INVALID"


class ReportField(str, Enum):
    """Candidate-report text fields that may be cited verbatim by a Judge decision."""

    CLAIM = "claim"
    WHERE = "where"
    PROPERTY = "property"
    VIOLATED_OBLIGATION = "violated_obligation"
    EXPECTED = "expected"
    OBSERVED = "observed"
    REASON = "reason"
    BASIS = "basis"


class CausalReportField(str, Enum):
    """Report fields eligible for complete causal-certificate audit."""

    OBSERVED = "observed"
    REASON = "reason"
    BASIS = "basis"


class ReportTextEvidenceRole(str, Enum):
    """Closed semantic role played by an exact quotation from the candidate report."""

    CLAIM_BOUNDARY = "CLAIM_BOUNDARY"
    CAUSAL_SUPPORT = "CAUSAL_SUPPORT"
    REFUTED_PREMISE = "REFUTED_PREMISE"


class CausalFieldVerdict(str, Enum):
    """Truth status of one complete report-owned causal field under artifact audit."""

    SUPPORTED = "SUPPORTED"
    MIXED = "MIXED"
    REFUTED = "REFUTED"


class MaterialAssertionVerdict(str, Enum):
    """Artifact truth of one material factual or causal assertion in a report field."""

    SUPPORTED = "SUPPORTED"
    REFUTED = "REFUTED"


class ArtifactAuthority(str, Enum):
    """Closed roles that prevent author source, lowered model, and facts being conflated."""

    NORMATIVE_SOURCE = "normative_source"
    AUTHOR_SOURCE = "author_source"
    CLOSED_MODEL = "closed_model"
    DETERMINISTIC_FACT = "deterministic_fact"
    MAPPING = "mapping"
    PROVENANCE = "provenance"


class ArtifactRole(str, Enum):
    """Complete common pair artifact roles exposed identically to both input adapters."""

    NATURAL_LANGUAGE = "natural_language"
    PLANTUML_SOURCE = "plantuml_source"
    FCSTM_MODEL = "fcstm_model"
    CANONICAL_SOURCE_IR = "canonical_source_ir"
    EXACT_SOURCE_INVENTORY = "exact_source_inventory"
    REFERENCE_INSPECTION = "reference_inspection"
    INSPECTION_EQUIVALENT_FACTS = "inspection_equivalent_facts"
    VERIFY_FACTS = "verify_facts"
    SMT_FACTS = "smt_facts"
    WORKING_CONTRACT = "working_contract"
    SOURCE_TRACE = "source_trace"
    CASE_REPORT = "case_report"


class CandidateEvidence(FrozenModel):
    """One report-owned evidence statement, never a method-only W/D/predicate verdict."""

    evidence_ref: str = Field(
        min_length=1,
        description="Anonymous evidence ID cited by the report itself; an arm with no report-owned evidence supplies an empty list, and downstream review uses this only to audit the claim, never as an eligibility gate.",
    )
    statement: str = Field(
        min_length=1,
        description="Technical evidence statement actually supplied by the report; this is candidate material and does not mean the Judge has confirmed its truth.",
    )


class CandidateReport(FrozenModel):
    """Arm-neutral projection of one actually published atomic technical report.

    Adapters produce this object and the unified Judge consumes it. It owns only
    semantic content present in the final report; it has no authority over truth,
    matching, W/D/L, predicates, or historical scores.
    """

    schema_version: Literal["paper1.semantic-judge.candidate-report.v1"] = Field(
        default="paper1.semantic-judge.candidate-report.v1",
        description="Candidate-report protocol version for persistence compatibility; it says nothing about report quality.",
    )
    report_id: str = Field(
        pattern=r"^R\d{4}$",
        description="Anonymous report ID within the pair, used only for exact closure; never infer experimental arm or semantics from its number, order, or prefix.",
    )
    claim: str = Field(
        min_length=1,
        description="Atomic technical claim actually published by the report; it is a candidate statement that the Judge must verify independently rather than trust directly.",
    )
    where: str | None = Field(
        default=None,
        description="Locus or where supplied by the report itself; null means the original report omitted it, and an adapter may not add it for that arm.",
    )
    property: str | None = Field(
        default=None,
        description="Property explicitly claimed as violated by the report; null means the original report has no typed property and must never block FULL or validity.",
    )
    violated_obligation: str | None = Field(
        default=None,
        description="Normative obligation stated by the report; null means there was no separate field, so downstream review may audit claim/reason but the adapter may not synthesize one.",
    )
    expected: str | None = Field(
        default=None,
        description="Expected behavior described by the report; null means the original report did not separate expected from observed, not that it lacks semantic content.",
    )
    observed: str | None = Field(
        default=None,
        description="Observed behavior described by the report; null means the original report did not provide a separate observation and must not be penalized for the missing field.",
    )
    reason: str = Field(
        min_length=1,
        description="Causal explanation actually owned by the report at publication; it is candidate evidence that the Judge independently checks against common artifacts.",
    )
    basis: str | None = Field(
        default=None,
        description="Artifact basis actually owned by the report; null means the source arm had no basis field, so no method-only dossier may be inferred or added.",
    )
    source_refs: tuple[str, ...] = Field(
        default_factory=tuple,
        description="NL, source, model, or fact references actually carried by the report; an empty tuple means the original report had no structured references and does not affect eligibility.",
    )
    evidence: tuple[CandidateEvidence, ...] = Field(
        default_factory=tuple,
        description="Publicly auditable evidence statements owned by the report; excludes W/D/L, predicates, compilation plans, and hidden intermediate reasoning.",
    )


class ReportTextEvidence(FrozenModel):
    """Exact report-owned text used to delimit or audit one Judge decision.

    The backend materializes this evidence from provider-selected report-field
    references, verifies the exact text, and records its hash. It proves textual
    provenance only; common artifacts still determine whether the premise is true.
    """

    report_field: ReportField = Field(
        description="CandidateReport scalar text field containing exact_quote; this is a provenance selector, not a semantic conclusion.",
    )
    exact_quote: str = Field(
        min_length=1,
        description="Case-sensitive verbatim substring from the selected report field; generated paraphrases and facts found only in common artifacts are forbidden.",
    )
    semantic_role: ReportTextEvidenceRole = Field(
        description="How the quoted report-owned text participates in this decision: claim boundary, artifact-compatible causal support, or a premise refuted by common artifacts.",
    )
    reason: str = Field(
        min_length=1,
        description="Why this exact quotation has the selected role in the current relation or validity judgment; it must not add content absent from the quote.",
    )
    basis: str = Field(
        min_length=1,
        description="Auditable field-level provenance for the quotation and the supplied artifact facts used to verify or refute it.",
    )


class MaterialAssertionAuditJudgment(FrozenModel):
    """Provider audit of one material assertion from a complete causal field."""

    assertion_id: str = Field(
        pattern=r"^A[1-9][0-9]*$",
        description="Field-local assertion ID in A1, A2, ... sequence; IDs are audit keys only and carry no semantic weight.",
    )
    assertion: str = Field(
        min_length=1,
        description="Concise English statement of one complete material factual assertion, modeling-semantic assumption, or causal link from the report field; never combine independently testable assertions or hide a refuted premise inside a supported row.",
    )
    verdict: MaterialAssertionVerdict = Field(
        description="SUPPORTED only when this exact material assertion is artifact-compatible; REFUTED when the common closure contradicts it or cannot sustain its factual, modeling-semantic, or causal premise.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of this assertion verdict, without substituting a nearby true defect for the report's stated premise.",
    )
    basis: str = Field(
        min_length=1,
        description="Common-artifact evidence that directly verifies or refutes this assertion.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied report-field and common-artifact references actually used for this assertion verdict.",
    )


class CausalFieldAuditJudgment(FrozenModel):
    """Provider audit of one complete causal field owned by a candidate report.

    The Judge produces one row for every non-empty reason, basis, and observed
    field. Each row exhaustively decomposes the field into material assertions.
    The backend retrieves the immutable source text, computes its hash, and derives
    the whole-field verdict from the assertion verdicts instead of asking the
    provider to repeat a potentially contradictory aggregate classification.
    """

    report_field: CausalReportField = Field(
        description="Complete causal field from the supplied CandidateReport, not a reason or basis generated by this judgment. Audit each non-null CandidateReport reason, basis, and observed field exactly once and never invent a row for a null field.",
    )
    material_assertion_audits: tuple[MaterialAssertionAuditJudgment, ...] = Field(
        min_length=1,
        description="Exhaustive ordered decomposition of every material factual assertion, modeling-semantic assumption, and causal link in the complete field. Use one row per independently testable assertion; omission cannot make a field supported.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation covering the complete assertion audit, including every refuted premise; do not state a provider-selected whole-field enum.",
    )
    basis: str = Field(
        min_length=1,
        description="Common-artifact evidence used for the exhaustive assertion audit, with enough detail for the backend-derived whole-field verdict to be reviewed.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Report-field and common-artifact references actually used for the complete assertion audit; the tuple must not be empty.",
    )

    @model_validator(mode="after")
    def material_assertion_ids_are_exact(self) -> CausalFieldAuditJudgment:
        """Require canonical contiguous assertion identities within one field audit."""

        actual = [item.assertion_id for item in self.material_assertion_audits]
        expected = [f"A{index}" for index in range(1, len(actual) + 1)]
        if actual != expected:
            raise ValueError(
                "material_assertion_audits must use contiguous IDs in source order; "
                f"expected={expected}, actual={actual}"
            )
        return self


def derive_causal_field_verdict(
    assertions: tuple[MaterialAssertionAuditJudgment, ...],
) -> CausalFieldVerdict:
    """Derive a whole-field verdict from an exhaustive material-assertion audit."""

    verdicts = {item.verdict for item in assertions}
    if verdicts == {MaterialAssertionVerdict.SUPPORTED}:
        return CausalFieldVerdict.SUPPORTED
    if verdicts == {MaterialAssertionVerdict.REFUTED}:
        return CausalFieldVerdict.REFUTED
    return CausalFieldVerdict.MIXED


class ReportCausalFieldAudit(FrozenModel):
    """Persisted artifact audit of one complete candidate-report causal field.

    The backend materializes exact_text and exact_text_sha256 from the immutable
    CandidateReport after validating the provider's field-reference closure. The
    provider supplies only the field selector and semantic verdict, so verbatim
    copying can neither fail the call nor truncate the persisted audit evidence.
    """

    report_field: CausalReportField = Field(
        description="Complete CandidateReport reason, basis, or observed field audited exactly once by the provider and materialized by the backend.",
    )
    exact_text: str = Field(
        min_length=1,
        description="Complete case-sensitive CandidateReport field value retrieved deterministically by the backend, never copied or paraphrased by the provider.",
    )
    exact_text_sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 digest of exact_text computed deterministically by the backend for persisted provenance verification.",
    )
    material_assertion_audits: tuple[MaterialAssertionAuditJudgment, ...] = Field(
        min_length=1,
        description="Provider-authored exhaustive assertion audit retained verbatim so the backend-derived whole-field verdict remains independently auditable.",
    )
    verdict: CausalFieldVerdict = Field(
        description="Backend-derived whole-field verdict: all assertions supported yields SUPPORTED, mixed assertion truth yields MIXED, and all assertions refuted yields REFUTED.",
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of the whole-field verdict that addresses every material causal clause rather than only a convenient fragment.",
    )
    basis: str = Field(
        min_length=1,
        description="Common-artifact evidence used to verify or refute the complete field, with enough detail to audit a MIXED or REFUTED classification.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Report-field and common-artifact references actually used for the whole-field verdict; the tuple must not be empty.",
    )

    @model_validator(mode="after")
    def persisted_audit_is_derived_and_hashed(self) -> ReportCausalFieldAudit:
        """Reject persisted rows with inconsistent source hashes or field verdicts."""

        expected = "sha256:" + hashlib.sha256(
            self.exact_text.encode("utf-8")
        ).hexdigest()
        if self.exact_text_sha256 != expected:
            raise ValueError(
                "exact_text_sha256 must equal the SHA-256 digest of exact_text; "
                f"expected={expected}, actual={self.exact_text_sha256}"
            )
        expected_verdict = derive_causal_field_verdict(self.material_assertion_audits)
        if self.verdict != expected_verdict:
            raise ValueError(
                "verdict must be derived from material_assertion_audits; "
                f"expected={expected_verdict.value}, actual={self.verdict.value}"
            )
        return self


class ExpectedAxisHints(FrozenModel):
    """Optional frozen-ledger taxonomy hints that describe but never gate semantic FULL."""

    defect_locus: str | None = Field(
        default=None,
        description="Ledger hint describing the defect locus; null means unannotated, and the Judge must not require field-for-field identity from a report.",
    )
    defect_element: str | None = Field(
        default=None,
        description="Ledger hint describing an element; it only aids interpretation of the expected issue and is not an exact-field hit gate.",
    )
    defect_qualifier: str | None = Field(
        default=None,
        description="Ledger qualifier hint; null does not change the expected issue's identity.",
    )
    defect_logic_kind: str | None = Field(
        default=None,
        description="Ledger logic-kind hint used only as semantic context, never as a report eligibility condition.",
    )
    defect_reference: str | None = Field(
        default=None,
        description="Reference-authority hint recorded by the ledger; it is unrelated to report evidence strength or W.",
    )


class ExpectedIssue(FrozenModel):
    """One D2/D1 frozen expected issue after removing D/L and scoring metadata.

    The ledger adapter produces this expected-denominator object. It defines the
    semantic target for recall, but does not decide any report's truth or match.
    """

    schema_version: Literal["paper1.semantic-judge.expected-issue.v1"] = Field(
        default="paper1.semantic-judge.expected-issue.v1",
        description="Anonymous expected-issue projection version; it does not expose ledger D or L.",
    )
    expected_id: str = Field(
        pattern=r"^E\d{4}$",
        description="Anonymous expected ID within the pair, used only for the complete relation matrix; the original ledger ID remains only in provider-external mapping.",
    )
    summary: str = Field(
        min_length=1,
        description="Core defect summary from the frozen ledger; read it together with complete detail rather than treating its opening phrase or taxonomy as the only matchable facet.",
    )
    detail: str = Field(
        min_length=1,
        description="Complete frozen-ledger mechanism, locus, consequence, boundary, and explicit actionable facets. A report may FULL-match an independently actionable core facet whose repair materially mitigates the expected violation even when it does not reproduce every facet.",
    )
    source_statement: str | None = Field(
        default=None,
        description="Original or reviewed technical statement from ledger provenance; null means the field is absent and does not change the expected denominator.",
    )
    axes: ExpectedAxisHints = Field(
        description="Ledger taxonomy hints used only for interpretation; they must not become an exact locus/property/scope/direction gate.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Ledger or NL artifact references that trace the expected issue; Judge basis should verify them together with the common closure.",
    )


class ArtifactDocument(FrozenModel):
    """One immutable common artifact with explicit authority and exact content hash."""

    artifact_id: str = Field(
        pattern=r"^artifact:[a-z0-9_-]+$",
        description="Stable artifact reference within the pair for exact citation in Judge basis and source_refs.",
    )
    role: ArtifactRole = Field(
        description="Closed-set role of the artifact in the unified closure; identical for every experimental arm on the same pair."
    )
    authority: ArtifactAuthority = Field(
        description="Artifact authority boundary that prevents authored source, closed model, deterministic facts, and provenance from substituting for one another."
    )
    sha256: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of the projected artifact content used to prove common-closure identity across arms.",
    )
    schema_version: str = Field(
        min_length=1, description="Artifact's own schema/version; plain text uses an explicit text version."
    )
    content: str = Field(
        min_length=1,
        description="Complete UTF-8 text or stable JSON text; factual authority comes from role and authority, not from a report.",
    )
    reason: str = Field(
        min_length=1, description="Why this artifact belongs in the common closure required for truth arbitration."
    )
    basis: str = Field(
        min_length=1, description="Artifact source and builder-algorithm basis with no experimental-arm or historical-score information."
    )


class JudgeArtifactClosure(FrozenModel):
    """Arm-independent pair evidence closure used for report validity arbitration."""

    schema_version: Literal["paper1.semantic-judge.artifact-closure.v2"] = Field(
        default="paper1.semantic-judge.artifact-closure.v2",
        description="Common artifact-closure schema version; any content or truncation-policy change must alter the version or hash.",
    )
    pair_id: str = Field(
        pattern=r"^\d{4}$",
        description="Frozen pair identity used only to select common artifacts; it does not identify an experimental arm.",
    )
    artifacts: tuple[ArtifactDocument, ...] = Field(
        min_length=1,
        description="Complete common artifacts in fixed role order; never add, remove, reorder, or truncate them by report-producing arm.",
    )
    closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="SHA-256 of stable closure JSON excluding this field, used as apples-to-apples evidence.",
    )
    reason: str = Field(
        min_length=1, description="Why the common closure is sufficient to audit truth and fair to both arms."
    )
    basis: str = Field(
        min_length=1, description="Closure-builder version, PairInput, and per-artifact hash basis."
    )

    @model_validator(mode="after")
    def unique_artifact_roles_and_ids(self) -> JudgeArtifactClosure:
        ids = [item.artifact_id for item in self.artifacts]
        roles = [item.role for item in self.artifacts]
        if len(ids) != len(set(ids)):
            raise ValueError(
                f"artifact_closure.artifacts has duplicate artifact_id values: {ids}"
            )
        if len(roles) != len(set(roles)):
            raise ValueError(
                f"artifact_closure.artifacts has duplicate role values: {roles}"
            )
        return self


class UnifiedJudgeInput(FrozenModel):
    """Complete arm-neutral provider input shared after source-specific adaptation."""

    schema_version: Literal["paper1.semantic-judge.input.v1"] = Field(
        default="paper1.semantic-judge.input.v1",
        description="Unified Judge input protocol version; both arms must enter the same class and serialization.",
    )
    protocol_version: str = Field(
        min_length=1,
        description="Frozen issue #195 protocol version; a semantic change invalidates scores from older versions.",
    )
    pair_id: str = Field(
        pattern=r"^\d{4}$",
        description="Pair under assessment; input contains no arm name, historical result, or method label.",
    )
    reports: tuple[CandidateReport, ...] = Field(
        description="Anonymous arm-neutral projections of actually published reports; may be empty, and may not add semantics absent from the source arm."
    )
    expected_issues: tuple[ExpectedIssue, ...] = Field(
        min_length=1,
        description="Anonymous projection of the pair's frozen D2+D1 expected denominator; contains no D or L.",
    )
    artifact_closure: JudgeArtifactClosure = Field(
        description="Common truth-audit closure serialized identically for every experimental arm."
    )
    reason: str = Field(
        min_length=1, description="How anonymous reports, frozen expected issues, and the common closure compose this input."
    )
    basis: str = Field(
        min_length=1,
        description="Adapter, ledger-projection, artifact-builder, and protocol-hash basis.",
    )

    @model_validator(mode="after")
    def exact_input_identity(self) -> UnifiedJudgeInput:
        if self.artifact_closure.pair_id != self.pair_id:
            raise ValueError(
                "artifact_closure.pair_id conflicts with input pair_id: "
                f"expected {self.pair_id}, actual {self.artifact_closure.pair_id}"
            )
        report_ids = [item.report_id for item in self.reports]
        expected_ids = [item.expected_id for item in self.expected_issues]
        if len(report_ids) != len(set(report_ids)):
            raise ValueError(
                f"reports contains duplicate report_id values: {report_ids}"
            )
        if len(expected_ids) != len(set(expected_ids)):
            raise ValueError(
                f"expected_issues contains duplicate expected_id values: {expected_ids}"
            )
        return self


class RelationAssessment(FrozenModel):
    """One dense backend-materialized relation for an exact report/expected pair.

    Provider output contains one compact positional decision per expected issue,
    with detailed evidence only on positive rows and grouped evidence for NO rows.
    The backend materializes this complete matrix after validating report truth.
    A FULL or PARTIAL row therefore always belongs to a valid known report.
    """

    report_id: str = Field(
        min_length=1, description="Anonymous report ID being compared; it must come from the exact input closure."
    )
    expected_id: str = Field(
        min_length=1,
        description="Anonymous expected ID being compared; it must come from the exact input closure.",
    )
    match: MatchStrength = Field(
        description="Final relation after validity-first closure; FULL and PARTIAL are legal only for a valid known report, while PARTIAL remains support rather than a hit or false positive."
    )
    report_text_evidence: tuple[ReportTextEvidence, ...] = Field(
        min_length=1,
        description="Backend-materialized report-owned text delimiting this pairwise relation. Every row has CLAIM_BOUNDARY; each FULL/PARTIAL row also cites the report-level SUPPORTED causal certificate, while a NO row does not imply validity or invalidity.",
    )
    reason: str = Field(
        min_length=1,
        description="Why the pair is FULL, PARTIAL, or NO; explain root-cause, obligation, symptom, or repair-overlap boundaries.",
    )
    basis: str = Field(
        min_length=1,
        description="Supplied report, expected issue, and common-artifact facts that support the relation judgment.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Report, expected, and artifact references actually used by the relation judgment; must not be empty.",
    )


class SupportedRelationJudgment(FrozenModel):
    """One provider-authored FULL or PARTIAL relation for a valid report.

    The Judge produces this sparse row only after the report's core claim is
    valid. The backend verifies exact IDs, relation closure, report-owned field
    references, and the selected report-level causal certificate before it
    materializes the dense relation audit.
    """

    report_id: str = Field(
        min_length=1,
        description="Anonymous report ID from the exact input closure; the value carries no semantic or experimental information.",
    )
    expected_id: str = Field(
        min_length=1,
        description="Anonymous expected ID receiving this positive relation; it must occur in the exact expected closure.",
    )
    match: PositiveMatchStrength = Field(
        description="Artifact-supported positive relation: FULL contributes a hit after backend ownership derivation, while PARTIAL contributes support only."
    )
    report_field_refs: tuple[ReportField, ...] = Field(
        min_length=1,
        description="Non-null CandidateReport fields that delimit this exact relation; include claim and any locus, property, obligation, or behavior field actually used. The backend materializes their complete text and hashes.",
    )
    causal_certificate_field: CausalReportField = Field(
        description="Complete report-owned reason, basis, or observed field whose SUPPORTED audit establishes the causal premise used by this relation; it must match the report-level validity certificate."
    )
    reason: str = Field(
        min_length=1,
        description="English expected-specific explanation of why this valid report is FULL or PARTIAL, including the exact root-cause, obligation, symptom, or repair overlap."
    )
    basis: str = Field(
        min_length=1,
        description="English basis citing the supplied report, expected issue, and common artifact facts that establish this positive relation."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied report, expected, and artifact references actually used for this relation; references are evidence pointers, not free-form conclusions."
    )


class NoMatchRelationJudgment(FrozenModel):
    """One explicit minimal NO relation in a provider relation partition.

    NO rows carry only identity and the closed enum. Shared NO reason, basis, and
    source references remain at report level, avoiding repeated prose without
    allowing an omitted expected issue to default silently to NO.
    """

    expected_id: str = Field(
        min_length=1,
        description="Anonymous expected ID receiving an explicit NO_MATCH relation; the dynamic schema fixes its exact position and identity.",
    )
    match: Literal[MatchStrength.NO_MATCH] = Field(
        description="Explicit NO_MATCH enum; omission never implies NO and this row can never carry FULL or PARTIAL.",
    )


class ReportJudgment(FrozenModel):
    """One validity-first provider judgment with sparse exhaustive relations.

    The Judge produces core truth, a complete causal certificate, and one typed
    relation decision at every expected position. It never produces final
    VALID_KNOWN or VALID_NOVEL ownership; the backend derives that classification
    from core_truth and the validated relation partition.
    """

    report_id: str = Field(
        min_length=1, description="Anonymous ID of the assessed report; it must occur exactly once in the response."
    )
    core_truth: CoreClaimTruth = Field(
        description="Artifact-audited truth before ledger ownership. Select VALID exactly when causal_certificate_field has verdict SUPPORTED; select INVALID exactly when it has verdict MIXED or REFUTED, with zero positive relations and exhaustive NO closure."
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="Stable phrase key based on an actionable technical root cause; never use report ID/order or merge nearby claims with different properties or sources.",
    )
    causal_field_audits: tuple[CausalFieldAuditJudgment, ...] = Field(
        min_length=1,
        description="Exactly one whole-field verdict for every non-null reason, basis, and observed field in the supplied CandidateReport. Select report fields without copying their text; the backend materializes exact text and hash after closure validation."
    )
    causal_certificate_field: CausalReportField = Field(
        description="One audited CandidateReport field carrying the core truth certificate. Its verdict and core_truth must agree exactly: SUPPORTED with VALID, or MIXED/REFUTED with INVALID."
    )
    relation_decisions: tuple[
        SupportedRelationJudgment | NoMatchRelationJudgment, ...
    ] = Field(
        min_length=1,
        description="Exactly one decision per expected issue in dynamic-schema order. FULL/PARTIAL rows retain expected-specific evidence; NO rows explicitly retain identity without repeated prose."
    )
    no_match_reason: str | None = Field(
        min_length=1,
        description="English group explanation for all explicit NO_MATCH decision rows. It is required when any NO row exists and must be null when every row is positive."
    )
    no_match_basis: str | None = Field(
        min_length=1,
        description="English report, expected, and artifact basis for a non-empty grouped NO closure; null means every expected issue has a positive relation."
    )
    no_match_source_refs: tuple[str, ...] | None = Field(
        description="Supplied references used for a non-empty grouped NO closure; null means no NO relation exists, while an empty tuple is never valid."
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of why the report's own core technical claim is VALID or INVALID under the complete artifact audit; do not discuss backend-derived known/novel ownership."
    )
    basis: str = Field(
        min_length=1,
        description="NL, PlantUML, FCSTM, deterministic facts, or complete semantic-audit basis used for the truth judgment.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied source references actually used for report validity; must not be empty.",
    )


class JudgeResponse(FrozenModel):
    """Validity-first provider response with sparse evidence and exact decisions."""

    schema_version: Literal["semantic-judge.response.v10"] = Field(
        default="semantic-judge.response.v10",
        description="Provider response version implementing assertion-level causal audits, core truth, and a provider-native exact positional relation partition.",
    )
    report_judgments: tuple[ReportJudgment, ...] = Field(
        description="Core truth, causal certificate, sparse relation closure, root cause, reason, and basis for every report exactly once."
    )
    reason: str = Field(
        min_length=1, description="Overall semantic conclusion of the complete reading; do not merely restate counts."
    )
    basis: str = Field(
        min_length=1,
        description="Protocol, anonymous input, and common artifact-closure basis used by this reading.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied artifact, report, and expected references actually used by the top-level reading.",
    )


class ReportAssessment(FrozenModel):
    """One dimension-B validity decision plus exhaustive relation-derived ownership."""

    report_id: str = Field(
        min_length=1, description="Anonymous ID of the assessed report; it must occur exactly once in the response."
    )
    core_truth: CoreClaimTruth = Field(
        description="Provider-audited core claim truth retained separately from the backend-derived known, novel, or invalid classification."
    )
    validity: ReportValidity = Field(
        description="Backend-derived issue #195 final report class; only INVALID is a semantic false positive."
    )
    full_expected_ids: tuple[str, ...] = Field(
        description="All expected IDs that FULL_MATCH this report, derived exactly from the relation matrix."
    )
    partial_expected_ids: tuple[str, ...] = Field(
        description="All expected IDs that PARTIAL_MATCH this report; they support coverage but count as neither hit nor false positive."
    )
    no_match_expected_ids: tuple[str, ...] = Field(
        description="All expected IDs with NO_MATCH for this report; the three relation sets must exactly cover the expected closure."
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="Stable phrase key based on an actionable technical root cause, used for redundancy and cluster precision; never use report ID or order.",
    )
    report_text_evidence: tuple[ReportTextEvidence, ...] = Field(
        min_length=1,
        description="Validated exact report-owned quotations retained from ReportJudgment for downstream causal-certificate audit.",
    )
    causal_field_audits: tuple[ReportCausalFieldAudit, ...] = Field(
        min_length=1,
        description="Validated complete causal-field audits retained from ReportJudgment, including true contextual fields that do not independently support the report's core claim.",
    )
    reason: str = Field(
        min_length=1,
        description="Why the report claim is true or false and why a valid report is KNOWN or NOVEL; unmatched status alone proves neither.",
    )
    basis: str = Field(
        min_length=1,
        description="NL, PlantUML, FCSTM, deterministic facts, or complete semantic-audit basis used for the truth judgment.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied source references actually used for report validity; must not be empty.",
    )

    @model_validator(mode="after")
    def core_truth_and_ownership_are_closed(self) -> ReportAssessment:
        relation_sets = (
            self.full_expected_ids,
            self.partial_expected_ids,
            self.no_match_expected_ids,
        )
        flattened = [value for values in relation_sets for value in values]
        if len(flattened) != len(set(flattened)):
            raise ValueError(
                f"report_assessment[{self.report_id}] relation ID sets overlap or contain duplicates: {flattened}"
            )
        has_positive = bool(self.full_expected_ids or self.partial_expected_ids)
        expected_validity = (
            ReportValidity.INVALID
            if self.core_truth == CoreClaimTruth.INVALID
            else ReportValidity.VALID_KNOWN
            if has_positive
            else ReportValidity.VALID_NOVEL
        )
        if self.core_truth == CoreClaimTruth.INVALID and has_positive:
            raise ValueError(
                f"report_assessment[{self.report_id}] core_truth=INVALID requires all relations NO_MATCH; "
                f"full={self.full_expected_ids}, partial={self.partial_expected_ids}"
            )
        if self.validity != expected_validity:
            raise ValueError(
                f"report_assessment[{self.report_id}].validity must be backend-derived as "
                f"{expected_validity.value}; actual={self.validity.value}, core_truth={self.core_truth.value}, "
                f"has_positive_relation={has_positive}"
            )
        return self


class ExpectedAssessment(FrozenModel):
    """One exhaustive expected-side coverage decision derived from valid reports."""

    expected_id: str = Field(
        min_length=1, description="Anonymous ID of the summarized expected issue; it must occur exactly once in the response."
    )
    full_report_ids: tuple[str, ...] = Field(
        description="Report IDs with FULL relation to this expected issue and VALID_KNOWN report validity."
    )
    partial_report_ids: tuple[str, ...] = Field(
        description="Report IDs with PARTIAL relation to this expected issue and VALID_KNOWN report validity."
    )
    no_support_report_ids: tuple[str, ...] = Field(
        description="Every remaining report ID that provides no valid FULL or PARTIAL support."
    )
    hit: bool = Field(
        description="Whether any VALID_KNOWN plus FULL_MATCH report exists; only this condition contributes a primary hit."
    )
    supported: bool = Field(
        description="Whether any VALID_KNOWN plus FULL or PARTIAL report exists; INVALID reports never contribute support."
    )
    reason: str = Field(
        min_length=1,
        description="Semantic explanation of this expected issue's hit/support status; duplicate reports still count the expected issue only once.",
    )
    basis: str = Field(
        min_length=1, description="Corresponding relation, validity, and common-artifact basis."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Expected, report, and artifact references actually used by this expected assessment.",
    )


class JudgeReading(FrozenModel):
    """One complete independent or arbitrated issue #195 reading of a pair."""

    schema_version: Literal["semantic-judge.reading.v4"] = Field(
        default="semantic-judge.reading.v4",
        description="Complete dense reading version with backend-hashed causal source text and assertion-derived field verdicts; it does not encode primary or arbitration role.",
    )
    relations: tuple[RelationAssessment, ...] = Field(
        description="Complete report-by-expected matrix including every NO_MATCH; it must not be sparse."
    )
    report_assessments: tuple[ReportAssessment, ...] = Field(
        description="Dimension-B and clustering assessment for every report exactly once."
    )
    expected_assessments: tuple[ExpectedAssessment, ...] = Field(
        description="Hit/support audit for every expected issue exactly once."
    )
    reason: str = Field(
        min_length=1, description="Overall semantic conclusion of the complete reading; do not merely restate counts."
    )
    basis: str = Field(
        min_length=1,
        description="Protocol, anonymous input, and common artifact-closure basis used by this reading.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied artifact, report, and expected references actually used by the top-level reading.",
    )

    @model_validator(mode="after")
    def dense_relation_and_metric_closure(self) -> JudgeReading:
        report_by_id = {row.report_id: row for row in self.report_assessments}
        expected_by_id = {row.expected_id: row for row in self.expected_assessments}
        if len(report_by_id) != len(self.report_assessments):
            raise ValueError("report_assessments contains duplicate report_id values")
        if len(expected_by_id) != len(self.expected_assessments):
            raise ValueError("expected_assessments contains duplicate expected_id values")
        expected_keys = {
            (report_id, expected_id)
            for report_id in report_by_id
            for expected_id in expected_by_id
        }
        relation_by_key = {
            (row.report_id, row.expected_id): row for row in self.relations
        }
        if len(relation_by_key) != len(self.relations) or set(relation_by_key) != expected_keys:
            raise ValueError(
                "JudgeReading.relations must cover every report/expected pair exactly once; "
                f"missing={sorted(expected_keys - set(relation_by_key))}, "
                f"extra={sorted(set(relation_by_key) - expected_keys)}, "
                f"duplicate_count={len(self.relations) - len(relation_by_key)}"
            )
        for report_id, assessment in report_by_id.items():
            by_match = {
                match: tuple(
                    expected_id
                    for expected_id in expected_by_id
                    if relation_by_key[(report_id, expected_id)].match == match
                )
                for match in MatchStrength
            }
            actual = (
                assessment.full_expected_ids,
                assessment.partial_expected_ids,
                assessment.no_match_expected_ids,
            )
            expected = (
                by_match[MatchStrength.FULL_MATCH],
                by_match[MatchStrength.PARTIAL_MATCH],
                by_match[MatchStrength.NO_MATCH],
            )
            if actual != expected:
                raise ValueError(
                    f"report_assessment[{report_id}] relation sets conflict with dense matrix; "
                    f"expected={expected}, actual={actual}"
                )
        for expected_id, assessment in expected_by_id.items():
            full = tuple(
                report_id
                for report_id in report_by_id
                if relation_by_key[(report_id, expected_id)].match == MatchStrength.FULL_MATCH
            )
            partial = tuple(
                report_id
                for report_id in report_by_id
                if relation_by_key[(report_id, expected_id)].match == MatchStrength.PARTIAL_MATCH
            )
            no_support = tuple(
                report_id
                for report_id in report_by_id
                if report_id not in set(full) | set(partial)
            )
            actual = (
                assessment.full_report_ids,
                assessment.partial_report_ids,
                assessment.no_support_report_ids,
                assessment.hit,
                assessment.supported,
            )
            expected = (full, partial, no_support, bool(full), bool(full or partial))
            if actual != expected:
                raise ValueError(
                    f"expected_assessment[{expected_id}] conflicts with dense matrix; "
                    f"expected={expected}, actual={actual}"
                )
        return self


class ConflictKind(str, Enum):
    """Deterministically detectable disagreements requiring semantic arbitration."""

    RELATION = "relation"
    CORE_TRUTH = "core_truth"
    ROOT_CAUSE_CLUSTER = "root_cause_cluster"


class ConflictRecord(FrozenModel):
    """Audit trail for one primary-reading disagreement and arbitrated outcome."""

    kind: ConflictKind = Field(
        description="Whether the conflict concerns relation, core claim truth, or root-cause clustering."
    )
    object_ref: str = Field(
        min_length=1,
        description="Stable anonymous reference to the conflicted object, such as report:R0001/expected:E0002.",
    )
    reading_1_value: str = Field(
        min_length=1, description="Enum or cluster value from the first independent reading."
    )
    reading_2_value: str = Field(
        min_length=1, description="Enum or cluster value from the second independent reading."
    )
    final_value: str = Field(
        min_length=1, description="Final value selected after re-reading complete artifacts; it cannot be UNKNOWN."
    )
    reason: str = Field(
        min_length=1, description="Why this final value was selected instead of majority voting or arm-specific substitute credit."
    )
    basis: str = Field(
        min_length=1, description="Artifact basis for the corresponding relation or report in the final reading."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="Supplied references actually used to arbitrate the conflict."
    )


class ReadingDisagreement(FrozenModel):
    """Provider-visible primary disagreement before a final value is selected."""

    kind: ConflictKind = Field(
        description="Relation, core-truth, or root-cause-clustering conflict type requiring arbitration."
    )
    object_ref: str = Field(
        min_length=1,
        description="Anonymous report/expected object reference for the conflict; it does not expose a source-arm ID.",
    )
    reading_1_value: str = Field(min_length=1, description="Structured value from the first independent reading.")
    reading_2_value: str = Field(min_length=1, description="Structured value from the second independent reading.")


class ArbitrationInput(FrozenModel):
    """Complete typed arbitration input containing no arm or method-only metadata."""

    schema_version: Literal["semantic-judge.arbitration-input.v5"] = Field(
        default="semantic-judge.arbitration-input.v5",
        description="Targeted arbitration-input version carrying assertion-level causal audits and positional relation partitions only for substantive conflicts.",
    )
    judge_input: UnifiedJudgeInput = Field(
        description="Anonymous reports, expected issues, and common artifact closure identical to the primary input."
    )
    primary_conflicting_judgments_1: tuple[ReportJudgment, ...] = Field(
        min_length=1,
        description="Only first-reading report judgments named by the conflict set; verified non-conflicting judgments are omitted and reused by the backend."
    )
    primary_conflicting_judgments_2: tuple[ReportJudgment, ...] = Field(
        min_length=1,
        description="Only second-reading report judgments named by the conflict set, aligned exactly with the first-reading conflict IDs."
    )
    disagreements: tuple[ReadingDisagreement, ...] = Field(
        min_length=1,
        description="All substantive conflicts found by deterministic comparison of relation enums, core truth, and clusters; wording differences are excluded."
    )
    reason: str = Field(
        min_length=1, description="Why complete artifacts must be reviewed again instead of voting or retaining UNKNOWN."
    )
    basis: str = Field(
        min_length=1, description="Issue #195 dual-reading arbitration contract and exact conflict detection."
    )

    @model_validator(mode="after")
    def exact_conflicting_report_closure(self) -> ArbitrationInput:
        conflicted_ids = {
            row.object_ref.split("/", 1)[0].removeprefix("report:")
            for row in self.disagreements
        }
        first_ids = [row.report_id for row in self.primary_conflicting_judgments_1]
        second_ids = [row.report_id for row in self.primary_conflicting_judgments_2]
        if (
            set(first_ids) != conflicted_ids
            or len(first_ids) != len(set(first_ids))
            or set(second_ids) != conflicted_ids
            or len(second_ids) != len(set(second_ids))
        ):
            raise ValueError(
                "ArbitrationInput primary conflicting judgments must cover every conflicted "
                f"report exactly once; expected={sorted(conflicted_ids)}, "
                f"reading_1={first_ids}, reading_2={second_ids}"
            )
        return self


class ArbitrationResponse(FrozenModel):
    """Targeted provider response replacing only conflicted report judgments."""

    schema_version: Literal["semantic-judge.arbitration-response.v4"] = Field(
        default="semantic-judge.arbitration-response.v4",
        description="Conflict-only arbitration response version using assertion-level causal audits and exact positional relation partitions; unchanged report judgments are never regenerated.",
    )
    report_judgments: tuple[ReportJudgment, ...] = Field(
        min_length=1,
        description="One complete sparse replacement for every conflicted report exactly once and no row for a non-conflicting report."
    )
    reason: str = Field(
        min_length=1,
        description="English explanation of how the targeted re-audit resolves the complete conflict set without voting."
    )
    basis: str = Field(
        min_length=1,
        description="English common-artifact and primary-disagreement basis for the targeted replacements."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Supplied report, expected, and artifact references actually used for targeted arbitration."
    )


class UsageReceipt(FrozenModel):
    """Normalized provider usage for one Judge model call, including cache accounting."""

    model_call_id: str | None = Field(
        default=None,
        description="Provider or public-runtime call ID; null means a provider error exposed no ID.",
    )
    status: str = Field(min_length=1, description="Completion or failure status of this call attempt.")
    model: str | None = Field(
        default=None, description="Model ID actually reported by the provider; null means it was unobservable."
    )
    input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Normalized total input tokens; null means the provider did not report them.",
    )
    output_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Normalized output tokens; null means the provider did not report them.",
    )
    cache_read_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Normalized input_token_details.cache_read value; null means it was not reported.",
    )
    cache_write_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Provider cache-creation or cache-write tokens; null means they were not reported.",
    )
    cost_counted: bool = Field(
        description="Whether this usage is billable under the established provider-error exemption."
    )
    billing_disposition: str = Field(
        min_length=1,
        description="Billable, provider_error_retry_exempt, or an explicit unobservable status.",
    )
    raw_usage_json: str = Field(
        min_length=1,
        description="Stable JSON for the complete normalized usage row; preserves unknown provider fields without passing a free-form dictionary across stages.",
    )


class RetryRecord(FrozenModel):
    """One outer or transport retry audit row for a Judge call."""

    attempt_no: int = Field(
        ge=1, description="One-based attempt number within this Judge cell."
    )
    status: str = Field(
        min_length=1,
        description="Terminal attempt status such as success, exception, or provider_error.",
    )
    provider_error: bool = Field(
        description="Whether this is a provider-side error; only this retry class may be cost-exempt."
    )
    error_code: str | None = Field(
        default=None, description="Structured error code; null means success or that the provider supplied no code."
    )
    error_message: str | None = Field(
        default=None, description="Auditable error message; null means no error, and the value must never contain a secret."
    )
    billing_disposition: str = Field(
        min_length=1, description="Cost-accounting treatment for this attempt."
    )
    raw_attempt_json: str = Field(
        min_length=1, description="Stable JSON containing complete redacted attempt/retry metadata."
    )


class JudgeCallReceipt(FrozenModel):
    """Persistent receipt for one primary or arbitration structured Judge call."""

    call_id: str = Field(
        min_length=1,
        description="Stable call ID within the pair; it identifies audit files and carries no judgment semantics.",
    )
    phase: Literal["primary_1", "primary_2", "arbitration"] = Field(
        description="Role of the call in the dual-reading arbitration flow."
    )
    status: Literal["success", "failed"] = Field(
        description="Whether the structured call produced a complete validated reading."
    )
    profile: str = Field(
        min_length=1, description="utils.llm profile used by the unified Judge; it must be identical for both arms."
    )
    schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Exact-closure response-schema hash for this pair.",
    )
    prompt_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the actual system and user prompts used for protocol-freeze audit.",
    )
    usage: tuple[UsageReceipt, ...] = Field(
        description="Usage for every success, failure, and retry; provider-error exemptions are preserved per row."
    )
    retries: tuple[RetryRecord, ...] = Field(
        description="Outer or transport retry records; an empty tuple means no retry occurred."
    )
    cost_usd: float = Field(
        ge=0,
        description="Judge cost for this call calculated by the runtime from normalized usage; it is not an optimization target.",
    )
    cost_eligible: bool = Field(
        description="Whether every billable usage row has complete pricing and token data."
    )
    artifact_paths: tuple[str, ...] = Field(
        description="Public-runtime prompt, raw, result, and audit path; used only for review and never sent back to the provider."
    )
    reason: str = Field(min_length=1, description="Why the call succeeded or failed and whether arbitration is required.")
    basis: str = Field(
        min_length=1, description="utils.llm/AgentApp, profile, schema, and retry basis."
    )


class ExpectedOutcome(FrozenModel):
    """Deterministic decoded expected outcome using the original frozen ledger ID."""

    ledger_id: str = Field(
        min_length=1, description="Frozen ledger ID restored outside the provider for formal item-level aggregation."
    )
    hit: bool = Field(description="Whether a final VALID_KNOWN plus FULL_MATCH report exists.")
    supported: bool = Field(description="Whether a final VALID_KNOWN plus FULL or PARTIAL report exists.")
    full_report_ids: tuple[str, ...] = Field(
        description="Original published report IDs that hit this expected issue; duplicates still count the expected issue once."
    )
    partial_report_ids: tuple[str, ...] = Field(
        description="Original published report IDs that only support this expected issue."
    )
    reason: str = Field(
        min_length=1, description="Original semantic explanation from the final expected assessment."
    )
    basis: str = Field(
        min_length=1, description="Artifact and relation basis from the final expected assessment."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="Supplied references from the final expected assessment."
    )


class ReportOutcome(FrozenModel):
    """Deterministic decoded report outcome using the source artifact's original ID."""

    original_report_id: str = Field(
        min_length=1, description="Original report ID restored by provider-external adapter mapping."
    )
    validity: ReportValidity = Field(
        description="Final dimension-B classification; only INVALID counts as a semantic false positive."
    )
    full_ledger_ids: tuple[str, ...] = Field(
        description="Original ledger IDs with final FULL_MATCH."
    )
    partial_ledger_ids: tuple[str, ...] = Field(
        description="Original ledger IDs with final PARTIAL_MATCH."
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="Final root-cause cluster key used for cluster metrics and redundancy.",
    )
    reason: str = Field(min_length=1, description="Reason from the final report-validity judgment.")
    basis: str = Field(
        min_length=1, description="Artifact basis from the final report-validity judgment."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="Supplied references from the final report-validity judgment."
    )


class SemanticMetrics(FrozenModel):
    """Issue #195 deterministic pair/run metrics; no LLM may self-report these values."""

    schema_version: Literal["paper1.semantic-judge.metrics.v1"] = Field(
        default="paper1.semantic-judge.metrics.v1",
        description="Deterministic metric-calculator schema version.",
    )
    expected_count: int = Field(ge=0, description="Frozen D2+D1 expected denominator.")
    full_hit_count: int = Field(
        ge=0, description="Number of unique expected issues hit by VALID_KNOWN plus FULL."
    )
    fn_count: int = Field(ge=0, description="expected_count - full_hit_count.")
    supported_count: int = Field(
        ge=0, description="Number of unique expected issues covered by a valid FULL or PARTIAL report."
    )
    hit_rate: float = Field(ge=0, le=1, description="full_hit_count / expected_count.")
    supported_rate: float = Field(
        ge=0, le=1, description="supported_count / expected_count."
    )
    report_count: int = Field(
        ge=0, description="Number of all final adjudicated published reports; no final UNKNOWN exists."
    )
    valid_known_count: int = Field(ge=0, description="Number of raw VALID_KNOWN reports.")
    valid_novel_count: int = Field(
        ge=0, description="Number of raw VALID_NOVEL reports; they count as neither hits nor false positives."
    )
    invalid_count: int = Field(
        ge=0, description="Number of raw INVALID reports, which are the only semantic false positives."
    )
    semantic_precision: float = Field(
        ge=0, le=1, description="(VALID_KNOWN+VALID_NOVEL)/report_count."
    )
    ledger_unmatched_count: int = Field(
        ge=0,
        description="PARTIAL-only known reports plus novel and invalid reports; this is a legacy diagnostic and must not be named false positive.",
    )
    cluster_count: int = Field(
        ge=0, description="Number of all clusters after deduplication by final actionable root-cause key."
    )
    valid_cluster_count: int = Field(
        ge=0, description="Number of valid known or novel root-cause clusters."
    )
    invalid_cluster_count: int = Field(
        ge=0, description="Number of invalid root-cause clusters."
    )
    root_cause_cluster_precision: float = Field(
        ge=0, le=1, description="valid_cluster_count / cluster_count."
    )
    redundancy_rate: float = Field(
        ge=0,
        le=1,
        description="(report_count-cluster_count)/report_count; duplicate valid reports are not false positives.",
    )
    valid_redundancy_rate: float = Field(
        ge=0, le=1, description="Cluster redundancy rate restricted to valid reports."
    )
    reason: str = Field(
        min_length=1,
        description="Deterministic calculator explanation of hit, support, false positive, precision, and clustering.",
    )
    basis: str = Field(
        min_length=1, description="Issue #195 formulas and the final exact-closure reading."
    )


class JudgeScaleAudit(FrozenModel):
    """Provider-free proof that one real Judge payload fits configured model limits.

    The audit is built from the same arm-neutral input, prompt serializer, dynamic
    response schema, and output validators used by live judging. Character-based
    token estimates are deliberately conservative and are labeled as estimates;
    this record proves structural feasibility without calling or weakening the
    Judge model.
    """

    schema_version: Literal["semantic-judge.scale-audit.v2"] = Field(
        default="semantic-judge.scale-audit.v2",
        description="Provider-free Judge scale-audit version with a source-length-derived material-assertion envelope.",
    )
    generated_at_utc: datetime = Field(
        description="UTC time when this deterministic scale audit was materialized."
    )
    pair_id: str = Field(
        pattern=r"^\d{4}$", description="Pair whose real unified Judge input was measured."
    )
    round: int = Field(
        ge=1, description="Round of the existing published reports used by the audit."
    )
    source_format: Literal["x1v2_record", "evidence_discovery_release"] = Field(
        description="Provider-external source adapter used to construct the anonymous reports."
    )
    source_path: str = Field(
        min_length=1, description="Path to the existing published-report artifact measured by this audit."
    )
    source_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Byte hash of the published-report source artifact."
    )
    protocol_version: str = Field(
        min_length=1, description="Frozen issue #195 protocol version used by the measured Judge."
    )
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="SHA-256 of the frozen issue #195 snapshot."
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="Judge runner and sparse-closure algorithm version."
    )
    algorithm_source_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the exact adapter, CLI, metrics, model, protocol, runner, schema, scale-audit, and shared structured-runtime source bytes used for this audit.",
    )
    prompt_version: str = Field(
        min_length=1, description="Version of the English arm-neutral Judge prompt measured by this audit."
    )
    prompt_template_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of all frozen semantic prompt templates."
    )
    model_profile: str = Field(
        min_length=1, description="Public LLM profile whose configured limits are checked."
    )
    model_id: str = Field(
        min_length=1, description="Provider model identifier resolved from the public profile."
    )
    profile_fingerprint: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Secret-free fingerprint of the resolved public model profile."
    )
    context_window_tokens: int = Field(
        gt=0, description="Configured model context-window limit in tokens."
    )
    profile_max_output_tokens: int = Field(
        gt=0, description="Configured profile output limit in tokens."
    )
    judge_max_output_tokens: int = Field(
        gt=0, description="Frozen Judge-specific output cap in tokens."
    )
    effective_max_output_tokens: int = Field(
        gt=0, description="Minimum of profile_max_output_tokens and judge_max_output_tokens."
    )
    report_count: int = Field(
        ge=0, description="Number of real anonymous published reports in the measured input."
    )
    expected_count: int = Field(
        ge=0, description="Number of frozen expected issues in the measured input."
    )
    relation_position_count: int = Field(
        ge=0, description="Complete report-by-expected relation position count before sparse encoding."
    )
    report_causal_text_chars: int = Field(
        ge=0, description="Total characters in non-null report reason, basis, and observed fields."
    )
    maximum_report_causal_text_chars: int = Field(
        ge=0, description="Largest per-report total across reason, basis, and observed fields."
    )
    material_assertion_chars_per_row: int = Field(
        gt=0,
        description="Conservative maximum source-field characters represented by one synthetic assertion row in both validated output envelopes.",
    )
    material_assertion_envelope_count: int = Field(
        ge=0,
        description="Total synthetic assertion rows reserved from real causal-field lengths across the validated output envelopes.",
    )
    maximum_field_material_assertion_envelope_count: int = Field(
        ge=0,
        description="Largest synthetic assertion-row count reserved for any one real report field.",
    )
    serialized_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Stable hash of the exact anonymous unified Judge input."
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the common pair artifact closure in the measured input."
    )
    system_prompt_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the exact system prompt text measured by this audit."
    )
    primary_prompt_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the exact serialized primary user prompt."
    )
    response_schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of the actual dynamic exact-closure provider schema."
    )
    system_prompt_chars: int = Field(
        ge=0, description="Character count of the exact system prompt."
    )
    system_prompt_estimated_tokens: int = Field(
        ge=0, description="Conservative four-characters-per-token estimate for the system prompt."
    )
    primary_prompt_chars: int = Field(
        ge=0, description="Character count of the exact serialized primary user prompt."
    )
    primary_prompt_estimated_tokens: int = Field(
        ge=0, description="Conservative four-characters-per-token estimate for the primary user prompt."
    )
    response_schema_chars: int = Field(
        ge=0, description="Character count of the stable serialized dynamic response schema."
    )
    response_schema_estimated_tokens: int = Field(
        ge=0, description="Conservative four-characters-per-token estimate for the response schema."
    )
    request_estimated_tokens: int = Field(
        ge=0, description="Combined estimated tokens for system prompt, primary prompt, and response schema."
    )
    all_no_response_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of a validated all-NO sparse structural response for this exact input."
    )
    all_no_response_chars: int = Field(
        ge=0, description="Pretty-serialized character count of the validated all-NO structural response."
    )
    all_no_response_estimated_tokens: int = Field(
        ge=0, description="Conservative token estimate for the validated all-NO structural response."
    )
    all_positive_response_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Hash of a validated response with every relation position represented as FULL."
    )
    all_positive_response_chars: int = Field(
        ge=0, description="Pretty-serialized character count of the all-positive structural envelope."
    )
    all_positive_response_estimated_tokens: int = Field(
        ge=0, description="Conservative token estimate for the all-positive structural envelope."
    )
    reserved_context_tokens: int = Field(
        ge=0, description="Request estimate plus the complete effective Judge output allowance."
    )
    context_headroom_tokens: int = Field(
        description="Configured context window minus reserved_context_tokens; a negative value records failure."
    )
    all_no_fits_output_limit: bool = Field(
        description="Whether the validated all-NO structural response fits the effective output limit."
    )
    all_positive_fits_output_limit: bool = Field(
        description="Whether the validated all-positive structural envelope fits the effective output limit."
    )
    reserved_context_fits_window: bool = Field(
        description="Whether the full output allowance remains available after the measured request estimate."
    )
    status: Literal["pass", "fail"] = Field(
        description="Deterministic conjunction of output-shape and reserved-context checks."
    )
    reason: str = Field(
        min_length=1, description="English explanation of the structural scale verdict and retained Judge guarantees."
    )
    basis: str = Field(
        min_length=1, description="Exact source, input, prompt, schema, profile, and validated-shape basis."
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1, description="Paths and stable hashes needed to reproduce this provider-free audit."
    )

    @model_validator(mode="after")
    def deterministic_scale_verdict(self) -> JudgeScaleAudit:
        expected_effective_limit = min(
            self.profile_max_output_tokens, self.judge_max_output_tokens
        )
        if self.effective_max_output_tokens != expected_effective_limit:
            raise ValueError(
                "effective_max_output_tokens must equal the smaller profile and Judge cap"
            )
        expected_relation_positions = self.report_count * self.expected_count
        if self.relation_position_count != expected_relation_positions:
            raise ValueError(
                "relation_position_count must equal report_count * expected_count"
            )
        expected_request = (
            self.system_prompt_estimated_tokens
            + self.primary_prompt_estimated_tokens
            + self.response_schema_estimated_tokens
        )
        if self.request_estimated_tokens != expected_request:
            raise ValueError(
                "request_estimated_tokens must equal the three measured request components"
            )
        expected_reserved = expected_request + expected_effective_limit
        if self.reserved_context_tokens != expected_reserved:
            raise ValueError(
                "reserved_context_tokens must equal request estimate plus effective output limit"
            )
        expected_headroom = self.context_window_tokens - expected_reserved
        if self.context_headroom_tokens != expected_headroom:
            raise ValueError(
                "context_headroom_tokens must equal context window minus reserved tokens"
            )
        expected_flags = (
            self.all_no_response_estimated_tokens <= expected_effective_limit,
            self.all_positive_response_estimated_tokens <= expected_effective_limit,
            expected_headroom >= 0,
        )
        actual_flags = (
            self.all_no_fits_output_limit,
            self.all_positive_fits_output_limit,
            self.reserved_context_fits_window,
        )
        if actual_flags != expected_flags:
            raise ValueError(
                f"scale fit flags must be deterministic; expected={expected_flags}, actual={actual_flags}"
            )
        expected_status = "pass" if all(expected_flags) else "fail"
        if self.status != expected_status:
            raise ValueError(
                f"status must equal deterministic scale verdict {expected_status}; actual={self.status}"
            )
        return self


class AdapterIdMap(FrozenModel):
    """Provider-external reversible mapping between anonymous and source IDs."""

    anonymous_id: str = Field(min_length=1, description="Anonymous R/E ID sent to the provider.")
    original_id: str = Field(
        min_length=1,
        description="Original artifact or frozen ledger ID; it never enters the provider payload.",
    )


class AdapterAudit(FrozenModel):
    """Evidence that source-specific adaptation ended before the shared Judge path."""

    schema_version: Literal["paper1.semantic-judge.adapter-audit.v1"] = Field(
        default="paper1.semantic-judge.adapter-audit.v1",
        description="Provider-external adapter-audit schema.",
    )
    source_format: Literal["x1v2_record", "evidence_discovery_release"] = Field(
        description="Written only to local audit; this field and arm identity never enter UnifiedJudgeInput.",
    )
    source_path: str = Field(
        min_length=1, description="Path to the original result being rejudged; used for provenance and never sent to the Judge."
    )
    source_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Byte hash of the original result."
    )
    report_id_map: tuple[AdapterIdMap, ...] = Field(
        description="Exact mapping from anonymous report IDs to original release IDs."
    )
    expected_id_map: tuple[AdapterIdMap, ...] = Field(
        description="Exact mapping from anonymous expected IDs to ledger IDs."
    )
    projected_field_names: tuple[str, ...] = Field(
        description="Field names of the CandidateReport schema shared by both arms, used for field-level fairness diff."
    )
    excluded_field_names: tuple[str, ...] = Field(
        description="Audit of explicitly excluded arm, W, D, L, predicate, and history fields."
    )
    reason: str = Field(
        min_length=1, description="How the adapter projects only semantics actually owned by the original report."
    )
    basis: str = Field(
        min_length=1, description="Source artifact, adapter version, and anonymization-rule basis."
    )


class PairJudgeResult(FrozenModel):
    """Self-contained pair result with two readings, arbitration, metrics, and audit."""

    schema_version: Literal["paper1.semantic-judge.pair-result.v3"] = Field(
        default="paper1.semantic-judge.pair-result.v3",
        description="Unified pair-Judge persistence version containing backend-hashed causal fields and assertion-derived audit verdicts.",
    )
    run_id: str = Field(
        min_length=1, description="Judge run ID; never reuse it across different protocol, code, or input versions."
    )
    pair_id: str = Field(pattern=r"^\d{4}$", description="Pair being rejudged.")
    round: int = Field(ge=1, description="Experiment round of the original published reports; it does not affect semantic judgment.")
    protocol_version: str = Field(
        min_length=1, description="Frozen issue #195 protocol version."
    )
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="SHA-256 of the original issue #195 snapshot bytes."
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="Unified runner, arbitration, and persistence algorithm version."
    )
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Git commit that actually executed the Judge."
    )
    model_profile: str = Field(
        min_length=1, description="gpt-5.6-luna profile shared by both independent readings and arbitration."
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Common artifact hash that must be identical for both arms on the same pair.",
    )
    serialized_input_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Stable JSON hash of the anonymous unified Judge input.",
    )
    response_schema_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Dynamic exact-closure schema hash for this pair.",
    )
    prompt_template_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the frozen system, primary, and arbitration prompt templates.",
    )
    adapter_audit: AdapterAudit = Field(
        description="Provider-external evidence of source adaptation and anonymous mapping."
    )
    primary_reading_1: JudgeReading = Field(description="First complete independent reading.")
    primary_reading_2: JudgeReading = Field(description="Second complete independent reading.")
    arbitration_reading: JudgeReading | None = Field(
        default=None,
        description="Backend-merged complete reading after targeted report replacements when relation, core-truth, or cluster conflicts exist; null when there is no conflict."
    )
    conflicts: tuple[ConflictRecord, ...] = Field(
        description="All substantive conflicts between the two primary readings and the final choice; wording differences are not conflicts."
    )
    final_reading: JudgeReading = Field(
        description="Final authoritative reading with no UNKNOWN; when conflicts exist it must come from arbitration."
    )
    report_outcomes: tuple[ReportOutcome, ...] = Field(
        description="Provider-external decoded K/N/I, relation, and clustering audit for every original report."
    )
    expected_outcomes: tuple[ExpectedOutcome, ...] = Field(
        description="Provider-external decoded hit/support audit for every ledger item."
    )
    metrics: SemanticMetrics = Field(
        description="Pair metrics deterministically recomputed from the final reading."
    )
    call_receipts: tuple[JudgeCallReceipt, ...] = Field(
        description="Complete usage, cost, and retry receipts for both primary readings and optional arbitration."
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="Completed only after both readings, required arbitration, and exact accounting are complete.",
    )
    reason: str = Field(
        min_length=1, description="Summary of pair completeness, conflict handling, and final classifications."
    )
    basis: str = Field(
        min_length=1,
        description="Protocol, input/schema/prompt hashes, public runtime, and deterministic-metrics basis.",
    )


class RunPairReceipt(FrozenModel):
    """One pair/round location and terminal status in a semantic Judge run."""

    pair_id: str = Field(pattern=r"^\d{4}$", description="Frozen pair ID.")
    round: int = Field(ge=1, description="Original publication round.")
    result_path: str = Field(
        min_length=1, description="Path to the complete PairJudgeResult JSON."
    )
    result_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="PairJudgeResult byte hash."
    )
    artifact_closure_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Common artifact-closure hash for this pair."
    )
    report_count: int = Field(ge=0, description="Number of published reports assessed.")
    expected_count: int = Field(ge=0, description="Size of the frozen expected denominator.")
    status: Literal["completed"] = Field(
        default="completed", description="Terminal status with no crash, omission, or UNKNOWN."
    )


class RunPairFailure(FrozenModel):
    """Typed terminal diagnostic for a pair without a complete Judge result.

    The CLI emits this after preserving all available input, adapter, and public
    runtime artifacts. It is never eligible for aggregation and never substitutes
    for a completed PairJudgeResult.
    """

    schema_version: Literal["semantic-judge.pair-failure.v2"] = Field(
        default="semantic-judge.pair-failure.v2",
        description="Failure-diagnostic version retaining complete call accounting; it is not a semantic result and cannot enter metrics."
    )
    pair_id: str = Field(pattern=r"^\d{4}$", description="Frozen pair ID that failed.")
    round: int = Field(ge=1, description="Original round of the reports in the failed cell.")
    source_path: str = Field(
        min_length=1, description="Path to the original published reports actually read by this cell."
    )
    input_path: str | None = Field(
        default=None,
        description="Path to the unified input when it was persisted successfully; null means failure occurred before input construction.",
    )
    adapter_audit_path: str | None = Field(
        default=None,
        description="Path to the adapter audit when it was persisted successfully; null means failure occurred before adaptation.",
    )
    llm_artifact_path: str = Field(
        min_length=1,
        description="Public-runtime audit root for this pair, used to recover usage and retry evidence after provider or schema failure.",
    )
    error_type: str = Field(
        min_length=1,
        description="Terminal exception class name used to distinguish provider, schema, and local bugs.",
    )
    error_message: str = Field(
        min_length=1, description="Localizable terminal error message; it must preserve the schema or runtime cause."
    )
    call_receipts: tuple[JudgeCallReceipt, ...] = Field(
        description="Every primary or arbitration call completed or failed before the terminal cell error, including normalized usage, cache, retry, and cost."
    )
    total_judge_cost_usd: float = Field(
        ge=0,
        description="Sum of all observable billable Judge call costs before failure; failure never converts incurred cost to null or zero."
    )
    cost_eligible: bool = Field(
        description="Whether every call before failure had complete pricing and usage; false preserves partial observable cost rather than erasing it."
    )
    status: Literal["failed"] = Field(
        default="failed", description="This cell produced no complete Judge result and is ineligible for aggregation."
    )
    reason: str = Field(
        min_length=1, description="Why this cell cannot be treated as completed or used in paper metrics."
    )
    basis: str = Field(
        min_length=1,
        description="Persistence basis covering input, adapter, runtime audit, and captured exception.",
    )


class RunManifest(FrozenModel):
    """Frozen provenance and input contract for one unified semantic Judge run."""

    schema_version: Literal["paper1.semantic-judge.run-manifest.v1"] = Field(
        default="paper1.semantic-judge.run-manifest.v1",
        description="Unified Judge run-manifest version.",
    )
    run_id: str = Field(min_length=1, description="Non-reusable Judge run ID.")
    source_format: Literal["x1v2_record", "evidence_discovery_release"] = Field(
        description="Local source-adapter type; it never enters the provider payload."
    )
    source_root: str = Field(
        min_length=1, description="Root of existing original published results; the Judge does not regenerate issues."
    )
    source_root_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$",
        description="Hash of the source-file list and bytes actually selected for this run.",
    )
    report_root: str = Field(
        min_length=1, description="Root of the common representation reports for all 54 pairs."
    )
    ledger_path: str = Field(min_length=1, description="Path to the frozen 145-item ledger source of truth.")
    ledger_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Byte hash of the complete frozen ledger."
    )
    protocol_version: str = Field(
        min_length=1, description="Frozen issue #195 protocol version."
    )
    protocol_sha256: str = Field(
        pattern=r"^[0-9a-f]{64}$", description="SHA-256 hash of the issue #195 snapshot bytes."
    )
    judge_algorithm_version: str = Field(
        min_length=1, description="Unified Judge runner version."
    )
    judge_code_commit: str = Field(
        pattern=r"^[0-9a-f]{40}$", description="Clean tracked git commit when the run started."
    )
    model_profile: str = Field(
        min_length=1, description="Single profile shared by every Judge reading and arbitration call."
    )
    selected_pair_ids: tuple[str, ...] = Field(
        min_length=1, description="Pair selection frozen before the run."
    )
    selected_rounds: tuple[int, ...] = Field(
        min_length=1, description="Round selection frozen before the run."
    )
    workers: int = Field(
        ge=1, description="Number of pair-level parallel workers; it does not change single-pair Judge semantics."
    )
    transport_retries: int = Field(
        ge=0, description="In-place retry limit for provider errors; it must be identical for both arms."
    )
    reason: str = Field(
        min_length=1,
        description="Local provenance stating whether this is a baseline or current-method rejudge; it is never sent to the provider.",
    )
    basis: str = Field(
        min_length=1,
        description="CLI selection, source hash, and protocol, code, and model versions.",
    )


class RunSummary(FrozenModel):
    """Deterministically aggregatable semantic Judge run summary and completeness proof."""

    schema_version: Literal["paper1.semantic-judge.run-summary.v1"] = Field(
        default="paper1.semantic-judge.run-summary.v1",
        description="Unified Judge summary schema version.",
    )
    run_id: str = Field(min_length=1, description="Corresponding RunManifest.run_id.")
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Byte hash of the frozen RunManifest."
    )
    pair_receipts: tuple[RunPairReceipt, ...] = Field(
        description="Result closure containing every selected pair-by-round cell exactly once."
    )
    overall: SemanticMetrics = Field(
        description="Metrics aggregated over raw reports and expected positions from all cells."
    )
    l2_expected_count: int = Field(
        ge=0,
        description="L2 expected positions used only for ledger-side grouping; L never enters the provider.",
    )
    l2_full_hit_count: int = Field(
        ge=0, description="Final FULL-hit L2 expected positions."
    )
    l2_hit_rate: float = Field(
        ge=0, le=1, description="l2_full_hit_count / l2_expected_count."
    )
    total_judge_cost_usd: float = Field(
        ge=0, description="Complete cost of all primary and arbitration Judge calls; it is not optimized."
    )
    cost_eligible: bool = Field(
        description="Whether every call receipt can be priced from normalized usage."
    )
    status: Literal["completed"] = Field(
        default="completed",
        description="Completed only when every selected cell is complete with no UNKNOWN, missing report, or missing ledger item.",
    )
    reason: str = Field(
        min_length=1, description="Run-completeness and principal hit, support, K/N/I, and precision conclusions."
    )
    basis: str = Field(
        min_length=1,
        description="Deterministic recomputation from every PairJudgeResult and the issue #195 formulas.",
    )


class RunFailureSummary(FrozenModel):
    """Incomplete-run receipt that prevents partial pair results becoming a score."""

    schema_version: Literal["semantic-judge.run-failure.v2"] = Field(
        default="semantic-judge.run-failure.v2",
        description="Terminal incomplete-run version with complete successful and failed call accounting, physically separated from completed metrics."
    )
    run_id: str = Field(min_length=1, description="Non-reusable ID of the corresponding failed Judge run.")
    manifest_hash: str = Field(
        pattern=r"^sha256:[0-9a-f]{64}$", description="Byte hash of the frozen RunManifest."
    )
    completed_pair_receipts: tuple[RunPairReceipt, ...] = Field(
        description="Pairs completed before or during concurrent failure; retained only for audit and never spliced into a summary."
    )
    failures: tuple[RunPairFailure, ...] = Field(
        min_length=1,
        description="Typed terminal diagnostic for every incomplete pair; at least one is required.",
    )
    total_judge_cost_usd: float = Field(
        ge=0,
        description="Observable cost of every completed and failed Judge call in this incomplete run; no semantic score is derived from it."
    )
    cost_eligible: bool = Field(
        description="Whether all call receipts in the incomplete run have complete pricing and usage information."
    )
    status: Literal["failed"] = Field(
        default="failed", description="Not every selected cell completed, so no formal metrics exist."
    )
    reason: str = Field(
        min_length=1, description="Direct reason the run produced no completed summary."
    )
    basis: str = Field(
        min_length=1,
        description="Manifest, successful receipts, failure artifacts, and the no-partial-summary rule.",
    )
