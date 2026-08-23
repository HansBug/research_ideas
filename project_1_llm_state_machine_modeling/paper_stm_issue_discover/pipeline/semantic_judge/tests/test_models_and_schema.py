from __future__ import annotations

import inspect
import json
import re
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
from pipeline.semantic_judge.protocol import (
    ARBITRATION_INSTRUCTION,
    PRIMARY_INSTRUCTION,
    SYSTEM_PROMPT,
)
from pipeline.semantic_judge.schema import (
    build_exact_response_model,
    materialize_reading,
)
from pydantic import BaseModel, ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REPOSITORY_ROOT = PROJECT_ROOT.parents[1]


def minimal_input(
    *, report_count: int = 1, expected_count: int = 1
) -> UnifiedJudgeInput:
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
                    "report_text_evidence": [
                        {
                            "report_field": "claim",
                            "exact_quote": report.claim,
                            "semantic_role": "CLAIM_BOUNDARY",
                            "reason": "The exact claim defines the report boundary.",
                            "basis": f"CandidateReport {report.report_id}.claim",
                        },
                        *(
                            [
                                {
                                    "report_field": "reason",
                                    "exact_quote": report.reason,
                                    "semantic_role": "CAUSAL_SUPPORT",
                                    "reason": "The exact report reason supplies causal support for this fixture relation.",
                                    "basis": f"CandidateReport {report.report_id}.reason",
                                }
                            ]
                            if match
                            in {MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH}
                            else []
                        ),
                    ],
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
        has_known_relation = any(
            matches.get(
                (report.report_id, expected.expected_id), MatchStrength.NO_MATCH
            )
            in {MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH}
            for expected in judge_input.expected_issues
        )
        selected_validity = validity.get(
            report.report_id,
            ReportValidity.VALID_KNOWN
            if has_known_relation
            else ReportValidity.VALID_NOVEL,
        )
        report_rows.append(
            {
                "report_id": report.report_id,
                "validity": selected_validity.value,
                "root_cause_cluster_key": clusters.get(
                    report.report_id, f"technical-cause-{report.report_id}"
                ),
                "report_text_evidence": [
                    {
                        "report_field": "claim",
                        "exact_quote": report.claim,
                        "semantic_role": "CLAIM_BOUNDARY",
                        "reason": "The exact claim defines the report boundary.",
                        "basis": f"CandidateReport {report.report_id}.claim",
                    },
                    {
                        "report_field": "reason",
                        "exact_quote": report.reason,
                        "semantic_role": (
                            "REFUTED_PREMISE"
                            if selected_validity == ReportValidity.INVALID
                            else "CAUSAL_SUPPORT"
                        ),
                        "reason": "The exact report reason supplies the validity evidence role for this fixture.",
                        "basis": f"CandidateReport {report.report_id}.reason",
                    },
                ],
                "reason": f"artifact review classifies {report.report_id}",
                "basis": "fixture artifact truth review",
                "source_refs": [
                    f"report:{report.report_id}",
                    "artifact:natural_language",
                ],
            }
        )
    expected_rows = []
    for expected in judge_input.expected_issues:
        expected_rows.append(
            {
                "expected_id": expected.expected_id,
                "reason": f"coverage for {expected.expected_id}",
                "basis": "fixture relation and validity matrix",
                "source_refs": [
                    f"expected:{expected.expected_id}",
                    "artifact:natural_language",
                ],
            }
        )
    return {
        "schema_version": "paper1.semantic-judge.response.v3",
        "relations": relation_rows,
        "report_judgments": report_rows,
        "expected_judgments": expected_rows,
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


def test_judge_prompts_and_runtime_schema_use_english_audit_language() -> None:
    han_text = re.compile(r"[\u3400-\u9fff]")
    classes = [
        value
        for value in vars(models).values()
        if inspect.isclass(value)
        and issubclass(value, BaseModel)
        and value.__module__ == models.__name__
    ]
    for model in classes:
        assert not han_text.search(inspect.getdoc(model) or ""), model.__name__
        for field_name, field in model.model_fields.items():
            assert not han_text.search(field.description or ""), (
                f"{model.__name__}.{field_name}"
            )
        schema_text = json.dumps(
            model.model_json_schema(), ensure_ascii=False, sort_keys=True
        )
        assert not han_text.search(schema_text), model.__name__

    for prompt in (SYSTEM_PROMPT, PRIMARY_INSTRUCTION, ARBITRATION_INSTRUCTION):
        assert not han_text.search(prompt)
        assert "in English" in prompt


def test_runtime_schema_contains_descriptions_enums_and_exact_literals() -> None:
    judge_input = minimal_input(report_count=2, expected_count=2)
    schema = build_exact_response_model(judge_input).model_json_schema()
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
    properties = schema["properties"]
    assert "report_judgments" in properties
    assert "expected_judgments" in properties
    assert "report_assessments" not in properties
    assert "expected_assessments" not in properties
    assert "full_expected_ids" not in serialized


def test_exact_schema_rejects_missing_relation_and_inconsistent_validity() -> None:
    judge_input = minimal_input(report_count=1, expected_count=2)
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(judge_input)
    payload["relations"].pop()
    with pytest.raises(ValidationError, match="relations"):
        schema.model_validate(payload)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
        validity={"R0001": ReportValidity.VALID_NOVEL},
    )
    with pytest.raises(
        ValidationError, match="VALID_NOVEL requires all relations NO_MATCH"
    ):
        schema.model_validate(payload)


def test_exact_schema_rejects_report_quote_not_owned_by_selected_field() -> None:
    judge_input = minimal_input()
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(judge_input)
    payload["relations"][0]["report_text_evidence"][0]["exact_quote"] = (
        "fact invented from common artifacts"
    )

    with pytest.raises(
        ValidationError, match="exact_quote is not a case-sensitive substring"
    ):
        schema.model_validate(payload)


def test_full_relation_requires_report_owned_causal_support() -> None:
    judge_input = minimal_input()
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    payload["relations"][0]["report_text_evidence"] = [
        row
        for row in payload["relations"][0]["report_text_evidence"]
        if row["semantic_role"] != "CAUSAL_SUPPORT"
    ]

    with pytest.raises(
        ValidationError, match="requires CAUSAL_SUPPORT for FULL_MATCH"
    ):
        schema.model_validate(payload)


def test_invalid_report_requires_an_exact_refuted_premise() -> None:
    judge_input = minimal_input()
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(
        judge_input,
        validity={"R0001": ReportValidity.INVALID},
    )
    payload["report_judgments"][0]["report_text_evidence"] = [
        row
        for row in payload["report_judgments"][0]["report_text_evidence"]
        if row["semantic_role"] != "REFUTED_PREMISE"
    ]

    with pytest.raises(
        ValidationError, match="requires REFUTED_PREMISE for INVALID"
    ):
        schema.model_validate(payload)


def test_backend_materializes_relation_sets_hit_and_support() -> None:
    judge_input = minimal_input(report_count=2, expected_count=2)
    payload = reading_payload(
        judge_input,
        matches={
            ("R0001", "E0001"): MatchStrength.FULL_MATCH,
            ("R0002", "E0002"): MatchStrength.PARTIAL_MATCH,
        },
    )
    response = build_exact_response_model(judge_input).model_validate(payload)
    reading = materialize_reading(response)
    assert reading.report_assessments[0].full_expected_ids == ("E0001",)
    assert reading.report_assessments[1].partial_expected_ids == ("E0002",)
    assert reading.expected_assessments[0].hit
    assert reading.expected_assessments[1].supported
    assert not reading.expected_assessments[1].hit


def test_common_artifact_closure_is_adapter_independent() -> None:
    report_root = PROJECT_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
    first = build_artifact_closure(report_root, "0004")
    second = build_artifact_closure(report_root, "0004")
    assert first == second
    assert first.closure_hash == second.closure_hash
    assert len(first.artifacts) == 12
    assert {item.role for item in first.artifacts} == set(ArtifactRole)


def test_0029_stage_projection_fits_context_without_dropping_core_evidence() -> None:
    report_root = PROJECT_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"
    closure = build_artifact_closure(report_root, "0029")
    by_role = {item.role: item for item in closure.artifacts}
    total_characters = sum(len(item.content) for item in closure.artifacts)
    assert total_characters < 300_000
    for role in (
        ArtifactRole.NATURAL_LANGUAGE,
        ArtifactRole.PLANTUML_SOURCE,
        ArtifactRole.FCSTM_MODEL,
        ArtifactRole.EXACT_SOURCE_INVENTORY,
        ArtifactRole.INSPECTION_EQUIVALENT_FACTS,
        ArtifactRole.VERIFY_FACTS,
        ArtifactRole.SMT_FACTS,
        ArtifactRole.SOURCE_TRACE,
    ):
        assert by_role[role].content
    for role in (
        ArtifactRole.CANONICAL_SOURCE_IR,
        ArtifactRole.REFERENCE_INSPECTION,
        ArtifactRole.WORKING_CONTRACT,
        ArtifactRole.CASE_REPORT,
    ):
        projection = json.loads(by_role[role].content)["projection"]
        assert projection["source_sha256"].startswith("sha256:")
        assert projection["included_fields"]
        assert projection["omitted_fields"]
        assert projection["truncation_applied"] is False


def test_both_adapters_emit_one_candidate_schema_without_privileged_fields(
    tmp_path: Path,
) -> None:
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
    baseline_reports, baseline_audit, _, _ = adapt_x1v2_record(baseline, expected_map)
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
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
        validity={"R0001": ReportValidity.VALID_NOVEL},
    )
    with pytest.raises(
        ValidationError, match="VALID_NOVEL requires all relations NO_MATCH"
    ):
        schema.model_validate(payload)
