# Paper1 当前状态

Paper1 当前冻结实验是 [v60/current 与 X1v2 baseline](./final_results/v60_current_vs_x1v2_baseline/README.md) 的同口径比较。当前方法、Judge、evaluation 的发布结构已拆分为独立包；最终实验运行代码仍由归档中的 immutable commit、run ID、资源 hash 与 protocol hash 标识，重构后的 HEAD 不冒充实际实验提交。

## 当前事实

| 项目 | 当前状态 | 证据入口 |
| --- | --- | --- |
| 主实验 | 54 pair、3 round、145 expected、435 round-level expected；v60/current 与 X1v2 baseline 同一 issue #195 Judge | [最终归档](./final_results/v60_current_vs_x1v2_baseline/README.md) |
| 方法 | typed evidence-discovery method；19 个冻结谓词只用于可执行证据，不是发现准入门 | [method/](./method/README.md) |
| Judge | issue #195 的两阶段 relation/validity 裁定，与方法隔离 | [judge/](./judge/README.md) |
| 评测 | provider-free 汇总 hit、precision、W-on-hits、K/N/I、predicate usage 与成本 | [evaluation/](./evaluation/README.md) |
| ledger | 当前唯一台账为 145 条 `ledger_v2` | [ledger_v2](./discover_matrix/ledger_v2/README.md) |
| 结构复现 | 内部 RC、clean-install、固定 15-pair 技术回归和审查材料已另行保存 | [release_validation/](./release_validation/README.md) |

当前 headline 是 current 的 overall FULL 306/435 = 70.34% 与 baseline 的 211/435 = 48.51%。其余指标、分母、成本资格和 W 定义不得从本页转述，应回到最终归档。X1v2 的 legacy 59.8%/70.3%/47.9% 来自不同 Judge 与网格，只作为历史材料保留。

## 不属于当前结论

v46、v27、v26 与旧 feedback-loop 是历史方法、旧判定或过程记录；它们不能作为 current method、current result 或默认复算入口。当前研究也不证明时钟、不变式、正交 region/并发、hybrid、无界时序、其他执行模型或其他 ledger 上的效果。历史材料和可比性边界见 [实验历史索引](./archive/experiment_history/README.md)。
