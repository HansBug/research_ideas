#!/usr/bin/env python3
"""反向对照第二阶段抽样：从剩余 335 个主臂 hit 位再抽 25，使对照 n 从 20 升到 45。

⭐ 理由（在看到第二阶段任何判定之前写下）：主结果的方差被反向对照支配——它的权重是
355/588 = 0.604，而样本只有 20。⛔ 反向对照抽样不足恰恰是**偏向主臂**的方向（少抽反向
翻转 = 少扣分），所以补样是收紧而不是放宽。
⛔ 第一阶段的 60 + 20 不改动，主结果照旧按预登记口径报；本阶段只作为方差收缩的敏感性。
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20260812
N_ADD = 25
#: ⛔ 原先这里写死了一条绝对路径，⚠️ 它在 2026-08-17 的两次搬迁后都指向不存在的目录。
#: ⭐ 改为按目录名向上锚定 —— 再搬只会报错，不会静默读空（CLAUDE.md §9.5-3）。
PAPER = next(q for q in Path(__file__).resolve().parents
             if q.name == "paper_stm_issue_discover")
MATRIX = PAPER / "archive" / "r10_ledger_v1_and_v46"
#: 第一版台账（126 条）与 60 份逐 pair 复审。⚠️ 2026-08-17 随台账证据链从 `archive/…/manual_review/`
#: 搬到 `discover_matrix/ledger_v2/provenance/`。⛔ 它已**不是**当前台账 —— 当前台账是
#: `discover_matrix/ledger_v2/ledger.json` 的 145 条；本处只用它复现 588 网格的第一版口径分母。
PROVENANCE = PAPER / "discover_matrix" / "ledger_v2" / "provenance"
OUT_OF_SCOPE = ("0008", "0018", "0028", "0038", "0048", "0058")
BOUNDARY_RULED = ("EIS-0043-02",)


def primary_predicate(record: dict) -> str:
    for a in record.get("assertions") or []:
        if a.get("role") == "primary":
            preds = a.get("predicates") or []
            return preds[0] if preds else "UNKNOWN"
    return "NONE"


def main() -> None:
    ledger = {r["id"]: r for r in json.loads(
        (PROVENANCE / "expected_issue_set.json").read_text())["records"]}
    tiers = json.loads((MATRIX / "v46" / "verdicts" / "v46_tiers.json").read_text())["verdicts"]
    reportable = sorted(rid for rid, r in ledger.items()
                        if str(r["pair"])[-4:] not in OUT_OF_SCOPE and rid not in BOUNDARY_RULED)

    hits = []
    for rid in reportable:
        pair = str(ledger[rid]["pair"])[-4:]
        pred = primary_predicate(ledger[rid])
        for model in ("claude", "gpt"):
            for idx, value in enumerate(tiers[rid][model], 1):
                if value == 1:
                    hits.append({"key": f"{rid}|run{idx}/{pair}-{model}", "record_id": rid,
                                 "pair": pair, "model": model, "run": idx,
                                 "primary_predicate": pred, "original_hit": True})
    assert len(hits) == 355

    prev = json.loads(Path("/tmp/x1reju/sample.json").read_text())
    taken = {p["key"] for p in prev["sample_hit"]}
    pool = [h for h in hits if h["key"] not in taken]
    assert len(pool) == 335

    by_pred = defaultdict(list)
    for p in pool:
        by_pred[p["primary_predicate"]].append(p)
    total = len(pool)
    raw = {k: N_ADD * len(v) / total for k, v in by_pred.items()}
    alloc = {k: int(v) for k, v in raw.items()}
    rema = sorted(by_pred, key=lambda k: (-(raw[k] - alloc[k]), k))
    i = 0
    while sum(alloc.values()) < N_ADD:
        k = rema[i % len(rema)]
        if alloc[k] < len(by_pred[k]):
            alloc[k] += 1
        i += 1

    rng = random.Random(f"{SEED}:hit-stage2")
    picked = []
    for pred in sorted(by_pred):
        want = alloc[pred]
        if not want:
            continue
        buckets = defaultdict(list)
        for p in by_pred[pred]:
            buckets[(p["model"], p["run"])].append(p)
        for b in buckets.values():
            rng.shuffle(b)
        order = sorted(buckets)
        rng.shuffle(order)
        taken_n, cursor = 0, 0
        while taken_n < want:
            b = buckets[order[cursor % len(order)]]
            cursor += 1
            if b:
                picked.append(b.pop())
                taken_n += 1
    assert len(picked) == N_ADD
    picked.sort(key=lambda p: p["key"])

    Path("/tmp/x1reju/sample_ext.json").write_text(
        json.dumps({"seed": SEED, "stage": 2, "n": N_ADD, "sample_hit_stage2": picked},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    c = defaultdict(int)
    for p in picked:
        c[p["primary_predicate"]] += 1
    print("stage2 hit sample:", len(picked), "pairs:", len({p['pair'] for p in picked}))
    print(" pred:", dict(sorted(c.items())))
    print(" model:", {m: sum(1 for p in picked if p['model'] == m) for m in ('claude', 'gpt')})
    print(" run:", {r: sum(1 for p in picked if p['run'] == r) for r in (1, 2, 3)})


if __name__ == "__main__":
    main()
