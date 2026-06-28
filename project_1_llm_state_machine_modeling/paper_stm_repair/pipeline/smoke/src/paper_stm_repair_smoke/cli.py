from __future__ import annotations

import argparse
import hashlib
import json
import re
import signal
import tempfile
import threading
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


def repo_root_from_file() -> Path:
    cur = Path(__file__).resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = repo_root_from_file()
PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair"
PIPELINE_ROOT = PAPER_ROOT / "pipeline"
SMOKE_ROOT = PIPELINE_ROOT / "smoke"
SELECTED_DIR = PAPER_ROOT / "selected_seed_examples"
CONVERSION_REPORTS = PIPELINE_ROOT / "conversion/reports"
REPRESENTATION_REPORTS = PIPELINE_ROOT / "representation/reports"
EVALUATION_DIR = PIPELINE_ROOT / "evaluation/dry_run_examples"
SEED_LIBRARY_DIR = PAPER_ROOT / "corpora/seed_library"
RECOVERY_REPORT_PATH = CONVERSION_REPORTS / "plantuml_recovery_report.json"

SELECTED_EXAMPLE_IDS = [
    "llms-emp-gpt4o-hldcs",
    "sefm-ssc7-umple",
    "llms-emp-deepseek-microwave",
    "llms-emp-kimi-autonomous-collision",
]

NON_ENTRY_DIRS = {"schemas", "tools"}
AUXILIARY_FILES = {"manual_download_queue.bib"}
STATUS_ORDER = ["converted", "partial", "blocked", "missing_asset", "needs_generation", "not_applicable"]
PAIR_ARCHIVE_THRESHOLD = 50
ARCHIVE_SIZE_THRESHOLD = 5 * 1024 * 1024


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def rel(path: Path | str | None) -> str | None:
    if path is None:
        return None
    p = Path(path)
    try:
        return str(p.resolve().relative_to(REPO_ROOT.resolve()))
    except Exception:
        return str(path)


def repo_path(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    p = Path(path)
    return p if p.is_absolute() else REPO_ROOT / p


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_commit() -> str:
    import subprocess

    try:
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_ROOT, text=True).strip()
    except Exception:
        return "unknown"


def git_status_porcelain() -> list[str]:
    import subprocess

    try:
        return subprocess.check_output(["git", "status", "--short"], cwd=REPO_ROOT, text=True).splitlines()
    except Exception:
        return ["<git status unavailable>"]


def generation_context(command: str, schema_paths: list[Path] | None = None) -> dict[str, Any]:
    schema_paths = schema_paths or []
    cli_path = Path(__file__)
    status = git_status_porcelain()
    return {
        "command": command,
        "repo_commit": git_commit(),
        "repo_commit_scope": "base commit at generation time; if generated artifacts are committed in the same PR commit, use generator_cli_sha256/schema_sha256 plus PR diff for exact provenance",
        "git_dirty": bool(status),
        "git_status_porcelain": status[:200],
        "generator_cli_path": rel(cli_path),
        "generator_cli_sha256": sha256_file(cli_path),
        "schema_sha256": {rel(p): sha256_file(p) for p in schema_paths if p.exists()},
        "repair_contribution_allowed": False,
    }


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def find_stm0(example_dir: Path) -> Path | None:
    files = sorted(example_dir.glob("stm0.*"))
    return files[0] if len(files) == 1 else None


def by_key(items: Iterable[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]:
    return {str(item.get(key)): item for item in items if item.get(key) is not None}


def load_loss_ledger(path: Path, example_field: str = "example_id") -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    if not path.exists():
        return out
    for row in read_jsonl(path):
        out[str(row.get(example_field))].append(row)
    return out


def selected_pair_index() -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    if not SELECTED_DIR.exists():
        return out
    r3_items = by_key(load_json(CONVERSION_REPORTS / "selected_seed_examples_conversion_report.json").get("items", []), "example_id") if (CONVERSION_REPORTS / "selected_seed_examples_conversion_report.json").exists() else {}
    r45_items = by_key(load_json(REPRESENTATION_REPORTS / "fcstm_export_report.json").get("items", []), "example_id") if (REPRESENTATION_REPORTS / "fcstm_export_report.json").exists() else {}
    r45_losses = load_loss_ledger(REPRESENTATION_REPORTS / "fcstm_export_loss_ledger.jsonl")
    for d in sorted(p for p in SELECTED_DIR.iterdir() if p.is_dir()):
        meta_path = d / "source_meta.json"
        if not meta_path.exists():
            continue
        meta = load_json(meta_path)
        pair_id = meta.get("pair_id")
        if not pair_id:
            continue
        out[pair_id] = {
            "example_id": d.name,
            "source_meta": meta,
            "r3_item": r3_items.get(d.name),
            "r45_item": r45_items.get(d.name),
            "r45_losses": r45_losses.get(d.name, []),
        }
    return out


def loss_summary(loss_rows: list[dict[str, Any]]) -> dict[str, Any]:
    categories = sorted({str(r.get("loss_type") or r.get("reason_code") or "unknown") for r in loss_rows})
    reason_codes = sorted({str(r.get("reason_code") or r.get("loss_code") or r.get("loss_type") or "unknown") for r in loss_rows})
    irrecoverable = sorted({str(r.get("canonical_ref") or r.get("affected_item_id") or r.get("source_ref") or "unknown") for r in loss_rows if r.get("severity") in {"blocking_transition", "model_blocking", "blocking", "high"}})
    return {
        "loss_count": len(loss_rows),
        "loss_categories": categories,
        "loss_reason_codes": reason_codes,
        "irrecoverable_fields": irrecoverable,
    }


def selected_status(r3_item: dict[str, Any] | None, r45_item: dict[str, Any] | None, checks_ok: bool) -> tuple[str, str]:
    if not checks_ok:
        return "blocked", "R5.SELECTED.blocked_trace_or_hash_mismatch"
    if not r3_item or not r45_item:
        return "blocked", "R5.SELECTED.blocked_missing_upstream_report"
    if r45_item.get("parse_status") != "ok" or r45_item.get("inspect_status") != "ok":
        return "blocked", "R5.SELECTED.blocked_fcstm_parse_or_inspect_failed"
    if r3_item.get("status") != "converted" or r45_item.get("status") != "converted" or int(r45_item.get("loss_count") or 0) > 0:
        return "partial", "R5.SELECTED.partial_upstream_caveat_or_loss"
    return "pass", "R5.SELECTED.pass_all_trace_and_parse_checks"


def run_selected(_: argparse.Namespace) -> int:
    out_dir = SMOKE_ROOT / "selected_examples"
    rec_dir = out_dir / "smoke_records"
    rec_dir.mkdir(parents=True, exist_ok=True)

    r3_report = load_json(CONVERSION_REPORTS / "selected_seed_examples_conversion_report.json")
    r3_items = by_key(r3_report.get("items", []), "example_id")
    r45_report = load_json(REPRESENTATION_REPORTS / "fcstm_export_report.json")
    r45_items = by_key(r45_report.get("items", []), "example_id")
    r45_losses = load_loss_ledger(REPRESENTATION_REPORTS / "fcstm_export_loss_ledger.jsonl")

    records: list[dict[str, Any]] = []
    summary_counts = Counter()
    for example_id in SELECTED_EXAMPLE_IDS:
        example_dir = SELECTED_DIR / example_id
        source_meta_path = example_dir / "source_meta.json"
        fcstm_meta_path = example_dir / "fcstm_meta.json"
        nl_path = example_dir / "nl.txt"
        stm_path = find_stm0(example_dir)
        selected_fcstm = example_dir / "model.fcstm"
        source_meta = load_json(source_meta_path) if source_meta_path.exists() else {}
        fcstm_meta = load_json(fcstm_meta_path) if fcstm_meta_path.exists() else {}
        r3_item = r3_items.get(example_id)
        r45_item = r45_items.get(example_id)
        r45_parse_report = {}
        if r45_item and r45_item.get("parse_inspect_report_path"):
            parse_report_path = repo_path(r45_item.get("parse_inspect_report_path"))
            if parse_report_path and parse_report_path.exists():
                r45_parse_report = load_json(parse_report_path)
        eval_paths = {
            name: EVALUATION_DIR / example_id / name
            for name in ["eligibility_decision.json", "diagnostic_draft.json", "scenario_draft.json", "better_stm_checklist.json"]
        }
        checks = {
            "selected_dir_exists": example_dir.exists(),
            "nl_exists": nl_path.exists(),
            "stm0_exists": bool(stm_path and stm_path.exists()),
            "source_meta_exists": source_meta_path.exists(),
            "fcstm_meta_exists": fcstm_meta_path.exists(),
            "selected_fcstm_exists": selected_fcstm.exists(),
            "nl_sha256_match": nl_path.exists() and source_meta.get("nl_sha256") == sha256_file(nl_path),
            "stm0_sha256_match": bool(stm_path and source_meta.get("stm0_sha256") == sha256_file(stm_path)),
            "trace_verified": source_meta.get("trace_verified") is True,
            "selected_fcstm_sha256_match": selected_fcstm.exists() and fcstm_meta.get("selected_fcstm_sha256") == sha256_file(selected_fcstm),
            "selected_fcstm_sync_hash_match": fcstm_meta.get("selected_fcstm_sha256") == fcstm_meta.get("synchronized_from_fcstm_sha256"),
            "r3_item_exists": r3_item is not None,
            "r3_canonical_exists": bool(r3_item and r3_item.get("canonical_output_path") and repo_path(r3_item.get("canonical_output_path")).exists()),
            "r45_item_exists": r45_item is not None,
            "r45_export_exists": bool(r45_item and r45_item.get("fcstm_path") and repo_path(r45_item.get("fcstm_path")).exists()),
            "r45_parse_report_exists": bool(r45_item and r45_item.get("parse_inspect_report_path") and repo_path(r45_item.get("parse_inspect_report_path")).exists()),
            "r45_parse_ok": bool(r45_item and r45_item.get("parse_status") == "ok"),
            "r45_inspect_ok": bool(r45_item and r45_item.get("inspect_status") == "ok"),
            "r45_parse_report_read_status_match": bool(r45_item and r45_parse_report and r45_parse_report.get("parse_status") == r45_item.get("parse_status")),
            "r45_parse_report_read_inspect_match": bool(r45_item and r45_parse_report and r45_parse_report.get("inspect_status") == r45_item.get("inspect_status")),
            "r4_fixture_all_exist": all(p.exists() for p in eval_paths.values()),
            "repair_contribution_allowed_false": fcstm_meta.get("repair_contribution_allowed") is False and (not r45_item or r45_item.get("repair_contribution_allowed") is False),
        }
        checks_ok = all(checks.values())
        status, reason = selected_status(r3_item, r45_item, checks_ok)
        losses = loss_summary(r45_losses.get(example_id, []))
        record = {
            "schema_version": "r5.selected_smoke_record.v0",
            "example_id": example_id,
            "seed_id": source_meta.get("seed_id") or (r3_item or {}).get("seed_id"),
            "created_at": now_iso(),
            "source": {
                "nl_path": rel(nl_path),
                "stm0_path": rel(stm_path),
                "source_meta_path": rel(source_meta_path),
                "stm_format": source_meta.get("stm_format"),
                "nl_sha256": sha256_file(nl_path) if nl_path.exists() else None,
                "stm0_sha256": sha256_file(stm_path) if stm_path and stm_path.exists() else None,
                "trace_verified": source_meta.get("trace_verified"),
                "source_locator": source_meta.get("source_locator"),
            },
            "upstream_r3": {
                "status": (r3_item or {}).get("status"),
                "status_reason_code": (r3_item or {}).get("status_reason_code"),
                "canonical_output_path": (r3_item or {}).get("canonical_output_path"),
                "conversion_source": (r3_item or {}).get("conversion_source"),
                "tool_invocation_status": (r3_item or {}).get("tool_invocation_status"),
                "r3_1_normalization_replay_used": any(d.get("code") == "R3.R31.NORMALIZED_SCXML_REPLAY_USED" for d in (r3_item or {}).get("diagnostics", [])),
            },
            "upstream_r45": {
                "status": (r45_item or {}).get("status"),
                "status_reason_code": (r45_item or {}).get("status_reason_code"),
                "fcstm_path": (r45_item or {}).get("fcstm_path"),
                "parse_inspect_report_path": (r45_item or {}).get("parse_inspect_report_path"),
                "parse_status": (r45_item or {}).get("parse_status"),
                "inspect_status": (r45_item or {}).get("inspect_status"),
                "direct_parse_report_status": r45_parse_report.get("parse_status"),
                "direct_parse_report_inspect_status": r45_parse_report.get("inspect_status"),
                "blocked_transitions_count": (r45_item or {}).get("blocked_transitions_count"),
                **losses,
            },
            "upstream_r4_fixture": {k: rel(v) for k, v in eval_paths.items()},
            "checks": checks,
            "status": status,
            "status_reason_code": reason,
            "repair_contribution_allowed": False,
            "attribution": "r5_pre_repair_readiness_audit_only",
        }
        write_json(rec_dir / f"{example_id}.json", record)
        records.append(record)
        summary_counts[status] += 1

    report = {
        "schema_version": "r5.selected_smoke_report.v0",
        "run_id": "r5-selected-deterministic-smoke",
        "created_at": now_iso(),
        "repo_commit": git_commit(),
        "generation_context": generation_context(
            "python -m paper_stm_repair_smoke.cli run-selected",
            [SMOKE_ROOT / "schemas/selected_smoke_report.schema.json"],
        ),
        "repair_contribution_allowed": False,
        "items": records,
        "summary": {
            "examples": len(records),
            "pass": summary_counts.get("pass", 0),
            "partial": summary_counts.get("partial", 0),
            "blocked": summary_counts.get("blocked", 0),
        },
    }
    write_json(out_dir / "smoke_report.json", report)
    write_selected_summary(out_dir / "smoke_summary.md", report)
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0


def write_selected_summary(path: Path, report: dict[str, Any]) -> None:
    all_checks_ok = all(all(item.get("checks", {}).values()) for item in report.get("items", []))
    lines = [
        "# R5 selected 四例 deterministic smoke 摘要",
        "",
        "本文件由 `python -m paper_stm_repair_smoke.cli run-selected` 生成。JSON 事实源是 [smoke_report.json](./smoke_report.json)，本 Markdown 只做人类阅读入口，不作为第二事实真源。",
        "",
        f"- examples: {report['summary']['examples']}",
        f"- pass: {report['summary']['pass']}",
        f"- partial: {report['summary']['partial']}",
        f"- blocked: {report['summary']['blocked']}",
        "",
    ]
    if report["summary"]["partial"] == report["summary"]["examples"] and all_checks_ok:
        lines.extend([
            "> 当前 4 例全部落为 `partial` 是预期的 pre-repair baseline state，不表示 smoke 未跑通；每例 R5 contract checks 均通过。",
            "> `partial` 仅表示上游 R3/R4/R4.5 已记录 conversion / representation loss 或 caveat，R5 不能把这些 loss 当作 repair gain 清零。",
            "",
        ])
    lines.extend([
        "| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |",
        "|---|---|---|---|---|---|---:|---|---|",
    ])
    for item in report["items"]:
        lines.append(
            f"| `{item['example_id']}` | `{item['status']}` | `{item.get('seed_id')}` | "
            f"`{item['source'].get('stm_format')}` | `{item['upstream_r3'].get('status')}` | "
            f"`{item['upstream_r45'].get('parse_status')}/{item['upstream_r45'].get('inspect_status')}` | "
            f"{item['upstream_r45'].get('loss_count')} | `{item['status_reason_code']}` | "
            f"[record](./smoke_records/{item['example_id']}.json) |"
        )
    lines.extend([
        "",
        "所有条目均为 pre-repair smoke；`repair_contribution_allowed=false`。`partial` 不表示不可用，而是表示进入后续 R6/R7 前必须保留 conversion / representation caveat。",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


@dataclass
class RecoveryIndex:
    by_pair_id: dict[str, dict[str, Any]]
    zip_path: Path | None


def load_recovery_index() -> RecoveryIndex:
    if not RECOVERY_REPORT_PATH.exists():
        return RecoveryIndex({}, None)
    doc = load_json(RECOVERY_REPORT_PATH)
    zip_rel = (doc.get("artifact_archive") or {}).get("archive_path")
    return RecoveryIndex({str(i.get("pair_id")): i for i in doc.get("items", [])}, repo_path(zip_rel) if zip_rel else None)


def row_is_eligible_generated(row: dict[str, Any], entry_role: str) -> bool:
    return bool(
        row.get("is_generated_stm0") is True
        and row.get("is_reference") is False
        and row.get("is_postprocessed") is False
        and row.get("trace_verified") is True
        and row.get("eligibility_state") in {"final_pool_ready", "conditional_final_pool"}
        and row.get("stm0_text")
        and row.get("stm0_sha256")
        and entry_role in {"final_pool_ready", "conditional_final_pool"}
    )


def infer_stm_format(row: dict[str, Any]) -> str:
    fmt = row.get("stm_format")
    if fmt:
        return str(fmt)
    text = str(row.get("stm0_text") or "").lstrip()
    if text.startswith("@startuml"):
        return "plantuml"
    if text.startswith("<?xml") or "<TURTLEGMODELING" in text[:1000]:
        return "ttool_xml"
    if "class " in text[:300] and "{" in text[:300]:
        return "umple"
    return "unknown"


def base_pair_record(entry_id: str, row: dict[str, Any], registry: dict[str, Any]) -> dict[str, Any]:
    pair_id = str(row.get("pair_id") or row.get("case_id") or f"{entry_id}:unknown")
    return {
        "schema_version": "r5.seed_sweep_pair_record.v0",
        "record_id": f"{entry_id}::{pair_id}",
        "entry_id": entry_id,
        "pair_id": pair_id,
        "pair_set_id": row.get("pair_set_id"),
        "source_asset_id": row.get("source_asset_id"),
        "source_local_path": row.get("source_local_path"),
        "resource_role": registry.get("recommended_role"),
        "source_category": (registry.get("resource_profile") or {}).get("resource_category"),
        "source_locator": row.get("source_locator"),
        "source_locator_type": row.get("source_locator_type"),
        "source_sha256": row.get("source_sha256"),
        "nl_sha256": row.get("nl_sha256"),
        "stm0_sha256": row.get("stm0_sha256"),
        "generation_actor": row.get("generation_actor"),
        "generation_model_or_method": row.get("generation_model_or_method"),
        "trace_verified": row.get("trace_verified"),
        "is_generated_stm0": row.get("is_generated_stm0"),
        "is_reference": row.get("is_reference"),
        "is_postprocessed": row.get("is_postprocessed"),
        "stm_format": infer_stm_format(row),
        "repair_contribution_allowed": False,
        "conversion_attribution": "r5_conversion_readiness_probe_not_repair",
        "representation_attribution": "r5_fcstm_lowering_probe_not_repair",
        "handoff_target": None,
    }


def timeout_pair_record(entry_id: str, row: dict[str, Any], registry: dict[str, Any], max_seconds: int) -> dict[str, Any]:
    rec = base_pair_record(entry_id, row, registry)
    rec.update({
        "status": "blocked",
        "status_reason_code": "R5.SWEEP.blocked_pair_timeout",
        "max_per_pair_seconds": max_seconds,
        "error_type": "TimeoutError",
        "error_message": f"R5 per-pair conversion probe exceeded {max_seconds} seconds",
        "loss_count": 0,
        "loss_categories": [],
        "loss_reason_codes": ["R5.LOSS.pair_timeout"],
        "irrecoverable_fields": ["conversion_probe_runtime"],
        "handoff_target": "converter_followup",
    })
    return rec


def convert_pair_record_with_timeout(
    entry_id: str,
    row: dict[str, Any],
    registry: dict[str, Any],
    recovery: RecoveryIndex,
    tmp_root: Path,
    selected_pairs: dict[str, dict[str, Any]] | None,
    max_seconds: int,
    continue_on_error: bool,
) -> dict[str, Any]:
    if max_seconds <= 0 or not hasattr(signal, "setitimer") or threading.current_thread() is not threading.main_thread():
        rec = convert_pair_record(entry_id, row, registry, recovery, tmp_root, selected_pairs)
        if not continue_on_error and rec.get("status_reason_code") == "R5.SWEEP.blocked_exception_during_probe":
            raise RuntimeError(f"{rec.get('record_id')} failed during conversion probe: {rec.get('error_type')}: {rec.get('error_message')}")
        return rec

    def _handler(signum: int, frame: Any) -> None:  # pragma: no cover - exercised by timeout integration, not unit-sized.
        raise TimeoutError(f"R5 per-pair conversion probe exceeded {max_seconds} seconds")

    old_handler = signal.getsignal(signal.SIGALRM)
    old_timer = signal.setitimer(signal.ITIMER_REAL, max_seconds)
    signal.signal(signal.SIGALRM, _handler)
    try:
        rec = convert_pair_record(entry_id, row, registry, recovery, tmp_root, selected_pairs)
        if not continue_on_error and rec.get("status_reason_code") == "R5.SWEEP.blocked_exception_during_probe":
            raise RuntimeError(f"{rec.get('record_id')} failed during conversion probe: {rec.get('error_type')}: {rec.get('error_message')}")
        return rec
    except TimeoutError:
        if not continue_on_error:
            raise
        return timeout_pair_record(entry_id, row, registry, max_seconds)
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, old_handler)
        if old_timer and old_timer[0] > 0:
            signal.setitimer(signal.ITIMER_REAL, old_timer[0], old_timer[1])


def convert_pair_record(entry_id: str, row: dict[str, Any], registry: dict[str, Any], recovery: RecoveryIndex, tmp_root: Path, selected_pairs: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    pair_id = str(row.get("pair_id") or row.get("case_id") or f"{entry_id}:unknown")
    base = base_pair_record(entry_id, row, registry)
    text = row.get("stm0_text") or ""
    if sha256_text(text) != row.get("stm0_sha256"):
        base.update({
            "status": "missing_asset",
            "status_reason_code": "R5.SWEEP.missing_asset_stm0_hash_mismatch",
            "error": "stm0_text sha256 does not match registry row stm0_sha256",
            **loss_summary([]),
            "loss_reason_codes": ["R5.LOSS.asset_hash_mismatch"],
            "irrecoverable_fields": ["stm0_text"],
            "handoff_target": "asset_repair_required",
        })
        return base

    fmt = base["stm_format"]
    if fmt == "ttool_xml":
        base.update({
            "status": "partial",
            "status_reason_code": "R5.SWEEP.partial_ttool_xml_conditional_inventory_only",
            "loss_count": 1,
            "loss_categories": ["format_caveat"],
            "loss_reason_codes": ["R5.LOSS.ttool_xml_requires_smd_t0_slice"],
            "irrecoverable_fields": ["TTool XML includes whole AVATAR project; current R4.5 cannot produce trusted T0 fcstm"],
            "handoff_target": "r7_eligibility_review",
        })
        return base
    if fmt not in {"plantuml", "umple"}:
        base.update({
            "status": "blocked",
            "status_reason_code": "R5.SWEEP.blocked_unsupported_stm_format",
            **loss_summary([]),
            "loss_reason_codes": ["R5.LOSS.unsupported_stm_format"],
            "irrecoverable_fields": [fmt],
            "handoff_target": "converter_followup",
        })
        return base

    try:
        if fmt == "plantuml":
            recovery_item = recovery.by_pair_id.get(pair_id)
            if not recovery_item:
                base.update({
                    "status": "blocked",
                    "status_reason_code": "R5.SWEEP.blocked_no_r31_recovery_probe_for_plantuml_pair",
                    **loss_summary([]),
                    "loss_reason_codes": ["R5.LOSS.no_committed_official_scxml_probe"],
                    "irrecoverable_fields": ["official_scxml"],
                    "handoff_target": "converter_followup",
                })
                return base
            preflight = recovery_item.get("raw_preflight") if recovery_item.get("raw_conversion_pass") else recovery_item.get("normalized_preflight")
            conversion_source = "official_scxml_raw" if recovery_item.get("raw_conversion_pass") else "official_scxml_r3_1_normalized_replay"
            if not preflight or preflight.get("structured_export_status") != "scxml_export_ok" or not preflight.get("structured_export_path"):
                base.update({
                    "status": "blocked",
                    "status_reason_code": "R5.SWEEP.blocked_official_scxml_unavailable",
                    "raw_conversion_pass": recovery_item.get("raw_conversion_pass"),
                    "normalized_conversion_pass": recovery_item.get("normalized_conversion_pass"),
                    **loss_summary([]),
                    "loss_reason_codes": ["R5.LOSS.official_scxml_unavailable"],
                    "irrecoverable_fields": ["official_scxml"],
                    "handoff_target": "r8_negative_evidence",
                })
                return base
            if not recovery.zip_path or not recovery.zip_path.exists():
                base.update({
                    "status": "missing_asset",
                    "status_reason_code": "R5.SWEEP.missing_asset_r31_recovery_archive",
                    **loss_summary([]),
                    "loss_reason_codes": ["R5.LOSS.missing_recovery_archive"],
                    "irrecoverable_fields": [str(recovery.zip_path)],
                    "handoff_target": "asset_repair_required",
                })
                return base
            member = preflight["structured_export_path"]
            scxml_path = tmp_root / entry_id / f"{pair_id}.scxml"
            scxml_path.parent.mkdir(parents=True, exist_ok=True)
            with zipfile.ZipFile(recovery.zip_path) as zf:
                scxml_path.write_bytes(zf.read(member))
            from paper_stm_repair_conversion.adapters.scxml import ScxmlOptions, convert_scxml
            from paper_stm_repair_representation.lowering import FCSTMExporter, inspect_fcstm

            result = convert_scxml(
                scxml_path,
                example_id=pair_id,
                seed_id=entry_id,
                options=ScxmlOptions(
                    adapter="plantuml",
                    source_format="plantuml",
                    conversion_source="official_scxml",
                    canonical_extraction_method=f"R5 seed sweep uses committed R3.1 official PlantUML SCXML probe ({conversion_source}) parsed by xml.etree.ElementTree",
                    status_on_success="converted",
                    fallback_used=False,
                    fallback_scope=None,
                    timing_level="none",
                    source_language="PlantUML state diagram",
                ),
                structured_export_relpath=member,
                structured_export_sha256=preflight.get("structured_export_sha256"),
            )
            canonical = result.to_canonical_dict()
            exported = FCSTMExporter(canonical).export() if result.status in {"converted", "partial"} else None
        else:
            selected_hit = (selected_pairs or {}).get(pair_id)
            if selected_hit and selected_hit.get("r45_item"):
                r3_item = selected_hit.get("r3_item") or {}
                r45_item = selected_hit.get("r45_item") or {}
                ls = loss_summary(selected_hit.get("r45_losses", []))
                status = "converted" if r45_item.get("status") == "converted" and r45_item.get("parse_status") == "ok" and r45_item.get("inspect_status") == "ok" and not ls.get("loss_count") and r3_item.get("status") == "converted" else "partial"
                base.update({
                    "status": status,
                    "status_reason_code": "R5.SWEEP.partial_reused_selected_umple_committed_r3_r45_caveat" if status == "partial" else "R5.SWEEP.converted_reused_selected_umple_committed_r3_r45",
                    "selected_example_id": selected_hit.get("example_id"),
                    "canonical_status": r3_item.get("status"),
                    "conversion_source": r3_item.get("conversion_source"),
                    "fcstm_sha256": sha256_file(repo_path(r45_item.get("fcstm_path"))) if r45_item.get("fcstm_path") and repo_path(r45_item.get("fcstm_path")).exists() else None,
                    "parse_status": r45_item.get("parse_status"),
                    "inspect_status": r45_item.get("inspect_status"),
                    "blocked_transitions_count": r45_item.get("blocked_transitions_count"),
                    **ls,
                    "handoff_target": "r6_candidate" if status == "converted" else "r7_eligibility_review",
                })
                base["loss_categories"] = sorted(set(base.get("loss_categories", [])) | {"selected_umple_reuse_caveat"})
                base["loss_reason_codes"] = sorted(set(base.get("loss_reason_codes", [])) | {"R5.LOSS.selected_umple_reused_committed_r3_r45"})
                return base
            # R5 has no committed official Umple batch export beyond selected.
            base.update({
                "status": "blocked",
                "status_reason_code": "R5.SWEEP.blocked_no_batch_umple_structured_export_probe",
                **loss_summary([]),
                "loss_reason_codes": ["R5.LOSS.no_batch_umple_structured_export_probe"],
                "irrecoverable_fields": ["official_scxml"],
                "handoff_target": "converter_followup",
            })
            return base

        r45_losses = exported.get("loss_rows", []) if exported else []
        fcstm = exported.get("fcstm") if exported else None
        if not fcstm:
            base.update({
                "status": "blocked",
                "status_reason_code": "R5.SWEEP.blocked_no_fcstm_emitted",
                **loss_summary(r45_losses),
                "handoff_target": "r8_negative_evidence",
            })
            return base
        fcstm_path = tmp_root / entry_id / f"{pair_id}.fcstm"
        fcstm_path.parent.mkdir(parents=True, exist_ok=True)
        fcstm_path.write_text(fcstm, encoding="utf-8")
        parse_report = inspect_fcstm(fcstm, fcstm_path)
        ls = loss_summary(r45_losses)
        parse_ok = parse_report.get("parse_status") == "ok" and parse_report.get("inspect_status") == "ok"
        has_loss_or_caveat = bool(ls.get("loss_count")) or conversion_source != "official_scxml_raw"
        status = "converted" if parse_ok and exported.get("status") == "converted" and not has_loss_or_caveat else "partial" if parse_ok else "blocked"
        reason_code = "R5.SWEEP.converted_fcstm_parse_inspect_ok"
        if status == "partial" and conversion_source != "official_scxml_raw":
            reason_code = "R5.SWEEP.partial_r3_1_normalization_or_representation_loss"
        elif status == "partial":
            reason_code = "R5.SWEEP.partial_representation_loss_or_caveat"
        elif status == "blocked":
            reason_code = "R5.SWEEP.blocked_fcstm_parse_or_inspect_failed"
        if conversion_source != "official_scxml_raw":
            ls["loss_categories"] = sorted(set(ls.get("loss_categories", [])) | {"r3_1_normalization_replay"})
            ls["loss_reason_codes"] = sorted(set(ls.get("loss_reason_codes", [])) | {"R5.LOSS.r3_1_normalization_replay_not_repair"})
        base.update({
            "status": status,
            "status_reason_code": reason_code,
            "canonical_status": result.status,
            "canonical_states_count": len(result.states),
            "canonical_transitions_count": len(result.transitions),
            "conversion_source": conversion_source,
            "structured_export_sha256": preflight.get("structured_export_sha256"),
            "fcstm_sha256": sha256_text(fcstm),
            "parse_status": parse_report.get("parse_status"),
            "inspect_status": parse_report.get("inspect_status"),
            "blocked_transitions_count": len(exported.get("blocked_transitions", [])),
            **ls,
            "handoff_target": "r6_candidate" if status == "converted" else "r7_eligibility_review",
        })
        return base
    except TimeoutError:
        raise
    except Exception as exc:
        base.update({
            "status": "blocked",
            "status_reason_code": "R5.SWEEP.blocked_exception_during_probe",
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            **loss_summary([]),
            "loss_reason_codes": ["R5.LOSS.exception_during_probe"],
            "irrecoverable_fields": [type(exc).__name__],
            "handoff_target": "converter_followup",
        })
        return base


def aggregate_primary(statuses: list[str], *, has_registry: bool, role: str, missing_asset: bool) -> str:
    if not has_registry:
        return "not_applicable"
    if missing_asset or "missing_asset" in statuses:
        return "missing_asset"
    if role == "pipeline_only" or "needs_generation" in statuses:
        return "needs_generation"
    if not statuses:
        return "not_applicable"
    if any(s in statuses for s in ["converted", "partial"]) and any(s in statuses for s in ["blocked", "partial"]):
        return "partial"
    if statuses and all(s == "converted" for s in statuses):
        return "converted"
    if statuses and all(s == "blocked" for s in statuses):
        return "blocked"
    if "converted" in statuses:
        return "partial"
    if "partial" in statuses:
        return "partial"
    return statuses[0] if statuses else "not_applicable"


def entry_not_applicable_record(entry_dir: Path, reason: str) -> dict[str, Any]:
    entry_id = entry_dir.name
    return {
        "schema_version": "r5.seed_sweep_entry_record.v0",
        "entry_id": entry_id,
        "has_registry": False,
        "registry_path": None,
        "recommended_role": None,
        "resource_category": None,
        "primary_entry_status": "not_applicable",
        "entry_statuses": ["not_applicable"],
        "status_reason_code": reason,
        "status_counts_by_pair": {"not_applicable": 0},
        "status_counts_by_asset": {"not_applicable": 0},
        "pair_record_count": 0,
        "asset_record_count": 0,
        "handoff_target": "related_work_or_excluded",
        "repair_contribution_allowed": False,
        "notes": "No seed_resource_registry.json is committed for this entry in R5; it remains related/paper-level evidence unless upgraded by a later first-source asset PR.",
    }


def load_asset_records(entry_dir: Path, registry: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
    manifest_rel = (registry.get("asset_summary") or {}).get("manifest_path")
    if not manifest_rel:
        return [], False
    manifest_path = entry_dir / manifest_rel
    if not manifest_path.exists():
        return [], True
    manifest = load_json(manifest_path)
    records = []
    missing = False
    for asset in manifest.get("assets", []):
        local = asset.get("local_path")
        local_path = (entry_dir / "assets" / local) if local else None
        exists = bool(local_path and local_path.exists())
        hash_ok = exists and (not asset.get("sha256") or sha256_file(local_path) == asset.get("sha256"))
        status = "available" if exists and hash_ok else "missing_asset"
        if status == "missing_asset":
            missing = True
        records.append({
            "schema_version": "r5.seed_sweep_asset_record.v0",
            "record_id": f"{entry_dir.name}::asset::{asset.get('asset_id')}",
            "entry_id": entry_dir.name,
            "asset_id": asset.get("asset_id"),
            "role": asset.get("role"),
            "local_path": rel(local_path) if local_path else None,
            "download_status": asset.get("download_status"),
            "storage_mode": asset.get("storage_mode"),
            "sha256": asset.get("sha256"),
            "exists": exists,
            "hash_ok": hash_ok,
            "status": status,
            "repair_contribution_allowed": False,
        })
    return records, missing


def run_seed_sweep(args: argparse.Namespace) -> int:
    out_dir = SMOKE_ROOT / "seed_library_sweep"
    audit_dir = out_dir / "audit_records"
    archive_dir = out_dir / "archives"
    for p in [out_dir, audit_dir, archive_dir]:
        p.mkdir(parents=True, exist_ok=True)
    for old in audit_dir.glob("*.json"):
        old.unlink()
    for old in archive_dir.glob("*.zip"):
        old.unlink()

    recovery = load_recovery_index()
    selected_pairs = selected_pair_index()
    entries = sorted(p for p in SEED_LIBRARY_DIR.iterdir() if p.is_dir() and p.name not in NON_ENTRY_DIRS)
    excluded_dirs = sorted(p.name for p in SEED_LIBRARY_DIR.iterdir() if p.is_dir() and p.name in NON_ENTRY_DIRS)
    excluded_files = sorted(p.name for p in SEED_LIBRARY_DIR.iterdir() if p.is_file() and p.name in AUXILIARY_FILES)

    entry_records: list[dict[str, Any]] = []
    pair_records_all: list[dict[str, Any]] = []
    asset_records_all: list[dict[str, Any]] = []
    index_records: list[dict[str, Any]] = []
    archives: list[dict[str, Any]] = []

    with tempfile.TemporaryDirectory(prefix="r5_seed_sweep_") as td:
        tmp_root = Path(td)
        for entry_dir in entries:
            registry_path = entry_dir / "seed_resource_registry.json"
            if not registry_path.exists():
                rec = entry_not_applicable_record(entry_dir, "R5.SWEEP.not_applicable_no_seed_resource_registry")
                entry_records.append(rec)
                continue
            registry = load_json(registry_path)
            entry_id = entry_dir.name
            role = str(registry.get("recommended_role") or "unknown")
            category = str((registry.get("resource_profile") or {}).get("resource_category") or "unknown")
            asset_records, missing_assets = load_asset_records(entry_dir, registry)
            asset_records_all.extend(asset_records)

            pair_records: list[dict[str, Any]] = []
            pair_paths = []
            for pair_set in registry.get("pair_sets", []):
                rel_path = pair_set.get("extracted_pairs_path")
                if rel_path:
                    pair_paths.append(entry_dir / rel_path)
            summary_path = (registry.get("extracted_summary") or {}).get("pairs_jsonl")
            if summary_path:
                pair_paths.append(entry_dir / summary_path)
            pair_paths = sorted(set(pair_paths))

            if role == "pipeline_only" or category == "nl_code_reproducible":
                pair_records.append({
                    "schema_version": "r5.seed_sweep_pair_record.v0",
                    "record_id": f"{entry_id}::needs_generation",
                    "entry_id": entry_id,
                    "pair_id": None,
                    "status": "needs_generation",
                    "status_reason_code": "R5.SWEEP.needs_generation_pipeline_only_no_author_generated_stm0",
                    "raw_nl_count": (registry.get("source_inventory") or {}).get("raw_nl_count"),
                    "unique_nl_count": (registry.get("source_inventory") or {}).get("unique_nl_count"),
                    "resource_role": role,
                    "source_category": category,
                    "handoff_target": "followup_seed_generation_pr_required_before_r7_or_excluded_by_r7",
                    "minimum_resources_for_generation": {
                        "asset_manifest": rel(entry_dir / ((registry.get("asset_summary") or {}).get("manifest_path") or "")),
                        "code_urls": (registry.get("source_work") or {}).get("code_urls", []),
                        "paper_llm_models": ((registry.get("resource_profile") or {}).get("paper_llm_models") or []),
                    },
                    "loss_count": 0,
                    "loss_categories": [],
                    "loss_reason_codes": ["R5.LOSS.no_author_generated_stm0"],
                    "irrecoverable_fields": ["generated_stm0"],
                    "repair_contribution_allowed": False,
                    "conversion_attribution": "not_run_in_r5",
                    "representation_attribution": "not_run_in_r5",
                })
            elif not pair_paths:
                pair_records.append({
                    "schema_version": "r5.seed_sweep_pair_record.v0",
                    "record_id": f"{entry_id}::not_applicable",
                    "entry_id": entry_id,
                    "pair_id": None,
                    "status": "not_applicable",
                    "status_reason_code": "R5.SWEEP.not_applicable_no_extracted_pairs_jsonl",
                    "resource_role": role,
                    "source_category": category,
                    "handoff_target": "related_work_or_excluded",
                    "repair_contribution_allowed": False,
                })
            else:
                seen_pair_ids: set[str] = set()
                for pair_path in pair_paths:
                    rows = read_jsonl(pair_path)
                    if not rows and role == "pipeline_only":
                        continue
                    for row in rows:
                        pair_id = str(row.get("pair_id") or row.get("case_id") or f"row_{len(seen_pair_ids)}")
                        if pair_id in seen_pair_ids:
                            continue
                        seen_pair_ids.add(pair_id)
                        if not row_is_eligible_generated(row, role):
                            pair_records.append({
                                "schema_version": "r5.seed_sweep_pair_record.v0",
                                "record_id": f"{entry_id}::{pair_id}",
                                "entry_id": entry_id,
                                "pair_id": pair_id,
                                "status": "not_applicable",
                                "status_reason_code": "R5.SWEEP.not_applicable_pair_not_eligible_generated_stm0",
                                "resource_role": role,
                                "source_category": category,
                                "eligibility_state": row.get("eligibility_state"),
                                "is_generated_stm0": row.get("is_generated_stm0"),
                                "is_reference": row.get("is_reference"),
                                "is_postprocessed": row.get("is_postprocessed"),
                                "trace_verified": row.get("trace_verified"),
                                "handoff_target": "related_work_or_excluded",
                                "repair_contribution_allowed": False,
                            })
                            continue
                        pair_records.append(
                            convert_pair_record_with_timeout(
                                entry_id,
                                row,
                                registry,
                                recovery,
                                tmp_root,
                                selected_pairs,
                                args.max_per_pair_seconds,
                                args.continue_on_error,
                            )
                        )

            pair_records_all.extend(pair_records)
            counts = Counter(r["status"] for r in pair_records)
            asset_counts = Counter(a["status"] for a in asset_records)
            primary = aggregate_primary(list(counts.elements()), has_registry=True, role=role, missing_asset=missing_assets)
            entry_rec = {
                "schema_version": "r5.seed_sweep_entry_record.v0",
                "entry_id": entry_id,
                "has_registry": True,
                "registry_path": rel(registry_path),
                "recommended_role": role,
                "resource_category": category,
                "source_work_title": (registry.get("source_work") or {}).get("title"),
                "primary_entry_status": primary,
                "entry_statuses": sorted(counts.keys(), key=lambda s: STATUS_ORDER.index(s) if s in STATUS_ORDER else 99),
                "status_reason_code": f"R5.SWEEP.entry_primary_{primary}",
                "status_counts_by_pair": dict(sorted(counts.items())),
                "status_counts_by_asset": dict(sorted(asset_counts.items())),
                "pair_record_count": len(pair_records),
                "asset_record_count": len(asset_records),
                "source_inventory": registry.get("source_inventory"),
                "pair_sets": registry.get("pair_sets", []),
                "handoff_target": "r6_candidate" if primary == "converted" else "r7_eligibility_review" if primary == "partial" else "r8_negative_evidence" if primary == "blocked" else "asset_repair_required" if primary == "missing_asset" else "followup_seed_generation_pr_required_before_r7_or_excluded_by_r7" if primary == "needs_generation" else "related_work_or_excluded",
                "repair_contribution_allowed": False,
            }
            entry_records.append(entry_rec)

            if len(pair_records) > PAIR_ARCHIVE_THRESHOLD or len(json.dumps(pair_records, ensure_ascii=False).encode("utf-8")) > ARCHIVE_SIZE_THRESHOLD:
                zip_path = archive_dir / f"{entry_id}_records.zip"
                member_root = f"{entry_id}_records"
                with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
                    for rec in pair_records:
                        member = f"{member_root}/{rec['record_id'].replace('::','__')}.json"
                        payload = json.dumps(rec, ensure_ascii=False, indent=2, sort_keys=True).encode("utf-8")
                        zf.writestr(member, payload)
                        index_records.append({
                            "record_type": "pair",
                            "record_id": rec["record_id"],
                            "entry_id": entry_id,
                            "asset_id": rec.get("source_asset_id"),
                            "pair_id": rec.get("pair_id"),
                            "status": rec.get("status"),
                            "path_in_zip": member,
                            "archive_path": rel(zip_path),
                            "sha256": sha256_bytes(payload),
                        })
                archives.append({
                    "archive_path": rel(zip_path),
                    "sha256": sha256_file(zip_path),
                    "record_count": len(pair_records),
                    "schema_version": "r5.seed_sweep_pair_record.v0",
                    "internal_root": member_root,
                    "generation_command": "python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error",
                    "bytes": zip_path.stat().st_size,
                })
            else:
                for rec in pair_records:
                    rec_path = audit_dir / f"{rec['record_id'].replace('::','__')}.json"
                    write_json(rec_path, rec)
                    index_records.append({
                        "record_type": "pair",
                        "record_id": rec["record_id"],
                        "entry_id": entry_id,
                        "asset_id": rec.get("source_asset_id"),
                        "pair_id": rec.get("pair_id"),
                        "status": rec.get("status"),
                        "path_on_disk": rel(rec_path),
                        "sha256": sha256_file(rec_path),
                    })

            for asset_rec in asset_records:
                asset_path = audit_dir / f"{asset_rec['record_id'].replace('::','__')}.json"
                write_json(asset_path, asset_rec)
                index_records.append({
                    "record_type": "asset",
                    "record_id": asset_rec["record_id"],
                    "entry_id": entry_id,
                    "asset_id": asset_rec.get("asset_id"),
                    "pair_id": None,
                    "status": asset_rec.get("status"),
                    "path_on_disk": rel(asset_path),
                    "sha256": sha256_file(asset_path),
                })

    entry_counts = Counter(e["primary_entry_status"] for e in entry_records)
    pair_counts = Counter(p["status"] for p in pair_records_all)
    asset_counts = Counter(a["status"] for a in asset_records_all)
    meta = {
        "schema_version": "r5.seed_sweep_report.v0",
        "created_at": now_iso(),
        "repo_commit": git_commit(),
        "denominator_freeze_commit": git_commit(),
        "generation_context": generation_context(
            "python -m paper_stm_repair_smoke.cli run-seed-sweep --max-per-pair-seconds 30 --continue-on-error",
            [SMOKE_ROOT / "schemas/seed_sweep_report.schema.json"],
        ),
        "seed_library_dir": rel(SEED_LIBRARY_DIR),
        "entry_dir_count": len(entries),
        "registry_entry_count": sum(1 for e in entries if (e / "seed_resource_registry.json").exists()),
        "unregistered_entry_count": sum(1 for e in entries if not (e / "seed_resource_registry.json").exists()),
        "excluded_non_entry_dirs": excluded_dirs,
        "excluded_auxiliary_files": excluded_files,
        "max_per_pair_seconds": args.max_per_pair_seconds,
        "continue_on_error": args.continue_on_error,
        "repair_contribution_allowed": False,
    }
    report = {
        "schema_version": "r5.seed_sweep_report.v0",
        "run_id": "r5-seed-library-sweep",
        "meta": meta,
        "summary": {
            "entry_status_counts": dict(sorted(entry_counts.items())),
            "pair_status_counts": dict(sorted(pair_counts.items())),
            "asset_status_counts": dict(sorted(asset_counts.items())),
            "entries_total": len(entry_records),
            "pair_records_total": len(pair_records_all),
            "asset_records_total": len(asset_records_all),
            "archives_total": len(archives),
        },
        "entries": sorted(entry_records, key=lambda x: x["entry_id"]),
    }
    write_json(out_dir / "sweep_report.json", report)
    write_json(out_dir / "records_index.json", {"schema_version": "r5.records_index.v0", "records": sorted(index_records, key=lambda x: x["record_id"])})
    write_json(out_dir / "archive_manifest.json", {
        "schema_version": "r5.archive_manifest.v0",
        "archives": archives,
        "policy": {
            "record_archiving_rule": "High-cardinality pair records are stored in per-entry zip archives when record count > 50 or serialized bytes > 5 MiB.",
            "archive_path_base": "repository_root",
            "path_resolution": "archive_path values are relative to repository root; path_in_zip values are relative to archive internal_root.",
            "repair_contribution_allowed": False,
        },
    })
    write_sweep_summaries(out_dir, report, pair_records_all, archives)
    write_handoffs(pair_records_all, entry_records)
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0


def rows_for_status(records: list[dict[str, Any]], statuses: set[str], limit: int = 20) -> list[dict[str, Any]]:
    return [r for r in sorted(records, key=lambda x: (x.get("status") or "", x.get("entry_id") or "", str(x.get("pair_id") or ""))) if r.get("status") in statuses][:limit]


def sorted_status_rows(records: list[dict[str, Any]], statuses: set[str]) -> list[dict[str, Any]]:
    return [
        r
        for r in sorted(records, key=lambda x: (x.get("status") or "", x.get("entry_id") or "", str(x.get("pair_id") or "")))
        if r.get("status") in statuses
    ]


def pr_body_sampling_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Implement the R5 PR-body sampling contract: first 3, plus median/tail for >100."""
    if len(rows) <= 3:
        return rows
    indices = {0, 1, 2}
    if len(rows) > 100:
        indices.update({len(rows) // 2, len(rows) - 1})
    return [rows[i] for i in sorted(indices)]


def bounded_even_sample(rows: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    """Bounded representative handoff sample; includes head/tail and spreads rows across the sorted list."""
    if len(rows) <= limit:
        return rows
    if limit <= 1:
        return rows[:limit]
    n = len(rows)
    indices = sorted({round(i * (n - 1) / (limit - 1)) for i in range(limit)})
    return [rows[i] for i in indices]


def write_sweep_summaries(out_dir: Path, report: dict[str, Any], pair_records: list[dict[str, Any]], archives: list[dict[str, Any]]) -> None:
    lines = [
        "# R5 seed library 全量转换摸排摘要",
        "",
        "本文件由 `run-seed-sweep` 生成。事实源是 [sweep_report.json](./sweep_report.json)，本 Markdown 只做人类入口。",
        "",
        "## 1. denominator",
        "",
        f"- entry directories: {report['meta']['entry_dir_count']}",
        f"- registry entries: {report['meta']['registry_entry_count']}",
        f"- unregistered entries: {report['meta']['unregistered_entry_count']}",
        f"- excluded non-entry dirs: `{', '.join(report['meta']['excluded_non_entry_dirs'])}`",
        "",
        "## 2. entry 状态统计",
        "",
        "| status | entries |",
        "|---|---:|",
    ]
    for status, count in sorted(report["summary"]["entry_status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## 3. pair 状态统计", "", "| status | pairs |", "|---|---:|"])
    for status, count in sorted(report["summary"]["pair_status_counts"].items()):
        lines.append(f"| `{status}` | {count} |")
    lines.extend(["", "## 4. entry 明细", "", "| entry_id | primary | statuses | pairs | assets | handoff |", "|---|---|---|---:|---:|---|"])
    for e in report["entries"]:
        lines.append(f"| `{e['entry_id']}` | `{e['primary_entry_status']}` | `{', '.join(e.get('entry_statuses', []))}` | {e.get('pair_record_count', 0)} | {e.get('asset_record_count', 0)} | `{e.get('handoff_target')}` |")
    lines.extend(["", "## 5. archive", "", f"- archives: {len(archives)}", "- index: [records_index.json](./records_index.json)", "- manifest: [archive_manifest.json](./archive_manifest.json)", ""])
    (out_dir / "sweep_summary.md").write_text("\n".join(lines), encoding="utf-8")

    def case_md(title: str, statuses: set[str], filename: str) -> None:
        all_rows = sorted_status_rows(pair_records, statuses)
        rows = all_rows[:40]
        if len(all_rows) > len(rows):
            scope_note = f"> 本文件仅列出前 {len(rows)} 条抽样记录（{len(rows)}/{len(all_rows)}）；完整清单以 [records_index.json](./records_index.json) 和 [sweep_report.json](./sweep_report.json) 为准。"
        else:
            scope_note = f"> 本文件列出该类别全部记录（{len(rows)}/{len(all_rows)}）；机器事实源仍以 [records_index.json](./records_index.json) 和 [sweep_report.json](./sweep_report.json) 为准。"
        text = [f"# {title}", "", scope_note, "", "事实源为 [sweep_report.json](./sweep_report.json) 与 [records_index.json](./records_index.json)。", "", "| entry | pair | status | reason | handoff |", "|---|---|---|---|---|"]
        if not rows:
            text.append("| `<none>` | `<none>` | `<none>` | 该类别为空，见 sweep_report.json 机器统计。 | `<none>` |")
        for r in rows:
            text.append(f"| `{r.get('entry_id')}` | `{r.get('pair_id')}` | `{r.get('status')}` | `{r.get('status_reason_code')}` | `{r.get('handoff_target')}` |")
        (out_dir / filename).write_text("\n".join(text) + "\n", encoding="utf-8")

    case_md("R5 blocked / missing_asset cases", {"blocked", "missing_asset"}, "blocked_cases.md")
    case_md("R5 partial cases", {"partial"}, "partial_cases.md")
    write_sampling_analysis(out_dir / "sampling_analysis.md", pair_records)


def write_sampling_analysis(path: Path, pair_records: list[dict[str, Any]]) -> None:
    groups = {
        "converted": [r for r in pair_records if r.get("status") == "converted"],
        "partial": [r for r in pair_records if r.get("status") == "partial"],
        "blocked_or_missing": [r for r in pair_records if r.get("status") in {"blocked", "missing_asset"}],
        "not_applicable": [r for r in pair_records if r.get("status") == "not_applicable"],
        "needs_generation": [r for r in pair_records if r.get("status") == "needs_generation"],
    }
    lines = [
        "# R5 seed sweep 抽样分析",
        "",
        "抽样规则：每个状态组内按 `status -> entry_id -> pair_id` 排序，每类至少取前 3 条；若该类超过 100 条，再追加中位与末尾各 1 条。高基数全量明细仍以 archive / records_index 为准。",
        "",
    ]
    for name, rows in groups.items():
        rows = sorted(rows, key=lambda x: (x.get("status") or "", x.get("entry_id") or "", str(x.get("pair_id") or "")))
        sample = pr_body_sampling_rows(rows)
        lines.extend([f"## {name}", "", f"- machine count: {len(rows)}", ""])
        if not sample:
            lines.append("该类别为空；为空依据是 pair-level machine count 为 0。\n")
            continue
        lines.extend(["| entry | pair | status | reason | 学术解释 |", "|---|---|---|---|---|"])
        for r in sample:
            explanation = {
                "converted": "可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。",
                "partial": "可作为后续 eligibility review 对象；不能无条件进入主实验。",
                "blocked": "当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。",
                "missing_asset": "资产证据链缺口；先修一手资源，不进入主实验。",
                "not_applicable": "不是作者一手 generated seed；只保留为相关工作或排除证据。",
                "needs_generation": "需另开 generation PR 复跑；R5 不生成。",
            }.get(r.get("status"), "需人工复核。")
            lines.append(f"| `{r.get('entry_id')}` | `{r.get('pair_id')}` | `{r.get('status')}` | `{r.get('status_reason_code')}` | {explanation} |")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_handoffs(pair_records: list[dict[str, Any]], entry_records: list[dict[str, Any]]) -> None:
    handoff_dir = SMOKE_ROOT / "handoff"
    handoff_dir.mkdir(parents=True, exist_ok=True)
    converted = [r for r in pair_records if r.get("status") == "converted"]
    partial = [r for r in pair_records if r.get("status") == "partial"]
    negative = [r for r in pair_records if r.get("status") in {"blocked", "missing_asset", "not_applicable", "needs_generation"}]
    converted_sorted = sorted_status_rows(converted, {"converted"})
    partial_sorted = sorted_status_rows(partial, {"partial"})
    converted_sample = bounded_even_sample(converted_sorted, 50)
    partial_sample = bounded_even_sample(partial_sorted, 100)
    common = {"schema_version": "r5.handoff.v0", "created_at": now_iso(), "repo_commit": git_commit(), "repair_contribution_allowed": False}
    write_json(handoff_dir / "r5_to_r6_repair_inputs.json", {**common, "handoff_target": "r6_candidate", "summary": {"converted": len(converted)}, "items": converted, "notes": "Only pre-repair converted candidates. R6 still must run its own eligibility gates; R5 does not execute repair."})
    write_json(handoff_dir / "r5_to_r7_seed_eligibility.json", {
        **common,
        "handoff_target": "r7_seed_eligibility_review",
        "summary": {"converted": len(converted), "partial": len(partial), "entries": len(entry_records)},
        "sample_policy": "bounded_even_sample over rows sorted by status -> entry_id -> pair_id; samples are navigation aids, not full eligibility lists",
        "sample_limits": {"converted_sample": 50, "partial_sample": 100},
        "sample_counts": {"converted_sample": len(converted_sample), "partial_sample": len(partial_sample)},
        "sample_truncated": {"converted": len(converted_sorted) > len(converted_sample), "partial": len(partial_sorted) > len(partial_sample)},
        "full_list_via": {
            "records_index": rel(SMOKE_ROOT / "seed_library_sweep/records_index.json"),
            "archive_manifest": rel(SMOKE_ROOT / "seed_library_sweep/archive_manifest.json"),
            "filter": "record_type == 'pair' and status in {'converted', 'partial'}",
        },
        "converted_sample": converted_sample,
        "partial_sample": partial_sample,
    })
    write_json(handoff_dir / "r5_to_r8_negative_evidence.json", {**common, "handoff_target": "r8_negative_evidence", "summary": dict(Counter(r.get("status") for r in negative)), "items": negative[:300]})



LLMS_EMP_ENTRY_ID = "llms-emp-stm-subset"
LLMS_EMP_SWEEP_DIR = SMOKE_ROOT / "seed_library_sweep"
LLMS_EMP_PAIRS_PATH = SEED_LIBRARY_DIR / "llms-emp-stm-subset/assets/extracted/pairs.jsonl"
LLMS_EMP_ARCHIVE_PATH = LLMS_EMP_SWEEP_DIR / "archives/llms-emp-stm-subset_records.zip"
LLMS_EMP_STATUS_ORDER = {"converted": 0, "partial": 1, "blocked": 2}
LLM_FAMILY_NORMALIZED = {
    "GPT-4o": "gpt-4o",
    "GPT-4": "gpt-4",
    "Llama": "llama",
    "Kimi": "kimi",
    "DeepSeek": "deepseek",
    "Claude": "claude",
}
LLM_FAMILY_ORDER = ["gpt-4o", "gpt-4", "llama", "kimi", "deepseek", "claude"]
SELECTED_R55_SMOKE_EXAMPLES = [
    "llms-emp-gpt4o-hldcs",
    "sefm-ssc7-umple",
    "llms-emp-deepseek-microwave",
    "llms-emp-kimi-autonomous-collision",
]
LOSS_ATTRIBUTION_MAP = {
    "R5.LOSS.r3_1_normalization_replay_not_repair": {
        "observed_issue": "pre-SCXML normalization replay was required; this is conversion readiness, not repair gain",
        "source_stage": "plantuml_toolchain",
        "primary_attribution": "pipeline_artifact",
        "secondary_attributions": ["plantuml_toolchain"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R45.LOSS.condition_like_label_lowered_as_event": {
        "observed_issue": "condition-like transition label was preserved as an event label rather than a verified guard",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "r5_7_candidate_only",
        "secondary_attributions": ["seed_defect", "fcstm_lowering"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": True,
        "confidence": "medium",
    },
    "R45.LOSS.source_lifted_to_composite_boundary": {
        "observed_issue": "source endpoint was lifted to a composite-state boundary during representation lowering",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "fcstm_lowering",
        "secondary_attributions": ["scxml_canonical"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R45.LOSS.target_lifted_to_composite_boundary": {
        "observed_issue": "target endpoint was lifted to a composite-state boundary during representation lowering",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "fcstm_lowering",
        "secondary_attributions": ["scxml_canonical"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R45.LOSS.composite_target_lowered_to_initial_child": {
        "observed_issue": "transition into a composite target was lowered to an initial child",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "fcstm_lowering",
        "secondary_attributions": ["scxml_canonical"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R45.LOSS.cross_scope_transition_unrepresentable": {
        "observed_issue": "cross-scope transition could not be represented without hierarchy approximation",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "fcstm_lowering",
        "secondary_attributions": ["scxml_canonical"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R45.LOSS.initial_inferred_from_source_order_or_start_state": {
        "observed_issue": "initial child was inferred from source order or start-state convention",
        "source_stage": "fcstm_lowering",
        "primary_attribution": "fcstm_lowering",
        "secondary_attributions": ["pipeline_artifact"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
    "R5.LOSS.official_scxml_unavailable": {
        "observed_issue": "official PlantUML SCXML export was unavailable after raw and normalized probes",
        "source_stage": "plantuml_toolchain",
        "primary_attribution": "plantuml_toolchain",
        "secondary_attributions": ["unknown"],
        "pipeline_artifact": True,
        "r5_7_candidate_only": False,
        "confidence": "high",
    },
}
LOSS_PRIORITY = [
    "R5.LOSS.official_scxml_unavailable",
    "R45.LOSS.condition_like_label_lowered_as_event",
    "R5.LOSS.r3_1_normalization_replay_not_repair",
    "R45.LOSS.cross_scope_transition_unrepresentable",
    "R45.LOSS.source_lifted_to_composite_boundary",
    "R45.LOSS.target_lifted_to_composite_boundary",
    "R45.LOSS.composite_target_lowered_to_initial_child",
    "R45.LOSS.initial_inferred_from_source_order_or_start_state",
]


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def slugify(text: str, max_len: int = 48) -> str:
    s = re.sub(r"[^0-9A-Za-z]+", "_", text.strip().lower()).strip("_")
    return (s[:max_len].strip("_") or "unknown")


def llms_emp_cluster_id(index: int, row: dict[str, Any]) -> str:
    source = slugify(str(row.get("model_source") or "source"), 16)
    name = slugify(str(row.get("model_name") or "model"), 34)
    return f"llms_emp_nl_{index:02d}_{source}_{name}"


def normalize_llm_family(value: str | None) -> str:
    return LLM_FAMILY_NORMALIZED.get(str(value or ""), slugify(str(value or "unknown"), 20))


def load_llms_emp_pairs() -> list[dict[str, Any]]:
    return read_jsonl(LLMS_EMP_PAIRS_PATH)


def load_llms_emp_sweep_records() -> list[dict[str, Any]]:
    if not LLMS_EMP_ARCHIVE_PATH.exists():
        return []
    with zipfile.ZipFile(LLMS_EMP_ARCHIVE_PATH) as zf:
        return [json.loads(zf.read(name).decode("utf-8")) for name in sorted(zf.namelist()) if name.endswith(".json")]


def load_llms_emp_index_records() -> dict[str, dict[str, Any]]:
    index_path = LLMS_EMP_SWEEP_DIR / "records_index.json"
    if not index_path.exists():
        return {}
    index = load_json(index_path)
    return {str(r.get("pair_id")): r for r in index.get("records", []) if r.get("entry_id") == LLMS_EMP_ENTRY_ID and r.get("record_type") == "pair"}



def llms_emp_behavior_features(nl_text: str, model_name: str, model_source: str) -> dict[str, bool]:
    """Cluster-level behavior-feature profile used by R5.6 scope decisions.

    This is intentionally a conservative feature census, not a repair-target
    adjudication. R5.7 must still inspect NL and raw STM_0 before confirming
    any guard/event/action defect.
    """
    lower = f"{model_source} {model_name} {nl_text}".lower()
    has_explicit_time = any(token in lower for token in [" second", " seconds", "timer", "cooking time", "execution time", "maximum of", "minimum of"])
    has_guard_like_condition = any(token in lower for token in [" if ", " when ", "condition", "based on", "detected", "receives", "receive", "=true", "<", ">", "less than", "front_distance", "dist_to_"])
    has_action_or_entry_exit = any(token in lower for token in ["entry", "exit", "send", "start", "stop", "accelerate", "decelerate", "brake", "cancel", "open", "close", "attack", "search"])
    has_variables_or_data_conditions = any(token in lower for token in ["front_distance", "dist_to_front", "dist_to_exit", "memfull", "sunny", "charged", "prob", "=true", "<", ">", "zero time", "timer"])
    has_hierarchy = any(token in lower for token in ["sub-state", "substates", "substate", "sub-machine", "sub machine", "within", "regions", "orthogonal", "operate state", "highwaymode", "urbanmode"])
    has_pseudostate = any(token in lower for token in ["initialstate", "initial state", "finalstate", "final state", "finishstate", "fork", "join", "choice", "junction", "[*]"])
    has_concurrency_or_regions = any(token in lower for token in ["parallel", "orthogonal", "concurrent", "regions", "fork", "join"])
    return {
        "has_guard_like_condition": has_guard_like_condition,
        "has_action_or_entry_exit": has_action_or_entry_exit,
        "has_variables_or_data_conditions": has_variables_or_data_conditions,
        "has_hierarchy": has_hierarchy,
        "has_pseudostate": has_pseudostate,
        "has_explicit_time": has_explicit_time,
        "has_concurrency_or_regions": has_concurrency_or_regions,
    }

def llms_emp_cluster_specs(pairs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    first_by_nl: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for row in pairs:
        sha = str(row.get("nl_sha256"))
        if sha not in first_by_nl:
            first_by_nl[sha] = row
            order.append(sha)
    specs: dict[str, dict[str, Any]] = {}
    for index, sha in enumerate(order):
        row = first_by_nl[sha]
        name = str(row.get("model_name") or "")
        source = str(row.get("model_source") or "")
        cid = llms_emp_cluster_id(index, row)
        lower = f"{source} {name}".lower()
        if "digital camera" in lower:
            structure = "UML-SysML statechart"
            time_level = "T1"
            role = "supplementary_stress"
            task_type = "相机控制：显式执行时间与伪状态压力样例"
            time_note = "NL 含秒级执行时间、fork/join 与概率/守卫式线索；不能作为 T0 主结论证据。"
        elif "microwave" in lower:
            structure = "UML-SysML statechart"
            time_level = "T0.5"
            role = "main_candidate"
            task_type = "微波炉控制：timer-like caveat"
            time_note = "NL 提到 cooking time 与 timer expires，但没有形式化 clock 语义；本阶段按 T0.5 timer-like caveat 处理。"
        elif "collision" in lower:
            structure = "UML-SysML statechart"
            time_level = "T0"
            role = "main_candidate"
            task_type = "碰撞规避模式控制"
            time_note = "无显式 clock / duration；主要 caveat 是并发/正交区域语义。"
        elif "high-level driving" in lower or "autonomous mode" in lower:
            structure = "HSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "自动驾驶模式控制"
            time_note = "距离/模式条件是离散守卫式线索；无显式 clock。"
        elif "pump" in lower:
            structure = "HSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "泵子系统模式控制"
            time_note = "离散模式/状态切换；无显式 timing。"
        elif "hybrid sport" in lower or "hsuv" in lower:
            structure = "HSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "车辆运行模式控制"
            time_note = "用户/动作驱动的离散模式切换；无显式 timing。"
        elif "train control" in lower:
            structure = "HSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "列车运动控制"
            time_note = "存在 entry/action-like 标签，但无 clock/duration 语义。"
        elif "brake" in lower:
            structure = "FSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "制动子系统控制"
            time_note = "“after entering”等顺序短语是 ordering cue，不是 clock 约束。"
        elif "uav" in lower:
            structure = "HSM"
            time_level = "T0"
            role = "main_candidate"
            task_type = "无人机群任务控制"
            time_note = "离散任务状态迁移；无显式 timing。"
        else:
            structure = "unknown"
            time_level = "unknown"
            role = "unknown"
            task_type = "unknown"
            time_note = "没有命中 R5.5 cluster 规则；保持保守。"
        nl_text = str(row.get("nl_text") or "")
        specs[sha] = {
            "nl_cluster_id": cid,
            "nl_cluster_index": index,
            "nl_sha256": sha,
            "model_source": source,
            "model_name": name,
            "task_type": task_type,
            "structure_family": structure,
            "time_level": time_level,
            "time_level_note": time_note,
            "control_system_type": "control_system",
            "r5_6_story_role": role,
            "nl_source_locator": row.get("source_locator"),
            "nl_text_excerpt": nl_text[:800],
            "behavior_feature_profile": llms_emp_behavior_features(nl_text, name, source),
            "behavior_feature_note": "R5.5 feature census only; R5.7 must adjudicate guard/event/action targets case by case from NL + raw STM_0.",
        }
    return specs


def primary_loss_code(codes: list[str]) -> str:
    for code in LOSS_PRIORITY:
        if code in codes:
            return code
    return codes[0] if codes else "none"


def attribution_for_codes(codes: list[str]) -> dict[str, Any]:
    code = primary_loss_code(codes)
    base = LOSS_ATTRIBUTION_MAP.get(code)
    if base is None:
        if not codes:
            return {
                "r5_loss_code": "none",
                "observed_issue": "none",
                "source_stage": "raw_seed",
                "primary_attribution": "unknown",
                "secondary_attributions": [],
                "pipeline_artifact": False,
                "r5_7_candidate_only": False,
                "attribution_confidence": "unknown",
            }
        return {
            "r5_loss_code": code,
            "observed_issue": "unmapped loss code; keep in risk table",
            "source_stage": "unknown",
            "primary_attribution": "unknown",
            "secondary_attributions": [],
            "pipeline_artifact": True,
            "r5_7_candidate_only": False,
            "attribution_confidence": "unknown",
        }
    secondary = set(base.get("secondary_attributions", []))
    for extra_code in codes:
        extra = LOSS_ATTRIBUTION_MAP.get(extra_code)
        if extra:
            secondary.update(extra.get("secondary_attributions", []))
            if extra.get("primary_attribution") != base.get("primary_attribution"):
                secondary.add(str(extra.get("primary_attribution")))
    return {
        "r5_loss_code": code,
        "observed_issue": base["observed_issue"],
        "source_stage": base["source_stage"],
        "primary_attribution": base["primary_attribution"],
        "secondary_attributions": sorted(s for s in secondary if s and s != base.get("primary_attribution")),
        "pipeline_artifact": bool(base["pipeline_artifact"] or any((LOSS_ATTRIBUTION_MAP.get(c) or {}).get("pipeline_artifact") for c in codes)),
        "r5_7_candidate_only": bool(base["r5_7_candidate_only"] or any((LOSS_ATTRIBUTION_MAP.get(c) or {}).get("r5_7_candidate_only") for c in codes)),
        "attribution_confidence": base["confidence"],
    }


def story_role_for_pair(status: str, cluster: dict[str, Any], codes: list[str], attribution: dict[str, Any]) -> str:
    if status == "blocked":
        return "negative_evidence"
    if cluster.get("time_level") in {"T1", "T2+ out-of-scope"}:
        return "supplementary_stress"
    # R5.5 is a pre-repair census. T0/T0.5 partial rows remain main-pool
    # candidates with attribution caveats; conversion/representation loss is
    # excluded from repair gain later instead of excluding the seed here.
    return "main_candidate"


def llms_emp_record_evidence_anchor(index_rec: dict[str, Any] | None, pointer: str) -> str:
    if not index_rec:
        return pointer
    if index_rec.get("path_in_zip"):
        return f"{index_rec.get('archive_path')}::{index_rec.get('path_in_zip')}#{pointer}"
    return f"{index_rec.get('path_on_disk')}#{pointer}"


def recovery_item_index() -> dict[str, dict[str, Any]]:
    if not RECOVERY_REPORT_PATH.exists():
        return {}
    doc = load_json(RECOVERY_REPORT_PATH)
    return {str(item.get("pair_id")): item for item in doc.get("items", []) if item.get("seed_id") == LLMS_EMP_ENTRY_ID}


def run_llms_emp_profile(_: argparse.Namespace) -> int:
    pairs = load_llms_emp_pairs()
    sweep_records = {r["pair_id"]: r for r in load_llms_emp_sweep_records()}
    index_records = load_llms_emp_index_records()
    recovery_items = recovery_item_index()
    clusters = llms_emp_cluster_specs(pairs)
    out_dir = LLMS_EMP_SWEEP_DIR

    case_rows: list[dict[str, Any]] = []
    cluster_matrix_rows: list[dict[str, Any]] = []
    partial_rows: list[dict[str, Any]] = []
    blocked_rows: list[dict[str, Any]] = []
    for row in sorted(pairs, key=lambda x: x["pair_id"]):
        pair_id = str(row["pair_id"])
        rec = sweep_records[pair_id]
        index_rec = index_records.get(pair_id)
        cluster = clusters[str(row["nl_sha256"])]
        codes = list(rec.get("loss_reason_codes") or [])
        attr = attribution_for_codes(codes)
        status = str(rec.get("status"))
        llm_family = normalize_llm_family(row.get("llm"))
        observed_issue = "none" if status == "converted" and not codes else attr["observed_issue"]
        source_stage = "raw_seed" if status == "converted" and not codes else attr["source_stage"]
        story_role = story_role_for_pair(status, cluster, codes, attr)
        evidence_path = index_rec.get("archive_path") if index_rec else rel(LLMS_EMP_ARCHIVE_PATH)
        evidence_anchor = llms_emp_record_evidence_anchor(index_rec, "/loss_reason_codes")
        case = {
            "schema_version": "r5_5.llms_emp_case_matrix.v0",
            "seed_id": LLMS_EMP_ENTRY_ID,
            "nl_cluster_id": cluster["nl_cluster_id"],
            "nl_cluster_index": cluster["nl_cluster_index"],
            "raw_pair_id": pair_id,
            "llm_family": llm_family,
            "llm_output_id": pair_id,
            "generation_model_or_method": row.get("generation_model_or_method"),
            "nl_source_locator": row.get("source_locator"),
            "stm_source_locator": row.get("source_locator"),
            "nl_sha256": row.get("nl_sha256"),
            "stm0_sha256": row.get("stm0_sha256"),
            "source_sha256": row.get("source_sha256"),
            "conversion_status": status,
            "status_reason_code": rec.get("status_reason_code"),
            "structure_family": cluster["structure_family"],
            "time_level": cluster["time_level"],
            "control_system_type": cluster["control_system_type"],
            "observed_issue": observed_issue,
            "source_stage": source_stage,
            "r5_loss_codes": codes,
            "canonical_status": rec.get("canonical_status"),
            "parse_status": rec.get("parse_status"),
            "inspect_status": rec.get("inspect_status"),
            "fcstm_sha256": rec.get("fcstm_sha256"),
            "repair_contribution_allowed": False,
            "r5_6_story_role": story_role,
            "evidence_path": evidence_path,
            "evidence_anchor": evidence_anchor,
        }
        case_rows.append(case)
        cluster_matrix_rows.append({
            "schema_version": "r5_5.llms_emp_cluster_llm_matrix.v0",
            "nl_cluster_id": cluster["nl_cluster_id"],
            "nl_cluster_index": cluster["nl_cluster_index"],
            "llm_family": llm_family,
            "raw_pair_id": pair_id,
            "conversion_status": status,
            "structure_family": cluster["structure_family"],
            "time_level": cluster["time_level"],
            "primary_issue": observed_issue,
            "r5_loss_codes": codes,
            "r5_6_story_role": story_role,
        })
        if status == "partial":
            partial_rows.append({
                "schema_version": "r5_5.llms_emp_partial_attribution.v0",
                "seed_id": LLMS_EMP_ENTRY_ID,
                "nl_cluster_id": cluster["nl_cluster_id"],
                "raw_pair_id": pair_id,
                "llm_family": llm_family,
                "conversion_status": status,
                "observed_issue": observed_issue,
                "source_stage": source_stage,
                "r5_loss_code": attr["r5_loss_code"],
                "r5_loss_codes": codes,
                "primary_attribution": attr["primary_attribution"],
                "secondary_attributions": attr["secondary_attributions"],
                "evidence_path": evidence_path,
                "evidence_anchor": evidence_anchor,
                "diagnostic_or_tool_code": attr["r5_loss_code"],
                "pipeline_artifact": attr["pipeline_artifact"],
                "r5_7_candidate_only": attr["r5_7_candidate_only"],
                "attribution_confidence": attr["attribution_confidence"],
                "r5_6_story_role": story_role,
                "notes": "R5.5 attribution is pre-repair only; do not count conversion or lowering gain as repair gain.",
            })
        if status == "blocked":
            recovery = recovery_items.get(pair_id, {})
            raw_preflight = recovery.get("raw_preflight") or {}
            normalized_preflight = recovery.get("normalized_preflight") or {}
            blocked_rows.append({
                "raw_pair_id": pair_id,
                "nl_cluster_id": cluster["nl_cluster_id"],
                "llm_family": llm_family,
                "model_name": row.get("model_name"),
                "issue_category": recovery.get("issue_category"),
                "raw_command": raw_preflight.get("command"),
                "normalized_command": normalized_preflight.get("command"),
                "tool_name": normalized_preflight.get("tool_name") or raw_preflight.get("tool_name"),
                "tool_version_head": normalized_preflight.get("tool_version_head") or raw_preflight.get("tool_version_head"),
                "raw_syntax_status": raw_preflight.get("syntax_status"),
                "normalized_syntax_status": normalized_preflight.get("syntax_status"),
                "raw_scxml_returncode": raw_preflight.get("scxml_returncode"),
                "normalized_scxml_returncode": normalized_preflight.get("scxml_returncode"),
                "stderr_tail": normalized_preflight.get("stderr_tail") or raw_preflight.get("stderr_tail"),
                "stdout_tail": normalized_preflight.get("stdout_tail") or raw_preflight.get("stdout_tail"),
                "raw_candidate_path": recovery.get("raw_candidate_path"),
                "normalized_candidate_path": recovery.get("normalized_candidate_path"),
                "raw_conversion_pass": recovery.get("raw_conversion_pass"),
                "normalized_conversion_pass": recovery.get("normalized_conversion_pass"),
                "render_status": "unknown_from_committed_r5_evidence",
                "pre_scxml_recovery_possible": bool(recovery.get("normalized_conversion_pass")),
                "evidence_path": rel(RECOVERY_REPORT_PATH),
                "evidence_anchor": f"/items[pair_id={pair_id}]/normalized_preflight",
            })

    cluster_profiles: list[dict[str, Any]] = []
    for sha, cluster in sorted(clusters.items(), key=lambda kv: kv[1]["nl_cluster_index"]):
        rows = [c for c in case_rows if c["nl_cluster_id"] == cluster["nl_cluster_id"]]
        cluster_profiles.append({
            "schema_version": "r5_5.llms_emp_cluster_profile.v0",
            **cluster,
            "raw_pair_count": len(rows),
            "llm_families": sorted({r["llm_family"] for r in rows}, key=lambda x: LLM_FAMILY_ORDER.index(x) if x in LLM_FAMILY_ORDER else 99),
            "status_counts": dict(sorted(Counter(r["conversion_status"] for r in rows).items())),
            "time_level_counts": dict(sorted(Counter(r["time_level"] for r in rows).items())),
            "structure_family_counts": dict(sorted(Counter(r["structure_family"] for r in rows).items())),
            "loss_code_counts": dict(sorted(Counter(code for r in rows for code in r["r5_loss_codes"]).items())),
            "story_role_counts": dict(sorted(Counter(r["r5_6_story_role"] for r in rows).items())),
        })

    write_jsonl(out_dir / "llms_emp_case_matrix.jsonl", case_rows)
    write_jsonl(out_dir / "llms_emp_cluster_profiles.jsonl", cluster_profiles)
    write_jsonl(out_dir / "llms_emp_cluster_llm_matrix.jsonl", cluster_matrix_rows)
    write_jsonl(out_dir / "llms_emp_partial_attribution_ledger.jsonl", partial_rows)
    write_llms_emp_deep_profile(out_dir / "llms_emp_deep_profile.md", case_rows, cluster_profiles, partial_rows, blocked_rows)
    write_llms_emp_blocked_probe(out_dir / "llms_emp_blocked_probe.md", blocked_rows)
    write_jsonl(out_dir / "llms_emp_blocked_probe.jsonl", blocked_rows)
    write_llms_emp_r56_handoff(out_dir / "llms_emp_r56_handoff.md", case_rows, cluster_profiles, partial_rows, blocked_rows)
    print(json.dumps({
        "cases": len(case_rows),
        "clusters": len(cluster_profiles),
        "partial": len(partial_rows),
        "blocked": len(blocked_rows),
        "decision": "proceed_with_supplementary",
    }, ensure_ascii=False, sort_keys=True))
    return 0


def md_counter_table(counter: Counter | dict[str, int], key_name: str = "项", value_name: str = "数量") -> list[str]:
    lines = [f"| {key_name} | {value_name} |", "|---|---:|"]
    for key, value in sorted(dict(counter).items()):
        lines.append(f"| `{key}` | {value} |")
    return lines


def status_symbol(status: str) -> str:
    return {"converted": "🟢", "partial": "🟡", "blocked": "🔴"}.get(status, "⚪")


def write_llms_emp_deep_profile(path: Path, cases: list[dict[str, Any]], clusters: list[dict[str, Any]], partials: list[dict[str, Any]], blocked: list[dict[str, Any]]) -> None:
    status_counts = Counter(c["conversion_status"] for c in cases)
    llm_status = defaultdict(Counter)
    time_counts = Counter(c["time_level"] for c in cases)
    family_counts = Counter(c["structure_family"] for c in cases)
    role_counts = Counter(c["r5_6_story_role"] for c in cases)
    loss_counts = Counter(code for c in cases for code in c["r5_loss_codes"])
    for c in cases:
        llm_status[c["llm_family"]][c["conversion_status"]] += 1
    by_cluster = defaultdict(dict)
    for c in cases:
        by_cluster[c["nl_cluster_id"]][c["llm_family"]] = c
    lines = [
        "# R5.5 `llms-emp-stm-subset` 主 seed 池深度画像",
        "",
        "本文件由 `python -m paper_stm_repair_smoke.cli run-llms-emp-profile` 生成。机器事实源是 [llms_emp_case_matrix.jsonl](./llms_emp_case_matrix.jsonl)、[llms_emp_cluster_profiles.jsonl](./llms_emp_cluster_profiles.jsonl)、[llms_emp_cluster_llm_matrix.jsonl](./llms_emp_cluster_llm_matrix.jsonl) 与 [llms_emp_partial_attribution_ledger.jsonl](./llms_emp_partial_attribution_ledger.jsonl)。本 Markdown 只做人类阅读入口。",
        "",
        "## 1. 结论",
        "",
        "`llms-emp-stm-subset` 仍是 R6/R7 的主 seed 池，但应按 **proceed_with_supplementary** 口径进入后续阶段：主线可围绕 T0/T0.5 离散状态机族展开；Digital Camera cluster 带显式秒级执行时间与复杂 pseudo-state，应进入 supplementary / stress；3 个 blocked 样例进入 negative evidence / converter follow-up。",
        "",
        "关键纪律：60 个 raw pair 是 10 个唯一 NL × 6 个 LLM 输出，不得在论文中写成 60 个独立需求；conversion / normalization / `.fcstm` lowering 均不得计入 repair gain。",
        "",
        "## 2. 总体统计",
        "",
    ]
    lines += md_counter_table(status_counts, "conversion_status", "pairs")
    lines += ["", "### 2.1 时间等级", ""]
    lines += md_counter_table(time_counts, "time_level", "pairs")
    lines += ["", "### 2.2 结构家族", ""]
    lines += md_counter_table(family_counts, "structure_family", "pairs")
    lines += ["", "### 2.3 R5.6 story role", ""]
    lines += md_counter_table(role_counts, "r5_6_story_role", "pairs")
    cluster_role_counts = Counter(c["r5_6_story_role"] for c in clusters)
    lines += ["", "### 2.4 cluster 口径 story role", ""]
    lines += md_counter_table(cluster_role_counts, "r5_6_story_role", "clusters")
    lines += ["", "### 2.5 行为特征画像", "", "本节是 R5.5 的保守 feature census，只支撑 R5.6 scope 决策；不能直接把某个特征计为 R5.7 已确认 repair target。", "", "| feature | clusters |", "|---|---:|"]
    feature_counts = Counter()
    for cluster in clusters:
        for key, value in (cluster.get("behavior_feature_profile") or {}).items():
            if value:
                feature_counts[key] += 1
    for key, value in sorted(feature_counts.items()):
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "### 2.6 loss code", ""]
    lines += md_counter_table(loss_counts, "loss code", "count")
    lines += ["", "## 3. cluster × LLM 交叉矩阵", "", "符号：🟢 = converted；🟡 = partial；🔴 = blocked。emoji 列只编码状态，具体含义见本段。", "", "| cluster | 模型 / 来源 | time | family | GPT-4o | GPT-4 | Llama | Kimi | DeepSeek | Claude |", "|---|---|---|---|---|---|---|---|---|---|"]
    for cluster in clusters:
        cells = []
        for llm in LLM_FAMILY_ORDER:
            c = by_cluster[cluster["nl_cluster_id"]].get(llm)
            cells.append(f"{status_symbol(c['conversion_status'])} `{c['raw_pair_id'][-4:]}`" if c else "⚪")
        lines.append(f"| `{cluster['nl_cluster_id']}` | {cluster['model_name']} / {cluster['model_source']} | `{cluster['time_level']}` | `{cluster['structure_family']}` | " + " | ".join(cells) + " |")
    lines += ["", "## 4. LLM 维度状态", "", "| LLM | converted | partial | blocked |", "|---|---:|---:|---:|"]
    for llm in LLM_FAMILY_ORDER:
        cnt = llm_status[llm]
        lines.append(f"| `{llm}` | {cnt.get('converted', 0)} | {cnt.get('partial', 0)} | {cnt.get('blocked', 0)} |")
    lines += ["", "## 5. cluster 画像", "", "| cluster | role | 控制语义 | 行为特征 | time note | 状态分布 | 主要 loss |", "|---|---|---|---|---|---|---|"]
    for cluster in clusters:
        losses = ", ".join(f"`{k}`×{v}" for k, v in cluster.get("loss_code_counts", {}).items()) or "无"
        features = ", ".join(f"`{k}`" for k, v in (cluster.get("behavior_feature_profile") or {}).items() if v) or "无"
        lines.append(f"| `{cluster['nl_cluster_id']}` | `{cluster['r5_6_story_role']}` | {cluster['task_type']} | {features} | {cluster['time_level_note']} | {cluster['status_counts']} | {losses} |")
    lines += ["", "## 6. partial 归因摘要", "", "| primary_attribution | count |", "|---|---:|"]
    for key, value in sorted(Counter(p["primary_attribution"] for p in partials).items()):
        lines.append(f"| `{key}` | {value} |")
    lines += ["", "## 7. blocked 摘要", "", "| raw_pair_id | cluster | LLM | issue_category | 当前结论 |", "|---|---|---|---|---|"]
    for b in blocked:
        conclusion = "raw 与 normalized PlantUML 均未获得可信 official SCXML；当前只能进入 negative evidence / converter follow-up。"
        lines.append(f"| `{b['raw_pair_id']}` | `{b['nl_cluster_id']}` | `{b['llm_family']}` | `{b.get('issue_category')}` | {conclusion} |")
    lines += ["", "## 8. 给 R5.6/R5.7 的学术含义", "", "1. 当前主线不宜声称覆盖 timed automata 或任意 UML；主实验应保守限定为 T0/T0.5 的 FSM/HSM/EFSM-lite/statechart 子族。", "2. `condition_like_label_lowered_as_event` 是最接近 R5.7 repair target 的候选问题，但必须逐例回到 NL 证据，不能把所有 event label 都自动升级为 guard。", "3. `r3_1_normalization_replay`、scope lifting、initial inference 等主要是 conversion / representation attribution，不得写成 repair loop 改善。", "4. Digital Camera cluster 可保留为 supplementary / stress，用于说明当前边界为什么不外推到显式时间状态机。", ""]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_llms_emp_blocked_probe(path: Path, blocked: list[dict[str, Any]]) -> None:
    lines = [
        "# R5.5 `llms-emp` blocked probe",
        "",
        "本文件记录 3 个 `R5.LOSS.official_scxml_unavailable` 样例的可复核失败证据。事实源是 [plantuml_recovery_report.json](../../conversion/reports/plantuml_recovery_report.json) 与 [llms_emp_case_matrix.jsonl](./llms_emp_case_matrix.jsonl)。",
        "",
        "## 1. 总结",
        "",
        "3 个 blocked 样例均有作者一手 `NL + generated PlantUML`，但 R3.1 的 raw 与 normalized official PlantUML probe 均未获得可信 SCXML。当前 committed evidence 未证明它们可渲染；只能说明 `-checkonly` / `-tscxml` 路径失败，且当前 normalization rules 未修复。",
        "",
        "注意：当前 committed evidence 只保存 JSON 中的 stdout / stderr tail，没有完整 stdout/stderr log 文件；如后续需要精确错误行，应另开 converter follow-up probe。",
        "",
    ]
    for b in blocked:
        lines += [
            f"## {b['raw_pair_id']} / {b['llm_family']}",
            "",
            f"- cluster: `{b['nl_cluster_id']}`",
            f"- model: {b.get('model_name')}",
            f"- issue_category: `{b.get('issue_category')}`",
            f"- tool: {b.get('tool_name')} / {b.get('tool_version_head')}",
            f"- raw syntax status: `{b.get('raw_syntax_status')}`; normalized syntax status: `{b.get('normalized_syntax_status')}`",
            f"- raw scxml returncode: `{b.get('raw_scxml_returncode')}`; normalized scxml returncode: `{b.get('normalized_scxml_returncode')}`",
            f"- raw candidate: `{b.get('raw_candidate_path')}`",
            f"- normalized candidate: `{b.get('normalized_candidate_path')}`",
            f"- render status: `{b.get('render_status')}`",
            f"- pre-SCXML recovery possible: `{b.get('pre_scxml_recovery_possible')}`",
            f"- evidence: `{b.get('evidence_path')}#{b.get('evidence_anchor')}`",
            "",
            "```text",
            str(b.get("stderr_tail") or "<no stderr tail captured>")[-1200:],
            "```",
            "",
        ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_llms_emp_r56_handoff(path: Path, cases: list[dict[str, Any]], clusters: list[dict[str, Any]], partials: list[dict[str, Any]], blocked: list[dict[str, Any]]) -> None:
    status_counts = Counter(c["conversion_status"] for c in cases)
    time_counts = Counter(c["time_level"] for c in cases)
    cluster_time = Counter(c["time_level"] for c in clusters)
    role_counts = Counter(c["r5_6_story_role"] for c in cases)
    lines = [
        "# R5.5 -> R5.6 story / model scope handoff",
        "",
        "## 1. boundary_decision",
        "",
        "`proceed_with_supplementary`",
        "",
        "理由：10 个 NL cluster 中 8 个为 T0、1 个为 T0.5、1 个为 T1；60 个 pair 中 57 个可进入 `.fcstm` 级别，3 个 blocked 有负证据。主实验可以围绕 T0/T0.5 离散状态机族继续推进，但 Digital Camera cluster 与 blocked pair 应进入 supplementary / stress / negative evidence，而不是主 claim 证据。",
        "",
        "## 2. supporting_counts",
        "",
        f"- pair status: `{dict(sorted(status_counts.items()))}`",
        f"- pair time level: `{dict(sorted(time_counts.items()))}`",
        f"- cluster time level: `{dict(sorted(cluster_time.items()))}`",
        f"- story roles: `{dict(sorted(role_counts.items()))}`",
        f"- partial ledger rows: `{len(partials)}`",
        f"- blocked rows: `{len(blocked)}`",
        "",
        "## 3. blocking_evidence",
        "",
        "- 3 个 blocked 均为 `R5.LOSS.official_scxml_unavailable`，详见 [llms_emp_blocked_probe.md](./llms_emp_blocked_probe.md)。",
        "- Digital Camera cluster 含显式秒级执行时间与复杂 pseudo-state，应避免支撑 T0 主 claim。",
        "- 大量 partial 来自 conversion / representation attribution，不能计入 repair gain。",
        "",
        "## 4. confidence",
        "",
        "`medium-high`：一手 pair / R5 sweep / R3.1 recovery / R4.5 loss 证据完整；但 time level 与 repair target taxonomy 仍需 R5.6/R5.7 正式冻结。",
        "",
        "## 5. r5_7_candidate_summary",
        "",
        "- `R45.LOSS.condition_like_label_lowered_as_event` 是主要 repair target 候选，但必须逐例有 NL 证据。",
        "- 层次 lowering、scope lifting、initial inference 默认是 representation caveat，不直接进入 repair target。",
        "- blocked official SCXML unavailable 是 converter follow-up / negative evidence，不是 repair loop 能直接声称修复的问题。",
        "",
        "## 6. recommended_next_action",
        "",
        "R5.6 应在 `story/model_scope.md` 中冻结 main / supplementary-stress / negative evidence 的模型范围，并把主实验 claim 限定到 T0/T0.5 离散状态机族；R5.7 再定义 guard/event/action/hierarchy 的 repair target。",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def validate_llms_emp_profile(errors: list[str]) -> None:
    out_dir = LLMS_EMP_SWEEP_DIR
    paths = {
        "case": out_dir / "llms_emp_case_matrix.jsonl",
        "cluster": out_dir / "llms_emp_cluster_profiles.jsonl",
        "matrix": out_dir / "llms_emp_cluster_llm_matrix.jsonl",
        "partial": out_dir / "llms_emp_partial_attribution_ledger.jsonl",
        "deep": out_dir / "llms_emp_deep_profile.md",
        "blocked": out_dir / "llms_emp_blocked_probe.md",
        "blocked_jsonl": out_dir / "llms_emp_blocked_probe.jsonl",
        "handoff": out_dir / "llms_emp_r56_handoff.md",
    }
    for name, p in paths.items():
        if not p.exists():
            errors.append(f"missing R5.5 artifact {name}: {rel(p)}")
    if any(not p.exists() for p in paths.values()):
        return
    cases = read_jsonl(paths["case"])
    clusters = read_jsonl(paths["cluster"])
    matrix = read_jsonl(paths["matrix"])
    partials = read_jsonl(paths["partial"])
    if len(cases) != 60:
        errors.append("R5.5 case matrix must contain 60 rows")
    if len(clusters) != 10:
        errors.append("R5.5 cluster profiles must contain 10 rows")
    if len(matrix) != 60:
        errors.append("R5.5 cluster×LLM matrix must contain 60 rows")
    status_counts = Counter(c.get("conversion_status") for c in cases)
    if status_counts != {"converted": 16, "partial": 41, "blocked": 3}:
        errors.append(f"R5.5 case status counts mismatch: {dict(status_counts)}")
    if len(partials) != status_counts.get("partial", 0):
        errors.append("R5.5 partial attribution rows must equal partial case count")
    blocked_rows = read_jsonl(paths["blocked_jsonl"])
    if len(blocked_rows) != status_counts.get("blocked", 0):
        errors.append("R5.5 blocked probe jsonl rows must equal blocked case count")
    for row in blocked_rows:
        if "normalization_repair_possible" in row:
            errors.append(f"R5.5 blocked {row.get('raw_pair_id')} must use pre_scxml_recovery_possible, not normalization_repair_possible")
        if "pre_scxml_recovery_possible" not in row:
            errors.append(f"R5.5 blocked {row.get('raw_pair_id')} missing pre_scxml_recovery_possible")
    for row in clusters:
        features = row.get("behavior_feature_profile")
        if not isinstance(features, dict) or not features:
            errors.append(f"R5.5 cluster {row.get('nl_cluster_id')} missing behavior_feature_profile")
        for key in ["has_guard_like_condition", "has_action_or_entry_exit", "has_variables_or_data_conditions", "has_hierarchy", "has_pseudostate", "has_explicit_time"]:
            if key not in features:
                errors.append(f"R5.5 cluster {row.get('nl_cluster_id')} missing behavior feature {key}")
    cluster_ids = {c.get("nl_cluster_id") for c in clusters}
    if len(cluster_ids) != 10:
        errors.append("R5.5 cluster ids must be unique")
    matrix_pairs = {m.get("raw_pair_id") for m in matrix}
    case_pairs = {c.get("raw_pair_id") for c in cases}
    if matrix_pairs != case_pairs:
        errors.append("R5.5 cluster×LLM matrix pair ids must match case matrix")
    for cluster_id in cluster_ids:
        rows = [m for m in matrix if m.get("nl_cluster_id") == cluster_id]
        if len(rows) != 6:
            errors.append(f"R5.5 cluster {cluster_id} must have 6 LLM outputs")
        if sorted(r.get("llm_family") for r in rows) != sorted(LLM_FAMILY_ORDER):
            errors.append(f"R5.5 cluster {cluster_id} does not cover all 6 LLM families")
    required_partial = {"observed_issue", "source_stage", "r5_loss_code", "evidence_anchor", "attribution_confidence", "r5_6_story_role"}
    for row in partials:
        missing = [k for k in required_partial if row.get(k) in {None, ""}]
        if missing:
            errors.append(f"R5.5 partial {row.get('raw_pair_id')} missing {missing}")
        if row.get("conversion_status") != "partial":
            errors.append(f"R5.5 partial ledger includes non-partial row {row.get('raw_pair_id')}")
    blocked_text = paths["blocked"].read_text(encoding="utf-8")
    for pid in ["llms_emp_stm_results_0018", "llms_emp_stm_results_0028", "llms_emp_stm_results_0037"]:
        if pid not in blocked_text:
            errors.append(f"R5.5 blocked probe missing {pid}")
    handoff_text = paths["handoff"].read_text(encoding="utf-8")
    if "proceed_with_supplementary" not in handoff_text:
        errors.append("R5.5 handoff must state proceed_with_supplementary")
    deep_text = paths["deep"].read_text(encoding="utf-8")
    for required_phrase in ["行为特征画像", "cluster 口径 story role", "feature census"]:
        if required_phrase not in deep_text:
            errors.append(f"R5.5 deep profile missing {required_phrase}")

def load_index_payloads(index: dict[str, Any]) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    archive_cache: dict[str, zipfile.ZipFile] = {}
    try:
        for rec in index.get("records", []):
            payload = None
            if rec.get("path_on_disk"):
                p = repo_path(rec["path_on_disk"])
                if p and p.exists():
                    payload = load_json(p)
            elif rec.get("path_in_zip") and rec.get("archive_path"):
                zp = repo_path(rec["archive_path"])
                if zp and zp.exists():
                    zf = archive_cache.setdefault(str(zp), zipfile.ZipFile(zp))
                    member = rec.get("path_in_zip")
                    if member in zf.namelist():
                        payload = json.loads(zf.read(member).decode("utf-8"))
            if payload is not None:
                payloads.append(payload)
    finally:
        for zf in archive_cache.values():
            zf.close()
    return payloads


def nonzero_status_dict(values: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in sorted(values.items()) if v}


FORBIDDEN_CODE_PATTERNS = [
    ("env_access", re.compile(r"\bos\.environ\b|\bgetenv\s*\(")),
    ("dotenv", re.compile(r"dotenv|load_dotenv", re.IGNORECASE)),
    ("env_file_literal", re.compile(r"[\"']\.env[\"']")),
    ("openai_provider", re.compile(r"\bopenai\b|OpenAI\s*\(", re.IGNORECASE)),
    ("anthropic_provider", re.compile(r"\banthropic\b|Anthropic\s*\(", re.IGNORECASE)),
    ("google_genai_provider", re.compile(r"google\.generativeai|genai\.Client|GenerativeModel", re.IGNORECASE)),
    ("http_client", re.compile(r"\brequests\b|\bhttpx\b|urllib\.request|aiohttp", re.IGNORECASE)),
]

FORBIDDEN_RUNTIME_KEYS = {
    "api_key",
    "api_token",
    "bearer_token",
    "provider_usage",
    "provider_endpoint",
    "runtime_provider",
    "llm_runtime_provider",
    "raw_output",
    "raw_response",
    "prompt",
    "retry_log",
    "usage",
}


def validate_no_llm_or_env_boundary(errors: list[str], indexed_payloads: list[dict[str, Any]], handoff_docs: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Machine gate for the R5 deterministic/no-provider boundary.

    R5 may record that original authors used LLMs, but R5 itself must not read
    `.env`, call hosted providers, or write runtime LLM usage artifacts.
    """
    scanned_files: list[str] = []
    for root in [SMOKE_ROOT / "src", SMOKE_ROOT / "tests"]:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.py")):
            scanned_files.append(rel(path) or str(path))
            text = path.read_text(encoding="utf-8")
            if path.resolve() == Path(__file__).resolve():
                text = re.sub(
                    r"FORBIDDEN_CODE_PATTERNS = \[.*?\n\]\n\nFORBIDDEN_RUNTIME_KEYS = \{.*?\n\}\n",
                    "",
                    text,
                    flags=re.DOTALL,
                )
            for code, pattern in FORBIDDEN_CODE_PATTERNS:
                if pattern.search(text):
                    errors.append(f"R5 deterministic boundary violation in {rel(path)}: {code}")

    scanned_docs = 0

    def visit(obj: Any, where: str) -> None:
        nonlocal scanned_docs
        if isinstance(obj, dict):
            scanned_docs += 1
            for key, value in obj.items():
                key_s = str(key).lower()
                if key_s in FORBIDDEN_RUNTIME_KEYS:
                    errors.append(f"R5 runtime LLM/provider key is not allowed at {where}.{key}")
                visit(value, f"{where}.{key}")
        elif isinstance(obj, list):
            for i, value in enumerate(obj):
                visit(value, f"{where}[{i}]")

    for i, payload in enumerate(indexed_payloads):
        visit(payload, f"records_index_payload[{i}]")
    for name, doc in handoff_docs.items():
        visit(doc, f"handoff.{name}")

    return {
        "status": "ok",
        "scanned_python_files": scanned_files,
        "scanned_json_dicts": scanned_docs,
        "forbidden_code_patterns": [code for code, _ in FORBIDDEN_CODE_PATTERNS],
        "forbidden_runtime_keys": sorted(FORBIDDEN_RUNTIME_KEYS),
    }


def validate(_: argparse.Namespace) -> int:
    errors: list[str] = []
    try:
        import jsonschema
    except Exception:  # pragma: no cover - dependency is in requirements, but keep message explicit
        jsonschema = None

    selected_report_path = SMOKE_ROOT / "selected_examples/smoke_report.json"
    sweep_report_path = SMOKE_ROOT / "seed_library_sweep/sweep_report.json"
    index_path = SMOKE_ROOT / "seed_library_sweep/records_index.json"
    manifest_path = SMOKE_ROOT / "seed_library_sweep/archive_manifest.json"
    handoff_paths = [
        SMOKE_ROOT / "handoff/r5_to_r6_repair_inputs.json",
        SMOKE_ROOT / "handoff/r5_to_r7_seed_eligibility.json",
        SMOKE_ROOT / "handoff/r5_to_r8_negative_evidence.json",
    ]
    for path in [selected_report_path, sweep_report_path, index_path, manifest_path, *handoff_paths]:
        if not path.exists():
            errors.append(f"missing required artifact: {rel(path)}")
    if not errors:
        selected = load_json(selected_report_path)
        sweep_for_schema = load_json(sweep_report_path)
        if jsonschema is not None:
            jsonschema.validate(selected, load_json(SMOKE_ROOT / "schemas/selected_smoke_report.schema.json"))
            jsonschema.validate(sweep_for_schema, load_json(SMOKE_ROOT / "schemas/seed_sweep_report.schema.json"))
        if len(selected.get("items", [])) != 4:
            errors.append("selected smoke report must contain exactly 4 items")
        selected_recomputed = Counter(item.get("status") for item in selected.get("items", []))
        if selected.get("summary", {}).get("examples") != len(selected.get("items", [])):
            errors.append("selected summary examples does not recompute")
        for status in ["pass", "partial", "blocked"]:
            if selected.get("summary", {}).get(status) != selected_recomputed.get(status, 0):
                errors.append(f"selected summary {status} does not recompute")
        for item in selected.get("items", []):
            if item.get("repair_contribution_allowed") is not False:
                errors.append(f"selected {item.get('example_id')} missing repair_contribution_allowed=false")
            if item.get("status") not in {"pass", "partial", "blocked"}:
                errors.append(f"selected {item.get('example_id')} has invalid status {item.get('status')}")
            if not all(item.get("checks", {}).values()):
                errors.append(f"selected {item.get('example_id')} has failed checks")
            r3_path = repo_path((item.get("upstream_r3") or {}).get("canonical_output_path"))
            if r3_path and r3_path.exists() and load_json(r3_path).get("example_id") != item.get("example_id"):
                errors.append(f"selected {item.get('example_id')} R3 canonical example_id mismatch")
            parse_path = repo_path((item.get("upstream_r45") or {}).get("parse_inspect_report_path"))
            if parse_path and parse_path.exists():
                parse_doc = load_json(parse_path)
                if parse_doc.get("parse_status") != (item.get("upstream_r45") or {}).get("parse_status"):
                    errors.append(f"selected {item.get('example_id')} direct parse_status mismatch")
                if parse_doc.get("inspect_status") != (item.get("upstream_r45") or {}).get("inspect_status"):
                    errors.append(f"selected {item.get('example_id')} direct inspect_status mismatch")
            for fixture_path in (item.get("upstream_r4_fixture") or {}).values():
                fp = repo_path(fixture_path)
                if fp and fp.exists() and load_json(fp).get("example_id") != item.get("example_id"):
                    errors.append(f"selected {item.get('example_id')} R4 fixture example_id mismatch: {fixture_path}")
            rec_path = SMOKE_ROOT / "selected_examples/smoke_records" / f"{item.get('example_id')}.json"
            if not rec_path.exists():
                errors.append(f"missing selected record {rec_path}")
        sweep = load_json(sweep_report_path)
        entries = sweep.get("entries", [])
        if sweep.get("meta", {}).get("entry_dir_count") != len(entries):
            errors.append("sweep entry_dir_count does not equal entries length")
        recomputed = Counter(e.get("primary_entry_status") for e in entries)
        if dict(sorted(recomputed.items())) != sweep.get("summary", {}).get("entry_status_counts"):
            errors.append("entry status counts do not recompute from entries")
        if sweep.get("meta", {}).get("repair_contribution_allowed") is not False:
            errors.append("sweep meta missing repair_contribution_allowed=false")
        index = load_json(index_path)
        manifest = load_json(manifest_path)
        indexed_payloads = load_index_payloads(index)
        pair_payloads = [p for p in indexed_payloads if p.get("schema_version") == "r5.seed_sweep_pair_record.v0"]
        asset_payloads = [p for p in indexed_payloads if p.get("schema_version") == "r5.seed_sweep_asset_record.v0"]
        pair_counts = Counter(p.get("status") for p in pair_payloads)
        asset_counts = Counter(p.get("status") for p in asset_payloads)
        if len(pair_payloads) != sweep.get("summary", {}).get("pair_records_total"):
            errors.append("pair_records_total does not recompute from records_index payloads")
        if dict(sorted(pair_counts.items())) != sweep.get("summary", {}).get("pair_status_counts"):
            errors.append("pair_status_counts do not recompute from records_index payloads")
        if len(asset_payloads) != sweep.get("summary", {}).get("asset_records_total"):
            errors.append("asset_records_total does not recompute from records_index payloads")
        if dict(sorted(asset_counts.items())) != sweep.get("summary", {}).get("asset_status_counts"):
            errors.append("asset_status_counts do not recompute from records_index payloads")
        pair_count_by_entry = Counter(p.get("entry_id") for p in pair_payloads)
        asset_count_by_entry = Counter(p.get("entry_id") for p in asset_payloads)
        pair_status_by_entry: dict[str, Counter] = defaultdict(Counter)
        asset_status_by_entry: dict[str, Counter] = defaultdict(Counter)
        for payload in pair_payloads:
            pair_status_by_entry[str(payload.get("entry_id"))][payload.get("status")] += 1
        for payload in asset_payloads:
            asset_status_by_entry[str(payload.get("entry_id"))][payload.get("status")] += 1
        for entry in entries:
            entry_id = str(entry.get("entry_id"))
            if pair_count_by_entry.get(entry_id, 0) != entry.get("pair_record_count", 0):
                errors.append(f"{entry_id} pair_record_count does not recompute from index")
            if asset_count_by_entry.get(entry_id, 0) != entry.get("asset_record_count", 0):
                errors.append(f"{entry_id} asset_record_count does not recompute from index")
            if nonzero_status_dict(dict(pair_status_by_entry.get(entry_id, Counter()))) != nonzero_status_dict(entry.get("status_counts_by_pair", {})):
                errors.append(f"{entry_id} status_counts_by_pair does not recompute from index")
            if nonzero_status_dict(dict(asset_status_by_entry.get(entry_id, Counter()))) != nonzero_status_dict(entry.get("status_counts_by_asset", {})):
                errors.append(f"{entry_id} status_counts_by_asset does not recompute from index")
        for arc in manifest.get("archives", []):
            zp = repo_path(arc.get("archive_path"))
            if not zp or not zp.exists():
                errors.append(f"archive missing: {arc.get('archive_path')}")
                continue
            if sha256_file(zp) != arc.get("sha256"):
                errors.append(f"archive sha256 mismatch: {arc.get('archive_path')}")
            with zipfile.ZipFile(zp) as zf:
                members = [m for m in zf.namelist() if m.endswith(".json")]
            if len(members) != arc.get("record_count"):
                errors.append(f"archive record count mismatch: {arc.get('archive_path')}")
        archive_cache: dict[str, zipfile.ZipFile] = {}
        try:
            for rec in index.get("records", []):
                if rec.get("path_on_disk"):
                    p = repo_path(rec["path_on_disk"])
                    if not p or not p.exists() or sha256_file(p) != rec.get("sha256"):
                        errors.append(f"index path_on_disk invalid for {rec.get('record_id')}")
                elif rec.get("path_in_zip"):
                    archive_path = rec.get("archive_path")
                    zp = repo_path(archive_path) if archive_path else None
                    if not zp or not zp.exists():
                        errors.append(f"index archive missing for {rec.get('record_id')}")
                        continue
                    zf = archive_cache.setdefault(str(zp), zipfile.ZipFile(zp))
                    member = rec.get("path_in_zip")
                    if member not in zf.namelist():
                        errors.append(f"index path_in_zip missing for {rec.get('record_id')}")
                    elif sha256_bytes(zf.read(member)) != rec.get("sha256"):
                        errors.append(f"index path_in_zip sha256 invalid for {rec.get('record_id')}")
        finally:
            for zf in archive_cache.values():
                zf.close()
        # Validate pair records reachable from index and loss fields for converted/partial.
        for payload in pair_payloads:
            if payload.get("status") in {"converted", "partial"}:
                for field in ["loss_count", "loss_categories", "loss_reason_codes", "irrecoverable_fields", "conversion_attribution", "representation_attribution", "repair_contribution_allowed"]:
                    if field not in payload:
                        errors.append(f"{payload.get('record_id')} missing loss/attribution field {field}")
                if payload.get("repair_contribution_allowed") is not False:
                    errors.append(f"{payload.get('record_id')} repair_contribution_allowed must be false")
        handoff_docs = {hp.name: load_json(hp) for hp in handoff_paths}
        validate_llms_emp_profile(errors)
        boundary_report = validate_no_llm_or_env_boundary(errors, indexed_payloads, handoff_docs)
        r6 = handoff_docs["r5_to_r6_repair_inputs.json"]
        if len(r6.get("items", [])) != pair_counts.get("converted", 0):
            errors.append("R6 handoff items must include all converted pair payloads")
        if (r6.get("summary") or {}).get("converted") != pair_counts.get("converted", 0):
            errors.append("R6 handoff converted summary does not match pair counts")
        r7 = handoff_docs["r5_to_r7_seed_eligibility.json"]
        if (r7.get("summary") or {}).get("converted") != pair_counts.get("converted", 0):
            errors.append("R7 handoff converted summary does not match pair counts")
        if (r7.get("summary") or {}).get("partial") != pair_counts.get("partial", 0):
            errors.append("R7 handoff partial summary does not match pair counts")
        if "partial_items" in r7:
            errors.append("R7 handoff must use partial_sample, not misleading partial_items")
        if not r7.get("sample_policy") or not r7.get("full_list_via"):
            errors.append("R7 handoff must document sample policy and full_list_via")
        if r7.get("sample_truncated") != {"converted": pair_counts.get("converted", 0) > len(r7.get("converted_sample", [])), "partial": pair_counts.get("partial", 0) > len(r7.get("partial_sample", []))}:
            errors.append("R7 handoff sample_truncated flags do not match sample lengths")
        r8 = handoff_docs["r5_to_r8_negative_evidence.json"]
        r8_expected = dict(Counter(p.get("status") for p in pair_payloads if p.get("status") in {"blocked", "missing_asset", "not_applicable", "needs_generation"}))
        if r8.get("summary") != r8_expected:
            errors.append("R8 handoff negative evidence summary does not match pair counts")
        for hp, doc in handoff_docs.items():
            if doc.get("repair_contribution_allowed") is not False:
                errors.append(f"handoff missing repair_contribution_allowed=false: {hp}")
    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1
    print(json.dumps({
        "status": "ok",
        "validated": [rel(p) for p in [selected_report_path, sweep_report_path, index_path, manifest_path, *handoff_paths]],
        "deterministic_boundary": boundary_report if "boundary_report" in locals() else None,
    }, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R5 deterministic smoke and seed library readiness audit CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    p_selected = sub.add_parser("run-selected", help="generate selected four-example smoke report")
    p_selected.set_defaults(func=run_selected)
    p_sweep = sub.add_parser("run-seed-sweep", help="generate seed library full census report")
    p_sweep.add_argument("--max-per-pair-seconds", type=int, default=30)
    p_sweep.add_argument("--continue-on-error", dest="continue_on_error", action="store_true", default=True, help="Keep sweeping after per-pair conversion errors/timeouts (default).")
    p_sweep.add_argument("--no-continue-on-error", dest="continue_on_error", action="store_false", help="Fail fast on per-pair tool exceptions/timeouts for strict debugging; not used for committed R5 census.")
    p_sweep.set_defaults(func=run_seed_sweep)
    p_llms = sub.add_parser("run-llms-emp-profile", help="generate R5.5 llms-emp deep profile artifacts")
    p_llms.set_defaults(func=run_llms_emp_profile)
    p_validate = sub.add_parser("validate", help="validate R5 smoke/sweep artifacts")
    p_validate.set_defaults(func=validate)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
