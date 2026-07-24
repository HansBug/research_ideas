from __future__ import annotations

from langchain_core.messages import AIMessage

from utils.llm import LLMConfig

from paper_stm_feedback_loop.discover import responder as responder_module
from paper_stm_feedback_loop.discover.responder import DirectStructuredResponder
from paper_stm_feedback_loop.discover.schemas import RequirementReview


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
