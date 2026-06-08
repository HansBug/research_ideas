"""Thin PR-M3 runner for codex-exec skill experiments.

The runner only handles launch/config/archive/report glue.  It deliberately does
not implement state-machine modeling semantics; the mature agent must read and
use ``agent_loop_skill`` to produce the model and ledgers.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Sequence

if __package__ and __package__.startswith("project_1_llm_state_machine_modeling."):
    _PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

from method.agent_loop_skill.codex_exec_experiment import (  # noqa: E402
    CODEX_EXEC_ENV_KEYS,
    REPO_ROOT,
    M3_AGENT_ARTIFACTS,
    CodexExecCase,
    augment_metadata,
    ensure_machine_audit_artifacts,
    build_codex_prompt,
    build_command_plan,
    initial_manifest,
    load_env_file,
    redact_text,
    redacted_env_snapshot,
    relpath,
    render_run_summary,
    resolve_codex_exec_config,
    secret_values_from_env,
    update_manifest_after_run,
    utc_now_iso,
    codex_exec_cases,
    write_forbidden_call_check,
    write_invalid_placeholders,
    write_json,
    write_redaction_report,
    write_transcript_redacted,
)


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _tee_stream(prefix: str, stream, path: Path, secret_values: dict[str, str]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for raw_line in iter(stream.readline, ""):
            safe = redact_text(raw_line, secret_values)
            f.write(safe)
            f.flush()
            # Keep terminal readable while still showing progress.
            preview = safe.rstrip()
            if len(preview) > 600:
                preview = preview[:600] + " ...<truncated>"
            print(f"[{prefix}] {preview}", flush=True)


def run_one_case(
    *,
    case: CodexExecCase,
    out_root: Path,
    codex_bin: str,
    env_file: Path | None,
    dry_run: bool,
    cli_default_config: str | None,
    cli_extra_config: Sequence[str],
    cli_override_config: Sequence[str],
) -> dict[str, object]:
    file_env = load_env_file(env_file)
    run_env = dict(file_env)
    run_env.update(os.environ)
    secret_values = secret_values_from_env(run_env)
    config_entries = resolve_codex_exec_config(
        file_env=file_env,
        process_env=os.environ,
        cli_default_config=cli_default_config,
        cli_extra_config=cli_extra_config,
        cli_override_config=cli_override_config,
    )

    run_dir = out_root / case.case_key
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "checks").mkdir(exist_ok=True)
    prompt = build_codex_prompt(case, run_dir, out_root.name)
    (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")

    command_plan = build_command_plan(
        codex_bin=codex_bin,
        repo_root=REPO_ROOT,
        last_message_path=run_dir / "last_message.md",
        config_entries=config_entries,
    )
    (run_dir / "command.redacted.txt").write_text(" ".join(command_plan.command_redacted) + "\n", encoding="utf-8")
    write_json(run_dir / "env.redacted.json", redacted_env_snapshot(run_env, file_env.keys()))
    manifest = initial_manifest(
        case=case,
        run_dir=run_dir,
        command_plan=command_plan,
        prompt=prompt,
        file_env_keys=file_env.keys(),
    )
    write_json(run_dir / "run_manifest.json", manifest)

    if dry_run:
        write_invalid_placeholders(run_dir, reason="dry-run: codex exec not launched")
        forbidden = write_forbidden_call_check(run_dir)
        write_transcript_redacted(run_dir, secret_values)
        redaction = write_redaction_report(run_dir, secret_values)
        manifest = update_manifest_after_run(manifest, run_dir=run_dir, started_monotonic=time.monotonic(), exit_code=0, invalid_reason="dry-run")
        manifest["redaction_status"] = "ok" if redaction.get("ok") else "fail"
        write_json(run_dir / "run_manifest.json", manifest)
        augment_metadata(run_dir, manifest)
        completeness = ensure_machine_audit_artifacts(run_dir, manifest)
        manifest["artifact_completeness"] = completeness
        write_json(run_dir / "run_manifest.json", manifest)
        redaction = write_redaction_report(run_dir, secret_values)
        manifest["redaction_status"] = "ok" if redaction.get("ok") else "fail"
        write_json(run_dir / "run_manifest.json", manifest)
        (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
        return {"case_key": case.case_key, "status": "dry-run", "run_dir": relpath(run_dir), "exit_code": 0}

    started = time.monotonic()
    print(f"[runner] start {case.case_key}: {' '.join(command_plan.command_redacted)}", flush=True)
    import subprocess

    stdout_events = run_dir / "codex_events.jsonl"
    stdout_log = run_dir / "codex_stdout.log"
    stderr_log = run_dir / "codex_stderr.log"
    proc = subprocess.Popen(
        command_plan.command,
        cwd=REPO_ROOT,
        env=run_env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
    )
    assert proc.stdin is not None and proc.stdout is not None and proc.stderr is not None
    proc.stdin.write(prompt)
    proc.stdin.close()

    stderr_thread = threading.Thread(target=_tee_stream, args=(f"{case.case_key}:stderr", proc.stderr, stderr_log, secret_values), daemon=True)
    stderr_thread.start()
    with stdout_events.open("w", encoding="utf-8") as events_f, stdout_log.open("w", encoding="utf-8") as stdout_f:
        for raw_line in iter(proc.stdout.readline, ""):
            safe = redact_text(raw_line, secret_values)
            events_f.write(safe)
            stdout_f.write(safe)
            events_f.flush()
            stdout_f.flush()
            preview = safe.rstrip()
            if len(preview) > 600:
                preview = preview[:600] + " ...<truncated>"
            print(f"[{case.case_key}:json] {preview}", flush=True)
    exit_code = proc.wait()
    stderr_thread.join(timeout=5)

    invalid_reason = None
    if exit_code != 0:
        invalid_reason = f"codex exec exited with code {exit_code}"
    if not (run_dir / "final_model.fcstm").exists() and invalid_reason is None:
        invalid_reason = "missing final_model.fcstm"
    if not (run_dir / "report.md").exists() and invalid_reason is None:
        invalid_reason = "missing report.md"
    if not (run_dir / "metadata.json").exists() and invalid_reason is None:
        invalid_reason = "missing metadata.json"
    if invalid_reason:
        write_invalid_placeholders(run_dir, reason=invalid_reason)

    completeness_pre = {name: (run_dir / name).exists() for name in M3_AGENT_ARTIFACTS}
    forbidden = write_forbidden_call_check(run_dir)
    write_transcript_redacted(run_dir, secret_values)
    redaction = write_redaction_report(run_dir, secret_values)
    manifest = update_manifest_after_run(manifest, run_dir=run_dir, started_monotonic=started, exit_code=exit_code, invalid_reason=invalid_reason)
    manifest["redaction_status"] = "ok" if redaction.get("ok") else "fail"
    manifest["forbidden_call_check"] = forbidden
    manifest["artifact_completeness_before_harness_fill"] = completeness_pre
    write_json(run_dir / "run_manifest.json", manifest)
    augment_metadata(run_dir, manifest)
    completeness = ensure_machine_audit_artifacts(run_dir, manifest)
    manifest["artifact_completeness"] = completeness
    write_json(run_dir / "run_manifest.json", manifest)
    # Re-scan after metadata/audit augmentation so hashes/report reflect the final artifact set.
    redaction = write_redaction_report(run_dir, secret_values)
    manifest["redaction_status"] = "ok" if redaction.get("ok") else "fail"
    write_json(run_dir / "run_manifest.json", manifest)
    (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
    print(f"[runner] done {case.case_key}: status={manifest['status']} run_dir={relpath(run_dir)}", flush=True)
    return {"case_key": case.case_key, "status": manifest["status"], "run_dir": relpath(run_dir), "exit_code": exit_code, "invalid_run_reason": invalid_reason}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-set", default="all", choices=["mandatory", "all", "e2-aligned", "mandatory+screening"])
    parser.add_argument("--case-keys", default="", help="comma-separated case keys; default runs all cases in --case-set")
    parser.add_argument("--out-root", default="", help="output root; default runs/codex_exec_skill/pr_m3_<timestamp>")
    parser.add_argument("--codex-bin", default=os.environ.get("CODEX_BIN", shutil.which("codex") or "codex"))
    parser.add_argument("--env-file", default=".env", help="dotenv file to load before process env override; use '' to disable")
    parser.add_argument("--codex-config", default=None, help="optional CLI default config blob")
    parser.add_argument("--codex-extra-config", action="append", default=[], help="additional key=value config blob; repeatable")
    parser.add_argument("--codex-override-config", action="append", default=[], help="highest-precedence key=value config blob; repeatable")
    parser.add_argument("--parallel", type=int, default=1, help="number of codex exec processes to run concurrently")
    parser.add_argument("--dry-run", action="store_true", help="write prompt/manifest without launching codex exec")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    case_keys = _parse_csv(args.case_keys)
    out_root = Path(args.out_root) if args.out_root else REPO_ROOT / "runs" / "codex_exec_skill" / ("pr_m3_" + utc_now_iso().replace(":", "").replace("+", "Z"))
    if not out_root.is_absolute():
        out_root = REPO_ROOT / out_root
    env_file = Path(args.env_file) if args.env_file else None
    if env_file is not None and not env_file.is_absolute():
        env_file = REPO_ROOT / env_file

    cases = codex_exec_cases(args.case_set, case_keys=case_keys or None)
    out_root.mkdir(parents=True, exist_ok=True)
    write_json(
        out_root / "runner_invocation.json",
        {
            "started_at": utc_now_iso(),
            "case_keys": [case.case_key for case in cases],
            "out_root": relpath(out_root),
            "codex_bin": args.codex_bin,
            "env_file_loaded": relpath(env_file) if env_file else None,
            "codex_exec_env_keys": list(CODEX_EXEC_ENV_KEYS),
            "dry_run": args.dry_run,
            "parallel": args.parallel,
        },
    )

    results: list[dict[str, object]] = []
    if args.parallel <= 1 or len(cases) <= 1:
        for case in cases:
            results.append(
                run_one_case(
                    case=case,
                    out_root=out_root,
                    codex_bin=args.codex_bin,
                    env_file=env_file,
                    dry_run=args.dry_run,
                    cli_default_config=args.codex_config,
                    cli_extra_config=args.codex_extra_config,
                    cli_override_config=args.codex_override_config,
                )
            )
    else:
        with ThreadPoolExecutor(max_workers=args.parallel) as executor:
            future_map = {
                executor.submit(
                    run_one_case,
                    case=case,
                    out_root=out_root,
                    codex_bin=args.codex_bin,
                    env_file=env_file,
                    dry_run=args.dry_run,
                    cli_default_config=args.codex_config,
                    cli_extra_config=args.codex_extra_config,
                    cli_override_config=args.codex_override_config,
                ): case
                for case in cases
            }
            for future in as_completed(future_map):
                results.append(future.result())
    summary = {"ended_at": utc_now_iso(), "out_root": relpath(out_root), "results": sorted(results, key=lambda item: str(item["case_key"]))}
    write_json(out_root / "runner_summary.json", summary)
    print("[runner] summary:")
    print(summary)
    return 0 if all(item.get("exit_code") == 0 and item.get("status") != "invalid" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
