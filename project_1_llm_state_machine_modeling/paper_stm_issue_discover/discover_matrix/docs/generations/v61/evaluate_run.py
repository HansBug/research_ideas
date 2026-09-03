"""Score a v61 diagnostic / full run against the preregistered thresholds.

usage:
  python evaluate_run.py --method-root <run root with method/<pair>/round-N.json>
                         --judge-root <judge output dir with current-r*/pairs/*.json>
                         [--v60-judge-root runs/paper1/judge-full-3a1ba5cf1-iter6cfg]
                         [--round 1]

Blocks (preregistered.md §2): anchor / benefit. Metrics per block: reports per cell,
judge K/N/I and precision, FULL ledger ids, targeted C1/C2 ids hit, L2 ids hit. When a
v60 judge root is given the same numbers are printed for the same pairs and round so
the comparison is judge-to-judge. Human gold is not used (it does not exist for new
outputs); the v60 human numbers live in preregistered.md §3.
"""
from __future__ import annotations

import argparse
import glob
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
P1 = HERE.parents[4]
LEDGER = P1 / "discover_matrix" / "ledger_v2" / "ledger.json"
ANCHOR = ("0002", "0007", "0035", "0011", "0000")
BENEFIT = ("0009", "0029", "0049", "0039", "0010", "0030", "0014", "0044", "0056", "0016")
TARGETED = {
    "EIS-0009-03", "EIS-0029-05", "EIS-0049-02", "EIS-0005-02", "EIS-0009-02", "EIS-0016-02", "EIS-0014-03",
    "VU-0014-01", "EIS-0034-05", "EIS-0030-03", "EIS-0050-01", "EIS-0000-02", "EIS-0020-02", "VU-0054-01",
    "INS-0039-03", "INS-0044-03", "DIFF-0039-04", "INS-0056-01", "EIS-0010-02",
    "EIS-0010-05", "EIS-0030-02", "EIS-0040-01", "VU-0010-01", "VU-0046-01", "EIS-0019-03",
}
KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}


def load_judge(root: Path, rnd: int) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(str(root / f"current-r{rnd}*" / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        if int(data["round"]) != rnd:
            continue
        for o in data.get("report_outcomes") or []:
            out[o["original_report_id"]] = {
                "class": KNI[o["validity"]],
                "full": list(o.get("full_ledger_ids") or []),
                "partial": list(o.get("partial_ledger_ids") or []),
                "defect": o.get("d_tier") or o.get("a0_subtype") or "",
            }
    return out


def load_method(root: Path, rnd: int) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted(glob.glob(str(root / "method" / "*" / f"round-{rnd}.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for c in data.get("report_issue_clusters") or []:
            out[c["issue_id"]] = {
                "pair": data["pair_id"], "property": c.get("property"), "direction": c.get("violation_direction"),
                "predicate_id": c.get("predicate_id") or "-", "title": c.get("title") or "",
                "coverage_class": c.get("coverage_class"), "sub_claims": len(c.get("folded_sub_claims") or []),
            }
    return out


def block(name: str, pairs: tuple[str, ...], method: dict, judge: dict, items: dict) -> None:
    ids = [e for e in items if items[e]["pair"] in pairs]
    l2 = {e for e in ids if items[e]["L"] == "L2"}
    reps = [r for r in method if method[r]["pair"] in pairs]
    judged = [r for r in reps if r in judge]
    cls = Counter(judge[r]["class"] for r in judged)
    full = {e for r in judged for e in judge[r]["full"] if e in items}
    n = len(reps) or 1
    print(f"\n== {name}: {len(pairs)} pairs, {len(ids)} ledger ids (L2 {len(l2)}) ==")
    print(f"  reports {len(reps)} ({len(reps)/len(pairs):.1f}/cell), judged {len(judged)}, folded sub-claims {sum(method[r]['sub_claims'] for r in reps)}")
    print(f"  judge K/N/I {cls['K']}/{cls['N']}/{cls['I']}  precision {100*(cls['K']+cls['N'])/max(1,len(judged)):.1f}%")
    print(f"  FULL ledger ids {len(full)}/{len(ids)} = {100*len(full)/max(1,len(ids)):.1f}%   L2 {len(full & l2)}/{len(l2)}")
    tgt = sorted(e for e in ids if e in TARGETED)
    print(f"  targeted C1/C2 ids hit {len(full & set(tgt))}/{len(tgt)}: hit={sorted(full & set(tgt))} missed={sorted(set(tgt)-full)}")
    missed = sorted(set(ids) - full)
    print(f"  missed ids: {missed}")
    tab = Counter((method[r]["predicate_id"], method[r]["property"], method[r]["direction"], judge[r]["class"]) for r in judged)
    by = defaultdict(Counter)
    for (pid, prop, d, c), v in tab.items():
        by[(pid, prop, d)][c] += v
    print("  per predicate/property: n K/N/I")
    for k, c in sorted(by.items(), key=lambda kv: -sum(kv[1].values()))[:14]:
        print(f"    {k[0]:>3s} {k[1]}:{k[2]:<16s} {sum(c.values()):3d}  {c['K']}/{c['N']}/{c['I']}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--method-root", type=Path, required=True)
    ap.add_argument("--judge-root", type=Path, required=True)
    ap.add_argument("--v60-judge-root", type=Path)
    ap.add_argument("--v60-method-root", type=Path, default=P1 / "final_results" / "v60_current_vs_x1v2_baseline" / "raw" / "v60_current" / "method")
    ap.add_argument("--round", type=int, default=1)
    ap.add_argument("--pairs", nargs="*", help="override pair list (default: anchor + benefit)")
    a = ap.parse_args()
    items = json.loads(LEDGER.read_text(encoding="utf-8"))["items"]
    method = load_method(a.method_root, a.round)
    judge = load_judge(a.judge_root, a.round)
    print(f"method reports round {a.round}: {len(method)}; judged: {len(judge)}")
    blocks = [("ANCHOR", ANCHOR), ("BENEFIT", BENEFIT), ("SUBSET", ANCHOR + BENEFIT)] if not a.pairs else [("PAIRS", tuple(a.pairs))]
    for name, pairs in blocks:
        block(name, pairs, method, judge, items)
    if a.v60_judge_root:
        print("\n\n######## v60 same pairs, same round, judge-to-judge reference ########")
        m60 = load_method(a.v60_method_root, a.round)
        j60 = load_judge(a.v60_judge_root, a.round)
        for name, pairs in blocks:
            block(name + " (v60)", pairs, m60, j60, items)


if __name__ == "__main__":
    main()
