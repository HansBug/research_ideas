# X1v2 历史 Judge 结果（已替代）

本文件保存的是 ledger_v2 形成时期的 X1v2 历史命中表，不是当前 baseline 结果。它曾报告 `hit@1 59.8%`、`hit@3 70.3%`、`hit@all 47.9%`；这些数字使用旧 Judge、两个生成模型臂和不同网格，不能与当前方法结果或当前 X1v2 baseline 相减、排名或作为论文 headline。

当前唯一有效的 X1v2 baseline 结果见 [v4 公平对照层](../../final_results/v60_current_vs_x1v2_baseline/derived/fair_comparison_v4/README.md)：在与 v60/current 相同的 54 pair、3 round、145 expected issue、435 expected-round units 上，baseline v3 的 overall FULL 为 227/435 = 52.18%，L2 FULL 为 50/117 = 42.74%，hit@3 为 106/145 = 73.10%，hit@all 为 46/145 = 31.72%，report precision 为 417/512 = 81.45%。旧 Judge/网格数字只留作历史资料，不是当前比较口径。

本页保留的理由是 provenance：它可以解释 ledger 形成时期曾采用的历史基线网格，不能复算或替代当前结果。X1v2 的 current W 审计也在最终归档中：512 条 finding 的 finding-level W0/W1/W2 为 1/511/0；W 与谓词体系不绑定，而 X1v2 predicate usage 仍不适用。
