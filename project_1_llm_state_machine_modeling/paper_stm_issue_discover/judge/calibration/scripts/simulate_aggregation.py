"""Offline simulation of mechanism-level aggregation over two runs that share the validity prompt (stdlib only).

Pools the per-report validity samples of two calibration runs (reading 1, reading 2 and, when it
happened, the arbitration reading of each run) and reports, against the frozen gold:
  - agreement of each run as-is;
  - majority vote over 3 / 4 / 6 pooled samples on defect_class and on valid-vs-invalid;
  - the oracle ceiling (any pooled sample equals gold);
  - confidence gating: agreement on reports whose samples are unanimous versus split.
Relation for a simulated valid outcome is taken from whichever run judged that report valid; when
neither did, the outcome is counted as N. This is an upper-bound estimate, not a new judge run.

Usage: python simulate_aggregation.py --gold subset_v1/gold_v1.tsv --run-a <runs dir A> --run-b <runs dir B>
"""

from __future__ import annotations

import argparse
import collections
import csv
import glob
import json
from pathlib import Path

VALID = {"D2", "D1"}
KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}


def samples(run_dir: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for f in glob.glob(str(run_dir / "*" / "pairs" / "*.json")):
        d = json.loads(Path(f).read_text(encoding="utf-8"))
        anon = {r["anonymous_id"]: r["original_id"] for r in d["adapter_audit"]["report_id_map"]}
        c1 = {c["report_id"]: c["defect_adjudication"]["defect_class"] for c in d["validity_reading_1"]["certificates"]}
        c2 = {c["report_id"]: c["defect_adjudication"]["defect_class"] for c in d["validity_reading_2"]["certificates"]}
        arb = {c["report_id"]: c["defect_adjudication"]["defect_class"] for c in d.get("validity_arbitration_certificates", [])}
        fin = {o["original_report_id"]: o for o in d["report_outcomes"]}
        for a, rid in anon.items():
            o = fin[rid]
            out[rid] = {"r1": c1[a], "r2": c2[a], "arb": arb.get(a), "final": o["defect_class"], "kni": KNI[o["validity"]], "pos": bool(o["full_ledger_ids"] or o["partial_ledger_ids"])}
    return out


def majority(values):
    c = collections.Counter(v for v in values if v)
    if not c:
        return None
    top, n = c.most_common(1)[0]
    return None if list(c.values()).count(n) > 1 else top


def vi(x):
    return None if x is None else ("V" if x in VALID else "I")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--run-a", type=Path, required=True)
    parser.add_argument("--run-b", type=Path, required=True)
    args = parser.parse_args()
    with args.gold.open(encoding="utf-8") as handle:
        gold = {r["report_id"]: r for r in csv.DictReader(handle, delimiter="\t")}
    A, B = samples(args.run_a), samples(args.run_b)
    rows = {rid: g for rid, g in gold.items() if rid in A and rid in B}

    def kni_of(defect, a, b):
        if defect not in VALID:
            return "I"
        for r in (a, b):
            if r["kni"] != "I":
                return "K" if r["pos"] else "N"
        return "N"

    def evaluate(label, choose):
        cells = []
        for side in ("current", "baseline"):
            n = ok = 0
            for rid, g in rows.items():
                if g["side"] != side:
                    continue
                d = choose(A[rid], B[rid])
                if d is None:
                    continue
                n += 1
                ok += kni_of(d, A[rid], B[rid]) == g["gold_class"]
            cells.append(f"{ok}/{n} = {100.0 * ok / n:.1f}%" if n else "n/a")
        print(f"| {label} | {cells[0]} | {cells[1]} |")

    print("| aggregation | current | baseline |")
    print("| :-- | :-- | :-- |")
    evaluate("run A final", lambda a, b: a["final"])
    evaluate("run B final", lambda a, b: b["final"])
    evaluate("run A majority(r1, r2, arbitration) else final", lambda a, b: majority([a["r1"], a["r2"], a["arb"]]) or a["final"])
    evaluate("run B majority(r1, r2, arbitration) else final", lambda a, b: majority([b["r1"], b["r2"], b["arb"]]) or b["final"])
    evaluate("pooled majority of 4 primaries else A final", lambda a, b: majority([a["r1"], a["r2"], b["r1"], b["r2"]]) or a["final"])
    evaluate("pooled majority of up to 6 samples else A final", lambda a, b: majority([a["r1"], a["r2"], a["arb"], b["r1"], b["r2"], b["arb"]]) or a["final"])
    evaluate("pooled majority of up to 6 on valid/invalid only", lambda a, b: {"V": "D2", "I": "D0", None: a["final"]}[majority([vi(x) for x in (a["r1"], a["r2"], a["arb"], b["r1"], b["r2"], b["arb"])])])

    def oracle(a, b, g):
        for x in (a["r1"], a["r2"], a["arb"], b["r1"], b["r2"], b["arb"]):
            if x and kni_of(x, a, b) == g["gold_class"]:
                return True
        return False

    print()
    for side in ("current", "baseline"):
        ids = [rid for rid, g in rows.items() if g["side"] == side]
        hit = sum(oracle(A[r], B[r], gold[r]) for r in ids)
        print(f"- oracle ceiling ({side}): any of up to 6 pooled samples equals gold: {hit}/{len(ids)} = {100.0 * hit / len(ids):.1f}%")
    print()
    print("| confidence gate | side | confident | uncertain | routed to human |")
    print("| :-- | :-- | :-- | :-- | :-- |")
    gates = [
        ("run B readings agree on valid/invalid", lambda a, b: vi(b["r1"]) == vi(b["r2"]), B),
        ("run B readings agree on defect_class", lambda a, b: b["r1"] == b["r2"], B),
        ("4 primaries unanimous on valid/invalid", lambda a, b: len({vi(a["r1"]), vi(a["r2"]), vi(b["r1"]), vi(b["r2"])}) == 1, B),
        ("both runs' finals give the same K/N/I", lambda a, b: a["kni"] == b["kni"], B),
    ]
    for label, cond, ref in gates:
        for side in ("current", "baseline"):
            ids = [rid for rid, g in rows.items() if g["side"] == side]
            conf = [r for r in ids if cond(A[r], B[r])]
            unc = [r for r in ids if not cond(A[r], B[r])]
            acc = lambda xs: (sum(ref[r]["kni"] == gold[r]["gold_class"] for r in xs), len(xs))
            c, u = acc(conf), acc(unc)
            print(f"| {label} | {side} | {c[0]}/{c[1]} = {100.0 * c[0] / max(c[1], 1):.1f}% | {u[0]}/{u[1]} = {100.0 * u[0] / max(u[1], 1):.1f}% | {100.0 * u[1] / len(ids):.0f}% |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
