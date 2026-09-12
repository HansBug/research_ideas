"""Regression tests for frozen domain invariants over native FCSTM carriers."""

from __future__ import annotations

import hashlib
from pathlib import Path

from pipeline.evidence_discovery.backends import run_backend
from pipeline.evidence_discovery.compiler import compile_plan
from pipeline.evidence_discovery.compiler.plans import validate_plan
from pipeline.evidence_discovery.evidence.witness_levels import calculate_witness_level
from pipeline.evidence_discovery.inputs import PairInput, parse_fcstm
from pipeline.evidence_discovery.inputs.context import build_inspection_equivalent_facts
from pipeline.evidence_discovery.registry import load_registry
from pipeline.evidence_discovery.semantics import bind_candidate
from pipeline.evidence_discovery.semantics.domain_invariants import (
    DomainInvariantContract,
    materialize_domain_invariant_contracts,
)


_INITIAL_CONDITIONAL_SOURCE = """
def int x = 0;
state Root {
    state A;
    [*] -> A : Begin + [x >= 0];
}
"""


def _pair(tmp_path: Path) -> PairInput:
    """Build one closed native fixture without a ledger or expected issue."""

    model = parse_fcstm(_INITIAL_CONDITIONAL_SOURCE)
    model_hash = "sha256:" + hashlib.sha256(
        _INITIAL_CONDITIONAL_SOURCE.encode("utf-8")
    ).hexdigest()
    (tmp_path / "nl.txt").write_text(
        "The fixture uses a frozen language invariant.", encoding="utf-8"
    )
    (tmp_path / "fcstm.fcstm").write_text(
        _INITIAL_CONDITIONAL_SOURCE, encoding="utf-8"
    )
    return PairInput(
        pair_id="0000",
        pair_dir=tmp_path,
        nl_text="Fixture requirement text is intentionally not used by the invariant.",
        fcstm_text=_INITIAL_CONDITIONAL_SOURCE,
        plantuml_text="",
        model=model,
        hashes={"fcstm": model_hash},
        inspection_facts=build_inspection_equivalent_facts(model, model_hash),
    )


def _execute(pair: PairInput, contract: DomainInvariantContract):
    """Compile and execute one domain invariant through the production backend."""

    candidate = contract.candidate()
    binding = bind_candidate(candidate, pair.model)
    assert binding.precise
    plan = compile_plan(
        candidate,
        binding,
        load_registry(),
        obligation_id="fixture:r1:domain-invariant",
        round_index=1,
        model=pair.model,
        model_hash=pair.hashes["fcstm"],
    )
    validate_plan(plan)
    receipt = run_backend(plan, pair.model, "fixture:r1:domain-invariant:receipt")
    return candidate, binding, plan, receipt


def test_initial_pseudostate_invariants_are_native_and_executable(tmp_path: Path) -> None:
    """Initial trigger and guard violations keep distinct native W2 receipts."""

    pair = _pair(tmp_path)
    contracts, candidates, dispositions = materialize_domain_invariant_contracts(pair)

    assert {item.predicate_id for item in contracts} == {"S3", "S5"}
    assert {item.predicate_id for item in candidates} == {"S3", "S5"}
    assert {item["status"] for item in dispositions} == {"admitted"}
    assert all(item.authority_ref.startswith("UML-2.5.1") for item in contracts)

    for contract in contracts:
        candidate, binding, plan, receipt = _execute(pair, contract)
        assert contract.candidate_mismatches(candidate) == ()
        assert plan.predicate_id == contract.predicate_id
        assert receipt.terminal_state == "completed"
        assert receipt.verdict == "false"
        assert calculate_witness_level(binding, plan, receipt) == "W2"


def test_domain_invariant_deduplicates_an_exact_existing_candidate(tmp_path: Path) -> None:
    """A matching exact carrier claim is retained once rather than double-published."""

    pair = _pair(tmp_path)
    _contracts, candidates, _dispositions = materialize_domain_invariant_contracts(pair)
    trigger_candidate = next(item for item in candidates if item.predicate_id == "S3")

    duplicate_contracts, duplicate_candidates, dispositions = materialize_domain_invariant_contracts(
        pair,
        existing_candidates=(trigger_candidate,),
    )

    assert len(duplicate_contracts) == 1
    assert [item.predicate_id for item in duplicate_candidates] == ["S5"]
    assert any(item["status"] == "duplicate_exact_candidate" for item in dispositions)
