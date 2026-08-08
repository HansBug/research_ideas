"""`hit@all` 必须同时约束元数与谓词，不能只约束谓词。

v37 的 `run1/0057-gpt` 耗尽重试没落盘，`EIS-0057-01` 那个「记录 × 臂」单元只剩两轮，
两轮都命中。三处 `hit@all` 的实现都写成 `all(valid)`，而 `valid` 是丢掉 `None` 之后
的列表 —— 于是这个单元被计成「三轮全中」，`hit@all` 报成 73/198，真值是 72/198。

这个方向是错的：**缺测越多，数字越好看**。一个全部失败只剩一轮、那一轮恰好命中的单元
会被算作满分稳定。所以判据不能只问「我看到的都命中吗」，必须问「三轮都在且都命中吗」。

三处实现分别在 `metrics_at_k.report_band`、`build_comment._ratios`、
`blind_agreement._hit_at_k`，都改成显式接收 `rounds`。这里锁的是性质，不是某一处写法：
每个实现都喂同一份「两轮全中」的残缺单元，它都不得计入 `hit@all`。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import blind_agreement  # noqa: E402
import build_comment  # noqa: E402
import metrics_at_k as mk  # noqa: E402


def _ratio(text: str) -> tuple[int, int]:
    """`"2/3 = 66.7%"` -> `(2, 3)`。"""

    head = text.split("=")[0].strip()
    num, _, den = head.partition("/")
    return int(num), int(den)


@pytest.mark.parametrize(
    ("series", "expect_all"),
    [
        ([1, 1, 1], 1),  # 三轮齐全且全中 —— 唯一该计入的形状
        ([1, 1, None], 0),  # 两轮全中，第三轮缺测 —— v37 踩的那个
        ([1, None, None], 0),  # 只剩一轮且命中 —— 从单点断言稳定性
        ([1, 1, 0], 0),  # 三轮齐全但有未命中
    ],
    ids=["complete", "one-missing", "two-missing", "complete-with-miss"],
)
def test_build_comment_ratios_require_full_arity(series, expect_all) -> None:
    verdicts = {"EIS-0000-01": {"claude": list(series)}}
    ratios = build_comment._ratios(verdicts, ["EIS-0000-01"], rounds=3)
    assert _ratio(ratios["hit@all"]) == (expect_all, 1), ratios


@pytest.mark.parametrize(
    ("series", "expect_all"),
    [([1, 1, 1], 1), ([1, 1, None], 0), ([1, None, None], 0), ([1, 1, 0], 0)],
    ids=["complete", "one-missing", "two-missing", "complete-with-miss"],
)
def test_blind_agreement_hit_at_k_requires_full_arity(series, expect_all) -> None:
    ratios = blind_agreement._hit_at_k({"u": list(series)}, ["u"], rounds=3)
    assert _ratio(ratios["hit@all"]) == (expect_all, 1), ratios


@pytest.mark.parametrize(
    ("series", "expect_all"),
    [([1, 1, 1], 1), ([1, 1, None], 0), ([1, None, None], 0)],
    ids=["complete", "one-missing", "two-missing"],
)
def test_report_band_requires_full_arity(series, expect_all, capsys) -> None:
    """小样本时比率闸门不出百分比，所以断言它照常打印的原始计数行。"""

    mk.report_band({"EIS-0000-01": {"claude": list(series)}}, ["EIS-0000-01"],
                   "t", rounds=3)
    printed = capsys.readouterr().out.replace(" ", "")
    assert f"三轮全中{expect_all}/条目1" in printed, printed


def test_hit_at_1_and_hit_at_3_still_use_what_was_observed() -> None:
    """arity 守卫只加在 `hit@all` 上。

    `hit@1` 的分母是实际判定位，`hit@3` 问的是「三轮里至少一次」—— 缺测不改变
    「至少一次」的答案，只有「全部」会被缺测抬高。把守卫加到这两个上会把分母改错。
    """

    verdicts = {"EIS-0000-01": {"claude": [1, 1, None]}}
    ratios = build_comment._ratios(verdicts, ["EIS-0000-01"], rounds=3)
    assert _ratio(ratios["hit@1"]) == (2, 2)
    assert _ratio(ratios["hit@3"]) == (1, 1)
    assert _ratio(ratios["hit@all"]) == (0, 1)


def test_the_v37_shape_reproduces_the_corrected_number() -> None:
    """把 v37 那个单元的形状喂进去，`hit@all` 必须少算它。"""

    verdicts = {
        "EIS-0057-01": {"claude": [1, 1, 1], "gpt": [None, 1, 1]},
        "EIS-0000-01": {"claude": [0, 0, 0], "gpt": [0, 0, 0]},
    }
    ids = list(verdicts)
    ratios = build_comment._ratios(verdicts, ids, rounds=3)
    # 四个单元，只有 claude 那个是三轮齐全且全中。
    assert _ratio(ratios["hit@all"]) == (1, 4), ratios
    assert _ratio(ratios["hit@3"]) == (2, 4), ratios


def test_arity_guard_is_present_in_every_implementation() -> None:
    """三处实现都必须显式收 `rounds`，新增第四处也得收。"""

    import inspect

    for fn in (build_comment._ratios, blind_agreement._hit_at_k, mk.report_band):
        assert "rounds" in inspect.signature(fn).parameters, fn.__qualname__
        assert "len(" in inspect.getsource(fn), fn.__qualname__


def test_audit_json_on_disk_agrees_if_present() -> None:
    """有 v37 审计产物时，顺带核对 73/198 这个已发布的数。"""

    path = pathlib.Path("/tmp/v37_audit_324.json")
    if not path.exists():
        pytest.skip("v37 审计产物不在本机")
    import collections

    by_arm: dict[tuple[str, str], list[int]] = collections.defaultdict(list)
    for entry in json.loads(path.read_text())["audit"]:
        arm = entry["cell"].split("-")[-1]
        by_arm[(entry["record_id"], arm)].append(int(entry["hit"]))
    at_all = sum(1 for v in by_arm.values() if len(v) == 3 and all(v))
    assert (at_all, len(by_arm)) == (73, 198)
