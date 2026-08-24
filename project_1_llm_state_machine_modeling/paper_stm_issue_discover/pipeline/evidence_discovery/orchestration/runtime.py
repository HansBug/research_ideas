from __future__ import annotations

import asyncio
import json
import threading
from pathlib import Path
from typing import Any, Generic, TypeVar

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from utils.agent import AgentApp, AgentError, AgentSpec
from utils.llm import estimate_usage_cost_usd, load_llm_registry

T = TypeVar("T", bound=BaseModel)

# A streaming provider call gets a finite first-byte/read boundary. Each model
# invocation has a separate complete-call deadline, while the enclosing
# structured stage has enough time for one bounded schema-repair turn. For
# non-streaming calls there is no first byte to wait for, so the provider
# timeout itself is set to the complete-call deadline.
PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS = 30
PROVIDER_CALL_DEADLINE_SECONDS = 300
STRUCTURED_STAGE_DEADLINE_SECONDS = 3 * PROVIDER_CALL_DEADLINE_SECONDS
MAX_STRUCTURED_OUTPUT_TOKENS = 10_000
JUDGE_MAX_STRUCTURED_OUTPUT_TOKENS = 20_000
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


class StructuredStageTimeout(TimeoutError):
    """Raised when the enclosing structured stage exhausts its local deadline."""


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


def _usage_rows(
    result: Any, *, outer_attempt: int | None = None
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    usage = (
        result.get("usage", ())
        if isinstance(result, dict)
        else getattr(result, "usage", ())
    )
    for item in usage or ():
        if not isinstance(item, dict):
            continue
        value = item.get("usage")
        if isinstance(value, dict):
            row = dict(value)
            row["source_record"] = {
                key: item.get(key)
                for key in ("call_id", "attempt_id", "call_kind")
                if key in item
            }
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


def _read_result_artifact(path: Path) -> tuple[dict[str, Any] | None, str]:
    """Recover a committed public result without turning audit damage into a gate."""

    if not path.is_file():
        return None, "result_artifact_missing"
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None, "result_artifact_unreadable"
    if not isinstance(value, dict):
        return None, "result_artifact_not_an_object"
    return value, "committed_result_artifact"


def _is_provider_error(error: dict[str, Any] | None) -> bool:
    """Classify only explicit transport/provider ownership as provider error.

    Public ``utils.agent`` receipts normalize provider failures to a typed code,
    phase, or ``details.source``. Free-text messages are deliberately excluded:
    a schema or local bug mentioning a timeout/provider must remain billable and
    must not receive the provider retry exemption.
    """

    if not error:
        return False
    code = str(error.get("code", "")).strip().lower().replace("-", "_")
    explicit_codes = {
        "provider_error",
        "provider_timeout",
        "transport_error",
        "rate_limit",
        "rate_limit_error",
        "api_connection_error",
        "api_timeout_error",
        "service_unavailable",
    }
    if code in explicit_codes:
        return True
    if code.startswith("http_"):
        status = code.removeprefix("http_").split("_", 1)[0]
        if status in {"408", "409", "429"} or status.startswith("5"):
            return True
    if str(error.get("phase", "")).strip().lower() == "model_transport":
        return True
    details = error.get("details")
    if not isinstance(details, dict):
        return False
    if str(details.get("source", "")).strip().lower() == "provider":
        return True
    detail_type = str(details.get("type", "")).strip().lower().replace("-", "_")
    return detail_type == "providercalltimeout"


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


class StructuredSchemaValidationFailure(BaseModel):
    """One exact rejected structured action revalidated against its runtime schema."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    outer_attempt: int = Field(
        ge=1,
        description="One-based public runtime cell attempt containing the rejected structured action.",
    )
    turn: int = Field(
        ge=1,
        description="Agent turn that emitted arguments rejected by the exact Pydantic response schema.",
    )
    tool_call_id: str | None = Field(
        default=None,
        description="Provider tool-call ID for the rejected arguments; null means the audit adapter did not expose one.",
    )
    schema_name: str = Field(
        min_length=1,
        description="Exact runtime Pydantic response-model name used to reproduce the validation failure.",
    )
    error_count: int = Field(
        ge=1,
        description="Number of Pydantic validation errors reproduced for this rejected action.",
    )
    validation_error: str = Field(
        min_length=1,
        description="Complete English Pydantic ValidationError text, including object paths, constraints, and actual conflicts.",
    )
    errors_json: str = Field(
        min_length=1,
        description="Stable JSON array from ValidationError.errors(), normalized for direct machine audit.",
    )


class StructuredSchemaValidationBundle(BaseModel):
    """Persistent typed audit of all schema-invalid actions in one runtime cell attempt."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    schema_version: str = Field(
        default="evidence-discovery.structured-schema-validation.v1",
        description="Public structured-validation audit schema version for persistence compatibility.",
    )
    schema_name: str = Field(
        min_length=1,
        description="Exact Pydantic response-model name applied to every rejected action in this bundle.",
    )
    failures: tuple[StructuredSchemaValidationFailure, ...] = Field(
        min_length=1,
        description="Complete ordered set of reproducible schema failures found in the public action audit.",
    )
    reason: str = Field(
        min_length=1,
        description="Why these rejected structured actions failed deterministic validation.",
    )
    basis: str = Field(
        min_length=1,
        description="Exact runtime schema plus committed public action arguments used for reproduction.",
    )


def _schema_validation_failures(
    records: list[dict[str, Any]],
    schema: type[BaseModel],
    *,
    outer_attempt: int,
) -> list[StructuredSchemaValidationFailure]:
    """Reproduce exact Pydantic errors for every schema-invalid action record."""

    failures: list[StructuredSchemaValidationFailure] = []
    for record in records:
        record_type = record.get("record_type") or record.get("record")
        arguments = record.get("arguments")
        if record_type != "action" or not isinstance(arguments, dict):
            continue
        try:
            schema.model_validate(arguments)
        except ValidationError as exc:
            errors = _jsonable(exc.errors(include_url=False, include_input=False))
            failures.append(
                StructuredSchemaValidationFailure(
                    outer_attempt=outer_attempt,
                    turn=int(record.get("turn") or 1),
                    tool_call_id=(
                        str(record["tool_call_id"])
                        if record.get("tool_call_id")
                        else None
                    ),
                    schema_name=schema.__name__,
                    error_count=exc.error_count(),
                    validation_error=str(exc),
                    errors_json=json.dumps(
                        errors,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                )
            )
    return failures


def _persist_schema_validation_failures(
    path: Path,
    schema: type[BaseModel],
    failures: list[StructuredSchemaValidationFailure],
) -> None:
    """Persist a complete typed schema-failure audit beside public call artifacts."""

    if not failures:
        return
    bundle = StructuredSchemaValidationBundle(
        schema_name=schema.__name__,
        failures=tuple(failures),
        reason="Rejected structured actions did not satisfy the exact runtime Pydantic response contract.",
        basis="Committed public audit arguments revalidated locally against the same runtime schema.",
    )
    path.write_text(bundle.model_dump_json(indent=2) + "\n", encoding="utf-8")


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
        if record_type == "transport_retry" and record.get("operation") == "scheduled":
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
    fallback_without_call_identity = not failed_call_ids and (
        has_provider_retry or actual_outer_retry
    )
    for row in rows:
        call_id = row.get("model_call_id")
        failed_status = row.get("status") in {"failed", "unavailable", "cancelled"}
        if (isinstance(call_id, str) and call_id in failed_call_ids) or (
            failed_status and fallback_without_call_identity
        ):
            row["cost_counted"] = False
            row["billing_disposition"] = "provider_error_retry_exempt"


def _cost_for_usage(rows: list[dict[str, Any]], pricing: Any) -> dict[str, Any]:
    if pricing is None:
        return {
            "eligible": False,
            "total_usd": 0.0,
            "unpriced_usage_count": len(
                [row for row in rows if row.get("cost_counted") is not False]
            ),
            "reason": "Profile has no pricing card; observable usage is retained but cannot be priced.",
            "attempts": [],
        }
    costs: list[dict[str, Any]] = []
    total = 0.0
    eligible = True
    for row in rows:
        if row.get("cost_counted") is False:
            costs.append(
                {
                    "eligible": True,
                    "total_usd": 0.0,
                    "billing_disposition": row.get("billing_disposition", "excluded"),
                    "outer_attempt": row.get("outer_attempt"),
                    "model_call_id": row.get("model_call_id"),
                }
            )
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
    return {
        "eligible": eligible,
        "total_usd": total,
        "unpriced_usage_count": sum(not bool(item.get("eligible")) for item in costs),
        "attempts": costs,
    }


class StructuredContextBudget(BaseModel):
    """Prompt-size, provider-token, and truncation audit for one structured call."""

    model_config = ConfigDict(extra="forbid", frozen=True, str_strip_whitespace=True)

    mode: str = Field(
        min_length=1,
        description="Structured LLM or provider-free fixture context mode.",
    )
    projection_version: str = Field(
        min_length=1,
        description="Versioned prompt projection applied before serialization.",
    )
    prompt_characters: int = Field(
        ge=0, description="Exact serialized user prompt character count."
    )
    estimated_prompt_tokens: int = Field(
        ge=0,
        description="Conservative four-characters-per-token pre-provider estimate.",
    )
    provider_input_tokens: int | None = Field(
        default=None,
        ge=0,
        description="Actual provider-reported input tokens across audited attempts, when available.",
    )
    context_window_tokens: int | None = Field(
        default=None,
        gt=0,
        description="Configured model context window, when available in the public profile.",
    )
    max_output_tokens: int = Field(
        gt=0, description="Configured maximum structured output token count."
    )
    truncation_applied: bool = Field(
        description="Whether runtime text truncation removed any supplied stage input."
    )
    projection_decision: str = Field(
        min_length=1, description="Explicit stage projection and truncation decision."
    )
    reason: str = Field(
        min_length=1, description="Non-empty explanation of context-budget handling."
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty prompt, profile, usage, and projection basis.",
    )


class StructuredCallOutcome(BaseModel, Generic[T]):
    """Auditable result of one public structured runtime cell."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    kind: str = Field(
        min_length=1, description="Runtime operation kind, such as method or judge."
    )
    status: str = Field(
        min_length=1,
        description="Terminal cell status, including success or failed diagnostics.",
    )
    response: T | None = Field(
        default=None,
        description="Validated Pydantic structured response, or null when schema/runtime handling failed.",
    )
    result: dict[str, Any] = Field(
        description="Raw public runtime result metadata retained for audit."
    )
    attempts: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Per-cell outer attempts, provider diagnostics, retry receipts, and artifact paths.",
    )
    schema_validation_failures: list[StructuredSchemaValidationFailure] = Field(
        default_factory=list,
        description="Every rejected structured action that deterministically failed the exact runtime Pydantic schema, retained across cell attempts.",
    )
    usage: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Normalized usage rows with model-call identity and billing disposition.",
    )
    cost: dict[str, Any] = Field(
        default_factory=dict,
        description="Cost calculation and eligibility for this cell's usage rows.",
    )
    context_budget: StructuredContextBudget = Field(
        description="Prompt size, provider token, model window, and truncation receipt."
    )
    real_llm: bool = Field(
        description="Whether this outcome came from the configured real provider rather than a fixture runtime."
    )
    reason: str = Field(
        min_length=1,
        description="Non-empty explanation of the structured call terminal outcome.",
    )
    basis: str = Field(
        min_length=1,
        description="Non-empty runtime, provider, schema, and retry basis for the terminal outcome.",
    )

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
            "schema_validation_failures": _jsonable(self.schema_validation_failures),
            "usage": self.usage,
            "cost": self.cost,
            "context_budget": self.context_budget.model_dump(mode="json"),
            "real_llm": self.real_llm,
            "reason": self.reason,
            "basis": self.basis,
        }


class PublicStructuredRuntime:
    """One process-local AgentApp runtime with a persistent async event loop."""

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
        self._start_event_loop()
        self._transport_model = self._submit_to_event_loop(
            self._initialize_async_runtime()
        )

    def _start_event_loop(self) -> None:
        """Start the one background event loop owned by this runtime."""

        self._event_loop: asyncio.AbstractEventLoop | None = None
        self._event_loop_start_error: BaseException | None = None
        self._event_loop_ready = threading.Event()
        self._event_loop_thread = threading.Thread(
            target=self._event_loop_main,
            name=f"structured-runtime-{self.profile}",
            daemon=True,
        )
        self._closed = False
        self._event_loop_thread.start()
        if not self._event_loop_ready.wait(timeout=10.0):
            raise RuntimeError("persistent structured-runtime event loop did not start")
        if self._event_loop_start_error is not None:
            raise RuntimeError("persistent structured-runtime event loop failed") from (
                self._event_loop_start_error
            )
        if self._event_loop is None:
            raise RuntimeError("persistent structured-runtime event loop is unavailable")

    def _event_loop_main(self) -> None:
        """Own one event loop for every async client and cell in this runtime."""

        loop: asyncio.AbstractEventLoop | None = None
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._event_loop = loop
        except Exception as exc:  # noqa: BLE001 - propagate startup across threads
            self._event_loop_start_error = exc
            self._event_loop_ready.set()
            return
        self._event_loop_ready.set()
        try:
            loop.run_forever()
        finally:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(
                    asyncio.gather(*pending, return_exceptions=True)
                )
            loop.run_until_complete(loop.shutdown_asyncgens())
            asyncio.set_event_loop(None)
            loop.close()

    def _submit_to_event_loop(self, coroutine):
        """Run one coroutine on the runtime-owned loop and return synchronously."""

        loop = self._event_loop
        if loop is None or not loop.is_running() or self._closed:
            coroutine.close()
            raise RuntimeError("persistent structured-runtime event loop is closed")
        if threading.current_thread() is self._event_loop_thread:
            coroutine.close()
            raise RuntimeError("synchronous submission from the runtime event loop")
        return asyncio.run_coroutine_threadsafe(coroutine, loop).result()

    async def _initialize_async_runtime(self):
        """Construct the model and unshared async transport inside its owner loop."""

        transport_spec = AgentSpec(
            name="evidence-discovery-persistent-transport",
            system_prompt="Persistent process-local transport holder; never invoked directly.",
            limits={"model_calls": 1, "turns": 1},
        )
        transport_app = AgentApp.from_registry(
            transport_spec,
            self.registry,
            profile=self.profile,
            model_options={
                "streaming": self.streaming,
                "max_retries": 0,
                # An unhashable timeout makes langchain-openai allocate an
                # instance-owned async httpx client instead of its global cache.
                "timeout": httpx.Timeout(
                    float(_provider_timeout_seconds(self.streaming))
                ),
            },
        )
        self._async_call_lock = asyncio.Lock()
        return transport_app.model

    async def _aclose_transport_model(self) -> None:
        """Close process-local async and sync clients before stopping the loop."""

        async_client = getattr(self._transport_model, "root_async_client", None)
        if async_client is None:
            async_client = getattr(self._transport_model, "_async_client", None)
        if async_client is not None:
            close = getattr(async_client, "close", None)
            if close is None:
                close = getattr(async_client, "aclose", None)
            if close is not None:
                close_result = close()
                if hasattr(close_result, "__await__"):
                    await close_result
        sync_client = getattr(self._transport_model, "root_client", None)
        if sync_client is not None:
            close = getattr(sync_client, "close", None)
            if close is not None:
                close()

    async def _arun_app(self, app: AgentApp, prompt: str, **options: Any):
        """Execute one app on the persistent loop with an async stage timeout."""

        async with self._async_call_lock:
            try:
                return await asyncio.wait_for(
                    app.arun(prompt, **options),
                    timeout=float(STRUCTURED_STAGE_DEADLINE_SECONDS),
                )
            except asyncio.TimeoutError as exc:
                raise StructuredStageTimeout(
                    "structured stage exceeded its local "
                    f"{STRUCTURED_STAGE_DEADLINE_SECONDS}-second deadline"
                ) from exc

    def close(self) -> None:
        """Close async clients on their owner loop and stop the loop thread."""

        if self._closed:
            return
        close_error: BaseException | None = None
        try:
            self._submit_to_event_loop(self._aclose_transport_model())
        except Exception as exc:  # noqa: BLE001 - always stop the loop after close
            close_error = exc
        finally:
            self._closed = True
            loop = self._event_loop
            if loop is not None and loop.is_running():
                loop.call_soon_threadsafe(loop.stop)
            self._event_loop_thread.join(timeout=10.0)
        if self._event_loop_thread.is_alive():
            raise RuntimeError("persistent structured-runtime event loop did not stop")
        if close_error is not None:
            raise RuntimeError("failed to close persistent async transport") from (
                close_error
            )

    def _app(
        self,
        kind: str,
        schema: type[T],
        system_prompt: str,
        *,
        streaming: bool,
    ) -> AgentApp:
        # AgentApp owns a per-run call ledger and spec. AgentApp.arun() makes a
        # shallow run-scoped model copy for callbacks, so reusing this process-
        # local base model preserves the provider client's connection pool while
        # keeping structured-output state and budgets isolated per cell.
        spec = AgentSpec(
            name=f"evidence-discovery-{kind}",
            system_prompt=system_prompt,
            output_schema=schema,
            limits={
                "model_calls": max(6, self.transport_retries + 4),
                "turns": 6,
                "model_call_seconds": PROVIDER_CALL_DEADLINE_SECONDS,
                "seconds": STRUCTURED_STAGE_DEADLINE_SECONDS,
            },
            require_tool_call=False,
            retry_missing_structured_output=True,
            transport_retry_delays_seconds=self.transport_retry_delays,
        )
        if streaming != self.streaming:
            raise ValueError(
                "process-local persistent transport requires one streaming mode"
            )
        return AgentApp(
            spec,
            self.config,
            self._transport_model,
            profile=self.profile,
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
        max_output_tokens: int | None = None,
    ) -> StructuredCallOutcome[T]:
        return self._call_unlocked(
            kind=kind,
            schema=schema,
            system_prompt=system_prompt,
            prompt=prompt,
            artifact_id=artifact_id,
            retry_cell_on_provider_error=retry_cell_on_provider_error,
            streaming=streaming,
            max_output_tokens=max_output_tokens,
        )

    def _call_unlocked(
        self,
        *,
        kind: str,
        schema: type[T],
        system_prompt: str,
        prompt: str,
        artifact_id: str,
        retry_cell_on_provider_error: bool = True,
        streaming: bool | None = None,
        max_output_tokens: int | None = None,
    ) -> StructuredCallOutcome[T]:
        use_streaming = self.streaming if streaming is None else streaming
        selected_max_output_tokens = (
            MAX_STRUCTURED_OUTPUT_TOKENS
            if max_output_tokens is None
            else max_output_tokens
        )
        if selected_max_output_tokens <= 0:
            raise ValueError("max_output_tokens must be positive")
        attempts: list[dict[str, Any]] = []
        all_usage: list[dict[str, Any]] = []
        all_schema_validation_failures: list[StructuredSchemaValidationFailure] = []
        last_result: dict[str, Any] = {}
        response: T | None = None
        status = "failed"
        max_outer_attempts = 2 if retry_cell_on_provider_error else 1
        for outer_attempt in range(1, max_outer_attempts + 1):
            attempt_dir = (
                self.artifact_root / artifact_id / f"cell-attempt-{outer_attempt}"
            )
            attempt_dir.mkdir(parents=True, exist_ok=True)
            audit_path = attempt_dir / "audit.jsonl"
            result_path = attempt_dir / "result.json"
            captured_result: dict[str, Any] | None = None
            rows: list[dict[str, Any]] = []
            try:
                result = self._submit_to_event_loop(
                    self._arun_app(
                        self._app(
                            kind,
                            schema,
                            system_prompt,
                            streaming=use_streaming,
                        ),
                        prompt,
                        renderer="quiet",
                        log_level="ERROR",
                        model_call_options={"max_tokens": selected_max_output_tokens},
                        audit_out=audit_path,
                        result_out=result_path,
                    )
                )
                captured_result = result.to_dict()
                last_result = captured_result
                audit_records = _read_audit_records(audit_path)
                schema_validation_failures = _schema_validation_failures(
                    audit_records,
                    schema,
                    outer_attempt=outer_attempt,
                )
                all_schema_validation_failures.extend(schema_validation_failures)
                schema_validation_path = attempt_dir / "schema_validation_failures.json"
                _persist_schema_validation_failures(
                    schema_validation_path,
                    schema,
                    schema_validation_failures,
                )
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
                validated_response = None
                if result.status == "success" and result.output is not None:
                    validated_response = (
                        result.output
                        if isinstance(result.output, schema)
                        else schema.model_validate(result.output)
                    )
                attempt = {
                    "outer_attempt": outer_attempt,
                    "status": result.status,
                    "provider_error": provider_error,
                    "error": error,
                    "audit_path": str(audit_path),
                    "result_path": str(result_path),
                    "usage_count": len(rows),
                    "billing_disposition": "provider_error_attempt_requires_row_level_join"
                    if provider_error
                    else "billable",
                    "retry_records": _retry_records(audit_records),
                    "schema_validation_failures": _jsonable(schema_validation_failures),
                    "schema_validation_failure_path": (
                        str(schema_validation_path)
                        if schema_validation_failures
                        else None
                    ),
                }
                attempts.append(attempt)
                if validated_response is not None:
                    response = validated_response
                    status = "success"
                    break
                if provider_error and outer_attempt < max_outer_attempts:
                    continue
                status = "failed"
                break
            except (StructuredStageTimeout, AgentError, ValueError, TypeError) as exc:
                audit_records = _read_audit_records(audit_path)
                schema_validation_failures = _schema_validation_failures(
                    audit_records,
                    schema,
                    outer_attempt=outer_attempt,
                )
                all_schema_validation_failures.extend(schema_validation_failures)
                schema_validation_path = attempt_dir / "schema_validation_failures.json"
                _persist_schema_validation_failures(
                    schema_validation_path,
                    schema,
                    schema_validation_failures,
                )
                if captured_result is not None:
                    artifact_result = captured_result
                    recovery_source = "in_memory_public_result"
                else:
                    artifact_result, recovery_source = _read_result_artifact(
                        result_path
                    )
                    rows = _usage_rows(
                        artifact_result or {},
                        outer_attempt=outer_attempt,
                    )
                    all_usage.extend(rows)
                if artifact_result is not None:
                    last_result = artifact_result
                if isinstance(exc, StructuredStageTimeout):
                    error_payload = {
                        "code": "structured_stage_timeout",
                        "message": str(exc),
                        "phase": "local_runtime",
                    }
                    if not rows:
                        rows = [
                            {
                                "model_call_id": None,
                                "status": "cancelled",
                                "input_tokens": None,
                                "output_tokens": None,
                                "source": "unavailable",
                                "unavailable_reason": recovery_source,
                                "cost_counted": True,
                                "billing_disposition": "billable_usage_unavailable",
                                "outer_attempt": outer_attempt,
                            }
                        ]
                        all_usage.extend(rows)
                elif isinstance(exc, AgentError):
                    error_payload = {
                        "code": exc.code,
                        "message": exc.message,
                        "details": _jsonable(exc.details),
                    }
                else:
                    error_payload = {
                        "code": type(exc).__name__,
                        "message": str(exc),
                        "phase": "local_runtime",
                    }
                provider_error = _is_provider_error(error_payload)
                actual_outer_retry = bool(
                    provider_error and outer_attempt < max_outer_attempts
                )
                _annotate_usage_billing(
                    rows,
                    audit_records=audit_records,
                    final_error=error_payload,
                    actual_outer_retry=actual_outer_retry,
                )
                attempts.append(
                    {
                        "outer_attempt": outer_attempt,
                        "status": "exception",
                        "provider_error": provider_error,
                        "error": error_payload,
                        "audit_path": str(audit_path),
                        "result_path": str(result_path),
                        "usage_count": len(rows),
                        "usage_recovery": {
                            "status": (
                                "recovered"
                                if artifact_result is not None and rows
                                else "recovered_without_rows"
                                if artifact_result is not None
                                else "unavailable"
                            ),
                            "source": recovery_source,
                            "result_path": str(result_path),
                            "reason": (
                                "Usage rows were recovered from the committed public result artifact."
                                if rows
                                and recovery_source == "committed_result_artifact"
                                else "Usage rows were retained from the in-memory public result before local validation failed."
                                if rows and recovery_source == "in_memory_public_result"
                                else "No committed usage rows were available; cost remains explicitly unobserved rather than assumed to be zero."
                            ),
                        },
                        "billing_disposition": "provider_error_attempt_requires_row_level_join"
                        if provider_error
                        else "billable",
                        "retry_records": _retry_records(audit_records),
                        "schema_validation_failures": _jsonable(
                            schema_validation_failures
                        ),
                        "schema_validation_failure_path": (
                            str(schema_validation_path)
                            if schema_validation_failures
                            else None
                        ),
                    }
                )
                if provider_error and outer_attempt < max_outer_attempts:
                    continue
                status = "failed"
                last_result = (
                    {**artifact_result, "wrapper_error": error_payload}
                    if artifact_result is not None
                    else {"status": "failed", "error": error_payload}
                )
                break
        cost = _cost_for_usage(all_usage, self.config.pricing)
        provider_input_tokens = sum(
            int(row["input_tokens"])
            for row in all_usage
            if isinstance(row.get("input_tokens"), int)
        )
        context_budget = StructuredContextBudget(
            mode="structured_llm",
            projection_version="stage-context-projection.v6",
            prompt_characters=len(prompt),
            estimated_prompt_tokens=(len(prompt) + 3) // 4,
            provider_input_tokens=(provider_input_tokens if all_usage else None),
            context_window_tokens=self.config.context_window_tokens,
            max_output_tokens=selected_max_output_tokens,
            truncation_applied=False,
            projection_decision="The stage-specific structured projection was serialized in full; runtime text truncation was not applied.",
            reason="The call records both the pre-provider prompt size and actual provider usage when available.",
            basis="stage-context-projection.v6, utils.llm profile limits, and normalized usage rows",
        )
        return StructuredCallOutcome(
            kind=kind,
            status=status,
            response=response,
            result=last_result,
            attempts=attempts,
            schema_validation_failures=all_schema_validation_failures,
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
                f"stream_first_byte_timeout={PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS}s; "
                f"provider_call_deadline={PROVIDER_CALL_DEADLINE_SECONDS}s; "
                f"structured_stage_deadline={STRUCTURED_STAGE_DEADLINE_SECONDS}s"
            ),
        )


class FixtureStructuredRuntime:
    """Provider-free structured runtime for end-to-end fixture smoke runs.

    This fixture returns no semantic candidates or judge relations. Dynamic
    grounding schemas still receive explicit unbound rows for every required
    cardinality contract, so structural coverage is exercised without making a
    semantic domain choice. It is never used for live results and carries no
    ledger payload.
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
        selected_max_output_tokens = int(
            kwargs.get("max_output_tokens") or MAX_STRUCTURED_OUTPUT_TOKENS
        )
        if schema.__name__ == "NLContractResponse":
            payload: dict[str, Any] = {
                "contracts": [],
                "segment_disposition": {},
                "reason": "Fixture contract output leaves semantic extraction to the fallback receipt.",
                "basis": "provider-free fixture runtime",
            }
        elif any(base.__name__ == "GroundingResponse" for base in schema.__mro__):
            cardinality_contract_ids = tuple(
                getattr(schema, "expected_cardinality_contract_ids", ())
            )
            payload = {
                "lens": (
                    "behavior_consequence"
                    if artifact_id.endswith("/behavior_consequence")
                    else "contract_structure_contrast"
                ),
                "additional_contracts": [],
                "cardinality_bindings": [
                    {
                        "binding_id": f"CARD-BIND-FIXTURE-{index}",
                        "contract_id": contract_id,
                        "status": "unbound",
                        "member_domain": "unresolved",
                        "owner_source_id": None,
                        "owner_model_ref": None,
                        "alternative_reading": None,
                        "reason": "The provider-free fixture cannot select a semantic member domain or exact owner.",
                        "basis": "provider-free fixture runtime; no provider semantic judgment was performed",
                    }
                    for index, contract_id in enumerate(
                        cardinality_contract_ids,
                        start=1,
                    )
                ],
                "candidates": [],
                "unresolved": [],
                "reason": "Fixture grounding output leaves candidate generation to the fallback receipt.",
                "basis": "provider-free fixture runtime",
            }
        elif schema.__name__ == "DAdjudicationResponse":
            parts = artifact_id.split("/")
            pair_id = parts[1] if len(parts) > 1 else "fixture"
            round_id = next(
                (item for item in parts if item.startswith("round-")), "round-1"
            )
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
            # The empty fixture response must fail the exact judge shape check;
            # no ledger/release assessment is synthesized by deterministic code.
            payload = {
                "ledger_assessments": [],
                "release_assessments": [],
                "reason": "Fixture judge output intentionally leaves semantic relations unavailable.",
                "basis": "provider-free fixture runtime",
            }
        response = schema.model_validate(payload)
        context_budget = StructuredContextBudget(
            mode="provider_free_fixture",
            projection_version="stage-context-projection.v6",
            prompt_characters=len(prompt),
            estimated_prompt_tokens=(len(prompt) + 3) // 4,
            provider_input_tokens=None,
            context_window_tokens=None,
            max_output_tokens=selected_max_output_tokens,
            truncation_applied=False,
            projection_decision="The provider-free fixture consumed the complete serialized stage projection without truncation.",
            reason="Fixture prompt size is recorded even though no provider token usage exists.",
            basis="provider-free fixture runtime and stage-context-projection.v6",
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
