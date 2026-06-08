output_dir: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs`

status: `success`

final_model: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/final_model.fcstm`

report: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/report.md`

metadata: `runs/codex_exec_skill/pr_m3_four_20260608_122318/path1_abs/metadata.json`

主要限制: single self-assessment，无独立 reviewer/人工签核；模型只覆盖离散三态 ABS 监督器，不覆盖 PID、液压/车辆连续动力学；部分中间态场景使用 `runtime_hotstart_surrogate`，但已记录 reachable prefix 和外部输入 ledger。