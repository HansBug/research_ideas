"""Charts comparing reviewer behavior on baseline vs new (protocol-FSM) samples."""
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
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def _row_meta(r: dict) -> dict:
    meta = r.get("metadata") or {}
    if not meta and "metadata_json" in r:
        try:
            meta = json.loads(r["metadata_json"])
        except Exception:
            meta = {}
    return meta


def _normalize_human(val, unit) -> float | None:
    if val is None:
        return None
    try:
        v = float(val)
    except Exception:
        return None
    u = (unit or "").strip().lower()
    if u in {"score_0_100", "/100"}:
        return max(0.0, min(1.0, v / 100.0))
    if u == "/10":
        return max(0.0, min(1.0, v / 10.0))
    return max(0.0, min(1.0, v))


def chart_score_distribution() -> Path:
    base = _load_jsonl(ETL_OUT / "experiment_baseline_result.jsonl")
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")

    base_scores = [r["overall_score"] for r in base if r.get("success")]
    new_scores = [r["overall_score"] for r in new if r.get("success")]

    fig, ax = plt.subplots(figsize=(8.5, 4.4))
    bins = np.linspace(0, 1, 11)
    ax.hist([base_scores, new_scores], bins=bins, color=["#9ca3af", "#2563eb"],
            label=[f"baseline (UML/SysML, n={len(base_scores)})",
                   f"new (protocol-FSM, n={len(new_scores)})"], alpha=0.85)
    ax.set_xlabel("reviewer overall_score (0..1)")
    ax.set_ylabel("count")
    ax.set_title("Reviewer overall_score distribution: baseline vs new (protocol-FSM)")
    ax.legend()
    fig.tight_layout()
    out = CHARTS / "10_score_distribution.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_alignment_scatter() -> Path:
    base = _load_jsonl(ETL_OUT / "experiment_baseline_result.jsonl")
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6), sharex=True, sharey=True)
    for ax, rows, label, color in [
        (axes[0], base, "baseline (UML/SysML)", "#9ca3af"),
        (axes[1], new, "new (protocol-FSM)", "#2563eb"),
    ]:
        xs, ys = [], []
        for r in rows:
            if not r.get("success"):
                continue
            meta = _row_meta(r)
            h = _normalize_human(meta.get("human_review_score"), meta.get("human_review_score_unit"))
            if h is None:
                continue
            xs.append(h)
            ys.append(r["overall_score"])
        if xs:
            ax.scatter(xs, ys, c=color, alpha=0.85, s=30, edgecolors="white", linewidth=0.5)
            ax.plot([0, 1], [0, 1], color="#d1d5db", linestyle="--", linewidth=1)
            sx = pd.Series(xs); sy = pd.Series(ys)
            rho = sx.rank().corr(sy.rank()) if sx.std() and sy.std() else None
            mae = float(np.mean(np.abs(np.array(xs) - np.array(ys)))) if xs else None
            ax.set_title(f"{label}\nn={len(xs)}, ρ={rho:.3f}, MAE={mae:.3f}")
        else:
            ax.set_title(f"{label}\n(no paired scores)")
        ax.set_xlabel("human reference score (normalized 0..1)")
        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.02, 1.02)
        ax.set_aspect("equal")
    axes[0].set_ylabel("reviewer overall_score")
    fig.suptitle("Reviewer ↔ human alignment: baseline vs new sample", y=1.02)
    fig.tight_layout()
    out = CHARTS / "11_alignment_scatter.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_judgement_triage() -> Path:
    base = _load_jsonl(ETL_OUT / "experiment_baseline_result.jsonl")
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")
    judg_order = ["poor", "weak", "acceptable", "good", "excellent"]
    triage_order = ["direct_pass", "review_required", "high_risk", "uncertain", "blocked"]

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.6))
    for label, rows, color in [
        ("baseline", base, "#9ca3af"),
        ("new", new, "#2563eb"),
    ]:
        succ = [r for r in rows if r.get("success")]
        # Judgement
        jcounts = {k: 0 for k in judg_order}
        for r in succ:
            j = r.get("overall_judgement", "?")
            jcounts[j] = jcounts.get(j, 0) + 1
        # Triage
        tcounts = {k: 0 for k in triage_order}
        for r in succ:
            t = r.get("triage_label", "?")
            tcounts[t] = tcounts.get(t, 0) + 1

        offset = 0.0 if label == "baseline" else 0.4
        x_j = np.arange(len(judg_order))
        x_t = np.arange(len(triage_order))
        axes[0].bar(x_j + offset, [jcounts[k] for k in judg_order], width=0.4, label=label, color=color)
        axes[1].bar(x_t + offset, [tcounts[k] for k in triage_order], width=0.4, label=label, color=color)

    axes[0].set_xticks(np.arange(len(judg_order)) + 0.2)
    axes[0].set_xticklabels(judg_order, rotation=20)
    axes[0].set_title("Reviewer overall_judgement distribution")
    axes[0].set_ylabel("count")
    axes[0].legend()

    axes[1].set_xticks(np.arange(len(triage_order)) + 0.2)
    axes[1].set_xticklabels(triage_order, rotation=20)
    axes[1].set_title("Reviewer triage_label distribution")
    axes[1].legend()

    fig.tight_layout()
    out = CHARTS / "12_judgement_triage.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def chart_per_paper() -> Path:
    base = _load_jsonl(ETL_OUT / "experiment_baseline_result.jsonl")
    new = _load_jsonl(ETL_OUT / "experiment_new_result.jsonl")

    rows = []
    for r in base + new:
        if not r.get("success"):
            continue
        meta = _row_meta(r)
        rows.append({
            "paper": meta.get("paper_slug", "?"),
            "set": "baseline" if meta.get("paper_slug") in {
                "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models",
                "llms_emp", "ttool-ai",
            } else "new",
            "reviewer_score": r["overall_score"],
            "human_norm": _normalize_human(meta.get("human_review_score"), meta.get("human_review_score_unit")),
            "latency_s": r.get("latency_s"),
        })
    df = pd.DataFrame(rows)
    if df.empty:
        return Path()

    short_names = {
        "structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models": "structure-event\n-driven",
        "llms_emp": "llms_emp",
        "ttool-ai": "ttool-ai",
        "psmbench": "psmbench",
        "rfcnlp": "rfcnlp",
        "hermes": "hermes",
    }
    df["paper_short"] = df["paper"].map(lambda p: short_names.get(p, p))
    grp = df.groupby("paper_short").agg(
        reviewer_mean=("reviewer_score", "mean"),
        reviewer_std=("reviewer_score", "std"),
        human_mean=("human_norm", "mean"),
        n=("reviewer_score", "size"),
    ).fillna(0.0)
    # Sort by set then by mean
    paper_set = df.drop_duplicates("paper_short").set_index("paper_short")["set"].to_dict()
    grp["set"] = grp.index.map(paper_set)
    grp = grp.sort_values(["set", "reviewer_mean"], ascending=[True, False])

    fig, ax = plt.subplots(figsize=(9.5, 4.6))
    x = np.arange(len(grp))
    w = 0.4
    colors_rev = ["#1d4ed8" if s == "new" else "#6b7280" for s in grp["set"]]
    colors_hum = ["#93c5fd" if s == "new" else "#d1d5db" for s in grp["set"]]
    bars1 = ax.bar(x - w/2, grp["reviewer_mean"], w, yerr=grp["reviewer_std"], color=colors_rev,
                   label="reviewer mean", alpha=0.9, capsize=4)
    bars2 = ax.bar(x + w/2, grp["human_mean"], w, color=colors_hum, label="human mean (norm 0..1)", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{p}\n(n={int(grp.at[p,'n'])}, {grp.at[p,'set']})" for p in grp.index])
    ax.set_ylabel("score")
    ax.set_ylim(0, 1.0)
    ax.set_title("Per-paper: reviewer score vs normalized human score")
    ax.legend(loc="upper right")
    fig.tight_layout()
    out = CHARTS / "13_per_paper.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def main() -> None:
    outs = [
        chart_score_distribution(),
        chart_alignment_scatter(),
        chart_judgement_triage(),
        chart_per_paper(),
    ]
    for p in outs:
        if p:
            print(f"chart written: {p}")


if __name__ == "__main__":
    main()
