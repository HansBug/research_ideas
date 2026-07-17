from __future__ import annotations

from typing import Any

from typing_extensions import Literal

from pydantic import BaseModel, ConfigDict, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class SupportingRecord(StrictModel):
    record_id: str
    summary: str = ""


class IssueCheck(StrictModel):
    check_id: str
    check_origin: Literal["nl_grounded_behavioral_issue", "raw_internal_inconsistency"]
    check_kind: Literal["scenario", "property", "static_consistency"]
    statement: str
    expected_outcome: dict[str, Any] = Field(default_factory=dict)
    basis_hashes: dict[str, str] = Field(default_factory=dict)
    source_basis: list[str] = Field(default_factory=list)
    nl_basis: list[dict[str, str]] = Field(default_factory=list)
    executable_spec: dict[str, Any] = Field(default_factory=dict)
    binding_refs: list[str] = Field(default_factory=list)
    required: bool = True


class CheckDraft(StrictModel):
    check_id: str
    check_kind: Literal["scenario", "property", "static_consistency"]
    statement: str
    expected_outcome: dict[str, Any] = Field(default_factory=dict)
    source_basis: list[str] = Field(default_factory=list)
    nl_basis: list[dict[str, str]] = Field(default_factory=list)
    executable_spec: dict[str, Any] = Field(default_factory=dict)
    binding_refs: list[str] = Field(default_factory=list)
    required: bool = True


class DiscoverCheckDraft(CheckDraft):
    check_origin: Literal["nl_grounded_behavioral_issue", "raw_internal_inconsistency"]


class CheckDraftSubmission(StrictModel):
    checks: list[CheckDraft] = Field(default_factory=list)
    rationale: str = ""


class RootIssue(StrictModel):
    node_id: str
    issue_id: str
    previous_node_id: str | None = None
    assessment: Literal["confirmed", "candidate_only"]
    downstream_repair_allowed: bool
    statement: str
    rationale: str
    supporting_record_ids: list[str] = Field(default_factory=list)
    required_check_ids: list[str] = Field(default_factory=list)
    source_element_refs: list[str] = Field(default_factory=list)


class RejectedProposition(StrictModel):
    proposition_id: str
    assessment: Literal["rejected"] = "rejected"
    statement: str
    rationale: str
    supporting_record_ids: list[str] = Field(default_factory=list)
    considered_check_ids: list[str] = Field(default_factory=list)
    source_element_refs: list[str] = Field(default_factory=list)


class DiscoverSubmission(StrictModel):
    submission_type: Literal["submit_discovery"] = "submit_discovery"
    assessment_origin: Literal["discover"] = "discover"
    check_drafts: list[DiscoverCheckDraft] = Field(min_length=1)
    no_issue_found: bool = False
    root_nodes: list[RootIssue] = Field(default_factory=list)
    rejected_propositions: list[RejectedProposition] = Field(default_factory=list)
    rationale: str = ""
