# evidence/ — 历史审计与证据索引入口

`evidence/` 只保存 R0/R1 以来形成的历史审计材料、上游证据索引、候选矩阵和分支追踪。它不是当前 corpus 事实真源，也不负责冻结 seed、repair baseline、NL dataset、转换器协议或主实验结果。

当前事实源必须回到：

| 需要判断什么 | 当前事实源 | evidence 中对应旧材料的角色 |
|---|---|---|
| `<NL, STM_0>` seed / seed library | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) | 只解释 R1 如何形成候选与筛选口径。 |
| STM repair baseline / near-neighbor | [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md) | 只保留 generation-era baseline 与旧近邻审计。 |
| 控制系统纯 NL 数据源 | [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md) | 只保留来源覆盖、可用性与历史统计线索。 |

## 1. 子路径

| 子路径 | 职责 | 入口 |
|---|---|---|
| [ledgers/](./ledgers/) | 上游事实、来源覆盖、artifact 可获取性和旧资产继承边界台账。 | [SUMMARY.md](./SUMMARY.md) |
| [audits/](./audits/) | R1 baseline / strict seed 审计口径和执行方案。 | [audits/baseline_asset_audit.md](./audits/baseline_asset_audit.md) |
| [matrices/](./matrices/) | 候选 baseline 与格式转换压力矩阵。 | [matrices/baseline_candidate_matrix.md](./matrices/baseline_candidate_matrix.md) |
| [traces/](./traces/) | 分支局部资产与消费决策追踪。 | [traces/branch_asset_trace.md](./traces/branch_asset_trace.md) |

## 2. 三件套

1. 本文件：说明 `evidence/` 的定位、边界和子路径。
2. [SUMMARY.md](./SUMMARY.md)：维护历史审计材料总账、当前事实源跳转和风险提示。
3. [GUIDE.md](./GUIDE.md)：规定后续如何读取、移动、补充或引用本目录材料。

## 3. 读取纪律

1. 需要冻结 R2 seed 时，回到 [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md)，不能直接从 [matrices/baseline_candidate_matrix.md](./matrices/baseline_candidate_matrix.md) 或 [audits/strict_seed_literature_survey.md](./audits/strict_seed_literature_survey.md) 选样本。
2. 需要判断 repair baseline 时，回到 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)，不能把旧 generation baseline 台账改写成当前 repair baseline 事实。
3. 需要控制系统 NL 数据源时，回到 [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md)，不能把只有 NL 的 source pool 提前计为 paired seed。
4. 本目录可以解释“为什么后来这样分工”，但不得替代 `corpora/`、`repair_baselines/`、`nl_datasets/` 的当前总账。
