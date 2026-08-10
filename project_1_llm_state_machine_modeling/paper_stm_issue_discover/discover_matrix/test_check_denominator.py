"""分母核对：缺的位计为未命中，不得从分母剔除。

v33 的单 pair 诊断里，一轮崩掉没落盘，我用「已落盘轮」当分母报成 `2/2` 而不是 `2/3` ——
把丢格从分母里悄悄去掉，于是一个越容易崩的改动看起来越好。用户当场指出「为什么分母变成 2 了」。

这类错误看起来完全正常：88 位的覆盖率与 99 位的覆盖率在报告里长得一样，只有分母那一行会露出来，
而那一行最容易被写成「记录数 × 6」的推算值而非实测值。所以分母不推算，逐记录数。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

MATRIX = Path(__file__).resolve().parent.parent / "discover_matrix"
if str(MATRIX) not in sys.path:
    sys.path.insert(0, str(MATRIX))

import check_denominator as C  # noqa: E402
import verdict_tiers as V  # noqa: E402


@pytest.fixture
def runs(tmp_path, monkeypatch):
    monkeypatch.setattr(V, "RUNS", tmp_path)
    return tmp_path


def _cell(base: Path, run: str, pair: str, arm: str) -> None:
    d = base / run / f"{pair}-{arm}"
    d.mkdir(parents=True)
    (d / "discover-completed.json").write_text("{}")


def _generation(base: Path, pairs: list[str], skip: set[tuple[str, str, str]] = frozenset()):
    (base / "GRID.txt").write_text(" ".join(pairs) + "\n")
    for r in (1, 2, 3):
        for p in pairs:
            for arm in ("claude", "gpt"):
                if (f"run{r}", p, arm) in skip:
                    continue
                _cell(base, f"run{r}", p, arm)


def _real_pair() -> str:
    """取一个台账里真有 in_scope 记录的 pair，否则可判定记录数为 0、测试空过。"""

    for record in V.ledger_claims().values():
        if record["in_scope"]:
            return record["pair"]
    pytest.skip("台账里没有 in_scope 记录")


def test_a_complete_generation_passes(runs) -> None:
    base = runs / "matrix-ok"
    base.mkdir()
    _generation(base, [_real_pair()])
    result = C.check(base)
    assert result["records_incomplete"] == {}
    assert result["positions_landed"] == result["positions_expected"]
    assert "分母可用" in C.render(result)


def test_a_missing_cell_is_named_and_counted_against_the_denominator(runs) -> None:
    """⭐ 这是 v33 那个错误的形状：缺的位必须出现在报告里，且分母不变。"""

    pair = _real_pair()
    base = runs / "matrix-hole"
    base.mkdir()
    _generation(base, [pair], skip={("run2", pair, "gpt")})
    result = C.check(base)
    assert result["records_incomplete"], "缺位必须被报出来"
    assert result["positions_expected"] % 6 == 0
    assert result["positions_landed"] < result["positions_expected"]
    text = C.render(result)
    assert f"run2/{pair}-gpt" in text
    assert "不得从分母剔除" in text


def test_the_exit_code_blocks_the_pipeline(runs) -> None:
    """⭐ 非零退出是它作为流程闸的全部作用 —— 报了却放行等于没报。"""

    pair = _real_pair()
    base = runs / "matrix-hole2"
    base.mkdir()
    _generation(base, [pair], skip={("run1", pair, "claude")})
    assert C.main(["--base", str(base)]) == 1

    ok = runs / "matrix-ok2"
    ok.mkdir()
    _generation(ok, [pair])
    assert C.main(["--base", str(ok)]) == 0


def test_grid_mismatch_is_reported(runs) -> None:
    """`GRID.txt` 声明了 pair 但一格都没落盘 —— 整个 pair 缺失最容易被漏看。"""

    pair = _real_pair()
    base = runs / "matrix-gridmiss"
    base.mkdir()
    (base / "GRID.txt").write_text(f"{pair} 9999\n")
    for r in (1, 2, 3):
        for arm in ("claude", "gpt"):
            _cell(base, f"run{r}", pair, arm)
    result = C.check(base)
    assert result["grid_matches"] is False
    assert "9999" in C.render(result)
    assert C.main(["--base", str(base)]) == 1


def test_pairs_without_judgeable_records_are_listed_not_silently_dropped(runs) -> None:
    """零可判定记录的 pair 必须被点出来 —— 它们只进精度侧，不产生召回分母。"""

    pair = _real_pair()
    base = runs / "matrix-zero"
    base.mkdir()
    # `_generation` 已经为两个 pair 都建了格，不要再建一遍 —— 首版重复建目录、FileExistsError。
    _generation(base, [pair, "9998"])
    result = C.check(base)
    assert "9998" in result["pairs_with_no_judgeable_record"]
    assert "只进精度侧" in C.render(result)


def test_a_missing_grid_file_falls_back_to_what_landed(runs) -> None:
    pair = _real_pair()
    base = runs / "matrix-nogrid"
    base.mkdir()
    for r in (1, 2, 3):
        for arm in ("claude", "gpt"):
            _cell(base, f"run{r}", pair, arm)
    result = C.check(base)
    assert result["grid_declared"] == []
    assert result["grid_matches"] is True
    assert result["records_incomplete"] == {}
