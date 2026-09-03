"""Sparse exact-closure provider schemas and deterministic dense materialization."""

from __future__ import annotations

import hashlib
import re
import json
from collections.abc import Iterable
from typing import Annotated, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator, model_validator

from .artifacts import stable_model_hash
from .causal_audit import build_causal_audit_plan, build_report_core_envelope
from .models import (
    ArbitrationResponse,
    AtomicArbitrationResponse,
    AtomicPrimaryResponse,
    AuditedNoMatchRelationJudgment,
    CausalFieldAuditJudgment,
    CausalFieldVerdict,
    ClauseAuditJudgment,
    CoreClaimTruth,
    DefectClass,
    ExpectedAssessment,
    FrozenFieldValidityAudit,
    FrozenValidityCertificate,
    JudgeReading,
    JudgeResponse,
    MatchStrength,
    MaterialAssertionVerdict,
    NoMatchRelationJudgment,
    PositiveMatchStrength,
    RelationAssessment,
    RelationBatchJudgeInput,
    RelationBatchResponse,
    RelationJudgeInput,
    RelationResponse,
    ReportAssessment,
    ReportCausalFieldAudit,
    ReportField,
    ReportJudgment,
    ReportTextEvidence,
    ReportTextEvidenceRole,
    ReportValidity,
    SupportedRelationJudgment,
    UnifiedJudgeInput,
    VALID_DEFECT_CLASSES,
    ValidityAuditWarning,
    ValidityBatchJudgeInput,
    ValidityBatchResponse,
    ValidityClauseRole,
    ValidityGateJudgment,
    ValidityGateStatus,
    ValidityJudgeInput,
    ValidityResponse,
    minimum_evidence_status_of,
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
    audit_plan = build_causal_audit_plan((report,)).report_plans[0]
    plan_by_field = {item.report_field.value: item for item in audit_plan.field_plans}
    for audit in row.causal_field_audits:
        field_name = audit.report_field.value
        expected_assertion_ids = [
            item.assertion_id for item in plan_by_field[field_name].source_units
        ]
        actual_assertion_ids = [
            item.assertion_id for item in audit.material_assertion_audits
        ]
        if actual_assertion_ids != expected_assertion_ids:
            raise ValueError(
                f"{object_path}.causal_field_audits[{field_name}] source-unit "
                "closure failed; "
                f"expected={expected_assertion_ids}, actual={actual_assertion_ids}"
            )
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
    if len(actual_partition) != len(set(actual_partition)) or set(
        actual_partition
    ) != set(expected_ids):
        raise ValueError(
            f"{object_path}.relation_decisions must cover every expected ID "
            f"exactly once; expected={expected_ids}, positive={positive_ids}, "
            f"no_match={no_match_ids}"
        )
    return core_truth


def _exact_relation_decision_type(
    *, expected_id: str, suffix: str, audited_no_match: bool = False
):
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

    no_match_base = (
        AuditedNoMatchRelationJudgment if audited_no_match else NoMatchRelationJudgment
    )

    class ExactNoMatchRelationJudgment(no_match_base):  # type: ignore[valid-type,misc]
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


def _exact_relation_tuple(
    expected_ids: tuple[str, ...],
    *,
    suffix: str,
    audited_no_match: bool = False,
):
    """Return one shared exact relation tuple type for a pair's expected closure."""

    relation_decision_types = tuple(
        _exact_relation_decision_type(
            expected_id=expected_id,
            suffix=f"{suffix}_{index}",
            audited_no_match=audited_no_match,
        )
        for index, expected_id in enumerate(expected_ids)
    )
    return tuple.__class_getitem__(relation_decision_types)


def _exact_report_model(
    judge_input: UnifiedJudgeInput,
    *,
    allowed_report_ids: tuple[str, ...],
    exact_relation_tuple,
    suffix: str,
):
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    report_id_type = _literal(allowed_report_ids)
    reports_by_id = {item.report_id: item for item in judge_input.reports}

    class ExactReportJudgment(ReportJudgment):
        """One validity-first sparse judgment restricted to exact closure IDs."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
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
    shared_relation_tuple = _exact_relation_tuple(
        expected_ids, suffix=f"{suffix}_relations"
    )
    ExactReportJudgment = _exact_report_model(
        judge_input,
        allowed_report_ids=report_ids,
        exact_relation_tuple=shared_relation_tuple,
        suffix=suffix,
    )

    class ExactJudgeResponse(JudgeResponse):
        """Sparse validity-first semantics with exact exhaustive report closure."""

        report_judgments: tuple[ExactReportJudgment, ...] = Field(
            min_length=len(report_ids),
            max_length=len(report_ids),
            description="One exact causal-certificate and exhaustive relation judgment for every anonymous report; report order is semantically irrelevant.",
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


def build_exact_primary_model(
    judge_input: UnifiedJudgeInput, target_report_id: str
) -> type[AtomicPrimaryResponse]:
    """Build one flat primary response over one exact report and all expected IDs."""

    reports_by_id = {item.report_id: item for item in judge_input.reports}
    if target_report_id not in reports_by_id:
        raise ValueError(
            f"target_report_id is outside the report closure: {target_report_id}"
        )
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    suffix = hashlib.sha256(
        (target_report_id + "::" + "|".join(expected_ids) + "::primary").encode("utf-8")
    ).hexdigest()[:12]
    report_id_type = _literal((target_report_id,))
    exact_relation_tuple = _exact_relation_tuple(
        expected_ids, suffix=f"{suffix}_relations"
    )

    class ExactAtomicPrimaryResponse(AtomicPrimaryResponse):
        """Flat independent judgment for exactly one anonymous report."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="The one anonymous report ID fixed by this atomic primary call."
        )
        relation_decisions: exact_relation_tuple = Field(  # type: ignore[valid-type]
            description="One provider-native discriminated decision at each exact expected position, in input order; keep this field at the response root."
        )

        @model_validator(mode="after")
        def exact_primary_closure(self) -> ExactAtomicPrimaryResponse:
            _validate_report_judgment(
                row=self,
                report=reports_by_id[self.report_id],
                expected_ids=expected_ids,
                object_path=f"atomic_primary[{self.report_id}]",
            )
            return self

    ExactAtomicPrimaryResponse.__name__ = f"ExactAtomicPrimaryResponse_{suffix}"
    return cast(type[AtomicPrimaryResponse], ExactAtomicPrimaryResponse)


def build_validity_input(
    judge_input: UnifiedJudgeInput, target_report_id: str
) -> ValidityJudgeInput:
    """Project one report and common artifacts into an expected-isolated input."""

    report = next(
        (item for item in judge_input.reports if item.report_id == target_report_id),
        None,
    )
    if report is None:
        raise ValueError(
            f"target_report_id is outside the report closure: {target_report_id}"
        )
    envelope = build_report_core_envelope(report)
    return ValidityJudgeInput(
        protocol_version=judge_input.protocol_version,
        report=report,
        core_envelope=envelope,
        artifact_closure=judge_input.artifact_closure,
        reason="This input physically isolates report validity from expected-issue matching and experimental metadata.",
        basis=(
            f"{judge_input.protocol_version}; {envelope.envelope_hash}; "
            f"{judge_input.artifact_closure.closure_hash}"
        ),
    )


def build_validity_batch_input(
    judge_input: UnifiedJudgeInput,
    report_ids: tuple[str, ...],
    *,
    batch_id: str,
) -> ValidityBatchJudgeInput:
    """Project a bounded report set and one shared closure into validity input."""

    reports_by_id = {item.report_id: item for item in judge_input.reports}
    if not report_ids or len(report_ids) != len(set(report_ids)):
        raise ValueError("validity batch report_ids must be non-empty and unique")
    unknown = tuple(item for item in report_ids if item not in reports_by_id)
    if unknown:
        raise ValueError(
            f"validity batch report IDs are outside the report closure: {unknown}"
        )
    reports = tuple(reports_by_id[item] for item in report_ids)
    envelopes = tuple(build_report_core_envelope(item) for item in reports)
    return ValidityBatchJudgeInput(
        batch_id=batch_id,
        protocol_version=judge_input.protocol_version,
        reports=reports,
        core_envelopes=envelopes,
        artifact_closure=judge_input.artifact_closure,
        reason=(
            "This bounded input audits every report independently while physically "
            "isolating validity from expected issues and experimental metadata."
        ),
        basis=(
            f"{judge_input.protocol_version}; {batch_id}; "
            + ",".join(item.envelope_hash for item in envelopes)
            + f"; {judge_input.artifact_closure.closure_hash}"
        ),
    )


def validity_item_input(
    batch_input: ValidityBatchJudgeInput, index: int
) -> ValidityJudgeInput:
    """Reconstruct one atomic validity view without duplicating serialized artifacts."""

    report = batch_input.reports[index]
    envelope = batch_input.core_envelopes[index]
    return ValidityJudgeInput(
        protocol_version=batch_input.protocol_version,
        report=report,
        core_envelope=envelope,
        artifact_closure=batch_input.artifact_closure,
        reason="This input physically isolates report validity from expected-issue matching and experimental metadata.",
        basis=(
            f"{batch_input.protocol_version}; {envelope.envelope_hash}; "
            f"{batch_input.artifact_closure.closure_hash}"
        ),
    )


def _exact_clause_audit_group(field_plan, *, suffix: str) -> type[BaseModel]:
    """Build one fixed object property for every immutable source clause."""

    field_definitions: dict[str, tuple[object, Field]] = {}
    for index, clause in enumerate(field_plan.clauses):
        clause_id_type = _literal((clause.clause_id,))

        class ExactClauseAuditJudgment(ClauseAuditJudgment):
            """Truth judgment fixed to one immutable report source clause."""

            clause_id: clause_id_type = Field(  # type: ignore[valid-type]
                description="Clause ID fixed by this exact source position; it cannot be omitted, duplicated, or moved."
            )

        ExactClauseAuditJudgment.__name__ = f"ExactClauseAuditJudgment_{suffix}_{index}"
        field_definitions[f"item{index}"] = (
            ExactClauseAuditJudgment,
            Field(
                description=(
                    f"Required audit for immutable source clause {clause.clause_id} "
                    f"at exact position {index}; the property name and clause ID are fixed."
                )
            ),
        )

    class ExactClauseAuditGroup(BaseModel):
        """Provider-stable object containing exact source-clause audit slots."""

        model_config = ConfigDict(extra="forbid", frozen=True)

    model = create_model(
        f"ExactClauseAuditGroup_{suffix}",
        __base__=ExactClauseAuditGroup,
        **field_definitions,
    )
    model.__doc__ = (
        "Provider-stable fixed object with one required itemN property for every "
        "immutable source clause in source order."
    )
    return model


def _ordered_clause_audits(
    response: BaseModel, field_plan
) -> tuple[ClauseAuditJudgment, ...]:
    """Read one fixed audit object back in immutable source order."""

    group = getattr(response, f"{field_plan.report_field.value}_audit")
    return tuple(
        getattr(group, f"item{index}")
        for index, _clause in enumerate(field_plan.clauses)
    )


def build_exact_validity_model(
    validity_input: ValidityJudgeInput,
) -> type[ValidityResponse]:
    """Build fixed top-level field slots for one expected-isolated validity call."""

    suffix = hashlib.sha256(
        (
            validity_input.report.report_id
            + "::"
            + validity_input.core_envelope.envelope_hash
            + "::validity"
        ).encode("utf-8")
    ).hexdigest()[:12]
    report_id_type = _literal((validity_input.report.report_id,))
    field_definitions: dict[str, tuple[object, Field]] = {
        "report_id": (
            report_id_type,
            Field(
                description="The one anonymous report ID fixed by this expected-isolated validity call."
            ),
        )
    }
    for field_plan in validity_input.core_envelope.field_plans:
        field_name = f"{field_plan.report_field.value}_audit"
        exact_group = _exact_clause_audit_group(
            field_plan, suffix=f"{suffix}_{field_plan.report_field.value}"
        )
        field_definitions[field_name] = (
            exact_group,
            Field(
                description=(
                    f"Required fixed audit object for every immutable clause in CandidateReport.{field_plan.report_field.value}; "
                    "fill each itemN property exactly once, judge the complete semantic proposition, classify its role in the bounded report claim, and retain auxiliary errors without promoting them to a hard gate."
                )
            ),
        )

    class ExactValidityResponseBase(ValidityResponse):
        """Validity response with deterministic closure over this exact report."""

        @model_validator(mode="after")
        def exact_gate_closure(self) -> ExactValidityResponseBase:
            clause_rows = [
                (field_plan.report_field, clause)
                for field_plan in validity_input.core_envelope.field_plans
                for clause in _ordered_clause_audits(self, field_plan)
            ]
            claim_rows = [
                clause
                for field, clause in clause_rows
                if field.value == "claim"
                and clause.validity_role == ValidityClauseRole.CORE_CLAIM
            ]
            if not claim_rows:
                raise ValueError(
                    "claim_audit must classify at least one complete clause as CORE_CLAIM"
                )
            defect_class = self.defect_adjudication.defect_class
            hard_refuted = [
                clause.clause_id
                for _field, clause in clause_rows
                if clause.validity_role
                in (
                    ValidityClauseRole.CORE_CLAIM,
                    ValidityClauseRole.INDISPENSABLE_MECHANISM,
                )
                and clause.verdict == MaterialAssertionVerdict.REFUTED
            ]
            if defect_class in VALID_DEFECT_CLASSES and hard_refuted:
                raise ValueError(
                    f"defect_class {defect_class.value} asserts the load-bearing fact is true of the author source, "
                    f"but CORE_CLAIM/INDISPENSABLE_MECHANISM clauses {hard_refuted} are REFUTED. Re-read each refuted "
                    "clause under the report's competent reading: a clause saying a guard, condition, effect, action, "
                    "initial edge, or unconditional entry is missing means that no separate carrier of that kind is "
                    "authored, so it is SUPPORTED when the author wrote the content only as label text or as a labeled "
                    "transition; an over-stated or mis-named conjunct about the same locus and repair is "
                    "AUXILIARY_CONTEXT. Choose A0_FALSE_POSITIVE only when the author source contradicts the report's "
                    "concern as a whole."
                )
            if defect_class == DefectClass.A0_FALSE_POSITIVE and not hard_refuted:
                raise ValueError(
                    "defect_class A0_FALSE_POSITIVE requires the false load-bearing premise to be marked REFUTED "
                    "on a CORE_CLAIM or INDISPENSABLE_MECHANISM clause"
                )
            return self

    model = create_model(
        f"ExactValidityResponse_{suffix}",
        __base__=ExactValidityResponseBase,
        **field_definitions,
    )
    model.__doc__ = (
        "Expected-isolated validity response with one required fixed audit slot "
        "for every non-null report field."
    )

    return cast(type[ValidityResponse], model)


def _merge_split_singleton_items(
    payload: object,
    *,
    batch_id: str,
    batch_schema_version: str,
    report_id: str,
    expected_ids: tuple[str, ...],
) -> object:
    """Merge a one-report batch answered as one item per expected issue into ``item0``.

    Providers sometimes partition a single-report relation batch by expected issue
    and return ``item0..itemN`` that all name the same report, each carrying a subset
    of the expected positions. The report identity and the expected order are fixed
    by the input, so recombining the decisions is a deterministic normalization, not
    a judgment. A foreign report ID, two different decisions for one expected ID, or
    a missing expected position leaves the payload unchanged so the ordinary
    validation error is reported instead.
    """

    if not isinstance(payload, dict):
        return payload
    items = {key: value for key, value in payload.items() if re.fullmatch(r"item\d+", key)}
    if len(items) < 2:
        return payload
    for item in items.values():
        if not isinstance(item, dict) or item.get("report_id", report_id) != report_id:
            return payload
    ordered_keys = sorted(items, key=lambda key: int(key[4:]))
    by_expected: dict[str, dict] = {}
    source_refs: list[str] = []
    for key in ordered_keys:
        for decision in items[key].get("relation_decisions") or ():
            if not isinstance(decision, dict) or "expected_id" not in decision:
                return payload
            prior = by_expected.get(decision["expected_id"])
            if prior is not None and prior.get("match") != decision.get("match"):
                return payload
            by_expected.setdefault(decision["expected_id"], decision)
        for ref in items[key].get("relation_source_refs") or ():
            if isinstance(ref, str) and ref not in source_refs:
                source_refs.append(ref)
    if set(by_expected) != set(expected_ids):
        return payload
    merged = {
        **items[ordered_keys[0]],
        "report_id": report_id,
        "relation_decisions": [by_expected[expected_id] for expected_id in expected_ids],
    }
    if source_refs:
        merged["relation_source_refs"] = source_refs
    rest = {key: value for key, value in payload.items() if key not in items}
    return {**rest, "schema_version": batch_schema_version, "batch_id": batch_id, "item0": merged}


def _wrap_bare_singleton_item(
    payload: object,
    *,
    batch_id: str,
    batch_schema_version: str,
    report_count: int,
) -> object:
    """Wrap a bare single-item response into ``item0`` for a one-report batch.

    Providers sometimes answer a one-report batch in the atomic item shape (the
    item's fields at top level). The batch identity is fixed by the input, so
    wrapping is a deterministic normalization, not a judgment; multi-report
    batches and payloads that already carry ``item0`` are returned unchanged.
    """

    if report_count != 1 or not isinstance(payload, dict) or "item0" in payload:
        return payload
    item = {
        key: value
        for key, value in payload.items()
        if key not in {"batch_id", "schema_version"}
    }
    if "report_id" not in item:
        return payload
    if "schema_version" in payload and isinstance(payload["schema_version"], str):
        item["schema_version"] = payload["schema_version"]
    return {"schema_version": batch_schema_version, "batch_id": batch_id, "item0": item}


def build_exact_validity_batch_model(
    batch_input: ValidityBatchJudgeInput,
) -> type[ValidityBatchResponse]:
    """Build one fixed item slot for every report and every source clause."""

    suffix = hashlib.sha256(
        (
            batch_input.batch_id
            + "::"
            + "|".join(item.envelope_hash for item in batch_input.core_envelopes)
            + "::validity-batch"
        ).encode("utf-8")
    ).hexdigest()[:12]
    batch_id_type = _literal((batch_input.batch_id,))
    field_definitions: dict[str, tuple[object, Field]] = {
        "batch_id": (
            batch_id_type,
            Field(description="The exact validity batch ID; return it unchanged."),
        )
    }
    for index, report in enumerate(batch_input.reports):
        exact_item = build_exact_validity_model(validity_item_input(batch_input, index))
        field_definitions[f"item{index}"] = (
            exact_item,
            Field(
                description=(
                    f"Required independent complete validity audit for anonymous report "
                    f"{report.report_id} at exact batch position {index}."
                )
            ),
        )

    class ExactValidityBatchResponseBase(ValidityBatchResponse):
        """Exact expected-isolated response over one bounded report batch."""

        @model_validator(mode="before")
        @classmethod
        def wrap_bare_singleton(cls, payload: object) -> object:
            return _wrap_bare_singleton_item(
                payload,
                batch_id=batch_input.batch_id,
                batch_schema_version="semantic-judge.validity-batch-response.v1",
                report_count=len(batch_input.reports),
            )

    model = create_model(
        f"ExactValidityBatchResponse_{suffix}",
        __base__=ExactValidityBatchResponseBase,
        **field_definitions,
    )
    model.__doc__ = (
        "Expected-isolated bounded-batch validity response with one required "
        "fixed report item and complete clause slots at every input position."
    )
    model.__semantic_judge_recipe__ = {  # type: ignore[attr-defined]
        "kind": "validity_batch",
        "input": batch_input.model_dump(mode="json"),
    }
    return cast(type[ValidityBatchResponse], model)


def validity_batch_responses(
    response: BaseModel, batch_input: ValidityBatchJudgeInput
) -> tuple[ValidityResponse, ...]:
    """Extract exact validity responses in immutable batch order."""

    rows = tuple(
        getattr(response, f"item{index}")
        for index, _report in enumerate(batch_input.reports)
    )
    actual_ids = [item.report_id for item in rows]
    expected_ids = [item.report_id for item in batch_input.reports]
    if actual_ids != expected_ids:
        raise ValueError(
            "validity batch response report closure differs from the input order"
        )
    return cast(tuple[ValidityResponse, ...], rows)


def _field_verdict(
    clause_audits: tuple[ClauseAuditJudgment, ...],
) -> CausalFieldVerdict:
    verdicts = {item.verdict for item in clause_audits}
    if verdicts == {MaterialAssertionVerdict.SUPPORTED}:
        return CausalFieldVerdict.SUPPORTED
    if verdicts == {MaterialAssertionVerdict.REFUTED}:
        return CausalFieldVerdict.REFUTED
    return CausalFieldVerdict.MIXED


def _derive_clause_gate(
    field_audits: tuple[FrozenFieldValidityAudit, ...],
    *,
    role: ValidityClauseRole,
    label: str,
    fallback_source_refs: tuple[str, ...],
) -> ValidityGateJudgment:
    """Materialize one non-redundant hard gate from exact clause judgments."""

    rows = tuple(
        clause
        for field in field_audits
        for clause in field.clause_audits
        if clause.validity_role == role
    )
    status = (
        ValidityGateStatus.REFUTED
        if any(row.verdict == MaterialAssertionVerdict.REFUTED for row in rows)
        else ValidityGateStatus.SATISFIED
    )
    if rows:
        reason = f"Backend-derived {label} gate is {status.value}: " + " ".join(
            f"{row.clause_id}={row.verdict.value}: {row.reason}" for row in rows
        )
        basis = " ".join(f"{row.clause_id}: {row.basis}" for row in rows)
        source_refs = _unique(ref for row in rows for ref in row.source_refs)
    else:
        reason = (
            f"Backend-derived {label} gate is SATISFIED because the bounded claim "
            "requires no separate clause with this semantic role."
        )
        basis = (
            "Complete fixed clause-role closure contains no separate required premise."
        )
        source_refs = fallback_source_refs
    return ValidityGateJudgment(
        status=status,
        reason=reason,
        basis=basis,
        source_refs=source_refs,
    )


def materialize_validity_certificate(
    response: BaseModel,
    validity_input: ValidityJudgeInput,
) -> FrozenValidityCertificate:
    """Freeze exact report text, clause verdicts, and backend-derived core truth."""

    field_audits = []
    for field_plan in validity_input.core_envelope.field_plans:
        field_name = field_plan.report_field.value
        clause_audits = _ordered_clause_audits(response, field_plan)
        exact_text = getattr(validity_input.report, field_name)
        if not isinstance(exact_text, str):
            raise TypeError(
                f"core envelope references null CandidateReport.{field_name}"
            )
        field_audits.append(
            FrozenFieldValidityAudit(
                report_field=field_plan.report_field,
                is_core_field=field_plan.is_core_field,
                exact_text=exact_text,
                exact_text_sha256="sha256:"
                + hashlib.sha256(exact_text.encode("utf-8")).hexdigest(),
                clauses=field_plan.clauses,
                clause_audits=clause_audits,
                verdict=_field_verdict(clause_audits),
                reason=" ".join(
                    f"{item.clause_id}={item.verdict.value}: {item.reason}"
                    for item in clause_audits
                ),
                basis=" ".join(
                    f"{item.clause_id}: {item.basis}" for item in clause_audits
                ),
                source_refs=_unique(
                    ref for item in clause_audits for ref in item.source_refs
                ),
            )
        )
    frozen_audits = tuple(field_audits)
    auxiliary_warnings = tuple(
        ValidityAuditWarning(
            report_field=field.report_field,
            clause_id=clause.clause_id,
            reason=clause.reason,
            basis=clause.basis,
            source_refs=clause.source_refs,
        )
        for field in frozen_audits
        for clause in field.clause_audits
        if clause.validity_role == ValidityClauseRole.AUXILIARY_CONTEXT
        and clause.verdict == MaterialAssertionVerdict.REFUTED
    )
    response_source_refs = tuple(response.validity_source_refs)
    core_claim_gate = _derive_clause_gate(
        frozen_audits,
        role=ValidityClauseRole.CORE_CLAIM,
        label="core claim",
        fallback_source_refs=response_source_refs,
    )
    indispensable_mechanism_gate = _derive_clause_gate(
        frozen_audits,
        role=ValidityClauseRole.INDISPENSABLE_MECHANISM,
        label="indispensable mechanism",
        fallback_source_refs=response_source_refs,
    )
    adjudication = response.defect_adjudication
    minimum_evidence_status = minimum_evidence_status_of(adjudication.defect_class)
    minimum_evidence_gate = ValidityGateJudgment(
        status=minimum_evidence_status,
        reason=(
            f"Backend-derived minimum-evidence gate is {minimum_evidence_status.value} from defect class "
            f"{adjudication.defect_class.value}: {adjudication.reason}"
        ),
        basis=adjudication.basis,
        source_refs=adjudication.source_refs,
    )
    core_truth = (
        CoreClaimTruth.VALID
        if all(
            gate.status == ValidityGateStatus.SATISFIED
            for gate in (
                core_claim_gate,
                indispensable_mechanism_gate,
                minimum_evidence_gate,
            )
        )
        else CoreClaimTruth.INVALID
    )
    values = {
        "schema_version": "semantic-judge.frozen-validity-certificate.v3",
        "report_id": validity_input.report.report_id,
        "core_truth": core_truth,
        "validity_input_hash": stable_model_hash(validity_input),
        "core_envelope_hash": validity_input.core_envelope.envelope_hash,
        "field_audits": frozen_audits,
        "core_claim_gate": core_claim_gate,
        "indispensable_mechanism_gate": indispensable_mechanism_gate,
        "minimum_evidence_gate": minimum_evidence_gate,
        "defect_adjudication": adjudication,
        "auxiliary_warnings": auxiliary_warnings,
        "root_cause_cluster_key": response.root_cause_cluster_key,
        "reason": response.validity_reason,
        "basis": response.validity_basis,
        "source_refs": response_source_refs,
    }
    hash_payload = {}
    for key, value in values.items():
        if isinstance(value, tuple):
            hash_payload[key] = [
                item.model_dump(mode="json") if isinstance(item, BaseModel) else item
                for item in value
            ]
        elif isinstance(value, BaseModel):
            hash_payload[key] = value.model_dump(mode="json")
        elif isinstance(value, CoreClaimTruth):
            hash_payload[key] = value.value
        else:
            hash_payload[key] = value
    serialized = json.dumps(
        hash_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    return FrozenValidityCertificate(
        **values,
        certificate_hash="sha256:"
        + hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
    )


def build_relation_input(
    judge_input: UnifiedJudgeInput,
    certificate: FrozenValidityCertificate,
    *,
    relation_scope: str = "valid_only",
) -> RelationJudgeInput:
    """Build one relation-only input from an immutable admissible certificate."""

    report = next(
        item for item in judge_input.reports if item.report_id == certificate.report_id
    )
    return RelationJudgeInput(
        protocol_version=judge_input.protocol_version,
        report=report,
        validity_certificate=certificate,
        relation_scope=relation_scope,  # type: ignore[arg-type]
        expected_issues=judge_input.expected_issues,
        artifact_closure=judge_input.artifact_closure,
        reason="This input permits expected matching only after report validity has been frozen independently.",
        basis=(
            f"{judge_input.protocol_version}; {certificate.certificate_hash}; "
            f"{judge_input.artifact_closure.closure_hash}"
        ),
    )


def build_relation_batch_input(
    judge_input: UnifiedJudgeInput,
    certificates: tuple[FrozenValidityCertificate, ...],
    *,
    batch_id: str,
    relation_scope: str = "valid_only",
) -> RelationBatchJudgeInput:
    """Build one relation matrix input with shared expected and artifact closures."""

    reports_by_id = {item.report_id: item for item in judge_input.reports}
    if not certificates:
        raise ValueError("relation batch requires at least one admissible certificate")
    reports = tuple(reports_by_id[item.report_id] for item in certificates)
    return RelationBatchJudgeInput(
        batch_id=batch_id,
        protocol_version=judge_input.protocol_version,
        reports=reports,
        validity_certificates=certificates,
        relation_scope=relation_scope,  # type: ignore[arg-type]
        expected_issues=judge_input.expected_issues,
        artifact_closure=judge_input.artifact_closure,
        reason=(
            "This bounded input compares each frozen-valid report with the complete "
            "expected denominator without reopening validity."
        ),
        basis=(
            f"{judge_input.protocol_version}; {batch_id}; "
            + ",".join(item.certificate_hash for item in certificates)
            + f"; {judge_input.artifact_closure.closure_hash}"
        ),
    )


def relation_item_input(
    batch_input: RelationBatchJudgeInput, index: int
) -> RelationJudgeInput:
    """Reconstruct one atomic relation view from a shared serialized batch."""

    return RelationJudgeInput(
        protocol_version=batch_input.protocol_version,
        report=batch_input.reports[index],
        validity_certificate=batch_input.validity_certificates[index],
        relation_scope=batch_input.relation_scope,
        expected_issues=batch_input.expected_issues,
        artifact_closure=batch_input.artifact_closure,
        reason=batch_input.reason,
        basis=(
            f"{batch_input.protocol_version}; {batch_input.batch_id}; "
            f"{batch_input.validity_certificates[index].certificate_hash}; "
            f"{batch_input.artifact_closure.closure_hash}"
        ),
    )


def build_exact_relation_model(
    relation_input: RelationJudgeInput,
) -> type[RelationResponse]:
    """Build a relation-only schema over one VALID report and every expected ID."""

    expected_ids = tuple(item.expected_id for item in relation_input.expected_issues)
    suffix = hashlib.sha256(
        (
            relation_input.report.report_id
            + "::"
            + relation_input.validity_certificate.certificate_hash
            + "::"
            + "|".join(expected_ids)
        ).encode("utf-8")
    ).hexdigest()[:12]
    report_id_type = _literal((relation_input.report.report_id,))
    exact_relation_tuple = _exact_relation_tuple(
        expected_ids,
        suffix=f"{suffix}_relations",
        audited_no_match=True,
    )

    class ExactRelationResponse(RelationResponse):
        """Relation-only judgment for one frozen-valid anonymous report."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="The one anonymous valid report ID fixed by this relation call."
        )
        validity_certificate_hash: str = Field(
            default=relation_input.validity_certificate.certificate_hash,
            pattern=r"^sha256:[0-9a-f]{64}$",
            description="Backend-owned immutable validity certificate hash; the provider does not need to return it, and any returned value is replaced by the frozen hash.",
        )
        relation_decisions: exact_relation_tuple = Field(  # type: ignore[valid-type]
            description="One discriminated FULL_MATCH, PARTIAL_MATCH, or explicit NO_MATCH decision at every exact expected position in input order."
        )

        @field_validator("validity_certificate_hash", mode="before")
        @classmethod
        def pin_frozen_certificate_hash(cls, value: object) -> str:
            """The certificate is fixed by the batch input; a provider echo cannot change or break it."""

            return relation_input.validity_certificate.certificate_hash

        @model_validator(mode="after")
        def exact_relation_closure(self) -> ExactRelationResponse:
            positive_ids = []
            no_match_ids = []
            for index, decision in enumerate(self.relation_decisions):
                if decision.match == MatchStrength.NO_MATCH:
                    no_match_ids.append(decision.expected_id)
                    continue
                positive = cast(SupportedRelationJudgment, decision)
                if ReportField.CLAIM not in positive.report_field_refs:
                    raise ValueError(
                        f"relation_decisions[{index}].report_field_refs must include claim"
                    )
                for field_ref in positive.report_field_refs:
                    if not isinstance(
                        getattr(relation_input.report, field_ref.value), str
                    ):
                        raise TypeError(
                            f"relation_decisions[{index}] references null report field {field_ref.value}"
                        )
                positive_ids.append(positive.expected_id)
            actual = positive_ids + no_match_ids
            if len(actual) != len(set(actual)) or set(actual) != set(expected_ids):
                raise ValueError(
                    "relation_decisions must cover every expected ID exactly once"
                )
            return self

    ExactRelationResponse.__name__ = f"ExactRelationResponse_{suffix}"
    return cast(type[RelationResponse], ExactRelationResponse)


def build_exact_relation_batch_model(
    batch_input: RelationBatchJudgeInput,
) -> type[RelationBatchResponse]:
    """Build an exact report-by-expected matrix response for one bounded batch."""

    suffix = hashlib.sha256(
        (
            batch_input.batch_id
            + "::"
            + "|".join(
                item.certificate_hash for item in batch_input.validity_certificates
            )
            + "::relation-batch"
        ).encode("utf-8")
    ).hexdigest()[:12]
    batch_id_type = _literal((batch_input.batch_id,))
    field_definitions: dict[str, tuple[object, Field]] = {
        "batch_id": (
            batch_id_type,
            Field(description="The exact relation batch ID; return it unchanged."),
        )
    }
    for index, report in enumerate(batch_input.reports):
        exact_item = build_exact_relation_model(relation_item_input(batch_input, index))
        field_definitions[f"item{index}"] = (
            exact_item,
            Field(
                description=(
                    f"Required complete expected relation partition for anonymous "
                    f"report {report.report_id} at exact batch position {index}."
                )
            ),
        )

    class ExactRelationBatchResponseBase(RelationBatchResponse):
        """Exact response over one frozen-valid report-by-expected matrix."""

        @model_validator(mode="before")
        @classmethod
        def wrap_bare_singleton(cls, payload: object) -> object:
            if len(batch_input.reports) == 1:
                payload = _merge_split_singleton_items(
                    payload,
                    batch_id=batch_input.batch_id,
                    batch_schema_version="semantic-judge.relation-batch-response.v1",
                    report_id=batch_input.reports[0].report_id,
                    expected_ids=tuple(item.expected_id for item in batch_input.expected_issues),
                )
            return _wrap_bare_singleton_item(
                payload,
                batch_id=batch_input.batch_id,
                batch_schema_version="semantic-judge.relation-batch-response.v1",
                report_count=len(batch_input.reports),
            )

    model = create_model(
        f"ExactRelationBatchResponse_{suffix}",
        __base__=ExactRelationBatchResponseBase,
        **field_definitions,
    )
    model.__doc__ = (
        "Relation-only bounded-batch response with one required report item and "
        "one exact FULL, PARTIAL, or NO decision at every expected position."
    )
    model.__semantic_judge_recipe__ = {  # type: ignore[attr-defined]
        "kind": "relation_batch",
        "input": batch_input.model_dump(mode="json"),
    }
    return cast(type[RelationBatchResponse], model)


def relation_batch_responses(
    response: BaseModel, batch_input: RelationBatchJudgeInput
) -> tuple[RelationResponse, ...]:
    """Extract exact relation partitions in immutable batch order."""

    rows = tuple(
        getattr(response, f"item{index}")
        for index, _report in enumerate(batch_input.reports)
    )
    actual_ids = [item.report_id for item in rows]
    expected_ids = [item.report_id for item in batch_input.reports]
    if actual_ids != expected_ids:
        raise ValueError(
            "relation batch response report closure differs from the input order"
        )
    return cast(tuple[RelationResponse, ...], rows)


def build_exact_arbitration_model(
    judge_input: UnifiedJudgeInput,
    conflicted_report_ids: tuple[str, ...],
) -> type[AtomicArbitrationResponse]:
    """Build one flat conflict-only response over one exact report identity."""

    if len(conflicted_report_ids) != 1:
        raise ValueError(
            "atomic arbitration requires exactly one conflicted report ID; "
            f"actual={conflicted_report_ids}"
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
    report_id = conflicted_report_ids[0]
    report_id_type = _literal((report_id,))
    reports_by_id = {item.report_id: item for item in judge_input.reports}
    exact_relation_tuple = _exact_relation_tuple(
        expected_ids, suffix=f"{suffix}_relations"
    )

    class ExactAtomicArbitrationResponse(AtomicArbitrationResponse):
        """Flat final judgment for exactly one conflicted anonymous report."""

        report_id: report_id_type = Field(  # type: ignore[valid-type]
            description="The one anonymous report ID fixed by this atomic arbitration call."
        )
        relation_decisions: exact_relation_tuple = Field(  # type: ignore[valid-type]
            description="One provider-native discriminated decision at each exact expected position, in input order; keep this field at the response root."
        )

        @model_validator(mode="after")
        def exact_atomic_closure(self) -> ExactAtomicArbitrationResponse:
            _validate_report_judgment(
                row=self,
                report=reports_by_id[self.report_id],
                expected_ids=expected_ids,
                object_path=f"atomic_arbitration[{self.report_id}]",
            )
            return self

    ExactAtomicArbitrationResponse.__name__ = f"ExactAtomicArbitrationResponse_{suffix}"
    return cast(type[AtomicArbitrationResponse], ExactAtomicArbitrationResponse)


def merge_arbitration_response(
    primary_response: JudgeResponse,
    arbitration_response: ArbitrationResponse,
    response_model: type[JudgeResponse],
) -> JudgeResponse:
    """Replace conflicted reports and revalidate the complete sparse closure."""

    replacements = {row.report_id: row for row in arbitration_response.report_judgments}
    merged = [
        replacements.get(row.report_id, row)
        for row in primary_response.report_judgments
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
            "sha256:" + hashlib.sha256(field_value.encode("utf-8")).hexdigest()
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
    report_plan = build_causal_audit_plan((report,)).report_plans[0]
    field_plan = next(
        item
        for item in report_plan.field_plans
        if item.report_field == judgment.report_field
    )
    return ReportCausalFieldAudit(
        report_field=judgment.report_field,
        exact_text=field_value,
        exact_text_sha256="sha256:"
        + hashlib.sha256(field_value.encode("utf-8")).hexdigest(),
        source_units=field_plan.source_units,
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
                            if field_ref.value
                            == judgment.causal_certificate_field.value
                            else ReportTextEvidenceRole.CLAIM_BOUNDARY
                        ),
                        reason=(
                            "The complete supported causal certificate establishes the report-owned premise used by this relation."
                            if field_ref.value
                            == judgment.causal_certificate_field.value
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

    relation_by_key = {(row.report_id, row.expected_id): row for row in relations}
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


def materialize_two_stage_reading(
    certificates: tuple[FrozenValidityCertificate, ...],
    relation_responses: tuple[RelationResponse, ...],
    judge_input: UnifiedJudgeInput,
    *,
    closure_rule: str = "validity_first",
) -> JudgeReading:
    """Derive dense issue #195 ownership from frozen truth and relation closure.

    ``validity_first`` is the v3.2 protocol: INVALID certificates close as all-NO.
    ``relation_first`` (default since v3.8) decides hit first: D0 / NOT_A_DEFECT_CLAIM
    certificates are also compared with the ledger, a FULL_MATCH closes them as
    VALID_KNOWN, a PARTIAL_MATCH only records support, and FALSE_POSITIVE stays INVALID.
    """

    if closure_rule not in ("validity_first", "relation_first"):
        raise ValueError(f"unknown closure_rule: {closure_rule}")
    relation_first = closure_rule == "relation_first"

    report_ids = tuple(item.report_id for item in judge_input.reports)
    expected_ids = tuple(item.expected_id for item in judge_input.expected_issues)
    reports_by_id = {item.report_id: item for item in judge_input.reports}
    certificates_by_id = {item.report_id: item for item in certificates}
    if set(certificates_by_id) != set(report_ids) or len(certificates_by_id) != len(
        certificates
    ):
        raise ValueError("validity certificates must cover every report exactly once")
    candidate_ids = {
        report_id
        for report_id, certificate in certificates_by_id.items()
        if certificate.core_truth == CoreClaimTruth.VALID
        or (
            relation_first
            and certificate.defect_adjudication.defect_class
            != DefectClass.A0_FALSE_POSITIVE
        )
    }
    responses_by_id = {item.report_id: item for item in relation_responses}
    expected_response_ids = candidate_ids if expected_ids else set()
    if set(responses_by_id) != expected_response_ids or len(responses_by_id) != len(
        relation_responses
    ):
        raise ValueError(
            "relation responses must cover every and only VALID report exactly once when the expected denominator is non-empty, and must be empty when the denominator is empty"
        )

    relations = []
    report_assessments = []
    for report_id in report_ids:
        report = reports_by_id[report_id]
        certificate = certificates_by_id[report_id]
        response = responses_by_id.get(report_id)
        decisions_by_expected = (
            {item.expected_id: item for item in response.relation_decisions}
            if response is not None
            else {}
        )
        positive_by_expected = {
            expected_id: cast(SupportedRelationJudgment, decision)
            for expected_id, decision in decisions_by_expected.items()
            if decision.match != MatchStrength.NO_MATCH
        }
        full_expected_ids = []
        partial_expected_ids = []
        for expected_id in expected_ids:
            positive = positive_by_expected.get(expected_id)
            if positive is None:
                if report_id not in candidate_ids:
                    relation_reason = "The expected-isolated validity certificate is INVALID, so issue #195 requires this relation to be NO_MATCH."
                    relation_basis = f"{certificate.certificate_hash}; {certificate.reason}; all-NO invalid-report closure"
                    relation_source_refs = certificate.source_refs
                else:
                    no_match = decisions_by_expected.get(expected_id)
                    if no_match is None or no_match.match != MatchStrength.NO_MATCH:
                        raise ValueError(
                            f"valid report {report_id} lacks explicit NO_MATCH evidence for {expected_id}"
                        )
                    audited_no_match = cast(AuditedNoMatchRelationJudgment, no_match)
                    relation_reason = audited_no_match.reason
                    relation_basis = audited_no_match.basis
                    relation_source_refs = audited_no_match.source_refs
                relation = RelationAssessment(
                    report_id=report_id,
                    expected_id=expected_id,
                    match=MatchStrength.NO_MATCH,
                    report_text_evidence=(
                        _materialized_text_evidence(
                            report=report,
                            report_field=ReportField.CLAIM,
                            semantic_role=ReportTextEvidenceRole.CLAIM_BOUNDARY,
                            reason="The complete published claim defines this explicit NO relation boundary.",
                            basis=f"frozen_validity:{certificate.certificate_hash}",
                        ),
                    ),
                    reason=relation_reason,
                    basis=relation_basis,
                    source_refs=relation_source_refs,
                )
            else:
                match = MatchStrength(positive.match.value)
                if match == MatchStrength.FULL_MATCH:
                    full_expected_ids.append(expected_id)
                else:
                    partial_expected_ids.append(expected_id)
                field_refs = list(positive.report_field_refs)
                if ReportField.REASON not in field_refs:
                    field_refs.append(ReportField.REASON)
                evidence = tuple(
                    _materialized_text_evidence(
                        report=report,
                        report_field=field_ref,
                        semantic_role=(
                            ReportTextEvidenceRole.CLAIM_BOUNDARY
                            if field_ref == ReportField.CLAIM
                            else ReportTextEvidenceRole.CAUSAL_SUPPORT
                        ),
                        reason=(
                            "The complete published claim delimits this positive relation."
                            if field_ref == ReportField.CLAIM
                            else "The expected-isolated certificate establishes this complete report field as artifact-compatible support."
                        ),
                        basis=f"relation:{report_id}/{expected_id}; {certificate.certificate_hash}",
                    )
                    for field_ref in field_refs
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

        has_positive = bool(full_expected_ids or partial_expected_ids)
        relation_first_known = (
            relation_first
            and bool(full_expected_ids)
            and certificate.core_truth == CoreClaimTruth.INVALID
            and report_id in candidate_ids
        )
        relation_first_partial_only = (
            relation_first
            and has_positive
            and not full_expected_ids
            and certificate.core_truth == CoreClaimTruth.INVALID
            and report_id in candidate_ids
        )
        if relation_first_known:
            validity = ReportValidity.VALID_KNOWN
        else:
            validity = (
                ReportValidity.INVALID
                if certificate.core_truth == CoreClaimTruth.INVALID
                else ReportValidity.VALID_KNOWN
                if has_positive
                else ReportValidity.VALID_NOVEL
            )
        ownership_reason = (
            "Backend ownership is VALID_KNOWN under relation-first closure: the author-source fact is not refuted and a FULL_MATCH ledger relation settles the obligation question."
            if relation_first_known
            else "Backend ownership is INVALID under relation-first closure: the defect class is D0 or NOT_A_DEFECT_CLAIM and the report has only PARTIAL_MATCH support, which is recorded but does not make it a hit."
            if relation_first_partial_only
            else "Backend ownership is INVALID because expected-isolated core truth is INVALID and every relation is mechanically NO_MATCH."
            if validity == ReportValidity.INVALID
            else "Backend ownership is VALID_KNOWN because frozen core truth is VALID and at least one FULL_MATCH or PARTIAL_MATCH relation exists."
            if validity == ReportValidity.VALID_KNOWN
            else "Backend ownership is VALID_NOVEL because frozen core truth is VALID and every expected relation is explicitly NO_MATCH."
        )
        reason_audit = next(
            item
            for item in certificate.field_audits
            if item.report_field.value == "reason"
        )
        report_assessments.append(
            ReportAssessment(
                report_id=report_id,
                core_truth=certificate.core_truth,
                validity=validity,
                defect_class=certificate.defect_adjudication.defect_class,
                closure_rule=closure_rule,  # type: ignore[arg-type]
                full_expected_ids=tuple(full_expected_ids),
                partial_expected_ids=tuple(partial_expected_ids),
                no_match_expected_ids=tuple(
                    expected_id
                    for expected_id in expected_ids
                    if expected_id not in positive_by_expected
                ),
                root_cause_cluster_key=certificate.root_cause_cluster_key,
                report_text_evidence=(
                    _materialized_text_evidence(
                        report=report,
                        report_field=ReportField.CLAIM,
                        semantic_role=ReportTextEvidenceRole.CLAIM_BOUNDARY,
                        reason="The complete published claim is a mandatory part of the frozen validity envelope.",
                        basis=f"frozen_validity:{certificate.certificate_hash}",
                    ),
                    _materialized_text_evidence(
                        report=report,
                        report_field=ReportField.REASON,
                        semantic_role=(
                            ReportTextEvidenceRole.CAUSAL_SUPPORT
                            if reason_audit.verdict == CausalFieldVerdict.SUPPORTED
                            else ReportTextEvidenceRole.REFUTED_PREMISE
                        ),
                        reason="The complete published reason was audited before any expected issue became visible.",
                        basis=f"frozen_validity:{certificate.certificate_hash}",
                    ),
                ),
                causal_field_audits=certificate.field_audits,
                reason=f"{certificate.reason} {ownership_reason}",
                basis=(
                    f"{certificate.basis}; deterministic ownership from immutable core truth "
                    "and the exhaustive expected relation partition"
                ),
                source_refs=_unique(
                    [f"report:{report_id}"]
                    + list(certificate.source_refs)
                    + [f"expected:{expected_id}" for expected_id in expected_ids]
                ),
            )
        )

    relation_by_key = {(item.report_id, item.expected_id): item for item in relations}
    expected_assessments = []
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
        supported_ids = set(full_report_ids) | set(partial_report_ids)
        expected_assessments.append(
            ExpectedAssessment(
                expected_id=expected_id,
                full_report_ids=full_report_ids,
                partial_report_ids=partial_report_ids,
                no_support_report_ids=tuple(
                    report_id
                    for report_id in report_ids
                    if report_id not in supported_ids
                ),
                hit=bool(full_report_ids),
                supported=bool(supported_ids),
                reason=(
                    f"Expected issue {expected_id} has FULL support from {list(full_report_ids)} "
                    f"and PARTIAL support from {list(partial_report_ids)}; every remaining report is NO_MATCH."
                ),
                basis="Deterministic two-stage materialization from frozen validity and exhaustive relation closures.",
                source_refs=_unique(
                    [f"expected:{expected_id}"]
                    + [
                        ref
                        for report_id in report_ids
                        for ref in relation_by_key[(report_id, expected_id)].source_refs
                    ]
                ),
            )
        )
    return JudgeReading(
        relations=tuple(relations),
        report_assessments=tuple(report_assessments),
        expected_assessments=tuple(expected_assessments),
        reason="Expected-isolated validity certificates and relation-only responses were deterministically closed with no UNKNOWN.",
        basis="Frozen certificate hashes, exact expected positions, common artifacts, and issue #195 ownership formulas.",
        source_refs=_unique(
            [judge_input.artifact_closure.closure_hash]
            + [item.certificate_hash for item in certificates]
            + [
                ref
                for response in relation_responses
                for ref in response.relation_source_refs
            ]
        ),
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
