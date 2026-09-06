# Towards using Few-Shot Prompt Learning for Automating Model Completion — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `few-shot-model-completion` |
| 标题 | Towards using Few-Shot Prompt Learning for Automating Model Completion |
| 年份 / venue | 2023 / ICSE-NIER |
| 当前角色 | 弱近邻 model completion |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无 NL repair 输入；partial UML class/activity models |
| 模型 / STM 输出 | UML class diagram / activity diagram；activity 是行为近邻但非 STM |
| 修正 / 补全 / refinement 方法 | partial model -> textual prompt -> GPT-3 sequence completion -> parse back suggestions，按频率排序 |
| feedback 来源 | 无 formal checker；评估用 ground truth 和人工语义等价判断 |
| 自动化程度 | 建议生成自动；接受/评估依赖人工 |
| LLM / agent 角色 | GPT-3 text-davinci-002 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

可作为 partial model completion 方法参照；不能作为 repair baseline 主证据。

## 4. 证据位置

`paper_content.txt` 任务、partial model prompt、class/activity examples、GitHub replication；旁路核验材料复核。

## 5. 主要风险与使用边界

activity diagram 不能等同 STM；短文实验；无修复闭环/形式化 feedback。
