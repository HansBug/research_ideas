"""V4 verify charts: 5 reps default-config airouter strict-llm vs W3 N1 miaocg-baseline."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
SUMMARY = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "migration_verify" / "default_verify_v4_summary.json"
CHARTS = CORPUS_ROOT / "etl" / "out" / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)


def _resolve_cjk_font() -> str:
    candidates = ["Noto Sans CJK SC", "Noto Sans CJK JP", "Noto Sans CJK HK",
                  "WenQuanYi Zen Hei", "WenQuanYi Micro Hei",
                  "Source Han Sans SC", "Microsoft YaHei", "SimHei", "AR PL UMing CN"]
    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in candidates:
        if name in available:
            return name
    for ttc in ("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",):
        if Path(ttc).exists():
            font_manager.fontManager.addfont(ttc)
            return font_manager.FontProperties(fname=ttc).get_name()
    return "DejaVu Sans"


_CJK = _resolve_cjk_font()
plt.rcParams.update({
    "figure.dpi": 130, "savefig.dpi": 140,
    "axes.spines.top": False, "axes.spines.right": False,
    "font.size": 10, "font.family": "sans-serif",
    "font.sans-serif": [_CJK, "DejaVu Sans", "Arial", "sans-serif"],
    "axes.unicode_minus": False,
})

V4_COLOR = "#dc2626"
W3_COLOR = "#2563eb"


def chart_90_metric_grid(summary: dict, out: Path):
    metrics = ["HAI", "RAS", "SAS",
               "record_ScoreAlign", "record_Calib", "record_ReasonAlign",
               "summary_ScoreAlign", "summary_RankAlign", "summary_Spearman",
               "summary_EvDisc", "weighted_kappa", "record_EquivAlign"]
    v4 = summary["v4_default_strict_5reps"]
    w3 = summary["w3_n1_baseline_5reps"]
    fig, axes = plt.subplots(3, 4, figsize=(16, 10))
    for ax, m in zip(axes.flat, metrics):
        n = v4.get(m, {})
        w = w3.get(m, {})
        if not n or not w:
            ax.set_visible(False); continue
        x = np.array([0, 1])
        means = [n["mean"], w["mean"]]
        stds = [n["std"], w["std"]]
        colors = [V4_COLOR, W3_COLOR]
        ax.bar(x, means, yerr=stds, color=colors, capsize=5, alpha=0.85, edgecolor="black", linewidth=0.5)
        for i, (mean, std) in enumerate(zip(means, stds)):
            ax.text(i, mean + std + 0.5, f"{mean:.2f}\n±{std:.2f}",
                    ha="center", fontsize=8, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(["V4\nairouter strict\n(5 reps)", "W3 N1\nmiaocg no-strict\n(5 reps)"], fontsize=7)
        ax.set_title(m, fontsize=10, fontweight="bold")
        ax.tick_params(axis="y", labelsize=8)
        delta = means[0] - means[1]
        denom = max(stds[1], 0.001)
        z = delta / denom
        within = abs(z) <= 2
        text_color = "#16a34a" if within else "#dc2626"
        ax.text(0.5, 1.05, f"ΔMean={delta:+.2f}, |Z|={abs(z):.1f}σ_W3 {'✓' if within else '×'}",
                ha="center", transform=ax.transAxes, fontsize=8, color=text_color, fontweight="bold")
    fig.suptitle("V4 默认配置 5-rep verification (airouter + strict-llm + retries=8 + max_workers=12) vs W3 N1 baseline",
                 fontsize=12, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_91_per_rep_dots(summary: dict, out: Path):
    cores = ["HAI", "RAS", "SAS",
             "summary_ScoreAlign", "summary_RankAlign", "summary_Spearman",
             "weighted_kappa", "record_Calib"]
    v4 = summary["v4_default_strict_5reps"]
    w3 = summary["w3_n1_baseline_5reps"]
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    for ax, m in zip(axes.flat, cores):
        n = v4.get(m, {}); w = w3.get(m, {})
        if not n or not w:
            ax.set_visible(False); continue
        v4_vals = n.get("values", [])
        w3_vals = w.get("values", [])
        ax.scatter([0]*len(v4_vals), v4_vals, color=V4_COLOR, s=110, alpha=0.7,
                   label="V4 (5 reps)", edgecolors="black", linewidths=0.5)
        ax.scatter([1]*len(w3_vals), w3_vals, color=W3_COLOR, s=110, alpha=0.7,
                   label="W3 N1 (5 reps)", edgecolors="black", linewidths=0.5)
        ax.hlines([n["mean"]], -0.2, 0.2, color=V4_COLOR, linewidth=2.5)
        ax.hlines([w["mean"]], 0.8, 1.2, color=W3_COLOR, linewidth=2.5)
        ax.fill_between([-0.2, 0.2], n["mean"]-n["std"], n["mean"]+n["std"],
                        color=V4_COLOR, alpha=0.15)
        ax.fill_between([0.8, 1.2], w["mean"]-w["std"], w["mean"]+w["std"],
                        color=W3_COLOR, alpha=0.15)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["V4", "W3 N1"], fontsize=10)
        ax.set_title(m, fontsize=11, fontweight="bold")
        ax.set_ylabel("value", fontsize=9)
        if m == "HAI":
            ax.legend(fontsize=8, loc="lower right")
        ax.grid(True, alpha=0.3, linestyle=":")
    fig.suptitle("Per-rep distribution (5 reps each) — V4 strict-llm 真 LLM vs W3 N1 miaocg cache-hit",
                 fontsize=12, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_92_significance(summary: dict, out: Path):
    metrics = list(summary["v4_default_strict_5reps"].keys())
    v4 = summary["v4_default_strict_5reps"]
    w3 = summary["w3_n1_baseline_5reps"]
    z_scores = []
    annotations = []
    for m in metrics:
        n = v4.get(m, {}); w = w3.get(m, {})
        if not n or not w or w.get("std", 0) == 0:
            z_scores.append(0); annotations.append("σ=0"); continue
        z = (n["mean"] - w["mean"]) / w["std"]
        z_scores.append(abs(z))
        annotations.append(f"{z:+.1f}σ")
    fig, ax = plt.subplots(figsize=(13, 5))
    arr = np.array(z_scores).reshape(1, -1)
    cmap = plt.cm.RdYlGn_r
    im = ax.imshow(arr, cmap=cmap, vmin=0, vmax=4, aspect="auto")
    for j, (z, ann) in enumerate(zip(z_scores, annotations)):
        color = "white" if z > 2 else "#1f2937"
        ax.text(j, 0, ann, ha="center", va="center", fontsize=9, color=color, fontweight="bold")
    ax.set_xticks(range(len(metrics)))
    ax.set_xticklabels(metrics, rotation=25, ha="right", fontsize=8)
    ax.set_yticks([0]); ax.set_yticklabels(["V4 vs W3 N1"], fontsize=10, fontweight="bold")
    ax.set_title("V4 默认配置 vs W3 N1 baseline — Δmean / σ_W3 (|Z|>2 红格 = 显著差异)",
                 fontsize=11, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.05)
    cbar.set_label("|Z-score|", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def main() -> None:
    if not SUMMARY.exists():
        raise SystemExit(f"missing {SUMMARY}; run analyze_default_verify_v4 first")
    summary = json.loads(SUMMARY.read_text())
    chart_90_metric_grid(summary, CHARTS / "90_v4_metric_grid.png")
    chart_91_per_rep_dots(summary, CHARTS / "91_v4_per_rep_dots.png")
    chart_92_significance(summary, CHARTS / "92_v4_significance.png")


if __name__ == "__main__":
    main()
