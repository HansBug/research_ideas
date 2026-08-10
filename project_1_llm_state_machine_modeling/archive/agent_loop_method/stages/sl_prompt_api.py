"""Facade re-export of SL prompt generators; not a standalone prompt implementation.

This module is the LG-M1-B skill-facing API for prompt assembly.  It gathers the
existing ``sl_*_prompt.py`` builders/parsers behind one discoverable import path
while leaving shared implementation utilities in ``sl_prompt_common.py``.
Importing this facade does not call a provider and does not execute the full
agent loop.
"""

from __future__ import annotations

from method.stages.sl10_repair_review_prompt import build_sl10_repair_review_prompt, parse_sl10_repair_review_response
from method.stages.sl_delta_review_prompt import build_sl10b_delta_review_prompt, parse_sl10b_delta_review_response
from method.stages.sl_initial_modeling_prompt import build_sl1_initial_modeling_prompt, parse_sl1_initial_modeling_response
from method.stages.sl_model_review_prompt import build_sl7_model_review_prompt, compact_sl7_review_input, parse_sl7_model_review_response
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl_scenario_generation_prompt import (
    build_sl5_scenario_generation_prompt,
    compact_sl5_design_summary_for_prompt,
    compact_sl5_inspect_for_prompt,
    parse_sl5_scenario_generation_response,
)

__all__ = [
    "build_sl1_initial_modeling_prompt",
    "parse_sl1_initial_modeling_response",
    "build_sl5_scenario_generation_prompt",
    "parse_sl5_scenario_generation_response",
    "compact_sl5_design_summary_for_prompt",
    "compact_sl5_inspect_for_prompt",
    "build_sl7_model_review_prompt",
    "parse_sl7_model_review_response",
    "compact_sl7_review_input",
    "build_sl9_repair_prompt",
    "build_sl10_repair_review_prompt",
    "parse_sl10_repair_review_response",
    "build_sl10b_delta_review_prompt",
    "parse_sl10b_delta_review_response",
]
