"""判定前的分母核对：每条记录必须恰好 6 位，缺的位计为未命中而不是从分母剔除。

## 为什么这必须是脚本

v33 的单 pair 诊断里，一轮崩掉没落盘，我用「已落盘轮」当分母报成 `2/2` 而不是 `2/3` ——
**那等于把丢格从分母里悄悄去掉**，而一个越容易崩的改动看起来越好。用户当场指出「为什么分母
变成 2 了」。

这类错误的特征是**看起来完全正常**：一个 88 位的覆盖率与一个 99 位的覆盖率在报告里长得一样，
只有分母那一行会露出来，而那一行恰好是最容易被写成「记录数 × 6」的推算值而非实测值。

所以分母不推算，逐记录数。

## 检查项

| 检查 | 判据 | 不通过时 |
| :-- | :-- | :-- |
| 总格数 | 落盘数 = `GRID.txt` 的 pair 数 × 6 | 用同一 `BASE` 重跑启动器续跑 |
| 逐记录位数 | 每条可判定记录**恰好** 6 位 | 缺的位计为未命中，并点名是哪一格 |
| 格集一致 | `GRID.txt` 与实际落盘的 pair 集合一致 | 说明差异来源 |

用法：

    python -m check_denominator --generation matrix-v37
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any

import verdict_tiers as V


def check(base: Path) -> dict[str, Any]:
    declared = base / "GRID.txt"
    grid_declared = (
        sorted(
            token
            for token in declared.read_text().split()
            if len(token) == 4 and token.isdigit()
        )
        if declared.is_file()
        else []
    )
    landed_cells: set[tuple[str, str, str]] = set()
    for completed in base.glob("run*/*/discover-completed.json"):
        match = V._CELL.match(completed.parent.name)
        if match:
            landed_cells.add(
                (completed.parent.parent.name, match.group(1), match.group(2))
            )
    grid_landed = sorted({pair for _r, pair, _a in landed_cells})

    ledger = V.ledger_claims()
    # 可判定 = 在格集内且 in_scope。`expressible` 不参与分母 —— 台账自陈不可表达的记录仍在
    # 范围内，把它剔除会让分母随口径浮动（v35 那次两个分母混用就是这么来的）。
    judgeable = {
        record_id: record
        for record_id, record in ledger.items()
        if record["pair"] in set(grid_declared or grid_landed) and record["in_scope"]
    }
    expected_cells = [
        (f"run{r}", arm) for r in (1, 2, 3) for arm in ("claude", "gpt")
    ]
    per_record: dict[str, list[str]] = {}
    for record_id, record in judgeable.items():
        missing = [
            f"{run}/{record['pair']}-{arm}"
            for run, arm in expected_cells
            if (run, record["pair"], arm) not in landed_cells
        ]
        per_record[record_id] = missing
    incomplete = {rid: miss for rid, miss in per_record.items() if miss}
    return {
        "base": str(base),
        "grid_declared": grid_declared,
        "grid_landed": grid_landed,
        "grid_matches": (not grid_declared) or grid_declared == grid_landed,
        "cells_expected": len(grid_declared or grid_landed) * 6,
        "cells_landed": len(landed_cells),
        "judgeable_records": len(judgeable),
        "positions_expected": len(judgeable) * 6,
        "positions_landed": sum(6 - len(m) for m in per_record.values()),
        "records_incomplete": incomplete,
        "pairs_with_no_judgeable_record": sorted(
            set(grid_declared or grid_landed) - {r["pair"] for r in judgeable.values()}
        ),
    }


def render(result: dict[str, Any]) -> str:
    ok = "✅"
    bad = "❌"
    lines = [
        f"# 分母核对 — {Path(result['base']).name}",
        "",
        f"| 检查 | 值 | |",
        f"|:--|--:|:-:|",
        f"| 格集（`GRID.txt`） | {len(result['grid_declared'])} pair | "
        f"{ok if result['grid_matches'] else bad} |",
        f"| 落盘格数 | {result['cells_landed']} / {result['cells_expected']} | "
        f"{ok if result['cells_landed'] >= result['cells_expected'] else bad} |",
        f"| 可判定记录 | {result['judgeable_records']} | |",
        f"| **判定位** | **{result['positions_landed']} / {result['positions_expected']}** | "
        f"{ok if not result['records_incomplete'] else bad} |",
        "",
    ]
    if not result["grid_matches"]:
        missing = sorted(set(result["grid_declared"]) - set(result["grid_landed"]))
        lines += [
            f"⚠️ `GRID.txt` 声明的 pair 与落盘的不一致，缺：{missing}",
            "",
        ]
    if result["records_incomplete"]:
        lines += [
            f"⚠️ **{len(result['records_incomplete'])} 条记录不足 6 位。"
            "缺的位必须计为未命中，不得从分母剔除。**",
            "",
            "| 记录 | 缺的格 |",
            "|:--|:--|",
        ]
        for record_id, missing in sorted(result["records_incomplete"].items()):
            lines.append(f"| `{record_id}` | {' '.join(missing)} |")
        lines.append("")
    else:
        lines += ["每条可判定记录都恰好 6 位，分母可用。", ""]
    if result["pairs_with_no_judgeable_record"]:
        pairs = result["pairs_with_no_judgeable_record"]
        lines += [
            f"格集内无可判定记录的 pair（{len(pairs)} 个）：{' '.join(pairs)}",
            "",
            "它们的格只进精度侧（`grounded-extra` / `fabricated` / `boundary`），不产生召回分母。",
        ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base")
    parser.add_argument("--generation")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.base:
        base = Path(args.base)
        if not base.is_absolute():
            base = V.REPO / base
    elif args.generation:
        base = V.RUNS / args.generation
    else:
        raise SystemExit("需要 --base 或 --generation")
    if not base.is_dir():
        raise SystemExit(f"运行目录不存在：{base}")
    result = check(base)
    print(json.dumps(result, ensure_ascii=False, indent=1) if args.json else render(result))
    # 分母不完整时非零退出 —— 让它在流程里挡住后续判定
    return 1 if (result["records_incomplete"] or not result["grid_matches"]) else 0


if __name__ == "__main__":
    raise SystemExit(main())
