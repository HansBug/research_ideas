from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.evidence_discovery.reporting.method_composite import (
    CompositeBuildProvenance,
    CompositeCellReceipt,
    CompositeFileReceipt,
    CompositeReplacementReceipt,
    CompositeRetryAudit,
    CompositeSourceRun,
    MethodCompositeManifest,
    MethodCompositeSummary,
    build_method_composite,
)

REGISTRY_HASH = "sha256:" + "9" * 64
CONTRACT_HASH = "sha256:" + "8" * 64
INPUT_HASHES = {
    "0001": "sha256:" + "1" * 64,
    "0002": "sha256:" + "2" * 64,
}


def _cell(
    *,
    run_id: str,
    source_commit: str,
    pair_id: str,
    cost: float,
    schema_failures: int = 0,
) -> dict[str, object]:
    failures = [
        {
            "turn": index + 1,
            "validation_error": "fixture schema mismatch",
        }
        for index in range(schema_failures)
    ]
    return {
        "schema": "evidence-discovery.method_cell.v8",
        "run_id": run_id,
        "run_contract_hash": CONTRACT_HASH,
        "source_provenance": {
            "source_commit": source_commit,
            "source_branch": "fixture",
            "source_dirty": False,
            "reason": "Fixture method source.",
            "basis": "Fixture commit.",
        },
        "pair_id": pair_id,
        "pair_input_hash": INPUT_HASHES[pair_id],
        "round": 1,
        "status": "completed",
        "prompt_hash": None,
        "context_manifest": None,
        "input_hashes": {},
        "stage_outputs": {},
        "stage_receipts": [],
        "model_output": {
            "issues": [],
            "reason": "Fixture output.",
            "basis": "Fixture basis.",
        },
        "llm_calls": [
            {
                "attempts": [
                    {
                        "provider_error": False,
                        "retry_records": [],
                        "schema_validation_failures": failures,
                    }
                ],
                "usage": [{"status": "completed"}],
            }
        ],
        "llm_call": {"cost": {"total_usd": cost}},
        "eligible": True,
        "eligibility_reasons": ["Fixture cell is terminal."],
        "evidence_records": [],
        "predicate_execution_receipts": [],
        "report_issue_clusters": [
            {
                "issue_id": f"{pair_id}:r1:issue:0",
                "title": "Fixture issue",
            }
        ],
        "errors": [],
        "reason": "Fixture method cell.",
        "basis": "Fixture identity and cost.",
    }


def _write_source(
    root: Path,
    *,
    run_id: str,
    source_commit: str,
    pairs: tuple[str, ...],
    costs: dict[str, float],
    schema_failures: dict[str, int] | None = None,
) -> None:
    schema_failures = schema_failures or {}
    root.mkdir(parents=True)
    manifest = {
        "run_id": run_id,
        "status": "completed",
        "source_provenance": {
            "source_commit": source_commit,
            "source_branch": "fixture",
            "source_dirty": False,
        },
        "registry_version": "four-family-19-core.v1",
        "registry_hash": REGISTRY_HASH,
        "profile": "fixture",
        "rounds": 1,
        "selected_pair_ids": list(pairs),
        "scope": "diagnostic_subset",
        "workers": 16,
        "pair_input_hashes": {pair_id: INPUT_HASHES[pair_id] for pair_id in pairs},
    }
    total_cost = 0.0
    for pair_id in pairs:
        cell = _cell(
            run_id=run_id,
            source_commit=source_commit,
            pair_id=pair_id,
            cost=costs[pair_id],
            schema_failures=schema_failures.get(pair_id, 0),
        )
        total_cost += costs[pair_id]
        method_path = root / "method" / pair_id / "round-1.json"
        method_path.parent.mkdir(parents=True)
        method_path.write_text(json.dumps(cell, indent=2) + "\n", encoding="utf-8")
        status = {
            "schema": "evidence-discovery.pair_status.v3",
            "run_id": run_id,
            "run_contract_hash": CONTRACT_HASH,
            "pair_id": pair_id,
            "status": "completed",
            "resume_action": "executed_fresh",
            "started_at": "2026-08-27T00:00:00Z",
            "method_cells": 1,
            "eligible_method_cells": 1,
            "errors": 0,
            "audit_errors": 0,
            "method_cost_usd": costs[pair_id],
            "method_cost_eligible": True,
            "reason": "Fixture pair is terminal.",
            "basis": "Fixture cell and cost.",
        }
        status_path = root / "pairs" / pair_id / "status.json"
        status_path.parent.mkdir(parents=True)
        status_path.write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
        bundle = root / "audit_bundles" / f"{pair_id}:r1:issue:0.json"
        bundle.parent.mkdir(parents=True, exist_ok=True)
        bundle.write_text(json.dumps({"pair_id": pair_id}) + "\n", encoding="utf-8")
    (root / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    (root / "summary.json").write_text(
        json.dumps(
            {
                "run_id": run_id,
                "status": "completed",
                "method_cost_usd": total_cost,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def _provenance() -> CompositeBuildProvenance:
    return CompositeBuildProvenance(
        source_commit="c" * 40,
        source_branch="fixture",
        reason="Fixture composite build.",
        basis="Fixture clean commit.",
    )


def test_method_composite_selects_only_recovery_key_and_closes_all_costs(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    recovery = tmp_path / "recovery"
    _write_source(
        base,
        run_id="a" * 32,
        source_commit="1" * 40,
        pairs=("0001", "0002"),
        costs={"0001": 0.1, "0002": 0.2},
        schema_failures={"0002": 1},
    )
    _write_source(
        recovery,
        run_id="b" * 32,
        source_commit="2" * 40,
        pairs=("0002",),
        costs={"0002": 0.3},
        schema_failures={"0002": 2},
    )
    source_bytes = {
        path: path.read_bytes()
        for root in (base, recovery)
        for path in root.rglob("*.json")
    }

    output = tmp_path / "composite"
    manifest, summary = build_method_composite(
        composite_id="d" * 32,
        base_run_root=base,
        replacement_run_roots=(recovery,),
        output_root=output,
        build_provenance=_provenance(),
    )

    assert len(manifest.cell_receipts) == 2
    assert len(manifest.replacements) == 1
    assert manifest.method_source_commits == ("1" * 40, "2" * 40)
    selected = {row.pair_id: row for row in manifest.cell_receipts}
    assert selected["0001"].source_run_id == "a" * 32
    assert selected["0002"].source_run_id == "b" * 32
    assert selected["0001"].method_artifact.hardlink_identity_preserved is True
    assert selected["0002"].method_artifact.hardlink_identity_preserved is True
    assert summary.selected_result_cost_usd == pytest.approx(0.4)
    assert summary.superseded_cell_cost_usd == pytest.approx(0.2)
    assert summary.unselected_source_cost_usd == pytest.approx(0.0)
    assert summary.method_cost_usd == pytest.approx(0.6)
    assert summary.replacements[0].base_retry_audit.schema_validation_failure_count == 1
    assert selected["0002"].retry_audit.schema_validation_failure_count == 2
    assert json.loads((output / "run_manifest.json").read_text())["schema"] == (
        "evidence-discovery.method-composite.v1"
    )
    assert json.loads((output / "summary.json").read_text())["metrics"]["cost"][
        "total_incurred_usd"
    ] == pytest.approx(0.6)
    assert all(path.read_bytes() == payload for path, payload in source_bytes.items())


def test_method_composite_rejects_recovery_with_different_pair_input(
    tmp_path: Path,
) -> None:
    base = tmp_path / "base"
    recovery = tmp_path / "recovery"
    _write_source(
        base,
        run_id="a" * 32,
        source_commit="1" * 40,
        pairs=("0001", "0002"),
        costs={"0001": 0.1, "0002": 0.2},
    )
    _write_source(
        recovery,
        run_id="b" * 32,
        source_commit="2" * 40,
        pairs=("0002",),
        costs={"0002": 0.3},
    )
    recovery_cell = recovery / "method/0002/round-1.json"
    payload = json.loads(recovery_cell.read_text())
    payload["pair_input_hash"] = "sha256:" + "7" * 64
    recovery_cell.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    with pytest.raises(ValueError, match="replacement pair input mismatch"):
        build_method_composite(
            composite_id="d" * 32,
            base_run_root=base,
            replacement_run_roots=(recovery,),
            output_root=tmp_path / "composite",
            build_provenance=_provenance(),
        )


def test_method_composite_models_document_every_field() -> None:
    for model in (
        CompositeFileReceipt,
        CompositeRetryAudit,
        CompositeSourceRun,
        CompositeCellReceipt,
        CompositeReplacementReceipt,
        CompositeBuildProvenance,
        MethodCompositeManifest,
        MethodCompositeSummary,
    ):
        assert model.__doc__ and model.__doc__.strip()
        assert all(
            field.description and field.description.strip()
            for field in model.model_fields.values()
        )
