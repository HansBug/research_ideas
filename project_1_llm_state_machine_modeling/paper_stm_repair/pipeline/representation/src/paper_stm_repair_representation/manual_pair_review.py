from __future__ import annotations

import hashlib
import json
import re
from typing import Any

from jsonschema import Draft202012Validator


GENERIC_REVIEW_ANCHORS = {
    "[*]",
    "--",
    "->",
    "@enduml",
    "@startuml",
    "event",
    "state",
}
SHALLOW_REVIEW_PHRASES = {
    "declared reviewed",
    "remaining semantics",
    "reviewed as required",
    "all semantics were reviewed",
}
RISK_ASSESSMENT_BY_TAG = {
    "concurrent_region": "capability_excluded",
    "explicit_concurrency": "capability_excluded",
    "final_boundary": "source_fact_preserved",
    "lifecycle": "capability_excluded",
    "multi_segment_macro": "compiler_artifact_excluded",
    "official_identity_remap": "source_fact_preserved",
    "source_normalization": "compiler_artifact_excluded",
    "synthetic_state": "compiler_artifact_excluded",
}
SOURCE_ANCHOR_PREFIX = "source-ref:"
FCSTM_ANCHOR_PREFIX = "element-ref:"
CAPABILITY_EXCLUDED_STATE_KINDS = {
    "choice",
    "fork",
    "join",
    "junction",
}
SOURCE_PROJECTION_RULES = {
    "state": {
        "allowed": {("direct", "preserved")},
        "compiler_policy": "forbidden",
    },
    "capability_excluded_state": {
        "allowed": {
            ("capability_excluded", "preserved_with_exclusions"),
            ("capability_excluded", "source_issue_visible"),
        },
        "compiler_policy": "forbidden",
    },
    "transition_macro_root": {
        "allowed": {
            ("macro", "preserved_with_exclusions"),
            ("macro", "source_issue_visible"),
        },
        "compiler_policy": "required",
    },
    "state_body_text": {
        "allowed": {
            ("metadata", "preserved_with_exclusions"),
            ("metadata", "source_issue_visible"),
        },
        "compiler_policy": "forbidden",
    },
    "concurrent_region": {
        "allowed": {
            ("capability_excluded", "preserved_with_exclusions"),
            ("capability_excluded", "source_issue_visible"),
        },
        "compiler_policy": "forbidden",
    },
    "lifecycle_action": {
        "allowed": {
            ("capability_excluded", "preserved_with_exclusions"),
            ("capability_excluded", "source_issue_visible"),
        },
        "compiler_policy": "required",
    },
}


def _sha256_json(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def manual_review_observation_digest(review: dict[str, Any]) -> str:
    observations = review["observations"]
    return _sha256_json(
        {
            "narratives": {
                field: observations[field]
                for field in (
                    "nl_intent",
                    "plantuml_semantics",
                    "fcstm_projection",
                    "attribution_rationale",
                    "capability_rationale",
                )
            },
            "semantic_correspondences": review["semantic_correspondences"],
            "risk_assessments": review["second_pass"]["risk_assessments"],
        }
    )


def _source_line_for_ref(source_text: str, reference: str) -> str | None:
    marker = ":line:"
    if marker not in reference:
        return None
    suffix = reference.rsplit(marker, 1)[1]
    match = re.match(r"(\d+)", suffix)
    if match is None:
        return None
    line_number = int(match.group(1))
    lines = source_text.splitlines()
    if line_number < 1 or line_number > len(lines):
        return None
    return lines[line_number - 1].strip()


def _parse_exact_anchor(anchor: str, *, prefix: str) -> tuple[str, str] | None:
    if not anchor.startswith(prefix) or "|" not in anchor:
        return None
    reference, payload = anchor[len(prefix) :].split("|", 1)
    if (
        not reference
        or not payload
        or reference != reference.strip()
        or payload != payload.strip()
        or "\n" in reference
        or "\r" in reference
        or "\n" in payload
        or "\r" in payload
    ):
        return None
    return reference, payload


def plantuml_evidence_anchor(*, source_text: str, source_ref: str) -> str:
    line = _source_line_for_ref(source_text, source_ref)
    if not line:
        raise ValueError(f"PlantUML source ref has no non-empty line: {source_ref}")
    return f"{SOURCE_ANCHOR_PREFIX}{source_ref}|{line}"


def _plantuml_anchor_matches_refs(
    *, source_text: str, anchor: str, source_refs: list[str]
) -> bool:
    parsed = _parse_exact_anchor(anchor, prefix=SOURCE_ANCHOR_PREFIX)
    if parsed is None:
        return False
    reference, payload = parsed
    return (
        reference in source_refs
        and _source_line_for_ref(source_text, reference) == payload
    )


def _path_matches(actual: str, expected: str) -> bool:
    if actual == expected:
        return True
    _, separator, unwrapped = actual.partition(".")
    return bool(separator) and unwrapped == expected


def _scope_key(scope: str | None) -> str:
    return "" if scope in {None, "__root__"} else scope


def _fcstm_line_refs_by_element(
    *,
    fcstm_text: str,
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> dict[str, set[tuple[int, str]]]:
    state_pattern = re.compile(
        r"^(?:pseudo )?state ([A-Za-z_][A-Za-z0-9_]*)(?:\s+named\s+.*)?(?:\s+\{|;)$"
    )
    event_pattern = re.compile(
        r"^event ([A-Za-z_][A-Za-z0-9_]*)(?:\s+named\s+.*)?;$"
    )
    action_pattern = re.compile(
        r"^(enter abstract|exit abstract|>> during before abstract) "
        r"([A-Za-z_][A-Za-z0-9_]*);$"
    )
    lifecycle_kind_by_prefix = {
        "enter abstract": "entry",
        "exit abstract": "exit",
        ">> during before abstract": "do",
    }
    stack: list[str] = []
    records: list[tuple[int, str, str]] = []
    states: dict[str, tuple[int, str]] = {}
    events: dict[str, tuple[int, str]] = {}
    actions: dict[tuple[str, str, str], list[tuple[int, str]]] = {}
    for line_number, raw_line in enumerate(fcstm_text.splitlines(), start=1):
        line = raw_line.strip()
        if not line:
            continue
        if line == "}":
            if stack:
                stack.pop()
            continue
        scope = ".".join(stack)
        records.append((line_number, line, ".".join(stack[1:])))
        state_match = state_pattern.fullmatch(line)
        if state_match is not None:
            identifier = state_match.group(1)
            path = ".".join([*stack, identifier])
            states[path] = (line_number, line)
            if line.endswith("{"):
                stack.append(identifier)
            continue
        event_match = event_pattern.fullmatch(line)
        if event_match is not None:
            events[".".join([*stack, event_match.group(1)])] = (line_number, line)
            continue
        action_match = action_pattern.fullmatch(line)
        if action_match is not None:
            lifecycle_kind = lifecycle_kind_by_prefix[action_match.group(1)]
            actions.setdefault(
                (scope, lifecycle_kind, action_match.group(2)), []
            ).append((line_number, line))

    result: dict[str, set[tuple[int, str]]] = {
        element_id: set() for element_id in elements_by_id
    }
    for element_id, element in elements_by_id.items():
        for model_ref in element.get("model_refs", []):
            if not isinstance(model_ref, str) or ":" not in model_ref:
                continue
            kind, value = model_ref.split(":", 1)
            if kind == "state" and value in states:
                result[element_id].add(states[value])
            elif kind == "event" and value in events:
                result[element_id].add(events[value])

        metadata = element.get("metadata", {})
        kind = element.get("kind")
        if kind == "state_body_text":
            state_id = metadata.get("state_id")
            text = metadata.get("text") or element.get("semantic_fields", {}).get(
                "text"
            )
            marker = (
                json.dumps(
                    f"[PlantUML body] {text}",
                    ensure_ascii=False,
                )[1:-1]
                if isinstance(text, str)
                else None
            )
            result[element_id].update(
                line_ref
                for path, line_ref in states.items()
                if isinstance(state_id, str)
                and _path_matches(path, state_id)
                and marker
                and marker in line_ref[1]
            )
        elif kind == "concurrent_region":
            owner_scope = metadata.get("owner_scope")
            region_index = metadata.get("region_index")
            marker = (
                f"[PlantUML concurrent region {region_index}]"
                if isinstance(region_index, int)
                else None
            )
            result[element_id].update(
                line_ref
                for path, line_ref in states.items()
                if (
                    (
                        isinstance(owner_scope, str)
                        and _path_matches(path, owner_scope)
                    )
                    or (owner_scope is None and "." not in path)
                )
                and marker
                and marker in line_ref[1]
            )

    action_elements: dict[tuple[str, str, str], list[str]] = {}
    for element_id, element in elements_by_id.items():
        action_ids = [
            value
            for model_ref in element.get("model_refs", [])
            if isinstance(model_ref, str)
            and model_ref.startswith("action:")
            for value in [model_ref.split(":", 1)[1]]
        ]
        if not action_ids:
            continue
        source_lifecycle_elements = [
            source_element
            for macro_id in element.get("macro_ids", [])
            for source_id in macros_by_id.get(macro_id, {}).get(
                "source_element_ids", []
            )
            for source_element in [elements_by_id.get(source_id, {})]
            if source_element.get("kind") == "lifecycle_action"
        ]
        for source_element in source_lifecycle_elements:
            metadata = source_element.get("metadata", {})
            state_id = metadata.get("state_id")
            lifecycle_kind = metadata.get("lifecycle_kind")
            if not isinstance(state_id, str) or lifecycle_kind not in {
                "entry",
                "do",
                "exit",
            }:
                continue
            matching_scopes = {
                scope
                for scope, kind, action_id in actions
                if kind == lifecycle_kind
                and action_id in action_ids
                and _path_matches(scope, state_id)
            }
            for scope in matching_scopes:
                for action_id in action_ids:
                    key = (scope, lifecycle_kind, action_id)
                    if key in actions:
                        action_elements.setdefault(key, []).append(element_id)
    for key, element_ids in action_elements.items():
        line_refs = actions.get(key, [])
        if len(line_refs) == len(element_ids):
            for element_id, line_ref in zip(element_ids, line_refs):
                result[element_id].add(line_ref)

    emitted_elements: dict[tuple[str, str], list[str]] = {}
    for element_id, element in elements_by_id.items():
        metadata = element.get("metadata", {})
        line = metadata.get("line")
        scope = metadata.get("scope")
        if isinstance(line, str) and isinstance(scope, str):
            emitted_elements.setdefault((_scope_key(scope), line.strip()), []).append(
                element_id
            )
    emitted_lines: dict[tuple[str, str], list[tuple[int, str]]] = {}
    for line_number, line, scope in records:
        emitted_lines.setdefault((scope, line), []).append((line_number, line))
    for key, element_ids in emitted_elements.items():
        line_refs = emitted_lines.get(key, [])
        occurrences = {
            element_id: elements_by_id[element_id]
            .get("metadata", {})
            .get("scope_line_occurrence")
            for element_id in element_ids
        }
        if (
            len(line_refs) == len(element_ids)
            and set(occurrences.values()) == set(range(1, len(line_refs) + 1))
        ):
            for element_id, occurrence in occurrences.items():
                result[element_id].add(line_refs[occurrence - 1])
    return result


def _parse_fcstm_anchor(anchor: str) -> tuple[str, int, str] | None:
    parsed = _parse_exact_anchor(anchor, prefix=FCSTM_ANCHOR_PREFIX)
    if parsed is None:
        return None
    bound_ref, payload = parsed
    marker = "@line:"
    if marker not in bound_ref:
        return None
    element_id, line_text = bound_ref.rsplit(marker, 1)
    if not element_id or not line_text.isdigit() or int(line_text) < 1:
        return None
    return element_id, int(line_text), payload


def _fcstm_anchor_ids_for_element(
    *,
    element_id: str,
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> set[str]:
    if element_id not in elements_by_id:
        return set()
    allowed = {element_id}
    element = elements_by_id[element_id]
    if element.get("origin") == "source_owned":
        allowed.update(
            member_id
            for macro_id in element.get("macro_ids", [])
            for member_id in macros_by_id.get(macro_id, {}).get(
                "member_element_ids", []
            )
        )
    return allowed


def fcstm_evidence_anchors(
    *,
    fcstm_text: str,
    element_ids: list[str],
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> list[str]:
    """Return a deterministic minimal exact-line cover for review elements."""

    uncovered = set(element_ids)
    candidates: dict[str, set[str]] = {}
    line_refs = _fcstm_line_refs_by_element(
        fcstm_text=fcstm_text,
        elements_by_id=elements_by_id,
        macros_by_id=macros_by_id,
    )
    for target_id in element_ids:
        for anchor_id in _fcstm_anchor_ids_for_element(
            element_id=target_id,
            elements_by_id=elements_by_id,
            macros_by_id=macros_by_id,
        ):
            for line_number, line in line_refs.get(anchor_id, set()):
                anchor = (
                    f"{FCSTM_ANCHOR_PREFIX}{anchor_id}@line:{line_number}|{line}"
                )
                candidates.setdefault(anchor, set()).add(target_id)

    selected: list[str] = []
    while uncovered:
        ranked = sorted(
            (
                (-len(covered & uncovered), anchor, covered)
                for anchor, covered in candidates.items()
                if covered & uncovered
            )
        )
        if not ranked:
            break
        _, anchor, covered = ranked[0]
        selected.append(anchor)
        uncovered -= covered
    return selected


def _fcstm_anchor_matches_element(
    *,
    fcstm_text: str,
    anchor: str,
    element_id: str,
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> bool:
    parsed = _parse_fcstm_anchor(anchor)
    if parsed is None:
        return False
    anchor_id, line_number, payload = parsed
    if anchor_id not in _fcstm_anchor_ids_for_element(
        element_id=element_id,
        elements_by_id=elements_by_id,
        macros_by_id=macros_by_id,
    ):
        return False
    return (line_number, payload) in _fcstm_line_refs_by_element(
        fcstm_text=fcstm_text,
        elements_by_id=elements_by_id,
        macros_by_id=macros_by_id,
    ).get(anchor_id, set())


def _anchor_payload(anchor: str, *, prefix: str) -> str | None:
    if prefix == FCSTM_ANCHOR_PREFIX:
        parsed_fcstm = _parse_fcstm_anchor(anchor)
        return parsed_fcstm[2] if parsed_fcstm is not None else None
    parsed = _parse_exact_anchor(anchor, prefix=prefix)
    return parsed[1] if parsed is not None else None


def _source_projection_rule(element: dict[str, Any]) -> dict[str, Any] | None:
    kind = element.get("kind")
    if kind == "state" and element.get("semantic_fields", {}).get(
        "kind"
    ) in CAPABILITY_EXCLUDED_STATE_KINDS:
        return SOURCE_PROJECTION_RULES["capability_excluded_state"]
    return SOURCE_PROJECTION_RULES.get(kind)


def validate_manual_pair_review(
    *,
    review: dict[str, Any],
    case_id: str,
    pair_id: str,
    review_subject_sha256: str,
    contract: dict[str, Any],
    contract_sha256: str,
    nl_text: str,
    source_text: str,
    fcstm_text: str,
    validator: Draft202012Validator,
) -> None:
    validator.validate(review)
    if review["case_id"] != case_id or review["pair_id"] != pair_id:
        raise ValueError(f"manual review identity drift for {case_id}")
    if review["review_subject_sha256"] != review_subject_sha256:
        raise ValueError(f"stale manual review subject for {case_id}")
    if review["working_contract_sha256"] != contract_sha256:
        raise ValueError(f"stale manual working-contract hash for {case_id}")
    if not all(review["reviewed_inputs"].values()):
        raise ValueError(f"manual review did not read all required inputs for {case_id}")

    context = review["review_context"]
    if not all(
        isinstance(context[field], str) and context[field].strip() for field in context
    ):
        raise ValueError(f"manual review context is incomplete for {case_id}")
    if not context["session_id"].startswith("omx-") or not context[
        "model_id"
    ].startswith("gpt-"):
        raise ValueError(f"manual review context identity is invalid for {case_id}")

    observations = review["observations"]
    narrative_fields = (
        "nl_intent",
        "plantuml_semantics",
        "fcstm_projection",
        "attribution_rationale",
        "capability_rationale",
    )
    if any(len(observations[field].strip()) < 20 for field in narrative_fields):
        raise ValueError(f"manual review observations are too generic for {case_id}")
    if len({observations[field].strip() for field in narrative_fields}) != len(
        narrative_fields
    ):
        raise ValueError(f"manual review observations are duplicated for {case_id}")
    nl_anchors = observations["nl_anchors"]
    if not nl_anchors or any(
        len(anchor.strip()) < 4
        or anchor.strip() in GENERIC_REVIEW_ANCHORS
        or anchor not in nl_text
        for anchor in nl_anchors
    ):
        raise ValueError(f"manual review nl_anchors are not bound for {case_id}")
    for anchor_field, narrative_field, label in (
        ("nl_anchors", "nl_intent", "NL"),
        ("plantuml_anchors", "plantuml_semantics", "PlantUML"),
        ("fcstm_anchors", "fcstm_projection", "FCSTM"),
    ):
        prefix = (
            SOURCE_ANCHOR_PREFIX
            if anchor_field == "plantuml_anchors"
            else FCSTM_ANCHOR_PREFIX
            if anchor_field == "fcstm_anchors"
            else None
        )
        payloads = [
            _anchor_payload(anchor, prefix=prefix) if prefix else anchor
            for anchor in observations[anchor_field]
        ]
        if not payloads or not any(
            payload and payload in observations[narrative_field] for payload in payloads
        ):
            raise ValueError(
                f"manual review {label} narrative is not anchor-bound for {case_id}"
            )
    if not any(
        token in observations["attribution_rationale"]
        for token in ("source_owned", "compiler_owned", "macro", "conversion")
    ):
        raise ValueError(
            f"manual review attribution rationale is not contract-specific for {case_id}"
        )
    if not any(
        token in observations["capability_rationale"]
        for token in (
            "capability",
            "eligible",
            "ineligible",
            "simulation",
            "source_static",
            "transition_trace",
        )
    ):
        raise ValueError(
            f"manual review capability rationale is not contract-specific for {case_id}"
        )

    elements_by_id = {
        item["element_id"]: item for item in contract.get("elements", [])
    }
    macros_by_id = {
        item["macro_id"]: item for item in contract.get("macros", [])
    }
    positive_trace_sources = {
        source_id
        for entry in contract.get("source_trace_base", {}).get("entries", [])
        for source_id in entry.get("source_elements", [])
    }
    for anchor in observations["plantuml_anchors"]:
        if not any(
            _plantuml_anchor_matches_refs(
                source_text=source_text,
                anchor=anchor,
                source_refs=elements_by_id[source_id].get("source_refs", []),
            )
            for source_id in positive_trace_sources
            if source_id in elements_by_id
        ):
            raise ValueError(
                f"manual review plantuml_anchors are not bound for {case_id}"
            )
    for anchor in observations["fcstm_anchors"]:
        if not any(
            _fcstm_anchor_matches_element(
                fcstm_text=fcstm_text,
                anchor=anchor,
                element_id=element_id,
                elements_by_id=elements_by_id,
                macros_by_id=macros_by_id,
            )
            for element_id in elements_by_id
        ):
            raise ValueError(f"manual review fcstm_anchors are not bound for {case_id}")
    correspondences = review["semantic_correspondences"]
    if len(correspondences) < 2:
        raise ValueError(
            f"manual review lacks two semantic correspondences for {case_id}"
        )
    identities = [
        (
            item["nl_anchor"],
            item["plantuml_anchor"],
            item["fcstm_anchor"],
            tuple(item["source_element_ids"]),
            tuple(item["compiler_element_ids"]),
            item["projection_kind"],
            item["assessment"],
        )
        for item in correspondences
    ]
    if len(identities) != len(set(identities)):
        raise ValueError(f"manual review repeats a semantic correspondence for {case_id}")
    occurrence_identities = [
        (
            item["plantuml_anchor"],
            tuple(item["source_element_ids"]),
        )
        for item in correspondences
    ]
    if len(occurrence_identities) != len(set(occurrence_identities)):
        raise ValueError(
            f"manual review repeats a source semantic occurrence for {case_id}"
        )
    correspondence_anchors = {
        "nl": {item["nl_anchor"] for item in correspondences},
        "plantuml": {item["plantuml_anchor"] for item in correspondences},
        "fcstm": {item["fcstm_anchor"] for item in correspondences},
    }
    for observed_field, correspondence_field, label in (
        ("nl_anchors", "nl", "NL"),
        ("plantuml_anchors", "plantuml", "PlantUML"),
        ("fcstm_anchors", "fcstm", "FCSTM"),
    ):
        if not set(observations[observed_field]).issubset(
            correspondence_anchors[correspondence_field]
        ):
            raise ValueError(
                f"manual review {label} anchors lack semantic correspondence for {case_id}"
            )
    for index, item in enumerate(correspondences):
        if (
            item["nl_anchor"].strip() in GENERIC_REVIEW_ANCHORS
            or item["nl_anchor"] not in nl_text
        ):
            raise ValueError(
                f"semantic correspondence {index} is not source-bound for {case_id}"
            )
        source_ids = item["source_element_ids"]
        compiler_ids = item["compiler_element_ids"]
        if any(
            element_id not in elements_by_id
            or elements_by_id[element_id].get("origin") != "source_owned"
            or element_id not in positive_trace_sources
            for element_id in source_ids
        ):
            raise ValueError(
                f"semantic correspondence {index} lacks positive source identity for {case_id}"
            )
        if any(
            element_id not in elements_by_id
            or elements_by_id[element_id].get("origin") != "compiler_owned"
            for element_id in compiler_ids
        ):
            raise ValueError(
                f"semantic correspondence {index} has invalid compiler ownership for {case_id}"
            )
        if any(
            not _plantuml_anchor_matches_refs(
                source_text=source_text,
                anchor=item["plantuml_anchor"],
                source_refs=elements_by_id[element_id].get("source_refs", []),
            )
            for element_id in source_ids
        ):
            raise ValueError(
                f"semantic correspondence {index} PlantUML anchor is element-misaligned "
                f"for {case_id}"
            )
        expected_compiler_ids = {
            member_id
            for source_id in source_ids
            for macro_id in elements_by_id[source_id].get("macro_ids", [])
            for member_id in macros_by_id.get(macro_id, {}).get(
                "member_element_ids", []
            )
        }
        if not set(compiler_ids).issubset(expected_compiler_ids):
            raise ValueError(
                f"semantic correspondence {index} compiler members are not source-macro-bound "
                f"for {case_id}"
            )
        parsed_anchor = _parse_fcstm_anchor(item["fcstm_anchor"])
        if parsed_anchor is None:
            raise ValueError(
                f"semantic correspondence {index} has invalid FCSTM anchor for {case_id}"
            )
        anchor_id = parsed_anchor[0]
        declared_anchor_ids = set(source_ids) | set(compiler_ids)
        if anchor_id not in declared_anchor_ids:
            raise ValueError(
                f"semantic correspondence {index} FCSTM anchor ownership is undeclared "
                f"for {case_id}"
            )
        if any(
            not _fcstm_anchor_matches_element(
                fcstm_text=fcstm_text,
                anchor=item["fcstm_anchor"],
                element_id=element_id,
                elements_by_id=elements_by_id,
                macros_by_id=macros_by_id,
            )
            for element_id in [*source_ids, *compiler_ids]
        ):
            raise ValueError(
                f"semantic correspondence {index} FCSTM anchor is element-misaligned "
                f"for {case_id}"
            )
        projection = item["projection_kind"]
        assessment = item["assessment"]
        if assessment == "blocked":
            raise ValueError(
                f"blocked semantic correspondence {index} cannot support PASS for {case_id}"
            )
        source_rules = [
            _source_projection_rule(elements_by_id[element_id])
            for element_id in source_ids
        ]
        if any(rule is None for rule in source_rules):
            raise ValueError(
                f"semantic correspondence {index} has an unsupported source kind for {case_id}"
            )
        allowed_pairs = set.intersection(
            *(set(rule["allowed"]) for rule in source_rules if rule is not None)
        )
        if (projection, assessment) not in allowed_pairs:
            raise ValueError(
                f"semantic correspondence {index} projection/assessment contradicts "
                f"source kind or capability for {case_id}"
            )
        compiler_policies = {
            rule["compiler_policy"] for rule in source_rules if rule is not None
        }
        if len(compiler_policies) != 1:
            raise ValueError(
                f"semantic correspondence {index} mixes incompatible source kinds for {case_id}"
            )
        compiler_policy = next(iter(compiler_policies))
        if compiler_policy == "required" and not compiler_ids:
            raise ValueError(
                f"semantic correspondence {index} requires a compiler projection for {case_id}"
            )
        if compiler_policy == "forbidden" and compiler_ids:
            raise ValueError(
                f"semantic correspondence {index} exposes an inapplicable compiler "
                f"projection for {case_id}"
            )
        rationale = item["rationale"]
        if not any(element_id in rationale for element_id in source_ids):
            raise ValueError(
                f"semantic correspondence {index} rationale lacks source identity for {case_id}"
            )
        if any(phrase in rationale.lower() for phrase in SHALLOW_REVIEW_PHRASES):
            raise ValueError(
                f"semantic correspondence {index} is a shallow attestation for {case_id}"
            )

    if any(
        review[field] != "pass"
        for field in (
            "ownership_verdict",
            "macro_verdict",
            "capability_verdict",
            "verdict",
        )
    ):
        raise ValueError(f"manual review is not PASS for {case_id}")
    required_second_pass = contract["review_subject"]["second_pass_required"]
    second_pass = review["second_pass"]
    if second_pass["required"] != required_second_pass:
        raise ValueError(f"manual second-pass requirement drift for {case_id}")
    if required_second_pass and not second_pass["completed"]:
        raise ValueError(f"required second pass is incomplete for {case_id}")
    if required_second_pass:
        risk_tags = contract["review_subject"]["risk_tags"]
        obligations = contract["review_subject"]["review_obligations"]
        assessments = second_pass["risk_assessments"]
        if (
            second_pass["review_subject_sha256"] != review_subject_sha256
            or second_pass["reviewer_id"] != "main_session_llm"
            or second_pass["review_method"]
            != "risk_focused_independent_second_pass"
            or second_pass["risk_tags_reviewed"] != risk_tags
            or [item["obligation_id"] for item in assessments]
            != [item["obligation_id"] for item in obligations]
            or not isinstance(second_pass["observations"], str)
            or len(second_pass["observations"].strip()) < 20
            or any(tag not in second_pass["observations"] for tag in risk_tags)
            or len(second_pass["notes"].strip()) < 20
        ):
            raise ValueError(
                f"required second pass is not evidence-bound for {case_id}"
            )
        for item, obligation in zip(assessments, obligations):
            if item["risk_tag"] != obligation["risk_tag"]:
                raise ValueError(
                    f"second-pass risk-tag binding drift for {case_id}: "
                    f"{item['obligation_id']}"
                )
            if item["element_ids"] != obligation["element_ids"]:
                raise ValueError(
                    f"second-pass ownership occurrence drift for {case_id}: "
                    f"{item['obligation_id']}"
                )
            expected_assessment = RISK_ASSESSMENT_BY_TAG.get(item["risk_tag"])
            if expected_assessment is None or item["assessment"] != expected_assessment:
                raise ValueError(
                    f"second-pass assessment is incompatible with risk occurrence for "
                    f"{case_id}: {item['obligation_id']}"
                )
            if not obligation["source_refs"] or any(
                not any(
                    _plantuml_anchor_matches_refs(
                        source_text=source_text,
                        anchor=anchor,
                        source_refs=[source_ref],
                    )
                    for anchor in item["plantuml_anchors"]
                )
                for source_ref in obligation["source_refs"]
            ):
                raise ValueError(
                    f"second-pass PlantUML evidence is occurrence-misaligned for {case_id}: "
                    f"{item['obligation_id']}"
                )
            fcstm_not_applicable = item["risk_tag"] == "source_normalization"
            if fcstm_not_applicable and item["fcstm_anchors"]:
                raise ValueError(
                    f"second-pass FCSTM evidence must be empty for source normalization "
                    f"in {case_id}: {item['obligation_id']}"
                )
            if fcstm_not_applicable:
                normalization_elements = [
                    elements_by_id[element_id]
                    for element_id in item["element_ids"]
                    if element_id in elements_by_id
                ]
                if any(
                    element.get("kind") != "source_normalization"
                    or any(
                        not isinstance(element.get("metadata", {}).get(field), str)
                        or element["metadata"][field] not in item["rationale"]
                        for field in ("rule_id", "before", "after")
                    )
                    for element in normalization_elements
                ):
                    raise ValueError(
                        f"second-pass normalization evidence lacks exact rule/before/after "
                        f"binding for {case_id}: {item['obligation_id']}"
                    )
            if not fcstm_not_applicable and (
                not item["fcstm_anchors"]
                or any(
                    not any(
                        _fcstm_anchor_matches_element(
                            fcstm_text=fcstm_text,
                            anchor=anchor,
                            element_id=element_id,
                            elements_by_id=elements_by_id,
                            macros_by_id=macros_by_id,
                        )
                        for anchor in item["fcstm_anchors"]
                    )
                    for element_id in item["element_ids"]
                )
            ):
                raise ValueError(
                    f"second-pass FCSTM evidence is occurrence-misaligned for {case_id}: "
                    f"{item['obligation_id']}"
                )
            if any(element_id not in elements_by_id for element_id in item["element_ids"]):
                raise ValueError(
                    f"second-pass ownership evidence is not bound for {case_id}: "
                    f"{item['risk_tag']}"
                )
            if (
                item["risk_tag"] not in item["rationale"]
                or item["obligation_id"] not in item["rationale"]
                or any(
                    phrase in item["rationale"].lower()
                    for phrase in SHALLOW_REVIEW_PHRASES
                )
            ):
                raise ValueError(
                    f"second-pass rationale is shallow for {case_id}: "
                    f"{item['risk_tag']}"
                )
    elif (
        second_pass["completed"]
        or any(
            second_pass[field] is not None
            for field in (
                "review_subject_sha256",
                "reviewer_id",
                "review_method",
                "observations",
            )
        )
        or second_pass["risk_tags_reviewed"]
        or second_pass["risk_assessments"]
    ):
        raise ValueError(f"unexpected second-pass evidence for {case_id}")
    blocking = [
        finding for finding in review["findings"] if finding["severity"] in {"C", "I"}
    ]
    if blocking:
        raise ValueError(
            f"manual review has blocking findings for {case_id}: {blocking}"
        )
