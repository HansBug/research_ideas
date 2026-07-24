from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urlsplit

from .config import LLMConfig


_ADAPTER_PACKAGES = {
    "openai": "langchain-openai",
    "openai-responses": "langchain-openai",
    "anthropic": "langchain-anthropic",
    "deepseek": "langchain-deepseek",
}

_ADAPTER_NAMES = {
    "openai": "langchain-openai/chat-completions",
    "openai-responses": "langchain-openai/responses",
    "anthropic": "langchain-anthropic/messages",
    "deepseek": "langchain-deepseek/chat-completions",
}


class LLMModelFactoryError(ValueError):
    """Raised when a neutral LLM model cannot be constructed from config."""


def adapter_name(adapter: str) -> str:
    """Return the stable transport name for a supported adapter."""

    try:
        return _ADAPTER_NAMES[adapter]
    except KeyError as exc:
        raise LLMModelFactoryError(f"unsupported LLM adapter: {adapter}") from exc


def default_stream_usage(config: LLMConfig) -> bool:
    """Return a conservative stream-usage default for the configured adapter."""

    if config.adapter == "anthropic":
        return True
    if config.adapter == "deepseek":
        return False
    host = (urlsplit(config.base_url or "https://api.openai.com").hostname or "").lower()
    return host == "api.openai.com"


def model_kwargs(
    config: LLMConfig,
    *,
    streaming: bool = True,
    stream_usage: bool | None = None,
    max_retries: int | None = 0,
    model_options: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build provider constructor kwargs from ``LLMConfig`` without side imports."""

    kwargs = config.connection_kwargs()
    if config.max_output_tokens is not None:
        kwargs[
            "max_completion_tokens"
            if config.adapter in {"openai", "openai-responses"}
            else "max_tokens"
        ] = config.max_output_tokens
    if config.adapter in {"openai", "openai-responses"}:
        kwargs["use_responses_api"] = config.adapter == "openai-responses"
    kwargs["streaming"] = streaming
    kwargs["stream_usage"] = default_stream_usage(config) if stream_usage is None else stream_usage
    if max_retries is not None:
        kwargs["max_retries"] = max_retries
    kwargs.update(dict(model_options or {}))
    return kwargs


def create_chat_model(
    config: LLMConfig,
    *,
    model_options: Mapping[str, Any] | None = None,
    require_api_key: bool = True,
    streaming: bool = True,
    stream_usage: bool | None = None,
    max_retries: int | None = 0,
) -> Any:
    """Construct the LangChain chat model selected by ``LLMConfig.adapter``.

    The returned model is deliberately provider-neutral from this package's
    perspective: callers can use normal LangChain APIs, including direct
    ``with_structured_output(..., include_raw=True)`` where the adapter supports
    it.  This module does not import agent runtimes or project-specific repair
    loops.
    """

    if require_api_key and config.api_key is None:
        raise LLMModelFactoryError("api_key is required for real model construction")
    adapter = config.adapter
    try:
        if adapter == "deepseek":
            from langchain_deepseek import ChatDeepSeek as ChatModel
        elif adapter == "anthropic":
            from langchain_anthropic import ChatAnthropic as ChatModel
        elif adapter in {"openai", "openai-responses"}:
            from langchain_openai import ChatOpenAI as ChatModel
        else:  # pragma: no cover - LLMConfig validates this today.
            raise LLMModelFactoryError(f"unsupported LLM adapter: {adapter}")
    except ImportError as exc:  # pragma: no cover - environment dependent.
        package = _ADAPTER_PACKAGES.get(adapter, adapter)
        raise LLMModelFactoryError(f"{package} is required") from exc

    try:
        return ChatModel(
            **model_kwargs(
                config,
                streaming=streaming,
                stream_usage=stream_usage,
                max_retries=max_retries,
                model_options=model_options,
            )
        )
    except Exception as exc:
        raise LLMModelFactoryError("model construction failed") from exc
