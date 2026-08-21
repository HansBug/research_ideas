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
        "timeout",
        "connection",
        "http_5",
        "http_4",
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
    call_ids: set[str] = set()
    for record in records:
        record_type = record.get("record_type") or record.get("record")
        if record_type == "transport_retry":
            if record.get("operation") in {"scheduled", "exhausted"}:
                call_id = record.get("failed_model_call_id")
                if isinstance(call_id, str) and call_id:
                    call_ids.add(call_id)
        elif record_type == "model_failed" and _is_provider_error(record.get("error")):
            call_id = record.get("model_call_id")
            if isinstance(call_id, str) and call_id:
                call_ids.add(call_id)
    if _is_provider_error(final_error):
        # A terminal provider error may not expose a model call id. Only rows
        # explicitly marked as failed/unavailable are eligible for this
        # fallback; completed earlier calls in the same cell remain billable.
        return call_ids
    return call_ids


def _annotate_usage_billing(
    rows: list[dict[str, Any]],
    *,
    audit_records: list[dict[str, Any]],
    final_error: dict[str, Any] | None,
) -> None:
    """Attach billing decisions to the specific failed provider attempts.

    The public AgentApp result contains normalized usage, while transport retry
    identity is emitted in its audit JSONL. Joining them here keeps provider
    retry exemptions local to the failed model call and leaves all other calls
    in the same cell billable.
    """

    failed_call_ids = _provider_failure_call_ids(audit_records, final_error)
    has_provider_retry = bool(_retry_records(audit_records))
    terminal_provider_error = _is_provider_error(final_error)
    for row in rows:
        call_id = row.get("model_call_id")
        failed_status = row.get("status") in {"failed", "unavailable", "cancelled"}
        if (isinstance(call_id, str) and call_id in failed_call_ids) or (
            failed_status and (has_provider_retry or terminal_provider_error)
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
        }


class PublicStructuredRuntime:
    """One public AgentApp wrapper shared by method and independent judge."""

    def __init__(self, profile: str, artifact_root: Path):
        self.profile = profile
        self.artifact_root = artifact_root
        self.artifact_root.mkdir(parents=True, exist_ok=True)
        self.registry = load_llm_registry()
        self.config = self.registry.require(profile)
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
            limits={"model_calls": 4, "turns": 4},
            require_tool_call=False,
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
        streaming: bool = True,
    ) -> StructuredCallOutcome[T]:
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
                        streaming=streaming,
                    ).run(
                        prompt,
                        renderer="quiet",
                        log_level="ERROR",
                        model_call_options={"max_tokens": 8000},
                        audit_out=audit_path,
                        result_out=result_path,
                    )
                last_result = result.to_dict()
                audit_records = _read_audit_records(audit_path)
                rows = _usage_rows(result, outer_attempt=outer_attempt)
                all_usage.extend(rows)
                error = result.error if isinstance(result.error, dict) else None
                _annotate_usage_billing(
                    rows,
                    audit_records=audit_records,
                    final_error=error,
                )
                provider_error = _is_provider_error(error)
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
        return StructuredCallOutcome(
            kind=kind,
            status=status,
            response=response,
            result=last_result,
            attempts=attempts,
            usage=all_usage,
            cost=cost,
        )


class FixtureStructuredRuntime:
    """Provider-free structured runtime for end-to-end fixture smoke runs.

    This fixture intentionally returns empty grounding and judge surfaces so
    the method's no-silent-drop fallbacks, typed D coverage checks, receipts,
    and independent-judge normalization are exercised without credentials.
    It is never used for live results and carries no ledger payload.
    """

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
        return StructuredCallOutcome(
            kind=kind,
            status="success",
            response=response,
            result={"call_id": f"fixture:{kind}"},
            attempts=[],
            usage=[],
            cost={"eligible": True, "total_usd": 0.0, "attempts": []},
        )
