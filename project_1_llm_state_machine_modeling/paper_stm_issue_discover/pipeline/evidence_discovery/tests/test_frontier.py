from __future__ import annotations

from pathlib import Path

from pipeline.evidence_discovery.inputs import load_pair
from pipeline.evidence_discovery.semantics import (
    CandidateIssue,
    ContractBindingHint,
    FrontierBatch,
    GroundingResponse,
    IdentityNormalizationReceipt,
    NLContract,
    NLContractResponse,
    NLTransitionAlternative,
    NLTransitionGroup,
    SegmentCoverage,
    SemanticBinding,
    canonicalize_grounding_response,
    materialize_segment_coverage,
    materialize_v27_frontier,
)


PAPER_ROOT = Path(__file__).parents[3]
REPORT_ROOT = PAPER_ROOT / "pipeline/representation/reports/llms_emp_r45_java_60"


def _hint(role: str, value: str, segment_id: str) -> ContractBindingHint:
    return ContractBindingHint(
        role=role,
        value=value,
        source_ref=segment_id,
        reason=f"The provider-free fixture binds the exact {role} concept.",
        basis=f"typed {segment_id} fixture",
    )


def _contract(
    *,
    contract_id: str,
    segment_id: str,
    locus_kind: str,
    locus_names: tuple[str, ...],
    property_name: str,
    expected_direction: str,
    violation_direction: str,
    hints: tuple[ContractBindingHint, ...],
    state_role: str | None = None,
) -> NLContract:
    return NLContract(
        contract_id=contract_id,
        segment_id=segment_id,
        quote=f"Provider-free {segment_id} normative clause.",
        normative_statement=f"The typed {property_name} obligation must hold at {locus_names}.",
        locus_kind=locus_kind,
        locus_names=locus_names,
        property=property_name,
        state_role=state_role,
        expected_direction=expected_direction,
        violation_direction=violation_direction,
        evidence_types=("source_identity", "closed_model_inventory"),
        binding_hints=hints,
        scope=f"Typed scope for {locus_names}",
        source_refs=(segment_id,),
        reason="The fixture establishes one atomic normative obligation.",
        basis=f"provider-free {segment_id} typed contract",
    )


def _response(contracts: list[NLContract], groups=None) -> NLContractResponse:
    return NLContractResponse(
        contracts=contracts,
        transition_groups=list(groups or ()),
        segment_disposition={item.segment_id: "covered" for item in contracts},
        reason="The fixture supplies a complete typed contract projection.",
        basis="provider-free frontier contract fixture",
    )


def _keys(batch: FrontierBatch) -> set[tuple[str, tuple[str, ...], str, str]]:
    return {
        (
            item.kind,
            item.candidate.locus_names,
            item.candidate.property,
            item.candidate.violation_direction,
        )
        for item in batch.obligations
    }


def test_0029_frontier_materializes_relational_v27_obligations() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    containment = _contract(
        contract_id="NL-CONTRACT-NL1-CONTAINMENT",
        segment_id="NL1",
        locus_kind="composite",
        locus_names=("InitialState", "AutonomousMode"),
        property_name="containment",
        expected_direction="must_exist",
        violation_direction="wrong_scope",
        hints=(
            _hint("owner", "AutonomousMode", "NL1"),
            _hint("target", "InitialState", "NL1"),
        ),
        state_role="initial_state",
    )
    termination = _contract(
        contract_id="NL-CONTRACT-NL6-TERMINATION",
        segment_id="NL6",
        locus_kind="state",
        locus_names=("FinishState",),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="missing",
        hints=(
            _hint("owner", "HighwayMode", "NL6"),
            _hint("target", "FinishState", "NL6"),
        ),
        state_role="termination_state",
    )
    wrong_scope = _contract(
        contract_id="NL-CONTRACT-NL11-TERMINATION-SCOPE",
        segment_id="NL11",
        locus_kind="state",
        locus_names=("UrbanMode", "FinishState"),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="wrong_scope",
        hints=(
            _hint("owner", "UrbanMode", "NL11"),
            _hint("target", "FinishState", "NL11"),
        ),
        state_role="termination_state",
    )
    cruise = _contract(
        contract_id="NL-CONTRACT-NL3-CRUISE",
        segment_id="NL3",
        locus_kind="transition",
        locus_names=("enter_hwy", "cruise"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "enter_hwy", "NL3"),
            _hint("target", "cruise", "NL3"),
        ),
    )
    lane = _contract(
        contract_id="NL-CONTRACT-NL3-LANE",
        segment_id="NL3",
        locus_kind="transition",
        locus_names=("enter_hwy", "lane_change"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "enter_hwy", "NL3"),
            _hint("target", "lane_change", "NL3"),
        ),
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL3-ALTERNATIVES",
        segment_id="NL3",
        source_name="enter_hwy",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL3-CRUISE",
                target_name="cruise",
                condition="dist_to_front<25",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The first condition selects cruise.",
                basis="provider-free NL3 alternative",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL3-LANE",
                target_name="lane_change",
                condition="extra_lane=true",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The second condition selects lane_change.",
                basis="provider-free NL3 alternative",
            ),
        ),
        source_refs=("NL3",),
        reason="The typed group has one source and two distinct targets.",
        basis="provider-free transition-group fixture",
    )
    response = _response(
        [containment, termination, wrong_scope, cruise, lane], [group]
    )

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    keys = _keys(batch)
    assert (
        "containment",
        ("InitialState", "AutonomousMode"),
        "containment",
        "wrong_scope",
    ) in keys
    assert any(item[0] == "stable_termination" for item in keys)
    assert any(item[0] == "transition_group_collision" for item in keys)
    assert any(item[0] == "wrong_scope_route" for item in keys)


def test_0029_grounding_group_identity_is_canonical_and_consumed() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    cruise = _contract(
        contract_id="NL-CONTRACT-NL3-CRUISE-ENDPOINT",
        segment_id="NL3",
        locus_kind="transition",
        locus_names=("enter_hwy", "cruise"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "enter_hwy", "NL3"),
            _hint("target", "cruise", "NL3"),
        ),
    )
    lane = _contract(
        contract_id="NL-CONTRACT-NL3-LANE-ENDPOINT",
        segment_id="NL3",
        locus_kind="transition",
        locus_names=("enter_hwy", "lane_change"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "enter_hwy", "NL3"),
            _hint("target", "lane_change", "NL3"),
        ),
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-LENS-LOCAL",
        segment_id="NL3",
        source_name="enter_hwy",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-CRUISE-LOCAL",
                target_name="cruise",
                condition="distance condition A",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The first branch selects cruise.",
                basis="provider-free NL3 branch A",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-LANE-LOCAL",
                target_name="lane_change",
                condition="distance condition B",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The second branch selects lane_change.",
                basis="provider-free NL3 branch B",
            ),
        ),
        source_refs=("NL3",),
        reason="Grounding recovers one shared-source alternative relation.",
        basis="provider-free 0029 grounding group",
    )
    first = GroundingResponse(
        lens="contract_structure_contrast",
        additional_transition_groups=[group],
        reason="The structure lens recovers the group.",
        basis="provider-free first lens",
    )
    second = first.model_copy(
        update={
            "lens": "behavior_consequence",
            "additional_transition_groups": [
                group.model_copy(update={"group_id": "NL-GROUP-OTHER-LOCAL"})
            ],
            "reason": "The behavior lens recovers the same group.",
            "basis": "provider-free second lens",
        }
    )
    normalized_first, first_receipts = canonicalize_grounding_response(first)
    normalized_second, second_receipts = canonicalize_grounding_response(second)
    first_group = normalized_first.additional_transition_groups[0]
    second_group = normalized_second.additional_transition_groups[0]

    assert first_group.group_id == second_group.group_id
    assert first_group.group_id != group.group_id
    assert first_receipts[0].canonical_group_id == first_group.group_id
    assert second_receipts[0].canonical_group_id == second_group.group_id

    contracts = _response([cruise, lane])
    batch = materialize_v27_frontier(
        pair,
        contracts,
        {item.contract_id: item for item in contracts.contracts},
        (normalized_first, normalized_second),
        (),
    )
    collisions = [
        item for item in batch.obligations if item.kind == "transition_group_collision"
    ]
    assert len(collisions) == 1
    assert collisions[0].contract.property == "guard_disjointness"


def test_0046_frontier_separates_root_entry_and_reachable_consumers() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    operating = _contract(
        contract_id="NL-CONTRACT-NL2-SEARCHING-ACTION",
        segment_id="NL2",
        locus_kind="state",
        locus_names=("Searching",),
        property_name="state_action",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(_hint("state", "Searching", "NL2"),),
        state_role="operating_state",
    )
    event_contract = _contract(
        contract_id="NL-CONTRACT-NL4-TASK-EVENT",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("Searching", "Attacking"),
        property_name="trigger_set",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "Searching", "NL4"),
            _hint("target", "Attacking", "NL4"),
            _hint("event", "Task_Assignment_Received", "NL4"),
        ),
        state_role="operating_state",
    )
    response = _response([operating, event_contract])

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    keys = _keys(batch)
    assert any(item[0] == "root_reachability" for item in keys)
    assert any(item[0] == "owner_initial_entry" for item in keys)
    assert any(item[0] == "event_consumer_coverage" for item in keys)
    consumer = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "event_consumer_coverage"
    )
    assert consumer.property == "event_consumer_coverage"
    assert consumer.violation_direction == "unconsumed"
    assert "declaration" in consumer.strongest_rebuttal.lower()


def test_frontier_merges_duplicate_typed_candidate_support() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
    contracts = [
        _contract(
            contract_id=f"NL-CONTRACT-NL{index}-PUMP-ACTION",
            segment_id=f"NL{index}",
            locus_kind="state",
            locus_names=("PumpState",),
            property_name="state_action",
            expected_direction="must_exist",
            violation_direction="missing",
            hints=(_hint("state", "PumpState", f"NL{index}"),),
            state_role="operating_state",
        )
        for index in (3, 4)
    ]
    response = _response(contracts)

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in contracts},
        (),
        (),
    )

    dead_ends = [
        item for item in batch.obligations if item.kind == "reachable_dead_end"
    ]
    assert len(dead_ends) == 1
    assert dead_ends[0].source_contract_ids == tuple(
        item.contract_id for item in contracts
    )
    assert any(
        item.kind == "reachable_dead_end" and item.status == "not_applicable"
        for item in batch.checks
    )


def test_0029_wrong_target_requires_exact_semantic_binding() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    contract = _contract(
        contract_id="NL-CONTRACT-NL5-CRUISE-EXIT",
        segment_id="NL5",
        locus_kind="transition",
        locus_names=("cruise", "highway exit"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "cruise", "NL5"),
            _hint("target", "highway exit", "NL5"),
        ),
    )
    expected_target = next(item for item in pair.model.states if item.name == "exit_hwy")
    carrier = next(
        item
        for item in pair.model.transitions
        if item.source == "cruise" and item.target == "FinishState"
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=[
            SemanticBinding(
                binding_id="BIND-NL5-EXIT-TARGET",
                contract_id=contract.contract_id,
                role="target",
                concept_name="highway exit",
                status="exact",
                source_element_ref="HighwayMode.exit_hwy",
                model_element_ref=expected_target.ref,
                carrier_transition_ref=carrier.ref,
                reason="The supplied source inventory uniquely binds the normative exit concept, while the carrier is the exact cruise transition for this clause.",
                basis="NL5, HighwayMode.exit_hwy, and the exact closed cruise transition",
            )
        ],
        reason="The fixture supplies one exact cross-artifact target binding.",
        basis="provider-free SemanticBinding regression",
    )
    response = _response([contract])

    batch = materialize_v27_frontier(
        pair,
        response,
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    issue = next(item.candidate for item in batch.obligations if item.kind == "wrong_target")
    assert issue.locus_names == ("cruise", "exit_hwy")
    assert issue.property == "transition_endpoints"
    assert issue.violation_direction == "wrong_target"
    assert issue.predicate_id is None
    assert set(issue.element_refs) == {
        pair.model.state("cruise").ref,
        expected_target.ref,
        pair.model.state("FinishState").ref,
        carrier.ref,
    }

    no_binding = materialize_v27_frontier(
        pair,
        response,
        {contract.contract_id: contract},
        (),
        (),
    )
    assert all(item.kind != "wrong_target" for item in no_binding.obligations)


def test_0053_frontier_preserves_three_leaf_and_global_properties() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0053")
    contracts = [
        _contract(
            contract_id=f"NL-CONTRACT-NL{index}-{state}-ACTION",
            segment_id=f"NL{index}",
            locus_kind="state",
            locus_names=(state,),
            property_name="state_action",
            expected_direction="must_exist",
            violation_direction="missing",
            hints=(_hint("state", state, f"NL{index}"),),
            state_role="operating_state",
        )
        for index, state in ((3, "PumpState"), (4, "WaterState"), (5, "MethaneState"))
    ]
    contracts.extend(
        [
            _contract(
                contract_id="NL-CONTRACT-NL4-PUMP-WATER",
                segment_id="NL4",
                locus_kind="transition",
                locus_names=("PumpState", "WaterState"),
                property_name="transition_endpoints",
                expected_direction="must_exist",
                violation_direction="missing",
                hints=(
                    _hint("source", "PumpState", "NL4"),
                    _hint("target", "WaterState", "NL4"),
                ),
            ),
            _contract(
                contract_id="NL-CONTRACT-NL5-WATER-METHANE",
                segment_id="NL5",
                locus_kind="transition",
                locus_names=("WaterState", "MethaneState"),
                property_name="transition_endpoints",
                expected_direction="must_exist",
                violation_direction="missing",
                hints=(
                    _hint("source", "WaterState", "NL5"),
                    _hint("target", "MethaneState", "NL5"),
                ),
            ),
        ]
    )
    response = _response(contracts)

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    dead_ends = {
        item.candidate.locus_names[0]
        for item in batch.obligations
        if item.kind == "reachable_dead_end"
    }
    assert dead_ends == {"PumpState", "WaterState", "MethaneState"}
    global_issue = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "cross_wrapper_reachability"
    )
    assert global_issue.locus_names == (
        "PumpState",
        "WaterState",
        "MethaneState",
    )
    assert global_issue.property == "reachability"
    assert global_issue.predicate_id is None


def test_frontier_pydantic_descriptions_reach_json_schema() -> None:
    identity_schema = IdentityNormalizationReceipt.model_json_schema()
    frontier_schema = FrontierBatch.model_json_schema()

    assert "grounding branch-local identity" in identity_schema["description"]
    assert "typed identity" in identity_schema["properties"]["semantic_key"]["description"]
    assert "execute-batch" in frontier_schema["description"]
    assert "candidate" in frontier_schema["properties"]["obligations"]["description"]
    definitions = frontier_schema["$defs"]
    assert set(definitions["FrontierCheckReceipt"]["properties"]["status"]["enum"]) == {
        "candidate",
        "satisfied",
        "unresolved",
        "not_applicable",
    }
    binding_schema = SemanticBinding.model_json_schema()
    assert "跨制品语义绑定" in binding_schema["description"]
    assert set(binding_schema["properties"]["status"]["enum"]) == {
        "exact",
        "ambiguous",
        "unbound",
    }


def test_segment_coverage_is_complete_observable_audit_not_a_gate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0053")
    contract = _contract(
        contract_id="NL-CONTRACT-NL4-PUMP-WATER-COVERAGE",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("PumpState", "WaterState"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("source", "PumpState", "NL4"),
            _hint("target", "WaterState", "NL4"),
        ),
    )
    response = _response([contract])

    normalized = materialize_segment_coverage(
        response, [segment.segment_id for segment in pair.nl_segments]
    )

    assert len(normalized.segment_coverage) == len(pair.nl_segments)
    nl4 = next(item for item in normalized.segment_coverage if item.segment_id == "NL4")
    assert nl4.disposition == "covered"
    assert nl4.semantic_categories == ("transition_endpoint",)
    assert nl4.contract_ids == (contract.contract_id,)
    unreported = next(
        item for item in normalized.segment_coverage if item.segment_id != "NL4"
    )
    assert unreported.disposition == "unreported"
    assert unreported.contract_ids == ()
    assert normalized.contracts == [contract]

    schema = SegmentCoverage.model_json_schema()
    assert "不证明语义完整" in schema["description"]
    assert set(schema["properties"]["disposition"]["enum"]) == {
        "covered",
        "context",
        "ambiguous",
        "unreported",
    }
