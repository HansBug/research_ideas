"""A2 removes execution machinery while retaining semantic obligations."""

import json
import re

import pytest
from pydantic import ValidationError

from paper_stm_method.semantics import workflow
from paper_stm_method.semantics.adjudication import SemanticAdjudication
from paper_stm_method.semantics.binding import BindingResult
from paper_stm_method.semantics.no_predicates import (
    SemanticCandidate, SemanticContract, SemanticContractCompletionResponse,
    SemanticContractResponse, SemanticDecisionResponse, SemanticGroundingResponse,
    build_semantic_evidence_record, project_instruction,
)
from paper_stm_method.semantics.obligations import CandidateIssue


def candidate_payload():
    return dict(
        contract_id="NL-CONTRACT-NL1-ACTION", locus_kind="state", locus_names=["A"],
        property="state_action", violation_direction="missing", evidence_types=["action_fact"],
        title="Required action is absent", requirement_quote="A performs the required action.",
        element_refs=["state:A:line:2"], source_refs=["NL1"],
        expected="A performs the required action.", observed="A declares no action.",
        strongest_rebuttal="An exact inherited action could satisfy the requirement.",
        reason="The supplied exact action inventory is empty.", basis="NL1 and state:A:line:2",
    )


def test_provider_contracts_remove_execution_fields_without_mutating_full():
    full = workflow.GroundingResponse.model_json_schema()
    for model in (SemanticContractResponse, SemanticContractCompletionResponse,
                  SemanticGroundingResponse, SemanticDecisionResponse):
        schema = json.dumps(model.model_json_schema())
        for fragment in ("predicate_id", "predicate_inputs", "frozen predicate", "predicate/backend"):
            assert fragment not in schema
    assert workflow.GroundingResponse.model_json_schema() == full
    assert "predicate_inputs" in json.dumps(full)
    payload = candidate_payload()
    assert SemanticCandidate.model_validate(payload).contract_id == payload["contract_id"]
    for field, value in (("predicate_id", None), ("predicate_inputs", {})):
        with pytest.raises(ValidationError):
            SemanticCandidate.model_validate({**payload, field: value})


def test_semantic_contract_retains_cross_field_validation():
    payload = dict(
        contract_id="NL-CONTRACT-NL1-CARDINALITY", segment_id="NL1", quote="There are two modes.",
        normative_statement="The owner contains two modes.", locus_kind="composite", locus_names=["Owner"],
        property="cardinality", expected_direction="must_equal", violation_direction="mismatched",
        evidence_types=["closed_model_inventory"], scope="Owner", source_refs=["NL1"],
        reason="The requirement explicitly counts modes.", basis="NL1",
    )
    with pytest.raises(ValidationError, match="requires cardinality_requirement"):
        SemanticContract.model_validate(payload)


def test_system_instructions_keep_semantic_checks_without_predicate_guidance():
    for name in ("CONTRACT_SYSTEM_PROMPT", "DISCOVERY_GROUNDING_SYSTEM_PROMPT", "D_SYSTEM_PROMPT"):
        original = getattr(workflow, name)
        projected = project_instruction(original)
        assert not re.search(r"\b(?:S[1-5]|G[1-3]|R[1-3]|V1)\b|predicate_id|predicate_inputs|backend|registry", projected)
        assert "ground truth" in projected
        assert "reason" in projected and "basis" in projected
        assert getattr(workflow, name) == original
    grounding = project_instruction(workflow.DISCOVERY_GROUNDING_SYSTEM_PROMPT)
    assert "Inspection-equivalent facts" in grounding
    assert "Respect protected compiler-macro boundaries" in grounding
    assert "Cardinality grounding protocol" in grounding


@pytest.mark.parametrize("precise,grounding,emitted,level", [
    (True, "established", True, "W1"),
    (True, "not_established", False, "W1"),
    (False, "established", False, "W0"),
])
def test_semantic_evidence_needs_binding_and_adjudication(precise, grounding, emitted, level):
    candidate = CandidateIssue.model_validate(candidate_payload())
    binding = BindingResult(
        precise=precise, element_refs=candidate.element_refs, source_refs=candidate.source_refs,
        reason="Exact fixture references.", basis="Fixture model inventory.",
    )
    semantic = SemanticAdjudication(
        obligation_id="example:r1:i0", grounding=grounding, violated_obligation=candidate.expected,
        strongest_defeater=None, defeater_kind="none", defeater_disposition="defeated",
        reason="The supplied facts decide the action obligation.", basis="NL1 and fixture inventory.",
    )
    record = build_semantic_evidence_record(
        obligation_id=semantic.obligation_id, candidate=candidate, binding=binding,
        source_attribution={"fixture": True}, retry_records=[], semantic_adjudication=semantic,
    )
    assert record["issue_emitted"] is emitted
    assert record["witness_level"] == level
    assert record["plan"] is record["receipt"] is record["execution_receipt"] is None
    assert record["execution_status"] == "disabled_by_ablation"
    assert record["audit_bundle"] is None
