from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .adapters import convert_plantuml, convert_ttool_xml, convert_umple
from .report import make_example_report, sha256_file, write_json

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
        row = {
            "example_id": example_dir.name,
            "nl_path": _rel(nl_path, repo_root),
            "stm0_path": _rel(stm_path, repo_root),
            "stm_format": meta["stm_format"],
            "nl_sha256": nl_hash,
            "stm0_sha256": stm_hash,
            "expected_nl_sha256": meta["nl_sha256"],
            "expected_stm0_sha256": meta["stm0_sha256"],
            "nl_hash_match": nl_hash == meta["nl_sha256"],
            "stm0_hash_match": stm_hash == meta["stm0_sha256"],
            "source_pairs_jsonl": _rel((example_dir / meta["source_pairs_jsonl"]).resolve(), repo_root),
        }
        row["source_pairs_exists"] = (repo_root / row["source_pairs_jsonl"]).exists()
        audit.append(row)
    return audit


def _tool_info(adapter: str, meta: dict[str, Any]) -> dict[str, Any]:
    if adapter == "plantuml":
        return {
            "tool_name": "PlantUML syntax / minimal R3 adapter",
            "tool_version": "local-minimal-parser-v0; external plantuml jar not required for AST",
            "tool_source_url": "https://plantuml.com/command-line",
            "tool_invocation_status": "fallback_parser_used_after_toolchain_survey_no_stable_ast",
            "raw_locator": meta.get("source_locator"),
            "manual_normalization": False,
        }
    if adapter == "umple":
        return {
            "tool_name": "Umple textual syntax / minimal R3 adapter",
            "tool_version": "local-minimal-parser-v0; official Umple compiler surveyed",
            "tool_source_url": "https://cruise.umple.org/umple/",
            "tool_invocation_status": "fallback_parser_used_for_smoke_after_official_toolchain_survey",
            "raw_locator": meta.get("source_locator"),
            "manual_normalization": False,
        }
    return {
        "tool_name": "TTool / AVATAR XML inventory adapter",
        "tool_version": "local-xml-inventory-v0; official TTool surveyed",
        "tool_source_url": "https://ttool.telecom-paris.fr/",
        "tool_invocation_status": "partial_inventory_only_no_t0_slice",
        "raw_locator": meta.get("source_locator"),
        "manual_normalization": False,
    }


def convert_one(repo_root: Path, example_dir: Path, reports_dir: Path, run_id: str, conversion_command: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    meta = _load_meta(example_dir)
    stm_path = _find_stm(example_dir)
    fmt = meta["stm_format"]
    kwargs = {"example_id": example_dir.name, "seed_id": meta["seed_id"], "source_format": fmt}
    if fmt == "plantuml":
        result = convert_plantuml(stm_path, **kwargs)
    elif fmt == "umple":
        result = convert_umple(stm_path, **kwargs)
    elif fmt == "ttool_xml":
        result = convert_ttool_xml(stm_path, **kwargs)
    else:
        raise ValueError(f"Unsupported stm_format for R3: {fmt}")

    canonical_dir = reports_dir / "canonical"
    canonical_output_path: Path | None = None
    canonical_output_sha256: str | None = None
    if result.status in {"converted", "partial"}:
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
        tool_info=_tool_info(result.adapter, meta),
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
        "| example_id | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | losses | 说明 |",
        "|---|---|---|---:|---:|---|---|---:|---|",
    ]
    for report in reports:
        reason = (report.get("blocking_reason") or "").replace("|", "/")
        lines.append(
            f"| `{report['example_id']}` | `{report['source_format']}` | `{report['status']}` | "
            f"{report['states_count']} | {report['transitions_count']} | `{report['timing_level']}` | "
            f"`{report['hierarchy_level']}` | {report['losses_count']} | {reason} |"
        )
    lines.extend([
        "",
        f"Loss ledger 行数：{len(loss_rows)}",
        "",
        "所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。",
        "",
    ])
    path.write_text("\n".join(lines), encoding="utf-8")


def convert_selected(args: argparse.Namespace) -> int:
    repo_root = _repo_root_from_cwd()
    selected_dir = repo_root / args.selected_dir
    reports_dir = repo_root / args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    audit = audit_inputs(repo_root, selected_dir)
    if not all(row["nl_hash_match"] and row["stm0_hash_match"] and row["source_pairs_exists"] for row in audit):
        raise SystemExit("selected_seed_examples input audit failed; inspect selected_seed_examples_input_audit.json")
    write_json(reports_dir / "selected_seed_examples_input_audit.json", {"items": audit})

    conversion_command = "python -m paper_stm_repair_conversion.cli convert-selected"
    run_id = args.run_id
    reports: list[dict[str, Any]] = []
    loss_rows: list[dict[str, Any]] = []
    for example_dir in sorted(p for p in selected_dir.iterdir() if p.is_dir()):
        report, losses = convert_one(repo_root, example_dir, reports_dir, run_id, conversion_command)
        reports.append(report)
        loss_rows.extend(losses)
    loss_sha = _write_loss_ledger(reports_dir / "selected_seed_examples_loss_ledger.jsonl", loss_rows)
    report_doc = {
        "report_version": "r3.selected_seed_examples_conversion_report.v0",
        "run_id": run_id,
        "items": reports,
        "loss_ledger_sha256": loss_sha,
        "note": "R3 smoke fixture only; not main experiment evidence. Item report_sha256 is the SHA-256 of the report document before embedding that hash into item rows, avoiding a misleading self-referential hash.",
    }
    pre_embed_report_sha = write_json(reports_dir / "selected_seed_examples_conversion_report.json", report_doc)
    for item in report_doc["items"]:
        item["report_sha256"] = pre_embed_report_sha
    write_json(reports_dir / "selected_seed_examples_conversion_report.json", report_doc)
    _write_summary(reports_dir / "selected_seed_examples_summary.md", reports, loss_rows)
    print(json.dumps({"reports_dir": str(reports_dir), "examples": len(reports), "losses": len(loss_rows)}, ensure_ascii=False, indent=2))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="R3 paper_stm_repair conversion v0 CLI")
    sub = parser.add_subparsers(dest="command", required=True)
    conv = sub.add_parser("convert-selected", help="convert selected_seed_examples into R3 canonical/report fixtures")
    conv.add_argument("--selected-dir", default=str(REPO_REL_BASE), help="selected_seed_examples directory relative to repo root")
    conv.add_argument("--reports-dir", default=str(CONVERSION_REL_BASE / "reports"), help="conversion reports directory relative to repo root")
    conv.add_argument("--run-id", default="r3-selected-seed-examples-v0", help="stable run id for committed smoke fixture")
    conv.set_defaults(func=convert_selected)
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
