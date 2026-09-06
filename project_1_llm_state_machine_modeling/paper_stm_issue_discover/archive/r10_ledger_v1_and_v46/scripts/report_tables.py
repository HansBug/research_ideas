"""Render the report's data section from an audit bundle.

Kept separate from `build_gist.py` because it answers a different question.  That
script produces the evidence; this one produces the tables a reader sees first, and
the two must not drift -- so every number here is read out of the bundle rather
than recomputed.

Three tables:

  per-cell     terminal state, issue and exclusion counts, expected-issue verdicts,
               LLM calls and wall time
  verdicts     the hit/miss ledger rolled up, with the denominator spelled out
  fabrication  what `_fabrication_scan.json` found, including the case where it
               did not run -- an absent scan is reported, never treated as clean

Usage: report_tables.py <audit_dir> [previous_audit_dir]
    With a second bundle, adds a delta column so a claim of improvement can be
    checked against the run it improved on.
"""

from __future__ import annotations

import json
import pathlib
import sys
from collections import Counter

PROFILE_SHORT = {"gpt-5.5": "gpt", "claude-opus-4-7": "claude"}


def _cells(audit_dir: pathlib.Path) -> list[dict]:
    out = []
    for path in sorted(audit_dir.glob("*-audit.json")):
        record = json.loads(path.read_text())
        artifact = record.get("terminal_artifact") or {}
        verdicts = record.get("expected_issue_verdicts") or []
        out.append({
            "cell": path.name.removesuffix("-audit.json"),
            "pair": record.get("pair"),
            "profile": record.get("profile"),
            "terminal": record.get("terminal"),
            "issues": len(artifact.get("issues") or []),
            "excluded": len(artifact.get("excluded_findings") or []),
            "satisfied": len(artifact.get("satisfied_requirement_ids") or []),
            "requirements": len(record.get("requirements") or []),
            "assertions": len(record.get("assertions") or []),
            "llm_calls": (record.get("telemetry") or {}).get("llm_calls"),
            "elapsed_ms": (record.get("telemetry") or {}).get("node_elapsed_ms"),
            "verdicts": [
                (v.get("expected_issue") or "", v.get("verdict") or "") for v in verdicts
            ],
            "provenance": record.get("expected_ledger_provenance"),
        })
    return out


def _short(cell: dict) -> str:
    return f"{cell['pair']}-{PROFILE_SHORT.get(cell['profile'], cell['profile'])}"


def per_cell_table(cells: list[dict], previous: dict[str, dict] | None = None) -> str:
    head = "| 格子 | 终态 | 需求 | 断言 | issues | excluded | satisfied | LLM | 耗时 | 期望缺陷判定 |"
    rule = "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |"
    rows = [head, rule]
    for cell in cells:
        verdicts = "; ".join(
            f"`{eid.replace('EXP-', '')}`={verdict}" if eid else verdict
            for eid, verdict in cell["verdicts"]
        ) or "—"
        if cell["terminal"] != "completed":
            # A cell that did not finish has no issue count, and printing its zero
            # beside a previous run's number reads as "the false positive is gone".
            # That is the same mistake the false-positive checker refuses to make,
            # and it is worse here because a table is what gets quoted.
            issues = "—"
        else:
            issues = str(cell["issues"])
            if previous and _short(cell) in previous:
                was = previous[_short(cell)]
                if was["terminal"] == "completed" and was["issues"] != cell["issues"]:
                    issues = f"{cell['issues']} (前轮 {was['issues']})"
        minutes = (
            f"{cell['elapsed_ms'] / 60000:.0f}m" if cell.get("elapsed_ms") else "—"
        )
        done = cell["terminal"] == "completed"
        rows.append(
            f"| `{_short(cell)}` | {cell['terminal']} | {cell['requirements']} | "
            f"{cell['assertions']} | {issues} | "
            f"{cell['excluded'] if done else '—'} | "
            f"{cell['satisfied'] if done else '—'} | "
            f"{cell['llm_calls'] or '—'} | {minutes} | {verdicts} |"
        )
    return "\n".join(rows)


def verdict_rollup(cells: list[dict]) -> str:
    counts: Counter[str] = Counter()
    for cell in cells:
        for _eid, verdict in cell["verdicts"]:
            counts[verdict] += 1
    total = sum(counts.values())
    lines = ["| 判定 | 条数 | 占比 |", "| --- | ---: | ---: |"]
    for verdict, n in counts.most_common():
        lines.append(f"| {verdict} | {n} | {n / total:.0%} |")
    lines.append(f"| **合计** | **{total}** | |")
    # The denominator is not the number of cells: pairs carry 0, 1 or 3 expected
    # issues, and a pair with none contributes one "no expected issue" row.
    with_expected = sum(
        1 for cell in cells for eid, _v in cell["verdicts"] if eid.startswith("EXP-")
    )
    lines.append("")
    lines.append(
        f"分母说明：{len(cells)} 个格子共 {total} 条判定，其中 {with_expected} 条对应 "
        f"ledger 中的具名 expected issue，其余为「本 pair 无期望问题」行。"
    )
    unfinished = [c for c in cells if c["terminal"] != "completed"]
    if unfinished:
        lines.append("")
        lines.append(
            "**本轮有未完成格子**："
            + "、".join(f"`{_short(c)}`（{c['terminal']}）" for c in unfinished)
            + "。其判定记为「run 未完成」，既不计命中也不计未命中；"
            "在这些格子终态之前，本表的命中率不是完整结果。"
        )
    return "\n".join(lines)


def fabrication_section(audit_dir: pathlib.Path) -> str:
    path = audit_dir / "_fabrication_scan.json"
    if not path.exists():
        return (
            "**捏造扫描未产出。** 该 bundle 不携带任何方向的证据，"
            "其缺失不得读作干净结果。"
        )
    scan = json.loads(path.read_text())
    if "error" in scan:
        return (
            f"**捏造扫描失败**：`{scan['error']}`。"
            f"覆盖格子 {len(scan.get('cells_scanned') or [])} 个但未完成检查，"
            "不得读作干净结果。"
        )
    findings = scan.get("findings") or []
    header = (
        f"扫描于 commit `{scan.get('git_commit', '?')[:8]}`，"
        f"覆盖 {len(scan.get('cells_scanned') or [])} 个格子，"
        f"发现 **{len(findings)}** 条站不住的已发布 issue。"
    )
    if not findings:
        return header + "\n\n每条已发布 issue 的主断言仍重算为 False，且其证据未触及归因排除元素。"
    lines = [header, "", "| 格子 | 需求 | 类别 | 证据 |", "| --- | --- | --- | --- |"]
    for row in findings:
        lines.append(
            f"| `{row['cell']}` | `{row['requirement_id']}` | "
            f"`{row['defect_class']}` | {row['evidence']} |"
        )
    return "\n".join(lines)


def main() -> int:
    if not 2 <= len(sys.argv) <= 3:
        print(__doc__)
        return 2
    audit_dir = pathlib.Path(sys.argv[1])
    cells = _cells(audit_dir)
    previous = None
    if len(sys.argv) == 3:
        previous = {_short(c): c for c in _cells(pathlib.Path(sys.argv[2]))}

    print("### 逐格结果\n")
    print(per_cell_table(cells, previous))
    print("\n### 判定汇总\n")
    print(verdict_rollup(cells))
    print("\n### 捏造扫描\n")
    print(fabrication_section(audit_dir))
    provenance = {c.get("provenance") for c in cells}
    print(
        f"\n### expected ledger 来源\n\n每份审计产物记录的 provenance："
        f"{', '.join(sorted(str(p) for p in provenance))}。"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
