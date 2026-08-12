"""Build BLINDED judging material for x1-split-intervention.

Per pair: full NL, full PlantUML author source, untruncated ledger statements, and the three
arms' complete output rendered as 甲 / 乙 under a per-pair random mapping.

⛔ Nothing is truncated: the v46 judging used --compact and that is a known defect.
⛔ The arm identity is never written into the material; the key goes to a separate file that
   judges do not receive.
"""
import json, pathlib, random, sys

REPO = pathlib.Path("/home/zhangshaoang/oo-projects/research_ideas-3")
R = REPO / "runs/paper1"
ARM_DIR = {"control": R / "x1-split-intervention/control",
           "treatment_v1": R / "x1-split-intervention/treatment",
           "treatment_v2": R / "x1-split-intervention-v2/treatment_v2"}
DM = REPO / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/discover_matrix"
PAIRDIR = REPO / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/representation/reports/llms_emp_r45_java_60/pairs"
MAT = pathlib.Path("/tmp/x1intervene/material")
MAT.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(DM))
import metrics_at_k as M
REPORTABLE = set(M.REPORTABLE)

GRID = json.load(open("/tmp/x1intervene/grid.json"))
PAIRS = GRID["pairs"]
LED = json.load(open(DM / "manual_review/expected_issue_set.json"))["records"]

rng = random.Random(20260812)
key = {}


def render_arm(cell: pathlib.Path) -> str:
    f = cell / "discover-completed.json"
    if not f.exists():
        fail = cell / "discover-failed.json"
        if fail.exists():
            d = json.loads(fail.read_text())
            # the failure record carries `error_message`, not `error`
            msg = d.get("error_message") or d.get("error") or ""
            return (f"**该格运行失败**：`{d.get('error_type','?')}` — {str(msg)[:500]}\n\n"
                    f"该格没有任何已发布 issue。\n")
        return "**该格未落盘（运行中或失败且无失败文件）**\n"
    d = json.loads(f.read_text())
    L = []
    iss = d.get("issues") or []
    L.append(f"`coverage_status = {d.get('coverage_status')}`，已发布 issue **{len(iss)}** 条。\n")
    if not iss:
        L.append("（无已发布 issue）\n")
    for i, x in enumerate(iss, 1):
        L.append(f"**[{i}] {x.get('title','')}**\n")
        L.append(f"- `attribution_status` = `{x.get('attribution_status')}`")
        if x.get("shared_root_cause"):
            L.append(f"- 共同根因：{x['shared_root_cause']}")
        if x.get("shared_elements"):
            L.append(f"- 涉及元素：`{'`, `'.join(str(e) for e in x['shared_elements'])}`")
        r = x.get("rationale") or x.get("description") or x.get("detail") or ""
        if r:
            L.append(f"- 论证：{r}")
        L.append("")
    # the four "found but not published" categories -- omitting them makes a
    # gate-discarded finding indistinguishable from never having been found
    for field, label in (("excluded_findings", "被归因策略排除的发现"),
                         ("excluded_observations", "被证据角色制度静默的观察"),
                         ("coverage_gaps", "预算耗尽的覆盖缺口"),
                         ("rejected_issues", "被结构门丢弃的 issue")):
        v = d.get(field) or []
        if v:
            L.append(f"\n**{label}（{len(v)} 条）**\n")
            for e in v:
                L.append(f"- {json.dumps(e, ensure_ascii=False)}")
    return "\n".join(L) + "\n"


for pair in PAIRS:
    arms = ["control", "treatment_v1", "treatment_v2"]
    rng.shuffle(arms)
    key[pair] = {"甲": arms[0], "乙": arms[1], "丙": arms[2]}
    # ⚠️ present_for_judgment.expected() filters on `expressible_with_closed_vocabulary`, which
    # drops EIS-0005-03 -- a REPORTABLE record and a member of this experiment's REGRESSION set.
    # The capability denominator is REPORTABLE, so filter on that and keep every graded record.
    want = set(GRID["target"]) | set(GRID["regression"])
    recs = [r for r in LED if str(r["pair"])[-4:] == pair and r.get("in_scope") is True
            and (r["id"] in want or r.get("expressible_with_closed_vocabulary") is True)]

    L = [f"# 判定材料 · pair {pair}\n",
         "## 一 · 需求原文（NL 全文）\n", "```text",
         (PAIRDIR / pair / "nl.txt").read_text().strip(), "```\n",
         "## 二 · 被审模型（PlantUML 作者源全文）\n", "```plantuml",
         (PAIRDIR / pair / "plantuml.puml").read_text().strip(), "```\n",
         f"## 三 · 台账期望记录（{len(recs)} 条，statement 未截断）\n"]
    for r in recs:
        elig = "★进能力分母" if r["id"] in REPORTABLE else "不进能力分母（NL 越界或边界裁定剔除）"
        L.append(f"### {r['id']}  [{elig}]\n")
        L.append(f"- `layer` = `{r['layer']}` / `direction` = `{r.get('direction')}`")
        L.append(f"- `primary_predicate` = `{r.get('primary_predicate')}`")
        L.append(f"\n{r['statement']}\n")
        if r.get("nl_evidence"):
            L.append(f"**NL 依据**：{r['nl_evidence']}\n")
    L.append("## 四 · 三份模型产出\n")
    for tag in ("甲", "乙", "丙"):
        L.append(f"### 产出 {tag}\n")
        L.append(render_arm(ARM_DIR[key[pair][tag]] / f"{pair}-claude"))
    (MAT / f"pair-{pair}.md").write_text("\n".join(L))
    print(f"pair {pair}: {len(recs)} records, material {(MAT/f'pair-{pair}.md').stat().st_size:,} bytes")

json.dump(key, open("/tmp/x1intervene/blind_key.json", "w"), indent=1, ensure_ascii=False)
print("\nkey -> /tmp/x1intervene/blind_key.json  (⛔ judges must not see this)")
