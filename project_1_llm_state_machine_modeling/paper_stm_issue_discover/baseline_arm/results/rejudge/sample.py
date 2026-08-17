#!/usr/bin/env python3
"""机械可复现的分层抽样：从主臂 v46 的 233 个 miss 位抽 60，从 355 个 hit 位抽 20。

⛔ 本脚本必须在任何判定动作之前运行并落盘 /tmp/x1reju/sample.json。
随机种子写死；分层维度 = primary 谓词（含 NONE），层内按 (model, run) 六桶轮转以平衡
model / run，桶内按种子随机序取。
"""
from __future__ import annotations

import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20260812
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
N_MISS = 60
N_HIT = 20


def primary_predicate(record: dict) -> str:
    for a in record.get("assertions") or []:
        if a.get("role") == "primary":
            preds = a.get("predicates") or []
            return preds[0] if preds else "UNKNOWN"
    return "NONE"


def main() -> None:
    ledger = {
        r["id"]: r
        for r in json.loads((PROVENANCE / "expected_issue_set.json").read_text())["records"]
    }
    tiers = json.loads((MATRIX / "v46" / "verdicts" / "v46_tiers.json").read_text())["verdicts"]
    reportable = sorted(
        rid
        for rid, r in ledger.items()
        if str(r["pair"])[-4:] not in OUT_OF_SCOPE and rid not in BOUNDARY_RULED
    )
    assert len(reportable) == 98, len(reportable)

    positions = []
    for rid in reportable:
        pair = str(ledger[rid]["pair"])[-4:]
        pred = primary_predicate(ledger[rid])
        for model in ("claude", "gpt"):
            series = tiers[rid][model]
            assert len(series) == 3
            for idx, value in enumerate(series, 1):
                positions.append(
                    {
                        "key": f"{rid}|run{idx}/{pair}-{model}",
                        "record_id": rid,
                        "pair": pair,
                        "model": model,
                        "run": idx,
                        "primary_predicate": pred,
                        "original_hit": bool(value),
                    }
                )
    assert len(positions) == 588
    misses = [p for p in positions if not p["original_hit"]]
    hits = [p for p in positions if p["original_hit"]]
    assert len(misses) == 233 and len(hits) == 355

    def stratified(pool: list[dict], n: int, tag: str) -> list[dict]:
        by_pred: dict[str, list[dict]] = defaultdict(list)
        for p in pool:
            by_pred[p["primary_predicate"]].append(p)
        # 比例分配（最大余数法），保证每个非空层至少 1 个当 n 足够。
        total = len(pool)
        raw = {k: n * len(v) / total for k, v in by_pred.items()}
        alloc = {k: int(v) for k, v in raw.items()}
        # 先给四个「主臂最弱谓词」保底 1（若该层有位且分配为 0）。
        for k in ("reaches", "edge_declared", "event_consumed", "guard_distinguishable"):
            if k in by_pred and alloc.get(k, 0) == 0:
                alloc[k] = 1
        while sum(alloc.values()) > n:
            k = max(alloc, key=lambda x: (alloc[x] - raw[x], x))
            alloc[k] -= 1
        rema = sorted(by_pred, key=lambda k: (-(raw[k] - alloc[k]), k))
        i = 0
        while sum(alloc.values()) < n:
            k = rema[i % len(rema)]
            if alloc[k] < len(by_pred[k]):
                alloc[k] += 1
            i += 1
        assert sum(alloc.values()) == n

        rng = random.Random(f"{SEED}:{tag}")
        picked: list[dict] = []
        for pred in sorted(by_pred):
            want = alloc[pred]
            if not want:
                continue
            buckets: dict[tuple[str, int], list[dict]] = defaultdict(list)
            for p in by_pred[pred]:
                buckets[(p["model"], p["run"])].append(p)
            for b in buckets.values():
                rng.shuffle(b)
            order = sorted(buckets)
            rng.shuffle(order)
            taken, cursor = 0, 0
            while taken < want:
                bucket = buckets[order[cursor % len(order)]]
                cursor += 1
                if bucket:
                    picked.append(bucket.pop())
                    taken += 1
                if cursor > 10000:
                    raise RuntimeError("bucket exhausted")
        assert len(picked) == n
        return sorted(picked, key=lambda p: p["key"])

    sample_miss = stratified(misses, N_MISS, "miss")
    sample_hit = stratified(hits, N_HIT, "hit")
    keys = {p["key"] for p in sample_miss} | {p["key"] for p in sample_hit}
    assert len(keys) == N_MISS + N_HIT

    payload = {
        "seed": SEED,
        "generated_by": "/tmp/x1reju/sample.py",
        "universe": {"positions": 588, "miss": 233, "hit": 355},
        "sample_miss": sample_miss,
        "sample_hit": sample_hit,
    }
    Path("/tmp/x1reju/sample.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    def summarise(name: str, rows: list[dict]) -> None:
        print(f"\n=== {name} (n={len(rows)}) ===")
        for dim in ("primary_predicate", "model", "run"):
            counts: dict = defaultdict(int)
            for r in rows:
                counts[r[dim]] += 1
            print(f"  {dim}: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda x: str(x[0]))))
        print(f"  distinct pairs: {len({r['pair'] for r in rows})}")

    summarise("sample_miss", sample_miss)
    summarise("sample_hit", sample_hit)
    print(f"\ntotal distinct pairs in both samples: {len({r['pair'] for r in sample_miss + sample_hit})}")


if __name__ == "__main__":
    main()
