"""Verify the independent Luna route recheck without contacting the provider."""
import hashlib
import json
import zipfile
from datetime import datetime
from pathlib import Path


def verify(root):
    manifest = json.loads((root / "manifest.json").read_text())
    assert manifest["formal_result_eligible"] is False
    assert manifest["remaining_private_value_matches"] == 0
    with zipfile.ZipFile(root / "luna-route-diagnostics.zip") as archive:
        assert set(archive.namelist()) == set(manifest["members"])
        for name, item in manifest["members"].items():
            raw = archive.read(name)
            assert len(raw) == item["bytes"] and hashlib.sha256(raw).hexdigest() == item["sha256"]

        def read(name):
            return json.loads(archive.read(name))

        baseline = read("baseline/artifacts/record.json")
        probe = read("baseline/probe.json")
        assert baseline["status"] == "ok" and baseline["streaming"] is True
        assert baseline["configured_model"] == baseline["observed_model"] == "gpt-5.6-luna"
        assert baseline["usage"]["status"] == "completed"
        rows = []
        hashes = {}
        for name in archive.namelist():
            if not name.endswith("/request.body"):
                continue
            prefix = name.removesuffix("request.body")
            request = read(name)
            assert request["stream"] is True and request["model"] == "gpt-5.6-luna"
            assert request["max_output_tokens"] == 128000
            digest = hashlib.sha256(archive.read(name)).hexdigest()
            if name.startswith("checks/native-same-plain/"):
                metadata = read(prefix + "record.json")
                status = metadata["http_status"]
                hashes["native"] = digest
            else:
                metadata = read(prefix + "metadata.json")
                status = metadata["status_code"]
                if name.startswith("checks/plain-api/wire/"):
                    hashes["adapter"] = digest
                    original_request_hash = manifest["members"][name]["original_sha256"]
            if name.startswith("baseline/"):
                assert status == 200
                events = [json.loads(line[6:]) for line in archive.read(prefix + "response.body").splitlines()
                          if line.startswith(b"data: ") and line[6:] != b"[DONE]"]
                terminal, = [e["response"] for e in events if e.get("type") == "response.completed"]
                assert terminal["model"] == "gpt-5.6-luna" and terminal["status"] == "completed"
                assert terminal.get("incomplete_details") is None
                assert datetime.fromisoformat(probe["started_at"]).timestamp() <= terminal["created_at"] <= datetime.fromisoformat(probe["finished_at"]).timestamp()
                assert terminal["usage"]["input_tokens"] == baseline["usage"]["input_tokens"] == 4956
                assert terminal["usage"]["output_tokens"] == baseline["usage"]["output_tokens"] == 214
                assert terminal["usage"]["output_tokens_details"]["reasoning_tokens"] == 0
            else:
                assert status == 503
            rows.append({"request": name, "status": status})
        assert len(rows) == 5 and sum(r["status"] == 200 for r in rows) == 1
        assert hashes["adapter"] == hashes["native"]
        for case in ("plain-api", "plain-api-recheck", "runtime-tool", "native-same-plain"):
            record = read("checks/" + case + "/record.json")
            assert record["profile_fingerprint"] == probe["config_fingerprint"]
        runtime = read("checks/runtime-tool/record.json")
        assert runtime["status"] == "failed" and runtime["runtime_closed"]
        assert not runtime["outcome"]["schema_validation_failures"]
        assert len(runtime["outcome"]["attempts"]) == 1
        assert runtime["outcome"]["attempts"][0]["provider_error"] is True
        final_gate = json.loads((root / "final-gate-recheck.json").read_text())
        request = json.loads(final_gate["request_body_utf8"])
        assert request["stream"] is True and request["max_output_tokens"] == 128000
        assert request["model"] == "gpt-5.6-luna"
        for field in ("request", "response"):
            assert hashlib.sha256(final_gate[field + "_body_utf8"].encode()).hexdigest() == final_gate["source_sha256"][field]
        assert final_gate["source_sha256"]["request"] == original_request_hash
        assert final_gate["wire"]["status_code"] == 503
        assert final_gate["probe"]["profile_fingerprint"] == probe["config_fingerprint"]
        assert final_gate["probe"]["transport_retries"] == 0
        assert final_gate["probe"]["status"] == "failed"
        assert not final_gate["formal_result_eligible"]
        assert json.loads(final_gate["response_body_utf8"])["error"]["message"] == "Service temporarily unavailable"
        assert final_gate["privacy"]["known_private_matches"] == final_gate["privacy"]["credential_pattern_matches"] == 0
    return {"verified_members": len(manifest["members"]), "source_commit": probe["source_commit"],
            "baseline_status": baseline["status"], "baseline_seconds": probe["seconds"],
            "http_200": 1, "http_503": 4, "same_plain_payload_sha256": hashes["adapter"],
            "runtime_closed": True, "requests": rows,
            "final_gate_recheck_http_status": final_gate["wire"]["status_code"],
            "final_gate_original_request_sha256": original_request_hash,
            "final_gate_recheck_seconds": final_gate["probe"]["seconds"]}


if __name__ == "__main__":
    print(json.dumps(verify(Path(__file__).parent / "evidence/luna_route_20260907"), indent=2))
