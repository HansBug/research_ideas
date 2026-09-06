from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest

from utils.llm import LLMConfig, LLMRegistry
from utils.structured_runtime import PublicStructuredRuntime


@pytest.mark.parametrize("adapter", ["openai", "openai-responses", "anthropic", "deepseek"])
def test_structured_runtime_constructs_provider_transport_without_network(tmp_path, monkeypatch, adapter):
    config = LLMConfig(adapter=adapter, model="test-model", api_key="test-key",
                       base_url="http://127.0.0.1:1", stream_usage=True)
    registry = LLMRegistry({"fixture": config}, "fixture")
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: registry)
    with patch("socket.socket.connect", side_effect=AssertionError("unexpected network access")):
        runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0)
        try:
            model = runtime._transport_model
            assert model.stream_usage is True
            timeout = model.default_request_timeout if adapter == "anthropic" else model.request_timeout
            if adapter == "anthropic":
                assert timeout == 30.0
            else:
                assert isinstance(timeout, httpx.Timeout)
                with pytest.raises(TypeError):
                    hash(timeout)
        finally:
            runtime.close()
        assert not runtime._event_loop_thread.is_alive()
