import asyncio
import json

import httpx
import pytest
from openai import APIError
from pydantic import BaseModel

from utils.llm import LLMConfig, LLMRegistry, create_chat_model
from utils.structured_runtime import PublicStructuredRuntime


def failed_stream(monkeypatch):
    requests, responses = [], []
    events = [
        {"type": "response.created", "response": {"id": "resp_failed"}},
        {"type": "response.failed", "response": {"id": "resp_failed", "status": "failed",
         "error": {"code": "server_error", "message": "Our servers are currently overloaded. Please try again later."}}},
    ]
    payload = "".join("data: " + json.dumps(e) + "\n\n" for e in events).encode()

    def respond(request):
        requests.append(json.loads(request.content))
        response = httpx.Response(200, headers={"content-type": "text/event-stream"}, content=payload)
        responses.append(response)
        return response

    transport = httpx.MockTransport(respond)
    monkeypatch.setattr(httpx.Client, "_transport_for_url", lambda *args: transport)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    return requests, responses


def config():
    return LLMConfig(adapter="openai-responses", model="gpt-5.6-luna", api_key="offline-key",
                     base_url="https://example.invalid/v1", max_output_tokens=128000)


@pytest.mark.parametrize("asynchronous", [False, True])
def test_factory_raises_provider_error_for_http_200_failed_event(monkeypatch, asynchronous):
    requests, responses = failed_stream(monkeypatch)
    model = create_chat_model(config(), streaming=True, max_retries=0)

    async def consume():
        try:
            return [chunk async for chunk in model.astream("ok")]
        finally:
            await model.root_async_client.close()

    try:
        with pytest.raises(APIError) as error:
            if asynchronous:
                asyncio.run(consume())
            else:
                list(model.stream("ok"))
        assert error.value.code == "server_error"
        assert error.value.body["type"] == "response.failed"
        assert error.value.body["status_code"] == 200
        assert len(requests) == 1 and requests[0]["stream"] is True
        assert requests[0]["max_output_tokens"] == 128000
        assert all(response.is_closed for response in responses)
    finally:
        model.root_client.close()


def test_runtime_preserves_provider_failure_without_schema_retry(tmp_path, monkeypatch):
    requests, responses = failed_stream(monkeypatch)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"fixture": config()}, "fixture"))

    class Answer(BaseModel):
        answer: str

    runtime = PublicStructuredRuntime("fixture", tmp_path, transport_retries=0, streaming=True)
    try:
        result = runtime.call(kind="probe", schema=Answer, system_prompt="Use the tool.", prompt="ok",
                              artifact_id="failed", retry_cell_on_provider_error=False)
    finally:
        runtime.close()
    assert not result.succeeded
    assert len(requests) == 1
    assert result.attempts[0]["provider_error"] is True
    assert not result.schema_validation_failures
    assert result.usage[0]["status"] == "failed"
    assert all(response.is_closed for response in responses)
    assert not runtime._event_loop_thread.is_alive()
