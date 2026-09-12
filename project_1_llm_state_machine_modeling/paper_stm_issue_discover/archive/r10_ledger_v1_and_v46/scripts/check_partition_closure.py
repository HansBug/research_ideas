"""覆盖侧与多报侧是否切的同一刀：`hit-evidence ∩ 台账外 = ∅`，以及跨侧一致性 $\\kappa_{cross}$。

## 为什么需要它

上一代次的 `台账命中 79 / 台账外 160` 这个划分**不闭合**。覆盖侧用**人工判定表**、多报侧用**机械匹配
的补集** —— 两个不同的匹配器切同一批已发布 issue，而没有任何检查确认两刀切出来的是同一刀。实测至少
**23/82 = 28.0%** 的多报项，其底层 issue 在人工判定表里已被记为该轮命中。

这类错误之所以能长期存在，是因为**它在两个指标上都产生了看起来有利的效果**：判未命中压低覆盖率
（显得保守可信），判有据额外压低虚构率（显得精确）。**没有任何单侧检查会觉得可疑。**

而 Cohen $\\kappa$ 对它**结构性失明**：$\\kappa$ 测的是「两个判定者对**同一问题**是否一致」，而这类错误
是「同一批对象被**两个不同问题**各判一次」。更致命的是两位判定者若读同一份带倾向的指令，共享偏倚下
$\\kappa$ 可以是 1.000 而两人同时错。

## 两个检查

### 不变量 1（划分）`hit-evidence ∩ 台账外 = ∅`

对每个多报项，用**冻结机械匹配器**（`round_variance` 的 `_issue_signature` + `_match`，其判定逻辑早于
v21、**不随判据变化**，这正是它有资格做对照的原因）回溯它的底层 issue；若该 issue 匹配到某台账条目、
且该条目在人工判定表里该轮恰为 `1`，即为**双计**。

### $\\kappa_{cross}$（跨侧一致性）—— ⚠️ 已知系统性低估，读它前先读这段

人工判定 vs 冻结机械匹配器，在 (台账条目 × 格 × 轮) 上算 Cohen $\\kappa$。本实现在 v22 上给出
**0.215**（193 位，一致 60.6%，`only_human` 74 / `only_mechanical` 2）。

**这个 0.215 系统性偏低，原因是两个判定器的表达力不同，不是判定不一致。** `_match` 只在「某条 issue
的元素集与某台账条目重叠」时命中，而人工判定的 1 可以来自判据 §3 的形态 ③（负向对偶）与 ④（蕴含更
上游）—— **那正是重叠式匹配器按设计抓不到的**。所以 `only_human = 74` 里绝大部分不是分歧。

📌 根因分析报的是 **0.714**。我无法在不知道它定义域口径的情况下复现，**故此处报我能复算的 0.215 并
标注低估方向，不去凑那个数**。差额需要它给出定义域后才能对齐。

**这个指标的设计缺陷值得记**：它对「判据表达力差异」与「判定不一致」不加区分，而两者含义完全不同。
在改进之前，它只能用于**定位需要人读的位**（`only_human` / `only_mechanical` 两格的成员），
**不能作为判定质量的度量**。

它与判定者间的 $\\kappa$ 仍是两个不同的量，必须并列报：$\\kappa_{judge}$ 高 = 同一问题可重复；
$\\kappa_{cross}$ 高 = 判定与一个不随判据移动的参照物一致。**前者高不能替后者作证。**

## 机械匹配器只是对照物，不是判据

`docs/protocol/hit_criterion.md` §5 把终局判定保留给人，理由有实证：`present_for_judgment.py` 的 docstring 记着两例
「触及了正确元素却得出**相反**结论」，任何重叠式匹配器都会判它们命中。所以 $\\kappa_{cross} < 1$ 不等于
人工判定错 —— 它只是说两者在哪些位上分歧，而那些位**需要人读**。

用法：`check_partition_closure.py <verdicts.json> [--over blind_sample/overreport_part*.json] [--json]`
非零退出以 gate 发布。
"""

from __future__ import annotations

import argparse
import collections
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import round_variance as rv  # noqa: E402

RUNS = HERE.parents[2] / "runs" / "paper1"


def _cell_issues(base: pathlib.Path, pair: str, arm: str) -> dict[str, list]:
    """→ {run: [(issue, requirements)]}，跳过 `.try` 作废目录。"""

    out: dict[str, list] = {}
    for run_dir in sorted(base.glob("run*")):
        cell = run_dir / f"{pair}-{arm}"
        final = cell / "discover-completed.json"
        if not final.is_file():
            continue
        payload = json.loads(final.read_text())
        reqs = {
            r.get("requirement_id"): r
            for r in rv._find_requirements(payload)
            if r.get("requirement_id")
        }
        out[run_dir.name] = [(i, reqs) for i in (payload.get("issues") or [])]
    return out


def double_counted(verdicts: dict, over_items: list[dict], generation: str) -> dict:
    """不变量 1：被记为命中证据的 issue 不得同时出现在多报池里。"""

    base = RUNS / f"matrix-{generation}"
    ledger = rv._ledger_by_pair()
    hits, misses, unmatched, problems = 0, 0, 0, []
    for item in over_items:
        pair, arm = item.get("pair"), item.get("arm")
        title = str(item.get("claim_title") or "")[:60]
        if not (pair and arm and title):
            continue
        found = None
        for run, issues in _cell_issues(base, pair, arm).items():
            for issue, reqs in issues:
                text = str(issue.get("title") or issue.get("summary") or "")
                if text[:60] != title:
                    continue
                match = rv._match(rv._issue_signature(issue, reqs), ledger.get(pair, []))
                if match:
                    found = (match[0], run)
        if not found:
            unmatched += 1
            continue
        record_id, run = found
        index = int(run[3:]) - 1
        series = (verdicts.get(record_id) or {}).get(arm)
        if isinstance(series, list) and index < len(series) and series[index] == 1:
            hits += 1
            problems.append({
                "item_id": item.get("item_id"), "record_id": record_id,
                "arm": arm, "run": run,
                "why": "该 issue 既是命中证据、又在多报池里",
            })
        else:
            misses += 1
    return {
        "over_items": len(over_items),
        "matched_to_ledger": hits + misses,
        "double_counted": hits,
        "matched_but_judged_miss": misses,
        "unmatched": unmatched,
        "violations": problems,
        "invariant": "hit-evidence ∩ 台账外 = ∅",
        "holds": hits == 0,
    }


def kappa_cross(verdicts: dict, generation: str) -> dict:
    """人工判定 vs 冻结机械匹配器，在 (台账条目 × 格 × 轮) 上。"""

    base = RUNS / f"matrix-{generation}"
    ledger = rv._ledger_by_pair()
    pairs: list[tuple[int, int]] = []
    for pair, entries in sorted(ledger.items()):
        for arm in ("claude", "gpt"):
            per_run = _cell_issues(base, pair, arm)
            if not per_run:
                continue
            for run, issues in sorted(per_run.items()):
                index = int(run[3:]) - 1
                mech = set()
                for issue, reqs in issues:
                    match = rv._match(rv._issue_signature(issue, reqs), entries)
                    if match:
                        mech.add(match[0])
                # 该轮零发布时跳过：那时机械侧与人工侧都没有可判对象。
                #
                # ⚠️ 但这**不足以**消除低估。真正的原因是 `_match` 的定义域比人工判据窄：它只认元素
                # 重叠，而人工可依判据 §3 的形态 ③/④ 用完全不同的元素表达同一命题。加这道过滤后
                # `only_human` 仍是 74，κ 仍是 0.215 —— 所以低估是**表达力差异**，不是「无数据被
                # 当成判 0」。首版注释把成因写成后者，是错的，已改。
                if not issues:
                    continue
                for entry in entries:
                    rid = entry["id"]
                    series = (verdicts.get(rid) or {}).get(arm)
                    if not isinstance(series, list) or index >= len(series):
                        continue
                    human = series[index]
                    if human is None:
                        continue
                    pairs.append((int(human), 1 if rid in mech else 0))
    if not pairs:
        return {"positions": 0, "kappa_cross": None,
                "note": "零输入。空结果与「完全一致」不可区分，所以这是错误而不是 κ=1"}
    n = len(pairs)
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    a1 = sum(1 for a, _ in pairs if a == 1) / n
    b1 = sum(1 for _, b in pairs if b == 1) / n
    pe = a1 * b1 + (1 - a1) * (1 - b1)
    kappa = None if pe >= 1.0 else round((po - pe) / (1 - pe), 3)
    cm = collections.Counter(pairs)
    return {
        "positions": n,
        "agreement": f"{agree}/{n} = {po * 100:.1f}%",
        "human_hit_rate": f"{a1 * 100:.1f}%",
        "mechanical_hit_rate": f"{b1 * 100:.1f}%",
        "kappa_cross": kappa,
        "only_human": cm[(1, 0)],
        "only_mechanical": cm[(0, 1)],
        "note": ("与判定者间的 κ 是两个不同的量，必须并列报。前者高不能替后者作证 —— "
                 "机械匹配器有资格做对照，正是因为它不随判据变化。"),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("verdicts", type=pathlib.Path)
    parser.add_argument("--generation", default="v22")
    parser.add_argument("--over", nargs="*", type=pathlib.Path, default=[])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    verdicts = json.loads(args.verdicts.read_text()).get("verdicts") or {}
    if not verdicts:
        raise SystemExit(f"ERROR: no verdicts in {args.verdicts}")

    over: list[dict] = []
    for path in args.over:
        over += json.loads(path.read_text()).get("items") or []

    result: dict = {"generation": args.generation, "kappa_cross": kappa_cross(verdicts, args.generation)}
    if over:
        result["partition"] = double_counted(verdicts, over, args.generation)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=1))
    else:
        k = result["kappa_cross"]
        print(f"κ_cross（人工判定 vs 冻结机械匹配器）@ {args.generation}")
        for key in ("positions", "agreement", "human_hit_rate", "mechanical_hit_rate",
                    "kappa_cross", "only_human", "only_mechanical"):
            print(f"  {key:22s} {k.get(key)}")
        if "partition" in result:
            p = result["partition"]
            print(f"\n划分闭合性（不变量：{p['invariant']}）")
            for key in ("over_items", "matched_to_ledger", "double_counted",
                        "matched_but_judged_miss", "unmatched"):
                print(f"  {key:24s} {p[key]}")
            print(f"  {'成立？':22s} {'✅' if p['holds'] else '❌'}")
            for v in p["violations"][:6]:
                print(f"    双计: {v['item_id']} → {v['record_id']}[{v['arm']}] {v['run']}")
        print(f"\n{k['note']}")

    # 不变量不成立即非零退出，用于 gate 发布。首版写成 `.get("holds", True)` 而 partition 键在
    # 未传 `--over` 时不存在 —— 于是 gate 在最该拦的情形（没给多报数据）反而放行。缺数据应当拒绝，
    # 与本目录其他工具同一条纪律：零输入不得读成一次干净的检查。
    if "partition" not in result:
        print("\n⚠️ 未传 --over，划分闭合性**未被检查**。gate 拒绝放行。", file=sys.stderr)
        return 2
    return 0 if result["partition"]["holds"] else 1


if __name__ == "__main__":
    sys.exit(main())
