"""Ablation charts: each Iter's contribution + winner identification."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ABL = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "ablation"
CHARTS = CORPUS_ROOT / "etl" / "out" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})

CONFIGS = [
    "baseline_det",
    "baseline_llm",
    "iter_v0",
    "iter_a_only",
    "iter_b_only",
    "iter_c_only",
    "iter_abc",
]
SHORT_LABELS = {
    "baseline_det": "det\n(no LLM)",
    "baseline_llm": "LLM\n(no rubric)",
    "iter_v0": "v0\nrubric",
    "iter_a_only": "A only\n(asym bounds)",
    "iter_b_only": "B only\n(diff prompt)",
    "iter_c_only": "C only\n(selective)",
    "iter_abc": "A+B+C\n(combined)",
}
COLORS = {
    "baseline_det": "#9ca3af",
    "baseline_llm": "#fbbf24",
    "iter_v0": "#a78bfa",
    "iter_a_only": "#3b82f6",
    "iter_b_only": "#f97316",
    "iter_c_only": "#10b981",
    "iter_abc": "#dc2626",
}


def _resolve(report: dict, dotted: str) -> float | None:
    cur = report
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return float(cur) if isinstance(cur, (int, float)) else None


def load_all() -> dict[str, dict]:
    out = {}
    for label in CONFIGS:
        p = ABL / f"report_{label}.json"
        if p.exists():
            try:
                out[label] = json.loads(p.read_text())
            except Exception:
                pass
    return out


def chart_headline_grid() -> Path:
    """6 metrics × all configs."""
    reports = load_all()
    if len(reports) < 3:
        return Path()
    metrics = [
        ("HAI", "HAI", 100),
        ("RAS", "record_metrics.RAS", 100),
        ("SAS", "summary_metrics.SAS", 100),
        ("record\nScoreAlign", "record_metrics.ScoreAlign", 100),
        ("summary\nRankAlign", "summary_metrics.RankAlign", 100),
        ("summary\nSpearman·100", "summary_metrics.spearman_rho", 100),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    for ax, (mname, dotted, ymax) in zip(axes, metrics):
        names = []
        vals = []
        cols = []
        for label in CONFIGS:
            if label not in reports:
                continue
            v = _resolve(reports[label], dotted)
            if v is None:
                continue
            if "Spearman" in mname:
                v = v * 100
            names.append(SHORT_LABELS[label])
            vals.append(v)
            cols.append(COLORS[label])
        x = np.arange(len(names))
        bars = ax.bar(x, vals, color=cols)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8, rotation=0)
        ax.set_title(mname, fontsize=11)
        ax.set_ylim(0, max(ymax, max(vals) * 1.1) if vals else ymax)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=8)
    fig.suptitle("Ablation grid: 7 configs × 6 key metrics (slice 40 task)", fontsize=12, y=1.00)
    fig.tight_layout()
    out = CHARTS / "40_ablation_headline_grid.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_iter_contribution() -> Path:
    """Bar chart: contribution of each Iter A/B/C vs v0 baseline."""
    reports = load_all()
    if "iter_v0" not in reports:
        return Path()
    base = reports["iter_v0"]

    metrics = [
        ("HAI", "HAI"),
        ("summary\nRankAlign", "summary_metrics.RankAlign"),
        ("summary\nSpearman·100", "summary_metrics.spearman_rho"),
        ("record\nScoreAlign", "record_metrics.ScoreAlign"),
        ("crit_issue\nrecall·100", "critical_issue_metrics.critical_issue_recall"),
        ("weighted\nkappa·100", "judgement_metrics.weighted_kappa"),
    ]
    iter_configs = ["iter_a_only", "iter_b_only", "iter_c_only", "iter_abc"]
    fig, ax = plt.subplots(figsize=(13, 5.2))
    x = np.arange(len(metrics))
    w = 0.20
    offsets = [-1.5*w, -0.5*w, 0.5*w, 1.5*w]
    for cfg, off in zip(iter_configs, offsets):
        if cfg not in reports:
            continue
        deltas = []
        for _, dotted in metrics:
            base_v = _resolve(base, dotted)
            cfg_v = _resolve(reports[cfg], dotted)
            if base_v is None or cfg_v is None:
                deltas.append(0)
                continue
            mult = 100 if any(k in dotted for k in ("spearman_rho", "macro_f1", "weighted_kappa", "critical_issue_recall", "issue_f1")) else 1
            deltas.append((cfg_v - base_v) * mult)
        bars = ax.bar(x + off, deltas, w, color=COLORS[cfg], label=SHORT_LABELS[cfg].replace("\n", " "))
        for b, v in zip(bars, deltas):
            color = "#16a34a" if v > 0 else "#dc2626" if v < -0.5 else "#9ca3af"
            ax.text(b.get_x() + b.get_width()/2, v + (1 if v >= 0 else -3),
                    f"{v:+.1f}", ha="center", fontsize=7, color=color, fontweight="bold")
    ax.axhline(0, color="black", linewidth=0.7)
    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in metrics], fontsize=9)
    ax.set_ylabel("Δ vs iter_v0 (rubric without iter)")
    ax.set_title("Per-iter contribution decomposition: A / B / C / A+B+C vs rubric_v0")
    ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    out = CHARTS / "41_iter_contribution.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_acceptance_passrate() -> Path:
    """Pass/fail per config across the 7 acceptance gates."""
    reports = load_all()
    gates = [
        ("HAI ≥ 85", "HAI", 85.02),
        ("record SA ≥ 65", "record_metrics.ScoreAlign", 65),
        ("summary SA ≥ 60", "summary_metrics.ScoreAlign", 60),
        ("summary RA ≥ 70", "summary_metrics.RankAlign", 70),
        ("Spearman·100 ≥ 45", "summary_metrics.spearman_rho", 0.45),
        ("kappa·100 ≥ 65", "judgement_metrics.weighted_kappa", 0.65),
        ("crit_issue·100 ≥ 90", "critical_issue_metrics.critical_issue_recall", 0.90),
    ]

    matrix = []
    cfgs_present = [c for c in CONFIGS if c in reports]
    for cfg in cfgs_present:
        row = []
        for _, dotted, t in gates:
            v = _resolve(reports[cfg], dotted)
            if v is None:
                row.append(0)
            else:
                row.append(1 if v >= t else 0)
        matrix.append(row)
    if not matrix:
        return Path()

    fig, ax = plt.subplots(figsize=(11, max(3.5, len(cfgs_present) * 0.6)))
    arr = np.array(matrix)
    im = ax.imshow(arr, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(gates)))
    ax.set_xticklabels([g[0] for g in gates], rotation=20, ha="right", fontsize=9)
    ax.set_yticks(range(len(cfgs_present)))
    ax.set_yticklabels([SHORT_LABELS[c].replace("\n", " ") for c in cfgs_present], fontsize=9)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            ch = "✓" if arr[i, j] == 1 else "✗"
            ax.text(j, i, ch, ha="center", va="center", fontsize=14,
                    color="white", fontweight="bold")
    pass_counts = arr.sum(axis=1)
    for i, c in enumerate(pass_counts):
        ax.text(arr.shape[1] - 0.4, i, f"{int(c)}/{arr.shape[1]}",
                ha="left", va="center", fontsize=10, color="#1f2937", fontweight="bold")
    ax.set_title("Acceptance gate pass/fail matrix")
    fig.tight_layout()
    out = CHARTS / "42_acceptance_passrate.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_runtime_cost() -> Path:
    """Runtime cost (tokens, latency) per config."""
    reports = load_all()
    if not reports:
        return Path()
    cfgs = [c for c in CONFIGS if c in reports]
    tokens = []
    lat = []
    labels = []
    for c in cfgs:
        rt = reports[c].get("runtime_metrics", {})
        tokens.append(float(rt.get("llm_total_tokens", 0)))
        lat.append(float(rt.get("latency_p95", 0)))
        labels.append(SHORT_LABELS[c].replace("\n", " "))
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))
    for ax, vals, name, color_map in [
        (axes[0], tokens, "LLM total tokens", "#3b82f6"),
        (axes[1], lat, "latency_p95 (s)", "#f97316"),
    ]:
        bars = ax.bar(np.arange(len(labels)), vals, color=[COLORS[c] for c in cfgs])
        ax.set_xticks(np.arange(len(labels)))
        ax.set_xticklabels(labels, rotation=20, ha="right", fontsize=8)
        ax.set_title(name)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v * 1.02,
                    f"{int(v):,}" if name.startswith("LLM") else f"{v:.0f}",
                    ha="center", fontsize=8)
    fig.suptitle("Runtime cost across configs", y=1.02)
    fig.tight_layout()
    out = CHARTS / "43_runtime_cost.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [
        chart_headline_grid(),
        chart_iter_contribution(),
        chart_acceptance_passrate(),
        chart_runtime_cost(),
    ]
    for p in outs:
        if p:
            print(f"chart written: {p}")
        else:
            print("chart skipped (insufficient data)")


if __name__ == "__main__":
    main()
