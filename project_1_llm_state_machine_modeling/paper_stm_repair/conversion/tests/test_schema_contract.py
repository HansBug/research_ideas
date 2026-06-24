from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
REPORTS = ROOT / "reports"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_schema_files_are_valid_json_schema():
    metaschema = jsonschema.Draft202012Validator.META_SCHEMA
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        jsonschema.Draft202012Validator(metaschema).validate(load_json(path))


def test_committed_report_validates_against_schema():
    schema = load_json(SCHEMAS / "conversion_report.schema.json")
    report = load_json(REPORTS / "selected_seed_examples_conversion_report.json")
    jsonschema.Draft202012Validator(schema).validate(report)
    assert len(report["items"]) == 4


def test_committed_canonical_outputs_validate_against_schema():
    schema = load_json(SCHEMAS / "canonical_stm.schema.json")
    for path in sorted((REPORTS / "canonical").glob("*.canonical_stm.json")):
        jsonschema.Draft202012Validator(schema).validate(load_json(path))


def test_loss_ledger_rows_validate_against_schema():
    schema = load_json(SCHEMAS / "loss_ledger.schema.json")
    rows = [json.loads(line) for line in (REPORTS / "selected_seed_examples_loss_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows
    for row in rows:
        jsonschema.Draft202012Validator(schema).validate(row)
        assert row["repair_contribution_allowed"] is False
