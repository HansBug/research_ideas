output_dir: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator`

status: `valid_run_reviewer_queue`

final_model 路径: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/final_model.fcstm`

report 路径: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/report.md`

metadata 路径: `runs/codex_exec_skill/pr_m3_four_clean_20260608_133322/path1_elevator/metadata.json`

主要限制: NFRR 是 producer 自评，未人工/独立签核，final tier 被 cap 到 `T2`；`hbrg` 用 `int 0/1/2` 抽象原文位串且为 output-only waiver；未建模门控、排队调度、时间/FPGA 细节和未给出的优先级策略。