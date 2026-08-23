"""Dynamic exact-closure Pydantic response schema for one Judge pair."""

from __future__ import annotations

import hashlib
import json
from typing import Literal, cast

from pydantic import Field, model_validator

from .models import (
    ExpectedAssessment,
    JudgeReading,
    RelationAssessment,
    ReportAssessment,
    ReportValidity,
    UnifiedJudgeInput,
)


def _literal(values: tuple[str, ...]):
    return Literal.__getitem__(values or ("__EMPTY_CLOSURE__",))


def build_exact_reading_model(judge_input: UnifiedJudgeInput) -> type[JudgeReading]:
    """Build a provider schema that names only IDs in this exact pair closure."""

    report_ids = tuple(item.report_id for item in judge_input.reports)
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    report_id_type = _literal(report_ids)
    expected_id_type = _literal(expected_ids)
    relation_count = len(report_ids) * len(expected_ids)

    class ExactRelationAssessment(RelationAssessment):
        """One exact report/expected row whose IDs are closed by this pair input."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="输入 exact closure 中的匿名 report ID；不得新建、改写或遗漏。"
        )
        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="输入 exact closure 中的匿名 expected ID；不得新建、改写或遗漏。"
        )

    class ExactReportAssessment(ReportAssessment):
        """One exact report validity row closed over every expected ID."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="输入 exact closure 中的匿名 report ID；每条 exactly once。"
        )
        full_expected_ids: tuple[expected_id_type, ...] = Field(  # type: ignore[valid-type]
            description="该报告 FULL_MATCH 的全部 expected IDs；允许为空。"
        )
        partial_expected_ids: tuple[expected_id_type, ...] = Field(  # type: ignore[valid-type]
            description="该报告 PARTIAL_MATCH 的全部 expected IDs；允许为空。"
        )
        no_match_expected_ids: tuple[expected_id_type, ...] = Field(  # type: ignore[valid-type]
            description="该报告 NO_MATCH 的全部 expected IDs；三组精确分割 closure。"
        )

    class ExactExpectedAssessment(ExpectedAssessment):
        """One exact expected coverage row closed over every report ID."""

        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="输入 exact closure 中的匿名 expected ID；每条 exactly once。"
        )
        full_report_ids: tuple[report_id_type, ...] = Field(  # type: ignore[valid-type]
            description="VALID_KNOWN + FULL_MATCH 的全部 report IDs；允许为空。"
        )
        partial_report_ids: tuple[report_id_type, ...] = Field(  # type: ignore[valid-type]
            description="VALID_KNOWN + PARTIAL_MATCH 的全部 report IDs；允许为空。"
        )
        no_support_report_ids: tuple[report_id_type, ...] = Field(  # type: ignore[valid-type]
            description="其余全部 report IDs；三组精确分割 closure。"
        )

    class ExactJudgeReading(JudgeReading):
        """Full #195 reading with deterministic ID closure and derived consistency."""

        relations: tuple[ExactRelationAssessment, ...] = Field(
            min_length=relation_count,
            max_length=relation_count,
            description="完整 report x expected 关系矩阵；包含全部 NO_MATCH，数量固定。",
        )
        report_assessments: tuple[ExactReportAssessment, ...] = Field(
            min_length=len(report_ids),
            max_length=len(report_ids),
            description="每条匿名 report exactly once；空报告集时为空。",
        )
        expected_assessments: tuple[ExactExpectedAssessment, ...] = Field(
            min_length=len(expected_ids),
            max_length=len(expected_ids),
            description="每条匿名 expected exactly once。",
        )

        @model_validator(mode="after")
        def exact_closure_and_derived_consistency(self) -> ExactJudgeReading:
            expected_relation_keys = {
                (report_id, expected_id)
                for report_id in report_ids
                for expected_id in expected_ids
            }
            actual_relation_keys = [
                (row.report_id, row.expected_id) for row in self.relations
            ]
            if set(actual_relation_keys) != expected_relation_keys or len(actual_relation_keys) != len(set(actual_relation_keys)):
                missing = sorted(expected_relation_keys - set(actual_relation_keys))
                extra = sorted(set(actual_relation_keys) - expected_relation_keys)
                raise ValueError(
                    "relations exact closure failed; "
                    f"missing={missing}, extra={extra}, duplicate_count={len(actual_relation_keys)-len(set(actual_relation_keys))}"
                )
            report_rows = [row.report_id for row in self.report_assessments]
            if set(report_rows) != set(report_ids) or len(report_rows) != len(set(report_rows)):
                raise ValueError(
                    "report_assessments must contain each input report exactly once; "
                    f"expected={report_ids}, actual={report_rows}"
                )
            expected_rows = [row.expected_id for row in self.expected_assessments]
            if set(expected_rows) != set(expected_ids) or len(expected_rows) != len(set(expected_rows)):
                raise ValueError(
                    "expected_assessments must contain each input expected exactly once; "
                    f"expected={expected_ids}, actual={expected_rows}"
                )
            relation_by_key = {
                (row.report_id, row.expected_id): row.match for row in self.relations
            }
            report_by_id = {row.report_id: row for row in self.report_assessments}
            for report_id, row in report_by_id.items():
                derived_full = {
                    expected_id
                    for expected_id in expected_ids
                    if relation_by_key[(report_id, expected_id)].value == "FULL_MATCH"
                }
                derived_partial = {
                    expected_id
                    for expected_id in expected_ids
                    if relation_by_key[(report_id, expected_id)].value == "PARTIAL_MATCH"
                }
                derived_none = set(expected_ids) - derived_full - derived_partial
                actual_groups = (
                    set(row.full_expected_ids),
                    set(row.partial_expected_ids),
                    set(row.no_match_expected_ids),
                )
                if actual_groups != (derived_full, derived_partial, derived_none):
                    raise ValueError(
                        f"report_assessments[{report_id}] relation groups conflict with matrix; "
                        f"expected_full={sorted(derived_full)}, actual_full={sorted(actual_groups[0])}, "
                        f"expected_partial={sorted(derived_partial)}, actual_partial={sorted(actual_groups[1])}, "
                        f"expected_none={sorted(derived_none)}, actual_none={sorted(actual_groups[2])}"
                    )
                if row.validity == ReportValidity.VALID_KNOWN and not (derived_full or derived_partial):
                    raise ValueError(
                        f"report_assessments[{report_id}].validity=VALID_KNOWN requires at least one FULL/PARTIAL relation"
                    )
                if row.validity == ReportValidity.VALID_NOVEL and (derived_full or derived_partial):
                    raise ValueError(
                        f"report_assessments[{report_id}].validity=VALID_NOVEL requires all relations NO_MATCH"
                    )
            for expected_row in self.expected_assessments:
                expected_id = expected_row.expected_id
                derived_full_reports = {
                    report_id
                    for report_id in report_ids
                    if report_by_id[report_id].validity == ReportValidity.VALID_KNOWN
                    and relation_by_key[(report_id, expected_id)].value == "FULL_MATCH"
                }
                derived_partial_reports = {
                    report_id
                    for report_id in report_ids
                    if report_by_id[report_id].validity == ReportValidity.VALID_KNOWN
                    and relation_by_key[(report_id, expected_id)].value == "PARTIAL_MATCH"
                }
                derived_no_support = set(report_ids) - derived_full_reports - derived_partial_reports
                if (
                    set(expected_row.full_report_ids) != derived_full_reports
                    or set(expected_row.partial_report_ids) != derived_partial_reports
                    or set(expected_row.no_support_report_ids) != derived_no_support
                    or expected_row.hit != bool(derived_full_reports)
                    or expected_row.supported != bool(derived_full_reports or derived_partial_reports)
                ):
                    raise ValueError(
                        f"expected_assessments[{expected_id}] conflicts with relation/validity matrix; "
                        f"full={sorted(derived_full_reports)}, partial={sorted(derived_partial_reports)}, "
                        f"no_support={sorted(derived_no_support)}"
                    )
            return self

    suffix = hashlib.sha256(
        ("|".join(report_ids) + "::" + "|".join(expected_ids)).encode("utf-8")
    ).hexdigest()[:12]
    ExactRelationAssessment.__name__ = f"ExactRelationAssessment_{suffix}"
    ExactReportAssessment.__name__ = f"ExactReportAssessment_{suffix}"
    ExactExpectedAssessment.__name__ = f"ExactExpectedAssessment_{suffix}"
    ExactJudgeReading.__name__ = f"ExactJudgeReading_{suffix}"
    return cast(type[JudgeReading], ExactJudgeReading)


def reading_schema_hash(schema: type[JudgeReading]) -> str:
    """Hash the actual provider structured-output schema, including descriptions."""

    payload = json.dumps(
        schema.model_json_schema(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return "sha256:" + hashlib.sha256(payload.encode("utf-8")).hexdigest()
