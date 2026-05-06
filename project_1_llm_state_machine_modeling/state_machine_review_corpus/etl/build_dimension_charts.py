"""Per-dimension reviewer behavior comparison: baseline vs new."""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"
CHARTS = ETL_OUT / "charts"
CHARTS.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 140,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "font.size": 10,
})


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _dimension_scores(rows: list[dict]) -> dict[str, list[float]]:
    out: dict[str, list[float]] = {}
    for r in rows:
        if not r.get("success"):
            continue
        try:
            dims = json.loads(r.get("dimension_results_json", "[]"))
        except Exception:
            continue
        for d in dims:
            out.setdefault(d["dimension_name"], []).append(float(d.get("score", 0.0)))
    return out


def chart_dimension_comparison() -> Path:
    base = _load_jsonl(ETL_OUT / "experiment_baseline_result.jsonl")
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")
    base_dims = _dimension_scores(base)
    new_dims = _dimension_scores(new)

    dim_names = [
        "notation_syntax", "semantic_completeness", "behavioral_consistency",
        "requirement_traceability", "pragmatic_clarity", "evidence_discipline",
    ]
    dim_labels = ["Notation\nSyntax", "Semantic\nCompleteness", "Behavioral\nConsistency",
                  "Requirement\nTraceability", "Pragmatic\nClarity", "Evidence\nDiscipline"]

    base_means = [
        (sum(base_dims.get(d, [])) / len(base_dims[d])) if base_dims.get(d) else 0.0
        for d in dim_names
    ]
    new_means = [
        (sum(new_dims.get(d, [])) / len(new_dims[d])) if new_dims.get(d) else 0.0
        for d in dim_names
    ]
    base_stds = [
        (float(np.std(base_dims[d]))) if base_dims.get(d) else 0.0
        for d in dim_names
    ]
    new_stds = [
        (float(np.std(new_dims[d]))) if new_dims.get(d) else 0.0
        for d in dim_names
    ]

    x = np.arange(len(dim_names))
    w = 0.38
    fig, ax = plt.subplots(figsize=(10.5, 4.8))
    ax.bar(x - w/2, base_means, w, yerr=base_stds, color="#9ca3af", label=f"baseline (n={len([r for r in base if r.get('success')])})", capsize=4)
    ax.bar(x + w/2, new_means, w, yerr=new_stds, color="#2563eb", label=f"new (n={len([r for r in new if r.get('success')])})", capsize=4)
    ax.set_xticks(x)
    ax.set_xticklabels(dim_labels)
    ax.set_ylabel("dimension score (0..1)")
    ax.set_ylim(0, 1.0)
    ax.set_title("Per-dimension reviewer score: baseline vs new (protocol-FSM)")
    ax.legend()
    for i, (bm, nm) in enumerate(zip(base_means, new_means)):
        ax.text(i - w/2, bm + 0.02, f"{bm:.2f}", ha="center", fontsize=8, color="#374151")
        ax.text(i + w/2, nm + 0.02, f"{nm:.2f}", ha="center", fontsize=8, color="#1e3a8a", fontweight="bold")
    fig.tight_layout()
    out = CHARTS / "14_dimension_comparison.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_proxy_metrics_radar() -> Path:
    """RAS / SAS / CRAS / HAI proxy on baseline vs new."""
    align_path = ETL_OUT / "experiment_alignment.json"
    if not align_path.exists():
        return Path()
    payload = json.loads(align_path.read_text())
    base = payload.get("baseline", {})
    new = payload.get("new", {})
    if not base.get("proxy_metrics") or not new.get("proxy_metrics"):
        return Path()

    metrics = ["RAS_proxy", "SAS_proxy", "CRAS_proxy", "HAI_proxy"]
    base_vals = [base["proxy_metrics"][m] for m in metrics]
    new_vals = [new["proxy_metrics"][m] for m in metrics]

    x = np.arange(len(metrics))
    w = 0.38
    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars1 = ax.bar(x - w/2, base_vals, w, color="#9ca3af", label=f"baseline (UML/SysML, n={base.get('n_paired')})")
    bars2 = ax.bar(x + w/2, new_vals, w, color="#2563eb", label=f"new (protocol-FSM, n={new.get('n_paired')})")
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("_proxy", "") for m in metrics])
    ax.set_ylabel("score (0..100)")
    ax.set_ylim(0, 100)
    ax.set_title("Proxy alignment metrics: reviewer behaviour on baseline vs new domain")
    ax.legend()
    for b, v in zip(bars1, base_vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=9, color="#374151")
    for b, v in zip(bars2, new_vals):
        ax.text(b.get_x() + b.get_width()/2, v + 1.5, f"{v:.1f}", ha="center", fontsize=9, color="#1e3a8a", fontweight="bold")
    # Show delta line
    for i, (bv, nv) in enumerate(zip(base_vals, new_vals)):
        d = nv - bv
        ax.text(i, max(bv, nv) + 5, f"Δ={d:+.1f}",
                ha="center", fontsize=9, color="#16a34a" if d > 0 else "#dc2626")
    fig.tight_layout()
    out = CHARTS / "15_proxy_metrics.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_psmbench_llm_ranking_cross_check() -> Path:
    """Compare reviewer's mean score per LLM (on new sample) against PSMBench's
    paper-style auto-F1 mean per LLM. If our reviewer ranks LLMs the same way
    the paper's auto F1 does, that's a strong cross-validation signal.
    """
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")
    if not new:
        return Path()
    rows = []
    for r in new:
        if not r.get("success"):
            continue
        try:
            meta = json.loads(r.get("metadata_json", "{}"))
        except Exception:
            meta = {}
        if meta.get("paper_slug") != "psmbench":
            continue
        rows.append({
            "llm": meta.get("llm_name", "?"),
            "reviewer": float(r["overall_score"]),
            "paper_F1": float(meta.get("human_review_score", 0.0) or 0.0),
        })
    if not rows:
        return Path()

    import pandas as pd
    df = pd.DataFrame(rows)
    g = df.groupby("llm").agg(
        reviewer_mean=("reviewer", "mean"),
        paper_F1_mean=("paper_F1", "mean"),
        n=("reviewer", "size"),
    ).sort_values("paper_F1_mean", ascending=True)

    fig, ax = plt.subplots(figsize=(9.5, 5.0))
    y = np.arange(len(g))
    w = 0.4
    ax.barh(y - w/2, g["paper_F1_mean"], w, color="#9ca3af",
            label="PSMBench paper-style F1 (auto)", alpha=0.85)
    ax.barh(y + w/2, g["reviewer_mean"], w, color="#2563eb",
            label="Our reviewer overall_score (gpt-5.5)", alpha=0.95)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{idx} (n={int(g.at[idx,'n'])})" for idx in g.index])
    ax.set_xlabel("score (0..1)")
    ax.set_xlim(0, 1.0)
    ax.set_title("PSMBench LLM ranking: reviewer vs paper auto-F1 (per LLM mean)")
    ax.legend()

    # Annotate per-LLM Spearman corr
    rho = df["reviewer"].rank().corr(df["paper_F1"].rank())
    ax.text(0.62, 0.05, f"item-level Spearman ρ = {rho:.3f}\n(n={len(df)} item pairs)",
            transform=ax.transAxes, fontsize=10, color="#374151",
            bbox=dict(boxstyle="round", facecolor="#fef3c7", edgecolor="#fbbf24"))
    fig.tight_layout()
    out = CHARTS / "16_psmbench_ranking_crosscheck.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [chart_dimension_comparison(), chart_proxy_metrics_radar(), chart_psmbench_llm_ranking_cross_check()]
    for p in outs:
        if p:
            print(f"chart written: {p}")


if __name__ == "__main__":
    main()
