"""Evaluator-only expected-issue witness audit derived from immutable run artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .export import write_json
from .stage_loss import build_stage_loss_audit


def _artifact_hash(payload: dict[str, Any]) -> str:
    """Return a stable integrity hash for a JSON-compatible audit payload."""

    return "sha256:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def build_expected_issue_witness_audit(
    *,
    method_root: str | Path,
    judge_root: str | Path,
    applicability_path: str | Path | None = None,
) -> dict[str, Any]:
    """Join external expected rows to method witness chains without feeding them back."""

    stage_loss = build_stage_loss_audit(
        method_root=method_root,
        judge_root=judge_root,
        applicability_path=applicability_path,
    )
    rows = [
        {
            "pair_id": row["pair_id"],
            "round": row["round"],
            "expected_id": row["expected_id"],
            "summary": row["summary"],
            "match_status": row["match_status"],
            "matching_report_ids": row["matching_report_ids"],
            "matching_reports": row["matching_reports"],
            "max_witness_level": row["max_witness_level"],
            "max_witness_basis": row["max_witness_basis"],
            "stage_loss": {
                "contract_extraction": row["contract_extraction"],
                "grounding": row["grounding"],
                "frontier": row["frontier"],
                "candidate": row["candidate"],
                "execute_batch": row["execute_batch"],
                "evidence_record": row["evidence_record"],
                "publish": row["publish"],
                "last_method_stage": row["last_method_stage"],
                "method_disposition": row["method_disposition"],
                "root_cause_owner": row["root_cause_owner"],
            },
            "reason": row["reason"],
            "basis": row["basis"],
        }
        for row in stage_loss["rows"]
    ]
    match_counts = Counter(row["match_status"] for row in rows)
    max_witness_counts = Counter(
        row["max_witness_level"] or "NO_MATCHING_WITNESS" for row in rows
    )
    full_rows = [row for row in rows if row["match_status"] == "FULL"]
    full_max_w2 = sum(row["max_witness_level"] == "W2" for row in full_rows)
    payload: dict[str, Any] = {
        "schema": "evidence-discovery.expected-issue-witness-audit.v1",
        "run_id": stage_loss["run_id"],
        "source_commit": stage_loss["source_commit"],
        "registry_hash": stage_loss["registry_hash"],
        "method_root": stage_loss["method_root"],
        "judge_root": stage_loss["judge_root"],
        "stage_loss_artifact_hash": stage_loss["artifact_hash"],
        "evaluation_boundary": (
            "This evaluator-only artifact is created after method artifacts are immutable. "
            "It must never be imported by method prompts, binding, routing, execution, W, D, or publication."
        ),
        "rows": rows,
        "summary": {
            "expected_count": len(rows),
            "match_counts": dict(sorted(match_counts.items())),
            "max_witness_counts": dict(sorted(max_witness_counts.items())),
            "full_expected_count": len(full_rows),
            "full_max_w2_count": full_max_w2,
            "full_max_w2_share": full_max_w2 / len(full_rows) if full_rows else None,
            "w2_all_expected_count": sum(row["max_witness_level"] == "W2" for row in rows),
            "w2_all_expected_denominator": len(rows),
        },
        "reason": (
            "Every external expected issue is retained with its FINAL Judge relation, matching method reports, "
            "maximum witness level, receipt chain, and the last observed method loss stage."
        ),
        "basis": "immutable method artifacts joined to frozen external Judge pair results via report IDs",
    }
    unsigned = dict(payload)
    payload["artifact_hash"] = _artifact_hash(unsigned)
    return payload


def main(argv: list[str] | None = None) -> int:
    """Write the evaluator-only expected-issue witness audit."""

    parser = argparse.ArgumentParser(description="Build an evaluator-side expected-issue witness audit.")
    parser.add_argument("--method-root", required=True)
    parser.add_argument("--judge-root", required=True)
    parser.add_argument("--applicability", default=None)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_expected_issue_witness_audit(
        method_root=args.method_root,
        judge_root=args.judge_root,
        applicability_path=args.applicability,
    )
    write_json(Path(args.output), payload)
    print(json.dumps({"output": str(Path(args.output).resolve()), "artifact_hash": payload["artifact_hash"], "rows": len(payload["rows"])}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
