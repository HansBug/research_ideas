from __future__ import annotations

from typing import Any

from paper_stm_feedback_loop.assertions import get_assertion_environment_api_docs

from .schemas import (
    AssertionCheckPublic,
    AssertionScript,
    AttributionProjection,
    CoverageGap,
    FrozenDiscoverInputs,
    ReleasedAssertionResults,
    RequirementCoverageProjection,
    RequirementSet,
    RevisionFeedback,
    RevisionLedgerEvent,
)
from .utils import prompt_json, sha256_data


def _model_vocabulary(frozen: FrozenDiscoverInputs) -> dict[str, Any]:
    """Hand the producers the exact declared paths they must bind against.

    They previously received only the raw FCSTM text plus diagnostics, so every
    state and event name had to be re-derived by reading the DSL.  A single
    mistyped event makes an assertion vacuously true rather than failing loudly,
    which is how pair 0029 lost a real defect.  Listing the vocabulary removes
    the need to guess.
    """

    vocabulary = frozen.model_vocabulary or {}
    compiler_owned = list(
        vocabulary.get("compiler_owned_variables_not_usable_as_evidence") or ()
    )
    payload: dict[str, Any] = {
        "note": (
            "Exact declared paths. predicate_bindings and assertion expressions "
            "must use these verbatim; a name absent from these lists does not "
            "exist in the model."
        ),
        "states": list(vocabulary.get("states") or ()),
        "events": list(vocabulary.get("events") or ()),
        "variables": list(vocabulary.get("variables") or ()),
    }
    if compiler_owned:
        # Shown, not hidden: the producer will see these names in the FCSTM text
        # and needs to know why they are not on the list above.  An empty
        # `variables` next to a populated one of these is the honest statement
        # that the model has no variable of the author's own -- which for a
        # quantity the NL names is the finding.
        payload["compiler_owned_variables"] = compiler_owned
        payload["compiler_owned_variables_note"] = (
            "Created by the converter for its own routing, not by the model's "
            "author. The evidence layer drops them from every effect answer, so "
            "binding one proves nothing about a quantity the NL names. If the NL "
            "requires a quantity and `variables` above is empty, this model has no "
            "variable of its own to carry it: name the variable it should have "
            "declared and assert that name's existence, rather than binding one of "
            "these."
        )
    return payload


def _source_context(frozen: FrozenDiscoverInputs) -> dict[str, Any]:
    """Return a compact, input-derived source-scope view for LLM nodes."""

    trace = frozen.source_trace if isinstance(frozen.source_trace, dict) else {}
    raw_entries = trace.get("entries", [])
    entries = raw_entries if isinstance(raw_entries, list) else []
    projected_entries = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        boundary = entry.get("attribution_boundary")
        boundary = boundary if isinstance(boundary, dict) else {}
        projected_entries.append(
            {
                "trace_id": entry.get("trace_id"),
                "intermediate_elements": entry.get("intermediate_elements", []),
                "source_elements": entry.get("source_elements", []),
                "source_level_claim_allowed": boundary.get(
                    "source_level_claim_allowed"
                ),
                "representation_related": boundary.get("representation_related"),
                "conversion_or_lowering_related": boundary.get(
                    "conversion_or_lowering_related"
                ),
            }
        )
    contract = (
        frozen.working_contract if isinstance(frozen.working_contract, dict) else {}
    )
    contract_summary = contract.get("summary", {})
    contract_summary = contract_summary if isinstance(contract_summary, dict) else {}
    raw_exclusions = trace.get("attribution_exclusions", [])
    exclusions = raw_exclusions if isinstance(raw_exclusions, list) else []
    return {
        "trace_scope": trace.get("trace_scope"),
        "schema_version": trace.get("schema_version"),
        "entry_count": len(entries),
        "attribution_exclusion_count": len(exclusions),
        "closure_claim_allowed": (
            (trace.get("source_traceability") or {}).get("closure_claim_allowed")
            if isinstance(trace.get("source_traceability"), dict)
            else None
        ),
        "entries": projected_entries,
        "working_contract_summary": {
            key: contract_summary.get(key)
            for key in (
                "simulation_status",
                "source_static_discovery_status",
                "diagnostic_binding_status",
            )
            if key in contract_summary
        },
    }


def _revision_ledger_payload(
    events: tuple[RevisionLedgerEvent, ...], current_revision: int | None
) -> list[dict[str, Any]]:
    """Render reconstructable history without duplicating the current artifact."""

    payload = []
    for event in events:
        item = event.model_dump(mode="json")
        if (
            event.event in {"artifact_created", "artifact_rejected"}
            and event.revision == current_revision
        ):
            item["artifact_delta"] = {
                "omitted": "current artifact is supplied in full beside this ledger"
            }
        payload.append(item)
    return payload


def render_requirement_split_input(
    frozen: FrozenDiscoverInputs,
    current_result: RequirementSet | None = None,
    revision_feedback: RevisionFeedback | None = None,
    revision_ledger: tuple[RevisionLedgerEvent, ...] = (),
) -> str:
    payload: dict[str, Any] = {
        "natural_language": frozen.natural_language,
        "nl_segments": frozen.nl_segments,
        "stm_text": frozen.stm_text,
        "inspect_digest": frozen.inspect_digest,
        "declared_model_vocabulary": _model_vocabulary(frozen),
        "source_context": _source_context(frozen),
        "mode": "revise" if current_result else "create",
        "content_language": frozen.language,
        "revision_ledger": _revision_ledger_payload(
            revision_ledger,
            current_result.revision if current_result is not None else None,
        ),
    }
    if current_result is not None:
        payload["current_result"] = current_result.model_dump(mode="json")
        payload["revision_feedback"] = (
            revision_feedback.model_dump(mode="json") if revision_feedback else None
        )
    return prompt_json(payload)


def render_requirement_review_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    coverage: RequirementCoverageProjection,
    previous_feedback: RevisionFeedback | None = None,
    revision_ledger: tuple[RevisionLedgerEvent, ...] = (),
) -> str:
    return prompt_json(
        {
            "natural_language": frozen.natural_language,
            "nl_segments": frozen.nl_segments,
            "stm_text": frozen.stm_text,
            "requirements": requirements.model_dump(mode="json"),
            "coverage_projection": coverage.model_dump(mode="json"),
            # The reviewer is asked to reject bindings that do not name declared
            # paths, so it needs the same vocabulary the splitter was given.
            "declared_model_vocabulary": _model_vocabulary(frozen),
            "source_context": _source_context(frozen),
            "previous_revision_feedback": (
                previous_feedback.model_dump(mode="json")
                if previous_feedback is not None
                else None
            ),
            "content_language": frozen.language,
            "revision_ledger": _revision_ledger_payload(
                revision_ledger, requirements.revision
            ),
        }
    )


def render_assertion_conversion_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    current_result: AssertionScript | None = None,
    revision_feedback: RevisionFeedback | None = None,
    revision_ledger: tuple[RevisionLedgerEvent, ...] = (),
) -> str:
    payload: dict[str, Any] = {
        "accepted_requirements": requirements.model_dump(mode="json"),
        "stm_text": frozen.stm_text,
        "inspect_digest": frozen.inspect_digest,
        "declared_model_vocabulary": _model_vocabulary(frozen),
        "source_context": _source_context(frozen),
        "evidence_api": get_assertion_environment_api_docs(),
        "mode": "revise" if current_result else "create",
        "content_language": frozen.language,
        "revision_ledger": _revision_ledger_payload(
            revision_ledger,
            current_result.revision if current_result is not None else None,
        ),
    }
    if current_result is not None:
        payload["current_result"] = current_result.model_dump(mode="json")
        payload["revision_feedback"] = (
            revision_feedback.model_dump(mode="json") if revision_feedback else None
        )
    return prompt_json(payload)


def render_assertion_review_input(
    frozen: FrozenDiscoverInputs,
    requirements: RequirementSet,
    script: AssertionScript,
    public_check: AssertionCheckPublic,
    revision_ledger: tuple[RevisionLedgerEvent, ...] = (),
    coverage_gaps: tuple[CoverageGap, ...] = (),
) -> str:
    # This payload intentionally excludes sealed and released assertion results.
    return prompt_json(
        {
            "natural_language": frozen.natural_language,
            "stm_text": frozen.stm_text,
            "accepted_requirements": requirements.model_dump(mode="json"),
            "assertion_script": script.model_dump(mode="json"),
            "reviewed_script_hash": sha256_data(script),
            "public_check": public_check.model_dump(mode="json"),
            "evidence_api": get_assertion_environment_api_docs(),
            "content_language": frozen.language,
            "coverage_gaps": [
                gap.model_dump(mode="json") for gap in coverage_gaps
            ],
            "revision_ledger": _revision_ledger_payload(
                revision_ledger, script.revision
            ),
        }
    )


def render_adjudicator_input(
    requirements: RequirementSet,
    script: AssertionScript,
    released: ReleasedAssertionResults,
    attribution: AttributionProjection,
    coverage_gaps: tuple[CoverageGap, ...] = (),
) -> str:
    return prompt_json(
        {
            "accepted_requirements": requirements.model_dump(mode="json"),
            "assertion_script": script.model_dump(mode="json"),
            "strict_bool_results": released.model_dump(mode="json"),
            "safe_attribution": attribution.model_dump(mode="json"),
            "coverage_gaps": [gap.model_dump(mode="json") for gap in coverage_gaps],
        }
    )
