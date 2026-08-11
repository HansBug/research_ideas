"""`check_md_anchors` 的回归测试。

这个工具存在的理由是一次真实事故：改写 `paper_story.md` §10 之后，两份预案里指向它的
**10 处「§号 + 逐字片段」锚点**全部失配，而当时的验证结论是「失效引用净增 0」——
那句话字面属实，因为 `check_md_links` 只查链接可达性，**看不见片段是否还在**。
链接仍然通、§号仍然在，唯独引的那句话已经被改掉了。

所以这里的测试重点有两个，缺一不可：
1. **真失配必须报**——否则工具白写；
2. **不是锚点的引述不许报**——过报同样致命。实测过两版：只要求「同一行有链接」时报
   189 处，加上「行内有 §」仍报 121 处，其中绝大多数是一行里链接与引述各说各话。
   ⚠️ 一个报 121 次狼的工具比没有工具更糟，因为人会学会忽略它。
"""

from __future__ import annotations

import pathlib

from tools.check_md_anchors import normalize, scan


def _w(tmp: pathlib.Path, name: str, body: str) -> None:
    p = tmp / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")


def test_missing_fragment_is_reported(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "target.md", "# T\n\n## 3. 别的标题\n")
    _w(tmp_path, "a.md", "见 [target](./target.md) §3「问题形式化与任务定义」。\n")
    bad = scan(tmp_path)
    assert [b[3] for b in bad] == ["问题形式化与任务定义"]


def test_present_fragment_is_clean(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "target.md", "# T\n\n## 3. 问题形式化与任务定义\n")
    _w(tmp_path, "a.md", "见 [target](./target.md) §3「问题形式化与任务定义」。\n")
    assert scan(tmp_path) == []


def test_emphasis_markers_are_normalized_away(tmp_path: pathlib.Path) -> None:
    """加粗边界漂移不算失配——同一句话，收 `**` 的位置不同，内容完全一致。"""
    _w(tmp_path, "target.md", "**覆盖性的分母来自需求侧**，不是模型的可疑点集\n")
    _w(tmp_path, "a.md", "见 [t](./target.md) §5「覆盖性的**分母来自需求侧**」。\n")
    assert scan(tmp_path) == []


def test_whitespace_is_normalized_away(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "target.md", "真值\n封存\n")
    _w(tmp_path, "a.md", "见 [t](./target.md) §7「真值封存」。\n")
    assert scan(tmp_path) == []


def test_quote_without_section_marker_is_not_an_anchor(tmp_path: pathlib.Path) -> None:
    """没有 §号就不是 §9.4 规定的锚点形态，⛔ 不许报。"""
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", "见 [t](./target.md)，其中「这篇论文是什么」讲得最清楚。\n")
    assert scan(tmp_path) == []


def test_quote_far_from_link_is_not_an_anchor(tmp_path: pathlib.Path) -> None:
    """⭐ 这是过报的主因：一行里链接与引述各说各话。

    实测现场：`paper_story.md` 某行链接指向 `README.md`，而同行的「…」引的是
    talks 里的导师原话——两者毫无关系。按「同一行」判会把它当锚点报出来。
    """
    filler = "中" * 200
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", f"见 [t](./target.md) §1 的说明。{filler}另外「导师原话在别处」。\n")
    assert scan(tmp_path) == []


def test_section_marker_must_sit_between_link_and_fragment(
    tmp_path: pathlib.Path,
) -> None:
    """§号在链接**之前**不算——那是「§1 见 [t](...)」这种句式，片段未必锚在 t 上。"""
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", "§1 提到 [t](./target.md)，而「另一份文件的说法」不同。\n")
    assert scan(tmp_path) == []


def test_ellipsis_fragment_is_skipped(tmp_path: pathlib.Path) -> None:
    """带省略号的本就不是逐字引用，报它是噪声。"""
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", "见 [t](./target.md) §3「开头……结尾」。\n")
    assert scan(tmp_path) == []


def test_short_fragment_is_skipped(tmp_path: pathlib.Path) -> None:
    """太短的引号内容多半是术语而非引文，避免噪声。"""
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", "见 [t](./target.md) §3「入口」。\n")
    assert scan(tmp_path) == []


def test_archive_is_skipped(tmp_path: pathlib.Path) -> None:
    """归档是冻结史料，其锚点指向历史版本，⛔ 不该被要求跟着现行版走。"""
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "archive/old.md", "见 [t](../target.md) §3「早已改掉的说法」。\n")
    assert scan(tmp_path) == []


def test_broken_link_is_left_to_the_other_tool(tmp_path: pathlib.Path) -> None:
    """目标不存在归 `check_md_links` 管，⛔ 这里不重复报。"""
    _w(tmp_path, "a.md", "见 [t](./gone.md) §3「某个片段」。\n")
    assert scan(tmp_path) == []


def test_self_reference_is_skipped(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "a.md", "见 [自己](./a.md) §3「本文件不存在的话」。\n")
    assert scan(tmp_path) == []


def test_multiple_fragments_after_one_link(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "target.md", "语料里确有这一句\n")
    _w(tmp_path, "a.md", "见 [t](./target.md) §3「语料里确有这一句」与「语料里没有这一句」。\n")
    assert [b[3] for b in scan(tmp_path)] == ["语料里没有这一句"]


def test_reported_line_number_is_correct(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "target.md", "无关内容\n")
    _w(tmp_path, "a.md", "第一行\n\n见 [t](./target.md) §3「找不到的片段」。\n")
    assert [b[1] for b in scan(tmp_path)] == [3]


def test_normalize_strips_emphasis_and_space() -> None:
    assert normalize("**a** `b` c") == "abc"


def test_the_real_regression_shape(tmp_path: pathlib.Path) -> None:
    """复现那次真实事故：正文把「尚未纳入」整段删掉，锚点必须变红。"""
    _w(tmp_path, "story.md", "## 10 相关工作\n\n五条轴，第 5 轴**轴已确立**。\n")
    _w(
        tmp_path,
        "plan.md",
        "| 影响 | [story](./story.md) §10 末段那条「**尚未纳入**的轴」需转正 |\n",
    )
    bad = scan(tmp_path)
    assert len(bad) == 1 and "尚未纳入" in bad[0][3]
