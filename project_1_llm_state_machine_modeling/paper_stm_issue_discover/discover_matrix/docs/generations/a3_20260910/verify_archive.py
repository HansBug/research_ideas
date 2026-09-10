"""Verify frozen A3 arithmetic with stdlib only, without private raw streams."""

import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path

from analyze_a3 import arithmetic, content_breakdown, per_round
from verify_sources import PAPER, digest, read


def canonical(value):
    return json.loads(json.dumps(value))


def predicate_view(data):
    path = PAPER / "evaluation/src/paper_stm_evaluation/predicate_id_mapping.py"
    spec = importlib.util.spec_from_file_location("a3_predicate_mapping", path)
    mapping = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mapping)
    rows = []
    for model, arms in data["models"].items():
        for arm in ("a3", "full"):
            version = mapping.PRE_P1_REGISTRY if (model, arm) == ("luna", "full") else mapping.CURRENT_REGISTRY
            counts = Counter((r["predicate_id"], r["validity"]) for r in arms[arm]["reports"])
            for predicate in sorted({p for p, _ in counts}, key=lambda p: p or ""):
                rows.append({"model": model, "arm": arm, "source_registry": version,
                             "original_predicate_id": predicate,
                             "current_predicate_id": mapping.current_predicate_id(version, predicate),
                             **{label: counts[predicate, validity] for label, validity in
                                (("K", "VALID_KNOWN"), ("N", "VALID_NOVEL"), ("I", "INVALID"))}})
    scope = "Labels on frozen published reports only. Preserve original IDs; no execution or judgement changes. Luna Full is pre-P1; Sonnet Full and both A3 runs use P1."
    if set(data["models"]) == {"qwen", "muse"}:
        scope = "Labels on frozen Qwen/Muse published reports only; Full and A3 use P1. Preserve original IDs; no execution or judgement changes."
    return {"schema": "a3.predicate-report-view.v1", "mapping_sha256": digest(path), "rows": rows, "scope": scope}


def verify(archive, models=("sonnet", "luna")):
    manifest = read(archive / "archive_manifest.json")
    for name, expected_hash in manifest["files"].items():
        assert digest(archive / name) == expected_hash, name
    ledger = PAPER / "discover_matrix/ledger_v2/ledger.json"
    assert digest(ledger) == manifest["ledger_sha256"]
    items = read(ledger)["items"]
    data, math = read(archive / "results.json"), arithmetic()
    assert predicate_view(data) == read(archive / "predicate_view.json")
    assert data["complete"] and set(data["models"]) == set(models)
    if set(models) == {"qwen", "muse"}:
        from analyze_open_judge import four_model_summary
        assert canonical(four_model_summary(data)) == read(archive / "four_model_summary.json"), "four-model summary"
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
        mappings = [r for c in arms["a3"]["cells"] for r in c["generation_mapping"]]
        assert len(mappings) == arms["a3"]["funnel"]["generated"]
        assert {r["final_report_id"] for r in mappings if r["final_report_id"]} == {r["original_report_id"] for r in arms["a3"]["reports"]}
        for field, prefix in (("publication_status", "publication_"), ("verdict", "raw_verdict_"), ("witness_level", "witness_")):
            for value, count in Counter(r[field] for r in mappings).items():
                assert arms["a3"]["funnel"][prefix + value] == count
        comparison = math.compare(arms["a3"], arms["full"], items)
        comparison["scope"] = arms["comparison"]["scope"]
        comparison["content"] = content_breakdown(arms["a3"], arms["full"], items)
        assert canonical(comparison) == arms["comparison"], (model, "comparison")
    return {model: {"cells": len(arms["a3"]["cells"]), "reports": len(arms["a3"]["reports"])} for model, arms in data["models"].items()}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=PAPER / "final_results/a3_20260910")
    parser.add_argument("--raw-root", type=Path)
    parser.add_argument("--model", action="append", choices=("sonnet", "luna", "qwen", "muse"), help="Expected model group; defaults to the original Sonnet/Luna archive.")
    args = parser.parse_args()
    result = verify(args.archive, args.model or ("sonnet", "luna"))
    if args.raw_root:
        inventory = read(args.archive / "raw_index.json")["files"]
        for name, record in inventory.items():
            path = args.raw_root / name
            assert not path.is_symlink() and path.stat().st_size == record["bytes"], name
            assert digest(path) == record["sha256"], name
        result["verified_raw_files"] = len(inventory)
    print(json.dumps(result, indent=2))
