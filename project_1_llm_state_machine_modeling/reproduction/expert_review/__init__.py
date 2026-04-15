from .expert_review_agent import ExpertReviewAgent, heuristic_expert_review
from .expert_review_schema import ExpertReviewRequest, ExpertReviewResult, result_to_flat_row


def review_artifacts(
    prompt: str,
    input_text: str,
    pred_output: str,
    ref_output: str | None = None,
) -> ExpertReviewResult:
    request = ExpertReviewRequest(prompt=prompt, input_text=input_text, pred_output=pred_output, ref_output=ref_output)
    return ExpertReviewAgent().review(request)


def review_model(prompt: str, input_text: str, pred_output: str, ref_output: str | None = None) -> ExpertReviewResult:
    return review_artifacts(prompt, input_text, pred_output, ref_output)

__all__ = [
    "ExpertReviewAgent",
    "ExpertReviewRequest",
    "ExpertReviewResult",
    "heuristic_expert_review",
    "review_artifacts",
    "review_model",
    "result_to_flat_row",
]
