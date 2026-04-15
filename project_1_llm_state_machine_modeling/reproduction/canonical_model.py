from __future__ import annotations

from typing import Any


def _normalize_state(state: dict[str, Any], *, block_name: str | None = None) -> dict[str, Any]:
    return {
        "name": str(state.get("name", "")).strip(),
        "parent": (str(state.get("parent")).strip() if state.get("parent") else None),
        "parallel_group": (
            str(state.get("parallel_group")).strip() if state.get("parallel_group") else None
        ),
        "is_history": bool(state.get("is_history", False)),
        "is_initial": bool(state.get("is_initial", False)),
        "block": block_name or state.get("block"),
    }


def _normalize_transition(
    transition: dict[str, Any], *, block_name: str | None = None
) -> dict[str, Any]:
    return {
        "source": str(transition.get("source", "")).strip(),
        "target": str(transition.get("target", "")).strip(),
        "event": str(transition.get("event", "")).strip(),
        "guard": str(transition.get("guard", "")).strip(),
        "action": str(transition.get("action", "")).strip(),
        "block": block_name or transition.get("block"),
    }


def normalize_machine(payload: dict[str, Any]) -> dict[str, Any]:
    result = {
        "machine_name": str(payload.get("machine_name", "")).strip(),
        "states": [],
        "transitions": [],
        "parallel_regions": [],
        "blocks": [],
    }
    for state in payload.get("states", []) or []:
        if isinstance(state, dict):
            result["states"].append(_normalize_state(state))
    for transition in payload.get("transitions", []) or []:
        if isinstance(transition, dict):
            result["transitions"].append(_normalize_transition(transition))
    for region in payload.get("parallel_regions", []) or []:
        if isinstance(region, dict):
            result["parallel_regions"].append(
                {
                    "parent": str(region.get("parent", "")).strip(),
                    "region": str(region.get("region", "")).strip(),
                    "states": [str(value).strip() for value in (region.get("states") or []) if value],
                }
            )
    for block in payload.get("blocks", []) or []:
        if not isinstance(block, dict):
            continue
        block_name = str(block.get("name", "")).strip()
        normalized_block = {
            "name": block_name,
            "attributes": block.get("attributes", []) or [],
            "signals": block.get("signals", []) or [],
            "states": [],
            "transitions": [],
        }
        for state in block.get("states", []) or []:
            if isinstance(state, dict):
                normalized_state = _normalize_state(state, block_name=block_name)
                normalized_block["states"].append(normalized_state)
                result["states"].append(normalized_state)
        for transition in block.get("transitions", []) or []:
            if isinstance(transition, dict):
                normalized_transition = _normalize_transition(transition, block_name=block_name)
                normalized_block["transitions"].append(normalized_transition)
                result["transitions"].append(normalized_transition)
        result["blocks"].append(normalized_block)
    return result


def count_machine_components(payload: dict[str, Any]) -> dict[str, int]:
    machine = normalize_machine(payload)
    state_count = sum(1 for state in machine["states"] if state["name"])
    transition_count = sum(
        1 for transition in machine["transitions"] if transition["source"] and transition["target"]
    )
    guard_count = sum(1 for transition in machine["transitions"] if transition["guard"])
    action_count = sum(1 for transition in machine["transitions"] if transition["action"])
    hierarchical_state_count = sum(1 for state in machine["states"] if state["parent"])
    history_state_count = sum(1 for state in machine["states"] if state["is_history"])
    parallel_region_count = len(machine["parallel_regions"])
    if parallel_region_count == 0:
        parallel_region_count = len(
            {
                (state["parent"], state["parallel_group"])
                for state in machine["states"]
                if state["parallel_group"]
            }
        )
    state_machine_panel_count = sum(
        1 for block in machine["blocks"] if block["states"] or block["transitions"]
    )
    return {
        "state_count": state_count,
        "transition_count": transition_count,
        "guard_count": guard_count,
        "action_count": action_count,
        "hierarchical_state_count": hierarchical_state_count,
        "history_state_count": history_state_count,
        "parallel_region_count": parallel_region_count,
        "state_machine_panel_count": state_machine_panel_count,
    }
