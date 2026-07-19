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

## Phase-II final conversion-validation pool

[`feedback_final_pairs.jsonl`](./feedback_final_pairs.jsonl) 不替代上述 Phase-I seed。它专门用于 Issue #161 的最终转换验收，按论文所述的顺序 regeneration 流程，为每行选择最后一个非空阶段：

1. `Result with Semantic Checking`
2. `Result with Grammar Checking`
3. `Result with Format Checking`
4. `Generation PlantUML`（该行没有任何 checking 输出时的 fail-safe 回退）

当前 60 行中 `58` 行选择 semantic checking，`2` 行回退 generation；`52/60` 相对 Phase-I 发生变化。每行同时保存全部非空 stage 的 hash、最终选择列、Excel 行号与 Phase-I hash。reference `PlantUML` 仍只保存 hash，绝不参与选择。
