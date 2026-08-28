from __future__ import annotations

import time
from datetime import datetime, timezone

import httpx
import openai
import pytest
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.runnables.utils import AddableDict
from paper_stm_feedback_loop.discover import nodes
from paper_stm_feedback_loop.discover import responder as responder_module
from paper_stm_feedback_loop.discover.responder import DirectStructuredResponder
from paper_stm_feedback_loop.discover.schemas import DiscoverInput, RequirementReview

from utils.llm import LLMConfig


class _Registry:
    def __init__(self, config: LLMConfig) -> None:
        self.config = config

    def require(self, name: str) -> LLMConfig:
        assert name == "unit-profile"
        return self.config


class _Structured:
    def __init__(self, schema):
        self.schema = schema

    def stream(self, _messages):
        parsed = self.schema(
            decision="accept",
            reviewed_revision=1,
            rationale="The requirement set is complete.",
        )
        raw = AIMessage(
            content="",
            usage_metadata={
                "input_tokens": 120,
                "output_tokens": 30,
                "total_tokens": 150,
                "input_token_details": {"cache_read": 20},
            },
            response_metadata={"model_name": "observed-unit-model"},
        )
        yield AddableDict(raw=raw)
        yield AddableDict(parsed=parsed)
        yield AddableDict(parsing_error=None)


class _Model:
    def __init__(self):
        self.structured_options = None

    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.structured_options = {
            "include_raw": include_raw,
            "method": method,
        }
        return _Structured(schema)


class _InvokeStructured(_Structured):
    def invoke(self, messages):
        response = None
        for chunk in self.stream(messages):
            response = chunk if response is None else response + chunk
        return response


class _InvokeOnlyModel:
    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        return _InvokeStructured(schema)


class _IncompleteStructured:
    def stream(self, _messages):
        raw = AIMessageChunk(
            content="",
            usage_metadata={
                "input_tokens": 100,
                "output_tokens": 10,
                "total_tokens": 110,
            },
            tool_call_chunks=[
                {
                    "name": "RequirementReview",
                    "args": ('{"decision":"accept","reviewed_revision":1,"rationale":'),
                    "id": "incomplete-call",
                    "index": 0,
                }
            ],
        )
        parsed = RequirementReview(
            decision="accept",
            reviewed_revision=1,
            rationale="The requirement set is complete.",
        )
        yield AddableDict(raw=raw)
        yield AddableDict(parsed=parsed)
        yield AddableDict(parsing_error=None)


class _TruncatedStructured(_IncompleteStructured):
    def stream(self, messages):
        chunks = list(super().stream(messages))
        raw = chunks[0]["raw"]
        raw.response_metadata = {"stop_reason": "max_tokens"}
        yield from chunks


class _IncompleteModel:
    def with_structured_output(self, _schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        return _IncompleteStructured()


class _TruncatedModel:
    def with_structured_output(self, _schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        return _TruncatedStructured()


class _ProviderError(RuntimeError):
    status_code = 503


class _ProviderFailureStructured:
    def stream(self, _messages):
        raise _ProviderError("provider unavailable")
        yield  # pragma: no cover


class _RecoveringProviderModel:
    def __init__(self) -> None:
        self.calls = 0

    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.calls += 1
        return _ProviderFailureStructured() if self.calls == 1 else _Structured(schema)


class _RelayedUpstreamFailureStructured:
    def stream(self, _messages):
        request = httpx.Request("POST", "https://provider.invalid/v1/chat/completions")
        response = httpx.Response(400, request=request)
        raise openai.BadRequestError(
            "Error code: 400",
            response=response,
            body={
                "message": "Upstream request failed request-id=fixture",
                "type": "invalid_request_error",
            },
        )
        yield  # pragma: no cover


class _RecoveringRelayedUpstreamModel(_RecoveringProviderModel):
    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.calls += 1
        return (
            _RelayedUpstreamFailureStructured()
            if self.calls == 1
            else _Structured(schema)
        )


class _RelayToolChoiceDriftStructured:
    def stream(self, _messages):
        request = httpx.Request("POST", "https://provider.invalid/v1/chat/completions")
        response = httpx.Response(400, request=request)
        raise openai.BadRequestError(
            "Error code: 400",
            response=response,
            body={
                "error": {
                    "message": (
                        "Missing required parameter: 'tool_choice.name'. "
                        "request-id=fixture"
                    ),
                    "type": "invalid_request_error",
                }
            },
        )
        yield  # pragma: no cover


class _RecoveringRelayToolChoiceDriftModel(_RecoveringProviderModel):
    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.calls += 1
        return (
            _RelayToolChoiceDriftStructured()
            if self.calls == 1
            else _Structured(schema)
        )


class _RecoveringIncompleteModel:
    def __init__(self) -> None:
        self.calls = 0

    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.calls += 1
        return _IncompleteStructured() if self.calls == 1 else _Structured(schema)


class _CapturingAnthropicModel:
    def __init__(self) -> None:
        self.messages = []

    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method is None
        parent = self

        class _CapturingStructured(_Structured):
            def stream(self, messages):
                parent.messages = messages
                yield from super().stream(messages)

        return _CapturingStructured(schema)


def test_direct_responder_records_same_profile_model_and_usage(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    created = {}

    def create_model(*_args, **kwargs):
        created.update(kwargs)
        model = _Model()
        created["model"] = model
        return model

    monkeypatch.setattr(responder_module, "create_chat_model", create_model)
    stream_updates = []
    responder = DirectStructuredResponder(
        "unit-profile",
        effort="xhigh",
        on_stream_chunk=lambda role, chunks, elapsed_ms: stream_updates.append(
            (role, chunks, elapsed_ms)
        ),
    )
    assert created["streaming"] is True
    assert created["max_retries"] == 0
    assert created["effort"] == "xhigh"
    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )
    observation = responder.take_last_observation()

    assert output.decision == "accept"
    assert observation is not None
    assert observation.profile == "unit-profile"
    assert observation.requested_effort == "xhigh"
    assert observation.configured_model == "configured-unit-model"
    assert observation.observed_model == "observed-unit-model"
    assert observation.schema_contract_repeated_in_prompt is True
    assert len(observation.structured_schema_sha256) == 64
    assert observation.system_prompt.startswith("system")
    assert len(observation.system_prompt) > len("system")
    assert observation.usage["input_tokens"] == 120
    assert observation.usage["cache_read_input_tokens"] == 20
    assert len(observation.attempts) == 1
    assert [(role, chunks) for role, chunks, _ in stream_updates] == [
        ("requirement_reviewer", 1),
        ("requirement_reviewer", 2),
        ("requirement_reviewer", 3),
    ]
    assert all(elapsed_ms >= 0 for _, _, elapsed_ms in stream_updates)

    compact_responder = DirectStructuredResponder(
        "unit-profile", repeat_schema_in_prompt=False
    )
    compact_responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )
    compact_observation = compact_responder.take_last_observation()
    assert compact_observation is not None
    assert compact_observation.system_prompt == "system"
    assert compact_observation.schema_contract_repeated_in_prompt is False
    assert (
        compact_observation.structured_schema_sha256
        == observation.structured_schema_sha256
    )

    state = {
        "_input": DiscoverInput(
            run_id="record-hash",
            natural_language="A requirement.",
            stm_text="state Root { }",
            profile="unit-profile",
            language="en-US",
        )
    }
    state["frozen_inputs"] = nodes._fallback_prepare(state["_input"])
    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )
    started = datetime.now(timezone.utc)
    node_record = nodes._record_node(
        state,
        node_name="unit",
        revision=1,
        kind="llm",
        input_value="user",
        output_value=output,
        started_at=started,
        start_ns=time.perf_counter_ns(),
    )
    llm_record = nodes._llm_call_record(
        state,
        responder=responder,
        node_record=node_record,
        role="requirement_reviewer",
        revision=1,
        system_prompt="system",
        user_prompt="user",
        output=output,
    )
    assert llm_record.system_prompt_sha256
    assert llm_record.user_prompt_sha256
    assert llm_record.parsed_output_sha256
    assert llm_record.raw_response_sha256
    assert llm_record.streaming is True
    assert llm_record.requested_effort == "xhigh"


def test_responses_adapter_uses_non_streaming_structured_invoke(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai-responses",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    created = {}

    def create_model(*_args, **kwargs):
        created.update(kwargs)
        return _InvokeOnlyModel()

    monkeypatch.setattr(responder_module, "create_chat_model", create_model)
    progress = []
    responder = DirectStructuredResponder(
        "unit-profile",
        streaming=False,
        on_stream_chunk=lambda role, chunks, elapsed_ms: progress.append(
            (role, chunks, elapsed_ms)
        ),
    )

    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )
    observation = responder.take_last_observation()

    assert output.decision == "accept"
    assert observation is not None
    assert observation.adapter == "openai-responses"
    assert created["streaming"] is False
    assert [(role, chunks) for role, chunks, _ in progress] == [
        ("requirement_reviewer", 1)
    ]
    assert observation.streaming is False


@pytest.mark.parametrize("streaming", [True, False])
def test_explicit_streaming_override_is_recorded(monkeypatch, streaming: bool) -> None:
    config = LLMConfig(
        adapter="openai-responses",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    created = {}

    def create_model(*_args, **kwargs):
        created.update(kwargs)
        return _Model() if streaming else _InvokeOnlyModel()

    monkeypatch.setattr(responder_module, "create_chat_model", create_model)
    responder = DirectStructuredResponder("unit-profile", streaming=streaming)
    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )
    assert output.decision == "accept"
    observation = responder.take_last_observation()
    assert observation is not None
    assert observation.streaming is streaming
    assert created["streaming"] is streaming


def test_direct_responder_marks_stable_anthropic_prefix_for_one_hour_cache(
    monkeypatch,
) -> None:
    config = LLMConfig(
        adapter="anthropic",
        model="claude-opus-4-7",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    model = _CapturingAnthropicModel()
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: model,
    )
    responder = DirectStructuredResponder(
        "unit-profile",
        repeat_schema_in_prompt=False,
        prompt_cache_ttl="1h",
    )

    responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="stable-system-prefix",
        user_input="pair-specific dossier",
    )

    observation = responder.take_last_observation()
    assert observation is not None
    assert observation.prompt_cache == {
        "mode": "anthropic-ephemeral",
        "enabled": True,
        "ttl": "1h",
    }
    assert model.messages[0].content == [
        {
            "type": "text",
            "text": "stable-system-prefix",
            "cache_control": {"type": "ephemeral", "ttl": "1h"},
        }
    ]
    assert model.messages[1].content == "pair-specific dossier"


def test_direct_responder_rejects_incomplete_structured_stream(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: _IncompleteModel(),
    )
    responder = DirectStructuredResponder("unit-profile", transport_retries=0)

    with pytest.raises(
        RuntimeError, match="structured tool-call arguments are incomplete"
    ):
        responder.invoke_structured(
            role="requirement_reviewer",
            schema=RequirementReview,
            system_prompt="system",
            user_input="user",
        )

    observation = responder.take_last_observation()
    assert observation is not None
    assert observation.status == "failed"
    assert len(observation.attempts) == 1
    assert observation.attempts[0]["failure_phase"] == "structured_stream"
    assert observation.attempts[0]["retryable"] is True
    assert observation.attempts[0]["cost_counted"] is True
    assert observation.usage["input_tokens"] == 100


def test_direct_responder_retries_incomplete_stream_without_business_revision(
    monkeypatch,
) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    model = _RecoveringIncompleteModel()
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: model,
    )
    responder = DirectStructuredResponder("unit-profile", transport_retries=1)

    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )

    observation = responder.take_last_observation()
    assert output.decision == "accept"
    assert observation is not None
    assert observation.status == "completed"
    assert model.calls == 2
    assert [attempt["status"] for attempt in observation.attempts] == [
        "failed",
        "completed",
    ]
    assert observation.attempts[0]["failure_phase"] == "structured_stream"
    assert observation.attempts[0]["cost_counted"] is True
    assert observation.usage["input_tokens"] == 220
    assert observation.usage["output_tokens"] == 40
    assert observation.usage["total_tokens"] == 260


def test_output_limit_is_counted_and_not_blindly_transport_retried(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: _TruncatedModel(),
    )
    responder = DirectStructuredResponder("unit-profile", transport_retries=3)

    with pytest.raises(
        responder_module.StructuredOutputTruncatedError,
        match="stop_reason='max_tokens'",
    ):
        responder.invoke_structured(
            role="requirement_reviewer",
            schema=RequirementReview,
            system_prompt="system",
            user_input="user",
        )

    observation = responder.take_last_observation()
    assert observation is not None
    assert len(observation.attempts) == 1
    assert observation.attempts[0]["failure_phase"] == "structured_output_limit"
    assert observation.attempts[0]["retryable"] is False
    assert observation.attempts[0]["cost_counted"] is True
    assert observation.usage["total_tokens"] == 110


def test_provider_error_retry_is_the_only_cost_exemption(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    model = _RecoveringProviderModel()
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: model,
    )
    monkeypatch.setattr(responder_module, "_retry_delay", lambda *_args: 0.0)
    responder = DirectStructuredResponder("unit-profile", transport_retries=1)

    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )

    observation = responder.take_last_observation()
    assert output.decision == "accept"
    assert observation is not None
    assert model.calls == 2
    assert observation.attempts[0]["failure_phase"] == "provider_response"
    assert observation.attempts[0]["cost_counted"] is False
    assert observation.attempts[0]["billing_disposition"] == (
        "provider_error_retry_exempt"
    )
    assert observation.attempts[1]["cost_counted"] is True
    assert observation.usage["input_tokens"] == 120
    assert observation.usage["output_tokens"] == 30


def test_relay_mislabeled_upstream_error_retries_in_place_and_is_exempt(
    monkeypatch,
) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    model = _RecoveringRelayedUpstreamModel()
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: model,
    )
    monkeypatch.setattr(responder_module, "_retry_delay", lambda *_args: 0.0)
    responder = DirectStructuredResponder("unit-profile", transport_retries=1)

    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )

    observation = responder.take_last_observation()
    assert output.decision == "accept"
    assert observation is not None
    assert model.calls == 2
    assert observation.attempts[0]["failure_phase"] == "provider_response"
    assert observation.attempts[0]["retryable"] is True
    assert observation.attempts[0]["cost_counted"] is False
    assert observation.attempts[0]["billing_disposition"] == (
        "provider_error_retry_exempt"
    )
    assert observation.attempts[1]["billing_disposition"] == "counted"


def test_relay_tool_choice_contract_drift_retries_in_place_and_is_exempt(
    monkeypatch,
) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    model = _RecoveringRelayToolChoiceDriftModel()
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: model,
    )
    monkeypatch.setattr(responder_module, "_retry_delay", lambda *_args: 0.0)
    responder = DirectStructuredResponder("unit-profile", transport_retries=1)

    output = responder.invoke_structured(
        role="requirement_reviewer",
        schema=RequirementReview,
        system_prompt="system",
        user_input="user",
    )

    observation = responder.take_last_observation()
    assert output.decision == "accept"
    assert observation is not None
    assert model.calls == 2
    assert observation.attempts[0]["failure_phase"] == "provider_response"
    assert observation.attempts[0]["retryable"] is True
    assert observation.attempts[0]["cost_counted"] is False
    assert observation.attempts[0]["billing_disposition"] == (
        "provider_error_retry_exempt"
    )
    assert observation.attempts[1]["billing_disposition"] == "counted"


def test_unretried_provider_error_is_counted(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    monkeypatch.setattr(
        responder_module,
        "create_chat_model",
        lambda *_args, **_kwargs: _RecoveringProviderModel(),
    )
    responder = DirectStructuredResponder("unit-profile", transport_retries=0)

    with pytest.raises(RuntimeError, match="provider unavailable"):
        responder.invoke_structured(
            role="requirement_reviewer",
            schema=RequirementReview,
            system_prompt="system",
            user_input="user",
        )

    observation = responder.take_last_observation()
    assert observation is not None
    assert len(observation.attempts) == 1
    assert observation.attempts[0]["cost_counted"] is True
    assert observation.attempts[0]["billing_disposition"] == "counted"


def test_empty_structured_output_is_retryable_but_schema_violations_are_not() -> None:
    """A tool call whose streamed JSON never assembled must be retried.

    Pair 0006 died on attempt 1 with `model_type / input=None` even though the
    provider had emitted a well-formed RequirementSet: the streamed
    `partial_json` was simply never merged.  That is a transport symptom, and
    marking it permanent threw away an otherwise healthy run.
    """

    import sys
    from pathlib import Path

    src = Path(__file__).resolve().parents[1] / "src"
    if str(src) not in sys.path:
        sys.path.insert(0, str(src))
    from paper_stm_feedback_loop.discover.responder import _retryable_error
    from pydantic import BaseModel, ValidationError

    class Shape(BaseModel):
        value: int

    try:
        Shape.model_validate(None)
    except ValidationError as exc:
        assert _retryable_error(exc) is True

    try:
        Shape.model_validate({"value": "not-an-int"})
    except ValidationError as exc:
        assert _retryable_error(exc) is False, (
            "a genuine schema violation must reach the contract loop, not be retried"
        )
