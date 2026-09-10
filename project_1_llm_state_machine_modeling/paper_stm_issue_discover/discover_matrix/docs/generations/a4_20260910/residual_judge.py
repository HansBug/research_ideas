"""Export only A4 residual publications to the unchanged native Luna judge CLI."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import uuid

from utils.artifact_io import write_json
from paper_stm_evaluation.a4_run import verify
from paper_stm_evaluation.a4_sources import checked_json
from paper_stm_judge.protocol import PROTOCOL_SHA256, PROTOCOL_VERSION, prompt_hash


FIELDS = (
    "issue_id", "title", "locus_names", "locus_kind", "property", "expected", "observed",
    "candidate_reason", "reason", "candidate_basis", "source_refs", "element_refs", "requirement_quote",
)


def prepare(paper: Path, root: Path) -> dict:
    counts = verify(paper, root)
    if counts["eligible_cells"] != 162:
        raise ValueError("Finish and verify all 162 method tails before this judge batch")
    manifest = json.loads((root / "manifest.json").read_text())
    filters = {round_index: {} for round_index in (1, 2, 3)}
    completed = {}
    for path in sorted((root / "judge").glob("*/pairs/*.json")):
        record = json.loads(path.read_text())
        if record.get("status") != "completed":
            continue
        if (record["model_profile"] != "gpt-5.6-luna" or record["k_closure"] != "relation_first"
                or record["validity_aggregation"] != "arbitration"
                or record["validity_arbitration_trigger"] != "any" or record["closure_profile"] != "full"
                or record["protocol_sha256"] != PROTOCOL_SHA256
                or record["protocol_version"] != PROTOCOL_VERSION
                or record["prompt_template_hash"] != prompt_hash()
                or record.get("validity_extra_readings")):
            raise ValueError("Residual judge protocol settings changed")
        source_path = root / "judge_source/method" / record["pair_id"] / f"round-{record['round']}.json"
        _, source_hash = checked_json(source_path, record["adapter_audit"]["source_hash"])
        for report in record["report_outcomes"]:
            key = (record["pair_id"], record["round"], report["original_report_id"])
            if key in completed:
                raise ValueError("Duplicate completed residual judgment")
            completed[key] = {"outcome": report, "source": str(path.relative_to(root)),
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "source_hash": source_hash}
    final = []
    for row in manifest["sources"]["cells"]:
        cell_root = root / "cells" / row["pair"] / f"round-{row['round']}"
        tail = json.loads((cell_root / "tail.json").read_text())
        accounting = json.loads((cell_root / "accounting.json").read_text())
        source_view = {
            "schema": "paper1.a4.judge-publication-view.v1", "pair_id": row["pair"], "round": row["round"],
            "eligible": tail["eligible"], "status": "completed_with_diagnostics" if tail["errors"] else "completed",
            "tail_sha256": hashlib.sha256((cell_root / "tail.json").read_bytes()).hexdigest(),
            "report_issue_clusters": [{key: report[key] for key in FIELDS if key in report}
                                      for report in tail["report_issue_clusters"]],
        }
        destination = root / "judge_source/method" / row["pair"] / f"round-{row['round']}.json"
        if destination.exists():
            if json.loads(destination.read_text()) != source_view:
                raise ValueError("Residual publication input changed")
        else:
            write_json(destination, source_view)
        pending = []
        for report in accounting["reports"]:
            if report["route"] == "residual":
                key = (row["pair"], row["round"], report["report_id"])
                if key in completed:
                    decision = completed.pop(key)
                    report.update(route="newly_judged", outcome=decision["outcome"], judge_provenance=decision)
                else:
                    pending.append(report["report_id"])
            elif report["route"] == "reused_full":
                report["reuse_id_map"] = {
                    "full_report_id": report["full_equivalent_report_id"], "a4_report_id": report["report_id"],
                    "ledger_ids": "unchanged canonical IDs from the original relation assignments",
                    "source_refs": "Original anonymous references remain attributed to the frozen Full judge source.",
                }
        accounting["pending"] = len(pending)
        final.append(accounting)
        if pending:
            filters[row["round"]][row["pair"]] = pending
    if completed:
        raise ValueError("Completed judge includes reports outside the residual population")
    write_json(root / "final_accounting.json", {"cells": final, "pending": sum(cell["pending"] for cell in final)})
    return filters


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--input-root", type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    filters = prepare(args.paper_root.resolve(), args.root.resolve())
    pending = {r: sum(map(len, f.values())) for r, f in filters.items()}
    print(json.dumps({"residual_pending": pending}), flush=True)
    if not args.allow_live or not any(pending.values()):
        return
    if not args.input_root or not args.ledger:
        parser.error("Live residual judge requires frozen --input-root and --ledger")
    commands = []
    for round_index, workers in ((1, 3), (2, 3), (3, 2)):
        if not filters[round_index]:
            continue
        batch = f"r{round_index}-{uuid.uuid4().hex}"
        filter_path = args.root / "judge_filters" / f"{batch}.json"
        write_json(filter_path, filters[round_index])
        commands.append([
            sys.executable, "-m", "paper_stm_judge.cli", "--report-root", str(args.input_root),
            "--ledger", str(args.ledger), "--source-format", "evidence_discovery_release",
            "--source-root", str(args.root / "judge_source"), "--output-dir", str(args.root / "judge"),
            "--run-id", batch, "--profile", "gpt-5.6-luna", "--round", str(round_index),
            "--workers", str(workers), "--transport-retries", "8", "--validity-readings", "2",
            "--validity-aggregation", "arbitration", "--validity-arbitration-trigger", "any",
            "--k-closure", "relation_first", "--closure-profile", "full",
            "--report-filter", str(filter_path), "--allow-live",
        ])
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(subprocess.run, command, check=False) for command in commands]
        codes = [future.result().returncode for future in as_completed(futures)]
    remaining = prepare(args.paper_root.resolve(), args.root.resolve())
    print(json.dumps({"judge_exit_codes": codes, "residual_pending": {r: sum(map(len, f.values())) for r, f in remaining.items()}}))


if __name__ == "__main__":
    main()
