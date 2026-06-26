# 自动制动告警 TTool XML inventory focused dry-run

## 1. R4 decision

| 字段 | 值 |
|---|---|
| `example_id` | `ttool-automatedbraking-xml` |
| R3 status | `partial` |
| R3 code | `R3.STATUS.partial` |
| canonical | `project_1_llm_state_machine_modeling/paper_stm_repair/conversion/reports/canonical/ttool-automatedbraking-xml.canonical_stm.json` |
| R4 decision | `focused` |
| model-level evaluation | `false` |
| repair-loop smoke | `false` |

## 2. 输入链接

- NL: [nl.txt](../../../selected_seed_examples/ttool-automatedbraking-xml/nl.txt)
- STM_0: [stm0.xml](../../../selected_seed_examples/ttool-automatedbraking-xml/stm0.xml)
- R2 样例说明：[selected_seed_examples/ttool-automatedbraking-xml/README.md](../../../selected_seed_examples/ttool-automatedbraking-xml/README.md)
- R3 转换摘要：[selected_seed_examples_summary.md](../../../conversion/reports/selected_seed_examples_summary.md)
- R3 转换 JSON：[selected_seed_examples_conversion_report.json](../../../conversion/reports/selected_seed_examples_conversion_report.json)
- R3 canonical: [ttool-automatedbraking-xml.canonical_stm.json](../../../conversion/reports/canonical/ttool-automatedbraking-xml.canonical_stm.json)
- R3 loss ledger: [selected_seed_examples_loss_ledger.jsonl](../../../conversion/reports/selected_seed_examples_loss_ledger.jsonl)

## 3. 为什么这样处理

TTool 样例用于暴露 XML / SysML / AVATAR 切片压力；R4 focused dry-run 只检查降级与阻塞表达。

## 4. Caveats

- R3 canonical 是 XML/SMD inventory，不是完整解析的纯 T0 状态机。
- R3.LOSS.structure.high: P1/P2 graphical IDs 未解析到精确 source/target。
- R3.LOSS.timing.medium: AVATAR timing fields 未解释为 T0 semantics。

## 5. R4 fixture

| 文件 | 作用 |
|---|---|
| [eligibility_decision.json](./eligibility_decision.json) | 记录该样例能否进入 complete / focused / blocked dry-run。 |
| [diagnostic_draft.json](./diagnostic_draft.json) | 记录 R4 diagnostic draft 与 R3 evidence locator。 |
| [scenario_draft.json](./scenario_draft.json) | 记录最小 scenario / regression gate 草案。 |
| [better_stm_checklist.json](./better_stm_checklist.json) | 记录 Better STM 五条件 dry-run 判定；R4 默认不得 claim Better。 |
