"""Render the expected-issue-set bundle: per-pair readable ledgers + the audit files.

Two destinations, deliberately separate gists:

  readable/   one `<pair>-eis.md` per pair -- what a human reads to judge a finding, with the
              NL clause, both sides of the diff, the assertion group and every upstream link
  audit/      the machine-readable records plus the coverage and reconciliation JSON

They are separate because they answer different questions and are cited differently: the
issue body links a reader to the readable ledger for a specific pair, while a reviewer
re-running the numbers pulls the audit JSON. Mixing them makes both harder to cite.

Usage: render_eis_bundle.py [--out DIR]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

# ⚠️ 2026-08-17 归档：本文件原在 `discover_matrix/` 顶层，`HERE` 即指那一层；
# ⛔ 归档到 `archive/r10_ledger_v1_and_v46/scripts/` 后深度多了两层，`HERE / "manual_review"`
# 会解析到不存在的 `scripts/manual_review`。⭐ 故改为指向归档根（它保留了原 discover_matrix
# 的内部布局：manual_review/ · v46/ · verdicts/ …），⛔ 不数层数、按目录名锚定。
_F = pathlib.Path(__file__).resolve()
HERE = next(p for p in _F.parents if p.name == "r10_ledger_v1_and_v46")
MR = HERE / "manual_review"

#: The audit gist and the issue, so cross-references in the readable ledgers are clickable
#: rather than telling the reader to go find them.
AUDIT_GIST = "e92fb6ca165b46d19b1638f03ae93842"
READABLE_GIST = "c34f29f80e778802fe4da5e2a7e3a82b"
ISSUE_URL = "https://github.com/HansBug/research_ideas/issues/172"

LLMS = ["GPT-4o", "GPT-4", "Llama", "Kimi", "DeepSeek", "Claude"]
NLS = [f"NL{i:02d}" for i in range(1, 11)]
NL_DOMAIN = {
    "NL01": "列车控制", "NL02": "基础制动", "NL03": "无人机集群", "NL04": "数码相机",
    "NL05": "自动驾驶模式", "NL06": "泵控制", "NL07": "碰撞避免",
    "NL08": "驾驶模式切换", "NL09": "HSUV", "NL10": "微波炉",
}
LAYER_ZH = {
    "wellformedness": "良构性",
    "nl_named": "NL 点名",
    "nl_contradiction": "与 NL 矛盾",
    "over_specification": "过度指定且有害",
}
DIRECTION_ZH = {
    "reachability": "可达性与终止", "entry": "初始入口", "guard": "守卫与条件",
    "hierarchy": "层次归属", "effect_action": "动作与 effect", "event": "事件与触发",
    "pseudostate": "伪状态类型", "cardinality": "元素数量",
    "target_scope": "迁移目标", "unclassified": "未归类",
}
ROLE_ZH = {
    "primary": "主断言",
    "negative_control": "负控（须为 True）",
    "corroborating": "佐证",
    "recovered_unverified": "从文本恢复、未能验证",
}


def one_line(t, limit=600) -> str:
    s = re.sub(r"\s+", " ", str(t or "")).strip().replace("|", "\\|")
    return s if len(s) <= limit else s[:limit].rstrip() + "……"


def render_pair(pair: str, recs: list[dict], cov: list[dict]) -> str:
    g = recs[0]["group"]
    L = [
        f"# `{pair}` — {g} {NL_DOMAIN.get(g, '')} × {recs[0]['llm']}",
        "",
        f"expected issue **{len(recs)}** 条。每条给出：违反了 NL 的哪一句、参考侧与生成侧的对照、"
        f"归因层（凭什么归因于生成方）、断言组、以及与上游数据的关联。",
        "",
    ]
    if cov:
        L += [
            f"## 旧台帐（issue #166）在本 pair 上的条目",
            "",
            "| 旧条目 | 类别 | 类别含义 | 交代结果 |",
            "| --- | --- | --- | --- |",
        ]
        for c in cov:
            L.append(f"| `{c['id']}` | `{c['category']}` | {one_line(c['category_label'], 90)} "
                     f"| `{c['outcome']}` |")
        L += ["",
              "> `binding_match` = 旧条目的 `eval_assert` 与本 pair 某条新断言共享模型元素（机器可判）；"
              "`same_pair_only` = 本 pair 有新条目但 binding 不相交，具体对应需人工判定。"
              "数据取自 frozen ledger（47 / 47 条带 `eval_assert`，"
              "SHA-256 `03d8756650c0…`）；全库合计 38 `binding_match` / 9 `same_pair_only` / "
              "0 `unaccounted`。",
              ""]

    for r in recs:
        L += [
            "---",
            "",
            f"## {r['id']}",
            "",
            "| 字段 | 值 |",
            "| --- | --- |",
            f"| 归因层 | `{r['layer']}`（{LAYER_ZH.get(r['layer'], '')}）—— {r['layer_basis']} |",
            f"| 缺陷方向 | `{r['direction']}`（{DIRECTION_ZH.get(r['direction'], '')}）|",
            f"| 触及的元组分量 | {r.get('element_of_M') or '—'} |",
            f"| 原始档位 | `{r['verdict']}` |",
            f"| 判定来源 | `{r['decided_by']}`"
            + ("（含主裁定）" if r["parent_ruling"] else "") + " |",
            f"| 可自动验收 | {'是' if r['automatable'] else '**否——须人工判定**'} |",
            f"| 同质组 | `{r['homogeneity_group']}`"
            + (f"（组内 {r['homogeneity_group_size']} 条）"
               if r["homogeneity_group_size"] > 1 else "") + " |",
            "",
            "**缺陷描述**",
            "",
            one_line(r["statement"], 1500),
            "",
        ]
        if r.get("basis_superseded_by_ruling"):
            L += [
                "**⚠️ 本条的判据经主裁定更换** —— 上面的缺陷描述是复核者当时的原话，"
                "其中作为归因依据的部分已被撤回并替换。撤回理由与新判据：", "",
                "> " + one_line(r["basis_superseded_by_ruling"], 2200), "",
            ]
        if r.get("nl_evidence"):
            L += ["**NL 依据（复核者逐字引用）**", "", "> " + one_line(r["nl_evidence"], 900), ""]
        if r.get("reference_side") or r.get("generated_side"):
            L += [
                "**两侧对照**", "",
                "| | 内容 |", "| --- | --- |",
                f"| 参考侧 | {one_line(r.get('reference_side'), 700) or '—'} |",
                f"| 生成侧 | {one_line(r.get('generated_side'), 700) or '—'} |",
                "",
            ]
        if r["assertions"]:
            L += [
                f"**断言组（{len(r['assertions'])} 条）**", "",
                "| # | 角色 | 谓词 | 族 | 表达式 | 实测 |",
                "| --: | --- | --- | :-: | --- | :-: |",
            ]
            LONG = 140   # past this a cell truncation would cut mid-identifier
            for i, a in enumerate(r["assertions"], 1):
                expr = re.sub(r"\s+", " ", a["expression"]).strip()
                shown = (f"见下 `[{i}]`" if len(expr) > LONG
                         else "`" + expr.replace("|", "\\|") + "`")
                L.append(
                    f"| `[{i}]` | {ROLE_ZH.get(a['role'], a['role'])} | "
                    f"{'、'.join(f'`{p}`' for p in a['predicates']) or '—'} | "
                    f"{'/'.join(a['families']) or '—'} | {shown} | "
                    f"`{a.get('measured', '—')}` |")
            L.append("")
            L += ["> 族：`S` = 结构（静态查询）· `B` = 行为（需展开执行）· "
                  "`P` = 性质（含步数界）。角色口径见 "
                  "[`00-README.md`](#file-00-readme-md)。", ""]
            # A truncated assertion is not evidence -- a reader must be able to copy and run
            # it. Anything too long for a cell is emitted verbatim in a code block, which
            # also gives GitHub's copy button.
            longs = [(i, a) for i, a in enumerate(r["assertions"], 1)
                     if len(re.sub(r"\s+", " ", a["expression"]).strip()) > LONG]
            if longs:
                L += ["完整表达式（可直接复制求值）：", "", "```python"]
                for i, a in longs:
                    L.append(f"# [{i}] {ROLE_ZH.get(a['role'], a['role'])}"
                             f" — 实测 {a.get('measured', '—')}")
                    L.append(re.sub(r"\s+", " ", a["expression"]).strip())
                L += ["```", ""]
            prim = next((a for a in r["assertions"] if a["role"] == "primary"), None)
            if prim and prim.get("rewrote_from"):
                # The reason for a rewrite varies -- some originals used a non-closed
                # primitive, others bound the wrong element or lacked a qualified path. So
                # record what it was rewritten from and let the text speak, rather than
                # asserting a single reason that is not always the right one.
                L += [f"> 主断言经重写。原式：`{one_line(prim['rewrote_from'], 400)}`", ""]
            if not any(a["role"] == "negative_control" for a in r["assertions"]):
                L += ["> ⚠️ 本条**没有经实测验证的负控**。缺负控意味着无法排除主断言对正确模型"
                      "也返回 `False` 的可能——本轮 18 条 benign `extra` 中有 **8** 条正是因此被拒"
                  "（其 harm test 记录写明 non-discriminating）。", ""]
        else:
            L += [
                "**断言组：空 —— 现有 19 个封闭谓词表述不出这条**", "",
                "> 该缺陷成立（有 NL 依据或模型自身证据），但当前谓词面给不出可复跑的正面断言，"
                "因此**只能人工验收**。这类共 14 条，构成本集合的自动化上限。", "",
            ]
        u = r["upstream"]
        L += [
            "**上游关联**", "",
            "| 来源 | 值 |", "| --- | --- |",
            f"| 逐对复核主档 | `{u['review_file']}` 的 `diffs[{u['diff_index']}]` |",
            f"| 本 pair 的旧台帐 E1 | "
            + ("、".join(f"`{i}`" for i in u["ledger_e1_ids_on_this_pair"]) or "无") + " |",
            f"| 8 格运行已发布 issue | "
            + ("、".join(f"`{p['issue_id']}`（{p['cell']}）"
                        for p in u["eight_cell_published"]) or "本 pair 未进入 8 格运行") + " |",
            f"| 论文两阶段 F1 | {u.get('paper_f1_phase2') if u.get('paper_f1_phase2') is not None else '—'} |",
            "",
        ]
        if r.get("superseded_assertion"):
            L += [f"> 本条断言经主裁定替换。原断言（含复核者当时的说明）：\n>\n"
                  f"> ```\n> {one_line(r['superseded_assertion'], 2000)}\n> ```\n>\n"
                  f"> 替换理由见 [`nlreview_parent_rulings.json`]"
                  f"(https://gist.github.com/HansBug/{AUDIT_GIST}"
                  f"#file-nlreview_parent_rulings-json)。", ""]
    return "\n".join(L).rstrip() + "\n"


def main() -> int:
    out = pathlib.Path(sys.argv[sys.argv.index("--out") + 1]) if "--out" in sys.argv \
        else MR / "eis_bundle"
    (out / "readable").mkdir(parents=True, exist_ok=True)
    (out / "audit").mkdir(parents=True, exist_ok=True)

    eis = json.loads((MR / "expected_issue_set.json").read_text())
    cov = json.loads((MR / "ledger_coverage.json").read_text())
    by_pair = defaultdict(list)
    for r in eis["records"]:
        by_pair[r["pair"]].append(r)
    cov_by_pair = defaultdict(list)
    for c in cov["entries"]:
        cov_by_pair[c["pair"]].append(c)

    for pair, recs in sorted(by_pair.items()):
        (out / "readable" / f"{pair}-eis.md").write_text(
            render_pair(pair, recs, cov_by_pair.get(pair, [])))

    # The 14 non-automatable records get their own file. They are the set's automation
    # ceiling, and a reader asking "what exactly can the predicates not say?" should not
    # have to grep 48 per-pair files to find out.
    rep_rows = {}
    rp = MR / "loop_audit/replay_attribution.json"
    if rp.exists():
        rep_rows = {(r["case"], r["diff_index"]): r
                    for r in json.loads(rp.read_text())["rows"]}
    noa = [r for r in eis["records"] if not r.get("automatable")]
    GAP_BY_ID = {
        "EIS-0033-02": "缺 `initial_edge_count` / `unique_default_entry` / "
                       "`entry_is_in_scope` 一类谓词；`initial_target` 的拒答语义"
                       "把整个「多默认进入点」族变成不可判定",
    }
    GAP = {
        "A": "`action_declared` 无动作名参数；effect 通道要求「变量 + 符号」，"
             "而该通道在本语料恒为空（全库唯一变量是 converter 的 `R45RouteToken`）",
        "Tr": "`edge_declared` 强制要求具名 trigger，completion 边（无触发）表达不出",
        "V": "R4.5 从不把方括号解析为守卫；作者自有守卫全库为零，"
             "`guard_distinguishable` 的判别分支不可达",
        "S": "S 族全是具名点查询，无存在量词，「壳缺失」只能照搬参考名",
    }
    N = [f"# {len(noa)} 条只能人工验收的记录 —— 逐条明细", "",
         f"这 {len(noa)} 条构成 expected issue set 的**自动化上限**：缺陷成立、可归因，"
         "但现有 19 个封闭谓词给不出可复跑的正面断言。"
         "它们**仍然是 expected issue**——入选条件是「缺陷真实且可归因」，"
         "不是「本工具当前能不能表述它」。按可表述性剔除，就会用工具能力反向定义研究边界。", "",
         f"正文对这批条目的成因分析与扩谓词决策见 [issue #172 §4.3–4.5]({ISSUE_URL})。", "",
         "## 分布", "", "| 维度 | 分布 |", "| --- | --- |",
         "| 元组分量 | " + "、".join(f"**{k}** {v}" for k, v in
                                  Counter(r.get("element_of_M") for r in noa).most_common()) + " |",
         "| 缺陷方向 | " + "、".join(f"`{k}` {v}" for k, v in
                                  Counter(r["direction"] for r in noa).most_common()) + " |",
         "| 归因层 | " + "、".join(f"`{k}` {v}" for k, v in
                                 Counter(r["layer"] for r in noa).most_common()) + " |", "",
         "## 逐条", ""]
    for r in sorted(noa, key=lambda x: x["id"]):
        st = ((rep_rows.get((r["pair"], r["upstream"]["diff_index"])) or {})
              .get("attribution_status") or "declared_not_expressible")
        N += [f"### {r['id']} — `{r['pair']}` {r['group']} × {r['llm']}", "",
              "| 字段 | 值 |", "| --- | --- |",
              f"| 归因层 | `{r['layer']}` |", f"| 缺陷方向 | `{r['direction']}` |",
              f"| 元组分量 | **{r.get('element_of_M')}** |", f"| 归因重放 | `{st}` |",
              # A per-element lookup mislabels 0033#2: its element is Tr but the gap is about
        #初始边作用域/唯一性, not the completion-edge trigger problem the Tr bucket names.
        # Per-record overrides come first.
        f"| 词表缺口 | {GAP_BY_ID.get(r['id']) or GAP.get(r.get('element_of_M'), '—')} |",
              f"| 完整台帐 | [`{r['pair']}-eis.md`](#file-{r['pair']}-eis-md) |", "",
              "**缺陷描述**", "", one_line(r["statement"], 700), ""]
        if r.get("nl_evidence"):
            N += ["**NL 依据**", "", "> " + one_line(r["nl_evidence"], 500), ""]
        if r["assertions"]:
            N += [f"**曾尝试的表达式（{len(r['assertions'])} 条，均不可求值或不判别）**",
                  "", "```python"]
            for a in r["assertions"][:4]:
                N.append(f"# {a['role']} — 实测 {a.get('measured', '—')}")
                N.append(re.sub(r"\s+", " ", a["expression"]).strip()[:300])
            N += ["```", ""]
        else:
            N += ["**断言组：空** —— 复核者尝试后判定 19 谓词写不出。", ""]
        N += ["---", ""]
    (out / "readable" / "00-NOT-AUTOMATABLE.md").write_text("\n".join(N).rstrip() + "\n")

    # Both READMEs are generated, not hand-written: their headline figures were hand-typed
    # once and immediately went stale (the negative-control count said 0 after it became 2).
    t = eis["totals"]
    cov_t = cov.get("totals", {})
    NAV = (f"↩ **正文**：[issue #172]({ISSUE_URL})"
           f" ｜ ↔ **另一面**：")
    (out / "readable" / "00-README.md").write_text(f"""# LLMS-EMP expected issue set — 逐 pair 可读台帐

{NAV}[审计数据 gist](https://gist.github.com/HansBug/{AUDIT_GIST})

本 gist 是 **expected issue set** 的逐 pair 可读面：{t['pairs_covered']} 个 pair、共 **{t['records']}** 条 expected issue。审计数据（机读主档、覆盖校验、谓词复跑、一致性检查）在另一个 gist。

## 每条记录包含什么

| 字段 | 说明 |
| --- | --- |
| 归因层 | 凭什么把这条归因于生成方。四层：`wellformedness`（模型自身 + 良构性/投影语义即可判定）/ `nl_named`（NL 逐字点名该元素）/ `nl_contradiction`（与 NL 显式义务矛盾）/ `over_specification`（凭空多出且有可断言后果）|
| 缺陷方向 | 什么坏了（可达性、初始入口、守卫、层次、动作、事件、伪状态、基数）|
| 触及的元组分量 | 落在 $M = (S, E, V, Tr, A)$ 的哪个分量 |
| 断言组 | 主断言（经复跑）+ 负控 + 佐证。**负控须实测为 `True`**，否则无法排除主断言对正确模型也返回 `False`。超长表达式在表下以可复制的 code block 给出 |
| 上游关联 | 复核主档的 diff 下标、本 pair 的旧台帐 E1、8 格运行已发布 issue、论文两阶段 F1 |

## 本 gist 的两个入口文件

| 文件 | 用途 |
| --- | --- |
| [`00-NOT-AUTOMATABLE.md`](#file-00-not-automatable-md) | 那 {t['needs_human_judgement']} 条只能人工验收的记录，逐条给出元组分量、词表缺口与曾尝试过的表达式 |
| `<pair>-eis.md` | 该 pair 的完整台帐 |

## 必须先知道的四件事

1. **{t['records']} 条中 {t['automatable']} 条可自动验收**（主断言实测返回 `False`），**{t['needs_human_judgement']} 条**只能人工验收（现有 19 个封闭谓词表述不出，或表达式不可求值）。后者构成本集合的自动化上限，逐条标注在各 pair 文件里。
2. **只有 {t['with_negative_control']} 条带经实测验证的负控**（覆盖率 {t['with_negative_control'] / t['records']:.0%}）。复核者在散文里记录过更多负控，但从散文恢复的表达式绝大多数不可求值。**这是本集合已知的最大证据弱点**——没有负控就无法机械排除「正确模型也返回 `False`」。
3. **旧台帐（issue #166 的 47 条）可做 binding 级交代。** frozen ledger 位于 `.omx/specs/…/ledger.json`（SHA-256 `03d8756650c0…`），其 47/47 条带 `eval_assert`。实测 **{cov_t.get('binding_match', 0)} 条 `binding_match`、{cov_t.get('same_pair_only', 0)} 条 `same_pair_only`、{cov_t.get('unaccounted', 0)} 条 `unaccounted`**。⚠️ 本 gist 的早前版本称该台帐已丢失、仅 5 条可比——那是误判，已更正。
4. **归因门控是最重要的限制。** 按流水线自己的裁决契约，非 `safe` 的 `False` 断言强制进 `excluded_findings`、永不成为 confirmed issue。把本集合当命中率分母时必须同时报告归因分层，否则会把按设计不该上报的条目记成漏检。详见正文 §TL;DR 末的归因门控表。

## 判定口径

`correct` / `similar` 不计入问题（语义等价即不计）；`problem` 与 `extra` 走两条不同路径——`problem` 判**可归因性**，`extra` 判**有害性**，因为前者的有害性由定义蕴含、后者的可归因性由来源唯一而免费。四档判定与两条路径的完整定义见 issue 正文 §0.2。
""")
    (out / "audit" / "00-README.md").write_text(f"""# LLMS-EMP expected issue set — 审计数据

{NAV}[逐 pair 可读台帐 gist](https://gist.github.com/HansBug/{READABLE_GIST})

本 gist 是 **expected issue set** 的机读面：**{t['records']}** 条记录、{t['pairs_covered']} 个 pair。

## 文件

| 文件 | 内容 |
| --- | --- |
| `expected_issue_set.json` | **主档**：{t['records']} 条记录，每条含自然语言描述、归因层、缺陷方向、断言组（primary / negative_control / corroborating，各带实测值）、同质组、上游关联 |
| `index.tsv` | 逐 pair 一行：条数、可自动验收数、须人工数、层分布、方向分布、旧台帐 E1 数、是否进入 8 格运行 |
| `ledger_coverage.json` | issue #166 的 47 条逐条对照本集合（读 frozen ledger）|
| `final_stratification.json` | 154 行分层逐行数据，含判定来源与全部主裁定 |
| `defect_classification.json` | 缺陷方向 × 谓词族交叉分类 |
| `reconcile.json` | 交叉一致性检查：多个独立来源报同一批数，任何不一致都会阻断发布 |
| `predcov_*` | 谓词覆盖复跑：五批原始判定 + 独立复跑 + 方法与已知坑 |
| `loopaudit_*` | 8 格运行审计：逐格命中/漏检、**归因重放**、prompt 审计、范畴裁定 |
| `nlreview_*` | NL 复核各批判定、`extra` 有害性判定、**主裁定**、`extra` 归属政策 |

## 计数口径（混用会算错）

| 口径 | 值 | 含义 |
| --- | ---: | --- |
| 记录条数 | {t['records']} | 一条 expected issue 一条记录 |
| 同质组 | {t['homogeneity_groups']} | 同 pair 上主谓词与元素集合相同者视为同一缺陷。当前实际合并 **{t['homogeneity_merges']}** 次——该机制尚未生效 |
| 可自动验收 | {t['automatable']} | 主断言实测返回 `False` |
| 须人工判定 | {t['needs_human_judgement']} | 无可求值主断言 |
| 带实测有效负控 | {t['with_negative_control']} | 负控须实测为 `True` |

## 断言组的三种角色

`primary` 陈述缺陷（须实测 `False`）；`negative_control` 证明主断言不是恒假（**须实测 `True`**）；`corroborating` 补第二个后果。标为 `recovered_unverified` 的是从复核者散文里恢复、未能自动求值的表达式——记录在案以便人工核对，**不计入证据**。
""")

    # index.tsv: one row per pair, machine-readable
    lines = ["pair\tgroup\tllm\teis_count\tautomatable\tneeds_human\tlayers\tdirections\t"
             "ledger_e1_count\tin_eight_cell"]
    for pair, recs in sorted(by_pair.items()):
        lines.append("\t".join([
            pair, recs[0]["group"] or "", recs[0]["llm"] or "", str(len(recs)),
            str(sum(1 for r in recs if r["automatable"])),
            str(sum(1 for r in recs if not r["automatable"])),
            ",".join(f"{k}:{v}" for k, v in Counter(r["layer"] for r in recs).items()),
            ",".join(f"{k}:{v}" for k, v in Counter(r["direction"] for r in recs).items()),
            str(len(recs[0]["upstream"]["ledger_e1_ids_on_this_pair"])),
            "yes" if recs[0]["upstream"]["eight_cell_published"] else "no",
        ]))
    (out / "audit" / "index.tsv").write_text("\n".join(lines) + "\n")

    for name in ["expected_issue_set.json", "ledger_coverage.json", "final_stratification.json",
                 "defect_classification.json", "reconcile.json"]:
        src = MR / name
        if src.exists():
            (out / "audit" / name).write_text(src.read_text())
    for sub, pref in [("predicate_coverage", "predcov"), ("loop_audit", "loopaudit"),
                      ("nl_review", "nlreview")]:
        d = MR / sub
        if d.is_dir():
            for f in sorted(d.iterdir()):
                if f.is_file():
                    (out / "audit" / f"{pref}_{f.name}").write_text(f.read_text())

    nr = len(list((out / "readable").iterdir()))
    na = len(list((out / "audit").iterdir()))
    print(f"readable {nr} 个文件、audit {na} 个文件 → {out}")
    print(f"记录 {eis['totals']['records']} 条，覆盖 {eis['totals']['pairs_covered']} 个 pair")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
