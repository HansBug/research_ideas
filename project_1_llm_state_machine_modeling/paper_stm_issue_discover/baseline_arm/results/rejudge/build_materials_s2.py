#!/usr/bin/env python3
"""为抽样出的 80 个主臂位重建「与 X1 同等信息量」的判定材料。

⛔ 材料里绝不出现：原判定的 hit / equivalence_form / argument、样本归属（miss 样本还是
hit 样本）、台账的 primary_predicate / layer / direction / assertions / replay / verdict。
⭐ 材料里必须出现（这正是主臂原判定所缺的四样）：NL 全文、PlantUML 作者源全文、
未截断的 issue 全文、以及 X1 的「倾向命中」判定顺序（在指令文件里）。
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

PAPER = Path(
    "/home/zhangshaoang/oo-projects/research_ideas-3/project_1_llm_state_machine_modeling"
    "/paper_stm_issue_discover"
)
# ⚠️⚠️ 2026-08-17：第一版台账、v46 与 v46 时代脚本已整体归档。
# ⛔ 本臂的 588 网格工装（`expected_issue_set.json` 的 98 条分母、`metrics_at_k` 等）
# 属**第一版台账口径**，故 `MATRIX` 重定向到归档树；⭐ 当前口径的 X1v2 结果在
# `discover_matrix/ledger_v2/X1V2_RESULTS.md`，与本处工装无关。
MATRIX = PAPER / "archive" / "r10_ledger_v1_and_v46"
CORPUS = PAPER / "pipeline" / "representation" / "reports" / "llms_emp_r45_java_60" / "pairs"
RUN_ROOT = Path("/home/zhangshaoang/oo-projects/research_ideas/runs/paper1/matrix-v46-full")
OUT = Path("/tmp/x1reju/materials_s2")

FALLOUT_BLOCKS = (
    ("excluded_findings", "被归因策略排除的发现"),
    ("excluded_observations", "被证据角色制度静默的观察"),
    ("coverage_gaps", "自报覆盖缺口（预算耗尽等）"),
    ("@rejected_issues", "被结构门丢弃的发现"),
    ("@rejected_exclusions", "被结构门丢弃的排除项"),
    ("@issue_citations_pruned", "被剪除的引用（发现仍保留）"),
    ("@unaccounted_safe_false_assertions", "safe 且为 False 但无人认领的断言"),
    ("@unsupported_issues_dropped", "被判无支撑而丢弃的 issue"),
)


def released_table(cell_dir: Path) -> str:
    path = cell_dir / "loops" / "discover.md"
    if not path.is_file():
        return "_（该格无 discover.md）_"
    text = path.read_text(encoding="utf-8")
    marker = "## Released Results And Evidence"
    i = text.find(marker)
    if i < 0:
        return "_（该格 discover.md 无 Released Results And Evidence 段）_"
    rest = text[i + len(marker):]
    m = re.search(r"\n#{2,3} ", rest)
    return rest[: m.start()].strip() if m else rest.strip()


def render_cell(cell_dir: Path, label: str) -> str:
    out: list[str] = []
    f = cell_dir / "discover-completed.json"
    if not f.is_file():
        return f"### {label} — ⚠️ **格缺失 / 格失败**（该位记 `null`，⛔ 不记 0）\n"
    d = json.loads(f.read_text(encoding="utf-8"))
    issues = d.get("issues") or []
    out.append(f"### {label} — 发布了 {len(issues)} 条 issue，coverage_status = `{d.get('coverage_status')}`")
    out.append("")
    if not issues:
        out.append("⚠️ **本格未发布任何 issue。**")
        out.append("")
    for idx, x in enumerate(issues, 1):
        out.append(f"**[{idx}]** {str(x.get('title') or '').strip()}")
        out.append("")
        out.append(f"- **issue_id**：`{x.get('issue_id')}`")
        out.append(f"- **requirement_ids**：{x.get('requirement_ids')}　**assertion_ids**：{x.get('assertion_ids')}")
        out.append(f"- **attribution_status**：`{x.get('attribution_status')}`")
        out.append(f"- **rationale（⛔ 未截断）**：{str(x.get('rationale') or '').strip()}")
        out.append("")

    out.append("#### 该格的已发布断言与结果（证据上下文）")
    out.append("")
    out.append(released_table(cell_dir))
    out.append("")

    recon = d.get("adjudication_reconciliation") or {}
    printed = False
    for key, label_zh in FALLOUT_BLOCKS:
        rows = (recon.get(key[1:]) if key.startswith("@") else d.get(key)) or []
        if not rows:
            continue
        if not printed:
            out.append(
                "#### ⛔ 以下区块**不计入命中**（对应 X1 材料里的 `analysis`）——"
                "呈现它们只是为了让判定者看到本格想到了什么"
            )
            out.append("")
            printed = True
        out.append(f"**{label_zh}（{len(rows)}）**")
        out.append("")
        for x in rows:
            if isinstance(x, dict):
                txt = x.get("title") or x.get("statement") or x.get("reason") or json.dumps(x, ensure_ascii=False)
                why = x.get("rationale") or x.get("reason") or x.get("exclusion_reason") or ""
                out.append(f"- {str(txt).strip()}")
                if why and why != txt:
                    out.append(f"  - 理由：{str(why).strip()}")
            else:
                out.append(f"- {str(x).strip()}")
        out.append("")
    return "\n".join(out)


def main() -> None:
    sample = json.loads(Path("/tmp/x1reju/sample_ext.json").read_text(encoding="utf-8"))
    rows = sample["sample_hit_stage2"]
    ledger = {
        r["id"]: r
        for r in json.loads((MATRIX / "manual_review" / "expected_issue_set.json").read_text())["records"]
    }

    by_pair: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_pair[r["pair"]].append(r)

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.md"):
        old.unlink()

    manifest = []
    for seq, pair in enumerate(sorted(by_pair), 1):
        entries = sorted(by_pair[pair], key=lambda r: (r["record_id"], r["run"], r["model"]))
        record_ids = sorted({e["record_id"] for e in entries})
        cells = sorted({(e["run"], e["model"]) for e in entries})

        nl = (CORPUS / pair / "nl.txt").read_text(encoding="utf-8").strip()
        puml = (CORPUS / pair / "plantuml.puml").read_text(encoding="utf-8").strip()

        lines: list[str] = []
        lines.append(f"# 重判材料 S{seq:02d} · pair {pair}")
        lines.append("")
        lines.append(
            "> ⛔ **本文件不含任何既有判定结果**。判据只有一条：**这一格所表达的命题，"
            "与台账那条记录所表达的命题，是否指向同一个作者源缺陷。**"
        )
        lines.append(">")
        lines.append(
            "> ⭐ 判缺陷时读下面的 **PlantUML 作者源**，⛔ 不读 `model.fcstm`（编译产物）。"
        )
        lines.append("")
        lines.append("## 一、需求原文（NL，全文）")
        lines.append("")
        lines.append("```text")
        lines.append(nl)
        lines.append("```")
        lines.append("")
        lines.append("## 二、被审模型（PlantUML 作者源，全文）")
        lines.append("")
        lines.append("```plantuml")
        lines.append(puml)
        lines.append("```")
        lines.append("")
        lines.append(f"## 三、台账期望（本材料涉及 {len(record_ids)} 条）")
        lines.append("")
        for rid in record_ids:
            rec = ledger[rid]
            lines.append(f"### {rid}")
            lines.append("")
            lines.append(str(rec.get("statement") or "").strip())
            lines.append("")
            ev = str(rec.get("nl_evidence") or "").strip()
            if ev:
                lines.append(f"**NL 出处**：{ev}")
                lines.append("")
            sup = str(rec.get("basis_superseded_by_ruling") or "").strip()
            if sup:
                lines.append(
                    "⛔ **本条的原判据已被裁定部分撤回，判定时必须按撤回后的判据读，"
                    "⛔ 不得按上面 statement 里已被放弃的那部分归因：**"
                )
                lines.append("")
                lines.append(f"> {sup}")
                lines.append("")
        lines.append("## 四、被审格的完整产出（⛔ 未截断）")
        lines.append("")
        for run, model in cells:
            lines.append(render_cell(RUN_ROOT / f"run{run}" / f"{pair}-{model}", f"run{run} · {model}"))
            lines.append("")
        lines.append("## 五、要填的位")
        lines.append("")
        lines.append(f"本材料共 **{len(entries)} 位**，⛔ 一个都不能漏。位键逐字如下：")
        lines.append("")
        for e in entries:
            lines.append(f"- `{e['key']}`")
        lines.append("")
        (OUT / f"{seq:02d}-{pair}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
        manifest.append({"seq": seq, "pair": pair, "file": f"{seq:02d}-{pair}.md",
                         "positions": [e["key"] for e in entries]})

    Path("/tmp/x1reju/materials_s2_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    total = sum(len(m["positions"]) for m in manifest)
    print(f"wrote {len(manifest)} pair materials, {total} positions -> {OUT}")
    sizes = sorted(((OUT / m["file"]).stat().st_size, m["file"]) for m in manifest)
    print("smallest:", sizes[:3])
    print("largest:", sizes[-3:])
    print("total bytes:", sum(s for s, _ in sizes))


if __name__ == "__main__":
    main()
