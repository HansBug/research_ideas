# R5.7.4 裁决样例 baseline `.fcstm` bundle

本目录保存 R5.7.4 为 `repair_target_adjudication/` 补齐的两个 standalone baseline 表示包：`llms_emp_stm_results_0001` 与 `llms_emp_stm_results_0018`。它们不是 `selected_seed_examples/` 的新增 smoke 样例，也不是 `STM_k` 或 repair 结果；它们只是把 R5 seed-sweep 中已经存在的 `.fcstm_sha256`、parse ok、inspect ok 结果物化成可直接打开和复验的 baseline evidence bundle。

## 目录内容

| 路径 | pair | 作用 |
|---|---|---|
| [llms-emp-gpt4o-hstbs/](./llms-emp-gpt4o-hstbs/) | `llms_emp_stm_results_0001` | T0 / FSM / low-noise control 的 standalone baseline `.fcstm` bundle。 |
| [llms-emp-gpt4-digital-camera/](./llms-emp-gpt4-digital-camera/) | `llms_emp_stm_results_0018` | T1 supplementary stress 的 standalone baseline `.fcstm` bundle。 |
| [r5_7_4_adjudication_fcstm_export_report.json](./r5_7_4_adjudication_fcstm_export_report.json) | 两例总账 | 记录 bundle 路径、hash、parse / inspect 状态、来源与 `repair_contribution_allowed=false`。 |
| [r5_7_4_adjudication_fcstm_export_loss_ledger.jsonl](./r5_7_4_adjudication_fcstm_export_loss_ledger.jsonl) | 两例合并 loss ledger | 合并 representation lowering loss；只能作为 readiness / caveat 证据，不能计 repair gain。 |

每个 pair 子目录包含：

- `model.fcstm`：物化后的 baseline 表示。
- `canonical_stm.json`：从 committed R3.1 official PlantUML SCXML probe 重建的 canonical STM。
- `name_mapping.json`：raw label 到 pyfcstm identifier 的映射。
- `lowering_inventory.json`：lowering 盘点与 `source_traceability`。
- `parse_inspect_report.json`：pyfcstm parse / inspect 结果。
- `fcstm_export_loss_ledger.jsonl`：该 pair 的 lowering loss rows。
- `bundle_meta.json`：bundle 总元数据、hash 与来源路径。

## 使用纪律

1. 本目录只用于 R5.7.4 静态裁决和 R5.7.5 constructed `STM_k` Better adjudication dry-run 的 baseline evidence。
2. 不要把这里的 `.fcstm` 当作论文贡献、人工修复结果或 `STM_k`。
3. 0001 / 0018 后续不应再被写成“缺 standalone `.fcstm`”；正确口径是：seed-sweep 早已有 hash / parse / inspect，R5.7.4 已补齐 standalone bundle。
4. R5.7.5 若构造候选 `STM_k`，必须同时记录 baseline hash、candidate hash、change ledger、target-instance ledger 和 Better gate 裁决。
