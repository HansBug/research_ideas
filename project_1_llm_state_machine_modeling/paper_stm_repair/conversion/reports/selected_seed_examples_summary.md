# R3 selected_seed_examples 转换 v0 摘要

本文件由 `python -m paper_stm_repair_conversion.cli convert-selected` 生成，是 R3 reviewer fixture；它不是最终实验结果。

| example_id | 上游 NL | 原始 STM_0 | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | syntax | structured export | losses | 说明 |
|---|---|---|---|---|---:|---:|---|---|---|---|---:|---|
| `llms-emp-deepseek-microwave` | [nl.txt](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-deepseek-microwave/nl.txt) | [stm0.puml](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml) | `plantuml` | `converted` | 17 | 20 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 | R3.1 normalization replay 后重新走官方 SCXML；raw STM_0 不覆盖，不计 repair gain。 |
| `llms-emp-gpt4o-hldcs` | [nl.txt](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt) | [stm0.puml](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml) | `plantuml` | `converted` | 7 | 7 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 |  |
| `llms-emp-kimi-autonomous-collision` | [nl.txt](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-kimi-autonomous-collision/nl.txt) | [stm0.puml](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml) | `plantuml` | `converted` | 20 | 26 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 |  |
| `sefm-ssc7-umple` | [nl.txt](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/sefm-ssc7-umple/nl.txt) | [stm0.ump](../../../../project_1_llm_state_machine_modeling/paper_stm_repair/selected_seed_examples/sefm-ssc7-umple/stm0.ump) | `umple` | `partial` | 7 | 22 | `qualitative` | `flat` | `ok` | `scxml_export_ok` | 1 | Umple official SCXML rewrites after(...) timer-like transitions; R3 preserves this as targeted timing loss while canonical structure remains SCXML-derived. |

Loss ledger 行数：1

所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。
