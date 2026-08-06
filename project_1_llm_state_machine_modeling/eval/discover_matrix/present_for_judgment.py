"""并列呈现每格的模型产出与该 pair 的台账期望。**不做匹配、不给判定。**

判定必须人工逐条做，这是既定纪律，理由在 v20run1 上得到了直接证据：两条模型产出触及了
正确的元素、却得出与台账**相反**的结论（台账记「守卫晚一条边，未充电时仍可进入 X」= 可达性
过强，模型报「运行时不可达」= 可达性不足；台账记「只有 fork_state 类型正确」，模型报
「fork_state 类型错」）。任何按标题或元素相似度对齐的脚本都会把这两条判成命中。

本脚本的职责因此严格限定为「把两侧摆在一起，并把三类失败区分开」：

  issues                  已发布的条目
  excluded_findings       发现了但被归因策略排除
  excluded_observations   发现了但被证据角色制度静默（supporting_false 不能开 issue）
  coverage_gaps           发现了但预算耗尽

后三类若只看 issues 列表，全部表现为「没发现」，而修法方向截然不同——一个要放宽归因，
一个要重新设计角色语义，一个要调预算。前十八代次只看 issues，这可能正是「分析没有触及
根本」的一个具体来源。

用法：python present_for_judgment.py [代次前缀] [可选的单个 pair]
"""
import json, pathlib, sys, collections
HERE = pathlib.Path(__file__).resolve().parent
LED = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
BASE = HERE.parents[2] / "runs" / "paper1" / "matrix-i175"
HOLD = set(json.loads((HERE / "holdout.json").read_text())["holdout"])

def expected(pair):
    out=[]
    for r in LED["records"]:
        if str(r["pair"])[-4:]==pair and r.get("in_scope") is True and r.get("expressible_with_closed_vocabulary") is True:
            out.append(r)
    return out

gen = sys.argv[1] if len(sys.argv)>1 else "v19"
only = sys.argv[2] if len(sys.argv)>2 else None
for rnd in (1,2,3):
    for cell in sorted((BASE/f"{gen}run{rnd}").glob("*-claude")) if (BASE/f"{gen}run{rnd}").is_dir() else []:
        pair = cell.name.split("-")[0]
        if only and pair!=only: continue
        f = cell/"discover-completed.json"
        tag = "HOLDOUT" if pair in HOLD else "hist"
        if not f.exists():
            fail = cell/"discover-failed.json"
            print(f"\n{'='*100}\n{gen}run{rnd} {pair} [{tag}]  ** {'FAILED: '+json.loads(fail.read_text()).get('error_type','?') if fail.exists() else 'IN PROGRESS'} **")
            continue
        d = json.loads(f.read_text())
        iss = d.get("issues") or []
        print(f"\n{'='*100}\n{gen}run{rnd} {pair} [{tag}]  coverage={d.get('coverage_status')}  issues={len(iss)}")
        print("-- 台账期望（可判定） --")
        for r in expected(pair):
            print(f"   {r['id']}  {r['layer']}/{r.get('direction')}  pred={r.get('primary_predicate')}")
            print(f"      {r['statement'][:170]}")
        print(f"-- 模型产出（attribution: {[x.get('attribution_status') for x in iss]}） --")
        for i,x in enumerate(iss,1):
            t = x.get("title") or x.get("summary") or ""
            print(f"   [{i}] {t[:170]}")
            det = (x.get("description") or x.get("detail") or x.get("rationale") or "")
            if det: print(f"       {det[:230]}")

        # 「从未发现」与「发现了但被丢掉」是两种不同的失败，根因不同，必须分开看。
        for key, label in (("excluded_findings", "被排除的发现"),
                           ("excluded_observations", "被排除的观察"),
                           ("coverage_gaps", "自报覆盖缺口")):
            rows = d.get(key) or []
            if not rows:
                continue
            print(f"-- {label}（{len(rows)}）--")
            for x in rows[:8]:
                if isinstance(x, dict):
                    txt = x.get("title") or x.get("statement") or x.get("reason") or x.get("detail") or json.dumps(x, ensure_ascii=False)
                    why = x.get("reason") or x.get("exclusion_reason") or ""
                    print(f"   * {str(txt)[:150]}")
                    if why and why != txt: print(f"     理由: {str(why)[:150]}")
                else:
                    print(f"   * {str(x)[:150]}")
