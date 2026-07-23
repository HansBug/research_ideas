from __future__ import annotations

from typing import Any

from pydantic import Field, create_model

from ..schemas.tools import NonBlankString, SimpleStructuredTool, StrictToolModel
from .coverage_registry import CoverageRegistry


EvalAssertInput = create_model(
    "EvalAssertInput",
    __base__=StrictToolModel,
    **{
        "assert": (str, Field(min_length=1)),
        "reason": (NonBlankString, ...),
    },
)


def execute(registry: CoverageRegistry, assert_text: str, reason: str) -> dict[str, object]:
    """Evaluate exactly one registered latest assertion expression."""

    return registry.eval_assert(assert_text, reason=reason)


def build_tool(registry: CoverageRegistry) -> SimpleStructuredTool:
    """Purpose: create the single-assertion ``eval_assert`` tool.

    Parameters: ``registry`` is the Controller-owned append-only
    ``CoverageRegistry`` with a previously accepted coverage plan. The public
    Agent-facing schema is strictly and only ``assert`` plus ``reason``; internal
    code uses ``assert_text`` because ``assert`` is a Python keyword. No batch,
    array, Root ID, assertion ID, executor kind, model selector, or expected
    outcome field is accepted.

    Returns: a ``StructuredTool`` named ``eval_assert``. It returns the matched
    assertion chain/version/root/unit IDs, expression SHA-256, model hash, strict
    bool value when available, ``match_status`` (``matches``/``contradicts``/
    ``inconclusive``), function-call trace, limitations, exception details,
    saved original ``reason``, generated ``reason_context``, and record ID.

    Execution: the Controller matches the provided expression text exactly
        against one and only one registered latest assertion. It then directly
        evaluates that expression in the frozen eval environment with whitelisted
        pure builtins, registered vars/functions, dependency-provenance audit,
        a runtime gate for all declared required function families, and no
        semantic DSL conversion.

    Failure semantics: unregistered expressions, non-unique latest expression
    matches, arrays/batches/extra fields, non-bool returns, exceptions, dunder or
    untracked dependencies, no model evidence, and missing required function
    families fail closed. Invalid public schema calls do not execute. Runtime
    failures become inconclusive assertion records rather than confirmed issues.
    An inconclusive latest required assertion blocks terminal submission. If
    other latest assertions still have no first evaluation, the returned action
    names the exact next missing expression so the finite initial worklist is
    completed without repeating the inconclusive expression. Once no latest
    assertion is missing, the Controller forces ``revise_assertion`` until the
    same obligation has a stable ``matches`` or ``contradicts`` result; no
    partial-success output is allowed.

    Evidence limitations: ``True`` only means the registered positive assertion
    matched current frozen evidence; ``False`` only means that assertion
    contradicted it. This tool does not prove semantic coverage, source-level
    attribution, absence of hidden defects, Repair eligibility, or safety against
    malicious Python code.

    Permissions: evaluate exactly one already registered latest assertion in the
    current run. No arbitrary paths, network, shell, environment variables,
    hidden reference/gold inputs, model refresh, batch execution, or submission.

    When to use: call at least once per latest required assertion after
    ``register_coverage_plan`` accepts the plan. Each call evaluates one expression.
    A diagnostic retry of the same latest version is append-only and must explain
    why it is repeated; projection uses the latest stable terminal attempt. After
    ``revise_assertion`` creates a new version, execute that new exact expression.

    When not to use: do not use for ad-hoc predicates, combined multi-Root
    checks, model exploration, source tracing, final submit, or expressions that
    are negative-by-convention instead of positive obligations.

    Examples: ``{"assert":"transition_exists(source='Root.Searching', event='Root.Task_Assignment', target='Root.Attack')","reason":"ROOT-002 requires the Task_Assignment transition into Attack; evaluate the registered positive relation assertion."}``.

    Supported vars/functions: V1 exposes no Agent-defined free variables. Only
    Controller-registered frozen views explicitly listed by ``read_task`` may be
    referenced. Functions are ``states``, ``events``,
    ``variables``, ``transitions``, ``effects``, ``initial_child``,
    ``transition_exists``, ``guards_overlap``, ``effect_delta``,
    ``effect_deltas``, ``simulate``,
    ``fbmcq``, ``mapped_source_refs``, ``mapped_fcstm_refs``, and
    ``bound_model_refs``. Pure builtins are exactly ``abs/all/any/bool/float/int/
    iter/len/list/max/min/round/set/sorted/str/sum/tuple``.
    ``SimulationObservation`` exposes ``cycles/final/
    model_sha256/requested_initialization/effective_initialization``;
    ``CycleObservation`` exposes ``index/is_ended/active_states/
    variables/input_events/consumed_events/unconsumed_events/
    fired_transitions/is_active``. Use ``.final.is_ended is True`` for an NL
    top-level final/completion obligation; after termination there is no active
    state to query.
    ``FBMCQObservation`` exposes ``canonical_query/status/holds/bound/witness/
    replay_status``.

    Positive bool principle: write the assertion so ``True`` means the model
    satisfies the Root's obligation and ``False`` means the obligation is
    contradicted. Do not add ``expected`` fields or invert the meaning in
    ``reason``.

    Guide/family/registration/single-call/failed-call semantics: FCSTM guide and
    task reading precede registration; expressions using ``fbmcq(...)`` require
    the FBMCQ guide before registration; planned required function families must
    be observed at runtime; exact latest registration is mandatory; every call
    evaluates one expression only; failures are saved as inconclusive/invalid
    records and never publish a Root verdict by themselves.
    """

    def eval_assert(**kwargs: Any) -> dict[str, object]:
        """Purpose
        -------
        Execute one registered latest positive Python bool assertion.

        When to use
        -----------
        Use after ``register_coverage_plan`` for each latest required assertion,
        one expression per tool call. Diagnostic retries remain append-only.

        When not to use
        ----------------
        Do not use for batches, arrays, Root IDs, assertion IDs, ad-hoc
        expressions, exploration, source attribution, final submit, or combined
        multi-Root obligations.

        Parameters
        ----------
        Public schema fields are exactly ``assert`` and ``reason``. ``assert`` is
        the complete Python expression and must exactly match one unique latest
        registered assertion expression. ``reason`` is trimmed and saved.

        Returns
        -------
        Matched chain/version/root/unit IDs, expression SHA, bool value when
        strict bool, ``match_status``, call trace, limitations, exception details,
        original ``reason``, generated ``reason_context``, and record ID.

        Execution
        ---------
        Match by exact latest expression/SHA context, audit dependencies, direct
        ``eval`` with frozen vars/functions and pure builtins, require every
        declared item in ``required function families`` to appear in the actual
        call trace, and append one evaluation record.

        Failure semantics
        -----------------
        Unknown/non-unique latest expression, schema extras, non-bool return,
        exception, untracked/dunder dependency, no model evidence, or missing
        family fails closed. Failed eval is inconclusive; invalid match does not
        execute. When later registered assertions are still missing, recovery
        feedback identifies the exact next missing expression and postpones
        revision until every latest assertion has received one first evaluation.

        Evidence limitations
        --------------------
        A bool result proves only this registered expression against frozen
        evidence, not semantic completeness or source attribution.

        Permissions
        -----------
        Single current-run expression eval only; no arbitrary paths, network,
        shell, environment, reference/gold inputs, refresh, or batch.

        Examples
        --------
        ``{"assert":"len(states(parent='Root.Searching', recursive=False)) == 3","reason":"ROOT-001 checks the registered structure-family assertion for exactly three search-area states."}``

        Supported vars/functions
        ------------------------
        V1 has no Agent-defined free variables. Use only the following exact
        Controller-registered functions and keyword names:

        - ``states(parent=None, recursive=True, name=None) -> tuple[State]``.
          ``parent`` selects descendants; use ``recursive=False`` for direct
          children. ``name`` is exact name/path matching, not fuzzy search.
        - ``events(name=None) -> tuple[Event]`` and
          ``variables(name=None) -> tuple[Variable]``. Empty tuples are stable
          absence facts; do not infer why an item is absent.
        - ``initial_child(state) -> str | None``. It returns one structured
          initial target; an ambiguous/malformed initial relation is unsupported.
        - ``transitions(source=None, event=None, target=None, forced=None) ->
          tuple[Transition]``. Filters are exact qualified path/name matches.
        - ``transition_exists(source=None, event=None, target=None) -> bool``.
          Use this for required or forbidden transition relations. Include
          ``target`` whenever the NL constrains the destination; event existence
          alone is a weaker and invalid substitute. This checks a static model
          relation; it does not by itself observe the final runtime state across
          hierarchical execution. Use simulation instead when the NL proposition
          is about the behavior produced after a trigger and a short bounded setup
          can exercise it.
        - ``guards_overlap(left_ref, right_ref) -> bool`` where refs are
          ``transition:T<n>`` or ``transition:<n>``. It decides missing/equal
          guards only; distinct non-empty guards are unsupported rather than
          guessed.
        - ``effects(source=None, event=None, target=None, variable=None) ->
          tuple[Transition]`` returns matching transitions carrying effects. A
          tuple is not a strict bool: use ``bool(effects(...))`` only when mere
          existence is exactly the intended proposition, never for a directional
          decrease/increase. Do not write ``effects(...) and ...`` because
          an empty tuple can become the final non-bool result through Python
          short-circuit semantics.
        - ``effect_delta(source=None, event=None, target=None, variable=<name>)
          -> int | float | None``. Compatibility helper for one named variable.
          ``None`` means no matching assignment; one ambiguous transition,
          missing/ambiguous variable, nonnumeric initial value, or a complex
          effect expression is unsupported. Keep this only when the variable name
          is explicitly grounded in the frozen source/model facts.
        - ``effect_deltas(source=None, event=None, target=None) ->
          tuple[(variable, delta), ...]``. Open effect-evidence helper for all
          parseable numeric assignments on matching transitions. It returns an
          empty tuple for stable absence (no matching transition, no effect, no
          assignments, or no variables to report) and never requires a sentinel
          or invented variable-name probe. For NL that says “some count/resource
          decreases” and does not ground one exact variable name, prefer
          ``any(delta < 0 for _, delta in effect_deltas(...))``. Because the
          helper itself is registered as the ``effect`` family, this expression
          still leaves effect evidence in the runtime call trace even when the
          tuple is empty and ``any(...)`` returns ``False``. Use an exact delta
          only when the source explicitly requires that amount.
        - ``simulate(cycles=<list[list[str]]>, initial_state=None,
          initial_vars=None) -> SimulationObservation``.
          Every outer item is exactly one FCSTM cycle; each inner list is the
          complete event set for that cycle. ``[]`` is an explicit eventless
          cycle. No hidden initialization cycle is inserted. Cold starts must
          begin with ``[]``. With ``initial_state=None``, a literal partial
          ``initial_vars`` mapping may override named declared variables; omitted
          variables keep their declaration initializers and the effective full
          mapping is recorded. A hot start requires one exact ``initial_state`` and
          a complete literal ``initial_vars`` mapping and is already initialized,
          so it does not require a leading ``[]``. For a local "while in S, E
          leads to T" proposition, put E in the first hot-start caller cycle and
          verify that the effective initialization is in S, E appears in that
          cycle's ``consumed_events`` rather than ``unconsumed_events``, and T is
          active after that cycle. A leading empty cycle may leave S through a
          completion transition before E; final-state coincidence alone is not
          event-causality evidence. A SimulationObservation exposes
          ``.requested_initialization``, ``.effective_initialization``,
          ``.cycles``, and ``.final``; a CycleObservation exposes ``.index``,
          ``.is_ended``, ``.active_states``, ``.variables``, ``.input_events``,
          ``.consumed_events``, ``.unconsumed_events``,
          ``.fired_transitions``, ``.limitations`` and
          ``.is_active(state)``. For an NL top-level final/completion result,
          assert ``simulate(...).final.is_ended is True``; a terminated runtime
          has no active state, so do not call ``is_active`` after termination or
          append a diagnostic cycle after the terminating event. Reusing an
          external event in a later non-terminal cycle is legal; consumed-event
          accounting is not a one-use scenario rule. In hierarchical FCSTM
          execution the same supplied event may appear more than once in one
          cycle's ``consumed_events`` while nested and ancestor-level forced
          transitions process it. Check membership and absence from
          ``unconsumed_events``; never require a count of exactly one or treat
          duplicate labels alone as an issue. Prefer this function when
          the NL asks what behavior occurs after a trigger; assert the resulting
          active state or termination rather than inferring it from one static
          transition relation.
        - ``fbmcq(query) -> FBMCQObservation``. ``query`` is one complete
          official FBMCQ string with the bound inside it, for example
          ``check reach <= 8: active("Root.Attack");``. Read
          ``read_fbmcq_guide`` before registering/revising such an assertion.
          Assert ``.holds is True`` or the positive property actually required.
          Available fields are ``.canonical_query/.status/.holds/.bound/
          .witness/.replay_status``. Parse/solver/replay uncertainty is
          inconclusive, never ``False``.
        - ``mapped_source_refs(fcstm_ref) -> tuple[str, ...]`` and
          ``mapped_fcstm_refs(source_ref) -> tuple[str, ...]`` expose frozen
          source-trace mappings. They support attribution, not behavior truth.
        - ``bound_model_refs(coverage_unit_id, fact_kind=None) -> tuple[str,
          ...]`` returns the qualified refs of SourceFacts registered to one
          CoverageUnit. It may support a binding explanation but must not be the
          sole or primary truth condition for a behavioral Root.

        Immutable views expose the following exact public field families. A field
        that is valid for the view contract but absent from one concrete record
        evaluates as ``None``; an unlisted field is rejected before eval.

        - State: ``path/name/parent_path/is_leaf/is_pseudo/is_composite/substates/
          initial_targets``.
        - Event: ``qualified_name/name/scope/used_by/is_declared/is_used``.
        - Variable: ``qualified_name/name/type/init_value/read_in_states/
          written_in_states/read_in_guards/written_in_effects``.
        - Transition: ``from_path/to_path/event/event_scope/guard/effect/
          effect_self_assigns/is_forced/forced_origin/transition_index``.
        - Simulation and formal observations use only the fields listed in their
          function entries above; source mappings expose ``source_ref/model_ref/
          relation_policy/confidence/producer/raw``.

        Unknown fields, methods, dunder access, imports and unregistered names
        are rejected before eval. Prefer direct function filters when they express
        the same proposition more simply, but public view fields such as
        ``states(name='Root.Idle')[0].is_leaf`` are supported evidence rather than
        an unsupported workaround.

        Pure builtins are exactly ``abs/all/any/bool/float/int/iter/len/list/
        max/min/round/set/sorted/str/sum/tuple``. They are composition helpers,
        not model evidence. A valid assertion must actually call at least one
        registered evidence function, and the runtime call trace must contain
        every family declared in ``required_function_families``.

        Generator and binding rules
        ---------------------------
        Comprehension targets such as ``name`` in ``any(check(name) for name in
        [...])`` are locally bound names and are allowed by the provenance audit.
        Every function, view field, method, and outer name remains registry-bound.
        Literal candidate names must come from the frozen NL/source terminology or
        actual ``variables()`` inventory and the assertion rationale must explain
        the binding. Do not add unrelated aliases merely to make a missing-effect
        assertion return the desired value. For open directional effects, prefer
        ``effect_deltas(...)`` over a fabricated ``effect_delta(..., variable=...)``
        probe. ``effect_delta.variable`` must be one exact literal name from the
        frozen model inventory; concatenated/computed probes are rejected. An open
        ``effect_deltas`` generator must not filter a hand-picked variable and must
        bind one exact literal source/event/target transition. For
        stable missing variables/effects, ``effect_deltas(...)``
        returns ``()`` so ``any(delta < 0 for _, delta in effect_deltas(...))``
        is strict ``False`` while the ``effect`` family is still traced; the
        legacy ``effect_delta(...)`` returns ``None`` and ``(delta or 0) < 0`` is
        also strict ``False`` for grounded variable-specific assertions.
        Ambiguous transitions or unsupported expressions remain inconclusive.

        Expression design principles
        ----------------------------
        One expression serves one Root and one independently repairable positive
        obligation. ``True`` must always mean “the frozen FCSTM satisfies this
        obligation”; ``False`` must mean contradiction. Do not use a bare
        constant, model/name coincidence, mapping count, ``expected`` field,
        batch/list of assertions, multiple Roots joined by ``and``, or an
        exploratory trace result as the verdict. Cardinality and directional
        effect assertions must be direct top-level positive predicates; an ``or``
        branch cannot provide a second way to make the assertion pass. Cardinality
        must count the NL-named model object, never ``bound_model_refs`` or an
        unrelated inventory. Multiple complementary
        assertions for one Root are allowed, but register and execute each one
        separately.

        Correct examples include:

        - required target:
          ``transition_exists(source='Root.Active', event='Root.stop',
          target='Root.Off')``;
        - forbidden transition:
          ``not transition_exists(source='Root.Moving',
          event='Root.Open_Door')``;
        - exactly three direct areas:
          ``len(states(parent='Root.Searching', recursive=False)) == 3``;
        - open decrement without a variable-name probe:
          ``any(delta < 0 for _, delta in effect_deltas(source='Root.Attack',
          event='Root.Attack_Complete', target='Root.Searching'))``;
        - grounded variable-specific decrement:
          ``(effect_delta(source='Root.Attack', event='Root.Attack_Complete',
          variable='uav_count') or 0) < 0``;
        - bounded cycle path:
          ``simulate(cycles=[[], ['Root.go']]).final.is_active('Root.Done')``;
        - local hot-start event behavior:
          ``simulate(initial_state='Root.Idle', initial_vars={},
          cycles=[['Root.go']]).final.is_active('Root.Done')``; inspect the same
          recorded call's cycle-0 consumed/unconsumed events during coverage
          review before attributing the target state to ``Root.go``;
        - top-level completion:
          ``simulate(cycles=[[], ['Root.stop']]).final.is_ended is True``;
        - bounded formal property:
          ``fbmcq('check reach <= 8: active("Root.Done");').holds is True``.

        Positive bool principle
        -----------------------
        ``True`` means the model satisfies the positive Root obligation; ``False``
        means contradiction. Do not use an ``expected`` field.

        Guide/family/registration/single-call/failed-call semantics
        ----------------------------------------------------------
        FBMCQ assertions require the FBMCQ guide before registration; planned
        families must be observed at runtime; exact latest registration is
        required; one call evaluates one assertion; failed calls are recorded but
        do not publish a verdict.
        """

        return execute(registry, kwargs["assert"], kwargs["reason"])

    return SimpleStructuredTool(
        func=eval_assert,
        name="eval_assert",
        description=eval_assert.__doc__ or "eval_assert",
        args_schema=EvalAssertInput,
    )
