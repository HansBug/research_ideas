"""The pair grid a generation runs, read from disk rather than typed.

Written after the same mistake twice in one round: a measurement script carried the grid as a
literal and had `0058` in it, which has never been in the grid, while `0000` was missing. The
number it produced (22 affected scopes, actually 16) went into a pre-registration document. A
grid that is typed is a second source of a fact that already exists in two places on disk.

Precedence:
  1. `--grid` on the command line, for a generation that deliberately changes the set.
  2. The most recent `runs/paper1/matrix-*/run1/` directory listing, which is what a generation
     actually ran -- the only unfalsifiable record of it.
  3. `holdout.json`'s `run_pairs` union its `holdout`, which is what the frozen bookkeeping
     says is in play.

Deliberately no hardcoded fallback. A checkout with neither runs nor a frozen hold-out cannot
know the grid, and guessing is how the wrong number gets into a document that claims to be
pre-registered.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
RUNS = REPO / "runs" / "paper1"

_CELL = re.compile(r"^(\d{4})-(claude|gpt)$")


def from_runs(generation: str | None = None) -> list[str]:
    """Pairs that a generation's `run1/` actually contains. Newest generation if unspecified."""

    if not RUNS.is_dir():
        return []
    candidates = sorted(
        (d for d in RUNS.glob("matrix-*") if (d / "run1").is_dir()),
        key=lambda d: d.stat().st_mtime,
        reverse=True,
    )
    if generation:
        candidates = [d for d in candidates if d.name == generation or d.name.endswith(generation)]
    for directory in candidates:
        pairs = set()
        for cell in (directory / "run1").iterdir():
            match = _CELL.match(cell.name)
            if match and cell.is_dir():
                pairs.add(match.group(1))
        if pairs:
            return sorted(pairs)
    return []


def from_frozen() -> list[str]:
    """`run_pairs` union `holdout`: what the frozen bookkeeping says is in play."""

    path = HERE / "holdout.json"
    if not path.is_file():
        return []
    frozen = json.loads(path.read_text())
    return sorted(set(frozen.get("run_pairs") or ()) | set(frozen.get("holdout") or ()))


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
) -> list[str]:
    """The grid, by the precedence in the module docstring. Raises rather than guessing.

    `apply_scope=False` 返回未筛选的原始格集，只用于复算历史代次的数字。
    """

    if explicit:
        pairs = sorted({p.strip() for p in re.split(r"[,\s]+", explicit) if p.strip()})
        if pairs:
            return in_scope(pairs) if apply_scope else pairs
    for source in (lambda: from_runs(generation), from_frozen):
        pairs = source()
        if pairs:
            return in_scope(pairs) if apply_scope else pairs
    raise SystemExit(
        "cannot determine the grid: no `runs/paper1/matrix-*/run1/` and no `holdout.json`. "
        "Pass it with `--grid` and say in the report where it came from."
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--grid")
    parser.add_argument("--generation", help="e.g. matrix-v21")
    parser.add_argument("--source", action="store_true", help="print where it came from")
    parser.add_argument("--all", action="store_true", help="不做建模对象筛选，用于复算历史代次")
    args = parser.parse_args()
    pairs = grid(args.grid, args.generation, apply_scope=not args.all)
    if args.source:
        # ⚠️ 与来源比对必须用**未筛选**的格集：筛选后 `pairs` 与 `from_runs()` 不再逐字相等，
        # 直接比会把 runs 来源误标成 holdout.json，而来源标注是报告里说明数字出处的那一行。
        raw = grid(args.grid, args.generation, apply_scope=False)
        origin = (
            "--grid"
            if args.grid
            else ("runs" if from_runs(args.generation) == raw else "holdout.json")
        )
        if not args.all:
            origin += "（已过建模对象筛选）"
        print(f"{len(pairs)} pairs from {origin}: {' '.join(pairs)}")
    else:
        print(" ".join(pairs))
