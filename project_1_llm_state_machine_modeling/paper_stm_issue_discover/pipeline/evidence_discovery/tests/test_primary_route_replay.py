"""Regression tests for the provider-free primary-route A/B cohort boundary."""

from __future__ import annotations

import pytest

from pipeline.evidence_discovery.route_replay import (
    _contracts_and_grounding,
    _predicate_null_evidence_rows,
)
from pipeline.evidence_discovery.semantics import GroundingResponse, NLContract


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
