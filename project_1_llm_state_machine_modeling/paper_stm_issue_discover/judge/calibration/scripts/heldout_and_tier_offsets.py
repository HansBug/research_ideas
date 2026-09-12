"""第六轮配置 judge 对 v60 人工裁定的留出行一致率与按 L 分层的 hit@1 偏移。

校准子集（201 + 100 行）参与过配置选择，因此一致率另在排除该子集后的 1070 + 412 行上报告；
hit@1 偏移按 L0/L1/L2 分层给出。只读，标准库。用法：从仓库根 ``venv/bin/python <this file>``。
"""
from __future__ import annotations

import ast
import csv
import glob
import json
import os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
FULL = os.path.join(P1, "judge", "calibration", "results", "full_v3.11_3a1ba5cf1")
SUBSET = os.path.join(P1, "judge", "calibration", "subset_v1")
LEDGER = os.path.join(P1, "discover_matrix", "ledger_v2", "ledger.json")
HUMAN_INDEX = os.path.join(P1, "final_results", "v60_current_vs_x1v2_baseline", "derived", "fair_comparison_v4", "combined_report_index_v4.json")
JUDGE_CURRENT = "runs/paper1/judge-full-3a1ba5cf1-iter6cfg"  # v60 current judge cells (gitignored run dir)
JUDGE_BASELINE = os.path.join(P1, "final_results", "v61_source_divergence_vs_x1v2_baseline", "raw", "judge_v3.11_iter6cfg")


def agreement(rows: list[dict]) -> str:
    n = len(rows)
    agree = sum(1 for r in rows if r["human_class"] == r["judge_class"])
    hv = sum(1 for r in rows if r["human_class"] != "I")
    jv = sum(1 for r in rows if r["judge_class"] != "I")
    return f"n={n} agree {agree}/{n}={100 * agree / n:.1f}% human-valid {100 * hv / n:.1f}% judge-valid {100 * jv / n:.1f}% offset {100 * (jv - hv) / n:+.1f} pp"


def subset_ids(name: str) -> set[str]:
    ids: set[str] = set()
    for v in json.load(open(os.path.join(SUBSET, name))).values():
        ids.update(v if isinstance(v, list) else (v.get("report_ids") or []))
    return ids


def judge_units(root: str, side: str, tier: dict) -> set[tuple[str, str]]:
    units = set()
    for f in glob.glob(f"{root}/{side}-r*/pairs/*.json"):
        d = json.load(open(f))
        for o in d.get("report_outcomes") or []:
            if o["validity"] == "VALID_KNOWN":
                units.update((e, f"r{d['round']}") for e in (o.get("full_ledger_ids") or []) if e in tier)
    return units


def main() -> None:
    tier = {k: v["L"] for k, v in json.load(open(LEDGER))["items"].items()}
    for side, filt in (("current", "report_filter_current.json"), ("baseline", "report_filter_baseline.json")):
        ids = subset_ids(filt)
        rows = list(csv.DictReader(open(os.path.join(FULL, f"{side}_all_reports.tsv")), delimiter="\t"))
        print(f"{side}: subset {len(ids)} | in-subset {agreement([r for r in rows if r['report_id'] in ids])}")
        print(f"{side}: held-out {agreement([r for r in rows if r['report_id'] not in ids])}")
        print(f"{side}: all      {agreement(rows)}")
    idx = json.load(open(HUMAN_INDEX))["rows"]
    for tag, side_name, root, jside in (("v60 current", "v60_current", JUDGE_CURRENT, "current"), ("baseline", "x1v2_baseline", JUDGE_BASELINE, "baseline")):
        human = set()
        for r in idx:
            if r["side"] == side_name and r["validity"] == "VALID_KNOWN":
                fl = r["full_ledger_ids"]
                for e in ast.literal_eval(fl) if isinstance(fl, str) else fl:
                    if e in tier:
                        human.add((e, f"r{r['round']}"))
        if not glob.glob(f"{root}/{jside}-r*/pairs/*.json"):
            print(f"{tag}: judge cells not found under {root}; skip")
            continue
        judge = judge_units(root, jside, tier)
        print(f"{tag}: hit@1 human {len(human)} judge {len(judge)} offset {len(judge) - len(human):+d} (units judged FULL by both: {len(human & judge)})")
        for L in ("L0", "L1", "L2"):
            h = sum(1 for e, _ in human if tier[e] == L)
            j = sum(1 for e, _ in judge if tier[e] == L)
            print(f"  {L}: human {h} judge {j} offset {j - h:+d}")


if __name__ == "__main__":
    main()
