# 种子文库一手资源登记表（REGISTRY.md）

> 本文件是一手种子资源登记主表，逐条维护资源明细。[SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要，不复制本表全量事实。

## 1. 资源登记角色口径

| emoji | 中文角色 | 机器枚举 | 判定含义 | 是否可计现成生成种子 |
|---|---|---|---|---|
| 🟢 | 最终池可直接复验 | `final_pool_ready` | 已提交的一手 $NL + STM_0$ 生成配对可直接复验 | 是 |
| 🟡 | 条件候选 | `conditional_final_pool` | 一手入口明确，但仍有许可、再分发、本地化、合成数据或版本固定等阻塞 | 条件可用，需先清阻塞项 |
| 🟠 | 仅流水线 / 需本项目复跑 | `pipeline_only` | 有 NL、提示词、schema 或代码，但作者未公开生成的 $STM_0$ | 否，需本项目复跑另建种子 |
| 🔵 | 仅参考模型 | `reference_only` | 有 $NL +$ 参考 STM，但不是生成的 $STM_0$ | 否 |
| ⚪ | 论文级可重建线索 | `paper_reconstructable` | 只有论文图示、附录或示例可人工重建 | 否 |
| 🔴 | 相关但不入池 / 排除 | `related_only` / `excluded` | 不满足当前一手种子条件 | 否 |

## 2. 一手资源主表

> “条目”列若有 `assets/README.md`，会直接链接到该条目的一手资源说明；没有 `assets/` 的条目保持普通文本，避免额外 assets 列造成横向阅读负担。表格中少数反引号枚举、文件路径、字段名、哈希和版本标识保留为机器可读写法，其余说明尽量使用中文。

| 条目 | 角色 | 一手入口 | 可计生成对 | 已回溯验证 | 原生样例 / 参考解 | NL 字段 | $STM_0$ 字段 | 许可 / 再分发 / 版本 | R2 处理建议 | 当前阻塞 | 结构化记录 |
|---|---:|---|---:|---:|---|---|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文附录 / 无作者原生配对包<br>无已提交一手生成配对 | [JSON](./automated-transition-use-cases-uml-sm/seed_resource_registry.json) |
| `dependable-product-families-usecases-state-machines` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 变体建模需切片且作者站点受阻<br>无已提交一手生成配对 | [JSON](./dependable-product-families-usecases-state-machines/seed_resource_registry.json) |
| `designing-fsm-gpt4` | 🔴 | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 无稳定一手配对<br>无已提交一手生成配对 | [JSON](./designing-fsm-gpt4/seed_resource_registry.json) |
| `from-use-cases-to-statecharts` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./from-use-cases-to-statecharts/seed_resource_registry.json) |
| [`fsm-bench-20`](./fsm-bench-20/assets/README.md) | 🟠 | 已下载 | 0 | 0 | 20 / 0 | `dataset/systems/*.json` 中的需求文本 | 作者未公开生成输出 | 许可明确 / 可再分发 / DOI `10.5281/zenodo.20517969`，标签 `v1.0.0` | 需要本项目复跑 | 作者未公开生成的 $STM_0$<br>入种子池前需本项目复跑 | [JSON](./fsm-bench-20/seed_resource_registry.json) |
| [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md) | 🟡 | 已下载 | 60 | 60 | 60 / 10 | `Requirement Description` | `Generation PlantUML` | 许可未知 / 再分发未知 / Google Drive folder `10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6`，`gdown` 下载于 2026-06-22 | 带 caveat 条件使用 | 数据许可未知<br>再分发未知<br>需隔离 reference `PlantUML` 与 checking 后结果，避免泄漏<br>旧 parquet 不是一手来源 | [JSON](./llms-emp-stm-subset/seed_resource_registry.json) |
| `maritaca-use-case-behavior-models` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 作者站点受阻且无机读配对<br>无已提交一手生成配对 | [JSON](./maritaca-use-case-behavior-models/seed_resource_registry.json) |
| `object-models-uml-embedded` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./object-models-uml-embedded/seed_resource_registry.json) |
| `rscharter-statechart-elements` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 仅公开元素 / 纯输入，无生成配对<br>无已提交一手生成配对 | [JSON](./rscharter-statechart-elements/seed_resource_registry.json) |
| [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md) | 🟡 | 已下载 | 1 | 1 | 1 / 8 | `backend/resources/state_machine_descriptions.py::SSC7_fall_2024` | `Paper Experiment Resources/Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` | 许可未知 / 再分发未知 / 4open 匿名 ZIP，SHA-256 `0e553383...` | 带 caveat 条件使用 | 许可未知<br>再分发未知<br>匿名 4open 制品缺少 release / DOI 固定<br>目前只抽取 SSC7 一组生成配对 | [JSON](./sefm-llm-state-machine/seed_resource_registry.json) |
| `statechart-codesign-usecases` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 论文示例且存在序列场景边界<br>无已提交一手生成配对 | [JSON](./statechart-codesign-usecases/seed_resource_registry.json) |
| `statechart-use-case-validation-event-driven` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文图示，无机读配对<br>无已提交一手生成配对 | [JSON](./statechart-use-case-validation-event-driven/seed_resource_registry.json) |
| `statistical-usage-testing-uml` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./statistical-usage-testing-uml/seed_resource_registry.json) |
| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 🟡 | 已下载 | 989 | 999 | 999 / 0 | `input` | `uml_code` | 许可未知 / 再分发未知 / Hugging Face 快照 SHA `e330d1afc19361ecbc970348b94cd858e5d32df6` | 带 caveat 条件使用 | 数据集许可未知<br>合成需求 caveat<br>非控制系统场景需质量抽检<br>10 行为 `No valid PlantUML code found.`，已排除 | [JSON](./unified-uml-multimodal-validation/seed_resource_registry.json) |
| `unified-use-case-statecharts` | ⚪ | 不适用 | 0 | 0 | 0 / 0 | — | — | 不适用 / 不适用 / 无 | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./unified-use-case-statecharts/seed_resource_registry.json) |

## 3. 当前结论

- `unified-uml-multimodal-validation` 已全量抽取 Hugging Face parquet 的 999 行，其中 989 行是可回溯的有效 PlantUML 生成配对，10 行为 `No valid PlantUML code found.` 并已排除；因 license、synthetic NL、非控制系统场景与质量抽检 caveat，仍只能是 🟡 条件候选。
- `llms-emp-stm-subset` 已用 `gdown` 下载论文 Google Drive 一手 workbook，并从 `Experiment Results.xlsx` / `STM Results` 全量抽取 60 条 `Requirement Description + Generation PlantUML` 生成配对；因 license / redistribution unknown 以及 reference / checking 列泄漏风险，仍只能是 🟡 条件候选。
- `sefm-llm-state-machine` 已提交 1 组 SSC7 4open ZIP 生成配对；因许可、再分发与匿名 release pin caveat，仍只能是 🟡 条件候选。
- `fsm-bench-20` 目前是“仅流水线 / 需本项目复跑”：有 NL、提示词、schema 和代码，但作者未公开生成的 $STM_0$。
- 传统 use-case / statechart 工作当前只作论文级可重建线索或相关工作证据，不能进入现成 seed 池。

## 4. 未列入登记表的既有条目处置

R2.0 只为 15 个重点条目建立 `seed_resource_registry.json`。其余既有目录并不因为“目录存在”而自动进入一手种子池；在补齐登记记录、`assets/`、哈希、定位器和 validator 之前，统一按下表处置，**可计生成数量均为 0**。后续若要升级任何条目，必须先补单条目 `seed_resource_registry.json`，再回写本文件主表。

| 条目 | 默认角色 | 角色说明 | 原因摘要 |
|---|---:|---|---|
| `beyond-scenarios-state-models` | ⚪ | 论文级可重建线索 | 经典 use-case / state-model 文献，当前只有论文级证据；无一手机读生成配对。 |
| `completion-sysml-gwt` | 🔴 | 相关但不入池 | completion / repair-like 任务，依赖已有 partial model，不是当前 $NL \to STM_0$ 种子。 |
| `executable-state-machines-structured-text` | ⚪ | 论文级可重建线索 | 结构化文本 / SPS 路径需要论文级重建；无作者原生配对包。 |
| `executable-use-cases-domain-machine-specifications` | 🔴 | 相关但不入池 | 仅 BibTeX / 元数据，全文与一手配对仍受阻。 |
| `execution-nl-req-bt-sm` | 🔴 | 相关但不入池 | $NL \to BT \to SM$ 中间链路；BT / SM 原生数据包未冻结。 |
| `fsm-gen-iec-61499` | 🔴 | 相关但不入池 | IEC 61499 / refinement 边界，初始 $STM_0$ 与后续 refinement 难隔离，私有制品未公开。 |
| `ijisrt-uml-state-diagrams-llm` | ⚪ | 论文级可重建线索 | 只有论文示例 / prompt 级线索，无一手生成配对发布包。 |
| `integrating-graphical-nl-specifications` | 🔴 | 相关但不入池 | NL 与 graphical notation 共现，不是 $NL \to STM_0$ 输出资源。 |
| `most-states-modes` | 🔴 | 相关但不入池 | MoSt / NuSMV 非目标 STM family；只作形式化相关工作。 |
| `nl-standard-docs-state-machines` | 🔴 | 相关但不入池 | 标准 / 协议式文档边界，原始输出包未公开。 |
| `nlp-req-formalization-testcase-generation` | 🔴 | 相关但不入池 | IRDL / testcase / sequence 中间链路，不是可直接入池的生成 $STM_0$。 |
| `pushing-generative-envelope-mbse` | ⚪ | 论文级可重建线索 | 论文级 MBSE / SysML 线索；无一手生成配对发布包。 |
| `req-mermaid-statechart` | 🔴 | 相关但不入池 | 任务贴合但数据 / 输出私有，不可复验。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🔴 | 相关但不入池 | scenario / statechart co-evolution 或反向边界，不是当前 seed。 |
| `scenarios-statecharts-interrelated` | 🔴 | 相关但不入池 | scenario / event trace 输入边界，非自然语言需求唯一输入。 |
| `semi-auto-efsm-standard-docs` | 🔴 | 相关但不入池 | 标准文档 / EFSM 边界，case 数据 / 生成 EFSM 包未公开。 |
| `specification-based-verification-usecase-sm` | 🔴 | 相关但不入池 | state machine 是验证执行机制，不是目标生成种子。 |
| `towards-automatic-model-completion` | 🔴 | 相关但不入池 | model completion / repair-only，依赖 partial SMD。 |
| `ttool-ai-smd-subset` | 🔴 | 相关但不入池 | SysML SMD / timing / 私有制品边界；当前不提供一手生成配对。 |
| `umple-nl-state-machine` | ⚪ | 论文级可重建线索 | 论文级 Umple / NL 示例可重建；无一手生成配对发布包。 |
| `web-tool-goal-statechart-derivation` | 🔴 | 相关但不入池 | goal model / requirements view 输入，不是 NL-only 生成 $STM_0$。 |
