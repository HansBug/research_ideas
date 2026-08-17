"""跨臂逐位对拍：⭐ 两臂的判定标准是否一致？⛔ 只定位，⛔ 不裁定。

## 为什么这是 Δ 可能为负时**最先要做**的检查

两臂的判定表键格式**逐字相同**（`<record_id>|run<N>/<pair>-<arm>`），所以可以逐位并列。⭐ 若 X1
的 `hit@1` 高于主臂，只有两种解释，而它们的学术含义完全相反：

| 解释 | 含义 | 怎么区分 |
| :-- | :-- | :-- |
| **A · 真实效应** | 基线确实发现了主臂发现不了的东西 | ⭐ 差异应集中在**主臂零命中池**；且两侧 `argument` 在同形态上给出一致的判据 |
| **B · 判定伪影** | X1 的判定组比主臂那轮判得松 | ⚠️ 差异会**均匀分布**、甚至在主臂满格池上也出现；两侧 `argument` 对同类主张给出不同结论 |

⛔ **不做这个区分就报 Δ，等于把 B 当成 A 发表。**

## ⚠️ 一处已知的材料限制

本工作区**没有主臂的逐格产出**（`runs/paper1/matrix-v46-full/` 不在此 clone）。⭐ 所以对拍的另一
侧只有主臂判定表里的 `argument` 散文——它记着判定者当时读到了什么。⚠️ 这够用来判「判据是否一致」，
⛔ 但不够用来判「主臂那格到底报了什么」。差异位必须按此限制如实标注。

## ⛔ 本模块不裁定

它输出的是一张**工作清单**：每个跨臂分歧位并列两侧 `hit` 与 `argument`，供人工逐条读。
⭐ 判据是那一句：**「若把 X1 这条产出原样放进主臂那一格，我还会判命中吗？」**
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
import sys

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

PAPER = _HERE.parents[1]
# ⚠️⚠️ 2026-08-17：第一版台账、v46 与 v46 时代脚本已整体归档。
# ⛔ 本臂的 588 网格工装（`expected_issue_set.json` 的 98 条分母、`metrics_at_k` 等）
# 属**第一版台账口径**，故 `MATRIX` 重定向到归档树；⭐ 当前口径的 X1v2 结果在
# `discover_matrix/ledger_v2/X1V2_RESULTS.md`，与本处工装无关。
MATRIX = PAPER / "archive" / "r10_ledger_v1_and_v46"
MAIN_HUMAN = MATRIX / "v46" / "verdicts" / "v46_human.json"
MAIN_TIERS = MATRIX / "v46" / "verdicts" / "v46_tiers.json"

from verdicts import expected_keys  # noqa: E402

POOLS = ("full", "near", "unstable", "zero")


def main_arm_positions() -> dict[str, bool | None]:
    """主臂逐位命中，从**格式 B**（`v46_tiers.json`）展开。

    ⭐ 为什么不用 `v46_human.json`：那份只有 574 位（20 位靠 A 层自动确认、不在文件里）。
    ⚠️ 格式 B 是主臂**已发布数字的真源**（`hit@1 = 355/588` 由它算出），⛔ 用它才对得上分母。
    """

    payload = json.loads(MAIN_TIERS.read_text(encoding="utf-8"))
    out: dict[str, bool | None] = {}
    for record_id, value in (payload.get("verdicts") or {}).items():
        if not isinstance(value, dict):
            continue
        pair = record_id.split("-")[1]
        for arm, series in value.items():
            if arm == "direction" or not isinstance(series, list):
                continue
            for index, entry in enumerate(series, 1):
                key = f"{record_id}|run{index}/{pair}-{arm}"
                out[key] = None if entry is None else bool(entry)
    return out


def main_arm_arguments() -> dict[str, str]:
    """主臂逐位的等价性论证（574 位有，20 位无）。"""

    payload = json.loads(MAIN_HUMAN.read_text(encoding="utf-8"))
    return {
        key: str(entry.get("argument") or "")
        for key, entry in payload.items()
        if isinstance(entry, dict)
    }


def pool_of_record() -> dict[str, str]:
    """每条记录在**主臂**的池归属（命中位数 0..6）。⚠️ 只用于诊断分布，⛔ 不进判定材料。"""

    positions = main_arm_positions()
    counts: dict[str, int] = defaultdict(int)
    for key, hit in positions.items():
        if hit:
            counts[key.split("|")[0]] += 1
    out: dict[str, str] = {}
    for record_id in {k.split("|")[0] for k in positions}:
        n = counts.get(record_id, 0)
        out[record_id] = (
            "full" if n >= 6 else "near" if n == 5 else "unstable" if n >= 1 else "zero"
        )
    return out


def compare(x1_table: dict[str, Any]) -> dict[str, Any]:
    main = main_arm_positions()
    main_args = main_arm_arguments()
    pools = pool_of_record()
    x1 = x1_table.get("verdicts") or {}

    cells: dict[str, Counter] = defaultdict(Counter)
    disagreements: list[dict[str, Any]] = []
    both = 0

    for key in expected_keys():
        if key not in x1:
            continue
        entry = x1[key]
        x1_hit = entry.get("hit")
        main_hit = main.get(key)
        if x1_hit is None or main_hit is None:
            continue
        both += 1
        record_id = key.split("|")[0]
        pool = pools.get(record_id, "?")
        if x1_hit and main_hit:
            cells[pool]["both_hit"] += 1
        elif not x1_hit and not main_hit:
            cells[pool]["both_miss"] += 1
        elif x1_hit and not main_hit:
            cells[pool]["x1_only"] += 1
            disagreements.append(
                {
                    "key": key,
                    "pool_of_main_arm": pool,
                    "direction": "x1_only",
                    "x1": {
                        "hit": True,
                        "equivalence_form": entry.get("equivalence_form"),
                        "argument": entry.get("argument"),
                        "judged_by": entry.get("judged_by"),
                    },
                    "main_arm": {
                        "hit": False,
                        "argument": main_args.get(key)
                        or "(该位无逐格 argument：主臂那 20 位之一，或未在 v46_human.json 中)",
                    },
                }
            )
        else:
            cells[pool]["main_only"] += 1
            disagreements.append(
                {
                    "key": key,
                    "pool_of_main_arm": pool,
                    "direction": "main_only",
                    "x1": {
                        "hit": False,
                        "argument": entry.get("argument"),
                        "judged_by": entry.get("judged_by"),
                    },
                    "main_arm": {
                        "hit": True,
                        "argument": main_args.get(key)
                        or "(该位无逐格 argument：主臂那 20 位之一)",
                    },
                }
            )

    totals = Counter()
    for counter in cells.values():
        totals.update(counter)
    return {
        "comparable_positions": both,
        "by_pool": {pool: dict(cells.get(pool, Counter())) for pool in POOLS},
        "totals": dict(totals),
        "disagreements": disagreements,
    }


def diagnose(result: dict[str, Any]) -> list[str]:
    """⭐ 把「真实效应 vs 判定伪影」的判据机械化到可读的程度。⛔ 仍不裁定。"""

    lines: list[str] = []
    by_pool = result["by_pool"]
    totals = result["totals"]
    x1_only = totals.get("x1_only", 0)
    main_only = totals.get("main_only", 0)
    lines.append(
        f"X1 独有命中 {x1_only} 位；主臂独有命中 {main_only} 位；"
        f"净差 {x1_only - main_only:+d} 位"
    )

    # 判据：X1 独有命中若集中在主臂零命中池 → 倾向真实效应；若在满格池也大量出现 → 需查判定标准。
    zero_pool = by_pool.get("zero", {})
    full_pool = by_pool.get("full", {})
    zero_share = zero_pool.get("x1_only", 0) / x1_only if x1_only else 0.0
    full_share = full_pool.get("x1_only", 0) / x1_only if x1_only else 0.0
    lines.append(
        f"X1 独有命中的池分布：零命中池 {zero_pool.get('x1_only', 0)} 位（{zero_share:.1%}）· "
        f"满格池 {full_pool.get('x1_only', 0)} 位（{full_share:.1%}）"
    )
    if full_share > 0.25:
        lines.append(
            "⚠️ 满格池上出现大量 X1 独有命中——满格池是主臂 6/6 稳定命中的记录，"
            "⛔ 在那里 X1 独有命中意味着**主臂在同一位判了未命中**，这需要逐条查判定标准，"
            "⛔ 不能直接读成能力差异。"
        )
    if zero_share > 0.5:
        lines.append(
            "⭐ X1 独有命中过半集中在主臂零命中池——这是「真实效应」的形状："
            "基线在主臂完全没覆盖的缺陷上有产出。⚠️ 仍须逐条读 argument 确认。"
        )
    return lines


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Cross-arm per-position comparison.")
    parser.add_argument("--x1-verdicts", required=True, type=Path)
    parser.add_argument("--out", default=None)
    parser.add_argument("--show", type=int, default=12)
    args = parser.parse_args(argv)

    table = json.loads(args.x1_verdicts.read_text(encoding="utf-8"))
    result = compare(table)

    print(f"comparable positions: {result['comparable_positions']}")
    print(f"totals: {result['totals']}")
    print("by pool (main arm's pools):")
    for pool in POOLS:
        print(f"  {pool:>8}: {result['by_pool'][pool]}")
    print()
    for line in diagnose(result):
        print(line)
    print()
    print(f"disagreements: {len(result['disagreements'])} (showing {args.show})")
    for item in result["disagreements"][: args.show]:
        print(
            f"  - {item['key']} [{item['direction']}, main pool={item['pool_of_main_arm']}]\n"
            f"      X1  ({item['x1'].get('judged_by')}): "
            f"{str(item['x1'].get('argument'))[:160]}\n"
            f"      main: {str(item['main_arm'].get('argument'))[:160]}"
        )

    if args.out:
        result["limitation"] = (
            "⚠️ 本工作区没有主臂逐格产出（runs/paper1/matrix-v46-full/ 不在此 clone），"
            "所以对拍的主臂一侧只有判定表的 argument 散文。够判「判据是否一致」，"
            "⛔ 不够判「主臂那格到底报了什么」。"
        )
        result["criterion"] = (
            "逐条读的判据是：若把 X1 这条产出原样放进主臂那一格，我还会判命中吗？"
        )
        Path(args.out).write_text(
            json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
