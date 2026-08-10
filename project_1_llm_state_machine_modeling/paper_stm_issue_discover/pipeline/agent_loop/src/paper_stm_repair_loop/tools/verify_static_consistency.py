from __future__ import annotations

from typing import Any

_LIMITATIONS = [
    "static_consistency_helper_only",
    "bounded_to_check_fcstm_structured_facts",
    "not_an_agent_tool",
    "no_nl_alignment_or_coverage_verdict",
]


def execute(checks: list[dict[str, Any]], *, check_result: dict[str, Any] | None = None) -> dict[str, Any]:
    """Purpose: evaluate bounded ``static_consistency`` helper checks from Controller-owned issue checks.

    Parameters: ``checks`` is the immutable Controller check list; only items with
    ``check_kind="static_consistency"`` are evaluated. ``check_result`` is the
    current ``check_fcstm`` structured result for the same model/hash and must
    contain ``executable=true`` plus normalized diagnostics/inspect facts. The
    supported typed executable specs are ``diagnostic_expectation``,
    ``transition_shape``, ``forced_transition_shape``, ``state_shape``, and
    ``state_label_scopes``. The latter four consume only normalized inspect
    facts produced by deterministic binding; Agents never supply raw paths.
    Callers cannot provide arbitrary filesystem paths, alternate model text,
    run/case selectors, URLs, shell commands, Python/Z3, or reference/gold data.

    Returns: a JSON-safe dictionary with ``execution_status``, ``static_results``,
    ``errors`` when applicable, ``not_applicable``, and ``limitations``. Each
    static result contains ``check_id``, ``status`` (``passed``, ``failed``, or
    ``not_implemented``), bounded ``expected`` and ``observed`` facts, and a
    reason for unsupported/malformed specs. Unsupported specs are never silently
    converted into pass.

    Execution: reads only the diagnostics and transition facts already produced
    by ``check_fcstm``. Diagnostic expectations count matching structured
    diagnostic codes/severities. Transition checks compare explicitly named
    normal or forced-transition fields. State checks compare declared hierarchy
    shape or same-label occurrences across expected parent scopes. The helper
    does not parse source text heuristically, call an LLM, run a solver, mutate
    the model, or refresh mutable state.

    Failure semantics: missing/non-executable ``check_fcstm`` input returns
    ``execution_status=failed``. Malformed specs, unsupported helper kinds,
    missing transition indices, unknown diagnostic codes, ``timeout``,
    ``incomplete``, or replay-mismatch-like upstream states do not pass by
    default. A ``failed`` static result is a bounded structural mismatch, not a
    tool crash or confirmed source defect.

    Evidence limitations: this helper can support mechanical applicability of a
    source-internal consistency check, but it cannot prove NL alignment, semantic
    correctness, source closure, coverage sufficiency, global model correctness,
    issue severity, or repair success. Static consistency is intentionally an
    internal ``check_fcstm`` helper and not an Agent-facing tool.

    Permissions: read-only over the current ``check_fcstm`` result and the
    supplied immutable checks; no Agent-supplied arbitrary paths, alternate
    model/run/case, shell, Python/Z3, network, writes, mutation, or
    seed/reference/gold inputs are accepted.

    Example: ``execute([{"check_id":"ST1","check_kind":"static_consistency","executable_spec":{"kind":"state_shape","state_path":"Root.Mode","expect":{"is_composite":true}}}], check_result=check_fcstm_result)`` returns a bounded structured state-shape comparison under ``static_results``.
    """

    static_checks = [check for check in checks if isinstance(check, dict) and check.get("check_kind") == "static_consistency"] if isinstance(checks, list) else []
    if not static_checks:
        return {"execution_status": "completed", "static_results": [], "errors": [], "not_applicable": True, "limitations": list(_LIMITATIONS)}
    if not check_result or not check_result.get("executable"):
        return {
            "execution_status": "failed",
            "static_results": [],
            "errors": [{"message": "check_fcstm must succeed before static consistency checks"}],
            "not_applicable": False,
            "limitations": [*_LIMITATIONS, "check_fcstm_required"],
        }

    inspect = check_result.get("inspect", {})
    diagnostics = inspect.get("diagnostics", []) or check_result.get("diagnostics", []) or []
    transitions = inspect.get("transitions", []) or []
    forced_transitions = inspect.get("forced_transitions", []) or []
    states = inspect.get("states", []) or []
    results: list[dict[str, Any]] = []
    for check in static_checks:
        check_id = check.get("check_id")
        spec = check.get("executable_spec") or {}
        if not isinstance(spec, dict):
            results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "executable_spec must be an object"})
            continue
        kind = spec.get("kind")
        if kind == "diagnostic_expectation":
            code = spec.get("code")
            severity = spec.get("severity")
            if not isinstance(code, str) or not code:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "diagnostic_expectation.code must be a non-empty string"})
                continue
            matching = [item for item in diagnostics if isinstance(item, dict) and item.get("code") == code and (severity is None or item.get("severity") == severity)]
            expected_count = spec.get("expect_count")
            if not isinstance(expected_count, int) or expected_count < 0:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "expect_count must be a non-negative integer"})
                continue
            results.append({
                "check_id": check_id,
                "status": "passed" if len(matching) == expected_count else "failed",
                "bounded": True,
                "expected": {"code": code, "severity": severity, "count": expected_count},
                "observed": {"count": len(matching), "diagnostics": matching},
            })
            continue
        if kind == "transition_shape":
            index = spec.get("transition_index")
            expected = spec.get("expect") or {}
            if not isinstance(index, int) or not isinstance(expected, dict) or not expected:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "transition_shape requires integer transition_index and non-empty expect"})
                continue
            observed = next((item for item in transitions if isinstance(item, dict) and item.get("transition_index") == index), None)
            if observed is None:
                results.append({"check_id": check_id, "status": "failed", "bounded": True, "expected": expected, "observed": None, "reason": "transition_not_found"})
                continue
            actual = {key: observed.get(key) for key in expected}
            results.append({"check_id": check_id, "status": "passed" if actual == expected else "failed", "bounded": True, "expected": expected, "observed": actual})
            continue
        if kind == "forced_transition_shape":
            expected = spec.get("expect") or {}
            if not isinstance(expected, dict) or not expected:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "forced_transition_shape requires non-empty expect"})
                continue
            observed = next(
                (
                    item
                    for item in forced_transitions
                    if isinstance(item, dict)
                    and all(item.get(key) == value for key, value in expected.items())
                ),
                None,
            )
            results.append({"check_id": check_id, "status": "passed" if observed is not None else "failed", "bounded": True, "expected": expected, "observed": observed})
            continue
        if kind == "state_shape":
            state_path = spec.get("state_path")
            expected = spec.get("expect") or {}
            if not isinstance(state_path, str) or not isinstance(expected, dict) or not expected:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "state_shape requires state_path and non-empty expect"})
                continue
            observed = next((item for item in states if isinstance(item, dict) and item.get("path") == state_path), None)
            actual = None if observed is None else {key: observed.get(key) for key in expected}
            results.append({"check_id": check_id, "status": "passed" if actual == expected else "failed", "bounded": True, "expected": expected, "observed": actual})
            continue
        if kind == "state_label_scopes":
            state_paths = spec.get("state_paths")
            expected_scopes = spec.get("expected_scope_labels")
            if not isinstance(state_paths, list) or not state_paths or not isinstance(expected_scopes, list) or not expected_scopes:
                results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": "state_label_scopes requires non-empty state_paths and expected_scope_labels"})
                continue
            by_path = {item.get("path"): item for item in states if isinstance(item, dict) and item.get("path")}
            observed_scopes = sorted(
                {
                    str(by_path[path].get("parent_path") or "").rsplit(".", 1)[-1]
                    for path in state_paths
                    if path in by_path
                }
            )
            expected = sorted(str(item) for item in expected_scopes)
            results.append({"check_id": check_id, "status": "passed" if observed_scopes == expected else "failed", "bounded": True, "expected": {"scope_labels": expected}, "observed": {"scope_labels": observed_scopes, "state_paths": state_paths}})
            continue
        results.append({"check_id": check_id, "status": "not_implemented", "bounded": True, "reason": f"unsupported static consistency kind: {kind}"})
    return {"execution_status": "completed", "static_results": results, "errors": [], "not_applicable": False, "limitations": list(_LIMITATIONS)}
