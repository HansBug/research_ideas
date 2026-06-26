# Better STM checklist v0

## 1. 来源

本 checklist 直接操作化 [../experiment_design/better_stm_definition.md](../experiment_design/better_stm_definition.md) 中的定义：

```text
Better(STM_k, STM_0 | NL, S, D, R)
```

R4 没有 `STM_k`，因此本目录中的 checklist 是评价门 dry-run：验证字段、证据与聚合逻辑可执行，而不是声称任何样例已经 Better。

## 2. 五条件

| 字段 | 条件 | R4 判定要点 |
|---|---|---|
| `no_new_blocking_diagnostics` | `STM_k` 不得引入新的 blocking diagnostics。 | R4 无 `STM_k` 时通常 `not_applicable`；若 R3 已 no-canonical，可记为 `fail` 支撑 blocked。 |
| `no_critical_regression_on_frozen_scenarios` | 冻结场景 / 回归不退化。 | placeholder / unknown oracle 不能 pass。 |
| `improves_at_least_one_preregistered_dimension` | 至少一个预注册维度改善。 | R4 无 repair candidate，不能 pass。 |
| `no_nl_semantic_degradation` | 基于 NL 的裁决不退化。 | partial / no-canonical 通常 `unknown` 或 `not_applicable`。 |
| `conversion_gain_separated_from_repair_gain` | conversion / normalization gain 与 repair gain 分离。 | R4 应明确 `pass`，并把 R3/R3.1 gain 标为不可计入 repair。 |

## 3. 聚合规则

1. 只有五条件全部为 `pass` 时，`can_claim_better_stm=true`。
2. 任一条件 `fail`，整体为 `not_better` 或 `not_evaluable`。
3. 任一关键条件 `unknown`，整体不得为 Better STM。
4. `not_applicable` 不能当作 `pass`；R4 dry-run 默认 `can_claim_better_stm=false`。
5. R3/R3.1 conversion / normalization 改善只能进入 conversion attribution，不得进入 repair gain。

## 4. JSON schema

Checklist fixture 由 [schemas/better_stm_checklist.schema.json](./schemas/better_stm_checklist.schema.json) 约束。
