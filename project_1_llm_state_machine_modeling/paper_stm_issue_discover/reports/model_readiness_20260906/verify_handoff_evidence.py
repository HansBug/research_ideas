"""Recompute the final E1 compatibility snapshot offline, including provider failures."""
import hashlib
import json
import math
import zipfile
from collections import Counter
from pathlib import Path

from verify_stream_evidence import verify as verify_previous


def verify(root):
    previous = verify_previous(root / "stream_20260907")
    directory = root / "handoff_20260907"
    manifest = json.loads((directory / "manifest.json").read_text())
    assert manifest["formal_result_eligible"] is False
    assert manifest["remaining_private_value_matches"] == 0
    with zipfile.ZipFile(directory / "handoff-diagnostics.zip") as archive:
        assert set(archive.namelist()) == set(manifest["members"])
        for name, expected in manifest["members"].items():
            raw = archive.read(name)
            assert hashlib.sha256(raw).hexdigest() == expected["sha256"], name
            assert len(raw) == expected["bytes"], name
            assert "private" not in Path(name).parts and not Path(name).name.startswith("pr.")

        def read(name):
            return json.loads(archive.read(name))

        profiles = read("ready/final-profiles.json")
        assert profiles["registry_profiles"] == 23
        assert profiles["config_permissions"] == "0o600"
        configs = profiles["profiles"]
        prefix = "cells/e1-muse30b-schema-order-final-stream/"
        probe = read(prefix + "probe.json")
        assert probe["streaming"] and probe["rounds"] == 1
        assert set(probe["pairs"]) == {"0019", "0029", "0049"}
        assert probe["candidate_judge_calls"] == 0 and probe["run_output_override"] is None
        assert probe["output_budget_mode"] == "remaining_context"
        assert probe["config_fingerprint"] == configs["e1-muse30b"]["fingerprint"]
        audit = read(prefix + "summary-audit.json")
        run_id = audit["run_id"]
        run = prefix + "artifacts/" + run_id + "/"
        summary = read(run + "summary.json")
        cells = []
        for pair in sorted(probe["pairs"]):
            cell = read(run + "method/" + pair + "/round-1.json")
            status = summary["per_pair"][pair]
            assert cell["eligible"] and status["status"] == "completed"
            assert not cell["errors"] and status["errors"] == status["audit_errors"] == 0
            assert len(cell["stage_receipts"]) == 8
            assert all(s["status"] == "completed" for s in cell["stage_receipts"])
            assert all(not s["context_budget"]["truncation_applied"] for s in cell["stage_receipts"])
            assert len(cell["llm_calls"]) == 5
            assert all(s["status"] == "success" for s in cell["llm_calls"])
            cells.append({"profile": "e1-muse30b", "pair": pair, "status": status["status"],
                          "eligible": cell["eligible"], "errors": 0, "audit_errors": 0,
                          "stages": [s["status"] for s in cell["stage_receipts"]],
                          "schema_repairs": sum(len(s["schema_validation_failures"]) for s in cell["llm_calls"])})
        requests = [n for n in archive.namelist()
                    if n.startswith(prefix + "call_metadata/wire/") and n.endswith("/request.body")]
        assert len(requests) == len(audit["calls"]) == 16
        assert len({c["model_call_id"] for c in audit["calls"]}) == 16
        assert audit["counts"]["compact_count"] == audit["counts"]["unmapped_wire_requests"] == 0
        for name in requests:
            request = read(name)
            assert request["stream"] is True
            assert request["model"] == configs["e1-muse30b"]["model"]
            assert not {"max_tokens", "max_completion_tokens", "max_output_tokens"} & request.keys()
            assert read(name.removesuffix("request.body") + "metadata.json")["status_code"] == 200
        for call in audit["calls"]:
            assert call["normalized_usage"] and call["tool_call_count"] == 1
            assert all(w["provider_finish_reasons"] == ["tool_calls"] for w in call["wire"])
        assert audit["counts"]["max_input_tokens"] == max(c["normalized_usage"]["input_tokens"] for c in audit["calls"])
        assert audit["counts"]["max_output_tokens"] == max(c["normalized_usage"]["output_tokens"] for c in audit["calls"])

        loads = []
        for case, target, count in (("long16k", 16000, 32), ("native90", math.floor(.9 * 131072), 2)):
            source = "serving/muse/schema-order-final/" + case + "/"
            rows = [json.loads(line) for line in archive.read(source + "requests.jsonl").splitlines() if line]
            measured = [r for r in rows if not r["warmup"]]
            result, = read(source + "summary.json")
            assert len(measured) == result["requests"] == result["eligible"] == count
            assert all(r["eligible"] and r["payload"]["stream"] for r in measured)
            assert all(not {"max_tokens", "max_completion_tokens"} & r["payload"].keys() for r in rows)
            minimum = min(r["usage"]["prompt_tokens"] for r in measured)
            assert minimum == result["input_tokens_min"] and minimum >= target
            latency = sorted(r["seconds"] for r in measured)
            assert result["latency_p95"] == latency[math.ceil(len(latency) * .95) - 1]
            assert result["concurrency"] == (16 if case == "long16k" else 1)
            loads.append({"model": "muse", "check": case, "input_tokens_min": minimum,
                          "requests": count, "eligible": count, "p95_seconds": result["latency_p95"]})

        baselines = []
        for row in read("ready/baseline-audit.json"):
            source = "ready/" + row["profile"] + "/" + row["variant"] + "/"
            actual = read(source + "artifacts/record.json")
            assert actual["status"] == row["status"] and actual["usage"] == row["usage"]
            assert row["probe"]["config_fingerprint"] == configs[row["profile"]]["fingerprint"]
            for name in archive.namelist():
                if not name.startswith(source + "call_metadata/wire/") or not name.endswith("/request.body"):
                    continue
                request = read(name)
                assert request["stream"] is True and request["model"] == configs[row["profile"]]["model"]
                caps = [request[k] for k in ("max_tokens", "max_completion_tokens", "max_output_tokens") if k in request]
                expected = [] if configs[row["profile"]]["output_budget_mode"] == "remaining_context" else [configs[row["profile"]]["max_output_tokens"]]
                assert caps == expected
            if row["status"] == "ok":
                assert actual["observed_model"] == actual["configured_model"]
                assert actual["usage"]["status"] == "completed"
                assert all(w["status"] == 200 and w["usage"] and w["finish_reasons"] for w in row["wire"])
            else:
                assert row["profile"] == "gpt-5.6-luna"
                assert actual["failure_class"] == "transport_exhausted"
                assert all(w["status"] == 503 for w in row["wire"])
            baselines.append({"profile": row["profile"], "variant": row["variant"], "status": row["status"],
                              "seconds": row["probe"]["seconds"], "usage": row["usage"],
                              "http": [w["status"] for w in row["wire"]]})

        reuse = read("ready/luna-method-reuse.json")
        assert reuse["historical_run_unchanged"] and not reuse["historical_compact_count"]
        assert all(v for k, v in reuse["field_equalities"].items() if k != "context_window_tokens")
        assert reuse["pair_status"]["status"] == "completed"
        with zipfile.ZipFile(root / "stream_20260907/stream-diagnostics.zip") as old:
            for profile, variant in (("claude-sonnet-5", "model-max-stream"),
                                     ("e1-qwen38-27b", "model-max-remaining-stream-registered")):
                prior = json.loads(old.read("cells/" + profile + "-" + variant + "/summary-audit.json"))
                assert prior["probe"]["config_fingerprint"] == configs[profile]["fingerprint"]
                for pair, cell in prior["pairs"].items():
                    assert all(s["status"] == "success" for s in cell["llm_stages"])
                    for stage in cell["stage_receipts"]:
                        degraded = profile == "claude-sonnet-5" and pair == "0029" and stage["name"] in {"d_adjudication", "validate_d"}
                        assert stage["status"] == ("completed_with_diagnostics" if degraded else "completed")
            sonnet = json.loads(old.read("cells/claude-sonnet-5-model-max-stream/summary-audit.json"))
            thinking = [u["output_tokens_details"]["thinking_tokens"] for c in sonnet["calls"]
                        for w in c["wire"] for u in w["raw_usage_events"] if "output_tokens_details" in u]
            assert len(thinking) == 24 and set(thinking) == {0}
        correction = read("ready/sonnet-reasoning-usage-correction.json")
        assert len(correction["rows"]) == 24 and all(r["thinking_tokens"] == 0 for r in correction["rows"])

    return {"verified_members": len(manifest["members"]), "final_muse_run": run_id,
            "final_muse_source_commit": probe["source_commit"], "final_muse_seconds": probe["seconds"],
            "final_muse_counts": audit["counts"], "method_cells": cells + [c for c in previous["method_cells"]
                if c["profile"] in {"claude-sonnet-5", "e1-qwen38-27b"}],
            "loads": loads + [r for r in previous["loads"] if r["model"] == "qwen38"],
            "baseline_attempts": baselines,
            "baseline_http_counts": dict(Counter(str(s) for b in baselines for s in b["http"])),
            "luna_historical_method": reuse["run_id"], "sonnet_gateway_thinking_tokens": 0}


if __name__ == "__main__":
    print(json.dumps(verify(Path(__file__).parent / "evidence"), indent=2))
