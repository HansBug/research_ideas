from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from collections.abc import Callable
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


def _status_code(exc: Exception) -> int | None:
    value = getattr(exc, "status_code", None)
    if isinstance(value, int):
        return value
    response = getattr(exc, "response", None)
    value = getattr(response, "status_code", None)
    return value if isinstance(value, int) else None


def _empty_structured_output(exc: Exception) -> bool:
    """True when validation failed because nothing was assembled at all.

    A streamed tool call whose ``partial_json`` never gets merged surfaces as a
    pydantic ``model_type`` error against ``None`` rather than as an incomplete
    stream.  That is a transport symptom, not the model violating the schema --
    on pair 0006 the provider had in fact emitted a well-formed RequirementSet.
    Treating it as a permanent contract error killed the whole run on attempt 1.
    """

    errors = getattr(exc, "errors", None)
    if not callable(errors):
        return False
    try:
        items = errors()
    except Exception:  # pragma: no cover - defensive
        return False
    return any(
        item.get("type") == "model_type"
        and item.get("input") is None
        and not item.get("loc")
        for item in items
        if isinstance(item, dict)
    )


def _retryable_error(exc: Exception) -> bool:
    if isinstance(exc, IncompleteStructuredStreamError):
        return True
    if _empty_structured_output(exc):
        return True
    if isinstance(exc, (ValueError, TypeError)):
        return False
    status = _status_code(exc)
    if status is None:
        return True
    return status in {408, 409, 425, 429} or status >= 500


class IncompleteStructuredStreamError(RuntimeError):
    """The provider ended a structured stream before its tool-call JSON closed."""


def _validate_complete_structured_stream(raw: Any) -> None:
    """Reject partial tool-call payloads that LangChain may parse with defaults.

    Structured streaming can expose a partially accumulated ``tool_call_chunks``
    payload while the parsed Pydantic object already exists.  The latter is not
    sufficient evidence that the provider response was complete: omitted fields
    may have been filled from schema defaults.  Validate the accumulated raw
    arguments before accepting the parsed value.
    """

    invalid_tool_calls = getattr(raw, "invalid_tool_calls", None)
    if invalid_tool_calls:
        raise IncompleteStructuredStreamError(
            "provider returned invalid structured tool-call chunks"
        )
    tool_call_chunks = getattr(raw, "tool_call_chunks", None)
    if not tool_call_chunks:
        return
    for index, chunk in enumerate(tool_call_chunks):
        if not isinstance(chunk, dict):
            continue
        args = chunk.get("args")
        if isinstance(args, str):
            try:
                json.loads(args)
            except json.JSONDecodeError as exc:
                raise IncompleteStructuredStreamError(
                    f"structured tool-call arguments are incomplete at chunk {index}"
                ) from exc


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
        on_stream_chunk: Callable[[str, int, float], None] | None = None,
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
            streaming=True,
            max_retries=0,
        )
        self.transport_retries = max(0, transport_retries)
        self._on_stream_chunk = on_stream_chunk
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
                structured_options: dict[str, Any] = {"include_raw": True}
                if self.config.adapter in {"openai", "openai-responses"}:
                    # Function calling accepts Pydantic defaults/unions that the
                    # stricter OpenAI response_format JSON-schema subset rejects.
                    # This is still one direct model response, not a business-tool loop.
                    structured_options["method"] = "function_calling"
                structured = self.model.with_structured_output(
                    schema, **structured_options
                )
                response = None
                chunk_count = 0
                for chunk in structured.stream(
                    [SystemMessage(system_prompt), HumanMessage(user_input)]
                ):
                    chunk_count += 1
                    response = chunk if response is None else response + chunk
                    if self._on_stream_chunk is not None:
                        self._on_stream_chunk(
                            role,
                            chunk_count,
                            (time.perf_counter_ns() - attempt_start_ns) / 1_000_000,
                        )
                if response is None:
                    raise RuntimeError("structured stream produced no response")
                if not isinstance(response, dict):
                    raise TypeError("include_raw structured response must be a mapping")
                raw = response.get("raw")
                parsing_error = response.get("parsing_error")
                if parsing_error is not None:
                    raise ValueError(f"structured validation failed: {parsing_error}")
                _validate_complete_structured_stream(raw)
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
                retryable = _retryable_error(exc)
                status = _status_code(exc)
                failure_phase = (
                    "structured_stream"
                    if isinstance(exc, IncompleteStructuredStreamError)
                    else
                    "structured_validation"
                    if isinstance(exc, (ValueError, TypeError))
                    else "provider_response"
                    if status is not None
                    else "transport"
                )
                attempts.append(
                    {
                        "attempt_index": attempt_index,
                        "started_at": attempt_started.isoformat(),
                        "finished_at": _utc_now().isoformat(),
                        "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns) / 1_000_000,
                        "status": "failed",
                        "failure_phase": failure_phase,
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
