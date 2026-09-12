"""Standalone provider-free smoke test shipped with the method release."""

from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from paper_stm_method.inputs import parse_fcstm
from paper_stm_method.inputs.fcstm_native_projection import load_native_document
from paper_stm_method.compiler.soundness import assess_soundness
from paper_stm_method.compiler.publication_eligibility import (
    default_publication_audit_path,
    load_publication_eligibility_audit,
)
from paper_stm_method.evidence.receipts import (
    RawReceipt,
    _canonical_hash,
    build_predicate_execution_receipt,
)
from paper_stm_method.registry import load_registry
from paper_stm_method.orchestration import runner


def test_packaged_resources_and_synthetic_fcstm_fixture_load_without_provider() -> None:
    """The released package loads its registry and a minimal FCSTM fixture offline."""

    registry = load_registry()
    source = (Path(__file__).parent / "fixtures" / "minimal.fcstm").read_text(
        encoding="utf-8"
    )
    model = parse_fcstm(source)

    assert registry.registry_hash == "sha256:27e6bee263a37079cb86aa5dfdc904e3ba9711533b6cb1c91e9d911912d7d42d"
    assert {state.name for state in model.states} >= {"Root", "Idle", "Active"}


def test_release_provenance_fallback_is_fail_closed_without_a_packaged_manifest(monkeypatch) -> None:
    """A source checkout without Git or generated package manifest cannot claim a live provenance."""

    monkeypatch.setattr(runner, "_git_source_provenance", lambda: None)
    monkeypatch.setattr(runner, "_release_source_provenance", lambda: None)
    assert runner._source_provenance()["source_commit"] == "unknown"


def test_packaged_release_manifest_verifies_its_embedded_commit() -> None:
    """A built release exposes verified provenance without relying on an environment variable."""

    provenance = runner._release_source_provenance()
    if provenance is None:
        return
    assert len(provenance["source_commit"]) == 40
    assert provenance["source_branch"] == "package-release"
    assert provenance["source_dirty"] is False


def test_r1_publication_audit_supplies_exact_polarity_claim_scope() -> None:
    """Source audits supply claim scope; verified releases without one fail closed."""

    registry = load_registry()
    audit = load_publication_eligibility_audit(registry)

    if runner._release_source_provenance() is not None:
        assert not default_publication_audit_path().exists()
        assert audit.catalog_hash is None
        assert audit.by_predicate == {
            predicate_id: {"true": False, "false": False}
            for predicate_id in registry.predicates
        }
        return

    assert default_publication_audit_path().is_file()
    assert audit.catalog_hash is not None
    assert set(audit.by_predicate) == set(registry.predicates)
    assert audit.by_predicate["G2"] == {"true": True, "false": True}
    assert audit.by_predicate["S1"] == {"true": True, "false": True}


def test_malformed_publication_audit_fails_closed(tmp_path: Path) -> None:
    """A missing or malformed paper audit cannot promote any predicate polarity to W2."""

    catalog = tmp_path / "current_source_catalog.json"
    catalog.write_text('{"registry_version":"wrong"}', encoding="utf-8")

    audit = load_publication_eligibility_audit(load_registry(), catalog_path=catalog)

    assert audit.catalog_hash is None
    assert all(
        not eligible
        for rule in audit.by_predicate.values()
        for eligible in rule.values()
    )


def test_empty_instance_authority_cannot_promote_a_completed_receipt_to_w2() -> None:
    """A model hash alone cannot authorize a requirement-relative W2 claim."""

    typed_inputs = {"predicate_id": "S1", "state": "Idle"}
    plan = SimpleNamespace(
        plan_id="fixture-plan",
        predicate_id="S1",
        inputs=SimpleNamespace(model_dump=lambda mode: typed_inputs),
        formal_program="ASSERT S1",
        formal_program_hash="sha256:" + "1" * 64,
        input_shape_valid=True,
        binding_complete=True,
        backend_available=True,
        soundness_fragment_satisfied=True,
        binding_precise=True,
        predicate_registered=True,
        artifact_attribution_complete=True,
        publication_eligibility_by_polarity={"true": True, "false": True},
    )
    receipt = RawReceipt(
        receipt_id="0001:r1:i0:receipt",
        backend="fixture",
        terminal_state="completed",
        verdict="false",
        reason="Fixture completed with a Boolean result.",
        basis="Provider-free fixture.",
    )
    base = {
        "requirement": {"pair_id": "0001", "obligation_id": "0001:r1:i0"},
        "model": {"hash": "sha256:" + "2" * 64},
        "plan": {
            "plan_id": "fixture-plan",
            "predicate_id": "S1",
            "typed_inputs_hash": _canonical_hash(typed_inputs),
            "compiled_program_hash": "sha256:" + "1" * 64,
        },
        "receipt": {"receipt_id": receipt.receipt_id},
    }
    incomplete = build_predicate_execution_receipt(
        pair_id="0001", run_id="0" * 32, contract_id="fixture-contract",
        obligation_id="0001:r1:i0", plan=plan, receipt=receipt,
        source_attribution=base,
        model_hash="sha256:" + "2" * 64,
    )
    complete = build_predicate_execution_receipt(
        pair_id="0001", run_id="0" * 32, contract_id="fixture-contract",
        obligation_id="0001:r1:i0", plan=plan, receipt=receipt,
        source_attribution={
            **base,
            "instance_authority": {
                "requirement_quote": "The system enters Idle.",
                "source_refs": ["NL1"],
                "binding_element_refs": ["state:Idle:line:1"],
                "binding_precise": True,
            },
        },
        model_hash="sha256:" + "2" * 64,
    )

    assert incomplete["witness_level"] == "W1"
    assert incomplete["execution_state"] == "completed"
    assert incomplete["execution_status"] == "executed"
    assert incomplete["predicate_verdict"] == "false"
    assert incomplete["failure_kind"] is None
    assert complete["witness_level"] == "W2"


def test_w2_requires_an_identity_bound_attribution_chain() -> None:
    """Every source-attribution identity must match the executed plan and receipt."""

    typed_inputs = {"predicate_id": "S1", "state": "Idle"}
    model_hash = "sha256:" + "2" * 64
    plan = SimpleNamespace(
        plan_id="fixture-plan",
        predicate_id="S1",
        inputs=SimpleNamespace(model_dump=lambda mode: typed_inputs),
        formal_program="ASSERT S1",
        formal_program_hash="sha256:" + "1" * 64,
        input_shape_valid=True,
        binding_complete=True,
        backend_available=True,
        soundness_fragment_satisfied=True,
        binding_precise=True,
        predicate_registered=True,
        artifact_attribution_complete=True,
        publication_eligibility_by_polarity={"true": True, "false": True},
    )
    receipt = RawReceipt(
        receipt_id="0001:r1:i0:receipt",
        backend="fixture",
        terminal_state="completed",
        verdict="false",
        reason="Fixture completed with a Boolean result.",
        basis="Provider-free fixture.",
    )
    complete = {
        "requirement": {"pair_id": "0001", "obligation_id": "0001:r1:i0"},
        "model": {"hash": model_hash},
        "plan": {
            "plan_id": "fixture-plan",
            "predicate_id": "S1",
            "typed_inputs_hash": _canonical_hash(typed_inputs),
            "compiled_program_hash": "sha256:" + "1" * 64,
        },
        "receipt": {"receipt_id": receipt.receipt_id},
        "instance_authority": {
            "requirement_quote": "The system enters Idle.",
            "source_refs": ["NL1"],
            "binding_element_refs": ["state:Idle:line:1"],
            "binding_precise": True,
        },
    }
    for mutated in (
        {**complete, "requirement": {"pair_id": "9999", "obligation_id": "0001:r1:i0"}},
        {**complete, "model": {"hash": "sha256:" + "3" * 64}},
        {**complete, "plan": {**complete["plan"], "typed_inputs_hash": "sha256:" + "4" * 64}},
        {**complete, "receipt": {"receipt_id": "another:receipt"}},
    ):
        execution = build_predicate_execution_receipt(
            pair_id="0001",
            run_id="0" * 32,
            contract_id="fixture-contract",
            obligation_id="0001:r1:i0",
            plan=plan,
            receipt=receipt,
            source_attribution=mutated,
            model_hash=model_hash,
        )
        assert execution["witness_level"] == "W1"
        assert execution["execution_state"] == "completed"
        assert execution["execution_status"] == "executed"
        assert execution["predicate_verdict"] == "false"
        assert execution["failure_kind"] is None


@pytest.mark.parametrize("predicate_verdict", ("true", "false"))
@pytest.mark.parametrize("eligible", (None, False, True))
def test_claim_scope_rule_does_not_rewrite_a_completed_receipt(predicate_verdict, eligible) -> None:
    """Claim-scope metadata never erases a source-bound executed witness."""

    typed_inputs = {"predicate_id": "S1", "state": "Idle"}
    plan = SimpleNamespace(
        plan_id="fixture-no-publication-rule",
        predicate_id="S1",
        inputs=SimpleNamespace(model_dump=lambda mode: typed_inputs),
        formal_program="ASSERT S1",
        formal_program_hash="sha256:" + "1" * 64,
        input_shape_valid=True,
        binding_complete=True,
        backend_available=True,
        soundness_fragment_satisfied=True,
        binding_precise=True,
        predicate_registered=True,
        artifact_attribution_complete=True,
    )
    if eligible is not None:
        plan.publication_eligibility_by_polarity = {"true": eligible, "false": eligible}
    receipt = RawReceipt(
        receipt_id="0001:r1:i2:receipt",
        backend="fixture",
        terminal_state="completed",
        verdict=predicate_verdict,
        reason="Fixture completed with a Boolean result.",
        basis="Provider-free fixture.",
    )
    attribution = {
        "requirement": {"pair_id": "0001", "obligation_id": "0001:r1:i2"},
        "model": {"hash": "sha256:" + "2" * 64},
        "plan": {
            "plan_id": plan.plan_id,
            "predicate_id": plan.predicate_id,
            "typed_inputs_hash": _canonical_hash(typed_inputs),
            "compiled_program_hash": plan.formal_program_hash,
        },
        "receipt": {"receipt_id": receipt.receipt_id},
        "instance_authority": {
            "requirement_quote": "The system remains Idle.",
            "source_refs": ["NL3"],
            "binding_element_refs": ["state:Idle:line:1"],
            "binding_precise": True,
        },
    }
    execution = build_predicate_execution_receipt(
        pair_id="0001",
        run_id="0" * 32,
        contract_id="fixture-contract",
        obligation_id="0001:r1:i2",
        plan=plan,
        receipt=receipt,
        source_attribution=attribution,
        model_hash="sha256:" + "2" * 64,
    )

    assert execution["execution_state"] == "completed"
    assert execution["execution_status"] == "executed"
    assert execution["predicate_verdict"] == predicate_verdict
    assert execution["witness_level"] == "W2"
    assert execution["w2_publication_eligible"] is bool(eligible)
