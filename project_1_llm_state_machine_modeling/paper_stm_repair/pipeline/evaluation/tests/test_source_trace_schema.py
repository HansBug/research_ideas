from __future__ import annotations

import copy
import json
from collections import defaultdict
from pathlib import Path

import jsonschema
import pytest

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
TRACE_FIXTURES = ROOT / "fixtures" / "source_trace"
ISSUE_FIXTURES = ROOT / "fixtures" / "source_issue_ledger"

NEGATIVE_TRACE_RELATIONS = {"ambiguous", "untraceable", "conversion_artifact"}
CLOSURE_ELIGIBLE_RELATIONS = {"exact", "normalized", "split"}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def iter_trace_fixture_paths():
    return sorted(TRACE_FIXTURES.glob("*.json"))


def iter_trace_entries():
    for path in iter_trace_fixture_paths():
        ledger = load_json(path)
        for entry in ledger["trace_entries"]:
            yield path, ledger, entry


@pytest.fixture(scope="module")
def source_trace_schema():
    return load_json(SCHEMAS / "source_trace.schema.json")


@pytest.fixture(scope="module")
def source_trace_validator(source_trace_schema):
    return jsonschema.Draft202012Validator(source_trace_schema)


def assert_invalid(validator: jsonschema.Draft202012Validator, ledger: dict):
    errors = sorted(validator.iter_errors(ledger), key=lambda e: list(e.path))
    assert errors, "mutated invalid source trace ledger unexpectedly passed schema validation"


def first_entry(fixture_name: str) -> tuple[dict, dict]:
    ledger = load_json(TRACE_FIXTURES / f"{fixture_name}.json")
    return ledger, ledger["trace_entries"][0]


def issue_by_id() -> dict[str, dict]:
    issues: dict[str, dict] = {}
    for path in ISSUE_FIXTURES.glob("*.json"):
        ledger = load_json(path)
        for issue in ledger["issues"]:
            assert issue["issue_id"] not in issues, issue["issue_id"]
            issues[issue["issue_id"]] = issue
    return issues


def confirmed_repair_issue_ids() -> set[str]:
    return {
        issue_id
        for issue_id, issue in issue_by_id().items()
        if issue["confirmation_status"] == "confirmed" and issue["downstream_repair_allowed"] is True
    }


def build_issue_to_trace_index() -> dict[str, list[dict]]:
    index: dict[str, list[dict]] = defaultdict(list)
    for _, _, entry in iter_trace_entries():
        for issue_id in entry["required_for_issue_ids"]:
            index[issue_id].append(entry)
    return index


def source_ids(entry: dict) -> set[str]:
    return {element["element_id"] for element in entry["source_elements"]}


def test_source_trace_schema_is_valid_json_schema(source_trace_schema):
    jsonschema.Draft202012Validator.check_schema(source_trace_schema)


def test_committed_source_trace_fixtures_validate_against_schema(source_trace_validator):
    fixture_paths = iter_trace_fixture_paths()
    assert {path.stem for path in fixture_paths} == {
        "exact_transition_trace",
        "normalized_guard_trace",
        "split_transition_trace",
        "ambiguous_trace",
        "untraceable_element",
        "conversion_artifact_trace",
    }
    for path in fixture_paths:
        source_trace_validator.validate(load_json(path))


def test_fixtures_are_contract_fixtures_not_seed_archive_or_run_records():
    forbidden_fragments = ["selected_seed_examples", "archive/r5_7", "runs/", "/home/"]
    for path in iter_trace_fixture_paths():
        ledger = load_json(path)
        assert ledger["trace_scope"] == "contract_fixture"
        assert ledger["source_model_id"].startswith("synthetic-")
        text = json.dumps(ledger, ensure_ascii=False)
        assert not any(fragment in text for fragment in forbidden_fragments), path


def test_v0_trace_relation_enum_excludes_merged_and_inferred(source_trace_validator):
    ledger, entry = first_entry("exact_transition_trace")
    for unsupported in ["merged", "inferred"]:
        mutated = copy.deepcopy(ledger)
        mutated["trace_entries"][0]["trace_relation"] = unsupported
        assert_invalid(source_trace_validator, mutated)


def test_exact_and_normalized_traces_are_projectable_with_positive_claim_boundary():
    for fixture_name in ["exact_transition_trace", "normalized_guard_trace"]:
        _, entry = first_entry(fixture_name)
        assert entry["projection_status"] == "projectable"
        assert entry["attribution_boundary"]["source_level_claim_allowed"] is True
        assert entry["attribution_boundary"]["closure_claim_allowed"] is True
        assert entry["attribution_boundary"]["conversion_or_lowering_related"] is False
        assert entry["source_elements"]
        assert entry["intermediate_elements"]


def test_normalized_trace_requires_normalization_evidence(source_trace_validator):
    ledger, entry = first_entry("normalized_guard_trace")
    assert any(ev["evidence_type"] == "normalization_report" for ev in entry["trace_evidence"])
    mutated = copy.deepcopy(ledger)
    for ev in mutated["trace_entries"][0]["trace_evidence"]:
        if ev["evidence_type"] == "normalization_report":
            ev["evidence_type"] = "structural_match"
    assert_invalid(source_trace_validator, mutated)


def test_split_trace_is_partially_projectable_not_full_closure(source_trace_validator):
    ledger, entry = first_entry("split_transition_trace")
    assert entry["trace_relation"] == "split"
    assert entry["projection_status"] == "partially_projectable"
    assert entry["attribution_boundary"]["source_level_claim_allowed"] is True
    assert entry["attribution_boundary"]["closure_claim_allowed"] is False
    assert len(entry["intermediate_elements"]) >= 2
    assert len(entry["trace_relation_rationale"]) >= 20
    assert entry["projection_detail"]["projectable_source_behavior"]
    assert entry["projection_detail"]["non_projectable_or_ambiguous_part"]
    assert entry["projection_detail"]["closure_implication"]

    mutated = copy.deepcopy(ledger)
    mutated["trace_entries"][0]["projection_status"] = "projectable"
    mutated["trace_entries"][0]["attribution_boundary"]["closure_claim_allowed"] = True
    assert_invalid(source_trace_validator, mutated)

    mutated = copy.deepcopy(ledger)
    del mutated["trace_entries"][0]["projection_detail"]
    assert_invalid(source_trace_validator, mutated)


def test_negative_trace_relations_have_negative_claim_boundary_and_unprojectable_status(source_trace_validator):
    for fixture_name in ["ambiguous_trace", "untraceable_element", "conversion_artifact_trace"]:
        ledger, entry = first_entry(fixture_name)
        assert entry["trace_relation"] in NEGATIVE_TRACE_RELATIONS
        assert entry["attribution_boundary"]["source_level_claim_allowed"] is False
        assert entry["attribution_boundary"]["closure_claim_allowed"] is False
        assert entry["projection_status"] in {"unprojectable", "not_applicable"}

        mutated = copy.deepcopy(ledger)
        mutated["trace_entries"][0]["attribution_boundary"]["source_level_claim_allowed"] = True
        assert_invalid(source_trace_validator, mutated)

        mutated = copy.deepcopy(ledger)
        mutated["trace_entries"][0]["attribution_boundary"]["closure_claim_allowed"] = True
        assert_invalid(source_trace_validator, mutated)


def test_untraceable_requires_empty_source_and_negative_trace_evidence(source_trace_validator):
    ledger, entry = first_entry("untraceable_element")
    assert entry["source_elements"] == []
    assert any(ev["evidence_type"] == "negative_trace_check" for ev in entry["trace_evidence"])

    mutated = copy.deepcopy(ledger)
    mutated["trace_entries"][0]["source_elements"] = [
        {
            "element_id": "T_fake",
            "element_type": "transition",
            "reference": "fake source element",
            "summary": "Mutation should not be allowed for untraceable relation.",
        }
    ]
    assert_invalid(source_trace_validator, mutated)


def test_conversion_artifact_trace_is_not_a_source_level_confirmed_issue_trace():
    issues = issue_by_id()
    _, entry = first_entry("conversion_artifact_trace")
    assert entry["trace_relation"] == "conversion_artifact"
    assert entry["projection_status"] == "not_applicable"
    assert entry["attribution_boundary"]["conversion_or_lowering_related"] is True
    assert any(ev["evidence_type"] == "conversion_report" for ev in entry["trace_evidence"])
    assert entry["required_for_issue_ids"] == ["ISSUE.CONV.001"]
    assert issues["ISSUE.CONV.001"]["confirmation_status"] == "rejected_conversion_artifact"


def test_required_issue_ids_exist_in_source_issue_ledger_fixtures():
    issues = issue_by_id()
    for path, _, entry in iter_trace_entries():
        for issue_id in entry["required_for_issue_ids"]:
            assert issue_id in issues, (path, entry["trace_id"], issue_id)


def test_negative_trace_relations_do_not_bind_confirmed_repair_eligible_issues():
    confirmed_ids = confirmed_repair_issue_ids()
    for path, _, entry in iter_trace_entries():
        if entry["trace_relation"] in NEGATIVE_TRACE_RELATIONS:
            assert not (set(entry["required_for_issue_ids"]) & confirmed_ids), (path, entry["trace_id"])


def test_confirmed_repair_eligible_issues_have_projectable_or_partial_trace_coverage():
    issues = issue_by_id()
    index = build_issue_to_trace_index()

    assert confirmed_repair_issue_ids() == {"ISSUE.GUARD.001", "ISSUE.INTERNAL.001"}

    for issue_id in confirmed_repair_issue_ids():
        issue = issues[issue_id]
        traces = index[issue_id]
        assert traces, issue_id
        eligible_traces = [
            entry
            for entry in traces
            if entry["trace_relation"] in CLOSURE_ELIGIBLE_RELATIONS
            and entry["projection_status"] in {"projectable", "partially_projectable"}
            and entry["attribution_boundary"]["source_level_claim_allowed"] is True
        ]
        assert eligible_traces, issue_id
        traced_source_ids = set().union(*(source_ids(entry) for entry in eligible_traces))
        issue_source_ids = {element["element_id"] for element in issue["source_element_refs"]}
        assert issue_source_ids <= traced_source_ids


def test_reverse_index_is_the_authoritative_issue_to_trace_link_for_v0():
    index = build_issue_to_trace_index()
    assert {entry["trace_id"] for entry in index["ISSUE.GUARD.001"]} == {
        "TRACE.EXACT.T_MOVE",
        "TRACE.NORM.DOOR_GUARD",
    }
    assert {entry["trace_id"] for entry in index["ISSUE.INTERNAL.001"]} == {
        "TRACE.SPLIT.UNLOCK_CONFLICT"
    }


def test_source_trace_schema_and_fixtures_do_not_reintroduce_better_stm_protocol_words():
    forbidden = [
        "can_claim_better_stm",
        "which stm is better",
        "blind adjudication",
        "constructed STM_k",
        "method effectiveness",
    ]
    paths = [SCHEMAS / "source_trace.schema.json", *iter_trace_fixture_paths()]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        assert not any(fragment.lower() in lowered for fragment in forbidden), path


def test_projectable_entries_require_source_and_intermediate_elements(source_trace_validator):
    for fixture_name in ["exact_transition_trace", "normalized_guard_trace", "split_transition_trace"]:
        ledger, _ = first_entry(fixture_name)
        mutated = copy.deepcopy(ledger)
        mutated["trace_entries"][0]["source_elements"] = []
        assert_invalid(source_trace_validator, mutated)

        mutated = copy.deepcopy(ledger)
        mutated["trace_entries"][0]["intermediate_elements"] = []
        assert_invalid(source_trace_validator, mutated)


def test_schema_rejects_extra_fields_to_keep_contract_stable(source_trace_validator):
    ledger, _ = first_entry("exact_transition_trace")
    mutated = copy.deepcopy(ledger)
    mutated["trace_entries"][0]["method_effectiveness_claim"] = True
    assert_invalid(source_trace_validator, mutated)
