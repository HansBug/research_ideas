from __future__ import annotations

from pydantic import Field

from ..schemas.coverage import CoveragePlan
from ..schemas.tools import SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


class RegisterCoveragePlanInput(StrictToolModel):
    plan: CoveragePlan
    reason: str = Field(min_length=1)


def execute(registry: CoverageRegistry, plan: CoveragePlan, reason: str) -> dict[str, object]:
    """Register the append-only Discover coverage plan in a controller registry."""

    return registry.register_plan(plan.model_dump(mode="json", by_alias=True), reason=reason)


def build_tool(registry: CoverageRegistry) -> SimpleStructuredTool:
    """Purpose: create the ``register_coverage_plan`` tool for one Discover attempt.

    Parameters: ``registry`` is the Controller-owned append-only
    ``CoverageRegistry`` closed over before Agent dispatch and already seeded
    with Controller-owned frozen InputSegment, CoverageRequirement, and SourceFact
    IDs. The Agent-facing
    input schema has exactly ``plan`` and ``reason``. ``plan`` may contain only
    Agent-declared ``coverage_units``, ``segment_dispositions``, optional
    ``fact_dispositions``, ``proposition_roots``/``roots``, and
    ``logical_assertions``/``assertions``; it must not submit or overwrite
    ``input_segments``, ``coverage_requirements``, or ``source_facts``. ``reason`` is the natural-language
    rationale for freezing this exact coverage analysis; it is saved verbatim and
    is not parsed for IDs.

    Returns: a LangChain ``StructuredTool`` named ``register_coverage_plan``.
    Successful calls return ``execution_status=completed``, counts for units,
    roots, assertion chains, the accepted latest assertion records, and
    ``registered_reference_closure=true`` and
    ``registered_coverage_complete=false`` until execution closes. Rejected calls
    return ``execution_status=invalid_arguments`` plus machine-readable errors.

    Execution: the tool validates the two-way coverage contract before accepting
    the plan: every frozen clause requirement must map to exactly one shared
    clause Unit and to at least one same-unit required assertion basis; every
    behavior-relevant fact must be covered by a Unit, may not be dispositioned,
    and must be directly verified by a fact-specific compatible assertion whose
    basis includes that fact ID; every CoverageRequirement must carry the same
    segment/dimension and an allowed evidence-family route;
    each in-scope CoverageUnit has exactly one Root, each Root has at least one
    required assertion, and latest assertion expressions/SHA values are unique
    across chains. Required function families must be one of exactly
    ``structure/relation/effect/simulation/formal/mapping``. Acceptance is
    append-only and freezes the initial v1 assertion versions; a second
    registration is rejected.

    Failure semantics: Agent-supplied ``input_segments``/``coverage_requirements``/
    ``source_facts``, malformed references, uncovered frozen segments,
    requirements, defect-family rows, or facts,
    unit/root-cardinality violations, roots without required assertions,
    duplicate latest expressions, or a repeated registration reject the whole
    plan and preserve the previous registry state. Rejection records are still
    appended for audit.

    Evidence limitations: registration proves reference closure over the
    Controller-frozen clause/cue worklist, source facts, assertion routes, and
    assertion-shape policy. Final exhaustive coverage still requires subsequent
    terminal deterministic evaluation, no incomplete Root, and a current
    passing ``review_discovery_coverage`` result.

    Permissions: this tool writes only to the in-memory/current-run
    append-only registry supplied by the Controller. It cannot read arbitrary
    paths, refresh model/source state, call an LLM, evaluate assertions, access
    reference/gold assets, execute shell/Python outside the registry, or submit
    the final discovery.

    When to use: call once after reading the FCSTM guide and task, after the
    Agent has split segments/requirements/facts into CoverageUnits/Roots and
    written all initial required assertions.

    When not to use: do not call for incremental assertion execution, revisions,
    source tracing, final submit, ad-hoc model queries, or to hide a behavioral
    segment behind a disposition.

    Examples: ``{"plan":{"segment_dispositions":[],"fact_dispositions":[],"coverage_units":[...],"proposition_roots":[...],"logical_assertions":[...],"rationale":"Complete issue-agnostic two-way coverage."},"reason":"Freeze the Controller-closed worklist before evaluating every latest assertion."}``.
    """

    def register_coverage_plan(plan: CoveragePlan, reason: str) -> dict[str, object]:
        """Purpose
        -------
        Freeze the Discover Agent's declared coverage registry exactly once.

        When to use
        -----------
        Use after ``read_task`` and before any ``eval_assert`` call, when every
        frozen CoverageRequirement and behavior-relevant segment/fact has a valid
        route and every in-scope unit has one Root plus required assertions.

        When not to use
        ----------------
        Do not use for assertion execution, revisions, source lookup, submission,
        batching, or re-registering a modified plan after evaluation begins.

        Parameters
        ----------
        ``plan`` contains dispositions, units, roots, and assertions. Every NL
        Unit supplies ``requirement_ids`` and ``dimensions`` exactly as returned
        by ``read_task``.
        Frozen InputSegments/CoverageRequirements/SourceFacts are Controller
        inputs, not Agent-writable fields. ``reason`` is saved verbatim.

        Returns
        -------
        ``execution_status=completed`` with accepted counts and latest assertion
        records, or ``invalid_arguments`` with rejection errors and limitations.

        Execution
        ---------
        The Controller checks frozen clause/requirement/fact closure, direct
        requirement-to-assertion and fact-to-executable-predicate links, all
        requirement-to-evidence-family compatibility and semantic assertion
        shape, CoverageUnit<->Root
        cardinality, at least one required
        assertion per Root, and unique latest
        assertion expression/SHA across chains. Function family values are
        restricted to ``structure/relation/effect/simulation/formal/mapping``.
        Accepted data is append-only.

        Failure semantics
        -----------------
        Any gate failure rejects the complete registration. No partial plan,
        Root, or assertion becomes latest; a rejection record preserves the
        original ``reason`` and gate diagnostics.

        Evidence limitations
        --------------------
        Registration certifies the frozen exhaustive matrix is fully referenced.
        It does not mark final coverage complete and does not replace assertion
        execution or source attribution.

        Permissions
        -----------
        Current-run registry only; no arbitrary paths, network, shell, LLM calls,
        reference/gold inputs, or assertion eval.

        Examples
        --------
        ``{"plan":{"segment_dispositions":[],"fact_dispositions":[],"coverage_units":[{"coverage_unit_id":"CU-1","unit_kind":"behavior_obligation","segment_ids":["SEG-NL-001"],"source_fact_ids":["FACT-1"],"requirement_ids":["REQ-001-TRANSITION-01"],"dimensions":["transition"],"statement":"go reaches Done","rationale":"One repairable target obligation."}],"proposition_roots":[{"node_id":"ROOT-1","coverage_unit_id":"CU-1","statement":"go reaches Done","rationale":"Root for CU-1."}],"logical_assertions":[{"assertion_chain_id":"ASSERT-1","root_node_id":"ROOT-1","coverage_unit_id":"CU-1","required":true,"assert":"transition_exists(source='Root.A', event='Root.go', target='Root.Done')","basis_ids":["SEG-NL-001","REQ-001-TRANSITION-01"],"obligation_signature":"go-handler","required_function_families":["relation"],"evidence_scope":{"semantic_profile":"single_active_leaf_fcstm_v1","max_steps":null,"max_time":null,"abstraction":"discrete_event","claim_strength":"transition_fact"},"rationale":"Positive target obligation."}],"rationale":"All issue-agnostic coverage rows are closed."},"reason":"Register the strict worklist before eval."}``
        """

        if isinstance(plan, dict):
            plan = CoveragePlan.model_validate(plan)
        return execute(registry, plan, reason)

    return SimpleStructuredTool(
        func=register_coverage_plan,
        name="register_coverage_plan",
        description=register_coverage_plan.__doc__ or "register_coverage_plan",
        args_schema=RegisterCoveragePlanInput,
    )
