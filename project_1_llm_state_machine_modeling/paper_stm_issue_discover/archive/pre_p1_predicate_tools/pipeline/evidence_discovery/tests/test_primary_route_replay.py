"""Regression tests for the provider-free primary-route A/B cohort boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from pipeline.evidence_discovery.route_replay import (
    _contracts_and_grounding,
    _predicate_null_evidence_rows,
    _source_cell_run_id,
    merge_saved_frontier_contracts,
)
from pipeline.evidence_discovery.semantics import CandidateIssue, GroundingResponse, NLContract


def _record(obligation_id: str, predicate_id: str | None, witness_level: str) -> dict[str, object]:
    """Build one minimal historical evidence row for cohort-selection coverage."""

    return {
        "obligation_id": obligation_id,
        "plan": {"predicate_id": predicate_id},
        "witness_level": witness_level,
    }


def test_primary_route_replay_targets_only_final_predicate_null_w1_evidence() -> None:
    """Auxiliary execute candidates and W0/null rows cannot inflate the 88-style cohort."""

    selected = _predicate_null_evidence_rows(
        {
            "evidence_records": [
                _record("fixture:null-w1", None, "W1"),
                _record("fixture:null-w0", None, "W0"),
                _record("fixture:s2-w1", "S2", "W1"),
                _record("fixture:null-w2", None, "W2"),
            ]
        }
    )

    assert list(selected) == ["fixture:null-w1"]
    assert selected["fixture:null-w1"][0] == 0


def test_primary_route_replay_rejects_duplicate_final_evidence_identity() -> None:
    """A source run cannot silently count one final predicate-null obligation twice."""

    with pytest.raises(ValueError, match="duplicate predicate-null W1 evidence"):
        _predicate_null_evidence_rows(
            {
                "evidence_records": [
                    _record("fixture:duplicate", None, "W1"),
                    _record("fixture:duplicate", None, "W1"),
                ]
            }
        )


def _derived_contract() -> NLContract:
    """Build one runner-canonical derived contract for replay merge coverage."""

    return NLContract(
        contract_id="NL-CONTRACT-NL1-DERIVED-fixture",
        segment_id="NL1",
        quote="The required state must be reachable.",
        normative_statement="Exact state A must be reachable from exact state B.",
        locus_kind="state",
        locus_names=("A", "B"),
        property="reachability",
        expected_direction="must_reach",
        violation_direction="unreachable",
        evidence_types=("source_identity", "reachability_fact"),
        scope="B to A reachability",
        source_refs=("NL1",),
        reason="The first grounding lens derives the exact reachability obligation.",
        basis="first grounding lens fixture",
    )


def _grounding(lens: str, contract: NLContract) -> dict[str, object]:
    """Build one sparse grounding branch containing a derived contract."""

    return GroundingResponse(
        lens=lens,
        additional_contracts=[contract],
        reason="The branch emits one sparse derived contract.",
        basis="provider-free replay merge fixture",
    ).model_dump(mode="json")


def test_primary_route_replay_merges_same_typed_contract_identity() -> None:
    """Cross-lens prose differences retain the runner's first execution projection."""

    first = _derived_contract()
    second = first.model_copy(
        update={
            "quote": "A second exact quotation for the same typed obligation.",
            "normative_statement": "The same exact B-to-A reachability relation must hold.",
            "reason": "The second lens independently derives the same typed identity.",
            "basis": "second grounding lens fixture",
        }
    )
    contracts, grounding = _contracts_and_grounding(
        {
            "stage_outputs": {
                "contract_extraction": {"contracts": []},
                "discovery_grounding": {
                    "branches": [
                        _grounding("contract_structure_contrast", first),
                        _grounding("behavior_consequence", second),
                    ]
                },
            }
        }
    )

    assert len(grounding) == 2
    assert contracts[first.contract_id] == first


def test_primary_route_replay_rejects_same_id_with_different_typed_identity() -> None:
    """A branch-local ID cannot collapse different semantic keys during replay."""

    first = _derived_contract()
    conflicting = first.model_copy(update={"property": "universal_reachability"})
    with pytest.raises(ValueError, match="conflicting saved contract identity"):
        _contracts_and_grounding(
            {
                "stage_outputs": {
                    "contract_extraction": {"contracts": []},
                    "discovery_grounding": {
                        "branches": [
                            _grounding("contract_structure_contrast", first),
                            _grounding("behavior_consequence", conflicting),
                        ]
                    },
                }
            }
        )


def test_primary_route_replay_merges_saved_frontier_contract_before_routing() -> None:
    """Saved frontier obligations are typed replay inputs, not absent contracts."""

    contract = _derived_contract()
    candidate = CandidateIssue(
        contract_id=contract.contract_id,
        locus_kind=contract.locus_kind,
        locus_names=contract.locus_names,
        property=contract.property,
        violation_direction=contract.violation_direction,
        evidence_types=contract.evidence_types,
        title="Saved frontier candidate",
        requirement_quote=contract.quote,
        expected=contract.normative_statement,
        observed="The saved frontier retains the exact closed-model observation.",
        strongest_rebuttal="The fixture supplies no alternate source contract.",
        reason="The candidate is backed by the saved derived frontier contract.",
        basis="route replay saved frontier merge fixture",
    )
    cell = {
        "stage_outputs": {
            "execute_batch": {
                "frontier_batch": {
                    "obligations": [
                        {
                            "frontier_id": "route-replay-frontier-1",
                            "kind": "root_reachability",
                            "contract": contract.model_dump(mode="json"),
                            "candidate": candidate.model_dump(mode="json"),
                            "source_contract_ids": [contract.contract_id],
                            "reason": "The fixture persists one typed frontier contract.",
                            "basis": "route replay saved frontier fixture",
                        }
                    ],
                    "reason": "Saved fixture frontier.",
                    "basis": "route replay saved frontier fixture",
                }
            }
        }
    }
    contracts: dict[str, NLContract] = {}

    exclusions = merge_saved_frontier_contracts(cell, contracts)

    assert exclusions == {}
    assert contracts == {contract.contract_id: contract}


def _sha256(path: Path) -> str:
    """Return the receipt-form SHA-256 for one fixture artifact."""

    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def test_primary_route_replay_accepts_hash_closed_composite_cell(tmp_path: Path) -> None:
    """A selected recovery cell retains its original run ID inside a composite."""

    method_path = tmp_path / "method" / "0001" / "round-1.json"
    method_path.parent.mkdir(parents=True)
    method_path.write_text("{}", encoding="utf-8")
    artifact_hash = _sha256(method_path)
    source_cell_run_id = "a" * 32
    cell = {"pair_id": "0001", "round": 1, "run_id": source_cell_run_id}
    manifest = {
        "schema": "evidence-discovery.method-composite.v1",
        "run_id": "b" * 32,
        "cell_receipts": [
            {
                "pair_id": "0001",
                "round": 1,
                "source_run_id": source_cell_run_id,
                "method_artifact": {
                    "composite_path": str(method_path),
                    "source_hash": artifact_hash,
                    "composite_hash": artifact_hash,
                    "hardlink_identity_preserved": True,
                },
            }
        ],
    }

    assert _source_cell_run_id(manifest, tmp_path, method_path, cell) == source_cell_run_id


def test_primary_route_replay_rejects_composite_cell_with_wrong_original_run(
    tmp_path: Path,
) -> None:
    """A composite cannot silently substitute a cell from an unselected run."""

    method_path = tmp_path / "method" / "0001" / "round-1.json"
    method_path.parent.mkdir(parents=True)
    method_path.write_text("{}", encoding="utf-8")
    artifact_hash = _sha256(method_path)
    manifest = {
        "schema": "evidence-discovery.method-composite.v1",
        "run_id": "b" * 32,
        "cell_receipts": [
            {
                "pair_id": "0001",
                "round": 1,
                "source_run_id": "a" * 32,
                "method_artifact": {
                    "composite_path": str(method_path),
                    "source_hash": artifact_hash,
                    "composite_hash": artifact_hash,
                    "hardlink_identity_preserved": True,
                },
            }
        ],
    }

    with pytest.raises(ValueError, match="does not match composite receipt"):
        _source_cell_run_id(
            manifest,
            tmp_path,
            method_path,
            {"pair_id": "0001", "round": 1, "run_id": "c" * 32},
        )
