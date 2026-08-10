"""comment 的结构本身是纪律，所以按结构断言，不按措辞。

上一代次是单表 34 行。字段没问题，问题是**任何单表都会把行数当成分母** —— 读者的默认阅读是
「表里有多少行就有多少条被度量」，而 v22 的可报记录只有 3 条，其余 30 条是共演化观测，照常
报出但不构成主张。一张 33 行的表加一句脚注解决不了：脚注会被跳过，表头不会。
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import build_comment as bc  # noqa: E402
import metrics_at_k as mk  # noqa: E402


def _full_verdicts(pattern=(1, 0, 1)) -> dict:
    """完整判定表。可报记录的命中带方向形态 —— 否则 `validate` 会拒，而它拒得对。

    这条 fixture 在方向校验落地时立刻转红，五个断言一起。那不是校验过严，是 fixture 少了一个
    判定者本来就必须提供的字段：一条判为命中却说不出按哪种形态成立的记录，正是判反最常见的样子。
    """

    # ⚠️ 分母是 `REPORTABLE`（99 条），不是台账全部（126 条）。差的 27 条是 `00x8` 的 NL 越界
    # 记录：那份 NL 要求 fork/join 与秒级时间约束，忠实模型在 M 中无法表示，v35 起先验不进网格。
    # 把它们放进判定表会被 `validate` 判为「网格被改错」—— 而那条检查是对的，见
    # NL_SCOPE_RULE.md §五。v23/v24 的历史判定表确实含 `00x8`（那两代跑过），
    # 但本 fixture 模拟的是**当前**口径。
    verdicts: dict[str, object] = {}
    for record_id in sorted(mk.REPORTABLE):
        entry: dict[str, object] = {"claude": list(pattern)}
        if 1 in pattern:
            entry["direction"] = {"claude": "direct"}
        verdicts[record_id] = entry
    return {"verdicts": verdicts, "over": {}}


def _rendered() -> str:
    return bc.render(_full_verdicts(), "v22", 3)


def test_ratios_appear_only_in_the_capability_band() -> None:
    """给了比率它就会被引用，所以共演化的两节一个都不给。"""
    text = _rendered()
    sections = text.split("\n## ")
    with_ratio = [s.split("\n", 1)[0] for s in sections if "hit@1" in s]
    assert len(with_ratio) == 1, with_ratio
    assert "可报告记录" in with_ratio[0]


def test_the_header_carries_no_fraction_over_the_full_ledger() -> None:
    """头部速览不得出现 `n/33`，那正是把共演化条目算进分母的写法。"""
    header = _rendered().split("\n## ", 1)[0]
    import re

    fractions = re.findall(r"\d+\s*/\s*\d+", header)
    assert not fractions, fractions


def test_the_threshold_table_is_a_real_table() -> None:
    """分层可报条目表必须实体存在。

    hold-out 移除前它恒为空（可报记录只有 3 条，四层全部不达阈值），当时"空本身是结论"。
    现在全部 126 条记录同等参与度量，四层都达阈值 —— 表不再为空，但它**仍必须是一张实体表**：
    分层条目数是读者判断"某层的比率能不能单独引用"的唯一依据，写成脚注会被跳过。
    """

    rendered = _rendered()
    assert "## 达阈值的层" in rendered
    for layer in bc.LAYERS:
        assert f"| {layer} |" in rendered, layer
    assert "不设 hold-out" in rendered


def test_the_band_holds_every_reportable_record() -> None:
    """能力那一节必须装下**全部**可报告记录，且**只**装它们。

    两个方向都要锁：少一条是「更改分母」，多一条是把已被边界裁定剔除的记录混进能力主张。
    后者曾真实发生——度量按判定表里出现的全部 id 算，报出 366/594，而全部文档报 360/588。
    """
    text = _rendered()
    band = text.split("## 可报告记录", 1)[1].split("\n## ", 1)[0]
    for record_id in mk.REPORTABLE:
        assert record_id in band, record_id
    for record_id in sorted(mk._ledger_ids()):
        if record_id in mk.REPORTABLE:
            continue
        assert record_id not in band, record_id


def test_a_blocked_record_is_flagged_where_it_is_read() -> None:
    """在它自己那一行，不是只在文末。读者是逐行读表的。"""
    text = _rendered()
    for record_id, why in mk.BLOCKED.items():
        if record_id not in mk.REPORTABLE:
            continue
        line = next(l for l in text.splitlines() if l.startswith(f"| {record_id}"))
        assert "⚠️" in line and why[:8] in line, line


def test_it_refuses_to_render_an_invalid_verdict_table() -> None:
    """渲染出来的表会被引用，而它的分母是错的 —— 所以不渲染。"""
    incomplete = {"verdicts": {"EIS-0035-02": [1, 1, 1]}, "over": {}}
    with pytest.raises(SystemExit) as caught:
        bc.render(incomplete, "v22", 3)
    # 措辞 2026-08-10 起改为「范围内记录缺」，因为旧措辞「可报记录缺 …… 即剔除不利样本」
    # 会让读者把 `00x8` 的先验越界读成分母被篡改 —— 已实际造成一次误启动。
    assert "范围内记录缺" in str(caught.value)


def test_the_brief_does_not_cut_mid_clause() -> None:
    """截断线切掉台账自己的结论子句是有前科的，见 present_for_judgment 的 --full。"""
    ledger = bc._ledger()
    for record_id in mk.REPORTABLE:
        brief = bc._brief(ledger[record_id])
        assert brief, record_id
        # 要么完整到句读，要么显式带省略号 —— 不能静默半句。
        assert brief.endswith("…") or not str(ledger[record_id]["statement"]).startswith(
            brief + "的"
        ), brief


def test_a_hit_must_state_how_the_identity_holds() -> None:
    """防判反的机械检查点。

    上一代次有两条模型产出触及了正确的元素、却得出与台账**相反**的结论，而唯一的防线（并列
    呈现）当时在真实路径上输出零行。要求填形态的作用不是记录，是**强制做一次方向比对** ——
    填不出 `HIT_CRITERION.md` §3 四种形态里的哪一种，就说明没做过那次比对。
    """
    verdicts = {rid: {"claude": [1, 0, 1]} for rid in sorted(mk._ledger_ids())}
    problems = mk.validate({"": None} and verdicts, {}, 3)
    complained = [p for p in problems if "方向形态" in p]
    assert len(complained) == len(mk.REPORTABLE), problems


def test_only_the_capability_band_is_asked_for_a_direction() -> None:
    """共演化带三十条逐条填形态的成本，换不来能被引用的结论。"""
    verdicts = {rid: {"claude": [1, 0, 1]} for rid in sorted(mk._ledger_ids())}
    for rid in mk.REPORTABLE:
        verdicts[rid]["direction"] = {"claude": "direct"}
    assert not [p for p in mk.validate(verdicts, {}, 3) if "方向形态" in p]


def test_an_unknown_direction_form_is_refused() -> None:
    """四种形态来自 HIT_CRITERION.md §3，自由文本会让这个字段退化成摆设。"""
    verdicts = {rid: {"claude": [1, 0, 1]} for rid in sorted(mk._ledger_ids())}
    for rid in mk.REPORTABLE:
        verdicts[rid]["direction"] = {"claude": "差不多吧"}
    assert [p for p in mk.validate(verdicts, {}, 3) if "不在 HIT_CRITERION" in p]


def test_a_miss_needs_no_direction() -> None:
    """未命中没有「按哪种形态成立」可言，强制它填等于制造噪声。"""
    verdicts = {rid: {"claude": [0, 0, 0]} for rid in sorted(mk._ledger_ids())}
    assert not [p for p in mk.validate(verdicts, {}, 3) if "方向形态" in p]
