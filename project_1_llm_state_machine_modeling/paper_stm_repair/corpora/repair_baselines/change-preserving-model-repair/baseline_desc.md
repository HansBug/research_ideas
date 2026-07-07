# Change-Preserving Model Repair — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `change-preserving-model-repair` |
| 标题 | Change-Preserving Model Repair |
| 年份 / venue | 2017 / FASE |
| 当前角色 | 模型一致性 / change-preserving repair 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | UML class/sequence/state machine diagrams 可作为评估对象之一，但方法是 generic model repair/graph transformation |
| 修正输入 | 历史版本 V1 + 潜在不一致版本 V2 + edit operation history / consistency-preserving operations |
| 修正输出 | concrete repair steps / complement operations to restore consistency while preserving changes |
| 修正 / 补全 / refinement 方法 | graph transformation；识别 edit operations；把 inconsistent EO 补成 consistency-preserving operation 的 complement repair |
| feedback 来源 | metamodel/consistency violations + edit history |
| 自动化程度 | 半自动/工具辅助；用户可查看、测试、回滚 repair |
| LLM / agent 角色 | 无 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不满足本文 baseline：无 NL，目标不是 STM 语义 repair；但可提供 model repair taxonomy 与 history-guided repair 参考。

## 4. 证据位置

paper_content.txt:10-23, 40-61, 454-492, 541-551

## 5. 主要风险与使用边界

generic UML/model consistency，非需求语义状态机；依赖 CPO/EO rule specification。
