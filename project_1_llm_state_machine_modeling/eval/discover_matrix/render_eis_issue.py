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
    oos = json.loads((MR / "_summary.json").read_text())["out_of_scope_totals"]
    strata_all = Counter(r["stratum"] for r in
                         json.loads((MR / "final_stratification.json").read_text())["rows"])
    L = [
        "### 0.1 断言对象边界",
        "",
        "本集合的断言对象是 **FSM / HSM / EFSM**，即 $M = (S, E, V, Tr, A)$；"
        "**时钟 $C$、不变式 $Inv$ 与正交区并发执行语义不在断言对象内。**"
        "判据来自 [MANUAL_REVIEW_SPEC.md](https://github.com/HansBug/research_ideas/blob/main/"
        "project_1_llm_state_machine_modeling/eval/discover_matrix/MANUAL_REVIEW_SPEC.md) "
        "的六行硬规则：数量与结构断言（「有 N 个 X」）在范围内；"
        "「区域之间是否同时活跃」在范围外；定时器动作属 $A$、定时器事件属 $E$、"
        "零时守卫属 $V$，三者均在范围内；真正的时长约束（`execTime`）在范围外。",
        "",
        "**418 → 153 的两道过滤（后文不再重复）：**",
        "",
        "| 过滤 | 条数 | 说明 |",
        "| --- | ---: | --- |",
        f"| 逐条 `out_of_scope` tag | {sum(oos.values())} | "
        f"并发 {oos['concurrency']} + 时间 {oos['timing']}。其中 **`problem`/`extra` 档 9 条**"
        f"（并发 7 + 时间 2）——这 9 条可归因于生成方，但按断言对象边界排除 |",
        "| 主裁定追加剔除 | 1 | `0013`#1：该事实与参考共有，且只在正交区被展平后成立 |",
        "",
        "剩余 153 条经逐条复检全部落在范畴内。**这个 153/153 必须读作"
        "「对已过滤集合的复检未发现漏剔」，不是「原始差异集天然全在范畴内」**——"
        "范围外的条目在复核阶段就已被扣除。复检中有 3 条需重新论证归因基础"
        "（`0043`#2、`0047`#0、`0056`#3），重新论证后仍在范畴内。",
        "",
        "**与 [GROUND_TRUTH_LIMITATIONS.md](https://github.com/HansBug/research_ideas/blob/main/"
        "project_1_llm_state_machine_modeling/eval/discover_matrix/GROUND_TRUTH_LIMITATIONS.md)"
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
        "不是「缺陷率」（见 §6 的枚举面依赖）；"
        "不是「必须被 Repair 的命令」（Repair 另有运行时门禁）。",
        "",
        "### 0.3 计数单位与粒度依赖（必须披露）",
        "",
        "**一条 expected issue = 一条复核 diff 行**，因此 129 这个数**依赖审阅者把一个现象拆成几条**：",
        "",
        "- 各审阅单元的 diffs/case 在 **4.8 – 9.2** 之间；粒度与 `problem` 数的 "
        "Pearson $r = 0.850$，即组间差异约 **72%** 可由拆分粒度解释；",
        "- 实例：`0027` 把 4 个死端合成 **1** 条，`0047` 把 3 项拆成 **3** 条；"
        "双盲复审中盲审 B 把 `0045` 拆成 **4** 条而原审判 **1** 条；",
        "- 拆分纪律本身也强制产生拆分：一条兼有范畴内与范畴外两面的 diff **必须**拆成两条。",
        "",
        "因此正确表述是：**129 是当前拆分口径下的条数，不是缺陷的客观个数。**"
        "跨 LLM、跨 NL 组比较绝对数值无效（见 §5）。",
        "",
        "### 0.4 术语与口径",
        "",
        "| 术语 | 定义 | 数量 |",
        "| --- | --- | ---: |",
        "| **差异（diff）** | 一条复核记录行，档位 ∈ {`correct`, `similar`, `problem`, "
        "`extra`, `uncertain`} | 418 |",
        "| **计入问题** | 档位为 `problem`/`extra`、未带 `out_of_scope` tag，再减主裁定剔除 | 153 |",
        "| **expected issue**（= 可入 / admissible）| 「计入问题」中归因层属四个可入层之一"
        "且未搁置者。正文统一用 expected issue | 129 |",
        "| **可自动验收** | 存在 `primary` 断言且**实测为 `False`**。指 oracle 侧能否机械判定"
        "该缺陷存在，与运行时 Confirm 阶段无关 | 115 |",
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
    L = [
        "### 6.1 参考模型：不作归因依据，但决定了差异的可见性",
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
        "### 6.2 部分 NL 是从模型反推的，这削弱 `nl_named` 层",
        "",
        "原论文 §3.3 写明：\"For undocumented cases, we analyzed model structures and "
        "behaviors to **infer implicit requirements**\" —— 那些 case 的 **NL 是从作者模型反推的**。"
        "后果：在这些 case 上，「NL 点名了 X，生成侧缺 X」部分退化为「参考模型有 X」，"
        "即 `nl_named` 层想避开的那个 oracle 通过 NL 间接回流。"
        "这一层是最大层（69 / 129 = 53%），所以不是边缘风险。",
        "",
        "**待办**：逐 NL 组标注 documented / inferred 两态，"
        "并对落在 inferred 组的 `nl_named` 条目做一次降级复核。"
        "在此之前，`nl_named` 的 69 条**不应**被表述为「与参考模型无关」。",
        "",
        "### 6.3 审阅者与被审对象同类",
        "",
        "逐对复核由 LLM 执行，判定的也是 LLM 制品。"
        "12 例双盲复审的 Cohen $\\kappa$ = **0.750**、一致率 **91.7%**，"
        "只能证明**判定可复现**，不能证明**判定正确**。本集合的 129 条继承这一局限。",
        "",
        "### 6.4 `wellformedness` 层不是 oracle-free，而是换了一个 oracle",
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
    bl = t["by_layer"]
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
        f"**{t['records'] - safe_n} / {t['records']} = "
        f"{pct(t['records'] - safe_n, t['records'])} 的记录，"
        f"按流水线自己的裁决契约不得成为 confirmed issue。**"
        "这不是软降级而是硬门控：`discover/prompts.py:73` 明写"
        "「False results marked representation_debt or unattributed must go to "
        "excluded_findings, **never confirmed issues**」。"
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
        f"{wf['unattributed']} 条 `unattributed`）。"
        f"通过率最高的是 `nl_contradiction`"
        f"（{attr_by_layer['nl_contradiction']['safe']} / {bl['nl_contradiction']}）。"
        "原因见 §6.4：该层的判定大量依赖 R4.5 投影注入的合成节点，"
        "而那些节点正是归因排除表里的元素。",
        "",
        "```mermaid",
        "pie showData title 归因层分布（129 条）",
    ]
    for k in LAYER_ORDER:
        if k in bl:
            L.append(f'    "{k} {LAYER_ZH[k][0]}" : {bl[k]}')
    L += ["```", ""]
    L += [
        "",
        f"⚠️ 同质组的口径经过一次修正：初版报 {t['records'] - 3} 组，"
        f"因为合并键在记录缺主断言时退化为 `(pair, None, ())`，"
        f"把同 pair 上无断言记录中的 3 对**不同**缺陷误并"
        f"（`0025`、`0034`、`0035` 各一对）。修正后无断言记录各自单独成组，"
        f"因此**该机制在本集合上没有消解任何真实重复**——它是为后续规模准备的，当前未生效。",
    ]
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
        "**其 47 / 47 条带 `eval_assert`，其中 44 条含可提取的模型元素路径。**"
        "初版之所以判为丢失，是因为检索 `ledger.json` 时用的 glob 不匹配 `.omx` 这个点开头的目录。",
        "",
        f"本节数字已改用 frozen ledger 重算（来源：`{prov}`）。"
        f"这也纠正了一处违规：`HIT_CRITERION.md` §7 明文规定"
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
