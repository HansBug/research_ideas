"""把 `verdict_tiers.py` 的 audit JSON 转成 `full_tables.py` 一族期待的 verdicts 形状。

## 为什么需要这个文件

本目录有两代判定工具，v24 之后断了链：

| 代次 | 判定入口 | 产物形状 |
| :-- | :-- | :-- |
| ≤ v24 | 人工标注 → `onepass_merge.py` | `{"verdicts": {rid: {"claude": [0/1/None×轮], "gpt": [...]}}}` |
| ≥ v35 | `verdict_tiers.py`（A/B/C 三层 + 人工） | `{"audit": [{record_id, cell, hit, ...}]}` |

消费端 —— `full_tables.py`、`metrics_at_k.py`、`build_comment.py`、`generation_history.py` ——
全部只认前一种。于是 v37 / v40 / v41 / v44 四个代次的 comment 表格都是**临时手搓**的，而手搓正是
错误的来源：v41 曾把基线写成 251，两次更正才到 280；v44 曾拿「v44 六格 36 条 issue」去比
「v45 五格 20 条」，分母不同类。这些都不是判定错误，是**呈现环节**的算术错误，而呈现环节本该由
工具承担。

所以这里只做形状转换，**不做任何判定**：`hit` 从哪来、怎么定的，全部仍由 `verdict_tiers.py`
负责。转换器唯一的职责是别把位丢了、别把分母搞错。

## 三个值必须可区分

`1` 命中、`0` 未命中、`null` **无判定**。第三种不是 0：它意味着该格没落盘、或该位没被判过。
把 null 读成 0 会让分母虚高而分子不变，即无声地压低命中率 —— 这是本目录反复出现的错误
（`full_tables.py` 的模块 docstring 记了同一条）。所以：

- 该 pair 该轮该臂**没有落盘的格** → `null`
- 格落盘了但这一位不在 audit 里（未判） → `null`
- 在 audit 里 → `1` / `0`

轮数不写死，由 `runs/paper1/<generation>/run*` 实际存在的目录算出；写死轮数会让缺轮静默变成
`null` 填充，读者看不出是「没跑」还是「没判」。

用法::

    audit_to_verdicts.py --generation matrix-v46-full --audit /tmp/v46_audit.json \
        --out v46/verdicts/v46_tiers.json
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"

ARMS = ("claude", "gpt")

#: `run1/0030-claude` → (`run1`, `0030`, `claude`)。`.try3` 之类的放弃目录不是独立的格。
_CELL = re.compile(r"^(?P<run>run\d+)/(?P<pair>\d{4})-(?P<arm>[a-z0-9.-]+?)(?:\.try\d+)?$")


def parse_cell(cell: str) -> tuple[str, str, str] | None:
    match = _CELL.match(cell.strip())
    if not match:
        return None
    return match["run"], match["pair"], match["arm"]


def landed_cells(generation: str) -> set[tuple[str, str, str]]:
    """哪些 (轮, pair, 臂) 真的落盘了。

    分母只认落盘的格。没落盘的位记 `null` 而不是 `0` —— 「没跑」与「跑了没找到」是两件事，
    混起来会让一次基础设施故障看上去像方法失效。
    """

    found: set[tuple[str, str, str]] = set()
    root = RUNS / generation
    for receipt in root.glob("run*/*/discover-completed.json"):
        parsed = parse_cell(f"{receipt.parent.parent.name}/{receipt.parent.name}")
        if parsed:
            found.add(parsed)
    return found


def rounds_of(generation: str) -> list[str]:
    root = RUNS / generation
    names = sorted(
        (p.name for p in root.glob("run*") if p.is_dir()),
        key=lambda n: int(n[3:]) if n[3:].isdigit() else 0,
    )
    return names


def convert(generation: str, audit_path: pathlib.Path) -> dict:
    audit = json.loads(audit_path.read_text())["audit"]
    runs = rounds_of(generation)
    landed = landed_cells(generation)

    judged: dict[str, dict[tuple[str, str], bool]] = {}
    pair_of: dict[str, str] = {}
    for entry in audit:
        parsed = parse_cell(entry["cell"])
        if parsed is None:
            continue
        run, pair, arm = parsed
        record_id = entry["record_id"]
        judged.setdefault(record_id, {})[(run, arm)] = bool(entry["hit"])
        pair_of[record_id] = pair

    verdicts: dict[str, dict[str, list[int | None]]] = {}
    for record_id, series in judged.items():
        pair = pair_of[record_id]
        row: dict[str, list[int | None]] = {}
        for arm in ARMS:
            values: list[int | None] = []
            for run in runs:
                if (run, pair, arm) not in landed:
                    values.append(None)          # 格没落盘
                elif (run, arm) in series:
                    values.append(1 if series[(run, arm)] else 0)
                else:
                    values.append(None)          # 落盘了但这一位未判
            row[arm] = values
        verdicts[record_id] = row
    return {"generation": generation, "rounds": runs, "verdicts": verdicts}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--generation", required=True)
    parser.add_argument("--audit", required=True, type=pathlib.Path)
    parser.add_argument("--out", type=pathlib.Path)
    args = parser.parse_args(argv)
    payload = convert(args.generation, args.audit)
    text = json.dumps(payload, ensure_ascii=False, indent=1)
    if args.out:
        args.out.write_text(text)
        counts = [
            v
            for row in payload["verdicts"].values()
            for values in row.values()
            for v in values
        ]
        print(
            f"{len(payload['verdicts'])} 条记录 × {len(ARMS)} 臂 × "
            f"{len(payload['rounds'])} 轮 = {len(counts)} 位 ｜ "
            f"命中 {counts.count(1)} ｜ 未命中 {counts.count(0)} ｜ "
            f"无判定 {counts.count(None)} → {args.out}"
        )
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
