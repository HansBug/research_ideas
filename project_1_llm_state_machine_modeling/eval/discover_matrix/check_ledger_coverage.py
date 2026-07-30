"""Account for every one of issue #166's 47 expected issues against the new set.

Reads the **frozen ledger** at `.omx/specs/autoresearch-paper1-llms-emp-60-expected-issues/
ledger.json`. An earlier version of this script read `expected_issues_reconstructed.json`
instead, on the belief that the frozen ledger had been lost in the 2026-07-29 machine
rebuild. That belief was wrong: the file is in the repository, was committed by `94074e4e`
on 2026-07-29 22:01, its SHA-256 matches the figure published in issue #166, and **47 of 47
findings carry an `eval_assert`** (44 of them with extractable model-element paths). The
reconstruction only ever covered 4 pairs / 5 findings, and `HIT_CRITERION.md` §7 explicitly
forbids computing hit figures from it. Reading the wrong file understated binding-level
coverage by a factor of ~9.

So the question this script answers is the strong one: **for each ledger entry, does the new
set contain a finding whose assertion binds to the same model elements?**

Three outcomes per ledger entry, and the third is the one that matters:

  binding_match     the ledger entry has an `eval_assert` and it shares model elements with
                    a new-set assertion -- machine-decidable, the strongest link
  same_pair_only    the new set has findings on that pair but the link rests on reading the
                    statements, not on binding -- needs a human to confirm or deny
  unaccounted       the new set has NO admissible finding on that pair at all -- either the
                    ledger was wrong, or this review missed something

`unaccounted` is the number that must be zero (or individually explained) before the new set
can claim to supersede the ledger. Anything else would be quietly dropping prior findings.

Usage: check_ledger_coverage.py --i166 <issue-166 body.md> [--json OUT]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
MR = HERE / "manual_review"
#: `.omx` is a dotted directory, so a plain glob for `ledger.json` misses it -- which is how
#: it came to be believed lost. Pin the path explicitly.
FROZEN_LEDGER = (HERE.parents[2] / ".omx/specs"
                 / "autoresearch-paper1-llms-emp-60-expected-issues/ledger.json")

_EXP = re.compile(r"EXP-(\d{4})-([A-Z]{2})-(\d{3})")
_PATH = re.compile(r"llms_emp_feedback_final_\d{4}[\w.]*")

#: `issue_166` category codes, so a reader can see what kind of defect each entry claimed.
#: Verbatim from issue #166 §3's taxonomy table, so the two documents cannot drift apart.
CATEGORY = {
    "IT": "初始化、完成与作用域：初态、终态、局部退出或全局完成缺失、提前或作用域错误",
    "TR": "迁移关系完整性：NL 明确要求的 source-trigger-target 关系缺失，或三者之一错误",
    "SH": "结构与层次完整性：NL 明确要求的状态、子状态、层次归属或区域结构缺失或错置",
    "GC": "条件、选择与冲突：条件缺失或错置，或同一适用条件产生无法区分的冲突目标",
    "EA": "Effect 与动作：NL 明确要求的 effect、赋值、输出或状态局部动作缺失或错误",
    "UA": "未授权行为：额外迁移违反 NL 明确给出的 remain、until、only 或 never 义务",
    "DA": "领域与任务对齐：作者模型属于错误任务领域，或缺少足以识别任务的核心行为",
    "TO": "时间相关（issue #166 的 taxonomy 含此类，但落在 paper1 问题定义之外）",
}


def ledger_entries(i166_text: str) -> dict[str, dict]:
    """Every EXP id in issue #166, with the line it appears on as its statement.

    The per-pair table rows are the authoritative inventory (the issue's own §4), so the row
    text is the closest thing to a statement that survives."""
    out: dict[str, dict] = {}
    for line in i166_text.splitlines():
        for m in _EXP.finditer(line):
            iid = m.group(0)
            if iid in out:
                continue
            cells = [c.strip() for c in line.split("|")] if "|" in line else [line.strip()]
            # The longest cell that is not the id itself carries the description.
            desc = max((c for c in cells if iid not in c), key=len, default="")
            out[iid] = {
                "id": iid, "pair": m.group(1), "category": m.group(2),
                "category_label": CATEGORY.get(m.group(2), "未知类别"),
                "statement_from_i166": re.sub(r"\s+", " ", desc)[:400],
            }
    return out


def main() -> int:
    if "--i166" not in sys.argv:
        print("需要 --i166 <path>：issue #166 的 body 文本")
        return 2
    i166 = pathlib.Path(sys.argv[sys.argv.index("--i166") + 1]).read_text()
    entries = ledger_entries(i166)

    eis = json.loads((MR / "expected_issue_set.json").read_text())
    by_pair: dict[str, list] = defaultdict(list)
    for r in eis["records"]:
        by_pair[r["pair"]].append(r)

    # The frozen ledger is authoritative. Fall back to the reconstruction only if it is
    # absent, and say so loudly, because the two give very different coverage figures.
    recon_assert: dict[str, set[str]] = {}
    provenance = "missing"
    frozen = FROZEN_LEDGER
    if frozen.exists():
        provenance = "frozen"
        payload = json.loads(frozen.read_text())
        for f in payload.get("findings") or []:
            if f.get("issue_id") and f.get("eval_assert"):
                recon_assert[f["issue_id"]] = set(_PATH.findall(f["eval_assert"]))
            # `source_trace_bindings` names elements the ledger itself resolved, so fold
            # them in: they are the same claim stated as data rather than as an expression.
            for b in f.get("source_trace_bindings") or []:
                for v in (b.values() if isinstance(b, dict) else [b]):
                    if isinstance(v, str):
                        recon_assert.setdefault(f["issue_id"], set()).update(
                            _PATH.findall(v))
    else:
        rp = HERE / "expected_issues_reconstructed.json"
        if rp.exists():
            provenance = "reconstructed"
            def walk(o):
                if isinstance(o, dict):
                    if o.get("issue_id") and o.get("eval_assert"):
                        recon_assert[o["issue_id"]] = set(_PATH.findall(o["eval_assert"]))
                    for v in o.values():
                        walk(v)
                elif isinstance(o, list):
                    for v in o:
                        walk(v)
            walk(json.loads(rp.read_text()))

    results = []
    for iid, e in sorted(entries.items()):
        cands = by_pair.get(e["pair"], [])
        outcome, matched = "unaccounted", []
        if iid in recon_assert and recon_assert[iid]:
            for r in cands:
                for a in r["assertions"]:
                    if recon_assert[iid] & set(a.get("elements") or []):
                        matched.append(r["id"])
                        break
            if matched:
                outcome = "binding_match"
        if outcome != "binding_match" and cands:
            outcome = "same_pair_only"
            matched = [r["id"] for r in cands]
        results.append({**e, "outcome": outcome,
                        "has_reconstructed_eval_assert": iid in recon_assert,
                        "new_set_matches": matched,
                        "new_set_findings_on_pair": len(cands)})

    tally = Counter(r["outcome"] for r in results)
    print(f"台帐来源：**{provenance}**"
          + (f"（{frozen}）" if provenance == "frozen" else "")
          + f"；其中 {sum(1 for e in entries if e in recon_assert)} / {len(entries)} "
            f"条有可提取的 binding\n")
    if provenance != "frozen":
        print("⚠️ 未使用 frozen ledger —— HIT_CRITERION.md §7 禁止基于重建版计算命中数字\n")
    print(f"issue #166 的 expected issue：**{len(results)}** 条\n")
    print("| 交代结果 | 条数 | 含义 |")
    print("| --- | ---: | --- |")
    print(f"| `binding_match` | **{tally['binding_match']}** | "
          f"旧条目有 `eval_assert`，且与新集合某条断言共享模型元素——机器可判 |")
    print(f"| `same_pair_only` | **{tally['same_pair_only']}** | "
          f"新集合在该 pair 上有条目，但关联只能靠读陈述，需人工确认 |")
    print(f"| `unaccounted` | **{tally['unaccounted']}** | "
          f"新集合在该 pair 上**没有任何可入条目**——必须逐条解释 |")
    print(f"| **合计** | **{len(results)}** | |")

    print(f"\n按类别：")
    print("| 类别 | 条数 | 含义 |")
    print("| --- | ---: | --- |")
    for c, n in Counter(r["category"] for r in results).most_common():
        print(f"| `{c}` | {n} | {CATEGORY.get(c, '未知')} |")

    un = [r for r in results if r["outcome"] == "unaccounted"]
    if un:
        print(f"\n### 未被交代的 {len(un)} 条——每条都需要解释\n")
        print("| 旧条目 | pair | 类别 | 该 pair 在新集合中的可入条数 |")
        print("| --- | --- | --- | ---: |")
        for r in un:
            print(f"| `{r['id']}` | `{r['pair']}` | {r['category']} | "
                  f"{r['new_set_findings_on_pair']} |")

    covered_pairs = {r["pair"] for r in results}
    print(f"\n旧台帐涉及 {len(covered_pairs)} 个 pair；"
          f"新集合覆盖 {eis['totals']['pairs_covered']} 个 pair")
    only_new = sorted({r["pair"] for r in eis["records"]} - covered_pairs)
    print(f"**只在新集合里有条目的 pair：{len(only_new)} 个** —— "
          f"这些是旧台帐完全没有记录的：" + "、".join(f"`{p}`" for p in only_new))

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is":
                "把 issue #166 的 47 条 expected issue 逐条对照新集合。"
                "旧台帐 ledger.json 已丢失、47 条中仅 5 条有重建的 eval_assert，"
                "因此只有那 5 条能做 binding 级比对，其余只能确认『该 pair 在新集合中有条目』"
                "并留待人工确认。unaccounted 必须为 0 或逐条解释，否则新集合不能声称取代旧台帐。",
            "ledger_provenance": provenance,
            "ledger_path": str(frozen if provenance == "frozen" else "reconstructed"),
            "totals": {**dict(tally), "ledger_entries": len(results),
                       "pairs_in_ledger": len(covered_pairs),
                       "pairs_only_in_new_set": only_new},
            "entries": results,
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
