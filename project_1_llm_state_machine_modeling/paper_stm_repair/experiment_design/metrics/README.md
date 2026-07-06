# metrics/ — 指标与统计职责入口

本目录维护指标定义、统计表字段候选、报告口径、降级写法和可视化表格骨架。

当前状态：R5.7.3 已冻结客观代理指标框架 v0，主入口是 [objective_metric_framework.md](./objective_metric_framework.md)。该框架只定义 objective metrics 作为 Better STM gate 的证据层，不冻结最终阈值、统计检验、主结果表列或真实 repair 效果。

后续指标必须对应 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 的 G0--G6 判定条件，并避免看结果后倒推阈值。

## R5.7.1 已冻结的指标纪律

[../evaluation_logic.md](../evaluation_logic.md) 已冻结：客观指标只能作为 supporting evidence，不能单独判 Better STM。R5.7.3 已新增 [objective_metric_framework.md](./objective_metric_framework.md)，每个指标族至少需要写明：

| 字段 | 要求 |
|---|---|
| 指标层 | hard gate、structural element、traceability、scenario / behavior、cost / stability 或 semantic adjudication。 |
| 偏序方向 | 明确什么算更好，例如 `parse valid: true > false`、`untraced additions: fewer is better`。 |
| 适用边界 | 说明适用于 T0、T0.5 caveat、T1 stress 还是仅作辅助。 |
| 投机风险 | 说明如何防止刷指标，例如删除语义、折叠 guard/action、只优化总 F1。 |
| 语义裁决接口 | 说明何时回到 `NL`、原始 / 规范化 `STM_0`、candidate `STM_k` 与 change ledger 裁决。 |

禁止把 parse ok、inspect ok、diagnostics fewer、总体 F1 更高、场景通过率更高、文本相似度更高、conversion success 或低 token cost 单独写成 Better STM 或方法有效性证据。

## R5.7.2 已冻结的指标权限上限

R5.7.2 进一步明确：指标是 Better STM gate 的证据材料，不是 verdict 本身。R5.7.3 设计 objective metrics 时必须继承以下权限上限：

| 指标类型 | 可支持 | 不可支持 |
|---|---|---|
| parse / schema / inspect | A gate、run validity。 | Better STM 成功。 |
| diagnostics fewer | improvement gate 的候选证据。 | 语义更优的充分条件。 |
| guard/action/state coverage | structural / semantic target 的代理证据。 | 不经 NL-grounded 裁决的修复成功。 |
| scenario pass rate | no-regression / behavior obligation 的局部证据。 | 覆盖全部需求或消除 semantic drift。 |
| F1 / accuracy | 只有存在 adjudicated reference target 时可用。 | 默认总分或通用质量标签。 |
| token / iteration cost | 稳定性和可用性辅助证据。 | 模型质量或 repair effectiveness。 |

若某个候选 `STM_k` 指标变好但违反 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 的 semantic gate、attribution gate 或 no-regression gate，必须判为 `not_better`、`partial` 或 `unknown`，不能以指标覆盖语义问题。


## R5.7.3 已冻结的客观指标框架

[objective_metric_framework.md](./objective_metric_framework.md) 是 R5.7.3 的长期规则真源，已冻结：

1. 五级 `metric_permission`：`hard_gate / supporting_evidence / trigger_only / report_only / forbidden`。
2. v0 指标族：readiness、provenance、diagnostics、structural element、traceability、scenario behavior、semantic target closure、cost stability、baseline/textual background。
3. G0--G6 gate × metric matrix。
4. structural slot：state、transition、event、guard、action、hierarchy_or_pseudostate、trace_link。
5. 无统一 gold STM 时的 reference、分母与 P/R/F1 降级纪律。
6. anti-gaming 风险标签与 semantic adjudication evidence bundle。
7. T0 / T0.5 / T1 的 `scope_applicability`、`headline_inclusion` 和 pair / cluster / LLM-family 汇总纪律。
8. semantic target closure 分层统计，禁止单一 closure 总分。
9. baseline 指标迁移表与 `llms_emp.Acc_P / Acc_S` 命名降级。

阅读顺序：先读 [../evaluation_logic.md](../evaluation_logic.md) 理解评价逻辑链，再读 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 与 [../quality_model/repair_target_taxonomy.md](../quality_model/repair_target_taxonomy.md) 理解 Better STM gate 和 repair target，最后读 [objective_metric_framework.md](./objective_metric_framework.md) 理解客观指标如何进入 gate。

## 仍未冻结的内容

以下内容仍由 R7 / R8 正式协议冻结，不属于 R5.7.3：

- numeric thresholds；
- statistical test / effect size plan；
- final eligibility filter；
- final success denominator；
- final primary / secondary endpoints；
- Better STM success rate 或 repair effectiveness result。
