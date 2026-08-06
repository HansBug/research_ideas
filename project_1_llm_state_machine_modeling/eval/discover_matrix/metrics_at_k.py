"""从人工判定表算 metric@k。**脚本不做匹配、不读模型输出——只做算术。**

分工是刻意的：判定由人工做（见 present_for_judgment.py 的理由），算术由脚本做。脚本读不到
模型输出，所以它不可能"顺手"把判定也做了。

输入是一个 JSON：{"verdicts": {"EIS-0007-01": [1,0,1], ...}, "over": {"0007": [2,1,0], ...}}
其中三元组是 run1/run2/run3 的人工判定：1=命中，0=未命中，null=该轮该格失败（不计入分母）。
over 是每轮的多报条数（人工认定为「不在台账内且确为误报」的条目数）。

hit@1    = 命中数 / 有效(条目,轮次)对数        —— 一次运行的期望产出
hit@3    = 至少一轮命中的条目比例              —— 该缺陷是否在能力范围内
hit@all  = 全部有效轮次都命中的条目比例        —— 稳定性
over@1   = 每轮平均多报数
over@any = 出现过多报的格子数
"""
import json, sys, collections, pathlib

d = json.loads(pathlib.Path(sys.argv[1]).read_text())
V = d["verdicts"]; O = d.get("over", {})
_FROZEN = json.loads((pathlib.Path(__file__).resolve().parent / "holdout.json").read_text())
# 三带，不是两带。`holdout` 里有三个 pair 因为参与了 A1 的编写（0018/0038 是动机，0048 同
# NL 组）而不再能支撑能力主张；把它们留在 hold-out 带里，等于让「方法+样本共演化」的观测
# 冒充样本外证据。它们照常全量报出，只是单独成带。
HOLD = set(_FROZEN.get("reportable_holdout") or _FROZEN["holdout"])
BURNED = set(_FROZEN.get("burned") or {})

def group(ids, name):
    if not ids: return
    pairs_n = 0; hits = 0; at3 = 0; atall = 0; items = 0
    rows = []
    for k in sorted(ids):
        v = [x for x in V[k] if x is not None]
        if not v: rows.append((k, V[k], "全轮失败")); continue
        items += 1; pairs_n += len(v); hits += sum(v)
        a3 = 1 if any(v) else 0; aa = 1 if all(v) else 0
        at3 += a3; atall += aa
        if len(v) < 2:
            # n=1 时 hit@all 与 hit@1 退化为同一个数，说「稳定」是从单点断言稳定性。
            kind = f"轮次不足({len(v)}轮)，不得据此说稳定"
        else:
            kind = "稳定命中" if aa else ("hit@3 only" if a3 else "全轮未命中")
        rows.append((k, V[k], kind))
    print(f"\n### {name}   条目={items}  有效(条目,轮次)={pairs_n}")
    print(f"hit@1   = {hits}/{pairs_n} = {hits/pairs_n*100:.1f}%")
    print(f"hit@3   = {at3}/{items} = {at3/items*100:.1f}%")
    print(f"hit@all = {atall}/{items} = {atall/items*100:.1f}%")
    thin = [k for k in sorted(ids) if len([x for x in V[k] if x is not None]) in (1, 2)]
    if thin:
        print(f"!! 轮次不足 3 的条目 {len(thin)} 个：{thin}。hit@all 在这些条目上不构成稳定性证据。")
    for k, raw, kind in rows: print(f"   {k:16} {raw}  {kind}")

hold_ids = [k for k in V if k.split("-")[1] in HOLD]
burn_ids = [k for k in V if k.split("-")[1] in BURNED]
hist_ids = [k for k in V if k.split("-")[1] not in HOLD and k.split("-")[1] not in BURNED]
group(hold_ids, "HOLD-OUT（能力主张的唯一依据）")
group(burn_ids, "已烧毁 hold-out（方法+样本共演化观测，不作能力主张）")
group(hist_ids, "历史四格（共同演化观测，不作能力主张）")

if O:
    print("\n### 多报")
    for name, keep in (("hold-out", lambda p: p in HOLD),
                       ("已烧毁 hold-out", lambda p: p in BURNED),
                       ("历史四格", lambda p: p not in HOLD and p not in BURNED)):
        sel = {p: v for p, v in O.items() if keep(p)}
        vals = [x for v in sel.values() for x in v if x is not None]
        if not vals:
            continue
        any_n = sum(1 for v in sel.values() if any(x for x in v if x))
        print(f"  {name}: over@1 = {sum(vals)}/{len(vals)} = {sum(vals)/len(vals):.2f} 条/轮"
              f"   over@any = {any_n} 个格子")
        for p_, v in sorted(sel.items()):
            print(f"     {p_}: {v}")
