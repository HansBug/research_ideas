from __future__ import annotations

import inspect
from pathlib import Path

import pytest
from pipeline.semantic_judge import models
from pipeline.semantic_judge.artifacts import (
    adapt_evidence_discovery_release,
    adapt_x1v2_record,
    build_artifact_closure,
    build_unified_input,
    candidate_schema_field_set,
    load_expected_issues,
)
from pipeline.semantic_judge.models import (
    ArtifactAuthority,
    ArtifactDocument,
    ArtifactRole,
    CandidateReport,
    ExpectedAxisHints,
    ExpectedIssue,
    JudgeArtifactClosure,
    MatchStrength,
    ReportValidity,
    UnifiedJudgeInput,
)
from pipeline.semantic_judge.schema import build_exact_reading_model
from pydantic import BaseModel, ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]


def minimal_input(*, report_count: int = 1, expected_count: int = 1) -> UnifiedJudgeInput:
    artifact = ArtifactDocument(
        artifact_id="artifact:natural_language",
        role=ArtifactRole.NATURAL_LANGUAGE,
        authority=ArtifactAuthority.NORMATIVE_SOURCE,
        sha256="sha256:" + "1" * 64,
        schema_version="text.v1",
        content="NL1: required behavior",
        reason="The normative source is required.",
        basis="fixture source",
    )
    closure = JudgeArtifactClosure(
        pair_id="0023",
        artifacts=(artifact,),
        closure_hash="sha256:" + "2" * 64,
        reason="Fixture common closure.",
        basis="provider-free fixture",
    )
    reports = tuple(
        CandidateReport(
            report_id=f"R{index:04d}",
            claim=f"claim {index}",
            reason=f"reason {index}",
        )
        for index in range(1, report_count + 1)
    )
    expected = tuple(
        ExpectedIssue(
            expected_id=f"E{index:04d}",
            summary=f"expected {index}",
            detail=f"expected detail {index}",
            axes=ExpectedAxisHints(),
            source_refs=(f"expected:E{index:04d}",),
        )
        for index in range(1, expected_count + 1)
    )
    return build_unified_input(
        reports=reports,
        expected_issues=expected,
        artifact_closure=closure,
    )


def reading_payload(
    judge_input: UnifiedJudgeInput,
    *,
    matches: dict[tuple[str, str], MatchStrength] | None = None,
    validity: dict[str, ReportValidity] | None = None,
    clusters: dict[str, str] | None = None,
) -> dict:
    matches = matches or {}
    validity = validity or {}
    clusters = clusters or {}
    relation_rows = []
    for report in judge_input.reports:
        for expected in judge_input.expected_issues:
            match = matches.get(
                (report.report_id, expected.expected_id), MatchStrength.NO_MATCH
            )
            relation_rows.append(
                {
                    "report_id": report.report_id,
                    "expected_id": expected.expected_id,
                    "match": match.value,
                    "reason": f"{report.report_id} to {expected.expected_id} is {match.value}",
                    "basis": "fixture report, expected, and artifact evidence",
                    "source_refs": [
                        f"report:{report.report_id}",
                        f"expected:{expected.expected_id}",
                        "artifact:natural_language",
                    ],
                }
            )
    report_rows = []
    for report in judge_input.reports:
        full = [
            expected.expected_id
            for expected in judge_input.expected_issues
            if matches.get((report.report_id, expected.expected_id), MatchStrength.NO_MATCH)
            == MatchStrength.FULL_MATCH
        ]
        partial = [
            expected.expected_id
            for expected in judge_input.expected_issues
            if matches.get((report.report_id, expected.expected_id), MatchStrength.NO_MATCH)
            == MatchStrength.PARTIAL_MATCH
        ]
        no_match = [
            expected.expected_id
            for expected in judge_input.expected_issues
            if expected.expected_id not in {*full, *partial}
        ]
        selected_validity = validity.get(
            report.report_id,
            ReportValidity.VALID_KNOWN
            if full or partial
            else ReportValidity.VALID_NOVEL,
        )
        report_rows.append(
            {
                "report_id": report.report_id,
                "validity": selected_validity.value,
                "full_expected_ids": full,
                "partial_expected_ids": partial,
                "no_match_expected_ids": no_match,
                "root_cause_cluster_key": clusters.get(
                    report.report_id, f"technical-cause-{report.report_id}"
                ),
                "reason": f"artifact review classifies {report.report_id}",
                "basis": "fixture artifact truth review",
                "source_refs": [f"report:{report.report_id}", "artifact:natural_language"],
            }
        )
    report_validity = {
        row["report_id"]: ReportValidity(row["validity"]) for row in report_rows
    }
    expected_rows = []
    for expected in judge_input.expected_issues:
        full_reports = [
            report.report_id
            for report in judge_input.reports
            if report_validity[report.report_id] == ReportValidity.VALID_KNOWN
            and matches.get((report.report_id, expected.expected_id), MatchStrength.NO_MATCH)
            == MatchStrength.FULL_MATCH
        ]
        partial_reports = [
            report.report_id
            for report in judge_input.reports
            if report_validity[report.report_id] == ReportValidity.VALID_KNOWN
            and matches.get((report.report_id, expected.expected_id), MatchStrength.NO_MATCH)
            == MatchStrength.PARTIAL_MATCH
        ]
        unsupported = [
            report.report_id
            for report in judge_input.reports
            if report.report_id not in {*full_reports, *partial_reports}
        ]
        expected_rows.append(
            {
                "expected_id": expected.expected_id,
                "full_report_ids": full_reports,
                "partial_report_ids": partial_reports,
                "no_support_report_ids": unsupported,
                "hit": bool(full_reports),
                "supported": bool(full_reports or partial_reports),
                "reason": f"coverage for {expected.expected_id}",
                "basis": "fixture relation and validity matrix",
                "source_refs": [f"expected:{expected.expected_id}", "artifact:natural_language"],
            }
        )
    return {
        "schema_version": "paper1.semantic-judge.reading.v1",
        "relations": relation_rows,
        "report_assessments": report_rows,
        "expected_assessments": expected_rows,
        "reason": "Complete provider-free fixture reading.",
        "basis": "Issue #195 fixture matrix and artifact review.",
        "source_refs": ["artifact:natural_language"],
    }


def test_every_pydantic_model_and_field_has_description() -> None:
    classes = [
        value
        for value in vars(models).values()
        if inspect.isclass(value)
        and issubclass(value, BaseModel)
        and value.__module__ == models.__name__
    ]
    assert classes
    for model in classes:
        assert inspect.getdoc(model), model.__name__
        for field_name, field in model.model_fields.items():
            assert field.description, f"{model.__name__}.{field_name}"


def test_runtime_schema_contains_descriptions_enums_and_exact_literals() -> None:
    judge_input = minimal_input(report_count=2, expected_count=2)
    schema = build_exact_reading_model(judge_input).model_json_schema()
    serialized = str(schema)
    assert schema["description"]
    assert schema["properties"]["relations"]["description"]
    assert "FULL_MATCH" in serialized
    assert "PARTIAL_MATCH" in serialized
    assert "NO_MATCH" in serialized
    assert "VALID_KNOWN" in serialized
    assert "VALID_NOVEL" in serialized
    assert "INVALID" in serialized
    assert "R0001" in serialized and "R0002" in serialized
    assert "E0001" in serialized and "E0002" in serialized


def test_exact_schema_rejects_missing_relation_and_inconsistent_summary() -> None:
    judge_input = minimal_input(report_count=1, expected_count=2)
    schema = build_exact_reading_model(judge_input)
    payload = reading_payload(judge_input)
    payload["relations"].pop()
    with pytest.raises(ValidationError, match="relations"):
        schema.model_validate(payload)
    payload = reading_payload(judge_input)
    payload["expected_assessments"][0]["hit"] = True
    with pytest.raises(ValidationError, match=r"expected_assessments\[E0001\]"):
        schema.model_validate(payload)


def test_common_artifact_closure_is_adapter_independent() -> None:
    report_root = PROJECT_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
    first = build_artifact_closure(report_root, "0004")
    second = build_artifact_closure(report_root, "0004")
    assert first == second
    assert first.closure_hash == second.closure_hash
    assert len(first.artifacts) == 12
    assert {item.role for item in first.artifacts} == set(ArtifactRole)


def test_both_adapters_emit_one_candidate_schema_without_privileged_fields(tmp_path: Path) -> None:
    ledger = PROJECT_ROOT / "discover_matrix/ledger_v2/ledger.json"
    _, expected_map = load_expected_issues(ledger, "0004")
    baseline = tmp_path / "baseline.json"
    baseline.write_text(
        '{"status":"ok","pair_id":"llms_emp_feedback_final_0004","round":1,'
        '"parsed_output":{"issues":[{"issue":"claim","where":"state A",'
        '"reason":"because"}]}}',
        encoding="utf-8",
    )
    method = tmp_path / "method.json"
    method.write_text(
        '{"status":"completed","eligible":true,"pair_id":"0004","round":1,'
        '"report_issue_clusters":[{"issue_id":"original-1","title":"claim",'
        '"candidate_reason":"because","candidate_basis":"NL1","locus_kind":"state",'
        '"locus_names":["A"],"property":"deadlock_freedom","expected":"continues",'
        '"observed":"dead end","source_refs":["NL1"],"element_refs":["state:A"]}]}',
        encoding="utf-8",
    )
    baseline_reports, baseline_audit, _, _ = adapt_x1v2_record(
        baseline, expected_map
    )
    method_reports, method_audit, _, _ = adapt_evidence_discovery_release(
        method, expected_map
    )
    assert baseline_audit.projected_field_names == method_audit.projected_field_names
    assert set(baseline_audit.projected_field_names) == candidate_schema_field_set()
    assert baseline_reports[0].property is None
    assert baseline_reports[0].basis is None
    assert method_reports[0].property == "deadlock_freedom"
    forbidden = {"d_level", "witness_level", "predicate_id", "arm", "L"}
    assert forbidden.isdisjoint(baseline_reports[0].model_dump())
    assert forbidden.isdisjoint(method_reports[0].model_dump())


def test_valid_novel_requires_all_no_match_structurally() -> None:
    judge_input = minimal_input()
    schema = build_exact_reading_model(judge_input)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
        validity={"R0001": ReportValidity.VALID_NOVEL},
    )
    with pytest.raises(ValidationError, match="VALID_NOVEL requires all relations NO_MATCH"):
        schema.model_validate(payload)
