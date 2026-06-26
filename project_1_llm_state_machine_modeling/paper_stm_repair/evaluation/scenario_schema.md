# R4 scenario / regression suite schema v0

## 1. 目标

R4 scenario schema 只定义后续 R5/R6/R7 可复用的最小场景结构。它不承诺本 PR 已具备完整仿真能力，也不把 dry-run 场景写成正式主实验。

## 2. 最小字段

| 字段 | 说明 |
|---|---|
| `scenario_id` | 稳定 ID，例如 `R4.SCENARIO.llms_hldcs_mode_switch`。 |
| `source_nl_ref` | 指向 `selected_seed_examples/<id>/nl.txt`。 |
| `source_stm_ref` | 指向 `stm0.*` 或 R3 canonical。 |
| `initial_state` | 初始状态；未知时可为 `null`，但必须说明原因。 |
| `event_sequence` | 事件 / 条件序列；R4 可为空数组表示 blocked / placeholder。 |
| `expected_observation` | 期望状态、迁移或人工断言。 |
| `oracle_type` | oracle 类型，见下表。 |
| `is_regression_gate` | 是否可作为回归门。placeholder 不得为 true。 |
| `blocking_on_failure` | 失败是否阻塞后续 Better STM claim。 |
| `evidence_locator` | 指向 NL、STM、canonical、R3 report 或 loss ledger。 |

## 3. oracle_type 枚举

| 值 | 含义 | 可作为 regression gate |
|---|---|---:|
| `reachability` | 检查某状态可达。 | 是，若 evidence 明确。 |
| `transition_presence` | 检查某迁移存在。 | 是，若 source/target/event 明确。 |
| `forbidden_transition` | 检查不应存在的迁移。 | 是，若 NL 明确禁止。 |
| `trace_prefix` | 检查 trace 前缀或事件序列。 | 是，若语义明确。 |
| `human_assertion` | 人工裁决断言。 | 可作为辅助，不宜单独作自动门。 |
| `placeholder` | 字段占位或设计讨论。 | 否。 |

## 4. blocked / partial 规则

1. `partial` 样例可有 focused scenario，但必须在 `limitations` 中列出 R3 loss。
2. `blocked` 样例可以有 `placeholder` scenario 来记录为何不能构造回归门。
3. no-canonical 样例不得伪造 initial state、transition 或 trace。
4. 若 scenario 使用 `placeholder` 或关键 `unknown`，对应 Better STM checklist 不能 pass。

## 5. JSON schema

场景 suite 由 [schemas/scenario.schema.json](./schemas/scenario.schema.json) 约束。
