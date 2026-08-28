# Paper STM Evaluation

`paper-stm-evaluation` 只负责 provider-free 的评测和报告：它读取已经完成的 method 与 Judge 制品、ledger 和冻结参考数据，计算并验证跨 arm 指标。method 和 Judge 都不 import evaluation；evaluation 不参与发现、predicate 执行或 Semantic Judge 判定。

## 指标所有权

| 指标 | 含义与分母 |
| --- | --- |
| hit@1 / overall FULL | round-level expected row 的 `FULL` 数，当前主宇宙为 435 行 |
| hit@3 | 每条 expected 在 3 个 round 中至少一次 `FULL`，分母 145 |
| hit@all | 每条 expected 在 3 个 round 中均为 `FULL`，分母 145 |
| L2 | 仅 ledger 的 L2 expected；当前分母分别为 117 round-level row 或 39 expected |
| semantic precision | `VALID_KNOWN + VALID_NOVEL` 除以全部 report；`INVALID` 才是 semantic FP |
| K/N/I | report-level 与 root-cause cluster-level 的 `VALID_KNOWN`、`VALID_NOVEL`、`INVALID` 汇总 |
| W-on-hits | 对每条 `FULL` expected 聚合其 supporting report 的最高 W；分母是 FULL hits，不是 finding 数 |
| predicate usage | 当前计划谓词集合中实际 terminal receipt 的覆盖；不等于 candidate、W2 或 report 数 |
| cost | method/Judge 调用、token、cache、retry 与 cost eligibility；缺少可定价 usage 时不以估算值补齐 |

W 不依赖 19 谓词体系。X1v2 的 predicate usage 不适用，但其 W 来自 512 条冻结 finding 的两轮独立逐条审计；evaluation 将此 finding-level 结果按冻结 `full_report_ids` 聚合为 hit-level max-W。

## 最终归档复算

权威入口是 `paper_stm_evaluation.final_results_archive`。该命令只读归档并核查 schema、映射、hash、链接和离线复算，不调用 provider，也不依赖未跟踪 `runs/`。

```bash
PYTHONPATH=project_1_llm_state_machine_modeling/paper_stm_issue_discover/evaluation/src:project_1_llm_state_machine_modeling/paper_stm_issue_discover \
venv/bin/python -m paper_stm_evaluation.final_results_archive validate \
  --archive-root project_1_llm_state_machine_modeling/paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline
```

当前结论和机器可读汇总在 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md)。`pipeline.evidence_discovery.reporting.final_results_archive` 仅是兼容入口，不是新的 evaluation 所有权。
