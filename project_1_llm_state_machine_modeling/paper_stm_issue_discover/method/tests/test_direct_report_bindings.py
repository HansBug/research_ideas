"""Every predicate accepts the exact identities advertised by the A3 prompt."""

from types import SimpleNamespace

import pytest

from paper_stm_method.backends import run_backend
from paper_stm_method.orchestration.direct_report import execution_candidate
from paper_stm_method.semantics.obligations import CandidateIssue
from pipeline.evidence_discovery.tests.test_native_backend_conformance import _fixture_cases, _plan


@pytest.mark.parametrize("predicate", ("S1", "S2", "S3", "S4", "S5", "G1", "G2", "G3", "R1", "R2", "R3", "V1"))
def test_exact_catalog_refs_reach_real_backend(predicate):
    fixture = _fixture_cases()[predicate]
    model = fixture["model"]
    refs = {key: node.ref for node in (*model.states, *model.events) for key in (node.name, node.canonical_path)}

    def catalog_refs(value):
        if isinstance(value, str):
            return refs.get(value, value)
        if isinstance(value, (list, tuple)):
            return [catalog_refs(item) for item in value]
        if isinstance(value, dict):
            return {key: catalog_refs(item) for key, item in value.items()}
        return value

    candidate = CandidateIssue(
        title="Fixture", contract_id="NL-CONTRACT-A3-0", requirement_quote="Fixture", source_refs=["plantuml:line:1"],
        locus_kind="state", locus_names=["A"], property="other", violation_direction="missing",
        expected="Fixture", observed="Fixture", reason="Fixture", basis="Fixture", strongest_rebuttal="Fixture",
        evidence_types=["source_identity"], predicate_id=predicate,
        predicate_inputs=catalog_refs(fixture["positive"]), element_refs=[],
    )
    adapted = execution_candidate(candidate, SimpleNamespace(model=model))
    receipt = run_backend(_plan(predicate, adapted.predicate_inputs), model, "a3:identity-fixture")
    assert receipt.terminal_state == "completed"
    assert receipt.verdict == "true"
    assert adapted.expected == candidate.expected and adapted.observed == candidate.observed
