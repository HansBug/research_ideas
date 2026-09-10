"""Drain existing round pools, then judge every remaining current A3 cell once."""

import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys
import time
import uuid

from analyze_a3 import analyze
from run_batches import PAPER, REPORT, emit, launch
from utils.artifact_io import write_json


def finish_round(root, rnd, predecessor_pid):
    while predecessor_pid:
        status = subprocess.run(["ps", "-p", str(predecessor_pid), "-o", "stat="], capture_output=True, text=True, check=False).stdout.strip()
        if not status or status.startswith("Z"):
            break
        time.sleep(2)
    data = analyze(root, allow_partial=True)
    outcomes = []
    for model in ("sonnet", "luna"):
        arm = data["models"][model]["a3"]
        selected = [c for c in arm["cells"] if c["round"] == rnd and not c["judged"]]
        assert arm["coverage"]["eligible_cells"] == 162
        if not selected:
            continue
        source = root / "judge_source" / model / f"r{rnd}"
        for cell in selected:
            path = source / "method" / cell["pair_id"] / f"round-{rnd}.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            assert not path.exists(), "a frozen selected source must not be overwritten"
            path.symlink_to(cell["source"])
        run_id = uuid.uuid4().hex
        write_json(source / "selection.json", {"schema": "a3.remaining-judge-selection.v1", "model": model, "round": rnd,
                   "workers": 8, "predecessor_pid": predecessor_pid, "cells": selected,
                   "reason": "All method generations are frozen; completed identical projections are excluded before one native remaining batch."})
        command = [sys.executable, "-W", "ignore", "-m", "paper_stm_judge.cli",
                   "--report-root", str(REPORT), "--ledger", str(PAPER / "discover_matrix/ledger_v2/ledger.json"),
                   "--source-format", "evidence_discovery_release", "--source-root", str(source),
                   "--output-dir", str(root / "judge" / model / f"r{rnd}-remaining"), "--run-id", run_id,
                   "--profile", "gpt-5.6-luna", "--round", str(rnd), "--workers", "8", "--allow-live"]
        for cell in selected:
            command += ["--pair-id", cell["pair_id"]]
        process = launch(command, root / "logs" / f"judge-final-{run_id}.log")
        code = process.wait()
        emit(event="remaining_judge_terminal", model=model, round=rnd, pid=process.pid, returncode=code, selected=len(selected))
        outcomes.append(code)
    return outcomes


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--predecessor-pids", nargs=3, type=int, required=True, metavar=("R1", "R2", "R3"))
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    if not args.allow_live:
        parser.error("explicit --allow-live is required")
    with ThreadPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(finish_round, args.root.resolve(), rnd, pid) for rnd, pid in enumerate(args.predecessor_pids, 1)]
        results = [future.result() for future in futures]
    if any(code for codes in results for code in codes):
        raise SystemExit("One or more native batches retained failures; inspect receipts without resampling successful cells.")
