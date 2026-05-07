from __future__ import annotations

from langchain_openai import ChatOpenAI

from ..agent import ExpertReviewAgent
from ..schema import ExpertReviewRequest, ExpertReviewResult
from ..graph.runtime import run_expert_review_workflow


def review_artifacts(
    prompt: str,
    input_text: str,
    pred_output: str,
    ref_output: str | None = None,
) -> ExpertReviewResult:
    request = ExpertReviewRequest(prompt=prompt, input_text=input_text, pred_output=pred_output, ref_output=ref_output)
    return ExpertReviewAgent().review(request)


def review_model(
    prompt: str,
    input_text: str,
    pred_output: str,
    ref_output: str | None = None,
) -> ExpertReviewResult:
    return review_artifacts(prompt, input_text, pred_output, ref_output)


def heuristic_expert_review(request: ExpertReviewRequest, llm: ChatOpenAI | None = None) -> ExpertReviewResult:
    backend_label = "langgraph_multi_agent_v1_deterministic"
    if llm is not None:
        backend_label = "langgraph_multi_agent_v1_hybrid"
    return run_expert_review_workflow(
        request,
        llm=llm,
        llm_model_name=None,
        llm_provider=None,
        backend_label=backend_label,
    )


__all__ = ["heuristic_expert_review", "review_artifacts", "review_model"]
