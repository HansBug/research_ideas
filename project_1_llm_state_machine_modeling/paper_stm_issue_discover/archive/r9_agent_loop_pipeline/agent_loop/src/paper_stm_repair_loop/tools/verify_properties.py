from __future__ import annotations

import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any, Callable

from ..pyfcstm_adapter import sha256_text

_LIMITATIONS = [
    "bounded_model_checking_only",
    "bounded_no_counterexample_is_not_unbounded_proof",
    "expected_outcome_is_check_internal_not_semantic_oracle",
]
_BAD_STATUSES = {"unknown", "timeout", "incomplete", "replay_mismatch", "error", "execution_error", "tool_unavailable"}


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _safe_json_loads(text: str) -> dict[str, Any]:
    value = json.loads(text)
    if not isinstance(value, dict):
        raise ValueError("BMC JSON output must be an object")
    return value


def _match_expected(expected: Any, property_satisfied: Any, stable: bool) -> str:
    if not stable:
        return "inconclusive"
    if not isinstance(expected, dict) or "property_satisfied" not in expected or not isinstance(property_satisfied, bool):
        return "inconclusive"
    return "matches" if expected["property_satisfied"] is property_satisfied else "contradicts"


def _interpret_bmc(check: dict[str, Any], query: str, payload: dict[str, Any], exit_code: int) -> dict[str, Any]:
    result = payload.get("result") if isinstance(payload.get("result"), dict) else {}
    prop = payload.get("property") if isinstance(payload.get("property"), dict) else {}
    replay = payload.get("replay")
    replay_ok = isinstance(replay, dict) and replay.get("ok") is True
    status = str(result.get("status") or "unknown")
    timeout = bool(result.get("timeout") or result.get("timeout_ms") or status == "timeout")
    incomplete = bool(result.get("incomplete") or result.get("has_incomplete_model") or status == "incomplete")
    property_satisfied = result.get("property_satisfied")
    outcome = result.get("outcome")
    stable = True
    public_status = status
    if timeout:
        public_status = "timeout"
        stable = False
    elif incomplete:
        public_status = "incomplete"
        stable = False
    elif status in {"unknown", "error", "execution_error"}:
        public_status = status
        stable = False
    elif replay is not None and not replay_ok:
        public_status = "replay_mismatch"
        stable = False
    elif not isinstance(property_satisfied, bool):
        public_status = "unknown"
        stable = False
    match = _match_expected(check.get("expected_outcome"), property_satisfied, stable)
    passed = stable and public_status not in _BAD_STATUSES and match != "contradicts" and exit_code in {0, 1}
    # If an expected bool is present, only an exact match can be a pass. Without
    # an expected bool, the BMC fact is completed but not a pass/fail verdict for
    # the check's sealed expectation.
    if isinstance(check.get("expected_outcome"), dict) and "property_satisfied" in check.get("expected_outcome", {}):
        passed = passed and match == "matches"
    return {
        "check_id": check.get("check_id"),
        "status": "passed" if passed else public_status if public_status in _BAD_STATUSES else "failed" if match == "contradicts" else "completed",
        "passed": bool(passed),
        "query": query,
        "query_sha256": _sha256_text(query),
        "kind": prop.get("kind") or result.get("kind"),
        "bound": prop.get("bound"),
        "polarity": prop.get("polarity") or result.get("polarity"),
        "solver_status": status,
        "property_satisfied": property_satisfied,
        "outcome": outcome,
        "witness": payload.get("witness"),
        "replay": replay,
        "timeout": timeout,
        "incomplete": incomplete,
        "exit_code": exit_code,
        "expected": check.get("expected_outcome"),
        "expected_outcome_match_status": match,
        "raw_bmc": payload,
    }


def _run_bmc(model_text: str, query: str, model_path: str, timeout_ms: int | None, max_bound: int | None, bmc_runner: Callable[..., tuple[str, int]] | None) -> tuple[str, int]:
    with tempfile.TemporaryDirectory(prefix="paper1-bmc-") as tmp:
        tmpdir = Path(tmp)
        model_file = tmpdir / (Path(model_path).name if model_path and model_path != "<memory>" else "model.fcstm")
        query_file = tmpdir / "query.fbmcq"
        model_file.write_text(model_text, encoding="utf-8")
        query_file.write_text(query, encoding="utf-8")
        if bmc_runner is None:
            from pyfcstm.entry.bmc import build_bmc_output

            return build_bmc_output(str(model_file), str(query_file), json_output=True, timeout_ms=timeout_ms, max_bound=max_bound)
        return bmc_runner(str(model_file), str(query_file), json_output=True, timeout_ms=timeout_ms, max_bound=max_bound)


def _state_shape(check: dict[str, Any], inspect: dict[str, Any]) -> dict[str, Any]:
    states = {state.get("path"): state for state in inspect.get("states", []) if isinstance(state, dict) and state.get("path")}
    spec = check.get("executable_spec") or {}
    state_path = spec.get("state")
    expected = spec.get("expect") or {}
    if spec.get("kind") != "state_shape" or not isinstance(state_path, str) or not expected:
        return {"check_id": check.get("check_id"), "status": "not_implemented", "passed": False, "bounded": True, "property_satisfied": None, "solver_status": "not_implemented", "reason": "unsupported_property_spec"}
    observed = states.get(state_path)
    if observed is None:
        return {"check_id": check.get("check_id"), "status": "failed", "passed": False, "bounded": True, "property_satisfied": False, "solver_status": "deterministic_static", "outcome": "property_violated", "expected": expected, "observed": None, "reason": "state_not_found", "expected_outcome_match_status": "contradicts"}
    predicates = {
        "is_leaf": observed.get("is_leaf"),
        "is_composite": observed.get("is_composite"),
        "is_pseudo": observed.get("is_pseudo"),
        "has_substates": bool(observed.get("substates")),
    }
    passed = all(predicates.get(key) == value for key, value in expected.items() if key != "substates_min")
    if "substates_min" in expected:
        passed = passed and len(observed.get("substates", [])) >= expected["substates_min"]
    return {"check_id": check.get("check_id"), "status": "passed" if passed else "failed", "passed": bool(passed), "bounded": True, "property_satisfied": bool(passed), "solver_status": "deterministic_static", "outcome": "property_satisfied" if passed else "property_violated", "expected": expected, "observed": {**predicates, "substates": observed.get("substates", [])}, "expected_outcome_match_status": "matches" if passed else "contradicts"}


def execute(
    model_text: str,
    checks: list[dict[str, Any]],
    *,
    check_result: dict[str, Any] | None = None,
    bounds_profile_ref: str | None = None,
    timeout_ms: int | None = None,
    max_bound: int | None = None,
    bmc_runner: Callable[..., tuple[str, int]] | None = None,
    **_kwargs: Any,
) -> dict[str, Any]:
    """Purpose: run bounded FBMCQ property checks for the Controller's current model and preserve replay-aware BMC evidence.

    Parameters: ``model_text`` is the controller-bound FCSTM artifact and
    ``checks`` is the immutable current ``issue_checks[]`` list; Agents cannot
    provide arbitrary model text, paths, run ids, case ids, URLs, shell commands,
    Python/Z3, or reference/gold inputs. Property checks use
    ``check_kind="property"``. Preferred executable specs contain
    ``{"kind":"fbmcq", "query":"check ...;"}`` or ``fbmcq``/``query`` text.
    The legacy ``state_shape`` spec remains supported for local structural smoke
    tests. ``check_result`` supplies existing inspect facts for legacy specs.
    ``bounds_profile_ref``, ``timeout_ms``, and ``max_bound`` are controller
    profile controls. ``bmc_runner`` is an injectable public-API-compatible test
    seam; production uses ``pyfcstm.entry.bmc.build_bmc_output(...,
    json_output=True)``.

    Returns: ``execution_status``, ``model_sha256``, ``bounds_profile_ref``,
    ``property_results``, ``errors``, ``not_applicable``, and ``limitations``.
    FBMCQ results save ``query``, ``query_sha256``, ``kind``, ``bound``,
    ``polarity``, solver status, ``property_satisfied``, ``outcome``, witness,
    replay, timeout, incomplete flag, ``expected_outcome_match_status``, and a
    boolean ``passed`` that is false for unknown/timeout/incomplete/replay
    mismatch/error.

    Execution: each FBMCQ query is written to a temporary query file beside a
    temporary copy of the controller-bound model and executed through pyfcstm's
    public BMC output API with JSON output. The JSON is parsed, normalized, and
    interpreted by polarity/status only within the bounded result protocol. The
    function does not call an LLM, synthesize new properties, mutate the model, or
    read hidden evaluator assets.

    Failure semantics: malformed property specs become ``not_implemented``;
    BMC parser/solver exceptions become per-check ``execution_error`` and top
    level ``errors``; JSON parse failure is an execution error. ``unknown``,
    ``timeout``, ``incomplete``, missing ``property_satisfied``, and replay
    mismatch are never passes. A violated property is a normal completed domain
    fact, not a tool failure.

    Evidence limitations: BMC answers only the FBMCQ query within the declared
    bound/profile. No counterexample within a bound is not an unbounded proof.
    ``expected_outcome_match_status`` compares against the check's sealed typed
    expectation only and does not prove NL faithfulness, coverage sufficiency,
    source closure, repair correctness, or method-level success.

    Permissions: read-only over the current controller-bound model/checks and
    temporary files created internally; no Agent-supplied arbitrary paths,
    alternate model/run/case, shell, Python/Z3 expressions, network, writes,
    mutation, seed/reference/gold, or hidden oracle access.

    Example: ``execute(model, [{"check_id":"P1","check_kind":"property","executable_spec":{"kind":"fbmcq","query":"check reach <= 1: active(\"Root.Idle\");"},"expected_outcome":{"property_satisfied":true}}])`` returns a bounded BMC record with query hash, kind, bound, polarity, outcome, witness/replay metadata, and ``passed`` only if the result is stable and matches the sealed expectation.
    """

    properties = [c for c in checks if c.get("check_kind") == "property"] if isinstance(checks, list) else []
    if not properties:
        return {"execution_status": "completed", "model_sha256": sha256_text(model_text), "bounds_profile_ref": bounds_profile_ref, "property_results": [], "errors": [], "not_applicable": True, "limitations": list(_LIMITATIONS)}

    inspect = (check_result or {}).get("inspect", {}) if isinstance(check_result, dict) else {}
    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    for check in properties:
        spec = check.get("executable_spec") or {}
        if not isinstance(spec, dict):
            item = {"check_id": check.get("check_id"), "status": "not_implemented", "passed": False, "reason": "executable_spec_must_be_object"}
            results.append(item)
            continue
        query = spec.get("query") or spec.get("fbmcq")
        if spec.get("kind") in {"fbmcq", "fbmcq_query"} or isinstance(query, str):
            if not isinstance(query, str) or not query.strip():
                results.append({"check_id": check.get("check_id"), "status": "not_implemented", "passed": False, "reason": "fbmcq_query_missing"})
                continue
            try:
                text, exit_code = _run_bmc(model_text, query, "<memory>", timeout_ms, max_bound, bmc_runner)
                payload = _safe_json_loads(text)
                results.append(_interpret_bmc(check, query, payload, exit_code))
            except TimeoutError:
                item = {"check_id": check.get("check_id"), "status": "timeout", "passed": False, "query": query, "query_sha256": _sha256_text(query), "expected_outcome_match_status": "inconclusive"}
                results.append(item)
                errors.append({"check_id": check.get("check_id"), "type": "TimeoutError"})
            except Exception as exc:
                item = {"check_id": check.get("check_id"), "status": "execution_error", "passed": False, "query": query, "query_sha256": _sha256_text(query), "expected_outcome_match_status": "inconclusive", "error": {"type": type(exc).__name__, "message": str(exc)}}
                results.append(item)
                errors.append({"check_id": check.get("check_id"), "type": type(exc).__name__, "message": str(exc)})
            continue
        results.append(_state_shape(check, inspect))
    return {"execution_status": "completed", "model_sha256": sha256_text(model_text), "bounds_profile_ref": bounds_profile_ref, "property_results": results, "errors": errors, "not_applicable": False, "limitations": list(_LIMITATIONS)}
