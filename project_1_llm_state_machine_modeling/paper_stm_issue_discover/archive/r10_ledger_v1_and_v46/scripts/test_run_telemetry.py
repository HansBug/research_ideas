"""遥测汇总只许做除法，不许猜；且不得把「键名取错」伪装成「该角色没消耗」。

三条各对应一个真实坑：

1. **`tokens_by_role` 的子键是 `input`/`output`，顶层 `tokens` 却是 `input_tokens`/`output_tokens`。**
   按错的键取会静默得到全 0，而全 0 与「该角色确实没消耗」在表里长得一样 —— 本文件第一版
   就是这么错的，逐角色一栏全是 0.0%。
2. **`.tryN` 目录必须排除**：那是被放弃的尝试，算进成本会虚增。
3. **`cache_read_input_tokens` 为 0 不等于没有缓存**，只等于 provider 没报；
   汇总层不得据此推断任何结论（本测试只锁住「原样透传」）。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_telemetry as T


def _cell(root: pathlib.Path, name: str, *, out: int, inp: int, ms: int, roles: dict) -> None:
    run, cell = name.split("/")
    d = root / run / cell
    d.mkdir(parents=True, exist_ok=True)
    (d / "discover-completed.json").write_text(json.dumps({
        "issues": [],
        "telemetry_summary": {
            "tokens": {"input_tokens": inp, "output_tokens": out, "total_tokens": inp + out,
                       "cache_read_input_tokens": 0},
            "tokens_by_role": roles,
            "llm_elapsed_ms_by_role": {k: 1000 for k in roles},
            "node_elapsed_ms_by_name": {"split_requirements": ms},
            "node_elapsed_ms_sum": ms,
            "llm_elapsed_ms_sum": 1000 * len(roles),
            "llm_call_count": len(roles),
            "node_count": 3,
        },
    }))


@pytest.fixture()
def gen(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> str:
    root = tmp_path / "matrix-t"
    _cell(root, "run1/0001-claude", out=100, inp=900, ms=5000,
          roles={"requirement_splitter": {"input": 500, "output": 60, "total": 560},
                 "assertion_converter": {"input": 400, "output": 40, "total": 440}})
    _cell(root, "run1/0002-gpt", out=200, inp=800, ms=7000,
          roles={"requirement_splitter": {"input": 800, "output": 200, "total": 1000}})
    # 放弃的尝试：不得计入成本
    _cell(root, "run1/0002-gpt.try1", out=9999, inp=9999, ms=9999,
          roles={"requirement_splitter": {"input": 9999, "output": 9999, "total": 19998}})
    monkeypatch.setattr(T, "RUNS", tmp_path)
    return "matrix-t"


def test_by_role_uses_the_right_subkeys(gen: str) -> None:
    """全 0 是键名取错的症状，不是「没消耗」。"""

    s = T.summarise(T.collect(gen))
    assert s["output_tokens_by_role"] == {"requirement_splitter": 260, "assertion_converter": 40}
    assert s["input_tokens_by_role"] == {"requirement_splitter": 1300, "assertion_converter": 400}
    assert sum(s["output_tokens_by_role"].values()) > 0


def test_abandoned_try_directories_are_excluded(gen: str) -> None:
    s = T.summarise(T.collect(gen))
    assert s["cells"] == 2
    assert s["output_tokens_total"] == 300, "放弃的尝试被算进了成本"


def test_totals_are_plain_sums(gen: str) -> None:
    s = T.summarise(T.collect(gen))
    assert s["input_tokens_total"] == 1700
    assert s["node_elapsed_ms_total"] == 12000
    assert s["llm_calls_total"] == 3


def test_per_cell_stats_come_from_real_cells(gen: str) -> None:
    s = T.summarise(T.collect(gen))
    o = s["output_tokens_per_cell"]
    assert (o["min"], o["max"]) == (100, 200)
    assert s["node_elapsed_s_per_cell"]["max"] == 7.0


def test_cache_field_is_passed_through_not_interpreted(gen: str) -> None:
    """为 0 只代表 provider 没报；汇总层不得据此下任何结论。"""

    cells = T.collect(gen)["cells"]
    assert all(c["cache_read_input_tokens"] == 0 for c in cells)
    assert "cache" not in json.dumps(T.summarise(T.collect(gen)), ensure_ascii=False)
