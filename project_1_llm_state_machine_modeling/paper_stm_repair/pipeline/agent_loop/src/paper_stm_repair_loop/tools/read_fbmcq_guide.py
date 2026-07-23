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
        "recommended_tools": [
            "register_coverage_plan",
            "revise_assertion",
            "eval_assert",
        ],
        "recommended_action": (
            "Choose FBMCQ whenever the proposition ranges over multiple allowed "
            "executions, valuations, paths, safety, persistence, absence, or "
            "eventual response. An explicit NL bound is not required: record the "
            "finite horizon as requirement_bound or analysis_bound. Do not call "
            "FBMCQ merely to decorate a structural or concrete-trace proposition."
        ),
        "pass_criteria": (
            "Any registered FBMCQ assertion contains one exact query whose parsed "
            "property kind and bound match its declared formal metadata, whose "
            "assumptions are grounded, and whose finite limitation is explicit."
        ),
        "limitations": [
            "query_authoring_reference_only",
            "does_not_prove_nl_alignment_or_coverage",
            "bounded_result_is_not_unbounded_correctness",
        ],
    }


def build_tool(state: GuideAccessState) -> SimpleStructuredTool:
    """Build the attempt-local FBMCQ guide reader with one required reason."""

    served_metadata: dict[str, Any] | None = None

    def read_fbmcq_guide(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        Read pyfcstm's packaged, integrity-checked FBMCQ authoring guide before
        the first attempt to read, write, revise, or request execution of an FBMCQ
        property in this Agent attempt. Full-formal Discover always reads this
        guide once after ``read_task`` so all providers receive the same capability
        description; reading it does not require later FBMCQ use.

        When to use
        -----------
        In the full-formal profile, use exactly once immediately after
        ``read_task`` and before planning/investigation. In a non-formal ablation
        this tool is not exposed.

        When not to use
        ----------------
        Do not call it repeatedly and do not use guide text as proof that a
        property holds. Reading the guide is capability normalization, not a
        quota requiring a formal assertion.

        Parameters
        ----------
        Exactly one non-empty ``reason`` string in the run content language. No
        query, path, model, run/case, URL, shell, Python/Z3, or reference/gold
        selector is accepted.

        Returns
        -------
        A JSON object with ``execution_status=completed``, ``guide_kind=fbmcq``,
        complete Markdown ``content``, upstream version/SHA-256/size/chapter
        metadata, minimum-sufficient-evidence guidance, and limitations. The guide
        covers model facts, property kinds, frames/steps/bounds, definedness,
        response windows, and vacuity avoidance.

        Execution
        ---------
        Calls ``pyfcstm.llm.get_fbmcq_language_guide_prompt_for_llm`` and its
        metadata API. pyfcstm verifies the packaged SHA-256 sidecar. Only a
        successful result marks the guide as read; coverage registration/revision
        then permits an expression containing ``fbmcq(...)``. The full guide is returned
        once; a repeated call returns only the same metadata and
        ``execution_status=no_new_guide_fact``.

        Failure semantics
        -----------------
        Resource or checksum failure leaves formal assertion registration locked.
        A registration/revision attempted first is rejected with a prerequisite;
        the Agent must read this guide and resubmit the same intended obligation.

        Evidence limitations
        --------------------
        Correct FBMCQ syntax and bounded execution do not prove that a query is
        faithful to NL, complete, sufficiently strong, non-overfitted, or suitable
        as a method-effectiveness oracle.

        Permissions
        -----------
        Read-only packaged-resource access. No arbitrary paths, filesystem scan,
        network, provider call, mutation, shell/Python/Z3, or reference/gold data.

        Examples
        --------
        The first input ``{"reason":"Read official FBMCQ syntax before registering a bounded assertion."}`` returns the full guide and SHA-256. Repeated input returns only metadata and a
        ``no_new_guide_fact`` limitation.
        """

        nonlocal served_metadata
        if served_metadata is not None:
            return {
                "execution_status": "no_new_guide_fact",
                "guide_kind": "fbmcq",
                **served_metadata,
                "reason": reason,
                "limitations": [
                    "duplicate_guide_read_not_replayed",
                    "no_new_guide_fact",
                    "use_existing_visible_guide",
                ],
            }
        result = execute()
        result["reason"] = reason
        result["guide_access_sequence"] = state.mark_read("fbmcq", result)
        served_metadata = {
            key: result.get(key)
            for key in (
                "resource_name",
                "pyfcstm_version",
                "sha256",
                "expected_sha256",
                "byte_size",
                "line_count",
                "chapter_count",
                "guide_access_sequence",
            )
        }
        return result

    return SimpleStructuredTool(
        func=read_fbmcq_guide,
        name="read_fbmcq_guide",
        description=read_fbmcq_guide.__doc__ or "read_fbmcq_guide",
        args_schema=ReadGuideInput,
    )
