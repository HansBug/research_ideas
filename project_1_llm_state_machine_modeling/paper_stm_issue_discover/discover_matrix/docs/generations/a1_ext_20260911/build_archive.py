"""Freeze the A1-ext run into final_results/a1_ext_20260911. Local-only: needs the gitignored run directory.

Never re-judges or re-runs anything. Reads frozen judge pair outcomes, the frozen judge_source method cells,
the immutable E2 Full ours cells and the ledger; writes results.json, source_manifest.json and archive_manifest.json.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

from a1ext_common import (AXES, MODELS, PAPER, PROFILES, calculate, compare, content_breakdown, digest, expected_rows,
                          ledger_items, per_round, read, strict_cluster_bootstrap)

RUN_DEFAULT = Path("/home/zhangshaoang/oo-projects/research_ideas-2/runs/paper1/a1_ext_20260911")
OUT = PAPER / "final_results/a1_ext_20260911"
E2 = PAPER / "final_results/e2_20260907"
LUNA = PAPER / "final_results/a1_no_inspect_vs_v61_20260906/results.json"
JUDGE_PROMPT = "sha256:761309756a872bd52810acca1e667864acbff91e0e1f10540de7c064710a8fda"
JUDGE_PROTOCOL = "d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210"
REPORT_FIELDS = ("original_report_id", "validity", "defect_class", "d_tier", "a0_subtype", "full_ledger_ids",
                 "partial_ledger_ids", "root_cause_cluster_key", "reason", "basis")
METHOD_FIELDS = ("title", "property", "predicate_id", "witness_level", "coverage_class", "violation_direction", "contract_id")


def rel(path, root):
    return str(Path(path).resolve().relative_to(root.resolve()))


def judge_pairs(run, model):
    """{(pair, round): (path, judge)} over completed judged cells; aborted duplicates excluded; no duplicate keys."""
    out = {}
    for path in sorted((run / "judge" / model).glob("r*/*/pairs/*.json")):
        if "_aborted" in path.parts:
            continue
        judge = read(path)
        if judge["status"] != "completed":
            continue
        key = (judge["pair_id"], int(judge["round"]))
        assert key not in out, (model, key, "duplicate completed judge")
        assert judge["model_profile"] == "aizzz-luna-judge" and judge["prompt_template_hash"] == JUDGE_PROMPT
        assert judge["protocol_sha256"] == JUDGE_PROTOCOL and judge["validity_aggregation"] == "arbitration"
        assert judge["closure_profile"] == "full" and judge["k_closure"] == "relation_first"
        assert judge["validity_arbitration_trigger"] == "any" and not judge["validity_extra_readings"]
        out[key] = (path, judge)
    return out


def judge_runs(run, model):
    lines = [l for l in (run / "logs" / f"{model}-judge.exit").read_text().splitlines() if l.strip()]
    rows = []
    for d in sorted((run / "judge" / model).glob("r*/*/")):
        rid = d.name; rnd = int(d.parent.name[1:])
        start = next((l for l in lines if l.startswith("start") and rid in l), "")
        end = next((l for l in lines if l.startswith("end") and rid in l), "")
        rows.append({"round": rnd, "run_id": rid, "workers": int(re.search(r"workers=(\d+)", start).group(1)) if "workers=" in start else 1,
                     "pairs_completed": len(list((d / "pairs").glob("*.json"))), "pair_failures": len(list((d / "failures").glob("*.json"))),
                     "started_at": start.split()[1] if start else None, "ended_at": end.split()[1] if end else None,
                     "rc": int(re.search(r"rc=(\d+)", end).group(1)) if end else None,
                     "resample_of_failed_pair": "resample=1" in start, "manifest_sha256": digest(d / "run_manifest.json")})
    return rows


def a1ext_arm(run, model, items, clusters):
    src = run / "judge_source" / model
    manifest = read(src / "MANIFEST.json")
    judges = judge_pairs(run, model)
    cells, reports = [], []
    funnel = Counter(); w_candidates = Counter(); w_published = Counter(); coverage_class = Counter(); exec_status = Counter()
    calls = Counter()
    for path in sorted(src.glob("method/*/round-*.json")):
        cell = read(path); key = (cell["pair_id"], int(cell["round"]))
        assert key in judges, ("unjudged cell", model, key)
        jpath, judge = judges[key]
        clusters_by_issue = {r["issue_id"]: r for r in cell["report_issue_clusters"]}
        outcomes = judge["report_outcomes"]
        assert {r["original_report_id"] for r in outcomes} == set(clusters_by_issue), (model, key, "judge reports != published clusters")
        for o in outcomes:
            c = clusters_by_issue[o["original_report_id"]]
            reports.append({"pair_id": key[0], "round": key[1], **{k: o.get(k) for k in REPORT_FIELDS},
                            **{k: c.get(k) for k in METHOD_FIELDS}, "method_cell": f"{key[0]}/round-{key[1]}",
                            "nl_cluster": clusters[key[0]]})
        replaced = manifest["replaced_by_recovery"].get(f"{key[0]}/r{key[1]}")
        cells.append({"pair_id": key[0], "round": key[1], "reports": len(outcomes), "status": cell["status"], "eligible": cell["eligible"],
                      "errors": len(cell["errors"]), "source": f"judge_source/{model}/method/{key[0]}/round-{key[1]}.json", "sha256": digest(path),
                      "method_run_id": cell["run_id"], "replaced_by_isolated_recovery": bool(replaced),
                      "recovery_source": rel(replaced, run) if replaced else None,
                      "judge_run_id": judge["run_id"], "judge_source": rel(jpath, run), "judge_sha256": digest(jpath),
                      "candidates": len(cell["evidence_records"]), "llm_calls": len(cell["llm_calls"])})
        funnel["cells"] += 1; funnel["candidates"] += len(cell["evidence_records"]); funnel["published"] += len(outcomes)
        for er in cell["evidence_records"]:
            w_candidates[er.get("witness_level") or "n/a"] += 1; coverage_class[er.get("coverage_class") or "n/a"] += 1
            exec_status[(er.get("execution_receipt") or {}).get("execution_status") or "n/a"] += 1
            funnel["candidates_with_predicate"] += bool(er.get("predicate_id")); funnel["candidates_emitted"] += bool(er.get("issue_emitted"))
        for c in cell["report_issue_clusters"]:
            w_published[c.get("witness_level") or "n/a"] += 1
        for lc in cell["llm_calls"]:
            calls["structured_calls"] += 1
            calls["schema_validation_failures"] += len(lc.get("schema_validation_failures") or [])
            for a in lc.get("attempts", []):
                calls["transport_retry_records"] += len(a.get("retry_records") or [])
            for u in lc.get("usage") or []:
                calls["input_tokens"] += u.get("input_tokens") or 0; calls["output_tokens"] += u.get("output_tokens") or 0
    assert len(cells) == 162 and set(judges) == {(c["pair_id"], c["round"]) for c in cells}
    arm = {"label": f"A1-ext no-inspect / {PROFILES[model]}", "profile": PROFILES[model], "ledger_hash": digest(PAPER / "discover_matrix/ledger_v2/ledger.json"),
           "judge_source_manifest_sha256": digest(src / "MANIFEST.json"), "judge_runs": judge_runs(run, model),
           "coverage": {"planned_cells": 162, "eligible_cells": sum(c["eligible"] for c in cells), "judged_cells": len(cells),
                        "planned_expected_rounds": 3 * len(items), "unjudged_reports": 0,
                        "degraded_cells": sum(1 for c in cells if not c["status"].startswith("completed")),
                        "cells_with_diagnostics": sum(1 for c in cells if c["status"] == "completed_with_diagnostics"),
                        "cells_replaced_by_isolated_recovery": sum(c["replaced_by_isolated_recovery"] for c in cells)},
           "cells": cells, "reports": reports, "expected": expected_rows(reports, items),
           "metrics": calculate(reports, items), "per_round": per_round(reports, items), "content": content_breakdown(reports, items),
           "funnel": {**dict(funnel), "candidate_witness": dict(w_candidates), "published_witness": dict(w_published),
                      "candidate_coverage_class": dict(coverage_class), "candidate_execution_status": dict(exec_status)},
           "call_audit": dict(calls)}
    assert arm["coverage"]["eligible_cells"] == 162 and arm["coverage"]["degraded_cells"] == 0
    return arm


def full_arm(model, items, clusters):
    data = read(E2 / model / "cells.json")
    cells, reports = [], []
    funnel = Counter(); w_candidates = Counter(); w_published = Counter(); coverage_class = Counter(); verdicts = Counter()
    for c in data["cells"]:
        if c["arm"] != "ours":
            continue
        key = (c["pair"], int(c["round"]))
        by_issue = {e["issue_id"]: e for e in c.get("candidate_evidence", [])}
        for r in c["reports"]:
            e = by_issue.get(r["original_report_id"], {})
            reports.append({"pair_id": key[0], "round": key[1], **{k: r.get(k) for k in REPORT_FIELDS},
                            **{k: e.get(k) for k in METHOD_FIELDS if k != "title"}, "title": None,
                            "method_cell": f"{key[0]}/round-{key[1]}", "nl_cluster": clusters[key[0]]})
            w_published[e.get("witness_level") or "n/a"] += 1
        cells.append({"pair_id": key[0], "round": key[1], "reports": len(c["reports"]), "status": c["status"], "eligible": c["status"].startswith("completed"),
                      "source": f"final_results/e2_20260907/{c['source']}", "sha256": "sha256:" + c["sha256"] if not str(c["sha256"]).startswith("sha256:") else c["sha256"],
                      "source_commit": c.get("source_commit"), "judge_source": f"final_results/e2_20260907/{c['judge_source']}", "judge_sha256": c.get("judge_sha256"),
                      "candidates": len(c.get("candidate_evidence", [])), "llm_calls": c.get("calls")})
        funnel["cells"] += 1; funnel["candidates"] += len(c.get("candidate_evidence", [])); funnel["published"] += len(c["reports"])
        for e in c.get("candidate_evidence", []):
            w_candidates[e.get("witness_level") or "n/a"] += 1; coverage_class[e.get("coverage_class") or "n/a"] += 1
            funnel["candidates_with_predicate"] += bool(e.get("predicate_id")); funnel["candidates_emitted"] += bool(e.get("issue_emitted"))
        for r in c.get("predicate_receipts", []):
            verdicts[r.get("verdict") or r.get("execution_state") or "n/a"] += 1
    assert len(cells) == 162
    return {"label": f"E2 Full ours / {data['model']}", "profile": PROFILES[model], "e2_cells_sha256": digest(E2 / model / "cells.json"),
            "coverage": {"planned_cells": 162, "eligible_cells": sum(c["eligible"] for c in cells), "judged_cells": len(cells),
                         "planned_expected_rounds": 3 * len(items), "unjudged_reports": 0},
            "cells": cells, "reports": reports, "expected": expected_rows(reports, items),
            "metrics": calculate(reports, items), "per_round": per_round(reports, items), "content": content_breakdown(reports, items),
            "funnel": {**dict(funnel), "candidate_witness": dict(w_candidates), "published_witness": dict(w_published),
                       "candidate_coverage_class": dict(coverage_class), "predicate_receipt_verdicts": dict(verdicts)}}


def luna_reference():
    d = read(LUNA)
    return {"archive": "final_results/a1_no_inspect_vs_v61_20260906/results.json", "sha256": digest(LUNA),
            "metrics": {"no_inspect_a1": d["a1"]["metrics"], "full_v61": d["v61"]["metrics"]},
            "comparison": {k: d["comparison"][k] for k in ("delta_pp", "cluster_bootstrap_95pct", "bootstrap_seed", "bootstrap_replicates")},
            "scope": "Read-only pointer to the frozen Luna A1 archive; the four-model tables cite it without recomputation here."}


def source_manifest(run, models):
    def run_manifests(pattern):
        rows = []
        for mf in sorted(run.glob(pattern)):
            m = read(mf)
            rows.append({"run_id": m["run_id"], "profile": m.get("profile"), "ablation": m.get("ablation"), "rounds": m.get("rounds"),
                         "workers": m.get("workers"), "status": m.get("status"), "source_commit": m["source_provenance"]["source_commit"],
                         "source_branch": m["source_provenance"]["source_branch"], "path": rel(mf, run), "sha256": digest(mf)})
        return rows
    raw = []
    for path in sorted(list(run.glob("judge_source/*/method/*/round-*.json")) + list(run.glob("judge/*/r*/*/pairs/*.json"))):
        raw.append({"path": rel(path, run), "sha256": digest(path), "bytes": path.stat().st_size, "excluded": "_aborted" in path.parts})
    return {"schema": "a1ext.source-manifest.v1", "run_root": "runs/paper1/a1_ext_20260911 (gitignored, local only)",
            "method_runs": {m: run_manifests(f"method/{m}/*/run_manifest.json") for m in models},
            "failed_attempts_excluded": run_manifests("method/sonnet_failed_403_attempt1/*/run_manifest.json"),
            "isolated_recovery_runs": {m: run_manifests(f"method/{m}_recovery/*/*/run_manifest.json") for m in models},
            "judge_source_manifests": {m: {"sha256": digest(run / "judge_source" / m / "MANIFEST.json"), **{k: v for k, v in read(run / "judge_source" / m / "MANIFEST.json").items() if k != "files"}} for m in models},
            "aborted_judge_runs": [rel(p, run) for p in sorted((run / "judge" / "_aborted").glob("*"))],
            "incidents": "INCIDENTS.md", "run_record": "RUN_RECORD.md",
            "raw_index": raw, "raw_policy": "Raw method cells, judge outcomes, prompts, streams and usage stay in the local run directory; this manifest pins their hashes."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=RUN_DEFAULT)
    parser.add_argument("--out", type=Path, default=OUT)
    args = parser.parse_args()
    run, out = args.run.resolve(), args.out.resolve()
    assert (run / "DONE").exists(), "run not finished"
    items = ledger_items()
    clusters = read(E2 / "muse/cells.json")["pair_clusters"]
    for e, i in items.items():
        assert clusters[i["pair"]] == i["pair_context"]["nl_sha8"], e
    commit = subprocess.run(["git", "-C", str(PAPER), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
    results = {"schema": "a1ext.three-model-no-inspect.v1", "complete": True, "frozen_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
               "build_commit": commit, "ledger_hash": digest(PAPER / "discover_matrix/ledger_v2/ledger.json"), "ledger_items": len(items),
               "expected_round_units": 3 * len(items), "pair_clusters": clusters,
               "judge": {"profile": "aizzz-luna-judge", "model": "gpt-5.6-luna", "endpoint_ref": "https://api.aizzz.xyz/v1", "workers": 24,
                         "protocol_sha256": JUDGE_PROTOCOL, "prompt_template_hash": JUDGE_PROMPT, "validity_readings": 2,
                         "validity_aggregation": "arbitration", "validity_arbitration_trigger": "any", "k_closure": "relation_first", "closure_profile": "full",
                         "same_provider_as": "A1 #205 judge_aizzz batches"},
               "scope": "Three fixed model configurations, no-inspect versus the immutable same-model E2 Full ours; automated judge, zero new human confirmations; not a pure single-factor causal estimate.",
               "models": {}, "luna_reference": luna_reference()}
    for model in MODELS:
        ext = a1ext_arm(run, model, items, clusters)
        full = full_arm(model, items, clusters)
        results["models"][model] = {"a1ext": ext, "full": full,
                                    "comparison": {**compare(ext, full, items), "strict": strict_cluster_bootstrap(ext, full, items)}}
        m = results["models"][model]
        print(model, "a1ext", m["a1ext"]["metrics"]["reports"], m["a1ext"]["metrics"]["hit1"], "full", m["full"]["metrics"]["reports"], m["full"]["metrics"]["hit1"], flush=True)
    out.mkdir(parents=True, exist_ok=True)
    (out / "results.json").write_text(json.dumps(results, ensure_ascii=False, indent=1, sort_keys=True) + "\n")
    (out / "source_manifest.json").write_text(json.dumps(source_manifest(run, MODELS), ensure_ascii=False, indent=1) + "\n")
    for name in ("INCIDENTS.md", "RUN_RECORD.md"):
        shutil.copy2(run / name, out / name)
    files = {n: digest(out / n) for n in ("results.json", "source_manifest.json", "INCIDENTS.md", "RUN_RECORD.md")}
    (out / "archive_manifest.json").write_text(json.dumps({"schema": "a1ext.archive-manifest.v1", "created_at": results["frozen_at"], "build_commit": commit,
                                                              "ledger_sha256": results["ledger_hash"], "files": files}, indent=1) + "\n")
    print("archive written to", out, "| results.json bytes", (out / "results.json").stat().st_size)


if __name__ == "__main__":
    main()
