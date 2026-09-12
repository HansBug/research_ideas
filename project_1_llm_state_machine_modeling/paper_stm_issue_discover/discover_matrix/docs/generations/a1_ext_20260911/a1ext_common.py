"""Shared, provider-free arithmetic for the A1-ext archive. Reuses the frozen A1 analyzer verbatim.

Metric definitions are imported from analyze_a1.py (FULL hit units, hit@1/@3/@all, K/N/I precision,
strict = valid and external D1/D2, nine-NL-cluster paired bootstrap with seed 20260906 and 10000 replicates).
This module only adds per-round splits, ledger-axis content splits, a strict-precision interval computed with
the same cluster scheme, and the expected-round rows used by the archive verifier.
"""
from collections import defaultdict
from pathlib import Path
import random
import sys

PAPER = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PAPER / "discover_matrix/docs/generations/a1_no_inspect_20260906"))
from analyze_a1 import calculate, compare, digest, read, ratio  # noqa: E402

MODELS = ("sonnet", "muse", "qwen")
NAMES = {"sonnet": "Claude Sonnet 5", "muse": "Muse Glimmer-30B", "qwen": "Qwen3.8-27B", "luna": "gpt-5.6-luna"}
PROFILES = {"sonnet": "claude-sonnet-5", "muse": "e1-muse30b", "qwen": "e1-qwen38-27b"}
ARMS = ("a1ext", "full")
AXES = ("defect_element", "defect_logic_kind")


def ledger_items():
    items = read(PAPER / "discover_matrix/ledger_v2/ledger.json")["items"]
    return items if isinstance(items, dict) else {i["id"]: i for i in items}


def expected_rows(reports, items):
    """One row per (ledger item, round): FULL / PARTIAL support and hit flags, mirroring the A1 archive."""
    rows = []
    for eid, item in sorted(items.items()):
        for rnd in (1, 2, 3):
            sel = [r for r in reports if r["pair_id"] == item["pair"] and r["round"] == rnd and r["validity"] == "VALID_KNOWN"]
            full = sorted(r["original_report_id"] for r in sel if eid in r["full_ledger_ids"])
            partial = sorted(r["original_report_id"] for r in sel if eid in r["partial_ledger_ids"])
            rows.append({"ledger_id": eid, "round": rnd, "pair_id": item["pair"], "L": item["L"],
                         "full_report_ids": full, "partial_report_ids": partial,
                         "hit": bool(full), "supported": bool(full or partial)})
    return rows


def per_round(reports, items):
    return {str(rnd): calculate([r for r in reports if r["round"] == rnd], items) for rnd in (1, 2, 3)}


def content_breakdown(reports, items):
    """FULL hit units grouped by ledger axis values; denominators are 3 rounds x items carrying the value."""
    full = {(e, r["round"]) for r in reports if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    out = {}
    for axis in AXES:
        groups = defaultdict(set)
        for eid, item in items.items():
            groups[str(item["axes"].get(axis))].add(eid)
        out[axis] = {value: ratio(sum(1 for e, _ in full if e in ids), 3 * len(ids)) for value, ids in sorted(groups.items())}
    return out


def strict_view(reports):
    strict = [r for r in reports if r["validity"] != "INVALID" and r["d_tier"] in ("D1", "D2")]
    units = {(e, r["round"]) for r in strict if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    return len(strict), len(reports), units


def strict_cluster_bootstrap(a1ext, full, items, seed=20260906, replicates=10000):
    """Same nine-cluster paired resampling as analyze_a1.compare, applied to strict precision and strict hit@1."""
    clusters = sorted({i["pair_context"]["nl_sha8"] for i in items.values()})
    assert len(clusters) == 9
    rows = []
    for cluster in clusters:
        subitems = {e for e, i in items.items() if i["pair_context"]["nl_sha8"] == cluster}
        row = {}
        for label, arm in (("a1ext", a1ext), ("full", full)):
            reps = [r for r in arm["reports"] if r["nl_cluster"] == cluster]
            n_strict, n_reports, units = strict_view(reps)
            row[label] = {"strict_n": n_strict, "reports": n_reports,
                          "strict_hits": sum(1 for e, _ in units if e in subitems), "expected": 3 * len(subitems)}
        rows.append(row)

    def difference(indices):
        out = {}
        for key, num, den in (("strict_precision", "strict_n", "reports"), ("strict_hit1", "strict_hits", "expected")):
            rates = {}
            for label in ("a1ext", "full"):
                n = sum(rows[i][label][num] for i in indices)
                d = sum(rows[i][label][den] for i in indices)
                rates[label] = n / d if d else None
            out[key] = 100 * (rates["a1ext"] - rates["full"]) if None not in rates.values() else None
        return out

    rng = random.Random(seed)
    samples = [difference(rng.choices(range(9), k=9)) for _ in range(replicates)]
    intervals = {}
    for key in ("strict_precision", "strict_hit1"):
        values = sorted(s[key] for s in samples if s[key] is not None)
        intervals[key] = {"percentile_2_5": values[int(.025 * (len(values) - 1))],
                          "percentile_97_5": values[int(.975 * (len(values) - 1))], "defined_replicates": len(values)}
    return {"delta_pp": difference(range(9)), "cluster_bootstrap_95pct": intervals,
            "bootstrap_seed": seed, "bootstrap_replicates": replicates,
            "basis": "Nine NL clusters resampled with replacement, both arms scored on the same resampled clusters; extension of analyze_a1.compare to the strict scoring range."}


def arm_summary(arm, items):
    """Compact numbers for tables; everything recomputed from stored reports."""
    m = calculate(arm["reports"], items)
    n_strict, n_reports, strict_units = strict_view(arm["reports"])
    return {"reports": m["reports"], "K": m["K"], "N": m["N"], "I": m["I"], "precision": m["precision"],
            "strict_precision": ratio(n_strict, n_reports), "hit1": m["hit1"], "strict_hit1": ratio(len(strict_units), 3 * len(items)),
            "hit3": m["hit3"], "hitall": m["hitall"], "tiers": {L: m["tiers"][L]["hit1"] for L in ("L0", "L1", "L2")},
            "tiers_hit3": {L: m["tiers"][L]["hit3"] for L in ("L0", "L1", "L2")}, "tiers_hitall": {L: m["tiers"][L]["hitall"] for L in ("L0", "L1", "L2")}}


def pct(r):
    return "n/a" if r["rate"] is None else f"{r['numerator']}/{r['denominator']}（{100 * r['rate']:.2f}%）"


def pp(a, b):
    return f"{100 * (a['rate'] - b['rate']):+.2f}"
