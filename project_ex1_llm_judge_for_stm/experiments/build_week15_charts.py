"""Week 1.5 comprehensive ablation charts: A×B grid + 62-task validation."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
PHASE14 = CORPUS_ROOT / "etl" / "out" / "phase14_combined"
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


def _resolve(report: dict, dotted: str) -> float | None:
    cur = report
    for part in dotted.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return float(cur) if isinstance(cur, (int, float)) else None


def _load(path: Path, sub_key: str | None = None) -> dict | None:
    if not path.exists():
        return None
    try:
        rep = json.loads(path.read_text())
        return rep.get(sub_key) if sub_key else rep
    except Exception:
        return None


def chart_2x2_ab_grid() -> Path:
    """A×B 2x2 grid heatmap on key metrics."""
    rep_v0 = _load(ABL / "report_iter_v0.json")
    rep_a = _load(ABL / "report_iter_a_only.json")
    rep_b = _load(ABL / "report_iter_b_only.json")
    rep_ab = _load(ABL / "report_iter_a_b.json")
    if not all((rep_v0, rep_a, rep_b, rep_ab)):
        return Path()

    metrics = [
        ("HAI", "HAI"),
        ("RAS", "record_metrics.RAS"),
        ("SAS", "summary_metrics.SAS"),
        ("record\nScoreAlign", "record_metrics.ScoreAlign"),
        ("summary\nRankAlign", "summary_metrics.RankAlign"),
        ("summary\nSpearman·100", "summary_metrics.spearman_rho"),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(13, 7))
    axes = axes.flatten()
    for ax, (title, dotted) in zip(axes, metrics):
        v0 = _resolve(rep_v0, dotted)
        va = _resolve(rep_a, dotted)
        vb = _resolve(rep_b, dotted)
        vab = _resolve(rep_ab, dotted)
        if "spearman_rho" in dotted:
            v0, va, vb, vab = (x * 100 for x in (v0, va, vb, vab))
        grid = np.array([[v0, va], [vb, vab]])  # rows: A=0/1, cols: B=0/1
        # Actually let's do rows=B (off/on top→bottom), cols=A (off/on left→right)
        # So [B=0,A=0]=v0, [B=0,A=1]=a, [B=1,A=0]=b, [B=1,A=1]=ab
        grid = np.array([[v0, va], [vb, vab]])
        im = ax.imshow(grid, cmap="RdYlGn", vmin=min(v0, va, vb, vab) * 0.92,
                       vmax=max(v0, va, vb, vab) * 1.08, aspect="auto")
        ax.set_xticks([0, 1]); ax.set_xticklabels(["A=off", "A=on"])
        ax.set_yticks([0, 1]); ax.set_yticklabels(["B=off", "B=on"])
        ax.set_title(title, fontsize=11)
        for i in range(2):
            for j in range(2):
                v = grid[i, j]
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        fontsize=12, color="black", fontweight="bold")
    fig.suptitle("2×2 A×B ablation grid (40-task, no Iter-C; v0=top-left, A+B=bottom-right)", fontsize=12, y=1.02)
    fig.tight_layout()
    out = CHARTS / "50_ab_grid_2x2.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_62task_validation() -> Path:
    """62-task slice: Week 0 → Week 1 v0 → Week 1.5 B-only / A+B."""
    configs = [
        ("Week 0\ndet_full", PHASE14 / "report_deterministic.json", "slice_report", "#9ca3af"),
        ("Week 0\nLLM (no rubric)", PHASE14 / "report_slice_llm_auto.json", None, "#fbbf24"),
        ("Week 1\nv0 rubric", PHASE14 / "report_slice_rubric_llm.json", None, "#a78bfa"),
        ("Week 1.5\nB only", WK15 / "report_iter_b_only_62task.json", None, "#10b981"),
        ("Week 1.5\nA+B", WK15 / "report_iter_a_b_62task.json", None, "#dc2626"),
    ]

    metrics = [
        ("HAI", "HAI"),
        ("RAS", "record_metrics.RAS"),
        ("SAS", "summary_metrics.SAS"),
        ("record\nScoreAlign", "record_metrics.ScoreAlign"),
        ("summary\nRankAlign", "summary_metrics.RankAlign"),
        ("summary\nSpearman·100", "summary_metrics.spearman_rho"),
    ]

    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    axes = axes.flatten()
    for ax, (title, dotted) in zip(axes, metrics):
        names, vals, cols = [], [], []
        for label, path, sub_key, col in configs:
            rep = _load(path, sub_key)
            if rep is None:
                continue
            v = _resolve(rep, dotted)
            if v is None:
                continue
            if "spearman_rho" in dotted:
                v *= 100
            names.append(label)
            vals.append(v)
            cols.append(col)
        x = np.arange(len(names))
        bars = ax.bar(x, vals, color=cols)
        ax.set_xticks(x)
        ax.set_xticklabels(names, fontsize=8)
        ax.set_title(title, fontsize=11)
        ax.set_ylim(0, max(vals) * 1.18 if vals else 100)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width()/2, v + max(vals) * 0.02, f"{v:.1f}",
                    ha="center", fontsize=8, fontweight="bold")
    fig.suptitle("62-task slice validation: does Week 1.5 (A+B / B-only) catch up to Week 0 baselines?", fontsize=12, y=1.02)
    fig.tight_layout()
    out = CHARTS / "51_62task_validation.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_summary_winners() -> Path:
    """Per-metric "winner" summary across all configs (40 + 62)."""
    rows = []
    # 40-task
    for label, path in [
        ("v0 (40)", ABL / "report_iter_v0.json"),
        ("A (40)", ABL / "report_iter_a_only.json"),
        ("B (40)", ABL / "report_iter_b_only.json"),
        ("AB (40)", ABL / "report_iter_a_b.json"),
        ("ABC (40)", ABL / "report_iter_abc.json"),
    ]:
        rep = _load(path)
        if rep is None:
            continue
        rows.append((label, rep))
    # 62-task
    for label, path, sub_key in [
        ("Week0 LLM (62)", PHASE14 / "report_slice_llm_auto.json", None),
        ("v0 (62)", PHASE14 / "report_slice_rubric_llm.json", None),
        ("B (62)", WK15 / "report_iter_b_only_62task.json", None),
        ("AB (62)", WK15 / "report_iter_a_b_62task.json", None),
    ]:
        rep = _load(path, sub_key)
        if rep is None:
            continue
        rows.append((label, rep))

    if not rows:
        return Path()

    metrics = ["HAI", "RAS", "SAS", "record_metrics.ScoreAlign",
               "summary_metrics.RankAlign", "summary_metrics.spearman_rho",
               "judgement_metrics.weighted_kappa"]
    metric_labels = ["HAI", "RAS", "SAS", "rec ScA", "sum RA", "sum ρ·100", "kappa·100"]

    matrix = []
    for label, rep in rows:
        vec = []
        for m in metrics:
            v = _resolve(rep, m)
            if v is None:
                vec.append(np.nan)
            else:
                if "spearman_rho" in m or "weighted_kappa" in m:
                    v *= 100
                vec.append(v)
        matrix.append(vec)
    arr = np.array(matrix)

    fig, ax = plt.subplots(figsize=(11, max(4.5, len(rows) * 0.5)))
    # Per-column normalization for color (winner = green)
    col_max = np.nanmax(arr, axis=0)
    col_min = np.nanmin(arr, axis=0)
    norm = (arr - col_min) / (col_max - col_min + 1e-9)
    im = ax.imshow(norm, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(metric_labels)))
    ax.set_xticklabels(metric_labels, fontsize=9)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([r[0] for r in rows], fontsize=9)
    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            v = arr[i, j]
            is_max = (col_max[j] == v) and not np.isnan(v)
            ax.text(j, i, f"{v:.1f}", ha="center", va="center",
                    fontsize=8,
                    color="black" if 0.3 <= norm[i, j] <= 0.85 or np.isnan(norm[i, j]) else "white",
                    fontweight="bold" if is_max else "normal")
    ax.set_title("All configs × metrics (cell color = relative position, bold = column max)")
    fig.tight_layout()
    out = CHARTS / "52_summary_winners.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [
        chart_2x2_ab_grid(),
        chart_62task_validation(),
        chart_summary_winners(),
    ]
    for p in outs:
        if p:
            print(f"chart written: {p}")
        else:
            print("chart skipped (insufficient data)")


if __name__ == "__main__":
    main()
