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

SCHEMA_VERSION = "v1"


class StrictBaseModel(BaseModel):
    # JSON arrays are the wire representation of immutable tuple fields. Keep
    # extra-field rejection/frozen outputs while using StrictBool explicitly at
    # the truth-bearing method boundaries.
    model_config = ConfigDict(extra="forbid", frozen=True)


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


class DiscoverInput(StrictBaseModel):
    schema_name: Literal["DiscoverInput"] = "DiscoverInput"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
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


class Requirement(StrictBaseModel):
    requirement_id: str = Field(pattern=r"^REQ-[A-Za-z0-9_.-]+$", min_length=5)
    statement: str = Field(min_length=1)
    rationale: str = Field(default="")
    source_segment_ids: tuple[str, ...] = Field(default_factory=tuple)
    checkability: Literal[
        "structure",
        "relation",
        "effect",
        "simulation",
        "fbmcq",
        "topology",
        "provenance",
    ]


class RequirementSet(StrictBaseModel):
    schema_name: Literal["RequirementSet"] = "RequirementSet"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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


class RequirementReviewFinding(StrictBaseModel):
    requirement_id: str | None = None
    severity: Literal["critical", "important", "minor"]
    message: str = Field(min_length=1)
    required_change: str = Field(min_length=1)


class RequirementReview(StrictBaseModel):
    schema_name: Literal["RequirementReview"] = "RequirementReview"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    evidence_family: Literal[
        "structure",
        "relation",
        "effect",
        "simulation",
        "fbmcq",
        "topology",
        "provenance",
    ]


class AssertionScript(StrictBaseModel):
    schema_name: Literal["AssertionScript"] = "AssertionScript"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    status: Literal["executable", "invalid"]
    error: str | None = None


class AssertionCheckPublic(StrictBaseModel):
    schema_name: Literal["AssertionCheckPublic"] = "AssertionCheckPublic"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    schema_version: Literal["v1"] = SCHEMA_VERSION
    has_confirmed_issues: StrictBool
    issues: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    satisfied_requirement_ids: tuple[str, ...] = Field(default_factory=tuple)
    excluded_findings: tuple[AdjudicatedIssue, ...] = Field(default_factory=tuple)
    rationale: str = Field(min_length=1)

    @model_validator(mode="after")
    def _issue_flag_consistent(self) -> "DiscoverAdjudication":
        if self.has_confirmed_issues != bool(self.issues):
            raise ValueError("has_confirmed_issues must match issues emptiness")
        if any(issue.attribution_status != "safe" for issue in self.issues):
            raise ValueError("confirmed issues must be attribution-safe")
        if any(
            finding.attribution_status == "safe"
            for finding in self.excluded_findings
        ):
            raise ValueError("excluded findings must be representation debt or unattributed")
        return self


class DiscoverCompleted(StrictBaseModel):
    schema_name: Literal["DiscoverCompleted"] = "DiscoverCompleted"
    schema_version: Literal["v1"] = SCHEMA_VERSION
    run_id: str
    status: Literal["completed"] = "completed"
    input_hashes: dict[str, str]
    requirement_set_hash: str
    assertion_script_hash: str
    released_results_hash: str
    adjudication: DiscoverAdjudication
    issues: tuple[AdjudicatedIssue, ...]
    regression_guards: tuple[str, ...] = Field(default_factory=tuple)
    telemetry_summary: dict[str, Any] = Field(default_factory=dict)
    content_language: Literal["zh-CN", "en-US"] = "zh-CN"


class RunFailure(StrictBaseModel):
    schema_name: Literal["RunFailure"] = "RunFailure"
    schema_version: Literal["v1"] = SCHEMA_VERSION
    run_id: str
    node_name: str
    message: str = Field(min_length=1)
    failed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class NodeExecutionRecord(StrictBaseModel):
    schema_name: Literal["NodeExecutionRecord"] = "NodeExecutionRecord"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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


class LLMCallRecord(StrictBaseModel):
    schema_name: Literal["LLMCallRecord"] = "LLMCallRecord"
    schema_version: Literal["v1"] = SCHEMA_VERSION
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
    parsed_output: dict[str, Any] | None = None
    raw_response: dict[str, Any] | None = None
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
    final_output: DiscoverCompleted
    failure: RunFailure
    node_execution_records: list[NodeExecutionRecord]
    llm_call_records: list[LLMCallRecord]
    requirement_fingerprints: tuple[str, ...]
    assertion_fingerprints: tuple[str, ...]
    _input: DiscoverInput
    _requirement_feedback: RevisionFeedback
    _assertion_feedback: RevisionFeedback
