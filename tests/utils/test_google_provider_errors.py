import json

import httpx
import pytest
from google.genai.errors import ClientError, ServerError
from langchain_google_genai.chat_models import GoogleAPIError
from pydantic import BaseModel

from utils.agent.runtime import _exception_details, _retryable_transport_error
from utils.llm import LLMConfig, LLMRegistry
from utils.structured_runtime import PublicStructuredRuntime


@pytest.mark.parametrize("cls,status,retryable", [(ClientError, 400, False), (ClientError, 401, False),
                                                (ClientError, 429, True), (ServerError, 503, True),
                                                (GoogleAPIError, 504, True)])
def test_google_http_status_keeps_provider_ownership(cls, status, retryable):
    error = cls(status, {"error": {"code": status, "message": "fixture provider error"}})
    details = _exception_details(error)
    assert details["source"] == "provider"
    assert details["status_code"] == status
    assert _retryable_transport_error(error) is retryable


def test_runtime_numeric_code_is_not_assumed_to_be_http_status():
    class LocalError(Exception):
        code = 504

    assert _exception_details(LocalError())["source"] == "runtime"
    assert not _retryable_transport_error(LocalError())


def test_native_google_504_records_provider_failure_without_extra_retry(tmp_path, monkeypatch):
    requests = []
    def respond(request):
        requests.append(json.loads(request.content))
        return httpx.Response(504, json={"error": {"code": 504, "status": "DEADLINE_EXCEEDED",
                                                   "message": "fixture gateway timeout"}})
    transport = httpx.MockTransport(respond)
    monkeypatch.setattr(httpx.AsyncClient, "_transport_for_url", lambda *args: transport)
    config = LLMConfig(adapter="google-genai", model="gemini-test", api_key="test-key",
                       base_url="https://example.invalid", max_output_tokens=4096)
    monkeypatch.setattr("utils.structured_runtime.load_llm_registry", lambda: LLMRegistry({"test": config}, "test"))
    class Answer(BaseModel):
        answer: str
    runtime = PublicStructuredRuntime("test", tmp_path, transport_retries=0, streaming=False)
    try:
        result = runtime.call(kind="fixture", schema=Answer, system_prompt="Answer.", prompt="Hello.",
                              artifact_id="failure", retry_cell_on_provider_error=False)
    finally:
        runtime.close()
    assert len(requests) == 1
    assert requests[0]["generationConfig"]["maxOutputTokens"] == 10000
    assert not result.succeeded
    assert result.result["error"]["code"] == "provider_error"
    assert result.result["error"]["details"]["status_code"] == 504
    assert result.schema_validation_failures == []
