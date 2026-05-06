"""Analyze a reviewer batch JSONL output: distributions, correlation with
human scores, per-paper breakdown, and (optionally) old-vs-new comparison.

Usage:
    python -m state_machine_review_corpus.etl.analyze_reviewer_run \
        --baseline etl/out/experiment_baseline_result.jsonl \
        --new etl/out/experiment_new_result.jsonl \
        --output-json etl/out/experiment_analysis.json
"""
from __future__ import annotations

import argparse
import json
import math
import statistics
from pathlib import Path
from typing import Any

import pandas as pd

CORPUS_ROOT = Path(__file__).resolve().parent.parent
ETL_OUT = CORPUS_ROOT / "etl" / "out"


def _normalize_human_score(score: float | None, unit: str | None) -> float | None:
    """Map human scores to 0..1 for comparable plotting."""
    if score is None or (isinstance(score, float) and math.isnan(score)):
        return None
    s = float(score)
    u = (unit or "").strip().lower()
    if u in {"score_0_100", "/100"}:
        return max(0.0, min(1.0, s / 100.0))
    if u == "/10":
        return max(0.0, min(1.0, s / 10.0))
    return max(0.0, min(1.0, s))


def _spearman(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    rx = pd.Series(xs).rank()
    ry = pd.Series(ys).rank()
    if rx.std() == 0 or ry.std() == 0:
        return None
    return float(rx.corr(ry, method="pearson"))


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    sx = pd.Series(xs)
    sy = pd.Series(ys)
    if sx.std() == 0 or sy.std() == 0:
        return None
    return float(sx.corr(sy))


def _mae(xs: list[float], ys: list[float]) -> float | None:
    if not xs or len(xs) != len(ys):
        return None
    return float(sum(abs(x - y) for x, y in zip(xs, ys)) / len(xs))


def _summarize_run(rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(rows)
    succ = [r for r in rows if r.get("success")]
    if not succ:
        return {"total": total, "success_count": 0}

    reviewer_scores = [float(r["overall_score"]) for r in succ]
    confidences = [float(r["confidence"]) for r in succ]
    judgements: dict[str, int] = {}
    triages: dict[str, int] = {}
    backends: dict[str, int] = {}
    for r in succ:
        judgements[r.get("overall_judgement", "?")] = judgements.get(r.get("overall_judgement", "?"), 0) + 1
        triages[r.get("triage_label", "?")] = triages.get(r.get("triage_label", "?"), 0) + 1
        backend = r.get("used_review_backend") or "unknown"
        backends[backend] = backends.get(backend, 0) + 1

    # Pull human scores from metadata (flat output uses metadata_json)
    human_norms: list[float | None] = []
    for r in succ:
        meta = r.get("metadata") or {}
        if not meta and "metadata_json" in r:
            try:
                meta = json.loads(r["metadata_json"])
            except Exception:
                meta = {}
        h = meta.get("human_review_score")
        u = meta.get("human_review_score_unit")
        human_norms.append(_normalize_human_score(h, u))
    paired = [
        (rs, hn)
        for rs, hn in zip(reviewer_scores, human_norms)
        if hn is not None
    ]
    paired_xs = [p[0] for p in paired]
    paired_ys = [p[1] for p in paired]

    latencies = [float(r.get("latency_s", 0.0)) for r in succ]
    return {
        "total": total,
        "success_count": len(succ),
        "reviewer_score": {
            "mean": statistics.mean(reviewer_scores),
            "std": statistics.pstdev(reviewer_scores) if len(reviewer_scores) > 1 else 0.0,
            "min": min(reviewer_scores),
            "max": max(reviewer_scores),
        },
        "human_score_normalized": {
            "mean": statistics.mean([h for h in human_norms if h is not None]) if any(h is not None for h in human_norms) else None,
            "n": len([h for h in human_norms if h is not None]),
        },
        "alignment_with_human": {
            "n_paired": len(paired),
            "spearman_rho": _spearman(paired_xs, paired_ys),
            "pearson_r": _pearson(paired_xs, paired_ys),
            "mae": _mae(paired_xs, paired_ys),
        },
        "judgement_distribution": judgements,
        "triage_distribution": triages,
        "review_backend_distribution": backends,
        "confidence": {
            "mean": statistics.mean(confidences),
            "std": statistics.pstdev(confidences) if len(confidences) > 1 else 0.0,
        },
        "latency_s": {
            "mean": statistics.mean(latencies),
            "p95": sorted(latencies)[int(0.95 * (len(latencies) - 1))] if latencies else 0.0,
            "max": max(latencies),
        },
    }


def _row_meta(r: dict[str, Any]) -> dict[str, Any]:
    meta = r.get("metadata") or {}
    if not meta and "metadata_json" in r:
        try:
            meta = json.loads(r["metadata_json"])
        except Exception:
            meta = {}
    return meta


def _by_paper(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        slug = _row_meta(r).get("paper_slug", "?")
        grouped.setdefault(slug, []).append(r)
    return {slug: _summarize_run(items) for slug, items in grouped.items()}


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    rows = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=ETL_OUT / "experiment_baseline_result.jsonl")
    parser.add_argument("--new", type=Path, default=ETL_OUT / "experiment_new_result.jsonl")
    parser.add_argument("--output-json", type=Path, default=ETL_OUT / "experiment_analysis.json")
    args = parser.parse_args()

    baseline_rows = _load_jsonl(args.baseline)
    new_rows = _load_jsonl(args.new)

    payload = {
        "baseline": {
            "summary": _summarize_run(baseline_rows),
            "by_paper": _by_paper(baseline_rows),
        },
        "new": {
            "summary": _summarize_run(new_rows),
            "by_paper": _by_paper(new_rows),
        },
    }
    args.output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    print(f"Analysis written: {args.output_json}")
    # Quick stdout summary
    for label in ("baseline", "new"):
        s = payload[label]["summary"]
        if s.get("success_count", 0) == 0:
            print(f"{label}: NO SUCCESSFUL ROWS")
            continue
        print(f"{label}: success={s['success_count']}/{s['total']}, "
              f"reviewer_score mean={s['reviewer_score']['mean']:.3f}, "
              f"alignment ρ={s['alignment_with_human']['spearman_rho']}, "
              f"MAE={s['alignment_with_human']['mae']}, "
              f"latency mean={s['latency_s']['mean']:.1f}s")


if __name__ == "__main__":
    main()
