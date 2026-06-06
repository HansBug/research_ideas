#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Dict, List

from run_efsm_hsm_t0_double_a_manual_audit import (
    REPO_ROOT,
    load_case_rows,
    select_candidates,
)


GUIDE_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "EFSM_HSM_T0_DOUBLE_A_AUDIT_GUIDE.md"
BATCH_SCHEMA_PATH = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit" / "efsm_hsm_t0_double_a_batch_result.schema.json"
MANUAL_AUDIT_DIR = REPO_ROOT / "project_1_llm_state_machine_modeling" / "sources" / "manual_audit"
DEFAULT_OUT = MANUAL_AUDIT_DIR / "audit_batch.jsonl"


def load_existing_from_dir(skip_out: Path | None = None) -> Dict[str, Dict[str, str]]:
    existing: Dict[str, Dict[str, str]] = {}
    for path in sorted(MANUAL_AUDIT_DIR.glob("audit*.jsonl")):
        if skip_out is not None and path.resolve() == skip_out.resolve():
            continue
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = json.loads(line)
                existing[row["case_id"]] = row
    return existing


def build_prompt(batch: List[Dict[str, str]]) -> str:
    lines = [
        f"先阅读 `{GUIDE_PATH.relative_to(REPO_ROOT)}`，再对下面这些目标案例做人工式逐条审核。",
        "你这次是在一个小批量任务里处理多个案例，但每个案例都必须独立阅读并独立判断，不允许共享一个笼统结论。",
        "对每个案例都要先看 `STM.md`、再看 `DESC.md`，必要时回 `paper_content.txt`。",
        "禁止只凭标题、已有标签、领域或系统名猜测；必须依据目标文件本身给结论。",
        "",
        "输出要求：",
        "1. 只输出符合 schema 的 JSON 对象，顶层字段必须是 `results`。",
        "2. `results` 数组顺序必须与下方案例顺序一致。",
        "3. `results` 里的每个元素都必须包含准确的 `case_id`。",
        "4. `results` 里的每个元素的 `rationale` 使用 3-5 句中文，必须分别说明：",
        "   - 为什么判这个 `scope_level`",
        "   - 为什么判这个 `evidence_compactness`",
        "   - 为什么判这个 `hidden_time_risk`",
        "   - 为什么判这个 `pyfcstm_fit`",
        "5. `cluster_key` 必须是稳定、可复用、与具体系统名解耦的英文短横线 slug。",
        "6. 只有在控制图像确实近同构时，才复用同一个 `cluster_key`；不要为了统一而硬压不同模式。",
        "",
        "目标案例列表：",
    ]
    for idx, candidate in enumerate(batch, start=1):
        lines.extend(
            [
                f"{idx}. `case_id = {candidate['case_id']}`",
                f"   - 案例名：`{candidate['case']}`",
                f"   - `STM.md`：`{candidate['stm_path']}`",
                f"   - `DESC.md`：`{candidate['desc_path']}`",
                f"   - 必要时回：`{candidate['paper_content_path']}`",
            ]
        )
    return "\n".join(lines)


def run_codex_batch(batch: List[Dict[str, str]], model: str | None = None, reasoning_effort: str | None = None) -> List[Dict[str, str]]:
    with tempfile.TemporaryDirectory() as tmpdir:
        out_path = Path(tmpdir) / "out.json"
        cmd = [
            "codex",
            "exec",
            "--dangerously-bypass-approvals-and-sandbox",
            "-C",
            str(REPO_ROOT),
            "--output-schema",
            str(BATCH_SCHEMA_PATH),
            "-o",
            str(out_path),
        ]
        if model:
            cmd.extend(["-m", model])
        if reasoning_effort:
            cmd.extend(["-c", f"model_reasoning_effort={json.dumps(reasoning_effort)}"])
        cmd.append(build_prompt(batch))
        subprocess.run(
            cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        payload = json.loads(out_path.read_text(encoding="utf-8"))

    if not isinstance(payload, dict) or not isinstance(payload.get("results"), list):
        raise ValueError("Batch audit result is not an object with a results list")

    results = payload["results"]
    expected_ids = [candidate["case_id"] for candidate in batch]
    actual_ids = [str(item.get("case_id", "")) for item in results]
    if actual_ids != expected_ids:
        raise ValueError(f"Batch audit case ids mismatch: expected {expected_ids}, got {actual_ids}")

    return results


def enrich_candidates(rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
    enriched: List[Dict[str, str]] = []
    for row in rows:
        stm_path = row["jump"].split("[STM](")[1].split(")")[0].replace("./", "project_1_llm_state_machine_modeling/sources/")
        stm = REPO_ROOT / stm_path
        candidate = dict(row)
        candidate["stm_path"] = str(stm.relative_to(REPO_ROOT))
        candidate["desc_path"] = str((stm.parent / "DESC.md").relative_to(REPO_ROOT))
        candidate["paper_content_path"] = str((stm.parent / "paper_content.txt").relative_to(REPO_ROOT))
        enriched.append(candidate)
    return enriched


def chunked(rows: List[Dict[str, str]], size: int) -> List[List[Dict[str, str]]]:
    return [rows[i : i + size] for i in range(0, len(rows), size)]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--case-ids", nargs="*", default=None)
    parser.add_argument("--shard-count", type=int, default=None)
    parser.add_argument("--shard-index", type=int, default=None)
    parser.add_argument("--model", type=str, default=None)
    parser.add_argument("--reasoning-effort", type=str, default="medium")
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.batch_size < 1:
        raise ValueError("--batch-size must be >= 1")

    if (args.shard_count is None) != (args.shard_index is None):
        raise ValueError("--shard-count and --shard-index must be provided together")
    if args.shard_count is not None and not (0 <= args.shard_index < args.shard_count):
        raise ValueError("--shard-index must be within [0, --shard-count)")

    rows = enrich_candidates(select_candidates(load_case_rows()))
    if args.case_ids:
        wanted = set(args.case_ids)
        rows = [row for row in rows if row["case_id"] in wanted]

    existing = {} if args.overwrite else load_existing_from_dir(skip_out=args.out)
    pending = [row for row in rows if row["case_id"] not in existing]

    if args.shard_count is not None:
        pending = pending[args.shard_index :: args.shard_count]

    batches = chunked(pending, args.batch_size)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("a", encoding="utf-8") as f:
        for idx, batch in enumerate(batches, start=1):
            case_ids = ", ".join(candidate["case_id"] for candidate in batch)
            print(f"[batch {idx}/{len(batches)}] auditing case ids: {case_ids}", flush=True)
            results = run_codex_batch(batch, model=args.model, reasoning_effort=args.reasoning_effort)
            by_id = {row["case_id"]: row for row in results}
            for candidate in batch:
                result = by_id[candidate["case_id"]]
                payload = {
                    "case_id": candidate["case_id"],
                    "paper_id": candidate["paper_id"],
                    "domain": candidate["domain"],
                    "case": candidate["case"],
                    "object": candidate["object"],
                    "stm_path": candidate["stm_path"],
                    "desc_path": candidate["desc_path"],
                    "cluster_key": result["cluster_key"],
                    "scope_level": result["scope_level"],
                    "complexity_bin": result["complexity_bin"],
                    "evidence_compactness": result["evidence_compactness"],
                    "hidden_time_risk": result["hidden_time_risk"],
                    "pyfcstm_fit": result["pyfcstm_fit"],
                    "rationale": result["rationale"],
                }
                f.write(json.dumps(payload, ensure_ascii=False) + "\n")
                f.flush()
                os.fsync(f.fileno())


if __name__ == "__main__":
    main()
