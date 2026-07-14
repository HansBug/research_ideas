"""Validate committed real-model demo artifacts.

This deliberately consumes only the public result/audit/receipt files.  It is
kept under tests/ so a smoke run can be checked without importing provider
clients or re-running a model.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


_SECRET = re.compile(r"(?:sk|sess|key)-[A-Za-z0-9_-]{8,}|Bearer\s+[^\s]+", re.I)
_TOOLS = {"current_system_time", "calculate_expression"}
_OUTPUT_FIELDS = {"summary", "base_time", "offset_hours", "target_time", "evidence_ids"}


def _sha256(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_profile(root: Path, profile: str) -> None:
    audit = root / f"{profile}-audit.jsonl"
    result = root / f"{profile}-result.json"
    receipt = root / f"{profile}-audit.jsonl.receipt.json"
    for path in (audit, result, receipt):
        if not path.is_file():
            raise AssertionError(f"{profile}: missing artifact {path}")
    if list(root.glob(f".{audit.name}.*.part")) or list(root.glob(f".{result.name}.*.part")):
        raise AssertionError(f"{profile}: uncommitted .part artifact remains")

    receipt_data = _load_json(receipt)
    if receipt_data.get("artifact_status") != "committed":
        raise AssertionError(f"{profile}: receipt is not committed")
    if receipt_data.get("audit_sha256") != _sha256(audit) or receipt_data.get("result_sha256") != _sha256(result):
        raise AssertionError(f"{profile}: receipt hash mismatch")

    result_data = _load_json(result)
    if result_data.get("status") != "success" or not result_data.get("academic_eligible"):
        raise AssertionError(f"{profile}: result is not an eligible success")
    output = result_data.get("output")
    if not isinstance(output, dict) or set(output) != _OUTPUT_FIELDS:
        raise AssertionError(f"{profile}: structured output fields are incomplete")
    completed_tools = {
        item.get("name")
        for item in result_data.get("tool_calls", [])
        if item.get("kind") == "business" and item.get("status") == "completed"
    }
    if not _TOOLS.issubset(completed_tools):
        raise AssertionError(f"{profile}: required tools were not completed")

    records = [_load_json_line(line, audit) for line in audit.read_text(encoding="utf-8").splitlines() if line.strip()]
    finishes = [record for record in records if record.get("record") == "finish"]
    if len(finishes) != 1:
        raise AssertionError(f"{profile}: expected one finish record")
    if not records or records[0].get("record") != "context":
        raise AssertionError(f"{profile}: audit does not start with context")
    if not any(record.get("record") == "decision" for record in records):
        raise AssertionError(f"{profile}: audit has no model decision")
    if not any(record.get("record") == "action" for record in records):
        raise AssertionError(f"{profile}: audit has no tool action")
    serialized = audit.read_text(encoding="utf-8") + result.read_text(encoding="utf-8")
    if _SECRET.search(serialized):
        raise AssertionError(f"{profile}: credential-like value leaked")


def _load_json_line(line: str, path: Path) -> dict[str, Any]:
    try:
        value = json.loads(line)
    except json.JSONDecodeError as exc:  # pragma: no cover - CLI diagnostic
        raise AssertionError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AssertionError(f"non-object audit record in {path}")
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate committed utils.agent real smoke artifacts")
    parser.add_argument("--root", type=Path, default=Path("runs/utils-agent"))
    parser.add_argument(
        "--profiles",
        nargs="+",
        default=("gpt-5.5", "deepseek-v4-flash", "claude-opus-4-7"),
    )
    args = parser.parse_args()
    for profile in args.profiles:
        validate_profile(args.root, profile)
    print(f"smoke-valid: {len(args.profiles)} profile(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
