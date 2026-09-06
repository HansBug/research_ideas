"""x1-split-intervention: manipulation check + side effects + cost.

Reads the control and treatment arms produced by /tmp/x1intervene/launch.sh and reports
everything the preregistration promised EXCEPT the hit verdicts, which are human-judged.
"""
import json, pathlib, collections, statistics, sys

R = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3/runs/paper1")
ARM_DIR = {"control": R/"x1-split-intervention/control",
           "treatment_v1": R/"x1-split-intervention/treatment",
           "treatment_v2": R/"x1-split-intervention-v2/treatment_v2"}
ARMS = ("control", "treatment_v1", "treatment_v2")
DM = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix")
sys.path.insert(0, str(DM))
import metrics_at_k as M
REPORTABLE = set(M.REPORTABLE)

GRID = json.load(open("/tmp/x1intervene/grid.json"))
PAIRS, TARGET, REGRESSION = GRID["pairs"], set(GRID["target"]), set(GRID["regression"])
ledger = {r["id"]: r for r in json.load(open(DM / "manual_review/expected_issue_set.json"))["records"]}


def requirement_predicates(cell):
    """parsed_output.requirements[].predicate ONLY -- never regex the whole record."""
    out = set()
    for rec in sorted(cell.glob("records/*requirement-splitter-llm-call-completed*/record.json")):
        p = json.loads(rec.read_text()).get("parsed_output")
        if isinstance(p, dict):
            for r in p.get("requirements") or ():
                if isinstance(r, dict) and r.get("predicate"):
                    out.add(str(r["predicate"]))
    return out


def final_requirement_predicates(cell):
    """Predicates in the LAST splitter revision -- what actually went downstream."""
    recs = sorted(cell.glob("records/*requirement-splitter-llm-call-completed*/record.json"))
    if not recs:
        return set()
    p = json.loads(recs[-1].read_text()).get("parsed_output") or {}
    return {str(r["predicate"]) for r in (p.get("requirements") or ())
            if isinstance(r, dict) and r.get("predicate")}


def cell_stats(cell):
    f = cell / "discover-completed.json"
    if not f.exists():
        return None
    d = json.loads(f.read_text())
    t = d.get("telemetry_summary") or {}
    tok = t.get("tokens") or {}
    return dict(
        issues=len(d.get("issues") or []),
        coverage_gaps=len(d.get("coverage_gaps") or []),
        degraded=len(d.get("degraded_stages") or []),
        coverage_status=d.get("coverage_status"),
        wall_s=(t.get("node_elapsed_ms_sum") or 0) / 1000,
        in_tok=tok.get("input_tokens") or 0,
        out_tok=tok.get("output_tokens") or 0,
        excluded_findings=len(d.get("excluded_findings") or []),
    )


report = {"arms": {}, "manipulation": {}, "per_pair": {}}
for arm in ARMS:
    rows, sysp = [], set()
    for pair in PAIRS:
        cell = ARM_DIR[arm] / f"{pair}-claude"
        st = cell_stats(cell)
        wp_all, wp_fin = requirement_predicates(cell), final_requirement_predicates(cell)
        recs = sorted(cell.glob("records/*requirement-splitter-llm-call-completed*/record.json"))
        if recs:
            sysp.add(json.loads(recs[0].read_text())["system_prompt_sha256"][:16])
        rows.append(dict(pair=pair, landed=st is not None, **(st or {}),
                         written_any=sorted(wp_all), written_final=sorted(wp_fin)))
    report["arms"][arm] = dict(rows=rows, splitter_prompt_sha=sorted(sysp))

# ---- manipulation check: did the TARGET predicate enter the requirement set? ----
for arm in ARMS:
    byp = {r["pair"]: r for r in report["arms"][arm]["rows"]}
    hit_any = hit_fin = n = 0
    detail = []
    for rid in sorted(TARGET):
        rec = ledger[rid]
        pair, pred = rec["pair"], rec.get("primary_predicate")
        row = byp.get(pair)
        if row is None or not row["landed"]:
            detail.append((rid, pair, pred, None, None)); continue
        a, f = pred in row["written_any"], pred in row["written_final"]
        n += 1; hit_any += a; hit_fin += f
        detail.append((rid, pair, pred, a, f))
    report["manipulation"][arm] = dict(n=n, in_any_revision=hit_any, in_final=hit_fin, detail=detail)

# ---------------------------------- print ----------------------------------
print("=" * 96)
print("x1-split-intervention  ·  操纵检查与副作用（命中判定另行人工进行）")
print("=" * 96)

for arm in ARMS:
    rows = [r for r in report["arms"][arm]["rows"]]
    landed = [r for r in rows if r["landed"]]
    print(f"\n### {arm}   落盘 {len(landed)}/{len(rows)}   splitter prompt sha16={report['arms'][arm]['splitter_prompt_sha']}")
    if not landed:
        continue
    for k, lbl in (("issues", "已发布 issue"), ("coverage_gaps", "coverage_gaps"),
                   ("degraded", "degraded_stages"), ("excluded_findings", "excluded_findings")):
        v = [r[k] for r in landed]
        print(f"   {lbl:22s} 均值 {statistics.mean(v):6.2f}  中位 {statistics.median(v):5.1f}  最大 {max(v):3d}  非零格 {sum(1 for x in v if x)}")
    print(f"   {'墙钟(s)':22s} 合计 {sum(r['wall_s'] for r in landed):8.0f}  均值 {statistics.mean([r['wall_s'] for r in landed]):7.0f}")
    print(f"   {'token in/out':22s} {sum(r['in_tok'] for r in landed):>10,d} / {sum(r['out_tok'] for r in landed):>9,d}")

print("\n" + "=" * 96)
print("操纵检查（preregistered §4.2）：TARGET 位的台账 primary 谓词是否进了需求集")
print("=" * 96)
for arm in ARMS:
    m = report["manipulation"][arm]
    if m["n"]:
        print(f"  {arm:10s} n={m['n']:2d}  出现在任一修订 {m['in_any_revision']:2d}/{m['n']} = {m['in_any_revision']/m['n']:5.1%}"
              f"   出现在最终需求集 {m['in_final']:2d}/{m['n']} = {m['in_final']/m['n']:5.1%}")

print(f"\n{'record':14s}{'pair':6s}{'predicate':24s}" + "".join(f"{a:>16s}" for a in ARMS))
DET = {a: {d[0]: d for d in report["manipulation"][a]["detail"]} for a in ARMS}
fm = lambda d: "格未落盘" if d is None or d[3] is None else ("最终集OK" if d[4] else ("仅中间修订" if d[3] else "X"))
for rid in sorted(TARGET):
    c = DET["control"].get(rid)
    print(f"{rid:14s}{c[1]:6s}{str(c[2]):24s}" + "".join(f"{fm(DET[a].get(rid)):>16s}" for a in ARMS))

# predicate supply, all four swept predicates
print("\n四条扫描谓词的供给（写进最终需求集的格数 / 落盘格数）")
SWEPT = ["edge_declared", "reaches", "event_consumed", "guard_distinguishable"]
print(f"{'predicate':26s}" + "".join(f"{a:>16s}" for a in ARMS))
for pred in SWEPT + ["occupancy_after"]:
    cells = []
    for arm in ARMS:
        rows = [r for r in report["arms"][arm]["rows"] if r["landed"]]
        cells.append(f"{sum(1 for r in rows if pred in r['written_final'])}/{len(rows)}" if rows else "-")
    print(f"{pred:26s}" + "".join(f"{c:>16s}" for c in cells))

# per-cell requirement counts, to separate "asked more" from "asked differently"
print("\n每格需求条数（最终修订）")
print(f"{'pair':8s}" + "".join(f"{a:>16s}" for a in ARMS))
for pair in PAIRS:
    cells = []
    for arm in ARMS:
        cell = ARM_DIR[arm] / f"{pair}-claude"
        recs = sorted(cell.glob("records/*requirement-splitter-llm-call-completed*/record.json"))
        if not recs:
            cells.append("-"); continue
        p = json.loads(recs[-1].read_text()).get("parsed_output") or {}
        cells.append(str(len(p.get("requirements") or [])))
    print(f"{pair:8s}" + "".join(f"{c:>16s}" for c in cells))

json.dump(report, open("/tmp/x1intervene/analysis.json", "w"), indent=1, default=str)
print("\n-> /tmp/x1intervene/analysis.json")
