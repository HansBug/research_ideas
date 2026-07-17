from __future__ import annotations

import copy
from typing import Any

from ..schemas.tools import FrozenTaskSnapshot, ReadTaskInput, SimpleStructuredTool


_ALLOWED_KEYS = ("stage", "loop_no", "model", "targets", "current_records", "readable_history")


def _coerce_frozen_snapshot(snapshot: dict[str, Any]) -> FrozenTaskSnapshot:
    candidate = snapshot.get("frozen_task") if isinstance(snapshot.get("frozen_task"), dict) else snapshot
    six_field_view = {key: copy.deepcopy(candidate[key]) for key in _ALLOWED_KEYS if key in candidate}
    missing = [key for key in _ALLOWED_KEYS if key not in six_field_view]
    if missing:
        # Compatibility bridge for early PR-discover snapshots while keeping the
        # Agent-facing surface exactly six keys.
        six_field_view.setdefault("stage", str(candidate.get("stage", "B-discover")))
        six_field_view.setdefault("loop_no", int(candidate.get("loop_no", 0)))
        six_field_view.setdefault(
            "model",
            {
                "fcstm": candidate.get("fcstm", ""),
                "fcstm_sha256": candidate.get("fcstm_sha256", candidate.get("model_sha256", "")),
                "context_snapshot_head": candidate.get("context_snapshot_head", ""),
            },
        )
        six_field_view.setdefault("targets", copy.deepcopy(candidate.get("targets", [])))
        six_field_view.setdefault(
            "current_records",
            {
                "nl": candidate.get("nl"),
                "raw_source": candidate.get("raw_source"),
                "source_trace": candidate.get("source_trace"),
                "issue_checks": candidate.get("issue_checks", []),
                "tool_results": candidate.get("tool_results", {}),
                "evidence_index": candidate.get("evidence_index", {}),
            },
        )
        six_field_view.setdefault("readable_history", copy.deepcopy(candidate.get("readable_history", [])))
    return FrozenTaskSnapshot.model_validate(six_field_view)


def execute(snapshot: dict[str, Any]) -> dict[str, Any]:
    """Purpose: return the Discover Agent's attempt-frozen six-field task snapshot.

    Parameters: ``snapshot`` is a controller-owned Python dictionary that is
    already bound to the current Discover attempt before provider dispatch.  It
    is not an Agent argument and must not contain a caller-supplied path, model
    replacement, run selector, case selector, URL, shell command, Python code, or
    reference/gold asset.  If the dictionary contains ``frozen_task``, that value
    is interpreted as the canonical six-field view; otherwise this compatibility
    function derives the six-field view from the current snapshot keys.

    Returns: a JSON object conforming to ``FrozenTaskSnapshot`` with exactly
    ``stage``, ``loop_no``, ``model``, ``targets``, ``current_records``, and
    ``readable_history``.  ``model`` carries the frozen fcstm content/hash and, if
    available, the ``context_snapshot_head`` hash.  ``current_records`` expands
    the NL/source/model trace/check/tool facts available to this attempt rather
    than returning mutable filesystem locations or opaque IDs only.

    Execution: the function deep-copies the controller-captured object, filters
    to the six allowed keys, validates it with a strict Pydantic schema, and
    serializes the validated model.  It performs no file IO, network IO, model
    parsing, LLM call, cache refresh, latest-state lookup, or mutation; repeated
    calls after Compact return the same closed-over snapshot.

    Failure semantics: malformed controller input raises a Pydantic validation
    error during setup or direct unit execution; a production wrapper should turn
    that into ``run_failed(context_budget_exceeded|snapshot_invalid)`` before LLM
    dispatch rather than exposing a partial task.  This tool never converts an
    exception message into evidence about the STM.

    Evidence limitations: the returned snapshot defines the evidence boundary for
    Discover only.  It does not prove that checks are semantically complete, that
    warnings are issues, that the model is correct, or that source closure holds.

    Permissions: the Agent-facing callable produced by ``build_tool`` accepts no
    parameters at all; it cannot read arbitrary paths, choose another run/case,
    replace the model, execute shell/Python/Z3, access the network, or read
    reference/gold inputs.

    Example: ``execute({"stage":"B-discover","loop_no":0,"model":{"fcstm":"state Root {}","fcstm_sha256":"abc"},"targets":[],"current_records":{"checks":[]},"readable_history":[]})``
    returns ``{"stage":"B-discover","loop_no":0,"model":{"fcstm":"state Root {}","fcstm_sha256":"abc"},"targets":[],"current_records":{"checks":[]},"readable_history":[]}``.
    """

    return _coerce_frozen_snapshot(snapshot).model_dump(mode="json")


def build_tool(snapshot: dict[str, Any]) -> SimpleStructuredTool:
    """Purpose: create the zero-argument ``read_task`` tool for one frozen attempt.

    Parameters: ``snapshot`` is the controller-captured attempt snapshot described
    by ``execute``; it is closed over by this factory and is never supplied by the
    Agent.  The resulting tool input schema is ``ReadTaskInput`` with no fields.

    Returns: a LangChain ``StructuredTool`` named ``read_task`` whose output is a
    ``FrozenTaskSnapshot`` JSON object with exactly six top-level keys.

    Execution: validation is performed once at factory time to fail closed before
    provider dispatch, then the registered callable returns the same validated
    JSON payload on every invocation.

    Failure semantics: invalid snapshot shape fails during tool construction;
    runtime calls have no domain failure mode because they perform no external IO.

    Evidence limitations: re-reading the task resolves memory/Compact
    uncertainty only; it is not evidence of model correctness or issue closure.

    Permissions: no Agent parameter can name a path, URL, run, case, alternate
    model, shell command, Python/Z3 program, or reference/gold artifact.

    Example: ``build_tool(snapshot).invoke({})`` returns the same six-field task
    object as ``execute(snapshot)``.
    """

    frozen = _coerce_frozen_snapshot(snapshot)

    def read_task() -> dict[str, Any]:
        """Purpose
        -------
        Re-read the canonical, immutable working context for this exact
        ``B-discover`` attempt. Use it to orient at the start of the workflow and
        to recover after context compaction or memory uncertainty. It is not a
        general record reader and never observes facts appended after the attempt
        snapshot was frozen.

        Parameters
        ----------
        None. The tool-call JSON object must be exactly ``{}``. Unknown keys are
        rejected by the strict input schema. In particular, there is no ``path``,
        ``run_id``, ``case_id``, ``model``, ``record_id``, or refresh flag.

        Returns
        -------
        A ``FrozenTaskSnapshot`` JSON object with exactly six top-level fields:

        - ``stage``: string stage identifier; here it must be ``B-discover``.
        - ``loop_no``: integer logical loop number; Discover uses ``0``.
        - ``model``: the complete frozen ``STM_0`` content, model identifier,
          SHA-256, and normalized inspect facts supplied to this attempt.
        - ``targets``: frozen target list; ordinary Discover currently uses ``[]``.
        - ``current_records``: expanded current-run NL, raw/source model,
          source-trace, prepared checks, Controller results, record IDs, hashes,
          statuses, and limitations available when the attempt began.
        - ``readable_history``: immutable prior-stage/loop history exposed to this
          attempt; initial Discover currently uses ``[]``.

        Execution
        ---------
        1. Return a deep-copied Pydantic-validated snapshot captured before
           provider dispatch.
        2. Preserve the same six fields, values, model hash, record set, and
           context snapshot identity on every call.
        3. Perform no filesystem scan, latest-record lookup, cache refresh,
           model execution, LLM call, or mutation.

        Failure semantics
        -----------------
        Snapshot shape, reference-blindness, and hash identity are validated by
        the Controller before this tool is exposed. A malformed or oversized
        snapshot fails the run before Agent dispatch; this function has no partial
        fallback. If a returned hash differs from the preloaded context, treat the
        attempt as invalid rather than reconciling the two views yourself.

        Evidence limitations
        --------------------
        The result identifies what evidence exists and which artifact/hash it
        belongs to. It does not prove NL alignment, check completeness, source
        closure, model correctness, absence of missed issues, or that a diagnostic
        is a behavioral defect. Record presence is not proof of its conclusion;
        inspect each record's status and limitations.

        Permissions
        -----------
        Read-only and current-attempt only. No arbitrary paths, alternate
        model/run/case selectors, network, shell, Python/Z3, writes, refresh,
        future Repair/Confirm state, or hidden reference/gold inputs are allowed.

        Example
        -------
        Input ``{}`` returns a value shaped as
        ``{"stage":"B-discover","loop_no":0,"model":{"model_id":"STM_0","content":"...","model_sha256":"..."},"targets":[],"current_records":{"nl":{...}},"readable_history":[]}``.
        """

        return frozen.model_dump(mode="json")

    return SimpleStructuredTool(func=read_task, name="read_task", description=read_task.__doc__ or "read_task", args_schema=ReadTaskInput)
