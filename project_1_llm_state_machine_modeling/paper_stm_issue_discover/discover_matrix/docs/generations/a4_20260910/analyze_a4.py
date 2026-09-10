"""Offline A4 reconstruction from immutable Full and local tail/judge artifacts."""

import argparse
from collections import Counter, defaultdict
import importlib.util
import json
from pathlib import Path

from paper_stm_evaluation.a4_accounting import publication_members
from paper_stm_evaluation.a4_replay import digest, mask_prepared
from paper_stm_evaluation.a4_sources import REFERENCE, checked_json
from utils.artifact_io import write_json
from utils.structured_runtime import _usage_rows


PAPER = Path(__file__).resolve().parents[4]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


arithmetic = load_module("a1_arithmetic", PAPER / "discover_matrix/docs/generations/a1_no_inspect_20260906/analyze_a1.py")
residual = load_module("a4_residual", Path(__file__).with_name("residual_judge.py"))
LABELS = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}


def report_row(outcome, pair, round_index):
    return {**outcome, "pair_id": pair, "round": round_index,
            "d_tier": outcome.get("d_tier"), "a0_subtype": outcome.get("a0_subtype")}


def calculate_metrics(reports, items):
    result = arithmetic.calculate(reports, items)
    result["D_A"] = {key if key is not None else "NO_EXTERNAL_D_A_LABEL": count
                     for key, count in result["D_A"].items()}
    return result


def tally(reports, cells, expected_count):
    labels = Counter(LABELS[r["validity"]] for r in reports)
    full = {(e, r["round"]) for r in reports if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    supported = full | {(e, r["round"]) for r in reports if r["validity"] == "VALID_KNOWN" for e in r["partial_ledger_ids"]}
    return {"cells": cells, **{k: labels[k] for k in "KNI"}, "reports": len(reports),
            "precision": arithmetic.ratio(labels["K"] + labels["N"], len(reports)),
            "strict_precision": arithmetic.ratio(sum(r["validity"] != "INVALID" and r.get("d_tier") in ("D1", "D2") for r in reports), len(reports)),
            "invalid_per_cell": arithmetic.ratio(labels["I"], cells),
            "valid_reports": labels["K"] + labels["N"],
            "hit": arithmetic.ratio(len(full), expected_count),
            "support": arithmetic.ratio(len(supported), expected_count)}


def analyze(root):
    pending = residual.prepare(PAPER, root)
    assert not any(pending.values()), "Residual judgments are incomplete"
    manifest = json.loads((root / "manifest.json").read_text())
    final = json.loads((root / "final_accounting.json").read_text())
    accounting = {(c["pair_id"], c["round"]): c for c in final["cells"]}
    items = json.loads((PAPER / "discover_matrix/ledger_v2/ledger.json").read_text())["items"]
    assert len(accounting) == 162 and len(items) == 145
    reports = {"full": [], "a4": []}
    cells, candidates, publications = [], [], []
    flows, transitions, routes, diagnostics = Counter(), Counter(), Counter(), Counter()
    d_changes, true_origins, errors = Counter(), Counter(), []
    calls, attempts, schema_failures, reused_calls, wording_changed, semantic_changed = 0, 0, 0, 0, 0, 0
    source_hashes, examples, usage = {}, {}, {}
    for row in manifest["sources"]["cells"]:
        pair, rnd = row["pair"], row["round"]
        source, source_hash = checked_json(PAPER / row["source"], row["sha256"])
        judge, judge_hash = checked_json(PAPER / row["judge_source"], row["judge_sha256"])
        source_hashes[row["source"]] = source_hash
        source_hashes[row["judge_source"]] = judge_hash
        cell_root = root / "cells" / pair / f"round-{rnd}"
        tail, tail_hash = checked_json(cell_root / "tail.json")
        assert tail["eligible"]
        assert tail["counters"]["upstream_generation_calls"] == tail["counters"]["backend_execution_calls"] == 0
        batch = source["stage_outputs"]["execute_batch"]
        assert tail["all_candidates_reached_d"] == [c["obligation_id"] for c in batch["candidates"]]
        masked = [mask_prepared(c) for c in batch["candidates"]]
        masked = [{k: v.model_dump(mode="json") if hasattr(v, "model_dump") else v for k, v in c.items()} for c in masked]
        assert digest(masked) == tail["identity"]["masked_input_hash"]
        assert json.loads((cell_root / "masked_input.json").read_text())["candidates"] == masked
        for evidence in tail["evidence_records"]:
            assert evidence["receipt"]["verdict"] == "unknown"
        old = {r["original_report_id"]: r for r in judge["report_outcomes"]}
        new = accounting[pair, rnd]["reports"]
        assert {r["report_id"] for r in new} == {r["issue_id"] for r in tail["report_issue_clusters"]}
        assert len(new) == len({r["report_id"] for r in new})
        before = [report_row(r, pair, rnd) for r in old.values()]
        after = [report_row(r["outcome"], pair, rnd) for r in new]
        assert all(r["original_report_id"] == a["report_id"] for r, a in zip(after, new))
        reports["full"].extend(before)
        reports["a4"].extend(after)
        expected_ids = {e["ledger_id"] for e in judge["expected_outcomes"]}
        assert expected_ids == {e for e, v in items.items() if v["pair"] == pair}
        members = defaultdict(list)
        for report in tail["report_issue_clusters"]:
            for member in publication_members(tail, report):
                members[member["obligation_id"]].append(report["issue_id"])
        evidence = {r["obligation_id"]: r for r in tail["evidence_records"]}
        old_evidence = {r["obligation_id"]: r for r in source["evidence_records"]}
        unresolved = set(tail["stage_outputs"]["validate_d"]["final_unresolved_ids"])
        assert set(evidence) == {r["obligation_id"] for r in batch["candidates"]}
        primary = {r["issue_id"]: r["obligation_id"] for r in tail["report_issue_clusters"]}
        for c in batch["candidates"]:
            oid = c["obligation_id"]
            e = evidence[oid]
            origin = "probe" if int(oid.rsplit(":i", 1)[1]) >= batch["candidate_count"] - batch["execution_probe_count"] else "nonprobe"
            state = "standalone" if any(primary[rid] == oid for rid in members[oid]) else "folded" if members[oid] else "rejected"
            flow = (c["receipt"]["verdict"], origin, e["d_level"], state)
            flows["/".join(flow)] += 1
            if flow[0] == "true":
                true_origins[origin] += 1
            old_d = old_evidence.get(oid, {}).get("d_level", "absent")
            d_changes[f"{old_d}->{e['d_level']}"] += 1
            candidates.append({"pair": pair, "round": rnd, "obligation_id": oid, "verdict": flow[0],
                               "origin": origin, "old_d": old_d, "new_d": e["d_level"], "publication": state,
                               "unresolved": oid in unresolved,
                               "final_report_ids": members[oid], "claim_hash": digest(c["candidate"]),
                               "source": row["source"], "tail": str((cell_root / "tail.json").relative_to(root))})
            example_key = f"{flow[0]}/{state}"
            examples.setdefault(example_key, {
                **candidates[-1], "title": c["candidate"]["title"],
                "expected": c["candidate"]["expected"], "observed": c["candidate"]["observed"],
                "full_semantic": old_evidence.get(oid, {}).get("semantic_adjudication"),
                "a4_semantic": e["semantic_adjudication"],
            })
        equivalents = set()
        for r in new:
            assert r["route"] in {"oracle_true_I", "reused_full", "newly_judged"}
            routes[r["route"]] += 1
            if r["route"] == "oracle_true_I":
                assert r["oracle_true_obligation_ids"] and r["outcome"]["validity"] == "INVALID"
            eq = r["full_equivalent_report_id"]
            new_label = LABELS[r["outcome"]["validity"]]
            old_label = LABELS[old[eq]["validity"]] if eq else "absent_or_changed"
            transitions[f"{old_label}->{new_label}"] += 1
            if eq:
                assert eq not in equivalents, "One Full publication reused more than once"
                equivalents.add(eq)
                wording_changed += any(k in r.get("wording_audit", {}) for k in ("reason", "basis"))
                semantic_changed += "semantic_adjudication" in r.get("wording_audit", {})
            publications.append({"pair": pair, "round": rnd, "report_id": r["report_id"], "route": r["route"],
                                 "label": new_label, "full_equivalent_report_id": eq, "old_label": old_label,
                                 "oracle_true_obligation_ids": r["oracle_true_obligation_ids"],
                                 "projection_hash": digest(r["projection"]), "outcome": r["outcome"],
                                 "judge_provenance": {k: v for k, v in r.get("judge_provenance", {}).items() if k != "outcome"}})
            if r["route"] == "oracle_true_I":
                member_ids = [oid for oid, ids in members.items() if r["report_id"] in ids]
                if len(member_ids) > len(r["oracle_true_obligation_ids"]):
                    examples.setdefault("mixed_oracle_report", {**publications[-1], "member_obligation_ids": member_ids})
        for rid in set(old) - equivalents:
            transitions[f"{LABELS[old[rid]['validity']]}->absent_or_changed"] += 1
        for receipt in tail["stage_receipts"]:
            assert receipt["status"] in {"completed", "completed_with_diagnostics"}
            assert not receipt["context_budget"]["truncation_applied"]
            diagnostics[f"{receipt['stage_name']}/{receipt['status']}"] += 1
        calls += tail["counters"]["terminal_structured_calls"]
        reused_calls += sum(c["reused"] for c in tail["call_audit"])
        attempts += sum(len(c["attempts"]) for c in tail["llm_calls"])
        schema_failures += sum(len(c["schema_validation_failures"]) for c in tail["llm_calls"])
        errors.extend({"pair": pair, "round": rnd, **e} for e in tail["errors"])
        cells.append({"pair": pair, "round": rnd, "source_hash": source_hash, "judge_hash": judge_hash,
                      "tail_hash": tail_hash, "full": tally(before, 1, len(expected_ids)),
                      "a4": tally(after, 1, len(expected_ids)), "routes": dict(Counter(r["route"] for r in new)),
                      "elapsed_seconds": tail["elapsed_seconds"], "calls": tail["counters"]["terminal_structured_calls"],
                      "errors": len(tail["errors"]),
                      "unresolved_ids": tail["stage_outputs"]["validate_d"]["final_unresolved_ids"]})
    metrics = {arm: calculate_metrics(rs, items) for arm, rs in reports.items()}
    rounds = {str(rnd): {arm: tally([r for r in rs if r["round"] == rnd], 54, 145) for arm, rs in reports.items()} for rnd in (1, 2, 3)}
    reference = REFERENCE[manifest["identity"]["model"]][0]
    assert tuple(metrics["full"][key] for key in "KNI") == reference
    assert sum(routes.values()) == metrics["a4"]["reports"]
    pairs = sorted({c["pair"] for c in cells})
    assert len(pairs) == 54 and {(c["pair"], c["round"]) for c in cells} == {(p, r) for p in pairs for r in (1, 2, 3)}
    pair_deltas = {p: {arm: tally([r for r in rs if r["pair_id"] == p], 3, 3 * sum(v["pair"] == p for v in items.values())) for arm, rs in reports.items()} for p in pairs}
    hit_units = {arm: {(e, r["round"]) for r in rs if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
                 for arm, rs in reports.items()}
    hit_changes = {"lost": sorted(hit_units["full"] - hit_units["a4"]),
                   "gained": sorted(hit_units["a4"] - hit_units["full"])}
    v0, v1 = (metrics[arm]["K"] + metrics[arm]["N"] for arm in ("full", "a4"))
    i0, i1 = (metrics[arm]["I"] for arm in ("full", "a4"))
    intermediate = v1 / (v1 + i0) if v1 + i0 else None
    decomposition = {
        "order": "replace valid volume first with Full I fixed, then replace I; arithmetic, not a causal decomposition",
        "valid_volume_pp": 100 * (intermediate - metrics["full"]["precision"]["rate"]) if intermediate is not None else None,
        "invalid_volume_pp": 100 * (metrics["a4"]["precision"]["rate"] - intermediate) if intermediate is not None and v1 + i1 else None,
    }
    real_terminal_calls = runtime_attempts = saved_attempts = failed_attempts = 0
    for path in sorted((root / "cells").glob("*/round-*/attempts/*/tail.json")):
        attempt = json.loads(path.read_text())
        saved_attempts += 1
        failed_attempts += not attempt["eligible"]
        real_terminal_calls += sum(not c["reused"] for c in attempt["call_audit"])
        for audit, call in zip(attempt["call_audit"], attempt["llm_calls"], strict=True):
            if not audit["reused"]:
                runtime_attempts += len(call["attempts"])
            for u in call["usage"]:
                key = u["model_call_id"]
                public = {k: u.get(k) for k in (
                    "model_call_id", "model", "input_tokens", "output_tokens", "reasoning_tokens",
                    "started_at_utc", "ended_at_utc", "duration_seconds", "time_to_first_chunk_seconds",
                    "status", "output_budget", "provider_response",
                )}
                if key in usage:
                    assert usage[key] == public
                usage[key] = public
    transport_retries = 0
    for path in (root / "cells").glob("*/round-*/attempts/*/provider/**/audit.jsonl"):
        with path.open() as stream:
            transport_retries += sum(json.loads(line).get("record_type") == "transport_retry" for line in stream)
    judge_receipts, judge_usage = [], {}
    for path in sorted((root / "judge").glob("*/*/*.json")):
        if path.parent.name not in {"pairs", "failures"}:
            continue
        record = json.loads(path.read_text())
        for call in record["call_receipts"]:
            assert 1 <= len(call["report_ids"]) <= 8
            judge_receipts.append({"source": str(path.relative_to(root)), "pair": record["pair_id"],
                                   "round": record["round"], "parent_status": path.parent.name,
                                   **{k: call[k] for k in ("call_id", "batch_id", "report_ids", "phase", "status", "prompt_hash", "duration_seconds")},
                                   "attempts": [{k: attempt.get(k) for k in ("attempt_no", "status", "provider_error", "error_code")}
                                                for attempt in call["retries"]]})
            for item in call["usage"]:
                public = {k: item.get(k) for k in ("model_call_id", "status", "model", "input_tokens", "output_tokens")}
                key = public["model_call_id"]
                assert key, "Judge usage must identify its observed provider call"
                if key in judge_usage:
                    assert judge_usage[key] == public
                judge_usage[key] = public
    # Failed continuations and uncollected sibling outputs also consumed calls.
    all_judge_usage = dict(judge_usage)
    for path in sorted((root / "judge").glob("*/llm/**/result.json")):
        for row in _usage_rows(json.loads(path.read_text())):
            public = {k: row.get(k) for k in ("model_call_id", "status", "model", "input_tokens", "output_tokens")}
            key = public["model_call_id"]
            assert key, "Raw judge usage must identify its provider call"
            if key in all_judge_usage:
                assert all_judge_usage[key] == public
            all_judge_usage[key] = public
    judge_calls = sum(r["parent_status"] == "pairs" for r in judge_receipts)
    return {"schema": "paper1.a4.analysis.v1", "model": manifest["identity"]["model"],
            "identity": manifest["identity"], "namespace": manifest["namespace"], "source_hashes": source_hashes,
            "metrics": metrics, "rounds": rounds, "routes": dict(routes), "transitions": dict(transitions),
            "candidate_flows": dict(sorted(flows.items())), "true_origins": dict(true_origins),
            "d_transitions": dict(d_changes), "matched_wording_changed": wording_changed,
            "matched_semantic_assessment_changed": semantic_changed, "stage_statuses": dict(diagnostics),
            "calls": {"terminal_final_layout": calls, "cached_terminal_final_layout": reused_calls,
                      "outer_runtime_attempts_final_layout": attempts, "real_terminal_all_attempts": real_terminal_calls,
                      "outer_runtime_attempts_all": runtime_attempts, "saved_cell_attempts": saved_attempts,
                      "failed_cell_attempts": failed_attempts, "transport_retry_events": transport_retries,
                      "schema_failures_final_layout": schema_failures, "residual_judge_completed_receipts": judge_calls,
                      "residual_judge_observed_model_calls": len(judge_usage),
                      "residual_judge_observed_model_calls_all_artifacts": len(all_judge_usage)},
            "errors": errors, "cells": cells, "candidates": candidates, "publications": publications,
            "examples": examples, "usage": list(usage.values()),
            "judge_batches": judge_receipts,
            "judge_observed_usage": list(judge_usage.values()),
            "judge_all_artifact_usage": list(all_judge_usage.values()),
            "hit_changes": hit_changes, "precision_decomposition": decomposition,
            "paired_by_pair": pair_deltas,
            "scope": "Conditional terminal intervention; paired by pair across all three rounds. No significance interval or population-independence claim."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if "final_results" in args.output.resolve().parts:
        parser.error("Derived analysis must stay outside frozen final_results")
    result = analyze(args.root.resolve())
    write_json(args.output, result)
    print(json.dumps({k: result[k] for k in ("model", "routes", "rounds", "calls")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
