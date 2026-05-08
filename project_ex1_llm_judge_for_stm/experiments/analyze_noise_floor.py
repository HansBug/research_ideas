"""Aggregate Week 3 noise-floor experiment reports into mean ± std summary
+ per-task variance breakdown + cross-config comparison.

Reads:
  etl/out/phase14_combined/week3_noise/noise_n{1,2,3,4}_*_rep{1..5}.json

Writes:
  etl/out/phase14_combined/week3_noise/noise_summary.json
  etl/out/phase14_combined/week3_noise/noise_per_task_variance.json
  etl/sc_self_investigation_data.json (NOT touched — separate concern)

Run:
  python -m project_ex1_llm_judge_for_stm.state_machine_review_corpus.etl.analyze_noise_floor
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

CORPUS_ROOT = Path(__file__).resolve().parent.parent
OUT = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "week3_noise"

CONFIGS = {
    "N1_W1.5_B-only": [OUT / f"noise_n1_w15_rep{k}.json" for k in range(1, 6)],
    "N2_SC-N1_T0_V1": [OUT / f"noise_n2_sc_n1_rep{k}.json" for k in range(1, 6)],
    "N3_W0_LLM-auto": [OUT / f"noise_n3_w0_rep{k}.json" for k in range(1, 6)],
    "N4_W1_rubric-v0": [OUT / f"noise_n4_w1_rep{k}.json" for k in range(1, 6)],
}

# 与 W1.5/W2 PR comment 对齐的核心指标
METRICS = [
    ("HAI", "HAI"),
    ("HAI_legacy", "HAI_legacy"),
    ("RAS", "record_metrics.RAS"),
    ("SAS", "summary_metrics.SAS"),
    ("CRAS", "component_metrics.CRAS"),
    ("PDS", "protocol_metrics.PDS"),
    ("record_ScoreAlign", "record_metrics.ScoreAlign"),
    ("record_RankAlign", "record_metrics.pairwise_order_accuracy"),
    ("record_Calib", "record_metrics.Calib"),
    ("record_ReasonAlign", "record_metrics.ReasonAlign"),
    ("record_EquivAlign", "record_metrics.EquivAlign"),
    ("summary_ScoreAlign", "summary_metrics.ScoreAlign"),
    ("summary_RankAlign", "summary_metrics.RankAlign"),
    ("summary_Spearman", "summary_metrics.spearman_rho"),
    ("summary_EvDisc", "summary_metrics.EvidenceDiscipline"),
    ("summary_Stability", "summary_metrics.Stability"),
    ("weighted_kappa", "judgement_metrics.weighted_kappa"),
    ("crit_recall", "critical_issue_metrics.recall"),
]

# 历史 single-shot 数据（用于对比新分布）
HISTORICAL_SINGLE_SHOT = {
    "N1_W1.5_B-only": {  # from week15/report_iter_b_only_62task.json
        "HAI": 81.755, "RAS": 77.481, "SAS": 69.210, "CRAS": 100.000, "PDS": 100.000,
        "record_ScoreAlign": 61.687, "record_Calib": 90.201,
        "summary_ScoreAlign": 63.754, "summary_RankAlign": 70.833, "summary_Spearman": 0.606,
        "summary_EvDisc": 55.000, "weighted_kappa": 0.618,
    },
    "N3_W0_LLM-auto": {  # from week0 (HAI=85.02 stated)
        "HAI": 85.02, "RAS": 83.71, "SAS": 71.77, "CRAS": 100.0, "PDS": 100.0,
    },
    "N4_W1_rubric-v0": {  # from week1
        "HAI": 78.51,  # known mixed-signal location
    },
    "N2_SC-N1_T0_V1": {  # from week2 q3 SC rerun_0
        "HAI": 83.547, "RAS": 80.495, "SAS": 71.164,
        "summary_ScoreAlign": 53.953, "summary_RankAlign": 58.333, "summary_Spearman": 0.255,
        "summary_EvDisc": 100.000, "record_Calib": 79.938, "weighted_kappa": 0.618,
    },
}


def _resolve(d, dotted):
    cur = d
    for p in dotted.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur if isinstance(cur, (int, float)) else None


def _by_task(rep, key="task_id"):
    return {row.get(key): row for row in rep.get("normalized_rows", []) if row.get(key)}


def main() -> None:
    summary = {}
    per_task_variance = {}
    for cfg_name, paths in CONFIGS.items():
        existing = [p for p in paths if p.exists()]
        if len(existing) < len(paths):
            missing = [p.name for p in paths if not p.exists()]
            print(f"[warn] {cfg_name}: missing {missing}")
        if not existing:
            continue
        reports = [json.loads(p.read_text()) for p in existing]
        n_reps = len(reports)
        cfg_summary = {"n_reps": n_reps, "rep_files": [p.name for p in existing], "metrics": {}}
        for label, dotted in METRICS:
            vals = [_resolve(r, dotted) for r in reports]
            vals = [v for v in vals if v is not None]
            if not vals:
                continue
            entry = {
                "n": len(vals),
                "values": vals,
                "mean": statistics.mean(vals),
                "median": statistics.median(vals),
                "min": min(vals),
                "max": max(vals),
                "range": max(vals) - min(vals),
                "std": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
                "std_sample": statistics.stdev(vals) if len(vals) > 1 else 0.0,
            }
            hist = HISTORICAL_SINGLE_SHOT.get(cfg_name, {}).get(label)
            if hist is not None:
                entry["historical_single_shot"] = hist
                if entry["std"] > 0:
                    entry["historical_z_score"] = (hist - entry["mean"]) / entry["std"]
                entry["historical_within_2std"] = abs(hist - entry["mean"]) <= 2 * entry["std"] if entry["std"] > 0 else None
            cfg_summary["metrics"][label] = entry
        summary[cfg_name] = cfg_summary

        # Per-task variance
        common_tids: set | None = None
        for r in reports:
            tids = set(_by_task(r).keys())
            common_tids = tids if common_tids is None else common_tids & tids
        if not common_tids:
            continue
        idx = [_by_task(r) for r in reports]
        per_task = {}
        for tid in common_tids:
            scores = [idx[k][tid].get("agent_score") for k in range(n_reps)]
            scores = [s for s in scores if s is not None]
            if len(scores) < 2:
                continue
            judgements = [idx[k][tid].get("agent_judgement") for k in range(n_reps)]
            human = idx[0][tid].get("human_score")
            bucket = idx[0][tid].get("eval_bucket")
            per_task[tid] = {
                "bucket": bucket,
                "human_score": human,
                "agent_scores": scores,
                "score_mean": statistics.mean(scores),
                "score_std": statistics.pstdev(scores),
                "score_range": max(scores) - min(scores),
                "judgement_distribution": {j: judgements.count(j) for j in set(judgements) if j is not None},
                "n_distinct_judgements": len(set(j for j in judgements if j is not None)),
            }
        per_task_variance[cfg_name] = per_task

    OUT.mkdir(parents=True, exist_ok=True)
    summary_path = OUT / "noise_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    per_task_path = OUT / "noise_per_task_variance.json"
    per_task_path.write_text(json.dumps(per_task_variance, ensure_ascii=False, indent=2, default=str))
    print(f"summary written → {summary_path}")
    print(f"per-task variance written → {per_task_path}")

    # Console table preview
    print(f"\n{'config':<22}{'n_reps':>7}", end="")
    for label, _ in METRICS[:6]:
        print(f"{label[:14]:>16}", end="")
    print()
    for cfg_name, cfg_data in summary.items():
        print(f"{cfg_name:<22}{cfg_data['n_reps']:>7}", end="")
        for label, _ in METRICS[:6]:
            m = cfg_data["metrics"].get(label, {})
            mu = m.get("mean", 0)
            sd = m.get("std", 0)
            print(f"  {mu:>6.2f}±{sd:<5.2f}", end="")
        print()


if __name__ == "__main__":
    main()
