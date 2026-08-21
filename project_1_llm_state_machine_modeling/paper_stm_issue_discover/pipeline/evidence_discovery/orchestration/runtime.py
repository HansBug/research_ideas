from __future__ import annotations

import json
import signal
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

from utils.agent import AgentApp, AgentError, AgentSpec
from utils.llm import estimate_usage_cost_usd, load_llm_registry


T = TypeVar("T", bound=BaseModel)

# A streaming provider call gets a finite first-byte boundary. Its complete
# structured cell is bounded separately by ``PROVIDER_CALL_DEADLINE_SECONDS``.
# For non-streaming calls there is no first byte to wait for, so the provider
# timeout itself is set to the complete-call deadline.
PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS = 30
PROVIDER_CALL_DEADLINE_SECONDS = 120
MAX_STRUCTURED_OUTPUT_TOKENS = 8000
DEFAULT_TRANSPORT_RETRIES = 8
TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS = (5.0, 20.0, 60.0, 120.0, 240.0)


def _transport_retry_delays(retries: int) -> tuple[float, ...]:
    """Expand the audited retry schedule to the requested retry count."""

    if retries < 0:
        raise ValueError("transport_retries must be non-negative")
    if retries == 0:
        return ()
    tail = TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS[-1]
    return tuple(
        TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS[index]
        if index < len(TRANSPORT_RETRY_DELAY_SCHEDULE_SECONDS)
        else tail
        for index in range(retries)
    )


def _provider_timeout_seconds(streaming: bool) -> int:
    """Select the provider timeout for the transport mode.

    Streaming calls use the provider's first-byte/read boundary while the
    surrounding runtime enforces the complete-cell wall-clock deadline.
    Non-streaming calls use the complete-call timeout because no first-byte
    callback exists.
    """

    return (
        PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS
        if streaming
        else PROVIDER_CALL_DEADLINE_SECONDS
    )


class ProviderCallTimeout(TimeoutError):
    """Raised when the public structured cell exceeds its wall-clock deadline."""


@contextmanager
def _provider_deadline(seconds: int):
    """Bound a synchronous AgentApp call without changing its request payload."""

    if threading.current_thread() is not threading.main_thread():
        # SIGALRM is process-global; callers using a worker thread still rely
        # on the adapter timeout configured on the model itself.
        yield
        return
    previous = signal.getsignal(signal.SIGALRM)

    def _raise_timeout(_signum: int, _frame: Any) -> None:
        raise ProviderCallTimeout(
            f"provider structured call exceeded {seconds} seconds"
        )

    signal.signal(signal.SIGALRM, _raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, float(seconds))
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0.0)
        signal.signal(signal.SIGALRM, previous)


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return _jsonable(value.model_dump(mode="json"))
    return str(value)


def _usage_rows(result: Any, *, outer_attempt: int | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in getattr(result, "usage", ()) or ():
        if not isinstance(item, dict):
            continue
        value = item.get("usage")
        if isinstance(value, dict):
            row = dict(value)
            row["source_record"] = {key: item.get(key) for key in ("call_id", "attempt_id", "call_kind") if key in item}
            row["cost_counted"] = item.get("cost_counted", True)
            row["billing_disposition"] = item.get("billing_disposition", "billable")
            if outer_attempt is not None:
                row["outer_attempt"] = outer_attempt
            rows.append(row)
        elif all(key in item for key in ("input_tokens", "output_tokens")):
            row = dict(item)
            row.setdefault("cost_counted", True)
            row.setdefault("billing_disposition", "billable")
            if outer_attempt is not None:
                row["outer_attempt"] = outer_attempt
            rows.append(row)
    return rows


def _is_provider_error(error: dict[str, Any] | None) -> bool:
    if not error:
        return False
    code = str(error.get("code", "")).lower()
    message = str(error.get("message", "")).lower()
    details = json.dumps(error.get("details", {}), ensure_ascii=False).lower()
    text = " ".join((code, message, details))
    markers = (
        "provider",
        "transport",
        "rate_limit",
        "ratelimit",
        "http_408",
        "http_409",
        "http_429",
        "http_5",
        "upstream",
        "timeout",
        "connection",
        "api_error",
    )
    return any(marker in text for marker in markers)


def _read_audit_records(path: Path) -> list[dict[str, Any]]:
    """Read public retry receipts without making audit parsing a run gate."""

    if not path.is_file():
        return []
    records: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, dict):
            records.append(value)
    return records


def _retry_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        record
        for record in records
        if record.get("record") == "transport_retry"
        or record.get("record_type") == "transport_retry"
    ]


def _provider_failure_call_ids(
    records: list[dict[str, Any]],
    final_error: dict[str, Any] | None,
) -> set[str]:
    del final_error
    call_ids: set[str] = set()
    for record in records:
        record_type = record.get("record_type") or record.get("record")
        if record_type == "transport_retry":
            if record.get("operation") == "scheduled":
                call_id = record.get("failed_model_call_id")
                if isinstance(call_id, str) and call_id:
                    call_ids.add(call_id)
    return call_ids


def _annotate_usage_billing(
    rows: list[dict[str, Any]],
    *,
    audit_records: list[dict[str, Any]],
    final_error: dict[str, Any] | None,
    actual_outer_retry: bool = False,
) -> None:
    """Attach billing decisions to the specific failed provider attempts.

    The public AgentApp result contains normalized usage, while transport retry
    identity is emitted in its audit JSONL. Joining them here keeps provider
    retry exemptions local to the failed model call and leaves all other calls
    in the same cell billable.
    """

    failed_call_ids = _provider_failure_call_ids(audit_records, final_error)
    del final_error
    has_provider_retry = any(
        record.get("operation") == "scheduled"
        for record in _retry_records(audit_records)
    )
    if not has_provider_retry and not actual_outer_retry:
        return
    for row in rows:
        call_id = row.get("model_call_id")
        failed_status = row.get("status") in {"failed", "unavailable", "cancelled"}
        if (isinstance(call_id, str) and call_id in failed_call_ids) or (
            failed_status and (has_provider_retry or actual_outer_retry)
        ):
            row["cost_counted"] = False
            row["billing_disposition"] = "provider_error_retry_exempt"


def _cost_for_usage(rows: list[dict[str, Any]], pricing: Any) -> dict[str, Any]:
    if pricing is None:
        return {"eligible": False, "total_usd": None, "reason": "profile has no pricing card", "attempts": []}
    costs: list[dict[str, Any]] = []
    total = 0.0
    eligible = True
    for row in rows:
        if row.get("cost_counted") is False:
            costs.append({
                "eligible": True,
                "total_usd": 0.0,
                "billing_disposition": row.get("billing_disposition", "excluded"),
                "outer_attempt": row.get("outer_attempt"),
                "model_call_id": row.get("model_call_id"),
            })
            continue
        cost = estimate_usage_cost_usd(row, pricing)
        cost["billing_disposition"] = row.get("billing_disposition", "billable")
        cost["outer_attempt"] = row.get("outer_attempt")
        cost["model_call_id"] = row.get("model_call_id")
        costs.append(cost)
        if not cost.get("eligible"):
            eligible = False
        if isinstance(cost.get("total_usd"), (int, float)):
            total += float(cost["total_usd"])
    return {"eligible": eligible, "total_usd": total if eligible else None, "attempts": costs}


class StructuredContextBudget(BaseModel):
    """Prompt-size, provider-token, and truncation audit for one structured call."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    mode: str = Field(min_length=1, description="Structured LLM or provider-free fixture context mode.")
    projection_version: str = Field(min_length=1, description="Versioned prompt projection applied before serialization.")
    prompt_characters: int = Field(ge=0, description="Exact serialized user prompt character count.")
    estimated_prompt_tokens: int = Field(ge=0, description="Conservative four-characters-per-token pre-provider estimate.")
    provider_input_tokens: int | None = Field(default=None, ge=0, description="Actual provider-reported input tokens across audited attempts, when available.")
    context_window_tokens: int | None = Field(default=None, gt=0, description="Configured model context window, when available in the public profile.")
    max_output_tokens: int = Field(gt=0, description="Configured maximum structured output token count.")
    truncation_applied: bool = Field(description="Whether runtime text truncation removed any supplied stage input.")
    projection_decision: str = Field(min_length=1, description="Explicit stage projection and truncation decision.")
    reason: str = Field(min_length=1, description="Non-empty explanation of context-budget handling.")
    basis: str = Field(min_length=1, description="Non-empty prompt, profile, usage, and projection basis.")


class StructuredCallOutcome(BaseModel, Generic[T]):
    """Auditable result of one public structured runtime cell."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    kind: str = Field(min_length=1, description="Runtime operation kind, such as method or judge.")
    status: str = Field(min_length=1, description="Terminal cell status, including success or failed diagnostics.")
    response: T | None = Field(default=None, description="Validated Pydantic structured response, or null when schema/runtime handling failed.")
    result: dict[str, Any] = Field(description="Raw public runtime result metadata retained for audit.")
    attempts: list[dict[str, Any]] = Field(default_factory=list, description="Per-cell outer attempts, provider diagnostics, retry receipts, and artifact paths.")
    usage: list[dict[str, Any]] = Field(default_factory=list, description="Normalized usage rows with model-call identity and billing disposition.")
    cost: dict[str, Any] = Field(default_factory=dict, description="Cost calculation and eligibility for this cell's usage rows.")
    context_budget: StructuredContextBudget = Field(description="Prompt size, provider token, model window, and truncation receipt.")
    real_llm: bool = Field(description="Whether this outcome came from the configured real provider rather than a fixture runtime.")
    reason: str = Field(min_length=1, description="Non-empty explanation of the structured call terminal outcome.")
    basis: str = Field(min_length=1, description="Non-empty runtime, provider, schema, and retry basis for the terminal outcome.")

    @property
    def succeeded(self) -> bool:
        return self.status == "success" and self.response is not None

    @property
    def provider_error(self) -> bool:
        return bool(self.attempts and self.attempts[-1].get("provider_error"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "status": self.status,
            "response": _jsonable(self.response),
            "result": self.result,
            "attempts": self.attempts,
            "usage": self.usage,
            "cost": self.cost,
            "context_budget": self.context_budget.model_dump(mode="json"),
            "real_llm": self.real_llm,
            "reason": self.reason,
            "basis": self.basis,
        }


class PublicStructuredRuntime:
    """One public AgentApp wrapper shared by method and independent judge."""

    real_llm = True

    def __init__(
        self,
        profile: str,
        artifact_root: Path,
        *,
        transport_retries: int = DEFAULT_TRANSPORT_RETRIES,
        streaming: bool = True,
    ):
        self.profile = profile
        self.artifact_root = artifact_root
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        self.registry = load_llm_registry()
        self.config = self.registry.require(profile)
        self.transport_retries = transport_retries
        self.transport_retry_delays = _transport_retry_delays(transport_retries)
        self.streaming = streaming

    def _app(
        self,
        kind: str,
        schema: type[T],
        system_prompt: str,
        *,
        streaming: bool,
    ) -> AgentApp:
        # AgentApp owns a per-run call ledger, but the LangGraph/provider model
        # wrapper can retain structured-output state across invocations. A fresh
        # public app per cell keeps the frozen cell boundary explicit and avoids
        # a previous cell exhausting the next cell's model-call budget.
        spec = AgentSpec(
            name=f"evidence-discovery-{kind}",
            system_prompt=system_prompt,
            output_schema=schema,
            limits={
                "model_calls": max(6, self.transport_retries + 4),
                "turns": 6,
                "seconds": PROVIDER_CALL_DEADLINE_SECONDS,
            },
            require_tool_call=False,
            retry_missing_structured_output=True,
            transport_retry_delays_seconds=self.transport_retry_delays,
        )
        return AgentApp.from_registry(
            spec,
            self.registry,
            profile=self.profile,
            model_options={
                "streaming": streaming,
                "max_retries": 0,
                "timeout": _provider_timeout_seconds(streaming),
            },
        )

    def call(
        self,
        *,
        kind: str,
        schema: type[T],
        system_prompt: str,
        prompt: str,
        artifact_id: str,
        retry_cell_on_provider_error: bool = True,
        streaming: bool | None = None,
    ) -> StructuredCallOutcome[T]:
        use_streaming = self.streaming if streaming is None else streaming
        attempts: list[dict[str, Any]] = []
        all_usage: list[dict[str, Any]] = []
        last_result: dict[str, Any] = {}
        response: T | None = None
        status = "failed"
        max_outer_attempts = 2 if retry_cell_on_provider_error else 1
        for outer_attempt in range(1, max_outer_attempts + 1):
            attempt_dir = self.artifact_root / artifact_id / f"cell-attempt-{outer_attempt}"
            attempt_dir.mkdir(parents=True, exist_ok=True)
            audit_path = attempt_dir / "audit.jsonl"
            result_path = attempt_dir / "result.json"
            try:
                with _provider_deadline(PROVIDER_CALL_DEADLINE_SECONDS):
                    result = self._app(
                        kind,
                        schema,
                        system_prompt,
                        streaming=use_streaming,
                    ).run(
                        prompt,
                        renderer="quiet",
                        log_level="ERROR",
                        model_call_options={"max_tokens": MAX_STRUCTURED_OUTPUT_TOKENS},
                        audit_out=audit_path,
                        result_out=result_path,
                    )
                last_result = result.to_dict()
                audit_records = _read_audit_records(audit_path)
                rows = _usage_rows(result, outer_attempt=outer_attempt)
                all_usage.extend(rows)
                error = result.error if isinstance(result.error, dict) else None
                provider_error = _is_provider_error(error)
                actual_outer_retry = bool(
                    provider_error and outer_attempt < max_outer_attempts
                )
                _annotate_usage_billing(
                    rows,
                    audit_records=audit_records,
                    final_error=error,
                    actual_outer_retry=actual_outer_retry,
                )
                attempt = {
                    "outer_attempt": outer_attempt,
                    "status": result.status,
                    "provider_error": provider_error,
                    "error": error,
                    "audit_path": str(audit_path),
                    "result_path": str(result_path),
                    "usage_count": len(rows),
                    "billing_disposition": "provider_error_attempt_requires_row_level_join" if provider_error else "billable",
                    "retry_records": _retry_records(audit_records),
                }
                attempts.append(attempt)
                if result.status == "success" and result.output is not None:
                    response = result.output if isinstance(result.output, schema) else schema.model_validate(result.output)
                    status = "success"
                    break
                if provider_error and outer_attempt < max_outer_attempts:
                    continue
                status = "failed"
                break
            except (ProviderCallTimeout, AgentError, ValueError, TypeError) as exc:
                audit_records = _read_audit_records(audit_path)
                error_payload = {
                    "code": "provider_timeout" if isinstance(exc, ProviderCallTimeout) else type(exc).__name__,
                    "message": str(exc),
                }
                provider_error = _is_provider_error(error_payload)
                attempts.append({
                    "outer_attempt": outer_attempt,
                    "status": "exception",
                    "provider_error": provider_error,
                    "error": error_payload,
                    "audit_path": str(audit_path),
                    "result_path": str(result_path),
                    "usage_count": 0,
                    "billing_disposition": "provider_error_attempt_requires_row_level_join" if provider_error else "billable",
                    "retry_records": _retry_records(audit_records),
                })
                if provider_error and outer_attempt < max_outer_attempts:
                    continue
                status = "failed"
                last_result = {"status": "failed", "error": error_payload}
                break
        cost = _cost_for_usage(all_usage, self.config.pricing)
        provider_input_tokens = sum(
            int(row["input_tokens"])
            for row in all_usage
            if isinstance(row.get("input_tokens"), int)
        )
        context_budget = StructuredContextBudget(
            mode="structured_llm",
            projection_version="stage-context-projection.v2",
            prompt_characters=len(prompt),
            estimated_prompt_tokens=(len(prompt) + 3) // 4,
            provider_input_tokens=(provider_input_tokens if all_usage else None),
            context_window_tokens=self.config.context_window_tokens,
            max_output_tokens=MAX_STRUCTURED_OUTPUT_TOKENS,
            truncation_applied=False,
            projection_decision="The stage-specific structured projection was serialized in full; runtime text truncation was not applied.",
            reason="The call records both the pre-provider prompt size and actual provider usage when available.",
            basis="stage-context-projection.v2, utils.llm profile limits, and normalized usage rows",
        )
        return StructuredCallOutcome(
            kind=kind,
            status=status,
            response=response,
            result=last_result,
            attempts=attempts,
            usage=all_usage,
            cost=cost,
            context_budget=context_budget,
            real_llm=True,
            reason=(
                "The public structured call completed with a validated Pydantic response."
                if status == "success"
                else "The public structured call exhausted its provider/schema path and retained a terminal failure receipt."
            ),
            basis=(
                f"utils.agent AgentApp; transport_retries={self.transport_retries}; "
                f"stream_timeout={PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS}s; total_deadline={PROVIDER_CALL_DEADLINE_SECONDS}s"
            ),
        )


class FixtureStructuredRuntime:
    """Provider-free structured runtime for end-to-end fixture smoke runs.

    This fixture intentionally returns empty grounding and judge surfaces so
    the method's no-silent-drop fallbacks, typed D coverage checks, receipts,
    and independent-judge normalization are exercised without credentials.
    It is never used for live results and carries no ledger payload.
    """

    real_llm = False

    def call(
        self,
        *,
        kind: str,
        schema: type[T],
        system_prompt: str,
        prompt: str,
        artifact_id: str,
        **kwargs: Any,
    ) -> StructuredCallOutcome[T]:
        if schema.__name__ == "NLContractResponse":
            payload: dict[str, Any] = {
                "contracts": [],
                "segment_disposition": {},
                "reason": "Fixture contract output leaves semantic extraction to the fallback receipt.",
                "basis": "provider-free fixture runtime",
            }
        elif schema.__name__ == "GroundingResponse":
            payload = {
                "branch": "model" if kind == "model_grounding" else "source",
                "candidates": [],
                "rejected_contract_ids": [],
                "reason": "Fixture grounding output leaves candidate generation to the fallback receipt.",
                "basis": "provider-free fixture runtime",
            }
        elif schema.__name__ == "DAdjudicationResponse":
            parts = artifact_id.split("/")
            pair_id = parts[1] if len(parts) > 1 else "fixture"
            round_id = next((item for item in parts if item.startswith("round-")), "round-1")
            round_number = round_id.split("-", 1)[1] if "-" in round_id else "1"
            payload = {
                "decisions": [
                    {
                        "obligation_id": f"{pair_id}:r{round_number}:i0",
                        "grounding": "unresolved",
                        "violated_obligation": "The fixture does not make an open-world semantic decision.",
                        "strongest_defeater": None,
                        "defeater_kind": "none",
                        "defeater_disposition": "defeated",
                        "reason": "Fixture D output preserves an unresolved semantic decision.",
                        "basis": "provider-free fixture runtime",
                    }
                ],
                "reason": "Fixture D output is intentionally unresolved.",
                "basis": "provider-free fixture runtime",
            }
        else:
            # Judge normalization supplies one conservative assessment per
            # ledger/release unit after this empty provider-free response.
            payload = {
                "ledger_assessments": [],
                "release_assessments": [],
                "reason": "Fixture judge output is normalized conservatively by the independent-judge boundary.",
                "basis": "provider-free fixture runtime",
            }
        response = schema.model_validate(payload)
        context_budget = StructuredContextBudget(
            mode="provider_free_fixture",
            projection_version="stage-context-projection.v2",
            prompt_characters=len(prompt),
            estimated_prompt_tokens=(len(prompt) + 3) // 4,
            provider_input_tokens=None,
            context_window_tokens=None,
            max_output_tokens=MAX_STRUCTURED_OUTPUT_TOKENS,
            truncation_applied=False,
            projection_decision="The provider-free fixture consumed the complete serialized stage projection without truncation.",
            reason="Fixture prompt size is recorded even though no provider token usage exists.",
            basis="provider-free fixture runtime and stage-context-projection.v2",
        )
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
            context_budget=context_budget,
            real_llm=False,
            reason="The provider-free fixture returned a validated staged response.",
            basis="provider-free fixture runtime",
        )
