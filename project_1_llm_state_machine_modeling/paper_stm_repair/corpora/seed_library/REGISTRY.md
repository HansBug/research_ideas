# 种子文库一手资源登记表（REGISTRY.md）

> 本文件是一手种子资源登记主表，逐条维护资源明细。[SUMMARY.md](./SUMMARY.md) 只保留研究结论与统计摘要，不复制本表全量事实。

## 1. 资源登记角色口径

> 本轮起，**许可 / 再分发不再作为升绿 blocker**：这些对象均来自论文、作者制品页、Zenodo、Hugging Face、Google Drive 或 4open 等公开学术资源，后续论文中规范引用原作即可。本表的 🟢/🟡 主要按“一手资源是否可回溯、是否有 generated $STM_0$、是否存在数据质量 / 泄漏 / 领域适配 caveat”判断。

| emoji | 中文角色 | 机器枚举 | 判定含义 | 是否可计现成生成种子 |
|---|---|---|---|---|
| 🟢 | 可直接复验 | `final_pool_ready` | 已提交的一手 $NL + STM_0$ 生成配对可通过 raw hash / locator / 文本回溯复验；仍可在备注中保留 synthetic、非控制系统、样本少等学术 caveat | 是 |
| 🟡 | 条件候选 | `conditional_final_pool` | 一手入口明确，但还缺关键 raw、locator、generated 输出、泄漏隔离或质量审计，暂不能直接计入现成生成种子 | 条件可用，需先清具体阻塞 |
| 🟠 | 仅流水线 / 需本项目复跑 | `pipeline_only` | 有 NL、提示词、schema 或代码，但作者未公开生成的 $STM_0$ | 否，需本项目复跑另建种子 |
| 🔵 | 仅参考模型 | `reference_only` | 有 $NL +$ 参考 STM，但不是生成的 $STM_0$ | 否 |
| ⚪ | 论文级可重建线索 | `paper_reconstructable` | 只有论文图示、附录或示例可人工重建 | 否 |
| 🔴 | 相关但不入池 / 排除 | `related_only` / `excluded` | 不满足当前一手种子条件 | 否 |

## 2. 一手资源主表

> “条目”列若有 `assets/README.md`，会直接链接到该条目的一手资源说明；没有 `assets/` 的条目保持普通文本，避免额外 assets 列造成横向阅读负担。`NL 数` 写作 `raw / unique`：`raw` 是一手资源里可定位的 NL 行/条目数，`unique` 是按 NL 文本去重后的数量。`NL-only` 也按 `raw / unique` 理解；若 raw 与 unique 相同可写成 `n / n`，表示有 NL 但没有可计 generated $STM_0$ 的数量，例如 generation failure 行或 pipeline-only requirements。传统论文级线索若没有机读一手资源，统一写 `0 / 未知`，不要把论文图示数误当作可复验 seed 数。

| 条目 | 角色 | 一手入口 | NL 数 | 可计生成对 | 已回溯验证 | 参考解 | NL-only | NL 字段 | $STM_0$ 字段 | R2 处理建议 | 当前阻塞 / caveat | 结构化记录 | 备注 |
|---|---:|---|---:|---:|---:|---:|---:|---|---|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文附录 / 无作者原生配对包<br>无已提交一手生成配对 | [JSON](./automated-transition-use-cases-uml-sm/seed_resource_registry.json) | 需人工全文读附录才可统计论文示例 NL 数；不计一手 seed |
| `dependable-product-families-usecases-state-machines` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 变体建模需切片且作者站点受阻<br>无已提交一手生成配对 | [JSON](./dependable-product-families-usecases-state-machines/seed_resource_registry.json) | product-family 变体需人工切片；不计一手 seed |
| `designing-fsm-gpt4` | 🔴 | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 无稳定一手配对<br>无已提交一手生成配对 | [JSON](./designing-fsm-gpt4/seed_resource_registry.json) | 相关方法线索，当前无一手 pair |
| `from-use-cases-to-statecharts` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./from-use-cases-to-statecharts/seed_resource_registry.json) | paper-only 示例；不计一手 seed |
| [`fsm-bench-20`](./fsm-bench-20/assets/README.md) | 🟠 | 已下载 | 252 / 252 | 0 | 0 | 0 | 252 / 252 | `dataset/systems/*.json` 中 20 个系统、252 条 requirements | 作者未公开生成输出；schema 只定义期望 FSM JSON | 需要本项目复跑 | 作者未公开生成的 $STM_0$<br>`benchmark/gold/*.json` 为空 `{}` placeholder，不能冒充 reference / generated STM | [JSON](./fsm-bench-20/seed_resource_registry.json) | 20 个系统、252 条 NL requirements 且去重后仍为 252；可作 NL-only / pipeline fallback，不是现成 pair |
| [`llms-emp-stm-subset`](./llms-emp-stm-subset/assets/README.md) | 🟢 | 已下载 | 60 / 10 | 60 | 60 | 10 | 0 / 0 | `Requirement Description` | `Generation PlantUML` | 可直接作为一手 LLM seed 使用 | 需隔离 reference `PlantUML` 与 checking 后结果，避免泄漏<br>旧 parquet 不是一手来源 | [JSON](./llms-emp-stm-subset/seed_resource_registry.json) | `STM Results` 为 60 行 × 37 列；10 个唯一需求描述 × Claude/DeepSeek/GPT-4/GPT-4o/Kimi/Llama 6 个 LLM；`Generation PlantUML` exact unique=59 但 pair 仍按 60 行计 |
| `maritaca-use-case-behavior-models` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 作者站点受阻且无机读配对<br>无已提交一手生成配对 | [JSON](./maritaca-use-case-behavior-models/seed_resource_registry.json) | 需人工全文 / 作者站点核验后才可统计论文示例 |
| `object-models-uml-embedded` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./object-models-uml-embedded/seed_resource_registry.json) | paper-only 示例；不计一手 seed |
| `rscharter-statechart-elements` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 仅公开元素 / 纯输入，无生成配对<br>无已提交一手生成配对 | [JSON](./rscharter-statechart-elements/seed_resource_registry.json) | 可能有输入元素线索，但无 generated pair |
| [`sefm-llm-state-machine`](./sefm-llm-state-machine/assets/README.md) | 🟢 | 已下载 | 9 / 9 | 1 | 1 | 8 | 8 / 8 | `state_machine_descriptions.py` 中 9 个 NL symbols；eligible pair 只用 `SSC7_fall_2024` | `Final Single Prompt/Claude Sonnet 3.5/SSC7_single_prompt_*.txt` | 可直接作为单例一手 LLM seed 使用；其余 8 个无 generated 输出的 NL 只作 NL-only/reference-only 资产 | 目前只有 SSC7 有 generated text output<br>其他 8 个 NL 缺 generated 输出（7 个 reference-only + 1 个 ATAS 纯 NL-only）<br>workbook image refs 不能反推 STM 文本 | [JSON](./sefm-llm-state-machine/seed_resource_registry.json) | 论文实验口径为 8 个课程 reactive-system descriptions + 8 个 expert reference；ZIP 额外含 ATAS NL，共 9 个 unique NL；8 个 reference solutions、1 个 generated SSC7 text output、63 个 workbook image-ref cells / 47 个唯一图片名但无可恢复 PNG / STM 文本；8 个无 generated 输出的 NL 中 7 个有 reference solution、1 个 ATAS 为纯 NL-only |
| `statechart-codesign-usecases` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 论文示例且存在序列场景边界<br>无已提交一手生成配对 | [JSON](./statechart-codesign-usecases/seed_resource_registry.json) | paper-only co-design 示例；保守不计 |
| `statechart-use-case-validation-event-driven` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文图示，无机读配对<br>无已提交一手生成配对 | [JSON](./statechart-use-case-validation-event-driven/seed_resource_registry.json) | 论文图示线索；无机读 pair |
| `statistical-usage-testing-uml` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./statistical-usage-testing-uml/seed_resource_registry.json) | paper-only 示例；保守不计 |
| [`unified-uml-multimodal-validation`](./unified-uml-multimodal-validation/assets/README.md) | 🟢 | 已下载 | 999 / 999 | 989 | 999 | 0 | 10 / 10 | `input` | `uml_code` | 可作为 synthetic UML state-diagram smoke/stress seed | 合成需求 caveat<br>非控制系统场景需质量抽检<br>10 行为 `No valid PlantUML code found.`，已列入 `excluded_pair_ids` 并排除 | [JSON](./unified-uml-multimodal-validation/seed_resource_registry.json) | LLaMA-3.2-1B 合成通用软件 feature description，DeepSeek-R1-Distill-Qwen-32B 生成 PlantUML；999 raw NL 与 989 eligible NL 均 exact / whitespace-normalized 唯一，不是 1×N；10 个 failure 行共享同一个 sentinel，不计 unique generated STM_0；论文有 pipeline-level VLM/94-expert validation，但 HF parquet 无逐行 VLM/human score |
| `unified-use-case-statecharts` | ⚪ | 不适用 | 0 / 未知 | 0 | 0 | 0 | 未知 / 未知 | — | — | 不作为种子使用 | 只有论文示例<br>无已提交一手生成配对 | [JSON](./unified-use-case-statecharts/seed_resource_registry.json) | paper-only case studies；保守不计 |

## 3. 当前结论

- `llms-emp-stm-subset`、`sefm-llm-state-machine`、`unified-uml-multimodal-validation` 均已有 committed 一手 raw、typed locator、文本 / hash 回溯和 validator 复算，因此本轮按 `final_pool_ready` 处理；后续论文中规范引用原工作即可，不再把许可 / 再分发写作升绿 blocker。
- `llms-emp-stm-subset` 已用 `gdown` 下载论文 Google Drive 一手 workbook，并从 `Experiment Results.xlsx` / `STM Results` 全量抽取 60 条 `Requirement Description + Generation PlantUML` 生成配对；它实际是 **10 个唯一 NL × 6 个 LLM 输出** 的 1×N 形态，使用时必须只读 `Generation PlantUML`，不得混入 reference `PlantUML` 或 checking 后结果。
- `sefm-llm-state-machine` 的论文实验口径是 8 个 reactive-system descriptions + 8 个 expert reference；当前 raw ZIP 真实结构是 **9 个 NL descriptions（多出 ATAS NL-only）、8 个 reference solutions、1 个 generated text output、63 个 workbook image-ref cells / 47 个唯一图片名但无 embedded PNG / STM 文本**。只有 SSC7 同时具备 NL 与 Claude Sonnet 3.5 single-prompt generated Umple 文本，因此只有 1 个可计 generated pair。其他 8 个无 generated 输出的 NL 中 7 个有 reference solution、1 个 ATAS 为纯 NL-only；它们都不可计为 $NL + STM_0$ generated pair。
- `unified-uml-multimodal-validation` 已全量抽取 Hugging Face parquet 的 999 行，其中 989 行是可回溯的有效 PlantUML 生成配对，10 行为 `No valid PlantUML code found.`，已列入 `excluded_pair_ids` 并排除；989 个 eligible row 的 NL exact / whitespace-normalized 去重后均唯一，不存在有限 NL 对多个 STM 的 1×N 形态。该数据是 synthetic 通用软件 feature-description → PlantUML state diagram，适合 smoke/stress，不应包装成真实控制系统需求。
- `fsm-bench-20` 目前是“仅流水线 / 需本项目复跑”：有 20 个系统、252 条 NL requirements（去重后仍为 252）、提示词、schema 和代码；`benchmark/gold/*.json` 是空 `{}` placeholder，作者未公开生成的 $STM_0$。
- 传统 use-case / statechart 工作当前只作论文级可重建线索或相关工作证据，不能进入现成 seed 池；若要统计论文示例 NL 数，必须另做人工全文抽取，不得混入一手资源主表。

## 4. 未列入登记表的既有条目处置

R2.0 只为 15 个重点条目建立 `seed_resource_registry.json`。其余既有目录并不因为“目录存在”而自动进入一手种子池；在补齐登记记录、`assets/`、哈希、定位器和 validator 之前，统一按下表处置，**可计生成数量均为 0**。本表的 `NL 数` / `NL-only` 是“当前已提交一手机读资源”的计数，不统计论文图示或可人工重建的示例；因此统一写 `0 / 未知` 与 `未知 / 未知`。后续若要升级任何条目，必须先补单条目 `seed_resource_registry.json`，再回写本文件主表。

| 条目 | 默认角色 | NL 数 | NL-only | 可计生成对 | 角色说明 | 原因摘要 |
|---|---:|---:|---:|---:|---|---|
| `beyond-scenarios-state-models` | ⚪ | 0 / 未知 | 未知 / 未知 | 0 | 论文级可重建线索 | 经典 use-case / state-model 文献，当前只有论文级证据；无一手机读生成配对。 |
| `completion-sysml-gwt` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | completion / repair-like 任务，依赖已有 partial model，不是当前 $NL \to STM_0$ 种子。 |
| `executable-state-machines-structured-text` | ⚪ | 0 / 未知 | 未知 / 未知 | 0 | 论文级可重建线索 | 结构化文本 / SPS 路径需要论文级重建；无作者原生配对包。 |
| `executable-use-cases-domain-machine-specifications` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | 仅 BibTeX / 元数据，全文与一手配对仍受阻。 |
| `execution-nl-req-bt-sm` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | $NL \to BT \to SM$ 中间链路；BT / SM 原生数据包未冻结。 |
| `fsm-gen-iec-61499` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | IEC 61499 / refinement 边界，初始 $STM_0$ 与后续 refinement 难隔离，私有制品未公开。 |
| `ijisrt-uml-state-diagrams-llm` | ⚪ | 0 / 未知 | 未知 / 未知 | 0 | 论文级可重建线索 | 只有论文示例 / prompt 级线索，无一手生成配对发布包。 |
| `integrating-graphical-nl-specifications` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | NL 与 graphical notation 共现，不是 $NL \to STM_0$ 输出资源。 |
| `most-states-modes` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | MoSt / NuSMV 非目标 STM family；只作形式化相关工作。 |
| `nl-standard-docs-state-machines` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | 标准 / 协议式文档边界，原始输出包未公开。 |
| `nlp-req-formalization-testcase-generation` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | IRDL / testcase / sequence 中间链路，不是可直接入池的生成 $STM_0$。 |
| `pushing-generative-envelope-mbse` | ⚪ | 0 / 未知 | 未知 / 未知 | 0 | 论文级可重建线索 | 论文级 MBSE / SysML 线索；无一手生成配对发布包。 |
| `req-mermaid-statechart` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | 任务贴合但数据 / 输出私有，不可复验。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | scenario / statechart co-evolution 或反向边界，不是当前 seed。 |
| `scenarios-statecharts-interrelated` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | scenario / event trace 输入边界，非自然语言需求唯一输入。 |
| `semi-auto-efsm-standard-docs` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | 标准文档 / EFSM 边界，case 数据 / 生成 EFSM 包未公开。 |
| `specification-based-verification-usecase-sm` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | state machine 是验证执行机制，不是目标生成种子。 |
| `towards-automatic-model-completion` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | model completion / repair-only，依赖 partial SMD。 |
| `ttool-ai-smd-subset` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | SysML SMD / timing / 私有制品边界；当前不提供一手生成配对。 |
| `umple-nl-state-machine` | ⚪ | 0 / 未知 | 未知 / 未知 | 0 | 论文级可重建线索 | 论文级 Umple / NL 示例可重建；无一手生成配对发布包。 |
| `web-tool-goal-statechart-derivation` | 🔴 | 0 / 未知 | 未知 / 未知 | 0 | 相关但不入池 | goal model / requirements view 输入，不是 NL-only 生成 $STM_0$。 |
