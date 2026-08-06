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
    return {
        "verdicts": {rid: list(pattern) for rid in sorted(mk._ledger_ids())},
        "over": {},
    }


def _rendered() -> str:
    return bc.render(_full_verdicts(), "v22", 3)


def test_ratios_appear_only_in_the_capability_band() -> None:
    """给了比率它就会被引用，所以共演化的两节一个都不给。"""
    text = _rendered()
    sections = text.split("\n## ")
    with_ratio = [s.split("\n", 1)[0] for s in sections if "hit@1" in s]
    assert len(with_ratio) == 1, with_ratio
    assert "能力主张" in with_ratio[0]


def test_the_header_carries_no_fraction_over_the_full_ledger() -> None:
    """头部速览不得出现 `n/33`，那正是把共演化条目算进分母的写法。"""
    header = _rendered().split("\n## ", 1)[0]
    import re

    fractions = re.findall(r"\d+\s*/\s*\d+", header)
    assert not fractions, fractions


def test_the_empty_threshold_table_is_a_real_table() -> None:
    """§9 的结论是「本代次不产出能力主张」。写着 0 的表能被看见，脚注会被跳过。"""
    text = _rendered()
    assert "## ⚠️ 达阈值的层" in text
    block = text.split("## ⚠️ 达阈值的层", 1)[1].split("\n## ", 1)[0]
    for layer in bc.LAYERS:
        assert f"| {layer} |" in block, layer
    assert block.count("| ✗ |") >= 1


def test_the_capability_band_holds_exactly_the_reportable_records() -> None:
    text = _rendered()
    band = text.split("## 能力主张", 1)[1].split("\n## ", 1)[0]
    for record_id in mk.REPORTABLE:
        assert record_id in band, record_id
    # 共演化条目不得混进这一节。
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
    assert "可报记录缺" in str(caught.value)


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
