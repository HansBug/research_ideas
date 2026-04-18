from __future__ import annotations

import contextvars
import statistics
from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import Any, Iterator


@dataclass(slots=True)
class LLMOperationRecord:
    operation: str
    success: bool
    json_mode: bool
    repair_used: bool
    used_stream: bool
    transport_call_count: int
    failed_transport_call_count: int
    latency_s: float
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    error_type: str | None = None


@dataclass(slots=True)
class LLMUsageSummary:
    llm_configured: bool = False
    configured_model_name: str | None = None
    configured_provider: str | None = None
    effective_llm_used: bool = False
    fallback_only: bool = False
    operation_attempt_count: int = 0
    operation_success_count: int = 0
    operation_failure_count: int = 0
    transport_call_count: int = 0
    transport_failure_count: int = 0
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    total_latency_s: float = 0.0
    latency_p50: float = 0.0
    latency_p95: float = 0.0
    token_cost_per_record: float = 0.0
    successful_operations: list[str] = field(default_factory=list)
    failed_operations: list[str] = field(default_factory=list)
    operation_breakdown: dict[str, dict[str, int]] = field(default_factory=dict)


@dataclass(slots=True)
class _MutableRunTracker:
    llm_configured: bool
    configured_model_name: str | None
    configured_provider: str | None
    records: list[LLMOperationRecord] = field(default_factory=list)

    def record(self, item: LLMOperationRecord) -> None:
        self.records.append(item)

    def summarize(self, *, record_count: int = 1) -> LLMUsageSummary:
        latencies = [item.latency_s for item in self.records]
        breakdown: dict[str, dict[str, int]] = {}
        for item in self.records:
            packet = breakdown.setdefault(item.operation, {"success": 0, "failure": 0})
            packet["success" if item.success else "failure"] += 1
        success_ops = [item.operation for item in self.records if item.success]
        failure_ops = [item.operation for item in self.records if not item.success]
        summary = LLMUsageSummary(
            llm_configured=self.llm_configured,
            configured_model_name=self.configured_model_name,
            configured_provider=self.configured_provider,
            effective_llm_used=any(item.success for item in self.records),
            fallback_only=bool(self.llm_configured and self.records and not any(item.success for item in self.records)),
            operation_attempt_count=len(self.records),
            operation_success_count=sum(1 for item in self.records if item.success),
            operation_failure_count=sum(1 for item in self.records if not item.success),
            transport_call_count=sum(item.transport_call_count for item in self.records),
            transport_failure_count=sum(item.failed_transport_call_count for item in self.records),
            prompt_tokens=sum(item.prompt_tokens for item in self.records),
            completion_tokens=sum(item.completion_tokens for item in self.records),
            total_tokens=sum(item.total_tokens for item in self.records),
            total_latency_s=round(sum(item.latency_s for item in self.records), 6),
            latency_p50=round(statistics.median(latencies), 6) if latencies else 0.0,
            latency_p95=round(_p95(latencies), 6),
            token_cost_per_record=round(
                sum(item.total_tokens for item in self.records) / max(1, record_count),
                6,
            ),
            successful_operations=success_ops,
            failed_operations=failure_ops,
            operation_breakdown=breakdown,
        )
        return summary


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(0.95 * (len(ordered) - 1))))
    return ordered[index]


_RUN_TRACKER: contextvars.ContextVar[_MutableRunTracker | None] = contextvars.ContextVar(
    "expert_review_llm_run_tracker",
    default=None,
)


@contextmanager
def llm_run_context(
    *,
    llm_configured: bool,
    configured_model_name: str | None,
    configured_provider: str | None,
) -> Iterator[None]:
    token = _RUN_TRACKER.set(
        _MutableRunTracker(
            llm_configured=llm_configured,
            configured_model_name=configured_model_name,
            configured_provider=configured_provider,
        )
    )
    try:
        yield
    finally:
        _RUN_TRACKER.reset(token)


def record_llm_operation(
    *,
    operation: str,
    success: bool,
    json_mode: bool,
    repair_used: bool,
    used_stream: bool,
    transport_call_count: int,
    failed_transport_call_count: int,
    latency_s: float,
    prompt_tokens: int,
    completion_tokens: int,
    total_tokens: int,
    error_type: str | None = None,
) -> None:
    tracker = _RUN_TRACKER.get()
    if tracker is None:
        return
    tracker.record(
        LLMOperationRecord(
            operation=operation,
            success=success,
            json_mode=json_mode,
            repair_used=repair_used,
            used_stream=used_stream,
            transport_call_count=transport_call_count,
            failed_transport_call_count=failed_transport_call_count,
            latency_s=round(latency_s, 6),
            prompt_tokens=max(0, int(prompt_tokens)),
            completion_tokens=max(0, int(completion_tokens)),
            total_tokens=max(0, int(total_tokens)),
            error_type=error_type,
        )
    )


def summarize_current_llm_usage(*, record_count: int = 1) -> LLMUsageSummary:
    tracker = _RUN_TRACKER.get()
    if tracker is None:
        return LLMUsageSummary(token_cost_per_record=0.0)
    return tracker.summarize(record_count=record_count)


def usage_dict_from_response(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage_metadata", None)
    if isinstance(usage, dict):
        prompt = usage.get("input_tokens", usage.get("prompt_tokens", 0))
        completion = usage.get("output_tokens", usage.get("completion_tokens", 0))
        total = usage.get("total_tokens", 0)
        if total or prompt or completion:
            return {
                "prompt_tokens": int(prompt or 0),
                "completion_tokens": int(completion or 0),
                "total_tokens": int(total or (prompt or 0) + (completion or 0)),
            }
    response_metadata = getattr(response, "response_metadata", None)
    if isinstance(response_metadata, dict):
        token_usage = response_metadata.get("token_usage")
        if isinstance(token_usage, dict):
            prompt = token_usage.get("prompt_tokens", 0)
            completion = token_usage.get("completion_tokens", 0)
            total = token_usage.get("total_tokens", 0)
            return {
                "prompt_tokens": int(prompt or 0),
                "completion_tokens": int(completion or 0),
                "total_tokens": int(total or (prompt or 0) + (completion or 0)),
            }
    return {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


__all__ = [
    "LLMUsageSummary",
    "llm_run_context",
    "record_llm_operation",
    "summarize_current_llm_usage",
    "usage_dict_from_response",
]
