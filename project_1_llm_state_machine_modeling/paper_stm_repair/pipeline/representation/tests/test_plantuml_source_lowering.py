from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from paper_stm_repair_conversion.adapters.plantuml_source import parse_plantuml_source
from paper_stm_repair_representation.plantuml_source_audit import audit_lowered_artifact
from paper_stm_repair_representation.plantuml_source_lowering import (
    lower_plantuml_source,
)
from paper_stm_repair_representation.plantuml_working_contract import (
    bind_inspect_diagnostics,
    build_review_obligations,
    validate_working_contract,
)
from pyfcstm.diagnostics.inspect import inspect_model
from pyfcstm.model.load import load_state_machine_from_text
from pyfcstm.simulate import SimulationRuntime


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "project_1_llm_state_machine_modeling").is_dir():
            return parent
    raise RuntimeError("repository root not found")


REPO_ROOT = _repo_root()
PAIRS = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/corpora/seed_library"
    / "llms-emp-stm-subset/assets/extracted/feedback_final_pairs.jsonl"
)
WORKING_CONTRACT_SCHEMA = (
    REPO_ROOT
    / "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/representation"
    / "schemas/working_fcstm_contract.schema.json"
)


def _sha256_json_for_test(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _rows() -> list[dict]:
    return [json.loads(line) for line in PAIRS.read_text(encoding="utf-8").splitlines()]


def _lower_text(text: str, *, example_id: str) -> dict:
    canonical = parse_plantuml_source(text, example_id=example_id)
    return lower_plantuml_source(canonical)


def _artifact(text: str, *, example_id: str = "audit-fixture"):
    canonical = parse_plantuml_source(text, example_id=example_id)
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()
    return canonical, lowered, model, report


BASIC_SOURCE = """@startuml
[*] --> A
state A
state B
A --> B : Go
B --> [*] : Stop
@enduml
"""

CROSS_SCOPE_SOURCE = """@startuml
state Outside
state Outer {
  [*] --> Inner
  state Inner
  Inner --> Outside : Leave
}
[*] --> Outer
@enduml
"""

COMPOSITE_SOURCE = """@startuml
state Operate {
  [*] --> Idle
  state Idle
}
state Off
[*] --> Operate
Operate --> Off : Shutdown
@enduml
"""

NESTED_FINAL_SOURCE = """@startuml
state Area {
  [*] --> Active
  state Active
  Active --> [*] : Done
}
[*] --> Area
@enduml
"""

PLACEHOLDER_SOURCE = """@startuml
state Container {
  state RealChild
}
[*] --> Container
@enduml
"""

MULTIPLE_INITIAL_SOURCE = """@startuml
state Active {
  [*] --> First
  [*] --> Second
  state First
  state Second
}
[*] --> Active
@enduml
"""

REGION_SOURCE = """@startuml
state Parallel {
  [*] --> LeftIdle
  LeftIdle --> LeftDone : left
  --
  [*] --> RightIdle
  RightIdle --> RightDone : right
}
@enduml
"""


def test_final_boundary_is_emitted_as_fcstm_exit():
    lowered = _lower_text(
        """@startuml
[*] --> PoweredOn
PoweredOn --> [*] : keyOff
@enduml
""",
        example_id="root-final-fixture",
    )
    assert "PoweredOn -> [*] : /keyOff;" in lowered["fcstm"]
    assert 'state end named "end"' not in lowered["fcstm"]
    assert lowered["comparison"]["final_transition_coverage"] == "1/1"


def test_lifecycle_actions_are_emitted_as_abstract_actions():
    lowered = _lower_text(
        """@startuml
[*] --> InMotion
state InMotion {
  entry/Accelerate
  do/Send
  exit/Stop
  state Active
  [*] --> Active
}
@enduml
""",
        example_id="lifecycle-fixture",
    )
    assert "enter abstract Accelerate;" in lowered["fcstm"]
    assert ">> during before abstract Send;" in lowered["fcstm"]
    assert "exit abstract Stop;" in lowered["fcstm"]
    assert lowered["comparison"]["lifecycle_action_coverage"] == "3/3"


def test_lifecycle_only_empty_composite_preserves_hook_without_inventing_a_leaf():
    canonical, lowered, model, _ = _artifact(
        """@startuml
[*] --> Active
state Active {
  entry/Prepare
}
@enduml
""",
        example_id="lifecycle-empty-composite-fixture",
    )
    runtime = SimulationRuntime(model)
    runtime.cycle()
    active = next(
        state for state in canonical["model"]["states"] if state["id"] == "Active"
    )
    assert active["kind"] == "composite"
    assert active["attributes"]["lifecycle_actions"][0]["text"] == "Prepare"
    assert lowered["comparison"]["lifecycle_action_coverage"] == "1/1"
    assert runtime.current_state.path[-2] == "Active"
    assert runtime.current_state.path[-1].startswith("UnspecifiedInitial")


def test_scope_exit_and_parent_continuation_reach_autonomous_initial_state():
    lowered = _lower_text(
        """@startuml
state Human {
  [*] --> Idle
  state Idle
}
state Autonomous {
  [*] --> Ready
  state Ready
}
[*] --> Human
Human --> Autonomous : Switch
@enduml
""",
        example_id="composite-entry-fixture",
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    runtime.cycle()
    assert runtime.current_state.path[-2:] == ("Human", "Idle")
    runtime.cycle([f"{model.root_state.name}.Switch"])
    assert runtime.current_state.path[-2:] == ("Autonomous", "Ready")


def test_initial_transition_label_is_preserved_as_opaque_event():
    lowered = _lower_text(
        """@startuml
[*] --> Idle : Power On
state Idle
@enduml
""",
        example_id="event-initial-fixture",
    )

    assert 'named "Awaiting initial event: Power On"' in lowered["fcstm"]
    assert "-> Idle : /Power_On;" in lowered["fcstm"]
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0001"
    )
    assert mapping["status"] == "mapped"
    assert len(mapping["emitted"]) == 2
    assert mapping["emitted"][0]["generated_role"] == "source_initial_wait_entry"
    assert "/Power_On" in mapping["emitted"][1]["line"]


def test_working_contract_protects_synthetic_states_and_excludes_them_from_positive_trace():
    canonical, lowered, _, report = _artifact(
        """@startuml
[*] --> Human : Power On
state Human {
}
@enduml
""",
        example_id="ownership-fixture",
    )
    contract = lowered["working_contract"]
    synthetics = [
        item for item in contract["elements"] if item["kind"] == "synthetic_state"
    ]

    assert {item["metadata"]["generated_reason"] for item in synthetics} == {
        "event_gated_plantuml_initial_wait",
        "missing_source_initial_fail_closed",
    }
    assert all(item["origin"] == "compiler_owned" for item in synthetics)
    assert all(item["edit_policy"] == "protected" for item in synthetics)
    positive_refs = {
        ref
        for entry in contract["source_trace_base"]["entries"]
        for ref in entry["intermediate_elements"]
    }
    assert not positive_refs.intersection(
        ref for item in synthetics for ref in item["model_refs"]
    )
    assert set(contract["source_trace_base"]["attribution_exclusions"]) >= {
        item["element_id"] for item in synthetics
    }
    assert contract["usage_gate"] == "audit_only"
    assert contract["artifact_role"] == "structural_projection"
    assert all(
        entry["trace_dimension"] == "identity_only"
        and entry["behavioral_fidelity"] == "not_assessed"
        and entry["attribution_boundary"]["closure_claim_allowed"] is False
        for entry in contract["source_trace_base"]["entries"]
    )
    validate_working_contract(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        contract=contract,
    )
    contract = bind_inspect_diagnostics(
        fcstm=lowered["fcstm"],
        inspect_report=report,
        contract=contract,
    )
    assert contract["usage_gate"] == "discover_input_with_capability_mask"
    assert contract["artifact_role"] == "attribution_scoped_working_model"
    contract["artifact_bindings"] = {
        "canonical_path": "project_1_llm_state_machine_modeling/paper_stm_repair/canonical.json",
        "fcstm_path": "project_1_llm_state_machine_modeling/paper_stm_repair/model.fcstm",
        "parse_inspect_path": "project_1_llm_state_machine_modeling/paper_stm_repair/inspect.json",
        "source_trace_path": "project_1_llm_state_machine_modeling/paper_stm_repair/trace.json",
        "canonical_file_sha256": "a" * 64,
        "fcstm_file_sha256": "b" * 64,
        "parse_inspect_file_sha256": "c" * 64,
        "source_trace_file_sha256": "d" * 64,
        "comparison_sha256": "e" * 64,
        "ast_audit_sha256": "f" * 64,
    }
    review_obligations = build_review_obligations(
        comparison=lowered["comparison"],
        official_identity=canonical["metadata"]["official_identity_reconciliation"],
        contract=contract,
    )
    contract["review_subject"] = {
        "review_subject_sha256": "1" * 64,
        "risk_tags": sorted({item["risk_tag"] for item in review_obligations}),
        "review_obligations": review_obligations,
        "second_pass_required": bool(review_obligations),
    }
    Draft202012Validator(
        json.loads(WORKING_CONTRACT_SCHEMA.read_text(encoding="utf-8"))
    ).validate(contract)
    validate_working_contract(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        contract=contract,
        inspect_report=report,
    )


def test_cross_scope_transition_is_one_source_macro_with_protected_members():
    canonical, lowered, _, _ = _artifact(
        CROSS_SCOPE_SOURCE,
        example_id="macro-fixture",
    )
    contract = lowered["working_contract"]
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["reason_code"] == "R45.MAP.cross_scope_exit_continuation"
    )
    macro = next(
        item
        for item in contract["macros"]
        if item["macro_id"] == f"macro:transition:{mapping['transition_id']}"
    )
    elements = {item["element_id"]: item for item in contract["elements"]}

    assert len(mapping["emitted"]) == 2
    assert len(macro["member_element_ids"]) == 2
    assert macro["rewrite_policy"] == "controller_regenerate_only"
    assert all(
        elements[item]["origin"] == "compiler_owned"
        for item in macro["member_element_ids"]
    )
    assert all(
        elements[item]["edit_policy"] == "protected"
        for item in macro["member_element_ids"]
    )
    trace = next(
        item
        for item in contract["source_trace_base"]["entries"]
        if item["trace_id"] == f"trace:transition:{mapping['transition_id']}"
    )
    assert trace["intermediate_elements"] == [macro["macro_id"]]
    validate_working_contract(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        contract=contract,
    )


def test_capabilities_keep_static_source_analysis_when_runtime_semantics_are_unsupported():
    _, lowered, _, _ = _artifact(REGION_SOURCE, example_id="capability-fixture")
    capabilities = lowered["working_contract"]["capability_eligibility"]

    assert capabilities["parse"]["status"] == "eligible"
    assert capabilities["inspect_structure"]["status"] == "eligible"
    assert (
        capabilities["source_static_discovery"]["status"] == "eligible_with_exclusions"
    )
    assert capabilities["simulation"]["status"] == "ineligible"
    assert capabilities["transition_trace"]["status"] == "ineligible"
    assert (
        "R45.DEBT.concurrent_region_semantics"
        in capabilities["simulation"]["reason_codes"]
    )
    assert lowered["working_contract"]["usage_gate"] == "audit_only"
    assert set(capabilities["source_static_discovery"]["eligible_element_ids"])


@pytest.mark.parametrize(
    "mutation, message",
    [
        ("synthetic_source_owned", "transition macro contains non-compiler member"),
        ("partial_macro", "transition macro member drift"),
        (
            "compiler_positive_trace",
            "positive source trace binds a non-source-owned element",
        ),
    ],
)
def test_working_contract_rejects_attribution_and_partial_macro_tampering(
    mutation: str, message: str
):
    canonical, lowered, _, _ = _artifact(
        """@startuml
state Outside
state Outer {
  state Inner
  Inner --> Outside : Leave
}
[*] --> Outer : Start
@enduml
""",
        example_id=f"contract-mutation-{mutation}",
    )
    contract = copy.deepcopy(lowered["working_contract"])
    if mutation == "synthetic_source_owned":
        synthetic = next(
            item for item in contract["elements"] if item["kind"] == "synthetic_state"
        )
        synthetic["origin"] = "source_owned"
        synthetic["edit_policy"] = "direct_issue_bound"
    elif mutation == "partial_macro":
        macro = next(
            item
            for item in contract["macros"]
            if item["macro_kind"] == "R45.MAP.cross_scope_exit_continuation"
        )
        macro["member_element_ids"].pop()
    else:
        compiler = next(
            item for item in contract["elements"] if item["origin"] == "compiler_owned"
        )
        contract["source_trace_base"]["entries"].append(
            {
                "trace_id": "trace:malicious",
                "trace_class": "source_semantic_identity",
                "trace_dimension": "identity_only",
                "source_elements": [compiler["element_id"]],
                "intermediate_elements": ["macro:malicious"],
                "trace_relation": "exact",
                "projection_status": "projectable",
                "required_for_issue_ids": [],
                "issue_binding_policy": "discover_must_confirm_source_issue",
                "behavioral_fidelity": "not_assessed",
                "attribution_boundary": {
                    "source_level_claim_allowed": True,
                    "conversion_or_lowering_related": False,
                    "representation_related": False,
                    "closure_claim_allowed": False,
                    "rationale": "malicious",
                },
                "trace_relation_rationale": "malicious",
                "trace_evidence": [],
                "reviewer_notes": "malicious",
            }
        )

    with pytest.raises(ValueError, match=message):
        validate_working_contract(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            contract=contract,
        )


@pytest.mark.parametrize(
    "mutation,message",
    [
        ("field_ownership", "field ownership drift"),
        ("positive_trace_deletion", "positive source trace coverage drift"),
        ("macro_wrong_source", "transition macro source binding drift"),
        ("element_digest", "working contract element digest drift"),
        ("macro_digest", "working contract macro digest drift"),
        ("compiler_digest", "working contract compiler-owned digest drift"),
        ("capability_field", "eligible field projection drift"),
    ],
)
def test_working_contract_recomputes_attribution_invariants_from_source(
    mutation: str, message: str
):
    canonical, lowered, _, _ = _artifact(
        BASIC_SOURCE,
        example_id=f"source-recomputed-{mutation}",
    )
    contract = copy.deepcopy(lowered["working_contract"])
    if mutation == "field_ownership":
        transition = next(
            item
            for item in contract["elements"]
            if item["kind"] == "transition_macro_root"
        )
        transition["field_ownership"]["event_interpretation"] = "source_owned"
        contract["inventory_digests"]["element_set_sha256"] = _sha256_json_for_test(
            contract["elements"]
        )
    elif mutation == "positive_trace_deletion":
        contract["source_trace_base"]["entries"].pop()
        contract["summary"]["positive_trace_count"] -= 1
        contract["inventory_digests"]["source_trace_set_sha256"] = (
            _sha256_json_for_test(contract["source_trace_base"]["entries"])
        )
    elif mutation == "macro_wrong_source":
        transitions = [
            item
            for item in contract["elements"]
            if item["kind"] == "transition_macro_root"
        ][:2]
        first_macro = next(
            item
            for item in contract["macros"]
            if item["macro_id"] == transitions[0]["macro_ids"][0]
        )
        second_macro = next(
            item
            for item in contract["macros"]
            if item["macro_id"] == transitions[1]["macro_ids"][0]
        )
        transitions[0]["macro_ids"], transitions[1]["macro_ids"] = (
            transitions[1]["macro_ids"],
            transitions[0]["macro_ids"],
        )
        first_macro["source_element_ids"], second_macro["source_element_ids"] = (
            second_macro["source_element_ids"],
            first_macro["source_element_ids"],
        )
        contract["inventory_digests"]["element_set_sha256"] = _sha256_json_for_test(
            contract["elements"]
        )
        contract["inventory_digests"]["macro_set_sha256"] = _sha256_json_for_test(
            contract["macros"]
        )
    elif mutation == "element_digest":
        contract["inventory_digests"]["element_set_sha256"] = "0" * 64
    elif mutation == "macro_digest":
        contract["inventory_digests"]["macro_set_sha256"] = "0" * 64
    elif mutation == "compiler_digest":
        contract["inventory_digests"]["compiler_owned_set_sha256"] = "0" * 64
    else:
        capability = contract["capability_eligibility"]["source_static_discovery"]
        capability["eligible_field_refs"].pop()

    with pytest.raises(ValueError, match=message):
        validate_working_contract(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            contract=contract,
        )


@pytest.mark.parametrize(
    "capability,status,message",
    [
        ("main_result", "eligible", "baseline main_result status is not fail-closed"),
        (
            "repair",
            "eligible_with_exclusions",
            "baseline repair status is not fail-closed",
        ),
        (
            "final_export",
            "eligible_with_exclusions",
            "baseline final_export status is not fail-closed",
        ),
        (
            "confirm",
            "eligible_with_exclusions",
            "baseline confirm status is not fail-closed",
        ),
        (
            "simulation",
            "eligible_with_exclusions",
            "baseline simulation status is not fail-closed",
        ),
    ],
)
def test_working_contract_rejects_premature_result_repair_or_simulation_promotion(
    capability: str, status: str, message: str
):
    canonical, lowered, _, _ = _artifact(BASIC_SOURCE, example_id="gate-tamper")
    contract = copy.deepcopy(lowered["working_contract"])
    contract["capability_eligibility"][capability]["status"] = status

    with pytest.raises(ValueError, match=message):
        validate_working_contract(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            contract=contract,
        )


def test_bound_inspect_diagnostics_never_preconfirm_a_source_issue():
    canonical, lowered, _, report = _artifact(
        """@startuml
[*] --> A
state A
state B
A --> B
A --> B
@enduml
""",
        example_id="diagnostic-attribution-fixture",
    )
    contract = bind_inspect_diagnostics(
        fcstm=lowered["fcstm"],
        inspect_report=report,
        contract=lowered["working_contract"],
    )

    attribution = contract["diagnostic_attribution"]
    assert attribution["binding_status"] == "bound"
    assert len(attribution["records"]) == len(report["diagnostics"])
    assert {item["outcome"] for item in attribution["records"]}.issubset(
        {
            "rejected_conversion_artifact",
            "candidate_only_until_source_evidence",
            "insufficient_evidence",
        }
    )
    assert all(
        item["promotion_ceiling"] in {"candidate_only", "rejected_or_insufficient"}
        for item in attribution["records"]
    )
    diagnostics_capability = contract["capability_eligibility"]["inspect_diagnostics"]
    assert diagnostics_capability["status"] == "ineligible"
    assert diagnostics_capability["eligible_element_ids"] == []
    validate_working_contract(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        contract=contract,
        inspect_report=report,
    )


def test_source_input_normalization_is_a_conversion_boundary_not_positive_trace():
    canonical, lowered, _, _ = _artifact(
        """@startuml
state S as \"S\"
@enduml
""",
        example_id="normalization-boundary-fixture",
    )
    canonical["metadata"]["source_normalizations"] = [
        {
            "rule_id": "transport_quote_repair",
            "raw_ref": "normalization-boundary-fixture.puml:line:2",
            "before": 'state S as ""S""',
            "after": 'state S as "S"',
        }
    ]
    lowered = lower_plantuml_source(canonical)
    contract = lowered["working_contract"]

    assert not [
        entry
        for entry in contract["source_trace_base"]["entries"]
        if entry["source_elements"] == ["source:normalization:1"]
    ]
    boundary = contract["source_trace_base"]["boundary_entries"][0]
    assert boundary["trace_relation"] == "conversion_artifact"
    assert boundary["attribution_boundary"]["source_level_claim_allowed"] is False
    assert boundary["attribution_boundary"]["closure_claim_allowed"] is False
    assert (
        "source:normalization:1"
        in contract["source_trace_base"]["attribution_exclusions"]
    )
    validate_working_contract(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        contract=contract,
    )


def test_unlabeled_fanout_is_structurally_preserved_with_operational_debt():
    lowered = _lower_text(
        """@startuml
[*] --> PumpState
PumpState --> WaterState
PumpState --> MethaneState
@enduml
""",
        example_id="fanout-fixture",
    )

    assert "PumpState -> WaterState;" in lowered["fcstm"]
    assert "PumpState -> MethaneState;" in lowered["fcstm"]
    assert lowered["comparison"]["structural_verdict"] == "structure_preserved"
    reasons = {
        item["reason_code"] for item in lowered["comparison"]["operational_debts"]
    }
    assert "R45.DEBT.ambiguous_unlabeled_fanout" in reasons


def test_transition_to_composite_without_initial_stops_at_explicit_placeholder():
    lowered = _lower_text(
        """@startuml
[*] --> Closed
state Closed
state Open {
  state Empty
}
Closed --> Open : Door Opened
@enduml
""",
        example_id="missing-composite-initial-fixture",
    )

    assert "Closed -> Open : /Door_Opened;" in lowered["fcstm"]
    assert 'state UnspecifiedInitial named "Unspecified initial";' in lowered["fcstm"]
    debts = {item["reason_code"] for item in lowered["comparison"]["operational_debts"]}
    assert "R45.DEBT.missing_explicit_initial" in debts


def test_initial_to_composite_without_child_initial_is_structurally_preserved():
    lowered = _lower_text(
        """@startuml
state CollisionAvoidance {
  state Monitoring
}
[*] --> CollisionAvoidance : Possible collision detected
@enduml
""",
        example_id="initial-missing-composite-initial-fixture",
    )
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["transition_id"] == "tr_0001"
    )

    assert mapping["status"] == "mapped"
    assert mapping["reason_code"] == "R45.MAP.initial_boundary"
    assert (
        "InitialWaittr_0001 -> CollisionAvoidance : /Possible_collision_detected;"
        in lowered["fcstm"]
    )
    assert 'state UnspecifiedInitial named "Unspecified initial";' in lowered["fcstm"]


def test_opaque_state_body_is_preserved_in_fcstm_display_name_and_trace():
    lowered = _lower_text(
        """@startuml
[*] --> TurnOn
TurnOn : {max=2s, min=2s}
@enduml
""",
        example_id="body-fixture",
    )
    mappings = [
        item
        for item in lowered["comparison"]["body_mappings"]
        if item["representation"] == "state_display_name"
    ]

    assert {item["state_id"] for item in mappings} == {"TurnOn"}
    for item in mappings:
        assert item["text"] in lowered["fcstm"]
        assert item["raw_ref"]
    assert lowered["comparison"]["body_line_coverage"] == "1/1"


def test_invalid_self_initial_is_preserved_as_a_stoppable_surrogate():
    lowered = _lower_text(
        """@startuml
state DoorsClosing {
  [*] --> DoorsClosing
  state Closed
}
[*] --> DoorsClosing
@enduml
""",
        example_id="invalid-self-initial-fixture",
    )
    mapping = next(
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["reason_code"] == "R45.MAP.invalid_source_initial_surrogate"
    )

    assert mapping["status"] == "mapped"
    assert mapping["reason_code"] == "R45.MAP.invalid_source_initial_surrogate"
    assert mapping["emitted"][0]["generated_role"] == "invalid_source_initial_surrogate"
    assert (
        "PlantUML initial target outside child scope: DoorsClosing" in lowered["fcstm"]
    )


def test_invalid_final_scope_is_preserved_as_a_stoppable_surrogate():
    lowered = _lower_text(
        """@startuml
state Outside
[*] --> Outside
state Container {
  Outside --> [*] : finish
}
@enduml
""",
        example_id="invalid-final-scope",
    )
    mappings = [
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["reason_code"] == "R45.MAP.invalid_source_final_surrogate"
    ]

    assert len(mappings) == 1
    assert all(item["status"] == "mapped" for item in mappings)
    assert all(
        item["emitted"][0]["generated_role"] == "invalid_source_final_surrogate"
        for item in mappings
    )
    assert (
        "PlantUML final boundary outside source ancestry: @final:Container"
        in (lowered["fcstm"])
    )
    assert lowered["comparison"]["final_transition_coverage"] == "1/1"
    assert any(
        item["reason_code"] == "R45.DEBT.invalid_source_final_scope"
        for item in lowered["comparison"]["operational_debts"]
    )


def test_concurrent_regions_and_separator_are_preserved_but_execution_is_blocked():
    source = """@startuml
state Parallel {
  [*] --> LeftIdle
  LeftIdle --> LeftDone : left
  --
  [*] --> RightIdle
  RightIdle --> RightDone : right
}
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="parallel-regions")
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()
    audit = audit_lowered_artifact(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        model=model,
        inspect_report=report,
    )

    assert lowered["comparison"]["concurrent_region_coverage"] == "2/2"
    assert lowered["comparison"]["concurrent_region_separator_coverage"] == "1/1"
    assert "[PlantUML concurrent region 0]" in lowered["fcstm"]
    assert "[PlantUML concurrent region 1]" in lowered["fcstm"]
    assert any(
        item["reason_code"] == "R45.DEBT.concurrent_region_semantics"
        for item in lowered["comparison"]["operational_debts"]
    )
    assert lowered["comparison"]["fcstm_execution_eligible"] is False
    assert audit["status"] == "passed"


def test_junction_stereotype_is_lowered_and_audited_as_pseudostate():
    canonical, lowered, model, report = _artifact(
        """@startuml
[*] --> Before
state Before
state Merge <<junction>>
state After
Before --> Merge : route
Merge --> After
@enduml
""",
        example_id="junction-fixture",
    )
    junction = next(
        state for state in model.root_state.walk_states() if state.name == "Merge"
    )

    assert canonical["model"]["states"][1]["kind"] == "junction"
    assert "pseudo state Merge" in lowered["fcstm"]
    assert junction.is_pseudo
    assert (
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )["status"]
        == "passed"
    )


def test_workbook_transport_normalization_is_hash_bound_and_audited():
    row = _rows()[58]
    canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
    lowered = lower_plantuml_source(canonical)

    assert lowered["comparison"]["source_normalization_coverage"] == "6/6"
    assert len(lowered["comparison"]["source_normalization_mappings"]) == 6
    assert "source_input.workbook_doubled_state_quotes" in lowered["fcstm"]
    assert "source_input.workbook_trailing_end_quote" in lowered["fcstm"]
    assert any(
        item["reason_code"] == "R45.DEBT.source_input_normalization"
        for item in lowered["comparison"]["operational_debts"]
    )


def test_ast_audit_rejects_concurrent_region_membership_tamper():
    canonical, lowered, model, report = _artifact(REGION_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    tampered["concurrent_region_mappings"][0]["state_ids"] = ["Parallel.RightIdle"]

    with pytest.raises(ValueError, match="concurrent region trace drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_concurrent_separator_tamper():
    canonical, lowered, model, report = _artifact(REGION_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    tampered["concurrent_region_separator_mappings"][0]["following_region_index"] = 7

    with pytest.raises(ValueError, match="concurrent separator trace drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_source_normalization_tamper():
    row = _rows()[58]
    canonical, lowered, model, report = _artifact(
        row["stm0_text"], example_id=row["pair_id"]
    )
    tampered = copy.deepcopy(lowered["comparison"])
    tampered["source_normalization_mappings"][0]["before"] = "different raw text"

    with pytest.raises(ValueError, match="source normalization trace drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_independently_rejects_official_entity_identity_tamper():
    canonical, lowered, model, report = _artifact(BASIC_SOURCE)
    tampered = copy.deepcopy(canonical)
    entity = next(
        item
        for item in tampered["metadata"]["official_validation"]["model"]["entities"]
        if item.get("qualified_name") == "A"
    )
    entity["qualified_name"] = "TamperedA"

    with pytest.raises(ValueError, match="canonical state identities differ"):
        audit_lowered_artifact(
            canonical=tampered,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ast_audit_independently_rejects_official_reconciliation_count_tamper():
    canonical, lowered, model, report = _artifact(BASIC_SOURCE)
    tampered = copy.deepcopy(canonical)
    tampered["metadata"]["official_identity_reconciliation"][
        "transition_identity_alignment_count"
    ] = 0

    with pytest.raises(
        ValueError, match="official transition reconciliation count drift"
    ):
        audit_lowered_artifact(
            canonical=tampered,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_unparsed_semantic_line_cannot_pass_structural_audit():
    source = """@startuml
[*] --> Idle
this is not PlantUML state syntax
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="unparsed-negative")
    lowered = lower_plantuml_source(canonical)
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()

    assert canonical["status"] == "partial"
    assert lowered["comparison"]["structural_verdict"] == "structure_blocked"
    with pytest.raises(ValueError, match="structural verdict is not preserved"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ownerless_lifecycle_is_preserved_as_root_display_metadata():
    lowered = _lower_text(
        """@startuml
[*] --> Idle
state Idle
exit/Send Obstacle Detected
@enduml
""",
        example_id="ownerless-lifecycle-fixture",
    )
    orphan = lowered["comparison"]["orphan_lifecycle_mappings"]

    assert len(orphan) == 1
    assert orphan[0]["representation"] == "root_display_name"
    assert orphan[0]["text"] in lowered["fcstm"]
    assert lowered["comparison"]["lifecycle_action_coverage"] == "1/1"
    assert lowered["comparison"]["abstract_lifecycle_hook_coverage"] == "0/1"


def test_multiple_initial_edges_are_all_preserved_with_operational_debt():
    lowered = _lower_text(
        """@startuml
state Active {
  [*] --> BrakeControlState
  [*] --> SteeringControlState
  [*] --> SensorControlState
}
[*] --> Active
@enduml
""",
        example_id="multiple-initial-fixture",
    )
    initial_mappings = [
        item
        for item in lowered["comparison"]["transition_mappings"]
        if item["source"] == "@initial:Active"
    ]

    assert all(
        item["status"] == "mapped" and item["emitted"] for item in initial_mappings
    )
    assert "[*] -> BrakeControlState;" in lowered["fcstm"]
    assert "[*] -> SteeringControlState;" in lowered["fcstm"]
    assert "[*] -> SensorControlState;" in lowered["fcstm"]
    assert any(
        item["reason_code"] == "R45.DEBT.multiple_initial_fanout"
        for item in lowered["comparison"]["operational_debts"]
    )


def test_ast_audit_rejects_trace_parent_drift():
    canonical, lowered, model, report = _artifact(CROSS_SCOPE_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    tampered["state_mappings"][0]["fcstm_parent_path"] = "wrong.parent"

    with pytest.raises(ValueError, match="parent mismatch"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_missing_emitted_transition_occurrence():
    canonical, lowered, _, _ = _artifact(BASIC_SOURCE)
    removed = "B -> [*] : /Stop;"
    tampered_fcstm = lowered["fcstm"].replace(removed, "", 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="authored transition multiset"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_joint_lowering_and_trace_endpoint_drift():
    canonical, lowered, _, _ = _artifact(BASIC_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if item["transition_id"] == "tr_0002"
    )
    original = mapping["emitted"][0]["line"]
    rewritten = original.replace("A -> B", "A -> A")
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="endpoint projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_cross_scope_exit_retargeted_inside_scope():
    canonical, lowered, _, _ = _artifact(CROSS_SCOPE_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if any(
            emitted["generated_role"] == "cross_scope_exit_segment"
            for emitted in item["emitted"]
        )
    )
    exit_segment = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "cross_scope_exit_segment"
    )
    original = exit_segment["line"]
    rewritten = original.replace("-> [*]", "-> Inner")
    exit_segment["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="cross-scope exit projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_untracked_extra_transition():
    canonical, lowered, _, _ = _artifact(BASIC_SOURCE)
    prefix, suffix = lowered["fcstm"].rsplit("}\n", 1)
    tampered_fcstm = prefix + "    A -> B;\n}\n" + suffix
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="authored transition multiset"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_joint_event_binding_drift():
    canonical, lowered, _, _ = _artifact(BASIC_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if item["transition_id"] == "tr_0002"
    )
    original = mapping["emitted"][0]["line"]
    rewritten = original.replace("/Go", "/Stop")
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="event projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_event_initial_wait_disconnect():
    source = """@startuml
[*] --> A : Start
state A
state B
@enduml
"""
    canonical, lowered, _, _ = _artifact(source)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if item["transition_id"] == "tr_0001"
    )
    main = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "source_initial_transition"
    )
    original = main["line"]
    rewritten = original.replace("-> A", "-> B")
    main["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(
        ValueError, match="initial transition endpoint projection drift"
    ):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_composite_force_loss():
    canonical, lowered, _, _ = _artifact(COMPOSITE_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if item["emitted"][0]["line"].startswith("!Operate -> Off")
    )
    original = mapping["emitted"][0]["line"]
    assert original.startswith("!")
    rewritten = original[1:]
    mapping["emitted"][0]["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="endpoint projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_nested_final_target_drift():
    canonical, lowered, _, _ = _artifact(NESTED_FINAL_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["transition_mappings"]
        if any(
            emitted["generated_role"] == "nested_final_completion_hold"
            for emitted in item["emitted"]
        )
    )
    terminal = next(
        item
        for item in mapping["emitted"]
        if item["generated_role"] == "nested_final_completion_hold"
    )
    original = terminal["line"]
    synthetic_target = original.split("->", 1)[1].split(":", 1)[0].strip().rstrip(";")
    rewritten = original.replace(synthetic_target, "Active")
    terminal["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="nested final boundary projection drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_fail_closed_placeholder_retargeted_to_real_child():
    canonical, lowered, _, _ = _artifact(PLACEHOLDER_SOURCE)
    tampered = copy.deepcopy(lowered["comparison"])
    mapping = next(
        item
        for item in tampered["synthetic_transition_mappings"]
        if item["scope"] == "Container"
    )
    original = mapping["line"]
    rewritten = "[*] -> RealChild;"
    mapping["line"] = rewritten
    tampered_fcstm = lowered["fcstm"].replace(original, rewritten, 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="synthetic initial target/reason drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=tampered,
            model=model,
            inspect_report=report,
        )


def test_ast_audit_rejects_multiple_initial_declaration_reordering():
    canonical, lowered, _, _ = _artifact(MULTIPLE_INITIAL_SOURCE)
    first = "[*] -> First;"
    second = "[*] -> Second;"
    tampered_fcstm = lowered["fcstm"].replace(first, "<FIRST>", 1)
    tampered_fcstm = tampered_fcstm.replace(second, first, 1).replace(
        "<FIRST>", second, 1
    )
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="initial transition declaration order drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_event_specific_deep_entry_precedes_composite_default_initial():
    source = """@startuml
[*] --> Outside
state Outside
state C {
    [*] --> Default
    state Default
    state Wanted
}
Outside --> C.Wanted : Go
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="priority_probe")
    lowered = lower_plantuml_source(canonical)
    assert lowered["fcstm"].index("[*] -> Wanted : /Go;") < lowered["fcstm"].index(
        "[*] -> Default;"
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    report = inspect_model(model).to_json()
    audit_lowered_artifact(
        canonical=canonical,
        fcstm=lowered["fcstm"],
        comparison=lowered["comparison"],
        model=model,
        inspect_report=report,
    )
    wanted = "[*] -> Wanted : /Go;"
    default = "[*] -> Default;"
    tampered_fcstm = lowered["fcstm"].replace(wanted, "<WANTED>", 1)
    tampered_fcstm = tampered_fcstm.replace(default, wanted, 1).replace(
        "<WANTED>", default, 1
    )
    tampered_model = load_state_machine_from_text(tampered_fcstm)
    tampered_report = inspect_model(tampered_model).to_json()
    with pytest.raises(ValueError, match="transition-specific entry priority drift"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=tampered_model,
            inspect_report=tampered_report,
        )
    runtime = SimulationRuntime(model)
    runtime.cycle()
    runtime.cycle([f"{model.root_state.name}.Go"])
    assert runtime.current_state.path[-2:] == ("C", "Wanted")


def test_deep_source_initial_precedes_nested_default_initial():
    source = """@startuml
state C {
    [*] --> Default
    state Default
    state Wanted
}
[*] --> C.Wanted
@enduml
"""
    canonical = parse_plantuml_source(source, example_id="deep_initial_priority_probe")
    lowered = lower_plantuml_source(canonical)
    assert lowered["fcstm"].index("[*] -> Wanted;") < lowered["fcstm"].index(
        "[*] -> Default;"
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)
    runtime.cycle()
    assert runtime.current_state.path[-2:] == ("C", "Wanted")


def test_ast_audit_rejects_opaque_body_metadata_loss():
    source = """@startuml
[*] --> Active
Active : opaque source annotation
@enduml
"""
    canonical, lowered, _, _ = _artifact(source)
    body_text = lowered["comparison"]["body_mappings"][0]["text"]
    tampered_fcstm = lowered["fcstm"].replace(body_text, "<removed>", 1)
    model = load_state_machine_from_text(tampered_fcstm)
    report = inspect_model(model).to_json()

    with pytest.raises(ValueError, match="display metadata mismatch|body missing"):
        audit_lowered_artifact(
            canonical=canonical,
            fcstm=tampered_fcstm,
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )


def test_final_boundary_terminates_runtime_instead_of_entering_end_leaf():
    lowered = _lower_text(
        """@startuml
[*] --> PoweredOn
PoweredOn --> [*] : keyOff
@enduml
""",
        example_id="root-final-runtime-fixture",
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    runtime.cycle()
    runtime.cycle([f"{model.root_state.name}.keyOff"])

    assert runtime.is_ended is True
    assert runtime.brief_stack == []


def test_nested_final_stabilizes_then_outer_final_can_terminate():
    lowered = _lower_text(
        """@startuml
state Area {
  [*] --> Active
  state Active
  Active --> [*] : Done
}
[*] --> Area
Area --> [*] : Close
@enduml
""",
        example_id="nested-final-runtime-fixture",
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    runtime = SimulationRuntime(model)

    def event(name: str) -> list[str]:
        return [f"{model.root_state.name}.{name}"]

    runtime.cycle()
    assert runtime.current_state.path[-2:] == ("Area", "Active")
    runtime.cycle(event("Done"))
    assert runtime.current_state.path[-2] == "Area"
    assert runtime.current_state.path[-1].startswith("FinalWait")
    runtime.cycle(event("Close"))

    assert runtime.is_ended is True


def test_cross_scope_deep_targets_remain_event_distinguished():
    lowered = _lower_text(
        """@startuml
[*] --> Outside
state Outside
state Modes {
  [*] --> Default
  state Default
  state Braking
  state Steering
}
Outside --> Modes.Braking : Brake
Outside --> Modes.Steering : Steer
@enduml
""",
        example_id="deep-target-events-fixture",
    )
    model = load_state_machine_from_text(lowered["fcstm"])
    expectations = {
        "Brake": "Braking",
        "Steer": "Steering",
    }

    for event_name, expected_branch in expectations.items():
        runtime = SimulationRuntime(model)
        runtime.cycle()
        runtime.cycle([f"{model.root_state.name}.{event_name}"])
        assert runtime.current_state.path[-1] == expected_branch


def test_all_60_outputs_preserve_every_source_element_and_parse_inspect():
    rows = _rows()
    assert len(rows) == 60

    totals = {
        "states": 0,
        "source": 0,
        "mapped": 0,
        "blocked": 0,
        "structure_preserved": 0,
        "body_source": 0,
        "body_mapped": 0,
        "lifecycle_source": 0,
        "lifecycle_mapped": 0,
        "separators_source": 0,
        "separators_mapped": 0,
        "regions_source": 0,
        "regions_mapped": 0,
        "normalizations_source": 0,
        "normalizations_mapped": 0,
    }
    debt_reasons: dict[str, int] = {}
    for row in rows:
        canonical = parse_plantuml_source(row["stm0_text"], example_id=row["pair_id"])
        lowered = lower_plantuml_source(canonical)
        model = load_state_machine_from_text(lowered["fcstm"])
        report = inspect_model(model).to_json()
        ast_audit = audit_lowered_artifact(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            model=model,
            inspect_report=report,
        )

        assert (
            report["metrics"]["n_states_leaf"] + report["metrics"]["n_states_composite"]
            > 0
        )
        assert not [
            item for item in report["diagnostics"] if item.get("severity") == "error"
        ]
        assert ast_audit["status"] == "passed"
        assert lowered["comparison"]["source_transition_count"] == len(
            canonical["model"]["transitions"]
        )
        assert lowered["comparison"]["mapped_transition_count"] == len(
            canonical["model"]["transitions"]
        )
        assert lowered["comparison"]["blocked_transition_count"] == 0
        assert lowered["comparison"]["silently_dropped_transition_count"] == 0
        assert lowered["comparison"]["fcstm_execution_eligible"] is False
        assert lowered["comparison"]["discover_eligible"] is False
        contract = bind_inspect_diagnostics(
            fcstm=lowered["fcstm"],
            inspect_report=report,
            contract=lowered["working_contract"],
        )
        assert contract["usage_gate"] == "discover_input_with_capability_mask"
        assert (
            contract["capability_eligibility"]["source_static_discovery"]["status"]
            == "eligible_with_exclusions"
        )
        assert (
            contract["attribution_policy"]["main_result_conversion_artifact_limit"] == 0
        )
        assert all(
            entry["attribution_boundary"]["closure_claim_allowed"] is False
            for entry in contract["source_trace_base"]["entries"]
        )
        assert contract["capability_eligibility"]["repair"]["status"] == "not_run"
        assert contract["capability_eligibility"]["main_result"]["status"] == "not_run"
        assert (
            contract["capability_eligibility"]["simulation"]["status"] == "ineligible"
        )
        assert (
            contract["capability_eligibility"]["inspect_diagnostics"][
                "eligible_element_ids"
            ]
            == []
        )
        validate_working_contract(
            canonical=canonical,
            fcstm=lowered["fcstm"],
            comparison=lowered["comparison"],
            contract=contract,
            inspect_report=report,
        )
        assert all(
            mapping["status"] == "mapped" and mapping["emitted"]
            for mapping in lowered["comparison"]["transition_mappings"]
        )
        assert all(
            emitted["line"] in lowered["fcstm"]
            for mapping in lowered["comparison"]["transition_mappings"]
            for emitted in mapping["emitted"]
        )
        assert lowered["comparison"]["state_coverage"] == (
            f"{len(canonical['model']['states'])}/{len(canonical['model']['states'])}"
        )
        assert len(lowered["comparison"]["state_mappings"]) == len(
            canonical["model"]["states"]
        )
        totals["states"] += len(canonical["model"]["states"])
        totals["source"] += lowered["comparison"]["source_transition_count"]
        totals["mapped"] += lowered["comparison"]["mapped_transition_count"]
        totals["blocked"] += lowered["comparison"]["blocked_transition_count"]
        totals["structure_preserved"] += (
            lowered["comparison"]["structural_verdict"] == "structure_preserved"
        )
        body_mapped, body_source = map(
            int, lowered["comparison"]["body_line_coverage"].split("/")
        )
        lifecycle_mapped, lifecycle_source = map(
            int, lowered["comparison"]["lifecycle_action_coverage"].split("/")
        )
        totals["body_source"] += body_source
        totals["body_mapped"] += body_mapped
        totals["lifecycle_source"] += lifecycle_source
        totals["lifecycle_mapped"] += lifecycle_mapped
        for prefix, field in (
            ("separators", "concurrent_region_separator_coverage"),
            ("regions", "concurrent_region_coverage"),
            ("normalizations", "source_normalization_coverage"),
        ):
            mapped, source = map(int, lowered["comparison"][field].split("/"))
            totals[f"{prefix}_source"] += source
            totals[f"{prefix}_mapped"] += mapped
        for debt in lowered["comparison"]["operational_debts"]:
            reason = debt["reason_code"]
            debt_reasons[reason] = debt_reasons.get(reason, 0) + 1

    assert totals == {
        "states": 516,
        "source": 757,
        "mapped": 757,
        "blocked": 0,
        "structure_preserved": 60,
        "body_source": 95,
        "body_mapped": 95,
        "lifecycle_source": 16,
        "lifecycle_mapped": 16,
        "separators_source": 20,
        "separators_mapped": 20,
        "regions_source": 29,
        "regions_mapped": 29,
        "normalizations_source": 6,
        "normalizations_mapped": 6,
    }
    assert {
        "R45.DEBT.concurrent_region_semantics",
        "R45.DEBT.invalid_source_final_scope",
        "R45.DEBT.source_input_normalization",
    } <= set(debt_reasons)
