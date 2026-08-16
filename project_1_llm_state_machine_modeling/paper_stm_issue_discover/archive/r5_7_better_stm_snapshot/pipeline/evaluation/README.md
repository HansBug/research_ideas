# evaluation/ — R4 诊断、场景与 Better STM 评价门 v0

## 0. 定位

`evaluation/` 是第一篇论文 `<NL, STM_0> -> STM_k / Better STM` 主线的评价门工作区。它在真实修正循环、真实 LLM 调用和正式主实验之前，冻结一套可审计的 R4 v0 规则：样例准入、诊断分类、场景 / 回归门、Better STM 五条件、人工裁决草案和后续指标表。

本目录只支撑 R4 dry-run 与后续 R5/R6/R7 的接口，不产生论文主结果，不证明修正循环有效，也不把四例冒烟写成最终实验集合。

## 1. 阅读顺序

1. [EVALUATION_GATE.md](./EVALUATION_GATE.md)：核心规则总表；优先阅读它来理解 R4 到底制定了什么规则。
2. [reports/dry_run_summary.md](./reports/dry_run_summary.md)：四个静态样例的 dry-run 总结、输入链接和 JSON 固化样例入口。
3. [schemas/](./schemas/) 与 [tests/](./tests/)：machine-readable contract 与回归测试。

## 2. 与上游目录的关系

| 上游 / 下游 | 关系 |
|---|---|
| [../../selected_seed_examples/](../../../../selected_seed_examples) | R4 dry-run 固定复用的四个静态 `<NL, STM_0>` 冒烟样例；这是 smoke 迷你文库，不是最终实验集合、样本上限或论文主结果集合。当前四例为 `llms-emp-deepseek-microwave`、`llms-emp-gpt4o-hldcs`、`llms-emp-kimi-autonomous-collision`、`sefm-ssc7-umple`；TTool 与 `unified-uml-synthetic-0000` 已从 selected smoke 移除，只能作为历史 / 后续专项 / registry 线索。 |
| [../conversion/](../../../../pipeline/conversion) | R3 转换器 v0 与 R3.1 PlantUML recovery eligibility audit；R4 只能引用其 status / loss / canonical 裁决，不得改写 R3 转换语义。 |
| [../../experiment_design/quality_model/better_stm_definition.md](../../experiment_design/quality_model/better_stm_definition.md) | Better STM 五条件的上游定义；本目录将其落成 checklist 与 schema。 |
| [../../experiment_design/README.md](../../experiment_design/README.md) | 上游顺序约束：评价门必须先于真实修正预演冻结。 |
| R5/R6/R7/R8 | R5/R6 复用本目录 schema 做 deterministic dry-run / loop skeleton；R7 才冻结正式实验 protocol；R8 才执行主实验。 |

## 3. 路径结构

```text
evaluation/
├── README.md
├── EVALUATION_GATE.md
├── reports/
│   └── dry_run_summary.md
├── human_rubric_v0.json
├── dry_run_examples/
│   └── <example_id>/
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

## 4. 四例 dry-run 总览

每个 `dry_run_examples/<example_id>/` 下的四类 JSON 固化样例 都必须同时保留两层追溯字段：

1. 顶层 `source_nl_path`、`source_stm0_path`、`source_meta_path`、`canonical_output_path`，方便后续脚本和人工 review 直接定位上游 NL、原始 `STM_0`、source meta 与 R3 canonical。
2. `traceability` 对象，保存同一组字段，作为 schema 统一入口和后续聚合逻辑的稳定字段。

二者必须与 R3 conversion report 中对应 `example_id` 的路径一致；不能只在 scenario / evidence locator 中间接出现，否则会削弱 R4 评价门证据链。

| 样例 | R3 裁决 | R4 decision | 用途 |
|---|---|---|---|
| `llms-emp-deepseek-microwave` | `converted` / official SCXML via R3.1 normalization replay | `complete` | microwave 依赖 R3.1 pre-SCXML normalization replay；raw `stm0.puml` 不覆盖，conversion / 规范化收益 不计入修正收益。 |
| `llms-emp-gpt4o-hldcs` | `converted` / official SCXML canonical | `complete` | 完整跑通 diagnostic + scenario + checklist 字段。 |
| `llms-emp-kimi-autonomous-collision` | `converted` / official SCXML canonical | `complete` | 新加入 Kimi 自动驾驶 / 碰撞规避样例，验证较复杂 PlantUML canonical 的 gate 字段链路。 |
| `sefm-ssc7-umple` | `partial` / official SCXML + timing loss | `focused` | 验证 partial canonical 与 timing caveat 的表达。 |

详情见 [reports/dry_run_summary.md](./reports/dry_run_summary.md)。

## 5. 禁止主张

R4 可以声称：本文在 修正循环 前定义并 dry-run 了可审计的诊断 / 场景 / Better STM 评价门 v0。

R4 不能声称：

1. 修正循环已经有效；R6/R8 才涉及修正运行。
2. 正式实验 protocol 已冻结；R7 才冻结。
3. 四例 dry-run 是主实验结果或最终样本上限。
4. R3/R3.1 conversion / normalization recovery 是 Better STM repair 收益。
5. `partial` / `blocked` / no-canonical / normalization-recovered 样例可直接进入模型级 Better STM 判定。
6. `llms-emp-deepseek-microwave` 的 R3.1 pre-SCXML normalization replay 可计入 conversion eligibility，但不能计入修正收益；raw `stm0.puml` 不得覆盖。
7. TTool 与 `unified-uml-synthetic-0000` 已不属于当前四例 dry-run；若未来恢复，只能作为补充 adapter / registry case 重新准入。

## 6. 验证命令

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests
```

若仓库没有 Codecov 或 PR 无覆盖率评论，不得虚构 coverage 数字；只能把本地 pytest 与 GitHub `feedback-smoke` 作为 coverage proxy，并说明局限。

## 6. 维护纪律

1. 不改写 R3 裁决：R4 只能引用或映射 R3 `status_reason_code`、diagnostic code 与 loss code；不能把 R3 `partial` 写成 `converted`。
2. 不混淆 conversion 与 repair：R3.1 recovery 只属于 conversion eligibility，不属于 Better STM repair 收益。
3. 不伪造 canonical：no-canonical 样例只能 blocked / diagnostic-only，不得用 source-text regex、旧固化样例或人工脑补生成模型级评价输入。
4. 不把 `unknown` 当 `pass`；任一关键 `unknown` 都不能支持 Better STM 主张。
5. 不把 `placeholder` oracle 当回归门；`oracle_type=placeholder` 时必须 `is_regression_gate=false`。
6. 不调用真实 LLM、不读取 `.env`、不执行修正循环。
7. 规则事实集中维护在 [EVALUATION_GATE.md](./EVALUATION_GATE.md)；四例说明集中维护在 [reports/dry_run_summary.md](./reports/dry_run_summary.md)，不要再拆出平行规则文档。

新增 dry-run 样例时，必须先确认一手 seed 与 R3 conversion report，再生成 `eligibility_decision.json`、`diagnostic_draft.json`、`scenario_draft.json`、`better_stm_checklist.json`，并保证四类 JSON 顶层都有 `source_nl_path`、`source_stm0_path`、`source_meta_path` 与 `canonical_output_path`。

## 7. 验收命令

```bash
python -m pytest project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/tests
```

若测试失败，先判断是否破坏学术证据链：例如 R3 status 不一致、`unknown` 被计为 pass、placeholder oracle 被当作回归门，应优先修复。
