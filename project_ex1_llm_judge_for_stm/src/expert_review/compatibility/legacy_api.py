"""``legacy_api`` 模块。

**作用**：本模块属于 ``expert_review`` 体系内的辅助实现层；具体职责
由内部 class / function 的 docstring 描述。

**设计思路**：见包级 :mod:`expert_review.compatibility` 文档与
``PYDOC_INVENTORY.md`` 盘点清单。
"""
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
    """``review_artifacts`` 函数。

    :param prompt: 见函数签名与上下文。
    :param input_text: 见函数签名与上下文。
    :param pred_output: 见函数签名与上下文。
    :param ref_output: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    request = ExpertReviewRequest(prompt=prompt, input_text=input_text, pred_output=pred_output, ref_output=ref_output)
    return ExpertReviewAgent().review(request)


def review_model(
    prompt: str,
    input_text: str,
    pred_output: str,
    ref_output: str | None = None,
) -> ExpertReviewResult:
    """``review_model`` 函数。

    :param prompt: 见函数签名与上下文。
    :param input_text: 见函数签名与上下文。
    :param pred_output: 见函数签名与上下文。
    :param ref_output: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
    return review_artifacts(prompt, input_text, pred_output, ref_output)


def heuristic_expert_review(request: ExpertReviewRequest, llm: ChatOpenAI | None = None) -> ExpertReviewResult:
    """``heuristic_expert_review`` 函数。

    :param request: 见函数签名与上下文。
    :param llm: 见函数签名与上下文。
    :return: 见函数签名与上下文。
    """
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