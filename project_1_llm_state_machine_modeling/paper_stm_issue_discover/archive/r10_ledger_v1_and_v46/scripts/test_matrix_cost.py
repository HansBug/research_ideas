"""代次成本汇总：两种时间不得混用，缺测不得读成零。

两个失效形态都实测过同型的：

1. **串行累加当墙钟。** v35 的累加耗时是 8h15m，而 48 格在 `MAX=8` 下实际墙钟 1.61 小时 ——
   差 5 倍。用累加值回答「跑完要多久」会把 324 格估成两天多。
2. **`None` 当 0。** `cache_creation_input_tokens` 在 24 格里是 `None`（provider 没报），
   合起来若按 0 相加，会得到「缓存从未创建」这个结论 —— 而 `cache_read` 明明有 4.8M。
   缺测必须与真零分开报，这正是仓库纪律「任何 0/从不/全部 的结果先打分母」。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# ⛔ 归档后脚本与测试同在 `scripts/`，原先的 `…/ "discover_matrix"` 指向不存在的目录。
MATRIX = Path(__file__).resolve().parent
if str(MATRIX) not in sys.path:
    sys.path.insert(0, str(MATRIX))

import matrix_cost  # noqa: E402


def _cell(base: Path, run: str, pair: str, arm: str, telemetry: dict) -> None:
    directory = base / run / f"{pair}-{arm}"
    directory.mkdir(parents=True)
    (directory / "discover-completed.json").write_text(
        json.dumps({"telemetry_summary": telemetry})
    )


def _telemetry(**over) -> dict:
    base = {
        "llm_call_count": 10,
        "transport_attempt_count": 11,
        "retry_count": 1,
        "node_elapsed_ms_sum": 60_000.0,
        "node_elapsed_ms_by_name": {"split_requirements": 40_000.0, "publish": 20_000.0},
        "llm_elapsed_ms_by_role": {"requirement_splitter": 40_000.0},
        "tokens": {
            "input_tokens": 1_000,
            "output_tokens": 100,
            "total_tokens": 1_100,
            "cache_read_input_tokens": 500,
            "cache_creation_input_tokens": None,
            "reasoning_tokens": None,
        },
        "tokens_by_role": {"requirement_splitter": {"input": 1_000, "output": 100, "total": 1_100}},
    }
    base.update(over)
    return base


@pytest.fixture
def base(tmp_path):
    root = tmp_path / "matrix-vtest"
    _cell(root, "run1", "0000", "claude", _telemetry())
    _cell(root, "run1", "0000", "gpt", _telemetry(llm_call_count=20))
    _cell(root, "run2", "0006", "claude", _telemetry())
    return root


def test_sums_across_cells(base) -> None:
    s = matrix_cost.summarise(base)
    assert s["cells_completed"] == 3
    assert s["llm_calls"] == 40
    assert s["transport_retries"] == 3
    assert s["tokens"]["total_tokens"] == 3_300
    assert s["node_ms_by_stage"]["split_requirements"] == 120_000.0


def test_missing_token_fields_are_counted_not_summed_as_zero(base) -> None:
    """⭐ `None` 与 0 必须分开 —— 否则「缓存从未创建」会成为一个凭空的结论。"""

    s = matrix_cost.summarise(base)
    assert s["tokens_missing_in_cells"]["cache_creation_input_tokens"] == 3
    assert s["tokens_missing_in_cells"]["reasoning_tokens"] == 3
    assert s["tokens_missing_in_cells"]["input_tokens"] == 0
    # 全缺测时不得出现一个看起来正常的 0
    assert "cache_creation_input_tokens" not in s["tokens"]


def test_wallclock_absence_is_stated_not_substituted(base) -> None:
    """⭐ 没有墙钟时必须说没有，不得拿串行累加冒充。"""

    s = matrix_cost.summarise(base)
    assert s["wallclock"]["available"] is False
    assert "不得用累加值代替" in s["wallclock"]["note"]
    text = matrix_cost.render(s)
    assert "墙钟不可用" in text
    assert "这是各节点耗时相加，不是墙钟" in text


def test_wallclock_is_read_when_the_launcher_wrote_it(base) -> None:
    (base / "WALLCLOCK.txt").write_text(
        "started_at: 2026-08-08T03:23:00Z\n"
        "max_concurrency: 8\n"
        "finished_at: 2026-08-08T05:00:00Z\n"
        "elapsed: 1h37m00s\n"
    )
    s = matrix_cost.summarise(base)
    assert s["wallclock"]["available"] is True
    assert s["wallclock"]["elapsed"] == "1h37m00s"
    assert "1h37m00s" in matrix_cost.render(s)


def test_per_arm_and_per_pair_breakdowns(base) -> None:
    s = matrix_cost.summarise(base)
    assert s["by_arm"]["claude"]["cells"] == 2
    assert s["by_arm"]["gpt"]["llm_calls"] == 20
    assert set(s["by_pair"]) == {"0000", "0006"}


def test_an_empty_generation_refuses_rather_than_printing_zeros(tmp_path) -> None:
    """⭐ 一份看起来正常的空汇总比报错危险 —— 它会被当成「这一代次没花什么」。"""

    empty = tmp_path / "matrix-empty"
    empty.mkdir()
    with pytest.raises(SystemExit, match="没有落盘完成的格"):
        matrix_cost.main(["--base", str(empty)])


def test_unparsable_cell_is_skipped_not_fatal(base) -> None:
    bad = base / "run3" / "0009-claude"
    bad.mkdir(parents=True)
    (bad / "discover-completed.json").write_text("{ not json")
    assert matrix_cost.summarise(base)["cells_completed"] == 3


def test_non_cell_directories_are_ignored(base) -> None:
    (base / "run1" / "notacell").mkdir()
    (base / "run1" / "0000-claude.try2").mkdir()
    assert matrix_cost.summarise(base)["cells_completed"] == 3


# ---------------------------------------------------------------- 续跑墙钟

def _segmented(base, *segments) -> None:
    lines = []
    for index, seconds in enumerate(segments, 1):
        lines.append(f"segment: {index}")
        lines.append(f"segment_{index}_started_at: 2026-08-08T0{index}:00:00Z")
        if index == 1:
            lines.append("started_at: 2026-08-08T01:00:00Z")
            lines.append("max_concurrency: 8")
        lines.append(f"segment_{index}_elapsed_seconds: {seconds}")
        lines.append(f"finished_at: 2026-08-08T0{index}:30:00Z")
    (base / "WALLCLOCK.txt").write_text("\n".join(lines) + "\n")


def test_a_resumed_run_sums_its_segments(base) -> None:
    """⭐ 续跑是**预期用法**：`one()` 在每次尝试开头检查落盘就返回，所以重跑会跳过已完成的格。

    逐行读取时后者覆盖前者，若不相加，「跑了 9 小时、中断、再跑 20 分钟补完」会被报成 20 分钟 ——
    这在 324 格上是最可能发生的读数错误。
    """

    _segmented(base, 32_400, 1_200)
    wall = matrix_cost.summarise(base)["wallclock"]
    assert wall["segments"] == 2
    assert wall["elapsed_seconds"] == 33_600
    assert wall["elapsed"] == "9h20m00s"
    assert "不是一次跑完" in wall["segments_note"]
    assert "续跑 2 段" in matrix_cost.render(matrix_cost.summarise(base))


def test_a_single_segment_carries_no_resume_note(base) -> None:
    """⭐ 负控：一次跑完时不得出现「续跑」字样，否则读者会以为数字是拼的。"""

    _segmented(base, 5_800)
    wall = matrix_cost.summarise(base)["wallclock"]
    assert wall["segments"] == 1
    assert "segments_note" not in wall
    assert "续跑" not in matrix_cost.render(matrix_cost.summarise(base))


def test_started_at_is_the_first_segments(base) -> None:
    """总起始时间必须是**第一段**的，尾段的 finished_at 才是终点。"""

    _segmented(base, 100, 200, 300)
    wall = matrix_cost.summarise(base)["wallclock"]
    assert wall["started_at"] == "2026-08-08T01:00:00Z"
    assert wall["finished_at"] == "2026-08-08T03:30:00Z"
    assert wall["elapsed_seconds"] == 600


def test_a_malformed_segment_value_is_skipped_not_fatal(base) -> None:
    (base / "WALLCLOCK.txt").write_text(
        "segment: 1\nsegment_1_elapsed_seconds: oops\nmax_concurrency: 8\n"
    )
    wall = matrix_cost.summarise(base)["wallclock"]
    assert wall["available"] is True
    assert "segments" not in wall
