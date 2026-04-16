#!/usr/bin/env python3

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
import re
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]
SUMMARY_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "SUMMARY.md"
MANUAL_AUDIT_DIR = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit"
OUT_PATH = MANUAL_AUDIT_DIR / "efsm_hsm_t0_double_a_summary_section.md"

TABLE_HEADER = "| # | 论文# | 领域 | 案例 | 控制对象 | 状态机类型 | 时间级别 | 结构标签 | 数据集角色 | 原文细节 | 描述细节 | 跳转 |"


def load_case_rows() -> List[Dict[str, str]]:
    text = SUMMARY_PATH.read_text(encoding="utf-8")
    idx = text.index("### 案例清单")
    lines = text[idx:].splitlines()
    rows: List[Dict[str, str]] = []
    start = False
    for line in lines:
        if line.strip() == TABLE_HEADER:
            start = True
            continue
        if not start:
            continue
        if not line.startswith("|"):
            break
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) != 12 or parts[0] in {"#", "---:"} or parts[0].startswith("---"):
            continue
        rows.append(
            {
                "case_id": parts[0],
                "paper_id": parts[1],
                "domain": parts[2],
                "case": parts[3],
                "object": parts[4],
                "sm_type": parts[5].replace("`", ""),
                "time_level": parts[6].replace("`", ""),
                "structure": parts[7].replace("`", ""),
                "role": parts[8].replace("`", ""),
                "src_detail": parts[9].replace("`", ""),
                "desc_detail": parts[10].replace("`", ""),
                "jump": parts[11],
            }
        )
    return rows


def select_candidates(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        row
        for row in rows
        if row["sm_type"] in {"EFSM", "HSM"}
        and row["time_level"] == "T0"
        and row["role"] == "💎 核心保留"
        and row["src_detail"] == "🟢 A"
        and row["desc_detail"] == "🟢 A"
    ]


def load_results() -> Dict[str, Dict[str, str]]:
    results: Dict[str, Dict[str, str]] = {}
    for path in sorted(MANUAL_AUDIT_DIR.glob("audit*.jsonl")):
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                results[row["case_id"]] = row
    return results


def counter_table(title: str, counter: Counter) -> str:
    total = sum(counter.values())
    lines = [title, "", "| 值 | 数量 | 占比 |", "| --- | ---: | ---: |"]
    for key, value in counter.most_common():
        ratio = f"{value / total * 100:.1f}%"
        lines.append(f"| `{key}` | {value} | {ratio} |")
    return "\n".join(lines)


def render() -> str:
    candidates = select_candidates(load_case_rows())
    results = load_results()

    missing = [row["case_id"] for row in candidates if row["case_id"] not in results]
    if missing:
        raise SystemExit(f"Missing manual audit results for case ids: {' '.join(missing[:20])}")

    merged = []
    for row in candidates:
        audit = results[row["case_id"]]
        merged.append({**row, **audit})

    merged.sort(key=lambda row: int(row["case_id"]))

    scope_counter = Counter(row["scope_level"] for row in merged)
    complexity_counter = Counter(row["complexity_bin"] for row in merged)
    evidence_counter = Counter(row["evidence_compactness"] for row in merged)
    risk_counter = Counter(row["hidden_time_risk"] for row in merged)
    fit_counter = Counter(row["pyfcstm_fit"] for row in merged)
    cluster_counter = Counter(row["cluster_key"] for row in merged)
    type_counter = Counter(row["sm_type"] for row in merged)

    paper_count = len({row["paper_id"] for row in merged})

    lines: List[str] = []
    lines.append("## `EFSM/HSM + T0 + 双A` 候选采样子账")
    lines.append("")
    lines.append("### 说明")
    lines.append("")
    lines.append("1. 本节只覆盖 `状态机类型 ∈ {EFSM, HSM}`、`时间级别 = T0`、`原文/描述 = 🟢 A`、`数据集角色 = 💎` 的候选条目。")
    lines.append(f"2. 当前候选总数为 **{len(merged)}** 条，对应 **{paper_count}** 篇论文。")
    lines.append("3. 六个新增指标全部由人工式逐条审核生成；执行上允许用小批量 `codex exec` 承载，但每条案例都单独给出结论。审核定义与 few-shot 示例见 [manual_audit/EFSM_HSM_T0_DOUBLE_A_AUDIT_GUIDE.md](./manual_audit/EFSM_HSM_T0_DOUBLE_A_AUDIT_GUIDE.md)。")
    lines.append("4. 本子账服务于 `60-100` 条实验数据集的采样治理，不替代上文案例总账。")
    lines.append("")
    lines.append("### 候选总体统计")
    lines.append("")
    lines.append("| 指标 | 数量 | 说明 |")
    lines.append("| --- | ---: | --- |")
    lines.append(f"| 候选案例总数 | {len(merged)} | 满足 `EFSM/HSM + T0 + 双A + 💎` 的条目数 |")
    lines.append(f"| 关联论文数 | {paper_count} | 候选覆盖的唯一论文数 |")
    lines.append(f"| `EFSM` | {type_counter.get('EFSM', 0)} | 候选中的扩展状态机条目数 |")
    lines.append(f"| `HSM` | {type_counter.get('HSM', 0)} | 候选中的层次状态机条目数 |")
    lines.append("")
    lines.append(counter_table("### `scope_level` 分布", scope_counter))
    lines.append("")
    lines.append(counter_table("### `complexity_bin` 分布", complexity_counter))
    lines.append("")
    lines.append(counter_table("### `evidence_compactness` 分布", evidence_counter))
    lines.append("")
    lines.append(counter_table("### `hidden_time_risk` 分布", risk_counter))
    lines.append("")
    lines.append(counter_table("### `pyfcstm_fit` 分布", fit_counter))
    lines.append("")
    lines.append("### `cluster_key` 高频项（前 30）")
    lines.append("")
    lines.append("| `cluster_key` | 数量 |")
    lines.append("| --- | ---: |")
    for key, value in cluster_counter.most_common(30):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    lines.append("### 候选清单（含 6 个新增字段）")
    lines.append("")
    lines.append("| # | 论文# | 领域 | 案例 | 控制对象 | 状态机类型 | 结构标签 | `cluster_key` | `scope_level` | `complexity_bin` | `evidence_compactness` | `hidden_time_risk` | `pyfcstm_fit` | 跳转 |")
    lines.append("| ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for row in merged:
        lines.append(
            f"| {row['case_id']} | {row['paper_id']} | {row['domain']} | {row['case']} | {row['object']} | `{row['sm_type']}` | `{row['structure']}` | `{row['cluster_key']}` | `{row['scope_level']}` | `{row['complexity_bin']}` | `{row['evidence_compactness']}` | `{row['hidden_time_risk']}` | `{row['pyfcstm_fit']}` | {row['jump']} |"
        )

    return "\n".join(lines) + "\n"


def main() -> None:
    OUT_PATH.write_text(render(), encoding="utf-8")
    print(OUT_PATH)


if __name__ == "__main__":
    main()
