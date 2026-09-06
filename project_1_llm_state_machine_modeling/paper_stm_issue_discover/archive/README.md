# Paper1 历史归档

本目录保存已经脱离当前主线的代码、实验材料、协议快照和写作草案。它们用于追溯和必要时的历史复现，不承担当前方法、当前结果或默认入口的职责。当前论文结果只以 [v60/current 与 X1v2 baseline 最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md) 为准。

[实验历史索引](./experiment_history/README.md) 是版本迭代的唯一入口，集中说明 v46、v27-stream、v60 与 X1v2 comparison arm 的来源、结果、可比性和保留材料。不要直接从历史快照提取 current headline。

| 归档路径 | 内容与使用边界 |
| --- | --- |
| [experiment_history/](./experiment_history/README.md) | 重要实验代次、可比性说明与历史 raw ZIP inventory |
| [r10_ledger_v1_and_v46/](./r10_ledger_v1_and_v46/README.md) | 第一版 ledger 与 v46 的已跟踪原始审计；仅作历史复核 |
| [legacy/feedback_loop/](./legacy/feedback_loop/README.md) | 已停用的 feedback-loop 实现；不在当前 method 发布包或默认运行路径中 |
| [r7_issue_lifecycle_scaffold/](./r7_issue_lifecycle_scaffold/README.md) | 早期 lifecycle 协议和 fixture；仅保留设计 provenance |
| [r8_story_pre_rebuild/](./r8_story_pre_rebuild/README.md) | 旧论文叙事草案；不得作为现行贡献或实验事实来源 |
| [r9_agent_loop_pipeline/](./r9_agent_loop_pipeline/ARCHIVE_README.md) | 旧单 Agent discover 实现；仅供历史复活 |
| [r1_5_to_r1_7_seed_corpus_snapshot/](./r1_5_to_r1_7_seed_corpus_snapshot/README.md) 与 [r5_7_better_stm_snapshot/](./r5_7_better_stm_snapshot/README.md) | 早期语料、评价路线和快照材料 |

归档文件保持其冻结语境。需要引用当前事实时，应链接现行方法、Judge、evaluation 或最终归档，而不是把历史描述改写成当前机制。
