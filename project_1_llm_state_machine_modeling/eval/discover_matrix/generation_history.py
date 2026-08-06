"""历代对比表，从盘上的产物直接算。

`CLAUDE.md` §3.7 要求每一轮实验报告**独立可读**，不得让读者去翻前几轮 —— 其中一项是「历代
对比表，覆盖全部已完成代次，并标注每代对应的代码版本与配置差异」。

上一代次那张表是手抄 PR comment 的，于是它继承了 comment 里的每一处错。这里改为从
`runs/paper1/matrix-*` 直接算，能算的只有**结构性事实**：格数、终态、六类结局的条数、覆盖状态、
拒答面、模型臂。

**命中率不在这里。** 命中要人工判定，判定表只有 v21 与 v22 有（更早的代次判定表没入库，只在
各自的 PR comment 里）。硬把它们凑进同一张表，等于把不同判定口径的数字并排放 —— 而口径本身
在这些代次之间变过（`HIT_CRITERION.md` §6 记着已用语义同一性原则修正过的结论）。所以这张表
只给可从产物复算的量，命中率一列留给判定表能覆盖的代次。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RUNS = ROOT / "runs" / "paper1"
_ROUND = re.compile(r"^run\d+$")
#: `matrix-i175/` 是历史遗留的公共父目录，v2 到 v20 的轮次目录全在它下面，形如 `v10run1`。
#: 上一版只认 `run<N>`，于是那十九个代次一个都没进历代对比表 —— 而这张表的全部意义就是覆盖
#: 全部已完成代次（CLAUDE.md §3.7）。`.aborted-*` 后缀的按其名字排除：那些是作废的运行。
_LEGACY_ROUND = re.compile(r"^(v\d+[a-z]?(?:-[a-z]+)?)run(\d+)$")


def legacy_generations(directory: pathlib.Path) -> dict[str, list[pathlib.Path]]:
    """`matrix-i175/` 下按 `<gen>run<N>` 命名的历史代次。

    这批目录是 v2--v20 的真实产物。把它们排除在历代对比表之外，表就只剩三四行，而 §3.7 要的
    是「覆盖全部已完成代次」。作废的运行按其目录名后缀排除，并在输出里点名，不静默丢。
    """

    found: dict[str, list[pathlib.Path]] = collections.defaultdict(list)
    for child in sorted(directory.iterdir()):
        if not child.is_dir():
            continue
        match = _LEGACY_ROUND.match(child.name)
        if match:
            found[match.group(1)].append(child)
    return dict(found)


def scan(directory: pathlib.Path, rounds: list[pathlib.Path] | None = None,
         label: str | None = None) -> dict:
    # 只认 `run<N>`。`matrix-i175/` 下还有 `smoke/` 与 `v10run1/`，把它们当轮次会让「臂」
    # 变成 `2+3+504+claude+gpt` —— 那些是从别的目录结构里切出来的碎片。与 count_refusals
    # 同一条口径，跳过的目录名报出来而不是静默吞掉。
    explicit = rounds is not None
    if rounds is None:
        rounds = [d for d in sorted(directory.iterdir()) if d.is_dir() and _ROUND.match(d.name)]
    # 跳过清单只在扫父目录时算。历史代次共用同一个父目录，逐个重算会把同一份清单打印十九遍。
    skipped = [] if explicit else [
        d.name for d in sorted(directory.iterdir())
        if d.is_dir() and not _ROUND.match(d.name) and not _LEGACY_ROUND.match(d.name)
    ]
    if not rounds:
        rounds, skipped = [directory], []
    cells = completed = failed = 0
    totals: collections.Counter = collections.Counter()
    coverage: collections.Counter = collections.Counter()
    arms: set[str] = set()
    for round_dir in rounds:
        for cell in sorted(p for p in round_dir.iterdir() if p.is_dir() and "try" not in p.name):
            if "-" not in cell.name:
                continue
            cells += 1
            arm = cell.name.rsplit("-", 1)[-1]
            # 已知臂名之外的一律不计入。目录名格式在代次之间变过，把切出来的碎片当臂名，
            # 会让表里出现 `2+3+504+claude+gpt` 这种读不出意思的单元格。
            if arm in {"claude", "gpt"} or arm.startswith(("claude-", "gpt-")):
                arms.add(arm.split("-")[0])
            final = cell / "discover-completed.json"
            if not final.is_file():
                failed += 1
                continue
            completed += 1
            payload = json.loads(final.read_text())
            coverage[payload.get("coverage_status", "?")] += 1
            for key in ("issues", "excluded_findings", "excluded_observations", "coverage_gaps"):
                totals[key] += len(payload.get(key) or [])
    return {
        "generation": label or directory.name,
        "source": "legacy" if explicit else "own_dir",
        "rounds": len(rounds),
        "skipped_dirs": skipped,
        "cells": cells,
        "completed": completed,
        "failed": failed,
        "arms": sorted(arms),
        "coverage": dict(coverage),
        **{k: totals[k] for k in
           ("issues", "excluded_findings", "excluded_observations", "coverage_gaps")},
    }


def _order(name: str) -> tuple:
    """按版本号排，不按字典序 —— 否则 `v10` 排在 `v2` 前面。"""

    match = re.search(r"v(\d+)", name)
    return (0 if match else 1, int(match.group(1)) if match else 0, name)


def _verdict_ratio(generation: str) -> str:
    """该代次能力主张带的 hit@1，仅当判定表已入库。没有就明说没有，不猜。"""

    path = HERE / "verdicts" / f"{generation.replace('matrix-', '')}_as_published.json"
    if not path.is_file():
        return "—"
    import metrics_at_k as mk

    payload = json.loads(path.read_text())
    verdicts = payload.get("verdicts") or {}
    hits = triples = 0
    for record_id in mk.REPORTABLE:
        for series in mk._arms(verdicts.get(record_id, {})).values():
            valid = [x for x in series if x is not None]
            hits += sum(valid)
            triples += len(valid)
    return f"{hits}/{triples} = {hits / triples * 100:.1f}%" if triples else "—"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--only", help="逗号分隔的代次名过滤，如 v18,v21,v22")
    args = parser.parse_args(argv)
    if not RUNS.is_dir():
        print(f"no {RUNS}", file=sys.stderr)
        return 2
    wanted = {w.strip() for w in (args.only or "").split(",") if w.strip()}
    rows = []
    for directory in sorted(RUNS.glob("matrix-*")):
        if wanted and not any(w in directory.name for w in wanted):
            continue
        try:
            rows.append(scan(directory))
        except OSError:
            continue
        # 历史代次寄居在同一个父目录下，逐个展开。
        for generation, round_dirs in sorted(legacy_generations(directory).items()):
            if wanted and not any(w in generation for w in wanted):
                continue
            try:
                rows.append(scan(directory, rounds=round_dirs, label=generation))
            except OSError:
                continue
    rows.sort(key=lambda r: (_order(r["generation"]), r["source"]))
    if not rows:
        print("no generations found", file=sys.stderr)
        return 2
    if args.markdown:
        print("| 代次 | 轮 | 格 | 完成 | 臂 | full/partial | issues | excluded | observations "
              "| gaps | 能力主张带 hit@1 |")
        print("| --- | --: | --: | --: | --- | --- | --: | --: | --: | --: | --- |")
        for row in rows:
            cov = "/".join(str(row["coverage"].get(k, 0)) for k in ("full", "partial"))
            # 父目录 `matrix-v18/` 与 `matrix-i175/v18run*` 都叫 v18，是同一代次的两处产物。
            # 不合并（轮数、臂、格集都不同），改为标出来源，让读者知道为什么有两行。
            name = row["generation"].replace("matrix-", "")
            if row["source"] == "legacy":
                name += " *(i175/)*"
            print(
                f"| `{name}` | {row['rounds']} | {row['cells']} "
                f"| {row['completed']} | {'+'.join(row['arms']) or '—'} | {cov} "
                f"| {row['issues']} | {row['excluded_findings']} | {row['excluded_observations']} "
                f"| {row['coverage_gaps']} | {_verdict_ratio(row['generation'])} |"
            )
        skipped = {r["generation"]: r["skipped_dirs"] for r in rows if r.get("skipped_dirs")}
        if skipped:
            print(f"\n跳过的非轮次目录：{skipped}")
        print("\n⚠️ **命中率只有判定表已入库的代次才有。** 更早代次的判定只存在于各自的 PR "
              "comment 里，而判定口径在这些代次之间变过（见 `HIT_CRITERION.md` §6），"
              "把它们并排放等于把不同口径的数字放在一列。")
    else:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
