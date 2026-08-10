from __future__ import annotations

import copy
import json
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
PAPER_ROOT = ROOT.parents[1]
SCHEMAS = ROOT / "schemas"
FIXTURES = ROOT / "fixtures" / "source_issue_ledger"
ISSUE_LIFECYCLE_DOCS = PAPER_ROOT / "experiment_design" / "issue_lifecycle"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def iter_fixture_ledgers():
    return sorted(FIXTURES.glob("*.json"))


@pytest.fixture(scope="module")
def source_issue_schema():
    return load_json(SCHEMAS / "source_issue_ledger.schema.json")


@pytest.fixture(scope="module")
def source_issue_validator(source_issue_schema):
    return jsonschema.Draft202012Validator(source_issue_schema)


def assert_invalid(validator: jsonschema.Draft202012Validator, ledger: dict, fragment: str | None = None):
    errors = sorted(validator.iter_errors(ledger), key=lambda e: list(e.path))
    assert errors, "mutated invalid ledger unexpectedly passed schema validation"
    if fragment is not None:
        joined = "\n".join(error.message for error in errors)
        assert fragment in joined


def first_issue(fixture_name: str) -> tuple[dict, dict]:
    ledger = load_json(FIXTURES / f"{fixture_name}.json")
    return ledger, ledger["issues"][0]


def test_source_issue_ledger_schema_is_valid_json_schema(source_issue_schema):
    jsonschema.Draft202012Validator.check_schema(source_issue_schema)


def test_committed_source_issue_ledger_fixtures_validate_against_schema(source_issue_validator):
    fixture_paths = iter_fixture_ledgers()
    assert {path.stem for path in fixture_paths} == {
        "expression_debt_folded_event",
        "confirmed_guard_mismatch",
        "raw_internal_inconsistency_confirmed",
        "conversion_artifact_rejected",
        "out_of_scope_timed_case",
        "insufficient_evidence_candidate",
    }
    for path in fixture_paths:
        source_issue_validator.validate(load_json(path))


def test_fixtures_are_contract_fixtures_not_seed_or_archive_annotations():
    forbidden_fragments = ["selected_seed_examples", "archive/r5_7", "runs/", "/home/"]
    for path in iter_fixture_ledgers():
        ledger = load_json(path)
        assert ledger["ledger_scope"] == "contract_fixture"
        assert ledger["source_model_id"].startswith("synthetic-")
        text = json.dumps(ledger, ensure_ascii=False)
        assert not any(fragment in text for fragment in forbidden_fragments), path


def test_confirmed_issues_are_the_only_repair_eligible_issues():
    for path in iter_fixture_ledgers():
        ledger = load_json(path)
        for issue in ledger["issues"]:
            if issue["confirmation_status"] == "confirmed":
                assert issue["issue_level"] == "confirmed"
                assert issue["downstream_repair_allowed"] is True
                assert issue["attribution_boundary"]["source_level_claim_allowed"] is True
                assert issue["attribution_boundary"]["conversion_or_lowering_related"] is False
                assert issue["attribution_boundary"]["representation_related"] is False
                assert issue["rejection_reason"] == ""
            else:
                assert issue["downstream_repair_allowed"] is False
                assert issue["confirmation_evidence_path"] == "not_applicable"


def test_nl_grounded_confirmed_issue_has_three_evidence_kinds():
    ledger, issue = first_issue("confirmed_guard_mismatch")
    assert issue["confirmation_status"] == "confirmed"
    assert issue["confirmation_evidence_path"] == "nl_grounded_behavioral_issue"
    assert issue["nl_evidence"]
    assert issue["source_stm_evidence"]
    assert issue["behavior_evidence"]
    assert {ev["evidence_type"] for ev in issue["behavior_evidence"]} != {"human_annotation"}
    jsonschema.Draft202012Validator(load_json(SCHEMAS / "source_issue_ledger.schema.json")).validate(ledger)


def test_raw_internal_inconsistency_path_does_not_require_nl_evidence_but_requires_internal_check():
    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    assert issue["confirmation_status"] == "confirmed"
    assert issue["confirmation_evidence_path"] == "raw_internal_inconsistency"
    assert issue["nl_evidence"] == []
    assert len(issue["source_element_refs"]) >= 2
    assert len(issue["source_stm_evidence"]) >= 2
    assert any(ev["evidence_type"] == "source_internal_consistency_check" for ev in issue["behavior_evidence"])
    assert "NL evidence is not required" in issue["confirmation_rationale"]
    assert "conversion" in issue["attribution_boundary"]["rationale"].lower()
    jsonschema.Draft202012Validator(load_json(SCHEMAS / "source_issue_ledger.schema.json")).validate(ledger)


def test_conversion_artifact_is_rejected_and_attribution_bounded():
    _, issue = first_issue("conversion_artifact_rejected")
    assert issue["confirmation_status"] == "rejected_conversion_artifact"
    assert issue["issue_level"] == "rejected"
    assert issue["downstream_repair_allowed"] is False
    assert issue["attribution_boundary"]["source_level_claim_allowed"] is False
    assert issue["attribution_boundary"]["conversion_or_lowering_related"] is True


def test_expression_debt_fixture_stays_candidate_only():
    _, issue = first_issue("expression_debt_folded_event")
    assert issue["confirmation_status"] == "candidate_only"
    assert issue["issue_family"] == "expression_debt_or_folded_behavior"
    assert issue["downstream_repair_allowed"] is False


def test_schema_rejects_non_confirmed_repair_eligible_mutation(source_issue_validator):
    ledger, issue = first_issue("expression_debt_folded_event")
    issue["downstream_repair_allowed"] = True
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_confirmed_without_confirmed_path(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["confirmation_evidence_path"] = "not_applicable"
    assert_invalid(source_issue_validator, ledger)



def test_schema_rejects_nl_grounded_without_nl_requirement(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["nl_evidence"] = [copy.deepcopy(issue["nl_evidence"][0])]
    issue["nl_evidence"][0]["evidence_type"] = "human_annotation"
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_nl_grounded_without_source_stm_fragment(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["source_stm_evidence"] = [copy.deepcopy(issue["source_stm_evidence"][0])]
    issue["source_stm_evidence"][0]["evidence_type"] = "human_annotation"
    assert_invalid(source_issue_validator, ledger)


@pytest.mark.parametrize("weak_type", ["human_annotation", "other_reference", "conversion_report"])
def test_schema_rejects_nl_grounded_without_behavioral_typed_evidence(source_issue_validator, weak_type):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["behavior_evidence"] = [copy.deepcopy(issue["behavior_evidence"][0])]
    issue["behavior_evidence"][0]["evidence_type"] = weak_type
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_raw_internal_with_nl_evidence(source_issue_validator):
    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    issue["nl_evidence"] = [
        {
            "evidence_id": "NL1",
            "evidence_type": "nl_requirement",
            "reference": "synthetic NL should not be attached to the raw-internal path",
            "summary": "Raw-internal path must remain independent from NL evidence in v0.",
        }
    ]
    assert_invalid(source_issue_validator, ledger)

def test_schema_rejects_raw_internal_without_internal_consistency_evidence(source_issue_validator):
    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    issue["behavior_evidence"] = [copy.deepcopy(issue["behavior_evidence"][0])]
    issue["behavior_evidence"][0]["evidence_type"] = "probe_result"
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_raw_internal_without_nl_not_required_rationale(source_issue_validator):
    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    issue["confirmation_rationale"] = "The raw/source artifact is internally contradictory."
    assert_invalid(source_issue_validator, ledger)



def test_schema_rejects_raw_internal_with_single_source_element_or_evidence(source_issue_validator):
    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    issue["source_element_refs"] = issue["source_element_refs"][:1]
    assert_invalid(source_issue_validator, ledger)

    ledger, issue = first_issue("raw_internal_inconsistency_confirmed")
    issue["source_stm_evidence"] = issue["source_stm_evidence"][:1]
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_confirmed_expression_debt_family(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["issue_family"] = "expression_debt_or_folded_behavior"
    assert_invalid(source_issue_validator, ledger)

def test_schema_rejects_conversion_artifact_with_source_level_claim_allowed(source_issue_validator):
    ledger, issue = first_issue("conversion_artifact_rejected")
    issue["attribution_boundary"]["source_level_claim_allowed"] = True
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_confirmed_conversion_family(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["issue_family"] = "conversion_artifact"
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_confirmed_empty_source_element_refs(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["source_element_refs"] = []
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_behavior_evidence_that_is_actually_nl_requirement(source_issue_validator):
    ledger, issue = first_issue("confirmed_guard_mismatch")
    issue["behavior_evidence"][0]["evidence_type"] = "nl_requirement"
    assert_invalid(source_issue_validator, ledger)


def test_schema_rejects_rejected_other_without_reason(source_issue_validator):
    ledger, issue = first_issue("conversion_artifact_rejected")
    issue["confirmation_status"] = "rejected_other"
    issue["issue_family"] = "other_v0"
    issue["rejection_reason"] = ""
    issue["attribution_boundary"]["conversion_or_lowering_related"] = False
    issue["attribution_boundary"]["representation_related"] = False
    assert_invalid(source_issue_validator, ledger)


def test_no_fixture_uses_better_stm_or_constructed_stmk_as_active_protocol():
    forbidden = ["can_claim_better_stm", "which stm is better", "better stm", "blind adjudication"]
    for path in [SCHEMAS / "source_issue_ledger.schema.json", *iter_fixture_ledgers()]:
        text = path.read_text(encoding="utf-8").lower()
        assert not any(term in text for term in forbidden), path


def test_issue_lifecycle_markdown_links_resolve():
    import re

    for md_path in sorted(ISSUE_LIFECYCLE_DOCS.rglob("*.md")):
        text = md_path.read_text(encoding="utf-8")
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if target.startswith(("http://", "https://", "#")):
                continue
            clean_target = target.split("#", 1)[0]
            if not clean_target:
                continue
            resolved = (md_path.parent / clean_target).resolve()
            assert resolved.exists(), f"{md_path}: broken link {target} -> {resolved}"
