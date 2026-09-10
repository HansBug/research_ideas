"""Run only the frozen-Full final-report tail, then deterministic A4 accounting."""

from __future__ import annotations

import argparse
import fcntl
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import multiprocessing
from pathlib import Path
import subprocess
import time
import uuid

from utils.artifact_io import write_json
from utils.llm import load_llm_registry
from utils.structured_runtime import PublicStructuredRuntime
from paper_stm_method.orchestration.runner import _source_provenance

from .a4_accounting import account_cell
from .a4_replay import TREATMENT, digest, mask_prepared, replay_tail, restore_pair
from .a4_sources import checked_json, source_manifest


def code_identity(paper: Path) -> dict:
    repo = paper.parents[1]
    prefixes = ["utils/", str(paper.relative_to(repo) / "method/src/"),
                str(paper.relative_to(repo) / "evaluation/src/paper_stm_evaluation/")]
    paths = subprocess.check_output(["git", "ls-files", "-z", "--", *prefixes], cwd=repo).decode().split("\0")
    hashes = {path: hashlib.sha256((repo / path).read_bytes()).hexdigest()
              for path in paths if path.endswith(".py") or path.endswith(".json")}
    return {"source_provenance": _source_provenance(), "files_hash": digest(hashes), "files": hashes}


def freeze(paper: Path, output: Path, model: str, profile: str) -> dict:
    if "final_results" in output.resolve().parts:
        raise ValueError("A4 live artifacts must not be written into frozen final_results")
    sources = source_manifest(paper, model)
    config = load_llm_registry().require(profile)
    code = code_identity(paper)
    if code["source_provenance"]["source_dirty"]:
        raise ValueError("Commit the reviewed implementation before measured calls")
    identity = {
        "treatment": TREATMENT, "model": model, "profile": profile,
        "source_manifest_hash": digest(sources), "code_hash": code["files_hash"],
        "profile_hash": digest(config.model_dump(mode="json", exclude={"api_key", "pricing"})),
        "stream": True, "run_output_override": None,
        "source_input_policy": "frozen twelve-role artifact hashes; no inspection recomputation",
    }
    path = output / "manifest.json"
    if path.exists():
        manifest = json.loads(path.read_text())
        if manifest["identity"] != identity:
            raise ValueError("A4 resume provenance/configuration mismatch; use a separate run")
        return manifest
    manifest = {
        "schema": "paper1.a4.run.v1", "identity": identity, "namespace": digest(identity),
        "run_id": uuid.uuid4().hex, "created_at": datetime.now(timezone.utc).isoformat(),
        "config": config.public_dict(), "code": code, "sources": sources,
        "dependencies": {
            "reused": ["prepare", "contract_extraction", "contract_completion", "discovery_grounding",
                       "candidate_order", "routing", "binding", "plan"],
            "invalidated": ["execution_view", "satisfied_partition", "old_d", "validate_d", "publish"],
            "llm_recomputed": ["d_adjudication", "necessary_d_adjudication_correction"],
            "deterministic_recomputed": ["validate_d", "publish", "deduplication", "folding", "accounting"],
        },
    }
    write_json(path, manifest)
    return manifest


def execute_cell(task: dict) -> dict:
    paper, root, input_root = (Path(task[key]) for key in ("paper", "output", "input_root"))
    manifest, row = task["manifest"], task["source"]
    cell_root = root / "cells" / row["pair"] / f"round-{row['round']}"
    result_path = cell_root / "tail.json"
    source, source_hash = checked_json(paper / row["source"], row["sha256"])
    judge, _ = checked_json(paper / row["judge_source"], row["judge_sha256"])
    prepared = [mask_prepared(item) for item in source["stage_outputs"]["execute_batch"]["candidates"]]
    masked = [{key: value.model_dump(mode="json") if hasattr(value, "model_dump") else value
               for key, value in item.items()} for item in prepared]
    identity = {"namespace": manifest["namespace"], "source_hash": source_hash,
                "masked_input_hash": digest(masked), "pair": row["pair"], "round": row["round"]}
    if result_path.exists():
        previous = json.loads(result_path.read_text())
        if previous["identity"] != identity:
            raise ValueError("A4 cell resume source/masked-input mismatch")
        if previous["eligible"]:
            return {"pair": row["pair"], "round": row["round"], "reused_cell": True,
                    "reports": len(previous["report_issue_clusters"])}
    pair = restore_pair(source, input_root)
    attempt_root = cell_root / "attempts" / uuid.uuid4().hex
    write_json(cell_root / "masked_input.json", {"identity": identity, "candidates": masked})
    started = time.monotonic()
    runtime = PublicStructuredRuntime(manifest["identity"]["profile"], attempt_root / "provider", streaming=True)
    try:
        result = replay_tail(
            pair=pair, prepared=prepared, runtime=runtime, output_root=attempt_root,
            run_identity={"run_id": manifest["run_id"]}, round_index=row["round"],
            cache_root=cell_root / "stage_cache", namespace=digest(identity),
        )
    finally:
        runtime.close()
    result.update(identity=identity, source=row, elapsed_seconds=time.monotonic() - started,
                  ended_at=datetime.now(timezone.utc).isoformat())
    write_json(attempt_root / "tail.json", result)
    write_json(result_path, result)
    accounting = account_cell(source, judge, result)
    write_json(cell_root / "accounting.json", accounting)
    checked_json(paper / row["source"], row["sha256"])
    return {"pair": row["pair"], "round": row["round"], "eligible": result["eligible"],
            "reports": len(accounting["reports"]), "residual": accounting["pending"],
            "routes": {route: sum(item["route"] == route for item in accounting["reports"])
                       for route in ("oracle_true_I", "reused_full", "residual")},
            "calls": result["counters"]["terminal_structured_calls"],
            "elapsed_seconds": result["elapsed_seconds"], "errors": len(result["errors"])}


def verify(paper: Path, root: Path) -> dict:
    manifest = json.loads((root / "manifest.json").read_text())
    sources = source_manifest(paper, manifest["identity"]["model"])
    if digest(sources) != manifest["identity"]["source_manifest_hash"]:
        raise ValueError("Frozen source manifest drift")
    counts = {"completed_cells": 0, "eligible_cells": 0, "reports": 0,
              "oracle_true_I": 0, "reused_full": 0, "residual": 0}
    for row in sources["cells"]:
        cell_root = root / "cells" / row["pair"] / f"round-{row['round']}"
        if not (cell_root / "tail.json").exists():
            continue
        result = json.loads((cell_root / "tail.json").read_text())
        if result["identity"]["namespace"] != manifest["namespace"]:
            raise ValueError("A4 output namespace mismatch")
        source, _ = checked_json(paper / row["source"], row["sha256"])
        judge, _ = checked_json(paper / row["judge_source"], row["judge_sha256"])
        accounting = account_cell(source, judge, result)
        if accounting != json.loads((cell_root / "accounting.json").read_text()):
            raise ValueError("A4 accounting does not reconstruct")
        if result["counters"]["upstream_generation_calls"] or result["counters"]["backend_execution_calls"]:
            raise ValueError("A4 upstream/backend execution invariant violated")
        counts["completed_cells"] += 1
        counts["eligible_cells"] += result["eligible"]
        counts["reports"] += len(accounting["reports"])
        for report in accounting["reports"]:
            counts[report["route"]] += 1
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("freeze", "run", "verify"))
    parser.add_argument("--paper-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--input-root", type=Path)
    parser.add_argument("--model", choices=("sonnet", "luna"))
    parser.add_argument("--profile")
    parser.add_argument("--workers", type=int, default=16)
    parser.add_argument("--limit", type=int, help="Preselected prefix smoke; successful cells remain in the same population")
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    paper, root = args.paper_root.resolve(), args.output.resolve()
    if args.action == "verify":
        print(json.dumps(verify(paper, root), sort_keys=True)); return
    if not args.model or not args.profile:
        parser.error("--model and --profile are required")
    manifest = freeze(paper, root, args.model, args.profile)
    if args.action == "freeze":
        print(json.dumps({"namespace": manifest["namespace"], "source_cells": len(manifest["sources"]["cells"])})); return
    if not args.allow_live or not args.input_root or not 1 <= args.workers <= 16:
        parser.error("run requires --allow-live, --input-root and 1..16 workers")
    cells = manifest["sources"]["cells"][:args.limit]
    started = time.monotonic()
    with (root / ".run.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with ProcessPoolExecutor(max_workers=args.workers, mp_context=multiprocessing.get_context("spawn")) as pool:
            futures = [pool.submit(execute_cell, {"paper": str(paper), "output": str(root),
                       "input_root": str(args.input_root.resolve()), "manifest": manifest, "source": cell}) for cell in cells]
            for index, future in enumerate(as_completed(futures), 1):
                print(json.dumps({"finished": index, "total": len(cells),
                                  "batch_elapsed_seconds": time.monotonic() - started, **future.result()}), flush=True)
    print(json.dumps(verify(paper, root), sort_keys=True))


if __name__ == "__main__":
    main()
