"""Classify the admissible findings by defect direction, and cross that with predicate coverage.

Two questions that look like one but are not:

  *what broke*        the defect direction -- read off the reviewer's `reason`, which says
                      what the model got wrong
  *can we say it*     whether one of the 19 closed predicates expresses it -- read off the
                      `assertable` field, which says how to assert it

Crossing them is the point. A direction with many findings and no predicate is a
vocabulary gap; a predicate carrying many directions is doing work it was not scoped for;
and a direction whose findings all rest on existence predicates is one where we can say
"the model lacks X" but not "and therefore it misbehaves".

Direction is decided by the *first* matching rule, ordered so the more specific structural
claim wins over the generic one -- a reason may mention a missing state and a dead end, and
the dead end is the sharper statement.

Usage: classify_defects.py [--json <out>]
"""

from __future__ import annotations

import json
import pathlib
import re
import sys
from collections import Counter, defaultdict

HERE = pathlib.Path(__file__).resolve().parent
REVIEWS = HERE / "manual_review"

CLOSED = {
    "state_declared": "S", "variable_declared": "S", "event_declared": "S",
    "containment": "S", "initial_target": "S", "edge_declared": "S",
    "effect_declared": "S", "action_declared": "S", "guard_distinguishable": "S",
    "cardinality": "S", "occupancy_after": "B", "event_consumed": "B",
    "stays_in": "B", "variable_delta_after": "B", "reaches": "B", "terminates": "B",
    "invariant": "P", "response_within": "P", "persists_until": "P",
}
#: Predicates that only witness presence. For a missing NL-named element that is the whole
#: claim; for a *consequence* it is not -- "the model lacks X" does not say "and therefore
#: it misbehaves", which is what makes a finding hard to dispute.
EXISTENCE_ONLY = {"state_declared", "event_declared", "variable_declared",
                  "edge_declared", "effect_declared", "action_declared"}

#: Ordered. Earlier rules are the sharper claim.
DIRECTIONS: list[tuple[str, str, str]] = [
    ("reachability", "可达性与终止：死端、吸收态、不可达、无终态、不能终止", "|".join([
        r"死端", r"吸收", r"不可达", r"无法到达", r"到不了", r"停滞", r"永久停",
        r"无出边", r"无任何出边", r"死代码", r"无入边", r"活锁", r"死锁",
        r"永远无法结束", r"永不终止", r"不能终止", r"无终态", r"没有终态",
        r"无 ?final", r"终结", r"完成路径", r"不可重入",
    ])),
    ("entry", "初始入口：缺初始边、带触发的初始边、多个竞争入口、默认子态错", "|".join([
        r"初始边", r"初始迁移", r"默认进入", r"默认子[态状]", r"初始子状态",
        r"初始伪状态", r"缺初始", r"无初始", r"非确定初始", r"入口",
        r"UnspecifiedInitial", r"竞争初始", r"冷启动", r"first transitions",
    ])),
    ("hierarchy", "层次归属：containment 丢失、错误嵌套、复合态未展开、作用域错", "|".join([
        r"层次", r"子态", r"子状态", r"复合[态状]", r"归属", r"嵌套", r"平铺",
        r"submachine", r"包壳", r"wrapper", r"兄弟[态状]", r"作用域", r"上层状态",
    ])),
    ("guard", "守卫与条件：缺守卫、不可区分、位置错、条件被折进事件名", "|".join([
        r"守卫", r"guard", r"不可区分", r"无法区分", r"条件", r"阈值",
        r"\[.{0,24}\]", r"判据", r"消歧",
    ])),
    ("event", "事件与触发：事件缺失、被压成复合名、自造事件、触发方向错", "|".join([
        r"事件", r"触发", r"trigger", r"复合事件", r"压成", r"事件名",
        r"自造", r"凭空", r"方向", r"标签",
    ])),
    ("effect_action", "动作与 effect：entry/exit 动作缺失、变量增减缺失", "|".join([
        r"effect", r"动作", r"entry", r"exit", r"递减", r"计数", r"变量",
        r"赋值", r"输出信号",
    ])),
    ("cardinality", "元素数量：NL 点名 N 个而模型 M 个、克隆件、区域数", "|".join([
        r"数量断言", r"三个", r"个具名", r"克隆", r"枚举", r"区域数", r"个区域",
        r"只剩", r"多出一个",
    ])),
    ("pseudostate", "伪状态类型：fork / join / junction / choice 未声明或错配", "|".join([
        r"伪状态", r"pseudo", r"fork", r"join", r"junction", r"choice",
    ])),
    ("target_scope", "迁移目标：目标状态错、边接错位置", "|".join([
        r"目标", r"接到", r"接线", r"挂在", r"指向", r"边的源", r"源端",
    ])),
]
_COMPILED = [(k, re.compile(p)) for k, _d, p in DIRECTIONS]


def direction(reason: str) -> tuple[str, str]:
    for name, pattern in _COMPILED:
        if m := pattern.search(reason or ""):
            return name, m.group(0)[:20]
    return "unclassified", ""


def predicates(assertable: str) -> list[str]:
    bare = re.sub(r"(['\"]).*?\1", "''", assertable or "", flags=re.S)
    seen = []
    for m in re.findall(r"[A-Za-z_][A-Za-z_0-9]*\s*\(", bare):
        name = m.rstrip("( ")
        if name in CLOSED and name not in seen:
            seen.append(name)
    return seen


def main() -> int:
    fin = json.loads((REVIEWS / "final_stratification.json").read_text())
    admissible = set(fin["admissible_strata"])
    reasons: dict[tuple[str, int], dict] = {}
    for path in sorted(REVIEWS.glob("*-review.json")):
        review = json.loads(path.read_text())
        for i, diff in enumerate(review.get("diffs") or []):
            reasons[(review["case"], i)] = diff
    rows = []
    for r in fin["rows"]:
        if r["stratum"] not in admissible:
            continue
        diff = reasons[(r["case"], r["diff_index"])]
        d, trig = direction(diff.get("reason") or "")
        ps = predicates(r["assertable"])
        rows.append({**r, "direction": d, "direction_trigger": trig, "predicates": ps,
                     "primary_predicate": ps[0] if ps else None,
                     "existence_only": bool(ps) and all(p in EXISTENCE_ONLY for p in ps)})

    print(f"可入 expected issue **{len(rows)}** 条，按缺陷方向与谓词覆盖交叉分类\n")
    by_dir = Counter(r["direction"] for r in rows)
    print("## 缺陷方向\n")
    print("| 方向 | 条数 | 占比 | 含义 |")
    print("| --- | ---: | ---: | --- |")
    for name, desc, _p in DIRECTIONS:
        if by_dir[name]:
            print(f"| `{name}` | **{by_dir[name]}** | {by_dir[name]/len(rows):.0%} | {desc} |")
    if by_dir["unclassified"]:
        print(f"| `unclassified` | {by_dir['unclassified']} | "
              f"{by_dir['unclassified']/len(rows):.0%} | 关键词未命中 |")

    print("\n## 谓词覆盖\n")
    by_pred = Counter(r["primary_predicate"] or "<无>" for r in rows)
    print("| 谓词 | 族 | 条数 | 只能证明存在性 |")
    print("| --- | :-: | ---: | :-: |")
    for name, n in by_pred.most_common():
        fam = CLOSED.get(name, "—")
        eo = "✓" if name in EXISTENCE_ONLY else ""
        print(f"| `{name}` | {fam} | {n} | {eo} |")
    unused = sorted(set(CLOSED) - set(by_pred))
    print(f"\n**19 个谓词中未被用到的 {len(unused)} 个**："
          + "、".join(f"`{u}`" for u in unused))
    eo_n = sum(1 for r in rows if r["existence_only"])
    print(f"\n**只能给出存在性断言的 {eo_n} 条**（{eo_n/len(rows):.0%}）"
          f"——能说「模型缺 X」，不能说「因此行为坏了」")
    no_pred = [r for r in rows if not r["predicates"]]
    print(f"**无任何封闭谓词可表达的 {len(no_pred)} 条**："
          + "、".join(f"`{r['case']}`#{r['diff_index']}" for r in no_pred))

    print("\n## 方向 × 谓词族\n")
    fam_of = lambda r: CLOSED.get(r["primary_predicate"], "—")
    grid: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        grid[r["direction"]][fam_of(r)] += 1
    print("| 方向 | S 结构 | B 行为 | P 性质 | 无谓词 | 合计 |")
    print("| --- | ---: | ---: | ---: | ---: | ---: |")
    for name, _d, _p in DIRECTIONS + [("unclassified", "", "")]:
        if not by_dir[name]:
            continue
        g = grid[name]
        print(f"| `{name}` | {g['S']} | {g['B']} | {g['P']} | {g['—']} | **{by_dir[name]}** |")
    tot = Counter()
    for g in grid.values():
        tot.update(g)
    print(f"| **合计** | **{tot['S']}** | **{tot['B']}** | **{tot['P']}** | "
          f"**{tot['—']}** | **{len(rows)}** |")

    print("\n## 方向 × 可归因层\n")
    grid2: dict[str, Counter] = defaultdict(Counter)
    for r in rows:
        grid2[r["direction"]][r["stratum"]] += 1
    strata = ["wellformedness", "nl_named", "nl_contradiction", "over_specification"]
    print("| 方向 | " + " | ".join(s.replace("_", " ") for s in strata) + " |")
    print("| --- | " + " | ".join(["---:"] * len(strata)) + " |")
    for name, _d, _p in DIRECTIONS + [("unclassified", "", "")]:
        if not by_dir[name]:
            continue
        print(f"| `{name}` | " + " | ".join(str(grid2[name][s]) for s in strata) + " |")

    if "--json" in sys.argv:
        dest = pathlib.Path(sys.argv[sys.argv.index("--json") + 1])
        dest.write_text(json.dumps({
            "what_this_is": "130 条可入 expected issue 的缺陷方向分类与谓词覆盖交叉。"
                            "方向读自 reason（什么坏了），谓词读自 assertable（能否表达）。",
            "totals": {"admissible": len(rows), "by_direction": dict(by_dir),
                       "by_primary_predicate": dict(by_pred),
                       "existence_only": eo_n, "no_predicate": len(no_pred),
                       "unused_predicates": unused},
            "rows": rows,
        }, ensure_ascii=False, indent=1) + "\n")
        print(f"\n已写 {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
