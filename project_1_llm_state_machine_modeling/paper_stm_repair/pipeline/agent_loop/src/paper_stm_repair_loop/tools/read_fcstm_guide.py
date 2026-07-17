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
    """Build the attempt-local zero-argument FCSTM guide reader."""

    def read_fcstm_guide() -> dict[str, Any]:
        """Purpose
        -------
        Read pyfcstm's packaged, integrity-checked FCSTM grammar and runtime
        semantics guide before the first attempt to read, inspect, execute, write,
        or modify FCSTM content in this Agent attempt.

        Parameters
        ----------
        None. The strict tool input is exactly ``{}``; no path, model, run/case,
        URL, shell, Python/Z3, or reference/gold selector is accepted.

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

        Example
        -------
        Input ``{}`` returns the full guide with a stable SHA-256. A successful
        response must precede the first ``read_task`` call.
        """

        result = execute()
        result["guide_access_sequence"] = state.mark_read("fcstm", result)
        return result

    return SimpleStructuredTool(
        func=read_fcstm_guide,
        name="read_fcstm_guide",
        description=read_fcstm_guide.__doc__ or "read_fcstm_guide",
        args_schema=ReadGuideInput,
    )
