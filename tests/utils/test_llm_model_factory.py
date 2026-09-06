from __future__ import annotations

import json
import sys
from pathlib import Path

import httpx
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
        ("google-genai", "ChatGoogleGenerativeAI", "langchain-google-genai/generate-content"),
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


@pytest.mark.parametrize(
    ("adapter", "effort", "expected"),
    [
        ("openai", "low", {"reasoning_effort": "low"}),
        ("openai-responses", "xhigh", {"reasoning": {"effort": "xhigh"}}),
        ("anthropic", "medium", {"effort": "medium"}),
        ("google-genai", "low", {"thinking_level": "low"}),
    ],
)
def test_explicit_effort_uses_adapter_specific_constructor_shape(
    adapter: str, effort: str, expected: dict[str, object]
) -> None:
    config = LLMConfig(adapter=adapter, model="test-model", api_key="test-key")

    kwargs = model_kwargs(config, effort=effort)

    for key, value in expected.items():
        assert kwargs[key] == value


@pytest.mark.parametrize("adapter", ["openai", "openai-responses", "anthropic", "deepseek"])
def test_omitted_effort_does_not_add_provider_effort_fields(adapter: str) -> None:
    kwargs = model_kwargs(
        LLMConfig(adapter=adapter, model="test-model", api_key="test-key")
    )

    assert "reasoning_effort" not in kwargs
    assert "reasoning" not in kwargs
    assert "effort" not in kwargs
    assert "thinking" not in kwargs


def test_responses_effort_merges_with_other_reasoning_options() -> None:
    config = LLMConfig(
        adapter="openai-responses", model="gpt-test", api_key="test-key"
    )

    kwargs = model_kwargs(
        config,
        model_options={"reasoning": {"summary": "auto"}},
        effort="high",
    )

    assert kwargs["reasoning"] == {"summary": "auto", "effort": "high"}


@pytest.mark.parametrize(
    ("adapter", "effort", "message"),
    [
        ("anthropic", "none", "unsupported effort"),
        ("deepseek", "low", "does not support explicit effort"),
        ("openai-responses", "minimal", "unsupported effort"),
        ("google-genai", "none", "unsupported effort"),
    ],
)
def test_unsupported_effort_is_rejected(
    adapter: str, effort: str, message: str
) -> None:
    config = LLMConfig(adapter=adapter, model="test-model", api_key="test-key")

    with pytest.raises(LLMModelFactoryError, match=message):
        model_kwargs(config, effort=effort)


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


def test_google_native_schema_reaches_the_wire_and_uses_explicit_credentials(monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_API_KEY", "environment-key-must-not-be-used")
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)
    requests = []

    def respond(request):
        requests.append(request)
        assert request.headers["x-goog-api-key"] == "profile-key"
        assert request.url.path == "/v1beta/models/gemini-test:generateContent"
        generation = json.loads(request.content)["generationConfig"]
        assert generation["maxOutputTokens"] == 123
        assert generation["responseMimeType"] == "application/json"
        assert generation["responseJsonSchema"]["properties"]["answer"]["type"] == "string"
        return httpx.Response(200, json={
            "candidates": [{"content": {"role": "model", "parts": [{"text": '{"answer":"ok"}'}]},
                            "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 9, "candidatesTokenCount": 3, "totalTokenCount": 12},
            "modelVersion": "gemini-test",
        })

    model = create_chat_model(
        LLMConfig(adapter="google-genai", model="gemini-test", api_key="profile-key",
                  base_url="https://example.invalid", max_output_tokens=123),
        streaming=False, model_options={"client_args": {"transport": httpx.MockTransport(respond)}},
    )
    try:
        result = model.with_structured_output(StructuredAnswer, method="json_schema", include_raw=True).invoke("answer")
        assert result["parsed"] == StructuredAnswer(answer="ok")
        assert result["raw"].usage_metadata["total_tokens"] == 12
        assert len(requests) == 1
    finally:
        model.client.close()


def test_google_adapter_rejects_ambient_backend_override(monkeypatch) -> None:
    monkeypatch.setenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
    with pytest.raises(LLMModelFactoryError, match="GOOGLE_GENAI_USE_VERTEXAI"):
        create_chat_model(LLMConfig(adapter="google-genai", model="gemini-test", api_key="test-key"))


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


def test_profile_stream_usage_is_shared_by_factory_and_agent() -> None:
    from utils.agent import AgentApp, AgentSpec

    config = LLMConfig(model="local-model", base_url="http://127.0.0.1:8100/v1",
                       api_key="test-key", stream_usage=True)
    assert create_chat_model(config).stream_usage is True
    app = AgentApp.from_config(AgentSpec(name="usage", system_prompt="answer"), config)
    assert app.model.stream_usage is True
    assert create_chat_model(config, stream_usage=False).stream_usage is False
    app = AgentApp.from_config(AgentSpec(name="usage", system_prompt="answer"), config,
                              model_options={"stream_usage": False})
    assert app.model.stream_usage is False
