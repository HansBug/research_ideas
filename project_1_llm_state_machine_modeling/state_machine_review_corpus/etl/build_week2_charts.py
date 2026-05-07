"""Week 2 Q3 self-consistency charts: trade-off visualization."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
PHASE14 = CORPUS_ROOT / "etl" / "out" / "phase14_combined"
WK2 = PHASE14 / "week2"
ABL = PHASE14 / "ablation"
WK15 = PHASE14 / "week15"
CHARTS = CORPUS_ROOT / "etl" / "out" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def _resolve(rep, dotted):
    cur = rep
    for p in dotted.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return float(cur) if isinstance(cur, (int, float)) else None


def _load(p, sub=None):
    if not p.exists():
        return None
    rep = json.loads(p.read_text())
    return rep.get(sub) if sub else rep


# ============================================================================
# Chart 60: Stage 1 — variance source comparison (40-task)
# ============================================================================
def chart_stage1_variance_sources():
    configs = [
        ("v0", ABL / "report_iter_v0.json", "#a78bfa"),
        ("B-only", ABL / "report_iter_b_only.json", "#10b981"),
        ("Q3_temp", WK2 / "report_q3_temp_n3.json", "#3b82f6"),
        ("Q3_para", WK2 / "report_q3_para_n3.json", "#f97316"),
        ("Q3_both", WK2 / "report_q3_both_n3.json", "#dc2626"),
    ]
    metrics = [
        ("HAI", "HAI"),
        ("RAS", "record_metrics.RAS"),
        ("SAS", "summary_metrics.SAS"),
        ("record\nScoreAlign", "record_metrics.ScoreAlign"),
        ("summary\nRankAlign", "summary_metrics.RankAlign"),
        ("Spearman·100", "summary_metrics.spearman_rho"),
        ("kappa·100", "judgement_metrics.weighted_kappa"),
        ("crit_issue\nrecall·100", "critical_issue_metrics.critical_issue_recall"),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(15, 8))
    axes = axes.flatten()
    for ax, (title, dotted) in zip(axes, metrics):
        names, vals, cols = [], [], []
        for label, p, col in configs:
            rep = _load(p)
            if rep is None: continue
            v = _resolve(rep, dotted)
            if v is None: continue
            if "spearman_rho" in dotted or "kappa" in dotted or "recall" in dotted:
                v *= 100
            names.append(label)
            vals.append(v)
            cols.append(col)
        x = np.arange(len(names))
        bars = ax.bar(x, vals, color=cols)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8, rotation=15)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(0, max(vals) * 1.18 if vals else 100)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + max(vals) * 0.02, f"{v:.1f}",
                    ha="center", fontsize=8, fontweight="bold")
    fig.suptitle("Stage 1 (40-task): variance_source 消融 — temp/paraphrase/both 三种几乎完全相同", y=1.00)
    fig.tight_layout()
    out = CHARTS / "60_stage1_variance_sources.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ============================================================================
# Chart 61: Stage 3 — 62-task: full trade-off vs W1.5 baseline
# ============================================================================
def chart_stage3_tradeoff():
    configs = [
        ("Week 0\ndet", PHASE14 / "report_deterministic.json", "slice_report", "#9ca3af"),
        ("Week 0\nLLM-mode", PHASE14 / "report_slice_llm_auto.json", None, "#fbbf24"),
        ("Week 1\nv0 rubric", PHASE14 / "report_slice_rubric_llm.json", None, "#a78bfa"),
        ("Week 1.5\nB-only", WK15 / "report_iter_b_only_62task.json", None, "#10b981"),
        ("Week 2\nQ3 (both)", WK2 / "report_q3_both_n3_62task.json", None, "#dc2626"),
    ]
    metrics = [
        ("HAI", "HAI"),
        ("RAS", "record_metrics.RAS"),
        ("SAS", "summary_metrics.SAS"),
        ("record\nScoreAlign", "record_metrics.ScoreAlign"),
        ("summary\nRankAlign", "summary_metrics.RankAlign"),
        ("Spearman·100", "summary_metrics.spearman_rho"),
        ("kappa·100", "judgement_metrics.weighted_kappa"),
        ("record_Calib", "record_metrics.Calib"),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    axes = axes.flatten()
    for ax, (title, dotted) in zip(axes, metrics):
        names, vals, cols = [], [], []
        for label, p, sub, col in configs:
            rep = _load(p, sub)
            if rep is None: continue
            v = _resolve(rep, dotted)
            if v is None: continue
            if "spearman_rho" in dotted or "kappa" in dotted or "recall" in dotted:
                v *= 100
            names.append(label)
            vals.append(v)
            cols.append(col)
        x = np.arange(len(names))
        bars = ax.bar(x, vals, color=cols)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8, rotation=15)
        ax.set_title(title, fontsize=10)
        ax.set_ylim(0, max(vals) * 1.18 if vals else 100)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + max(vals) * 0.02, f"{v:.1f}",
                    ha="center", fontsize=8, fontweight="bold")
    fig.suptitle("Stage 3 (62-task): Q3 vs all baselines — clean trade-off pattern", y=1.00)
    fig.tight_layout()
    out = CHARTS / "61_stage3_62task_tradeoff.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ============================================================================
# Chart 62: Acceptance gates pass/fail matrix
# ============================================================================
def chart_acceptance_gates():
    configs = [
        ("Week 0 det", PHASE14 / "report_deterministic.json", "slice_report"),
        ("Week 0 LLM", PHASE14 / "report_slice_llm_auto.json", None),
        ("Week 1 v0", PHASE14 / "report_slice_rubric_llm.json", None),
        ("Week 1.5 B-only", WK15 / "report_iter_b_only_62task.json", None),
        ("Week 2 Q3 (both)", WK2 / "report_q3_both_n3_62task.json", None),
    ]
    gates = [
        ("HAI ≥ 85", "HAI", 85.02),
        ("record_SA ≥ 65", "record_metrics.ScoreAlign", 65.0),
        ("summary_SA ≥ 60", "summary_metrics.ScoreAlign", 60.0),
        ("summary_RA ≥ 70", "summary_metrics.RankAlign", 70.0),
        ("Spearman ≥ 0.45", "summary_metrics.spearman_rho", 0.45),
        ("kappa ≥ 0.65", "judgement_metrics.weighted_kappa", 0.65),
        ("crit_issue ≥ 0.90", "critical_issue_metrics.critical_issue_recall", 0.90),
    ]
    matrix = []
    cfgs_present = []
    for label, p, sub in configs:
        rep = _load(p, sub)
        if rep is None: continue
        cfgs_present.append(label)
        row = []
        for _, dotted, t in gates:
            v = _resolve(rep, dotted)
            row.append(1 if (v is not None and v >= t) else 0)
        matrix.append(row)
    arr = np.array(matrix)
    fig, ax = plt.subplots(figsize=(11.5, max(4, len(cfgs_present) * 0.7)))
    im = ax.imshow(arr, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(gates)))
    ax.set_xticklabels([g[0] for g in gates], rotation=20, ha="right", fontsize=9)
    ax.set_yticks(range(len(cfgs_present)))
    ax.set_yticklabels(cfgs_present, fontsize=9)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ch = "✓" if arr[i, j] == 1 else "✗"
            ax.text(j, i, ch, ha="center", va="center", fontsize=14,
                    color="white", fontweight="bold")
    pass_counts = arr.sum(axis=1)
    for i, c in enumerate(pass_counts):
        ax.text(arr.shape[1] - 0.4, i, f"{int(c)}/{arr.shape[1]}",
                ha="left", va="center", fontsize=10, color="#1f2937", fontweight="bold")
    ax.set_title("62-task acceptance gates — Q3 同样 4/7 但不同的 4 个（trade-off 不是 win）")
    fig.tight_layout()
    out = CHARTS / "62_week2_acceptance_gates.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ============================================================================
# Chart 63: Q3 effect — record vs summary regime
# ============================================================================
def chart_regime_split():
    """Show that Q3 helps record but hurts summary regime."""
    b_only = _load(WK15 / "report_iter_b_only_62task.json")
    q3 = _load(WK2 / "report_q3_both_n3_62task.json")
    if not (b_only and q3):
        return None

    record_metrics = [
        ("ScoreAlign", "record_metrics.ScoreAlign"),
        ("issue_f1·100", "record_metrics.issue_f1"),
        ("EquivAlign", "record_metrics.EquivAlign"),
        ("Calib", "record_metrics.Calib"),
    ]
    summary_metrics = [
        ("ScoreAlign", "summary_metrics.ScoreAlign"),
        ("RankAlign", "summary_metrics.RankAlign"),
        ("Spearman·100", "summary_metrics.spearman_rho"),
        ("EvidDisc", "summary_metrics.EvidenceDiscipline"),
    ]

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for ax, (regime_name, metrics) in zip(axes, [("Record regime", record_metrics), ("Summary regime", summary_metrics)]):
        names, b_vals, q_vals, deltas = [], [], [], []
        for mname, dotted in metrics:
            bv = _resolve(b_only, dotted)
            qv = _resolve(q3, dotted)
            if bv is None or qv is None: continue
            if "issue_f1" in dotted or "spearman_rho" in dotted:
                bv *= 100; qv *= 100
            names.append(mname)
            b_vals.append(bv)
            q_vals.append(qv)
            deltas.append(qv - bv)
        x = np.arange(len(names))
        w = 0.4
        ax.bar(x - w/2, b_vals, w, color="#10b981", label="W1.5 B-only")
        ax.bar(x + w/2, q_vals, w, color="#dc2626", label="W2 Q3 (both, N=3)")
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=9)
        ax.set_title(regime_name, fontsize=11)
        ax.set_ylim(0, max(max(b_vals), max(q_vals)) * 1.22)
        for i, (b, q, d) in enumerate(zip(b_vals, q_vals, deltas)):
            color = "#16a34a" if d > 1 else ("#dc2626" if d < -1 else "#9ca3af")
            ax.text(i, max(b, q) + max(max(b_vals), max(q_vals)) * 0.04,
                    f"Δ {d:+.1f}", ha="center", fontsize=9, color=color, fontweight="bold")
        ax.legend(fontsize=8)
    fig.suptitle("Q3 trade-off split by regime: 大胜 record / 大败 summary", y=1.02)
    fig.tight_layout()
    out = CHARTS / "63_week2_regime_split.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ============================================================================
# Chart 64: SC variance signal — disagreement / dim_std
# ============================================================================
def chart_sc_signal():
    """Show that variance signal is small (mean_max_dim_std ~0.024-0.029) → SC has limited room."""
    items = [
        ("Q3_temp_n3", WK2 / "report_q3_temp_n3.json"),
        ("Q3_para_n3", WK2 / "report_q3_para_n3.json"),
        ("Q3_both_n3", WK2 / "report_q3_both_n3.json"),
        ("Q3_both_n3\n(62-task)", WK2 / "report_q3_both_n3_62task.json"),
    ]
    names, dis_counts, dis_total, mean_stds = [], [], [], []
    for label, p in items:
        rep = _load(p)
        if rep is None: continue
        sc = rep.get("self_consistency_summary", {})
        names.append(label)
        dis_counts.append(sc.get("n_disagreement_flag_true", 0))
        dis_total.append(sc.get("n_total_tasks", 0))
        mean_stds.append(sc.get("mean_max_dim_std", 0.0))

    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    x = np.arange(len(names))

    # disagreement_flag rate
    rates = [c/t if t else 0 for c, t in zip(dis_counts, dis_total)]
    bars = axes[0].bar(x, rates, color=["#3b82f6", "#f97316", "#dc2626", "#8b5cf6"])
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(names, fontsize=8, rotation=15)
    axes[0].set_title("disagreement_flag rate (任务级)")
    axes[0].set_ylabel("fraction of tasks with judgement disagreement")
    axes[0].set_ylim(0, max(rates + [0.05]) * 1.5)
    for b, c, t in zip(bars, dis_counts, dis_total):
        axes[0].text(b.get_x() + b.get_width()/2, b.get_height() + 0.01, f"{c}/{t}",
                     ha="center", fontsize=9)

    # mean_max_dim_std
    bars = axes[1].bar(x, mean_stds, color=["#3b82f6", "#f97316", "#dc2626", "#8b5cf6"])
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(names, fontsize=8, rotation=15)
    axes[1].set_title("mean(max_dim_std across tasks) — variance signal")
    axes[1].set_ylim(0, max(mean_stds + [0.05]) * 1.5)
    for b, v in zip(bars, mean_stds):
        axes[1].text(b.get_x() + b.get_width()/2, b.get_height() + 0.001, f"{v:.4f}",
                     ha="center", fontsize=9)

    fig.suptitle("Q3 SC variance signal: 三个 source 在 N=3 几乎相同；62-task 上 std 更小", y=1.02)
    fig.tight_layout()
    out = CHARTS / "64_week2_sc_signal.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ============================================================================
# Chart 65: HAI evolution timeline
# ============================================================================
def chart_hai_timeline():
    """HAI progression Week 0 → Week 1 → Week 1.5 → Week 2."""
    items = [
        ("W0 det\n(973 deterministic full)", 85.02, "#9ca3af", "baseline (no LLM)"),
        ("W0 LLM\n(62-task slice, no rubric)", 80.89, "#fbbf24", "Phase 15 baseline"),
        ("W1 v0\n(rubric, no iter)", 80.51, "#a78bfa", "rubric introduced"),
        ("W1.5 B-only\n(rubric + Iter-B)", 81.76, "#10b981", "current working baseline"),
        ("W2 Q3\n(rubric + Iter-B + SC)", 79.88, "#dc2626", "trade-off"),
    ]
    fig, ax = plt.subplots(figsize=(13, 5))
    x = np.arange(len(items))
    vals = [v for _, v, _, _ in items]
    cols = [c for _, _, c, _ in items]
    bars = ax.bar(x, vals, color=cols)
    ax.axhline(85.02, color="#1f2937", linestyle="--", linewidth=1)
    ax.text(len(items) - 0.5, 85.5, "HAI ≥ 85 acceptance gate", fontsize=8, color="#1f2937")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{name}\n({desc})" for name, _, _, desc in items], fontsize=8)
    ax.set_ylim(75, 88)
    ax.set_ylabel("HAI (post-Tier-A)")
    ax.set_title("HAI 进展 Week 0 → Week 2 — Q3 让 HAI 净跌（trade-off 代价）")
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width()/2, v + 0.2, f"{v:.2f}", ha="center", fontsize=10, fontweight="bold")

    # Highlight key transitions
    for i, ((_, va, _, _), (_, vb, _, _)) in enumerate(zip(items[:-1], items[1:])):
        d = vb - va
        color = "#16a34a" if d > 0 else "#dc2626"
        ax.annotate(f"{d:+.2f}", xy=(i + 0.5, (va + vb) / 2),
                    fontsize=9, color=color, fontweight="bold", ha="center")

    fig.tight_layout()
    out = CHARTS / "65_week2_hai_timeline.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main():
    outs = [
        chart_stage1_variance_sources(),
        chart_stage3_tradeoff(),
        chart_acceptance_gates(),
        chart_regime_split(),
        chart_sc_signal(),
        chart_hai_timeline(),
    ]
    for p in outs:
        if p:
            print(f"chart written: {p}")


if __name__ == "__main__":
    main()
