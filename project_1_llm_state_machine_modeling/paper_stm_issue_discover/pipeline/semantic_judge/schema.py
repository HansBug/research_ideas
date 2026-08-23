"""Sparse exact-closure provider schemas and deterministic dense materialization."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from typing import Annotated, Literal, cast

from pydantic import BaseModel, Field, model_validator

from .models import (
    ArbitrationResponse,
    CausalFieldAuditJudgment,
    CausalFieldVerdict,
    CoreClaimTruth,
    ExpectedAssessment,
    JudgeReading,
    JudgeResponse,
    MatchStrength,
    NoMatchRelationJudgment,
    PositiveMatchStrength,
    RelationAssessment,
    ReportAssessment,
    ReportCausalFieldAudit,
    ReportField,
    ReportJudgment,
    ReportTextEvidence,
    ReportTextEvidenceRole,
    ReportValidity,
    SupportedRelationJudgment,
    UnifiedJudgeInput,
    derive_causal_field_verdict,
)


def _literal(values: tuple[str, ...]):
    return Literal.__getitem__(values or ("__EMPTY_CLOSURE__",))


def _validate_report_judgment(
    *,
    row: ReportJudgment,
    report,
    expected_ids: tuple[str, ...],
    object_path: str,
) -> CoreClaimTruth:
    """Validate deterministic report-field, certificate, and relation invariants."""

    expected_causal_fields = {
        field_name: field_value
        for field_name in ("reason", "basis", "observed")
        if isinstance((field_value := getattr(report, field_name)), str)
    }
    actual_causal_fields = [item.report_field.value for item in row.causal_field_audits]
    if set(actual_causal_fields) != set(expected_causal_fields) or len(
        actual_causal_fields
    ) != len(set(actual_causal_fields)):
        raise ValueError(
            f"{object_path}.causal_field_audits exact closure failed; "
            f"expected={sorted(expected_causal_fields)}, actual={actual_causal_fields}"
        )
    audit_by_field: dict[str, CausalFieldAuditJudgment] = {}
    for audit in row.causal_field_audits:
        field_name = audit.report_field.value
        audit_by_field[field_name] = audit
    certificate_name = row.causal_certificate_field.value
    certificate = audit_by_field.get(certificate_name)
    if certificate is None:
        raise ValueError(
            f"{object_path}.causal_certificate_field={certificate_name} has no corresponding "
            "whole-field causal audit"
        )
    certificate_verdict = derive_causal_field_verdict(
        certificate.material_assertion_audits
    )
    core_truth = (
        CoreClaimTruth.VALID
        if certificate_verdict == CausalFieldVerdict.SUPPORTED
        else CoreClaimTruth.INVALID
    )

    positive_relations: list[SupportedRelationJudgment] = []
    no_match_ids: list[str] = []
    positive_ids: list[str] = []
    for index, decision in enumerate(row.relation_decisions):
        if decision.match == MatchStrength.NO_MATCH:
            no_match_ids.append(decision.expected_id)
            continue
        relation = cast(SupportedRelationJudgment, decision)
        field_names = [item.value for item in relation.report_field_refs]
        if len(field_names) != len(set(field_names)):
            raise ValueError(
                f"{object_path}.relation_decisions[{index}].report_field_refs contains "
                f"duplicates: {field_names}"
            )
        if ReportField.CLAIM not in relation.report_field_refs:
            raise ValueError(
                f"{object_path}.relation_decisions[{index}].report_field_refs must include claim"
            )
        for field_name in field_names:
            if not isinstance(getattr(report, field_name), str):
                raise ValueError(  # noqa: TRY004 - Pydantic reports this as response-schema validation
                    f"{object_path}.relation_decisions[{index}].report_field_refs references "
                    f"null CandidateReport.{field_name} for report {row.report_id}"
                )
        positive_relations.append(relation)
        positive_ids.append(relation.expected_id)
    if len(positive_ids) != len(set(positive_ids)):
        raise ValueError(
            f"{object_path}.relation_decisions contains duplicate positive expected IDs: "
            f"{positive_ids}"
        )
    if core_truth == CoreClaimTruth.INVALID and positive_relations:
        raise ValueError(
            f"{object_path} has a MIXED/REFUTED causal certificate and requires every "
            "relation_decision to be NO_MATCH; "
            f"actual_positive_expected_ids={positive_ids}"
        )

    if len(no_match_ids) != len(set(no_match_ids)):
        raise ValueError(
            f"{object_path}.relation_decisions contains duplicate NO expected IDs: {no_match_ids}"
        )
    if no_match_ids:
        if row.no_match_closure is None:
            raise ValueError(
                f"{object_path} has a non-empty NO_MATCH closure and requires non-null "
                "no_match_closure evidence"
            )
    elif row.no_match_closure is not None:
        raise ValueError(
            f"{object_path} has an empty NO_MATCH closure, so no_match_closure must be null"
        )
    actual_partition = positive_ids + no_match_ids
    if len(actual_partition) != len(set(actual_partition)) or set(actual_partition) != set(
        expected_ids
    ):
        raise ValueError(
            f"{object_path}.relation_decisions must cover every expected ID "
            f"exactly once; expected={expected_ids}, positive={positive_ids}, "
            f"no_match={no_match_ids}"
        )
    return core_truth


def _exact_relation_decision_type(*, expected_id: str, suffix: str):
    """Build one discriminator union fixed to one expected position."""

    expected_id_type = _literal((expected_id,))

    class ExactFullRelationJudgment(SupportedRelationJudgment):
        """One FULL relation fixed to an exact anonymous expected position."""

        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous expected ID fixed by this exact relation position."
        )
        match: Literal[PositiveMatchStrength.FULL_MATCH] = Field(
            description="Artifact-supported FULL_MATCH relation at this exact expected position."
        )

    class ExactPartialRelationJudgment(SupportedRelationJudgment):
        """One PARTIAL relation fixed to an exact anonymous expected position."""

        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous expected ID fixed by this exact relation position."
        )
        match: Literal[PositiveMatchStrength.PARTIAL_MATCH] = Field(
            description="Artifact-supported PARTIAL_MATCH relation at this exact expected position."
        )

    class ExactNoMatchRelationJudgment(NoMatchRelationJudgment):
        """One explicit NO relation fixed to an exact anonymous expected position."""

        expected_id: expected_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous expected ID fixed by this exact NO relation position."
        )

    ExactFullRelationJudgment.__name__ = f"ExactFullRelationJudgment_{suffix}"
    ExactPartialRelationJudgment.__name__ = f"ExactPartialRelationJudgment_{suffix}"
    ExactNoMatchRelationJudgment.__name__ = f"ExactNoMatchRelationJudgment_{suffix}"
    return Annotated[
        ExactFullRelationJudgment
        | ExactPartialRelationJudgment
        | ExactNoMatchRelationJudgment,
        Field(discriminator="match"),
    ]


def _exact_report_model(
    judge_input: UnifiedJudgeInput,
    *,
    allowed_report_ids: tuple[str, ...],
    suffix: str,
):
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    allowed_report_id_type = _literal(allowed_report_ids)
    reports_by_id = {item.report_id: item for item in judge_input.reports}
    relation_decision_types = tuple(
        _exact_relation_decision_type(
            expected_id=expected_id,
            suffix=f"{suffix}_{index}",
        )
        for index, expected_id in enumerate(expected_ids)
    )
    exact_relation_tuple = tuple.__class_getitem__(relation_decision_types)

    class ExactReportJudgment(ReportJudgment):
        """One validity-first sparse judgment restricted to exact closure IDs."""

        report_id: allowed_report_id_type = Field(  # type: ignore[valid-type]
            description="Anonymous report ID from the exact required closure; include each required report exactly once."
        )
        relation_decisions: exact_relation_tuple = Field(  # type: ignore[valid-type]
            description="One provider-native discriminated decision at each exact expected position, in input order; no expected ID can be omitted, duplicated, or moved."
        )

        @model_validator(mode="after")
        def exact_report_closure(self) -> ExactReportJudgment:
            _validate_report_judgment(
                row=self,
                report=reports_by_id[self.report_id],
                expected_ids=expected_ids,
                object_path=f"report_judgments[{self.report_id}]",
            )
            return self

    ExactReportJudgment.__name__ = f"ExactReportJudgment_{suffix}"
    return ExactReportJudgment


def build_exact_response_model(judge_input: UnifiedJudgeInput) -> type[JudgeResponse]:
    """Build a sparse-evidence provider schema over exact report/expected IDs."""

    report_ids = tuple(item.report_id for item in judge_input.reports)
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    suffix = hashlib.sha256(
        ("|".join(report_ids) + "::" + "|".join(expected_ids)).encode("utf-8")
    ).hexdigest()[:12]
    ExactReportJudgment = _exact_report_model(
        judge_input,
        allowed_report_ids=report_ids,
        suffix=suffix,
    )

    class ExactJudgeResponse(JudgeResponse):
        """Sparse validity-first semantics with exact exhaustive report closure."""

        report_judgments: tuple[ExactReportJudgment, ...] = Field(
            min_length=len(report_ids),
            max_length=len(report_ids),
            description="One core-truth, causal-certificate, and sparse exhaustive relation judgment for every anonymous report exactly once."
        )

        @model_validator(mode="after")
        def exact_report_identity(self) -> ExactJudgeResponse:
            actual = [row.report_id for row in self.report_judgments]
            if set(actual) != set(report_ids) or len(actual) != len(set(actual)):
                raise ValueError(
                    "report_judgments must contain every input report exactly once; "
                    f"expected={report_ids}, actual={actual}"
                )
            return self

    ExactJudgeResponse.__name__ = f"ExactJudgeResponse_{suffix}"
    return cast(type[JudgeResponse], ExactJudgeResponse)


def build_exact_arbitration_model(
    judge_input: UnifiedJudgeInput,
    conflicted_report_ids: tuple[str, ...],
) -> type[ArbitrationResponse]:
    """Build a conflict-only replacement schema over exact report identities."""

    if not conflicted_report_ids or len(conflicted_report_ids) != len(
        set(conflicted_report_ids)
    ):
        raise ValueError(
            f"conflicted_report_ids must be non-empty and unique: {conflicted_report_ids}"
        )
    known_report_ids = {item.report_id for item in judge_input.reports}
    if not set(conflicted_report_ids) <= known_report_ids:
        raise ValueError(
            "conflicted_report_ids contains values outside the input closure: "
            f"{sorted(set(conflicted_report_ids) - known_report_ids)}"
        )
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    suffix = hashlib.sha256(
        (
            "|".join(conflicted_report_ids)
            + "::"
            + "|".join(expected_ids)
            + "::arbitration"
        ).encode("utf-8")
    ).hexdigest()[:12]
    ExactReportJudgment = _exact_report_model(
        judge_input,
        allowed_report_ids=conflicted_report_ids,
        suffix=suffix,
    )

    class ExactArbitrationResponse(ArbitrationResponse):
        """Targeted replacements for every conflicted report and no other report."""

        report_judgments: tuple[ExactReportJudgment, ...] = Field(
            min_length=len(conflicted_report_ids),
            max_length=len(conflicted_report_ids),
            description="One complete sparse replacement for every conflicted report exactly once; unchanged reports are omitted."
        )

        @model_validator(mode="after")
        def exact_conflict_identity(self) -> ExactArbitrationResponse:
            actual = [row.report_id for row in self.report_judgments]
            if set(actual) != set(conflicted_report_ids) or len(actual) != len(set(actual)):
                raise ValueError(
                    "arbitration report_judgments must replace every conflicted report "
                    f"exactly once; expected={conflicted_report_ids}, actual={actual}"
                )
            return self

    ExactArbitrationResponse.__name__ = f"ExactArbitrationResponse_{suffix}"
    return cast(type[ArbitrationResponse], ExactArbitrationResponse)


def merge_arbitration_response(
    primary_response: JudgeResponse,
    arbitration_response: ArbitrationResponse,
    response_model: type[JudgeResponse],
) -> JudgeResponse:
    """Replace conflicted reports and revalidate the complete sparse closure."""

    replacements = {
        row.report_id: row for row in arbitration_response.report_judgments
    }
    merged = [
        replacements.get(row.report_id, row) for row in primary_response.report_judgments
    ]
    payload = primary_response.model_dump(mode="json")
    payload["report_judgments"] = [row.model_dump(mode="json") for row in merged]
    payload["reason"] = arbitration_response.reason
    payload["basis"] = arbitration_response.basis
    payload["source_refs"] = list(arbitration_response.source_refs)
    return response_model.model_validate(payload)


def _materialized_text_evidence(
    *,
    report,
    report_field: ReportField,
    semantic_role: ReportTextEvidenceRole,
    reason: str,
    basis: str,
) -> ReportTextEvidence:
    field_value = getattr(report, report_field.value)
    if not isinstance(field_value, str):
        raise ValueError(  # noqa: TRY004 - impossible value is a persisted closure-validation failure
            f"cannot materialize null CandidateReport.{report_field.value} for {report.report_id}"
        )
    return ReportTextEvidence(
        report_field=report_field,
        exact_quote=field_value,
        semantic_role=semantic_role,
        reason=reason,
        basis=(
            f"{basis}; CandidateReport {report.report_id}.{report_field.value}; "
            "sha256:"
            + hashlib.sha256(field_value.encode("utf-8")).hexdigest()
        ),
    )


def _unique(values: Iterable[str]) -> tuple[str, ...]:
    return tuple(dict.fromkeys(values))


def _materialized_causal_field_audit(
    *, report, judgment: CausalFieldAuditJudgment
) -> ReportCausalFieldAudit:
    """Attach source text, digest, and a derived verdict to one assertion audit."""

    field_value = getattr(report, judgment.report_field.value)
    if not isinstance(field_value, str):
        raise ValueError(  # noqa: TRY004 - validated closure makes this unreachable
            f"cannot materialize null CandidateReport.{judgment.report_field.value} "
            f"for {report.report_id}"
        )
    return ReportCausalFieldAudit(
        report_field=judgment.report_field,
        exact_text=field_value,
        exact_text_sha256="sha256:"
        + hashlib.sha256(field_value.encode("utf-8")).hexdigest(),
        material_assertion_audits=judgment.material_assertion_audits,
        verdict=derive_causal_field_verdict(judgment.material_assertion_audits),
        reason=" ".join(
            f"{item.assertion_id}={item.verdict.value}: {item.reason}"
            for item in judgment.material_assertion_audits
        ),
        basis=" ".join(
            f"{item.assertion_id}: {item.basis}"
            for item in judgment.material_assertion_audits
        ),
        source_refs=_unique(
            ref
            for item in judgment.material_assertion_audits
            for ref in item.source_refs
        ),
    )


def materialize_reading(
    response: JudgeResponse,
    judge_input: UnifiedJudgeInput,
) -> JudgeReading:
    """Derive ownership, dense NO rows, expected coverage, and exact text audit."""

    report_ids = tuple(item.report_id for item in judge_input.reports)
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    reports_by_id = {item.report_id: item for item in judge_input.reports}
    judgments_by_id = {row.report_id: row for row in response.report_judgments}
    if set(judgments_by_id) != set(report_ids) or len(judgments_by_id) != len(
        response.report_judgments
    ):
        raise ValueError("materialize_reading requires exact validated report closure")

    relations: list[RelationAssessment] = []
    report_assessments: list[ReportAssessment] = []
    for report_id in report_ids:
        judgment = judgments_by_id[report_id]
        report = reports_by_id[report_id]
        causal_judgments_by_field = {
            audit.report_field.value: audit for audit in judgment.causal_field_audits
        }
        certificate_judgment = causal_judgments_by_field[
            judgment.causal_certificate_field.value
        ]
        certificate_verdict = derive_causal_field_verdict(
            certificate_judgment.material_assertion_audits
        )
        core_truth = (
            CoreClaimTruth.VALID
            if certificate_verdict == CausalFieldVerdict.SUPPORTED
            else CoreClaimTruth.INVALID
        )
        positive_by_expected = {
            row.expected_id: cast(SupportedRelationJudgment, row)
            for row in judgment.relation_decisions
            if row.match != MatchStrength.NO_MATCH
        }
        full_expected_ids: list[str] = []
        partial_expected_ids: list[str] = []
        for expected_id in expected_ids:
            positive = positive_by_expected.get(expected_id)
            if positive is None:
                relation = RelationAssessment(
                    report_id=report_id,
                    expected_id=expected_id,
                    match=MatchStrength.NO_MATCH,
                    report_text_evidence=(
                        _materialized_text_evidence(
                            report=report,
                            report_field=ReportField.CLAIM,
                            semantic_role=ReportTextEvidenceRole.CLAIM_BOUNDARY,
                            reason="The complete published claim defines the report boundary for this explicit NO relation.",
                            basis=f"report_judgments[{report_id}].relation_decisions",
                        ),
                    ),
                    reason=cast(str, judgment.no_match_closure.reason),
                    basis=cast(str, judgment.no_match_closure.basis),
                    source_refs=cast(
                        tuple[str, ...], judgment.no_match_closure.source_refs
                    ),
                )
            else:
                match = MatchStrength(positive.match.value)
                if match == MatchStrength.FULL_MATCH:
                    full_expected_ids.append(expected_id)
                else:
                    partial_expected_ids.append(expected_id)
                evidence = tuple(
                    _materialized_text_evidence(
                        report=report,
                        report_field=field_ref,
                        semantic_role=(
                            ReportTextEvidenceRole.CAUSAL_SUPPORT
                            if field_ref.value == judgment.causal_certificate_field.value
                            else ReportTextEvidenceRole.CLAIM_BOUNDARY
                        ),
                        reason=(
                            "The complete supported causal certificate establishes the report-owned premise used by this relation."
                            if field_ref.value == judgment.causal_certificate_field.value
                            else "The complete referenced report field delimits the published technical claim used by this relation."
                        ),
                        basis=f"supported_relation:{report_id}/{expected_id}",
                    )
                    for field_ref in positive.report_field_refs
                )
                if not any(
                    item.semantic_role == ReportTextEvidenceRole.CAUSAL_SUPPORT
                    for item in evidence
                ):
                    certificate_field = ReportField(
                        judgment.causal_certificate_field.value
                    )
                    evidence += (
                        _materialized_text_evidence(
                            report=report,
                            report_field=certificate_field,
                            semantic_role=ReportTextEvidenceRole.CAUSAL_SUPPORT,
                            reason="The complete supported causal certificate establishes the report-owned premise used by this relation.",
                            basis=f"supported_relation:{report_id}/{expected_id}",
                        ),
                    )
                relation = RelationAssessment(
                    report_id=report_id,
                    expected_id=expected_id,
                    match=match,
                    report_text_evidence=evidence,
                    reason=positive.reason,
                    basis=positive.basis,
                    source_refs=positive.source_refs,
                )
            relations.append(relation)

        validity = (
            ReportValidity.INVALID
            if core_truth == CoreClaimTruth.INVALID
            else ReportValidity.VALID_KNOWN
            if full_expected_ids or partial_expected_ids
            else ReportValidity.VALID_NOVEL
        )
        if validity == ReportValidity.VALID_KNOWN:
            ownership_reason = (
                "Backend ownership is VALID_KNOWN because core_truth is VALID and "
                "the exhaustive relation closure contains positive expected IDs "
                f"{full_expected_ids + partial_expected_ids}."
            )
        elif validity == ReportValidity.VALID_NOVEL:
            ownership_reason = (
                "Backend ownership is VALID_NOVEL because core_truth is VALID and "
                "every expected relation is explicitly NO_MATCH."
            )
        else:
            ownership_reason = (
                "Backend ownership is INVALID because core_truth is INVALID and "
                "every expected relation is explicitly NO_MATCH."
            )
        certificate_role = (
            ReportTextEvidenceRole.CAUSAL_SUPPORT
            if core_truth == CoreClaimTruth.VALID
            else ReportTextEvidenceRole.REFUTED_PREMISE
        )
        certificate_audit = _materialized_causal_field_audit(
            report=report,
            judgment=certificate_judgment,
        )
        report_assessments.append(
            ReportAssessment(
                report_id=report_id,
                core_truth=core_truth,
                validity=validity,
                full_expected_ids=tuple(full_expected_ids),
                partial_expected_ids=tuple(partial_expected_ids),
                no_match_expected_ids=tuple(
                    expected_id
                    for expected_id in expected_ids
                    if expected_id not in positive_by_expected
                ),
                root_cause_cluster_key=judgment.root_cause_cluster_key,
                report_text_evidence=(
                    _materialized_text_evidence(
                        report=report,
                        report_field=ReportField.CLAIM,
                        semantic_role=ReportTextEvidenceRole.CLAIM_BOUNDARY,
                        reason="The complete published claim defines the report-level validity boundary.",
                        basis=f"report_judgments[{report_id}]",
                    ),
                    _materialized_text_evidence(
                        report=report,
                        report_field=ReportField(
                            judgment.causal_certificate_field.value
                        ),
                        semantic_role=certificate_role,
                        reason=(
                            "The complete field supplies the artifact-compatible causal certificate for the valid core claim."
                            if core_truth == CoreClaimTruth.VALID
                            else "The complete field contains the mixed or refuted premise that invalidates the core claim."
                        ),
                        basis=f"report_judgments[{report_id}].causal_certificate_field",
                    ),
                ),
                causal_field_audits=tuple(
                    _materialized_causal_field_audit(
                        report=report,
                        judgment=causal_judgments_by_field[field_name],
                    )
                    for field_name in ("reason", "basis", "observed")
                    if isinstance(getattr(report, field_name), str)
                ),
                reason=f"{certificate_audit.reason} {ownership_reason}",
                basis=(
                    f"{certificate_audit.basis}; deterministic ownership derivation from "
                    "core_truth and the exact positive/NO expected-ID partition"
                ),
                source_refs=_unique(
                    [f"report:{report_id}"]
                    + list(certificate_audit.source_refs)
                    + [f"expected:{expected_id}" for expected_id in expected_ids]
                ),
            )
        )

    relation_by_key = {
        (row.report_id, row.expected_id): row for row in relations
    }
    expected_assessments: list[ExpectedAssessment] = []
    for expected_id in expected_ids:
        full_report_ids = tuple(
            report_id
            for report_id in report_ids
            if relation_by_key[(report_id, expected_id)].match
            == MatchStrength.FULL_MATCH
        )
        partial_report_ids = tuple(
            report_id
            for report_id in report_ids
            if relation_by_key[(report_id, expected_id)].match
            == MatchStrength.PARTIAL_MATCH
        )
        supported_report_ids = set(full_report_ids) | set(partial_report_ids)
        relation_rows = tuple(
            relation_by_key[(report_id, expected_id)] for report_id in report_ids
        )
        expected_assessments.append(
            ExpectedAssessment(
                expected_id=expected_id,
                full_report_ids=full_report_ids,
                partial_report_ids=partial_report_ids,
                no_support_report_ids=tuple(
                    report_id
                    for report_id in report_ids
                    if report_id not in supported_report_ids
                ),
                hit=bool(full_report_ids),
                supported=bool(supported_report_ids),
                reason=(
                    f"Expected issue {expected_id} has FULL support from {list(full_report_ids)} "
                    f"and PARTIAL support from {list(partial_report_ids)}; all remaining reports are NO_MATCH."
                ),
                basis="Deterministic materialization of every validated positional relation decision and grouped NO evidence for this expected issue.",
                source_refs=_unique(
                    [f"expected:{expected_id}"]
                    + [ref for row in relation_rows for ref in row.source_refs]
                ),
            )
        )
    return JudgeReading(
        relations=tuple(relations),
        report_assessments=tuple(report_assessments),
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
