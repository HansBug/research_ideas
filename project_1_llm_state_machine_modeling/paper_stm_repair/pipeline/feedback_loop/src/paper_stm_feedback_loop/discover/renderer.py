from __future__ import annotations

from typing import Any

from paper_stm_feedback_loop.assertions import get_assertion_environment_api_docs

from .schemas import (
    AssertionCheckPublic,
    AssertionScript,
    AttributionProjection,
    FrozenDiscoverInputs,
    ReleasedAssertionResults,
    RequirementCoverageProjection,
    RequirementSet,
    RevisionFeedback,
)
from .utils import canonical_json, sha256_data


def render_requirement_split_input(
    frozen: FrozenDiscoverInputs,
    current_result: RequirementSet | None = None,
    revision_feedback: RevisionFeedback | None = None,
) -> str:
    payload: dict[str, Any] = {
        "natural_language": frozen.natural_language,
        "nl_segments": frozen.nl_segments,
        "stm_text": frozen.stm_text,
        "inspect_digest": frozen.inspect_digest,
        "mode": "revise" if current_result else "create",
        "content_language": frozen.language,
    }
    if current_result is not None:
        payload["current_result"] = current_result.model_dump(mode="json")
        payload["revision_feedback"] = (
            revision_feedback.model_dump(mode="json") if revision_feedback else None
        )
    return canonical_json(payload)


def render_requirement_review_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    coverage: RequirementCoverageProjection,
) -> str:
    return canonical_json(
        {
            "natural_language": frozen.natural_language,
            "nl_segments": frozen.nl_segments,
            "stm_text": frozen.stm_text,
            "requirements": requirements.model_dump(mode="json"),
            "coverage_projection": coverage.model_dump(mode="json"),
            "content_language": frozen.language,
        }
    )


def render_assertion_conversion_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    current_result: AssertionScript | None = None,
    revision_feedback: RevisionFeedback | None = None,
) -> str:
    payload: dict[str, Any] = {
        "accepted_requirements": requirements.model_dump(mode="json"),
        "stm_text": frozen.stm_text,
        "inspect_digest": frozen.inspect_digest,
        "evidence_api": get_assertion_environment_api_docs(),
        "mode": "revise" if current_result else "create",
        "content_language": frozen.language,
    }
    if current_result is not None:
        payload["current_result"] = current_result.model_dump(mode="json")
        payload["revision_feedback"] = (
            revision_feedback.model_dump(mode="json") if revision_feedback else None
        )
    return canonical_json(payload)


def render_assertion_review_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    script: AssertionScript,
    public_check: AssertionCheckPublic,
) -> str:
    # This payload intentionally excludes sealed and released assertion results.
    return canonical_json(
        {
            "natural_language": frozen.natural_language,
            "stm_text": frozen.stm_text,
            "accepted_requirements": requirements.model_dump(mode="json"),
            "assertion_script": script.model_dump(mode="json"),
            "reviewed_script_hash": sha256_data(script),
            "public_check": public_check.model_dump(mode="json"),
            "evidence_api": get_assertion_environment_api_docs(),
            "content_language": frozen.language,
        }
    )


def render_adjudicator_input(
    requirements: RequirementSet,
    script: AssertionScript,
    released: ReleasedAssertionResults,
    attribution: AttributionProjection,
) -> str:
    return canonical_json(
        {
            "accepted_requirements": requirements.model_dump(mode="json"),
            "assertion_script": script.model_dump(mode="json"),
            "strict_bool_results": released.model_dump(mode="json"),
            "safe_attribution": attribution.model_dump(mode="json"),
        }
    )
