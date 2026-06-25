from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .adapters import convert_plantuml, convert_ttool_xml, convert_umple
from .models import Loss
from .report import make_example_report, sha256_file, write_json
from .toolchain import ToolchainSetupError, preflight_for_format
from .normalization.recovery import run_recovery

REPO_REL_BASE = Path("project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples")
CONVERSION_REL_BASE = Path("project_1_llm_state_machine_modeling/paper_stm_repair/conversion")


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
        source_stm0_hash_match = stm_hash == source_pair_stm0_sha256
        normalization_documented = bool(meta.get("hash_scope")) and meta_source_stm0_sha256 == source_pair_stm0_sha256
        row = {
            "example_id": example_dir.name,
            "nl_path": _rel(nl_path, repo_root),
            "stm0_path": _rel(stm_path, repo_root),
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
            "source_nl_hash_match": nl_hash == source_pair_nl_sha256,
            "source_stm0_hash_match": source_stm0_hash_match,
            "source_hash_divergence_documented": source_stm0_hash_match or normalization_documented,
            "hash_scope": meta.get("hash_scope"),
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


def convert_one(repo_root: Path, example_dir: Path, reports_dir: Path, run_id: str, conversion_command: str, created_at: str | None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    meta = _load_meta(example_dir)
    stm_path = _find_stm(example_dir)
    fmt = meta["stm_format"]
    try:
        preflight = preflight_for_format(fmt, stm_path, example_id=example_dir.name, repo_root=repo_root, reports_dir=reports_dir).to_metadata()
    except ToolchainSetupError as exc:
        raise SystemExit(f"R3 conversion toolchain setup failed for {example_dir.name}:\n{exc}") from None
    kwargs = {"example_id": example_dir.name, "seed_id": meta["seed_id"], "source_format": fmt}
    if fmt == "plantuml":
        result = convert_plantuml(stm_path, preflight=preflight, repo_root=repo_root, **kwargs)
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
        "| example_id | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | syntax | structured export | losses | 说明 |",
        "|---|---|---|---:|---:|---|---|---|---|---:|---|",
    ]
    for report in reports:
        reason = (report.get("blocking_reason") or "").replace("|", "/")
        preflight = report.get("tool_preflight") or {}
        syntax_status = (preflight.get("syntax_status") or "").replace("|", "/")
        structured_status = (preflight.get("structured_export_status") or "").replace("|", "/")
        lines.append(
            f"| `{report['example_id']}` | `{report['source_format']}` | `{report['status']}` | "
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
        and row["source_nl_hash_match"]
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
    report = run_recovery(
        repo_root=repo_root,
        reports_dir=repo_root / args.reports_dir,
        run_dir=repo_root / args.run_dir,
        run_id=args.run_id,
        pair_sources=[Path(p) for p in args.pair_source] if args.pair_source else None,
        limit=args.limit,
        created_at=args.created_at,
        generation_command=generation_command,
    )
    summary = report["summary"]
    print(json.dumps({
        "reports_dir": str(repo_root / args.reports_dir),
        "run_dir": str(repo_root / args.run_dir),
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
    rec.add_argument("--run-dir", default="runs/paper_stm_repair/conversion/plantuml_recovery/r3_1_committed", help="run artifact directory relative to repo root")
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
