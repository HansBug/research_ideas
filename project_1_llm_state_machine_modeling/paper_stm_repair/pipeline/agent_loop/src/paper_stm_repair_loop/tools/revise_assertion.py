from __future__ import annotations

from typing import Any

from pydantic import Field, create_model

from ..schemas.assertions import FormalBoundOrigin, FormalPropertyKind, FunctionFamily
from ..schemas.tools import NonBlankString, SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


ReviseAssertionInput = create_model(
    "ReviseAssertionInput",
    __base__=StrictToolModel,
    **{
        "assertion_chain_id": (str, Field(min_length=1)),
        "assert": (str, Field(min_length=1)),
        "formal_property_kind": (FormalPropertyKind | None, None),
        "formal_bound": (int | None, Field(default=None, ge=1)),
        "formal_bound_origin": (FormalBoundOrigin | None, None),
        "formal_assumption_basis_ids": (
            list[str],
            Field(default_factory=list),
        ),
        "required_function_families": (
            list[FunctionFamily] | None,
            Field(default=None, min_length=1),
        ),
        "reason": (NonBlankString, ...),
    },
)


def execute(
    registry: CoverageRegistry,
    assertion_chain_id: str,
    assert_text: str,
    reason: str,
    *,
    formal_property_kind: str | None = None,
    formal_bound: int | None = None,
    formal_bound_origin: str | None = None,
    formal_assumption_basis_ids: list[str] | None = None,
    required_function_families: list[str] | None = None,
) -> dict[str, object]:
    """Append a new latest assertion version in the controller registry."""

    return registry.revise_assertion(
        assertion_chain_id,
        assert_text,
        reason=reason,
        formal_property_kind=formal_property_kind,
        formal_bound=formal_bound,
        formal_bound_origin=formal_bound_origin,
        formal_assumption_basis_ids=formal_assumption_basis_ids,
        required_function_families=required_function_families,
    )


def build_tool(registry: CoverageRegistry) -> SimpleStructuredTool:
    """Purpose: create the ``revise_assertion`` tool for one Discover attempt.

    Parameters: ``registry`` is the Controller-owned append-only
    ``CoverageRegistry``. The public input fields are ``assertion_chain_id``,
    ``assert`` (internally ``assert_text`` because ``assert`` is a Python
    keyword), the nullable Issue #165 formal metadata fields, and ``reason``.
    ``reason`` is trimmed and stored as the revision rationale and is not
    trusted for Root/Unit matching.

    Returns: a ``StructuredTool`` named ``revise_assertion``. Accepted revisions
    return the new ``assertion_version_id``, ``assert_sha256``, preserved
    Root/Unit/required/basis/evidence-scope metadata, the current version's
    explicit function-family route, and
    append-only limitations. Rejections return ``invalid_arguments`` and preserve
    the old latest version.

    Execution: the tool appends one new version to an existing assertion chain.
    It never mutates old versions or old results. The revision inherits
    ``required``, Root, CoverageUnit, basis IDs, and evidence scope from the
    previous latest version. Omit ``required_function_families`` to inherit the
    previous route; when the revised expression changes evidence route, submit
    the complete non-empty current family list so the runtime authenticity gate
    checks what this version actually claims to use. This metadata is not a tool
    quota. A revised FBMCQ expression must resubmit property kind, bound,
    bound origin, and assumption basis; the Controller reparses the exact query
    and rejects any mismatch. The new expression/SHA must not duplicate another
    chain's latest active expression.

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

    When not to use: do not use to add a new Root, change basis/scope,
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
        evidence scope, or to add a different semantic obligation. Change
        ``required_function_families`` only when the expression's evidence route
        changes for the same obligation.

        Parameters
        ----------
        ``assertion_chain_id`` names one existing chain. ``assert`` is one Python
        expression string. For a single ``fbmcq(...)`` call, provide matching
        ``formal_property_kind``, ``formal_bound``, ``formal_bound_origin`` and
        ``formal_assumption_basis_ids``. For a non-formal expression, leave the
        first three null and the basis list empty. ``reason`` is required natural
        language; an ``analysis_bound`` rationale must name the finite bound and
        explain why that horizon fits the proposition. Every assumption basis ID
        must already be a frozen ID in the inherited assertion ``basis_ids``;
        arbitrary profile-like IDs are not accepted without a frozen registry.
        ``required_function_families`` is optional: omit it to inherit the prior
        route, or provide the complete non-empty route for this new version.

        Returns
        -------
        Accepted revisions return the new version ID, SHA, and inherited metadata.
        Rejections return ``invalid_arguments`` and old-latest preservation data.

        Execution
        ---------
        The Controller checks chain existence and latest expression uniqueness,
        then appends ``@vN`` with inherited required/root/unit/basis/scope and
        either inherited or explicitly replaced function-family metadata.

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

        return execute(
            registry,
            kwargs["assertion_chain_id"],
            kwargs["assert"],
            kwargs["reason"],
            formal_property_kind=kwargs.get("formal_property_kind"),
            formal_bound=kwargs.get("formal_bound"),
            formal_bound_origin=kwargs.get("formal_bound_origin"),
            formal_assumption_basis_ids=kwargs.get(
                "formal_assumption_basis_ids"
            ),
        )

    return SimpleStructuredTool(
        func=revise_assertion,
        name="revise_assertion",
        description=revise_assertion.__doc__ or "revise_assertion",
        args_schema=ReviseAssertionInput,
    )
