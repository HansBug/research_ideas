"""Cross-iteration trend table over judge/calibration/results/*/{current,baseline}/all_rows.tsv (stdlib only).

Prints, per iteration and side, the preregistered criteria P1-P6 plus per-stratum K/N/I agreement,
and the agreement restricted to the rows every listed iteration judged (so partial coverage does not
inflate one iteration against another).
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
RESULTS = HERE.parents[1] / "results"


def load(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as handle:
        return {r["report_id"]: r for r in csv.DictReader(handle, delimiter="\t")}


def pct(n: int, d: int) -> str:
    return f"{n}/{d} = {100.0 * n / d:.1f}%" if d else "n/a"


def criteria(rows: list[dict]) -> dict[str, str]:
    agree = sum(r["class_agree"] == "True" for r in rows)
    n_to_i = [r for r in rows if r["stratum"].startswith("N->I")]
    i_to_valid = [r for r in rows if r["stratum"] in ("I->K", "I->N")]
    k_to_k = [r for r in rows if r["stratum"].startswith("K->K")]
    gold_valid = sum(r["gold_class"] in ("K", "N") for r in rows)
    new_valid = sum(r["new_class"] in ("K", "N") for r in rows)
    return {
        "P1 K/N/I": pct(agree, len(rows)),
        "P2 N->I judged I": pct(sum(r["new_class"] == "I" for r in n_to_i), len(n_to_i)),
        "P3 I->valid judged valid": pct(sum(r["new_class"] in ("K", "N") for r in i_to_valid), len(i_to_valid)),
        "P4 K->K kept K": pct(sum(r["new_class"] == "K" for r in k_to_k), len(k_to_k)),
        "P5 defect exact": pct(sum(r["defect_agree"] == "True" for r in rows), len(rows)),
        "P6 valid-rate bias": f"{100.0 * (new_valid - gold_valid) / len(rows):+.1f} pp" if rows else "n/a",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=RESULTS)
    args = parser.parse_args()
    iterations = sorted(p for p in args.results.iterdir() if p.is_dir() and p.name.startswith("iter"))
    for side in ("current", "baseline"):
        tables = {it.name: load(it / side / "all_rows.tsv") for it in iterations if (it / side / "all_rows.tsv").is_file()}
        if not tables:
            continue
        common = set.intersection(*(set(t) for t in tables.values()))
        print(f"\n## {side}: {len(common)} rows judged by every iteration\n")
        keys = list(criteria([]).keys())
        print("| criterion | " + " | ".join(tables) + " |")
        print("| :-- | " + " | ".join(":--" for _ in tables) + " |")
        per_iter = {name: criteria([t[r] for r in sorted(common)]) for name, t in tables.items()}
        for key in keys:
            print(f"| {key} | " + " | ".join(per_iter[name][key] for name in tables) + " |")
        strata = sorted({t[r]["stratum"] for t in tables.values() for r in common})
        print("\n| stratum | n | " + " | ".join(tables) + " |")
        print("| :-- | --: | " + " | ".join(":--" for _ in tables) + " |")
        for stratum in strata:
            cells = []
            n = 0
            for name, t in tables.items():
                rows = [t[r] for r in common if t[r]["stratum"] == stratum]
                n = len(rows)
                cells.append(pct(sum(r["class_agree"] == "True" for r in rows), n))
            print(f"| `{stratum}` | {n} | " + " | ".join(cells) + " |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
