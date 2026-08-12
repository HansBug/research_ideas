"""Judging-independent probe: for each TARGET record and each arm, how deep into the
pipeline did the ledger's own question get?

This does NOT need hit verdicts. It reuses `verdict_tiers.ledger_claims()` (the exact
(predicate, bindings) -> expected-truth the ledger wrote) and `verdict_tiers.cell_evidence()`
(every predicate call the cell actually evaluated, with bindings, result and published flag),
which are the same primitives `loss_stages.py` and the tier-A adjudicator use.

Stages, deepest reached wins:
  ① 需求层  predicate never written into any requirement revision, and never called
  ② 断言层  predicate present, but nothing bound the way the ledger asks
  ⑤ 绑定层  same as ② except the cell DID publish something using that predicate
  ④ 发布层  the exact question was asked and got the expected truth, but was not published
  ✔ 已发布  asked, expected truth, published  (= tier-A hit condition)
"""
import json, pathlib, sys, collections

REPO = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3")
DM = REPO / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix"
sys.path.insert(0, str(DM))
import verdict_tiers as V

ARM_DIR = {"control": REPO / "runs/paper1/x1-split-intervention/control",
           "treatment_v1": REPO / "runs/paper1/x1-split-intervention/treatment",
           "treatment_v2": REPO / "runs/paper1/x1-split-intervention-v2/treatment_v2"}
ARMS = tuple(ARM_DIR)

GRID = json.load(open("/tmp/x1intervene/grid.json"))
TARGET, REGRESSION = sorted(GRID["target"]), sorted(GRID["regression"])
ledger = V.ledger_claims()


def written(cell):
    out = set()
    for rec in sorted(cell.glob("records/*requirement-splitter-llm-call-completed*/record.json")):
        p = json.loads(rec.read_text()).get("parsed_output")
        if isinstance(p, dict):
            for r in p.get("requirements") or ():
                if isinstance(r, dict) and r.get("predicate"):
                    out.add(str(r["predicate"]))
    return out


def answers(call, bindings):
    cb, lb = dict(call["bindings"]), dict(bindings)
    if set(lb) - set(cb):
        return False
    if set(cb) - set(lb) - V._HORIZON_BINDINGS:
        return False
    return all(lb[k] == cb[k] for k in lb)


DEPTH = {"① 需求层": 1, "② 断言层": 2, "⑤ 绑定层": 3, "④ 发布层": 4, "✔ 已发布": 5}


def stage(rid, cell):
    if not (cell / "discover-completed.json").exists():
        return "格未落盘"
    rec = ledger[rid]
    claims = rec.get("claims") or {}
    if not rec.get("primary_predicate"):
        return "无 primary"
    if not claims:
        return "primary 不可机械解析"
    ev, wr = V.cell_evidence(cell), written(cell)
    best = "① 需求层"
    for (pred, binds), expected in claims.items():
        same = [c for c in ev["calls"] if c["predicate"] == pred]
        ans = [c for c in same if answers(c, binds)]
        if pred not in wr and not same:
            s = "① 需求层"
        elif not ans:
            s = "⑤ 绑定层" if any(c["published"] for c in same) else "② 断言层"
        elif not any(c["result"] is expected for c in ans):
            s = "② 断言层"
        elif not any(c["published"] and c["result"] is expected for c in ans):
            s = "④ 发布层"
        else:
            s = "✔ 已发布"
        if DEPTH.get(s, 0) > DEPTH.get(best, 0):
            best = s
    return best


for name, recs in (("TARGET", TARGET), ("REGRESSION", REGRESSION)):
    print("\n" + "=" * 96)
    print(f"{name} · 台账原问题在各臂到达的最深环节（不依赖人工判定）")
    print("=" * 96)
    print(f"{'record':14s}{'pair':6s}{'predicate':24s}" + "".join(f"{a:>20s}" for a in ARMS))
    tal = collections.defaultdict(collections.Counter)
    for rid in recs:
        r = ledger[rid]
        cells = []
        for a in ARMS:
            s = stage(rid, ARM_DIR[a] / f"{r['pair']}-claude")
            cells.append(s); tal[a][s] += 1
        print(f"{rid:14s}{r['pair']:6s}{str(r.get('primary_predicate')):24s}" + "".join(f"{c:>20s}" for c in cells))
    print(f"\n  小计：")
    for a in ARMS:
        print(f"    {a:14s} " + "  ".join(f"{k}={v}" for k, v in sorted(tal[a].items())))
