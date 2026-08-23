"""Exact-closure provider schema and deterministic Judge reading materialization."""

from __future__ import annotations

import hashlib
import json
from typing import Literal, cast

from pydantic import BaseModel, Field, model_validator

from .models import (
    ExpectedAssessment,
    ExpectedJudgment,
    JudgeReading,
    JudgeResponse,
    MatchStrength,
    RelationAssessment,
    ReportAssessment,
    ReportJudgment,
    ReportTextEvidenceRole,
    ReportValidity,
    UnifiedJudgeInput,
)


def _literal(values: tuple[str, ...]):
    return Literal.__getitem__(values or ("__EMPTY_CLOSURE__",))


def build_exact_response_model(judge_input: UnifiedJudgeInput) -> type[JudgeResponse]:
    """Build the provider schema over the exact anonymous IDs in one pair input."""

    report_ids = tuple(item.report_id for item in judge_input.reports)
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    report_id_type = _literal(report_ids)
    expected_id_type = _literal(expected_ids)
    relation_count = len(report_ids) * len(expected_ids)
    reports_by_id = {item.report_id: item for item in judge_input.reports}

    class ExactRelationAssessment(RelationAssessment):
        """One exact report/expected relation whose IDs are closed by this input."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous report ID from the exact input closure; do not create, rewrite, or omit an ID."
        )
        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous expected ID from the exact input closure; do not create, rewrite, or omit an ID."
        )

    class ExactReportJudgment(ReportJudgment):
        """One exact report validity/cluster judgment without derived relation sets."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous report ID from the exact input closure; include every ID exactly once."
        )

    class ExactExpectedJudgment(ExpectedJudgment):
        """One exact expected explanation without backend-derived coverage fields."""

        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous expected ID from the exact input closure; include every ID exactly once."
        )

    class ExactJudgeResponse(JudgeResponse):
        """Provider-authored #195 semantics with exact closure and no duplicated sums."""

        relations: tuple[ExactRelationAssessment, ...] = Field(
            min_length=relation_count,
            max_length=relation_count,
            description="Complete report-by-expected relation matrix with every NO_MATCH row and the exact fixed size.",
        )
        report_judgments: tuple[ExactReportJudgment, ...] = Field(
            min_length=len(report_ids),
            max_length=len(report_ids),
            description="Validity, root-cause cluster, and evidence for every anonymous report exactly once; do not repeat relation-derived ID sets.",
        )
        expected_judgments: tuple[ExactExpectedJudgment, ...] = Field(
            min_length=len(expected_ids),
            max_length=len(expected_ids),
            description="Semantic explanation for every anonymous expected issue exactly once; the backend derives hit and support.",
        )

        @model_validator(mode="after")
        def exact_closure_and_validity_consistency(self) -> ExactJudgeResponse:
            expected_relation_keys = {
                (report_id, expected_id)
                for report_id in report_ids
                for expected_id in expected_ids
            }
            actual_relation_keys = [
                (row.report_id, row.expected_id) for row in self.relations
            ]
            actual_relation_key_set = set(actual_relation_keys)
            if actual_relation_key_set != expected_relation_keys or len(
                actual_relation_keys
            ) != len(actual_relation_key_set):
                missing = sorted(expected_relation_keys - actual_relation_key_set)
                extra = sorted(actual_relation_key_set - expected_relation_keys)
                raise ValueError(
                    "relations exact closure failed; "
                    f"missing={missing}, extra={extra}, "
                    f"duplicate_count={len(actual_relation_keys) - len(actual_relation_key_set)}"
                )
            report_rows = [row.report_id for row in self.report_judgments]
            if set(report_rows) != set(report_ids) or len(report_rows) != len(
                set(report_rows)
            ):
                raise ValueError(
                    "report_judgments must contain each input report exactly once; "
                    f"expected={report_ids}, actual={report_rows}"
                )
            expected_rows = [row.expected_id for row in self.expected_judgments]
            if set(expected_rows) != set(expected_ids) or len(expected_rows) != len(
                set(expected_rows)
            ):
                raise ValueError(
                    "expected_judgments must contain each input expected exactly once; "
                    f"expected={expected_ids}, actual={expected_rows}"
                )
            relation_by_key = {
                (row.report_id, row.expected_id): row.match for row in self.relations
            }
            evidence_rows = [
                (f"relations[{row.report_id},{row.expected_id}]", row.report_id, row.report_text_evidence)
                for row in self.relations
            ] + [
                (f"report_judgments[{row.report_id}]", row.report_id, row.report_text_evidence)
                for row in self.report_judgments
            ]
            for object_path, report_id, evidence in evidence_rows:
                report = reports_by_id[report_id]
                for index, item in enumerate(evidence):
                    field_value = getattr(report, item.report_field.value)
                    if not isinstance(field_value, str):
                        raise ValueError(  # noqa: TRY004 - Pydantic must wrap provider validation failures
                            f"{object_path}.report_text_evidence[{index}] references null "
                            f"CandidateReport.{item.report_field.value} for report {report_id}"
                        )
                    if item.exact_quote not in field_value:
                        raise ValueError(
                            f"{object_path}.report_text_evidence[{index}].exact_quote is not "
                            f"a case-sensitive substring of report {report_id} field "
                            f"{item.report_field.value}; actual_quote={item.exact_quote!r}"
                        )
            for row in self.relations:
                roles = {item.semantic_role for item in row.report_text_evidence}
                if ReportTextEvidenceRole.CLAIM_BOUNDARY not in roles:
                    raise ValueError(
                        f"relations[{row.report_id},{row.expected_id}].report_text_evidence "
                        "requires CLAIM_BOUNDARY"
                    )
                if row.match in {
                    MatchStrength.FULL_MATCH,
                    MatchStrength.PARTIAL_MATCH,
                } and ReportTextEvidenceRole.CAUSAL_SUPPORT not in roles:
                    raise ValueError(
                        f"relations[{row.report_id},{row.expected_id}].report_text_evidence "
                        f"requires CAUSAL_SUPPORT for {row.match.value}"
                    )
            for row in self.report_judgments:
                roles = {item.semantic_role for item in row.report_text_evidence}
                if ReportTextEvidenceRole.CLAIM_BOUNDARY not in roles:
                    raise ValueError(
                        f"report_judgments[{row.report_id}].report_text_evidence requires "
                        "CLAIM_BOUNDARY"
                    )
                required_role = (
                    ReportTextEvidenceRole.REFUTED_PREMISE
                    if row.validity == ReportValidity.INVALID
                    else ReportTextEvidenceRole.CAUSAL_SUPPORT
                )
                if required_role not in roles:
                    raise ValueError(
                        f"report_judgments[{row.report_id}].report_text_evidence requires "
                        f"{required_role.value} for {row.validity.value}"
                    )
                has_known_relation = any(
                    relation_by_key[(row.report_id, expected_id)]
                    in {MatchStrength.FULL_MATCH, MatchStrength.PARTIAL_MATCH}
                    for expected_id in expected_ids
                )
                if (
                    row.validity == ReportValidity.VALID_KNOWN
                    and not has_known_relation
                ):
                    raise ValueError(
                        f"report_judgments[{row.report_id}].validity=VALID_KNOWN "
                        "requires at least one FULL_MATCH or PARTIAL_MATCH relation"
                    )
                if row.validity == ReportValidity.VALID_NOVEL and has_known_relation:
                    raise ValueError(
                        f"report_judgments[{row.report_id}].validity=VALID_NOVEL "
                        "requires all relations NO_MATCH"
                    )
            return self

    suffix = hashlib.sha256(
        ("|".join(report_ids) + "::" + "|".join(expected_ids)).encode("utf-8")
    ).hexdigest()[:12]
    ExactRelationAssessment.__name__ = f"ExactRelationAssessment_{suffix}"
    ExactReportJudgment.__name__ = f"ExactReportJudgment_{suffix}"
    ExactExpectedJudgment.__name__ = f"ExactExpectedJudgment_{suffix}"
    ExactJudgeResponse.__name__ = f"ExactJudgeResponse_{suffix}"
    return cast(type[JudgeResponse], ExactJudgeResponse)


def materialize_reading(response: JudgeResponse) -> JudgeReading:
    """Derive every score-bearing set from validated semantic rows exactly once."""

    report_ids = tuple(row.report_id for row in response.report_judgments)
    expected_ids = tuple(row.expected_id for row in response.expected_judgments)
    relation_by_key = {
        (row.report_id, row.expected_id): row for row in response.relations
    }
    report_judgment_by_id = {row.report_id: row for row in response.report_judgments}

    report_assessments = tuple(
        ReportAssessment(
            report_id=judgment.report_id,
            validity=judgment.validity,
            full_expected_ids=tuple(
                expected_id
                for expected_id in expected_ids
                if relation_by_key[(judgment.report_id, expected_id)].match
                == MatchStrength.FULL_MATCH
            ),
            partial_expected_ids=tuple(
                expected_id
                for expected_id in expected_ids
                if relation_by_key[(judgment.report_id, expected_id)].match
                == MatchStrength.PARTIAL_MATCH
            ),
            no_match_expected_ids=tuple(
                expected_id
                for expected_id in expected_ids
                if relation_by_key[(judgment.report_id, expected_id)].match
                == MatchStrength.NO_MATCH
            ),
            root_cause_cluster_key=judgment.root_cause_cluster_key,
            report_text_evidence=judgment.report_text_evidence,
            reason=judgment.reason,
            basis=judgment.basis,
            source_refs=judgment.source_refs,
        )
        for judgment in response.report_judgments
    )
    expected_assessments = []
    for judgment in response.expected_judgments:
        full_report_ids = tuple(
            report_id
            for report_id in report_ids
            if report_judgment_by_id[report_id].validity == ReportValidity.VALID_KNOWN
            and relation_by_key[(report_id, judgment.expected_id)].match
            == MatchStrength.FULL_MATCH
        )
        partial_report_ids = tuple(
            report_id
            for report_id in report_ids
            if report_judgment_by_id[report_id].validity == ReportValidity.VALID_KNOWN
            and relation_by_key[(report_id, judgment.expected_id)].match
            == MatchStrength.PARTIAL_MATCH
        )
        supported_report_ids = set(full_report_ids) | set(partial_report_ids)
        expected_assessments.append(
            ExpectedAssessment(
                expected_id=judgment.expected_id,
                full_report_ids=full_report_ids,
                partial_report_ids=partial_report_ids,
                no_support_report_ids=tuple(
                    report_id
                    for report_id in report_ids
                    if report_id not in supported_report_ids
                ),
                hit=bool(full_report_ids),
                supported=bool(supported_report_ids),
                reason=judgment.reason,
                basis=judgment.basis,
                source_refs=judgment.source_refs,
            )
        )
    return JudgeReading(
        relations=response.relations,
        report_assessments=report_assessments,
        expected_assessments=tuple(expected_assessments),
        reason=response.reason,
        basis=response.basis,
        source_refs=response.source_refs,
    )


def response_schema_hash(schema: type[BaseModel]) -> str:
    """Hash the actual provider structured-output schema, including descriptions."""

    payload = json.dumps(
        schema.model_json_schema(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
