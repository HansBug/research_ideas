# protocols/ — 实验协议职责入口

本目录预留真实修正循环、对照 / 消融、人工裁决、回滚、重试和审计协议。

当前状态：仍未冻结主实验协议。R5.7.5 已完成 constructed answer-key suite 与 full blind adjudication protocol dry-run，并保存 Claude / DeepSeek / Codex 三方 isolated judge 输出；这些运行只验证评价协议可执行，不是 repair loop，也不构成真实修正效果。

后续协议必须先于真实结果冻结，并记录输入输出、模型配置、失败处理、redaction、run record 和复验方式。

## R5.7.1 已冻结的后续协议接口

R5.7.1 已在 [../evaluation_logic.md](../evaluation_logic.md) 中冻结以下接口，供 R5.7.5 / R6 / R7 / R8 继承：

1. repair gain 只能从 canonical `STM_0 -> STM_k` 开始计算；raw -> canonical 的 conversion / normalization / representation lowering 不计 repair gain。
2. 每个 repair run 必须保留 change-level attribution ledger，至少能说明 source artifact、canonical baseline hash、candidate hash、change type、证据来源、是否可计 repair gain 和禁止归因理由。
3. failure、partial、unknown、out-of-scope、rollback、oscillation、non-convergence 必须进入可审计 ledger；不能只保存 success。
4. 真实 LLM 调用仍需遵守仓库 `.env`、provider、model id、prompt、raw output、usage、redaction 与 run record 纪律；R5.7.1 本身不调用真实 LLM，R5.7.5 blind judge 调用也只属于 evaluation protocol dry-run，不属于 repair run。

## R5.7.2 已冻结的语义裁决接口

R5.7.2 在 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 中冻结 semantic gate：Better STM 的最终正向判定必须回到 `NL + raw STM_0 + canonical STM_0 + STM_k + conversion ledger + change ledger + diagnostics + scenario trace + rubric output` 的完整 evidence bundle。

后续人工 / LLM-as-Judge / 结构化裁决协议至少应满足：

1. **规则先处理 hard facts**：scope、A gate、ledger 完整性、schema / parse、明显删除需求行为、明显无 trace 新增。
2. **LLM-as-Judge 只能 provisional**：必须输出结构化 verdict、证据引用、置信度、冲突项和 forbidden extrapolation；不得作为 gold label 直接统计。
3. **人工处理冲突与 headline audit**：LLM 与规则冲突、低置信度、headline success、代表性 failure 都需要人工升级。
4. **change-level attribution 必须存在**：每个候选变化都要说明是否来自 canonical `STM_0 -> STM_k`，不能把 raw -> canonical 的 conversion / normalization 收益写成 repair gain。
5. **规则修订必须 evidence-driven**：R5.7.4 / R7 若发现本协议不足，必须先记录 dry-run finding、旧规则失败点和修订理由，再更新协议；没有真实 finding 的改动只能标为 provisional。


## R5.7.5 constructed STM_k 与 blind 裁决协议 dry-run 接口

R5.7.5 新增 [better_adjudication_prompt_v0.md](./better_adjudication_prompt_v0.md)、[better_adjudication_output_schema_v0.json](./better_adjudication_output_schema_v0.json) 与 [better_adjudication_prompt_dry_run_notes.md](./better_adjudication_prompt_dry_run_notes.md)，用于冻结 constructed `STM_k` answer-key suite 的裁决输入输出纪律。

R5.7.5 随后新增 [better_adjudication_blind_prompt_v0.md](./better_adjudication_blind_prompt_v0.md) 与 [better_adjudication_blind_output_schema_v0.json](./better_adjudication_blind_output_schema_v0.json)，用于 full blind adjudication：judge 只能读取 blind packet，不得看到 expected verdict、oracle mapping、Cxx answer-key slug、构造意图或 PR 讨论上下文。

这些文件只验证评价协议能否处理 `better / not_better / partial / unknown / stmk_repair_failure / protocol_or_provenance_invalid / stress_t1` 等路径，并校准 LLM semantic judge 与 deterministic scorer 的职责边界；不代表真实 repair loop 已运行，也不支持 repair effectiveness 主张。

配套阅读入口：

1. canonical 总报告：[../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md](../../reports/2026-07-05-07-18-31-r5-7-5-full-blind-adjudication-dry-run.md)
2. constructed 人类报告：[../../reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md](../../reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md)
3. 20 case 人类文档：[../better_adjudication_dry_run/README.md](../better_adjudication_dry_run/README.md)
4. constructed 机器 evidence bundle：[../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/README.md](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/README.md)
5. blind 机器 evidence bundle：[../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/README.md](../../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/README.md)

后续 R6/R7 若复用本协议，必须先把 parse/hash/provenance/identity/schema/transport 等机械事实做成 deterministic preflight blocker；LLM-as-Judge 只能处理语义裁决，不得替代这些机械检查。
