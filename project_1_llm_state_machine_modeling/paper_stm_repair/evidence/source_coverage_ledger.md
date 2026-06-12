# source coverage ledger：R1 来源覆盖与去重闭合

## 1. 用途

本文件记录 PR-R1 对上游 baseline / seed 资产来源的覆盖情况。它的目标不是复制 `baselines/SUMMARY.md` 或 `sources/SUMMARY.md` 全表，而是让后续 PR-R2 知道：哪些来源已经作为候选池入口被纳入、哪些只做高优先级深审、哪些仍是分支局部线索、哪些不能写成已闭合事实。

去重顺序：DOI > 标准化标题 > 作者/年份 > slug / 本地目录。若同一论文同时出现在 PR comment、旧分支文件和 `baselines/` 正式目录中，以 `baselines/` 当前四件套与 `ASSETS.md` 为主事实源；旧分支只作为 provenance / wording 线索。

## 2. coverage 总表

| 来源 | 当前状态 | discovered | included | excluded / deferred | closed? | R1 处理 |
|---|---|---:|---:|---:|---|---|
| [baselines/SUMMARY.md](../../baselines/SUMMARY.md) | main 已有 | 91 | 91 | 0 | closed-at-summary-level | 作为 baseline 候选全集总账；R1 不重写 91 篇逐篇事实。 |
| 五绿 direct baseline `ASSETS.md` | main 已有 | 9 | 9 | 0 | closed-for-direct-assets | 作为 R1 深审对象；见 [baseline_candidate_matrix.md](./baseline_candidate_matrix.md)。 |
| PR [#73](https://github.com/HansBug/research_ideas/pull/73) | merged into main | 4 | 4 | 0 | closed-at-entry-level | 四件套均在当前树存在；多为形式模型强近邻，不升格为 exact STM direct baseline。 |
| PR [#82](https://github.com/HansBug/research_ideas/pull/82) | merged into main | 7 | 7 | 0 | closed-at-entry-level | LLM4MDE 强近邻；记录输出格式差异，防止混入 direct STM。 |
| PR [#92](https://github.com/HansBug/research_ideas/pull/92) | merged into main | 19 | 19 | 0 | closed-at-entry-level | 19 篇均有四件套；其中 3 篇新增 direct baseline 有 `ASSETS.md`。 |
| [sources/SUMMARY.md](../../sources/SUMMARY.md) | main 已有 | 787 | 787 | 0 | closed-at-summary-level | 作为真实控制系统 seed 池线索；R1 只记录规模和抽样入口，不冻结具体 seed。 |
| PR [#93](https://github.com/HansBug/research_ideas/pull/93) | open / 分支局部 | 430 changed files | 0 re-landed | 430 branch-local | partial | 只记录 provenance；不把 `path1_foundation/**` 写成 main 事实。 |
| PR [#94](https://github.com/HansBug/research_ideas/pull/94) | merged into #93 branch | 20 changed files | 0 re-landed | 20 branch-local | partial | 九大 baseline S1a 逐篇审计可作 cite-only 线索；不复制旧 story wording。 |
| PR [#96](https://github.com/HansBug/research_ideas/pull/96) | merged into #93 branch | 27 changed files | 0 re-landed | 27 branch-local | partial | 旧 S0a story / claim guardrail 只作历史参考；当前以 R0 / #102 为准。 |
| PR-R0 [#102](https://github.com/HansBug/research_ideas/pull/102) | merged into #100 | 17 R0 文档 | 17 | 0 | closed | 作为 R1 本地事实锚点。 |

## 3. 重要边界

1. `baselines/` 当前已有 91 篇 completed baseline 条目，但 R1 只对 9 个五绿 direct baseline 与若干强近邻做资产角色重排；未逐篇深审 91 篇的可转换性。
2. `sources/` 当前已有 787 篇；按 [sources/SUMMARY.md](../../sources/SUMMARY.md) 的“按领域统计的论文状态分布”合计行，其中 715 篇为 `🟢 直接可用`，可作为 PR-R2 seed 池线索。R1 不从中选定四例，也不改 `sources/` 总账。
3. PR #94 / #96 的资产只存在于 `paper/project1-path1-foundation` 分支；当前 PR 不 re-land 其文件，只在 [branch_asset_trace.md](./branch_asset_trace.md) 记录消费决策。
4. “四件套齐全”只说明论文分析完成，不等于代码、数据、ground truth 或结果包可复现。

## 4. R2 handoff

PR-R2 选择四例样本时应优先从以下三类入口抽样：

1. `sources/` 的真实控制系统样本，用于构造本研究自己的 `<NL, STM_0>` seed。
2. 五绿 direct baseline 中 artifact 较强的条目，尤其是 `structure-and-event-driven-frameworks...`、`llms_emp`、`ttool-ai`、`designing-fsm...`。
3. 分支局部 PR #94 的逐篇 baseline 盘点作为补充证据，但必须回到当前 `baselines/` 原始目录和 `ASSETS.md` 复核。
