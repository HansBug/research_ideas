from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent
REPO = SKILL_ROOT.parents[3]
HEALTH = SKILL_ROOT / "health_check.py"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_agent_loop_skill_health_check_passes_and_reports_json() -> None:
    result = subprocess.run(
        [sys.executable, str(HEALTH), "--format", "json"],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    )
    checks = json.loads(result.stdout)

    assert checks
    assert {item["name"] for item in checks} >= {
        "entry_symlinks",
        "stage_symlinks_resolve",
        "stage_symlink_strategy",
        "forbidden_top_runner",
        "repair_chain_terms",
        "tools_no_misleading_legacy",
        "e2e_input_grounding",
        "run_agent_loop_mentions_guarded",
    }
    assert all(item["ok"] for item in checks)


def test_agent_loop_skill_stage_symlinks_are_read_only_documented() -> None:
    readme = _read(SKILL_ROOT / "stages" / "README.md")

    assert "只读" in readme
    assert "method/stages/docs" in readme
    assert "FixRequestBatch" in readme
    assert "SL-10(NL + FixLog + local evidence)" in readme
    assert "SD-10.md" in readme
    assert "SL-10B.md" in readme
    assert "不是" in readme

    for path in sorted((SKILL_ROOT / "stages").glob("*.md")):
        if path.name == "README.md":
            continue
        assert path.is_symlink(), f"{path} should remain a symlink"
        assert path.exists(), f"{path} target should resolve"
        assert "method/stages/docs" in str(path.resolve())


def test_agent_loop_skill_docs_close_legacy_repair_wording() -> None:
    tools = _read(SKILL_ROOT / "tools.md")
    prompts = _read(SKILL_ROOT / "prompts.md")
    e2e = _read(SKILL_ROOT / "e2e_ref_model_guide.md")
    entry = _read(SKILL_ROOT / "AGENT_LOOP_SKILL.md")

    assert "PR-E1 runtime 会把它提升为" not in tools
    assert "FixPlan.suggested_fix_hints" not in tools
    assert "PR-E1 已将默认 repair 主链提升为" in tools
    assert "[prompts.md](./prompts.md)" in tools
    assert "FixRequest.suggested_fix_hints" in tools

    for text in [tools, prompts, e2e, entry]:
        assert "FixRequestBatch" in text
        assert "FixLog" in text
        assert "SL-9" in text
        assert "SL-10" in text


def test_agent_loop_skill_e2e_boundaries_are_self_contained() -> None:
    entry = _read(SKILL_ROOT / "AGENT_LOOP_SKILL.md")
    e2e = _read(SKILL_ROOT / "e2e_ref_model_guide.md")

    for text in [entry, e2e]:
        assert "method.loop.run_agent_loop" in text
        assert "PR-D representative runner" in text
        assert "一键 full staged runner" in text
        assert "不得" in text or "禁止" in text

    assert "NL 片段" in e2e
    assert "论文子路径" in e2e
    assert "paper_content.txt" in e2e
    assert "paper.pdf" in e2e
    assert "bibtex.bib" in e2e
