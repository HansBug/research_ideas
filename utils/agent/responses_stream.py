"""Compatibility entry point for callers expecting the original AgentError."""

from utils.llm.responses_stream import guard_responses_streams as _guard_responses_streams

from .runtime import AgentError


def _agent_error(reason, *, response, details):
    return AgentError("provider_error", "Responses stream failed: " + reason, details=details)


def guard_responses_streams(model):
    _guard_responses_streams(model, error_factory=_agent_error)
