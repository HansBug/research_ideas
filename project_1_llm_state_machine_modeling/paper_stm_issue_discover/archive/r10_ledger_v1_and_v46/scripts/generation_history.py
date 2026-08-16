"""历代对比表，从盘上的产物直接算。

`CLAUDE.md` §3.7 要求每一轮实验报告**独立可读**，不得让读者去翻前几轮 —— 其中一项是「历代
对比表，覆盖全部已完成代次，并标注每代对应的代码版本与配置差异」。

上一代次那张表是手抄 PR comment 的，于是它继承了 comment 里的每一处错。这里改为从
`runs/paper1/matrix-*` 直接算，能算的只有**结构性事实**：格数、终态、六类结局的条数、覆盖状态、
拒答面、模型臂。

**命中率不在这里。** 命中要人工判定，判定表只有 v21 与 v22 有（更早的代次判定表没入库，只在
各自的 PR comment 里）。硬把它们凑进同一张表，等于把不同判定口径的数字并排放 —— 而口径本身
在这些代次之间变过（`docs/protocol/hit_criterion.md` §6 记着已用语义同一性原则修正过的结论）。所以这张表
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
#: 格目录下最新文件在这个窗口内被改过，即判为「进行中」而非「失败」。
#: 单格实测耗时 10–40 分钟（某格曾达 40 分钟，见 `docs/generations/v22/backlog.md` L-4），故取 45 分钟。
_IN_FLIGHT_WINDOW = 45 * 60


#: 格目录下最新文件在这个窗口内被改过，即判为「进行中」而非「失败」。
#: 单格实测耗时 10–40 分钟（某格曾达 40 分钟），故取 45 分钟。
_IN_FLIGHT_WINDOW = 45 * 60


def _now() -> float:
    """当前时间。抽成函数以便测试注入 —— 直接调 `time.time()` 会让 in-flight 判定不可测。"""

    import time

    return time.time()


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
    cells = completed = failed = in_flight = 0
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
                # 「目录已建但产物未落」有两种成因，**不可混为一谈**：
                #
                #   进行中  —— 该格正在跑，产物还没写
                #   失败    —— 该格已放弃（启动器耗尽重试，或运行被杀）
                #
                # 首版一律计入 `failed`，于是**对进行中的运行会误报**：v24 跑到 38/66 时该字段报
                # `failed: 8`，而那 8 格正在跑。把它写进报告就是把在飞的格报成失败。
                #
                # 判据用「该代次目录下是否还有活进程」不可靠（本工具可能在别的机器上跑），改用
                # **文件新近度**：格目录下有文件在 `_IN_FLIGHT_WINDOW` 内被改过 → 进行中。
                newest = max(
                    (f.stat().st_mtime for f in cell.rglob("*") if f.is_file()),
                    default=0.0,
                )
                if newest and (_now() - newest) < _IN_FLIGHT_WINDOW:
                    in_flight += 1
                else:
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
        "in_flight": in_flight,
        "arms": sorted(arms),
        "coverage": dict(coverage),
        **{k: totals[k] for k in
           ("issues", "excluded_findings", "excluded_observations", "coverage_gaps")},
    }


def _order(name: str) -> tuple:
    """按版本号排，不按字典序 —— 否则 `v10` 排在 `v2` 前面。"""

    match = re.search(r"v(\d+)", name)
    return (0 if match else 1, int(match.group(1)) if match else 0, name)


#: 判定表的两种文件名。首版只认 `_as_published`，于是 `v22_manual.json` 静默返回 `—` ——
#: 当前代次的命中率从历代对比表里消失，而读者只会看到一个破折号。**有数据时出现的静默「无数据」
#: 比缺数据更坏**，所以这里枚举全部已用过的命名，并在找不到时区分「没有判定表」与「有但读不了」。
_VERDICT_SUFFIXES = ("_as_published", "_manual")


def _verdict_paths(generation: str) -> list[pathlib.Path]:
    stem = generation.replace("matrix-", "")
    return [HERE / "verdicts" / f"{stem}{sfx}.json" for sfx in _VERDICT_SUFFIXES]


def _ratio_over(verdicts: dict, ids) -> tuple[str, int]:
    import metrics_at_k as mk

    hits = triples = 0
    for record_id in ids:
        for series in mk._arms(verdicts.get(record_id, {})).values():
            valid = [x for x in series if x is not None]
            hits += sum(valid)
            triples += len(valid)
    if not triples:
        return "—", 0
    return f"{hits}/{triples} = {hits / triples * 100:.1f}%", triples


def _verdict_ratio(generation: str) -> tuple[str, str]:
    """该代次能力主张带的 hit@1，**两个分母都给**。

    返回 `(按当前可报集重算, 按该代次发布时的可报集)`。

    为什么必须两列：只遍历当前 `mk.REPORTABLE` 时，历史代次的数字会随烧毁而变，而且是**抬高
    方向** —— 被烧的记录若在那一代次恰为未命中，去掉它就等于去掉一个分母里的 0。实测：

        v21   发布时 4/9 = 44.4%   →  按当前 2 条重算 3/6 = 50.0%   (+5.6)
        v22   发布时 9/18 = 50.0%  →  按当前 2 条重算 8/12 = 66.7%  (+16.7)

    **后一行是本工具存在的全部理由。** 拿新代次的「当前口径」数字去比 v22 的「发布口径」50.0%，
    会凭空得出一个 16.7 点的改进 —— 那个改进完全来自分母变化，与方法无关。v23 的正确对照基线
    是 66.7%，不是 50.0%。`CLAUDE.md` §3.7 要求历代对比标注口径差异，这就是那条要求的具体形态；
    §3.5 条款 4 禁止的「评测口径迁就结果」在这里的形态是**沉默地换分母**，而不是显式改判据。
    """

    for path in _verdict_paths(generation):
        if not path.is_file():
            continue
        try:
            payload = json.loads(path.read_text())
        except (OSError, ValueError) as exc:
            # 有文件却读不了，不能与「没有判定表」共用一个破折号。
            return f"⚠️ 判定表不可读（{type(exc).__name__}）", "⚠️"
        verdicts = payload.get("verdicts") or {}
        import metrics_at_k as mk

        now, _ = _ratio_over(verdicts, mk.REPORTABLE)
        # 第二列必须是**该代次发布时**的可报集，不是判定表的全体记录 —— 后者含烧毁带与历史格，
        # 算出来是另一个带的数字而表头写着能力主张带。判定表若没记下当时的可报集，就说没记，
        # 不用「遍历全部键」去近似它。
        own_ids = payload.get("reportable_records_at_publication")
        if not own_ids:
            return now, "⚠️ 该代次未记录当时的可报集"
        missing = [r for r in own_ids if r not in verdicts]
        if missing:
            return now, f"⚠️ 声明的可报集有 {len(missing)} 条不在判定表内"
        own, _ = _ratio_over(verdicts, own_ids)
        return now, own
    return "—", "—"


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
              "| gaps | hit@1（当前 2 条可报集重算） | hit@1（该代次发布时的可报集） |")
        print("| --- | --: | --: | --: | --- | --- | --: | --: | --: | --: | --- | --- |")
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
                f"| {row['coverage_gaps']} | {' | '.join(_verdict_ratio(row['generation']))} |"
            )
        skipped = {r["generation"]: r["skipped_dirs"] for r in rows if r.get("skipped_dirs")}
        if skipped:
            print(f"\n跳过的非轮次目录：{skipped}")
        print("\n⚠️ **命中率只有判定表已入库的代次才有。** 更早代次的判定只存在于各自的 PR "
              "comment 里，而判定口径在这些代次之间变过（见 `docs/protocol/hit_criterion.md` §6），"
              "把它们并排放等于把不同口径的数字放在一列。")
    else:
        for row in rows:
            print(json.dumps(row, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
