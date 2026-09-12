from __future__ import annotations

import copy
import hashlib
import json
from collections.abc import Callable
from typing import Any

from ..eval_env.topology import TopologyIndex, is_within, ref_matches
from ..pyfcstm_adapter import load_model_for_simulation
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


def _model_text_from(snapshot: dict[str, Any]) -> str | None:
    model = snapshot.get("model")
    if not isinstance(model, dict):
        return None
    value = model.get("content") or model.get("fcstm")
    return value if isinstance(value, str) and value.strip() else None


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


def _requested_filters(
    *,
    name_contains: str | None,
    exact: bool,
    path: str | None,
    within: str | None,
    source: str | None,
    event: str | None,
    target: str | None,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "name_contains": name_contains,
        "exact": exact,
        "path": path,
        "within": within,
        "source": source,
        "event": event,
        "target": target,
        **(extra or {}),
    }


def _unsupported_operation_filters(params: QueryModelInput) -> list[str]:
    """Return filters that this non-entity operation would otherwise ignore."""

    values = params.model_dump(mode="json")
    common = {
        "query_kind",
        "operation",
        "offset",
        "limit",
        "root_node_ids",
        "reason",
        "recursive",
    }
    supported = {
        "topology": {"within"},
        "path": {"source", "target", "event", "within", "exact", "avoid", "max_hops"},
    }.get(params.operation, set())
    unsupported: list[str] = []
    for key, value in values.items():
        if key in common or key in supported:
            continue
        if value not in (None, False, [], ""):
            unsupported.append(key)
    return unsupported


def _filter_entities(
    items: list[dict[str, Any]],
    query_kind: str,
    *,
    name_contains: str | None,
    exact: bool,
    path: str | None,
    within: str | None,
    source: str | None,
    event: str | None,
    target: str | None,
    parent: str | None,
    recursive: bool,
    kind: str | None,
    name: str | None,
    scope: str | None,
    declared: bool | None,
    used: bool | None,
    variable_type: str | None,
    read_in: str | None,
    written_in: str | None,
    has_event: bool | None,
    has_guard: bool | None,
    has_effect: bool | None,
    forced: bool | None,
    self_loop: bool | None,
    source_within: str | None,
    target_within: str | None,
) -> list[dict[str, Any]]:
    out = items
    if path is not None:
        key = "path" if query_kind == "states" else "qualified_name"
        out = [item for item in out if ref_matches(str(item.get(key)) if item.get(key) is not None else None, path, exact=exact)]
    if within is not None:
        if query_kind == "transitions":
            out = [item for item in out if is_within(item.get("from_path"), within) or is_within(item.get("to_path"), within)]
        else:
            key = "path" if query_kind == "states" else "qualified_name"
            out = [item for item in out if is_within(str(item.get(key)) if item.get(key) is not None else None, within)]
    if query_kind == "transitions":
        if source is not None:
            out = [item for item in out if ref_matches(item.get("from_path"), source, exact=exact)]
        if event is not None:
            out = [item for item in out if ref_matches(item.get("event"), event, exact=exact)]
        if target is not None:
            out = [item for item in out if ref_matches(item.get("to_path"), target, exact=exact)]
        if has_event is not None:
            out = [item for item in out if bool(item.get("event")) is has_event]
        if has_guard is not None:
            out = [item for item in out if bool(item.get("guard")) is has_guard]
        if has_effect is not None:
            out = [item for item in out if bool(item.get("effect")) is has_effect]
        if forced is not None:
            out = [item for item in out if bool(item.get("is_forced")) is forced]
        if self_loop is not None:
            out = [
                item
                for item in out
                if (item.get("from_path") == item.get("to_path")) is self_loop
            ]
        if source_within is not None:
            out = [item for item in out if is_within(item.get("from_path"), source_within)]
        if target_within is not None:
            out = [item for item in out if is_within(item.get("to_path"), target_within)]
    elif query_kind == "states":
        if name is not None:
            out = [item for item in out if item.get("name") == name]
        if parent is not None:
            if recursive:
                out = [item for item in out if is_within(item.get("path"), parent, include_self=False)]
            else:
                out = [item for item in out if ref_matches(item.get("parent_path"), parent, exact=exact)]
        if kind is not None:
            flag = {"leaf": "is_leaf", "composite": "is_composite", "pseudo": "is_pseudo"}[kind]
            out = [item for item in out if bool(item.get(flag))]
    elif query_kind == "events":
        if name is not None:
            out = [item for item in out if item.get("name") == name]
        if scope is not None:
            out = [item for item in out if ref_matches(item.get("scope"), scope, exact=exact)]
        if declared is not None:
            out = [item for item in out if bool(item.get("is_declared")) is declared]
        if used is not None:
            out = [item for item in out if bool(item.get("is_used")) is used]
    elif query_kind == "variables":
        if name is not None:
            out = [item for item in out if item.get("name") == name]
        if variable_type is not None:
            out = [item for item in out if item.get("type") == variable_type]
        if read_in is not None:
            out = [
                item
                for item in out
                if any(
                    ref_matches(str(ref), read_in, exact=exact)
                    for key in ("read_in_states", "read_in_guards")
                    for ref in (item.get(key) or [])
                )
            ]
        if written_in is not None:
            out = [
                item
                for item in out
                if any(
                    ref_matches(str(ref), written_in, exact=exact)
                    for key in ("written_in_states", "written_in_effects")
                    for ref in (item.get(key) or [])
                )
            ]
    if name_contains:
        needle = name_contains.casefold()
        out = [item for item in out if needle in json.dumps(item, ensure_ascii=False, sort_keys=True).casefold()]
    return out


def execute(
    inspect: dict[str, Any],
    query_kind: str = "states",
    name_contains: str | None = None,
    offset: int = 0,
    limit: int = 50,
    *,
    operation: str = "entities",
    exact: bool = False,
    path: str | None = None,
    within: str | None = None,
    parent: str | None = None,
    recursive: bool = True,
    kind: str | None = None,
    name: str | None = None,
    scope: str | None = None,
    declared: bool | None = None,
    used: bool | None = None,
    variable_type: str | None = None,
    read_in: str | None = None,
    written_in: str | None = None,
    source: str | None = None,
    event: str | None = None,
    target: str | None = None,
    has_event: bool | None = None,
    has_guard: bool | None = None,
    has_effect: bool | None = None,
    forced: bool | None = None,
    self_loop: bool | None = None,
    source_within: str | None = None,
    target_within: str | None = None,
    avoid: list[str] | None = None,
    max_hops: int | None = None,
    reason: str = "controller-internal deterministic inspect query",
    root_node_ids: list[str] | None = None,
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
    requested page; ``total_matches`` counts all filtered entity matches before paging; for ``operation=path`` it counts only returned path records with ``exists=true`` while preserving absence sentinels under ``paths``.

    Execution: entity queries use the already normalized inspect payload.
    Topology/path queries load only the same Controller-frozen FCSTM text through
    the existing adapter and call public pyfcstm topology algorithms plus a
    deterministic BFS. The function never accepts alternate model input, calls
    an LLM, runs simulation/formal verification, or infers a behavior verdict.

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
            {
                "query_kind": query_kind,
                "operation": operation,
                "name_contains": name_contains,
                "exact": exact,
                "path": path,
                "within": within,
                "parent": parent,
                "recursive": recursive,
                "kind": kind,
                "name": name,
                "scope": scope,
                "declared": declared,
                "used": used,
                "variable_type": variable_type,
                "read_in": read_in,
                "written_in": written_in,
                "source": source,
                "event": event,
                "target": target,
                "has_event": has_event,
                "has_guard": has_guard,
                "has_effect": has_effect,
                "forced": forced,
                "self_loop": self_loop,
                "source_within": source_within,
                "target_within": target_within,
                "avoid": avoid or [],
                "max_hops": max_hops,
                "offset": offset,
                "limit": limit,
                "root_node_ids": root_node_ids or [],
                "reason": reason,
            }
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
            operation=operation if operation in {"entities", "topology", "path"} else "entities",
            requested_filters=_requested_filters(name_contains=name_contains if isinstance(name_contains, str) else None, exact=bool(exact), path=path if isinstance(path, str) else None, within=within if isinstance(within, str) else None, source=source if isinstance(source, str) else None, event=event if isinstance(event, str) else None, target=target if isinstance(target, str) else None, extra={"max_hops": max_hops, "avoid": avoid or []}),
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
            operation=params.operation,
            requested_filters=_requested_filters(name_contains=params.name_contains, exact=params.exact, path=params.path, within=params.within, source=params.source, event=params.event, target=params.target, extra={"max_hops": params.max_hops, "avoid": list(params.avoid)}),
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
            operation=params.operation,
            requested_filters=_requested_filters(name_contains=params.name_contains, exact=params.exact, path=params.path, within=params.within, source=params.source, event=params.event, target=params.target, extra={"max_hops": params.max_hops, "avoid": list(params.avoid)}),
            limitations=[*_LIMITATIONS, "normalized_inspect_category_unavailable"],
        ).model_dump(mode="json")
    requested_filters = _requested_filters(
        name_contains=params.name_contains,
        exact=params.exact,
        path=params.path,
        within=params.within,
        source=params.source,
        event=params.event,
        target=params.target,
        extra={
            key: value
            for key, value in params.model_dump(mode="json").items()
            if key
            not in {
                "query_kind",
                "operation",
                "name_contains",
                "exact",
                "path",
                "within",
                "source",
                "event",
                "target",
                "offset",
                "limit",
                "root_node_ids",
                "reason",
            }
        },
    )
    effective_filters = {key: value for key, value in requested_filters.items() if value not in (None, False)}
    if params.operation == "topology":
        unsupported_filters = _unsupported_operation_filters(params)
        if unsupported_filters:
            return ModelQueryResult(
                execution_status="invalid_arguments",
                query_kind=params.query_kind,
                operation=params.operation,
                matched_items=[],
                total_matches=0,
                offset=params.offset,
                limit=params.limit,
                truncated=False,
                model_sha256=model_sha256,
                root_node_ids=list(params.root_node_ids),
                reason=params.reason,
                requested_filters=requested_filters,
                effective_filters=effective_filters,
                limitations=[
                    *_LIMITATIONS,
                    "unsupported_topology_filters",
                    *[f"unsupported_filter:{name}" for name in unsupported_filters],
                ],
            ).model_dump(mode="json")
        model_text = _model_text_from(inspect)
        machine = (
            load_model_for_simulation(model_text, "inputs/STM_0.fcstm")
            if model_text is not None
            else None
        )
        topology = TopologyIndex(inspect_data, machine).topology(within=params.within)
        return ModelQueryResult(
            execution_status="completed",
            query_kind=params.query_kind,
            operation=params.operation,
            matched_items=[],
            total_matches=len(topology.get("states", [])) + len(topology.get("transitions", [])),
            offset=params.offset,
            limit=params.limit,
            truncated=False,
            model_sha256=model_sha256,
            root_node_ids=list(params.root_node_ids),
            reason=params.reason,
            requested_filters=requested_filters,
            effective_filters=effective_filters,
            topology=topology,
            limitations=[*_LIMITATIONS, "static_topology_only", "guards_and_effects_not_evaluated"],
        ).model_dump(mode="json")
    if params.operation == "path":
        unsupported_filters = _unsupported_operation_filters(params)
        if unsupported_filters:
            return ModelQueryResult(
                execution_status="invalid_arguments",
                query_kind=params.query_kind,
                operation=params.operation,
                matched_items=[],
                total_matches=0,
                offset=params.offset,
                limit=params.limit,
                truncated=False,
                model_sha256=model_sha256,
                root_node_ids=list(params.root_node_ids),
                reason=params.reason,
                requested_filters=requested_filters,
                effective_filters=effective_filters,
                limitations=[
                    *_LIMITATIONS,
                    "unsupported_path_filters",
                    *[f"unsupported_filter:{name}" for name in unsupported_filters],
                ],
            ).model_dump(mode="json")
        if not params.source or not params.target:
            return ModelQueryResult(
                execution_status="invalid_arguments",
                query_kind=params.query_kind,
                operation=params.operation,
                matched_items=[],
                total_matches=0,
                offset=params.offset,
                limit=params.limit,
                truncated=False,
                model_sha256=model_sha256,
                root_node_ids=list(params.root_node_ids),
                reason=params.reason,
                requested_filters=requested_filters,
                effective_filters=effective_filters,
                limitations=[*_LIMITATIONS, "path_operation_requires_source_and_target"],
            ).model_dump(mode="json")
        model_text = _model_text_from(inspect)
        machine = (
            load_model_for_simulation(model_text, "inputs/STM_0.fcstm")
            if model_text is not None
            else None
        )
        paths = TopologyIndex(inspect_data, machine).path(
            source=params.source,
            target=params.target,
            event=params.event,
            within=params.within,
            max_depth=params.max_hops,
            exact=params.exact,
            avoid=tuple(params.avoid),
        )
        return ModelQueryResult(
            execution_status="completed",
            query_kind=params.query_kind,
            operation=params.operation,
            matched_items=[],
            total_matches=sum(1 for path_record in paths if path_record.get("exists") is True),
            offset=params.offset,
            limit=params.limit,
            truncated=False,
            model_sha256=model_sha256,
            root_node_ids=list(params.root_node_ids),
            reason=params.reason,
            requested_filters=requested_filters,
            effective_filters=effective_filters,
            paths=paths,
            limitations=[*_LIMITATIONS, "static_path_only", "guards_and_effects_not_evaluated"],
        ).model_dump(mode="json")
    items = _filter_entities(
        _items_for(inspect_data, params.query_kind),
        params.query_kind,
        name_contains=params.name_contains,
        exact=params.exact,
        path=params.path,
        within=params.within,
        source=params.source,
        event=params.event,
        target=params.target,
        parent=params.parent,
        recursive=params.recursive,
        kind=params.kind,
        name=params.name,
        scope=params.scope,
        declared=params.declared,
        used=params.used,
        variable_type=params.variable_type,
        read_in=params.read_in,
        written_in=params.written_in,
        has_event=params.has_event,
        has_guard=params.has_guard,
        has_effect=params.has_effect,
        forced=params.forced,
        self_loop=params.self_loop,
        source_within=params.source_within,
        target_within=params.target_within,
    )
    total = len(items)
    page = items[params.offset : params.offset + params.limit]
    return ModelQueryResult(
        execution_status="completed",
        query_kind=params.query_kind,
        operation=params.operation,
        matched_items=page,
        total_matches=total,
        offset=params.offset,
        limit=params.limit,
        truncated=params.offset + params.limit < total,
        model_sha256=model_sha256,
        root_node_ids=list(params.root_node_ids),
        reason=params.reason,
        requested_filters=requested_filters,
        effective_filters=effective_filters,
        limitations=list(_LIMITATIONS),
    ).model_dump(mode="json")


def build_tool(
    snapshot: dict[str, Any],
    *,
    registered_root_ids: Callable[[], set[str]] | None = None,
) -> SimpleStructuredTool:
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
    ``invalid_arguments``; missing inspect returns
    ``tool_unavailable``; no bare exception text is treated as model evidence.

    Evidence limitations: the tool exposes structure only, never a quality,
    behavior, source-closure, or repair verdict.

    Permissions: no Agent-supplied paths, model text, run/case identifiers,
    network, shell, Python/Z3, writes, or reference/gold inputs.

    Example: ``build_tool(snapshot).invoke({"query_kind":"states","offset":0,"limit":5})`` returns a paginated ``ModelQueryResult``.
    """

    frozen = copy.deepcopy(snapshot)
    completed_requests: set[tuple[Any, ...]] = set()
    fully_returned_categories: set[str] = set()
    seen_item_hashes: dict[str, set[str]] = {}

    def item_hash(item: dict[str, Any]) -> str:
        payload = json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def query_model(
        query_kind: str,
        name_contains: str | None = None,
        operation: str = "entities",
        exact: bool = False,
        path: str | None = None,
        within: str | None = None,
        parent: str | None = None,
        recursive: bool = True,
        kind: str | None = None,
        name: str | None = None,
        scope: str | None = None,
        declared: bool | None = None,
        used: bool | None = None,
        variable_type: str | None = None,
        read_in: str | None = None,
        written_in: str | None = None,
        source: str | None = None,
        event: str | None = None,
        target: str | None = None,
        has_event: bool | None = None,
        has_guard: bool | None = None,
        has_effect: bool | None = None,
        forced: bool | None = None,
        self_loop: bool | None = None,
        source_within: str | None = None,
        target_within: str | None = None,
        avoid: list[str] | None = None,
        max_hops: int | None = None,
        offset: int = 0,
        limit: int = 50,
        root_node_ids: list[str] | None = None,
        reason: str = "",
    ) -> dict[str, Any]:
        """Purpose
        -------
        Query normalized structural facts for the frozen ``STM_0`` when the
        Discover workflow has a named evidence gap, such as locating a state,
        checking an event's qualified name, inspecting a transition shape, or
        reviewing a diagnostic. This tool returns facts only; it does not create
        checks, assess propositions, or issue a quality/repair verdict.

        When to use
        -----------
        After the mandatory guide/task read phase, use it either for one targeted
        provisional clause/Root question needed to register an exact assertion,
        or after registration for one named structural gap from an inconclusive
        evaluation or coverage finding.

        When not to use
        ----------------
        Do not use this tool before reading the frozen task, enumerate the model,
        duplicate `read_task`, or use query results
        directly as a Root verdict; the final proposition must use `eval_assert`.
        Once a query answers its named gap, incorporate the result into the
        registered assertion instead of issuing adjacent inventory queries.

        Parameters
        ----------
        ``query_kind`` (required string enum): exactly one of ``states``,
        ``events``, ``transitions``, ``variables``, or ``diagnostics``.
        ``operation`` (optional enum, default ``entities``): ``entities`` returns
        paginated inspect rows, ``topology`` returns a deterministic static
        state/edge slice, and ``path`` returns a shortest declared path using the
        shared topology backend.
        ``name_contains`` (optional string or null, default null): case-insensitive
        substring matched against each item's canonical JSON; it is not a regex,
        query language, state predicate, or solver expression. ``exact`` switches
        path/source/event/target filters from legacy suffix-compatible matching to
        exact dotted-reference matching. ``path`` filters exact entity refs,
        ``within`` restricts dotted topology scope, and ``source``/``event``/
        ``target`` and the documented entity filters narrow structural rows.
        ``avoid`` and ``max_hops`` bound only the static path query; they are not
        NL timing semantics.
        ``offset`` (integer, default 0): zero-based index in the filtered result;
        must be at least 0.
        ``limit`` (integer, default 50): maximum page size; must be 1 through 500.
        ``root_node_ids`` (non-empty list of strings): exact registered Roots whose
        named evidence gap motivates this query.
        ``reason`` (non-empty string): the concrete structural question and why
        this query is needed, written in the run content language.
        The strict JSON input accepts no additional fields.

        Returns
        -------
        A ``ModelQueryResult`` JSON object:

        - ``execution_status``: ``completed``, ``invalid_arguments``, or
          ``tool_unavailable`` for this deterministic adapter.
        - ``query_kind``: normalized requested category.
        - ``matched_items``: only the requested page; each item preserves inspect
          fields and includes deterministic ``_index`` when absent.
        - ``total_matches``: filtered count before pagination for entity queries; for ``operation=path`` this counts only paths with ``exists=true`` and does not count the preserved ``exists=false`` absence sentinel.
        - ``offset`` / ``limit``: effective page arguments.
        - ``truncated``: true when another page exists after this page.
        - ``model_sha256``: frozen model identity; compare it with ``read_task``.
        - ``limitations``: machine-readable evidence-boundary/status notes.
        - ``recommended_tools`` / ``recommended_action`` / ``pass_criteria``:
          phase-aware guidance for incorporating a completed fact page or
          correcting a rejected request without repeating it.

        Execution
        ---------
        1. Validate the strict enum, filter type, offset, limit, Root IDs and
           reason. Reject an
           exact duplicate request. If an unfiltered page from offset 0 already
           returned the complete category with ``truncated=false``, reject later
           requests for that same frozen category because no new fact can appear.
        3. Read only the normalized inspect and frozen FCSTM closed over before
           dispatch.
        4. Normalize items, apply exact/path/within/source/event/target filters,
           or derive topology/path records from the shared deterministic backend,
           then count matches and slice ``[offset:offset+limit]`` deterministically.
        5. Compare returned item hashes with facts already exposed for this
           category. A query that adds no new structural fact is rejected; once
           the union covers the frozen category, mark it fully returned.
        6. Return a strict schema tied to the same frozen ``model_sha256``. No
           no alternate model lookup, simulation, BMC, LLM call, cache refresh,
           or latest-state lookup occurs.

        Failure semantics
        -----------------
        Invalid enum/type/range, an exact duplicate, a query that yields no new structural
        fact, or a query against a category already returned in full returns
        ``invalid_arguments`` with an empty page and limitation code.
        Missing/non-structural inspect category returns
        ``tool_unavailable``. An empty completed page is a valid domain result and
        does not mean the model element is impossible or erroneous. Diagnostics
        are facts and remain non-verdict evidence.

        Evidence limitations
        --------------------
        Use results to ground element refs or decide whether another bounded trace
        or source mapping is needed. A matched/missing item, diagnostic, or page
        count cannot alone confirm an issue, prove behavior, prove NL alignment,
        establish source closure, justify Repair, or prove completeness. Static
        topology/path results do not evaluate guards, effects, event availability,
        or lifecycle initialization. If ``truncated=true``, fetch the required next
        page before claiming absence.

        Permissions
        -----------
        Read-only and current-attempt only. No arbitrary paths, alternate model,
        run/case selectors, network, shell, Python/Z3, custom predicates, writes,
        future stage data, or hidden reference/gold assets.

        Examples
        --------
        Input ``{"query_kind":"states","operation":"entities","path":"Root.Idle","exact":true,"offset":0,"limit":10,"root_node_ids":["ROOT-001"],"reason":"Locate exact state refs for ROOT-001."}``
        returns ``{"execution_status":"completed","query_kind":"states","matched_items":[{"path":"Root.Idle","_index":0}],"total_matches":1,"offset":0,"limit":10,"truncated":false,"model_sha256":"...","root_node_ids":["ROOT-001"],"reason":"Locate exact state refs for ROOT-001.","limitations":[...]}``.
        """

        root_node_ids = list(root_node_ids or [])

        def finalize(result: dict[str, Any]) -> dict[str, Any]:
            completed = result.get("execution_status") == "completed"
            if completed:
                registered = (
                    registered_root_ids()
                    if registered_root_ids is not None
                    else set()
                )
                if not (set(root_node_ids) & registered):
                    recommended_tools = ["register_coverage_plan"]
                    recommended_action = (
                        "Use this targeted pre-registration fact to finish the "
                        "same provisional Root's positive assertion, then register "
                        "the complete coverage plan. Do not expand into an inventory sweep."
                    )
                    pass_criteria = (
                        "The complete plan registers the stable Root and an exact "
                        "assertion grounded by this structural result."
                    )
                else:
                    recommended_tools = ["revise_assertion", "eval_assert"]
                    recommended_action = (
                        "Incorporate these structural facts into the implicated "
                        "registered assertion and its latest evaluation. Do not "
                        "issue adjacent inventory queries when the named gap is resolved."
                    )
                    pass_criteria = (
                        "The next semantic actions revise and evaluate executable "
                        "assertion evidence for the named Root."
                    )
            else:
                recommended_tools = ["query_model", "revise_assertion", "eval_assert"]
                recommended_action = (
                    "Read the limitation code. Correct an invalid filter/page only "
                    "when the named structural gap remains; for duplicate, fully "
                    "returned, or no-new-fact results, use the facts already exposed "
                    "and revise/evaluate the registered assertion instead of retrying."
                )
                pass_criteria = (
                    "The next call either supplies a corrected query that can expose "
                    "a specifically missing fact or advances the existing evidence into a revised latest assertion."
                )
            return {
                **result,
                "root_node_ids": root_node_ids,
                "reason": reason,
                "recommended_tools": recommended_tools,
                "recommended_action": recommended_action,
                "pass_criteria": pass_criteria,
            }

        request_key = (
            query_kind,
            operation,
            json.dumps(
                {
                    "name_contains": name_contains,
                    "exact": exact,
                    "path": path,
                    "within": within,
                    "parent": parent,
                    "recursive": recursive,
                    "kind": kind,
                    "name": name,
                    "scope": scope,
                    "declared": declared,
                    "used": used,
                    "variable_type": variable_type,
                    "read_in": read_in,
                    "written_in": written_in,
                    "source": source,
                    "event": event,
                    "target": target,
                    "has_event": has_event,
                    "has_guard": has_guard,
                    "has_effect": has_effect,
                    "forced": forced,
                    "self_loop": self_loop,
                    "source_within": source_within,
                    "target_within": target_within,
                    "avoid": avoid or [],
                    "max_hops": max_hops,
                    "offset": offset,
                    "limit": limit,
                },
                sort_keys=True,
            ),
        )
        if request_key in completed_requests:
            return finalize(ModelQueryResult(
                execution_status="invalid_arguments",
                query_kind=query_kind,  # type: ignore[arg-type]
                matched_items=[],
                total_matches=0,
                offset=max(0, offset),
                limit=limit if isinstance(limit, int) and 1 <= limit <= 500 else 50,
                truncated=False,
                model_sha256=_model_sha256_from(frozen),
                limitations=[*_LIMITATIONS, "duplicate_query_not_executed"],
            ).model_dump(mode="json"))
        if operation == "entities" and query_kind in fully_returned_categories:
            return finalize(ModelQueryResult(
                execution_status="invalid_arguments",
                query_kind=query_kind,  # type: ignore[arg-type]
                matched_items=[],
                total_matches=0,
                offset=max(0, offset),
                limit=limit if isinstance(limit, int) and 1 <= limit <= 500 else 50,
                truncated=False,
                model_sha256=_model_sha256_from(frozen),
                limitations=[
                    *_LIMITATIONS,
                    "category_already_returned_untruncated",
                ],
            ).model_dump(mode="json"))
        result = execute(
            frozen,
            query_kind,
            name_contains,
            offset,
            limit,
            operation=operation,
            exact=exact,
            path=path,
            within=within,
            parent=parent,
            recursive=recursive,
            kind=kind,
            name=name,
            scope=scope,
            declared=declared,
            used=used,
            variable_type=variable_type,
            read_in=read_in,
            written_in=written_in,
            source=source,
            event=event,
            target=target,
            has_event=has_event,
            has_guard=has_guard,
            has_effect=has_effect,
            forced=forced,
            self_loop=self_loop,
            source_within=source_within,
            target_within=target_within,
            avoid=avoid,
            max_hops=max_hops,
            reason=reason,
            root_node_ids=root_node_ids,
        )
        if result.get("execution_status") == "completed":
            completed_requests.add(request_key)
            if operation != "entities":
                return finalize(result)
            page_hashes = {
                item_hash(item)
                for item in result.get("matched_items", [])
                if isinstance(item, dict)
            }
            previously_seen = seen_item_hashes.setdefault(query_kind, set())
            new_hashes = page_hashes - previously_seen
            if not new_hashes and previously_seen:
                return finalize(ModelQueryResult(
                    execution_status="invalid_arguments",
                    query_kind=query_kind,  # type: ignore[arg-type]
                    matched_items=[],
                    total_matches=0,
                    offset=offset,
                    limit=limit,
                    truncated=False,
                    model_sha256=_model_sha256_from(frozen),
                    limitations=[*_LIMITATIONS, "no_new_structural_fact"],
                ).model_dump(mode="json"))
            previously_seen.update(new_hashes)
            category_size = len(_items_for(_inspect_from(frozen), query_kind))
            entity_filters = {
                "name_contains": name_contains,
                "path": path,
                "within": within,
                "parent": parent,
                "kind": kind,
                "name": name,
                "scope": scope,
                "declared": declared,
                "used": used,
                "variable_type": variable_type,
                "read_in": read_in,
                "written_in": written_in,
                "source": source,
                "event": event,
                "target": target,
                "has_event": has_event,
                "has_guard": has_guard,
                "has_effect": has_effect,
                "forced": forced,
                "self_loop": self_loop,
                "source_within": source_within,
                "target_within": target_within,
            }
            unfiltered_complete_page = (
                not any(value is not None for value in entity_filters.values())
                and offset == 0
                and result.get("truncated") is False
            )
            if unfiltered_complete_page or len(previously_seen) >= category_size:
                fully_returned_categories.add(query_kind)
        return finalize(result)

    return SimpleStructuredTool(func=query_model, name="query_model", description=query_model.__doc__ or "query_model", args_schema=QueryModelInput)
