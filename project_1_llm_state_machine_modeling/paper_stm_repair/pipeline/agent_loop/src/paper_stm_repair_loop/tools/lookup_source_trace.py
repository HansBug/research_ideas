from __future__ import annotations

import copy
import hashlib
import json
from typing import Any

from ..schemas.tools import LookupSourceTraceInput, SourceTraceLookupResult, SimpleStructuredTool
from .post_batch_investigation import PostBatchInvestigationState

_LIMITATIONS = [
    "issue_agnostic_source_trace_only",
    "partial_or_ambiguous_mapping_not_closure",
    "no_source_semantic_verdict",
]


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _trace_from(snapshot_or_trace: dict[str, Any]) -> dict[str, Any]:
    if isinstance(snapshot_or_trace.get("source_trace"), dict):
        return snapshot_or_trace["source_trace"]
    current_records = snapshot_or_trace.get("current_records")
    if isinstance(current_records, dict) and isinstance(current_records.get("source_trace"), dict):
        return current_records["source_trace"]
    return snapshot_or_trace


def _trace_sha(trace: dict[str, Any], snapshot_or_trace: dict[str, Any]) -> str:
    for container in (snapshot_or_trace, trace):
        for key in ("trace_sha256", "source_trace_sha256", "sha256"):
            value = container.get(key) if isinstance(container, dict) else None
            if isinstance(value, str) and value:
                return value
    return _sha256_json(trace)


def _entry_refs(entry: dict[str, Any], direction: str) -> tuple[list[str], list[str]]:
    if direction == "source_to_fcstm":
        request_side = entry.get("source_elements", []) or entry.get("source_refs", []) or []
        counterpart = entry.get("intermediate_elements", []) or entry.get("fcstm_elements", []) or entry.get("fcstm_refs", []) or []
    else:
        request_side = entry.get("intermediate_elements", []) or entry.get("fcstm_elements", []) or entry.get("fcstm_refs", []) or []
        counterpart = entry.get("source_elements", []) or entry.get("source_refs", []) or []
    request_refs = [ref for ref in request_side if isinstance(ref, str)]
    counterpart_refs = [ref for ref in counterpart if isinstance(ref, str)]
    return request_refs, counterpart_refs


def execute(trace: dict[str, Any], element_refs: list[str], direction: str = "fcstm_to_source") -> dict[str, Any]:
    """Purpose: look up frozen source↔fcstm trace mappings without closure claims.

    Parameters: ``trace`` is the controller-bound issue-agnostic source trace or a
    snapshot containing it; this is not an Agent argument.  Agent parameters are
    ``element_refs`` (non-empty list of typed refs) and ``direction`` equal to
    ``source_to_fcstm`` or ``fcstm_to_source``.  Agent input cannot contain a
    filesystem path, alternate trace path, model text, run id, case id, URL,
    shell command, Python/Z3 code, or reference/gold data.

    Returns: ``SourceTraceLookupResult`` with ``execution_status``, ``direction``,
    ``requested_refs``, ``exact_matches``, ``ambiguous_matches``,
    ``untraceable_refs``, ``trace_sha256``, and ``limitations``.  Each requested
    ref is classified exactly once: exact means one trace entry with at least one
    counterpart; ambiguous means multiple entries or multiple counterpart refs;
    untraceable means no usable counterpart in the frozen trace.

    Execution: validates arguments, reads only ``trace.entries``, selects the
    request side according to ``direction``, and deterministically partitions
    requested refs into exact/ambiguous/untraceable.  It does not infer mappings
    from names, parse source files, inspect other runs, call an LLM, or mutate
    trace data.

    Failure semantics: invalid direction, empty refs, or non-string refs return
    ``invalid_arguments`` with all requested refs untraceable.  Missing trace
    entries return ``tool_unavailable``.  Ambiguity is a normal structured result,
    not an exception and not a closure verdict.

    Evidence limitations: exact mappings can support bounded grounding.  Ambiguous
    or untraceable mappings must remain visible and cannot support confirmed
    source closure; even exact mappings do not prove source semantics, NL
    alignment, model equivalence, or repair success by themselves.

    Permissions: read-only against the current run's frozen trace; no arbitrary
    paths, alternate runs/cases, network, shell, Python/Z3, writes, or hidden
    reference/gold inputs.

    Example: ``execute({"entries":[{"source_elements":["source:req1"],"intermediate_elements":["transition:T1"]}]}, ["transition:T1"], "fcstm_to_source")`` returns one exact match from ``transition:T1`` to ``source:req1`` and no ambiguous/untraceable refs.
    """

    trace_data = _trace_from(trace)
    trace_sha256 = _trace_sha(trace_data if isinstance(trace_data, dict) else {}, trace)
    try:
        params = LookupSourceTraceInput.model_validate({"element_refs": element_refs, "direction": direction})
    except Exception as exc:
        return SourceTraceLookupResult(
            execution_status="invalid_arguments",
            direction="fcstm_to_source" if direction not in {"source_to_fcstm", "fcstm_to_source"} else direction,  # type: ignore[arg-type]
            requested_refs=element_refs if isinstance(element_refs, list) else [],
            exact_matches=[],
            ambiguous_matches=[],
            untraceable_refs=element_refs if isinstance(element_refs, list) else [],
            trace_sha256=trace_sha256,
            limitations=[*_LIMITATIONS, "invalid_arguments", type(exc).__name__],
        ).model_dump(mode="json")
    if not params.element_refs or any(not isinstance(ref, str) or not ref.strip() for ref in params.element_refs):
        return SourceTraceLookupResult(
            execution_status="invalid_arguments",
            direction=params.direction,
            requested_refs=params.element_refs,
            exact_matches=[],
            ambiguous_matches=[],
            untraceable_refs=params.element_refs,
            trace_sha256=trace_sha256,
            limitations=[*_LIMITATIONS, "element_refs_must_be_non_empty_strings"],
        ).model_dump(mode="json")
    entries = trace_data.get("entries") if isinstance(trace_data, dict) else None
    if not isinstance(entries, list):
        return SourceTraceLookupResult(
            execution_status="tool_unavailable",
            direction=params.direction,
            requested_refs=params.element_refs,
            exact_matches=[],
            ambiguous_matches=[],
            untraceable_refs=params.element_refs,
            trace_sha256=trace_sha256,
            limitations=[*_LIMITATIONS, "trace_entries_unavailable"],
        ).model_dump(mode="json")
    exact: list[dict[str, Any]] = []
    ambiguous: list[dict[str, Any]] = []
    untraceable: list[str] = []
    for ref in params.element_refs:
        candidates: list[dict[str, Any]] = []
        for idx, entry in enumerate(entries):
            if not isinstance(entry, dict):
                continue
            request_refs, counterpart_refs = _entry_refs(entry, params.direction)
            if ref in request_refs:
                candidates.append({"entry_index": idx, "requested_ref": ref, "mapped_refs": counterpart_refs, "entry": copy.deepcopy(entry)})
        usable = [candidate for candidate in candidates if candidate["mapped_refs"]]
        if len(usable) == 1 and len(usable[0]["mapped_refs"]) == 1:
            exact.append(usable[0])
        elif usable:
            ambiguous.append({"requested_ref": ref, "candidates": usable})
        else:
            untraceable.append(ref)
    return SourceTraceLookupResult(
        execution_status="completed",
        direction=params.direction,
        requested_refs=params.element_refs,
        exact_matches=exact,
        ambiguous_matches=ambiguous,
        untraceable_refs=untraceable,
        trace_sha256=trace_sha256,
        limitations=list(_LIMITATIONS),
    ).model_dump(mode="json")


def build_tool(
    snapshot: dict[str, Any],
    investigation_state: PostBatchInvestigationState | None = None,
) -> SimpleStructuredTool:
    """Purpose: create ``lookup_source_trace`` bound to one frozen source trace.

    Parameters: ``snapshot`` is the controller-captured attempt snapshot or trace
    object.  It is closed over before provider dispatch; Agents only provide the
    strict ``LookupSourceTraceInput`` fields.

    Returns: a ``StructuredTool`` named ``lookup_source_trace`` with strict input
    schema and ``SourceTraceLookupResult`` output semantics.

    Execution: when a protocol state is supplied, requires one distinct eligible
    ``evaluate_checks`` batch and permits one completed consolidated lookup for
    that batch; then partitions refs using the frozen trace hash.

    Failure semantics: invalid refs/direction and missing trace are structured
    failures; ambiguous/untraceable mappings are explicit normal outputs and must
    not be hidden.

    Evidence limitations: this can ground refs but never proves source closure,
    source semantics, model equivalence, or repair success by itself.

    Permissions: no Agent-supplied paths, alternate traces, model/run/case
    selectors, network, shell, Python/Z3, writes, or reference/gold inputs.

    Example: ``build_tool(snapshot).invoke({"element_refs":["transition:T1"],"direction":"fcstm_to_source"})`` returns exact/ambiguous/untraceable mapping buckets tied to the frozen ``trace_sha256``.
    """

    frozen = copy.deepcopy(snapshot)

    def lookup_source_trace(element_refs: list[str], direction: str = "fcstm_to_source") -> dict[str, Any]:
        """Purpose
        -------
        Resolve typed element references through the current run's frozen,
        issue-agnostic source-to-fcstm trace when a Discover proposition needs an
        attribution boundary after an eligible full-batch ``evaluate_checks``
        result. Submit all refs for the current batch in one consolidated call;
        the Controller permits one completed lookup per distinct eligible
        draft-batch hash, and re-evaluating identical drafts does not reopen it.
        The tool classifies recorded mappings; it does not
        infer semantic equivalence, create issue bindings, or declare closure.

        Parameters
        ----------
        ``element_refs`` (required JSON array of strings): one or more exact typed
        refs already present in the source trace, such as ``transition:T1``,
        ``state:Root.Idle``, or a source-side ref. Empty strings and an empty list
        are invalid. Names are not fuzzy-matched.
        ``direction`` (string enum, default ``fcstm_to_source``):
        ``fcstm_to_source`` treats each requested ref as an intermediate/fcstm
        element and returns source counterparts; ``source_to_fcstm`` does the
        reverse. The strict input accepts no extra fields or alternate trace.

        Returns
        -------
        A ``SourceTraceLookupResult`` JSON object:

        - ``execution_status``: ``completed``, ``invalid_arguments``, or
          ``tool_unavailable`` for this deterministic adapter.
        - ``direction`` and ``requested_refs``: effective request identity.
        - ``exact_matches``: refs with exactly one usable trace entry and exactly
          one counterpart; each item includes ``requested_ref``, ``mapped_refs``,
          ``entry_index``, and the copied trace ``entry``.
        - ``ambiguous_matches``: refs with multiple usable entries or counterpart
          refs; each item preserves every candidate rather than choosing one.
        - ``untraceable_refs``: refs with no usable counterpart.
        - ``trace_sha256``: frozen trace identity; compare with ``read_task``.
        - ``limitations``: issue-agnostic/partial-mapping evidence boundaries.
        Every requested ref appears in exactly one of the three result buckets.

        Execution
        ---------
        1. Require a distinct eligible full-batch ``evaluate_checks`` result and
           reject repeated source lookup for the same draft-batch hash.
        2. Validate the direction and non-empty exact ref strings.
        3. Read only ``entries`` from the source trace closed over before dispatch.
        4. Select source or intermediate side according to ``direction``.
        5. Partition each ref deterministically into exact, ambiguous, or
           untraceable without name guessing, parsing files, or consulting an LLM.
        6. Return all candidates and the same frozen trace hash; no cache refresh,
           latest-state lookup, issue mutation, or record publication occurs.

        Failure semantics
        -----------------
        Missing eligible evaluation returns ``prerequisite_required``. A second
        lookup for the same eligible draft batch returns ``invalid_arguments`` and
        must not be retried. Invalid direction, empty list, non-string, or blank ref returns
        ``invalid_arguments`` and no exact match. Missing/non-list trace entries
        returns ``tool_unavailable``. Ambiguous and untraceable are normal
        completed mapping outcomes, not exceptions; never silently select an
        ambiguous candidate. A completed exact match can still be semantically
        insufficient.

        Evidence limitations
        --------------------
        Exact mapping can support current-run grounding only. Ambiguous or
        untraceable mapping cannot support a confirmed root's deterministic
        attribution. Even an exact mapping does not prove NL alignment, source
        semantics, behavioral equivalence, source closure, correctness, or Repair
        success. A conversion/lowering difference is not a source behavioral issue
        merely because the mapping exists.

        Permissions
        -----------
        Read-only current-attempt trace. No arbitrary paths, alternate trace,
        model/run/case selector, network, shell, Python/Z3, writes, future-stage
        data, or hidden reference/gold assets.

        Example
        -------
        Input ``{"element_refs":["transition:T1"],"direction":"fcstm_to_source"}``
        may return ``{"execution_status":"completed","direction":"fcstm_to_source","requested_refs":["transition:T1"],"exact_matches":[{"entry_index":0,"requested_ref":"transition:T1","mapped_refs":["source:req1"],"entry":{...}}],"ambiguous_matches":[],"untraceable_refs":[],"trace_sha256":"...","limitations":[...]}``.
        """

        trace = _trace_from(frozen)
        trace_sha256 = _trace_sha(trace, frozen)
        batch_sha256 = (
            investigation_state.latest_eligible_batch()
            if investigation_state is not None
            else None
        )
        if investigation_state is not None and batch_sha256 is None:
            return SourceTraceLookupResult(
                execution_status="prerequisite_required",
                direction=direction,
                requested_refs=element_refs,
                exact_matches=[],
                ambiguous_matches=[],
                untraceable_refs=element_refs,
                trace_sha256=trace_sha256,
                limitations=[*_LIMITATIONS, "eligible_evaluate_checks_required_first"],
            ).model_dump(mode="json")
        if (
            investigation_state is not None
            and batch_sha256 is not None
            and investigation_state.already_completed("lookup_source_trace", batch_sha256)
        ):
            return SourceTraceLookupResult(
                execution_status="invalid_arguments",
                direction=direction,
                requested_refs=element_refs,
                exact_matches=[],
                ambiguous_matches=[],
                untraceable_refs=element_refs,
                trace_sha256=trace_sha256,
                limitations=[
                    *_LIMITATIONS,
                    "post_batch_source_lookup_already_completed",
                    "one_lookup_per_distinct_eligible_batch",
                ],
            ).model_dump(mode="json")
        result = execute(frozen, element_refs, direction)
        if (
            investigation_state is not None
            and batch_sha256 is not None
            and result.get("execution_status") == "completed"
        ):
            investigation_state.mark_completed("lookup_source_trace", batch_sha256)
        return result

    return SimpleStructuredTool(func=lookup_source_trace, name="lookup_source_trace", description=lookup_source_trace.__doc__ or "lookup_source_trace", args_schema=LookupSourceTraceInput)
