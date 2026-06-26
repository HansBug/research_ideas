# R4 dry-run summary

| example_id | R3 status | canonical | R4 decision | model-level evaluation | 关键原因 |
|---|---|---:|---|---:|---|
| `llms-emp-gpt4o-hldcs` | `converted` | yes | `complete` | yes | official SCXML canonical 可用且 losses=0；但 R4 仍不 claim Better。 |
| `sefm-ssc7-umple` | `partial` | yes | `focused` | no | Umple `after(60)` timing loss 必须保留。 |
| `ttool-automatedbraking-xml` | `partial` | inventory-only | `focused` | no | TTool XML 只做 SMD inventory，connector/timing 未解释为纯 T0。 |
| `unified-uml-synthetic-0000` | `partial` | no | `blocked` | no | 官方 PlantUML syntax failed，无 trusted canonical，禁止 source-text fallback。 |

## Better STM dry-run 结论

四例均为 `evaluation_context=gate_dry_run`，因此 `can_claim_better_stm=false`。R4 只证明评价门字段与证据链可执行，不证明任何 repair loop 改善。

## 后续传递给 R5/R6/R7 的约束

1. 只有 `complete` 样例可进入完整 deterministic smoke；`focused` 样例只能 limited / supplementary；`blocked` 样例只能 diagnostic-only。
2. R7 若扩大样本池，必须保留相同 eligibility / checklist 聚合逻辑。
3. R8 主结果必须区分 conversion attribution 与 repair-loop attribution。
