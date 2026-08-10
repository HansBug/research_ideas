"""两个代次的同口径对比：只比**两边都已完成的格**，只用 A 层（确定性、无人参与）。

## 为什么需要它，以及为什么只用 A 层

代次间比较最容易出的错是**分母不同却直接比百分比**：一个代次 48 格、另一个 25 格（还在跑），
或两者格集不同。本模块只取交集，并把交集大小打在最前面。

只用 A 层是刻意的：

- A 层是**确定性**的，任何人重跑得到同一结果，所以两代次之间的差不掺入判定者的变化。
- 人工判定跨代次不可比 —— 同一个人在两轮之间会学到东西（v35 那两处作用域误判就是在第二次
  复核时才发现的），而那个学习会被误读成方法变好。

⚠️ **A 层不完备（v35 实测 38%），所以它的差是方向性证据而不是效应量。** 报「提升了多少」必须用
人工判定的完整口径；本模块回答的是「往哪个方向动了、动在哪条记录上」。

用法：

    python -m generation_diff --base matrix-v35 --head matrix-v36
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any

import verdict_tiers as V


def _cells(generation: str) -> dict[tuple[str, str, str], Path]:
    out: dict[tuple[str, str, str], Path] = {}
    root = V.RUNS / generation
    if not root.is_dir():
        raise SystemExit(f"代次目录不存在：{root}")
    for completed in sorted(root.glob("run*/*/discover-completed.json")):
        match = V._CELL.match(completed.parent.name)
        if match:
            out[(completed.parent.parent.name, match.group(1), match.group(2))] = completed.parent
    return out


def compare(base: str, head: str) -> dict[str, Any]:
    ledger = V.ledger_claims()
    base_cells, head_cells = _cells(base), _cells(head)
    common = sorted(set(base_cells) & set(head_cells))
    if not common:
        raise SystemExit(
            f"{base} 与 {head} 没有共同已完成的格 —— 拒绝输出一份看起来正常的空对比"
        )

    def tally(cells: dict[tuple[str, str, str], Path]) -> tuple[collections.Counter, int]:
        hits: collections.Counter = collections.Counter()
        issues = 0
        for key in common:
            directory = cells[key]
            evidence = V.cell_evidence(directory)
            try:
                payload = json.loads((directory / "discover-completed.json").read_text())
            except (OSError, json.JSONDecodeError):
                payload = {}
            issues += len(payload.get("issues") or ())
            for record_id, record in ledger.items():
                if record["pair"] != key[1] or not record["in_scope"]:
                    continue
                if V.tier_a(record, evidence)["matched"]:
                    hits[record_id] += 1
        return hits, issues

    base_hits, base_issues = tally(base_cells)
    head_hits, head_issues = tally(head_cells)
    moved = {
        record_id: {"base": base_hits[record_id], "head": head_hits[record_id]}
        for record_id in set(base_hits) | set(head_hits)
        if base_hits[record_id] != head_hits[record_id]
    }
    return {
        "base": base,
        "head": head,
        "cells_in_base": len(base_cells),
        "cells_in_head": len(head_cells),
        "cells_compared": len(common),
        "pairs_compared": sorted({key[1] for key in common}),
        "tier_a_hits": {"base": sum(base_hits.values()), "head": sum(head_hits.values())},
        "published_issues": {"base": base_issues, "head": head_issues},
        "records_moved": dict(sorted(moved.items())),
    }


def render(result: dict[str, Any]) -> str:
    lines = [
        f"# 同口径对比 — {result['base']} → {result['head']}",
        "",
        f"**只比两边都已完成的 {result['cells_compared']} 格**"
        f"（{result['base']} 共 {result['cells_in_base']}，{result['head']} 共 {result['cells_in_head']}）"
        f"，覆盖 pair {' '.join(result['pairs_compared'])}",
        "",
        "判定只用 A 层：确定性、无人参与，所以两代次之间的差不掺入判定者的变化。"
        "⚠️ A 层不完备（v35 实测 38%），故这是**方向性证据而不是效应量**。",
        "",
        "| 指标 | base | head | 差 |",
        "|:--|--:|--:|--:|",
    ]
    for label, key in (("A 层命中位", "tier_a_hits"), ("已发布 issue", "published_issues")):
        base_value, head_value = result[key]["base"], result[key]["head"]
        lines.append(f"| {label} | {base_value} | {head_value} | {head_value - base_value:+d} |")
    if result["records_moved"]:
        lines += ["", "## 逐记录变动", "", "| 记录 | base | head | |", "|:--|--:|--:|:-:|"]
        for record_id, row in result["records_moved"].items():
            arrow = "↑" if row["head"] > row["base"] else "↓"
            lines.append(f"| `{record_id}` | {row['base']} | {row['head']} | {arrow} |")
    else:
        lines += ["", "A 层逐记录无变动。"]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", required=True, help="例如 matrix-v35")
    parser.add_argument("--head", required=True, help="例如 matrix-v36")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = compare(args.base, args.head)
    print(json.dumps(result, ensure_ascii=False, indent=1) if args.json else render(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
