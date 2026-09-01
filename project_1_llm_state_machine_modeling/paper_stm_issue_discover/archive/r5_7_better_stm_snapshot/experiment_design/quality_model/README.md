# quality_model/ — 质量模型入口

本目录维护 STM repair 结果的质量判定模型。R5.7.2 之后，本目录不只保存一句 Better STM 定义，而是保存 **Better STM gate 链 + repair target taxonomy** 两个长期合同。

## 1. 文件清单与阅读顺序

| 顺序 | 文件 | 读它是为了什么 | 不能把它当成什么 |
|---:|---|---|---|
| 1 | [better_stm_definition.md](./better_stm_definition.md) | 读取 R5.7.2 Better STM 判定合同：对象角色、G0–G6 gate、三层输出模型、硬拒绝、T0.5 caveat、指标权限和裁决接口。 | 不是 repair loop 结果；不报告 `STM_k`、成功率或方法效果。 |
| 2 | [repair_target_taxonomy.md](./repair_target_taxonomy.md) | 读取 R5.7.2 修复目标分类合同：11 类 target、11 字段、五级 `repair_action_allowed`、candidate-only 纪律和代表性例子。 | 不是已确认缺陷统计；不证明某个 pair 已经需要修。 |

## 2. 当前冻结结论

1. Better STM 必须通过 G0–G6 gate：scope、A gate、attribution、no-regression、improvement、semantic、reporting。
2. raw `STM_0` 是 source evidence；Better 比较对象是 canonical `STM_0` vs `STM_k`。
3. conversion / normalization / `.fcstm` parse / inspect 收益不得计入 repair-loop gain。
4. 客观指标只作 supporting evidence；parse ok、diagnostics fewer、scenario pass 或 F1 更高都不能单独判 Better。
5. `condition_like_label_lowered_as_event` 等 representation symptom 只能先是 candidate-only，必须回到 `NL + raw STM_0 + canonical STM_0 + evidence bundle` 后才能确认是否为 repair target。
6. T0.5 tick / counter 可作 caveat 层讨论；T1 / timed automata / hybrid / arbitrary UML / protocol FSM 不进入 T0 headline。

## 3. 与其他 experiment_design 子路径的关系

| 子路径 | 关系 |
|---|---|
| [../evaluation_logic.md](../evaluation_logic.md) | R5.7.1 冻结 claim boundary、分母、A 层与归因边界；本目录细化 Better STM 与修复目标。 |
| [../eligibility/](../eligibility/) | 继承 G0/G1/G2 的 scope、A gate 和 provenance-invalid 去向。 |
| [../protocols/](../protocols/) | 继承 G5 semantic adjudication、evidence bundle、LLM-as-Judge provisional 与人工冲突裁决。 |
| [../metrics/](../metrics/) | R5.7.3 将在本目录的指标权限上限内定义 objective metrics。 |
| [../scope/](../scope/) | R5.6/R5.7 的 T0/T0.5/T1 与模型族边界是本目录所有 target 的上游约束。 |

## 4. 维护纪律

1. 本目录规则不得因后续 R6/R7/R8 结果好坏反向漂移。
2. 若 dry-run 或真实 run 发现规则缺陷，必须在 findings ledger 中记录触发样例、旧规则失败方式和新规则修订理由，再更新本目录。
3. 新增 target 必须补齐 [repair_target_taxonomy.md](./repair_target_taxonomy.md) 的 11 字段，并说明 `repair_action_allowed`。
4. 修改 Better STM gate 必须同步检查 [../evaluation_logic.md](../evaluation_logic.md)、[../eligibility/README.md](../eligibility/README.md)、[../protocols/README.md](../protocols/README.md)、[../metrics/README.md](../../../r7_issue_lifecycle_scaffold/experiment_design/metrics/README.md) 与 [../../story/claim_evidence_map.md](../../../../story/claim_evidence_map.md)。
