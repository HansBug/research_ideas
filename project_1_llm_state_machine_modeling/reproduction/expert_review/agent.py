from __future__ import annotations

from langchain_openai import ChatOpenAI

from .schema import ExpertReviewRequest, ExpertReviewResult
from .utils import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER_ORDER,
    PROVIDER_CONFIGS,
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
        self._provider_key, self._llm = self._build_llm()

    def _build_llm(self) -> tuple[str | None, ChatOpenAI | None]:
        env = resolve_api_env()
        for provider_key in self.provider_order:
            provider = PROVIDER_CONFIGS.get(provider_key)
            if provider is None:
                continue
            api_key = None
            for env_key in provider["env_keys"]:
                api_key = env.get(env_key)
                if api_key:
                    break
            if not api_key:
                continue
            try:
                llm = ChatOpenAI(
                    model=self.model_name,
                    api_key=api_key,
                    base_url=provider["base_url"],
                    temperature=self.temperature,
                    timeout=self.timeout,
                    max_retries=0,
                )
                return provider_key, llm
            except Exception:
                continue
        return None, None

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
