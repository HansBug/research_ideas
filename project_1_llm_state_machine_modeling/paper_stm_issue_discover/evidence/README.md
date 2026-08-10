# evidence/ — 历史审计与证据索引入口

> 🔴 **本目录不在当前运行路径上，全部内容是 R0/R1 时期的历史审计材料。**
> 它回答的是「当年为什么这样分工」，不回答「现在的事实是什么」。
>
> | 你想找 | 去哪 |
> | :-- | :-- |
> | 论文的实验证据链、台账、判定 | [../discover_matrix/](../discover_matrix/) |
> | 当前语料事实 | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) |
> | 当前方法实现 | [../pipeline/feedback_loop/](../pipeline/feedback_loop/) |
>
> ⚠️ **不要从本目录选样本、定 baseline 或引统计。** 这里的候选矩阵与筛选台账全部是 R1 口径，
> 已被 [../corpora/](../corpora/) 的三件套取代。
>
> 本目录只有 Markdown，**无代码、无测试、无机器事实源**。四个子目录各配 `README.md`：
> [ledgers/](./ledgers/)、[audits/](./audits/)、[matrices/](./matrices/)、[traces/](./traces/)。

`evidence/` 只保存 R0/R1 以来形成的历史审计材料、上游证据索引、候选矩阵和分支追踪。它不是当前 corpus 事实真源，也不负责冻结 seed、repair baseline、NL dataset、转换器协议或主实验结果。

当前事实源必须回到：

| 需要判断什么 | 当前事实源 | evidence 中对应旧材料的角色 |
|---|---|---|
| `<NL, STM_0>` seed / seed library | [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md) | 只解释 R1 如何形成候选与筛选口径。 |
| STM repair baseline / near-neighbor | [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md) | 只保留 generation-era baseline 与旧近邻审计。 |
| 控制系统纯 NL 数据源 | [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md) | 只保留来源覆盖、可用性与历史统计线索。 |
| 转换 / 表示 / readiness 机器事实源 | [../pipeline/conversion/README.md](../pipeline/conversion/README.md)、[../pipeline/representation/README.md](../pipeline/representation/README.md)、[../pipeline/readiness_audit/README.md](../pipeline/readiness_audit/README.md) | 只解释旧格式压力和转换候选来源；不替代当前 pipeline 事实源。 |
| 人类阅读报告和 story handoff | [../reports/SUMMARY.md](../reports/SUMMARY.md) | 只作历史证据背景；当前结论以 reports 总账和具体报告为准。 |

## 1. 子路径

| 子路径 | 职责 | 入口 |
|---|---|---|
| [ledgers/](./ledgers/) | 上游事实、来源覆盖、artifact 可获取性、旧资产继承边界台账，以及 2026-07-07 战略转向后的 active / update / archive / historical 资产地图。 | [ledgers/README.md](./ledgers/README.md) |
| [audits/](./audits/) | R1 baseline / strict seed 审计口径、执行方案，以及 PR-asset-map 静态扫描审计报告。 | [audits/README.md](./audits/README.md) |
| [matrices/](./matrices/) | 候选 baseline 与格式转换压力矩阵。 | [matrices/README.md](./matrices/README.md) |
| [traces/](./traces/) | 分支局部资产与消费决策追踪。 | [traces/README.md](./traces/README.md) |

## 2. 三件套

1. 本文件：说明 `evidence/` 的定位、边界和子路径。
2. [SUMMARY.md](./SUMMARY.md)：维护历史审计材料总账、当前事实源跳转和风险提示。
3. [GUIDE.md](./GUIDE.md)：规定后续如何读取、移动、补充或引用本目录材料。

## 3. 读取纪律

1. 需要冻结 R2 seed 时，回到 [../corpora/seed_library/SUMMARY.md](../corpora/seed_library/SUMMARY.md)，不能直接从 [matrices/baseline_candidate_matrix.md](./matrices/baseline_candidate_matrix.md) 或 [audits/strict_seed_literature_survey.md](./audits/strict_seed_literature_survey.md) 选样本。
2. 需要判断 repair baseline 时，回到 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)，不能把旧 generation baseline 台账改写成当前 repair baseline 事实。
3. 需要控制系统 NL 数据源时，回到 [../corpora/nl_datasets/SUMMARY.md](../corpora/nl_datasets/SUMMARY.md)，不能把只有 NL 的 source pool 提前计为 paired seed。
4. 本目录可以解释“为什么后来这样分工”，但不得替代 `corpora/`、`repair_baselines/`、`nl_datasets/` 的当前总账。
