from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Literal, TypedDict

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    field_validator,
    model_validator,
)

from .predicates import PREDICATE_BY_NAME, PREDICATE_NAMES, verification_kind_of

SCHEMA_VERSION = "v2"


class StrictBaseModel(BaseModel):
    # JSON arrays are the wire representation of immutable tuple fields. Keep
    # extra-field rejection/frozen outputs while using StrictBool explicitly at
    # the truth-bearing method boundaries.
    model_config = ConfigDict(extra="forbid", frozen=True)


VerificationKind = Literal["structure", "behavior", "property"]
EvidenceFamily = Literal[
    "structure",
    "relation",
    "effect",
    "simulation",
    "fbmcq",
    "topology",
    "provenance",
]
AssertionRole = Literal["primary", "supporting"]


class CoverageObligation(StrictBaseModel):
    domain: str = Field(default="requirement", min_length=1)
    partition_by: str | None = None
    aggregation: Literal["all", "any", "exactly_one", "custom"] = "all"
    custom_policy_id: str | None = None
    limitations: tuple[str, ...] = Field(default_factory=tuple)

    @model_validator(mode="after")
    def _custom_policy_is_named(self) -> "CoverageObligation":
        if self.aggregation == "custom" and not self.custom_policy_id:
            raise ValueError("custom coverage aggregation requires custom_policy_id")
        if self.aggregation != "custom" and self.custom_policy_id is not None:
            raise ValueError("custom_policy_id is only valid for custom aggregation")
        return self


class NodeName(str, Enum):
    PREPARE = "prepare"
    SPLIT_REQUIREMENTS = "split_requirements"
    REVIEW_REQUIREMENTS = "review_requirements"
    CONVERT_ASSERTIONS = "convert_assertions"
    PRECHECK_AND_SEAL = "precheck_and_seal"
    REVIEW_ASSERTIONS = "review_assertions"
    RELEASE_RESULTS = "release_results"
    BIND_ATTRIBUTION = "bind_attribution"
    ADJUDICATE_RESULTS = "adjudicate_results"
    PUBLISH = "publish"


class RevisionFeedback(StrictBaseModel):
    target: Literal["requirements", "assertions"]
    reason: str = Field(min_length=1)
    findings: tuple[str, ...] = Field(default_factory=tuple)
    target_item_ids: tuple[str, ...] = Field(default_factory=tuple)
    recovery_seed: dict[str, Any] | None = None
    origin: Literal[
        "requirement_review",
        "assertion_contract",
        "assertion_precheck",
        "assertion_review",
    ] = "assertion_review"


class RevisionLedgerEvent(StrictBaseModel):
    """Append-only public history for one producer/reviewer revision loop."""

    sequence: int = Field(ge=1)
    loop: Literal["requirements", "assertions"]
    event: Literal[
        "artifact_created",
        "artifact_rejected",
        "artifact_quarantined",
        "check_completed",
        "review_completed",
    ]
    revision: int = Field(ge=1)
    artifact_hash: str | None = None
    status: str = Field(min_length=1)
    artifact_delta: dict[str, Any] = Field(default_factory=dict)
    rationale: str | None = None
    findings: tuple[str, ...] = Field(default_factory=tuple)
    item_ids: tuple[str, ...] = Field(default_factory=tuple)
    budget_counters: dict[str, int] = Field(default_factory=dict)


class DiscoverInput(StrictBaseModel):
    schema_name: Literal["DiscoverInput"] = "DiscoverInput"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str = Field(min_length=1)
    natural_language: str = Field(min_length=1)
    stm_text: str = Field(min_length=1)
    manifest: dict[str, Any] = Field(default_factory=dict)
    source_trace: dict[str, Any] = Field(default_factory=dict)
    profile: str = Field(default="fake", min_length=1)
    language: Literal["zh-CN", "en-US"] = "zh-CN"


class DiscoverRunIdentity(StrictBaseModel):
    run_id: str = Field(min_length=1)
    profile: str = Field(min_length=1)
    language: Literal["zh-CN", "en-US"]
    created_at: datetime


class FrozenDiscoverInputs(StrictBaseModel):
    schema_name: Literal["FrozenDiscoverInputs"] = "FrozenDiscoverInputs"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str = Field(min_length=1)
    natural_language: str = Field(min_length=1)
    stm_text: str = Field(min_length=1)
    nl_segments: dict[str, str] = Field(default_factory=dict)
    inspect_digest: dict[str, Any] = Field(default_factory=dict)
    source_trace: dict[str, Any] = Field(default_factory=dict)
    working_contract: dict[str, Any] = Field(default_factory=dict)
    input_hashes: dict[str, str]
    tool_env_hash: str = Field(min_length=1)
    profile: str = Field(min_length=1)
    language: Literal["zh-CN", "en-US"]
    # Deterministic pair-level verdict on whether bounded formal checking can
    # run at all on this model (see assertions.fbmcq.probe_fbmcq_feasibility).
    # Empty means "not probed"; the controller then keeps the strict contract.
    fbmcq_canary: dict[str, Any] = Field(default_factory=dict)
    resource_options: dict[str, Any] = Field(default_factory=dict)
    # Every state and event path the frozen model declares, so a relation query
    # over a non-existent element can be rejected instead of silently passing.
    known_model_paths: tuple[str, ...] = Field(default_factory=tuple)
    #: Declared paths grouped by kind, handed to the producers so they can bind a
    #: predicate to exact model terms instead of guessing them from the raw DSL.
    #: A guessed event name makes an assertion vacuously true, which is how pair
    #: 0029 lost a real defect to a one-character typo.
    model_vocabulary: dict[str, tuple[str, ...]] = Field(default_factory=dict)


class Requirement(StrictBaseModel):
    requirement_id: str = Field(pattern=r"^REQ-[A-Za-z0-9_.-]+$", min_length=5)
    statement: str = Field(min_length=1)
    rationale: str = Field(default="")
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    # Lightweight, input-derived scope ledger.  It may record explicit or
    # carefully qualified inferred source context, but never evaluator gold.
    source_context: dict[str, Any] = Field(default_factory=dict)
    # The named claim shape, from the closed vocabulary in ``discover.predicates``.
    # When present it *derives* verification_kind: the family, and therefore the
    # mandatory evidence, is a table lookup rather than a per-sentence judgement.
    # That judgement is exactly what two models used to answer differently for
    # the same requirement.  Optional so v1/v2 fixtures stay readable.
    predicate: str | None = None
    #: Concrete arguments for the predicate, e.g. {"source": ..., "trigger": ...}.
    #: They give the converter the terms to bind and let a later gate check that
    #: the assertion tests this claim rather than an easier neighbouring one.
    predicate_bindings: dict[str, str] = Field(default_factory=dict)
    verification_kind: VerificationKind
    quantifier: str = Field(default="unspecified", min_length=1)
    trigger: str | None = None
    expected_outcome: str | None = None
    timing: str | None = None
    coverage_obligation: CoverageObligation = Field(default_factory=CoverageObligation)
    limitations: tuple[str, ...] = Field(default_factory=tuple)
    # Read-only compatibility for v1 fixtures and historical artifacts. New
    # producer prompts must emit verification_kind and leave this field absent.
    checkability: (
        Literal[
            "structure",
            "relation",
            "effect",
            "simulation",
            "fbmcq",
            "topology",
            "provenance",
        ]
        | None
    ) = Field(default=None, exclude=True)

    @model_validator(mode="before")
    @classmethod
    def _derive_kind_from_predicate(cls, value: Any) -> Any:
        """Let the named predicate settle the family, and reject unknown names.

        The predicate is authoritative on purpose.  If a producer names
        ``occupancy_after`` but labels the requirement ``structure``, honouring
        the label would let a declaration check close a runtime claim -- the
        false-positive shape this vocabulary exists to prevent.  So the label is
        overwritten, not merely validated.
        """

        if not isinstance(value, dict):
            return value
        predicate = value.get("predicate")
        if predicate is None:
            return value
        if not isinstance(predicate, str) or predicate not in PREDICATE_NAMES:
            raise ValueError(
                f"unknown predicate {predicate!r}; use one of the closed "
                f"vocabulary: {', '.join(sorted(PREDICATE_NAMES))}"
            )
        entry = PREDICATE_BY_NAME[predicate]
        missing = [
            name
            for name in entry.bindings
            if not str((value.get("predicate_bindings") or {}).get(name) or "").strip()
        ]
        if missing:
            raise ValueError(
                f"predicate {predicate!r} requires bindings {list(entry.bindings)}; "
                f"missing or empty: {missing}"
            )
        return {**value, "verification_kind": verification_kind_of(predicate)}

    @model_validator(mode="before")
    @classmethod
    def _upgrade_v1_checkability(cls, value: Any) -> Any:
        if not isinstance(value, dict) or value.get("verification_kind"):
            return value
        legacy = value.get("checkability")
        mapping = {
            "structure": "structure",
            "relation": "structure",
            "topology": "structure",
            "provenance": "structure",
            "effect": "behavior",
            "simulation": "behavior",
            "fbmcq": "property",
        }
        if legacy in mapping:
            return {**value, "verification_kind": mapping[legacy]}
        return value


class RequirementSet(StrictBaseModel):
    schema_name: Literal["RequirementSet"] = "RequirementSet"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    revision: int = Field(ge=1)
    requirements: tuple[Requirement, ...] = Field(min_length=1)
    segment_disposition: dict[
        str, Literal["covered", "context", "ambiguous", "out_of_scope"]
    ] = Field(default_factory=dict)

    @field_validator("requirements")
    @classmethod
    def _unique_requirement_ids(
        cls, reqs: tuple[Requirement, ...]
    ) -> tuple[Requirement, ...]:
        ids = [req.requirement_id for req in reqs]
        if len(ids) != len(set(ids)):
            raise ValueError("requirement_id values must be unique")
        return reqs


class RequirementCoverageProjection(StrictBaseModel):
    covered_requirement_ids: tuple[str, ...]
    missing_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    accepted_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    quarantined_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)


class CoverageGap(StrictBaseModel):
    gap_id: str = Field(pattern=r"^GAP-[A-Za-z0-9_.-]+$", min_length=5)
    stage: Literal["requirement_split", "assertion_conversion", "assertion_review"]
    requirement_id: str | None = None
    assertion_ids: tuple[str, ...] = Field(default_factory=tuple)
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    reason_code: Literal[
        "no_progress",
        "revision_budget_exhausted",
        "contract_invalid",
        "review_unresolved",
    ]
    reason: str = Field(min_length=1)
    last_revision: int = Field(ge=0)
    last_feedback: str | None = None
    history_refs: tuple[str, ...] = Field(default_factory=tuple)
    coverage_impact: str = Field(min_length=1)
    blocks_full_coverage: StrictBool


class ExcludedObservation(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole
    disposition: Literal[
        "supporting_false",
        "quarantined",
        "representation_debt",
        "unattributed",
    ]
    rationale: str = Field(min_length=1)


class RequirementReviewFinding(StrictBaseModel):
    requirement_id: str | None = None
    severity: Literal["critical", "important", "minor"]
    message: str = Field(min_length=1)
    required_change: str = Field(min_length=1)


class RequirementReview(StrictBaseModel):
    schema_name: Literal["RequirementReview"] = "RequirementReview"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    decision: Literal["accept", "revise"]
    reviewed_revision: int = Field(ge=1)
    findings: tuple[RequirementReviewFinding, ...] = Field(default_factory=tuple)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _decision_findings_consistent(self) -> "RequirementReview":
        if self.decision == "accept" and self.findings:
            raise ValueError("accept reviews must not contain findings")
        if self.decision == "revise" and not self.findings:
            raise ValueError("revise reviews require at least one finding")
        return self


class AssertionSpec(StrictBaseModel):
    assertion_id: str = Field(pattern=r"^AST-[A-Za-z0-9_.-]+$", min_length=5)
    requirement_id: str = Field(pattern=r"^REQ-[A-Za-z0-9_.-]+$", min_length=5)
    description: str = Field(min_length=1)
    expression: str = Field(min_length=1)
    failure_message: str = Field(min_length=1)
    evidence_family: EvidenceFamily
    role: AssertionRole | None = None
    coverage_key: str | None = None
    aggregation_group: str | None = None

    @model_validator(mode="before")
    @classmethod
    def _upgrade_v1_assertion_role(cls, value: Any) -> Any:
        if not isinstance(value, dict):
            return value
        assertion_id = value.get("assertion_id")
        requirement_id = value.get("requirement_id")
        if not assertion_id or not requirement_id:
            return value
        return {
            **value,
            "coverage_key": value.get("coverage_key") or f"legacy:{assertion_id}",
            "aggregation_group": value.get("aggregation_group")
            or f"legacy-group:{requirement_id}",
        }

    @model_validator(mode="after")
    def _coverage_fields_present(self) -> "AssertionSpec":
        if not self.coverage_key or not self.aggregation_group:
            raise ValueError("assertions require coverage_key and aggregation_group")
        return self


class AssertionScript(StrictBaseModel):
    schema_name: Literal["AssertionScript"] = "AssertionScript"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    revision: int = Field(ge=1)
    prefix: str = ""
    assertions: tuple[AssertionSpec, ...] = Field(min_length=1)
    requirement_mapping: dict[str, tuple[str, ...]] = Field(default_factory=dict)

    @field_validator("assertions")
    @classmethod
    def _unique_assertion_ids(
        cls, assertions: tuple[AssertionSpec, ...]
    ) -> tuple[AssertionSpec, ...]:
        ids = [item.assertion_id for item in assertions]
        if len(ids) != len(set(ids)):
            raise ValueError("assertion_id values must be unique")
        return assertions


class AssertionExecutionPublic(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole = "primary"
    coverage_key: str | None = None
    status: Literal["executable", "invalid"]
    error: str | None = None


class AssertionCheckPublic(StrictBaseModel):
    schema_name: Literal["AssertionCheckPublic"] = "AssertionCheckPublic"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str = Field(min_length=1)
    tool_env_hash: str = Field(min_length=1)
    status: Literal["executable", "invalid"]
    executions: tuple[AssertionExecutionPublic, ...]

    @model_validator(mode="after")
    def _status_matches_executions(self) -> "AssertionCheckPublic":
        if self.status == "executable" and any(
            e.status != "executable" for e in self.executions
        ):
            raise ValueError("executable check cannot contain invalid executions")
        if self.status == "invalid" and not any(
            e.status == "invalid" for e in self.executions
        ):
            raise ValueError("invalid check requires an invalid execution")
        return self


class AssertionResult(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    role: AssertionRole = "primary"
    coverage_key: str | None = None
    aggregation_group: str | None = None
    truth_value: StrictBool
    script_hash: str
    tool_env_hash: str
    evidence_family: str = Field(min_length=1)
    failure_message: str | None = None
    evidence_scope: dict[str, Any] = Field(default_factory=dict)
    evidence_record_ids: tuple[str, ...] = Field(default_factory=tuple)
    check_detail: dict[str, Any] = Field(default_factory=dict)


class SealedAssertionReceipt(StrictBaseModel):
    schema_name: Literal["SealedAssertionReceipt"] = "SealedAssertionReceipt"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str = Field(min_length=1)
    tool_env_hash: str = Field(min_length=1)
    sealed_hash: str = Field(min_length=1)
    result_count: int = Field(ge=0)
    sealed_payload_ref: str = Field(min_length=1)


class AssertionReviewFinding(StrictBaseModel):
    assertion_id: str | None = None
    requirement_id: str | None = None
    severity: Literal["critical", "important", "minor"]
    message: str = Field(min_length=1)
    required_change: str = Field(min_length=1)


class AssertionReview(StrictBaseModel):
    schema_name: Literal["AssertionReview"] = "AssertionReview"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    decision: Literal["accept", "revise"]
    reviewed_script_hash: str = Field(min_length=1)
    findings: tuple[AssertionReviewFinding, ...] = Field(default_factory=tuple)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _decision_findings_consistent(self) -> "AssertionReview":
        if self.decision == "accept" and self.findings:
            raise ValueError("accept reviews must not contain findings")
        if self.decision == "revise" and not self.findings:
            raise ValueError("revise reviews require at least one finding")
        return self


class ReleasedAssertionResults(StrictBaseModel):
    schema_name: Literal["ReleasedAssertionResults"] = "ReleasedAssertionResults"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    script_hash: str
    tool_env_hash: str
    sealed_hash: str
    results: tuple[AssertionResult, ...]


class AttributionBinding(StrictBaseModel):
    assertion_id: str
    requirement_id: str
    status: Literal["safe", "representation_debt", "unattributed"]
    source_refs: tuple[str, ...] = Field(default_factory=tuple)
    trace_entry_ids: tuple[str, ...] = Field(default_factory=tuple)
    exclusion_refs: tuple[str, ...] = Field(default_factory=tuple)
    source_level_claim_allowed: StrictBool = False
    rationale: str = Field(min_length=1)


class AttributionProjection(StrictBaseModel):
    schema_name: Literal["AttributionProjection"] = "AttributionProjection"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    bindings: tuple[AttributionBinding, ...]


class AdjudicatedIssue(StrictBaseModel):
    issue_id: str = Field(pattern=r"^ISSUE-[A-Za-z0-9_.-]+$", min_length=7)
    requirement_id: str
    assertion_ids: tuple[str, ...] = Field(min_length=1)
    title: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    attribution_status: Literal["safe", "representation_debt", "unattributed"]


class DiscoverAdjudication(StrictBaseModel):
    schema_name: Literal["DiscoverAdjudication"] = "DiscoverAdjudication"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    has_confirmed_issues: StrictBool
    issues: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    satisfied_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    excluded_findings: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    excluded_observations: tuple[ExcludedObservation, ...] = Field(
        default_factory=tuple
    )
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _issue_flag_consistent(self) -> "DiscoverAdjudication":
        if self.has_confirmed_issues != bool(self.issues):
            raise ValueError("has_confirmed_issues must match issues emptiness")
        if any(issue.attribution_status != "safe" for issue in self.issues):
            raise ValueError("confirmed issues must be attribution-safe")
        # Supporting False observations can arrive in excluded_findings from
        # the structured LLM response. The deterministic adjudication node
        # removes them before enforcing primary-only issue/exclusion closure.
        return self


class DiscoverCompleted(StrictBaseModel):
    schema_name: Literal["DiscoverCompleted"] = "DiscoverCompleted"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    status: Literal["completed"] = "completed"
    input_hashes: dict[str, str]
    requirement_set_hash: str
    assertion_script_hash: str
    released_results_hash: str
    adjudication: DiscoverAdjudication
    issues: tuple[AdjudicatedIssue, ...]
    coverage_status: Literal["full", "partial"] = "full"
    coverage_gaps: tuple[CoverageGap, ...] = Field(default_factory=tuple)
    satisfied_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    # Primary False assertions the adjudicator kept out of `issues` because
    # their attribution is representation_debt or unattributed.  These were
    # recorded in the adjudication but never surfaced in the published
    # artifact, so a reader of discover-completed.json could not tell "no
    # evidence was produced" from "False evidence could not be attributed" --
    # on pair 0006 that hid the entire EXP-0006-EA-001 observation.
    excluded_findings: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    excluded_observations: tuple[ExcludedObservation, ...] = Field(
        default_factory=tuple
    )
    adjudication_reconciliation: dict[str, Any] = Field(default_factory=dict)
    regression_guards: tuple[str, ...] = Field(default_factory=tuple)
    telemetry_summary: dict[str, Any] = Field(default_factory=dict)
    content_language: Literal["zh-CN", "en-US"] = "zh-CN"


class RunFailure(StrictBaseModel):
    schema_name: Literal["RunFailure"] = "RunFailure"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    node_name: str
    message: str = Field(min_length=1)
    failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NodeExecutionRecord(StrictBaseModel):
    schema_name: Literal["NodeExecutionRecord"] = "NodeExecutionRecord"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    node_call_id: str
    node_name: str
    revision: int = Field(ge=0)
    kind: Literal["deterministic", "llm"]
    status: Literal["completed", "failed"]
    input_hash: str
    output_hash: str | None = None
    started_at: datetime
    finished_at: datetime
    elapsed_ms: float = Field(ge=0)
    failure: str | None = None
    details: dict[str, Any] = Field(default_factory=dict)


class LLMCallRecord(StrictBaseModel):
    schema_name: Literal["LLMCallRecord"] = "LLMCallRecord"
    schema_version: Literal["v2"] = SCHEMA_VERSION
    run_id: str
    llm_call_id: str
    node_call_id: str
    role: str
    revision: int = Field(ge=0)
    profile: str
    adapter: str | None = None
    provider: str | None = None
    configured_model: str | None = None
    observed_model: str | None = None
    started_at: datetime
    finished_at: datetime
    elapsed_ms: float = Field(ge=0)
    status: Literal["completed", "failed"]
    model_id: str | None = None
    input_hash: str
    output_hash: str | None = None
    system_prompt: str
    user_prompt: str
    system_prompt_sha256: str | None = None
    user_prompt_sha256: str | None = None
    parsed_output: dict[str, Any] | None = None
    raw_response: dict[str, Any] | None = None
    parsed_output_sha256: str | None = None
    raw_response_sha256: str | None = None
    system_prompt_chars: int = Field(ge=0)
    user_prompt_chars: int = Field(ge=0)
    output_chars: int | None = Field(default=None, ge=0)
    input_tokens: int | None = Field(default=None, ge=0)
    output_tokens: int | None = Field(default=None, ge=0)
    total_tokens: int | None = Field(default=None, ge=0)
    cache_read_input_tokens: int | None = Field(default=None, ge=0)
    cache_creation_input_tokens: int | None = Field(default=None, ge=0)
    ephemeral_5m_input_tokens: int | None = Field(default=None, ge=0)
    ephemeral_1h_input_tokens: int | None = Field(default=None, ge=0)
    reasoning_tokens: int | None = Field(default=None, ge=0)
    usage_status: Literal["complete", "partial", "unavailable"] = "unavailable"
    usage_sources: tuple[str, ...] = Field(default_factory=tuple)
    transport_attempts: tuple[dict[str, Any], ...] = Field(default_factory=tuple)
    failure: str | None = None


class DiscoverGraphState(TypedDict, total=False):
    run_identity: DiscoverRunIdentity
    frozen_inputs: FrozenDiscoverInputs
    requirement_set: RequirementSet
    requirement_coverage: RequirementCoverageProjection
    requirement_review: RequirementReview
    assertion_script: AssertionScript
    assertion_check_public: AssertionCheckPublic
    sealed_assertion_results: SealedAssertionReceipt
    assertion_review: AssertionReview
    released_assertion_results: ReleasedAssertionResults
    attribution_projection: AttributionProjection
    adjudication: DiscoverAdjudication
    coverage_gaps: tuple[CoverageGap, ...]
    _adjudication_reconciliation: dict[str, Any]
    final_output: DiscoverCompleted
    failure: RunFailure
    node_execution_records: list[NodeExecutionRecord]
    llm_call_records: list[LLMCallRecord]
    requirement_fingerprints: tuple[str, ...]
    assertion_fingerprints: tuple[str, ...]
    _assertion_contract_failure_signatures: tuple[str, ...]
    _assertion_invalid_signatures: tuple[str, ...]
    _input: DiscoverInput
    _requirement_feedback: RevisionFeedback
    _requirement_revision_ledger: tuple[RevisionLedgerEvent, ...]
    _requirement_review_repair_count: int
    _requirement_contract_repair_count: int
    _requirement_split_contract_feedback: RevisionFeedback | None
    _assertion_feedback: RevisionFeedback | None
    _assertion_feedback_history: tuple[RevisionFeedback, ...]
    _assertion_revision_ledger: tuple[RevisionLedgerEvent, ...]
    _assertion_review_repair_count: int
    _assertion_conversion_contract_feedback: RevisionFeedback | None
    _assertion_contract_repair_count: int
    _assertion_no_progress_recovery_count: int
    # Item-local budgets (Issue #167 §8.3).  Keyed by assertion id and by
    # semantic failure identity respectively, so isolation can act per item
    # instead of per whole script.
    _assertion_item_repair_counts: dict[str, int]
    _assertion_invalid_semantic_counts: dict[str, int]
    _precheck_round_count: int
    _last_executable_assertion_script: AssertionScript
    _quarantined_assertion_ids: tuple[str, ...]
