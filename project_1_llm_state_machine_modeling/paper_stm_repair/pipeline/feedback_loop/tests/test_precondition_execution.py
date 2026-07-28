"""Topological execution and blocking, end to end (issue #170 §11.5).

The property under test is that an unmet prerequisite produces `blocked`, not
`invalid`.  The difference is the whole design: `invalid` sends the script back
for a repair nobody can make -- there is no way to compute a delta for a variable
that does not exist -- and after five rounds the requirement is filed as
"unchecked", which is how pair 0006's expected defect was lost the first time.
`blocked` says instead: this claim was not evaluated because its premise failed,
and the premise's own `False` is the finding.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions import build_eval_environment  # noqa: E402
from paper_stm_feedback_loop.assertions.checker import AssertionChecker  # noqa: E402
from paper_stm_feedback_loop.discover import nodes  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionScript,
    AssertionSpec,
    FrozenDiscoverInputs,
    Requirement,
    RequirementSet,
)

#: Pair 0006's shape: states and events, but no variable of the author's own.
MODEL = """state Root {
    event go;
    event done;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go;
    Busy -> Idle : /done;
}
"""

#: The same machine with the variable the NL asks for.
MODEL_WITH_VAR = """def int units = 5;
state Root {
    event go;
    event done;
    state Idle;
    state Busy;
    [*] -> Idle;
    Idle -> Busy : /go effect { units = units - 1; };
    Busy -> Idle : /done;
}
"""


def _spec(aid, role, expr, depends_on=(), family="structure"):
    return AssertionSpec(
        assertion_id=aid,
        requirement_id="REQ-001",
        role=role,
        coverage_key=f"key-{aid}",
        aggregation_group="REQ-001:all",
        rationale="NL 要求数量递减；模型声明表为空，故提议 units 承载。",
        evidence_family=family,
        description="d",
        expression=expr,
        failure_message=f"[REQ-001][{aid}] m",
        depends_on=tuple(depends_on),
    )


EXISTS = 'variable_declared(name="units") is True'
DELTA = (
    'variable_delta_after(source="Root.Idle", trigger="Root.go", '
    'variable="units", sign="negative") is True'
)


def _run(model, assertions):
    """Execute `precheck_and_seal` against a real model and return its executions."""

    script = AssertionScript(
        revision=1,
        assertions=tuple(assertions),
        requirement_mapping={"REQ-001": tuple(a.assertion_id for a in assertions)},
        strategies={"REQ-001": "拆两条：变量存在性是效果可判定的前提。"},
    )
    frozen = FrozenDiscoverInputs(
        run_id="exec",
        natural_language="After go the unit count decreases.",
        stm_text=model,
        input_hashes={"nl": "0" * 64},
        tool_env_hash="0" * 64,
        profile="exec",
        language="en-US",
    )
    checker = AssertionChecker(
        environment=build_eval_environment(
            model_text=model,
            source_mappings=[],
            source_exclusions=[],
            timeout_seconds=30,
            fbmcq_solver_timeout_ms=10_000,
            fbmcq_max_bound=3,
            fbmcq_process_wall_seconds=15.0,
        )
    )
    out = nodes.precheck_and_seal(
        {
            "frozen_inputs": frozen,
            "assertion_script": script,
            "requirement_set": RequirementSet(
                revision=1,
                requirements=(
                    Requirement(
                        requirement_id="REQ-001",
                        statement="After go the unit count decreases.",
                        predicate="variable_delta_after",
                        predicate_bindings={
                            "source": "Root.Idle",
                            "trigger": "Root.go",
                            "variable": "units",
                            "sign": "negative",
                        },
                        verification_kind="behavior",
                    ),
                ),
            ),
            "node_execution_records": (),
        },
        sealed_store=nodes.InMemorySealedStore(),
        assertion_checker=checker,
    )
    public = out.get("assertion_check_public")
    return {e.assertion_id: e for e in (public.executions if public else ())}, out


PAIR = lambda: (  # noqa: E731 - a fixture, not a helper
    _spec("AST-REQ-001-0", "precondition", EXISTS),
    _spec("AST-REQ-001-1", "primary", DELTA, ("AST-REQ-001-0",), "simulation"),
)


def test_an_unmet_prerequisite_blocks_rather_than_invalidates():
    """The model declares no variable, so the delta has nothing to compute."""

    execs, _ = _run(MODEL, PAIR())
    assert execs["AST-REQ-001-0"].status == "executable"
    assert execs["AST-REQ-001-1"].status == "blocked"
    assert "AST-REQ-001-0" in (execs["AST-REQ-001-1"].error or "")


def test_a_blocked_item_does_not_send_the_script_back_for_repair():
    """`invalid` would cost five rounds and end as an unchecked coverage gap."""

    _, out = _run(MODEL, PAIR())
    public = out["assertion_check_public"]
    assert public.status == "executable"
    assert out.get("_assertion_feedback") is None


def test_a_met_prerequisite_lets_the_dependent_run():
    """Control: with the variable present, both assertions execute."""

    execs, _ = _run(MODEL_WITH_VAR, PAIR())
    assert execs["AST-REQ-001-0"].status == "executable"
    assert execs["AST-REQ-001-1"].status == "executable"


def test_the_prerequisite_runs_before_its_dependent_whatever_the_declaration_order():
    """Declaration order must not decide the outcome.

    Listing the dependent first used to mean it ran first, so the prerequisite's
    truth was unknown at that moment and the dependency was silently ignored.
    """

    reversed_pair = tuple(reversed(PAIR()))
    execs, _ = _run(MODEL, reversed_pair)
    assert execs["AST-REQ-001-1"].status == "blocked"
    assert execs["AST-REQ-001-0"].status == "executable"


def test_a_blocked_assertion_produces_no_sealed_result():
    """It was never evaluated, so there is no verdict to seal.

    A sealed `False` here would be a defect report resting on nothing.
    """

    _, out = _run(MODEL, PAIR())
    receipt = out["sealed_assertion_results"]
    assert receipt.result_count == 1, "only the prerequisite has a verdict"


def test_the_chain_extends_past_one_level():
    """A dependent of a blocked assertion is itself blocked.

    The prerequisite's id is absent from the truth table -- it was never
    evaluated -- and `blocked_by` treats absent exactly like False.
    """

    chain = (
        _spec("AST-REQ-001-0", "precondition", EXISTS),
        _spec("AST-REQ-001-1", "primary", DELTA, ("AST-REQ-001-0",), "simulation"),
        _spec(
            "AST-REQ-001-2",
            "supporting",
            'event_declared(name="Root.go") is True',
            ("AST-REQ-001-1",),
        ),
    )
    execs, _ = _run(MODEL, chain)
    assert execs["AST-REQ-001-1"].status == "blocked"
    assert execs["AST-REQ-001-2"].status == "blocked", (
        "a dependent of a blocked assertion must not run either"
    )


# --------------------------------------------------------------------------
# Verdict: every assertion must be explicitly satisfied (issue #170 §11.5)
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Verdict: every assertion must be explicitly satisfied (issue #170 §11.5)
# --------------------------------------------------------------------------


def _adjudicate(
    *,
    results,
    executions,
    satisfied_claim,
    requirement_aggregation="all",
    excluded=(),
):
    """Drive `adjudicate_results` over canned results and a canned check.

    The LLM's own answer is supplied verbatim so the test observes the
    deterministic normalisation rather than a model's judgement.
    """

    from paper_stm_feedback_loop.discover.schemas import (
        AssertionCheckPublic,
        AttributionProjection,
        DiscoverAdjudication,
        DiscoverInput,
        ReleasedAssertionResults,
    )

    frozen = nodes._fallback_prepare(
        DiscoverInput(
            run_id="verdict",
            natural_language="After go the unit count decreases.",
            stm_text=MODEL,
            language="en-US",
        )
    )
    requirements = RequirementSet(
        revision=1,
        requirements=(
            Requirement(
                requirement_id="REQ-001",
                statement="After go the unit count decreases.",
                predicate="variable_delta_after",
                predicate_bindings={
                    "source": "Root.Idle",
                    "trigger": "Root.go",
                    "variable": "units",
                    "sign": "negative",
                },
                verification_kind="behavior",
                coverage_obligation={"aggregation": requirement_aggregation},
            ),
        ),
    )
    specs = PAIR()
    script = AssertionScript(
        revision=1,
        assertions=specs,
        requirement_mapping={"REQ-001": tuple(a.assertion_id for a in specs)},
    )
    released = ReleasedAssertionResults(
        script_hash="script", tool_env_hash="env", sealed_hash="sealed", results=results
    )
    out = nodes.adjudicate_results(
        {
            "_input": DiscoverInput(
                run_id="verdict",
                natural_language="After go the unit count decreases.",
                stm_text=MODEL,
                language="en-US",
            ),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
            "released_assertion_results": released,
            # `bind_attribution` produces one binding per released result, so a
            # fixture that omits them is not a shape the graph can reach.
            "attribution_projection": AttributionProjection(
                bindings=tuple(
                    {
                        "assertion_id": r.assertion_id,
                        "requirement_id": r.requirement_id,
                        "status": "unattributed",
                        "source_refs": (),
                        "trace_entry_ids": (),
                        "source_level_claim_allowed": False,
                        "rationale": "fixture",
                    }
                    for r in results
                )
            ),
            "assertion_check_public": AssertionCheckPublic(
                script_hash="s" * 8,
                tool_env_hash="e" * 8,
                status="executable",
                executions=executions,
            ),
        },
        nodes.CallableStructuredResponder(
            lambda _r, _s, _sys, _p: DiscoverAdjudication(
                has_confirmed_issues=False,
                issues=(),
                excluded_findings=excluded,
                excluded_observations=(),
                satisfied_requirement_ids=satisfied_claim,
                rationale="canned",
            )
        ),
    )
    if "failure" in out:
        raise AssertionError(f"adjudicate_results failed: {out['failure'].message}")
    return out["adjudication"]


def _result(aid, role, value, family="structure"):
    from paper_stm_feedback_loop.discover.schemas import AssertionResult

    return AssertionResult(
        assertion_id=aid,
        requirement_id="REQ-001",
        role=role,
        coverage_key=f"key-{aid}",
        aggregation_group="REQ-001:all",
        truth_value=value,
        script_hash="script",
        tool_env_hash="env",
        evidence_family=family,
    )


def _execution(aid, role, status):
    from paper_stm_feedback_loop.discover.schemas import AssertionExecutionPublic

    return AssertionExecutionPublic(
        assertion_id=aid, requirement_id="REQ-001", role=role, status=status
    )


def test_a_requirement_whose_premise_failed_is_not_satisfied():
    """The primary was blocked, so it sealed nothing.

    Aggregating only over primaries would leave an empty list, and `any` over an
    empty list is vacuously true -- the requirement would be reported satisfied
    while its premise is on record as False.  Counting the precondition closes it.
    """

    adjudication = _adjudicate(
        results=(_result("AST-REQ-001-0", "precondition", False),),
        executions=(
            _execution("AST-REQ-001-0", "precondition", "executable"),
            _execution("AST-REQ-001-1", "primary", "blocked"),
        ),
        satisfied_claim=("REQ-001",),  # the model wrongly claims satisfaction
        requirement_aggregation="any",
        # A False precondition must be accounted for -- the node rejects an
        # adjudication that leaves any non-safe False unexplained, and a missing
        # element now qualifies as one.  That rejection is itself the property
        # §11.4 asks for: the finding cannot be silently dropped.
        excluded=(
            {
                "issue_id": "ISSUE-REQ-001-PREMISE",
                "requirement_id": "REQ-001",
                "assertion_ids": ("AST-REQ-001-0",),
                "title": "模型未声明承载数量的变量",
                "rationale": "canned",
                "attribution_status": "unattributed",
            },
        ),
    )
    assert "REQ-001" not in adjudication.satisfied_requirement_ids


def test_a_blocked_primary_alone_disqualifies_the_requirement():
    """Even when every sealed verdict is True.

    A precondition that passed plus a primary that never ran is not a satisfied
    requirement: the claim the requirement actually makes was never evaluated.
    """

    adjudication = _adjudicate(
        results=(_result("AST-REQ-001-0", "precondition", True),),
        executions=(
            _execution("AST-REQ-001-0", "precondition", "executable"),
            _execution("AST-REQ-001-1", "primary", "blocked"),
        ),
        satisfied_claim=("REQ-001",),
    )
    assert "REQ-001" not in adjudication.satisfied_requirement_ids


def test_both_green_is_satisfied():
    """Control: the rule is "all explicitly satisfied", not "never satisfied"."""

    adjudication = _adjudicate(
        results=(
            _result("AST-REQ-001-0", "precondition", True),
            _result("AST-REQ-001-1", "primary", True, "simulation"),
        ),
        executions=(
            _execution("AST-REQ-001-0", "precondition", "executable"),
            _execution("AST-REQ-001-1", "primary", "executable"),
        ),
        satisfied_claim=("REQ-001",),
    )
    assert "REQ-001" in adjudication.satisfied_requirement_ids


def test_a_false_precondition_sinks_the_requirement_even_with_a_true_primary():
    """Should the primary somehow run and pass, the failed premise still counts.

    `supporting` is excluded from this aggregate on purpose -- corroboration may
    legitimately be False -- but a premise may not.
    """

    adjudication = _adjudicate(
        results=(
            _result("AST-REQ-001-0", "precondition", False),
            _result("AST-REQ-001-1", "primary", True, "simulation"),
        ),
        executions=(
            _execution("AST-REQ-001-0", "precondition", "executable"),
            _execution("AST-REQ-001-1", "primary", "executable"),
        ),
        satisfied_claim=("REQ-001",),
        excluded=(
            {
                "issue_id": "ISSUE-REQ-001-PREMISE",
                "requirement_id": "REQ-001",
                "assertion_ids": ("AST-REQ-001-0",),
                "title": "模型未声明承载数量的变量",
                "rationale": "canned",
                "attribution_status": "unattributed",
            },
        ),
    )
    assert "REQ-001" not in adjudication.satisfied_requirement_ids
