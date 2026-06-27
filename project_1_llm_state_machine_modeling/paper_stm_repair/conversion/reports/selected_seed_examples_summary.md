# R3 selected_seed_examples 转换 v0 摘要

本文件由 `python -m paper_stm_repair_conversion.cli convert-selected` 生成，是 R3 reviewer fixture；它不是最终实验结果。

| example_id | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | syntax | structured export | losses | 说明 |
|---|---|---|---:|---:|---|---|---|---|---:|---|
| `llms-emp-gpt4o-hldcs` | `plantuml` | `converted` | 7 | 7 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 |  |
| `llms-emp-kimi-autonomous-collision` | `plantuml` | `converted` | 20 | 26 | `none` | `hierarchical` | `ok` | `scxml_export_ok` | 0 |  |
| `sefm-ssc7-umple` | `umple` | `partial` | 7 | 22 | `qualitative` | `flat` | `ok` | `scxml_export_ok` | 1 | Umple official SCXML rewrites after(...) timer-like transitions; R3 preserves this as targeted timing loss while canonical structure remains SCXML-derived. |
| `unified-uml-synthetic-0000` | `plantuml` | `converted` | 7 | 7 | `none` | `flat` | `ok` | `scxml_export_ok` | 0 |  |

Loss ledger 行数：1

所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。
