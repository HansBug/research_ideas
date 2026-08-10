from __future__ import annotations

import copy
from typing import Any, Mapping

from ..records import sha256_json
from ..schemas.inspect import InspectModelInput, InspectModelResult
from ..schemas.tools import SimpleStructuredTool


_LIMITATIONS = [
    "controller_frozen_check_result_only",
    "read_only_llm_safe_projection",
    "no_parse_or_semantic_rerun",
    "no_filesystem_network_or_reference_access",
]
_RECOMMENDED_NEXT_EVIDENCE = [
    "Use the already returned inspect facts and read_task SourceFacts; do not call inspect_model again for the same fingerprint.",
    "Use query_model for a bounded, named states/events/transitions/variables/diagnostics gap that existing facts do not answer.",
    "Use register_coverage_plan when the existing facts are enough to commit assertions; registration does not require pre-proving truth.",
    "Use eval_assert for latest registered assertions after registration; use lookup_source_trace only for attribution of specific contradicted model refs.",
]


def _as_dict(value: Any) -> dict[str, Any]:
    return copy.deepcopy(value) if isinstance(value, dict) else {}


def _extract_inspect(check_result: Mapping[str, Any]) -> dict[str, Any]:
    inspect = check_result.get("inspect")
    if isinstance(inspect, dict):
        return copy.deepcopy(inspect)
    model = check_result.get("model")
    if isinstance(model, dict):
        inspect = model.get("normalized_inspect") or model.get("inspect")
        if isinstance(inspect, dict):
            return copy.deepcopy(inspect)
    return {}


def _extract_model_sha256(check_result: Mapping[str, Any], inspect: Mapping[str, Any]) -> str | None:
    for key in ("model_sha256", "fcstm_sha256", "sha256"):
        value = check_result.get(key)
        if isinstance(value, str) and value:
            return value
    model = check_result.get("model")
    if isinstance(model, dict):
        for key in ("model_sha256", "fcstm_sha256", "sha256"):
            value = model.get(key)
            if isinstance(value, str) and value:
                return value
    value = inspect.get("model_sha256")
    return value if isinstance(value, str) and value else None


def project_check_result(check_result: Mapping[str, Any], *, reason: str = "") -> dict[str, Any]:
    """Return the LLM-safe inspect view for one Controller-frozen check result."""

    inspect = _extract_inspect(check_result)
    diagnostics = check_result.get("diagnostics")
    if not isinstance(diagnostics, list):
        diagnostics = inspect.get("diagnostics") if isinstance(inspect.get("diagnostics"), list) else []
    metrics = check_result.get("metrics")
    if not isinstance(metrics, dict):
        metrics = inspect.get("metrics") if isinstance(inspect.get("metrics"), dict) else {}
    model_sha256 = _extract_model_sha256(check_result, inspect)
    check_sha256 = sha256_json(dict(check_result))
    payload = {
        "execution_status": "completed" if check_result else "tool_unavailable",
        "parse_status": check_result.get("parse_status"),
        "semantic_status": check_result.get("semantic_status"),
        "inspect_status": check_result.get("inspect_status"),
        "executable": bool(check_result.get("executable", False)),
        "diagnostics": copy.deepcopy(diagnostics),
        "inspect": inspect,
        "metrics": copy.deepcopy(metrics),
        "model": {
            "model_id": check_result.get("model_id") or _as_dict(check_result.get("model")).get("model_id") or "STM_0",
            "model_type": check_result.get("model_type"),
            "sha256": model_sha256,
            "model_sha256": model_sha256,
            "inspect_sha256": sha256_json(inspect),
        },
        "check": {
            "sha256": check_sha256,
            "check_result_sha256": check_sha256,
            "schema": "paper1.inspect_model.weak_lead.v1",
        },
        "limitations": list(_LIMITATIONS),
        "recommended_next_evidence": list(_RECOMMENDED_NEXT_EVIDENCE),
        "record_id": check_result.get("record_id") if isinstance(check_result.get("record_id"), str) else None,
        "reason": reason,
    }
    return InspectModelResult.model_validate(payload).model_dump(mode="json")


def execute(check_result: dict[str, Any], reason: str) -> dict[str, Any]:
    """Purpose: expose only the Controller-frozen FCSTM check_result inspect view.

    Parameters: ``check_result`` is the Controller-owned immutable result of the
    parse, semantic-build, inspect, and executable preflight for the current
    model. ``reason`` is the Agent's non-empty explanation for why this exact
    frozen view is needed. Agents cannot supply alternate model text, file paths,
    run IDs, case IDs, shell commands, Python code, URLs, refresh flags, or
    reference/gold artifacts.

    Returns: a JSON object with parse/semantic/inspect statuses, executable flag,
    diagnostics, normalized inspect facts, metrics, model hash, check-result hash,
    limitations, recommended next evidence, record ID when the Controller supplied
    one, and the original reason. Recovery guidance tells the Agent to stop
    repeated inspect calls and use existing facts, query_model,
    register_coverage_plan, or eval_assert instead. It does not include raw task text, source text,
    hidden reference data, mutable paths, or post-freeze records.

    Execution: validates and deep-copies the already frozen check_result, computes
    stable hashes, and emits an LLM-safe projection. It performs no filesystem IO,
    network IO, model parsing, semantic rebuild, pyfcstm rerun, LLM call, cache
    refresh, latest-state lookup, or mutation.

    Failure semantics: a missing or malformed frozen check_result returns a
    bounded unavailable projection rather than inventing facts. Domain diagnostics
    remain observations, not confirmed NL defects or repair instructions.

    Evidence limitations: this weak-lead view proves only mechanical FCSTM
    executability and structured inspect availability under the Controller's
    frozen check. It does not prove NL alignment, source closure, issue severity,
    repair correctness, or property satisfaction.

    Permissions: read-only over one in-memory Controller-frozen check_result; no
    arbitrary paths, shell/Python/Z3, network, alternate run/case/model selectors,
    writes, refresh, future state, or reference/gold inputs are allowed.

    Example: ``execute({"parse_status":"ok","semantic_status":"ok","inspect_status":"ok","executable":True,"inspect":{"states":[]},"model_sha256":"abc"}, "Inspect weak lead.")`` returns a completed projection with inspect and hash fields only.
    """

    return project_check_result(check_result, reason=reason)


def build_tool(check_result: dict[str, Any]) -> SimpleStructuredTool:
    """Purpose: create the ``inspect_model`` tool bound to one frozen check_result.

    Parameters: ``check_result`` is closed over by the Controller before provider
    dispatch and is never supplied by the Agent. The resulting tool input schema
    contains exactly one required ``reason`` field.

    Returns: a LangChain structured tool named ``inspect_model``. The first call
    for a check-result fingerprint returns the full LLM-safe projection; repeated
    calls for the same fingerprint return ``execution_status=no_new_fact`` with
    the complete result schema, stable hashes, executable/status fields, and
    recovery guidance that does not recommend another ``inspect_model`` call.

    Execution: computes the frozen fingerprint once, tracks whether that
    fingerprint has already been served, and never refreshes or re-runs model
    analysis.

    Failure semantics: duplicate calls are not failures, but they add no evidence
    and should stop repeated weak-lead inspection.

    Evidence limitations: the tool is an inspect weak lead only; downstream tools
    must still bind SourceFacts, register assertions, execute checks, and pass
    review gates.

    Permissions: no Agent parameter can select a path, run, case, alternate
    model, shell command, Python/Z3 program, URL, write target, or reference/gold
    artifact.

    Example: ``build_tool(check).invoke({"reason":"Inspect the frozen model."})`` returns the frozen projection; a second call returns ``no_new_fact``.
    """

    frozen = copy.deepcopy(check_result)
    first = project_check_result(frozen, reason="controller validation")
    fingerprint = first["check"]["check_result_sha256"]
    model_sha256 = first["model"].get("model_sha256")
    served = False

    def inspect_model(reason: str) -> dict[str, Any]:
        """Purpose
        -------
        Inspect the current attempt's Controller-frozen FCSTM check result as a
        weak lead. Use it only to see parse, semantic, inspect, executable,
        diagnostics, metrics, model hash, check hash, limitations, and recommended
        next evidence for the already frozen model.

        When to use
        -----------
        Use after ``read_task`` when a concrete coverage Root needs bounded model
        structure or diagnostics before choosing ``query_model``,
        ``lookup_source_trace``, assertion registration, or trace observation.

        When not to use
        ----------------
        Do not repeat it for the same fingerprint, do not use it to refresh the
        model, and do not treat it as source-grounded proof or repair authority.

        Parameters
        ----------
        Exactly one non-empty ``reason`` string. Unknown keys are rejected. There
        is no path, run ID, case ID, model text, record selector, refresh flag,
        shell command, Python/Z3 program, URL, or reference/gold selector.

        Returns
        -------
        The first call returns ``execution_status=completed`` with exactly the
        LLM-safe projection of the frozen check result: parse/semantic/inspect
        statuses, executable, diagnostics, inspect, metrics, model hashes, check
        hashes, limitations, recommended next evidence, record ID if supplied, and
        reason. A repeated call for the same fingerprint returns
        ``execution_status=no_new_fact`` with the complete result schema, the same
        fingerprint hashes, executable/status fields, limitations, recommended
        next evidence, record ID, and reason. The guidance says to stop repeated
        inspect and use existing facts, ``query_model``,
        ``register_coverage_plan``, or ``eval_assert`` instead.

        Execution
        ---------
        Deep-copy only the Controller-frozen in-memory check result. Compute stable
        JSON hashes. Perform no parsing, semantic rebuild, filesystem IO, network
        IO, LLM call, cache refresh, latest-state lookup, or mutation.

        Failure semantics
        -----------------
        Missing frozen data yields a bounded unavailable projection. Duplicate
        calls are stop signals, not new facts. Diagnostics are observations and do
        not by themselves establish NL issue existence or repair closure.

        Evidence limitations
        --------------------
        This weak-lead view proves only what the frozen pyfcstm check observed. It
        does not prove NL alignment, source closure, issue severity, global
        property satisfaction, or repair correctness.

        Permissions
        -----------
        Read-only and current-attempt only. No arbitrary paths, alternate
        model/run/case selectors, shell/Python/Z3, network, writes, refresh,
        future state, or hidden reference/gold inputs are allowed.

        Examples
        --------
        ``{"reason":"Inspect the frozen check before querying transitions."}``
        returns the completed projection on first use. Repeating with
        ``{"reason":"Check again."}`` returns ``no_new_fact`` with complete
        schema keys and guidance to stop repeated inspect.
        """

        nonlocal served
        if served:
            payload = dict(first)
            payload.update(
                {
                    "execution_status": "no_new_fact",
                    "reason": reason,
                    "diagnostics": [],
                    "inspect": {},
                    "metrics": {},
                    "limitations": [
                        *_LIMITATIONS,
                        "duplicate_fingerprint_not_replayed",
                        "stop_repeating_inspect_model",
                    ],
                    "recommended_next_evidence": list(_RECOMMENDED_NEXT_EVIDENCE),
                }
            )
            payload["model"] = {
                "model_id": first["model"].get("model_id"),
                "model_type": first["model"].get("model_type"),
                "sha256": model_sha256,
                "model_sha256": model_sha256,
                "inspect_sha256": first["model"].get("inspect_sha256"),
            }
            payload["check"] = {
                "sha256": fingerprint,
                "check_result_sha256": fingerprint,
                "schema": first["check"].get("schema"),
            }
            return InspectModelResult.model_validate(payload).model_dump(mode="json")
        served = True
        return project_check_result(frozen, reason=reason)

    return SimpleStructuredTool(
        func=inspect_model,
        name="inspect_model",
        description=inspect_model.__doc__ or "inspect_model",
        args_schema=InspectModelInput,
    )
