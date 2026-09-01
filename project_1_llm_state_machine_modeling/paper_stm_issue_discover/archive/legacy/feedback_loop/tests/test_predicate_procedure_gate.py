"""Gate D: the named predicate fixes which procedure may close it.

Issue #170 C3.  Pair 0006 produced a false positive with every existing gate
green: the requirement asked whether the system *reaches* FormationAdjustment
after interception, and the primary assertion answered whether an *edge to it is
declared*.  Those are different questions, and the easier one was accepted.

These tests pin the gate, and equally pin what it must not break: a Family S
requirement is legitimately closed by a structural query, and a requirement with
no predicate keeps the pre-vocabulary behaviour.
"""

from __future__ import annotations

import pytest

from paper_stm_feedback_loop.discover.capability import called_evidence_functions
from paper_stm_feedback_loop.discover.predicates import (
    PREDICATE_BY_NAME,
    PREDICATES,
    procedure_mismatch,
)

DECLARED = 'edge_declared(source="R.A", trigger="R.e", target="R.B") is True'
SIMULATED = 'occupancy_after(source="R.A", trigger="R.e", target="R.B") is True'
FORMAL = 'invariant(scope="R.A", condition=\'active("R.B")\', bound=3) is True'


def _check(predicate: str, expression: str):
    return procedure_mismatch(predicate, called_evidence_functions(expression))


def test_declaration_query_cannot_close_a_runtime_claim():
    """The 0006 shape: this is the substitution the gate exists to stop."""

    mismatch = _check("occupancy_after", DECLARED)
    assert mismatch is not None
    assert mismatch[0] == "occupancy_after"
    assert "must be discharged by calling occupancy_after" in mismatch[1]
    assert "edge_declared" in mismatch[1]


def test_runtime_claim_closed_by_simulation_passes():
    assert _check("occupancy_after", SIMULATED) is None


def test_structural_claim_closed_by_structural_query_passes():
    """The gate must not punish Family S for being cheap."""

    assert _check("edge_declared", DECLARED) is None


def test_property_claim_needs_bounded_checking():
    assert _check("invariant", SIMULATED) is not None
    assert _check("invariant", FORMAL) is None


def test_absent_or_unknown_predicate_falls_back():
    """v1/v2 artifacts and non-adopting producers must still run."""

    assert _check("", DECLARED) is None
    assert _check("not_a_predicate", DECLARED) is None


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_every_predicate_accepts_its_own_procedure(predicate):
    """A predicate whose own procedure trips the gate would be unusable."""

    assert procedure_mismatch(predicate, frozenset({predicate})) is None


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_no_predicate_lists_its_own_procedure_as_a_locator(predicate):
    """A locator is by definition weaker; listing the procedure would be a hole."""

    entry = PREDICATE_BY_NAME[predicate]
    for locator in entry.locators:
        assert not locator.startswith(f"{entry.procedure_function}("), locator


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_no_other_predicate_can_close_this_claim(predicate):
    """Every predicate asks a different question; none may substitute."""

    for other in (p.name for p in PREDICATES):
        if other == predicate:
            continue
        assert procedure_mismatch(predicate, frozenset({other})) is not None


def test_gate_runs_inside_convert_assertions_and_names_the_requirement():
    """End to end through the node, so the gate is not merely importable."""

    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.schemas import (
        AssertionScript,
        AssertionSpec,
        Requirement,
        RequirementSet,
    )

    requirements = RequirementSet(
        revision=1,
        requirements=(
            Requirement(
                requirement_id="REQ-006",
                statement="After interception the system moves to FormationAdjustment.",
                predicate="occupancy_after",
                predicate_bindings={
                    "source": "R.Intercepting",
                    "trigger": "R.Attack_Complete",
                    "target": "R.FormationAdjustment",
                },
                verification_kind="behavior",
            ),
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            AssertionSpec(
                assertion_id="AST-REQ-006-01",
                requirement_id="REQ-006",
                role="primary",
                coverage_key="k1",
                aggregation_group="g1",
                rationale="Fixture assertion; rationale not under test here.",
                evidence_family="relation",
                description="d",
                expression=DECLARED,
                failure_message="[REQ-006][AST-REQ-006-01] m",
            ),
        ),
    )

    class Responder:
        def invoke_structured(self, *args, **kwargs):
            return script

    from paper_stm_feedback_loop.discover.schemas import FrozenDiscoverInputs

    frozen = FrozenDiscoverInputs(
        run_id="gate",
        natural_language="nl",
        stm_text="stm",
        input_hashes={"nl": "0" * 64},
        tool_env_hash="0" * 64,
        profile="gate",
        language="en-US",
    )
    out = nodes.convert_assertions(
        {
            "requirement_set": requirements,
            "node_execution_records": (),
            "frozen_inputs": frozen,
        },
        Responder(),
    )
    # The gate reports through the node's repair channel rather than crashing the
    # run, so assert on the recorded reason.
    blob = repr(out)
    assert "must be discharged by calling occupancy_after" in blob, blob[:600]


# --------------------------------------------------------------------------
# Model vocabulary: the producers must be told the exact declared paths
# --------------------------------------------------------------------------

VOCAB_MODEL = """def int c = 0;
state Root {
    event go;
    event stop;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : /go;
}
"""


def _frozen_for(model: str):
    from paper_stm_feedback_loop.discover.nodes import _fallback_prepare
    from paper_stm_feedback_loop.discover.schemas import DiscoverInput

    return _fallback_prepare(
        DiscoverInput(
            run_id="vocab",
            natural_language="Idle shall reach Done on go.",
            stm_text=model,
            language="en-US",
        )
    )


def test_declared_events_are_not_dropped_from_the_vocabulary():
    """States carry `path`, events carry `qualified_name`.

    Reading `path` for both yielded zero events, so a fabricated event reference
    could never be caught -- the pair-0029 `event="/pick"` defect class.
    """

    frozen = _frozen_for(VOCAB_MODEL)
    assert frozen.model_vocabulary["states"], "states must be listed"
    assert frozen.model_vocabulary["events"], "events must be listed"
    assert any(item.endswith(".go") for item in frozen.model_vocabulary["events"])
    assert any(item.endswith(".stop") for item in frozen.model_vocabulary["events"])
    assert frozen.model_vocabulary["variables"], "declared variables must be listed"


def test_known_model_paths_covers_states_and_events():
    """This is what `unresolved_model_references` intersects against."""

    frozen = _frozen_for(VOCAB_MODEL)
    assert len(frozen.known_model_paths) >= 6
    assert any(p.endswith(".go") for p in frozen.known_model_paths)
    assert any(p.endswith(".Idle") for p in frozen.known_model_paths)


@pytest.mark.parametrize(
    "renderer_name",
    [
        "render_requirement_split_input",
        "render_requirement_review_input",
        "render_assertion_conversion_input",
    ],
)
def test_every_producer_payload_carries_the_vocabulary(renderer_name):
    """A producer asked to bind exact paths must be shown them."""

    import json

    from paper_stm_feedback_loop.discover import renderer as R
    from paper_stm_feedback_loop.discover.schemas import (
        Requirement,
        RequirementCoverageProjection,
        RequirementSet,
    )

    frozen = _frozen_for(VOCAB_MODEL)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            Requirement(
                requirement_id="REQ-001",
                statement="s",
                verification_kind="structure",
            ),
        ),
    )
    render = getattr(R, renderer_name)
    if renderer_name == "render_requirement_split_input":
        payload = render(frozen)
    elif renderer_name == "render_requirement_review_input":
        payload = render(frozen, requirements, RequirementCoverageProjection(covered_requirement_ids=("REQ-001",)))
    else:
        payload = render(frozen, requirements)
    vocabulary = json.loads(payload)["declared_model_vocabulary"]
    assert vocabulary["states"], renderer_name
    assert vocabulary["events"], renderer_name


# --------------------------------------------------------------------------
# C4: path() as a locator, now reachable only through the topology facade
# (it is deliberately not in the assertion namespace any more)

PATH_MODEL = """state Root {
    event go;
    event next;
    state Start;
    state Outer {
        state Inner;
        [*] -> Inner;
    }
    [*] -> Start;
    Start -> Outer : /go;
}
"""


def _path_api():
    from paper_stm_feedback_loop.assertions.pyfcstm_adapter import (
        check_fcstm,
        load_model_for_simulation,
    )
    from paper_stm_feedback_loop.assertions.topology import TopologyAPI

    inspect = check_fcstm(PATH_MODEL, "<test>").get("inspect") or {}
    machine = load_model_for_simulation(PATH_MODEL, "<test>")
    return TopologyAPI(inspect, machine).path


def test_composite_and_leaf_targets_agree():
    """Entering a composite means occupying a leaf inside it.

    Resolving against leaf-level nodes only made a composite target
    unreachable by construction, so the same question got opposite answers
    depending on how the target was spelled.
    """

    path = _path_api()
    composite = path(source="Root.Start", target="Root.Outer")
    leaf = path(source="Root.Start", target="Root.Outer.Inner")
    assert composite.exists is True
    assert leaf.exists is True
    assert composite.exists == leaf.exists


def test_positive_path_carries_transition_identity():
    """An empty transition_refs left a positive path with nothing to bind."""

    path = _path_api()
    result = path(source="Root.Start", target="Root.Outer")
    assert list(result.transition_refs), "a positive path must name its transitions"
    assert all(str(r).startswith("transition:") for r in result.transition_refs)


def test_path_still_declares_itself_guard_blind():
    """The over-approximation must stay visible; it may locate, never close."""

    path = _path_api()
    result = path(source="Root.Start", target="Root.Outer")
    assert result.guard_agnostic is True


# --------------------------------------------------------------------------
# Every predicate must be executable.  A predicate that can only ever raise is
# worse than a missing one: requirements routed to it land as `unsupported`
# while the vocabulary advertises that the claim is checkable.
# --------------------------------------------------------------------------

EXEC_MODEL = """def int c = 0;
state Root {
    event go;
    event stop;
    state Idle;
    state Busy { enter { c = 1; } }
    state Done;
    [*] -> Idle;
    Idle -> Busy : /go effect { c = c + 1; };
    Busy -> Done : /stop;
}
"""

EXEC_ARGS = {
    "state_declared": dict(state="Root.Idle", kind="leaf"),
    "variable_declared": dict(variable="c"),
    "event_declared": dict(event="Root.go"),
    "containment": dict(parent="Root", child="Root.Idle"),
    "initial_target": dict(composite="Root", child="Root.Idle"),
    "edge_declared": dict(source="Root.Idle", trigger="Root.go", target="Root.Busy"),
    "effect_declared": dict(
        source="Root.Idle", trigger="Root.go", variable="c", sign="positive"
    ),
    "action_declared": dict(state="Root.Busy", phase="entry"),
    "guard_distinguishable": dict(source="Root.Idle", trigger="Root.go"),
    "cardinality": dict(scope="Root", count=3),
    "occupancy_after": dict(source="Root.Idle", trigger="Root.go", target="Root.Busy"),
    "event_consumed": dict(source="Root.Idle", trigger="Root.go"),
    "stays_in": dict(source="Root.Idle", trigger="Root.stop"),
    "variable_delta_after": dict(
        source="Root.Idle", trigger="Root.go", variable="c", sign="positive"
    ),
    "reaches": dict(source="Root.Idle", target="Root.Done", within_cycles=3),
    "terminates": dict(scope="Root.Busy", trigger="Root.stop"),
    "invariant": dict(scope="Root.Idle", condition='active("Root.Idle")', bound=2),
    "response_within": dict(trigger="Root.go", response="Root.Busy", bound=3),
    "persists_until": dict(state="Root.Idle", release='active("Root.Busy")', bound=2),
}


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_every_predicate_returns_a_verdict_on_a_real_model(predicate):
    from paper_stm_feedback_loop.assertions import build_eval_environment

    assert predicate in EXEC_ARGS, f"{predicate} has no executability fixture"
    env = build_eval_environment(
        model_text=EXEC_MODEL,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=30_000,
        fbmcq_max_bound=6,
        fbmcq_process_wall_seconds=40.0,
    )
    value = env.globals[predicate](**EXEC_ARGS[predicate])
    assert isinstance(value, bool), f"{predicate} returned {value!r}, not a strict bool"


# --------------------------------------------------------------------------
# The gates read a complete `assert` statement, not a bare expression
# --------------------------------------------------------------------------


def test_gates_parse_a_complete_assert_statement():
    """Assertions arrive as statements; the gates must not need an expression.

    Parsing only in "eval" mode raised on every real assertion and returned an
    empty call set, so the procedure gate concluded no predicate had been called
    and rejected correct scripts until their repair budget ran out.  Both smoke
    cells died this way.
    """

    from paper_stm_feedback_loop.discover.capability import (
        called_evidence_functions,
        unresolved_model_references,
    )

    statement = (
        'assert state_declared(state="Root.Idle", kind="leaf") is True, '
        '"[REQ-001][AST-REQ-001-1] not a leaf"'
    )
    assert called_evidence_functions(statement) == frozenset({"state_declared"})
    assert procedure_mismatch("state_declared", called_evidence_functions(statement)) is None
    # And the reference gate must see the bindings inside a statement too.
    assert unresolved_model_references(statement, frozenset({"Root.Other"})) == (
        "state='Root.Idle'",
    )


def test_bare_expression_still_parses():
    """The prefix line of a script is a bare expression; keep both accepted."""

    from paper_stm_feedback_loop.discover.capability import called_evidence_functions

    assert called_evidence_functions(
        'state_declared(state="Root.Idle", kind="leaf")'
    ) == frozenset({"state_declared"})


# --------------------------------------------------------------------------
# Every predicate documents its own fields and shows three worked calls
# --------------------------------------------------------------------------


def _signature_arguments(name: str) -> tuple[set[str], set[str]]:
    """Return ``(required, optional)`` argument names from the rendered signature."""

    from paper_stm_feedback_loop.discover.predicates import PREDICATE_OPTIONS

    entry = PREDICATE_BY_NAME[name]
    required = set(entry.bindings)
    optional = {
        opt.split(":")[0].strip() for opt in PREDICATE_OPTIONS.get(name, ())
    } - required
    return required, optional


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_each_predicate_documents_every_field_and_shows_three_calls(predicate):
    """A field the producer cannot see the domain of is a field it guesses.

    Two matrix cells burned revisions on literals that were legal at runtime but
    absent from the prompt -- `kind="any"` was accepted by the implementation and
    missing from the signature.  Pinning the docs to the signature makes that
    class of drift a test failure instead of a wasted cell.
    """

    entry = PREDICATE_BY_NAME[predicate]
    required, optional = _signature_arguments(predicate)

    documented = {name for name, _ in entry.field_specs}
    assert required <= documented, f"{predicate}: undocumented bindings {required - documented}"
    assert documented <= required | optional, (
        f"{predicate}: field spec for non-existent argument {documented - required - optional}"
    )
    for name, spec in entry.field_specs:
        assert len(spec) > 15, f"{predicate}.{name} spec is too thin to act on: {spec!r}"

    assert len(entry.examples) >= 3, f"{predicate} shows only {len(entry.examples)} calls"


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_every_worked_call_is_well_formed_against_the_signature(predicate):
    """The examples are executable calls, not illustrative prose.

    Checked by parsing rather than by reading: an example that omits a required
    binding, or passes one the callable does not accept, teaches a call that
    fails at precheck.
    """

    import ast

    entry = PREDICATE_BY_NAME[predicate]
    required, optional = _signature_arguments(predicate)
    for example in entry.examples:
        call, _, _note = example.partition("  # ")
        node = ast.parse(call.strip(), mode="eval").body
        assert isinstance(node, ast.Call), example
        assert isinstance(node.func, ast.Name) and node.func.id == predicate, example
        assert not node.args, f"{predicate}: predicates are keyword-only: {example}"
        passed = {kw.arg for kw in node.keywords}
        assert required <= passed, f"{predicate}: missing {required - passed} in {example}"
        assert passed <= required | optional, (
            f"{predicate}: unknown argument {passed - required - optional} in {example}"
        )
        for kw in node.keywords:
            ast.literal_eval(kw.value)  # every value must be a literal


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_binding_and_call_forms_of_an_example_agree(predicate):
    """The splitter's dict and the converter's call must show the same values."""

    from paper_stm_feedback_loop.discover.predicates import binding_examples

    entry = PREDICATE_BY_NAME[predicate]
    import ast
    import json

    dicts = binding_examples(predicate)
    assert len(dicts) == len(entry.examples)
    for (payload, _note), example in zip(dicts, entry.examples):
        # Compare the parsed values, not the presence of marker substrings: a
        # dict rendered from a *different* example would still contain "Sys.".
        call = ast.parse(example.partition("  # ")[0].strip(), mode="eval").body
        expected = {
            kw.arg: str(ast.literal_eval(kw.value)) for kw in call.keywords
        }
        assert json.loads(payload) == expected, example


def test_both_prompts_carry_the_per_predicate_detail():
    """Rendering, not just the table -- the producer reads the prompt."""

    from paper_stm_feedback_loop.discover.predicates import callable_prompt, vocabulary_prompt

    vocabulary, callable_ref = vocabulary_prompt(), callable_prompt()
    for item in PREDICATES:
        for name, spec in item.field_specs:
            assert spec in vocabulary, f"{item.name}.{name} missing from vocabulary_prompt"
            assert spec in callable_ref, f"{item.name}.{name} missing from callable_prompt"
        for example in item.examples:
            assert example in callable_ref, f"{item.name}: {example} missing from callable_prompt"


# --------------------------------------------------------------------------
# A predicate that cannot answer both ways is a false-positive generator
# --------------------------------------------------------------------------

_DISCRIMINATION_HOLDS = """state Root {
    event go;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go;
    Busy -> Busy : /go;
}
"""

_DISCRIMINATION_FAILS = """state Root {
    event go;
    event other;
    state Idle;
    state Busy;
    state Elsewhere;
    [*] -> Idle;
    Idle -> Elsewhere : /go;
    Elsewhere -> Busy : /other;
}
"""


def _p_family_env(model):
    from paper_stm_feedback_loop.assertions import build_eval_environment

    return build_eval_environment(
        model_text=model,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=60,
        fbmcq_solver_timeout_ms=30_000,
        fbmcq_max_bound=6,
        fbmcq_process_wall_seconds=40.0,
    )


def test_response_within_tells_a_satisfying_model_from_a_violating_one():
    """It shipped constant-False once; a one-sided predicate is not evidence.

    `Idle -> Busy : /go` with a self-loop keeping the answer available satisfies
    the obligation; routing `go` to a third state that only later reaches Busy
    violates it.  A predicate that cannot separate those two would report every
    model defective.
    """

    holds = _p_family_env(_DISCRIMINATION_HOLDS).globals["response_within"](
        trigger="Root.go", response="Root.Busy", bound=3, source="Root.Idle"
    )
    fails = _p_family_env(_DISCRIMINATION_FAILS).globals["response_within"](
        trigger="Root.go", response="Root.Busy", bound=3, source="Root.Idle"
    )
    assert holds is True
    assert fails is False


@pytest.mark.parametrize("predicate", ["invariant", "response_within", "persists_until"])
def test_the_pseudo_initial_is_accepted_by_every_family_p_predicate(predicate):
    """`[*]` must mean the same thing everywhere it is legal.

    `terminates` and `reaches` read it as the cold start; the Family P
    predicates interpolated the literal straight into `init state("[*]")`, which
    the solver rejects.  A producer copying a legal binding from one predicate to
    another then got a failure with nothing in the message to diagnose it -- and
    `invariant(scope="[*]")` was a worked example in the prompt.
    """

    env = _p_family_env(_DISCRIMINATION_HOLDS)
    kwargs = {
        "invariant": dict(scope="[*]", condition='!active("Root.Busy")', bound=3),
        "response_within": dict(
            trigger="Root.go", response="Root.Busy", bound=3, source="[*]"
        ),
        "persists_until": dict(state="Root.Idle", release='active("Root.Busy")', bound=3),
    }[predicate]
    value = env.globals[predicate](**kwargs)
    assert isinstance(value, bool), f"{predicate} did not answer for the cold start"


def test_response_within_never_answers_about_a_source_nobody_chose():
    """Two ways that used to happen; both are silently-different questions.

    `source="[*]"` fell through to `_default_init()` via `or`, so an obligation
    stated about power-on was answered about some pinned leaf.  And the default
    itself was "the first leaf in inspect order", which ignored the trigger
    entirely -- the same claim answered True on a model whose first declared leaf
    happened to be the trigger's source and False on one declaring an unrelated
    state first, with declaration order deciding the verdict.

    So: the pseudo-initial still means no pin, and an ambiguous trigger is
    refused rather than resolved by picking one.
    """

    from paper_stm_feedback_loop.assertions.exceptions import UnsupportedEvidence
    from paper_stm_feedback_loop.assertions.predicate_api import PSEUDO_INITIAL

    env = _p_family_env(_DISCRIMINATION_HOLDS)
    api = env.predicates
    assert api._hot_startable(PSEUDO_INITIAL) is None
    with pytest.raises(UnsupportedEvidence, match="declared on 2 sources"):
        api._default_init("Root.go")
    # A trigger no transition carries names no source, so the obligation runs
    # unpinned rather than against an invented one.
    assert api._default_init("Root.nosuchevent") is None


# --------------------------------------------------------------------------
# A dead end is worse than a rejection
# --------------------------------------------------------------------------


def test_a_literal_primary_is_rejected_and_the_message_names_the_exit():
    """Pair 0006-gpt died with twelve revisions and a rationale, not a check.

    Its Requirement bound `release` to `<undeclared>`.  Every route the converter
    tried was closed: the predicate call is refused for an expression binding,
    each substitute release condition was rejected by the Reviewer as changing
    the obligation, and the twelfth attempt was `expression: "False"` with a
    paragraph explaining why the model cannot satisfy the claim.

    Rejecting that is correct -- a literal calls no predicate, so it asserts a
    defect on no evidence at all.  But the producer had nowhere left to go, and
    the run died at `convert_assertions`.  So the message has to name the move
    that is legal.

    That move is no longer "emit no primary and take a coverage gap": a gap says
    "not checked", which loses the finding, and the controller no longer has that
    state.  It is the two-assertion shape, which ends with a named element and a
    verdict on it.
    """

    mismatch = procedure_mismatch("persists_until", frozenset())
    assert mismatch is not None
    message = mismatch[1]
    assert "no predicate at all" in message
    assert "`False`" in message, "the literal shape has to be named"
    assert "`precondition`" in message, "the exit has to be named"
    assert "depends_on" in message
    assert "coverage gap" not in message, "the retired exit must not be offered"


def test_calling_the_wrong_predicate_still_gets_the_substitution_message():
    """The two failures need different advice; do not collapse them."""

    mismatch = procedure_mismatch("occupancy_after", frozenset({"edge_declared"}))
    assert mismatch is not None
    assert "called ['edge_declared'] instead" in mismatch[1]
    assert "answers a different question" in mismatch[1]
    assert "emit no primary" not in mismatch[1], (
        "a producer that called the wrong predicate must not be told to omit it"
    )


def test_the_converter_prompt_states_the_two_assertion_shape():
    """The gate message is the second chance; the prompt is the first.

    The earlier design's exit was "write no primary and accept a coverage gap".
    That is gone: a gap is "not checked", which is useless to a repair stage.  The
    shape now produces a named element and two verdicts instead.
    """

    from paper_stm_feedback_loop.discover import prompts

    converter = prompts.ASSERTION_CONVERTER_PROMPT
    assert "needs two assertions, not one" in converter
    assert "under a name you propose from" in converter
    # 既不是 "recorded as `blocked`"，也不再是 `supporting`：两条都是 `primary`，
    # 彼此无 `depends_on`，所以两条都被求值、都计入需求判定，缺失表现为「断言为假」
    # 而不是「断言没跑」。
    assert "The second `primary` is still evaluated" in converter
    assert "recorded as `blocked`" not in converter
    assert "The primary is still evaluated" not in converter


def test_every_named_binding_is_known_to_both_reference_tables():
    """Otherwise a binding is validated by nobody, and the gates disagree.

    `variable_declared` and `event_declared` shipped with a parameter called
    `name`, which neither table listed.  Two holes opened at once.  The runtime
    fell through to the no-table branch, so an event path was never held to its
    `<root>.<event>` shape.  Worse, the static reference gate could not see the
    binding at all -- so the name a `precondition` proposes was invisible to it,
    the dependent primary's identical name looked like an unresolved reference,
    and pair 0006 deadlocked for six revisions between that refusal and the
    placeholder refusal until its repair budget ran out.

    `response_within(response=...)` had the same hole on the static side alone: a
    response naming no declared state was looked up, not found, and answered
    False -- a defect reported against a model that never had it.

    So this is not a naming preference.  A binding that names a model element has
    to be known to the shape table (which decides what a legal name looks like)
    and to the path table (which decides whether the model declares it).
    """

    import inspect

    from paper_stm_feedback_loop.assertions.predicate_api import (
        BINDING_DECLARATION_TABLE,
        PredicateAPI,
    )
    from paper_stm_feedback_loop.discover.capability import BOUND_PATH_KWARGS
    from paper_stm_feedback_loop.discover.predicates import PREDICATES

    # Bindings that are values, not names: no element is looked up for them.
    literal_bindings = {
        "kind",
        "sign",
        "phase",
        "count",
        "bound",
        "within_cycles",
        "condition",
        "release",
    }
    for item in PREDICATES:
        signature = inspect.signature(getattr(PredicateAPI, item.name))
        parameters = {n for n in signature.parameters if n != "self"}
        # The vocabulary and the implementation must agree on the binding names,
        # or the prompt documents a call the runtime rejects.
        assert set(item.bindings) <= parameters, (
            f"{item.name} declares bindings {item.bindings} the implementation "
            f"does not accept: {signature}"
        )
        for binding in parameters - literal_bindings:
            assert binding in BINDING_DECLARATION_TABLE, (
                f"{item.name}({binding}=...) has no shape rule; it would skip "
                "identifier validation entirely"
            )
            assert binding in BOUND_PATH_KWARGS, (
                f"{item.name}({binding}=...) is invisible to the static reference "
                "gate, so neither absent names nor proposed names are seen there"
            )


# --------------------------------------------------------------------------
# v46：被点名的谓词若在本格拒绝作答，Gate D 必须让路


def _refusal_feedback(assertion_id: str, message: str):
    from paper_stm_feedback_loop.discover.schemas import RevisionFeedback

    return RevisionFeedback(
        target="assertions",
        reason="precheck",
        origin="assertion_precheck",
        findings=(
            str({
                "assertion_id": assertion_id,
                "error": {"type": "UnsupportedEvidence", "message": message},
            }),
        ),
    )


def _gate_d_case():
    """一条 `initial_target` 需求 + 一条改用别的谓词的 primary。"""

    from paper_stm_feedback_loop.discover.schemas import (
        AssertionScript,
        AssertionSpec,
        FrozenDiscoverInputs,
        Requirement,
        RequirementSet,
    )

    requirements = RequirementSet(
        revision=1,
        requirements=(
            Requirement(
                requirement_id="REQ-004",
                statement="进入任务范围时应落入三个状态区域之一。",
                predicate="initial_target",
                predicate_bindings={"composite": "R.Scope", "child": "R.Scope.A"},
                verification_kind="structure",
            ),
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            AssertionSpec(
                assertion_id="AST-REQ-004-2",
                requirement_id="REQ-004",
                role="primary",
                coverage_key="k1",
                aggregation_group="g1",
                rationale="initial_target 已拒答，退到可回答的结构证据。",
                evidence_family="structure",
                description="改用可回答的谓词。",
                expression='state_declared(state="R.Scope", kind="any") is True',
                failure_message="[REQ-004][AST-REQ-004-2] m",
            ),
        ),
    )
    frozen = FrozenDiscoverInputs(
        run_id="gate-d",
        natural_language="nl",
        stm_text="stm",
        input_hashes={"nl": "0" * 64},
        tool_env_hash="0" * 64,
        profile="gate-d",
        language="zh-CN",
    )

    class Responder:
        def invoke_structured(self, *args, **kwargs):
            return script

    return requirements, frozen, Responder()


def _gate_d_findings(extra_state: dict) -> tuple[str, ...]:
    from paper_stm_feedback_loop.discover import nodes

    requirements, frozen, responder = _gate_d_case()
    out = nodes.convert_assertions(
        {
            "requirement_set": requirements,
            "node_execution_records": (),
            "frozen_inputs": frozen,
            **extra_state,
        },
        responder,
    )
    feedback = out.get("_assertion_conversion_contract_feedback")
    return tuple(feedback.findings) if feedback else ()


def test_gate_d_yields_when_the_named_predicate_refused_to_answer() -> None:
    """`initial_target` 在入口有歧义的制品上拒绝作答，而 Gate D 强制必须调它。

    v46 实测：前 40 格里三个降级格**全部**是这一条。`initial_target` 占台账
    15/88 = 17%，是第一大谓词，所以这条死路系统性压制最大的一类测量。

    Gate D 的前提是「被点名的谓词决定这个命题」。当该谓词在这份制品上**不能决定**时，
    前提不成立 —— 按 §13，该放宽的正是判据已不成立的那一条。
    """

    strict = _gate_d_findings({})
    assert any("must be discharged by calling" in f for f in strict), strict

    lenient = _gate_d_findings({
        "_assertion_feedback_history": (
            _refusal_feedback(
                "AST-REQ-004-1",
                "'R.Scope' declares 3 unconditional initial edges, so entry is "
                "genuinely ambiguous and no single initial child can be named",
            ),
        ),
    })
    assert not any("must be discharged by calling" in f for f in lenient), lenient


def test_the_waiver_is_scoped_to_the_requirement_that_was_refused() -> None:
    """别的需求拒答过，不能给这条需求开后门 —— 否则豁免会变成万能后门。"""

    findings = _gate_d_findings({
        "_assertion_feedback_history": (
            _refusal_feedback("AST-REQ-009-1", "unrelated refusal"),
        ),
    })
    assert any("must be discharged by calling" in f for f in findings), findings


def test_the_waiver_needs_an_actual_refusal_not_any_feedback() -> None:
    """普通的修订反馈不构成豁免依据；只有谓词拒答才算。"""

    from paper_stm_feedback_loop.discover.schemas import RevisionFeedback

    findings = _gate_d_findings({
        "_assertion_feedback_history": (
            RevisionFeedback(
                target="assertions",
                reason="reviewer",
                origin="assertion_review",
                findings=("AST-REQ-004-1 的 rationale 未引用 NL 子句",),
            ),
        ),
    })
    assert any("must be discharged by calling" in f for f in findings), findings
