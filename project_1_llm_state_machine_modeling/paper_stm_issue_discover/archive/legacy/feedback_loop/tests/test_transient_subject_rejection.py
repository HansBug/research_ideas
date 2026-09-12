"""A node the notation defines as transient cannot be the subject of an occupancy claim.

`_reject_undiscriminating_root` already refuses the always-true half of this: the root is
inside every configuration, so `occupancy_after(target=<root>)` holds however the model
behaves and the check reports nothing. Pseudo-states are the exact mirror. A choice, fork,
join or junction is left in the same step it is entered -- no configuration ever *contains*
one -- so `occupancy_after(target=<choice>)` is false however the model behaves. Both
bindings produce a verdict that is a property of the notation rather than of the artefact,
and both therefore carry no information about the model under test.

The asymmetry in how they were handled is why this matters here. An always-true binding
quietly passes and hides a defect; an always-false one quietly *publishes* one. Across the
v20 run that second direction produced 17 assertions on pairs `0018` and `0038`,
every one of them False, every one of them published as a finding about the model. The
adjudicator had no way to tell them apart from real evidence -- the rationale often said in
so many words that the state is transient, and the finding shipped anyway.

Scope, stated plainly because the previous design note overstated it: this covers pseudo-states
the projection renders as `pseudo state` leaves. Pair `0048` writes its `<<fork>>`/`<<join>>`
with bodies, they project to composites, and `occupancy_after` treats occupying a composite as
occupying one of its leaves -- so those six assertions came back True and are a different
failure (the defect encoded into the binding's own coordinate system). This rule does not
reach them and is not written as though it does.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.assertions.predicate_api import (  # noqa: E402
    PredicateAPI,
    UnsupportedEvidence,
)

#: A choice that really is transient in the notation: entered and left in one step, with an
#: ordinary state on each side so the model is otherwise well-formed.
MODEL_WITH_CHOICE = """state Root {
    event go;
    state Idle;
    state Warm;
    state Done;
    pseudo state Pick;
    [*] -> Idle;
    Idle -> Pick : go;
    Pick -> Warm;
    Warm -> Done;
}
"""


def _api(text: str = MODEL_WITH_CHOICE) -> PredicateAPI:
    from paper_stm_feedback_loop.assertions.runtime import build_eval_environment

    environment = build_eval_environment(
        model_text=text,
        source_mappings=[],
        source_exclusions=[],
        timeout_seconds=30,
        fbmcq_solver_timeout_ms=15_000,
        fbmcq_max_bound=4,
        fbmcq_process_wall_seconds=20.0,
    )
    return environment.predicates


def _pseudo_paths(api: PredicateAPI) -> list[str]:
    return [r.path for r in api.structure.states() if getattr(r, "is_pseudo", False)]


def test_the_fixture_actually_contains_a_pseudo_state() -> None:
    """Without this the rejection tests could pass against a model that has none."""
    paths = _pseudo_paths(_api())
    assert any(p.endswith("Pick") for p in paths), paths


@pytest.mark.parametrize(
    "call",
    [
        pytest.param(
            lambda api, pseudo: api.occupancy_after(
                source="Root.Idle", trigger="Root.go", target=pseudo
            ),
            id="occupancy_after-target",
        ),
        pytest.param(
            lambda api, pseudo: api.reaches(source="Root.Idle", target=pseudo),
            id="reaches-target",
        ),
        pytest.param(
            lambda api, pseudo: api.response_within(
                source="Root.Idle", trigger="Root.go", response=pseudo
            ),
            id="response_within-response",
        ),
        pytest.param(
            lambda api, pseudo: api.persists_until(state=pseudo, release="true"),
            id="persists_until-state",
        ),
    ],
)
def test_occupancy_predicates_refuse_a_transient_subject(call) -> None:
    """Refused, not answered False -- a False here would be published as a finding."""
    api = _api()
    pseudo = next(p for p in _pseudo_paths(api) if p.endswith("Pick"))
    with pytest.raises(UnsupportedEvidence) as excinfo:
        call(api, pseudo)
    message = str(excinfo.value)
    assert "Pick" in message
    # The producer has to be able to act on this, and the action is the same one the root
    # refusal asks for: name the state the requirement is actually about.
    assert "transient" in message.lower() or "never occupied" in message.lower()


def test_the_refusal_says_what_to_bind_instead() -> None:
    api = _api()
    pseudo = next(p for p in _pseudo_paths(api) if p.endswith("Pick"))
    with pytest.raises(UnsupportedEvidence) as excinfo:
        api.occupancy_after(source="Root.Idle", trigger="Root.go", target=pseudo)
    assert "outcome" in str(excinfo.value).lower() or "branch" in str(excinfo.value).lower()


def test_ordinary_states_are_untouched() -> None:
    """The rule must not cost the predicates their normal answers.

    `Idle --go--> Pick --> Warm` really does put the machine in `Warm`, so a binding on the
    branch outcome keeps working -- that is the binding the refusal is pointing at.
    """
    api = _api()
    assert api.occupancy_after(
        source="Root.Idle", trigger="Root.go", target="Root.Warm", within_cycles=1
    ) is True
    assert api.reaches(source="Root.Idle", target="Root.Warm") is True


def test_a_transient_subject_in_a_non_occupancy_position_is_still_allowed() -> None:
    """`state_declared(kind='pseudo')` exists precisely to ask about these nodes.

    Refusing every mention of a pseudo-state would remove the one legitimate way to state
    that the model declares -- or fails to declare -- a choice the specification calls for.
    """
    api = _api()
    pseudo = next(p for p in _pseudo_paths(api) if p.endswith("Pick"))
    assert api.state_declared(state=pseudo, kind="pseudo") is True
    assert api.state_declared(state=pseudo, kind="leaf") is False


def test_the_rule_guards_only_the_claim_slots() -> None:
    """Scoped to exactly the slots the root rule guards -- `source` is not one of them.

    `source` states where the question is asked from, not what is being claimed, and the
    root rule leaves it alone for the same reason. Whether a transient *source* yields a
    meaningful answer is a separate question this rule does not decide; it is left to the
    predicate's own semantics so that the change stays a mirror rather than an extension.
    """
    api = _api()
    pseudo = next(p for p in _pseudo_paths(api) if p.endswith("Pick"))
    try:
        api.occupancy_after(source=pseudo, trigger="Root.go", target="Root.Warm")
    except UnsupportedEvidence as exc:
        assert "transient" not in str(exc).lower(), (
            "the transient rule must not reach `source`; it was refused by this rule"
        )


def test_the_root_refusal_still_works() -> None:
    """The mirror it is modelled on must not have been disturbed."""
    api = _api()
    with pytest.raises(UnsupportedEvidence):
        api.occupancy_after(source="Root.Idle", trigger="Root.go", target="Root")
