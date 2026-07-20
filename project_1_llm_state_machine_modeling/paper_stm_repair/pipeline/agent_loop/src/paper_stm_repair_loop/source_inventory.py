from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Any


INVENTORY_VERSION = "paper1.source_inventory.v1"
PYFCSTM_PRODUCER = "pyfcstm.inspect"
SOURCE_TRACE_PRODUCER = "paper1.source_trace_base"
CONTROLLER_PRODUCER = "paper1.controller"
BEHAVIOR_RELEVANT_KINDS = frozenset(
    {
        "state",
        "event",
        "variable",
        "transition",
        "forced_transition",
        "guard",
        "effect",
        "initial_relation",
        "hierarchy",
        "region",
    }
)


def build_source_inventory(
    check_fcstm_result: dict[str, Any],
    *,
    source_trace_base: dict[str, Any] | None = None,
    relation_policy: str | None = None,
    identity_refs: list[dict[str, Any]] | None = None,
    producer_version: str | None = None,
) -> dict[str, Any]:
    inspect = _resolve_inspect(check_fcstm_result)
    counters: dict[str, int] = defaultdict(int)
    facts: list[dict[str, Any]] = []

    for state in _items(inspect, "states"):
        ref = _first(state, "path", "qualified_name", "name", default="unknown")
        facts.append(_fact(counters, "state", f"state:{ref}", producer_version, "pyfcstm_public_structured_inspect", payload=state))
        parent = _first(state, "parent_path", "parent")
        if parent:
            facts.append(
                _fact(
                    counters,
                    "hierarchy",
                    f"hierarchy:{parent}->{ref}",
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    source=parent,
                    target=ref,
                    payload={"parent": parent, "child": ref},
                )
            )
        for initial in state.get("initial_targets", []) or []:
            if not isinstance(initial, dict):
                continue
            target = _first(initial, "target", "to_path")
            facts.append(
                _fact(
                    counters,
                    "initial_relation",
                    f"initial_relation:{ref}->{target}",
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    source=ref,
                    event=_first(initial, "event"),
                    target=target,
                    guard=_first(initial, "guard"),
                    payload={"owner": ref, **_without_semantic_role(initial)},
                )
            )
        for region in state.get("regions", []) or []:
            region_payload = _dict_item(region)
            facts.append(
                _fact(
                    counters,
                    "region",
                    f"region:{ref}:{_support_ref('region', region_payload).split(':', 1)[-1]}",
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    source=ref,
                    payload={"owner": ref, **region_payload},
                )
            )

    for event in _items(inspect, "events"):
        ref = _first(event, "qualified_name", "path", "name", default="unknown")
        facts.append(_fact(counters, "event", f"event:{ref}", producer_version, "pyfcstm_public_structured_inspect", payload=event))

    for variable in _items(inspect, "variables"):
        ref = _first(variable, "qualified_name", "path", "name", default="unknown")
        facts.append(_fact(counters, "variable", f"variable:{ref}", producer_version, "pyfcstm_public_structured_inspect", payload=variable))

    for transition in _items(inspect, "transitions"):
        fact_kind = "forced_transition" if bool(_first(transition, "is_forced", "forced", default=False)) else "transition"
        source = _first(transition, "from_path", "source", "from", "source_state")
        event = _first(transition, "event", "trigger", "event_name")
        target = _first(transition, "to_path", "target", "to", "target_state")
        transition_ref = _transition_ref(transition, source, event, target)
        guard = _first(transition, "guard", "condition")
        effects = _effects(transition)
        facts.append(
            _fact(
                counters,
                fact_kind,
                transition_ref,
                producer_version,
                "pyfcstm_public_structured_inspect",
                source=source,
                event=event,
                target=target,
                guard=guard,
                effects=effects,
                payload=transition,
            )
        )
        if guard:
            facts.append(
                _fact(
                    counters,
                    "guard",
                    f"guard:{transition_ref}",
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    source=source,
                    event=event,
                    target=target,
                    guard=str(guard),
                    payload={"transition_ref": transition_ref, "guard": guard},
                )
            )
        for effect in effects:
            facts.append(
                _fact(
                    counters,
                    "effect",
                    f"effect:{transition_ref}:{sha256_text(effect)[:12]}",
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    source=source,
                    event=event,
                    target=target,
                    effects=[effect],
                    payload={"transition_ref": transition_ref, "effect": effect},
                )
            )

    for key, kind in [
        ("initial_relations", "initial_relation"),
        ("initial", "initial_relation"),
        ("hierarchy", "hierarchy"),
        ("regions", "region"),
        ("diagnostics", "diagnostic"),
        ("unsupported_markers", "unsupported_marker"),
    ]:
        for item in _items(inspect, key):
            facts.append(
                _fact(
                    counters,
                    kind,
                    _support_ref(kind, item),
                    producer_version,
                    "pyfcstm_public_structured_inspect",
                    payload=item,
                )
            )

    for diagnostic in check_fcstm_result.get("diagnostics", []) or []:
        facts.append(
            _fact(
                counters,
                "diagnostic",
                _support_ref("diagnostic", diagnostic),
                producer_version,
                "pyfcstm_public_structured_inspect",
                payload=diagnostic,
            )
        )

    if source_trace_base:
        for entry in source_trace_base.get("entries", []) or []:
            facts.append(
                _fact(
                    counters,
                    "source_fcstm_mapping",
                    _support_ref("source_fcstm_mapping", entry),
                    None,
                    "paper1_input_bridge_source_trace_base",
                    producer=SOURCE_TRACE_PRODUCER,
                    payload=_without_semantic_role(entry),
                )
            )

    if relation_policy == "exact_identity":
        for entry in identity_refs or []:
            facts.append(
                _fact(
                    counters,
                    "source_fcstm_mapping",
                    _support_ref("source_fcstm_mapping", entry),
                    INVENTORY_VERSION,
                    "controller_synthetic_exact_identity_relation",
                    producer=CONTROLLER_PRODUCER,
                    payload=_without_semantic_role(entry),
                )
            )

    facts = _deduplicate_facts(facts)
    return {
        "schema_version": INVENTORY_VERSION,
        "inventory_sha256": sha256_text(
            json.dumps(facts, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        ),
        "facts": facts,
    }


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _resolve_inspect(result: dict[str, Any]) -> dict[str, Any]:
    if "inspect" in result and isinstance(result["inspect"], dict):
        return result["inspect"]
    model = result.get("model")
    if isinstance(model, dict) and isinstance(model.get("normalized_inspect"), dict):
        return model["normalized_inspect"]
    return result


def _items(mapping: dict[str, Any], key: str) -> list[dict[str, Any]]:
    value = mapping.get(key)
    if value is None:
        return []
    if isinstance(value, list):
        return [_dict_item(item) for item in value]
    if isinstance(value, dict):
        return [_dict_item(item) for item in value.values()]
    return []


def _dict_item(item: Any) -> dict[str, Any]:
    if isinstance(item, dict):
        return _without_semantic_role(item)
    return {"value": item}


def _without_semantic_role(mapping: dict[str, Any]) -> dict[str, Any]:
    return {str(key): value for key, value in mapping.items() if str(key) != "semantic_role"}


def _first(mapping: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def _effects(transition: dict[str, Any]) -> list[str]:
    effects = _first(transition, "effects", "effect", "actions", default=[])
    if effects is None:
        return []
    if isinstance(effects, list):
        return [str(effect) for effect in effects]
    return [str(effects)]


def _transition_ref(transition: dict[str, Any], source: Any, event: Any, target: Any) -> str:
    index = _first(transition, "transition_index", "index", "id")
    if index is not None:
        return f"transition:{index}"
    parts = [str(part) for part in (source, event, target) if part is not None]
    return "transition:" + ":".join(parts) if parts else "transition:unknown"


def _support_ref(kind: str, item: dict[str, Any]) -> str:
    for key in ("qualified_name", "path", "code", "id", "name"):
        if key in item:
            return f"{kind}:{item[key]}"
    return f"{kind}:{sha256_text(repr(item))[:12]}"


def _fact(
    counters: dict[str, int],
    fact_kind: str,
    qualified_ref: str,
    producer_version: str | None,
    provenance: str,
    *,
    producer: str = PYFCSTM_PRODUCER,
    source: Any = None,
    event: Any = None,
    target: Any = None,
    guard: Any = None,
    effects: list[str] | None = None,
    payload: dict[str, Any] | None = None,
) -> dict[str, Any]:
    counters[fact_kind] += 1
    clean_payload = _without_semantic_role(payload or {})
    return {
        "fact_id": f"FACT-{fact_kind.upper().replace('_', '-')}-{counters[fact_kind]:03d}",
        "fact_kind": fact_kind,
        "qualified_refs": [qualified_ref],
        "producer": producer,
        "producer_version": producer_version,
        "provenance": provenance,
        "behavior_relevant": fact_kind in BEHAVIOR_RELEVANT_KINDS,
        "source": None if source is None else str(source),
        "event": None if event is None else str(event),
        "target": None if target is None else str(target),
        "guard": None if guard is None else str(guard),
        "effects": effects or [],
        "payload": clean_payload,
    }


def _deduplicate_facts(facts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep one stable fact for duplicate inspect/top-level diagnostic payloads."""

    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    for fact in facts:
        identity = json.dumps(
            {
                key: value
                for key, value in fact.items()
                if key != "fact_id"
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        if identity in seen:
            continue
        seen.add(identity)
        result.append(fact)
    counters: dict[str, int] = defaultdict(int)
    for fact in result:
        kind = str(fact["fact_kind"])
        counters[kind] += 1
        fact["fact_id"] = f"FACT-{kind.upper().replace('_', '-')}-{counters[kind]:03d}"
    return result
