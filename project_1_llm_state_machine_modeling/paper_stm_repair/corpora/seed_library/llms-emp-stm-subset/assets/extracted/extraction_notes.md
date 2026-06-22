# extraction_notes

## 1. 下载与抽取

使用 `gdown.download_folder` 从论文给出的 Google Drive folder 下载一手资源。本条目只提交 seed registry 必需的最小一手资源：`Experiment Results.xlsx`、`Dataset.xlsx`、`README.md` 与下载元数据；Streamlit demo、向量索引、visualization 脚本和重复 ESE workbook 不进入 committed seed assets。

## 2. 当前全量抽取结果

`Experiment Results.xlsx` / `STM Results` 共 60 行，全部具备 `Requirement Description` 与 `Generation PlantUML`，并且 6 个 LLM 各 10 行：Claude、DeepSeek、GPT-4、GPT-4o、Kimi、Llama。

## 3. 风险

同一 sheet 同时含 reference `PlantUML`、format/grammar/semantic checking 后结果和评测列；抽取时只允许把 `Generation PlantUML` 作为原始 `STM_0`，其它列只可作 reference / leakage 风险说明。数据许可和再分发状态仍未知，因此条目保持 `conditional_final_pool`。
