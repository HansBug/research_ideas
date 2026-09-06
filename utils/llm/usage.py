from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any, TypedDict

try:  # pragma: no cover - exercised when langchain-core is installed.
    from langchain_core.messages import BaseMessage
except ImportError:  # pragma: no cover
    BaseMessage = ()  # type: ignore[assignment]


class UsageSource(TypedDict):
    source: str
    usage: dict[str, Any]


_NORMALIZED_KEYS = (
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
    "ephemeral_5m_input_tokens",
    "ephemeral_1h_input_tokens",
    "reasoning_tokens",
)


def _safe_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _safe_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_safe_json(item) for item in value]
    if isinstance(value, (str, int, bool)) or value is None:
        return value
    if isinstance(value, float):
        return value if math.isfinite(value) else repr(value)
    return repr(value)


def _messages_from_event(value: Any) -> list[Any]:
    if isinstance(BaseMessage, type) and isinstance(value, BaseMessage):
        return [value]
    if isinstance(value, Mapping):
        value = value.get("messages", [])
    if isinstance(value, (list, tuple)):
        messages: list[Any] = []
        for item in value:
            update = getattr(item, "update", None)
            if update is not None:
                messages.extend(_messages_from_event(update))
            elif isinstance(item, Mapping) and "update" in item:
                messages.extend(_messages_from_event(item["update"]))
            elif isinstance(BaseMessage, type) and isinstance(item, BaseMessage):
                messages.append(item)
        return messages
    update = getattr(value, "update", None)
    if update is not None:
        return _messages_from_event(update)
    return []


def model_output_messages(value: Any) -> list[Any]:
    """Return messages from standard LangChain model outputs/events."""

    if isinstance(BaseMessage, type) and isinstance(value, BaseMessage):
        return [value]
    generations = getattr(value, "generations", None)
    if generations:
        messages: list[Any] = []
        for generation_group in generations:
            items = generation_group if isinstance(generation_group, (list, tuple)) else (generation_group,)
            for generation in items:
                message = getattr(generation, "message", None)
                if isinstance(BaseMessage, type) and isinstance(message, BaseMessage):
                    messages.append(message)
        return messages
    return _messages_from_event(value)


def collect_usage_sources(value: Any) -> list[UsageSource]:
    """Collect public LangChain/provider usage surfaces without choosing one."""

    sources: list[UsageSource] = []
    llm_output = getattr(value, "llm_output", None)
    if llm_output is None and isinstance(value, Mapping):
        llm_output = value.get("llm_output")
    if isinstance(llm_output, Mapping):
        usage_value = llm_output.get("token_usage") or llm_output.get("usage")
        if isinstance(usage_value, Mapping):
            sources.append({"source": "llm_output.token_usage", "usage": dict(usage_value)})
    for message in model_output_messages(value):
        usage_metadata = getattr(message, "usage_metadata", None)
        if isinstance(usage_metadata, Mapping):
            sources.append({"source": "usage_metadata", "usage": dict(usage_metadata)})
        response_metadata = getattr(message, "response_metadata", {}) or {}
        if isinstance(response_metadata, Mapping):
            usage_value = response_metadata.get("token_usage") or response_metadata.get("usage")
            if isinstance(usage_value, Mapping):
                sources.append({"source": "response_metadata.token_usage", "usage": dict(usage_value)})
    return sources


def usage_number(usage: Mapping[str, Any] | None, *keys: str) -> int | None:
    """Return the first non-negative finite integer-like usage value."""

    if not isinstance(usage, Mapping):
        return None
    for key in keys:
        value = usage.get(key)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)) and math.isfinite(float(value)) and value >= 0:
            return int(value)
    return None


def _first_number(*values: int | None) -> int | None:
    return next((value for value in values if value is not None), None)


def input_cache_details(usage: Mapping[str, Any] | None) -> dict[str, int | None]:
    """Normalize cache read/creation fields while preserving Anthropic TTLs."""

    if not isinstance(usage, Mapping):
        return {
            "cache_read_input_tokens": None,
            "cache_creation_input_tokens": None,
            "ephemeral_5m_input_tokens": None,
            "ephemeral_1h_input_tokens": None,
        }
    details = usage.get("input_token_details")
    details = details if isinstance(details, Mapping) else {}
    prompt_details = usage.get("prompt_tokens_details")
    prompt_details = prompt_details if isinstance(prompt_details, Mapping) else {}
    raw_creation = usage.get("cache_creation")
    raw_creation = raw_creation if isinstance(raw_creation, Mapping) else {}

    cache_read = _first_number(
        usage_number(details, "cache_read", "cached_tokens", "cache_read_input_tokens"),
        usage_number(prompt_details, "cached_tokens", "cache_read", "cache_read_input_tokens"),
        usage_number(usage, "cache_read_input_tokens", "prompt_cache_hit_tokens", "cached_tokens", "cache_read"),
    )
    creation_5m = _first_number(
        usage_number(details, "ephemeral_5m_input_tokens"),
        usage_number(raw_creation, "ephemeral_5m_input_tokens"),
        usage_number(usage, "ephemeral_5m_input_tokens"),
    )
    creation_1h = _first_number(
        usage_number(details, "ephemeral_1h_input_tokens"),
        usage_number(raw_creation, "ephemeral_1h_input_tokens"),
        usage_number(usage, "ephemeral_1h_input_tokens"),
    )
    generic_creation = _first_number(
        usage_number(details, "cache_creation", "cache_creation_input_tokens", "cache_write_tokens"),
        usage_number(usage, "cache_creation_input_tokens", "cache_write_tokens", "prompt_cache_miss_tokens"),
        usage_number(usage, "cache_creation") if not raw_creation else None,
    )
    ttl_values = [value for value in (creation_5m, creation_1h) if value is not None]
    ttl_total = sum(ttl_values) if ttl_values else None
    cache_creation = ttl_total if ttl_total is not None and generic_creation in {None, 0} else generic_creation
    return {
        "cache_read_input_tokens": cache_read,
        "cache_creation_input_tokens": cache_creation,
        "ephemeral_5m_input_tokens": creation_5m,
        "ephemeral_1h_input_tokens": creation_1h,
    }


def normalize_usage(
    usage: Mapping[str, Any] | None,
    *,
    source: str | None = None,
    status: str = "completed",
    observed_sources: Sequence[UsageSource] | None = None,
    usage_conflict: bool = False,
) -> dict[str, Any]:
    """Normalize token usage without inventing values missing from the source."""

    output_details = usage.get("output_token_details") if isinstance(usage, Mapping) else None
    output_details = output_details if isinstance(output_details, Mapping) else {}
    completion_details = usage.get("completion_tokens_details") if isinstance(usage, Mapping) else None
    completion_details = completion_details if isinstance(completion_details, Mapping) else {}
    normalized = {
        "input_tokens": usage_number(usage, "input_tokens", "prompt_tokens"),
        "output_tokens": usage_number(usage, "output_tokens", "completion_tokens"),
        "total_tokens": usage_number(usage, "total_tokens"),
        **input_cache_details(usage),
        "reasoning_tokens": _first_number(
            usage_number(output_details, "reasoning", "reasoning_tokens"),
            usage_number(completion_details, "reasoning", "reasoning_tokens"),
            usage_number(usage, "reasoning", "reasoning_tokens"),
        ),
        "source": source if source is not None else ("provider" if usage else "unavailable"),
        "status": status,
        "unavailable_reason": None if usage else "adapter_did_not_expose_provider_usage",
        "usage_conflict": usage_conflict,
        "observed_usage": _safe_json(dict(usage or {})),
        "usage_sources": [item["source"] for item in observed_sources or ()],
        "observed_usages": _safe_json(list(observed_sources or ())),
    }
    return normalized


def usage_signature(usage: Mapping[str, Any]) -> tuple[int | None, ...]:
    details = input_cache_details(usage)
    output_details = usage.get("output_token_details")
    output_details = output_details if isinstance(output_details, Mapping) else {}
    completion_details = usage.get("completion_tokens_details")
    completion_details = completion_details if isinstance(completion_details, Mapping) else {}
    return (
        usage_number(usage, "input_tokens", "prompt_tokens"),
        usage_number(usage, "output_tokens", "completion_tokens"),
        usage_number(usage, "total_tokens"),
        details["cache_read_input_tokens"],
        details["cache_creation_input_tokens"],
        details["ephemeral_5m_input_tokens"],
        details["ephemeral_1h_input_tokens"],
        _first_number(
            usage_number(output_details, "reasoning", "reasoning_tokens"),
            usage_number(completion_details, "reasoning", "reasoning_tokens"),
            usage_number(usage, "reasoning", "reasoning_tokens"),
        ),
    )


def select_usage_source(sources: Sequence[UsageSource]) -> tuple[UsageSource | None, bool]:
    """Select the terminal public usage source and flag real numeric conflicts."""

    selected = None
    for preferred in ("usage_metadata", "llm_output.token_usage", "response_metadata.token_usage"):
        selected = next((item for item in sources if item["source"] == preferred), None)
        if selected is not None:
            break
    signatures = [usage_signature(item["usage"]) for item in sources]
    conflict = len({item for item in signatures if any(value is not None for value in item)}) > 1
    return selected, conflict


def normalize_model_output_usage(value: Any, *, status: str = "completed") -> dict[str, Any]:
    """Collect, select, and normalize usage from a LangChain model output."""

    sources = collect_usage_sources(value)
    selected, conflict = select_usage_source(sources)
    return normalize_usage(
        selected["usage"] if selected is not None else None,
        source=selected["source"] if selected is not None else None,
        status=status if selected is not None else "unavailable",
        observed_sources=sources,
        usage_conflict=conflict,
    )


__all__ = [
    "UsageSource",
    "collect_usage_sources",
    "input_cache_details",
    "model_output_messages",
    "normalize_model_output_usage",
    "normalize_usage",
    "select_usage_source",
    "usage_number",
]
