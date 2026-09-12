from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal

from .tools import NonBlankString


class StrictContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True, strict=True)


FunctionFamily = Literal[
    "structure",
    "relation",
    "effect",
    "simulation",
    "formal",
    "mapping",
]

FormalPropertyKind = Literal[
    "reach",
    "forbid",
    "invariant",
    "must_reach",
    "exists_always",
    "cover",
    "response",
]
FormalBoundOrigin = Literal["requirement_bound", "analysis_bound"]


class EvidenceScope(StrictContractModel):
    semantic_profile: str
    max_steps: int | None = Field(default=None, ge=0)
    max_time: int | float | None = None
    abstraction: str
    claim_strength: str


class LogicalAssertion(StrictContractModel):
    assertion_chain_id: str
    assertion_version_id: str
    root_node_id: str
    coverage_unit_id: str
    required: bool = True
    assert_: str = Field(alias="assert", min_length=1)
    assert_sha256: str
    basis_ids: list[str] = Field(default_factory=list)
    obligation_signature: str
    required_function_families: list[FunctionFamily] = Field(default_factory=list)
    evidence_scope: EvidenceScope
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"
    formal_property_kind: FormalPropertyKind | None = None
    formal_bound: int | None = Field(default=None, ge=1)
    formal_bound_origin: FormalBoundOrigin | None = None
    formal_assumption_basis_ids: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_assertion_basis(self) -> "LogicalAssertion":
        if not self.basis_ids:
            raise ValueError("LogicalAssertion requires at least one basis id")
        if not self.required_function_families:
            raise ValueError("LogicalAssertion requires at least one evidence function family")
        return self


class LogicalAssertionRegistration(StrictContractModel):
    assertion_chain_id: str = Field(min_length=1)
    root_node_id: str = Field(min_length=1)
    coverage_unit_id: str = Field(min_length=1)
    required: bool = True
    assert_: str = Field(alias="assert", min_length=1)
    basis_ids: list[str] = Field(min_length=1)
    obligation_signature: str = Field(min_length=1)
    required_function_families: list[FunctionFamily] = Field(min_length=1)
    evidence_scope: EvidenceScope
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"
    formal_property_kind: FormalPropertyKind | None = None
    formal_bound: int | None = Field(default=None, ge=1)
    formal_bound_origin: FormalBoundOrigin | None = None
    formal_assumption_basis_ids: list[str] = Field(default_factory=list)


class EvalAssertToolInput(StrictContractModel):
    assert_: str = Field(alias="assert", min_length=1)
    reason: NonBlankString


class EvalAssertResult(StrictContractModel):
    execution_status: Literal["completed", "inconclusive"]
    assertion_chain_id: str
    assertion_version_id: str
    assert_sha256: str
    root_node_id: str
    coverage_unit_id: str
    prepared_record_id: str
    record_id: str | None = None
    match_status: Literal["matches", "contradicts", "inconclusive"]
    inconclusive_reason: str | None = None
    python_value_type: str | None = None
    python_value: bool | None = None
    exception: dict[str, Any] | None = None
    function_calls: list[dict[str, Any]] = Field(default_factory=list)
    observed_function_families: list[FunctionFamily] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    producer_versions: dict[str, Any] = Field(default_factory=dict)
    model_sha256: str
    dependency_provenance: dict[str, Any]
    eval_vars_hash_before: str
    eval_vars_hash_after: str
    function_registry_hash: str
    reason: str
    reason_context: dict[str, Any]
    missing_latest_required_assertions: list[dict[str, Any]] = Field(
        default_factory=list
    )
    incomplete_latest_required_assertions: list[dict[str, Any]] = Field(
        default_factory=list
    )
    submit_allowed: bool = False
    controller_projection: dict[str, Any] | None = None
    formal_property_kind: FormalPropertyKind | None = None
    formal_bound: int | None = Field(default=None, ge=1)
    formal_bound_origin: FormalBoundOrigin | None = None
    formal_assumption_basis_ids: list[str] = Field(default_factory=list)
    initialization: dict[str, Any] = Field(default_factory=dict)
    formal: dict[str, Any] = Field(default_factory=dict)
    check: dict[str, Any] = Field(default_factory=dict)
    policy: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_status_value(self) -> "EvalAssertResult":
        if self.match_status == "matches" and self.python_value is not True:
            raise ValueError("matches requires python_value=True")
        if self.match_status == "contradicts" and self.python_value is not False:
            raise ValueError("contradicts requires python_value=False")
        if self.match_status == "inconclusive" and self.python_value is not None:
            raise ValueError("inconclusive requires python_value=None")
        return self
