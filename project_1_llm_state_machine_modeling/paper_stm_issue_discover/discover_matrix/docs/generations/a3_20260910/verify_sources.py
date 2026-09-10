"""Provider-free verification of immutable Full controls and A3 input identity."""

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

PAPER = Path(__file__).resolve().parents[4]


def read(path):
    return json.loads(path.read_text())


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def checked(path, expected):
    actual = digest(path)
    assert actual.removeprefix("sha256:") == expected.removeprefix("sha256:"), str(path)
    return actual


def verify():
    from paper_stm_method.inputs import load_pair

    spec = importlib.util.spec_from_file_location("a1_arithmetic", PAPER / "discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py")
    arithmetic = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(arithmetic)
    archive = PAPER / "final_results/e2_20260907"
    sonnet = read(archive / "sonnet/cells.json")
    luna = read(archive / "luna_history.json")
    items = read(PAPER / "discover_matrix/ledger_v2/ledger.json")["items"]
    assert len(items) == 145
    pairs = sorted(sonnet["pair_clusters"])
    assert len(pairs) == 54
    inputs = {p: load_pair(PAPER / "pipeline/representation/reports/llms_emp_r45_java_60/pairs" / p) for p in pairs}
    result = {"schema": "a3.full-source-verification.v1", "models": {}}
    for model in ("sonnet", "luna"):
        cells = [c for c in sonnet["cells"] if c["arm"] == "ours"] if model == "sonnet" else luna["verification"]["arms"]["ours"]["cells"]
        manifests, reports = [], []
        for cell in cells:
            pair_id, rnd = cell.get("pair", cell.get("pair_id")), cell["round"]
            if model == "sonnet":
                method_path = archive / "raw" / cell["source"]
                judge_path = archive / "raw" / cell["judge_source"]
                checked(judge_path, cell["judge_sha256"])
                checked(method_path, cell["sha256"])
            else:
                judge_path = PAPER / cell["source"]
                checked(judge_path, cell["sha256"])
                raw = PAPER / "final_results/v61_source_divergence_vs_x1v2_baseline/raw"
                folder = "v61_current_fill0045/method" if (pair_id, rnd) == ("0045", 1) else "v61_current/method/method"
                method_path = raw / folder / pair_id / f"round-{rnd}.json"
            method, judge = read(method_path), read(judge_path)
            checked(method_path, judge["adapter_audit"]["source_hash"])
            assert method["pair_id"] == judge["pair_id"] == pair_id
            assert method["round"] == judge["round"] == rnd
            assert method["eligible"] and judge["status"] == "completed"
            current = inputs[pair_id].hashes
            differences = {k: {"historical": value, "current": current.get(k)} for k, value in method["input_hashes"].items() if current.get(k) != value}
            assert not differences, (model, pair_id, rnd, differences)
            outcomes = judge["report_outcomes"]
            assert len(outcomes) == len(method["report_issue_clusters"])
            assert {r["original_report_id"] for r in outcomes} == {r["issue_id"] for r in method["report_issue_clusters"]}
            if model == "sonnet":
                fields = ("original_report_id", "validity", "d_tier", "a0_subtype", "full_ledger_ids", "partial_ledger_ids")
                assert [{k:r[k] for k in fields} for r in outcomes] == [{k:r[k] for k in fields} for r in cell["reports"]]
            reports.extend({**r, "pair_id": pair_id, "round": rnd, "nl_cluster": sonnet["pair_clusters"][pair_id]} for r in outcomes)
            manifests.append({"pair_id": pair_id, "round": rnd,
                              "method_source": str(method_path.relative_to(PAPER)), "method_sha256": digest(method_path),
                              "judge_source": str(judge_path.relative_to(PAPER)), "judge_sha256": digest(judge_path),
                              "input_hashes": current, "reports": len(outcomes)})
        assert len(manifests) == 162
        assert {(c["pair_id"], c["round"]) for c in manifests} == {(p, r) for p in pairs for r in (1, 2, 3)}
        metrics = arithmetic.calculate(reports, items)
        assert tuple(metrics[k] for k in ("K", "N", "I")) == ((536, 183, 104) if model == "sonnet" else (561, 198, 144))
        result["models"][model] = {"cells": sorted(manifests, key=lambda c:(c["pair_id"], c["round"])), "metrics": metrics}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = verify()
    if args.output:
        args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({m: {"cells": len(v["cells"]), **{k: v["metrics"][k] for k in ("K", "N", "I", "precision", "hit1", "hit3", "hitall")}} for m, v in result["models"].items()}, indent=2))
