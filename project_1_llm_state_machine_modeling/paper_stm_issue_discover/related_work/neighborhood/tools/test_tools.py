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


class TestMergeGlobDefault:
    def test_default_glob_is_strict(self):
        """⛔ 默认 glob 必须限定成 `A*_*.md`。

        ⚠️ 检索 agent 会往同一目录写临时抓取物（实测有 `paper_clean.md`、
        `atlas.txt`、`hal.html`）。⭐ `paper_clean.md` 是一篇论文的清洗正文 ——
        ⛔ 里面的表格长得**很像**候选表（有 `|`、有标题、有年份），⛔ 被解析进来
        不会报错，⭐ 只会让候选数虚高并混入不存在的条目。

        ⚠️ **诚实记录**：本轮那个文件恰好贡献 0 行，⛔ 所以这道防护实际上没拦住
        任何东西。⭐ 保留它是因为**下一个临时文件不一定这么无害**。
        """
        import argparse
        import inspect

        import merge_candidates  # noqa: PLC0415

        src = inspect.getsource(merge_candidates.main)
        assert '"A*_*.md"' in src, "⛔ 默认 glob 被放宽了"
        assert 'glob("*.md")' not in src

        ap = argparse.ArgumentParser()
        ap.add_argument("--glob", default="A*_*.md")
        assert ap.parse_args([]).glob == "A*_*.md"


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


class TestRevisionDrift:
    """⛔ 回归：判据粒度决定能不能看见 drift。

    ⚠️ **真实事故**：初版只用全字段逐字节哈希，⛔ 得抵消率 **1.0%**，⭐ 于是判
    「外部文献那条 drift 假设在我们数据上不成立」。⛔⛔ **那是假阴性** ——
    ⭐ 换到 `expression` 粒度是 **35.8%**、⭐ 换到谓词名粒度是 **43.7%**。

    ⭐ 根因：⛔ 4519 次编辑里 3106 次（69%）**只改散文字段**，⭐ 任何措辞变化都让
    全字段哈希不同，⛔ 于是「回到旧值」几乎不可能发生。

    ⭐⭐ **判据太严与太松同样危险** —— ⛔ 前者把真信号判成不存在。
    """

    def test_three_grains_are_all_reported(self):
        from measure_revision_drift import _GRAINS  # noqa: PLC0415

        names = [n for n, _ in _GRAINS]
        assert names == ["全字段", "只 expression", "只谓词名"], "⛔ 三个粒度缺一不可"

    @pytest.mark.parametrize(
        "expr,want",
        [
            ("initial_target(composite='a', child='b')", "initial_target"),
            ("  occupancy_after( x )", "occupancy_after"),
            ("edge_declared(src='S1')", "edge_declared"),
            ("", ""),
            ("42 + 1", ""),
        ],
    )
    def test_predicate_extraction(self, expr, want):
        from measure_revision_drift import _pred  # noqa: PLC0415

        assert _pred({"expression": expr}) == want

    def test_prose_only_edit_invisible_at_expression_grain(self):
        """⭐ 只改 `rationale` 的编辑：⛔ 全字段看是「改了」，⭐ expression 粒度看是「没改」。"""
        from measure_revision_drift import _canon, _expr  # noqa: PLC0415

        a = {"assertion_id": "X", "expression": "f(1)", "rationale": "因为甲"}
        b = {"assertion_id": "X", "expression": "f(1)", "rationale": "因为乙"}
        assert _canon(a) != _canon(b)
        assert _expr(a) == _expr(b)

    def test_ordering_key_uses_two_numbers(self):
        """⛔ 排序必须按 (loop, seq) 两段数字。

        ⚠️ 只按文件名字符串排，⛔ 序号位数变化时会错序 —— ⭐ 而错序会让
        「改了又改回来」**凭空出现**（⛔ 假阳性），⭐ 与上面那个假阴性是一对。
        """
        from measure_revision_drift import _IDX  # noqa: PLC0415

        m = _IDX.match("L000-000023-convert-assertions-state-update")
        assert m and (int(m.group(1)), int(m.group(2))) == (0, 23)
        assert sorted(["L000-000009-x", "L000-000100-x"], key=lambda s: tuple(int(g) for g in _IDX.match(s).groups())) == [
            "L000-000009-x",
            "L000-000100-x",
        ]

    def test_volatile_fields_excluded(self):
        """⛔ `revision` 每轮必变，⭐ 参与比较会让所有断言都显得改过。"""
        from measure_revision_drift import _VOLATILE, _canon  # noqa: PLC0415

        assert "revision" in _VOLATILE
        assert _canon({"expression": "f(1)", "revision": 1}) == _canon({"expression": "f(1)", "revision": 5})


class TestShellDetection:
    def test_source_extensions_catch_the_second_shell_kind(self):
        """⛔ 第二种空壳：⭐ **有一堆文件，⛔ 但一行源码都没有**。

        ⚠️ **真实事故**：某论文仓库 25 个 blob、⭐ 其中 24 个「非文档」，⛔ 于是初版
        工具判 🟢 —— ⭐ 但那 24 个**全是 PDF 报告与 CSV**，⛔ `.py` / `.ipynb` / `.sh`
        一个都没有。⭐ 论文自称公开了实验代码，⛔ 公开的其实是**实验产物**。

        ⭐ 第一种空壳（只剩 README）好认；⛔ **这第二种在任何「文件数」指标上都健康。**
        """
        from verify_assets import _DOC_ONLY, _SOURCE_EXT  # noqa: PLC0415

        for ext in (".py", ".ipynb", ".sh", ".java", ".cpp"):
            assert ext in _SOURCE_EXT
        #: ⛔ 产物类后缀绝不能算源码
        for ext in (".pdf", ".csv", ".png", ".xlsx", ".json", ".xml"):
            assert ext not in _SOURCE_EXT
        #: ⭐ 两个集合不相交 —— ⛔ 否则同一个文件会被两边计数
        assert not (_DOC_ONLY & _SOURCE_EXT)

    def test_doc_extensions_cover_the_flowfsm_case(self):
        """⭐ FlowFSM 空壳只含 `README.md` 与 `.gitignore` —— 两者都必须算文档。

        ⛔ 这是**真实事故的回归**：`baselines/` 2026-06-10 人工核验发现该仓库返回 200
        且存在，⛔ 但没有任何源码。⭐ 若 `.gitignore` 不在文档集里，它会被算成
        「非文档文件」，于是空壳判据失效、误判 🟢。
        """
        assert ".md" in _DOC_ONLY
        assert ".gitignore" in _DOC_ONLY


# --------------------------------------------------------------------------- #
# model_recency：⭐ 代际测量
# --------------------------------------------------------------------------- #

def test_recency_longest_match_wins():
    """⛔⛔ `GPT-4` 是 `GPT-4o` / `GPT-4.1` 的前缀 —— 若朴素匹配，新模型会被记成 2023-03。"""
    from tools.model_recency import scan
    assert scan("we use GPT-4o-mini for all runs") == {"gpt-4o-mini": 1}
    assert scan("GPT-4.1 Mini with temperature 0") == {"gpt-4.1-mini": 1}
    assert scan("the GPT-4 technical report") == {"gpt-4": 1}
    assert scan("GPT-4, GPT-4o, and GPT-4.1") == {"gpt-4": 1, "gpt-4o": 1, "gpt-4.1": 1}


def test_recency_boundary_is_not_word_boundary():
    """⛔ `\\b` 把 `.` 当边界，会让 `gpt-4` 在 `gpt-4.1` 里命中。这里钉住它不会。"""
    from tools.model_recency import scan
    assert "gpt-4" not in scan("gpt-4.1-nano")
    assert "claude-3-haiku" not in scan("Claude 3.5 Sonnet")
    assert "deepseek-v3" not in scan("DeepSeek-V3.1 Terminus")
    assert "llama-3-1" not in scan("Llama 3.3 70B")


def test_recency_drops_our_own_arm():
    """⛔⛔ 我方型号出现在每张卡的「与我们对比」节 —— ⭐ 不剔会把旧证据洗成同代。"""
    from tools.model_recency import scan
    text = "本篇用 gpt-3.5-turbo；而我们主臂是 gpt-5.5 与 claude-opus-4-7"
    assert scan(text) == {"gpt-3.5-turbo": 1}
    assert scan(text, drop_ours=False)["gpt-5.5"] == 1


def test_recency_tier_boundaries():
    from tools.model_recency import _tier
    assert _tier(0) == "A 同代" and _tier(6) == "A 同代"
    assert _tier(7) == "B 近一代" and _tier(16) == "B 近一代"
    assert _tier(17) == "C 隔代" and _tier(28) == "C 隔代"
    assert _tier(29) == "D 两代以上" and _tier(37) == "D 两代以上"


def test_recency_reference_point_is_earlier_arm_model():
    """⭐ 参照点取主臂较早者，⛔ 使代际差不被高估。"""
    from tools.model_recency import _REF, _months_behind
    assert (_REF.year, _REF.month) == (2026, 4)
    assert _months_behind("gpt-3.5-turbo") == 37
    assert _months_behind("gpt-5.1") == 5


# ---------------------------------------------------------------------------
# 口径迁移检查器 —— ⭐ 三条钉的都是本轮**实际踩到**的陷阱
# ---------------------------------------------------------------------------


def test_migration_exemption_is_root_invariant():
    """⛔⛔ 同一份文件在两种扫根下必须同判。

    ⭐ 本脚本支持从 `neighborhood/` 也从 `paper_stm_issue_discover/` 扫。
    ⛔ 首版只做前缀匹配，于是 `cards/x.md` 被豁免、
    `related_work/neighborhood/cards/x.md` **没有** —— ⭐ 换个根就换个结论。
    ⭐ 判据：豁免必须只由「文件是谁」决定，⛔ 不由「从哪扫」决定。
    """
    from tools.check_criteria_migration import _is_exempt

    short = _is_exempt("cards/atlas-layered-constraints.md")
    long = _is_exempt("related_work/neighborhood/cards/atlas-layered-constraints.md")
    assert short is not None and short == long
    # ⭐ 边界限定：`cards/**` ⛔ 不得误命中 `flashcards/`
    assert _is_exempt("flashcards/y.md") is None


def test_migration_exempts_every_preregistration_variant():
    """⛔⛔ 事前登记一份都不许漏 —— ⭐ 漏了会指使人去改事前登记。

    ⭐ 按仓库 `CLAUDE.md` §3.5.1，事前登记的全部价值来自「写在看到结果之前」，
    ⛔ 就地改写会毁掉证据链。⚠️ 实测仓库里有三种命名，⛔ 只挂精确名会漏两种。
    """
    from tools.check_criteria_migration import _is_exempt

    for name in (
        "baseline_arm/preregistered.md",
        "baseline_arm/preregistered_actionability.md",
        "discover_matrix/docs/generations/v21/preregistered_calibre.md",
        "discover_matrix/v46/preregistered.md",
    ):
        why = _is_exempt(name)
        assert why is not None, name
        assert "写在看到结果之前" in why, name


def test_migration_section_flag_does_not_leak_across_files():
    """⛔⛔ 这条钉的是一个**统计口径**错误，⭐ 不是代码风格问题。

    ⭐ 用 **一次** ``awk '/^## E\\./{e=1} /^## F\\./{e=0} e && /标志物/' cards/*.md``
    统计时，``e`` 跨文件不重置 —— ⛔ 某卡缺 ``## F.`` 就会让后续所有文件被算进 §E。
    ⭐⭐ 本轨首次统计因此得 **62**，逐文件重跑后是 **63**。
    ⭐ 判据：一份没有 §E 的文本，其 §E 命中必须是 0，⛔ 与上一次调用无关。
    """
    from tools.check_criteria_migration import iter_section_hits

    with_e = "## E. 意义\n我们的 19 条谓词如何\n"          # ⭐ 有 §E 且不闭合（无 §F）
    without_e = "## A. 元信息\n我们的 19 条谓词如何\n"     # ⛔ 无 §E

    assert len(iter_section_hits(with_e, "E")) == 1
    # ⭐ 紧接着调用一份无 §E 的文本 —— ⛔ 若 flag 泄漏，这里会是 1
    assert iter_section_hits(without_e, "E") == []
    # ⭐ 反向再确认一次，⛔ 排除「恰好顺序对了」
    assert iter_section_hits(with_e, "E") != []


def test_migration_counts_lines_not_occurrences():
    """⛔ 计数单位必须是**行**。

    ⭐ 出现次数会聚集在少数行上 —— ⛔ 本轨曾按次数报「53 处」，
    ⭐ 而那实际只有 27 行，读起来像 53 个独立地点。⭐ 行数才是迁移工作量。
    """
    from tools.check_criteria_migration import scan_text

    one_line_many_hits = "hit@1 与 hit@3 与 hit@all 三口径\n"
    counts = scan_text(one_line_many_hits)
    assert sum(counts.values()) == 1, counts
