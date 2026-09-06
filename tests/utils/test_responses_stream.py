"""Offline HTTP/SSE integration with the installed SDK and LangChain adapter."""

import asyncio
import json

import httpx
import pytest
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from utils.agent import AgentApp, AgentError, AgentSpec
from utils.agent.responses_stream import guard_responses_streams
from utils.agent.runtime import _exception_details, _retryable_transport_error
from utils.llm import LLMConfig
from utils.structured_runtime import _is_provider_error, _provider_retry_allowed


def response(status="completed", **extra):
    return {"id": "resp-test", "created_at": 1, "object": "response",
            "model": "gpt-5.6-luna", "status": status, "error": None,
            "output": [], "parallel_tool_calls": True, "tools": [],
            "tool_choice": "auto", "usage": {"input_tokens": 3, "output_tokens": 1,
            "total_tokens": 4, "input_tokens_details": {"cached_tokens": 0},
            "output_tokens_details": {"reasoning_tokens": 0}}, **extra}


GOOD = [
    {"type": "response.created", "sequence_number": 0, "response": response("in_progress")},
    {"type": "response.output_text.delta", "sequence_number": 1, "item_id": "msg-test",
     "output_index": 0, "content_index": 0, "delta": "OK", "logprobs": []},
    {"type": "response.completed", "sequence_number": 2, "response": response()},
]


def sse(events):
    return "".join("event: " + e["type"] + "\ndata: " + json.dumps(e) + "\n\n" for e in events).encode()


def model_for(events, *, guarded=True, headers=False):
    def handle(request):
        return httpx.Response(200, content=sse(events), headers={
            "content-type": "text/event-stream", "x-request-id": "req-test"})
    transport = httpx.MockTransport(handle)
    model = ChatOpenAI(model="gpt-5.6-luna", api_key="test-key", use_responses_api=True,
                       streaming=True, max_retries=0, include_response_headers=headers,
                       http_client=httpx.Client(transport=transport),
                       http_async_client=httpx.AsyncClient(transport=transport))
    if guarded:
        guard_responses_streams(model)
    return model


def invoke(model, asynchronous):
    if asynchronous:
        return asyncio.run(model.ainvoke([HumanMessage(content="same request")]))
    return model.invoke([HumanMessage(content="same request")])


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("headers", [False, True])
def test_normal_stream_unchanged(asynchronous, headers):
    old = invoke(model_for(GOOD, guarded=False, headers=headers), asynchronous)
    new = invoke(model_for(GOOD, headers=headers), asynchronous)
    assert old.content == new.content
    assert old.tool_calls == new.tool_calls
    assert old.usage_metadata == new.usage_metadata
    assert old.response_metadata == new.response_metadata


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("events,reason,retryable", [
    ([], "empty_stream", True),
    (GOOD[:2], "eof_before_response_completed", True),
    ([{"type": "response.failed", "sequence_number": 0, "response": response("failed",
       error={"code": "server_error", "message": "origin failure"})}], "response.failed", True),
    ([{"type": "error", "code": "rate_limit_exceeded", "message": "busy", "sequence_number": 0}], "error", True),
    ([{"type": "error", "code": "invalid_api_key", "message": "unauthorized", "sequence_number": 0}], "error", False),
    ([{"type": "error", "code": "invalid_request_error", "message": "bad schema", "sequence_number": 0}], "error", False),
    ([{"type": "response.incomplete", "sequence_number": 0, "response": response("incomplete",
       incomplete_details={"reason": "max_output_tokens"})}], "response.incomplete", False),
])
def test_stream_failure_has_structured_reason(events, reason, retryable, asynchronous):
    with pytest.raises(AgentError) as caught:
        invoke(model_for(events), asynchronous)
    error = caught.value
    assert error.details["reason"] == reason
    assert error.details["request_id"] == "req-test"
    assert _retryable_transport_error(error) is retryable
    assert _is_provider_error({"code": error.code, "details": _exception_details(error)})
    assert _provider_retry_allowed({"code": error.code, "details": _exception_details(error)}) is retryable
    if reason == "response.failed":
        assert error.details["response_id"] == "resp-test"
        assert error.details["usage"]["total_tokens"] == 4
        assert error.details["raw_error"]["code"] == "server_error"


def test_raw_failed_event_retries_exact_request_and_preserves_receipts(tmp_path):
    calls = []
    def handle(request):
        calls.append(json.loads(request.content))
        events = GOOD if len(calls) > 1 else [{"type": "response.failed", "sequence_number": 0,
            "response": response("failed", error={"code": "server_error", "message": "temporary"})}]
        return httpx.Response(200, content=sse(events), headers={
            "content-type": "text/event-stream", "x-request-id": f"req-{len(calls)}"})
    model = model_for([])
    model.root_async_client._client = httpx.AsyncClient(transport=httpx.MockTransport(handle))
    audit = tmp_path / "audit.jsonl"
    result = AgentApp._for_test(
        AgentSpec(name="stream-retry", system_prompt="Answer.", transport_retry_delays_seconds=(0,)),
        LLMConfig(model="gpt-5.6-luna", adapter="openai-responses"), model,
    ).run("same request", renderer="quiet", audit_out=audit)
    assert result.status == "success", result.error
    assert len(calls) == 2 and calls[0] == calls[1]
    retries = [r for r in map(json.loads, audit.read_text().splitlines()) if r.get("record") == "transport_retry"]
    assert [r["operation"] for r in retries] == ["scheduled", "recovered"]
    assert retries[0]["request_fingerprint"] == retries[1]["request_fingerprint"]
    assert retries[0]["error"]["raw_error"]["code"] == "server_error"
    assert retries[0]["error"]["request_id"] == "req-1"
    assert result.usage[0]["total_tokens"] == 4


def test_from_config_installs_guard_only_for_responses():
    app = AgentApp.from_config(
        AgentSpec(name="guard-construction", system_prompt="Answer."),
        LLMConfig(model="gpt-5.6-luna", adapter="openai-responses", api_key="test-key"),
    )
    assert hasattr(app.model.root_async_client.responses._post, "__wrapped__")
