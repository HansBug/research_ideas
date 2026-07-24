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
from paper_stm_feedback_loop.discover.graph import build_discover_graph, run_discover  # noqa: E402
from paper_stm_feedback_loop.discover.schemas import (  # noqa: E402
    AssertionReview,
    AssertionResult,
    AssertionScript,
    AttributionProjection,
    ReleasedAssertionResults,
    DiscoverAdjudication,
    DiscoverInput,
    RequirementReview,
    RequirementSet,
    RevisionFeedback,
)
from paper_stm_feedback_loop.discover.utils import sha256_data  # noqa: E402

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


def test_simulation_prompts_distinguish_initial_variable_names_from_result_paths() -> None:
    assert "declaration names, not qualified paths" in prompts.ASSERTION_CONVERTER_PROMPT
    assert "declaration names rather than qualified state-machine paths" in prompts.ASSERTION_REVIEWER_PROMPT


def _input(run_id: str = "r") -> DiscoverInput:
    return DiscoverInput(
        run_id=run_id,
        natural_language="After go, Done shall become active.",
        stm_text=MODEL,
        language="en-US",
    )


def test_fake_stategraph_runs_complete_without_old_agent_loop_import() -> None:
    assert "paper_stm_repair_loop" not in sys.modules
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
    store = InMemorySealedStore()
    checker = AssertionChecker(
        EvalEnvironment(model_text=MODEL, bmc_runner=fake_bmc_runner)
    )
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
    assert "causal bounded FBMCQ" in (
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
    assert "simulation or fbmcq" in out["_assertion_conversion_contract_feedback"].findings[0]


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


def test_effect_simulation_precheck_requires_hot_start() -> None:
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
                "description": "cold behavior witness",
                "expression": (
                    "simulate(cycles=[[], ['go']]).final.is_active('Root.Done')"
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
    assert out["assertion_check_public"].status == "invalid"
    assert "hot-start" in out["assertion_check_public"].executions[0].error


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
    assert "at least one `simulation` or `fbmcq`" in prompts.ASSERTION_CONVERTER_PROMPT
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
