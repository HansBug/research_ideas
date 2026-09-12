#!/usr/bin/env python3
"""汇总重判结果、做主 session 裁定、算翻转率与外推。"""
from __future__ import annotations

import json
import glob
import random
from collections import defaultdict
from pathlib import Path

OUT = Path("/tmp/x1reju")

#: ⭐ 主 session 的裁定覆盖。每条都写明理由，理由都指向**收紧**方向。
OVERRIDES: dict[str, tuple[bool, str]] = {
    # 载体是 excluded_findings 里的断言，且未被任何已发布 issue 引用。
    # 主臂自己的 A 层定义（verdict_tiers.py docstring）：「只看已发布 issue 引用的断言。
    # 被排除的发现不算命中 —— 它没有进入产物。」X1 侧同理（analysis 不承载命中）。
    "EIS-0002-02|run2/0002-claude": (False, "载体 AST-REQ-009-1/010-1 在 excluded_findings 内且无已发布 issue 引用；主臂 A 层与 X1 规则都不许它承载命中"),
    "EIS-0005-01|run1/0005-gpt": (False, "载体 AST-REQ-002-1 在 excluded_findings 内且无已发布 issue 引用"),
    "EIS-0005-01|run2/0005-claude": (False, "载体 AST-REQ-002-1 在 excluded_findings 内且无已发布 issue 引用"),
    "EIS-0035-03|run1/0035-gpt": (False, "载体 AST-REQ-019-2 在 excluded_findings 内且无已发布 issue 引用"),
    # 重复计入：该 issue 逐字对应 EIS-0033-01（「三子态被声明成 PumpControl 的兄弟」），
    # 而 EIS-0033-01 在同一格已判命中（6/6）。同一条发现不得再认领 -02。
    "EIS-0033-02|run2/0033-gpt": (False, "所援引 issue 逐字对应 EIS-0033-01，且该记录在同格已计命中（6/6）；再认领 -02 属一果两记"),
}


def wilson(k: int, n: int, z: float = 1.959963985) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main() -> None:
    sample = json.loads((OUT / "sample.json").read_text())
    meta = {p["key"]: p for p in sample["sample_miss"] + sample["sample_hit"]}

    ext = json.loads((OUT / "sample_ext.json").read_text())
    for p in ext["sample_hit_stage2"]:
        p["stage"] = 2
        meta[p["key"]] = p
    for k in list(meta):
        meta[k].setdefault("stage", 1)

    raw: dict[str, dict] = {}
    for f in sorted(glob.glob(str(OUT / "verdicts" / "R*.json")) + glob.glob(str(OUT / "verdicts" / "S*.json"))):
        d = json.loads(Path(f).read_text())
        for k, v in d["positions"].items():
            v["judged_by"] = d.get("judged_by")
            raw[k] = v
    assert len(raw) == 105, len(raw)

    recheck: dict[str, dict] = {}
    for f in ("V1_recheck.json", "V2_recheck.json"):
        p = OUT / "verdicts" / f
        if p.is_file():
            payload = json.loads(p.read_text())
            body = payload.get("positions", payload)
            for k, v in body.items():
                if isinstance(v, dict):
                    recheck[k] = v

    rows = []
    for key, m in meta.items():
        v = raw[key]
        group_hit = v["hit"] is True
        final_hit = group_hit
        note = ""
        if key in OVERRIDES:
            final_hit, note = OVERRIDES[key]
        rc = recheck.get(key) or {}
        rows.append(
            {
                **m,
                "group": v["judged_by"],
                "group_hit": group_hit,
                "carrier": v.get("carrier"),
                "equivalence_form": v.get("equivalence_form"),
                "argument": v.get("argument"),
                "recheck_upheld": rc.get("upheld"),
                "recheck_strength": rc.get("strength"),
                "adjudication": note,
                "final_hit": final_hit,
            }
        )
    (OUT / "positions_final.json").write_text(
        json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    miss = [r for r in rows if not r["original_hit"]]
    hit = [r for r in rows if r["original_hit"]]
    hit_s1 = [r for r in hit if r["stage"] == 1]
    assert len(miss) == 60 and len(hit) == 45 and len(hit_s1) == 20

    flips = [r for r in miss if r["final_hit"]]
    revs = [r for r in hit if not r["final_hit"]]
    raw_flips = [r for r in miss if r["group_hit"]]
    raw_revs = [r for r in hit if not r["group_hit"]]

    N_MISS_ALL, N_HIT_ALL, N_ALL = 233, 355, 588

    def block(title, k1, n1, k2, n2):
        p1, p2 = k1 / n1, k2 / n2
        lo1, hi1 = wilson(k1, n1)
        lo2, hi2 = wilson(k2, n2)
        gained = N_MISS_ALL * p1
        lost = N_HIT_ALL * p2
        new_hits = 355 + gained - lost
        # Monte Carlo over Beta(Jeffreys) posteriors
        rng = random.Random(20260812)
        draws = []
        for _ in range(200000):
            q1 = rng.betavariate(k1 + 0.5, n1 - k1 + 0.5)
            q2 = rng.betavariate(k2 + 0.5, n2 - k2 + 0.5)
            draws.append((N_MISS_ALL * q1 - N_HIT_ALL * q2) / N_ALL * 100)
        draws.sort()
        d_lo, d_hi = draws[int(0.025 * len(draws))], draws[int(0.975 * len(draws))]
        d_pt = (gained - lost) / N_ALL * 100
        print(f"\n### {title}")
        print(f"  miss->hit  : {k1}/{n1} = {p1*100:.1f}%   95%CI(Wilson) [{lo1*100:.1f}%, {hi1*100:.1f}%]")
        print(f"  hit->miss  : {k2}/{n2} = {p2*100:.1f}%   95%CI(Wilson) [{lo2*100:.1f}%, {hi2*100:.1f}%]")
        print(f"  外推：233 miss 位翻正 {gained:.1f}，355 hit 位翻负 {lost:.1f}")
        print(f"  主臂 hit@1: 355/588 = 60.4%  ->  {new_hits:.1f}/588 = {new_hits/588*100:.1f}%")
        print(f"  Δ(X1-主臂): 14.9pp  ->  {75.3 - new_hits/588*100:.1f}pp")
        print(f"  判定仪器可解释的 pp（正数=缩小差距）: {d_pt:+.2f}pp   95%CI [{d_lo:+.2f}, {d_hi:+.2f}]")
        return dict(k1=k1, n1=n1, k2=k2, n2=n2, p1=p1, p2=p2, ci1=(lo1, hi1), ci2=(lo2, hi2),
                    new_hits=new_hits, d_pt=d_pt, d_ci=(d_lo, d_hi))

    print("=" * 100)
    print("X1 判定条件下重判主臂 —— 结果")
    print("=" * 100)
    revs1 = [r for r in hit_s1 if not r["final_hit"]]
    r_pre = block("预登记口径（miss 60 / 反向对照 20）", len(flips), 60, len(revs1), 20)
    r_primary = block("主结果（反向对照补样至 45，方差收缩；载体限已发布 issue）", len(flips), 60, len(revs), 45)
    r_raw = block("敏感性 A：判定组原始输出（含 excluded_findings 承载 + 一果两记）", len(raw_flips), 60, len(raw_revs), 45)
    r_onedir = block("敏感性 B：只做单向重判（不含反向对照）—— 演示单向会高估多少", len(flips), 60, 0, 45)

    print("\n### 逐条：miss -> hit 翻转位")
    for r in flips:
        print(f"  {r['key']}  pred={r['primary_predicate']}  group={r['group']}  form={r['equivalence_form']}  strength={r['recheck_strength']}")
    print("\n### 逐条：hit -> miss 反向翻转位")
    for r in revs:
        print(f"  {r['key']}  pred={r['primary_predicate']}  group={r['group']}  stage={r['stage']}")
    print("\n### 被主 session 收紧掉的位（判定组判命中、裁定为未命中）")
    for r in rows:
        if r["group_hit"] and not r["final_hit"]:
            print(f"  {r['key']}  ({'miss样本' if not r['original_hit'] else 'hit样本'})  {r['adjudication']}")

    print("\n### 分层：miss 样本按 primary 谓词")
    by = defaultdict(lambda: [0, 0])
    for r in miss:
        by[r["primary_predicate"]][1] += 1
        if r["final_hit"]:
            by[r["primary_predicate"]][0] += 1
    for k in sorted(by, key=lambda x: (-by[x][1], x)):
        f, n = by[k]
        print(f"  {k:24s} {f}/{n}")

    print("\n### 分层：miss 样本按 model / run")
    for dim in ("model", "run"):
        by2 = defaultdict(lambda: [0, 0])
        for r in miss:
            by2[r[dim]][1] += 1
            if r["final_hit"]:
                by2[r[dim]][0] += 1
        print(f"  {dim}: " + ", ".join(f"{k}={by2[k][0]}/{by2[k][1]}" for k in sorted(by2, key=str)))

    print("\n### 分层：miss 样本按 pair（只列有翻转的）")
    by3 = defaultdict(lambda: [0, 0])
    for r in miss:
        by3[r["pair"]][1] += 1
        if r["final_hit"]:
            by3[r["pair"]][0] += 1
    for k in sorted(by3):
        if by3[k][0]:
            print(f"  pair {k}: {by3[k][0]}/{by3[k][1]}")

    (OUT / "stats.json").write_text(
        json.dumps({"preregistered": r_pre, "primary": r_primary, "raw": r_raw, "one_directional": r_onedir},
                   ensure_ascii=False, indent=2, default=str) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
