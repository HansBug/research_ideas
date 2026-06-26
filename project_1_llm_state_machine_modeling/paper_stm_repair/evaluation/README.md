# evaluation/ — R4 诊断、场景与 Better STM 评价门 v0

## 0. 定位

`evaluation/` 是 PR-R4 为第一篇论文 `<NL, STM_0> -> STM_k / Better STM` 主线建立的评价门工作区。它在真实修正循环、真实 LLM 调用和正式主实验之前，先冻结一套可审计的 **诊断 taxonomy、场景 / 回归 schema、Better STM 五条件 checklist、eligibility policy 与人工裁决 rubric v0**。

本目录只支撑 R4 v0 dry-run 与后续 R5/R6/R7 的接口，不产生论文主结果，不证明 repair loop 有效，也不把四例 smoke panel 写成最终实验集合。

## 1. 与上游目录的关系

| 上游 / 下游 | 关系 |
|---|---|
| [../selected_seed_examples/](../selected_seed_examples/) | R4 dry-run 固定复用的四个静态 `<NL, STM_0>` smoke 样例；不是最终实验集合。 |
| [../conversion/](../conversion/) | R3 converter v0 与 R3.1 PlantUML recovery eligibility audit；R4 只能引用其 status / loss / canonical 裁决，不得改写 R3 转换语义。 |
| [../experiment_design/better_stm_definition.md](../experiment_design/better_stm_definition.md) | Better STM 五条件的上游定义；本目录将其落成 checklist 与 schema。 |
| [../experiment_design/evaluation_gate.md](../experiment_design/evaluation_gate.md) | 上游顺序约束：评价门必须先于真实修正预演冻结。 |
| R5/R6/R7/R8 | R5/R6 复用本目录 schema 做 deterministic dry-run / loop skeleton；R7 才冻结正式实验 protocol；R8 才执行主实验。 |

## 2. 阅读顺序

1. [GUIDE.md](./GUIDE.md)：先确认 R4 工作纪律、证据等级和禁止 claim。
2. [diagnostic_taxonomy.md](./diagnostic_taxonomy.md)：查看诊断 code、severity、source stage 和 R3 映射规则。
3. [scenario_schema.md](./scenario_schema.md)：查看场景 / 回归 suite 的最小结构。
4. [better_stm_checklist.md](./better_stm_checklist.md)：查看五条件 checklist 与聚合判定。
5. [eligibility_policy.md](./eligibility_policy.md)：查看 R3 `converted / partial / blocked` 如何进入 R4/R5。
6. [human_rubric.md](./human_rubric.md)：查看人工裁决 rubric v0。
7. [metrics_table_plan.md](./metrics_table_plan.md)：查看 R7/R8 结果表骨架。
8. [dry_run_examples/](./dry_run_examples/)：查看四例 dry-run fixture 与 R4 decision。
9. [schemas/](./schemas/) 与 [tests/](./tests/)：查看 machine-readable contract 与回归测试。

## 3. 路径结构

```text
evaluation/
├── README.md
├── GUIDE.md
├── diagnostic_taxonomy.md
├── better_stm_checklist.md
├── scenario_schema.md
├── eligibility_policy.md
├── human_rubric.md
├── metrics_table_plan.md
├── dry_run_examples/
│   ├── README.md
│   ├── r4_dry_run_summary.md
│   └── <example_id>/
│       ├── README.md
│       ├── diagnostic_draft.json
│       ├── scenario_draft.json
│       ├── eligibility_decision.json
│       └── better_stm_checklist.json
├── schemas/
│   ├── diagnostic.schema.json
│   ├── scenario.schema.json
│   ├── better_stm_checklist.schema.json
│   ├── eligibility_decision.schema.json
│   └── human_rubric.schema.json
└── tests/
    ├── test_r4_schema_contract.py
    └── test_r4_selected_examples_dry_run.py
```

## 4. R4 dry-run 总结

| 样例 | R3 裁决 | R4 decision | 用途 |
|---|---|---|---|
| [llms-emp-gpt4o-hldcs](./dry_run_examples/llms-emp-gpt4o-hldcs/README.md) | `converted` / official SCXML canonical | `complete` | 完整跑通 diagnostic + scenario + checklist 字段。 |
| [sefm-ssc7-umple](./dry_run_examples/sefm-ssc7-umple/README.md) | `partial` / official SCXML + timing loss | `focused` | 验证 partial canonical 与 timing caveat 的表达。 |
| [ttool-automatedbraking-xml](./dry_run_examples/ttool-automatedbraking-xml/README.md) | `partial` / official XML inventory | `focused` | 验证 inventory-only / unresolved connector / timed AVATAR 的降级策略。 |
| [unified-uml-synthetic-0000](./dry_run_examples/unified-uml-synthetic-0000/README.md) | `partial` / no canonical conversion | `blocked` | 验证 no-canonical 输入只能进入 blocked / toolchain-boundary analysis。 |

## 5. 禁止 claim

R4 可以声称：本文在 repair loop 前定义并 dry-run 了可审计的诊断 / 场景 / Better STM 评价门 v0。

R4 不能声称：

1. repair loop 已经有效；R6/R8 才涉及修正运行。
2. 正式实验 protocol 已冻结；R7 才冻结。
3. 四例 dry-run 是主实验结果或最终样本上限。
4. R3/R3.1 conversion / normalization recovery 是 Better STM repair 收益。
5. `partial` / `blocked` / no-canonical 样例可直接进入模型级 Better STM 判定。

## 6. 验证命令

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/evaluation/tests
```

若仓库没有 Codecov 或 PR 无覆盖率评论，不得虚构 coverage 数字；只能把本地 pytest 与 GitHub `feedback-smoke` 作为 coverage proxy，并说明局限。
