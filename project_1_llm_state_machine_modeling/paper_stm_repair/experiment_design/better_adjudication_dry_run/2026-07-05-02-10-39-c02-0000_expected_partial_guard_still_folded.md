# C02 — 条件仍折叠在 event label

> 证据引用说明：本文件中的 `[src-*]` / `[clm-*]` / `[cmd-*]` key 指向文末审计附录。

## 1. 输入事实源

- base pair：`llms_emp_stm_results_0000`（HLDCS / GPT-4o / T0 HSM）`[src-baseline]`
- machine bundle：[project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c02_0000_expected_partial_guard_still_folded](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c02_0000_expected_partial_guard_still_folded/) `[src-case-bundle]`
- candidate sha256：`288c4fd1cdb90ad440047b2334afc1c5995e35809ff6dfea4a8ba61d0f4e33ce` `[src-case-bundle]`

## 2. 构造变化

只重命名 folded event，不建立可机检 guard。 `[clm-change]`

## 3. expected gate path

| gate | expected status |
|---|---|
| G0 | `pass` |
| G1 | `pass` |
| G2 | `pass` |
| G3 | `pass` |
| G4 | `partial` |
| G5 | `partial` |
| G6 | `pass` |

## 4. expected verdict

- `scope_routing_status`: `in_scope_t0_protocol_case`
- `run_validity_status`: `valid_constructed_protocol_case`
- `primary_expected_verdict`: `partial` `[clm-verdict]`
- `headline_eligible=false`; `repair_effectiveness_eligible=false`。

## 5. 反例意义与禁止外推

本 case 用于覆盖 `guard_action_event_folding, under_repair`。它只能说明评价协议如何处理该风险，不能说明真实 repair loop 的成功率或失败率 `[clm-boundary]`。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | 当前 PR 提交 | R5.7.5 首次新增 `C02` constructed case 文档 | — | [expected_verdict.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c02_0000_expected_partial_guard_still_folded/expected_verdict.json) |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-baseline] | baseline_pointer | [baseline_pointer.json](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c02_0000_expected_partial_guard_still_folded/baseline_pointer.json) | json | baseline 来源 | `$.base_pair_id`, `$.baseline_path` |
| [src-case-bundle] | case_bundle | [case bundle](../../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/c02_0000_expected_partial_guard_still_folded/) | directory | candidate、ledger、expected verdict | `candidate.fcstm`, `expected_verdict.json` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-change] | C02-C1 | 构造变化：只重命名 folded event，不建立可机检 guard。 | trace | [src-case-bundle] `change_ledger.json` | [cmd-json] | high | 人工构造，不是真实 repair 输出。 |
| [clm-verdict] | C02-C2 | expected verdict 为 `partial`。 | classification | [src-case-bundle] `expected_verdict.json` | [cmd-json] | high | 只作为 protocol expectation。 |
| [clm-boundary] | C02-C3 | 本 case 不支持 repair effectiveness。 | prohibition | [src-case-bundle] `headline_eligible=false` | [cmd-json] | high | R7/R8 真实 run 可另行评估。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 目的 |
|---|---|---|
| [cmd-json] | 见下方可复制命令。 | 检查 JSON 与 expected verdict；C17 还检查 candidate 预期 parse-invalid。 |


#### [cmd-json] 可复制复验命令

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --case C02 --parse
```
