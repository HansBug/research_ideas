"""Compute RAS/SAS/HAI-style alignment metrics from a batch reviewer JSONL.

Replicates the formulas used in `reproduction/expert_review/benchmark.py`:

    ScoreAlign  = 100 * (1 - mean |reviewer - human|)
    RankAlign   = 100 * pairwise_order_accuracy(reviewer vs human)
    judgement_align = 100 * fraction(judgement match)
    Spearman ρ, Pearson r, MAE — auxiliary alignment indicators
    HAI_proxy   = 0.40·RAS_proxy + 0.30·SAS_proxy + 0.30·CRAS_proxy
                  (we lack issue_f1 / equivalence / calibration / stability,
                  so we substitute proxies. See `weights` block in output.)

This is a lightweight standalone analysis intended for the PR-comment narrative;
it is NOT a full benchmark replacement. The full benchmark requires re-invoking
the LLM to compute issue_f1 / equivalence / calibration etc.
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"

JUDGEMENT_LABELS = ("poor", "weak", "acceptable", "good", "excellent")


def _row_meta(r: dict) -> dict:
    meta = r.get("metadata") or {}
    if not meta and "metadata_json" in r:
        try:
            meta = json.loads(r["metadata_json"])
        except Exception:
            meta = {}
    return meta


def _normalize_human(val: Any, unit: Any) -> float | None:
    if val is None:
        return None
    try:
        v = float(val)
    except Exception:
        return None
    if math.isnan(v):
        return None
    u = (unit or "").strip().lower()
    if u in {"score_0_100", "/100"}:
        return max(0.0, min(1.0, v / 100.0))
    if u == "/10":
        return max(0.0, min(1.0, v / 10.0))
    return max(0.0, min(1.0, v))


def _judgement_from_score(s: float) -> str:
    if s >= 0.85:
        return "excellent"
    if s >= 0.70:
        return "good"
    if s >= 0.50:
        return "acceptable"
    if s >= 0.30:
        return "weak"
    return "poor"


def _pairwise_order_accuracy(reviewer: list[float], human: list[float]) -> float:
    """Fraction of pairs where reviewer order matches human order (ties skipped)."""
    if len(reviewer) < 2:
        return 0.0
    correct = 0
    total = 0
    for i, j in combinations(range(len(reviewer)), 2):
        h_d = human[i] - human[j]
        r_d = reviewer[i] - reviewer[j]
        if h_d == 0:
            continue
        total += 1
        if (h_d > 0) == (r_d > 0) or (r_d == 0):
            correct += 1
    return correct / total if total else 0.0


def _spearman(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return float("nan")
    sx = pd.Series(xs).rank()
    sy = pd.Series(ys).rank()
    if sx.std() == 0 or sy.std() == 0:
        return float("nan")
    return float(sx.corr(sy))


def _pearson(xs: list[float], ys: list[float]) -> float:
    if len(xs) < 3:
        return float("nan")
    sx = pd.Series(xs)
    sy = pd.Series(ys)
    if sx.std() == 0 or sy.std() == 0:
        return float("nan")
    return float(sx.corr(sy))


def _load_jsonl(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def compute_metrics(rows: list[dict]) -> dict[str, Any]:
    succ = [r for r in rows if r.get("success")]
    if not succ:
        return {"n_total": len(rows), "n_success": 0}

    paired = []
    for r in succ:
        meta = _row_meta(r)
        h = _normalize_human(meta.get("human_review_score"), meta.get("human_review_score_unit"))
        if h is None:
            continue
        paired.append({
            "item_id": r["item_id"],
            "paper_slug": meta.get("paper_slug", "?"),
            "case_id": meta.get("case_id", "?"),
            "llm_name": meta.get("llm_name", "?"),
            "reviewer_score": float(r["overall_score"]),
            "reviewer_judgement": str(r["overall_judgement"]),
            "reviewer_confidence": float(r["confidence"]),
            "evidence_discipline_score": float(r.get("evidence_discipline_score", 0.0)),
            "triage_label": str(r["triage_label"]),
            "human_score_norm": h,
            "human_judgement": _judgement_from_score(h),
            "latency_s": float(r.get("latency_s", 0.0)),
        })

    if not paired:
        return {"n_total": len(rows), "n_success": len(succ), "n_paired": 0}

    df = pd.DataFrame(paired)
    rev = df["reviewer_score"].tolist()
    hum = df["human_score_norm"].tolist()
    mae = sum(abs(r - h) for r, h in zip(rev, hum)) / len(rev)
    rmse = math.sqrt(sum((r - h) ** 2 for r, h in zip(rev, hum)) / len(rev))
    score_align = 100.0 * (1.0 - mae)  # benchmark.py-style ScoreAlign
    rank_align = 100.0 * _pairwise_order_accuracy(rev, hum)
    spearman = _spearman(rev, hum)
    pearson = _pearson(rev, hum)
    judgement_align = 100.0 * (df["reviewer_judgement"] == df["human_judgement"]).sum() / len(df)

    # Reviewer-side stats
    rev_mean = statistics.mean(rev)
    rev_std = statistics.pstdev(rev) if len(rev) > 1 else 0.0
    rev_low_count = sum(1 for v in rev if v < 0.3)
    rev_high_count = sum(1 for v in rev if v >= 0.7)
    confidence_mean = statistics.mean(df["confidence"]) if "confidence" in df.columns else statistics.mean(df["reviewer_confidence"])
    evidence_disc_mean = statistics.mean(df["evidence_discipline_score"])
    latency_mean = statistics.mean(df["latency_s"])
    latency_p95 = sorted(df["latency_s"])[int(0.95 * (len(df) - 1))] if len(df) > 1 else df["latency_s"].iloc[0]

    # Triage / judgement distributions
    triage_dist = df["triage_label"].value_counts().to_dict()
    judg_dist = df["reviewer_judgement"].value_counts().to_dict()
    backend_dist = pd.Series([r.get("used_review_backend", "?") for r in succ]).value_counts().to_dict()

    # Per-paper breakdown
    per_paper: dict[str, dict[str, Any]] = {}
    for paper, sub in df.groupby("paper_slug"):
        if len(sub) < 2:
            sub_rho = float("nan")
            sub_align = float("nan")
        else:
            rev_list = sub["reviewer_score"].tolist()
            hum_list = sub["human_score_norm"].tolist()
            sub_align = 100.0 * (1.0 - sum(abs(r - h) for r, h in zip(rev_list, hum_list)) / len(rev_list))
            sub_rho = _spearman(rev_list, hum_list)
        per_paper[paper] = {
            "n": len(sub),
            "reviewer_mean": float(sub["reviewer_score"].mean()),
            "human_mean": float(sub["human_score_norm"].mean()),
            "score_align": float(sub_align),
            "spearman_rho": float(sub_rho),
            "rank_align": 100.0 * _pairwise_order_accuracy(
                sub["reviewer_score"].tolist(),
                sub["human_score_norm"].tolist(),
            ),
        }

    # RAS / SAS / CRAS / HAI proxies (limited components)
    # RAS proxy weights remain the canonical 0.30 ScoreAlign + 0.20 ReasonProxy + ... but
    # we lack issue_f1/equivalence/calibration here, so we substitute Spearman-based
    # proxies. Document this in `weights_rationale`.
    spearman_to_score = max(0.0, 100.0 * (spearman if not math.isnan(spearman) else 0.0))
    confidence_score = 100.0 * confidence_mean
    evidence_score = 100.0 * evidence_disc_mean
    ras_proxy = (
        0.45 * score_align
        + 0.25 * spearman_to_score
        + 0.15 * judgement_align
        + 0.15 * confidence_score
    )
    sas_proxy = (
        0.40 * score_align
        + 0.30 * rank_align
        + 0.20 * evidence_score
        + 0.10 * confidence_score
    )
    cras_proxy = (
        0.50 * judgement_align
        + 0.50 * evidence_score
    )
    hai_proxy = 0.40 * ras_proxy + 0.30 * sas_proxy + 0.30 * cras_proxy

    return {
        "n_total": len(rows),
        "n_success": len(succ),
        "n_paired": len(paired),
        "paired_rows": paired,
        "alignment": {
            "MAE": mae,
            "RMSE": rmse,
            "ScoreAlign": score_align,
            "RankAlign": rank_align,
            "spearman_rho": spearman,
            "pearson_r": pearson,
            "JudgementAlign": judgement_align,
        },
        "reviewer_stats": {
            "score_mean": rev_mean,
            "score_std": rev_std,
            "low_count_lt_0.3": rev_low_count,
            "high_count_ge_0.7": rev_high_count,
            "confidence_mean": confidence_mean,
            "evidence_discipline_mean": evidence_disc_mean,
            "latency_mean_s": latency_mean,
            "latency_p95_s": latency_p95,
        },
        "human_stats": {
            "score_mean": statistics.mean(hum),
            "score_std": statistics.pstdev(hum) if len(hum) > 1 else 0.0,
        },
        "distributions": {
            "triage_label": triage_dist,
            "reviewer_judgement": judg_dist,
            "review_backend": backend_dist,
        },
        "per_paper": per_paper,
        "proxy_metrics": {
            "RAS_proxy": ras_proxy,
            "SAS_proxy": sas_proxy,
            "CRAS_proxy": cras_proxy,
            "HAI_proxy": hai_proxy,
            "weights_rationale": (
                "RAS proxy: 0.45·ScoreAlign + 0.25·Spearman + 0.15·JudgementAlign + 0.15·Confidence. "
                "SAS proxy: 0.40·ScoreAlign + 0.30·RankAlign + 0.20·Evidence + 0.10·Confidence. "
                "CRAS proxy: 0.50·JudgementAlign + 0.50·Evidence (no full TP/FP/FN component eval here). "
                "HAI proxy: 0.40·RAS + 0.30·SAS + 0.30·CRAS — same shape as benchmark.py."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=ETL_OUT / "experiment_baseline_result.jsonl")
    parser.add_argument("--new", type=Path, default=ETL_OUT / "experiment_new_result.jsonl")
    parser.add_argument("--output-json", type=Path, default=ETL_OUT / "experiment_alignment.json")
    args = parser.parse_args()

    base = compute_metrics(_load_jsonl(args.baseline))
    nw = compute_metrics(_load_jsonl(args.new))
    payload = {"baseline": base, "new": nw}

    # Compute deltas
    if base.get("n_paired", 0) > 0 and nw.get("n_paired", 0) > 0:
        keys_align = ["MAE", "RMSE", "ScoreAlign", "RankAlign", "spearman_rho", "pearson_r", "JudgementAlign"]
        keys_proxy = ["RAS_proxy", "SAS_proxy", "CRAS_proxy", "HAI_proxy"]
        delta_align = {k: nw["alignment"][k] - base["alignment"][k] for k in keys_align}
        delta_proxy = {k: nw["proxy_metrics"][k] - base["proxy_metrics"][k] for k in keys_proxy}
        payload["delta_new_minus_baseline"] = {
            "alignment": delta_align,
            "proxy_metrics": delta_proxy,
        }

    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"Alignment metrics written: {args.output_json}")
    for label, m in [("baseline", base), ("new", nw)]:
        if m.get("n_paired", 0) == 0:
            print(f"{label}: n_paired=0 (NO scores available)")
            continue
        a = m["alignment"]
        p = m["proxy_metrics"]
        print(f"{label}: n={m['n_paired']}, "
              f"ρ={a['spearman_rho']:.3f}, MAE={a['MAE']:.3f}, "
              f"ScoreAlign={a['ScoreAlign']:.1f}, RankAlign={a['RankAlign']:.1f}, "
              f"HAI_proxy={p['HAI_proxy']:.2f}")
    if "delta_new_minus_baseline" in payload:
        d = payload["delta_new_minus_baseline"]
        print(f"Δ (new - baseline): ScoreAlign={d['alignment']['ScoreAlign']:+.2f}, "
              f"HAI_proxy={d['proxy_metrics']['HAI_proxy']:+.2f}")


if __name__ == "__main__":
    main()
