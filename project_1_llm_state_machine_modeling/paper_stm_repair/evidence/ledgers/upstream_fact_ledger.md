# upstream fact ledger：上游事实源与使用边界

## 1. 事实优先级

事实优先级为：**2026-06-12 导师定调与 PR #100 > 已合入 `main` 的仓库事实 > PR #93/#94/#96 分支局部资产 > 历史 comment / gist / 旧草案**。

## 2. 上游来源表

| 来源 | 当前状态 | R0 使用方式 | 不可越界 |
|---|---|---|---|
| PR [#100](https://github.com/HansBug/research_ideas/pull/100) | upstream umbrella / 合同已冻结 | 本 PR 的直接上游合同；R0 只实现“主线与范围冻结”。 | 不提前实现 R1--R7。 |
| PR [#99 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818) | merged PR comment，且已被正式 talks 记录吸收 | 作为 2026-06-12 会后定调的直接记录。 | 不把 comment 当成独立落盘文件；以 talks 记录为长期事实源。 |
| [2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | `main` 已有正式导师讨论记录 | 第一篇转向、`fcstm` 弱化、baseline 重排、第二篇转向等高优先级事实源。 | 不把 AI 衍生建议误写成导师原话。 |
| [talks/SUMMARY.md](../../../talks/SUMMARY.md) | `main` 已有总账 | 确认当前高优先级约束。 | 新导师意见出现时需更新。 |
| PR [#93](https://github.com/HansBug/research_ideas/pull/93) | OPEN / historical | 旧 foundation / 路径结构 / 历史资产入口。 | 旧 `NL -> STM` story 不继承；分支文件不是 `main` 事实。 |
| PR [#94](https://github.com/HansBug/research_ideas/pull/94) / [#96](https://github.com/HansBug/research_ideas/pull/96) | merged into #93 branch only | 可参考 baseline 反证、claim gate、旧 outline 经验。 | 不直接写成当前分支已有文件。 |
| PR [#73](https://github.com/HansBug/research_ideas/pull/73) / [#82](https://github.com/HansBug/research_ideas/pull/82) / [#92](https://github.com/HansBug/research_ideas/pull/92) | `main` 已合入 | 后续 R1 baseline / seed 资产盘点线索。 | R0 不做逐篇盘点，不认定可运行。 |
| [../../sources/](../../../sources/) | `main` 已有 | 后续 R1/R2 潜在 seed 池线索。 | R0 不抽样、不冻结 Top-N。 |
| [../../baselines/](../../../baselines/) | `main` 已有 | 后续 R1 资产盘点入口。 | R0 不判断代码 / artifact 可获取性。 |

## 3. 关键事实摘要

| 事实 | 来源 | R0 处理 |
|---|---|---|
| 第一篇不再主打 `NL -> STM` 生成。 | talks 2026-06-12 / PR #99 comment / PR #100 | 写入 story 与 task boundary。 |
| `NL -> STM_0` 只作为 seed construction / baseline source / related work。 | talks 2026-06-12 / PR #100 | 写入非目标与 claim gate。 |
| 修正 run 内无人化。 | talks 2026-06-12 | 写入 task boundary。 |
| `fcstm` / DSL 弱化。 | talks 2026-06-04 延续 + 2026-06-12 | 写入 terminology policy。 |
| baseline 不作废，角色重排。 | talks 2026-06-12 / PR #100 | R1 盘点，R0 只登记边界。 |
| 评价门应先于真实修正预演冻结。 | PR #100 三路 review 后合同 | R4/R6 继承，R0 只写原则。 |

## 4. 使用规范

1. 引用 PR comment 时，必须同时确认是否已有落盘文档吸收。
2. 引用分支局部资产时，必须标注 “#93 分支局部 / 未进 `main`”。
3. 任何进入论文正文的事实都应在 R7 前回到落盘文件或可访问链接核验。
4. 不确定内容写“待 R1/R2/R3 核验”，不要脑补。
