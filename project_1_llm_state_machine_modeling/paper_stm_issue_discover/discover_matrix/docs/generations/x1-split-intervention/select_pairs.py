"""Per-pair main-arm hit rate restricted to the 'primary_predicate not written into
the requirement set' stratum. Read-only join of three sources."""
import json, pathlib, collections, sys

DM = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix")
RUNS = pathlib.Path.home()/"oo-projects/research_ideas/runs/paper1/matrix-v46-full"
sys.path.insert(0, str(DM))
import metrics_at_k as M
REPORTABLE = set(M.REPORTABLE)

ledger = {r["id"]: r for r in json.load(open(DM/"manual_review/expected_issue_set.json"))["records"]}
tiers = json.load(open(DM/"v46/verdicts/v46_tiers.json"))["verdicts"]
x1 = json.load(open("/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/baseline_arm/results/tiers_x1.json"))["verdicts"]

ARMS = {"claude": "claude", "gpt": "gpt"}

def written_predicates(cell_dir):
    """parsed_output.requirements[].predicate ONLY -- never regex the whole record."""
    out = set()
    for rec in sorted(cell_dir.glob("records/*requirement-splitter-llm-call-completed*/record.json")):
        p = json.loads(rec.read_text()).get("parsed_output")
        if isinstance(p, dict):
            for r in p.get("requirements") or ():
                if isinstance(r, dict) and r.get("predicate"):
                    out.add(str(r["predicate"]))
    return out

cache = {}
rows = []
for rid, v in tiers.items():
    if rid not in REPORTABLE: continue
    rec = ledger[rid]; pair = rec["pair"]; pred = rec.get("primary_predicate")
    for arm in ("claude", "gpt"):
        bits = v.get(arm) or []
        xb = (x1.get(rid) or {}).get(arm) or []
        for i, hit in enumerate(bits):
            run = f"run{i+1}"
            cell = RUNS/run/f"{pair}-{arm}"
            if cell not in cache: cache[cell] = written_predicates(cell)
            written = cache[cell]
            stratum = ("no_primary" if not pred
                       else "in_set" if pred in written else "not_in_set")
            rows.append(dict(rid=rid, pair=pair, arm=arm, run=run, pred=pred,
                             stratum=stratum, main=int(hit),
                             x1=int(xb[i]) if i < len(xb) else None))

print(f"positions={len(rows)} main_hits={sum(r['main'] for r in rows)}")
for s in ("in_set","not_in_set","no_primary"):
    sub=[r for r in rows if r["stratum"]==s]
    mh=sum(r["main"] for r in sub); xh=sum(r["x1"] or 0 for r in sub)
    print(f"  {s:12s} n={len(sub):4d} main={mh/len(sub):.1%} x1={xh/len(sub):.1%}")

print("\n=== per-pair, NOT_IN_SET stratum (sorted by main hit rate asc, then n desc) ===")
bp=collections.defaultdict(lambda: dict(n=0,mh=0,xh=0,preds=collections.Counter()))
for r in rows:
    if r["stratum"]!="not_in_set": continue
    b=bp[r["pair"]]; b["n"]+=1; b["mh"]+=r["main"]; b["xh"]+=r["x1"] or 0; b["preds"][r["pred"]]+=1
print(f"{'pair':6s}{'n':>4s}{'main':>8s}{'x1':>8s}{'gap':>8s}  predicates")
for pair,b in sorted(bp.items(), key=lambda kv:(kv[1]["mh"]/kv[1]["n"], -kv[1]["n"])):
    m=b["mh"]/b["n"]; x=b["xh"]/b["n"]
    print(f"{pair:6s}{b['n']:>4d}{m:>8.1%}{x:>8.1%}{(x-m)*100:>+7.1f}  {dict(b['preds'])}")
json.dump(rows, open("/tmp/x1intervene/v46_stratified_positions.json","w"), indent=1)
