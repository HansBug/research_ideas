# extraction_notes

## 1. 下载与抽取

使用 `gdown.download_folder` 从论文给出的 Google Drive folder 下载一手资源。本条目只提交 seed registry 必需的最小一手资源：`Experiment Results.xlsx`、`Dataset.xlsx`、`README.md` 与下载元数据；Streamlit demo、向量索引、visualization 脚本和重复 ESE workbook 不进入 committed seed assets。

## 2. 当前全量抽取结果

`Experiment Results.xlsx` / `STM Results` 共 60 行，全部具备 `Requirement Description` 与 `Generation PlantUML`，并且 6 个 LLM 各 10 行：Claude、DeepSeek、GPT-4、GPT-4o、Kimi、Llama。

## 3. 风险

同一 sheet 同时含 reference `PlantUML`、format/grammar/semantic checking 后结果和评测列；抽取时只允许把 `Generation PlantUML` 作为原始 `STM_0`，其它列只可作 reference / leakage 风险说明。公开学术资源按引用原作处理，许可 / 再分发不再作为升绿 blocker；本条目当前为 `final_pool_ready`，核心 caveat 是 reference / checking 列隔离。

## 4. Phase-II final 的独立用途

Issue #161 的最终 converter 验收另行使用 [`feedback_final_pairs.jsonl`](./feedback_final_pairs.jsonl)。论文说明 Phase-II 依次执行 PlantUML format、SysML grammar、SysML semantic 与 requirements consistency checking，并在每次反馈后 regeneration；workbook 对应结果列也按该顺序展开。因此 extractor 为每行选择最后一个非空 checking 输出，同时保留完整 lineage。

该文件是 conversion-validation pool，不是 paper1 原始生成 seed，也不能用于把作者反馈收益归因给本研究 repair loop。原始 Phase-I `STM_0` 的事实真源仍是 [`pairs.jsonl`](./pairs.jsonl)。
