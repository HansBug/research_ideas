from __future__ import annotations

import argparse
import json
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from .adapters import convert_plantuml, convert_ttool_xml, convert_umple
from .models import Loss
from .report import make_example_report, sha256_file, write_json
from .toolchain import ToolchainSetupError, preflight_for_format, run_plantuml_on_candidate
from .normalization.archive import build_recovery_workdir_archive
from .normalization.recovery import run_recovery

REPO_REL_BASE = Path("project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples")
CONVERSION_REL_BASE = Path("project_1_llm_state_machine_modeling/paper_stm_repair/conversion")
RECOVERY_ARTIFACT_REL_BASE = CONVERSION_REL_BASE / "artifacts" / "plantuml_recovery" / "r3_1_committed"


def _repo_root_from_cwd() -> Path:
    cwd = Path.cwd().resolve()
    cur = cwd
    while cur != cur.parent:
        if (cur / ".git").exists() and (cur / "project_1_llm_state_machine_modeling").exists():
            return cur
        cur = cur.parent
    return cwd


def _find_stm(example_dir: Path) -> Path:
    files = sorted(example_dir.glob("stm0.*"))
    if len(files) != 1:
        raise ValueError(f"{example_dir}: expected exactly one stm0.* file, got {files}")
    return files[0]


def _load_meta(example_dir: Path) -> dict[str, Any]:
    return json.loads((example_dir / "source_meta.json").read_text(encoding="utf-8"))


def _load_source_pair_record(example_dir: Path, meta: dict[str, Any]) -> dict[str, Any]:
    source_pairs = (example_dir / meta["source_pairs_jsonl"]).resolve()
    for line in source_pairs.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("pair_id") == meta["pair_id"]:
            return record
    raise ValueError(f"{example_dir.name}: pair_id {meta['pair_id']} not found in {source_pairs}")


def _rel(path: Path, repo_root: Path) -> str:
    try:
        return str(path.resolve().relative_to(repo_root.resolve()))
    except ValueError:
        return str(path)


def audit_inputs(repo_root: Path, selected_dir: Path) -> list[dict[str, Any]]:
    audit = []
    for example_dir in sorted(p for p in selected_dir.iterdir() if p.is_dir()):
        meta = _load_meta(example_dir)
        nl_path = example_dir / "nl.txt"
        stm_path = _find_stm(example_dir)
        nl_hash = sha256_file(nl_path)
        stm_hash = sha256_file(stm_path)
        pair_record = _load_source_pair_record(example_dir, meta)
        source_pair_nl_sha256 = pair_record.get("nl_sha256")
        source_pair_stm0_sha256 = pair_record.get("stm0_sha256")
        meta_source_nl_sha256 = meta.get("source_nl_sha256", meta.get("nl_sha256"))
        meta_source_stm0_sha256 = meta.get("source_stm0_sha256", meta.get("stm0_sha256"))
        source_nl_hash_match = nl_hash == source_pair_nl_sha256
        source_stm0_hash_match = stm_hash == source_pair_stm0_sha256
        hash_scope = meta.get("hash_scope") or ""
        nl_normalization_documented = bool(hash_scope) and meta_source_nl_sha256 == source_pair_nl_sha256
        stm0_normalization_documented = bool(hash_scope) and meta_source_stm0_sha256 == source_pair_stm0_sha256
        row = {
            "example_id": example_dir.name,
            "nl_path": _rel(nl_path, repo_root),
            "stm0_path": _rel(stm_path, repo_root),
            "source_nl_path": _rel(nl_path, repo_root),
            "source_stm0_path": _rel(stm_path, repo_root),
            "stm_format": meta["stm_format"],
            "pair_id": meta["pair_id"],
            "nl_sha256": nl_hash,
            "stm0_sha256": stm_hash,
            "expected_nl_sha256": meta["nl_sha256"],
            "expected_stm0_sha256": meta["stm0_sha256"],
            "source_pair_nl_sha256": source_pair_nl_sha256,
            "source_pair_stm0_sha256": source_pair_stm0_sha256,
            "meta_source_nl_sha256": meta_source_nl_sha256,
            "meta_source_stm0_sha256": meta_source_stm0_sha256,
            "nl_hash_match": nl_hash == meta["nl_sha256"],
            "stm0_hash_match": stm_hash == meta["stm0_sha256"],
            "source_nl_hash_match": source_nl_hash_match,
            "source_stm0_hash_match": source_stm0_hash_match,
            "source_nl_hash_divergence_documented": source_nl_hash_match or nl_normalization_documented,
            "source_stm0_hash_divergence_documented": source_stm0_hash_match or stm0_normalization_documented,
            "source_hash_divergence_documented": (source_nl_hash_match or nl_normalization_documented) and (source_stm0_hash_match or stm0_normalization_documented),
            "hash_scope": hash_scope,
            "source_pairs_jsonl": _rel((example_dir / meta["source_pairs_jsonl"]).resolve(), repo_root),
        }
        row["source_pairs_exists"] = (repo_root / row["source_pairs_jsonl"]).exists()
        audit.append(row)
    return audit


def _apply_toolchain_preflight(result: Any, preflight: dict[str, Any]) -> None:
    result.metadata["tool_preflight_summary"] = {
        "tool_name": preflight.get("tool_name"),
        "tool_invocation_status": preflight.get("tool_invocation_status"),
        "syntax_status": preflight.get("syntax_status"),
        "structured_export_status": preflight.get("structured_export_status"),
        "structured_export_format": preflight.get("structured_export_format"),
        "structured_export_path": preflight.get("structured_export_path"),
        "structured_export_sha256": preflight.get("structured_export_sha256"),
        "fallback_reason": preflight.get("fallback_reason"),
    }
    syntax_status = preflight.get("syntax_status")
    structured_status = preflight.get("structured_export_status") or ""
    if syntax_status == "ok":
        result.diagnostics.append({
            "code": "R3.TOOLCHAIN.OFFICIAL_SYNTAX_OK",
            "severity": "info",
            "tool_name": preflight.get("tool_name"),
            "structured_export_status": structured_status,
            "structured_export_path": preflight.get("structured_export_path"),
            "message": "Official/mature toolchain syntax preflight succeeded before R3 canonical structured extraction.",
        })
    elif syntax_status and syntax_status.startswith("xml_wellformed"):
        result.diagnostics.append({
            "code": "R3.TOOLCHAIN.XML_ARTIFACT_WELLFORMED",
            "severity": "info",
            "tool_name": preflight.get("tool_name"),
            "structured_export_status": structured_status,
            "structured_export_path": preflight.get("structured_export_path"),
            "message": "TTool/AVATAR official XML artifact is well-formed; no documented headless SCXML/JSON/AST export was evidenced in R3.",
        })
    else:
        if result.status == "converted":
            result.status = "partial"
        reason = preflight.get("fallback_reason") or "Official/mature toolchain preflight did not succeed; no source-text parser output may be used as canonical conversion."
        result.blocking_reason = reason if not result.blocking_reason else result.blocking_reason
        loss_id = f"{result.example_id}:{result.adapter}:official_preflight_failed"
        result.diagnostics.append({
            "code": "R3.TOOLCHAIN.OFFICIAL_SYNTAX_FAILED",
            "severity": "high",
            "tool_name": preflight.get("tool_name"),
            "syntax_status": syntax_status,
            "structured_export_status": structured_status,
            "loss_ref": loss_id,
            "message": reason,
        })
        result.losses.append(
            Loss(
                loss_id=loss_id,
                example_id=result.example_id,
                source_ref=preflight.get("command")[-1] if preflight.get("command") else result.source_format,
                canonical_ref=None,
                loss_type="tooling",
                severity="high",
                rationale=reason,
                needs_manual_review=True,
            )
        )


def _tool_info(meta: dict[str, Any], preflight: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool_name": preflight.get("tool_name"),
        "tool_version": preflight.get("tool_version"),
        "tool_source_url": preflight.get("tool_source_url"),
        "tool_invocation_status": preflight.get("tool_invocation_status"),
        "raw_locator": meta.get("source_locator"),
        "manual_normalization": False,
        "tool_preflight": preflight,
    }


def _load_recovery_item(repo_root: Path, pair_id: str) -> dict[str, Any] | None:
    report_path = repo_root / CONVERSION_REL_BASE / "reports" / "plantuml_recovery_report.json"
    if not report_path.exists():
        return None
    report = json.loads(report_path.read_text(encoding="utf-8"))
    for item in report.get("items", []):
        if item.get("pair_id") == pair_id:
            return item
    return None


def _replay_r31_normalized_preflight(
    *,
    repo_root: Path,
    example_id: str,
    meta: dict[str, Any],
    reports_dir: Path,
    original_preflight: dict[str, Any],
) -> dict[str, Any] | None:
    """Re-run official PlantUML on a committed R3.1 normalized candidate.

    This is intentionally narrow: it is not a regex/source parser fallback and it
    does not parse the selected raw PlantUML text.  It only replays an R3.1
    deterministic normalization artifact that already passed the committed
    semantic-preservation audit, and then obtains a fresh SCXML export from the
    configured PlantUML toolchain in this run.
    """

    recovery_item = _load_recovery_item(repo_root, meta.get("pair_id", ""))
    if not recovery_item:
        return None
    if not (
        recovery_item.get("main_eligibility_included")
        and recovery_item.get("normalized_conversion_pass")
        and recovery_item.get("semantic_preservation_pass") is True
    ):
        return None
    normalized_member = recovery_item.get("normalized_candidate_path")
    if not normalized_member:
        return None
    recovery_report = json.loads((repo_root / CONVERSION_REL_BASE / "reports" / "plantuml_recovery_report.json").read_text(encoding="utf-8"))
    archive_info = recovery_report.get("artifact_archive") or {}
    archive_rel = archive_info.get("archive_path")
    if not archive_rel:
        return None
    archive_path = repo_root / archive_rel
    if not archive_path.exists():
        return None
    with tempfile.TemporaryDirectory(prefix=f"r3_1_replay_{example_id}_") as td:
        candidate_path = Path(td) / Path(normalized_member).name
        with zipfile.ZipFile(archive_path) as zf:
            candidate_path.write_bytes(zf.read(normalized_member))
        replay = run_plantuml_on_candidate(
            candidate_path,
            example_id=example_id,
            repo_root=repo_root,
            reports_dir=reports_dir,
            export_subdir="toolchain_exports",
            output_stem="stm0.r3_1_normalized",
        ).to_metadata()
    replay.setdefault("evidence", {})
    replay["evidence"].update({
        "r3_1_normalization_replay": True,
        "r3_1_recovery_report_path": str((CONVERSION_REL_BASE / "reports" / "plantuml_recovery_report.json")),
        "r3_1_recovery_archive_path": archive_info.get("archive_path"),
        "r3_1_normalized_candidate_member": normalized_member,
        "r3_1_original_raw_preflight": {
            "syntax_status": original_preflight.get("syntax_status"),
            "structured_export_status": original_preflight.get("structured_export_status"),
            "fallback_reason": original_preflight.get("fallback_reason"),
        },
        "semantic_preservation_pass": recovery_item.get("semantic_preservation_pass"),
        "rule_ids": recovery_item.get("rule_ids", []),
        "raw_candidate_path": recovery_item.get("raw_candidate_path"),
        "source_line_sha256": recovery_item.get("source_line_sha256"),
    })
    replay["tool_invocation_status"] = "official_cli_syntax_and_scxml_ok_after_r3_1_normalization_replay"
    return replay


def _maybe_apply_r31_recovery_preflight(
    *,
    repo_root: Path,
    example_dir: Path,
    meta: dict[str, Any],
    reports_dir: Path,
    preflight: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    if meta.get("stm_format") != "plantuml":
        return preflight, None
    if preflight.get("syntax_status") == "ok" and preflight.get("structured_export_status") == "scxml_export_ok":
        return preflight, None
    replay = _replay_r31_normalized_preflight(
        repo_root=repo_root,
        example_id=example_dir.name,
        meta=meta,
        reports_dir=reports_dir,
        original_preflight=preflight,
    )
    if replay and replay.get("syntax_status") == "ok" and replay.get("structured_export_status") == "scxml_export_ok":
        return replay, preflight
    return preflight, None


def convert_one(repo_root: Path, example_dir: Path, reports_dir: Path, run_id: str, conversion_command: str, created_at: str | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    meta = _load_meta(example_dir)
    stm_path = _find_stm(example_dir)
    fmt = meta["stm_format"]
    try:
        raw_preflight = preflight_for_format(fmt, stm_path, example_id=example_dir.name, repo_root=repo_root, reports_dir=reports_dir).to_metadata()
    except ToolchainSetupError as exc:
        raise SystemExit(f"R3 conversion toolchain setup failed for {example_dir.name}:\n{exc}") from None
    preflight, original_preflight = _maybe_apply_r31_recovery_preflight(
        repo_root=repo_root,
        example_dir=example_dir,
        meta=meta,
        reports_dir=reports_dir,
        preflight=raw_preflight,
    )
    kwargs = {"example_id": example_dir.name, "seed_id": meta["seed_id"], "source_format": fmt}
    if fmt == "plantuml":
        result = convert_plantuml(stm_path, preflight=preflight, repo_root=repo_root, **kwargs)
        if original_preflight is not None:
            result.metadata["r3_1_normalization_replay_used"] = True
            result.metadata["selected_raw_source_path"] = _rel(stm_path, repo_root)
            result.metadata["source_text_used_for_canonical"] = False
            result.diagnostics.append({
                "code": "R3.R31.NORMALIZED_SCXML_REPLAY_USED",
                "severity": "info",
                "message": "Raw selected PlantUML failed official SCXML export, so R3 replayed a committed R3.1 deterministic normalized candidate and re-ran official PlantUML -tscxml. This is conversion normalization only, not repair gain.",
                "raw_syntax_status": original_preflight.get("syntax_status"),
                "raw_structured_export_status": original_preflight.get("structured_export_status"),
                "normalized_structured_export_path": preflight.get("structured_export_path"),
                "recovery_report_path": str(CONVERSION_REL_BASE / "reports" / "plantuml_recovery_report.json"),
            })
    elif fmt == "umple":
        result = convert_umple(stm_path, preflight=preflight, repo_root=repo_root, **kwargs)
    elif fmt == "ttool_xml":
        result = convert_ttool_xml(stm_path, **kwargs)
    else:
        raise ValueError(f"Unsupported stm_format for R3: {fmt}")
    _apply_toolchain_preflight(result, preflight)

    canonical_dir = reports_dir / "canonical"
    canonical_output_path: Path | None = None
    canonical_output_sha256: str | None = None
    if result.status in {"converted", "partial"} and result.metadata.get("conversion_source") in {"official_scxml", "official_xml"}:
        canonical_output_path = canonical_dir / f"{example_dir.name}.canonical_stm.json"
        canonical_output_sha256 = write_json(canonical_output_path, result.to_canonical_dict())

    loss_rows = result.losses_dicts()
    loss_ledger_path = reports_dir / "selected_seed_examples_loss_ledger.jsonl"
    report = make_example_report(
        result=result,
        example_dir=example_dir,
        stm_path=stm_path,
        source_meta_path=example_dir / "source_meta.json",
        canonical_output_path=canonical_output_path,
        canonical_output_sha256=canonical_output_sha256,
        loss_ledger_path=loss_ledger_path,
        repo_root=repo_root,
        run_id=run_id,
        conversion_command=conversion_command,
        created_at=created_at,
        tool_info=_tool_info(meta, preflight),
    )
    return report, loss_rows


def _write_loss_ledger(path: Path, rows: list[dict[str, Any]]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")
    import hashlib

    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _write_summary(path: Path, reports: list[dict[str, Any]], loss_rows: list[dict[str, Any]]) -> None:
    lines = [
        "# R3 selected_seed_examples 转换 v0 摘要",
        "",
        "本文件由 `python -m paper_stm_repair_conversion.cli convert-selected` 生成，是 R3 reviewer fixture；它不是最终实验结果。",
        "",
        "| example_id | 上游 NL | 原始 STM_0 | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | syntax | structured export | losses | 说明 |",
        "|---|---|---|---|---|---:|---:|---|---|---|---|---:|---|",
    ]
    for report in reports:
        reason = (report.get("blocking_reason") or "").replace("|", "/")
        diagnostic_codes = {diag.get("code") for diag in report.get("diagnostics", [])}
        if "R3.R31.NORMALIZED_SCXML_REPLAY_USED" in diagnostic_codes:
            r31_note = "R3.1 normalization replay 后重新走官方 SCXML；raw STM_0 不覆盖，不计 repair gain。"
            reason = f"{reason} {r31_note}".strip()
        preflight = report.get("tool_preflight") or {}
        syntax_status = (preflight.get("syntax_status") or "").replace("|", "/")
        structured_status = (preflight.get("structured_export_status") or "").replace("|", "/")
        lines.append(
            f"| `{report['example_id']}` | [{Path(report['source_nl_path']).name}](../../../../{report['source_nl_path']}) | "
            f"[{Path(report['source_stm0_path']).name}](../../../../{report['source_stm0_path']}) | "
            f"`{report['source_format']}` | `{report['status']}` | "
            f"{report['states_count']} | {report['transitions_count']} | `{report['timing_level']}` | "
            f"`{report['hierarchy_level']}` | `{syntax_status}` | `{structured_status}` | {report['losses_count']} | {reason} |"
        )
    lines.extend([
        "",
        f"Loss ledger 行数：{len(loss_rows)}",
        "",
        "所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。",
        "",
    ])
    failures = [
        report
        for report in reports
        if (report.get("tool_preflight") or {}).get("syntax_status") not in {"ok", "xml_wellformed_checked_by_python_etree"}
        or (report.get("tool_preflight") or {}).get("structured_export_status") in {"scxml_export_failed", "scxml_not_trusted_after_syntax_failure"}
    ]
    if failures:
        lines.extend([
            "## 官方工具链失败细节",
            "",
            "以下内容记录的是官方/成熟工具链返回值与截断后的输出；R3 不会因此退回正则或 source-text parser，也不会复用 committed SCXML。",
            "",
        ])
        for report in failures:
            preflight = report.get("tool_preflight") or {}
            lines.extend([
                f"### `{report['example_id']}`",
                "",
                f"- tool: `{preflight.get('tool_name')}`",
                f"- command: `{preflight.get('command')}`",
                f"- returncode: `{preflight.get('returncode')}`",
                f"- structured_export_status: `{preflight.get('structured_export_status')}`",
                f"- fallback_used: `{report.get('fallback_used')}`；canonical_output_path: `{report.get('canonical_output_path')}`",
                "",
                "stderr tail:",
                "",
                "```text",
                (preflight.get("stderr_tail") or "").strip() or "<empty>",
                "```",
                "",
            ])
    path.write_text("\n".join(lines), encoding="utf-8")


def convert_selected(args: argparse.Namespace) -> int:
    repo_root = _repo_root_from_cwd()
    selected_dir = repo_root / args.selected_dir
    reports_dir = repo_root / args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    # Avoid stale canonical fixtures when a formerly partial example becomes blocked after stricter structured-export gates.
    canonical_dir = reports_dir / "canonical"
    if canonical_dir.exists():
        for old in canonical_dir.glob("*.canonical_stm.json"):
            old.unlink()
    audit = audit_inputs(repo_root, selected_dir)
    if not all(
        row["nl_hash_match"]
        and row["stm0_hash_match"]
        and row["source_pairs_exists"]
        and row["source_hash_divergence_documented"]
        for row in audit
    ):
        raise SystemExit("selected_seed_examples input audit failed; inspect selected_seed_examples_input_audit.json")
    write_json(reports_dir / "selected_seed_examples_input_audit.json", {"items": audit})

    conversion_command = "python -m paper_stm_repair_conversion.cli convert-selected"
    run_id = args.run_id
    reports: list[dict[str, Any]] = []
    loss_rows: list[dict[str, Any]] = []
    for example_dir in sorted(p for p in selected_dir.iterdir() if p.is_dir()):
        report, losses = convert_one(repo_root, example_dir, reports_dir, run_id, conversion_command, args.created_at)
        reports.append(report)
        loss_rows.extend(losses)
    loss_sha = _write_loss_ledger(reports_dir / "selected_seed_examples_loss_ledger.jsonl", loss_rows)
    report_doc = {
        "report_version": "r3.selected_seed_examples_conversion_report.v0",
        "run_id": run_id,
        "items": reports,
        "loss_ledger_sha256": loss_sha,
        "note": "R3 smoke fixture only; not main experiment evidence. repo_commit records the clean converter-code commit used before writing committed report artifacts; item report_sha256 is the SHA-256 of the report document before embedding that hash into item rows, avoiding a misleading self-referential hash.",
    }
    pre_embed_report_sha = write_json(reports_dir / "selected_seed_examples_conversion_report.json", report_doc)
    for item in report_doc["items"]:
        item["report_sha256"] = pre_embed_report_sha
    write_json(reports_dir / "selected_seed_examples_conversion_report.json", report_doc)
    _write_summary(reports_dir / "selected_seed_examples_summary.md", reports, loss_rows)
    print(json.dumps({"reports_dir": str(reports_dir), "examples": len(reports), "losses": len(loss_rows)}, ensure_ascii=False, indent=2))
    return 0


def recover_plantuml(args: argparse.Namespace) -> int:
    repo_root = _repo_root_from_cwd()
    generation_command = "python -m paper_stm_repair_conversion.cli recover-plantuml"
    run_dir = repo_root / args.run_dir
    report = run_recovery(
        repo_root=repo_root,
        reports_dir=repo_root / args.reports_dir,
        run_dir=run_dir,
        run_id=args.run_id,
        pair_sources=[Path(p) for p in args.pair_source] if args.pair_source else None,
        limit=args.limit,
        created_at=args.created_at,
        generation_command=generation_command,
    )
    archive_manifest = None
    if args.archive_dir:
        archive_manifest = build_recovery_workdir_archive(
            repo_root=repo_root,
            workdir=run_dir,
            archive_dir=repo_root / args.archive_dir,
            report=report,
        )
        if not args.keep_workdir:
            shutil.rmtree(run_dir, ignore_errors=True)
    summary = report["summary"]
    print(json.dumps({
        "reports_dir": str(repo_root / args.reports_dir),
        "run_dir": str(run_dir),
        "archive": archive_manifest["archive_path"] if archive_manifest else None,
        "raw_total": summary["raw_total"],
        "failed_before": summary["failed_before"],
        "technical_scxml_pass_all_rules": summary["technical_scxml_pass_all_rules"],
        "low_risk_scxml_pass": summary["low_risk_scxml_pass"],
        "main_eligibility_included": summary["main_eligibility_included"],
    }, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R3 paper_stm_repair conversion v0 CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    conv = sub.add_parser("convert-selected", help="convert selected_seed_examples into R3 canonical/report fixtures")
    conv.add_argument("--selected-dir", default=str(REPO_REL_BASE), help="selected_seed_examples directory relative to repo root")
    conv.add_argument("--reports-dir", default=str(CONVERSION_REL_BASE / "reports"), help="conversion reports directory relative to repo root")
    conv.add_argument("--run-id", default="r3-selected-seed-examples-v0", help="stable run id for committed smoke fixture")
    conv.add_argument("--created-at", default=None, help="optional ISO timestamp for deterministic committed fixtures")
    conv.set_defaults(func=convert_selected)

    rec = sub.add_parser("recover-plantuml", help="run R3.1 PlantUML pre-SCXML normalization/recovery audit")
    rec.add_argument("--reports-dir", default=str(CONVERSION_REL_BASE / "reports"), help="conversion reports directory relative to repo root")
    rec.add_argument("--run-dir", default=str(RECOVERY_ARTIFACT_REL_BASE / "workdir"), help="run artifact directory relative to repo root")
    rec.add_argument("--archive-dir", default=str(RECOVERY_ARTIFACT_REL_BASE), help="directory for committed zipped run artifacts relative to repo root; set empty string to skip archive packaging")
    rec.add_argument("--keep-workdir", action="store_true", help="preserve extracted high-cardinality recovery workdir after archive packaging; default deletes it so PRs only carry zip artifacts")
    rec.add_argument("--run-id", default="r3.1-plantuml-recovery-v0", help="stable run id for recovery audit")
    rec.add_argument("--created-at", default=None, help="optional ISO timestamp for deterministic committed fixtures")
    rec.add_argument("--limit", type=int, default=None, help="optional maximum number of PlantUML pairs for smoke/debug")
    rec.add_argument(
        "--pair-source",
        action="append",
        default=None,
        help="PlantUML pairs.jsonl source relative to repo root; may be repeated; defaults to LLMS-EMP and Unified UML seed pairs",
    )
    rec.set_defaults(func=recover_plantuml)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
