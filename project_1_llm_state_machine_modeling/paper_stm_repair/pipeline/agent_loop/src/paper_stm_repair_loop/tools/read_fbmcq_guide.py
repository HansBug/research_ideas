from __future__ import annotations

from typing import Any

from pyfcstm.llm import (
    get_fbmcq_language_guide_prompt_for_llm,
    get_fbmcq_language_guide_prompt_metadata_for_llm,
)

from ..schemas.tools import ReadGuideInput, SimpleStructuredTool
from .guide_access import GuideAccessState


def execute() -> dict[str, Any]:
    """Return the integrity-checked upstream FBMCQ guide and metadata."""

    content = get_fbmcq_language_guide_prompt_for_llm()
    metadata = dict(get_fbmcq_language_guide_prompt_metadata_for_llm())
    return {
        "execution_status": "completed",
        "guide_kind": "fbmcq",
        **metadata,
        "content": content,
        "limitations": [
            "query_authoring_reference_only",
            "does_not_prove_nl_alignment_or_coverage",
            "bounded_result_is_not_unbounded_correctness",
        ],
    }


def build_tool(state: GuideAccessState) -> SimpleStructuredTool:
    """Build the attempt-local zero-argument FBMCQ guide reader."""

    def read_fbmcq_guide() -> dict[str, Any]:
        """Purpose
        -------
        Read pyfcstm's packaged, integrity-checked FBMCQ authoring guide before
        the first attempt to read, write, revise, or request execution of an FBMCQ
        property in this Agent attempt.

        Parameters
        ----------
        None. The strict input is exactly ``{}``; no query, path, model, run/case,
        URL, shell, Python/Z3, or reference/gold selector is accepted.

        Returns
        -------
        A JSON object with ``execution_status=completed``, ``guide_kind=fbmcq``,
        complete Markdown ``content``, upstream version/SHA-256/size/chapter
        metadata, and limitations. The guide covers model facts, property kinds,
        frames/steps/bounds, definedness, response windows, and vacuity avoidance.

        Execution
        ---------
        Calls ``pyfcstm.llm.get_fbmcq_language_guide_prompt_for_llm`` and its
        metadata API. pyfcstm verifies the packaged SHA-256 sidecar. Only a
        successful result marks the guide as read; ``evaluate_checks`` then permits
        a batch containing ``check_kind=property``.

        Failure semantics
        -----------------
        Resource or checksum failure leaves property execution locked. A property
        batch submitted first receives ``execution_status=prerequisite_required``;
        the Agent must read this guide and resubmit the unchanged intended batch.

        Evidence limitations
        --------------------
        Correct FBMCQ syntax and bounded execution do not prove that a query is
        faithful to NL, complete, sufficiently strong, non-overfitted, or suitable
        as a method-effectiveness oracle.

        Permissions
        -----------
        Read-only packaged-resource access. No arbitrary paths, filesystem scan,
        network, provider call, mutation, shell/Python/Z3, or reference/gold data.

        Example
        -------
        Input ``{}`` returns the full guide and SHA-256. Call it before the first
        ``evaluate_checks`` request whose batch contains a property draft.
        """

        result = execute()
        result["guide_access_sequence"] = state.mark_read("fbmcq", result)
        return result

    return SimpleStructuredTool(
        func=read_fbmcq_guide,
        name="read_fbmcq_guide",
        description=read_fbmcq_guide.__doc__ or "read_fbmcq_guide",
        args_schema=ReadGuideInput,
    )
