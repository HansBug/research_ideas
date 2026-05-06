"""Charts comparing det / LLM-mode / rubric-LLM on the same 62-task slice."""
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


def _load() -> tuple[dict, dict, dict]:
    det = json.loads((PHASE14 / "report_deterministic.json").read_text())["slice_report"]
    llm = json.loads((PHASE14 / "report_slice_llm_auto.json").read_text())
    rub = json.loads((PHASE14 / "report_slice_rubric_llm.json").read_text())
    return det, llm, rub


def chart_three_way_headline() -> Path:
    det, llm, rub = _load()
    metrics = [
        ("HAI", det["HAI"], llm["HAI"], rub["HAI"]),
        ("HAI_legacy", det["HAI_legacy"], llm["HAI_legacy"], rub["HAI_legacy"]),
        ("RAS", det["record_metrics"]["RAS"], llm["record_metrics"]["RAS"], rub["record_metrics"]["RAS"]),
        ("SAS", det["summary_metrics"]["SAS"], llm["summary_metrics"]["SAS"], rub["summary_metrics"]["SAS"]),
        ("CRAS", det["component_metrics"]["CRAS"], llm["component_metrics"]["CRAS"], rub["component_metrics"]["CRAS"]),
        ("PDS", det["protocol_metrics"]["PDS"], llm["protocol_metrics"]["PDS"], rub["protocol_metrics"]["PDS"]),
    ]
    names = [m[0] for m in metrics]
    det_v = [m[1] for m in metrics]
    llm_v = [m[2] for m in metrics]
    rub_v = [m[3] for m in metrics]

    x = np.arange(len(names))
    w = 0.27
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.bar(x - w, det_v, w, color="#9ca3af", label="deterministic")
    ax.bar(x, llm_v, w, color="#fbbf24", label="LLM-mode (no rubric)")
    ax.bar(x + w, rub_v, w, color="#2563eb", label="rubric-LLM (Week 1)")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylim(0, 110)
    ax.set_ylabel("score (0-100)")
    ax.set_title("Slice 62 task: deterministic vs LLM-mode vs rubric-LLM (Week 1)")
    ax.legend(loc="lower right")
    for arr, off, color, weight in [(det_v, -w, "#374151", "normal"),
                                    (llm_v, 0, "#92400e", "normal"),
                                    (rub_v, +w, "#1e3a8a", "bold")]:
        for i, v in enumerate(arr):
            ax.text(i + off, v + 1.5, f"{v:.1f}", ha="center", fontsize=8, color=color, fontweight=weight)
    fig.tight_layout()
    out = CHARTS / "30_three_way_headline.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_submetric_winners() -> Path:
    """Sub-metric drilldown: where rubric wins/loses vs LLM-mode."""
    det, llm, rub = _load()
    sub = [
        # (label, det, llm, rub)
        ("record\nScoreAlign", det["record_metrics"]["ScoreAlign"], llm["record_metrics"]["ScoreAlign"], rub["record_metrics"]["ScoreAlign"]),
        ("record\nissue_f1·100", det["record_metrics"]["issue_f1"]*100, llm["record_metrics"]["issue_f1"]*100, rub["record_metrics"]["issue_f1"]*100),
        ("record\nEquivAlign", det["record_metrics"]["EquivAlign"], llm["record_metrics"]["EquivAlign"], rub["record_metrics"]["EquivAlign"]),
        ("record\nCalib", det["record_metrics"]["Calib"], llm["record_metrics"]["Calib"], rub["record_metrics"]["Calib"]),
        ("summary\nScoreAlign", det["summary_metrics"]["ScoreAlign"], llm["summary_metrics"]["ScoreAlign"], rub["summary_metrics"]["ScoreAlign"]),
        ("summary\nRankAlign", det["summary_metrics"]["RankAlign"], llm["summary_metrics"]["RankAlign"], rub["summary_metrics"]["RankAlign"]),
        ("summary\nSpearman·100", det["summary_metrics"]["spearman_rho"]*100, llm["summary_metrics"]["spearman_rho"]*100, rub["summary_metrics"]["spearman_rho"]*100),
        ("crit_issue\nrecall·100", det["critical_issue_metrics"]["critical_issue_recall"]*100, llm["critical_issue_metrics"]["critical_issue_recall"]*100, rub["critical_issue_metrics"]["critical_issue_recall"]*100),
        ("judg\nmacro_F1·100", det["judgement_metrics"]["macro_f1"]*100, llm["judgement_metrics"]["macro_f1"]*100, rub["judgement_metrics"]["macro_f1"]*100),
    ]
    names = [s[0] for s in sub]
    det_v = [s[1] for s in sub]
    llm_v = [s[2] for s in sub]
    rub_v = [s[3] for s in sub]

    x = np.arange(len(names))
    w = 0.27
    fig, ax = plt.subplots(figsize=(13, 5.2))
    ax.bar(x - w, det_v, w, color="#9ca3af", label="deterministic")
    ax.bar(x, llm_v, w, color="#fbbf24", label="LLM-mode (no rubric)")
    ax.bar(x + w, rub_v, w, color="#2563eb", label="rubric-LLM (Week 1)")
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylim(0, 110)
    ax.set_ylabel("score (0-100)")
    ax.set_title("Sub-metric drilldown: where does rubric win or lose vs LLM-mode?")
    ax.legend(loc="lower right")
    # Highlight key sub-metrics
    for i, (l, r) in enumerate(zip(llm_v, rub_v)):
        d = r - l
        c = "#16a34a" if d > 1.5 else ("#dc2626" if d < -1.5 else "#9ca3af")
        marker = "▲" if d > 1.5 else ("▼" if d < -1.5 else "≈")
        ax.text(i + w, r + 4, f"{marker} {d:+.1f}", ha="center", fontsize=8, color=c, fontweight="bold")
    fig.tight_layout()
    out = CHARTS / "31_submetric_winners.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_acceptance_gate() -> Path:
    """7 Week 0 acceptance gates with rubric values overlaid."""
    det, llm, rub = _load()
    gates = [
        # (name, target, baseline_det, baseline_LLM_or_full, rubric_value, target_op)
        ("HAI ≥ 85.02", 85.02, det["HAI"], llm["HAI"], rub["HAI"], "ge"),
        ("record\nScoreAlign ≥ 65", 65, det["record_metrics"]["ScoreAlign"], llm["record_metrics"]["ScoreAlign"], rub["record_metrics"]["ScoreAlign"], "ge"),
        ("summary\nRankAlign ≥ 70", 70, det["summary_metrics"]["RankAlign"], llm["summary_metrics"]["RankAlign"], rub["summary_metrics"]["RankAlign"], "ge"),
        ("summary\nScoreAlign ≥ 60", 60, det["summary_metrics"]["ScoreAlign"], llm["summary_metrics"]["ScoreAlign"], rub["summary_metrics"]["ScoreAlign"], "ge"),
        ("Spearman·100\n≥ 45", 45, det["summary_metrics"]["spearman_rho"]*100, llm["summary_metrics"]["spearman_rho"]*100, rub["summary_metrics"]["spearman_rho"]*100, "ge"),
        ("weighted_kappa\n·100 ≥ 65", 65, det["judgement_metrics"]["weighted_kappa"]*100, llm["judgement_metrics"]["weighted_kappa"]*100, rub["judgement_metrics"]["weighted_kappa"]*100, "ge"),
        ("crit_issue\nrecall·100 ≥ 90", 90, det["critical_issue_metrics"]["critical_issue_recall"]*100, llm["critical_issue_metrics"]["critical_issue_recall"]*100, rub["critical_issue_metrics"]["critical_issue_recall"]*100, "ge"),
    ]
    names = [g[0] for g in gates]
    targets = [g[1] for g in gates]
    rubs = [g[4] for g in gates]
    passes = [r >= t for r, t in zip(rubs, targets)]

    x = np.arange(len(names))
    w = 0.65
    fig, ax = plt.subplots(figsize=(11.5, 4.8))
    colors = ["#16a34a" if p else "#dc2626" for p in passes]
    bars = ax.bar(x, rubs, w, color=colors)
    # Target markers as horizontal segments
    for i, t in enumerate(targets):
        ax.hlines(t, i - w/2, i + w/2, color="#1f2937", linestyle="--", linewidth=2)
    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=9)
    ax.set_ylabel("score")
    ax.set_ylim(0, max(110, max(rubs) * 1.15))
    n_pass = sum(passes)
    ax.set_title(f"Week 1 rubric vs Week 0 acceptance gates: {n_pass}/{len(gates)} pass")
    for b, v, t, p in zip(bars, rubs, targets, passes):
        mark = "✓" if p else "✗"
        c = "#14532d" if p else "#7f1d1d"
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{mark} {v:.1f}", ha="center", fontsize=10, fontweight="bold", color=c)
        ax.text(b.get_x() + b.get_width()/2, t + 2.5, f"target {t}", ha="center", fontsize=8, color="#1f2937")
    fig.tight_layout()
    out = CHARTS / "32_acceptance_gate.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [chart_three_way_headline(), chart_submetric_winners(), chart_acceptance_gate()]
    for p in outs:
        print(f"chart written: {p}")


if __name__ == "__main__":
    main()
