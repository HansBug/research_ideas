"""Compare a judge run against the human decisions over the whole report population.

Unlike compare_calibration_run.py (subset rows + strata), this script scores every
report the run judged against the human decisions in ``final_results`` and computes
the paper's headline shape directly: K / N / I counts, report precision, and
expected-level hit@1 / hit@3 / hit@all from FULL matches. The human side is computed
the same way from the human relations, so the human hit@1 must reproduce the frozen
report (current 310/435, baseline 227/435) as a self-check. Partial runs are scored on
the pair-rounds present; coverage is printed.

usage: compare_full_run.py --run-dir runs/paper1/judge-full-<hash>-iter6cfg --out <dir>
"""
from __future__ import annotations

import argparse
import csv
import glob
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_calibration_subset as bcs  # noqa: E402

KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}
ROUNDS = (1, 2, 3)


def report_round(report_id: str) -> tuple[str, int]:
    m = re.match(r"^(\d{4}):r(\d):", report_id)
    if not m:
        raise ValueError(report_id)
    return m.group(1), int(m.group(2))


def load_judge_run(root: Path, side: str) -> tuple[dict[str, dict], dict[tuple[str, int], dict[str, bool]], set[str]]:
    reports: dict[str, dict] = {}
    expected_hits: dict[tuple[str, int], dict[str, bool]] = {}
    ledger_ids: set[str] = set()
    for path in sorted(glob.glob(str(root / f"{side}-r*" / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        pair, rnd = data["pair_id"], int(data["round"])
        hits = {}
        for e in data.get("expected_outcomes") or []:
            hits[e["ledger_id"]] = bool(e.get("hit"))
            ledger_ids.add(e["ledger_id"])
        expected_hits[(pair, rnd)] = hits
        for o in data.get("report_outcomes") or []:
            rid = o["original_report_id"]
            full = list(o.get("full_ledger_ids") or []); partial = list(o.get("partial_ledger_ids") or [])
            reports[rid] = {
                "class": KNI[o["validity"]], "defect": bcs._gold_defect(o.get("d_tier"), o.get("a0_subtype")) if (o.get("d_tier") or o.get("a0_subtype")) else (o.get("defect_class") or ""),
                "relation": "FULL_MATCH" if full else "PARTIAL_MATCH" if partial else "NO_MATCH",
                "full": full, "partial": partial, "reason": (o.get("reason") or "")[:600],
            }
    return reports, expected_hits, ledger_ids


def load_gold_full(side: str) -> dict[str, dict]:
    """Human decisions with FULL ledger ids kept separate (needed for hits)."""
    FR = bcs.FR
    gold: dict[str, dict] = {}
    if side == "current":
        data = json.loads((FR / "derived" / "manual_adjudication_v4_current_reaudit" / "current_report_decisions_v4.json").read_text(encoding="utf-8"))
        for d in data["decisions"]:
            gold[d["original_report_id"]] = {"class": d["canonical_class"], "defect": bcs._gold_defect(d.get("d_tier"), d.get("a0_subtype")), "full": list(d.get("full_ledger_ids") or []), "partial": list(d.get("partial_ledger_ids") or []), "reason": (d.get("reason") or "")[:600]}
    else:
        root = FR / "derived" / "manual_adjudication_v3_baseline_ni"
        for d in json.loads((root / "baseline_report_decisions_v3.json").read_text(encoding="utf-8"))["decisions"]:
            gold[d["original_report_id"]] = {"class": d["corrected_kni"], "defect": bcs._gold_defect(d.get("d_tier"), d.get("a0_type")), "full": list(d.get("full_ledger_ids") or []), "partial": list(d.get("partial_ledger_ids") or []), "reason": (d.get("reason") or "")[:600]}
        for r in json.loads((root / "frozen_k_snapshot_v3.json").read_text(encoding="utf-8"))["rows"]:
            rid = r.get("original_report_id") or r["report_id"]
            rels = r.get("relations") or []
            full = [x["expected_id"] for x in rels if x.get("relation") == "FULL_MATCH"]
            partial = [x["expected_id"] for x in rels if x.get("relation") == "PARTIAL_MATCH"]
            gold[rid] = {"class": r["corrected_kni"], "defect": bcs._gold_defect(r.get("strict_da"), r.get("a0_type")), "full": full, "partial": partial, "reason": (r.get("reason") or "")[:600]}
    for g in gold.values():
        g["relation"] = "FULL_MATCH" if g["full"] else "PARTIAL_MATCH" if g["partial"] else "NO_MATCH"
    return gold


def hits_from_reports(reports: dict[str, dict], pair_rounds: set[tuple[str, int]]) -> dict[tuple[str, int], set[str]]:
    out: dict[tuple[str, int], set[str]] = defaultdict(set)
    for rid, r in reports.items():
        pair, rnd = report_round(rid)
        if (pair, rnd) in pair_rounds:
            out[(pair, rnd)].update(r["full"])
    return out


def hit_metrics(hit_sets: dict[tuple[str, int], set[str]], ledger_ids: set[str], pair_rounds: set[tuple[str, int]]) -> dict[str, float]:
    by_id_rounds: dict[str, set[int]] = defaultdict(set)
    units = 0
    for (pair, rnd), ids in hit_sets.items():
        for lid in ids:
            if lid in ledger_ids:
                by_id_rounds[lid].add(rnd); units += 1
    covered_rounds = {lid: {rnd for (p, rnd) in pair_rounds if p == lid.split("-")[1]} for lid in ledger_ids}
    unit_denominator = sum(len(v) for v in covered_rounds.values())
    hit3 = sum(1 for lid in ledger_ids if by_id_rounds.get(lid))
    hitall = sum(1 for lid in ledger_ids if covered_rounds[lid] and covered_rounds[lid] <= by_id_rounds.get(lid, set()))
    return {"hit1_units": units, "unit_denominator": unit_denominator, "hit3": hit3, "hitall": hitall, "ids": len(ledger_ids)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    lines = [f"# Full-population comparison: `{args.run_dir.name}`", ""]
    for side in ("current", "baseline"):
        reports, expected_hits, ledger_ids = load_judge_run(args.run_dir, side)
        if not reports:
            lines.append(f"## {side}: no judged pairs yet"); continue
        gold = load_gold_full(side)
        pair_rounds = set(expected_hits)
        gold_in_scope = {rid: g for rid, g in gold.items() if report_round(rid) in pair_rounds}
        judged = {rid: r for rid, r in reports.items() if rid in gold}
        missing = [rid for rid in gold_in_scope if rid not in reports]
        conf = Counter((r["class"], gold[rid]["class"]) for rid, r in judged.items())
        agree = sum(1 for rid, r in judged.items() if r["class"] == gold[rid]["class"])
        jk = Counter(r["class"] for r in judged.values()); gk = Counter(gold[rid]["class"] for rid in judged)
        # hits: judge from its expected_outcomes; human from human FULL ids on the same pair-rounds
        judge_hits = {pr: {lid for lid, h in hits.items() if h} for pr, hits in expected_hits.items()}
        human_hits = hits_from_reports(gold_in_scope, pair_rounds)
        # ledger universe restricted to pairs judged
        jm = hit_metrics(judge_hits, ledger_ids, pair_rounds); hm = hit_metrics(human_hits, ledger_ids, pair_rounds)
        n = len(judged)
        lines += [f"## {side}", "",
                  f"- pair-rounds judged: {len(pair_rounds)}; reports judged and matched to human decisions: {n}; human reports in scope not judged: {len(missing)}; ledger ids in scope: {len(ledger_ids)}",
                  f"- K/N/I agreement: **{agree}/{n} = {100*agree/max(n,1):.1f}%**",
                  f"- K/N/I counts: judge K {jk['K']} / N {jk['N']} / I {jk['I']}; human K {gk['K']} / N {gk['N']} / I {gk['I']}",
                  f"- report precision (K+N)/all: judge {100*(jk['K']+jk['N'])/max(n,1):.1f}%; human {100*(gk['K']+gk['N'])/max(n,1):.1f}%",
                  f"- hit@1 FULL units: judge {jm['hit1_units']}/{jm['unit_denominator']} = {100*jm['hit1_units']/max(jm['unit_denominator'],1):.1f}%; human {hm['hit1_units']}/{hm['unit_denominator']} = {100*hm['hit1_units']/max(hm['unit_denominator'],1):.1f}%",
                  f"- hit@3 (any round): judge {jm['hit3']}/{jm['ids']}; human {hm['hit3']}/{hm['ids']}",
                  f"- hit@all (every judged round): judge {jm['hitall']}/{jm['ids']}; human {hm['hitall']}/{hm['ids']}",
                  "", "| judge \\ human | K | N | I |", "| :-- | --: | --: | --: |"]
        for jc in "KNI":
            lines.append(f"| **{jc}** | " + " | ".join(str(conf[(jc, hc)]) for hc in "KNI") + " |")
        # disagreement groups
        groups = Counter((gold[rid]["class"], r["class"], r["defect"]) for rid, r in judged.items() if r["class"] != gold[rid]["class"])
        lines += ["", "disagreements by (human → judge, judge defect): " + ", ".join(f"{h}→{j}/{d}={c}" for (h, j, d), c in groups.most_common(12)), ""]
        with (args.out / f"{side}_disagreements.tsv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t")
            w.writerow(["report_id", "pair", "round", "human_class", "human_defect", "human_relation", "human_full", "judge_class", "judge_defect", "judge_relation", "judge_full", "judge_partial", "judge_reason", "human_reason"])
            for rid in sorted(judged):
                r = judged[rid]; g = gold[rid]
                if r["class"] != g["class"]:
                    pair, rnd = report_round(rid)
                    w.writerow([rid, pair, rnd, g["class"], g["defect"], g["relation"], ";".join(g["full"]), r["class"], r["defect"], r["relation"], ";".join(r["full"]), ";".join(r["partial"]), r["reason"], g["reason"]])
        with (args.out / f"{side}_all_reports.tsv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t")
            w.writerow(["report_id", "human_class", "human_defect", "human_relation", "judge_class", "judge_defect", "judge_relation"])
            for rid in sorted(judged):
                r = judged[rid]; g = gold[rid]
                w.writerow([rid, g["class"], g["defect"], g["relation"], r["class"], r["defect"], r["relation"]])
    (args.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
