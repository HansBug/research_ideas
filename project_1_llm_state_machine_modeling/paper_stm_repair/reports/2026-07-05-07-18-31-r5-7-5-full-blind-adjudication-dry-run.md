# R5.7.5 full blind adjudication dry-run 报告

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排。

## 1. 定位与回答的问题

本报告补充在 R5.7.5 constructed answer-key suite 之后，回答一个此前不能由 answer-key fixture 证明的问题：在 judge **看不到 expected verdict、Cxx 构造意图、oracle mapping、PR 讨论上下文** 的情况下，仅给出 `NL + raw STM_0 + canonical STM_0 + candidate STM_k + neutral mechanical/provenance facts`，是否能按 R5.7.1--R5.7.4 的 E0--E11 / G0--G6 评价链完成 blind Better STM 裁决 `[clm-blind-purpose]`。

本报告仍然不是 repair effectiveness 报告：20 个 `STM_k` 均为 constructed protocol cases，不是真实 repair loop 输出；全部 `headline_eligible=false`、`repair_effectiveness_eligible=false`、`real_repair_run_id=null` `[clm-boundary]`。

## 2. blind 隔离纪律

| 环节 | 本轮做法 | 证据 |
|---|---|---|
| judge 输入 | `blind_inputs/Bxx/` 只含 `input_packet.json`、`nl.txt`、`raw_stm0.plantuml`、`canonical_stm0.fcstm`、`candidate_stmk.fcstm`；不含 expected verdict / Cxx slug / answer key。 | [src-blind-index], [cmd-leakage] |
| hidden oracle | `oracle_answer_key.json` 只给 scorer 使用，不进入 prompt。 | [src-oracle] |
| 上下文隔离 | 每个 case 由 `run_blind_judge.py` 调用 `claude -p --no-session-persistence --bare --model sonnet --json-schema ...`，并在仓库外临时目录运行；运行目录只包含 `prompt.txt` 和 `output_schema.json`。 | [src-runner], [src-manifest] |
| 全过程存档 | 每个 Bxx 均保存 `prompt.txt`、`raw_output.txt`、`combined_output_for_parse.txt`、`parsed_output.json`、`stdout.txt`、`stderr.txt`、`run_meta_start.json`、`run_meta_end.json`。 | [src-outputs], [src-manifest] |
| prompt 一致性 | final scoring 前重建 20 个 prompt 并与归档 prompt 比对，`mismatch_count=0`。 | [src-prompt-check], [cmd-prompt-check] |
| 结构化评分 | `score_blind_outputs.py` 只在 `exit_code=0`、schema-valid、identity 匹配且无 provider/CLI nonzero parsed-output 时计入 final score。 | [src-score-script], [cmd-score] |

## 3. 最终全量 dry-run 结果

最终全量运行窗口：`2026-07-05T14:40:09` 到 `2026-07-05T14:54:39`；final judge family 为 `claude-blind-judge`。本轮 B01--B20 均由隔离外部 CLI 子进程执行；其中 B18 在 C20 反例被加硬为“明显删除 NL 支持的 Power_Off / human fallback”后重新运行，最终 `prompt_consistency_check` 证明 20/20 归档 prompt 与当前 bundle 完全一致 `[clm-prompt-consistency]`。

| 指标 | 数值 |
|---|---:|
| case_count | 20 |
| valid_output_count | 20 |
| verdict_match_count | 20 |
| scope_match_count | 20 |
| run_validity_match_count | 20 |
| gate_all_match_count | 6 |
| gate_disagreement_count | 25 |
| leakage_detected_count | 0 |

结论：20/20 输出 schema-valid，20/20 primary verdict 与 hidden oracle 一致，20/20 scope routing 一致，20/20 run validity 一致，0 个输出报告泄露；gate-level 只有 6/20 完全一致，因此 gate-level disagreement 应保留为 calibration evidence，而不是被“洗”成主结论 `[clm-final-score]`。

## 4. expected verdict 覆盖

| expected verdict | 数量 |
|---|---:|
| `better` | 2 |
| `not_better` | 12 |
| `partial` | 2 |
| `unknown` | 1 |
| `protocol_or_provenance_invalid` | 1 |
| `stmk_repair_failure` | 1 |
| `stress_t1` | 1 |

这组分布覆盖 R5.7.5 需要压力测试的主要分支：strict improvement、not better、partial / under-repair、unknown / evidence-insufficient、candidate failure、protocol/provenance invalid、T0.5 caveat 与 T1 stress `[clm-branch-coverage]`。

## 5. 20 case blind 对照表

`verdict` / `scope` 列中 ✅ 表示 observed 与 hidden oracle 一致；人工升级列中 ✅ 表示本次 judge 未要求 human escalation，⚠️ 表示 judge 自身认为需要升级。

| blind | source | expected | observed | verdict | expected scope | observed scope | scope | confidence | no human escalation | gate disagreements |
|---|---|---|---|---|---|---|---|---|---|---:|
| B01 | C08 | `partial` | `partial` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` | ✅ | 2 |
| B02 | C10 | `unknown` | `unknown` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `low` | ⚠️ | 2 |
| B03 | C02 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B04 | C09 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 0 |
| B05 | C05 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 0 |
| B06 | C01 | `better` | `better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 0 |
| B07 | C04 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B08 | C19 | `partial` | `partial` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` | ✅ | 2 |
| B09 | C11 | `better` | `better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` | ✅ | 0 |
| B10 | C03 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B11 | C12 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 0 |
| B12 | C18 | `protocol_or_provenance_invalid` | `protocol_or_provenance_invalid` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `medium` | ⚠️ | 3 |
| B13 | C17 | `stmk_repair_failure` | `stmk_repair_failure` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 4 |
| B14 | C13 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 2 |
| B15 | C15 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B16 | C06 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B17 | C14 | `not_better` | `not_better` | ✅ | `caveat_t05` | `caveat_t05` | ✅ | `medium` | ✅ | 1 |
| B18 | C20 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 0 |
| B19 | C07 | `not_better` | `not_better` | ✅ | `in_scope_t0_protocol_case` | `in_scope_t0_protocol_case` | ✅ | `high` | ✅ | 1 |
| B20 | C16 | `stress_t1` | `stress_t1` | ✅ | `out_of_headline_stress_t1` | `out_of_headline_stress_t1` | ✅ | `high` | ✅ | 3 |

## 6. gate-level calibration 结果

primary verdict / scope / run-validity 已 20/20 对齐，但 G0--G6 的细粒度状态仍存在 25 处 disagreement。该结果说明：当前 prompt 足以支撑主裁决流程，但 gate-level schema 与 oracle 粒度仍需要在 R6/R7 前继续校准，尤其是 `not_evaluated` vs `unknown`、`partial` vs `pass`、以及 T0.5/T1 scope gate 的状态编码 `[clm-gate-calibration]`。

| gate | status match |
|---|---:|
| G0 | 18 / 20 |
| G1 | 20 / 20 |
| G2 | 14 / 20 |
| G3 | 16 / 20 |
| G4 | 11 / 20 |
| G5 | 16 / 20 |
| G6 | 20 / 20 |

| blind | source | gate disagreements |
|---|---|---|
| B01 | C08 | G4: `pass`→`partial`; G5: `pass`→`partial` |
| B02 | C10 | G2: `pass`→`partial`; G3: `unknown`→`pass` |
| B03 | C02 | G2: `fail`→`pass` |
| B07 | C04 | G2: `pass`→`fail` |
| B08 | C19 | G4: `pass`→`partial`; G5: `pass`→`partial` |
| B10 | C03 | G4: `pass`→`partial` |
| B12 | C18 | G3: `not_evaluated`→`unknown`; G4: `not_evaluated`→`unknown`; G5: `not_evaluated`→`unknown` |
| B13 | C17 | G2: `not_evaluated`→`not_applicable`; G3: `not_evaluated`→`fail`; G4: `not_evaluated`→`fail`; G5: `not_evaluated`→`fail` |
| B14 | C13 | G2: `fail`→`pass`; G4: `not_applicable`→`fail` |
| B15 | C15 | G2: `pass`→`fail` |
| B16 | C06 | G4: `not_applicable`→`fail` |
| B17 | C14 | G0: `caveat`→`pass` |
| B19 | C07 | G4: `not_applicable`→`fail` |
| B20 | C16 | G0: `out_of_headline`→`fail`; G3: `not_applicable`→`pass`; G4: `not_applicable`→`fail` |

## 7. 本轮 blind run 反向校准出的关键规则

| 校准点 | 触发 case | 最终处理 | 学术理由 |
|---|---|---|---|
| 不透明 `effect_token_*` 不得被当作 action/effect improvement。 | C10/B02 | prompt 加硬：无语义变量且无 trace map 时，若 readable label / topology 未删，应输出 `unknown`，不能因“看起来增加了 effect block”输出 `partial`。 | 避免 LLM judge 把形式化 instrumentation 误当语义修复。 |
| text-similarity 反例必须是 cue-free 但语义删除明确。 | C20/B18 | candidate 加硬为删除 NL 支持的 `Power_Off` final behavior 与 human steering/brake fallback。 | 如果反例只删除 ambiguous transition，blind judge 会合理地判为 partial/better；反例必须服务于真实 anti-gaming 风险而非人为陷阱。 |
| partial 是“有局部严格收益但同族目标未闭合”，不是失败。 | C08/B01、C19/B08 | 保留 `partial`，不强行改成 better 或 not_better。 | action/effect 或 guard 有局部收益，但同族 entry/do action 或重复 guard pattern 没闭合。 |
| gate-level 不追求 20/20 人工抹平。 | 多 case | final report 保留 25 个 gate disagreement。 | primary verdict 是当前 R5.7.5 的核心验收；gate disagreement 是后续 prompt/schema/oracle calibration evidence。 |
| schema-invalid / provider-invalid 不进入主统计。 | runner/scorer | scorer 只有合法 JSON、schema-valid、identity match、exit_code=0 时 eligible。 | 学术审计中不能把“看起来答对”的无效输出计入主结果。 |

## 8. 限制与禁止外推

1. 本轮证明的是 **blind adjudication protocol 可执行性、分支覆盖与校准价值**，不是 repair method effectiveness `[clm-boundary]`。
2. 当前 final eligible run 只使用一个 judge family（`claude-blind-judge`）。如果后续论文要把 LLM-as-Judge 本身作为方法学证据，需要 R7/R8 另做多 judge、一致性、随机性和人工仲裁实验 `[clm-limitation]`。
3. `.fcstm`、`pyfcstm`、PlantUML canonicalization 仍只是实验内部介质；不得作为贡献或 repair gain `[clm-boundary]`。
4. 20/20 是对 hidden oracle 的一致性，不等于 oracle 绝对正确；本轮 C10/C20 的校准正说明 oracle / prompt / fixture 必须经 blind dry-run 反向审计 `[clm-calibration]`。

## 9. 后续 handoff

- R5.7.5 可以把 `better_adjudication_blind_prompt_v0.md`、`better_adjudication_blind_output_schema_v0.json`、blind input bundle、oracle/scorer/run manifest 作为 R6/R7 评价协议输入。
- R6/R7 若进入真实 repair loop，必须重新生成真实 `AgentLoopRunRecord` / change ledger / target ledger / prompt raw output / usage；不得复用本轮 constructed `STM_k` 作为真实结果。
- R7 若扩展 judge，应优先补：多 judge blind repeat、人工仲裁样例、scenario-overfitting 反例、LLM nondeterminism 统计、gate-level status calibration。

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| 本文件 | 当前 PR 提交 | 当前 PR 提交 | R5.7.5 追加 full blind adjudication dry-run 后冻结 final Claude score、oracle/prompt/case 校准与 R6/R7 handoff。 | — | [score_summary.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/claude-blind-judge/score_summary.json) |

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-suite] | constructed_suite | [suite_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/suite_index.json) | json | 20 个 constructed source case、expected branch、eligibility boundary | `$.cases[*]`, `$.coverage_summary` |
| [src-blind-index] | blind_input_index | [blind_input_index.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/blind_input_index.json) | json | Bxx blind input 入口，不含 hidden oracle | `$.cases[*]` |
| [src-oracle] | oracle_answer_key | [oracle_answer_key.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/oracle_answer_key.json) | json | scorer 使用的 hidden oracle，不进入 judge prompt | `$.cases[*]` |
| [src-prompt] | blind_prompt | [better_adjudication_blind_prompt_v0.md](../experiment_design/protocols/better_adjudication_blind_prompt_v0.md) | md | blind judge 裁决 prompt 与 fail-closed 规则 | §2、§2.2、§5 |
| [src-schema] | blind_schema | [better_adjudication_blind_output_schema_v0.json](../experiment_design/protocols/better_adjudication_blind_output_schema_v0.json) | json | blind output JSON schema | required fields, enum |
| [src-runner] | run_blind_judge | [run_blind_judge.py](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/run_blind_judge.py) | py | 逐 case 构造 prompt、调用 isolated judge、写盘全过程 | `build_prompt`, `subprocess.run` |
| [src-score-script] | score_blind_outputs | [score_blind_outputs.py](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py) | py | schema-valid / identity / provider status / oracle match 评分 | `score_row`, `eligible_output` |
| [src-score] | score_summary | [score_summary.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/claude-blind-judge/score_summary.json) | json | final 20 case blind score | top-level counts, `rows[*]` |
| [src-manifest] | final_run_manifest | [final_run_manifest.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/claude-blind-judge/final_run_manifest.json) | json | final run 起止时间、每 case prompt/raw/parsed/meta 路径 | `cases[*]` |
| [src-outputs] | judge_outputs | [claude-blind-judge/](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/claude-blind-judge) | directory | 每 case prompt/raw/parsed/stdout/stderr/run meta | `Bxx/*` |
| [src-prompt-check] | prompt_consistency | [prompt_consistency_check.stdout.json](../pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/judge_outputs/claude-blind-judge/prompt_consistency_check.stdout.json) | json | 20 case 归档 prompt 与当前 bundle 一致性检查 | `mismatch_count=0` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-blind-purpose] | R5.7.5-B1 | 本报告验证的是 blind adjudication protocol，而不是 answer-key fixture 自检。 | scope | [src-blind-index], [src-runner] | [cmd-final-run] | high | 只覆盖 constructed cases。 |
| [clm-boundary] | R5.7.5-B2 | 全部 case 禁止计入 headline success 或 repair effectiveness。 | prohibition | [src-suite] case-level eligibility false；[src-prompt] 固定输出 eligibility false | [cmd-validate-constructed] | high | 真实 repair loop 可另建结果。 |
| [clm-final-score] | R5.7.5-B3 | final Claude full blind run 达成 20/20 schema-valid、20/20 verdict match、20/20 scope match、20/20 run validity match、0 leakage。 | result | [src-score] top-level counts | [cmd-score] | high | 单 judge family；gate-level 仍有 25 处 disagreement。 |
| [clm-branch-coverage] | R5.7.5-B4 | 本轮覆盖 better/not_better/partial/unknown/failure/protocol invalid/stress 与 T0.5 caveat。 | coverage | [src-suite] coverage summary；[src-score] rows | [cmd-score] | high | scenario-overfitting 仍 handoff。 |
| [clm-calibration] | R5.7.5-B5 | blind dry-run 反向校准了 C10/C20 fixture 与 prompt/scorer 纪律。 | design finding | [src-score] rows；[src-prompt] fail-closed rules；[src-suite] current expected verdict | [cmd-score] | medium | 历史中间 runs 未作为最终统计，只作为设计修订动因。 |
| [clm-gate-calibration] | R5.7.5-B6 | 主 verdict 已稳定，但 gate-level status 仍需 R6/R7 校准。 | limitation / handoff | [src-score] `gate_status_match_counts`, `gate_disagreement_count` | [cmd-score] | high | 不阻塞 R5.7.5；不能把 gate-level 写成 20/20。 |
| [clm-prompt-consistency] | R5.7.5-B7 | final archived prompts 与当前 prompt template / blind inputs 一致，未使用 stale prompt。 | audit | [src-prompt-check] `mismatch_count=0` | [cmd-prompt-check] | high | 只能证明 prompt bytes 一致，不证明 judge 无随机性。 |
| [clm-limitation] | R5.7.5-B8 | 单 judge 20/20 不能证明 LLM-as-Judge 方法学充分可靠。 | limitation | [src-runner] judge=`claude`；[src-score] judge field | [cmd-score] | high | R7/R8 需多 judge / 人工仲裁。 |

### A.4 复验命令

| 编号 / 引用键 | 命令 | 目的 |
|---|---|---|
| [cmd-validate-constructed] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_constructed_stmk/validate_suite.py --parse` | 验证 constructed suite 结构、hash、schema 与 C17 parse-invalid 预期。 |
| [cmd-build] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_blind_bundle.py` | 从 constructed suite 刷新 blind inputs 与 hidden oracle。 |
| [cmd-leakage] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/leakage_check.py` | 检查 blind inputs 不含 expected verdict / oracle / Cxx slug。 |
| [cmd-final-run] | `source .env && for i in $(seq -w 1 20); do python "$BASE/run_blind_judge.py" --judge claude --case "B$i" --timeout 900; done` | 执行 20 case isolated Claude blind judge；每 case prompt/raw/parsed/meta 写盘。 |
| [cmd-score] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/score_blind_outputs.py --judge claude-blind-judge --require-all-valid --require-all-core-match --require-no-leakage` | 复算 score summary 并要求 all valid / core match / no leakage。 |
| [cmd-manifest] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/build_final_run_manifest.py --judge claude-blind-judge` | 生成 final run manifest。 |
| [cmd-prompt-check] | `python project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/evaluation/dry_run_examples/r5_7_5_blind_adjudication/prompt_consistency_check.py --judge claude-blind-judge` | 检查 final archived prompts 与当前 bundle/template 一致。 |
