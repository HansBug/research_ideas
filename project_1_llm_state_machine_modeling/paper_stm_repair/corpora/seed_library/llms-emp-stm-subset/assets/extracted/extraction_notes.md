# extraction_notes

## 1. 下载与抽取

使用 `gdown.download_folder` 从论文给出的 Google Drive folder 下载一手资源。本条目只提交 seed registry 必需的最小一手资源：`Experiment Results.xlsx`、`Dataset.xlsx`、`README.md` 与下载元数据；Streamlit demo、向量索引、visualization 脚本和重复 ESE workbook 不进入 committed seed assets。

## 2. 当前全量抽取结果

`Experiment Results.xlsx` / `STM Results` 共 60 行，全部具备 `Requirement Description` 与 `Generation PlantUML`，并且 6 个 LLM 各 10 行：Claude、DeepSeek、GPT-4、GPT-4o、Kimi、Llama。

## 3. 风险

同一 sheet 同时含 reference `PlantUML`、format/grammar/semantic checking 后结果和评测列。Phase-I 原始 `STM_0` 只允许来自 `Generation PlantUML`，并独立冻结在 [`phase_i_pairs.jsonl`](./phase_i_pairs.jsonl)；默认 Discover pool 则显式读取作者 feedback-final 选择，不得把两种口径混写。公开学术资源按引用原作处理，许可 / 再分发不再作为升绿 blocker；核心 caveat 是 reference / checking 列隔离与作者 checking 收益归因。

## 4. author-feedback-final 的默认用途

Issue #161 的最终 converter 验收与 Discover 默认输入使用 [`feedback_final_pairs.jsonl`](./feedback_final_pairs.jsonl)；默认 [`pairs.jsonl`](./pairs.jsonl) 是它的字节相同消费槽位。论文说明 Phase-II 依次执行 PlantUML format、SysML grammar、SysML semantic 与 requirements consistency checking，并在每次反馈后 regeneration；workbook 对应结果列也按该顺序展开。因此 extractor 为每行选择最后一个非空 checking 输出，同时保留完整 lineage。

该文件是 author-feedback-final pool，不是 paper1 原始生成 seed，也不能用于把作者反馈收益归因给本研究 repair loop。原始 Phase-I `STM_0` 的 JSONL 事实真源是 [`phase_i_pairs.jsonl`](./phase_i_pairs.jsonl)，一手事实真源仍是 workbook 的 `Generation PlantUML` 列。
