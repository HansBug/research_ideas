from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .models import ConversionResult


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def write_json(path: Path, data: dict[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    path.write_text(text, encoding="utf-8")
    return sha256_text(text)


def repo_commit(repo_root: Path) -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo_root, text=True).strip()
    except Exception:
        return "unknown"


def _rel(path: Path | None, repo_root: Path) -> str | None:
    if path is None:
        return None
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def make_example_report(
    *,
    result: ConversionResult,
    example_dir: Path,
    stm_path: Path,
    source_meta_path: Path,
    canonical_output_path: Path | None,
    canonical_output_sha256: str | None,
    loss_ledger_path: Path,
    repo_root: Path,
    run_id: str,
    conversion_command: str,
    created_at: str | None,
    tool_info: dict[str, Any],
) -> dict[str, Any]:
    status_reason_code = f"R3.STATUS.{result.status}"
    return {
        "example_id": result.example_id,
        "seed_id": result.seed_id,
        "source_format": result.source_format,
        "adapter": result.adapter,
        "status": result.status,
        "status_reason_code": status_reason_code,
        "states_count": len(result.states),
        "transitions_count": len(result.transitions),
        "variables_count": len(result.variables),
        "resolved_states_count": int(result.metadata.get("resolved_states_count", len(result.states))),
        "resolved_transitions_count": int(result.metadata.get("resolved_transitions_count", len(result.transitions))),
        "timing_level": result.timing_level,
        "hierarchy_level": result.hierarchy_level,
        "losses_count": len(result.losses),
        "blocking_reason": result.blocking_reason,
        "source_sha256": sha256_file(stm_path),
        "canonical_output_sha256": canonical_output_sha256,
        "canonical_output_path": _rel(canonical_output_path, repo_root),
        "report_version": "r3.conversion_report.v0",
        "run_id": run_id,
        "created_at": created_at or datetime.now(timezone.utc).isoformat(),
        "conversion_command": conversion_command,
        "repo_commit": repo_commit(repo_root),
        "input_version": sha256_file(source_meta_path),
        "schema_version": "r3.canonical_stm.v0",
        "adapter_version": "0.1.0",
        "tool_name": tool_info.get("tool_name"),
        "tool_version": tool_info.get("tool_version"),
        "tool_source_url": tool_info.get("tool_source_url"),
        "tool_invocation_status": tool_info.get("tool_invocation_status"),
        "tool_preflight": tool_info.get("tool_preflight"),
        "source_locator": f"selected_seed_examples/{example_dir.name}/{stm_path.name}",
        "raw_locator": tool_info.get("raw_locator"),
        "source_meta_path": _rel(source_meta_path, repo_root),
        "loss_ledger_path": _rel(loss_ledger_path, repo_root),
        "report_sha256": None,
        "manual_normalization": tool_info.get("manual_normalization", False),
        "manual_edit_allowed": False,
        "manual_edit_ledger_ref": None,
        "eligibility": "r3_smoke_fixture_only_not_main_experiment",
        "diagnostics": result.diagnostics,
    }
