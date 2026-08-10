# Repairing Timed Automata Clock Guards through Abstraction and Testing — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `repairing-timed-automata-clock-guards` |
| 标题 | Repairing Timed Automata Clock Guards through Abstraction and Testing |
| 年份 / venue | 2019 / TAP@FM |
| 当前角色 | 异构 timed-automata testing/oracle repair 近邻 |
| 阅读来源 | 本地 `paper_content.txt` 全文阅读 + 摘要/方法/实验/资源段落核验 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL |
| 模型 / STM 输入 | Timed automata / Parametric Timed Automata |
| 修正输入 | initial faulty TA + oracle over timed traces；假设 states/transitions 结构正确，仅 clock guards 错 |
| 修正输出 | repaired TA with instantiated clock-guard parameters |
| 修正 / 补全 / refinement 方法 | TA -> PTA abstraction；生成 timed traces；查询 oracle；IMITATOR 合成参数约束；Choco 求解 |
| feedback 来源 | oracle 接受/拒绝 timed traces + tests |
| 自动化程度 | 自动化流程；依赖 oracle |
| LLM / agent 角色 | 无 |

## 3. 与本文 source-level issue discovery / repair / closure 任务的关系

不满足本文 baseline：没有 NL，也不是 NL-derived STM_0；但可作 oracle/testing-guided formal repair near-neighbor。

## 4. 证据位置

paper_content.txt:11-24, 49-67, 248-283, 530-562, 636-648

## 5. 主要风险与使用边界

硬假设结构正确且只修 guard constants；目标 timed automata；oracle 非本文输入范式。
