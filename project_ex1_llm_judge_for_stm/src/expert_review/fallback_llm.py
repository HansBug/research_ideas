"""Multi-provider LLM client with automatic fallback + per-provider cooldown.

Design:
- Holds an ordered chain of (provider_key, ChatOpenAI) candidates.
- On `.invoke(messages)`, tries providers in order. A provider that fails
  (timeout / connection error / HTTP error) is put into cooldown for
  `cooldown_seconds`; subsequent calls skip it until the cooldown expires,
  at which point we retry — so when the higher-quality provider recovers,
  we resume using it ASAP.
- `.bind(**kwargs)` returns a new FallbackLLMClient with each candidate
  replaced by `candidate.bind(**kwargs)`. Cooldown state is shared so
  bound clones don't bypass cooldowns.

Drop-in compatible with langchain_openai.ChatOpenAI for our usage —
we only call `.invoke(messages)` and `.bind(**kwargs)` on the LLM.
"""
from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class _CooldownState:
    """Shared cooldown state across the original client and all .bind() clones."""
    cooldowns: dict[str, float] = field(default_factory=dict)  # provider_key -> earliest_retry_epoch
    failure_log: list[dict[str, Any]] = field(default_factory=list)
    success_log: list[dict[str, Any]] = field(default_factory=list)
    lock: threading.Lock = field(default_factory=threading.Lock)

    def is_in_cooldown(self, provider_key: str) -> bool:
        """``is_in_cooldown`` 函数。

        :param provider_key: 见函数签名与上下文。
        :return: 见函数签名与上下文。
        """
        with self.lock:
            return self.cooldowns.get(provider_key, 0.0) > time.time()

    def mark_failure(self, provider_key: str, cooldown_s: float, exc: Exception) -> None:
        """``mark_failure`` 函数。

        :param provider_key: 见函数签名与上下文。
        :param cooldown_s: 见函数签名与上下文。
        :param exc: 见函数签名与上下文。
        """
        with self.lock:
            self.cooldowns[provider_key] = time.time() + cooldown_s
            self.failure_log.append({
                "provider": provider_key,
                "type": type(exc).__name__,
                "message": str(exc)[:300],
                "ts": time.time(),
                "cooldown_until": self.cooldowns[provider_key],
            })

    def mark_success(self, provider_key: str) -> None:
        """``mark_success`` 函数。

        :param provider_key: 见函数签名与上下文。
        """
        with self.lock:
            # Successful call clears cooldown for this provider (it's alive again)
            self.cooldowns.pop(provider_key, None)
            self.success_log.append({"provider": provider_key, "ts": time.time()})


class FallbackLLMClient:
    """Tries providers in chain order; skips those in cooldown; raises only
    when ALL providers in the chain failed for this single call."""

    def __init__(
        self,
        chain: list[tuple[str, Any]],
        cooldown_seconds: dict[str, int] | None = None,
        default_cooldown: int = 180,
        state: _CooldownState | None = None,
    ) -> None:
        """内部 helper：``__init__``。

        :param chain: 见函数签名与上下文。
        :param cooldown_seconds: 见函数签名与上下文。
        :param default_cooldown: 见函数签名与上下文。
        :param state: 见函数签名与上下文。
        """
        if not chain:
            raise ValueError("FallbackLLMClient requires at least one (provider_key, llm) tuple")
        self._chain = chain  # [(provider_key, ChatOpenAI / RunnableBinding), ...]
        self._cooldown_map = dict(cooldown_seconds or {})
        self._default_cooldown = default_cooldown
        self._state = state if state is not None else _CooldownState()
        # Track last successful provider (for telemetry / "_provider_key" backward-compat)
        self.last_provider_used: str | None = None

    @property
    def primary_provider_key(self) -> str:
        """First provider in chain — used for backward-compat label fields."""
        return self._chain[0][0]

    def _cooldown_for(self, provider_key: str) -> float:
        """内部 helper：``_cooldown_for``。

        :param provider_key: 见函数签名与上下文。
        :return: 见函数签名与上下文。
        """
        return float(self._cooldown_map.get(provider_key, self._default_cooldown))

    def invoke(self, messages: Any, **kwargs: Any) -> Any:
        """Try each provider in chain order. On failure, mark cooldown and try
        next. Raise the LAST exception only if ALL providers failed.

        2026-05-08: When chain has only 1 provider, cooldown logic is bypassed
        — there's nothing to fall back to, so cooldown only hurts (locks out
        legitimate retries). Single-provider mode = always retry.
        """
        single_provider = len(self._chain) == 1
        last_exc: Exception | None = None
        attempts: list[str] = []
        skipped: list[str] = []
        for provider_key, llm in self._chain:
            if not single_provider and self._state.is_in_cooldown(provider_key):
                skipped.append(provider_key)
                continue
            attempts.append(provider_key)
            try:
                result = llm.invoke(messages, **kwargs)
                self._state.mark_success(provider_key)
                self.last_provider_used = provider_key
                return result
            except Exception as exc:
                if not single_provider:
                    cooldown_s = self._cooldown_for(provider_key)
                    self._state.mark_failure(provider_key, cooldown_s, exc)
                last_exc = exc
                continue
        # All providers either in cooldown or failed
        if last_exc is not None:
            raise last_exc
        # All in cooldown — try first anyway (force retry, in case all expired)
        provider_key, llm = self._chain[0]
        try:
            result = llm.invoke(messages, **kwargs)
            self._state.mark_success(provider_key)
            self.last_provider_used = provider_key
            return result
        except Exception as exc:
            if not single_provider:
                cooldown_s = self._cooldown_for(provider_key)
                self._state.mark_failure(provider_key, cooldown_s, exc)
            raise

    def bind(self, **kwargs: Any) -> "FallbackLLMClient":
        """Return a new FallbackLLMClient with `.bind(**kwargs)` applied to
        every underlying client. Cooldown state is shared so we don't lose
        cooldown info across bound clones (e.g. JSON mode binding).
        """
        bound_chain = [(pk, llm.bind(**kwargs)) for pk, llm in self._chain]
        return FallbackLLMClient(
            bound_chain,
            cooldown_seconds=self._cooldown_map,
            default_cooldown=self._default_cooldown,
            state=self._state,  # ← share state
        )

    # Some langchain helpers do `getattr(llm, '_default_response_format', None)`,
    # etc. Forward unknown attribute access to the primary provider's underlying client.
    def __getattr__(self, name: str) -> Any:
        """内部 helper：``__getattr__``。

        :param name: 见函数签名与上下文。
        :return: 见函数签名与上下文。
        """
        if name.startswith("_"):
            raise AttributeError(name)
        # Fall back to the first chain LLM's attribute
        return getattr(self._chain[0][1], name)

    def __repr__(self) -> str:
        """内部 helper：``__repr__``。
        :return: 见函数签名与上下文。
        """
        keys = ",".join(pk for pk, _ in self._chain)
        return f"FallbackLLMClient(chain=[{keys}])"


def build_fallback_chain(
    *,
    model: str,
    provider_order: list[str],
    provider_configs: dict[str, dict[str, Any]],
    env: dict[str, str],
    temperature: float = 0.0,
    timeout: float = 30.0,
) -> list[tuple[str, Any]]:
    """Build the (provider_key, ChatOpenAI) chain by walking provider_order
    and collecting providers that have an API key set.

    Returns a possibly-empty list. Caller decides whether to wrap in
    FallbackLLMClient or fall through to deterministic mode.
    """
    from langchain_openai import ChatOpenAI

    chain: list[tuple[str, Any]] = []
    for provider_key in provider_order:
        provider = provider_configs.get(provider_key)
        if provider is None:
            continue
        api_key = None
        for env_key in provider["env_keys"]:
            value = env.get(env_key)
            if value:
                api_key = value
                break
        if not api_key:
            continue
        # 2026-05-08: respect provider's wire_api preference
        # airouter / findcg / miaocg / deepghs are reasoning-model providers
        # (gpt-5.5 with hidden chain-of-thought) that work via /v1/responses.
        # langchain ChatOpenAI's default /v1/chat/completions deadlocks against
        # their reasoning + SSE stack. Setting use_responses_api=True fixes it.
        wire_api = provider.get("wire_api", "chat_completions")
        use_responses = wire_api == "responses"
        try:
            kwargs = dict(
                model=model,
                api_key=api_key,
                base_url=provider["base_url"],
                temperature=temperature,
                timeout=timeout,
                # 2026-05-08: 充分 retry 给 airouter reasoning model + transient 限速空间
                # langchain-openai 默认指数 backoff（base=0.5s, max=2s, jitter）
                # 8 次 retry = ~30s wallclock 累计，充分消化短 spike
                max_retries=8,
            )
            if use_responses:
                # use_responses_api routes to /v1/responses with proper reasoning-model handling
                kwargs["use_responses_api"] = True
            llm = ChatOpenAI(**kwargs)
        except Exception:
            continue
        chain.append((provider_key, llm))
    return chain


__all__ = ["FallbackLLMClient", "build_fallback_chain"]