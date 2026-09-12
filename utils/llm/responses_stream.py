"""Validate Responses SSE termination before LangChain can discard failure events.

The SDK owns SSE decoding. Only its per-resource stream class is substituted;
request parameters, parsing of successful events, and dependency files stay intact.
"""

from functools import wraps
import json

import httpx
from openai import APIError, AsyncStream, Stream
from openai.types.responses import ResponseStreamEvent


class ResponsesStreamError(APIError):
    """Provider failure with the original SSE, usage and replay decision."""

    def __init__(self, reason, *, response, details):
        error = details.get("raw_error")
        body = dict(error) if isinstance(error, dict) else {}
        body.update(type=reason, status_code=response.status_code)
        message = body.get("message") or "Responses stream failed: " + reason
        super().__init__(message, request=response.request, body=body)
        self.response = response
        self.status_code = response.status_code
        self.request_id = details.get("request_id")
        self.details = details


class _StreamState:
    def __init__(self, response, error_factory):
        self.response = response
        self.error_factory = error_factory
        self.request_id = response.headers.get("x-request-id")
        self.response_id = None
        self.model = None
        self.usage = None
        self.events = []
        self.complete = False

    def fail(self, reason, *, event=None, error=None, retryable=True):
        raise self.error_factory(
            reason,
            response=self.response,
            details={
                "source": "provider", "type": "ResponsesStreamError",
                "reason": reason, "retryable": retryable,
                "status_code": self.response.status_code, "model": self.model,
                "request_id": self.request_id, "response_id": self.response_id,
                "usage": self.usage, "recent_event_types": self.events[-12:],
                "raw_error": error, "failure_event": event,
            },
        )

    def observe(self, sse):
        if sse.data == "[DONE]":
            self.finish()
            return
        try:
            payload = sse.json()
        except json.JSONDecodeError as exc:
            self.fail("invalid_event_json", error=str(exc), retryable=False)
        if not isinstance(payload, dict):
            self.fail("non_object_event", error=payload, retryable=False)
        kind = payload.get("type") or sse.event
        self.events.append(kind)
        self.events = self.events[-12:]
        response = payload.get("response") or {}
        if not isinstance(response, dict):
            self.fail("non_object_response", event=payload, retryable=False)
        self.response_id = response.get("id") or self.response_id
        self.model = response.get("model") or self.model
        self.usage = response.get("usage") or self.usage
        error = payload.get("error") or response.get("error")
        if kind in {"error", "response.failed"} or error:
            error = error or {k: payload.get(k) for k in ("code", "message", "param")}
            code = error.get("code") if isinstance(error, dict) else None
            # Unknown provider codes remain visible but are not blindly retried.
            retryable = code in {
                "server_error", "internal_error", "internal_server_error",
                "rate_limit_exceeded", "rate_limit_error", "overloaded",
                "service_unavailable", "timeout", "request_timeout",
                # Relay dropped its upstream read mid-stream at HTTP 200 (aizzz: A1
                # grounding lens 2026-09-06; method cell 0053 contract_extraction
                # 2026-09-11). The exact request is replayable, so it is transient.
                "stream_read_error",
            }
            if code == "upstream_error" and error.get("message") == "Upstream service temporarily unavailable":
                retryable = True
            self.fail(kind or "error", event=payload, error=error, retryable=retryable)
        if kind == "response.incomplete":
            self.fail(kind, event=payload, error=response.get("incomplete_details"), retryable=False)
        if kind == "response.completed":
            self.complete = True

    def finish(self):
        if not self.complete:
            self.fail("empty_stream" if not self.events else "eof_before_response_completed")


class _CheckedStream(Stream[ResponseStreamEvent]):
    def _iter_events(self):
        state = _StreamState(self.response, self._client.responses._responses_error_factory)
        try:
            for event in super()._iter_events():
                state.observe(event)
                yield event
        except httpx.TransportError as exc:
            state.fail("transport_interrupted", error={"type": type(exc).__name__, "message": str(exc)},
                       retryable=isinstance(exc, (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)))
        state.finish()


class _CheckedAsyncStream(AsyncStream[ResponseStreamEvent]):
    async def _iter_events(self):
        state = _StreamState(self.response, self._client.responses._responses_error_factory)
        try:
            async for event in super()._iter_events():
                state.observe(event)
                yield event
        except httpx.TransportError as exc:
            state.fail("transport_interrupted", error={"type": type(exc).__name__, "message": str(exc)},
                       retryable=isinstance(exc, (httpx.TimeoutException, httpx.NetworkError, httpx.RemoteProtocolError)))
        state.finish()


def guard_responses_streams(model, *, error_factory=ResponsesStreamError):
    """Install a per-client guard, including the SDK's raw-response parse path.

    OpenAI has no public hook before typed streaming events reach LangChain.
    This one SDK resource hook is covered by raw-SSE integration tests, including
    sync/async and response headers. Nothing is patched globally or in site-packages.
    """

    for client, stream_type in (
        (model.root_client, _CheckedStream),
        (model.root_async_client, _CheckedAsyncStream),
    ):
        if client is None:
            continue
        resource = client.responses
        original_post = resource._post
        if getattr(original_post, "_checks_responses_stream", False):
            continue
        # The legacy agent import retains AgentError; both production factories
        # use the default provider error and install this hook exactly once.
        resource._responses_error_factory = error_factory

        @wraps(original_post)
        def post(*args, _post=original_post, _stream=stream_type, **kwargs):
            if kwargs.get("stream"):
                kwargs["stream_cls"] = _stream
            return _post(*args, **kwargs)

        post._checks_responses_stream = True
        resource._post = post
