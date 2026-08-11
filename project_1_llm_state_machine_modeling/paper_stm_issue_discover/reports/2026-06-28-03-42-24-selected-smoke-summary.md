# R5 selected 四例 deterministic smoke 摘要

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排；新增证据时只新增 key，不批量改旧 key。

## R5 selected 四例 deterministic smoke 摘要

本 report 迁移自 R5 `run-selected` 生成的旧 human summary；当前 JSON 事实源是 [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json)，本 Markdown 只做人类阅读入口，不作为第二事实真源 [src-smoke-report]。

- examples: 4 [clm-smoke-status]
- pass: 0 [clm-smoke-status]
- partial: 4 [clm-smoke-status]
- blocked: 0 [clm-smoke-status]

> 当前 4 例全部落为 `partial` 是预期的 pre-repair baseline state，不表示 smoke 未跑通；每例 R5 contract checks 均通过 [clm-smoke-checks]。`partial` 仅表示上游 R3/R4/R4.5 已记录 conversion / representation loss 或 caveat，R5 不能把这些 loss 当作 repair gain 清零 [clm-smoke-r3-r45]。

| example_id | status | seed | 格式 | R3 | R4.5 parse/inspect | loss | 关键原因 | record |
|---|---|---|---|---|---|---:|---|---|
| `llms-emp-gpt4o-hldcs` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 3 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-gpt4o-hldcs.json) |
| `sefm-ssc7-umple` | `partial` | `sefm-llm-state-machine` | `umple` | `partial` | `ok/ok` | 5 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/sefm-ssc7-umple.json) |
| `llms-emp-deepseek-microwave` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 7 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-deepseek-microwave.json) |
| `llms-emp-kimi-autonomous-collision` | `partial` | `llms-emp-stm-subset` | `plantuml` | `converted` | `ok/ok` | 17 | `R5.SELECTED.partial_upstream_caveat_or_loss` | [record](../pipeline/readiness_audit/selected_examples/smoke_records/llms-emp-kimi-autonomous-collision.json) |

所有条目均为 pre-repair smoke；`repair_contribution_allowed=false`。`partial` 不表示不可用，而是表示进入后续 R6/R7 前必须保留 conversion / representation caveat [clm-smoke-checks][clm-smoke-r3-r45]。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/selected_examples/smoke_summary.md` | `6e1d8b510209804a0e4afeeeed4a81720d398270` (2026-06-28 03:10:11 +0800, R5 smoke 初始生成) | `5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4` (2026-06-28 03:42:24 +0800, selected smoke 学术解释冻结) | `5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4` (2026-06-28 03:42:24 +0800)：收敛证据链审查问题后形成本 report 命名时间；后续入口简化与路径迁移不改变 selected smoke 的 4/0/4/0 事实。 | `58564df31b4777228cb3850074c9cc8fd4a78c99` (2026-06-28 14:07:34 +0800, 文档入口简化)、`73af4d83a7ccffeac47ca61ab6708bfcbfe44c6f` (2026-06-28 15:06:16 +0800, pipeline 路径迁移)、`1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [selected smoke JSON](../pipeline/readiness_audit/selected_examples/smoke_report.json)；[selected smoke records](../pipeline/readiness_audit/selected_examples/smoke_records/) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-smoke-report] | `smoke_report` | [smoke_report.json](../pipeline/readiness_audit/selected_examples/smoke_report.json) | `json` | 支撑四例总数、状态、generation context 与 `repair_contribution_allowed=false` | `#/summary`、`#/items[]`、`#/generation_context` |
| [src-smoke-records] | `smoke_records` | [smoke_records/](../pipeline/readiness_audit/selected_examples/smoke_records/) | `json` | 支撑每个 example 的 nested R3/R4.5 字段、hash 与 trace checks | `*.json#/checks`、`#/source`、`#/upstream_r3`、`#/upstream_r45` |
| [src-smoke-selected] | `selected_examples` | [../selected_seed_examples/](../selected_seed_examples/) | `source` | 支撑四例 `NL + STM_0 + converted .fcstm` 文件存在与 hash 对齐 | `example_id/{nl.txt,stm0.*,model.fcstm,source_meta.json,fcstm_meta.json}` |
| [src-smoke-r3-conversion] | `conversion_report` | [selected_seed_examples_conversion_report.json](../pipeline/conversion/reports/selected_seed_examples_conversion_report.json) | `json` | 支撑 R3 转换状态与 canonical source | `#/items[example_id=...]` |
| [src-smoke-r45-fcstm] | `fcstm_report` | [fcstm_export_report.json](../pipeline/representation/reports/fcstm_export_report.json) | `json` | 支撑 R4.5 `.fcstm` lowering / parse / inspect 状态 | `#/items[example_id=...]` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-smoke-status] | `R5-SMOKE-C1` | selected smoke 共 4 例，`pass=0 / partial=4 / blocked=0`。 | `count` | `smoke_report#/summary` | [cmd-smoke-summary] | `high` | 只说明 deterministic smoke 状态，不代表正式实验结果。 |
| [clm-smoke-checks] | `R5-SMOKE-C2` | 四例 contract checks 均通过，且 `repair_contribution_allowed=false`。 | `trace` | `smoke_report#/items[].checks`、`smoke_records/*.json#/checks` | [cmd-smoke-records] | `high` | checks 证明文件链路和 hash 一致，不证明 repair loop 已运行。 |
| [clm-smoke-r3-r45] | `R5-SMOKE-C3` | 表格中的 R3/R4.5 与 loss 数来自 nested smoke record 字段。 | `trace` | `items[].upstream_r3.status`、`items[].upstream_r45.{parse_status,inspect_status,loss_count}` | [cmd-smoke-records] | `high` | `loss_count` 是 pre-repair caveat，不是 repair gain。 |
| [clm-smoke-provenance] | `R5-SMOKE-C4` | 生成时 `generation_context.git_dirty=true`，但 report 以 committed JSON、schema hash 与 selected files 复验。 | `risk` | `smoke_report#/generation_context` | [cmd-smoke-summary] | `medium` | dirty tree 是 provenance caveat；不得只凭 `repo_commit` 重建完整工作树状态。 |

### A.4 复验命令

```bash
# [cmd-smoke-summary] CMD-SMOKE-1 / CMD-SMOKE-4
python - <<'PY'
import json
p='project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/selected_examples/smoke_report.json'
d=json.load(open(p))
print(d['summary'])
print({'git_dirty': d['generation_context']['git_dirty'], 'git_dirty_path_count': d['generation_context']['git_dirty_path_count'], 'repair_contribution_allowed': d['repair_contribution_allowed']})
PY
```

```bash
# [cmd-smoke-records] CMD-SMOKE-2 / CMD-SMOKE-3
python - <<'PY'
import json, pathlib
base=pathlib.Path('project_1_llm_state_machine_modeling/paper_stm_issue_discover/pipeline/readiness_audit/selected_examples/smoke_records')
for fp in sorted(base.glob('*.json')):
    r=json.load(open(fp))
    print(fp.name, r['status'], all(r['checks'].values()), r['upstream_r3']['status'], r['upstream_r45']['parse_status']+'/'+r['upstream_r45']['inspect_status'], r['upstream_r45']['loss_count'])
PY
```
