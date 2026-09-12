from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal


class RecordModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class EvidenceScopeMetadata(RecordModel):
    """Reviewer-visible evidence metadata for one assertion attempt."""

    initialization: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Requested and effective cold/hot initialization, state, variables, "
            "cycles, final observation, and limitations for simulation evidence."
        ),
    )
    formal: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Canonical formal query, parsed property kind, finite bound, bound "
            "origin, assumptions, solver status, witness, replay status, and limitations."
        ),
    )
    check: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Check-result, model, tool, schema, and backend fingerprints used to "
            "produce the evidence record."
        ),
    )
    policy: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Evidence-policy fingerprint and assumption provenance that define how "
            "the attempt may be interpreted by reviewers and renderers."
        ),
    )
    formal_bound_origin: Literal["requirement_bound", "analysis_bound"] | None = None


class EvidenceCallModel(BaseModel):
    """Base model for typed evidence calls while preserving backend details."""

    model_config = ConfigDict(extra="allow")


class SimulationEvidenceCall(EvidenceCallModel):
    requested: dict[str, Any]
    effective: dict[str, Any]
    cycles: list[list[str]]
    final: dict[str, Any]


class FormalEvidenceCall(EvidenceCallModel):
    query: str
    canonical_query: str
    formal_property_kind: str
    formal_bound: int = Field(ge=0)
    limitations: list[str]


class InitializationEvidence(RecordModel):
    calls: list[SimulationEvidenceCall]


class FormalEvidence(RecordModel):
    calls: list[FormalEvidenceCall]
    formal_property_kind: str | None = None
    formal_bound: int | None = Field(default=None, ge=0)
    formal_bound_origin: Literal["requirement_bound", "analysis_bound"] | None = None
    formal_assumption_basis_ids: list[str] = Field(default_factory=list)


class CheckEvidence(EvidenceCallModel):
    check_record_id: str
    check_result_sha256: str
    model_sha256: str
    tool_hash: str
    tool_schema_hash: str


class PolicyEvidence(EvidenceCallModel):
    policy_hash: str
    evidence_policy_fingerprint: str


class EvalAssertCompletedPayload(EvidenceCallModel):
    """Fail-closed evidence contract for one completed assertion record."""

    initialization: InitializationEvidence
    formal: FormalEvidence
    check: CheckEvidence
    policy: PolicyEvidence
    limitations: list[str]

    @model_validator(mode="after")
    def validate_formal_scope(self) -> "EvalAssertCompletedPayload":
        if not self.formal.calls:
            return self
        if (
            self.formal.formal_property_kind is None
            or self.formal.formal_bound is None
            or self.formal.formal_bound_origin is None
        ):
            raise ValueError(
                "formal calls require property kind, bound, and bound origin"
            )
        required = {
            "finite_horizon_only",
            "exact_query_and_assumptions_only",
            "does_not_establish_unbounded_correctness",
        }
        for call in self.formal.calls:
            if not required.issubset(set(call.limitations)):
                raise ValueError("formal call lacks bounded-evidence limitations")
        if not required.issubset(set(self.limitations)):
            raise ValueError("record lacks bounded-evidence limitations")
        return self


class DiscoverEligibilityRecordPayload(EvidenceCallModel):
    """Eligibility fields persisted in the immutable discover completion record."""

    agent_trace_eligible: bool
    agent_trace_eligibility_scope: Literal["agent_behavior_trace"]
    input_academic_eligible: bool
    input_academic_ineligibility_reason: str | None = None
    agent_academic_eligible: bool
    main_result_eligible: Literal[False]

    @model_validator(mode="after")
    def validate_legacy_trace_alias(self) -> "DiscoverEligibilityRecordPayload":
        if self.agent_academic_eligible != self.agent_trace_eligible:
            raise ValueError(
                "agent_academic_eligible must equal agent_trace_eligible"
            )
        return self


class Record(RecordModel):
    record_id: str
    sequence: int
    logical_loop_index: int = 0
    record_type: str
    stage: str = "B-discover"
    loop_id: str = "loop-000"
    previous_record_id: str | None = None
    previous_record_sha256: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    artifact_refs: list[dict[str, Any]] = Field(default_factory=list)
    record_sha256: str
