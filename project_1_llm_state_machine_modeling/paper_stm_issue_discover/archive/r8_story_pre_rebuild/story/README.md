# story/README.md — 论文叙事入口

本目录维护 paper1 的论文叙事：thesis、贡献口径、章节结构、claim-evidence 映射、
任务边界、建模对象与术语。

> ⚠️ **本目录已按 2026-08-07 / 08-08 导师定调整体改写。**
> paper1 收窄为 **issue discover 单独成篇**，repair 另立后续论文。
> 历史文档里的「多轮 Repair-Confirm」「closure / regression audit」「loop 是 headline
> contribution」等表述**全部作废**，只允许在解释历史转向时出现。

## 1. 当前 thesis

给定一份自然语言需求 `NL` 与一份由 LLM 从该需求生成的状态机模型 `STM_0`，
**把「这个模型哪里不符合需求」变成一个可机械求值的问题**：把需求全覆盖地拆成义务，
把每条义务转换成受限谓词逻辑上的断言，在被评审模型上求值——
为假者构成一条带可执行判据与闭合证据链的发现，为真者构成回归防护。

## 2. 两条 contribution

1. **谓词逻辑元模型与断言体系本身**，而不是「发现了多少问题」。
   断言由 NL 全覆盖拆分出的需求条目转换而来，因而覆盖性来自构造；
   求值为假的挂钩 issue，为真的构成回归防护。
2. **带上下文的发现**（导师原话可直接用于 Intro motivation）：现有的很多 detection 方法
   报告错误，缺少错误的上下文信息——一方面需要人工进行繁重的复核，另一方面也不便于进行
   错误修复后的回归确认。本方法给出的是可执行判据 + 闭合证据链。

⚠️ 修复只在讨论一节**捎带提及一小段**，不展开、不承诺效果、不给数据。

## 3. 文件职责

| 顺序 | 文件 | 职责 | 不能替代什么 |
| --: | :-- | :-- | :-- |
| 1 | [paper_story.md](./paper_story.md) | 叙事主干：问题、价值、现有方法的问题、方法洞察、两条 contribution、可说 / 不可说的话、审稿人风险 | 不替代正文；不替代 claim 的证据核对 |
| 2 | [paper_outline.md](./paper_outline.md) | 章节结构，按导师那条大逻辑排；含 RQ 定义与每节的验收判据 | 不替代正文；不复制实验数字 |
| 3 | [claim_evidence_map.md](./claim_evidence_map.md) | 每条 claim 的证据、强度、允许 / 禁止写法 | 不做数字的第二事实源——数字一律回实验报告核对 |
| 4 | [task_boundary.md](./task_boundary.md) | 输入输出、方法内外、人类角色、失败与不确定状态 | 不定义指标口径 |
| 5 | [model_scope.md](./model_scope.md) | 建模对象 $M = (S, E, V, Tr, A)$、可断言的行为表达、禁止外推 | 不把中间表示定义为研究对象 |
| 6 | [terminology_policy.md](./terminology_policy.md) | 术语中英口径、四组易混术语、指标写法、禁用词 | 不定义 run record 字段 |

**推荐阅读顺序**：想理解论文说什么 → 1、2；想写某一节 → 2 找结构、3 核 claim、6 核措辞；
想核任何数字 → 直接去实验报告。

## 4. 上游事实源与优先级

| 级别 | 来源 | 用途 |
| --: | :-- | :-- |
| 1 | 2026-08-07 / 08-08 导师定调 | 论文收窄、两条 contribution、RQ 设计原则、修复不展开。⚠️ 口头，尚未落成正式 talks 记录；原话摘录在 [../README.md](../../../README.md) §2 |
| 2 | [../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md](../../../../talks/2026-08-10-实验-v46全量矩阵双侧结论.md) | **全部实验数字的唯一来源**，自包含 |
| 3 | [../discover_matrix/docs/protocol/](../../../discover_matrix/docs/protocol/) | 判定口径、方法出处口径、建模对象边界判据——改它们等于改研究规则 |
| 4 | [../README.md](../../../README.md)、[../GUIDE.md](../../../GUIDE.md)、[../STATUS.md](../../../STATUS.md) | 工作区口径、纪律与当前状态 |
| 5 | [../../talks/](../../../../talks/) 的更早导师记录 | 历史转向的背景；被后续记录覆盖的部分不得作为 active 依据 |

⛔ **施工流程状态**（PR 进度、review 状态、CI）以 GitHub PR / issue 为准，本目录不维护。

## 5. 历史框架处理

| 历史框架 | 当前状态 |
| :-- | :-- |
| discover + repair 合成一篇 | 已作废（2026-08-07 / 08-08）。repair 另立后续论文 |
| loop + executable feedback integration 作为 headline contribution | 已作废（同上），降为方法支撑 |
| Better STM / which STM is better | 两代前已作废；资产在 [../archive/](../../) |
| source-level closure / regression audit 作为评价框架 | 已作废，随 repair 一并移出本文 |
| Path-1 / Path-2 评测链、旧 agent loop 基础设施 | 已停用，在 [../../archive/](../../../../archive/)，完整保留可复活，不参与本文任何结论 |

⚠️ 与 repair 期一并搁置但**文件仍在**的资产：
[../experiment_design/issue_lifecycle/](../../r7_issue_lifecycle_scaffold/experiment_design/issue_lifecycle/)、
[../experiment_design/source_trace/](../../r7_issue_lifecycle_scaffold/experiment_design/source_trace/)、
[../evidence/ledgers/](../../../evidence/ledgers/)。它们只作历史背景与后续 repair 论文的迁移输入，
**不得作为本文的方法或评价框架引用**。

## 6. Reviewer challenge 快答

完整对照表在 [claim_evidence_map.md](./claim_evidence_map.md) §4，这里只放三条最常问的。

**Q：这是不是在证明某种建模语言 / DSL 更好？**

不是。中间表示只是求值介质——行为性问题在 PlantUML 上没有定义，必须编译到带形式语义的
表示上才能求值。而且这次编译自身有已量化的损耗，我们如实报告它，不把它算成收益。

**Q：贡献是不是「跑了一个大实验，找到了六成缺陷」？**

不是。贡献是谓词逻辑元模型与断言体系；覆盖率是支撑它的证据，不是贡献本身。
且该数字只能作为上界读，并且必须与算力代价一起给。

**Q：那些没被已知缺陷认领的产出，是不是误报？**

不是。逐条读完后这个读法是错的：按条目计最大的一块是评审入口的编译损失，
既不是被评审模型的缺陷，也不是方法的误判。见 [claim_evidence_map.md](./claim_evidence_map.md) C11–C12。

## 7. 相对上一版改了什么、为什么

| 改动 | 为什么 |
| :-- | :-- |
| thesis 从「source-level behavioral issue discovery **and closure**」收窄为「问题发现 + 断言体系」 | 导师定调 discover 单独成篇 |
| contribution 从三条改为两条 | 同上 |
| 文件职责表新增每份的「不能替代什么」，并新增「数字一律回实验报告核对」 | 旧版的 claim map 曾是唯一的 evidence 表，容易变成数字的第二事实源 |
| 新增 §4 上游事实源的五级优先级 | 旧版只列四个来源、无优先级；而现在同时存在导师口头定调、实验报告、判定口径文档三类事实源，冲突时必须有裁定顺序 |
| §5 历史框架表新增「repair 期资产虽在但不得引用」的显式提示 | `experiment_design/issue_lifecycle/`、`source_trace/`、`evidence/ledgers/` 文件仍在原地，不写清会被后续 agent 当成 active 框架 |
| Reviewer 快答从「是不是证明 fcstm 更好 / 是不是定义 better specification」换成三条当前会被问的 | 旧两问针对的框架已两代前作废 |
