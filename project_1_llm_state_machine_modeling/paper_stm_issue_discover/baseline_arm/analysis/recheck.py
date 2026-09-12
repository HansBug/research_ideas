"""横向复核：同形态是否被判出两种结果。⛔ 只定位，⛔ 不裁定。

## ⛔ 为什么不能直接用主臂的 `adjudication_recheck.py`

它靠 `published_titles()` 读 run record 的 `issues[i]["title"]`。⛔ X1 的 `NaiveIssue` 没有 `title`
字段 → `coverage()` 恒 `0.0` → 一位都过不了阈值 → **输出「0 对 0 位」**。

⛔⛔ **而「0 对」正是达标判据的形状** —— 于是「检查通过」与「检查根本没有作用对象」在终端上完全
一样。⚠️ 这是本仓库反复出现的最坏失败形态（主臂的 `present_for_judgment.py` docstring 记着同类
事故：「这个脚本曾经在真实路径上**输出零行并 exit 0**」），而 `adjudication_recheck.py` 没有非零
退出保护。

## ⭐ 改动只有一处：把「标题」换成「三字段拼接」

⭐ **台账侧一个字都不改**：`element_forms` / `coverage` / `predicate_of` 全部**直接 import 主臂的
实现**，⛔ 不复制。⚠️ 若各写一份，两臂就是用不同的尺子量同一件事——那比违反隔离更严重。

⭐ 立论对 X1 **同样成立，甚至更成立**（`adjudication_recheck.primary_elements` 的 docstring 逐字）：

> **同一个缺陷，散文可以换着说，元素名不能。**

⚠️ X1 没有谓词名可依赖，指认元素**只能**写元素名，所以这条立论在 X1 上比在主臂上更硬。

## ⛔ 判据不是「0 对」

⚠️ **v46 自己就不是 0 对**：实测 28 对分属 9 族，经人工裁定为工具按元素重合度配对的假阳性。
⛔ 照抄「须为 0 对」会立刻违约。

⭐ **X1 的判据是「每一对都有书面处置」**：逐对判为「工具假阳性」或「真不一致并已更正」。

## ⚠️ 配对条件的一处改动

主臂用「台账 primary 的谓词相同」配对。⭐ X1 侧本无谓词，⛔ 但台账侧仍有——所以这个条件照旧可用，
⚠️ **文档必须写明此处的 predicate 是台账侧属性，⛔ 不是产出侧属性**，否则读者会误以为 X1 有谓词。

⭐ 另加一条 X1 特有的配对维度：**`judged_by` 不同**。⚠️ 判定组编制与主臂同构（八组并行 + 一组
复核），组间不一致是这类工具最该抓的东西，而主臂那份工具在单代次内根本不看组。
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

PAPER = _HERE.parents[1]
# ⚠️⚠️ 2026-08-17：第一版台账、v46 与 v46 时代脚本已整体归档。
# ⛔ 本臂的 588 网格工装（`expected_issue_set.json` 的 98 条分母、`metrics_at_k` 等）
# 属**第一版台账口径**，故 `MATRIX` 重定向到归档树；⭐ 当前口径的 X1v2 结果在
# `discover_matrix/ledger_v2/X1V2_RESULTS.md`，与本处工装无关。
MATRIX = PAPER / "archive" / "r10_ledger_v1_and_v46"
# ⭐ 判定链共用：`analysis/` 属**测量工具**，它与主臂共用尺子正是「同口径」的要求。
# ⛔ 隔离约束的是 `src/`（被测对象），⛔ 不是这里。
if str(MATRIX / "scripts") not in sys.path:
    sys.path.insert(0, str(MATRIX / "scripts"))

import adjudication_recheck as A  # noqa: E402
from verdicts import reportable_records  # noqa: E402

#: 与主臂同值。⚠️ 「漏掉的代价是判定错误留在数据里，误报的代价只是人多读一条」——
#: 主臂实测精度约 1/2，这个比例下多捞一些是划算的。
THRESHOLD = A.DEFAULT_THRESHOLD


def ledger_primary() -> dict[str, str]:
    """record_id → primary 断言表达式。

    ⚠️ 这是台账的「答案」字段之一，⛔ **绝不进判定材料**；⭐ 但复核是判定**之后**由分析者跑的，
    读它不构成泄漏——泄漏的定义是「判定者在判定时看到」。
    """

    out: dict[str, str] = {}
    for record in reportable_records():
        for assertion in record.get("assertions") or []:
            if assertion.get("role") == "primary":
                out[record["id"]] = str(assertion.get("expression") or "")
                break
    return out


def published_texts(run_root: Path, cell: str) -> list[str]:
    """一格的每条 issue 拼成一段可搜索文本。

    ⭐ 这是本模块**唯一**相对主臂的改动：主臂读 `issues[i]["title"]`，X1 拼
    `issue + where + reason` 三个自由文本字段。⛔ 若只读其中一个，元素名可能落在另一个里。
    """

    run, name = cell.split("/")
    path = run_root / run / name / "record.json"
    if not path.is_file():
        return []
    record = json.loads(path.read_text(encoding="utf-8"))
    parsed = record.get("parsed_output") or {}
    texts: list[str] = []
    for issue in parsed.get("issues") or []:
        texts.append(
            " ".join(
                str(issue.get(field) or "") for field in ("issue", "where", "reason")
            )
        )
    return texts


def describe_positions(table: dict[str, Any], run_root: Path) -> list[dict[str, Any]]:
    """每个位算出：台账元素集、被覆盖的元素集、覆盖率、判定、判定组。"""

    primary = ledger_primary()
    rows: list[dict[str, Any]] = []
    for key, entry in (table.get("verdicts") or {}).items():
        record_id, _, cell = key.partition("|")
        expression = primary.get(record_id, "")
        elements = A.element_forms(expression)
        best_ratio, best_covered = 0.0, frozenset()
        for text in published_texts(run_root, cell):
            ratio, covered = A.coverage(elements, text)
            if ratio > best_ratio:
                best_ratio, best_covered = ratio, covered
        rows.append(
            {
                "key": key,
                "record_id": record_id,
                "cell": cell,
                "predicate_of_ledger_primary": A.predicate_of(expression),
                "elements": sorted(elements),
                "covered": sorted(best_covered),
                "coverage": round(best_ratio, 4),
                "hit": entry.get("hit"),
                "judged_by": entry.get("judged_by"),
                "argument": entry.get("argument"),
            }
        )
    return rows


def inconsistencies(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """同形态判出两种结果的对。

    形态由**两侧共同**决定（沿用主臂的立论）：
    * 台账侧：同一条记录的 primary 谓词相同（⚠️ **台账侧属性**，⛔ 不是 X1 的产出属性）
    * 产出侧：issue 覆盖的元素集合**完全相同**

    ⛔ 只看台账相同不行（不同格的制品不同，命中不同是正常的）；⛔ 只看覆盖相同也不行
    （同一句 issue 可能对应不同台账条目）。
    """

    eligible = [r for r in rows if r["coverage"] >= THRESHOLD and r["hit"] is not None]
    buckets: dict[tuple[str, tuple[str, ...]], list[dict[str, Any]]] = defaultdict(list)
    for row in eligible:
        buckets[(row["predicate_of_ledger_primary"], tuple(row["covered"]))].append(row)

    flagged: list[dict[str, Any]] = []
    for (predicate, covered), group in sorted(buckets.items()):
        for left, right in combinations(group, 2):
            if left["hit"] == right["hit"]:
                continue
            flagged.append(
                {
                    "predicate_of_ledger_primary": predicate,
                    "covered_elements": list(covered),
                    "cross_group": left["judged_by"] != right["judged_by"],
                    "left": {k: left[k] for k in ("key", "hit", "judged_by", "argument")},
                    "right": {k: right[k] for k in ("key", "hit", "judged_by", "argument")},
                }
            )
    return flagged


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Locate same-shape/different-verdict pairs in the X1 verdict table."
    )
    parser.add_argument("--verdicts", required=True, type=Path)
    parser.add_argument("--run-root", required=True, type=Path)
    parser.add_argument("--out", default=None)
    args = parser.parse_args(argv)

    table = json.loads(args.verdicts.read_text(encoding="utf-8"))
    rows = describe_positions(table, args.run_root.expanduser().resolve())

    # ⛔ 防「静默全 0」：若一个位都过不了阈值，说明改造失败（例如字段名对不上），
    # ⚠️ 而那与「检查通过」在终端上长得一样。所以这里必须非零退出。
    eligible = [r for r in rows if r["coverage"] >= THRESHOLD]
    print(f"positions: {len(rows)}; above threshold {THRESHOLD}: {len(eligible)}")
    if not eligible:
        print(
            "⛔ 零个位过阈值 —— 这不是「检查通过」，是检查没有作用对象。"
            "先核 published_texts() 是否读到了 issue 文本。",
            flush=True,
        )
        return 2

    flagged = inconsistencies(rows)
    cross = [f for f in flagged if f["cross_group"]]
    print(f"same-shape/different-verdict pairs: {len(flagged)} (cross-group: {len(cross)})")
    print(
        "⚠️ 判据不是「0 对」（v46 自己是 28 对，人工裁定为工具假阳性），"
        "⭐ 而是「每一对都有书面处置」。"
    )
    for item in flagged[:25]:
        print(
            f"  - [{item['predicate_of_ledger_primary']}] {item['covered_elements']}\n"
            f"      {item['left']['key']} hit={item['left']['hit']} ({item['left']['judged_by']})\n"
            f"      {item['right']['key']} hit={item['right']['hit']} ({item['right']['judged_by']})"
        )
    if len(flagged) > 25:
        print(f"  ... 另有 {len(flagged) - 25} 对")

    if args.out:
        Path(args.out).write_text(
            json.dumps(
                {
                    "threshold": THRESHOLD,
                    "positions": len(rows),
                    "above_threshold": len(eligible),
                    "flagged_pairs": flagged,
                    "note": (
                        "predicate_of_ledger_primary 是**台账侧**属性，⛔ 不是 X1 的产出属性——"
                        "X1 不产出谓词。判据是「每一对都有书面处置」，⛔ 不是「0 对」。"
                    ),
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
