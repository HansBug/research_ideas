"""An element that exists only because the author omitted something cannot hide the omission.

Two attribution rules were rejecting exactly the findings they were meant to protect, and both
reproduced in all three rounds of the v2 matrix -- nine blocked assertions, zero variance.

**`initial_target` against an injected placeholder.** `0029-claude` asserts
`initial_target(HighwayMode, HighwayMode.enter_hwy)`. The author declared no initial entry for
that region, so the R4.5 projection injected `HighwayMode.UnspecifiedInitial` and the assertion
came back False against it. The evidence therefore touches a compiler-owned element, and the
generic rule downgraded it to `representation_debt` -- which reads as "we cannot tell whether
the author is at fault". But `UnspecifiedInitial` exists *because* the author declared nothing:
a model with a real initial entry would have no such node, and the assertion would be True.
The placeholder is the omission's fingerprint, not a confound.

The exemption is narrow, and the vocabulary already names its boundary. For predicates in
`_DECLARED_PATH_IS_THE_CLAIM` -- `containment`, `initial_target` -- the claim *is* about what
the model declares, so an injected stand-in for the missing declaration is admissible evidence.
For a behavioural predicate the same element is a genuine confound: `occupancy_after` through
`UnspecifiedInitial` really cannot tell an author defect from a lowering artefact, because the
run passes through a node the author never wrote.

**A proposed name has no trace entry of its own.** `0050-claude` asserts
`state_declared(AutonomousMode.auto_final)` -- a step-4 proposal for a substate the
specification names and the model lacks. Nothing in the frozen trace covers a path that does
not exist, so `source_refs` came back empty and the status was `unattributed`. But the claim is
about `AutonomousMode`, which the author did declare and which the trace does cover. Attributing
it to the declared ancestor is what makes "this composite declares no such child" an
author-level statement instead of an unanswerable one.

Both rules are keyed on the predicate rather than on the element, so neither widens what counts
as author-owned for any claim about behaviour.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import nodes  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionResult,
    AssertionScript,
    DiscoverInput,
    ReleasedAssertionResults,
    RequirementSet,
)

# `Region` declares `other_r` as its entry, not `enter_r`. That is the defect the fixture
# stands in for -- and it has to be *some* declared entry, because the DSL rejects a composite
# with none, which is why the projection injects a placeholder in the real corpus instead.
MODEL = """state Root {
    event go;
    state Region {
        state enter_r;
        state other_r;
        [*] -> other_r;
        enter_r -> other_r : go;
    }
    state Plain;
    [*] -> Plain;
}
"""

#: What the R4.5 projection adds when a composite declares no initial entry. Listed in
#: `attribution_exclusions` because it is the compiler's, not the author's.
INJECTED = "compiler:state:Root.Region.UnspecifiedInitial"


def _input() -> DiscoverInput:
    return DiscoverInput(
        run_id="omission",
        natural_language="The system begins in the enter_r substate.",
        stm_text=MODEL,
        language="en-US",
    )


def _state(
    expression: str,
    *,
    predicate: str,
    observed: list[str],
    bindings: dict[str, str],
    exclusions: tuple[str, ...] = (INJECTED,),
    trace_elements: tuple[str, ...] = ("source:state:Root.Region",),
) -> dict:
    """A one-assertion state ready for `bind_attribution`.

    `observed` is what the predicate's call trace touched -- the list the attribution layer
    intersects against the frozen trace and against `attribution_exclusions`.
    """
    frozen = nodes._fallback_prepare(_input())
    frozen = frozen.model_copy(
        update={
            "source_trace": {
                "attribution_exclusions": list(exclusions),
                "entries": [
                    {
                        "trace_id": "T1",
                        # `_trace_entry_matches` intersects this list against what the
                        # predicate's call trace touched.
                        "intermediate_elements": ["Root.Region"],
                        "source_elements": list(trace_elements),
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
            }
        }
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-1",
                "requirement_id": "REQ-001",
                "description": "The claim under test.",
                "expression": expression,
                "failure_message": "[REQ-001][AST-REQ-001-1] requirement failed",
                "evidence_family": "structure",
                "role": "primary",
                "coverage_key": "AST-REQ-001-1",
                "aggregation_group": "REQ-001:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-1",)},
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-1",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
                role="primary",
                check_detail={"function_call_trace": [{"model_refs": observed}]},
            ),
        ),
    )
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "The system begins in the enter_r substate.",
                "checkability": "structure",
                "predicate": predicate,
                "predicate_bindings": bindings,
            },
        ),
    )
    return {
        "_input": _input(),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": script,
        "released_assertion_results": released,
    }


def _bind(state: dict) -> dict:
    out = nodes.bind_attribution(state)
    assert "failure" not in out, out.get("failure")
    return out["attribution_projection"].bindings[0]


def test_initial_target_against_an_injected_placeholder_is_source_owned() -> None:
    """The v2 `0029-claude` failure, reproduced three rounds out of three."""
    binding = _bind(
        _state(
            'initial_target(composite="Root.Region", child="Root.Region.enter_r") is True',
            predicate="initial_target",
            observed=["Root.Region", "Root.Region.UnspecifiedInitial"],
            bindings={"composite": "Root.Region", "child": "Root.Region.enter_r"},
        )
    )
    assert binding.status == "safe", binding.rationale
    assert "declares" in binding.rationale


def test_containment_gets_the_same_exemption() -> None:
    """`_DECLARED_PATH_IS_THE_CLAIM` holds both, and both ask what the model declares."""
    binding = _bind(
        _state(
            'containment(parent="Root.Region", child="Root.Region.enter_r") is True',
            predicate="containment",
            observed=["Root.Region", "Root.Region.UnspecifiedInitial"],
            bindings={"parent": "Root.Region", "child": "Root.Region.enter_r"},
        )
    )
    assert binding.status == "safe", binding.rationale


def test_a_behavioural_predicate_keeps_the_confound() -> None:
    """The boundary. A run through an injected node cannot tell author from lowering.

    Without this the exemption would launder every `occupancy_after` whose path happens to
    cross a projected node -- which is the confound `representation_debt` exists to record.
    """
    binding = _bind(
        _state(
            'occupancy_after(source="Root.Region", target="Root.Plain", trigger="Root.go") is True',
            predicate="occupancy_after",
            observed=["Root.Region", "Root.Region.UnspecifiedInitial"],
            bindings={
                "source": "Root.Region",
                "target": "Root.Plain",
                "trigger": "Root.go",
            },
        )
    )
    assert binding.status == "representation_debt", binding.rationale


def test_an_exclusion_that_is_not_an_omission_placeholder_still_blocks() -> None:
    """Route-control tokens are added for lowering, not to stand in for something missing.

    `R45RouteToken` exists on every projected model regardless of what the author wrote, so
    evidence resting on it says nothing about the author either way.
    """
    binding = _bind(
        _state(
            'initial_target(composite="Root.Region", child="Root.Region.enter_r") is True',
            predicate="initial_target",
            observed=["Root.Region", "R45RouteToken"],
            bindings={"composite": "Root.Region", "child": "Root.Region.enter_r"},
            exclusions=("compiler:route_control:R45RouteToken",),
        )
    )
    assert binding.status == "representation_debt", binding.rationale


def test_a_proposed_name_is_attributed_to_its_declared_ancestor() -> None:
    """The v2 `0050-claude` failure, reproduced three rounds out of three.

    Nothing in the frozen trace covers `Root.Region.absent_child` -- it does not exist. But the
    claim is about `Root.Region`, which the author declared and the trace does cover.
    """
    binding = _bind(
        _state(
            'state_declared(state="Root.Region.absent_child", kind="any") is True',
            predicate="state_declared",
            observed=["Root.Region.absent_child"],
            bindings={"state": "Root.Region.absent_child", "kind": "any"},
        )
    )
    assert binding.status == "safe", binding.rationale
    assert "source:state:Root.Region" in binding.source_refs
    assert "ancestor" in binding.rationale


def test_a_proposed_name_with_no_declared_ancestor_stays_unattributed() -> None:
    """A name whose whole path is invented has nothing author-owned to rest on.

    `Root.Nowhere.absent` names no declared composite, so there is no author-level subject and
    the finding genuinely cannot be attributed.
    """
    binding = _bind(
        _state(
            'state_declared(state="Root.Nowhere.absent", kind="any") is True',
            predicate="state_declared",
            observed=["Root.Nowhere.absent"],
            bindings={"state": "Root.Nowhere.absent", "kind": "any"},
        )
    )
    assert binding.status == "unattributed", binding.rationale


def test_the_ancestor_rule_does_not_apply_to_behavioural_predicates() -> None:
    """A behavioural claim needs the run it describes to be author-owned, not just a name."""
    binding = _bind(
        _state(
            'occupancy_after(source="Root.Region.absent_child", target="Root.Plain", trigger="Root.go") is True',
            predicate="occupancy_after",
            observed=["Root.Region.absent_child"],
            bindings={
                "source": "Root.Region.absent_child",
                "target": "Root.Plain",
                "trigger": "Root.go",
            },
        )
    )
    assert binding.status == "unattributed", binding.rationale
