"""谓词统计的三条不变量。

这份统计会直接进报告，且两侧分母不同质、极易串味，所以把最容易出错的三件事各钉一条：
族归属必须来自谓词定义本身（不能在统计侧另写一份）、台账侧只数进入能力分母的记录、
表达式抽取不能把非谓词的函数名算进来。
"""

from __future__ import annotations

import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import predicate_usage as PU  # noqa: E402


def test_families_come_from_the_predicate_definition() -> None:
    """族归属只有一个真源。统计侧若自己维护一份，两边会悄悄漂移。"""

    family, order = PU._predicate_names()
    assert len(order) == 19, "闭合词表应为 19 个谓词"
    assert set(family.values()) == {"S", "B", "P"}
    assert set(PU._FAMILY_LABEL) == {"S", "B", "P"}, "标签表与谓词定义的族码必须对齐"


def test_ledger_side_counts_only_reportable_records() -> None:
    """台账侧的分母是能力分母（98 条），不是台账全量（126 条）。"""

    import metrics_at_k as mk

    family, order = PU._predicate_names()
    per_all, per_primary = PU.ledger_side(set(order))
    assert sum(per_primary.values()) <= sum(per_all.values())
    # 98 条可判记录带 86 条 primary 断言；primary 计数不应超过它。
    assert sum(per_primary.values()) == 86, "primary 断言数与台账构成表不一致"
    assert len(mk.REPORTABLE) == 98


@pytest.mark.parametrize(
    ("expression", "expected"),
    [
        ('state_declared(state="A", kind="leaf") is True', ["state_declared"]),
        # `is True` / `and` / 嵌套括号都不是谓词，不能被算进去
        ('reaches(source="A", target="B", steps=3) is False', ["reaches"]),
        # 未知函数名必须被丢弃，否则词表一变统计就虚高
        ('not_a_predicate(x=1)', []),
        ('', []),
    ],
)
def test_only_known_predicates_are_extracted(expression: str, expected: list[str]) -> None:
    _, order = PU._predicate_names()
    assert PU._predicates_in(expression, set(order)) == expected


def test_missing_run_directory_degrades_instead_of_raising(monkeypatch: pytest.MonkeyPatch) -> None:
    """运行目录不在时给零，不抛——统计脚本在没有 runs/ 的环境里也要能跑台账侧。"""

    monkeypatch.setattr(PU, "RUNS", HERE / "__no_such_dir__")
    _, order = PU._predicate_names()
    published, generated, cells, issues = PU.output_side(set(order))
    assert (cells, issues) == (0, 0)
    assert not published and not generated
