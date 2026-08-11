"""合并各判定组的结果 → 格式 A 的总判定表，并过 C 层闸。

⚠️ 判定组编制与主臂 v46 同构（那一轮是「八个并行判定组 + 一组回读原件复核」）。⭐ 所以逐位保留
`judged_by`：它是「同形态被不同组判成不同结果」这种**组间不一致的唯一可查线索**。

## ⛔ 三种「缺」必须区分，行为完全不同

| 缺什么 | 行为 |
| :-- | :-- |
| 某个位**键不存在** | ⛔ 硬错误。⚠️ 一个只判了一半的审计文件与判完的**在形状上无从区分** |
| 某位 `hit: null` | ⭐ 合法（格失败 / 未落盘），⛔ 但必须写明理由 |
| 两个组判了**同一个位** | ⛔ 硬错误：分工重叠说明分配表错了，而重叠位取哪一个都是一次未记录的裁定 |

⛔ **本模块不做任何裁定**：它只合并、校验、报冲突。裁定只能改 `J*.json`。
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

from verdicts import EQUIVALENCE_FORMS, expected_keys, validate  # noqa: E402


def load_groups(verdict_dir: Path) -> dict[str, dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    for path in sorted(verdict_dir.glob("J*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        label = payload.get("judged_by") or path.stem
        if label in groups:
            raise SystemExit(f"duplicate judged_by label {label!r} (from {path})")
        groups[label] = payload
    if not groups:
        raise SystemExit(f"no J*.json found under {verdict_dir}")
    return groups


def merge(groups: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """返回 (格式 A 总表, 问题清单)。"""

    problems: list[str] = []
    positions: dict[str, dict[str, Any]] = {}
    owner: dict[str, str] = {}
    unclaimed: dict[str, list[int]] = {}

    for label, payload in groups.items():
        for pair, block in (payload.get("pairs") or {}).items():
            for key, entry in (block.get("positions") or {}).items():
                if key in owner:
                    problems.append(
                        f"{key}: 被 {owner[key]} 与 {label} 双重判定——分工重叠，"
                        "取哪一个都是一次未记录的裁定"
                    )
                    continue
                owner[key] = label
                enriched = dict(entry) if isinstance(entry, dict) else {}
                enriched["judged_by"] = label
                positions[key] = enriched
            for cell, indices in (block.get("unclaimed_issues") or {}).items():
                if cell in unclaimed:
                    problems.append(f"{cell}: unclaimed_issues 被两个组填过")
                    continue
                unclaimed[cell] = list(indices)
            note = str(block.get("note") or "").strip()
            if note:
                problems.append(f"ℹ️ {label}/{pair} 留了 note（不是错误，需人工过一眼）：{note}")

    table = {
        "_schema": "x1-baseline-arm-verdicts-A/1",
        "_groups": sorted(groups),
        "_equivalence_forms": list(EQUIVALENCE_FORMS),
        "verdicts": positions,
        "unclaimed_issues": unclaimed,
    }
    return table, problems


def summarize(table: dict[str, Any]) -> dict[str, Any]:
    entries = table["verdicts"]
    hit = sum(1 for e in entries.values() if e.get("hit") is True)
    miss = sum(1 for e in entries.values() if e.get("hit") is False)
    null = sum(1 for e in entries.values() if e.get("hit") is None)
    forms = Counter(
        e.get("equivalence_form") for e in entries.values() if e.get("hit") is True
    )
    by_group: dict[str, Counter] = defaultdict(Counter)
    for entry in entries.values():
        by_group[entry.get("judged_by", "?")][
            "hit" if entry.get("hit") is True else ("null" if entry.get("hit") is None else "miss")
        ] += 1
    unclaimed_total = sum(len(v) for v in table.get("unclaimed_issues", {}).values())
    return {
        "positions": len(entries),
        "hit": hit,
        "miss": miss,
        "null": null,
        "hit_rate": (hit / (hit + miss)) if (hit + miss) else None,
        "equivalence_forms": dict(forms),
        "by_group": {g: dict(c) for g, c in sorted(by_group.items())},
        "unclaimed_issue_total": unclaimed_total,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Merge per-group verdicts and gate them.")
    parser.add_argument("--verdict-dir", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    groups = load_groups(Path(args.verdict_dir))
    table, problems = merge(groups)

    gate = validate(table)
    fatal = [p for p in problems if not p.startswith("ℹ️")] + gate

    summary = summarize(table)
    table["_summary"] = summary
    Path(args.out).write_text(
        json.dumps(table, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print(f"groups: {', '.join(sorted(groups))}")
    print(f"positions: {summary['positions']} / {len(expected_keys())}")
    print(f"hit={summary['hit']} miss={summary['miss']} null={summary['null']}")
    if summary["hit_rate"] is not None:
        print(f"raw hit rate (hit / (hit+miss)) = {summary['hit_rate']:.4f}")
    print(f"forms: {summary['equivalence_forms']}")
    print(f"by group: {summary['by_group']}")
    print(f"unclaimed issues: {summary['unclaimed_issue_total']}")
    for note in [p for p in problems if p.startswith("ℹ️")]:
        print(note)
    if fatal:
        print(f"\n⛔ {len(fatal)} 个必须处理的问题：")
        for problem in fatal[:60]:
            print(f"  - {problem}")
        if len(fatal) > 60:
            print(f"  ... 另有 {len(fatal) - 60} 条")
        return 1
    print("\n✅ 合并与 C 层闸全部通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
