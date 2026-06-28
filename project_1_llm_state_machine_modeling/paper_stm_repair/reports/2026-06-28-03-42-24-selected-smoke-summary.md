# R5 selected 四例 deterministic smoke 摘要

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/selected_examples/smoke_summary.md` | `6e1d8b51` (2026-06-28 03:10:11 +0800, R5 smoke 初始生成) | `73af4d83` (2026-06-28 15:05:25 +0800, `refactor(paper1-r5): 将阶段链路迁入pipeline路径`) | `5d0a2a01` (2026-06-28 03:42:24 +0800)：收敛证据链审查问题后形成本 report 命名时间；后续 `58564df3`/`73af4d83` 主要为入口简化与路径迁移。 | 本报告所在的 R5.5.1 migration commit（同一提交内无法自嵌最终 SHA；精确提交用 `git log --follow -- <report>` 复核）；仅迁移 human-facing report 与改写入口，不改 canonical machine facts。 | [selected smoke JSON](../pipeline/readiness_audit/selected_examples/smoke_report.json)；[selected smoke records](../pipeline/readiness_audit/selected_examples/smoke_records/) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## R5 selected 四例 deterministic smoke 摘要

本 report 迁移自 R5 `run-selected` 生成的旧 human summary；当前 JSON 事实源是 [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json)，本 Markdown 只做人类阅读入口，不作为第二事实真源。

- examples: 4
- pass: 0
- partial: 4
- blocked: 0

> 当前 4 例全部落为 `partial` 是预期的 pre-repair baseline state，不表示 smoke 未跑通；每例 R5 contract checks 均通过。
> `partial` 仅表示上游 R3/R4/R4.5 已记录 conversion / representation loss 或 caveat，R5 不能把这些 loss 当作 repair gain 清零。

| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |
|---|---|---|---|---|---|---:|---|---|
| `llms-emp-gpt4o-hldcs` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 3 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-gpt4o-hldcs.json) |
| `sefm-ssc7-umple` | `partial` | `sefm-llm-state-machine` | `umple` | `partial` | `ok/ok` | 5 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/sefm-ssc7-umple.json) |
| `llms-emp-deepseek-microwave` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 7 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-deepseek-microwave.json) |
| `llms-emp-kimi-autonomous-collision` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 17 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-kimi-autonomous-collision.json) |

所有条目均为 pre-repair smoke；`repair_contribution_allowed=false`。`partial` 不表示不可用，而是表示进入后续 R6/R7 前必须保留 conversion / representation caveat。
