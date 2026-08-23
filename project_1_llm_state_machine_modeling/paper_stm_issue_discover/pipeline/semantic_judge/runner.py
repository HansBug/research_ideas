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
    build_exact_response_model,
    materialize_reading,
    response_schema_hash,
)


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
    for report_id in sorted(reports_1):
        first = reports_1[report_id]
        second = reports_2[report_id]
        if first.validity != second.validity:
            disagreements.append(
                ReadingDisagreement(
                    kind=ConflictKind.VALIDITY,
                    object_ref=f"report:{report_id}",
                    reading_1_value=first.validity.value,
                    reading_2_value=second.validity.value,
                )
            )
        if first.root_cause_cluster_key != second.root_cause_cluster_key:
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
        row.validity.value
        if disagreement.kind == ConflictKind.VALIDITY
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
        for path_key in ("audit_path", "result_path"):
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


def _validated_reading(outcome: StructuredCallOutcome[Any], phase: str) -> JudgeReading:
    if not outcome.succeeded or outcome.response is None:
        raise RuntimeError(
            f"semantic Judge {phase} failed after provider/schema handling: {outcome.reason}; {outcome.basis}"
        )
    response = JudgeResponse.model_validate(outcome.response.model_dump(mode="json"))
    return materialize_reading(response)


def judge_pair(
    *,
    run_id: str,
    round_no: int,
    judge_input: UnifiedJudgeInput,
    adapter_audit: AdapterAudit,
    runtime: PublicStructuredRuntime,
    judge_code_commit: str,
) -> PairJudgeResult:
    """Run two blind readings and a full arbitration on any substantive conflict."""

    response_model = build_exact_response_model(judge_input)
    schema_hash = response_schema_hash(response_model)
    primary_prompt = build_primary_prompt(judge_input)
    primary_prompt_hash = _sha256_text(SYSTEM_PROMPT + "\n" + primary_prompt)
    pair_id = judge_input.pair_id
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
    reading_1 = _validated_reading(outcome_1, "primary_1")
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
    reading_2 = _validated_reading(outcome_2, "primary_2")
    receipts = [
        _call_receipt(
            call_id=f"{pair_id}:r{round_no}:primary-1",
            phase="primary_1",
            profile=runtime.profile,
            schema_hash=schema_hash,
            actual_prompt_hash=primary_prompt_hash,
            outcome=outcome_1,
        ),
        _call_receipt(
            call_id=f"{pair_id}:r{round_no}:primary-2",
            phase="primary_2",
            profile=runtime.profile,
            schema_hash=schema_hash,
            actual_prompt_hash=primary_prompt_hash,
            outcome=outcome_2,
        ),
    ]
    disagreements = detect_disagreements(reading_1, reading_2)
    arbitration_reading = None
    if disagreements:
        arbitration_input = ArbitrationInput(
            judge_input=judge_input,
            primary_reading_1=reading_1,
            primary_reading_2=reading_2,
            disagreements=disagreements,
            reason="Primary semantic values conflict; issue #195 requires complete artifact review and final arbitration with no UNKNOWN.",
            basis=f"{JUDGE_ALGORITHM_VERSION}; exact enum/validity/root-cause comparison",
        )
        arbitration_prompt = build_arbitration_prompt(arbitration_input)
        arbitration_prompt_hash = _sha256_text(
            SYSTEM_PROMPT + "\n" + arbitration_prompt
        )
        arbitration_outcome = runtime.call(
            kind="semantic-judge-arbitration",
            schema=response_model,
            system_prompt=SYSTEM_PROMPT,
            prompt=arbitration_prompt,
            artifact_id=f"{pair_id}/round-{round_no}/arbitration",
            retry_cell_on_provider_error=True,
            max_output_tokens=min(
                JUDGE_MAX_OUTPUT_TOKENS, runtime.config.max_output_tokens
            ),
        )
        arbitration_reading = _validated_reading(arbitration_outcome, "arbitration")
        receipts.append(
            _call_receipt(
                call_id=f"{pair_id}:r{round_no}:arbitration",
                phase="arbitration",
                profile=runtime.profile,
                schema_hash=schema_hash,
                actual_prompt_hash=arbitration_prompt_hash,
                outcome=arbitration_outcome,
            )
        )
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
