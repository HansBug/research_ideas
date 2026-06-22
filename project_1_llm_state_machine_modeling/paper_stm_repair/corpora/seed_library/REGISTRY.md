# seed_library/REGISTRY.md
> 本文件是一手种子资源登记主表，逐条维护资源明细。[SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要，不复制本表全量事实。
## 1. 角色口径
| emoji | 资源登记角色枚举 | 含义 | 是否可计现成生成种子 |
|---|---|---|---|
| 🟢 | `final_pool_ready` | 已提交的一手 `NL + 生成 `STM_0`` 可直接复验 | 是 |
| 🟡 | `conditional_final_pool` | 一手入口明确，但仍有许可、再分发、本地化、合成数据或版本固定等阻塞 | 条件可用，需先清阻塞项 |
| 🟠 | `pipeline_only` | 有 NL、提示词、schema 或代码，但作者未公开 generated `STM_0` | 否，需本项目复跑另建种子 |
| 🔵 | `reference_only` | 有 `NL + reference STM`，但不是 generated `STM_0` | 否 |
| ⚪ | `paper_reconstructable` | 只有论文图示、附录或示例可人工重建 | 否 |
| 🔴 | `related_only` / `excluded` | 不满足当前一手种子条件 | 否 |
## 2. 一手资源主表

> `条目` 列若有 `assets/README.md`，会直接链接到该条目的一手资源说明；没有 `assets/` 的条目保持普通文本，避免额外 assets 列造成横向阅读负担。表格中少数反引号枚举保留为机器可读字段，其余说明尽量使用中文。

| 条目 | 角色 | 一手入口状态 | 可计生成对 | 已回溯验证 | 原生 case / 参考解 | NL 来源字段 | STM_0 来源字段 | 许可 / 再分发 / 版本 | R2 建议 | 阻塞项 | 机器记录 |
|---|---:|---|---:|---:|---|---|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文附录 / 无作者原生 pair 包<br>无已提交一手生成 pair | [json](./automated-transition-use-cases-uml-sm/seed_resource_registry.json) |
| `dependable-product-families-usecases-state-machines` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 变体建模需切片且作者站点受阻<br>无已提交一手生成 pair | [json](./dependable-product-families-usecases-state-machines/seed_resource_registry.json) |
| `designing-fsm-gpt4` | 🔴 | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 无稳定一手 pair<br>无已提交一手生成 pair | [json](./designing-fsm-gpt4/seed_resource_registry.json) |
| `from-use-cases-to-statecharts` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文示例<br>无已提交一手生成 pair | [json](./from-use-cases-to-statecharts/seed_resource_registry.json) |
| [`fsm-bench-20`](./fsm-bench-20/assets/README.md) | 🟠 | 已下载 | 0 | 0 | 20 / 0 | `dataset/systems/*.json` 需求文本 | 作者未公开 generated 输出 | 许可明确 / 可再分发 / `doi:10.5281/zenodo.20517969; tag:v1.0.0` | 需要本项目复跑 | 作者未公开 generated `STM_0`<br>入种子池前需本项目复跑 | [json](./fsm-bench-20/seed_resource_registry.json) |
| [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md) | 🟡 | 仅元数据 | 0 | 0 | 10 / 10 | `Requirement Description` | `Generation PlantUML` | `unknown` / 仅元数据 / `drive_workbook_pending` | 带 caveat 条件使用 | Drive workbook 尚未提交<br>数据许可未知<br>旧 parquet 不是一手来源 | [json](./llms-emp-stm-subset/seed_resource_registry.json) |
| `maritaca-use-case-behavior-models` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 作者站点受阻且无机读 pair<br>无已提交一手生成 pair | [json](./maritaca-use-case-behavior-models/seed_resource_registry.json) |
| `object-models-uml-embedded` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文示例<br>无已提交一手生成 pair | [json](./object-models-uml-embedded/seed_resource_registry.json) |
| `rscharter-statechart-elements` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 仅公开元素 / 纯输入，无生成 pair<br>无已提交一手生成 pair | [json](./rscharter-statechart-elements/seed_resource_registry.json) |
| [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md) | 🟡 | 已下载 | 1 | 1 | 1 / 8 | backend/resources/state_machine_descriptions.py::SSC7_fall_2024 | Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt | 许可未知 / 再分发未知 / `4open_anonymous_zip_sha256:0e553383...` | 带 caveat 条件使用 | 许可未知<br>再分发未知<br>匿名 4open 制品缺少 release / DOI 固定<br>目前只抽取 SSC7 一组生成 pair | [json](./sefm-llm-state-machine/seed_resource_registry.json) |
| `statechart-codesign-usecases` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 论文示例且存在 序列场景边界<br>无已提交一手生成 pair | [json](./statechart-codesign-usecases/seed_resource_registry.json) |
| `statechart-use-case-validation-event-driven` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文图示，无机读 pair<br>无已提交一手生成 pair | [json](./statechart-use-case-validation-event-driven/seed_resource_registry.json) |
| `statistical-usage-testing-uml` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文示例<br>无已提交一手生成 pair | [json](./statistical-usage-testing-uml/seed_resource_registry.json) |
| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 🟡 | 已下载 | 3 | 3 | 3 / 0 | `input` | `uml_code` | 许可未知 / 再分发未知 / `hf_sha:e330d1afc19361ecbc970348b94cd858e5d32df6` | 带 caveat 条件使用 | 数据集许可未知<br>合成需求 caveat<br>999 行全量解析尚未完成 | [json](./unified-uml-multimodal-validation/seed_resource_registry.json) |
| `unified-use-case-statecharts` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / `none` | 不作为种子使用 | 只有论文示例<br>无已提交一手生成 pair | [json](./unified-use-case-statecharts/seed_resource_registry.json) |

## 3. 当前结论

- 已提交且可回溯验证的生成示例目前包括 `unified-uml-multimodal-validation` 的前三行 Hugging Face 样例，以及 `sefm-llm-state-machine` 的 1 组 SSC7 4open ZIP 样例；二者仍因许可、合成数据或发布稳定性等 caveat 只能是 🟡 条件候选。
- `llms-emp-stm-subset` 是强相关一手入口候选，但当前已提交资产尚未包含 workbook，因此可计生成数量仍为 0；后续需先冻结一手原始资源。
- `fsm-bench-20` 是 pipeline-only：有 NL、提示词、schema 和代码，但作者未公开生成的 `STM_0`。
- 传统 use-case / statechart 工作当前只作论文级可重建线索或相关工作证据，不能进入现成 seed 池。

## 4. 未列入 registry 的既有条目处置

R2.0 只为 `15` 个重点条目建立 `seed_resource_registry.json`。其余既有目录并不因为“目录存在”而自动进入一手种子池；在补齐 registry、assets、hash、locator 和 validator 之前，统一按下表处置，**可计生成数量均为 0**。后续若要升级任何条目，必须先补单条目 `seed_resource_registry.json`，再回写本文件主表。

| 条目 | R2.0 默认处置 | 原因摘要 |
|---|---:|---|
| `beyond-scenarios-state-models` | ⚪ `paper_reconstructable` | 经典 use-case/state-model 文献，当前只有论文级证据；无一手机读生成 pair。 |
| `completion-sysml-gwt` | 🔴 `related_only` | completion / repair-like 任务，依赖已有 partial model，不是当前 `NL -> 生成 `STM_0`` 种子。 |
| `executable-state-machines-structured-text` | ⚪ `paper_reconstructable` | 结构化文本 / SPS 路径需要论文级重建；无作者原生 pair 包。 |
| `executable-use-cases-domain-machine-specifications` | 🔴 `related_only` | 仅 BibTeX / metadata，全文与一手 pair 仍受阻。 |
| `execution-nl-req-bt-sm` | 🔴 `related_only` | NL -> BT -> SM 中间链路；BT / SM 原生数据包未冻结。 |
| `fsm-gen-iec-61499` | 🔴 `related_only` | IEC 61499 / refinement 边界，初始 `STM_0` 与后续 refinement 难隔离，私有制品未公开。 |
| `ijisrt-uml-state-diagrams-llm` | ⚪ `paper_reconstructable` | 只有论文示例 / prompt 级线索，无一手生成 pair 发布包。 |
| `integrating-graphical-nl-specifications` | 🔴 `related_only` | NL 与 graphical notation 共现，不是 `NL -> STM_0` 输出资源。 |
| `most-states-modes` | 🔴 `related_only` | MoSt / NuSMV 非目标 STM family；只作形式化相关工作。 |
| `nl-standard-docs-state-machines` | 🔴 `related_only` | 标准 / 协议式文档边界，原始输出包未公开。 |
| `nlp-req-formalization-testcase-generation` | 🔴 `related_only` | IRDL / testcase / sequence 中间链路，不是可直接入池的 生成 `STM_0`。 |
| `pushing-generative-envelope-mbse` | ⚪ `paper_reconstructable` | 论文级 MBSE / SysML 线索；无一手生成 pair 发布包。 |
| `req-mermaid-statechart` | 🔴 `related_only` | 任务贴合但数据 / 输出私有，不可复验。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🔴 `related_only` | scenario/statechart co-evolution 或反向边界，不是当前 seed。 |
| `scenarios-statecharts-interrelated` | 🔴 `related_only` | scenario / event trace 输入边界，非自然语言需求唯一输入。 |
| `semi-auto-efsm-standard-docs` | 🔴 `related_only` | 标准文档 / EFSM 边界，case 数据 / 生成 EFSM 包未公开。 |
| `specification-based-verification-usecase-sm` | 🔴 `related_only` | state machine 是验证执行机制，不是目标 生成种子。 |
| `towards-automatic-model-completion` | 🔴 `related_only` | model completion / repair-only，依赖 partial SMD。 |
| `ttool-ai-smd-subset` | 🔴 `related_only` | SysML SMD / timing / 私有制品边界；当前不提供一手生成 pair。 |
| `umple-nl-state-machine` | ⚪ `paper_reconstructable` | 论文级 Umple/NL 示例可重建；无一手生成 pair 发布包。 |
| `web-tool-goal-statechart-derivation` | 🔴 `related_only` | goal model / requirements view 输入，不是 NL-only 生成 `STM_0`。 |
