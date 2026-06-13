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
| [sources/SUMMARY.md](../../sources/SUMMARY.md) | main 已有 | 787 篇 / 746 正例案例 | 787 篇入口 / 337 条 `T0+FSM/HSM/EFSM` 子池 | 409 条非 strict 正例案例 | closed-at-summary-level / strict-screening-partial | 作为真实控制系统 NL source pool；337 条只是 strict-source 子池，不等于 paired seed 已闭合。 |
| PR [#93](https://github.com/HansBug/research_ideas/pull/93) | open / 分支局部 | 430 changed files | 0 re-landed | 430 branch-local | partial | 只记录 provenance；不把 `path1_foundation/**` 写成 main 事实。 |
| PR [#94](https://github.com/HansBug/research_ideas/pull/94) | merged into #93 branch | 20 changed files | 0 re-landed | 20 branch-local | partial | 九大 baseline S1a 逐篇审计可作 cite-only 线索；不复制旧 story wording。 |
| PR [#96](https://github.com/HansBug/research_ideas/pull/96) | merged into #93 branch | 27 changed files | 0 re-landed | 27 branch-local | partial | 旧 S0a story / claim guardrail 只作历史参考；当前以 R0 / #102 为准。 |
| PR-R0 [#102](https://github.com/HansBug/research_ideas/pull/102) | merged into #100 | 17 R0 文档 | 17 | 0 | closed | 作为 R1 本地事实锚点。 |


## 3. strict seed screening 增补口径

R1 新增 [strict_seed_literature_survey.md](./strict_seed_literature_survey.md) 作为大规模 seed 文献调研协议。当前 coverage 总表中的 `included` 表示“纳入候选入口”，不表示 strict seed eligibility 已逐篇闭合。后续 PR-R2 / R7 若继续扩展外部文献，需要按以下字段回填：`discovered / screened / SS-A / SS-B / ES-C / NN-D / EX-E / pending`。

| 来源 | discovered | screened | strict / strict-like 初判 | 排除 / 降级重点 | closure |
|---|---:|---:|---|---|---|
| `sources/` 案例级子池 | 746 正例案例 | 746 summary-level | 337 条 `T0+FSM/HSM/EFSM` 子池 | `T1+`、Protocol、Resource-flow、Hybrid 等 409 条非 strict 正例 | strict-source partial；需 R2 构造 / 冻结 `STM_0`。 |
| 九个 direct baseline | 9 | 9 candidate-level | `structure-event`、`llms_emp` STM 子集、`ttool-ai` SMD 子集、`umple`、`designing-fsm`、`req`、`pushing-envelope` 分别按 artifact 风险分层 | FlowFSM / SpecGPT 触发 `X_PROTOCOL` | candidate-level partial；需 R2/R3 冻结 artifact。 |
| `reproduction/results/` | 4 个 parquet 入口 | 4 | `structure_event=32` 行、`llms_emp` STM 子集 `38/98`、`ttool=6` 行 | `llms_emp` ACT/SD、TTool 非 SMD 联合模型、Nimbus RSML-e 边界 | local artifact partial。 |
| reviewer corpus | 973 review records | summary-level | strict-compatible review records 可支撑 review/eval，不是 seed 总账 | protocol 新增 153 行不得并入主 seed | reviewer-evidence only。 |
| 外部新增学术检索 | pending | pending | pending | pending | not started in R1。 |

## 4. 重要边界

1. `baselines/` 当前已有 91 篇 completed baseline 条目，但 R1 只对 9 个五绿 direct baseline 与若干强近邻做资产角色重排；未逐篇深审 91 篇的可转换性，也未完成 91 篇 strict seed eligibility 闭合。
2. `sources/` 当前已有 787 篇；按 [sources/SUMMARY.md](../../sources/SUMMARY.md) 的“按领域统计的论文状态分布”合计行，其中 715 篇为 `🟢 直接可用`，可作为 PR-R2 seed 池线索。案例级严格筛后有 337 条 `T0+FSM/HSM/EFSM` 子池，但这仍是 NL source pool，不等于 paired strict seed 已经冻结。R1 不从中选定四例，也不改 `sources/` 总账。
3. PR #94 / #96 的资产只存在于 `paper/project1-path1-foundation` 分支；当前 PR 不 re-land 其文件，只在 [branch_asset_trace.md](./branch_asset_trace.md) 记录消费决策。
4. “四件套齐全”只说明论文分析完成，不等于代码、数据、ground truth 或结果包可复现。

## 5. R2 handoff

PR-R2 选择四例样本时应优先从以下三类入口抽样：

1. `sources/` 的真实控制系统样本，用于构造本研究自己的 `<NL, STM_0>` seed。
2. 五绿 direct baseline 中 artifact 较强的条目，尤其是 `structure-and-event-driven-frameworks...`、`llms_emp`、`ttool-ai`、`designing-fsm...`。
3. 分支局部 PR #94 的逐篇 baseline 盘点作为补充证据，但必须回到当前 `baselines/` 原始目录和 `ASSETS.md` 复核。
