# R5 selected 四例 deterministic smoke 摘要

本文件由 `python -m paper_stm_repair_smoke.cli run-selected` 生成。JSON 事实源是 [smoke_report.json](./smoke_report.json)，本 Markdown 只做人类阅读入口，不作为第二事实真源。

- examples: 4
- pass: 0
- partial: 4
- blocked: 0

| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |
|---|---|---|---|---|---|---:|---|---|
| `llms-emp-gpt4o-hldcs` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 3 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-gpt4o-hldcs.json) |
| `sefm-ssc7-umple` | `partial` | `sefm-llm-state-machine` | `umple` | `partial` | `ok/ok` | 5 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/sefm-ssc7-umple.json) |
| `llms-emp-deepseek-microwave` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 7 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-deepseek-microwave.json) |
| `llms-emp-kimi-autonomous-collision` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 17 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](./smoke_records/llms-emp-kimi-autonomous-collision.json) |

所有条目均为 pre-repair smoke；`repair_contribution_allowed=false`。`partial` 不表示不可用，而是表示进入后续 R6/R7 前必须保留 conversion / representation caveat。
