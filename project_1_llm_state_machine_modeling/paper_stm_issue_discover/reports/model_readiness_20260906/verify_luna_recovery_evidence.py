"""Verify the final Luna connection and full method receipts without a provider."""
import hashlib
import json
import zipfile
from pathlib import Path


def verify(directory):
    manifest = json.loads((directory / "manifest.json").read_text())
    assert manifest["formal_result_eligible"] is False
    assert manifest["remaining_private_value_matches"] == 0
    with zipfile.ZipFile(directory / "luna-recovery-diagnostics.zip") as archive:
        names = archive.namelist()
        assert set(names) == set(manifest["members"])
        for name, expected in manifest["members"].items():
            data = archive.read(name)
            assert len(data) == expected["bytes"]
            assert hashlib.sha256(data).hexdigest() == expected["sha256"]
            assert not set(Path(name).parts) & {"private", "__pycache__"}
            assert Path(name).name not in {"connection.json", "llmconfig.yml", ".llmconfig.yml", "original.llmconfig.yml"}

        def read(name):
            return json.loads(archive.read(name))

        comparison = read("configuration/config-comparison.json")
        profiles = comparison["profiles"]
        config = profiles["gpt-5.6-luna"]
        assert comparison["changed_luna_fields"] == ["api_key", "base_url"]
        assert comparison["registry_profiles"] == 23 and comparison["config_permissions"] == "0o600"
        assert len(comparison["other_profile_equalities"]) == 22
        assert all(comparison["other_profile_equalities"].values())
        with zipfile.ZipFile(directory.parent / "handoff_20260907/handoff-diagnostics.zip") as previous:
            prior = json.loads(previous.read("ready/final-profiles.json"))["profiles"]
        for profile in ("claude-sonnet-5", "e1-qwen38-27b", "e1-muse30b"):
            assert profiles[profile] == prior[profile]
        assert config["model"] == "gpt-5.6-luna" and config["adapter"] == "openai-responses"
        assert config["context_window_tokens"] == 1050000 and config["max_output_tokens"] == 128000
        assert config["fingerprint"] != prior["gpt-5.6-luna"]["fingerprint"]
        probes = {kind: read(kind + "/" + filename) for kind, filename in
                  (("plain", "record.json"), ("runtime", "record.json"),
                   ("baseline", "probe.json"), ("method", "probe.json"))}
        for kind, probe in probes.items():
            assert probe.get("profile_fingerprint", probe.get("config_fingerprint")) == config["fingerprint"]
            assert probe.get("stream", probe.get("streaming")) is True
            assert probe["transport_retries"] == 0 and probe.get("run_output_override") is None
            assert probe["formal_result_eligible"] is False
            expected_source = ("5cbf1442d6df8bbd3a87ce8d05cc789b5d6a9022" if kind == "method"
                               else "672069f854102d3a2b1b1d07cff9c278eba933a1")
            assert probe["source_commit"] == expected_source

        rows = []
        for name in sorted(n for n in names if n.endswith("/request.body")
                           and n.split("/", 1)[0] in probes):
            prefix = name.removesuffix("request.body")
            request, metadata = read(name), read(prefix + "metadata.json")
            assert request["stream"] is True and request["max_output_tokens"] == 128000
            assert request["model"] == "gpt-5.6-luna" and metadata["status_code"] == 200
            events = [json.loads(line[6:]) for line in archive.read(prefix + "response.body").splitlines()
                      if line.startswith(b"data: ") and line[6:] != b"[DONE]"]
            terminal, = [e["response"] for e in events if e.get("type") == "response.completed"]
            assert terminal["status"] == "completed" and terminal["model"] == "gpt-5.6-luna"
            assert terminal.get("incomplete_details") is None
            assert not any(e.get("type") in {"error", "response.failed", "response.incomplete"} for e in events)
            usage = terminal["usage"]
            assert usage["total_tokens"] == usage["input_tokens"] + usage["output_tokens"]
            kind = name.split("/", 1)[0]
            if kind in {"runtime", "method"}:
                assert request["reasoning"] == {"effort": "none"}
                assert request["tool_choice"] == "required"
            else:
                assert "reasoning" not in request
            assert not {"temperature", "top_p"} & request.keys()
            if kind != "plain":
                calls = [item for item in terminal["output"] if item["type"] == "function_call"]
                assert calls and all(isinstance(json.loads(call["arguments"]), dict) for call in calls)
            rows.append({"kind": kind, "request": name, "model_call_id": metadata.get("model_call_id"),
                         "usage": usage, "finish": "response.completed", "incomplete_details": None,
                         "reasoning": request.get("reasoning"), "max_output_tokens": 128000,
                         "seconds": metadata.get("body_completed_seconds", metadata.get("seconds")),
                         "first_sse_seconds": metadata.get("first_sse_seconds")})

        assert probes["plain"]["status"] == "completed"
        runtime = probes["runtime"]
        assert runtime["status"] == "success" and runtime["typed_response"] and runtime["runtime_closed"]
        assert not runtime["outcome"]["schema_validation_failures"]
        assert len(runtime["outcome"]["attempts"]) == 1
        baseline = read("baseline/artifacts/record.json")
        assert baseline["status"] == "ok" and baseline["streaming"] is True
        assert baseline["configured_model"] == baseline["observed_model"] == config["model"]
        baseline_wire, = [r for r in rows if r["kind"] == "baseline"]
        assert baseline["usage"]["input_tokens"] == baseline_wire["usage"]["input_tokens"] == 5118
        assert baseline["usage"]["output_tokens"] == baseline_wire["usage"]["output_tokens"] == 183

        probe = probes["method"]
        assert probe["pairs"] == ["0001"] and probe["rounds"] == probe["workers"] == 1
        assert probe["candidate_judge_calls"] == 0
        summary_name, = [n for n in names if n.startswith("method/artifacts/") and n.endswith("/summary.json")]
        run = summary_name.removesuffix("summary.json")
        summary, cell = read(summary_name), read(run + "method/0001/round-1.json")
        status = summary["per_pair"]["0001"]
        assert cell["eligible"] and set(cell["eligibility_reasons"]) == {
            "real_contract_output", "at_least_one_completed_grounding_lens",
            "auditable_semantic_result", "method_receipt_complete"}
        assert cell["source_provenance"]["source_commit"] == probe["source_commit"]
        assert cell["source_provenance"]["source_dirty"] is False
        assert status["status"] == "completed" and status["errors"] == status["audit_errors"] == 0
        assert not cell["errors"] and len(cell["stage_receipts"]) == 8
        assert all(s["status"] == "completed" for s in cell["stage_receipts"])
        assert all(not s["context_budget"]["truncation_applied"] for s in cell["stage_receipts"])
        assert all(s["status"] == "success" for s in cell["llm_calls"])
        results = [read(n) for n in names if n.startswith(run + "llm/method/") and n.endswith("/result.json")]
        assert len(results) == len(cell["llm_calls"])
        assert all(r["status"] == "success" and not r["compact_count"] for r in results)
        method_rows = [r for r in rows if r["kind"] == "method"]
        audit = read("method/summary-audit.json")
        assert len(method_rows) == len(audit["calls"]) == audit["counts"]["responses"]
        assert not audit["counts"]["unmapped_wire_requests"]
        assert {r["model_call_id"] for r in method_rows} == {c["model_call_id"] for c in audit["calls"]}
        for call in audit["calls"]:
            wire, = [r for r in method_rows if r["model_call_id"] == call["model_call_id"]]
            for key in ("input_tokens", "output_tokens", "total_tokens"):
                assert call["normalized_usage"][key] == wire["usage"][key]
            assert wire["usage"]["output_tokens_details"]["reasoning_tokens"] == 0
            assert wire["usage"]["input_tokens"] + wire["max_output_tokens"] <= config["context_window_tokens"]
            wire["stage_path"] = call["stage_path"]
        d_stage, = [s for s in cell["stage_receipts"] if s["stage_name"] == "d_adjudication"]
        assert len(d_stage["diagnostics"]) == 1
        assert d_stage["diagnostics"][0]["status"] == "completed"
        assert d_stage["diagnostics"][0]["exceeds_budget"] is False
        assert len(cell["predicate_execution_receipts"]) == 5
        assert len(rows) == len(method_rows) + 3
        prior_probe = read("method-prior/probe.json")
        assert prior_probe["source_commit"] == probes["baseline"]["source_commit"]
        assert prior_probe["config_fingerprint"] == config["fingerprint"]
        prior_audit = read("method-prior/summary-audit.json")
        assert prior_audit["counts"]["calls"] == 8 and prior_audit["counts"]["missing_usage"] == 1
        prior_finishes = []
        for name in names:
            if not (name.startswith("method-prior/") and name.endswith("/response.body")):
                continue
            events = [json.loads(line[6:]) for line in archive.read(name).splitlines()
                      if line.startswith(b"data: ") and line[6:] != b"[DONE]"]
            terminal, = [e for e in events if e.get("type") in {"response.failed", "response.completed"}]
            prior_finishes.append(terminal["type"])
            if terminal["type"] == "response.failed":
                assert terminal["response"]["error"]["code"] == "server_error"
                assert manifest["members"][name]["original_sha256"] == "68bb863b3856e2fdcf10bea2e411c202e501a6fa535c01a37eb8c0ae6a515e4b"
        assert prior_finishes.count("response.failed") == 1
        assert prior_finishes.count("response.completed") == 7
        replay = read("configuration/replayed-provider-failure.json")
        assert replay["status"] == "provider_failure_caught" and replay["http_status"] == 200
        assert replay["network_calls"] == 0 and replay["sdk_calls"] == 1 and replay["response_closed"]
        rejected = read("method-launch-rejected/probe.json")
        assert rejected["exit_code"] == 1
        assert not any(n.startswith("method-launch-rejected/call_metadata/") for n in names)
        assert b"clean tracked worktree" in archive.read("method-launch-rejected/process.log")
        checks = read("configuration/post-guard-checks.json")
        assert checks["source_commit"] == probe["source_commit"]
        assert checks["frozen_method_baseline_pyfcstm_diff_empty"]
        assert checks["regression"]["passed"] == 259 and checks["regression"]["skipped"] == 1
        assert checks["regression"]["failures"] == checks["regression"]["errors"] == 0
        report = directory.parent.parent / "2026-09-07-11-10-00-luna-connection-recovery.md"
        if report.exists():
            markdown = report.read_text()
            for row in method_rows:
                usage = row["usage"]
                table_row = (f'| `{row["model_call_id"]}` | {row["stage_path"].removesuffix("/cell-attempt-1")} | '
                             f'{usage["input_tokens"]} | {usage["output_tokens"]} | 0 | '
                             f'{row["first_sse_seconds"]:.2f} | {row["seconds"]:.2f} |')
                assert table_row in markdown, row["model_call_id"]
    return {"verified_members": len(manifest["members"]), "run_id": run.split("/")[-2],
            "source_commit": probe["source_commit"], "method_seconds": probe["seconds"],
            "method_calls": len(method_rows), "llm_stages": len(cell["llm_calls"]),
            "prior_method": {"run_id": prior_audit["run_id"], "completed_responses": 7,
                             "failed_responses": 1, "missing_usage": 1,
                             "frozen_audit_omitted_provider_failure": True},
            "stage_receipts": [{"name": s["stage_name"], "status": s["status"],
                                "diagnostics": len(s.get("diagnostics") or [])} for s in cell["stage_receipts"]],
            "schema_repairs": sum(len(s["schema_validation_failures"]) for s in cell["llm_calls"]),
            "eligible": cell["eligible"], "errors": status["errors"], "audit_errors": status["audit_errors"],
            "method_max_input": max(r["usage"]["input_tokens"] for r in method_rows),
            "method_max_output": max(r["usage"]["output_tokens"] for r in method_rows),
            "requests": rows}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify(Path(__file__).parent / "evidence/luna_recovery_20260907")
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k != "requests"}, indent=2))
