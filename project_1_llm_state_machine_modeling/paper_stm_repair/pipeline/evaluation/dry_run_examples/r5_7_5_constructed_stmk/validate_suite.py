#!/usr/bin/env python3
"""Validate the R5.7.5 constructed STM_k dry-run evidence bundle.

This script is intentionally local to the R5.7.5 evidence bundle.  It is not
part of the repair method implementation; it only gives reports and case notes
an executable audit command.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


BUNDLE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = BUNDLE_ROOT.parents[5]
SCHEMA_PATH = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/experiment_design/"
    "protocols/better_adjudication_output_schema_v0.json"
)
REQUIRED_CASE_FILES = [
    "baseline_pointer.json",
    "candidate.fcstm",
    "change_ledger.json",
    "target_instance_ledger.json",
    "adjudication_record.json",
    "expected_verdict.json",
]
COMMON_FALSE_FIELDS = ["headline_eligible", "repair_effectiveness_eligible"]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def validate_common_boundary(obj: dict[str, Any], label: str) -> None:
    require(obj.get("constructed_for_protocol_dry_run") is True, f"{label}: constructed flag is not true")
    require(obj.get("real_repair_run_id") is None, f"{label}: real_repair_run_id is not null")
    for field in COMMON_FALSE_FIELDS:
        require(obj.get(field) is False, f"{label}: {field} is not false")


def validate_adjudication_schema(record: dict[str, Any]) -> None:
    try:
        import jsonschema  # type: ignore
    except Exception:
        return
    jsonschema.validate(record, load_json(SCHEMA_PATH))


def pyfcstm_parse(candidate: Path) -> int:
    result = subprocess.run(
        [sys.executable, "-m", "pyfcstm", "plantuml", "-i", str(candidate)],
        cwd=REPO_ROOT,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=30,
    )
    return result.returncode


def validate_case(case: dict[str, Any], parse: bool) -> None:
    case_id = case["case_id"]
    case_dir = REPO_ROOT / case["case_dir"]
    require(case_dir.is_dir(), f"{case_id}: missing case dir {case_dir}")
    for name in REQUIRED_CASE_FILES:
        require((case_dir / name).exists(), f"{case_id}: missing {name}")

    validate_common_boundary(case, f"suite_index.cases[{case_id}]")
    expected = load_json(case_dir / "expected_verdict.json")
    adjudication = load_json(case_dir / "adjudication_record.json")
    change_ledger = load_json(case_dir / "change_ledger.json")
    target_ledger = load_json(case_dir / "target_instance_ledger.json")
    baseline_pointer = load_json(case_dir / "baseline_pointer.json")

    for name, obj in [
        ("expected_verdict", expected),
        ("adjudication_record", adjudication),
        ("change_ledger", change_ledger),
        ("target_instance_ledger", target_ledger),
        ("baseline_pointer", baseline_pointer),
    ]:
        require(obj.get("case_id") == case_id, f"{case_id}: {name}.case_id mismatch")
        validate_common_boundary(obj, f"{case_id}.{name}")

    require(expected.get("evidence_keys"), f"{case_id}: expected_verdict.evidence_keys is empty")
    require(adjudication.get("evidence_keys"), f"{case_id}: adjudication_record.evidence_keys is empty")
    require(
        expected.get("primary_expected_verdict") == case.get("primary_expected_verdict"),
        f"{case_id}: expected verdict mismatch with suite_index",
    )
    require(
        adjudication.get("primary_expected_verdict") == case.get("primary_expected_verdict"),
        f"{case_id}: adjudication verdict mismatch with suite_index",
    )
    validate_adjudication_schema(adjudication)

    if parse:
        actual_invalid = pyfcstm_parse(case_dir / "candidate.fcstm") != 0
        expected_invalid = case.get("primary_expected_verdict") == "stmk_repair_failure"
        require(actual_invalid == expected_invalid, f"{case_id}: pyfcstm parse expectation mismatch")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", help="Validate a single case id, e.g. C01")
    parser.add_argument("--parse", action="store_true", help="Also run pyfcstm parse expectation checks")
    args = parser.parse_args()

    suite = load_json(BUNDLE_ROOT / "suite_index.json")
    validate_common_boundary(suite, "suite_index")
    require(suite.get("case_count") == len(suite.get("cases", [])), "suite_index.case_count mismatch")
    require(
        suite.get("coverage_summary", {}).get("scenario_overfitting") == "handoff_only_not_covered",
        "scenario_overfitting coverage status must be handoff_only_not_covered",
    )

    cases = suite["cases"]
    if args.case:
        cases = [case for case in cases if case["case_id"] == args.case]
        require(len(cases) == 1, f"case not found: {args.case}")

    for case in cases:
        validate_case(case, parse=args.parse)

    print(f"r5.7.5-constructed-stmk-validation-ok cases={len(cases)} parse={args.parse}")


if __name__ == "__main__":
    main()
