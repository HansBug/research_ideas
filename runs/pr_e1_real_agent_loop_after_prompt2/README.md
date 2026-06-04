# PR-E1 prompt-fix3 paired rerun evidence

本目录记录 PR-E1 在进一步补充 pyfcstm action-block / event-trigger prompt 约束之后的真实 paired rerun 证据。

- `SUMMARY.md`：本批汇总表、配置结论、失败模式与样本筛选建议。
- `summary.json`：机器可读汇总。
- `<run_id>/report.md`：单次运行报告，包含 NL 原文、中文翻译、最终 FCSTM、stage 表和 iteration 表。
- `<run_id>/<run_id>.agent_loop.json.gz`：真实 `AgentLoopRunRecord`。
- `<run_id>/checks.json`：schema / secret / eligibility 检查。
- `<run_id>/run_logs/`：runner 捕获的 `stdout.txt` / `stderr.txt`。
- `promptfix3-path2-default-runner.txt`：外层 runner 耗时记录。

边界：该批为真实 provider 调用；当前只补 Path2 default paired rerun，用于验证 promptfix3 是否把 Path2 从 parse failure 推进到 SD-4 design feedback。结果仍为 exploratory / diagnostic evidence，不构成正式 Path1/Path2 主实验指标。
