from __future__ import annotations

import json

import httpx
import pytest
from pydantic import BaseModel

from utils.llm import LLMConfig, LLMRegistry, create_chat_model
from utils.structured_runtime import PublicStructuredRuntime


class BudgetAnswer(BaseModel):
    answer: str


ADAPTERS = ["openai", "openai-responses", "anthropic", "deepseek", "google-genai"]


def _response(adapter):
    arguments = {"answer": "ok"}
    if adapter == "google-genai":
        return {
            "candidates": [{"content": {"role": "model", "parts": [{"functionCall": {
                "name": "BudgetAnswer", "args": arguments,
            }}]}, "finishReason": "STOP"}],
            "usageMetadata": {"promptTokenCount": 7, "candidatesTokenCount": 3,
                              "thoughtsTokenCount": 2, "totalTokenCount": 12},
            "modelVersion": "test-model",
        }
    if adapter == "anthropic":
        return {
            "id": "msg_fixture", "type": "message", "role": "assistant", "model": "test-model",
            "content": [{"type": "tool_use", "id": "call_fixture", "name": "BudgetAnswer", "input": arguments}],
            "stop_reason": "tool_use", "stop_sequence": None,
            "usage": {"input_tokens": 7, "output_tokens": 5},
        }
    if adapter == "openai-responses":
        return {
            "id": "resp_fixture", "object": "response", "created_at": 1,
            "model": "test-model", "status": "completed", "error": None,
            "incomplete_details": None,
            "output": [{"type": "function_call", "id": "fc_fixture", "call_id": "call_fixture",
                        "name": "BudgetAnswer", "arguments": json.dumps(arguments), "status": "completed"}],
            "usage": {"input_tokens": 7, "output_tokens": 5, "total_tokens": 12,
                      "input_tokens_details": {"cached_tokens": 0}, "output_tokens_details": {"reasoning_tokens": 2}},
        }
    return {
        "id": "chatcmpl_fixture", "object": "chat.completion", "created": 1, "model": "test-model",
        "choices": [{"index": 0, "finish_reason": "tool_calls", "message": {
            "role": "assistant", "content": None, "tool_calls": [{"id": "call_fixture", "type": "function",
                "function": {"name": "BudgetAnswer", "arguments": json.dumps(arguments)}}],
        }}],
        "usage": {"prompt_tokens": 7, "completion_tokens": 5, "total_tokens": 12,
                  "completion_tokens_details": {"reasoning_tokens": 2}},
    }


def _mock_wire(monkeypatch, adapter, requests, *, reject=False, incomplete=False):
    def respond(request):
        requests.append(json.loads(request.content))
        if reject:
            return httpx.Response(400, json={"error": {"message": "offline stop", "type": "invalid_request_error"}})
        payload = _response(adapter)
        if incomplete:
            payload.update(status="incomplete", incomplete_details={"reason": "max_output_tokens"})
        return httpx.Response(200, json=payload)

    transport = httpx.MockTransport(respond)
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)


def _wire_cap(adapter, request):
    if adapter == "google-genai":
        return request["generationConfig"]["maxOutputTokens"]
    key = "max_output_tokens" if adapter == "openai-responses" else (
        "max_completion_tokens" if adapter == "openai" else "max_tokens"
    )
    return request[key]


@pytest.mark.parametrize("adapter", ADAPTERS)
@pytest.mark.parametrize("profile_cap", [4096, 32768])
@pytest.mark.parametrize("override", [None, 10000, 65536])
def test_structured_output_budget_matches_serialized_request_and_audit(tmp_path, monkeypatch, adapter, profile_cap, override):
    expected_cap = profile_cap if override is None else override
    requests = []
    _mock_wire(monkeypatch, adapter, requests)
    config = LLMConfig(adapter=adapter, model="test-model", api_key="offline-key",
                       base_url="https://example.invalid", max_output_tokens=profile_cap)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config}, "fixture"))
    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=False)
    try:
        result = runtime.call(kind="budget", schema=BudgetAnswer, system_prompt="Answer using the tool.",
                              prompt="Return ok.", artifact_id="wire", retry_cell_on_provider_error=False,
                              max_output_tokens=override)
    finally:
        runtime.close()
    assert result.succeeded, result.reason
    assert len(requests) == 1
    assert _wire_cap(adapter, requests[0]) == expected_cap
    rows = [json.loads(line) for line in (tmp_path / "wire/cell-attempt-1/audit.jsonl").read_text().splitlines()]
    budget = rows[0]["inference"]["output_budget"]
    assert budget == {"profile_max_output_tokens": profile_cap, "call_max_output_tokens": override,
                      "request_max_output_tokens": expected_cap,
                      "source": "profile" if override is None else "run_override"}
    assert rows[0]["capacity"]["max_output_tokens"] == _wire_cap(adapter, requests[0])
    usage = next(row["usage"] for row in rows if row["record"] == "decision")
    assert usage["output_budget"] == budget
    assert usage["output_tokens"] == 5
    assert usage["total_tokens"] == 12
    if adapter != "anthropic":
        assert usage["output_token_details"]["reasoning"] == 2
    expected = ({"status": "completed"} if adapter == "openai-responses" else
                {"stop_reason": "tool_use"} if adapter == "anthropic" else
                {"finish_reason": "STOP"} if adapter == "google-genai" else {"finish_reason": "tool_calls"})
    assert usage["provider_response"] == expected
    projection = next(row["rendered_input_projection"] for row in rows if row["record"] == "decision")
    assert "[redacted]" not in json.dumps(projection["model_settings"])


@pytest.mark.parametrize("adapter", ADAPTERS)
@pytest.mark.parametrize("streaming", [False, True])
def test_factory_cap_override_reaches_wire(tmp_path, monkeypatch, adapter, streaming):
    profile_cap = 10000
    requests = []
    _mock_wire(monkeypatch, adapter, requests, reject=True)
    model = create_chat_model(
        LLMConfig(adapter=adapter, model="test-model", api_key="offline-key",
                  base_url="https://example.invalid", max_output_tokens=32768),
        streaming=streaming, model_options={"max_tokens": 10000},
    )
    try:
        with pytest.raises(Exception):
            model.invoke("Offline cap probe.")
        assert len(requests) == 1
        assert _wire_cap(adapter, requests[0]) == profile_cap
    finally:
        if adapter == "google-genai":
            model.client.close()


def test_responses_incomplete_reason_survives_valid_structured_output(tmp_path, monkeypatch):
    requests = []
    _mock_wire(monkeypatch, "openai-responses", requests, incomplete=True)
    config = LLMConfig(adapter="openai-responses", model="test-model", api_key="offline-key",
                       base_url="https://example.invalid", max_output_tokens=32768)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config}, "fixture"))
    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=False)
    try:
        result = runtime.call(kind="budget", schema=BudgetAnswer, system_prompt="Answer using the tool.",
                              prompt="Return ok.", artifact_id="incomplete", retry_cell_on_provider_error=False)
    finally:
        runtime.close()
    assert result.succeeded
    assert result.usage[0]["provider_response"] == {
        "status": "incomplete", "incomplete_details": {"reason": "max_output_tokens"},
    }


@pytest.mark.parametrize("adapter", ADAPTERS)
def test_streaming_runtime_budget_is_on_wire_even_on_provider_failure(tmp_path, monkeypatch, adapter):
    profile_cap = 32768
    requests = []
    _mock_wire(monkeypatch, adapter, requests, reject=True)
    config = LLMConfig(adapter=adapter, model="test-model", api_key="offline-key",
                       base_url="https://example.invalid", max_output_tokens=32768)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config}, "fixture"))
    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=True)
    try:
        result = runtime.call(kind="budget", schema=BudgetAnswer, system_prompt="Answer using the tool.",
                              prompt="Return ok.", artifact_id="failure", retry_cell_on_provider_error=False)
    finally:
        runtime.close()
    assert not result.succeeded
    assert len(requests) == 1
    assert _wire_cap(adapter, requests[0]) == profile_cap
    assert result.usage[0]["output_budget"]["request_max_output_tokens"] == profile_cap
    assert result.usage[0]["output_tokens"] is None
    assert result.usage[0]["provider_response"] == {}
