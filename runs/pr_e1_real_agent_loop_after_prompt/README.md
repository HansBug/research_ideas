# PR-E1 prompt-fix paired rerun evidence

本目录记录 PR-E1 在修正 pyfcstm grammar / SL-1 / SL-9 prompt 之后的真实 paired rerun 证据。

- `SUMMARY.md`：汇总表、配置结论、失败模式与样本筛选建议。
- `summary.json`：机器可读汇总。
- `<run_id>/report.md`：单次运行报告，包含 NL 原文、中文翻译、最终 FCSTM、stage 表和 iteration 表。
- `<run_id>/<run_id>.agent_loop.json.gz`：真实 AgentLoopRunRecord。
- `<run_id>/checks.json`：schema / secret / eligibility 检查。
- `<run_id>/run_logs/`：runner 捕获的 stdout / stderr。

边界：这些 run 均为真实 provider 调用；非 default 配置为显式 exploratory condition，不进入 Path1/Path2 主结果。
