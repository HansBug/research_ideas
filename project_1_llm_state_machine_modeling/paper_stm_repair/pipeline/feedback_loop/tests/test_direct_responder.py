from __future__ import annotations

import time
from datetime import datetime, timezone

import pytest
from langchain_core.messages import AIMessage, AIMessageChunk
from langchain_core.runnables.utils import AddableDict

from utils.llm import LLMConfig

from paper_stm_feedback_loop.discover import responder as responder_module
from paper_stm_feedback_loop.discover import nodes
from paper_stm_feedback_loop.discover.responder import DirectStructuredResponder
from paper_stm_feedback_loop.discover.schemas import DiscoverInput, RequirementReview


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


class _IncompleteStructured:
    def stream(self, _messages):
        raw = AIMessageChunk(
            content="",
            tool_call_chunks=[
                {
                    "name": "RequirementReview",
                    "args": (
                        '{"decision":"accept","reviewed_revision":1,'
                        '"rationale":'
                    ),
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


class _IncompleteModel:
    def with_structured_output(self, _schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        return _IncompleteStructured()


class _RecoveringIncompleteModel:
    def __init__(self) -> None:
        self.calls = 0

    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        self.calls += 1
        return _IncompleteStructured() if self.calls == 1 else _Structured(schema)


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
        on_stream_chunk=lambda role, chunks, elapsed_ms: stream_updates.append(
            (role, chunks, elapsed_ms)
        ),
    )
    assert created["streaming"] is True
    assert created["max_retries"] == 0
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
    assert observation.configured_model == "configured-unit-model"
    assert observation.observed_model == "observed-unit-model"
    assert observation.usage["input_tokens"] == 120
    assert observation.usage["cache_read_input_tokens"] == 20
    assert len(observation.attempts) == 1
    assert [(role, chunks) for role, chunks, _ in stream_updates] == [
        ("requirement_reviewer", 1),
        ("requirement_reviewer", 2),
        ("requirement_reviewer", 3),
    ]
    assert all(elapsed_ms >= 0 for _, _, elapsed_ms in stream_updates)

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

    with pytest.raises(RuntimeError, match="structured tool-call arguments are incomplete"):
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
