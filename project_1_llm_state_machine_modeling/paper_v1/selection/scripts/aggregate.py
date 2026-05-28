"""Aggregate codex reviews into SELECTION_REPORT.md.

Reads reviews/*.json + candidates.jsonl, computes total scores, applies
verdict + composite score ranking, and emits:

  - SELECTION_REPORT.md  : full table (emoji-rendered) + top-15 candidate +
                           top-15 backup + dimension breakdown
  - summary.parquet      : machine-readable aggregate (optional, requires pyarrow)
  - summary.csv          : CSV fallback

Scoring composite (independent of codex verdict):
    base = H + G + A + F                                 # 0..12
    weighted = 1.0*H + 0.9*G + 1.0*A + 0.8*F             # tilt to H/A (baseline weakest)
    final = weighted + 0.3 * baseline_difficulty + 0.3 * fcstm_fit

Candidate eligibility:
  - exclusions all false
  - base >= 4  (some meaningful complexity)

Stratification target (12 candidates final): HSM=5-6, EFSM=4-5, FSM=2-3
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

SELECTION_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SELECTION_ROOT.parents[2]
CANDIDATES = SELECTION_ROOT / "candidates.jsonl"
REVIEWS_DIR = SELECTION_ROOT / "reviews"
REPORT_PATH = SELECTION_ROOT / "SELECTION_REPORT.md"
CSV_PATH = SELECTION_ROOT / "summary.csv"
DOMAIN_EMOJI_PATH = SELECTION_ROOT / "domain_emoji.json"


SCORE_EMOJI = {0: "⚪", 1: "🟡", 2: "🟢", 3: "💎"}
VERDICT_EMOJI = {"candidate": "🟢", "backup": "🟡", "exclude": "❌"}


def load_domain_emoji() -> dict[str, str]:
    if DOMAIN_EMOJI_PATH.exists():
        return json.loads(DOMAIN_EMOJI_PATH.read_text(encoding="utf-8"))
    return {}


def build_feature_tags(r: dict) -> str:
    """Synthesize concise emoji-tagged feature highlights from scores + traps + primitives."""
    tags: list[str] = []
    # Score-driven 💎 tags (only when score==3 — strongest signal)
    if r["H"] == 3: tags.append("层次💎")
    if r["G"] == 3: tags.append("算术guard💎")
    if r["A"] == 3: tags.append("丰富动作💎")
    if r["F"] == 3: tags.append("故障恢复💎")
    # Trap-driven tags (rare + strong signals only)
    traps = r.get("trap_signals", {})
    def trap_on(prefix: str) -> bool:
        for k in traps:
            if k.startswith(prefix + "_"):
                return bool((traps.get(k) or {}).get("present"))
        return False
    if trap_on("T6"): tags.append("全局应急🌐")
    if trap_on("T5"): tags.append("复合内行为🧱")
    # Primitive-strong tags
    prims = r.get("primitive_adv", {})
    def prim_strong(prefix: str) -> bool:
        for k in prims:
            if k.startswith(prefix + "_"):
                return int((prims.get(k) or {}).get("strength", 0)) == 2
        return False
    if prim_strong("C3"): tags.append("forced/aspect🔁")
    if prim_strong("C1"): tags.append("深复合DFS🌀")
    return " / ".join(tags) if tags else "—"


def normalize_stm_type(s: str) -> str:
    s = s or ""
    for k in ("HSM", "EFSM", "FSM", "Protocol", "Resource", "Hybrid"):
        if k in s:
            return k
    return "Other"


def load_all() -> list[dict]:
    domain_emoji = load_domain_emoji()
    cands: dict[str, dict] = {}
    with CANDIDATES.open("r", encoding="utf-8") as f:
        for line in f:
            row = json.loads(line)
            cands[row["sample_id"]] = row

    out: list[dict] = []
    for c_id, c in cands.items():
        review_path = REVIEWS_DIR / f"{c_id}.json"
        if not review_path.exists():
            continue
        try:
            r = json.loads(review_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        scores = r.get("scores", {}) or {}

        def s(k: str) -> int:
            v = scores.get(k, {})
            try:
                return int(v.get("score", 0))
            except Exception:
                return 0

        h, g, a, f = s("H_hierarchical"), s("G_guards_arith"), s("A_actions_nontrivial"), s("F_fault_recovery")
        base = h + g + a + f
        weighted = 1.0 * h + 0.9 * g + 1.0 * a + 0.8 * f
        bd_raw = int(r.get("baseline_difficulty", 0) or 0)
        ff_raw = int(r.get("fcstm_fit", 0) or 0)

        # Post-hoc bd_final: count only T2/T4/T5/T6 (STM-CONTENT signals),
        # ignore T1/T3 (NL-STRUCTURE signals, codex over-flags them).
        # T6 (global cross-cutting) auto-uplifts to bd_final=3.
        traps = r.get("bd_trap_signals", {}) or {}
        def trap_on(prefix: str) -> bool:
            for k in traps:
                if k.startswith(prefix + "_"):
                    return bool((traps.get(k) or {}).get("present"))
            return False
        t2, t4, t5, t6 = trap_on("T2"), trap_on("T4"), trap_on("T5"), trap_on("T6")
        bd_content_count = sum([t2, t4, t5, t6])
        if t6:
            bd_final = 3
        elif bd_content_count >= 3:
            bd_final = 3
        elif bd_content_count == 2:
            bd_final = 2
        elif bd_content_count == 1:
            bd_final = 1
        else:
            bd_final = 0

        # Post-hoc ft_final: count primitive_adv breadth_weak (strength≥1) + breadth_strong (==2)
        # ft uses codex's reported ft_raw because v3 prompt's derivation matches our intent.
        ff = ff_raw
        # final = weighted (HGAF) + 0.3·bd_final + 0.3·ft  — bd uses post-hoc, not raw
        final = round(weighted + 0.3 * bd_final + 0.3 * ff, 2)

        excl = r.get("exclusions", {}) or {}
        any_excl = any(bool(excl.get(k)) for k in ("has_parallel", "has_history_restore",
                                                    "only_io_no_stm", "too_thin_for_stm"))
        stm_type = normalize_stm_type(c["entry_meta"].get("stm_type") or c["file_meta"].get("stm_type", ""))
        verdict = r.get("verdict", "exclude")

        # System brief: strip the "X领域的" prefix if present and truncate
        ctrl = c["entry_meta"].get("control_object", "")
        sys_brief = ctrl
        # remove "<emoji>领域的" prefix patterns like "智慧停车领域的"
        import re as _re
        sys_brief = _re.sub(r"^[^领]*领域的", "", sys_brief)
        if len(sys_brief) > 38:
            sys_brief = sys_brief[:37] + "…"

        out.append(
            {
                "sample_id": c_id,
                "paper_slug": c["paper_slug"],
                "entry_idx": c["entry_idx"],
                "entry_title": c["entry_title"],
                "control_object": ctrl,
                "domain_emoji": domain_emoji.get(c["paper_slug"], "❓"),
                "sys_brief": sys_brief,
                "stm_type": stm_type,
                "H": h, "G": g, "A": a, "F": f,
                "base": base,
                "weighted": round(weighted, 2),
                "baseline_difficulty": bd_final,  # post-hoc, replaces codex raw
                "bd_raw": bd_raw,  # keep raw for audit
                "fcstm_fit": ff,
                "final": final,
                "any_excl": any_excl,
                "excl_flags": [k for k, v in excl.items() if v],
                "verdict": verdict,
                "pitch": r.get("one_line_pitch", "")[:200],
                "rationale": r.get("rationale", "")[:600],
                "stm_md_path": c["stm_md_path"],
                "duration_s": r.get("_meta", {}).get("duration_s", 0),
                "trap_signals": r.get("bd_trap_signals", {}),
                "primitive_adv": r.get("ft_primitive_advantage", {}),
            }
        )
    out.sort(key=lambda r: r["final"], reverse=True)
    return out


def pick_pools(rows: list[dict], n_candidate: int = 15, n_backup: int = 15) -> tuple[list[dict], list[dict], list[dict]]:
    """Stratified pick. Returns (candidate_pool, backup_pool, excluded)."""
    # Pool 1: eligible = no excl + base >= 4 + verdict != exclude
    eligible = [r for r in rows if not r["any_excl"] and r["base"] >= 4 and r["verdict"] != "exclude"]
    excluded = [r for r in rows if r not in eligible]

    # Stratification: prefer HSM heavy, EFSM medium, FSM small
    targets = {"HSM": 6, "EFSM": 5, "FSM": 3, "Other": 1}
    candidate: list[dict] = []
    by_type: dict[str, list[dict]] = {}
    for r in eligible:
        by_type.setdefault(r["stm_type"], []).append(r)

    # Fill candidate per-type
    for t, n in targets.items():
        picks = by_type.get(t, [])[:n]
        candidate.extend(picks)
    # If under-filled, top-up from leftover sorted by final
    used = {r["sample_id"] for r in candidate}
    leftover = [r for r in eligible if r["sample_id"] not in used]
    while len(candidate) < n_candidate and leftover:
        candidate.append(leftover.pop(0))
    candidate = candidate[:n_candidate]

    # Backup pool: next n_backup high-scoring eligible not in candidate
    used = {r["sample_id"] for r in candidate}
    backup = [r for r in eligible if r["sample_id"] not in used][:n_backup]

    return candidate, backup, excluded


def s_emoji(score: int) -> str:
    return SCORE_EMOJI.get(int(score), "?")


def render_row(r: dict, idx: int) -> str:
    excl_marker = "❌" if r["any_excl"] else "·"
    feature_tags = build_feature_tags(r)
    sys_brief = r["sys_brief"].replace("|", "/")
    return (
        f"| {idx} | {r['domain_emoji']} | `{r['sample_id']}` | {r['stm_type']} | "
        f"{sys_brief} | {feature_tags} | "
        f"{s_emoji(r['H'])} {r['H']} | {s_emoji(r['G'])} {r['G']} | "
        f"{s_emoji(r['A'])} {r['A']} | {s_emoji(r['F'])} {r['F']} | "
        f"**{r['final']}** | {r['baseline_difficulty']}/{r['fcstm_fit']} | "
        f"{VERDICT_EMOJI.get(r['verdict'], '?')} | {excl_marker} |"
    )


TABLE_HEADER = (
    "| # | 🌐 | sample_id | type | 系统简述 | 关注特性 | H | G | A | F | final | bd/ft | V | excl |\n"
    "|---:|:-:|---|---|---|---|:-:|:-:|:-:|:-:|---:|:-:|:-:|:-:|\n"
)


def render_report(rows: list[dict], candidate: list[dict], backup: list[dict], excluded: list[dict]) -> str:
    n_total = len(rows)
    n_eligible = n_total - len(excluded)

    # Dimension breakdown
    dim_dist: dict[str, dict[int, int]] = {k: {0: 0, 1: 0, 2: 0, 3: 0} for k in ("H", "G", "A", "F")}
    for r in rows:
        for k in ("H", "G", "A", "F"):
            dim_dist[k][int(r[k])] += 1

    by_type: dict[str, int] = {}
    for r in rows:
        by_type[r["stm_type"]] = by_type.get(r["stm_type"], 0) + 1

    by_type_cand: dict[str, int] = {}
    for r in candidate:
        by_type_cand[r["stm_type"]] = by_type_cand.get(r["stm_type"], 0) + 1

    lines: list[str] = []
    lines.append("# Path 1 候选样本选样报告（codex 自动评审）\n")
    lines.append("> **产出位置**：`project_1_llm_state_machine_modeling/paper_v1/selection/SELECTION_REPORT.md`\n")
    lines.append("> **数据来源**：`sources/` T0+🟢 子集 × codex (gpt-5.5) `--sandbox read-only` 全文阅读评分\n")
    lines.append("> **scoring rubric**：H 层次 / G 守卫算术 / A 动作非平凡 / F 故障恢复，每维 0-3，对应 baseline 自报 F1 最低的 3 个组件 (actions=0.34 / guards=0.42 / hierarchical=~0.5)\n")
    lines.append("\n")

    lines.append("## 评分图例\n\n")
    lines.append("| 分数 | Emoji | 含义 |\n")
    lines.append("|:-:|:-:|---|\n")
    lines.append("| 0 | ⚪ | 缺失 / 无信号 |\n")
    lines.append("| 1 | 🟡 | 浅 / 表面提及 |\n")
    lines.append("| 2 | 🟢 | 明确存在 |\n")
    lines.append("| 3 | 💎 | 强 / 定义性特征 |\n\n")
    lines.append("Verdict：🟢 candidate / 🟡 backup / ❌ exclude；excl：❌ 命中硬排除（parallel / history / IO-only / too_thin）\n\n")
    lines.append("**领域 emoji 图例**（与 [`sources/SUMMARY.md`](../../sources/SUMMARY.md) 一致）：\n\n")
    lines.append("🚗 汽车与道路车辆 / 🚆 轨道交通 / ✈️ 航空航天 / 🩺 医疗设备 / 🏭 工业自动化 / 🏢 楼宇机电 / 🌡️ 过程与环境 / 🚦 道路交通信号 / 🅿️ 智慧停车 / ⚙️ 通用控制 / 🧩 建模工程 / 🔐 安全分析\n\n")
    lines.append("**关注特性 tag 图例**（基于评分 + trap + primitive 派生）：\n\n")
    lines.append("| tag | 含义 | 触发条件 |\n")
    lines.append("|---|---|---|\n")
    lines.append("| 层次💎 | hierarchy 强 | H==3 |\n")
    lines.append("| 算术guard💎 | 多变量算术 guard | G==3 |\n")
    lines.append("| 丰富动作💎 | 非平凡 action | A==3 |\n")
    lines.append("| 故障恢复💎 | 显式故障恢复 | F==3 |\n")
    lines.append("| 全局应急🌐 | 跨状态全局 escape | T6 trap=True |\n")
    lines.append("| 复合内行为🧱 | 复合状态自身行为 | T5 trap=True |\n")
    lines.append("| forced/aspect🔁 | pyfcstm C3 强 | C3 strength=2 |\n")
    lines.append("| 深复合DFS🌀 | pyfcstm C1 强 | C1 strength=2 |\n\n")

    lines.append("## 总览统计\n\n")
    lines.append(f"- 已评审 sample 总数：**{n_total}**（T0+🟢 候选池 = 323）\n")
    lines.append(f"- 通过硬排除 + base≥4 的合格样本：**{n_eligible}**\n")
    lines.append(f"- 最终选定候选 (Top-15)：**{len(candidate)}**\n")
    lines.append(f"- 备选 (Backup-15)：**{len(backup)}**\n")
    lines.append(f"- 排除 / 不合格：**{len(excluded)}**\n\n")

    lines.append("### STM 类型分布\n\n")
    lines.append("| STM 类型 | 评审样本数 | 候选池 (15) | 目标 |\n")
    lines.append("|---|---:|---:|---|\n")
    lines.append(f"| HSM | {by_type.get('HSM', 0)} | {by_type_cand.get('HSM', 0)} | 5-6 |\n")
    lines.append(f"| EFSM | {by_type.get('EFSM', 0)} | {by_type_cand.get('EFSM', 0)} | 4-5 |\n")
    lines.append(f"| FSM | {by_type.get('FSM', 0)} | {by_type_cand.get('FSM', 0)} | 2-3 |\n")
    lines.append(f"| Other | {by_type.get('Other', 0)} + {by_type.get('Protocol', 0)} + {by_type.get('Resource', 0)} | {by_type_cand.get('Other', 0)} | ≤1 |\n\n")

    lines.append("### 维度命中分布\n\n")
    lines.append("| 维度 | ⚪ 0 | 🟡 1 | 🟢 2 | 💎 3 |\n")
    lines.append("|---|---:|---:|---:|---:|\n")
    for k in ("H", "G", "A", "F"):
        d = dim_dist[k]
        lines.append(f"| {k} | {d[0]} | {d[1]} | {d[2]} | {d[3]} |\n")
    lines.append("\n")

    # bd / ft full distribution
    bd_dist = {0: 0, 1: 0, 2: 0, 3: 0}
    ft_dist = {0: 0, 1: 0, 2: 0, 3: 0}
    for r in rows:
        bd_dist[r["baseline_difficulty"]] = bd_dist.get(r["baseline_difficulty"], 0) + 1
        ft_dist[r["fcstm_fit"]] = ft_dist.get(r["fcstm_fit"], 0) + 1
    lines.append("### bd / ft 分布（重设计 prompt 后）\n\n")
    lines.append("| 维度 | ⚪ 0 | 🟡 1 | 🟢 2 | 💎 3 |\n")
    lines.append("|---|---:|---:|---:|---:|\n")
    lines.append(f"| bd | {bd_dist.get(0,0)} | {bd_dist.get(1,0)} | {bd_dist.get(2,0)} | {bd_dist.get(3,0)} |\n")
    lines.append(f"| ft | {ft_dist.get(0,0)} | {ft_dist.get(1,0)} | {ft_dist.get(2,0)} | {ft_dist.get(3,0)} |\n\n")

    # Trap signal frequencies
    trap_keys = ("T1_cross_section_element", "T2_implicit_domain_term", "T3_implicit_action_from_prose",
                 "T4_multivar_arith_guard", "T5_composite_internal_behavior", "T6_global_cross_cutting_recovery")
    prim_keys = ("C1_speculative_dfs", "C2_expr_ir_smt", "C3_forced_and_aspect", "C4_abstract_action")
    trap_counts = {k: 0 for k in trap_keys}
    prim_strengths = {k: [0, 0, 0] for k in prim_keys}  # [strength=0, 1, 2]
    n_with_trap = 0
    n_with_prim = 0
    for r in rows:
        traps = r.get("trap_signals") or {}
        if traps:
            n_with_trap += 1
            for k in trap_keys:
                if (traps.get(k) or {}).get("present"):
                    trap_counts[k] += 1
        prims = r.get("primitive_adv") or {}
        if prims:
            n_with_prim += 1
            for k in prim_keys:
                s = int((prims.get(k) or {}).get("strength", 0))
                if 0 <= s <= 2:
                    prim_strengths[k][s] += 1
    if n_with_trap > 0:
        lines.append("### bd 命中 trap 频率（来自 baseline 自报 failure 模式）\n\n")
        lines.append("| Trap | 命中样本数 | 占比 |\n")
        lines.append("|---|---:|---:|\n")
        for k in trap_keys:
            lines.append(f"| {k} | {trap_counts[k]} | {trap_counts[k]/max(n_with_trap,1)*100:.1f}% |\n")
        lines.append(f"\n（统计基数：含 trap_signals 字段的样本 = {n_with_trap}）\n\n")
    if n_with_prim > 0:
        lines.append("### ft pyfcstm primitive 优势强度分布\n\n")
        lines.append("| Primitive | ⚪ 0 (none) | 🟡 1 (weak) | 🟢 2 (strong) |\n")
        lines.append("|---|---:|---:|---:|\n")
        for k in prim_keys:
            s = prim_strengths[k]
            lines.append(f"| {k} | {s[0]} | {s[1]} | {s[2]} |\n")
        lines.append(f"\n（统计基数：含 primitive_advantage 字段的样本 = {n_with_prim}）\n\n")

    # ---------- Candidate Top-15 ----------
    lines.append("## 候选池 — Top 15（推荐主用）\n\n")
    lines.append("> 列说明：🌐 领域 / 系统简述 (来自 STM.md `控制对象`) / 关注特性 (基于 H/G/A/F + trap + primitive 派生的高信号 emoji 标签)\n\n")
    lines.append(TABLE_HEADER)
    for i, r in enumerate(candidate, 1):
        lines.append(render_row(r, i) + "\n")
    lines.append("\n")

    for i, r in enumerate(candidate, 1):
        lines.append(f"### 候选 #{i}: {r['domain_emoji']} `{r['sample_id']}`\n\n")
        lines.append(f"- **领域**：{r['domain_emoji']}　|　**STM 类型**：{r['stm_type']}\n")
        lines.append(f"- **控制对象**：{r['control_object']}\n")
        lines.append(f"- **关注特性**：{build_feature_tags(r)}\n")
        lines.append(f"- **评分**：H={s_emoji(r['H'])}{r['H']} G={s_emoji(r['G'])}{r['G']} A={s_emoji(r['A'])}{r['A']} F={s_emoji(r['F'])}{r['F']}，final=**{r['final']}**，bd={r['baseline_difficulty']}，ft={r['fcstm_fit']}\n")
        lines.append(f"- **pitch**：{r['pitch']}\n")
        lines.append(f"- **rationale**：{r['rationale']}\n")
        lines.append(f"- **STM.md**：[`{r['stm_md_path']}`](../../{r['stm_md_path'].split('project_1_llm_state_machine_modeling/')[-1]})\n\n")

    # ---------- Backup ----------
    lines.append("## 备选池 — Backup 15\n\n")
    lines.append(TABLE_HEADER)
    for i, r in enumerate(backup, 1):
        lines.append(render_row(r, i) + "\n")
    lines.append("\n")

    # ---------- Full table ----------
    lines.append("## 全量评审表（按 final 降序，含被排除样本）\n\n")
    lines.append(TABLE_HEADER)
    for i, r in enumerate(rows, 1):
        lines.append(render_row(r, i) + "\n")
    lines.append("\n")

    return "".join(lines)


def main() -> None:
    rows = load_all()
    if not rows:
        print("[aggregate] no reviews found yet", file=sys.stderr)
        return
    candidate, backup, excluded = pick_pools(rows)
    md = render_report(rows, candidate, backup, excluded)
    REPORT_PATH.write_text(md, encoding="utf-8")

    # CSV summary
    with CSV_PATH.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["rank", "sample_id", "paper_slug", "stm_type", "H", "G", "A", "F",
                    "base", "weighted", "baseline_difficulty", "fcstm_fit", "final",
                    "verdict", "any_excl", "excl_flags", "pitch"])
        for i, r in enumerate(rows, 1):
            w.writerow([i, r["sample_id"], r["paper_slug"], r["stm_type"], r["H"], r["G"], r["A"], r["F"],
                        r["base"], r["weighted"], r["baseline_difficulty"], r["fcstm_fit"], r["final"],
                        r["verdict"], r["any_excl"], ";".join(r["excl_flags"]), r["pitch"]])

    print(f"[aggregate] rows={len(rows)} eligible={len(rows)-len(excluded)} "
          f"candidate={len(candidate)} backup={len(backup)} excluded={len(excluded)}")
    print(f"  wrote: {REPORT_PATH.relative_to(REPO_ROOT)}")
    print(f"  wrote: {CSV_PATH.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
