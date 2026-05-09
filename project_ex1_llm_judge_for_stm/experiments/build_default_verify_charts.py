"""Charts for default-config verification: NEW (project_ex1) vs W3 N1 baseline.

Reads:
  experiments/out/phase14_combined/migration_verify/default_verify_summary.json

Outputs in etl/out/charts/:
  80_default_verify_metric_grid.png       — 12 key metrics × 2 sources side-by-side
  81_default_verify_significance.png      — |Δ| / σ_W3 heatmap
  82_default_verify_distributions.png     — per-rep dot plot for HAI/RAS/SAS/kappa
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
SUMMARY = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "migration_verify" / "default_verify_summary.json"
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

NEW_COLOR = "#dc2626"   # red
W3_COLOR = "#2563eb"    # blue


def chart_80_metric_grid(summary: dict, out: Path):
    metrics = ["HAI", "RAS", "SAS",
               "record_ScoreAlign", "record_Calib", "record_ReasonAlign",
               "summary_ScoreAlign", "summary_RankAlign", "summary_Spearman",
               "summary_EvDisc", "weighted_kappa", "record_EquivAlign"]
    new_data = summary["new_default_config_5reps"]
    w3_data = summary["w3_n1_baseline_5reps"]
    fig, axes = plt.subplots(3, 4, figsize=(15, 9))
    for ax, m in zip(axes.flat, metrics):
        n = new_data.get(m, {})
        w = w3_data.get(m, {})
        if not n or not w:
            ax.set_visible(False)
            continue
        x = np.array([0, 1])
        means = [n["mean"], w["mean"]]
        stds = [n["std"], w["std"]]
        colors = [NEW_COLOR, W3_COLOR]
        ax.bar(x, means, yerr=stds, color=colors, capsize=5, alpha=0.85, edgecolor="black", linewidth=0.5)
        for i, (mean, std) in enumerate(zip(means, stds)):
            ax.text(i, mean + std + 0.5, f"{mean:.2f}\n±{std:.2f}",
                    ha="center", fontsize=8, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(["NEW\n(project_ex1\ndefault)", "W3 N1\n(PR #6\nbaseline)"], fontsize=8)
        ax.set_title(m, fontsize=10, fontweight="bold")
        ax.tick_params(axis="y", labelsize=8)
        delta = means[0] - means[1]
        denom = max(stds[1], 0.001)
        z = delta / denom
        within = abs(z) <= 2
        text_color = "#16a34a" if within else "#dc2626"
        ax.text(0.5, 1.05, f"Δ={delta:+.2f}, |Z|={abs(z):.1f}σ_W3 {'✓' if within else '✗'}",
                ha="center", transform=ax.transAxes, fontsize=8, color=text_color, fontweight="bold")
    fig.suptitle("Default config verification — NEW (project_ex1, rubric+iter_b 默认 ON) vs W3 N1 baseline (rubric+iter_b 显式)",
                 fontsize=12, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_81_significance(summary: dict, out: Path):
    metrics = list(summary["new_default_config_5reps"].keys())
    new_data = summary["new_default_config_5reps"]
    w3_data = summary["w3_n1_baseline_5reps"]
    z_scores = []
    annotations = []
    for m in metrics:
        n = new_data.get(m, {})
        w = w3_data.get(m, {})
        if not n or not w or w.get("std", 0) == 0:
            z_scores.append(0)
            annotations.append("σ=0")
            continue
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
    ax.set_yticks([0]); ax.set_yticklabels(["NEW vs W3 N1"], fontsize=10, fontweight="bold")
    ax.set_title("默认配置迁移验证：NEW 5-rep mean 离 W3 N1 5-rep mean 的 Z-score（按 W3 N1 σ 度量；|Z|>2 红格 = 漂出 95% 区间）",
                 fontsize=10, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.05)
    cbar.set_label("|Z-score|", fontsize=9)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_82_distributions(summary: dict, out: Path):
    cores = ["HAI", "RAS", "SAS", "weighted_kappa"]
    new_data = summary["new_default_config_5reps"]
    w3_data = summary["w3_n1_baseline_5reps"]
    fig, axes = plt.subplots(1, 4, figsize=(15, 4.5))
    for ax, m in zip(axes, cores):
        n = new_data.get(m, {})
        w = w3_data.get(m, {})
        if not n or not w:
            ax.set_visible(False); continue
        new_vals = n.get("values", [])
        w3_vals = w.get("values", [])
        # Dot plot
        ax.scatter([0]*len(new_vals), new_vals, color=NEW_COLOR, s=80, alpha=0.7, label="NEW (project_ex1)", edgecolors="black", linewidths=0.5)
        ax.scatter([1]*len(w3_vals), w3_vals, color=W3_COLOR, s=80, alpha=0.7, label="W3 N1 (PR #6)", edgecolors="black", linewidths=0.5)
        # Mean line
        ax.hlines([n["mean"]], -0.2, 0.2, color=NEW_COLOR, linewidth=2)
        ax.hlines([w["mean"]], 0.8, 1.2, color=W3_COLOR, linewidth=2)
        # ±σ band
        ax.fill_between([-0.2, 0.2], n["mean"]-n["std"], n["mean"]+n["std"], color=NEW_COLOR, alpha=0.15)
        ax.fill_between([0.8, 1.2], w["mean"]-w["std"], w["mean"]+w["std"], color=W3_COLOR, alpha=0.15)
        ax.set_xticks([0, 1]); ax.set_xticklabels(["NEW", "W3 N1"], fontsize=10)
        ax.set_title(m, fontsize=11, fontweight="bold")
        ax.set_ylabel("value", fontsize=9)
        if m == "HAI":
            ax.legend(fontsize=8, loc="lower right")
        ax.grid(True, alpha=0.3, linestyle=":")
    fig.suptitle("Per-rep distribution (5 reps each)：默认配置 NEW vs W3 N1 baseline 横向对比",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def main() -> None:
    if not SUMMARY.exists():
        raise SystemExit(f"missing {SUMMARY}; run analyze_default_verify first")
    summary = json.loads(SUMMARY.read_text())
    chart_80_metric_grid(summary, CHARTS / "80_default_verify_metric_grid.png")
    chart_81_significance(summary, CHARTS / "81_default_verify_significance.png")
    chart_82_distributions(summary, CHARTS / "82_default_verify_distributions.png")


if __name__ == "__main__":
    main()
