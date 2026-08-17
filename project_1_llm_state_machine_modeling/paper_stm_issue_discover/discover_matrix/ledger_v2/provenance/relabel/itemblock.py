"""**唯一**的条目渲染器 —— 台账与候选全部走这一条路。

⚠️⚠️ **2026-08-14 重构：此前四类条目各有一套版式，⛔ 读者根本看不出在说什么。**

拆掉的东西（用户裁定「无关内容不要弄」）：

| 拆掉的 | 为什么 |
| :-- | :-- |
| **来源标注**（`§3.1 真漏记` / `§3.2 未采纳的 diff` / `§3.6 inspect 确定性发现`） | ⛔ 「这条是 inspect 还是 diff 报的」不影响它成不成立 |
| 台账侧的 `参考侧` / `生成侧` 两行 | ⚠️ 与 `问题描述` 重复，且用的是流水线内部术语 |
| **自动风险标记** | ⛔ 打了标记不等于不成立、没打不等于成立 —— 它只制造噪音 |
| 座标映射块的整段 caveat（三行免责声明） | ⭐ 压成 `问题类型` 一行，caveat 收进本节导语印一次 |
| `inspect` 补充证据折叠区 · 底层诊断表 · `diag_indices` | ⛔ 工具内部细节，判读者不需要 |
| 三臂原话的折叠区 | ⭐ 已并入判定表格的「理由」列 |

⭐ **现行版式，四段，顺序固定，所有条目一致：**

    ### <ID> <emoji>
    **问题类型**：<五轴座标，中英双写>
    **问题描述**：<一段话，说清这条主张的是什么>
    | 判读者 | 判定 | 理由 |     ← 三方逐字原话
    **meta review**（人工归纳）  ← 推荐 / 理由 / 分歧点 / 重点关注
    ~~~ 裁决填写区 ~~~

⛔ 顺序不许改：判读者要先知道**这是什么问题**，再看三方怎么判，再看我方推荐，最后才动笔。
⚠️ 把填写区放在最后是刻意的 —— 它是终点，不是入口。
"""
import re

import newfields as NF
import terms as T

#: PlantUML 的 `[*]` 伪态记号，⛔ 裸写进 Markdown 会被解析成链接语法。
#: ⭐ 只匹配**紧跟左括号**的裸 `[*]` —— 那才是会被 Markdown 解析成链接的形态。
#: ⛔ 早先写成「一切裸 `[*]`」，⚠️ 结果把 `[*] --> FinalState` 也改成 `` `[*]` --> ``，
#: 于是「渲染结果与 audit json 逐字一致」那道对拍失效 —— ⭐ 精确到真有害的那一种。
_RE_BARE_STAR = re.compile(r"(?<!`)\[\*\](?=\s*\()")


def safe_md(text):
    r"""把一段上游文字变成**渲染安全**的 Markdown 行内文本。

    ⛔⛔ **这个函数存在的理由是一个真渲染 bug，不是洁癖。** 上游文字里常出现 PlantUML 的
    `[*]` 伪态记号，⚠️ 而只要它后面紧跟一个括号，Markdown 就把 `[*](...)` 解析成**链接** ——
    实测 `nl_0004/0034.md` 里 `源内两处 [*] 边是 line 11、line 25` 后面接了 `(line 11/25)`，
    ⛔ 渲染出来是一个标签为 `*` 的死链，而链接检查器也确实把它报成死链。

    ⭐ 修法是给裸 `[*]` 包反引号（已包的不动）。⛔ 不许改上游原文 —— 那是判读者的逐字原话。
    """
    return _RE_BARE_STAR.sub("`[*]`", str(text or ""))


#: 五轴的渲染顺序。⭐ `defect_logic_kind` 与 `defect_element`/`qualifier` 是条件式互斥分支，
#: ⛔ 故只印实际有值的那些，不留空格子。
AXES = ("defect_locus", "defect_element", "defect_qualifier",
        "defect_logic_kind", "defect_reference")


def kind_line(mapping):
    """`问题类型` 一到三行。

    ⚠️⚠️ **2026-08-15 由「全塞一行」改成分行。** 原先把五轴 + 界外提示 + `other` 说明 +
    逐字依据串成一行，⛔ 实测那一行能到 400+ 字，读者根本找不到自己要的那一段。
    ⭐ 现在：第一行只放**五轴**（一眼可扫），后续每样各占一行。

    映射不上时印卡点类别与理由原话 —— ⚠️ 判读者需要知道「这一条我方也没归类出来」，
    ⭐ 那本身就是要他重点看的信号；⛔ 理由不许截断（它是唯一说明卡点的地方）。
    """
    if not mapping:
        return ["**问题类型**：（尚无归类记录）"]
    if not mapping.get("mappable"):
        blocker = mapping.get("blocker")
        import candidate_mapping as CM
        zh = CM.BLOCKER_ZH.get(blocker)
        head = f"**问题类型**：⚠️ **我方未能归类**（卡点：{zh[0]}）" if zh \
            else "**问题类型**：⚠️ **我方未能归类**"
        out = [head]
        note = safe_md((mapping.get("note") or "").replace("\n", " ").strip())
        if note:
            out.append(f"- 卡点理由：{note}")
        if zh:
            out.append(f"- 这类卡点的含义：{zh[1]}")
        return out
    bits, out_of_scope = [], []
    for axis in AXES:
        val = mapping.get(axis)
        if not val:
            continue
        bits.append(T.bi(val, NF.ZH[axis].get(val)))
        if not NF.counts_as_defect(axis, val):
            out_of_scope.append((axis, val))
    out = ["**问题类型**：" + (" · ".join(bits) if bits else "（未归类）")]
    # ⭐ 界外取值必须当场写明它不计分 —— ⛔ 只印一个 `region` 而不说它不计入统计，
    # 判读者会把它当成一条普通缺陷，⛔ 而那正是 CLAUDE.md 边界禁止的两种误读之一。
    for axis, val in out_of_scope:
        out.append(f"- ⚠️ **`{val}` 是界外取值、不计分**："
                   f"{NF.OUT_OF_SCOPE_VALUES[(axis, val)]}")
    if (mapping.get(NF.OTHER_NOTE_FIELD) or "").strip():
        out.append(f"- `other` 说明：{safe_md(mapping[NF.OTHER_NOTE_FIELD].strip())}")
    # ⭐ 归类所依据的**原文逐字片段**必须跟着印 —— ⛔ 只给结论不给依据，
    # ⚠️ 判读者无法判断我方是不是读错了那一句，而「我方可能读错」正是要他复核的东西。
    ev = (mapping.get("evidence") or "").replace("\n", " ").strip()
    if ev:
        out.append(f"- 归类依据（原文逐字）：{safe_md(ev)}")
    return out


#: 本节导语里那句共用说明。⭐ 印在 §2 / §3 各一次，⛔ 不逐条重复。
SECTION_NOTE = ("每条的版式一致：**问题类型 → 问题描述 → 三方判定 → meta review → 裁决区**。"
                "标记：✅ 已定采纳 · ❌ 已定不采纳 · ❓ 三臂一致判两读并立（这三种不需你动）· "
                "🟡 两读并立待你选 · 🟠 有偏向待你认可 · 🔴 三方无偏向待你亲裁。"
                "⚠️ `问题类型` 是我方读该条正文后自己判的，**不是已经定下来的事实**；候选侧还多一层：它映射的是「若这条线索成立属于哪一格」，**不代表它成立**。**你的裁决优先**"
                f"（完整口径见 [{'HOWTO.md'}](../HOWTO.md) §D.2）。")


def render(key, desc, mapping, saved, fb, DT, kind="candidate", extra=()):
    """一条条目的完整块。⭐ 四段固定顺序，⛔ 所有条目一致。

    `desc` 是问题描述（已成句的一段话）；`mapping` 是五轴座标记录（可为 `None`）；
    `extra` 是紧跟描述之后的补充行（`UM-` 的逐条说法、并入本条的补充证据）。
    """
    out = [f"### {key}{DT.mark(key)}", ""]
    out.extend(kind_line(mapping))
    out.append("")
    out.append("**问题描述**：" + (desc or "（本条无描述文本）").replace("\n", " ").strip())
    out.append("")
    for ln in extra:
        out.append(ln)
    if extra:
        out.append("")
    out.extend(DT.verdict_table(key))
    out.extend(DT.meta_block(key))
    out.append(fb.render(key, kind, DT.prefill(key, kind) or fb.LEDGER_TEMPLATE,
                         saved.get(key)))
    out.append("")
    return out
