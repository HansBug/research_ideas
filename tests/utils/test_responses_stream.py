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
    ([{"type": "response.failed", "sequence_number": 0, "response": response("failed",
       error={"code": "upstream_error", "message": "Upstream service temporarily unavailable"})}], "response.failed", True),
    ([{"type": "response.failed", "sequence_number": 0, "response": response("failed",
       error={"code": "upstream_error", "message": "upstream rejected request"})}], "response.failed", False),
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
        assert error.details["raw_error"] == events[0]["response"]["error"]


@pytest.mark.parametrize("error", [
    {"code": "server_error", "message": "temporary"},
    {"code": "upstream_error", "message": "Upstream service temporarily unavailable"},
])
def test_raw_failed_event_retries_exact_request_and_preserves_receipts(tmp_path, error):
    calls = []
    def handle(request):
        calls.append(json.loads(request.content))
        events = GOOD if len(calls) > 1 else [{"type": "response.failed", "sequence_number": 0,
            "response": response("failed", error=error)}]
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
    assert retries[0]["error"]["raw_error"] == error
    assert retries[0]["error"]["request_id"] == "req-1"
    assert result.usage[0]["total_tokens"] == 4


def test_from_config_installs_guard_only_for_responses():
    app = AgentApp.from_config(
        AgentSpec(name="guard-construction", system_prompt="Answer."),
        LLMConfig(model="gpt-5.6-luna", adapter="openai-responses", api_key="test-key"),
    )
    assert hasattr(app.model.root_async_client.responses._post, "__wrapped__")


def production_model(entry):
    from utils.llm import create_chat_model

    config = LLMConfig(adapter="openai-responses", model="gpt-5.6-luna", api_key="offline-key",
                       base_url="https://provider.invalid/v1", max_output_tokens=128000)
    options = {"streaming": True, "max_retries": 0}
    if entry == "factory":
        model = create_chat_model(config, model_options=options)
    else:
        model = AgentApp.from_config(AgentSpec(name="stream", system_prompt="Answer."),
                                     config, model_options=options).model
    model.include_response_headers = True
    # Each parametrized case owns its clients; LangChain caches default clients.
    model.root_client._client = httpx.Client()
    model.root_async_client._client = httpx.AsyncClient()
    return model


@pytest.mark.parametrize("entry", ["factory", "agent"])
@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize("events,reason,retryable", [
    ([], "empty_stream", True),
    (GOOD[:2], "eof_before_response_completed", True),
    ([{"type": "response.failed", "response": response("failed", error={
        "code": "server_error", "message": "overloaded"})}], "response.failed", True),
    ([{"type": "error", "code": "invalid_api_key", "message": "service unavailable"}], "error", False),
    ([{"type": "response.incomplete", "response": response("incomplete",
        incomplete_details={"reason": "max_output_tokens"})}], "response.incomplete", False),
])
def test_both_construction_paths_preserve_provider_failure(monkeypatch, entry, asynchronous, events, reason, retryable):
    from utils.llm.model_factory import guard_responses_stream_errors
    from utils.llm.responses_stream import ResponsesStreamError

    requests, responses = [], []

    def handle(request):
        requests.append(json.loads(request.content))
        result = httpx.Response(200, content=sse(events), headers={
            "content-type": "text/event-stream", "x-request-id": "req-test"})
        responses.append(result)
        return result

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    model = production_model(entry)
    posts = [client.responses._post for client in (model.root_client, model.root_async_client)]
    guard_responses_stream_errors(model)
    guard_responses_streams(model)
    assert posts == [client.responses._post for client in (model.root_client, model.root_async_client)]
    try:
        with pytest.raises(ResponsesStreamError) as caught:
            invoke(model, asynchronous)
        error = caught.value
        details = _exception_details(error)
        assert details["reason"] == reason and details["status_code"] == 200
        assert details["request_id"] == "req-test" and details["source"] == "provider"
        assert error.body["type"] == reason and error.body["status_code"] == 200
        assert _retryable_transport_error(error) is retryable
        assert _provider_retry_allowed({"details": details}) is retryable
        if reason in {"response.failed", "response.incomplete"}:
            assert details["model"] == "gpt-5.6-luna" and details["response_id"] == "resp-test"
            assert details["usage"]["total_tokens"] == 4
            assert details["failure_event"] == events[0]
        assert len(requests) == 1 and requests[0]["max_output_tokens"] == 128000
        assert requests[0]["stream"] is True and all(r.is_closed for r in responses)
    finally:
        model.root_client.close()
        asyncio.run(model.root_async_client.close())


@pytest.mark.parametrize("entry", ["factory", "agent"])
@pytest.mark.parametrize("asynchronous", [False, True])
def test_production_guard_preserves_completed_stream(monkeypatch, entry, asynchronous):
    transport = httpx.MockTransport(lambda request: httpx.Response(
        200, content=sse(GOOD), headers={"content-type": "text/event-stream", "x-request-id": "req-test"}))
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    model = production_model(entry)
    try:
        old = invoke(model_for(GOOD, guarded=False, headers=True), asynchronous)
        new = invoke(model, asynchronous)
        assert old.model_dump() == new.model_dump()
    finally:
        model.root_client.close()
        asyncio.run(model.root_async_client.close())


@pytest.mark.parametrize("asynchronous", [False, True])
def test_interrupted_stream_preserves_usage_and_closes_response(monkeypatch, asynchronous):
    from utils.llm.responses_stream import ResponsesStreamError

    class Interrupted(httpx.SyncByteStream, httpx.AsyncByteStream):
        def __iter__(self):
            yield sse(GOOD[:1])
            raise httpx.ReadError("connection interrupted")

        async def __aiter__(self):
            yield sse(GOOD[:1])
            raise httpx.ReadError("connection interrupted")

    responses = []

    def handle(request):
        result = httpx.Response(200, stream=Interrupted(), headers={"content-type": "text/event-stream"})
        responses.append(result)
        return result

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    model = production_model("factory")
    try:
        with pytest.raises(ResponsesStreamError) as caught:
            invoke(model, asynchronous)
        details = _exception_details(caught.value)
        assert details["reason"] == "transport_interrupted" and details["retryable"] is True
        assert details["raw_error"]["type"] == "ReadError" and details["usage"]["total_tokens"] == 4
        assert all(r.is_closed for r in responses)
    finally:
        model.root_client.close()
        asyncio.run(model.root_async_client.close())


@pytest.mark.parametrize("provider_code,expected_attempts", [("invalid_api_key", 1), ("server_error", 2)])
def test_current_structured_runtime_respects_retryability_and_failed_usage(tmp_path, monkeypatch, provider_code, expected_attempts):
    from pydantic import BaseModel
    from utils.llm import LLMRegistry
    from utils.structured_runtime import PublicStructuredRuntime

    requests = []
    failed = {"type": "response.failed", "response": response("failed", error={
        "code": provider_code, "message": "service unavailable"})}

    def handle(request):
        requests.append(json.loads(request.content))
        return httpx.Response(200, content=sse([failed]), headers={"content-type": "text/event-stream"})

    transport = httpx.MockTransport(handle)
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    config = LLMConfig(adapter="openai-responses", model="gpt-5.6-luna", api_key="offline-key", max_output_tokens=128000)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config}, "fixture"))

    class Answer(BaseModel):
        answer: str

    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=True)
    try:
        result = runtime.call(kind="probe", schema=Answer, system_prompt="Use the tool.",
                              prompt="same request", artifact_id="failed")
    finally:
        runtime.close()
    assert not result.succeeded and len(result.attempts) == len(requests) == expected_attempts
    assert all(request == requests[0] for request in requests)
    assert not result.schema_validation_failures
    assert all(attempt["provider_error"] for attempt in result.attempts)
    assert len(result.usage) == expected_attempts
    assert all(row["status"] == "failed" and row["total_tokens"] == 4 for row in result.usage)
    assert result.attempts[-1]["error"]["details"]["failure_event"] == failed


def test_explicit_nonretryable_wins_over_status_message_and_cause():
    error = AgentError("provider_error", "service unavailable", details={
        "source": "provider", "retryable": False, "status_code": 520})
    error.__cause__ = httpx.ReadTimeout("read timed out")
    assert _retryable_transport_error(error) is False
