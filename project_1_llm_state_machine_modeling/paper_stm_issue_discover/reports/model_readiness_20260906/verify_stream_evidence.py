"""Verify the E1 streaming evidence archive offline; never contact a provider."""
import hashlib
import json
import math
import zipfile
from collections import Counter
from pathlib import Path


def verify(root):
    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest["formal_result_eligible"] is False
    assert manifest["remaining_private_value_matches"] == 0
    cells = []
    loads = []
    models = []
    with zipfile.ZipFile(root / "stream-diagnostics.zip") as archive:
        assert set(archive.namelist()) == set(manifest["members"])
        for name, expected in manifest["members"].items():
            data = archive.read(name)
            assert hashlib.sha256(data).hexdigest() == expected["sha256"], name
            assert len(data) == expected["bytes"], name
            assert "private" not in Path(name).parts
            assert not name.endswith("-connection.json")

        def read(name):
            return json.loads(archive.read(name))

        selected = {
            "gateway-b-gemini-3.8-native": "model-max-stream",
            "claude-sonnet-5": "model-max-stream",
            "claude-haiku-4-5": "model-max-stream",
            "e1-qwen38-27b": "model-max-remaining-stream-registered",
            "e1-muse30b": "model-max-remaining-stream",
        }
        for profile, variant in selected.items():
            prefix = "cells/" + profile + "-" + variant + "/"
            probe = read(prefix + "probe.json")
            assert probe["streaming"] is True and probe["rounds"] == 1
            assert probe["candidate_judge_calls"] == 0
            assert set(probe["pairs"]) == {"0029", "0019", "0049"}
            assert probe["run_output_override"] is None
            requests = 0
            d_schemas = 0
            for name in archive.namelist():
                if not name.startswith(prefix + "call_metadata/wire/") or not name.endswith("/request.body"):
                    continue
                request = read(name)
                requests += 1
                assert request.get("stream") is True or "generationConfig" in request
                caps = [request[key] for key in ("max_tokens", "max_completion_tokens", "max_output_tokens") if key in request]
                if "maxOutputTokens" in request.get("generationConfig", {}):
                    caps.append(request["generationConfig"]["maxOutputTokens"])
                if probe.get("output_budget_mode", "profile") == "remaining_context":
                    assert not caps, name
                else:
                    assert caps == [probe["profile_max_output_tokens"]], name
                for tool in request.get("tools", []):
                    for function in tool.get("functionDeclarations", [tool.get("function", tool)]):
                        if function.get("name") == "DAdjudicationResponse":
                            schema = function.get("parameters", function.get("input_schema", {}))
                            assert {"reason", "basis"} <= set(schema["required"]), name
                            assert schema["properties"]["decisions"]["type"].lower() == "array", name
                            d_schemas += 1
            assert d_schemas > 0, profile
            summaries = [n for n in archive.namelist() if n.startswith(prefix + "artifacts/")
                         and n.endswith("/summary.json")]
            assert len(summaries) == 1
            summary = read(summaries[0])
            run = summaries[0].removesuffix("summary.json")
            for pair in ("0029", "0019", "0049"):
                cell = read(run + "method/" + pair + "/round-1.json")
                status = summary["per_pair"][pair]
                assert cell["eligible"] == bool(status["eligible_method_cells"])
                assert len(cell["errors"]) == status["errors"]
                assert cell["run_id"] == summary["run_id"]
                assert len(cell["stage_receipts"]) == 8
                assert all(r["context_budget"]["truncation_applied"] is False for r in cell["stage_receipts"])
                cells.append({"profile": profile, "pair": pair, "status": status["status"],
                              "eligible": cell["eligible"], "errors": status["errors"],
                              "audit_errors": status["audit_errors"]})
            audit = read(prefix + "summary-audit.json")
            calls = audit["calls"]
            assert requests == len(calls) == audit["counts"]["wire_requests"]
            assert len({c["model_call_id"] for c in calls}) == len(calls)
            assert audit["counts"]["unmapped_wire_requests"] == 0
            assert all(c.get("pair") in probe["pairs"] for c in calls)
            assert sum(not c["normalized_usage"] for c in calls) == audit["counts"]["missing_usage"]
            finishes = Counter(f for c in calls for w in c["wire"] for f in w["provider_finish_reasons"])
            assert dict(finishes) == audit["counts"]["finish_reasons"]
            models.append({"profile": profile, "run_id": summary["run_id"],
                           "source_commit": probe["source_commit"], "seconds": probe["seconds"],
                           "calls": len(calls), "provider_finishes": dict(finishes),
                           "max_input_tokens": max(c["normalized_usage"].get("input_tokens", 0) for c in calls),
                           "max_output_tokens": max(c["normalized_usage"].get("output_tokens", 0) for c in calls),
                           "d_schema_transmitted_count": d_schemas,
                           "schema_repairs": sum(s["schema_failures"] for p in audit["pairs"].values()
                                                 for s in p["llm_stages"])})

        for model, checks in (("qwen38", ("long16k", "native90", "extended90")),
                              ("muse", ("long16k", "native90"))):
            for check in checks:
                prefix = "serving/" + model + "/model-max/" + check + "/"
                rows = [json.loads(line) for line in archive.read(prefix + "requests.jsonl").splitlines() if line]
                observed = [r for r in rows if not r["warmup"]]
                summary, = read(prefix + "summary.json")
                assert summary["requests"] == len(observed)
                assert summary["eligible"] == sum(r["eligible"] for r in observed)
                assert summary["truncated"] == sum(r.get("finish_reason") == "length" for r in observed)
                assert summary["transport_failed"] == sum(r["status"] == "failed" for r in observed)
                assert all(r["payload"]["stream"] is True for r in rows)
                assert all(not {"max_tokens", "max_completion_tokens"} & r["payload"].keys() for r in rows)
                latency = sorted(r["seconds"] for r in observed)
                assert summary["latency_p95"] == latency[math.ceil(len(latency) * .95) - 1]
                minimum = min(r.get("usage", {}).get("prompt_tokens", 0) for r in observed)
                assert summary["input_tokens_min"] == minimum
                target = 16000 if check == "long16k" else math.floor(.9 * (
                    1_000_000 if check == "extended90" else 262144 if model == "qwen38" else 131072))
                assert minimum >= target, (model, check, minimum, target)
                assert summary["concurrency"] == (16 if check == "long16k" else 1)
                loads.append({"model": model, "check": check, "requests": len(observed),
                              "eligible": summary["eligible"], "input_tokens_min": minimum,
                              "p95_seconds": summary["latency_p95"]})

        for model in ("qwen38-failed-0001", "muse-large-0029-model-max"):
            comparisons = read("comparisons/" + model + "/comparison.json")
            assert set(comparisons) == {"adapter-tunnel", "native-tunnel", "native-loopback"}
            hashes = {rows[0]["request_sha256_verified"] for rows in comparisons.values()}
            assert len(hashes) == 1
            assert all(rows[0]["same_as_frozen_request"] for rows in comparisons.values())
    return {"verified_members": len(manifest["members"]), "models": models,
            "method_cells": cells, "loads": loads}


if __name__ == "__main__":
    print(json.dumps(verify(Path(__file__).parent / "evidence/stream_20260907"), indent=2))
