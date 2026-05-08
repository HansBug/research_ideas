"""Charts for Week 0 phase14 strict baseline run."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
PHASE14 = CORPUS_ROOT / "etl" / "out" / "phase14_combined"
CHARTS = CORPUS_ROOT / "etl" / "out" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def chart_phase13_vs_combined() -> Path:
    """Phase 13 baseline (820 rows) vs Combined (973 rows) deterministic full."""
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())
    full_r = det["full_report"]

    # Phase 13 historical (issue 4272619082)
    phase13 = {
        "HAI_legacy": 86.86, "RAS": 84.37, "SAS": 81.80,
        "CRAS": 100.0, "PDS": 100.0,
        "judg_macro_f1": 79.96, "weighted_kappa": 84.52,
        "unsupported_claim_rate": 7.92,
    }
    combined = {
        "HAI_legacy": full_r["HAI_legacy"],
        "RAS": full_r["record_metrics"]["RAS"],
        "SAS": full_r["summary_metrics"]["SAS"],
        "CRAS": full_r["component_metrics"]["CRAS"],
        "PDS": full_r["protocol_metrics"]["PDS"],
        "judg_macro_f1": full_r["judgement_metrics"]["macro_f1"] * 100,
        "weighted_kappa": full_r["judgement_metrics"]["weighted_kappa"] * 100,
        "unsupported_claim_rate": full_r["record_metrics"]["unsupported_claim_rate"] * 100,
    }

    metrics = ["HAI_legacy", "RAS", "SAS", "CRAS", "PDS", "judg_macro_f1", "weighted_kappa"]
    labels = ["HAI\n(legacy)", "RAS", "SAS", "CRAS", "PDS", "judgement\nmacro_F1", "weighted\nkappa"]
    p13 = [phase13[m] for m in metrics]
    cm = [combined[m] for m in metrics]

    x = np.arange(len(metrics))
    w = 0.38
    fig, ax = plt.subplots(figsize=(10, 4.6))
    bars1 = ax.bar(x - w/2, p13, w, color="#9ca3af", label="Phase 13 (820 rows, baseline)")
    bars2 = ax.bar(x + w/2, cm, w, color="#2563eb", label="Combined (973 rows, +protocol-FSM)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("score (0..100)")
    ax.set_ylim(0, 110)
    ax.set_title("Phase 13 baseline → Combined (after adding 153 protocol-FSM rows): deterministic full")
    ax.legend(loc="lower right")
    for b, v in zip(bars1, p13):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=8, color="#374151")
    for b, v in zip(bars2, cm):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=8, color="#1e3a8a", fontweight="bold")
    for i, (a, b) in enumerate(zip(p13, cm)):
        d = b - a
        c = "#16a34a" if d > 0 else ("#9ca3af" if abs(d) < 0.5 else "#dc2626")
        ax.text(i, max(a, b) + 8, f"Δ {d:+.1f}", ha="center", fontsize=9, color=c, fontweight="bold")
    fig.tight_layout()
    out = CHARTS / "20_phase13_vs_combined.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_per_split() -> Path:
    """HAI / RAS / SAS per split (train/dev/validation/lockbox)."""
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())
    splits = det.get("split_summary") or {}
    if not splits:
        return Path()

    split_names = ["train", "dev", "validation", "lockbox"]
    metrics_to_plot = ["HAI", "RAS", "SAS"]
    fig, ax = plt.subplots(figsize=(9, 4.6))
    x = np.arange(len(split_names))
    w = 0.25
    colors = {"HAI": "#2563eb", "RAS": "#9ca3af", "SAS": "#dc2626"}
    for i, m in enumerate(metrics_to_plot):
        vals = [splits[s].get(m, 0) for s in split_names]
        bars = ax.bar(x + (i - 1) * w, vals, w, color=colors[m], label=m)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=8)
    ax.set_xticks(x)
    ax.set_xticklabels(split_names)
    ax.set_ylabel("score")
    ax.set_ylim(0, 100)
    ax.set_title("Combined 973 rows: HAI / RAS / SAS by data split (deterministic full)")
    ax.legend(loc="lower right")
    fig.tight_layout()
    out = CHARTS / "21_per_split.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_lofo_worst() -> Path:
    """LOFO worst-fold gap per regime — the cross-domain generalization stress test."""
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())
    gen = det.get("lofo_generalization") or {}
    if not gen:
        return Path()

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # Left: worst-fold gap per regime (lower = better generalization)
    regimes = ["record", "summary", "component", "protocol"]
    worst_gaps = [gen[r].get("worst_holdout_gap_vs_full", 0) for r in regimes]
    avg_gaps = [gen[r].get("avg_gap_vs_full", 0) for r in regimes]
    family_counts = [
        det["lofo_summary"][r].get("family_count", 0) for r in regimes
    ]

    x = np.arange(len(regimes))
    w = 0.4
    axes[0].bar(x - w/2, avg_gaps, w, color="#9ca3af", label="avg fold gap")
    bars2 = axes[0].bar(x + w/2, worst_gaps, w, color="#dc2626", label="worst-fold gap")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels([f"{r}\n({c} folds)" for r, c in zip(regimes, family_counts)])
    axes[0].set_ylabel("LOFO gap (lower = better cross-fold generalization)")
    axes[0].set_title("LOFO worst-fold gap per regime")
    axes[0].axhline(13.09, color="#fbbf24", linestyle="--", linewidth=1)
    axes[0].text(0.02, 13.5, "Phase 14 baseline worst (record) = 13.09", fontsize=8, color="#92400e")
    for b, v in zip(bars2, worst_gaps):
        axes[0].text(b.get_x() + b.get_width()/2, v + 0.5, f"{v:.2f}", ha="center", fontsize=9, color="#7f1d1d", fontweight="bold")
    axes[0].legend()
    axes[0].set_ylim(0, max(worst_gaps) * 1.15)

    # Right: summary regime fold-level metric (the regime hit hardest)
    summary_gen = gen.get("summary", {})
    metrics = ["full_SAS", "avg_SAS", "worst_holdout_SAS"]
    labels = ["full\n(all data)", "avg fold", "worst fold\n(holdout)"]
    vals = [summary_gen.get(m, 0) for m in metrics]
    colors = ["#16a34a", "#9ca3af", "#dc2626"]
    bars = axes[1].bar(labels, vals, color=colors)
    for b, v in zip(bars, vals):
        axes[1].text(b.get_x() + b.get_width()/2, v + 1, f"{v:.2f}", ha="center", fontsize=10, fontweight="bold")
    axes[1].set_ylabel("SAS")
    axes[1].set_ylim(0, 100)
    axes[1].set_title(f"Summary regime LOFO drilldown\n(worst family = {summary_gen.get('worst_family','?')})")
    fig.tight_layout()
    out = CHARTS / "22_lofo_worst.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_record_metrics_breakdown() -> Path:
    """Record-level sub-metrics: ScoreAlign / issue_F1 / ReasonAlign / EquivAlign / Calib."""
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())
    full_r = det["full_report"]
    rm = full_r["record_metrics"]
    sm = full_r["summary_metrics"]

    submetrics_record = {
        "ScoreAlign": rm["ScoreAlign"],
        "issue_f1·100": rm["issue_f1"] * 100,
        "ReasonAlign": rm["ReasonAlign"],
        "EquivAlign": rm["EquivAlign"],
        "Calib": rm["Calib"],
    }
    weights_record = {
        "ScoreAlign": 0.30, "issue_f1·100": 0.25, "ReasonAlign": 0.20,
        "EquivAlign": 0.15, "Calib": 0.10,
    }
    contributions_record = {k: v * weights_record[k] for k, v in submetrics_record.items()}

    submetrics_summary = {
        "ScoreAlign": sm["ScoreAlign"],
        "RankAlign": sm["RankAlign"],
        "EvidDisc": sm["EvidenceDiscipline"],
        "Stability": sm["Stability"],
    }
    weights_summary = {"ScoreAlign": 0.40, "RankAlign": 0.25, "EvidDisc": 0.20, "Stability": 0.15}
    contributions_summary = {k: v * weights_summary[k] for k, v in submetrics_summary.items()}

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))

    # Left: record sub-metrics + their weighted contribution to RAS
    keys = list(submetrics_record.keys())
    raw = [submetrics_record[k] for k in keys]
    contrib = [contributions_record[k] for k in keys]
    x = np.arange(len(keys))
    w = 0.4
    axes[0].bar(x - w/2, raw, w, color="#9ca3af", label="raw value")
    axes[0].bar(x + w/2, contrib, w, color="#2563eb", label="weighted contribution to RAS")
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(keys, rotation=0, fontsize=9)
    axes[0].set_title(f"RAS = Σ(weight·sub-metric) = {full_r['record_metrics']['RAS']:.2f}")
    axes[0].set_ylabel("score")
    axes[0].set_ylim(0, 100)
    axes[0].legend()
    for i, (r, c) in enumerate(zip(raw, contrib)):
        axes[0].text(i - w/2, r + 1, f"{r:.1f}", ha="center", fontsize=8)
        axes[0].text(i + w/2, c + 1, f"{c:.1f}", ha="center", fontsize=8, fontweight="bold")

    # Right: summary sub-metrics
    keys = list(submetrics_summary.keys())
    raw = [submetrics_summary[k] for k in keys]
    contrib = [contributions_summary[k] for k in keys]
    x = np.arange(len(keys))
    axes[1].bar(x - w/2, raw, w, color="#9ca3af", label="raw value")
    axes[1].bar(x + w/2, contrib, w, color="#dc2626", label="weighted contribution to SAS")
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(keys, fontsize=9)
    axes[1].set_title(f"SAS = Σ(weight·sub-metric) = {full_r['summary_metrics']['SAS']:.2f}")
    axes[1].set_ylim(0, 100)
    axes[1].legend()
    for i, (r, c) in enumerate(zip(raw, contrib)):
        axes[1].text(i - w/2, r + 1, f"{r:.1f}", ha="center", fontsize=8)
        axes[1].text(i + w/2, c + 1, f"{c:.1f}", ha="center", fontsize=8, fontweight="bold")

    fig.tight_layout()
    out = CHARTS / "23_ras_sas_breakdown.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_det_vs_llm() -> Path:
    """Deterministic vs LLM-enabled slice (if LLM report exists)."""
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())
    llm_report_path = PHASE14 / "report_slice_llm_auto.json"
    if not llm_report_path.exists():
        return Path()
    llm_r = json.loads(llm_report_path.read_text())
    det_slice = det["slice_report"]

    metrics = ["HAI", "HAI_legacy"]
    labels_x = ["HAI (post-Tier-A)", "HAI_legacy"]
    pairs = []
    for m in metrics:
        pairs.append((det_slice.get(m, 0), llm_r.get(m, 0)))
    sub_metric_labels = []
    sub_metric_pairs = []
    for prefix, name in [("record_metrics", "RAS"), ("summary_metrics", "SAS"),
                         ("component_metrics", "CRAS"), ("protocol_metrics", "PDS")]:
        sub_metric_labels.append(name)
        sub_metric_pairs.append((det_slice[prefix].get(name, 0), llm_r[prefix].get(name, 0)))

    fig, ax = plt.subplots(figsize=(10, 4.5))
    all_labels = labels_x + sub_metric_labels
    all_pairs = pairs + sub_metric_pairs
    x = np.arange(len(all_labels))
    w = 0.4
    det_vals = [p[0] for p in all_pairs]
    llm_vals = [p[1] for p in all_pairs]
    ax.bar(x - w/2, det_vals, w, color="#9ca3af", label="deterministic slice")
    ax.bar(x + w/2, llm_vals, w, color="#16a34a", label="LLM-enabled slice (gpt-5.5/airouter)")
    ax.set_xticks(x)
    ax.set_xticklabels(all_labels, rotation=0)
    ax.set_ylabel("score")
    ax.set_ylim(0, 110)
    ax.set_title("Deterministic vs LLM-enabled (slice 62 tasks): does LLM help on combined data?")
    ax.legend()
    for i, (d, l) in enumerate(zip(det_vals, llm_vals)):
        ax.text(i - w/2, d + 1.5, f"{d:.1f}", ha="center", fontsize=8, color="#374151")
        ax.text(i + w/2, l + 1.5, f"{l:.1f}", ha="center", fontsize=8, color="#14532d", fontweight="bold")
        delta = l - d
        c = "#16a34a" if delta > 0.5 else ("#9ca3af" if abs(delta) < 0.5 else "#dc2626")
        ax.text(i, max(d, l) + 7, f"Δ {delta:+.1f}", ha="center", fontsize=9, color=c, fontweight="bold")
    fig.tight_layout()
    out = CHARTS / "24_det_vs_llm.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [
        chart_phase13_vs_combined(),
        chart_per_split(),
        chart_lofo_worst(),
        chart_record_metrics_breakdown(),
        chart_det_vs_llm(),
    ]
    for p in outs:
        if p:
            print(f"chart written: {p}")


if __name__ == "__main__":
    main()
