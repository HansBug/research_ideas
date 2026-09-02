"""Two-stage executable path for expected-isolated validity and relation judging."""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel

from utils.structured_runtime import (
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
    RelationBatchArbitrationInput,
    RelationBatchJudgeInput,
    RelationResponse,
    RelationStageReading,
    RetryRecord,
    UnifiedJudgeInput,
    UsageReceipt,
    ValidityArbitrationInput,
    ValidityBatchArbitrationInput,
    ValidityBatchJudgeInput,
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
    build_exact_relation_batch_model,
    build_exact_validity_batch_model,
    build_relation_batch_input,
    build_validity_batch_input,
    build_validity_input,
    materialize_two_stage_reading,
    materialize_validity_certificate,
    relation_batch_responses,
    response_schema_hash,
    validity_batch_responses,
    validity_item_input,
)

MAX_REPORTS_PER_BATCH = 8
MAX_ESTIMATED_BATCH_OUTPUT_TOKENS = 18_000


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


def build_validity_batch_prompt(validity_input: ValidityBatchJudgeInput) -> str:
    """Serialize a bounded expected-isolated batch with one artifact closure."""

    return (
        f"{VALIDITY_PRIMARY_INSTRUCTION}\n\n"
        "<validity_batch_input>\n"
        f"{validity_input.model_dump_json(indent=2)}\n"
        "</validity_batch_input>"
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


def build_validity_batch_arbitration_prompt(
    arbitration_input: ValidityBatchArbitrationInput,
) -> str:
    """Serialize all validity conflicts in one expected-isolated batch."""

    return (
        f"{VALIDITY_ARBITRATION_INSTRUCTION}\n\n"
        "<validity_batch_arbitration_input>\n"
        f"{arbitration_input.model_dump_json(indent=2)}\n"
        "</validity_batch_arbitration_input>"
    )


def build_relation_prompt(relation_input) -> str:
    """Serialize one relation-only input with an immutable VALID certificate."""

    return (
        f"{RELATION_PRIMARY_INSTRUCTION}\n\n"
        "<relation_input>\n"
        f"{relation_input.model_dump_json(indent=2)}\n"
        "</relation_input>"
    )


def build_relation_batch_prompt(relation_input: RelationBatchJudgeInput) -> str:
    """Serialize a bounded report-by-expected matrix with shared artifacts."""

    return (
        f"{RELATION_PRIMARY_INSTRUCTION}\n\n"
        "<relation_batch_input>\n"
        f"{relation_input.model_dump_json(indent=2)}\n"
        "</relation_batch_input>"
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


def build_relation_batch_arbitration_prompt(
    arbitration_input: RelationBatchArbitrationInput,
) -> str:
    """Serialize all relation conflicts in one immutable-validity batch."""

    return (
        f"{RELATION_ARBITRATION_INSTRUCTION}\n\n"
        "<relation_batch_arbitration_input>\n"
        f"{arbitration_input.model_dump_json(indent=2)}\n"
        "</relation_batch_arbitration_input>"
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
    """Compare aggregate truth, hard gates, and each fixed clause role/verdict."""

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
    first_class = certificate_1.defect_adjudication.defect_class
    second_class = certificate_2.defect_adjudication.defect_class
    if first_class != second_class:
        disagreements.append(
            ReadingDisagreement(
                kind=ConflictKind.DEFECT_CLASS,
                object_ref=f"report:{report_id}/defect_class",
                reading_1_value=first_class.value,
                reading_2_value=second_class.value,
            )
        )
    gates = (
        ("core_claim", certificate_1.core_claim_gate, certificate_2.core_claim_gate),
        (
            "indispensable_mechanism",
            certificate_1.indispensable_mechanism_gate,
            certificate_2.indispensable_mechanism_gate,
        ),
        (
            "minimum_evidence",
            certificate_1.minimum_evidence_gate,
            certificate_2.minimum_evidence_gate,
        ),
    )
    for gate_name, first_gate, second_gate in gates:
        if first_gate.status != second_gate.status:
            disagreements.append(
                ReadingDisagreement(
                    kind=ConflictKind.VALIDITY_GATE,
                    object_ref=f"report:{report_id}/gate:{gate_name}",
                    reading_1_value=first_gate.status.value,
                    reading_2_value=second_gate.status.value,
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
        first_clauses = {item.clause_id: item for item in first_field.clause_audits}
        second_clauses = {
            item.clause_id: item for item in second_fields[field_name].clause_audits
        }
        if set(first_clauses) != set(second_clauses):
            raise ValueError("validity certificate clause closures differ")
        for clause_id, first_clause in first_clauses.items():
            first_value = (
                f"{first_clause.validity_role.value}:{first_clause.verdict.value}"
            )
            second_clause = second_clauses[clause_id]
            second_value = (
                f"{second_clause.validity_role.value}:{second_clause.verdict.value}"
            )
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
    pair_id: str,
    batch_id: str,
    report_ids: tuple[str, ...],
    phase: str,
    profile: str,
    schema_hash: str,
    actual_prompt_hash: str,
    outcome: StructuredCallOutcome[Any],
) -> JudgeCallReceipt:
    outcome_result = getattr(outcome, "result", {})
    dispatch = outcome_result.get("dispatch", {}) if outcome_result else {}
    fallback_time = datetime.now(timezone.utc).isoformat()
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
        pair_id=pair_id,
        batch_id=batch_id,
        report_ids=report_ids,
        phase=phase,  # type: ignore[arg-type]
        status="success" if outcome.succeeded else "failed",
        process_id=int(dispatch.get("process_id") or os.getpid()),
        started_at_utc=str(dispatch.get("started_at_utc") or fallback_time),
        ended_at_utc=str(dispatch.get("ended_at_utc") or fallback_time),
        duration_seconds=float(dispatch.get("duration_seconds") or 0.0),
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


def _require_response(outcome: StructuredCallOutcome[Any], phase: str) -> Any:
    if not outcome.succeeded or outcome.response is None:
        raise RuntimeError(
            f"semantic Judge {phase} failed after provider/schema handling: "
            f"{outcome.reason}; {outcome.basis}"
        )
    return outcome.response


def _reading_source_refs(certificates) -> tuple[str, ...]:
    refs = [ref for certificate in certificates for ref in certificate.source_refs]
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
                if item.report_id == report_id and item.expected_id == expected_id
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
        elif disagreement.kind == ConflictKind.DEFECT_CLASS:
            certificate = final_certificates[report_id]
            final_value = certificate.defect_adjudication.defect_class.value
            reason = certificate.defect_adjudication.reason
            basis = certificate.defect_adjudication.basis
            source_refs = certificate.defect_adjudication.source_refs
        elif disagreement.kind == ConflictKind.VALIDITY_GATE:
            gate_name = disagreement.object_ref.split("/gate:", 1)[1]
            certificate = final_certificates[report_id]
            gate = {
                "core_claim": certificate.core_claim_gate,
                "indispensable_mechanism": (certificate.indispensable_mechanism_gate),
                "minimum_evidence": certificate.minimum_evidence_gate,
            }[gate_name]
            final_value = gate.status.value
            reason = gate.reason
            basis = gate.basis
            source_refs = gate.source_refs
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
            final_value = f"{clause.validity_role.value}:{clause.verdict.value}"
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


@dataclass(frozen=True)
class _BatchCallPlan:
    """Internal immutable call plan; all provider-facing data remains Pydantic."""

    batch_id: str
    phase: str
    reading_no: int | None
    report_ids: tuple[str, ...]
    batch_input: BaseModel
    schema: type[BaseModel]
    kind: str
    system_prompt: str
    prompt: str
    artifact_id: str

    def runtime_call(self, max_output_tokens: int) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "schema": self.schema,
            "system_prompt": self.system_prompt,
            "prompt": self.prompt,
            "artifact_id": self.artifact_id,
            "retry_cell_on_provider_error": True,
            "max_output_tokens": max_output_tokens,
        }


def _stable_batch_id(prefix: str, index: int, report_ids: tuple[str, ...]) -> str:
    digest = hashlib.sha256("|".join(report_ids).encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{index:02d}-{digest}"


def _bounded_groups(
    rows: tuple[Any, ...], estimate_tokens
) -> tuple[tuple[Any, ...], ...]:
    """Split in stable order using report-count and conservative output budgets."""

    groups: list[tuple[Any, ...]] = []
    current: list[Any] = []
    current_tokens = 0
    for row in rows:
        estimate = int(estimate_tokens(row))
        if current and (
            len(current) >= MAX_REPORTS_PER_BATCH
            or current_tokens + estimate > MAX_ESTIMATED_BATCH_OUTPUT_TOKENS
        ):
            groups.append(tuple(current))
            current = []
            current_tokens = 0
        current.append(row)
        current_tokens += estimate
    if current:
        groups.append(tuple(current))
    return tuple(groups)


def _validity_report_groups(
    judge_input: UnifiedJudgeInput, report_ids: tuple[str, ...] | None = None
) -> tuple[tuple[str, ...], ...]:
    ids = report_ids or tuple(item.report_id for item in judge_input.reports)
    atomic = {
        report_id: build_validity_input(judge_input, report_id) for report_id in ids
    }

    def estimate(report_id: str) -> int:
        envelope = atomic[report_id].core_envelope
        clause_count = sum(len(item.clauses) for item in envelope.field_plans)
        field_count = len(envelope.field_plans)
        # The exact v6 response envelope is approximately 120-140 tokens per
        # clause on the real fixed-six inputs. Keep explicit headroom without
        # doubling that envelope and forcing three- or four-report batches.
        return 350 + clause_count * 155 + field_count * 45

    return _bounded_groups(ids, estimate)


def _relation_certificate_groups(
    certificates: tuple[FrozenValidityCertificate, ...], expected_count: int
) -> tuple[tuple[FrozenValidityCertificate, ...], ...]:
    return _bounded_groups(
        certificates,
        lambda _certificate: 450 + expected_count * 190,
    )


def _call_many(runtime, plans: tuple[_BatchCallPlan, ...], max_tokens: int):
    calls = tuple(plan.runtime_call(max_tokens) for plan in plans)
    if hasattr(runtime, "call_many"):
        return runtime.call_many(calls)
    return tuple(runtime.call(**call) for call in calls)


def _execute_with_split(
    *,
    runtime,
    initial_plans: tuple[_BatchCallPlan, ...],
    split_plan,
    receipts: list[JudgeCallReceipt],
    schema_hashes: dict[str, str],
    pair_id: str,
    round_no: int,
) -> tuple[tuple[_BatchCallPlan, Any], ...]:
    """Keep successful batches and deterministically split only failed batches."""

    completed: list[tuple[_BatchCallPlan, Any]] = []
    pending = initial_plans
    max_tokens = min(JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens)
    while pending:
        outcomes = _call_many(runtime, pending, max_tokens)
        retry_plans: list[_BatchCallPlan] = []
        for plan, outcome in zip(pending, outcomes, strict=True):
            model_hash = response_schema_hash(plan.schema)
            schema_hashes[f"{plan.phase}:{plan.batch_id}"] = model_hash
            receipts.append(
                _call_receipt(
                    call_id=f"{pair_id}:r{round_no}:{plan.phase}:{plan.batch_id}",
                    pair_id=pair_id,
                    batch_id=plan.batch_id,
                    report_ids=plan.report_ids,
                    phase=plan.phase,
                    profile=runtime.profile,
                    schema_hash=model_hash,
                    actual_prompt_hash=_sha256_text(
                        plan.system_prompt + "\n" + plan.prompt
                    ),
                    outcome=outcome,
                )
            )
            if outcome.succeeded:
                completed.append((plan, outcome))
                continue
            if len(plan.report_ids) == 1:
                _require_response(outcome, f"{plan.phase}_{plan.batch_id}")
            midpoint = len(plan.report_ids) // 2
            child_sets = (
                plan.report_ids[:midpoint],
                plan.report_ids[midpoint:],
            )
            retry_plans.extend(
                split_plan(plan, child_ids, child_index)
                for child_index, child_ids in enumerate(child_sets, start=1)
            )
        pending = tuple(retry_plans)
    return tuple(completed)


def judge_pair(
    *,
    run_id: str,
    round_no: int,
    judge_input: UnifiedJudgeInput,
    adapter_audit: AdapterAudit,
    runtime: PublicStructuredRuntime,
    judge_code_commit: str,
) -> PairJudgeResult:
    """Run bounded dual-reading batches, freeze truth, then batch relations."""

    pair_id = judge_input.pair_id
    receipts: list[JudgeCallReceipt] = []
    schema_hashes: dict[str, str] = {}

    def make_validity_primary(
        report_ids: tuple[str, ...], reading_no: int, batch_id: str
    ) -> _BatchCallPlan:
        batch_input = build_validity_batch_input(
            judge_input, report_ids, batch_id=batch_id
        )
        model = build_exact_validity_batch_model(batch_input)
        prompt = build_validity_batch_prompt(batch_input)
        phase = f"validity_primary_{reading_no}"
        return _BatchCallPlan(
            batch_id=batch_id,
            phase=phase,
            reading_no=reading_no,
            report_ids=report_ids,
            batch_input=batch_input,
            schema=model,
            kind="semantic-judge-validity-batch",
            system_prompt=VALIDITY_SYSTEM_PROMPT,
            prompt=prompt,
            artifact_id=(f"{pair_id}/round-{round_no}/{phase}-{batch_id}"),
        )

    try:
        validity_groups = _validity_report_groups(judge_input)
        validity_primary_plans = tuple(
            make_validity_primary(
                report_ids,
                reading_no,
                _stable_batch_id("VB", index, report_ids),
            )
            for index, report_ids in enumerate(validity_groups, start=1)
            for reading_no in (1, 2)
        )

        def split_validity_primary(
            plan: _BatchCallPlan,
            child_ids: tuple[str, ...],
            child_index: int,
        ) -> _BatchCallPlan:
            return make_validity_primary(
                child_ids,
                int(plan.reading_no or 1),
                f"{plan.batch_id}.s{child_index}",
            )

        validity_completed = _execute_with_split(
            runtime=runtime,
            initial_plans=validity_primary_plans,
            split_plan=split_validity_primary,
            receipts=receipts,
            schema_hashes=schema_hashes,
            pair_id=pair_id,
            round_no=round_no,
        )
        validity_maps: dict[int, dict[str, FrozenValidityCertificate]] = {
            1: {},
            2: {},
        }
        for plan, outcome in validity_completed:
            response = _require_response(outcome, f"{plan.phase}_{plan.batch_id}")
            batch_input = ValidityBatchJudgeInput.model_validate(plan.batch_input)
            rows = validity_batch_responses(response, batch_input)
            for index, row in enumerate(rows):
                certificate = materialize_validity_certificate(
                    row, validity_item_input(batch_input, index)
                )
                validity_maps[int(plan.reading_no or 1)][certificate.report_id] = (
                    certificate
                )
        report_order = tuple(item.report_id for item in judge_input.reports)
        if any(
            set(validity_maps[reading_no]) != set(report_order) for reading_no in (1, 2)
        ):
            raise ValueError("validity batch materialization did not close all reports")
        validity_reading_1 = ValidityStageReading(
            certificates=tuple(validity_maps[1][item] for item in report_order),
            reason="Every report received one complete independent expected-isolated batch reading.",
            basis="Shared common artifacts, fixed report slots, and exact source-clause closure.",
            source_refs=_reading_source_refs(validity_maps[1].values()),
        )
        validity_reading_2 = ValidityStageReading(
            certificates=tuple(validity_maps[2][item] for item in report_order),
            reason="Every report received a second complete independent expected-isolated batch reading.",
            basis="The same immutable batch inputs, shared common artifacts, and exact source-clause closure.",
            source_refs=_reading_source_refs(validity_maps[2].values()),
        )
        validity_1_by_id = validity_maps[1]
        validity_2_by_id = validity_maps[2]
        validity_disagreements = tuple(
            disagreement
            for report_id in report_order
            for disagreement in detect_validity_disagreements(
                validity_1_by_id[report_id], validity_2_by_id[report_id]
            )
        )
        final_certificates = dict(validity_1_by_id)
        conflicted_validity_ids = tuple(
            report_id
            for report_id in report_order
            if any(
                item.object_ref.startswith(f"report:{report_id}")
                for item in validity_disagreements
            )
        )

        def make_validity_arbitration(
            report_ids: tuple[str, ...], batch_id: str
        ) -> _BatchCallPlan:
            batch_input = build_validity_batch_input(
                judge_input, report_ids, batch_id=batch_id
            )
            arbitration_input = ValidityBatchArbitrationInput(
                validity_input=batch_input,
                primary_certificates_1=tuple(
                    validity_1_by_id[item] for item in report_ids
                ),
                primary_certificates_2=tuple(
                    validity_2_by_id[item] for item in report_ids
                ),
                disagreements=tuple(
                    item
                    for item in validity_disagreements
                    if any(
                        item.object_ref.startswith(f"report:{report_id}")
                        for report_id in report_ids
                    )
                ),
                reason="All substantive validity conflicts in this batch require a fresh expected-isolated reading.",
                basis=f"{JUDGE_ALGORITHM_VERSION}; exact validity enum comparison",
            )
            model = build_exact_validity_batch_model(batch_input)
            return _BatchCallPlan(
                batch_id=batch_id,
                phase="validity_arbitration",
                reading_no=None,
                report_ids=report_ids,
                batch_input=batch_input,
                schema=model,
                kind="semantic-judge-validity-arbitration-batch",
                system_prompt=VALIDITY_SYSTEM_PROMPT,
                prompt=build_validity_batch_arbitration_prompt(arbitration_input),
                artifact_id=(
                    f"{pair_id}/round-{round_no}/validity-arbitration-{batch_id}"
                ),
            )

        validity_arbitrations: list[FrozenValidityCertificate] = []
        if conflicted_validity_ids:
            arbitration_groups = _validity_report_groups(
                judge_input, conflicted_validity_ids
            )
            plans = tuple(
                make_validity_arbitration(ids, _stable_batch_id("VA", index, ids))
                for index, ids in enumerate(arbitration_groups, start=1)
            )

            def split_validity_arbitration(
                plan: _BatchCallPlan,
                child_ids: tuple[str, ...],
                child_index: int,
            ) -> _BatchCallPlan:
                return make_validity_arbitration(
                    child_ids, f"{plan.batch_id}.s{child_index}"
                )

            completed = _execute_with_split(
                runtime=runtime,
                initial_plans=plans,
                split_plan=split_validity_arbitration,
                receipts=receipts,
                schema_hashes=schema_hashes,
                pair_id=pair_id,
                round_no=round_no,
            )
            arbitration_by_id = {}
            for plan, outcome in completed:
                response = _require_response(
                    outcome, f"validity_arbitration_{plan.batch_id}"
                )
                batch_input = ValidityBatchJudgeInput.model_validate(plan.batch_input)
                for index, row in enumerate(
                    validity_batch_responses(response, batch_input)
                ):
                    certificate = materialize_validity_certificate(
                        row, validity_item_input(batch_input, index)
                    )
                    arbitration_by_id[certificate.report_id] = certificate
            validity_arbitrations = [
                arbitration_by_id[item] for item in conflicted_validity_ids
            ]
            final_certificates.update(arbitration_by_id)

        ordered_certificates = tuple(final_certificates[item] for item in report_order)
        invalid_ids = tuple(
            item.report_id
            for item in ordered_certificates
            if item.core_truth == CoreClaimTruth.INVALID
        )
        valid_certificates = tuple(
            item
            for item in ordered_certificates
            if item.core_truth == CoreClaimTruth.VALID
        )

        def make_relation_primary(
            certificates: tuple[FrozenValidityCertificate, ...],
            reading_no: int,
            batch_id: str,
        ) -> _BatchCallPlan:
            batch_input = build_relation_batch_input(
                judge_input, certificates, batch_id=batch_id
            )
            model = build_exact_relation_batch_model(batch_input)
            phase = f"relation_primary_{reading_no}"
            return _BatchCallPlan(
                batch_id=batch_id,
                phase=phase,
                reading_no=reading_no,
                report_ids=tuple(item.report_id for item in certificates),
                batch_input=batch_input,
                schema=model,
                kind="semantic-judge-relation-batch",
                system_prompt=RELATION_SYSTEM_PROMPT,
                prompt=build_relation_batch_prompt(batch_input),
                artifact_id=f"{pair_id}/round-{round_no}/{phase}-{batch_id}",
            )

        relation_maps: dict[int, dict[str, RelationResponse]] = {1: {}, 2: {}}
        if valid_certificates and judge_input.expected_issues:
            relation_groups = _relation_certificate_groups(
                valid_certificates, len(judge_input.expected_issues)
            )
            relation_plans = tuple(
                make_relation_primary(
                    certificates,
                    reading_no,
                    _stable_batch_id(
                        "RB",
                        index,
                        tuple(item.report_id for item in certificates),
                    ),
                )
                for index, certificates in enumerate(relation_groups, start=1)
                for reading_no in (1, 2)
            )

            certificate_by_id = {item.report_id: item for item in valid_certificates}

            def split_relation_primary(
                plan: _BatchCallPlan,
                child_ids: tuple[str, ...],
                child_index: int,
            ) -> _BatchCallPlan:
                return make_relation_primary(
                    tuple(certificate_by_id[item] for item in child_ids),
                    int(plan.reading_no or 1),
                    f"{plan.batch_id}.s{child_index}",
                )

            completed = _execute_with_split(
                runtime=runtime,
                initial_plans=relation_plans,
                split_plan=split_relation_primary,
                receipts=receipts,
                schema_hashes=schema_hashes,
                pair_id=pair_id,
                round_no=round_no,
            )
            for plan, outcome in completed:
                response = _require_response(outcome, f"{plan.phase}_{plan.batch_id}")
                batch_input = RelationBatchJudgeInput.model_validate(plan.batch_input)
                for row in relation_batch_responses(response, batch_input):
                    materialized = RelationResponse.model_validate(
                        row.model_dump(mode="json")
                    )
                    relation_maps[int(plan.reading_no or 1)][materialized.report_id] = (
                        materialized
                    )

        expected_valid_ids = (
            {item.report_id for item in valid_certificates}
            if judge_input.expected_issues
            else set()
        )
        if any(
            set(relation_maps[reading_no]) != expected_valid_ids
            for reading_no in (1, 2)
        ):
            raise ValueError(
                "relation batch materialization did not close all VALID reports"
            )

        def relation_stage(reading_no: int) -> RelationStageReading:
            responses = tuple(
                relation_maps[reading_no][item]
                for item in report_order
                if item in relation_maps[reading_no]
            )
            empty_denominator = not judge_input.expected_issues
            return RelationStageReading(
                responses=responses,
                backend_invalid_report_ids=invalid_ids,
                reason=(
                    "The expected denominator is empty, so no relation model call is required."
                    if empty_denominator
                    else "Every frozen-valid report received one complete batched relation reading; invalid reports remained backend-owned all-NO closures."
                ),
                basis=(
                    "Immutable validity certificates and the explicit empty expected denominator."
                    if empty_denominator
                    else "Shared expected and artifact closures with one exact report-by-expected matrix."
                ),
                source_refs=tuple(
                    dict.fromkeys(
                        [item.certificate_hash for item in ordered_certificates]
                        + [
                            ref
                            for response in responses
                            for ref in response.relation_source_refs
                        ]
                    )
                )
                or (judge_input.artifact_closure.closure_hash,),
            )

        relation_reading_1 = relation_stage(1)
        relation_reading_2 = relation_stage(2)
        relation_1_by_id = relation_maps[1]
        relation_2_by_id = relation_maps[2]
        relation_disagreements = tuple(
            disagreement
            for report_id in report_order
            if report_id in relation_1_by_id
            for disagreement in detect_relation_disagreements(
                relation_1_by_id[report_id], relation_2_by_id[report_id]
            )
        )
        conflicted_relation_ids = tuple(
            report_id
            for report_id in report_order
            if any(
                item.object_ref.startswith(f"report:{report_id}/")
                for item in relation_disagreements
            )
        )
        final_relation_responses = dict(relation_1_by_id)
        relation_arbitrations: list[RelationResponse] = []

        if conflicted_relation_ids:
            certificate_by_id = {item.report_id: item for item in valid_certificates}

            def make_relation_arbitration(
                report_ids: tuple[str, ...], batch_id: str
            ) -> _BatchCallPlan:
                certificates = tuple(certificate_by_id[item] for item in report_ids)
                batch_input = build_relation_batch_input(
                    judge_input, certificates, batch_id=batch_id
                )
                arbitration_input = RelationBatchArbitrationInput(
                    relation_input=batch_input,
                    primary_responses_1=tuple(
                        relation_1_by_id[item] for item in report_ids
                    ),
                    primary_responses_2=tuple(
                        relation_2_by_id[item] for item in report_ids
                    ),
                    disagreements=tuple(
                        item
                        for item in relation_disagreements
                        if any(
                            item.object_ref.startswith(f"report:{report_id}/")
                            for report_id in report_ids
                        )
                    ),
                    reason="All substantive relation conflicts in this batch require fresh expected-specific readings.",
                    basis=f"{JUDGE_ALGORITHM_VERSION}; immutable certificates and exact relation comparison",
                )
                model = build_exact_relation_batch_model(batch_input)
                return _BatchCallPlan(
                    batch_id=batch_id,
                    phase="relation_arbitration",
                    reading_no=None,
                    report_ids=report_ids,
                    batch_input=batch_input,
                    schema=model,
                    kind="semantic-judge-relation-arbitration-batch",
                    system_prompt=RELATION_SYSTEM_PROMPT,
                    prompt=build_relation_batch_arbitration_prompt(arbitration_input),
                    artifact_id=f"{pair_id}/round-{round_no}/relation-arbitration-{batch_id}",
                )

            conflicted_certificates = tuple(
                certificate_by_id[item] for item in conflicted_relation_ids
            )
            groups = _relation_certificate_groups(
                conflicted_certificates, len(judge_input.expected_issues)
            )
            plans = tuple(
                make_relation_arbitration(
                    tuple(item.report_id for item in certificates),
                    _stable_batch_id(
                        "RA",
                        index,
                        tuple(item.report_id for item in certificates),
                    ),
                )
                for index, certificates in enumerate(groups, start=1)
            )

            def split_relation_arbitration(
                plan: _BatchCallPlan,
                child_ids: tuple[str, ...],
                child_index: int,
            ) -> _BatchCallPlan:
                return make_relation_arbitration(
                    child_ids, f"{plan.batch_id}.s{child_index}"
                )

            completed = _execute_with_split(
                runtime=runtime,
                initial_plans=plans,
                split_plan=split_relation_arbitration,
                receipts=receipts,
                schema_hashes=schema_hashes,
                pair_id=pair_id,
                round_no=round_no,
            )
            arbitration_by_id = {}
            for plan, outcome in completed:
                response = _require_response(
                    outcome, f"relation_arbitration_{plan.batch_id}"
                )
                batch_input = RelationBatchJudgeInput.model_validate(plan.batch_input)
                for row in relation_batch_responses(response, batch_input):
                    materialized = RelationResponse.model_validate(
                        row.model_dump(mode="json")
                    )
                    arbitration_by_id[materialized.report_id] = materialized
            relation_arbitrations = [
                arbitration_by_id[item] for item in conflicted_relation_ids
            ]
            final_relation_responses.update(arbitration_by_id)

        ordered_relation_responses = tuple(
            final_relation_responses[item]
            for item in report_order
            if item in final_relation_responses
        )
        final_reading = materialize_two_stage_reading(
            ordered_certificates, ordered_relation_responses, judge_input
        )
    except Exception as exc:
        raise JudgeExecutionFailure(str(exc), tuple(receipts)) from exc

    disagreements = validity_disagreements + relation_disagreements
    conflicts = _conflict_records(disagreements, final_certificates, final_reading)
    report_outcomes, expected_outcomes = decode_outcomes(final_reading, adapter_audit)
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
            "Two expected-isolated validity batch readings and two relation-only "
            f"batch readings completed; {len(validity_disagreements)} validity and "
            f"{len(relation_disagreements)} relation disagreements were fully arbitrated."
        ),
        basis=(
            f"{PROTOCOL_VERSION}; {JUDGE_ALGORITHM_VERSION}; {PROMPT_VERSION}; "
            f"max_batch_reports={MAX_REPORTS_PER_BATCH}; fixed clause closure, immutable "
            "validity certificates, exact relation matrices, process-isolated calls, and deterministic issue #195 metrics"
        ),
    )
