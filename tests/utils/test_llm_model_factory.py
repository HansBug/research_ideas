from __future__ import annotations

import sys
from pathlib import Path
import pytest
from pydantic import BaseModel

from utils.llm.config import LLMConfig
from utils.llm.model_factory import (
    LLMModelFactoryError,
    adapter_name,
    create_chat_model,
    default_stream_usage,
    model_kwargs,
)


class StructuredAnswer(BaseModel):
    answer: str


@pytest.mark.parametrize(
    ("adapter", "expected_class", "expected_transport"),
    [
        ("openai", "ChatOpenAI", "langchain-openai/chat-completions"),
        ("openai-responses", "ChatOpenAI", "langchain-openai/responses"),
        ("anthropic", "ChatAnthropic", "langchain-anthropic/messages"),
        ("deepseek", "ChatDeepSeek", "langchain-deepseek/chat-completions"),
    ],
)
def test_create_chat_model_selects_adapter_and_supports_include_raw_structured_output(
    adapter: str, expected_class: str, expected_transport: str
) -> None:
    config = LLMConfig(adapter=adapter, model="test-model", api_key="test-key")

    model = create_chat_model(config)

    assert type(model).__name__ == expected_class
    assert adapter_name(adapter) == expected_transport
    structured = model.with_structured_output(StructuredAnswer, include_raw=True)
    assert structured is not None


def test_openai_responses_adapter_enables_responses_api() -> None:
    config = LLMConfig(adapter="openai-responses", model="gpt-test", api_key="test-key")

    kwargs = model_kwargs(config)
    model = create_chat_model(config)

    assert kwargs["use_responses_api"] is True
    assert getattr(model, "use_responses_api") is True


def test_max_output_tokens_use_provider_specific_constructor_names() -> None:
    openai = model_kwargs(LLMConfig(adapter="openai", model="gpt-test", max_output_tokens=123, api_key="x"))
    anthropic = model_kwargs(LLMConfig(adapter="anthropic", model="claude-test", max_output_tokens=456, api_key="x"))
    deepseek = model_kwargs(LLMConfig(adapter="deepseek", model="deepseek-test", max_output_tokens=789, api_key="x"))

    assert openai["max_completion_tokens"] == 123
    assert "max_tokens" not in openai
    assert anthropic["max_tokens"] == 456
    assert deepseek["max_tokens"] == 789


def test_factory_requires_explicit_api_key_by_default() -> None:
    with pytest.raises(LLMModelFactoryError, match="api_key"):
        create_chat_model(LLMConfig(adapter="openai", model="gpt-test"))


def test_model_options_override_defaults_without_reading_agent_runtime() -> None:
    for forbidden in ("utils.agent", "utils.agent.runtime", "paper_stm_repair_loop"):
        sys.modules.pop(forbidden, None)
    config = LLMConfig(adapter="deepseek", model="deepseek-test", api_key="x")

    kwargs = model_kwargs(config, model_options={"streaming": False, "timeout": 30})

    assert kwargs["streaming"] is False
    assert kwargs["timeout"] == 30
    assert "utils.agent" not in sys.modules
    assert "utils.agent.runtime" not in sys.modules
    assert "paper_stm_repair_loop" not in sys.modules
    assert "utils.agent" not in Path("utils/llm/model_factory.py").read_text(encoding="utf-8")


def test_default_stream_usage_is_adapter_specific() -> None:
    assert default_stream_usage(LLMConfig(adapter="anthropic", model="claude", api_key="x")) is True
    assert default_stream_usage(LLMConfig(adapter="deepseek", model="deepseek", api_key="x")) is False
    assert default_stream_usage(LLMConfig(adapter="openai", model="gpt", api_key="x")) is True
    assert (
        default_stream_usage(
            LLMConfig(adapter="openai", model="gpt", base_url="https://example.invalid/v1", api_key="x")
        )
        is False
    )
