"""Pydantic protocols for the arm-neutral issue #195 semantic Judge."""

from __future__ import annotations

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


class ReportValidity(str, Enum):
    """Issue #195 dimension B: report truth and known/novel ownership."""

    VALID_KNOWN = "VALID_KNOWN"
    VALID_NOVEL = "VALID_NOVEL"
    INVALID = "INVALID"


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
        description="Core defect summary from the frozen ledger; this is part of the expected issue's semantic identity.",
    )
    detail: str = Field(
        min_length=1,
        description="Complete frozen-ledger defect mechanism, locus, consequence, and boundary used for academically broad FULL/PARTIAL assessment.",
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
    """One required dimension-A decision for an exact report/expected pair."""

    report_id: str = Field(
        min_length=1, description="Anonymous report ID being compared; it must come from the exact input closure."
    )
    expected_id: str = Field(
        min_length=1,
        description="Anonymous expected ID being compared; it must come from the exact input closure.",
    )
    match: MatchStrength = Field(
        description="Issue #195 dimension A, separate from report validity; PARTIAL is neither a hit nor a false positive."
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


class ReportJudgment(FrozenModel):
    """LLM-authored dimension-B and root-cause judgment without derived ID sets."""

    report_id: str = Field(
        min_length=1, description="Anonymous ID of the assessed report; it must occur exactly once in the response."
    )
    validity: ReportValidity = Field(
        description="Issue #195 dimension B; only INVALID is a semantic false positive."
    )
    root_cause_cluster_key: str = Field(
        min_length=1,
        description="Stable phrase key based on an actionable technical root cause; never use report ID/order or merge nearby claims with different properties or sources.",
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


class ExpectedJudgment(FrozenModel):
    """LLM-authored expected-side semantic explanation without derived coverage fields."""

    expected_id: str = Field(
        min_length=1,
        description="Anonymous ID of the explained expected issue; it must occur exactly once in the response.",
    )
    reason: str = Field(
        min_length=1,
        description="Semantic summary of this expected issue's relations to all reports; the backend derives hit and support deterministically from the matrix.",
    )
    basis: str = Field(
        min_length=1,
        description="Per-relation, validity, and common-artifact basis; do not self-report metric values.",
    )
    source_refs: tuple[str, ...] = Field(
        min_length=1,
        description="Expected, report, and artifact references actually used by this expected judgment.",
    )


class JudgeResponse(FrozenModel):
    """LLM response containing only semantic judgments, never deterministic summaries."""

    schema_version: Literal["paper1.semantic-judge.response.v2"] = Field(
        default="paper1.semantic-judge.response.v2",
        description="Provider structured-output schema version; from v2 onward, only the backend generates derived sets, hit, and support.",
    )
    relations: tuple[RelationAssessment, ...] = Field(
        description="Complete report-by-expected matrix including every NO_MATCH; it must not be sparse."
    )
    report_judgments: tuple[ReportJudgment, ...] = Field(
        description="Validity, root cause, reason, and basis for every report exactly once."
    )
    expected_judgments: tuple[ExpectedJudgment, ...] = Field(
        description="Semantic reason and basis for every expected issue exactly once; do not repeat derivable sets."
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
    validity: ReportValidity = Field(
        description="Issue #195 dimension B; only INVALID is a semantic false positive."
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

    schema_version: Literal["paper1.semantic-judge.reading.v1"] = Field(
        default="paper1.semantic-judge.reading.v1",
        description="Complete-reading schema version; it does not encode primary or arbitration role.",
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


class ConflictKind(str, Enum):
    """Deterministically detectable disagreements requiring semantic arbitration."""

    RELATION = "relation"
    VALIDITY = "validity"
    ROOT_CAUSE_CLUSTER = "root_cause_cluster"


class ConflictRecord(FrozenModel):
    """Audit trail for one primary-reading disagreement and arbitrated outcome."""

    kind: ConflictKind = Field(
        description="Whether the conflict concerns relation, validity, or root-cause clustering."
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
        description="Relation, validity, or root-cause-clustering conflict type requiring arbitration."
    )
    object_ref: str = Field(
        min_length=1,
        description="Anonymous report/expected object reference for the conflict; it does not expose a source-arm ID.",
    )
    reading_1_value: str = Field(min_length=1, description="Structured value from the first independent reading.")
    reading_2_value: str = Field(min_length=1, description="Structured value from the second independent reading.")


class ArbitrationInput(FrozenModel):
    """Complete typed arbitration input containing no arm or method-only metadata."""

    schema_version: Literal["paper1.semantic-judge.arbitration-input.v1"] = Field(
        default="paper1.semantic-judge.arbitration-input.v1",
        description="Unified arbitration-input version; built only when the two independent readings have a substantive conflict.",
    )
    judge_input: UnifiedJudgeInput = Field(
        description="Anonymous reports, expected issues, and common artifact closure identical to the primary input."
    )
    primary_reading_1: JudgeReading = Field(
        description="First complete independent reading with its reason, basis, and source references."
    )
    primary_reading_2: JudgeReading = Field(
        description="Second complete independent reading with its reason, basis, and source references."
    )
    disagreements: tuple[ReadingDisagreement, ...] = Field(
        min_length=1,
        description="All substantive conflicts found by deterministic comparison of relation enums, validity, and clusters; wording differences are excluded.",
    )
    reason: str = Field(
        min_length=1, description="Why complete artifacts must be reviewed again instead of voting or retaining UNKNOWN."
    )
    basis: str = Field(
        min_length=1, description="Issue #195 dual-reading arbitration contract and exact conflict detection."
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
    fn_count: int = Field(ge=0, description="expected_count - full_hit_count。")
    supported_count: int = Field(
        ge=0, description="Number of unique expected issues covered by a valid FULL or PARTIAL report."
    )
    hit_rate: float = Field(ge=0, le=1, description="full_hit_count / expected_count。")
    supported_rate: float = Field(
        ge=0, le=1, description="supported_count / expected_count。"
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
        ge=0, le=1, description="(VALID_KNOWN+VALID_NOVEL)/report_count。"
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
        ge=0, le=1, description="valid_cluster_count / cluster_count。"
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

    schema_version: Literal["paper1.semantic-judge.pair-result.v1"] = Field(
        default="paper1.semantic-judge.pair-result.v1",
        description="Unified pair-Judge persistence protocol version.",
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
        description="Complete arbitration reading when relation, validity, or cluster conflicts exist; null when there is no conflict.",
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
        pattern=r"^sha256:[0-9a-f]{64}$", description="PairJudgeResult bytes hash。"
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

    schema_version: Literal["paper1.semantic-judge.pair-failure.v1"] = Field(
        default="paper1.semantic-judge.pair-failure.v1",
        description="Failure-diagnostic persistence version; this is not a semantic Judge result and cannot enter metrics.",
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
        description="CLI selection、source hash、protocol/code/model version。",
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
        ge=0, description="final FULL-hit L2 expected positions。"
    )
    l2_hit_rate: float = Field(
        ge=0, le=1, description="l2_full_hit_count/l2_expected_count。"
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

    schema_version: Literal["paper1.semantic-judge.run-failure.v1"] = Field(
        default="paper1.semantic-judge.run-failure.v1",
        description="Terminal schema version for an incomplete run, physically separated from completed RunSummary.",
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
