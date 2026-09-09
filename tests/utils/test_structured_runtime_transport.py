from __future__ import annotations

from unittest.mock import patch

from utils.llm import LLMConfig, LLMRegistry
from utils.structured_runtime import PublicStructuredRuntime


def test_anthropic_transport_constructs_with_numeric_timeout(tmp_path, monkeypatch):
    config = LLMConfig(
        adapter="anthropic",
        model="test-model",
        api_key="test-key",
        base_url="http://127.0.0.1:1",
    )
    monkeypatch.setattr(
        "utils.structured_runtime.load_llm_registry",
        lambda: LLMRegistry({"fixture": config}, "fixture"),
    )
    with patch("socket.socket.connect", side_effect=AssertionError("unexpected network access")):
        runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0)
        try:
            assert runtime._transport_model.default_request_timeout == 30
        finally:
            runtime.close()
