from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal

from .roots import PropositionRootNode
from .tools import NonBlankString


class StrictContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class DiscoverOutcome(StrictContractModel):
    run_outcome: Literal[
        "issues_found",
        "reviewer_accepted_zero_issue",
    ]
    registered_worklist_complete: Literal[True]
    major_behavior_coverage_assurance: Literal[
        "controller_closed_dual_llm_reviewed",
        "evaluator_checked",
        "preregistered_holdout_checked",
    ] = "controller_closed_dual_llm_reviewed"
    input_segment_coverage: dict[str, Any] = Field(default_factory=dict)
    selected_source_fact_evidence_coverage: dict[str, Any] = Field(default_factory=dict)
    coverage_requirement_coverage: dict[str, Any] = Field(default_factory=dict)
    assertion_execution_coverage: dict[str, Any] = Field(default_factory=dict)
    major_behavior_coverage_review: dict[str, Any] = Field(default_factory=dict)
    proposition_roots: list[PropositionRootNode] = Field(default_factory=list)
    issue_root_projection: list[PropositionRootNode] = Field(default_factory=list)
    regression_guard_projection: list[PropositionRootNode] = Field(default_factory=list)
    incomplete_root_projection: list[PropositionRootNode] = Field(default_factory=list)
    rationale: str = ""

    @model_validator(mode="after")
    def validate_outcome_coverage(self) -> "DiscoverOutcome":
        if self.incomplete_root_projection:
            raise ValueError("successful Discover output cannot publish incomplete roots")
        roots = {root.node_id: root for root in self.proposition_roots}
        if len(roots) != len(self.proposition_roots):
            raise ValueError("proposition root IDs must be unique")
        for root in self.issue_root_projection:
            if roots.get(root.node_id) != root:
                raise ValueError("issue projection must reference an identical published root")
            if not (
                root.status == "issue"
                and root.runtime_issue_assessment == "confirmed"
                and root.repair_allowed is True
            ):
                raise ValueError("issue projection accepts confirmed repair-allowed roots only")
        for root in self.regression_guard_projection:
            if roots.get(root.node_id) != root or not (
                root.status == "ok" and root.regression_guard is True
            ):
                raise ValueError("regression projection accepts identical ok guards only")
        for root in self.incomplete_root_projection:
            if roots.get(root.node_id) != root or root.status != "incomplete":
                raise ValueError("incomplete projection accepts identical incomplete roots only")
        return self


class DiscoverSubmission(StrictContractModel):
    submission_type: Literal["submit_discovery"] = "submit_discovery"
    outcome: DiscoverOutcome
    reason: NonBlankString


class AgentReceiptRef(StrictContractModel):
    audit_path: str
    result_path: str
    receipt_path: str | None = None
    result_sha256: str


class DiscoverCompleted(StrictContractModel):
    schema_version: Literal["paper1.discover_completed.v2"] = (
        "paper1.discover_completed.v2"
    )
    run_id: str
    stage: Literal["B-discover"] = "B-discover"
    loop_no: Literal[0] = 0
    model_id: Literal["STM_0"] = "STM_0"
    model_sha256: str
    input_segments: list[dict[str, Any]] = Field(default_factory=list)
    coverage_requirements: list[dict[str, Any]] = Field(default_factory=list)
    source_facts: list[dict[str, Any]] = Field(default_factory=list)
    coverage_plan: dict[str, Any]
    outcome: DiscoverOutcome
    agent_real_llm: bool
    agent_academic_eligible: bool
    test_replay: bool = False
    main_result_eligible: Literal[False] = False
    main_result_eligibility_owner: Literal["post_loop_experiment_gate"] = (
        "post_loop_experiment_gate"
    )
    main_result_eligibility_reason: str
    agent_receipt_ref: AgentReceiptRef
    supporting_record_ids: list[str] = Field(default_factory=list)
    completed_record_id: str
    completed_record_sha256: str
