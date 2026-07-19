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
    return lines[line_number - 1]


def _plantuml_anchor_matches_refs(
    *, source_text: str, anchor: str, source_refs: list[str]
) -> bool:
    lines = [
        line
        for reference in source_refs
        if (line := _source_line_for_ref(source_text, reference)) is not None
    ]
    return bool(lines) and any(anchor in line or line.strip() in anchor for line in lines)


def _projection_evidence(
    *,
    element_id: str,
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> tuple[set[str], set[str]]:
    literals: set[str] = set()
    identifiers: set[str] = set()
    visited: set[str] = set()

    def visit(current_id: str) -> None:
        if current_id in visited or current_id not in elements_by_id:
            return
        visited.add(current_id)
        element = elements_by_id[current_id]
        metadata = element.get("metadata", {})
        semantic_fields = element.get("semantic_fields", {})
        line = metadata.get("line")
        if isinstance(line, str) and line.strip():
            literals.add(line.strip())
        for field in ("text", "raw_label"):
            value = metadata.get(field) or semantic_fields.get(field)
            if isinstance(value, str) and len(value.strip()) >= 4:
                literals.add(value.strip())
        raw_ref = metadata.get("raw_ref")
        if isinstance(raw_ref, str) and raw_ref.strip():
            literals.add(raw_ref.strip())
        if element.get("kind") == "concurrent_region":
            region_index = metadata.get("region_index")
            if isinstance(region_index, int):
                literals.add(f"[PlantUML concurrent region {region_index}]")
        for field in ("fcstm_identifier", "fcstm_path"):
            value = semantic_fields.get(field) or metadata.get(field)
            if isinstance(value, str) and value.strip():
                identifiers.add(value.rsplit(".", 1)[-1])
        for model_ref in element.get("model_refs", []):
            if not isinstance(model_ref, str) or ":" not in model_ref:
                continue
            kind, value = model_ref.split(":", 1)
            if kind in {"state", "event"} and value:
                identifiers.add(value.rsplit(".", 1)[-1])
        for macro_id in element.get("macro_ids", []):
            macro = macros_by_id.get(macro_id, {})
            for member_id in macro.get("member_element_ids", []):
                visit(member_id)

    visit(element_id)
    return literals, identifiers


def _fcstm_anchor_matches_element(
    *,
    anchor: str,
    element_id: str,
    elements_by_id: dict[str, dict[str, Any]],
    macros_by_id: dict[str, dict[str, Any]],
) -> bool:
    literals, identifiers = _projection_evidence(
        element_id=element_id,
        elements_by_id=elements_by_id,
        macros_by_id=macros_by_id,
    )
    if any(literal in anchor or anchor in literal for literal in literals):
        return True
    return any(
        re.search(rf"(?<![A-Za-z0-9_]){re.escape(identifier)}(?![A-Za-z0-9_])", anchor)
        for identifier in identifiers
    )


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
    for field, text in (
        ("nl_anchors", nl_text),
        ("plantuml_anchors", source_text),
        ("fcstm_anchors", fcstm_text),
    ):
        anchors = observations[field]
        if not anchors or any(
            len(anchor.strip()) < 4
            or anchor.strip() in GENERIC_REVIEW_ANCHORS
            or anchor not in text
            for anchor in anchors
        ):
            raise ValueError(f"manual review {field} are not bound for {case_id}")
    for anchor_field, narrative_field, label in (
        ("nl_anchors", "nl_intent", "NL"),
        ("plantuml_anchors", "plantuml_semantics", "PlantUML"),
        ("fcstm_anchors", "fcstm_projection", "FCSTM"),
    ):
        if not any(
            anchor in observations[narrative_field]
            for anchor in observations[anchor_field]
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
        if any(
            anchor.strip() in GENERIC_REVIEW_ANCHORS or anchor not in text
            for anchor, text in (
                (item["nl_anchor"], nl_text),
                (item["plantuml_anchor"], source_text),
                (item["fcstm_anchor"], fcstm_text),
            )
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
        if any(
            not _fcstm_anchor_matches_element(
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
        if projection == "direct" and compiler_ids:
            raise ValueError(
                f"direct semantic correspondence {index} exposes compiler members for {case_id}"
            )
        if projection == "macro" and not compiler_ids:
            raise ValueError(
                f"macro semantic correspondence {index} lacks compiler members for {case_id}"
            )
        if projection == "capability_excluded" and assessment == "preserved":
            raise ValueError(
                f"capability-excluded correspondence {index} overclaims preservation for {case_id}"
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
            if any(
                not any(
                    _fcstm_anchor_matches_element(
                        anchor=anchor,
                        element_id=element_id,
                        elements_by_id=elements_by_id,
                        macros_by_id=macros_by_id,
                    )
                    for anchor in item["fcstm_anchors"]
                )
                for element_id in item["element_ids"]
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
