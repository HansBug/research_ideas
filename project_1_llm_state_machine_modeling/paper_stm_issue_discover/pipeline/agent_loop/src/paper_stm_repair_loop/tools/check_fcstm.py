from __future__ import annotations

from typing import Any

from ..pyfcstm_adapter import check_fcstm as _check
from .verify_static_consistency import execute as _verify_static_consistency


def execute(
    model_text: str,
    model_path: str = "<memory>",
    *,
    static_checks: list[dict[str, Any]] | None = None,
    verify_profile_ref: str | None = None,
) -> dict[str, Any]:
    """Purpose: run the Controller's FCSTM parse, semantic-build, inspect, and scoped static helper pass for one frozen model.

    Parameters: ``model_text`` is the controller-bound FCSTM source for the
    current model artifact, normally ``STM_0`` in Discover or a submitted Repair
    candidate before publication. ``model_path`` is a controller-provided label
    used only for pyfcstm diagnostics and defaults to ``"<memory>"``; Agents must
    not supply arbitrary paths or alternate model content. ``static_checks`` is an
    optional controller-owned list of already prepared ``static_consistency``
    check objects to evaluate as an internal helper, not as a separate Agent
    tool. ``verify_profile_ref`` is reserved for a fixed local-verify registry
    profile; this implementation records it but does not accept arbitrary solver
    expressions.

    Returns: a JSON-safe dictionary with ``execution_status``, ``parse_status``,
    ``semantic_status``, ``inspect_status``, ``executable``, ``diagnostics``,
    ``inspect``, ``metrics``, ``model_sha256``, and ``model_type``. When
    ``static_checks`` is provided, the result also contains
    ``static_consistency`` with the same structured helper output produced by
    ``verify_static_consistency.execute``. Parse/semantic failure is represented
    as ``execution_status=completed`` with ``executable=false`` and a safe error
    object.

    Execution: delegates parsing, semantic construction, diagnostics, and LLM-safe
    inspect JSON production to the public pyfcstm structured adapter. Diagnostics
    are kept JSON-safe and are copied into both the machine result and
    Agent-facing report fields. If static helper checks are supplied, they are
    evaluated only after the current inspect result exists, using the current
    model hash and structured facts rather than text heuristics. No LLM call,
    mutation, network access, cache refresh, or reference/gold lookup occurs.

    Failure semantics: malformed FCSTM, pyfcstm parse errors, semantic build
    errors, unavailable inspect, unsupported static helper specs, or local helper
    errors never become confirmed issues or repair commands by themselves.
    Required downstream stages must fail closed when ``executable`` is false or a
    required helper result is missing, stale, schema-invalid, ``unknown``,
    ``timeout``, ``incomplete``, or replay-mismatched. Bare exception messages are
    stored only inside safe error objects and are not treated as structured model
    facts.

    Evidence limitations: a successful parse/semantic/inspect result means the
    FCSTM is mechanically executable under pyfcstm and exposes scoped structural
    facts. Warnings, diagnostics, repair guidance, local verify facts, and static
    helper results do not prove NL alignment, semantic correctness, source
    closure, issue severity, absence of defects, or global property satisfaction.

    Permissions: read-only over the controller-bound current model and optional
    controller-bound static check objects. The callable does not accept arbitrary
    filesystem paths from an Agent, shell commands, Python/Z3 snippets, URLs,
    alternate run/case selectors, mutable artifacts, seed/reference/gold inputs,
    or permission to edit the model.

    Example: ``execute('state Root { state Idle; [*] -> Idle; }')`` returns a
    completed executable result with inspect facts for ``Root`` and ``Root.Idle``.
    ``execute(model, static_checks=[{"check_id":"S1","check_kind":"static_consistency","executable_spec":{"kind":"diagnostic_expectation","code":"W_UNREFERENCED_VAR","expect_count":0}}])`` embeds a bounded ``static_consistency`` helper result without exposing a separate Agent tool.
    """

    result = _check(model_text, model_path)
    if verify_profile_ref is not None:
        result.setdefault("verify_profile_ref", verify_profile_ref)
        result.setdefault("local_verify", {"execution_status": "not_run", "reason": "fixed_registry_profile_not_configured"})
    if static_checks is not None:
        result["static_consistency"] = _verify_static_consistency(static_checks, check_result=result)
    return result
