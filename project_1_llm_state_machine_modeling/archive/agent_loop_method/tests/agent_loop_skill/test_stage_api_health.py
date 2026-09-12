"""LG-M1-B agent_loop_skill health tests for stage API docs."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parents[5]
assert (REPO / "project_1_llm_state_machine_modeling").is_dir(), "REPO root detection failed"
SKILL_ROOT = REPO / "project_1_llm_state_machine_modeling" / "archive" / "agent_loop_method" / "agent_loop_skill"
HEALTH = SKILL_ROOT / "health_check.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_skill_docs_recommend_stage_api_not_full_loop_or_symlink_programming() -> None:
    entry = _read(SKILL_ROOT / "AGENT_LOOP_SKILL.md")
    tools = _read(SKILL_ROOT / "tools.md")
    prompts = _read(SKILL_ROOT / "prompts.md")
    stages = _read(SKILL_ROOT / "stages" / "README.md")
    combined = "\n".join([entry, tools, prompts, stages])

    assert "archive.agent_loop_method.stages.api" in combined
    assert "archive.agent_loop_method.stages.sc_control" in combined
    assert "archive.agent_loop_method.stages.sl_prompt_api" in combined
    assert "程序化调用" in combined
    assert "symlink" in stages.lower()
    assert "人类可读" in stages

    # Full-loop mentions are allowed only as boundary / ban language.
    for line in combined.splitlines():
        if "archive.agent_loop_method.loop.run_agent_loop" in line:
            assert any(marker in line for marker in ["不得", "禁止", "不要", "不是", "不调用"]), line


def test_health_check_reports_stage_api_contract() -> None:
    result = subprocess.run(
        [sys.executable, str(HEALTH), "--format", "json"],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    )
    checks = json.loads(result.stdout)
    by_name = {item["name"]: item for item in checks}
    assert "stage_api_contract" in by_name
    assert by_name["stage_api_contract"]["ok"] is True
    assert "archive.agent_loop_method.stages.api" in by_name["stage_api_contract"]["detail"]
