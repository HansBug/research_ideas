"""Charts for Week 3 noise-floor experiment results.

Reads:
  etl/out/phase14_combined/week3_noise/noise_summary.json
  etl/out/phase14_combined/week3_noise/noise_per_task_variance.json

Produces 6 charts in etl/out/charts/:
  70_noise_hai_distribution.png      — HAI ±σ for all 4 configs vs historical single-shots
  71_noise_metric_grid.png           — 9 key metrics × 4 configs ±σ
  72_noise_per_task_variance.png     — score_std per task, broken down by config & bucket
  73_noise_n1_vs_n2_comparison.png   — N1 (standard) vs N2 (SC-N1) head-to-head, all metrics
  74_noise_significance_check.png    — historical single-shot vs new dist (Z-score map)
  75_noise_high_var_tasks.png        — top-K most volatile tasks per config

Run:
  python project_ex1_llm_judge_for_stm/experiments/build_noise_floor_charts.py
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
OUT_NOISE = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "week3_noise"
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

CFG_COLORS = {
    "N1_W1.5_B-only": "#2563eb",
    "N2_SC-N1_T0_V1": "#dc2626",
    "N3_W0_LLM-auto": "#16a34a",
    "N4_W1_rubric-v0": "#ca8a04",
}
CFG_LABELS = {
    "N1_W1.5_B-only": "N1: W1.5 B-only\n(标准 runner)",
    "N2_SC-N1_T0_V1": "N2: SC-N1\n(T=0+V1, SC pipeline)",
    "N3_W0_LLM-auto": "N3: W0\n(LLM-auto baseline)",
    "N4_W1_rubric-v0": "N4: W1\n(rubric v0)",
}


def chart_70_hai_distribution(summary: dict, out: Path):
    fig, ax = plt.subplots(figsize=(10, 5.5))
    cfgs = list(summary.keys())
    x = np.arange(len(cfgs))
    means = [summary[c]["metrics"]["HAI"]["mean"] for c in cfgs]
    stds = [summary[c]["metrics"]["HAI"]["std"] for c in cfgs]
    colors = [CFG_COLORS[c] for c in cfgs]
    bars = ax.bar(x, means, yerr=stds, color=colors, capsize=6, alpha=0.85, edgecolor="black", linewidth=0.6)
    for c, m, s in zip(cfgs, means, stds):
        idx = cfgs.index(c)
        ax.text(idx, m + s + 0.5, f"{m:.2f}\n±{s:.2f}", ha="center", fontsize=9, fontweight="bold")
        hist = summary[c]["metrics"]["HAI"].get("historical_single_shot")
        if hist is not None:
            ax.scatter([idx], [hist], color="red", marker="*", s=180, zorder=5,
                       label="历史 single-shot" if idx == 0 else None)
            ax.text(idx + 0.18, hist, f"{hist:.2f}", color="red", fontsize=9, va="center")
    ax.axhline(85.02, ls="--", color="gray", alpha=0.5)
    ax.text(len(cfgs)-0.5, 85.5, "HAI ≥ 85 acceptance gate", fontsize=8, color="gray")
    ax.set_xticks(x); ax.set_xticklabels([CFG_LABELS[c] for c in cfgs], fontsize=8)
    ax.set_ylabel("HAI", fontsize=11)
    ax.set_title("Week 3 Noise Floor：4 个配置 HAI 分布（5 reps，mean ± std）", fontsize=11, fontweight="bold")
    ax.set_ylim(70, 92)
    if any(summary[c]["metrics"]["HAI"].get("historical_single_shot") is not None for c in cfgs):
        ax.legend(loc="lower right", fontsize=8)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_71_metric_grid(summary: dict, out: Path):
    metrics = ["HAI", "RAS", "SAS", "record_ScoreAlign", "summary_ScoreAlign",
               "summary_RankAlign", "summary_Spearman", "weighted_kappa", "record_Calib"]
    cfgs = list(summary.keys())
    fig, axes = plt.subplots(3, 3, figsize=(13, 10))
    for ax, m_label in zip(axes.flat, metrics):
        x = np.arange(len(cfgs))
        means = [summary[c]["metrics"].get(m_label, {}).get("mean", 0) for c in cfgs]
        stds = [summary[c]["metrics"].get(m_label, {}).get("std", 0) for c in cfgs]
        colors = [CFG_COLORS[c] for c in cfgs]
        ax.bar(x, means, yerr=stds, color=colors, capsize=4, alpha=0.85, edgecolor="black", linewidth=0.5)
        for i, (m, s) in enumerate(zip(means, stds)):
            ax.text(i, m + s + (max(means) - min(means)) * 0.03 + 0.05,
                    f"{m:.2f}\n±{s:.2f}", ha="center", fontsize=7)
        ax.set_xticks(x)
        ax.set_xticklabels([c.split("_")[0] for c in cfgs], fontsize=8)
        ax.set_title(m_label, fontsize=10, fontweight="bold")
        ax.tick_params(axis="y", labelsize=8)
    fig.suptitle("Week 3 Noise Floor：9 个核心 metric × 4 个配置（5 reps，mean ± std）",
                 fontsize=12, fontweight="bold", y=1.00)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_72_per_task_variance(per_task: dict, out: Path):
    cfgs = list(per_task.keys())
    fig, axes = plt.subplots(1, len(cfgs), figsize=(4 * len(cfgs), 4.5), sharey=True)
    if len(cfgs) == 1:
        axes = [axes]
    bucket_colors = {"record": "#2563eb", "summary": "#dc2626", "component": "#16a34a", "protocol": "#ca8a04"}
    for ax, cfg in zip(axes, cfgs):
        tasks = per_task[cfg]
        by_bucket: dict[str, list[float]] = {}
        for tid, info in tasks.items():
            by_bucket.setdefault(info["bucket"], []).append(info["score_std"])
        positions = list(range(len(by_bucket)))
        labels = list(by_bucket.keys())
        data = [by_bucket[b] for b in labels]
        bp = ax.boxplot(data, positions=positions, widths=0.6, patch_artist=True, showfliers=True,
                        flierprops=dict(marker="o", markersize=3, alpha=0.5))
        for patch, lbl in zip(bp["boxes"], labels):
            patch.set_facecolor(bucket_colors.get(lbl, "#6b7280"))
            patch.set_alpha(0.6)
        ax.set_xticks(positions); ax.set_xticklabels(labels, fontsize=9, rotation=15)
        ax.set_title(cfg, fontsize=10, fontweight="bold")
        ax.set_ylabel("agent_score std (5 reps)", fontsize=9)
        ax.grid(True, alpha=0.3, linestyle=":")
    fig.suptitle("Week 3 Noise Floor：每 task 跨 5 reps 的 agent_score 噪声分布（按 regime 分组）",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_73_n1_vs_n2(summary: dict, out: Path):
    if "N1_W1.5_B-only" not in summary or "N2_SC-N1_T0_V1" not in summary:
        return
    metrics = ["HAI", "RAS", "SAS", "record_ScoreAlign", "summary_ScoreAlign",
               "summary_RankAlign", "summary_Spearman", "summary_EvDisc",
               "weighted_kappa", "record_Calib"]
    n1 = summary["N1_W1.5_B-only"]["metrics"]
    n2 = summary["N2_SC-N1_T0_V1"]["metrics"]
    fig, ax = plt.subplots(figsize=(13, 6))
    x = np.arange(len(metrics))
    width = 0.4
    n1_means = [n1.get(m, {}).get("mean", 0) for m in metrics]
    n1_stds = [n1.get(m, {}).get("std", 0) for m in metrics]
    n2_means = [n2.get(m, {}).get("mean", 0) for m in metrics]
    n2_stds = [n2.get(m, {}).get("std", 0) for m in metrics]
    ax.bar(x - width/2, n1_means, width, yerr=n1_stds, label="N1: 标准 runner", color="#2563eb", capsize=4, alpha=0.85)
    ax.bar(x + width/2, n2_means, width, yerr=n2_stds, label="N2: SC pipeline", color="#dc2626", capsize=4, alpha=0.85)
    for i, (m1, s1, m2, s2) in enumerate(zip(n1_means, n1_stds, n2_means, n2_stds)):
        delta = m2 - m1
        denom = max(s1, s2, 0.01)
        sigmas = abs(delta) / denom
        if sigmas >= 2:
            ax.annotate(f"Δ={delta:+.2f}\n({sigmas:.1f}σ)", xy=(i, max(m1+s1, m2+s2) + 1.5),
                        ha="center", fontsize=8, color="red", fontweight="bold")
        else:
            ax.annotate(f"Δ={delta:+.2f}", xy=(i, max(m1+s1, m2+s2) + 1.5),
                        ha="center", fontsize=8, color="gray")
    ax.set_xticks(x); ax.set_xticklabels(metrics, rotation=20, ha="right", fontsize=9)
    ax.set_title("Week 3：N1（标准 pipeline）vs N2（SC pipeline N=1，同名义配置）— 测代码路径差异",
                 fontsize=11, fontweight="bold")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.3, linestyle=":", axis="y")
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_74_significance_check(summary: dict, out: Path):
    metrics_to_check = ["HAI", "RAS", "SAS", "record_ScoreAlign", "summary_ScoreAlign",
                        "summary_RankAlign", "summary_Spearman", "weighted_kappa", "record_Calib"]
    cfgs = list(summary.keys())
    grid = np.full((len(cfgs), len(metrics_to_check)), np.nan)
    annotations = [["" for _ in metrics_to_check] for _ in cfgs]
    for i, c in enumerate(cfgs):
        for j, m in enumerate(metrics_to_check):
            entry = summary[c]["metrics"].get(m, {})
            if "historical_z_score" in entry:
                z = entry["historical_z_score"]
                grid[i, j] = z
                annotations[i][j] = f"{z:+.1f}σ"
    fig, ax = plt.subplots(figsize=(13, 5))
    cmap = plt.cm.RdYlGn_r
    im = ax.imshow(np.abs(grid), cmap=cmap, vmin=0, vmax=4, aspect="auto")
    for i in range(len(cfgs)):
        for j in range(len(metrics_to_check)):
            if not np.isnan(grid[i, j]):
                color = "white" if abs(grid[i, j]) > 2 else "#1f2937"
                ax.text(j, i, annotations[i][j], ha="center", va="center", fontsize=9, color=color, fontweight="bold")
            else:
                ax.text(j, i, "—", ha="center", va="center", fontsize=10, color="#9ca3af")
    ax.set_xticks(range(len(metrics_to_check)))
    ax.set_xticklabels(metrics_to_check, rotation=20, ha="right", fontsize=9)
    ax.set_yticks(range(len(cfgs)))
    ax.set_yticklabels([CFG_LABELS[c] for c in cfgs], fontsize=8)
    ax.set_title("Week 3：历史 single-shot vs 新分布 Z-score 表（|Z|>2 = 落在分布尾部，红字=可疑非典型）",
                 fontsize=11, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025)
    cbar.set_label("|Z-score|", fontsize=9)
    cbar.ax.tick_params(labelsize=8)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def chart_75_high_var_tasks(per_task: dict, out: Path, top_k: int = 8):
    cfgs = list(per_task.keys())
    fig, axes = plt.subplots(1, len(cfgs), figsize=(5.5 * len(cfgs), 5.5), sharex=False)
    if len(cfgs) == 1:
        axes = [axes]
    for ax, cfg in zip(axes, cfgs):
        tasks = per_task[cfg]
        ranked = sorted(tasks.items(), key=lambda kv: kv[1]["score_std"], reverse=True)[:top_k]
        names = [tid[:35] + ("…" if len(tid) > 35 else "") for tid, _ in ranked]
        stds = [info["score_std"] for _, info in ranked]
        ranges = [info["score_range"] for _, info in ranked]
        buckets = [info["bucket"] for _, info in ranked]
        bucket_colors = {"record": "#2563eb", "summary": "#dc2626", "component": "#16a34a", "protocol": "#ca8a04"}
        colors = [bucket_colors.get(b, "#6b7280") for b in buckets]
        y = np.arange(len(ranked))
        ax.barh(y, stds, color=colors, alpha=0.85)
        for i, (s, r) in enumerate(zip(stds, ranges)):
            ax.text(s + max(stds) * 0.02, i, f"std={s:.3f} (range={r:.3f})", fontsize=7, va="center")
        ax.set_yticks(y); ax.set_yticklabels(names, fontsize=7)
        ax.invert_yaxis()
        ax.set_title(f"{cfg} — top {top_k} 高噪声 task", fontsize=10, fontweight="bold")
        ax.set_xlabel("agent_score std (5 reps)", fontsize=9)
        ax.grid(True, alpha=0.3, linestyle=":", axis="x")
    fig.suptitle("Week 3：每个配置 top-K 高 score-noise task（颜色=regime）",
                 fontsize=11, fontweight="bold", y=1.02)
    fig.tight_layout()
    fig.savefig(out, bbox_inches="tight")
    print(f"chart written: {out}")


def main() -> None:
    summary_path = OUT_NOISE / "noise_summary.json"
    per_task_path = OUT_NOISE / "noise_per_task_variance.json"
    if not summary_path.exists():
        raise SystemExit(f"missing {summary_path}; run analyze_noise_floor first")
    summary = json.loads(summary_path.read_text())
    per_task = json.loads(per_task_path.read_text()) if per_task_path.exists() else {}

    chart_70_hai_distribution(summary, CHARTS / "70_noise_hai_distribution.png")
    chart_71_metric_grid(summary, CHARTS / "71_noise_metric_grid.png")
    if per_task:
        chart_72_per_task_variance(per_task, CHARTS / "72_noise_per_task_variance.png")
        chart_75_high_var_tasks(per_task, CHARTS / "75_noise_high_var_tasks.png")
    chart_73_n1_vs_n2(summary, CHARTS / "73_noise_n1_vs_n2_comparison.png")
    chart_74_significance_check(summary, CHARTS / "74_noise_significance_check.png")


if __name__ == "__main__":
    main()
