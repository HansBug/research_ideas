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
    PREDICATES,
    procedure_mismatch,
)

DECLARED = 'transition_exists(source="R.A", event="R.e", target="R.B") is True'
SIMULATED = 'simulate(cycles=[[], ["R.e"]]).final.is_active("R.B") is True'
FORMAL = 'fbmcq(\'check invariant <= 3: active("R.B");\').holds is True'


def _check(predicate: str, expression: str):
    return procedure_mismatch(predicate, called_evidence_functions(expression))


def test_declaration_query_cannot_close_a_runtime_claim():
    """The 0006 shape: this is the substitution the gate exists to stop."""

    mismatch = _check("occupancy_after", DECLARED)
    assert mismatch is not None
    assert mismatch[0] == "simulate"
    assert "must call simulate()" in mismatch[1]
    assert "transition_exists" in mismatch[1]


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

    from paper_stm_feedback_loop.discover.predicates import PREDICATE_BY_NAME

    entry = PREDICATE_BY_NAME[predicate]
    assert procedure_mismatch(predicate, frozenset({entry.procedure_function})) is None


@pytest.mark.parametrize("predicate", [item.name for item in PREDICATES])
def test_no_predicate_lists_its_own_procedure_as_a_locator(predicate):
    """A locator is by definition weaker; listing the procedure would be a hole."""

    from paper_stm_feedback_loop.discover.predicates import PREDICATE_BY_NAME

    entry = PREDICATE_BY_NAME[predicate]
    for locator in entry.locators:
        assert not locator.startswith(f"{entry.procedure_function}("), locator


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
    assert "must call simulate" in blob, blob[:600]


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
