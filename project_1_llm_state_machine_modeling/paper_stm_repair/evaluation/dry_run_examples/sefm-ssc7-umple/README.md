# 自助结账系统 Umple timing-loss focused dry-run

## 1. R4 decision

| 字段 | 值 |
|---|---|
| `example_id` | `sefm-ssc7-umple` |
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/canonical/sefm-ssc7-umple.canonical_stm.json` |
| R4 decision | `focused` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

## 2. 输入链接

- NL: [nl.txt](../../../selected_seed_examples/sefm-ssc7-umple/nl.txt)
- STM_0: [stm0.ump](../../../selected_seed_examples/sefm-ssc7-umple/stm0.ump)
- R2 样例说明：[selected_seed_examples/sefm-ssc7-umple/README.md](../../../selected_seed_examples/sefm-ssc7-umple/README.md)
- R3 转换摘要：[selected_seed_examples_summary.md](../../../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[selected_seed_examples_conversion_report.json](../../../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 canonical: [sefm-ssc7-umple.canonical_stm.json](../../../conversion/reports/canonical/sefm-ssc7-umple.canonical_stm.json)
- R3 loss ledger: [selected_seed_examples_loss_ledger.jsonl](../../../conversion/reports/selected_seed_examples_loss_ledger.jsonl)

## 3. 为什么这样处理

R3 canonical 结构可用但 status=partial；R4 focused dry-run 用于确保 timing loss 不被误计为 repair 目标或 Better STM 改善。

## 4. Caveats

- R3.LOSS.timing.medium: raw Umple after(60) 未被 official SCXML 原样保留。
- 只能验证 partial/loss caveat 表达，不能作为完整 timing semantics evaluation。

## 5. R4 fixture

| 文件 | 作用 |
|---|---|
| [eligibility_decision.json](./eligibility_decision.json) | 记录该样例能否进入 complete / focused / blocked dry-run。 |
| [diagnostic_draft.json](./diagnostic_draft.json) | 记录 R4 diagnostic draft 与 R3 evidence locator。 |
| [scenario_draft.json](./scenario_draft.json) | 记录最小 scenario / regression gate 草案。 |
| [better_stm_checklist.json](./better_stm_checklist.json) | 记录 Better STM 五条件 dry-run 判定；R4 默认不得 claim Better。 |
