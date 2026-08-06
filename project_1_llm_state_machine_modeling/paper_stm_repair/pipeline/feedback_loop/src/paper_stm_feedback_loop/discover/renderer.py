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
    # What the model says through `[*]`, which has no name and so appears in none
    # of the lists above.  Without it a producer reading this block concludes the
    # model cannot terminate and proposes a `FinalState`; pair 0050 did that twice
    # on a model that terminates correctly.  These two keys are what the four-step
    # procedure's step 1 reads.
    facts = frozen.pseudo_state_facts or {}
    # Full rows only for the edges a claim can be built on.  The rest exist to
    # answer one question -- "the model text shows `X -> [*]` here, why is that not
    # termination?" -- and a per-scope tally answers it in a line.  Spelled out, pair
    # 0029's 36 exit rows added 8.5 KB to a 2 KB vocabulary, and its requirement
    # splitter is the one call in the corpus whose response the gateway truncates.
    rows = list(facts.get("terminating_transitions") or ())
    payload["terminating_transitions"] = [row for row in rows if row.get("ends_run")]
    exits: dict[str, int] = {}
    for row in rows:
        if not row.get("ends_run"):
            exits[str(row.get("exits_scope") or "")] = (
                exits.get(str(row.get("exits_scope") or ""), 0) + 1
            )
    payload["composite_exits_not_terminating"] = [
        {"exits_scope": scope, "edges": count} for scope, count in sorted(exits.items())
    ]
    payload["terminating_transitions_note"] = (
        "Every `-> [*]` edge the model declares. `[*]` leaves whatever scope owns "
        "the source, so it ends the run only when that scope is the root -- read "
        "`ends_run`, not the arrow. `ends_run: true` means a requirement about "
        "finishing, ending or shutting down is answered by `terminates` over that "
        "source and trigger; there is no state to bind, so proposing a `FinalState` "
        "name reports a defect against a model that is correct. `ends_run: false` "

        "`via_token` records the two-edge form the converter emits: the inner exit "
        "sets a route token and an outer edge ends the run on it. Every other `-> [*]` "
        "edge is tallied per scope under `composite_exits_not_terminating`: those "
        "leave a composite and route onward, so a completion claim over one is a "
        "reachability question (`occupancy_after` / `reaches`) about a declared "
        "state, not `terminates`. If this list is empty, nothing ends the run -- a completion claim is then about "
        "reaching a declared state, or, when no declared state carries the "
        "sentence's completion notion at all, step 4 applies and you propose the "
        "name."
    )
    payload["initial_entries"] = list(facts.get("initial_entries") or ())
    payload["initial_entries_note"] = (
        "Declared entries per composite. Entry takes an `unconditional` edge when "
        "one exists; a guarded or triggered entry is only taken when its condition "
        "already holds. `initial_target` claims are decided against this, with two "
        "cases that are not what they look like.\n"
        "`converter_generated: true` marks a target the converter inserted, not one "
        "the author chose. It is unconditional *because* no author entry was, so it "
        "is the converter's fallback rather than the model's answer to \"where does "
        "this composite start\". Do not bind it as the entry the NL names: state "
        "the claim about the state the NL names, whose `initial_target` then "
        "answers False -- and that False is the finding, since the model gives the "
        "author's entry a guard and the default to a generated holder.\n"
        "When a composite lists two or more entries and none is unconditional, "
        "`initial_target` cannot answer at all and raises. State *that* claim -- the "
        "entry claim, nothing else -- as "
        "`edge_declared(source=\"[*]\", trigger=..., target=...)` for the "
        "declaration or `occupancy_after(source=\"[*]\", ...)` for the behaviour, "
        "and pick that predicate in the Requirement, since the predicate is frozen "
        "before the assertion stage.\n"
        "`[*]` is an entry anchor and only that. Do not carry it into a requirement "
        "about a phase the machine is already running in: a termination claim bound "
        "to `source=\"[*]\"` asks whether the run ends *from power-on*, and if the model "
        "happens to be wrong in that configuration the answer comes back true for a "
        "reason the sentence never asked about. Name the running state instead, one requirement per state the "
        "sentence ranges over."
    )
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


#: Content digests carried through `check_detail` for replay verification. They are about
#: two thirds of the adjudicator's payload and there is nothing a reader can do with them --
#: unlike `kwargs` and `model_refs` in the same structure, which hold the resolved predicate
#: arguments and are often the only place a shared element such as `Power_Off` is visible
#: (`source_refs` carries states alone).
_OPAQUE_DIGEST_KEYS = frozenset(
    {
        "args_hash",
        "kwargs_hash",
        "result_hash",
        "namespace_hash_before",
        "namespace_hash_after",
        "expression_sha256",
        "ported_source_commit",
    }
)


def _without_digests(value: Any) -> Any:
    """Drop content digests, keeping everything a reader could reason about.

    Rendering-time only: `bind_attribution` reads `check_detail.function_call_trace` and
    `actual_function_families` off the stored results, so the results themselves are left
    exactly as released. Attribution is where three of the eight-cell misses already sit;
    it must not acquire a fourth from a display concern.
    """
    if isinstance(value, dict):
        return {
            key: _without_digests(item)
            for key, item in value.items()
            if key not in _OPAQUE_DIGEST_KEYS
            and not (key.endswith("_sha256") or key.endswith("_hash"))
        }
    if isinstance(value, list):
        return [_without_digests(item) for item in value]
    return value


#: How a released result is allowed to be dispositioned, derived from role and attribution.
#: The rule is already in the prompt; carrying it per-result puts it where the adjudicator is
#: looking when it decides. A supporting False was placed in `issues` once across the eight
#: cells -- the deterministic layer trimmed it, but the rationale kept citing the trimmed id.
_DISPOSITION_HINTS = {
    "may_become_issue": "primary/precondition False with safe attribution",
    "excluded_only": "primary/precondition False that attribution could not make safe",
    "observation_only": "supporting evidence: never an issue, never an excluded finding",
}


def _disposition_hint(role: str, truth_value: bool | None, status: str | None) -> str:
    if role == "supporting":
        return "observation_only"
    if truth_value is False and status == "safe":
        return "may_become_issue"
    if truth_value is False:
        return "excluded_only"
    return "observation_only"


def _merge_candidates(
    requirements: RequirementSet,
    mergeable_requirement_ids: set[str],
) -> list[dict[str, Any]]:
    """Requirement pairs that differ only in `source`, computed rather than guessed.

    A specification sentence that never says which mode it applies to becomes one Requirement
    per mode, because `occupancy_after` needs a concrete `source`. When they then share a
    predicate, trigger and target, the same model element is under test from two directions
    and one defect can explain both.

    Two limits, both deliberate. The pairs are scoped to Requirements that could actually
    become issues -- unscoped, pair 0029 yields thirteen candidates whose counterparts have
    no safe-False assertion, which could never merge and would only make the adjudicator's
    acceptance rate unreadable. And the rule is narrow: on pair 0029 the two Requirements
    that genuinely belong together use different predicates, so it returns nothing for them.
    It is a hint to check, not a grouping to apply.
    """
    keyed: dict[tuple[str, str, str], list[str]] = {}
    for requirement in requirements.requirements:
        if requirement.requirement_id not in mergeable_requirement_ids:
            continue
        bindings = requirement.predicate_bindings or {}
        trigger, target = bindings.get("trigger"), bindings.get("target")
        source = bindings.get("source")
        if not trigger or not target or not source:
            continue
        keyed.setdefault(
            (str(requirement.checkability), str(trigger), str(target)), []
        ).append(requirement.requirement_id)
    return [
        {
            "requirement_ids": sorted(ids),
            "shared_bindings": {"trigger": trigger, "target": target},
            "differs_in": "source",
        }
        for (_checkability, trigger, target), ids in sorted(keyed.items())
        if len(ids) > 1
    ]


def render_adjudicator_input(
    requirements: RequirementSet,
    script: AssertionScript,
    released: ReleasedAssertionResults,
    attribution: AttributionProjection,
    coverage_gaps: tuple[CoverageGap, ...] = (),
    *,
    stm_text: str = "",
) -> str:
    """Everything needed to decide whether two failures are one defect.

    `stm_text` is new here and is safe to supply precisely because this role cannot overturn
    anything: which assertions exist, which are False, and which may become issues are all
    settled before this call, and the closure check in `adjudicate_results` rejects any
    response that changes them. What the model buys is the ability to check a claimed shared
    element against the artefact instead of asserting it.
    """
    status_by_assertion = {
        binding.assertion_id: binding.status for binding in attribution.bindings
    }
    role_by_assertion = {
        assertion.assertion_id: assertion.role for assertion in script.assertions
    }
    results = released.model_dump(mode="json")
    mergeable: set[str] = set()
    for result in results.get("results", []):
        assertion_id = result.get("assertion_id")
        role = role_by_assertion.get(assertion_id, result.get("role") or "primary")
        status = status_by_assertion.get(assertion_id)
        hint = _disposition_hint(role, result.get("truth_value"), status)
        result["disposition_hint"] = hint
        if hint == "may_become_issue":
            mergeable.add(str(result.get("requirement_id")))
    return prompt_json(
        {
            "stm_text": stm_text,
            "accepted_requirements": requirements.model_dump(mode="json"),
            "assertion_script": script.model_dump(mode="json"),
            "strict_bool_results": _without_digests(results),
            "safe_attribution": attribution.model_dump(mode="json"),
            "merge_candidates": _merge_candidates(requirements, mergeable),
            "disposition_hint_legend": _DISPOSITION_HINTS,
            "coverage_gaps": [gap.model_dump(mode="json") for gap in coverage_gaps],
        }
    )
