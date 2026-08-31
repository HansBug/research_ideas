# Paper1 当前状态

Paper1 当前冻结实验是 [v60/current 与 X1v2 baseline](./final_results/v60_current_vs_x1v2_baseline/README.md) 的同口径比较。当前方法、人工裁定、evaluation 的发布结构已拆分为独立包；最终实验运行代码仍由归档中的 immutable commit、run ID、资源 hash 与 protocol hash 标识，重构后的 HEAD 不冒充实际实验提交。

## 当前事实

| 项目 | 当前状态 | 证据入口 |
| --- | --- | --- |
| 主实验 | 54 pair、3 round、145 条参考缺陷条目、435 个 round-level evaluation units；v60/current 与 X1v2 baseline 使用同一 issue #195 人工裁定口径 | [最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md) |
| 方法 | typed evidence-discovery method；19 个冻结谓词分为 Structure/Topology/Trajectory simulation/Bounded verification 四族；v60 实际执行 12 个 distinct predicate ID，8 个 distinct predicate ID 出现在 report-bound finding 中 | [method/](./method/README.md) 与 [v4 报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md) |
| 人工裁定 | issue #195 的两阶段 relation/validity 人工裁定，与方法隔离 | [judge/](./judge/README.md) |
| 评测 | provider-free 汇总 hit、precision、W-on-hits、K/N/I、predicate usage 与成本 | [evaluation/](./evaluation/README.md) |
| ledger | 当前唯一台账为 145 条 `ledger_v2` | [ledger_v2](./discover_matrix/ledger_v2/README.md) |
| 内部后端审计 | 145 条输入与 receipt 的 source-first 复核、四路 review、pane5 仲裁与离线复算均已保存；只用于 evaluation-only 能力检查，不进入 paper1 主叙事或 method routing | [内部谓词后端审计](./discover_matrix/ledger_v2/predicate_gold_v1/README.md) |
| 结构复现 | 内部 RC、clean-install、固定 15-pair 技术回归和审查材料已另行保存 | [release_validation/](./release_validation/README.md) |

当前 headline 以 [v4 公平对照报告](./final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md) 为准：current 的 overall FULL 为 310/435 = 71.26%，X1v2 baseline v3 为 227/435 = 52.18%；report precision 分别为 980/1271 = 77.10% 和 417/512 = 81.45%。其余指标、分母、成本资格和 W 定义回到最终归档的 v4 comparison layer。历史人工裁定记录与旧网格数字只保留在 archive/history，不进入当前主结果。

## 不属于当前结论

v46、v27、v26 与旧 feedback-loop 是历史方法、旧判定或过程记录；它们不能作为 current method、current result 或默认复算入口。当前研究也不证明时钟、不变式、正交 region/并发、hybrid、无界时序、其他执行模型或其他 ledger 上的效果。历史材料和可比性边界见 [实验历史索引](./archive/experiment_history/README.md)。
