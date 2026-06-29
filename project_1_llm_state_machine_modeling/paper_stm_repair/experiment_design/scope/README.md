# scope/ — 实验范围职责入口

本目录用于维护实验对象、RQ 版本、样本范围、时间层级和 story / experiment scope 边界。

当前状态：已落地 R5.5 -> R5.6 scope handoff 草案 [2026-06-29-17-33-35-r5-5-scope-handoff.md](./2026-06-29-17-33-35-r5-5-scope-handoff.md)，并新增 R5.6 -> R5.7 硬约束 [r5_6_to_r5_7_handoff_constraints.md](./r5_6_to_r5_7_handoff_constraints.md)。R5.6 的 story-level scope 真源是 [../../story/model_scope.md](../../story/model_scope.md)：T0 离散 FSM/HSM/离散 UML-SysML statechart 子集作为主线，EFSM-lite 只是当前无独立样例的候选范围上限，T0.5 作为 timer-like caveat，Digital Camera / T1-ish 作为 supplementary stress，timed / hybrid / arbitrary UML / protocol FSM excluded。上述文件不是最终主实验协议，也不冻结最终样本集合、repair target taxonomy 或指标阈值。

## 当前 scope 文件

| 文件 | 状态 | 用途 |
|---|---|---|
| [2026-06-29-17-33-35-r5-5-scope-handoff.md](./2026-06-29-17-33-35-r5-5-scope-handoff.md) | R5.5 handoff 草案 | 给 R5.6 story / model scope freeze 使用；含证据链、claim-evidence map 与复验命令。 |
| [r5_6_to_r5_7_handoff_constraints.md](./r5_6_to_r5_7_handoff_constraints.md) | R5.6 -> R5.7 硬约束 | 给 R5.7 repair target taxonomy / eligibility 前置设计使用；明确不得重新打开的 scope、不得直接升级的 representation symptoms 和最低 taxonomy 字段。 |
| [../../story/model_scope.md](../../story/model_scope.md) | R5.6 story-level scope 真源 | 冻结 paper story / model scope / claim boundary；本目录引用其结论但不复制成第二事实源。 |

## 与 story/ 的边界

- [../../story/](../../story/)：论文讲什么、主张怎么写、claim gate 如何表达。
- 本目录：哪些对象进入实验设计、哪些 RQ / seed / system family / time tier 纳入或排除。

禁止把 story 的叙事判断直接写成实验 eligibility；也禁止把未跑实验的 scope 草案写成论文结论。
