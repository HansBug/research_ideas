from __future__ import annotations

from typing import Any

from pydantic import Field, create_model

from ..schemas.tools import NonBlankString, SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


ReviseAssertionInput = create_model(
    "ReviseAssertionInput",
    __base__=StrictToolModel,
    **{
        "assertion_chain_id": (str, Field(min_length=1)),
        "assert": (str, Field(min_length=1)),
        "reason": (NonBlankString, ...),
    },
)


def execute(registry: CoverageRegistry, assertion_chain_id: str, assert_text: str, reason: str) -> dict[str, object]:
    """Append a new latest assertion version in the controller registry."""

    return registry.revise_assertion(assertion_chain_id, assert_text, reason=reason)


def build_tool(registry: CoverageRegistry) -> SimpleStructuredTool:
    """Purpose: create the ``revise_assertion`` tool for one Discover attempt.

    Parameters: ``registry`` is the Controller-owned append-only
    ``CoverageRegistry``. The public input fields are ``assertion_chain_id``,
    ``assert`` (internally ``assert_text`` because ``assert`` is a Python
    keyword), and ``reason``. ``reason`` is trimmed and stored as the revision
    rationale and is not trusted for Root/Unit matching.

    Returns: a ``StructuredTool`` named ``revise_assertion``. Accepted revisions
    return the new ``assertion_version_id``, ``assert_sha256``, inherited
    Root/Unit/required/basis/evidence-scope/function-family metadata, and
    append-only limitations. Rejections return ``invalid_arguments`` and preserve
    the old latest version.

    Execution: the tool appends one new version to an existing assertion chain.
    It never mutates old versions or old results. The revision inherits
    ``required``, Root, CoverageUnit, basis IDs, evidence scope, and required
    function families from the previous latest version, so the public API cannot
    weaken them. The new expression/SHA must not duplicate another chain's latest
    active expression.

    Failure semantics: unknown chain IDs, same-expression revisions, or duplicate
    latest expression/SHA collisions are rejected and recorded; the previous
    latest version remains the only latest version for matching and projection.

    Evidence limitations: revision acceptance proves only metadata inheritance
    and expression uniqueness. It does not prove logical equivalence, semantic
    non-weakening, model correctness, or issue truth; evaluator/hidden-twin checks
    remain responsible for semantic weakening.

    Permissions: current-run registry only. No arbitrary paths, network, shell,
    hidden references/gold inputs, model refresh, assertion evaluation, or final
    submit are permitted.

    When to use: use only after a registered assertion version has syntax,
    dependency, evidence, or expression-shape problems and must be replaced by a
    new expression for the same Root/Unit obligation.

    When not to use: do not use to add a new Root, change basis/family/scope,
    downgrade a required assertion, batch multiple chains, or execute evidence.

    Examples: ``{"assertion_chain_id":"ASSERT-003","assert":"(effect_delta(source='Root.Attack', event='Root.Attack_Complete', variable='uav_count') or 0) < 0","reason":"Keep the same quantity-decrease obligation but avoid the prior ambiguous helper."}``.
    """

    def revise_assertion(**kwargs: Any) -> dict[str, object]:
        """Purpose
        -------
        Append a replacement expression version for one already registered
        assertion chain without deleting or weakening the previous version.

        When to use
        -----------
        Use when the latest assertion expression cannot be evaluated or needs a
        narrower executable formulation for the same Root/Unit.

        When not to use
        ----------------
        Do not use to change Root, CoverageUnit, required status, basis,
        evidence scope, required function families, or to add a different
        semantic obligation.

        Parameters
        ----------
        ``assertion_chain_id`` names one existing chain. ``assert`` is one Python
        expression string. ``reason`` is required natural language; surrounding
        whitespace is removed before it is saved.

        Returns
        -------
        Accepted revisions return the new version ID, SHA, and inherited metadata.
        Rejections return ``invalid_arguments`` and old-latest preservation data.

        Execution
        ---------
        The Controller checks chain existence and latest expression uniqueness,
        then appends ``@vN`` with inherited required/root/unit/basis/scope/family.

        Failure semantics
        -----------------
        Rejected revisions leave the prior latest expression active. The failed
        attempt is still recorded for audit.

        Evidence limitations
        --------------------
        No eval occurs here and semantic non-weakening is not automatically
        proven by syntactic inheritance.

        Permissions
        -----------
        Current registry mutation only; no arbitrary paths, network, shell,
        reference/gold inputs, model refresh, or batch execution.

        Examples
        --------
        ``{"assertion_chain_id":"ASSERT-1","assert":"transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')","reason":"Revise to an exact target relation while inheriting ROOT-1."}``
        """

        return execute(registry, kwargs["assertion_chain_id"], kwargs["assert"], kwargs["reason"])

    return SimpleStructuredTool(
        func=revise_assertion,
        name="revise_assertion",
        description=revise_assertion.__doc__ or "revise_assertion",
        args_schema=ReviseAssertionInput,
    )
