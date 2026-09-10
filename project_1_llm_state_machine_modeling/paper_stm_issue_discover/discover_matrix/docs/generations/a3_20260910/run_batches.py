"""A3-only native CLI scheduling: one method pool and three judge pools."""

import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid

PAPER = Path(__file__).resolve().parents[4]
REPORT = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"


def read(path):
    return json.loads(path.read_text())


def emit(**data):
    print(json.dumps({"time": time.time(), **data}), flush=True)


def launch(command, log):
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("x") as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT)
    emit(event="start", pid=process.pid, command=command, log=str(log))
    return process


def run(root, smoke_judge):
    from paper_stm_method.orchestration.runner import FROZEN_PAIR_IDS
    from paper_stm_judge.artifacts import adapt_evidence_discovery_release

    pairs = sorted(FROZEN_PAIR_IDS)
    smoke = {"0000", "0001", "0002"}
    # Smoke r1 is supplied as an already completed, audited method source.
    sources = [("sonnet", root / "sonnet/smoke-corrected")]
    batches = [
        ("sonnet", "remaining", [p for p in pairs if p not in smoke], None),
        ("sonnet", "smoke-r2", sorted(smoke), 2),
        ("sonnet", "smoke-r3", sorted(smoke), 3),
        ("luna", "full", pairs, None),
    ]
    method = None
    judges = {r: None for r in (1, 2, 3)}
    submitted = {("sonnet", p, 1) for p in smoke}
    completed = set()
    method_failures = []
    judge_failures = []
    for model, directory in sources:
        assert len(list(directory.glob("method/*/round-1.json"))) == 3
    prior_source = Path(read(smoke_judge / "run_manifest.json")["source_root"])
    for pair in smoke:
        old, old_audit, _, _ = adapt_evidence_discovery_release(prior_source / "method" / pair / "round-1.json", ())
        new, new_audit, _, _ = adapt_evidence_discovery_release(sources[0][1] / "method" / pair / "round-1.json", ())
        assert [r.model_dump() for r in old] == [r.model_dump() for r in new], "smoke judge input changed"
        emit(event="smoke_judge_reuse", pair=pair, original_source_hash=old_audit.source_hash,
             corrected_source_hash=new_audit.source_hash, judge_root=str(smoke_judge), exact_report_projection=True)
    while True:
        for pair in smoke:
            result = smoke_judge / "pairs" / f"{pair}.json"
            if result.exists() and read(result)["status"] == "completed":
                completed.add(("sonnet", pair, 1))
        if method is not None and method[0].poll() is not None:
            process, model, directory = method
            emit(event="method_terminal", pid=process.pid, returncode=process.returncode, model=model)
            if process.returncode:
                method_failures.append(str(directory))
            method = None
        if method is None and batches:
            model, name, selected, rnd = batches.pop(0)
            run_id = uuid.uuid4().hex
            output = root / model / name
            directory = output / run_id
            command = [sys.executable, "-W", "ignore", "-m", "paper_stm_method.cli",
                       "--report-root", str(REPORT), "--output-dir", str(output),
                       "--run-id", run_id, "--profile", "claude-sonnet-5" if model == "sonnet" else "gpt-5.6-luna",
                       "--ablation", "direct-report", "--rounds", "1" if rnd else "3",
                       "--workers", "16", "--allow-live", "--allow-full-live"]
            if rnd:
                command += ["--round", str(rnd)]
            for pair in selected:
                command += ["--pair-id", pair]
            method = (launch(command, root / "logs" / f"method-{model}-{name}.log"), model, directory)
            sources.append((model, directory))
        for rnd in judges:
            active = judges[rnd]
            if active is not None and active[0].poll() is not None:
                process, model, selected, directory = active
                for pair in selected:
                    path = directory / "pairs" / f"{pair}.json"
                    if path.exists() and read(path)["status"] == "completed":
                        completed.add((model, pair, rnd))
                    else:
                        judge_failures.append((model, pair, rnd, str(directory)))
                emit(event="judge_terminal", pid=process.pid, round=rnd, returncode=process.returncode,
                     judged=len(completed), failed=len(judge_failures))
                judges[rnd] = None
            if judges[rnd] is not None:
                continue
            for model, source in sources:
                ready = []
                for path in sorted(source.glob(f"method/*/round-{rnd}.json")):
                    pair = path.parent.name
                    if (model, pair, rnd) in submitted:
                        continue
                    cell = read(path)
                    if cell["eligible"] and cell["status"] in ("completed", "completed_with_diagnostics"):
                        ready.append(pair)
                # Eight ready cells fill one native pool; drain smaller tails too.
                source_done = (source / "summary.json").exists() or source.name == "smoke-corrected" or method is None or method[2] != source
                if not ready or (len(ready) < 8 and not source_done):
                    continue
                selected = ready[:8]
                run_id = uuid.uuid4().hex
                output = root / "judge" / model / f"r{rnd}"
                command = [sys.executable, "-W", "ignore", "-m", "paper_stm_judge.cli",
                           "--report-root", str(REPORT), "--ledger", str(PAPER / "discover_matrix/ledger_v2/ledger.json"),
                           "--source-format", "evidence_discovery_release", "--source-root", str(source),
                           "--output-dir", str(output), "--run-id", run_id, "--profile", "gpt-5.6-luna",
                           "--round", str(rnd), "--workers", "8", "--allow-live"]
                for pair in selected:
                    command += ["--pair-id", pair]
                    submitted.add((model, pair, rnd))
                judges[rnd] = (launch(command, root / "logs" / f"judge-{run_id}.log"), model, selected, output / run_id)
                break
        if method is None and not batches and all(value is None for value in judges.values()) and all(("sonnet", p, 1) in completed for p in smoke):
            break
        time.sleep(2)
    expected = {(model, pair, rnd) for model in ("sonnet", "luna") for pair in pairs for rnd in (1, 2, 3)}
    emit(event="terminal", completed=len(completed), missing=sorted(expected-completed),
         method_failures=method_failures, judge_failures=judge_failures)
    assert completed == expected and not method_failures and not judge_failures


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--smoke-judge", type=Path, required=True)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    if not args.allow_live:
        parser.error("explicit --allow-live is required")
    run(args.root.resolve(), args.smoke_judge.resolve())
