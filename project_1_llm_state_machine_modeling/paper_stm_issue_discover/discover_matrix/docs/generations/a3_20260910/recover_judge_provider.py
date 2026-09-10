"""Resume a provider-interrupted judge using its exact successful stage results."""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import time
import uuid

from paper_stm_judge.cli import _code_commit
from paper_stm_judge.execution import ProcessStructuredRuntime
from paper_stm_judge.models import AdapterAudit, UnifiedJudgeInput
from paper_stm_judge.runner import judge_pair
from paper_stm_judge.schema import response_schema_hash
from paper_stm_method.orchestration.runner import _model_config_hash
from utils.artifact_io import write_json
from utils.structured_runtime import StructuredCallOutcome, StructuredContextBudget
from verify_sources import digest, read


class ResumeStages:
    def __init__(self, live, receipts):
        self.live, self.profile, self.config = live, live.profile, live.config
        self.saved, self.reused = {}, {}
        for receipt in receipts:
            if receipt["status"] != "success":
                continue
            paths = [Path(p) for p in receipt["artifact_paths"] if Path(p).name == "result.json"]
            successful = [(path, read(path)) for path in paths if read(path)["status"] == "success"]
            assert len(successful) == 1, "Each saved stage needs exactly one successful terminal result."
            path, result = successful[0]
            artifact_id = "/".join(path.parts[-5:-2])
            assert artifact_id not in self.saved
            self.saved[artifact_id] = receipt, path, result

    def call_many(self, calls):
        results = [self.call(**call) if call["artifact_id"] in self.saved else None for call in calls]
        pending = [index for index, result in enumerate(results) if result is None]
        if pending:
            completed = self.live.call_many(tuple(calls[index] for index in pending))
            for index, result in zip(pending, completed, strict=True):
                results[index] = result
        return tuple(results)

    def call(self, **call):
        if call["artifact_id"] not in self.saved:
            return self.live.call(**call)
        receipt, path, result = self.saved[call["artifact_id"]]
        actual_hash = "sha256:" + hashlib.sha256((call["system_prompt"] + "\n" + call["prompt"]).encode()).hexdigest()
        assert actual_hash == receipt["prompt_hash"], "Saved stage prompt changed."
        assert response_schema_hash(call["schema"]) == receipt["schema_hash"], "Saved stage schema changed."
        assert result["real_llm"] and result["model"] == self.config.model
        assert call["max_output_tokens"] == result["max_output_tokens"]
        response = call["schema"].model_validate(result["output"])
        self.reused[receipt["call_id"]] = {"receipt": receipt, "result_path": str(path), "sha256": digest(path)}
        return StructuredCallOutcome(
            kind=call["kind"], status="success", response=response, result=result,
            attempts=[json.loads(row["raw_attempt_json"]) for row in receipt["retries"]],
            usage=[json.loads(row["raw_usage_json"]) for row in receipt["usage"]],
            cost={"total_usd": receipt["cost_usd"], "eligible": receipt["cost_eligible"]}, real_llm=True,
            context_budget=StructuredContextBudget(
                mode="structured_llm", projection_version="judge-stage-resume.v1",
                prompt_characters=len(call["prompt"]), estimated_prompt_tokens=(len(call["prompt"]) + 3) // 4,
                provider_input_tokens=sum(row["input_tokens"] or 0 for row in receipt["usage"]),
                context_window_tokens=result["context_window_tokens"], max_output_tokens=result["max_output_tokens"],
                truncation_applied=False, projection_decision="Reused an exact committed successful judge stage.",
                reason="Same input, prompt and schema; no new provider call for this stage.",
                basis="Original stage result and original call receipt preserved by hash."),
            reason="Reused an exact successful real judge stage after provider interruption.",
            basis="Original call receipt replaces the reconstructed receipt in the final result.")


def recover(failure_path, destination):
    failure = read(failure_path)
    original_root = failure_path.parent.parent
    manifest = read(original_root / "run_manifest.json")
    assert failure["status"] == "failed"
    assert failure["call_receipts"][-1]["status"] == "failed"
    assert failure["call_receipts"][-1]["retries"][-1]["provider_error"], "Schema failures require diagnosis, not resampling."
    assert manifest["validity_readings"] == 2 and manifest["validity_aggregation"] == "arbitration"
    assert manifest["k_closure"] == "relation_first" and manifest["closure_profile"] == "full"
    assert manifest["validity_arbitration_trigger"] == "any"
    config_hash = _model_config_hash(manifest["model_profile"])
    assert config_hash == "sha256:05e7d948fd676e677f49a039ea75f0356f5aa005bbc2db89f5e72bf6ff4e446a"
    input_path, adapter_path = Path(failure["input_path"]), Path(failure["adapter_audit_path"])
    judge_input = UnifiedJudgeInput.model_validate(read(input_path))
    adapter = AdapterAudit.model_validate(read(adapter_path))
    assert digest(Path(adapter.source_path)) == adapter.source_hash
    code_commit = _code_commit()
    run_id = uuid.uuid4().hex
    output = destination / run_id
    output.mkdir(parents=True, exist_ok=False)
    recovery = {"schema": "a3.judge-provider-resume.v1", "run_id": run_id,
                "source_failure": str(failure_path), "failure_sha256": digest(failure_path),
                "source_manifest_sha256": digest(original_root / "run_manifest.json"),
                "input_sha256": digest(input_path), "adapter_sha256": digest(adapter_path),
                "judge_code_commit": code_commit, "workers": 8, "model_config_hash": config_hash,
                "reason": "Resume missing stages after provider interruption; preserve successful independent readings and failed usage."}
    write_json(output / "run_manifest.json", recovery)
    write_json(output / "inputs" / f"{failure['pair_id']}.json", judge_input.model_dump(mode="json"))
    write_json(output / "adapter_audits" / f"{failure['pair_id']}.json", adapter.model_dump(mode="json"))
    with ProcessStructuredRuntime(manifest["model_profile"], output / "llm", workers=8,
                                  transport_retries=manifest["transport_retries"], streaming=True) as live:
        runtime = ResumeStages(live, failure["call_receipts"])
        try:
            result = judge_pair(run_id=run_id, round_no=failure["round"], judge_input=judge_input,
                                adapter_audit=adapter, runtime=runtime, judge_code_commit=code_commit)
        except Exception as exc:
            write_json(output / "recovery_failure.json", {"error_type": type(exc).__name__, "message": str(exc),
                       "reused": runtime.reused,
                       "call_receipts": [r.model_dump(mode="json") for r in getattr(exc, "call_receipts", ())]})
            raise
    assert len(runtime.reused) == len(runtime.saved), "A successful prior stage was not consumed."
    payload = result.model_dump(mode="json")
    payload["call_receipts"] = [runtime.reused[r["call_id"]]["receipt"] if r["call_id"] in runtime.reused else r
                                for r in payload["call_receipts"]]
    payload["call_receipts"] = [r for r in failure["call_receipts"] if r["status"] != "success"] + payload["call_receipts"]
    type(result).model_validate(payload)
    recovery["reused_stages"] = runtime.reused
    recovery["prior_failed_calls"] = [r for r in failure["call_receipts"] if r["status"] != "success"]
    write_json(output / "run_manifest.json", recovery)
    write_json(output / "pairs" / f"{failure['pair_id']}.json", payload)
    print(json.dumps({"output": str(output), "reused_stages": len(runtime.reused), "status": payload["status"]}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--failure", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--wait-pid", type=int)
    parser.add_argument("--allow-live", action="store_true")
    args = parser.parse_args()
    if not args.allow_live:
        parser.error("explicit --allow-live is required")
    while args.wait_pid:
        status = subprocess.run(["ps", "-p", str(args.wait_pid), "-o", "stat="], capture_output=True, text=True).stdout.strip()
        if not status or status.startswith("Z"):
            break
        time.sleep(2)
    recover(args.failure.resolve(), args.output_dir.resolve())
