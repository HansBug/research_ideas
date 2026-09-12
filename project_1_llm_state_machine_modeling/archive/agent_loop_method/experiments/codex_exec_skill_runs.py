"""Thin PR-M3 runner for codex-exec skill experiments.

The runner only handles launch/config/archive/report glue.  It deliberately does
not implement state-machine modeling semantics; the mature agent must read and
use ``agent_loop_skill`` to produce the model and ledgers.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Sequence

if __package__ and __package__.startswith("project_1_llm_state_machine_modeling."):
    _PROJECT_ROOT = Path(__file__).resolve().parents[3]
    if str(_PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(_PROJECT_ROOT))

from archive.agent_loop_method.agent_loop_skill.codex_exec_experiment import (  # noqa: E402
    CODEX_EXEC_ENV_KEYS,
    REPO_ROOT,
    M3_AGENT_ARTIFACTS,
    RUNNER_OWNED_ARTIFACTS,
    codex_json_stream_audit,
    CodexExecCase,
    augment_metadata,
    attach_runner_audit_outputs,
    ensure_machine_audit_artifacts,
    build_codex_prompt,
    build_command_plan,
    git_metadata,
    initial_manifest,
    load_env_file,
    load_json_file,
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
    build_external_codex_exec_case,
)


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def _resolve_repo_path(value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = REPO_ROOT / path
    return path


def _read_required_text(path: Path, *, label: str) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"{label} not found: {path}")
    return path.read_text(encoding="utf-8")


def _cases_from_args(args: argparse.Namespace) -> list[CodexExecCase]:
    """Resolve built-in presets or one external NL-only/NL+paper_dir case."""

    if args.nl_file:
        if args.case_keys:
            raise ValueError("--case-keys is only valid for built-in presets; external input uses --case-key")
        if args.case_set != "all":
            raise ValueError("--case-set is only valid for built-in presets; external input uses --path")
        nl_file = _resolve_repo_path(args.nl_file)
        assert nl_file is not None
        nl = _read_required_text(nl_file, label="--nl-file")
        nl_zh = None
        if args.nl_zh_file:
            nl_zh_file = _resolve_repo_path(args.nl_zh_file)
            assert nl_zh_file is not None
            nl_zh = _read_required_text(nl_zh_file, label="--nl-zh-file")
        paper_dir = _resolve_repo_path(args.paper_dir)
        if paper_dir is not None and not paper_dir.is_dir():
            raise FileNotFoundError(f"--paper-dir not found or not a directory: {paper_dir}")
        source_path = _resolve_repo_path(args.source_path) or paper_dir
        if source_path is not None and not source_path.exists():
            raise FileNotFoundError(f"--source-path not found: {source_path}")
        case_id = args.case_id or nl_file.stem
        return [
            build_external_codex_exec_case(
                case_id=case_id,
                case_key=args.case_key,
                path=args.path,
                title=args.title,
                nl=nl,
                nl_zh=nl_zh,
                source_url=args.source_url or relpath(nl_file),
                paper_dir=paper_dir,
                source_path=source_path,
                selection_rationale=args.selection_rationale,
                variable_participation_note=args.variable_participation_note,
                state_mode_participation_note=args.state_mode_participation_note,
            )
        ]
    external_only_args = [
        args.case_id,
        args.case_key,
        args.title,
        args.nl_zh_file,
        args.paper_dir,
        args.source_path,
        args.source_url,
        args.selection_rationale,
        args.variable_participation_note,
        args.state_mode_participation_note,
    ]
    if any(external_only_args):
        raise ValueError("external case metadata requires --nl-file; built-in presets use --case-set/--case-keys only")
    case_keys = _parse_csv(args.case_keys)
    return codex_exec_cases(args.case_set, case_keys=case_keys or None)


def _external_input_snapshot(args: argparse.Namespace) -> dict[str, object] | None:
    if not args.nl_file:
        return None
    return {
        "case_id": args.case_id or None,
        "case_key": args.case_key or None,
        "path": args.path,
        "title": args.title or None,
        "nl_file": relpath(_resolve_repo_path(args.nl_file) or Path(args.nl_file)),
        "nl_zh_file": relpath(_resolve_repo_path(args.nl_zh_file)) if args.nl_zh_file else None,
        "paper_dir": relpath(_resolve_repo_path(args.paper_dir)) if args.paper_dir else None,
        "source_path": relpath(_resolve_repo_path(args.source_path)) if args.source_path else None,
        "source_url": args.source_url or None,
        "selection_rationale": args.selection_rationale or None,
        "variable_participation_note": args.variable_participation_note or None,
        "state_mode_participation_note": args.state_mode_participation_note or None,
    }


def _case_run_dirs(root: Path) -> list[Path]:
    if (root / "run_manifest.json").is_file():
        return [root]
    return sorted(path.parent for path in root.rglob("run_manifest.json") if path.is_file())


def refresh_existing_run_root(root: Path, *, env_file: Path | None) -> dict[str, object]:
    """Deterministically refresh runner-owned audit/provenance for existing runs.

    This does not re-launch ``codex exec`` and does not rewrite producer-owned
    model/report/ledger content.  It is intended for post-hoc audit-tool
    upgrades such as PR #79's structured-event marker scanner fix.
    """

    if not root.exists():
        raise FileNotFoundError(f"--refresh-run-root does not exist: {root}")
    file_env = load_env_file(env_file)
    run_env = dict(file_env)
    run_env.update(os.environ)
    secret_values = secret_values_from_env(run_env)
    audit_git = git_metadata()
    run_dirs = _case_run_dirs(root)
    results: list[dict[str, object]] = []
    for run_dir in run_dirs:
        manifest_path = run_dir / "run_manifest.json"
        manifest = load_json_file(manifest_path)
        if not manifest or "parse_error" in manifest:
            raise ValueError(f"cannot refresh invalid manifest: {manifest_path}")
        event_audit = codex_json_stream_audit(run_dir / "codex_events.jsonl")
        write_json(run_dir / "checks" / "codex_json_stream_audit.json", event_audit)
        forbidden = write_forbidden_call_check(run_dir)
        write_transcript_redacted(run_dir, secret_values)
        augment_metadata(run_dir, manifest)
        completeness = ensure_machine_audit_artifacts(run_dir, manifest)
        manifest["artifact_completeness"] = completeness
        redaction = write_redaction_report(run_dir, secret_values)
        manifest = attach_runner_audit_outputs(
            run_dir,
            manifest,
            event_audit=event_audit,
            forbidden_check=forbidden,
            redaction_report=redaction,
            provenance_mode="deterministic_refresh_existing_run",
            provenance_note=(
                "Existing codex exec event/model artifacts were not regenerated; "
                "runner-owned audit/provenance/normalized summary were refreshed deterministically."
            ),
            audit_git=audit_git,
        )
        write_json(manifest_path, manifest)
        (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
        # Re-run redaction after run_summary and manifest have been rewritten.
        redaction = write_redaction_report(run_dir, secret_values)
        manifest = attach_runner_audit_outputs(
            run_dir,
            manifest,
            event_audit=event_audit,
            forbidden_check=forbidden,
            redaction_report=redaction,
            provenance_mode="deterministic_refresh_existing_run",
            provenance_note=(
                "Existing codex exec event/model artifacts were not regenerated; "
                "runner-owned audit/provenance/normalized summary were refreshed deterministically."
            ),
            audit_git=audit_git,
        )
        write_json(manifest_path, manifest)
        (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
        results.append(
            {
                "case_key": (manifest.get("case") or {}).get("case_key") if isinstance(manifest.get("case"), dict) else run_dir.name,
                "run_dir": relpath(run_dir),
                "event_audit_ok": event_audit.get("ok"),
                "redaction_ok": redaction.get("ok"),
                "forbidden_runner_used": forbidden.get("forbidden_runner_used"),
                "producer_commit": ((manifest.get("runner_audit_provenance") or {}).get("producer_run_git") or {}).get("commit")
                if isinstance(manifest.get("runner_audit_provenance"), dict)
                and isinstance((manifest.get("runner_audit_provenance") or {}).get("producer_run_git"), dict)
                else None,
                "audit_commit": audit_git.get("commit"),
            }
        )
    summary = {
        "ended_at": utc_now_iso(),
        "root": relpath(root),
        "mode": "deterministic_refresh_existing_run",
        "audit_git": audit_git,
        "results": results,
    }
    write_json(root / "refresh_summary.json", summary)
    return summary


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
    capture_dir = run_dir / "_runner_capture"
    capture_dir.mkdir(parents=True, exist_ok=True)

    prompt = build_codex_prompt(case, run_dir, out_root.name)
    env_snapshot = redacted_env_snapshot(run_env, file_env.keys())

    command_plan = build_command_plan(
        codex_bin=codex_bin,
        repo_root=REPO_ROOT,
        last_message_path=run_dir / "last_message.md",
        config_entries=config_entries,
    )
    command_redacted_text = " ".join(command_plan.command_redacted) + "\n"
    manifest = initial_manifest(
        case=case,
        run_dir=run_dir,
        command_plan=command_plan,
        prompt=prompt,
        file_env_keys=file_env.keys(),
    )

    def _write_runner_owned_initial() -> None:
        (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        (run_dir / "command.redacted.txt").write_text(command_redacted_text, encoding="utf-8")
        write_json(run_dir / "env.redacted.json", env_snapshot)
        write_json(run_dir / "run_manifest.json", manifest)

    def _restore_runner_owned_static() -> None:
        # Mature agents may accidentally overwrite these files while assembling
        # their own audit package.  The runner is the authority for launch
        # prompt/config/command/manifest, so it rewrites them after the child
        # process exits.  This prevents attached-session placeholders from
        # masquerading as codex-exec evidence.
        (run_dir / "prompt.md").write_text(prompt, encoding="utf-8")
        (run_dir / "command.redacted.txt").write_text(command_redacted_text, encoding="utf-8")
        write_json(run_dir / "env.redacted.json", env_snapshot)

    _write_runner_owned_initial()

    if dry_run:
        write_invalid_placeholders(run_dir, reason="dry-run: codex exec not launched")
        _restore_runner_owned_static()
        (run_dir / "codex_events.jsonl").write_text("", encoding="utf-8")
        (run_dir / "codex_stdout.log").write_text("", encoding="utf-8")
        (run_dir / "codex_stderr.log").write_text("", encoding="utf-8")
        event_audit = codex_json_stream_audit(run_dir / "codex_events.jsonl")
        write_json(run_dir / "checks" / "codex_json_stream_audit.json", event_audit)
        forbidden = write_forbidden_call_check(run_dir)
        write_transcript_redacted(run_dir, secret_values)
        redaction = write_redaction_report(run_dir, secret_values)
        manifest = update_manifest_after_run(manifest, run_dir=run_dir, started_monotonic=time.monotonic(), exit_code=0, invalid_reason="dry-run")
        manifest = attach_runner_audit_outputs(
            run_dir,
            manifest,
            event_audit=event_audit,
            forbidden_check=forbidden,
            redaction_report=redaction,
            provenance_mode="dry_run_initial_audit",
        )
        write_json(run_dir / "run_manifest.json", manifest)
        augment_metadata(run_dir, manifest)
        completeness = ensure_machine_audit_artifacts(run_dir, manifest)
        manifest["artifact_completeness"] = completeness
        redaction = write_redaction_report(run_dir, secret_values)
        manifest = attach_runner_audit_outputs(
            run_dir,
            manifest,
            event_audit=event_audit,
            forbidden_check=forbidden,
            redaction_report=redaction,
            provenance_mode="dry_run_final_audit",
        )
        write_json(run_dir / "run_manifest.json", manifest)
        (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
        return {"case_key": case.case_key, "status": "dry-run", "run_dir": relpath(run_dir), "exit_code": 0}

    started = time.monotonic()
    print(f"[runner] start {case.case_key}: {' '.join(command_plan.command_redacted)}", flush=True)
    import subprocess

    stdout_events_capture = capture_dir / "codex_events.jsonl"
    stdout_log_capture = capture_dir / "codex_stdout.log"
    stderr_log_capture = capture_dir / "codex_stderr.log"
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

    stderr_thread = threading.Thread(target=_tee_stream, args=(f"{case.case_key}:stderr", proc.stderr, stderr_log_capture, secret_values), daemon=True)
    stderr_thread.start()
    with stdout_events_capture.open("w", encoding="utf-8") as events_f, stdout_log_capture.open("w", encoding="utf-8") as stdout_f:
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

    # Reassert runner-owned evidence after the child process exits.  Official
    # codex JSON/stdout/stderr files are copied from the private capture dir so
    # producer code cannot replace them with hand-written placeholders.
    _restore_runner_owned_static()
    shutil.copyfile(stdout_events_capture, run_dir / "codex_events.jsonl")
    shutil.copyfile(stdout_log_capture, run_dir / "codex_stdout.log")
    shutil.copyfile(stderr_log_capture, run_dir / "codex_stderr.log")
    shutil.rmtree(capture_dir, ignore_errors=True)

    event_audit = codex_json_stream_audit(run_dir / "codex_events.jsonl")
    write_json(run_dir / "checks" / "codex_json_stream_audit.json", event_audit)

    invalid_reason = None
    if exit_code != 0:
        invalid_reason = f"codex exec exited with code {exit_code}"
    if not event_audit.get("ok") and invalid_reason is None:
        invalid_reason = f"codex_json_stream_invalid:{event_audit.get('reason')}"
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
    manifest = attach_runner_audit_outputs(
        run_dir,
        manifest,
        event_audit=event_audit,
        forbidden_check=forbidden,
        redaction_report=redaction,
        provenance_mode="initial_post_exec_audit",
    )
    manifest["artifact_completeness_before_harness_fill"] = completeness_pre
    write_json(run_dir / "run_manifest.json", manifest)
    augment_metadata(run_dir, manifest)
    completeness = ensure_machine_audit_artifacts(run_dir, manifest)
    manifest["artifact_completeness"] = completeness
    # Re-scan after metadata/audit augmentation so hashes/report reflect the final artifact set.
    redaction = write_redaction_report(run_dir, secret_values)
    manifest = attach_runner_audit_outputs(
        run_dir,
        manifest,
        event_audit=event_audit,
        forbidden_check=forbidden,
        redaction_report=redaction,
        provenance_mode="final_post_exec_audit",
    )
    write_json(run_dir / "run_manifest.json", manifest)
    (run_dir / "run_summary.md").write_text(render_run_summary(run_dir, manifest, forbidden, redaction), encoding="utf-8")
    print(f"[runner] done {case.case_key}: status={manifest['status']} run_dir={relpath(run_dir)}", flush=True)
    return {"case_key": case.case_key, "status": manifest["status"], "run_dir": relpath(run_dir), "exit_code": exit_code, "invalid_run_reason": invalid_reason}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-set", default="all", choices=["mandatory", "all", "e2-aligned", "mandatory+screening"])
    parser.add_argument("--case-keys", default="", help="comma-separated case keys; default runs all cases in --case-set")
    parser.add_argument("--case-id", default="", help="external case id; requires --nl-file")
    parser.add_argument("--case-key", default="", help="external run directory key; requires --nl-file")
    parser.add_argument("--path", default="path1", choices=["path1", "path2"], help="external input path label; requires --nl-file")
    parser.add_argument("--title", default="", help="external case title; requires --nl-file")
    parser.add_argument("--nl-file", default="", help="external NL input file for NL-only / NL+paper_dir runs")
    parser.add_argument("--nl-zh-file", default="", help="optional Chinese NL translation file for external input")
    parser.add_argument("--paper-dir", default="", help="optional paper directory for NL+paper_dir external input")
    parser.add_argument("--source-path", default="", help="optional source path override for external input")
    parser.add_argument("--source-url", default="", help="optional source URL/label for external input")
    parser.add_argument("--selection-rationale", default="", help="optional external input selection rationale")
    parser.add_argument("--variable-participation-note", default="", help="optional variable participation note")
    parser.add_argument("--state-mode-participation-note", default="", help="optional state/mode participation note")
    parser.add_argument("--out-root", default="", help="output root; default runs/codex_exec_skill/pr_m3_<timestamp>")
    parser.add_argument("--codex-bin", default=os.environ.get("CODEX_BIN", shutil.which("codex") or "codex"))
    parser.add_argument("--env-file", default=".env", help="dotenv file to load before process env override; use '' to disable")
    parser.add_argument("--codex-config", default=None, help="optional CLI default config blob")
    parser.add_argument("--codex-extra-config", action="append", default=[], help="additional key=value config blob; repeatable")
    parser.add_argument("--codex-override-config", action="append", default=[], help="highest-precedence key=value config blob; repeatable")
    parser.add_argument("--parallel", type=int, default=1, help="number of codex exec processes to run concurrently")
    parser.add_argument("--dry-run", action="store_true", help="write prompt/manifest without launching codex exec")
    parser.add_argument("--refresh-run-root", default="", help="deterministically refresh runner-owned audit/provenance for an existing run root")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    env_file = Path(args.env_file) if args.env_file else None
    if env_file is not None and not env_file.is_absolute():
        env_file = REPO_ROOT / env_file

    if args.refresh_run_root:
        root = _resolve_repo_path(args.refresh_run_root)
        assert root is not None
        summary = refresh_existing_run_root(root, env_file=env_file)
        print("[runner] refresh summary:")
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return 0 if all(item.get("event_audit_ok") and item.get("redaction_ok") for item in summary["results"]) else 1

    out_root = Path(args.out_root) if args.out_root else REPO_ROOT / "runs" / "codex_exec_skill" / ("pr_m3_" + utc_now_iso().replace(":", "").replace("+", "Z"))
    if not out_root.is_absolute():
        out_root = REPO_ROOT / out_root

    cases = _cases_from_args(args)
    external_input = _external_input_snapshot(args)
    out_root.mkdir(parents=True, exist_ok=True)
    write_json(
        out_root / "runner_invocation.json",
        {
            "started_at": utc_now_iso(),
            "input_mode": "external" if external_input else "builtin",
            "external_input": external_input,
            "case_set": args.case_set if not external_input else None,
            "case_keys_requested": _parse_csv(args.case_keys) if not external_input else [],
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
