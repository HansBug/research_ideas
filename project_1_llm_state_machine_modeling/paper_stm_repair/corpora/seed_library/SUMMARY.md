# seed_library/SUMMARY.md

## 1. 当前状态一句话

本 SUMMARY 是 PR-R1.8-B 迁移后的 seed library 当前横向事实真源；它承接 R1.7 bounded snapshot v4，而不是全域 census。旧 `seed_corpus/` 的横向 ledgers 与 raw search 已归档到 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/)，当前事实以本文件和 24 个单条目目录为准。

核心口径：seed library 记录上游 `NL -> STM_0` 方法 / 来源集合，不是本论文 `STM_0 -> STM_k` repair baseline；R2 四例样本还需要后续 case-level freeze。

## 2. 关键统计表

| 指标 | 数量 | 可复算位置 | caveat |
|---|---:|---|---|
| 去重候选 | 47 | §5 候选全集摘要表；[archive/legacy_ledgers/candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/candidate_matrix.md) | R1.7 bounded snapshot v4。 |
| screening 入账 | 47 | [archive/legacy_ledgers/screening_ledger.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/screening_ledger.md)；§13 迁移表 | 与候选 ID 一一对应。 |
| 单条目全文 / artifact 目录 | 24 | §7 资产表；`find corpora/seed_library -mindepth 1 -maxdepth 1 -type d` | `fsm-bench-20` 是 artifact-only。 |
| R1.7 search round 哨兵 | 8 | §10 搜索覆盖摘要；[archive/search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/) | archive 另含 R1.6 与早期 search 记录。 |
| 旧九 direct generation baseline crosswalk | 9/9 | §7 旧九 crosswalk；[archive/legacy_ledgers/baseline_seed_method_crosswalk.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/baseline_seed_method_crosswalk.md) | 这是 seed 方法集合，不是 repair baseline。 |
| R2 主 / 条件主可计候选 | 4 | §4 / §6；候选表 `计数资格=yes-main/yes-conditional` | 2 强主 + 2 条件主，仍需 R2 裁决。 |
| manual queue 状态 | 2 / 2 / 10 / 2 | §8 manual queue | downloaded/excluded；excluded-by-metadata；still-blocked；new-manual-pending。 |

## 3. seed 定义与分级口径

| 概念 | 口径 |
|---|---|
| strict seed | 有证据表明 `STM_0` 由自然语言需求 / 用例 / 场景 / 系统描述 / 文本规格生成、派生、抽取或人工建模得到。 |
| 目标 STM family | T0 范围内 FSM / HSM / EFSM / statechart；关键 timed / hybrid / protocol / process 行为不可隔离时不计主 seed。 |
| `SS` | 文献资格：`SS-A` 强 seed，`SS-B` 条件 seed，`ES-C` 扩展 / 边界，`NN-D` 不满足，`EX-E` 排除。 |
| `SA` | artifact 可用性：`SA-1/SA-2` 可考虑实验；`SA-3` paper-only；`SA-4` private；`SA-5` blocked / no artifact。 |
| 计数资格 | 只有 `yes-main` / `yes-conditional` 进入当前 R2 主 / 条件主候选计数。 |

## 4. R2 handoff 分组

| 分组 | 候选 | 当前用途 |
|---|---|---|
| 强主 seed 候选 | `sefm-llm-state-machine`、`llms-emp-stm-subset` | 最优先进入 R2 四例候选池；仍需冻结 artifact、license/hash、输入输出切片。 |
| 条件主 seed 候选 | `designing-fsm-gpt4`、`unified-uml-multimodal-validation` | 可补足四例候选数；前者必须 initial-generation-only，后者必须标 synthetic / license caveat。 |
| pipeline fallback | `fsm-bench-20` | 任务关系强、MIT / Zenodo / GitHub 可用；但 generated `STM_0` outputs 未公开冻结，需要 R2 复跑。 |
| paper-only strict / conditional evidence | `nlp-req-formalization-testcase-generation`、`statistical-usage-testing-uml`、`unified-use-case-statecharts`、`statechart-codesign-usecases`、`object-models-uml-embedded`、`pushing-generative-envelope-mbse` 等 | related work、manual reconstruction 线索和 strict gate 论证；不计 R2 主 seed。 |
| extended / converter pressure | `ttool-ai-smd-subset`、`fsm-gen-iec-61499` | 对 converter、控制系统相关性和 feedback story 有价值，但因 timing / private artifact / intermediate boundary 不计主 seed。 |
| protocol-domain seed method / hard exclusion sentinel | `protocol-flowfsm-sentinel`、`3gpp-protocol-sentinel` 及其他 protocol / sequence / completion / formal-spec sentinel | 保留为方法证据和防误收证据，不计控制系统四例。 |

## 5. 候选全集摘要表（47 行）

本表是当前候选全集的 SUMMARY-first 摘要，覆盖 #109 §4.1 要求的字段组：元数据、NL 输入、STM 输出、生成关系、资产 / license 指针、实验角色、分级风险和证据指针。更细的历史原表见 [archive/legacy_ledgers/candidate_matrix.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/candidate_matrix.md)。

| seed_id | 年份 | 来源批次 | NL 输入 | STM 输出 / T0 caveat | 生成关系 / actor | SS/SA | 计数资格 | 角色 / 风险 | 证据 |
|---|---:|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | 2026 | baseline / reproduction | non-structured system descriptions | UML state machine / statechart；T0 | explicit NL->STM；LLM=yes | SS-A/SA-2 | yes-main | R2 seed candidate / near comparison；R2 前需冻结 artifact、license/hash、逐 case T0 边界 | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | 2024 | baseline / reproduction | natural-language requirements / prompts | SysML / PlantUML STM subset；T0 | explicit requirements->STM for STM subset；LLM=yes | SS-A/SA-2 | yes-main | R2 seed candidate / judge calibration；只允许 STM 子集；ACT/SD 排除；pipeline 需自建 | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | 2026 | baseline | synthetic NL requirements | DFSM / Mealy CSV；T0 | explicit NL->DFSM initial generation; repair excluded；LLM=yes | SS-B/SA-2 | yes-conditional | conditional R2 seed / initial-generation-only；只冻结初始 NL->DFSM/Mealy CSV；repair/oracle/fault-model 部分排除 | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | 2026 | R1.6 LLM/recent fulltext + HF artifact | synthetic user-focused requirements / feature descriptions | PlantUML state diagrams subset；T0 | LLaMA-generated requirement -> DeepSeek PlantUML state diagram；LLM=yes | SS-B/SA-2 | yes-conditional | conditional R2 seed candidate / synthetic boundary；R2 前需 row-level parse/render 抽检与 license caveat | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |
| `fsm-bench-20` | 2026 | R1.6 LLM/recent + Zenodo/GitHub | 20 natural-language software requirement sets | deterministic FSM JSON / EFSM-like guarded FSM；T0 schema / output missing | explicit NL requirements -> deterministic FSM JSON pipeline；LLM=yes | SS-A/SA-2 | no-pipeline-output-missing | conditional pipeline seed / R2 rerun candidate；不直接计四例；SA-2 仅指 pipeline artifact 可冻结，generated `STM_0` outputs 需复跑或找到公开归档后升级 | [seed_desc](./fsm-bench-20/seed_desc.md) |
| `ttool-ai-smd-subset` | 2024 | baseline / reproduction | NL system specification | SysML state-machine diagram subset；timed-SMD caveat | NL->SysML joint model, SMD subset；LLM=yes | ES-C/SA-2 | no-eligibility | converter pressure / timed boundary；当前不计主 seed；需 case-level T0 isolation 或 PR-R3 timing 规范化后才可升级 | [seed_desc](./ttool-ai-smd-subset/seed_desc.md) |
| `fsm-gen-iec-61499` | 2025 | baseline / R1.6 fulltext | industrial automation NL requirements + I/O interface | FSM / IEC 61499 ECC function block；T0? IEC 61499 boundary | LLM initial FSM + iterative refinement；LLM=yes | SS-B/SA-4 | no-artifact | strong related work / private-artifact boundary；不计主 seed；initial STM 与迭代/用户反馈难隔离 | [seed_desc](./fsm-gen-iec-61499/seed_desc.md) |
| `ijisrt-uml-state-diagrams-llm` | 2026 | R1.6 LLM/recent fulltext | textual system descriptions / prompts | UML 2.5 state diagrams / PlantUML；T0 | LLM prompt -> PlantUML state diagram；LLM=yes | SS-A/SA-3 | no-artifact | recent related work / paper-only seed evidence；不计主 seed；案例偏 toy 且无 raw outputs | [seed_desc](./ijisrt-uml-state-diagrams-llm/seed_desc.md) |
| `umple-nl-state-machine` | 2024 | baseline | short requirements | Umple state machine；T0 | explicit requirements->Umple SM；LLM=yes | SS-A/SA-3 | no-artifact | literature evidence / related work；不计入 R2 主 seed 下限，除非另行重建 artifact | [seed_desc](./umple-nl-state-machine/seed_desc.md) |
| `req-mermaid-statechart` | 2025 | baseline | automotive product-function requirements | Mermaid.js statechart；T0? | NL->Mermaid statechart；LLM=yes | SS-B/SA-4 | no-artifact | related work / private-data boundary；任务贴合但私有数据不可复验；不计 R2 主 seed 下限 | [seed_desc](./req-mermaid-statechart/seed_desc.md) |
| `pushing-generative-envelope-mbse` | 2025 | baseline / paper-only seed method | air purifier / vacuum natural-language MBSE prompts | SysML v2 state machine diagrams / requirements list；T0 | prompt/temperature-driven NL -> STM-family generation；LLM=yes | SS-B/SA-3 | no-artifact | paper-only seed method evidence / prompt-temperature reference；无公开逐次输出包、代码、数据包或 license；仅 paper-level reconstructible | [seed_desc](./pushing-generative-envelope-mbse/seed_desc.md) |
| `from-use-cases-to-statecharts` | 2001 | baseline | natural-language use cases | UML statecharts；T0 with timing caveat | use-case->statechart derivation；LLM=no | SS-B/SA-3 | no-artifact | classic literature / manual example；statechart 是中间产物；不计 R2 主 seed 下限 | [seed_desc](./from-use-cases-to-statecharts/seed_desc.md) |
| `beyond-scenarios-state-models` | 2004 | baseline | restricted English use cases + domain model | hierarchical finite state transition machine；T0 | use-case->state model algorithm；LLM=no | SS-B/SA-3 | no-artifact | classic literature / not R2 main；paper_content 乱码，主要证据来自 PDF 页面核验；不计 R2 主 seed 下限 | [seed_desc](./beyond-scenarios-state-models/seed_desc.md) |
| `executable-state-machines-structured-text` | 2019 | baseline | structured textual requirements / SPS | executable FSM；T0 | structured text->executable FSM；LLM=no | SS-B/SA-3 | no-artifact | classic weak seed / related work；NL->SPS 是人工步骤；不计 R2 主 seed 下限 | [seed_desc](./executable-state-machines-structured-text/seed_desc.md) |
| `maritaca-use-case-behavior-models` | 2017 | R1.6 classic search | semi-structured textual use case descriptions | state machine models；T0? | NLP extraction of state machines from use cases；LLM=no | SS-B?/SA-5 | no-artifact | classic manual queue / weak seed；需 IEEE PDF；无 artifact 前不计主 seed | https://doi.org/10.1109/DSN-W.2017.33 |
| `dependable-product-families-usecases-state-machines` | 2016 | R1.6 classic search | restricted use cases with variability / exceptions | state machine model；T0? variability boundary | automatic extraction from use-case modeling；LLM=no | SS-B?/SA-5 | no-artifact | classic manual queue / product-family boundary；需 IEEE PDF；variability 是否可隔离待核 | https://doi.org/10.1109/LADC.2016.28 |
| `automated-transition-use-cases-uml-sm` | 2011 | external | use cases | UML state machines；T0 | use-case->UML SM；LLM=no | SS-B?/SA-5 | no-artifact | classic use-case candidate / manual queue；需下载全文确认输出与 use-case 格式；无 artifact 前不计主 seed | https://doi.org/10.1007/978-3-642-21470-7_9 |
| `execution-nl-req-bt-sm` | 2012 | external | NL requirements | state machines via behavior trees；T0? | NL->BT->SM；LLM=no | ES-C/SA-4? | no-artifact | extended seed / BT intermediate boundary；需人工下载 JSS PDF；BT intermediate 与 artifact 缺失使其不计主 seed | https://doi.org/10.1016/j.jss.2012.06.013 |
| `completion-sysml-gwt` | 2024 | external / baseline / R1.6 fulltext | GWT requirements + partial SysML model / pre-existing states | SysML state machine transitions；T0? | completion / partial-model refinement；LLM=no | NN-D/SA-3 | no-artifact | completion boundary / related work；`X_REPAIR_ONLY` confirmed：依赖已有 partial model，不计 strict seed | [seed_desc](./completion-sysml-gwt/seed_desc.md) |
| `towards-automatic-model-completion` | 2022 | R1.7 manual queue recheck | GWT requirements + partial SysML model / partial SMD | completed SysML state-machine fragments；N/A / repair-only | partial-model completion, not initial NL->STM；LLM=no | NN-D/SA-3 | no-artifact | completion / repair-only boundary；`X_REPAIR_ONLY` confirmed：已有 partial model 输入，不计 strict seed | [seed_desc](./towards-automatic-model-completion/seed_desc.md) |
| `scenarios-statecharts-interrelated` | 待核 | baseline | OMT event trace diagrams / structured scenarios | statecharts；T0 | structured scenario->statechart；LLM=no | NN-D/SA-3 | no-artifact | exclusion sentinel / snowball boundary；P1 失败：输入不是自然语言需求文本，触发结构化 scenario 边界 | [seed_desc](./scenarios-statecharts-interrelated/seed_desc.md) |
| `generating-statechart-designs-from-scenarios` | 2000 | external | UML sequence diagrams / scenarios | statecharts；T0 | sequence/scenario->statechart；LLM=no | NN-D/SA-3? | no-artifact | sequence-class exclusion sentinel；`X_SEQUENCE_CLASS`：输入不是 NL requirements；R1.6 已移出人工下载主队列 | https://doi.org/10.1145/337180.337217 |
| `synthesis-revisited-scenario-based` | 2005 | external / baseline | LSC / MSC-style formal scenario | statecharts；T0 | formal scenario->statechart；LLM=no | NN-D/SA-3 | no-artifact | formal scenario boundary；`X_FORMAL_SPEC` / `X_SEQUENCE_CLASS`：不计 strict seed | https://doi.org/10.1007/978-3-540-31847-7_18 |
| `requirements-analysis-prototyping-scenarios-statecharts` | 待核 | external | scenarios / statechart co-evolution | statecharts；T0? | statechart->scenarios or co-evolution；LLM=no | NN-D/SA-3? | no-artifact | co-exist / direction boundary；当前更像 statechart -> scenario/prototype，不是 NL->STM | external scout; Wayback PDF line |
| `nl-standard-docs-state-machines` | 2018 | external | natural-language standard documents | state machines；T0? protocol/standard risk | standard text extraction；LLM=no/unknown | NN-D/pending/SA-5 | no-artifact | standard/protocol sentinel；确认是否 standard/protocol extraction；不作为主 seed | https://doi.org/10.2514/1.I010525 |
| `semi-auto-efsm-standard-docs` | 2015 | R1.6 classic/protocol search | natural-language standard documents | EFSM；T0? protocol/standard risk | semi-automatic extraction；LLM=no | NN-D/pending/SA-5 | no-artifact | standard/protocol sentinel；除非证明是控制标准例外，否则不计主 seed | https://doi.org/10.1109/DSN-W.2015.17 |
| `statechart-use-case-validation-event-driven` | 2012 | R1.6 Crossref refined search | use-case models | statecharts? validation artifact；T0? | validation vs generation pending；LLM=no | pending/SA-5 | no-artifact | generation-vs-validation boundary；确认是否生成 statechart；当前不计 | https://doi.org/10.1145/2245276.2231947 |
| `rscharter-statechart-elements` | 待核 | R1.6 Crossref refined search | requirements specification | statechart diagram elements；T0? | requirements -> statechart elements extraction；LLM=no/unknown | pending/SA-5 | no-artifact | new search candidate / manual queue；需 SSRN 全文确认输出是否完整 STM | https://doi.org/10.2139/ssrn.4964857 |
| `most-states-modes` | 2024 | external | NL requirements | states/modes formal model；T0?/formal | formalization；LLM=no | ES-C/NN-D/SA-3? | no-artifact | related work；需查是否输出 STM family | external search planner |
| `sysmlv2-formalized-requirements` | 2025 | external / baseline | requirements + temporal logic | SysML v2 state machine?；T1+/formal risk | formalization；LLM=no/LLM? | ES-C/SA-3? | no-artifact | extended / boundary；LTL/formalization 风险高 | `baselines/enhancing-model-based-development-formalized-requirements/` |
| `protocol-flowfsm-sentinel` | 2024 | baseline / protocol-domain seed method | RFC / protocol text | protocol FSM / rulebook / states-transitions；T0? protocol | RFC text -> protocol FSM extraction；LLM=yes | NN-D/SA-3/SA-5 | no-artifact | protocol-domain seed method / exclusion sentinel for control-system four examples；`X_PROTOCOL`：不计控制系统四例，但不可从 seed 方法集合消失 | `baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/`; alias `protocol-flowfsm-seed-method` in §7.1 旧九 crosswalk |
| `3gpp-protocol-sentinel` | 2024 | baseline / protocol-domain seed method | 3GPP specification text | protocol FSM with states / conditions / actions / transitions；T0? protocol | standard text -> protocol FSM extraction；LLM=maybe | NN-D/SA-3/SA-5 | no-artifact | protocol-domain seed method / exclusion sentinel for control-system four examples；`X_PROTOCOL`：不计控制系统四例，但保留 ensemble / span-grounded extraction 方法证据 | `baselines/automated-extraction-protocol-state-machines-3gpp-specifications/`; alias `specgpt-3gpp-seed-method` in §7.1 旧九 crosswalk |
| `source-autonomous-driving-hsm` | 待核 | sources | system description | HSM；T0 | source pool; generation by this project if used；LLM=no | pending-source/SA-2? | no-project-constructed | source candidate / possible student seed；sources 不自动等于 strict seed | sources scout |
| `source-rotorcraft-uas-hsm` | 待核 | sources | system description | HSM；T0 | source pool; generation by this project if used；LLM=no | pending-source/SA-2? | no-project-constructed | source candidate；需构造 STM0 并防泄漏 | sources scout |
| `source-smarthand-hsm` | 待核 | sources | system description | HSM；T0 | source pool; generation by this project if used；LLM=no | pending-source/SA-2? | no-project-constructed | source candidate；需查目录名与证据 | sources scout |
| `source-hfsm-human-robot` | 待核 | sources | system description | HSM；T0 | source pool; generation by this project if used；LLM=no | pending-source/SA-2? | no-project-constructed | source candidate；需构造 STM0 | sources scout |
| `source-avp-hsm` | 待核 | sources | system description | HSM；T0 | source pool; generation by this project if used；LLM=no | pending-source/SA-2? | no-project-constructed | source candidate；需防停车趋同 | sources scout |
| `nlp-req-formalization-testcase-generation` | 2021 | R1.7 CEUR fulltext wave | natural-language functional requirements / text documents | IRDL requirement model -> UML state machine -> test cases；T0 state machine after IRDL/sequence intermediate | semi-automated NL requirements -> IRDL -> UML state machine；LLM=no | SS-B/SA-3 | no-artifact | strong paper-only seed evidence / test-generation boundary；不计主 seed；intermediate IRDL/sequence + no machine-readable output | [seed_desc](./nlp-req-formalization-testcase-generation/seed_desc.md) |
| `statistical-usage-testing-uml` | 2003 | R1.7 classic fulltext wave | textual/tabular UML use case + domain class model | UML state chart / state machine / usage graph；T0 | textual use case -> structured use case -> state diagram；LLM=no | SS-B/SA-3 | no-artifact | paper-only strict literature evidence / manual reconstruction；不计主 seed；requires refinement/domain model and lacks artifact | [seed_desc](./statistical-usage-testing-uml/seed_desc.md) |
| `unified-use-case-statecharts` | 2007 | R1.7 classic fulltext wave | use cases in SRS | unified UC statechart；T0 | manual UCUM use-case unification -> statechart；LLM=no | SS-B/SA-3 | no-artifact | classic paper-only / manual unified UC statechart seed；不计主 seed；manual/case-study method and no machine-readable artifact | [seed_desc](./unified-use-case-statecharts/seed_desc.md) |
| `statechart-codesign-usecases` | 2003 | R1.7 classic fulltext wave | use cases / use case diagram | statechart / sub-statecharts / top-level statechart；T0 | direct use-case -> statechart route plus sequence-diagram route；LLM=no | SS-B/SA-3 | no-artifact | embedded co-design paper-only boundary；不计主 seed；sequence-diagram route and manual method caveat | [seed_desc](./statechart-codesign-usecases/seed_desc.md) |
| `object-models-uml-embedded` | 2004 | R1.7 classic fulltext wave | textual use case description | UML statechart / extended statechart；T0 | convert use case into a statechart then identify objects；LLM=no | SS-B/SA-3 | no-artifact | embedded use-case-to-statechart paper-only evidence；不计主 seed；object-model goal and no artifact | [seed_desc](./object-models-uml-embedded/seed_desc.md) |
| `integrating-graphical-nl-specifications` | 2016 | R1.7 boundary fulltext wave | NL requirements + existing graphical notation | statechart / graphical notation is input not output；N/A / co-exist | graphical notation + NL -> LDG/test model, not NL->STM；LLM=no | NN-D/SA-3 | no-artifact | boundary negative / NL-GN integration related work；`X_COEXIST_ONLY`; prevents co-exist-only false positives | [seed_desc](./integrating-graphical-nl-specifications/seed_desc.md) |
| `specification-based-verification-usecase-sm` | 2008 | R1.7 boundary fulltext wave | semi-formal textual use cases | verification state machine inside SystemC testbench；N/A / testbench-only | use case spec -> testbench/test cases; state machine is not target STM；LLM=no | NN-D/SA-3 | no-artifact | testbench boundary / related work；`X_COEXIST_ONLY`; verification state machine is execution mechanism | [seed_desc](./specification-based-verification-usecase-sm/seed_desc.md) |
| `executable-use-cases-domain-machine-specifications` | 2004 | R1.7 Crossref/DBLP manual candidate | executable use cases / application-domain requirements | machine specifications / possible state-machine-adjacent；unknown | possible link from use cases to machine specs；LLM=no | pending/SA-5 | no-artifact | new manual candidate / direction boundary；需人工全文确认是否输出 STM family | Crossref round; DOI https://doi.org/10.1049/ic:20040231 |
| `web-tool-goal-statechart-derivation` | 2015 | R1.7 Crossref/DBLP manual candidate | goal models / requirements model | statechart derivation；T0? goal-model boundary | goal model -> statechart derivation, not necessarily NL input；LLM=no | NN-D/pending/SA-5 | no-artifact | goal-model/statechart boundary；可能触发 `X_SEQUENCE_ONLY` / non-NL input；需全文确认 | Crossref round; DOI https://doi.org/10.1109/RE.2015.7320444 |
| `ucgen-usecase-descriptions` | 2026 | R1.7 Crossref negative | requirements specification | use case textual descriptions；N/A | requirements -> use case text, no STM output；LLM=yes | EX-E/SA-5 | no-artifact | negative sentinel / output-not-STM；`X_NON_STM_FORMALISM`/non-STM output；不进入 seed | Crossref textual usecase round |

## 6. R2 handoff / 可计候选表

| seed_id | NL公开/唯一性 | STM格式/T0 | actor/LLM | raw/code/data/license/hash | oracle/repair泄漏 | 转换风险 | 资格 | 证据 |
|---|---|---|---|---|---|---|---|---|
| `sefm-llm-state-machine` | non-structured system descriptions；公开性见 artifacts | UML state machine / statechart；T0 | explicit NL->STM；LLM=yes | 4open artifact 可用但 license/release/commit 待冻结；local + 4open | medium；R2 前需冻结 artifact、license/hash、逐 case T0 边界 | semi-automatic | yes-main | [seed_desc](./sefm-llm-state-machine/seed_desc.md) |
| `llms-emp-stm-subset` | natural-language requirements / prompts；公开性见 artifacts | SysML / PlantUML STM subset；T0 | explicit requirements->STM for STM subset；LLM=yes | data/results 可用，pipeline code/license 待核；local + Drive | medium；只允许 STM 子集；ACT/SD 排除；pipeline 需自建 | semi-automatic | yes-main | [seed_desc](./llms-emp-stm-subset/seed_desc.md) |
| `designing-fsm-gpt4` | synthetic NL requirements；公开性见 artifacts | DFSM / Mealy CSV；T0 | explicit NL->DFSM initial generation; repair excluded；LLM=yes | GitHub repo exists, no release/license；local + GitHub | high；只冻结初始 NL->DFSM/Mealy CSV；repair/oracle/fault-model 部分排除 | deterministic-ish CSV | yes-conditional | [seed_desc](./designing-fsm-gpt4/seed_desc.md) |
| `unified-uml-multimodal-validation` | synthetic user-focused requirements / feature descriptions；公开性见 artifacts | PlantUML state diagrams subset；T0 | LLaMA-generated requirement -> DeepSeek PlantUML state diagram；LLM=yes | HF public parquet; 999 state rows; license unclear；DOI + HF sha | medium；R2 前需 row-level parse/render 抽检与 license caveat | machine-readable PlantUML | yes-conditional | [seed_desc](./unified-uml-multimodal-validation/seed_desc.md) |

## 7. 旧九 generation baseline crosswalk 与 24 目录资产表

### 7.1 旧九 generation baseline crosswalk（9/9）

| 原 baseline | seed 方法 ID | 矩阵 ID / 当前目录 | 输入 NL | 输出 STM | 方法 / LLM | 原装 pair 可获取性 | R2 当前用途 |
|---|---|---|---|---|---|---|---|
| Structure- and Event-Driven Frameworks | ``sefm-llm-state-machine`` |  | 8 个非结构化 reactive-system / system descriptions | UML state machine / statechart，含 reference solutions 和多策略生成结果 | LLM；single prompt、structure-driven、event-driven、hybrid strategy；有生成策略但不是 repair loop |  /  | 强主 seed 候选；优先进入 PR-R2 裁决 |
| LLMS EMP / SysML Behavior Models | ``llms-emp-stm-subset`` |  | 107 个 SysML 行为模型需求描述；只取 `diagram_type=stm` 子集 | PlantUML / SysML STM；ACT/SD 必须排除 | LLM；requirements + prompt；论文含 checking / feedback-regeneration 设计，但公开代码不足 |  /  | 强主 seed 候选；STM 子集 seed / judge calibration |
| Designing FSM with GPT-4 | ``designing-fsm-gpt4`` |  | 合成英文 DFSM / Mealy 需求描述 | CSV DFSM / Mealy machine | GPT-4/GPT-4o；初始生成 + oracle / checking / repair 实验；seed 只能取 initial generation |  /  | 条件主 seed；initial-generation-only，强防泄漏 |
| TTool-AI | ``ttool-ai-smd-subset`` |  | platooning、spacebasedsystem、AutomatedBraking 等自然语言系统规范 | SysML/TTool state-machine diagram subset；同时含 BD/IBD 等非 STM | ChatGPT 3.5；TTool-AI 自动反馈循环、语法/语义检查、JSON→TTool XML |  /  | converter pressure / 条件 seed 方法；R3 定义 SMD/timing 处理后可重裁 |
| Umple thesis | ``umple-nl-state-machine`` |  | 5 个自然语言 requirements 系统：Blackjack、Course Section、Credit Card、Driver License、Hotel Stay | Umple textual state machine code | Llama 3；zero-shot、one-shot、RAG；无自动 repair loop |  /  | paper-only seed evidence / 手工重建线索 |
| REQ automotive thesis | ``req-mermaid-statechart`` |  | Volvo Cars / Car Weaver 产品功能自然语言需求 | Mermaid.js statechart | GPT-3.5/GPT-4/GPT-4o；含数据增强 / 微调 / prompt 生成；无公开闭环资产 |  /  | private-data seed method / related work；不进主四例 |
| Pushing the Generative Envelope | ``pushing-generative-envelope-mbse`` |  | air purifier、vacuum 两个简短自然语言 MBSE 题项 | SysML v2 state machine diagrams，同时生成 requirements list | local LLM；Mixtral-8x7B-Instruct、Llama-3-Smaug-8B；zero/one/few-shot、CoT、temperature 消融；无 feedback loop |  /  | paper-only seed method evidence；prompt/temperature 变量参考 |
| FlowFSM / Agentic Flow | ``protocol-flowfsm-seed-method`` |  | RFC 自然语言协议文档，FTP / RTSP | protocol FSM / command rulebook / states-transitions | LLM agent / CrewAI；prompt chaining、CoT、command extraction→transition analysis→rulebook synthesis |  /  | protocol-domain seed method；长文档/agentic extraction 参考，不默认进控制系统四例 |
| SpecGPT / 3GPP extraction | ``specgpt-3gpp-seed-method`` |  | 3GPP Release 17 NAS / NGAP / PFCP 自然语言/半结构化标准文档 | protocol FSM，含状态、condition/action、转移 | GPT-4o、DeepSeek V3、Qwen Turbo、Claude Sonnet 4、Gemini 2.5 Pro；CoT/few-shot/context stitching/ensemble |  /  | protocol-domain seed method；ensemble / span grounding 方法参考，不默认进控制系统四例 |

### 7.2 24 个单条目目录资产表

| slug | paper.pdf | paper_content.txt | bibtex.bib | seed_desc.md | artifacts.md | 说明 |
|---|---:|---:|---:|---:|---:|---|
| `beyond-scenarios-state-models` | Y | Y | Y | Y | Y | - |
| `completion-sysml-gwt` | Y | Y | Y | Y | Y | - |
| `designing-fsm-gpt4` | Y | Y | Y | Y | Y | - |
| `executable-state-machines-structured-text` | Y | Y | Y | Y | Y | - |
| `from-use-cases-to-statecharts` | Y | Y | Y | Y | Y | - |
| `fsm-bench-20` | N | N | Y | Y | Y | artifact-only / pipeline fallback |
| `fsm-gen-iec-61499` | Y | Y | Y | Y | Y | - |
| `ijisrt-uml-state-diagrams-llm` | Y | Y | Y | Y | Y | - |
| `integrating-graphical-nl-specifications` | Y | Y | Y | Y | Y | - |
| `llms-emp-stm-subset` | Y | Y | Y | Y | Y | - |
| `nlp-req-formalization-testcase-generation` | Y | Y | Y | Y | Y | - |
| `object-models-uml-embedded` | Y | Y | Y | Y | Y | - |
| `pushing-generative-envelope-mbse` | Y | Y | Y | Y | Y | - |
| `req-mermaid-statechart` | Y | Y | Y | Y | Y | - |
| `scenarios-statecharts-interrelated` | Y | Y | Y | Y | Y | - |
| `sefm-llm-state-machine` | Y | Y | Y | Y | Y | - |
| `specification-based-verification-usecase-sm` | Y | Y | Y | Y | Y | - |
| `statechart-codesign-usecases` | Y | Y | Y | Y | Y | - |
| `statistical-usage-testing-uml` | Y | Y | Y | Y | Y | - |
| `towards-automatic-model-completion` | Y | Y | Y | Y | Y | - |
| `ttool-ai-smd-subset` | Y | Y | Y | Y | Y | - |
| `umple-nl-state-machine` | Y | Y | Y | Y | Y | - |
| `unified-uml-multimodal-validation` | Y | Y | Y | Y | Y | HF dataset files |
| `unified-use-case-statecharts` | Y | Y | Y | Y | Y | - |

## 8. manual queue / blocker

### 8.1 状态分布

| 状态 | 数量 | ID | R2影响 |
|---|---:|---|---|
| downloaded / excluded | 2 | `completion-sysml-gwt`、`towards-automatic-model-completion` | 已有全文并确认为 repair-only，不阻塞 R2。 |
| excluded by metadata | 2 | `generating-statechart-designs-from-scenarios`、`ucgen-usecase-descriptions` | 元数据已足够排除，不阻塞 R2。 |
| still-blocked | 10 | `automated-transition-use-cases-uml-sm`、`execution-nl-req-bt-sm`、`maritaca-use-case-behavior-models`、`dependable-product-families-usecases-state-machines`、`statechart-use-case-validation-event-driven`、`semi-auto-efsm-standard-docs`、`rscharter-statechart-elements`、`nl-standard-docs-state-machines`、`requirements-analysis-prototyping-scenarios-statecharts`、`most-states-modes` | 可后续人工下载 / related work，不应阻塞 R2。 |
| new-manual-pending | 2 | `executable-use-cases-domain-machine-specifications`、`web-tool-goal-statechart-derivation` | 新候选待人工全文确认，不作为 R2 blocker。 |

### 8.2 当前 pending 明细

| ID | 标题 | 来源 URL | 状态 |
|---|---|---|---|
| `automated-transition-use-cases-uml-sm` | Automated Transition from Use Cases to UML State Machines to Support State-Based Testing | https://doi.org/10.1007/978-3-642-21470-7_9 | still-blocked：Springer paywall / 未发现公开 artifact；PR-R2 可暂不依赖。 |
| `execution-nl-req-bt-sm` | Execution of Natural Language Requirements using State Machines Synthesised from Behavior Trees | https://doi.org/10.1016/j.jss.2012.06.013 | still-blocked：ScienceDirect 访问受限；BT intermediate 使其不作为主 seed。 |
| `maritaca-use-case-behavior-models` | MARITACA: From Textual Use Case Descriptions to Behavior Models | https://doi.org/10.1109/DSN-W.2017.33 | still-blocked：IEEE paywall / artifact not found；高优先人工下载。 |
| `dependable-product-families-usecases-state-machines` | Modeling Dependable Product-Families: From Use Cases to State Machine Models | https://doi.org/10.1109/LADC.2016.28 | still-blocked：IEEE paywall / artifact not found。 |
| `statechart-use-case-validation-event-driven` | Statechart-based use case requirement validation of event-driven systems | https://doi.org/10.1145/2245276.2231947 | still-blocked：ACM paywall / generation-vs-validation boundary。 |
| `semi-auto-efsm-standard-docs` | Semi-automatic Generation of Extended Finite State Machines from Natural Language Standard Documents | https://doi.org/10.1109/DSN-W.2015.17 | still-blocked：IEEE paywall；默认 standard/protocol sentinel。 |
| `rscharter-statechart-elements` | Rscharter: A Framework for Extracting Statechart Diagram Elements from the Requirements Specification | https://doi.org/10.2139/ssrn.4964857 | still-blocked / public-OA-browser：SSRN CLI 403；需人工浏览器下载。 |
| `nl-standard-docs-state-machines` | From Natural Language Standard Documents to State Machines: Advantages and Drawbacks | https://doi.org/10.2514/1.I010525 | still-blocked：AIAA 访问受限；默认 standard/protocol sentinel。 |
| `requirements-analysis-prototyping-scenarios-statecharts` | Requirements Analysis and Prototyping Using Scenarios and Statecharts | 待定位 | still-blocked / low priority：正式 PDF 未定位；方向疑似反。 |
| `most-states-modes` | Modeling and Verification of Natural Language Requirements based on States and Modes | https://doi.org/10.1145/3640822 | still-blocked / public-OA-browser：ACM/HAL CLI 受阻；默认 related-work 不计 seed。 |
| `executable-use-cases-domain-machine-specifications` | Executable use cases as links between application domain requirements and machine specifications | https://doi.org/10.1049/ic:20040231 | new-manual-pending：publisher closed；非 R2 blocker。 |
| `web-tool-goal-statechart-derivation` | Web tool for Goal modelling and statechart derivation | https://doi.org/10.1109/RE.2015.7320444 | new-manual-pending：IEEE closed；需确认 input 是否 NL。 |

## 9. negative evidence / hard exclusion

### 9.1 排除码口径

| 排除码 | 常用别名 | 含义 |
|---|---|---|
| `X_PROTOCOL_FSM` | `X_PROTOCOL` | RFC / 3GPP / network protocol FSM 或 standard/protocol 风险。 |
| `X_PROCESS_MODEL` | `X_PROCESS` | BPMN / workflow / business process / resource-flow。 |
| `X_NON_STM_FORMALISM` | `X_FORMAL_SPEC` / `X_FORMAL_SPEC_ONLY` | Petri / CSP / Event-B / TLA+ / LTL/STL / formal scenario 等非 STM 输出。 |
| `X_T1PLUS_TIMED_HYBRID` | `X_T1_PLUS` / `X_T1_PLUS_OR_HYBRID` | timed automata / hybrid / critical timeout 语义不可隔离。 |
| `X_SEQUENCE_ONLY` | `X_SEQUENCE_CLASS` | sequence diagram / MSC / LSC / structured scenario trace 输入或输出，不是 NL requirements -> STM。 |
| `X_REPAIR_ONLY` | `X_REPAIR_ONLY` | 已有 model / partial state machine completion、repair 或 refinement，不是 initial `NL -> STM_0`。 |
| `X_COEXIST_ONLY` | `X_NO_GEN_REL?` | 只有 NL 与 STM 共现，方向或生成关系不足。 |

### 9.2 排除 / sentinel 表

| ID | 排除码 | 触发对象 / 原因 | 角色 | 证据 |
|---|---|---|---|---|
| `protocol-flowfsm-sentinel` | `X_PROTOCOL` |  |  |  |
| `3gpp-protocol-sentinel` | `X_PROTOCOL` |  |  |  |
| `bpmn-process-sentinel` | `X_PROCESS` |  |  |  |
| `formal-spec-sentinel` | `X_FORMAL_SPEC` |  |  |  |
| `repair-only-sentinel` | `X_REPAIR_ONLY` |  |  |  |
| `most-states-modes` | `X_FORMAL_SPEC?` |  |  |  |
| `sysmlv2-formalized-requirements` | `X_FORMAL_SPEC` / `X_T1_PLUS?` |  |  |  |
| `completion-sysml-gwt` | `X_REPAIR_ONLY` |  |  |  |
| `scenarios-statecharts-interrelated` | `X_SEQUENCE_CLASS` |  |  |  |
| `generating-statechart-designs-from-scenarios` | `X_SEQUENCE_CLASS` |  |  |  |
| `synthesis-revisited-scenario-based` | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` |  |  |  |
| `requirements-analysis-prototyping-scenarios-statecharts` | `X_NO_GEN_REL?` |  |  |  |
| `semi-auto-efsm-standard-docs` | `X_PROTOCOL?` / `CONTROL_STANDARD_EXCEPTION_PENDING` |  |  |  |
| `integrating-graphical-nl-specifications` | `X_COEXIST_ONLY` |  |  |  |
| `specification-based-verification-usecase-sm` | `X_COEXIST_ONLY` / `X_NON_STM_FORMALISM?` |  |  |  |
| `towards-automatic-model-completion` | `X_REPAIR_ONLY` |  |  |  |
| `ucgen-usecase-descriptions` | `X_NON_STM_FORMALISM` |  |  |  |
| `web-tool-goal-statechart-derivation` | `X_SEQUENCE_ONLY?` / `X_COEXIST_ONLY?` |  |  |  |

## 10. 搜索覆盖摘要与 archive 入口

R1.7 search round 哨兵为 8；archive 中还保留 R1.6 与早期 search 记录。raw JSONL / round markdown 只作审计证据，当前结论以本 SUMMARY 为准。

| round | source | query / 入口 | 原始命中 | fulltext/artifact | blocker / 早停 | 结论 |
|---|---|---|---:|---:|---|---|
| `r17-01-openalex-broad-nl-requirements` | OpenAlex | broad NL requirements / statechart / use-case query clusters | 95 | 0 | high noise broad query / broad search kept as negative evidence | 详见 [round-r17-01-openalex-broad-nl-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-01-openalex-broad-nl-requirements.md) |
| `r17-02-crossref-refined-usecase-statechart` | Crossref | use-case / statechart / requirements refined query | 50 | 1 | no fulltext/artifact / exact DOI/title discovery | 详见 [round-r17-02-crossref-refined-usecase-statechart.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-02-crossref-refined-usecase-statechart.md) |
| `r17-03-crossref-textual-usecase-behavior` | Crossref | textual use case descriptions behavior models state machine | 30 | 0 | output-not-STM noise / MARITACA remains manual | 详见 [round-r17-03-crossref-textual-usecase-behavior.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-03-crossref-textual-usecase-behavior.md) |
| `r17-04-arxiv-llm-requirements` | arXiv | LLM + state machine / state diagram requirements | 40 | 0 | requirements-quality / slicing / non-STM LLM noise / no new SA-1/2 seed | 详见 [round-r17-04-arxiv-llm-requirements.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-04-arxiv-llm-requirements.md) |
| `r17-05-semanticscholar-blocker` | Semantic Scholar API | 6 query clusters | 6 errors | 0 | HTTP 429 Too Many Requests / degraded to OpenAlex/Crossref/arXiv/DBLP | 详见 [round-r17-05-semanticscholar-blocker.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-05-semanticscholar-blocker.md) |
| `r17-06-dblp-exact-title` | DBLP API | 12 exact-title manual/classic candidates | 3 confirmed before 429/connection limits | 0 | DBLP rate/connection limit / metadata corroboration only | 详见 [round-r17-06-dblp-exact-title.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-06-dblp-exact-title.md) |
| `r17-07-classic-fulltext-wave` | OA/publisher PDFs | classic use-case / embedded / test-generation fulltext wave | 7 | 7 dirs | all paper-only / two hard boundaries / strengthens negative evidence; no new SA-1/2 | 详见 [round-r17-07-classic-fulltext-wave.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-07-classic-fulltext-wave.md) |
| `r17-08-manual-queue-artifact-recheck` | publisher exact + artifact search | R1.6 manual queue + R1.7 new manual candidates | 13 | 1 new downloaded dir | paywall / browser-only OA / no artifact / manual queue status distribution updated | 详见 [round-r17-08-manual-queue-artifact-recheck.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/round-r17-08-manual-queue-artifact-recheck.md) |

archive 入口：

- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/README.md)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/)
- [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_results/)

## 11. 文献筛查与全文阅读 provenance 摘要

旧 `agent_provenance.md` 已归档为 [../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md](../../archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/agent_provenance.md)。其记录范围仅限文献筛查、全文阅读、证据等级调整和研究性 blocker；不记录 PR review / ready / merge 进度。R1.7 最终整合输出为：47 candidates / 47 screening / 24 single-paper dirs；主 / 条件主可计候选仍为 4；Semantic Scholar API 429 已记录并由 OpenAlex/Crossref/arXiv/DBLP exact-title 替代。

## 12. 关键风险与 R2 建议

1. **四例候选仍紧绷**：当前 `yes-main / yes-conditional` 只有 4 条，且其中 2 条为条件候选。
2. **`fsm-bench-20` 不能直接算 generated seed**：公开包有 dataset / prompt / schema / code / MIT，但缺作者冻结 generated `STM_0` outputs；若使用必须 R2 复跑并保存 manifest/hash。
3. **paper-only / private / protocol 方法不能替代可运行样本**：它们必须进入 seed 方法集合，但不能冒充可复验实验输入。
4. **closed/manual 项可能改变 related-work 叙述，不应改变当前 hard gate**。
5. **本 snapshot 非全域 census**：只能作为 bounded snapshot + negative evidence + fallback handoff。

R2 最小动作：先冻结 `sefm-llm-state-machine` 与 `llms-emp-stm-subset`，再裁决 `designing-fsm-gpt4` 与 `unified-uml-multimodal-validation`；若条件候选失败，启动 `fsm-bench-20` 复跑或 project-constructed seed fallback。

## 13. 迁移表

| 旧路径 / 对象 | 新路径 / 新章节 | 当前事实真源 | 迁移理由 |
|---|---|---|---|
| `seed_corpus/README.md` | `seed_corpus/README.md redirect + corpora/seed_library/README.md` | corpora/seed_library/README.md | 旧入口降级为跳转，避免第二事实源。 |
| `seed_corpus/GUIDE.md` | `archive/.../legacy_ledgers/seed_corpus_GUIDE.md + corpora/seed_library/GUIDE.md` | corpora/seed_library/GUIDE.md | 旧规则归档，新规则按 SUMMARY-first 重写。 |
| `seed_corpus/SUMMARY.md` | `archive/.../legacy_ledgers/seed_corpus_SUMMARY.md + corpora/seed_library/SUMMARY.md` | corpora/seed_library/SUMMARY.md | 旧总账归档，新总账承载所有横向事实。 |
| `candidate_matrix.md` | `archive/.../legacy_ledgers/candidate_matrix.md；摘要进入 SUMMARY §5` | corpora/seed_library/SUMMARY.md | 47 条候选进入单一横向总账。 |
| `screening_ledger.md` | `archive/.../legacy_ledgers/screening_ledger.md；47/47 进入 SUMMARY §2/§5/§13` | corpora/seed_library/SUMMARY.md | 候选 / screening 对齐哨兵可复算。 |
| `exclusion_ledger.md` | `archive/.../legacy_ledgers/exclusion_ledger.md；摘要进入 SUMMARY §9` | corpora/seed_library/SUMMARY.md | negative evidence 直接可见。 |
| `manual_download_queue.md` | `archive/.../legacy_ledgers/manual_download_queue.md；摘要进入 SUMMARY §8` | corpora/seed_library/SUMMARY.md | manual blocker 直接可见。 |
| `baseline_seed_method_crosswalk.md` | `archive/.../legacy_ledgers/baseline_seed_method_crosswalk.md；9/9 表进入 SUMMARY §7` | corpora/seed_library/SUMMARY.md | 旧九 generation baseline 进入 seed 方法集合，不误作 repair baseline。 |
| `seed_selection_candidates.md` | `archive/.../legacy_ledgers/seed_selection_candidates.md；R2 handoff 进入 SUMMARY §4/§6` | corpora/seed_library/SUMMARY.md | R2=4 handoff 可直接读取。 |
| `search_log.md / search_rounds/ / search_results/` | `archive/.../legacy_ledgers/search_log.md、archive/..../../archive/r1_5_to_r1_7_seed_corpus_snapshot/search_rounds/、archive/.../search_results/；摘要进入 SUMMARY §10` | corpora/seed_library/SUMMARY.md | raw search 归档，搜索覆盖摘要当前可读。 |
| `agent_provenance.md` | `archive/.../legacy_ledgers/agent_provenance.md；研究性审计摘要进入 SUMMARY §11` | corpora/seed_library/SUMMARY.md | 保留文献筛查 provenance，但不记录 PR 流程状态。 |
| `seed_corpus/papers/<slug>/` | `corpora/seed_library/<slug>/；资产表进入 SUMMARY §7` | corpora/seed_library/<slug>/ + SUMMARY §7 | 24 个单篇 / artifact 证据容器迁入当前 seed library。 |

## 14. 更新日志

| 时间 | 更新 |
|---|---|
| 2026-06-14 17:55:00 | PR-R1.8-B：迁移旧 `seed_corpus/` 到 `corpora/seed_library/`；建立三件套；旧横向 ledger、search rounds / results 进入 archive；当前 SUMMARY 可复算 `47/47`、`24 dirs`、`9/9 crosswalk`、R2=4 和 manual queue 状态。 |
| 2026-06-14 13:20:00 | PR-R1.7 bounded snapshot v4：纠正 seed 方法集合 vs R2 四例计数口径，补齐旧九 direct baseline crosswalk，新增 `pushing-generative-envelope-mbse`，扩展到 47 candidates / 47 screening / 24 single-paper dirs；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 12:10:00 | PR-R1.7 bounded snapshot v3：扩展到 46 candidates / 46 screening / 23 single-paper dirs / 8 R1.7 search rounds；新增 classic fulltext wave、manual queue 状态分布和 negative evidence；主 / 条件主可计候选仍为 4 条。 |
| 2026-06-14 03:55:00 | PR-R1.6 bounded snapshot v2：扩展到 36 条候选、15 个单篇目录、4 条可交接主 / 条件主候选；新增 Zenodo/GitHub/HF artifact 核验、search_rounds 与 PR-R2 handoff。 |
| 2026-06-14 02:22:00 | 补齐 `req-mermaid-statechart` 单篇目录与 27 条 screening ledger，修正人工下载队列 6 条、主 seed 保守计数 3 条、TTool timing 降级和 R2 blocker 交接口径。 |
| 2026-06-14 01:40:00 | 初始化 seed 文库总账、候选矩阵、筛查台账、排除台账、人工下载队列和 agent provenance。 |
