"""「进行中」必须与「失败」分开计数。

## 为什么需要这条测试

`generation_history.py` 首版把「目录已建但 `discover-completed.json` 未落」一律计入 `failed`。这个 bug
**只在运行进行中才显形** —— 此前所有代次都是跑完才用该工具，所以它从未暴露。

实测：v24 跑到 39/66 时该字段报 `failed: 8`，而那 8 格正在跑。把它写进报告就是把在飞的格报成失败，
而 `failed` 恰是审计者最先会查的字段。

判据用文件新近度（`_IN_FLIGHT_WINDOW`）而不是「是否有活进程」—— 后者要求本工具与运行在同一台机器上，
那不是它的使用前提（历代表可能在别处复算）。
"""

from __future__ import annotations

import importlib.util
import json
import pathlib

import pytest

HERE = pathlib.Path(__file__).resolve().parent
MATRIX = HERE.parent / "discover_matrix"


def _module():
    path = MATRIX / "generation_history.py"
    if not path.is_file():
        pytest.skip("no generation_history.py")
    spec = importlib.util.spec_from_file_location("generation_history", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _cell(root: pathlib.Path, name: str, *, completed: bool) -> pathlib.Path:
    cell = root / name
    cell.mkdir(parents=True)
    if completed:
        (cell / "discover-completed.json").write_text(json.dumps({
            "coverage_status": "full", "issues": [], "excluded_findings": [],
            "excluded_observations": [], "coverage_gaps": [],
        }))
    else:
        (cell / "partial.log").write_text("in progress")
    return cell


def test_recent_incomplete_cell_counts_as_in_flight(tmp_path: pathlib.Path) -> None:
    module = _module()
    run = tmp_path / "run1"
    _cell(run, "0000-claude", completed=True)
    _cell(run, "0006-gpt", completed=False)   # 刚写过 → 进行中

    result = module.scan(tmp_path)
    assert result["completed"] == 1
    assert result["in_flight"] == 1, "刚写过的未完成格必须计为进行中"
    assert result["failed"] == 0, (
        "把在飞的格计为失败会让报告把进行中的运行报成失败 —— "
        "而 `failed` 是审计者最先查的字段"
    )


def test_stale_incomplete_cell_counts_as_failed(tmp_path: pathlib.Path, monkeypatch) -> None:
    """窗口之外的未完成格仍算失败 —— 否则一个被杀掉的运行会永远显示「进行中」。"""

    module = _module()
    run = tmp_path / "run1"
    _cell(run, "0000-claude", completed=True)
    _cell(run, "0006-gpt", completed=False)

    # 把「现在」推到窗口之后，而不是去改文件 mtime：后者依赖文件系统时间粒度。
    real_now = module._now()
    monkeypatch.setattr(module, "_now", lambda: real_now + module._IN_FLIGHT_WINDOW + 60)

    result = module.scan(tmp_path)
    assert result["failed"] == 1
    assert result["in_flight"] == 0


def test_completed_run_reports_neither(tmp_path: pathlib.Path) -> None:
    module = _module()
    run = tmp_path / "run1"
    for name in ("0000-claude", "0000-gpt", "0006-claude"):
        _cell(run, name, completed=True)
    result = module.scan(tmp_path)
    assert (result["completed"], result["failed"], result["in_flight"]) == (3, 0, 0)
