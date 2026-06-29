# R5 seed library readiness report

> 证据引用说明：正文中的方括号引用（如 `[src-*]`、`[clm-*]`、`[cmd-*]`）均指向文末审计附录。这些键是稳定 ASCII key，不按数字顺序重排；新增证据时只新增 key，不批量改旧 key。

## 迁移说明

本 report 汇总 R5 seed library readiness 的 human-facing 入口：全量 entry/pair 摘要、状态抽样、blocked 全量表与 partial 前 40 条展示。高基数事实仍以 `sweep_report.json`、`records_index.json`、archive 与 per-pair records 为准 [src-readiness-sweep][src-readiness-index][src-readiness-record-archives]。

## A. 全量转换摸排摘要（迁移自 `sweep_summary.md`）

## R5 seed library 全量转换摸排摘要

本 report 迁移自 R5 `run-seed-sweep` 生成的旧 human summary；当前事实源是 [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)，本 Markdown 只做人类入口。

R5 后对主实验 seed 方向的归纳见 [R5 `llms-emp` 方向性分析报告](./2026-06-28-19-42-58-r5-llms-emp-directional-analysis.md)：当前建议后续 R6/R7 优先围绕 `llms-emp-stm-subset` 展开，并按 10 个唯一 NL cluster 报告。

### 1. denominator

- entry directories: 36 [clm-readiness-denominator]
- registry entries: 16 [clm-readiness-denominator]
- unregistered entries: 20 [clm-readiness-denominator]
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

- archives: 2 [src-readiness-archive-manifest]
- index: [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)
- manifest: [archive_manifest.json](../pipeline/readiness_audit/artifact_archives/archive_manifest.json)

## B. 抽样分析（迁移自 `sampling_analysis.md`）

## R5 seed sweep 抽样分析

抽样规则：每个状态组内按 `status -> entry_id -> pair_id` 排序，每类至少取前 3 条；若该类超过 100 条，再追加中位与末尾各 1 条。高基数全量明细仍以 archive / records_index 为准 [clm-readiness-partial-slice][src-readiness-index]。

### converted

- machine count: 529 [clm-readiness-status]

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0001` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0002` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0003` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0468` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0997` | `converted` | `R5.SWEEP.converted_fcstm_parse_inspect_ok` | 可进入 pre-repair `.fcstm` 表示，但仍需保留 loss 与 attribution。 |

### partial

- machine count: 504 [clm-readiness-status]

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0000` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0004` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0005` | `partial` | `R5.SWEEP.partial_representation_loss_or_caveat` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0462` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |
| `unified-uml-multimodal-validation` | `unified_uml_state_train_0998` | `partial` | `R5.SWEEP.partial_r3_1_normalization_or_representation_loss` | 可作为后续 eligibility review 对象；不能无条件进入主实验。 |

### blocked_or_missing

- machine count: 23 [clm-readiness-status][clm-readiness-blocked-reason]

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `llms-emp-stm-subset` | `llms_emp_stm_results_0018` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0028` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |
| `llms-emp-stm-subset` | `llms_emp_stm_results_0037` | `blocked` | `R5.SWEEP.blocked_official_scxml_unavailable` | 当前工具链负证据；优先归入 R8 negative evidence 或 converter follow-up。 |

### not_applicable

- machine count: 20 [clm-readiness-status]

| entry | pair | status | reason | 学术解释 |
|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |
| `dependable-product-families-usecases-state-machines` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |
| `from-use-cases-to-statecharts` | `None` | `not_applicable` | `R5.SWEEP.not_applicable_no_extracted_pairs_jsonl` | 不是作者一手 generated seed；只保留为相关工作或排除证据。 |

### needs_generation

- machine count: 2 [clm-readiness-status]

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

## 审计附录：证据链与事实源

### A.1 来源考据表

| source path | source creation commit | prefix commit | substantive fact commit 判定理由 | non-prefix revision/migration commit | canonical machine source |
|---|---|---|---|---|---|
| `pipeline/readiness_audit/seed_sweep/sweep_summary.md` | `6e1d8b510209804a0e4afeeeed4a81720d398270` (2026-06-28 03:10:11 +0800, R5 seed sweep 初始生成) | `185aa02c26caba9eece9327248379004fd7f6488` (2026-06-28 04:03:18 +0800, readiness denominator 与抽样展示冻结) | `185aa02c26caba9eece9327248379004fd7f6488` (2026-06-28 04:03:18 +0800)：补齐复验入口与抽样展示；`5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4` 已先修正证据链，`bbd974c17da1c113eca847c1ae7ba2969c7f0644` 只追加主 seed 方向链接，不改变 readiness denominator。 | `73af4d83a7ccffeac47ca61ab6708bfcbfe44c6f` (2026-06-28 15:05:25 +0800, pipeline 路径迁移)；`1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json)；[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json)；[archive_manifest.json](../pipeline/readiness_audit/artifact_archives/archive_manifest.json) |
| `pipeline/readiness_audit/seed_sweep/sampling_analysis.md`、`blocked_cases.md`、`partial_cases.md` | `6e1d8b510209804a0e4afeeeed4a81720d398270` / `5d0a2a01de4fd3cc50a0b626dc775f15bc60a1f4`（R5 sweep 衍生展示文件创建与证据链修正） | `185aa02c26caba9eece9327248379004fd7f6488` (2026-06-28 04:03:18 +0800, readiness denominator 与抽样展示冻结) | `185aa02c26caba9eece9327248379004fd7f6488`：抽样展示成为可复验 readiness report 的稳定 human-facing 入口；blocked/partial 表仅是机器索引的阅读切片。 | `73af4d83a7ccffeac47ca61ab6708bfcbfe44c6f` (2026-06-28 15:05:25 +0800, pipeline 路径迁移)；`1ab6af18eda24cf35a10eb9e99e1f59ca9b6b616` (2026-06-29 02:41:50 +0800, R5.5.1 reports/readiness 路径迁移)；后续修正只补 CI 路径、full SHA 与人类入口链接，不改 canonical machine facts。 | [sweep archive](../pipeline/readiness_audit/artifact_archives/archives/)；[audit records](../pipeline/readiness_audit/seed_sweep/audit_records/)；[records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) |

> 本节是本 report 的事实绑定入口：Markdown 只做人类阅读与论文写作 handoff，不替代 canonical JSON/JSONL/ZIP/committed run artifacts。复验时优先回到最后一列机器事实源。

### A.2 上游事实源清单

| 编号 / 引用键 | source_id | 事实源 | 类型 | 用途 | 关键锚点 |
|---|---|---|---|---|---|
| [src-readiness-sweep] | `sweep_report` | [sweep_report.json](../pipeline/readiness_audit/seed_sweep/sweep_report.json) | `json` | 支撑 entry / pair denominator、状态统计与 generation context | `#/summary`、`#/entries[]`、`#/meta` |
| [src-readiness-index] | `records_index` | [records_index.json](../pipeline/readiness_audit/seed_sweep/records_index.json) | `json` | 支撑 per-record 全量索引、blocked / partial 展示和 handoff target | `#/records[]`，按 `entry_id` / `pair_id` / `status` filter |
| [src-readiness-archive-manifest] | `archive_manifest` | [archive_manifest.json](../pipeline/readiness_audit/artifact_archives/archive_manifest.json) | `json` | 支撑高基数 record archive 的位置、hash 与策略 | `#/archives[]`；`llms-emp-stm-subset_records.zip.sha256=f3ee8bf5755aae3b5021cf49e119a235c1de7db0b5e02af8f4b81f7044fe7d8f` |
| [src-readiness-record-archives] | `record_archives` | [archives/](../pipeline/readiness_audit/artifact_archives/archives/) | `zip` | 支撑高基数 per-pair record 的 status reason、fcstm hash 与完整 record JSON；尤其 blocked reason 需要打开 ZIP 内 JSON 复核 | `*_records.zip`；member pattern: `<entry>_records/*.json`；hash 见 `archive_manifest#/archives[]/sha256` |
| [src-readiness-audit-records] | `audit_records` | [audit_records/](../pipeline/readiness_audit/seed_sweep/audit_records/) | `json` | 支撑 per-entry / per-asset / per-pair 细节复核 | `entry_id__*.json` |
| [src-readiness-seed-registry] | `seed_registry` | [REGISTRY.md](../corpora/seed_library/REGISTRY.md) 与各 `seed_resource_registry.json` | `md/json` | 支撑 first-source / not_applicable / needs_generation 的资源分类背景 | `seed_id` row、`resource_category`、`pair_sets` |

### A.3 Claim-evidence map

| 编号 / 引用键 | claim_id | 结论 / claim | 类型 | 上游事实源与锚点 | 复验命令 | 置信度 | 限制 / caveat |
|---|---|---|---|---|---|---|---|
| [clm-readiness-denominator] | `R5-READINESS-C1` | R5 sweep denominator 为 36 entries、16 registry entries、20 unregistered entries。 | `count` | `sweep_report#/summary`、`#/meta` | [cmd-readiness-summary] | `high` | denominator 是 R5 seed library 快照，不是系统性文献全集。 |
| [clm-readiness-status] | `R5-READINESS-C2` | pair 状态为 `converted=529 / partial=504 / blocked=23 / not_applicable=20 / needs_generation=2`。 | `count` | `sweep_report#/summary/pair_status_counts`、`records_index#/records[].status` | [cmd-readiness-status] | `high` | 这是 pre-repair readiness，不是方法成功率。 |
| [clm-readiness-entry-handoff] | `R5-READINESS-C3` | entry 明细与 handoff target 来自 `entries[]` 聚合。 | `classification` | `sweep_report#/entries[]/{entry_id,primary_entry_status,status_counts_by_pair,handoff_target}` | [cmd-readiness-summary] | `high` | `not_applicable` / `needs_generation` 的学术排除理由需回到 registry / assets。 |
| [clm-readiness-blocked-reason] | `R5-READINESS-C4` | blocked 展示本轮没有 missing-asset case；23 条均为 `R5.SWEEP.blocked_official_scxml_unavailable`。 | `count` | `records_index#/records[status=blocked]`、record archive member `status_reason_code`、`sweep_report#/summary/pair_status_counts` | [cmd-readiness-blocked-archive] | `high` | `records_index` 只保存状态，reason 必须打开 ZIP 内 per-record JSON 复验；blocked 只表示当前工具链 / committed evidence 下不可进入转换结果。 |
| [clm-readiness-partial-slice] | `R5-READINESS-C5` | partial 前 40 条是排序后的阅读切片，不是完整 partial 清单。 | `trace` | `records_index#/records[status=partial]`，排序 `entry_id,pair_id` 后截断 | [cmd-readiness-partial-slice] | `high` | 完整 504 条以 `records_index` 和 record archives 为准。 |

### A.4 复验命令

```bash
# [cmd-readiness-summary] CMD-READINESS-1 / CMD-READINESS-2 / CMD-READINESS-3
python - <<'PY'
import json
p='project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/seed_sweep/sweep_report.json'
d=json.load(open(p))
print(d['summary'])
print({k:d['meta'][k] for k in ['entry_dir_count','registry_entry_count','unregistered_entry_count','repair_contribution_allowed']})
print([(e['entry_id'], e['primary_entry_status'], e['pair_record_count'], e['handoff_target']) for e in d['entries'][:5]])
PY
```

```bash
# [cmd-readiness-status] / [cmd-readiness-blocked-archive] / [cmd-readiness-partial-slice] CMD-READINESS-4 / CMD-READINESS-5
python - <<'PY'
import json, collections, pathlib, zipfile
root=pathlib.Path('.')
p=root/'project_1_llm_state_machine_modeling/paper_stm_repair/pipeline/readiness_audit/seed_sweep/records_index.json'
rows=json.load(open(p))['records']
print(collections.Counter(r.get('status') for r in rows))
blocked=[r for r in rows if r.get('status')=='blocked']
reasons=collections.Counter()
entries=collections.Counter()
for r in blocked:
    entries[r['entry_id']] += 1
    with zipfile.ZipFile(root/r['archive_path']) as z:
        rec=json.loads(z.read(r['path_in_zip']))
    reasons[rec.get('status_reason_code')] += 1
print('blocked_entries', entries)
print('blocked_archive_reasons', reasons)
partial=sorted([r for r in rows if r.get('status')=='partial'], key=lambda r:(r.get('entry_id') or '', r.get('pair_id') or ''))
print('partial_total', len(partial), 'first40_last', partial[39].get('record_id'))
PY
```
