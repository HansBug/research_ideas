"""Standalone provider-free smoke test shipped with the method release."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from paper_stm_method.inputs import parse_fcstm
from paper_stm_method.inputs.fcstm_native_projection import load_native_document
from paper_stm_method.compiler.soundness import assess_soundness
from paper_stm_method.evidence.receipts import RawReceipt, build_predicate_execution_receipt
from paper_stm_method.registry import load_registry
from paper_stm_method.orchestration import runner


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


def test_empty_instance_authority_cannot_promote_a_completed_receipt_to_w2() -> None:
    """A model hash alone cannot authorize a requirement-relative W2 claim."""

    plan = SimpleNamespace(
        plan_id="fixture-plan",
        predicate_id="S1",
        inputs=SimpleNamespace(model_dump=lambda mode: {"predicate_id": "S1", "state": "Idle"}),
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
        receipt_id="0001:r1:i0:receipt",
        backend="fixture",
        terminal_state="completed",
        verdict="false",
        reason="Fixture completed with a Boolean result.",
        basis="Provider-free fixture.",
    )
    base = {
        "requirement": {"obligation_id": "0001:r1:i0"},
        "model": {"hash": "sha256:" + "2" * 64},
        "plan": {"plan_id": "fixture-plan"},
        "receipt": {"receipt_id": receipt.receipt_id},
    }
    incomplete = build_predicate_execution_receipt(
        pair_id="0001", run_id="0" * 32, contract_id="fixture-contract",
        obligation_id="0001:r1:i0", plan=plan, receipt=receipt,
        source_attribution=base,
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
    )

    assert incomplete["witness_level"] == "W1"
    assert incomplete["failure_kind"] == "attribution_failure"
    assert complete["witness_level"] == "W2"
