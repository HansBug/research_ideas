# Automated BPMN Model Generation from Textual Process Descriptions: A Multi-Stage LLM-Driven Approach — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `automated-bpmn-diagnostic-repair` |
| 标题 | Automated BPMN Model Generation from Textual Process Descriptions: A Multi-Stage LLM-Driven Approach |
| 年份 / venue | 2026 / arXiv |
| 当前角色 | BPMN diagnostics-to-repair 方法近邻 |
| 阅读来源 | 本地 `paper_content.txt` + 独立全文阅读任务结果 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | textual process descriptions |
| 模型 / STM 输出 | BPMN 2.0 XML；行为/process 模型但非 STM |
| 修正 / 补全 / refinement 方法 | 六阶段 LLM pipeline；SpiffWorkflow validation diagnostics、XML / namespace / connectivity checks 后 LLM localized repair |
| feedback 来源 | SpiffWorkflow diagnostics、XML/parser structural checks、execution-oriented compliance constraints |
| 自动化程度 | 较高，但完整代码/数据未公开 |
| LLM / agent 角色 | ChatGPT-4o、Gemini 2.5 Flash/Pro 等 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

可借鉴 diagnostics-to-repair loop 和结构评估；非 STM baseline。

## 4. 证据位置

`paper_content.txt` 摘要、SpiffWorkflow repair、pipeline、validation failure correction loop、750->387 corpus；独立全文阅读任务核验。

## 5. 主要风险与使用边界

BPMN 与 STM 语义差异大；数据描述由 BPMN 反向生成；完整数据/实现未公开；gateway logic 未充分评估。
