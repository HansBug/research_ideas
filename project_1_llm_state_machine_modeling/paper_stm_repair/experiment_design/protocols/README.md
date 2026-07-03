# protocols/ — 实验协议职责入口

本目录预留真实修正循环、对照 / 消融、人工裁决、回滚、重试和审计协议。

当前状态：仅冻结职责入口，尚未冻结主实验协议，也未声明任何真实 LLM 运行已完成。

后续协议必须先于真实结果冻结，并记录输入输出、模型配置、失败处理、redaction、run record 和复验方式。

## R5.7.1 已冻结的后续协议接口

R5.7.1 已在 [../evaluation_logic.md](../evaluation_logic.md) 中冻结以下接口，供 R5.7.5 / R6 / R7 / R8 继承：

1. repair gain 只能从 canonical `STM_0 -> STM_k` 开始计算；raw -> canonical 的 conversion / normalization / representation lowering 不计 repair gain。
2. 每个 repair run 必须保留 change-level attribution ledger，至少能说明 source artifact、canonical baseline hash、candidate hash、change type、证据来源、是否可计 repair gain 和禁止归因理由。
3. failure、partial、unknown、out-of-scope、rollback、oscillation、non-convergence 必须进入可审计 ledger；不能只保存 success。
4. 真实 LLM 调用仍需遵守仓库 `.env`、provider、model id、prompt、raw output、usage、redaction 与 run record 纪律；当前 R5.7.1 不调用真实 LLM。

## R5.7.2 已冻结的语义裁决接口

R5.7.2 在 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 中冻结 semantic gate：Better STM 的最终正向判定必须回到 `NL + raw STM_0 + canonical STM_0 + STM_k + conversion ledger + change ledger + diagnostics + scenario trace + rubric output` 的完整 evidence bundle。

后续人工 / LLM-as-Judge / 结构化裁决协议至少应满足：

1. **规则先处理 hard facts**：scope、A gate、ledger 完整性、schema / parse、明显删除需求行为、明显无 trace 新增。
2. **LLM-as-Judge 只能 provisional**：必须输出结构化 verdict、证据引用、置信度、冲突项和 forbidden extrapolation；不得作为 gold label 直接统计。
3. **人工处理冲突与 headline audit**：LLM 与规则冲突、低置信度、headline success、代表性 failure 都需要人工升级。
4. **change-level attribution 必须存在**：每个候选变化都要说明是否来自 canonical `STM_0 -> STM_k`，不能把 raw -> canonical 的 conversion / normalization 收益写成 repair gain。
5. **规则修订必须 evidence-driven**：R5.7.4 / R7 若发现本协议不足，必须先记录 dry-run finding、旧规则失败点和修订理由，再更新协议；没有真实 finding 的改动只能标为 provisional。
