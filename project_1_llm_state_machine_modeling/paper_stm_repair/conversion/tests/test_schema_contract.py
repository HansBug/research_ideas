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


def test_committed_recovery_report_validates_against_schema():
    schema = load_json(SCHEMAS / "recovery_report.schema.json")
    report_path = REPORTS / "plantuml_recovery_report.json"
    report = load_json(report_path)
    jsonschema.Draft202012Validator(schema).validate(report)
    assert report["repo_commit"] == report["generator_code_commit"]
    assert report["generator_code_commit"] not in {"unknown", "8ed7607ab20f828ade4aefb4ef4d60dfb5996558"}
    assert report["generator_worktree_dirty"] is False
    assert report["generator_git_status_porcelain"] == []
    assert "artifact commit" in report["artifact_commit_note"]
    assert "clean" in report["repo_commit_semantics"].lower()
    assert isinstance(report["generator_worktree_dirty"], bool)
    assert isinstance(report["generator_git_status_porcelain"], list)
    assert "recover-plantuml" in report["generation_command"]
    assert report["summary"]["raw_total"] == 1049
    assert report["summary"]["failed_before"] == 499
    assert "technical_scxml_pass_all_rules" in report["summary"]
    assert "low_risk_scxml_pass" in report["summary"]
    assert "main_eligibility_included" in report["summary"]
    assert "by_seed_class" in report["summary"]
    assert "eligible_after_composition_by_llm" in report["summary"]["llms_emp_cross_llm_gate"]
    assert "semantic_preservation_audit_summary" in report
    assert report["semantic_preservation_audit_summary"]["main_eligibility_requires_pass"] is True
    assert report["semantic_preservation_audit_summary"]["low_risk_fail_total"] == 0
    assert report["source_file_immutability"]
    assert all(row["source_file_unchanged"] for row in report["source_file_immutability"])
    assert all(row["source_line_unchanged"] and row["source_file_unchanged"] for row in report["raw_immutability"])
    assert all(
        item["main_eligibility_included"] <= item["normalized_conversion_pass"]
        for item in report["items"]
    )
    assert all(
        (not item["main_eligibility_included"]) or item.get("semantic_preservation_pass") is True
        for item in report["items"]
    )
    assert all(
        (not item["main_eligibility_included"]) or "PUML.NORM.alias_embedded_pseudostate_marker" not in item.get("rule_ids", [])
        for item in report["items"]
    )
    assert all(
        (not item["main_eligibility_included"]) or "when" not in json.dumps(item.get("semantic_preservation_audit"), ensure_ascii=False).lower()
        for item in report["items"]
    )
    assert all(
        not str(item.get("raw_candidate_path", "")).startswith("runs/")
        for item in report["items"]
    )
    assert all(
        not str(item.get("normalized_candidate_path", "")).startswith("runs/")
        for item in report["items"]
    )
    assert all(
        item["normalized_conversion_pass"] == (item["normalized_scxml_pass"] and item["normalized_canonical_parse_pass"])
        for item in report["items"]
    )


def test_committed_normalization_ledger_validates_against_schema():
    schema = load_json(SCHEMAS / "normalization_ledger.schema.json")
    rows = [json.loads(line) for line in (REPORTS / "plantuml_normalization_ledger.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    assert rows
    for row in rows:
        jsonschema.Draft202012Validator(schema).validate(row)
        assert row["repair_contribution_allowed"] is False
    assert any(row["rule_id"] == "PUML.NORM.fork_join_decl_to_state" and row["concurrency_degraded"] for row in rows)


def test_committed_recovery_outputs_do_not_embed_local_absolute_paths():
    for path in [
        REPORTS / "plantuml_recovery_report.json",
        REPORTS / "plantuml_recovery_summary.md",
        REPORTS / "plantuml_normalization_ledger.jsonl",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "/home/" not in text
        assert "/tmp/" not in text
