# Upstream Fact Ledger

## 1. 事实源等级

| 等级 | 来源 | R0 使用规则 |
|---:|---|---|
| S0 | [PR #100](https://github.com/HansBug/research_ideas/pull/100) | 直接上游合同；R0 必须与其子 PR 表、四例运行规划和 claim gate 一致。 |
| S0 | [PR #99 会后定调 comment](https://github.com/HansBug/research_ideas/pull/99#issuecomment-4689018818)、[2026-06-12 导师讨论记录](../../../talks/2026-06-12-导师-两篇论文转向与模型修正定调.md) | 第一篇新主线最高优先级事实。 |
| S1 | `main` 已合入 baseline 线索：[#73](https://github.com/HansBug/research_ideas/pull/73)、[#82](https://github.com/HansBug/research_ideas/pull/82)、[#92](https://github.com/HansBug/research_ideas/pull/92) | 后续 R1 资产盘点线索；R0 不把候选直接写成可运行 baseline。 |
| S2 | 历史 foundation PR [#93](https://github.com/HansBug/research_ideas/pull/93) | OPEN / historical；只作旧结构、早期计划和历史资产入口。 |
| S2 | [#94](https://github.com/HansBug/research_ideas/pull/94)、[#96](https://github.com/HansBug/research_ideas/pull/96) | 已合入 #93 分支，但 #93 未合入 `main`；属于分支局部资产。 |
| S3 | 旧 comment、Gist、临时讨论 | 只能作发现线索，不得升级为论文事实。 |

## 2. PR 状态核验

| PR | 当前状态 | 对 R0 的作用 | 风险 |
|---|---|---|---|
| #100 | OPEN，base=`main`，head=`paper1/better-stm-repair-loop-umbrella` | R0 直接上游。 | 若 #100 body 后续变更，R0 需同步。 |
| #99 | MERGED to `main` | 2026-06-12 导师汇报和会后转向记录入口。 | 无；但 comment 与正式 talk 记录需共同引用。 |
| #93 | OPEN，base=`main` | 历史 foundation / Path-1 工作区入口。 | 旧 `NL -> STM` story 已被覆盖，不能继承。 |
| #94 | MERGED into #93 branch | 九大 baseline 盘点线索。 | 分支局部，不是 `main` 事实；R1 需复核。 |
| #96 | MERGED into #93 branch | 旧 S0a story reframe 线索。 | 分支局部，且 story 已被 2026-06-12 再次覆盖。 |
| #73/#82/#92 | MERGED to `main` | baseline 候选和近邻工作线索。 | 只能作为线索，R1 需复核论文、代码和 artifact。 |

## 3. 已冻结事实

1. 第一篇当前主线是 `<NL, STM_0> -> STM_k / Better STM` 的无人化反馈驱动修正。
2. `NL -> STM_0` 只作为 seed construction / baseline source / related work。
3. `fcstm` / `pyfcstm` / DSL 不作为论文核心概念或贡献。
4. baseline 角色重排为 seed source、converter pressure、error taxonomy、limited comparison 和 related work evidence。
5. R0 不跑四例真实运行；四例预演至少依赖 R1/R2/R3/R4。

## 4. 不得升级为事实的内容

1. PR #94/#96 中尚未进入 `main` 的文件内容。
2. 旧 `path1_foundation/` 的目录存在性。
3. 尚未复核的 baseline 代码、demo、artifact 可获取性。
4. 尚未冻结的四例样本。
5. 尚未运行的修正效果、场景通过率、诊断闭合率或人工评分。
