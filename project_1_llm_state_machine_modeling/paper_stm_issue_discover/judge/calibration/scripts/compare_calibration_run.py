"""Compare one calibration judge run against the frozen human gold labels (stdlib only).

Usage:
  python compare_calibration_run.py --side current --gold subset_v1/gold_v1.tsv \
      --run-dir <run>/r1 --run-dir <run>/r2 --run-dir <run>/r3 --out results/<tag>/current

Reads ``pairs/*.json`` report outcomes and the final validity certificates of each
run directory, joins them with ``gold_v1.tsv`` and writes:
  summary.md          class / defect-class matrices, per-stratum agreement, bias, coverage
  all_rows.tsv        one row per judged subset report
  disagreements.tsv   rows whose K/N/I class differs from gold, with judge reason/basis
  disagreements.md    the same rows in a reviewable form
"""

from __future__ import annotations

import argparse
import csv
import glob
import json
from collections import Counter, defaultdict
from pathlib import Path

KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}
CLASSES = ("K", "N", "I")
DEFECTS = ("D2", "D1", "D0", "A0_FALSE_POSITIVE", "A0_NOT_A_DEFECT_CLAIM")


def load_gold(path: Path, side: str) -> dict[str, dict]:
    with path.open(encoding="utf-8") as handle:
        return {row["report_id"]: row for row in csv.DictReader(handle, delimiter="\t") if row["side"] == side}


def load_run(run_dir: Path) -> tuple[dict[str, dict], list[str]]:
    judged: dict[str, dict] = {}
    for path in sorted(glob.glob(str(run_dir / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        anon_to_orig = {row["anonymous_id"]: row["original_id"] for row in data["adapter_audit"]["report_id_map"]}
        certificates = {c["report_id"]: c for c in data["validity_reading_1"]["certificates"]}
        for c in data.get("validity_arbitration_certificates", []):
            certificates[c["report_id"]] = c
        conflicts = Counter(item["kind"] for item in data.get("conflicts", []))
        for outcome in data["report_outcomes"]:
            rid = outcome["original_report_id"]
            anon = next(a for a, o in anon_to_orig.items() if o == rid)
            cert = certificates[anon]
            adj = cert["defect_adjudication"]
            judged[rid] = {
                "new_class": KNI[outcome["validity"]],
                "new_defect": outcome.get("defect_class") or "",
                "new_relation": "FULL_MATCH" if outcome.get("full_ledger_ids") else "PARTIAL_MATCH" if outcome.get("partial_ledger_ids") else "NO_MATCH",
                "new_ledger_ids": ";".join(list(outcome.get("full_ledger_ids") or []) + list(outcome.get("partial_ledger_ids") or [])),
                "adjudication_reason": adj["reason"],
                "adjudication_basis": adj["basis"],
                "core_gate": cert["core_claim_gate"]["status"],
                "mechanism_gate": cert["indispensable_mechanism_gate"]["status"],
                "arbitrated": anon in {c["report_id"] for c in data.get("validity_arbitration_certificates", [])},
                "pair_conflicts": dict(conflicts),
                "run_dir": str(run_dir),
            }
    failures = [Path(p).stem for p in glob.glob(str(run_dir / "failures" / "*.json"))]
    return judged, failures


def matrix(rows: list[dict], a: str, b: str, labels: tuple[str, ...]) -> list[str]:
    counts = Counter((r[a], r[b]) for r in rows)
    head = "| " + a + " \\ " + b + " | " + " | ".join(labels) + " | total |"
    lines = [head, "| :-- | " + " | ".join("--:" for _ in labels) + " | --: |"]
    for x in labels:
        lines.append(f"| **{x}** | " + " | ".join(str(counts.get((x, y), 0)) for y in labels) + f" | {sum(counts.get((x, y), 0) for y in labels)} |")
    lines.append("| total | " + " | ".join(str(sum(counts.get((x, y), 0) for x in labels)) for y in labels) + f" | {len(rows)} |")
    return lines


def pct(n: int, d: int) -> str:
    return f"{n}/{d} = {100.0 * n / d:.1f}%" if d else "n/a"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--side", choices=("current", "baseline"), required=True)
    parser.add_argument("--gold", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--label", default="")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    gold = load_gold(args.gold, args.side)
    judged: dict[str, dict] = {}
    failures: list[str] = []
    for run_dir in args.run_dir:
        j, f = load_run(run_dir)
        judged.update(j)
        failures += [f"{run_dir}:{x}" for x in f]
    rows = []
    for rid, g in sorted(gold.items()):
        if rid not in judged:
            continue
        n = judged[rid]
        rows.append({**g, **n, "class_agree": n["new_class"] == g["gold_class"], "defect_agree": n["new_defect"] == g["gold_defect"], "old_agree": g["judge_class"] == g["gold_class"]})
    missing = sorted(set(gold) - set(judged))
    extra = sorted(set(judged) - set(gold))

    lines = [f"# Calibration comparison: {args.side} {args.label}".rstrip(), ""]
    lines += [f"- run dirs: {', '.join(str(r) for r in args.run_dir)}", f"- subset gold rows: {len(gold)}; judged and matched: {len(rows)}; missing: {len(missing)}; judged outside subset: {len(extra)}; failed pairs: {len(failures)}", ""]
    if missing:
        lines += ["missing: " + ", ".join(missing), ""]
    if failures:
        lines += ["failures: " + ", ".join(failures), ""]
    agree = sum(r["class_agree"] for r in rows)
    old_agree = sum(r["old_agree"] for r in rows)
    dagree = sum(r["defect_agree"] for r in rows)
    lines += ["## Headline", "", f"- K/N/I agreement with gold: **{pct(agree, len(rows))}** (frozen v3.2 judge on the same rows: {pct(old_agree, len(rows))})", f"- defect-class exact agreement: {pct(dagree, len(rows))}"]
    d2d1 = sum(1 for r in rows if not r["defect_agree"] and {r["new_defect"], r["gold_defect"]} == {"D2", "D1"})
    lines += [f"- defect-class disagreements that are only D2<->D1: {d2d1}"]
    gold_valid = sum(r["gold_class"] in ("K", "N") for r in rows)
    new_valid = sum(r["new_class"] in ("K", "N") for r in rows)
    old_valid = sum(r["judge_class"] in ("K", "N") for r in rows)
    lines += [f"- valid rate: gold {pct(gold_valid, len(rows))}; new judge {pct(new_valid, len(rows))}; frozen judge {pct(old_valid, len(rows))}", f"- arbitrated reports: {sum(r['arbitrated'] for r in rows)}", ""]
    lines += ["## K/N/I matrix (rows = new judge, columns = gold)", ""] + matrix(rows, "new_class", "gold_class", CLASSES) + [""]
    lines += ["## Defect-class matrix (rows = new judge, columns = gold)", ""] + matrix(rows, "new_defect", "gold_defect", DEFECTS) + [""]
    lines += ["## Per stratum (stratum = frozen judge class -> gold class)", "", "| stratum | n | class agree | defect agree | new class distribution |", "| :-- | --: | --: | --: | :-- |"]
    by_stratum: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_stratum[r["stratum"]].append(r)
    for stratum, items in sorted(by_stratum.items()):
        dist = Counter(r["new_class"] for r in items)
        lines.append(f"| `{stratum}` | {len(items)} | {pct(sum(r['class_agree'] for r in items), len(items))} | {pct(sum(r['defect_agree'] for r in items), len(items))} | " + ", ".join(f"{k}={v}" for k, v in sorted(dist.items())) + " |")
    lines += ["", "## Disagreements by pair", ""]
    dis = [r for r in rows if not r["class_agree"]]
    lines += [", ".join(f"{k}={v}" for k, v in sorted(Counter(r["pair"] for r in dis).items())) or "none", ""]
    (args.out / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    cols = ["side", "report_id", "pair", "round", "stratum", "judge_class", "gold_class", "gold_defect", "gold_relation", "gold_ledger_ids", "new_class", "new_defect", "new_relation", "new_ledger_ids", "core_gate", "mechanism_gate", "arbitrated", "class_agree", "defect_agree", "adjudication_reason", "adjudication_basis", "gold_reason"]
    def tsv(path: Path, items: list[dict]) -> None:
        with path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=cols, delimiter="\t", extrasaction="ignore")
            writer.writeheader()
            for r in items:
                writer.writerow({k: (str(r.get(k, "")).replace("\t", " ").replace("\n", " ")) for k in cols})
    tsv(args.out / "all_rows.tsv", rows)
    tsv(args.out / "disagreements.tsv", dis)
    md = [f"# Disagreements: {args.side} {args.label}".rstrip(), "", f"{len(dis)} of {len(rows)} rows differ from gold on K/N/I.", ""]
    for r in dis:
        md += [f"## `{r['report_id']}` stratum `{r['stratum']}` : frozen {r['judge_class']} / gold {r['gold_class']} ({r['gold_defect']}, {r['gold_relation']}) / new **{r['new_class']}** ({r['new_defect']}, {r['new_relation']}; gates core={r['core_gate']} mech={r['mechanism_gate']}; arbitrated={r['arbitrated']})", "", f"- new adjudication reason: {r['adjudication_reason']}", f"- new adjudication basis: {r['adjudication_basis']}", f"- gold reason: {r['gold_reason']}", ""]
    (args.out / "disagreements.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
