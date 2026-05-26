#!/usr/bin/env python3
"""Aggregate codex review results -> REPORT.md.

Reads:
  - pool.tsv (authoritative bucket/case_name/paths)
  - results/<id>.json (codex review)

Writes:
  - REPORT.md (full 239 table + 15 candidates + 15 backup)

Selection rule (user-approved):
  - Total candidates: 15  (HSM 6 + EFSM 6 + FSM 3)
  - Backup pool:       15 (same distribution)

Ranking within bucket:
  - 4-axis weighted score (per bucket different axis priorities)
  - Tie-break: verdict tier > axis sum > scale richness
  - For EFSM bucket: enforce >=3 candidates have C2 score ∈ {🟢}
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
POOL = ROOT / "pool.tsv"
RESULTS_DIR = ROOT / "results"
REPORT = ROOT / "REPORT.md"

SCORE_MAP = {"🟢": 3, "🟡": 2, "🟠": 1, "⚪": 0}
VERDICT_TIER = {"💎 STRONG": 4, "✨ GOOD": 3, "🟢 OK": 2, "🔘 WEAK": 1}

# Per-bucket axis weights — reflects which contribution each bucket should anchor
BUCKET_AXIS_WEIGHT = {
    "HSM-layered":    {"C1": 3.0, "C2": 1.0, "C3": 2.5, "C4": 1.5},  # C1+C3 主战场
    "EFSM-interlock": {"C1": 0.5, "C2": 3.0, "C3": 1.0, "C4": 2.0},  # C2+C4 主战场
    "FSM-basic":      {"C1": 0.5, "C2": 1.0, "C3": 0.5, "C4": 2.5},  # C4 baseline
}

CANDIDATE_QUOTA = {"HSM-layered": 6, "EFSM-interlock": 6, "FSM-basic": 3}
BACKUP_QUOTA    = {"HSM-layered": 6, "EFSM-interlock": 6, "FSM-basic": 3}

# Cases above this state count get auto-bumped from candidates to backup
# (sprint NL should not be too unwieldy for LLM agent loop reasoning)
MAX_CANDIDATE_STATES = 20


def load_pool() -> dict[str, dict]:
    """id -> {bucket, slug, case_name, stm_path, paper_pdf, paper_content, paper_num}"""
    pool = {}
    with open(POOL) as f:
        rdr = csv.DictReader(f, delimiter="\t")
        for row in rdr:
            pool[row["id"]] = row
    return pool


def load_results(pool: dict) -> list[dict]:
    """Return list of merged records: pool row + codex review."""
    records = []
    for jp in sorted(RESULTS_DIR.glob("*.json")):
        cid = jp.stem
        if cid not in pool:
            continue
        try:
            data = json.loads(jp.read_text())
        except Exception as e:
            print(f"[warn] skip broken {jp}: {e}")
            continue
        # Override bucket from pool (codex sometimes renames)
        data["bucket"] = pool[cid]["bucket"]
        data["paper_slug"] = pool[cid]["paper_slug"]
        data["case_name"] = pool[cid]["case_name"]
        data["paper_num"] = pool[cid]["paper_num"]
        data["domain"] = pool[cid].get("domain", "?")
        data["_id"] = cid
        records.append(data)
    return records


def axis_scores(rec: dict) -> dict[str, int]:
    ax = rec.get("axes", {})
    out = {}
    for k_key, c_key in [
        ("C1", "C1_dead_end_potential"),
        ("C2", "C2_numerical_guard_richness"),
        ("C3", "C3_forced_fault_recovery"),
        ("C4", "C4_hardware_decoupling"),
    ]:
        s = ax.get(c_key, {}).get("score", "⚪")
        # First character is the emoji
        first = s[0] if s else "⚪"
        out[k_key] = SCORE_MAP.get(first, 0)
    return out


def composite(rec: dict) -> float:
    ax = axis_scores(rec)
    bucket = rec["bucket"]
    w = BUCKET_AXIS_WEIGHT[bucket]
    return sum(ax[k] * w[k] for k in ax)


def verdict_tier(rec: dict) -> int:
    v = rec.get("verdict", "")
    for k, t in VERDICT_TIER.items():
        if k in v:
            return t
    return 0


def scale_sum(rec: dict) -> int:
    sc = rec.get("scale", {}) or {}
    return sum(int(sc.get(k, 0) or 0) for k in ("state_count", "event_count", "variable_count", "transition_count"))


def rank_key(rec: dict) -> tuple:
    # Higher is better
    return (composite(rec), verdict_tier(rec), scale_sum(rec))


def _states(r: dict) -> int:
    return int(r.get("scale", {}).get("state_count", 0) or 0)


def pick(records: list[dict]):
    """Return (candidates, backup) lists obeying quotas.

    Cases with state_count > MAX_CANDIDATE_STATES are ineligible for candidates
    (they fall to backup automatically by being filtered out of the candidate
    pool but ranked normally for backup).
    """
    by_bucket: dict[str, list[dict]] = {b: [] for b in CANDIDATE_QUOTA}
    for r in records:
        by_bucket[r["bucket"]].append(r)
    for b in by_bucket:
        by_bucket[b].sort(key=rank_key, reverse=True)

    candidates = []
    backup = []

    # EFSM C2 enforcement (+ size filter)
    efsm = by_bucket["EFSM-interlock"]
    efsm_eligible = [r for r in efsm if _states(r) <= MAX_CANDIDATE_STATES]
    efsm_quota = CANDIDATE_QUOTA["EFSM-interlock"]
    c2_strong = [r for r in efsm_eligible if axis_scores(r)["C2"] == 3]
    c2_strong_picked = c2_strong[:3]
    c2_strong_ids = {r["_id"] for r in c2_strong_picked}
    other_efsm = [r for r in efsm_eligible if r["_id"] not in c2_strong_ids]
    efsm_candidates = c2_strong_picked + other_efsm[: efsm_quota - len(c2_strong_picked)]
    if len(efsm_candidates) < efsm_quota:
        already = {r["_id"] for r in efsm_candidates}
        for r in efsm_eligible:
            if r["_id"] not in already:
                efsm_candidates.append(r)
                if len(efsm_candidates) >= efsm_quota:
                    break
    efsm_candidates_ids = {r["_id"] for r in efsm_candidates}
    candidates.extend(efsm_candidates)
    # Backup = all remaining (including oversized), ranked
    backup.extend([r for r in efsm if r["_id"] not in efsm_candidates_ids][: BACKUP_QUOTA["EFSM-interlock"]])

    # HSM + FSM: top-N from size-eligible, backup includes oversized
    for b in ("HSM-layered", "FSM-basic"):
        lst = by_bucket[b]
        eligible = [r for r in lst if _states(r) <= MAX_CANDIDATE_STATES]
        cand = eligible[: CANDIDATE_QUOTA[b]]
        cand_ids = {r["_id"] for r in cand}
        candidates.extend(cand)
        remaining = [r for r in lst if r["_id"] not in cand_ids]
        backup.extend(remaining[: BACKUP_QUOTA[b]])

    return candidates, backup


def render_row(rec: dict) -> str:
    ax = rec.get("axes", {})
    def s(k):
        v = ax.get(k, {}).get("score", "⚪")
        return v[0] if v else "⚪"
    sc = rec.get("scale", {}) or {}
    verdict = rec.get("verdict", "?")
    verdict_short = verdict.split()[0] if verdict else "?"
    case = rec["case_name"]
    if len(case) > 60:
        case = case[:57] + "..."
    return (
        f"| {rec['_id']} "
        f"| {rec.get('domain','?')} "
        f"| {rec['bucket'].split('-')[0]} "
        f"| {s('C1_dead_end_potential')} "
        f"| {s('C2_numerical_guard_richness')} "
        f"| {s('C3_forced_fault_recovery')} "
        f"| {s('C4_hardware_decoupling')} "
        f"| {verdict_short} "
        f"| {sc.get('state_count','?')} / {sc.get('event_count','?')} / {sc.get('variable_count','?')} / {sc.get('transition_count','?')} "
        f"| [{case}](../../../sources/{rec['paper_slug']}/STM.md) "
        f"|"
    )


def _md_cell(s: str, limit: int = 160) -> str:
    """Make a string safe for a markdown table cell + truncate."""
    if not s:
        return "—"
    # Replace pipe & newline so the cell stays one logical row
    s = s.replace("|", "\\|").replace("\n", " ").replace("\r", " ").strip()
    # Collapse internal whitespace
    while "  " in s:
        s = s.replace("  ", " ")
    if len(s) > limit:
        s = s[: limit - 1].rstrip() + "…"
    return s


def render_overview_table(records: list[dict]) -> list[str]:
    """At-a-glance table for the candidate / backup pool."""
    lines = []
    lines.append(
        "| 序 | id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | scale (S/E/V/T) "
        "| 案例 | 系统简述 | 我们关注的特性 |"
    )
    lines.append("|---:|---|---|---|---|---|---|---|---|---|---|---|---|")
    bucket_order = {"HSM-layered": 0, "EFSM-interlock": 1, "FSM-basic": 2}
    grouped: dict[str, list[dict]] = {}
    for r in records:
        grouped.setdefault(r["bucket"], []).append(r)
    seq = 0
    for b in sorted(grouped, key=lambda k: bucket_order[k]):
        for r in grouped[b]:
            seq += 1
            ax = r.get("axes", {})
            def s(k):
                v = ax.get(k, {}).get("score", "⚪")
                return v[0] if v else "⚪"
            sc = r.get("scale", {}) or {}
            verdict = r.get("verdict", "?")
            verdict_short = verdict.split()[0] if verdict else "?"
            case = r["case_name"]
            case_disp = case if len(case) <= 50 else case[:47] + "…"
            what = _md_cell(r.get("what_it_is", ""), limit=180)
            feats = _md_cell(r.get("features_we_care_about", ""), limit=180)
            lines.append(
                f"| {seq} | {r['_id']} | {r.get('domain','?')} | {r['bucket'].split('-')[0]} "
                f"| {s('C1_dead_end_potential')} | {s('C2_numerical_guard_richness')} "
                f"| {s('C3_forced_fault_recovery')} | {s('C4_hardware_decoupling')} "
                f"| {verdict_short} "
                f"| {sc.get('state_count','?')}/{sc.get('event_count','?')}/{sc.get('variable_count','?')}/{sc.get('transition_count','?')} "
                f"| [{case_disp}](../../../sources/{r['paper_slug']}/STM.md) "
                f"| {what} "
                f"| {feats} |"
            )
    return lines


def render_card(rec: dict, rank: int) -> str:
    ax = rec.get("axes", {})
    def line(k, label):
        v = ax.get(k, {})
        return f"- **{label}**: {v.get('score','⚪')} — {v.get('evidence','—')}"
    return (
        f"##### {rank}. `[{rec['_id']}]` {rec.get('domain','?')} {rec['case_name']} ({rec['bucket']})\n"
        f"\n"
        f"- **领域**: {rec.get('domain','?')}\n"
        f"- **论文**: paper #{rec['paper_num']} [`{rec['paper_slug']}`](../../../sources/{rec['paper_slug']}/STM.md)\n"
        f"- **是什么**: {rec.get('what_it_is','?')}\n"
        f"- **scale**: states={rec.get('scale',{}).get('state_count','?')} / events={rec.get('scale',{}).get('event_count','?')} / vars={rec.get('scale',{}).get('variable_count','?')} / trans={rec.get('scale',{}).get('transition_count','?')}\n"
        f"- **verdict**: {rec.get('verdict','?')}\n"
        f"{line('C1_dead_end_potential', 'C1 多模式 dead-end')}\n"
        f"{line('C2_numerical_guard_richness', 'C2 数值守卫')}\n"
        f"{line('C3_forced_fault_recovery', 'C3 forced fault')}\n"
        f"{line('C4_hardware_decoupling', 'C4 硬件解耦')}\n"
        f"- **对 PATH2 的价值**: {rec.get('features_we_care_about','—')}\n"
        f"- **风险**: {rec.get('potential_pitfalls','—')}\n"
    )


def main():
    pool = load_pool()
    records = load_results(pool)
    print(f"Loaded {len(records)}/{len(pool)} records")
    if not records:
        print("No results yet — nothing to do")
        return

    candidates, backup = pick(records)
    cand_ids = {r["_id"] for r in candidates}
    backup_ids = {r["_id"] for r in backup}

    # Sort everything for full table by bucket then id
    bucket_order = {"HSM-layered": 0, "EFSM-interlock": 1, "FSM-basic": 2}
    records.sort(key=lambda r: (bucket_order[r["bucket"]], r["_id"]))

    # Per-bucket stats
    buckets = {}
    for r in records:
        b = r["bucket"]
        if b not in buckets:
            buckets[b] = []
        buckets[b].append(r)

    lines = []
    lines.append("# PATH2 候选样本 codex 全量评审报告\n")
    lines.append(f"- 候选池大小：**{len(pool)}** 条（T0 严格 + 双 🟢A + 💎 + 纯结构标签）")
    lines.append(f"- 已评审：**{len(records)}** 条")
    lines.append(f"- 候选（15）：HSM {CANDIDATE_QUOTA['HSM-layered']} + EFSM {CANDIDATE_QUOTA['EFSM-interlock']} + FSM {CANDIDATE_QUOTA['FSM-basic']}")
    lines.append(f"- 备选（15）：同分布")
    lines.append("")

    # Emoji legend
    lines.append("## 图例\n")
    lines.append("**axis score**: 🟢 强 / 🟡 中 / 🟠 弱 / ⚪ 无")
    lines.append("")
    lines.append("**verdict**: 💎 STRONG / ✨ GOOD / 🟢 OK / 🔘 WEAK")
    lines.append("")
    lines.append("**bucket**: HSM(-layered) / EFSM(-interlock) / FSM(-basic)")
    lines.append("")
    lines.append("**领域**（与 [sources/SUMMARY.md](../../../sources/SUMMARY.md) 同口径）：")
    lines.append("")
    lines.append("- 🚗 汽车与道路车辆控制 · 🚆 轨道交通与铁路控制 · ✈️ 航空航天与飞行/空管控制 · 🩺 医疗设备与生命支持控制")
    lines.append("- 🏭 工业自动化与离散制造 · 🏢 楼宇机电与电梯控制 · 🌡️ 过程与环境控制 · 🚦 道路交通信号控制")
    lines.append("- 🅿️ 智慧停车与车位管理 · 🧩 建模方法与系统工程 · 🔐 安全/安保分析 · ⚙️ 通用控制与形式化工具")
    lines.append("")

    # Stats per bucket
    lines.append("## 桶级统计\n")
    lines.append("| 桶 | 数量 | 💎 | ✨ | 🟢 | 🔘 | C1≥🟢 | C2≥🟢 | C3≥🟢 | C4≥🟢 |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for b in ("HSM-layered", "EFSM-interlock", "FSM-basic"):
        bs = buckets.get(b, [])
        n = len(bs)
        v_counts = {"💎": 0, "✨": 0, "🟢": 0, "🔘": 0}
        for r in bs:
            for k in v_counts:
                if r.get("verdict","").startswith(k):
                    v_counts[k] += 1
                    break
        c_counts = {f"C{i}":0 for i in (1,2,3,4)}
        for r in bs:
            ax = axis_scores(r)
            for k in c_counts:
                if ax[k] == 3:
                    c_counts[k] += 1
        lines.append(
            f"| {b} | {n} | {v_counts['💎']} | {v_counts['✨']} | {v_counts['🟢']} | {v_counts['🔘']} "
            f"| {c_counts['C1']} | {c_counts['C2']} | {c_counts['C3']} | {c_counts['C4']} |"
        )
    lines.append("")

    # Candidates section
    lines.append("## 🎯 候选池（15）\n")
    lines.append("### 速查表\n")
    lines.extend(render_overview_table(candidates))
    lines.append("")
    lines.append("### 详细卡片\n")
    for b in ("HSM-layered", "EFSM-interlock", "FSM-basic"):
        bcands = [r for r in candidates if r["bucket"] == b]
        lines.append(f"#### {b} （{len(bcands)} 条）\n")
        for i, r in enumerate(bcands, 1):
            lines.append(render_card(r, i))
            lines.append("")
    lines.append("")

    # Backup section
    lines.append("## 🛡️ 备选池（15）\n")
    lines.append("### 速查表\n")
    lines.extend(render_overview_table(backup))
    lines.append("")
    lines.append("### 详细卡片\n")
    for b in ("HSM-layered", "EFSM-interlock", "FSM-basic"):
        bbk = [r for r in backup if r["bucket"] == b]
        lines.append(f"#### {b} （{len(bbk)} 条）\n")
        for i, r in enumerate(bbk, 1):
            lines.append(render_card(r, i))
            lines.append("")
    lines.append("")

    # Full table per bucket
    lines.append("## 📋 全量评审表（按桶）\n")
    header = "| id | 领域 | 桶 | C1 | C2 | C3 | C4 | verdict | states/events/vars/trans | 案例 |"
    sep = "|---|---|---|---|---|---|---|---|---|---|"
    for b in ("HSM-layered", "EFSM-interlock", "FSM-basic"):
        bs = buckets.get(b, [])
        if not bs: continue
        lines.append(f"### {b} （{len(bs)} 条）\n")
        # Sort by candidate first, then composite
        bs_sorted = sorted(bs, key=lambda r: (
            0 if r["_id"] in cand_ids else (1 if r["_id"] in backup_ids else 2),
            -composite(r),
        ))
        lines.append(header)
        lines.append(sep)
        for r in bs_sorted:
            row = render_row(r)
            marker = " 🎯" if r["_id"] in cand_ids else (" 🛡️" if r["_id"] in backup_ids else "")
            row = row[:-1] + marker + " |"
            lines.append(row)
        lines.append("")

    REPORT.write_text("\n".join(lines) + "\n")
    print(f"Wrote {REPORT}")

    # Persistent stable selection manifest
    manifest = {
        "candidates": [
            {"id": r["_id"], "bucket": r["bucket"], "domain": r.get("domain", "?"),
             "paper_slug": r["paper_slug"], "case_name": r["case_name"],
             "scale": r.get("scale", {})}
            for r in candidates
        ],
        "backup": [
            {"id": r["_id"], "bucket": r["bucket"], "domain": r.get("domain", "?"),
             "paper_slug": r["paper_slug"], "case_name": r["case_name"],
             "scale": r.get("scale", {})}
            for r in backup
        ],
        "rules": {
            "candidate_quota": CANDIDATE_QUOTA,
            "backup_quota": BACKUP_QUOTA,
            "max_candidate_states": MAX_CANDIDATE_STATES,
        },
    }
    (ROOT / "selection.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Wrote {ROOT}/selection.json")


if __name__ == "__main__":
    main()
