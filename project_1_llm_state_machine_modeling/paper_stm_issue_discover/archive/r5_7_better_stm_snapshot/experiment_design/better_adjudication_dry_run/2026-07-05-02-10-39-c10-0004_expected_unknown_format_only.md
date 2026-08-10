# C10 — 格式变化但 action 证据不足

> 证据引用说明：本文件中的 `[src-*]` / `[clm-*]` / `[cmd-*]` key 指向文末审计附录。

## 1. 输入事实源

- base pair：`llms_emp_stm_results_0004`（Train Control / GPT-4o / T0 HSM）`[src-baseline]`
- machine bundle：[project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c10_0004_expected_unknown_format_only](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c10_0004_expected_unknown_format_only/) `[src-case-bundle]`
- candidate sha256：`9c8a08f8d045d5b4030f60b92119ad029cbcad8013344646b0aef607f464e610` `[src-case-bundle]`

## 2. 构造变化

只把 Closed/SendDeparted 改写成 Closed event，无法证明 SendDeparted 已保留。 `[clm-change]`

## 3. expected gate path

| gate | expected status |
|---|---|
| G0 | `pass` |
| G1 | `pass` |
| G2 | `pass` |
| G3 | `unknown` |
| G4 | `unknown` |
| G5 | `unknown` |
| G6 | `pass` |

## 4. expected verdict

- `scope_routing_status`: `in_scope_t0_protocol_case`
- `run_validity_status`: `valid_constructed_protocol_case`
- `primary_expected_verdict`: `unknown` `[clm-verdict]`
- `headline_eligible=false`; `repair_effectiveness_eligible=false`。

## 5. 反例意义与禁止外推

本 case 用于覆盖 `evidence_insufficient, ambiguous_action_effect_mapping, trace_loss`。它只能说明评价协议如何处理该风险，不能说明真实 repair loop 的成功率或失败率 `[clm-boundary]`。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | 当前 PR 提交 | R5.7.5 首次新增 `C10` constructed case 文档 | — | [expected_verdict.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c10_0004_expected_unknown_format_only/expected_verdict.json) |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-baseline] | baseline_pointer | [baseline_pointer.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c10_0004_expected_unknown_format_only/baseline_pointer.json) | json | baseline 来源 | `$.base_pair_id`, `$.baseline_path` |
| [src-case-bundle] | case_bundle | [case bundle](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c10_0004_expected_unknown_format_only/) | directory | candidate、ledger、expected verdict | `candidate.fcstm`, `expected_verdict.json` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-change] | C10-C1 | 构造变化：只把 Closed/SendDeparted 改写成 Closed event，无法证明 SendDeparted 已保留。 | trace | [src-case-bundle] `change_ledger.json` | [cmd-json] | high | 人工构造，不是真实 repair 输出。 |
| [clm-verdict] | C10-C2 | expected verdict 为 `unknown`。 | classification | [src-case-bundle] `expected_verdict.json` | [cmd-json] | high | 只作为 protocol expectation。 |
| [clm-boundary] | C10-C3 | 本 case 不支持 repair effectiveness。 | prohibition | [src-case-bundle] `headline_eligible=false` | [cmd-json] | high | R7/R8 真实 run 可另行评估。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 目的 |
|---|---|---|
| [cmd-json] | 见下方可复制命令。 | 检查 JSON 与 expected verdict；C17 还检查 candidate 预期 parse-invalid。 |


#### [cmd-json] 可复制复验命令

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --case C10 --parse
```
