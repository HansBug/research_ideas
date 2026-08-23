from __future__ import annotations

import inspect
import json
import re
from pathlib import Path

import pytest
from pydantic import BaseModel, ValidationError

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
    CoreClaimTruth,
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
from pipeline.semantic_judge.scale_audit import build_scale_audit
from pipeline.semantic_judge.schema import (
    build_exact_response_model,
    materialize_reading,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]


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
        basis="Provider-free fixture source.",
    )
    closure = JudgeArtifactClosure(
        pair_id="0023",
        artifacts=(artifact,),
        closure_hash="sha256:" + "2" * 64,
        reason="Fixture common closure.",
        basis="Provider-free fixture.",
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
    """Build a sparse provider response without bypassing exact validation."""

    matches = matches or {}
    validity = validity or {}
    clusters = clusters or {}
    report_rows = []
    for report in judge_input.reports:
        has_positive = any(
            matches.get(
                (report.report_id, expected.expected_id), MatchStrength.NO_MATCH
            )
            in {MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH}
            for expected in judge_input.expected_issues
        )
        selected_validity = validity.get(
            report.report_id,
            ReportValidity.VALID_KNOWN
            if has_positive
            else ReportValidity.VALID_NOVEL,
        )
        core_truth = (
            CoreClaimTruth.INVALID
            if selected_validity == ReportValidity.INVALID
            else CoreClaimTruth.VALID
        )
        positive_relations = []
        no_match_expected_ids = []
        for expected in judge_input.expected_issues:
            match = matches.get(
                (report.report_id, expected.expected_id), MatchStrength.NO_MATCH
            )
            if match in {MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH}:
                positive_relations.append(
                    {
                        "report_id": report.report_id,
                        "expected_id": expected.expected_id,
                        "match": match.value,
                        "report_field_refs": ["claim", "reason"],
                        "causal_certificate_field": "reason",
                        "reason": f"{report.report_id} to {expected.expected_id} is {match.value}.",
                        "basis": "Fixture report, expected issue, and artifact evidence.",
                        "source_refs": [
                            f"report:{report.report_id}",
                            f"expected:{expected.expected_id}",
                            "artifact:natural_language",
                        ],
                    }
                )
            else:
                no_match_expected_ids.append(expected.expected_id)
        report_rows.append(
            {
                "report_id": report.report_id,
                "core_truth": core_truth.value,
                "root_cause_cluster_key": clusters.get(
                    report.report_id, f"technical-cause-{report.report_id}"
                ),
                "causal_field_audits": [
                    {
                        "report_field": field_name,
                        "exact_text": field_value,
                        "verdict": (
                            "REFUTED"
                            if core_truth == CoreClaimTruth.INVALID
                            else "SUPPORTED"
                        ),
                        "reason": "The complete fixture causal field receives one artifact verdict.",
                        "basis": f"CandidateReport {report.report_id}.{field_name} and fixture artifacts.",
                        "source_refs": [
                            f"report:{report.report_id}:{field_name}",
                            "artifact:natural_language",
                        ],
                    }
                    for field_name in ("reason", "basis", "observed")
                    if isinstance((field_value := getattr(report, field_name)), str)
                ],
                "causal_certificate_field": "reason",
                "supported_relations": positive_relations,
                "no_match_expected_ids": no_match_expected_ids,
                "no_match_reason": (
                    "The listed expected issues have no true defect relation to this report."
                    if no_match_expected_ids
                    else None
                ),
                "no_match_basis": (
                    "Fixture report, expected issues, and common artifact closure."
                    if no_match_expected_ids
                    else None
                ),
                "no_match_source_refs": (
                    [f"report:{report.report_id}", "artifact:natural_language"]
                    if no_match_expected_ids
                    else None
                ),
                "reason": f"Artifact review classifies {report.report_id}.",
                "basis": "Fixture artifact truth review.",
                "source_refs": [
                    f"report:{report.report_id}",
                    "artifact:natural_language",
                ],
            }
        )
    return {
        "schema_version": "semantic-judge.response.v7",
        "report_judgments": report_rows,
        "reason": "Complete provider-free fixture reading.",
        "basis": "Issue #195 fixture closure and artifact review.",
        "source_refs": ["artifact:natural_language"],
    }


def test_every_pydantic_model_and_field_has_english_description() -> None:
    non_ascii = re.compile(r"[^\x00-\x7f]")
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
        assert not non_ascii.search(inspect.getdoc(model) or ""), model.__name__
        for field_name, field in model.model_fields.items():
            assert field.description, f"{model.__name__}.{field_name}"
            assert not non_ascii.search(field.description or ""), (
                f"{model.__name__}.{field_name}"
            )


def test_judge_prompts_and_runtime_schema_use_english_audit_language() -> None:
    non_ascii = re.compile(r"[^\x00-\x7f]")
    for prompt in (SYSTEM_PROMPT, PRIMARY_INSTRUCTION, ARBITRATION_INSTRUCTION):
        assert not non_ascii.search(prompt)
        assert "English" in prompt
    schema_text = json.dumps(
        build_exact_response_model(minimal_input()).model_json_schema(),
        ensure_ascii=False,
        sort_keys=True,
    )
    assert not non_ascii.search(schema_text)


def test_runtime_schema_is_sparse_described_and_hides_derived_classes() -> None:
    schema = build_exact_response_model(
        minimal_input(report_count=2, expected_count=2)
    ).model_json_schema()
    serialized = json.dumps(schema, sort_keys=True)
    assert schema["description"]
    assert schema["properties"]["report_judgments"]["description"]
    assert "supported_relations" in serialized
    assert "no_match_expected_ids" in serialized
    assert "FULL_MATCH" in serialized and "PARTIAL_MATCH" in serialized
    assert "NO_MATCH" not in serialized
    assert "VALID_KNOWN" not in serialized
    assert "VALID_NOVEL" not in serialized
    assert '"VALID"' in serialized and '"INVALID"' in serialized
    assert "SUPPORTED" in serialized
    assert "MIXED" in serialized
    assert "REFUTED" in serialized
    assert "R0001" in serialized and "R0002" in serialized
    assert "E0001" in serialized and "E0002" in serialized
    assert "expected_judgments" not in schema["properties"]


@pytest.mark.parametrize(
    ("match", "validity", "allowed"),
    [
        (MatchStrength.FULL_MATCH, ReportValidity.VALID_KNOWN, True),
        (MatchStrength.FULL_MATCH, ReportValidity.VALID_NOVEL, False),
        (MatchStrength.FULL_MATCH, ReportValidity.INVALID, False),
        (MatchStrength.PARTIAL_MATCH, ReportValidity.VALID_KNOWN, True),
        (MatchStrength.PARTIAL_MATCH, ReportValidity.VALID_NOVEL, False),
        (MatchStrength.PARTIAL_MATCH, ReportValidity.INVALID, False),
        (MatchStrength.NO_MATCH, ReportValidity.VALID_KNOWN, True),
        (MatchStrength.NO_MATCH, ReportValidity.VALID_NOVEL, True),
        (MatchStrength.NO_MATCH, ReportValidity.INVALID, True),
    ],
)
def test_all_report_relation_validity_combinations(
    match: MatchStrength,
    validity: ReportValidity,
    allowed: bool,
) -> None:
    judge_input = minimal_input(report_count=1, expected_count=2)
    matches = (
        {("R0001", "E0001"): match}
        if match != MatchStrength.NO_MATCH
        else (
            {("R0001", "E0002"): MatchStrength.FULL_MATCH}
            if validity == ReportValidity.VALID_KNOWN
            else {}
        )
    )
    source_validity = {
        "R0001": (
            ReportValidity.INVALID
            if validity == ReportValidity.INVALID
            else ReportValidity.VALID_KNOWN
            if matches
            else ReportValidity.VALID_NOVEL
        )
    }
    provider_payload = reading_payload(
        judge_input, matches=matches, validity=source_validity
    )
    if validity == ReportValidity.INVALID and match != MatchStrength.NO_MATCH:
        with pytest.raises(
            ValidationError, match="core_truth=INVALID requires supported_relations"
        ):
            build_exact_response_model(judge_input).model_validate(provider_payload)
        return
    response = build_exact_response_model(judge_input).model_validate(provider_payload)
    assessment = materialize_reading(response, judge_input).report_assessments[0]
    payload = assessment.model_dump(mode="json")
    payload["validity"] = validity.value
    if match == MatchStrength.FULL_MATCH:
        payload["full_expected_ids"] = ["E0001"]
        payload["partial_expected_ids"] = []
        payload["no_match_expected_ids"] = ["E0002"]
    elif match == MatchStrength.PARTIAL_MATCH:
        payload["full_expected_ids"] = []
        payload["partial_expected_ids"] = ["E0001"]
        payload["no_match_expected_ids"] = ["E0002"]
    payload["core_truth"] = (
        CoreClaimTruth.INVALID.value
        if validity == ReportValidity.INVALID
        else CoreClaimTruth.VALID.value
    )
    if allowed:
        models.ReportAssessment.model_validate(payload)
    else:
        with pytest.raises(ValidationError):
            models.ReportAssessment.model_validate(payload)


def test_invalid_core_truth_rejects_full_and_partial_relations() -> None:
    judge_input = minimal_input()
    for match in (MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH):
        payload = reading_payload(
            judge_input,
            matches={("R0001", "E0001"): match},
            validity={"R0001": ReportValidity.INVALID},
        )
        with pytest.raises(
            ValidationError, match="core_truth=INVALID requires supported_relations"
        ):
            build_exact_response_model(judge_input).model_validate(payload)


def test_positive_and_no_sets_require_exact_exhaustive_closure() -> None:
    judge_input = minimal_input(report_count=1, expected_count=2)
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(judge_input)
    payload["report_judgments"][0]["no_match_expected_ids"].pop()
    with pytest.raises(ValidationError, match="must cover every expected ID exactly once"):
        schema.model_validate(payload)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    payload["report_judgments"][0]["no_match_expected_ids"].append("E0001")
    with pytest.raises(ValidationError, match="must cover every expected ID exactly once"):
        schema.model_validate(payload)


def test_empty_no_closure_requires_explicit_null_group_evidence() -> None:
    judge_input = minimal_input()
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    payload["report_judgments"][0]["no_match_reason"] = "No rows remain."
    with pytest.raises(ValidationError, match="must all be null"):
        build_exact_response_model(judge_input).model_validate(payload)


def test_positive_relation_requires_owned_fields_and_report_certificate() -> None:
    judge_input = minimal_input()
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    relation = payload["report_judgments"][0]["supported_relations"][0]
    relation["report_field_refs"] = ["claim", "where"]
    with pytest.raises(ValidationError, match="references null CandidateReport.where"):
        schema.model_validate(payload)
    payload = reading_payload(
        judge_input,
        matches={("R0001", "E0001"): MatchStrength.FULL_MATCH},
    )
    payload["report_judgments"][0]["supported_relations"][0][
        "causal_certificate_field"
    ] = "basis"
    with pytest.raises(ValidationError, match="must reference report certificate reason"):
        schema.model_validate(payload)


def test_causal_field_audit_requires_exact_complete_closure() -> None:
    judge_input = minimal_input()
    report = judge_input.reports[0].model_copy(
        update={"basis": "complete basis", "observed": "complete observation"}
    )
    judge_input = judge_input.model_copy(update={"reports": (report,)})
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(judge_input)
    payload["report_judgments"][0]["causal_field_audits"].pop()
    with pytest.raises(ValidationError, match="causal_field_audits exact closure failed"):
        schema.model_validate(payload)
    payload = reading_payload(judge_input)
    payload["report_judgments"][0]["causal_field_audits"][0]["exact_text"] = (
        "incomplete"
    )
    with pytest.raises(
        ValidationError, match="must equal the complete CandidateReport.reason value"
    ):
        schema.model_validate(payload)


def test_core_truth_requires_compatible_whole_field_certificate() -> None:
    judge_input = minimal_input()
    schema = build_exact_response_model(judge_input)
    payload = reading_payload(judge_input)
    payload["report_judgments"][0]["causal_field_audits"][0]["verdict"] = "MIXED"
    with pytest.raises(ValidationError, match="core_truth=VALID conflicts"):
        schema.model_validate(payload)
    payload = reading_payload(
        judge_input, validity={"R0001": ReportValidity.INVALID}
    )
    payload["report_judgments"][0]["causal_field_audits"][0]["verdict"] = (
        "SUPPORTED"
    )
    with pytest.raises(ValidationError, match="core_truth=INVALID conflicts"):
        schema.model_validate(payload)


def test_invalid_report_may_retain_supported_context_without_rescuing_claim() -> None:
    judge_input = minimal_input()
    report = judge_input.reports[0].model_copy(
        update={"basis": "The report cites the natural-language artifact."}
    )
    judge_input = judge_input.model_copy(update={"reports": (report,)})
    payload = reading_payload(
        judge_input, validity={"R0001": ReportValidity.INVALID}
    )
    audits = payload["report_judgments"][0]["causal_field_audits"]
    next(row for row in audits if row["report_field"] == "basis")["verdict"] = (
        "SUPPORTED"
    )
    validated = build_exact_response_model(judge_input).model_validate(payload)
    reading = materialize_reading(validated, judge_input)
    assert reading.report_assessments[0].validity == ReportValidity.INVALID
    assert all(row.match == MatchStrength.NO_MATCH for row in reading.relations)


def test_backend_materializes_dense_relations_ownership_hit_and_support() -> None:
    judge_input = minimal_input(report_count=3, expected_count=2)
    payload = reading_payload(
        judge_input,
        matches={
            ("R0001", "E0001"): MatchStrength.FULL_MATCH,
            ("R0002", "E0002"): MatchStrength.PARTIAL_MATCH,
        },
        validity={"R0003": ReportValidity.INVALID},
    )
    response = build_exact_response_model(judge_input).model_validate(payload)
    reading = materialize_reading(response, judge_input)
    assert len(reading.relations) == 6
    assert reading.report_assessments[0].validity == ReportValidity.VALID_KNOWN
    assert reading.report_assessments[1].validity == ReportValidity.VALID_KNOWN
    assert reading.report_assessments[2].validity == ReportValidity.INVALID
    assert "Backend ownership is VALID_KNOWN" in reading.report_assessments[0].reason
    assert "Backend ownership is INVALID" in reading.report_assessments[2].reason
    assert "expected:E0001" in reading.report_assessments[0].source_refs
    assert "expected:E0002" in reading.report_assessments[0].source_refs
    assert reading.expected_assessments[0].hit is True
    assert reading.expected_assessments[1].hit is False
    assert reading.expected_assessments[1].supported is True
    evidence = reading.relations[0].report_text_evidence
    assert any("sha256:" in row.basis for row in evidence)


def test_backend_canonicalizes_reversed_all_no_closure() -> None:
    judge_input = minimal_input(report_count=1, expected_count=3)
    payload = reading_payload(judge_input)
    payload["report_judgments"][0]["no_match_expected_ids"].reverse()

    response = build_exact_response_model(judge_input).model_validate(payload)
    reading = materialize_reading(response, judge_input)

    assert response.report_judgments[0].no_match_expected_ids == (
        "E0003",
        "E0002",
        "E0001",
    )
    assert reading.report_assessments[0].no_match_expected_ids == (
        "E0001",
        "E0002",
        "E0003",
    )


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


def test_sparse_0029_scale_shape_fits_output_budget_without_implicit_no_rows() -> None:
    judge_input = minimal_input(report_count=22, expected_count=8)
    payload = reading_payload(judge_input)
    validated = build_exact_response_model(judge_input).model_validate(payload)
    serialized = validated.model_dump_json()
    dense_relation_count = 22 * 8
    assert sum(len(row.supported_relations) for row in validated.report_judgments) == 0
    assert all(len(row.no_match_expected_ids) == 8 for row in validated.report_judgments)
    assert dense_relation_count == 176
    assert len(serialized) < 80_000
    assert (len(serialized) + 3) // 4 < 20_000


def test_typed_scale_audit_checks_exact_prompt_schema_and_sparse_envelopes() -> None:
    judge_input = minimal_input(report_count=22, expected_count=8)
    audit = build_scale_audit(
        judge_input,
        round_no=1,
        source_format="evidence_discovery_release",
        source_path="/audit/source/round-1.json",
        source_hash="sha256:" + "3" * 64,
        algorithm_source_hash="sha256:" + "5" * 64,
        model_profile="provider-free-profile",
        model_id="provider-free-model",
        profile_fingerprint="sha256:" + "4" * 64,
        context_window_tokens=272_000,
        profile_max_output_tokens=128_000,
    )

    assert audit.status == "pass"
    assert audit.report_count == 22
    assert audit.expected_count == 8
    assert audit.relation_position_count == 176
    assert audit.effective_max_output_tokens == 64_000
    assert audit.all_no_fits_output_limit
    assert audit.all_positive_fits_output_limit
    assert audit.reserved_context_fits_window
    assert audit.context_headroom_tokens > 0
    assert audit.all_positive_response_estimated_tokens > audit.all_no_response_estimated_tokens
    assert audit.response_schema_hash.startswith("sha256:")


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
