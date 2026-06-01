"""Canonical stage identifiers for the PR-0 agent-loop contract."""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StageKind(str, Enum):
    LLM = "LLM"
    DETERMINISTIC = "deterministic"
    CONTROL = "control"


class StageStatus(str, Enum):
    OK = "ok"
    FAIL = "fail"
    SKIPPED = "skipped"
    ERROR = "error"
    ADVISORY = "advisory"


class FeedbackSource(str, Enum):
    PARSE = "parse"
    SEMANTIC = "semantic"
    DESIGN = "design"
    SIM = "sim"
    JUDGE = "judge"
    MODEL_REVIEW = "model_review"
    REPAIR_REVIEW = "repair_review"


class StageId(str, Enum):
    SC_0_START = "SC-0"
    SL_1_INITIAL_MODELING = "SL-1"
    SD_2_PARSE = "SD-2"
    SD_3_SEMANTIC = "SD-3"
    SD_4_DESIGN = "SD-4"
    SL_5_SCENARIO_GENERATION = "SL-5"
    SD_5A_SCENARIO_COVERAGE = "SD-5A"
    SC_5F_SCENARIO_FREEZE = "SC-5F"
    SD_6_SIM = "SD-6"
    SL_7_MODEL_REVIEW = "SL-7"
    SD_8_FIX_PLAN = "SD-8"
    SL_9_REPAIR = "SL-9"
    SD_10_REPAIR_REVIEW = "SD-10"
    SL_10B_DELTA_REVIEW = "SL-10B"
    SC_11_ACCEPT_CANDIDATE = "SC-11"
    SC_12_EXIT = "SC-12"
    SC_13_TRACE_AUDIT = "SC-13"


@dataclass(frozen=True)
class StageSpec:
    stage_id: str
    kind: StageKind
    name: str
    doc_filename: str
    feedback_source: FeedbackSource | None = None


ALL_STAGE_SPECS: tuple[StageSpec, ...] = (
    StageSpec(StageId.SC_0_START.value, StageKind.CONTROL, "启动入口", "SC-0-start.md"),
    StageSpec(StageId.SL_1_INITIAL_MODELING.value, StageKind.LLM, "初始建模", "SL-1-initial-modeling.md"),
    StageSpec(StageId.SD_2_PARSE.value, StageKind.DETERMINISTIC, "ParseFeedback", "SD-2-parse.md", FeedbackSource.PARSE),
    StageSpec(StageId.SD_3_SEMANTIC.value, StageKind.DETERMINISTIC, "SemanticFeedback", "SD-3-semantic.md", FeedbackSource.SEMANTIC),
    StageSpec(StageId.SD_4_DESIGN.value, StageKind.DETERMINISTIC, "DesignFeedback", "SD-4-design.md", FeedbackSource.DESIGN),
    StageSpec(StageId.SL_5_SCENARIO_GENERATION.value, StageKind.LLM, "场景生成", "SL-5-scenario-generation.md"),
    StageSpec(StageId.SD_5A_SCENARIO_COVERAGE.value, StageKind.DETERMINISTIC, "场景覆盖自检", "SD-5A-scenario-coverage.md"),
    StageSpec(StageId.SC_5F_SCENARIO_FREEZE.value, StageKind.CONTROL, "冻结 ScenarioSet", "SC-5F-scenario-freeze.md"),
    StageSpec(StageId.SD_6_SIM.value, StageKind.DETERMINISTIC, "SimFeedback", "SD-6-sim.md", FeedbackSource.SIM),
    StageSpec(StageId.SL_7_MODEL_REVIEW.value, StageKind.LLM, "轻量模型评审", "SL-7-lightweight-model-review.md", FeedbackSource.MODEL_REVIEW),
    StageSpec(StageId.SD_8_FIX_PLAN.value, StageKind.DETERMINISTIC, "FixPlan", "SD-8-fix-plan.md"),
    StageSpec(StageId.SL_9_REPAIR.value, StageKind.LLM, "修复", "SL-9-repair.md"),
    StageSpec(StageId.SD_10_REPAIR_REVIEW.value, StageKind.DETERMINISTIC, "RepairReview", "SD-10-repair-review.md", FeedbackSource.REPAIR_REVIEW),
    StageSpec(StageId.SL_10B_DELTA_REVIEW.value, StageKind.LLM, "轻量修复评审", "SL-10B-delta-review.md"),
    StageSpec(StageId.SC_11_ACCEPT_CANDIDATE.value, StageKind.CONTROL, "接受 candidate", "SC-11-accept-candidate.md"),
    StageSpec(StageId.SC_12_EXIT.value, StageKind.CONTROL, "收敛退出", "SC-12-exit.md"),
    StageSpec(StageId.SC_13_TRACE_AUDIT.value, StageKind.CONTROL, "Trace/Audit", "SC-13-trace-audit.md"),
)

STAGE_SPECS_BY_ID: dict[str, StageSpec] = {spec.stage_id: spec for spec in ALL_STAGE_SPECS}
FEEDBACK_SOURCE_TO_STAGE_ID: dict[str, str] = {
    spec.feedback_source.value: spec.stage_id
    for spec in ALL_STAGE_SPECS
    if spec.feedback_source is not None
}
