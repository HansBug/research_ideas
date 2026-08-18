#!/usr/bin/env python3
"""Build per-case bundle .md for human audit.

Usage:  build_bundle.py <id>

Reads:
  - pool.tsv (case metadata)
  - expansions/<id>.json (English expanded NL with [E] markers + provenance)
  - codex_drafts/<id>.fcstm (ref DSL)
  - codex_drafts/<id>.scenarios.json (test scenarios)
  - codex_drafts/<id>.notes.md (codex design notes)
  - codex_drafts/<id>.result.json (codex final validation JSON)
  - claude_reviews/<id>.json (claude cross-review)
  - verifier_logs/<id>.final_verify.log

Writes:
  - bundles/<id>.md (one-stop human review file)

Chinese NL translation is also generated inline using a quick local fallback
heuristic; if user wants higher quality translation, can be regenerated.
"""
from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # path2_selection/
POOL = ROOT / "pool.tsv"
EXPANSIONS = ROOT / "expansions"
RS = ROOT / "ref_stms"


def load_pool() -> dict:
    pool = {}
    with open(POOL) as f:
        for row in csv.DictReader(f, delimiter="\t"):
            pool[row["id"]] = row
    return pool


def load_expansion(cid: str) -> dict:
    p = EXPANSIONS / f"{cid}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def load_codex(cid: str) -> tuple[str, str, dict, str]:
    fcstm = RS / "codex_drafts" / f"{cid}.fcstm"
    scenarios = RS / "codex_drafts" / f"{cid}.scenarios.json"
    notes = RS / "codex_drafts" / f"{cid}.notes.md"
    result = RS / "codex_drafts" / f"{cid}.result.json"
    return (
        fcstm.read_text() if fcstm.exists() else "",
        scenarios.read_text() if scenarios.exists() else "",
        json.loads(result.read_text()) if result.exists() else {},
        notes.read_text() if notes.exists() else "",
    )


def load_claude(cid: str) -> dict:
    p = RS / "claude_reviews" / f"{cid}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def load_verify_log(cid: str) -> str:
    p = RS / "verifier_logs" / f"{cid}.final_verify.log"
    return p.read_text() if p.exists() else "(no verify log)"


def render_diagram(cid: str, fcstm_path: Path) -> tuple[str, str]:
    """Render the fcstm to SVG (and PlantUML source) via pyfcstm CLI.

    Returns (svg_relpath_from_bundle, puml_relpath_from_bundle) for embedding.
    """
    import subprocess
    if not fcstm_path.exists() or fcstm_path.stat().st_size == 0:
        return ("", "")
    svg_out = RS / "diagrams" / f"{cid}.svg"
    puml_out = RS / "diagrams" / f"{cid}.puml"
    svg_out.parent.mkdir(parents=True, exist_ok=True)
    # SVG
    try:
        subprocess.run(
            ["python3", "pyfcstm/pyfcstm_cli.py", "visualize",
             "-i", str(fcstm_path),
             "-o", str(svg_out),
             "-t", "svg",
             "-l", "normal",
             "--no-open"],
            cwd=str(Path(__file__).resolve().parent.parent.parent.parent.parent.parent),  # repo root
            capture_output=True, text=True, timeout=120, check=False,
        )
    except Exception:
        pass
    # PlantUML source
    try:
        subprocess.run(
            ["python3", "pyfcstm/pyfcstm_cli.py", "plantuml",
             "-i", str(fcstm_path),
             "-o", str(puml_out),
             "-l", "normal"],
            cwd=str(Path(__file__).resolve().parent.parent.parent.parent.parent.parent),
            capture_output=True, text=True, timeout=60, check=False,
        )
    except Exception:
        pass
    # Relative paths from bundles/<id>.md location (one level up from diagrams/)
    svg_rel = f"../diagrams/{cid}.svg" if svg_out.exists() and svg_out.stat().st_size > 0 else ""
    puml_rel = f"../diagrams/{cid}.puml" if puml_out.exists() and puml_out.stat().st_size > 0 else ""
    return (svg_rel, puml_rel)


def generate_cn_translation(cid: str, expanded_nl: str) -> str:
    """Translate expanded_nl to Chinese via claude CLI, preserving [E] markers.

    Cached to <RS>/translations/<id>.cn.txt. Returns the translation string
    (or a placeholder if generation fails).
    """
    import subprocess
    cache = RS / "translations" / f"{cid}.cn.txt"
    if cache.exists() and cache.stat().st_size > 50:
        return cache.read_text()
    cache.parent.mkdir(parents=True, exist_ok=True)

    prompt = (
        "Translate the following English NL into clear technical Chinese, preserving every "
        "[En] inline citation marker exactly where it appears in the English text. Use one "
        "single Chinese paragraph (no line breaks, no markdown). Do not add explanations.\n\n"
        f"<English NL>\n{expanded_nl}\n</English NL>\n\n"
        "Output the Chinese translation only — no JSON, no fences, no preface."
    )
    try:
        r = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json"],
            capture_output=True, text=True, timeout=180, check=False,
        )
        if r.returncode != 0:
            return f"(译文生成失败 rc={r.returncode}; stderr 末段: {r.stderr[-200:]})"
        env = json.loads(r.stdout)
        if env.get("is_error"):
            return f"(译文生成失败: {env.get('result','unknown')[:200]})"
        text = (env.get("result") or "").strip()
        # Strip optional ``` fence
        if text.startswith("```"):
            nl = text.find("\n")
            if nl >= 0:
                text = text[nl+1:]
            if text.rstrip().endswith("```"):
                text = text.rstrip()[:-3]
        text = text.strip()
        # Strip any leading explanatory `★ Insight ─` block — find first Chinese sentence
        if text.startswith("`★"):
            import re as _re
            m = _re.search(r"[一-鿿]", text)
            if m:
                text = text[m.start():].strip()
        if not text:
            return "(译文为空)"
        cache.write_text(text)
        return text
    except subprocess.TimeoutExpired:
        return "(译文生成超时)"
    except Exception as e:
        return f"(译文生成异常: {type(e).__name__}: {str(e)[:200]})"


def main():
    if len(sys.argv) != 2:
        print("usage: build_bundle.py <id>", file=sys.stderr)
        sys.exit(1)
    cid = sys.argv[1]

    pool = load_pool()
    if cid not in pool:
        print(f"unknown case_id {cid}", file=sys.stderr)
        sys.exit(2)
    pr = pool[cid]
    exp = load_expansion(cid)
    fcstm_src, scenarios_json, result_json, notes_md = load_codex(cid)
    claude_rev = load_claude(cid)
    verify_log = load_verify_log(cid)

    case_name = pr.get("case_name", "?")
    bucket = pr.get("bucket", "?")
    domain = pr.get("domain", "?")
    paper_slug = pr.get("paper_slug", "?")
    paper_num = pr.get("paper_num", "?")

    expanded_nl = exp.get("expanded_nl", "(no expansion available)")
    provenance = exp.get("provenance", [])

    out_lines = []

    # YAML frontmatter
    out_lines.append("---")
    out_lines.append(f"case_id: {cid}")
    out_lines.append(f"paper_slug: {paper_slug}")
    out_lines.append(f"paper_num: {paper_num}")
    out_lines.append(f"case_name: \"{case_name}\"")
    out_lines.append(f"bucket: {bucket}")
    out_lines.append(f"domain: \"{domain}\"")
    out_lines.append("generation:")
    fv = result_json.get("final_validation", {}) if result_json else {}
    out_lines.append(f"  codex_iterations: {result_json.get('iterations', '?')}")
    out_lines.append(f"  pyfcstm_parse: {fv.get('parse', '?')}")
    out_lines.append(f"  pyfcstm_sem: {fv.get('sem', '?')}")
    out_lines.append(f"  pyfcstm_sim_smoke: {fv.get('sim', '?')}")
    out_lines.append(f"  scenarios_total: {fv.get('scenarios_total', '?')}")
    out_lines.append(f"  scenarios_pass: {fv.get('scenarios_pass', '?')}")
    out_lines.append(f"  scenarios_fail: {fv.get('scenarios_fail', '?')}")
    out_lines.append(f"  claude_verdict: {claude_rev.get('verdict', '(pending)')}")
    out_lines.append("---")
    out_lines.append("")

    # Header
    out_lines.append(f"# Case `{cid}` {domain} — {case_name}")
    out_lines.append("")
    out_lines.append(f"**Bucket**: {bucket}  |  **Paper**: #{paper_num} `{paper_slug}`")
    out_lines.append("")
    out_lines.append(f"- [STM.md case section](../../../sources/{paper_slug}/STM.md)")
    out_lines.append(f"- [paper PDF](../../../sources/{paper_slug}/paper.pdf)")
    out_lines.append(f"- [expansion NL JSON (含 provenance)](../expansions/{cid}.json)")
    out_lines.append(f"- [codex 起草笔记](../ref_stms/codex_drafts/{cid}.notes.md)")
    out_lines.append("")

    # §1 English NL (with [E] markers)
    out_lines.append("## 1. 英文 NL（含 inline [E] 溯源 markers）")
    out_lines.append("")
    out_lines.append("> 这是 codex 评审阶段生成的扩充 NL（commit `259e6ea7`），每条 substantive 信息带 `[En]` 标记。完整 provenance 表见 [expansion JSON](../expansions/" + cid + ".json)。")
    out_lines.append("")
    out_lines.append(expanded_nl)
    out_lines.append("")

    # §2 Chinese NL — inline claude translation
    out_lines.append("## 2. 中文 NL 译文（claude 翻译，保留 [En] markers）")
    out_lines.append("")
    cn_translation = generate_cn_translation(cid, expanded_nl) if expanded_nl and "(no expansion" not in expanded_nl else "(无 expansion，无法译文)"
    out_lines.append(cn_translation)
    out_lines.append("")
    # Also append review-level summaries as quick anchors
    what_it_is = exp.get("what_it_is") or ""
    feats = exp.get("features_we_care_about") or ""
    if what_it_is or feats:
        out_lines.append("**速读锚点（来自 codex review 阶段）**：")
        out_lines.append("")
        if what_it_is:
            out_lines.append(f"- **系统简述**：{what_it_is}")
        if feats:
            out_lines.append(f"- **关注特性**：{feats}")
        out_lines.append("")

    # §3 ref pyfcstm STM
    out_lines.append("## 3. Reference pyfcstm STM (codex 起草，待用户签字)")
    out_lines.append("")
    # Render diagram first
    fcstm_path = RS / "codex_drafts" / f"{cid}.fcstm"
    svg_rel, puml_rel = render_diagram(cid, fcstm_path)
    if svg_rel:
        out_lines.append(f"### 3.1 状态机图（pyfcstm visualize SVG）")
        out_lines.append("")
        out_lines.append(f"![Case {cid} state diagram]({svg_rel})")
        out_lines.append("")
        if puml_rel:
            out_lines.append(f"PlantUML 源文件：[`{puml_rel}`]({puml_rel})")
            out_lines.append("")
        out_lines.append(f"### 3.2 pyfcstm DSL 源码")
        out_lines.append("")
    out_lines.append("```pyfcstm")
    out_lines.append(fcstm_src if fcstm_src else "(no DSL generated)")
    out_lines.append("```")
    out_lines.append("")
    if result_json:
        c_used = result_json.get("c_axis_used", {})
        cov = result_json.get("scenario_coverage_summary", {})
        out_lines.append("**codex 自报 C-axis 使用情况**:")
        for c in ["C1", "C2", "C3", "C4"]:
            used = c_used.get(c, "?")
            out_lines.append(f"- {c}: {'✓' if used is True else ('✗' if used is False else '?')}")
        out_lines.append("")
        out_lines.append("**codex 自报 scenarios 覆盖情况**:")
        for k, label in [
            ("modes_covered", "模式数"),
            ("guards_covered", "guards 数"),
            ("fault_paths_covered", "fault paths 数"),
            ("per_cycle_behaviors_covered", "per-cycle 行为数"),
            ("effectors_covered", "硬件 effectors 数"),
        ]:
            v = cov.get(k, "?")
            out_lines.append(f"- {label}: {v}")
        out_lines.append("")

    # §4 scenarios.json
    out_lines.append("## 4. Test scenarios（覆盖 NL 全特性，必须 100% pass）")
    out_lines.append("")
    if scenarios_json:
        out_lines.append("```json")
        out_lines.append(scenarios_json.strip())
        out_lines.append("```")
    else:
        out_lines.append("(no scenarios.json)")
    out_lines.append("")

    # §5 pyfcstm verifier log
    out_lines.append("## 5. pyfcstm 验证日志（parse + sem + sim + scenarios 全跑）")
    out_lines.append("")
    out_lines.append("```")
    out_lines.append(verify_log.strip()[:5000])
    out_lines.append("```")
    out_lines.append("")

    # §6 codex notes
    out_lines.append("## 6. Codex 起草笔记")
    out_lines.append("")
    if notes_md:
        out_lines.append(notes_md.strip())
    else:
        out_lines.append("(no codex notes)")
    out_lines.append("")

    # §7 claude review
    out_lines.append("## 7. Claude 交叉评审")
    out_lines.append("")
    if claude_rev:
        out_lines.append(f"**Verdict**: {claude_rev.get('verdict', '?')}")
        out_lines.append("")
        scores = claude_rev.get("scores", {})
        out_lines.append("| 维度 | 打分 | evidence |")
        out_lines.append("|---|---|---|")
        for k, label in [
            ("semantic_correctness", "语义正确性"),
            ("nl_faithfulness", "NL 忠实性"),
            ("c_axis_grounding_appropriateness", "C-axis grounding 恰当性"),
            ("nl_coverage", "scenarios NL 覆盖度"),
        ]:
            sc = scores.get(k, {})
            emoji = sc.get("emoji", "?")
            ev = (sc.get("evidence", "") or "").replace("|", "\\|").replace("\n", " ").strip()
            if len(ev) > 200:
                ev = ev[:197] + "…"
            out_lines.append(f"| {label} | {emoji} | {ev} |")
        out_lines.append("")
        halls = claude_rev.get("hallucinations_found", [])
        if halls:
            out_lines.append("**Hallucination 检查**:")
            for h in halls:
                out_lines.append(f"- `{h.get('type','?')}` `{h.get('name','?')}`: {h.get('issue','')}")
            out_lines.append("")
        sug = claude_rev.get("specific_revision_suggestions", [])
        if sug:
            out_lines.append("**修订建议**:")
            for s in sug:
                out_lines.append(f"- {s}")
            out_lines.append("")
        miss = claude_rev.get("missing_scenarios_suggestions", [])
        if miss:
            out_lines.append("**缺失 scenarios 建议**:")
            for s in miss:
                out_lines.append(f"- {s}")
            out_lines.append("")
        overall = claude_rev.get("overall_comment", "")
        if overall:
            out_lines.append(f"**总评**: {overall}")
            out_lines.append("")
    else:
        out_lines.append("(claude 评审尚未跑)")
        out_lines.append("")

    # §8 user audit zone
    out_lines.append("## 8. 用户审阅区（待签字）")
    out_lines.append("")
    out_lines.append("**审阅状态**：⬜ 待审 / ⬜ approve / ⬜ revise / ⬜ rewrite")
    out_lines.append("")
    out_lines.append("**审阅笔记**（用户填写）：")
    out_lines.append("")
    out_lines.append("- ")
    out_lines.append("")
    out_lines.append("**修订要求**（用户填写）：")
    out_lines.append("")
    out_lines.append("- ")
    out_lines.append("")
    out_lines.append("**签字**：（用户填写日期 + 姓名）")
    out_lines.append("")
    out_lines.append("---")
    out_lines.append("")
    out_lines.append(f"**最终 ref 落盘路径（待签字后）**: `audited/{cid}.fcstm` + `audited/{cid}.audit.md`")

    bundle_path = RS / "bundles" / f"{cid}.md"
    bundle_path.parent.mkdir(parents=True, exist_ok=True)
    bundle_path.write_text("\n".join(out_lines))
    print(f"[{cid}] bundle wrote {bundle_path}")


if __name__ == "__main__":
    main()
