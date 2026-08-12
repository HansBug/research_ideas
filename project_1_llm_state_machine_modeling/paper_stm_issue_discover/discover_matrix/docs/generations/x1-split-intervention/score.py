"""Unblind the judge verdicts and score them against the PREREGISTERED criteria.

Inputs : /tmp/x1intervene/verdicts_*.json  (judge output, arms labelled 甲/乙/丙)
         /tmp/x1intervene/blind_key.json   (per-pair 甲/乙/丙 -> arm)
         /tmp/x1intervene/grid.json        (TARGET / REGRESSION record sets)
Output : per-position before/after table + the preregistered verdict.

⛔ The thresholds below are copied from preregistered.md §4 and must not be edited.
"""
import json, glob, pathlib, collections, sys

ARMS = ("control", "treatment_v1", "treatment_v2")
KEY = json.load(open("/tmp/x1intervene/blind_key.json"))
GRID = json.load(open("/tmp/x1intervene/grid.json"))
TARGET, REGRESSION, PAIRS = set(GRID["target"]), set(GRID["regression"]), GRID["pairs"]
DM = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix")
sys.path.insert(0, str(DM))
import metrics_at_k as M
REPORTABLE = set(M.REPORTABLE)
ledger = {r["id"]: r for r in json.load(open(DM / "manual_review/expected_issue_set.json"))["records"]}

# ---- preregistered thresholds, §4. DO NOT EDIT. ----
PRE = dict(strong_abs=9, strong_delta=5, partial_abs=6, partial_delta=3,
           null_delta=1, n_target=14, manipulation_floor=0.50)

# ---- load and unblind ----
hits = {}          # (record_id, arm) -> bool
args_ = {}
dupes = collections.Counter()
JUDGE_FILES = [f for f in sorted(glob.glob("/tmp/x1intervene/verdicts_[A-Z].json"))]
print("判定文件：", [pathlib.Path(f).name for f in JUDGE_FILES])
for f in JUDGE_FILES:
    data = json.load(open(f))
    blocks = data if isinstance(data, list) else [data]
    for blk in blocks:
        pair = str(blk["pair"]).zfill(4)
        for v in blk["verdicts"]:
            arm = KEY[pair][v["arm"]]
            rid = v["record_id"]
            if (rid, arm) in hits:
                dupes[(rid, arm)] += 1
            hits[(rid, arm)] = bool(v["hit"])
            args_[(rid, arm)] = (v.get("equivalence_form"), v.get("argument", ""), v.get("note", ""))

if dupes:
    print(f"⚠️ 重复判定 {len(dupes)} 处（后者覆盖前者）：{list(dupes)[:5]}")

# ---- coverage check: every (record, arm) must be judged ----
allrec = sorted({r for r in TARGET | REGRESSION})
missing = [(r, a) for r in allrec for a in ARMS if (r, a) not in hits]
print(f"应判 {len(allrec)*3} 位，已判 {len(allrec)*3-len(missing)} 位，缺 {len(missing)} 位")
if missing:
    print("  缺：", missing[:20])


REPO = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3")
ARM_DIR = {"control": REPO / "runs/paper1/x1-split-intervention/control",
           "treatment_v1": REPO / "runs/paper1/x1-split-intervention/treatment",
           "treatment_v2": REPO / "runs/paper1/x1-split-intervention-v2/treatment_v2"}
# A crashed cell publishes nothing, so all its records read as misses. That is the correct
# primary number -- a lost sample is a lost sample -- but CLAUDE.md §10 says a crash should
# have been a degradation, so the crash penalises the arm for an engineering defect rather
# than a capability gap. Report both: primary counts crashes as misses, sensitivity drops them.
CRASHED = {(a, p) for a in ARM_DIR for p in PAIRS
           if not (ARM_DIR[a] / f"{p}-claude/discover-completed.json").exists()}
if CRASHED:
    print(f"⚠️ 未落盘/失败格：{sorted(CRASHED)}")


def tally(recs, arm, drop_crashed=False):
    got = [r for r in recs if (r, arm) in hits]
    if drop_crashed:
        got = [r for r in got if (arm, ledger[r]["pair"]) not in CRASHED]
    return sum(hits[(r, arm)] for r in got), len(got)


print("\n" + "=" * 92)
print("命中汇总（1 轮，claude-opus-4-7，10 pair）")
print("=" * 92)
print(f"{'位集':16s}" + "".join(f"{a:>18s}" for a in ARMS))
for name, recs in (("TARGET(14)", TARGET), ("REGRESSION(12)", REGRESSION),
                   ("合计(26)", TARGET | REGRESSION)):
    row = []
    for a in ARMS:
        h, n = tally(recs, a)
        row.append(f"{h}/{n} = {h/n:.1%}" if n else "-")
    print(f"{name:16s}" + "".join(f"{c:>18s}" for c in row))

# Within-TARGET split: the four swept predicates vs the rest. The sweep should move the
# former and not specifically the former's neighbours -- a gain concentrated on non-swept
# records would mean the arm just asks more questions, not that the sweep did anything.
SWEPT = {"edge_declared", "reaches", "event_consumed", "guard_distinguishable"}
tgt_swept = {r for r in TARGET if ledger[r].get("primary_predicate") in SWEPT}
tgt_other = TARGET - tgt_swept
print(f"\nTARGET 内部拆分（扫描射程内 {len(tgt_swept)} 条 vs 射程外 {len(tgt_other)} 条）")
print(f"{'子集':22s}" + "".join(f"{a:>18s}" for a in ARMS))
for name, recs in ((f"射程内({len(tgt_swept)})", tgt_swept), (f"射程外({len(tgt_other)})", tgt_other)):
    row = []
    for a in ARMS:
        h, n = tally(recs, a)
        row.append(f"{h}/{n} = {h/n:.1%}" if n else "-")
    print(f"{name:22s}" + "".join(f"{c:>18s}" for c in row))

print("\n" + "=" * 92)
print("TARGET 逐位 before/after")
print("=" * 92)
print(f"{'record':14s}{'pair':6s}{'predicate':24s}" + "".join(f"{a:>16s}" for a in ARMS))
for rid in sorted(TARGET):
    rec = ledger[rid]
    cells = ["命中" if hits.get((rid, a)) else ("未命中" if (rid, a) in hits else "未判")
             for a in ARMS]
    mark = ""
    if hits.get((rid, "control")) is False and hits.get((rid, "treatment_v2")) is True:
        mark = "  <- v2 追回"
    if hits.get((rid, "control")) is True and hits.get((rid, "treatment_v2")) is False:
        mark = "  <- v2 丢失"
    print(f"{rid:14s}{rec['pair']:6s}{str(rec.get('primary_predicate')):24s}"
          + "".join(f"{c:>16s}" for c in cells) + mark)

print("\n" + "=" * 92)
print("REGRESSION 逐位")
print("=" * 92)
print(f"{'record':14s}{'pair':6s}{'predicate':24s}" + "".join(f"{a:>16s}" for a in ARMS))
for rid in sorted(REGRESSION):
    rec = ledger[rid]
    cells = ["命中" if hits.get((rid, a)) else ("未命中" if (rid, a) in hits else "未判")
             for a in ARMS]
    print(f"{rid:14s}{rec['pair']:6s}{str(rec.get('primary_predicate')):24s}" + "".join(f"{c:>16s}" for c in cells))

# ---- preregistered verdict ----
ct, cn = tally(TARGET, "control")
print("\n" + "=" * 92)
print("对照预登记 §4 的判定（阈值为跑前写死，⛔ 未改动）")
print("=" * 92)
manip = json.load(open("/tmp/x1intervene/analysis.json"))["manipulation"]
for arm in ("treatment_v1", "treatment_v2"):
    tt, tn = tally(TARGET, arm)
    delta = tt - ct
    m = manip.get(arm, {})
    mrate = (m.get("in_final", 0) / m["n"]) if m.get("n") else 0.0
    print(f"\n### {arm}")
    print(f"  TARGET 命中 {tt}/{tn}（对照 {ct}/{cn}），Δ = {delta:+d} 位")
    print(f"  操纵检查：TARGET 谓词进最终需求集 {m.get('in_final')}/{m.get('n')} = {mrate:.1%}"
          f"（下限 {PRE['manipulation_floor']:.0%}）")
    if mrate < PRE["manipulation_floor"]:
        verdict = "数据不足 —— 干预未被有效实施（操纵检查未过下限）"
    elif tt >= PRE["strong_abs"] and delta >= PRE["strong_delta"]:
        verdict = "H-SPLIT 成立"
    elif tt >= PRE["partial_abs"] and delta >= PRE["partial_delta"]:
        verdict = "H-SPLIT 部分成立"
    elif delta <= PRE["null_delta"]:
        verdict = "H-SPLIT 不成立（H-REVERSE 得到支持）"
    else:
        verdict = "数据不足（落在判据之间）"
    print(f"  ⭐ 判定：{verdict}")

# ⭐ The crux for H-SPLIT vs H-REVERSE: among positions where the ledger's predicate DID make
# it into the final requirement set ("the question got asked"), did a hit follow? H-SPLIT says
# asking is the binding constraint, so asked-positions should convert at a high rate. H-REVERSE
# says the downstream cannot answer these anyway, so asking changes little.
manip_detail = {a: {d[0]: d for d in json.load(open("/tmp/x1intervene/analysis.json"))["manipulation"][a]["detail"]}
                for a in ARMS}
print("\n" + "=" * 92)
print("⭐ 问到了 vs 命中（TARGET，仅计已判且已落盘的位）")
print("=" * 92)
print(f"{'arm':14s}{'问到了→命中':>18s}{'没问到→命中':>18s}")
conv = {}
for a in ARMS:
    asked = [r for r in sorted(TARGET) if (r, a) in hits
             and manip_detail[a].get(r) and manip_detail[a][r][4] is True]
    notasked = [r for r in sorted(TARGET) if (r, a) in hits
                and manip_detail[a].get(r) and manip_detail[a][r][4] is False]
    ah, nh = sum(hits[(r, a)] for r in asked), sum(hits[(r, a)] for r in notasked)
    conv[a] = (ah, len(asked), nh, len(notasked))
    f1 = f"{ah}/{len(asked)}" + (f" = {ah/len(asked):.0%}" if asked else "")
    f2 = f"{nh}/{len(notasked)}" + (f" = {nh/len(notasked):.0%}" if notasked else "")
    print(f"{a:14s}{f1:>18s}{f2:>18s}")
print("\n合并三臂（问到了 vs 没问到，同一套判定口径）：")
A = [sum(conv[a][0] for a in ARMS), sum(conv[a][1] for a in ARMS)]
B = [sum(conv[a][2] for a in ARMS), sum(conv[a][3] for a in ARMS)]
print(f"  问到了 {A[0]}/{A[1]}" + (f" = {A[0]/A[1]:.0%}" if A[1] else "")
      + f"   没问到 {B[0]}/{B[1]}" + (f" = {B[0]/B[1]:.0%}" if B[1] else ""))

print("\n敏感性：剔除崩格后的 TARGET（⛔ 不作为主数字，仅用于看崩格惩罚了谁）")
print(f"{'':22s}" + "".join(f"{a:>18s}" for a in ARMS))
row = []
for a in ARMS:
    h, n = tally(TARGET, a, drop_crashed=True)
    row.append(f"{h}/{n} = {h/n:.1%}" if n else "-")
print(f"{'TARGET(去崩格)':22s}" + "".join(f"{c:>18s}" for c in row))

json.dump({"hits": {f"{r}|{a}": v for (r, a), v in hits.items()},
           "args": {f"{r}|{a}": v for (r, a), v in args_.items()}},
          open("/tmp/x1intervene/verdicts_merged.json", "w"), indent=1, ensure_ascii=False)
print("\n-> /tmp/x1intervene/verdicts_merged.json")
