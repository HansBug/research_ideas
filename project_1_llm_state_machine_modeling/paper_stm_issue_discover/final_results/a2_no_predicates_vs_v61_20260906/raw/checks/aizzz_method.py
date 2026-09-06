"""Run only missing A2 cells on the registered Luna endpoint with the normal runtime."""
import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import multiprocessing
import os
from pathlib import Path

from paper_stm_method.orchestration import runner
from utils.structured_runtime import PublicStructuredRuntime

BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / "method_aizzz/af618190b34652b58ed0ae9ec231bdfe"
SOURCES = [BASE / "transport_recovery/55f3799341d046888d8b2e61261913c6",
           BASE / "method/2d9c2b12efb4498489af2f268e9ede94"]
REPORT = Path.cwd().with_name("research_ideas-2") / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60"
PROFILE = "aizzz-luna-eval"


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def provider_failed(cell):
    return any(isinstance(row.get("error"), dict) and (
        row["error"].get("code") in {"provider_error", "transport_error"}
        or row["error"].get("details", {}).get("message") == "No generations found in stream.")
        for row in cell.get("errors", []))


def run_cell(task):
    pair, rnd = task["pair_id"], task["round"]
    assert runner._model_config_hash(PROFILE) == task["model_config_hash"]
    runtime = PublicStructuredRuntime(PROFILE, ROOT / "llm", transport_retries=8, streaming=True)
    try:
        cell = runner._method_cell(pair=runner.load_pair(REPORT / "pairs" / pair), round_index=rnd,
            runtime=runtime, output_root=ROOT, run_identity=task["identity"])
        runner._finalize_w2_audit_links(output_root=ROOT, pair_id=pair, rounds_data=[cell])
        return {"pair_id": pair, "round": rnd, "status": cell["status"], "eligible": cell["eligible"]}
    finally:
        runtime.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    assert args.allow_live
    assert all(not Path(f"/proc/{pid}").exists() for pid in (2713929, 2713989, 2713992)), "old writer still exists"
    assert read(BASE / "checks/aizzz-cutover.json")["old_method_stopped"]
    ROOT.mkdir(parents=True, exist_ok=True)
    lock = (ROOT / "writer.lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    assert not (ROOT / "execution_identity.json").exists(), "already attempted; inspect receipts before repeating"
    old = read(SOURCES[-1] / "run_manifest.json")
    provenance = runner._source_provenance()
    assert not provenance["source_dirty"]
    config = runner.load_llm_registry().require(PROFILE)
    assert config.model == "gpt-5.6-luna" and str(config.base_url).rstrip("/") == "https://api.aizzz.xyz/v1"
    assert runner._prompt_schema_hash("no-predicates") == old["prompt_schema_hash"]
    selection = []
    for pair in old["selected_pair_ids"]:
        for rnd in (1, 2, 3):
            paths = [source / "method" / pair / f"round-{rnd}.json" for source in SOURCES]
            previous = next((path for path in paths if path.exists()), None)
            cell = read(previous) if previous else None
            reuse = cell is not None and not provider_failed(cell)
            if reuse:
                assert cell["status"] in {"completed", "completed_with_diagnostics", "failed_with_receipt"}
            selection.append({"pair_id": pair, "round": rnd, "action": "reuse" if reuse else "recover",
                "reason": "preserve_terminal_result" if reuse else "audited_provider_failure" if cell else "missing_at_provider_cutover",
                "old_path": str(previous) if previous else None, "old_hash": digest(previous) if previous else None})
    manifest = runner._prepare_run_manifest(output_root=ROOT, profile=PROFILE, ablation="no-predicates",
        run_id=ROOT.name, source_provenance=provenance, registry_version=old["registry_version"], registry_hash=old["registry_hash"],
        prompt_schema_hash=old["prompt_schema_hash"], input_data_hash=old["input_data_hash"], pair_input_hashes=old["pair_input_hashes"],
        rounds=3, selected_pair_ids=old["selected_pair_ids"], workers=16, transport_retries=8, streaming=True,
        selection_preflight=None, resume=False, predecessor_snapshot=str(SOURCES[0]), model_config_hash=runner._model_config_hash(PROFILE))
    identity = {"run_id": ROOT.name, "run_contract_hash": manifest.run_contract_hash, "ablation": "no-predicates",
                "source_provenance": provenance, "pair_input_hashes": old["pair_input_hashes"]}
    plan = {"schema": "a2.provider-cutover.v1", "run_id": ROOT.name, "root": str(ROOT), "selection": selection,
            "source_roots": [str(s) for s in SOURCES], "identity": identity, "workers": 16, "planned_cells": 162,
            "model_config_hash": manifest.model_config_hash, "script_hash": digest(Path(__file__)),
            "created_at": datetime.now(timezone.utc).isoformat()}
    runner.write_json(ROOT / "continuation_plan.json", plan)
    runner.write_json(ROOT / "execution_identity.json", {"pid": os.getpid(), "source_provenance": provenance,
        "profile": PROFILE, "workers": 16, "script_hash": plan["script_hash"], "started_at": plan["created_at"]})
    tasks = [{**row, "identity": identity, "model_config_hash": manifest.model_config_hash}
             for row in selection if row["action"] == "recover"]
    print(json.dumps({"pid": os.getpid(), "run_id": ROOT.name, "workers": 16, "reuse": 162 - len(tasks), "pending": len(tasks)}), flush=True)
    results = []
    with ProcessPoolExecutor(max_workers=16, mp_context=multiprocessing.get_context("spawn")) as pool:
        futures = {pool.submit(run_cell, task): task for task in tasks}
        for future in as_completed(futures):
            task = futures[future]
            try:
                result = future.result()
            except Exception as exc:
                result = {"pair_id": task["pair_id"], "round": task["round"], "status": "execution_error", "error": str(exc)}
            results.append(result)
            runner.write_json(ROOT / "continuation_progress.json", results)
            print(json.dumps(result), flush=True)
    runner.write_json(ROOT / "continuation_summary.json", {"status": "terminal", "results": results, "planned_cells": len(tasks)})


if __name__ == "__main__":
    main()
