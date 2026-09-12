"""v61 RQ2/RQ3 与附录 C 的规范复算脚本（judge 口径，两臂同一 judge）。

从 final_results/v61_source_divergence_vs_x1v2_baseline 的归档数据复算：
无效报告构成、N/K 的 D 构成、逐对有效率范围（RQ2）；FULL 命中单元的 W 分布、
报告级 W、谓词回执与绑定、仅由分歧审计报告承载的命中单元（RQ3）；逐轮命中与
L1 逐条对照表（附录 C）。用法::

    venv/bin/python <this file> [--archive <archive root>] [--out <derived dir>]
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ARCHIVE = os.path.join(P1, "final_results", "v61_source_divergence_vs_x1v2_baseline")
LEDGER = os.path.join(P1, "discover_matrix", "ledger_v2", "ledger.json")
ROUNDS = ("r1", "r2", "r3")
TIERS = ("L0", "L1", "L2")


def load_judge(root: str, side: str) -> dict:
    out = {}
    for f in glob.glob(f"{root}/{side}-r*/pairs/*.json"):
        d = json.load(open(f))
        for o in d.get("report_outcomes") or []:
            out[o["original_report_id"]] = {
                "round": f"r{d['round']}",
                "pair": o["original_report_id"].split(":")[0],
                "v": o["validity"],
                "d": o.get("d_tier"),
                "a0": o.get("a0_subtype"),
                "full": list(o.get("full_ledger_ids") or []),
                "partial": list(o.get("partial_ledger_ids") or []),
            }
    return out


def load_method(archive: str) -> tuple[dict, dict, set, dict]:
    """返回 (clusters by issue_id, evidence by issue_id, divergence issue ids, receipts by cell)。"""
    clusters, evidence, divergence, receipts = {}, {}, set(), {}
    files = glob.glob(f"{archive}/raw/v61_current/method/method/*/round-*.json") + glob.glob(
        f"{archive}/raw/v61_current_fill0045/**/round-*.json", recursive=True
    )
    for f in files:
        d = json.load(open(f))
        if d["status"] != "completed":
            continue  # 0045 r1 原格失败，由 fill 目录的重采样格替代
        cell = (d["pair_id"], f"r{d['round']}")
        checks = d["stage_outputs"]["execute_batch"]["frontier_batch"]["checks"]
        div_contracts = {c["canonical_contract_id"] for c in checks if c.get("kind") == "source_divergence"}
        for c in d["report_issue_clusters"]:
            clusters[c["issue_id"]] = c
            if c.get("contract_id") in div_contracts:
                divergence.add(c["issue_id"])
        for e in d.get("evidence_records") or []:
            evidence[e["issue_id"]] = e
        receipts[cell] = d.get("predicate_execution_receipts") or []
    return clusters, evidence, divergence, receipts


def pct(a: int, b: int) -> str:
    return f"{a}/{b}={100.0 * a / b:.1f}%" if b else f"{a}/0"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", default=ARCHIVE)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    out_dir = args.out or os.path.join(args.archive, "derived")
    items = json.load(open(LEDGER))["items"]
    tier = {k: v["L"] for k, v in items.items()}
    jroot = os.path.join(args.archive, "raw", "judge_v3.11_iter6cfg")
    arms = {"v61": load_judge(jroot, "current"), "baseline": load_judge(jroot, "baseline")}
    clusters, evidence, divergence, receipts = load_method(args.archive)
    publish_folded = publish_agg_members = 0
    for f in glob.glob(f"{args.archive}/raw/v61_current/method/method/*/round-*.json") + glob.glob(
        f"{args.archive}/raw/v61_current_fill0045/**/round-*.json", recursive=True
    ):
        d = json.load(open(f))
        if d["status"] == "completed":
            publish_folded += d["stage_outputs"]["publish"].get("folded_issue_count", 0)
            publish_agg_members += d["stage_outputs"]["publish"].get("guard_modality_aggregated_count", 0)
    lines: list[str] = []
    say = lines.append

    say("# v61 RQ2 / RQ3 / 附录 C 复算（judge 口径）")
    for arm, jd in arms.items():
        n = len(jd)
        v = Counter(o["v"] for o in jd.values())
        da = Counter(o["d"] or o["a0"] for o in jd.values())
        k_by_d = Counter(o["d"] for o in jd.values() if o["v"] == "VALID_KNOWN")
        n_by_d = Counter(o["d"] for o in jd.values() if o["v"] == "VALID_NOVEL")
        per_pair = defaultdict(Counter)
        for o in jd.values():
            per_pair[o["pair"]][o["v"] != "INVALID"] += 1
        rates = [c[True] / (c[True] + c[False]) for c in per_pair.values()]
        say(f"\n## {arm}: reports={n}; K/N/I={v['VALID_KNOWN']}/{v['VALID_NOVEL']}/{v['INVALID']}; "
            f"precision={pct(v['VALID_KNOWN'] + v['VALID_NOVEL'], n)}")
        say(f"D2/D1/D0/FP/NADC = {da['D2']}/{da['D1']}/{da['D0']}/{da['FALSE_POSITIVE']}/{da['NOT_A_DEFECT_CLAIM']}")
        say(f"K by D: {dict(k_by_d)}; N by D: {dict(n_by_d)}")
        say(f"per-pair validity rate: mean {100 * sum(rates) / len(rates):.1f}%, min {100 * min(rates):.0f}%, "
            f"max {100 * max(rates):.0f}%, pairs {len(rates)}")
        # hits
        full_units = {(e, o["round"]) for o in jd.values() if o["v"] == "VALID_KNOWN" for e in o["full"] if e in tier}
        per_round = {r: len({e for e, rr in full_units if rr == r}) for r in ROUNDS}
        say(f"FULL hit@1 = {pct(len(full_units), 435)}; per round {per_round}")
        for L in TIERS:
            n_ids = sum(1 for x in tier.values() if x == L)
            u = {(e, r) for e, r in full_units if tier[e] == L}
            ids = {e for e, _ in u}
            allr = {e for e in ids if all((e, r) in u for r in ROUNDS)}
            pr = {r: len({e for e, rr in u if rr == r}) for r in ROUNDS}
            say(f"  {L}: hit@1 {pct(len(u), 3 * n_ids)}; hit@3 {pct(len(ids), n_ids)}; hit@all {pct(len(allr), n_ids)}; per round {pr}")
        ids3 = {e for e, _ in full_units}
        say(f"hit@3 = {pct(len(ids3), 145)}; hit@all = {pct(len({e for e in ids3 if all((e, r) in full_units for r in ROUNDS)}), 145)}")
        strict_valid = sum(1 for o in jd.values() if o["v"] != "INVALID" and o["d"] in ("D2", "D1"))
        strict_units = {(e, o["round"]) for o in jd.values() if o["v"] == "VALID_KNOWN" and o["d"] in ("D2", "D1") for e in o["full"] if e in tier}
        strict_ids = {e for e, _ in strict_units}
        say(f"D2/D1-only sensitivity: validity {pct(strict_valid, n)}; FULL hit@1 {pct(len(strict_units), 435)}; hit@3 {pct(len(strict_ids), 145)}; "
            f"hit@all {pct(len({e for e in strict_ids if all((e, r) in strict_units for r in ROUNDS)}), 145)}")
        low = sorted((c[True] / (c[True] + c[False]), p, c[True] + c[False]) for p, c in per_pair.items())[:4]
        say(f"lowest per-pair validity (rate, pair, n): {[(round(r, 2), p, m) for r, p, m in low]}")
        supported = {(e, o["round"]) for o in jd.values() if o["v"] == "VALID_KNOWN" for e in o["full"] + o["partial"] if e in tier}
        say(f"supported coverage: units {pct(len(supported), 435)}; ids {pct(len({e for e, _ in supported}), 145)}")

    # ---------- RQ3 on v61 ----------
    jd = arms["v61"]
    say("\n## RQ3 (v61)")
    w_reports = Counter(clusters[r]["witness_level"] for r in jd if r in clusters)
    say(f"report-level W (published reports): {dict(w_reports)} of {len([r for r in jd if r in clusters])}")
    unit_w_root: dict[tuple, str] = {}
    unit_w_sub: dict[tuple, str] = {}
    unit_div_only: dict[tuple, bool] = {}
    unit_families: dict[tuple, set] = defaultdict(set)
    for rid, o in jd.items():
        if o["v"] != "VALID_KNOWN" or rid not in clusters:
            continue
        c = clusters[rid]
        w_root = c["witness_level"]
        w_sub = w_root
        for sc in c.get("folded_sub_claims") or []:
            ev = evidence.get(sc["issue_id"])
            if ev and ev.get("witness_level") == "W2":
                w_sub = "W2"
        fam = c.get("predicate_id") or ("DIV" if rid in divergence else "SEM")
        for e in o["full"]:
            if e not in tier:
                continue
            u = (e, o["round"])
            unit_w_root[u] = "W2" if (unit_w_root.get(u) == "W2" or w_root == "W2") else w_root
            unit_w_sub[u] = "W2" if (unit_w_sub.get(u) == "W2" or w_sub == "W2") else w_sub
            unit_div_only[u] = unit_div_only.get(u, True) and (rid in divergence)
            unit_families[u].add(fam)
    tot = len(unit_w_root)
    say(f"FULL-hit units {tot}: W2 root-only {sum(1 for w in unit_w_root.values() if w == 'W2')}; "
        f"W2 incl. folded sub-claim receipts {sum(1 for w in unit_w_sub.values() if w == 'W2')}")
    for L in TIERS:
        us = [u for u in unit_w_root if tier[u[0]] == L]
        say(f"  {L}: units {len(us)}; W2 root-only {sum(1 for u in us if unit_w_root[u] == 'W2')}; "
            f"W2 incl. sub-claims {sum(1 for u in us if unit_w_sub[u] == 'W2')}; "
            f"divergence-only units {sum(1 for u in us if unit_div_only[u])}")
    say(f"divergence-only FULL-hit units (all K FULL reports for the unit are divergence-audit reports): "
        f"{sum(1 for v in unit_div_only.values() if v)}; divergence-audit reports published: {len([r for r in jd if r in divergence])}, "
        f"of which K/N/I = {Counter(jd[r]['v'] for r in jd if r in divergence)}")
    # full decomposition of FULL-hit units by W category (incl.-sub-claim reading)
    unit_reports: dict[tuple, list] = defaultdict(list)
    for rid, o in jd.items():
        if o["v"] == "VALID_KNOWN" and rid in clusters:
            for e in o["full"]:
                if e in tier:
                    unit_reports[(e, o["round"])].append(rid)
    wcat: Counter = Counter()
    wcat_L: dict = defaultdict(Counter)
    bound_w1_receipts: Counter = Counter()
    for u, rids in unit_reports.items():
        cs = [clusters[r] for r in rids]
        if any(c["witness_level"] == "W2" for c in cs):
            k = "W2 (root report)"
        elif any(evidence.get(sc["issue_id"], {}).get("witness_level") == "W2" for c in cs for sc in c.get("folded_sub_claims") or []):
            k = "W2 (via folded sub-claim receipt)"
        elif all(r in divergence for r in rids):
            k = "W1 divergence-only (no predicate by construction)"
        elif any(c.get("predicate_id") for c in cs):
            k = "W1 predicate bound, receipt not closed"
            for c in cs:
                if c.get("predicate_id"):
                    rc = c.get("execution_receipt") or {}
                    bound_w1_receipts[(c["predicate_id"], str(rc.get("terminal_state")))] += 1
        else:
            k = "W1 no predicate (semantic candidate)"
        wcat[k] += 1
        wcat_L[k][tier[u[0]]] += 1
    say("FULL-hit units by W category (incl.-sub-claim reading): " + "; ".join(f"{k}: {v} (L0/L1/L2 {wcat_L[k]['L0']}/{wcat_L[k]['L1']}/{wcat_L[k]['L2']})" for k, v in wcat.most_common()))
    say(f"receipts on predicate-bound W1 hitting reports (predicate, terminal_state): {dict(bound_w1_receipts.most_common())}")
    fam_units = Counter()
    for u, fams in unit_families.items():
        for f in fams:
            fam_units[f] += 1
    say(f"FULL-hit units by hitting report family (a unit may count under several): {dict(fam_units.most_common())}")
    # predicate receipts and bindings
    term = Counter()
    term_true = Counter()
    for cell, rs in receipts.items():
        for r in rs:
            if r.get("terminal_state") != "completed":
                continue  # unsupported / not attempted: no verdict
            term[r["predicate_id"]] += 1
            if r.get("verdict") == "pass":
                term_true[r["predicate_id"]] += 1
    bound = Counter(clusters[r]["predicate_id"] for r in jd if r in clusters and clusters[r].get("predicate_id"))
    bound_valid = Counter(clusters[r]["predicate_id"] for r in jd if r in clusters and clusters[r].get("predicate_id") and jd[r]["v"] != "INVALID")
    say(f"predicate IDs with terminal receipts: {len(term)} -> {dict(sorted(term.items()))} (total {sum(term.values())}); "
        f"of which pass (true polarity): {dict(sorted(term_true.items()))} (total {sum(term_true.values())}); "
        f"violation (false polarity): {sum(term.values()) - sum(term_true.values())}")
    say(f"predicate IDs bound to published reports: {len(bound)} -> {dict(sorted(bound.items()))}; total bound reports {sum(bound.values())}")
    say(f"predicate IDs bound to valid (K/N) reports: {len(bound_valid)} -> {dict(sorted(bound_valid.items()))}")
    w2_bound = Counter(clusters[r]["predicate_id"] for r in jd if r in clusters and clusters[r]["witness_level"] == "W2")
    say(f"W2 reports by predicate: {dict(sorted(w2_bound.items()))}")
    roots = sum(1 for r in jd if r in clusters and clusters[r].get("folded_sub_claims"))
    agg = sum(1 for r in jd if r in clusters and clusters[r].get("guard_modality_aggregation"))
    say(f"published roots carrying folded sub-claims: {roots} (publish-stage folded_issue_count summed over cells: {publish_folded}); "
        f"guard-modality aggregated roots: {agg} (members: {publish_agg_members})")

    # ---------- appendix C.1: L1 table ----------
    l1 = sorted(e for e, L in tier.items() if L == "L1")
    excerpt_file = os.path.join(HERE, "l1_basis_excerpts.json")
    excerpts = json.load(open(excerpt_file)) if os.path.exists(excerpt_file) else {}
    rows = ["| 条目 | 方法命中轮数 | 基线命中轮数 | L 依据（摘） | 方法侧命中报告族 |", "| --- | ---: | ---: | --- | --- |"]
    win = lose = tie = 0
    base_units = {(e, o["round"]) for o in arms["baseline"].values() if o["v"] == "VALID_KNOWN" for e in o["full"] if e in tier}
    for e in l1:
        m = sum(1 for r in ROUNDS if (e, r) in unit_w_root)
        b = sum(1 for r in ROUNDS if (e, r) in base_units)
        win += m > b
        lose += m < b
        tie += m == b
        fams = sorted({f for r in ROUNDS for f in unit_families.get((e, r), set())})
        basis = excerpts.get(e) or items[e]["L_basis"].replace("|", "/")[:60]
        rows.append(f"| `{e}` | {m} | {b} | {basis} | {'、'.join(fams) if fams else '—'} |")
    say(f"\n## appendix C.1 (L1, {len(l1)} ids): method wins {win}, baseline wins {lose}, ties {tie}")
    lines.extend(rows)
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "evaluate_rq3_output.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(os.path.join(out_dir, "appendix_c1_l1_table.md"), "w") as fh:
        fh.write("\n".join(rows) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
