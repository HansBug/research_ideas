from __future__ import annotations

import json
import re
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
    compact_sl7_review_input,
    parse_sl7_model_review_response,
)
from method.stages.sl_repair_prompt import build_sl9_repair_prompt
from method.stages.sl_scenario_generation_prompt import (
    build_sl5_scenario_generation_prompt,
    compact_sl5_inspect_for_prompt,
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


def test_pyfcstm_grammar_digest_documents_parseable_boolean_flag_subset() -> None:
    grammar = (METHOD_ROOT / "prompts" / "_pyfcstm_grammar.md").read_text(encoding="utf-8")

    assert "def bool armed = false;" not in grammar
    assert "Boolean-like flags MUST be encoded as `int`" in grammar
    assert "never `def bool`" in grammar
    assert "no `// ...`, no `/* ... */`" in grammar
    assert "root-level `! * -> Manual ..." in grammar
    assert "exists only as a nested child" in grammar
    assert "Plain `during { ... }` is only used on leaf states" in grammar
    assert "if (expr)" in grammar
    assert "NL events are represented with `:: EventName`" in grammar


def test_sl1_and_sl9_prompts_carry_pr_e1_parse_subset_constraints() -> None:
    sl1 = "\n".join(
        message["content"]
        for message in build_sl1_initial_modeling_prompt(
            nl="A fault flag controls fallback.",
            pyfcstm_grammar_digest="def int flag = 0; state Root { [*] -> Idle; state Idle; }",
        )
    )
    sl9 = "\n".join(
        message["content"]
        for message in build_sl9_repair_prompt(
            nl="A fault flag controls fallback.",
            current_dsl="def bool fault = false; state Root { [*] -> Idle; state Idle; }",
            fix_plan={"target": "parse"},
            selected_diagnostics=[{"code": "SyntaxFailError", "got": "bool"}],
            grammar_digest="def int flag = 0; state Root { [*] -> Idle; state Idle; }",
            repair_target="parse",
        )
    )

    assert "do not emit" in sl1
    assert "`def bool`, `true`, `false`, `!flag`" in sl1
    assert "target a state resolvable in that scope" in sl1
    assert "`max(...)` or `min(...)`" in sl1
    assert "Use plain `during { ... }` only on leaf states" in sl1
    assert "never `if (expr)`" in sl1
    assert "Treat NL trigger names" in sl1
    assert "Target-aware repair rules" in sl9
    assert "meaningless self-assignments" in sl9
    assert "Root-level forced transitions may only target states resolvable" in sl9
    assert "E_DURING_ASPECT_INVALID" in sl9
    assert "If diagnostics show undeclared event-like names" in sl9
    assert "make every required" in sl9
    assert "Do not rewrite event-triggered transitions into chain-scope `: Event`" in sl9
    assert "Output exactly one complete DSL file" in sl9
    assert "default-init scenarios usually need an empty cycle" in sl9
    assert "mental NL obligation ledger" in sl1
    assert "A parseable empty shell is not" in sl1
    assert "nfrr_quality_cap" in sl9
    assert "agent_loop_root_cause" in sl9
    assert "structurally too small for explicit NL obligations" in sl9


def test_sl5_prompt_parser_returns_typed_scenarios_and_prompt_includes_context() -> None:
    previous = [
        ScenarioCase(
            name="default_init_reaches_idle",
            description="default-init probe",
            steps=[{"before_cycles": 1, "expected_state": "Root.Idle"}],
        )
    ]
    messages = build_sl5_scenario_generation_prompt(
        nl="Default init reaches Idle; Start reaches Active.",
        current_dsl="state Root { [*] -> Idle; state Idle; state Active; Idle -> Active :: Start; }",
        inspect_json={"states": [{"path": "Root.Idle"}, {"path": "Root.Active"}]},
        design_summary={"blocking_items": []},
        grounding_map=_grounding_map(),
        coverage_directive="Cover Start transition.",
        previous_scenarios=previous,
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "SL-5" in joined
    assert "TestScenario" in joined
    assert "GroundingMap" in joined
    assert "Cover Start transition" in joined
    assert "before_cycles: 1" in joined
    assert "NL/DSL-grounded local event names" in joined
    assert "`StartEvent`" in joined
    assert "`ResetEvent`" in joined
    assert "Avoid over-asserting weak or incidental variables" in joined
    assert "previous_scenarios" in joined
    assert "default_init_reaches_idle" in joined
    assert "preserve their names" in joined
    assert "initial-state provenance" in joined

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


def test_sl5_prompt_compacts_large_inspect_payload_and_avoids_duplicate_dsl() -> None:
    """SL-5 should not resend huge raw inspect graphs or duplicate full DSL.

    PR-E1 real LNG diagnostics showed repeated provider 5xx around a large
    structured SL-5 request.  This is a general prompt-shape problem, not a
    benchmark special case: scenario generation needs a compact model summary
    plus one DSL block, not the full SD-4 inspect payload and the same DSL
    twice.  This test must not impose a small context-window assumption.
    """

    current_dsl = "state Root { [*] -> S0; " + " ".join(f"state S{i};" for i in range(50)) + " }"
    large_inspect = {
        "root_state_path": "Root",
        "states": [
            {"path": f"Root.S{i}", "children": [f"Root.S{i}.C{j}" for j in range(20)], "long": "s" * 1000}
            for i in range(60)
        ],
        "transitions": [
            {"source": f"Root.S{i}", "target": f"Root.S{i+1}", "guard": "x > 0 " * 200, "effect": "y = y + 1;" * 80}
            for i in range(59)
        ],
        "variables": [{"name": f"v{i}", "type": "float", "dataflow": "d" * 1000} for i in range(60)],
        "events": [{"name": f"E{i}", "detail": "e" * 1000} for i in range(60)],
        "actions": [{"state": f"Root.S{i}", "text": "a" * 1000} for i in range(60)],
        "diagnostics": [{"code": "W_X", "severity": "warning", "message": "m" * 2000} for _ in range(60)],
        "metrics": {"state_count": 60, "transition_count": 59},
        "var_dataflow": {"very_large": "v" * 20000},
        "reachability_graph": {"very_large": "r" * 20000},
        "action_ref_graph": {"very_large": "a" * 20000},
    }

    compact = compact_sl5_inspect_for_prompt(large_inspect)
    messages = build_sl5_scenario_generation_prompt(
        nl="Exercise representative state transitions.",
        current_dsl=current_dsl,
        inspect_json=large_inspect,
        design_summary={"blocking_items": [], "context": "c" * 10000},
        grounding_map=_grounding_map(),
    )
    joined = "\n".join(m["content"] for m in messages)

    assert compact["state_count"] == 60
    assert compact["transition_count"] == 59
    assert "_truncated_items" in json.dumps(compact, ensure_ascii=False)
    assert "compact_inspect_summary" in joined
    assert "\"current_dsl\"" not in joined
    assert joined.count("```pyfcstm") == 1
    assert "m" * 2000 not in joined
    assert "very_large" not in joined
    assert len(joined) < len(json.dumps(large_inspect, ensure_ascii=False))


def test_sl9_prompt_contains_preserve_checklist_and_variable_role_context() -> None:
    messages = build_sl9_repair_prompt(
        nl="The controller reads sensor value ext from external input signals before selecting Active.",
        current_dsl="def int ext = 0; state Root { [*] -> Idle; state Idle; state Active; Idle -> Active : if [ext > 0]; }",
        fix_plan=_fix_plan(),
        selected_diagnostics=[
            {
                "source": "design",
                "source_stage": "SD-4",
                "variable_role_summary": {
                    "source": "SD-4 diagnostic refs and generic NL external-input rationale",
                    "variables": {"ext": {"role_hint": "external_input_candidate"}},
                },
            }
        ],
        preserve_list=["state:Idle", "transition:Idle_to_Active"],
        grammar_digest=_grammar_digest(),
        repair_target="design",
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "variable_role_summary" in joined
    assert "external-input vs internal-state" in joined
    assert "required_preserve_element_ids" in joined
    assert "no unrelated grounded branch was deleted" in joined
    assert "no new ungrounded plant/environment dynamics were invented" in joined


def test_sl9_prompt_carries_rework_repair_memory() -> None:
    messages = build_sl9_repair_prompt(
        nl="The repaired candidate must preserve required grounding.",
        current_dsl="state Root { [*] -> Idle; state Idle; }",
        fix_plan=_fix_plan(),
        fix_log=[
            {
                "entry_id": "fixlog-2-sl10_review",
                "phase": "sl10_review",
                "candidate_dsl_hash": "sha256:old",
                "repair_memory": {
                    "actionable_rework_guidance": [
                        {"kind": "missing_required_grounding", "instruction": "explain state:Required"}
                    ]
                },
            }
        ],
        repair_memory={
            "repeated_candidate_hashes": ["sha256:old"],
            "latest_actionable_rework_guidance": [
                {"kind": "missing_required_grounding", "instruction": "explain state:Required"}
            ],
        },
        grammar_digest=_grammar_digest(),
        repair_target="design",
    )
    joined = "\n".join(m["content"] for m in messages)

    assert "repair_memory" in joined
    assert "repeated candidate hashes" in joined
    assert "sha256:old" in joined
    assert "missing_required_grounding" in joined



def test_default_agent_loop_prompts_do_not_contain_pr_e1_sample_specific_tokens() -> None:
    """Guard against benchmark overfit in default agent-loop prompts.

    PR-E1 may keep concrete sample metadata in ``pr_e1_real_runs.py`` and run
    artifacts, but the reusable SL prompt contracts and grammar digest must not
    contain lexical hints from the evaluated ABS/CARA/Elevator/LNG samples.
    """

    sample_specific_tokens = {
        "ABS",
        "CARA",
        "Elevator",
        "LNG",
        "StartAC",
        "Ask_StartAC",
        "Autocontrol",
        "PS1",
        "PS2",
        "PS3",
        "path1_cara",
        "path2_lng",
        "case_id",
        "case_key",
    }
    prompts = {
        "SL-1": "\n".join(
            message["content"]
            for message in build_sl1_initial_modeling_prompt(
                nl="A synthetic actuator starts waiting; BeginMove enters Moving; ArriveDone enters Done.",
                spec_json={"states": ["Waiting", "Moving", "Done"], "events": ["BeginMove", "ArriveDone"]},
            )
        ),
        "SL-5": "\n".join(
            message["content"]
            for message in build_sl5_scenario_generation_prompt(
                nl="A synthetic actuator starts waiting; BeginMove enters Moving; ArriveDone enters Done.",
                current_dsl="state SyntheticActuator { [*] -> Waiting; state Waiting; state Moving; state Done; Waiting -> Moving :: BeginMove; Moving -> Done :: ArriveDone; }",
            )
        ),
        "SL-9": "\n".join(
            message["content"]
            for message in build_sl9_repair_prompt(
                nl="A synthetic actuator starts waiting; BeginMove enters Moving; ArriveDone enters Done.",
                current_dsl="state SyntheticActuator { [*] -> Waiting; state Waiting; }",
                fix_plan={"target": "design"},
            )
        ),
    }

    for prompt_name, prompt_text in prompts.items():
        hits = sorted(
            token
            for token in sample_specific_tokens
            if re.search(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])", prompt_text)
        )
        assert hits == [], f"{prompt_name} prompt contains PR-E1 sample-specific token(s): {hits}"


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
    assert "NFRR v3 is a review rubric, not a deterministic SD hard gate" in joined
    assert "T2 within-scope candidate" in joined
    assert "nfrr_quality_cap" in joined
    assert "agent_loop_root_cause" in joined
    assert "Do not stop at \"model quality is poor\"" in joined


def test_sl7_nfrr_quality_categories_parse_and_do_not_imply_sd_gate() -> None:
    parsed = parse_sl7_model_review_response(
        json.dumps(
            {
                "decision": "fail",
                "risk_level": "major",
                "findings": [
                    {
                        "category": "nfrr_quality_cap",
                        "severity": "major",
                        "summary": "T1 cap: NL requires multiple branches but DSL is an empty shell.",
                        "evidence": [{"tier": "T1", "cap_reasons": ["critical_required_missing"]}],
                    },
                    {
                        "category": "agent_loop_root_cause",
                        "severity": "major",
                        "summary": "Likely SL-1 obligation extraction missed required transitions.",
                        "evidence": [{"stage": "SL-1"}],
                    },
                ],
                "blocking_findings": [
                    {
                        "category": "agent_loop_root_cause",
                        "severity": "major",
                        "summary": "Fix root cause rather than only reporting poor quality.",
                        "evidence": [{"stage": "SL-1"}],
                    }
                ],
            }
        )
    )

    assert parsed["findings"][0]["category"] == "nfrr_quality_cap"
    assert parsed["blocking_findings"][0]["category"] == "agent_loop_root_cause"


def test_sl7_prompt_compacts_large_inspect_and_design_payloads() -> None:
    large_inspect = {
        "root_state_path": "Root",
        "states": [{"path": f"Root.S{i}", "children": [f"C{j}" for j in range(20)]} for i in range(40)],
        "transitions": [{"source": f"S{i}", "target": f"S{i+1}", "guard": "x > 0" * 100} for i in range(40)],
        "variables": [{"name": f"v{i}", "type": "float", "init": 0} for i in range(40)],
        "events": [{"name": f"e{i}"} for i in range(40)],
        "actions": [{"name": f"a{i}"} for i in range(40)],
        "diagnostics": [{"code": "W_X", "severity": "warning", "message": "m" * 2000} for _ in range(40)],
        "metrics": {"state_count": 40},
    }
    large_design = {
        "ok": True,
        "policy_profile": "path_smoke",
        "blocking_items": [],
        "advisory_items": [{"code": "W_X", "message": "long" * 1000, "refs": {"i": i}} for i in range(40)],
        "info_items": [{"code": "I_X", "message": "long" * 1000, "refs": {"i": i}} for i in range(40)],
        "inspect_summary": {"diagnostic_codes": ["W_X"] * 40, "prompt_ready_summary": "p" * 4000},
    }

    compact = compact_sl7_review_input(
        inspect_json=large_inspect,
        design_diagnostics_summary=large_design,
        sim_summary={"ok": True, "scenario_results": [{"name": f"s{i}", "status": "pass"} for i in range(20)]},
    )
    messages = build_sl7_model_review_prompt(
        nl="Start should activate the controller.",
        current_dsl="state Root { [*] -> S0; state S0; }",
        grounding_map=_grounding_map(),
        inspect_json=large_inspect,
        design_diagnostics_summary=large_design,
        sim_summary={"ok": True, "scenario_results": [{"name": f"s{i}", "status": "pass"} for i in range(20)]},
        review_policy={"mode": "audit_only"},
    )
    joined = "\n".join(m["content"] for m in messages)

    assert compact["inspect_model_to_json_summary"]["state_count"] == 40
    assert compact["design_diagnostics_summary"]["advisory_count"] == 40
    assert "_truncated_items" in joined
    assert "inspect_model_to_json_summary" in joined
    assert "design_diagnostics_summary" in joined
    assert len(joined) < 30000
    assert "m" * 2000 not in joined
    assert "long" * 1000 not in joined



def test_parse_json_response_preserves_backticks_inside_fenced_json_string() -> None:
    raw = json.dumps(
        {
            "decision": "audit_only",
            "risk_level": "none",
            "findings": [
                {
                    "category": "structure_smell",
                    "severity": "info",
                    "summary": "DSL text contains a literal ``` fence marker in evidence.",
                    "evidence": ["```pyfcstm\nstate Root { }\n```"],
                }
            ],
            "blocking_findings": [],
        },
        ensure_ascii=False,
    )

    parsed = parse_sl7_model_review_response(f"```json\n{raw}\n```")

    assert parsed["decision"] == "audit_only"
    assert "```pyfcstm" in parsed["findings"][0]["evidence"][0]

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
