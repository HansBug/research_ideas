"""Validate Responses SSE termination before LangChain can discard failure events.

The SDK owns SSE decoding. Only its per-resource stream class is substituted;
request parameters, parsing of successful events, and dependency files stay intact.
"""

from functools import wraps
import json

import httpx
from openai import AsyncStream, Stream
from openai.types.responses import ResponseStreamEvent

from .runtime import AgentError, _exception_details, _retryable_transport_error


class _StreamState:
    def __init__(self, response):
        self.request_id = response.headers.get("x-request-id")
        self.response_id = None
        self.usage = None
        self.events = []
        self.complete = False

    def fail(self, reason, *, event=None, error=None, retryable=True):
        raise AgentError(
            "provider_error",
            "Responses stream failed: " + reason,
            details={
                "source": "provider", "type": "ResponsesStreamError",
                "reason": reason, "retryable": retryable,
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
        state = _StreamState(self.response)
        try:
            for event in super()._iter_events():
                state.observe(event)
                yield event
        except httpx.TransportError as exc:
            state.fail("transport_interrupted", error=_exception_details(exc),
                       retryable=_retryable_transport_error(exc))
        state.finish()


class _CheckedAsyncStream(AsyncStream[ResponseStreamEvent]):
    async def _iter_events(self):
        state = _StreamState(self.response)
        try:
            async for event in super()._iter_events():
                state.observe(event)
                yield event
        except httpx.TransportError as exc:
            state.fail("transport_interrupted", error=_exception_details(exc),
                       retryable=_retryable_transport_error(exc))
        state.finish()


def guard_responses_streams(model):
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

        @wraps(original_post)
        def post(*args, _post=original_post, _stream=stream_type, **kwargs):
            if kwargs.get("stream"):
                kwargs["stream_cls"] = _stream
            return _post(*args, **kwargs)

        resource._post = post
