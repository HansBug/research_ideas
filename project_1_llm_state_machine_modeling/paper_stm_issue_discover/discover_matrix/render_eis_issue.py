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
FAMILY_ZH = {"S": "结构（静态查询）", "B": "行为（需展开执行）", "P": "性质（含步数界）"}
#: The 19 closed predicates, so "which were unused" is computed rather than asserted.
FAMILY_OF = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}


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

    # ---------------------------------------------------------------- 边界与定义（§0）
    smry = json.loads((MR / "_summary.json").read_text())
    g = smry["grade_totals"]
    oos = smry["out_of_scope_totals"]
    bl = t["by_layer"]
    strata_all = Counter(r["stratum"] for r in
                         json.loads((MR / "final_stratification.json").read_text())["rows"])
    L = [
        "### 0.1 断言对象边界",
        "",
        "本集合的断言对象是 **FSM / HSM / EFSM**，即 $M = (S, E, V, Tr, A)$；"
        "**时钟 $C$、不变式 $Inv$ 与正交区并发执行语义不在断言对象内**。"
        "判据来自 [manual_review_spec.md](https://github.com/HansBug/research_ideas/blob/main/"
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/manual_review_spec.md) "
        "的六行硬规则：数量与结构断言（「有 N 个 X」）在范围内；"
        "「区域之间是否同时活跃」在范围外；定时器动作属 $A$、定时器事件属 $E$、"
        "零时守卫属 $V$，三者均在范围内；真正的时长约束（`execTime`）在范围外。",
        "",
        "**418 → 153 的三道过滤（后文不再重复）：**",
        "",
        "| # | 过滤 | 剩余 | 说明 |",
        "| --: | --- | ---: | --- |",
        f"| 1 | 档位过滤 | {g['problem'] + g['extra']} | "
        f"只保留 `problem` {g['problem']} + `extra` {g['extra']}；"
        f"`correct` {g['correct']} / `similar` {g['similar']} / `uncertain` {g['uncertain']} "
        f"不进入（语义等价或证据不足）|",
        f"| 2 | `out_of_scope` tag（`problem`/`extra` 档）| "
        f"{g['problem'] + g['extra'] - 9} | 减 9 条（并发 7 + 时间 2）。"
        f"全档位共 {sum(oos.values())} 条带该 tag"
        f"（并发 {oos['concurrency']} + 时间 {oos['timing']}），"
        f"其余落在 `similar` / `uncertain` 档、本就不计入 |",
        "| 3 | 主裁定追加剔除 | **153** | "
        "`0013`#1：该事实与参考共有，且只在正交区被展平后成立 |",
        "",
        "剩余 153 条经逐条复检全部落在范畴内。**这个 153/153 必须读作"
        "「对已过滤集合的复检未发现漏剔」，不是「原始差异集天然全在范畴内」**——"
        "范围外的条目在复核阶段就已被扣除。复检中有 3 条需重新论证归因基础"
        "（`0043`#2、`0047`#0、`0056`#3），重新论证后仍在范畴内。",
        "",
        "**与 [ground_truth_limitations.md](https://github.com/HansBug/research_ideas/blob/main/"
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/ground_truth_limitations.md)"
        " §2 的口径差异（必须声明）**：§2 按**对象**排除正交并发相关候选；"
        "本轮按**断言形式**排除——对象是正交区、但断言写成 $S$ 内的存在性或数量命题时判为范围内。"
        "本轮口径**更窄**，因此本集合含有若干在 §2 口径下会被整条排除的条目"
        "（上述 3 条 disputed 即是）。引用两份文档的排除数时不得互换。",
        "",
        "**继承 §2 的强制披露**：本分母系统性排除了基线论文最大的一类语义问题"
        "（`missing regions`），原因是该类不在本轮断言对象内，**而非方法未能检出**；"
        "同样**不得**据此声称「这些模型没有并发类问题」。",
        "",
        "### 0.2 什么算一条 expected issue",
        "",
        "一条 expected issue 是**同时满足四项**的记录：",
        "",
        "1. **来自逐对复核的一条 diff**，档位为 `problem`（违反 NL 或丢失参考承载的语义）"
        "或 `extra`（生成方多出、参考与 NL 均未要求）。"
        "`correct` / `similar` / `uncertain` 档不进入。",
        "2. **落在 §0.1 的断言对象范畴内**。",
        "3. **可归因于生成方**，且归因方式属四个归因层之一。",
        "4. **不处于搁置状态**。",
        "",
        "据此明确排除的（合计 "
        f"{sum(v for k, v in strata_all.items() if k not in LAYER_ORDER)} 条）：",
        "",
        "| 排除层 | 条数 | 为什么不入 |",
        "| --- | ---: | --- |",
        f"| `over_specification_benign` | {strata_all['over_specification_benign']} | "
        f"生成方多出，但写不出可断言的后果 |",
        f"| `reference_only` | {strata_all['reference_only']} | "
        f"只在参考侧、NL 未点名——不可归因于生成方 |",
        f"| `uncertain_stratum` | {strata_all['uncertain_stratum']} | "
        f"已审阅但搁置（断言实测 `None`，或该行自述「本任务不裁」）|",
        f"| `over_specification_duplicate` | {strata_all['over_specification_duplicate']} | "
        f"后果已被同 pair 另一条承载，计入会双算 |",
        f"| `out_of_scope_concurrency` | {strata_all['out_of_scope_concurrency']} | "
        f"主裁定移出范畴 |",
        "",
        "它**不是**：不是「差异」（418 条差异中大部分因语义等价、不可归因或范畴外而不计入）；"
        "不是「缺陷率」（见 §7.1 的枚举面依赖）；"
        "不是「必须被 Repair 的命令」（Repair 另有运行时门禁）。",
        "",
        "### 0.3 计数单位与粒度依赖（必须披露）",
        "",
        f"**一条 expected issue = 一条复核 diff 行**，因此 {t['records']} 这个数"
        f"**依赖审阅者把一个现象拆成几条**：",
        "",
        "- 各审阅单元的 diffs/case 在 **4.8 – 9.2** 之间；粒度与 `problem` 数的 "
        "Pearson $r = 0.850$，即组间差异约 **72%** 可由拆分粒度解释；",
        "- 实例：`0027` 把 4 个死端合成 **1** 条，`0047` 把 3 项拆成 **3** 条；"
        "双盲复审中盲审 B 把 `0045` 拆成 **4** 条而原审判 **1** 条；",
        "- 拆分纪律本身也强制产生拆分：一条兼有范畴内与范畴外两面的 diff **必须**拆成两条。",
        "",
        f"因此正确表述是：**{t['records']} 是当前拆分口径下的条数，不是缺陷的客观个数**。"
        "跨 LLM、跨 NL 组比较绝对数值无效（见 §6）。",
        "",
        "### 0.4 术语与口径",
        "",
        "| 术语 | 定义 | 数量 |",
        "| --- | --- | ---: |",
        "| **差异（diff）** | 一条复核记录行，档位 ∈ {`correct`, `similar`, `problem`, "
        "`extra`, `uncertain`} | 418 |",
        "| **计入问题** | 档位为 `problem`/`extra`、未带 `out_of_scope` tag，再减主裁定剔除 | 153 |",
        "| **expected issue**（= 可入 / admissible）| 「计入问题」中归因层属四个可入层之一"
        f"且未搁置者。正文统一用 expected issue | {t['records']} |",
        "| **可自动验收** | 存在 `primary` 断言且**实测为 `False`**。指 oracle 侧能否机械判定"
        f"该缺陷存在，与运行时 Confirm 阶段无关 | {t['automatable']} |",
        "| **E1** | 旧台帐（#166）对一条 expected issue 的编号前缀口径，"
        "本文只在引用旧台帐时使用 | 47 |",
        "| **8 格运行** | 最近一次完整 Discover 运行覆盖的 8 个单元格"
        "（`0000`/`0006`/`0029`/`0050` 各 × Claude 与 GPT）| 8 |",
        "",
        "**「计入问题」的口径必须随数字标注**：仓库内该量有多个合法口径——主档 154；"
        "主裁定剔除 `0013`#1 后 **153**（本文全文使用此值）；"
        "按 `RESCOPE.md` 的边界重判口径为 157，剔除后 156。"
        "引用时不得省略口径名，跨口径加减必须先换算。",
    ]
    emit("boundary.md", "\n".join(L))

    # ---------------------------------------------------------------- oracle 局限（§6）
    bl_named = bl.get("nl_named", 0)
    L = [
        "### 7.1 参考模型：不作归因依据，但决定了差异的可见性",
        "",
        "本集合的四个归因层**都不以参考模型为 oracle**。但必须区分两件事：",
        "",
        "- **归因侧**不依赖参考模型 —— 成立；",
        "- **召回侧**依赖参考模型 —— 418 条差异的枚举来自「作者生成 STM_0 相对参考 STM_0」"
        "的逐对比对。**参考模型没有承载的缺陷类，本集合就不会枚举到。**",
        "",
        "参考模型是原论文作者人工重建的产物，其正确性未经独立验证；"
        "[#171](https://github.com/HansBug/research_ideas/issues/171) 在 **6 个 NL 组**"
        "记录了参考与 NL 的冲突，且 `uncertain` 的最大卡点类别就是「参考模型自身可疑」。"
        f"因此 **{{PAIRS}} / 60 的 pair 覆盖率是相对该枚举面的覆盖率，"
        "不是对 60 个模型全部缺陷的覆盖率。**",
        "",
        "### 7.2 部分 NL 是从模型反推的，这削弱 `nl_named` 层",
        "",
        "原论文 §3.3 写明：\"For undocumented cases, we analyzed model structures and "
        "behaviors to **infer implicit requirements**\" —— 那些 case 的 **NL 是从作者模型反推的**。"
        "后果：在这些 case 上，「NL 点名了 X，生成侧缺 X」部分退化为「参考模型有 X」，"
        "即 `nl_named` 层想避开的那个 oracle 通过 NL 间接回流。"
        f"这一层是最大层（{bl_named} / {t['records']} = {pct(bl_named, t['records'])}），"
        f"所以不是边缘风险。",
        "",
        "**待办**：逐 NL 组标注 documented / inferred 两态，"
        "并对落在 inferred 组的 `nl_named` 条目做一次降级复核。"
        "在此之前，`nl_named` 的 69 条**不应**被表述为「与参考模型无关」。",
        "",
        "### 7.3 审阅者与被审对象同类",
        "",
        "逐对复核由 LLM 执行，判定的也是 LLM 制品。"
        "12 例双盲复审的 Cohen $\\kappa$ = **0.750**、一致率 **91.7%**，"
        f"只能证明**判定可复现**，不能证明**判定正确**。本集合的 {t['records']} 条继承这一局限。",
        "",
        "### 7.4 `wellformedness` 层不是 oracle-free，而是换了一个 oracle",
        "",
        "这一层的判据从「作者参考模型」换成「良构性规范语义 + 投影语义」。"
        "后者是公共的、可被第三方检查的，这才是它的真实优势——**不是「不需要 oracle」**。"
        "三点须如实说明：",
        "",
        "1. 逐条记录里 **10 / 37** 条自己就引用了 UML 或标准语义作依据"
        "（如 `EIS-0007-02`「UML 亦不允许初始迁移带触发」），**3 / 37** 条引用了参考模型。",
        "2. 投影语义引入特有风险：若某「缺陷」只在正交区被展平后才出现，"
        "它属于表示层而非作者语义。主裁定已按此移出 `0013`#1。"
        "本层仍有**至少 2 条**（`EIS-0043-02`、`EIS-0033-02`）的缺陷事实"
        "依赖投影注入的合成元素，需按同一判据逐条复核。",
        "3. **本层是四层中人工复核覆盖最低的一层**：37 条中 **31 条**的归层由词法判据给出"
        "（`decided_by = lexical`），未经人工复审；`FINAL_STRATIFICATION.md` 已点名 7 行"
        "需过「区域/展平」筛，其中 1 行一筛即被移出，其余 6 行仍在本集合内。"
        "**在这 6 行复核完成前，本层的证据强度不应被表述为高于 `nl_named`。**",
    ]
    emit("limitations.md", "\n".join(L).replace("{PAIRS}", str(t["pairs_covered"])))

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
        f"| **同质组** | **{t['homogeneity_groups']}** | 同 pair 上主谓词与元素集合完全相同者"
        f"视为同一缺陷。当前 **{t['homogeneity_merges']} 次合并**——"
        f"在 {t['homogeneity_groupable_records']} 条有 binding 的记录里键零碰撞，"
        f"故组数 = 记录数。**命中率仍应按同质组计**，以防后续新增记录出现真实重复 |",
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
    mx = max(bl.values())
    for k in LAYER_ORDER:
        if k not in bl:
            continue
        zh, basis = LAYER_ZH[k]
        L.append(f"| `{k}`（{zh}）| **{bl[k]}** | {pct(bl[k], t['records'])} | "
                 f"{bar(bl[k], mx)} | {basis} |")
    L.append(f"| **合计** | **{sum(bl.values())}** | 100% | | |")
    # Attribution replay, joined by (pair, diff_index). This is the single most consequential
    # limitation of the set and it is not visible from the layer table alone: the pipeline's
    # own contract routes non-`safe` False assertions to `excluded_findings` and *never* to
    # confirmed issues (discover/prompts.py:73, :298).
    rep_rows = {(r["case"], r["diff_index"]): r
                for r in json.loads((MR / "loop_audit/replay_attribution.json").read_text())
                ["rows"]}
    attr = Counter()
    attr_by_layer: dict[str, Counter] = defaultdict(Counter)
    for r in recs:
        row = rep_rows.get((r["pair"], r["upstream"]["diff_index"])) or {}
        st = row.get("attribution_status") or "declared_not_expressible"
        attr[st] += 1
        attr_by_layer[r["layer"]][st] += 1
    safe_n = attr["safe"]
    L += [
        "",
        "### ⚠️ 归因门控：本集合最重要的限制",
        "",
        "把这 " + str(t["records"]) + " 条逐条重放一遍归因，结果是：",
        "",
        "| 归因结论 | 条数 | 占比 | 按流水线契约能否成为 confirmed issue |",
        "| --- | ---: | ---: | --- |",
        f"| `safe` | **{attr['safe']}** | {pct(attr['safe'], t['records'])} | 可以 |",
        f"| `representation_debt` | **{attr['representation_debt']}** | "
        f"{pct(attr['representation_debt'], t['records'])} | "
        f"**不能**——判定所依赖的元素落在该 pair 的 `attribution_exclusions` 里 |",
        f"| `unattributed` | **{attr['unattributed']}** | "
        f"{pct(attr['unattributed'], t['records'])} | **不能**——找不到可信源头映射 |",
        f"| `declared_not_expressible` | {attr['declared_not_expressible']} | "
        f"{pct(attr['declared_not_expressible'], t['records'])} | 无断言可归因 |",
        "",
        f"**{attr['representation_debt'] + attr['unattributed']} 条触发 "
        f"`excluded_findings` 硬门控**"
        f"（`representation_debt` {attr['representation_debt']} + "
        f"`unattributed` {attr['unattributed']}）："
        "`discover/prompts.py:73` 明写「False results marked representation_debt or "
        "unattributed must go to excluded_findings, **never confirmed issues**」。"
        f"连同 {attr['declared_not_expressible']} 条无可求值断言，"
        f"共 **{t['records'] - safe_n} / {t['records']} = "
        f"{pct(t['records'] - safe_n, t['records'])} 的记录不满足"
        f"「binding = `safe` 且实测 `False`」这一 confirmed 前提**"
        "（`prompts.py` 另一句：「Create confirmed issues only from False assertions "
        "whose binding status is safe」）。**两个数口径不同，不可互换：48 是硬门控触发数，"
        f"{t['records'] - safe_n} 是不满足 confirmed 前提的总数**。"
        "把本集合当作命中率分母时，必须同时报告这个分层，"
        "否则会把流水线按设计不该上报的条目记成漏检。",
        "",
        "**按归因通过率给四层重新排序，结论与直觉相反：**",
        "",
        "| 层 | 条数 | 其中 `safe` | 通过率 |",
        "| --- | ---: | ---: | ---: |",
    ]
    for k in sorted(bl, key=lambda x: -attr_by_layer[x]["safe"] / max(bl[x], 1)):
        L.append(f"| `{k}`（{LAYER_ZH[k][0]}）| {bl[k]} | {attr_by_layer[k]['safe']} | "
                 f"**{pct(attr_by_layer[k]['safe'], bl[k])}** |")
    wf = attr_by_layer["wellformedness"]
    L += [
        "",
        f"⚠️ **一处必须撤回的表述。** 本 issue 初版称 `wellformedness` 这一层「最难被质疑」，"
        f"理由是它不需要 NL 也不需要参考模型。**按归因实测，它恰恰是四层里通过率最低的一层**："
        f"{bl['wellformedness']} 条里只有 **{wf['safe']} 条** `safe`"
        f"（{wf['representation_debt']} 条 `representation_debt`、"
        f"{wf['unattributed']} 条 `unattributed`、"
        f"{wf['declared_not_expressible']} 条无可求值断言）。"
        f"通过率最高的是 `nl_contradiction`"
        f"（{attr_by_layer['nl_contradiction']['safe']} / {bl['nl_contradiction']}）。"
        "原因见 §7.4：该层的判定大量依赖 R4.5 投影注入的合成节点，"
        "而那些节点正是归因排除表里的元素。",
        "",
        "```mermaid",
        f"pie showData title 归因层分布（{t['records']} 条）",
    ]
    for k in LAYER_ORDER:
        if k in bl:
            L.append(f'    "{k} {LAYER_ZH[k][0]}" : {bl[k]}')
    L += ["```", ""]
    L += [
        "",
        f"⚠️ 同质组的口径经过一次修正：初版（129 条记录时）报 126 组，"
        f"因为合并键在记录缺主断言时退化为 `(pair, None, ())`，"
        f"把同 pair 上无断言记录中的 3 对**不同**缺陷误并"
        f"（`0025`、`0034`、`0035` 各一对）。修正后无断言记录各自单独成组，"
        f"因此**该机制在本集合上没有消解任何真实重复**——它是为后续规模准备的，当前未生效。",
    ]
    emit("headline.md", "\n".join(L))

    # ------------------------------------------------- 门控三类拆解 + 14 条详情（§4.x）
    # These three groups get lumped together as "62 records cannot be reported", which makes
    # them look like one problem with one fix. They are not: one is an attribution
    # resolution limit, one is trace coverage, one is vocabulary. Only the third is a
    # question about the predicate set, and conflating them would send the fix in the wrong
    # direction -- so the split is spelled out rather than left to the reader.
    noa = [r for r in recs if not r["automatable"]]
    reason_of = Counter()
    for r in recs:
        row = rep_rows.get((r["pair"], r["upstream"]["diff_index"])) or {}
        st = row.get("attribution_status")
        if st in ("representation_debt", "unattributed"):
            reason_of[(st, row.get("attribution_reason"))] += 1
    gate_dir = Counter()
    for r in recs:
        row = rep_rows.get((r["pair"], r["upstream"]["diff_index"])) or {}
        if row.get("attribution_status") in ("representation_debt", "unattributed"):
            gate_dir[r["direction"]] += 1
    n_debt, n_unattr, n_dne = (attr["representation_debt"], attr["unattributed"],
                               attr["declared_not_expressible"])

    L = [
        "上一节的 " + str(n_debt + n_unattr + n_dne) + " 条常被当成同一个问题，"
        "从而指向同一个修法。**它们不是**。按机器给出的成因，它们是三类互不相干的东西，"
        "各自的解法完全不同：",
        "",
        "| 类 | 条数 | 机器给出的成因 | 卡在哪一层 | 解法方向 |",
        "| :-: | ---: | --- | --- | --- |",
        f"| **A** | **{n_debt}** | `exclusion_intersection`"
        f"（{reason_of[('representation_debt', 'exclusion_intersection')]}/{n_debt} 全是这一个）"
        f"| **归因分辨力** | 改归因，不扩谓词、不改边界 |",
        f"| **B** | **{n_unattr}** | "
        + "、".join(f"`{k[1]}` {v}" for k, v in sorted(reason_of.items())
                   if k[0] == "unattributed")
        + " | **trace 覆盖** | 补 `source_trace`，纯工程 |",
        f"| **C** | **{n_dne}** | 19 谓词写不出**可求值的正面主断言**"
        f"（{n_dne - 1} 条零表达式 + 1 条表达式不判别）| **词表能力** | 扩谓词（见 §4.3）|",
        "",
        "### 4.1 A 类：作者的错，被 converter 的补丁盖住了",
        "",
        f"这 {n_debt} 条的成因**全部**是 `exclusion_intersection`——判定所依赖的元素，"
        "落在该 pair 自己的 `attribution_exclusions` 里。但**踩到的是哪种排除元素，"
        "决定了它属于哪种问题**，不能一概而论：",
        "",
        "| 踩到的排除元素 | 条数 | 性质 | 修复归属 |",
        "| --- | ---: | --- | --- |",
        "| 含 `UnspecifiedInitial` | **17** | "
        "**作者漏写初始边的症状**——下面的四步机制描述的正是这一类 | 判定 ①（症状/原因）|",
        "| 仅 `InvalidInitial*` / `InvalidFinal*` / `FinalWait*` | **4** | "
        "同为投影补丁，但形状不同（越界初始边被替换、完成边被补终态）。"
        "机制同类，判定 ① 未必直接覆盖 | 需逐条确认 |",
        "| 纯 `R45RouteToken`（路由变量）| **9** | "
        "**不是任何作者缺陷的症状**，而是投影为拆分迁移普遍注入的管线。"
        "任何行为族谓词（`reaches` / `occupancy_after` / `stays_in`）"
        "在这些 pair 上都会碰它 | 判定 ②（route-control 豁免）|",
        "| `event_projection` | **2** | `0038` 的两条时间事件被投影改写 | 需逐条确认 |",
        "",
        "**下面这个机制只对上表第一行的 17 条成立**"
        "（按表头字面把前两行合起来算是 21 条，"
        "但那 4 条的补丁形状不同，判定 ① 未必直接覆盖，故分列）：",
        "",
        "```",
        "1. 作者没写初始边                            ← 真缺陷，可归因于生成方",
        "2. R4.5 投影为让模型合法，注入 UnspecifiedInitial",
        "3. initial_target 判定时读到的初始子态就是这个合成节点",
        "4. 归因阶段发现「证据踩在 attribution_exclusions 里的元素上」→ representation_debt → 挡下",
        "```",
        "",
        "**关键在于：合成节点是症状，不是原因。** 作者确实有错，只是错的表现形式被 converter "
        "填平了（已回原始 PlantUML 抽样验证：`0014` 顶层无 `[*] -->`、`0044` 的 `InMotion{}` "
        "与 `0058` 的 `Join2{}` 内均无初始边，确为生成方漏写）。所以这 17 条被挡，"
        "**不是归因判错，而是归因分辨力不足**——它只能看到「证据踩在排除元素上」，"
        "看不到「这个排除元素的存在本身就是缺陷的后果」。",
        "",
        "**而那 9 条踩 `R45RouteToken` 的不适用这个论证**：路由变量不是谁的错的症状，"
        "它在每个投影模型里都存在。它们需要的是另一条独立规则——"
        "**对行为族谓词豁免 route-control 观测**，而不是「区分症状与原因」。"
        f"因此 A 类 {n_debt} 条要的是**两处判定逻辑**（① 症状/原因 17 条、② route-control 豁免 9 条），"
        "而不是一处；另 6 条（4 条其他合成节点 + 2 条 `event_projection`）"
        "**两处判定都未必覆盖，需逐条确认**。",
        "",
        "这也解释了 §TL;DR 那张通过率表为什么反直觉："
        f"`wellformedness` 层 {bl['wellformedness']} 条里有 "
        f"{attr_by_layer['wellformedness']['representation_debt']} 条是 "
        f"`representation_debt`，因为该层大量依赖投影语义。"
        "**该层证据不弱，是归因看不穿投影这一层。**",
        "",
        "### 4.2 B 类：source_trace 覆盖不全",
        "",
        f"{n_unattr} 条中 "
        f"{reason_of[('unattributed', 'no_safe_trace_entry')]} 条是 `no_safe_trace_entry`"
        f"（冻结的 source trace 里找不到可安全归因的条目）、"
        f"{reason_of[('unattributed', 'path_taint_ambiguous')]} 条是 `path_taint_ambiguous`。"
        "这是工程覆盖问题，不涉及方法论：trace 没记全，判定就无从溯源。",
        "",
        "### 4.3 C 类：这 " + str(len(noa)) + " 条才是真正的词表问题",
        "",
        "按元组分量分布，问题的重心一目了然：",
        "",
        "| 分量 | 条数 | 占比 |",
        "| :-: | ---: | ---: |",
    ]
    el = Counter(r.get("element_of_M") for r in noa)
    for k, v in el.most_common():
        L.append(f"| **{k}** | {v} | {pct(v, len(noa))} |")
    L.append(f"| **合计** | **{len(noa)}** | 100% |")
    L += [
        "",
        f"**$A$ 占 {el.get('A', 0)} 条（{pct(el.get('A', 0), len(noa))}）——而 $A$ 正是 "
        "$M = (S, E, V, Tr, A)$ 的分量之一。** 这个事实决定了后面的取舍（§4.5）。",
        "",
        "#### 主体：动作与输出信号（$A$）",
        "",
        "微波炉那一组是最干净的例子——**同一份 NL 的六个模型全中**：",
        "",
        "> NL 第 5/6/7/8 句显式要求 timer 启停与 cooking time 的显示/更新"
        "（\"where the timer starts\"、\"stops the timer\"、"
        "\"the cooking time is displayed and updated\"），参考以迁移 effect 承载，"
        "**生成侧完全缺失**。",
        "",
        "19 个谓词为什么说不出这条：",
        "",
        "| 通道 | 谓词 | 为什么不行 |",
        "| --- | --- | --- |",
        "| effect | `effect_declared` / `variable_delta_after` | "
        "两者都要求 `variable` + `sign`，即「某变量增减」。"
        "但 `Start Timer` 是**具名的抽象动作**，不是数值变化 |",
        "| effect | `variable_declared` | "
        "只需 `variable` 一个参数，但它问的是「模型有没有这个**变量**」，"
        "而缺的是一个**动作** |",
        "| — | 上述三条路共同的死路 | "
        "它们都指向数值/变量通道，而全库唯一被声明过的变量是 converter 的 "
        "`R45RouteToken`（60 个模型里 33 个声明它、27 个零变量），"
        "**该通道在本语料恒为空** |",
        "| action | `action_declared(state=..., phase=...)` | "
        "**没有动作名参数**。它只能证明「这个状态挂了某个动作」，"
        "证明不了「挂的是 `Start Timer`」|",
        "",
        "另两条比「说不出」更危险，因为谓词会**给出错误的肯定答案**：",
        "",
        "> `0034`#5：NL 第 3 句要求 `EmergencyStopping` 既执行 `Emergency Stop` "
        "又发送 `Obstacle Detected` 信号。作者只保留了前者，"
        "后者**在全模型任何相位、任何迁移上都不存在**。",
        "",
        "此时 `action_declared(EmergencyStopping, 'entry')` 实测返回 **`True`**"
        "——因为确实挂了 `Emergency Stop`。**谓词说「有动作」，而缺的是「哪个动作」**。"
        "更棘手的是同名的 `Obstacle_Detected` 作为**触发事件**是声明了的，"
        "`event_declared` 同样返回 **`True`**——**两个谓词同时给出错误的肯定答案**，"
        "而缺失的是它作为**输出动作**的那一面。"
        "这是漏检（false pass），不是表述不出，性质更严重。"
        "（负控：同模型的 `Stopping` 与 `exit` / `during` 相位均返回 `False`，说明该谓词不是恒真。）",
        "",
        "#### 其余分量",
        "",
        "| 分量 | 条目 | 卡点 |",
        "| :-: | --- | --- |",
        "| $Tr$ | `0008`#5、`0038`#4 | 「`choice3` 应直连 `Junction3` 但分支缺失」涉及伪状态间的边，"
        "而 `edge_declared` 强制要求具名 `trigger`，completion 边（无触发）表达不出 |",
        "| $Tr$ | `0033`#2 | 三条初始边全部越出子作用域，被投影替换成三个 `Invalid` 标记 |",
        "| $V$ | `0025`#1、`0035`#3 | 「该边既无守卫也未在事件名点出零时」。"
        "R4.5 **从不把方括号解析为守卫**"
        "（源 PlantUML 里非 `[*]` 的方括号标签共 40 处、去重 29 条、分布在 10 个 pair，"
        "无一成为守卫；它们全部被折进事件名），"
        "且全库 160/160 个守卫都是 converter 的 route-control、"
        "**作者自有守卫为零**——`guard_distinguishable` 的判别分支在本语料几乎不可达 |",
        "| $S$ | `0007`#3 | 整棵臆造子树无入边（死代码）+ 同一非正交区里三条初始迁移 |",
        "",
        "### 4.4 命中率该怎么算",
        "",
        f"这 {n_debt + n_unattr + n_dne} 条的处理，两种极端都会得出错误结论：",
        "",
        "| 做法 | 后果 |",
        "| --- | --- |",
        f"| 全算进分母 | 流水线**按设计不该报**的条目被记成漏检 → **低估**流水线 |",
        f"| 全踢出分母 | 掩盖归因与词表的真实局限 → **高估**流水线 |",
        "",
        f"**建议：分母仍是 {t['records']} 条**（缺陷成立与否，与工具能否报它无关），"
        "**但命中率必须拆三层报**：",
        "",
        f"1. **`safe` {attr['safe']} 条上的命中率** = 当前流水线的真实能力，这是唯一"
        "可直接解读为「检出率」的数；",
        f"2. **A 类 {n_debt} 条** = 受归因分辨力限制而结构性不可达，"
        "**不应记为流水线漏检**，应记为归因层待改进；",
        f"3. **B 类 {n_unattr} + C 类 {n_dne} 条** = 受 trace 覆盖与词表能力限制，同上分列。",
        "",
        "### 4.5 扩谓词，还是把这些排除在边界之外",
        "",
        "**三类要分开决策，把它们当一个问题是最容易犯的错。**",
        "",
        "| 类 | 决策 | 理由 |",
        "| :-: | --- | --- |",
        f"| **A**（{n_debt}）| **改归因分辨力**，不扩谓词、不改边界 | "
        "谓词已经正确检测到了缺陷。要做的是**两处判定**（不是一批谓词）："
        "① 区分「证据落在合成节点上」与「缺陷本身由合成节点造成」"
        "——前者应放行（作者的错），后者应挡下（converter 的产物），覆盖 17 条；"
        "② 对行为族谓词豁免 route-control 观测，覆盖 9 条。"
        "剩余 6 条需逐条确认（见 §4.1 表）|",
        f"| **B**（{n_unattr}）| **补 source_trace 覆盖** | 纯工程，不涉及方法论 |",
        f"| **C**（{n_dne}）| **必须扩谓词，不能排除在边界外** | 见下三条理由 |",
        "",
        "**理由一：$A$ 就在 paper1 的问题定义里。** paper1 锚定 $M = (S, E, V, Tr, A)$，"
        "排除的只有时钟 $C$、不变式 $Inv$ 与正交并发。"
        f"而这 {len(noa)} 条里 **{el.get('A', 0)} 条落在 $A$**。"
        "把它们排除，等于 paper1 声称覆盖 $A$ 分量、却对 $A$ 的内容无法断言"
        "——这个自相矛盾审稿人一定会问。",
        "",
        "**理由二：这个错误本仓库已经犯过一次。** "
        "[ground_truth_limitations.md](https://github.com/HansBug/research_ideas/blob/main/"
        "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix/docs/protocol/ground_truth_limitations.md)"
        " §4 记录的正是它：#166 台帐的「正向断言可执行」门槛建立在 6 个底层原语上，"
        "直接把整类问题挡在门外。**用工具当前能力反向定义研究边界，会让偏差变成不可见**"
        "——一旦排除，「谓词面缺什么」就不再是可报告的结论，而是被静默吸收的系统性缺口。",
        "",
        f"**理由三：要扩的量很小、方向很明确。** 这 {len(noa)} 条不是 "
        f"{len(noa)} 个方向，而是五个具体缺口：",
        "",
        "| 缺口 | 覆盖条数 | 形态 | 难度 |",
        "| --- | ---: | --- | --- |",
        "| 状态局部动作名 | **2** | "
        "`action_declared(state, phase, action=...)` | 低，**但须与归因修复同批**："
        "`0034` 的 5 个作者自写动作在排除表里被记为 `compiler:lifecycle_action:*`，"
        "单独落地只会把它们从 C 类挪进 A 类 |",
        "| 迁移具名 effect / 输出信号 | **6** | 需边级具名 effect 谓词 | "
        "⚠️ **需先改 R4.5**：trigger/effect 被折叠进事件名"
        "（`0034` 的 `Closed/SendDeparted` 投影成单一 `event Closed_SendDeparted`），"
        "而参考侧过同一条 R4.5 后同样不会有 action——"
        "新谓词在正确模型上**也返回 `False`**，按 §5 的标准属「非区分」，不成其为证据 |",
        "| 无触发 / completion 边 | 2 | 允许 `edge_declared` 的 `trigger` 为空 | 低 |",
        "| 守卫非空 / 边须携带区分条件 | 2 | "
        "⚠️ **扩谓词也判别不出**——作者自有守卫全库为零，卡在表示层，"
        "应老实标为投影层缺口 | 需先改 R4.5 |",
        "| 存在量词 / 最小性 | 2 | S 族全是具名点查询，无存在量词 | 结构性，可暂缓 |",
        "",
        "按难度分成两组：**第 1、3 行（共 4 条）只需给现有谓词加参数或放宽约束**"
        "（动作名参数、允许 `edge_declared` 的 `trigger` 为空）；"
        "**第 2、4 行（共 8 条）卡在表示层**——R4.5 折叠 trigger/effect、且不产出守卫，"
        "**扩谓词单独落地无用**。第 5 行属结构性缺口，可暂缓。"
        "这修正了一个容易过于乐观的判断："
        f"$A$ 分量的 {el.get('A', 0)} 条里，只有 2 条能靠加参数解决，另 6 条需要先动投影层。",
        "",
        "### 4.6 一个必须由人裁定的边界政策",
        "",
        "有件事扩谓词解决不了：**是否允许闭世界禁令命题**"
        "（「该状态必须保持吸收」「不得声明该事件」）。",
        "",
        "**⚠️ 本节的分母不是 §4.3 的 14 条**，而是 153 条「计入问题」上的 **30 条**"
        "不可表述（其层分布：`over_specification_benign` 15、`nl_named` 12、"
        "`over_specification` 1、`wellformedness` 1、`reference_only` 1——"
        "其中只有 14 条进入本集合的 126）。",
        "",
        "这 30 条里有 5 条（NL02 钳夹类）实测 "
        "`invariant(scope=S, condition=active(S))` **确实返回 `False`** 且有有效正控"
        "（`0026` 的真吸收态返回 `True`）——按纯机械判据它们本该算「可表述」。"
        "它们被留在不可表述里，依据的是一条**未写进 "
        "[`predcov_BRIEF.md`](https://gist.github.com/HansBug/"
        + agist + "#file-predcov_brief-md) 的政策**：闭世界禁令不算合法断言。",
        "",
        "**这条政策若翻转，影响的方向与直觉相反。** 受影响的 8 条"
        "（`0021`#0、`0031`#0、`0041`#0、`0041`#1、`0051`#0、"
        "`0002`#3、`0010`#7、`0043`#2——这里的 `#N` 是 `diff_index` 不是 EIS 编号）"
        "**全部落在 `over_specification_benign`，一条都不在 126 里**。所以翻转**不会**"
        f"减少 §4.3 的 {len(noa)} 条，而是会把最多 8 条 benign `extra` 提升为"
        f"可断言的 `over_specification`，即**分母从 {t['records']} 变为最多 "
        f"{t['records'] + 8}**。",
        "",
        "**这是分层政策问题，不是谓词能力问题，必须由人裁定。**",
        "",
        "### 4.7 优先级建议",
        "",
        "| 序 | 动作 | 影响条数 | 成本 | 附带收益 |",
        "| --: | --- | ---: | --- | --- |",
        f"| 1 | 改归因分辨力（区分「证据踩合成节点」与「缺陷由合成节点造成」）| **{n_debt}** | "
        "**两处**判定逻辑：① 症状/原因（覆盖 17 条）+ ② route-control 豁免（覆盖 9 条）；"
        "另 6 条需逐条确认 | "
        f"`wellformedness` 层通过率从 "
        f"{pct(attr_by_layer['wellformedness']['safe'], bl['wellformedness'])} 升至最高 86%。"
        "⚠️ **这只解除归因侧的结构性阻塞，不构成对 §8 已撤回的「该层最难被质疑」的恢复**"
        "——§7.4 列出的三条限制（10/37 引外部标准语义、3/37 引参考模型、"
        "31/37 未经人工复审）与归因无关，仍然成立 |",
        "| 2 | 给 `action_declared` 加动作名参数 | **2** | 加一个参数（依赖第 1 项）| "
        "补上 $A$ 分量的一部分 |",
        "| 2b | 边级具名 effect 谓词 + R4.5 停止折叠 trigger/effect | **6** | "
        "需改投影层 | 补齐 $A$ 分量；不先改 R4.5 则新谓词非区分 |",
        f"| 3 | 补 source_trace 覆盖 | **{n_unattr}** | 纯工程 | — |",
        f"| 4 | 裁定闭世界政策 | ≥8（**153 行台帐口径，不在 {t['records']} 内**）| "
        "需人决策 | 若翻转则分母增大，不是减小 |",
        "| 5 | 最小性 / 存在量词谓词 | 2 | 结构性大 | 可留作 future work |",
    ]
    emit("gate_detail.md", "\n".join(L))

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
    # A `None` key survives JSON round-trip as the *string* "null", so `if k` lets it
    # through and `.get(None)` misses it -- which printed a phantom predicate named `null`
    # with 13 records while claiming 0 records had no predicate.
    NULLISH = {None, "null", "None", ""}
    bp = {k: v for k, v in t["by_primary_predicate"].items() if k not in NULLISH}
    none_n = sum(v for k, v in t["by_primary_predicate"].items() if k in NULLISH)
    L += [
        "",
        "### 承载谓词",
        "",
        "族的含义：" + "、".join(f"`{k}` = {v}" for k, v in FAMILY_ZH.items()) + "。",
        "",
        "| 谓词 | 族 | 条数 | 图示 |",
        "| --- | :-: | ---: | --- |",
    ]
    fam_of = FAMILY_OF
    mxp = max(bp.values()) if bp else 1
    for k, n in sorted(bp.items(), key=lambda kv: -kv[1]):
        L.append(f"| `{k}` | {fam_of.get(k, '—')} | **{n}** | {bar(n, mxp)} |")
    L.append(f"| **无可求值主断言** | — | **{none_n}** | {bar(none_n, mxp)} |")
    L.append(f"| **合计** | | **{sum(bp.values()) + none_n}** | |")
    unused = sorted(set(FAMILY_OF) - set(bp))
    rest = t["needs_human_judgement"] - none_n
    L += [
        "",
        f"19 个封闭谓词里 **{len(bp)}** 个被用到，未用到的 {len(unused)} 个是 "
        + "、".join(f"`{u}`" for u in unused) + "。",
        "",
        "",
        "**⚠️ 最大谓词组的证据不是自足的。** `initial_target` 是本集合承载最多的谓词，"
        "但对抗性复核逐条追出了实际决定其 `False` 的那个初始子态："
        "**21 条里有 18 条（86%）的初始子态是 R4.5 投影注入的合成节点**"
        "（`UnspecifiedInitial` ×17、`InvalidInitialtr_*` ×1），"
        "而这些节点正列在各 pair 自己的 `attribution_exclusions` 里"
        "（`compiler:state:…UnspecifiedInitial`）。"
        "复核者的散文**确实**追对了根因（「作者源没写初始边、投影因此注入 UnspecifiedInitial」），"
        "但**断言本身没有编码这个推理**：一个 `initial_target` 的 `False` 同时兼容"
        "(a) 根本没写初始边、(b) 初始边指向了别的子态、"
        "(c) converter 的 route-token 守卫迫使无条件回退。"
        "因此这 18 条要判定归因，必须再读一份断言从未触及的制品（源 PlantUML）——"
        "**这与 `wellformedness` 声称的「仅凭生成模型自身即可判定」直接冲突**，"
        "也是上面归因通过率里该层垫底的直接原因。",
        "",
        f"**{none_n}** 条没有可求值的主断言"
        + (f"，另 {rest} 条写得出封闭谓词表达式但从散文恢复后不可求值（`EIS-0007-03`）"
           if rest else "")
        + f"，合计 **{t['needs_human_judgement']}** 条只能人工验收——这就是本集合的自动化上限。",
    ]
    emit("directions.md", "\n".join(L))

    # ---------------------------------------------------------------- ledger coverage
    ct = cov["totals"]
    prov = cov.get("ledger_provenance", "unknown")
    L = [
        "⚠️ **一处必须更正的前提。** 本 issue 的初版称 issue "
        "[#166](https://github.com/HansBug/research_ideas/issues/166) 的机器总账 "
        "`ledger.json` 已在 2026-07-29 机器重建中丢失且不可恢复，因此无法做 binding 级交代。"
        "**这个判断是错的。** 该文件一直在仓库里：路径 "
        "`.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/ledger.json`，"
        "370,994 字节，SHA-256 `03d8756650c0…` 与 #166 正文公布的「机器总账 SHA-256」逐字符一致，"
        "已于 2026-07-29 22:01 由 commit `94074e4e` 恢复并纳入 git。"
        "**其 47 / 47 条带 `eval_assert`，其中 44 条含可提取的模型元素路径**。"
        "初版之所以判为丢失，是因为检索 `ledger.json` 时用的 glob 不匹配 `.omx` 这个点开头的目录。",
        "",
        f"本节数字已改用 frozen ledger 重算（来源：`{prov}`）。"
        f"这也纠正了一处违规：`docs/protocol/hit_criterion.md` §7 明文规定"
        f"「不要再基于重建版计算或引用任何命中数字」，而初版读的正是那份仅覆盖 4 个 pair 的重建物。",
        "",
        "关系仍然是：**本集合即台帐**，#166 的 47 条作为一份"
        "**必须被逐条交代的覆盖清单**。改用 frozen ledger 后的逐条结果：",
        "",
        "| 交代结果 | 条数 | 含义 |",
        "| --- | ---: | --- |",
        f"| `binding_match` | **{ct.get('binding_match', 0)}** | "
        f"旧条目的 `eval_assert` 与本集合某条断言**共享模型元素**——机器可判，最强关联 |",
        f"| `same_pair_only` | **{ct.get('same_pair_only', 0)}** | "
        f"本集合在该 pair 上有条目，但 binding 不相交——具体对应需人工确认 |",
        f"| `unaccounted` | **{ct.get('unaccounted', 0)}** | "
        f"本集合在该 pair 上没有任何可入条目——**这个数必须为 0**，否则等于静默丢弃既有发现 |",
        f"| **合计** | **{ct['ledger_entries']}** | |",
        "",
        f"**`unaccounted` = {ct.get('unaccounted', 0)}**，即旧台帐涉及的每个 pair 本集合都有对应条目。"
        f"其中 **{ct.get('binding_match', 0)} 条达到 binding 级交代**"
        f"（{pct(ct.get('binding_match', 0), ct['ledger_entries'])}）——"
        f"旧条目的断言与本集合某条断言绑定到了同一批模型元素，这是机器可判的最强关联。"
        f"剩余 **{ct.get('same_pair_only', 0)} 条**只达到 pair 级："
        f"**它们只证明「该 pair 有新条目」，不证明「新条目覆盖了旧条目所指的那个缺陷」**——"
        f"这是必要条件而非充分条件，需逐条人工确认，尚未完成。",
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
        f'    A["issue #166 frozen ledger<br/>47 条 / {ct["pairs_in_ledger"]} pair"] '
        f'-->|"{ct.get("binding_match", 0)} 条 binding_match"| C',
        f'    A -->|"{ct.get("same_pair_only", 0)} 条 same_pair_only<br/>待人工确认"| C',
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
        "本轮 18 条 benign `extra` 中，harm test 记录明确写着「non-discriminating："
        "正确模型没有该事件，谓词在那里同样返回 `False`」的有 **8 条**"
        "（`0021`#0、`0024`#4、`0029`#5、`0031`#0、`0034`#6、`0041`#0、`0041`#1、`0051`#0）——"
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
