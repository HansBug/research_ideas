# R4 eligibility policy v0

## 1. 目标

Eligibility policy 决定 R3 输出能否进入 R4/R5/R6 的不同层级 dry-run。它只处理开发 / smoke / protocol 草案，不冻结 R7 主实验最终纳入规则。

## 2. R3 status 到 R4 decision

| R3 状态 / 来源 | R4 decision | 允许事项 | 禁止事项 |
|---|---|---|---|
| `converted` + official SCXML/XML canonical | `complete` | 完整 diagnostic / scenario / checklist dry-run；可进入 R5 deterministic smoke。 | 不得声称已有 repair gain。 |
| `partial` + canonical 可用 | `focused` | limited diagnostic / scenario dry-run；必须携带 loss caveat。 | 不得无 caveat 进入模型级 Better STM。 |
| `partial` + inventory-only canonical | `focused` 或 `supplementary` | inventory-level diagnostic、边界说明。 | 不得冒充纯 T0 状态机。 |
| `partial` + no canonical conversion | `blocked` | blocked / diagnostic-only / toolchain-boundary analysis。 | 不得做模型级 evaluation 或 repair proposal。 |
| `blocked / unsupported` | `blocked` | 记录原因、风险和后续修复建议。 | 不进入 R5/R6 model-level smoke。 |

## 3. R3.1 recovery 规则

R3.1 `main_eligibility_included=466` 表示 PlantUML 转换前 normalization/recovery 后的主 eligibility 线索。它可用于 R7/R8 扩大候选池，但不能在 R4/R5/R6 中被写成 Better STM repair gain。

## 4. 决策字段

每个 dry-run 样例必须有 `eligibility_decision.json`，至少说明：

- R3 `status` 与 `status_reason_code`
- canonical 是否存在
- `r4_dry_run_decision`
- diagnostic / scenario / model-level / repair-loop smoke 是否允许
- required caveats
- evidence locators

Schema 见 [schemas/eligibility_decision.schema.json](./schemas/eligibility_decision.schema.json)。
