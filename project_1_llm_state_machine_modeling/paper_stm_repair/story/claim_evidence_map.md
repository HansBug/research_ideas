# claim-evidence map：主张与证据门

## 1. 使用原则

每条论文主张必须有可追溯证据。R0/R5.5 只冻结 claim gate、seed readiness 和 story handoff，不证明 repair-loop claim 已成立。若后续 PR 无法提供证据，R7 写作必须降级或删除对应 claim。

## 2. 主张台账

| Claim ID | 可写主张草案 | 当前状态 | 必需证据 | 后续 PR | 安全降级写法 |
|---|---|---|---|---|---|
| C1 | 本文定义并研究 `<NL, STM_0> -> STM_k` 的反馈驱动状态机修正任务。 | R0/R5.5 可支撑任务定义和主 seed 池画像。 | [paper_story.md](./paper_story.md)、[task_boundary.md](./task_boundary.md)、[../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md](../reports/2026-06-29-00-03-56-llms-emp-main-seed-profile.md)。 | R0 / R5.5 / R7 | “We frame / study” 而非 “we solve”。 |
| C2 | 结构化 diagnostics 与 scenario feedback 可用于驱动无人化修正循环。 | 仅有规划与评价门，未实证 repair 效果。 | pipeline diagnostics / scenario gate、R6/R8 repair ledger、回归检查。 | R4 / R6 / R8 | “can be integrated into a repair loop” 而非 “guarantee improvement”。 |
| C3 | `STM_k` 可在预注册条件下相对 `STM_0` 更优。 | 尚未验证。 | 五条件台账、同一 `STM_0` 对比、人工裁决、回归检查。 | R4 / R6 / R8 | 在预注册 eligible runs 中报告逐条件结果；未满足五条件者不得计为 Better STM，只能作局部改善或失败模式。 |
| C4 | prior artifacts 可重排为 seed source、repair-baseline / near-neighbor landscape 和 converter pressure。 | R1--R5.5 已有 seed registry、repair baseline 总账、conversion profile 和 reports，但 eligibility 仍未最终冻结。 | seed 看 [../corpora/seed_library/REGISTRY.md](../corpora/seed_library/REGISTRY.md)；baseline / near-neighbor 看 [../corpora/repair_baselines/SUMMARY.md](../corpora/repair_baselines/SUMMARY.md)；human-facing handoff 看 [../reports/SUMMARY.md](../reports/SUMMARY.md)；readiness / conversion 机器证据看 [../pipeline/readiness_audit/README.md](../pipeline/readiness_audit/README.md)。 | R1 / R2 / R3 / R5.7 | 若资源不足，写“可获取 artifact 子集”，并区分 seed、baseline 和 converter pressure。 |
| C5 | 转换规范化收益与 repair-loop 收益可以分开归因。 | R0 定义要求；R5/R5.5 已暴露 conversion partial / blocked，但还没有 repair 后对照。 | 转换前 / 后 / 修正后诊断计数、conversion attribution ledger、repair ledger。 | R3 / R5 / R6 / R8 | 若台账不完整，只作 case analysis。 |
| C6 | 修正协议能报告拒绝修复、回滚、振荡和不收敛。 | 仅有 protocol requirement，尚无真实 run evidence。 | R6/R8 repair ledger、accept / reject / rollback ledger、oscillation / non-convergence ledger 与结果统计。 | R6 / R8 | 若实现不完整，改写为“we log and analyze observed failure modes”。 |

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
2. 每个 claim ID 必须在 R1--R8 中有明确证据文件或降级理由。
3. 没有实验证据的 claim 只能写成 task framing、method design 或 pilot observation。
4. 工程审计制品可以支撑 reproducibility，但不能替代方法贡献或实验结论。


## 5. 本轮恢复后的 story 文件入口

- 主线与贡献草案：[paper_story.md](./paper_story.md)
- 方法内外边界：[task_boundary.md](./task_boundary.md)
- 术语与禁用表达：[terminology_policy.md](./terminology_policy.md)
