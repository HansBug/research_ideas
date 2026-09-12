from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal


class StrictContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class PropositionRootRegistration(StrictContractModel):
    node_id: str = Field(min_length=1)
    previous_node_id: str | None = None
    coverage_unit_id: str = Field(min_length=1)
    statement: str = Field(min_length=1)
    model_element_refs: list[str] = Field(default_factory=list)
    source_element_refs: list[str] = Field(default_factory=list)
    rationale: str = Field(min_length=1)
    record_language: str = "zh-CN"


class PropositionRootNode(StrictContractModel):
    node_id: str
    previous_node_id: str | None = None
    coverage_unit_id: str
    assertion_chain_ids: list[str] = Field(min_length=1)
    statement: str = Field(min_length=1)
    status: Literal["planned", "evaluating", "ok", "issue", "incomplete"]
    runtime_issue_assessment: Literal["confirmed", "candidate_only"] | None = None
    repair_allowed: bool = False
    regression_guard: bool = False
    model_element_refs: list[str] = Field(default_factory=list)
    source_element_refs: list[str] = Field(default_factory=list)
    supporting_record_ids: list[str] = Field(default_factory=list)
    rationale: str = ""
    record_language: str = "zh-CN"

    @model_validator(mode="after")
    def validate_projection_flags(self) -> "PropositionRootNode":
        if self.status == "issue" and self.runtime_issue_assessment == "confirmed" and not self.repair_allowed:
            raise ValueError("confirmed issue root must be repair_allowed")
        if self.status == "ok" and self.repair_allowed:
            raise ValueError("ok root cannot be repair_allowed")
        if self.status != "ok" and self.regression_guard:
            raise ValueError("only ok roots can be regression guards")
        return self
