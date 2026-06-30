#!/usr/bin/env python3
"""Run A1-DT v2 per-paper/per-agent CLI audits.

This runner is intentionally conservative:
- each task launches exactly one external CLI process for exactly one paper;
- prompts are already materialized under prompts/;
- stdout/stderr are captured under logs/;
- final CLI answer is written under results/;
- TASKS.tsv status is updated only after the process exits.
"""
from __future__ import annotations

import argparse
import csv
import os
import shlex
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from threading import Lock

REPO = Path(__file__).resolve().parents[5]
LIB = REPO / "project_1_llm_state_machine_modeling/paper_agent_based_slr/survey_of_surveys"
BATCH = LIB / "audits/a1dt-v2-19x3"
TASKS = BATCH / "TASKS.tsv"
FIELDNAMES = ["slug", "agent", "status", "prompt_path", "result_path", "log_path", "adjudication_path"]
TASKS_LOCK = Lock()


@dataclass
class Task:
    slug: str
    agent: str
    status: str
    prompt_path: str
    result_path: str
    log_path: str
    adjudication_path: str


def load_env() -> dict[str, str]:
    """Load .env through bash source semantics without logging secret values."""
    env = os.environ.copy()
    env_path = REPO / ".env"
    if not env_path.exists():
        return env
    cmd = f"set -a; source {shlex.quote(str(env_path))}; python - <<'PYENV'\nimport os, json\nprint(json.dumps(dict(os.environ)))\nPYENV"
    proc = subprocess.run(["bash", "-lc", cmd], cwd=REPO, text=True, capture_output=True, timeout=30)
    if proc.returncode != 0:
        # Keep existing env but record failure in caller log.
        env["A1DT_ENV_SOURCE_ERROR"] = proc.stderr[-1000:]
        return env
    import json
    loaded = json.loads(proc.stdout)
    env.update({str(k): str(v) for k, v in loaded.items()})
    return env


def read_tasks() -> list[Task]:
    with TASKS.open(encoding="utf-8", newline="") as f:
        return [Task(**row) for row in csv.DictReader(f, delimiter="\t")]


def write_tasks(tasks: list[Task]) -> None:
    tmp = TASKS.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, delimiter="\t")
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.__dict__)
    tmp.replace(TASKS)


def update_status(slug: str, agent: str, status: str) -> None:
    with TASKS_LOCK:
        tasks = read_tasks()
        for t in tasks:
            if t.slug == slug and t.agent == agent:
                t.status = status
        write_tasks(tasks)


def command_for(task: Task, output_file: Path) -> list[str]:
    prompt = str(BATCH / task.prompt_path)
    if task.agent == "codex":
        return [
            "codex", "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "-C", str(REPO),
            "-o", str(output_file),
            "-",
        ]
    if task.agent == "deepseek":
        return [
            "codex-deepseek", "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "-C", str(REPO),
            "-o", str(output_file),
            "-",
        ]
    if task.agent == "claude":
        return [
            "claude", "-p",
            "--dangerously-skip-permissions",
            "--add-dir", str(REPO),
            "--output-format", "text",
        ]
    raise ValueError(task.agent)


def run_one(task: Task, timeout_sec: int, env: dict[str, str]) -> tuple[str, str, int, str]:
    prompt_file = BATCH / task.prompt_path
    result_file = BATCH / task.result_path
    log_file = BATCH / task.log_path
    result_file.parent.mkdir(parents=True, exist_ok=True)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_text = prompt_file.read_text(encoding="utf-8")

    start = time.strftime("%Y-%m-%d %H:%M:%S")
    cmd = command_for(task, result_file)
    log_lines = [
        f"task={task.slug} agent={task.agent}",
        f"start={start}",
        f"cwd={REPO}",
        f"cmd={' '.join(shlex.quote(c) for c in cmd[:-1])} -" if cmd[-1] == "-" else f"cmd={' '.join(shlex.quote(c) for c in cmd)}",
        f"prompt={prompt_file.relative_to(REPO)}",
        f"result={result_file.relative_to(REPO)}",
        f"env_sourced={'.env exists' if (REPO/'.env').exists() else '.env absent'}",
    ]
    if env.get("A1DT_ENV_SOURCE_ERROR"):
        log_lines.append("env_source_error=<redacted; see local runner warning>")
    try:
        if task.agent == "claude":
            proc = subprocess.run(cmd + [prompt_text], cwd=REPO, env=env, text=True, capture_output=True, timeout=timeout_sec)
            if proc.stdout:
                # Claude -p can emit the complete report only to stdout; always overwrite
                # stale summary outputs so result_path remains the auditable artifact.
                result_file.write_text(proc.stdout, encoding="utf-8")
        else:
            proc = subprocess.run(cmd, input=prompt_text, cwd=REPO, env=env, text=True, capture_output=True, timeout=timeout_sec)
        end = time.strftime("%Y-%m-%d %H:%M:%S")
        log_lines += [f"end={end}", f"returncode={proc.returncode}", "--- STDOUT ---", proc.stdout or "", "--- STDERR ---", proc.stderr or ""]
        log_file.write_text("\n".join(log_lines), encoding="utf-8")
        if not result_file.exists() or result_file.stat().st_size == 0:
            # Some CLIs only print stdout; persist it even on nonzero for audit.
            result_file.write_text(proc.stdout or proc.stderr or "", encoding="utf-8")
        status = "completed" if proc.returncode == 0 and result_file.stat().st_size > 0 else "blocked"
        update_status(task.slug, task.agent, status)
        return task.slug, task.agent, proc.returncode, status
    except subprocess.TimeoutExpired as e:
        end = time.strftime("%Y-%m-%d %H:%M:%S")
        log_lines += [f"end={end}", "returncode=timeout", "--- STDOUT ---", e.stdout or "", "--- STDERR ---", e.stderr or ""]
        log_file.write_text("\n".join(log_lines), encoding="utf-8")
        result_file.write_text(f"# BLOCKED: timeout\n\nTask {task.slug} / {task.agent} exceeded {timeout_sec}s.\n", encoding="utf-8")
        update_status(task.slug, task.agent, "blocked")
        return task.slug, task.agent, 124, "blocked"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--agent", choices=["codex", "claude", "deepseek"], help="run only one agent type")
    ap.add_argument("--slug", help="run only one slug")
    ap.add_argument("--only-planned", action="store_true", help="skip completed tasks")
    ap.add_argument("--max-workers", type=int, default=1)
    ap.add_argument("--timeout-sec", type=int, default=1800)
    args = ap.parse_args(argv)
    tasks = read_tasks()
    selected = []
    for t in tasks:
        if args.agent and t.agent != args.agent:
            continue
        if args.slug and t.slug != args.slug:
            continue
        if args.only_planned and t.status == "completed":
            continue
        selected.append(t)
    if not selected:
        print("no tasks selected")
        return 0
    env = load_env()
    print(f"selected {len(selected)} tasks; max_workers={args.max_workers}; timeout={args.timeout_sec}s")
    failures = 0
    with ThreadPoolExecutor(max_workers=args.max_workers) as ex:
        futs = [ex.submit(run_one, t, args.timeout_sec, env) for t in selected]
        for fut in as_completed(futs):
            slug, agent, code, status = fut.result()
            print(f"{slug}\t{agent}\tcode={code}\tstatus={status}")
            if status != "completed":
                failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
