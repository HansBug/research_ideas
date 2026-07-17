from __future__ import annotations

import re
from typing import Any, Iterable

from .records import sha256_json
from .schemas import CheckDraftSubmission, DiscoverCheckDraft, IssueCheck


def _normal(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def _event_tokens(value: str) -> set[str]:
    aliases = {
        "auto": "autonomous",
        "final": "exit",
        "greater": "",
        "less": "",
        "than": "",
    }
    ignored = {"gt", "lt", "gte", "lte", "ge", "le", "eq", "ne", "or", "event"}
    tokens: set[str] = set()
    for token in re.findall(r"[a-z0-9]+", value.lower()):
        token = aliases.get(token, token)
        if token and token not in ignored:
            tokens.add(token)
    return tokens


def _best_match(
    label: str,
    candidates: Iterable[tuple[str, str]],
    *,
    event_semantics: bool = False,
) -> str | None:
    wanted = _normal(label)
    if not wanted:
        return None
    ranked: list[tuple[int, str]] = []
    wanted_tokens = _event_tokens(label) if event_semantics else set()
    for identifier, visible in candidates:
        forms = {_normal(identifier), _normal(identifier.rsplit(".", 1)[-1]), _normal(visible)}
        if wanted in forms:
            ranked.append((0, identifier))
        elif any(wanted in form or form in wanted for form in forms if form):
            ranked.append((1, identifier))
        elif wanted_tokens:
            candidate_tokens = _event_tokens(identifier.rsplit(".", 1)[-1]) | _event_tokens(visible)
            if wanted_tokens == candidate_tokens:
                ranked.append((2, identifier))
            elif wanted_tokens.issubset(candidate_tokens) or candidate_tokens.issubset(wanted_tokens):
                ranked.append((3, identifier))
    if not ranked:
        return None
    best_rank = min(rank for rank, _identifier in ranked)
    best_matches = sorted({identifier for rank, identifier in ranked if rank == best_rank})
    return best_matches[0] if len(best_matches) == 1 else None


def _bind_drafts(
    nl_drafts: CheckDraftSubmission,
    source_drafts: CheckDraftSubmission,
    inspect: dict[str, Any],
    *,
    binding_rejections: list[dict[str, Any]] | None = None,
) -> list[IssueCheck]:
    states = [(item["path"], item.get("name", item["path"])) for item in inspect.get("states", []) if item.get("path")]
    events = [(item["qualified_name"], item["qualified_name"].rsplit(".", 1)[-1]) for item in inspect.get("events", []) if item.get("qualified_name")]
    transitions = list(inspect.get("transitions", []))
    state_items = [item for item in inspect.get("states", []) if isinstance(item, dict) and item.get("path")]
    state_by_path = {str(item["path"]): item for item in state_items}
    forced_transitions = [item for item in inspect.get("forced_transitions", []) if isinstance(item, dict)]
    output: list[IssueCheck] = []
    grouped = (("nl_grounded_behavioral_issue", nl_drafts.checks), ("raw_internal_inconsistency", source_drafts.checks))
    for origin, drafts in grouped:
        for index, draft in enumerate(drafts, start=1):
            spec = dict(draft.executable_spec)
            if origin == "raw_internal_inconsistency":
                consistency_status = draft.expected_outcome.get("consistency_status")
                if len(draft.source_basis) < 2 or consistency_status != "contradicts" or draft.nl_basis:
                    if binding_rejections is not None:
                        binding_rejections.append(
                            {
                                "draft_origin": "raw_internal_inconsistency",
                                "draft_check_id": draft.check_id,
                                "reason": "source_internal_conflict_contract_unsatisfied",
                                "required_source_basis_min": 2,
                                "observed_source_basis_count": len(draft.source_basis),
                                "required_consistency_status": "contradicts",
                                "observed_consistency_status": consistency_status,
                            }
                        )
                    continue
            refs: list[str] = []
            if draft.check_kind == "scenario":
                labels = spec.pop("event_labels", None) or spec.get("events") or ([spec["event"]] if spec.get("event") else [])
                precondition_label = spec.pop("precondition_state_label", None)
                precondition_state = (
                    _best_match(str(precondition_label), states)
                    if isinstance(precondition_label, str) and precondition_label
                    else None
                )
                bound_events = [_best_match(str(label), events, event_semantics=True) for label in labels]
                missing_labels = [str(label) for label, bound in zip(labels, bound_events) if bound is None]
                bound_events = [item for item in bound_events if item is not None]
                spec = {
                    "events": bound_events,
                    "setup_events": bound_events[:-1],
                    "tested_event": bound_events[-1] if bound_events else None,
                    "requested_event_labels": [str(label) for label in labels],
                    "unbound_event_labels": missing_labels,
                    "precondition_state": precondition_state,
                    "requested_precondition_state_label": precondition_label,
                    "unbound_precondition_state_label": (
                        precondition_label if precondition_state is None else None
                    ),
                }
                refs = [f"event:{item}" for item in bound_events]
                if precondition_state is not None:
                    refs.append(f"state:{precondition_state}")
            elif draft.check_kind == "property":
                target_label = str(spec.pop("target_label", ""))
                state = _best_match(target_label, states)
                kind = str(spec.get("kind") or "reach")
                temporal_kinds = {
                    "reach",
                    "cover",
                    "exists_always",
                    "forbid",
                    "invariant",
                    "must_reach",
                }
                bound = 0
                if kind in temporal_kinds:
                    raw_bound = spec.get("bound", 3)
                    if (
                        isinstance(raw_bound, bool)
                        or not isinstance(raw_bound, int)
                        or raw_bound <= 0
                    ):
                        if binding_rejections is not None:
                            binding_rejections.append(
                                {
                                    "draft_origin": origin,
                                    "draft_check_id": draft.check_id,
                                    "reason": "property_bound_must_be_positive_integer",
                                    "observed_type": type(raw_bound).__name__,
                                }
                            )
                        continue
                    bound = raw_bound
                if state:
                    if kind in temporal_kinds:
                        predicate = f'active("{state}")'
                        spec = {"query": f"check {kind} <= {bound}: {predicate};", "kind": kind, "bound": bound}
                    elif kind == "has_substates":
                        spec = {"kind": "state_shape", "state": state, "expect": {"is_composite": True, "substates_min": 1}}
                    elif kind == "simple_state":
                        spec = {"kind": "state_shape", "state": state, "expect": {"is_leaf": True, "is_composite": False}}
                    refs = [f"state:{state}"]
            else:
                static_kind = spec.get("kind")
                if static_kind == "transition_shape":
                    source = _best_match(str(spec.get("source_label", "")), states)
                    target = _best_match(str(spec.get("target_label", "")), states)
                    event = _best_match(str(spec.get("event_label", "")), events, event_semantics=True) if spec.get("event_label") else None
                    target_candidates = {target} if target else set()
                    if target and target in state_by_path:
                        target_candidates.update(
                            str(item["target"])
                            for item in state_by_path[target].get("initial_targets", [])
                            if isinstance(item, dict) and item.get("target")
                        )
                    transition = next(
                        (
                            item
                            for item in transitions
                            if (source is None or item.get("from_path") == source)
                            and (not target_candidates or item.get("to_path") in target_candidates)
                            and (event is None or item.get("event") == event)
                        ),
                        None,
                    )
                    if transition is not None:
                        expected = {"from_path": transition.get("from_path"), "to_path": transition.get("to_path"), "event": transition.get("event")}
                        spec = {"kind": "transition_shape", "transition_index": transition["transition_index"], "expect": expected}
                        refs = [f"transition:{transition['transition_index']}"]
                    else:
                        forced = next(
                            (
                                item
                                for item in forced_transitions
                                if (source is None or item.get("state_path") == source)
                                and (not target_candidates or item.get("to_path") in target_candidates)
                                and (event is None or item.get("event") == event)
                            ),
                            None,
                        )
                        if forced is not None:
                            expected = {
                                "state_path": forced.get("state_path"),
                                "to_path": forced.get("to_path"),
                                "event": forced.get("event"),
                                "original_raw": forced.get("original_raw"),
                            }
                            spec = {"kind": "forced_transition_shape", "expect": expected}
                            refs = [f"forced_transition:{forced.get('original_raw')}"]
                elif static_kind == "state_declaration":
                    state = _best_match(str(spec.get("state_label", "")), states)
                    if state is not None:
                        expected = {"is_composite": spec.get("state_kind") == "composite"}
                        spec = {"kind": "state_shape", "state_path": state, "expect": expected}
                        refs = [f"state:{state}"]
                elif static_kind == "label_reuse":
                    label = _normal(str(spec.get("state_label", "")))
                    matching = [item for item in state_items if _normal(str(item.get("name") or item["path"].rsplit(".", 1)[-1])) == label]
                    if matching:
                        state_paths = [str(item["path"]) for item in matching]
                        spec = {
                            "kind": "state_label_scopes",
                            "state_paths": state_paths,
                            "expected_scope_labels": [str(item) for item in spec.get("scopes", [])],
                        }
                        refs = [f"state:{path}" for path in state_paths]
            check_id = f"CHK-{'NL' if origin.startswith('nl_') else 'SRC'}-{index:03d}"
            expected = dict(draft.expected_outcome)
            if draft.check_kind == "scenario" and isinstance(expected.get("target_label"), str):
                state = _best_match(expected["target_label"], states)
                if state is not None:
                    expected = {
                        "state_in": state,
                        "consumed_events": list(spec.get("events", [])),
                        "unconsumed_events": [],
                    }
                    target_ref = f"state:{state}"
                    if target_ref not in refs:
                        refs.append(target_ref)
            elif draft.check_kind == "property" and "property_satisfied" not in expected and isinstance(expected.get("satisfied"), bool):
                expected = {"property_satisfied": expected["satisfied"]}
            output.append(
                IssueCheck(
                    check_id=check_id,
                    check_origin=origin,
                    check_kind=draft.check_kind,
                    statement=draft.statement,
                    expected_outcome=expected,
                    basis_hashes={
                        "nl_basis": sha256_json(draft.nl_basis),
                        "source_basis": sha256_json(draft.source_basis),
                        "expected_outcome": sha256_json(expected),
                    },
                    source_basis=draft.source_basis,
                    nl_basis=draft.nl_basis,
                    executable_spec=spec,
                    binding_refs=refs,
                    required=draft.required,
                )
            )
    return output


def bind_discover_drafts(
    drafts: list[DiscoverCheckDraft],
    inspect: dict[str, Any],
    *,
    binding_rejections: list[dict[str, Any]] | None = None,
) -> list[IssueCheck]:
    """Bind one single-Agent Discover draft batch to normalized FCSTM facts.

    This function is deterministic and contains no provider call. Drafts are
    partitioned by ``check_origin`` only to reuse the established NL/source
    binding rules; their order within each origin is preserved. Any source draft
    that does not establish a source-internal contradiction is recorded in
    ``binding_rejections`` and omitted from the executable check set.
    """

    nl_checks = []
    source_checks = []
    for draft in drafts:
        payload = draft.model_dump(mode="json", exclude={"check_origin"})
        if draft.check_origin == "nl_grounded_behavioral_issue":
            nl_checks.append(payload)
        else:
            source_checks.append(payload)
    return _bind_drafts(
        CheckDraftSubmission.model_validate({"checks": nl_checks}),
        CheckDraftSubmission.model_validate({"checks": source_checks}),
        inspect,
        binding_rejections=binding_rejections,
    )
