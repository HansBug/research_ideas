# DRY_RUNS.md — R4 四例评价门 dry-run

## 0. 定位

本文件集中说明 R4 对四个静态 `<NL, STM_0>` smoke 样例的评价门 dry-run。四例来自 [../selected_seed_examples/](../selected_seed_examples/)，只用于验证 diagnostic / scenario / eligibility / Better STM checklist 字段能否被审计，不调用真实 LLM，不执行 repair loop，不产生主实验结果，也不构成最终样本上限。

四例的 machine-readable fixture 保存在 [dry_run_examples/](./dry_run_examples/) 下。每个样例目录只保留 JSON 证据包，不再单独维护 README，避免说明分散。

## 1. 总览

| example_id | R3 status | canonical | R4 decision | model-level evaluation | 关键原因 |
|---|---|---:|---|---:|---|
| `llms-emp-gpt4o-hldcs` | `converted` | yes | `complete` | yes | official SCXML canonical 可用且 losses=0；但 R4 仍不 claim Better。 |
| `sefm-ssc7-umple` | `partial` | yes | `focused` | no | Umple `after(60)` timing loss 必须保留。 |
| `ttool-automatedbraking-xml` | `partial` | inventory-only | `focused` | no | TTool XML 只做 SMD inventory，connector/timing 未解释为纯 T0。 |
| `unified-uml-synthetic-0000` | `partial` | no | `blocked` | no | 官方 PlantUML syntax failed，无 trusted canonical，禁止 source-text fallback。 |

## 2. Better STM dry-run 结论

四例均为 `evaluation_context=gate_dry_run`，因此 `can_claim_better_stm=false`。R4 只证明评价门字段与证据链可执行，不证明任何 repair loop 改善。

关键纪律：

1. `placeholder` scenario 不得作为 regression gate。
2. `unknown` / `not_applicable` 不得当作 Better STM pass。
3. conversion / normalization gain 不得计作 repair gain。
4. partial / blocked 样例不得进入 model-level Better STM 判定。

## 3. 单例详情

### 3.1 `llms-emp-gpt4o-hldcs`：高层驾驶模块 PlantUML 完整 dry-run

| 字段 | 值 |
|---|---|
| R3 status | `converted` |
| R3 code | `R3.STATUS.converted` |
| canonical | [llms-emp-gpt4o-hldcs.canonical_stm.json](../conversion/reports/canonical/llms-emp-gpt4o-hldcs.canonical_stm.json) |
| R4 decision | `complete` |
| model-level evaluation | `true` |
| repair-loop smoke | `true` |

输入与证据：

- NL: [../selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt](../selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt)
- STM_0: [../selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml](../selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml)
- R2 样例说明：[../selected_seed_examples/llms-emp-gpt4o-hldcs/README.md](../selected_seed_examples/llms-emp-gpt4o-hldcs/README.md)
- R3 转换摘要：[../conversion/reports/selected_seed_examples_summary.md](../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)
- R4 fixture：[eligibility](./dry_run_examples/llms-emp-gpt4o-hldcs/eligibility_decision.json)、[diagnostic](./dry_run_examples/llms-emp-gpt4o-hldcs/diagnostic_draft.json)、[scenario](./dry_run_examples/llms-emp-gpt4o-hldcs/scenario_draft.json)、[checklist](./dry_run_examples/llms-emp-gpt4o-hldcs/better_stm_checklist.json)

处理原因：R3 使用 PlantUML 官方 SCXML 导出生成 canonical，status=converted 且 losses_count=0，可完整验证 R4 字段链路。Caveat 是 R4 只是 gate dry-run，没有 `STM_k` 或 repair gain。

### 3.2 `sefm-ssc7-umple`：自助结账系统 Umple timing-loss focused dry-run

| 字段 | 值 |
|---|---|
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | [sefm-ssc7-umple.canonical_stm.json](../conversion/reports/canonical/sefm-ssc7-umple.canonical_stm.json) |
| R4 decision | `focused` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

输入与证据：

- NL: [../selected_seed_examples/sefm-ssc7-umple/nl.txt](../selected_seed_examples/sefm-ssc7-umple/nl.txt)
- STM_0: [../selected_seed_examples/sefm-ssc7-umple/stm0.ump](../selected_seed_examples/sefm-ssc7-umple/stm0.ump)
- R2 样例说明：[../selected_seed_examples/sefm-ssc7-umple/README.md](../selected_seed_examples/sefm-ssc7-umple/README.md)
- R3 转换摘要：[../conversion/reports/selected_seed_examples_summary.md](../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 loss ledger: [../conversion/reports/selected_seed_examples_loss_ledger.jsonl](../conversion/reports/selected_seed_examples_loss_ledger.jsonl)
- R4 fixture：[eligibility](./dry_run_examples/sefm-ssc7-umple/eligibility_decision.json)、[diagnostic](./dry_run_examples/sefm-ssc7-umple/diagnostic_draft.json)、[scenario](./dry_run_examples/sefm-ssc7-umple/scenario_draft.json)、[checklist](./dry_run_examples/sefm-ssc7-umple/better_stm_checklist.json)

处理原因：R3 canonical 结构可用但 status=partial；R4 focused dry-run 用于确保 timing loss 不被误计为 repair 目标或 Better STM 改善。Caveat 是 `R3.LOSS.timing.medium` 表示 raw Umple `after(60)` 未被 official SCXML 原样保留，因此只能验证 partial/loss caveat 表达，不能作为完整 timing semantics evaluation。

### 3.3 `ttool-automatedbraking-xml`：自动制动告警 TTool XML inventory focused dry-run

| 字段 | 值 |
|---|---|
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | [ttool-automatedbraking-xml.canonical_stm.json](../conversion/reports/canonical/ttool-automatedbraking-xml.canonical_stm.json) |
| R4 decision | `focused` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

输入与证据：

- NL: [../selected_seed_examples/ttool-automatedbraking-xml/nl.txt](../selected_seed_examples/ttool-automatedbraking-xml/nl.txt)
- STM_0: [../selected_seed_examples/ttool-automatedbraking-xml/stm0.xml](../selected_seed_examples/ttool-automatedbraking-xml/stm0.xml)
- R2 样例说明：[../selected_seed_examples/ttool-automatedbraking-xml/README.md](../selected_seed_examples/ttool-automatedbraking-xml/README.md)
- R3 转换摘要：[../conversion/reports/selected_seed_examples_summary.md](../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 loss ledger: [../conversion/reports/selected_seed_examples_loss_ledger.jsonl](../conversion/reports/selected_seed_examples_loss_ledger.jsonl)
- R4 fixture：[eligibility](./dry_run_examples/ttool-automatedbraking-xml/eligibility_decision.json)、[diagnostic](./dry_run_examples/ttool-automatedbraking-xml/diagnostic_draft.json)、[scenario](./dry_run_examples/ttool-automatedbraking-xml/scenario_draft.json)、[checklist](./dry_run_examples/ttool-automatedbraking-xml/better_stm_checklist.json)

处理原因：TTool 样例用于暴露 XML / SysML / AVATAR 切片压力；R4 focused dry-run 只检查降级与阻塞表达。Caveats 是 R3 canonical 是 XML/SMD inventory，不是完整解析的纯 T0 状态机；`R3.LOSS.structure.high` 表示 P1/P2 graphical IDs 未解析到精确 source/target；`R3.LOSS.timing.medium` 表示 AVATAR timing fields 未解释为 T0 semantics。

### 3.4 `unified-uml-synthetic-0000`：合成点餐菜单 PlantUML no-canonical blocked dry-run

| 字段 | 值 |
|---|---|
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | 无 |
| R4 decision | `blocked` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

输入与证据：

- NL: [../selected_seed_examples/unified-uml-synthetic-0000/nl.txt](../selected_seed_examples/unified-uml-synthetic-0000/nl.txt)
- STM_0: [../selected_seed_examples/unified-uml-synthetic-0000/stm0.puml](../selected_seed_examples/unified-uml-synthetic-0000/stm0.puml)
- R2 样例说明：[../selected_seed_examples/unified-uml-synthetic-0000/README.md](../selected_seed_examples/unified-uml-synthetic-0000/README.md)
- R3 转换摘要：[../conversion/reports/selected_seed_examples_summary.md](../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../conversion/reports/selected_seed_examples_conversion_report.json](../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 loss ledger: [../conversion/reports/selected_seed_examples_loss_ledger.jsonl](../conversion/reports/selected_seed_examples_loss_ledger.jsonl)
- R4 fixture：[eligibility](./dry_run_examples/unified-uml-synthetic-0000/eligibility_decision.json)、[diagnostic](./dry_run_examples/unified-uml-synthetic-0000/diagnostic_draft.json)、[scenario](./dry_run_examples/unified-uml-synthetic-0000/scenario_draft.json)、[checklist](./dry_run_examples/unified-uml-synthetic-0000/better_stm_checklist.json)

处理原因：No-canonical 样例用于验证 R4 能正确 blocked，而不是伪造模型级 evaluation。Caveats 是 PlantUML 官方 syntax check failed；R3 不信任 SCXML 导出；没有 canonical STM；不得使用 source-text regex 或旧 fixture 冒充转换结果；synthetic / non-control-domain 只能作为格式边界样例。

## 4. 后续传递给 R5/R6/R7 的约束

1. 只有 `complete` 样例可进入完整 deterministic smoke；`focused` 样例只能 limited / supplementary；`blocked` 样例只能 diagnostic-only。
2. R7 若扩大样本池，必须保留相同 eligibility / checklist 聚合逻辑。
3. R8 主结果必须区分 conversion attribution 与 repair-loop attribution。
