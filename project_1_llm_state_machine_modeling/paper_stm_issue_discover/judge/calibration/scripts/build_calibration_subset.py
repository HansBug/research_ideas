"""Build the ~300-report judge calibration subset from frozen archives (stdlib only, read-only).

Strata are defined by how the frozen v3.2 Judge class (K/N/I) moved under the
final human adjudication (current: v4; baseline: v3 combined). Most of the
subset comes from reports whose class changed; a smaller part is stable so that
the run also shows the judge does not disturb settled cases.

Outputs go to ``judge/calibration/subset_v1/``:
  report_filter_current.json / report_filter_baseline.json  -> ``--report-filter`` inputs
  gold_v1.tsv                                              -> per-report gold labels and stratum
  summary.md                                               -> counts by stratum / pair / round
"""

from __future__ import annotations

import argparse
import glob
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve()
PAPER_ROOT = HERE.parents[3]
FR = PAPER_ROOT / "final_results" / "v60_current_vs_x1v2_baseline"
OUT = HERE.parents[1] / "subset_v1"
SEED = 20260903

# stratum -> target count; stratum key is (judge_class, gold_class[, gold_defect])
PLAN = {
    "current": {
        ("N", "I", "D0"): 60,
        ("N", "I", "A0_NOT_A_DEFECT_CLAIM"): 50,
        ("N", "I", "A0_FALSE_POSITIVE"): 1,
        ("N", "K", "*"): 15,
        ("I", "K", "*"): 8,
        ("I", "N", "*"): 12,
        ("K", "I", "*"): 1,
        ("K", "K", "D2"): 22,
        ("K", "K", "D1"): 8,
        ("N", "N", "*"): 12,
        ("I", "I", "*"): 12,
    },
    "baseline": {
        ("N", "I", "*"): 25,
        ("N", "K", "*"): 4,
        ("I", "K", "*"): 20,
        ("I", "N", "*"): 21,
        ("K", "K", "*"): 15,
        ("N", "N", "*"): 8,
        ("I", "I", "*"): 7,
    },
}
KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}


def _gold_defect(d_tier: str | None, a0: str | None) -> str:
    if d_tier in ("D2", "D1", "D0"):
        return d_tier
    if a0:
        return f"A0_{a0}"
    return "A0"


def load_judge(side: str) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for path in sorted(glob.glob(str(FR / "raw" / side / "judge" / "source_runs" / "*" / "pairs" / "*.json"))):
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        for outcome in data["report_outcomes"]:
            rid = outcome["original_report_id"]
            if rid in rows:
                raise SystemExit(f"duplicate judge id {rid}")
            rows[rid] = {
                "judge_class": KNI[outcome["validity"]],
                "judge_reason": outcome["reason"],
            }
    return rows


def load_gold_current() -> dict[str, dict]:
    data = json.loads((FR / "derived" / "manual_adjudication_v4_current_reaudit" / "current_report_decisions_v4.json").read_text(encoding="utf-8"))
    rows = {}
    for d in data["decisions"]:
        rid = d["original_report_id"]
        relation = "FULL_MATCH" if d.get("full_ledger_ids") else "PARTIAL_MATCH" if d.get("partial_ledger_ids") else "NO_MATCH"
        rows[rid] = {
            "gold_class": d["canonical_class"],
            "gold_defect": _gold_defect(d.get("d_tier"), d.get("a0_subtype")),
            "gold_relation": relation,
            "gold_ledger_ids": ";".join(list(d.get("full_ledger_ids") or []) + list(d.get("partial_ledger_ids") or [])),
            "gold_w": d.get("w_level") or "",
            "gold_reason": (d.get("reason") or "")[:400],
        }
    return rows


def load_gold_baseline() -> dict[str, dict]:
    root = FR / "derived" / "manual_adjudication_v3_baseline_ni"
    rows = {}
    for d in json.loads((root / "baseline_report_decisions_v3.json").read_text(encoding="utf-8"))["decisions"]:
        rid = d["original_report_id"]
        relation = "FULL_MATCH" if d.get("full_ledger_ids") else "PARTIAL_MATCH" if d.get("partial_ledger_ids") else "NO_MATCH"
        witness = d.get("witness") or {}
        rows[rid] = {
            "gold_class": d["corrected_kni"],
            "gold_defect": _gold_defect(d.get("d_tier"), d.get("a0_type")),
            "gold_relation": relation,
            "gold_ledger_ids": ";".join(list(d.get("full_ledger_ids") or []) + list(d.get("partial_ledger_ids") or [])),
            "gold_w": witness.get("level") or "",
            "gold_reason": (d.get("reason") or "")[:400],
            "gold_layer": "v3_reaudited_non_k",
        }
    for r in json.loads((root / "frozen_k_snapshot_v3.json").read_text(encoding="utf-8"))["rows"]:
        rid = r["report_id"]
        witness = r.get("witness") or {}
        relations = r.get("relations") or []
        full = [x["expected_id"] for x in relations if x.get("relation") == "FULL_MATCH"]
        partial = [x["expected_id"] for x in relations if x.get("relation") == "PARTIAL_MATCH"]
        if not full and not partial and r.get("ledger_ids"):
            full = list(r["ledger_ids"])
        rows[rid] = {
            "gold_class": r["corrected_kni"],
            "gold_defect": _gold_defect(r.get("strict_da"), r.get("a0_type")),
            "gold_relation": "FULL_MATCH" if full else "PARTIAL_MATCH" if partial else "NO_MATCH",
            "gold_ledger_ids": ";".join(full + partial),
            "gold_w": witness.get("level") or "",
            "gold_reason": (r.get("reason") or "")[:400],
            "gold_layer": "v2_frozen_k",
        }
    return rows


def stratum_key(row: dict, side: str) -> tuple[str, str, str] | None:
    for key in PLAN[side]:
        jc, gc, gd = key
        if row["judge_class"] != jc or row["gold_class"] != gc:
            continue
        if gd == "*" or row["gold_defect"] == gd:
            return key
    return None


def pick(rows: dict[str, dict], side: str, rng: random.Random) -> list[tuple[str, dict, str]]:
    by_stratum: dict[tuple, list[str]] = defaultdict(list)
    for rid, row in rows.items():
        key = stratum_key(row, side)
        if key is not None:
            by_stratum[key].append(rid)
    chosen: list[tuple[str, dict, str]] = []
    for key, target in PLAN[side].items():
        pool = sorted(by_stratum.get(key, []))
        rng.shuffle(pool)
        # round-robin over pairs so a single pair cannot dominate a stratum
        per_pair: dict[str, list[str]] = defaultdict(list)
        for rid in pool:
            per_pair[rid[:4]].append(rid)
        order = sorted(per_pair)
        rng.shuffle(order)
        taken: list[str] = []
        while len(taken) < min(target, len(pool)):
            progressed = False
            for pair in order:
                if per_pair[pair] and len(taken) < target:
                    taken.append(per_pair[pair].pop())
                    progressed = True
            if not progressed:
                break
        label = f"{key[0]}->{key[1]}" + (f"/{key[2]}" if key[2] != "*" else "")
        chosen.extend((rid, rows[rid], label) for rid in sorted(taken))
    return chosen


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(SEED)
    summary_lines = ["# Calibration subset v1", "", f"seed = {SEED}; built from frozen `final_results/v60_current_vs_x1v2_baseline` (read-only).", ""]
    tsv_rows = ["side\treport_id\tpair\tround\tstratum\tjudge_class\tgold_class\tgold_defect\tgold_relation\tgold_ledger_ids\tgold_w\tgold_layer\tgold_reason"]
    for side, judge_side, loader in (("current", "v60_current", load_gold_current), ("baseline", "x1v2_baseline", load_gold_baseline)):
        judge = load_judge(judge_side)
        gold = loader()
        if set(judge) != set(gold):
            raise SystemExit(f"{side}: judge/gold id sets differ: {len(set(judge) ^ set(gold))}")
        rows = {rid: {**judge[rid], **gold[rid]} for rid in judge}
        chosen = pick(rows, side, rng)
        filt: dict[str, list[str]] = defaultdict(list)
        for rid, _row, _label in chosen:
            filt[rid[:4]].append(rid)
        (args.out / f"report_filter_{side}.json").write_text(json.dumps({k: sorted(v) for k, v in sorted(filt.items())}, indent=2) + "\n", encoding="utf-8")
        by_label = Counter(label for _rid, _row, label in chosen)
        by_pair = Counter(rid[:4] for rid, _row, _label in chosen)
        by_round = Counter(rid.split(":")[1] for rid, _row, _label in chosen)
        summary_lines += [f"## {side}: {len(chosen)} reports, {len(filt)} pairs", "", "| stratum | n |", "| :-- | --: |"]
        summary_lines += [f"| `{label}` | {n} |" for label, n in sorted(by_label.items())]
        summary_lines += ["", "rounds: " + ", ".join(f"{k}={v}" for k, v in sorted(by_round.items())), "", "pairs: " + ", ".join(f"{k}={v}" for k, v in sorted(by_pair.items())), ""]
        for rid, row, label in chosen:
            pair, rnd = rid.split(":")[0], rid.split(":")[1]
            tsv_rows.append("\t".join([
                side, rid, pair, rnd, label, row["judge_class"], row["gold_class"], row["gold_defect"], row["gold_relation"],
                row["gold_ledger_ids"], row["gold_w"], row.get("gold_layer", "v4_current_reaudit"),
                row["gold_reason"].replace("\t", " ").replace("\n", " "),
            ]))
    (args.out / "gold_v1.tsv").write_text("\n".join(tsv_rows) + "\n", encoding="utf-8")
    (args.out / "summary.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    print("\n".join(summary_lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
