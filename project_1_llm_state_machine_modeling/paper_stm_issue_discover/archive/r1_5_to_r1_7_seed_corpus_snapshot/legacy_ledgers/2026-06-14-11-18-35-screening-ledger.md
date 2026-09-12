> **Cold archive / deprecated historical snapshot.** 本文件已经脱离当前 R5.5+ 主线，只用于追溯 R1.5--R1.7 旧 seed_corpus 的历史证据链；不得作为当前 seed、baseline、eligibility 或主实验事实源。当前事实请回到 `paper_stm_repair/corpora/`、`paper_stm_repair/reports/` 与 `paper_stm_repair/pipeline/` 的对应入口。

## 归档来源与时间考据

| 字段 | 值 |
|---|---|
| 原始来源路径 | `project_1_llm_state_machine_modeling/paper_stm_repair/seed_corpus/screening_ledger.md` |
| 当前归档路径 | `archive/r1_5_to_r1_7_seed_corpus_snapshot/legacy_ledgers/2026-06-14-11-18-35-screening-ledger.md` |
| 时间前缀 / 内容冻结依据 | `d3758f2bd5a780274ff1a249b40c7184a4230242` — 2026-06-14 11:18:35 +0800 — fix(paper1-r1.7): 补齐旧baseline seed方法入账 |
| 迁入 archive commit | `928933dd3bf941aa2e5f39c43dca7c4c33f04500` — 2026-06-14 18:14:27 +0800 — docs(paper1-r1.8-b): 重构seed文库三件套 |
| 当前事实源替代入口 | [../../../corpora/seed_library/SUMMARY.md](../../../corpora/seed_library/SUMMARY.md)、[../../../corpora/repair_baselines/SUMMARY.md](../../../corpora/repair_baselines/SUMMARY.md)、[../../../corpora/nl_datasets/SUMMARY.md](../../../corpora/nl_datasets/SUMMARY.md)、[../../../reports/SUMMARY.md](../../../reports/SUMMARY.md) |

# screening ledger

筛查层级：`title` / `abstract` / `fulltext` / `artifact`。没有 fulltext / artifact 证据不得标 `SS-A`；`SA-3/SA-4/SA-5`、timed boundary、completion-only、private-data 或 outputs 未冻结的候选不得直接计入 PR-R2 主 seed 下限。

| ID | title/abstract 判定 | fulltext 判定 | artifact 判定 | 当前深度 | 纳入 / 排除理由 | 下一步 | 优先级 |
| --- | --- | --- | --- | --- | --- | --- |---|
| sefm-llm-state-machine | include | pass | pending license/hash | artifact | 最贴近 strict seed；已有 8 case × 4 strategy 线索 | 逐 case 冻结输入/输出/参考与 license | P0 |
| llms-emp-stm-subset | include STM subset only | pass | pending parquet row check | artifact | 仅 `diagram_type=stm` 可讨论；ACT/SD 排除 | 读取 parquet schema 与样例 | P0 |
| designing-fsm-gpt4 | include initial generation only | pass | partial / no license | artifact | 初始 `NL->DFSM/Mealy CSV` 可作条件 seed；repair/oracle 全部排除 | 建立 initial-only seed 切片，防 oracle leakage | P0 |
| unified-uml-multimodal-validation | include conditional | pass with synthetic caveat | HF state parquet available / license unclear | artifact | state subset 可机器下载，生成链路清楚；输入为 synthetic requirements，`SS-B + SA-2` | 交 PR-R2 作为条件主候选，需 row-level parse/render/license 抽检 | P0 |
| fsm-bench-20 | include strong | metadata/artifact pass; no paper PDF | dataset/prompt/schema/code pass; generated outputs missing | artifact | NL requirements -> deterministic FSM JSON 明确；但 outputs/gold 未冻结，暂不计主 seed | R2 若使用需复跑并冻结 raw/cleaned outputs | P0 |
| ttool-ai-smd-subset | include extended / timed boundary | pass with timing caveat | public partial | artifact | NL->SysML SMD 子集成立，但 `after (5, 5)` 等时间语义使其当前不计主 seed | PR-R3 定义 timed-SMD 规范化；若有 T0-only case 再升级 | P1 |
| fsm-gen-iec-61499 | include related-work | pass task relation / private artifact | private / unavailable | fulltext | 控制系统 NL->FSM 贴近，但 fbAssistant、数据和输出不公开，`SA-4` | 只作 related work / private boundary | P1 |
| ijisrt-uml-state-diagrams-llm | include recent LLM | pass paper-level relation | paper-only | fulltext | 文本描述 -> UML state diagram 清楚；无数据/代码/raw outputs，`SA-3` | related work；不计主 seed | P1 |
| umple-nl-state-machine | include | pass | paper-only | fulltext | NL->Umple state machine 成立，但无 benchmark/output/license | 仅作文献证据；若使用需手工重建 | P1 |
| req-mermaid-statechart | include related-work-only | pass | private / unavailable | artifact | 汽车需求 -> Mermaid statechart 任务贴合，但 Volvo/Car Weaver 数据私有 | 不计 R2 主 seed；仅 related work / private-data boundary | P1 |
| pushing-generative-envelope-mbse | include paper-only seed method | pass | paper-only / no public raw outputs | fulltext | 两个自然语言 MBSE 题项经 local LLM prompt/temperature 设置生成 SysML v2 state machine diagrams；属于 seed 方法集合，但 `SA-3` | 保留 prompt/temperature seed 方法证据；不计 R2 主四例 | P1 |
| from-use-cases-to-statecharts | include | pass | paper-only | fulltext | classic use-case -> statechart 候选；含 timing caveat 且无机器可读 artifact | 仅 manual transcription / related work | P1 |
| beyond-scenarios-state-models | include | pass via PDF | paper-only | fulltext | restricted NL use case -> hierarchical FSTM；无 UCEd/code/license | 仅 manual transcription / snowball parent | P1 |
| executable-state-machines-structured-text | include weak | pass with NL->SPS caveat | paper-only | fulltext | structured text -> executable FSM；第一步 NL->SPS 为人工 | related work；不计主 seed | P1 |
| maritaca-use-case-behavior-models | include classic | manual pending | closed / no public artifact | metadata/abstract | semi-structured use case descriptions -> state machine models；无公开 artifact | 人工下载 IEEE PDF | P1 |
| dependable-product-families-usecases-state-machines | include classic | manual pending | closed / no public artifact | metadata/abstract | restricted use cases -> state machine models；product-family variability boundary | 人工下载 IEEE PDF | P1 |
| automated-transition-use-cases-uml-sm | include classic | manual pending | no public artifact found | metadata/abstract | use case -> UML state machine 经典线索，需全文确认 | 人工下载 Springer PDF | P1 |
| execution-nl-req-bt-sm | include extended | manual pending | no public artifact found | metadata/abstract | NL->BT->SM 方向相关，但中间 BT 与 artifact 缺失使其当前不计主 seed | 人工下载 JSS PDF，核 P1/P2/P3/P4 | P2 |
| completion-sysml-gwt | include completion boundary | fail strict P3 / completion-only | paper-only | fulltext | partial SysML model + GWT requirements 补全已有 state machine transitions，触发 `X_REPAIR_ONLY` | 保留为 completion boundary，不计主 seed | P2 |
| towards-automatic-model-completion | include with completion caveat | downloaded / fail strict initial-generation | paper-only | fulltext | GWT requirements + partial SysML model / partial SMD completion，触发 `X_REPAIR_ONLY` | 移出 pending；保留 completion boundary | P2 |
| scenarios-statecharts-interrelated | boundary | fail P1 strict | paper-only | fulltext | 输入是结构化 scenario / OMT event trace diagrams，不是 NL requirements | 保留为 `X_SEQUENCE_CLASS` sentinel | P2 |
| generating-statechart-designs-from-scenarios | boundary | fail P1 likely | excluded by metadata / closed ACM optional | metadata + scout | 输入为 sequence/scenario diagrams 而非 NL requirements，`X_SEQUENCE_CLASS`；不需要为 strict seed 再追人工下载 | 保留 sentinel；已移出 manual queue 主队列 | P2 |
| synthesis-revisited-scenario-based | boundary | fail P1 strict | paper-only/local | metadata + local/scout | LSC/MSC-style formal scenario -> statechart，不是自然语言需求 | 保留 formal scenario sentinel | P2 |
| requirements-analysis-prototyping-scenarios-statecharts | boundary | direction mismatch likely | paper-only/wayback | metadata/scout | 更像 statechart -> scenarios/prototype 或 co-evolution，不是 NL->STM | 低优先人工核验 | P2 |
| nl-standard-docs-state-machines | boundary | pending | pending | title/abstract | natural-language standards -> state machines，可能是 protocol / standard extraction | 定位 AIAA PDF，确认是否 `X_PROTOCOL` / standard-only | P2 |
| semi-auto-efsm-standard-docs | boundary | manual pending | closed / unknown | metadata | standard documents -> EFSM；protocol/standard risk 高 | 除非证明确为控制标准例外，否则只作 sentinel | P2 |
| statechart-use-case-validation-event-driven | pending boundary | manual pending | closed / unknown | metadata | 题名相关，但可能是 validation 而非 generation | 人工下载/全文确认 | P2 |
| rscharter-statechart-elements | pending candidate | manual pending | SSRN / unknown | metadata | requirements -> statechart diagram elements，需确认是否完整 statechart | 人工下载 SSRN 全文 | P1 |
| most-states-modes | related-work | pending | pending | title/abstract | states/modes formalization 线索，未确认 STM family | 下载全文，确认是否 strict seed 或 formalization-only | P2 |
| sysmlv2-formalized-requirements | related-work / formal-spec boundary | pending | local paper | title/abstract | temporal logic + SysML v2，LTL/formalization 风险高 | 读取全文，可能保持 `X_FORMAL_SPEC` | P2 |
| protocol-flowfsm-sentinel | include as protocol-domain seed method / exclude control-system sample | confirmed protocol boundary | paper/code/output incomplete | fulltext | RFC 文档到 protocol FSM / rulebook 的 seed 方法成立，但触发 `X_PROTOCOL`，不默认进入控制系统四例 | 保留为 protocol-domain seed method 与长文档 agentic extraction 参考；不计 R2 控制系统样本 | P3 |
| 3gpp-protocol-sentinel | include as protocol-domain seed method / exclude control-system sample | confirmed protocol boundary | private / no GT-output package | fulltext | 3GPP 标准文档到 protocol FSM 的 extraction 方法成立，但触发 `X_PROTOCOL`，不默认进入控制系统四例 | 保留为 protocol-domain seed method 与 ensemble/span grounding 参考；不计 R2 控制系统样本 | P3 |
| source-autonomous-driving-hsm | source candidate | pending | local | title/abstract | HSM T0 A/A 高优先；但 `sources/` 是 NL 描述池，不自动 strict | 若用于 seed，需单独构造 STM0 并防泄漏 | P3 |
| source-rotorcraft-uas-hsm | source candidate | pending | local | title/abstract | UAS mission HSM T0 A/A 高优先 | 同上 | P3 |
| source-smarthand-hsm | source candidate | pending | local | title/abstract | 医疗假肢 HSM T0 A/A 高优先 | 同上 | P3 |
| source-hfsm-human-robot | source candidate | pending | local | title/abstract | 协作装配 HFSM T0 A/A 高优先 | 同上 | P3 |
| source-avp-hsm | source candidate | pending | local | title/abstract | AVP HSM T0 A/A 高优先 | 同上 | P3 |
| nlp-req-formalization-testcase-generation | include industrial NLP/MBT seed evidence | pass with IRDL/sequence intermediate caveat | paper-only / no public tool output | fulltext | NL functional requirements -> IRDL/sequence -> UML state machine；中间模型与 test-generation 主线使其 `SS-B / SA-3` | related work / manual reconstruction；不计主 seed | P1 |
| statistical-usage-testing-uml | include classic use-case seed | pass with refinement/domain-model caveat | paper-only / prototype not public | fulltext | textual/tabular UML use case -> structured use case -> state diagram / usage graph；因 refinement/domain class model caveat 标 `SS-B / SA-3` | 保留 paper-only strict evidence；不计主 seed | P1 |
| unified-use-case-statecharts | include classic UCUM seed | pass with manual case-study caveat | paper-only | fulltext | use cases -> unified UC statechart；人工/方法论 case studies，`SS-B / SA-3` | manual reconstruction / related work；不计主 seed | P1 |
| statechart-codesign-usecases | include embedded co-design seed | pass with direct/sequence route caveat | paper-only | fulltext | use cases 可 direct translate to statechart；也有 sequence-diagram route，`SS-B / SA-3` | classic weak seed；不计主 seed | P1 |
| object-models-uml-embedded | include embedded use-case->statechart | pass with object-model goal caveat | paper-only | fulltext | textual use case -> statechart -> object model，`SS-B / SA-3` | paper-only evidence；不计主 seed | P1 |
| integrating-graphical-nl-specifications | include boundary negative | fail strict P3 / statechart is input | paper-only | fulltext | NL 与 statechart/graphical notation 集成，但方向是 GN+NL -> LDG/test，不是 NL->STM | 写入 exclusion ledger；防 co-exist-only 误收 | P2 |
| specification-based-verification-usecase-sm | include boundary negative | fail target STM / testbench state machine | paper-only | fulltext | textual use cases -> SystemC testbench/test cases；verification state machine 是执行机制，不是目标系统 STM | 写入 exclusion ledger；防 testbench 误收 | P2 |
| executable-use-cases-domain-machine-specifications | include manual candidate | manual pending | closed / no artifact found | metadata | Crossref 命中 executable use cases linking requirements and machine specs；是否 STM family 未知 | 人工下载或后续降级 | P2 |
| web-tool-goal-statechart-derivation | include goal/statechart boundary | manual pending / likely non-NL input | IEEE closed / no artifact found | metadata | goal modelling -> statechart derivation；可能不是 NL requirements 输入 | 保留 boundary，需全文确认 | P2 |
| ucgen-usecase-descriptions | exclude output-not-STM | fail P2 | metadata only | metadata | LLM 生成 use case textual descriptions，不输出 STM | negative sentinel，不进 seed | P3 |
