"""Systematic ablation analysis: how much does each Iter (A/B/C) contribute?

Loads all 7 configs (det baseline / LLM no-rubric / v0 rubric / A only / B only / C only / A+B+C),
computes deltas vs each baseline, and writes a JSON summary + tabular view.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ABL = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "ablation"

CONFIGS = [
    ("baseline_det", "deterministic (no LLM, no rubric)"),
    ("baseline_llm", "LLM-mode (no rubric)"),
    ("iter_v0", "rubric v0 (no iter)"),
    ("iter_a_only", "Iter-A only (asymmetric bounds)"),
    ("iter_b_only", "Iter-B only (differentiation prompt)"),
    ("iter_c_only", "Iter-C only (selective: rubric record/mixed only)"),
    ("iter_abc", "Iter-A+B+C (kitchen sink)"),
]

METRICS_TO_TRACK = [
    ("HAI", "HAI"),
    ("HAI_legacy", "HAI_legacy"),
    ("RAS", "record_metrics.RAS"),
    ("SAS", "summary_metrics.SAS"),
    ("CRAS", "component_metrics.CRAS"),
    ("PDS", "protocol_metrics.PDS"),
    ("record_ScoreAlign", "record_metrics.ScoreAlign"),
    ("record_issue_f1", "record_metrics.issue_f1"),
    ("record_EquivAlign", "record_metrics.EquivAlign"),
    ("record_Calib", "record_metrics.Calib"),
    ("summary_ScoreAlign", "summary_metrics.ScoreAlign"),
    ("summary_RankAlign", "summary_metrics.RankAlign"),
    ("summary_Spearman", "summary_metrics.spearman_rho"),
    ("crit_issue_recall", "critical_issue_metrics.critical_issue_recall"),
    ("judg_macro_f1", "judgement_metrics.macro_f1"),
    ("weighted_kappa", "judgement_metrics.weighted_kappa"),
    ("unsupported_claim_rate", "record_metrics.unsupported_claim_rate"),
    ("token_total", "runtime_metrics.llm_total_tokens"),
    ("latency_p95", "runtime_metrics.latency_p95"),
]


def _resolve(report: dict, dotted: str) -> float | None:
    cur = report
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return float(cur) if isinstance(cur, (int, float)) else None


def load_all_configs() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for label, _desc in CONFIGS:
        p = ABL / f"report_{label}.json"
        if p.exists():
            try:
                out[label] = json.loads(p.read_text())
            except Exception as e:
                print(f"WARN: cannot load {p}: {e}")
    return out


def build_metrics_table(reports: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for metric_label, dotted in METRICS_TO_TRACK:
        row: dict[str, float | None] = {"metric": metric_label}
        for cfg_label, _ in CONFIGS:
            if cfg_label in reports:
                row[cfg_label] = _resolve(reports[cfg_label], dotted)
            else:
                row[cfg_label] = None
        rows.append(row)
    df = pd.DataFrame(rows)
    return df


def compute_deltas(df: pd.DataFrame, baseline_col: str = "iter_v0") -> pd.DataFrame:
    """Compute Δ vs given baseline."""
    delta = df[["metric"]].copy()
    if baseline_col not in df.columns:
        return delta
    base = df[baseline_col]
    for cfg_label, _ in CONFIGS:
        if cfg_label == baseline_col:
            continue
        if cfg_label not in df.columns:
            continue
        delta[f"Δ_{cfg_label}_vs_{baseline_col}"] = df[cfg_label] - base
    return delta


def find_winner(df: pd.DataFrame) -> str:
    """Pick winner based on simple weighted score:
    HAI weight 3, summary RankAlign weight 2, summary Spearman weight 2,
    record ScoreAlign weight 1, all others weight 1. Higher is better.
    """
    scoring_metrics = {
        "HAI": 3.0,
        "summary_RankAlign": 2.0,
        "summary_Spearman": 2.0,
        "record_ScoreAlign": 1.0,
        "summary_ScoreAlign": 1.0,
        "crit_issue_recall": 1.0,
        "judg_macro_f1": 0.5,
        "weighted_kappa": 0.5,
    }
    scores: dict[str, float] = {}
    for cfg_label, _ in CONFIGS:
        if cfg_label not in df.columns or cfg_label == "baseline_det":
            continue
        total = 0.0
        for m, w in scoring_metrics.items():
            row = df[df["metric"] == m]
            if len(row) == 0:
                continue
            v = row[cfg_label].iloc[0]
            if pd.isna(v):
                continue
            # Normalize Spearman (could be 0-1)
            if m == "summary_Spearman":
                v = v * 100
            total += w * v
        scores[cfg_label] = total
    best = max(scores, key=scores.get) if scores else None
    return best, scores


def acceptance_gates(df: pd.DataFrame, gates: dict[str, float]) -> pd.DataFrame:
    """Mark pass/fail per config per gate."""
    rows = []
    for gate_name, target in gates.items():
        row = {"gate": gate_name, "target": target}
        for cfg_label, _ in CONFIGS:
            if cfg_label not in df.columns:
                row[cfg_label] = None
                continue
            metric_row = df[df["metric"] == gate_name]
            if len(metric_row) == 0:
                row[cfg_label] = None
                continue
            v = metric_row[cfg_label].iloc[0]
            if pd.isna(v):
                row[cfg_label] = None
            else:
                row[cfg_label] = "✓" if v >= target else f"✗ ({v:.2f})"
        rows.append(row)
    return pd.DataFrame(rows)


def main() -> None:
    reports = load_all_configs()
    print(f"Loaded {len(reports)} / {len(CONFIGS)} configs:")
    for label, desc in CONFIGS:
        flag = "✓" if label in reports else "✗"
        print(f"  {flag} {label}: {desc}")
    print()

    if not reports:
        print("NO REPORTS YET")
        return

    metrics_df = build_metrics_table(reports)
    deltas_df = compute_deltas(metrics_df, baseline_col="iter_v0")

    winner, scores = find_winner(metrics_df)
    print(f"\n=== Composite-score winner ===")
    for k, v in sorted(scores.items(), key=lambda x: -x[1]):
        marker = "🏆" if k == winner else "  "
        print(f"  {marker} {k}: {v:.2f}")
    print()

    # Acceptance gates from Week 0
    gates = {
        "HAI": 85.02,  # Week 0 baseline floor
        "record_ScoreAlign": 65.0,
        "summary_ScoreAlign": 60.0,
        "summary_RankAlign": 70.0,
        "summary_Spearman": 0.45,
        "weighted_kappa": 0.65,
        "crit_issue_recall": 0.90,
    }
    gate_df = acceptance_gates(metrics_df, gates)
    print("=== Acceptance gates ===")
    print(gate_df.to_string(index=False))
    print()

    print("=== Headline metrics across configs ===")
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 200)
    print(metrics_df.to_string(index=False, float_format=lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)))
    print()

    print("=== Deltas vs iter_v0 (rubric without iter) ===")
    print(deltas_df.to_string(index=False, float_format=lambda x: f"{x:+.4f}" if isinstance(x, float) else str(x)))

    # Save JSON summary
    out_json = ABL / "ablation_summary.json"
    summary = {
        "configs": dict(CONFIGS),
        "winner": winner,
        "winner_scores": scores,
        "metrics_table": metrics_df.to_dict(orient="records"),
        "deltas_vs_v0": deltas_df.to_dict(orient="records"),
        "acceptance_gates": gate_df.to_dict(orient="records"),
        "gate_thresholds": gates,
    }
    out_json.write_text(json.dumps(summary, ensure_ascii=False, indent=2, default=str))
    print(f"\nSaved: {out_json}")


if __name__ == "__main__":
    main()
