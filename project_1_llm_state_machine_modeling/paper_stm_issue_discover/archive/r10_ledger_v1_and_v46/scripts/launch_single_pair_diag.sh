#!/usr/bin/env bash
# 单 pair 诊断运行，**带重试**，保证分母是请求的轮数而不是「碰巧落盘的轮数」。
#
# ⚠️ 这个脚本存在的理由：早先的诊断我直接 nohup 起三个进程、没有重试，于是崩掉的那轮没有
# `discover-completed.json`，我就用「已落盘轮」当分母报成 `2/2`。**那等于把丢格从分母里悄悄去掉** ——
# 崩溃轮本该计为未命中，否则一个越容易崩的改动看起来越好。
#
# 正式矩阵启动器 `launch_v22_matrix.sh` 一直有 `MAXTRY=6`；诊断脚本漏了它。
#
# 用法: launch_single_pair_diag.sh <out_dir> <pair> <profile> <rounds> [max_try]
set -u
REPO=/home/zhangshaoang/oo-projects/research_ideas
FL="$REPO/project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/feedback_loop"
OUT="$(readlink -m "$1")"; PAIR="$2"; PROFILE="$3"; ROUNDS="${4:-3}"; MAXTRY="${5:-6}"
SHORT="${PROFILE%%-*}"

mkdir -p "$OUT"
{
  cd "$REPO" || exit 1
  echo "commit: $(git rev-parse HEAD)"
  echo "pair: $PAIR | profile: $PROFILE | rounds: $ROUNDS | max_try: $MAXTRY"
  echo "written_before_launch: yes"
} > "$OUT/CODE_VERSION.txt"

cd "$FL" || exit 1
one() {
  local r="$1" out="$OUT/run$r/$PAIR-$SHORT"
  for i in $(seq 1 "$MAXTRY"); do
    [ -f "$out/discover-completed.json" ] && { echo "OK run$r (try $((i-1)))"; return 0; }
    # 保留失败的产物用于审计：崩因本身是数据（哪些门/协议在薄 NL 上更容易触发）。
    [ -d "$out" ] && mv "$out" "$out.try$i" 2>/dev/null
    PYTHONPATH="$FL/src:$REPO" "$REPO/venv/bin/python" -u -m paper_stm_feedback_loop.discover \
      --pair-id "llms_emp_feedback_final_$PAIR" --profile "$PROFILE" --content-language zh-CN \
      --output-dir "$out" > "$OUT/run$r-$PAIR-$SHORT.try$i.log" 2>&1
  done
  [ -f "$out/discover-completed.json" ] && { echo "OK run$r (try $MAXTRY)"; return 0; }
  # 耗尽重试才算真的丢格 —— 这一轮在报告里必须计为未命中，不得从分母剔除。
  echo "EXHAUSTED run$r after $MAXTRY tries" >&2
  return 1
}

for r in $(seq 1 "$ROUNDS"); do one "$r" & sleep 3; done
wait
echo "--- 落盘 $(ls "$OUT"/run*/"$PAIR-$SHORT"/discover-completed.json 2>/dev/null | wc -l) / $ROUNDS ---"
