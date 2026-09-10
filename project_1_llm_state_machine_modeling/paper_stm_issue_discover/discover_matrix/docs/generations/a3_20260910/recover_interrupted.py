"""Preserve completed cells and recover an externally interrupted A3 batch."""

import argparse
from pathlib import Path
import uuid

from paper_stm_method.inputs import load_pair
from paper_stm_method.orchestration import runner
from paper_stm_method.orchestration.direct_report import DirectReportResponse, build_prompt
from utils import structured_runtime as runtime
from utils.artifact_io import write_json
from verify_sources import PAPER, read, digest


def recover(source, root):
    manifest = read(source / "run_manifest.json")
    report_root = PAPER / "pipeline/representation/reports/llms_emp_r45_java_60"
    assert manifest["ablation"] == "direct-report"
    config = runner.load_llm_registry().require(manifest["profile"])
    assert runner._model_config_hash(manifest["profile"]) == manifest["model_config_hash"]
    expected = {(p, r) for p in manifest["selected_pair_ids"] for r in (1, 2, 3)}
    complete = {(read(p)["pair_id"], read(p)["round"]) for p in source.glob("method/*/round-*.json")}
    recovered = set()
    directory = root / "sonnet/recovered"
    assert not directory.exists()
    identity = {"ablation": "direct-report", "run_id": uuid.uuid4().hex,
                "source_provenance": runner._source_provenance(),
                "run_contract_hash": runner._hash_json({"source_manifest": digest(source / "run_manifest.json"), "recovery_code": runner._source_provenance()})}
    audit = {"schema": "a3.interruption-recovery.v1", "identity": identity,
             "reason": "Scheduler process teardown unexpectedly terminated its method child; completed artifacts are preserved. No quality-based resampling.",
             "source_root": str(source), "source_manifest_hash": digest(source / "run_manifest.json"),
             "completed_before_recovery": sorted(complete), "saved_generations": []}
    for pair_id, rnd in sorted(expected - complete):
        result_path = source / "llm/method" / pair_id / f"round-{rnd}/direct-report/cell-attempt-1/result.json"
        if not result_path.exists():
            continue
        result = read(result_path)
        assert result["status"] == "success" and result["real_llm"]
        response = DirectReportResponse.model_validate(result["output"])
        pair = load_pair(report_root / "pairs" / pair_id)
        prompt = build_prompt(pair)
        rows = runtime._usage_rows(result, outer_attempt=1)
        records = runtime._read_audit_records(result_path.with_name("audit.jsonl"))
        runtime._annotate_usage_billing(rows, audit_records=records, final_error=None, actual_outer_retry=False)
        outcome = runtime.StructuredCallOutcome(
            kind="direct_report", status="success", response=response, result=result,
            attempts=[{"outer_attempt": 1, "status": "success", "provider_error": False,
                       "result_path": str(result_path), "audit_path": str(result_path.with_name("audit.jsonl")),
                       "result_hash": digest(result_path), "recovery": "saved real generation; no provider call"}],
            schema_validation_failures=runtime._schema_validation_failures(records, DirectReportResponse, outer_attempt=1),
            usage=rows, cost=runtime._cost_for_usage(rows, config.pricing), real_llm=True,
            context_budget=runtime.StructuredContextBudget(
                mode="structured_llm", projection_version="stage-context-projection.v6", prompt_characters=len(prompt),
                estimated_prompt_tokens=(len(prompt)+3)//4, provider_input_tokens=sum(r.get("input_tokens", 0) for r in rows),
                context_window_tokens=result["context_window_tokens"], max_output_tokens=result["max_output_tokens"],
                truncation_applied=False, projection_decision="Saved complete provider result recovered after process interruption.",
                reason="Prompt reconstructed from unchanged pair and A3 schema; raw result retained.", basis="source manifest, raw output and usage"),
            reason="Recovered a successful committed provider result after external process interruption.",
            basis="Original provider output, audit, usage and exact schema validation; no new sampling.")

        class Saved:
            def call(self, **kwargs):
                assert kwargs["prompt"] == prompt
                return outcome

        cell = runner._method_cell(pair=pair, round_index=rnd, runtime=Saved(), output_root=directory, run_identity=identity)
        runner._finalize_w2_audit_links(output_root=directory, pair_id=pair_id, rounds_data=[cell])
        recovered.add((pair_id, rnd))
        audit["saved_generations"].append({"pair_id": pair_id, "round": rnd, "source": str(result_path), "sha256": digest(result_path)})
    missing = expected - complete - recovered
    audit["missing_cells_to_resume"] = sorted(missing)
    write_json(directory / "run_manifest.json", audit)
    for rnd in (1, 2, 3):
        selected = sorted(p for p, r in missing if r == rnd)
        if not selected:
            continue
        summary = runner.run_experiment(report_root=report_root, output_dir=root / "sonnet" / f"fill-r{rnd}",
                                        profile=manifest["profile"], ablation="direct-report", rounds=1, round_index=rnd,
                                        pair_ids=selected, workers=16, allow_live=True, allow_full_live=True,
                                        predecessor_snapshot=str(source))
        print({"round": rnd, "completed": summary["method_cell_count"], "source": summary["artifact_root"]}, flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    if not args.allow_live:
        parser.error("explicit --allow-live is required")
    recover(args.source.resolve(), args.root.resolve())
