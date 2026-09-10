"""Aggregate frozen open-model A3 judgments using the existing A3 arithmetic."""
import argparse
from collections import Counter
import json
from pathlib import Path

from analyze_a3 import arithmetic, content_breakdown, normalized_reports, per_round
from verify_sources import PAPER, digest, read


def analyze(root, allow_partial=False):
    math = arithmetic()
    items = read(PAPER / "discover_matrix/ledger_v2/ledger.json")["items"]
    selected = read(root / "method_selection.json")
    clusters = read(PAPER / "final_results/e2_20260907/qwen/cells.json")["pair_clusters"]
    output = {"schema": "a3.open-judged.v1", "complete": True, "models": {},
              "scope": "Qwen/Muse A3 versus immutable same-model Full; automated judge, no new human confirmations.",
              "ledger_items": len(items), "expected_round_units": 3 * len(items)}
    for model in ("qwen", "muse"):
        judges = {}
        for path in sorted(root.glob(f"judge/{model}/*/*/pairs/*.json")):
            judge = read(path)
            if judge["status"] != "completed":
                continue
            key = judge["pair_id"], judge["round"]
            assert key not in judges, (model, key, "duplicate successful judge")
            assert judge["model_profile"] == "gpt-5.6-luna"
            assert judge["validity_aggregation"] == "arbitration"
            assert judge["closure_profile"] == "full" and judge["k_closure"] == "relation_first"
            assert judge["validity_arbitration_trigger"] == "any"
            assert judge["prompt_template_hash"] == "sha256:761309756a872bd52810acca1e667864acbff91e0e1f10540de7c064710a8fda"
            assert not judge["validity_extra_readings"]
            judges[key] = path, judge
        methods = selected["models"][model]
        expected = {(c["pair"], c["round"]) for c in methods["cells"]}
        assert len(expected) == 162 and set(judges) <= expected
        reports, cells, funnel, calls = [], [], Counter(), Counter()
        usage_ids = set()
        for row in methods["cells"]:
            key = row["pair"], row["round"]
            path = root / "judge_source" / model / "method" / key[0] / f"round-{key[1]}.json"
            assert digest(path).removeprefix("sha256:") == row["sha256"]
            method = read(path)
            cell = {"pair_id": key[0], "round": key[1], "source": str(path), "sha256": digest(path),
                    "eligible": method["eligible"], "reports": len(method["report_issue_clusters"]), "judged": key in judges}
            assert cell["eligible"] and cell["reports"] == row["published"]
            funnel["method_cells"] += 1
            funnel["eligible_cells"] += 1
            funnel["generated"] += len(method["evidence_records"])
            funnel["published"] += cell["reports"]
            cell["generation_mapping"] = []
            for record in method["evidence_records"]:
                mapped = {k: record.get(k) for k in ("generation_index", "generation_hash", "issue_id", "final_report_id",
                          "publication_status", "issue_emitted", "predicate_id", "title", "witness_level", "source_quotes_exact", "reason", "basis")}
                mapped.update(binding_precise=record.get("binding", {}).get("precise"),
                              verdict=record.get("receipt", {}).get("verdict"),
                              execution_status=record.get("execution_receipt", {}).get("execution_status"))
                cell["generation_mapping"].append(mapped)
                for field, prefix in (("publication_status", "publication_"), ("verdict", "raw_verdict_"), ("witness_level", "witness_")):
                    funnel[prefix + str(mapped[field])] += 1
            if key in judges:
                judge_path, judge = judges[key]
                assert judge["adapter_audit"]["source_hash"] == digest(path)
                assert {r["original_report_id"] for r in judge["report_outcomes"]} == {r["issue_id"] for r in method["report_issue_clusters"]}
                anonymous = {r["anonymous_id"] for r in judge["adapter_audit"]["report_id_map"]}
                for reading in (1, 2):
                    certificates = judge[f"validity_reading_{reading}"]["certificates"]
                    assert len(certificates) == len(anonymous)
                    assert {c["report_id"] for c in certificates} == anonymous
                    relations = judge[f"relation_reading_{reading}"]
                    assert {r["report_id"] for r in relations["responses"]} | set(relations["backend_invalid_report_ids"]) == anonymous
                assert {e["ledger_id"] for e in judge["expected_outcomes"]} == {e for e, item in items.items() if item["pair"] == key[0]}
                for expected_row in judge["expected_outcomes"]:
                    eid = expected_row["ledger_id"]
                    valid = [r for r in judge["report_outcomes"] if r["validity"] == "VALID_KNOWN"]
                    full_ids = {r["original_report_id"] for r in valid if eid in r["full_ledger_ids"]}
                    partial_ids = {r["original_report_id"] for r in valid if eid in r["partial_ledger_ids"]}
                    assert set(expected_row["full_report_ids"]) == full_ids
                    assert set(expected_row["partial_report_ids"]) == partial_ids
                    assert expected_row["hit"] == bool(full_ids) and expected_row["supported"] == bool(full_ids | partial_ids)
                reports.extend(normalized_reports(cell, method, judge, path, clusters))
                cell.update(judge_source=str(judge_path.relative_to(root)), judge_sha256=digest(judge_path),
                            expected_outcomes=judge["expected_outcomes"])
                for receipt in judge["call_receipts"]:
                    calls["stage_receipts"] += 1
                    calls["stage_status_" + receipt["status"]] += 1
                    calls["recorded_cost_usd"] += receipt["cost_usd"] or 0
                    calls["unpriced_stage_receipts"] += receipt["cost_usd"] is None
                    for usage in receipt["usage"]:
                        assert usage["model_call_id"] not in usage_ids
                        usage_ids.add(usage["model_call_id"])
                        calls["observed_provider_calls"] += 1
                        calls["usage_status_" + usage["status"]] += 1
                        calls["unknown_token_usage_rows"] += usage["input_tokens"] is None or usage["output_tokens"] is None
                        for name in ("input_tokens", "output_tokens"):
                            calls[name] += usage[name] or 0
            cells.append(cell)
        complete = set(judges) == expected
        output["complete"] &= complete
        if not allow_partial:
            assert complete, (model, "missing judge cells", sorted(expected-set(judges)))
        coverage = {"planned_cells": 162, "eligible_cells": 162, "judged_cells": len(judges),
                    "unjudged_reports": sum(c["reports"] for c in cells if not c["judged"]),
                    "missing_method_cells": [], "missing_judge_cells": sorted(expected-set(judges))}
        a3 = {"reports": reports, "cells": cells, "coverage": coverage, "funnel": dict(funnel),
              "call_audit": methods["usage"], "judge_call_audit": dict(calls),
              "metrics": math.calculate(reports, items),
              "metrics_scope": "complete_162_cells" if complete else f"interim_{len(judges)}_judged_cells"}
        full_reports, full_cells = [], []
        e2 = PAPER / "final_results/e2_20260907"
        for source in read(e2 / model / "cells.json")["cells"]:
            if source["arm"] != "ours":
                continue
            path, judge_path = e2 / "raw" / source["source"], e2 / "raw" / source["judge_source"]
            assert digest(path).removeprefix("sha256:") == source["sha256"].removeprefix("sha256:")
            assert digest(judge_path) == source["judge_sha256"]
            method, judge = read(path), read(judge_path)
            assert judge["adapter_audit"]["source_hash"] == digest(path)
            cell = {"pair_id": source["pair"], "round": source["round"], "reports": len(source["reports"]),
                    "method_source": str(path.relative_to(PAPER)), "method_sha256": digest(path),
                    "judge_source": str(judge_path.relative_to(PAPER)), "judge_sha256": digest(judge_path)}
            assert len(judge["report_outcomes"]) == len(method["report_issue_clusters"]) == cell["reports"]
            full_cells.append(cell)
            full_reports.extend(normalized_reports(cell, method, judge, path, clusters))
        assert len(full_cells) == 162
        full = {"reports": full_reports, "cells": full_cells, "metrics": math.calculate(full_reports, items)}
        for arm in (a3, full):
            arm["metrics"]["valid_reports"] = arm["metrics"]["K"] + arm["metrics"]["N"]
            arm["metrics"]["I_per_completed_cell"] = math.ratio(arm["metrics"]["I"], len(judges) if arm is a3 else 162)
            arm["per_round"] = per_round(arm["reports"], arm["cells"], items, math)
        comparison = math.compare(a3, full, items) if complete else None
        if comparison:
            comparison["scope"] = "Same-model A3 versus frozen Full, 54 pairs x 3 rounds; nine NL clusters. Historical serving seed/date differences remain."
            comparison["content"] = content_breakdown(a3, full, items)
        output["models"][model] = {"a3": a3, "full": full, "comparison": comparison}
    return output


def four_model_summary(open_results):
    assert open_results["complete"] and set(open_results["models"]) == {"qwen", "muse"}
    previous_path = PAPER / "final_results/a3_20260910/results.json"
    previous = read(previous_path)
    assert previous["complete"] and set(previous["models"]) == {"sonnet", "luna"}
    models = {**previous["models"], **open_results["models"]}
    return {"schema": "a3.four-model-summary.v1", "complete": True, "human_confirmations": 0,
            "prior_results_sha256": digest(previous_path), "method_cells": 648, "judged_cells": 648,
            "published_reports": sum(d["a3"]["metrics"]["reports"] for d in models.values()),
            "unjudged_reports": sum(d["a3"]["coverage"]["unjudged_reports"] for d in models.values()),
            "models": {m: {"a3": {k: d["a3"][k] for k in ("metrics", "per_round", "coverage", "funnel")},
                           "full": {k: d["full"][k] for k in ("metrics", "per_round")},
                           "comparison": {k: d["comparison"][k] for k in ("scope", "delta_pp", "cluster_bootstrap_95pct", "lost_by_tier", "gained_by_tier")}}
                       for m, d in models.items()}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    parser.add_argument("--four-model-output", type=Path)
    args = parser.parse_args()
    data = analyze(args.root.resolve(), args.allow_partial)
    args.output.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n")
    if args.four_model_output:
        args.four_model_output.write_text(json.dumps(four_model_summary(data), ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({m: {k: v for k, v in d["a3"]["coverage"].items() if not k.startswith("missing_")} for m, d in data["models"].items()}))
