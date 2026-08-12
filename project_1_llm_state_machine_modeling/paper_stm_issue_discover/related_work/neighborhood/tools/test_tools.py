"""L3 两个工具的回归测试。

⛔ 跑法（⚠️ 不在 `pipeline/` 的规范测试集里，需单独跑）::

    cd project_1_llm_state_machine_modeling/paper_stm_issue_discover/related_work/neighborhood
    python -m pytest tools/test_tools.py -q
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from merge_candidates import norm_arxiv, norm_doi, norm_title, parse_tables  # noqa: E402
from verify_assets import _DOC_ONLY  # noqa: E402


class TestNormTitle:
    def test_case_folding_before_stripping(self):
        """⛔ L2 栽过的坑：`.lower()` 若在 `re.sub` 之后，大写字母会被当分隔符吃掉。

        ⭐ 判据是「仅大小写不同的两个标题必须归一到同一个 key」。
        """
        a = norm_title("Model Consistency Evaluation With LLM")
        b = norm_title("model consistency evaluation with llm")
        assert a == b == "model consistency evaluation with llm"

    def test_punctuation_and_spacing_collapse(self):
        assert norm_title("LLM-based  Repair: A Study!") == norm_title("LLM based repair a study")

    def test_letters_survive(self):
        """⛔ 回归：曾经的错误实现会把大写字母替换成空格，⭐ 这里钉死它不会。"""
        assert "abc" in norm_title("ABC")


class TestNormDoi:
    def test_extracts_from_markdown_link(self):
        assert norm_doi("see [x](https://doi.org/10.1145/234426.234431)") == "10.1145/234426.234431"

    def test_strips_trailing_punctuation(self):
        """⭐ markdown 常把 `)` `.` `,` 粘在 DOI 尾巴上。"""
        assert norm_doi("(10.1109/TSE.2023.1234).") == "10.1109/tse.2023.1234"

    def test_none_when_absent(self):
        assert norm_doi("no identifier here") is None


class TestNormArxiv:
    @pytest.mark.parametrize(
        "text,want",
        [
            ("https://arxiv.org/abs/2501.01234", "2501.01234"),
            ("arXiv:2411.17501v2", "2411.17501"),
            ("2503.12345v11 something", "2503.12345"),
        ],
    )
    def test_version_suffix_dropped(self, text, want):
        """⛔ 版本号必须去掉 —— ⭐ 否则 v1 与 v2 会被当成两篇不同的工作。"""
        assert norm_arxiv(text) == want

    def test_none_when_absent(self):
        assert norm_arxiv("10.1145/1234") is None


class TestParseTables:
    def test_reads_rows_and_skips_separator(self, tmp_path: Path):
        f = tmp_path / "x.md"
        f.write_text(
            "prose line\n\n"
            "| 标题 | 年 | 链接 |\n"
            "| :-- | :-- | :-- |\n"
            "| Some Long Enough Paper Title Here | 2025 | https://arxiv.org/abs/2501.00001 |\n",
            encoding="utf-8",
        )
        rows = parse_tables(f)
        assert len(rows) == 1
        assert rows[0]["年"] == "2025"
        assert rows[0]["_src"] == "x.md"

    def test_header_resets_after_non_table_line(self, tmp_path: Path):
        """⭐ 两张表之间隔着散文时，第二张表的表头必须被重新识别。

        ⛔ 否则第二张表的表头行会被当成数据行混进结果。
        """
        f = tmp_path / "y.md"
        f.write_text(
            "| A | B |\n| :-- | :-- |\n| first row of data here okay | v1 |\n"
            "\nsome prose in between\n\n"
            "| C | D |\n| :-- | :-- |\n| second row of data here okay | v2 |\n",
            encoding="utf-8",
        )
        rows = parse_tables(f)
        assert [set(r) - {"_src"} for r in rows] == [{"A", "B"}, {"C", "D"}]

    def test_ragged_row_dropped_not_misaligned(self, tmp_path: Path):
        """⛔ 列数对不上的行必须丢弃 —— ⭐ 强行 zip 会静默错位，比丢掉更糟。"""
        f = tmp_path / "z.md"
        f.write_text(
            "| A | B | C |\n| :-- | :-- | :-- |\n"
            "| good row with enough text | x | y |\n"
            "| ragged row missing a cell here |\n",
            encoding="utf-8",
        )
        assert len(parse_tables(f)) == 1


class TestBehavioralRegex:
    """⛔ 回归：`automat` 前缀会把「自动化」当成「自动机」。

    ⚠️ **真实事故**：初版判据用了 `automat`，⭐ 于是 `P059`（*Evaluating the Quality
    of Class **Diagrams** … and **Automation***，⛔ 类图论文）被判成行为类。
    ⭐ 实测全表 `automat\\w*` 共 11 次命中，⛔ **只有 1 次是 `automata`**，
    其余是 `Automation` / `automating` / `automatic` / `automated` / `AutomationML`。

    ⭐ 这属 `CLAUDE.md` §11 点名的那类错误：⛔ **词法判据冒充语义判断**。
    """

    @pytest.mark.parametrize(
        "text",
        ["Findings, Guidelines and Automation", "automating the process", "AutomationML", "fully automated"],
    )
    def test_automation_words_are_not_behavioral(self, text):
        from analyze_s1_corpus import _BEHAVIORAL  # noqa: PLC0415

        assert not _BEHAVIORAL.search(text), f"⛔ 「{text}」被误判为行为类"

    @pytest.mark.parametrize("text", ["timed automata", "a finite automaton", "hybrid automata models"])
    def test_real_automaton_words_still_match(self, text):
        from analyze_s1_corpus import _BEHAVIORAL  # noqa: PLC0415

        assert _BEHAVIORAL.search(text)

    @pytest.mark.parametrize(
        "text",
        ["UML (sequence diagram)", "BPMN 2.0", "Statechart", "state machine", "Scenario-based behavioral models"],
    )
    def test_core_behavioral_terms_match(self, text):
        from analyze_s1_corpus import _BEHAVIORAL  # noqa: PLC0415

        assert _BEHAVIORAL.search(text)

    def test_class_diagram_is_not_behavioral(self):
        """⭐ 最直接的反例：类图是结构图，⛔ 不是行为模型。"""
        from analyze_s1_corpus import _BEHAVIORAL  # noqa: PLC0415

        assert not _BEHAVIORAL.search("UML (Class Diagram) | UML class diagrams | Modeling artifacts")

    def test_artifact_fields_exclude_title_and_input(self):
        """⛔ 判制品不看标题、不看输入。

        ⚠️ 真实反例 `P050`：输入里提到 `UML activity diagram`，⛔ 但它做的是**转换
        工具推荐**，输出是 relevance scores —— ⭐ 把输入算进去会误判。
        """
        from analyze_s1_corpus import _ARTIFACT_FIELDS  # noqa: PLC0415

        assert "Titles" not in _ARTIFACT_FIELDS
        assert "Input_Artifact_Type" not in _ARTIFACT_FIELDS


class TestShellDetection:
    def test_doc_extensions_cover_the_flowfsm_case(self):
        """⭐ FlowFSM 空壳只含 `README.md` 与 `.gitignore` —— 两者都必须算文档。

        ⛔ 这是**真实事故的回归**：`baselines/` 2026-06-10 人工核验发现该仓库返回 200
        且存在，⛔ 但没有任何源码。⭐ 若 `.gitignore` 不在文档集里，它会被算成
        「非文档文件」，于是空壳判据失效、误判 🟢。
        """
        assert ".md" in _DOC_ONLY
        assert ".gitignore" in _DOC_ONLY
