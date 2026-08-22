from __future__ import annotations

from pathlib import Path

import pytest
from pydantic import ValidationError

from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.evidence.witness_levels import calculate_witness_level
from pipeline.evidence_discovery.inputs import load_pair
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import (
    CandidateIssue,
    CardinalityDomainBinding,
    CardinalityRequirement,
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
    bind_candidate,
    canonicalize_grounding_response,
    materialize_group_containment_contracts,
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
    cardinality_requirement: CardinalityRequirement | None = None,
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
        cardinality_requirement=cardinality_requirement,
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
    assert any(item[0] == "aggregate_stable_termination" for item in keys)
    assert any(item[0] == "transition_group_collision" for item in keys)
    assert any(item[0] == "wrong_scope_route" for item in keys)


def test_transition_endpoint_contract_requires_exact_typed_endpoint_roles() -> None:
    with pytest.raises(
        ValidationError,
        match="requires exactly one source hint and exactly one target hint",
    ):
        _contract(
            contract_id="NL-CONTRACT-NL3-INCOMPLETE-ENDPOINT",
            segment_id="NL3",
            locus_kind="transition",
            locus_names=("enter_hwy", "cruise"),
            property_name="transition_endpoints",
            expected_direction="must_exist",
            violation_direction="missing",
            hints=(_hint("source", "enter_hwy", "NL3"),),
        )

    valid = _contract(
        contract_id="NL-CONTRACT-NL3-COMPLETE-ENDPOINT",
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
    assert [hint.role for hint in valid.binding_hints] == ["source", "target"]

    schema = NLContract.model_json_schema()
    description = schema["properties"]["binding_hints"]["description"]
    assert "property=transition_endpoints" in description
    assert "恰有一个 source" in description


def test_common_owner_group_materializes_complete_containment_contracts() -> None:
    endpoints = [
        _contract(
            contract_id=f"NL-CONTRACT-NL2-ENDPOINT-{target.upper()}",
            segment_id="NL2",
            locus_kind="transition",
            locus_names=("InitialState", target),
            property_name="transition_endpoints",
            expected_direction="must_exist",
            violation_direction="missing",
            hints=(
                _hint("source", "InitialState", "NL2"),
                _hint("target", target, "NL2"),
            ),
        )
        for target in ("HighwayMode", "UrbanMode")
    ]
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL2-AUTONOMOUS-SIBLINGS",
        segment_id="NL2",
        source_name="InitialState",
        common_enclosing_owner_name="AutonomousMode",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL2-HIGHWAY",
                target_name="HighwayMode",
                condition="high_way=true",
                condition_role="qualified_guard",
                reason="The fixture preserves the HighwayMode alternative.",
                basis="provider-free NL2 group",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL2-URBAN",
                target_name="UrbanMode",
                condition="urban_way=true",
                condition_role="qualified_guard",
                reason="The fixture preserves the UrbanMode alternative.",
                basis="provider-free NL2 group",
            ),
        ),
        source_refs=("NL1", "NL2"),
        reason="The LLM fixture establishes one complete sibling group.",
        basis="provider-free common-owner discourse binding",
    )
    response = _response(endpoints, (group,))

    materialized = materialize_group_containment_contracts(response)

    relations = {
        (
            next(h.value for h in item.binding_hints if h.role == "owner"),
            next(h.value for h in item.binding_hints if h.role == "target"),
        )
        for item in materialized.contracts
        if item.property == "containment"
    }
    assert relations == {
        ("AutonomousMode", "InitialState"),
        ("AutonomousMode", "HighwayMode"),
        ("AutonomousMode", "UrbanMode"),
    }
    batch = materialize_v27_frontier(
        load_pair(REPORT_ROOT / "pairs" / "0029"),
        materialized,
        {item.contract_id: item for item in materialized.contracts},
        (),
        (),
    )
    aggregate = next(
        item for item in batch.obligations if item.kind == "aggregate_containment"
    )
    assert aggregate.candidate.locus_names == (
        "AutonomousMode",
        "InitialState",
        "HighwayMode",
        "UrbanMode",
    )

    ownerless = response.model_copy(
        update={
            "transition_groups": [
                group.model_copy(update={"common_enclosing_owner_name": None})
            ]
        }
    )
    assert materialize_group_containment_contracts(ownerless) == ownerless
    incomplete = _response(endpoints[:1], (group,))
    assert materialize_group_containment_contracts(incomplete) == incomplete


def test_containment_frontier_aggregates_only_complete_typed_group_scope() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")

    def containment(
        contract_id: str,
        segment_id: str,
        child: str,
    ) -> NLContract:
        return _contract(
            contract_id=contract_id,
            segment_id=segment_id,
            locus_kind="state",
            locus_names=(child, "AutonomousMode"),
            property_name="containment",
            expected_direction="must_be_contained",
            violation_direction="wrong_scope",
            hints=(
                _hint("owner", "AutonomousMode", segment_id),
                _hint("state", child, segment_id),
            ),
        )

    initial = containment(
        "NL-CONTRACT-NL1-AUTONOMOUS-INITIAL-CONTAINMENT",
        "NL1",
        "InitialState",
    )
    highway = containment(
        "NL-CONTRACT-NL2-AUTONOMOUS-HIGHWAY-CONTAINMENT",
        "NL2",
        "HighwayMode",
    )
    urban = containment(
        "NL-CONTRACT-NL2-AUTONOMOUS-URBAN-CONTAINMENT",
        "NL2",
        "UrbanMode",
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL2-AUTONOMOUS-MODES",
        segment_id="NL2",
        source_name="InitialState",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL2-HIGHWAY-CONTAINMENT",
                target_name="HighwayMode",
                condition="high_way=true",
                condition_role="qualified_guard",
                source_refs=("NL2",),
                reason="The first alternative remains in the enclosing mode.",
                basis="provider-free NL2 HighwayMode alternative",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL2-URBAN-CONTAINMENT",
                target_name="UrbanMode",
                condition="urban_way=true",
                condition_role="qualified_guard",
                source_refs=("NL2",),
                reason="The second alternative remains in the enclosing mode.",
                basis="provider-free NL2 UrbanMode alternative",
            ),
        ),
        source_refs=("NL1", "NL2"),
        reason="The discourse-scoped group enumerates both operating alternatives.",
        basis="provider-free complete containment group",
    )

    complete_contracts = [initial, highway, urban]
    complete = materialize_v27_frontier(
        pair,
        _response(complete_contracts, [group]),
        {item.contract_id: item for item in complete_contracts},
        (),
        (),
    )

    aggregate = next(
        item for item in complete.obligations
        if item.kind == "aggregate_containment"
    )
    assert aggregate.source_contract_ids == tuple(
        item.contract_id for item in complete_contracts
    )
    assert aggregate.candidate.locus_names == (
        "AutonomousMode",
        "InitialState",
        "HighwayMode",
        "UrbanMode",
    )
    assert aggregate.candidate.property == "containment"
    assert aggregate.candidate.violation_direction == "wrong_scope"
    assert aggregate.candidate.predicate_id is None
    assert not any(
        item.kind == "containment" and set(item.source_contract_ids).intersection(
            {contract.contract_id for contract in complete_contracts}
        )
        for item in complete.obligations
    )

    incomplete_contracts = [initial, highway]
    incomplete = materialize_v27_frontier(
        pair,
        _response(incomplete_contracts, [group]),
        {item.contract_id: item for item in incomplete_contracts},
        (),
        (),
    )
    assert not any(
        item.kind == "aggregate_containment" for item in incomplete.obligations
    )
    assert {
        item.source_contract_ids[0]
        for item in incomplete.obligations
        if item.kind == "containment"
    } == {initial.contract_id, highway.contract_id}


def test_0029_frontier_aggregates_complete_same_property_scopes() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    autonomous_entry = _contract(
        contract_id="NL-CONTRACT-NL1-AUTONOMOUS-ENTRY",
        segment_id="NL1",
        locus_kind="composite",
        locus_names=("AutonomousMode", "InitialState"),
        property_name="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        hints=(
            _hint("owner", "AutonomousMode", "NL1"),
            _hint("target", "InitialState", "NL1"),
        ),
        state_role="initial_state",
    )
    highway_entry = _contract(
        contract_id="NL-CONTRACT-NL3-HIGHWAY-ENTRY",
        segment_id="NL3",
        locus_kind="composite",
        locus_names=("HighwayMode", "enter_hwy"),
        property_name="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        hints=(
            _hint("owner", "HighwayMode", "NL3"),
            _hint("target", "enter_hwy", "NL3"),
        ),
        state_role="initial_state",
    )
    urban_entry = _contract(
        contract_id="NL-CONTRACT-NL7-URBAN-ENTRY",
        segment_id="NL7",
        locus_kind="composite",
        locus_names=("UrbanMode", "enter_urban"),
        property_name="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        hints=(
            _hint("owner", "UrbanMode", "NL7"),
            _hint("target", "enter_urban", "NL7"),
        ),
        state_role="initial_state",
    )
    highway_termination = _contract(
        contract_id="NL-CONTRACT-NL6-HIGHWAY-TERMINATION",
        segment_id="NL6",
        locus_kind="scope",
        locus_names=("HighwayMode", "FinishState"),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="not_completed",
        hints=(
            _hint("owner", "HighwayMode", "NL6"),
            _hint("target", "FinishState", "NL6"),
        ),
        state_role="termination_state",
    )
    urban_termination = _contract(
        contract_id="NL-CONTRACT-NL10-URBAN-TERMINATION",
        segment_id="NL10",
        locus_kind="scope",
        locus_names=("UrbanMode", "FinishState"),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="not_completed",
        hints=(
            _hint("owner", "UrbanMode", "NL10"),
            _hint("target", "FinishState", "NL10"),
        ),
        state_role="termination_state",
    )
    contracts = [
        autonomous_entry,
        highway_entry,
        urban_entry,
        highway_termination,
        urban_termination,
    ]
    mode_group = NLTransitionGroup(
        group_id="NL-GROUP-NL2-MODE-ALTERNATIVES",
        segment_id="NL2",
        source_name="InitialState",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL2-HIGHWAY",
                target_name="HighwayMode",
                condition="high_way=true",
                condition_role="qualified_guard",
                source_refs=("NL2",),
                reason="The first alternative selects HighwayMode.",
                basis="provider-free NL2 mode alternative",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL2-URBAN",
                target_name="UrbanMode",
                condition="urban_way=true",
                condition_role="qualified_guard",
                source_refs=("NL2",),
                reason="The second alternative selects UrbanMode.",
                basis="provider-free NL2 mode alternative",
            ),
        ),
        source_refs=("NL2",),
        reason="The typed group enumerates both sibling operating modes.",
        basis="provider-free NL2 transition-group fixture",
    )
    response = _response(contracts, [mode_group])

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in contracts},
        (),
        (),
    )

    initial = next(
        item for item in batch.obligations
        if item.kind == "aggregate_initial_entry"
    )
    assert initial.source_contract_ids == (
        highway_entry.contract_id,
        urban_entry.contract_id,
    )
    assert initial.candidate.locus_names == (
        "HighwayMode",
        "enter_hwy",
        "UrbanMode",
        "enter_urban",
    )
    assert initial.candidate.property == "initial_entry"
    assert initial.candidate.predicate_id is None
    autonomous = next(
        item
        for item in batch.obligations
        if item.kind == "owner_initial_entry"
        and item.source_contract_ids == (autonomous_entry.contract_id,)
    )
    assert autonomous.candidate.locus_names == (
        "AutonomousMode",
        "InitialState",
    )

    termination = next(
        item for item in batch.obligations
        if item.kind == "aggregate_stable_termination"
    )
    assert termination.source_contract_ids == (
        highway_termination.contract_id,
        urban_termination.contract_id,
    )
    assert termination.candidate.locus_names == (
        "HighwayMode",
        "UrbanMode",
        "FinishState",
    )
    assert termination.candidate.property == "termination"
    assert termination.candidate.violation_direction == "not_completed"
    assert termination.candidate.predicate_id is None
    assert not any(
        item.kind == "stable_termination" for item in batch.obligations
    )
    assert {
        highway_entry.contract_id,
        urban_entry.contract_id,
        highway_termination.contract_id,
        urban_termination.contract_id,
    }.issubset(set(batch.superseded_candidate_contract_ids))
    assert autonomous_entry.contract_id not in batch.superseded_candidate_contract_ids

    for index, obligation in enumerate((initial, termination)):
        candidate = obligation.candidate
        contract = obligation.contract
        assert candidate.contract_id == contract.contract_id
        assert candidate.locus_kind == contract.locus_kind
        assert candidate.locus_names == contract.locus_names
        assert candidate.property == contract.property
        assert candidate.violation_direction == contract.violation_direction
        binding = bind_candidate(candidate, pair.model)
        plan = compile_plan(
            candidate,
            binding,
            load_registry(),
            obligation_id=f"0029:r1:aggregate:{index}",
            round_index=1,
            model=pair.model,
            model_hash=pair.hashes["fcstm"],
        )
        receipt = run_backend(
            plan,
            pair.model,
            f"0029:r1:aggregate:{index}:receipt",
        )
        assert binding.precise is True
        assert plan.predicate_id is None
        assert plan.supported is False
        assert calculate_witness_level(binding, plan, receipt) == "W1"


def test_initial_entry_frontier_keeps_one_violation_atomic() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    contract = _contract(
        contract_id="NL-CONTRACT-NL3-HIGHWAY-ENTRY-ONLY",
        segment_id="NL3",
        locus_kind="composite",
        locus_names=("HighwayMode", "enter_hwy"),
        property_name="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        hints=(
            _hint("owner", "HighwayMode", "NL3"),
            _hint("target", "enter_hwy", "NL3"),
        ),
        state_role="initial_state",
    )

    batch = materialize_v27_frontier(
        pair,
        _response([contract]),
        {contract.contract_id: contract},
        (),
        (),
    )

    initial = [item for item in batch.obligations if "initial_entry" in item.kind]
    assert len(initial) == 1
    assert initial[0].kind == "owner_initial_entry"
    assert initial[0].source_contract_ids == (contract.contract_id,)
    assert contract.contract_id not in batch.superseded_candidate_contract_ids


def test_initial_entry_frontier_does_not_aggregate_duplicate_same_owner() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    contracts = [
        _contract(
            contract_id=f"NL-CONTRACT-NL3-HIGHWAY-ENTRY-{suffix}",
            segment_id="NL3",
            locus_kind="composite",
            locus_names=("HighwayMode", "enter_hwy"),
            property_name="initial_entry",
            expected_direction="must_enter",
            violation_direction="missing",
            hints=(
                _hint("owner", "HighwayMode", "NL3"),
                _hint("target", "enter_hwy", "NL3"),
            ),
            state_role="initial_state",
        )
        for suffix in ("A", "B")
    ]

    batch = materialize_v27_frontier(
        pair,
        _response(contracts),
        {item.contract_id: item for item in contracts},
        (),
        (),
    )

    initial = [item for item in batch.obligations if "initial_entry" in item.kind]
    assert len(initial) == 1
    assert initial[0].kind == "owner_initial_entry"
    assert initial[0].source_contract_ids == tuple(
        item.contract_id for item in contracts
    )
    assert not batch.superseded_candidate_contract_ids


def test_termination_frontier_does_not_aggregate_different_targets() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    contracts = [
        _contract(
            contract_id="NL-CONTRACT-NL6-HIGHWAY-FINISH",
            segment_id="NL6",
            locus_kind="scope",
            locus_names=("HighwayMode", "FinishState"),
            property_name="termination",
            expected_direction="must_terminate",
            violation_direction="not_completed",
            hints=(
                _hint("owner", "HighwayMode", "NL6"),
                _hint("target", "FinishState", "NL6"),
            ),
            state_role="termination_state",
        ),
        _contract(
            contract_id="NL-CONTRACT-NL8-URBAN-EXIT",
            segment_id="NL8",
            locus_kind="scope",
            locus_names=("UrbanMode", "exit_urban"),
            property_name="termination",
            expected_direction="must_terminate",
            violation_direction="not_completed",
            hints=(
                _hint("owner", "UrbanMode", "NL8"),
                _hint("target", "exit_urban", "NL8"),
            ),
            state_role="termination_state",
        ),
    ]

    batch = materialize_v27_frontier(
        pair,
        _response(contracts),
        {item.contract_id: item for item in contracts},
        (),
        (),
    )

    stable = [
        item for item in batch.obligations if "stable_termination" in item.kind
    ]
    assert len(stable) == 2
    assert {item.kind for item in stable} == {"stable_termination"}
    assert {item.candidate.locus_names for item in stable} == {
        ("HighwayMode", "FinishState"),
        ("UrbanMode", "exit_urban"),
    }


def test_termination_frontier_keeps_ownerless_contract_outside_aggregate() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    ownerless = _contract(
        contract_id="NL-CONTRACT-NL6-GLOBAL-FINISH",
        segment_id="NL6",
        locus_kind="state",
        locus_names=("FinishState",),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="not_completed",
        hints=(_hint("target", "FinishState", "NL6"),),
        state_role="termination_state",
    )
    owned = [
        _contract(
            contract_id=f"NL-CONTRACT-{segment}-{owner.upper()}-FINISH",
            segment_id=segment,
            locus_kind="scope",
            locus_names=(owner, "FinishState"),
            property_name="termination",
            expected_direction="must_terminate",
            violation_direction="not_completed",
            hints=(
                _hint("owner", owner, segment),
                _hint("target", "FinishState", segment),
            ),
            state_role="termination_state",
        )
        for segment, owner in (("NL6", "HighwayMode"), ("NL10", "UrbanMode"))
    ]
    contracts = [ownerless, *owned]

    batch = materialize_v27_frontier(
        pair,
        _response(contracts),
        {item.contract_id: item for item in contracts},
        (),
        (),
    )

    stable = [
        item for item in batch.obligations if "stable_termination" in item.kind
    ]
    assert len(stable) == 2
    atomic = next(item for item in stable if item.kind == "stable_termination")
    aggregate = next(
        item for item in stable if item.kind == "aggregate_stable_termination"
    )
    assert atomic.source_contract_ids == (ownerless.contract_id,)
    assert aggregate.source_contract_ids == tuple(
        item.contract_id for item in owned
    )
    assert ownerless.contract_id not in batch.superseded_candidate_contract_ids


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


def test_0029_group_frontier_resolves_composite_source_through_typed_entry() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    initial_entry = _contract(
        contract_id="NL-CONTRACT-NL3-INITIAL",
        segment_id="NL3",
        locus_kind="composite",
        locus_names=("HighwayMode", "enter_hwy"),
        property_name="initial_entry",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(
            _hint("owner", "HighwayMode", "NL3"),
            _hint("target", "enter_hwy", "NL3"),
        ),
        state_role="initial_state",
    )
    relation = _contract(
        contract_id="NL-CONTRACT-NL3-ALTERNATIVES",
        segment_id="NL3",
        locus_kind="transition",
        locus_names=("HighwayMode", "cruise", "lane_change"),
        property_name="other",
        expected_direction="must_cover",
        violation_direction="missing",
        hints=(
            _hint("scope", "HighwayMode", "NL3"),
            _hint("target", "cruise", "NL3"),
            _hint("target", "lane_change", "NL3"),
        ),
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL3-COMPOSITE-SOURCE",
        segment_id="NL3",
        source_name="HighwayMode",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL3-CRUISE",
                target_name="cruise",
                condition="dist_to_front<25 and extra_lane=true",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The first branch targets cruise.",
                basis="provider-free NL3 alternative",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL3-LANE",
                target_name="lane_change",
                condition="dist_to_front<25 and extra_lane=true",
                condition_role="qualified_guard",
                source_refs=("NL3",),
                reason="The second branch targets lane_change.",
                basis="provider-free NL3 alternative",
            ),
        ),
        source_refs=("NL3",),
        reason="The capability clause is stated at composite scope.",
        basis="provider-free composite-source transition group",
    )
    response = _response([initial_entry, relation], [group])

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    collision = next(
        item for item in batch.obligations if item.kind == "transition_group_collision"
    )
    assert collision.candidate.locus_names == (
        "enter_hwy",
        "cruise",
        "lane_change",
    )
    assert collision.candidate.property == "guard_disjointness"


def test_transition_group_frontier_rejects_distinct_exact_signatures() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    cruise = _contract(
        contract_id="NL-CONTRACT-NL4-CRUISE",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("lane_change", "cruise"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "lane_change", "NL4"),
            _hint("target", "cruise", "NL4"),
        ),
    )
    exit_hwy = _contract(
        contract_id="NL-CONTRACT-NL4-EXIT",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("lane_change", "exit_hwy"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "lane_change", "NL4"),
            _hint("target", "exit_hwy", "NL4"),
        ),
    )
    group = NLTransitionGroup(
        group_id="NL-GROUP-NL4-DISTINCT",
        segment_id="NL4",
        source_name="lane_change",
        alternatives=(
            NLTransitionAlternative(
                alternative_id="ALT-NL4-CRUISE",
                target_name="cruise",
                condition="lane_change_completed",
                condition_role="qualified_guard",
                source_refs=("NL4",),
                reason="Completion selects cruise.",
                basis="provider-free distinct-signature fixture",
            ),
            NLTransitionAlternative(
                alternative_id="ALT-NL4-EXIT",
                target_name="exit_hwy",
                condition="dist_to_exit<2",
                condition_role="qualified_guard",
                source_refs=("NL4",),
                reason="Exit distance selects exit_hwy.",
                basis="provider-free distinct-signature fixture",
            ),
        ),
        source_refs=("NL4",),
        reason="The alternatives have distinct conditions and targets.",
        basis="provider-free negative transition-group fixture",
    )
    response = _response([cruise, exit_hwy], [group])

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    assert all(
        item.kind != "transition_group_collision" for item in batch.obligations
    )


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
    owner_entry = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "owner_initial_entry"
    )
    assert owner_entry.locus_names == ("UAVSwarmStateMachine", "SearchRegion")
    assert any(ref.endswith("puml:line:2") for ref in owner_entry.source_refs)
    assert "MissionRegion" in owner_entry.observed
    consumer = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "event_consumer_coverage"
    )
    assert consumer.property == "event_consumer_coverage"
    assert consumer.violation_direction == "unconsumed"
    assert "declaration" in consumer.strongest_rebuttal.lower()


def test_0046_continuous_action_survives_same_segment_cardinality() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    cardinality = _0046_cardinality_contract()
    continuous_action = _contract(
        contract_id="NL-CONTRACT-NL2-CONTINUOUS-SEARCH",
        segment_id="NL2",
        locus_kind="state",
        locus_names=("Searching",),
        property_name="state_action",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(_hint("state", "Searching", "NL2"),),
        state_role="operating_state",
    )
    response = _response([cardinality, continuous_action])
    grounding = _0046_cardinality_binding(cardinality)

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (grounding,),
        (),
    )

    assert {item.property for item in response.contracts} == {
        "cardinality",
        "state_action",
    }
    assert any(item.kind == "cardinality" for item in batch.obligations)
    assert any(item.kind == "root_reachability" for item in batch.obligations)
    assert any(item.kind == "owner_initial_entry" for item in batch.obligations)


def test_0046_frontier_does_not_invent_owner_entry_without_operating_obligation() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    contextual = _contract(
        contract_id="NL-CONTRACT-NL2-SEARCHING-CONTEXT",
        segment_id="NL2",
        locus_kind="state",
        locus_names=("Searching",),
        property_name="element_declaration",
        expected_direction="must_exist",
        violation_direction="missing",
        hints=(_hint("state", "Searching", "NL2"),),
        state_role="condition_state",
    )
    response = _response([contextual])

    batch = materialize_v27_frontier(
        pair,
        response,
        {contextual.contract_id: contextual},
        (),
        (),
    )

    assert all(item.kind != "owner_initial_entry" for item in batch.obligations)


def _0046_cardinality_contract(
    member_domain: str = "direct_child_states",
) -> NLContract:
    return _contract(
        contract_id="NL-CONTRACT-NL2-THREE-AREAS",
        segment_id="NL2",
        locus_kind="scope",
        locus_names=("UAV swarm", "three different state areas"),
        property_name="cardinality",
        expected_direction="must_cover",
        violation_direction="missing",
        hints=(
            _hint("owner", "UAVSwarmStateMachine", "NL2"),
            _hint("scope", "three different state areas", "NL2"),
        ),
        state_role="operating_state",
        cardinality_requirement=CardinalityRequirement(
            required_count=3,
            member_domain=member_domain,
            scope_concept="UAV swarm state machine",
            member_concept="different state areas",
            alternative_reading=(
                "The phrase may denote three named operating states rather than direct structural child areas."
                if member_domain != "unresolved"
                else "The supplied clause admits direct-child and operating-state readings without selecting one."
            ),
            reason="The numbered clause gives a literal count and preserves its competing member-domain reading.",
            basis="provider-free NL2 cardinality fixture",
        ),
    )


def test_0046_frontier_compares_typed_three_area_requirement_with_exact_two_children() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    contract = _0046_cardinality_contract()
    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Three-area structure requires exact comparison",
        requirement_quote=contract.quote,
        element_refs=[
            pair.model.state("UAVSwarmStateMachine").ref,
            pair.model.state("SearchRegion").ref,
            pair.model.state("MissionRegion").ref,
        ],
        source_refs=["NL2"],
        expected="The authored operating scope must provide three direct state areas.",
        observed="Exact refs bind the owner and its supplied direct children.",
        strongest_rebuttal="The member domain may have another competent reading.",
        reason="The fixture exposes exact owner/member refs without parsing prose.",
        basis="provider-free 0046 cardinality binding fixture",
    )
    response = _response([contract])

    batch = materialize_v27_frontier(
        pair,
        response,
        {contract.contract_id: contract},
        (),
        (candidate,),
    )

    issue = next(
        item.candidate for item in batch.obligations if item.kind == "cardinality"
    )
    assert issue.locus_names == ("UAVSwarmStateMachine",)
    assert issue.property == "cardinality"
    assert issue.predicate_id is None
    assert contract.scope in issue.expected
    assert "primary direct-child reading has 2" in issue.observed
    assert "three named operating states" in issue.strongest_rebuttal
    assert batch.superseded_candidate_contract_ids == (contract.contract_id,)


def test_cardinality_frontier_keeps_unresolved_member_domain_unresolved() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    contract = _0046_cardinality_contract("unresolved")
    response = _response([contract])

    batch = materialize_v27_frontier(
        pair,
        response,
        {contract.contract_id: contract},
        (),
        (),
    )

    assert all(item.kind != "cardinality" for item in batch.obligations)
    receipt = next(item for item in batch.checks if item.kind == "cardinality")
    assert receipt.status == "unresolved"
    assert "no free-text or name-shape fallback" in receipt.basis


def _0046_cardinality_binding(
    contract: NLContract,
    *,
    lens: str = "contract_structure_contrast",
    member_domain: str = "direct_child_states",
    additional_contracts: tuple[NLContract, ...] = (),
) -> GroundingResponse:
    return GroundingResponse(
        lens=lens,
        additional_contracts=list(additional_contracts),
        cardinality_bindings=[
            CardinalityDomainBinding(
                binding_id=f"CARD-BIND-{lens}",
                contract_id=contract.contract_id,
                status="exact",
                member_domain=member_domain,
                owner_source_id="UAVSwarmStateMachine",
                owner_model_ref="state:UAVSwarmStateMachine:line:10",
                alternative_reading=(
                    "The clause may instead count named operating states; that competent reading remains for D."
                ),
                reason="The supplied source semantics select one primary structural member domain without using its observed count.",
                basis="provider-free NL2 plus exact source owner/member inventory and ModelIR owner ref",
            )
        ],
        reason="The fixture supplies one typed cardinality domain binding.",
        basis="provider-free grounding response",
    )


def test_0046_grounding_binding_closes_unresolved_cardinality_domain() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    contract = _0046_cardinality_contract("unresolved")
    grounding = _0046_cardinality_binding(contract)

    batch = materialize_v27_frontier(
        pair,
        _response([contract]),
        {contract.contract_id: contract},
        (grounding,),
        (),
    )

    obligation = next(item for item in batch.obligations if item.kind == "cardinality")
    assert obligation.candidate.locus_names == ("UAVSwarmStateMachine",)
    assert contract.scope in obligation.candidate.expected
    assert "primary direct-child reading has 2" in obligation.candidate.observed
    assert obligation.contract.cardinality_requirement is not None
    assert (
        obligation.contract.cardinality_requirement.member_domain
        == "direct_child_states"
    )
    assert "named operating states" in obligation.candidate.strongest_rebuttal
    assert contract.contract_id in batch.superseded_candidate_contract_ids


def test_cardinality_frontier_refuses_conflicting_exact_domain_bindings() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0046")
    contract = _0046_cardinality_contract("unresolved")
    structure = _0046_cardinality_binding(contract)
    named_members = _0046_cardinality_binding(
        contract,
        lens="behavior_consequence",
        member_domain="explicit_named_members",
    )

    batch = materialize_v27_frontier(
        pair,
        _response([contract]),
        {contract.contract_id: contract},
        (structure, named_members),
        (),
    )

    assert all(item.kind != "cardinality" for item in batch.obligations)
    receipt = next(item for item in batch.checks if item.kind == "cardinality")
    assert receipt.status == "unresolved"
    assert "conflicting exact cardinality domains" in receipt.reason


def test_cardinality_binding_follows_runner_canonical_contract_identity() -> None:
    raw_contract = _0046_cardinality_contract("unresolved").model_copy(
        update={
            "contract_id": (
                "NL-CONTRACT-NL2-DERIVED-contract_structure_contrast-CARDINALITY"
            )
        }
    )
    raw_response = _0046_cardinality_binding(
        raw_contract,
        additional_contracts=(raw_contract,),
    )

    normalized, receipts = canonicalize_grounding_response(raw_response)

    canonical_id = normalized.additional_contracts[0].contract_id
    assert canonical_id != raw_contract.contract_id
    assert normalized.cardinality_bindings[0].contract_id == canonical_id
    identity_receipt = next(
        item for item in receipts if isinstance(item, IdentityNormalizationReceipt)
    )
    assert identity_receipt.rewritten_cardinality_binding_count == 1


def test_derived_candidate_identity_is_projected_from_authoritative_contract() -> None:
    contract = _contract(
        contract_id="NL-CONTRACT-NL2-DERIVED-behavior_consequence-CONSUMERS",
        segment_id="NL2",
        locus_kind="scope",
        locus_names=("target search task response consumers",),
        property_name="event_consumer_coverage",
        expected_direction="must_cover",
        violation_direction="unconsumed",
        hints=(_hint("scope", "target search operation", "NL2"),),
        state_role="operating_state",
    )
    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=("target search response consumers",),
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Declared consumers are unreachable",
        requirement_quote=contract.quote,
        element_refs=["state:Searching:line:13"],
        source_refs=["NL2"],
        expected="Required event consumers must be reachable.",
        observed="The exact reachable consumer set is empty.",
        strongest_rebuttal="Declaration-only existence is a weaker property.",
        reason="The candidate evaluates the referenced derived contract.",
        basis="provider-free consumer identity fixture",
    )
    with pytest.raises(
        ValidationError, match="branch-local contract reference closure failed"
    ):
        GroundingResponse(
            lens="behavior_consequence",
            candidates=[candidate],
            reason="The malformed fixture omits its branch-local contract row.",
            basis="provider-free dangling derived reference fixture",
        )
    response = GroundingResponse(
        lens="behavior_consequence",
        additional_contracts=[contract],
        candidates=[candidate],
        reason="The fixture returns one derived consumer contract and candidate.",
        basis="provider-free derived identity normalization",
    )

    normalized, receipts = canonicalize_grounding_response(response)

    assert normalized.candidates[0].contract_id == normalized.additional_contracts[0].contract_id
    assert normalized.candidates[0].locus_names == contract.locus_names
    receipt = next(item for item in receipts if isinstance(item, IdentityNormalizationReceipt))
    assert receipt.projected_candidate_identity_count == 1


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


def test_0029_wrong_target_reuses_unique_exact_target_concept_binding() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    lane_exit = _contract(
        contract_id="NL-CONTRACT-NL4-LANE-EXIT",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("lane_change", "highway exit"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "lane_change", "NL4"),
            _hint("target", "highway exit", "NL4"),
        ),
    )
    cruise_exit = _contract(
        contract_id="NL-CONTRACT-NL5-CRUISE-EXIT",
        segment_id="NL5",
        locus_kind="transition",
        locus_names=("cruise", "highway exit"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "cruise", "NL5"),
            _hint("target", "highway exit", "NL5"),
        ),
    )
    expected_target = pair.model.state("exit_hwy")
    assert expected_target is not None
    lane_carrier = next(
        item
        for item in pair.model.transitions
        if item.source == "lane_change" and item.target == "exit_hwy"
    )
    grounding = GroundingResponse(
        lens="contract_structure_contrast",
        semantic_bindings=[
            SemanticBinding(
                binding_id="BIND-NL4-HIGHWAY-EXIT",
                contract_id=lane_exit.contract_id,
                role="target",
                concept_name="highway exit",
                status="exact",
                source_element_ref="source:state:HighwayMode.exit_hwy",
                model_element_ref=expected_target.ref,
                carrier_transition_ref=lane_carrier.ref,
                reason="The exact source inventory binds the highway-exit concept to exit_hwy.",
                basis="NL4 and exact source/model exit_hwy identity",
            )
        ],
        reason="The fixture provides one unique typed target-concept binding.",
        basis="provider-free cross-contract target binding",
    )
    groups = [
        NLTransitionGroup(
            group_id=f"NL-GROUP-{segment}-EXIT",
            segment_id=segment,
            source_name=source,
            alternatives=(
                NLTransitionAlternative(
                    alternative_id=f"ALT-{segment}-EXIT",
                    target_name="highway exit",
                    condition="dist_to_exit<2",
                    condition_role="qualified_guard",
                    reason="The exact exit condition belongs to this alternative.",
                    basis=f"provider-free {segment} transition group",
                ),
            ),
            reason="The fixture keeps the carrier condition in the typed group.",
            basis=f"provider-free {segment} relation",
        )
        for segment, source in (("NL4", "lane_change"), ("NL5", "cruise"))
    ]
    response = _response([lane_exit, cruise_exit], groups)

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (grounding,),
        (),
    )

    wrong_targets = [
        item for item in batch.obligations if item.kind == "wrong_target"
    ]
    assert len(wrong_targets) == 1
    issue = wrong_targets[0].candidate
    assert issue.contract_id == cruise_exit.contract_id
    assert issue.locus_names == ("cruise", "highway exit")
    assert pair.model.state("FinishState").ref in issue.element_refs
    assert any(ref.endswith("puml:line:15") for ref in issue.source_refs)


def test_0029_wrong_target_materializes_from_exact_cross_contract_roles() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0029")
    lane_exit = _contract(
        contract_id="NL-CONTRACT-NL4-LANE-EXIT",
        segment_id="NL4",
        locus_kind="transition",
        locus_names=("lane_change", "highway exit"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "lane_change", "NL4"),
            _hint("target", "highway exit", "NL4"),
            _hint("guard", "dist_to_exit<2", "NL4"),
        ),
    )
    cruise_exit = _contract(
        contract_id="NL-CONTRACT-NL5-CRUISE-EXIT",
        segment_id="NL5",
        locus_kind="transition",
        locus_names=("cruise", "highway exit"),
        property_name="transition_endpoints",
        expected_direction="must_exist",
        violation_direction="wrong_target",
        hints=(
            _hint("source", "cruise", "NL5"),
            _hint("target", "highway exit", "NL5"),
            _hint("guard", "dist_to_exit<2", "NL5"),
        ),
    )
    termination = _contract(
        contract_id="NL-CONTRACT-NL6-TERMINATION",
        segment_id="NL6",
        locus_kind="state",
        locus_names=("HighwayMode", "FinishState"),
        property_name="termination",
        expected_direction="must_terminate",
        violation_direction="missing",
        hints=(
            _hint("owner", "HighwayMode", "NL6"),
            _hint("target", "FinishState", "NL6"),
        ),
        state_role="termination_state",
    )
    response = _response([lane_exit, cruise_exit, termination])

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    wrong_targets = [
        item for item in batch.obligations if item.kind == "wrong_target"
    ]
    assert len(wrong_targets) == 1
    obligation = wrong_targets[0]
    assert obligation.candidate.contract_id == cruise_exit.contract_id
    assert obligation.candidate.locus_names == ("cruise", "highway exit")
    assert set(obligation.source_contract_ids) == {
        lane_exit.contract_id,
        cruise_exit.contract_id,
        termination.contract_id,
    }
    assert "FinishState" in obligation.candidate.observed
    assert pair.model.state("exit_hwy").ref in obligation.candidate.element_refs


def test_0053_frontier_preserves_three_leaf_and_global_properties() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0053")
    owner_entry_contract = _contract(
        contract_id="NL-CONTRACT-NL3-PUMPCONTROL-ENTRY",
        segment_id="NL3",
        locus_kind="composite",
        locus_names=("PumpControl", "PumpState"),
        property_name="initial_entry",
        expected_direction="must_enter",
        violation_direction="missing",
        hints=(
            _hint("owner", "PumpControl", "NL3"),
            _hint("target", "PumpState", "NL3"),
        ),
        state_role="initial_state",
    )
    contracts = [owner_entry_contract]
    contracts.extend(
        [
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
            for index, state in (
                (3, "PumpState"),
                (4, "WaterState"),
                (5, "MethaneState"),
            )
        ]
    )
    contracts.extend(
        [
            _contract(
                contract_id="NL-CONTRACT-NL4-PUMP-WATER",
                segment_id="NL4",
                locus_kind="transition",
                locus_names=("PumpState", "WaterState"),
                property_name="transition_endpoints",
                expected_direction="must_reach",
                violation_direction="wrong_target",
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
                expected_direction="must_reach",
                violation_direction="wrong_target",
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
    owner_entry = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "owner_initial_entry"
    )
    assert owner_entry.locus_names == ("PumpControl", "PumpState")
    assert owner_entry.property == "initial_entry"
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
    assert "mutually disconnected" in global_issue.title
    assert "named_source_transition_refs=[]" in global_issue.observed
    assert "cannot reach one another in any direction" in global_issue.observed
    aggregate = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "aggregate_zero_behavior"
    )
    assert aggregate.locus_names == (
        "PumpState",
        "WaterState",
        "MethaneState",
    )
    assert aggregate.property == "deadlock_freedom"
    assert aggregate.violation_direction == "dead_end"
    assert aggregate.predicate_id is None
    assert "named_source_transition_refs=[]" in aggregate.observed


def test_0023_frontier_keeps_direct_leaf_dead_ends_independent() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0023")
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
                expected_direction="must_reach",
                violation_direction="wrong_target",
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
                expected_direction="must_reach",
                violation_direction="wrong_target",
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

    leaf_dead_ends = [
        item.candidate
        for item in batch.obligations
        if item.kind == "reachable_dead_end"
    ]
    assert {item.locus_names for item in leaf_dead_ends} == {
        ("PumpState",),
        ("WaterState",),
        ("MethaneState",),
    }
    assert not any(
        item.kind == "aggregate_zero_behavior" for item in batch.obligations
    )
    assert not any(
        item.kind == "cross_wrapper_reachability" for item in batch.obligations
    )


def test_cross_wrapper_frontier_does_not_overclaim_mutual_disconnection() -> None:
    pair = load_pair(REPORT_ROOT / "pairs" / "0053")
    facts = pair.inspection_facts
    assert facts is not None
    named_transition = facts.transitions[0].model_copy(
        update={
            "source": "PumpState",
            "resolved_source_ref": "state:PumpState:line:4",
        }
    )
    pair = pair.model_copy(
        update={
            "inspection_facts": facts.model_copy(
                update={
                    "transitions": (named_transition, *facts.transitions[1:]),
                }
            )
        }
    )
    contracts = [
        _contract(
            contract_id="NL-CONTRACT-NL4-PUMP-WATER",
            segment_id="NL4",
            locus_kind="transition",
            locus_names=("PumpState", "WaterState"),
            property_name="transition_endpoints",
            expected_direction="must_reach",
            violation_direction="wrong_target",
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
            expected_direction="must_reach",
            violation_direction="wrong_target",
            hints=(
                _hint("source", "WaterState", "NL5"),
                _hint("target", "MethaneState", "NL5"),
            ),
        ),
    ]
    response = _response(contracts)

    batch = materialize_v27_frontier(
        pair,
        response,
        {item.contract_id: item for item in response.contracts},
        (),
        (),
    )

    issue = next(
        item.candidate
        for item in batch.obligations
        if item.kind == "cross_wrapper_reachability"
    )
    assert "mutually disconnected" not in issue.title
    assert "cannot reach one another in any direction" not in issue.observed


def test_frontier_pydantic_descriptions_reach_json_schema() -> None:
    identity_schema = IdentityNormalizationReceipt.model_json_schema()
    frontier_schema = FrontierBatch.model_json_schema()
    contract_schema = NLContractResponse.model_json_schema()

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
    cardinality_schema = contract_schema["$defs"]["CardinalityRequirement"]
    assert "规范性数量要求" in cardinality_schema["description"]
    assert "observed count" in cardinality_schema["properties"]["required_count"]["description"]
    assert set(
        cardinality_schema["properties"]["member_domain"]["enum"]
    ) == {
        "direct_child_states",
        "concurrent_regions",
        "explicit_named_members",
        "unresolved",
    }
    grounding_schema = GroundingResponse.model_json_schema()
    domain_binding_schema = grounding_schema["$defs"]["CardinalityDomainBinding"]
    assert "有限成员域" in domain_binding_schema["description"]
    assert "exact_source_inventory.states" in domain_binding_schema["properties"][
        "owner_source_id"
    ]["description"]
    assert "closed_model_inventory.states[].ref" in domain_binding_schema[
        "properties"
    ]["owner_model_ref"]["description"]
    assert set(domain_binding_schema["properties"]["status"]["enum"]) == {
        "exact",
        "ambiguous",
        "unbound",
    }
    assert "observed count" in grounding_schema["properties"][
        "cardinality_bindings"
    ]["description"]


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
