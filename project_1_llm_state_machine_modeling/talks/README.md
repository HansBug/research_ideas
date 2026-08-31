# project_1 Paper1 talks 与交班材料

> 当前默认入口是 [2026-08-31 Paper1 v60/current 与 X1v2 baseline 最终定性与 PR 收尾](./2026-08-31-paper1-v60-current与X1v2-baseline最终定性与PR收尾.md)。它不是导师原话，也不替代正式 v4 报告；读者应继续沿该 talk 进入 final-results v4。

本目录保留导师讨论、实验/调研记录和最终交班材料。旧记录不删除、不覆盖；凡标为 historical、superseded 或 provenance 的文件都不能作为当前 Paper1 headline 的事实源。当前 Paper1 的 validity、relation、D/A、K/N/I 和成分分析判断均由人工完成，机器只做 provider-free 的机械汇总与复核。

## 1. 定位

本目录用于维护 `project_1_llm_state_machine_modeling` 中与导师形成的**正式研究讨论记录**。它不同于仓库根目录的 [talks/](../../talks/) 工作区，也不同于本项目内的 [discussions/](../discussions/)：

1. 根目录 [talks/](../../talks/) 更偏通用会前/会后纪要工作流，可包含 PPT、原始碎片、待办等完整会议工作区。
2. [discussions/](../discussions/) 主要记录 AI 与用户内部推演、方案辩论、技术调研和临时判断。
3. 本目录只收录**已经包含导师意见、会后路线决策或正式学术口径调整**的讨论记录，是后续写作、实验设计和 agent 工作的高优先级上下文。

## 2. 使用原则

当本目录中的正式导师讨论记录与 [discussions/](../discussions/) 中的内部讨论存在冲突时，默认以本目录为准；若本目录与更晚的导师讨论记录冲突，则以时间更新、明确性更高的记录为准。

后续 AI 在处理 project_1 第一篇论文路线、实验设计、baseline 选择、样本选择或方法定位时，应优先读取：

1. 本文件 [README.md](./README.md)。
2. [GUIDE.md](./GUIDE.md)。
3. [SUMMARY.md](./SUMMARY.md)。
4. 与任务日期或主题最相关的单篇正式导师讨论记录。

## 3. 当前入口和文件状态

日期化文件共 12 篇：5 篇导师记录、3 篇实验记录、3 篇调研记录，以及 1 篇当前 Paper1 定性/交班 talk。

当前阅读路径：

1. [最终 Paper1 定性与 PR 收尾](./2026-08-31-paper1-v60-current与X1v2-baseline最终定性与PR收尾.md)
2. [v60/current 与 X1v2 baseline v3 正式报告](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/report/v60_current_vs_x1v2_baseline_v4_cn.md)
3. [final-results v4 README](../paper_stm_issue_discover/final_results/v60_current_vs_x1v2_baseline/README.md)

状态索引：

| 文件类别 | 文件 | 状态 | 替代入口 |
| --- | --- | --- | --- |
| Paper1 定性/交班 | [2026-08-31 最终 talk](./2026-08-31-paper1-v60-current与X1v2-baseline最终定性与PR收尾.md) | current | final-results v4 |
| 导师路线 | [2026-08-08 收窄为 issue-discover](./2026-08-08-导师-paper1收窄为issue-discover.md) | current route decision，不是实验结果 | 最终 talk、final-results v4 |
| 导师/调研背景 | 2026-08-12 谓词出处、2026-08-12 相关工作、2026-08-13 两篇调研 | provenance | 最终 talk 的学术口径和 `related_work/` |
| 早期路线与实验 | 2026-06-04、2026-06-12、2026-07-07、2026-08-10、2026-08-12 两篇实验 | historical/superseded | 最终 talk、final-results v4 |

逐篇状态和默认阅读顺序见 [SUMMARY.md](./SUMMARY.md)。

## 4. 历史记录

以下链接保留原文和 Git 路径，供 provenance 使用；它们不是当前 headline：

1. [2026-08-12-导师-谓词词表的出处根基与C3差异化.md](./2026-08-12-导师-谓词词表的出处根基与C3差异化.md)
2. [2026-08-10-实验-v46全量矩阵双侧结论.md](./2026-08-10-实验-v46全量矩阵双侧结论.md)
   - ⚠️ **实验结论记录，不是导师意见。** 收录理由：它决定 paper1 结果节能写什么数字、能下什么结论，属正式学术口径材料。覆盖侧与多报侧的整体结果、分层分析、五类裁定的定义与判定链路、各小类统计与典型案例，以及台账原始数据的 gist 与本地来源。文中「学术结论」一律标注 **【AI 衍生建议】**，尚待导师确认。

3. [2026-07-07-导师-paper1发现修正与BetterSTM归档.md](./2026-07-07-导师-paper1发现修正与BetterSTM归档.md)
   - 记录 2026-07-07 前后围绕 paper1 最新导师讨论转录与会后复盘形成的战略校准：第一篇不再以 `Better STM / which STM is better` 作为 active 评价框架，而转向 source-level behavioral issue discovery and closure；`fcstm` 进一步下沉为中间语义执行介质；R5.7 / Better STM-facing 资产应全量归档，主路径重建 issue / closure / regression-audit 新框架。该记录覆盖 2026-06-12 记录中的 Better STM 主评价口径。
4. [2026-06-12-导师-两篇论文转向与模型修正定调.md](./2026-06-12-导师-两篇论文转向与模型修正定调.md)
   - 记录 2026-06-12 关于第一篇从 `NL -> STM` 生成转向 `<NL, STM_0> -> STM_k / Better STM` 无人化反馈驱动修正、弱化 `fcstm` / DSL 名头、baseline 角色重排、多格式转换器需求，以及第二篇从 `sources` 文库综述转向 agent-based SLR 方法学论文的导师讨论与会后定调；其中 Better STM active framework 已被 2026-07-07 记录覆盖，但从 `NL -> STM` 转向已有模型反馈修正的背景仍有效。
5. [2026-06-04-导师-第一篇论文路线与E1E2定位.md](./2026-06-04-导师-第一篇论文路线与E1E2定位.md)
   - 记录 2026-06-04 关于 project_1 第一篇论文主线、Path-1/Path-2 分工、E1/E2 定位、核心贡献、baseline、数据选择、变量角色、LangChain/LangGraph、BMC/LTL 与 survey 可能性的导师意见；其中第一篇主任务边界已被 2026-06-12 和 2026-07-07 记录连续更新。

## 5. 维护边界

本目录不存放论文 PDF、单篇论文提取物或实验 raw artifacts。若需要引用这些材料，应使用相对路径或 GitHub URL 指向对应 PR / issue / 文件，并在正式讨论记录中说明它们的用途与可信度边界。
