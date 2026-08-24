from __future__ import annotations

import json

from pipeline.semantic_judge.composite import (
    CompositeCallAudit,
    CompositePairReceipt,
    CompositeRoundSummary,
    CompositeRunSummary,
    CompositeSourceRun,
    CrossRoundCoverage,
    RecoveredPairFailure,
    _call_audit,
)
from pipeline.semantic_judge.models import JudgeCallReceipt, RetryRecord, UsageReceipt


def test_composite_call_audit_preserves_schema_and_provider_retry_accounting() -> None:
    call = JudgeCallReceipt(
        call_id="0000:r1:validity_primary_1:VB-01",
        pair_id="0000",
        batch_id="VB-01",
        report_ids=("R0001",),
        phase="validity_primary_1",
        status="success",
        process_id=123,
        started_at_utc="2026-08-24T00:00:00+00:00",
        ended_at_utc="2026-08-24T00:00:01+00:00",
        duration_seconds=1.0,
        profile="gpt-5.6-luna",
        schema_hash="sha256:" + "1" * 64,
        prompt_hash="sha256:" + "2" * 64,
        usage=(
            UsageReceipt(
                model_call_id="request-1",
                status="completed",
                model="gpt-5.6-luna",
                input_tokens=100,
                output_tokens=10,
                cache_read_input_tokens=60,
                cache_write_input_tokens=5,
                cost_counted=True,
                billing_disposition="billable",
                raw_usage_json="{}",
            ),
            UsageReceipt(
                model_call_id=None,
                status="failed",
                model="gpt-5.6-luna",
                input_tokens=None,
                output_tokens=None,
                cache_read_input_tokens=None,
                cache_write_input_tokens=None,
                cost_counted=False,
                billing_disposition="provider_error_retry_exempt",
                raw_usage_json="{}",
            ),
        ),
        retries=(
            RetryRecord(
                attempt_no=1,
                status="success",
                provider_error=True,
                error_code="provider_error",
                error_message="connection failed",
                billing_disposition="billable",
                raw_attempt_json=json.dumps(
                    {
                        "schema_validation_failures": [{"turn": 1}, {"turn": 2}],
                        "retry_records": [
                            {
                                "error": {
                                    "type": "APIConnectionError",
                                    "message": "Event loop is closed",
                                }
                            }
                        ],
                    },
                    sort_keys=True,
                ),
            ),
        ),
        cost_usd=0.5,
        cost_eligible=True,
        artifact_paths=("result.json",),
        reason="Validated fixture call.",
        basis="Provider-free receipt fixture.",
    )

    audit = _call_audit((call,))

    assert audit.logical_call_count == 1
    assert audit.provider_request_count == 2
    assert audit.completed_provider_request_count == 1
    assert audit.failed_provider_request_count == 1
    assert audit.provider_error_attempt_count == 1
    assert audit.schema_validation_failure_count == 2
    assert audit.api_connection_error_count == 1
    assert audit.event_loop_closed_error_count == 1
    assert audit.input_tokens == 100
    assert audit.cache_read_input_tokens == 60
    assert audit.cache_creation_input_tokens == 5
    assert audit.uncached_input_tokens == 35
    assert audit.output_tokens == 10
    assert audit.cost_usd == 0.5


def test_composite_pydantic_models_document_every_field() -> None:
    models = (
        CompositeCallAudit,
        CompositeSourceRun,
        CompositePairReceipt,
        RecoveredPairFailure,
        CompositeRoundSummary,
        CrossRoundCoverage,
        CompositeRunSummary,
    )

    for model in models:
        assert model.__doc__ and model.__doc__.strip()
        assert all(
            field.description and field.description.strip()
            for field in model.model_fields.values()
        )
