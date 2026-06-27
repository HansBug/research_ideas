from __future__ import annotations

import argparse
import hashlib
import json
import signal
import shutil
import tempfile
import threading
import zipfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parents[5]
PAPER_ROOT = REPO_ROOT / "project_1_llm_state_machine_modeling/paper_stm_repair"
SMOKE_ROOT = PAPER_ROOT / "smoke"
SELECTED_DIR = PAPER_ROOT / "selected_seed_examples"
CONVERSION_REPORTS = PAPER_ROOT / "conversion/reports"
REPRESENTATION_REPORTS = PAPER_ROOT / "representation/reports"
EVALUATION_DIR = PAPER_ROOT / "evaluation/dry_run_examples"
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
        "| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |",
        "|---|---|---|---|---|---|---:|---|---|",
    ]
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
    write_json(out_dir / "archive_manifest.json", {"schema_version": "r5.archive_manifest.v0", "archives": archives, "policy": "High-cardinality pair records are stored in per-entry zip archives when record count > 50 or serialized bytes > 5 MiB."})
    write_sweep_summaries(out_dir, report, pair_records_all, archives)
    write_handoffs(pair_records_all, entry_records)
    print(json.dumps(report["summary"], ensure_ascii=False, sort_keys=True))
    return 0


def rows_for_status(records: list[dict[str, Any]], statuses: set[str], limit: int = 20) -> list[dict[str, Any]]:
    return [r for r in sorted(records, key=lambda x: (x.get("status") or "", x.get("entry_id") or "", str(x.get("pair_id") or ""))) if r.get("status") in statuses][:limit]


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
        rows = rows_for_status(pair_records, statuses, 40)
        text = [f"# {title}", "", "事实源为 [sweep_report.json](./sweep_report.json) 与 [records_index.json](./records_index.json)。", "", "| entry | pair | status | reason | handoff |", "|---|---|---|---|---|"]
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
        "not_applicable_or_needs_generation": [r for r in pair_records if r.get("status") in {"not_applicable", "needs_generation"}],
    }
    lines = [
        "# R5 seed sweep 抽样分析",
        "",
        "抽样规则：按 `status -> entry_id -> pair_id` 排序，每类取固定前若干条；高基数全量明细仍以 archive / records_index 为准。",
        "",
    ]
    for name, rows in groups.items():
        rows = sorted(rows, key=lambda x: (x.get("status") or "", x.get("entry_id") or "", str(x.get("pair_id") or "")))
        need = 2 if name == "converted" else 1
        sample = rows[: max(need, min(3, len(rows)))]
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
    common = {"schema_version": "r5.handoff.v0", "created_at": now_iso(), "repo_commit": git_commit(), "repair_contribution_allowed": False}
    write_json(handoff_dir / "r5_to_r6_repair_inputs.json", {**common, "handoff_target": "r6_candidate", "summary": {"converted": len(converted)}, "items": converted, "notes": "Only pre-repair converted candidates. R6 still must run its own eligibility gates; R5 does not execute repair."})
    write_json(handoff_dir / "r5_to_r7_seed_eligibility.json", {**common, "handoff_target": "r7_seed_eligibility_review", "summary": {"converted": len(converted), "partial": len(partial), "entries": len(entry_records)}, "converted_sample": converted[:50], "partial_items": partial[:100]})
    write_json(handoff_dir / "r5_to_r8_negative_evidence.json", {**common, "handoff_target": "r8_negative_evidence", "summary": dict(Counter(r.get("status") for r in negative)), "items": negative[:300]})


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
    print(json.dumps({"status": "ok", "validated": [rel(p) for p in [selected_report_path, sweep_report_path, index_path, manifest_path, *handoff_paths]]}, ensure_ascii=False, indent=2))
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
    p_validate = sub.add_parser("validate", help="validate R5 smoke/sweep artifacts")
    p_validate.set_defaults(func=validate)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
