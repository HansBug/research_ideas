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

HERE = pathlib.Path(__file__).resolve().parent
MR = HERE / "manual_review"

#: The audit gist and the issue, so cross-references in the readable ledgers are clickable
#: rather than telling the reader to go find them.
AUDIT_GIST = "e92fb6ca165b46d19b1638f03ae93842"
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
              "`same_pair_only` = 只能确认本 pair 有新条目，具体对应需人工判定"
              "（旧台帐 47 条中仅 5 条留有 `eval_assert`，其余在 2026-07-29 机器重建中丢失）。",
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
                      "也返回 `False` 的可能（本轮 18 条 benign 中有 5 条正是因此被拒）。", ""]
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
