#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List


REPO_ROOT = Path(__file__).resolve().parents[3]
SUMMARY_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "SUMMARY.md"
GUIDE_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "EFSM_HSM_T0_DOUBLE_A_AUDIT_GUIDE.md"
SCHEMA_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "efsm_hsm_t0_double_a_result.schema.json"
DEFAULT_OUT = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "efsm_hsm_t0_double_a_manual_audit.jsonl"

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
        row = {
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
        rows.append(row)
    return rows


def extract_stm_path(jump_cell: str) -> str:
    match = re.search(r"\[STM\]\(([^)]+)\)", jump_cell)
    if not match:
        raise ValueError(f"Cannot find STM link in jump cell: {jump_cell}")
    return match.group(1).replace("./", "project_1_llm_state_machine_modeling/sources/")


def select_candidates(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    candidates = []
    for row in rows:
        if row["sm_type"] not in {"EFSM", "HSM"}:
            continue
        if row["time_level"] != "T0":
            continue
        if row["role"] != "💎 核心保留":
            continue
        if row["src_detail"] != "🟢 A" or row["desc_detail"] != "🟢 A":
            continue
        stm_rel = extract_stm_path(row["jump"])
        stm_path = REPO_ROOT / stm_rel
        desc_path = stm_path.parent / "DESC.md"
        paper_content_path = stm_path.parent / "paper_content.txt"
        candidate = dict(row)
        candidate["stm_path"] = str(stm_path.relative_to(REPO_ROOT))
        candidate["desc_path"] = str(desc_path.relative_to(REPO_ROOT))
        candidate["paper_content_path"] = str(paper_content_path.relative_to(REPO_ROOT))
        candidates.append(candidate)
    return candidates


def build_prompt(candidate: Dict[str, str]) -> str:
    return f"""先阅读 `{GUIDE_PATH.relative_to(REPO_ROOT)}`，再阅读以下目标材料并做人工作风格的逐条审核：
- `{candidate['stm_path']}`
- `{candidate['desc_path']}`
- 必要时回 `{candidate['paper_content_path']}`

目标案例名：`{candidate['case']}`

请严格遵守审核 guide 的定义、边界条件和 few-shot 示例，不要只凭标题、现有标签或系统名猜测。

输出要求：
1. 只输出符合 schema 的 JSON。
2. `cluster_key` 必须是稳定、可复用、与具体系统名解耦的英文短横线 slug。
3. `rationale` 使用 3-5 句中文，必须说明：
   - 为什么判这个 `scope_level`
   - 为什么判这个 `evidence_compactness`
   - 为什么判这个 `hidden_time_risk`
   - 为什么判这个 `pyfcstm_fit`
"""


def load_existing(path: Path) -> Dict[str, Dict[str, str]]:
    if not path.exists():
        return {}
    existing: Dict[str, Dict[str, str]] = {}
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            existing[row["case_id"]] = row
    return existing


def run_codex(prompt: str) -> Dict[str, str]:
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "out.json"
        cmd = [
            "codex",
            "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "-C",
            str(REPO_ROOT),
            "--output-schema",
            str(SCHEMA_PATH),
            "-o",
            str(out_path),
            prompt,
        ]
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return json.loads(out_path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--case-ids", nargs="*", default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = select_candidates(load_case_rows())
    if args.case_ids:
        wanted = set(args.case_ids)
        rows = [row for row in rows if row["case_id"] in wanted]
    if args.limit is not None:
        rows = rows[: args.limit]

    existing = {} if args.overwrite else load_existing(args.out)
    pending = [row for row in rows if row["case_id"] not in existing]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for idx, candidate in enumerate(pending, start=1):
            print(f"[{idx}/{len(pending)}] auditing case {candidate['case_id']}: {candidate['case']}", flush=True)
            result = run_codex(build_prompt(candidate))
            payload = {
                "case_id": candidate["case_id"],
                "paper_id": candidate["paper_id"],
                "domain": candidate["domain"],
                "case": candidate["case"],
                "object": candidate["object"],
                "stm_path": candidate["stm_path"],
                "desc_path": candidate["desc_path"],
                **result,
            }
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())


if __name__ == "__main__":
    main()
