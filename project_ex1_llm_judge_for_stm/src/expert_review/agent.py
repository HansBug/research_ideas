from __future__ import annotations

from langchain_openai import ChatOpenAI

from .fallback_llm import FallbackLLMClient, build_fallback_chain
from .schema import ExpertReviewRequest, ExpertReviewResult
from .utils import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER_ORDER,
    PROVIDER_CONFIGS,
    PROVIDER_COOLDOWN_SECONDS,
    PROVIDER_FALLBACK_TIMEOUT,
    DEFAULT_COOLDOWN_SECONDS,
    resolve_api_env,
)
from .graph.runtime import run_expert_review_workflow


class ExpertReviewAgent:
    def __init__(
        self,
        model: str = DEFAULT_MODEL,
        provider_order: list[str] | None = None,
        temperature: float = 0.0,
        timeout: int = 180,
    ) -> None:
        self.model_name = model
        self.provider_order = list(DEFAULT_PROVIDER_ORDER) if provider_order is None else list(provider_order)
        self.temperature = temperature
        self.timeout = timeout
        # Use a SHORT per-attempt timeout so we fail-fast through the fallback
        # chain. The user-supplied `timeout` is treated as the upper bound on
        # the entire fallback attempt; per-provider timeout is capped tighter.
        self._per_attempt_timeout = min(int(timeout), PROVIDER_FALLBACK_TIMEOUT)
        self._provider_key, self._llm = self._build_llm()

    def _build_llm(self) -> tuple[str | None, FallbackLLMClient | None]:
        env = resolve_api_env()
        chain = build_fallback_chain(
            model=self.model_name,
            provider_order=self.provider_order,
            provider_configs=PROVIDER_CONFIGS,
            env=env,
            temperature=self.temperature,
            timeout=self._per_attempt_timeout,
        )
        if not chain:
            return None, None
        client = FallbackLLMClient(
            chain,
            cooldown_seconds=PROVIDER_COOLDOWN_SECONDS,
            default_cooldown=DEFAULT_COOLDOWN_SECONDS,
        )
        # Backward-compat: report the FIRST provider as the "provider_key".
        # Telemetry can read `client.last_provider_used` after each call.
        return client.primary_provider_key, client

    def review(self, request: ExpertReviewRequest) -> ExpertReviewResult:
        backend_label = "langgraph_multi_agent_v1"
        if self._llm is None:
            return run_expert_review_workflow(
                request,
                llm=None,
                llm_model_name=None,
                llm_provider=None,
                backend_label=f"{backend_label}_deterministic",
            )
        try:
            return run_expert_review_workflow(
                request,
                llm=self._llm,
                llm_model_name=self.model_name,
                llm_provider=self._provider_key,
                backend_label=f"{backend_label}_llm",
            )
        except Exception as exc:
            result = run_expert_review_workflow(
                request,
                llm=None,
                llm_model_name=self.model_name,
                llm_provider=self._provider_key,
                backend_label=f"{backend_label}_fallback",
            )
            result.notes.append(f"LLM-enabled runtime failed and fell back to deterministic flow: {type(exc).__name__}: {exc}")
            return result
