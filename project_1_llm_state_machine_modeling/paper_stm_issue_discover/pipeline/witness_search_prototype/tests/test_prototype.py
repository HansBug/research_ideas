from __future__ import annotations

import copy
import importlib.util
import json
import re
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "prototype.py"
SPEC = importlib.util.spec_from_file_location("witness_search_prototype", MODULE_PATH)
assert SPEC and SPEC.loader
prototype = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = prototype
SPEC.loader.exec_module(prototype)


def _pair_and_inspect(case: str = "0029"):
    pair = prototype.load_pair(case)
    inspect = prototype.inspect_fcstm(
        pair["fcstm"], pair["paths"]["fcstm"], smt_timeout_ms=3_000
    )
    return pair, inspect


def test_context_contains_all_views_and_mapping_comments() -> None:
    pair, inspect = _pair_and_inspect()
    context = prototype.build_context(pair, inspect)

    assert "# Natural-language requirements" in context
    assert "# Author-source PlantUML" in context
    assert "# Converted FCSTM with source/compiler mapping comments" in context
    assert "# Execution/source attribution boundary" in context
    assert "# Verify-enabled pyfcstm inspect cause summary" in context
    assert "cause_clusters" in context
    assert "PUML:L12 lower:direct" in context
    assert "PUML:L31 identity" in context
    assert "W_UNREACHABLE_STATE" in context
    assert "expected_issue" not in context


def test_fcstm_annotations_use_exact_ast_paths_for_duplicate_short_names() -> None:
    fcstm = """state Root named \"Root\" {
    state A named \"A\" {
        state Same named \"Same A\";
    }
    state B named \"B\" {
        state Same named \"Same B\";
    }
}"""
    contract = {
        "elements": [
            {
                "kind": "state",
                "origin": "source_owned",
                "source_refs": ["case.puml:line:10"],
                "metadata": {"fcstm_path": "Root.A.Same"},
            },
            {
                "kind": "state",
                "origin": "source_owned",
                "source_refs": ["case.puml:line:20"],
                "metadata": {"fcstm_path": "Root.B.Same"},
            },
        ]
    }

    annotated = prototype.annotate_fcstm(fcstm, contract).splitlines()

    assert "PUML:L10 identity" in annotated[2]
    assert "PUML:L20 identity" not in annotated[2]
    assert "PUML:L20 identity" in annotated[5]
    assert "PUML:L10 identity" not in annotated[5]


def test_attribution_exclusions_use_closed_formal_reference_projection() -> None:
    exclusions = ["compiler:state:Root.Generated"]

    assert prototype._reference_matches_exclusion("Root.Generated", exclusions)
    assert prototype._reference_matches_exclusion(
        "compiler:state:Root.Generated", exclusions
    )
    assert not prototype._reference_matches_exclusion("Generated", exclusions)
    assert not prototype._reference_matches_exclusion(
        "unknown:state:Root.Generated", exclusions
    )


def test_known_0029_l2_probes_produce_replayable_artifact_counterexamples() -> None:
    pair, inspect = _pair_and_inspect()
    root = pair["pair_name"]
    plan = prototype.ProbePlan(
        evidence_summary="Three behavior-level hypotheses from source and inspect clues.",
        candidates=[
            prototype.ProbeCandidate(
                rationale="NL requires the collision-avoidance subsystem to operate.",
                claim="The collision-avoidance initial state is unreachable.",
                basis_kind="nl_literal",
                nl_quote="The collision avoidance system is initially in the collision_avoidance_deactive state.",
                locations=["NL12"],
                priority=5,
                checks=[
                    prototype.ProbeCheck(
                        rationale="Search from root entry to the required initial state.",
                        kind="reaches",
                        source="[*]",
                        target=f"{root}.CollisionAvoidance.collision_avoidance_deactive",
                        within_cycles=4,
                    )
                ],
            ),
            prototype.ProbeCandidate(
                rationale="NL says auto_finished exits UrbanMode into a finish state.",
                claim="The urban completion event does not terminate execution.",
                basis_kind="nl_literal",
                nl_quote="The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.",
                locations=["NL10"],
                priority=5,
                checks=[
                    prototype.ProbeCheck(
                        rationale="Apply auto_finished from a reachable urban leaf.",
                        kind="terminates",
                        source=f"{root}.UrbanMode.straight",
                        trigger="auto_finished=true",
                    )
                ],
            ),
            prototype.ProbeCandidate(
                rationale="The converted target is nested under HighwayMode.",
                claim="Urban completion incorrectly enters HighwayMode.FinishState.",
                basis_kind="nl_literal",
                nl_quote="The system exits the UrbanMode state by transitioning to FinishState once `auto_finished=true` is satisfied.",
                locations=["NL10"],
                priority=5,
                checks=[
                    prototype.ProbeCheck(
                        rationale="The wrong nested finish target must not become active.",
                        kind="occupancy_after",
                        source=f"{root}.UrbanMode.straight",
                        trigger=f"{root}.auto_finished_true",
                        target=f"{root}.HighwayMode.FinishState",
                        within_cycles=3,
                        expected=False,
                    )
                ],
            ),
        ],
    )

    outcomes = prototype.execute_plan(pair, inspect, plan)
    groups = [item["probe_groups"][0] for item in outcomes]

    assert len(outcomes) == 3
    assert all(item["planner_envelope_only"] is True for item in outcomes)
    assert all("source_candidate" not in item for item in outcomes)
    assert all(group["witness_level"] == "W2" for group in groups)
    assert all(group["counterexample_found"] is True for group in groups)
    assert all(item["nl_anchor_valid"] is True for item in outcomes)
    assert groups[1]["checks"][0]["normalizations"] == [
        {
            "field": "trigger",
            "from": "auto_finished=true",
            "to": f"{root}.auto_finished_true",
        }
    ]


def test_0023_projection_risk_is_not_promoted_to_source_finding() -> None:
    pair, inspect = _pair_and_inspect("0023")
    plan = prototype.ProbePlan(
        candidates=[
            prototype.ProbeCandidate(
                obligation="WaterState must be behaviorally reachable.",
                claim="WaterState is unreachable from root entry.",
                basis_kind="nl_literal",
                nl_quote="The system can also transition to the WaterState substate, indicating that the pump is controlling or monitoring the water flow.",
                priority=5,
                locations=["PUML:L6", f"{pair['pair_name']}.PumpControl.WaterState"],
                checks=[
                    prototype.ProbeCheck(
                        kind="reaches",
                        source="[*]",
                        target=f"{pair['pair_name']}.PumpControl.WaterState",
                        within_cycles=4,
                    )
                ],
            )
        ]
    )

    outcome = prototype.execute_plan(pair, inspect, plan)[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_causality_certificate"] is None
    assert group["source_attribution"]["status"] == "unattributed"
    assert group["source_candidate"] is False
    assert prototype.build_issue_clusters([outcome]) == []


def test_inspect_clues_compile_to_unexecuted_probe_seeds() -> None:
    _, inspect = _pair_and_inspect("0029")

    seeds = prototype.derive_probe_seeds(inspect)

    assert seeds
    assert any(
        seed["diagnostic_code"] == "W_UNREACHABLE_STATE"
        and seed["checks"][0]["kind"] == "reaches"
        for seed in seeds
    )


def test_malformed_probe_degrades_without_aborting_pair() -> None:
    pair, inspect = _pair_and_inspect()
    plan = prototype.ProbePlan(
        evidence_summary="Malformed probe fixture.",
        candidates=[
            prototype.ProbeCandidate(
                rationale="Exercise the degradation path.",
                claim="Missing target cannot be executed.",
                basis_kind="implicit_oracle",
                priority=1,
                checks=[
                    prototype.ProbeCheck(
                        rationale="Intentionally incomplete.",
                        kind="reaches",
                        source="[*]",
                    )
                ],
            )
        ],
    )

    outcomes = prototype.execute_plan(pair, inspect, plan)
    group = outcomes[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["source_causality_certificate"] is None
    assert group["source_candidate"] is False
    assert group["checks"][0]["result"] == "unsupported"
    findings = prototype.build_finding_records(outcomes)
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W0"
    assert findings[0]["evidence_status"] == "coverage_gap"


def _seed_for_location(seeds, suffix: str):
    return next(
        seed
        for seed in seeds
        if any(str(location).endswith(suffix) for location in seed["locations"])
    )


def test_seed_and_custom_claims_are_isolated_and_source_deadlock_is_executable() -> (
    None
):
    pair, inspect = _pair_and_inspect("0004")
    seed = _seed_for_location(
        prototype.derive_probe_seeds(inspect), ".EmergencyStopping"
    )
    root = pair["pair_name"]
    plan = prototype.ProbePlan(
        candidates=[
            prototype.ProbeCandidate(
                obligation="Obstacle response must not permanently trap the controller.",
                claim="Obstacle Detected enters EmergencyStopping.",
                basis_kind="nl_literal",
                nl_quote="if an obstacle is detected",
                locations=["NL2"],
                priority=5,
                probe_seed_ids=[seed["seed_id"]],
                checks=[
                    prototype.ProbeCheck(
                        role="primary",
                        kind="occupancy_after",
                        source=f"{root}.InMotion.Accelerating",
                        trigger="Obstacle_Detected",
                        target=f"{root}.EmergencyStopping",
                        within_cycles=4,
                    )
                ],
            )
        ]
    )

    outcome = prototype.execute_plan(pair, inspect, plan)[0]
    by_id = {group["group_id"]: group for group in outcome["probe_groups"]}
    seed_group = by_id[f"seed:{seed['seed_id']}"]
    custom_group = by_id["custom"]

    assert seed_group["claim"] == seed["hypothesis"]
    assert seed_group["counterexample_found"] is True
    assert seed_group["source_candidate"] is True
    certificate = seed_group["source_causality_certificate"]
    assert certificate["kind"] == "reachable_deadlock"
    assert certificate["sound_for_claim"] is True
    assert certificate["state_path"][-1] == "EmergencyStopping"
    assert custom_group["claim"] == "Obstacle Detected enters EmergencyStopping."
    assert custom_group["counterexample_found"] is False
    assert outcome["planner_envelope_only"] is True
    assert "counterexample_found" not in outcome
    assert len(prototype.build_issue_clusters([outcome])) == 1


def test_missing_initial_consequences_cluster_to_one_causal_source_issue() -> None:
    pair, inspect = _pair_and_inspect("0046")
    seeds = prototype.derive_probe_seeds(inspect)
    selected = [
        _seed_for_location(seeds, ".SearchRegion.Searching"),
        _seed_for_location(seeds, ".SearchRegion.FormationAdjustment"),
    ]
    quote = "the UAV swarm continuously performs target search tasks"
    plan = prototype.ProbePlan(
        candidates=[
            prototype.ProbeCandidate(
                obligation="The search region behavior must be reachable.",
                claim=f"{seed['locations'][0]} is reachable.",
                basis_kind="nl_literal",
                nl_quote=quote,
                locations=["NL2"],
                priority=5,
                probe_seed_ids=[seed["seed_id"]],
            )
            for seed in selected
        ]
    )

    outcomes = prototype.execute_plan(pair, inspect, plan, seeds)
    clusters = prototype.build_issue_clusters(outcomes)

    assert all(
        outcome["probe_groups"][0]["source_candidate"] is True for outcome in outcomes
    )
    assert len(clusters) == 1
    assert clusters[0]["cause_key"].endswith(":UAVSwarmStateMachine")
    certificate = clusters[0]["source_causality_certificate"]
    assert certificate["kind"] == "missing_initial_with_compiler_consequence"
    assert certificate["initial_edge_count"] == 0
    assert certificate["causal_bridge_result"] is True
    assert certificate["source_behavior_equivalence_claimed"] is False


def test_concurrent_region_deadlock_certifies_complete_active_tuple() -> None:
    pair, inspect = _pair_and_inspect("0023")
    seeds = prototype.derive_progressive_evidence_seeds(pair, inspect)
    expected_targets = {
        "PumpControl.PumpState",
        "PumpControl.WaterState",
        "PumpControl.MethaneState",
    }
    deadlock_seeds = [
        seed
        for seed in seeds
        if isinstance(seed.get("source_causality_certificate"), dict)
        and seed["source_causality_certificate"].get("kind")
        == "concurrent_region_deadlock"
    ]

    assert len(deadlock_seeds) == 3
    assert {
        seed["source_causality_certificate"]["target"] for seed in deadlock_seeds
    } == expected_targets
    for seed in deadlock_seeds:
        certificate = seed["source_causality_certificate"]
        assert certificate["blocked_region_targets"] == [
            "PumpControl.PumpState",
            "PumpControl.WaterState",
            "PumpControl.MethaneState",
        ]
        assert certificate["sound_for_claim"] is True
        assert certificate["verdict"] == "counterexample"
        assert certificate["outgoing"] == []
        finding = {
            "witness_level": "W2",
            "source_causality_certificate": certificate,
        }
        assert prototype._protocol_d2_grounding(finding) == "impl"


def test_compiler_fail_closed_entry_deadlock_has_exact_source_bridge() -> None:
    pair, inspect = _pair_and_inspect("0053")
    seeds = prototype.derive_progressive_evidence_seeds(pair, inspect)
    target = "llms_emp_feedback_final_0053.PumpControl.UnspecifiedInitial"
    matching = [
        seed
        for seed in seeds
        if seed.get("locations") == [target]
        and isinstance(seed.get("source_causality_certificate"), dict)
        and seed["source_causality_certificate"].get("kind")
        == "source_entry_deadlock"
    ]

    assert len(matching) == 1
    certificate = matching[0]["source_causality_certificate"]
    assert certificate["scope"] == "PumpControl"
    assert certificate["sound_for_claim"] is True
    assert certificate["verdict"] == "counterexample"
    assert certificate["assumptions"]["compiler_bridge_exact"] is True
    assert certificate["assumptions"]["compiler_bridge_transition_target_exact"] is True
    assert certificate["assumptions"]["missing_source_initial"] is True
    bridge_receipts = certificate["compiler_causal_bridge"]["initial_target_receipts"]
    assert len(bridge_receipts) == 1
    assert bridge_receipts[0]["fcstm_target"] == target
    assert bridge_receipts[0]["fcstm_initial_transition"]["target_declared"] is True
    assert bridge_receipts[0]["matches_synthetic_state"] is True
    assert certificate["outgoing"] == []
    finding = {
        "witness_level": "W2",
        "source_causality_certificate": certificate,
    }
    assert prototype._protocol_d2_grounding(finding) == "impl"


def test_entry_deadlock_requires_synthetic_transition_to_target_exact_deadlock_state() -> (
    None
):
    pair, _ = _pair_and_inspect("0053")
    target = "llms_emp_feedback_final_0053.PumpControl.UnspecifiedInitial"
    mismatched = copy.deepcopy(pair)
    mismatched["fcstm"] = mismatched["fcstm"].replace(
        "[*] -> UnspecifiedInitial;", "[*] -> PumpRegion;"
    )
    for element in mismatched["working_contract"]["elements"]:
        if element.get("kind") != "synthetic_transition":
            continue
        metadata = element.get("metadata", {})
        if metadata.get("generated_reason") == "missing_source_initial_fail_closed":
            metadata["line"] = "[*] -> PumpRegion;"

    certificate = prototype._source_entry_deadlock_certificate(
        mismatched, target, "PumpControl"
    )

    assert certificate is not None
    bridge_receipt = certificate["compiler_causal_bridge"]["initial_target_receipts"][0]
    assert bridge_receipt["fcstm_target"] == (
        "llms_emp_feedback_final_0053.PumpControl.PumpRegion"
    )
    assert bridge_receipt["matches_synthetic_state"] is False
    assert certificate["assumptions"]["compiler_bridge_transition_target_exact"] is False
    assert certificate["assumptions"]["compiler_bridge_exact"] is False
    assert certificate["sound_for_claim"] is False
    assert prototype._protocol_d2_grounding(
        {"witness_level": "W2", "source_causality_certificate": certificate}
    ) is None


def test_missing_initial_structure_and_consequences_share_one_cause_key() -> None:
    structure = {
        "kind": "initial_contract_violation",
        "scope": "Root",
    }
    consequence = {
        "kind": "missing_initial_with_compiler_consequence",
        "scope": "Root",
    }

    structure_key = prototype._certificate_cause_key(structure)
    consequence_key = prototype._certificate_cause_key(consequence)

    assert structure_key == consequence_key == "source:initial_contract:Root"


def test_empty_initial_target_contract_uses_missing_initial_cause() -> None:
    absent = {
        "kind": "source_initial_target_contract",
        "composite": "Root",
        "child": "Root.Ready",
        "actual_parent": "Root",
        "initial_edges": [],
    }
    wrong_scope = {
        "kind": "source_initial_target_contract",
        "composite": "Root.Region2",
        "child": "Root.Region1.Ready",
        "actual_parent": "Root.Region1",
        "initial_edges": [{"id": "tr_initial"}],
    }

    assert prototype._certificate_cause_key(absent) == "source:initial_contract:Root"
    assert prototype._certificate_cause_key(wrong_scope) == (
        "source:initial_target:Root.Region1:Root.Region1.Ready"
    )


def test_initial_self_target_is_l0_but_cross_scope_target_is_l1() -> None:
    self_target = {
        "source_causality_certificate": {
            "kind": "source_initial_target_contract",
            "composite": "Root.Ready",
            "child": "Root.Ready",
            "matching_edge_count": 1,
        }
    }
    cross_scope = {
        "source_causality_certificate": {
            "kind": "source_initial_target_contract",
            "composite": "Root.Region2",
            "child": "Root.Region1.Ready",
            "matching_edge_count": 1,
        }
    }

    assert prototype._infer_l_level({}, self_target) == "L0"
    assert prototype._infer_l_level({}, cross_scope) == "L1"


def test_progressive_scout_finds_initial_contract_without_llm_backend_choice() -> None:
    pair, inspect = _pair_and_inspect("0016")

    outcomes = prototype.execute_progressive_evidence_seeds(pair, inspect)
    findings = prototype.build_finding_records(outcomes)

    initial = next(
        item
        for item in findings
        if item["source_causality_certificate"]
        and item["source_causality_certificate"]["kind"] == "initial_contract_violation"
    )
    assert initial["witness_level"] == "W2"
    assert initial["source_attribution"] == ["causal_dual_certificate"]
    assert initial["formal_oracle_rules"][0]["rule_id"] == (
        "OR-PYFCSTM-INITIAL-UNCONDITIONAL-MISSING-v1"
    )
    assert initial["formal_oracle_rules"][0]["semantic_decision_claimed"] is False
    assert (
        initial["execution_certificates"][0]["semantic_binding_receipt"]["authority"]
        == "formal_pyfcstm_diagnostic"
    )
    assert initial["compiled_assertions"][0]["backend"] == "pyfcstm.inspect"
    assert (
        "inspect_model(model"
        in initial["compiled_assertions"][0]["compiled_assertion_code"]
    )


def test_progressive_quote_binding_prefers_typed_initial_contract() -> None:
    pair, _ = _pair_and_inspect("0002")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="PumpControl",
                composite_concept_id="C-PumpControl",
                target="PumpState",
                target_concept_id="C-PumpState",
                nl_line=3,
                nl_quote="The system first transitions to the PumpState substate",
                priority=5,
            )
        ],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="PumpState",
                concept_id="C-PumpState",
                role="operating_state",
                nl_quote="there are three main substates: PumpState, WaterState, and MethaneState.",
                priority=5,
            )
        ],
        required_event_scope_contracts=[],
        required_action_contracts=[],
    )
    grounding = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-PumpState",
                source_state_id="PumpControl.PumpState",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    quotes = prototype.build_progressive_normative_quote_bindings(
        pair, plan, [grounding]
    )

    assert quotes["PumpControl.PumpState"] == (
        "The system first transitions to the PumpState substate"
    )


def test_progressive_scout_does_not_read_diagnostic_message_semantics() -> None:
    pair, inspect = _pair_and_inspect("0016")
    rewritten = copy.deepcopy(inspect)
    for diagnostic in rewritten["diagnostics"]:
        diagnostic["message"] = "Unrelated prose that carries no formal authority."

    original = prototype.derive_progressive_evidence_seeds(pair, inspect)
    paraphrased = prototype.derive_progressive_evidence_seeds(pair, rewritten)

    def semantic_surface(seeds):
        return [
            {
                key: seed[key]
                for key in (
                    "cause_key",
                    "obligation",
                    "claim",
                    "formal_fact",
                    "formal_oracle_rule",
                    "locations",
                )
            }
            for seed in seeds
        ]

    assert semantic_surface(original) == semantic_surface(paraphrased)


def test_source_static_scout_executes_cross_scope_initial_targets() -> None:
    pair, inspect = _pair_and_inspect("0016")

    findings = prototype.build_finding_records(
        prototype.execute_source_static_evidence_scouts(pair, inspect)
    )

    assert len(findings) == 2
    assert {item["source_causality_certificate"]["composite"] for item in findings} == {
        "SearchMission.Region1.Region2",
        "SearchMission.Region1.Region2.Region3",
    }
    assert all(item["witness_level"] == "W2" for item in findings)
    assert all(item["counterexample_found"] is True for item in findings)
    assert all(item["l_level"] == "L1" for item in findings)
    assert all(item["w_validation_errors"] == [] for item in findings)


def test_guard_only_profile_is_syntactic_and_fail_closed() -> None:
    first = prototype.parse_guard_only_label(" [ opaque guard body ] ")
    second = prototype.parse_guard_only_label("[different formal payload]")

    assert first is not None and second is not None
    assert first.explicit_trigger is None
    assert first.effect is None
    assert first.implicit_trigger == "completion"
    assert first.profile_id == second.profile_id
    assert prototype.parse_guard_only_label("event_name [guard]") is None
    assert prototype.parse_guard_only_label("[guard] / effect") is None
    assert prototype.parse_guard_only_label("[]") is None
    assert prototype.parse_guard_only_label("[unclosed") is None


def test_source_static_scout_runs_guarded_completion_and_keeps_it_w1() -> None:
    pair, inspect = _pair_and_inspect("0054")

    findings = prototype.build_finding_records(
        prototype.execute_source_static_evidence_scouts(pair, inspect)
    )
    finding = next(
        item
        for item in findings
        if item["source_causality_certificate"]
        and item["source_causality_certificate"]["kind"]
        == "source_guarded_completion_unfireable"
    )
    certificate = finding["source_causality_certificate"]

    assert certificate["assertion_executed"] is True
    assert certificate["label_profile"] == {
        "profile_id": prototype.UML_GUARD_ONLY_PROFILE_ID,
        "explicit_trigger_absent": True,
        "guard_present": True,
        "effect_absent": True,
        "implicit_trigger": "completion",
    }
    assert certificate["final_edges"] == []
    assert certificate["fcstm_projection_audit"]["projection_declared"] is True
    assert certificate["fcstm_projection_audit"]["projection_used"] is True
    assert certificate["fcstm_projection_audit"]["representation_divergence"] is True
    assert certificate["semantic_binding_receipt"]["authority"] == "formal_source_ast"
    assert finding["witness_level"] == "W1"
    assert finding["l_level"] == "L0"
    assert finding["source_attribution"] == ["representation_debt"]
    assert finding["counterexample_found"] is True
    assert finding["compiled_assertions"]
    assert finding["execution_certificates"] == []
    assert finding["w_validation_errors"] == []
    assert prototype._language_clause_for_finding(finding)["clause_id"] == (
        "UML251_DERIVED_GUARDED_COMPLETION"
    )


def test_guarded_completion_scout_does_not_read_natural_language_prose() -> None:
    pair, inspect = _pair_and_inspect("0054")
    rewritten = dict(pair)
    rewritten["nl"] = "Unrelated prose with no shared vocabulary."

    original = prototype.execute_source_static_evidence_scouts(pair, inspect)
    changed = prototype.execute_source_static_evidence_scouts(rewritten, inspect)

    def formal_result(outcomes):
        finding = next(
            item
            for item in prototype.build_finding_records(outcomes)
            if item["source_causality_certificate"]
            and item["source_causality_certificate"]["kind"]
            == "source_guarded_completion_unfireable"
        )
        certificate = dict(finding["source_causality_certificate"])
        certificate.pop("semantic_binding_receipt")
        return {
            "certificate": certificate,
            "witness_level": finding["witness_level"],
            "l_level": finding["l_level"],
            "compiled_assertions": finding["compiled_assertions"],
        }

    assert formal_result(original) == formal_result(changed)


def test_contract_assembler_applies_only_explicit_concept_bindings() -> None:
    pair, _ = _pair_and_inspect("0030")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="Autonomous",
                composite_concept_id="C-parent",
                target="ShortName",
                target_concept_id="C-child",
                nl_line=2,
                priority=2,
            )
        ],
        containment_contracts=[],
        transition_groups=[],
    )
    discovery = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-parent",
                source_state_id="Autonomous",
            ),
            prototype.CompactConceptBinding(
                concept_id="C-child",
                source_state_id="Autonomous.Navigating",
            ),
        ],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        additional_contracts=plan,
        surface_candidates=[],
        behavior_candidates=[],
        unresolved=[],
    )

    grounded, diagnostics = prototype._assemble_grounded_contract_plan(
        pair,
        prototype.ContractExtractionPlan(
            initial_contracts=[], containment_contracts=[], transition_groups=[]
        ),
        discovery,
    )

    assert diagnostics == []
    assert grounded.initial_contracts[0].target == "Autonomous.Navigating"


def test_llm_declared_missing_state_path_executes_on_both_artifacts() -> None:
    pair, inspect = _pair_and_inspect("0030")
    candidate = prototype.EvidenceCandidate(
        obligation="A requirement-grounded completion state must exist.",
        claim="The required completion state is absent.",
        basis_kind="nl_literal",
        nl_quote=(
            "2. The autonomous mode has sub-states and is represented by a sub "
            "machine state"
        ),
        priority=1,
        locations=["NL2"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="state_exists",
            source="Autonomous",
            subject="Autonomous.RequiredCompletion",
            expected=True,
        ),
    )

    validated, diagnostics = prototype._validate_direct_grounded_candidate(
        pair,
        prototype.BalancedEvidenceCandidate(
            **candidate.model_dump(), observed_fact="No exact state path is present."
        ),
        lane="surface_candidates",
        index=0,
    )
    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(
            pair, inspect, prototype.EvidencePlan(candidates=[validated])
        )
    )

    assert diagnostics == []
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["l_level"] == "L0"
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]
    assert findings[0]["source_causality_certificate"]["kind"] == (
        "source_required_state_presence"
    )
    assert findings[0]["execution_certificates"][0]["terminal"] is True


def test_required_state_contract_is_semantically_resolved_then_executed() -> None:
    pair, inspect = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="auto final",
                concept_id="C-auto-final",
                scope_concept_id="C-autonomous",
                role="condition_state",
                nl_quote="in (auto final)",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_state_bindings=[
            prototype.RequiredStateGrounding(
                item_index=0,
                status="missing",
                formal_kind="state",
                parent_scope_id="Autonomous",
                normative_formal_path="Autonomous.AutoFinal",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(pair, inspect, evidence)
    )

    assert diagnostics == []
    assert len(evidence.surface_candidates) == 1
    assert evidence.surface_candidates[0].goal == prototype.EvidenceGoal(
        relation="state_exists",
        source="Autonomous",
        subject="Autonomous.AutoFinal",
        expected=True,
    )
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["l_level"] == "L0"
    assert findings[0]["nl_anchor_valid"] is True
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]


def test_realized_termination_role_is_expanded_into_fixed_executable_lane() -> None:
    pair, inspect = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="FinishState",
                concept_id="C-FinishState",
                role="termination_state",
                nl_quote=(
                    "The HighwayMode ends when the system transitions to FinishState"
                ),
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-FinishState",
                source_state_id="HighwayMode.FinishState",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(pair, inspect, evidence)
    )

    assert diagnostics == []
    assert len(evidence.surface_candidates) == 1
    candidate = evidence.surface_candidates[0]
    assert candidate.domain_obligation == prototype.TemporalObligation(
        pattern="termination",
        state_ref="HighwayMode.FinishState",
        expected=True,
    )
    assert candidate.goal == prototype.EvidenceGoal(
        relation="termination_target",
        subject="HighwayMode.FinishState",
        expected=True,
    )
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["l_level"] == "L2"
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]
    assert findings[0]["source_causality_certificate"]["kind"] == (
        "source_unstable_termination_target"
    )


def test_required_state_execution_is_noninterfering_in_concept_prose() -> None:
    pair, inspect = _pair_and_inspect("0030")

    def execute(concept: str):
        raw = prototype.ContractExtractionPlan(
            initial_contracts=[],
            containment_contracts=[],
            transition_groups=[],
            required_state_contracts=[
                prototype.RequiredStateContract(
                    concept=concept,
                    concept_id="C-required",
                    role="condition_state",
                    nl_quote="in (auto final)",
                    priority=1,
                )
            ],
        )
        plan = prototype.DiscoveryGroundingPlan(
            concept_bindings=[],
            initial_contract_bindings=[],
            containment_contract_bindings=[],
            transition_group_bindings=[],
            required_state_bindings=[
                prototype.RequiredStateGrounding(
                    item_index=0,
                    status="missing",
                    formal_kind="state",
                    parent_scope_id="Autonomous",
                    normative_formal_path="Autonomous.AutoFinal",
                )
            ],
            surface_candidates=[],
            behavior_candidates=[],
        )
        _, evidence, diagnostics = prototype.validate_discovery_grounding(
            pair, raw, plan
        )
        assert diagnostics == []
        return prototype.execute_evidence_plan(pair, inspect, evidence)[0][
            "probe_groups"
        ][0]

    first = execute("auto final")
    rewritten = execute("an unrelated prose name with similar-looking states nearby")

    assert first["compiled_assertion"] == rewritten["compiled_assertion"]
    assert first["counterexample_found"] is rewritten["counterexample_found"] is True
    assert first["witness_level"] == rewritten["witness_level"] == "W2"


def test_required_state_missing_resolution_fails_closed_on_existing_path() -> None:
    pair, _ = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="semantic concept",
                concept_id="C-required",
                role="condition_state",
                nl_quote="in (auto final)",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_state_bindings=[
            prototype.RequiredStateGrounding(
                item_index=0,
                status="missing",
                formal_kind="state",
                parent_scope_id="Autonomous",
                normative_formal_path="Autonomous.Navigating",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, _, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert any(
        item["class"] == "formal_missing_state_reference_invalid"
        for item in diagnostics
    )


def test_missing_final_pseudostate_executes_to_w2_when_both_views_lack_it() -> None:
    pair, inspect = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="mode completion marker",
                concept_id="C-mode-final",
                role="termination_state",
                nl_quote="in (auto final)",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_state_bindings=[
            prototype.RequiredStateGrounding(
                item_index=0,
                status="missing",
                formal_kind="final_pseudostate",
                parent_scope_id="HumanDriving",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(pair, inspect, evidence)
    )

    assert diagnostics == []
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["l_level"] == "L0"
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]
    assert findings[0]["execution_certificates"][0]["verdict"] == "counterexample"
    assert findings[0]["source_causality_certificate"]["kind"] == (
        "source_required_final_pseudostate_presence"
    )


def test_generated_final_pseudostate_is_w1_representation_debt() -> None:
    pair, inspect = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="autonomous completion marker",
                concept_id="C-auto-final",
                scope_concept_id="C-autonomous",
                role="termination_state",
                nl_quote="in (auto final)",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_state_bindings=[
            prototype.RequiredStateGrounding(
                item_index=0,
                status="missing",
                formal_kind="final_pseudostate",
                parent_scope_id="Autonomous",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(pair, inspect, evidence)
    )

    assert diagnostics == []
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W1"
    assert findings[0]["l_level"] == "L0"
    assert findings[0]["source_attribution"] == ["representation_debt"]
    assert findings[0]["execution_certificates"][0]["terminal"] is True
    assert findings[0]["execution_certificates"][0]["verdict"] == "satisfied"


def test_required_event_scope_contract_expands_and_executes_each_exact_scope() -> None:
    pair, inspect = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_event_scope_contracts=[
            prototype.RequiredEventScopeContract(
                event_concept="power-off request",
                scope_concept="each operating mode",
                applicability="each_operating_mode",
                nl_quote="5 when power off, it will transit to final state",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_event_scope_bindings=[
            prototype.RequiredEventScopeGrounding(
                item_index=0,
                status="grounded",
                observed_transition_id="tr_0007",
                required_scope_ids=["HumanDriving", "Autonomous"],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    outcomes = prototype.execute_evidence_plan(pair, inspect, evidence)
    findings = prototype.build_finding_records(outcomes)

    assert diagnostics == []
    assert [item.goal.source for item in evidence.surface_candidates] == [
        "HumanDriving",
        "Autonomous",
    ]
    assert all(
        item.goal.required_scope_ids == ["HumanDriving", "Autonomous"]
        for item in evidence.surface_candidates
    )
    assert len(outcomes) == 2
    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["source_causality_certificate"]["source"] == "Autonomous"
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]


def test_required_event_scope_grounding_fails_closed_without_exact_scopes() -> None:
    pair, _ = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_event_scope_contracts=[
            prototype.RequiredEventScopeContract(
                event_concept="power-off request",
                scope_concept="every operating mode",
                applicability="each_operating_mode",
                nl_quote="5 when power off, it will transit to final state",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        required_event_scope_bindings=[
            prototype.RequiredEventScopeGrounding(
                item_index=0,
                status="grounded",
                observed_transition_id="tr_0007",
                required_scope_ids=[],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert evidence.surface_candidates == []
    assert any(item["class"] == "binding_patch_empty" for item in diagnostics)


def test_required_event_scope_fails_closed_without_structured_event_identity() -> None:
    pair, _ = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_event_scope_contracts=[
            prototype.RequiredEventScopeContract(
                event_concept="some event",
                scope_concept="autonomous mode",
                applicability="one_scope",
                nl_quote="5 when power off, it will transit to final state",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        required_event_scope_bindings=[
            prototype.RequiredEventScopeGrounding(
                item_index=0,
                status="grounded",
                observed_transition_id="tr_0002",
                required_scope_ids=["Autonomous"],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert evidence.surface_candidates == []
    assert [item["class"] for item in diagnostics] == [
        "formal_event_identity_missing"
    ]


def test_required_event_scope_execution_ignores_contract_prose() -> None:
    pair, inspect = _pair_and_inspect("0030")

    def execute(event_concept: str, scope_concept: str) -> dict:
        raw = prototype.ContractExtractionPlan(
            initial_contracts=[],
            containment_contracts=[],
            transition_groups=[],
            required_event_scope_contracts=[
                prototype.RequiredEventScopeContract(
                    event_concept=event_concept,
                    scope_concept=scope_concept,
                    applicability="one_scope",
                    nl_quote="5 when power off, it will transit to final state",
                    priority=1,
                )
            ],
        )
        plan = prototype.DiscoveryGroundingPlan(
            concept_bindings=[],
            initial_contract_bindings=[],
            containment_contract_bindings=[],
            transition_group_bindings=[],
            required_event_scope_bindings=[
                prototype.RequiredEventScopeGrounding(
                    item_index=0,
                    status="grounded",
                    observed_transition_id="tr_0007",
                    required_scope_ids=["Autonomous"],
                )
            ],
            surface_candidates=[],
            behavior_candidates=[],
        )
        _, evidence, diagnostics = prototype.validate_discovery_grounding(
            pair, raw, plan
        )
        assert diagnostics == []
        return prototype.execute_evidence_plan(pair, inspect, evidence)[0][
            "probe_groups"
        ][0]

    first = execute("power-off request", "autonomous mode")
    paraphrase = execute(
        "unrelated narrative label that must not be parsed",
        "another reporting-only description",
    )

    assert first["compiled_assertion"] == paraphrase["compiled_assertion"]
    for field in (
        "evaluated_artifact_sha256",
        "compiled_assertion_sha256",
        "observations",
        "terminal",
        "counterexample_found",
        "verdict",
    ):
        assert (
            first["execution_certificate"][field]
            == paraphrase["execution_certificate"][field]
        )
    for field in (
        "kind",
        "evaluated_artifact_sha256",
        "observed_transition_id",
        "source",
        "event",
        "active_scopes_checked",
        "consumers",
        "actual",
        "verdict",
    ):
        assert (
            first["source_causality_certificate"][field]
            == paraphrase["source_causality_certificate"][field]
        )


def test_scope_and_descendants_expands_only_from_exact_formal_parent_links() -> None:
    pair, inspect = _pair_and_inspect("0030")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=[],
        required_event_scope_contracts=[
            prototype.RequiredEventScopeContract(
                event_concept="parking request",
                scope_concept="autonomous operation and its substates",
                applicability="scope_and_descendants",
                nl_quote="2 the auto-driving mode contains navigating and parking modes",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        required_event_scope_bindings=[
            prototype.RequiredEventScopeGrounding(
                item_index=0,
                status="grounded",
                observed_transition_id="tr_0003",
                required_scope_ids=["Autonomous"],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    outcomes = prototype.execute_evidence_plan(pair, inspect, evidence)

    assert diagnostics == []
    assert [item.goal.source for item in evidence.surface_candidates] == [
        "Autonomous",
        "Autonomous.Navigating",
        "Autonomous.Parking",
    ]
    assert all(
        item.goal.required_scope_ids
        == ["Autonomous", "Autonomous.Navigating", "Autonomous.Parking"]
        for item in evidence.surface_candidates
    )
    assert all(
        isinstance(item.domain_obligation, prototype.GraphObligation)
        and item.domain_obligation.property == "event_consumer_reachable"
        and item.domain_obligation.source_ref == item.goal.source
        for item in evidence.surface_candidates
    )
    assert len(outcomes) == 3
    findings = prototype.build_finding_records(outcomes)
    assert len(findings) == 1
    assert all(item["witness_level"] == "W2" for item in findings)
    clusters = prototype.build_report_issue_clusters(findings)
    assert len(clusters) == 1
    assert clusters[0]["facet_count"] == 1


def test_scope_and_descendants_supports_the_exact_root_scope() -> None:
    pair, _ = _pair_and_inspect("0030")
    root = pair["pair_name"]

    covered = prototype._event_scope_ids(
        pair,
        [root],
        "scope_and_descendants",
    )

    assert covered == [
        root,
        "Autonomous",
        "Autonomous.Navigating",
        "Autonomous.Parking",
        "HumanDriving",
    ]


def test_event_scope_certificate_aggregates_exact_consumers_per_covered_scope() -> None:
    pair, _ = _pair_and_inspect("0030")
    goal = prototype.EvidenceGoal(
        relation="event_consumed_in_scope",
        source="Autonomous.Parking",
        observed_transition_id="tr_0003",
        scope_applicability="scope_and_descendants",
        required_scope_ids=[
            "Autonomous",
            "Autonomous.Navigating",
            "Autonomous.Parking",
        ],
        expected=True,
    )

    certificate = prototype._source_event_scope_certificate(pair, goal)

    assert certificate is not None
    assert certificate["event"] == "Park Request"
    assert certificate["source"] == "Autonomous.Parking"
    assert certificate["consumers"] == []
    assert certificate["missing_scope_ids"] == [
        "Autonomous",
        "Autonomous.Parking",
    ]
    assert certificate["coverage_actual"] is False
    assert [item["scope"] for item in certificate["consumers_by_scope"]] == [
        "Autonomous",
        "Autonomous.Navigating",
        "Autonomous.Parking",
    ]
    navigating = certificate["consumers_by_scope"][1]
    assert navigating["active_scopes_checked"] == [
        "Autonomous.Navigating",
        "Autonomous",
    ]
    assert [item["id"] for item in navigating["consumers"]] == ["tr_0003"]
    assert [item["id"] for item in certificate["aggregate_consumers"]] == [
        "tr_0003"
    ]
    assert certificate["verdict"] == "counterexample"


def test_descendant_event_scope_facets_share_one_typed_contract_cause() -> None:
    pair, _ = _pair_and_inspect("0030")
    required = ["Autonomous", "Autonomous.Navigating", "Autonomous.Parking"]
    certificates = [
        prototype._source_event_scope_certificate(
            pair,
            prototype.EvidenceGoal(
                relation="event_consumed_in_scope",
                source=scope,
                observed_transition_id="tr_0003",
                scope_applicability="scope_and_descendants",
                required_scope_ids=required,
            ),
        )
        for scope in ("Autonomous", "Autonomous.Parking")
    ]

    assert all(certificate is not None for certificate in certificates)
    cause_keys = {
        prototype._certificate_cause_key(certificate)
        for certificate in certificates
        if certificate is not None
    }
    assert len(cause_keys) == 1
    assert next(iter(cause_keys)).startswith("source:event_missing_scope_group:")


def test_event_scope_exact_event_identity_is_bound_only_by_transition_id() -> None:
    pair, _ = _pair_and_inspect("0030")

    first = prototype._source_event_scope_certificate(
        pair,
        prototype.EvidenceGoal(
            relation="event_consumed_in_scope",
            source="Autonomous.Navigating",
            observed_transition_id="tr_0003",
            required_scope_ids=["Autonomous.Navigating"],
        ),
    )
    second = prototype._source_event_scope_certificate(
        pair,
        prototype.EvidenceGoal(
            relation="event_consumed_in_scope",
            source="Autonomous.Navigating",
            observed_transition_id="tr_0004",
            required_scope_ids=["Autonomous.Navigating"],
        ),
    )

    assert first is not None and second is not None
    assert first["event"] == "Park Request"
    assert [item["id"] for item in first["consumers"]] == ["tr_0003"]
    assert second["event"] == "Parking Complete"
    assert second["consumers"] == []


def test_event_scope_distinguishes_authored_consumer_from_unreachable_component() -> None:
    pair, inspect = _pair_and_inspect("0046")
    root = pair["pair_name"]
    goal = prototype.EvidenceGoal(
        relation="event_consumed_in_scope",
        source=root,
        observed_transition_id="tr_0003",
        scope_applicability="one_scope",
        required_scope_ids=[root],
        expected=True,
    )
    certificate = prototype._source_event_scope_certificate(pair, goal)

    assert certificate is not None
    assert certificate["kind"] == "source_event_scope_unavailable"
    assert certificate["event"] == "Intercepted"
    assert [item["id"] for item in certificate["aggregate_consumers"]] == [
        "tr_0003"
    ]
    assert certificate["aggregate_consumers"][0]["source_reachable"] is False
    assert certificate["unreachable_scope_ids"] == [root]
    assert certificate["blocking_scope"] == "UAVSwarmStateMachine"

    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The interception response must be executable from the machine entry.",
        claim="The authored interception consumer is trapped in an unreachable region.",
        basis_kind="nl_literal",
        nl_quote="3 When the UAV swarm is intercepted, it transitions to the formation adjustment state.",
        priority=1,
        locations=["NL3", "tr_0003"],
        proposed_l="L2",
        domain_obligation=prototype.GraphObligation(
            property="event_consumer_reachable", source_ref=root, expected=True
        ),
        goal=goal,
    )
    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["execution_certificate"]["terminal"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"


def test_missing_state_path_requires_exact_parent_anchor() -> None:
    pair, _ = _pair_and_inspect("0030")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A required state exists.",
        claim="The required state is absent.",
        observed_fact="No exact state path is present.",
        basis_kind="nl_literal",
        nl_quote="2. The autonomous mode has sub-states.",
        priority=1,
        locations=["NL2"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="state_exists",
            source="HumanDriving",
            subject="Autonomous.RequiredCompletion",
            expected=True,
        ),
    )

    validated, diagnostics = prototype._validate_direct_grounded_candidate(
        pair, candidate, lane="surface_candidates", index=0
    )

    assert diagnostics[0]["class"] == "formal_id_invalid"
    assert validated.goal.subject is None


def test_scope_event_consumption_binds_event_without_overwriting_scope() -> None:
    pair, inspect = _pair_and_inspect("0030")
    candidate = prototype.EvidenceCandidate(
        obligation="The shutdown event must be consumed in every operating mode.",
        claim="The shutdown event is not consumed in one operating mode.",
        basis_kind="nl_literal",
        nl_quote="5 when power off, it will transit to final state",
        priority=1,
        locations=["NL5"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="event_consumed_in_scope",
            source="Autonomous",
            observed_transition_id="tr_0007",
            expected=True,
        ),
    )

    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(
            pair, inspect, prototype.EvidencePlan(candidates=[candidate])
        )
    )

    assert len(findings) == 1
    assert findings[0]["witness_level"] == "W2"
    assert findings[0]["l_level"] == "L0"
    assert findings[0]["source_attribution"] == ["causal_dual_certificate"]
    certificate = findings[0]["source_causality_certificate"]
    assert certificate["kind"] == "source_event_missing_in_scope"
    assert certificate["source"] == "Autonomous"
    assert certificate["observed_transition_id"] == "tr_0007"
    assert certificate["consumers"] == []
    assertion_ir = findings[0]["compiled_assertions"][0]["assertion_ir"]
    assert assertion_ir[1]["predicate"] == "event_consumed"
    assert assertion_ir[1]["bindings"]["source"] == (
        "llms_emp_feedback_final_0030.Autonomous"
    )


def test_existing_final_pseudostate_transition_reaches_d_as_rebutting_fact() -> None:
    pair, inspect = _pair_and_inspect("0030")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A shutdown transition to the root final pseudostate exists.",
        claim="The shutdown transition to the root final pseudostate is absent.",
        observed_fact="The source inventory contains a candidate final edge.",
        basis_kind="nl_literal",
        nl_quote="5 when power off, it will transit to final state",
        priority=1,
        locations=["NL5"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_exists",
            source="HumanDriving",
            target="@final:__root__",
            trigger="Power Off",
            expected=True,
        ),
    )

    validated, diagnostics = prototype._validate_direct_grounded_candidate(
        pair, candidate, lane="surface_candidates", index=0
    )
    outcomes = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[validated])
    )

    assert diagnostics == []
    assert outcomes[0]["probe_groups"][0]["counterexample_found"] is False
    assert outcomes[0]["probe_groups"][0]["execution_certificate"]["verdict"] == (
        "inconclusive"
    )
    findings = prototype.build_finding_records(outcomes)
    assert findings[0]["witness_level"] == "W1"
    d_context = prototype.build_d_context(pair, findings)
    assert '"matching_transitions":[{' in d_context
    assert '"id":"tr_0007"' in d_context
    assert '"target":"@final:__root__"' in d_context


def test_satisfied_explicit_probe_does_not_suppress_scout_counterexample() -> None:
    certificate = {
        "kind": "reachable_deadlock",
        "target": "Root.q_dead",
    }
    progressive = {
        "candidate_index": "P1",
        "candidate": {},
        "nl_anchor_valid": True,
        "probe_groups": [
            {
                "origin": "progressive_deterministic_scout",
                "source_candidate": True,
                "source_causality_certificate": certificate,
            }
        ],
    }
    explicit = {
        "candidate_index": 1,
        "candidate": {},
        "nl_anchor_valid": True,
        "probe_groups": [
            {
                "origin": "method_owned_evidence_compiler",
                "source_candidate": False,
                "counterexample_found": False,
                "source_causality_certificate": certificate,
            }
        ],
    }

    selected = prototype.select_finding_outcomes([progressive, explicit])

    assert progressive in selected
    assert explicit in selected


def test_progressive_scout_builds_source_cut_for_disconnected_submachine() -> None:
    pair, inspect = _pair_and_inspect("0059")

    findings = prototype.build_finding_records(
        prototype.execute_progressive_evidence_seeds(pair, inspect)
    )

    disconnected = next(
        item
        for item in findings
        if item["source_causality_certificate"]
        and item["source_causality_certificate"]["kind"]
        == "unreachable_source_component"
    )
    certificate = disconnected["source_causality_certificate"]
    assert certificate["component"] == "CollisionAvoidanceSystem"
    assert certificate["cross_component_incoming"] == []
    assert disconnected["witness_level"] == "W2"


def test_progressive_source_gate_accepts_complete_concurrency_certificate() -> None:
    pair, inspect = _pair_and_inspect("0023")

    outcomes = prototype.execute_progressive_evidence_seeds(pair, inspect)

    assert outcomes
    assert any(
        group["source_candidate"]
        for outcome in outcomes
        for group in outcome["probe_groups"]
    )
    assert all(
        group["source_causality_certificate"]["kind"]
        == "concurrent_region_deadlock"
        for outcome in outcomes
        for group in outcome["probe_groups"]
        if group["source_causality_certificate"]
    )
    assert all(
        group["source_causality_certificate"]["sound_for_claim"]
        for outcome in outcomes
        for group in outcome["probe_groups"]
        if group["source_causality_certificate"]
    )


def test_d_adjudication_is_per_obligation_facet_and_keeps_w_separate() -> None:
    pair, inspect = _pair_and_inspect("0004")
    findings = prototype.build_finding_records(
        prototype.execute_progressive_evidence_seeds(pair, inspect)
    )
    plan = prototype.DAdjudicationPlan(
        decisions=[
            prototype.DDecision(
                finding_key=finding["finding_key"],
                grounding="impl",
                violated_obligation="A reachable non-final controller state must not deadlock.",
                supporting_facts=[finding["claims"][0]],
                strongest_defeater="The state could be an intended final state.",
                defeater_kind="rebutting",
                defeater_disposition="defeated",
                rationale="The source declares no final marker and the state has no exit.",
                d_subclass="D2-impl",
                d_level="D2",
            )
            for finding in findings
        ]
    )

    adjudicated = prototype.apply_d_adjudication(findings, plan)
    confirmed = prototype.select_confirmed_issues(adjudicated)

    assert len(confirmed) == 2
    assert all(item["witness_level"] == "W2" for item in confirmed)
    assert all(item["d_decision"]["d_level"] == "D2" for item in confirmed)
    assert all(item["d_validation_errors"] == [] for item in confirmed)


def test_d_subclass_is_mechanically_derived_and_d0_may_be_undercut() -> None:
    finding = {
        "finding_key": "synthetic:language-rule",
        "witness_level": "W2",
        "source_causality_certificate": {
            "kind": "initial_contract_violation",
            "verdict": "counterexample",
            "initial_edges": [{"id": "tr_initial", "guard": "c"}],
        },
        "nl_quotes": [],
        "nl_anchor_valid": True,
    }
    d2 = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="lang",
        violated_obligation="An initial edge cannot carry a trigger.",
        strongest_defeater="The label could be presentation-only.",
        defeater_kind="undercutting",
        defeater_disposition="defeated",
        rationale="The source parser records the label as the trigger.",
        d_subclass="not_applicable",
        d_level="D2",
    )
    d0 = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="none",
        violated_obligation="No violated obligation was established.",
        strongest_defeater="The source evidence needed by the claim is absent.",
        defeater_kind="undercutting",
        defeater_disposition="survives",
        rationale="The allegation is not grounded by the supplied source facts.",
        d_subclass="D2-lit",
        d_level="D0",
    )

    normalized_d2 = prototype.normalize_d_decision(d2)
    normalized_d0 = prototype.normalize_d_decision(d0)

    assert normalized_d2.d_subclass == "D2-lit"
    assert prototype.validate_d_decision(finding, normalized_d2) == []
    assert normalized_d0.d_subclass == "not_applicable"
    assert prototype.validate_d_decision(finding, normalized_d0) == []


def test_exact_nl_quote_can_ground_d2_independent_of_candidate_basis_tag() -> None:
    finding = {
        "finding_key": "synthetic:reachable-deadlock",
        "basis_kind": "domain_norm",
        "witness_level": "W2",
        "nl_quotes": ["execution proceeds to q_choice"],
        "nl_anchor_valid": True,
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "verdict": "counterexample",
            "explicit_final": False,
        },
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="lit",
        violated_obligation="The state must continue.",
        strongest_defeater="No literal continuation obligation is stated.",
        defeater_kind="undercutting",
        defeater_disposition="defeated",
        rationale="The state is reachable and deadlocked.",
        d_subclass="D2-lit",
        d_level="D2",
    )

    assert prototype.validate_d_decision(finding, decision) == []


def test_reachable_deadlock_d2_is_formally_normalized_to_impl_without_reading_text() -> (
    None
):
    finding = {
        "finding_key": "synthetic:reachable-deadlock",
        "basis_kind": "nl_literal",
        "witness_level": "W2",
        "nl_quotes": ["execution proceeds to q_choice"],
        "nl_anchor_valid": True,
        "claims": ["Arbitrary prose that must not control the taxonomy."],
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "verdict": "counterexample",
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="lit",
        violated_obligation="The reachable non-final state must not deadlock.",
        strongest_defeater="The state could be intended as terminal.",
        defeater_kind="rebutting",
        defeater_disposition="defeated",
        rationale="The typed certificate excludes explicit finality and concurrency.",
        d_subclass="D2-lit",
        d_level="D2",
    )

    normalized = prototype.normalize_d_decision(decision, finding=finding)

    assert normalized.grounding == "impl"
    assert normalized.d_subclass == "D2-impl"
    assert normalized.violated_obligation == decision.violated_obligation
    assert prototype.validate_d_decision(finding, normalized) == []


def test_w2_dead_end_can_retain_typed_operational_d2_norm() -> None:
    finding = {
        "finding_key": "synthetic:operational-dead-end",
        "basis_kind": "domain_norm",
        "witness_level": "W2",
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "target": "Root.q_dead",
            "verdict": "counterexample",
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
        "domain_obligations": [
            {
                "family": "graph",
                "property": "escapable",
                "target_ref": "Root.q_dead",
                "expected": True,
            }
        ],
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="dom",
        violated_obligation="The operational state must admit continuation.",
        strongest_defeater="The dead-end may be an intended final state.",
        defeater_kind="rebutting",
        defeater_disposition="defeated",
        rationale="The typed operational obligation targets the reachable non-final state.",
        d_subclass="not_applicable",
        d_level="D2",
    )

    normalized = prototype.normalize_d_decision(decision, finding=finding)

    assert normalized.grounding == "dom"
    assert normalized.d_subclass == "D2-norm"
    assert prototype.validate_d_decision(finding, normalized) == []


def test_d2_norm_rejects_untyped_operational_prose() -> None:
    finding = {
        "finding_key": "synthetic:untyped-operational-dead-end",
        "witness_level": "W2",
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "target": "Root.q_dead",
            "verdict": "counterexample",
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="dom",
        violated_obligation="The operational state must admit continuation.",
        strongest_defeater="The dead-end may be an intended final state.",
        defeater_kind="rebutting",
        defeater_disposition="defeated",
        rationale="Free-text prose is not a typed domain obligation.",
        d_subclass="D2-norm",
        d_level="D2",
    )

    errors = prototype.validate_d_decision(finding, decision)

    assert "D2-norm requires a typed operational domain obligation" in errors


def test_d2_impl_is_closed_to_source_grounded_reachable_nonfinal_deadlock() -> None:
    finding = {
        "finding_key": "synthetic:unreachable-state",
        "basis_kind": "implicit_oracle",
        "witness_level": "W2",
        "nl_quotes": [],
        "nl_anchor_valid": False,
        "source_causality_certificate": {
            "kind": "unreachable_source_component",
            "verdict": "counterexample",
        },
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="impl",
        violated_obligation="The component must be reachable.",
        strongest_defeater="The component may be intentionally dormant.",
        defeater_kind="undercutting",
        defeater_disposition="defeated",
        rationale="The component is unreachable.",
        d_subclass="D2-impl",
        d_level="D2",
    )

    errors = prototype.validate_d_decision(finding, decision)

    assert any("protocol_d2_grounding is null" in error for error in errors)


def test_d1_requires_a_grounded_first_reading() -> None:
    finding = {
        "finding_key": "synthetic:ungrounded-ambiguity",
        "witness_level": "W1",
        "source_causality_certificate": None,
        "nl_quotes": [],
        "nl_anchor_valid": True,
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="none",
        violated_obligation="No violated obligation was established.",
        strongest_defeater="The alleged structure has not been established.",
        defeater_kind="undercutting",
        defeater_disposition="survives",
        rationale="Missing evidence is not a content-level second reading.",
        d_subclass="not_applicable",
        d_level="D1",
    )

    assert prototype.validate_d_decision(finding, decision) == [
        "D1 requires a grounded first reading"
    ]


def test_d0_accepts_a_surviving_undercutter_without_a_source_certificate() -> None:
    finding = {
        "finding_key": "synthetic:null-certificate-deadlock",
        "witness_level": "W1",
        "source_causality_certificate": None,
        "nl_quotes": [],
        "nl_anchor_valid": False,
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="none",
        violated_obligation="No violated obligation was established.",
        strongest_defeater="The required source deadlock premise is absent.",
        defeater_kind="undercutting",
        defeater_disposition="survives",
        rationale="A null source certificate leaves the implicit premise ungrounded.",
        d_subclass="not_applicable",
        d_level="D0",
    )

    assert prototype.validate_d_decision(finding, decision) == []


def test_d0_rejects_a_defeated_defeater() -> None:
    finding = {
        "finding_key": "synthetic:rebutted-claim",
        "witness_level": "W1",
        "source_causality_certificate": None,
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="none",
        violated_obligation="No violated obligation was established.",
        strongest_defeater="The alleged obligation is absent.",
        defeater_kind="undercutting",
        defeater_disposition="defeated",
        rationale="A defeated defeater cannot support D0 under the protocol.",
        d_subclass="not_applicable",
        d_level="D0",
    )

    assert prototype.validate_d_decision(finding, decision) == [
        "D0 requires a surviving or unresolved defeater"
    ]


def test_d0_rebuttal_disposition_describes_the_surviving_defeater() -> None:
    finding = {
        "finding_key": "synthetic:rebutted-by-source",
        "witness_level": "W1",
        "source_causality_certificate": None,
    }
    surviving = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="none",
        violated_obligation="No violated obligation remains.",
        strongest_defeater="The exact source already realizes the required edge.",
        defeater_kind="rebutting",
        defeater_disposition="survives",
        rationale="The rebuttal remains compatible with every supplied fact.",
        d_subclass="not_applicable",
        d_level="D0",
    )
    unresolved = surviving.model_copy(
        update={"defeater_disposition": "unresolved"}
    )

    assert prototype.validate_d_decision(finding, surviving) == []
    assert prototype.validate_d_decision(finding, unresolved) == [
        "D0 rebutting defeater must survive"
    ]


def test_d2_rejects_a_surviving_defeater() -> None:
    finding = {
        "finding_key": "synthetic:literal-with-surviving-defeater",
        "witness_level": "W2",
        "nl_quotes": ["The controller enters q_target."],
        "nl_anchor_valid": True,
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="lit",
        violated_obligation="The controller must enter q_target.",
        strongest_defeater="The clause may describe an optional route.",
        defeater_kind="undercutting",
        defeater_disposition="survives",
        rationale="The alternative reading remains compatible with the source.",
        d_subclass="D2-lit",
        d_level="D2",
    )

    assert prototype.validate_d_decision(finding, decision) == [
        "D2 requires the strongest defeater to be defeated"
    ]


def test_closed_d2_impl_accepts_a_defeated_defeater() -> None:
    finding = {
        "finding_key": "synthetic:closed-reachable-deadlock",
        "witness_level": "W2",
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "verdict": "counterexample",
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
    }
    decision = prototype.DDecision(
        finding_key=finding["finding_key"],
        grounding="impl",
        violated_obligation="A reachable non-final state must not deadlock.",
        strongest_defeater="The state could be intentionally final.",
        defeater_kind="rebutting",
        defeater_disposition="defeated",
        rationale="The closed certificate establishes non-finality and no continuation.",
        d_subclass="D2-impl",
        d_level="D2",
    )

    assert prototype.validate_d_decision(finding, decision) == []


def test_same_nl_anchor_and_semantic_binding_deduplicate_paraphrases() -> None:
    group = {
        "group_id": "compiled_goal",
        "claim": "The edge lacks its condition.",
        "source_causality_certificate": {
            "kind": "source_guard_presence",
            "source": "Root.A",
            "target": "Root.B",
        },
    }
    first = {
        "candidate_index": 1,
        "candidate": {
            "obligation": "A to B must carry condition c.",
            "basis_kind": "nl_literal",
            "nl_quote": "A enters B when c.",
            "locations": ["NL3"],
            "goal": {
                "relation": "guard_present",
                "source": "Root.A",
                "target": "Root.B",
                "condition": "c",
                "expected": True,
            },
        },
    }
    second = {
        "candidate_index": 2,
        "candidate": {
            "obligation": "The B branch from A is conditional.",
            "basis_kind": "nl_literal",
            "nl_quote": "when c",
            "locations": ["NL3", "PUML:L8"],
            "goal": {
                "relation": "guard_present",
                "source": "Root.A",
                "target": "Root.B",
                "condition": "c",
                "expected": True,
            },
        },
    }

    assert prototype._finding_key(first, group) == prototype._finding_key(second, group)


def test_evidence_goal_compiler_owns_backend_and_predicate_selection() -> None:
    goal = prototype.EvidenceGoal(
        relation="event_reaches_target",
        source="Root.Ready",
        trigger="Root.go",
        target="Root.Done",
    )

    route = prototype.compile_evidence_goal(goal)

    assert route["backend"] == "T_fcstm_trace"
    assert route["operation"] == "predicate_bundle"
    assert [check.kind for check in route["checks"]] == [
        "reaches",
        "occupancy_after",
    ]
    assert "backend" not in goal.model_dump()


def test_containment_goal_uses_subject_as_child_and_gets_dual_w2() -> None:
    pair, inspect = _pair_and_inspect("0016")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The three search regions are sibling children of SearchMission.",
        claim="Region2 is nested under Region1 instead of SearchMission.",
        basis_kind="nl_literal",
        nl_quote="three different state areas",
        priority=5,
        locations=["PUML:L12"],
        proposed_l="L1",
        observed_fact="Region2 is nested below Region1.",
        goal=prototype.EvidenceGoal(
            relation="contained_in",
            subject="SearchMission.Region1.Region2",
            target="SearchMission",
        ),
    )

    route = prototype.compile_evidence_goal(candidate.goal)
    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    group = outcome["probe_groups"][0]

    assert route["errors"] == []
    assert route["checks"][0].bindings == {
        "parent": "SearchMission",
        "child": "SearchMission.Region1.Region2",
    }
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert (
        group["source_causality_certificate"]["kind"] == "source_containment_contract"
    )
    assert group["source_causality_certificate"]["actual_parent"].endswith("Region1")


def test_child_count_goal_gets_exact_source_dual_w2() -> None:
    pair, inspect = _pair_and_inspect("0046")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="SearchRegion must contain exactly three grounded operating areas.",
        claim="SearchRegion has four direct authored children rather than three.",
        basis_kind="nl_literal",
        nl_quote="operates within three different state areas",
        priority=4,
        locations=["NL2", "PUML:L3"],
        proposed_l="L1",
        observed_fact="The exact source AST has four direct children in SearchRegion.",
        goal=prototype.EvidenceGoal(
            relation="child_count",
            subject="UAVSwarmStateMachine.SearchRegion",
            count=3,
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    group = outcome["probe_groups"][0]
    finding = prototype.build_finding_records([outcome])[0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert group["source_causality_certificate"]["kind"] == (
        "source_child_count_contract"
    )
    assert group["source_causality_certificate"]["direct_children"] == [
        "UAVSwarmStateMachine.SearchRegion.Attacking",
        "UAVSwarmStateMachine.SearchRegion.FormationAdjustment",
        "UAVSwarmStateMachine.SearchRegion.Idle",
        "UAVSwarmStateMachine.SearchRegion.Searching",
    ]
    assert group["source_causality_certificate"]["actual_count"] == 4
    receipt = group["execution_certificate"]["semantic_binding_receipt"]
    assert receipt["authority"] == "formal_source_ast"
    assert receipt["formal_reference_policy"] == ("exact_id_or_declared_mapping_only")
    assert receipt["scope"] == "formal_fact_only"
    assert receipt["semantic_decision_claimed"] is False
    assert receipt["semantic_provenance"] is None
    assert finding["l_level"] == "L1"


def test_invalid_initial_target_gets_source_scope_certificate() -> None:
    pair, inspect = _pair_and_inspect("0016")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A composite initial edge must target a child in the same scope.",
        claim="Region2 points its initial edge to a Search state outside Region2.",
        basis_kind="domain_norm",
        priority=5,
        locations=["PUML:L13"],
        proposed_l="L1",
        observed_fact="Search belongs to Region1 rather than Region2.",
        goal=prototype.EvidenceGoal(
            relation="initial_target",
            subject="SearchMission.Region1.Region2",
            target="SearchMission.Region1.Search",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    group = outcome["probe_groups"][0]
    finding = prototype.build_finding_records([outcome])[0]
    d_context = prototype.build_d_context(pair, [finding])

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert (
        group["source_causality_certificate"]["kind"]
        == "source_initial_target_contract"
    )
    assert group["source_causality_certificate"]["target_is_direct_child"] is False
    assert finding["l_level"] == "L1"
    assert "UML_INITIAL_TARGET_SAME_REGION" in d_context


def test_self_targeted_initial_edge_is_a_sound_source_counterexample() -> None:
    pair, _ = _pair_and_inspect("0004")

    certificate = prototype._source_initial_target_certificate(
        pair, "DoorsClosing", "DoorsClosing"
    )

    assert certificate is not None
    assert certificate["direct_children"] == []
    assert certificate["initial_edges"][0]["target"] == "DoorsClosing"
    assert certificate["scope_supports_initial"] is True
    assert certificate["target_is_direct_child"] is False
    assert certificate["sound_for_claim"] is True
    assert certificate["verdict"] == "counterexample"


def test_d_context_exposes_only_typed_duplicate_targets() -> None:
    pair, _ = _pair_and_inspect("0004")
    certificate = {
        "kind": "reachable_deadlock",
        "target": "Root.q_dead",
        "verdict": "counterexample",
        "explicit_final": False,
        "assumptions": {"no_concurrent_regions": True},
    }
    goal = {"relation": "state_exists", "subject": "Root.q_dead", "expected": True}
    earlier = {
        "finding_key": "source:deadlock:facet:a",
        "witness_level": "W2",
        "formal_goals": [goal],
        "source_causality_certificate": certificate,
    }
    matching = {
        "finding_key": "hypothesis:deadlock:facet:b",
        "witness_level": "W1",
        "formal_goals": [goal],
        "source_causality_certificate": certificate,
    }
    missing_proof = {
        "finding_key": "hypothesis:unproved:facet:c",
        "witness_level": "W1",
        "formal_goals": [],
        "source_causality_certificate": None,
    }

    context = prototype.build_d_context(pair, [earlier, matching, missing_proof])
    payload = context.split("# Findings to adjudicate\n\n", 1)[1]
    findings = json.loads(payload)
    by_key = {item["finding_key"]: item for item in findings}

    assert by_key["hypothesis:deadlock:facet:b"][
        "duplicate_eligible_earlier_keys"
    ] == ["source:deadlock:facet:a"]
    assert by_key["hypothesis:unproved:facet:c"][
        "duplicate_eligible_earlier_keys"
    ] == []


def _synthetic_d_pair() -> dict:
    return {
        "nl": "The controller enters q_dead.",
        "canonical": {
            "model": {
                "name": "Root",
                "states": [],
                "transitions": [],
                "concurrent_regions": [],
            }
        },
    }


def _d_dossiers(context: str) -> list[dict]:
    payload = context.split("# Findings to adjudicate\n\n", 1)[1]
    return json.loads(payload)


def test_d_context_has_uniform_auditable_slots_without_ledger_inputs() -> None:
    literal = {
        "finding_key": "synthetic:literal:facet:a",
        "basis_kind": "nl_literal",
        "bases": ["The exact requirement and source fact concern q_dead."],
        "claims": ["q_dead is deadlocked."],
        "obligations": ["The controller must enter and continue from q_dead."],
        "nl_quotes": ["The controller enters q_dead."],
        "nl_anchor_valid": True,
        "witness_level": "W2",
        "source_attribution": ["causal_dual_certificate"],
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "target": "Root.q_dead",
            "verdict": "counterexample",
            "sound_for_claim": True,
            "reachable": True,
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
    }
    sparse = {
        "finding_key": "synthetic:sparse:facet:b",
        "basis_kind": "implicit_oracle",
        "claims": ["A hypothesis without a typed formal fact."],
        "obligations": [],
        "nl_quotes": [],
        "nl_anchor_valid": False,
        "witness_level": "W0",
        "source_attribution": ["unattributed"],
        "source_causality_certificate": None,
    }

    by_key = {
        item["finding_key"]: item
        for item in _d_dossiers(
            prototype.build_d_context(_synthetic_d_pair(), [literal, sparse])
        )
    }
    required_slots = {
        "normative_basis",
        "applicability_reason",
        "formal_fact",
        "source_certificate",
        "strongest_defeater",
        "defeater_disposition",
        "alternative_reading",
        "mechanical_d_provenance_ceiling",
    }

    assert required_slots <= by_key[literal["finding_key"]].keys()
    assert required_slots <= by_key[sparse["finding_key"]].keys()
    assert by_key[literal["finding_key"]]["normative_basis"] == {
        "basis_kind": "nl_literal",
        "domain_obligations": [],
        "language_clause": None,
        "nl_anchor_valid": True,
        "nl_quote": "The controller enters q_dead.",
        "obligation": "The controller must enter and continue from q_dead.",
    }
    assert by_key[literal["finding_key"]]["formal_fact"] == {
        "canonical_source_fact": (
            "Source state 'Root.q_dead' is reachable, non-final, and has no "
            "enabled continuation in the certified fragment."
        ),
        "formal_oracle_facts": [],
    }
    assert by_key[literal["finding_key"]][
        "mechanical_d_provenance_ceiling"
    ] == {
        "admissible_d2_groundings": ["lit", "impl"],
        "level": "D2",
        "semantic_d_decision_claimed": False,
    }
    assert by_key[sparse["finding_key"]]["applicability_reason"] is None
    assert by_key[sparse["finding_key"]]["formal_fact"] is None
    assert by_key[sparse["finding_key"]]["source_certificate"] is None
    assert by_key[sparse["finding_key"]]["strongest_defeater"] is None
    assert by_key[sparse["finding_key"]]["defeater_disposition"] is None
    assert by_key[sparse["finding_key"]]["alternative_reading"] is None
    assert "recommended_d_level" not in by_key[sparse["finding_key"]]


def test_d_mechanical_ceiling_does_not_interpret_finding_prose() -> None:
    finding = {
        "finding_key": "synthetic:prose-a:facet:a",
        "basis_kind": "implicit_oracle",
        "bases": ["First arbitrary applicability explanation."],
        "claims": ["First arbitrary claim."],
        "obligations": ["First arbitrary obligation."],
        "nl_quotes": [],
        "nl_anchor_valid": False,
        "witness_level": "W2",
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "target": "Root.q_dead",
            "verdict": "counterexample",
            "explicit_final": False,
            "assumptions": {"no_concurrent_regions": True},
        },
    }
    paraphrased = copy.deepcopy(finding)
    paraphrased.update(
        {
            "finding_key": "synthetic:prose-b:facet:b",
            "bases": ["Unrelated rewritten audit prose."],
            "claims": ["Unrelated rewritten claim."],
            "obligations": ["Unrelated rewritten obligation."],
        }
    )

    dossiers = _d_dossiers(
        prototype.build_d_context(_synthetic_d_pair(), [finding, paraphrased])
    )

    assert dossiers[0]["mechanical_d_provenance_ceiling"] == dossiers[1][
        "mechanical_d_provenance_ceiling"
    ]
    assert dossiers[0]["formal_fact"] == dossiers[1]["formal_fact"]
    assert dossiers[0]["source_certificate"] == dossiers[1]["source_certificate"]


def test_d_context_exposes_unattributed_artifact_boundary() -> None:
    pair, _ = _pair_and_inspect("0046")
    finding = {
        "finding_key": "hypothesis:artifact-only:facet:a",
        "basis_kind": "implicit_oracle",
        "nl_anchor_valid": False,
        "claims": ["A generated helper is a reachable deadlock."],
        "obligations": ["The author source must not deadlock."],
        "nl_quotes": [],
        "locations": ["FCSTM:F1"],
        "evidence_status": "executed_counterexample",
        "coverage_gap_reasons": [],
        "counterexample_found": True,
        "source_attribution": ["unattributed"],
        "execution_certificates": [
            {
                "verdict": "counterexample",
                "terminal": True,
                "engine": {"adapter": "pyfcstm"},
            }
        ],
        "source_causality_certificate": None,
    }

    context = prototype.build_d_context(pair, [finding])

    assert '"source_attribution":["unattributed"]' in context
    assert '"source_certificate":null' in context


def test_d_context_preserves_formal_non_final_deadlock_fact() -> None:
    pair, _ = _pair_and_inspect("0004")
    finding = {
        "finding_key": "source:reachable_deadlock:Root.Stop:facet:a",
        "basis_kind": "implicit_oracle",
        "nl_anchor_valid": False,
        "claims": ["Root.Stop is a reachable deadlock."],
        "obligations": ["Reachable non-final states must admit continuation."],
        "nl_quotes": [],
        "locations": ["PUML:L1"],
        "evidence_status": "executed_counterexample",
        "coverage_gap_reasons": [],
        "counterexample_found": True,
        "source_attribution": ["causal_dual_certificate"],
        "execution_certificates": [],
        "source_causality_certificate": {
            "kind": "reachable_deadlock",
            "verdict": "counterexample",
            "sound_for_claim": True,
            "target": "Root.Stop",
            "reachable": True,
            "explicit_final": False,
            "outgoing": [],
        },
    }

    context = prototype.build_d_context(pair, [finding])

    assert '"explicit_final":false' in context
    assert '"reachable":true' in context


def test_missing_initial_edge_is_l0_but_still_has_dual_w2() -> None:
    pair, inspect = _pair_and_inspect("0046")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The composite must have an initial edge.",
        claim="UAVSwarmStateMachine has no initial edge to SearchRegion.",
        basis_kind="domain_norm",
        priority=5,
        locations=["PUML:L2"],
        proposed_l="L0",
        observed_fact="The composite has children but no source initial transition.",
        goal=prototype.EvidenceGoal(
            relation="initial_target",
            subject="UAVSwarmStateMachine",
            target="UAVSwarmStateMachine.SearchRegion",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    finding = prototype.build_finding_records([outcome])[0]

    assert finding["witness_level"] == "W2"
    assert finding["source_causality_certificate"]["matching_edge_count"] == 0
    assert finding["l_level"] == "L0"


def test_artifact_static_absence_without_source_certificate_is_unattributed() -> None:
    pair, inspect = _pair_and_inspect("0016")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A source-level data carrier must survive conversion.",
        claim="The converted FCSTM lacks the expected variable.",
        basis_kind="nl_literal",
        nl_quote="the number of UAVs in the swarm decreases accordingly",
        priority=3,
        locations=["F1"],
        proposed_l="L0",
        observed_fact="The converted variable inventory has no uav_count.",
        goal=prototype.EvidenceGoal(
            relation="variable_exists",
            variable="uav_count",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_causality_certificate"] is None
    assert group["source_attribution"]["status"] == "unattributed"
    assert group["source_candidate"] is False


def test_llm_selected_event_transition_is_formally_bound_and_unreachability_is_w2() -> (
    None
):
    pair, inspect = _pair_and_inspect("0046")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="An interception event must reach formation adjustment.",
        claim="Intercepted cannot be consumed because its sole source is unreachable.",
        basis_kind="nl_literal",
        nl_quote="When the UAV swarm is intercepted, it transitions to the formation adjustment state.",
        priority=5,
        locations=["F18"],
        proposed_l="L2",
        observed_fact="The only Intercepted consumer is Searching, which is unreachable.",
        goal=prototype.EvidenceGoal(
            relation="event_reaches_target",
            observed_transition_id="tr_0003",
            target="UAVSwarmStateMachine.SearchRegion.FormationAdjustment",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[], behavior_candidates=[candidate]
        ),
    )[0]
    group = outcome["probe_groups"][0]

    assert outcome["candidate"]["goal"]["source"].endswith("SearchRegion.Searching")
    assert group["compiler_route"]["method_bindings"] == [
        {
            "field": "source",
            "value": "UAVSwarmStateMachine.SearchRegion.Searching",
            "basis": "llm_selected_observed_transition_then_exact_ast_read",
        },
        {
            "field": "trigger",
            "value": "llms_emp_feedback_final_0046.Intercepted",
            "basis": "llm_selected_transition_id_then_declared_event_mapping",
        },
    ]
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["execution_certificate"]["observations"]["source_reachable"] is False
    assert (
        group["execution_certificate"]["observations"]["event_trace_executed"] is False
    )
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert (
        group["source_causality_certificate"]["kind"]
        == "missing_initial_with_compiler_consequence"
    )


def test_event_binding_preserves_llm_leaf_target_below_transition_composite() -> None:
    pair, inspect = _pair_and_inspect("0016")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Interception must enter the active formation-adjustment leaf.",
        claim="Interception does not enter FormationAdjust.AdjustingFormation.",
        basis_kind="nl_literal",
        nl_quote="When the UAV swarm is intercepted, it transitions to the formation adjustment state",
        priority=5,
        locations=["NL3"],
        proposed_l="L2",
        observed_fact="The source transition targets a composite whose initial descendant is the required leaf.",
        goal=prototype.EvidenceGoal(
            relation="event_reaches_target",
            observed_transition_id="tr_0009",
            target="FormationAdjust.AdjustingFormation",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[], behavior_candidates=[candidate]
        ),
    )[0]
    group = outcome["probe_groups"][0]

    assert (
        outcome["candidate"]["goal"]["target"] == "FormationAdjust.AdjustingFormation"
    )
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    assert group["execution_certificate"]["verdict"] == "satisfied"
    assert (
        group["execution_certificate"]["observations"][-1]["terminal_result"] == "true"
    )


def test_nl_event_words_without_formal_transition_binding_remain_w1() -> None:
    pair, inspect = _pair_and_inspect("0046")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="An interception event must reach formation adjustment.",
        claim="The event source is not formally grounded.",
        basis_kind="nl_literal",
        nl_quote="When the UAV swarm is intercepted, it transitions to the formation adjustment state.",
        priority=5,
        locations=["NL3"],
        proposed_l="L2",
        observed_fact="The NL concepts have not been bound to a formal transition ID.",
        goal=prototype.EvidenceGoal(
            relation="event_reaches_target",
            trigger="Intercepted",
            target="FormationAdjustment",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[], behavior_candidates=[candidate]
        ),
    )[0]

    assert outcome["probe_groups"][0]["witness_level"] == "W1"
    assert outcome["probe_groups"][0]["counterexample_found"] is False
    assert outcome["probe_groups"][0]["execution_certificate"] is None


def test_initial_contract_d_context_supplies_generic_language_clause() -> None:
    pair, inspect = _pair_and_inspect("0016")
    findings = prototype.build_finding_records(
        prototype.execute_progressive_evidence_seeds(pair, inspect)
    )
    initial = next(
        finding
        for finding in findings
        if finding["source_causality_certificate"]
        and finding["source_causality_certificate"]["kind"]
        == "initial_contract_violation"
    )

    context = prototype.build_d_context(pair, [initial])

    assert "UML_INITIAL_NO_TRIGGER_OR_GUARD" in context
    assert "must not have a trigger or guard" in context


def test_d_context_includes_exact_local_alternative_edges_without_text_matching() -> (
    None
):
    pair, _ = _pair_and_inspect("0029")
    finding = {
        "finding_key": "source:transition:test:facet:a",
        "basis_kind": "nl_literal",
        "bases": ["The source edge contradicts the explicit transition obligation."],
        "claims": ["One exact transition is absent."],
        "obligations": ["One exact transition is required."],
        "nl_quotes": [pair["nl"].splitlines()[3]],
        "source_attribution": ["causal_dual_certificate"],
        "evidence_status": "executed_counterexample",
        "formal_oracle_rules": [],
        "source_causality_certificate": {
            "kind": "source_transition_contract",
            "source": "HighwayMode.lane_change",
            "target": "HighwayMode.FinishState",
            "verdict": "counterexample",
        },
    }

    context = prototype.build_d_context(pair, [finding])

    assert '"id":"tr_0011"' in context
    assert '"target":"HighwayMode.exit_hwy"' in context
    assert "# Exact source state inventory" in context
    assert "The source edge contradicts the explicit transition obligation." in context


def test_d_context_exposes_typed_parent_entry_and_concurrency_facts() -> None:
    pair, _ = _pair_and_inspect("0053")

    context = prototype.build_d_context(pair, [])

    assert "# Typed source entry semantics" in context
    assert '"declared_concurrent_regions":[]' in context
    assert '"scope":"PumpControl","scope_initial_transition_ids":[]' in context
    assert '"PumpControl.PumpRegion":["tr_0002"]' in context


def test_compiler_owns_template_selection() -> None:
    goal = prototype.EvidenceGoal(
        relation="target_reachable",
        target="Root.Target",
    )

    route = prototype.compile_evidence_goal(goal)

    assert route["template"] == "T09_reachability_certificate"
    assert route["backend"] == "G_topology_proof"
    assert route["ignored_template_hint"] is None

    goal_schema = prototype.DiscoveryGroundingPlan.model_json_schema()["$defs"][
        "EvidenceGoal"
    ]
    assert "template" not in goal_schema["properties"]


def test_runtime_prompts_define_w_and_d_without_development_case_leakage() -> None:
    prompts = "\n".join(
        [
            prototype.CONTRACT_SYSTEM_PROMPT,
            prototype.DISCOVERY_GROUNDING_SYSTEM_PROMPT,
            *(prompt for _, prompt in prototype.DISCOVERY_GROUNDING_AUDIT_LENSES),
            prototype.EVIDENCE_SYSTEM_PROMPT,
            prototype.SEMANTIC_GROUNDING_SYSTEM_PROMPT,
            prototype.D_SYSTEM_PROMPT,
        ]
    )

    assert "W2 means" in prompts
    assert "D2 means" in prompts
    assert "`basis`" in prompts
    assert "q0" in prompts and "evt_a" in prompts
    assert re.search(r"\b00[0-9]{2}\b", prompts) is None
    for development_identifier in (
        "enter_hwy",
        "CollisionAvoidanceSystem",
        "FinishState",
        "UrbanMode",
    ):
        assert development_identifier not in prompts


def test_prompt_facing_schemas_are_documented_without_experiment_leakage() -> None:
    schemas = (
        prototype.ContractExtractionPlan,
        prototype.DiscoveryGroundingPlan,
        prototype.DAdjudicationPlan,
    )
    forbidden = (
        "baseline",
        "ledger",
        "x1v2",
        "v26",
        "0029",
        "0053",
        "collisionavoidancesystem",
        "urbanmode",
    )

    for model in schemas:
        schema = model.model_json_schema()
        documented_models = [(model.__name__, schema), *schema.get("$defs", {}).items()]
        for model_name, model_schema in documented_models:
            if "properties" not in model_schema:
                continue
            assert model_schema.get("description"), model_name
            for field_name, field_schema in model_schema["properties"].items():
                assert field_schema.get("description"), f"{model_name}.{field_name}"

        serialized = json.dumps(schema, ensure_ascii=False).lower()
        for forbidden_text in forbidden:
            assert forbidden_text not in serialized


def test_w2_requires_a_real_terminal_execution_certificate() -> None:
    invalid = {
        "witness_level": "W2",
        "execution_certificates": [
            {
                "terminal": False,
                "verdict": "inconclusive",
                "counterexample_found": False,
            }
        ],
    }

    assert prototype.validate_witness_record(invalid)


def test_probe_candidate_preserves_all_structured_evidence_locations() -> None:
    candidate = prototype.ProbeCandidate(
        claim="A formal goal has five independently useful evidence references.",
        basis_kind="implicit_oracle",
        priority=1,
        locations=["R1", "R2", "R3", "R4", "R5"],
    )

    assert candidate.locations == ["R1", "R2", "R3", "R4", "R5"]


def test_evidence_execution_degrades_one_candidate_without_dropping_peers(
    monkeypatch,
) -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidates = [
        prototype.BalancedEvidenceCandidate(
            obligation="The first target must be reachable.",
            claim="The first target is unreachable.",
            basis_kind="implicit_oracle",
            priority=1,
            locations=["R1"],
            proposed_l="L2",
            observed_fact="The formal reachability frontier motivates this goal.",
            goal=prototype.EvidenceGoal(
                relation="target_reachable",
                target="InitialState",
            ),
        ),
        prototype.BalancedEvidenceCandidate(
            obligation="The second target must be reachable.",
            claim="The second target is unreachable.",
            basis_kind="implicit_oracle",
            priority=1,
            locations=["R2"],
            proposed_l="L2",
            observed_fact="The formal reachability frontier motivates this goal.",
            goal=prototype.EvidenceGoal(
                relation="target_reachable",
                target="HighwayMode.enter_hwy",
            ),
        ),
    ]
    original = prototype._execute_evidence_candidate

    def fail_first(pair_arg, inspect_arg, candidate_arg, *, index):
        if index == 1:
            raise RuntimeError("synthetic candidate failure")
        return original(pair_arg, inspect_arg, candidate_arg, index=index)

    monkeypatch.setattr(prototype, "_execute_evidence_candidate", fail_first)

    outcomes = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[], behavior_candidates=candidates
        ),
    )

    assert len(outcomes) == 2
    assert "synthetic candidate failure" in outcomes[0]["candidate_contract_warning"]
    assert outcomes[1]["candidate_index"] == 2


def test_w2_requires_a_semantic_binding_receipt() -> None:
    invalid = {
        "witness_level": "W2",
        "execution_certificates": [
            {
                "terminal": True,
                "verdict": "counterexample",
                "counterexample_found": True,
                "evaluated_artifact_sha256": "artifact-hash",
                "compiled_assertion_sha256": "assertion-hash",
            }
        ],
    }

    errors = prototype.validate_witness_record(invalid)

    assert errors
    assert "semantic-binding receipt" in errors[0]


def test_llm_semantic_receipt_binds_to_the_actual_call_and_plan_hash_chain() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected authored completion edge must be absent.",
        claim="The selected completion edge is extraneous.",
        observed_fact="The exact selected transition exists in the source model.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=1,
        locations=["NL6", "tr_0025"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_absent",
            observed_transition_id="tr_0025",
        ),
    )
    semantic_plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[candidate],
        behavior_candidates=[],
    )
    grounded_contract = prototype.GroundedContractPlan()
    grounded_evidence = prototype.IssueDiscoveryPlan(
        surface_candidates=[candidate], behavior_candidates=[]
    )
    observation = {
        "llm_call_id": "call-grounding-1",
        "role": "paper1_discovery_grounding",
        "profile": "test-profile",
        "provider": "test-provider",
        "configured_model": "test-model",
        "observed_model": "test-model-2026",
        "status": "completed",
        "structured_schema_sha256": "schema-hash-1",
        "schema_contract_repeated_in_prompt": False,
        "system_prompt": "semantic grounding prompt",
        "user_prompt": "numbered NL and formal inventory",
        "raw_response": {"tool_call": "raw"},
        "parsed_output": semantic_plan.model_dump(mode="json"),
    }
    provenance = prototype.build_llm_binding_provenance(
        [observation],
        role="paper1_discovery_grounding",
        semantic_plan=semantic_plan,
        grounded_contract_plan=grounded_contract,
        grounded_evidence_plan=grounded_evidence,
        replayed=False,
    )

    assert provenance is not None
    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        grounded_evidence,
        binding_authority="paper1_discovery_grounding_llm",
        semantic_provenance=provenance,
    )[0]
    finding = prototype.build_finding_records([outcome])[0]
    receipt = finding["execution_certificates"][0]["semantic_binding_receipt"]

    assert finding["witness_level"] == "W2"
    assert receipt["schema"] == "paper1.semantic_binding_receipt.v2"
    assert receipt["semantic_provenance"]["llm_call_id"] == "call-grounding-1"
    assert (
        receipt["semantic_provenance"]["parsed_output_sha256"]
        == (receipt["semantic_provenance"]["semantic_plan_sha256"])
    )
    assert prototype.validate_witness_record(finding) == []
    run_record = {
        "replay_plans_from": None,
        "discovery_grounding_plan": semantic_plan.model_dump(mode="json"),
        "grounded_contract_plan": grounded_contract.model_dump(mode="json"),
        "grounded_evidence_plan": grounded_evidence.model_dump(mode="json"),
        "llm_observations": [observation],
        "outcomes": [outcome],
    }
    assert prototype.validate_record_semantic_provenance(run_record) == []

    empty_semantic_plan = prototype.DiscoveryGroundingPlan(
        surface_candidates=[], behavior_candidates=[]
    )
    ensemble_record = {
        "replay_plans_from": None,
        "discovery_grounding_plans": [
            empty_semantic_plan.model_dump(mode="json"),
            semantic_plan.model_dump(mode="json"),
        ],
        "grounded_contract_plans": [
            prototype.GroundedContractPlan().model_dump(mode="json"),
            grounded_contract.model_dump(mode="json"),
        ],
        "grounded_evidence_plans": [
            prototype.IssueDiscoveryPlan(
                surface_candidates=[], behavior_candidates=[]
            ).model_dump(mode="json"),
            grounded_evidence.model_dump(mode="json"),
        ],
        "llm_observations": [observation],
        "outcomes": [outcome],
    }
    assert prototype.validate_record_semantic_provenance(ensemble_record) == []

    tampered_record = copy.deepcopy(run_record)
    tampered_record["llm_observations"][0]["raw_response"] = {"tampered": True}
    assert prototype.validate_record_semantic_provenance(tampered_record)


def test_llm_authority_without_matching_call_provenance_cannot_qualify_for_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The selected authored completion edge must be absent.",
        claim="The selected completion edge is extraneous.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=1,
        locations=["NL6", "tr_0025"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_absent",
            observed_transition_id="tr_0025",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.EvidencePlan(candidates=[candidate]),
        binding_authority="paper1_discovery_grounding_llm",
    )[0]
    finding = prototype.build_finding_records([outcome])[0]

    assert outcome["probe_groups"][0]["counterexample_found"] is True
    assert finding["witness_level"] == "W1"
    assert finding["w_validation_errors"] == []


def test_llm_binding_provenance_rejects_a_plan_not_equal_to_parsed_output() -> None:
    semantic_plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[],
        behavior_candidates=[],
    )
    observation = {
        "llm_call_id": "call-grounding-2",
        "role": "paper1_discovery_grounding",
        "status": "completed",
        "parsed_output": {"tampered": True},
    }

    provenance = prototype.build_llm_binding_provenance(
        [observation],
        role="paper1_discovery_grounding",
        semantic_plan=semantic_plan,
        grounded_contract_plan=prototype.GroundedContractPlan(),
        grounded_evidence_plan=prototype.IssueDiscoveryPlan(
            surface_candidates=[], behavior_candidates=[]
        ),
        replayed=True,
    )

    assert provenance is None


def test_w2_rejects_tampered_semantic_provenance() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected authored completion edge must be absent.",
        claim="The selected completion edge is extraneous.",
        observed_fact="The exact selected transition exists in the source model.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=1,
        locations=["NL6", "tr_0025"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_absent",
            observed_transition_id="tr_0025",
        ),
    )
    semantic_plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[candidate],
        behavior_candidates=[],
    )
    grounded_contract = prototype.GroundedContractPlan()
    grounded_evidence = prototype.IssueDiscoveryPlan(
        surface_candidates=[candidate], behavior_candidates=[]
    )
    provenance = prototype.build_llm_binding_provenance(
        [
            {
                "llm_call_id": "call-grounding-tamper-test",
                "role": "paper1_discovery_grounding",
                "status": "completed",
                "structured_schema_sha256": "schema-hash-tamper-test",
                "schema_contract_repeated_in_prompt": False,
                "system_prompt": "semantic grounding prompt",
                "user_prompt": "numbered NL and formal inventory",
                "raw_response": {"tool_call": "raw"},
                "parsed_output": semantic_plan.model_dump(mode="json"),
            }
        ],
        role="paper1_discovery_grounding",
        semantic_plan=semantic_plan,
        grounded_contract_plan=grounded_contract,
        grounded_evidence_plan=grounded_evidence,
        replayed=False,
    )
    assert provenance is not None
    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        grounded_evidence,
        binding_authority="paper1_discovery_grounding_llm",
        semantic_provenance=provenance,
    )[0]
    finding = prototype.build_finding_records([outcome])[0]
    receipt = finding["execution_certificates"][0]["semantic_binding_receipt"]
    receipt["semantic_provenance"]["parsed_output_sha256"] = "tampered"

    assert prototype.validate_witness_record(finding)


def test_d1_and_d2_are_accepted_while_d0_remains_audit_only() -> None:
    base = {
        "finding_key": "synthetic:f1",
        "witness_level": "W2",
        "source_attribution": ["causal_dual_certificate"],
        "d_validation_errors": [],
        "w_validation_errors": [],
    }
    findings = [
        {**base, "d_decision": {"d_level": "D1"}},
        {**base, "finding_key": "synthetic:f2", "d_decision": {"d_level": "D2"}},
        {**base, "finding_key": "synthetic:f3", "d_decision": {"d_level": "D0"}},
    ]

    accepted = prototype.select_accepted_issues(findings)

    assert {item["finding_key"] for item in accepted} == {
        "synthetic:f1",
        "synthetic:f2",
    }


def test_report_clusters_merge_exact_cause_but_preserve_normative_facets() -> None:
    def finding(
        key: str,
        *,
        d_level: str,
        claim: str,
        obligation: str,
        l_level: str = "L2",
    ) -> dict:
        return {
            "finding_key": key,
            "claims": [claim],
            "obligations": [obligation],
            "nl_quotes": [obligation],
            "locations": ["NL3"],
            "witness_level": "W2",
            "l_level": l_level,
            "source_attribution": ["causal_dual_certificate"],
            "d_decision": {"d_level": d_level},
            "d_validation_errors": [],
            "w_validation_errors": [],
        }

    facets = [
        finding(
            "source:missing_initial:Root:facet:a",
            d_level="D2",
            claim="evt_a consumer is unreachable.",
            obligation="evt_a must reach q1.",
        ),
        finding(
            "source:missing_initial:Root:facet:b",
            d_level="D1",
            claim="evt_b consumer is unreachable.",
            obligation="evt_b must reach q2.",
        ),
        finding(
            "source:reachable_deadlock:q_stop:facet:c",
            d_level="D2",
            claim="q_stop is a reachable deadlock.",
            obligation="Reachable non-final states must progress.",
        ),
    ]

    clusters = prototype.build_report_issue_clusters(facets)
    missing_initial = next(
        cluster
        for cluster in clusters
        if cluster["cause_key"] == "source:missing_initial:Root"
    )

    assert len(clusters) == 2
    assert missing_initial["facet_count"] == 2
    assert missing_initial["facet_d_levels"] == {
        "source:missing_initial:Root:facet:a": "D2",
        "source:missing_initial:Root:facet:b": "D1",
    }
    assert missing_initial["d_level"] == "D2"
    assert missing_initial["release_status"] == "confirmed_report_issue"
    assert len(prototype.select_confirmed_report_issues(clusters)) == 2


def test_report_clusters_consume_validated_d_duplicate_relation() -> None:
    def finding(
        key: str,
        *,
        duplicate_of: str | None = None,
        claim: str,
    ) -> dict:
        return {
            "finding_key": key,
            "claims": [claim],
            "obligations": ["The exact transition guards must be disjoint."],
            "nl_quotes": [],
            "locations": ["PUML:L10", "PUML:L11"],
            "witness_level": "W2",
            "l_level": "L1",
            "source_attribution": ["causal_dual_certificate"],
            "source_causality_certificate": {
                "kind": "source_guard_overlap",
                "source": "Root.Mode",
                "verdict": "counterexample",
                "sound_for_claim": True,
                "evidence": {"transition_ids": ["t1", "t2"]},
            },
            "formal_goals": [
                {
                    "relation": "guards_distinguishable",
                    "source": "Root.Mode",
                    "expected": True,
                }
            ],
            "d_decision": {
                "d_level": "D1",
                "duplicate_of": duplicate_of,
                "duplicate_rationale": (
                    "Both findings bind the same exact transitions and property."
                    if duplicate_of is not None
                    else None
                ),
            },
            "d_validation_errors": [],
            "w_validation_errors": [],
        }

    first_key = "hypothesis:guard_overlap:primary:facet:a"
    second_key = "source:guard_overlap:t1,t2:facet:b"
    independent_key = "source:wrong_target:t2:facet:c"
    clusters = prototype.build_report_issue_clusters(
        [
            finding(first_key, claim="The guards of t1 and t2 overlap."),
            finding(
                second_key,
                duplicate_of=first_key,
                claim="The same t1 and t2 guard pair is non-disjoint.",
            ),
            finding(independent_key, claim="t2 has the wrong target."),
        ]
    )

    assert len(clusters) == 2
    merged = next(cluster for cluster in clusters if cluster["facet_count"] == 2)
    assert merged["cause_keys"] == [
        "hypothesis:guard_overlap:primary",
        "source:guard_overlap:t1,t2",
    ]
    assert merged["deduplicated_by_d"] == [
        {
            "finding_key": second_key,
            "duplicate_of": first_key,
            "source_cause_key": "source:guard_overlap:t1,t2",
            "target_cause_key": "hypothesis:guard_overlap:primary",
        }
    ]
    assert next(
        cluster for cluster in clusters if cluster["facet_count"] == 1
    )["cause_key"] == "source:wrong_target:t2"


def test_direct_duplicate_without_typed_proof_is_rejected_and_kept_separate() -> (
    None
):
    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="lit",
            violated_obligation="The same formal obligation is violated.",
            strongest_defeater="A compatible alternative remains.",
            defeater_kind="undercutting",
            defeater_disposition="survives",
            rationale="The first reading is grounded but remains provisional.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "The two findings are the same issue."
                if duplicate_of is not None
                else None
            ),
            d_subclass="not_applicable",
            d_level="D1",
        )

    findings = [
        {
            "finding_key": "finding:a",
            "source_causality_certificate": {
                "kind": "source_guard_overlap",
                "source": "Root.Mode",
                "verdict": "counterexample",
                "sound_for_claim": True,
            },
            "formal_goals": [
                {
                    "relation": "guards_distinguishable",
                    "source": "Root.Mode",
                    "expected": True,
                }
            ],
        },
        {
            "finding_key": "finding:b",
            "source_causality_certificate": None,
            "formal_goals": [],
        },
    ]

    adjudicated = prototype.apply_d_adjudication(
        findings,
        prototype.DAdjudicationPlan(
            decisions=[decision("finding:a"), decision("finding:b", "finding:a")]
        ),
    )

    duplicate = next(
        finding for finding in adjudicated if finding["finding_key"] == "finding:b"
    )
    assert duplicate["d_validation_errors"] == [
        "duplicate_of requires positive typed source-certificate cause identity for both findings"
    ]
    assert len(prototype.build_report_issue_clusters(adjudicated)) == 2


def test_direct_duplicate_requires_a_canonical_formal_property_signature() -> None:
    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="lit",
            violated_obligation="The same formal obligation is violated.",
            strongest_defeater="A compatible alternative remains.",
            defeater_kind="undercutting",
            defeater_disposition="survives",
            rationale="The first reading is grounded but remains provisional.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "The two findings share the same certified cause."
                if duplicate_of is not None
                else None
            ),
            d_subclass="not_applicable",
            d_level="D1",
        )

    certificate = {
        "kind": "source_guard_overlap",
        "source": "Root.Mode",
        "verdict": "counterexample",
        "sound_for_claim": True,
    }
    findings = [
        {
            "finding_key": "finding:a",
            "source_causality_certificate": certificate,
            "formal_goals": [
                {
                    "relation": "guards_distinguishable",
                    "source": "Root.Mode",
                    "expected": True,
                }
            ],
        },
        {
            "finding_key": "finding:b",
            "source_causality_certificate": certificate,
            "formal_goals": [],
        },
        {
            "finding_key": "finding:c",
            "source_causality_certificate": certificate,
            "formal_goals": [
                {
                    "relation": "guards_distinguishable",
                    "source": "Root.Mode",
                    "expected": True,
                }
            ],
        },
    ]

    adjudicated = prototype.apply_d_adjudication(
        findings,
        prototype.DAdjudicationPlan(
            decisions=[
                decision("finding:a"),
                decision("finding:b", "finding:a"),
                decision("finding:c", "finding:a"),
            ]
        ),
    )

    duplicate = next(
        finding for finding in adjudicated if finding["finding_key"] == "finding:b"
    )
    assert duplicate["d_validation_errors"] == [
        "duplicate_of requires a canonical formal-property signature for both findings"
    ]
    accepted_duplicate = next(
        finding for finding in adjudicated if finding["finding_key"] == "finding:c"
    )
    assert accepted_duplicate["d_validation_errors"] == []
    clusters = prototype.build_report_issue_clusters(adjudicated)
    assert sorted(cluster["facet_count"] for cluster in clusters) == [1, 2]


def test_w1_issue_is_provisional_and_not_a_confirmed_issue() -> None:
    finding = {
        "finding_key": "synthetic:w1",
        "witness_level": "W1",
        "source_attribution": ["source_localized"],
        "d_validation_errors": [],
        "w_validation_errors": [],
        "d_decision": {"d_level": "D2"},
    }

    assert prototype.select_confirmed_issues([finding]) == []
    accepted = prototype.select_accepted_issues([finding])
    assert accepted[0]["release_status"] == "provisional_issue"


def test_explicitly_unsound_source_certificate_blocks_release() -> None:
    finding = {
        "finding_key": "synthetic:unsound-source-claim",
        "witness_level": "W1",
        "source_attribution": ["source_localized"],
        "source_causality_certificate": {
            "kind": "source_transition_contract",
            "sound_for_claim": False,
            "result": False,
            "verdict": "inconclusive",
        },
        "d_validation_errors": [],
        "w_validation_errors": [],
        "d_decision": {"d_level": "D1"},
    }

    assert prototype.select_accepted_issues([finding]) == []
    assert prototype.select_confirmed_issues([finding]) == []


def test_0059_guard_overlap_gets_source_executable_smt_w2() -> None:
    pair, inspect = _pair_and_inspect("0059")
    source = f"{pair['pair_name']}.AutonomousMode.UrbanMode.enter_urban"
    plan = prototype.EvidencePlan(
        candidates=[
            prototype.EvidenceCandidate(
                obligation="Urban maneuver guards must select one maneuver.",
                claim="The three outgoing urban maneuver guards overlap.",
                basis_kind="domain_norm",
                priority=5,
                locations=["PUML:L21", "PUML:L22", "PUML:L23"],
                proposed_l="L1",
                domain_obligation=prototype.GuardSetObligation(
                    property="disjoint",
                    scope_ref=source,
                    transition_refs=["tr_0012", "tr_0013", "tr_0014"],
                    guard_bindings=[
                        prototype.GuardConditionBinding(
                            transition_id=transition_id,
                            source_label=(
                                prototype._source_transition_by_id(pair, transition_id)
                                or {}
                            ).get("attributes", {}).get("raw_label", ""),
                            semantic_role="guard_condition",
                        )
                        for transition_id in ("tr_0012", "tr_0013", "tr_0014")
                    ],
                ),
                goal=prototype.EvidenceGoal(
                    relation="guards_distinguishable",
                    source=source,
                ),
            )
        ]
    )

    outcome = prototype.execute_evidence_plan(pair, inspect, plan)[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert (
        group["execution_certificate"]["evaluated_artifact"] == pair["paths"]["fcstm"]
    )
    proof = group["execution_certificate"]["observations"]
    assert proof["overlap_found"] is True
    assert proof["all_terminal"] is True
    assert any(item["witness"] for item in proof["pairs"])


def test_guard_overlap_rejects_binding_for_a_different_authored_label() -> None:
    pair, inspect = _pair_and_inspect("0059")
    source = f"{pair['pair_name']}.AutonomousMode.UrbanMode.enter_urban"
    bindings = []
    for transition_id in ("tr_0012", "tr_0013", "tr_0014"):
        transition = prototype._source_transition_by_id(pair, transition_id)
        assert transition is not None
        raw_label = (transition.get("attributes") or {}).get("raw_label")
        bindings.append(
            prototype.GuardConditionBinding(
                transition_id=transition_id,
                source_label=(
                    "[semantically different authored label]"
                    if transition_id == "tr_0013"
                    else raw_label
                ),
                semantic_role="guard_condition",
            )
        )
    candidate = prototype.EvidenceCandidate(
        obligation="Urban maneuver guards must select one maneuver.",
        claim="The three outgoing urban maneuver guards overlap.",
        basis_kind="domain_norm",
        priority=5,
        locations=["PUML:L21", "PUML:L22", "PUML:L23"],
        proposed_l="L1",
        domain_obligation=prototype.GuardSetObligation(
            property="disjoint",
            scope_ref=source,
            transition_refs=["tr_0012", "tr_0013", "tr_0014"],
            guard_bindings=bindings,
        ),
        goal=prototype.EvidenceGoal(relation="guards_distinguishable", source=source),
    )

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["execution_certificate"] is None
    assert "does not equal authored raw label" in group["error"]


def test_transition_condition_binding_is_exactly_checked() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The HighwayMode-to-UrbanMode route must be available on urban_way=true.",
        claim="The route loses its required condition.",
        basis_kind="nl_literal",
        nl_quote="The system can transition from HighwayMode to UrbanMode when urban_way=true.",
        priority=5,
        locations=["PUML:L37"],
        proposed_l="L0",
        domain_obligation=prototype.AttachmentObligation(
            attachment="trigger",
            subject_ref="tr_0023",
        ),
        goal=prototype.EvidenceGoal(
            relation="transition_contract",
            source="HighwayMode",
            target="UrbanMode",
            trigger="high_way=true",
            observed_transition_id="tr_0023",
            expected=True,
        ),
    )

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_causality_certificate"]["condition_present"] is False


def test_unprofiled_boolean_like_labels_do_not_get_guard_smt_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    source = f"{pair['pair_name']}.HighwayMode.enter_hwy"
    plan = prototype.EvidencePlan(
        candidates=[
            prototype.EvidenceCandidate(
                obligation="The two highway alternatives need a defined selection.",
                claim="The outgoing conditions from enter_hwy overlap.",
                basis_kind="nl_literal",
                nl_quote="can transition to cruise or lane_change",
                priority=5,
                locations=["PUML:L12", "PUML:L13"],
                proposed_l="L1",
                goal=prototype.EvidenceGoal(
                    relation="guards_distinguishable",
                    source=source,
                ),
            )
        ]
    )

    outcome = prototype.execute_evidence_plan(pair, inspect, plan)[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["counterexample_found"] is False
    assert group["execution_certificate"] is None
    assert "guard-only transitions" in group["error"]


def test_0059_unreachable_goal_gets_artifact_cut_and_source_certificate() -> None:
    pair, inspect = _pair_and_inspect("0059")
    target = (
        f"{pair['pair_name']}.CollisionAvoidanceSystem.collision_avoidance_deactive"
    )
    plan = prototype.EvidencePlan(
        candidates=[
            prototype.EvidenceCandidate(
                obligation="The collision-avoidance initial behavior must be reachable.",
                claim="The collision-avoidance subsystem is unreachable.",
                basis_kind="nl_literal",
                nl_quote="The collision avoidance system is initially in the collision_avoidance_deactive state.",
                priority=5,
                locations=["NL12", "PUML:L37", "PUML:L38"],
                proposed_l="L2",
                goal=prototype.EvidenceGoal(
                    relation="target_reachable",
                    target=target,
                ),
            )
        ]
    )

    outcome = prototype.execute_evidence_plan(pair, inspect, plan)[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert group["compiler_route"]["backend"] == "G_topology_proof"
    receipt = group["execution_certificate"]
    assert target in receipt["observations"]["unreachable_leaves"]
    assert group["source_causality_certificate"]["kind"] in {
        "missing_initial_with_compiler_consequence",
        "unreachable_source_component",
    }


def test_guard_profile_projection_loss_is_artifact_w2_not_source_w2() -> None:
    pair, inspect = _pair_and_inspect("0059")
    root = pair["pair_name"]
    plan = prototype.EvidencePlan(
        candidates=[
            prototype.EvidenceCandidate(
                obligation="The enter_urban to lane_change_urban edge carries a guard.",
                claim="The converted edge lost the source guard role.",
                basis_kind="nl_literal",
                nl_quote="it can transition to lane_change_urban if the distance to the front vehicle is less than 15 meters",
                priority=4,
                locations=["NL7", "PUML:L21"],
                proposed_l="L1",
                goal=prototype.EvidenceGoal(
                    relation="guard_present",
                    source=f"{root}.AutonomousMode.UrbanMode.enter_urban",
                    target=f"{root}.AutonomousMode.UrbanMode.lane_change_urban",
                ),
            )
        ]
    )

    group = prototype.execute_evidence_plan(pair, inspect, plan)[0]["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "unattributed"
    assert group["source_causality_certificate"]["kind"] == "source_guard_presence"
    assert group["source_causality_certificate"]["verdict"] == "satisfied"


def test_event_only_label_does_not_satisfy_guard_attachment() -> None:
    pair, inspect = _pair_and_inspect("0029")
    root = pair["pair_name"]
    candidate = prototype.EvidenceCandidate(
        obligation="The cruise alternative must carry its stated condition as a guard.",
        claim="The transition has an event-like label but no formal guard.",
        basis_kind="nl_literal",
        nl_quote="can transition to cruise or lane_change",
        priority=4,
        locations=["NL3", "PUML:L12"],
        proposed_l="L1",
        domain_obligation={
            "family": "attachment",
            "attachment": "guard",
            "subject_ref": "tr_0006",
        },
        goal=prototype.EvidenceGoal(
            relation="guard_present",
            observed_transition_id="tr_0006",
            source=f"{root}.HighwayMode.enter_hwy",
            target=f"{root}.HighwayMode.cruise",
        ),
    )

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert group["source_causality_certificate"]["verdict"] == "counterexample"


def test_0059_contract_group_finds_missing_guard_and_direct_edge() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractLensPlan(
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="AutonomousMode.HighwayMode.enter_hwy",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="AutonomousMode.HighwayMode.cruise",
                        condition="dist_to_front<25",
                        observed_transition_id="tr_0006",
                    ),
                    prototype.ExpectedTransitionTarget(
                        target="AutonomousMode.HighwayMode.lane_change",
                        condition="dist_to_front<25 && extra_lane=true",
                    ),
                ],
                nl_line=3,
                priority=5,
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    outcomes = prototype.execute_contract_lens_plan(pair, inspect, plan)
    groups = [item["probe_groups"][0] for item in outcomes]
    counterexamples = [item for item in groups if item["counterexample_found"]]

    assert {
        item["source_causality_certificate"]["kind"] for item in counterexamples
    } == {"source_transition_contract"}
    assert all(item["witness_level"] == "W2" for item in counterexamples)


def test_two_conditioned_alternatives_create_exact_guard_set_obligation() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidates = prototype.expand_transition_groups(
        pair,
        [
            prototype.ExpectedTransitionGroup(
                source="HighwayMode.enter_hwy",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="HighwayMode.cruise",
                        condition="dist_to_front<25 & extra_lane=true",
                        observed_transition_id="tr_0006",
                    ),
                    prototype.ExpectedTransitionTarget(
                        target="HighwayMode.lane_change",
                        condition="dist_to_front<25 & extra_lane=true",
                        observed_transition_id="tr_0007",
                    ),
                ],
                nl_line=2,
                priority=5,
            )
        ],
    )

    guard_candidate = next(
        item for item in candidates if item.goal.relation == "guards_distinguishable"
    )

    assert guard_candidate.domain_obligation == prototype.GuardSetObligation(
        property="disjoint",
        scope_ref="HighwayMode.enter_hwy",
        transition_refs=["tr_0006", "tr_0007"],
        guard_bindings=[
            prototype.GuardConditionBinding(
                transition_id=transition_id,
                source_label=(
                    prototype._source_transition_by_id(pair, transition_id) or {}
                ).get("attributes", {}).get("raw_label", ""),
                semantic_role="guard_condition",
            )
            for transition_id in ("tr_0006", "tr_0007")
        ],
    )
    assert prototype.validate_operator_executable_soundness(guard_candidate) == []
    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[guard_candidate])
    )[0]["probe_groups"][0]
    assert group["witness_level"] == "W1"
    assert group["counterexample_found"] is False
    assert group["source_attribution"]["status"] == "source_localized"


def test_guard_set_without_two_exact_transition_refs_is_located_only() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.expand_transition_groups(
        pair,
        [
            prototype.ExpectedTransitionGroup(
                source="InitialState",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="HighwayMode",
                        condition="high_way=true",
                        observed_transition_id="tr_0003",
                    ),
                    prototype.ExpectedTransitionTarget(
                        target="UrbanMode",
                        condition="urban_way=true",
                    ),
                ],
                nl_line=2,
                priority=5,
            )
        ],
    )[-1]

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["counterexample_found"] is False
    assert "at least two exact transition_refs" in group["error"]


def test_grouped_initial_contracts_keep_two_w2_receipts_in_one_report_issue() -> None:
    pair, inspect = _pair_and_inspect("0029")
    outcomes = prototype.execute_contract_extraction_plan(
        pair,
        inspect,
        prototype.ContractExtractionPlan(
            initial_contracts=[
                prototype.ExpectedInitialContract(
                    composite="HighwayMode",
                    target="HighwayMode.enter_hwy",
                    nl_line=3,
                    requirement_group_id="RG-mode-entry",
                    priority=5,
                ),
                prototype.ExpectedInitialContract(
                    composite="UrbanMode",
                    target="UrbanMode.enter_urban",
                    nl_line=7,
                    requirement_group_id="RG-mode-entry",
                    priority=5,
                ),
            ],
            transition_groups=[],
        ),
    )
    findings = prototype.build_finding_records(outcomes)
    clusters = prototype.build_report_issue_clusters(findings)

    assert len(findings) == 2
    assert {item["witness_level"] for item in findings} == {"W2"}
    assert all(len(item["execution_certificates"]) == 1 for item in findings)
    assert len(clusters) == 1
    assert clusters[0]["facet_count"] == 2
    assert clusters[0]["cause_key"] == (
        "source:initial_requirement_group:RG-mode-entry"
    )
    assert len(clusters[0]["claims"]) == 2


def test_llm_grounding_output_can_restore_omitted_nl_alternative() -> None:
    pair, inspect = _pair_and_inspect("0059")
    raw_contract = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="cruise",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="lane_change",
                        condition="dist_to_front<25 && extra_lane=true",
                    )
                ],
                nl_line=3,
                priority=3,
            )
        ],
    )
    raw_evidence = prototype.IssueDiscoveryPlan(
        surface_candidates=[], behavior_candidates=[]
    )
    grounding = prototype.SemanticGroundingPlan(
        contract_plan=prototype.ContractExtractionPlan(
            initial_contracts=[],
            transition_groups=[
                prototype.ExpectedTransitionGroup(
                    source="AutonomousMode.HighwayMode.enter_hwy",
                    targets=[
                        prototype.ExpectedTransitionTarget(
                            target="AutonomousMode.HighwayMode.cruise",
                            condition="dist_to_front<25",
                            observed_transition_id="tr_0006",
                        ),
                        prototype.ExpectedTransitionTarget(
                            target="AutonomousMode.HighwayMode.lane_change",
                            condition="dist_to_front<25 && extra_lane=true",
                        ),
                    ],
                    nl_line=3,
                    priority=5,
                )
            ],
        ),
        evidence_bindings=[],
    )

    grounded, _, diagnostics = prototype.validate_semantic_grounding(
        pair, raw_evidence, grounding
    )

    outcomes = prototype.execute_contract_extraction_plan(pair, inspect, grounded)
    counterexample_kinds = {
        group["source_causality_certificate"]["kind"]
        for outcome in outcomes
        for group in outcome["probe_groups"]
        if group["counterexample_found"]
    }

    assert counterexample_kinds == {"source_transition_contract"}
    assert diagnostics == []
    assert len(raw_contract.transition_groups[0].targets) == 1


def test_llm_grounded_abstract_transition_contracts_execute_as_satisfied() -> None:
    fixtures = {
        "0016": [
            (
                "SearchMission",
                "FormationAdjust",
                "intercepted",
                "tr_0009",
                3,
            ),
            (
                "SearchMission",
                "AttackState",
                "task assignment information is received",
                "tr_0012",
                4,
            ),
        ],
        "0046": [
            (
                "UAVSwarmStateMachine.SearchRegion.Searching",
                "UAVSwarmStateMachine.SearchRegion.FormationAdjustment",
                "intercepted",
                "tr_0003",
                3,
            ),
            (
                "UAVSwarmStateMachine.SearchRegion.Searching",
                "UAVSwarmStateMachine.SearchRegion.Attacking",
                "task assignment information is received",
                "tr_0004",
                4,
            ),
        ],
    }

    for case, transitions in fixtures.items():
        pair, inspect = _pair_and_inspect(case)
        plan = prototype.ContractExtractionPlan(
            initial_contracts=[],
            transition_groups=[
                prototype.ExpectedTransitionGroup(
                    source=source,
                    targets=[
                        prototype.ExpectedTransitionTarget(
                            target=target,
                            condition=condition,
                            observed_transition_id=transition_id,
                        )
                    ],
                    nl_line=nl_line,
                    priority=5,
                )
                for source, target, condition, transition_id, nl_line in transitions
            ],
        )

        outcomes = prototype.execute_contract_extraction_plan(pair, inspect, plan)
        groups = [outcome["probe_groups"][0] for outcome in outcomes]

        assert all(group["witness_level"] == "W1" for group in groups)
        assert all(group["counterexample_found"] is False for group in groups)
        assert all(
            group["execution_certificate"]["verdict"] == "inconclusive" for group in groups
        )
        assert all(
            group["source_causality_certificate"]["verdict"] == "inconclusive"
            for group in groups
        )


def test_exact_three_way_contract_triggers_automatic_overlap_smt() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="AutonomousMode.UrbanMode.enter_urban",
                targets=[
                        prototype.ExpectedTransitionTarget(
                            target="AutonomousMode.UrbanMode.lane_change_urban",
                            condition="dist_to_front<15 && extra_lane=true",
                            observed_transition_id="tr_0012",
                        ),
                        prototype.ExpectedTransitionTarget(
                            target="AutonomousMode.UrbanMode.straight",
                            condition="road_clear",
                            observed_transition_id="tr_0013",
                        ),
                        prototype.ExpectedTransitionTarget(
                            target="AutonomousMode.UrbanMode.intersection",
                            condition="intersection=true",
                            observed_transition_id="tr_0014",
                        ),
                ],
                nl_line=7,
                priority=4,
            )
        ],
    )

    outcomes = prototype.execute_contract_extraction_plan(pair, inspect, plan)
    overlap_counterexamples = [
        group
        for outcome in outcomes
        for group in outcome["probe_groups"]
        if group["counterexample_found"]
        and group["source_causality_certificate"]["kind"] == "source_guard_overlap"
    ]

    assert len(overlap_counterexamples) == 1


def test_parent_level_transition_contract_accepts_complete_mapping_macro() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractLensPlan(
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="AutonomousMode.HighwayMode",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="AutonomousMode.UrbanMode",
                        condition="urban_way=true",
                    )
                ],
                nl_line=11,
                priority=4,
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    group = prototype.execute_contract_lens_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]

    assert group["counterexample_found"] is False
    receipts = group["execution_certificate"]["observations"]["mapping_macro_receipts"]
    assert receipts and all(item["complete"] for item in receipts)


def test_initial_contract_uses_initial_target_instead_of_direct_edge() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="AutonomousMode",
                target="AutonomousMode.InitialState",
                nl_line=1,
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]

    assert group["counterexample_found"] is False


def test_0029_grounded_containment_contract_gets_source_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[
            prototype.ExpectedContainmentContract(
                parent="AutonomousMode",
                child="InitialState",
                nl_line=1,
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    source = group["source_causality_certificate"]
    assert source["kind"] == "source_containment_contract"
    assert source["child"] == "InitialState"
    assert source["expected_parent"] == "AutonomousMode"
    assert source["actual_parent"] is None
    assert source["actual_ancestor_chain"] == []
    assert source["within_expected_ancestor"] is False
    assert group["witness_level"] == "W2"


def test_initial_contract_is_inconclusive_when_expected_composite_is_a_leaf() -> None:
    pair, inspect = _pair_and_inspect("0029")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="AutonomousMode",
                target="InitialState",
                nl_line=1,
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]
    source = group["source_causality_certificate"]

    assert source["direct_children"] == []
    assert source["scope_supports_initial"] is False
    assert source["sound_for_claim"] is False
    assert source["verdict"] == "inconclusive"


def test_initial_target_uses_eventless_attempted_entry_as_source_evidence() -> None:
    """An authored completion edge can prove attempted default-entry intent."""

    pair, inspect = _pair_and_inspect("0034")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="InMotion",
                target="Accelerating",
                nl_line=8,
                nl_quote=(
                    '8. The system enters the Accelerating substate when motion '
                    'begins, marked by the "Entry/Accelerate" action. '
                ),
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]
    source = group["source_causality_certificate"]

    assert source["attempted_entry_edge_count"] == 1
    assert source["attempted_entry_edges"][0]["target"] == "Accelerating"
    assert source["scope_supports_initial"] is True
    assert source["sound_for_claim"] is True
    assert source["verdict"] == "counterexample"
    assert group["witness_level"] == "W2"
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    compact = prototype._compact_source_certificate_for_d(source)
    assert compact["attempted_entry_edge_count"] == 1
    assert compact["attempted_entry_edges"][0]["id"] == "tr_0006"


def test_containment_certificate_distinguishes_transitive_from_direct_parent() -> None:
    pair, inspect = _pair_and_inspect("0053")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[
            prototype.ExpectedContainmentContract(
                parent="PumpControl",
                child="PumpControl.PumpRegion.PumpState",
                nl_line=2,
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]
    source = group["source_causality_certificate"]

    assert source["actual_parent"] == "PumpControl.PumpRegion"
    assert source["actual_ancestor_chain"] == [
        "PumpControl.PumpRegion",
        "PumpControl",
    ]
    assert source["within_expected_ancestor"] is True


def test_initial_contract_accepts_exact_formal_parent_and_child_ids() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="CollisionAvoidanceSystem",
                target="CollisionAvoidanceSystem.collision_avoidance_deactive",
                nl_line=12,
                priority=5,
            )
        ],
        transition_groups=[],
    )

    group = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0][
        "probe_groups"
    ][0]

    assert group["counterexample_found"] is False
    bindings = group["checks"][0]["normalized_probe"]["bindings"]
    assert str(bindings["composite"]).endswith(".CollisionAvoidanceSystem")
    assert str(bindings["child"]).endswith(
        ".CollisionAvoidanceSystem.collision_avoidance_deactive"
    )


def test_root_scope_is_an_exact_initial_contract_binding() -> None:
    pair, inspect = _pair_and_inspect("0054")
    root_scope = pair["canonical"]["model"]["name"]
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite=root_scope,
                composite_concept_id="C-System",
                target="DoorsClosing",
                target_concept_id="C-DoorsClosing",
                nl_line=1,
                priority=5,
            )
        ],
        transition_groups=[],
    )
    bindings = [
        prototype.SemanticConceptBinding(
            concept_id="C-System",
            source_state_id=root_scope,
            nl_lines=[1],
        ),
        prototype.SemanticConceptBinding(
            concept_id="C-DoorsClosing",
            source_state_id="DoorsClosing",
            nl_lines=[1],
        ),
    ]

    grounded, diagnostics = prototype._validate_grounded_contract_plan(
        pair, plan, bindings
    )
    group = prototype.execute_contract_extraction_plan(pair, inspect, grounded)[0][
        "probe_groups"
    ][0]

    assert diagnostics == []
    assert prototype._semantic_grounding_inventory(pair)["root_scope_id"] == root_scope
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    certificate = prototype._source_initial_target_certificate(
        pair, root_scope, "DoorsClosing"
    )
    assert certificate is not None
    assert certificate["composite"] == root_scope
    assert certificate["verdict"] == "satisfied"


def test_unresolved_transition_target_is_retained_as_w1_coverage_gap() -> None:
    pair, inspect = _pair_and_inspect("0059")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="lane_change",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="exit", condition="dist_to_exit<2"
                    )
                ],
                nl_line=4,
                priority=3,
            )
        ],
    )

    outcomes = prototype.execute_contract_extraction_plan(pair, inspect, plan)
    group = outcomes[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["counterexample_found"] is False
    assert group["execution_certificate"]["verdict"] == "inconclusive"
    assert group["source_causality_certificate"]["sound_for_claim"] is False
    findings = prototype.build_finding_records(outcomes)
    finding = next(
        finding
        for finding in findings
        if any(
            "lane_change must transition directly to exit" in obligation
            for obligation in finding["obligations"]
        )
    )
    assert finding["witness_level"] == "W1"
    assert finding["evidence_status"] == "coverage_gap"
    assert finding["counterexample_found"] is False


def test_l_is_derived_from_goal_relation_not_model_proposal() -> None:
    pair, inspect = _pair_and_inspect("0059")
    source = f"{pair['pair_name']}.AutonomousMode.UrbanMode.enter_urban"
    plan = prototype.EvidencePlan(
        candidates=[
            prototype.EvidenceCandidate(
                obligation="Outgoing alternatives must be distinguishable.",
                claim="The outgoing guards overlap.",
                basis_kind="domain_norm",
                priority=5,
                locations=["PUML:L21"],
                proposed_l="L2",
                goal=prototype.EvidenceGoal(
                    relation="guards_distinguishable",
                    source=source,
                ),
            )
        ]
    )

    findings = prototype.build_finding_records(
        prototype.execute_evidence_plan(pair, inspect, plan)
    )

    assert findings[0]["l_level"] == "L1"


def test_semantic_text_is_not_rejected_by_arbitrary_schema_length() -> None:
    long_explanation = "semantically relevant evidence " * 40

    candidate = prototype.BalancedEvidenceCandidate(
        obligation=long_explanation,
        claim=long_explanation,
        basis_kind="nl_literal",
        nl_quote=long_explanation,
        priority=3,
        locations=["NL1"],
        proposed_l="L2",
        observed_fact=long_explanation,
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Target",
        ),
    )

    assert len(candidate.claim) > 320


def test_semantic_evidence_is_not_rejected_by_arbitrary_citation_count() -> None:
    locations = [f"PUML:L{index}" for index in range(1, 9)]

    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A multi-step path must remain reachable.",
        claim="The complete source path supplies all cited evidence locations.",
        basis_kind="nl_literal",
        nl_quote="A multi-step path must remain reachable.",
        priority=3,
        locations=locations,
        proposed_l="L2",
        observed_fact="The evidence spans eight exact source locations.",
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            source="Root.Source",
            target="Root.Target",
        ),
    )

    assert candidate.locations == locations


def test_probe_candidate_accepts_four_source_locations() -> None:
    candidate = prototype.ProbeCandidate(
        claim="A localized hypothesis.",
        basis_kind="nl_literal",
        priority=3,
        locations=["NL1", "PUML:L1", "F1", "Root.State"],
    )

    assert len(candidate.locations) == 4


def test_grounding_validator_rejects_nonexistent_formal_state_id() -> None:
    pair, _ = _pair_and_inspect("0059")
    empty_evidence = prototype.IssueDiscoveryPlan(
        surface_candidates=[], behavior_candidates=[]
    )
    grounding = prototype.SemanticGroundingPlan(
        contract_plan=prototype.ContractExtractionPlan(
            initial_contracts=[],
            transition_groups=[
                prototype.ExpectedTransitionGroup(
                    source="not-a-formal-state-id",
                    targets=[
                        prototype.ExpectedTransitionTarget(
                            target="also-not-a-formal-state-id",
                            condition="a natural-language condition",
                        )
                    ],
                    nl_line=4,
                    priority=3,
                )
            ],
        ),
        evidence_bindings=[],
    )

    contract, _, diagnostics = prototype.validate_semantic_grounding(
        pair, empty_evidence, grounding
    )

    assert contract.transition_groups == []
    assert diagnostics[0]["class"] == "formal_id_invalid"


def test_direct_discovery_grounding_clears_nonexact_state_bindings() -> None:
    pair, inspect = _pair_and_inspect("0029")
    plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[],
        behavior_candidates=[
            prototype.BalancedEvidenceCandidate(
                obligation="A selected event must reach the required state.",
                claim="The selected event reaches a different state.",
                basis_kind="nl_literal",
                nl_quote=pair["nl"].splitlines()[4],
                priority=5,
                locations=["NL5"],
                proposed_l="L2",
                observed_fact="The selected source transition has another endpoint.",
                goal=prototype.EvidenceGoal(
                    relation="event_reaches_target",
                    observed_transition_id="tr_0009",
                    source="not-an-exact-state-id",
                    trigger="dist_to_exit<2",
                    target="also-not-an-exact-state-id",
                ),
            )
        ],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(
        pair,
        prototype.ContractExtractionPlan(initial_contracts=[], transition_groups=[]),
        plan,
    )
    goal = evidence.behavior_candidates[0].goal
    outcome = prototype.execute_evidence_plan(pair, inspect, evidence)[0]

    assert goal.source is None
    assert goal.target is None
    assert {item["class"] for item in diagnostics} == {"formal_id_invalid"}
    assert outcome["envelope_witness_level"] == "W1"
    assert outcome["has_counterexample_group"] is False


def test_contract_binding_patch_cannot_rewrite_normative_condition() -> None:
    pair, _ = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="the cruise concept",
                source_concept_id="C-cruise",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="the highway-exit concept",
                        target_concept_id="C-exit-highway",
                        condition="dist_to_exit<2",
                    )
                ],
                nl_line=5,
                priority=5,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-cruise", source_state_id="HighwayMode.cruise"
            ),
            prototype.CompactConceptBinding(
                concept_id="C-exit-highway",
                source_state_id="HighwayMode.exit_hwy",
            ),
        ],
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[
            prototype.TransitionGroupGrounding(
                item_index=0,
                status="grounded",
                source="HighwayMode.cruise",
                targets=[
                    prototype.TransitionTargetGrounding(
                        target_index=0,
                        target="HighwayMode.exit_hwy",
                        observed_transition_id="tr_0009",
                    )
                ],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    contract, _, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    target = contract.transition_groups[0].targets[0]

    assert diagnostics == []
    assert target.condition == "dist_to_exit<2"
    assert target.observed_transition_id == "tr_0009"
    assert contract.transition_groups[0].nl_line == 5
    assert contract.transition_groups[0].priority == 5


def test_sparse_grounding_instantiates_accepted_contracts_from_concept_bindings() -> (
    None
):
    pair, _ = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="the highway mode",
                composite_concept_id="C-highway",
                target="the highway entry",
                target_concept_id="C-entry",
                nl_line=3,
                priority=1,
            )
        ],
        containment_contracts=[
            prototype.ExpectedContainmentContract(
                parent="the highway mode",
                parent_concept_id="C-highway",
                child="the highway entry",
                child_concept_id="C-entry",
                nl_line=3,
                priority=1,
            )
        ],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="the cruise mode",
                source_concept_id="C-cruise",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="the highway exit",
                        target_concept_id="C-exit",
                        condition="dist_to_exit<2",
                    )
                ],
                nl_line=5,
                priority=1,
            )
        ],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept="the cruise mode",
                concept_id="C-cruise",
                scope_concept_id="C-highway",
                role="operating_state",
                nl_quote="In the cruise substate",
                priority=1,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-highway", source_state_id="HighwayMode"
            ),
            prototype.CompactConceptBinding(
                concept_id="C-entry", source_state_id="HighwayMode.enter_hwy"
            ),
            prototype.CompactConceptBinding(
                concept_id="C-cruise", source_state_id="HighwayMode.cruise"
            ),
            prototype.CompactConceptBinding(
                concept_id="C-exit", source_state_id="HighwayMode.exit_hwy"
            ),
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    grounded, evidence, diagnostics = prototype.validate_discovery_grounding(
        pair, raw, plan
    )

    assert diagnostics == []
    assert grounded.initial_contracts[0].composite == "HighwayMode"
    assert grounded.initial_contracts[0].target == "HighwayMode.enter_hwy"
    assert grounded.containment_contracts[0].child == "HighwayMode.enter_hwy"
    assert grounded.transition_groups[0].source == "HighwayMode.cruise"
    assert grounded.transition_groups[0].targets[0].target == "HighwayMode.exit_hwy"
    assert evidence.candidates == []


def test_grounded_contract_union_is_not_truncated_by_llm_output_bounds() -> None:
    pair, _ = _pair_and_inspect("0029")

    def group() -> prototype.ExpectedTransitionGroup:
        return prototype.ExpectedTransitionGroup(
            source="semantic source concept",
            targets=[
                prototype.ExpectedTransitionTarget(
                    target="semantic target concept",
                )
            ],
            nl_line=5,
            priority=3,
        )

    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[group() for _ in range(16)],
    )
    plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[
            prototype.TransitionGroupGrounding(
                item_index=index,
                status="grounded",
                source="HighwayMode.cruise",
                targets=[
                    prototype.TransitionTargetGrounding(
                        target_index=0,
                        target="HighwayMode.exit_hwy",
                    )
                ],
            )
            for index in range(16)
        ],
        additional_contracts=prototype.ContractExtractionPlan(
            initial_contracts=[],
            transition_groups=[
                prototype.ExpectedTransitionGroup(
                    source="HighwayMode.cruise",
                    targets=[
                        prototype.ExpectedTransitionTarget(
                            target="HighwayMode.exit_hwy",
                        )
                    ],
                    nl_line=5,
                    priority=3,
                )
                for _ in range(3)
            ],
        ),
        surface_candidates=[],
        behavior_candidates=[],
    )

    grounded, _, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert isinstance(grounded, prototype.GroundedContractPlan)
    assert len(grounded.transition_groups) == 19
    assert diagnostics == []


def test_llm_semantic_rejection_suppresses_raw_contract_without_text_rules() -> None:
    pair, _ = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="misread sequential concept",
                target="misread target concept",
                nl_line=5,
                priority=3,
            )
        ],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="wrong semantic source",
                targets=[
                    prototype.ExpectedTransitionTarget(target="wrong semantic target")
                ],
                nl_line=5,
                priority=3,
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[
            prototype.InitialContractGrounding(
                item_index=0,
                status="rejected",
                reason="The NL describes sequential flow, not composite entry.",
            )
        ],
        containment_contract_bindings=[],
        transition_group_bindings=[
            prototype.TransitionGroupGrounding(
                item_index=0,
                status="unresolved",
                reason="The NL source remains ambiguous.",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    grounded, _, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert grounded.initial_contracts == []
    assert grounded.transition_groups == []
    assert {item["class"] for item in diagnostics} == {
        "binding_semantically_rejected",
        "binding_semantically_unresolved",
    }


def test_runtime_has_no_deterministic_nl_semantic_matcher() -> None:
    for forbidden in (
        "derive_lexical_transition_groups",
        "augment_transition_groups",
        "_semantic_stem",
        "_semantic_tokens",
        "_semantic_phrase_matches",
        "_infer_unique_transition_binding",
    ):
        assert not hasattr(prototype, forbidden)


def test_semantic_reason_text_has_no_arbitrary_schema_length_gate() -> None:
    long_reason = "This remains a semantic explanation. " * 32

    gap = prototype.SemanticGroundingGap(
        scope="contract",
        item_index=0,
        field="source",
        reason=long_reason,
    )
    initial = prototype.InitialContractGrounding(
        item_index=0,
        status="rejected",
        reason=long_reason,
    )
    containment = prototype.ContainmentContractGrounding(
        item_index=0,
        status="unresolved",
        reason=long_reason,
    )
    transition = prototype.TransitionGroupGrounding(
        item_index=0,
        status="rejected",
        reason=long_reason,
    )
    required_state = prototype.RequiredStateGrounding(
        item_index=0,
        status="unresolved",
        reason=long_reason,
    )
    required_event = prototype.RequiredEventScopeGrounding(
        item_index=0,
        status="unresolved",
        reason=long_reason,
    )

    assert len(long_reason) > 320
    assert {
        gap.reason,
        initial.reason,
        containment.reason,
        transition.reason,
        required_state.reason,
        required_event.reason,
    } == {long_reason}


def test_semantic_contract_text_has_no_arbitrary_schema_length_gate() -> None:
    long_text = "semantically meaningful source text " * 40

    plan = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite=long_text,
                target=long_text,
                nl_line=1,
                nl_quote=long_text,
                priority=1,
            )
        ],
        containment_contracts=[
            prototype.ExpectedContainmentContract(
                parent=long_text,
                child=long_text,
                nl_line=1,
                nl_quote=long_text,
                priority=1,
            )
        ],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source=long_text,
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target=long_text,
                        condition=long_text,
                    )
                ],
                nl_line=1,
                nl_quote=long_text,
                priority=1,
            )
        ],
        required_state_contracts=[
            prototype.RequiredStateContract(
                concept=long_text,
                concept_id="C-long-state",
                role="operating_state",
                nl_quote=long_text,
                priority=1,
            )
        ],
        required_event_scope_contracts=[
            prototype.RequiredEventScopeContract(
                event_concept=long_text,
                scope_concept=long_text,
                applicability="one_scope",
                nl_quote=long_text,
                priority=1,
            )
        ],
    )

    assert len(long_text) > 480
    assert plan.transition_groups[0].targets[0].condition == long_text


def test_exhaustive_contract_and_grounding_lists_have_no_arbitrary_caps() -> None:
    target = prototype.ExpectedTransitionTarget(target="Root.Target")
    groups = [
        prototype.ExpectedTransitionGroup(
            source=f"Root.Source{index}",
            targets=[target] * 5,
            nl_line=index + 1,
            nl_quote=f"Requirement {index}",
            priority=5,
        )
        for index in range(17)
    ]
    contract = prototype.ContractExtractionPlan(
        initial_contracts=[],
        containment_contracts=[],
        transition_groups=groups,
    )
    grounding = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[
            prototype.TransitionGroupGrounding(
                item_index=index,
                status="grounded",
                source=group.source,
                targets=[
                    prototype.TransitionTargetGrounding(
                        target_index=target_index,
                        target=item.target,
                    )
                    for target_index, item in enumerate(group.targets)
                ],
            )
            for index, group in enumerate(groups)
        ],
        additional_contracts=contract,
        surface_candidates=[],
        behavior_candidates=[],
    )

    assert len(contract.transition_groups) == 17
    assert len(contract.transition_groups[0].targets) == 5
    assert len(grounding.transition_group_bindings) == 17
    contract_schema = prototype.ContractExtractionPlan.model_json_schema()
    grounding_schema = prototype.DiscoveryGroundingPlan.model_json_schema()
    assert "maxItems" not in contract_schema["properties"]["transition_groups"]
    assert "maxItems" not in grounding_schema["properties"]["transition_group_bindings"]


def test_unresolved_candidate_binding_is_an_execution_veto() -> None:
    pair, inspect = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[], containment_contracts=[], transition_groups=[]
    )
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected transition must be absent.",
        claim="The selected transition is extraneous.",
        observed_fact="One exact source transition was selected.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=1,
        locations=["NL6", "tr_0025"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_absent",
            observed_transition_id="tr_0025",
        ),
    )
    plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[candidate],
        behavior_candidates=[],
        unresolved=[
            prototype.SemanticGroundingGap(
                scope="surface_candidate",
                item_index=0,
                field="observed_transition_id",
                reason="Two semantic bindings remain competent.",
            )
        ],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    outcome = prototype.execute_evidence_plan(pair, inspect, evidence)[0]

    assert evidence.surface_candidates[0].goal.observed_transition_id is None
    assert outcome["envelope_witness_level"] == "W1"
    assert outcome["probe_groups"][0]["execution_certificate"] is None
    assert any(
        item["class"] == "semantic_binding_unresolved_veto" for item in diagnostics
    )


def test_unauthorized_transition_binding_expands_to_exact_absence_lane() -> None:
    pair, inspect = _pair_and_inspect("0029")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[], containment_contracts=[], transition_groups=[]
    )
    plan = prototype.DiscoveryGroundingPlan(
        initial_contract_bindings=[],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[],
        behavior_candidates=[],
        unauthorized_transition_bindings=[
            prototype.UnauthorizedTransitionGrounding(
                observed_transition_id="tr_0025",
                status="unauthorized",
                nl_quote=pair["nl"].splitlines()[5],
                nl_lines=[6, 10],
                rationale=(
                    "The NL enumerates mode-level completion sources and does not "
                    "authorize this additional source transition."
                ),
            )
        ],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert diagnostics == []
    assert len(evidence.surface_candidates) == 1
    candidate = evidence.surface_candidates[0]
    assert candidate.domain_obligation == prototype.ElementObligation(
        element_kind="transition",
        operator="absent",
        subject_ref="tr_0025",
    )
    assert candidate.goal == prototype.EvidenceGoal(
        relation="transition_absent",
        observed_transition_id="tr_0025",
        expected=False,
    )
    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        )
    )[0]
    assert outcome["probe_groups"][0]["counterexample_found"] is True
    assert outcome["probe_groups"][0]["source_causality_certificate"]["kind"] == (
        "source_extraneous_transition"
    )


def test_indexed_contract_binding_authorizes_root_without_duplicate_concept_row() -> (
    None
):
    pair, _ = _pair_and_inspect("0048")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[
            prototype.ExpectedInitialContract(
                composite="system",
                composite_concept_id="C-system",
                target="TurnOn",
                target_concept_id="C-TurnOn",
                nl_line=1,
                nl_quote="The system begins in the TurnOn state",
                priority=1,
            )
        ],
        containment_contracts=[],
        transition_groups=[],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[],
        initial_contract_bindings=[
            prototype.InitialContractGrounding(
                item_index=0,
                status="grounded",
                composite=pair["pair_name"],
                target="TurnOn",
            )
        ],
        containment_contract_bindings=[],
        transition_group_bindings=[],
        surface_candidates=[],
        behavior_candidates=[],
    )

    grounded, _, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert diagnostics == []
    assert grounded.initial_contracts[0].composite == pair["pair_name"]


def test_exact_quote_validation_checks_provenance_not_physical_line_segmentation() -> (
    None
):
    pair, _ = _pair_and_inspect("0030")

    def candidate(quote: str):
        return prototype.BalancedEvidenceCandidate(
            obligation="The shutdown event must be available.",
            claim="The shutdown event is unavailable.",
            observed_fact="A formal execution target is supplied separately.",
            basis_kind="nl_literal",
            nl_quote=quote,
            priority=1,
            locations=["NL5"],
            proposed_l="L0",
            goal=prototype.EvidenceGoal(
                relation="event_consumed_in_scope",
                source="Autonomous",
                observed_transition_id="tr_0007",
            ),
        )

    assert prototype._nl_anchor_valid(
        pair, candidate("5 when power off, it will transit to final state")
    )
    assert not prototype._nl_anchor_valid(
        pair, candidate("When shutdown occurs, the system terminates.")
    )
    domain_candidate = candidate(
        "When shutdown occurs, the system terminates."
    ).model_copy(update={"basis_kind": "domain_norm"})
    assert not prototype._nl_anchor_valid(pair, domain_candidate)


def test_executable_evidence_is_noninterfering_in_candidate_prose() -> None:
    pair, inspect = _pair_and_inspect("0029")
    goal = prototype.EvidenceGoal(
        relation="transition_absent",
        observed_transition_id="tr_0025",
    )

    def execute(*, obligation: str, claim: str, observed_fact: str):
        candidate = prototype.BalancedEvidenceCandidate(
            obligation=obligation,
            claim=claim,
            basis_kind="nl_literal",
            nl_quote=pair["nl"].splitlines()[5],
            priority=4,
            locations=["NL6", "tr_0025"],
            proposed_l="L0",
            observed_fact=observed_fact,
            goal=goal,
        )
        return prototype.execute_evidence_plan(
            pair,
            inspect,
            prototype.IssueDiscoveryPlan(
                surface_candidates=[candidate], behavior_candidates=[]
            ),
        )[0]["probe_groups"][0]

    first = execute(
        obligation="The selected authored completion edge must be absent.",
        claim="The selected completion edge is extraneous.",
        observed_fact="The exact selected transition exists in the source model.",
    )
    paraphrase = execute(
        obligation="A wholly different prose formulation of the same formal duty.",
        claim="Narrative wording must not steer the formal evaluator.",
        observed_fact="This sentence deliberately changes every reporting phrase.",
    )

    assert first["compiled_assertion"] == paraphrase["compiled_assertion"]
    assert first["witness_level"] == paraphrase["witness_level"] == "W2"
    assert first["counterexample_found"] is paraphrase["counterexample_found"] is True
    assert first["source_attribution"] == paraphrase["source_attribution"]
    for field in ("execution_certificate", "source_causality_certificate"):
        first_certificate = dict(first[field])
        paraphrase_certificate = dict(paraphrase[field])
        first_certificate.pop("semantic_binding_receipt")
        paraphrase_certificate.pop("semantic_binding_receipt")
        assert first_certificate == paraphrase_certificate


def test_normalize_check_applies_declared_source_namespace_mapping() -> None:
    pair, inspect = _pair_and_inspect("0059")
    check = prototype.ProbeCheck(
        kind="initial_target",
        bindings={
            "composite": "AutonomousMode.HighwayMode",
            "child": "AutonomousMode.HighwayMode.enter_hwy",
        },
    )

    normalized, changes = prototype.normalize_check(check, inspect, pair)

    assert str(normalized.bindings["composite"]).endswith(".AutonomousMode.HighwayMode")
    assert str(normalized.bindings["child"]).endswith(
        ".AutonomousMode.HighwayMode.enter_hwy"
    )
    assert {item["field"] for item in changes} == {
        "bindings.composite",
        "bindings.child",
    }


def test_normalize_check_does_not_guess_from_identifier_suffixes() -> None:
    pair, inspect = _pair_and_inspect("0059")
    check = prototype.ProbeCheck(
        kind="initial_target",
        bindings={"composite": "HighwayMode", "child": "enter_hwy"},
    )

    normalized, changes = prototype.normalize_check(check, inspect, pair)

    assert normalized.bindings == check.bindings
    assert changes == []


def test_normalize_check_does_not_complete_an_event_namespace_without_mapping() -> None:
    pair, inspect = _pair_and_inspect("0059")
    qualified = next(
        str(row["qualified_name"])
        for row in inspect["events"]
        if isinstance(row, dict)
        and isinstance(row.get("qualified_name"), str)
        and str(row["qualified_name"]).startswith(f"{pair['pair_name']}.")
    )
    unqualified = qualified.removeprefix(f"{pair['pair_name']}.")
    check = prototype.ProbeCheck(
        kind="event_declared",
        bindings={"event": unqualified},
    )

    normalized, changes = prototype.normalize_check(check, inspect, pair)

    assert normalized.bindings == check.bindings
    assert changes == []


def test_same_region_clause_requires_an_actual_cross_region_target() -> None:
    same_region = {
        "source_causality_certificate": {
            "kind": "source_initial_target_contract",
            "initial_edges": [{"id": "tr_initial", "target": "M.other"}],
            "target_is_direct_child": True,
            "verdict": "counterexample",
        }
    }
    cross_region = {
        "source_causality_certificate": {
            "kind": "source_initial_target_contract",
            "initial_edges": [{"id": "tr_initial", "target": "Other.q"}],
            "target_is_direct_child": False,
            "verdict": "counterexample",
        }
    }

    assert prototype._language_clause_for_finding(same_region) is None
    receipt = prototype._language_clause_for_finding(cross_region)
    assert receipt is not None
    assert receipt["antecedent_established"] is True
    assert receipt["violation_established"] is True


def test_0029_termination_target_gets_source_grounded_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="FinishState must establish stable termination.",
        claim="FinishState admits a nonterminating continuation.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=5,
        locations=["NL6"],
        proposed_l="L2",
        goal=prototype.EvidenceGoal(
            relation="termination_target",
            subject="HighwayMode.FinishState",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]
    observations = group["execution_certificate"]["observations"]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert observations["root_exit_path"] == []
    assert observations["reachable_cycles_avoiding_root_exit"]
    assert group["source_causality_certificate"]["kind"] == (
        "source_unstable_termination_target"
    )


def test_transition_contract_separates_normative_and_observed_targets() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The cruise exit must reach exit_hwy.",
        claim="The observed cruise exit reaches FinishState.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[4],
        priority=5,
        locations=["NL5", "PUML:L15"],
        proposed_l="L1",
        goal=prototype.EvidenceGoal(
            relation="transition_contract",
            observed_transition_id="tr_0009",
            source="HighwayMode.cruise",
            target="HighwayMode.exit_hwy",
            condition="dist_to_exit<2",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]
    assertion_ir = group["compiled_assertion"]["assertion_ir"]

    assert outcome["candidate"]["goal"]["target"] == "HighwayMode.exit_hwy"
    assert assertion_ir["normative"]["target"] == "HighwayMode.exit_hwy"
    assert assertion_ir["observed"]["target"] == "HighwayMode.FinishState"
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True


def test_transition_contract_derives_exact_condition_from_selected_transition() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The cruise state must leave on the stated exit condition.",
        claim="The selected exit transition loses its condition.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[4],
        priority=5,
        locations=["NL5", "PUML:L15"],
        proposed_l="L1",
        goal=prototype.EvidenceGoal(
            relation="transition_contract",
            observed_transition_id="tr_0009",
            source="HighwayMode.cruise",
            target="HighwayMode.FinishState",
            trigger="dist_to_exit<2",
            # Simulate a model rendering artifact.  The normative condition
            # remains auditable, while execution must use the exact AST label.
            condition="`dist_to_exit<2`",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    assert outcome["candidate"]["goal"]["condition"] == "`dist_to_exit<2`"
    assert outcome["candidate"]["goal"]["trigger"] == "dist_to_exit<2"
    assert not any(
        item["field"] == "trigger" for item in group["compiler_route"]["method_bindings"]
    )


def test_grounded_transition_condition_binding_enables_w2_without_rewriting_normative_text() -> None:
    pair, inspect = _pair_and_inspect("0029")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="HighwayMode.cruise",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="HighwayMode.FinishState",
                        condition="`dist_to_exit<2`",
                        formal_condition="dist_to_exit<2",
                        observed_transition_id="tr_0009",
                    )
                ],
                nl_line=5,
                priority=5,
            )
        ],
    )

    outcome = prototype.execute_contract_extraction_plan(pair, inspect, plan)[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    assert outcome["candidate"]["goal"]["condition"] == "`dist_to_exit<2`"
    assert outcome["candidate"]["goal"]["trigger"] == "dist_to_exit<2"


def test_transition_target_consistency_executes_with_two_exact_transition_ids() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="Both explicitly stated exit behaviors must reach the highway exit.",
        claim="The selected cruise exit has a target inconsistent with the reference exit.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[4],
        priority=5,
        locations=["NL5", "tr_0009", "tr_0011"],
        proposed_l="L1",
        goal=prototype.EvidenceGoal(
            relation="transition_target_consistency",
            observed_transition_id="tr_0009",
            reference_transition_id="tr_0011",
            target="HighwayMode.exit_hwy",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]
    source_certificate = group["source_causality_certificate"]
    execution = group["execution_certificate"]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert source_certificate["kind"] == "source_transition_target_inconsistency"
    assert source_certificate["observed_target"] == "HighwayMode.FinishState"
    assert source_certificate["reference_target"] == "HighwayMode.exit_hwy"
    assert source_certificate["reference_supports_normative_target"] is True
    assert execution["terminal"] is True
    assert execution["observations"]["observed_actual_projection"]["present"] is True
    assert execution["observations"]["observed_normative_projection"]["present"] is False
    assert execution["observations"]["reference_normative_projection"]["present"] is True

    finding = prototype.build_finding_records([outcome])[0]
    assert finding["witness_level"] == "W2"
    assert finding["l_level"] == "L1"
    assert finding["w_validation_errors"] == []
    d_context = prototype.build_d_context(pair, [finding])
    assert '"id":"tr_0009"' in d_context
    assert '"id":"tr_0011"' in d_context
    assert '"reference_transition_id":"tr_0011"' in d_context


def test_transition_target_consistency_with_invalid_reference_degrades() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Two semantically same-role transitions must share a target.",
        claim="The observed transition has the wrong target.",
        observed_fact="Two exact transition bindings were proposed.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[4],
        priority=5,
        locations=["NL5", "tr_0009"],
        proposed_l="L1",
        goal=prototype.EvidenceGoal(
            relation="transition_target_consistency",
            observed_transition_id="tr_0009",
            reference_transition_id="tr_missing",
            target="HighwayMode.exit_hwy",
        ),
    )

    grounded, diagnostics = prototype._validate_direct_grounded_candidate(
        pair, candidate, lane="surface_candidates", index=0
    )
    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[grounded])
    )[0]

    assert diagnostics[0]["class"] == "formal_transition_inconsistent"
    assert grounded.goal.reference_transition_id is None
    assert outcome["probe_groups"][0]["witness_level"] == "W1"
    assert outcome["probe_groups"][0]["execution_certificate"] is None


def test_d_prompt_distinguishes_stable_termination_from_deadlock_finality() -> None:
    assert "`explicit_final=false` is not a defeater" in prototype.D_SYSTEM_PROMPT
    assert "Reserve the exact `explicit_final` rule for" in prototype.D_SYSTEM_PROMPT
    assert "`reachable_deadlock`" in prototype.D_SYSTEM_PROMPT


def test_0029_scope_negative_event_route_executes_to_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="Urban completion must not enter HighwayMode.",
        claim="Urban completion enters the HighwayMode FinishState.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[9],
        priority=5,
        locations=["NL10", "PUML:L43"],
        proposed_l="L2",
        goal=prototype.EvidenceGoal(
            relation="event_avoids_scope",
            observed_transition_id="tr_0026",
            source="UrbanMode",
            forbidden_scope="HighwayMode",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_attribution"]["status"] == "causal_dual_certificate"
    assert group["source_causality_certificate"]["target_ancestor_chain"] == [
        "HighwayMode.FinishState",
        "HighwayMode",
    ]
    assert group["checks"][1]["execution"]["result"] == "false"
    finding = prototype.build_finding_records([outcome])[0]
    assert finding["claims"] == [
        (
            "Source transition 'tr_0026' from 'UrbanMode' to "
            "'HighwayMode.FinishState' enters forbidden scope 'HighwayMode'."
        )
    ]
    assert finding["model_claims"] == [
        "Urban completion enters the HighwayMode FinishState."
    ]


def test_0029_semantically_selected_extraneous_edge_executes_to_w2() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The selected authored completion edge must be absent.",
        claim="The selected completion edge is extraneous.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[5],
        priority=4,
        locations=["NL6", "PUML:L40"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_absent",
            observed_transition_id="tr_0025",
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]
    group = outcome["probe_groups"][0]

    assert outcome["candidate"]["goal"]["expected"] is False
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_causality_certificate"]["kind"] == (
        "source_extraneous_transition"
    )


def test_negative_transition_contract_is_rendered_as_present_but_forbidden() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="One exact authored edge is semantically forbidden.",
        claim="The exact authored edge should be absent.",
        observed_fact="The selected source transition exists.",
        basis_kind="nl_literal",
        nl_quote=pair["nl"].splitlines()[9],
        priority=1,
        locations=["NL10", "tr_0026"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="transition_contract",
            observed_transition_id="tr_0026",
            source="UrbanMode",
            target="HighwayMode.FinishState",
            trigger="auto_finished=true",
            expected=False,
        ),
    )

    outcome = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        ),
    )[0]
    finding = prototype.build_finding_records([outcome])[0]
    certificate = finding["source_causality_certificate"]

    assert certificate["kind"] == "source_extraneous_transition"
    assert certificate["actual"] is True
    assert finding["claims"] == [
        "Exact source transition 'tr_0026' is present but forbidden."
    ]


def test_same_llm_concept_id_cannot_bind_to_two_formal_states() -> None:
    pair, _ = _pair_and_inspect("0029")
    plan = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="HighwayMode.cruise",
                source_concept_id="C-cruise",
                targets=[
                    prototype.ExpectedTransitionTarget(
                        target="HighwayMode.FinishState",
                        target_concept_id="C-exit-highway",
                    )
                ],
                nl_line=5,
                priority=5,
            )
        ],
    )
    bindings = [
        prototype.SemanticConceptBinding(
            concept_id="C-cruise",
            source_state_id="HighwayMode.cruise",
            nl_lines=[5],
        ),
        prototype.SemanticConceptBinding(
            concept_id="C-exit-highway",
            source_state_id="HighwayMode.exit_hwy",
            nl_lines=[4, 5],
        ),
    ]

    grounded, diagnostics = prototype._validate_grounded_contract_plan(
        pair, plan, bindings
    )

    assert grounded.transition_groups == []
    assert diagnostics[0]["class"] == "formal_id_invalid"
    assert "disagrees with C-exit-highway binding" in diagnostics[0]["message"]


def test_concurrency_gate_reads_canonical_ast_not_raw_plantuml_text() -> None:
    pair, _ = _pair_and_inspect("0029")
    pair = {**pair, "plantuml": "@startuml\n--\n@enduml"}

    assert prototype._source_has_concurrent_separator(pair) is False


def test_typed_domain_obligation_lowers_to_compatible_compiler_relation() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected target must be reachable.",
        claim="The selected target is unreachable.",
        observed_fact="The source graph contains no path to the selected target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "reachable",
            "target_ref": "Root.Target",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Target",
        ),
    )

    assert isinstance(candidate.domain_obligation, prototype.GraphObligation)
    assert prototype.validate_domain_obligation_lowering(candidate) == []


def test_typed_target_reachable_alias_lowers_to_same_core_operator() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected target must be reachable.",
        claim="The selected target is unreachable.",
        observed_fact="The source graph contains no path to the selected target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "target_reachable",
            "target_ref": "Root.Target",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Target",
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == []
    assert prototype.validate_operator_executable_soundness(candidate) == []


def test_typed_domain_obligation_mismatch_fails_closed_without_text_rules() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected target must be reachable.",
        claim="The selected target is unreachable.",
        observed_fact="The source graph contains no path to the selected target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "temporal",
            "pattern": "response",
            "trigger_ref": "evt_a",
            "response_ref": "evt_b",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Target",
        ),
    )

    errors = prototype.validate_domain_obligation_lowering(candidate)

    assert len(errors) == 1
    assert "cannot lower" in errors[0]


def test_typed_reference_mismatch_fails_closed_before_compilation() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected target must be reachable.",
        claim="The selected target is unreachable.",
        observed_fact="The source graph contains no path to the selected target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "reachable",
            "target_ref": "Root.Other",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Target",
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == [
        "typed binding target_ref='Root.Other' does not equal lowering binding 'Root.Target'"
    ]


def test_named_termination_target_cannot_lower_to_whole_machine_termination() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Mode M must end when q_end is reached.",
        claim="q_end admits a continuation.",
        observed_fact="The exact source graph contains an inherited exit.",
        basis_kind="nl_literal",
        nl_quote="Mode M ends when q_end is reached.",
        priority=5,
        locations=["NL1", "Root.M.q_end"],
        proposed_l="L2",
        domain_obligation={
            "family": "temporal",
            "pattern": "termination",
            "state_ref": "Root.M.q_end",
        },
        goal=prototype.EvidenceGoal(
            relation="eventually_terminates",
            subject="Root.M.q_end",
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == [
        (
            "typed temporal termination with a named state_ref must lower to "
            "termination_target, not a whole-machine termination relation"
        )
    ]


def test_graph_stable_termination_binds_target_ref_to_goal_subject() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected completion state must terminate stably.",
        claim="The selected completion state admits a continuation.",
        observed_fact="The exact topology contains a continuation from the target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.End"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "stable_termination",
            "target_ref": "Root.End",
        },
        goal=prototype.EvidenceGoal(
            relation="termination_target",
            subject="Root.End",
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == []
    assert prototype.derive_support_disposition(candidate, []).status == "executable"


def test_source_aware_target_reachability_uses_the_bound_source() -> None:
    fcstm = """state Root {
    state Start;
    state Target;
    state Isolated;
    [*] -> Start;
    Start -> Target;
}
"""
    pair = {
        "pair_name": "Root",
        "paths": {"fcstm": "<synthetic.fcstm>", "canonical": "<synthetic.json>"},
        "fcstm": fcstm,
        "canonical": {"model": {}},
        "nl": "",
    }
    inspect = prototype.inspect_fcstm(
        fcstm, pair["paths"]["fcstm"], smt_timeout_ms=3_000
    )
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Target must be reachable from the selected source.",
        claim="Target is unreachable from the selected source.",
        observed_fact="The exact graph has no path from source to target.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Isolated", "Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "reachable",
            "source_ref": "Root.Isolated",
            "target_ref": "Root.Target",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            source="Root.Isolated",
            target="Root.Target",
        ),
    )

    outcome = prototype._execute_evidence_candidate(pair, inspect, candidate, index=1)
    group = outcome["probe_groups"][0]
    observations = group["execution_certificate"]["observations"]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert observations["source"] == "Root.Isolated"
    assert observations["target"] == "Root.Target"
    assert observations["source_target_path"] == []
    assert observations["reachable_from_source"] == ["Root.Isolated"]
    assert observations["query_bound"] is None


def test_bounded_target_reachability_fails_closed_without_bounded_backend() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Target must be reachable from source within two steps.",
        claim="Target is not reachable from source within two steps.",
        observed_fact="A bounded reachability check is required.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Source", "Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "reachable",
            "source_ref": "Root.Source",
            "target_ref": "Root.Target",
            "bound": 2,
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            source="Root.Source",
            target="Root.Target",
            within_cycles=2,
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == []
    outcome = prototype._execute_evidence_candidate({"nl": ""}, {}, candidate, index=1)
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["execution_certificate"] is None
    assert group["compiler_route"]["operation"] == "unsupported_executable_fragment"
    assert group["support_disposition"]["status"] == "located_only"
    assert "bounded trace backend" in group["error"]


def test_forbidden_reachability_fails_closed_on_guard_agnostic_topology() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Target must not be reachable from source.",
        claim="Target is reachable from source.",
        observed_fact="A possible static path is not an executable positive witness.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Source", "Root.Target"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "reachable",
            "source_ref": "Root.Source",
            "target_ref": "Root.Target",
            "expected": False,
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            source="Root.Source",
            target="Root.Target",
            expected=False,
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == []
    support = prototype.derive_support_disposition(candidate, [])

    assert support.status == "located_only"
    assert support.w_ceiling == "W1"


def test_lowering_compatibility_does_not_bypass_operator_soundness_gate() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="The selected state must have an escape.",
        claim="The selected state has no escape.",
        observed_fact="The exact state is localized for an escape check.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Stuck"],
        proposed_l="L2",
        domain_obligation={"family": "graph", "property": "escapable"},
        goal=prototype.EvidenceGoal(
            relation="state_escapable",
            subject="Root.Stuck",
        ),
    )

    assert prototype.validate_domain_obligation_lowering(candidate) == []
    support = prototype.derive_support_disposition(candidate, [])

    assert support.status == "located_only"
    assert support.w_ceiling == "W1"
    assert support.reason_code == "no_sound_lowering"


def test_unlowered_typed_obligation_gets_located_only_support_disposition() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="Every reachable configuration must be free of deadlock.",
        claim="The exact state is a reachable non-final deadlock.",
        observed_fact="The source model localizes the candidate deadlock state.",
        basis_kind="domain_norm",
        priority=5,
        locations=["Root.Concurrent"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "deadlock_free",
            "target_ref": "Root.Concurrent",
        },
        goal=prototype.EvidenceGoal(
            relation="target_reachable",
            target="Root.Concurrent",
        ),
    )

    outcome = prototype._execute_evidence_candidate(
        {"nl": ""}, {}, candidate, index=1
    )
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["execution_certificate"] is None
    assert group["compiler_route"]["operation"] == "invalid_typed_lowering"
    assert group["domain_obligation"]["family"] == "graph"
    assert group["support_disposition"] == {
        "status": "located_only",
        "w_ceiling": "W1",
        "surface_role": "core",
        "reason_code": "no_sound_lowering",
        "reason": "The obligation is localized but has no sound registered lowering.",
    }


def test_deadlock_free_typed_goal_uses_registered_topology_lowering() -> None:
    pair, inspect = _pair_and_inspect("0034")
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A reachable non-final state must admit continuation or termination.",
        claim="Stopping is a reachable deadlock.",
        observed_fact="The verify-enabled inspect frontier reports a reachable deadlock leaf at Stopping.",
        basis_kind="domain_norm",
        nl_quote="transition to the Stopping state when it arrives",
        priority=5,
        locations=["Stopping"],
        proposed_l="L2",
        domain_obligation={
            "family": "graph",
            "property": "deadlock_free",
            "source_ref": "Stopping",
            "expected": True,
        },
        goal=prototype.EvidenceGoal(
            relation="state_escapable",
            subject="Stopping",
            expected=True,
        ),
    )

    outcome = prototype._execute_evidence_candidate(pair, inspect, candidate, index=1)
    group = outcome["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["compiler_route"]["operation"] == "topology_certificate"
    assert group["execution_certificate"]["verdict"] == "counterexample"


def test_surface_roles_separate_core_macro_backend_and_extension() -> None:
    assert prototype.obligation_surface_role(
        prototype.GraphObligation(property="reachable")
    ) == "core"
    assert prototype.obligation_surface_role(
        prototype.GraphObligation(property="stable_termination")
    ) == "derived_macro"
    assert prototype.obligation_surface_role(
        prototype.GuardSetObligation(property="equivalent")
    ) == "backend_comparison"
    assert prototype.obligation_surface_role(
        prototype.AttachmentObligation(attachment="containment")
    ) == "under_supported_extension"


def _action_candidate(*, state: str, action: str | None) -> prototype.EvidenceCandidate:
    return prototype.EvidenceCandidate(
        obligation="The state must execute the exact required entry action.",
        claim="The exact required entry action is absent.",
        basis_kind="nl_literal",
        nl_quote=(
            "In the Approaching substate, the system sends the \"Send\" signal "
            "and continues to approach the destination."
        ),
        priority=5,
        locations=["NL9"],
        proposed_l="L0",
        domain_obligation=prototype.AttachmentObligation(
            attachment="action_phase",
            subject_ref=state,
            action_ref=action,
        ),
        goal=prototype.EvidenceGoal(
            relation="action_exists",
            subject=state,
            phase="entry",
            action=action,
        ),
    )


def test_exact_action_identity_produces_dual_w2_counterexample() -> None:
    pair, inspect = _pair_and_inspect("0034")
    candidate = _action_candidate(state="Approaching", action="Send")

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True
    assert group["source_candidate"] is True
    assert group["execution_certificate"]["verdict"] == "counterexample"
    assert group["source_causality_certificate"]["kind"] == "source_lifecycle_action"
    assert group["source_causality_certificate"]["verdict"] == "counterexample"


def test_action_projection_uses_working_contract_macro_not_text_rewriting() -> None:
    pair, inspect = _pair_and_inspect("0034")
    candidate = _action_candidate(
        state="EmergencyStopping", action="Emergency Stop"
    )
    candidate = candidate.model_copy(
        update={
            "nl_quote": (
                "When an obstacle is detected, the system enters the "
                "EmergencyStopping state, which includes the actions "
                "\"Emergency Stop\" and sends the \"Obstacle Detected\" signal."
            )
        }
    )

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]
    observations = group["execution_certificate"]["observations"]

    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    assert observations["accepted_action_names"] == [
        "Emergency Stop",
        "EmergencyStop",
    ]
    assert observations["working_contract_projection_receipts"][0]["complete"] is True
    assert observations["matching_action_rows"][0]["name"] == "EmergencyStop"


def test_action_exists_without_exact_identity_degrades_to_w1() -> None:
    pair, inspect = _pair_and_inspect("0034")

    group = prototype.execute_evidence_plan(
        pair,
        inspect,
        prototype.EvidencePlan(
            candidates=[_action_candidate(state="Approaching", action=None)]
        ),
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["execution_certificate"] is None
    assert "action_exists requires field(s): action" in group["error"]


def _required_action_contract(
    *, owner: str, concept_id: str, action: str, quote: str
) -> prototype.RequiredActionContract:
    return prototype.RequiredActionContract(
        action_concept=action,
        owner_concept=owner,
        owner_concept_id=concept_id,
        phase="any",
        action_kind="output_signal",
        nl_quote=quote,
        priority=5,
    )


def test_required_action_contract_expands_and_executes_independently() -> None:
    pair, inspect = _pair_and_inspect("0034")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[],
        required_action_contracts=[
            _required_action_contract(
                owner="Approaching",
                concept_id="C-Approaching",
                action="Send",
                quote=(
                    '9. In the Approaching substate, the system sends the "Send" '
                    "signal and continues to approach the destination."
                ),
            ),
            _required_action_contract(
                owner="EmergencyStopping",
                concept_id="C-EmergencyStopping",
                action="Obstacle Detected",
                quote=(
                    "3. When an obstacle is detected, the system enters the "
                    "EmergencyStopping state, which includes the actions "
                    '"Emergency Stop" and sends the "Obstacle Detected" signal.'
                ),
            ),
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-Approaching", source_state_id="Approaching"
            ),
            prototype.CompactConceptBinding(
                concept_id="C-EmergencyStopping",
                source_state_id="EmergencyStopping",
            ),
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    outcomes = prototype.execute_evidence_plan(pair, inspect, evidence)

    assert diagnostics == []
    assert [item.goal.action for item in evidence.surface_candidates] == [
        "Send",
        "Obstacle Detected",
    ]
    assert all(item.goal.phase is None for item in evidence.surface_candidates)
    groups = [outcome["probe_groups"][0] for outcome in outcomes]
    assert all(group["witness_level"] == "W2" for group in groups)
    assert all(group["counterexample_found"] is True for group in groups)
    assert all(
        group["source_attribution"]["status"] == "causal_dual_certificate"
        for group in groups
    )


def test_required_action_contract_accepts_present_action_in_any_phase() -> None:
    pair, inspect = _pair_and_inspect("0034")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[],
        required_action_contracts=[
            _required_action_contract(
                owner="EmergencyStopping",
                concept_id="C-EmergencyStopping",
                action="Emergency Stop",
                quote=(
                    "3. When an obstacle is detected, the system enters the "
                    "EmergencyStopping state, which includes the actions "
                    '"Emergency Stop" and sends the "Obstacle Detected" signal.'
                ),
            )
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-EmergencyStopping",
                source_state_id="EmergencyStopping",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)
    group = prototype.execute_evidence_plan(pair, inspect, evidence)[0][
        "probe_groups"
    ][0]

    assert diagnostics == []
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is False
    assert group["execution_certificate"]["verdict"] == "satisfied"


def test_required_action_veto_and_missing_owner_fail_closed() -> None:
    pair, _ = _pair_and_inspect("0034")
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[],
        required_action_contracts=[
            _required_action_contract(
                owner="Approaching",
                concept_id="C-Approaching",
                action="Send",
                quote=(
                    '9. In the Approaching substate, the system sends the "Send" '
                    "signal and continues to approach the destination."
                ),
            ),
            _required_action_contract(
                owner="EmergencyStopping",
                concept_id="C-EmergencyStopping",
                action="Obstacle Detected",
                quote=(
                    "3. When an obstacle is detected, the system enters the "
                    "EmergencyStopping state, which includes the actions "
                    '"Emergency Stop" and sends the "Obstacle Detected" signal.'
                ),
            ),
        ],
    )
    plan = prototype.DiscoveryGroundingPlan(
        required_action_bindings=[
            prototype.RequiredActionGrounding(
                item_index=0,
                status="rejected",
                reason="The extracted item is a transition trigger, not an action.",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    _, evidence, diagnostics = prototype.validate_discovery_grounding(pair, raw, plan)

    assert evidence.surface_candidates == []
    classes = [item["class"] for item in diagnostics]
    assert "binding_semantically_rejected" in classes
    assert "sparse_concept_binding_missing" in classes


def test_discovery_branch_can_recover_an_omitted_required_action() -> None:
    pair, inspect = _pair_and_inspect("0034")
    added = _required_action_contract(
        owner="Approaching",
        concept_id="C-Approaching",
        action="Send",
        quote=(
            '9. In the Approaching substate, the system sends the "Send" signal '
            "and continues to approach the destination."
        ),
    )
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[], transition_groups=[]
    )
    plan = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-Approaching", source_state_id="Approaching"
            )
        ],
        additional_contracts=prototype.ContractExtractionPlan(
            initial_contracts=[],
            transition_groups=[],
            required_action_contracts=[added],
        ),
        surface_candidates=[],
        behavior_candidates=[],
    )

    grounded, evidence, diagnostics = prototype.validate_discovery_grounding(
        pair, raw, plan
    )
    group = prototype.execute_evidence_plan(pair, inspect, evidence)[0][
        "probe_groups"
    ][0]

    assert diagnostics == []
    assert grounded.required_action_contracts == [added]
    assert evidence.surface_candidates[0].goal.action == "Send"
    assert group["witness_level"] == "W2"
    assert group["counterexample_found"] is True


def test_effect_changed_has_explicit_w1_ceiling_without_execution() -> None:
    pair, inspect = _pair_and_inspect("0029")
    candidate = prototype.EvidenceCandidate(
        obligation="The transition must change the route variable.",
        claim="The transition leaves the route variable unchanged.",
        basis_kind="nl_literal",
        nl_quote="The system starts in the AutonomousMode state.",
        priority=3,
        locations=["NL1"],
        proposed_l="L0",
        goal=prototype.EvidenceGoal(
            relation="effect_exists",
            source=f"{pair['pair_name']}.AutonomousMode",
            trigger=f"{pair['pair_name']}.auto_finished_true",
            variable="R45RouteToken",
            sign="changed",
        ),
    )

    group = prototype.execute_evidence_plan(
        pair, inspect, prototype.EvidencePlan(candidates=[candidate])
    )[0]["probe_groups"][0]

    assert group["witness_level"] == "W1"
    assert group["execution_certificate"] is None
    assert group["compiler_route"]["operation"] == "unsupported_executable_fragment"
    assert "no registered sound runtime operator" in group["error"]
