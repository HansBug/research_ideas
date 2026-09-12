"""Judge-scored full-run metrics (54 pairs x 3 rounds) for a v61 run, with v60 and baseline references.

usage: evaluate_full.py --method-root <run root> --judge-root <judge dir with current-r*/pairs>
                        [--v60-judge-root runs/paper1/judge-full-3a1ba5cf1-iter6cfg]

Metrics per side: reports, per-cell mean, judge K/N/I, report precision, finding-level precision
(one report per FULL unit), hit@1 units / 435, hit@3 ids / 145, hit@all ids / 145, per L tier.
Baseline numbers come from the same iteration-6 judge run (baseline-r*) so all three columns are
judge-to-judge.  Human gold (v60 frozen) is printed for orientation only.
"""
from __future__ import annotations

import argparse
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
P1 = HERE.parents[4]
LEDGER = P1 / "discover_matrix" / "ledger_v2" / "ledger.json"
KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}
ROUNDS = ("r1", "r2", "r3")


def load_judge(root: Path, side: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(str(root / f"{side}-r*" / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        rnd = f"r{data['round']}"
        for o in data.get("report_outcomes") or []:
            out[o["original_report_id"]] = {"pair": data["pair_id"], "round": rnd, "class": KNI[o["validity"]], "full": list(o.get("full_ledger_ids") or []), "partial": list(o.get("partial_ledger_ids") or [])}
    return out


def metrics(reports: dict[str, dict], items: dict, cells: int, label: str) -> dict:
    cls = Counter(r["class"] for r in reports.values())
    n = len(reports)
    units: dict[tuple[str, str], list[str]] = defaultdict(list)
    ids_rounds: dict[str, set[str]] = defaultdict(set)
    for rid, r in reports.items():
        for e in r["full"]:
            if e in items:
                units[(e, r["round"])].append(rid)
                ids_rounds[e].add(r["round"])
    hit1 = len(units)
    hit3 = len(ids_rounds)
    hitall = sum(1 for v in ids_rounds.values() if v >= set(ROUNDS))
    dup = sum(len(v) - 1 for v in units.values())
    finding_n = n - dup
    finding_k = cls["K"] - dup
    per_l = {}
    for tier in ("L0", "L1", "L2"):
        ids = [e for e in items if items[e]["L"] == tier]
        per_l[tier] = (sum(len(ids_rounds[e]) for e in ids), 3 * len(ids), sum(1 for e in ids if ids_rounds[e]), sum(1 for e in ids if ids_rounds[e] >= set(ROUNDS)))
    return {"label": label, "reports": n, "per_cell": n / max(1, cells), "K": cls["K"], "N": cls["N"], "I": cls["I"],
            "precision": 100 * (cls["K"] + cls["N"]) / max(1, n), "finding_precision": 100 * (finding_k + cls["N"]) / max(1, finding_n), "finding_reports": finding_n,
            "hit1": hit1, "hit3": hit3, "hitall": hitall, "per_l": per_l, "rounds": Counter(r["round"] for r in reports.values())}


def show(m: dict, max_units: int, n_ids: int) -> None:
    print(f"\n== {m['label']} ==")
    print(f"  reports {m['reports']} ({m['per_cell']:.1f}/cell; rounds {dict(sorted(m['rounds'].items()))})  K/N/I {m['K']}/{m['N']}/{m['I']}  precision {m['precision']:.1f}%  finding-level {m['finding_precision']:.1f}% over {m['finding_reports']} findings")
    print(f"  hit@1 {m['hit1']}/{max_units} = {100*m['hit1']/max_units:.1f}%   hit@3 {m['hit3']}/{n_ids}   hit@all {m['hitall']}/{n_ids}")
    for tier, (u, mx, h3, ha) in m["per_l"].items():
        print(f"  {tier}: hit@1 {u}/{mx} ({100*u/max(1,mx):.0f}%)  hit@3 {h3}  hit@all {ha}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--method-root", type=Path)
    ap.add_argument("--judge-root", type=Path, required=True)
    ap.add_argument("--v60-judge-root", type=Path, default=Path("runs/paper1/judge-full-3a1ba5cf1-iter6cfg"))
    ap.add_argument("--pairs", nargs="*")
    a = ap.parse_args()
    items = json.loads(LEDGER.read_text(encoding="utf-8"))["items"]
    if a.pairs:
        items = {k: v for k, v in items.items() if v["pair"] in a.pairs}
    n_ids = len(items); max_units = 3 * n_ids
    def restrict(reps):
        return {k: v for k, v in reps.items() if not a.pairs or v["pair"] in a.pairs}
    cells = 3 * (len(a.pairs) if a.pairs else 54)
    cur = restrict(load_judge(a.judge_root, "current"))
    show(metrics(cur, items, cells, f"v61 current (judge) {a.judge_root}"), max_units, n_ids)
    if a.v60_judge_root and a.v60_judge_root.is_dir():
        show(metrics(restrict(load_judge(a.v60_judge_root, "current")), items, cells, "v60 current (judge, iteration-6 config)"), max_units, n_ids)
        show(metrics(restrict(load_judge(a.v60_judge_root, "baseline")), items, cells, "baseline (judge, iteration-6 config)"), max_units, n_ids)
    print("\nhuman reference (frozen, full population): ours 1271 reports 749/231/291 precision 77.1% hit@1 310/435 hit@3 119 hit@all 86; baseline 512 reports 312/105/95 precision 81.4% hit@1 227/435 hit@3 106 hit@all 46")


if __name__ == "__main__":
    main()
