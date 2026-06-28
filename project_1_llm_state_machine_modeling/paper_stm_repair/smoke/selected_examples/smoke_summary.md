# R5 四例 smoke 摘要

本文件由 `python -m paper_stm_repair_smoke.cli run-selected` 生成。JSON 事实源是 [smoke_report.json](./smoke_report.json)，本 Markdown 只做人类阅读入口，不作为第二事实真源。

- examples: 4
- pass: 0
- partial: 4
- blocked: 0

> 当前 4 例全部落为 `partial` 是预期的 修正前基线状态，不表示 smoke 未跑通；每例 R5 contract checks 均通过。
> `partial` 仅表示上游 R3/R4/R4.5 已记录转换 / 表示层 loss 或 caveat，R5 不能把这些 loss 当作修正收益清零。

| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |
|---|---|---|---|---|---|---:|---|---|
| `llms-emp-gpt4o-hldcs` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 3 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-gpt4o-hldcs.json) |
| `sefm-ssc7-umple` | `partial` | `sefm-llm-state-machine` | `umple` | `partial` | `ok/ok` | 5 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/sefm-ssc7-umple.json) |
| `llms-emp-deepseek-microwave` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 7 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-deepseek-microwave.json) |
| `llms-emp-kimi-autonomous-collision` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 17 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-kimi-autonomous-collision.json) |

所有条目均为修正前 smoke；`repair_contribution_allowed=false`。`partial` 不表示不可用，而是表示进入后续 R6/R7 前必须保留转换 / 表示层 caveat。
