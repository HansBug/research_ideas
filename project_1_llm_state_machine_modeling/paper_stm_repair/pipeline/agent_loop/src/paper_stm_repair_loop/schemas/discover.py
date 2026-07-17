from __future__ import annotations

from typing_extensions import Literal

from pydantic import Field

from .common import DiscoverSubmission, IssueCheck, RejectedProposition, RootIssue, StrictModel


class AgentReceiptRef(StrictModel):
    audit_path: str
    result_path: str
    receipt_path: str | None = None
    result_sha256: str


class DiscoverCompleted(StrictModel):
    schema_version: Literal["paper1.discover_completed.v1"] = "paper1.discover_completed.v1"
    run_id: str
    stage: Literal["B-discover"] = "B-discover"
    loop_no: Literal[0] = 0
    model_id: str
    model_sha256: str
    issue_checks: list[IssueCheck] = Field(min_length=1)
    root_nodes: list[RootIssue] = Field(default_factory=list)
    rejected_propositions: list[RejectedProposition] = Field(default_factory=list)
    no_issue_found: bool
    rationale: str
    agent_real_llm: bool
    agent_academic_eligible: bool
    test_replay: bool
    main_result_eligible: Literal[False] = False
    agent_receipt_ref: AgentReceiptRef
    supporting_record_ids: list[str] = Field(default_factory=list)
    completed_record_id: str
    completed_record_sha256: str


def submission_payload(submission: DiscoverSubmission) -> dict[str, object]:
    return submission.model_dump(mode="json")
