# R3 selected_seed_examples 转换 v0 摘要

本文件由 `python -m paper_stm_repair_conversion.cli convert-selected` 生成，是 R3 reviewer fixture；它不是最终实验结果。

| example_id | 格式 | status | 状态数 | 迁移数 | timing | hierarchy | losses | 说明 |
|---|---|---|---:|---:|---|---|---:|---|
| `llms-emp-gpt4o-hldcs` | `plantuml` | `converted` | 9 | 7 | `none` | `hierarchical` | 0 |  |
| `sefm-ssc7-umple` | `umple` | `partial` | 7 | 22 | `qualitative` | `flat` | 1 | Umple adapter preserved after(...) timer-like transitions but R3 canonical T0 semantics does not execute timing. |
| `ttool-automatedbraking-xml` | `ttool_xml` | `partial` | 245 | 233 | `timed_constraints` | `concurrent` | 2 | TTool XML adapter performs XML/SMD inventory only: it extracts AVATAR SMD panels, state/start components and transition connector records, but does not yet resolve graphical connecting points to exact source/target states or slice a pure T0 state machine from the full SysML/AVATAR artifact. |
| `unified-uml-synthetic-0000` | `plantuml` | `converted` | 7 | 7 | `none` | `flat` | 0 |  |

Loss ledger 行数：3

所有 `partial` / `blocked` 裁决必须回到 JSON report 与 loss ledger 查看 source/ref、code 与 blocking reason。
