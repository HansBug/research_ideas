from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[2]
DRY_RUN = ROOT / "dry_run_examples"
SCHEMAS = ROOT / "schemas"
R3_REPORT = REPO / "project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/selected_seed_examples_conversion_report.json"

EXPECTED = {
    "llms-emp-gpt4o-hldcs": {"r3_status": "converted", "decision": "complete", "canonical": True, "model_level": True},
    "sefm-ssc7-umple": {"r3_status": "partial", "decision": "focused", "canonical": True, "model_level": False},
    "ttool-automatedbraking-xml": {"r3_status": "partial", "decision": "focused", "canonical": True, "model_level": False},
    "unified-uml-synthetic-0000": {"r3_status": "partial", "decision": "blocked", "canonical": False, "model_level": False},
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_all_four_r4_dry_run_examples_have_required_files_and_validate():
    schemas = {
        "diagnostic_draft.json": load_json(SCHEMAS / "diagnostic.schema.json"),
        "scenario_draft.json": load_json(SCHEMAS / "scenario.schema.json"),
        "eligibility_decision.json": load_json(SCHEMAS / "eligibility_decision.schema.json"),
        "better_stm_checklist.json": load_json(SCHEMAS / "better_stm_checklist.schema.json"),
    }
    dry_runs_doc = (ROOT / "DRY_RUNS.md").read_text(encoding="utf-8")
    for example_id in EXPECTED:
        assert example_id in dry_runs_doc
        example_dir = DRY_RUN / example_id
        for filename, schema in schemas.items():
            path = example_dir / filename
            assert path.exists(), path
            jsonschema.Draft202012Validator(schema).validate(load_json(path))


def test_r4_eligibility_decisions_match_r3_report_statuses():
    r3_by_id = {item["example_id"]: item for item in load_json(R3_REPORT)["items"]}
    assert set(r3_by_id) == set(EXPECTED)
    for example_id, expected in EXPECTED.items():
        eligibility = load_json(DRY_RUN / example_id / "eligibility_decision.json")
        r3 = r3_by_id[example_id]
        assert eligibility["r3_status"] == r3["status"] == expected["r3_status"]
        assert eligibility["r3_status_reason_code"] == r3["status_reason_code"]
        assert eligibility["r4_dry_run_decision"] == expected["decision"]
        assert eligibility["canonical_available"] is expected["canonical"]
        assert eligibility["allow_model_level_evaluation"] is expected["model_level"]
        assert eligibility["conversion_gain_counted_as_repair"] is False
        if not expected["canonical"]:
            assert eligibility["canonical_output_path"] is None
            assert eligibility["allow_repair_loop_smoke"] is False


def test_better_stm_checklists_never_claim_better_in_r4_gate_dry_run():
    for example_id in EXPECTED:
        checklist = load_json(DRY_RUN / example_id / "better_stm_checklist.json")
        assert checklist["evaluation_context"] == "gate_dry_run"
        assert checklist["can_claim_better_stm"] is False
        assert checklist["conversion_gain_counted_as_repair"] is False
        statuses = {name: data["status"] for name, data in checklist["conditions"].items()}
        assert any(status in {"unknown", "not_applicable", "fail"} for status in statuses.values())
        assert statuses["conversion_gain_separated_from_repair_gain"] == "pass"


def test_placeholder_scenarios_are_not_regression_gates():
    for example_id in EXPECTED:
        scenario = load_json(DRY_RUN / example_id / "scenario_draft.json")
        for item in scenario["scenarios"]:
            if item["oracle_type"] == "placeholder":
                assert item["is_regression_gate"] is False
                assert item["blocking_on_failure"] is False


def test_partial_and_blocked_examples_are_not_promoted_to_model_level_evaluation():
    sefm = load_json(DRY_RUN / "sefm-ssc7-umple" / "eligibility_decision.json")
    ttool = load_json(DRY_RUN / "ttool-automatedbraking-xml" / "eligibility_decision.json")
    unified = load_json(DRY_RUN / "unified-uml-synthetic-0000" / "eligibility_decision.json")
    assert sefm["allow_model_level_evaluation"] is False
    assert "timing" in " ".join(sefm["required_caveats"]).lower()
    assert ttool["allow_model_level_evaluation"] is False
    assert any("inventory" in caveat.lower() for caveat in ttool["required_caveats"])
    assert unified["r4_dry_run_decision"] == "blocked"
    assert unified["canonical_available"] is False
    assert unified["allow_model_level_evaluation"] is False
    assert unified["allow_repair_loop_smoke"] is False


def test_key_evidence_locators_point_to_existing_repo_files():
    for example_id in EXPECTED:
        for filename in ["diagnostic_draft.json", "scenario_draft.json", "eligibility_decision.json", "better_stm_checklist.json"]:
            text = (DRY_RUN / example_id / filename).read_text(encoding="utf-8")
            assert "/home/" not in text
            assert "/tmp/" not in text
        eligibility = load_json(DRY_RUN / example_id / "eligibility_decision.json")
        for locator in eligibility["evidence_locator"]:
            path = REPO / locator["path"]
            assert path.exists(), locator
