# Software Model Evolution with Large Language Models: Experiments on Simulated, Public, and Industrial Datasets — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `software-model-evolution-llm` |
| 标题 | Software Model Evolution with Large Language Models: Experiments on Simulated, Public, and Industrial Datasets |
| 年份 / venue | 2025 / ICSE |
| 当前角色 | LLM software model completion 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 模型中的 textual components / natural-language data；不是 requirements NL |
| 模型 / STM 输入 | general software models，Ecore/UML 2.5.1 / industrial SysML；不限定 STM |
| 修正输入 | model history / partial model context + edit operation prompt + retrieval examples |
| 修正输出 | single-location model completion suggestion / edit operation |
| 修正 / 补全 / refinement 方法 | RAMC：retrieval-augmented LLM prompt over model difference graphs；另比较 fine-tuning |
| feedback 来源 | 无 verifier feedback；主要是 completion correctness evaluation |
| 自动化程度 | 自动 completion/recommendation；非 repair loop |
| LLM / agent 角色 | GPT-family / LLM RAG/fine-tuning |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不满足本文 baseline：不是 `<NL, STM_0>` 输入，且模型 completion 泛化到 Ecore/SysML；可作 LLM model completion near-neighbor。

## 4. 证据位置

paper_content.txt:15-31, 104-150, 371-529, 599-660, 1146-1152

## 5. 主要风险与使用边界

NL 不是需求输入；任务是 model evolution completion，不是需求语义修正；工业数据不可公开。
