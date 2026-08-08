"""The pair grid a generation runs, read from disk rather than typed.

Written after the same mistake twice in one round: a measurement script carried the grid as a
literal and had `0058` in it, which has never been in the grid, while `0000` was missing. The
number it produced (22 affected scopes, actually 16) went into a pre-registration document. A
grid that is typed is a second source of a fact that already exists in two places on disk.

Precedence:
  1. `--corpus` on the command line, for the full-corpus run: every pair the corpus has, minus
     the ones the a-priori NL scope filter excludes.
  2. `--grid` on the command line, for a generation that deliberately changes the set.
  3. The most recent `runs/paper1/matrix-*/run1/` directory listing, which is what a generation
     actually ran -- the only unfalsifiable record of it.
  （曾有第 4 项 `holdout.json`。hold-out 机制已于 2026-08-09 永久移除 —— 方法在这批 pair 上
   迭代，不再区分留出与非留出，格集只能来自命令行或运行目录。）

Deliberately no hardcoded fallback. A checkout with no runs cannot
know the grid, and guessing is how the wrong number gets into a document that claims to be
pre-registered.

⚠️ `--corpus` is **explicit and never automatic**, even though it is the widest source. The
automatic chain answers "what did a generation run", and its answer has to stay falsifiable
against the run directories. Putting the corpus in that chain would make a checkout with no runs
silently claim the full corpus was the grid -- the same failure the module was written to prevent,
one level up. A full-corpus run is a decision, so it is typed once on the command line and
recorded by `--source`.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"
P1 = REPO / "project_1_llm_state_machine_modeling"
#: 语料的权威 pair 目录 —— 每个 pair 一个子目录，内含 `nl.txt` 与 `fcstm.fcstm`。
CORPUS = P1 / "paper_stm_repair/pipeline/representation/reports/llms_emp_r45_java_60/pairs"
#: 流水线实际读的输入。`--pair-id llms_emp_feedback_final_XXXX` 解析到这里。
SEEDS = P1 / "paper_stm_repair/selected_seed_examples"

_CELL = re.compile(r"^(\d{4})-(claude|gpt)$")
_PAIR = re.compile(r"^\d{4}$")


def from_corpus() -> list[str]:
    """语料里的全部 pair，且**必须同时有种子模型**。

    两个目录都要查，不是多余：`CORPUS` 决定「语料里有哪些 pair」，`SEEDS` 决定「流水线能不能读到
    它」。少了后一半，一个只在语料里、没有种子模型的 pair 会进入格集，然后在开跑几小时后逐格失败 ——
    而那时分母已经写进报告了。宁可在启动前就少列出它并说明。

    实测（2026-08-08）：语料 60 个，种子模型 60 个，两者完全重合，所以这层检查当前不减少任何 pair；
    它防的是后续语料扩充时两边不同步。
    """

    if not CORPUS.is_dir():
        return []
    pairs = {d.name for d in CORPUS.iterdir() if d.is_dir() and _PAIR.match(d.name)}
    if SEEDS.is_dir():
        seeded = {d.name[-4:] for d in SEEDS.glob("llms_emp_feedback_final_*") if d.is_dir()}
        pairs &= seeded
    return sorted(pairs)


#: 启动器在开跑前写下的格集。见 `from_runs` 的警告。
GRID_FILE = "GRID.txt"


def from_runs(generation: str | None = None) -> list[str]:
    """A generation's grid: its `GRID.txt` if it has one, else what `run1/` contains.

    ⚠️ **目录清点只在运行结束后才等于格集。** 实测（2026-08-08）：v36 开跑约 30 秒后无参调用返回
    4 个 pair 而不是 8 —— 目录是逐格创建的，而本函数按 mtime 取最近的代次，于是正在跑的那个
    代次给出一个残缺格集，且看起来完全正常。跑 324 格时这个窗口有 9 到 11 小时，任何在运行期
    做测量的脚本都会拿到错的分母。

    所以启动器在开跑**前**把格集写进 `GRID.txt`，本函数优先读它：格集从此是一份记录，而不是
    从逐格产物反推出来的推断。清点保留为旧代次的回退 —— 它们没有这份文件，删掉会让历史数字
    无法复算。
    """

    if not RUNS.is_dir():
        return []
    candidates = sorted(
        (d for d in RUNS.glob("matrix-*") if (d / "run1").is_dir() or (d / GRID_FILE).is_file()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if generation:
        candidates = [d for d in candidates if d.name == generation or d.name.endswith(generation)]
    for directory in candidates:
        declared = directory / GRID_FILE
        if declared.is_file():
            pairs = {
                token
                for token in re.split(r"[,\s]+", declared.read_text())
                if _PAIR.match(token)
            }
            if pairs:
                return sorted(pairs)
        if not (directory / "run1").is_dir():
            continue
        pairs = set()
        for cell in (directory / "run1").iterdir():
            match = _CELL.match(cell.name)
            if match and cell.is_dir():
                pairs.add(match.group(1))
        if pairs:
            return sorted(pairs)
    return []


def in_scope(pairs: list[str]) -> list[str]:
    """去掉建模对象之外的 pair（见 `nl_scope_filter.py`）。

    ⚠️ 为什么筛选放在这里、而不是改一个常量：本模块的全部设计前提是「格集从盘上读，不手敲」——
    历史来源（`runs/paper1/matrix-*/run1/`）都是**筛选之前**的运行，它们永远会带着
    `0018` / `0038` / `0048`。若只在文档里写「已排除」而这里不筛，下一次全量运行会照旧跑 11 个 pair，
    而报告按 8 个 pair 的分母去算 —— 分子分母出自不同格集，是最不容易被发现的口径错误。

    筛选本身仍是**先验**的：`nl_scope_filter` 只读 `nl.txt`，不看任何结果。
    """

    try:
        from nl_scope_filter import excluded_pairs
    except ImportError:  # 以脚本方式跑时同目录导入
        import sys

        sys.path.insert(0, str(HERE))
        from nl_scope_filter import excluded_pairs
    banned = set(excluded_pairs())
    return [p for p in pairs if p not in banned]


def grid(
    explicit: str | None = None,
    generation: str | None = None,
    apply_scope: bool = True,
    corpus: bool = False,
) -> list[str]:
    """The grid, by the precedence in the module docstring. Raises rather than guessing.

    `apply_scope=False` 返回未筛选的原始格集，只用于复算历史代次的数字。
    `corpus=True` 取全语料 —— 显式来源，见模块 docstring 的警告。
    """

    if corpus:
        pairs = from_corpus()
        if not pairs:
            raise SystemExit(
                f"--corpus 但语料目录不可用或为空：{CORPUS}。不猜格集。"
            )
        return in_scope(pairs) if apply_scope else pairs
    if explicit:
        pairs = sorted({p.strip() for p in re.split(r"[,\s]+", explicit) if p.strip()})
        if pairs:
            return in_scope(pairs) if apply_scope else pairs
    for source in (lambda: from_runs(generation),):
        pairs = source()
        if pairs:
            return in_scope(pairs) if apply_scope else pairs
    raise SystemExit(
        "cannot determine the grid: no `runs/paper1/matrix-*/run1/`. "
        "Pass it with `--grid` or `--corpus` and say in the report where it came from."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid")
    parser.add_argument("--generation", help="e.g. matrix-v21")
    parser.add_argument("--source", action="store_true", help="print where it came from")
    parser.add_argument("--all", action="store_true", help="不做建模对象筛选，用于复算历史代次")
    parser.add_argument(
        "--corpus",
        action="store_true",
        help="全语料格集（显式来源；不进自动优先级，见模块 docstring）",
    )
    args = parser.parse_args()
    pairs = grid(args.grid, args.generation, apply_scope=not args.all, corpus=args.corpus)
    if args.source:
        # ⚠️ 与来源比对必须用**未筛选**的格集：筛选后 `pairs` 与 `from_runs()` 不再逐字相等。
        raw = grid(args.grid, args.generation, apply_scope=False, corpus=args.corpus)
        if args.corpus:
            origin = f"corpus（{CORPUS.name} 下 {len(raw)} 个 pair，且均有种子模型）"
        elif args.grid:
            origin = "--grid"
        else:
            origin = "runs"
        if not args.all:
            origin += "（已过建模对象筛选）"
        print(f"{len(pairs)} pairs from {origin}: {' '.join(pairs)}")
    else:
        print(" ".join(pairs))
