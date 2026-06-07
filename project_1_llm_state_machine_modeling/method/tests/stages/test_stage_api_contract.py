"""LG-M1-B stage API contract tests.

These tests lock the skill-facing stage facade without calling the full agent
loop or any real provider.  They intentionally validate import boundaries and
public names rather than model quality.
"""

from __future__ import annotations

import inspect
import os
import subprocess
import sys
from pathlib import Path


def test_stage_api_exports_deterministic_tools_and_prompt_builders_without_provider() -> None:
    from method.stages import api

    expected = {
        "StageId",
        "StageKind",
        "StageStatus",
        "StageSpec",
        "ALL_STAGE_SPECS",
        "STAGE_SPECS_BY_ID",
        "SC_CONTROL_SCHEMA_VERSION",
        "run_sd2_parse",
        "run_sd3_semantic",
        "run_sd4_design",
        "run_sd5a_scenario_coverage",
        "freeze_scenario_set",
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
    }
    assert expected <= set(api.__all__)
    for name in expected:
        assert hasattr(api, name), name

    # The facade must not expose or import full-loop/provider entrypoints.
    assert not hasattr(api, "run_agent_loop")
    assert not hasattr(api, "RealEnvLLMProvider")
    source = inspect.getsource(api)
    assert "method.loop" not in source
    assert "gpt_client" not in source
    assert "load_dotenv" not in source
    assert "LLM_API_KEY" not in source


def test_sc_control_documents_scope_and_exposes_planned_stage_helpers() -> None:
    from method.stages import sc_control

    doc = sc_control.__doc__ or ""
    assert "ids.py" in doc
    assert "api.py" in doc
    assert "no-provider" in doc

    stage_ids = sc_control.canonical_stage_ids()
    assert stage_ids[0] == "SC-0"
    assert "SL-10" in stage_ids
    assert stage_ids[-1] == "SC-13"

    graph = sc_control.build_stage_control_summary()
    assert graph["schema_version"] == "lg-m1-b.stage-control.v1"
    assert graph["stage_ids"] == stage_ids
    assert graph["stage_count"] == len(stage_ids)
    assert graph["llm_stage_ids"]
    assert graph["deterministic_stage_ids"]
    assert graph["control_stage_ids"]


def test_sl_prompt_api_is_facade_not_prompt_implementation() -> None:
    from method.stages import sl_prompt_api

    doc = sl_prompt_api.__doc__ or ""
    assert "facade" in doc.lower()
    assert "sl_prompt_common.py" in doc
    assert "not a standalone prompt implementation" in doc
    assert "build_sl9_repair_prompt" in sl_prompt_api.__all__
    assert not hasattr(sl_prompt_api, "run_sl9_repair_llm")


def test_stage_api_files_do_not_read_env_or_call_full_loop() -> None:
    root = Path("project_1_llm_state_machine_modeling/method/stages")
    for rel in ["api.py", "sc_control.py", "sl_prompt_api.py"]:
        text = (root / rel).read_text(encoding="utf-8")
        assert "run_agent_loop" not in text
        assert "RealEnvLLMProvider" not in text
        assert "gpt_client" not in text
        assert "LLM_API_KEY" not in text
        assert "os.environ" not in text
        assert "method.llm_stages" not in text


def test_stage_api_import_and_sc_summary_work_without_llm_env() -> None:
    env = dict(os.environ)
    env["PYTHONPATH"] = "project_1_llm_state_machine_modeling"
    for key in ["LLM_ENDPOINT", "LLM_API_KEY", "LLM_MODEL"]:
        env.pop(key, None)
    script = (
        "from method.stages import api; "
        "summary = api.build_stage_control_summary(); "
        "assert summary[\"provider_free\"] is True; "
        "assert summary[\"full_loop_free\"] is True; "
        "assert api.SC_CONTROL_SCHEMA_VERSION == summary[\"schema_version\"]"
    )
    subprocess.run([sys.executable, "-c", script], cwd=Path.cwd(), env=env, check=True)
