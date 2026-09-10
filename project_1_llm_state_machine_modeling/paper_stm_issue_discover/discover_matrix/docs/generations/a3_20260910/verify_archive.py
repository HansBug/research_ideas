"""Verify frozen A3 arithmetic with stdlib only, without private raw streams."""

import argparse
from collections import Counter
import json
from pathlib import Path

from analyze_a3 import arithmetic, content_breakdown, per_round
from verify_sources import PAPER, digest, read


def canonical(value):
    return json.loads(json.dumps(value))


def verify(archive):
    manifest = read(archive / "archive_manifest.json")
    for name, expected_hash in manifest["files"].items():
        assert digest(archive / name) == expected_hash, name
    ledger = PAPER / "discover_matrix/ledger_v2/ledger.json"
    assert digest(ledger) == manifest["ledger_sha256"]
    items = read(ledger)["items"]
    data, math = read(archive / "results.json"), arithmetic()
    assert data["complete"] and set(data["models"]) == {"sonnet", "luna"}
    assert len(items) == data["ledger_items"] == 145
    assert data["expected_round_units"] == 435
    for model, arms in data["models"].items():
        for label in ("a3", "full"):
            arm = arms[label]
            cells = {(c["pair_id"], c["round"]) for c in arm["cells"]}
            pairs = {p for p, _ in cells}
            assert len(pairs) == 54 and len(arm["cells"]) == 162
            assert cells == {(p, rnd) for p in pairs for rnd in (1, 2, 3)}
            reports = arm["reports"]
            assert len({r["original_report_id"] for r in reports}) == len(reports)
            counts = Counter((r["pair_id"], r["round"]) for r in reports)
            assert set(counts) <= cells
            assert all(counts[c["pair_id"], c["round"]] == c["reports"] for c in arm["cells"])
            for report in reports:
                assert all(items[e]["pair"] == report["pair_id"] for e in report["full_ledger_ids"] + report["partial_ledger_ids"])
            metrics = math.calculate(reports, items)
            metrics["valid_reports"] = metrics["K"] + metrics["N"]
            metrics["I_per_completed_cell"] = math.ratio(metrics["I"], 162)
            assert canonical(metrics) == arm["metrics"], (model, label, "metrics")
            assert canonical(per_round(reports, arm["cells"], items, math)) == arm["per_round"]
        assert all(c["judged"] and c["eligible"] for c in arms["a3"]["cells"])
        assert not arms["a3"]["coverage"]["missing_judge_cells"]
        assert not arms["a3"]["coverage"]["missing_method_cells"]
        assert arms["a3"]["funnel"]["published"] == len(arms["a3"]["reports"])
        comparison = math.compare(arms["a3"], arms["full"], items)
        comparison["scope"] = arms["comparison"]["scope"]
        comparison["content"] = content_breakdown(arms["a3"], arms["full"], items)
        assert canonical(comparison) == arms["comparison"], (model, "comparison")
    return {model: {"cells": len(arms["a3"]["cells"]), "reports": len(arms["a3"]["reports"])} for model, arms in data["models"].items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=PAPER / "final_results/a3_20260910")
    args = parser.parse_args()
    print(json.dumps(verify(args.archive), indent=2))
