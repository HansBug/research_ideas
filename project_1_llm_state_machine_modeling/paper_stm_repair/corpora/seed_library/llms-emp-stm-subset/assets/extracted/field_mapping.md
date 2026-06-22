# field_mapping

| extracted 字段 | workbook 来源 |
|---|---|
| `nl_text` | `assets/raw/drive_download/Experiment Results.xlsx` / `STM Results` / `Requirement Description` |
| `stm0_text` | 同一 workbook / `STM Results` / `Generation PlantUML` |
| `generation_model_or_method` | `STM Results` / `LLMs` |
| `model_source` | `STM Results` / `Model Source` |
| `model_name` | `STM Results` / `Model Name` |
| reference | `STM Results` / `PlantUML`，只能作为 reference，不计原始 `STM_0` |
| postprocessed | `Result with Format/Grammar/Semantic Checking`，不得作为原始 `STM_0` |

本映射覆盖当前 committed Google Drive workbook 中 `STM Results` 的 60 行。validator 用 `sheet + row + columns + workbook sha256` 回溯每一条 `Requirement Description + Generation PlantUML`。
