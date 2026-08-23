"""Single executable path for issue #195 primary readings and arbitration."""

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
    ArbitrationInput,
    ArbitrationResponse,
    ConflictKind,
    ConflictRecord,
    JudgeCallReceipt,
    JudgeReading,
    JudgeResponse,
    PairJudgeResult,
    ReadingDisagreement,
    RetryRecord,
    UnifiedJudgeInput,
    UsageReceipt,
)
from .protocol import (
    ARBITRATION_INSTRUCTION,
    JUDGE_ALGORITHM_VERSION,
    JUDGE_MAX_OUTPUT_TOKENS,
    PRIMARY_INSTRUCTION,
    PROMPT_VERSION,
    PROTOCOL_SHA256,
    PROTOCOL_VERSION,
    SYSTEM_PROMPT,
    prompt_hash,
)
from .schema import (
    build_exact_arbitration_model,
    build_exact_response_model,
    materialize_reading,
    merge_arbitration_response,
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


def build_primary_prompt(judge_input: UnifiedJudgeInput) -> str:
    """Serialize the exact same primary prompt for either source adapter."""

    return (
        f"{PRIMARY_INSTRUCTION}\n\n"
        "<unified_judge_input>\n"
        f"{judge_input.model_dump_json(indent=2)}\n"
        "</unified_judge_input>"
    )


def build_arbitration_prompt(arbitration_input: ArbitrationInput) -> str:
    """Serialize complete common artifacts and both readings for conflict resolution."""

    return (
        f"{ARBITRATION_INSTRUCTION}\n\n"
        "<arbitration_input>\n"
        f"{arbitration_input.model_dump_json(indent=2)}\n"
        "</arbitration_input>"
    )


def detect_disagreements(
    reading_1: JudgeReading,
    reading_2: JudgeReading,
) -> tuple[ReadingDisagreement, ...]:
    """Compare only semantic enum/validity/cluster values, never wording or order."""

    disagreements: list[ReadingDisagreement] = []
    relations_1 = {(row.report_id, row.expected_id): row for row in reading_1.relations}
    relations_2 = {(row.report_id, row.expected_id): row for row in reading_2.relations}
    if set(relations_1) != set(relations_2):
        raise ValueError(
            "primary reading relation closures differ after schema validation"
        )
    for key in sorted(relations_1):
        value_1 = relations_1[key].match.value
        value_2 = relations_2[key].match.value
        if value_1 != value_2:
            disagreements.append(
                ReadingDisagreement(
                    kind=ConflictKind.RELATION,
                    object_ref=f"report:{key[0]}/expected:{key[1]}",
                    reading_1_value=value_1,
                    reading_2_value=value_2,
                )
            )
    reports_1 = {row.report_id: row for row in reading_1.report_assessments}
    reports_2 = {row.report_id: row for row in reading_2.report_assessments}
    if set(reports_1) != set(reports_2):
        raise ValueError(
            "primary reading report closures differ after schema validation"
        )
    cluster_members_1 = {
        report_id: frozenset(
            other.report_id
            for other in reports_1.values()
            if other.root_cause_cluster_key == report.root_cause_cluster_key
        )
        for report_id, report in reports_1.items()
    }
    cluster_members_2 = {
        report_id: frozenset(
            other.report_id
            for other in reports_2.values()
            if other.root_cause_cluster_key == report.root_cause_cluster_key
        )
        for report_id, report in reports_2.items()
    }
    for report_id in sorted(reports_1):
        first = reports_1[report_id]
        second = reports_2[report_id]
        if first.core_truth != second.core_truth:
            disagreements.append(
                ReadingDisagreement(
                    kind=ConflictKind.CORE_TRUTH,
                    object_ref=f"report:{report_id}",
                    reading_1_value=first.core_truth.value,
                    reading_2_value=second.core_truth.value,
                )
            )
        if cluster_members_1[report_id] != cluster_members_2[report_id]:
            disagreements.append(
                ReadingDisagreement(
                    kind=ConflictKind.ROOT_CAUSE_CLUSTER,
                    object_ref=f"report:{report_id}",
                    reading_1_value=first.root_cause_cluster_key,
                    reading_2_value=second.root_cause_cluster_key,
                )
            )
    return tuple(disagreements)


def _find_final_row(
    disagreement: ReadingDisagreement,
    final_reading: JudgeReading,
) -> tuple[str, str, str, tuple[str, ...]]:
    if disagreement.kind == ConflictKind.RELATION:
        report_part, expected_part = disagreement.object_ref.split("/")
        report_id = report_part.removeprefix("report:")
        expected_id = expected_part.removeprefix("expected:")
        row = next(
            item
            for item in final_reading.relations
            if item.report_id == report_id and item.expected_id == expected_id
        )
        return row.match.value, row.reason, row.basis, row.source_refs
    report_id = disagreement.object_ref.removeprefix("report:")
    row = next(
        item for item in final_reading.report_assessments if item.report_id == report_id
    )
    final_value = (
        row.core_truth.value
        if disagreement.kind == ConflictKind.CORE_TRUTH
        else row.root_cause_cluster_key
    )
    return final_value, row.reason, row.basis, row.source_refs


def build_conflict_records(
    disagreements: tuple[ReadingDisagreement, ...],
    final_reading: JudgeReading,
) -> tuple[ConflictRecord, ...]:
    """Attach the final arbitrated reason/basis to every detected disagreement."""

    records = []
    for disagreement in disagreements:
        final_value, reason, basis, source_refs = _find_final_row(
            disagreement, final_reading
        )
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
    retries: list[RetryRecord] = []
    artifact_paths: list[str] = []
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
        status=("success" if outcome.succeeded else "failed"),
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


def _validated_response(
    outcome: StructuredCallOutcome[Any], phase: str
) -> JudgeResponse:
    if not outcome.succeeded or outcome.response is None:
        raise RuntimeError(
            f"semantic Judge {phase} failed after provider/schema handling: {outcome.reason}; {outcome.basis}"
        )
    return JudgeResponse.model_validate(outcome.response.model_dump(mode="json"))


def _validated_arbitration_response(
    outcome: StructuredCallOutcome[Any], phase: str
) -> ArbitrationResponse:
    if not outcome.succeeded or outcome.response is None:
        raise RuntimeError(
            f"semantic Judge {phase} failed after provider/schema handling: {outcome.reason}; {outcome.basis}"
        )
    return ArbitrationResponse.model_validate(outcome.response.model_dump(mode="json"))


def _conflicted_report_ids(
    disagreements: tuple[ReadingDisagreement, ...],
) -> tuple[str, ...]:
    """Resolve every relation/report conflict to its enclosing report identity."""

    values = []
    for disagreement in disagreements:
        report_ref = disagreement.object_ref.split("/", 1)[0]
        values.append(report_ref.removeprefix("report:"))
    return tuple(dict.fromkeys(values))


def judge_pair(
    *,
    run_id: str,
    round_no: int,
    judge_input: UnifiedJudgeInput,
    adapter_audit: AdapterAudit,
    runtime: PublicStructuredRuntime,
    judge_code_commit: str,
) -> PairJudgeResult:
    """Run two blind sparse readings and targeted arbitration when required."""

    response_model = build_exact_response_model(judge_input)
    schema_hash = response_schema_hash(response_model)
    primary_prompt = build_primary_prompt(judge_input)
    primary_prompt_hash = _sha256_text(SYSTEM_PROMPT + "\n" + primary_prompt)
    pair_id = judge_input.pair_id
    receipts: list[JudgeCallReceipt] = []
    outcome_1 = runtime.call(
        kind="semantic-judge-primary",
        schema=response_model,
        system_prompt=SYSTEM_PROMPT,
        prompt=primary_prompt,
        artifact_id=f"{pair_id}/round-{round_no}/primary-1",
        retry_cell_on_provider_error=True,
        max_output_tokens=min(
            JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
        ),
    )
    receipts.append(
        _call_receipt(
            call_id=f"{pair_id}:r{round_no}:primary-1",
            phase="primary_1",
            profile=runtime.profile,
            schema_hash=schema_hash,
            actual_prompt_hash=primary_prompt_hash,
            outcome=outcome_1,
        )
    )
    try:
        response_1 = _validated_response(outcome_1, "primary_1")
        reading_1 = materialize_reading(response_1, judge_input)
    except Exception as exc:
        raise JudgeExecutionFailure(str(exc), tuple(receipts)) from exc
    outcome_2 = runtime.call(
        kind="semantic-judge-primary",
        schema=response_model,
        system_prompt=SYSTEM_PROMPT,
        prompt=primary_prompt,
        artifact_id=f"{pair_id}/round-{round_no}/primary-2",
        retry_cell_on_provider_error=True,
        max_output_tokens=min(
            JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
        ),
    )
    receipts.append(
        _call_receipt(
            call_id=f"{pair_id}:r{round_no}:primary-2",
            phase="primary_2",
            profile=runtime.profile,
            schema_hash=schema_hash,
            actual_prompt_hash=primary_prompt_hash,
            outcome=outcome_2,
        )
    )
    try:
        response_2 = _validated_response(outcome_2, "primary_2")
        reading_2 = materialize_reading(response_2, judge_input)
        disagreements = detect_disagreements(reading_1, reading_2)
    except Exception as exc:
        raise JudgeExecutionFailure(str(exc), tuple(receipts)) from exc
    arbitration_reading = None
    if disagreements:
        conflicted_report_ids = _conflicted_report_ids(disagreements)
        reports_by_id = {row.report_id: row for row in judge_input.reports}
        response_1_by_id = {
            row.report_id: row for row in response_1.report_judgments
        }
        response_2_by_id = {
            row.report_id: row for row in response_2.report_judgments
        }
        atomic_responses: list[ArbitrationResponse] = []
        try:
            for report_id in conflicted_report_ids:
                report_disagreements = tuple(
                    row
                    for row in disagreements
                    if row.object_ref.split("/", 1)[0]
                    == f"report:{report_id}"
                )
                atomic_input = judge_input.model_copy(
                    update={"reports": (reports_by_id[report_id],)}
                )
                arbitration_input = ArbitrationInput(
                    judge_input=atomic_input,
                    primary_conflicting_judgments_1=(
                        response_1_by_id[report_id],
                    ),
                    primary_conflicting_judgments_2=(
                        response_2_by_id[report_id],
                    ),
                    disagreements=report_disagreements,
                    reason="Primary semantic values for this report conflict; complete artifact review must select a final result with no UNKNOWN.",
                    basis=f"{JUDGE_ALGORITHM_VERSION}; exact relation/core-truth/root-cause-partition comparison",
                )
                arbitration_model = build_exact_arbitration_model(
                    atomic_input, (report_id,)
                )
                arbitration_schema_hash = response_schema_hash(arbitration_model)
                arbitration_prompt = build_arbitration_prompt(arbitration_input)
                arbitration_prompt_hash = _sha256_text(
                    SYSTEM_PROMPT + "\n" + arbitration_prompt
                )
                arbitration_outcome = runtime.call(
                    kind="semantic-judge-arbitration",
                    schema=arbitration_model,
                    system_prompt=SYSTEM_PROMPT,
                    prompt=arbitration_prompt,
                    artifact_id=(
                        f"{pair_id}/round-{round_no}/arbitration-{report_id}"
                    ),
                    retry_cell_on_provider_error=True,
                    max_output_tokens=min(
                        JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
                    ),
                )
                receipts.append(
                    _call_receipt(
                        call_id=(
                            f"{pair_id}:r{round_no}:arbitration:{report_id}"
                        ),
                        phase="arbitration",
                        profile=runtime.profile,
                        schema_hash=arbitration_schema_hash,
                        actual_prompt_hash=arbitration_prompt_hash,
                        outcome=arbitration_outcome,
                    )
                )
                atomic_responses.append(
                    _validated_arbitration_response(
                        arbitration_outcome, f"arbitration_{report_id}"
                    )
                )
            arbitration_response = ArbitrationResponse(
                report_judgments=tuple(
                    response.report_judgments[0]
                    for response in atomic_responses
                ),
                reason=" ".join(
                    f"{report_id}: {response.reason}"
                    for report_id, response in zip(
                        conflicted_report_ids, atomic_responses, strict=True
                    )
                ),
                basis=" ".join(
                    f"{report_id}: {response.basis}"
                    for report_id, response in zip(
                        conflicted_report_ids, atomic_responses, strict=True
                    )
                ),
                source_refs=tuple(
                    dict.fromkeys(
                        ref
                        for response in atomic_responses
                        for ref in response.source_refs
                    )
                ),
            )
            final_response = merge_arbitration_response(
                response_1,
                arbitration_response,
                response_model,
            )
            arbitration_reading = materialize_reading(final_response, judge_input)
        except Exception as exc:
            raise JudgeExecutionFailure(str(exc), tuple(receipts)) from exc
        final_reading = arbitration_reading
    else:
        final_reading = reading_1
    conflicts = build_conflict_records(disagreements, final_reading)
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
        response_schema_hash=schema_hash,
        prompt_template_hash=prompt_hash(),
        adapter_audit=adapter_audit,
        primary_reading_1=reading_1,
        primary_reading_2=reading_2,
        arbitration_reading=arbitration_reading,
        conflicts=conflicts,
        final_reading=final_reading,
        report_outcomes=report_outcomes,
        expected_outcomes=expected_outcomes,
        metrics=metrics,
        call_receipts=tuple(receipts),
        reason=(
            f"Two independent readings completed; {len(disagreements)} substantive conflicts "
            f"were {'fully arbitrated' if disagreements else 'absent'}."
        ),
        basis=(
            f"{PROTOCOL_VERSION}; {JUDGE_ALGORITHM_VERSION}; {PROMPT_VERSION}; "
            "exact response closure and deterministic issue #195 metrics"
        ),
    )
