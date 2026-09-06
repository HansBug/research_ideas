# Paper1 当前状态

Paper1 当前冻结实验是 [v61 与 X1v2 baseline](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 的同口径比较（两臂由同一校准语义 judge 判定；[v60 人工评测归档](./final_results/v60_current_vs_x1v2_baseline/README.md)只作仪器校准参照）。当前方法、人工裁定、evaluation 的发布结构已拆分为独立包；最终实验运行代码仍由归档中的 immutable commit、run ID、资源 hash 与 protocol hash 标识，重构后的 HEAD 不冒充实际实验提交。

## 当前事实

| 项目 | 当前状态 | 证据入口 |
| --- | --- | --- |
| 主实验 | 54 pair、3 round、145 条参考缺陷条目、435 个 round-level evaluation units；v61 与 X1v2 baseline 由同一台按 issue #195 人工裁定协议校准的语义 judge 判定 | [v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) |
| 方法 | typed evidence-discovery method；19 个冻结谓词分为 Structure/Topology/Trajectory simulation/Bounded verification 四族；v61 有 12 个 distinct predicate ID 产生终止回执，8 个绑定到最终报告，7 个绑定到有效报告 | [method/](./method/README.md) 与 [v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) |
| 人工裁定 | issue #195 的两阶段 relation/validity 人工裁定，与方法隔离 | [judge/](./judge/README.md) |
| 评测 | provider-free 汇总 hit、precision、W-on-hits、K/N/I、predicate usage 与成本 | [evaluation/](./evaluation/README.md) |
| ledger | 当前唯一台账为 145 条 `ledger_v2` | [ledger_v2](./discover_matrix/ledger_v2/README.md) |
| 内部后端审计 | 145 条输入与 receipt 的 source-first 复核、四路 review、pane5 仲裁与离线复算均已保存；只用于 evaluation-only 能力检查，不进入 paper1 主叙事或 method routing | [内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) |
| 结构复现 | 内部 RC、clean-install、固定 15-pair 技术回归和审查材料已另行保存 | [release_validation/](./release_validation/README.md) |

当前 headline 以 [v61 归档](./final_results/v61_source_divergence_vs_x1v2_baseline/README.md) 的 `derived/evaluate_rq3_output.txt` 为准：v61 的 overall FULL `hit@1` 为 323/435 = 74.25%，X1v2 baseline 为 225/435 = 51.72%；report precision 分别为 759/903 = 84.05% 和 427/512 = 83.40%（两臂同一校准语义 judge，方法侧尚无人工复核）。其余指标、分母、成分与限制见大纲 [story/paper_outline.md](./story/paper_outline.md) 与 [结果处置清单](./story/paper_result_inventory.md)。

## 不属于当前结论

v46、v27、v26 与旧 feedback-loop 是历史方法、旧判定或过程记录；它们不能作为 current method、current result 或默认复算入口。当前研究也不证明时钟、不变式、正交 region/并发、hybrid、无界时序、其他执行模型或其他 ledger 上的效果。历史材料和可比性边界见 [实验历史索引](./archive/experiment_history/README.md)。
