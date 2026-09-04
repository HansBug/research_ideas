"""Rough paper-level metric estimate implied by a judge calibration run.

Reads the population-weighted projections (``population_weighted.md`` written by
population_weighted.py) for current and baseline and turns them into the paper's
headline shape: K / N / I counts, report precision = (K + N) / all, and a rough
hit@1. The hit@1 estimate scales the human hit@1 by the projected K count using the
human ratio of hit@1 units per K report (current 310/749, baseline 227/312); it is
an order-of-magnitude guide, not a measurement. hit@3 and hit@all cannot be derived
from report-level counts and need the full-population judge run.

usage: paper_metric_estimate.py --label iter8A --current <pw.md> --baseline <pw.md> [more triples]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

GOLD = {
    "current": {"K": 749, "N": 231, "I": 291, "hit1_units": 310, "units": 435},
    "baseline": {"K": 312, "N": 105, "I": 95, "hit1_units": 227, "units": 435},
}


def projected(path: Path) -> dict[str, float]:
    text = path.read_text(encoding="utf-8")
    m = re.search(r"new judge projected (\{[^}]*\})", text)
    if not m:
        raise SystemExit(f"no projection in {path}")
    return {k.strip("' "): float(v) for k, v in re.findall(r"'([KNI])': ([\d.]+)", m.group(1))}


def estimate(side: str, kni: dict[str, float]) -> dict[str, float]:
    g = GOLD[side]
    total = kni["K"] + kni["N"] + kni["I"]
    precision = (kni["K"] + kni["N"]) / total
    hit1 = g["hit1_units"] * (kni["K"] / g["K"])
    return {"K": kni["K"], "N": kni["N"], "I": kni["I"], "precision": precision, "hit1_units": hit1, "hit1": hit1 / g["units"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", nargs=3, action="append", metavar=("LABEL", "CURRENT_PW", "BASELINE_PW"), required=True)
    args = parser.parse_args()
    rows = []
    for side in ("current", "baseline"):
        g = GOLD[side]
        rows.append((f"gold / {side}", g["K"], g["N"], g["I"], (g["K"] + g["N"]) / (g["K"] + g["N"] + g["I"]), g["hit1_units"] / g["units"]))
    for label, cur, base in args.run:
        for side, path in (("current", cur), ("baseline", base)):
            e = estimate(side, projected(Path(path)))
            rows.append((f"{label} / {side}", e["K"], e["N"], e["I"], e["precision"], e["hit1"]))
    print("| run / side | K | N | I | report precision | hit@1 (rough) |")
    print("| :-- | --: | --: | --: | --: | --: |")
    for label, k, n, i, p, h in rows:
        print(f"| {label} | {k:.0f} | {n:.0f} | {i:.0f} | {100 * p:.1f}% | {100 * h:.1f}% |")
    print()
    print("| run | Δ hit@1 (ours − baseline) | Δ precision (ours − baseline) |")
    print("| :-- | --: | --: |")
    by = {r[0].split(" / ")[0]: {} for r in rows}
    for label, k, n, i, p, h in rows:
        by[label.split(" / ")[0]][label.split(" / ")[1]] = (p, h)
    for run, sides in by.items():
        if "current" in sides and "baseline" in sides:
            print(f"| {run} | {100 * (sides['current'][1] - sides['baseline'][1]):+.1f} pp | {100 * (sides['current'][0] - sides['baseline'][0]):+.1f} pp |")
    print()
    print("hit@1 is scaled from the human hit@1 by projected K / human K; hit@3 and hit@all need the full-population run.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
