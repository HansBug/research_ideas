from __future__ import annotations

from typing import Any, Literal

from .config import LLMConfig

PromptCacheTTL = Literal["5m", "1h"]


def prompt_cache_policy(
    config: LLMConfig, *, ttl: PromptCacheTTL = "5m"
) -> dict[str, Any]:
    """Return the adapter-owned prompt-cache policy exposed in run records."""

    if config.adapter == "anthropic":
        return {"mode": "anthropic-ephemeral", "enabled": True, "ttl": ttl}
    return {"mode": "provider-default", "enabled": None, "ttl": None}


def cached_system_prompt_content(
    config: LLMConfig,
    text: str,
    *,
    ttl: PromptCacheTTL | None,
) -> str | list[dict[str, Any]]:
    """Place an Anthropic cache breakpoint after tools and the system prefix."""

    if config.adapter != "anthropic" or ttl is None:
        return text
    return [
        {
            "type": "text",
            "text": text,
            "cache_control": {"type": "ephemeral", "ttl": ttl},
        }
    ]


__all__ = [
    "PromptCacheTTL",
    "cached_system_prompt_content",
    "prompt_cache_policy",
]
