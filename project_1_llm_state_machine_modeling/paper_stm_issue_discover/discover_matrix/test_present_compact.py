"""`--compact` 只许去掉重复，不许去掉「四种没发现」的计数。

本脚本存在的唯一理由是：`issues` 为空与「发现了但被排除 / 被门丢弃 / 预算耗尽」在判定者眼里
长得一样，而根因和修法截然不同。compact 是为 324 格全量判定加的（默认模式下台账在同一 pair 内
被重复打印 6 遍，48 个 pair 约 8500 行），但它**必须保留那几行计数标题** —— 省掉它们，
这个脚本就退化成了它自己要防的东西。
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE / "present_for_judgment.py"


def _run(*args: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True, text=True, cwd=HERE,
    )
    return proc.stdout


@pytest.fixture(scope="module")
def has_v37() -> bool:
    root = HERE.parents[2] / "runs" / "paper1" / "matrix-v37"
    return root.is_dir()


def test_compact_keeps_every_not_found_category(has_v37: bool) -> None:
    if not has_v37:
        pytest.skip("本机没有 matrix-v37 产物")
    full = _run("v37", "--pair", "0014", "--full")
    compact = _run("v37", "--pair", "0014", "--compact", "--full")
    for label in ("被排除的发现", "被排除的观察", "自报覆盖缺口",
                  "被结构门丢弃的发现", "被判无支撑而丢弃的 issue"):
        # 只要默认模式印了某一类，compact 也必须印它的标题与计数。
        if label in full:
            assert label in compact, f"compact 丢掉了「{label}」这一类"


def test_compact_prints_the_ledger_once_per_pair(has_v37: bool) -> None:
    if not has_v37:
        pytest.skip("本机没有 matrix-v37 产物")
    compact = _run("v37", "--pair", "0014", "--compact", "--full")
    assert compact.count("-- 台账期望（可判定） --") == 1
    assert compact.count("-- 台账期望：见本 pair 首格 --") >= 1


def test_compact_keeps_every_cell_and_every_issue_title(has_v37: bool) -> None:
    """省的是描述与重复台账，不是格，也不是标题。"""

    if not has_v37:
        pytest.skip("本机没有 matrix-v37 产物")
    full = _run("v37", "--pair", "0014", "--full")
    compact = _run("v37", "--pair", "0014", "--compact", "--full")
    assert full.count("coverage=") == compact.count("coverage=")
    # issue 标题行形如 "   [1] xxx"；两种模式必须一样多。
    count = lambda s: sum(1 for l in s.splitlines() if l.lstrip().startswith("["))
    assert count(full) == count(compact)


def test_compact_is_actually_shorter(has_v37: bool) -> None:
    if not has_v37:
        pytest.skip("本机没有 matrix-v37 产物")
    full = _run("v37", "--pair", "0014", "--full").count("\n")
    compact = _run("v37", "--pair", "0014", "--compact", "--full").count("\n")
    assert compact < full * 0.75, f"compact={compact} full={full}，没省下多少就不值得多一个模式"
