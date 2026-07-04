# experiment_design/ — 实验设计约束入口

`experiment_design/` 维护第一篇 STM repair 论文的实验设计上游约束：评价逻辑链、问题范围、质量模型、eligibility 口径、协议入口和指标入口。本目录当前仍处于主实验前设计层，尚未冻结正式主实验协议、最终样本、最终指标阈值或真实 LLM 修正结果。

当前 R5.7.1 主入口是 [evaluation_logic.md](./evaluation_logic.md)：它冻结论文主张链、分母纪律、claim 类型、A 层准入、归因边界、客观指标位置、失败报告纪律和 R5.7.2--R5.7.5 下游接口。R5.7.2 在 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) 中进一步冻结 Better STM gate 链、三层输出模型和修复目标分类合同。R5.7.3 在 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) 中冻结客观代理指标框架 v0，明确指标只能作为 gate evidence / trigger / report-only，不替代 G5 semantic adjudication。R5.7.4 在 [repair_target_adjudication/README.md](./repair_target_adjudication/README.md) 中新增四例静态裁决入口，用真实 `llms-emp` 样例 dry-run taxonomy 与 metric permission。R5.7.5 在 [better_adjudication_dry_run/README.md](./better_adjudication_dry_run/README.md)、[protocols/better_adjudication_prompt_v0.md](./protocols/better_adjudication_prompt_v0.md) 与 [protocols/better_adjudication_output_schema_v0.json](./protocols/better_adjudication_output_schema_v0.json) 中冻结 constructed `STM_k` 覆盖性 dry-run 入口、裁决 prompt 和 fail-closed 输出 schema。以上内容都不是 repair loop 结果；R5.7.5 虽生成 constructed `STM_k` candidates，但不报告真实 `STM_k` 或方法效果。

## 1. 子路径

| 子路径 | 职责 | 当前状态 |
|---|---|---|
| [evaluation_logic.md](./evaluation_logic.md) | 维护 R5.7.1 评价逻辑链与主张边界：claim 类型、分母口径、A 层、归因边界、指标位置、失败报告纪律和后续 PR 接口。 | 已冻结 R5.7.1 合同；不生成 `STM_k`，不调用 LLM，不报告 repair effectiveness。 |
| [scope/](./scope/) | 维护实验范围、RQ 草案和 story / experiment scope 边界。 | 已有 R5.5 handoff 草案：[scope/2026-06-29-17-33-35-r5-5-scope-handoff.md](./scope/2026-06-29-17-33-35-r5-5-scope-handoff.md)；R5.6 story-level scope 真源：[../story/model_scope.md](../story/model_scope.md)；R5.6 -> R5.7 硬约束：[scope/r5_6_to_r5_7_handoff_constraints.md](./scope/r5_6_to_r5_7_handoff_constraints.md)；尚未冻结最终主实验协议。 |
| [quality_model/](./quality_model/) | 维护 Better STM gate 与 repair target taxonomy。 | R5.7.2 已冻结 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md)：parse ok / executable / lowering 本身不等于 Better STM，representation symptom 不能直接升级为 confirmed defect。 |
| [repair_target_adjudication/](./repair_target_adjudication/) | 维护 R5.7.4 静态裁决 dry-run：四个 `llms-emp` 样例的 taxonomy 裁决、metric permission 映射和 R6/R7 handoff。 | 已新增 [repair_target_adjudication/README.md](./repair_target_adjudication/README.md) 与四个秒级样例文件；只产生 static finding，不产生 `STM_k`、`valid_run` 或 Better STM 成功率。 |
| [better_adjudication_dry_run/](./better_adjudication_dry_run/) | 维护 R5.7.5 constructed `STM_k` 覆盖性 dry-run：20 个人工 / 确定性候选、expected verdict、gate path 和 anti-gaming 覆盖。 | 已新增 [better_adjudication_dry_run/README.md](./better_adjudication_dry_run/README.md) 与 20 case 文档；只验证 protocol coverage，不支持 repair effectiveness。 |
| [eligibility/](./eligibility/) | 维护 run / seed / conversion / provider failure 的纳入排除规则入口。 | 已接收 R5.7.1 A 层与 R5.7.2 `scope_routing_status` / `run_validity_status` / `better_adjudication_outcome` 三层输出纪律；仍未冻结 R7 正式 eligibility 协议。 |
| [protocols/](./protocols/) | 预留主实验、对照、人工裁决、修正循环协议入口。 | 已接收 R5.7.2 semantic adjudication evidence bundle、LLM-as-Judge provisional 与人工冲突裁决接口；仍未冻结 R7 正式协议。 |
| [metrics/](./metrics/) | 维护客观代理指标、统计表字段候选、报告口径和降级写法。 | R5.7.3 已冻结 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)：指标族、entry schema、G0--G6 gate × metric matrix、分母、偏序、scope、anti-gaming 与 baseline 迁移；仍不冻结最终阈值或正式结果。 |

## 2. 三件套

1. 本文件：说明目录定位、子路径和当前边界。
2. [SUMMARY.md](./SUMMARY.md)：汇总当前 RQ 草案、评价门顺序和未冻结项。
3. [GUIDE.md](./GUIDE.md)：约束后续如何补 scope、eligibility、protocol 和 metrics，防止结果倒推设计。
4. [evaluation_logic.md](./evaluation_logic.md)：R5.7.1 的评价逻辑链事实源，约束后续 R5.7.2--R5.7.5 与 R6/R7/R8 的 claim boundary。
5. [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md)：R5.7.2 的 Better STM 判定合同与修复目标分类合同。
6. [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md)：R5.7.3 的客观代理指标框架，约束指标如何作为 supporting evidence、trigger、report-only 或 forbidden。
7. [repair_target_adjudication/README.md](./repair_target_adjudication/README.md)：R5.7.4 的静态裁决 dry-run 入口，约束真实样例如何消费 taxonomy 与 metric permission。
8. [better_adjudication_dry_run/README.md](./better_adjudication_dry_run/README.md)、[protocols/better_adjudication_prompt_v0.md](./protocols/better_adjudication_prompt_v0.md)、[protocols/better_adjudication_output_schema_v0.json](./protocols/better_adjudication_output_schema_v0.json) 与 [../reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md](../reports/2026-07-05-02-10-39-r5-7-5-constructed-stmk-coverage-dry-run.md)：R5.7.5 constructed `STM_k` 覆盖性 dry-run、裁决 prompt/schema 和人类报告入口。

## 3. 当前边界

- 不冻结最终指标阈值。
- 不定义完整评分表。
- 不选择最终实验样本。
- 不跑真实 LLM 或修正循环。
- 不把当前草案写成主实验结论。
- 不让后续真实修正结果反向修改 Better STM 核心判定逻辑；若 dry-run 或真实 run 发现规则缺陷，必须以 findings ledger 驱动修订。
- 不突破 [../story/model_scope.md](../story/model_scope.md) 已冻结的 main / caveat / supplementary-stress / excluded 边界；R5.7 taxonomy 只能在该边界内细化。
- 不把 [evaluation_logic.md](./evaluation_logic.md) 中的 readiness、A-pass、parse ok、inspect ok、客观指标改善或转换恢复写成 repair effectiveness。
- 不把 [metrics/objective_metric_framework.md](./metrics/objective_metric_framework.md) 中的 metric improvement、slot-level F1、scenario pass、target closure 或 cost/stability 单独写成 Better STM；它们只能按 R5.7.3 权限进入 G0--G6 evidence bundle。

## 4. story 与 experiment_design/scope 边界

[../story/](../story/) 回答“论文讲什么、主张怎么写、哪些话不能说”；`experiment_design/scope/` 回答“哪些实验对象、RQ、样本层和分析边界进入实验设计”。

换言之：story 可以给出叙事与 claim gate，但不能冻结实验 eligibility、protocol 或 metric；experiment design 可以冻结实验范围与判定规则，但不能替代论文 story 写作或把未跑结果写成贡献。[evaluation_logic.md](./evaluation_logic.md) 位于二者之间：它把 story claim gate 转成实验可执行的证据链纪律；R5.7.2 的 [quality_model/better_stm_definition.md](./quality_model/better_stm_definition.md) 与 [quality_model/repair_target_taxonomy.md](./quality_model/repair_target_taxonomy.md) 在此基础上细化 Better STM 细则与 repair target taxonomy；R5.7.3/R5.7.4/R5.7.5 仍分别负责指标框架、静态 dry-run 和 constructed `STM_k` protocol coverage；R5.7.4 的静态 finding 与 R5.7.5 的 constructed expected verdict 都只能作为协议验证和后续 handoff，不得写成修复效果。
