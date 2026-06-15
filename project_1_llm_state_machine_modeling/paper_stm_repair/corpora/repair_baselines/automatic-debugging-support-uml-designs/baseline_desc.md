# Automatic Debugging Support for UML Designs — repair baseline 记录

## 1. 基本信息

| 字段 | 内容 |
|---|---|
| baseline_id | `automatic-debugging-support-uml-designs` |
| 标题 | Automatic Debugging Support for UML Designs |
| 年份 / venue | 2000 / AADEBUG / arXiv |
| 当前角色 | 经典 statechart debugging 近邻 |
| 阅读来源 | 本地 `paper_content.txt` + 独立全文阅读任务结果 |

## 2. 任务、输入与输出

| 维度 | 内容 |
|---|---|
| NL / 输入 | 无直接 NL；输入为 annotated sequence diagrams + domain theory / OCL pre/post |
| 模型 / STM 输出 | structured UML statecharts / hierarchical state machine |
| 修正 / 补全 / refinement 方法 | 从 sequence diagrams 综合 statecharts；statechart 修改后反向检查 sequence diagrams；用 state vector、unification、frame axiom 找冲突，可搜索 sequence-diagram patch |
| feedback 来源 | 逻辑冲突、failed unification、state vector 不一致、requirements/domain mismatch |
| 自动化程度 | 检测较自动；修复决策由用户完成 |
| LLM / agent 角色 | 无 |

## 3. 与本论文 `<NL, STM_0> -> Better STM` 的关系

可作为“statechart debugging + backward requirements checking”的经典前身；不是现代 LLM repair。

## 4. 证据位置

`paper_content.txt` 摘要、synthesis/backward checking、statechart 定义、conflict detection、debugging statechart、implementation；独立全文阅读任务核验。

## 5. 主要风险与使用边界

输入前提强，不是 NL；工具/数据不可复现；更像 debug/explanation 而非端到端自动修复。
