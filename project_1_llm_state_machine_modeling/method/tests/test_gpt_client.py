from __future__ import annotations

import pytest

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
