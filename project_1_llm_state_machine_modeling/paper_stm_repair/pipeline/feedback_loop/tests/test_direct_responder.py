from __future__ import annotations

import time
from datetime import datetime, timezone

from langchain_core.messages import AIMessage

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

    def invoke(self, _messages):
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
        return {"raw": raw, "parsed": parsed, "parsing_error": None}


class _Model:
    def with_structured_output(self, schema, include_raw=False, method=None):
        assert include_raw is True
        assert method == "function_calling"
        return _Structured(schema)


def test_direct_responder_records_same_profile_model_and_usage(monkeypatch) -> None:
    config = LLMConfig(
        adapter="openai",
        model="configured-unit-model",
        api_key="unit-test-key",
    )
    monkeypatch.setattr(
        responder_module, "load_llm_registry", lambda _path=None: _Registry(config)
    )
    monkeypatch.setattr(
        responder_module, "create_chat_model", lambda *_args, **_kwargs: _Model()
    )
    responder = DirectStructuredResponder("unit-profile")
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
