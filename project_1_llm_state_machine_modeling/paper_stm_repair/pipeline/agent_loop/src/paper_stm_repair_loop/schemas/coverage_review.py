from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal


class StrictReviewModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class CoverageReviewFinding(StrictReviewModel):
    finding_id: str = Field(min_length=1)
    category: Literal[
        "missing_semantic_obligation",
        "unexamined_model_behavior",
        "weak_or_misdirected_assertion",
        "unsupported_issue_projection",
        "possible_false_negative",
        "possible_false_positive",
        "evidence_gap",
    ]
    related_segment_ids: list[str] = Field(default_factory=list)
    related_requirement_ids: list[str] = Field(default_factory=list)
    related_source_fact_ids: list[str] = Field(default_factory=list)
    related_root_ids: list[str] = Field(default_factory=list)
    related_assertion_chain_ids: list[str] = Field(default_factory=list)
    problem: str = Field(min_length=20)
    missed_behavior_risk: str = Field(min_length=20)
    recommended_action: str = Field(min_length=20)
    recommended_tools: list[Literal[
        "query_model",
        "observe_trace",
        "lookup_source_trace",
        "read_fbmcq_guide",
        "register_coverage_plan",
        "revise_assertion",
        "eval_assert",
    ]] = Field(min_length=1)
    pass_criteria: str = Field(min_length=20)
    record_language: str = "zh-CN"

    @model_validator(mode="after")
    def validate_grounded_action(self) -> "CoverageReviewFinding":
        if not any(
            (
                self.related_segment_ids,
                self.related_requirement_ids,
                self.related_source_fact_ids,
                self.related_root_ids,
                self.related_assertion_chain_ids,
            )
        ):
            raise ValueError("coverage review finding must reference a current ledger ID")
        return self


class CoverageReviewVerdict(StrictReviewModel):
    review_kind: Literal["semantic_coverage", "adversarial_falsification"]
    passed: bool
    reviewed_segment_ids: list[str] = Field(default_factory=list)
    reviewed_requirement_ids: list[str] = Field(default_factory=list)
    reviewed_source_fact_ids: list[str] = Field(default_factory=list)
    reviewed_root_ids: list[str] = Field(default_factory=list)
    findings: list[CoverageReviewFinding] = Field(default_factory=list)
    coverage_analysis: str = Field(min_length=50)
    rationale: str = Field(min_length=20)
    record_language: str = "zh-CN"

    @model_validator(mode="after")
    def validate_pass_consistency(self) -> "CoverageReviewVerdict":
        if self.passed and self.findings:
            raise ValueError("passed review cannot contain blocking findings")
        if not self.passed and not self.findings:
            raise ValueError("failed review must provide actionable findings")
        return self
