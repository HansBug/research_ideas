# R4 dry_run_examples

本目录保存 PR-R4 对 #119 固定四例 smoke panel 的评价门 dry-run fixture。它只验证 diagnostic / scenario / eligibility / Better STM checklist 字段能否被审计，不调用真实 LLM，不执行 repair loop，不产生主实验结果。

| 样例 | R4 decision | 说明 |
|---|---|---|
| [llms-emp-gpt4o-hldcs](./llms-emp-gpt4o-hldcs/README.md) | `complete` | R3 converted，可完整跑通字段链路。 |
| [sefm-ssc7-umple](./sefm-ssc7-umple/README.md) | `focused` | canonical 可用但有 timing loss。 |
| [ttool-automatedbraking-xml](./ttool-automatedbraking-xml/README.md) | `focused` | XML/SMD inventory-only，不是纯 T0 STM。 |
| [unified-uml-synthetic-0000](./unified-uml-synthetic-0000/README.md) | `blocked` | 官方 PlantUML syntax failed，无 trusted canonical。 |

关键纪律：

1. `placeholder` scenario 不得作为 regression gate。
2. `unknown` / `not_applicable` 不得当作 Better STM pass。
3. conversion / normalization gain 不得计作 repair gain。
4. partial / blocked 样例不得进入 model-level Better STM 判定。
