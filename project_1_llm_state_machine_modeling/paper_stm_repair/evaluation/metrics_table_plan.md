# Metrics table plan v0

## 1. 目标

本文件预注册 R7/R8 结果表的字段骨架，避免后续根据 repair 结果临时挑选指标。R4 只冻结表头与解释，不填主实验数字。

## 2. 建议结果表

### Table A：eligibility / conversion attribution

| 字段 | 含义 |
|---|---|
| `seed_id` / `example_id` | 样例来源。 |
| `raw_format` | PlantUML / Umple / TTool XML 等。 |
| `r3_status` | `converted / partial / blocked / unsupported`。 |
| `conversion_losses` | R3 loss code 计数。 |
| `conversion_gain_counted_as_repair` | 必须为 `false`，除非单独实验条件。 |
| `r4_decision` | `complete / focused / blocked / supplementary`。 |

### Table B：diagnostic closure

| 字段 | 含义 |
|---|---|
| `run_id` | repair run 标识。 |
| `diagnostics_before_repair` | 转换后 `STM_0` 诊断计数。 |
| `diagnostics_after_repair` | `STM_k` 诊断计数。 |
| `new_blocking_diagnostics` | 新增 blocking 数量。 |
| `closed_must_fix` | `must_fix` 关闭数量。 |

### Table C：scenario / regression

| 字段 | 含义 |
|---|---|
| `scenario_count` | 冻结场景数量。 |
| `regression_gate_count` | 可作为回归门的场景数量。 |
| `pass_before` / `pass_after` | 修正前后通过数。 |
| `critical_regression_count` | 关键回归数量。 |
| `placeholder_or_unknown_count` | 不得计入主通过率的占位 / unknown 数。 |

### Table D：Better STM five-condition ledger

| 字段 | 含义 |
|---|---|
| `no_new_blocking_diagnostics` | pass/fail/unknown/not_applicable。 |
| `no_critical_regression_on_frozen_scenarios` | pass/fail/unknown/not_applicable。 |
| `improves_at_least_one_preregistered_dimension` | pass/fail/unknown/not_applicable。 |
| `no_nl_semantic_degradation` | pass/fail/unknown/not_applicable。 |
| `conversion_gain_separated_from_repair_gain` | pass/fail/unknown/not_applicable。 |
| `can_claim_better_stm` | 只有五项全 pass 才为 true。 |

## 3. 报告原则

1. 失败、回滚、不收敛、blocked 不能被静默删除。
2. 四例 smoke 结果只能作为开发证据，不进入主结果统计。
3. partial / inventory-only / no-canonical 样例必须单独分层报告。
4. 没有 Codecov 时不得虚构 coverage，只能说明本地测试与 GitHub smoke 的局限。
