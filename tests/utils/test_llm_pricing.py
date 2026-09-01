from __future__ import annotations

from utils.llm import (
    LLMPricing,
    LLMTokenPrices,
    estimate_usage_cost_usd,
)


def _pricing() -> LLMPricing:
    return LLMPricing(
        prices=LLMTokenPrices(
            input_usd_per_million_tokens=5,
            output_usd_per_million_tokens=25,
            cache_read_usd_per_million_tokens=0.5,
            cache_write_usd_per_million_tokens=6.25,
        ),
        source_url="https://docs.anthropic.com/en/docs/about-claude/pricing",
        verified_on="2026-08-18",
        basis="official_list_price",
        scope_note="Standard-context list price.",
    )


def test_estimate_usage_cost_prices_each_cache_class_once() -> None:
    result = estimate_usage_cost_usd(
        {
            "input_tokens": 100,
            "output_tokens": 20,
            "cache_read_input_tokens": 40,
            "cache_creation_input_tokens": 20,
        },
        _pricing(),
    )

    assert result["eligible"] is True
    assert result["categories"]["input"]["tokens"] == 40
    assert result["total_usd"] == 0.000845


def test_estimate_usage_cost_normalizes_nested_provider_cache_fields() -> None:
    result = estimate_usage_cost_usd(
        {
            "input_tokens": 100,
            "output_tokens": 20,
            "input_token_details": {"cache_read": 40, "cache_creation": 20},
        },
        _pricing(),
    )

    assert result["eligible"] is True
    assert result["categories"]["input"]["tokens"] == 40
    assert result["categories"]["cache_read"]["tokens"] == 40
    assert result["categories"]["cache_write"]["tokens"] == 20
    assert result["total_usd"] == 0.000845


def test_estimate_usage_cost_does_not_double_bill_reasoning_tokens() -> None:
    result = estimate_usage_cost_usd(
        {
            "input_tokens": 100,
            "output_tokens": 20,
            "reasoning_tokens": 9,
        },
        _pricing(),
    )

    assert result["eligible"] is True
    assert result["categories"]["output"]["tokens"] == 20
    assert result["output_usd"] == 0.0005
    assert result["total_usd"] == 0.001


def test_estimate_usage_cost_uses_default_cache_write_price() -> None:
    result = estimate_usage_cost_usd(
        {
            "input_tokens": 20,
            "output_tokens": 1,
            "cache_creation_input_tokens": 10,
        },
        _pricing(),
    )

    assert result["eligible"] is True
    assert result["categories"]["cache_write"]["tokens"] == 10
    assert result["total_usd"] == 0.0001375


def test_estimate_usage_cost_prices_generic_cache_miss_as_configured() -> None:
    pricing = LLMPricing(
        prices=LLMTokenPrices(
            input_usd_per_million_tokens=0.22,
            output_usd_per_million_tokens=0.66,
            cache_read_usd_per_million_tokens=0.007,
            cache_write_usd_per_million_tokens=0.22,
        ),
        source_url="https://api-docs.deepseek.com/quick_start/pricing",
        verified_on="2026-08-18",
        basis="official_list_price",
        scope_note="DeepSeek direct API off-peak list price.",
    )

    result = estimate_usage_cost_usd(
        {
            "input_tokens": 1_000_000,
            "output_tokens": 0,
            "cache_read_input_tokens": 600_000,
            "cache_creation_input_tokens": 400_000,
        },
        pricing,
    )

    assert result["eligible"] is True
    assert result["categories"]["input"]["tokens"] == 0
    assert result["categories"]["cache_write"]["tokens"] == 400_000
    assert result["total_usd"] == 0.0922


def test_estimate_usage_cost_records_mature_engine() -> None:
    result = estimate_usage_cost_usd(
        {"input_tokens": 100, "output_tokens": 20}, _pricing()
    )

    assert result["eligible"] is True
    assert result["engine"]["package"] == "genai-prices"
