"""格集来源：语料模式是显式的，运行期不得给出残缺格集。

## 这套测试钉的是什么

两件事，第二件是实测抓到的活缺陷：

1. **`--corpus` 不进自动优先级。** 它是最宽的来源，若进了自动链，一个没有 `runs/` 的 checkout 会
   静默宣称全语料就是格集 —— 与 `run_grid` 整个模块要防的失败同型，只是高一层。

2. **运行期的目录清点不等于格集。** 实测（2026-08-08）：v36 开跑约 30 秒后无参调用返回 4 个 pair
   而不是 8 —— 目录是逐格创建的，而 `from_runs` 按 mtime 取最近代次，于是**正在跑**的代次给出一个
   残缺格集，且看起来完全正常。跑 324 格时这个窗口有 9 到 11 小时，任何运行期做测量的脚本都会
   拿到错的分母，而分母错是最不容易被发现的口径错误。

   修法是启动器在开跑**前**写 `GRID.txt`，`from_runs` 优先读它。下面第二组测试构造正在跑的形状
   （目录只有一部分 pair，但 `GRID.txt` 已写全）来钉住它。
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
# ⛔ 归档后脚本与测试同在 `scripts/`，原先的 `…/ "discover_matrix"` 指向不存在的目录。
MATRIX = HERE
if str(MATRIX) not in sys.path:
    sys.path.insert(0, str(MATRIX))

import run_grid  # noqa: E402


@pytest.fixture
def runs(tmp_path, monkeypatch):
    """把 `RUNS` 指到一棵临时树，避免读到真实的运行目录。"""

    root = tmp_path / "paper1"
    root.mkdir()
    monkeypatch.setattr(run_grid, "RUNS", root)
    return root


def _generation(root: Path, name: str, cells: list[str], grid: list[str] | None = None) -> Path:
    directory = root / name
    (directory / "run1").mkdir(parents=True)
    for pair in cells:
        for arm in ("claude", "gpt"):
            (directory / "run1" / f"{pair}-{arm}").mkdir()
    if grid is not None:
        (directory / run_grid.GRID_FILE).write_text(" ".join(grid) + "\n")
    return directory


# ---------------------------------------------------------------- 运行期残缺格集

def test_declared_grid_beats_a_partial_directory_listing(runs) -> None:
    """⭐ 这是那个活缺陷。目录只建了 2 个 pair，`GRID.txt` 说 8 个 —— 必须报 8 个。"""

    declared = ["0000", "0006", "0029", "0032", "0035", "0043", "0047", "0050"]
    _generation(runs, "matrix-v36", cells=["0000", "0006"], grid=declared)
    assert run_grid.from_runs() == declared


def test_directory_listing_remains_the_fallback_for_older_generations(runs) -> None:
    """旧代次没有这份文件 —— 删掉清点会让历史数字无法复算。"""

    _generation(runs, "matrix-v24", cells=["0000", "0029"], grid=None)
    assert run_grid.from_runs() == ["0000", "0029"]


def test_a_generation_with_only_a_grid_file_is_still_found(runs) -> None:
    """开跑瞬间：`GRID.txt` 已写，`run1/` 里还什么都没有。"""

    directory = runs / "matrix-v37"
    directory.mkdir()
    (directory / run_grid.GRID_FILE).write_text("0004 0013\n")
    assert run_grid.from_runs() == ["0004", "0013"]


def test_a_malformed_grid_file_falls_back_rather_than_returning_junk(runs) -> None:
    _generation(runs, "matrix-v38", cells=["0000"], grid=[])
    (runs / "matrix-v38" / run_grid.GRID_FILE).write_text("not a pair list\n")
    assert run_grid.from_runs() == ["0000"]


def test_grid_file_tolerates_commas_and_newlines(runs) -> None:
    directory = runs / "matrix-v39"
    directory.mkdir()
    (directory / run_grid.GRID_FILE).write_text("0000,0006\n0029\n")
    assert run_grid.from_runs() == ["0000", "0006", "0029"]


# ---------------------------------------------------------------- 语料模式

def test_corpus_is_never_reached_automatically(runs) -> None:
    """⭐ 负控：没有任何自动路径会返回全语料。

    没有 runs 时必须**抛错**而不是回落到语料 —— 猜格集正是本模块存在的理由。

    ⛔ 本测试原先打桩的是 `from_frozen`，⚠️ 那个函数已在 `f3ea403c`（永久移除 hold-out 机制）
    随 holdout 一起删掉，测试没跟着改，于是 `monkeypatch.setattr` 直接抛 `AttributeError`
    —— **负控从此没有真正跑过**。⭐ 现在打桩仍然存在的自动来源 `from_runs`，意图不变。
    """

    monkey = pytest.MonkeyPatch()
    monkey.setattr(run_grid, "from_runs", lambda generation=None: [])
    try:
        with pytest.raises(SystemExit):
            run_grid.grid()
    finally:
        monkey.undo()


def test_corpus_flag_returns_the_corpus_minus_the_scope_filter() -> None:
    """全语料 60，减掉 NL 范围筛选的 6 个 fork/join pair = 54。"""

    if not run_grid.CORPUS.is_dir():
        pytest.skip("语料目录不在此 checkout 中")
    raw = run_grid.grid(corpus=True, apply_scope=False)
    filtered = run_grid.grid(corpus=True)
    assert len(raw) == 60, raw
    assert len(filtered) == 54, filtered
    assert set(raw) - set(filtered) == {"0008", "0018", "0028", "0038", "0048", "0058"}


def test_corpus_requires_a_seed_model_for_every_pair(tmp_path, monkeypatch) -> None:
    """⭐ 语料里有、但流水线读不到的 pair 不得进格集。

    少了这层，它会在开跑几小时后逐格失败 —— 而那时分母已经写进报告了。
    """

    corpus = tmp_path / "pairs"
    seeds = tmp_path / "seeds"
    for pair in ("0001", "0002", "0003"):
        (corpus / pair).mkdir(parents=True)
    for pair in ("0001", "0003"):
        (seeds / f"llms_emp_feedback_final_{pair}").mkdir(parents=True)
    monkeypatch.setattr(run_grid, "CORPUS", corpus)
    monkeypatch.setattr(run_grid, "SEEDS", seeds)
    assert run_grid.from_corpus() == ["0001", "0003"]


def test_corpus_refuses_rather_than_returning_empty(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(run_grid, "CORPUS", tmp_path / "missing")
    with pytest.raises(SystemExit, match="不猜格集"):
        run_grid.grid(corpus=True)


def test_module_reloads_cleanly(runs) -> None:
    """⭐ 上面几条不是导入顺序的假象。"""

    importlib.reload(run_grid)
    assert hasattr(run_grid, "from_corpus")
    assert run_grid.GRID_FILE == "GRID.txt"
