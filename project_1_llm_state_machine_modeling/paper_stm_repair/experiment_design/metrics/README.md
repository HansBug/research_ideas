# metrics/ — 指标与统计职责入口

本目录预留指标定义、统计表字段、报告口径、降级写法和可视化表格骨架。

当前状态：仅冻结职责入口，尚未冻结最终指标、阈值、统计检验或主结果表。

后续指标必须对应 [../quality_model/better_stm_definition.md](../quality_model/better_stm_definition.md) 的判定条件，并避免看结果后倒推阈值。

## R5.7.1 已冻结的指标纪律

[../evaluation_logic.md](../evaluation_logic.md) 已冻结：客观指标只能作为 supporting evidence，不能单独判 Better STM。后续 R5.7.3 若新增 `objective_metric_framework.md`，每个指标族至少需要写明：

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
