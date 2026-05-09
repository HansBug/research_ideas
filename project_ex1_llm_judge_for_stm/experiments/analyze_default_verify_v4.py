"""V4 verify: 5 reps of default config (rubric+iter_b on / strict-llm / airouter / max_workers=12 + retries=8).

Reads:
  experiments/out/phase14_combined/migration_verify/default_airouter_strict_rep{1..5}.json

Compares to:
  experiments/out/phase14_combined/week3_noise/noise_n1_w15_rep{1..5}.json
  (W3 N1 = rubric+iter_b on / NO strict-llm / miaocg-first / max_workers=6 + retries=0)

Output: console + default_verify_v4_summary.json

Run:
  python -m project_ex1_llm_judge_for_stm.experiments.analyze_default_verify_v4
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

CORPUS_ROOT = Path(__file__).resolve().parent.parent
OUT = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "migration_verify"
W3_DIR = CORPUS_ROOT / "etl" / "out" / "phase14_combined" / "week3_noise"

V4_REPS = [OUT / f"default_airouter_strict_rep{k}.json" for k in range(1, 6)]
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
    new_existing = [p for p in V4_REPS if p.exists()]
    w3_existing = [p for p in W3_REPS if p.exists()]
    if not new_existing:
        raise SystemExit(f"missing default_airouter_strict_rep*.json in {OUT}")
    if not w3_existing:
        raise SystemExit(f"missing noise_n1_w15_rep*.json in {W3_DIR}")

    new_reps = [json.loads(p.read_text()) for p in new_existing]
    w3_reps = [json.loads(p.read_text()) for p in w3_existing]

    new_stats = _stats(new_reps)
    w3_stats = _stats(w3_reps)

    print("= V4 default-config (airouter strict-llm, retries=8, max_workers=12) vs W3 N1 (miaocg, no strict)")
    print(f"  V4 reps: {len(new_existing)} | W3 reps: {len(w3_existing)}")
    print()
    print(f"{'metric':<22}{'V4 mean ± σ':>22}{'W3 N1 mean ± σ':>22}{'ΔMean':>10}{'σ-ratio (V4/W3)':>18}")
    print("-" * 94)
    for label, _ in METRICS:
        n = new_stats.get(label)
        w = w3_stats.get(label)
        if not n or not w:
            continue
        delta = n["mean"] - w["mean"]
        sigma_ratio = (n["std"] / w["std"]) if w["std"] > 0 else float("inf") if n["std"] > 0 else 1.0
        print(f"{label:<22}  {n['mean']:>7.3f} ± {n['std']:<6.3f}  {w['mean']:>7.3f} ± {w['std']:<6.3f}{delta:>+10.3f}{sigma_ratio:>18.2f}x")

    out_json = OUT / "default_verify_v4_summary.json"
    out_json.write_text(json.dumps({
        "v4_default_strict_5reps": {label: n for label, n in new_stats.items()},
        "w3_n1_baseline_5reps": {label: w for label, w in w3_stats.items()},
        "v4_config": {
            "rubric": True, "iter_b": True, "iter_a": False, "iter_c": None,
            "provider_chain": ["airouter"], "max_workers": 12, "strict_llm": True,
            "max_retries": 8, "timeout_per_attempt_s": 60,
            "checkpoint_dir": "per-rep",
        },
        "w3_n1_config": {
            "rubric": True, "iter_b": True,
            "provider_chain": ["miaocg", "deepghs", "findcg", "api68886868"],
            "max_workers": 6, "strict_llm": False, "max_retries": 0,
        },
    }, ensure_ascii=False, indent=2, default=str))
    print(f"\nsummary JSON written: {out_json}")


if __name__ == "__main__":
    main()
