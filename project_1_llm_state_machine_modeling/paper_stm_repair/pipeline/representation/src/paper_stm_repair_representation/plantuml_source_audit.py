from __future__ import annotations

import re
from collections import Counter
from typing import Any


_TRANSITION_RE = re.compile(
    r"^(?P<forced>!\s*)?(?P<source>\*|\[\*\]|[A-Za-z_][A-Za-z0-9_]*)\s*"
    r"->\s*(?P<target>\[\*\]|[A-Za-z_][A-Za-z0-9_]*)"
    r"(?:\s*:\s*/(?P<event>[A-Za-z_][A-Za-z0-9_]*))?;$"
)
_OFFICIAL_SYNTHETIC_SCOPE_RE = re.compile(r"^(?:CONC\d+|__stm_wrapper_\d+)$")


def _official_identity(value: str | None) -> str:
    if not value:
        return ""
    return ".".join(
        segment
        for segment in value.split(".")
        if segment and not _OFFICIAL_SYNTHETIC_SCOPE_RE.fullmatch(segment)
    )


def _official_endpoint(link: dict[str, Any], side: str) -> str:
    qualified = link[side]
    kind = link[f"{side}_kind"]
    if "CIRCLE_START" in kind or "CIRCLE_END" in kind:
        parent = qualified.rsplit(".", 1)[0] if "." in qualified else ""
        boundary = "initial" if "CIRCLE_START" in kind else "final"
        return f"@{boundary}:{_official_identity(parent) or '__root__'}"
    return _official_identity(qualified)


def _is_behavior_endpoint(kind: str) -> bool:
    return (
        kind.startswith("GROUP:")
        or "STATE" in kind
        or "CIRCLE_START" in kind
        or "CIRCLE_END" in kind
    )


def _assert_official_identity_projection(canonical: dict[str, Any]) -> None:
    metadata = canonical.get("metadata", {})
    reconciliation = metadata.get("official_identity_reconciliation", {})
    if reconciliation.get("status") != "aligned":
        raise ValueError("canonical is missing aligned official identity evidence")
    official = metadata["official_validation"]["model"]
    if official.get("status") != "state_diagram":
        raise ValueError("official identity oracle is not a StateDiagram")

    official_state_ids = {
        _official_identity(entity["qualified_name"])
        for entity in official["entities"]
        if entity.get("qualified_name")
        and _is_behavior_endpoint(entity["kind"])
        and "CIRCLE_START" not in entity["kind"]
        and "CIRCLE_END" not in entity["kind"]
        and not _OFFICIAL_SYNTHETIC_SCOPE_RE.fullmatch(
            entity["qualified_name"].rsplit(".", 1)[-1]
        )
    }
    official_state_ids.discard("")
    canonical_state_ids = {state["id"] for state in canonical["model"]["states"]}
    if canonical_state_ids != official_state_ids:
        raise ValueError(
            "canonical state identities differ from pinned PlantUML: "
            f"source_only={sorted(canonical_state_ids - official_state_ids)}, "
            f"official_only={sorted(official_state_ids - canonical_state_ids)}"
        )

    links = [
        link
        for link in official["links"]
        if _is_behavior_endpoint(link["source_kind"])
        and _is_behavior_endpoint(link["target_kind"])
    ]
    transitions = canonical["model"]["transitions"]
    if len(links) != len(transitions):
        raise ValueError("canonical/official behavior-link count differs")
    for transition, link in zip(transitions, links):
        raw_arrow = transition["attributes"]["raw_arrow"].lower()
        reverse = "left" in raw_arrow or "up" in raw_arrow
        source_side = "target" if reverse else "source"
        target_side = "source" if reverse else "target"
        expected = (
            _official_endpoint(link, source_side),
            _official_endpoint(link, target_side),
        )
        actual = (transition["source"], transition["target"])
        if actual != expected:
            raise ValueError(
                f"official endpoint identity drift for {transition['id']}: "
                f"{actual} != {expected}"
            )
    if reconciliation.get("official_state_count") != len(official_state_ids):
        raise ValueError("official state reconciliation count drift")
    if reconciliation.get("transition_identity_alignment_count") != len(links):
        raise ValueError("official transition reconciliation count drift")


def _state_lookup(model: Any) -> dict[str, Any]:
    return {".".join(state.path): state for state in model.root_state.walk_states()}


def _scope_paths(comparison: dict[str, Any], root_path: str) -> dict[str, str]:
    paths = {"__root__": root_path}
    paths.update(
        {
            mapping["state_id"]: mapping["fcstm_path"]
            for mapping in comparison["state_mappings"]
        }
    )
    return paths


def _endpoint_path(scope_path: str, endpoint: str) -> str:
    if endpoint == "[*]":
        return endpoint
    return f"{scope_path}.{endpoint}"


def _normalize_forced_origin(value: str) -> str:
    return re.sub(r"^!\s*", "!", value.strip())


def _source_chain(state_id: str, parents: dict[str, str | None]) -> list[str]:
    chain = [state_id]
    current = parents[state_id]
    while current is not None:
        chain.append(current)
        current = parents[current]
    return list(reversed(chain))


def _parsed_segments(mapping: dict[str, Any]) -> list[tuple[dict[str, Any], re.Match[str]]]:
    parsed: list[tuple[dict[str, Any], re.Match[str]]] = []
    for emitted in mapping["emitted"]:
        match = _TRANSITION_RE.fullmatch(emitted["line"])
        if match is None:
            raise ValueError(f"unrecognized emitted FCSTM transition syntax: {emitted['line']}")
        parsed.append((emitted, match))
    return parsed


def _concurrent_display_lines(
    canonical: dict[str, Any], scope: str | None
) -> list[str]:
    regions = sorted(
        [
            item
            for item in canonical["model"].get("concurrent_regions", [])
            if item.get("owner_scope") == scope
        ],
        key=lambda item: item["region_index"],
    )
    separators = [
        item
        for item in canonical.get("metadata", {}).get(
            "concurrent_region_separators", []
        )
        if item.get("owner_scope") == scope
    ]
    lines = []
    for region in regions:
        states = ", ".join(region.get("state_ids", [])) or "-"
        transitions = ", ".join(region.get("transition_ids", [])) or "-"
        lines.append(
            f"[PlantUML concurrent region {region['region_index']}] "
            f"states={states}; transitions={transitions}"
        )
    for separator in separators:
        lines.append(
            "[PlantUML concurrent separator] "
            f"region {separator['preceding_region_index']} -> "
            f"{separator['following_region_index']} at {separator['raw_ref']}"
        )
    return lines


def _state_display(canonical: dict[str, Any], state: dict[str, Any]) -> str:
    value = state.get("label") or state["id"]
    for body in state["attributes"].get("body_lines", []):
        value += f"\n[PlantUML body] {body.get('text') or ''}"
    for line in _concurrent_display_lines(canonical, state["id"]):
        value += f"\n{line}"
    return value


def _root_display(canonical: dict[str, Any]) -> str:
    value = canonical["model"].get("name") or canonical["example_id"]
    for item in canonical.get("metadata", {}).get("orphan_lifecycle_actions", []):
        value += (
            f"\n[Unowned PlantUML {item.get('kind', 'lifecycle')}] "
            f"{item.get('text') or ''}"
        )
    for line in _concurrent_display_lines(canonical, None):
        value += f"\n{line}"
    for change in canonical.get("metadata", {}).get("source_normalizations", []):
        value += (
            f"\n[PlantUML source normalization {change['rule_id']}] "
            f"{change['raw_ref']}: {change['before']} -> {change['after']}"
        )
    return value


def _assert_source_projection(
    *,
    mapping: dict[str, Any],
    transition: dict[str, Any],
    state_ids: dict[str, str],
    parents: dict[str, str | None],
    synthetic_states: list[dict[str, Any]],
    event_ids: dict[str, str],
    state_is_composite: dict[str, bool],
) -> None:
    segments = _parsed_segments(mapping)
    expected_event = (
        event_ids[transition["event"]] if transition.get("event") else None
    )
    for _, match in segments:
        if match.group("event") != expected_event:
            raise ValueError(f"transition event projection drift: {transition['id']}")
    by_role: dict[str, list[tuple[dict[str, Any], re.Match[str]]]] = {}
    for emitted, match in segments:
        by_role.setdefault(emitted["generated_role"], []).append((emitted, match))
    reason = mapping["reason_code"]

    if reason == "R45.MAP.invalid_source_initial_surrogate":
        linked = [
            state
            for state in synthetic_states
            if state.get("source_transition_id") == transition["id"]
            and state["generated_reason"] == "invalid_source_initial_target_surrogate"
        ]
        if len(linked) != 1 or transition["target"] not in linked[0]["display_name"]:
            raise ValueError(f"invalid initial surrogate lost target identity: {transition['id']}")
        return

    if reason == "R45.MAP.invalid_source_final_surrogate":
        linked = [
            state
            for state in synthetic_states
            if state.get("source_transition_id") == transition["id"]
            and state["generated_reason"] == "invalid_source_final_scope_surrogate"
        ]
        projected = by_role.get("invalid_source_final_surrogate", [])
        expected_scope = parents[transition["source"]] or "__root__"
        if (
            len(linked) != 1
            or transition["target"] not in linked[0]["display_name"]
            or len(projected) != 1
        ):
            raise ValueError(f"invalid final surrogate lost target identity: {transition['id']}")
        emitted, match = projected[0]
        if (
            emitted["scope"] != expected_scope
            or match.group("source") != state_ids[transition["source"]]
            or match.group("target") != linked[0]["fcstm_id"]
            or bool(match.group("forced"))
            != state_is_composite[transition["source"]]
        ):
            raise ValueError(f"invalid final surrogate endpoint drift: {transition['id']}")
        return

    if reason == "R45.MAP.direct_sibling":
        direct = by_role.get("source_direct_transition", [])
        expected_scope = parents[transition["source"]] or "__root__"
        if len(direct) != 1:
            raise ValueError(f"direct transition macro shape drift: {transition['id']}")
        emitted, match = direct[0]
        if (
            emitted["scope"] != expected_scope
            or match.group("source") != state_ids[transition["source"]]
            or match.group("target") != state_ids[transition["target"]]
            or bool(match.group("forced"))
            != state_is_composite[transition["source"]]
        ):
            raise ValueError(f"direct transition endpoint projection drift: {transition['id']}")
        return

    if transition["attributes"]["transition_kind"] == "initial":
        scope = transition.get("scope")
        target_chain = _source_chain(transition["target"], parents)
        if scope is None:
            path = target_chain
        elif scope in target_chain:
            path = target_chain[target_chain.index(scope) + 1 :]
        else:
            path = []
        main = by_role.get("source_initial_transition", [])
        expected_scope = scope or "__root__"
        if (
            not path
            or len(main) != 1
            or main[0][0]["scope"] != expected_scope
            or main[0][1].group("source") != "[*]"
            or main[0][1].group("target") != state_ids[path[0]]
            or bool(main[0][1].group("forced"))
        ):
            raise ValueError(f"initial transition endpoint projection drift: {transition['id']}")
        nested = by_role.get("source_initial_nested_entry_segment", [])
        actual_nested = [
            (
                emitted["scope"],
                match.group("source"),
                match.group("target"),
                bool(match.group("forced")),
            )
            for emitted, match in nested
        ]
        expected_nested = [
            (parent_state, "[*]", state_ids[child_state], False)
            for parent_state, child_state in zip(path, path[1:])
        ]
        if actual_nested != expected_nested:
            raise ValueError(f"nested initial projection drift: {transition['id']}")
        return

    if transition["attributes"]["transition_kind"] == "final":
        source_chain = _source_chain(transition["source"], parents)
        boundary_scope = transition.get("scope")
        if boundary_scope is None:
            exit_states = list(reversed(source_chain[1:]))
            actual_exits = [
                (
                    emitted["scope"],
                    match.group("source"),
                    match.group("target"),
                    bool(match.group("forced")),
                )
                for emitted, match in by_role.get("final_exit_segment", [])
            ]
            expected_exits = [
                (
                    parents[state_id] or "__root__",
                    state_ids[state_id],
                    "[*]",
                    state_is_composite[state_id],
                )
                for state_id in exit_states
            ]
            terminal = by_role.get("source_final_transition", [])
            expected_terminal = (
                "__root__",
                state_ids[source_chain[0]],
                "[*]",
                state_is_composite[source_chain[0]],
            )
            actual_terminal = [
                (
                    emitted["scope"],
                    match.group("source"),
                    match.group("target"),
                    bool(match.group("forced")),
                )
                for emitted, match in terminal
            ]
            if actual_exits != expected_exits or actual_terminal != [expected_terminal]:
                raise ValueError(f"root final boundary projection drift: {transition['id']}")
        else:
            linked = [
                state
                for state in synthetic_states
                if state.get("source_transition_id") == transition["id"]
                and state["generated_reason"] == "nested_plantuml_final_completion_hold"
            ]
            if len(linked) != 1 or boundary_scope not in source_chain:
                raise ValueError(f"nested final boundary projection drift: {transition['id']}")
            path = source_chain[source_chain.index(boundary_scope) + 1 :]
            exit_states = list(reversed(path[1:]))
            actual_exits = [
                (
                    emitted["scope"],
                    match.group("source"),
                    match.group("target"),
                    bool(match.group("forced")),
                )
                for emitted, match in by_role.get("nested_final_exit_segment", [])
            ]
            expected_exits = [
                (
                    parents[state_id] or "__root__",
                    state_ids[state_id],
                    "[*]",
                    state_is_composite[state_id],
                )
                for state_id in exit_states
            ]
            terminal_role = (
                "nested_final_completion_hold"
                if len(path) == 1
                else "nested_final_completion_continuation"
            )
            terminal_source = transition["source"] if len(path) == 1 else path[0]
            terminal = by_role.get(terminal_role, [])
            actual_terminal = [
                (
                    emitted["scope"],
                    match.group("source"),
                    match.group("target"),
                    bool(match.group("forced")),
                )
                for emitted, match in terminal
            ]
            expected_terminal = (
                boundary_scope,
                state_ids[terminal_source],
                linked[0]["fcstm_id"],
                state_is_composite[terminal_source] if len(path) == 1 else False,
            )
            if actual_exits != expected_exits or actual_terminal != [expected_terminal]:
                raise ValueError(f"nested final boundary projection drift: {transition['id']}")
        return

    source_chain = _source_chain(transition["source"], parents)
    target_chain = _source_chain(transition["target"], parents)
    common = 0
    while (
        common < len(source_chain)
        and common < len(target_chain)
        and source_chain[common] == target_chain[common]
    ):
        common += 1

    if reason == "R45.MAP.composite_to_descendant_forced":
        forced = by_role.get("composite_source_forced_descendant_entry", [])
        path = target_chain[common:]
        if (
            len(forced) != 1
            or forced[0][0]["scope"] != transition["source"]
            or forced[0][1].group("source") != "*"
            or not forced[0][1].group("forced")
            or not path
            or forced[0][1].group("target") != state_ids[path[0]]
        ):
            raise ValueError(f"composite descendant projection drift: {transition['id']}")
        entries = by_role.get("cross_scope_target_entry_segment", [])
        actual_entries = [
            (
                emitted["scope"],
                match.group("source"),
                match.group("target"),
                bool(match.group("forced")),
            )
            for emitted, match in entries
        ]
        expected_entries = [
            (parent_state, "[*]", state_ids[child_state], False)
            for parent_state, child_state in zip(path, path[1:])
        ]
        if actual_entries != expected_entries:
            raise ValueError(f"deep target projection drift: {transition['id']}")
        return

    if reason == "R45.MAP.descendant_to_ancestor_reentry":
        continuation = by_role.get("ancestor_reentry_parent_continuation", [])
        target_id = state_ids[transition["target"]]
        exit_segments = by_role.get("ancestor_reentry_exit_segment", []) + by_role.get(
            "ancestor_reentry_child_exit", []
        )
        exit_states = list(reversed(source_chain[len(target_chain) :]))
        actual_exits = [
            (
                emitted["scope"],
                match.group("source"),
                match.group("target"),
                bool(match.group("forced")),
            )
            for emitted, match in exit_segments
        ]
        expected_exits = [
            (
                parents[state_id] or "__root__",
                state_ids[state_id],
                "[*]",
                state_is_composite[state_id],
            )
            for state_id in exit_states
        ]
        if actual_exits != expected_exits:
            raise ValueError(f"ancestor reentry exit projection drift: {transition['id']}")
        expected_continuation_scope = parents[transition["target"]] or "__root__"
        if len(continuation) != 1 or (
            continuation[0][0]["scope"],
            continuation[0][1].group("source"),
            continuation[0][1].group("target"),
        ) != (expected_continuation_scope, target_id, target_id):
            raise ValueError(f"ancestor reentry target projection drift: {transition['id']}")
        if continuation[0][1].group("forced"):
            raise ValueError(f"ancestor reentry continuation force drift: {transition['id']}")
        return

    if reason == "R45.MAP.cross_scope_exit_continuation":
        source_branch = source_chain[common]
        target_branch = target_chain[common]
        continuation = by_role.get("cross_scope_parent_continuation", [])
        lca_scope = source_chain[common - 1] if common else "__root__"
        if len(continuation) != 1 or (
            continuation[0][0]["scope"],
            continuation[0][1].group("source"),
            continuation[0][1].group("target"),
        ) != (lca_scope, state_ids[source_branch], state_ids[target_branch]):
            raise ValueError(f"cross-scope continuation projection drift: {transition['id']}")
        expected_continuation_forced = (
            transition["source"] == source_branch
            and state_is_composite[transition["source"]]
        )
        if bool(continuation[0][1].group("forced")) != expected_continuation_forced:
            raise ValueError(f"cross-scope continuation force drift: {transition['id']}")
        exits = by_role.get("cross_scope_exit_segment", [])
        exit_states = list(reversed(source_chain[common + 1 :]))
        actual_exits = [
            (
                emitted["scope"],
                match.group("source"),
                match.group("target"),
                bool(match.group("forced")),
            )
            for emitted, match in exits
        ]
        expected_exits = [
            (
                parents[state_id] or "__root__",
                state_ids[state_id],
                "[*]",
                state_is_composite[state_id],
            )
            for state_id in exit_states
        ]
        if actual_exits != expected_exits:
            raise ValueError(f"cross-scope exit projection drift: {transition['id']}")
        entries = by_role.get("cross_scope_target_entry_segment", [])
        actual_entries = [
            (
                emitted["scope"],
                match.group("source"),
                match.group("target"),
                bool(match.group("forced")),
            )
            for emitted, match in entries
        ]
        expected_entries = [
            (parent_state, "[*]", state_ids[child_state], False)
            for parent_state, child_state in zip(
                target_chain[common:], target_chain[common + 1 :]
            )
        ]
        if actual_entries != expected_entries:
            raise ValueError(f"cross-scope target projection drift: {transition['id']}")
        return

    raise ValueError(f"unsupported mapping reason in source projection audit: {reason}")


def audit_lowered_artifact(
    *,
    canonical: dict[str, Any],
    fcstm: str,
    comparison: dict[str, Any],
    model: Any,
    inspect_report: dict[str, Any],
) -> dict[str, Any]:
    """Independently prove that the emitted FCSTM contains every mapped source fact."""

    if comparison["structural_verdict"] != "structure_preserved":
        raise ValueError("structural verdict is not preserved")
    if comparison["blocked_transition_count"] != 0:
        raise ValueError("blocked source transitions remain")
    if canonical.get("metadata", {}).get("unparsed_semantic_lines"):
        raise ValueError("canonical still contains unparsed semantic source lines")
    _assert_official_identity_projection(canonical)

    root_path = inspect_report["root_state_path"]
    actual_states = _state_lookup(model)
    scope_paths = _scope_paths(comparison, root_path)
    canonical_states = {state["id"]: state for state in canonical["model"]["states"]}
    canonical_transitions = {
        transition["id"]: transition for transition in canonical["model"]["transitions"]
    }
    if Counter(canonical_states.keys()) != Counter(
        mapping["state_id"] for mapping in comparison["state_mappings"]
    ):
        raise ValueError("state trace keys do not equal canonical state IDs")
    if Counter(canonical_transitions.keys()) != Counter(
        mapping["transition_id"] for mapping in comparison["transition_mappings"]
    ):
        raise ValueError("transition trace keys do not equal canonical transition IDs")
    if [item["transition_id"] for item in comparison["transition_mappings"]] != [
        item["id"] for item in canonical["model"]["transitions"]
    ]:
        raise ValueError("transition trace order differs from canonical source order")
    source_paths: set[str] = set()
    for mapping in comparison["state_mappings"]:
        source_state = canonical_states[mapping["state_id"]]
        expected_source = (
            source_state.get("parent"),
            source_state.get("kind"),
            source_state.get("label"),
            source_state["attributes"].get("declared_with_block", False),
            source_state["attributes"].get("parent_region_indices", [0]),
            source_state.get("raw_ref"),
        )
        traced_source = (
            mapping["source_parent"],
            mapping["source_kind"],
            mapping["source_label"],
            mapping["source_declared_with_block"],
            mapping["source_parent_region_indices"],
            mapping["raw_ref"],
        )
        if traced_source != expected_source:
            raise ValueError(f"state trace drift for {mapping['state_id']}")
        expected_display = _state_display(canonical, source_state)
        if mapping["fcstm_display_name"] != expected_display:
            raise ValueError(f"state display trace drift for {mapping['state_id']}")
        path = mapping["fcstm_path"]
        if path in source_paths:
            raise ValueError(f"source states are not mapped injectively: {path}")
        source_paths.add(path)
        state = actual_states.get(path)
        if state is None:
            raise ValueError(f"mapped source state missing from FCSTM AST: {path}")
        if state.extra_name != mapping["fcstm_display_name"]:
            raise ValueError(f"mapped source display metadata mismatch for {path}")
        actual_parent = ".".join(state.parent.path) if state.parent is not None else None
        if actual_parent != mapping["fcstm_parent_path"]:
            raise ValueError(
                f"mapped source parent mismatch for {path}: "
                f"expected {mapping['fcstm_parent_path']}, got {actual_parent}"
            )
        if mapping["source_kind"] in {"fork", "join", "choice", "junction"} and not state.is_pseudo:
            raise ValueError(f"PlantUML pseudo kind was not retained for {path}")
    synthetic_paths: set[str] = set()
    for mapping in comparison["synthetic_state_mappings"]:
        path = mapping["fcstm_path"]
        if path in source_paths or path in synthetic_paths:
            raise ValueError(f"synthetic state path is not unique: {path}")
        synthetic_paths.add(path)
        state = actual_states.get(path)
        if state is None:
            raise ValueError(f"tracked synthetic state missing from FCSTM AST: {path}")
        actual_parent = ".".join(state.parent.path) if state.parent is not None else None
        if actual_parent != mapping["fcstm_parent_path"]:
            raise ValueError(f"synthetic parent mismatch for {path}")
        if state.extra_name != mapping["display_name"]:
            raise ValueError(f"synthetic display metadata mismatch for {path}")
    expected_state_paths = {root_path} | source_paths | synthetic_paths
    if set(actual_states) != expected_state_paths:
        raise ValueError(
            "FCSTM AST contains missing or untracked states: "
            f"missing={sorted(expected_state_paths - set(actual_states))}, "
            f"untracked={sorted(set(actual_states) - expected_state_paths)}"
        )

    expected_raw_events = {
        transition.get("event")
        for transition in canonical["model"]["transitions"]
        if transition.get("event")
    }
    if Counter(expected_raw_events) != Counter(
        mapping["raw_label"] for mapping in comparison["event_mappings"]
    ):
        raise ValueError("opaque event trace does not reconstruct canonical labels")
    actual_events = model.root_state.events
    if set(actual_events) != {
        mapping["fcstm_id"] for mapping in comparison["event_mappings"]
    }:
        raise ValueError("FCSTM event declarations contain missing or untracked events")
    for mapping in comparison["event_mappings"]:
        event = actual_events[mapping["fcstm_id"]]
        if event.extra_name != mapping["raw_label"]:
            raise ValueError(f"opaque event label drift for {mapping['fcstm_path']}")

    for mapping in comparison["body_mappings"]:
        state = actual_states.get(mapping["fcstm_path"])
        if state is None or mapping["text"] not in (state.extra_name or ""):
            raise ValueError(
                f"opaque PlantUML body missing from FCSTM display metadata: {mapping['raw_ref']}"
            )
    expected_body_facts = sorted(
        (
            state["id"],
            body.get("raw_ref"),
            body.get("text") or "",
        )
        for state in canonical["model"]["states"]
        for body in state["attributes"].get("body_lines", [])
    )
    traced_body_facts = sorted(
        (item["state_id"], item.get("raw_ref"), item.get("text") or "")
        for item in comparison["body_mappings"]
    )
    if traced_body_facts != expected_body_facts:
        raise ValueError("opaque body trace does not reconstruct canonical body facts")

    inspect_states = {state["path"]: state for state in inspect_report["states"]}
    expected_lifecycle_facts = sorted(
        (
            state["id"],
            action["kind"],
            action["text"],
            action.get("raw_ref"),
        )
        for state in canonical["model"]["states"]
        for action in state["attributes"].get("lifecycle_actions", [])
    )
    traced_lifecycle_facts = sorted(
        (item["state_id"], item["kind"], item["text"], item.get("raw_ref"))
        for item in comparison["lifecycle_mappings"]
    )
    if traced_lifecycle_facts != expected_lifecycle_facts:
        raise ValueError("lifecycle trace does not reconstruct canonical actions")
    for mapping in comparison["lifecycle_mappings"]:
        state = inspect_states[mapping["fcstm_path"]]
        action_sets = {
            "entry": state["entry_actions"],
            "do": state["during_actions"] + state["aspect_before"] + state["aspect_after"],
            "exit": state["exit_actions"],
        }
        if mapping["fcstm_action_id"] not in action_sets[mapping["kind"]]:
            raise ValueError(f"lifecycle action missing from inspect: {mapping['raw_ref']}")
    root_state = actual_states[root_path]
    expected_root_display = _root_display(canonical)
    if root_state.extra_name != expected_root_display:
        raise ValueError("root display metadata drift")
    for mapping in comparison["orphan_lifecycle_mappings"]:
        if mapping["text"] not in (root_state.extra_name or ""):
            raise ValueError(
                f"ownerless lifecycle missing from root display metadata: {mapping['raw_ref']}"
            )
    expected_orphans = sorted(
        (item.get("kind"), item.get("text") or "", item.get("raw_ref"))
        for item in canonical.get("metadata", {}).get("orphan_lifecycle_actions", [])
    )
    traced_orphans = sorted(
        (item.get("kind"), item.get("text") or "", item.get("raw_ref"))
        for item in comparison["orphan_lifecycle_mappings"]
    )
    if traced_orphans != expected_orphans:
        raise ValueError("ownerless lifecycle trace does not reconstruct canonical facts")

    canonical_regions = canonical["model"].get("concurrent_regions", [])
    traced_regions = comparison["concurrent_region_mappings"]
    if comparison["concurrent_region_coverage"] != (
        f"{len(traced_regions)}/{len(canonical_regions)}"
    ):
        raise ValueError("concurrent region coverage drift")
    if len(traced_regions) != len(canonical_regions):
        raise ValueError("concurrent region trace count drift")
    for source, traced in zip(canonical_regions, traced_regions):
        if any(traced.get(key) != value for key, value in source.items()):
            raise ValueError(f"concurrent region trace drift: {source['id']}")
        owner_path = root_path if source.get("owner_scope") is None else scope_paths[
            source["owner_scope"]
        ]
        if traced["fcstm_owner_path"] != owner_path:
            raise ValueError(f"concurrent region owner drift: {source['id']}")
        if traced["display_line"] not in (actual_states[owner_path].extra_name or ""):
            raise ValueError(f"concurrent region missing from display: {source['id']}")

    canonical_separators = canonical.get("metadata", {}).get(
        "concurrent_region_separators", []
    )
    traced_separators = comparison["concurrent_region_separator_mappings"]
    if comparison["concurrent_region_separator_coverage"] != (
        f"{len(traced_separators)}/{len(canonical_separators)}"
    ):
        raise ValueError("concurrent separator coverage drift")
    if len(traced_separators) != len(canonical_separators):
        raise ValueError("concurrent separator trace count drift")
    for source, traced in zip(canonical_separators, traced_separators):
        if any(traced.get(key) != value for key, value in source.items()):
            raise ValueError(f"concurrent separator trace drift: {source['id']}")
        owner_path = root_path if source.get("owner_scope") is None else scope_paths[
            source["owner_scope"]
        ]
        if traced["fcstm_owner_path"] != owner_path:
            raise ValueError(f"concurrent separator owner drift: {source['id']}")
        if traced["display_line"] not in (actual_states[owner_path].extra_name or ""):
            raise ValueError(f"concurrent separator missing from display: {source['id']}")

    canonical_normalizations = canonical.get("metadata", {}).get(
        "source_normalizations", []
    )
    traced_normalizations = comparison["source_normalization_mappings"]
    if comparison["source_normalization_coverage"] != (
        f"{len(traced_normalizations)}/{len(canonical_normalizations)}"
    ):
        raise ValueError("source normalization coverage drift")
    if len(traced_normalizations) != len(canonical_normalizations):
        raise ValueError("source normalization trace count drift")
    for source, traced in zip(canonical_normalizations, traced_normalizations):
        if any(traced.get(key) != value for key, value in source.items()):
            raise ValueError(f"source normalization trace drift: {source['raw_ref']}")
        rendered = (
            f"[PlantUML source normalization {source['rule_id']}] "
            f"{source['raw_ref']}: {source['before']} -> {source['after']}"
        )
        if traced["fcstm_owner_path"] != root_path or rendered not in (
            root_state.extra_name or ""
        ):
            raise ValueError(f"source normalization missing from display: {source['raw_ref']}")

    emitted_lines = [
        emitted["line"]
        for mapping in comparison["transition_mappings"]
        for emitted in mapping["emitted"]
    ]
    synthetic_lines = [
        mapping["line"] for mapping in comparison["synthetic_transition_mappings"]
    ]
    emitted_object_ids = [
        emitted["emitted_object_id"]
        for mapping in comparison["transition_mappings"]
        for emitted in mapping["emitted"]
    ]
    if len(emitted_object_ids) != len(set(emitted_object_ids)):
        raise ValueError("emitted transition segment IDs are not unique")
    expected_line_counts = Counter(emitted_lines + synthetic_lines)
    fcstm_line_counts = Counter(
        line.strip()
        for line in fcstm.splitlines()
        if _TRANSITION_RE.fullmatch(line.strip())
    )
    if fcstm_line_counts != expected_line_counts:
        raise ValueError(
            "FCSTM authored transition multiset differs from source and synthetic trace: "
            f"missing={expected_line_counts - fcstm_line_counts}, "
            f"untracked={fcstm_line_counts - expected_line_counts}"
        )

    actual_transition_counts: Counter[tuple[Any, ...]] = Counter()
    forced_origin_counts: Counter[str] = Counter()
    for transition in inspect_report["transitions"]:
        actual_transition_counts[
            (
                transition["from_path"],
                transition["to_path"],
                transition.get("event"),
                bool(transition.get("is_forced")),
            )
        ] += 1
        if transition.get("forced_origin"):
            forced_origin_counts[_normalize_forced_origin(transition["forced_origin"])] += 1

    def actual_indices_for_line(scope_key: str, line: str) -> list[int]:
        match = _TRANSITION_RE.fullmatch(line)
        if match is None:
            raise ValueError(f"unrecognized traced transition syntax: {line}")
        scope_path = scope_paths[scope_key]
        event = match.group("event")
        qualified_event = f"{root_path}.{event}" if event else None
        if not match.group("forced"):
            signature = (
                _endpoint_path(scope_path, match.group("source")),
                _endpoint_path(scope_path, match.group("target")),
                qualified_event,
                False,
            )
            return [
                index
                for index, item in enumerate(inspect_report["transitions"])
                if (
                    item["from_path"],
                    item["to_path"],
                    item.get("event"),
                    bool(item.get("is_forced")),
                )
                == signature
            ]
        normalized_origin = _normalize_forced_origin(line)
        candidates = [
            item
            for item in inspect_report["transitions"]
            if item.get("forced_origin")
            and _normalize_forced_origin(item["forced_origin"]) == normalized_origin
        ]
        target = match.group("target")
        if target != "[*]":
            target_path = _endpoint_path(scope_path, target)
            candidates = [item for item in candidates if item["to_path"] == target_path]
        elif match.group("source") != "*":
            source_prefix = _endpoint_path(scope_path, match.group("source"))
            candidates = [
                item
                for item in candidates
                if item["from_path"] == source_prefix
                or item["from_path"].startswith(f"{source_prefix}.")
            ]
        candidate_ids = {id(item) for item in candidates}
        return [
            index
            for index, item in enumerate(inspect_report["transitions"])
            if id(item) in candidate_ids
        ]

    expected_transition_counts: Counter[tuple[Any, ...]] = Counter()
    forced_authored_counts: Counter[str] = Counter()
    state_ids = {
        mapping["state_id"]: mapping["fcstm_id"]
        for mapping in comparison["state_mappings"]
    }
    parents = {
        state["id"]: state.get("parent") for state in canonical["model"]["states"]
    }
    event_ids = {
        mapping["raw_label"]: mapping["fcstm_id"]
        for mapping in comparison["event_mappings"]
    }
    state_is_composite = {
        mapping["state_id"]: bool(actual_states[mapping["fcstm_path"]].substates)
        for mapping in comparison["state_mappings"]
    }
    for mapping in comparison["transition_mappings"]:
        source_transition = canonical_transitions[mapping["transition_id"]]
        expected_source_transition = {
            "id": source_transition["id"],
            "scope": source_transition.get("scope"),
            "kind": source_transition["attributes"]["transition_kind"],
            "source": source_transition["source"],
            "target": source_transition["target"],
            "raw_label": source_transition.get("label"),
            "raw_event": source_transition.get("event"),
            "raw_ref": source_transition.get("raw_ref"),
            "region_index": source_transition["attributes"].get("region_index", 0),
        }
        if mapping["source_transition"] != expected_source_transition:
            raise ValueError(f"transition trace drift for {mapping['transition_id']}")
        _assert_source_projection(
            mapping=mapping,
            transition=source_transition,
            state_ids=state_ids,
            parents=parents,
            synthetic_states=comparison["synthetic_state_mappings"],
            event_ids=event_ids,
            state_is_composite=state_is_composite,
        )
        for emitted in mapping["emitted"]:
            line = emitted["line"]
            match = _TRANSITION_RE.fullmatch(line)
            if match is None:
                raise ValueError(f"unrecognized emitted FCSTM transition syntax: {line}")
            if match.group("forced"):
                forced_authored_counts[_normalize_forced_origin(line)] += 1
                continue
            scope_path = scope_paths[emitted["scope"]]
            event = match.group("event")
            expected_transition_counts[
                (
                    _endpoint_path(scope_path, match.group("source")),
                    _endpoint_path(scope_path, match.group("target")),
                    f"{root_path}.{event}" if event else None,
                    False,
                )
            ] += 1

    synthetic_initial_reasons = {"missing_source_initial_fail_closed"}
    expected_synthetic_initial_targets = Counter(
        (
            state["fcstm_parent_path"],
            state["fcstm_id"],
            state["generated_reason"],
        )
        for state in comparison["synthetic_state_mappings"]
        if state["generated_reason"] in synthetic_initial_reasons
    )
    traced_synthetic_initial_targets: Counter[tuple[str, str, str]] = Counter()
    for mapping in comparison["synthetic_transition_mappings"]:
        match = _TRANSITION_RE.fullmatch(mapping["line"])
        if match is None or match.group("forced"):
            raise ValueError(f"invalid synthetic transition trace: {mapping}")
        reason = mapping["generated_reason"]
        if reason not in synthetic_initial_reasons:
            raise ValueError(f"unsupported synthetic transition reason: {reason}")
        scope_path = scope_paths[mapping["scope"]]
        expected_owner = None if mapping["scope"] == "__root__" else mapping["scope"]
        if (
            mapping["owner_state_id"] != expected_owner
            or match.group("source") != "[*]"
            or match.group("target") == "[*]"
            or match.group("event") is not None
        ):
            raise ValueError(f"synthetic initial contract drift: {mapping}")
        target_key = (scope_path, match.group("target"), reason)
        if target_key not in expected_synthetic_initial_targets:
            raise ValueError(f"synthetic initial target/reason drift: {mapping}")
        traced_synthetic_initial_targets[target_key] += 1
        expected_transition_counts[
            (
                _endpoint_path(scope_path, match.group("source")),
                _endpoint_path(scope_path, match.group("target")),
                None,
                False,
            )
        ] += 1
    if traced_synthetic_initial_targets != expected_synthetic_initial_targets:
        raise ValueError(
            "synthetic initial coverage differs from tracked synthetic states: "
            f"missing={expected_synthetic_initial_targets - traced_synthetic_initial_targets}, "
            f"extra={traced_synthetic_initial_targets - expected_synthetic_initial_targets}"
        )

    mappings_by_id = {
        mapping["transition_id"]: mapping
        for mapping in comparison["transition_mappings"]
    }
    initial_by_scope: dict[str, list[dict[str, Any]]] = {}
    unlabeled_by_source_scope: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for transition in canonical["model"]["transitions"]:
        kind = transition["attributes"]["transition_kind"]
        if kind == "initial":
            initial_by_scope.setdefault(transition.get("scope") or "__root__", []).append(
                transition
            )
        elif kind != "final" and not transition.get("event"):
            first_emitted = mappings_by_id[transition["id"]]["emitted"][0]
            key = (transition["source"], first_emitted["scope"])
            unlabeled_by_source_scope.setdefault(key, []).append(transition)

    for scope_key, transitions in initial_by_scope.items():
        if len(transitions) < 2:
            continue
        order: list[int] = []
        for transition in transitions:
            candidates = [
                item
                for item in mappings_by_id[transition["id"]]["emitted"]
                if item["scope"] == scope_key
                and (parsed := _TRANSITION_RE.fullmatch(item["line"])) is not None
                and parsed.group("source") == "[*]"
            ]
            if not candidates:
                raise ValueError(f"initial transition trace has no scope entry: {transition['id']}")
            emitted = candidates[0]
            indices = actual_indices_for_line(scope_key, emitted["line"])
            if not indices:
                raise ValueError(f"initial transition missing from AST order: {transition['id']}")
            order.append(min(indices))
        if order != sorted(order):
            raise ValueError(f"initial transition declaration order drift in {scope_key}")

    for (source_id, scope_key), transitions in unlabeled_by_source_scope.items():
        if len(transitions) < 2:
            continue
        order = []
        for transition in transitions:
            emitted = mappings_by_id[transition["id"]]["emitted"][0]
            indices = actual_indices_for_line(emitted["scope"], emitted["line"])
            if not indices:
                raise ValueError(f"fan-out transition missing from AST order: {transition['id']}")
            order.append(min(indices))
        if order != sorted(order):
            raise ValueError(
                f"unlabeled fan-out declaration order drift for {source_id} in {scope_key}"
            )

    source_initial_lines_by_scope: dict[str, list[str]] = {}
    priority_entry_lines_by_scope: dict[str, list[str]] = {}
    ordinary_initial_lines_by_scope: dict[str, list[str]] = {}
    for mapping in comparison["transition_mappings"]:
        for emitted in mapping["emitted"]:
            parsed = _TRANSITION_RE.fullmatch(emitted["line"])
            if parsed is not None and parsed.group("source") == "[*]":
                source_initial_lines_by_scope.setdefault(emitted["scope"], []).append(
                    emitted["line"]
                )
                if emitted["generated_role"] in {
                    "cross_scope_target_entry_segment",
                    "source_initial_nested_entry_segment",
                }:
                    priority_entry_lines_by_scope.setdefault(emitted["scope"], []).append(
                        emitted["line"]
                    )
                else:
                    ordinary_initial_lines_by_scope.setdefault(emitted["scope"], []).append(
                        emitted["line"]
                    )
    for scope_key, lines in priority_entry_lines_by_scope.items():
        priority_counts = Counter(lines)
        ordinary_counts = Counter(ordinary_initial_lines_by_scope.get(scope_key, []))
        priority_indices: list[int] = []
        ordinary_indices: list[int] = []
        for line in priority_counts.keys() | ordinary_counts.keys():
            indices = sorted(actual_indices_for_line(scope_key, line))
            priority_count = priority_counts[line]
            ordinary_count = ordinary_counts[line]
            if len(indices) < priority_count + ordinary_count:
                raise ValueError(f"initial occurrence count drift in {scope_key}: {line}")
            priority_indices.extend(indices[:priority_count])
            ordinary_indices.extend(
                indices[priority_count : priority_count + ordinary_count]
            )
        if ordinary_indices and (
            not priority_indices or max(priority_indices) >= min(ordinary_indices)
        ):
            raise ValueError(f"transition-specific entry priority drift in {scope_key}")
    for mapping in comparison["synthetic_transition_mappings"]:
        indices = actual_indices_for_line(mapping["scope"], mapping["line"])
        if not indices:
            raise ValueError(f"synthetic initial missing from AST order: {mapping}")
        source_indices = [
            index
            for line in source_initial_lines_by_scope.get(mapping["scope"], [])
            for index in actual_indices_for_line(mapping["scope"], line)
        ]
        if mapping["generated_reason"] == "missing_source_initial_fail_closed":
            if source_indices and min(indices) <= max(source_indices):
                raise ValueError(f"fail-closed placeholder priority drift: {mapping}")
        elif source_indices and max(indices) >= min(source_indices):
            raise ValueError(f"lifecycle active initial priority drift: {mapping}")

    actual_normal_counts = Counter(
        {
            signature: count
            for signature, count in actual_transition_counts.items()
            if signature[3] is False
        }
    )
    if actual_normal_counts != expected_transition_counts:
        raise ValueError(
            "pyfcstm normal AST transition multiset differs from trace: "
            f"missing={expected_transition_counts - actual_normal_counts}, "
            f"untracked={actual_normal_counts - expected_transition_counts}"
        )
    missing_forced = {
        line: count - forced_origin_counts[line]
        for line, count in forced_authored_counts.items()
        if forced_origin_counts[line] < count
    }
    if missing_forced:
        raise ValueError(f"mapped forced transitions missing from pyfcstm AST: {missing_forced}")
    unexpected_forced = set(forced_origin_counts) - set(forced_authored_counts)
    if unexpected_forced:
        raise ValueError(f"untracked forced transition origins: {sorted(unexpected_forced)}")

    return {
        "schema_version": "r4_5.plantuml_fcstm_ast_audit.v1",
        "status": "passed",
        "source_state_paths_verified": len(source_paths),
        "source_transition_macros_verified": len(comparison["transition_mappings"]),
        "emitted_transition_segments_verified": len(emitted_lines),
        "normal_ast_signatures_verified": sum(expected_transition_counts.values()),
        "forced_authored_lines_verified": sum(forced_authored_counts.values()),
        "body_lines_verified": len(comparison["body_mappings"]),
        "lifecycle_items_verified": (
            int(comparison["lifecycle_action_coverage"].split("/")[0])
        ),
        "concurrent_regions_verified": len(traced_regions),
        "concurrent_region_separators_verified": len(traced_separators),
        "source_normalizations_verified": len(traced_normalizations),
    }
