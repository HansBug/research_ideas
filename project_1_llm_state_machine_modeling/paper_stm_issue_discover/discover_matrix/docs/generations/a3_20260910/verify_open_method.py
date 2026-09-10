"""Verify and summarize the isolated Qwen/Muse A3 method-only archive."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(root, models):
    controls = read(root / "full_source_manifest.json")
    result = {"schema": "a3.open-method-only.v1", "judge_status": "not_run", "models": {}}
    assert not list(root.glob("**/judge/run_manifest.json"))
    for model in models:
        expected = {(c["pair"], c["round"]): c for c in controls[model]}
        assert len(expected) == 162
        seen, rows, counts, usage = set(), [], Counter(), Counter()
        usage_ids = set()
        recovery_path = root / model / "schema-recovered/run_manifest.json"
        recovery = read(recovery_path) if recovery_path.exists() else None
        for manifest in sorted(root.glob(f"{model}/*/*/run_manifest.json")):
            metadata = read(manifest)
            assert metadata["ablation"] == "direct-report"
            assert metadata["prompt_schema_hash"] == "sha256:8819378f31fd7f291e73324d1087e33e6a392103756bcab92093bfe50d889b9d"
            assert metadata["workers"] <= 16
            assert metadata["streaming"] is True
            assert metadata["profile"] == {"qwen": "e1-qwen38-27b", "muse": "e1-muse30b"}[model]
            for path in sorted(manifest.parent.glob("method/*/round-*.json")):
                cell = read(path)
                if recovery and (path.parent.name, path.name) == (Path(recovery["source"]).parent.name, Path(recovery["source"]).name):
                    assert not cell["eligible"] and "sha256:" + digest(path) == recovery["source_hash"]
                    original = cell
                    path = recovery_path.parent / "method" / cell["pair_id"] / f"round-{cell['round']}.json"
                    cell = read(path)
                    arguments = original["llm_calls"][0]["result"]["tool_calls"][0]["arguments"]
                    fragments = arguments["issues"]
                    merged = [{**fragments[i], **fragments[i + 1]} for i in range(0, len(fragments), 2)]
                    assert cell["model_output"] == {**arguments, "issues": merged}
                    assert cell["llm_calls"][0]["usage"] == original["llm_calls"][0]["usage"]
                    counts["recovered_cells"] += 1
                key = cell["pair_id"], cell["round"]
                assert key in expected and key not in seen, key
                seen.add(key)
                assert cell["input_hashes"] == expected[key]["input_hashes"]
                assert cell["eligible"] and cell["status"] in ("completed", "completed_with_diagnostics"), (key, cell["errors"])
                assert cell["ablation"] == "direct-report" and len(cell["llm_calls"]) == 1
                assert cell["stage_outputs"]["execute_batch"]["new_candidate_count"] == 0
                generated, records = cell["model_output"]["issues"], cell["evidence_records"]
                reports = cell["report_issue_clusters"]
                assert len(generated) == len(records)
                assert len({r["issue_id"] for r in reports}) == len(reports)
                assert {r["final_report_id"] for r in records if r["final_report_id"]} == {r["issue_id"] for r in reports}
                for record in records:
                    original = generated[record["generation_index"]]
                    assert record["d_level"] is None
                    assert all(record[k] == original[k] for k in ("expected", "observed", "reason", "basis"))
                    counts["disposition_" + record["publication_status"]] += 1
                    counts["verdict_" + record.get("receipt", {}).get("verdict", "missing")] += 1
                    counts["witness_" + record["witness_level"]] += 1
                call = cell["llm_calls"][0]
                assert not call["context_budget"]["truncation_applied"]
                usage["logical_generation_stages"] += 1
                usage["provider_model_calls"] += call["result"].get("model_calls_used", 0)
                usage["schema_validation_failures"] += len(call["schema_validation_failures"])
                usage["unpriced_usage_rows"] += call["cost"].get("unpriced_usage_count", 0)
                for item in call["usage"]:
                    assert item["model"] == {"qwen": "qwen3.8-27b", "muse": "muse-glimmer-30b"}[model]
                    assert item["model_call_id"] not in usage_ids
                    usage_ids.add(item["model_call_id"])
                    assert item["output_budget"]["source"] == "provider_remaining_context"
                    assert item["output_budget"]["request_max_output_tokens"] is None
                    usage["status_" + item["status"]] += 1
                    usage["finish_" + str((item.get("provider_response") or {}).get("finish_reason"))] += 1
                    for name in ("input_tokens", "output_tokens", "reasoning_tokens"):
                        usage[name] += item.get(name) or 0
                    usage["missing_token_usage_rows"] += item.get("input_tokens") is None or item.get("output_tokens") is None
                    usage["missing_reasoning_usage_rows"] += item.get("reasoning_tokens") is None
                counts.update(cells=1, generated=len(generated), published=len(reports), errors=len(cell["errors"]))
                rows.append({"pair": key[0], "round": key[1], "source": str(path.relative_to(root)),
                             "sha256": digest(path), "status": cell["status"], "eligible": cell["eligible"],
                             "generated": len(generated), "published": len(reports), "errors": cell["errors"],
                             "generation_mapping": cell["stage_outputs"]["publish"]["mapping"]})
        assert seen == set(expected), (model, "missing", sorted(set(expected) - seen))
        result["models"][model] = {"counts": dict(counts), "usage": dict(usage),
                                  "rounds": {str(r): {"cells": sum(c["round"] == r for c in rows),
                                                     "generated": sum(c["generated"] for c in rows if c["round"] == r),
                                                     "published": sum(c["published"] for c in rows if c["round"] == r)} for r in (1, 2, 3)},
                                  "cells": sorted(rows, key=lambda c: (c["pair"], c["round"]))}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--model", action="append", choices=("qwen", "muse"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--archive", type=Path, help="Compare public results and every indexed raw hash.")
    args = parser.parse_args()
    result = verify(args.root, args.model or ("qwen", "muse"))
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if args.archive:
        assert result == read(args.archive / "method-results.json")
        for entry in read(args.archive / "archive_manifest.json")["files"]:
            path = args.archive / entry["path"]
            assert path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"], path
        for entry in read(args.archive / "raw_index.json")["files"]:
            path = args.root / entry["path"]
            assert path.stat().st_size == entry["bytes"] and digest(path) == entry["sha256"], path
    print(json.dumps({m: {k: v for k, v in d.items() if k != "cells"} for m, d in result["models"].items()}, ensure_ascii=False))
