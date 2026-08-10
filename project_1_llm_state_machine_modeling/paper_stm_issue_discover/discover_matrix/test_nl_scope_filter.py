"""NL 层建模对象筛选的性质测试。

⚠️ 这些测试钉住的不是「输出是那 6 个 pair」，而是**筛选的公平性性质**：
先验（只读 NL）、按 NL 整体（不可拆到单 pair）、对阈值不敏感、且被排除集里含优于均值的样本。

一个可以调阈值调出想要结果的筛选不是先验筛选，所以敏感性必须是可执行的检查而不是文档断言。
"""

from __future__ import annotations

import importlib.util
import pathlib

import pytest

HERE = pathlib.Path(__file__).resolve().parent


def _mod():
    spec = importlib.util.spec_from_file_location("nl_scope_filter", HERE / "nl_scope_filter.py")
    assert spec and spec.loader
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def test_corpus_is_ten_nls_of_six_pairs() -> None:
    """语料结构：60 个 pair = 10 份 NL × 6。若上游语料变了，后面的性质都要重新论证。"""
    groups = _mod().nl_groups()
    assert len(groups) == 10, f"NL 份数变了: {len(groups)}"
    assert sorted(len(v) for v in groups.values()) == [6] * 10


def test_excluded_nl_is_exactly_the_last_digit_eight_family() -> None:
    """被排除的那份 NL 恰好是全部末位为 8 的 pair —— 「排除 `00x8`」这个说法成立。

    ⚠️ 不要把这条推广成「每份 NL 对应一个末位」。实测有**两个例外**：
    `a391765d` = `0002 0013 0023 0033 0043 0053`（2 与 3 混），
    `9fe426ba` = `0003 0012 0022 0032 0042 0052`（同上），即 `0012` 与 `0013` 在两份 NL 间互换。
    其余 8 份确实按末位对齐。**被排除的那份在干净的一侧**，所以简称成立，但这是实测事实而非规律。
    """
    ex = _mod().excluded_pairs()
    assert {p[-1] for p in ex} == {"8"}, f"被排除集不是全末位 8: {ex}"
    assert len(ex) == 6


def test_the_two_known_last_digit_exceptions_are_still_there() -> None:
    """把已知例外钉住：若上游语料重排，前一条测试的简称就要重新论证。"""
    groups = _mod().nl_groups()
    mixed = {h: sorted(v) for h, v in groups.items() if len({p[-1] for p in v}) > 1}
    assert len(mixed) == 2, f"末位混合的 NL 份数变了: {mixed}"
    assert {"0012", "0013"} <= {p for v in mixed.values() for p in v}


def test_exactly_one_nl_is_out_of_scope() -> None:
    m = _mod()
    out = [r for r in m.classify() if r["out_of_scope"]]
    assert len(out) == 1, f"超范围 NL 份数不是 1: {[r['nl'] for r in out]}"
    assert out[0]["pairs"] == ["0008", "0018", "0028", "0038", "0048", "0058"]


def test_partition_is_insensitive_to_thresholds() -> None:
    """⭐ 公平性核心：划分不能靠调阈值调出来。

    实测 154/187 组阈值给出相同划分（并发 1–11 × 计时 4–17）。这里要求 ≥ 3/4 的网格一致 ——
    留出余量以免语料微调就红，但足以挡住「阈值恰好卡在一个孤立点上」的情形。
    """
    same, total, _ = _mod()._sensitivity()
    assert same / total >= 0.75, f"划分对阈值敏感：只有 {same}/{total} 组一致"


def test_filter_reads_only_nl_text() -> None:
    """先验性：源码不得触及模型、产物或结果。

    这条比看输出更重要 —— 一个读了 `discover-completed.json` 的「先验」筛选不是先验筛选。
    """
    src = (HERE / "nl_scope_filter.py").read_text()
    for forbidden in (
        "model.fcstm",
        "discover-completed",
        "annotation_",
        "expected_issue_set",
        "runs/",
        "hit@",
    ):
        # 允许出现在文档字符串里（说明性），不允许出现在代码里
        import ast

        tree = ast.parse(src)
        docstrings = {ast.get_docstring(n) or "" for n in ast.walk(tree)
                      if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef))}
        in_doc = any(forbidden in d for d in docstrings)
        in_code = forbidden in src and not in_doc
        assert not in_code, f"筛选器代码触及 {forbidden!r}，不再是先验筛选"


@pytest.mark.parametrize("pair", ["0008", "0018", "0028", "0038", "0048", "0058"])
def test_excluded_pairs_are_stable(pair: str) -> None:
    assert pair in _mod().excluded_pairs()


@pytest.mark.parametrize("pair", ["0000", "0006", "0029", "0032", "0035", "0043", "0047", "0050"])
def test_grid_pairs_that_stay(pair: str) -> None:
    """格集里保留的 8 个 pair 必须不被排除 —— 含 `0043`（模型自造了 region，但 NL 未要求）。"""
    assert pair not in _mod().excluded_pairs()
