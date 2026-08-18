from __future__ import annotations

import json

from project_1_llm_state_machine_modeling.paper_stm_issue_discover.pipeline.witness_search_prototype import (
    graph,
    prototype,
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
        if role != "paper1_d_adjudication":
            raise AssertionError(role)
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n# Deterministic contract feedback", 1)[0]
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
        if role == "paper1_d_adjudication":
            return prototype.DAdjudicationPlan(decisions=[])
        return super().invoke_structured(
            role=role,
            schema=schema,
            system_prompt=system_prompt,
            user_input=user_input,
        )


class InvalidSemanticDResponder(FakeResponder):
    def invoke_structured(self, *, role, schema, system_prompt, user_input):
        if role != "paper1_d_adjudication":
            return super().invoke_structured(
                role=role,
                schema=schema,
                system_prompt=system_prompt,
                user_input=user_input,
            )
        payload = user_input.split("# Findings to adjudicate\n\n", 1)[1]
        payload = payload.split("\n\n# Deterministic contract feedback", 1)[0]
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
        responder.discovery_system_prompts[0]
        != responder.discovery_system_prompts[1]
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


def test_d_contract_failure_repairs_once_then_degrades_to_auditable_output() -> None:
    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        IncompleteDResponder(),
    )

    record = state["final_record"]
    assert record["d_unresolved_reason"]
    assert record["telemetry"]["d_repair_count"] == 2
    assert record["telemetry"]["d_call_count"] == 2
    assert record["confirmed_issues"] == []
    assert record["accepted_issues"] == []
    assert all(item["d_decision"] is None for item in record["finding_records"])


def test_d_semantic_validation_failure_degrades_without_rewriting_valid_decisions() -> None:
    state = graph.run_graph(
        graph.PrototypeGraphInput(case="0016", profile="fake"),
        InvalidSemanticDResponder(),
    )

    record = state["final_record"]
    assert record["d_unresolved_reason"]
    assert record["telemetry"]["d_repair_count"] == 0
    assert record["confirmed_issues"] == []
    assert record["accepted_issues"] == []
    assert all(item["d_status"] == "D_UNRESOLVED" for item in record["finding_records"])


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
