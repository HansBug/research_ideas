"""`check_md_links` 的回归测试。

每一条都对应一次真实误判：三类引用各自漏报过，且漏报的表现都是「零死链」——
一个看起来像通过的结论。所以这里的重点不是「能报出坏链接」，而是**坏链接不会被
静默放过**，以及**好链接不会被误报**（误报同样有害：它会让人学会忽略这个工具）。
"""

from __future__ import annotations

import pathlib

from tools.check_md_links import scan


def _w(tmp: pathlib.Path, name: str, body: str) -> pathlib.Path:
    p = tmp / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(body, encoding="utf-8")
    return p


def _kinds(bad: list) -> list[str]:
    return sorted(k for _, _, k, _ in bad)


def test_relative_link_to_missing_file_is_reported(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "a.md", "见 [别处](./gone.md)。")
    assert _kinds(scan(tmp_path, None)) == ["relative"]


def test_relative_link_to_existing_file_is_clean(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "b.md", "x")
    _w(tmp_path, "a.md", "见 [别处](./b.md)。")
    assert scan(tmp_path, None) == []


def test_anchor_is_stripped_before_resolving(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "b.md", "x")
    _w(tmp_path, "a.md", "见 [别处](./b.md#some-heading)。")
    assert scan(tmp_path, None) == []


def test_inline_code_is_not_a_link(tmp_path: pathlib.Path) -> None:
    """文档引用链接语法本身时会写在反引号里；那不是引用。

    实测误报现场：正文写「target 是小写而链接文字是大写：`[NL_SCOPE_RULE.md](...nl_scope_rule.md)`」，
    早先的扫描器把它当成真链接，报出一条并不存在的死链。
    """
    _w(tmp_path, "a.md", "写法应为 `[X.md](...x.md)`，注意大小写。")
    assert scan(tmp_path, None) == []


def test_fenced_code_is_not_a_link(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "a.md", "示例：\n\n```markdown\n[X](./nope.md)\n```\n")
    assert scan(tmp_path, None) == []


def test_illustrative_targets_are_exempt(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "a.md", "同目录写成 [GUIDE.md](./GUIDE.md)。")
    assert scan(tmp_path, None) == []


def test_blob_url_with_stale_path_is_reported(tmp_path: pathlib.Path) -> None:
    """本仓库的绝对 blob URL 可以对着工作区校验——只扫相对链接会全部漏掉。"""
    (tmp_path / ".git").mkdir()
    _w(tmp_path, "a.md",
       "见 https://github.com/o/r/blob/main/old/path/x.md 。")
    assert _kinds(scan(tmp_path, "o/r")) == ["blob-url"]


def test_blob_url_pointing_at_existing_path_is_clean(tmp_path: pathlib.Path) -> None:
    (tmp_path / ".git").mkdir()
    _w(tmp_path, "real/x.md", "x")
    _w(tmp_path, "a.md", "见 https://github.com/o/r/blob/main/real/x.md 。")
    assert scan(tmp_path, "o/r") == []


def test_blob_url_of_another_repo_is_not_checked(tmp_path: pathlib.Path) -> None:
    """别人仓库的路径无从校验，报它就是纯噪声。"""
    (tmp_path / ".git").mkdir()
    _w(tmp_path, "a.md", "见 https://github.com/someone/else/blob/main/whatever.md 。")
    assert scan(tmp_path, "o/r") == []


def test_blob_url_skipped_when_no_slug_given(tmp_path: pathlib.Path) -> None:
    (tmp_path / ".git").mkdir()
    _w(tmp_path, "a.md", "见 https://github.com/o/r/blob/main/gone.md 。")
    assert scan(tmp_path, None) == []


def test_line_number_beyond_end_of_file_is_reported(tmp_path: pathlib.Path) -> None:
    """行号越界是可机器判定的那一半；它静默失效，比断链更难发现。"""
    _w(tmp_path, "b.md", "one\ntwo\nthree\n")
    _w(tmp_path, "a.md", "见 [b](./b.md) 第 99 行。")
    assert _kinds(scan(tmp_path, None)) == ["lineno-oob"]


def test_line_number_within_file_is_not_reported(tmp_path: pathlib.Path) -> None:
    """⚠️ 在界内不等于指对了内容——那一半查不了，所以纪律仍是别用行号。"""
    _w(tmp_path, "b.md", "one\ntwo\nthree\n")
    _w(tmp_path, "a.md", "见 [b](./b.md) 第 2 行。")
    assert scan(tmp_path, None) == []


def test_line_number_range_uses_the_start_value(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "b.md", "one\ntwo\n")
    _w(tmp_path, "a.md", "见 [b](./b.md) 第 50–60 行。")
    assert _kinds(scan(tmp_path, None)) == ["lineno-oob"]


def test_line_number_against_missing_file_reports_only_the_dead_link(
    tmp_path: pathlib.Path,
) -> None:
    """目标都不存在时不该重复报两条。"""
    _w(tmp_path, "a.md", "见 [b](./gone.md) 第 99 行。")
    assert _kinds(scan(tmp_path, None)) == ["relative"]


def test_skipped_directories_are_not_scanned(tmp_path: pathlib.Path) -> None:
    _w(tmp_path, "runs/a.md", "见 [x](./gone.md)。")
    _w(tmp_path, "__pycache__/b.md", "见 [x](./gone.md)。")
    assert scan(tmp_path, None) == []


def test_reported_line_number_is_correct(tmp_path: pathlib.Path) -> None:
    """行号本身报错会让人查到错的地方，等于没报。"""
    _w(tmp_path, "a.md", "第一行\n\n第三行\n\n见 [x](./gone.md)。\n")
    bad = scan(tmp_path, None)
    assert [ln for _, ln, _, _ in bad] == [5]


def test_all_three_kinds_coexist(tmp_path: pathlib.Path) -> None:
    (tmp_path / ".git").mkdir()
    _w(tmp_path, "b.md", "one\n")
    _w(tmp_path, "a.md",
       "见 [x](./gone.md)；\n\n见 https://github.com/o/r/blob/main/nope.md；\n\n"
       "见 [b](./b.md) 第 42 行。\n")
    assert _kinds(scan(tmp_path, "o/r")) == ["blob-url", "lineno-oob", "relative"]
