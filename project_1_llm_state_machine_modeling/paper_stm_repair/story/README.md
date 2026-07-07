# story/README.md — paper1 story 入口

本目录维护 paper1 的 active story、任务边界、模型范围、术语和 claim-evidence。当前 story 已从旧的 Better STM / which STM is better 框架重置为 **source-level behavioral issue discovery and closure**。

## 1. 当前 thesis

给定自然语言需求 `NL` 与已有 raw/source 状态机 `STM_0`，本文研究如何通过中间语义执行表示和工具 / agent 反馈发现 source-level behavioral issues，确认问题、围绕 confirmed issues 修复，并回到 raw/source 层审计 closure 与 regression。

`fcstm` / `pyfcstm` 只作为 intermediate executable semantic representation / feedback medium；它们不是 paper1 的 contribution。

## 2. 文件职责

| 顺序 | 文件 | 职责 | 不能替代什么 |
|---:|---|---|---|
| 1 | [paper_story.md](./paper_story.md) | thesis、gap、challenge、method insight、contributions、claims-to-avoid。 | 不替代实验结果或 final paper。 |
| 2 | [task_boundary.md](./task_boundary.md) | 输入输出、方法内外、人类角色、failure / unsupported / unjudgeable 边界。 | 不冻结 final metrics / baseline。 |
| 3 | [model_scope.md](./model_scope.md) | 支持的状态机范围和行为表达范围。 | 不把 fcstm 定义为研究对象。 |
| 4 | [terminology_policy.md](./terminology_policy.md) | 术语中英文与禁用词。 | 不定义 run record schema。 |
| 5 | [claim_evidence_map.md](./claim_evidence_map.md) | claim strength、evidence、forbidden claims。 | 不把 planned work 写成已完成 evidence。 |
| 6 | [paper_outline.md](./paper_outline.md) | 后续论文结构草案。 | 不替代正式正文。 |

## 3. 上游事实源

1. 战略讨论：[../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md)
2. 资产清账：[../evidence/ledgers/paper1_strategy_asset_map.md](../evidence/ledgers/paper1_strategy_asset_map.md)
3. 当前状态：[../STATUS.md](../STATUS.md)
4. 工作纪律：[../GUIDE.md](../GUIDE.md)

## 4. 历史框架处理

- Better STM / which STM is better：superseded，不再是 active headline。
- R5.7 repair target taxonomy / objective metrics / adjudication dry-run：historical / archive-pending / calibration-only。
- constructed `STM_k`：不是真实 repair-loop output。
- `paper_v1/`、旧 `discussions/`：只作历史背景或 negative evidence，不继承旧 contribution wording。

## 5. Reviewer challenge 快速回答

**Q：这是不是在证明 fcstm 比 PlantUML / SysML-like 表达更好？**

不是。paper1 只需要一套中间语义执行表示来承载 diagnostics、simulation/probe、verification/check feedback。最终研究对象和评价落点仍是 raw/source 状态机制品中的 source-level behavioral issues 是否被发现、修复和闭合。

**Q：这是不是在定义什么是 better specification？**

不是。Better STM 主框架已经 superseded。当前问题是 issue lifecycle：发现哪些 source-level behavioral issues、哪些被确认、哪些被 issue-grounded repair 闭合、是否引入 regression。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 21:20:00 | story 入口重置为 source-level behavioral issue discovery and closure；Better STM 主框架降级为 historical / archive-pending。 |
