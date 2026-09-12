"""Evaluator-only cost-closure audit for a completed frozen semantic Judge run."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from utils.artifact_io import write_json
from .stage_loss import _is_composite_judge_summary


def _load(path: Path) -> dict[str, Any]:
    """Load a JSON object from a completed external Judge artifact."""

    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _items(value: Any) -> list[dict[str, Any]]:
    """Normalize a JSON list or mapping into JSON object rows."""

    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [item for item in value.values() if isinstance(item, dict)]
    return []


def _artifact_hash(payload: dict[str, Any]) -> str:
    """Return a stable integrity hash for this JSON-compatible audit payload."""

    return "sha256:" + hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _schema_failure_count(call: dict[str, Any]) -> int:
    """Count retained Pydantic failures without interpreting their text as semantics."""

    count = 0
    for retry in _items(call.get("retries")):
        raw = retry.get("raw_attempt_json")
        if not isinstance(raw, str):
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            continue
        count += len(_items(payload.get("schema_validation_failures")))
    return count


def _composite_calls(
    summary: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    calls: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []
    for source in _items(summary.get("source_runs")):
        terminal_path = Path(str(source["terminal_path"])).expanduser().resolve()
        terminal = _load(terminal_path)
        receipts = _items(terminal.get("pair_receipts"))
        if not receipts:
            receipts = _items(terminal.get("completed_pair_receipts"))
        for receipt in receipts:
            result_path = Path(str(receipt["result_path"])).expanduser().resolve()
            result = _load(result_path)
            for call in _items(result.get("call_receipts")):
                calls.append(
                    {
                        "source_run_id": source.get("run_id"),
                        "pair_id": result.get("pair_id") or receipt.get("pair_id"),
                        "round": result.get("round") or receipt.get("round"),
                        **call,
                    }
                )
        for failure in _items(terminal.get("failures")):
            failures.append(
                {
                    "source_run_id": source.get("run_id"),
                    "pair_id": failure.get("pair_id"),
                    "round": failure.get("round"),
                    "error_type": failure.get("error_type"),
                    "error_message": failure.get("error_message"),
                    "total_judge_cost_usd": failure.get("total_judge_cost_usd", 0.0),
                    "cost_eligible": failure.get("cost_eligible", False),
                    "reason": failure.get("reason"),
                    "basis": failure.get("basis"),
                }
            )
            for call in _items(failure.get("call_receipts")):
                calls.append(
                    {
                        "source_run_id": source.get("run_id"),
                        "pair_id": failure.get("pair_id"),
                        "round": failure.get("round"),
                        **call,
                    }
                )
    return calls, failures


def build_judge_cost_audit(*, judge_root: str | Path) -> dict[str, Any]:
    """Audit price completeness without changing frozen Judge results or costs."""

    root = Path(judge_root).expanduser().resolve()
    summary = _load(root / "summary.json")
    is_composite = _is_composite_judge_summary(summary)
    if is_composite:
        pair_ids = tuple(str(value) for value in summary.get("pair_ids", ()) if value)
        calls, source_failures = _composite_calls(summary)
        judge_code_commit = summary.get("semantic_judge_commit")
        protocol_sha256 = summary.get("protocol_sha256")
        model_profile = summary.get("model_profile")
        workers = [
            _load(Path(str(source["manifest_path"])).expanduser().resolve()).get("workers")
            for source in _items(summary.get("source_runs"))
        ]
        summary_cost = float(summary.get("total_incurred_cost_usd") or 0.0)
        summary_cost_eligible = bool(
            (summary.get("call_audit") or {}).get("cost_eligible")
        )
    else:
        manifest = _load(root / "run_manifest.json")
        pair_ids = tuple(str(value) for value in manifest.get("selected_pair_ids", ()) if value)
        calls = []
        source_failures = []
        for pair_id in pair_ids:
            payload = _load(root / "pairs" / f"{pair_id}.json")
            for call in _items(payload.get("call_receipts")):
                calls.append({"pair_id": pair_id, **call})
        judge_code_commit = manifest.get("judge_code_commit")
        protocol_sha256 = manifest.get("protocol_sha256")
        model_profile = manifest.get("model_profile")
        workers = manifest.get("workers")
        summary_cost = float(summary.get("total_judge_cost_usd") or 0.0)
        summary_cost_eligible = bool(summary.get("cost_eligible"))
    if not pair_ids:
        raise ValueError("Judge manifest has no selected_pair_ids")
    unpriced_calls = []
    provider_retries = 0
    non_provider_retries = 0
    schema_failure_count = 0
    for call in calls:
        retries = _items(call.get("retries"))
        provider_retries += sum(bool(retry.get("provider_error")) for retry in retries)
        non_provider_retries += sum(
            not bool(retry.get("provider_error")) and int(retry.get("attempt_no") or 1) > 1
            for retry in retries
        )
        schema_failure_count += _schema_failure_count(call)
        if not call.get("cost_eligible", False):
            unpriced_calls.append({
                "call_id": call.get("call_id"),
                "pair_id": call.get("pair_id"),
                "phase": call.get("phase"),
                "status": call.get("status"),
                "recorded_cost_usd": call.get("cost_usd"),
                "usage": [
                    {
                        "model_call_id": usage.get("model_call_id"),
                        "status": usage.get("status"),
                        "input_tokens": usage.get("input_tokens"),
                        "output_tokens": usage.get("output_tokens"),
                        "cache_read_input_tokens": usage.get("cache_read_input_tokens"),
                        "cost_counted": usage.get("cost_counted"),
                        "billing_disposition": usage.get("billing_disposition"),
                    }
                    for usage in _items(call.get("usage"))
                ],
                "artifact_paths": call.get("artifact_paths", []),
                "reason": (
                    "The successful Judge call has billable provider usage with incomplete token metadata, "
                    "so exact price reconstruction is unavailable."
                ),
                "basis": "frozen JudgeCallReceipt.cost_eligible=false and its preserved normalized usage rows",
            })
    recorded_cost = sum(float(call.get("cost_usd") or 0.0) for call in calls)
    payload: dict[str, Any] = {
        "schema": "evidence-discovery.judge-cost-audit.v1",
        "run_id": summary.get("run_id") or summary.get("composite_id"),
        "judge_root": str(root),
        "judge_code_commit": judge_code_commit,
        "protocol_sha256": protocol_sha256,
        "model_profile": model_profile,
        "workers": workers,
        "source_failures": source_failures,
        "billing": {
            "logical_call_count": len(calls),
            "priced_call_count": sum(bool(call.get("cost_eligible")) for call in calls),
            "unpriced_billable_call_count": len(unpriced_calls),
            "recorded_cost_usd": recorded_cost,
            "summary_cost_usd": summary_cost,
            "recorded_cost_matches_summary": abs(recorded_cost - summary_cost) < 1e-9,
            "cost_eligible": not unpriced_calls and summary_cost_eligible,
            "source_failure_count": len(source_failures),
            "provider_error_retry_count": provider_retries,
            "non_provider_outer_retry_count": non_provider_retries,
            "schema_validation_failure_count": schema_failure_count,
        },
        "unpriced_billable_calls": unpriced_calls,
        "phase_counts": dict(sorted(Counter(str(call.get("phase")) for call in calls).items())),
        "evaluation_boundary": (
            "This artifact only audits frozen external Judge billing receipts. It must never be imported by method "
            "prompts, binding, routing, execution, W, D, publication, or Judge semantic decisions."
        ),
        "reason": (
            "All successful, failed, retried, and unpriced Judge calls are retained. A missing provider usage record is reported "
            "as an unpriced billable call, never estimated as an exact cost and never treated as a semantic failure."
        ),
        "basis": "immutable semantic Judge run manifest, summary, pair call receipts, and normalized provider usage metadata",
    }
    unsigned = dict(payload)
    payload["artifact_hash"] = _artifact_hash(unsigned)
    return payload


def main(argv: list[str] | None = None) -> int:
    """Write an evaluator-only frozen Judge cost-closure audit."""

    parser = argparse.ArgumentParser(description="Build a frozen semantic Judge cost audit.")
    parser.add_argument("--judge-root", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    payload = build_judge_cost_audit(judge_root=args.judge_root)
    write_json(Path(args.output), payload)
    print(json.dumps({"output": str(Path(args.output).resolve()), "artifact_hash": payload["artifact_hash"], "cost_eligible": payload["billing"]["cost_eligible"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
