"""Standalone provider-free smoke test shipped with the method release."""

from __future__ import annotations

import hashlib
from pathlib import Path
from types import SimpleNamespace

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
from paper_stm_method.tools import replay


def test_packaged_resources_and_synthetic_fcstm_fixture_load_without_provider() -> None:
    """The released package loads its registry and a minimal FCSTM fixture offline."""

    registry = load_registry()
    source = (Path(__file__).parent / "fixtures" / "minimal.fcstm").read_text(
        encoding="utf-8"
    )
    model = parse_fcstm(source)

    assert registry.registry_hash == "sha256:38fa2e8060ff822836a3e6437a271998690d36cf60822053316eb21cda2015ca"
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


def test_v3_milliseconds_is_outside_the_native_executable_fragment() -> None:
    """The soundness gate must agree with V3's discrete backend contract."""

    source = (Path(__file__).parent / "fixtures" / "minimal.fcstm").read_text(
        encoding="utf-8"
    )
    model = parse_fcstm(source)
    native = load_native_document(source)
    assessment = assess_soundness(
        "V3",
        {
            "p": "Idle",
            "q": "Active",
            "bound": 1,
            "unit": "milliseconds",
            "scope": "cold",
        },
        model=model,
        model_hash=native.source_hash,
    )

    assert assessment.satisfied is False


def test_r1_publication_audit_supplies_exact_polarity_claim_scope() -> None:
    """The paper-side audit records claim scope without rewriting runtime W."""

    audit = load_publication_eligibility_audit(load_registry())

    assert default_publication_audit_path().is_file()
    assert audit.catalog_hash is not None
    assert audit.by_predicate["S1"] == {"true": True, "false": True}
    assert audit.by_predicate["G2"] == {"true": True, "false": True}
    assert audit.by_predicate["V5"] == {"true": True, "false": True}


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


def test_v5_true_keeps_w2_but_not_the_strongest_invariant_claim() -> None:
    """A bounded pass is an executed receipt, not an unbounded invariant proof."""

    typed_inputs = {
        "predicate_id": "V5",
        "state": "Idle",
        "expected": 1,
        "initial_scope": "cold",
    }
    model_hash = "sha256:" + "2" * 64
    plan = SimpleNamespace(
        plan_id="fixture-v5-plan",
        predicate_id="V5",
        inputs=SimpleNamespace(model_dump=lambda mode: typed_inputs),
        formal_program="ASSERT V5",
        formal_program_hash="sha256:" + "5" * 64,
        input_shape_valid=True,
        binding_complete=True,
        backend_available=True,
        soundness_fragment_satisfied=True,
        binding_precise=True,
        predicate_registered=True,
        artifact_attribution_complete=True,
        publication_eligibility_by_polarity={"true": False, "false": True},
    )
    attribution = {
        "requirement": {"pair_id": "0001", "obligation_id": "0001:r1:i1"},
        "model": {"hash": model_hash},
        "plan": {
            "plan_id": "fixture-v5-plan",
            "predicate_id": "V5",
            "typed_inputs_hash": _canonical_hash(typed_inputs),
            "compiled_program_hash": "sha256:" + "5" * 64,
        },
        "receipt": {"receipt_id": "0001:r1:i1:receipt"},
        "instance_authority": {
            "requirement_quote": "Idle remains occupied.",
            "source_refs": ["NL2"],
            "binding_element_refs": ["state:Idle:line:1"],
            "binding_precise": True,
        },
    }
    common = {
        "pair_id": "0001",
        "run_id": "0" * 32,
        "contract_id": "fixture-contract",
        "obligation_id": "0001:r1:i1",
        "plan": plan,
        "source_attribution": attribution,
        "model_hash": model_hash,
    }
    passed = build_predicate_execution_receipt(
        **common,
        receipt=RawReceipt(
            receipt_id="0001:r1:i1:receipt",
            backend="fixture",
            terminal_state="completed",
            verdict="true",
            reason="The bounded search found no violation.",
            basis="Provider-free fixture.",
        ),
    )
    violated = build_predicate_execution_receipt(
        **common,
        receipt=RawReceipt(
            receipt_id="0001:r1:i1:receipt",
            backend="fixture",
            terminal_state="completed",
            verdict="false",
            reason="The bounded search found a violation.",
            basis="Provider-free fixture.",
        ),
    )

    assert passed["execution_state"] == "completed"
    assert passed["witness_level"] == "W2"
    assert violated["witness_level"] == "W2"


def test_missing_claim_scope_rule_does_not_rewrite_a_completed_receipt() -> None:
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
    receipt = RawReceipt(
        receipt_id="0001:r1:i2:receipt",
        backend="fixture",
        terminal_state="completed",
        verdict="true",
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
    assert execution["predicate_verdict"] == "true"
    assert execution["witness_level"] == "W2"
    assert execution["w2_publication_eligible"] is False


def test_replay_keeps_the_historical_program_identity_when_loading_publication_audit() -> None:
    """The current eligibility catalog must not rewrite an executed program hash."""

    program = "ASSERT S1"
    program_hash = "sha256:" + hashlib.sha256(program.encode("utf-8")).hexdigest()
    model_hash = "sha256:" + "2" * 64
    plan = replay._replay_plan(
        {
            "predicate_id": "S1",
            "obligation_id": "0001:r1:i3",
            "binding": {
                "precise": True,
                "element_refs": ["state:Idle:line:1"],
                "source_refs": ["NL4"],
                "reason": "Fixture binding.",
                "basis": "Provider-free fixture.",
            },
            "plan": {
                "inputs": {
                    "predicate_id": "S1",
                    "kind": "state",
                    "element": "Idle",
                    "scope": "all",
                    "model_hash": model_hash,
                },
                "formal_program": program,
                "formal_program_hash": program_hash,
                "assumptions": [],
            },
            "source_attribution": {
                "requirement": {},
                "model": {},
                "plan": {},
                "receipt": {},
            },
        },
        load_registry(),
    )

    assert plan.formal_program == program
    assert plan.formal_program_hash == program_hash
    assert plan.publication_audit_hash is not None


def test_replay_rejects_any_issue_set_change() -> None:
    """Publication eligibility replay must never rewrite frozen issue publication."""

    record = {
        "pair_id": "0001",
        "obligation_id": "0001:r1:i4",
        "issue_id": "0001:r1:issue:4",
        "historical_witness_level": "W2",
        "witness_level": "W1",
        "d_level": "D2",
        "historical_issue_emitted": True,
        "issue_emitted": False,
        "replay_change": "other_protocol_update",
        "receipt": {"terminal_state": "completed", "verdict": "false"},
        "execution_receipt": {
            "artifact_attribution_complete": False,
            "w2_publication_eligible": False,
            "failure_kind": None,
            "execution_state": "completed",
            "independent_semantic_basis": True,
        },
        "audit_bundle": None,
        "plan": {},
        "source_attribution": {},
        "reason": "Fixture.",
        "basis": "Provider-free fixture.",
    }

    summary = replay._build_summary("0" * 32, "1" * 32, [record])

    assert summary["semantic_identity_changed_report_ids"] == ["0001:r1:issue:4"]
    assert summary["acceptance"]["frozen_issue_emission_unchanged"] is False
