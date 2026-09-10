"""Read-only, hash-checked Full source selection for the A4 tail experiment."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


REFERENCE = {
    "sonnet": ((536, 183, 104), (358, 475, 1419)),
    "luna": ((561, 198, 144), (573, 541, 1322)),
    "qwen": ((599, 256, 103), (346, 565, 1525)),
    "muse": ((544, 229, 137), (181, 475, 1318)),
}


def checked_json(path: Path, expected: str | None = None) -> tuple[dict, str]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if expected is not None and digest != expected.removeprefix("sha256:"):
        raise ValueError(f"Source hash mismatch: {path}")
    return json.loads(raw), digest


def contained(root: Path, relative: str) -> Path:
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f"Source escapes archive: {relative}")
    return path


def source_manifest(paper: Path, model: str) -> dict:
    """Verify method/judge identity and preserve raw historical predicate IDs."""
    e2 = paper / "final_results/e2_20260907"
    if model == "luna":
        index_path = e2 / "luna_history.json"
        index, index_hash = checked_json(index_path)
        selected = index["verification"]["arms"]["ours"]["cells"]
    else:
        index_path = e2 / model / "cells.json"
        index, index_hash = checked_json(index_path)
        selected = [cell for cell in index["cells"] if cell["arm"] == "ours"]
    cells = []
    labels, verdicts = Counter(), Counter()
    for row in selected:
        pair, round_index = row.get("pair", row.get("pair_id")), row["round"]
        if model == "luna":
            judge_path = contained(paper, row["source"])
            judge, judge_hash = checked_json(judge_path, row["sha256"])
            root = paper / "final_results/v61_source_divergence_vs_x1v2_baseline/raw"
            relative = (
                "v61_current_fill0045/method/0045/round-1.json"
                if (pair, round_index) == ("0045", 1)
                else f"v61_current/method/method/{pair}/round-{round_index}.json"
            )
            method_path = contained(root, relative)
            method, method_hash = checked_json(
                method_path, judge["adapter_audit"]["source_hash"]
            )
        else:
            method_path = contained(e2 / "raw", row["source"])
            judge_path = contained(e2 / "raw", row["judge_source"])
            method, method_hash = checked_json(method_path, row["sha256"])
            judge, judge_hash = checked_json(judge_path, row["judge_sha256"])
            if judge["adapter_audit"]["source_hash"].removeprefix("sha256:") != method_hash:
                raise ValueError(f"Judge/method source mismatch: {model}/{pair}/{round_index}")
        if not method["eligible"] or judge["status"] != "completed":
            raise ValueError(f"Ineligible frozen source: {model}/{pair}/{round_index}")
        if (method["pair_id"], method["round"]) != (pair, round_index):
            raise ValueError("Method source identity mismatch")
        if (judge["pair_id"], judge["round"]) != (pair, round_index):
            raise ValueError("Judge source identity mismatch")
        reports = method["report_issue_clusters"]
        outcomes = judge["report_outcomes"]
        report_ids = [report["issue_id"] for report in reports]
        judged_ids = [report["original_report_id"] for report in outcomes]
        if len(set(report_ids)) != len(report_ids) or sorted(report_ids) != sorted(judged_ids):
            raise ValueError("Final report/judgment bijection failed")
        candidates = method["stage_outputs"]["execute_batch"]["candidates"]
        obligations = [candidate["obligation_id"] for candidate in candidates]
        if len(set(obligations)) != len(obligations):
            raise ValueError("Duplicate frozen obligation")
        cell_labels = Counter(report["validity"] for report in outcomes)
        cell_verdicts = Counter(candidate["receipt"]["verdict"] for candidate in candidates)
        labels.update(cell_labels)
        verdicts.update(cell_verdicts)
        cells.append({
            "pair": pair, "round": round_index,
            "source": str(method_path.relative_to(paper)), "sha256": method_hash,
            "judge_source": str(judge_path.relative_to(paper)), "judge_sha256": judge_hash,
            "source_provenance": method["source_provenance"],
            "source_run_id": method["run_id"], "pair_input_hash": method["pair_input_hash"],
            "candidate_count": len(candidates), "report_count": len(reports),
            "verdicts": dict(cell_verdicts), "labels": dict(cell_labels),
        })
    identities = {(cell["pair"], cell["round"]) for cell in cells}
    pairs = {pair for pair, _ in identities}
    if len(cells) != 162 or len(pairs) != 54 or identities != {
        (pair, round_index) for pair in pairs for round_index in (1, 2, 3)
    }:
        raise ValueError(f"Incomplete source population: {model}")
    expected_labels, expected_verdicts = REFERENCE[model]
    if tuple(labels[key] for key in ("VALID_KNOWN", "VALID_NOVEL", "INVALID")) != expected_labels:
        raise ValueError(f"Full label reference mismatch: {model}: {labels}")
    if dict(verdicts) != dict(zip(("true", "false", "unknown"), expected_verdicts)):
        raise ValueError(f"Full verdict reference mismatch: {model}: {verdicts}")
    return {
        "schema": "paper1.a4.full-source-manifest.v1", "model": model,
        "index": str(index_path.relative_to(paper)), "index_sha256": index_hash,
        "labels": dict(labels), "verdicts": dict(verdicts),
        "cells": sorted(cells, key=lambda cell: (cell["pair"], cell["round"])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--model", choices=tuple(REFERENCE), action="append")
    args = parser.parse_args()
    for model in args.model or REFERENCE:
        manifest = source_manifest(args.paper_root.resolve(), model)
        print(json.dumps({key: value for key, value in manifest.items() if key != "cells"}, sort_keys=True))


if __name__ == "__main__":
    main()
