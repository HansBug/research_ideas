"""转换器只许改形状，不许改分母。

锁三件事，每一件都对应本目录真实犯过的错：

1. **`null` 不是 `0`。** 「格没落盘」「位没判」与「判了但没命中」是三种不同的事实；
   把前两种写成 0 会让分母虚高而分子不变，无声压低命中率。
2. **轮数由实际目录算出。** 写死轮数会让缺轮静默变成 `null` 填充，读者分不清「没跑」和「没判」。
3. **`.tryN` 目录不是独立的格。** 启动器每次整格重试前把目录改名，把它们算成格会虚增分母 ——
   `degradation_audit.py` 已经栽过一次（v41 的「未落盘」从 2 虚报成 13）。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import audit_to_verdicts as A  # noqa: E402


def _land(root: pathlib.Path, cell: str) -> None:
    run, name = cell.split("/")
    target = root / run / name
    target.mkdir(parents=True, exist_ok=True)
    (target / "discover-completed.json").write_text(json.dumps({"issues": []}))


@pytest.fixture()
def generation(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    root = tmp_path / "matrix-t"
    for cell in (
        "run1/0030-claude", "run1/0030-gpt",
        "run2/0030-claude",                      # run2 的 gpt 没落盘
        "run3/0030-claude", "run3/0030-gpt",
    ):
        _land(root, cell)
    # 放弃的重试目录：有失败收据、无完成收据，不得成为独立的格。
    (root / "run2" / "0030-gpt.try1").mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(A, "RUNS", tmp_path)
    return tmp_path


def _audit(tmp_path: pathlib.Path, entries: list[tuple[str, str, bool]]) -> pathlib.Path:
    path = tmp_path / "audit.json"
    path.write_text(json.dumps({"audit": [
        {"record_id": r, "cell": c, "hit": h} for r, c, h in entries
    ]}))
    return path


def test_unlanded_cell_is_null_not_zero(generation: pathlib.Path) -> None:
    audit = _audit(generation, [
        ("EIS-0030-01", "run1/0030-claude", True),
        ("EIS-0030-01", "run1/0030-gpt", False),
        ("EIS-0030-01", "run2/0030-claude", True),
        ("EIS-0030-01", "run3/0030-claude", True),
        ("EIS-0030-01", "run3/0030-gpt", True),
    ])
    out = A.convert("matrix-t", audit)
    assert out["rounds"] == ["run1", "run2", "run3"]
    row = out["verdicts"]["EIS-0030-01"]
    assert row["claude"] == [1, 1, 1]
    # run2 的 gpt 格没落盘 —— 必须是 None，不是 0。
    assert row["gpt"] == [0, None, 1]


def test_a_landed_but_unjudged_position_is_null(generation: pathlib.Path) -> None:
    """落盘了却没判过，与判了没命中不是一回事。"""

    audit = _audit(generation, [("EIS-0030-01", "run1/0030-claude", True)])
    row = A.convert("matrix-t", audit)["verdicts"]["EIS-0030-01"]
    assert row["claude"] == [1, None, None]
    assert row["gpt"] == [None, None, None]


def test_try_directories_do_not_become_cells(generation: pathlib.Path) -> None:
    """`run2/0030-gpt.try1` 与 `run2/0030-gpt` 是同一格，且它没有完成收据。"""

    assert ("run2", "0030", "gpt") not in A.landed_cells("matrix-t")
    assert A.parse_cell("run2/0030-gpt.try1") == ("run2", "0030", "gpt")


def test_rounds_come_from_disk_not_a_constant(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """只跑了一轮时，位数必须是 1 轮的量，不能补成 3 轮的 null。"""

    root = tmp_path / "matrix-one"
    _land(root, "run1/0040-claude")
    monkeypatch.setattr(A, "RUNS", tmp_path)
    audit = _audit(tmp_path, [("EIS-0040-01", "run1/0040-claude", False)])
    out = A.convert("matrix-one", audit)
    assert out["rounds"] == ["run1"]
    assert out["verdicts"]["EIS-0040-01"]["claude"] == [0]
    assert out["verdicts"]["EIS-0040-01"]["gpt"] == [None]


def test_round_order_is_numeric_not_lexicographic(
    tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """run10 排在 run2 之后。字典序会把逐轮列错位，而错位后每个值单独看都合法。"""

    root = tmp_path / "matrix-ten"
    for run in ("run1", "run2", "run10"):
        _land(root, f"{run}/0040-claude")
    monkeypatch.setattr(A, "RUNS", tmp_path)
    audit = _audit(tmp_path, [("EIS-0040-01", "run10/0040-claude", True)])
    out = A.convert("matrix-ten", audit)
    assert out["rounds"] == ["run1", "run2", "run10"]
    assert out["verdicts"]["EIS-0040-01"]["claude"] == [None, None, 1]


def test_hit_values_are_carried_through_untouched(generation: pathlib.Path) -> None:
    """转换器不做判定：audit 说什么就是什么。"""

    audit = _audit(generation, [
        ("EIS-0030-02", "run1/0030-claude", False),
        ("EIS-0030-02", "run1/0030-gpt", True),
    ])
    row = A.convert("matrix-t", audit)["verdicts"]["EIS-0030-02"]
    assert row["claude"][0] == 0
    assert row["gpt"][0] == 1
