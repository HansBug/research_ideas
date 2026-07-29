"""Stratify the 154 in-scope findings into what can and cannot become an expected issue.

Issue #171 §2 argues the whole set must not be admitted wholesale: the paper's own
requirement template forbids stating element counts or inter-element relations, so the NL
is constructively underdetermined and the reference model is one arbitrary member of the
set of NL-consistent models. Scoring against that member measures "guessed the author's
private model", not "modelled the requirement".

What survives that objection is three classes, and they are the strata here:

  wellformedness   defects readable from the model alone, with no oracle needed: an
                   untriggered completion edge that pre-empts a declared branch, a
                   triggered initial edge, a composite with no default substate, a dead
                   end / absorbing state / unreachable region
  nl_named         the NL names the element and the model does not have it
  nl_contradiction the model contradicts an explicit NL obligation

and one that does not:

  reference_only   present in the reference, absent from the NL. Real as a difference,
                   but not attributable to the generated model.

Classification is lexical over the reviewer's `reason`, which makes it a *proposal*, not a
verdict -- every row carries the phrase that triggered it so a reader can overrule it. The
point is to turn "how should we stratify" from a position into a number that can be
recomputed and argued with.

Usage: stratify_candidates.py [--json <out>]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
REVIEWS = HERE / "manual_review"

#: Ordered: the first stratum whose pattern matches wins, because a reason can mention
#: several things and the strongest ground should decide. Well-formedness first -- it
#: needs no oracle at all, so it is the least contestable.
#:
#: Regex rather than substrings, for one reason found the hard way: reviewers cite the NL
#: as `NL 第 3 句`, `NL 3`, `NL 3/4`, and `NL 逐句点名` interchangeably. A literal
#: `"NL 第"` needle left 48 of 154 rows unclassified, nearly all of which did cite the NL.
STRATA: list[tuple[str, str, str]] = [
    ("wellformedness", "良构性：无需 oracle，仅凭模型自身即可判定", "|".join([
        r"死端", r"吸收", r"不可达", r"停滞", r"无出边", r"无任何出边",
        r"无入边", r"无任何入边", r"死代码",
        r"缺默认子状态", r"无默认子态", r"默认子态", r"初始子状态",
        r"缺初始", r"无初始", r"非确定初始", r"初始迁移带", r"初始边带",
        r"带触发的初始", r"触发的初始边", r"三条初始", r"多条初始",
        r"completion", r"即发", r"抢占", r"挤压", r"活锁", r"死锁",
        r"永久停在", r"重入", r"不能终止", r"到不了", r"终态不可达", r"入口停滞",
        r"UML 不允许", r"结构违法", r"不是合法",
    ])),
    ("nl_contradiction", "与 NL 显式义务矛盾", "|".join([
        r"违反\s*NL", r"与\s*NL\s*相反", r"与\s*NL\s*矛盾", r"与\s*NL\s*显式",
        r"方向相反", r"方向写反", r"不符合\s*NL", r"违背\s*NL", r"与\s*NL\s*冲突",
    ])),
    # Exclusion before admission, and the order is load-bearing: "NL 未点名" contains
    # "点名", so with `nl_named` first every reference-only row was swallowed by it and
    # this stratum collapsed to a single row. Whether the NL *fails* to name something is
    # the stronger signal, so it decides first.
    ("reference_only", "仅存在于参考、NL 未点名——不可归因于生成方", "|".join([
        r"参考独有", r"NL\s*未提及", r"NL\s*未点名", r"NL\s*未要求", r"NL\s*未说",
        r"NL\s*没有", r"NL\s*未给", r"NL\s*无对应", r"NL\s*从未", r"NL\s*不要求",
        r"参考侧存疑", r"参考模型自身", r"参考自身", r"仅参考", r"NL\s*未把",
        r"NL\s*未涉及", r"NL\s*完全未",
    ])),
    ("nl_named", "NL 点名的元素缺失或错位", "|".join([
        r"NL\s*第", r"NL\s*\d", r"点名", r"NL\s*要求", r"NL\s*说", r"NL\s*明确",
        r"NL\s*逐字", r"NL\s*原文", r"NL\s*中的", r"NL\s*给", r"NL\s*描述",
    ])),
]
_COMPILED = [(name, re.compile(pattern)) for name, _d, pattern in STRATA]


def classify(reason: str) -> tuple[str, str]:
    """Return (stratum, the phrase that decided it)."""
    text = reason or ""
    for name, pattern in _COMPILED:
        if m := pattern.search(text):
            return name, m.group(0)
    return "unclassified", ""


def main() -> int:
    rows = []
    for path in sorted(REVIEWS.glob("*-review.json")):
        review = json.loads(path.read_text())
        case = review["case"]
        cross = review.get("cross_reference") or {}
        e1 = set((cross.get("ledger") or {}).get("e1_ids") or [])
        for index, diff in enumerate(review.get("diffs") or []):
            if diff.get("verdict") not in {"problem", "extra"}:
                continue
            if diff.get("out_of_scope"):
                continue
            stratum, trigger = classify(diff.get("reason") or "")
            rows.append({
                "case": case,
                "group": cross.get("group"),
                "llm": cross.get("llm"),
                "diff_index": index,
                "verdict": diff["verdict"],
                "stratum": stratum,
                "trigger": trigger,
                "assertable": (diff.get("assertable") or "").strip(),
                "predicate_exists": diff.get("predicate_exists"),
                "case_has_ledger_e1": bool(e1),
                "reason_head": (diff.get("reason") or "")[:120],
            })

    by_stratum = Counter(r["stratum"] for r in rows)
    admissible = {"wellformedness", "nl_contradiction", "nl_named"}
    # Printed in STRATA order, so the exclusion stratum appears where it decides.
    adm = [r for r in rows if r["stratum"] in admissible]
    print(f"计入问题 {len(rows)} 条（problem + extra，已排除范围外）\n")
    print("| 层 | 条数 | 可入 E1 | 说明 |")
    print("| --- | ---: | :-: | --- |")
    for name, desc, _pat in STRATA:
        print(f"| `{name}` | {by_stratum[name]} | {'✓' if name in admissible else '✗'} | {desc} |")
    print(f"| `unclassified` | {by_stratum['unclassified']} | ? | 词法判据未命中，需人工归层 |")
    # Report a range, not a point. `nl_named` fires on any reason that cites the NL at
    # all, and citing the NL is not the same as the NL having *named the missing element*
    # -- a reason often opens with the NL sentence and then says the reference added
    # something beyond it. So the lexical count is an upper bound on that stratum.
    # `wellformedness` needs no oracle and `nl_contradiction` quotes an explicit clash;
    # those two are the defensible floor.
    floor = by_stratum["wellformedness"] + by_stratum["nl_contradiction"]
    print(f"\n**可入 E1 的区间：{floor} – {len(adm)}**（共 {len(rows)} 条计入问题）")
    print(f"- 下界 **{floor}**：`wellformedness` + `nl_contradiction`。前者无需 oracle、"
          f"后者引了 NL 的显式冲突，是最难被反驳的两层")
    print(f"- 上界 **{len(adm)}**：再加上 `nl_named` {by_stratum['nl_named']} 条。"
          f"该层是**上界**——词法判据只要理由里提到 NL 就命中，而提到 NL ≠ NL 点名了缺失的那个元素")
    print(f"- 明确不可入 **{by_stratum['reference_only']}** 条，待人工归层 "
          f"**{by_stratum['unclassified']}** 条")

    # The point of stratum 2 (whether to backfill the 23 missed cases) is what it adds on
    # top of the ledger's existing 47, so split by whether the case already carries an E1.
    fresh = [r for r in adm if not r["case_has_ledger_e1"]]
    print(f"\n其中落在**台帐无 E1 的 case** 上：**{len(fresh)}** 条 "
          f"（分布在 {len({r['case'] for r in fresh})} 个 case）"
          f"——这是裁决点 2「补录」的实际增量上界")
    with_pred = sum(1 for r in adm if r["predicate_exists"] is True and r["assertable"])
    print(f"可入 E1 的 {len(adm)} 条中，有 assertable 且标 predicate_exists 的：{with_pred}")

    print("\n### 按 NL 组")
    print("| NL 组 | 可入 E1 | 良构性 | NL 矛盾 | NL 点名 | 仅参考 | 未归层 |")
    print("| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    per: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        per[r["group"]][r["stratum"]] += 1
    for group in sorted(per):
        c = per[group]
        print(f"| {group} | **{sum(c[k] for k in admissible)}** | {c['wellformedness']} | "
              f"{c['nl_contradiction']} | {c['nl_named']} | {c['reference_only']} | "
              f"{c['unclassified']} |")

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is": (
                "154 条计入问题按三类可入 E1 判据 + 一类不可归因的分层提案。"
                "词法判据，每行带触发词，是提案不是判定。"
            ),
            "admissible_strata": sorted(admissible),
            "totals": {
                "in_scope": len(rows),
                "admissible_upper": len(adm),
                "admissible_floor": by_stratum["wellformedness"] + by_stratum["nl_contradiction"],
                "floor_note": (
                    "下界 = wellformedness + nl_contradiction，无需 oracle 或引了 NL 显式冲突；"
                    "上界再加 nl_named，而该层是上界——词法判据只要理由提到 NL 就命中，"
                    "提到 NL 不等于 NL 点名了缺失的那个元素。"
                ),
                "by_stratum": dict(by_stratum),
                "admissible_on_cases_without_ledger_e1": len(fresh),
                "admissible_with_assertable": with_pred,
            },
            "rows": rows,
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
