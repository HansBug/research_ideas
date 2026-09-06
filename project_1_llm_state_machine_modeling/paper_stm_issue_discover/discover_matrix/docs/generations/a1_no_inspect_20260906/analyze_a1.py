"""Provider-free A1/v61 arithmetic over frozen, source-linked report outcomes."""

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import random


PAPER = Path(__file__).resolve().parents[4]


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def digest(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ratio(n, d):
    return {"numerator": n, "denominator": d, "rate": n / d if d else None}


def calculate(reports, items):
    counts = Counter(r["validity"] for r in reports)
    assert set(counts) <= {"VALID_KNOWN", "VALID_NOVEL", "INVALID"}
    full = {(e, r["round"]) for r in reports if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    supported = {(e, r["round"]) for r in reports if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"] + r["partial_ledger_ids"]}
    assert all(e in items and rnd in (1, 2, 3) for e, rnd in full | supported)

    def hit_view(units, eligible):
        selected = {(e, rnd) for e, rnd in units if e in eligible}
        rounds = {rnd: sum(r == rnd for _, r in selected) for rnd in (1, 2, 3)}
        ids = {e for e, _ in selected}
        return {"hit1": ratio(len(selected), 3 * len(eligible)),
                "hit3": ratio(len(ids), len(eligible)),
                "hitall": ratio(sum(all((e, r) in selected for r in (1, 2, 3)) for e in ids), len(eligible)),
                "per_round": rounds}

    strict = [r for r in reports if r["validity"] != "INVALID" and r["d_tier"] in ("D1", "D2")]
    strict_units = {(e, r["round"]) for r in strict if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    by_pair = defaultdict(list)
    for r in reports:
        by_pair[r["pair_id"]].append(r)
    per_pair = {p: ratio(sum(r["validity"] != "INVALID" for r in rows), len(rows)) for p, rows in sorted(by_pair.items())}
    # Preserve the historical finding-level arithmetic for comparability. One
    # multi-target report may support several units; report precision is primary.
    unit_reports = defaultdict(set)
    for r in reports:
        if r["validity"] == "VALID_KNOWN":
            for e in r["full_ledger_ids"]:
                unit_reports[e, r["round"]].add(r["original_report_id"])
    duplicate_memberships = sum(len(rids) - 1 for rids in unit_reports.values())
    return {
        "reports": len(reports), "K": counts["VALID_KNOWN"], "N": counts["VALID_NOVEL"], "I": counts["INVALID"],
        "precision": ratio(counts["VALID_KNOWN"] + counts["VALID_NOVEL"], len(reports)),
        **hit_view(full, items), "supported": hit_view(supported, items),
        "tiers": {level: hit_view(full, {e for e, row in items.items() if row["L"] == level}) for level in ("L0", "L1", "L2")},
        "strict": {"precision": ratio(len(strict), len(reports)), **hit_view(strict_units, items)},
        "D_A": dict(Counter(r["d_tier"] or r["a0_subtype"] for r in reports)),
        "per_pair_precision": per_pair,
        "per_pair_precision_mean": sum(x["rate"] for x in per_pair.values()) / len(per_pair) if per_pair else None,
        "finding_precision_historical": ratio(counts["VALID_KNOWN"] + counts["VALID_NOVEL"] - duplicate_memberships, len(reports) - duplicate_memberships),
        "finding_precision_caveat": "Historical FULL-unit membership deduplication, not cross-round semantic root-cause adjudication.",
    }



def vector(data, items):
    metrics = calculate(data, items)
    return {**{k: metrics[k] for k in ("hit1", "hit3", "hitall", "precision")},
            **{"L2_" + k: metrics["tiers"]["L2"][k] for k in ("hit1", "hit3", "hitall")}}


def compare(a1, v61, items):
    assert a1["coverage"]["judged_cells"] == a1["coverage"]["eligible_cells"] == 162
    assert a1["coverage"]["unjudged_reports"] == 0
    clusters = sorted({i["pair_context"]["nl_sha8"] for i in items.values()})
    assert len(clusters) == 9
    rows = []
    for cluster in clusters:
        subitems = {e: i for e, i in items.items() if i["pair_context"]["nl_sha8"] == cluster}
        rows.append({label: vector([r for r in data["reports"] if r["nl_cluster"] == cluster], subitems)
                     for label, data in (("a1", a1), ("v61", v61))})
    keys = tuple(rows[0]["a1"])

    def difference(indices):
        rates = {}
        for label in ("a1", "v61"):
            rates[label] = {}
            for key in keys:
                n = sum(rows[i][label][key]["numerator"] for i in indices)
                d = sum(rows[i][label][key]["denominator"] for i in indices)
                rates[label][key] = n / d if d else None
        return {k: 100 * (rates["a1"][k] - rates["v61"][k])
                if rates["a1"][k] is not None and rates["v61"][k] is not None else None for k in keys}

    rng = random.Random(20260906)
    samples = [difference(rng.choices(range(9), k=9)) for _ in range(10000)]
    intervals = {}
    for key in keys:
        values = sorted(s[key] for s in samples if s[key] is not None)
        intervals[key] = {"percentile_2_5": values[int(.025 * (len(values) - 1))],
                          "percentile_97_5": values[int(.975 * (len(values) - 1))], "defined_replicates": len(values)}
    left = {(e, r["round"]) for r in a1["reports"] if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
    right = {(e, r["round"]) for r in v61["reports"] if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}

    def changed(units, source):
        return [{"ledger_id": e, "round": rnd, "pair_id": items[e]["pair"], "L": items[e]["L"],
                 "supporting_reports": [{k: r.get(k) for k in ("original_report_id", "title", "property", "predicate_id", "witness_level", "source_divergence", "method_cell")}
                    for r in source["reports"] if r["round"] == rnd and e in r["full_ledger_ids"]]}
                for e, rnd in sorted(units)]

    return {"scope": "A1 versus immutable v61; historical version/provider-time differences remain; not a pure single-factor causal estimate",
        "delta_pp": difference(range(9)), "cluster_bootstrap_95pct": intervals,
        "bootstrap_seed": 20260906, "bootstrap_replicates": 10000,
        "per_cluster_delta_pp": {c: difference([i]) for i, c in enumerate(clusters)},
        "leave_one_cluster_out_delta_pp": {c: difference([j for j in range(9) if j != i]) for i, c in enumerate(clusters)},
        "lost": changed(right - left, v61), "gained": changed(left - right, a1),
        "lost_by_tier": dict(Counter(items[e]["L"] for e, _ in right-left)),
        "gained_by_tier": dict(Counter(items[e]["L"] for e, _ in left-right))}


def validate(data, items):
    assert len(items) == 145
    assert Counter(i["L"] for i in items.values()) == {"L0": 71, "L1": 35, "L2": 39}
    for label in ("a1", "v61"):
        arm = data[label]
        cells = {(c["pair_id"], c["round"]) for c in arm["cells"]}
        pairs = {p for p, _ in cells}
        assert len(pairs) == 54 and cells == {(p, r) for p in pairs for r in (1, 2, 3)}
        assert len(arm["cells"]) == arm["coverage"]["judged_cells"] == 162
        assert arm["coverage"]["planned_cells"] == arm["coverage"]["eligible_cells"] == 162
        assert arm["coverage"]["planned_expected_rounds"] == 435
        assert arm["coverage"]["unjudged_reports"] == 0
        reports = {r["original_report_id"]: r for r in arm["reports"]}
        assert len(reports) == len(arm["reports"]) == sum(c["reports"] for c in arm["cells"])
        per_cell = Counter((r["pair_id"], r["round"]) for r in reports.values())
        assert set(per_cell) <= cells, "reports outside the planned cells"
        assert all(per_cell[c["pair_id"], c["round"]] == c["reports"] for c in arm["cells"]), "per-cell report coverage"
        expected = {(r["ledger_id"], r["round"]): r for r in arm["expected"]}
        assert len(expected) == len(arm["expected"]) == 435
        assert set(expected) == {(e, r) for e in items for r in (1, 2, 3)}
        for (eid, rnd), row in expected.items():
            assert row["pair_id"] == items[eid]["pair"] and row["L"] == items[eid]["L"]
            selected = [r for r in reports.values() if r["pair_id"] == row["pair_id"] and r["round"] == rnd
                        and r["validity"] == "VALID_KNOWN"]
            full = {r["original_report_id"] for r in selected if eid in r["full_ledger_ids"]}
            partial = {r["original_report_id"] for r in selected if eid in r["partial_ledger_ids"]}
            assert full == set(row["full_report_ids"]) and partial == set(row["partial_report_ids"])
            assert row["hit"] == bool(full) and row["supported"] == bool(full | partial)
        actual = json.loads(json.dumps(calculate(arm["reports"], items)))
        assert actual == arm["metrics"], (label, "stored metrics differ from outcomes")
    actual = compare(data["a1"], data["v61"], items)
    assert actual == data["comparison"], "historical paired comparison differs from outcomes"
    return {label: data[label]["metrics"] for label in ("a1", "v61")}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path,
                        default=PAPER / "final_results/a1_no_inspect_vs_v61_20260906")
    args = parser.parse_args()
    manifest = read(args.archive / "archive_manifest.json")
    for name, expected_hash in manifest["files"].items():
        assert digest(args.archive / name) == expected_hash, name
    data = read(args.archive / "results.json")
    ledger = PAPER / "discover_matrix/ledger_v2/ledger.json"
    assert digest(ledger) == data["a1"]["ledger_hash"] == data["v61"]["ledger_hash"]
    metrics = validate(data, read(ledger)["items"])
    print(json.dumps({"status": "verified_offline_arithmetic", "metrics": metrics,
                      "delta_pp": data["comparison"]["delta_pp"],
                      "scope": "Recomputes saved judge decisions; no provider calls or re-adjudication."},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
