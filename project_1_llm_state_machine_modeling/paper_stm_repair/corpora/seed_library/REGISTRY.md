# seed_library/REGISTRY.md
> 本文件是一手 seed 资源 registry 主表，逐条维护资源明细。`SUMMARY.md` 只保留研究结论与统计摘要，不复制本表全量事实。
## 1. 角色口径
| emoji | recommended_role | 含义 | 是否可计现成 generated seed |
|---|---|---|---|
| 🟢 | `final_pool_ready` | committed 一手 `NL + generated STM_0` 可直接复验 | 是 |
| 🟡 | `conditional_final_pool` | 一手入口明确但仍有 license / local_only / 未落盘 / synthetic caveat | 条件，需先清 blocker |
| 🟠 | `pipeline_only` | 有 NL / prompt / schema / code，但作者未公开 generated `STM_0` | 否，需本项目复跑另建 seed |
| 🔵 | `reference_only` | 有 `NL + reference STM`，不是 generated `STM_0` | 否 |
| ⚪ | `paper_reconstructable` | 只有论文图示 / 附录 / 示例可人工重建 | 否 |
| 🔴 | `related_only` / `excluded` | 不满足当前一手 seed 条件 | 否 |
## 2. 一手资源主表
| seed_id | 角色 | 一手入口状态 | generated eligible | trace verified | canonical / reference | NL 字段 | STM_0 字段 | 许可/再分发/版本 | R2 建议 | blocker | 单条目 | assets |
|---|---:|---|---:|---:|---|---|---|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_appendix_only_no_native_pair_package<br>no_committed_first_source_generated_pair | [json](automated-transition-use-cases-uml-sm/seed_resource_registry.json) | — |
| `dependable-product-families-usecases-state-machines` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | variability_and_author_site_blocked<br>no_committed_first_source_generated_pair | [json](dependable-product-families-usecases-state-machines/seed_resource_registry.json) | — |
| `designing-fsm-gpt4` | 🔴 | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | no_stable_first_source_pair<br>no_committed_first_source_generated_pair | [json](designing-fsm-gpt4/seed_resource_registry.json) | — |
| `from-use-cases-to-statecharts` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_example_only<br>no_committed_first_source_generated_pair | [json](from-use-cases-to-statecharts/seed_resource_registry.json) | — |
| `fsm-bench-20` | 🟠 | `downloaded` | 0 | 0 | 20 / 0 | dataset/systems/*.json requirements | missing_generated_output | `clear` / `redistributable` / `doi:10.5281/zenodo.20517969; tag:v1.0.0` | `rerun_required` | no_published_generated_stm0<br>rerun_required_before_seed | [json](fsm-bench-20/seed_resource_registry.json) | [assets/manifest.json](fsm-bench-20/assets/manifest.json) |
| `llms-emp-stm-subset` | 🟡 | `metadata_only` | 0 | 0 | 10 / 10 | Requirement Description | Generation PlantUML | `unknown` / `metadata_only` / `drive_workbook_pending` | `usable_with_caveat` | drive_workbook_not_committed<br>data_license_unknown<br>old_parquet_not_first_source | [json](llms-emp-stm-subset/seed_resource_registry.json) | [assets/manifest.json](llms-emp-stm-subset/assets/manifest.json) |
| `maritaca-use-case-behavior-models` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | author_site_blocked_no_machine_readable_pair<br>no_committed_first_source_generated_pair | [json](maritaca-use-case-behavior-models/seed_resource_registry.json) | — |
| `object-models-uml-embedded` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_example_only<br>no_committed_first_source_generated_pair | [json](object-models-uml-embedded/seed_resource_registry.json) | — |
| `rscharter-statechart-elements` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | only_elements_and_pure_input_public_no_generated_pair<br>no_committed_first_source_generated_pair | [json](rscharter-statechart-elements/seed_resource_registry.json) | — |
| `sefm-llm-state-machine` | 🟡 | `metadata_only` | 0 | 0 | 1 / 8 | backend/resources/state_machine_descriptions.py::SSC7_fall_2024 | Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt | `unknown` / `metadata_only` / `4open_zip_pending` | `usable_with_caveat` | 4open_zip_not_committed<br>license_unknown<br>ssc7_pair_not_trace_verified | [json](sefm-llm-state-machine/seed_resource_registry.json) | [assets/manifest.json](sefm-llm-state-machine/assets/manifest.json) |
| `statechart-codesign-usecases` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_example_sequence_boundary<br>no_committed_first_source_generated_pair | [json](statechart-codesign-usecases/seed_resource_registry.json) | — |
| `statechart-use-case-validation-event-driven` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_figures_only_no_machine_readable_pair<br>no_committed_first_source_generated_pair | [json](statechart-use-case-validation-event-driven/seed_resource_registry.json) | — |
| `statistical-usage-testing-uml` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_example_only<br>no_committed_first_source_generated_pair | [json](statistical-usage-testing-uml/seed_resource_registry.json) | — |
| `unified-uml-multimodal-validation` | 🟡 | `downloaded` | 3 | 3 | 3 / 0 | input | uml_code | `unknown` / `unknown` / `hf_sha:e330d1afc19361ecbc970348b94cd858e5d32df6` | `usable_with_caveat` | dataset_license_unknown<br>synthetic_requirements_caveat<br>full_999_row_parse_not_yet_run | [json](unified-uml-multimodal-validation/seed_resource_registry.json) | [assets/manifest.json](unified-uml-multimodal-validation/assets/manifest.json) |
| `unified-use-case-statecharts` | ⚪ | `not_applicable` | 0 | 0 | 0 / 0 | — | — | `not_applicable` / `not_applicable` / `none` | `do_not_use_as_seed` | paper_example_only<br>no_committed_first_source_generated_pair | [json](unified-use-case-statecharts/seed_resource_registry.json) | — |

## 3. 当前结论

- committed 且可用 trace 的 generated 示例目前只有 `unified-uml-multimodal-validation` 的前三行审计样例，但其 license 与 synthetic caveat 使其只能是 🟡 条件候选。
- `llms-emp-stm-subset` 与 `sefm-llm-state-machine` 是强相关一手入口候选，但当前 committed assets 尚未包含 workbook / ZIP，因此 eligible generated count 仍为 0；后续需先冻结一手 raw。
- `fsm-bench-20` 是 pipeline-only：有 NL、prompt、schema 和代码，但作者未公开 generated `STM_0`。
- 传统 use-case/statechart 工作当前只作 paper-reconstructable / related evidence，不能进入现成 seed 池。

## 4. 未列入 registry 的既有条目处置

R2.0 只为 `15` 个重点条目建立 `seed_resource_registry.json`。其余既有目录并不因为“目录存在”而自动进入一手 seed 池；在补齐 registry、assets、hash、locator 和 validator 之前，统一按下表处置，**generated eligible count 均为 0**。后续若要升级任何条目，必须先补单条目 `seed_resource_registry.json`，再回写本文件主表。

| seed_id | R2.0 默认处置 | 原因摘要 |
|---|---:|---|
| `beyond-scenarios-state-models` | ⚪ `paper_reconstructable` | 经典 use-case/state-model 文献，当前只有论文级证据；无一手 machine-readable generated pair。 |
| `completion-sysml-gwt` | 🔴 `related_only` | completion/repair-like 任务，依赖已有 partial model，不是 current `NL -> generated STM_0` seed。 |
| `executable-state-machines-structured-text` | ⚪ `paper_reconstructable` | 结构化文本 / SPS 路径需要论文级重建；无作者原生 pair 包。 |
| `executable-use-cases-domain-machine-specifications` | 🔴 `related_only` | 仅 BibTeX / metadata，全文与一手 pair 仍受阻。 |
| `execution-nl-req-bt-sm` | 🔴 `related_only` | NL -> BT -> SM 中间链路；BT / SM 原生数据包未冻结。 |
| `fsm-gen-iec-61499` | 🔴 `related_only` | IEC 61499 / refinement 边界，初始 `STM_0` 与后续 refinement 难隔离，私有制品未公开。 |
| `ijisrt-uml-state-diagrams-llm` | ⚪ `paper_reconstructable` | 只有论文示例 / prompt 级线索，无一手 generated pair release。 |
| `integrating-graphical-nl-specifications` | 🔴 `related_only` | NL 与 graphical notation 共现，不是 `NL -> STM_0` 输出资源。 |
| `most-states-modes` | 🔴 `related_only` | MoSt / NuSMV 非目标 STM family；只作形式化相关工作。 |
| `nl-standard-docs-state-machines` | 🔴 `related_only` | 标准 / 协议式文档边界，原始输出包未公开。 |
| `nlp-req-formalization-testcase-generation` | 🔴 `related_only` | IRDL / testcase / sequence 中间链路，不是可直接入池的 generated STM_0。 |
| `pushing-generative-envelope-mbse` | ⚪ `paper_reconstructable` | 论文级 MBSE / SysML 线索；无一手 generated pair release。 |
| `req-mermaid-statechart` | 🔴 `related_only` | 任务贴合但数据 / 输出私有，不可复验。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🔴 `related_only` | scenario/statechart co-evolution 或反向边界，不是 current seed。 |
| `scenarios-statecharts-interrelated` | 🔴 `related_only` | scenario / event trace 输入边界，非自然语言需求唯一输入。 |
| `semi-auto-efsm-standard-docs` | 🔴 `related_only` | 标准文档 / EFSM 边界，case data / generated EFSM 包未公开。 |
| `specification-based-verification-usecase-sm` | 🔴 `related_only` | state machine 是验证执行机制，不是目标 generated seed。 |
| `towards-automatic-model-completion` | 🔴 `related_only` | model completion / repair-only，依赖 partial SMD。 |
| `ttool-ai-smd-subset` | 🔴 `related_only` | SysML SMD / timing / 私有制品边界；当前不提供一手 generated pair。 |
| `umple-nl-state-machine` | ⚪ `paper_reconstructable` | 论文级 Umple/NL 示例可重建；无一手 generated pair release。 |
| `web-tool-goal-statechart-derivation` | 🔴 `related_only` | goal model / requirements view 输入，不是 NL-only generated STM_0。 |
