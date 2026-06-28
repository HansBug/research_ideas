# R5 seed library 全量转换摸排摘要

本文件由 `run-seed-sweep` 生成。事实源是 [sweep_report.json](./sweep_report.json)，本 Markdown 只做人类入口。

## 1. denominator

- entry directories: 36
- registry entries: 16
- unregistered entries: 20
- excluded non-entry dirs: `schemas, tools`

## 2. entry 状态统计

| status | entries |
|---|---:|
| `needs_generation` | 2 |
| `not_applicable` | 30 |
| `partial` | 4 |

## 3. pair 状态统计

| status | pairs |
|---|---:|
| `blocked` | 23 |
| `converted` | 529 |
| `needs_generation` | 2 |
| `not_applicable` | 20 |
| `partial` | 504 |

## 4. entry 明细

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

## 5. archive

- archives: 2
- index: [records_index.json](./records_index.json)
- manifest: [archive_manifest.json](./archive_manifest.json)
