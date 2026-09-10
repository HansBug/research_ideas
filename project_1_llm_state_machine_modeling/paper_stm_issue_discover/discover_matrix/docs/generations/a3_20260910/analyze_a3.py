"""Recompute A3 sources, publication funnel, judgements, and paired metrics offline."""

import argparse
from collections import Counter
import importlib.util
import json
from pathlib import Path

from verify_sources import PAPER, digest, read, verify


def arithmetic():
    spec = importlib.util.spec_from_file_location("a1_arithmetic", PAPER / "discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_reports(cell, method, judge, method_path, clusters):
    published = {r["issue_id"]: r for r in method["report_issue_clusters"]}
    outcomes = judge["report_outcomes"]
    assert len(published) == len(outcomes)
    assert set(published) == {r["original_report_id"] for r in outcomes}
    return [{**r, "pair_id": cell["pair_id"], "round": cell["round"],
             "nl_cluster": clusters[cell["pair_id"]], "method_cell": str(method_path),
             "published_claim": {k: published[r["original_report_id"]].get(k) for k in
                                 ("title", "locus_kind", "locus_names", "property", "violation_direction", "expected", "observed", "requirement_quote", "source_refs", "reason", "basis")},
             **{k: published[r["original_report_id"]].get(k) for k in ("title", "property", "predicate_id", "witness_level")}}
            for r in outcomes]


def per_round(reports, cells, items, math):
    result = {}
    for rnd in (1, 2, 3):
        selected = [r for r in reports if r["round"] == rnd]
        counts = Counter(r["validity"] for r in selected)
        hit = {e for r in selected if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
        n_cells = sum(c["round"] == rnd and c.get("judged", True) for c in cells)
        result[rnd] = {"judged_cells": n_cells, "reports": len(selected),
                       "K": counts["VALID_KNOWN"], "N": counts["VALID_NOVEL"], "I": counts["INVALID"],
                       "valid_reports": counts["VALID_KNOWN"] + counts["VALID_NOVEL"],
                       "I_per_completed_cell": math.ratio(counts["INVALID"], n_cells),
                       "precision": math.ratio(counts["VALID_KNOWN"] + counts["VALID_NOVEL"], len(selected)),
                       "hit": math.ratio(len(hit), len(items)),
                       "tier_hits": {tier: math.ratio(sum(items[e]["L"] == tier for e in hit), sum(i["L"] == tier for i in items.values())) for tier in ("L0", "L1", "L2")}}
    return result


def analyze(root, allow_partial=False):
    from paper_stm_judge.artifacts import adapt_evidence_discovery_release

    math = arithmetic()
    items = read(PAPER / "discover_matrix/ledger_v2/ledger.json")["items"]
    clusters = read(PAPER / "final_results/e2_20260907/sonnet/cells.json")["pair_clusters"]
    controls = verify()
    output = {"schema": "a3.analysis.v1", "complete": True, "models": {},
              "scope": "Sonnet/Luna only; no Qwen/Muse results, no O2 eligibility implied",
              "ledger_items": len(items), "expected_round_units": 3 * len(items)}
    for model in ("sonnet", "luna"):
        source_roots = ([root / "sonnet/smoke-corrected", root / "sonnet/recovered", *sorted((root / "sonnet").glob("fill-r*/*/run_manifest.json")), *sorted((root / "sonnet/remaining").glob("*/run_manifest.json")),
                         *sorted((root / "sonnet/smoke-r2").glob("*/run_manifest.json")),
                         *sorted((root / "sonnet/smoke-r3").glob("*/run_manifest.json"))]
                        if model == "sonnet" else sorted((root / "luna/full").glob("*/run_manifest.json")))
        source_roots = [p.parent if p.name == "run_manifest.json" else p for p in source_roots]
        methods = {}
        for directory in source_roots:
            for path in directory.glob("method/*/round-*.json"):
                cell = read(path)
                key = cell["pair_id"], cell["round"]
                assert key not in methods, (model, key, "duplicate method cell")
                assert cell["ablation"] == "direct-report"
                assert len(cell["llm_calls"]) == 1
                assert cell["stage_outputs"]["execute_batch"]["new_candidate_count"] == 0
                assert all(r["d_level"] is None for r in cell["evidence_records"])
                assert all(r["expected"] == cell["model_output"]["issues"][r["generation_index"]]["expected"]
                           and r["observed"] == cell["model_output"]["issues"][r["generation_index"]]["observed"]
                           for r in cell["evidence_records"])
                assert len(cell["model_output"]["issues"]) == len(cell["evidence_records"])
                methods[key] = path, cell
        if model == "sonnet":
            recovered_root = root / "sonnet/schema-recovered"
            for path in recovered_root.glob("method/*/round-*.json"):
                cell = read(path)
                key = cell["pair_id"], cell["round"]
                prior_path, prior = methods[key]
                recovery = read(recovered_root / "run_manifest.json")
                assert not prior["eligible"] and cell["eligible"]
                assert recovery["source_hash"] == digest(prior_path)
                methods[key] = path, cell
        judgements = {}
        for path in sorted((root / "judge" / model).glob("*/*/pairs/*.json")):
            judge = read(path)
            key = judge["pair_id"], judge["round"]
            if judge["status"] != "completed":
                continue
            assert key not in judgements, (model, key, "duplicate judged cell")
            judgements[key] = path, judge
        expected = {(p, rnd) for p in clusters for rnd in (1, 2, 3)}
        assert set(methods) <= expected and set(judgements) <= set(methods)
        reports, cells, funnel, calls = [], [], Counter(), Counter()
        for key, (method_path, method) in sorted(methods.items()):
            funnel["method_cells"] += 1
            funnel["eligible_cells"] += bool(method["eligible"])
            funnel["generated"] += len(method["evidence_records"])
            funnel["published"] += len(method["report_issue_clusters"])
            for call in method["llm_calls"]:
                calls["logical_generation_stages"] += 1
                calls["provider_model_calls"] += call["result"].get("model_calls_used", 0)
                calls["schema_validation_failures"] += len(call["schema_validation_failures"])
                calls["structured_recovered_cells"] += bool(call["result"].get("structured_recovery"))
                calls["recorded_cost_usd"] += call["cost"].get("total_usd") or 0
                calls["unpriced_usage_rows"] += call["cost"].get("unpriced_usage_count", 0)
                for usage in call["usage"]:
                    for name in ("input_tokens", "output_tokens", "reasoning_tokens"):
                        calls[name] += usage.get(name) or 0
                    calls["usage_status_" + str(usage.get("status", "unrecorded"))] += 1
                calls["truncated_stages"] += bool(call["context_budget"]["truncation_applied"])
            for record in method["evidence_records"]:
                funnel["binding_precise"] += bool(record.get("binding", {}).get("precise"))
                funnel["publication_" + record["publication_status"]] += 1
                funnel["raw_verdict_" + record.get("receipt", {}).get("verdict", "missing")] += 1
                funnel["witness_" + record["witness_level"]] += 1
            row = {"pair_id": key[0], "round": key[1], "source": str(method_path), "sha256": digest(method_path),
                   "eligible": method["eligible"], "reports": len(method["report_issue_clusters"]), "judged": key in judgements}
            if key in judgements:
                judge_path, judge = judgements[key]
                assert method["eligible"]
                source_hash = judge["adapter_audit"]["source_hash"]
                if source_hash != row["sha256"]:
                    assert model == "sonnet" and key in {(p, 1) for p in ("0000", "0001", "0002")}
                    original = Path(judge["adapter_audit"]["source_path"])
                    assert digest(original) == source_hash
                    old_reports, _, _, _ = adapt_evidence_discovery_release(original, ())
                    new_reports, _, _, _ = adapt_evidence_discovery_release(method_path, ())
                    assert [r.model_dump() for r in old_reports] == [r.model_dump() for r in new_reports]
                    row["judge_reuse"] = {"original_source": str(original), "original_source_hash": source_hash,
                                         "reason": "Identical report projection; only deterministic execution evidence repaired."}
                reports.extend(normalized_reports(row, method, judge, method_path, clusters))
                row.update(judge_source=str(judge_path), judge_sha256=digest(judge_path))
            cells.append(row)
        coverage = {"planned_cells": 162, "eligible_cells": funnel["eligible_cells"], "judged_cells": len(judgements),
                    "unjudged_reports": sum(c["reports"] for c in cells if not c["judged"]),
                    "missing_method_cells": sorted(expected-set(methods)), "missing_judge_cells": sorted(expected-set(judgements))}
        complete = set(methods) == set(judgements) == expected and funnel["eligible_cells"] == 162
        output["complete"] &= complete
        if not allow_partial:
            assert complete, (model, coverage)
        full_reports = []
        full_cells = controls["models"][model]["cells"]
        for row in full_cells:
            path = PAPER / row["method_source"]
            full_reports.extend(normalized_reports(row, read(path), read(PAPER / row["judge_source"]), path, clusters))
        full = {"reports": full_reports, "metrics": controls["models"][model]["metrics"], "cells": full_cells}
        full["per_round"] = per_round(full_reports, full_cells, items, math)
        a3 = {"reports": reports, "cells": cells, "coverage": coverage, "funnel": dict(funnel),
              "call_audit": dict(calls), "call_audit_scope": "Selected completed generations, including their recorded retries. Interrupted unfinished calls remain separate raw audit; their missing usage is not zero cost.",
              "metrics": math.calculate(reports, items)}
        # Partial figures are explicitly marked and never used in paired inference.
        a3["metrics_scope"] = "complete_162_cells" if complete else f"interim_{len(judgements)}_judged_cells"
        a3["per_round"] = per_round(reports, cells, items, math)
        for arm in (a3, full):
            arm["metrics"]["valid_reports"] = arm["metrics"]["K"] + arm["metrics"]["N"]
            arm["metrics"]["I_per_completed_cell"] = math.ratio(arm["metrics"]["I"], len(judgements) if arm is a3 else 162)
        comparison = math.compare(a3, full, items) if complete else None
        if comparison:
            comparison["scope"] = "Same-model A3 versus frozen Full, 54 pairs x 3 rounds; nine NL clusters. Historical provider/date and Luna output-budget differences remain."
        output["models"][model] = {"a3": a3, "full": full, "comparison": comparison}
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    result = analyze(args.run_root.resolve(), args.allow_partial)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"complete": result["complete"], "models": {m: {"coverage": {k: len(v) if isinstance(v, list) else v for k, v in d["a3"]["coverage"].items()}, "funnel": d["a3"]["funnel"]} for m, d in result["models"].items()}}, indent=2))
