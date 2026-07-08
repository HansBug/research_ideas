# paper_stm_repair/STATUS.md — 当前状态总账

## 1. 当前阶段

paper1 处于 **战略转向后的 story reset / issue lifecycle 准备阶段**。当前 active 主线是 source-level behavioral issue discovery and closure，不再是 Better STM / which STM is better 主框架。

## 2. 已完成事实

| 类别 | 状态 | 证据入口 |
|---|---|---|
| 导师战略校准 | 已完成 | [../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md](../talks/2026-07-07-导师-paper1发现修正与BetterSTM归档.md) |
| 资产清账 | 已完成 | [evidence/ledgers/paper1_strategy_asset_map.md](./evidence/ledgers/paper1_strategy_asset_map.md), [evidence/audits/2026-07-07-post-strategy-asset-scan.md](./evidence/audits/2026-07-07-post-strategy-asset-scan.md) |
| seed / corpus 来源 | 已有基础资产 | [corpora/](./corpora/) |
| conversion / representation 基础设施 | 已有基础资产 | [pipeline/](./pipeline/) |
| 历史 R5/R5.5 reports | 已有历史材料 | [reports/](./reports/) |
| 历史 R5.7 Better STM reports | 已迁入 cold archive | [archive/r5_7_better_stm_snapshot/reports/](./archive/r5_7_better_stm_snapshot/reports/) |
| story reset | 当前已转为 source-level issue lifecycle 口径 | [story/](./story/) |
| 最小 issue ledger v0 | 已定义；覆盖 candidate / confirmed / rejected / out-of-scope / insufficient evidence 与 Q11=A raw-internal path | [experiment_design/issue_lifecycle/](./experiment_design/issue_lifecycle/), [pipeline/evaluation/schemas/source_issue_ledger.schema.json](./pipeline/evaluation/schemas/source_issue_ledger.schema.json), [pipeline/evaluation/tests/test_source_issue_ledger_schema.py](./pipeline/evaluation/tests/test_source_issue_ledger_schema.py) |

## 3. 尚未完成事实

| 后续能力 | 当前状态 | 后续 PR |
|---|---|---|
| Better STM-facing 资产归档 | 已完成；只允许 historical / superseded / calibration-only 引用 | [archive/r5_7_better_stm_snapshot/](./archive/r5_7_better_stm_snapshot/) |
| raw/source trace 与 patch/projection 挂接 | 未定义；`source_element_refs` / `required_future_trace` 只是 v0 placeholder | `PR-source-trace` |
| 最小 loop IO / run record | 未冻结 | `PR-loop-io` |
| discovery + strict confirmation | 未实现 | `PR-discover-confirm` |
| issue-grounded repair runner | 未实现 | `PR-repair-runner` |
| raw/source export 或 patch bundle | 未实现 | `PR-raw-export` |
| closure / regression audit | 未实现 | `PR-closure-audit` |
| pilot | 未运行 | `PR-loop-pilot` |
| final evaluation rubric | 未冻结；必须等 pilot 后 | `PR-eval-rubric` |
| baseline contract | 未冻结；必须等 pilot 和 rubric 后 | `PR-baseline-contract` |
| formal experiment protocol | 未冻结 | `PR-exp-protocol` |

## 4. 当前可声称与不可声称

### 可以声称

- 本工作区已经把 paper1 主线从一轮式 `NL -> STM` 生成转向已有状态机制品的反馈驱动问题发现与修正。
- 2026-07-07 导师讨论进一步确认：paper1 contribution 应聚焦 feedback-driven LLM refinement loop，以及 diagnostics / inspect、simulation / probe、formal verification / check feedback 如何进入这个 loop；不把 fcstm 本身作为贡献。
- 已有 conversion / representation / readiness 资产可作为后续方法 infrastructure。
- 已完成 asset map，可指导哪些材料保留、改写、归档或只作历史证据。

### 不可声称

- 不可声称已经证明 Better STM 主结果。
- 不可声称真实 repair loop 已经运行。
- 不可声称 constructed `STM_k` dry-run 是方法效果。
- 不可声称 `fcstm` / `pyfcstm` 是 paper1 contribution。
- 不可声称 ledger / audit / evidence bookkeeping 是 paper1 headline contribution。
- 不可声称 conversion / lowering / inspect ok 是 repair gain。
- 不可声称 final metrics / baseline / judge prompt 已经冻结。

## 5. 当前最高风险

1. 旧 Better STM wording 回流，导致 reviewer 以为本文在证明 specification 或 modeling language 优劣。
2. 把 expression debt / folded event / ugly expression 直接算作 confirmed issue。
3. 把中间表示能力写成贡献，而不是写成可执行反馈介质。
4. 把 ledger / audit / evidence bookkeeping 写成主贡献，偏离导师确认的 loop + simulation / formal-verification feedback 主线。
5. 在 pilot 前过早冻结 evaluation rubric 或 baseline contract。
6. 只停留在中间表示修复，未回到 raw/source 层说明 issue closure。

## 6. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-08 10:15:00 | STATUS 同步 `PR-issue-ledger`：最小 source issue ledger v0 已定义，但尚未接入真实 discovery / repair / closure loop。 |
| 2026-07-07 23:40:00 | STATUS 同步 `PR-better-archive`：R5.7 Better STM-facing 资产已迁入 cold archive，R5/R5.5 reports 与 R5.7 reports 分开。 |
| 2026-07-07 22:10:00 | STATUS 补充 contribution 修正：audit / ledger 只作方法和评价纪律，不能替代 loop + executable feedback integration。 |
| 2026-07-07 21:20:00 | STATUS 改为 source-level issue lifecycle 状态总账；明确真实 repair loop / pilot / final evaluation / baseline 均未完成。 |
| 2026-07-07 20:44:08 | asset map 完成，确认 root/story 需更新，R5.7 Better STM-facing 资产需归档。 |
