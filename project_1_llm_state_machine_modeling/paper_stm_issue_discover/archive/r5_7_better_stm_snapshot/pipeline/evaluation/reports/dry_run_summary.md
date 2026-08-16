> **工具输出摘要 / 非 canonical report。** 本文件只作为 R4 evaluation dry-run fixture 的机器邻近摘要；论文写作、人类审查和跨阶段学术结论请回到 `paper_stm_repair/reports/` 下的秒级 canonical report，row-level facts 以 `dry_run_examples/*/*.json` 与相关 schema 为准。

# R4 四例评价门 dry-run 摘要

## 0. 定位

本文件集中说明 R4 对四个静态 `<NL, STM_0>` 冒烟样例的评价门 dry-run。四例来自 [../../../selected_seed_examples/](../../../../../selected_seed_examples)，这是冒烟迷你文库，只用于验证 diagnostic / scenario / eligibility / Better STM checklist 字段能否被审计；它不调用真实 LLM，不执行修正循环，不产生主实验结果，也不构成最终实验集合或样本上限。当前四例为 `llms-emp-deepseek-microwave`、`llms-emp-gpt4o-hldcs`、`llms-emp-kimi-autonomous-collision`、`sefm-ssc7-umple`；TTool 与 `unified-uml-synthetic-0000` 已从 selected smoke 移除，只能作为历史 / 后续专项 / registry 线索。

四例的 machine-readable fixture 保存在 [dry_run_examples/](../dry_run_examples/) 下。每个样例目录只保留 JSON 证据包，不再单独维护 README，避免说明分散。每个 JSON 证据包顶层都必须直接给出 `source_nl_path`、`source_stm0_path`、`source_meta_path`、`canonical_output_path`，同时在 `traceability` 对象中保留同一组字段，确保本阶段 report 不需要间接解析 evidence locator 就能回到上游 NL 与原始 `STM_0`。

## 1. 总览

| example_id | R3 status | 规范化中间表示 | R4 decision | model-level evaluation | 关键原因 |
|---|---|---:|---|---:|---|
| `llms-emp-deepseek-microwave` | `converted` | yes | `complete` | yes | microwave 依赖 R3.1 pre-SCXML normalization replay 后的官方 SCXML；raw `stm0.puml` 不覆盖，规范化收益不计入修正收益。 |
| `llms-emp-gpt4o-hldcs` | `converted` | yes | `complete` | yes | 官方 SCXML 规范化中间表示可用且 losses=0；但 R4 仍不主张 Better。 |
| `llms-emp-kimi-autonomous-collision` | `converted` | yes | `complete` | yes | Kimi 自动驾驶 / 碰撞规避 PlantUML 样例加入；官方 SCXML 规范化中间表示可用。 |
| `sefm-ssc7-umple` | `partial` | yes | `focused` | no | Umple `after(60)` timing loss 必须保留。 |

## 2. Better STM dry-run 结论

四例均为 `evaluation_context=gate_dry_run`，因此 `can_claim_better_stm=false`。R4 只证明评价门字段与证据链可执行，不证明任何修正循环改善。

关键纪律：

1. `placeholder` scenario 不得作为 regression gate。
2. `unknown` / `not_applicable` 不得当作 Better STM pass。
3. 转换 / 规范化 gain 不得计作修正收益。
4. partial / blocked 样例不得进入 model-level Better STM 判定；normalization-recovered 样例即使可进入 complete dry-run，也只能把恢复收益归入转换归因。
5. `llms-emp-deepseek-microwave` 的 converted 依赖 R3.1 pre-SCXML normalization replay，只能作为 conversion eligibility / dry-run 证据；不能计入修正收益，且不得覆盖 raw `stm0.puml`。

## 3. 单例详情

### 3.1 `llms-emp-deepseek-microwave`：DeepSeek microwave PlantUML normalization-recovered 完整 dry-run

| 字段 | 值 |
|---|---|
| R3 status | `converted` |
| R3 code | `R3.STATUS.converted` |
| canonical JSON | [llms-emp-deepseek-microwave.canonical_stm.json](../../../../../pipeline/conversion/reports/canonical/llms-emp-deepseek-microwave.canonical_stm.json) |
| R4 decision | `complete` |
| model-level evaluation | `true` |
| repair-loop contract dry-run eligibility | `true` |

输入与证据：

- NL: [../../../selected_seed_examples/llms-emp-deepseek-microwave/nl.txt](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-deepseek-microwave/nl.txt)
- raw STM_0: [../../../selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml)
- R2 样例说明：[../../../selected_seed_examples/llms-emp-deepseek-microwave/README.md](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-deepseek-microwave/README.md)
- R3 转换摘要：[../../conversion/reports/selected_seed_examples_summary.md](../../../../../pipeline/conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../../conversion/reports/selected_seed_examples_conversion_report.json](../../../../../pipeline/conversion/reports/selected_seed_examples_conversion_report.json)
- R3/R3.1 normalization 报告：[../../conversion/reports/plantuml_recovery_report.json](../../../../../pipeline/conversion/reports/plantuml_recovery_report.json)、[../../conversion/reports/plantuml_recovery_summary.md](../../../../../pipeline/conversion/reports/plantuml_recovery_summary.md)
- R4 fixture：[eligibility](../dry_run_examples/llms-emp-deepseek-microwave/eligibility_decision.json)、[diagnostic](../dry_run_examples/llms-emp-deepseek-microwave/diagnostic_draft.json)、[scenario](../dry_run_examples/llms-emp-deepseek-microwave/scenario_draft.json)、[checklist](../dry_run_examples/llms-emp-deepseek-microwave/better_stm_checklist.json)

处理原因：该例替换历史 synthetic 冒烟，用于在当前四例中覆盖 R3.1 pre-SCXML normalization replay。R3 report 中 `canonical_output_path` 指向 replay 后官方 SCXML 派生的规范化中间表示；R4 只把它作为 conversion eligibility 证据。Caveats 是 raw [stm0.puml](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-deepseek-microwave/stm0.puml) 必须保持一手输入、不得覆盖；normalization / 转换 / 表示层带来的可解析性改善不能计入修正收益；microwave 标签中的时间 / guard 语义在当前阶段只作 dry-run caveat。

### 3.2 `llms-emp-gpt4o-hldcs`：高层驾驶模块 PlantUML 完整 dry-run

| 字段 | 值 |
|---|---|
| R3 status | `converted` |
| R3 code | `R3.STATUS.converted` |
| canonical JSON | [llms-emp-gpt4o-hldcs.canonical_stm.json](../../../../../pipeline/conversion/reports/canonical/llms-emp-gpt4o-hldcs.canonical_stm.json) |
| R4 decision | `complete` |
| model-level evaluation | `true` |
| repair-loop contract dry-run eligibility | `true` |

输入与证据：

- NL: [../../../selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-gpt4o-hldcs/nl.txt)
- STM_0: [../../../selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-gpt4o-hldcs/stm0.puml)
- R2 样例说明：[../../../selected_seed_examples/llms-emp-gpt4o-hldcs/README.md](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-gpt4o-hldcs/README.md)
- R3 转换摘要：[../../conversion/reports/selected_seed_examples_summary.md](../../../../../pipeline/conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../../conversion/reports/selected_seed_examples_conversion_report.json](../../../../../pipeline/conversion/reports/selected_seed_examples_conversion_report.json)
- R4 fixture：[eligibility](../dry_run_examples/llms-emp-gpt4o-hldcs/eligibility_decision.json)、[diagnostic](../dry_run_examples/llms-emp-gpt4o-hldcs/diagnostic_draft.json)、[scenario](../dry_run_examples/llms-emp-gpt4o-hldcs/scenario_draft.json)、[checklist](../dry_run_examples/llms-emp-gpt4o-hldcs/better_stm_checklist.json)

处理原因：R3 使用 PlantUML 官方 SCXML 导出生成 canonical JSON，status=converted 且 losses_count=0，可完整验证 R4 字段链路。Caveat 是 R4 只是 gate dry-run，没有 `STM_k` 或修正收益。

### 3.3 `llms-emp-kimi-autonomous-collision`：Kimi 自动驾驶 / 碰撞规避 PlantUML 完整 dry-run

| 字段 | 值 |
|---|---|
| R3 status | `converted` |
| R3 code | `R3.STATUS.converted` |
| canonical JSON | [llms-emp-kimi-autonomous-collision.canonical_stm.json](../../../../../pipeline/conversion/reports/canonical/llms-emp-kimi-autonomous-collision.canonical_stm.json) |
| R4 decision | `complete` |
| model-level evaluation | `true` |
| repair-loop contract dry-run eligibility | `true` |

输入与证据：

- NL: [../../../selected_seed_examples/llms-emp-kimi-autonomous-collision/nl.txt](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-kimi-autonomous-collision/nl.txt)
- STM_0: [../../../selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-kimi-autonomous-collision/stm0.puml)
- R2 样例说明：[../../../selected_seed_examples/llms-emp-kimi-autonomous-collision/README.md](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/llms-emp-kimi-autonomous-collision/README.md)
- R3 转换摘要：[../../conversion/reports/selected_seed_examples_summary.md](../../../../../pipeline/conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../../conversion/reports/selected_seed_examples_conversion_report.json](../../../../../pipeline/conversion/reports/selected_seed_examples_conversion_report.json)
- R4 fixture：[eligibility](../dry_run_examples/llms-emp-kimi-autonomous-collision/eligibility_decision.json)、[diagnostic](../dry_run_examples/llms-emp-kimi-autonomous-collision/diagnostic_draft.json)、[scenario](../dry_run_examples/llms-emp-kimi-autonomous-collision/scenario_draft.json)、[checklist](../dry_run_examples/llms-emp-kimi-autonomous-collision/better_stm_checklist.json)

处理原因：Kimi 样例加入当前四例 selected 冒烟，用于覆盖较复杂 PlantUML HSM / 自动驾驶碰撞规避场景。R3 使用 PlantUML 官方 SCXML 导出生成 canonical JSON，status=converted 且 losses_count=0，可完整验证 R4 字段链路。Caveat 是 R4 只是 gate dry-run，没有 `STM_k` 或修正收益；PlantUML 条件标签不被自动包装成严格 guard 语义。

### 3.4 `sefm-ssc7-umple`：自助结账系统 Umple timing-loss focused dry-run

| 字段 | 值 |
|---|---|
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical JSON | [sefm-ssc7-umple.canonical_stm.json](../../../../../pipeline/conversion/reports/canonical/sefm-ssc7-umple.canonical_stm.json) |
| R4 decision | `focused` |
| model-level evaluation | `false` |
| repair-loop contract dry-run eligibility | `false` |

输入与证据：

- NL: [../../../selected_seed_examples/sefm-ssc7-umple/nl.txt](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/sefm-ssc7-umple/nl.txt)
- STM_0: [../../../selected_seed_examples/sefm-ssc7-umple/stm0.ump](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/sefm-ssc7-umple/stm0.ump)
- R2 样例说明：[../../../selected_seed_examples/sefm-ssc7-umple/README.md](../../../../../pipeline/conversion/fixtures/r3_selected_seed_examples/sefm-ssc7-umple/README.md)
- R3 转换摘要：[../../conversion/reports/selected_seed_examples_summary.md](../../../../../pipeline/conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[../../conversion/reports/selected_seed_examples_conversion_report.json](../../../../../pipeline/conversion/reports/selected_seed_examples_conversion_report.json)
- R3 loss ledger: [../../conversion/reports/selected_seed_examples_loss_ledger.jsonl](../../../../../pipeline/conversion/reports/selected_seed_examples_loss_ledger.jsonl)
- R4 fixture：[eligibility](../dry_run_examples/sefm-ssc7-umple/eligibility_decision.json)、[diagnostic](../dry_run_examples/sefm-ssc7-umple/diagnostic_draft.json)、[scenario](../dry_run_examples/sefm-ssc7-umple/scenario_draft.json)、[checklist](../dry_run_examples/sefm-ssc7-umple/better_stm_checklist.json)

处理原因：R3 规范化中间表示结构可用但 status=partial；R4 focused dry-run 用于确保 timing loss 不被误计为 repair 目标或 Better STM 改善。Caveat 是 `R3.LOSS.timing.medium` 表示 raw Umple `after(60)` 未被 官方 SCXML 原样保留，因此只能验证 partial/loss caveat 表达，不能作为完整 timing semantics evaluation。

## 4. 后续传递给 R5/R6/R7 的约束

1. `complete` 样例可进入完整 确定性冒烟；`focused` 样例只能 limited / supplementary，尤其不能直接进入模型级 Better STM 判定。
2. R7 若扩大样本池，必须保留相同 eligibility / checklist 聚合逻辑，并继续把 selected examples 视为冒烟迷你文库而非最终实验集合。
3. R8 主结果必须区分 转换归因、normalization 归因与 repair-loop 归因。
4. TTool XML 与 `unified-uml-synthetic-0000` 若未来恢复，只能作为补充 adapter / supplementary / registry case 重新准入，不能回写成当前四例冒烟。
