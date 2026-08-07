"""需求层三道门的失败必须**局部隔离**，不得杀整格。

背景：`7c118ab2` 记录跨 v22/v23 四次重试里**三次**是门致命 raise，而 `47327849` 只把断言层降级了，
需求层的 `initialization_anchored` / `conceded_omission` / `trigger_consuming` 三道门仍是致命的。

代价不只是吞吐 —— 致命 raise 会把该轮**已产出的其余需求**一起丢掉（CLAUDE.md §6：run record
缺失关键证据）。诊断实测：`0047` 三轮 claude 里 **1 轮**因此整格丢失。

⚠️ 本文件测的是**隔离逻辑本身**，不经 LLM。逻辑与 `nodes.py` 里的判定同构：按已知 requirement id
匹配 finding 前缀 → 归责 → 存活集非空则隔离，否则仍致命。
"""

from __future__ import annotations

import pytest


def _isolate(requirement_ids: list[str], findings: list[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`nodes.py` 里那段隔离判定的同构实现，返回 (blamed, survivors)。"""
    blamed = tuple(r for r in requirement_ids if any(f.startswith(f"{r} ") for f in findings))
    survivors = tuple(r for r in requirement_ids if r not in blamed)
    return blamed, survivors


def test_one_bad_requirement_is_quarantined_and_the_rest_survive() -> None:
    """诊断实测的形态：`REQ-005` 绑 `[*]` 被门拒，其余五条应存活。"""
    ids = ["REQ-001", "REQ-002", "REQ-003", "REQ-004", "REQ-005", "REQ-006"]
    blamed, survivors = _isolate(ids, ["REQ-005 binds ['source'] to [*] with ..."])
    assert blamed == ("REQ-005",)
    assert len(survivors) == 5
    assert "REQ-005" not in survivors


def test_multiple_blamed_requirements() -> None:
    blamed, survivors = _isolate(
        ["REQ-001", "REQ-002", "REQ-003"],
        ["REQ-001 asks `reaches` while naming ...", "REQ-003 records in `limitations` ..."],
    )
    assert blamed == ("REQ-001", "REQ-003")
    assert survivors == ("REQ-002",)


def test_still_fatal_when_every_requirement_is_blamed() -> None:
    """⭐ 隔离后集合为空 → 没有局部可隔离的东西，失败确实是整格的，保留致命行为。

    这一支与 `47327849` 在断言层的处置一致：局部隔离不是「永不失败」，是「只在有东西可保留时保留」。
    """
    blamed, survivors = _isolate(["REQ-001"], ["REQ-001 binds ['source'] to [*] ..."])
    assert blamed == ("REQ-001",)
    assert survivors == ()  # 调用方据此仍 raise


def test_no_requirement_can_be_blamed_stays_fatal() -> None:
    """finding 不以任何已知 id 开头（格式变了 / 门换了措辞）→ 无法归责 → 仍致命。

    ⚠️ 这条是**故意**的保守设计：宁可整格失败，也不要静默丢掉一条无法归责的门报 ——
    后者会让「门拦下了什么」在 run record 里消失。
    """
    blamed, survivors = _isolate(["REQ-001", "REQ-002"], ["something changed the message format"])
    assert blamed == ()
    assert len(survivors) == 2  # 调用方据 `not blamed` 仍 raise


def test_prefix_match_requires_a_space_so_ids_do_not_collide() -> None:
    """`REQ-1` 不得匹配 `REQ-10 ...` 的 finding。"""
    blamed, _ = _isolate(["REQ-1", "REQ-10"], ["REQ-10 binds ..."])
    assert blamed == ("REQ-10",)


@pytest.mark.parametrize(
    "gate_message",
    [
        "REQ-005 binds ['source'] to [*] with source_context.behavior_phase='initialization'.",
        "REQ-005 records in `limitations` that the model never declared ['Sys.X']",
        "REQ-005 asks `reaches` while naming 'Sys.evt', an event the model declares.",
    ],
)
def test_all_three_requirement_gates_are_isolatable(gate_message: str) -> None:
    """三道门的 finding 都以 requirement id 开头，故三者都可隔离。"""
    blamed, survivors = _isolate(["REQ-004", "REQ-005"], [gate_message])
    assert blamed == ("REQ-005",)
    assert survivors == ("REQ-004",)


def test_nodes_py_does_not_raise_unconditionally_on_step_findings() -> None:
    """回归闸：`nodes.py` 里不得退回「见 step_findings 就 raise」。"""
    import pathlib

    src = (
        pathlib.Path(__file__).resolve().parents[1]
        / "src/paper_stm_feedback_loop/discover/nodes.py"
    ).read_text()
    i = src.index("if step_findings:")
    window = src[i : i + 2200]
    assert "quarantine not possible" in window, "隔离分支不见了，门又变成无条件致命"
    assert "survivors" in window
