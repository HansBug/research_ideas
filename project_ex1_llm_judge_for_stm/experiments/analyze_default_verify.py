"""Verify the default config (rubric+iter_b) reproduces W3 N1's distribution.

Reads:
  experiments/out/phase14_combined/migration_verify/default_w15style_rep{1..5}.json
Compares to:
  experiments/out/phase14_combined/week3_noise/noise_n1_w15_rep{1..5}.json (the W3 N1 reference)

Output: console + optional JSON dump

Run:
  python -m project_ex1_llm_judge_for_stm.experiments.analyze_default_verify
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

CORPUS_ROOT = Path(__file__).resolve().parent.parent
NEW_DIR = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "migration_verify"
W3_DIR = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "week3_noise"

NEW_REPS = [NEW_DIR / f"default_w15style_rep{k}.json" for k in range(1, 6)]
W3_REPS = [W3_DIR / f"noise_n1_w15_rep{k}.json" for k in range(1, 6)]

METRICS = [
    ("HAI", "HAI"),
    ("HAI_legacy", "HAI_legacy"),
    ("RAS", "record_metrics.RAS"),
    ("SAS", "summary_metrics.SAS"),
    ("CRAS", "component_metrics.CRAS"),
    ("PDS", "protocol_metrics.PDS"),
    ("record_ScoreAlign", "record_metrics.ScoreAlign"),
    ("record_Calib", "record_metrics.Calib"),
    ("record_ReasonAlign", "record_metrics.ReasonAlign"),
    ("record_EquivAlign", "record_metrics.EquivAlign"),
    ("summary_ScoreAlign", "summary_metrics.ScoreAlign"),
    ("summary_RankAlign", "summary_metrics.RankAlign"),
    ("summary_Spearman", "summary_metrics.spearman_rho"),
    ("summary_EvDisc", "summary_metrics.EvidenceDiscipline"),
    ("summary_Stability", "summary_metrics.Stability"),
    ("weighted_kappa", "judgement_metrics.weighted_kappa"),
]


def _resolve(d, dotted):
    cur = d
    for p in dotted.split("."):
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur if isinstance(cur, (int, float)) else None


def _stats(reps):
    out = {}
    for label, dotted in METRICS:
        vals = [_resolve(r, dotted) for r in reps]
        vals = [v for v in vals if v is not None]
        if not vals:
            continue
        out[label] = {
            "values": vals,
            "mean": statistics.mean(vals),
            "std": statistics.pstdev(vals) if len(vals) > 1 else 0.0,
            "min": min(vals),
            "max": max(vals),
            "n": len(vals),
        }
    return out


def main() -> None:
    new_existing = [p for p in NEW_REPS if p.exists()]
    w3_existing = [p for p in W3_REPS if p.exists()]
    if not new_existing:
        raise SystemExit(f"missing default_w15style_rep*.json in {NEW_DIR}")
    if not w3_existing:
        raise SystemExit(f"missing noise_n1_w15_rep*.json in {W3_DIR}")

    new_reps = [json.loads(p.read_text()) for p in new_existing]
    w3_reps = [json.loads(p.read_text()) for p in w3_existing]

    new_stats = _stats(new_reps)
    w3_stats = _stats(w3_reps)

    print(f"= NEW default-config (project_ex1) vs W3 N1 (PR #6 archive) — both rubric+iter_b 62-task")
    print(f"  NEW reps: {len(new_existing)} | W3 reps: {len(w3_existing)}")
    print()
    print(f"{'metric':<22}{'NEW mean ± σ':>22}{'W3 mean ± σ':>22}{'ΔMean':>10}{'σ-ratio (N/W3)':>18}{'within ±2σ_W3':>18}")
    print("-" * 112)
    n_within = 0
    n_total = 0
    for label, _ in METRICS:
        n = new_stats.get(label)
        w = w3_stats.get(label)
        if not n or not w:
            continue
        delta = n["mean"] - w["mean"]
        sigma_ratio = (n["std"] / w["std"]) if w["std"] > 0 else float("inf") if n["std"] > 0 else 1.0
        within_2sig_w3 = abs(delta) <= 2 * max(w["std"], 0.001)
        n_total += 1
        if within_2sig_w3:
            n_within += 1
        marker = "✓" if within_2sig_w3 else "✗"
        print(f"{label:<22}  {n['mean']:>7.3f} ± {n['std']:<6.3f}  {w['mean']:>7.3f} ± {w['std']:<6.3f}{delta:>+10.3f}{sigma_ratio:>18.2f}x{marker:>18}")

    print()
    print(f"= 一致性总结：{n_within}/{n_total} metric 落在 W3 N1 ±2σ 内")

    # Save JSON
    out_json = NEW_DIR / "default_verify_summary.json"
    out_json.write_text(json.dumps({
        "new_default_config_5reps": {label: n for label, n in new_stats.items()},
        "w3_n1_baseline_5reps": {label: w for label, w in w3_stats.items()},
        "consistency": {
            "n_within_2std_w3": n_within,
            "n_total_metrics": n_total,
            "ratio": f"{n_within}/{n_total}",
        },
    }, ensure_ascii=False, indent=2, default=str))
    print(f"\nsummary JSON written: {out_json}")


if __name__ == "__main__":
    main()
