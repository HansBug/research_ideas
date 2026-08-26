from __future__ import annotations

import json
import hashlib
from pathlib import Path

import pytest

from pipeline.evidence_discovery.reporting.expected_issue_witness import (
    build_expected_issue_witness_audit,
)
from pipeline.evidence_discovery.reporting.evaluation_summary import (
    build_evaluation_summary,
)
from pipeline.evidence_discovery.reporting.judge_cost_audit import build_judge_cost_audit
from pipeline.evidence_discovery.inputs import FROZEN_PAIR_IDS
from pipeline.evidence_discovery.reporting.applicability import (
    FULL_SCALE_PLANNED_PREDICATES,
)
from pipeline.evidence_discovery.reporting.stage_loss import (
    _predicate_feasibility,
    _resolve_planned_predicate_scope,
    build_stage_loss_audit,
)


def _write_fixture(root: Path) -> tuple[Path, Path]:
    method_root = root / "method-run"
    judge_root = root / "judge-run"
    pair_id = "0004"
    method_root.mkdir(parents=True)
    (method_root / "method" / pair_id).mkdir(parents=True)
    (judge_root / "pairs").mkdir(parents=True)

    (method_root / "run_manifest.json").write_text(
        json.dumps(
            {
                "run_id": "fixture-run",
                "selected_pair_ids": [pair_id],
                "source_provenance": {"source_commit": "fixture-commit"},
                "registry_hash": "fixture-registry",
            }
        ),
        encoding="utf-8",
    )
    (method_root / "summary.json").write_text(
        json.dumps({"metrics": {"method": {"method_diagnostics": 0}}}),
        encoding="utf-8",
    )

    obligation_id = f"{pair_id}:r1:i0"
    issue_id = f"{pair_id}:r1:issue:0"
    contract_id = "fixture-contract"
    receipt = {
        "obligation_id": obligation_id,
        "predicate_id": "S2",
        "execution_status": "executed",
        "terminal_state": "completed",
        "verdict": "violation",
        "typed_inputs_hash": "sha256:typed-inputs",
        "compiled_program_hash": "sha256:compiled-program",
        "receipt_hash": "sha256:receipt",
        "reason": "The exact typed endpoint is absent.",
        "basis": "provider-free stage-loss fixture",
    }
    plan = {
        "plan_id": f"{obligation_id}:plan",
        "predicate_id": "S2",
        "inputs": {"source": "A", "target": "B", "scope": "closed_fcstm"},
        "formal_program": "endpoint_exists(A, B)",
        "formal_program_hash": "sha256:compiled-program",
        "semantics": "exact transition endpoint existence",
    }
    candidate = {
        "obligation_id": obligation_id,
        "contract_id": contract_id,
        "predicate_id": "S2",
        "predicate_inputs": plan["inputs"],
        "element_refs": ["state:A", "state:B"],
        "source_refs": ["NL1"],
        "d_level": "D2",
        "witness_level": "W2",
        "plan": plan,
        "receipt": receipt,
        "issue_emitted": True,
        "issue_id": issue_id,
    }
    evidence = {
        "issue_id": issue_id,
        "obligation_id": obligation_id,
        "contract_id": contract_id,
        "predicate_id": "S2",
        "witness_level": "W2",
        "d_level": "D2",
        "plan": plan,
        "reason": "The exact typed endpoint is absent.",
        "basis": "provider-free stage-loss fixture",
    }
    method_payload = {
        "stage_outputs": {
            "contract_extraction": {
                "contracts": [
                    {
                        "contract_id": contract_id,
                        "segment_id": "NL1",
                        "property": "transition_endpoints",
                        "source_refs": ["NL1"],
                        "reason": "The fixture supplies one typed contract.",
                        "basis": "provider-free stage-loss fixture",
                    }
                ]
            },
            "discovery_grounding": {
                "branches": {
                    "branch": {
                        "semantic_bindings": [
                            {
                                "contract_id": contract_id,
                                "binding_id": "binding-1",
                                "model_element_ref": "state:A",
                                "carrier_transition_ref": "transition:1",
                                "status": "exact",
                                "reason": "The fixture supplies exact refs.",
                                "basis": "provider-free stage-loss fixture",
                            }
                        ]
                    }
                }
            },
            "execute_batch": {
                "candidates": [{"candidate": candidate}],
                "predicate_execution_receipts": [receipt],
                "publish": {"report_issue_ids": [issue_id]},
            },
        },
        "evidence_records": [evidence],
    }
    (method_root / "method" / pair_id / "round-1.json").write_text(
        json.dumps(method_payload), encoding="utf-8"
    )
    judge_payload = {
        "expected_outcomes": [
            {
                "ledger_id": "fixture-expected",
                "reason": "The fixture supplies one expected row.",
                "basis": "provider-free stage-loss fixture",
                "source_refs": ["NL1"],
                "full_report_ids": [issue_id],
                "partial_report_ids": [],
            }
        ],
        "report_outcomes": [
            {
                "original_report_id": issue_id,
                "validity": "VALID",
                "full_ledger_ids": ["fixture-expected"],
                "partial_ledger_ids": [],
            }
        ],
    }
    (judge_root / "pairs" / f"{pair_id}.json").write_text(
        json.dumps(judge_payload), encoding="utf-8"
    )
    (judge_root / "summary.json").write_text(
        json.dumps(
            {
                "overall": {"expected_count": 1, "full_hit_count": 1, "semantic_precision": 1.0},
                "l2_expected_count": 0,
                "l2_full_hit_count": 0,
                "l2_hit_rate": 0.0,
                "total_judge_cost_usd": 0.1,
                "cost_eligible": True,
            }
        ),
        encoding="utf-8",
    )
    (judge_root / "run_manifest.json").write_text(
        json.dumps(
            {
                "selected_pair_ids": [pair_id],
                "judge_code_commit": "fixture-judge-commit",
                "protocol_sha256": "fixture-protocol",
                "model_profile": "fixture-profile",
                "workers": 1,
            }
        ),
        encoding="utf-8",
    )
    return method_root, judge_root


def _promote_to_two_round_composite(method_root: Path, judge_root: Path) -> None:
    manifest_path = method_root / "run_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["rounds"] = 2
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    round_one_method = method_root / "method/0004/round-1.json"
    round_two_method = method_root / "method/0004/round-2.json"
    round_two_method.write_bytes(round_one_method.read_bytes())

    round_one_result = judge_root / "pairs/0004.json"
    round_two_result = judge_root / "pairs/0004-round-2.json"
    round_two_result.write_bytes(round_one_result.read_bytes())

    def receipt(path: Path, round_no: int) -> dict[str, object]:
        return {
            "pair_id": "0004",
            "round": round_no,
            "result_path": str(path.resolve()),
            "result_hash": "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    (judge_root / "summary.json").write_text(
        json.dumps(
            {
                "schema_version": "paper1.semantic-judge.composite-summary.v1",
                "pair_ids": ["0004"],
                "selected_rounds": [1, 2],
                "pair_receipts": [
                    receipt(round_one_result, 1),
                    receipt(round_two_result, 2),
                ],
            }
        ),
        encoding="utf-8",
    )


def test_stage_loss_audit_keeps_every_external_expected_row(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    payload = build_stage_loss_audit(method_root=method_root, judge_root=judge_root)

    assert payload["row_count"] == 1
    assert payload["receipt_closure"]["receipt_count"] == 1
    assert payload["receipt_closure"]["terminal_receipt_count"] == 1
    assert payload["receipt_closure"]["missing_obligation_ids"] == []
    assert len(payload["w2_receipt_closure"]) == 1
    assert payload["rows"][0]["judge_disposition"] == "FULL"
    assert payload["rows"][0]["last_method_stage"] == "publish"
    assert payload["planned_predicate_scope"] == "diagnostic-12"
    assert payload["planned_predicate_count"] == 12


def test_stage_loss_audit_reports_zero_use_without_counting_plans(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    payload = build_stage_loss_audit(method_root=method_root, judge_root=judge_root)

    feasibility = payload["predicate_feasibility"]
    assert feasibility["S2"]["terminal_execution_count"] == 1
    assert feasibility["S2"]["executed_violation"] == 1
    assert feasibility["G2"]["terminal_execution_count"] == 0
    assert feasibility["G2"]["planned_in_selected_protocol"] is False
    assert feasibility["R3"]["planned_in_selected_protocol"] is False


def test_invalid_v1_input_is_not_reported_as_a_missing_backend() -> None:
    feasibility = _predicate_feasibility(
        method_indexes={
            (1, "0029"): {
                "receipts": [
                    {
                        "predicate_id": "V1",
                        "execution_status": "unsupported",
                        "terminal_state": "unsupported",
                        "verdict": "unsupported",
                        "failure_kind": "invalid_input",
                        "backend": "none",
                    }
                ],
                "evidence": [],
            }
        },
        applicability=None,
        planned_predicates=FULL_SCALE_PLANNED_PREDICATES,
    )

    row = feasibility["V1"]
    assert row["backend_implemented"] is True
    assert row["backend_missing"] == 0
    assert row["input_contract_missing"] == 1
    assert row["failure_kinds"] == {"invalid_input": 1}
    assert row["zero_use_reason"] == "input_contract_missing"


def test_full_pair_universe_uses_the_fixed_fifteen_predicate_denominator() -> None:
    scope, predicates = _resolve_planned_predicate_scope(
        pair_ids=FROZEN_PAIR_IDS,
        requested_scope=None,
        applicability=None,
    )

    assert scope == "full-scale-15"
    assert predicates == FULL_SCALE_PLANNED_PREDICATES
    assert {"G2", "G3", "R2"}.issubset(predicates)


def test_representative_subset_requires_an_explicit_predicate_denominator() -> None:
    with pytest.raises(ValueError, match="denominator is ambiguous"):
        _resolve_planned_predicate_scope(
            pair_ids=("0000", "0004"),
            requested_scope=None,
            applicability=None,
        )

    scope, predicates = _resolve_planned_predicate_scope(
        pair_ids=("0000", "0004"),
        requested_scope="full-scale-15",
        applicability=None,
    )
    assert scope == "full-scale-15"
    assert predicates == FULL_SCALE_PLANNED_PREDICATES


def test_stage_loss_audit_does_not_feed_judge_fields_into_method_rows(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    payload = build_stage_loss_audit(method_root=method_root, judge_root=judge_root)

    method_only = {
        key for row in payload["rows"] for key in row["contract_extraction"]
    }
    assert "expected_id" not in method_only
    assert all(
        row["method_artifact"].endswith("round-1.json") for row in payload["rows"]
    )


def test_stage_loss_audit_closes_composite_pair_round_receipts(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    _promote_to_two_round_composite(method_root, judge_root)

    payload = build_stage_loss_audit(method_root=method_root, judge_root=judge_root)

    assert payload["selected_rounds"] == [1, 2]
    assert payload["cell_count"] == 2
    assert payload["row_count"] == 2
    assert {(row["round"], row["pair_id"]) for row in payload["rows"]} == {
        (1, "0004"),
        (2, "0004"),
    }
    assert set(payload["method_pair_artifacts"]) == {"r1:0004", "r2:0004"}
    assert set(payload["judge_pair_paths"]) == {"r1:0004", "r2:0004"}
    assert payload["predicate_feasibility"]["S2"]["terminal_execution_count"] == 2
    assert {row["round"] for row in payload["w2_receipt_closure"]} == {1, 2}

    witness = build_expected_issue_witness_audit(
        method_root=method_root, judge_root=judge_root
    )
    assert witness["summary"]["expected_count"] == 2
    assert {row["round"] for row in witness["rows"]} == {1, 2}

    evaluation = build_evaluation_summary(
        method_root=method_root, judge_root=judge_root
    )
    assert set(evaluation["per_cell"]) == {"r1:0004", "r2:0004"}
    assert evaluation["per_pair"]["0004"]["expected_position_count"] == 2
    assert evaluation["per_pair"]["0004"]["full_hit_at_least_once_count"] == 1
    assert evaluation["per_pair"]["0004"]["full_hit_all_rounds_count"] == 1


def test_expected_issue_witness_audit_keeps_full_witness_and_receipt_chain(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    payload = build_expected_issue_witness_audit(method_root=method_root, judge_root=judge_root)

    assert payload["summary"]["expected_count"] == 1
    assert payload["summary"]["full_expected_count"] == 1
    assert payload["summary"]["full_max_w2_count"] == 1
    row = payload["rows"][0]
    assert row["match_status"] == "FULL"
    assert row["max_witness_level"] == "W2"
    assert row["matching_report_ids"] == ["0004:r1:issue:0"]
    report = row["matching_reports"][0]
    assert report["predicate_id"] == "S2"
    assert report["witness_level"] == "W2"
    assert report["d_level"] == "D2"
    assert report["receipt_chain"]["receipt_hash"] == "sha256:receipt"
    assert "method prompts" in payload["evaluation_boundary"]
    assert payload["planned_predicate_scope"] == "diagnostic-12"
    assert payload["planned_predicate_count"] == 12


def test_evaluation_summary_keeps_hit_witness_precision_and_stage_loss_separate(tmp_path: Path) -> None:
    method_root, judge_root = _write_fixture(tmp_path)
    payload = build_evaluation_summary(method_root=method_root, judge_root=judge_root)

    assert payload["judge"]["overall"]["full_hit_count"] == 1
    assert payload["witness_ledger"]["w2_all_expected_denominator"] == 1
    pair = payload["per_pair"]["0004"]
    assert pair["full_hit_count"] == 1
    assert pair["full_max_w2_count"] == 1
    assert pair["method_d_levels"] == {"D2": 1}
    assert pair["route_stage_loss"]["non_full_last_method_stage"] == {}
    assert payload["planned_predicate_scope"] == "diagnostic-12"
    assert payload["planned_predicate_count"] == 12


def test_judge_cost_audit_keeps_unpriced_billable_call_visible(tmp_path: Path) -> None:
    _, judge_root = _write_fixture(tmp_path)
    pair_path = judge_root / "pairs" / "0004.json"
    pair = json.loads(pair_path.read_text(encoding="utf-8"))
    pair["call_receipts"] = [
        {
            "call_id": "0004:r1:validity_arbitration:fixture",
            "pair_id": "0004",
            "phase": "validity_arbitration",
            "status": "success",
            "cost_usd": 0.0,
            "cost_eligible": False,
            "usage": [
                {
                    "model_call_id": "fixture-call",
                    "status": "completed",
                    "input_tokens": None,
                    "output_tokens": None,
                    "cache_read_input_tokens": None,
                    "cost_counted": True,
                    "billing_disposition": "billable",
                }
            ],
            "retries": [],
            "artifact_paths": ["fixture/result.json"],
        }
    ]
    pair_path.write_text(json.dumps(pair), encoding="utf-8")
    summary_path = judge_root / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    summary["cost_eligible"] = False
    summary_path.write_text(json.dumps(summary), encoding="utf-8")

    payload = build_judge_cost_audit(judge_root=judge_root)

    assert payload["billing"]["logical_call_count"] == 1
    assert payload["billing"]["unpriced_billable_call_count"] == 1
    assert payload["billing"]["cost_eligible"] is False
    assert payload["unpriced_billable_calls"][0]["pair_id"] == "0004"


def test_composite_judge_cost_audit_keeps_source_failures_and_all_cost(
    tmp_path: Path,
) -> None:
    judge_root = tmp_path / "composite"
    source_root = tmp_path / "source-run"
    (source_root / "pairs").mkdir(parents=True)
    judge_root.mkdir()
    manifest_path = source_root / "run_manifest.json"
    manifest_path.write_text(json.dumps({"workers": 16}), encoding="utf-8")
    result_path = source_root / "pairs/0004.json"
    result_path.write_text(
        json.dumps(
            {
                "pair_id": "0004",
                "round": 1,
                "call_receipts": [
                    {
                        "call_id": "0004:r1:fixture",
                        "pair_id": "0004",
                        "phase": "validity_primary_1",
                        "status": "success",
                        "cost_usd": 0.1,
                        "cost_eligible": True,
                        "usage": [],
                        "retries": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    terminal_path = source_root / "failure_summary.json"
    terminal_path.write_text(
        json.dumps(
            {
                "completed_pair_receipts": [
                    {
                        "pair_id": "0004",
                        "round": 1,
                        "result_path": str(result_path.resolve()),
                    }
                ],
                "failures": [
                    {
                        "pair_id": "0009",
                        "round": 1,
                        "error_type": "ValueError",
                        "error_message": "adapter rejected source status",
                        "call_receipts": [],
                        "total_judge_cost_usd": 0.0,
                        "cost_eligible": True,
                        "reason": "No Judge call was made.",
                        "basis": "Frozen adapter preflight.",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    (judge_root / "summary.json").write_text(
        json.dumps(
            {
                "schema_version": "paper1.semantic-judge.composite-summary.v1",
                "composite_id": "fixture-composite",
                "pair_ids": ["0004"],
                "semantic_judge_commit": "a" * 40,
                "protocol_sha256": "b" * 64,
                "model_profile": "fixture-profile",
                "source_runs": [
                    {
                        "run_id": "source-run",
                        "manifest_path": str(manifest_path.resolve()),
                        "terminal_path": str(terminal_path.resolve()),
                    }
                ],
                "call_audit": {"cost_eligible": True},
                "total_incurred_cost_usd": 0.1,
            }
        ),
        encoding="utf-8",
    )

    payload = build_judge_cost_audit(judge_root=judge_root)

    assert payload["workers"] == [16]
    assert payload["billing"]["logical_call_count"] == 1
    assert payload["billing"]["source_failure_count"] == 1
    assert payload["billing"]["recorded_cost_usd"] == 0.1
    assert payload["billing"]["recorded_cost_matches_summary"] is True
    assert payload["source_failures"][0]["pair_id"] == "0009"
