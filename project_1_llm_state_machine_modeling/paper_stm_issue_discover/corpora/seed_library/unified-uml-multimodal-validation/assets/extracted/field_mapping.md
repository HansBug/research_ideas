# field_mapping

| extracted 字段 | raw 来源 |
|---|---|
| `nl_text` | `assets/raw/umlcode_state_diagram_train.parquet` 的 `input` 列 |
| `stm0_text` | 同一 parquet 的 `uml_code` 列 |
| `source_locator` | `row=<idx>; columns=input,uml_code,reasoning` |
| `generation_model_or_method` | 论文与 HF dataset 描述的 synthetic requirements -> PlantUML 生成流水线 |

本映射覆盖当前 committed parquet 的全量 999 行；validator 会逐行用 `source_locator` 回到 raw parquet 复算文本和哈希。有效 PlantUML 行计入 eligible，`No valid PlantUML code found.` 行只保留为生成失败证据，不计可用 seed。
