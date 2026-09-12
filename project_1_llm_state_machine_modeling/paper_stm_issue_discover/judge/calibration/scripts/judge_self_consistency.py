"""Run-to-run self-consistency of the judge between two iterations (stdlib only).

Compares two ``all_rows.tsv`` files row by row: how often the judge gives the same
K/N/I class, the same valid/invalid decision, and the same defect class, plus how
often at least one of the two runs agrees with gold. When the two iterations share
the same validity prompt, the valid/invalid figure is the judge's own sampling noise
floor on this subset; gold agreement cannot be expected to exceed it by much.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load(path: Path) -> dict[str, dict]:
    with path.open(encoding="utf-8") as handle:
        return {r["report_id"]: r for r in csv.DictReader(handle, delimiter="\t")}


def pct(n: int, d: int) -> str:
    return f"{n}/{d} = {100.0 * n / d:.1f}%" if d else "n/a"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=Path, required=True, help="all_rows.tsv of iteration A")
    parser.add_argument("--b", type=Path, required=True, help="all_rows.tsv of iteration B")
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    a, b = load(args.a), load(args.b)
    common = sorted(i for i in a if i in b)
    same_class = sum(a[i]["new_class"] == b[i]["new_class"] for i in common)
    same_valid = sum((a[i]["new_class"] != "I") == (b[i]["new_class"] != "I") for i in common)
    same_defect = sum(a[i]["new_defect"] == b[i]["new_defect"] for i in common)
    both = sum(a[i]["class_agree"] == "True" and b[i]["class_agree"] == "True" for i in common)
    either = sum(a[i]["class_agree"] == "True" or b[i]["class_agree"] == "True" for i in common)
    a_only = sum(a[i]["class_agree"] == "True" for i in common)
    b_only = sum(b[i]["class_agree"] == "True" for i in common)
    print(f"# Judge self-consistency {args.label}".rstrip())
    print()
    print(f"- rows judged by both: {len(common)}")
    print(f"- same K/N/I class: {pct(same_class, len(common))}")
    print(f"- same valid/invalid decision: {pct(same_valid, len(common))}")
    print(f"- same defect class: {pct(same_defect, len(common))}")
    print(f"- gold agreement A: {pct(a_only, len(common))}; B: {pct(b_only, len(common))}")
    print(f"- both runs agree with gold: {pct(both, len(common))}; at least one run agrees: {pct(either, len(common))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
