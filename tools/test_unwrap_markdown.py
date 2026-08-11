"""Tests for `unwrap_markdown`.

The risk with a reflow tool is not that it fails to join -- it is that it joins something
it should have left alone. Most of these tests are therefore about what stays put.
"""

from __future__ import annotations

import pytest

from tools.unwrap_markdown import unwrap


class TestJoinsParagraphs:
    def test_cjk_lines_join_without_a_space(self):
        """CommonMark renders the soft break as a space, and between two CJK characters
        that space is an artifact -- it shows up in the rendered page as 比对。 60."""
        assert unwrap("这是一段话，\n第二行。") == "这是一段话，第二行。"

    def test_latin_lines_join_with_a_space(self):
        assert unwrap("a sentence that was\nwrapped here") == "a sentence that was wrapped here"

    @pytest.mark.parametrize(("text", "expected"), [
        ("中文然后\nEnglish", "中文然后 English"),
        ("English then\n中文", "English then 中文"),
        ("汉字接\n42", "汉字接 42"),
    ])
    def test_mixed_script_boundaries_keep_the_space(self, text: str, expected: str):
        """A CJK *ideograph* next to Latin needs the separator. Fullwidth *punctuation*
        does not -- that case is in TestFullwidthPunctuationBoundaries."""
        assert unwrap(text) == expected

    def test_blank_line_still_separates_paragraphs(self):
        assert unwrap("一段。\n续行。\n\n新段。") == "一段。续行。\n\n新段。"

    def test_leading_whitespace_on_continuation_is_dropped(self):
        """One separator, not the original indent. Uses Latin text because between two
        CJK characters the correct join adds nothing, which would hide the trimming."""
        assert unwrap("start of line\n    indented continuation") == (
            "start of line indented continuation")

    def test_indented_cjk_continuation_joins_with_no_space_at_all(self):
        assert unwrap("开头\n    缩进的续行") == "开头缩进的续行"


class TestLeavesStructureAlone:
    def test_fenced_code_is_byte_identical(self):
        src = "```python\ndef f():\n    return (1 +\n            2)\n```\n"
        assert unwrap(src) == src

    def test_mermaid_fence_is_untouched(self):
        src = '```mermaid\npie title x\n  "a" : 1\n  "b" : 2\n```\n'
        assert unwrap(src) == src

    def test_tilde_fence_too(self):
        src = "~~~\nliteral\nlines\n~~~\n"
        assert unwrap(src) == src

    def test_a_paragraph_inside_a_fence_is_not_folded(self):
        src = "```\n中文一行\n中文二行\n```\n"
        assert unwrap(src) == src

    def test_table_rows_each_keep_their_line(self):
        src = "| a | b |\n| --- | --- |\n| 1 | 2 |\n"
        assert unwrap(src) == src

    def test_a_table_following_a_paragraph_is_not_absorbed(self):
        assert unwrap("说明文字\n| a |\n| --- |") == "说明文字\n| a |\n| --- |"

    def test_headings_stay_separate(self):
        assert unwrap("## 标题\n正文") == "## 标题\n正文"

    def test_thematic_break_stays_separate(self):
        assert unwrap("上文\n\n---\n\n下文") == "上文\n\n---\n\n下文"

    def test_html_block_tags_stay_on_their_own_lines(self):
        src = "<details><summary>x</summary>\n\n| a |\n| --- |\n\n</details>\n"
        assert unwrap(src) == src

    def test_indented_code_block_is_preserved(self):
        src = "前文\n\n    code line 1\n    code line 2\n"
        assert unwrap(src) == src

    def test_link_reference_definitions_stay_separate(self):
        src = "[a]: https://x\n[b]: https://y\n"
        assert unwrap(src) == src


class TestLists:
    def test_each_item_starts_a_new_line(self):
        assert unwrap("- 一\n- 二") == "- 一\n- 二"

    def test_continuation_folds_into_its_item(self):
        assert unwrap("- 列表项被\n  硬换行") == "- 列表项被硬换行"

    @pytest.mark.parametrize("marker", ["-", "*", "+", "1.", "2)"])
    def test_all_bullet_and_ordered_markers_recognised(self, marker: str):
        assert unwrap(f"{marker} 一\n{marker} 二") == f"{marker} 一\n{marker} 二"

    def test_a_list_after_a_paragraph_is_not_absorbed(self):
        assert unwrap("引导句：\n- 项") == "引导句：\n- 项"


class TestBlockquotes:
    def test_a_quote_run_folds_to_one_line(self):
        assert unwrap("> 引用被\n> 硬换行了。") == "> 引用被硬换行了。"

    def test_blank_quote_line_splits_the_run(self):
        assert unwrap("> 一段。\n>\n> 二段。") == "> 一段。\n>\n> 二段。"

    def test_a_table_inside_a_quote_keeps_its_rows(self):
        src = "> | a |\n> | --- |\n"
        assert unwrap(src) == src

    def test_quote_does_not_swallow_the_paragraph_after_it(self):
        assert unwrap("> 引用。\n\n正文。") == "> 引用。\n\n正文。"


class TestIdempotenceAndFidelity:
    @pytest.mark.parametrize("src", [
        "中文一段。\n续行。\n\n## 标题\n\n| a |\n| --- |\n\n```\ncode\n```\n",
        "- 项一\n  续行\n- 项二\n\n> 引用\n> 续行\n",
    ])
    def test_running_twice_changes_nothing_more(self, src: str):
        once = unwrap(src)
        assert unwrap(once) == once

    def test_trailing_newline_is_preserved(self):
        assert unwrap("一段。\n续行。\n").endswith("。\n")

    def test_already_unwrapped_text_is_returned_unchanged(self):
        src = "这是一整段没有硬换行的文字。\n\n## 标题\n\n下一段。\n"
        assert unwrap(src) == src

    def test_no_content_is_lost(self):
        """Every non-whitespace character survives the fold.

        Blockquote markers are stripped before comparing: folding `> 引` and `> 用` into
        `> 引用` legitimately drops one `>`, since the marker is structure rather than
        content, and the rendered output is identical either way.
        """
        src = "中文一段，\n带 English 词，\n和 `code`。\n\n- 项\n  续\n\n> 引\n> 用\n"
        strip = lambda t: "".join(t.replace(">", "").split())
        assert strip(unwrap(src)) == strip(src)


class TestFullwidthPunctuationBoundaries:
    """A break after fullwidth punctuation needs no separator, even before Latin text.

    These read wrong with a space -- `因此： 154 条` -- and the punctuation glyph already
    carries its own visual gap, so the space is doubly redundant.
    """

    @pytest.mark.parametrize(("text", "expected"), [
        ("因此：\n154 条", "因此：154 条"),
        ("以句号结束。\n60/60 全覆盖", "以句号结束。60/60 全覆盖"),
        ("逗号，\nGPT-4o 如此", "逗号，GPT-4o 如此"),
        ("问号？\nyes", "问号？yes"),
        ("括号收）\nnext", "括号收）next"),
    ])
    def test_no_space_after_a_fullwidth_closer(self, text: str, expected: str):
        assert unwrap(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [
        ("见下表\n（含合计）", "见下表（含合计）"),
        ("value\n「引用」", "value「引用」"),
    ])
    def test_no_space_before_a_fullwidth_opener(self, text: str, expected: str):
        assert unwrap(text) == expected

    def test_latin_to_latin_still_gets_its_space(self):
        assert unwrap("word,\nnext") == "word, next"


class TestAmbiguousWidthPunctuation:
    """`east_asian_width` calls the em dash and the middle dot Ambiguous, but Chinese text
    uses them fullwidth. Without special-casing, `理由——\\n因为` gains a stray space."""

    @pytest.mark.parametrize(("text", "expected"), [
        ("正确性未经验证——\n本审阅发现冲突", "正确性未经验证——本审阅发现冲突"),
        ("省略…\n后续内容", "省略…后续内容"),
        ("中文·\n分隔", "中文·分隔"),
    ])
    def test_cjk_context_takes_no_space(self, text: str, expected: str):
        assert unwrap(text) == expected

    @pytest.mark.parametrize(("text", "expected"), [
        ("an aside --\nand more", "an aside -- and more"),
        ("range 1—\n2 items", "range 1— 2 items"),
    ])
    def test_latin_context_keeps_its_spaces(self, text: str, expected: str):
        """The same glyph between Latin words is a real separator."""
        assert unwrap(text) == expected


def test_list_inside_blockquote_keeps_one_item_per_line() -> None:
    """引用块里的列表不能被折成一行。

    首版只对表格/标题在引用块内另起行，漏了列表项，于是

        > **优先级**：
        > - P0 —— …
        > - P1 —— …

    被折成 `> **优先级**：- P0 —— … - P1 —— …`，渲染出来是一个段落而不是列表。
    这类写法在本仓库的口径说明里很常见，不是边角情形。
    """

    src = (
        "> **优先级口径**：\n"
        "> - **P0** —— 会让 claim 站不住\n"
        "> - **P1** —— 成稿必须有\n"
    )
    out = unwrap(src)
    assert out.count("\n> - ") == 2, out
    assert "P0** —— 会让 claim 站不住 - **P1" not in out


def test_ordered_list_inside_blockquote_too() -> None:
    src = "> 步骤：\n> 1. 先看这个\n> 2. 再看那个\n"
    out = unwrap(src)
    assert "> 1. 先看这个" in out and "> 2. 再看那个" in out


def test_fenced_code_inside_a_blockquote_is_not_folded() -> None:
    """⛔ 引用块里的代码围栏必须逐字保留。

    `FENCE` 的 ``^\\s{0,3}`` 越不过 ``> `` 前缀，所以在补 `quoted_fence` 之前，
    围栏行、代码行、收尾围栏会一起掉进散文折叠分支，被压成一行
    ``> ```python code ``` ``。**这是对源代码的静默损坏**，且已真实发生过一次：
    一段引在 `>` 块里的 ``PredicateName = Literal[...]`` 摘录被本工具毁掉。
    """
    src = (
        "> 说明如下：\n"
        ">\n"
        "> ```python\n"
        "> PredicateName = Literal[tuple(PREDICATE_ORDER)]  # type: ignore\n"
        "> x = 1\n"
        "> ```\n"
        ">\n"
        "> 所以它是同一律。\n"
    )
    assert unwrap(src) == src


def test_quoted_fence_does_not_swallow_the_rest_of_the_file() -> None:
    """收尾围栏必须被认出来，否则其后的一切都进不了折叠。"""
    src = "> ```\n> code\n> ```\n\n这段\n应该折叠。\n"
    assert unwrap(src) == "> ```\n> code\n> ```\n\n这段应该折叠。\n"


def test_tilde_fence_inside_blockquote() -> None:
    src = "> ~~~\n> a  b\n> ~~~\n"
    assert unwrap(src) == src
