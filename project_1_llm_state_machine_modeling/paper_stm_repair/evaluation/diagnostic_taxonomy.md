# R4 diagnostic taxonomy v0

## 1. 目标

R4 diagnostic taxonomy 用于统一记录状态机问题、证据来源、严重级别和与 Better STM 五条件的关系。它不是最终缺陷分类论文贡献，而是 repair loop 前的评价门草案。

## 2. 顶层 code family

| code 前缀 | 类别 | 典型来源 |
|---|---|---|
| `R4.DIAG.r3_conversion.*` | R3 转换 / 工具链 / loss 映射 | R3 report、canonical JSON、loss ledger。 |
| `R4.DIAG.syntax.*` | 语法或解析问题 | 官方工具链、parser、schema validation。 |
| `R4.DIAG.semantic.*` | 状态 / 迁移 / guard / action 语义问题 | canonical STM、NL 对照、人工裁决。 |
| `R4.DIAG.scenario.*` | 场景 / 回归 oracle 问题 | scenario suite dry-run。 |
| `R4.DIAG.traceability.*` | 证据链 / locator 缺失 | 文件路径、hash、raw locator。 |
| `R4.DIAG.boundary.*` | 超出 T0 / no-canonical / inventory-only 边界 | partial / blocked 样例。 |

## 3. source_stage 枚举

| 值 | 含义 |
|---|---|
| `r3_conversion` | 来自 R3 转换报告、canonical JSON 或 loss ledger。 |
| `static_semantic` | 来自静态结构检查。 |
| `design_rule` | 来自设计规则或表示纪律。 |
| `scenario` | 来自场景 / 回归 suite。 |
| `human_review` | 来自人工 rubric 或裁决。 |
| `unknown` | 暂无可靠来源；不得支撑 Better STM claim。 |

## 4. severity 枚举

| severity | 阻塞含义 | 默认处理 |
|---|---|---|
| `blocking` | 阻止模型级 evaluation 或 Better STM claim。 | 必须修复或降级为 blocked / supplementary。 |
| `high` | 显著影响语义、结构或实验纳入。 | R7 前必须裁决。 |
| `medium` | 影响局部维度或需要人工 caveat。 | 可进入 focused dry-run。 |
| `low` | 轻微问题或记录性 caveat。 | 不单独阻塞。 |
| `info` | 事实记录。 | 不阻塞。 |

## 5. repair_relevance 枚举

| 值 | 含义 |
|---|---|
| `must_fix` | 若进入 repair loop，必须被修复或显式拒绝。 |
| `should_fix` | 建议修复；未修复需说明风险。 |
| `monitor` | 用于回归监控，不一定作为 repair 目标。 |
| `not_repair_target` | 不是 repair loop 目标，例如 conversion-only loss 或工具链边界。 |

## 6. R3 到 R4 映射

| R3 code / 状态 | R4 diagnostic 建议 | 说明 |
|---|---|---|
| `R3.STATUS.converted` | `R4.DIAG.r3_conversion.converted` | 可作为完整 dry-run 前提，但不是 Better STM 改善证据。 |
| `R3.LOSS.timing.medium` | `R4.DIAG.r3_conversion.timing_loss` | 不得把 timing loss 自动当作 repair gain 机会。 |
| `R3.LOSS.structure.high` | `R4.DIAG.r3_conversion.structure_loss` | 对 TTool inventory-only 样例阻止模型级 Better STM。 |
| `R3.LOSS.tooling.high` | `R4.DIAG.boundary.no_canonical_conversion` | no-canonical 样例只能 blocked / diagnostic-only。 |
| R3.1 `main_eligibility_included` | `R4.DIAG.r3_conversion.eligibility_recovered` | 只表示 conversion eligibility 线索，不表示 repair 收益。 |

## 7. JSON 结构

Machine-readable diagnostic bundle 由 [schemas/diagnostic.schema.json](./schemas/diagnostic.schema.json) 约束。每条 diagnostic 至少要包含 code、source stage、severity、repair relevance、Better STM 条件链接和 evidence locator。
