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
  rejected_issues         发现了但被结构门丢弃（C1 起：裁决层的结构校验不再杀格，改为丢弃并记录）
  issue_citations_pruned  发现被保留，但其中引用了归因层拒绝的证据，该引用被剪除

后三类若只看 issues 列表，全部表现为「没发现」，而修法方向截然不同——一个要放宽归因，
一个要重新设计角色语义，一个要调预算。前十八代次只看 issues，这可能正是「分析没有触及
根本」的一个具体来源。

⚠️ 这个脚本曾经在真实路径上**输出零行并 exit 0**。`BASE` 写死成 `matrix-i175`、轮次目录名
写死成 `<gen>run<N>`，而 v20 起的实际布局是 `runs/paper1/matrix-<gen>/run<N>`；模型 glob 写死
`*-claude`，而 v22 起有两条臂。零行输出与「所有格都没发现任何东西」在终端上完全一样 —— 对一个
存在理由就是「防止三种不同的失败被读成同一个未发现」的脚本，这是最坏的失败形态。

所以路径与格集不再写死：代次目录按 `matrix-<gen>` 与 `<gen>run<N>` 两种布局都试，模型臂从目录
名解析，且**找不到任何格时非零退出并说明找过哪些路径**。

用法：
    present_for_judgment.py v21                  # 全部轮次、全部臂
    present_for_judgment.py v22 --pair 0047      # 单个 pair
    present_for_judgment.py v22 --arm gpt        # 单条臂
    present_for_judgment.py v22 --full           # 不截断（判定时应当用这个）
"""
import argparse, json, pathlib, sys, collections
HERE = pathlib.Path(__file__).resolve().parent
LED = json.loads((HERE / "manual_review" / "expected_issue_set.json").read_text())
RUNS = HERE.parents[2] / "runs" / "paper1"
# hold-out 与分带机制已于 2026-08-09 永久移除：方法在这批 pair 上迭代，全部记录同等参与度量。
REPORTABLE: set = set()
# EIS-0047-03 干净但被 initialization_anchored 门结构性封死（预注册 §9.1）。它若报未命中，
# 那是门的抑制，不是能力缺口 —— 判定时必须看见这句话，否则会被记成未命中。
BLOCKED = {"EIS-0047-03": "被 initialization_anchored 门封死（预注册 §9.1）：两条编码都绑 "
                          "source=[*] 且 trigger 不在上电词表里，八种组合全拒"}


def _round_dirs(gen: str):
    """代次的轮次目录，两种历史布局都试，并把试过的路径报出来。"""
    tried, found = [], []
    for rnd in (1, 2, 3):
        for candidate in (RUNS / f"matrix-{gen}" / f"run{rnd}", RUNS / f"{gen}run{rnd}",
                          RUNS / f"matrix-{gen}" / f"{gen}run{rnd}"):
            tried.append(candidate)
            if candidate.is_dir():
                found.append((rnd, candidate))
                break
    return found, tried

def expected(pair):
    out=[]
    for r in LED["records"]:
        if str(r["pair"])[-4:]==pair and r.get("in_scope") is True and r.get("expressible_with_closed_vocabulary") is True:
            out.append(r)
    return out

ap = argparse.ArgumentParser(description="并列呈现，不做判定")
ap.add_argument("gen", help="代次前缀，如 v21 / v22")
ap.add_argument("--pair", help="只看一个 pair")
ap.add_argument("--arm", help="只看一条臂，如 claude / gpt")
ap.add_argument("--compact", action="store_true",
                help="台账每 pair 只打一次，每格只列 issue 标题与四类计数。"
                     "为 324 格全量判定而加：默认模式下台账在同一 pair 内被重复打印 6 遍，"
                     "48 个 pair 约 8500 行。**四类「没发现」的计数一个都不省** —— "
                     "省掉它们会让判定者把「被门丢弃」读成「从未发现」，那正是本脚本要防的事")
ap.add_argument("--full", action="store_true",
                help="不截断台账 statement 与模型 detail。判定时应当用这个："
                     "170/230 字符的截断线曾把台账自己的结论子句切掉")
args = ap.parse_args()
gen, only, arm = args.gen, args.pair, args.arm
LIM_LED = 10**9 if args.full else 170
LIM_MOD = 10**9 if args.full else 230

#: compact 模式下已打印过台账的 pair。
_LEDGER_PRINTED: set = set()

rounds, tried = _round_dirs(gen)
if not rounds:
    print(f"找不到 {gen} 的任何轮次目录。试过：", file=sys.stderr)
    for path in tried:
        print(f"  {path}", file=sys.stderr)
    # 零行输出与「什么都没发现」不可区分，所以这里必须非零退出。
    raise SystemExit(2)

shown = 0
for rnd, base in rounds:
    cells = sorted(c for c in base.iterdir() if c.is_dir() and "-" in c.name)
    for cell in cells:
        pair, _, this_arm = cell.name.partition("-")
        if only and pair != only: continue
        if arm and this_arm != arm: continue
        shown += 1
        f = cell/"discover-completed.json"
        tag = "可报" if any(r["id"] in REPORTABLE for r in expected(pair)) else "不进分母"
        if not f.exists():
            fail = cell/"discover-failed.json"
            print(f"\n{'='*100}\n{gen} run{rnd} {pair}-{this_arm} [{tag}]  ** {'FAILED: '+json.loads(fail.read_text()).get('error_type','?') if fail.exists() else 'IN PROGRESS'} **")
            continue
        d = json.loads(f.read_text())
        iss = d.get("issues") or []
        print(f"\n{'='*100}\n{gen} run{rnd} {pair}-{this_arm} [{tag}]  coverage={d.get('coverage_status')}  issues={len(iss)}")
        # compact：台账每 pair 只打一次。判定者在同一 pair 的 6 个格之间来回看时，
        # 重复的台账文本只增加行数不增加信息。
        if args.compact and pair in _LEDGER_PRINTED:
            print("-- 台账期望：见本 pair 首格 --")
        else:
            _LEDGER_PRINTED.add(pair)
            print("-- 台账期望（可判定） --")
            for r in expected(pair):
                rid = r["id"]
                # 两种资格，见 build_gist 同处注释。
                if rid in REPORTABLE:
                    elig = "★可报——承载能力主张"
                    if rid in BLOCKED: elig += f"，但 {BLOCKED[rid]}"
                else:
                    elig = "不进能力分母（NL 越界或边界裁定剔除）"
                print(f"   {rid}  {r['layer']}/{r.get('direction')}  pred={r.get('primary_predicate')}  [{elig}]")
                print(f"      {r['statement'][:LIM_LED]}")
        print(f"-- 模型产出（attribution: {[x.get('attribution_status') for x in iss]}） --")
        for i,x in enumerate(iss,1):
            t = x.get("title") or x.get("summary") or ""
            print(f"   [{i}] {t[:LIM_MOD]}")
            det = (x.get("description") or x.get("detail") or x.get("rationale") or "")
            if det and not args.compact: print(f"       {det[:LIM_MOD]}")

        # 「从未发现」与「发现了但被丢掉」是两种不同的失败，根因不同，必须分开看。
        recon = d.get("adjudication_reconciliation") or {}
        for key, label in (("excluded_findings", "被排除的发现"),
                           ("excluded_observations", "被排除的观察"),
                           ("coverage_gaps", "自报覆盖缺口"),
                           ("@rejected_issues", "被结构门丢弃的发现"),
                           ("@rejected_exclusions", "被结构门丢弃的排除项"),
                           ("@issue_citations_pruned", "被剪除的引用（发现仍保留）"),
                           # 这两类同样是丢发现，而上一版没印。`unaccounted_safe_false_assertions`
                           # 是「safe 且为 False 却无人认领」——与「从未发现」根因完全不同；
                           # `unsupported_issues_dropped` 是门把已成形的 issue 丢掉。v21 上前者
                           # 恰好与同格的 rejected_issues 同时出现，所以没漏——那是数据巧合。
                           ("@unaccounted_safe_false_assertions", "safe 且为 False 但无人认领的断言"),
                           ("@unsupported_issues_dropped", "被判无支撑而丢弃的 issue"),
                           ("@thin_merge_warnings", "同质合并过薄告警"),
                           ("@misfiled_findings_moved", "错档后被移动的发现")):
            # `@` 前缀的键来自 adjudication_reconciliation，不在顶层。
            # 这一类必须单列：一个被结构门丢弃的发现，若不显示出来，在判定者眼里与
            # 「从未发现」完全一样，而两者的根因和修法截然不同——前者是管线致因的漏检。
            rows = (recon.get(key[1:]) if key.startswith("@") else d.get(key)) or []
            if not rows:
                continue
            print(f"-- {label}（{len(rows)}）--")
            for x in ([] if args.compact else rows[:8]):
                if isinstance(x, dict):
                    txt = x.get("title") or x.get("statement") or x.get("reason") or x.get("detail") or json.dumps(x, ensure_ascii=False)
                    why = x.get("reason") or x.get("exclusion_reason") or ""
                    print(f"   * {str(txt)[:150]}")
                    if why and why != txt: print(f"     理由: {str(why)[:150]}")
                else:
                    print(f"   * {str(x)[:150]}")

if not shown:
    print(f"{gen} 的轮次目录存在，但一个格都没匹配上"
          f"（--pair={only!r} --arm={arm!r}）", file=sys.stderr)
    raise SystemExit(2)
print(f"\n{'='*100}\n共呈现 {shown} 格。可报记录 {len(REPORTABLE)} 条：{sorted(REPORTABLE)}")
if BLOCKED:
    for rid, why in BLOCKED.items():
        print(f"⚠️ {rid} {why}")
