from __future__ import annotations

from collections.abc import Mapping
from decimal import Decimal
from typing import Any

import genai_prices
from genai_prices import Usage
from genai_prices.types import ModelPrice

from .config import LLMPricing, LLMTokenPrices


def _token_count(usage: Mapping[str, Any], key: str) -> int | None:
    value = usage.get(key)
    return (
        value
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0
        else None
    )


def _decimal(value: float | None) -> Decimal | None:
    return Decimal(str(value)) if value is not None else None


def _model_price(prices: LLMTokenPrices) -> ModelPrice:
    return ModelPrice(
        input_mtok=_decimal(prices.input_usd_per_million_tokens),
        output_mtok=_decimal(prices.output_usd_per_million_tokens),
        cache_read_mtok=_decimal(prices.cache_read_usd_per_million_tokens),
        cache_write_mtok=_decimal(prices.cache_write_usd_per_million_tokens),
    )


def estimate_usage_cost_usd(
    usage: Mapping[str, Any],
    pricing: LLMPricing,
) -> dict[str, Any]:
    """Calculate configured input/output/cache-read/cache-write cost.

    Provider ``output_tokens`` already includes reasoning tokens.  Keep the
    reasoning detail for analysis, but never add it as a separate billing
    class here.
    """

    errors: list[str] = []
    input_tokens = _token_count(usage, "input_tokens")
    output_tokens = _token_count(usage, "output_tokens")
    if input_tokens is None or output_tokens is None:
        errors.append("input_tokens and output_tokens must be available")
        input_tokens = input_tokens or 0
        output_tokens = output_tokens or 0

    cache_read = _token_count(usage, "cache_read_input_tokens") or 0
    cache_creation = _token_count(usage, "cache_creation_input_tokens") or 0

    uncached_input = input_tokens - cache_read - cache_creation
    if uncached_input < 0:
        errors.append("cache token classes exceed input_tokens")
        uncached_input = 0
    prices = pricing.prices
    if cache_read and prices.cache_read_usd_per_million_tokens is None:
        errors.append("cache read tokens have no configured price")
    if cache_creation and prices.cache_write_usd_per_million_tokens is None:
        errors.append("cache write tokens have no configured price")

    calculation = None
    if not errors:
        try:
            calculation = _model_price(prices).calc_price(
                Usage(
                    input_tokens=input_tokens,
                    output_tokens=output_tokens,
                    cache_read_tokens=cache_read,
                    cache_write_tokens=cache_creation,
                )
            )
        except (TypeError, ValueError) as exc:
            errors.append(f"genai-prices rejected usage: {exc}")

    categories = {
        "input": {
            "tokens": uncached_input,
            "usd_per_million_tokens": prices.input_usd_per_million_tokens,
        },
        "cache_read": {
            "tokens": cache_read,
            "usd_per_million_tokens": prices.cache_read_usd_per_million_tokens,
        },
        "cache_write": {
            "tokens": cache_creation,
            "usd_per_million_tokens": prices.cache_write_usd_per_million_tokens,
        },
        "output": {
            "tokens": output_tokens,
            "usd_per_million_tokens": prices.output_usd_per_million_tokens,
        },
    }
    return {
        "schema": "utils.llm.usage_cost.v1",
        "eligible": not errors,
        "total_usd": float(calculation["total_price"])
        if calculation is not None
        else None,
        "input_usd": float(calculation["input_price"])
        if calculation is not None
        else None,
        "output_usd": float(calculation["output_price"])
        if calculation is not None
        else None,
        "currency": "USD",
        "categories": categories,
        "selected_rate_card": "configured",
        "engine": {"package": "genai-prices", "version": genai_prices.__version__},
        "pricing": pricing.model_dump(mode="json"),
        "errors": errors,
    }


__all__ = ["estimate_usage_cost_usd"]
