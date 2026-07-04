# R5.7.5 full blind adjudication dry-run 报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与回答的问题

本报告补充在 R5.7.5 constructed answer-key suite 之后，回答一个此前不能由 answer-key fixture 证明的问题：在 judge **看不到 expected verdict、Cxx 构造意图、oracle mapping、PR 讨论上下文** 的情况下，仅给出 `NL + raw STM_0 + canonical STM_0 + candidate STM_k + neutral mechanical/provenance facts`，是否能按 R5.7.1--R5.7.4 的 G0--G6 评价链完成 blind Better STM 裁决 `[clm-blind-purpose]`。

本报告仍然不是 repair effectiveness 报告：20 个 `STM_k` 均为 constructed protocol cases，不是真实 repair loop 输出；全部 `headline_eligible=false`、`repair_effectiveness_eligible=false`、`real_repair_run_id=null` `[clm-boundary]`。

## 2. blind 隔离纪律

| 环节 | 本轮做法 | 证据 |
|---|---|---|
| judge 输入 | `blind_inputs/Bxx/` 只含 `input_packet.json`、`nl.txt`、`raw_stm0.plantuml`、`canonical_stm0.fcstm`、`candidate_stmk.fcstm`；不含 expected verdict / Cxx slug / answer key。 | [src-blind-index], [cmd-leakage] |
| hidden oracle | `oracle_answer_key.json` 只给 scorer 使用，不进入 prompt。 | [src-oracle] |
| 上下文隔离 | 每个 case 由 `run_blind_judge.py` 调用 `codex-deepseek exec --ephemeral --sandbox read-only`，逐 case 重新启动，不继承本会话上下文。 | [src-runner], [src-manifest] |
| 全过程存档 | 每个 Bxx 均保存 `prompt.txt`、`raw_output.txt`、`combined_output_for_parse.txt`、`parsed_output.json`、`stdout.txt`、`stderr.txt`、`run_meta_start.json`、`run_meta_end.json`。 | [src-outputs], [src-manifest] |
| 结构化评分 | `score_blind_outputs.py` 只在输出 JSON schema-valid 时计算 verdict/scope/run-validity match。 | [src-score], [cmd-score] |

## 3. 最终全量 dry-run 结果

最终全量运行时间窗口：`2026-07-05T06:56:17` 到 `2026-07-05T07:18:31`；judge 为 `deepseek-blind-judge`。结果：

| 指标 | 数值 |
|---|---:|
| case_count | 20 |
| valid_output_count | 20 |
| verdict_match_count | 20 |
| scope_match_count | 20 |
| run_validity_match_count | 20 |
| leakage_detected_count | 0 |

结论：20/20 输出 schema-valid，20/20 primary verdict 与 hidden oracle 一致，20/20 scope routing 一致，20/20 run validity 一致，0 个输出报告泄露 `[clm-final-score]`。

## 4. expected verdict 覆盖

| expected verdict | 数量 |
|---|---:|
| `better` | 2 |
| `not_better` | 8 |
| `partial` | 3 |
| `protocol_or_provenance_invalid` | 3 |
| `stmk_repair_failure` | 1 |
| `stress_t1` | 1 |
| `unknown` | 2 |

这组分布覆盖了 R5.7.5 需要压力测试的主要分支：正向 strict improvement、not better、partial / under-repair、unknown / evidence-insufficient、candidate failure、protocol/provenance invalid、T0.5 caveat 与 T1 stress `[clm-branch-coverage]`。

## 5. 20 case blind 对照表

| blind | source | base pair | expected | observed | verdict | expected scope | observed scope | scope | confidence |
|---|---|---|---|---|---|---|---|---|---|
| B01 | C08 | `llms_emp_stm_results_0004` | `partial` | `partial` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` |
| B02 | C10 | `llms_emp_stm_results_0004` | `unknown` | `unknown` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` |
| B03 | C02 | `llms_emp_stm_results_0000` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B04 | C09 | `llms_emp_stm_results_0004` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B05 | C05 | `llms_emp_stm_results_0001` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B06 | C01 | `llms_emp_stm_results_0000` | `better` | `better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B07 | C04 | `llms_emp_stm_results_0000` | `protocol_or_provenance_invalid` | `protocol_or_provenance_invalid` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B08 | C19 | `llms_emp_stm_results_0039` | `partial` | `partial` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` |
| B09 | C11 | `llms_emp_stm_results_0039` | `better` | `better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B10 | C03 | `llms_emp_stm_results_0000` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B11 | C12 | `llms_emp_stm_results_0039` | `unknown` | `unknown` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` |
| B12 | C18 | `llms_emp_stm_results_0000` | `protocol_or_provenance_invalid` | `protocol_or_provenance_invalid` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B13 | C17 | `llms_emp_stm_results_0000` | `stmk_repair_failure` | `stmk_repair_failure` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B14 | C13 | `llms_emp_stm_results_0039` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B15 | C15 | `llms_emp_stm_results_0045` | `protocol_or_provenance_invalid` | `protocol_or_provenance_invalid` | ✅ | `caveat_t05` | `caveat_t05` | ✅ | `high` |
| B16 | C06 | `llms_emp_stm_results_0001` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B17 | C14 | `llms_emp_stm_results_0045` | `partial` | `partial` | ✅ | `caveat_t05` | `caveat_t05` | ✅ | `medium` |
| B18 | C20 | `llms_emp_stm_results_0000` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B19 | C07 | `llms_emp_stm_results_0001` | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` |
| B20 | C16 | `llms_emp_stm_results_0018` | `stress_t1` | `stress_t1` | ✅ | `out_of_headline_stress_t1` | `out_of_headline_stress_t1` | ✅ | `high` |

## 6. 本轮 blind run 反向校准出的关键规则

| 校准点 | 触发 case | 最终处理 | 学术理由 |
|---|---|---|---|
| partial 不是失败，而是“有局部严格收益但目标族未闭合”。 | C08/B01、C14/B17、C19/B08 | oracle 统一校准为 `partial`。 | 若候选改善 action/effect 或 guard/counter explicitness，但仍留下 NL 支持的同类缺口，则不能写 strict better，也不能等同 not_better。 |
| 证据不足时使用 `unknown`，而不是强行 not_better。 | C10/B02、C12/B11 | `semantic_evidence_status=insufficient_*` 且无清晰回归时输出 `unknown`。 | 避免把 traceability 不足误判成语义回归；也避免把不可证的格式化收益写成 better。 |
| T0.5 counter caveat 不能自动变成 strict better。 | C14/B17、C15/B15 | C14 为 `partial+caveat_t05`；C15 因额外 timed-automata 能力外推为 `protocol_or_provenance_invalid+caveat_t05`。 | 用户已决策 T0.5 可以离散 counter 降级，但缺 counter lifecycle 证据时只能作为 caveat / partial，不支撑 headline success。 |
| schema invalid 不能被 verdict 文本“看起来对”掩盖。 | B04 早期试跑 | scorer 已改成 schema-valid 才计 match；prompt 明确 gate object 不得加 schema 外字段。 | 学术审计中 schema-invalid 输出不能进入主统计。 |

## 7. 限制与禁止外推

1. 本轮证明的是 **blind adjudication protocol 可执行性与分支覆盖**，不是 repair method effectiveness `[clm-boundary]`。
2. 当前最终全量 judge 使用 DeepSeek-backed `codex-deepseek exec` 一个 judge family；后续若要把 LLM-as-Judge 本身写进论文，需要 R7/R8 另做多 judge、一致性、随机性和人工仲裁实验 `[clm-limitation]`。
3. `.fcstm`、`pyfcstm`、PlantUML canonicalization 仍只是实验内部介质；不得作为贡献或 repair gain `[clm-boundary]`。
4. score 20/20 是对 hidden oracle 的一致性，不等于 oracle 绝对正确；本轮已经展示 oracle 会被 blind dry-run 反向校准，后续规则修订必须继续保留 dry-run 证据 `[clm-calibration]`。

## 8. 后续 handoff

- R5.7.5 可以把 `better_adjudication_blind_prompt_v0.md`、`better_adjudication_blind_output_schema_v0.json`、blind input bundle、oracle/scorer/run manifest 作为 R6/R7 评价协议输入。
- R6/R7 若进入真实 repair loop，必须重新生成真实 `AgentLoopRunRecord` / change ledger / target ledger / prompt raw output / usage；不得复用本轮 constructed `STM_k` 作为真实结果。
- R7 若扩展 judge，应优先补：多 judge blind repeat、人工仲裁样例、scenario-overfitting 反例、LLM nondeterminism 统计。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | 当前 PR 提交 | R5.7.5 追加 full blind adjudication dry-run 后冻结最终 score、oracle 校准与 handoff。 | — | [score_summary.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/deepseek-blind-judge/score_summary.json) |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-suite] | constructed_suite | [suite_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json) | json | 20 个 constructed source case、expected branch、eligibility boundary | `$.cases[*]`, `$.coverage_summary` |
| [src-blind-index] | blind_input_index | [blind_input_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/blind_input_index.json) | json | Bxx blind input 入口，不含 hidden oracle | `$.cases[*]` |
| [src-oracle] | oracle_answer_key | [oracle_answer_key.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/oracle_answer_key.json) | json | scorer 使用的 hidden oracle，不进入 judge prompt | `$.cases[*]` |
| [src-prompt] | blind_prompt | [better_adjudication_blind_prompt_v0.md](../experiment_design/protocols/better_adjudication_blind_prompt_v0.md) | md | blind judge 裁决 prompt 与 fail-closed 规则 | §2、§2.2、§5 |
| [src-schema] | blind_schema | [better_adjudication_blind_output_schema_v0.json](../experiment_design/protocols/better_adjudication_blind_output_schema_v0.json) | json | blind output JSON schema | required fields, enum |
| [src-runner] | run_blind_judge | [run_blind_judge.py](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/run_blind_judge.py) | py | 逐 case 构造 prompt、调用 isolated judge、写盘全过程 | `build_prompt`, `subprocess.run` |
| [src-score] | score_summary | [score_summary.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/deepseek-blind-judge/score_summary.json) | json | 最终 20 case blind score | top-level counts, `rows[*]` |
| [src-manifest] | final_run_manifest | [final_run_manifest.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/deepseek-blind-judge/final_run_manifest.json) | json | final run 起止时间、每 case prompt/raw/parsed/meta 路径 | `cases[*]` |
| [src-outputs] | judge_outputs | [deepseek-blind-judge/](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/deepseek-blind-judge) | directory | 每 case prompt/raw/parsed/stdout/stderr/run meta | `Bxx/*` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-blind-purpose] | R5.7.5-B1 | 本报告验证的是 blind adjudication protocol，而不是 answer-key fixture 自检。 | scope | [src-blind-index], [src-runner] | [cmd-final-run] | high | 只覆盖 constructed cases。 |
| [clm-boundary] | R5.7.5-B2 | 全部 case 禁止计入 headline success 或 repair effectiveness。 | prohibition | [src-suite] case-level eligibility false；[src-prompt] 固定输出 eligibility false | [cmd-validate-constructed] | high | 真实 repair loop 可另建结果。 |
| [clm-final-score] | R5.7.5-B3 | 最终 DeepSeek full blind run 达成 20/20 schema-valid、20/20 verdict match、20/20 scope match、20/20 run validity match、0 leakage。 | result | [src-score] top-level counts | [cmd-score] | high | 仅一个 judge family。 |
| [clm-branch-coverage] | R5.7.5-B4 | 本轮覆盖 better/not_better/partial/unknown/failure/protocol invalid/stress 与 T0.5 caveat。 | coverage | [src-suite] coverage summary；[src-score] rows | [cmd-score] | high | scenario-overfitting 仍 handoff。 |
| [clm-calibration] | R5.7.5-B5 | blind dry-run 反向校准了 C08/C12/C14/C19 与 prompt/scorer 纪律。 | design finding | [src-score] rows；[src-prompt] fail-closed rules；[src-suite] current expected verdict | [cmd-score] | medium | 历史中间 runs 未作为最终统计，只作为设计修订动因。 |
| [clm-limitation] | R5.7.5-B6 | 单 judge 20/20 不能证明 LLM-as-Judge 方法学充分可靠。 | limitation | [src-runner] judge=`deepseek`；[src-score] judge field | [cmd-score] | high | R7/R8 需多 judge / 人工仲裁。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 目的 |
|---|---|---|
| [cmd-validate-constructed] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --parse` | 验证 constructed suite 结构、hash、schema 与 C17 parse-invalid 预期。 |
| [cmd-build] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_blind_bundle.py` | 从 constructed suite 刷新 blind inputs 与 hidden oracle。 |
| [cmd-leakage] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/leakage_check.py` | 检查 blind inputs 不含 expected verdict / oracle / Cxx slug。 |
| [cmd-final-run] | `source .env && for i in $(seq -w 1 20); do python "$BASE/run_blind_judge.py" --judge deepseek --case "B$i" --timeout 900; done` | 执行 20 case final blind judge。完整命令见 PR comment；运行结果已在 [src-manifest] 存档。 |
| [cmd-score] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge deepseek-blind-judge` | 复算 score summary。 |
