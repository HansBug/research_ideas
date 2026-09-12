from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest

from utils.llm import LLMConfig, LLMRegistry
from utils.structured_runtime import (
    PROVIDER_CALL_DEADLINE_SECONDS,
    PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS,
    STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS,
    PublicStructuredRuntime,
    _structured_stage_deadline_seconds,
)


@pytest.mark.parametrize("adapter", ["openai", "openai-responses", "anthropic", "deepseek", "google-genai"])
def test_structured_runtime_constructs_provider_transport_without_network(tmp_path, monkeypatch, adapter):
    config = LLMConfig(adapter=adapter, model="test-model", api_key="test-key",
                       base_url="http://127.0.0.1:1", stream_usage=True)
    registry = LLMRegistry({"fixture": config}, "fixture")
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: registry)
    with patch("socket.socket.connect", side_effect=AssertionError("unexpected network access")):
        runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0)
        try:
            model = runtime._transport_model
            if adapter == "google-genai":
                timeout = model.timeout
                assert "stream_usage" not in model.model_kwargs
            else:
                assert model.stream_usage is True
                timeout = model.default_request_timeout if adapter == "anthropic" else model.request_timeout
            if adapter in {"anthropic", "google-genai"}:
                assert timeout == PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS
            else:
                assert isinstance(timeout, httpx.Timeout)
                with pytest.raises(TypeError):
                    hash(timeout)
        finally:
            runtime.close()
        assert not runtime._event_loop_thread.is_alive()


def test_stream_wait_and_enclosing_deadlines_allow_long_structured_requests(tmp_path, monkeypatch):
    from pydantic import BaseModel

    class Answer(BaseModel):
        answer: str

    config = LLMConfig(adapter="google-genai", model="test-model", api_key="test-key")
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config}, "fixture"))
    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=True)
    try:
        app = runtime._app("fixture", Answer, "Answer.", streaming=True)
        assert runtime._transport_model.timeout == 300
        assert PROVIDER_FIRST_BYTE_TIMEOUT_SECONDS < PROVIDER_CALL_DEADLINE_SECONDS == 600
        assert app.spec.limits["model_call_seconds"] == 600
        assert app.spec.limits["model_calls"] == 6
        assert app.spec.limits["seconds"] == _structured_stage_deadline_seconds(0) == 3630
        assert _structured_stage_deadline_seconds(0) + STRUCTURED_WRAPPER_FINALIZATION_GRACE_SECONDS == 3660
    finally:
        runtime.close()
