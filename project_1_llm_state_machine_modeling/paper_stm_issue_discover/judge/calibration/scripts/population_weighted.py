"""Population-weighted agreement estimate for one calibration comparison.

The calibration subset over-samples the strata that changed between the frozen
judge and the human gold, so raw subset agreement is not the agreement the judge
would have on the full frozen population. This script weights each stratum's
subset agreement by that stratum's population count in the frozen
``final_results`` and reports both the estimate and the frozen judge's own
population agreement for reference. Strata absent from the sampling plan are
listed, not estimated.

usage: population_weighted.py --side current --all-rows <compare-out>/all_rows.tsv
"""
from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_calibration_subset as bcs  # noqa: E402


def stratum_name(key: tuple[str, str, str]) -> str:
    jc, gc, gd = key
    return f"{jc}->{gc}" + ("" if gd == "*" else f"/{gd}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--side", choices=("current", "baseline"), required=True)
    parser.add_argument("--all-rows", type=Path, required=True)
    args = parser.parse_args()
    judge_side = "v60_current" if args.side == "current" else "x1v2_baseline"
    judge = bcs.load_judge(judge_side)
    gold = bcs.load_gold_current() if args.side == "current" else bcs.load_gold_baseline()
    population = {rid: {**judge[rid], **gold[rid]} for rid in judge}
    pop_count: Counter[str] = Counter()
    unsampled: Counter[str] = Counter()
    frozen_agree = 0
    for row in population.values():
        key = bcs.stratum_key(row, args.side)
        frozen_agree += row["judge_class"] == row["gold_class"]
        if key is None:
            unsampled[f"{row['judge_class']}->{row['gold_class']}/{row['gold_defect']}"] += 1
        else:
            pop_count[stratum_name(key)] += 1
    subset = list(csv.DictReader(open(args.all_rows, encoding="utf-8"), delimiter="\t"))
    sub_n: Counter[str] = Counter()
    sub_agree: Counter[str] = Counter()
    new_class_by_stratum: dict[str, Counter[str]] = defaultdict(Counter)
    for row in subset:
        sub_n[row["stratum"]] += 1
        sub_agree[row["stratum"]] += row["new_class"] == row["gold_class"]
        new_class_by_stratum[row["stratum"]][row["new_class"]] += 1
    covered = sum(pop_count[s] for s in pop_count if sub_n[s])
    weighted = sum(pop_count[s] * sub_agree[s] / sub_n[s] for s in pop_count if sub_n[s])
    total = len(population)
    print(f"# population-weighted agreement: {args.side}")
    print()
    print(f"- population reports: {total}; covered by sampled strata: {covered}; unsampled: {total - covered}")
    print(f"- frozen judge agreement on population: {frozen_agree}/{total} = {100 * frozen_agree / total:.1f}%")
    print(f"- new judge population-weighted estimate: {weighted:.1f}/{covered} = {100 * weighted / covered:.1f}% (over covered strata)")
    # population K/N/I under the new judge, projected from subset stratum rates
    projected: Counter[str] = Counter()
    for s, n in pop_count.items():
        if sub_n[s]:
            for cls, k in new_class_by_stratum[s].items():
                projected[cls] += n * k / sub_n[s]
    gold_pop = Counter(r["gold_class"] for r in population.values())
    frozen_pop = Counter(r["judge_class"] for r in population.values())
    print(f"- population K/N/I: gold {dict(gold_pop)}; frozen judge {dict(frozen_pop)}; new judge projected " + str({k: round(v, 1) for k, v in sorted(projected.items())}))
    print()
    print("| stratum | population n | subset n | subset agree | weight × agree |")
    print("| :-- | --: | --: | --: | --: |")
    for s in sorted(pop_count, key=lambda x: -pop_count[x]):
        if sub_n[s]:
            print(f"| `{s}` | {pop_count[s]} | {sub_n[s]} | {sub_agree[s]}/{sub_n[s]} = {100 * sub_agree[s] / sub_n[s]:.1f}% | {pop_count[s] * sub_agree[s] / sub_n[s]:.1f} |")
        else:
            print(f"| `{s}` | {pop_count[s]} | 0 | – | – |")
    if unsampled:
        print()
        print("unsampled strata (not in the sampling plan): " + ", ".join(f"`{k}`={v}" for k, v in sorted(unsampled.items())))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
