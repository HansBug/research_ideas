# field_mapping

| extracted 字段 | raw 来源 |
|---|---|
| `nl_text` | `assets/raw/umlcode_state_diagram_train.parquet` 的 `input` 列 |
| `stm0_text` | 同一 parquet 的 `uml_code` 列 |
| `source_locator` | `row=<idx>; columns=input,uml_code,reasoning` |
| `generation_model_or_method` | 论文与 HF dataset 描述的 synthetic requirements -> PlantUML 生成流水线 |

本映射只覆盖本 PR 抽取的前三行审计样例；完整行级抽取应复用相同字段映射并由 validator 复算。
