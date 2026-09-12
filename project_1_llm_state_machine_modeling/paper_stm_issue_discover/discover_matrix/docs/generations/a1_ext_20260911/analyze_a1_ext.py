"""Provider-free verification and table export for the frozen A1-ext archive (stdlib only).

Default: verify archive hashes, ledger identity, cell and expected-round closure, and recompute every stored
metric, per-round split, content split, paired comparison and strict interval from the stored report outcomes.
`--tables` prints the tables used by the formal report from the same frozen arrays; nothing is written back.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from a1ext_common import (AXES, MODELS, NAMES, PAPER, arm_summary, calculate, compare, content_breakdown, digest, expected_rows,
                          ledger_items, pct, per_round, pp, read, strict_cluster_bootstrap, strict_view)

ARCHIVE = PAPER / "final_results/a1_ext_20260911"
LUNA = PAPER / "final_results/a1_no_inspect_vs_v61_20260906/results.json"


def canonical(value):
    return json.loads(json.dumps(value))


def validate_arm(arm, items, label):
    cells = {(c["pair_id"], c["round"]) for c in arm["cells"]}
    assert len({p for p, _ in cells}) == 54 and cells == {(p, r) for p in {p for p, _ in cells} for r in (1, 2, 3)}, label
    assert len(arm["cells"]) == arm["coverage"]["judged_cells"] == arm["coverage"]["eligible_cells"] == 162, label
    assert arm["coverage"]["planned_expected_rounds"] == 435 and arm["coverage"]["unjudged_reports"] == 0, label
    reports = {r["original_report_id"]: r for r in arm["reports"]}
    assert len(reports) == len(arm["reports"]) == sum(c["reports"] for c in arm["cells"]), (label, "report ids or per-cell counts")
    per_cell = Counter((r["pair_id"], r["round"]) for r in reports.values())
    assert all(per_cell[c["pair_id"], c["round"]] == c["reports"] for c in arm["cells"]), (label, "per-cell report coverage")
    assert all(r["nl_cluster"] for r in arm["reports"]), label
    assert canonical(expected_rows(arm["reports"], items)) == arm["expected"], (label, "expected rows")
    assert canonical(calculate(arm["reports"], items)) == arm["metrics"], (label, "stored metrics differ from outcomes")
    assert canonical(per_round(arm["reports"], items)) == arm["per_round"], (label, "per-round metrics")
    assert canonical(content_breakdown(arm["reports"], items)) == arm["content"], (label, "content split")
    assert arm["funnel"]["published"] == len(arm["reports"]) and arm["funnel"]["cells"] == 162, label


def verify(archive=ARCHIVE):
    manifest = read(archive / "archive_manifest.json")
    for name, expected in manifest["files"].items():
        assert digest(archive / name) == expected, name
    data = read(archive / "results.json")
    ledger = PAPER / "discover_matrix/ledger_v2/ledger.json"
    assert digest(ledger) == manifest["ledger_sha256"] == data["ledger_hash"]
    items = ledger_items()
    assert len(items) == 145 and Counter(i["L"] for i in items.values()) == {"L0": 71, "L1": 35, "L2": 39}
    assert data["complete"] and set(data["models"]) == set(MODELS)
    for model in MODELS:
        m = data["models"][model]
        for arm in ("a1ext", "full"):
            validate_arm(m[arm], items, f"{model}/{arm}")
        stored = dict(m["comparison"]); strict = stored.pop("strict")
        assert canonical(compare(m["a1ext"], m["full"], items)) == stored, (model, "paired comparison")
        assert canonical(strict_cluster_bootstrap(m["a1ext"], m["full"], items)) == strict, (model, "strict interval")
    luna = read(LUNA)
    assert digest(LUNA) == data["luna_reference"]["sha256"]
    assert data["luna_reference"]["metrics"]["no_inspect_a1"] == luna["a1"]["metrics"]
    assert data["luna_reference"]["metrics"]["full_v61"] == luna["v61"]["metrics"]
    return data, items, luna


def tables(data, items, luna):
    rows = []
    P = lambda r: pct(r)
    arms = {}
    for model in MODELS:
        arms[model] = {arm: arm_summary(data["models"][model][arm], items) for arm in ("a1ext", "full")}
    luna_arm = {"a1ext": {"reports": luna["a1"]["reports"], "cells": luna["a1"]["cells"]}, "full": {"reports": luna["v61"]["reports"], "cells": luna["v61"]["cells"]}}
    arms["luna"] = {arm: arm_summary(luna_arm[arm], items) for arm in ("a1ext", "full")}
    order = ("sonnet", "muse", "qwen", "luna")
    print("表 1：主表（三轮 pooled）")
    print("| 模型 | 条件 | 报告 R | K/N/I | 普通 precision | strict precision | hit@1 | strict hit@1 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in order:
        for arm, cond in (("full", "Full"), ("a1ext", "no-inspect")):
            s = arms[model][arm]
            print(f"| {NAMES[model]} | {cond} | {s['reports']} | {s['K']}/{s['N']}/{s['I']} | {P(s['precision'])} | {P(s['strict_precision'])} | {P(s['hit1'])} | {P(s['strict_hit1'])} |")
    print("\n表 2：差值（no-inspect − Full，pp）与有效报告变化")
    print("| 模型 | 有效报告 Full → no-inspect | 相对变化 | ΔI | Δ普通 pp | Δstrict pp | Δhit@1 pp | Δstrict hit@1 pp |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in order:
        f, a = arms[model]["full"], arms[model]["a1ext"]
        vf, va = f["K"] + f["N"], a["K"] + a["N"]
        print(f"| {NAMES[model]} | {vf} → {va} | {100 * (va - vf) / vf:+.2f}% | {a['I'] - f['I']:+d} | {pp(a['precision'], f['precision'])} | {pp(a['strict_precision'], f['strict_precision'])} | {pp(a['hit1'], f['hit1'])} | {pp(a['strict_hit1'], f['strict_hit1'])} |")
    print("\n表 3：逐轮（每行 54 格；hit 分母 145）")
    print("| 模型 | 条件 | 轮次 | 报告 | K/N/I | precision | hit |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for model in order:
        for arm, cond in (("full", "Full"), ("a1ext", "no-inspect")):
            src = luna_arm[arm]["reports"] if model == "luna" else data["models"][model][arm]["reports"]
            for rnd in (1, 2, 3):
                c = calculate([r for r in src if r["round"] == rnd], items)
                print(f"| {NAMES[model]} | {cond} | {rnd} | {c['reports']} | {c['K']}/{c['N']}/{c['I']} | {P(c['precision'])} | {c['per_round'][rnd]}/145（{100 * c['per_round'][rnd] / 145:.2f}%） |")
    print("\n表 4：跨轮覆盖与 L 分层（hit@3/@all 分母 145；层分母 213/105/117）")
    print("| 模型 | 条件 | hit@3 | hit@all | L0 hit@1 | L1 hit@1 | L2 hit@1 | L2 hit@3 | L2 hit@all |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in order:
        for arm, cond in (("full", "Full"), ("a1ext", "no-inspect")):
            s = arms[model][arm]
            print(f"| {NAMES[model]} | {cond} | {P(s['hit3'])} | {P(s['hitall'])} | {P(s['tiers']['L0'])} | {P(s['tiers']['L1'])} | {P(s['tiers']['L2'])} | {P(s['tiers_hit3']['L2'])} | {P(s['tiers_hitall']['L2'])} |")
    print("\n表 5：命中单元集合（台账 ID×轮次）的共有 / Full 独有 / no-inspect 独有，及按层")
    print("| 模型 | 共有 | Full 独有 | no-inspect 独有 | Full 独有按层 L0/L1/L2 | no-inspect 独有按层 L0/L1/L2 |")
    print("| --- | --- | --- | --- | --- | --- |")
    for model in MODELS:
        cmp_ = data["models"][model]["comparison"]
        a = {(e, r["round"]) for r in data["models"][model]["a1ext"]["reports"] if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
        f = {(e, r["round"]) for r in data["models"][model]["full"]["reports"] if r["validity"] == "VALID_KNOWN" for e in r["full_ledger_ids"]}
        lt, gt = cmp_["lost_by_tier"], cmp_["gained_by_tier"]
        print(f"| {NAMES[model]} | {len(a & f)} | {len(f - a)} | {len(a - f)} | {lt.get('L0', 0)}/{lt.get('L1', 0)}/{lt.get('L2', 0)} | {gt.get('L0', 0)}/{gt.get('L1', 0)}/{gt.get('L2', 0)} |")
    lc = luna["comparison"]
    print(f"| {NAMES['luna']} | {len({(e, r['round']) for r in luna['a1']['reports'] if r['validity']=='VALID_KNOWN' for e in r['full_ledger_ids']} & {(e, r['round']) for r in luna['v61']['reports'] if r['validity']=='VALID_KNOWN' for e in r['full_ledger_ids']})} | {len(lc['lost'])} | {len(lc['gained'])} | {lc['lost_by_tier'].get('L0',0)}/{lc['lost_by_tier'].get('L1',0)}/{lc['lost_by_tier'].get('L2',0)} | {lc['gained_by_tier'].get('L0',0)}/{lc['gained_by_tier'].get('L1',0)}/{lc['gained_by_tier'].get('L2',0)} |")
    print("\n表 6：按台账轴的 FULL 命中（分母 = 3 轮 × 该类条目数；每格 Full → no-inspect）")
    for axis in AXES:
        print(f"\n{axis}")
        values = sorted(data["models"]["sonnet"]["full"]["content"][axis])
        print("| 取值 | 条目数 | " + " | ".join(NAMES[m] for m in order) + " |")
        print("| --- | --- | " + " | ".join("---" for _ in order) + " |")
        luna_content = {arm: content_breakdown(luna_arm[arm]["reports"], items) for arm in ("a1ext", "full")}
        for v in values:
            cells = []
            for model in order:
                f = luna_content["full"][axis][v] if model == "luna" else data["models"][model]["full"]["content"][axis][v]
                a = luna_content["a1ext"][axis][v] if model == "luna" else data["models"][model]["a1ext"]["content"][axis][v]
                cells.append(f"{f['numerator']} → {a['numerator']}")
            den = data["models"]["sonnet"]["full"]["content"][axis][v]["denominator"]
            print(f"| {v} | {den // 3} | " + " | ".join(cells) + " |")
    print("\n表 7：候选、证据资格与执行组成（no-inspect 来自方法格原件；Full 来自 E2 cells.json）")
    print("| 模型 | 条件 | 格 | 候选 | 带谓词候选 | 候选 W0/W1/W2 | 候选 coverage_class（semantic_hit/executable_evidence/coverage_gap/execution_degraded） | 发布 | 发布 W1/W2 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in MODELS:
        for arm, cond in (("full", "Full"), ("a1ext", "no-inspect")):
            fn = data["models"][model][arm]["funnel"]; cw = fn["candidate_witness"]; cc = fn["candidate_coverage_class"]; pw = fn["published_witness"]
            print(f"| {NAMES[model]} | {cond} | {fn['cells']} | {fn['candidates']} | {fn['candidates_with_predicate']} | {cw.get('W0', 0)}/{cw.get('W1', 0)}/{cw.get('W2', 0)} | {cc.get('semantic_hit', 0)}/{cc.get('executable_evidence', 0)}/{cc.get('coverage_gap', 0)}/{cc.get('execution_degraded', 0)} | {fn['published']} | {pw.get('W1', 0)}/{pw.get('W2', 0)} |")
    print("\n表 8：九 NL 簇配对 bootstrap 95% 区间（no-inspect − Full，pp；seed 20260906，10000 次）")
    print("| 模型 | Δhit@1 | Δhit@3 | Δhit@all | ΔL2 hit@1 | Δprecision | Δstrict precision | Δstrict hit@1 |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    def iv(d, k):
        v = d[k]; return f"[{v['percentile_2_5']:+.2f}, {v['percentile_97_5']:+.2f}]"
    for model in MODELS:
        c = data["models"][model]["comparison"]; b = c["cluster_bootstrap_95pct"]; s = c["strict"]["cluster_bootstrap_95pct"]
        print(f"| {NAMES[model]} | {iv(b, 'hit1')} | {iv(b, 'hit3')} | {iv(b, 'hitall')} | {iv(b, 'L2_hit1')} | {iv(b, 'precision')} | {iv(s, 'strict_precision')} | {iv(s, 'strict_hit1')} |")
    b = luna["comparison"]["cluster_bootstrap_95pct"]
    print(f"| {NAMES['luna']}（A1 归档） | {iv(b, 'hit1')} | {iv(b, 'hit3')} | {iv(b, 'hitall')} | {iv(b, 'L2_hit1')} | {iv(b, 'precision')} | 归档未含 | 归档未含 |")
    print("\n表 9：逐簇 Δhit@1（pp）与留一簇差值范围")
    print("| 模型 | 逐簇 Δhit@1 下降簇数/9 | 逐簇范围 | 留一簇 Δhit@1 范围 | 留一簇 Δprecision 范围 |")
    print("| --- | --- | --- | --- | --- |")
    for model in MODELS:
        c = data["models"][model]["comparison"]
        per = [v["hit1"] for v in c["per_cluster_delta_pp"].values() if v["hit1"] is not None]
        loo = [v["hit1"] for v in c["leave_one_cluster_out_delta_pp"].values()]; loop = [v["precision"] for v in c["leave_one_cluster_out_delta_pp"].values()]
        print(f"| {NAMES[model]} | {sum(1 for x in per if x < 0)}/{len(per)} | [{min(per):+.2f}, {max(per):+.2f}] | [{min(loo):+.2f}, {max(loo):+.2f}] | [{min(loop):+.2f}, {max(loop):+.2f}] |")
    print("\n表 10：judge 与 method 运行审计")
    print("| 模型 | method run | 24 workers | 恢复替换格 | 带诊断格 | 结构化调用 | schema 反馈修订 | transport retry 记录 | judge runs（轮:run_id 前 8 位:rc） |")
    print("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for model in MODELS:
        a = data["models"][model]["a1ext"]; ca = a["call_audit"]; cov = a["coverage"]
        runs = "; ".join(f"r{j['round']}:{j['run_id'][:8]}:{j['rc']}{'(重采样)' if j['resample_of_failed_pair'] else ''}" for j in a["judge_runs"])
        mr = sorted({c["method_run_id"][:8] for c in a["cells"]})
        print(f"| {NAMES[model]} | {', '.join(mr)} | 是 | {cov['cells_replaced_by_isolated_recovery']} | {cov['cells_with_diagnostics']} | {ca['structured_calls']} | {ca['schema_validation_failures']} | {ca['transport_retry_records']} | {runs} |")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, default=ARCHIVE)
    parser.add_argument("--tables", action="store_true")
    args = parser.parse_args()
    data, items, luna = verify(args.archive)
    if args.tables:
        tables(data, items, luna)
    else:
        print(json.dumps({"status": "verified_offline_arithmetic", "models": {m: {arm: {k: data["models"][m][arm]["metrics"][k] for k in ("reports", "K", "N", "I", "hit1", "precision")} for arm in ("a1ext", "full")} for m in MODELS},
                          "scope": "Recomputes saved judge decisions; no provider calls or re-adjudication."}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
