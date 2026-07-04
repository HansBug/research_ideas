# R5.7.5 constructed STM_k 覆盖性 dry-run 报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与问题

R5.7.5 的目的不是运行真实 repair loop，而是构造一组可复验 `STM_k` 候选来压力测试 R5.7.1--R5.7.4 冻结的评价协议。所有候选均为人工 / 确定性构造，因此 `headline_eligible=false`、`repair_effectiveness_eligible=false`、`real_repair_run_id=null`；它们只能支持 protocol coverage claim `[clm-boundary]`。

## 2. 核心结论

1. 已落地 20 个 constructed `STM_k` case，覆盖 `better / not_better / partial / unknown / stmk_repair_failure / protocol_or_provenance_invalid / stress_t1` 七类主要输出 `[clm-suite]`。
2. `better` 仅在 protocol expectation 中出现（C01/C08/C11），用于验证 G0--G6 正路径能表达；不代表真实方法已经产生成功修复 `[clm-boundary]`。
3. anti-gaming 反例覆盖 semantic deletion、guard/action/event folding、over-repair、under-repair、trace loss、conversion laundering、hierarchy loss 与 textual similarity misuse；当前实现是 PR body 最小覆盖表的有意超集，用于让同一 case 同时标记次级风险，但不改变 primary expected verdict；`scenario_overfitting` 本轮明确未覆盖并交给 R7 `[clm-anti-gaming]`。
4. 0004 action-effect 覆盖使用手工 materialized protocol baseline；0009 complex guard 覆盖使用同 cluster selected smoke `0039` fallback。这两点都已写入 preflight caveat，不能外推成 0004/0009 的真实 repair 结果 `[clm-baseline]`。

## 3. expected verdict 覆盖表

| expected verdict | 数量 | case |
|---|---:|---|
| `better` | 3 | C01, C08, C11 |
| `not_better` | 7 | C03, C05, C06, C07, C09, C13, C20 |
| `partial` | 3 | C02, C14, C19 |
| `unknown` | 2 | C10, C12 |
| `stmk_repair_failure` | 1 | C17 |
| `protocol_or_provenance_invalid` | 3 | C04, C15, C18 |
| `stress_t1` | 1 | C16 |

注：上表统计的是 `primary_expected_verdict`，不是观察到的真实 repair 结果；`caveat_t05` 属于 scope routing 覆盖，由 C14/C15 覆盖。

## 4. 20 case 总表

| case | base pair | 构造目标 | expected verdict | scope | 风险 |
|---|---|---|---|---|---|
| C01 | `llms_emp_stm_results_0000` | 正确拆出 Front Distance guard | `better` | `in_scope_t0_protocol_case` | guard_action_event_folding |
| C02 | `llms_emp_stm_results_0000` | 条件仍折叠在 event label | `partial` | `in_scope_t0_protocol_case` | guard_action_event_folding, under_repair |
| C03 | `llms_emp_stm_results_0000` | guard 修好但破坏层级 | `not_better` | `in_scope_t0_protocol_case` | hierarchy_pseudostate_loss |
| C04 | `llms_emp_stm_results_0000` | 把 conversion/canonical 改善冒充 repair | `protocol_or_provenance_invalid` | `in_scope_t0_protocol_case` | conversion_laundering |
| C05 | `llms_emp_stm_results_0001` | no-op candidate | `not_better` | `in_scope_t0_protocol_case` | no_improvement |
| C06 | `llms_emp_stm_results_0001` | 低噪声 control 上过修复 | `not_better` | `in_scope_t0_protocol_case` | over_repair, trace_loss |
| C07 | `llms_emp_stm_results_0001` | 删除反馈失败路径 | `not_better` | `in_scope_t0_protocol_case` | semantic_deletion |
| C08 | `llms_emp_stm_results_0004` | 正确结构化 action/effect | `better` | `in_scope_t0_protocol_case` | action_effect |
| C09 | `llms_emp_stm_results_0004` | 删除动作效果 | `not_better` | `in_scope_t0_protocol_case` | semantic_deletion, action_effect |
| C10 | `llms_emp_stm_results_0004` | 格式变化但 action 证据不足 | `unknown` | `in_scope_t0_protocol_case` | evidence_insufficient |
| C11 | `llms_emp_stm_results_0039` | 复杂 guard 结构化 | `better` | `in_scope_t0_protocol_case` | guard_action_event_folding |
| C12 | `llms_emp_stm_results_0039` | 变量重命名导致 trace loss | `unknown` | `in_scope_t0_protocol_case` | trace_loss |
| C13 | `llms_emp_stm_results_0039` | 新增无证据自动退出 | `not_better` | `in_scope_t0_protocol_case` | over_repair |
| C14 | `llms_emp_stm_results_0045` | T0.5 timer cue 降级为 counter caveat | `partial` | `caveat_t05` | time_caveat |
| C15 | `llms_emp_stm_results_0045` | timed automata 能力外推 | `protocol_or_provenance_invalid` | `caveat_t05` | timed_automata_overclaim, conversion_laundering |
| C16 | `llms_emp_stm_results_0018` | T1 stress 不进入 headline | `stress_t1` | `out_of_headline_stress_t1` | scope_boundary |
| C17 | `llms_emp_stm_results_0000` | 候选自身 parse/schema invalid | `stmk_repair_failure` | `in_scope_t0_protocol_case` | candidate_invalid |
| C18 | `llms_emp_stm_results_0000` | 缺少 ledger/hash/evidence | `protocol_or_provenance_invalid` | `in_scope_t0_protocol_case` | missing_provenance |
| C19 | `llms_emp_stm_results_0039` | 只修一部分 complex guard | `partial` | `in_scope_t0_protocol_case` | under_repair, guard_action_event_folding |
| C20 | `llms_emp_stm_results_0000` | 文本更像但语义删除 | `not_better` | `in_scope_t0_protocol_case` | textual_similarity_misuse, semantic_deletion, guard_action_event_folding |

## 5. baseline preflight 结论

- 0000 / 0045 复用 R4.5 selected smoke `.fcstm`；0001 / 0018 复用 R5.7.4 standalone materialized baseline；0039 复用 selected smoke fallback；这些都只是内部实验介质 `[src-preflight]`。
- 0004 没有已提交 standalone `.fcstm`，本轮新增手工 materialized protocol baseline，只用于 action-effect 裁决协议 dry-run，不是 conversion 输出，也不是 repair gain `[clm-baseline]`。
- 0009 没有已提交 standalone `.fcstm`，本轮按 PR body 允许路径改用同 cluster 09 的 selected smoke `0039` fallback，报告时必须说清不是 0009-specific 真实修复 `[clm-baseline]`。

## 6. 学术风险与禁止主张

| 风险 | 本轮处理 | 禁止主张 |
|---|---|---|
| constructed candidate 被误当真实输出 | suite 与 case-level JSON 顶层固定 `constructed_for_protocol_dry_run=true`、`real_repair_run_id=null` | 禁止报告 repair effectiveness / success rate |
| `.fcstm`/pyfcstm 被误当贡献 | prompt、schema、README、report 均声明内部介质 | 禁止把 DSL/转换器写作贡献 |
| conversion laundering | C04/C15/C18 覆盖 protocol invalid | 禁止把 parse / normalization / lowering 写成 repair gain |
| metric gaming | C20 覆盖 textual similarity misuse | 禁止 metric-only Better verdict |
| scenario overfitting | 本轮不覆盖，handoff 给 R7 | 禁止声称 anti-gaming 已完整覆盖 |
| T0.5/T1 外推 | C14/C15/C16 仅 caveat/stress | 禁止进入 T0 headline success |

注：anti-gaming risk flags 允许一个 case 标记主风险与次级风险，因此本轮实际风险标注是 PR body 最小覆盖表的超集；coverage claim 只能按 `primary_expected_verdict` 与 `protocol_coverage_claim_allowed=true` 使用，不能把次级风险标记扩展为真实 repair 发现。

## 7. 后续入口

R7 scenario-ledger 必须补 `scenario_overfitting` 反例，并用真实 scenario oracle / trace 支撑。R6/R7 真实 repair loop 输出必须重新生成 run record、change ledger、target ledger、prompt/raw output/usage（若调用 LLM）和 eligibility；不得复用本轮 constructed expected verdict 作为结果。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | 当前 PR 提交 | R5.7.5 首次新增 constructed `STM_k` coverage dry-run report | — | [suite_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json) |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-suite] | suite_index | [suite_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json) | json | 20 case、outcome、eligibility、coverage summary | `$.cases[*]`, `$.coverage_summary` |
| [src-preflight] | baseline_preflight | [baseline_preflight.json](../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/baseline_preflight.json) | json | baseline 来源、0004 manual、0009->0039 fallback | `$.items[*]`, `$.fallbacks[*]` |
| [src-protocol] | prompt_schema | [better_adjudication_prompt_v0.md](../experiment_design/protocols/better_adjudication_prompt_v0.md)、[better_adjudication_output_schema_v0.json](../experiment_design/protocols/better_adjudication_output_schema_v0.json) | md/json | 裁决 prompt 与输出 schema | fail-closed checks、required fields |
| [src-r574] | r5_7_4_report | [2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md](./2026-07-03-23-44-12-r5-7-4-static-adjudication-dry-run.md) | md | R5.7.4 handoff 与 baseline 风险 | R5.7.5 handoff 段落 |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-boundary] | R5.7.5-C1 | R5.7.5 constructed cases 不支持 repair effectiveness 或 headline success。 | prohibition | [src-suite] `headline_eligible=false`, `repair_effectiveness_eligible=false`, `real_repair_run_id=null` | [cmd-json] | high | 后续真实 R7/R8 run 可另行计算。 |
| [clm-suite] | R5.7.5-C2 | 本轮覆盖 20 个 case 与 7 类 `primary_expected_verdict`，并由 C14/C15 覆盖 `caveat_t05` scope route。 | count/classification | [src-suite] `case_count=20`, `coverage_summary.outcomes` | [cmd-json] | high | expected verdict 不是观察到的真实结果。 |
| [clm-anti-gaming] | R5.7.5-C3 | 本轮覆盖多类 anti-gaming 风险，但 scenario overfitting 仅 handoff。 | risk | [src-suite] `cases[*].risks`, `coverage_summary.scenario_overfitting` | [cmd-json] | high | scenario overfitting 必须由 R7 scenario oracle 补齐。 |
| [clm-baseline] | R5.7.5-C4 | 0004 manual baseline 与 0039 fallback 均有 caveat，不能外推为真实 repair output。 | caveat | [src-preflight] `items[pair_key=0004]`, `fallbacks[requested_pair_id=0009]` | [cmd-json] | high | 不影响 protocol coverage，但限制 pair-specific 结论。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 目的 |
|---|---|---|
| [cmd-json] | 见下方可复制命令。 | 复验 JSON 可读、20 case、eligibility false、baseline pointer/preflight hash、schema negative guard、C17 parse-invalid 预期。 |


#### [cmd-json] 可复制复验命令

```bash
python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --parse
```
