# paper story：从生成状态机转向反馈驱动修正

## 1. 一句话 thesis

给定控制系统自然语言需求 `NL` 与初始状态机 `STM_0`，本文研究是否可以通过无人化、结构化反馈驱动的检查 / 诊断 / 仿真 / 修正循环，得到相对于 `STM_0` 更可检查、更可执行、更语义一致的候选状态机 `STM_k`。

## 2. 背景判断

直接从自然语言生成状态机已经是 crowded 战场。若继续主打 `NL -> STM`，论文会被拉回 prompt、模型选择、direct baseline 公平性和生成质量硬对比，而不容易突出本项目真正积累起来的 diagnostics、simulation、repair feedback 和 run audit 能力。

真实使用场景中，已有或可构造的初始状态机往往不是完全不可用，而是存在结构、语义、guard / action、行为场景或可执行性缺陷。一个更稳的研究问题是：**给定 `NL` 与 `STM_0`，系统能否自动发现缺陷、提出修正、检查回归、接受或回滚候选，从而得到更好的 `STM_k`。**

## 3. 核心 gap

| 既有工作常见能力 | 本文关注的缺口 |
|---|---|
| 生成 state-machine-like / UML / SysML / behavior artifacts。 | 生成后 artifact 是否可机检、可执行、可诊断、可修正通常没有形成闭环。 |
| 使用 prompt 或 agent 分阶段生成模型。 | 结构化 feedback 是否能稳定减少缺陷、避免回归、记录失败模式仍需实证。 |
| 使用自然语言或示例辅助建模。 | 初始模型与需求之间的 semantic drift、guard / action 错误、场景行为缺陷需要可审计修复协议。 |
| 一次性人工审查或工具检查。 | 缺少 `diagnose -> repair -> regression -> accept / rollback` 的无人化循环与归因台账。 |

## 4. 方法洞察

本文的关键不是提出一个新 DSL，也不是换更强模型重新生成状态机，而是把初始状态机规范化为可机检、可执行的状态机制品，使系统可以自动产生结构化反馈，并将反馈纳入修正循环：

```text
<NL, STM_i> -> diagnostics / scenario feedback -> candidate repair -> regression checks -> accept / reject / rollback -> STM_{i+1}
```

该循环必须记录 rejected repair、oscillation、non-convergence、semantic drift 和 converter attribution，不能只报告成功样例。

## 5. 贡献草案（R0 版本）

| 贡献草案 | 当前证据状态 | 后续证据门 |
|---|---|---|
| 定义 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | R0 story / task boundary 冻结。 | R7 写作时必须引用 R1--R6 证据，不可扩大为 `NL -> STM`。 |
| 提出无人化 repair run 协议：诊断、场景反馈、候选修正、回归检查、接受 / 拒绝 / 回滚。 | R0 仅定义边界。 | R4 冻结评价门；R5 实现循环；R6 评价协议。 |
| 操作化 `Better STM`，区分转换规范化收益与修正循环收益。 | R0 定义最小必要条件。 | R3 归因台账；R4/R6 指标与统计表。 |
| 将 prior baseline artifact 重排为 seed source、converter pressure、error taxonomy 和有限对照。 | R0 仅定方向。 | R1 资产盘点；R2 样本冻结；R6 对照矩阵。 |

## 6. Claims to avoid

1. 不写“首个 / 最强 `NL -> STM` 方法”。
2. 不写“提出新 DSL / fcstm 是核心贡献”。
3. 不写“完整形式化验证 / model checking 保证正确”。
4. 不写“自动修正一定提升质量”或“outperform all baselines”。
5. 不写“baseline 已经无须比较”。
6. 不把 run record、日志或复现工程本身写成论文方法贡献。

## 7. 当前未闭合风险

| 风险 | 需要后续 PR 闭合 |
|---|---|
| 哪些 prior artifact 可真实转为 `STM_0` 尚未盘点。 | PR-R1 / PR-R2 |
| 多格式转换器的最小范围尚未冻结。 | PR-R3 |
| 诊断、场景、评价量表尚未冻结。 | PR-R4 |
| 修正循环是否稳定有效尚未实证。 | PR-R5 / PR-R6 |
| 论文正文中如何安全定位 related work 尚未完成。 | PR-R7 |
