from __future__ import annotations

import json

from paper_stm_feedback_loop.discover.responder import DEFAULT_TRANSPORT_RETRIES

from project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype import (
    graph,
    prototype,
)


def test_all_prototype_entry_points_share_the_provider_retry_default() -> None:
    prototype_args = prototype.build_parser().parse_args(
        ["--case", "0000", "--output-dir", "out"]
    )
    graph_args = graph.build_parser().parse_args(
        ["--case", "0000", "--output-dir", "out"]
    )

    assert DEFAULT_TRANSPORT_RETRIES == 8
    assert prototype_args.transport_retries == DEFAULT_TRANSPORT_RETRIES
    assert graph_args.transport_retries == DEFAULT_TRANSPORT_RETRIES
    assert prototype_args.streaming is None
    assert graph_args.streaming is None
    assert (
        prototype.build_parser()
        .parse_args(["--case", "0000", "--output-dir", "out", "--stream"])
        .streaming
        is True
    )
    assert (
        graph.build_parser()
        .parse_args(["--case", "0000", "--output-dir", "out", "--no-stream"])
        .streaming
        is False
    )


class FakeResponder:
    def __init__(self) -> None:
        self.roles: list[str] = []
        self.discovery_system_prompts: list[str] = []

    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        del schema
        self.roles.append(role)
        if role == "paper1_contract_extraction":
            return prototype.ContractExtractionPlan(
                initial_contracts=[], transition_groups=[]
            )
        if role == "paper1_discovery_grounding":
            self.discovery_system_prompts.append(system_prompt)
            return prototype.DiscoveryGroundingPlan(
                initial_contract_bindings=[],
                containment_contract_bindings=[],
                transition_group_bindings=[],
                surface_candidates=[],
                behavior_candidates=[],
            )
        if role not in {"paper1_d_adjudication", "paper1_d_targeted_repair"}:
            raise AssertionError(role)
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n#", 1)[0]
        findings = json.loads(payload)
        decisions = []
        for finding in findings:
            certificate = finding.get("source_causality_certificate") or {}
            decisions.append(
                prototype.DDecision(
                    finding_key=finding["finding_key"],
                    grounding="lang",
                    violated_obligation="Composite entry must satisfy its entry contract.",
                    language_clause="A declared initial relation has one required target.",
                    supporting_facts=[str(certificate)],
                    strongest_defeater="The relation could be display-only.",
                    defeater_kind="undercutting",
                    defeater_disposition="defeated",
                    rationale="The canonical source records it as an initial relation.",
                    d_subclass="D2-lit",
                    d_level="D2",
                )
            )
        return prototype.DAdjudicationPlan(decisions=decisions)

    def take_last_observation(self):
        return None


class IncompleteDResponder(FakeResponder):
    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role in {"paper1_d_adjudication", "paper1_d_targeted_repair"}:
            self.roles.append(role)
            return prototype.DAdjudicationPlan(decisions=[])
        return super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )


class InvalidSemanticDResponder(FakeResponder):
    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role not in {"paper1_d_adjudication", "paper1_d_targeted_repair"}:
            return super().invoke_structured(
                role=role,
                schema=schema,
                system_prompt=system_prompt,
                user_input=user_input,
            )
        self.roles.append(role)
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n#", 1)[0]
        findings = json.loads(payload)
        return prototype.DAdjudicationPlan(
            decisions=[
                prototype.DDecision(
                    finding_key=finding["finding_key"],
                    grounding="lang",
                    violated_obligation="The source violates an initial-state rule.",
                    strongest_defeater="A tool could interpret the label differently.",
                    defeater_kind="rebutting",
                    defeater_disposition="survives",
                    rationale="This deliberately violates the D1 contract.",
                    d_subclass="not_applicable",
                    d_level="D1",
                )
                for finding in findings
            ]
        )


class TargetedDRepairResponder(FakeResponder):
    def __init__(self) -> None:
        super().__init__()
        self.d_finding_keys: list[list[str]] = []
        self.initial_decisions: dict[str, dict] = {}
        self.targeted_repair_inputs: list[str] = []

    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role not in {"paper1_d_adjudication", "paper1_d_targeted_repair"}:
            return super().invoke_structured(
                role=role,
                schema=schema,
                system_prompt=system_prompt,
                user_input=user_input,
            )
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n#", 1)[0]
        findings = json.loads(payload)
        self.d_finding_keys.append([item["finding_key"] for item in findings])
        if role == "paper1_d_targeted_repair":
            self.targeted_repair_inputs.append(user_input)
        plan = super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )
        if role == "paper1_d_adjudication":
            self.initial_decisions = {
                item.finding_key: item.model_dump(mode="json")
                for item in plan.decisions
            }
            first = plan.decisions[0].model_copy(
                update={
                    "grounding": "lang",
                    "strongest_defeater": "A competing interpretation survives.",
                    "defeater_kind": "rebutting",
                    "defeater_disposition": "survives",
                    "d_subclass": "not_applicable",
                    "d_level": "D1",
                }
            )
            plan = prototype.DAdjudicationPlan(decisions=[first, *plan.decisions[1:]])
        return plan


class InitialDExtraKeyResponder(FakeResponder):
    def __init__(self) -> None:
        super().__init__()
        self.d_finding_keys: list[list[str]] = []

    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role not in {"paper1_d_adjudication", "paper1_d_targeted_repair"}:
            return super().invoke_structured(
                role=role,
                schema=schema,
                system_prompt=system_prompt,
                user_input=user_input,
            )
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n#", 1)[0]
        findings = json.loads(payload)
        self.d_finding_keys.append([item["finding_key"] for item in findings])
        plan = super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )
        if role == "paper1_d_adjudication":
            extra = plan.decisions[0].model_copy(
                update={"finding_key": "unexpected:initial"}
            )
            return prototype.DAdjudicationPlan(decisions=[*plan.decisions, extra])
        return plan


class TargetedDRepairRepeatsFrozenResponder(TargetedDRepairResponder):
    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        plan = super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )
        if role != "paper1_d_targeted_repair":
            return plan
        repair_keys = set(self.d_finding_keys[-1])
        frozen_key = next(
            key for key in self.initial_decisions if key not in repair_keys
        )
        frozen = prototype.DDecision.model_validate(self.initial_decisions[frozen_key])
        return prototype.DAdjudicationPlan(decisions=[*plan.decisions, frozen])


class TargetedDRepairAddsUnknownResponder(TargetedDRepairResponder):
    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        plan = super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )
        if role != "paper1_d_targeted_repair":
            return plan
        extra = plan.decisions[0].model_copy(
            update={"finding_key": "unexpected:repair"}
        )
        return prototype.DAdjudicationPlan(decisions=[*plan.decisions, extra])


class OneSchemaRepairResponder(FakeResponder):
    def __init__(self) -> None:
        super().__init__()
        self.discovery_attempts = 0

    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role == "paper1_discovery_grounding":
            self.discovery_attempts += 1
            if self.discovery_attempts == 1:
                raise graph.StructuredOutputValidationError(
                    "observed_fact field required"
                )
        return super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )


def test_langgraph_runs_progressive_scouts_before_d_adjudication() -> None:
    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        FakeResponder(),
    )

    record = state["final_record"]
    assert record["strategy"] == (
        "shared_a_complementary_dual_b_formal_execution_single_d"
    )
    assert record["telemetry"]["requested_discovery_sample_count"] == 2
    assert record["telemetry"]["completed_discovery_branch_count"] == 2
    assert record["telemetry"]["progressive_seed_count"] == 2
    assert record["telemetry"]["confirmed_issue_count"] == 3
    assert record["telemetry"]["confirmed_report_issue_count"] == 2
    assert (
        len(record["report_issue_clusters"])
        == record["telemetry"]["report_issue_count"]
    )
    assert {item["l_level"] for item in record["confirmed_issues"]} == {"L0", "L1"}
    assert all(
        item["d_decision"]["d_level"] == "D2" for item in record["confirmed_issues"]
    )
    assert record["telemetry"]["token_budget"]["schema"] == (
        "paper1.model_matched_cost.v1"
    )
    assert record["telemetry"]["token_budget"]["raw_token_safety_cap"] == 200_000


def test_schema_error_is_repaired_once_inside_the_same_node() -> None:
    responder = OneSchemaRepairResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    assert state["final_record"].get("status") != "failed"
    assert responder.discovery_attempts == 3


def test_grounding_internal_error_degrades_and_preserves_scout_results(
    monkeypatch,
) -> None:
    def fail_internal_validation(*args, **kwargs):
        del args, kwargs
        raise RuntimeError("merged contract validation failed")

    monkeypatch.setattr(
        prototype, "validate_discovery_grounding", fail_internal_validation
    )

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        FakeResponder(),
    )

    record = state["final_record"]
    assert record.get("status") != "failed"
    assert record["outcomes"]
    assert any(
        item["class"] == "grounding_internal_error"
        for item in record["execution_diagnostics"]
    )


def test_fresh_graph_uses_shared_a_complementary_dual_b_and_single_d() -> None:
    responder = FakeResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    assert state["final_record"].get("status") != "failed"
    assert responder.roles == [
        "paper1_contract_extraction",
        "paper1_discovery_grounding",
        "paper1_discovery_grounding",
        "paper1_d_adjudication",
    ]
    assert len(responder.discovery_system_prompts) == 2
    assert (
        responder.discovery_system_prompts[0] != responder.discovery_system_prompts[1]
    )
    assert "contract_structure_contrast" in responder.discovery_system_prompts[0]
    assert "behavior_consequence" in responder.discovery_system_prompts[1]
    assert state["final_record"]["discovery_branch_lens"] == [
        "contract_structure_contrast",
        "behavior_consequence",
    ]


def test_cross_sample_exact_binding_conflict_is_withheld_without_text_matching() -> (
    None
):
    first = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-mode",
                source_state_id="M.q1",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )
    second = prototype.DiscoveryGroundingPlan(
        concept_bindings=[
            prototype.CompactConceptBinding(
                concept_id="C-mode",
                source_state_id="M.q2",
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    plans, diagnostics = graph._veto_explicit_cross_sample_conflicts([first, second])

    assert all(plan.concept_bindings == [] for plan in plans)
    assert all(plan.unresolved[0].field == "concept_bindings[C-mode]" for plan in plans)
    assert diagnostics[0]["class"] == "cross_sample_formal_binding_conflict"


def test_fresh_transition_binding_contract_is_exhaustive_by_index() -> None:
    raw = prototype.ContractExtractionPlan(
        initial_contracts=[],
        transition_groups=[
            prototype.ExpectedTransitionGroup(
                source="q0",
                targets=[
                    prototype.ExpectedTransitionTarget(target="q1"),
                    prototype.ExpectedTransitionTarget(target="q2"),
                ],
                nl_line=1,
                priority=5,
            )
        ],
    )
    incomplete = prototype.DiscoveryGroundingPlan(
        transition_group_bindings=[
            prototype.TransitionGroupGrounding(
                item_index=0,
                status="grounded",
                source="M.q0",
                targets=[
                    prototype.TransitionTargetGrounding(
                        target_index=0,
                        target="M.q1",
                    )
                ],
            )
        ],
        surface_candidates=[],
        behavior_candidates=[],
    )

    assert graph._fresh_transition_binding_errors(raw, incomplete) == [
        "transition_group[0].targets[1] is missing"
    ]

    complete = incomplete.model_copy(
        deep=True,
        update={
            "transition_group_bindings": [
                prototype.TransitionGroupGrounding(
                    item_index=0,
                    status="grounded",
                    source="M.q0",
                    targets=[
                        prototype.TransitionTargetGrounding(
                            target_index=0,
                            target="M.q1",
                        ),
                        prototype.TransitionTargetGrounding(
                            target_index=1,
                            target="M.q2",
                        ),
                    ],
                )
            ]
        },
    )
    assert graph._fresh_transition_binding_errors(raw, complete) == []


def test_fresh_untyped_candidate_is_quarantined_before_execution() -> None:
    candidate = prototype.BalancedEvidenceCandidate(
        obligation="A required state must exist.",
        claim="The required state is absent.",
        basis_kind="nl_literal",
        nl_quote="The required state exists.",
        priority=5,
        locations=["NL1"],
        proposed_l="L0",
        observed_fact="The exact state inventory does not contain the state.",
        goal=prototype.EvidenceGoal(
            relation="state_exists",
            subject="M.Required",
        ),
    )

    filtered, diagnostics = graph._quarantine_untyped_fresh_evidence(
        prototype.IssueDiscoveryPlan(
            surface_candidates=[candidate], behavior_candidates=[]
        )
    )

    assert filtered.candidates == []
    assert diagnostics == [
        {
            "stage": "discovery_grounding",
            "class": "fresh_typed_obligation_missing",
            "message": (
                "surface_candidates[0] was quarantined because fresh candidates "
                "require a paper-level typed obligation"
            ),
        }
    ]


def test_d_adjudication_covers_all_findings_in_one_call() -> None:
    responder = FakeResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    record = state["final_record"]
    assert record["telemetry"]["finding_count"] > 1
    assert record["telemetry"]["d_call_count"] == 1
    assert responder.roles.count("paper1_d_adjudication") == 1
    assert all(item["d_decision"] is not None for item in record["finding_records"])


def test_initial_d_extra_key_forces_whole_pair_targeted_repair() -> None:
    responder = InitialDExtraKeyResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    record = state["final_record"]
    assert record["telemetry"]["d_call_count"] == 2
    assert record["telemetry"]["d_repair_count"] == 1
    assert responder.roles.count("paper1_d_adjudication") == 1
    assert responder.roles.count("paper1_d_targeted_repair") == 1
    assert len(responder.d_finding_keys) == 2
    assert set(responder.d_finding_keys[1]) == set(responder.d_finding_keys[0])
    assert record.get("d_unresolved_reason") is None
    assert all(item["d_status"] != "D_UNRESOLVED" for item in record["finding_records"])


def test_d_contract_failure_repairs_once_then_degrades_to_auditable_output() -> None:
    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        IncompleteDResponder(),
    )

    record = state["final_record"]
    assert record["d_unresolved_reason"]
    assert record["telemetry"]["d_repair_count"] == 1
    assert record["telemetry"]["d_call_count"] == 2
    assert record["confirmed_issues"] == []
    assert record["accepted_issues"] == []
    assert all(item["d_decision"] is None for item in record["finding_records"])


def test_d_semantic_validation_failure_degrades_without_rewriting_valid_decisions() -> (
    None
):
    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        InvalidSemanticDResponder(),
    )

    record = state["final_record"]
    assert record["d_unresolved_reason"]
    assert record["telemetry"]["d_repair_count"] == 1
    assert record["telemetry"]["d_call_count"] == 2
    assert record["confirmed_issues"] == []
    assert record["accepted_issues"] == []
    assert all(item["d_status"] == "D_UNRESOLVED" for item in record["finding_records"])


def test_d_semantic_repair_sends_only_invalid_subset_and_freezes_valid_decisions() -> (
    None
):
    responder = TargetedDRepairResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    record = state["final_record"]
    assert record["telemetry"]["d_call_count"] == 2
    assert record["telemetry"]["d_repair_count"] == 1
    assert len(responder.d_finding_keys[0]) > 1
    assert len(responder.d_finding_keys[1]) == 1
    repaired_key = responder.d_finding_keys[1][0]
    final_by_key = {
        item["finding_key"]: item["d_decision"] for item in record["finding_records"]
    }
    for finding_key, initial in responder.initial_decisions.items():
        if finding_key != repaired_key:
            assert final_by_key[finding_key] == initial
    assert final_by_key[repaired_key]["d_level"] == "D2"
    assert record.get("d_unresolved_reason") is None
    assert len(responder.targeted_repair_inputs) == 1
    repair_input = responder.targeted_repair_inputs[0]
    assert "# Frozen valid decisions (read-only context)" in repair_input
    for finding_key in responder.initial_decisions:
        if finding_key != repaired_key:
            assert finding_key in repair_input


def test_targeted_d_repair_repeated_frozen_key_does_not_contaminate_frozen_decisions() -> (
    None
):
    responder = TargetedDRepairRepeatsFrozenResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    record = state["final_record"]
    repaired_key = responder.d_finding_keys[1][0]
    final_by_key = {item["finding_key"]: item for item in record["finding_records"]}
    assert record["telemetry"]["d_call_count"] == 2
    assert record["telemetry"]["d_repair_count"] == 1
    assert (
        "targeted repair must not repeat frozen finding_key"
        in record["d_unresolved_reason"]
    )
    assert final_by_key[repaired_key]["d_status"] == "D_UNRESOLVED"
    for finding_key, initial in responder.initial_decisions.items():
        if finding_key != repaired_key:
            assert final_by_key[finding_key]["d_status"] != "D_UNRESOLVED"
            assert final_by_key[finding_key]["d_decision"] == initial


def test_targeted_d_repair_unknown_key_does_not_contaminate_frozen_decisions() -> None:
    responder = TargetedDRepairAddsUnknownResponder()

    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"), responder
    )

    record = state["final_record"]
    repaired_key = responder.d_finding_keys[1][0]
    final_by_key = {item["finding_key"]: item for item in record["finding_records"]}
    assert record["telemetry"]["d_call_count"] == 2
    assert record["telemetry"]["d_repair_count"] == 1
    assert (
        "targeted repair returned unknown finding_key" in record["d_unresolved_reason"]
    )
    assert final_by_key[repaired_key]["d_status"] == "D_UNRESOLVED"
    for finding_key, initial in responder.initial_decisions.items():
        if finding_key != repaired_key:
            assert final_by_key[finding_key]["d_status"] != "D_UNRESOLVED"
            assert final_by_key[finding_key]["d_decision"] == initial


def test_d_duplicate_reference_must_be_known_and_earlier() -> None:
    findings = [{"finding_key": "f:a"}, {"finding_key": "f:b"}]

    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="lit",
            violated_obligation="The same exact obligation is violated.",
            strongest_defeater="A compatible alternative reading remains.",
            defeater_kind="undercutting",
            defeater_disposition="survives",
            rationale="The first reading is grounded but not conclusive.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "The exact source cause and violated property are identical."
                if duplicate_of is not None
                else None
            ),
            d_subclass="not_applicable",
            d_level="D1",
        )

    for invalid_target, expected_error in (
        ("f:b", "duplicate_of must reference an earlier stable finding_key"),
        ("f:unknown", "duplicate_of must reference a supplied finding_key"),
    ):
        valid, invalid, diagnostics = graph._partition_d_decisions(
            findings,
            prototype.DAdjudicationPlan(
                decisions=[decision("f:a", invalid_target), decision("f:b")]
            ),
        )

        assert set(valid) == {"f:b"}
        assert any(expected_error in message for message in invalid["f:a"])
        if invalid_target == "f:b":
            assert any(
                "eligible earlier keys=[]" in message for message in invalid["f:a"]
            )
        assert diagnostics == []


def test_d_duplicate_reference_cannot_merge_distinct_exact_source_causes() -> None:
    findings = [
        {
            "finding_key": "f:a",
            "source_causality_certificate": {
                "kind": "concurrent_region_deadlock",
                "target": "Root.RegionA.Stop",
            },
        },
        {
            "finding_key": "f:b",
            "source_causality_certificate": {
                "kind": "concurrent_region_deadlock",
                "target": "Root.RegionB.Stop",
            },
        },
    ]

    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="lit",
            violated_obligation="The reachable state must admit continuation.",
            strongest_defeater="A compatible alternative remains.",
            defeater_kind="undercutting",
            defeater_disposition="survives",
            rationale="The first reading is grounded but not conclusive.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "The two findings share one concurrent configuration."
                if duplicate_of is not None
                else None
            ),
            d_subclass="not_applicable",
            d_level="D1",
        )

    valid, invalid, diagnostics = graph._partition_d_decisions(
        findings,
        prototype.DAdjudicationPlan(
            decisions=[decision("f:a"), decision("f:b", "f:a")]
        ),
    )

    assert set(valid) == {"f:a"}
    assert invalid["f:b"] == [
        "duplicate_of conflicts with distinct exact source-certificate cause keys"
    ]
    assert diagnostics == []


def test_d_duplicate_reference_cannot_merge_distinct_formal_properties() -> None:
    certificate = {
        "kind": "missing_initial_with_compiler_consequence",
        "target": "Root",
    }
    findings = [
        {
            "finding_key": "f:a",
            "source_causality_certificate": certificate,
            "formal_goals": [
                {
                    "relation": "target_reachable",
                    "target": "Root.Searching",
                    "expected": True,
                }
            ],
        },
        {
            "finding_key": "f:b",
            "source_causality_certificate": certificate,
            "formal_goals": [
                {
                    "relation": "event_reaches_target",
                    "source": "Root.Searching",
                    "trigger": "Intercepted",
                    "target": "Root.FormationAdjustment",
                    "expected": True,
                }
            ],
        },
    ]

    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="lit",
            violated_obligation="A requirement-relative behavior is violated.",
            strongest_defeater="A compatible alternative remains.",
            defeater_kind="undercutting",
            defeater_disposition="survives",
            rationale="The first reading is grounded but not conclusive.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "The source cause is shared." if duplicate_of is not None else None
            ),
            d_subclass="not_applicable",
            d_level="D1",
        )

    valid, invalid, diagnostics = graph._partition_d_decisions(
        findings,
        prototype.DAdjudicationPlan(
            decisions=[decision("f:a"), decision("f:b", "f:a")]
        ),
    )

    assert set(valid) == {"f:a"}
    assert invalid["f:b"] == [
        "duplicate_of conflicts with distinct exact formal property signatures"
    ]
    assert diagnostics == []


def test_weaker_duplicate_cannot_inherit_earlier_d2_impl_receipt() -> None:
    assumptions = {
        "all_regions_have_one_initial": True,
        "all_region_initials_unconditional": True,
        "all_active_targets_leaf": True,
        "all_active_targets_nonfinal": True,
        "entry_path_has_no_guards": True,
        "no_enabled_outgoing": True,
        "owner_identity_resolved_exactly": True,
        "target_is_active_region_entry": True,
    }
    certified_key = "source:concurrent_region_deadlock:Root.A"
    weaker_key = "hypothesis:weaker"
    certificate = {
        "kind": "concurrent_region_deadlock",
        "target": "Root.A",
        "verdict": "counterexample",
        "explicit_final": False,
        "assumptions": assumptions,
    }
    formal_goals = [
        {
            "relation": "state_exists",
            "subject": "Root.A",
            "expected": True,
        }
    ]
    findings = [
        {
            "finding_key": weaker_key,
            "witness_level": "W1",
            "source_causality_certificate": certificate,
            "formal_goals": formal_goals,
        },
        {
            "finding_key": certified_key,
            "witness_level": "W2",
            "source_causality_certificate": certificate,
            "formal_goals": formal_goals,
        },
    ]

    def decision(finding_key: str, duplicate_of: str | None = None):
        return prototype.DDecision(
            finding_key=finding_key,
            grounding="impl",
            violated_obligation="The reachable non-final state must continue.",
            strongest_defeater="The state could be intended terminal.",
            defeater_kind="rebutting",
            defeater_disposition="defeated",
            rationale="The closed deadlock receipt defeats the alternative.",
            duplicate_of=duplicate_of,
            duplicate_rationale=(
                "This is a weaker statement of the same exact certified state."
                if duplicate_of is not None
                else None
            ),
            d_subclass="D2-impl",
            d_level="D2",
        )

    valid, invalid, diagnostics = graph._partition_d_decisions(
        findings,
        prototype.DAdjudicationPlan(
            decisions=[
                decision(certified_key),
                decision(weaker_key, certified_key),
            ]
        ),
    )

    ordered = sorted(findings, key=prototype.d_finding_sort_key)
    assert ordered[0]["finding_key"] == certified_key
    assert set(valid) == {certified_key}
    assert set(invalid) == {weaker_key}
    assert invalid[weaker_key] == [
        (
            "grounding=impl is forbidden because protocol_d2_grounding is null; "
            "use the supplied literal/language/domain provenance or lower D"
        )
    ]
    assert diagnostics == []


def test_replay_loader_can_reuse_plans_from_a_replay_run(tmp_path) -> None:
    prepare = tmp_path / "stages" / "L000-000001-prepare"
    contract_stage = tmp_path / "stages" / "L000-000002-contract-extraction"
    evidence_stage = tmp_path / "stages" / "L000-000003-evidence-planning"
    grounding_stage = tmp_path / "stages" / "L000-000004-semantic-grounding"
    for path in (prepare, contract_stage, evidence_stage, grounding_stage):
        path.mkdir(parents=True)
    contract = prototype.ContractExtractionPlan(
        initial_contracts=[], transition_groups=[]
    )
    evidence = prototype.IssueDiscoveryPlan(
        surface_candidates=[], behavior_candidates=[]
    )
    grounding = prototype.SemanticGroundingPlan(
        contract_plan=contract,
        evidence_bindings=[],
    )
    (prepare / "record.json").write_text(
        json.dumps(
            {
                "contract_plan": contract.model_dump(mode="json"),
                "evidence_plan": evidence.model_dump(mode="json"),
                "llm_observations": [{"usage": {"total_tokens": 7}}],
            }
        ),
        encoding="utf-8",
    )
    (contract_stage / "record.json").write_text(
        json.dumps({"contract_plan": contract.model_dump(mode="json")}),
        encoding="utf-8",
    )
    (evidence_stage / "record.json").write_text(
        json.dumps({"evidence_plan": evidence.model_dump(mode="json")}),
        encoding="utf-8",
    )
    (grounding_stage / "record.json").write_text(
        json.dumps(
            {
                "grounding_plan": grounding.model_dump(mode="json"),
                "llm_observations": [{"usage": {"total_tokens": 7}}],
            }
        ),
        encoding="utf-8",
    )

    loaded_contract, loaded_discoveries, observations = graph._load_replay_plans(
        tmp_path, prototype.load_pair("0016")
    )

    assert loaded_contract == contract
    assert len(loaded_discoveries) == 1
    loaded_discovery = loaded_discoveries[0]
    assert loaded_discovery.additional_contracts == contract
    assert loaded_discovery.evidence_plan == evidence
    assert observations[0]["usage"]["total_tokens"] == 7


def test_replay_loader_preserves_two_independent_discovery_branches(tmp_path) -> None:
    contract_stage = tmp_path / "stages" / "L000-000002-contract-extraction"
    discovery_stage = tmp_path / "stages" / "L000-000003-discovery-grounding"
    contract_stage.mkdir(parents=True)
    discovery_stage.mkdir(parents=True)
    contract = prototype.ContractExtractionPlan(
        initial_contracts=[], transition_groups=[]
    )
    plans = [
        prototype.DiscoveryGroundingPlan(surface_candidates=[], behavior_candidates=[]),
        prototype.DiscoveryGroundingPlan(surface_candidates=[], behavior_candidates=[]),
    ]
    (contract_stage / "record.json").write_text(
        json.dumps({"contract_plan": contract.model_dump(mode="json")}),
        encoding="utf-8",
    )
    (discovery_stage / "record.json").write_text(
        json.dumps(
            {
                "discovery_branches": [
                    {
                        "sample_index": index,
                        "discovery_grounding_plan": plan.model_dump(mode="json"),
                    }
                    for index, plan in enumerate(plans)
                ],
                "llm_observations": [{"usage": {"total_tokens": 11}}],
            }
        ),
        encoding="utf-8",
    )

    loaded_contract, loaded_plans, observations = graph._load_replay_plans(
        tmp_path, prototype.load_pair("0016")
    )

    assert loaded_contract == contract
    assert loaded_plans == plans
    assert observations[0]["usage"]["total_tokens"] == 11


def test_replay_loader_prefers_immutable_llm_outputs_over_ensemble_derivatives(
    tmp_path,
) -> None:
    contract_stage = tmp_path / "stages" / "L000-000002-contract-extraction"
    discovery_stage = tmp_path / "stages" / "L000-000003-discovery-grounding"
    contract_stage.mkdir(parents=True)
    discovery_stage.mkdir(parents=True)
    contract = prototype.ContractExtractionPlan(
        initial_contracts=[], transition_groups=[]
    )
    raw = [
        prototype.DiscoveryGroundingPlan(
            concept_bindings=[
                prototype.CompactConceptBinding(
                    concept_id="C-mode",
                    source_state_id=f"M.q{index}",
                )
            ],
            surface_candidates=[],
            behavior_candidates=[],
        )
        for index in (1, 2)
    ]
    derived = [plan.model_copy(update={"concept_bindings": []}) for plan in raw]
    (contract_stage / "record.json").write_text(
        json.dumps({"contract_plan": contract.model_dump(mode="json")}),
        encoding="utf-8",
    )
    (discovery_stage / "record.json").write_text(
        json.dumps(
            {
                "discovery_branches": [
                    {
                        "sample_index": index,
                        "discovery_grounding_plan": plan.model_dump(mode="json"),
                    }
                    for index, plan in enumerate(derived)
                ],
                "llm_observations": [
                    {
                        "role": "paper1_discovery_grounding",
                        "status": "completed",
                        "parsed_output": plan.model_dump(mode="json"),
                    }
                    for plan in raw
                ],
            }
        ),
        encoding="utf-8",
    )

    _, loaded_plans, _ = graph._load_replay_plans(tmp_path, prototype.load_pair("0016"))

    assert loaded_plans == raw


def test_usage_budget_reports_model_matched_usd_cost(tmp_path) -> None:
    pricing = {
        "prices": {
            "input_usd_per_million_tokens": 5.0,
            "output_usd_per_million_tokens": 25.0,
            "cache_read_usd_per_million_tokens": 0.5,
            "cache_write_usd_per_million_tokens": 6.25,
        },
        "source_url": "https://docs.anthropic.com/en/docs/about-claude/pricing",
        "verified_on": "2026-08-18",
        "basis": "official_list_price",
        "scope_note": "Standard-context list price.",
    }
    baseline_record = tmp_path / "x1v2-opus.json"
    baseline_record.write_text(
        json.dumps(
            {
                "configured_model": "claude-opus-4-7",
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "total_tokens": 120,
                    "cache_read_input_tokens": 0,
                    "cache_creation_input_tokens": 0,
                },
            }
        ),
        encoding="utf-8",
    )
    budget = graph._usage_budget(
        [
            {
                "role": "paper1_contract_extraction",
                "configured_model": "claude-opus-4-7",
                "pricing": pricing,
                "usage": {
                    "input_tokens": 100,
                    "output_tokens": 20,
                    "total_tokens": 120,
                    "cache_read_input_tokens": 40,
                    "cache_creation_input_tokens": 20,
                },
            }
        ],
        max_total_tokens=200,
        matched_x1v2_record=str(baseline_record),
    )

    assert budget["observed_total_tokens"] == 120
    assert budget["eligible"] is True
    assert budget["method_cost"]["total_usd"] == 0.000845
    comparison = budget["model_matched_x1v2_comparison"]
    assert comparison["configured_model"] == "claude-opus-4-7"
    assert comparison["x1v2_cost_usd"] == 0.001
    assert round(comparison["cost_multiplier"], 3) == 0.845
    assert comparison["within_25x"] is True


def test_failure_class_distinguishes_schema_from_provider() -> None:
    schema_observations = [
        {
            "attempts": [
                {
                    "failure_phase": "structured_validation",
                    "retryable": False,
                }
            ]
        },
        {
            "attempts": [
                {
                    "failure_phase": "structured_output_limit",
                    "retryable": False,
                }
            ]
        },
    ]
    provider_observations = [
        {
            "attempts": [
                {
                    "failure_phase": "provider_response",
                    "retryable": True,
                }
            ]
        }
    ]

    assert graph._failure_class_from_observations(schema_observations) == (
        "schema_invalid"
    )
    assert graph._failure_class_from_observations(provider_observations) == (
        "provider_failure"
    )


def test_failure_class_does_not_infer_provider_from_exception_text() -> None:
    observations = [
        {
            "failure": "ValidationError: provider returned a malformed object",
            "attempts": [
                {
                    "failure_phase": "structured_validation",
                    "retryable": False,
                }
            ],
        }
    ]

    assert graph._failure_class_from_observations(observations) == "schema_invalid"
