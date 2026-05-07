"""Q3 self-consistency wrapper: run reviewer N times per task with varied
configs (temperature / prompt paraphrase / both), then aggregate to one
result via median + confidence-from-variance + disagreement metadata.

Spec source: PR comment #4386634782 §七 (Week 2 plan); rules clarified in
Week 2 chat — score uses median, judgement is derived from median score
(not majority vote), confidence = clip(1 - α·max_dim_std, 0.10, 0.99).

Usage:
    python -m state_machine_review_corpus.etl.run_self_consistency_config \
        --base-dir <phase14_combined dir> \
        --record-limit 12 --summary-limit 12 --component-limit 12 --protocol-limit 4 \
        --rubric --iter-b \
        --variance-source both --n-reruns 3 \
        --config-label q3_both_n3 \
        --output etl/out/.../report_q3_both_n3.json
"""
from __future__ import annotations

import argparse
import copy
import json
import statistics
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any

from project_1_llm_state_machine_modeling.reproduction.expert_review.benchmark import (
    _evaluate_task_bundle,
    _load_benchmark_tables,
    build_benchmark_slices,
)
from project_1_llm_state_machine_modeling.reproduction.expert_review.schema import (
    judgement_from_score,
)


# Default rerun schedules (override via CLI if needed)
TEMP_SCHEDULE_N3 = [0.0, 0.3, 0.5]
TEMP_SCHEDULE_N5 = [0.0, 0.2, 0.4, 0.6, 0.8]
PARAPHRASE_VARIANTS = ["v1", "v2", "v3"]
PARAPHRASE_VARIANTS_N5 = ["v1", "v2", "v3", "v1", "v2"]  # cycle for N>3


def _build_rerun_overrides(
    rerun_index: int,
    variance_source: str,
    n_reruns: int,
) -> dict[str, Any]:
    """Compute the per-rerun metadata overrides given rerun index."""
    overrides: dict[str, Any] = {}
    temp_sched = TEMP_SCHEDULE_N3 if n_reruns == 3 else TEMP_SCHEDULE_N5
    para_sched = PARAPHRASE_VARIANTS if n_reruns == 3 else PARAPHRASE_VARIANTS_N5

    if variance_source in ("temp", "both"):
        overrides["rubric_temperature_override"] = temp_sched[rerun_index % len(temp_sched)]
    if variance_source in ("paraphrase", "both"):
        overrides["rubric_prompt_variant"] = para_sched[rerun_index % len(para_sched)]
    return overrides


def _aggregate_runs(
    runs: list[Any],
    *,
    confidence_alpha: float = 2.0,
) -> dict[str, Any]:
    """Aggregate N runs into a single result.

    Rules (per Week 2 design):
    - score: median across runs
    - dim_scores: median per dim
    - judgement: derived from median overall_score (not majority vote)
    - confidence: clip(1 - alpha * max_dim_std, 0.10, 0.99)
    - disagreement_flag: True if any run's judgement differs from median-derived
    - run_judgements / run_scores / dim_std: kept for analysis
    """
    if not runs:
        return {
            "overall_score": 0.0,
            "overall_judgement": "poor",
            "confidence": 0.10,
            "disagreement_flag": True,
            "n_runs": 0,
            "n_failed": 0,
            "all_failed": True,
        }

    overall_scores = [float(getattr(r, "overall_score", 0.0)) for r in runs]
    median_overall = statistics.median(overall_scores)

    # Per-dim scores
    dim_scores_per_run: dict[str, list[float]] = {}
    for r in runs:
        for d in getattr(r, "dimension_results", []) or []:
            name = getattr(d, "dimension_name", None) or (d.get("dimension_name") if isinstance(d, dict) else None)
            score = getattr(d, "score", None)
            if score is None and isinstance(d, dict):
                score = d.get("score")
            if name is not None and score is not None:
                dim_scores_per_run.setdefault(name, []).append(float(score))

    dim_medians = {dim: statistics.median(vals) for dim, vals in dim_scores_per_run.items() if vals}
    dim_stds = {
        dim: (statistics.pstdev(vals) if len(vals) > 1 else 0.0)
        for dim, vals in dim_scores_per_run.items() if vals
    }
    max_dim_std = max(dim_stds.values()) if dim_stds else 0.0
    confidence = max(0.10, min(0.99, 1.0 - confidence_alpha * max_dim_std))

    # Judgement: derive from median overall score (consistent with score)
    median_judgement = str(judgement_from_score(median_overall))

    # Disagreement flag: any individual run's judgement differs from the median's
    individual_judgements = [str(getattr(r, "overall_judgement", "?")) for r in runs]
    judgement_counter = Counter(individual_judgements)
    disagreement_flag = len(set(individual_judgements)) > 1

    # Confidence stats
    individual_confidences = [float(getattr(r, "confidence", 0.0)) for r in runs]

    return {
        "overall_score": median_overall,
        "overall_judgement": median_judgement,
        "confidence": confidence,
        "disagreement_flag": disagreement_flag,
        "n_runs": len(runs),
        "n_failed": 0,
        "all_failed": False,
        "run_overall_scores": overall_scores,
        "run_judgements": individual_judgements,
        "run_confidences": individual_confidences,
        "dim_medians": dim_medians,
        "dim_stds": dim_stds,
        "max_dim_std": max_dim_std,
        "judgement_distribution": dict(judgement_counter),
    }


def _patch_task_for_rerun(task, overrides: dict[str, Any]):
    """Return a deepcopy of the task with metadata overrides applied."""
    new_task = copy.deepcopy(task)
    if new_task.metadata is None:
        new_task.metadata = {}
    new_task.metadata.update(overrides)
    return new_task


def run_with_self_consistency(
    slice_tasks: dict[str, list],
    *,
    n_reruns: int,
    variance_source: str,
    confidence_alpha: float,
    base_metadata: dict[str, Any],
    llm_mode: str,
    model: str,
    provider_order: list[str] | None,
    temperature: float,
    timeout: int,
    report_label: str,
) -> dict[str, Any]:
    """Run N reruns of the slice, aggregate per task.

    For each rerun i: build per-task tasks with metadata overrides for that
    rerun_index (temp / paraphrase variant), then call _evaluate_task_bundle.
    Collect N reports, aggregate normalized_rows by task_id.
    """
    rerun_reports: list[dict[str, Any]] = []
    print(f"[{report_label}] starting {n_reruns} reruns, variance_source={variance_source}", flush=True)
    for i in range(n_reruns):
        overrides = _build_rerun_overrides(i, variance_source, n_reruns)
        # Apply base_metadata + overrides to all tasks in this rerun
        rerun_slice_tasks: dict[str, list] = {}
        for regime, tasks in slice_tasks.items():
            rerun_slice_tasks[regime] = [
                _patch_task_for_rerun(t, {**base_metadata, **overrides})
                for t in tasks
            ]
        t0 = time.time()
        report = _evaluate_task_bundle(
            rerun_slice_tasks,
            llm_mode=llm_mode,
            rerun_count=0,  # outer SC loop handles reruns
            report_label=f"{report_label}:rerun{i}",
            metadata={
                "scope": "self_consistency",
                "rerun_index": i,
                "variance_source": variance_source,
                "n_reruns": n_reruns,
                **base_metadata,
                **overrides,
            },
            review_cache=None,
            model=model,
            provider_order=provider_order if llm_mode == "auto" else None,
            temperature=temperature,
            timeout=timeout,
        )
        elapsed = time.time() - t0
        print(f"[{report_label}] rerun {i}/{n_reruns-1} done elapsed={elapsed/60:.1f}min overrides={overrides}", flush=True)
        rerun_reports.append(report)

    # Aggregate per task across reruns
    task_index: dict[str, list[Any]] = {}
    task_metadata: dict[str, dict[str, Any]] = {}
    for rerun_idx, report in enumerate(rerun_reports):
        for row in report.get("normalized_rows", []):
            tid = row.get("task_id", "?")
            task_index.setdefault(tid, []).append(row)
            if tid not in task_metadata:
                task_metadata[tid] = {
                    "eval_bucket": row.get("eval_bucket"),
                    "expected_regime": row.get("expected_regime"),
                    "human_score": row.get("human_score"),
                    "human_judgement": row.get("human_judgement"),
                    "human_issue_set": row.get("human_issue_set"),
                    "metadata": row.get("metadata"),
                }

    aggregated_rows = []
    for tid, rows in task_index.items():
        # Build pseudo-result objects from rows so we can reuse _aggregate_runs.
        # Each row has agent_score / agent_judgement / agent_confidence / etc.
        class _Wrapper:
            def __init__(self, row: dict):
                self.overall_score = row.get("agent_score", 0.0)
                self.overall_judgement = row.get("agent_judgement", "?")
                self.confidence = row.get("agent_confidence", 0.0)
                # No dimension_results in normalized_rows; use dim-level data if present
                self.dimension_results = []

        wrappers = [_Wrapper(r) for r in rows]
        agg = _aggregate_runs(wrappers, confidence_alpha=confidence_alpha)
        agg["task_id"] = tid
        agg["task_metadata"] = task_metadata.get(tid, {})
        agg["per_run_normalized_rows"] = rows  # keep raw for analysis
        aggregated_rows.append(agg)

    # Compute aggregate-level metrics by treating the median scores as "agent_score"
    # and re-running the metric formulas. To keep this simple, return both the raw
    # rerun reports AND the aggregated rows; downstream analyzer will recompute
    # RAS/SAS/etc. on the median scores.
    return {
        "scheme": "self_consistency",
        "n_reruns": n_reruns,
        "variance_source": variance_source,
        "confidence_alpha": confidence_alpha,
        "base_metadata": base_metadata,
        "rerun_reports": rerun_reports,
        "aggregated_rows": aggregated_rows,
    }


def _recompute_aggregated_metrics(sc_result: dict[str, Any]) -> dict[str, Any]:
    """Take the per-run reports and produce a single 'aggregated' report by
    overwriting agent_score / agent_judgement with median per task, then reusing
    the metric pipeline.

    Trick: take the FIRST rerun's report, replace its normalized_rows agent_*
    fields with the aggregated medians, then re-run the metric calculations
    """
    from project_1_llm_state_machine_modeling.reproduction.expert_review.benchmark import (
        _critical_issue_metrics,
        _component_alignment_metrics,
        _contradiction_metrics,
        _judgement_metrics,
        _protocol_metrics,
        _runtime_metrics,
        _score_align,
        _reason_alignment_metrics,
        _equivalence_metrics,
        _calibration_metrics,
        _stability_metrics,
        _summary_discipline_metrics,
        PHASE14_LOCKBOX_MAX_DEGRADE,
    )

    aggregated_rows = sc_result["aggregated_rows"]
    rerun_reports = sc_result["rerun_reports"]
    if not rerun_reports:
        return sc_result

    # Build a lookup task_id → aggregated dict
    agg_lookup = {a["task_id"]: a for a in aggregated_rows}

    # Use first rerun report as the structural template
    template = copy.deepcopy(rerun_reports[0])
    rebuilt_rows = []
    for row in template.get("normalized_rows", []):
        tid = row.get("task_id")
        agg = agg_lookup.get(tid, {})
        if agg:
            row = dict(row)
            row["agent_score"] = agg.get("overall_score", row.get("agent_score"))
            row["agent_judgement"] = agg.get("overall_judgement", row.get("agent_judgement"))
            row["agent_confidence"] = agg.get("confidence", row.get("agent_confidence"))
            row["sc_disagreement_flag"] = agg.get("disagreement_flag")
            row["sc_max_dim_std"] = agg.get("max_dim_std")
            row["sc_n_runs"] = agg.get("n_runs")
        rebuilt_rows.append(row)

    record_rows = [r for r in rebuilt_rows if r["eval_bucket"] == "record"]
    summary_rows = [r for r in rebuilt_rows if r["eval_bucket"] == "summary"]
    component_rows = [r for r in rebuilt_rows if r["eval_bucket"] == "component"]
    protocol_rows = [r for r in rebuilt_rows if r["eval_bucket"] == "protocol"]

    record_score = _score_align(record_rows)
    record_reason = _reason_alignment_metrics(record_rows)
    record_equiv = _equivalence_metrics(record_rows)
    record_calib = _calibration_metrics(record_rows)
    issue_f1 = (
        statistics.mean(row["issue_f1"] for row in record_rows) * 100.0
        if record_rows else 0.0
    )
    ras = (
        0.30 * record_score["ScoreAlign"]
        + 0.25 * issue_f1
        + 0.20 * record_reason["ReasonAlign"]
        + 0.15 * record_equiv["EquivAlign"]
        + 0.10 * record_calib["Calib"]
    )

    summary_score = _score_align(summary_rows)
    summary_discipline = _summary_discipline_metrics(summary_rows)
    stability = _stability_metrics(summary_rows + record_rows)
    rank_align = 100.0 * summary_score["pairwise_order_accuracy"]
    sas = (
        0.40 * summary_score["ScoreAlign"]
        + 0.25 * rank_align
        + 0.20 * summary_discipline["EvidenceDiscipline"]
        + 0.15 * stability["Stability"]
    )

    component_metrics = _component_alignment_metrics(component_rows)
    protocol_metrics = _protocol_metrics(protocol_rows)
    judgement_metrics = _judgement_metrics(record_rows + summary_rows + component_rows)
    contradiction_metrics = _contradiction_metrics(rebuilt_rows)
    critical_issue_metrics = _critical_issue_metrics(record_rows + summary_rows)
    runtime_metrics = _runtime_metrics(rebuilt_rows)
    hai_legacy = 0.55 * ras + 0.25 * sas + 0.20 * protocol_metrics["PDS"]
    hai = 0.40 * ras + 0.30 * sas + 0.30 * component_metrics["CRAS"]

    # Build SC-aware report
    aggregated_report = dict(template)
    aggregated_report.update({
        "report_label": template.get("report_label", "") + ":aggregated",
        "record_metrics": {
            **record_score, **record_reason, **record_equiv, **record_calib,
            "issue_f1": issue_f1 / 100.0, "RAS": ras,
        },
        "summary_metrics": {
            **summary_score, **summary_discipline, **stability,
            "RankAlign": rank_align, "SAS": sas,
        },
        "component_metrics": component_metrics,
        "protocol_metrics": protocol_metrics,
        "judgement_metrics": judgement_metrics,
        "contradiction_metrics": contradiction_metrics,
        "critical_issue_metrics": critical_issue_metrics,
        "runtime_metrics": runtime_metrics,
        "HAI": hai,
        "HAI_legacy": hai_legacy,
        "pds_gate": {"threshold": 95.0, "value": protocol_metrics["PDS"], "passed": bool(protocol_metrics["PDS"] >= 95.0)},
        "normalized_rows": rebuilt_rows,
        "self_consistency_summary": {
            "scheme": sc_result["scheme"],
            "n_reruns": sc_result["n_reruns"],
            "variance_source": sc_result["variance_source"],
            "confidence_alpha": sc_result["confidence_alpha"],
            "n_disagreement_flag_true": sum(
                1 for a in sc_result["aggregated_rows"]
                if a.get("disagreement_flag")
            ),
            "n_total_tasks": len(sc_result["aggregated_rows"]),
            "mean_max_dim_std": statistics.mean(
                a.get("max_dim_std", 0.0) for a in sc_result["aggregated_rows"]
            ) if sc_result["aggregated_rows"] else 0.0,
        },
    })
    return aggregated_report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", type=Path, required=True)
    parser.add_argument("--record-limit", type=int, default=12)
    parser.add_argument("--summary-limit", type=int, default=12)
    parser.add_argument("--component-limit", type=int, default=12)
    parser.add_argument("--protocol-limit", type=int, default=4)
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--rubric", action="store_true", default=False)
    parser.add_argument("--iter-a", action="store_true", default=False)
    parser.add_argument("--iter-b", action="store_true", default=False)
    parser.add_argument("--iter-c", nargs="*", default=None)
    # Q3 args
    parser.add_argument("--variance-source", choices=["temp", "paraphrase", "both"], default="both")
    parser.add_argument("--n-reruns", type=int, default=3)
    parser.add_argument("--confidence-alpha", type=float, default=2.0)
    # general
    parser.add_argument("--config-label", type=str, default="q3_default")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--llm-mode", type=str, default="auto", choices=["auto", "off"])
    parser.add_argument("--model", type=str, default="gpt-5.5")
    parser.add_argument("--provider-order", nargs="*", default=["airouter"])
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout", type=int, default=240)
    args = parser.parse_args()

    records, protocols, availability = _load_benchmark_tables(args.base_dir)
    slice_tasks = build_benchmark_slices(
        records, protocols,
        record_limit=args.record_limit,
        summary_limit=args.summary_limit,
        component_limit=args.component_limit,
        protocol_limit=args.protocol_limit,
        seed=args.seed,
    )

    base_metadata = {
        "rubric_llm_enabled": args.rubric,
        "rubric_iter_a_asymmetric": args.iter_a,
        "rubric_iter_b_diff_prompt": args.iter_b,
    }
    if args.iter_c is not None:
        base_metadata["rubric_iter_c_regimes"] = list(args.iter_c)

    t_total = time.time()
    sc_result = run_with_self_consistency(
        slice_tasks,
        n_reruns=args.n_reruns,
        variance_source=args.variance_source,
        confidence_alpha=args.confidence_alpha,
        base_metadata=base_metadata,
        llm_mode=args.llm_mode,
        model=args.model,
        provider_order=args.provider_order,
        temperature=args.temperature,
        timeout=args.timeout,
        report_label=f"week2_q3:{args.config_label}",
    )
    aggregated_report = _recompute_aggregated_metrics(sc_result)
    elapsed_total = time.time() - t_total

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(aggregated_report, ensure_ascii=False, indent=2, default=str)
    )
    print(f"[{args.config_label}] total elapsed_min={elapsed_total/60:.1f}", flush=True)
    print(f"[{args.config_label}] HAI={aggregated_report.get('HAI', 0):.4f} HAI_legacy={aggregated_report.get('HAI_legacy', 0):.4f}", flush=True)
    print(f"[{args.config_label}] RAS={aggregated_report['record_metrics'].get('RAS', 0):.4f} SAS={aggregated_report['summary_metrics'].get('SAS', 0):.4f}", flush=True)
    sc_summary = aggregated_report["self_consistency_summary"]
    print(f"[{args.config_label}] disagreement_flag_count={sc_summary['n_disagreement_flag_true']}/{sc_summary['n_total_tasks']} mean_max_dim_std={sc_summary['mean_max_dim_std']:.4f}", flush=True)


if __name__ == "__main__":
    main()
