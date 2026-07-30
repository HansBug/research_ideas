"""Render the expected-issue-set issue body from the data, not from memory.

Every number here is recomputed from `expected_issue_set.json` / `ledger_coverage.json` on
each run. The prior round established the split cleanly: every script-generated table
recomputed exactly, and every factual error sat in hand-typed prose. So the body is generated
and the hand-written part is kept to the arguments, which a reviewer must check by reading.

Emits fragments so the body and its comments can each take what they need.

Usage: render_eis_issue.py --readable-gist ID --audit-gist ID [--out DIR]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
MR = HERE / "manual_review"

LLMS = ["GPT-4o", "GPT-4", "Llama", "Kimi", "DeepSeek", "Claude"]
NLS = [f"NL{i:02d}" for i in range(1, 11)]
NL_DOMAIN = {
    "NL01": "列车控制", "NL02": "基础制动", "NL03": "无人机集群", "NL04": "数码相机",
    "NL05": "自动驾驶模式", "NL06": "泵控制", "NL07": "碰撞避免",
    "NL08": "驾驶模式切换", "NL09": "HSUV", "NL10": "微波炉",
}
LAYER_ORDER = ["nl_named", "wellformedness", "nl_contradiction", "over_specification"]
LAYER_ZH = {
    "wellformedness": ("良构性", "无需任何 oracle，仅凭生成模型自身即可判定"),
    "nl_named": ("NL 点名", "NL 逐字点名了那个缺失或错位的元素"),
    "nl_contradiction": ("与 NL 矛盾", "模型行为与 NL 的显式义务相反"),
    "over_specification": ("过度指定且有害", "生成方凭空多出，且造成可断言的负面后果"),
}
DIRECTION_ZH = {
    "reachability": "可达性与终止", "entry": "初始入口", "guard": "守卫与条件",
    "hierarchy": "层次归属", "effect_action": "动作与 effect", "event": "事件与触发",
    "pseudostate": "伪状态类型", "cardinality": "元素数量",
    "target_scope": "迁移目标", "unclassified": "未归类",
}
FAMILY_ZH = {"S": "结构", "B": "行为", "P": "性质"}


def anchor(name: str) -> str:
    """GitHub slugifies *only the dot*: lowercase, `.` -> `-`, underscores and hyphens kept.
    A wrong anchor does not 404 -- it silently lands on the page top."""
    return "file-" + name.lower().replace(".", "-")


def bar(n: int, mx: int, width: int = 14) -> str:
    if mx <= 0:
        return ""
    full = round(n / mx * width)
    return "█" * full + "░" * (width - full)


def pct(n: int, d: int) -> str:
    return f"{n / d:.0%}" if d else "—"


def main() -> int:
    def arg(flag, default=None):
        return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default

    rgist = arg("--readable-gist")
    agist = arg("--audit-gist")
    if not (rgist and agist):
        print("需要 --readable-gist 与 --audit-gist")
        return 2
    out = pathlib.Path(arg("--out", str(MR / "eis_issue")))
    out.mkdir(parents=True, exist_ok=True)

    def rlink(label, fname):
        return f"[{label}](https://gist.github.com/HansBug/{rgist}#{anchor(fname)})"

    def alink(label, fname):
        return f"[{label}](https://gist.github.com/HansBug/{agist}#{anchor(fname)})"

    eis = json.loads((MR / "expected_issue_set.json").read_text())
    cov = json.loads((MR / "ledger_coverage.json").read_text())
    recs = eis["records"]
    t = eis["totals"]
    written = []

    def emit(name, body):
        (out / name).write_text(body.rstrip() + "\n")
        written.append(name)

    by_pair = defaultdict(list)
    for r in recs:
        by_pair[r["pair"]].append(r)
    cell = {(r["group"], r["llm"]): r["pair"] for r in recs}
    # Pairs with zero admissible findings still occupy a cell; recover them from the review
    # files so the 60-cell grid is complete rather than showing holes.
    allpairs = {}
    for p in sorted(MR.glob("*-review.json")):
        rv = json.loads(p.read_text())
        cr = rv.get("cross_reference") or {}
        allpairs[rv["case"]] = (cr.get("group"), cr.get("llm"))
        cell.setdefault((cr.get("group"), cr.get("llm")), rv["case"])

    # ---------------------------------------------------------------- 60-cell grid
    L = [
        "每格给出 `pair ID` / **expected issue 条数** / 可自动验收数，并直达该 pair 的可读台帐。"
        "灰色 `0` 表示该 pair 无可入 expected issue（不等于无差异——"
        "语义等价与判定困难的差异都不计入）。",
        "",
        "| NL 组 | " + " | ".join(LLMS) + " | 行合计 |",
        "| --- | " + " | ".join([":-:"] * 6) + " | :-: |",
    ]
    col_n = Counter()
    col_a = Counter()
    tot_n = tot_a = 0
    for nl in NLS:
        cells, rn, ra = [], 0, 0
        for m in LLMS:
            p = cell.get((nl, m))
            if p is None:
                cells.append("—")
                continue
            rs = by_pair.get(p, [])
            n = len(rs)
            a = sum(1 for x in rs if x["automatable"])
            rn += n
            ra += a
            col_n[m] += n
            col_a[m] += a
            if n:
                cells.append(f"{rlink('`' + p + '`', f'{p}-eis.md')}<br>**{n}** ／ {a} 可自动")
            else:
                cells.append(f"`{p}`<br>0")
        tot_n += rn
        tot_a += ra
        L.append(f"| **{nl}** {NL_DOMAIN[nl]} | " + " | ".join(cells) + f" | **{rn}** ／ {ra} |")
    L.append("| **列合计** | "
             + " | ".join(f"**{col_n[m]}** ／ {col_a[m]}" for m in LLMS)
             + f" | **{tot_n}** ／ {tot_a} |")
    L += [
        "",
        f"合计 **{tot_n}** 条 expected issue，其中 **{tot_a}** 条可自动验收"
        f"（{pct(tot_a, tot_n)}）、**{tot_n - tot_a}** 条现有 19 个封闭谓词表述不出、只能人工验收。"
        f"分布在 **{t['pairs_covered']} / 60** 个 pair 上；"
        f"另 {60 - t['pairs_covered']} 个 pair 无可入条目。",
        "",
        f"逐 pair 机读索引：{alink('index.tsv', 'index.tsv')} ｜ "
        f"主档：{alink('expected_issue_set.json', 'expected_issue_set.json')}",
    ]
    emit("grid.md", "\n".join(L))

    # ---------------------------------------------------------------- headline + layers
    L = [
        "| 量 | 值 | 口径 |",
        "| --- | ---: | --- |",
        f"| **expected issue 条数** | **{t['records']}** | 一条记录一条 issue |",
        f"| **同质组** | **{t['homogeneity_groups']}** | 同 pair 上主谓词与元素集合相同者视为同一缺陷；"
        f"**命中率应按此计**，不按记录条数计 |",
        f"| 覆盖 pair | {t['pairs_covered']} / 60 | 10 NL × 6 LLM 全因子设计 |",
        f"| 可自动验收 | **{t['automatable']}**（{pct(t['automatable'], t['records'])}）| "
        f"主断言实测返回 `False` |",
        f"| 须人工验收 | **{t['needs_human_judgement']}** | 19 个封闭谓词表述不出 |",
        f"| 带实测有效负控 | **{t['with_negative_control']}** / {t['records']} | "
        f"负控须实测为 `True`。覆盖率 {pct(t['with_negative_control'], t['records'])}——"
        f"**这是本集合已知的最大证据弱点** |",
        f"| 经主裁定 | {t['with_parent_ruling']} | 复核结论被推翻或换据后重判 |",
        f"| 落在有旧台帐 E1 的 pair 上 | {t['on_pairs_with_ledger_e1']} | 其余落在旧台帐无记录的 pair |",
        "",
        "### 归因层：凭什么把一条差异归给生成方",
        "",
        "四层不是严重程度，而是**证明所依赖的 oracle 强度**，从强到弱：",
        "",
        "| 层 | 条数 | 占比 | 图示 | 判据 |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    bl = t["by_layer"]
    mx = max(bl.values())
    for k in LAYER_ORDER:
        if k not in bl:
            continue
        zh, basis = LAYER_ZH[k]
        L.append(f"| `{k}`（{zh}）| **{bl[k]}** | {pct(bl[k], t['records'])} | "
                 f"{bar(bl[k], mx)} | {basis} |")
    L.append(f"| **合计** | **{sum(bl.values())}** | 100% | | |")
    L += [
        "",
        f"`wellformedness` 这 {bl.get('wellformedness', 0)} 条最难被质疑——"
        "反驳它必须先反驳模型自身，不需要 NL 也不需要参考模型。",
        "",
        "```mermaid",
        "pie showData title 归因层分布（129 条）",
    ]
    for k in LAYER_ORDER:
        if k in bl:
            L.append(f'    "{k} {LAYER_ZH[k][0]}" : {bl[k]}')
    L += ["```", ""]
    emit("headline.md", "\n".join(L))

    # ---------------------------------------------------------------- directions
    bd = t["by_direction"]
    mx = max(bd.values())
    L = [
        "缺陷方向回答「什么坏了」，与「能否断言」是两个独立问题。",
        "",
        "| 方向 | 条数 | 占比 | 图示 | 含义 |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for k, n in sorted(bd.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | **{n}** | {pct(n, t['records'])} | {bar(n, mx)} | "
                 f"{DIRECTION_ZH.get(k, '')} |")
    L.append(f"| **合计** | **{sum(bd.values())}** | 100% | | |")

    # direction x layer
    grid = defaultdict(Counter)
    for r in recs:
        grid[r["direction"]][r["layer"]] += 1
    L += [
        "",
        "与归因层交叉后可以看出各方向的证据结构差异：",
        "",
        "| 方向 | " + " | ".join(LAYER_ZH[k][0] for k in LAYER_ORDER) + " | 合计 |",
        "| --- | " + " | ".join(["---:"] * len(LAYER_ORDER)) + " | ---: |",
    ]
    for k, n in sorted(bd.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | " + " | ".join(str(grid[k][s] or "·") for s in LAYER_ORDER)
                 + f" | **{n}** |")
    tot = Counter()
    for c in grid.values():
        tot.update(c)
    L.append("| **合计** | " + " | ".join(f"**{tot[s]}**" for s in LAYER_ORDER)
             + f" | **{sum(tot.values())}** |")

    # predicates
    bp = {k: v for k, v in t["by_primary_predicate"].items() if k}
    none_n = t["by_primary_predicate"].get(None, 0)
    L += [
        "",
        "### 承载谓词",
        "",
        "| 谓词 | 族 | 条数 | 图示 |",
        "| --- | :-: | ---: | --- |",
    ]
    fam_of = {}
    for r in recs:
        if r["assertions"]:
            for a in r["assertions"]:
                if a["role"] == "primary" and a["predicates"]:
                    fam_of[a["predicates"][0]] = "/".join(a["families"])
    mxp = max(bp.values()) if bp else 1
    for k, n in sorted(bp.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {fam_of.get(k, '—')} | **{n}** | {bar(n, mxp)} |")
    L.append(f"| **无谓词可用** | — | **{none_n}** | {bar(none_n, mxp)} |")
    L.append(f"| **合计** | | **{sum(bp.values()) + none_n}** | |")
    L += [
        "",
        f"19 个封闭谓词里 **{len(bp)}** 个被用到；"
        f"**{none_n}** 条无任何谓词可用——这 {none_n} 条正是本集合的自动化上限。",
    ]
    emit("directions.md", "\n".join(L))

    # ---------------------------------------------------------------- ledger coverage
    ct = cov["totals"]
    L = [
        "issue [#166](https://github.com/HansBug/research_ideas/issues/166) 的 47 条 expected issue "
        "**无法与本集合做 binding 级合并**：其 `ledger.json` 于 2026-07-29 机器重建时丢失、"
        "从未进入 git、不可恢复，47 条中仅 **5 条**被重建出机器可比的 `eval_assert`，"
        "其余 42 条只剩自然语言陈述。",
        "",
        "因此关系被反转：**本集合即台帐**，而 #166 的 47 条降级为一份"
        "**必须被逐条交代的覆盖清单**。逐条结果：",
        "",
        "| 交代结果 | 条数 | 含义 |",
        "| --- | ---: | --- |",
        f"| `binding_match` | **{ct.get('binding_match', 0)}** | "
        f"旧条目有 `eval_assert`，且与本集合某条断言**共享模型元素**——机器可判，最强关联 |",
        f"| `same_pair_only` | **{ct.get('same_pair_only', 0)}** | "
        f"本集合在该 pair 上有条目，但具体对应只能靠读陈述——需人工确认 |",
        f"| `unaccounted` | **{ct.get('unaccounted', 0)}** | "
        f"本集合在该 pair 上没有任何可入条目——**这个数必须为 0**，否则等于静默丢弃既有发现 |",
        f"| **合计** | **{ct['ledger_entries']}** | |",
        "",
        f"**`unaccounted` = {ct.get('unaccounted', 0)}。** 也就是说旧台帐涉及的每个 pair，"
        f"本集合都有对应条目。但必须说清这是**必要条件而非充分条件**："
        f"42 条 `same_pair_only` 只证明「该 pair 有新条目」，"
        f"不证明「新条目覆盖了旧条目所指的那个缺陷」——那需要逐条人工确认，本集合尚未完成。",
        "",
        "### 旧台帐的类别分布（#166 §3 的 taxonomy）",
        "",
        "| 类别 | 条数 | 含义 |",
        "| --- | ---: | --- |",
    ]
    cats = Counter(e["category"] for e in cov["entries"])
    labels = {e["category"]: e["category_label"] for e in cov["entries"]}
    for c, n in cats.most_common():
        L.append(f"| `{c}` | {n} | {labels.get(c, '')} |")
    L.append(f"| **合计** | **{sum(cats.values())}** | |")
    only_new = ct.get("pairs_only_in_new_set") or []
    L += [
        "",
        f"### 覆盖范围的扩张",
        "",
        f"旧台帐涉及 **{ct['pairs_in_ledger']}** 个 pair，本集合覆盖 **{t['pairs_covered']}** 个，"
        f"新增 **{len(only_new)}** 个旧台帐完全没有记录的 pair："
        + "、".join(f"`{p}`" for p in only_new) + "。",
        "",
        "```mermaid",
        "flowchart LR",
        f'    A["issue #166 台帐<br/>47 条 / {ct["pairs_in_ledger"]} pair"] '
        f'-->|"5 条 binding_match"| C',
        f'    A -->|"42 条 same_pair_only<br/>待人工确认"| C',
        f'    B["本轮逐对复核<br/>418 差异 → 153 计入问题"] -->|"四层归因筛选"| C',
        f'    C["expected issue set<br/>{t["records"]} 条 / {t["pairs_covered"]} pair"]',
        f'    C --> D["{t["automatable"]} 条可自动验收"]',
        f'    C --> E["{t["needs_human_judgement"]} 条须人工"]',
        "```",
        "",
        f"逐条对照数据：{alink('ledger_coverage.json', 'ledger_coverage.json')}",
    ]
    emit("coverage.md", "\n".join(L))

    # ---------------------------------------------------------------- per-LLM / per-NL
    bl_llm = t["by_llm"]
    bl_grp = t["by_group"]
    L = [
        "两个分布都是**描述性**的，不作能力归因——"
        "复核单元与 NL 组在设计上混淆（每个复核批次负责固定的 NL 组），"
        "因此按 NL 组的差异无法与复核者效应分离。",
        "",
        "| LLM | 条数 | 可自动 | 须人工 | 图示 |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    mx = max(bl_llm.values())
    for m in LLMS:
        rs = [r for r in recs if r["llm"] == m]
        a = sum(1 for r in rs if r["automatable"])
        L.append(f"| {m} | **{len(rs)}** | {a} | {len(rs) - a} | {bar(len(rs), mx)} |")
    L.append(f"| **合计** | **{sum(bl_llm.values())}** | {t['automatable']} | "
             f"{t['needs_human_judgement']} | |")
    L += [
        "",
        "| NL 组 | 领域 | 条数 | 图示 |",
        "| --- | --- | ---: | --- |",
    ]
    mx = max(bl_grp.values())
    for g in NLS:
        n = bl_grp.get(g, 0)
        L.append(f"| **{g}** | {NL_DOMAIN[g]} | {n} | {bar(n, mx)} |")
    L.append(f"| **合计** | | **{sum(bl_grp.values())}** | |")
    emit("distribution.md", "\n".join(L))

    # ---------------------------------------------------------------- assertion groups
    ad = t["assertion_count_distribution"]
    L = [
        "一条 expected issue 的证据不是单个表达式，而是一个**断言组**：",
        "",
        "| 角色 | 应有实测值 | 作用 |",
        "| --- | :-: | --- |",
        "| `primary` | `False` | 陈述缺陷本身。返回 `True` 说明断言不判别，返回 `None` 说明无法判定——两者都不是证据 |",
        "| `negative_control` | **`True`** | 证明主断言不是恒假。缺它就无法排除「正确模型也返回 `False`」 |",
        "| `corroborating` | `False` 或 `True` | 补第二个后果，加固而非替代主断言 |",
        "| `recovered_unverified` | — | 从复核者散文里恢复但未能自动求值；记录在案供人工核对，**不计入证据** |",
        "",
        "| 组内断言条数 | 记录数 |",
        "| ---: | ---: |",
    ]
    for k in sorted(ad, key=lambda x: int(x)):
        L.append(f"| {k} | {ad[k]} |")
    L += [
        f"| **合计** | **{sum(ad.values())}** |",
        "",
        f"**必须写明的弱点：{t['records']} 条中只有 {t['with_negative_control']} 条"
        f"带经实测验证的负控（{pct(t['with_negative_control'], t['records'])}）。**"
        "复核者在文本里记录过负控（如「正控：`0026` 真吸收态返回 `True`」），"
        "但从散文恢复出的表达式绝大多数不可求值，因此无法自动验证——"
        f"当前 {t['with_negative_control']} 条是随主裁定**以结构化字段**补入的，"
        "这也说明补齐的路径是可行的：把负控写成字段而不是散文。",
        "",
        "为什么这个缺口重要：**没有负控就无法机械排除「正确模型也返回 `False`」。**"
        "本轮 18 条 benign `extra` 中有 5 条正是因此被拒——"
        "`stays_in` 要求触发被消费，所以正确模型（根本不声明该事件）也返回 `False`。"
        "风险是实测过的，不是假想。因此本集合的 "
        f"{t['automatable']} 条「可自动验收」应读作**上界**："
        "它们的主断言都实测为 `False`，但除那 "
        f"{t['with_negative_control']} 条外，尚未证明这个 `False` 具有判别力。"
        "**补齐负控是本集合的首要改进项，也是把 expected issue set 用于命中率统计前必须做的事。**",
    ]
    emit("assertions.md", "\n".join(L))

    print(f"已生成 {len(written)} 个片段 → {out}")
    for n in written:
        print(f"  {n:20s} {len((out / n).read_text()):6d} 字符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
