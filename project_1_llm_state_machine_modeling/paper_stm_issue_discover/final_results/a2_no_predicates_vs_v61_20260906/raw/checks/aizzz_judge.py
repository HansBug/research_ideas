"""Freeze unjudged A2 sources, then replace this process with the native judge CLI."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys

import aizzz_method as method

PAPER = Path.cwd() / "project_1_llm_state_machine_modeling/paper_stm_issue_discover"
spec = importlib.util.spec_from_file_location("a2_analysis", PAPER / "discover_matrix/docs/generations/a2_no_predicates_20260906/analyze.py")
analysis = importlib.util.module_from_spec(spec)
spec.loader.exec_module(analysis)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, required=True, choices=(1, 2, 3))
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    assert args.allow_live
    assert not Path("/proc/2749908").exists(), "old scheduler is still running"
    plan_path = method.ROOT / "continuation_plan.json"
    _, selection, _ = analysis.load_selection(plan_path)
    submitted = set()
    output = method.BASE / "judge_aizzz"
    for parent in (method.BASE / "judge", output):
        for manifest_path in parent.glob("*/run_manifest.json"):
            manifest = analysis.read(manifest_path)
            if manifest["run_id"] == "82023a87854e5198b71a3ca48832a548":
                continue
            if (manifest_path.parent / "interruption_receipt.json").exists():
                keys = {(cell["pair_id"], cell["round"]) for path in (manifest_path.parent / "pairs").glob("*.json")
                        for cell in [analysis.read(path)]}
            else:
                assert any((manifest_path.parent / name).exists() for name in ("summary.json", "failure_summary.json")), "judge still active"
                keys = {(p, r) for p in manifest["selected_pair_ids"] for r in manifest["selected_rounds"]}
            assert not submitted & keys, "duplicate judge submission"
            submitted.update(keys)
    ready = []
    view = output / f"sources-{args.run_id}"
    sources = {}
    for (pair, rnd), row in sorted(selection.items()):
        if rnd != args.round or (pair, rnd) in submitted or not row["path"].is_file():
            continue
        cell = analysis.read(row["path"])
        if not cell["eligible"] or method.provider_failed(cell):
            continue
        target = view / "method" / pair / f"round-{rnd}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(row["path"])
        sources[pair] = {"path": str(row["path"]), "sha256": analysis.digest(row["path"])}
        ready.append(pair)
    assert ready, "no completed unjudged cells for this round"
    config = method.runner.load_llm_registry().require(method.PROFILE)
    config_hash = method.runner._model_config_hash(method.PROFILE)
    assert config_hash == analysis.LUNA_CONFIGS[method.PROFILE]
    command = [sys.executable, "-m", "paper_stm_judge.cli", "--source-format", "evidence_discovery_release",
        "--source-root", str(view), "--report-root", str(method.REPORT), "--ledger", str(PAPER / "discover_matrix/ledger_v2/ledger.json"),
        "--output-dir", str(output), "--run-id", args.run_id, "--round", str(args.round), "--profile", method.PROFILE,
        "--workers", "16", "--transport-retries", "8", "--validity-readings", "2", "--validity-aggregation", "arbitration",
        "--validity-arbitration-trigger", "any", "--k-closure", "relation_first", "--closure-profile", "full", "--allow-live"]
    for pair in ready:
        command.extend(["--pair-id", pair])
    receipt = {"run_id": args.run_id, "profile": method.PROFILE, "model": config.model,
        "endpoint": str(config.base_url).rstrip("/"), "model_config_hash": config_hash, "workers": 16,
        "source_provenance": method.runner._source_provenance(), "created_at": datetime.now(timezone.utc).isoformat(),
        "selection_plan_hash": analysis.digest(plan_path), "source_cells": sources, "command": command}
    assert not receipt["source_provenance"]["source_dirty"]
    receipt_path = method.BASE / "checks" / f"judge-request-{args.run_id}.json"
    assert not receipt_path.exists(), "launch already attempted"
    method.runner.write_json(receipt_path, receipt)
    print(json.dumps({"event": "exec_native_judge", "pid": os.getpid(), "run_id": args.run_id, "pairs": ready, "round": args.round, "workers": 16}), flush=True)
    os.execv(sys.executable, command)


if __name__ == "__main__":
    main()
