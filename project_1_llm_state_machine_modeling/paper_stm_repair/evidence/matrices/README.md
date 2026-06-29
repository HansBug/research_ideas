# matrices/ — 历史候选矩阵与格式压力入口

> **硬边界**：本子路径保存历史矩阵，用于横向比较候选、格式、工具链压力和早期 baseline 线索。矩阵是“分析视图”，不是当前事实源；凡涉及当前数字、纳入、排除和论文 claim，必须回跳到当前 registry / reports / machine artifacts。

## 1. 什么时候读这里

| 场景 | 是否建议读 | 理由 |
|---|---:|---|
| 想快速理解 R1 时哪些 baseline / seed 候选被放在一起比较 | 是 | [baseline_candidate_matrix.md](./baseline_candidate_matrix.md) 是历史候选矩阵。 |
| 想理解 prior output formats 对 R3 转换器造成的压力 | 是 | [format_conversion_matrix.md](./format_conversion_matrix.md) 保存格式压力视图。 |
| 想确定当前主实验 seed eligibility | 否 | 应读 [../../experiment_design/eligibility/README.md](../../experiment_design/eligibility/README.md)、[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md) 和当前 reports。 |
| 想报告当前转换成功率 | 否 | 应读 `pipeline/readiness_audit/` machine source 和 reports。 |

## 2. 本子路径文件清单

| 文件 | 内容 | 推荐阅读场景 | 禁止误用 |
|---|---|---|---|
| [baseline_candidate_matrix.md](./baseline_candidate_matrix.md) | 五绿 direct generation baseline 与近邻候选矩阵。 | 解释为什么一些工作被视为 seed source / converter pressure / related work。 | 不能作为当前 baseline 纳入表。 |
| [format_conversion_matrix.md](./format_conversion_matrix.md) | prior output format 与 R3 转换压力矩阵。 | 设计或解释转换器覆盖边界。 | 不能替代 R3/R4.5/R5 的真实转换结果。 |

## 3. 与其他 evidence 子路径的关系

| 子路径 | 何时跳转 |
|---|---|
| [../ledgers/README.md](../ledgers/README.md) | 需要矩阵背后的事实来源、可获取性和覆盖率依据时。 |
| [../audits/README.md](../audits/README.md) | 需要审计方案、排除码或 strict seed survey 背景时。 |
| [../traces/README.md](../traces/README.md) | 需要确认矩阵中某个分支资产是否后来被消费时。 |

## 4. 当前事实源回跳

| 当前问题 | 应回跳的事实源 |
|---|---|
| seed / generated pair 当前状态 | [../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md)、[../../corpora/seed_library/REGISTRY.md](../../corpora/seed_library/REGISTRY.md) |
| repair baseline 当前状态 | [../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md) |
| eligibility 规则 | [../../experiment_design/eligibility/README.md](../../experiment_design/eligibility/README.md) |
| 转换 pipeline | [../../pipeline/conversion/README.md](../../pipeline/conversion/README.md) |
| 表示桥 | [../../pipeline/representation/README.md](../../pipeline/representation/README.md) |
| readiness audit | [../../pipeline/readiness_audit/README.md](../../pipeline/readiness_audit/README.md) |
| reports 总账 | [../../reports/SUMMARY.md](../../reports/SUMMARY.md) |
