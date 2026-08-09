"""扫一代运行里所有发生过降级的格，并判断它们的结果还能不能进统计。

## 为什么必须有这个脚本

降级（CLAUDE.md §10）把「整格崩掉、不落盘」换成「带着残缺产物落盘」。这是对的——崩掉的格等于
样本从被测集里消失，而最容易崩的恰恰是缺陷最硬的那些格。但它的代价是：**降级格产出的制品
看起来完全正常**。`discover-completed.json` 照常存在，`issues` 照常是一个列表，只是那个列表
可能因为某个阶段中途放弃而偏短。

若没有一个专门的扫描口，这批格会安静地混进主结果，把「停止了寻找」记成「没有发现」。
v41 丢的两格是响亮的失败（进程退出、shell 报 RETRY）；降级之后同类问题会变成安静的失败，
**更难发现，不是更少发生**。这个脚本就是把安静重新变响亮。

## 判据

- `degraded_stages` 非空 = 该格有阶段放弃过预算。**这是唯一可靠的判据**，
  `coverage_status == "partial"` 顶不上：逐项隔离也会 partial，那是常态。
- 降级格**仍可进召回侧统计**（它确实产出了制品，命中就是命中）。
- 降级格**不得进精度侧统计**：某个阶段停止了把关，它发布的东西没有经过完整评审。
- 降级格的**零结果不得读作「无缺陷」**。

用法::

    python degradation_audit.py --generation matrix-v42
    python degradation_audit.py --generation matrix-v42 --json
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"


def scan(generation: str) -> dict:
    root = RUNS / generation
    cells: list[dict] = []
    failed: list[dict] = []
    for path in sorted(root.glob("*/*/discover-completed.json")):
        cell = f"{path.parent.parent.name}/{path.parent.name}"
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError) as exc:
            failed.append({"cell": cell, "error": f"{type(exc).__name__}: {exc}"})
            continue
        stages = payload.get("degraded_stages") or []
        gaps = payload.get("coverage_gaps") or []
        cells.append(
            {
                "cell": cell,
                "degraded": bool(stages),
                "degraded_stages": stages,
                "issues": len(payload.get("issues") or []),
                "coverage_status": payload.get("coverage_status"),
                # Degradation gaps carry no assertion ids; isolation gaps do. Counting them
                # apart is what lets a reader see whether the gaps came from routine per-item
                # isolation or from a stage giving up.
                "degradation_gaps": sum(1 for gap in gaps if not gap.get("assertion_ids")),
                "isolation_gaps": sum(1 for gap in gaps if gap.get("assertion_ids")),
            }
        )
    # A cell that never landed is a different problem from a cell that degraded, and after §10
    # it should be rare. Counting it here keeps both visible in one place.
    for path in sorted(root.glob("*/*/discover-failed.json")):
        cell = f"{path.parent.parent.name}/{path.parent.name}"
        if any(item["cell"] == cell for item in cells):
            continue  # a later retry landed; the receipt is stale
        try:
            payload = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            payload = {}
        failed.append(
            {
                "cell": cell,
                "error_type": payload.get("error_type"),
                "error_message": (payload.get("error_message") or "")[:200],
                "degraded_stages": payload.get("degraded_stages") or [],
                "coverage_gaps": len(payload.get("coverage_gaps") or []),
            }
        )
    degraded = [item for item in cells if item["degraded"]]
    return {
        "generation": generation,
        "landed": len(cells),
        "degraded": len(degraded),
        "not_landed": len(failed),
        "cells": cells,
        "degraded_cells": degraded,
        "failed_cells": failed,
        "eligible_for_precision": [
            item["cell"] for item in cells if not item["degraded"]
        ],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generation", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = scan(args.generation)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
        return 0

    print(f"# {result['generation']} 降级审计\n")
    print(
        f"落盘 {result['landed']} 格 ｜ **其中降级 {result['degraded']} 格** ｜ 未落盘 {result['not_landed']} 格\n"
    )
    if result["degraded"]:
        print("## 降级格（结果可进召回侧，不得进精度侧）\n")
        print("| 格 | issue 数 | 降级 gap | 隔离 gap | 放弃的阶段 |\n|:--|--:|--:|--:|:--|")
        for item in result["degraded_cells"]:
            stages = "<br>".join(entry[:110] for entry in item["degraded_stages"])
            print(
                f"| `{item['cell']}` | {item['issues']} | {item['degradation_gaps']} "
                f"| {item['isolation_gaps']} | {stages} |"
            )
        by_node: collections.Counter = collections.Counter(
            entry.split(":", 1)[0]
            for item in result["degraded_cells"]
            for entry in item["degraded_stages"]
        )
        print("\n按节点: " + " ｜ ".join(f"{k} {v}" for k, v in by_node.most_common()))
        zero = [i["cell"] for i in result["degraded_cells"] if i["issues"] == 0]
        if zero:
            print(
                f"\n⚠️ 其中 {len(zero)} 格降级且零 issue —— 这些格的零结果**不得**读作「未发现缺陷」："
                + " ".join(f"`{c}`" for c in zero)
            )
    else:
        print("## 无降级格\n")
    if result["failed_cells"]:
        print("\n## 未落盘（§10 之后应当罕见）\n")
        for item in result["failed_cells"]:
            print(
                f"- `{item['cell']}` {item.get('error_type')} — "
                f"降级轨迹 {len(item.get('degraded_stages') or [])} 条，"
                f"gap {item.get('coverage_gaps', 0)} 条"
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
