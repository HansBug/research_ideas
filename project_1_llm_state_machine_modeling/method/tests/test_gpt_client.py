from __future__ import annotations

import pytest

from method import gpt_client
from method.gpt_client import DEFAULT_REQUEST_TIMEOUT_SECONDS, get_request_timeout_seconds


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
