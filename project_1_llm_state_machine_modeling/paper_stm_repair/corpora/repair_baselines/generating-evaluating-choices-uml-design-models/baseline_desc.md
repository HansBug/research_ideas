# Generating and Evaluating Choices for Fixing Inconsistencies in UML Design Models — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `generating-evaluating-choices-uml-design-models` |
| 标题 | Generating and Evaluating Choices for Fixing Inconsistencies in UML Design Models |
| 年份 / venue | 2008 / ASE |
| 当前角色 | UML consistency choices 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | UML class/sequence/statechart mixed design model |
| 修正输入 | inconsistent UML design model + consistency rules + model profiler accessed elements |
| 修正输出 | valid choices/concrete changes and impact on consistency rules |
| 修正 / 补全 / refinement 方法 | generate-and-prune：按 model element type/location 生成候选值，再用 incremental consistency checking 剪枝 |
| feedback 来源 | consistency rule violations + invalid-choice explanations |
| 自动化程度 | 工具辅助；生成 choices，designer 决策 |
| LLM / agent 角色 | 无 |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

不满足本文 baseline：无 NL 与 NL->STM_0；可参考 consistency feedback 与 choice generation。

## 4. 证据位置

paper_content.txt:14-24, 47-72, 82-94, 239-241, 463 等

## 5. 主要风险与使用边界

UML 多视图 consistency，不是状态机需求语义 repair；不自动闭环。
