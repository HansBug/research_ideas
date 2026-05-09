#!/usr/bin/env bash
# Week 3 noise-floor experiment suite.
# Runs 4 configs × 5 reps = 20 single-shot evaluations on the 62-task slice
# without SC aggregation, to measure baseline pipeline noise.
#
# Provider chain: miaocg-first (50-concurrent capacity) to absorb 4-parallel ×
# 6-worker = 24 concurrent calls without hitting airouter's 800/hr limit.
# This is a known confound vs original W0/W1/W1.5 single-shots which used
# airouter-first; documented in PR comment for traceability.
#
# Usage:
#   bash run_noise_floor_suite.sh
# Output:
#   etl/out/phase14_combined/week3_noise/noise_n{1,2,3,4}_*_rep{1..5}.json
#   etl/out/phase14_combined/week3_noise/log_n{1,2,3,4}_*_rep{1..5}.log

set -uo pipefail

cd "$(dirname "$0")/../../.."  # repo root

BASE=project_ex1_llm_judge_for_stm/experiments/out/phase14_combined
OUT=$BASE/week3_noise
mkdir -p "$OUT"

# Noise-rep provider chain: miaocg(50-concurrent) → deepghs(fast) → airouter(cheap) → findcg → api68886868
PROVIDER_CHAIN="miaocg deepghs airouter findcg api68886868"

# 62-task slice (matches W1.5/W2 production)
SLICE_ARGS="--record-limit 18 --summary-limit 16 --component-limit 24 --protocol-limit 4 --seed 7"

run_n1_w15() {
    # W1.5 B-only via standard ablation runner — replicates production baseline
    for K in 1 2 3 4 5; do
        LABEL="noise_n1_w15_rep${K}"
        python3 -m project_ex1_llm_judge_for_stm.experiments.run_ablation_config \
            --base-dir "$BASE" \
            $SLICE_ARGS \
            --rubric --iter-b \
            --provider-order $PROVIDER_CHAIN \
            --max-workers 6 \
            --config-label "$LABEL" \
            --output "$OUT/${LABEL}.json" \
            > "$OUT/${LABEL}.log" 2>&1
        echo "[N1] rep${K} done at $(date +%H:%M:%S)"
    done
}

run_n2_sc_n1() {
    # SC parallel pipeline with N=1, T=0+V1 — same nominal config as W1.5 but
    # via SC code path. Measures pipeline divergence vs N1.
    for K in 1 2 3 4 5; do
        LABEL="noise_n2_sc_n1_rep${K}"
        python3 -m project_ex1_llm_judge_for_stm.experiments.run_self_consistency_config \
            --base-dir "$BASE" \
            $SLICE_ARGS \
            --rubric --iter-b \
            --variance-source temp --n-reruns 1 \
            --provider-order $PROVIDER_CHAIN \
            --max-workers 6 \
            --checkpoint-dir "$OUT/checkpoints_n2_rep${K}" \
            --config-label "$LABEL" \
            --output "$OUT/${LABEL}.json" \
            > "$OUT/${LABEL}.log" 2>&1
        echo "[N2] rep${K} done at $(date +%H:%M:%S)"
    done
}

run_n3_w0() {
    # W0 LLM-mode auto (no rubric, no iter)
    for K in 1 2 3 4 5; do
        LABEL="noise_n3_w0_rep${K}"
        python3 -m project_ex1_llm_judge_for_stm.experiments.run_ablation_config \
            --base-dir "$BASE" \
            $SLICE_ARGS \
            --provider-order $PROVIDER_CHAIN \
            --max-workers 6 \
            --config-label "$LABEL" \
            --output "$OUT/${LABEL}.json" \
            > "$OUT/${LABEL}.log" 2>&1
        echo "[N3] rep${K} done at $(date +%H:%M:%S)"
    done
}

run_n4_w1_v0() {
    # W1 rubric v0 (rubric on, no iter)
    for K in 1 2 3 4 5; do
        LABEL="noise_n4_w1_rep${K}"
        python3 -m project_ex1_llm_judge_for_stm.experiments.run_ablation_config \
            --base-dir "$BASE" \
            $SLICE_ARGS \
            --rubric \
            --provider-order $PROVIDER_CHAIN \
            --max-workers 6 \
            --config-label "$LABEL" \
            --output "$OUT/${LABEL}.json" \
            > "$OUT/${LABEL}.log" 2>&1
        echo "[N4] rep${K} done at $(date +%H:%M:%S)"
    done
}

# Run 4 configs in parallel (each runs 5 reps sequentially internally)
echo "=== Noise floor suite started at $(date) ==="
run_n1_w15 &
PID_N1=$!
run_n2_sc_n1 &
PID_N2=$!
run_n3_w0 &
PID_N3=$!
run_n4_w1_v0 &
PID_N4=$!

echo "PIDs: N1=$PID_N1 N2=$PID_N2 N3=$PID_N3 N4=$PID_N4"
wait $PID_N1 $PID_N2 $PID_N3 $PID_N4
echo "=== Noise floor suite finished at $(date) ==="
