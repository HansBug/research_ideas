from __future__ import annotations

import hashlib
import json
from typing import Any

_LIMITATIONS = [
    "mechanical_eligibility_only",
    "nl_alignment_not_proven",
    "coverage_completeness_not_proven",
    "bounded_obligations_only",
]
_BAD_OBLIGATION_STATUSES = {"unknown", "timeout", "incomplete", "replay_mismatch", "error", "execution_error", "tool_unavailable"}
_SUPPORTED_KINDS = {"scenario", "property", "static_consistency"}
_SUPPORTED_STATIC_SPECS = {
    "diagnostic_expectation",
    "transition_shape",
    "forced_transition_shape",
    "state_shape",
    "state_label_scopes",
}


def _sha256_json(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def _valid_binding_ref(ref: Any, inspect: dict[str, Any]) -> bool:
    if not isinstance(ref, str):
        return False
    if ref.startswith("state:"):
        return ref.removeprefix("state:") in {item.get("path") for item in inspect.get("states", []) if isinstance(item, dict)}
    if ref.startswith("event:"):
        event = ref.removeprefix("event:")
        return event in {item.get("qualified_name") for item in inspect.get("events", []) if isinstance(item, dict)} or event in {item.get("name") for item in inspect.get("events", []) if isinstance(item, dict)}
    if ref.startswith("variable:"):
        variable = ref.removeprefix("variable:")
        return variable in {item.get("name") for item in inspect.get("variables", []) if isinstance(item, dict)} or variable in {item.get("qualified_name") for item in inspect.get("variables", []) if isinstance(item, dict)}
    if ref.startswith("transition:"):
        raw = ref.removeprefix("transition:")
        if raw.startswith("T") and raw[1:].isdigit():
            raw = raw[1:]
        try:
            index = int(raw)
        except ValueError:
            return False
        return any(item.get("transition_index") == index for item in inspect.get("transitions", []) if isinstance(item, dict))
    if ref.startswith("forced_transition:"):
        raw = ref.removeprefix("forced_transition:")
        return raw in {item.get("original_raw") for item in inspect.get("forced_transitions", []) if isinstance(item, dict)}
    return False


def _executable_spec_ok(check_kind: Any, spec: Any) -> bool:
    if not isinstance(spec, dict) or not spec:
        return False
    if check_kind == "scenario":
        events = spec.get("events")
        return (
            isinstance(events, list)
            and bool(events)
            and all(isinstance(event, str) and bool(event) for event in events)
            and not spec.get("unbound_event_labels")
            and isinstance(spec.get("precondition_state"), str)
            and bool(spec["precondition_state"])
            and not spec.get("unbound_precondition_state_label")
            and spec.get("tested_event") == events[-1]
            and spec.get("setup_events") == events[:-1]
        )
    if check_kind == "property":
        if spec.get("kind") == "state_shape":
            state = spec.get("state")
            expect = spec.get("expect")
            return isinstance(state, str) and bool(state) and isinstance(expect, dict) and bool(expect)
        query = spec.get("query") or spec.get("fbmcq")
        return isinstance(query, str) and bool(query.strip())
    if check_kind == "static_consistency":
        kind = spec.get("kind")
        if kind not in _SUPPORTED_STATIC_SPECS:
            return False
        if kind == "diagnostic_expectation":
            return (
                isinstance(spec.get("code"), str)
                and bool(spec["code"])
                and isinstance(spec.get("expect_count"), int)
                and spec["expect_count"] >= 0
            )
        if kind == "transition_shape":
            return isinstance(spec.get("transition_index"), int) and isinstance(spec.get("expect"), dict) and bool(spec["expect"])
        if kind == "forced_transition_shape":
            return isinstance(spec.get("expect"), dict) and bool(spec["expect"])
        if kind == "state_shape":
            return isinstance(spec.get("state_path"), str) and bool(spec["state_path"]) and isinstance(spec.get("expect"), dict) and bool(spec["expect"])
        return (
            isinstance(spec.get("state_paths"), list)
            and bool(spec["state_paths"])
            and all(isinstance(path, str) and bool(path) for path in spec["state_paths"])
            and isinstance(spec.get("expected_scope_labels"), list)
            and bool(spec["expected_scope_labels"])
        )
    return False


def _property_result_obligation(result: dict[str, Any]) -> dict[str, Any]:
    """Project one bounded BMC result into a mechanical execution obligation."""

    status = str(result.get("status") or result.get("execution_status") or "unknown")
    solver_status = str(result.get("solver_status") or "unknown")
    timeout = bool(result.get("timeout") or status == "timeout")
    incomplete = bool(result.get("incomplete") or status == "incomplete")
    property_satisfied = result.get("property_satisfied")
    witness = result.get("witness")
    replay = result.get("replay")
    replay_required = witness is not None
    replay_ok = None if replay is None else bool(isinstance(replay, dict) and replay.get("ok") is True)

    if timeout:
        obligation_status = "timeout"
    elif incomplete:
        obligation_status = "incomplete"
    elif status in _BAD_OBLIGATION_STATUSES or solver_status in {"unknown", "error", "execution_error"}:
        obligation_status = status if status in _BAD_OBLIGATION_STATUSES else solver_status
    elif not isinstance(property_satisfied, bool):
        obligation_status = "unknown"
    elif replay_required and replay_ok is not True:
        obligation_status = "replay_mismatch" if replay is not None else "missing"
    else:
        # Completion here means only that the bounded query ran with a stable
        # result. Expected-outcome agreement remains Discover evidence and is
        # deliberately excluded from mechanical eligibility.
        obligation_status = "completed"

    return {
        "kind": "bounded_property_execution",
        "status": obligation_status,
        "query_hash": result.get("query_sha256") or _sha256_json(result.get("query")),
        "solver_status": solver_status,
        "property_satisfied_observed": isinstance(property_satisfied, bool),
        "replay_required": replay_required,
        "replay": replay,
        "replay_ok": replay_ok,
        "evidence_scope": "bounded_mechanical_execution_only",
    }


def _obligations_for(
    check: dict[str, Any],
    property_results: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    supplied = check.get("obligation_results")
    if isinstance(supplied, list):
        obligations = [item if isinstance(item, dict) else {"status": "error", "raw": str(item)} for item in supplied]
    elif check.get("check_kind") == "property":
        result = property_results.get(str(check.get("check_id")))
        if result is not None:
            obligations = [_property_result_obligation(result)]
        else:
            spec = check.get("executable_spec") or {}
            query = spec.get("query") or spec.get("fbmcq") if isinstance(spec, dict) else None
            obligations = [{"kind": "bounded_property_execution", "status": "not_run", "query_sha256": hashlib.sha256(str(query or "").encode("utf-8")).hexdigest()}]
    else:
        obligations = []
    normalized = []
    for item in obligations:
        status = str(item.get("status") or item.get("execution_status") or "unknown")
        replay = item.get("replay")
        replay_ok = None if replay is None else bool(isinstance(replay, dict) and replay.get("ok") is True)
        if replay_ok is False and status not in _BAD_OBLIGATION_STATUSES:
            status = "replay_mismatch"
        normalized.append({**item, "status": status, "query_hash": item.get("query_hash") or item.get("query_sha256") or _sha256_json(item), "replay_ok": replay_ok})
    return normalized


def _obligations_ok(obligations: list[dict[str, Any]]) -> bool:
    for item in obligations:
        status = item.get("status")
        if status in _BAD_OBLIGATION_STATUSES or status in {"not_run", "missing"}:
            return False
        if item.get("replay_ok") is False:
            return False
    return True


def execute(
    checks: list[dict[str, Any]],
    check_result: dict[str, Any],
    property_evidence: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Purpose: validate Discover check objects for mechanical binding, definedness, executability, and bounded obligation safety only.

    Parameters: ``checks`` is the controller-held immutable candidate
    ``issue_checks[]`` list. Each object should include ``check_id``,
    ``check_kind`` (``scenario``, ``property``, or ``static_consistency``),
    ``binding_refs``, ``source_basis``, ``expected_outcome``,
    ``executable_spec``, and ``required``. ``check_result`` is the current
    ``check_fcstm`` result for the same model/hash and is controller-bound; an
    Agent cannot provide arbitrary paths, model text, run/case selectors, solver
    code, URLs, or reference/gold inputs. ``property_evidence`` is the separate
    controller-produced ``verify_properties`` result for the same immutable
    check batch. It is joined by ``check_id`` and never written back into the
    sealed checks. Optional check-local ``obligation_results`` remain a test and
    compatibility input for bounded non-vacuity/replay facts.

    Returns: ``execution_status=completed``, overall ``mechanically_eligible``,
    per-check records with ``binding_status``, ``definedness_status``,
    ``executability_status``, ``non_vacuity_obligations``, and
    ``mechanically_eligible``, plus ``model_executable`` and explicit
    ``limitations``. The output deliberately contains no semantic correctness,
    coverage sufficiency, strength, quality, or effectiveness verdict.

    Execution: reads only the structured inspect facts from ``check_result``,
    resolves typed refs against states/events/variables/transitions, checks stable
    check ids and supported kinds, verifies that required executable specs are
    present in a supported check-kind-specific shape (including rejection of
    partially bound scenario event lists), joins current-run bounded property evidence, normalizes the bounded
    obligations, and fails eligibility for ``unknown``, ``timeout``,
    ``incomplete``, ``replay_mismatch``, errors, or missing required obligations.
    SAT evidence with a decoded witness requires successful replay; UNSAT needs
    no replay. Static consistency checks may be model-global only when they have
    source basis and a typed executable predicate.

    Failure semantics: invalid arguments, stale/non-executable FCSTM, duplicate
    check ids, unsupported check kinds, missing bindings, undefined refs,
    malformed specs, unknown/timeout/incomplete obligations, and replay mismatch
    are structured mechanical failures and are never silently dropped or converted
    to pass. The binder may revise only binding/executable/bounds in a later
    attempt; this function must not rewrite sealed NL/source basis or expected
    behavior. A stable property result can establish mechanical execution even
    when it contradicts the sealed expected outcome; that contradiction remains
    evidence for Discover and is not a reason to erase an executable check.

    Evidence limitations: mechanical eligibility says a check can be run and its
    bounded obligations did not fail in the supplied profile. It cannot prove the
    check faithfully expresses NL, has sufficient coverage, has appropriate
    strength, finds every issue, or supports method-level effectiveness. Mutation
    sensitivity facts, when present, are finite accounting only and are not part
    of eligibility.

    Permissions: read-only over the current ``check_fcstm`` result and candidate
    checks; no arbitrary filesystem paths, alternate model/run/case, shell,
    Python/Z3 expressions, network access, writes, mutation, seed/reference/gold
    inputs, or hidden evaluator oracle.

    Example: ``execute([{"check_id":"P1","check_kind":"property","binding_refs":["state:Root.Idle"],"source_basis":["source:req"],"executable_spec":{"query":"check reach <= 1: active(\"Root.Idle\");"},"required":true}], check_fcstm_result, {"property_results":[{"check_id":"P1","status":"passed","solver_status":"sat","property_satisfied":true,"witness":{"frames":[]},"replay":{"ok":true}}]})`` returns one mechanically eligible property record and no semantic quality verdict.
    """

    executable = bool(check_result.get("executable"))
    inspect = check_result.get("inspect", {}) if isinstance(check_result, dict) else {}
    results: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    property_results = {
        str(item.get("check_id")): item
        for item in (property_evidence or {}).get("property_results", [])
        if isinstance(item, dict) and item.get("check_id") is not None
    }
    if not isinstance(checks, list):
        return {"execution_status": "invalid_arguments", "mechanically_eligible": False, "model_executable": executable, "checks": [], "limitations": [*_LIMITATIONS, "checks_must_be_list"]}
    for check in checks:
        if not isinstance(check, dict):
            results.append({"check_id": None, "mechanically_eligible": False, "binding_status": "invalid", "definedness_status": "invalid", "executability_status": "invalid", "non_vacuity_obligations": []})
            continue
        check_id = check.get("check_id")
        check_kind = check.get("check_kind")
        refs = check.get("binding_refs", [])
        source_basis = check.get("source_basis", [])
        spec = check.get("executable_spec")
        required = bool(check.get("required", True))
        id_ok = isinstance(check_id, str) and bool(check_id) and check_id not in seen_ids
        seen_ids.add(str(check_id))
        kind_ok = check_kind in _SUPPORTED_KINDS
        refs_are_valid = isinstance(refs, list) and bool(refs) and all(_valid_binding_ref(ref, inspect) for ref in refs)
        static_global = (
            check_kind == "static_consistency"
            and isinstance(refs, list)
            and not refs
            and bool(source_basis)
            and isinstance(spec, dict)
            and spec.get("kind") == "diagnostic_expectation"
        )
        binding_ok = refs_are_valid or static_global
        spec_ok = _executable_spec_ok(check_kind, spec)
        obligations = _obligations_for(check, property_results)
        obligations_ok = _obligations_ok(obligations)
        # Property checks are allowed to omit explicit obligation results in the
        # current thin wrapper only when the executable spec is legacy state_shape;
        # FBMCQ checks must report bounded obligation status before eligibility.
        if check_kind == "property" and isinstance(spec, dict) and spec.get("kind") in {"fbmcq", "fbmcq_query"} and not obligations:
            obligations_ok = False
        eligible = executable and id_ok and kind_ok and binding_ok and spec_ok and obligations_ok
        results.append({
            "check_id": check_id,
            "check_kind": check_kind,
            "required": required,
            "mechanically_eligible": eligible,
            "binding_status": "valid" if binding_ok else "missing_or_undefined",
            "definedness_status": "valid" if id_ok and kind_ok else "invalid",
            "executability_status": "valid" if spec_ok and executable else "invalid",
            "non_vacuity_obligations": obligations,
        })
    overall = executable and all(item.get("mechanically_eligible") for item in results if item.get("required", True)) and bool(results)
    return {"execution_status": "completed", "mechanically_eligible": overall, "model_executable": executable, "checks": results, "limitations": list(_LIMITATIONS)}
