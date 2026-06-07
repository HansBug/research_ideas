"""Skill-facing Pythonic facade for project-1 agent-loop stages.

LG-M1-B provides this module as the stable import surface for Codex / Claude
Code skills and downstream toolbox code that need deterministic SD tools or SL
prompt builders without invoking the full agent loop.  Importing this module is
provider-free by construction: it does not read ``.env``, does not instantiate a
chat client, and does not call the full-loop driver.
"""

from __future__ import annotations

from method.stages.ids import ALL_STAGE_SPECS, STAGE_SPECS_BY_ID, FeedbackSource, StageId, StageKind, StageSpec, StageStatus
from method.stages.sc_control import SC_CONTROL_SCHEMA_VERSION, build_stage_control_summary, canonical_stage_ids, stage_specs_by_kind
from method.stages.sd_context import BuildResult, build_model_from_dsl, update_context_with_build
from method.stages.sd_tools import (
    DEFAULT_WARNING_REPAIR_BUDGET,
    freeze_scenario_set,
    mark_warning_repair_attempt,
    run_sd2_parse,
    run_sd3_semantic,
    run_sd4_design,
    run_sd5a_scenario_coverage,
    run_sd6_sim,
    run_sd8_fix_plan,
    run_sd10_repair_review,
)
from method.stages.sl_prompt_api import (
    build_sl1_initial_modeling_prompt,
    build_sl5_scenario_generation_prompt,
    compact_sl5_design_summary_for_prompt,
    compact_sl5_inspect_for_prompt,
    build_sl7_model_review_prompt,
    compact_sl7_review_input,
    build_sl9_repair_prompt,
    build_sl10_repair_review_prompt,
    build_sl10b_delta_review_prompt,
    parse_sl1_initial_modeling_response,
    parse_sl5_scenario_generation_response,
    parse_sl7_model_review_response,
    parse_sl10_repair_review_response,
    parse_sl10b_delta_review_response,
)

__all__ = [
    "ALL_STAGE_SPECS",
    "STAGE_SPECS_BY_ID",
    "FeedbackSource",
    "StageId",
    "StageKind",
    "StageSpec",
    "StageStatus",
    "BuildResult",
    "DEFAULT_WARNING_REPAIR_BUDGET",
    "build_model_from_dsl",
    "update_context_with_build",
    "SC_CONTROL_SCHEMA_VERSION",
    "build_stage_control_summary",
    "canonical_stage_ids",
    "stage_specs_by_kind",
    "freeze_scenario_set",
    "mark_warning_repair_attempt",
    "run_sd2_parse",
    "run_sd3_semantic",
    "run_sd4_design",
    "run_sd5a_scenario_coverage",
    "run_sd6_sim",
    "run_sd8_fix_plan",
    "run_sd10_repair_review",
    "build_sl1_initial_modeling_prompt",
    "parse_sl1_initial_modeling_response",
    "build_sl5_scenario_generation_prompt",
    "parse_sl5_scenario_generation_response",
    "compact_sl5_design_summary_for_prompt",
    "compact_sl5_inspect_for_prompt",
    "build_sl7_model_review_prompt",
    "compact_sl7_review_input",
    "parse_sl7_model_review_response",
    "build_sl9_repair_prompt",
    "build_sl10_repair_review_prompt",
    "parse_sl10_repair_review_response",
    "build_sl10b_delta_review_prompt",
    "parse_sl10b_delta_review_response",
]
