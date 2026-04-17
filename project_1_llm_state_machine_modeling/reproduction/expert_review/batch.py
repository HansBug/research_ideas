from __future__ import annotations

import argparse
import csv
import json
import statistics
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .agent import ExpertReviewAgent
from .compatibility import heuristic_expert_review
from .schema import ExpertReviewRequest, result_to_flat_row, to_dict


BATCH_SCHEMA_VERSION = "v1"


@dataclass(slots=True)
class BatchReviewItem:
    item_id: str
    prompt: str
    input_text: str
    pred_output: str
    ref_output: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchTriagePolicy:
    direct_pass_score_min: float = 0.84
    direct_pass_confidence_min: float = 0.16
    direct_pass_evidence_min: float = 0.78
    direct_pass_max_unsupported: int = 0
    high_risk_score_max: float = 0.50
    high_risk_evidence_max: float = 0.60
    high_risk_unsupported_min: int = 3


@dataclass(slots=True)
class BatchReviewRow:
    item_id: str
    overall_score: float
    overall_judgement: str
    confidence: float
    evidence_discipline_score: float
    unsupported_issue_count: int
    triage_label: str
    triage_action: str
    triage_reason: str
    latency_s: float
    attempt_count: int
    retry_count: int
    success: bool
    used_review_backend: str | None
    llm_model_name: str | None
    llm_provider: str | None
    metadata: dict[str, Any] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    review_result: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class BatchReviewRun:
    schema_version: str
    llm_mode: str
    triage_policy: BatchTriagePolicy
    max_retries: int
    rerun_count: int
    summary: dict[str, Any]
    rows: list[BatchReviewRow]


def batch_item_from_dict(payload: dict[str, Any]) -> BatchReviewItem:
    item_id = str(payload.get("item_id") or payload.get("id") or payload.get("task_id") or "").strip()
    if not item_id:
        raise ValueError("Batch review item requires `item_id`/`id`/`task_id`.")
    return BatchReviewItem(
        item_id=item_id,
        prompt=str(payload.get("prompt") or ""),
        input_text=str(payload.get("input_text") or payload.get("input") or ""),
        pred_output=str(payload.get("pred_output") or payload.get("prediction") or ""),
        ref_output=payload.get("ref_output"),
        metadata=dict(payload.get("metadata") or {}),
    )


def load_batch_items(path: Path) -> list[BatchReviewItem]:
    if path.suffix.lower() == ".jsonl":
        items = [
            batch_item_from_dict(json.loads(line))
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        return items

    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict):
        raw_items = payload.get("items")
        if not isinstance(raw_items, list):
            raise ValueError("JSON batch input must be a list or an object with key `items`.")
    elif isinstance(payload, list):
        raw_items = payload
    else:
        raise ValueError("Unsupported batch input payload.")
    return [batch_item_from_dict(dict(item)) for item in raw_items]


def _build_request(item: BatchReviewItem) -> ExpertReviewRequest:
    return ExpertReviewRequest(
        prompt=item.prompt,
        input_text=item.input_text,
        pred_output=item.pred_output,
        ref_output=item.ref_output,
        metadata=dict(item.metadata),
    )


def _dimension_score(result: Any, name: str) -> float:
    for item in getattr(result, "dimension_results", []):
        if getattr(item, "dimension_name", "") == name:
            return float(getattr(item, "score", 0.0))
    return 0.0


def _unsupported_issue_count(result: Any) -> int:
    return len(list(getattr(result, "unsupported_model_elements", [])))


def triage_review_result(result: Any, policy: BatchTriagePolicy | None = None) -> tuple[str, str, str]:
    active_policy = BatchTriagePolicy() if policy is None else policy
    evidence_score = _dimension_score(result, "evidence_discipline")
    unsupported_count = _unsupported_issue_count(result)
    score = float(getattr(result, "overall_score", 0.0))
    confidence = float(getattr(result, "confidence", 0.0))

    if (
        score < active_policy.high_risk_score_max
        or unsupported_count >= active_policy.high_risk_unsupported_min
        or evidence_score < active_policy.high_risk_evidence_max
    ):
        return (
            "high_risk_reject",
            "escalate_or_reject",
            "Low score / weak evidence discipline / too many unsupported issues make this item unsuitable for direct pass.",
        )

    if (
        score >= active_policy.direct_pass_score_min
        and confidence >= active_policy.direct_pass_confidence_min
        and evidence_score >= active_policy.direct_pass_evidence_min
        and unsupported_count <= active_policy.direct_pass_max_unsupported
    ):
        return (
            "direct_pass",
            "accept_without_manual_review",
            "High score, controlled unsupported issues, and adequate evidence discipline make this item suitable for direct pass.",
        )

    return (
        "manual_review",
        "queue_for_human_review",
        "This item is neither safely passable nor clearly rejectable, so it should enter the manual-review bucket.",
    )


def _review_once(
    item: BatchReviewItem,
    *,
    llm_mode: str,
    agent: ExpertReviewAgent | None,
) -> Any:
    request = _build_request(item)
    if llm_mode == "off":
        return heuristic_expert_review(request)
    if agent is None:
        raise ValueError("`agent` is required when llm_mode='auto'.")
    return agent.review(request)


def _p95(values: list[float]) -> float:
    if not values:
        return 0.0
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round(0.95 * (len(ordered) - 1))))
    return ordered[index]


def _row_to_export_dict(row: BatchReviewRow) -> dict[str, Any]:
    flat_result = dict(row.review_result.get("flat_result") or {})
    return {
        "item_id": row.item_id,
        "triage_label": row.triage_label,
        "triage_action": row.triage_action,
        "triage_reason": row.triage_reason,
        "overall_score": row.overall_score,
        "overall_judgement": row.overall_judgement,
        "confidence": row.confidence,
        "evidence_discipline_score": row.evidence_discipline_score,
        "unsupported_issue_count": row.unsupported_issue_count,
        "latency_s": row.latency_s,
        "attempt_count": row.attempt_count,
        "retry_count": row.retry_count,
        "success": row.success,
        "used_review_backend": row.used_review_backend,
        "llm_model_name": row.llm_model_name,
        "llm_provider": row.llm_provider,
        "metadata_json": json.dumps(row.metadata, ensure_ascii=False, sort_keys=True),
        "notes_json": json.dumps(row.notes, ensure_ascii=False, sort_keys=True),
        **flat_result,
    }


def export_batch_run(
    run: BatchReviewRun,
    *,
    output_json: Path | None = None,
    output_jsonl: Path | None = None,
    output_csv: Path | None = None,
) -> None:
    payload = {
        "schema_version": run.schema_version,
        "llm_mode": run.llm_mode,
        "max_retries": run.max_retries,
        "rerun_count": run.rerun_count,
        "triage_policy": asdict(run.triage_policy),
        "summary": run.summary,
        "rows": [asdict(row) for row in run.rows],
    }
    if output_json is not None:
        output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if output_jsonl is not None:
        lines = [json.dumps(_row_to_export_dict(row), ensure_ascii=False, sort_keys=True) for row in run.rows]
        output_jsonl.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
    if output_csv is not None:
        rows = [_row_to_export_dict(row) for row in run.rows]
        fieldnames: list[str] = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
        with output_csv.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)


def run_batch_review(
    items: list[BatchReviewItem],
    *,
    llm_mode: str = "off",
    max_retries: int = 0,
    rerun_count: int = 0,
    triage_policy: BatchTriagePolicy | None = None,
    model: str | None = None,
    provider_order: list[str] | None = None,
    temperature: float = 0.0,
    timeout: int = 180,
) -> BatchReviewRun:
    if llm_mode not in {"off", "auto"}:
        raise ValueError(f"Unsupported llm_mode: {llm_mode!r}")

    active_policy = BatchTriagePolicy() if triage_policy is None else triage_policy
    agent: ExpertReviewAgent | None = None
    if llm_mode == "auto":
        agent = ExpertReviewAgent(
            model=model or "gpt-4.1-mini",
            provider_order=provider_order,
            temperature=temperature,
            timeout=timeout,
        )

    rows: list[BatchReviewRow] = []
    retry_total = 0
    failure_count = 0
    total_start = time.perf_counter()

    for item in items:
        attempt_count = 0
        result = None
        failure_reason = ""
        item_start = time.perf_counter()
        while attempt_count <= max_retries:
            attempt_count += 1
            try:
                result = _review_once(item, llm_mode=llm_mode, agent=agent)
                break
            except Exception as exc:  # pragma: no cover - exercised through retry flow in runtime use
                failure_reason = f"{type(exc).__name__}: {exc}"
                if attempt_count > max_retries:
                    break
        latency_s = time.perf_counter() - item_start
        retry_count = max(0, attempt_count - 1)
        retry_total += retry_count

        if result is None:
            failure_count += 1
            rows.append(
                BatchReviewRow(
                    item_id=item.item_id,
                    overall_score=0.0,
                    overall_judgement="failed",
                    confidence=0.0,
                    evidence_discipline_score=0.0,
                    unsupported_issue_count=0,
                    triage_label="high_risk_reject",
                    triage_action="retry_or_manual_inspection",
                    triage_reason=f"Batch review failed after retries: {failure_reason}",
                    latency_s=round(latency_s, 6),
                    attempt_count=attempt_count,
                    retry_count=retry_count,
                    success=False,
                    used_review_backend=None,
                    llm_model_name=None,
                    llm_provider=None,
                    metadata=dict(item.metadata),
                    notes=[failure_reason] if failure_reason else [],
                    review_result={},
                )
            )
            continue

        triage_label, triage_action, triage_reason = triage_review_result(result, active_policy)
        flat_result = result_to_flat_row(result)
        rows.append(
            BatchReviewRow(
                item_id=item.item_id,
                overall_score=float(result.overall_score),
                overall_judgement=str(result.overall_judgement),
                confidence=float(result.confidence),
                evidence_discipline_score=_dimension_score(result, "evidence_discipline"),
                unsupported_issue_count=_unsupported_issue_count(result),
                triage_label=triage_label,
                triage_action=triage_action,
                triage_reason=triage_reason,
                latency_s=round(latency_s, 6),
                attempt_count=attempt_count,
                retry_count=retry_count,
                success=True,
                used_review_backend=result.used_review_backend,
                llm_model_name=result.llm_model_name,
                llm_provider=result.llm_provider,
                metadata=dict(item.metadata),
                notes=list(result.notes),
                review_result={
                    "result": to_dict(result),
                    "flat_result": flat_result,
                },
            )
        )

    rerun_rows = [row for row in rows if row.success][: min(rerun_count, len([row for row in rows if row.success]))]
    rerun_deltas: list[float] = []
    rerun_triage_flips = 0
    for row in rerun_rows:
        item = next(item for item in items if item.item_id == row.item_id)
        rerun_result = _review_once(item, llm_mode=llm_mode, agent=agent)
        rerun_deltas.append(abs(float(rerun_result.overall_score) - row.overall_score))
        rerun_label, _, _ = triage_review_result(rerun_result, active_policy)
        if rerun_label != row.triage_label:
            rerun_triage_flips += 1

    latencies = [row.latency_s for row in rows]
    scores = [row.overall_score for row in rows if row.success]
    confidences = [row.confidence for row in rows if row.success]
    triage_counts: dict[str, int] = {}
    for row in rows:
        triage_counts[row.triage_label] = triage_counts.get(row.triage_label, 0) + 1

    summary = {
        "total_items": len(items),
        "success_count": len([row for row in rows if row.success]),
        "failure_count": failure_count,
        "retry_total": retry_total,
        "retry_rate": round(retry_total / max(1, len(items)), 6),
        "latency_p50": round(statistics.median(latencies), 6) if latencies else 0.0,
        "latency_p95": round(_p95(latencies), 6),
        "latency_max": round(max(latencies), 6) if latencies else 0.0,
        "elapsed_total_s": round(time.perf_counter() - total_start, 6),
        "overall_score_mean": round(statistics.mean(scores), 6) if scores else 0.0,
        "overall_score_std": round(statistics.pstdev(scores), 6) if len(scores) > 1 else 0.0,
        "confidence_mean": round(statistics.mean(confidences), 6) if confidences else 0.0,
        "triage_counts": triage_counts,
        "rerun_score_std": round(statistics.mean(rerun_deltas), 6) if rerun_deltas else 0.0,
        "rerun_score_delta_max": round(max(rerun_deltas), 6) if rerun_deltas else 0.0,
        "triage_flip_rate": round(rerun_triage_flips / len(rerun_rows), 6) if rerun_rows else 0.0,
        "estimated_cost_usd_total": 0.0 if llm_mode == "off" else None,
        "cost_tracking_status": "deterministic_zero_cost" if llm_mode == "off" else "not_instrumented",
    }
    return BatchReviewRun(
        schema_version=BATCH_SCHEMA_VERSION,
        llm_mode=llm_mode,
        triage_policy=active_policy,
        max_retries=max_retries,
        rerun_count=rerun_count,
        summary=summary,
        rows=rows,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--llm-mode", choices=["off", "auto"], default="off")
    parser.add_argument("--max-retries", type=int, default=0)
    parser.add_argument("--rerun-count", type=int, default=4)
    parser.add_argument("--output-json", type=Path, default=None)
    parser.add_argument("--output-jsonl", type=Path, default=None)
    parser.add_argument("--output-csv", type=Path, default=None)
    args = parser.parse_args()

    items = load_batch_items(args.input)
    run = run_batch_review(
        items,
        llm_mode=args.llm_mode,
        max_retries=args.max_retries,
        rerun_count=args.rerun_count,
    )
    export_batch_run(
        run,
        output_json=args.output_json,
        output_jsonl=args.output_jsonl,
        output_csv=args.output_csv,
    )
    print(json.dumps(asdict(run), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
