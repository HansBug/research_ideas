from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from paper_stm_feedback_loop.discover import prompts, renderer  # noqa: E402
from paper_stm_feedback_loop.discover.graph import (  # noqa: E402
    build_discover_graph,
    route_after_convert,
    run_discover,
    run_discover_state,
)
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionCheckPublic,
    AssertionReview,
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    ReleasedAssertionResults,
    DiscoverAdjudication,
    DiscoverInput,
    RequirementReview,
    Requirement,
    RequirementSet,
    RevisionFeedback,
)
from paper_stm_feedback_loop.discover.utils import sha256_data  # noqa: E402
from paper_stm_feedback_loop.discover.nodes import default_fake_responder  # noqa: E402

MODEL = """state Root {
    event go;
    state Idle;
    state Done;
    [*] -> Idle;
    Idle -> Done : go;
}
"""


def test_requirement_prompts_preserve_shared_scope_without_inventing_universal_scope() -> None:
    assert "shared prepositional qualifiers" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "unconditional global requirement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "joint trigger" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "shared qualifiers" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "independent triggers" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "invent a universal quantifier" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Operational context" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Containment language" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "source mode/state" in prompts.REQUIREMENT_REVIEWER_PROMPT


def test_simulation_prompts_distinguish_initial_variable_names_from_result_paths() -> None:
    assert "declaration names, not qualified paths" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "declaration names rather than qualified state-machine paths" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "documented FBMCQ grammar" in prompts.ASSERTION_CONVERTER_PROMPT


def test_assertion_prompts_preserve_nl_targets_and_require_conflict_analysis() -> None:
    for prompt in (prompts.ASSERTION_CONVERTER_PROMPT, prompts.ASSERTION_REVIEWER_PROMPT):
        assert "source" in prompt
        assert "trigger" in prompt
        assert "destination" in prompt
        assert "conflicting_targets" in prompt
        assert "completion-holder" in prompt
    assert "Context and proxy discipline" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Convergence rule" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "Mandatory event-response gate" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Mandatory event-response review gate" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "source-trigger-destination" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "behavior_phase" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert 'pseudo-initial source is exactly `"[*]"`' in prompts.ASSERTION_REVIEWER_PROMPT
    assert "must not demand an invented direct edge" in prompts.ASSERTION_CONVERTER_PROMPT


def test_quantitative_effect_prompts_forbid_guessed_variable_names() -> None:
    assert "never invent or enumerate candidate variable names" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "without `variable=`" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "reject every invented identifier" in prompts.ASSERTION_REVIEWER_PROMPT


def test_prompts_merge_one_repair_unit_and_preserve_attributable_mismatch() -> None:
    assert "Repair-unit atomicity" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "same misplaced state" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "Do not leave a repair-relevant destination mismatch" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Attribution-preserving mismatch gate" in prompts.ASSERTION_REVIEWER_PROMPT


def test_prompts_enforce_positive_conflict_assertion_direction() -> None:
    assert "positive distinguishability obligation" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "positive distinguishability Requirement" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "not conflicting_targets" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Reject bare `conflicting_targets" in prompts.ASSERTION_REVIEWER_PROMPT


def test_requirement_prompts_distinguish_local_exit_from_completion() -> None:
    assert "Local-exit grounding" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "Local-exit review" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "separate completion/termination target" in prompts.REQUIREMENT_SPLITTER_PROMPT


def test_requirement_prompts_do_not_treat_missing_discriminator_as_nondeterminism() -> None:
    assert "Missing discriminator text" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "only an explicit statement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "absence of an explicit ban" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "separate distinguishability Requirement" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "undifferentiated condition set" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "different target-specific condition clauses" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "binding normalization" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "global guard mutual exclusion" in prompts.REQUIREMENT_REVIEWER_PROMPT


def test_assertion_prompts_distinguish_composed_completion_from_wrong_target() -> None:
    assert "Hierarchical completion distinction" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "Hierarchical completion review" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "genuine wrong direct target" in prompts.ASSERTION_CONVERTER_PROMPT
    for prompt in (prompts.ASSERTION_CONVERTER_PROMPT, prompts.ASSERTION_REVIEWER_PROMPT):
        assert "Limitation non-waiver" in prompt
        assert "cannot" in prompt or "may not" in prompt
        assert "Cardinality evidence gate" in prompt
        assert "Multi-step response gate" in prompt
    for benchmark_token in ("exit_hwy", "FinishState", "Power_Off", "R45RouteToken"):
        assert benchmark_token not in prompts.ASSERTION_CONVERTER_PROMPT
        assert benchmark_token not in prompts.ASSERTION_REVIEWER_PROMPT


def test_requirements_do_not_expose_benchmark_issue_taxonomy() -> None:
    assert "semantic_tags" not in Requirement.model_fields
    assert "hidden issue taxonomy" in prompts.REQUIREMENT_SPLITTER_PROMPT


def _input(run_id: str = "r") -> DiscoverInput:
    return DiscoverInput(
        run_id=run_id,
        natural_language="After go, Done shall become active.",
        stm_text=MODEL,
        language="en-US",
    )


def test_fake_stategraph_runs_complete_without_old_agent_loop_import() -> None:
    assert "paper_stm_repair_loop" not in sys.modules


def test_ambiguous_segment_is_disposed_not_missing() -> None:
    """Ambiguity is a recorded disposition, not an uncovered NL segment."""
    discover_input = _input().model_copy(
        update={"natural_language": "After go, Done shall become active.\nThe mode wording is ambiguous."}
    )

    def responder(role: str, schema: type[BaseModel], _: str, __: str) -> BaseModel:
        if schema is RequirementSet:
            return RequirementSet(
                revision=1,
                requirements=(
                    Requirement(
                        requirement_id="REQ-001",
                        statement="The system enters Idle.",
                        source_segment_ids=("NL-L001",),
                        checkability="structure",
                    ),
                ),
                segment_disposition={
                    "NL-L001": "covered",
                    "NL-L002": "ambiguous",
                },
            )
        if schema is RequirementReview:
            return RequirementReview(
                decision="accept",
                reviewed_revision=1,
                rationale="The ambiguous segment is explicitly retained for audit.",
            )
        return default_fake_responder(role, schema, _, __)

    state = run_discover_state(discover_input, responder)
    assert state["requirement_coverage"].missing_segment_ids == ()
    assert state["requirement_set"].segment_disposition["NL-L002"] == "ambiguous"
    completed = run_discover(
        _input("pair-0000")
    )
    assert completed.status == "completed"
    assert completed.run_id == "pair-0000"
    assert completed.adjudication.has_confirmed_issues is False
    assert "paper_stm_repair_loop" not in sys.modules


def test_review_payload_hides_sealed_and_released_truth_values() -> None:
    completed_states: list[dict[str, Any]] = []
    graph = build_discover_graph()
    for event in graph.stream(
        {
            "_input": _input("truth-hide")
        },
        stream_mode="updates",
    ):
        completed_states.append(event)
    release_index = next(
        index for index, item in enumerate(completed_states) if "release_results" in item
    )
    pre_release = completed_states[:release_index]
    assert pre_release
    dumped_pre_release = json.dumps(pre_release, default=str).lower()
    assert "truth_value" not in dumped_pre_release
    assert "_sealed_payload" not in dumped_pre_release
    review_event = next(item for item in pre_release if "review_assertions" in item)
    dumped = json.dumps(review_event["review_assertions"], default=str).lower()
    assert "truth_value" not in dumped
    assert "_sealed_payload" not in dumped


def test_runtime_callback_path_consumes_stream_updates_to_completion() -> None:
    updates: list[str] = []
    state = run_discover_state(
        _input("stream-callback"),
        on_update=lambda node_name, _update: updates.append(node_name),
    )
    assert updates[0] == "prepare"
    assert "adjudicate_results" in updates
    assert updates[-1] == "publish"
    assert state["final_output"].status == "completed"


def test_convert_failure_terminates_even_with_stale_contract_feedback() -> None:
    state = {
        "failure": object(),
        "_assertion_conversion_contract_feedback": RevisionFeedback(
            target="assertions",
            origin="assertion_contract",
            reason="Revise the invalid script.",
        ),
    }

    assert route_after_convert(state) == "run_failed"  # type: ignore[arg-type]


def test_renderer_assertion_review_input_has_no_truth_labels() -> None:
    from paper_stm_feedback_loop.discover.nodes import _fallback_prepare

    frozen = _fallback_prepare(
        _input()
    )
    reqs = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "NL",
                "checkability": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "check",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover.nodes import precheck_and_seal

    state = {
        "_input": _input(),
        "frozen_inputs": frozen,
        "assertion_script": script,
    }
    checked = precheck_and_seal(state, sealed_store=InMemorySealedStore())
    payload = renderer.render_assertion_review_input(
        frozen, reqs, script, checked["assertion_check_public"]
    )
    assert "truth_value" not in payload
    assert "sealed_payload" not in payload
    assert "sealed_hash" not in payload


def test_effect_fbmcq_bare_reach_is_rejected_before_sealing() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    def fake_bmc_runner(*_args: Any, **_kwargs: Any) -> tuple[str, int]:
        return (
            json.dumps(
                {
                    "result": {"status": "sat", "property_satisfied": True},
                    "property": {"kind": "reach", "bound": 5},
                    "replay": {"ok": True},
                }
            ),
            0,
        )

    discover_input = _input("bare-formal")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Bare bounded reachability.",
                "expression": (
                    "fbmcq('check reach <= 5: active(\"Root.Done\");').holds is True"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not reached",
                "evidence_family": "fbmcq",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checker = AssertionChecker(
        EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )

    assert checked["assertion_check_public"].status == "invalid"
    assert "bare reach target is not causal evidence" in (
        checked["assertion_check_public"].executions[0].error or ""
    )
    assert "hot-start simulation" in (
        checked["assertion_check_public"].executions[0].error or ""
    )
    repeated = nodes.precheck_and_seal(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    assert "no-progress gate" in repeated["failure"].message


def test_changed_invalid_script_is_not_treated_as_no_progress() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("changed-invalid-script")
    frozen = nodes._fallback_prepare(discover_input)

    def make_script(description: str, expression: str) -> AssertionScript:
        return AssertionScript(
            revision=1,
            assertions=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "description": description,
                    "expression": expression,
                    "failure_message": "[REQ-001][AST-REQ-001-01] helper failure",
                    "evidence_family": "structure",
                },
            ),
            requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
        )

    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A structure check.",
                "checkability": "structure",
            },
        ),
    )
    checker = AssertionChecker(
        EvalEnvironment(
            model_text=MODEL,
            extra_functions={
                "broken_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(AssertionError("backend failed")),
                ),
                "revised_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(AssertionError("backend failed again")),
                ),
            },
        )
    )
    store = InMemorySealedStore()
    first = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": make_script("first version", "broken_helper()"),
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    second = nodes.precheck_and_seal(
        {
            **first,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": make_script(
                "materially revised version", "revised_helper()"
            ),
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    assert "failure" not in second
    assert second["assertion_check_public"].status == "invalid"


def test_effect_cold_start_feedback_gives_hot_start_repair_shape() -> None:
    from paper_stm_feedback_loop.assertions import AssertionChecker, EvalEnvironment, InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("cold-effect")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Cold trace is insufficient.",
                "expression": "simulate(cycles=[['Root.go']]).final.is_active('Root.Done')",
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )
    error = checked["assertion_check_public"].executions[0].error or ""
    assert "initial_state=<exact state path>" in error
    assert "declaration name" in error


def test_invalid_effect_simulation_reports_script_error_before_hot_start_policy() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("invalid-effect-script"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The converter omitted a closing list bracket.",
                "expression": "simulate(cycles=[['Root.go'])",
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.precheck_and_seal(
        {
            "_input": _input("invalid-effect-script"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )

    error = out["assertion_check_public"].executions[0].error or ""
    assert "AssertionScriptSyntaxError" in error
    assert "hot-start" not in error


def test_name_error_feedback_forbids_rename_only_alias_repair() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("invalid-alias"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The assertion uses an undefined state alias.",
                "expression": (
                    "simulate(cycles=[['Root.go']], initial_state=human, "
                    "initial_vars={}).final.is_active('Root.Done')"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.precheck_and_seal(
        {
            "_input": _input("invalid-alias"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )

    error = out["assertion_check_public"].executions[0].error or ""
    assert "Do not rename an undefined alias" in error
    assert "quoted complete state/event path" in error


def test_effect_initialization_cold_path_is_allowed_when_explicit() -> None:
    from paper_stm_feedback_loop.assertions import AssertionChecker, EvalEnvironment, InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("initial-cold-effect")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After go, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Explicit initialization path.",
                "expression": "(lambda s: 'Root.go' in s.cycles[1].consumed_events and s.cycles[1].is_active('Root.Done'))(simulate(cycles=[[], ['Root.go']]))",
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )
    assert checked["assertion_check_public"].status == "executable"


def test_initialization_wording_does_not_bypass_effect_simulation_contract() -> None:
    from paper_stm_feedback_loop.assertions import AssertionChecker, EvalEnvironment, InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("initial-only-observation")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
                {
                    "requirement_id": "REQ-001",
                    "statement": "The system shall begin in the Root.Idle state.",
                    "checkability": "effect",
                },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "No-event initial-state observation.",
                "expression": "simulate(cycles=[[]]).final.is_active('Root.Idle')",
                "failure_message": "[REQ-001][AST-REQ-001-01] Root.Idle is not initially active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )
    assert checked["assertion_check_public"].status == "invalid"
    assert "hot-start" in str(checked["_assertion_feedback"].findings[0])


def test_pure_initial_configuration_allows_empty_cold_start_cycles() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("initial-configuration")
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "The system shall begin in the Root.Idle state.",
                "checkability": "effect",
                "source_context": {"behavior_phase": "initialization"},
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Finite cold-start initial configuration.",
                "expression": "simulate(cycles=[[], []]).final.is_active('Root.Idle')",
                "failure_message": "[REQ-001][AST-REQ-001-01] Root.Idle is not initially active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=MODEL)),
    )
    assert checked["assertion_check_public"].status == "executable"


def test_strict_schemas_reject_inconclusive_and_bad_review_shapes() -> None:
    with pytest.raises(ValidationError):
        DiscoverAdjudication.model_validate(
            {
                "has_confirmed_issues": False,
                "issues": [],
                "rationale": "ok",
                "truth_value": None,
            }
        )
    with pytest.raises(ValidationError):
        RequirementReview(
            decision="accept",
            reviewed_revision=1,
            findings=(
                {"severity": "important", "message": "x", "required_change": "y"},
            ),
            rationale="bad",
        )


def test_create_revise_pairs_and_no_progress_gate_are_enforced() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(
        _input()
    )
    current = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A",
                "checkability": "structure",
            },
        ),
    )

    def stale_responder(
        _role: str, schema: type[BaseModel], _system: str, _input: str
    ) -> BaseModel:
        assert schema is RequirementSet
        return current

    state = {
        "_input": _input(),
        "frozen_inputs": frozen,
        "requirement_set": current,
    }
    out = nodes.split_requirements(
        state, nodes.CallableStructuredResponder(stale_responder)
    )
    assert out["failure"].node_name == "split_requirements"
    assert "pair" in out["failure"].message


def test_converter_contract_reject_routes_existing_script_back_with_feedback() -> None:
    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.graph import route_after_convert

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "Done shall become active after go.",
                "checkability": "structure",
            },
        ),
    )
    current = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "current",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] current",
                "evidence_family": "structure",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    invalid_revision = current.model_copy(
        update={
            "revision": 2,
            "assertions": (
                current.assertions[0].model_copy(
                    update={
                        "failure_message": "[REQ-WRONG][AST-REQ-001-01] wrong owner",
                    }
                ),
            ),
        }
    )
    state = {
        "_input": _input("converter-contract"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": current,
        "_assertion_feedback": RevisionFeedback(
            target="assertions", reason="review requested a revision", findings=("scope",)
        ),
    }
    out = nodes.convert_assertions(
        state,
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: invalid_revision
        ),
    )
    assert "failure" not in out
    assert out["_assertion_conversion_contract_feedback"].findings
    assert out["_assertion_contract_repair_count"] == 1
    assert route_after_convert(out) == "convert_assertions"
    assert out["node_execution_records"][0].status == "failed"


def test_effect_requirement_rejects_relation_only_evidence() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )
    current = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "current relation check",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] relation",
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    state = {
        "_input": _input("effect-contract"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": current,
        "_assertion_feedback": RevisionFeedback(
            target="assertions", reason="review requested a revision"
        ),
    }
    out = nodes.convert_assertions(
        state,
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: current.model_copy(
                update={"revision": 2}
            )
        ),
    )
    assert "failure" not in out
    assert "effect, simulation, or fbmcq" in out["_assertion_conversion_contract_feedback"].findings[0]


def test_effect_only_evidence_can_expose_missing_typed_effect_without_simulation() -> None:
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )
    from paper_stm_feedback_loop.discover import nodes

    model = (
        ROOT / "fixtures/selected_models/0006/STM_0.fcstm"
    ).read_text(encoding="utf-8")
    discover_input = _input("effect-only").model_copy(
        update={
            "natural_language": (
                "After Attack_Complete, the UAV quantity shall decrease."
            ),
            "stm_text": model,
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "After Attack_Complete, the UAV quantity shall decrease.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The named quantity has no typed decrement effect.",
                "expression": (
                    "any(delta < 0 for _, delta in effect_deltas("
                    "source='Root.Attack', event='Root.Attack_Complete', "
                    "target='Root.Searching', variable='UAV_Quantity'))"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] UAV_Quantity does not decrease "
                    "on Attack_Complete"
                ),
                "evidence_family": "effect",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=AssertionChecker(EvalEnvironment(model_text=model)),
    )

    assert checked["assertion_check_public"].status == "executable"
    released = store.release(checked["sealed_assertion_results"].sealed_hash)
    assert len(released) == 1
    assert released[0].truth_value is False
    assert released[0].evidence_family == "effect"


def test_effect_requirement_does_not_accept_relation_only_after_contract_relaxation() -> None:
    """The new effect exception is narrow: relation remains insufficient."""

    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )
    relation_only = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "Only a transition relation is checked.",
                "expression": (
                    "transition_exists(source='Root.Idle', event='Root.go', "
                    "target='Root.Done')"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] effect missing",
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("relation-only-after-relaxation"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(
            lambda _role, _schema, _system, _payload: relation_only
        ),
    )

    assert out["_assertion_conversion_contract_feedback"].findings
    assert "effect, simulation, or fbmcq" in out[
        "_assertion_conversion_contract_feedback"
    ].findings[0]


def test_assertion_reviewer_has_a_bounded_revision_gate() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("bounded-review"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "Done shall become active after go.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "bounded check",
                "expression": (
                    "simulate(cycles=[['Root.go']], initial_state='Root.Idle', "
                    "initial_vars={}).final.is_active('Root.Done')"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done is not active",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    public_check = AssertionCheckPublic(
        script_hash=sha256_data(script),
        tool_env_hash=frozen.tool_env_hash,
        status="executable",
        executions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "executable",
            },
        ),
    )

    def always_revise(
        _role: str, schema: type[BaseModel], _system: str, _payload: str
    ) -> BaseModel:
        assert schema is AssertionReview
        return AssertionReview(
            decision="revise",
            reviewed_script_hash=sha256_data(script),
            findings=(
                {
                    "assertion_id": "AST-REQ-001-01",
                    "requirement_id": "REQ-001",
                    "severity": "important",
                    "message": "repeatable review finding",
                    "required_change": "make a material change",
                },
            ),
            rationale="repeatable review",
        )

    base_state = {
        "_input": _input("bounded-review"),
        "frozen_inputs": frozen,
        "requirement_set": requirements,
        "assertion_script": script,
        "assertion_check_public": public_check,
    }
    responder = nodes.CallableStructuredResponder(always_revise)
    for count in range(nodes.MAX_ASSERTION_REVIEW_REPAIRS):
        out = nodes.review_assertions(
            {**base_state, "_assertion_review_repair_count": count}, responder
        )
        assert "failure" not in out
        assert out["_assertion_review_repair_count"] == count + 1

    out = nodes.review_assertions(
        {
            **base_state,
            "_assertion_review_repair_count": nodes.MAX_ASSERTION_REVIEW_REPAIRS,
        },
        responder,
    )
    assert "failure" in out
    assert "bounded review gate" in out["failure"].message


def test_initial_converter_contract_violation_enters_bounded_revision() -> None:
    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.discover.graph import route_after_convert

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )
    invalid = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "relation only",
                "expression": "transition_exists(source='Root.Idle', event='Root.go', target='Root.Done')",
                "failure_message": "[REQ-001][AST-REQ-001-01] relation only",
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.convert_assertions(
        {
            "_input": _input("initial-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        nodes.CallableStructuredResponder(lambda *_args: invalid),
    )
    assert "failure" not in out
    assert out["assertion_script"].revision == 1
    assert out["_assertion_contract_repair_count"] == 1
    assert "effect, simulation, or fbmcq" in out["_assertion_feedback"].findings[0]
    assert route_after_convert(out) == "convert_assertions"


def test_repeated_contract_invalid_script_stops_without_five_duplicate_calls() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("repeat-contract"))
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, the system shall enter Done.",
                "checkability": "effect",
            },
        ),
    )
    invalid = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "relation only",
                "expression": "True",
                "failure_message": "[REQ-001][AST-REQ-001-01] relation only",
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    revisions = iter((1, 2))
    responder = nodes.CallableStructuredResponder(
        lambda _role, _schema, _system, _payload: invalid.model_copy(
            update={"revision": next(revisions)}
        )
    )
    first = nodes.convert_assertions(
        {
            "_input": _input("repeat-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
        },
        responder,
    )
    assert "failure" not in first
    second = nodes.convert_assertions(
        {
            "_input": _input("repeat-contract"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": first["assertion_script"],
            "_assertion_feedback": first["_assertion_feedback"],
            "_assertion_contract_failure_signatures": first[
                "_assertion_contract_failure_signatures"
            ],
            "_assertion_contract_repair_count": first[
                "_assertion_contract_repair_count"
            ],
        },
        responder,
    )
    assert "failure" in second
    assert "repeated contract-invalid" in second["failure"].message


def test_splitter_failure_routes_directly_to_run_failed_without_reviewer_masking() -> None:
    from paper_stm_feedback_loop.discover.graph import run_discover_state

    def fail_splitter(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        if schema is RequirementSet:
            raise RuntimeError("splitter transport failed")
        raise AssertionError("downstream reviewer must not be called")

    with pytest.raises(RuntimeError, match="split_requirements.*splitter transport failed"):
        run_discover_state(_input("split-failure"), fail_splitter)


def test_assertion_precheck_seals_strict_bool_and_invalid_exceptions() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(
        _input()
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "ok",
                "expression": "len(states()) > 0",
                "failure_message": "[REQ-001][AST-REQ-001-01] no states",
                "evidence_family": "structure",
            },
            {
                "assertion_id": "AST-REQ-001-02",
                "requirement_id": "REQ-001",
                "description": "bad",
                "expression": "broken_helper()",
                "failure_message": "[REQ-001][AST-REQ-001-02] helper failure",
                "evidence_family": "structure",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import (
        AssertionChecker,
        EvalEnvironment,
        InMemorySealedStore,
    )

    checker = AssertionChecker(
        EvalEnvironment(
            model_text=MODEL,
            extra_functions={
                "broken_helper": (
                    "structure",
                    lambda: (_ for _ in ()).throw(AssertionError("backend failed")),
                )
            },
        )
    )
    store = InMemorySealedStore()
    out = nodes.precheck_and_seal(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
        assertion_checker=checker,
    )
    public = out["assertion_check_public"]
    assert public.status == "invalid"
    assert public.executions[0].status == "executable"
    assert public.executions[1].status == "invalid"
    receipt = out["sealed_assertion_results"]
    sealed = store.release(receipt.sealed_hash)
    assert len(sealed) == 1
    assert sealed[0].truth_value is True


def test_effect_simulation_precheck_allows_explicit_cold_path() -> None:
    from paper_stm_feedback_loop.discover import nodes
    from paper_stm_feedback_loop.assertions import InMemorySealedStore

    frozen = nodes._fallback_prepare(_input())
    requirements = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "When go occurs, Done shall become active.",
                "checkability": "effect",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "explicit initialization cold-path witness",
                "expression": (
                    "(lambda s: 'Root.go' in s.cycles[1].consumed_events and s.cycles[1].is_active('Root.Done'))(simulate(cycles=[[], ['Root.go']]))"
                ),
                "failure_message": "[REQ-001][AST-REQ-001-01] Done was not reached",
                "evidence_family": "simulation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    out = nodes.precheck_and_seal(
        {
            "_input": _input("hot-start-policy"),
            "frozen_inputs": frozen,
            "requirement_set": requirements,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
    )
    assert out["assertion_check_public"].status == "executable"


def test_prompts_are_english_and_ban_tools_or_truth_leak() -> None:
    all_prompts = "\n".join(
        [
            prompts.REQUIREMENT_SPLITTER_PROMPT,
            prompts.REQUIREMENT_REVIEWER_PROMPT,
            prompts.ASSERTION_CONVERTER_PROMPT,
            prompts.ASSERTION_REVIEWER_PROMPT,
            prompts.RESULT_ADJUDICATOR_PROMPT,
        ]
    )
    assert "use tools" in all_prompts
    assert "AgentApp" not in all_prompts
    assert "sealed-result-blind" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "True/False" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "do not define functions or classes" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "public_check.script_hash" in prompts.ASSERTION_REVIEWER_PROMPT
    assert "behavioral requirement" in prompts.REQUIREMENT_SPLITTER_PROMPT
    assert "checkability classification" in prompts.REQUIREMENT_REVIEWER_PROMPT
    assert "at least one `effect`, `simulation`, or `fbmcq`" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "only evidence is static relation" in prompts.ASSERTION_REVIEWER_PROMPT


def test_cli_main_writes_output(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from paper_stm_feedback_loop.discover.cli import main
    from paper_stm_feedback_loop.discover import cli, nodes

    nl = tmp_path / "nl.txt"
    stm = tmp_path / "STM_0.fcstm"
    trace = tmp_path / "source_trace.json"
    nl.write_text("After go, Done shall become active.", encoding="utf-8")
    stm.write_text(MODEL, encoding="utf-8")
    trace.write_text('{"entries": [], "attribution_exclusions": []}', encoding="utf-8")
    monkeypatch.setattr(
        cli,
        "DirectStructuredResponder",
        lambda *_args, **_kwargs: nodes.CallableStructuredResponder(
            nodes.default_fake_responder
        ),
    )
    output = tmp_path / "run"
    assert (
        main(
            [
                "--case-id",
                "custom-0000",
                "--nl-file",
                str(nl),
                "--fcstm-file",
                str(stm),
                "--source-trace-file",
                str(trace),
                "--profile",
                "test-profile",
                "--content-language",
                "en-US",
                "--output-dir",
                str(output),
            ]
        )
        == 0
    )
    data = json.loads((output / "discover-completed.json").read_text(encoding="utf-8"))
    assert data["run_id"].startswith("custom-0000-test-profile-")
    assert data["status"] == "completed"
    assert (output / "loops" / "discover.md").is_file()
    assert list((output / "records").glob("L000-*-discover-completed/record.json"))


def test_cli_failure_writes_auditable_receipt(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from paper_stm_feedback_loop.discover import cli

    nl = tmp_path / "nl.txt"
    stm = tmp_path / "STM_0.fcstm"
    trace = tmp_path / "source_trace.json"
    nl.write_text("After go, Done shall become active.", encoding="utf-8")
    stm.write_text(MODEL, encoding="utf-8")
    trace.write_text('{"entries": [], "attribution_exclusions": []}', encoding="utf-8")
    monkeypatch.setattr(cli, "DirectStructuredResponder", lambda *_args, **_kwargs: object())
    monkeypatch.setattr(
        cli,
        "run_discover_state",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(RuntimeError("bounded review gate")),
    )
    output = tmp_path / "failed-run"
    with pytest.raises(RuntimeError, match="bounded review gate"):
        cli.main(
            [
                "--case-id",
                "custom-failure",
                "--nl-file",
                str(nl),
                "--fcstm-file",
                str(stm),
                "--source-trace-file",
                str(trace),
                "--profile",
                "test-profile",
                "--output-dir",
                str(output),
            ]
        )
    failure = json.loads((output / "discover-failed.json").read_text(encoding="utf-8"))
    assert failure["status"] == "failed"
    assert "bounded review gate" in failure["error_message"]
    assert "records/" in (output / "loops" / "discover-failed.md").read_text(encoding="utf-8")


def test_assertion_review_hash_must_match_current_script() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(
        _input()
    )
    reqs = RequirementSet(
        revision=1,
        requirements=(
            {
                "requirement_id": "REQ-001",
                "statement": "A",
                "checkability": "structure",
            },
        ),
    )
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "ok",
                "expression": "len(states()) > 0",
                "failure_message": "[REQ-001][AST-REQ-001-01] no states",
                "evidence_family": "structure",
            },
        ),
    )
    from paper_stm_feedback_loop.assertions import InMemorySealedStore

    checked = nodes.precheck_and_seal(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=InMemorySealedStore(),
    )

    def wrong_hash(
        _role: str, schema: type[BaseModel], _system: str, _input: str
    ) -> BaseModel:
        assert schema is AssertionReview
        return AssertionReview(
            decision="accept", reviewed_script_hash="bad", rationale="ok"
        )

    out = nodes.review_assertions(
        {
            "_input": _input(),
            "frozen_inputs": frozen,
            "requirement_set": reqs,
            "assertion_script": script,
            **checked,
        },
        nodes.CallableStructuredResponder(wrong_hash),
    )
    assert out["failure"].node_name == "review_assertions"
    assert (
        sha256_data(script) in out["failure"].message
        or "must match" in out["failure"].message
    )


def test_confirmed_issue_schema_rejects_unsafe_attribution() -> None:
    with pytest.raises(ValidationError):
        DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-001",
                    "requirement_id": "REQ-001",
                    "assertion_ids": ("AST-REQ-001-01",),
                    "title": "Unsafe finding",
                    "rationale": "False but source attribution is absent.",
                    "attribution_status": "unattributed",
                },
            ),
            rationale="must fail",
        )


def test_false_assertion_on_excluded_compiler_ref_is_representation_debt() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input().model_copy(
        update={
            "source_trace": {
                "entries": [],
                "attribution_exclusions": ["compiler:state:Root.Done"],
            }
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A deliberately absent transition.",
                "expression": "transition_exists(source='Root.Done', event='Root.go', target='Root.Idle')",
                "failure_message": "[REQ-001][AST-REQ-001-01] reverse transition is absent",
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False


def test_route_control_guarded_relation_is_representation_debt() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    model = """def int R45RouteToken = 0;
state Root {
    state Entry;
    [*] -> Entry : if [R45RouteToken == 5] effect { R45RouteToken = 0; };
}
"""
    discover_input = _input("route-control-relation").model_copy(
        update={
            "stm_text": model,
            "source_trace": {
                "entries": [],
                "attribution_exclusions": [
                    "compiler:route_control:R45RouteToken"
                ],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The initial relation should be unconditional.",
                "expression": (
                    "any(t.guard is None for t in "
                    "transitions(source='[*]', target='Root.Entry'))"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] initial relation is guarded"
                ),
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )

    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert "compiler:route_control:R45RouteToken" in binding.exclusion_refs


def test_wrong_target_near_miss_remains_source_attributable() -> None:
    from paper_stm_feedback_loop.assertions import InMemorySealedStore
    from paper_stm_feedback_loop.discover import nodes

    model = """state Root {
    event leave;
    state Cruise;
    state Exit;
    state Finish;
    [*] -> Cruise;
    Cruise -> Finish : leave;
}
"""
    discover_input = _input("wrong-target-near-miss").model_copy(
        update={
            "stm_text": model,
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:wrong-target",
                        "intermediate_elements": [
                            "Root.Cruise",
                            "Root.leave",
                            "Root.Finish",
                        ],
                        "source_elements": ["source:transition:wrong-target"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "The local exit must reach Exit.",
                "expression": (
                    "transition_exists(source='Root.Cruise', "
                    "event='Root.leave', target='Root.Exit')"
                ),
                "failure_message": (
                    "[REQ-001][AST-REQ-001-01] local exit reaches wrong target"
                ),
                "evidence_family": "relation",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    store = InMemorySealedStore()
    checked = nodes.precheck_and_seal(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    released = nodes.release_results(
        {
            **checked,
            "_input": discover_input,
            "frozen_inputs": frozen,
            "assertion_script": script,
        },
        sealed_store=store,
    )
    attributed = nodes.bind_attribution(
        {**released, "_input": discover_input, "frozen_inputs": frozen}
    )

    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "safe"
    assert binding.source_refs == ("source:transition:wrong-target",)


def test_simulation_false_on_ineligible_contract_is_representation_debt() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("simulation-ineligible").model_copy(
        update={
            "manifest": {
                "working_contract": {
                    "capability_eligibility": {
                        "simulation": {"status": "ineligible"}
                    }
                }
            },
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="simulation",
                check_detail={"function_call_trace": [{"args": ["Root.Done"]}]},
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False
    assert "contract:capability_eligibility.simulation" in binding.exclusion_refs


def test_simulation_false_without_ineligible_contract_keeps_source_trace_policy() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("simulation-eligible").model_copy(
        update={
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            }
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="simulation",
                check_detail={"function_call_trace": [{"args": ["Root.Done"]}]},
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "safe"


def test_mixed_effect_assertion_using_simulation_respects_ineligible_gate() -> None:
    from paper_stm_feedback_loop.discover import nodes

    discover_input = _input("mixed-simulation-ineligible").model_copy(
        update={
            "manifest": {
                "working_contract": {
                    "capability_eligibility": {
                        "simulation": {"status": "ineligible"}
                    }
                }
            },
            "source_trace": {
                "entries": [
                    {
                        "trace_id": "trace:state:Root.Done",
                        "intermediate_elements": ["Root.Done"],
                        "source_elements": ["source:state:Done"],
                        "attribution_boundary": {
                            "source_level_claim_allowed": True,
                            "representation_related": False,
                            "conversion_or_lowering_related": False,
                        },
                    }
                ],
                "attribution_exclusions": [],
            },
        }
    )
    frozen = nodes._fallback_prepare(discover_input)
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="effect",
                evidence_scope={
                    "actual_function_families": ["effect", "simulation"]
                },
                check_detail={
                    "actual_function_families": ["effect", "simulation"],
                    "function_call_trace": [{"args": ["Root.Done"]}],
                },
            ),
        ),
    )

    attributed = nodes.bind_attribution(
        {
            "_input": discover_input,
            "frozen_inputs": frozen,
            "released_assertion_results": released,
        }
    )
    binding = attributed["attribution_projection"].bindings[0]
    assert binding.status == "representation_debt"
    assert binding.source_level_claim_allowed is False
    assert "contract:capability_eligibility.simulation" in binding.exclusion_refs


def test_attribution_matching_requires_exact_structured_path() -> None:
    from paper_stm_feedback_loop.discover.nodes import _reference_matches_observed

    assert _reference_matches_observed(
        "state:case.Controller.Idle", {"case.Controller.Idle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"case.OtherRegion.Idle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"case.Controller.NotIdle"}
    )
    assert not _reference_matches_observed(
        "state:case.Controller.Idle", {"event:case.Controller.Idle"}
    )
    assert _reference_matches_observed(
        "compiler:route_control:R45RouteToken", {"R45RouteToken"}
    )
    assert _reference_matches_observed(
        "compiler:event_projection:Root.pedestrian_or_distance",
        {"Root.pedestrian_or_distance"},
    )


def test_adjudicator_must_account_for_every_safe_false_assertion() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("adjudication-closure"))
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A deliberately contradicted requirement.",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
            },
        ),
        requirement_mapping={"REQ-001": ("AST-REQ-001-01",)},
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "safe",
                "source_refs": ("state:Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )

    def omit_false(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        assert schema is DiscoverAdjudication
        return DiscoverAdjudication(
            has_confirmed_issues=False,
            issues=(),
            satisfied_requirement_ids=(),
            excluded_findings=(),
            rationale="omitted false assertion",
        )

    out = nodes.adjudicate_results(
        {
            "_input": _input("adjudication-closure"),
            "frozen_inputs": frozen,
            "requirement_set": RequirementSet(
                revision=1,
                requirements=(
                    {
                        "requirement_id": "REQ-001",
                        "statement": "A",
                        "checkability": "structure",
                    },
                ),
            ),
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(omit_false),
    )
    assert out["failure"].node_name == "adjudicate_results"
    assert "every attribution-safe False assertion" in out["failure"].message


def test_adjudicator_reconciles_derived_satisfied_ids_without_dropping_findings() -> None:
    from paper_stm_feedback_loop.discover import nodes

    frozen = nodes._fallback_prepare(_input("adjudication-reconcile"))
    script = AssertionScript(
        revision=1,
        assertions=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "description": "A contradicted requirement.",
                "expression": "False",
                "failure_message": "[REQ-001][AST-REQ-001-01] requirement failed",
                "evidence_family": "structure",
            },
            {
                "assertion_id": "AST-REQ-002-01",
                "requirement_id": "REQ-002",
                "description": "A satisfied requirement.",
                "expression": "True",
                "failure_message": "[REQ-002][AST-REQ-002-01] requirement failed",
                "evidence_family": "structure",
            },
        ),
        requirement_mapping={
            "REQ-001": ("AST-REQ-001-01",),
            "REQ-002": ("AST-REQ-002-01",),
        },
    )
    released = ReleasedAssertionResults(
        script_hash="script",
        tool_env_hash="env",
        sealed_hash="sealed",
        results=(
            AssertionResult(
                assertion_id="AST-REQ-001-01",
                requirement_id="REQ-001",
                truth_value=False,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
            AssertionResult(
                assertion_id="AST-REQ-002-01",
                requirement_id="REQ-002",
                truth_value=True,
                script_hash="script",
                tool_env_hash="env",
                evidence_family="structure",
            ),
        ),
    )
    attribution = AttributionProjection(
        bindings=(
            {
                "assertion_id": "AST-REQ-001-01",
                "requirement_id": "REQ-001",
                "status": "safe",
                "source_refs": ("state:Root.Done",),
                "trace_entry_ids": ("trace-1",),
                "source_level_claim_allowed": True,
                "rationale": "source-owned",
            },
        )
    )

    def overreports_satisfied(
        _role: str, schema: type[BaseModel], _system: str, _input_text: str
    ) -> BaseModel:
        assert schema is DiscoverAdjudication
        return DiscoverAdjudication(
            has_confirmed_issues=True,
            issues=(
                {
                    "issue_id": "ISSUE-REQ-001",
                    "requirement_id": "REQ-001",
                    "assertion_ids": ("AST-REQ-001-01",),
                    "title": "Requirement failed",
                    "rationale": "The safe assertion is false.",
                    "attribution_status": "safe",
                },
            ),
            # Deliberately include the false requirement: this is a derived
            # bookkeeping error that deterministic closure can correct.
            satisfied_requirement_ids=("REQ-001", "REQ-002"),
            rationale="The issue is retained and the satisfied list is provisional.",
        )

    out = nodes.adjudicate_results(
        {
            "_input": _input("adjudication-reconcile"),
            "frozen_inputs": frozen,
            "requirement_set": RequirementSet(
                revision=1,
                requirements=(
                    {"requirement_id": "REQ-001", "statement": "A", "checkability": "structure"},
                    {"requirement_id": "REQ-002", "statement": "B", "checkability": "structure"},
                ),
            ),
            "assertion_script": script,
            "released_assertion_results": released,
            "attribution_projection": attribution,
        },
        nodes.CallableStructuredResponder(overreports_satisfied),
    )
    assert "failure" not in out
    assert out["adjudication"].satisfied_requirement_ids == ("REQ-002",)
    assert out["adjudication"].issues[0].assertion_ids == ("AST-REQ-001-01",)
    assert out["_adjudication_reconciliation"]["normalization_applied"] is True
