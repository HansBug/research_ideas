# Computing repair trees for resolving inconsistencies in design models — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `computing-repair-trees-design-models` |
| 标题 | Computing repair trees for resolving inconsistencies in design models |
| 年份 / venue | 2012 / ASE |
| 当前角色 | 模型一致性 repair tree 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | UML design models；示例多为 class/sequence，声称适用于 arbitrary modeling/constraint languages |
| 修正输入 | inconsistent design model + design/OCL rule evaluation trace/cause |
| 修正输出 | repair tree：alternatives/sequences of model changes |
| 修正 / 补全 / refinement 方法 | 分析 design rule runtime evaluation，消除 false/non-minimal repairs，以 design-rule structure 组织 repair actions |
| feedback 来源 | constraint/design rule violation and evaluation trace |
| 自动化程度 | 自动化工具 Model/Analyzer；designer 选择 repair |
| LLM / agent 角色 | 无 |

## 3. 与本文 `<NL, STM_0> -> Better STM` 的关系

不满足本文 baseline：无 NL、非 STM-specific；可作 model inconsistency repair taxonomy。

## 4. 证据位置

paper_content.txt:11-26, 82-92, 832-900, 921-1019；工具入口 paper_content.txt:894-895

## 5. 主要风险与使用边界

不是状态机语义修复；repair tree 仍需人选择；工具老旧。
