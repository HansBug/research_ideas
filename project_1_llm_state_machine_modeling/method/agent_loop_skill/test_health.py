from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parent
REPO = SKILL_ROOT.parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
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
        "pr_e1_design_residue",
        "no_case_specific_optimization_policy",
        "e2e_input_grounding",
        "run_agent_loop_mentions_guarded",
        "codex_exec_experiment_contract",
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



def test_agent_loop_skill_tracks_pr_e1_design_residue() -> None:
    entry = _read(SKILL_ROOT / "AGENT_LOOP_SKILL.md")
    e2e = _read(SKILL_ROOT / "e2e_ref_model_guide.md")
    stages = _read(SKILL_ROOT / "stages" / "README.md")
    combined = "\n".join([entry, e2e, stages])

    for term in [
        "FixRequestBatch",
        "FixLog",
        "waiver",
        "rework",
        "SL-10(NL + FixLog + local evidence)",
        "diagnostic_hot_start",
        "SD-6",
        "NFRR",
    ]:
        assert term in combined

    assert "SD-10" in combined
    assert "SL-10B" in combined
    assert "不是默认主链" in combined or "不是" in combined
    assert "ABS" in combined and "Elevator" in combined and "CARA" in combined and "LNG" in combined
    assert "特判" in combined


def test_agent_loop_skill_codex_exec_experiment_contract() -> None:
    entry = _read(SKILL_ROOT / "AGENT_LOOP_SKILL.md")
    guide = _read(SKILL_ROOT / "codex_exec_experiment_guide.md")
    helper = _read(SKILL_ROOT / "codex_exec_experiment.py")

    assert "codex_exec_experiment_guide.md" in entry
    assert "CODEX_EXEC_DEFAULT_CONFIG=model_provider=airouter" in guide
    assert "codex exec --json" in guide
    assert "不得使用 `--ephemeral`" in guide
    for term in [
        "run_manifest.json",
        "codex_events.jsonl",
        "actual_file_reads.json",
        "tool_stage_check_ledger.json",
        "repair_ledger.json",
        "nfrr_report.json",
        "forbidden_call_check.json",
        "redaction_report.json",
        "report.md",
        "run_summary.md",
    ]:
        assert term in guide
    assert "TRACKED_DEFAULT_CODEX_EXEC_CONFIG" in helper
    assert "model_provider=airouter" in helper
    assert "codex_exec_cases" in helper


def test_codex_exec_forbidden_call_scan_ignores_doc_mentions_but_flags_executable_calls(tmp_path) -> None:
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import write_forbidden_call_check

    run_dir = tmp_path / "run"
    run_dir.mkdir()
    event_file = run_dir / "codex_events.jsonl"
    # First command reads documentation whose output mentions the forbidden API;
    # this must not count as actual E1 runner use.  Second command is a real
    # executable import/call and must be flagged.
    event_file.write_text(
        "\n".join(
            [
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "type": "command_execution",
                            "command": "/bin/bash -lc \"sed -n '1,20p' project_1_llm_state_machine_modeling/method/agent_loop_skill/SKILL.md\"",
                            "aggregated_output": "禁止调用 method.loop.run_agent_loop(...)，这里只是文档约束。",
                        },
                    },
                    ensure_ascii=False,
                ),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "type": "command_execution",
                            "command": "/bin/bash -lc \"python - <<'PY'\nfrom method.loop import run_agent_loop\nrun_agent_loop()\nPY\"",
                            "aggregated_output": "",
                        },
                    },
                    ensure_ascii=False,
                ),
            ]
        ),
        encoding="utf-8",
    )

    payload = write_forbidden_call_check(run_dir)

    assert payload["forbidden_runner_used"] is True
    assert len(payload["suspicious_tool_lines"]) == 1
    assert payload["suspicious_tool_lines"][0]["line"] == 2


def test_codex_exec_json_stream_audit_rejects_attached_runtime_note(tmp_path) -> None:
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import codex_json_stream_audit

    events = tmp_path / "codex_events.jsonl"
    events.write_text(
        json.dumps(
            {
                "type": "attached_runtime_note",
                "message": "No standalone codex exec --json event stream was available",
            }
        )
        + "\n",
        encoding="utf-8",
    )

    payload = codex_json_stream_audit(events)

    assert payload["ok"] is False
    assert payload["reason"] == "attached_or_non_exec_runtime_marker_present"



def test_codex_exec_json_stream_audit_ignores_marker_text_inside_tool_output(tmp_path) -> None:
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import codex_json_stream_audit

    events = tmp_path / "codex_events.jsonl"
    events.write_text(
        "\n".join(
            [
                json.dumps({"type": "thread.started"}),
                json.dumps({"type": "turn.started"}),
                json.dumps(
                    {
                        "type": "item.completed",
                        "item": {
                            "type": "command_execution",
                            "command": "rg attached_runtime_note project_1_llm_state_machine_modeling",
                            "aggregated_output": "def test_codex_exec_json_stream_audit_rejects_attached_runtime_note(tmp_path): ...",
                        },
                    }
                ),
                json.dumps({"type": "turn.completed"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    payload = codex_json_stream_audit(events)

    assert payload["ok"] is True
    assert payload["reason"] is None
    assert payload["disallowed_hits"] == []


def test_codex_exec_json_stream_audit_accepts_core_exec_events(tmp_path) -> None:
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import codex_json_stream_audit

    events = tmp_path / "codex_events.jsonl"
    events.write_text(
        "\n".join(
            [
                json.dumps({"type": "thread.started"}),
                json.dumps({"type": "turn.started"}),
                json.dumps({"type": "item.completed", "item": {"type": "agent_message", "text": "ok"}}),
                json.dumps({"type": "turn.completed"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    payload = codex_json_stream_audit(events)

    assert payload["ok"] is True
    assert payload["reason"] is None
    assert payload["type_counts"]["thread.started"] == 1


def test_codex_exec_prompt_marks_runner_owned_artifacts_as_harness_owned() -> None:
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import build_codex_prompt, codex_exec_cases

    prompt = build_codex_prompt(codex_exec_cases("all", case_keys=["path1_abs"])[0], Path("runs/tmp/path1_abs"), "tmp")

    assert "runner-owned" in prompt
    assert "不得创建、覆盖或修改" in prompt
    for name in [
        "codex_events.jsonl",
        "command.redacted.txt",
        "env.redacted.json",
        "run_manifest.json",
        "forbidden_call_check.json",
        "redaction_report.json",
        "run_summary.md",
    ]:
        assert name in prompt


def test_codex_exec_runner_rewrites_runner_owned_artifacts_after_child_overwrite(tmp_path) -> None:
    from project_1_llm_state_machine_modeling.method.experiments.codex_exec_skill_runs import run_one_case
    from project_1_llm_state_machine_modeling.method.agent_loop_skill.codex_exec_experiment import codex_exec_cases

    fake_codex = tmp_path / "fake_codex"
    fake_codex.write_text(
        f"#!{sys.executable}\n"
        + """
from __future__ import annotations
import json
import re
import sys
from pathlib import Path

# Behave like a tiny `codex exec --json` executable: ignore argv, read prompt
# from stdin, write producer artifacts, then emit JSONL events to stdout.
prompt = sys.stdin.read()
match = re.search(r"请把所有产物写入：`([^`]+)`", prompt)
if not match:
    raise SystemExit("run_dir not found in prompt")
out = Path(match.group(1))
out.mkdir(parents=True, exist_ok=True)
# Simulate a misbehaving mature agent that tries to overwrite runner-owned files.
(out / "codex_events.jsonl").write_text('{"type":"attached_runtime_note"}\\n', encoding="utf-8")
(out / "command.redacted.txt").write_text("attached-tmux-runtime\\n", encoding="utf-8")
(out / "env.redacted.json").write_text(json.dumps({"env_read": False}), encoding="utf-8")
(out / "run_manifest.json").write_text(json.dumps({"status": "fake"}), encoding="utf-8")
(out / "final_model.fcstm").write_text("state S { [*] -> A; state A; }\\n", encoding="utf-8")
(out / "report.md").write_text("# fake report\\n", encoding="utf-8")
(out / "metadata.json").write_text(json.dumps({"status": "fake-success"}), encoding="utf-8")
(out / "actual_file_reads.json").write_text("[]", encoding="utf-8")
(out / "tool_stage_check_ledger.json").write_text(json.dumps({"checks": {}}), encoding="utf-8")
(out / "repair_ledger.json").write_text("[]", encoding="utf-8")
(out / "nfrr_report.json").write_text(json.dumps({"claim": {"allowed_use": "test"}}), encoding="utf-8")
for event in [
    {"type": "thread.started"},
    {"type": "turn.started"},
    {"type": "item.completed", "item": {"type": "agent_message", "text": "ok"}},
    {"type": "turn.completed"},
]:
    print(json.dumps(event), flush=True)
""".lstrip(),
        encoding="utf-8",
    )
    fake_codex.chmod(0o755)

    result = run_one_case(
        case=codex_exec_cases("all", case_keys=["path1_abs"])[0],
        out_root=tmp_path / "runs",
        codex_bin=str(fake_codex),
        env_file=None,
        dry_run=False,
        cli_default_config=None,
        cli_extra_config=[],
        cli_override_config=[f"model={fake_codex}"],
    )

    run_dir = Path(result["run_dir"])
    events = (run_dir / "codex_events.jsonl").read_text(encoding="utf-8")
    command = (run_dir / "command.redacted.txt").read_text(encoding="utf-8")
    env = json.loads((run_dir / "env.redacted.json").read_text(encoding="utf-8"))
    manifest = json.loads((run_dir / "run_manifest.json").read_text(encoding="utf-8"))

    assert "attached_runtime_note" not in events
    assert "thread.started" in events
    assert "attached-tmux-runtime" not in command
    assert "exec --json" in command
    assert "file_env_keys_loaded" in env
    assert manifest["status"] == "completed"
    assert manifest["codex_json_stream_audit"]["ok"] is True
