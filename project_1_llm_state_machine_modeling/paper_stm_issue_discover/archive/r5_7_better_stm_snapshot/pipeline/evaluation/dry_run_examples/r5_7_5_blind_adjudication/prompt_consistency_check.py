#!/usr/bin/env python3
"""Verify archived blind judge prompts match the current bundle and prompt template.

This is an audit guard for R5.7.5: if a case input, prompt template, or
candidate file changes after a judge run, the archived output must not be
reported as final until the case is rerun.  The script rebuilds each prompt
using run_blind_judge.build_prompt and compares it to the archived prompt.txt.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
RUNNER = ROOT / "run_blind_judge.py"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_runner() -> Any:
    spec = importlib.util.spec_from_file_location("r575_run_blind_judge", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load runner: {RUNNER}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--judge", default="claude-blind-judge")
    ap.add_argument("--case-count", type=int, default=20)
    args = ap.parse_args()

    runner = load_runner()
    mismatches: list[dict[str, str]] = []
    checked: list[dict[str, str]] = []
    for idx in range(1, args.case_count + 1):
        bid = f"B{idx:02d}"
        expected_prompt = runner.build_prompt(bid, args.judge)
        archived_path = ROOT / "judge_outputs" / args.judge / bid / "prompt.txt"
        if not archived_path.exists():
            mismatches.append({"blind_case_id": bid, "reason": "archived_prompt_missing", "path": str(archived_path)})
            continue
        archived_prompt = archived_path.read_text(encoding="utf-8")
        expected_sha = sha256_text(expected_prompt)
        archived_sha = sha256_text(archived_prompt)
        row = {"blind_case_id": bid, "expected_prompt_sha256": expected_sha, "archived_prompt_sha256": archived_sha}
        checked.append(row)
        if expected_sha != archived_sha:
            mismatches.append({**row, "reason": "prompt_sha256_mismatch"})

    result = {
        "schema_version": "r5_7_5.prompt_consistency_check.v1",
        "judge": args.judge,
        "case_count": args.case_count,
        "checked_count": len(checked),
        "mismatch_count": len(mismatches),
        "mismatches": mismatches,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if mismatches:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
