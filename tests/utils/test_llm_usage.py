from __future__ import annotations

from langchain_core.messages import AIMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from utils.llm.usage import (
    collect_usage_sources,
    normalize_model_output_usage,
    normalize_usage,
    select_usage_source,
)


def test_normalize_usage_keeps_missing_fields_none() -> None:
    usage = {"input_tokens": 10, "output_tokens": 3}

    normalized = normalize_usage(usage, source="usage_metadata")

    assert normalized["input_tokens"] == 10
    assert normalized["output_tokens"] == 3
    assert normalized["total_tokens"] is None
    assert normalized["cache_read_input_tokens"] is None
    assert normalized["cache_creation_input_tokens"] is None
    assert normalized["ephemeral_5m_input_tokens"] is None
    assert normalized["ephemeral_1h_input_tokens"] is None
    assert normalized["reasoning_tokens"] is None
    assert normalized["source"] == "usage_metadata"
    assert normalized["status"] == "completed"


def test_normalize_usage_reads_openai_cache_and_reasoning_shapes() -> None:
    usage = {
        "prompt_tokens": 100,
        "completion_tokens": 25,
        "total_tokens": 125,
        "input_token_details": {"cached_tokens": 40, "cache_creation": 7},
        "output_token_details": {"reasoning_tokens": 9},
    }

    normalized = normalize_usage(usage)

    assert normalized["input_tokens"] == 100
    assert normalized["output_tokens"] == 25
    assert normalized["total_tokens"] == 125
    assert normalized["cache_read_input_tokens"] == 40
    assert normalized["cache_creation_input_tokens"] == 7
    assert normalized["reasoning_tokens"] == 9


def test_normalize_usage_preserves_anthropic_ephemeral_cache_ttls() -> None:
    usage = {
        "input_tokens": 11,
        "output_tokens": 5,
        "cache_read_input_tokens": 13,
        "cache_creation": {
            "ephemeral_5m_input_tokens": 17,
            "ephemeral_1h_input_tokens": 19,
        },
    }

    normalized = normalize_usage(usage)

    assert normalized["input_tokens"] == 11
    assert normalized["cache_read_input_tokens"] == 13
    assert normalized["cache_creation_input_tokens"] == 36
    assert normalized["ephemeral_5m_input_tokens"] == 17
    assert normalized["ephemeral_1h_input_tokens"] == 19
    assert normalized["total_tokens"] is None


def test_collect_select_and_normalize_usage_sources_prefers_usage_metadata() -> None:
    message = AIMessage(
        content="ok",
        usage_metadata={"input_tokens": 8, "output_tokens": 2, "total_tokens": 10},
        response_metadata={"token_usage": {"prompt_tokens": 7, "completion_tokens": 2, "total_tokens": 9}},
    )
    result = ChatResult(
        generations=[ChatGeneration(message=message)],
        llm_output={"token_usage": {"prompt_tokens": 6, "completion_tokens": 2, "total_tokens": 8}},
    )

    sources = collect_usage_sources(result)
    selected, conflict = select_usage_source(sources)
    normalized = normalize_model_output_usage(result)

    assert [item["source"] for item in sources] == [
        "llm_output.token_usage",
        "usage_metadata",
        "response_metadata.token_usage",
    ]
    assert selected is not None
    assert selected["source"] == "usage_metadata"
    assert conflict is True
    assert normalized["source"] == "usage_metadata"
    assert normalized["usage_sources"] == [
        "llm_output.token_usage",
        "usage_metadata",
        "response_metadata.token_usage",
    ]
    assert normalized["usage_conflict"] is True
    assert normalized["input_tokens"] == 8
    assert normalized["status"] == "completed"


def test_unavailable_usage_has_status_and_none_values() -> None:
    normalized = normalize_model_output_usage(AIMessage(content="no usage"))

    assert normalized["status"] == "unavailable"
    assert normalized["source"] == "unavailable"
    assert normalized["unavailable_reason"] == "adapter_did_not_expose_provider_usage"
    assert normalized["usage_sources"] == []
    assert normalized["input_tokens"] is None
    assert normalized["output_tokens"] is None
    assert normalized["total_tokens"] is None
