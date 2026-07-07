# AI-Driven Consistency of SysML Diagrams — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `ai-driven-consistency-sysml` |
| 标题 | AI-Driven Consistency of SysML Diagrams |
| 年份 / venue | 2024 / MODELS |
| 当前角色 | SysML consistency repair 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 旁路核验材料 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 自然语言 system specification + UCD/BD text representation |
| 模型 / STM 输出 | SysML UCD/BD；本文实验主体不是 SMD |
| 修正 / 补全 / refinement 方法 | 定义 UCD/BD consistency rules，TTool syntax/consistency checker，LLM 检测不一致并反馈 TTool-AI 修正图 |
| feedback 来源 | 形式化一致性规则、TTool checker、GPT inconsistency judgment、用户选择 |
| 自动化程度 | 半自动；用户参与筛选和反馈 |
| LLM / agent 角色 | OpenAI GPT 用于图生成、跨图不一致检测和修正 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

强相关 consistency / repair related work；不能写成 STM direct baseline。

## 4. 证据位置

`paper_content.txt` 摘要、UCD/BD scope、rules、correction loop、69 inconsistency / 60.5 repair；旁路核验材料复核。

## 5. 主要风险与使用边界

实验不处理 SMD；无模型检查反例/仿真 trace；human-in-the-loop；容易被误写成 STM baseline。
