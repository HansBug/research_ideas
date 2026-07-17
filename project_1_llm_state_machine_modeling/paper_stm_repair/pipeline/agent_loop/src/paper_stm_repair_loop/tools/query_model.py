from __future__ import annotations

import copy
import json
from typing import Any

from ..schemas.tools import ModelQueryResult, QueryModelInput, SimpleStructuredTool

_QUERY_KINDS = {"states", "events", "transitions", "variables", "diagnostics"}
_LIMITATIONS = [
    "structural_fact_only",
    "no_issue_or_quality_verdict",
    "bounded_to_frozen_normalized_inspect",
]


def _model_sha256_from(snapshot_or_inspect: dict[str, Any]) -> str:
    for key in ("model_sha256", "fcstm_sha256"):
        value = snapshot_or_inspect.get(key)
        if isinstance(value, str) and value:
            return value
    model = snapshot_or_inspect.get("model")
    if isinstance(model, dict):
        for key in ("model_sha256", "fcstm_sha256"):
            value = model.get(key)
            if isinstance(value, str) and value:
                return value
    return "unknown"


def _inspect_from(snapshot_or_inspect: dict[str, Any]) -> dict[str, Any]:
    for key in ("normalized_inspect", "inspect"):
        value = snapshot_or_inspect.get(key)
        if isinstance(value, dict):
            return value
    model = snapshot_or_inspect.get("model")
    if isinstance(model, dict):
        for key in ("normalized_inspect", "inspect"):
            value = model.get(key)
            if isinstance(value, dict):
                return value
    current_records = snapshot_or_inspect.get("current_records")
    if isinstance(current_records, dict):
        check = current_records.get("check_fcstm") or current_records.get("check_result")
        if isinstance(check, dict) and isinstance(check.get("inspect"), dict):
            return check["inspect"]
    return snapshot_or_inspect


def _items_for(inspect_data: dict[str, Any], query_kind: str) -> list[dict[str, Any]]:
    raw = inspect_data.get(query_kind, [])
    if isinstance(raw, dict):
        iterable = raw.values()
    elif isinstance(raw, list):
        iterable = raw
    else:
        iterable = []
    items: list[dict[str, Any]] = []
    for index, item in enumerate(iterable):
        if isinstance(item, dict):
            normalized = copy.deepcopy(item)
        else:
            normalized = {"value": item}
        normalized.setdefault("_index", index)
        items.append(normalized)
    return items


def execute(
    inspect: dict[str, Any],
    query_kind: str = "states",
    name_contains: str | None = None,
    offset: int = 0,
    limit: int = 50,
) -> dict[str, Any]:
    """Purpose: query paginated structural facts from frozen normalized inspect.

    Parameters: ``inspect`` is the controller-bound normalized inspect dictionary
    or an early snapshot containing it; this is not an Agent argument.  Agent
    parameters are ``query_kind`` (one of ``states``, ``events``,
    ``transitions``, ``variables``, ``diagnostics``), optional
    ``name_contains`` case-insensitive substring filter over the JSON rendering of
    each structural item, integer ``offset`` starting at 0, and integer ``limit``
    from 1 to 500.  The Agent never supplies model text, filesystem paths, run
    identifiers, case identifiers, URLs, shell commands, Python/Z3, or reference
    assets.

    Returns: ``ModelQueryResult`` with ``execution_status``, ``query_kind``,
    ``matched_items``, ``total_matches``, ``offset``, ``limit``, ``truncated``,
    ``model_sha256``, and ``limitations``.  ``matched_items`` contains only the
    requested page; ``total_matches`` counts all filtered matches before paging.

    Execution: the function extracts the already normalized inspect payload,
    selects the requested category, applies the optional substring filter, slices
    by ``offset``/``limit``, and validates the result with strict Pydantic output
    schema.  It does not parse/reload the model, call an LLM, run simulation, run
    verification, or infer behavior.

    Failure semantics: invalid enum, negative offset, nonpositive/oversized limit,
    or non-string filter returns ``execution_status=invalid_arguments`` with an
    empty page and explicit limitation; unavailable inspect data returns
    ``tool_unavailable``.  Domain facts such as diagnostics or missing states are
    data, not exceptions or issue verdicts.

    Evidence limitations: structural facts may help ground references and decide
    whether more evidence is needed.  They cannot alone confirm an issue, prove a
    property, show NL alignment, establish source closure, or turn a warning into
    a repairable defect.

    Permissions: read-only against the frozen current model inspect; no arbitrary
    path, alternate model, run/case selector, network, shell, Python/Z3 execution,
    mutation, or reference/gold access.

    Example: ``execute({"model_sha256":"m1","states":[{"path":"Root.Idle"}]}, "states", "Idle", 0, 10)`` returns ``{"execution_status":"completed","query_kind":"states","matched_items":[{"path":"Root.Idle","_index":0}],"total_matches":1,"offset":0,"limit":10,"truncated":false,"model_sha256":"m1","limitations":[...]}``.
    """

    # Backward-compatible bridge for the earlier registry call shape
    # ``execute(inspect, query_kind, limit)`` while the Agent-facing contract uses
    # ``name_contains, offset, limit``.
    if isinstance(name_contains, int) and offset == 0 and limit == 50:
        limit = name_contains
        name_contains = None
    model_sha256 = _model_sha256_from(inspect)
    try:
        params = QueryModelInput.model_validate(
            {"query_kind": query_kind, "name_contains": name_contains, "offset": offset, "limit": limit}
        )
    except Exception as exc:
        safe_kind = query_kind if query_kind in _QUERY_KINDS else "states"
        return ModelQueryResult(
            execution_status="invalid_arguments",
            query_kind=safe_kind,  # type: ignore[arg-type]
            matched_items=[],
            total_matches=0,
            offset=0 if not isinstance(offset, int) or offset < 0 else offset,
            limit=50 if not isinstance(limit, int) or limit <= 0 else limit,
            truncated=False,
            model_sha256=model_sha256,
            limitations=[*_LIMITATIONS, "invalid_arguments", type(exc).__name__],
        ).model_dump(mode="json")
    if params.offset < 0 or params.limit < 1 or params.limit > 500:
        return ModelQueryResult(
            execution_status="invalid_arguments",
            query_kind=params.query_kind,
            matched_items=[],
            total_matches=0,
            offset=max(0, params.offset),
            limit=50 if params.limit < 1 or params.limit > 500 else params.limit,
            truncated=False,
            model_sha256=model_sha256,
            limitations=[*_LIMITATIONS, "offset_or_limit_out_of_range"],
        ).model_dump(mode="json")
    inspect_data = _inspect_from(inspect)
    if not isinstance(inspect_data.get(params.query_kind, []), (list, dict)):
        return ModelQueryResult(
            execution_status="tool_unavailable",
            query_kind=params.query_kind,
            matched_items=[],
            total_matches=0,
            offset=params.offset,
            limit=params.limit,
            truncated=False,
            model_sha256=model_sha256,
            limitations=[*_LIMITATIONS, "normalized_inspect_category_unavailable"],
        ).model_dump(mode="json")
    items = _items_for(inspect_data, params.query_kind)
    if params.name_contains:
        needle = params.name_contains.casefold()
        items = [item for item in items if needle in json.dumps(item, ensure_ascii=False, sort_keys=True).casefold()]
    total = len(items)
    page = items[params.offset : params.offset + params.limit]
    return ModelQueryResult(
        execution_status="completed",
        query_kind=params.query_kind,
        matched_items=page,
        total_matches=total,
        offset=params.offset,
        limit=params.limit,
        truncated=params.offset + params.limit < total,
        model_sha256=model_sha256,
        limitations=list(_LIMITATIONS),
    ).model_dump(mode="json")


def build_tool(snapshot: dict[str, Any]) -> SimpleStructuredTool:
    """Purpose: create the ``query_model`` tool bound to one frozen inspect.

    Parameters: ``snapshot`` is the controller-captured attempt snapshot or
    normalized inspect object.  It is closed over before provider dispatch;
    Agents only provide the strict ``QueryModelInput`` fields.

    Returns: a ``StructuredTool`` named ``query_model`` with strict Pydantic input
    schema and ``ModelQueryResult`` output semantics.

    Execution: each invocation delegates to ``execute`` using the closed-over
    snapshot/inspect and therefore remains bound to the current attempt's model
    hash.  No cache refresh or latest-state lookup is performed.

    Failure semantics: bad Agent arguments return structured
    ``invalid_arguments``; missing inspect returns ``tool_unavailable``; no bare
    exception text is treated as model evidence.

    Evidence limitations: the tool exposes structure only, never a quality,
    behavior, source-closure, or repair verdict.

    Permissions: no Agent-supplied paths, model text, run/case identifiers,
    network, shell, Python/Z3, writes, or reference/gold inputs.

    Example: ``build_tool(snapshot).invoke({"query_kind":"states","offset":0,"limit":5})`` returns a paginated ``ModelQueryResult``.
    """

    frozen = copy.deepcopy(snapshot)

    def query_model(
        query_kind: str,
        name_contains: str | None = None,
        offset: int = 0,
        limit: int = 50,
    ) -> dict[str, Any]:
        """Purpose
        -------
        Query normalized structural facts for the frozen ``STM_0`` when the
        Discover workflow has a named evidence gap, such as locating a state,
        checking an event's qualified name, inspecting a transition shape, or
        reviewing a diagnostic. This tool returns facts only; it does not create
        checks, assess propositions, or issue a quality/repair verdict.

        Parameters
        ----------
        ``query_kind`` (required string enum): exactly one of ``states``,
        ``events``, ``transitions``, ``variables``, or ``diagnostics``.
        ``name_contains`` (optional string or null, default null): case-insensitive
        substring matched against each item's canonical JSON; it is not a regex,
        query language, state predicate, or solver expression.
        ``offset`` (integer, default 0): zero-based index in the filtered result;
        must be at least 0.
        ``limit`` (integer, default 50): maximum page size; must be 1 through 500.
        The strict JSON input accepts no additional fields.

        Returns
        -------
        A ``ModelQueryResult`` JSON object:

        - ``execution_status``: ``completed``, ``invalid_arguments``, or
          ``tool_unavailable`` for this deterministic adapter.
        - ``query_kind``: normalized requested category.
        - ``matched_items``: only the requested page; each item preserves inspect
          fields and includes deterministic ``_index`` when absent.
        - ``total_matches``: filtered count before pagination.
        - ``offset`` / ``limit``: effective page arguments.
        - ``truncated``: true when another page exists after this page.
        - ``model_sha256``: frozen model identity; compare it with ``read_task``.
        - ``limitations``: machine-readable evidence-boundary/status notes.

        Execution
        ---------
        1. Validate the strict enum, filter type, offset, and limit.
        2. Read only the normalized inspect category closed over before dispatch.
        3. Normalize items, apply the substring filter, count matches, and slice
           ``[offset:offset+limit]`` deterministically.
        4. Return a strict schema tied to the same frozen ``model_sha256``. No
           model parsing/reload, simulation, BMC, LLM call, cache refresh, or
           latest-state lookup occurs.

        Failure semantics
        -----------------
        Invalid enum/type/range returns ``invalid_arguments`` with an empty page
        and limitation code. Missing/non-structural inspect category returns
        ``tool_unavailable``. An empty completed page is a valid domain result and
        does not mean the model element is impossible or erroneous. Diagnostics
        are facts and remain non-verdict evidence.

        Evidence limitations
        --------------------
        Use results to ground element refs or decide whether another bounded trace
        or source mapping is needed. A matched/missing item, diagnostic, or page
        count cannot alone confirm an issue, prove behavior, prove NL alignment,
        establish source closure, justify Repair, or prove completeness. If
        ``truncated=true``, fetch the required next page before claiming absence.

        Permissions
        -----------
        Read-only and current-attempt only. No arbitrary paths, alternate model,
        run/case selectors, network, shell, Python/Z3, custom predicates, writes,
        future stage data, or hidden reference/gold assets.

        Example
        -------
        Input ``{"query_kind":"states","name_contains":"Idle","offset":0,"limit":10}``
        returns ``{"execution_status":"completed","query_kind":"states","matched_items":[{"path":"Root.Idle","_index":0}],"total_matches":1,"offset":0,"limit":10,"truncated":false,"model_sha256":"...","limitations":[...]}``.
        """

        return execute(frozen, query_kind, name_contains, offset, limit)

    return SimpleStructuredTool(func=query_model, name="query_model", description=query_model.__doc__ or "query_model", args_schema=QueryModelInput)
