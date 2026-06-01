from __future__ import annotations

import json
from pathlib import Path

import pytest

from method.schema import (
    FeedbackBundle,
    FixPlan,
    GroundedElement,
    GroundingMap,
    ParseFeedback,
    RepairRejection,
    RevisedFixPlan,
    ScenarioResult,
    SimFeedback,
    SpecJson,
    TestScenario as ScenarioCase,
)
from method.stages.sl_delta_review_prompt import (
    DELTA_REVIEW_DECISIONS,
    build_sl10b_delta_review_prompt,
    parse_sl10b_delta_review_response,
)
from method.stages.sl_initial_modeling_prompt import (
    build_sl1_initial_modeling_prompt,
    extract_candidate_dsl_or_legacy,
)
from method.stages.sl_model_review_prompt import (
    MODEL_REVIEW_CATEGORIES,
    build_sl7_model_review_prompt,
    parse_sl7_model_review_response,
)
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl_scenario_generation_prompt import (
    build_sl5_scenario_generation_prompt,
    parse_sl5_scenario_generation_response,
)

REPO = Path(__file__).resolve().parents[3]
METHOD_ROOT = REPO / "project_1_llm_state_machine_modeling" / "method"


def _grammar_digest() -> str:
    return "state Root { [*] -> Idle; state Idle; }"


def _grounding_map() -> GroundingMap:
    return GroundingMap(
        elements=[
            GroundedElement(
                element_id="state:Idle",
                element_kind="state",
                element_ref="Root.Idle",
                source_stage="SL-1",
                evidence_text="The controller starts idle.",
                requiredness="required",
                confidence=0.95,
            )
        ],
        source_summary={"nl": "one required idle state"},
    )


def _fix_plan() -> FixPlan:
    return FixPlan(
        target="design",
        source_stage="SD-4",
        source_feedback_id="W_DEADLOCK_LEAF:Root.Idle",
        severity="blocking_warning",
        diagnostic_ids=["W_DEADLOCK_LEAF:Root.Idle"],
        problem_summary="Root.Idle has no outgoing transition.",
        evidence=[{"code": "W_DEADLOCK_LEAF", "refs": {"state": "Root.Idle"}}],
        suggested_fix_hints=[{"hint": "add an NL-grounded outgoing transition"}],
        recommended_strategy=["Prefer adding missing transition over deleting grounded state."],
        forbidden_edits=["Do not remove required grounded state Root.Idle."],
        nl_grounding_hints=["Idle is required by NL."],
        target_element_ids=["state:Idle"],
        required_preserve_element_ids=["state:Idle"],
        allowed_edit_kinds=["add_transition", "add_event"],
        verification_plan=["parse", "semantic", "design", "sim"],
        max_edit_scope="localized",
        before_dsl_hash="sha256:before",
    )


def test_sl1_prompt_generator_is_prompt_only_and_contains_schema() -> None:
    messages = build_sl1_initial_modeling_prompt(
        nl="When Start is pressed, move from Idle to Active.",
        spec_json={"states": ["Idle", "Active"], "events": ["Start"]},
        pyfcstm_grammar_digest=_grammar_digest(),
    )

    assert [m["role"] for m in messages] == ["system", "user"]
    joined = "\n".join(m["content"] for m in messages)
    assert "SL-1" in joined
    assert "candidate_dsl" in joined
    assert "grounding_seeds" in joined
    assert "Output JSON only" in joined
    assert "Output ONLY the pyfcstm DSL code" not in joined
    assert "only the DSL code" not in joined
    assert "When Start is pressed" in joined
    assert "pyfcstm grammar" in joined.lower()
    assert "chat(" not in joined


def test_sl5_prompt_parser_returns_typed_scenarios_and_prompt_includes_context() -> None:
    messages = build_sl5_scenario_generation_prompt(
        nl="Default init reaches Idle; Start reaches Active.",
        current_dsl="state Root { [*] -> Idle; state Idle; state Active; Idle -> Active :: Start; }",
        inspect_json={"states": [{"path": "Root.Idle"}, {"path": "Root.Active"}]},
        design_summary={"blocking_items": []},
        grounding_map=_grounding_map(),
        coverage_directive="Cover Start transition.",
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "SL-5" in joined
    assert "TestScenario" in joined
    assert "GroundingMap" in joined
    assert "Cover Start transition" in joined

    scenarios = parse_sl5_scenario_generation_response(
        json.dumps(
            {
                "scenarios": [
                    {
                        "name": "start_reaches_active",
                        "description": "Start event moves Idle to Active.",
                        "initial_state": "Root.Idle",
                        "initial_vars": {},
                        "steps": [
                            {
                                "name": "after_start",
                                "events": ["Start"],
                                "expected_state": "Root.Active",
                            }
                        ],
                    }
                ]
            }
        )
    )

    assert len(scenarios) == 1
    assert isinstance(scenarios[0], ScenarioCase)
    assert scenarios[0].steps[0].expected_state == "Root.Active"


def test_sl5_parser_accepts_string_before_cycles_and_rejects_non_numeric() -> None:
    scenarios = parse_sl5_scenario_generation_response(
        json.dumps(
            {
                "scenarios": [
                    {
                        "name": "string_cycles",
                        "steps": [
                            {
                                "name": "wait",
                                "before_cycles": "3",
                                "events": [],
                                "expected_state": "Root.Idle",
                            }
                        ],
                    }
                ]
            }
        )
    )

    assert scenarios[0].steps[0].before_cycles == 3

    with pytest.raises(ValueError, match="before_cycles"):
        parse_sl5_scenario_generation_response(
            json.dumps({"scenarios": [{"name": "bad", "steps": [{"before_cycles": "later"}]}]})
        )


@pytest.mark.parametrize("category", sorted(MODEL_REVIEW_CATEGORIES))
def test_sl7_model_review_parser_accepts_all_issue14_categories(category: str) -> None:
    payload = {
        "decision": "fail",
        "risk_level": "major",
        "findings": [
            {
                "category": category,
                "severity": "major",
                "summary": "finding",
                "evidence": [{"element_id": "state:Idle"}],
            }
        ],
        "blocking_findings": [
            {
                "category": category,
                "severity": "major",
                "summary": "finding",
                "evidence": [{"element_id": "state:Idle"}],
            }
        ],
    }

    parsed = parse_sl7_model_review_response(json.dumps(payload))

    assert parsed["decision"] == "fail"
    assert parsed["findings"][0]["category"] == category


def test_sl7_prompt_contains_required_contract_fields() -> None:
    messages = build_sl7_model_review_prompt(
        nl="Start should activate the controller.",
        current_dsl="state Root { [*] -> Idle; state Idle; }",
        grounding_map=_grounding_map(),
        inspect_json={"states": ["Root.Idle"]},
        design_diagnostics_summary={"blocking_items": []},
        sim_summary={"ok": True, "n_scenarios": 1},
        five_component_summary={"states": 1, "events": 1, "transitions": 1},
        warning_budget_exhausted=["W_DEADLOCK_LEAF:Root.Idle"],
        review_policy={"mode": "audit_only", "failure_policy": "fail_open"},
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "SL-7" in joined
    assert "5-component summary" in joined
    assert "warning budget exhausted" in joined
    assert "ReviewPolicy" in joined
    assert "five_component_summary" in joined
    assert "warning_budget_exhausted" in joined
    assert "review_policy" in joined
    for category in MODEL_REVIEW_CATEGORIES:
        assert category in joined


def test_sl9_repair_prompt_accepts_fix_plan_and_revised_fix_plan() -> None:
    plan = _fix_plan()
    revised = RevisedFixPlan(
        original=plan,
        rejection=RepairRejection(
            rejected_by_stage="SD-10",
            reason="required state was deleted",
            target_resolved=False,
            regression_detected=True,
            drift_risk="major",
            evidence=[{"deleted_element_id": "state:Idle"}],
        ),
        revision_count=1,
    )

    messages = build_sl9_repair_prompt(
        nl="Idle is required; Start activates the controller.",
        current_dsl="state Root { [*] -> Idle; state Idle; }",
        fix_plan=revised,
        grounding_map=_grounding_map(),
        selected_diagnostics=[{"code": "W_DEADLOCK_LEAF"}],
        grammar_digest=_grammar_digest(),
        preserve_list=["state:Idle"],
        scenario_summary={"passing_scenarios": ["default_idle"]},
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "SL-9" in joined
    assert "RevisedFixPlan" in joined
    assert "RepairRejection" in joined
    assert "suggested_fix" in joined
    assert "hint, not a command" in joined
    assert "state:Idle" in joined
    assert "Output corrected pyfcstm DSL only" in joined


def test_modeler_agent_passes_nl_into_sl1_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    import method.agents.modeler as modeler

    captured: dict[str, object] = {}

    def fake_chat(*, messages, **kwargs):
        captured["messages"] = messages
        return (
            json.dumps(
                {
                    "candidate_dsl": "state Root { [*] -> Idle; state Idle; }",
                    "grounding_seeds": [],
                    "assumptions": [],
                }
            ),
            {},
        )

    monkeypatch.setattr(modeler, "chat", fake_chat)
    modeler.generate_model(
        SpecJson(states=["Idle"], raw={"states": ["Idle"]}),
        nl="Original NL evidence.",
    )

    joined = "\n".join(m["content"] for m in captured["messages"])
    assert "Original NL evidence." in joined


def test_sl1_legacy_dsl_extractor_still_supports_fenced_raw_dsl() -> None:
    assert (
        extract_candidate_dsl_or_legacy("```pyfcstm\nstate Root { [*] -> Idle; state Idle; }\n```")
        == "state Root { [*] -> Idle; state Idle; }"
    )


def test_repair_agent_uses_structured_sl9_inputs_without_repeating_nl_and_dsl(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    import method.agents.repair as repair

    captured: dict[str, object] = {}

    def fake_chat(*, messages, **kwargs):
        captured["messages"] = messages
        return ("state Root { [*] -> Idle; state Idle; }", {})

    monkeypatch.setattr(repair, "chat", fake_chat)
    repair.repair_model(
        "state Root { [*] -> Idle; state Idle; }",
        FeedbackBundle(parse=ParseFeedback(ok=False, error_message="parse failed")),
        nl="Original NL.",
    )

    user = captured["messages"][1]["content"]
    system = captured["messages"][0]["content"]
    assert user.count("Original NL.") == 1
    assert user.count("state Root { [*] -> Idle; state Idle; }") == 1
    assert "selected_diagnostics" in user
    assert '"source": "parse"' in user
    assert "## pyfcstm grammar digest\n\n\n" not in system


def test_sl10b_delta_review_prompt_and_parser_contract() -> None:
    messages = build_sl10b_delta_review_prompt(
        nl="Idle is required; Start activates the controller.",
        grounding_map=_grounding_map(),
        old_dsl="state Root { [*] -> Idle; state Idle; }",
        candidate_dsl="state Root { [*] -> Active; state Active; }",
        fix_plan=_fix_plan(),
        diff_summary={"deleted": ["Root.Idle"], "added": ["Root.Active"]},
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "SL-10B" in joined
    assert "old DSL" in joined
    assert "candidate DSL" in joined
    assert "diff summary" in joined
    assert "drift_evidence" in joined

    parsed = parse_sl10b_delta_review_response(
        json.dumps(
            {
                "decision": "reject",
                "drift_risk": "major",
                "drift_evidence": [{"deleted_required": "state:Idle"}],
                "required_revision": ["Restore Idle."],
            }
        )
    )

    assert parsed["decision"] in DELTA_REVIEW_DECISIONS
    assert parsed["drift_risk"] == "major"


def test_fake_review_response_rejects_unknown_category_and_invalid_decision() -> None:
    with pytest.raises(ValueError, match="unknown SL-7 finding category"):
        parse_sl7_model_review_response(
            json.dumps(
                {
                    "decision": "fail",
                    "risk_level": "major",
                    "findings": [{"category": "made_up", "severity": "major", "summary": "x"}],
                    "blocking_findings": [],
                }
            )
        )

    with pytest.raises(ValueError, match="SL-10B decision"):
        parse_sl10b_delta_review_response(
            json.dumps(
                {
                    "decision": "maybe",
                    "drift_risk": "minor",
                    "drift_evidence": [],
                }
            )
        )


def test_agents_reuse_sl_prompt_generators() -> None:
    import method.agents.modeler as modeler
    import method.agents.repair as repair
    import method.agents.scenariogen.generate as scenariogen

    assert modeler.build_sl1_initial_modeling_prompt is build_sl1_initial_modeling_prompt
    assert repair.build_sl9_repair_prompt is build_sl9_repair_prompt
    assert scenariogen.build_sl5_scenario_generation_prompt is build_sl5_scenario_generation_prompt


def test_sl_docs_and_skill_links_cover_pr1b_contract() -> None:
    docs = {
        "SL-1": METHOD_ROOT / "stages" / "docs" / "SL-1-initial-modeling.md",
        "SL-5": METHOD_ROOT / "stages" / "docs" / "SL-5-scenario-generation.md",
        "SL-7": METHOD_ROOT / "stages" / "docs" / "SL-7-lightweight-model-review.md",
        "SL-9": METHOD_ROOT / "stages" / "docs" / "SL-9-repair.md",
        "SL-10B": METHOD_ROOT / "stages" / "docs" / "SL-10B-delta-review.md",
    }
    required_sections = [
        "## 目标",
        "## 输入",
        "## 输出",
        "## 函数名或 prompt generator 名",
        "## 最小示例",
        "## 依赖关系",
        "## 常见失败模式",
    ]

    for stage_id, path in docs.items():
        text = path.read_text(encoding="utf-8")
        assert stage_id in text
        for section in required_sections:
            assert section in text, f"{path} missing {section}"
        link = METHOD_ROOT / "agent_loop_skill" / "stages" / f"{stage_id}.md"
        assert link.is_symlink(), f"{link} should be a symlink"
        assert link.exists(), f"{link} target should exist"

    prompts_md = (METHOD_ROOT / "agent_loop_skill" / "prompts.md").read_text(encoding="utf-8")
    for generator_name in [
        "build_sl1_initial_modeling_prompt",
        "build_sl5_scenario_generation_prompt",
        "build_sl7_model_review_prompt",
        "build_sl9_repair_prompt",
        "build_sl10b_delta_review_prompt",
    ]:
        assert generator_name in prompts_md

    sl7_text = docs["SL-7"].read_text(encoding="utf-8")
    for category in MODEL_REVIEW_CATEGORIES:
        assert category in sl7_text

    sl10b_text = docs["SL-10B"].read_text(encoding="utf-8")
    for decision in DELTA_REVIEW_DECISIONS:
        assert decision in sl10b_text
