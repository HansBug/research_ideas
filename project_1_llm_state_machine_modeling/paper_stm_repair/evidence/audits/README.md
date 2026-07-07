# audits/ — 历史审计报告入口

> **硬边界**：本子路径保存 R1 阶段的审计设计、审计执行结果、strict seed 调研口径，以及 2026-07-07 PR-asset-map 的静态扫描审计报告。它回答“当时怎么审 / 本轮如何扫到风险资产”，不回答“当前最终采用什么”。当前采用口径必须回到 `corpora/`、`reports/`、后续 `experiment_design/eligibility/` 和新的 issue lifecycle PR。

## 1. 什么时候读这里

| 场景 | 是否建议读 | 理由 |
|---|---:|---|
| 想知道 strict seed 早期筛选标准、排除码和人工审计流程 | 是 | [strict_seed_literature_survey.md](./strict_seed_literature_survey.md) 记录了 R1 审计口径。 |
| 想知道 baseline / seed / converter / comparison 资产如何被初步审计 | 是 | [baseline_asset_audit.md](./baseline_asset_audit.md) 是 R1 审计总账。 |
| 想复查 PR-asset-map 如何扫描 Better STM / `STM_k` / adjudication / repair target / conversion gain 风险资产 | 是 | [2026-07-07-post-strategy-asset-scan.md](./2026-07-07-post-strategy-asset-scan.md) 记录扫描命令、命中数量、代表性命中和判读。 |
| 想确定当前主 seed 池数量、转换状态或实验纳入资格 | 否 | 应读当前 reports / registry / machine JSONL。 |
| 想写论文 related work 的最终定位 | 谨慎 | 可作为线索，但必须回到论文原文、当前 corpus 和正式 citation。 |

## 2. 本子路径文件清单

| 文件 | 内容 | 推荐阅读场景 | 禁止误用 |
|---|---|---|---|
| [2026-07-07-post-strategy-asset-scan.md](./2026-07-07-post-strategy-asset-scan.md) | PR-asset-map 静态扫描审计报告。 | 后续需要复验 `paper1_strategy_asset_map.md` 的扫描证据与代表性命中时。 | 不能把扫描命中数量写成研究结果；不能替代后续 `PR-better-archive` 的实际移动。 |
| [baseline_asset_audit.md](./baseline_asset_audit.md) | R1 baseline / seed / converter / comparison 资产审计总账。 | 回看 R1 如何识别 generation-era baseline 和近邻资产。 | 不能直接决定当前 repair baseline。 |
| [strict_seed_literature_survey.md](./strict_seed_literature_survey.md) | strict seed 调研定义、排除码、分级标准和初始事实台账。 | 回看早期 seed 文献范围和排除理由。 | 不能把早期候选直接计入当前 paired seed。 |

## 3. 与其他 evidence 子路径的关系

| 子路径 | 何时跳转 |
|---|---|
| [../ledgers/README.md](../ledgers/README.md) | 审计报告需要事实等级、来源覆盖或 artifact 可获取性背景时。 |
| [../matrices/README.md](../matrices/README.md) | 需要把审计结论压缩成候选矩阵或格式压力矩阵时。 |
| [../traces/README.md](../traces/README.md) | 需要看某个分支局部资产是否已消费或排除时。 |

## 4. 当前事实源回跳

| 当前问题 | 应回跳的事实源 | 说明 |
|---|---|---|
| seed registry / paired seed 当前状态 | [../../corpora/seed_library/REGISTRY.md](../../corpora/seed_library/REGISTRY.md)、[../../corpora/seed_library/SUMMARY.md](../../corpora/seed_library/SUMMARY.md) | strict seed audit 只能解释早期筛选口径，不能替代当前 registry。 |
| repair baseline / near-neighbor 当前状态 | [../../corpora/repair_baselines/SUMMARY.md](../../corpora/repair_baselines/SUMMARY.md) | `baseline_asset_audit.md` 是 R1 generation-era 审计，不是当前 repair baseline 总账。 |
| conversion / representation 当前状态 | [../../pipeline/conversion/README.md](../../pipeline/conversion/README.md)、[../../pipeline/representation/README.md](../../pipeline/representation/README.md) | converter 相关审计必须回到当前 pipeline。 |
| readiness / seed profile 人类结论 | [../../reports/2026-06-28-04-03-18-seed-readiness-report.md](../../reports/2026-06-28-04-03-18-seed-readiness-report.md)、[../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)、[../../reports/SUMMARY.md](../../reports/SUMMARY.md) | 审计报告只能作 provenance，核心结论读 reports。 |
