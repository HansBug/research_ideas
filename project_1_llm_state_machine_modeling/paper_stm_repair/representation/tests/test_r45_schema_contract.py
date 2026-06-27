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


def test_committed_export_report_validates_against_schema():
    schema = load_json(SCHEMAS / "fcstm_export_report.schema.json")
    report = load_json(REPORTS / "fcstm_export_report.json")
    jsonschema.Draft202012Validator(schema).validate(report)
    assert report["summary"] == {"examples": 4, "converted": 4, "partial": 0, "blocked": 0}
    assert {item["example_id"] for item in report["items"]} == {
        "llms-emp-gpt4o-hldcs",
        "llms-emp-kimi-autonomous-collision",
        "sefm-ssc7-umple",
        "unified-uml-synthetic-0000",
    }
    assert all(item["repair_contribution_allowed"] is False for item in report["items"])


def test_committed_name_mapping_reports_validate_against_schema():
    schema = load_json(SCHEMAS / "name_mapping.schema.json")
    for path in sorted((REPORTS / "fcstm_exports").glob("*/name_mapping.json")):
        jsonschema.Draft202012Validator(schema).validate(load_json(path))


def test_committed_lowering_inventory_reports_validate_against_schema():
    schema = load_json(SCHEMAS / "lowering_inventory.schema.json")
    jsonschema.Draft202012Validator(schema).validate(load_json(REPORTS / "lowering_inventory.json"))
    for path in sorted((REPORTS / "fcstm_exports").glob("*/lowering_inventory.json")):
        jsonschema.Draft202012Validator(schema).validate(load_json(path))


def test_committed_loss_ledger_rows_validate_against_schema():
    schema = load_json(SCHEMAS / "fcstm_export_loss_ledger.schema.json")
    rows = [json.loads(line) for line in (REPORTS / "fcstm_export_loss_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows
    for row in rows:
        jsonschema.Draft202012Validator(schema).validate(row)
        assert row["repair_contribution_allowed"] is False
        assert row["attribution"] == "representation_lowering_not_repair"
