"""Re-aggregate SC reports from existing per-rerun checkpoints, applying the
2026-05-07 confidence-formula fix. Avoids re-running LLM calls.

For each (slice, source) pair where checkpoints exist:
- Load the 3 rerun checkpoint reports
- Apply patched `_aggregate_runs` to compute corrected agent_confidence
- Manually overlay corrected agent_score/judgement/confidence onto template rows
- Recompute only the metrics that depend on these fields
  (_score_align, _calibration_metrics, _summary_discipline_metrics,
   _protocol_metrics, _judgement_metrics, _critical_issue_metrics,
   _component_alignment_metrics)
- Keep contradiction_metrics / runtime_metrics from template (unaffected by fix
  and need result objects we can't reconstruct from JSON checkpoints)

Slices covered:
- 40-task: q3_temp_n3, q3_para_n3, q3_both_n3
- 62-task: q3_both_n3_62task

Run: python -m project_1_llm_state_machine_modeling.state_machine_review_corpus.etl.sc_reaggregate_from_checkpoints
"""
from __future__ import annotations

import json
from pathlib import Path

from project_1_llm_state_machine_modeling.state_machine_review_corpus.etl.run_self_consistency_config import (
    _aggregate_runs,
)
from project_1_llm_state_machine_modeling.reproduction.expert_review.benchmark import (
    CRITICAL_ISSUE_TAXONOMY,
    _calibration_metrics,
    _component_alignment_metrics,
    _equivalence_metrics,
    _judgement_metrics,
    _protocol_metrics,
    _reason_alignment_metrics,
    _score_align,
    _stability_metrics,
    _summary_discipline_metrics,
)
import copy
import statistics


def _critical_issue_metrics_offline(rows: list[dict]) -> dict:
    """Variant of _critical_issue_metrics that reads agent_issue_set from row
    instead of result.unsupported_model_elements (which is unavailable when
    loading from JSON checkpoints)."""
    relevant_rows = [row for row in rows if row.get("eval_bucket") != "component"]
    by_type = {issue: {"support": 0, "recalled": 0, "recall": 0.0} for issue in CRITICAL_ISSUE_TAXONOMY}
    total = 0
    recalled = 0
    for row in relevant_rows:
        human = set(row.get("human_issue_set", [])) & set(CRITICAL_ISSUE_TAXONOMY)
        agent = set(row.get("agent_issue_set", [])) & set(CRITICAL_ISSUE_TAXONOMY)
        total += len(human)
        recalled += len(human & agent)
        for issue in human:
            by_type[issue]["support"] += 1
            if issue in agent:
                by_type[issue]["recalled"] += 1
    for stats in by_type.values():
        support = int(stats["support"])
        stats["recall"] = stats["recalled"] / support if support else 1.0
    return {
        "critical_issue_support": total,
        "critical_issue_recalled": recalled,
        "critical_issue_recall": recalled / total if total else 1.0,
        "by_type": by_type,
    }

CORPUS_ROOT = Path(__file__).resolve().parent.parent
WK2 = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "week2"
CKPT = WK2 / "checkpoints"


_CONFIGS = [
    # (label, expected n_reruns, variance_source, confidence_alpha)
    ("q3_temp_n3", 3, "temp", 2.0),
    ("q3_para_n3", 3, "paraphrase", 2.0),
    ("q3_both_n3", 3, "both", 2.0),
    ("q3_both_n3_62task", 3, "both", 2.0),
]


class _Wrapper:
    def __init__(self, row: dict):
        self.overall_score = row.get("agent_score", 0.0)
        self.overall_judgement = row.get("agent_judgement", "?")
        self.confidence = row.get("agent_confidence", 0.0)
        dim_scores = row.get("agent_dim_scores") or {}
        if isinstance(dim_scores, dict):
            self.dimension_results = [
                {"dimension_name": k, "score": float(v)}
                for k, v in dim_scores.items()
            ]
        else:
            self.dimension_results = []


def _reaggregate_one(label: str, n_reruns: int, source: str, alpha: float) -> dict | None:
    rerun_files = [CKPT / f"week2_q3_{label}_rerun{i}.json" for i in range(n_reruns)]
    if not all(p.exists() for p in rerun_files):
        missing = [p.name for p in rerun_files if not p.exists()]
        print(f"[skip] {label}: missing checkpoints {missing}")
        return None
    rerun_reports = [json.loads(p.read_text()) for p in rerun_files]
    print(f"[{label}] loaded {len(rerun_reports)} rerun checkpoints")

    task_index: dict[str, list] = {}
    for report in rerun_reports:
        for row in report.get("normalized_rows", []):
            tid = row.get("task_id", "?")
            task_index.setdefault(tid, []).append(row)

    agg_lookup: dict[str, dict] = {}
    for tid, rows in task_index.items():
        wrappers = [_Wrapper(r) for r in rows]
        agg = _aggregate_runs(wrappers, confidence_alpha=alpha)
        agg_lookup[tid] = agg

    template = copy.deepcopy(rerun_reports[0])
    rebuilt_rows = []
    n_disagreement = 0
    max_dim_stds_collected = []
    for row in template.get("normalized_rows", []):
        tid = row.get("task_id")
        agg = agg_lookup.get(tid, {})
        if agg:
            row = dict(row)
            row["agent_score"] = agg.get("overall_score", row.get("agent_score"))
            row["agent_judgement"] = agg.get("overall_judgement", row.get("agent_judgement"))
            row["agent_confidence"] = agg.get("confidence", row.get("agent_confidence"))
            row["sc_consistency_confidence"] = agg.get("sc_consistency_confidence")
            row["sc_disagreement_flag"] = agg.get("disagreement_flag")
            row["sc_max_dim_std"] = agg.get("max_dim_std")
            row["sc_n_runs"] = agg.get("n_runs")
            if agg.get("disagreement_flag"):
                n_disagreement += 1
            if agg.get("max_dim_std") is not None:
                max_dim_stds_collected.append(agg["max_dim_std"])
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
    critical_issue_metrics = _critical_issue_metrics_offline(record_rows + summary_rows)
    hai_legacy = 0.55 * ras + 0.25 * sas + 0.20 * protocol_metrics["PDS"]
    hai = 0.40 * ras + 0.30 * sas + 0.30 * component_metrics["CRAS"]

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
        "critical_issue_metrics": critical_issue_metrics,
        "HAI": hai,
        "HAI_legacy": hai_legacy,
        "pds_gate": {"threshold": 95.0, "value": protocol_metrics["PDS"], "passed": bool(protocol_metrics["PDS"] >= 95.0)},
        "normalized_rows": rebuilt_rows,
        "self_consistency_summary": {
            "scheme": "self_consistency",
            "n_reruns": n_reruns,
            "variance_source": source,
            "confidence_alpha": alpha,
            "n_disagreement_flag_true": n_disagreement,
            "n_total_tasks": len(agg_lookup),
            "mean_max_dim_std": (
                statistics.mean(max_dim_stds_collected) if max_dim_stds_collected else 0.0
            ),
            "patch_note": "2026-05-07 confidence-formula fix applied: agent_confidence = median of run confidences (downstream-compatible); sc_consistency_confidence = clip(1-α·max_dim_std, 0.10, 0.99) preserved as auxiliary",
        },
    })
    # contradiction_metrics / runtime_metrics / error_map kept from template (unaffected by fix)
    return aggregated_report


def main() -> None:
    for label, n_reruns, source, alpha in _CONFIGS:
        aggregated_report = _reaggregate_one(label, n_reruns, source, alpha)
        if aggregated_report is None:
            continue
        output = WK2 / f"report_{label}.json"
        output.write_text(
            json.dumps(aggregated_report, ensure_ascii=False, indent=2, default=str)
        )
        hai = aggregated_report.get("HAI", 0)
        sas = aggregated_report.get("summary_metrics", {}).get("SAS", 0)
        ras = aggregated_report.get("record_metrics", {}).get("RAS", 0)
        kappa = aggregated_report.get("judgement_metrics", {}).get("weighted_kappa", 0)
        print(f"[{label}] re-aggregated → {output.name}: HAI={hai:.2f} RAS={ras:.2f} SAS={sas:.2f} kappa={kappa:.3f}")


if __name__ == "__main__":
    main()
