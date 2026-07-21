from __future__ import annotations

import re

from pydantic import BaseModel, ConfigDict, Field, model_validator
from typing_extensions import Literal

from .tool_reason import EvalAssertInput
from .coverage import CoveragePlan
from .tools import (
    LookupSourceTraceInput,
    ObserveTraceInput,
    QueryModelInput,
    ReadGuideInput,
)


class StrictReviewModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


CoverageReviewToolName = Literal[
    "query_model",
    "observe_trace",
    "lookup_source_trace",
    "read_fbmcq_guide",
    "register_coverage_plan",
    "revise_assertion",
    "eval_assert",
]


class RegisterCoveragePlanArguments(StrictReviewModel):
    plan: CoveragePlan
    reason: str = Field(min_length=1)


class ReviseAssertionArguments(StrictReviewModel):
    assertion_chain_id: str = Field(min_length=1)
    assert_: str = Field(alias="assert", min_length=1)
    reason: str = Field(min_length=1)


class CoverageImprovementStep(StrictReviewModel):
    tool: CoverageReviewToolName
    related_ids: list[str] = Field(min_length=1)
    objective: str = Field(min_length=20)
    suggested_arguments: dict[str, object] = Field(
        description=(
            "Tool-specific argument template. It must contain the minimum keys "
            "needed to make the proposed coverage action concrete."
        ),
    )
    expected_observation: str = Field(
        min_length=20,
        description="Observable model/ledger evidence this step must produce.",
    )

    @model_validator(mode="after")
    def validate_specificity(self) -> "CoverageImprovementStep":
        argument_model = {
            "query_model": QueryModelInput,
            "observe_trace": ObserveTraceInput,
            "lookup_source_trace": LookupSourceTraceInput,
            "read_fbmcq_guide": ReadGuideInput,
            "register_coverage_plan": RegisterCoveragePlanArguments,
            "revise_assertion": ReviseAssertionArguments,
            "eval_assert": EvalAssertInput,
        }[self.tool]
        try:
            argument_model.model_validate(self.suggested_arguments)
        except ValueError as exc:
            raise ValueError(
                f"invalid suggested_arguments for {self.tool}: {exc}"
            ) from exc
        observable = re.compile(
            r"(?:\b(?:true|false|terminal|accepted|completed|inconclusive|"
            r"matched_items|total_matches|exact_matches|untraceable|assertion|"
            r"transition|state|event|guard|effect|trace|record)\b|"
            r"返回|终态|接受|完成|不确定|匹配项|总数|精确映射|不可追溯|断言|迁移|"
            r"状态|事件|守卫|效应|轨迹|记录)",
            re.I,
        )
        if not observable.search(self.expected_observation):
            raise ValueError(
                "expected_observation must name a mechanically observable result"
            )
        return self


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
        "anti_gaming_risk",
        "reviewer_infrastructure_retry",
    ]
    related_segment_ids: list[str] = Field(default_factory=list)
    related_requirement_ids: list[str] = Field(default_factory=list)
    related_source_fact_ids: list[str] = Field(default_factory=list)
    related_root_ids: list[str] = Field(default_factory=list)
    related_assertion_chain_ids: list[str] = Field(default_factory=list)
    problem: str = Field(
        min_length=20,
        description="Evidence-grounded review finding, not a generic opinion.",
    )
    missed_behavior_risk: str = Field(
        min_length=20,
        description="Concrete false-negative or false-positive risk if left unresolved.",
    )
    coverage_dimensions: list[
        Literal[
            "nl_semantics",
            "model_behavior",
            "source_trace_grounding",
            "assertion_strength",
            "issue_projection_evidence",
            "anti_gaming",
            "reviewer_infrastructure",
        ]
    ] = Field(
        min_length=1,
        description=(
            "New coverage dimension(s) the main Agent must add or re-check before "
            "requesting another review. Use anti_gaming for sentinel variables, "
            "hard-coded candidate names, or filtered-cardinality padding."
        ),
    )
    recommended_action: str = Field(
        min_length=20,
        description=(
            "Executable next checks or assertion changes, including what additional "
            "behavior, path, condition, or evidence dimension they will cover. The "
            "action must literally name at least one entry from recommended_tools "
            "and at least one related ledger ID, be performable with those tools, "
            "and must not ask the Agent to edit Controller projection state directly."
        ),
    )
    recommended_tools: list[CoverageReviewToolName] = Field(min_length=1)
    recommended_steps: list[CoverageImprovementStep] = Field(
        min_length=1,
        description=(
            "Ordered executable coverage-improvement steps. Every recommended tool "
            "must have a step bound to current related ledger IDs."
        ),
    )
    pass_criteria: str = Field(
        min_length=20,
        description=(
            "Observable ledger/model criteria proving that the coverage gap is "
            "closed; generic statements that review should pass are invalid."
        ),
    )
    record_language: str = "zh-CN"

    @model_validator(mode="after")
    def validate_grounded_action(self) -> "CoverageReviewFinding":
        """Reject non-executable or method-boundary-breaking reviewer advice.

        Coverage reviewers are allowed to fail the gate, but their findings must
        be repairable by the current Discover Agent's tools.  The schema therefore
        rejects three classes observed in real runs: using FBMCQ as a natural
        language oracle, asking the Agent to mutate Controller projection labels
        directly, and strengthening the frozen NL into only/every-state/future
        obligations that were not present in the input.
        """

        if not any(
            (
                self.related_segment_ids,
                self.related_requirement_ids,
                self.related_source_fact_ids,
                self.related_root_ids,
                self.related_assertion_chain_ids,
            )
        ):
            raise ValueError(
                "coverage review finding must reference a current ledger ID"
            )

        action_text = "\n".join([self.recommended_action, self.pass_criteria]).lower()

        if (
            "read_fbmcq_guide" in self.recommended_tools
            and re.search(r"(?:interpret|clarif|explain|语义澄清|解释)", action_text)
            and re.search(r"(?:\bnl\b|natural language|自然语言|原文)", action_text)
        ):
            raise ValueError(
                "FBMCQ/read_fbmcq_guide cannot be recommended as a natural-language interpreter"
            )

        recommendation_text = "\n".join(
            [
                action_text,
                *(
                    "\n".join(
                        [
                            step.objective,
                            str(step.suggested_arguments),
                            step.expected_observation,
                        ]
                    ).lower()
                    for step in self.recommended_steps
                ),
            ]
        )
        protected_field = re.search(r"runtime_issue_assessment", recommendation_text)
        projection_state_write = re.search(
            r"(?:issue|root|controller)[-_ ]?projection", recommendation_text
        ) and re.search(
            r"(?:confirmed|ok|false_positive|model_abstraction_gap)",
            recommendation_text,
        )
        if protected_field or projection_state_write:
            raise ValueError(
                "reviewer action must not ask the Agent to mutate Controller projection state directly"
            )

        if not any(
            re.search(rf"\b{re.escape(tool)}\b", self.recommended_action)
            for tool in self.recommended_tools
        ):
            raise ValueError(
                "recommended_action must name at least one recommended tool"
            )

        related_ids = [
            *self.related_segment_ids,
            *self.related_requirement_ids,
            *self.related_source_fact_ids,
            *self.related_root_ids,
            *self.related_assertion_chain_ids,
        ]
        if not any(item in self.recommended_action for item in related_ids):
            raise ValueError(
                "recommended_action must name at least one related ledger ID"
            )

        step_tools = {step.tool for step in self.recommended_steps}
        if step_tools != set(self.recommended_tools):
            raise ValueError(
                "recommended_steps must cover exactly every recommended tool"
            )
        known_related_ids = set(related_ids)
        for step in self.recommended_steps:
            if not set(step.related_ids) <= known_related_ids:
                raise ValueError(
                    "recommended step related_ids must belong to the finding"
                )

        observable_criteria = re.compile(
            r"(?:\b(?:true|false|terminal|accepted|returns?|missing|unknown|"
            r"segment|requirement|sourcefact|root|assertion|trace|transition|"
            r"state|event|variable|guard|effect|mapping|record|id)\b|"
            r"返回|等于|不存在|枚举|断言|迁移|状态|事件|变量|守卫|效应|映射|"
            r"轨迹|台账|闭合|终态|记录|编号)",
            re.I,
        )
        if not observable_criteria.search(self.pass_criteria):
            raise ValueError(
                "pass_criteria must name an observable ledger or model outcome"
            )

        if (
            self.category == "anti_gaming_risk"
            and "anti_gaming" not in self.coverage_dimensions
        ):
            raise ValueError(
                "anti_gaming_risk findings must include anti_gaming coverage_dimensions"
            )
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
