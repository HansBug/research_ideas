from __future__ import annotations

from typing import Any

from pyfcstm.llm import (
    get_grammar_guide_prompt_for_llm,
    get_grammar_guide_prompt_metadata_for_llm,
)

from ..schemas.tools import ReadGuideInput, SimpleStructuredTool
from .guide_access import GuideAccessState


def execute() -> dict[str, Any]:
    """Return the integrity-checked upstream FCSTM guide and metadata."""

    content = get_grammar_guide_prompt_for_llm()
    metadata = dict(get_grammar_guide_prompt_metadata_for_llm())
    return {
        "execution_status": "completed",
        "guide_kind": "fcstm",
        **metadata,
        "content": content,
        "limitations": [
            "language_and_runtime_semantics_reference_only",
            "does_not_prove_nl_fidelity",
            "does_not_replace_parse_semantic_simulation_or_verification",
        ],
    }


def build_tool(state: GuideAccessState) -> SimpleStructuredTool:
    """Build the attempt-local FCSTM guide reader with one required reason."""

    served_metadata: dict[str, Any] | None = None

    def read_fcstm_guide(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        Read pyfcstm's packaged, integrity-checked FCSTM grammar and runtime
        semantics guide before the first attempt to read, inspect, execute, write,
        or modify FCSTM content in this Agent attempt.

        When to use
        -----------
        Use as the first business tool call of every Discover attempt.

        When not to use
        ----------------
        Do not repeat it to refresh context or use it as model evidence.

        Parameters
        ----------
        Exactly one non-empty ``reason`` string in the run content language. No
        path, model, run/case, URL, shell, Python/Z3, or reference/gold selector
        is accepted.

        Returns
        -------
        A JSON object with ``execution_status=completed``, ``guide_kind=fcstm``,
        complete Markdown ``content``, and upstream ``resource_name``,
        ``pyfcstm_version``, ``sha256``, ``expected_sha256``, ``byte_size``,
        ``line_count``, and ``chapter_count`` metadata plus limitations.

        Execution
        ---------
        Calls ``pyfcstm.llm.get_grammar_guide_prompt_for_llm`` and its metadata
        API. pyfcstm verifies the packaged SHA-256 sidecar before returning text.
        Only after both calls succeed does this tool mark the FCSTM guide as read
        for the current attempt, enabling ``read_task`` and model-dependent tools.
        The full guide is returned once. A repeated call returns only the same
        resource/version/SHA-256 identity with
        ``execution_status=no_new_guide_fact`` and never injects the guide text a
        second time.

        Failure semantics
        -----------------
        Missing, malformed, non-UTF-8, or checksum-mismatched resources raise the
        upstream integrity error and do not unlock any FCSTM-dependent tool. The
        Controller therefore fails closed rather than falling back to copied or
        remembered syntax.

        Evidence limitations
        --------------------
        The guide defines supported language and execution semantics. It does not
        prove that a model matches NL, that a diagnostic is a source issue, that
        checks are complete, or that any repair is correct.

        Permissions
        -----------
        Read-only packaged-resource access. No arbitrary paths, filesystem scan,
        network, provider call, mutation, shell/Python/Z3, or reference/gold data.

        Examples
        --------
        The first input ``{"reason":"Read official FCSTM semantics before inspecting STM_0."}`` returns the full guide with a stable SHA-256. A
        successful response must precede the first ``read_task`` call. A repeated
        input returns only metadata and a ``no_new_guide_fact`` limitation.
        """

        nonlocal served_metadata
        if served_metadata is not None:
            return {
                "execution_status": "no_new_guide_fact",
                "guide_kind": "fcstm",
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
        result["guide_access_sequence"] = state.mark_read("fcstm", result)
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
        func=read_fcstm_guide,
        name="read_fcstm_guide",
        description=read_fcstm_guide.__doc__ or "read_fcstm_guide",
        args_schema=ReadGuideInput,
    )
