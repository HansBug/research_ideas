"""Two-stage executable path for expected-isolated validity and relation judging."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from pipeline.evidence_discovery.orchestration.runtime import (
    PublicStructuredRuntime,
    StructuredCallOutcome,
)

from .artifacts import stable_model_hash
from .metrics import compute_semantic_metrics, decode_outcomes
from .models import (
    AdapterAudit,
    ConflictKind,
    ConflictRecord,
    CoreClaimTruth,
    FrozenValidityCertificate,
    JudgeCallReceipt,
    JudgeReading,
    PairJudgeResult,
    ReadingDisagreement,
    RelationArbitrationInput,
    RelationResponse,
    RelationStageReading,
    RetryRecord,
    UnifiedJudgeInput,
    UsageReceipt,
    ValidityArbitrationInput,
    ValidityJudgeInput,
    ValidityStageReading,
)
from .protocol import (
    JUDGE_ALGORITHM_VERSION,
    JUDGE_MAX_OUTPUT_TOKENS,
    PROMPT_VERSION,
    PROTOCOL_SHA256,
    PROTOCOL_VERSION,
    RELATION_ARBITRATION_INSTRUCTION,
    RELATION_PRIMARY_INSTRUCTION,
    RELATION_SYSTEM_PROMPT,
    VALIDITY_ARBITRATION_INSTRUCTION,
    VALIDITY_PRIMARY_INSTRUCTION,
    VALIDITY_SYSTEM_PROMPT,
    prompt_hash,
)
from .schema import (
    build_exact_relation_model,
    build_exact_validity_model,
    build_relation_input,
    build_validity_input,
    materialize_two_stage_reading,
    materialize_validity_certificate,
    response_schema_hash,
)


class JudgeExecutionFailure(RuntimeError):
    """Terminal Judge failure carrying every call receipt produced before failure."""

    def __init__(
        self,
        message: str,
        call_receipts: tuple[JudgeCallReceipt, ...],
    ) -> None:
        super().__init__(message)
        self.call_receipts = call_receipts


def _stable_json(value: Any) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _sha256_text(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def build_validity_prompt(validity_input: ValidityJudgeInput) -> str:
    """Serialize one expected-isolated validity input with no ledger fields."""

    return (
        f"{VALIDITY_PRIMARY_INSTRUCTION}\n\n"
        "<validity_input>\n"
        f"{validity_input.model_dump_json(indent=2)}\n"
        "</validity_input>"
    )


def build_validity_arbitration_prompt(
    arbitration_input: ValidityArbitrationInput,
) -> str:
    """Serialize one expected-isolated validity conflict for fresh arbitration."""

    return (
        f"{VALIDITY_ARBITRATION_INSTRUCTION}\n\n"
        "<validity_arbitration_input>\n"
        f"{arbitration_input.model_dump_json(indent=2)}\n"
        "</validity_arbitration_input>"
    )


def build_relation_prompt(relation_input) -> str:
    """Serialize one relation-only input with an immutable VALID certificate."""

    return (
        f"{RELATION_PRIMARY_INSTRUCTION}\n\n"
        "<relation_input>\n"
        f"{relation_input.model_dump_json(indent=2)}\n"
        "</relation_input>"
    )


def build_relation_arbitration_prompt(
    arbitration_input: RelationArbitrationInput,
) -> str:
    """Serialize one relation-only conflict without reopening report validity."""

    return (
        f"{RELATION_ARBITRATION_INSTRUCTION}\n\n"
        "<relation_arbitration_input>\n"
        f"{arbitration_input.model_dump_json(indent=2)}\n"
        "</relation_arbitration_input>"
    )


def build_primary_prompt(
    judge_input: UnifiedJudgeInput, target_report_id: str | None = None
) -> str:
    """Compatibility serializer that now returns only expected-isolated validity input."""

    if target_report_id is None:
        if len(judge_input.reports) != 1:
            raise ValueError(
                "target_report_id is required when the Judge input has multiple reports"
            )
        target_report_id = judge_input.reports[0].report_id
    return build_validity_prompt(build_validity_input(judge_input, target_report_id))


def detect_validity_disagreements(
    certificate_1: FrozenValidityCertificate,
    certificate_2: FrozenValidityCertificate,
) -> tuple[ReadingDisagreement, ...]:
    """Compare aggregate truth and every fixed clause verdict, never prose wording."""

    if certificate_1.report_id != certificate_2.report_id:
        raise ValueError("validity certificates identify different reports")
    report_id = certificate_1.report_id
    disagreements = []
    if certificate_1.core_truth != certificate_2.core_truth:
        disagreements.append(
            ReadingDisagreement(
                kind=ConflictKind.CORE_TRUTH,
                object_ref=f"report:{report_id}",
                reading_1_value=certificate_1.core_truth.value,
                reading_2_value=certificate_2.core_truth.value,
            )
        )
    first_fields = {
        item.report_field.value: item for item in certificate_1.field_audits
    }
    second_fields = {
        item.report_field.value: item for item in certificate_2.field_audits
    }
    if set(first_fields) != set(second_fields):
        raise ValueError("validity certificate field closures differ")
    for field_name, first_field in first_fields.items():
        first_clauses = {
            item.clause_id: item for item in first_field.clause_audits
        }
        second_clauses = {
            item.clause_id: item for item in second_fields[field_name].clause_audits
        }
        if set(first_clauses) != set(second_clauses):
            raise ValueError("validity certificate clause closures differ")
        for clause_id, first_clause in first_clauses.items():
            first_value = first_clause.verdict.value
            second_value = second_clauses[clause_id].verdict.value
            if first_value != second_value:
                disagreements.append(
                    ReadingDisagreement(
                        kind=ConflictKind.VALIDITY_CLAUSE,
                        object_ref=(
                            f"report:{report_id}/field:{field_name}/clause:{clause_id}"
                        ),
                        reading_1_value=first_value,
                        reading_2_value=second_value,
                    )
                )
    return tuple(disagreements)


def detect_relation_disagreements(
    response_1: RelationResponse,
    response_2: RelationResponse,
) -> tuple[ReadingDisagreement, ...]:
    """Compare every exact relation enum while ignoring explanatory wording."""

    if response_1.report_id != response_2.report_id:
        raise ValueError("relation responses identify different reports")
    first = {item.expected_id: item for item in response_1.relation_decisions}
    second = {item.expected_id: item for item in response_2.relation_decisions}
    if set(first) != set(second):
        raise ValueError("relation response expected closures differ")
    return tuple(
        ReadingDisagreement(
            kind=ConflictKind.RELATION,
            object_ref=f"report:{response_1.report_id}/expected:{expected_id}",
            reading_1_value=first[expected_id].match.value,
            reading_2_value=second[expected_id].match.value,
        )
        for expected_id in first
        if first[expected_id].match != second[expected_id].match
    )


def _cache_tokens(row: dict[str, Any], key: str) -> int | None:
    details = row.get("input_token_details")
    if not isinstance(details, dict):
        return None
    value = details.get(key)
    return int(value) if isinstance(value, int) else None


def _call_receipt(
    *,
    call_id: str,
    phase: str,
    profile: str,
    schema_hash: str,
    actual_prompt_hash: str,
    outcome: StructuredCallOutcome[Any],
) -> JudgeCallReceipt:
    usage = tuple(
        UsageReceipt(
            model_call_id=(
                str(row["model_call_id"]) if row.get("model_call_id") else None
            ),
            status=str(row.get("status") or "unknown"),
            model=(str(row["model"]) if row.get("model") else None),
            input_tokens=(
                int(row["input_tokens"])
                if isinstance(row.get("input_tokens"), int)
                else None
            ),
            output_tokens=(
                int(row["output_tokens"])
                if isinstance(row.get("output_tokens"), int)
                else None
            ),
            cache_read_input_tokens=_cache_tokens(row, "cache_read"),
            cache_write_input_tokens=(
                _cache_tokens(row, "cache_creation")
                or _cache_tokens(row, "cache_write")
            ),
            cost_counted=bool(row.get("cost_counted", True)),
            billing_disposition=str(row.get("billing_disposition") or "unspecified"),
            raw_usage_json=_stable_json(row),
        )
        for row in outcome.usage
    )
    retries = []
    artifact_paths = []
    for outer_index, attempt in enumerate(outcome.attempts, start=1):
        error = attempt.get("error")
        error_mapping = error if isinstance(error, dict) else {}
        retries.append(
            RetryRecord(
                attempt_no=int(attempt.get("outer_attempt") or outer_index),
                status=str(attempt.get("status") or "unknown"),
                provider_error=bool(attempt.get("provider_error")),
                error_code=(
                    str(error_mapping.get("code") or error_mapping.get("type"))
                    if error_mapping
                    else None
                ),
                error_message=(
                    str(error_mapping.get("message"))
                    if error_mapping.get("message")
                    else None
                ),
                billing_disposition=str(
                    attempt.get("billing_disposition") or "unspecified"
                ),
                raw_attempt_json=_stable_json(attempt),
            )
        )
        for path_key in (
            "audit_path",
            "result_path",
            "schema_validation_failure_path",
        ):
            if attempt.get(path_key):
                artifact_paths.append(str(attempt[path_key]))
        for transport in attempt.get("retry_records") or ():
            transport_error = transport.get("error")
            transport_mapping = (
                transport_error if isinstance(transport_error, dict) else {}
            )
            retries.append(
                RetryRecord(
                    attempt_no=int(transport.get("attempt_no") or 1),
                    status=str(transport.get("operation") or "transport_retry"),
                    provider_error=bool(transport_mapping),
                    error_code=(
                        str(transport_mapping.get("type"))
                        if transport_mapping.get("type")
                        else None
                    ),
                    error_message=(
                        str(transport_mapping.get("message"))
                        if transport_mapping.get("message")
                        else None
                    ),
                    billing_disposition=(
                        "provider_error_retry_exempt"
                        if transport_mapping
                        else "transport_recovery"
                    ),
                    raw_attempt_json=_stable_json(transport),
                )
            )
    return JudgeCallReceipt(
        call_id=call_id,
        phase=phase,  # type: ignore[arg-type]
        status="success" if outcome.succeeded else "failed",
        profile=profile,
        schema_hash=schema_hash,
        prompt_hash=actual_prompt_hash,
        usage=usage,
        retries=tuple(retries),
        cost_usd=float(outcome.cost.get("total_usd") or 0.0),
        cost_eligible=bool(outcome.cost.get("eligible", False)),
        artifact_paths=tuple(dict.fromkeys(artifact_paths)),
        reason=outcome.reason,
        basis=outcome.basis,
    )


def _require_response(
    outcome: StructuredCallOutcome[Any], phase: str
) -> Any:
    if not outcome.succeeded or outcome.response is None:
        raise RuntimeError(
            f"semantic Judge {phase} failed after provider/schema handling: "
            f"{outcome.reason}; {outcome.basis}"
        )
    return outcome.response


def _reading_source_refs(certificates) -> tuple[str, ...]:
    refs = [
        ref
        for certificate in certificates
        for ref in certificate.source_refs
    ]
    return tuple(dict.fromkeys(refs)) or ("artifact:empty-report-closure",)


def _schema_set_hash(schema_hashes: dict[str, str]) -> str:
    return _sha256_text(
        json.dumps(schema_hashes, sort_keys=True, separators=(",", ":"))
    )


def _conflict_records(
    disagreements: tuple[ReadingDisagreement, ...],
    final_certificates: dict[str, FrozenValidityCertificate],
    final_reading: JudgeReading,
) -> tuple[ConflictRecord, ...]:
    records = []
    for disagreement in disagreements:
        report_part = disagreement.object_ref.split("/", 1)[0]
        report_id = report_part.removeprefix("report:")
        if disagreement.kind == ConflictKind.RELATION:
            expected_id = disagreement.object_ref.split("/expected:", 1)[1]
            row = next(
                item
                for item in final_reading.relations
                if item.report_id == report_id
                and item.expected_id == expected_id
            )
            final_value = row.match.value
            reason = row.reason
            basis = row.basis
            source_refs = row.source_refs
        elif disagreement.kind == ConflictKind.CORE_TRUTH:
            certificate = final_certificates[report_id]
            final_value = certificate.core_truth.value
            reason = certificate.reason
            basis = certificate.basis
            source_refs = certificate.source_refs
        else:
            _, field_part, clause_part = disagreement.object_ref.split("/")
            field_name = field_part.removeprefix("field:")
            clause_id = clause_part.removeprefix("clause:")
            certificate = final_certificates[report_id]
            field_audit = next(
                item
                for item in certificate.field_audits
                if item.report_field.value == field_name
            )
            clause = next(
                item
                for item in field_audit.clause_audits
                if item.clause_id == clause_id
            )
            final_value = clause.verdict.value
            reason = clause.reason
            basis = clause.basis
            source_refs = clause.source_refs
        records.append(
            ConflictRecord(
                kind=disagreement.kind,
                object_ref=disagreement.object_ref,
                reading_1_value=disagreement.reading_1_value,
                reading_2_value=disagreement.reading_2_value,
                final_value=final_value,
                reason=reason,
                basis=basis,
                source_refs=source_refs,
            )
        )
    return tuple(records)


def judge_pair(
    *,
    run_id: str,
    round_no: int,
    judge_input: UnifiedJudgeInput,
    adapter_audit: AdapterAudit,
    runtime: PublicStructuredRuntime,
    judge_code_commit: str,
) -> PairJudgeResult:
    """Run expected-isolated validity, freeze truth, then judge relations."""

    pair_id = judge_input.pair_id
    receipts = []
    schema_hashes = {}
    validity_inputs = {
        report.report_id: build_validity_input(judge_input, report.report_id)
        for report in judge_input.reports
    }

    def run_validity(reading_no: int) -> ValidityStageReading:
        certificates = []
        phase = f"validity_primary_{reading_no}"
        for report in judge_input.reports:
            report_id = report.report_id
            validity_input = validity_inputs[report_id]
            model = build_exact_validity_model(validity_input)
            model_hash = response_schema_hash(model)
            schema_hashes[f"{phase}:{report_id}"] = model_hash
            prompt = build_validity_prompt(validity_input)
            outcome = runtime.call(
                kind="semantic-judge-validity",
                schema=model,
                system_prompt=VALIDITY_SYSTEM_PROMPT,
                prompt=prompt,
                artifact_id=(
                    f"{pair_id}/round-{round_no}/validity-primary-{reading_no}-{report_id}"
                ),
                retry_cell_on_provider_error=True,
                max_output_tokens=min(
                    JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
                ),
            )
            receipts.append(
                _call_receipt(
                    call_id=f"{pair_id}:r{round_no}:{phase}:{report_id}",
                    phase=phase,
                    profile=runtime.profile,
                    schema_hash=model_hash,
                    actual_prompt_hash=_sha256_text(
                        VALIDITY_SYSTEM_PROMPT + "\n" + prompt
                    ),
                    outcome=outcome,
                )
            )
            response = _require_response(outcome, f"{phase}_{report_id}")
            certificates.append(
                materialize_validity_certificate(response, validity_input)
            )
        return ValidityStageReading(
            certificates=tuple(certificates),
            reason="Every report received one complete expected-isolated validity reading.",
            basis="Fixed report-field slots, exact source-clause closure, and complete common artifacts.",
            source_refs=_reading_source_refs(certificates),
        )

    try:
        validity_reading_1 = run_validity(1)
        validity_reading_2 = run_validity(2)
        validity_1_by_id = {
            item.report_id: item for item in validity_reading_1.certificates
        }
        validity_2_by_id = {
            item.report_id: item for item in validity_reading_2.certificates
        }
        validity_disagreements = tuple(
            disagreement
            for report in judge_input.reports
            for disagreement in detect_validity_disagreements(
                validity_1_by_id[report.report_id],
                validity_2_by_id[report.report_id],
            )
        )
        validity_arbitrations = []
        final_certificates = dict(validity_1_by_id)
        conflicted_validity_ids = tuple(
            dict.fromkeys(
                item.object_ref.split("/", 1)[0].removeprefix("report:")
                for item in validity_disagreements
            )
        )
        for report_id in conflicted_validity_ids:
            disagreements = tuple(
                item
                for item in validity_disagreements
                if item.object_ref.startswith(f"report:{report_id}")
            )
            arbitration_input = ValidityArbitrationInput(
                validity_input=validity_inputs[report_id],
                primary_certificate_1=validity_1_by_id[report_id],
                primary_certificate_2=validity_2_by_id[report_id],
                disagreements=disagreements,
                reason="Substantive clause or aggregate truth values conflict and require a fresh expected-isolated reading.",
                basis=f"{JUDGE_ALGORITHM_VERSION}; exact validity enum comparison",
            )
            model = build_exact_validity_model(validity_inputs[report_id])
            model_hash = response_schema_hash(model)
            schema_hashes[f"validity_arbitration:{report_id}"] = model_hash
            prompt = build_validity_arbitration_prompt(arbitration_input)
            outcome = runtime.call(
                kind="semantic-judge-validity-arbitration",
                schema=model,
                system_prompt=VALIDITY_SYSTEM_PROMPT,
                prompt=prompt,
                artifact_id=(
                    f"{pair_id}/round-{round_no}/validity-arbitration-{report_id}"
                ),
                retry_cell_on_provider_error=True,
                max_output_tokens=min(
                    JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
                ),
            )
            receipts.append(
                _call_receipt(
                    call_id=(
                        f"{pair_id}:r{round_no}:validity_arbitration:{report_id}"
                    ),
                    phase="validity_arbitration",
                    profile=runtime.profile,
                    schema_hash=model_hash,
                    actual_prompt_hash=_sha256_text(
                        VALIDITY_SYSTEM_PROMPT + "\n" + prompt
                    ),
                    outcome=outcome,
                )
            )
            response = _require_response(
                outcome, f"validity_arbitration_{report_id}"
            )
            certificate = materialize_validity_certificate(
                response, validity_inputs[report_id]
            )
            validity_arbitrations.append(certificate)
            final_certificates[report_id] = certificate
        ordered_certificates = tuple(
            final_certificates[report.report_id] for report in judge_input.reports
        )

        relation_inputs = {
            certificate.report_id: build_relation_input(judge_input, certificate)
            for certificate in ordered_certificates
            if certificate.core_truth == CoreClaimTruth.VALID
        }
        invalid_ids = tuple(
            certificate.report_id
            for certificate in ordered_certificates
            if certificate.core_truth == CoreClaimTruth.INVALID
        )

        def run_relations(reading_no: int) -> RelationStageReading:
            responses = []
            phase = f"relation_primary_{reading_no}"
            for report in judge_input.reports:
                relation_input = relation_inputs.get(report.report_id)
                if relation_input is None:
                    continue
                model = build_exact_relation_model(relation_input)
                model_hash = response_schema_hash(model)
                schema_hashes[f"{phase}:{report.report_id}"] = model_hash
                prompt = build_relation_prompt(relation_input)
                outcome = runtime.call(
                    kind="semantic-judge-relation",
                    schema=model,
                    system_prompt=RELATION_SYSTEM_PROMPT,
                    prompt=prompt,
                    artifact_id=(
                        f"{pair_id}/round-{round_no}/relation-primary-{reading_no}-{report.report_id}"
                    ),
                    retry_cell_on_provider_error=True,
                    max_output_tokens=min(
                        JUDGE_MAX_OUTPUT_TOKENS,
                        runtime.config.max_output_tokens,
                    ),
                )
                receipts.append(
                    _call_receipt(
                        call_id=(
                            f"{pair_id}:r{round_no}:{phase}:{report.report_id}"
                        ),
                        phase=phase,
                        profile=runtime.profile,
                        schema_hash=model_hash,
                        actual_prompt_hash=_sha256_text(
                            RELATION_SYSTEM_PROMPT + "\n" + prompt
                        ),
                        outcome=outcome,
                    )
                )
                exact_response = _require_response(
                    outcome, f"{phase}_{report.report_id}"
                )
                responses.append(
                    RelationResponse.model_validate(
                        exact_response.model_dump(mode="json")
                    )
                )
            return RelationStageReading(
                responses=tuple(responses),
                backend_invalid_report_ids=invalid_ids,
                reason="Every frozen-valid report received one complete relation reading; invalid reports remain backend-owned all-NO closures.",
                basis="Immutable validity certificates, every expected position, and the unchanged common artifacts.",
                source_refs=tuple(
                    dict.fromkeys(
                        [
                            certificate.certificate_hash
                            for certificate in ordered_certificates
                        ]
                        + [
                            ref
                            for response in responses
                            for ref in response.relation_source_refs
                        ]
                    )
                )
                or (judge_input.artifact_closure.closure_hash,),
            )

        relation_reading_1 = run_relations(1)
        relation_reading_2 = run_relations(2)
        relation_1_by_id = {
            item.report_id: item for item in relation_reading_1.responses
        }
        relation_2_by_id = {
            item.report_id: item for item in relation_reading_2.responses
        }
        relation_disagreements = tuple(
            disagreement
            for report_id in relation_1_by_id
            for disagreement in detect_relation_disagreements(
                relation_1_by_id[report_id], relation_2_by_id[report_id]
            )
        )
        relation_arbitrations = []
        final_relation_responses = dict(relation_1_by_id)
        conflicted_relation_ids = tuple(
            dict.fromkeys(
                item.object_ref.split("/", 1)[0].removeprefix("report:")
                for item in relation_disagreements
            )
        )
        for report_id in conflicted_relation_ids:
            disagreements = tuple(
                item
                for item in relation_disagreements
                if item.object_ref.startswith(f"report:{report_id}/")
            )
            arbitration_input = RelationArbitrationInput(
                relation_input=relation_inputs[report_id],
                primary_response_1=relation_1_by_id[report_id],
                primary_response_2=relation_2_by_id[report_id],
                disagreements=disagreements,
                reason="Substantive FULL, PARTIAL, or NO enums conflict and require a fresh relation-only reading.",
                basis=f"{JUDGE_ALGORITHM_VERSION}; immutable validity certificate and exact relation comparison",
            )
            model = build_exact_relation_model(relation_inputs[report_id])
            model_hash = response_schema_hash(model)
            schema_hashes[f"relation_arbitration:{report_id}"] = model_hash
            prompt = build_relation_arbitration_prompt(arbitration_input)
            outcome = runtime.call(
                kind="semantic-judge-relation-arbitration",
                schema=model,
                system_prompt=RELATION_SYSTEM_PROMPT,
                prompt=prompt,
                artifact_id=(
                    f"{pair_id}/round-{round_no}/relation-arbitration-{report_id}"
                ),
                retry_cell_on_provider_error=True,
                max_output_tokens=min(
                    JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
                ),
            )
            receipts.append(
                _call_receipt(
                    call_id=(
                        f"{pair_id}:r{round_no}:relation_arbitration:{report_id}"
                    ),
                    phase="relation_arbitration",
                    profile=runtime.profile,
                    schema_hash=model_hash,
                    actual_prompt_hash=_sha256_text(
                        RELATION_SYSTEM_PROMPT + "\n" + prompt
                    ),
                    outcome=outcome,
                )
            )
            exact_response = _require_response(
                outcome, f"relation_arbitration_{report_id}"
            )
            response = RelationResponse.model_validate(
                exact_response.model_dump(mode="json")
            )
            relation_arbitrations.append(response)
            final_relation_responses[report_id] = response
        ordered_relation_responses = tuple(
            final_relation_responses[report.report_id]
            for report in judge_input.reports
            if report.report_id in final_relation_responses
        )
        final_reading = materialize_two_stage_reading(
            ordered_certificates,
            ordered_relation_responses,
            judge_input,
        )
    except Exception as exc:
        raise JudgeExecutionFailure(str(exc), tuple(receipts)) from exc

    disagreements = validity_disagreements + relation_disagreements
    conflicts = _conflict_records(
        disagreements, final_certificates, final_reading
    )
    report_outcomes, expected_outcomes = decode_outcomes(
        final_reading, adapter_audit
    )
    metrics = compute_semantic_metrics(final_reading)
    return PairJudgeResult(
        run_id=run_id,
        pair_id=pair_id,
        round=round_no,
        protocol_version=PROTOCOL_VERSION,
        protocol_sha256=PROTOCOL_SHA256,
        judge_algorithm_version=JUDGE_ALGORITHM_VERSION,
        judge_code_commit=judge_code_commit,
        model_profile=runtime.profile,
        artifact_closure_hash=judge_input.artifact_closure.closure_hash,
        serialized_input_hash=stable_model_hash(judge_input),
        response_schema_hash=_schema_set_hash(schema_hashes),
        prompt_template_hash=prompt_hash(),
        adapter_audit=adapter_audit,
        validity_reading_1=validity_reading_1,
        validity_reading_2=validity_reading_2,
        validity_arbitration_certificates=tuple(validity_arbitrations),
        relation_reading_1=relation_reading_1,
        relation_reading_2=relation_reading_2,
        relation_arbitration_responses=tuple(relation_arbitrations),
        conflicts=conflicts,
        final_reading=final_reading,
        report_outcomes=report_outcomes,
        expected_outcomes=expected_outcomes,
        metrics=metrics,
        call_receipts=tuple(receipts),
        reason=(
            "Two expected-isolated validity readings and two relation-only readings completed; "
            f"{len(validity_disagreements)} validity and {len(relation_disagreements)} relation disagreements were fully arbitrated."
        ),
        basis=(
            f"{PROTOCOL_VERSION}; {JUDGE_ALGORITHM_VERSION}; {PROMPT_VERSION}; "
            "fixed clause closure, immutable validity certificates, exact relation closure, and deterministic issue #195 metrics"
        ),
    )
