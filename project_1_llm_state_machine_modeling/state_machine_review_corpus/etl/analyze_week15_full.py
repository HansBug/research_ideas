"""Comprehensive Week 1.5 analysis:
- 40-task ablation grid: 8 configs (det / LLM / v0 / A / B / C / A+B / A+B+C)
- 62-task validation: 4 configs (det Week 0 / LLM Week 0 / iter_v0 Week 1 / B-only / A+B)

Produces:
- per-slice metrics tables
- 2x2 A×B grid (Iter-A on/off × Iter-B on/off)
- 62-task winner identification vs Week 0 baseline
- Acceptance gate compliance per config
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
PHASE14 = CORPUS_ROOT / "etl" / "out" / "phase14_combined"
ABL = PHASE14 / "ablation"
WK15 = PHASE14 / "week15"


# 40-task slice configs
CONFIGS_40 = [
    ("baseline_det", "deterministic (no LLM, no rubric)", ABL / "report_baseline_det.json"),
    ("baseline_llm", "LLM-mode (no rubric)", ABL / "report_baseline_llm.json"),
    ("iter_v0", "rubric v0 (no iter)", ABL / "report_iter_v0.json"),
    ("iter_a_only", "Iter-A only", ABL / "report_iter_a_only.json"),
    ("iter_b_only", "Iter-B only", ABL / "report_iter_b_only.json"),
    ("iter_c_only", "Iter-C only", ABL / "report_iter_c_only.json"),
    ("iter_a_b", "Iter-A+B (no C)", ABL / "report_iter_a_b.json"),
    ("iter_abc", "Iter-A+B+C", ABL / "report_iter_abc.json"),
]

# 62-task slice configs
CONFIGS_62 = [
    ("week0_det_full", "Week 0 deterministic full (973 rows)",
     PHASE14 / "report_deterministic.json", "slice_report"),
    ("week0_llm_slice", "Week 0 LLM-mode slice (62 task, no rubric)",
     PHASE14 / "report_slice_llm_auto.json", None),
    ("week1_v0_slice", "Week 1 v0 rubric slice (62 task, no iter)",
     PHASE14 / "report_slice_rubric_llm.json", None),
    ("week15_b_only_62", "Week 1.5 Iter-B only on 62 task",
     WK15 / "report_iter_b_only_62task.json", None),
    ("week15_a_b_62", "Week 1.5 Iter-A+B on 62 task",
     WK15 / "report_iter_a_b_62task.json", None),
]


METRICS = [
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


def load_config(path: Path, sub_key: str | None = None) -> dict | None:
    if not path.exists():
        return None
    try:
        report = json.loads(path.read_text())
    except Exception:
        return None
    if sub_key:
        return report.get(sub_key)
    return report


def build_table(configs: list[tuple]) -> pd.DataFrame:
    reports = {}
    for label, _desc, path, *rest in configs:
        sub_key = rest[0] if rest else None
        rep = load_config(path, sub_key)
        if rep is not None:
            reports[label] = rep
    rows = []
    for metric_label, dotted in METRICS:
        row = {"metric": metric_label}
        for label, _, *_ in configs:
            row[label] = _resolve(reports[label], dotted) if label in reports else None
        rows.append(row)
    return pd.DataFrame(rows), reports


def main() -> None:
    print("=" * 90)
    print("WEEK 1.5 COMPREHENSIVE ABLATION ANALYSIS")
    print("=" * 90)

    # === 40-task ablation grid (extended with iter_a_b) ===
    print("\n[1/3] 40-task ablation grid (8 configs):")
    df40, rep40 = build_table(CONFIGS_40)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 220)
    print(df40.to_string(index=False, float_format=lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)))

    # === 2x2 A×B grid ===
    print("\n[2/3] 2x2 A×B ablation (40-task slice, no Iter-C):")
    if all(c in rep40 for c in ("iter_v0", "iter_a_only", "iter_b_only", "iter_a_b")):
        labels = [
            ("A=0,B=0", "iter_v0"),
            ("A=1,B=0", "iter_a_only"),
            ("A=0,B=1", "iter_b_only"),
            ("A=1,B=1", "iter_a_b"),
        ]
        for metric in ["HAI", "RAS", "SAS", "summary_RankAlign", "summary_Spearman", "record_ScoreAlign"]:
            print(f"  {metric}:")
            for tag, cfg in labels:
                v = df40[df40["metric"] == metric][cfg].iloc[0]
                if v is not None:
                    print(f"    {tag} ({cfg}): {v:.4f}")

    # === 62-task validation ===
    print("\n[3/3] 62-task validation (4-5 configs):")
    df62, rep62 = build_table([(l, d, p, *r) for l, d, p, *r in CONFIGS_62])
    print(df62.to_string(index=False, float_format=lambda x: f"{x:.4f}" if isinstance(x, float) else str(x)))

    # === Acceptance gates on 62-task slice ===
    print("\n=== Acceptance gates on 62-task slice ===")
    gates = {
        "HAI": 85.02,
        "record_ScoreAlign": 65.0,
        "summary_ScoreAlign": 60.0,
        "summary_RankAlign": 70.0,
        "summary_Spearman": 0.45,
        "weighted_kappa": 0.65,
        "crit_issue_recall": 0.90,
    }
    rows = []
    for gate, target in gates.items():
        row = {"gate": gate, "target": target}
        for label, _, *_ in CONFIGS_62:
            v = df62[df62["metric"] == gate][label].iloc[0] if label in df62.columns else None
            if v is None or pd.isna(v):
                row[label] = None
            else:
                row[label] = "✓" if v >= target else f"✗ ({v:.2f})"
        rows.append(row)
    gate_df = pd.DataFrame(rows)
    print(gate_df.to_string(index=False))

    # Pass counts per config
    print("\nPass counts per 62-task config:")
    for label, _, *_ in CONFIGS_62:
        if label in df62.columns:
            count = sum(
                1 for r in gate_df.itertuples()
                if isinstance(getattr(r, label, None), str) and getattr(r, label) == "✓"
            )
            print(f"  {label}: {count}/{len(gates)}")

    # Save consolidated summary
    out = WK15 / "week15_summary.json"
    out.write_text(
        json.dumps(
            {
                "configs_40task": dict((l, d) for l, d, _, *_ in CONFIGS_40),
                "configs_62task": dict((l, d) for l, d, _, *_ in CONFIGS_62),
                "metrics_40task": df40.to_dict(orient="records"),
                "metrics_62task": df62.to_dict(orient="records"),
                "acceptance_gates_62": gate_df.to_dict(orient="records"),
                "gate_thresholds": gates,
            },
            ensure_ascii=False,
            indent=2,
            default=str,
        )
    )
    print(f"\nSaved: {out}")


if __name__ == "__main__":
    main()
