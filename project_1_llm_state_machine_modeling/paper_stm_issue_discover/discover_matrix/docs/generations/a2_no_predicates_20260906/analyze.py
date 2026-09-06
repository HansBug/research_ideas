"""Offline A2/v61 accounting. Never calls a provider or changes source records."""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np


HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[3]
spec = importlib.util.spec_from_file_location("v61_metrics", HERE.parent / "v61/evaluate_full.py")
v61 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v61)
KNI = {"VALID_KNOWN": "K", "VALID_NOVEL": "N", "INVALID": "I"}


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path):
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def ratio(n, d):
    return dict(numerator=n, denominator=d, rate=n / d if d else None)


def quality(reports, items):
    converted = {r["original_report_id"]: dict(pair=r["pair_id"], round=f"r{r['round']}",
                  **{"class": KNI[r["validity"]]}, full=r["full_ledger_ids"], partial=r["partial_ledger_ids"])
                 for r in reports}
    assert len(converted) == len(reports)
    m = v61.metrics(converted, items, 162, "offline")
    strict = [r for r in reports if r["validity"] != "INVALID" and r["d_tier"] in {"D1", "D2"}]
    strict_ids = {r["original_report_id"] for r in strict}
    sm = v61.metrics({k: r for k, r in converted.items() if k in strict_ids}, items, 162, "strict")
    return dict(
        reports=m["reports"], K=m["K"], N=m["N"], I=m["I"],
        precision=ratio(m["K"] + m["N"], m["reports"]),
        hit1=ratio(m["hit1"], 3 * len(items)), hit3=ratio(m["hit3"], len(items)), hitall=ratio(m["hitall"], len(items)),
        tiers={k: dict(hit1=ratio(u, d), hit3=ratio(h3, d // 3), hitall=ratio(ha, d // 3)) for k, (u, d, h3, ha) in m["per_l"].items()},
        strict=dict(precision=ratio(len(strict), len(reports)), hit1=ratio(sm["hit1"], 3 * len(items)),
                    hit3=ratio(sm["hit3"], len(items)), hitall=ratio(sm["hitall"], len(items))),
        D_A=dict(Counter(r["d_tier"] or r["a0_subtype"] for r in reports)),
    )


def load_selection(path):
    plan = read(path)
    assert plan["schema"] == "a2.transport-continuation.v1"
    root = Path(plan["root"])
    manifest = read(root / "run_manifest.json")
    assert plan["run_id"] == manifest["run_id"] == root.name
    assert plan["identity"]["source_provenance"] == manifest["source_provenance"]
    assert plan["identity"]["run_contract_hash"] == manifest["run_contract_hash"]
    assert manifest["ablation"] == "no-predicates" and manifest["rounds"] == 3
    roots = [Path(p) for p in plan["source_roots"]] + [root]
    assert len(set(p.resolve() for p in roots)) == len(roots)
    frozen = ("ablation", "selected_pair_ids", "rounds", "model_config_hash", "prompt_schema_hash",
              "input_data_hash", "pair_input_hashes", "registry_hash")
    for source in roots:
        other = read(source / "run_manifest.json")
        assert all(other[name] == manifest[name] for name in frozen), ("continuation identity drift", source)
    expected = {(p, r) for p in manifest["selected_pair_ids"] for r in (1, 2, 3)}
    selection = {}
    for row in plan["selection"]:
        key = (row["pair_id"], row["round"])
        assert key in expected and key not in selection
        assert row["action"] in {"reuse", "recover"}
        if row["old_path"]:
            old = Path(row["old_path"])
            assert old.parents[2].resolve() in {p.resolve() for p in roots[:-1]}
            assert digest(old) == row["old_hash"], ("frozen predecessor changed", old)
        if row["action"] == "reuse":
            assert row["old_path"] and row["old_hash"]
            selected, expected_hash = Path(row["old_path"]), row["old_hash"]
        else:
            selected, expected_hash = root / "method" / key[0] / f"round-{key[1]}.json", None
        assert selected.parent.name == key[0] and selected.name == f"round-{key[1]}.json"
        selection[key] = dict(path=selected.resolve(), expected_hash=expected_hash, action=row["action"])
    assert set(selection) == expected and len(expected) == plan["planned_cells"] == 162
    return roots, selection, {str(path): digest(path)}


def load_cells(roots, *, historical=False, selection=None):
    cells, reports, quarantined, hashes, attempts = {}, {}, [], {}, []
    for root in roots:
        manifest = read(root / "run_manifest.json")
        hashes[str(root / "run_manifest.json")] = digest(root / "run_manifest.json")
        for path in sorted((root / "method").glob("*/round-*.json")):
            raw = read(path)
            key = (raw["pair_id"], raw["round"])
            hashes[str(path)] = digest(path)
            assert raw["status"] in {"completed", "completed_with_diagnostics", "failed_with_receipt"}
            if historical and not raw["eligible"]:
                assert key == ("0045", 1) and raw["status"] == "failed_with_receipt"
                attempts.append(dict(pair_id=key[0], round=key[1], path=str(path), status=raw["status"], errors=raw.get("errors", [])))
                continue
            if not historical:
                assert raw["ablation"] == manifest["ablation"] == "no-predicates"
                assert raw["run_id"] == manifest["run_id"]
                assert raw["run_contract_hash"] == manifest["run_contract_hash"]
                assert raw["source_provenance"] == manifest["source_provenance"]
                assert raw["pair_input_hash"] == manifest["pair_input_hashes"][key[0]]
                assert raw["predicate_execution_receipts"] == []
            if selection is not None:
                assert not historical and key in selection
                chosen = selection[key]
                if path.resolve() != chosen["path"]:
                    attempts.append(dict(pair_id=key[0], round=key[1], path=str(path), status=raw["status"],
                                         errors=raw.get("errors", []), selection="preserved_predecessor_attempt"))
                    continue
                assert chosen["expected_hash"] is None or digest(path) == chosen["expected_hash"]
            assert key not in cells, ("duplicate method cell", key)
            stage = raw.get("stage_outputs", {})
            execute = stage.get("execute_batch", {})
            divergence = {c["canonical_contract_id"] for c in execute.get("frontier_batch", {}).get("checks", []) if c.get("kind") == "source_divergence"}
            cells[key] = dict(pair_id=key[0], round=key[1], status=raw["status"], eligible=raw["eligible"],
                              source=str(path), reports=len(raw["report_issue_clusters"]), errors=raw.get("errors", []),
                              input_hashes=raw.get("input_hashes", {}),
                              degraded=raw["status"] != "completed" or bool(raw.get("errors")),
                              publish=stage.get("publish"),
                              receipt_count=len(raw["predicate_execution_receipts"]))
            for row in raw["report_issue_clusters"]:
                rid = row["issue_id"]
                record = {name: row.get(name) for name in (
                    "title", "property", "violation_direction", "locus_names", "expected", "observed", "candidate_reason",
                    "candidate_basis", "contract_id", "predicate_id", "witness_level", "source_refs", "element_refs",
                    "binding", "folded_sub_claims", "contract_ids", "facet_issue_ids")}
                record.update(original_report_id=rid, pair_id=key[0], round=key[1], method_source=str(path),
                              source_divergence=row["contract_id"] in divergence)
                if raw["eligible"]:
                    assert rid not in reports
                    reports[rid] = record
                else:
                    quarantined.append(record)
    return cells, reports, quarantined, hashes, attempts


def load_judges(roots, cells, method_reports, items):
    reports, expected, judged, hashes, failures = {}, {}, set(), {}, []
    for root in roots:
        manifest = read(root / "run_manifest.json")
        hashes[str(root / "run_manifest.json")] = digest(root / "run_manifest.json")
        assert manifest["judge_algorithm_version"] == "semantic-judge.two-stage.v3.11"
        assert manifest["protocol_sha256"] == "d774d9bd3e4c4fe04735ed1d4ec064be197cfadcd52e21c8226e37175b29b210"
        assert manifest["k_closure"] == "relation_first" and manifest["closure_profile"] == "full"
        assert manifest["validity_readings"] == 2 and manifest["validity_aggregation"] == "arbitration"
        assert manifest["validity_arbitration_trigger"] == "any" and manifest["model_profile"] == "gpt-5.6-luna"
        assert manifest.get("report_filter_path") is None
        selected_cells = {(p, r) for p in manifest["selected_pair_ids"] for r in manifest["selected_rounds"]}
        assert selected_cells <= set(cells)
        for path in sorted((root / "failures").glob("*.json")):
            failure = read(path)
            key = (failure["pair_id"], failure["round"])
            assert key in selected_cells and cells[key]["eligible"]
            hashes[str(path)] = digest(path)
            failures.append(dict(source=str(path), run_id=manifest["run_id"], **failure))
        for path in sorted((root / "pairs").glob("*.json")):
            raw = read(path)
            key = (raw["pair_id"], raw["round"])
            assert raw["run_id"] == manifest["run_id"] and key in selected_cells
            assert key in cells and key not in judged, ("unexpected/duplicate judge cell", key)
            assert cells[key]["eligible"] and raw["status"] == "completed"
            hashes[str(path)] = digest(path)
            assert raw["adapter_audit"]["source_hash"] == digest(Path(cells[key]["source"]))
            selected = {rid for rid, r in method_reports.items() if (r["pair_id"], r["round"]) == key}
            assert {r["original_report_id"] for r in raw["report_outcomes"]} == selected, ("report denominator", key)
            judged.add(key)
            local = {}
            for outcome in raw["report_outcomes"]:
                rid = outcome["original_report_id"]
                assert rid not in reports and outcome["validity"] in KNI
                assert set(outcome["full_ledger_ids"]).isdisjoint(outcome["partial_ledger_ids"])
                assert outcome["validity"] == "VALID_KNOWN" or not (outcome["full_ledger_ids"] or outcome["partial_ledger_ids"])
                assert all(items[e]["pair"] == key[0] for e in outcome["full_ledger_ids"] + outcome["partial_ledger_ids"])
                reports[rid] = {**method_reports[rid], **outcome, "judge_source": str(path)}
                local[rid] = outcome
            assert {e["ledger_id"] for e in raw["expected_outcomes"]} == {e for e, item in items.items() if item["pair"] == key[0]}
            for e in raw["expected_outcomes"]:
                full = {rid for rid, r in local.items() if e["ledger_id"] in r["full_ledger_ids"]}
                partial = {rid for rid, r in local.items() if e["ledger_id"] in r["partial_ledger_ids"]}
                assert full == set(e["full_report_ids"]) and partial == set(e["partial_report_ids"])
                assert e["hit"] == bool(full) and e["supported"] == bool(full | partial)
                expected[e["ledger_id"], key[1]] = e
    return reports, expected, judged, hashes, failures


def summarize(label, cells, method_reports, reports, expected, judged, items, clusters):
    grid = {(p, r) for p in clusters for r in (1, 2, 3)}
    assert set(cells) == grid, ("incomplete method grid", sorted(grid - set(cells)))
    unjudged = set(method_reports) - set(reports)
    metrics = quality(list(reports.values()), items)
    valid = metrics["K"] + metrics["N"]
    # An unjudged report is unknown, never an implicit invalid report.
    precision_bounds = [ratio(valid, len(method_reports))["rate"], ratio(valid + len(unjudged), len(method_reports))["rate"]]
    rows = []
    for eid, item in sorted(items.items()):
        for rnd in (1, 2, 3):
            cell = cells[item["pair"], rnd]
            outcome = expected.get((eid, rnd))
            rows.append(dict(ledger_id=eid, pair_id=item["pair"], round=rnd, L=item["L"], nl_cluster=clusters[item["pair"]],
                             observed=outcome is not None, hit=outcome["hit"] if outcome else None,
                             supported=outcome["supported"] if outcome else None,
                             full_report_ids=outcome["full_report_ids"] if outcome else [],
                             partial_report_ids=outcome["partial_report_ids"] if outcome else [],
                             method_status=cell["status"], degraded=cell["degraded"],
                             missing_reason=None if outcome else ("method_ineligible" if not cell["eligible"] else "judge_incomplete")))
    assert len(rows) == 435
    hits = sum(r["hit"] is True for r in rows)
    assert hits == metrics["hit1"]["numerator"]
    unknown = sum(not r["observed"] for r in rows)
    eligible = {k for k, c in cells.items() if c["eligible"]}
    by_issue = defaultdict(list)
    for row in rows:
        by_issue[row["ledger_id"]].append(row["hit"])
    hit_bounds = dict(
        hit1=[hits / 435, (hits + unknown) / 435],
        hit3=[sum(any(v is True for v in values) for values in by_issue.values()) / 145,
              sum(any(v is not False for v in values) for values in by_issue.values()) / 145],
        hitall=[sum(all(v is True for v in values) for values in by_issue.values()) / 145,
                sum(all(v is not False for v in values) for values in by_issue.values()) / 145],
    )
    per_round = {}
    for rnd in (1, 2, 3):
        q = quality([r for r in reports.values() if r["round"] == rnd], items)
        per_round[str(rnd)] = {**{k: q[k] for k in ("reports", "K", "N", "I", "precision")},
                               "hit": ratio(q["hit1"]["numerator"], len(items)),
                               "strict_hit": ratio(q["strict"]["hit1"]["numerator"], len(items))}
    return dict(label=label, metrics=metrics, cells=list(cells.values()), reports=list(reports.values()), expected=rows,
                coverage=dict(planned_cells=162, terminal_cells=len(cells), statuses=dict(Counter(c["status"] for c in cells.values())),
                              eligible_cells=len(eligible), judged_cells=len(judged), missing_judge_cells=[list(k) for k in sorted(eligible - judged)],
                              eligible_reports=len(method_reports), judged_reports=len(reports), unjudged_reports=sorted(unjudged),
                              quarantined_report_count=sum(c["reports"] for c in cells.values() if not c["eligible"]),
                              planned_expected_rounds=435, observed_expected_rounds=435-unknown, unknown_expected_rounds=unknown,
                              degraded_expected_rounds=sum(r["degraded"] for r in rows),
                              hit_bounds_with_unknown_cells=hit_bounds,
                              hit1_upper_if_degraded_or_unknown_misses_were_hits=(hits + sum(r["hit"] is not True and (r["degraded"] or not r["observed"]) for r in rows)) / 435,
                              precision_bounds_on_eligible_emitted_reports=precision_bounds),
                precision_complete=not unjudged and eligible <= judged,
                metric_interpretation="Observed outcomes on the fixed planned denominator; missing cells are not normal zero-report cells. Degradation bounds include all diagnostics and do not attribute them to transport.",
                per_round=per_round,
                per_cluster={c: quality([r for r in reports.values() if clusters[r["pair_id"]] == c],
                                        {e: i for e, i in items.items() if clusters[i["pair"]] == c}) for c in sorted(set(clusters.values()))},
                per_pair={p: quality([r for r in reports.values() if r["pair_id"] == p],
                                     {e: i for e, i in items.items() if i["pair"] == p}) for p in sorted(clusters)})


def paired_uncertainty(current, reference):
    names = sorted(current["per_cluster"])
    assert len(names) == 9 and names == sorted(reference["per_cluster"])
    draws = np.random.default_rng(20260906).integers(0, 9, size=(10000, 9))
    out = {}
    for metric in ("hit1", "hit3", "hitall", "precision"):
        arrays = [np.asarray([[a["per_cluster"][c][metric]["numerator"], a["per_cluster"][c][metric]["denominator"]] for c in names], dtype=float) for a in (current, reference)]
        totals = [a.sum(axis=0) for a in arrays]
        point = totals[0][0] / totals[0][1] - totals[1][0] / totals[1][1] if all(t[1] for t in totals) else None
        sampled = [a[draws].sum(axis=1) for a in arrays]
        rates = [np.divide(a[:, 0], a[:, 1], out=np.full(len(a), np.nan), where=a[:, 1] != 0) for a in sampled]
        deltas = rates[0] - rates[1]
        defined = deltas[np.isfinite(deltas)]
        leave = {}
        for i, c in enumerate(names):
            left = [total - a[i] for total, a in zip(totals, arrays)]
            leave[c] = left[0][0] / left[0][1] - left[1][0] / left[1][1] if all(t[1] for t in left) else None
        out[metric] = dict(a2_minus_v61=point, percentile95=np.quantile(defined, [.025, .975]).tolist() if len(defined) else None,
                           defined_replicates=len(defined), undefined_replicates=len(deltas)-len(defined), leave_one_cluster_out=leave)
    return dict(seed=20260906, replicates=10000, clusters=names, metrics=out,
                interpretation="Nine paired NL clusters; descriptive uncertainty cannot remove version, provider-time, missingness, or Judge-time differences.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--v61-archive", type=Path, default=PAPER / "final_results/v61_source_divergence_vs_x1v2_baseline")
    parser.add_argument("--ledger", type=Path, default=PAPER / "discover_matrix/ledger_v2/ledger.json")
    parser.add_argument("--report-root", type=Path, required=True)
    parser.add_argument("--a2-root", type=Path)
    parser.add_argument("--a2-selection", type=Path)
    parser.add_argument("--a2-judge-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    items = read(args.ledger)["items"]
    assert len(items) == 145 and Counter(i["L"] for i in items.values()) == {"L0": 71, "L1": 35, "L2": 39}
    vr = args.v61_archive / "raw"
    vc, vm, vq, vh, va = load_cells([vr / "v61_current/method", vr / "v61_current_fill0045"], historical=True)
    assert not vq and len(vc) == 162 and len(vm) == 903 and len(va) == 1
    clusters = {p: hashlib.sha256((args.report_root / "pairs" / p / "nl.txt").read_bytes()).hexdigest()[:8] for p, _ in vc}
    assert sorted(Counter(clusters.values()).values()) == [6] * 9
    assert all(clusters[i["pair"]] == i["pair_context"]["nl_sha8"] for i in items.values())
    vj, ve, vseen, vjh, vf = load_judges(sorted((vr / "judge_v3.11_iter6cfg").glob("current-r*")), vc, vm, items)
    result = dict(schema="paper1.a2-v61-analysis.v1", human_confirmations=0, ledger_hash=digest(args.ledger),
                  v61=summarize("frozen_v61_ours", vc, vm, vj, ve, vseen, items, clusters),
                  historical_replaced_attempts=va, historical_judge_failures=vf, source_hashes={**vh, **vjh})
    m = result["v61"]["metrics"]
    assert [m[k] for k in ("reports", "K", "N", "I")] == [903, 561, 198, 144]
    assert [m[k]["numerator"] for k in ("hit1", "hit3", "hitall")] == [323, 130, 82]
    assert m["strict"]["precision"]["numerator"] == 678 and m["strict"]["hit1"]["numerator"] == 294
    assert len(vseen) == 162 and len(vj) == 903
    assert not (args.a2_root and args.a2_selection), "choose one A2 source mode"
    if args.a2_root or args.a2_selection:
        roots, selection, selection_hashes = load_selection(args.a2_selection) if args.a2_selection else ([args.a2_root], None, {})
        ac, am, aq, ah, aa = load_cells(roots, selection=selection)
        aj, ae, aseen, ajh, af = load_judges(args.a2_judge_root, ac, am, items)
        result["a2"] = summarize("a2_no_predicates", ac, am, aj, ae, aseen, items, clusters)
        result["quarantined_reports"] = aq
        result["a2_judge_failures"] = af
        result["a2_predecessor_attempts"] = aa
        result["a2_source_selection"] = {"plan": str(args.a2_selection) if args.a2_selection else None,
                                         "roots": [str(p) for p in roots]}
        result["input_comparison"] = [dict(pair_id=p, round=r, differences={name: dict(a2=value, v61=vc[p, r]["input_hashes"].get(name))
                                      for name, value in cell["input_hashes"].items() if value != vc[p, r]["input_hashes"].get(name)})
                                      for (p, r), cell in sorted(ac.items())]
        result["source_hashes"].update({**ah, **ajh, **selection_hashes})
        result["paired_uncertainty"] = paired_uncertainty(result["a2"], result["v61"]) if aj else None
        full = {(r["ledger_id"], r["round"]): r for r in result["v61"]["expected"]}
        result["changes"] = [dict(**r, v61_hit=full[r["ledger_id"], r["round"]]["hit"],
                                  v61_full_report_ids=full[r["ledger_id"], r["round"]]["full_report_ids"],
                                  change="unobserved" if r["hit"] is None else "lost" if not r["hit"] else "gained")
                             for r in result["a2"]["expected"] if r["hit"] != full[r["ledger_id"], r["round"]]["hit"]]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({label: result[label]["metrics"] for label in ("v61", "a2") if label in result}, indent=2))


if __name__ == "__main__":
    main()
