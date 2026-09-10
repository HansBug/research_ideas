# project_1 Paper1 talks 总账

> 本页只做导航和状态索引，不复制 headline 数字。A4 执行反馈消融事实见 [A4 报告](../paper_stm_issue_discover/reports/2026-09-10-17-01-11-a4-frozen-full-tail-results.md)，E2 多模型结果见 [E2 报告](../paper_stm_issue_discover/reports/2026-09-08-e2-three-backbone-results.md)；既有 Luna 主线入口是 [v61 归档 README](../paper_stm_issue_discover/final_results/v61_source_divergence_vs_x1v2_baseline/README.md)，现状分析见 [analysis_and_options.md](../paper_stm_issue_discover/discover_matrix/docs/generations/v61/analysis_and_options.md)；v60 归档只作仪器校准参照。历史记录中的旧数字、旧人工裁定记录、v46/v27/v2 路线仅用于 provenance，不能作为当前结论。

## 1. 默认阅读路径

先读 [2026-09-10 A4 谓词执行反馈消融 talk](./2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md)，再回溯完整方法的结果与导师路线。

1. [2026-09-09 E1/E2 多模型实验 talk](./2026-09-09-实验-E1E2多模型结果与论文叙事.md)
2. [2026-09-05 多模型对照与谓词降幻觉](./2026-09-05-导师-paper1多模型对照与谓词降幻觉.md)，再读 [2026-09-04 大纲收口、消融与基线、对外口径](./2026-09-04-导师-paper1大纲收口与消融基线口径.md)
3. [v61 归档 README](../paper_stm_issue_discover/final_results/v61_source_divergence_vs_x1v2_baseline/README.md)
4. [v61 现状分析与出路](../paper_stm_issue_discover/discover_matrix/docs/generations/v61/analysis_and_options.md)
5. [145 条 ledger](../paper_stm_issue_discover/discover_matrix/ledger_v2/README.md)；它是 expected inventory，不是实验 headline

## 2. 文件状态

| 文件 | 类型 | 状态 | 替代入口 |
| --- | --- | --- | --- |
| [2026-09-10 A4 谓词执行反馈消融 talk](./2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md) | 执行反馈消融与论文叙事 | current result interpretation；全部裁定闭合 | [A4 完整报告](../paper_stm_issue_discover/reports/2026-09-10-17-01-11-a4-frozen-full-tail-results.md) |
| [2026-09-09 E1/E2 多模型实验 talk](./2026-09-09-实验-E1E2多模型结果与论文叙事.md) | 实验结果与论文叙事 | current result interpretation；不建立第二套机器事实源 | E2 综合报告、E1 benchmark 矩阵、A1 归档 |
| [2026-09-05 多模型对照与谓词降幻觉](./2026-09-05-导师-paper1多模型对照与谓词降幻觉.md) | 导师路线决策 | current route；同 backbone 的 2+2 比较，A1/A2 单模型 | 模型调研与独立新实验；v61 仍冻结 |
| [2026-09-04 大纲收口、消融与基线、对外口径](./2026-09-04-导师-paper1大纲收口与消融基线口径.md) | 导师路线决策 | current route（v61 口径） | 大纲、待裁定表、v61 归档 |
| [2026-08-31 最终 talk](./2026-08-31-paper1-v60-current与X1v2-baseline最终定性与PR收尾.md) | 实验结论/交班 | historical/superseded（v60 口径） | v61 归档 |
| [2026-08-08 路线收窄](./2026-08-08-导师-paper1收窄为issue-discover.md) | 导师路线决策 | current route | 2026-09-04 talk、v61 归档 |
| 2026-08-12 谓词出处、2026-08-12 相关工作、2026-08-13 两篇调研 | provenance | provenance | 最终 talk 的学术口径和 `related_work/` |
| 2026-06-04、2026-06-12、2026-07-07 | 导师路线历史 | historical/partially superseded | 当前主线以 issue-discover 为准 |
| 2026-08-10、2026-08-12 三篇实验记录 | 旧实验结论 | historical/superseded | v61 归档 |

## 3. 日期化文件清单

共 16 篇，包含本次 A4 与既有 E1/E2 实验 talk。

| 日期 | 文件 | 状态 |
| --- | --- | --- |
| 2026-09-10 | [2026-09-10 A4 谓词执行反馈消融 talk](./2026-09-10-实验-A4谓词执行反馈消融与论文叙事.md) | 四模型末端反馈消融，实验解释 |
| 2026-09-09 | [E1/E2 多模型实验 talk](./2026-09-09-实验-E1E2多模型结果与论文叙事.md) | 完整方法多模型结果解释 |
| 2026-09-05 | [导师：Paper1 多模型对照与谓词降幻觉](./2026-09-05-导师-paper1多模型对照与谓词降幻觉.md) | current route decision，不是效果结论 |
| 2026-09-04 | [导师：Paper1 大纲收口、消融与基线、对外口径](./2026-09-04-导师-paper1大纲收口与消融基线口径.md) | current route decision（v61 口径） |
| 2026-08-31 | [Paper1 v60/current 与 X1v2 baseline 最终定性与 PR 收尾](./2026-08-31-paper1-v60-current与X1v2-baseline最终定性与PR收尾.md) | historical/superseded（v60 口径） |
| 2026-08-08 | [导师：paper1 收窄为 issue-discover](./2026-08-08-导师-paper1收窄为issue-discover.md) | current route decision |
| 2026-08-12 | [导师：谓词词表的出处根基与 C3 差异化](./2026-08-12-导师-谓词词表的出处根基与C3差异化.md) | provenance |
| 2026-08-12 | [调研：Paper1 相关工作版图与竞争定位](./2026-08-12-调研-paper1相关工作版图与竞争定位.md) | provenance |
| 2026-08-13 | [调研：工业应用场景叙事与算力可行域](./2026-08-13-调研-工业应用场景叙事与算力可行域.md) | provenance |
| 2026-08-13 | [调研：方法类文献的模型代次时效性](./2026-08-13-调研-方法类文献的模型代次时效性.md) | provenance |
| 2026-08-10 | [实验：v46 全量矩阵双侧结论](./2026-08-10-实验-v46全量矩阵双侧结论.md) | historical/superseded |
| 2026-08-12 | [实验：X1 朴素基线对照臂与八轮口径尝试](./2026-08-12-实验-X1朴素基线对照臂与八轮口径尝试.md) | historical/superseded |
| 2026-08-12 | [实验：为什么主臂比朴素基线低 15 个点](./2026-08-12-实验-为什么主臂比朴素基线低15个点.md) | historical/superseded |
| 2026-07-07 | [导师：paper1 发现修正与 BetterSTM 归档](./2026-07-07-导师-paper1发现修正与BetterSTM归档.md) | historical/partially superseded |
| 2026-06-12 | [导师：两篇论文转向与模型修正定调](./2026-06-12-导师-两篇论文转向与模型修正定调.md) | historical/partially superseded |
| 2026-06-04 | [导师：第一篇论文路线与 E1E2 定位](./2026-06-04-导师-第一篇论文路线与E1E2定位.md) | historical/superseded |

## 4. 维护边界

- 本目录不是 raw、ledger、人工裁定或 canonical decision 的事实源；实验数字分别回到 v61、E2、A4 各自的归档或核算，互不替代。
- 导师记录只代表当时讨论，不自动代表当前实验口径；实验和调研记录分别标明来源性质。
- 旧记录保留原文和原路径，不删除历史失败、不覆盖旧数字。需要复活时从本目录的 Git 历史恢复，并重新核对其输入、协议和版本。
- 当前 Paper1 主线是 issue discovery；repair、Better STM、Path-1/Path-2 和早期 v46/v27/v2 headline 不进入默认当前结果叙事。
