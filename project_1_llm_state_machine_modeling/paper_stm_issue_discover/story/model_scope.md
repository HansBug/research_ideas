# 建模对象与表达力边界

Paper1 研究的状态机对象为 `M = (S, E, V, Tr, A)`：状态、事件、变量、迁移和动作。它覆盖离散 FSM、层次状态机和带变量/guard/action 的 EFSM 子集；PlantUML 是作者制品的表达形式，FCSTM 是方法执行所用的闭合模型，不应混为同一个事实来源。

当前 19 谓词与 FCSTM backend 的可执行片段主要覆盖 FSM/HSM/EFSM。时钟、不变式、正交 region/并发、hybrid 与无界时序可能无法形成 W2 级可执行见证，但这不是缺陷发现范围门：相关主张仍必须正常裁为 D2/D1/D0，能精确定位但不可执行时保留为 W1。[nl_scope_rule.md](../discover_matrix/docs/protocol/nl_scope_rule.md) 记录的是冻结历史实验的 pair-universe 筛选，不定义什么算缺陷。

可执行谓词在 FCSTM/native facts 上求值，不能替代作者 PlantUML 的问题定位。任一编译或投影产生的表示差异必须通过 source trace 回到作者源后再归因，不能把编译制品的结构直接记为作者模型缺陷。当前的谓词、W 条件和 soundness fragment 以 [method/](../method/README.md) 与 [最终归档](../final_results/v60_current_vs_x1v2_baseline/README.md) 为准。

本页不从历史实验转抄数值，也不将片段范围外推为 arbitrary UML/SysML、时间自动机或混成自动机。旧范围讨论和历史试验材料仅由 [实验历史索引](../archive/experiment_history/README.md) 追溯。
