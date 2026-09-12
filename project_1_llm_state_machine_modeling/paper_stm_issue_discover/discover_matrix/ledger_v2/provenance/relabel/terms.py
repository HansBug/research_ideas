"""术语英中对照 —— ⭐ 工作单「自包含」的唯一真源。

为什么要有这一份
----------------
工作单是给**人**填的。⛔ 而它此前把字段的值直接印成裸英文标识符，判据则写成
「见 HOWTO.md §D.4」——⚠️ 于是判读者要填一张表得先翻两个文件，
⛔ 而最需要判据的那一栏恰恰是跳转最远的那一栏。

⛔ **每一条中文都必须能指到仓库里的出处（文件 + 行号），⛔ 指不到的一律标「仓库未定义」。**
⚠️ 这不是格式洁癖：中文名一旦是编的，判读者就会按编出来的语义去判，
⛔ 而那个语义与字段的真实定义之间的偏差**不会有任何报错**。

2026-08-13：本文件瘦身近八成
----------------------------
工作单 §2 此前把台账既有条目的十项元数据（`layer` / `direction` / `element_of_M` /
`decided_by` / `primary_predicate` / `nl_evidence` / `verdict` / `replay` / 同质组 /
上游）连同整节断言组一并印出来，本文件的大半篇幅就是为**那些展示值**准备的中英对照。

⛔ 那十项现在**不再呈现**，理由不是嫌长，是**锚定**：其中七项是我们自家框架给该条贴的
标签，⛔ 而本轮要判读者回答的恰恰是「这套框架有没有漏掉东西」；`verdict` / `replay`
更直接 —— ⛔ 它们是流水线的判定与复算结论，印出来等于先把标准答案给了判读者。

于是服务它们的常量与渲染 helper 整体删除：`LAYER_ZH` / `ELEMENT_ZH` / `DECIDED_BY_ZH` /
`VERDICT_ZH` / `REPLAY_ZH` / `ROLE_ZH` / `FAMILY_ZH` / `PREDICATE_ZH` /
`DIRECTION_MEANING` / `DIRECTION_ZH` / `DIRECTION_WHAT` / `FIELD_ZH`，以及
`layer_cell` / `direction_cell` / `element_cell` / `decided_by_cell` /
`predicate_cell` / `verdict_cell` / `role_label` / `family_label`。
⛔ **留一个不用的常量比删干净更糟**：它会让下一个人以为那一栏还印着，
⛔ 也会让「这些字段已经不呈现了」这条纪律失去机械保障
（[test_relabel.py](./test_relabel.py) 的 `test_the_stripped_ledger_metadata_is_gone_everywhere` 钉住）。

⭐ 剩下的两样都还在用：`SEG_MODE_ZH` 服务 §1.1 的 NL 分段口径说明，
`bi()` 服务 §2 / §3 的座标映射块（[newfields.py](./newfields.py) 的 `ZH` 给中文名）。
"""

from __future__ import annotations

#: NL 分段口径。⭐ 出处：`sources.nl_segments()` 的两个返回值（`sources.py:194` 与 `:202`）。
SEG_MODE_ZH = {
    "manual_override": ("人工标注分段",
                        "该份规约的编号无法机器判定，分段取自 "
                        "`corpora/nl_segmentation/overrides.json` 的人工标注"),
    "line_split": ("按物理行切", "按物理行切分，与 pipeline 同口径"),
}


def bi(term, zh):
    """⭐ 渲染成 `` `term`（中文） ``。⛔ zh 为空时只出英文，⛔ 不编中文。"""
    return f"`{term}`（{zh}）" if zh else f"`{term}`（该取值的中文名仓库未定义）"
