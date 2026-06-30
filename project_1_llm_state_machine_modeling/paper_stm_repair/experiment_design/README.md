# experiment_design/ — 实验设计约束入口

`experiment_design/` 维护第一篇 STM repair 论文的实验设计上游约束：问题范围、质量模型、eligibility 口径、协议入口和指标入口。本目录当前仍处于主实验前设计层，尚未冻结正式主实验协议、最终样本、最终指标阈值或真实 LLM 修正结果。

## 1. 子路径

| 子路径 | 职责 | 当前状态 |
|---|---|---|
| [scope/](./scope/) | 维护实验范围、RQ 草案和 story / experiment scope 边界。 | 已有 R5.5 handoff 草案：[scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./scope/2026-06-29-17-33-35-r5-5-scope-handoff.md)；R5.6 story-level scope 真源：[../story/model_scope.md](../story/model_scope.md)；R5.6 -> R5.7 硬约束：[scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md)；尚未冻结最终主实验协议。 |
| [quality_model/](./quality_model/) | 维护 Better STM 等质量判定模型。 | 已迁入 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md)，并明确 parse ok / executable / lowering 本身不等于 Better STM。 |
| [eligibility/](./eligibility/) | 预留 run / seed / conversion / provider failure 的纳入排除规则入口。 | 只有职责 README，未冻结 eligibility 协议。 |
| [protocols/](./protocols/) | 预留主实验、对照、人工裁决、修正循环协议入口。 | 只有职责 README，未冻结正式协议。 |
| [metrics/](./metrics/) | 预留指标、统计表字段和报告口径入口。 | 只有职责 README，未冻结最终指标。 |

## 2. 三件套

1. 本文件：说明目录定位、子路径和当前边界。
2. [SUMMARY.md](./SUMMARY.md)：汇总当前 RQ 草案、评价门顺序和未冻结项。
3. [GUIDE.md](./GUIDE.md)：约束后续如何补 scope、eligibility、protocol 和 metrics，防止结果倒推设计。

## 3. 当前边界

- 不冻结最终指标阈值。
- 不定义完整评分表。
- 不选择最终实验样本。
- 不跑真实 LLM 或修正循环。
- 不把当前草案写成主实验结论。
- 不让后续真实修正结果反向修改 Better STM 核心判定逻辑。
- 不突破 [../story/model_scope.md](../story/model_scope.md) 已冻结的 main / caveat / supplementary-stress / excluded 边界；R5.7 taxonomy 只能在该边界内细化。

## 4. story 与 experiment_design/scope 边界

[../story/](../story/) 回答“论文讲什么、主张怎么写、哪些话不能说”；`experiment_design/scope/` 回答“哪些实验对象、RQ、样本层和分析边界进入实验设计”。

换言之：story 可以给出叙事与 claim gate，但不能冻结实验 eligibility、protocol 或 metric；experiment design 可以冻结实验范围与判定规则，但不能替代论文 story 写作或把未跑结果写成贡献。
