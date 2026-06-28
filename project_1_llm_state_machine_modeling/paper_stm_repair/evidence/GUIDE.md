# evidence/GUIDE.md — 历史证据索引维护规范

## 1. 任务边界

`evidence/` 只维护历史审计与证据索引：上游事实等级、旧资产继承、候选矩阵、artifact 可获取性、分支局部追踪和 R1 strict seed 调研口径。

本目录不做：

1. 不冻结当前 seed 样本。
2. 不维护当前 repair baseline 事实总账。
3. 不维护当前 NL dataset 总账。
4. 不定义正式实验协议、eligibility、metric 或 run record schema。
5. 不把旧 generation-era baseline 改名成本文当前 repair baseline。

## 2. 当前事实源跳转规则

| 问题 | 应读取 | evidence 中可参考 |
|---|---|---|
| seed 候选是否当前有效 | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) | [audits/strict_seed_literature_survey.md](./audits/strict_seed_literature_survey.md)、[matrices/baseline_candidate_matrix.md](./matrices/baseline_candidate_matrix.md) |
| repair baseline 是否当前可用 | [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md) | [audits/baseline_asset_audit.md](./audits/baseline_asset_audit.md) |
| 纯 NL source 是否可用 | [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md) | [ledgers/source_coverage_ledger.md](./ledgers/source_coverage_ledger.md) |
| 旧分支事实能否引用 | 当前落盘文件 + PR 链接 | [traces/branch_asset_trace.md](./traces/branch_asset_trace.md) |

## 3. 子路径放置规则

1. `ledgers/`：放事实等级、覆盖率、可获取性、继承边界等 ledger；禁止放当前实验统计。
2. `audits/`：放审计报告、筛选口径、候选资格定义；禁止直接替代 corpus registry。
3. `matrices/`：放候选矩阵、格式转换矩阵；矩阵只能解释风险和候选角色。
4. `traces/`：放分支、PR、旧资产消费路径；不得复制未合入分支的大量内容。

## 4. 更新要求

1. 新增或移动文件时同步更新 [README.md](./README.md) 与 [SUMMARY.md](./SUMMARY.md) 的文件总账。
2. 若历史事实被新的 corpus 总账覆盖，应在本目录标注“已由某事实源覆盖”，不要删除旧审计痕迹。
3. 外部链接只作为历史证据线索；若用于当前实验，必须在对应 corpus / protocol 中重新核验。
4. 引用本目录材料写论文时，默认写作“historical audit / evidence index / screening rationale”，不要写成 current result。
