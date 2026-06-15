# Fixing Inconsistencies in UML Design Models — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `fixing-inconsistencies-uml-design-models` |
| 标题 | Fixing Inconsistencies in UML Design Models |
| 年份 / venue | 2007 / ICSE |
| 当前角色 | UML consistency fixing 经典近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | UML class/sequence/statechart mixed design model |
| 修正输入 | UML design model + consistency/well-formedness rule violations + profiling data |
| 修正输出 | choices for fixing inconsistencies and predicted side effects/dependencies |
| 修正 / 补全 / refinement 方法 | model profiling observes consistency rule evaluation behavior，定位 repair choices 和 side effects |
| feedback 来源 | consistency/well-formedness rule violation |
| 自动化程度 | 工具辅助，非全自动 repair；作者明确说工具不能自动决定是否 resolve |
| LLM / agent 角色 | 无 |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

不满足本文 baseline：无 NL；经典 model inconsistency repair related work。

## 4. 证据位置

paper_content.txt:11-25, 57-80, 172-215, 977-986

## 5. 主要风险与使用边界

老 UML 工具链，repair 是 choices/assistant，不是无人化 STM repair。
