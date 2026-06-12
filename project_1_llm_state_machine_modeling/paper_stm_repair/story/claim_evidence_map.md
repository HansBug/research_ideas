# claim-evidence map：主张与证据门

## 1. 使用原则

每条论文主张必须有可追溯证据。R0 只冻结 claim gate，不证明这些 claim 已成立。若后续 PR 无法提供证据，R7 写作必须降级或删除对应 claim。

## 2. 主张台账

| Claim ID | 可写主张草案 | 当前状态 | 必需证据 | 后续 PR | 安全降级写法 |
|---|---|---|---|---|---|
| C1 | 本文定义并研究 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | R0 可支撑任务定义。 | story、task boundary、related work positioning。 | R0 / R7 | “We frame / study” 而非 “we solve”。 |
| C2 | 结构化 diagnostics 与 scenario feedback 可用于驱动无人化修正循环。 | 仅有规划，未实证。 | 诊断/场景规范、R5 loop、R6 四例预演与主实验。 | R4 / R5 / R6 | “can be integrated into a repair loop” 而非 “guarantee improvement”。 |
| C3 | `STM_k` 可在预注册条件下相对 `STM_0` 更优。 | 尚未验证。 | 五条件台账、同一 `STM_0` 对比、人工裁决、回归检查。 | R4 / R6 | 若效果有限，写“部分样例显示改善，失败模式如下”。 |
| C4 | baseline / prior artifacts 可重排为 seed source 和 converter pressure。 | R0 只定方向。 | 论文、代码、artifact、格式、可转换性台账。 | R1 / R2 / R3 | 若资源不足，写“可获取 artifact 子集”。 |
| C5 | 转换规范化收益与 repair-loop 收益可以分开归因。 | R0 定义要求。 | 转换前 / 后 / 修正后诊断计数与信息损失台账。 | R3 / R6 | 若台账不完整，只作 case analysis。 |
| C6 | 修正协议能报告拒绝修复、回滚、振荡和不收敛。 | R0 定义要求。 | R5 repair ledger、R6 结果统计。 | R5 / R6 | 若实现不完整，改写为“we log and analyze observed failure modes”。 |

## 3. 禁止 claim

| 禁止 claim | 为什么禁止 |
|---|---|
| 本文是首个 `NL -> STM` 生成方法。 | 与导师定调冲突，也缺乏 novelty gate。 |
| 本文提出了新的状态机 DSL。 | 会把贡献带偏；DSL 只是内部载体。 |
| 本文完成形式化验证并保证正确性。 | 当前只计划轻量诊断 / 场景反馈，没有 soundness 证明。 |
| 修正循环总能提升状态机质量。 | 必须报告失败、回滚、振荡和不收敛。 |
| 转换器带来的改善属于 repair-loop 能力。 | 必须用三阶段台账分开归因。 |

## 4. R7 写作前检查

1. 每个 abstract / introduction claim 必须映射到上表某个 claim ID。
2. 每个 claim ID 必须在 R1--R6 中有明确证据文件或降级理由。
3. 没有实验证据的 claim 只能写成 task framing、method design 或 pilot observation。
4. 工程审计制品可以支撑 reproducibility，但不能替代方法贡献或实验结论。
