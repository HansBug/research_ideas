from __future__ import annotations

import functools
import hashlib
import json
import time
import uuid
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, TypeVar

from pydantic import BaseModel

from utils.llm import (
    PromptCacheTTL,
    adapter_name,
    cached_system_prompt_content,
    create_chat_model,
    load_llm_registry,
    normalize_model_output_usage,
    prompt_cache_policy,
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
    except Exception:  # noqa: BLE001  # pragma: no cover - third-party exception API
        return False
    return any(
        item.get("type") == "model_type"
        and item.get("input") is None
        and not item.get("loc")
        for item in items
        if isinstance(item, dict)
    )


#: Seconds to wait before each retry.  Retrying with no gap is what made the
#: existing budget useless: pair 0029's three attempts were issued 9 microseconds
#: apart and all three landed inside the same 60-second Cloudflare 504 window, so
#: the cell spent three minutes to fail exactly as it would have on one attempt.
#: The schedule is deliberately longer than a gateway timeout, and long enough
#: that a rate limit has a chance to clear.
TRANSPORT_RETRY_DELAYS: tuple[float, ...] = (5.0, 20.0, 60.0, 120.0, 240.0)


def _provider_retry_after_seconds(exc: BaseException) -> float | None:
    """Read a numeric `Retry-After` hint off the provider exception, if any.

    The provider knows better than any schedule when it will be ready; honouring
    the header keeps a 429 from being retried into another 429.
    """

    seen: list[BaseException] = []
    item: BaseException | None = exc
    while item is not None and item not in seen:
        seen.append(item)
        response = getattr(item, "response", None)
        headers = getattr(response, "headers", None) or getattr(item, "headers", None)
        if isinstance(headers, Mapping):
            raw = headers.get("retry-after") or headers.get("Retry-After")
            try:
                value = float(raw)
            except (TypeError, ValueError):
                value = 0.0
            if value > 0:
                return value
        body = getattr(item, "body", None)
        if isinstance(body, Mapping):
            try:
                value = float(body.get("retry_after"))
            except (TypeError, ValueError):
                value = 0.0
            if value > 0:
                return value
        item = item.__cause__ or item.__context__
    return None


def _retry_delay(exc: BaseException, retry_index: int) -> float:
    """How long to wait before retry number ``retry_index`` (0-based)."""

    hinted = _provider_retry_after_seconds(exc)
    if hinted is not None:
        return hinted
    if retry_index < len(TRANSPORT_RETRY_DELAYS):
        return TRANSPORT_RETRY_DELAYS[retry_index]
    return TRANSPORT_RETRY_DELAYS[-1]


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


@functools.cache
def _schema_contract(schema: type[Any]) -> str:
    """用 LangChain 原生的 `PydanticOutputParser` 把字段契约渲染进 system prompt。

    ⚠️ 为什么必须进 prompt 文本，而不是只靠 `with_structured_output(schema)`：
    后者只把**类型**约束交给 provider 的 tool schema，字段的**语义**（哪个值合法、
    为什么、与其他字段的关系）不在其中。实测代价 ——

    * `revision` 的语义只在 prompt 里以「on revise, increase the revision」一句自然语言出现，
      生产者连续 5 次发同一个值，把契约修复预算耗尽后整格失败（`diag-0047-v28/run3`）；
    * 而 `Requirement.predicate_bindings` 这类字段的说明写在 Python `#:` 注释里，
      **注释不进 `model_json_schema()`**，生产者看到的只有 `{"type": "object"}`。

    ⛔ 不要手写这段 schema 说明。手写会与模型定义脱同步，而脱同步的契约比没有契约更糟 ——
    它让生产者按一份过期的说明去满足一份现行的校验。`get_format_instructions()` 从同一个
    Pydantic 模型生成，改字段就自动改说明。

    字段语义应写在 `Field(description=...)` 里（它进 schema），不要只写成 `#` 注释。

    ⛔ 本函数**不捕获异常**。渲染失败若被降级成空串，运行会照常继续，只是生产者从此看不到字段契约 ——
    而那正是它存在的唯一理由。契约悄悄消失、指标随之变差、日志里却什么都没有，是最难定位的一类失败。
    渲染不出来就明着炸，让它在第一次调用时就暴露。
    """

    from langchain_core.output_parsers import PydanticOutputParser

    return (
        "\n\n" + PydanticOutputParser(pydantic_object=schema).get_format_instructions()
    )


class IncompleteStructuredStreamError(RuntimeError):
    """The provider ended a structured stream before its tool-call JSON closed."""


class StructuredOutputValidationError(RuntimeError):
    """The provider returned content that does not satisfy the requested schema."""


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
    structured_schema_sha256: str
    schema_contract_repeated_in_prompt: bool
    prompt_cache: dict[str, Any]
    pricing: dict[str, Any] | None
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
        transport_retries: int = 4,
        repeat_schema_in_prompt: bool = True,
        prompt_cache_ttl: PromptCacheTTL | None = None,
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
        self.repeat_schema_in_prompt = repeat_schema_in_prompt
        self.prompt_cache_ttl = prompt_cache_ttl
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
        schema_json = json.dumps(
            schema.model_json_schema(),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        structured_schema_sha256 = hashlib.sha256(schema_json.encode()).hexdigest()
        effective_system_prompt = system_prompt + (
            _schema_contract(schema) if self.repeat_schema_in_prompt else ""
        )
        prompt_cache = (
            prompt_cache_policy(self.config, ttl=self.prompt_cache_ttl)
            if self.prompt_cache_ttl is not None
            else {"mode": "disabled", "enabled": False, "ttl": None}
        )
        system_message_content = cached_system_prompt_content(
            self.config,
            effective_system_prompt,
            ttl=self.prompt_cache_ttl,
        )
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
                for chunk_count, chunk in enumerate(
                    structured.stream(
                        [
                            SystemMessage(content=system_message_content),
                            HumanMessage(user_input),
                        ]
                    ),
                    start=1,
                ):
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
                    raise StructuredOutputValidationError(
                        f"structured validation failed: {parsing_error}"
                    )
                _validate_complete_structured_stream(raw)
                parsed = response.get("parsed")
                if parsed is None:
                    # `with_structured_output(include_raw=True)` 的 docstring 承诺「The final
                    # output is always a dict with keys 'raw', 'parsed', and 'parsing_error'」，
                    # 但流式路径违反了它：`BaseCumulativeTransformOutputParser._transform`
                    # (transform.py:142) 恒定以 `partial=True` 调 parser，而
                    # `PydanticToolsParser.parse_result` 在 partial 下把 `ValidationError`
                    # `continue` 掉 (openai_tools.py:369-371)，返回 None → 什么都不 yield →
                    # `parsed` 键从不出现，异常没逃逸所以 `parsing_error` 也保持 None。
                    #
                    # 后果不是少个字段，是**把内容违约伪装成传输故障**：`schema.model_validate(None)`
                    # 抛出的 `model_type / input_value=None` 被 `_empty_structured_output` 判为
                    # 可重试，于是用完全相同的输入重试到底，真实的校验错误一次都没回到生产者手上。
                    # 全仓 340 条「模型正常收尾、内容完整」的失败都栽在这条通道上。
                    #
                    # 官方对「结构化 + 流式」这个组合没有 1.x 说明；v0.3 文档只说过 Pydantic
                    # schema 不在可流式范围内。所以这里不改架构，只把库吞掉的那次校验按
                    # `partial=False` 的语义重放一遍，让真因浮出来。
                    tool_calls = getattr(raw, "tool_calls", None) or []
                    if tool_calls:
                        # 抛出的是真实的 ValidationError，`_empty_structured_output` 不会认它
                        # （它带 loc，且 input 不是 None），因此按不可重试处理 —— 内容违约重试无益。
                        output = schema.model_validate(tool_calls[0].get("args"))
                    else:
                        raise IncompleteStructuredStreamError(
                            "structured stream produced neither a parsed object nor a tool call; "
                            f"stop_reason={getattr(raw, 'response_metadata', {}).get('stop_reason')!r}"
                        )
                else:
                    output = (
                        parsed
                        if isinstance(parsed, schema)
                        else schema.model_validate(parsed)
                    )
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
                        "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns)
                        / 1_000_000,
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
                    system_prompt=effective_system_prompt,
                    user_prompt=user_input,
                    parsed_output=output.model_dump(mode="json"),
                    raw_response=_jsonable(raw),
                    usage=usage,
                    attempts=tuple(attempts),
                    structured_schema_sha256=structured_schema_sha256,
                    schema_contract_repeated_in_prompt=self.repeat_schema_in_prompt,
                    prompt_cache=prompt_cache,
                    pricing=(
                        self.config.pricing.model_dump(mode="json")
                        if self.config.pricing is not None
                        else None
                    ),
                )
                return output
            except Exception as exc:  # noqa: BLE001 - provider SDKs use mixed errors
                last_error = exc
                retryable = _retryable_error(exc)
                status = _status_code(exc)
                failure_phase = (
                    "structured_stream"
                    if isinstance(exc, IncompleteStructuredStreamError)
                    else "structured_validation"
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
                        "elapsed_ms": (time.perf_counter_ns() - attempt_start_ns)
                        / 1_000_000,
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
                delay = _retry_delay(exc, attempt_index - 1)
                attempts[-1]["retry_after_seconds"] = delay
                time.sleep(delay)

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
            system_prompt=effective_system_prompt,
            user_prompt=user_input,
            parsed_output=None,
            raw_response=None,
            usage=unavailable,
            attempts=tuple(attempts),
            structured_schema_sha256=structured_schema_sha256,
            schema_contract_repeated_in_prompt=self.repeat_schema_in_prompt,
            prompt_cache=prompt_cache,
            pricing=(
                self.config.pricing.model_dump(mode="json")
                if self.config.pricing is not None
                else None
            ),
            failure=f"{type(last_error).__name__}: {last_error}"
            if last_error
            else "unknown failure",
        )
        if isinstance(last_error, StructuredOutputValidationError):
            raise last_error
        if isinstance(last_error, (ValueError, TypeError)):
            raise StructuredOutputValidationError(
                self._last_observation.failure
            ) from last_error
        raise RuntimeError(self._last_observation.failure) from last_error


__all__ = [
    "DirectStructuredResponder",
    "LLMObservation",
    "StructuredOutputValidationError",
]
