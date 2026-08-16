"""代次对比：只比交集，只用 A 层。

两个失效形态：

1. **分母不同却直接比百分比。** 一个代次 48 格、另一个 25 格（还在跑），或两者格集根本不同。
   本模块只取交集，并把交集大小打在最前面。
2. **把判定者的学习当成方法变好。** 人工判定跨代次不可比 —— v35 那两处作用域误判正是在第二次
   复核时才发现的，而那个学习会被误读成方法进步。所以只用确定性的 A 层。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

MATRIX = Path(__file__).resolve().parent.parent / "discover_matrix"
if str(MATRIX) not in sys.path:
    sys.path.insert(0, str(MATRIX))

import generation_diff as G  # noqa: E402
import verdict_tiers as V  # noqa: E402


def _write_cell(root: Path, run: str, pair: str, arm: str, issues: int) -> None:
    directory = root / run / f"{pair}-{arm}"
    directory.mkdir(parents=True)
    (directory / "discover-completed.json").write_text(
        json.dumps({"issues": [{"assertion_ids": []} for _ in range(issues)]})
    )


@pytest.fixture
def runs(tmp_path, monkeypatch):
    monkeypatch.setattr(V, "RUNS", tmp_path)
    return tmp_path


def test_only_the_intersection_is_compared(runs) -> None:
    """⭐ base 有 3 格、head 有 2 格 —— 只能比那 2 格。"""

    for pair in ("0000", "0006", "0029"):
        _write_cell(runs / "matrix-a", "run1", pair, "claude", issues=1)
    for pair in ("0000", "0006"):
        _write_cell(runs / "matrix-b", "run1", pair, "claude", issues=2)
    result = G.compare("matrix-a", "matrix-b")
    assert result["cells_in_base"] == 3
    assert result["cells_in_head"] == 2
    assert result["cells_compared"] == 2
    assert result["pairs_compared"] == ["0000", "0006"]
    # 只数交集里的 issue：base 2 个格 × 1 = 2，head 2 个格 × 2 = 4
    assert result["published_issues"] == {"base": 2, "head": 4}


def test_the_compared_count_is_stated_up_front(runs) -> None:
    for name, count in (("matrix-a", 1), ("matrix-b", 2)):
        for pair in ("0000", "0006")[:count]:
            _write_cell(runs / name, "run1", pair, "claude", issues=0)
    text = G.render(G.compare("matrix-a", "matrix-b"))
    assert "只比两边都已完成的 1 格" in text
    assert "方向性证据而不是效应量" in text


def test_an_empty_intersection_refuses(runs) -> None:
    """⭐ 一份看起来正常的空对比会被读成「两代次没有差别」。"""

    _write_cell(runs / "matrix-a", "run1", "0000", "claude", issues=0)
    _write_cell(runs / "matrix-b", "run1", "0006", "claude", issues=0)
    with pytest.raises(SystemExit, match="没有共同已完成的格"):
        G.compare("matrix-a", "matrix-b")


def test_a_missing_generation_refuses(runs) -> None:
    _write_cell(runs / "matrix-a", "run1", "0000", "claude", issues=0)
    with pytest.raises(SystemExit, match="代次目录不存在"):
        G.compare("matrix-a", "matrix-nope")


def test_no_movement_is_stated_rather_than_left_blank(runs) -> None:
    for name in ("matrix-a", "matrix-b"):
        _write_cell(runs / name, "run1", "0000", "claude", issues=0)
    text = G.render(G.compare("matrix-a", "matrix-b"))
    assert "A 层逐记录无变动" in text
