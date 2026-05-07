"""Visualize the protocol-FSM corpus expansion + benchmark integration."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"
CHARTS = ETL_OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

# Tight, neutral style
plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def chart_coverage_growth() -> Path:
    """Bar chart: coverage before vs after across summary regime metrics."""
    metrics = ["total\nrecords", "summary\nmain_eval", "summary\nfamilies", "protocol\nfamilies"]
    before = [820, 84, 12, 4]
    after = [973, 214, 28, 7]
    growth = [f"+{a-b} ({a/b:.1f}×)" for a, b in zip(after, before)]

    x = np.arange(len(metrics))
    w = 0.38
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bars1 = ax.bar(x - w/2, before, w, color="#9ca3af", label="baseline (820 rows)")
    bars2 = ax.bar(x + w/2, after, w, color="#2563eb", label="combined (973 rows)")
    ax.set_xticks(x)
    ax.set_xticklabels(metrics)
    ax.set_ylabel("count")
    ax.set_title("Reviewer benchmark coverage: baseline → combined (after protocol-FSM ETL)")
    ax.legend(loc="upper right")
    for b, val in zip(bars1, before):
        ax.text(b.get_x() + b.get_width()/2, val + max(after)*0.01, str(val), ha="center", fontsize=9, color="#4b5563")
    for b, val, g in zip(bars2, after, growth):
        ax.text(b.get_x() + b.get_width()/2, val + max(after)*0.01, str(val), ha="center", fontsize=9, color="#1e3a8a", fontweight="bold")
        ax.text(b.get_x() + b.get_width()/2, val + max(after)*0.06, g, ha="center", fontsize=8, color="#16a34a")
    ax.set_ylim(0, max(after) * 1.20)
    fig.tight_layout()
    out = CHARTS / "01_coverage_growth.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_llm_ranking() -> Path:
    """Horizontal bar chart of PSMBench LLM mean macro-F1."""
    df = pd.read_parquet(ETL_OUT / "protocol_fsm_human_review_records.parquet")
    psm = df[(df["paper_slug"] == "psmbench") & (df["record_type"] == "summary_level_run_score")]
    rank = psm.groupby("llm_name")["human_review_score"].agg(["mean", "std"]).sort_values("mean", ascending=True)

    fig, ax = plt.subplots(figsize=(8.5, 5.0))
    colors = ["#dc2626" if v < 0.30 else ("#f59e0b" if v < 0.45 else "#16a34a") for v in rank["mean"]]
    y = np.arange(len(rank))
    bars = ax.barh(y, rank["mean"], xerr=rank["std"], color=colors, alpha=0.85, ecolor="#6b7280", capsize=3)
    ax.set_yticks(y)
    ax.set_yticklabels(rank.index)
    ax.set_xlabel("mean F1 (state F1 + transition F1, averaged over 14 protocols)")
    ax.set_title("PSMBench LLM ranking — extracting protocol state machines from RFC")
    ax.set_xlim(0, 1.0)
    ax.axvline(0.5, color="#9ca3af", linestyle="--", linewidth=0.7)
    for b, m, s in zip(bars, rank["mean"], rank["std"]):
        ax.text(m + s + 0.02, b.get_y() + b.get_height()/2, f"{m:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    out = CHARTS / "02_llm_ranking.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_protocol_difficulty() -> Path:
    """Per-protocol mean F1 (averaged across 9 LLMs)."""
    df = pd.read_parquet(ETL_OUT / "protocol_fsm_human_review_records.parquet")
    psm = df[(df["paper_slug"] == "psmbench") & (df["record_type"] == "summary_level_run_score")]
    proto = psm.groupby("case_id")["human_review_score"].agg(["mean", "std"]).sort_values("mean", ascending=True)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    colors = plt.cm.RdYlGn(proto["mean"] / max(proto["mean"]))
    y = np.arange(len(proto))
    bars = ax.barh(y, proto["mean"], xerr=proto["std"], color=colors, alpha=0.90, ecolor="#6b7280", capsize=3)
    ax.set_yticks(y)
    ax.set_yticklabels(proto.index)
    ax.set_xlabel("mean F1 across 9 LLMs")
    ax.set_title("Per-protocol PSM extraction difficulty (lower = harder for LLMs)")
    ax.set_xlim(0, 1.0)
    for b, m in zip(bars, proto["mean"]):
        ax.text(m + 0.02, b.get_y() + b.get_height()/2, f"{m:.3f}", va="center", fontsize=9)
    fig.tight_layout()
    out = CHARTS / "03_protocol_difficulty.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_heatmap() -> Path:
    """Heatmap of LLM × protocol F1."""
    df = pd.read_parquet(ETL_OUT / "protocol_fsm_human_review_records.parquet")
    psm = df[(df["paper_slug"] == "psmbench") & (df["record_type"] == "summary_level_run_score")]
    pivot = psm.pivot_table(index="llm_name", columns="case_id", values="human_review_score", aggfunc="first")
    # Order rows by mean (best on top), columns by mean (easiest left)
    pivot = pivot.loc[pivot.mean(axis=1).sort_values(ascending=False).index]
    pivot = pivot[pivot.mean(axis=0).sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(11.5, 5.6))
    im = ax.imshow(pivot.values, cmap="RdYlGn", vmin=0, vmax=1, aspect="auto")
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    for i in range(pivot.shape[0]):
        for j in range(pivot.shape[1]):
            v = pivot.values[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=8,
                    color="black" if 0.30 <= v <= 0.75 else "white")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025)
    cbar.set_label("F1")
    ax.set_title("PSMBench: LLM × protocol F1 heatmap (rows=LLM, cols=protocol)")
    fig.tight_layout()
    out = CHARTS / "04_llm_protocol_heatmap.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_paper_coverage() -> Path:
    """Stacked bar: summary regime paper coverage before vs after."""
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    before = {"ttool-ai": 84}
    after = {"psmbench": 126, "ttool-ai": 84, "rfcnlp": 4}

    colors_after = {"psmbench": "#2563eb", "ttool-ai": "#9ca3af", "rfcnlp": "#16a34a"}
    bottom = 0
    ax.bar(["before"], [84], color="#9ca3af", label="ttool-ai (84)")
    bottom = 0
    for paper, count in after.items():
        c = colors_after[paper]
        ax.bar(["after"], [count], bottom=bottom, color=c, alpha=0.95,
               label=None if paper == "ttool-ai" else f"{paper} ({count})")
        ax.text(1, bottom + count/2, f"{paper}\n{count}", ha="center", va="center",
                fontsize=9, fontweight="bold", color="white" if c != "#9ca3af" else "#111827")
        bottom += count
    ax.text(0, 84/2, f"ttool-ai\n84", ha="center", va="center", fontsize=9, fontweight="bold", color="#111827")
    ax.set_ylabel("summary main_eval rows")
    ax.set_title("summary regime paper coverage: 1 paper / 84 rows → 3 papers / 214 rows")
    ax.set_ylim(0, 250)
    fig.tight_layout()
    out = CHARTS / "05_paper_coverage.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outputs = [
        chart_coverage_growth(),
        chart_llm_ranking(),
        chart_protocol_difficulty(),
        chart_heatmap(),
        chart_paper_coverage(),
    ]
    for p in outputs:
        print(f"chart written: {p}")


if __name__ == "__main__":
    main()
