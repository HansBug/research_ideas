"""Evaluator-only aggregate metrics for completed evidence-discovery runs."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .expected_issue_witness import build_expected_issue_witness_audit
from .export import write_json
from .judge_cost_audit import build_judge_cost_audit
from .stage_loss import build_stage_loss_audit


def _load(path: Path) -> dict[str, Any]:
    """Load one JSON-object artifact and reject non-object content."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _items(value: Any) -> list[dict[str, Any]]:
    """Normalize a JSON list or object mapping into object rows."""

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, dict)]
    return []


def _artifact_hash(payload: dict[str, Any]) -> str:
    """Return a stable integrity hash for a JSON-compatible audit payload."""

    return "sha256:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _counts(rows: list[dict[str, Any]], field: str, allowed: set[str] | None = None) -> dict[str, int]:
    """Count nonempty values, optionally restricting the reported vocabulary."""

    values = (
        str(row.get(field))
        for row in rows
        if row.get(field) is not None and (allowed is None or row.get(field) in allowed)
    )
    return dict(sorted(Counter(values).items()))


def build_evaluation_summary(
    *,
    method_root: str | Path,
    judge_root: str | Path,
    applicability_path: str | Path | None = None,
) -> dict[str, Any]:
    """Aggregate immutable method and complete frozen-Judge artifacts by pair."""

    method_root_path = Path(method_root).expanduser().resolve()
    judge_root_path = Path(judge_root).expanduser().resolve()
    judge_summary_path = judge_root_path / "summary.json"
    if not judge_summary_path.is_file():
        raise ValueError("evaluation summary requires a completed frozen Judge summary.json")
    stage_loss = build_stage_loss_audit(
        method_root=method_root_path,
        judge_root=judge_root_path,
        applicability_path=applicability_path,
    )
    expected_audit = build_expected_issue_witness_audit(
        method_root=method_root_path,
        judge_root=judge_root_path,
        applicability_path=applicability_path,
    )
    judge_cost_audit = build_judge_cost_audit(judge_root=judge_root_path)
    judge_summary = _load(judge_summary_path)
    expected_by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in expected_audit["rows"]:
        expected_by_pair[str(row["pair_id"])].append(row)
    stage_rows_by_pair: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in stage_loss["rows"]:
        stage_rows_by_pair[str(row["pair_id"])].append(row)

    per_pair: dict[str, dict[str, Any]] = {}
    all_receipts: list[dict[str, Any]] = []
    all_evidence: list[dict[str, Any]] = []
    for pair_id in stage_loss["selected_pair_ids"]:
        method_payload = _load(method_root_path / "method" / pair_id / "round-1.json")
        judge_payload = _load(judge_root_path / "pairs" / f"{pair_id}.json")
        evidence = _items(method_payload.get("evidence_records"))
        receipts = _items(method_payload.get("predicate_execution_receipts"))
        if not receipts:
            receipts = _items(
                method_payload.get("stage_outputs", {})
                .get("execute_batch", {})
                .get("predicate_execution_receipts")
            )
        all_evidence.extend(evidence)
        all_receipts.extend(receipts)
        expected_rows = expected_by_pair[pair_id]
        full_rows = [row for row in expected_rows if row["match_status"] == "FULL"]
        terminal_predicates = sorted({
            str(receipt.get("predicate_id"))
            for receipt in receipts
            if receipt.get("execution_state") == "completed"
            and receipt.get("terminal_state") == "completed"
            and receipt.get("predicate_verdict") in {"true", "false"}
        })
        report_outcomes = _items(judge_payload.get("report_outcomes"))
        per_pair[pair_id] = {
            "expected_count": len(expected_rows),
            "full_hit_count": len(full_rows),
            "partial_match_count": sum(row["match_status"] == "PARTIAL" for row in expected_rows),
            "full_max_w2_count": sum(row["max_witness_level"] == "W2" for row in full_rows),
            "full_max_w2_share": (
                sum(row["max_witness_level"] == "W2" for row in full_rows) / len(full_rows)
                if full_rows else None
            ),
            "w2_all_expected_count": sum(row["max_witness_level"] == "W2" for row in expected_rows),
            "method_witness_levels": _counts(evidence, "witness_level", {"W0", "W1", "W2"}),
            "method_d_levels": _counts(evidence, "d_level", {"D0", "D1", "D2", "D_UNRESOLVED"}),
            "terminal_predicates": terminal_predicates,
            "judge_metrics": judge_payload.get("metrics", {}),
            "judge_report_validity": _counts(report_outcomes, "validity"),
            "route_stage_loss": {
                "all_expected_root_cause_owner": _counts(stage_rows_by_pair[pair_id], "root_cause_owner"),
                "non_full_root_cause_owner": _counts(
                    [row for row in stage_rows_by_pair[pair_id] if row["match_status"] != "FULL"],
                    "root_cause_owner",
                ),
                "non_full_last_method_stage": _counts(
                    [row for row in stage_rows_by_pair[pair_id] if row["match_status"] != "FULL"],
                    "last_method_stage",
                ),
            },
            "reason": "Pair metrics join immutable method evidence/receipts with one complete frozen Judge pair result.",
            "basis": "frozen witness/determinacy fields, frozen semantic Judge rows, and evaluator-only expected/report joins",
        }

    payload: dict[str, Any] = {
        "schema": "evidence-discovery.evaluation-summary.v1",
        "run_id": stage_loss["run_id"],
        "source_commit": stage_loss["source_commit"],
        "registry_hash": stage_loss["registry_hash"],
        "method_root": str(method_root_path),
        "judge_root": str(judge_root_path),
        "judge_summary_path": str(judge_summary_path),
        "stage_loss_artifact_hash": stage_loss["artifact_hash"],
        "expected_issue_witness_artifact_hash": expected_audit["artifact_hash"],
        "judge_cost_audit_hash": judge_cost_audit["artifact_hash"],
        "evaluation_boundary": expected_audit["evaluation_boundary"],
        "judge": {
            "overall": judge_summary.get("overall", {}),
            "l2_expected_count": judge_summary.get("l2_expected_count"),
            "l2_full_hit_count": judge_summary.get("l2_full_hit_count"),
            "l2_hit_rate": judge_summary.get("l2_hit_rate"),
            "total_judge_cost_usd": judge_summary.get("total_judge_cost_usd"),
            "cost_eligible": judge_summary.get("cost_eligible"),
            "cost_audit": judge_cost_audit["billing"],
            "unpriced_billable_calls": judge_cost_audit["unpriced_billable_calls"],
        },
        "method": {
            "metrics": _load(method_root_path / "summary.json").get("metrics", {}).get("method", {}),
            "witness_levels": _counts(all_evidence, "witness_level", {"W0", "W1", "W2"}),
            "d_levels": _counts(all_evidence, "d_level", {"D0", "D1", "D2", "D_UNRESOLVED"}),
            "failure_kinds": _counts(
                [receipt for receipt in all_receipts if receipt.get("failure_kind")],
                "failure_kind",
            ),
        },
        "witness_ledger": expected_audit["summary"],
        "predicate_feasibility": stage_loss["predicate_feasibility"],
        "w2_receipt_closure": stage_loss["w2_receipt_closure"],
        "per_pair": per_pair,
        "reason": (
            "The summary keeps hit, max-W, W2/all-expected, method W/D, Judge precision/INVALID, "
            "predicate feasibility, cost, and stage loss as separate denominators."
        ),
        "basis": "immutable method summary/round artifacts, complete frozen Judge summary/pair artifacts, and evaluator-only joins",
    }
    unsigned = dict(payload)
    payload["artifact_hash"] = _artifact_hash(unsigned)
    return payload


def main(argv: list[str] | None = None) -> int:
    """Write the evaluator-only aggregate summary for one completed run."""

    parser = argparse.ArgumentParser(description="Build an evaluator-only evidence-discovery summary.")
    parser.add_argument("--method-root", required=True)
    parser.add_argument("--judge-root", required=True)
    parser.add_argument("--applicability", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_evaluation_summary(
        method_root=args.method_root,
        judge_root=args.judge_root,
        applicability_path=args.applicability,
    )
    write_json(Path(args.output), payload)
    print(json.dumps({"output": str(Path(args.output).resolve()), "artifact_hash": payload["artifact_hash"], "pairs": len(payload["per_pair"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
