"""Regression tests for immutable provider-free W-state replay."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.replay import run_provider_free_replay


def _hash(seed: str) -> str:
    """Return a deterministic SHA-256-shaped fixture value."""

    return "sha256:" + seed * 64


def _semantic(obligation_id: str) -> dict[str, object]:
    """Return an established semantic fact independent of backend failure."""

    return {
        "obligation_id": obligation_id,
        "grounding": "established",
        "violated_obligation": "The supplied requirement is violated by the closed model fact.",
        "strongest_defeater": None,
        "defeater_kind": "none",
        "defeater_disposition": "defeated",
        "reason": "The closed requirement and exact model binding establish the violation.",
        "basis": "fixture NL clause and closed FCSTM fact",
    }


def _record(
    *,
    index: int,
    predicate_id: str,
    inputs: dict[str, object],
    terminal_state: str,
    verdict: str,
    historical_witness_level: str,
    semantic: dict[str, object] | None,
) -> dict[str, object]:
    """Build one old-shape evidence record without calling a backend or provider."""

    obligation_id = f"0001:r1:i{index}"
    contract_id = f"NL-CONTRACT-fixture-{index}"
    input_payload = {
        "predicate_id": predicate_id,
        "schema_version": "evidence-discovery.predicate-inputs.v1",
        "element_refs": ["transition:line:1"],
        "model_hash": _hash("a"),
        **inputs,
    }
    return {
        "schema": "evidence-discovery.evidence_record.v1",
        "obligation_id": obligation_id,
        "contract_id": contract_id,
        "issue_id": f"0001:r1:issue:{index}",
        "predicate_id": predicate_id,
        "predicate_inputs": dict(inputs),
        "locus_kind": "transition",
        "locus_names": ["FixtureTransition"],
        "property": "guard" if predicate_id == "S5" else "state_action",
        "violation_direction": "wrong_guard" if predicate_id == "S5" else "missing",
        "evidence_types": ["semantic_comparison", "transition_fact"],
        "title": "Fixture predicate obligation",
        "requirement_quote": "The fixture requires the exact predicate condition.",
        "element_refs": ["transition:line:1"],
        "source_refs": ["fixture:nl:1"],
        "expected": "The exact predicate must hold.",
        "observed": "The stored raw receipt records the old backend outcome.",
        "strongest_rebuttal": "No competing fixture interpretation survives.",
        "candidate_reason": "Fixture candidate preserves a precise semantic issue.",
        "candidate_basis": "fixture source and closed model",
        "reason": "Historical deterministic disposition.",
        "basis": "historical source artifact",
        "binding": {
            "precise": True,
            "element_refs": ["transition:line:1"],
            "source_refs": ["fixture:nl:1"],
            "reason": "The fixture carrier resolves exactly.",
            "basis": "fixture closed ModelIR",
        },
        "plan": {
            "plan_id": f"{obligation_id}:plan",
            "predicate_id": predicate_id,
            "registry_version": "four-family-19-core.v1",
            "inputs": input_payload,
            "assumptions": ["closed_fcstm_input"],
            "formal_program": f"ASSERT {predicate_id} fixture",
            "formal_program_hash": _hash("b"),
            "source_audit_status": "candidate",
            "source_gate_passed": False,
        },
        "receipt": {
            "receipt_id": f"{obligation_id}:receipt",
            "backend": f"native:{predicate_id}",
            "terminal_state": terminal_state,
            "verdict": verdict,
            "reason": "Stored fixture raw backend result.",
            "basis": "fixture native backend receipt",
            "run_metadata": {"algorithm_version": "fixture-native.v1"},
        },
        "retry_records": [],
        "semantic_adjudication": semantic,
        "source_attribution": {
            "requirement": {"pair_id": "0001", "hash": _hash("c")},
            "model": {"hash": _hash("a")},
            "plan": {"plan_id": f"{obligation_id}:plan"},
            "receipt": {"receipt_id": f"{obligation_id}:receipt"},
            "roles": {"natural_language": "normative_source_contract", "fcstm": "closed_model_execution"},
            "input_context": {"artifact_hashes": {"fcstm": _hash("a"), "nl": _hash("c")}},
            "reason": "Fixture artifact chain is complete.",
            "basis": "fixture attribution",
        },
        "witness_level": historical_witness_level,
        "d_level": "D2" if semantic is not None else "D_UNRESOLVED",
        "issue_emitted": semantic is not None and verdict == "false",
    }


def _source_run(tmp_path: Path) -> Path:
    """Write a compact immutable old-shape run for replay regression coverage."""

    source = tmp_path / "source" / "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    method_path = source / "method" / "0001" / "round-1.json"
    method_path.parent.mkdir(parents=True)
    records = [
        _record(
            index=0,
            predicate_id="S5",
            inputs={"transition": "transition:line:1", "guard": "x > 0"},
            terminal_state="completed",
            verdict="false",
            historical_witness_level="W1",
            semantic=_semantic("0001:r1:i0"),
        ),
        _record(
            index=1,
            predicate_id="S4",
            inputs={"state": "state:Fixture:line:1", "phase": "operating", "action": "Act"},
            terminal_state="completed",
            verdict="false",
            historical_witness_level="W2",
            semantic=_semantic("0001:r1:i1"),
        ),
        _record(
            index=2,
            predicate_id="S5",
            inputs={"transition": "transition:line:1", "guard": "x > 0"},
            terminal_state="completed",
            verdict="true",
            historical_witness_level="W2",
            semantic=_semantic("0001:r1:i2"),
        ),
        _record(
            index=3,
            predicate_id="S5",
            inputs={"transition": "transition:line:1", "guard": "x > 0"},
            terminal_state="timeout",
            verdict="unknown",
            historical_witness_level="W1",
            semantic=None,
        ),
    ]
    method_path.write_text(
        json.dumps(
            {
                "run_id": "a" * 32,
                "pair_id": "0001",
                "evidence_records": records,
                "report_issue_clusters": [],
            }
        ),
        encoding="utf-8",
    )
    (source / "run_manifest.json").write_text(
        json.dumps({"run_id": "a" * 32}), encoding="utf-8"
    )
    (source / "summary.json").write_text(
        json.dumps({"source_commit": "f" * 40, "method_cell_count": 1}), encoding="utf-8"
    )
    return source


def test_provider_free_replay_recovers_w2_and_rejects_illegal_s4(tmp_path: Path) -> None:
    """Replay keeps stored truth while applying current typed W and failure rules."""

    source = _source_run(tmp_path)
    result = run_provider_free_replay(
        source_run=source,
        output_parent=tmp_path / "replays",
    )
    replay_root = Path(result["replay_root"])
    summary = json.loads((replay_root / "summary.json").read_text(encoding="utf-8"))
    payload = json.loads((replay_root / "replay_evidence.json").read_text(encoding="utf-8"))
    records = {record["obligation_id"]: record for record in payload["records"]}

    assert summary["completed_boolean_recoveries"] == 1
    assert summary["invalid_typed_input_rejections"] == 1
    assert summary["bibliography_runtime_w1_count"] == 0
    assert summary["unexplained_completed_boolean_w1_count"] == 0
    assert summary["invalid_typed_w2_count"] == 0
    assert summary["failure_as_violation_count"] == 0
    assert summary["w2_audit_closure_complete"] is True
    assert records["0001:r1:i0"]["witness_level"] == "W2"
    assert records["0001:r1:i0"]["issue_emitted"] is True
    assert records["0001:r1:i1"]["witness_level"] == "W1"
    assert records["0001:r1:i1"]["execution_receipt"]["failure_kind"] == "invalid_input"
    assert records["0001:r1:i2"]["witness_level"] == "W2"
    assert records["0001:r1:i2"]["issue_emitted"] is False
    assert records["0001:r1:i3"]["witness_level"] == "W1"
    assert records["0001:r1:i3"]["d_level"] == "D_UNRESOLVED"
    assert records["0001:r1:i3"]["issue_emitted"] is False
    assert "source_gate_passed" not in (replay_root / "replay_evidence.json").read_text(encoding="utf-8")
    assert "source_audit_status" not in (replay_root / "replay_evidence.json").read_text(encoding="utf-8")


def test_provider_free_replay_refuses_to_overwrite_immutable_output(tmp_path: Path) -> None:
    """A second identical replay cannot overwrite the first immutable artifact."""

    source = _source_run(tmp_path)
    output_parent = tmp_path / "replays"
    run_provider_free_replay(source_run=source, output_parent=output_parent)
    with pytest.raises(FileExistsError, match="immutable replay output already exists"):
        run_provider_free_replay(source_run=source, output_parent=output_parent)
