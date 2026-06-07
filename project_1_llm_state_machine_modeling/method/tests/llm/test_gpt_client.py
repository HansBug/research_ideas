from __future__ import annotations

import time

import pytest

from method import gpt_client
from method.gpt_client import DEFAULT_REQUEST_TIMEOUT_SECONDS, LLMRequestTimeoutError, get_request_timeout_seconds


def test_gpt_client_default_request_timeout_is_fail_fast(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("LLM_REQUEST_TIMEOUT_SECONDS", raising=False)

    assert get_request_timeout_seconds() == DEFAULT_REQUEST_TIMEOUT_SECONDS


def test_gpt_client_request_timeout_can_be_overridden(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_REQUEST_TIMEOUT_SECONDS", "123.5")

    assert get_request_timeout_seconds() == 123.5


def test_gpt_client_request_timeout_can_be_disabled_for_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_REQUEST_TIMEOUT_SECONDS", "none")

    assert get_request_timeout_seconds() is None


def test_gpt_client_request_timeout_rejects_invalid_value(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LLM_REQUEST_TIMEOUT_SECONDS", "forever")

    with pytest.raises(ValueError, match="LLM_REQUEST_TIMEOUT_SECONDS"):
        get_request_timeout_seconds()


def test_gpt_client_disables_sdk_hidden_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeOpenAI:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    monkeypatch.setenv("LLM_ENDPOINT", "https://example.test")
    monkeypatch.setenv("LLM_API_KEY", "sk-test")
    monkeypatch.setenv("LLM_REQUEST_TIMEOUT_SECONDS", "123")
    monkeypatch.setattr(gpt_client, "OpenAI", FakeOpenAI)

    client = gpt_client.get_llm_client()

    assert isinstance(client, FakeOpenAI)
    assert captured["base_url"] == "https://example.test/v1"
    assert captured["timeout"] == 123.0
    assert captured["max_retries"] == 0


def test_gpt_client_keeps_sdk_hidden_retries_disabled_without_timeout(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeOpenAI:
        def __init__(self, **kwargs: object) -> None:
            captured.update(kwargs)

    monkeypatch.setenv("LLM_ENDPOINT", "https://example.test/v1")
    monkeypatch.setenv("LLM_API_KEY", "sk-test")
    monkeypatch.setenv("LLM_REQUEST_TIMEOUT_SECONDS", "none")
    monkeypatch.setattr(gpt_client, "OpenAI", FakeOpenAI)

    client = gpt_client.get_llm_client()

    assert isinstance(client, FakeOpenAI)
    assert captured["base_url"] == "https://example.test/v1"
    assert "timeout" not in captured
    assert captured["max_retries"] == 0


def test_gpt_client_repo_deadline_interrupts_hung_call() -> None:
    started = time.monotonic()

    with pytest.raises(LLMRequestTimeoutError, match="exceeded"):
        with gpt_client._request_deadline(0.05):  # noqa: SLF001 - verifies repo-level hard deadline.
            time.sleep(10)

    assert time.monotonic() - started < 1.0

from types import SimpleNamespace


def _chunk(text: str):
    return SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=text))])


def _usage_chunk(prompt_tokens: int, completion_tokens: int, total_tokens: int):
    return SimpleNamespace(choices=[], usage=SimpleNamespace(prompt_tokens=prompt_tokens, completion_tokens=completion_tokens, total_tokens=total_tokens))


def test_gpt_client_chat_streams_by_default_and_aggregates_chunks(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeCompletions:
        def create(self, **kwargs: object):
            captured.update(kwargs)
            assert kwargs["stream"] is True
            assert kwargs["stream_options"] == {"include_usage": True}
            return iter([_chunk("hello"), _chunk(" "), _chunk("world")])

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    monkeypatch.setenv("LLM_MODEL", "mock-stream-model")
    monkeypatch.setenv("LLM_PROGRESS_LOG", "false")
    monkeypatch.delenv("LLM_STREAM", raising=False)
    monkeypatch.setattr(gpt_client, "get_llm_client", lambda: fake_client)

    content, usage = gpt_client.chat(messages=[{"role": "user", "content": "Say hello"}])

    assert content == "hello world"
    assert captured["model"] == "mock-stream-model"
    assert "max_tokens" not in captured
    assert usage["stream"] is True
    assert usage["chunk_count"] == 3
    assert usage["completion_chars"] == len("hello world")
    assert usage["prompt_chars"] == len("Say hello")
    assert usage["token_usage_available"] is False
    assert usage["total_tokens"] is None
    assert usage["estimated_total_tokens"] > 0


def test_gpt_client_chat_stream_records_usage_when_provider_emits_final_usage(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeCompletions:
        def create(self, **kwargs: object):
            assert kwargs["stream"] is True
            assert kwargs["stream_options"] == {"include_usage": True}
            return iter([_chunk("hello"), _usage_chunk(11, 3, 14)])

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    monkeypatch.setenv("LLM_MODEL", "mock-stream-model")
    monkeypatch.setenv("LLM_PROGRESS_LOG", "false")
    monkeypatch.setattr(gpt_client, "get_llm_client", lambda: fake_client)

    content, usage = gpt_client.chat(messages=[{"role": "user", "content": "Say hello"}])

    assert content == "hello"
    assert usage["token_usage_available"] is True
    assert usage["prompt_tokens"] == 11
    assert usage["completion_tokens"] == 3
    assert usage["total_tokens"] == 14


def test_gpt_client_chat_stream_treats_zero_usage_as_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeCompletions:
        def create(self, **kwargs: object):
            assert kwargs["stream"] is True
            return iter([_chunk("hello"), _usage_chunk(0, 0, 0)])

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    monkeypatch.setenv("LLM_MODEL", "mock-stream-model")
    monkeypatch.setenv("LLM_PROGRESS_LOG", "false")
    monkeypatch.setattr(gpt_client, "get_llm_client", lambda: fake_client)

    content, usage = gpt_client.chat(messages=[{"role": "user", "content": "Say hello"}])

    assert content == "hello"
    assert usage["token_usage_available"] is False
    assert usage["stream_usage_zero_reported"] is True
    assert usage["total_tokens"] is None
    assert usage["estimated_total_tokens"] > 0


def test_gpt_client_chat_can_disable_stream_for_control_diagnostics(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, object] = {}

    class FakeCompletions:
        def create(self, **kwargs: object):
            captured.update(kwargs)
            assert "stream" not in kwargs
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="non-stream ok"))],
                usage=SimpleNamespace(prompt_tokens=2, completion_tokens=3, total_tokens=5),
            )

    fake_client = SimpleNamespace(chat=SimpleNamespace(completions=FakeCompletions()))
    monkeypatch.setenv("LLM_MODEL", "mock-non-stream-model")
    monkeypatch.setenv("LLM_STREAM", "false")
    monkeypatch.setenv("LLM_PROGRESS_LOG", "false")
    monkeypatch.setattr(gpt_client, "get_llm_client", lambda: fake_client)

    content, usage = gpt_client.chat(messages=[{"role": "user", "content": "Say hello"}], max_tokens=123)

    assert content == "non-stream ok"
    assert captured["model"] == "mock-non-stream-model"
    assert captured["max_tokens"] == 123
    assert usage["stream"] is False
    assert usage["token_usage_available"] is True
    assert usage["total_tokens"] == 5
    assert usage["completion_chars"] == len("non-stream ok")
