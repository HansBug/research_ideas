# 合成点餐菜单 PlantUML no-canonical blocked dry-run

## 1. R4 decision

| 字段 | 值 |
|---|---|
| `example_id` | `unified-uml-synthetic-0000` |
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | `无` |
| R4 decision | `blocked` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

## 2. 输入链接

- NL: [nl.txt](../../../selected_seed_examples/unified-uml-synthetic-0000/nl.txt)
- STM_0: [stm0.puml](../../../selected_seed_examples/unified-uml-synthetic-0000/stm0.puml)
- R2 样例说明：[selected_seed_examples/unified-uml-synthetic-0000/README.md](../../../selected_seed_examples/unified-uml-synthetic-0000/README.md)
- R3 转换摘要：[selected_seed_examples_summary.md](../../../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[selected_seed_examples_conversion_report.json](../../../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 loss ledger: [selected_seed_examples_loss_ledger.jsonl](../../../conversion/reports/selected_seed_examples_loss_ledger.jsonl)

## 3. 为什么这样处理

No-canonical 样例用于验证 R4 能正确 blocked，而不是伪造模型级 evaluation。

## 4. Caveats

- PlantUML 官方 syntax check failed；R3 不信任 SCXML 导出。
- 没有 canonical STM；不得使用 source-text regex 或旧 fixture 冒充转换结果。
- synthetic / non-control-domain，只能作为格式边界样例。

## 5. R4 fixture

| 文件 | 作用 |
|---|---|
| [eligibility_decision.json](./eligibility_decision.json) | 记录该样例能否进入 complete / focused / blocked dry-run。 |
| [diagnostic_draft.json](./diagnostic_draft.json) | 记录 R4 diagnostic draft 与 R3 evidence locator。 |
| [scenario_draft.json](./scenario_draft.json) | 记录最小 scenario / regression gate 草案。 |
| [better_stm_checklist.json](./better_stm_checklist.json) | 记录 Better STM 五条件 dry-run 判定；R4 默认不得 claim Better。 |
