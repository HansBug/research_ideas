from __future__ import annotations

import importlib.util
from pathlib import Path
import json
import subprocess
import sys

import pytest

HELPER_PATH = Path(__file__).parent / "helpers" / "probe_discover_evidence_choice.py"
spec = importlib.util.spec_from_file_location("probe_discover_evidence_choice", HELPER_PATH)
assert spec is not None and spec.loader is not None
helper = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = helper
spec.loader.exec_module(helper)


def test_case_contract_matches_issue_165_section_13_1() -> None:
    records = {record["case_id"]: record for record in helper.contract_records()}

    assert tuple(records) == ("S1", "S2", "S3", "S4")
    assert records["S1"]["expected_evidence"] == ["query_structure"]
    assert records["S1"]["forbidden_evidence"] == ["simulate_concrete", "check_fbmcq"]
    assert records["S2"]["expected_evidence"] == ["simulate_concrete"]
    assert records["S3"]["expected_evidence"] == ["check_fbmcq"]
    assert records["S3"]["required_limitations"] == ["bounded"]
    assert records["S4"]["expected_evidence"] == ["check_fbmcq", "simulate_concrete"]
    assert records["S4"]["forbidden_evidence"] == []
    assert records["S4"]["required_limitations"] == ["bounded", "concrete"]


def test_visible_model_prompts_and_tool_docs_are_ascii_english() -> None:
    helper.assert_english_visible_prompts()
    texts = [helper.SYSTEM_PROMPT, helper.USER_PROMPT_TEMPLATE]
    texts.extend(item["description"] for item in helper.tool_prompt_manifest())
    for text in texts:
        text.encode("ascii")
        assert "必须" not in text
        assert "状态" not in text


def test_rubric_accepts_expected_choices_without_sequence_assertions() -> None:
    cases = {case.case_id: case for case in helper.CASES}

    s1 = helper.evaluate_rubric(cases["S1"], ["query_structure"], None)
    assert s1["passed"] is True

    s2 = helper.evaluate_rubric(
        cases["S2"],
        ["simulate_concrete"],
        {"selected_evidence": ["simulate_concrete"], "limitations": ["This is one concrete trace, not universal proof."]},
    )
    assert s2["passed"] is True

    s3 = helper.evaluate_rubric(
        cases["S3"],
        ["check_fbmcq"],
        {"selected_evidence": ["check_fbmcq"], "limitations": ["The formal result is bounded by analysis_bound=8."]},
    )
    assert s3["passed"] is True

    s4 = helper.evaluate_rubric(
        cases["S4"],
        ["simulate_concrete", "query_structure", "check_fbmcq"],
        {
            "selected_evidence": ["simulate_concrete", "query_structure", "check_fbmcq"],
            "limitations": ["The formal result is bounded and the concrete trace is not universal proof."],
        },
    )
    assert s4["passed"] is True

    s4_semantic_synonyms = helper.evaluate_rubric(
        cases["S4"],
        ["check_fbmcq", "simulate_concrete"],
        {
            "selected_evidence": ["check_fbmcq", "simulate_concrete"],
            "limitations": [
                "The analysis has a finite horizon of six steps.",
                "The simulation is a single execution witness, not a universal proof.",
            ],
        },
    )
    assert s4_semantic_synonyms["passed"] is True

    s4_analysis_bound_wording = helper.evaluate_rubric(
        cases["S4"],
        ["check_fbmcq", "simulate_concrete"],
        {
            "selected_evidence": ["check_fbmcq", "simulate_concrete"],
            "limitations": [
                "The formal result is verified only up to analysis bound 6.",
                "The simulation is a single witness, not a universal proof.",
            ],
        },
    )
    assert s4_analysis_bound_wording["passed"] is True


def test_rubric_rejects_semantic_mismatches() -> None:
    cases = {case.case_id: case for case in helper.CASES}

    s1 = helper.evaluate_rubric(cases["S1"], ["query_structure", "simulate_concrete"], None)
    assert s1["passed"] is False
    assert any("forbidden" in item for item in s1["failures"])

    s3 = helper.evaluate_rubric(
        cases["S3"],
        ["check_fbmcq"],
        {"selected_evidence": ["check_fbmcq"], "limitations": ["No limitation stated."]},
    )
    assert s3["passed"] is False
    assert any("bounded" in item for item in s3["failures"])

    s4 = helper.evaluate_rubric(cases["S4"], ["simulate_concrete"], None)
    assert s4["passed"] is False
    assert any("check_fbmcq" in item for item in s4["failures"])

    declared_only = helper.evaluate_rubric(
        cases["S3"],
        [],
        {
            "selected_evidence": ["check_fbmcq"],
            "limitations": ["The result is bounded."],
        },
    )
    assert declared_only["passed"] is False
    assert any("not executed" in item for item in declared_only["failures"])


def test_tool_call_names_counts_only_completed_business_calls() -> None:
    calls = [
        {"kind": "business", "name": "query_structure", "status": "requested"},
        {"kind": "business", "name": "query_structure", "status": "completed"},
        {"kind": "structured", "name": "EvidenceChoiceDecision", "status": "completed"},
    ]
    assert helper.tool_call_names(calls) == ["query_structure"]


@pytest.mark.parametrize(
    ("status", "error", "rubric", "expected"),
    [
        ("success", None, {"passed": True}, "none"),
        ("success", None, {"passed": False}, "semantic"),
        ("failed", {"code": "provider_error"}, {"passed": False}, "infrastructure"),
        ("failed", {"code": "structured_output_invalid"}, {"passed": False}, "semantic"),
    ],
)
def test_failure_kind_distinguishes_infrastructure_and_semantic(status, error, rubric, expected) -> None:
    assert helper.failure_kind(status, error, rubric) == expected


def test_cli_print_contract_is_importable_and_offline() -> None:
    completed = subprocess.run(
        [sys.executable, str(HELPER_PATH), "--print-contract"],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    lines = [json.loads(line) for line in completed.stdout.splitlines()]
    assert [line["case_id"] for line in lines] == ["S1", "S2", "S3", "S4"]
