#!/usr/bin/env bash
# v22: 11 pair × 2 model × 3 轮 = 66 格。失败自动重试直到落盘。
set -u
REPO=/home/zhangshaoang/oo-projects/research_ideas
FL="$REPO/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop"
CFG="$REPO/.llmconfig.yml"
BASE="${BASE:-$REPO/runs/paper1/matrix-v22}"
PAIRS=(0000 0006 0018 0029 0032 0035 0038 0043 0047 0048 0050)
MAX="${MAX:-8}"; MAXTRY=6
cd "$FL" || exit 1
one() {  # run pair profile short
  local run="$1" pair="$2" prof="$3" short="$4" out="$BASE/$run/$pair-$short"
  for i in $(seq 1 $MAXTRY); do
    [ -f "$out/discover-completed.json" ] && { echo "OK $run/$pair-$short (try $((i-1)))"; return 0; }
    [ -d "$out" ] && mv "$out" "$out.try$i" 2>/dev/null
    PYTHONPATH="$FL/src:$REPO" LLM_CONFIG_FILE="$CFG" \
      "$REPO/venv/bin/python" -u -m paper_stm_feedback_loop.discover \
      --pair-id "llms_emp_feedback_final_$pair" --profile "$prof" \
      --content-language zh-CN --llm-config "$CFG" --transport-retries 8 \
      --output-dir "$out" > "$BASE/$run/$pair-$short.log" 2>&1
    [ -f "$out/discover-completed.json" ] && { echo "OK $run/$pair-$short (try $i)"; return 0; }
    echo "RETRY $run/$pair-$short try$i: $(grep -oE 'Error code: [0-9]+|failed at [a-z_]+' "$BASE/$run/$pair-$short.log" | tail -1)"
    sleep 90
  done
  echo "EXHAUSTED $run/$pair-$short"
}
for run in run1 run2 run3; do
  mkdir -p "$BASE/$run"
  for pair in "${PAIRS[@]}"; do
    for spec in "claude-opus-4-7:claude" "gpt-5.5:gpt"; do
      while [ "$(jobs -rp | wc -l)" -ge "$MAX" ]; do sleep 10; done
      one "$run" "$pair" "${spec%%:*}" "${spec##*:}" &
      sleep 3
    done
  done
done
wait
echo "V22 ALL DONE"
for run in run1 run2 run3; do
  echo "  $run: $(ls $BASE/$run/*/discover-completed.json 2>/dev/null | wc -l)/22"
done
