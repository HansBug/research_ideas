#!/usr/bin/env bash
# <grid> pair × 2 model（claude-opus-4-7 + gpt-5.5）× 3 轮。失败自动重试直到落盘。
# 格数不硬编码：8 格诊断与 54 格全量走同一个脚本，`CORPUS=1` 切到全语料。
# 格集从盘上读（run_grid.py），不在本文件里维护第二份。
set -u
REPO=/home/zhangshaoang/oo-projects/research_ideas
FL="$REPO/project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop"
CFG="$REPO/.llmconfig.yml"
BASE="${BASE:-$REPO/runs/paper1/matrix-v22}"
# The grid is read from disk, not typed. A literal here was wrong once already -- it carried
# `0058`, which has never been in the grid, and the resulting count went into a document that
# claims to be pre-registered. See `run_grid.py`.
# `CORPUS=1` 取全语料（54 pair）。它是**显式**来源，不进 run_grid 的自动优先级 —— 见该模块
# docstring：把语料放进自动链，会让一个没有 runs 的 checkout 静默宣称全语料就是格集。
RG="$REPO/project_1_llm_state_machine_modeling/eval/discover_matrix/run_grid.py"
read -r -a PAIRS <<< "$("$REPO/venv/bin/python" "$RG" ${CORPUS:+--corpus} ${GRID:+--grid "$GRID"})"
[ "${#PAIRS[@]}" -gt 0 ] || { echo "refusing to run: could not determine the grid" >&2; exit 1; }
echo "grid: ${#PAIRS[@]} pairs -- ${PAIRS[*]}"
echo "grid source: $("$REPO/venv/bin/python" "$RG" ${CORPUS:+--corpus} ${GRID:+--grid "$GRID"} --source)"
MAX="${MAX:-8}"; MAXTRY=6

# ── 开跑前置闸：代码版本必须可追溯 ───────────────────────────────────────────────
# `full_tables.py` 已经会在缺 `CODE_VERSION.txt` 时警告「该代次只能靠时间戳反推代码版本」，
# 但此前没有任何东西保证它被写 —— v22/v23 就都只有事后反推件。写在这里，忘不掉。
#
# 同时拒绝在脏工作区或有未推送提交时开跑：CLAUDE.md §3.5.1 的理由不是备份而是**可追溯性** ——
# 运行记录里没有代码版本字段，一次运行归属于哪个 commit 只能靠时间戳反推，而若那个 commit 还在
# 本地，别人无法核对，而这正是审查「实验是否公平」时最先要查的东西。
if [ "${SKIP_VERSION_GATE:-0}" != "1" ]; then
  DIRTY="$(cd "$REPO" && git status --porcelain -- \
    "project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src")"
  if [ -n "$DIRTY" ]; then
    echo "refusing to run: pipeline src 有未提交改动 —— 该次运行将无法归属到某个 commit" >&2
    echo "$DIRTY" >&2; exit 1
  fi
  UNPUSHED="$(cd "$REPO" && git log --oneline '@{u}..HEAD' 2>/dev/null | wc -l)"
  if [ "$UNPUSHED" != "0" ]; then
    echo "refusing to run: 有 $UNPUSHED 个未推送提交 —— 别人无法核对本次运行的代码版本" >&2; exit 1
  fi
fi
mkdir -p "$BASE"
{
  cd "$REPO" || exit 1
  echo "commit: $(git rev-parse HEAD)"
  echo "branch: $(git rev-parse --abbrev-ref HEAD)"
  echo "written_before_launch: yes"
  echo "pipeline_src_diff_vs_commit: $(git status --porcelain -- \
    project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/feedback_loop/src | wc -l) files"
} > "$BASE/CODE_VERSION.txt"
echo "code version -> $BASE/CODE_VERSION.txt: $(head -1 "$BASE/CODE_VERSION.txt")"
# 格集也要在开跑**前**写下，理由与代码版本相同但故障形态更隐蔽：目录是逐格创建的，所以
# `run_grid.from_runs()` 的目录清点在运行**期间**给出残缺格集，且看起来完全正常。实测 v36 开跑
# 30 秒后无参调用返回 4 个 pair 而不是 8；跑 324 格时这个窗口有 9 到 11 小时，运行期做测量的
# 脚本会拿到错的分母。`from_runs` 优先读这份文件。
printf '%s\n' "${PAIRS[*]}" > "$BASE/GRID.txt"
echo "grid -> $BASE/GRID.txt (${#PAIRS[@]} pairs)"
# 墙钟只能在这里记。`node_elapsed_ms_sum` 是各节点耗时**串行累加**（某格 800 秒），而格是并发
# 跑的：48 格累加约 8.25 小时，MAX=8 下实际墙钟 1.61 小时 —— 差 5 倍。报「跑完要多久」必须用墙钟，
# 而事后无从复原，所以写在这里。`matrix_cost.py` 缺这份文件时会明确说缺，不用累加值冒充。
WALL_START_EPOCH=$SECONDS
{
  echo "started_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "max_concurrency: $MAX"
  echo "cells_planned: $(( ${#PAIRS[@]} * 6 ))"
} > "$BASE/WALLCLOCK.txt"
# ──────────────────────────────────────────────────────────────────────────────

cd "$FL" || exit 1
one() {  # run pair profile short
  # Split, not one `local`. Under `set -u`, `local a="$1" b="$a"` fails: `local` declares every
  # named variable first (unset), then assigns left to right, so the right-hand side of `b` sees
  # `a` as declared-but-unset. Without `set -u` it expands to empty instead -- equally wrong, and
  # silent. As written before this, every one of the 66 cells wrote to `//` and produced nothing,
  # while the launcher printed `0/22` and exited 0. Caught by a stub run, not by reading.
  local run="$1" pair="$2" prof="$3" short="$4"
  local out="$BASE/$run/$pair-$short"
  for i in $(seq 1 $MAXTRY); do
    [ -f "$out/discover-completed.json" ] && { echo "OK $run/$pair-$short (try $((i-1)))"; return 0; }
    # ⚠️ `.try$i` 的编号有 off-by-one：`i` 是循环计数器，i=1 时目录尚不存在、mv 静默失败，
    # i=2 时才把**第一次**尝试的产物移过去 —— 所以 **`.try2` 装的是第一次尝试的残留**。
    #
    # **不改这个名字，故意的。** 至少 6 个工具（anchor_shift / count_refusals /
    # generation_history / check_model_drift / blind_resample / round_variance）按 `"try"` 匹配来
    # 排除作废目录。改成 `.attempt` 会让它们把作废目录当成正常格计入，症状是「格数变多、指标被
    # 失败运行的中间产物污染」，**且没有任何报错**。
    #
    # 收益/风险不成比例：off-by-one 的代价是「读 `.try2` 时要记得它装的是第一次尝试」，一句注释
    # 就能解决；改名的代价是 6 处匹配逻辑，每一处漏改都是静默污染。
    #
    # 若将来要改：**先给所有工具引入一个共享的「是否为作废目录」判定函数，再改名** —— 不是先改名
    # 再追着修。
    [ -d "$out" ] && mv "$out" "$out.try$i" 2>/dev/null
    # L-1 修：`>>` 而非 `>`，并写一行分隔。首版用 `>` 覆盖日志，于是**造成重试的那次失败的
    # stderr 不可恢复** —— 实测某格日志只剩 1 行。救回来的唯一原因是 run record 独立于日志写盘，
    # 但两者失效模式不同：日志覆盖 run record 尚未落盘的那一段（例如进程在写 record 之前就被
    # provider 断开）。
    echo "=== attempt $i at $(date -u +%Y-%m-%dT%H:%M:%SZ) ===" >> "$BASE/$run/$pair-$short.log"
    PYTHONPATH="$FL/src:$REPO" LLM_CONFIG_FILE="$CFG" \
      "$REPO/venv/bin/python" -u -m paper_stm_feedback_loop.discover \
      --pair-id "llms_emp_feedback_final_$pair" --profile "$prof" \
      --content-language zh-CN --llm-config "$CFG" --transport-retries 8 \
      --output-dir "$out" >> "$BASE/$run/$pair-$short.log" 2>&1
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
ELAPSED=$(( SECONDS - WALL_START_EPOCH ))
{
  echo "finished_at: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "elapsed: $(( ELAPSED / 3600 ))h$(( ELAPSED % 3600 / 60 ))m$(( ELAPSED % 60 ))s"
  echo "elapsed_seconds: $ELAPSED"
  echo "cells_landed: $(ls "$BASE"/run*/*/discover-completed.json 2>/dev/null | wc -l)"
} >> "$BASE/WALLCLOCK.txt"
echo "MATRIX ALL DONE (${#PAIRS[@]} pairs x 2 arms x 3 rounds = $(( ${#PAIRS[@]} * 6 )) cells)"
echo "wallclock -> $BASE/WALLCLOCK.txt"
for run in run1 run2 run3; do
  echo "  $run: $(ls $BASE/$run/*/discover-completed.json 2>/dev/null | wc -l)/$(( ${#PAIRS[@]} * 2 ))"
done
