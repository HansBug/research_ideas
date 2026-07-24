from __future__ import annotations

import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, TypeVar

from pydantic import BaseModel

from utils.llm import (
    adapter_name,
    create_chat_model,
    load_llm_registry,
    normalize_model_output_usage,
)

T = TypeVar("T", bound=BaseModel)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    return repr(value)


@dataclass(frozen=True)
class LLMObservation:
    llm_call_id: str
    role: str
    profile: str
    adapter: str
    provider: str
    configured_model: str
    observed_model: str | None
    started_at: datetime
    finished_at: datetime
    elapsed_ms: float
    status: str
    system_prompt: str
    user_prompt: str
    parsed_output: dict[str, Any] | None
    raw_response: dict[str, Any] | None
    usage: dict[str, Any]
    attempts: tuple[dict[str, Any], ...]
    failure: str | None = None


class DirectStructuredResponder:
    """One provider-neutral structured LLM response per graph node.

    The responder deliberately has no AgentApp, tools, ReAct loop, or hidden
    model switch. Every call uses the single profile selected for the run.
    Provider/transport retries are visible as attempt observations and do not
    become business revisions.
    """

    def __init__(
        self,
        profile: str,
        *,
        registry_path: str | None = None,
        max_output_tokens: int | None = None,
        transport_retries: int = 2,
    ) -> None:
        registry = load_llm_registry(registry_path)
        self.profile = profile
        self.config = registry.require(profile)
        model_options = (
            {"max_tokens": max_output_tokens}
            if max_output_tokens is not None and self.config.adapter == "anthropic"
            else (
                {"max_completion_tokens": max_output_tokens}
                if max_output_tokens is not None
                else None
            )
        )
        self.model = create_chat_model(
            self.config,
            model_options=model_options,
            streaming=False,
            max_retries=0,
        )
        self.transport_retries = max(0, transport_retries)
        self._last_observation: LLMObservation | None = None

    def take_last_observation(self) -> LLMObservation | None:
        observation = self._last_observation
        self._last_observation = None
        return observation

    def invoke_structured(
        self, *, role: str, schema: type[T], system_prompt: str, user_input: str
    ) -> T:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("langchain_core is required for live discovery") from exc

        call_started = _utc_now()
        call_start_ns = time.perf_counter_ns()
        attempts: list[dict[str, Any]] = []
        last_error: Exception | None = None
        for attempt_index in range(1, self.transport_retries + 2):
            attempt_started = _utc_now()
            attempt_start_ns = time.perf_counter_ns()
            raw: Any = None
            try:
                structured = self.model.with_structured_output(schema, include_raw=True)
                response = structured.invoke(
                    [SystemMessage(system_prompt), HumanMessage(user_input)]
                )
                if not isinstance(response, dict):
                    raise TypeError("include_raw structured response must be a mapping")
                raw = response.get("raw")
                parsing_error = response.get("parsing_error")
                if parsing_error is not None:
                    raise ValueError(f"structured validation failed: {parsing_error}")
                parsed = response.get("parsed")
                output = parsed if isinstance(parsed, schema) else schema.model_validate(parsed)
                usage = normalize_model_output_usage(raw)
                metadata = getattr(raw, "response_metadata", {}) or {}
                observed_model = (
                    metadata.get("model_name") or metadata.get("model")
                    if isinstance(metadata, dict)
                    else None
                )
                attempts.append(
                    {
                        "attempt_index": attempt_index,
                        "started_at": attempt_started.isoformat(),
                        "finished_at": _utc_now().isoformat(),
                        "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns) / 1_000_000,
                        "status": "completed",
                        "failure_phase": "none",
                        "retryable": False,
                        "usage": usage,
                    }
                )
                finished = _utc_now()
                self._last_observation = LLMObservation(
                    llm_call_id=str(uuid.uuid4()),
                    role=role,
                    profile=self.profile,
                    adapter=self.config.adapter,
                    provider=adapter_name(self.config.adapter),
                    configured_model=self.config.model,
                    observed_model=str(observed_model) if observed_model else None,
                    started_at=call_started,
                    finished_at=finished,
                    elapsed_ms=(time.perf_counter_ns() - call_start_ns) / 1_000_000,
                    status="completed",
                    system_prompt=system_prompt,
                    user_prompt=user_input,
                    parsed_output=output.model_dump(mode="json"),
                    raw_response=_jsonable(raw),
                    usage=usage,
                    attempts=tuple(attempts),
                )
                return output
            except Exception as exc:
                last_error = exc
                retryable = not isinstance(exc, (ValueError, TypeError))
                attempts.append(
                    {
                        "attempt_index": attempt_index,
                        "started_at": attempt_started.isoformat(),
                        "finished_at": _utc_now().isoformat(),
                        "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns) / 1_000_000,
                        "status": "failed",
                        "failure_phase": (
                            "structured_validation"
                            if isinstance(exc, (ValueError, TypeError))
                            else "transport"
                        ),
                        "retryable": retryable,
                        "error_category": type(exc).__name__,
                        "error_message": str(exc),
                        "raw_response": _jsonable(raw),
                    }
                )
                if not retryable or attempt_index > self.transport_retries:
                    break

        finished = _utc_now()
        unavailable = normalize_model_output_usage(None, status="failed")
        self._last_observation = LLMObservation(
            llm_call_id=str(uuid.uuid4()),
            role=role,
            profile=self.profile,
            adapter=self.config.adapter,
            provider=adapter_name(self.config.adapter),
            configured_model=self.config.model,
            observed_model=None,
            started_at=call_started,
            finished_at=finished,
            elapsed_ms=(time.perf_counter_ns() - call_start_ns) / 1_000_000,
            status="failed",
            system_prompt=system_prompt,
            user_prompt=user_input,
            parsed_output=None,
            raw_response=None,
            usage=unavailable,
            attempts=tuple(attempts),
            failure=f"{type(last_error).__name__}: {last_error}" if last_error else "unknown failure",
        )
        raise RuntimeError(self._last_observation.failure) from last_error


__all__ = ["DirectStructuredResponder", "LLMObservation"]
