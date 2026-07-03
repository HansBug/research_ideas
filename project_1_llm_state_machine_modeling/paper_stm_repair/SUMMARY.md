# paper_stm_repair/SUMMARY.md — 顶层总账入口

本文件是 `paper_stm_repair/` 顶层的轻量总账入口，目的只是让读者按 `README.md -> SUMMARY.md -> GUIDE.md` 的统一习惯导航。

**当前状态与关键数字的事实真源仍是 [STATUS.md](./STATUS.md)**；本文件不复制 R5/R5.5 完整表，不作为第二事实源。若本文件与 [STATUS.md](./STATUS.md)、[reports/SUMMARY.md](./reports/SUMMARY.md) 或 pipeline JSON/JSONL/ZIP 不一致，按以下优先级处理：machine artifacts / corpus registry > [STATUS.md](./STATUS.md) > 本文件。

## 1. 当前一句话状态

当前完成的是 **修正前准备度审计**：一手 seed registry、四例静态样例、转换链路、`.fcstm` 表示桥、评价门草案、R5 全量摸排与 R5.5 `llms-emp` 主 seed 池画像已就位；尚未执行真实修正循环、尚未生成 `STM_k`，也尚未形成 Better STM 主实验结果。

R5.7.1--R5.7.3 已冻结评价逻辑链、Better STM / repair target 合同与客观代理指标框架，入口为 [experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md)、[experiment_design/quality_model/better_stm_definition.md](./experiment_design/quality_model/better_stm_definition.md)、[experiment_design/quality_model/repair_target_taxonomy.md](./experiment_design/quality_model/repair_target_taxonomy.md) 和 [experiment_design/metrics/objective_metric_framework.md](./experiment_design/metrics/objective_metric_framework.md)；这只支持 task / scope、readiness、protocol / evaluation、指标框架与 limitation 类型主张，不支持 repair effectiveness。

## 2. 顶层入口

| 需要回答的问题 | 入口 |
|---|---|
| 现在做到哪一步、关键数字是什么 | [STATUS.md](./STATUS.md) |
| 全局维护纪律和禁止主张 | [GUIDE.md](./GUIDE.md) |
| 人类可读研究报告总账 | [reports/SUMMARY.md](./reports/SUMMARY.md) |
| 阶段链路和机器事实源 | [pipeline/README.md](./pipeline/README.md) |
| 一手 seed 与资源登记 | [corpora/seed_library/REGISTRY.md](./corpora/seed_library/REGISTRY.md) |
| 论文 story / claim gate | [story/README.md](./story/README.md) |
| 实验评价逻辑 / scope / eligibility / quality model / metrics | [experiment_design/SUMMARY.md](./experiment_design/SUMMARY.md)、[experiment_design/evaluation_logic.md](./experiment_design/evaluation_logic.md)、[experiment_design/metrics/objective_metric_framework.md](./experiment_design/metrics/objective_metric_framework.md) |
| 历史审计与证据索引 | [evidence/SUMMARY.md](./evidence/SUMMARY.md) |
| cold / deprecated 历史快照 | [archive/README.md](./archive/README.md) |

## 3. 维护纪律

1. 不在本文件复制完整统计表；需要数字时链接 [STATUS.md](./STATUS.md)、[reports/](./reports/) 或 pipeline machine source。
2. 若 [STATUS.md](./STATUS.md) 的当前状态、主 seed 数字或后续入口发生变化，本文件只更新入口与一句话摘要。
3. 不记录 PR ready、CI 状态、merge 进度、review 已处理等动态流程信息。
4. 新增顶层长期子文库时，必须在本文件补入口，并在 [README.md](./README.md) 的目录地图同步说明。
