# PR-E1 baseline pre-fix real-run evidence

本目录记录 PR-E1 prompt 修正前的真实 baseline evidence，用作 paired rerun 的 before 侧对照。

- `SUMMARY.md` / `summary.json`：baseline 汇总。
- `<run_id>/report.md`：单次运行报告。
- `<run_id>/<run_id>.agent_loop.json.gz`：真实 AgentLoopRunRecord。
- `baseline0-default-runner.log`：本批 runner 外层耗时日志。

边界：该目录中的结果为修正前证据；后续推荐以 `runs/pr_e1_real_agent_loop_after_prompt/` 作为 after/micro-fix 证据目录。
