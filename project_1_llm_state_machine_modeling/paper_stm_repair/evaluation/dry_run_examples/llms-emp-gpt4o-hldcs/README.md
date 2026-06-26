# 高层驾驶模块 PlantUML 完整 dry-run

## 1. R4 decision

| 字段 | 值 |
|---|---|
| `example_id` | `llms-emp-gpt4o-hldcs` |
| R3 status | `converted` |
| R3 code | `R3.STATUS.converted` |
| canonical | `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/canonical/llms-emp-gpt4o-hldcs.canonical_stm.json` |
| R4 decision | `complete` |
| model-level evaluation | `true` |
| repair-loop smoke | `true` |

## 2. 输入链接

- NL: [nl.txt](../../../selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt)
- STM_0: [stm0.puml](../../../selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml)
- R2 样例说明：[selected_seed_examples/llms-emp-gpt4o-hldcs/README.md](../../../selected_seed_examples/llms-emp-gpt4o-hldcs/README.md)
- R3 转换摘要：[selected_seed_examples_summary.md](../../../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[selected_seed_examples_conversion_report.json](../../../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 canonical: [llms-emp-gpt4o-hldcs.canonical_stm.json](../../../conversion/reports/canonical/llms-emp-gpt4o-hldcs.canonical_stm.json)

## 3. 为什么这样处理

R3 使用 PlantUML 官方 SCXML 导出生成 canonical，status=converted 且 losses_count=0，可完整验证 R4 字段链路。

## 4. Caveats

- R4 只是 gate dry-run，没有 STM_k 或 repair gain。

## 5. R4 fixture

| 文件 | 作用 |
|---|---|
| [eligibility_decision.json](./eligibility_decision.json) | 记录该样例能否进入 complete / focused / blocked dry-run。 |
| [diagnostic_draft.json](./diagnostic_draft.json) | 记录 R4 diagnostic draft 与 R3 evidence locator。 |
| [scenario_draft.json](./scenario_draft.json) | 记录最小 scenario / regression gate 草案。 |
| [better_stm_checklist.json](./better_stm_checklist.json) | 记录 Better STM 五条件 dry-run 判定；R4 默认不得 claim Better。 |
