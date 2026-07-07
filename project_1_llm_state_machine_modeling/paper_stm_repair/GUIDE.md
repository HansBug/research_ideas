# paper_stm_repair/GUIDE.md — 后续 agent 工作纪律

## 1. 默认阅读顺序

处理本工作区时，默认按以下顺序阅读：

1. [README.md](./README.md)：确认当前 paper1 active 主线。
2. [SUMMARY.md](./SUMMARY.md)：获取轻量总账和下一步依赖。
3. [STATUS.md](./STATUS.md)：确认已完成 / 未完成事实和禁止主张。
4. [GUIDE.md](./GUIDE.md)：读取当前工作纪律。
5. [evidence/ledgers/paper1_strategy_asset_map.md](./evidence/ledgers/paper1_strategy_asset_map.md)：确认资产应 active / update / archive / historical。
6. [story/README.md](./story/README.md)：进入 paper story 专题。

任何后续 PR 如果需要使用历史 R5.7 / Better STM-facing 文件，必须先读 asset map，确认它们是否只是 historical / archive-pending。

## 2. Active 主线纪律

当前 active 主线是：**source-level behavioral issue discovery and closure**。

后续文档、方法和实验设计应围绕以下生命周期组织：

```text
NL + raw/source STM_0
  -> candidate issue discovery
  -> strict source-level confirmation
  -> confirmed issue ledger
  -> issue-grounded repair
  -> raw/source patch bundle or final raw/source STM_k
  -> closure / regression audit
```

不得重新把 active headline 写成：

- Better STM / which STM is better；
- `fcstm` / `pyfcstm` 建模语言贡献；
- ledger / audit / evidence bookkeeping 贡献；
- 一轮式 `NL -> STM` 生成；
- constructed `STM_k` adjudication；
- generic repair without source-level issue closure。

当前允许写成 paper1 contribution 的内容只有三类：

1. feedback-driven LLM refinement loop for existing STM artifacts；
2. diagnostics / inspect、simulation / probe、formal verification / check feedback 进入 loop 的 executable-feedback integration；
3. source-level repair output and empirical evaluation setup。

candidate / confirmed issue ledger、trace、attribution boundary、closure / regression audit、run record 和 post-pilot freeze discipline 均属于方法 / 评价 / 可复现纪律，不能写成 headline contribution。

## 3. 术语纪律

| 术语 | 必须含义 | 禁止误用 |
|---|---|---|
| raw/source `STM_0` | 输入的原始或源层状态机制品。 | 不把 canonical / fcstm 表示当成唯一评价对象。 |
| intermediate executable semantic representation | 用于 diagnostics / inspect / simulation / verification feedback 的中间执行表示。 | 不写成 paper1 contribution。 |
| candidate issue | 工具、LLM 或人工提示的可疑行为问题。 | 不直接计入 method success。 |
| confirmed source-level behavioral issue | 已回到 `NL + raw/source element + behavior evidence` 确认的问题。 | 不把 folded event / ugly expression 自动当确认问题。 |
| issue-grounded repair | 绑定 `issue_id` 的修复或 refinement。 | 不允许泛泛重写整个模型来声称变好。 |
| source-level patch bundle | 可回投到 raw/source 层解释的补丁、diff 或说明。 | 不把无法投影的中间改动算 closure。 |
| closure audit | 修复后判断原 issue closed / partially closed / not closed / over-repaired / unjudgeable。 | 不用单一 LLM 偏好判断替代证据链。 |
| regression audit | 检查修复是否引入新的 source-level issue。 | 不因原 issue 闭合就忽略新问题。 |

## 4. 资产使用纪律

资产状态以 [evidence/ledgers/paper1_strategy_asset_map.md](./evidence/ledgers/paper1_strategy_asset_map.md) 为准。

| decision | 使用方式 |
|---|---|
| `active` | 可直接作为当前基础设施或事实入口，但仍需遵守 contribution attribution。 |
| `update` | 只能在对应 PR 中改写后进入 active 主线。 |
| `archive` | 必须迁入 archive snapshot 后作为历史证据；归档前只能 archive-pending 引用。 |
| `historical` | 只解释“为什么转向”，不能作为 active claim evidence。 |

特别纪律：

1. R5.7 / Better STM-facing 资产在归档前不得作为 active evaluation framework。
2. `experiment_design/quality_model/`、`experiment_design/protocols/`、`experiment_design/better_adjudication_dry_run/`、`pipeline/evaluation/dry_run_examples/r5_7_5_*` 和 R5.7 reports 只能 historical / calibration 引用。
3. `corpora/repair_baselines/` 在 baseline contract 冻结前只作候选来源，不定义正式 baseline。
4. `discussions/` 和 `paper_v1/` 只作历史背景，不继承旧 claim wording。

## 5. Claim 与 evidence 纪律

- 每个强 claim 必须在 [story/claim_evidence_map.md](./story/claim_evidence_map.md) 中有 evidence 和 claim strength。
- planned work 只能写成 future / pending / protocol planning。
- pilot 前不得报告主实验数字、final metrics 或 baseline fairness 结论。
- 旧 dry-run 只支持 protocol calibration，不支持 method effectiveness。
- 若证据不足，应降低 claim 强度或标为 blocker。

## 6. PR 施工纪律

1. 复杂方法 / 协议 PR 先开 empty PR，body 写成 contract。
2. PR body 必须先过三路 review；C/I 未清零前不得进入实现。
3. 实现中若发现 scope 超出 body 或 asset map 漏项，应暂停并在 PR comment 写明需决策内容。
4. doc-only PR 不应新增 `runs/`、实验输出或 repair-loop run record。
5. review 必须做真实 dry-run：能否从入口找到事实源、能否判断该改哪些文件、能否回答 reviewer challenge。
6. 工程洁癖默认 M；只有影响学术目标、事实准确性、证据链或可复现性的问题才升级 C/I。

## 7. 静态检查建议

```bash
rg -n "Better STM|BetterSTM|which STM is better|relatively better|can_claim_better_stm|constructed STM_k|repair target taxonomy|fcstm.*contribution|conversion gain" \
  project_1_llm_state_machine_modeling/paper_stm_repair/README.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/SUMMARY.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/STATUS.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/GUIDE.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/story || true

rg -n "source-level|candidate issue|confirmed issue|closure|regression|issue-grounded|patch bundle|intermediate .*semantic" \
  project_1_llm_state_machine_modeling/paper_stm_repair/README.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/SUMMARY.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/STATUS.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/GUIDE.md \
  project_1_llm_state_machine_modeling/paper_stm_repair/story
```

高风险旧术语可以出现，但必须处于 historical / superseded / archive-pending / claims-to-avoid / forbidden claim 语境。

## 8. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-07-07 22:10:00 | GUIDE 增加 contribution 口径纪律：主贡献限于 loop + executable feedback integration + source-level repair/evaluation setup，ledger / audit 不作 headline contribution。 |
| 2026-07-07 21:20:00 | GUIDE 改为 source-level issue lifecycle 工作纪律，明确 asset map 优先级、fcstm attribution boundary 和 Better STM archive-pending 规则。 |
