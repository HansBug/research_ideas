from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
def repo_root() -> Path:
    for parent in [ROOT, *ROOT.parents]:
        if (parent / ".git").exists() and (parent / "project_1_llm_state_machine_modeling").exists():
            return parent
    raise RuntimeError("repository root not found")


REPO = repo_root()
DRY_RUN = ROOT / "dry_run_examples"
SCHEMAS = ROOT / "schemas"
R3_REPORT = REPO / "project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/conversion/reports/selected_seed_examples_conversion_report.json"

EXPECTED = {
    "llms-emp-deepseek-microwave": {"r3_status": "converted", "decision": "complete", "canonical": True, "model_level": True},
    "llms-emp-gpt4o-hldcs": {"r3_status": "converted", "decision": "complete", "canonical": True, "model_level": True},
    "llms-emp-kimi-autonomous-collision": {"r3_status": "converted", "decision": "complete", "canonical": True, "model_level": True},
    "sefm-ssc7-umple": {"r3_status": "partial", "decision": "focused", "canonical": True, "model_level": False},
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
    for example_id in EXPECTED:
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


def test_partial_examples_are_not_promoted_to_model_level_evaluation():
    sefm = load_json(DRY_RUN / "sefm-ssc7-umple" / "eligibility_decision.json")
    assert sefm["allow_model_level_evaluation"] is False
    assert "timing" in " ".join(sefm["required_caveats"]).lower()


def test_microwave_records_conversion_normalization_without_repair_credit():
    microwave = load_json(DRY_RUN / "llms-emp-deepseek-microwave" / "eligibility_decision.json")
    assert microwave["r3_status"] == "converted"
    assert microwave["r4_dry_run_decision"] == "complete"
    assert microwave["canonical_available"] is True
    assert microwave["allow_model_level_evaluation"] is True
    assert microwave["allow_repair_loop_smoke"] is True
    assert microwave["gain_attribution"] == "conversion_normalization"
    assert microwave["conversion_gain_counted_as_repair"] is False
    assert any("normalization" in caveat.lower() or "规范化" in caveat for caveat in microwave["required_caveats"])


def test_converted_examples_split_model_level_by_conversion_attribution():
    gpt4o = load_json(DRY_RUN / "llms-emp-gpt4o-hldcs" / "eligibility_decision.json")
    kimi = load_json(DRY_RUN / "llms-emp-kimi-autonomous-collision" / "eligibility_decision.json")
    microwave = load_json(DRY_RUN / "llms-emp-deepseek-microwave" / "eligibility_decision.json")
    assert gpt4o["r4_dry_run_decision"] == "complete"
    assert gpt4o["allow_model_level_evaluation"] is True
    assert kimi["r4_dry_run_decision"] == "complete"
    assert kimi["allow_model_level_evaluation"] is True
    assert microwave["r4_dry_run_decision"] == "complete"
    assert microwave["allow_model_level_evaluation"] is True
    assert microwave["gain_attribution"] == "conversion_normalization"


def test_r4_artifacts_have_top_level_source_traceability_matching_r3_report():
    r3_by_id = {item["example_id"]: item for item in load_json(R3_REPORT)["items"]}
    for example_id in EXPECTED:
        r3 = r3_by_id[example_id]
        expected_trace = {
            "source_nl_path": r3["source_nl_path"],
            "source_stm0_path": r3["source_stm0_path"],
            "source_meta_path": r3["source_meta_path"],
            "canonical_output_path": r3["canonical_output_path"],
        }
        for filename in ["diagnostic_draft.json", "scenario_draft.json", "eligibility_decision.json", "better_stm_checklist.json"]:
            artifact = load_json(DRY_RUN / example_id / filename)
            assert artifact["traceability"] == expected_trace
            for key, value in expected_trace.items():
                assert artifact[key] == value
                if value is not None:
                    assert (REPO / value).exists(), (example_id, filename, key, value)


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
