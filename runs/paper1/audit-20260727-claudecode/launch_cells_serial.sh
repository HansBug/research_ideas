#!/usr/bin/env bash
# Launch Discover cells with a bounded number in flight.
#
# The original launcher backgrounded all eight at once.  Each cell spawns FBMCQ
# children of its own, so the real process count is a multiple of that, and the
# machine went into swap.  A cell takes tens of minutes whether or not seven
# siblings are competing for memory, so the wall-clock cost of a cap is small and
# the failure mode it removes -- an OOM kill mid-run, which leaves a partial
# record indistinguishable from a model that produced nothing -- is expensive.
#
# Usage: launch_cells_serial.sh <out_dir> <max_parallel> <pair...>
set -u
REPO=/home/zhangshaoang/oo-projects/research_ideas
FL="$REPO/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop"
# Resolve before the `cd` below: a relative out-dir silently pointed at
# $FL/runs/... after the chdir, the log redirections failed, and every cell
# exited instantly with "no such file or directory" while the launcher happily
# reported "launched".
OUT="$(readlink -m "$1")"; shift
MAX="$1"; shift
PAIRS=("$@")

set -a; source "$REPO/.env"; set +a
mkdir -p "$OUT"
cd "$FL" || exit 1

launch() {
  local pair="$1" prof="$2" short="$3"
  PYTHONPATH="$FL/src:$REPO" nohup "$REPO/venv/bin/python" -u -m paper_stm_feedback_loop.discover \
    --pair-id "llms_emp_feedback_final_$pair" --profile "$prof" --content-language zh-CN \
    --output-dir "$OUT/$pair-$short" > "$OUT/$pair-$short.log" 2>&1 &
}

for pair in "${PAIRS[@]}"; do
  for spec in "gpt-5.5:gpt" "claude-opus-4-7:claude"; do
    prof="${spec%%:*}"; short="${spec##*:}"
    # Wait for a slot.  `jobs -rp` counts only this script's running children,
    # so an unrelated python process on the box does not stall the queue.
    while [ "$(jobs -rp | wc -l)" -ge "$MAX" ]; do sleep 20; done
    launch "$pair" "$prof" "$short"
    echo "launched $pair-$short ($(jobs -rp | wc -l) in flight)"
    sleep 5
  done
done

wait
echo "all cells finished into $OUT"
