"""What the adjudicator is shown, now that it is allowed to group Requirements.

Deciding whether two False assertions are one defect means checking whether they fail at the
same place in the model. The old payload made that hard in both directions at once: it did
not carry `stm_text`, so there was nothing to check a claimed shared element against, while
roughly two thirds of its 77k tokens were content hashes -- `args_hash`, `namespace_hash_*`,
`expression_sha256` -- that no reader can do anything with.

So the hashes go and the model comes in. Note what is *not* dropped: `kwargs` and
`model_refs` inside `function_call_trace` are the fully resolved predicate arguments, and
they are where an element like `Power_Off` actually appears -- `source_refs` only ever holds
states, so on pair 0000 the element the two Requirements share is visible nowhere else.

`merge_candidates` is the last addition and the one that needs the most care. Pairs sharing
a predicate, trigger and target while differing in source can be computed exactly, so the
adjudicator gets them for free rather than rediscovering them. But the rule is narrow -- on
pair 0029 the two Requirements that genuinely belong together use different predicates and
it finds nothing -- so it is passed as a hint to check, never as a decision to apply.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts, renderer  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    ReleasedAssertionResults,
    RequirementSet,
)

STM = """state Root {
    event power_off;
    state HumanDriving;
    state Autonomous;
    state Final;
    [*] -> HumanDriving;
}
"""


def _fixture() -> dict:
    """Pair 0000 in miniature: two Requirements, one misplaced `power_off` edge."""
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-006A",
                "statement": "Power off from human driving reaches the final state.",
                "checkability": "structure",
                "predicate_bindings": {
                    "source": "Root.HumanDriving",
                    "target": "Root.Final",
                    "trigger": "Root.power_off",
                },
            },
            {
                "requirement_id": "REQ-006B",
                "statement": "Power off from autonomous reaches the final state.",
                "checkability": "structure",
                "predicate_bindings": {
                    "source": "Root.Autonomous",
                    "target": "Root.Final",
                    "trigger": "Root.power_off",
                },
            },
            {
                "requirement_id": "REQ-010",
                "statement": "The swarm size decreases after an attack.",
                "checkability": "structure",
                "predicate_bindings": {
                    "source": "Root.HumanDriving",
                    "target": "Root.Autonomous",
                    "trigger": "Root.power_off",
                },
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=tuple(
            {
                "assertion_id": f"AST-{rid}-1",
                "requirement_id": rid,
                "description": f"{rid} holds.",
                "expression": "False",
                "failure_message": f"[{rid}][AST-{rid}-1] requirement failed",
                "evidence_family": "structure",
                "role": role,
                "coverage_key": f"AST-{rid}-1",
                "aggregation_group": f"{rid}:all",
                "rationale": "Fixture assertion; rationale not under test here.",
            }
            for rid, role in (
                ("REQ-006A", "primary"),
                ("REQ-006B", "primary"),
                ("REQ-010", "supporting"),
            )
        ),
        requirement_mapping={
            "REQ-006A": ("AST-REQ-006A-1",),
            "REQ-006B": ("AST-REQ-006B-1",),
            "REQ-010": ("AST-REQ-010-1",),
        },
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=tuple(
            AssertionResult(
                assertion_id=f"AST-{rid}-1",
                requirement_id=rid,
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
                role=role,
                check_detail={
                    "outcome": "false",
                    "terminal_expression": "occupancy_after(...)",
                    "audit": {"expression_sha256": "deadbeef" * 8},
                    "namespace_hash_before": "a" * 64,
                    "namespace_hash_after": "b" * 64,
                    "function_call_trace": [
                        {
                            "kwargs": {"trigger": "Root.power_off"},
                            "model_refs": ["Root.power_off"],
                            "args_hash": "c" * 64,
                            "kwargs_hash": "d" * 64,
                            "result_hash": "e" * 64,
                        }
                    ],
                },
                evidence_scope={"required_function_families": ["structure"]},
            )
            for rid, role in (
                ("REQ-006A", "primary"),
                ("REQ-006B", "primary"),
                ("REQ-010", "supporting"),
            )
        ),
    )
    attribution = AttributionProjection(
        bindings=tuple(
            {
                "assertion_id": f"AST-{rid}-1",
                "requirement_id": rid,
                "status": "safe",
                "source_refs": (f"state:Root.{state}",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            }
            for rid, state in (
                ("REQ-006A", "HumanDriving"),
                ("REQ-006B", "Autonomous"),
                ("REQ-010", "HumanDriving"),
            )
        )
    )
    return {
        "requirements": requirements,
        "script": script,
        "released": released,
        "attribution": attribution,
    }


def _payload() -> dict:
    fx = _fixture()
    return json.loads(
        renderer.render_adjudicator_input(
            fx["requirements"],
            fx["script"],
            fx["released"],
            fx["attribution"],
            (),
            stm_text=STM,
        )
    )


def test_the_model_is_shown() -> None:
    """A claimed shared element has to be checkable against something."""
    assert _payload()["stm_text"] == STM


def test_content_hashes_are_dropped_but_resolved_arguments_are_not() -> None:
    """The hashes are two thirds of the payload and no reader can use them.

    `model_refs` is the counter-case and the reason this is a field-level prune rather than
    dropping `check_detail` wholesale: on pair 0000 it is the only place `Power_Off` appears,
    because `source_refs` carries states alone.
    """
    text = json.dumps(_payload()["strict_bool_results"])
    for gone in ("args_hash", "kwargs_hash", "result_hash",
                 "namespace_hash_before", "namespace_hash_after", "expression_sha256"):
        assert gone not in text, f"{gone} should have been pruned"
    assert "model_refs" in text
    assert "Root.power_off" in text
    assert "terminal_expression" in text


def test_pruning_leaves_the_stored_results_untouched() -> None:
    """`bind_attribution` reads `check_detail`; the prune is for rendering only.

    Mutating the results in place here would break attribution, which is where three of the
    eight-cell misses already live -- see issue #175 §6.2.
    """
    fx = _fixture()
    renderer.render_adjudicator_input(
        fx["requirements"], fx["script"], fx["released"], fx["attribution"], (),
        stm_text=STM,
    )
    detail = fx["released"].results[0].check_detail
    assert detail["function_call_trace"][0]["args_hash"] == "c" * 64
    assert detail["namespace_hash_before"] == "a" * 64


def test_merge_candidates_pair_requirements_sharing_predicate_trigger_and_target() -> None:
    candidates = _payload()["merge_candidates"]
    pairs = {tuple(sorted(c["requirement_ids"])) for c in candidates}
    assert ("REQ-006A", "REQ-006B") in pairs


def test_merge_candidates_exclude_requirements_with_no_safe_false_primary() -> None:
    """Scoping the rule to Requirements that can actually become issues.

    Unscoped it produced thirteen candidates on pair 0029 whose counterparts had no
    safe-False assertion at all -- they could never have been merged, so their only effect
    would have been to make the adjudicator's candidate-acceptance rate meaningless.
    """
    candidates = _payload()["merge_candidates"]
    named = {rid for c in candidates for rid in c["requirement_ids"]}
    assert "REQ-010" not in named, "a supporting-only requirement cannot become an issue"


def test_each_result_carries_how_it_may_be_dispositioned() -> None:
    """The routing rule travels with the data, not only in the prompt.

    A supporting False was placed into `issues` once in the eight cells and the deterministic
    layer trimmed it, leaving a rationale that cited an assertion no longer listed.
    """
    hints = {
        r["assertion_id"]: r["disposition_hint"]
        for r in _payload()["strict_bool_results"]["results"]
    }
    assert hints["AST-REQ-006A-1"] == "may_become_issue"
    assert hints["AST-REQ-010-1"] == "observation_only"


def test_prompt_no_longer_scopes_merging_to_one_requirement() -> None:
    text = prompts.RESULT_ADJUDICATOR_PROMPT
    assert "complementary evidence for the same Requirement" not in text
    assert "same underlying model defect" in text


def test_prompt_no_longer_asks_for_every_supporting_assertion_id() -> None:
    """This instruction is why a supporting id was placed in `issues` -- it said to."""
    assert "retain every supporting assertion id" not in prompts.RESULT_ADJUDICATOR_PROMPT


def test_prompt_states_the_asymmetry_and_the_evidence_a_merge_owes() -> None:
    text = prompts.RESULT_ADJUDICATOR_PROMPT
    assert "shared_root_cause" in text and "shared_elements" in text
    assert "merge_candidates" in text
    # Over-merging understates the defect count and is the harder error to detect, so the
    # default has to be stated as not merging rather than left to inference.
    assert "do not merge" in text.lower()
