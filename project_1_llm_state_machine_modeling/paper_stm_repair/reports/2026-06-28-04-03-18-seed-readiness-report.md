# R5 seed library readiness report

## 事实源与复验 / 来源考据

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/seed_sweep/sweep_summary.md` | `6e1d8b51` (2026-06-28 03:10:11 +0800, R5 seed sweep 初始生成) | `73af4d83` (2026-06-28 15:05:25 +0800, `refactor(paper1-r5): 将阶段链路迁入pipeline路径`) | `185aa02c` (2026-06-28 04:03:18 +0800)：补齐复验入口与抽样展示；`5d0a2a01` 已先修正证据链，`bbd974c1` 只追加主 seed 方向链接，不改变 readiness denominator。 | 本报告所在的 R5.5.1 migration commit（同一提交内无法自嵌最终 SHA；精确提交用 `git log --follow -- <report>` 复核）；仅迁移 human-facing report 与改写入口，不改 canonical machine facts。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)；[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)；[archive_manifest.json](../pipeline/readiness_audit/artifact_archives/archive_manifest.json) |
| `pipeline/readiness_audit/seed_sweep/sampling_analysis.md`、`blocked_cases.md`、`partial_cases.md` | `6e1d8b51` / `5d0a2a01`（R5 sweep 衍生展示文件创建与证据链修正） | `73af4d83` (2026-06-28 15:05:25 +0800, `refactor(paper1-r5): 将阶段链路迁入pipeline路径`) | `185aa02c`：抽样展示成为可复验 readiness report 的稳定 human-facing 入口；blocked/partial 表仅是机器索引的阅读切片。 | 本报告所在的 R5.5.1 migration commit（同一提交内无法自嵌最终 SHA；精确提交用 `git log --follow -- <report>` 复核）；仅迁移 human-facing report 与改写入口，不改 canonical machine facts。 | [sweep archive](../pipeline/readiness_audit/artifact_archives/archives/)；[audit records](../pipeline/readiness_audit/seed_sweep/audit_records/)；[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

## 迁移说明

本 report 汇总 R5 seed library readiness 的 human-facing 入口：全量 entry/pair 摘要、状态抽样、blocked 全量表与 partial 前 40 条展示。高基数事实仍以 `sweep_report.json`、`records_index.json`、archive 与 per-pair records 为准。

## A. 全量转换摸排摘要（迁移自 `sweep_summary.md`）

## R5 seed library 全量转换摸排摘要

本 report 迁移自 R5 `run-seed-sweep` 生成的旧 human summary；当前事实源是 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)，本 Markdown 只做人类入口。

R5 后对主实验 seed 方向的归纳见 [llms_emp_main_seed_analysis.md](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)：当前建议后续 R6/R7 优先围绕 `llms-emp-stm-subset` 展开，并按 10 个唯一 NL cluster 报告。

### 1. denominator

- entry directories: 36
- registry entries: 16
- unregistered entries: 20
- excluded non-entry dirs: `schemas, tools`

### 2. entry 状态统计

| status | entries |
|---|---:|
| `needs_generation` | 2 |
| `not_applicable` | 30 |
| `partial` | 4 |

### 3. pair 状态统计

| status | pairs |
|---|---:|
| `blocked` | 23 |
| `converted` | 529 |
| `needs_generation` | 2 |
| `not_applicable` | 20 |
| `partial` | 504 |

### 4. entry 明细

| entry_id | primary | statuses | pairs | assets | handoff |
|---|---|---|---:|---:|---|
| `automated-transition-use-cases-uml-sm` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `beyond-scenarios-state-models` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `completion-sysml-gwt` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `dependable-product-families-usecases-state-machines` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `designing-fsm-gpt4` | `needs_generation` | `needs_generation` | 1 | 1 | `followup_seed_generation_pr_required_before_r7_or_excluded_by_r7` |
| `executable-state-machines-structured-text` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `executable-use-cases-domain-machine-specifications` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `execution-nl-req-bt-sm` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `from-use-cases-to-statecharts` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `fsm-bench-20` | `needs_generation` | `needs_generation` | 1 | 4 | `followup_seed_generation_pr_required_before_r7_or_excluded_by_r7` |
| `fsm-gen-iec-61499` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `ijisrt-uml-state-diagrams-llm` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `integrating-graphical-nl-specifications` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `llms-emp-stm-subset` | `partial` | `converted, partial, blocked` | 60 | 4 | `r7_eligibility_review` |
| `maritaca-use-case-behavior-models` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `most-states-modes` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `nl-standard-docs-state-machines` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `nlp-req-formalization-testcase-generation` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `object-models-uml-embedded` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `pushing-generative-envelope-mbse` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `req-mermaid-statechart` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `requirements-analysis-prototyping-scenarios-statecharts` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `rscharter-statechart-elements` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `scenarios-statecharts-interrelated` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `sefm-llm-state-machine` | `partial` | `partial` | 1 | 1 | `r7_eligibility_review` |
| `semi-auto-efsm-standard-docs` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `specification-based-verification-usecase-sm` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `statechart-codesign-usecases` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `statechart-use-case-validation-event-driven` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `statistical-usage-testing-uml` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `towards-automatic-model-completion` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `ttool-ai-smd-subset` | `partial` | `partial` | 6 | 3 | `r7_eligibility_review` |
| `umple-nl-state-machine` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |
| `unified-uml-multimodal-validation` | `partial` | `converted, partial, blocked, not_applicable` | 999 | 3 | `r7_eligibility_review` |
| `unified-use-case-statecharts` | `not_applicable` | `not_applicable` | 1 | 0 | `related_work_or_excluded` |
| `web-tool-goal-statechart-derivation` | `not_applicable` | `not_applicable` | 0 | 0 | `related_work_or_excluded` |

### 5. archive

- archives: 2
- index: [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)
- manifest: [archive_manifest.json](../pipeline/readiness_audit/artifact_archives/archive_manifest.json)

## B. 抽样分析（迁移自 `sampling_analysis.md`）

## R5 seed sweep 抽样分析

抽样规则：每个状态组内按 `status -> entry_id -> pair_id` 排序，每类至少取前 3 条；若该类超过 100 条，再追加中位与末尾各 1 条。高基数全量明细仍以 archive / records_index 为准。

### converted

- machine count: 529

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0001` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0002` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0003` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0468` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0997` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |

### partial

- machine count: 504

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0000` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0004` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0005` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0462` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0998` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |

### blocked_or_missing

- machine count: 23

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0018` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0028` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0037` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |

### not_applicable

- machine count: 20

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |
| `dependable-product-families-usecases-state-machines` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |
| `from-use-cases-to-statecharts` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |

### needs_generation

- machine count: 2

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `designing-fsm-gpt4` | `None` | `needs_generation` | `R5.SWEEP.needs_generation_pipeline_only_no_author_generated_stm0` | 需另开 generation PR 复跑；R5 不生成。 |
| `fsm-bench-20` | `None` | `needs_generation` | `R5.SWEEP.needs_generation_pipeline_only_no_author_generated_stm0` | 需另开 generation PR 复跑；R5 不生成。 |

## C. blocked / missing asset 全量展示（迁移自 `blocked_cases.md`）

## R5 blocked / missing_asset cases

> 本文件列出该类别全部记录（23/23）；机器事实源仍以 [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) 和 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) 为准。

事实源为 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) 与 [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)。

| entry | pair | status | reason | handoff |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0018` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0028` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0037` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0031` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0041` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0065` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0192` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0265` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0306` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0423` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0425` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0506` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0511` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0538` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0567` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0675` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0678` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0691` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0713` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0734` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0786` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0955` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0977` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | `r8_negative_evidence` |

## D. partial 前 40 条展示（迁移自 `partial_cases.md`）

## R5 partial cases

> 本文件仅列出前 40 条抽样记录（40/504）；完整清单以 [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) 和 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) 为准。

事实源为 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) 与 [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)。

| entry | pair | status | reason | handoff |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0000` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0004` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0005` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0008` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0009` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0010` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0014` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0015` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0016` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0017` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0019` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0020` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0021` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0022` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0023` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0024` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0025` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0026` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0027` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0029` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0030` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0032` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0033` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0034` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0035` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0038` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0039` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0040` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0041` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0042` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0043` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0044` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0045` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0046` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0047` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0048` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0049` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0050` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0057` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | `r7_eligibility_review` |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0058` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | `r7_eligibility_review` |
