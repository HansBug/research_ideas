from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
DRY_RUN = ROOT / "dry_run_examples"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validator(name: str) -> jsonschema.Draft202012Validator:
    return jsonschema.Draft202012Validator(load_json(SCHEMAS / name))


def test_r4_schema_files_are_valid_json_schema():
    metaschema = jsonschema.Draft202012Validator.META_SCHEMA
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        jsonschema.Draft202012Validator(metaschema).validate(load_json(path))


def test_committed_rubric_validates_against_schema():
    schema = load_json(SCHEMAS / "human_rubric.schema.json")
    rubric = load_json(ROOT / "human_rubric_v0.json")
    jsonschema.Draft202012Validator(schema).validate(rubric)
    assert rubric["human_for_evaluation_only"] is True
    assert rubric["used_by_repair_loop"] is False


def test_negative_placeholder_oracle_cannot_be_regression_gate():
    schema = load_json(SCHEMAS / "scenario.schema.json")
    valid = load_json(DRY_RUN / "unified-uml-synthetic-0000" / "scenario_draft.json")
    invalid = json.loads(json.dumps(valid))
    invalid["scenarios"][0]["oracle_type"] = "placeholder"
    invalid["scenarios"][0]["is_regression_gate"] = True
    invalid["scenarios"][0]["blocking_on_failure"] = True
    with __import__("pytest").raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(invalid)


def test_gate_dry_run_context_cannot_claim_better_stm():
    schema = load_json(SCHEMAS / "better_stm_checklist.schema.json")
    valid = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "better_stm_checklist.json")
    invalid = json.loads(json.dumps(valid))
    invalid["evaluation_context"] = "gate_dry_run"
    invalid["can_claim_better_stm"] = True
    invalid["overall_decision"] = "better"
    with __import__("pytest").raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(invalid)


def test_conversion_gain_counted_as_repair_is_schema_forbidden():
    schema = load_json(SCHEMAS / "eligibility_decision.schema.json")
    valid = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "eligibility_decision.json")
    invalid = json.loads(json.dumps(valid))
    invalid["conversion_gain_counted_as_repair"] = True
    with __import__("pytest").raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(invalid)


def test_repair_result_with_unknown_condition_cannot_claim_better_stm():
    schema = load_json(SCHEMAS / "better_stm_checklist.schema.json")
    valid = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "better_stm_checklist.json")
    invalid = json.loads(json.dumps(valid))
    invalid["evaluation_context"] = "repair_result"
    invalid["can_claim_better_stm"] = True
    invalid["overall_decision"] = "better"
    # Leave several conditions unknown / not_applicable to prove schema blocks
    # future statistics from treating unknown as pass.
    with __import__("pytest").raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(invalid)


def test_repair_result_with_all_pass_conditions_can_claim_better_stm_contractually():
    schema = load_json(SCHEMAS / "better_stm_checklist.schema.json")
    valid = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "better_stm_checklist.json")
    candidate = json.loads(json.dumps(valid))
    candidate["evaluation_context"] = "repair_result"
    candidate["can_claim_better_stm"] = True
    candidate["overall_decision"] = "better"
    candidate["gain_attribution"] = "repair_loop"
    for condition in candidate["conditions"].values():
        condition["status"] = "pass"
        condition["missing_evidence_reason"] = None
    jsonschema.Draft202012Validator(schema).validate(candidate)


def test_better_stm_claim_requires_repair_loop_gain_attribution():
    schema = load_json(SCHEMAS / "better_stm_checklist.schema.json")
    valid = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "better_stm_checklist.json")
    invalid = json.loads(json.dumps(valid))
    invalid["evaluation_context"] = "repair_result"
    invalid["can_claim_better_stm"] = True
    invalid["overall_decision"] = "better"
    invalid["gain_attribution"] = "conversion_normalization"
    for condition in invalid["conditions"].values():
        condition["status"] = "pass"
        condition["missing_evidence_reason"] = None
    with __import__("pytest").raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(invalid)
