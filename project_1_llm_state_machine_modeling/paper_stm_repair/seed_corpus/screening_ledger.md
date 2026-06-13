# screening ledger

筛查层级：`title` / `abstract` / `fulltext` / `artifact`。没有 fulltext / artifact 证据不得标 `SS-A`；`SA-3/SA-4/SA-5`、timed boundary、completion-only、private-data 或 outputs 未冻结的候选不得直接计入 PR-R2 主 seed 下限。

| ID | title/abstract 判定 | fulltext 判定 | artifact 判定 | 当前深度 | 纳入 / 排除理由 | 下一步 |
| --- | --- | --- | --- | --- | --- | --- |
| sefm-llm-state-machine | include | pass | pending license/hash | artifact | 最贴近 strict seed；已有 8 case × 4 strategy 线索 | 逐 case 冻结输入/输出/参考与 license |
| llms-emp-stm-subset | include STM subset only | pass | pending parquet row check | artifact | 仅 `diagram_type=stm` 可讨论；ACT/SD 排除 | 读取 parquet schema 与样例 |
| designing-fsm-gpt4 | include initial generation only | pass | partial / no license | artifact | 初始 `NL->DFSM/Mealy CSV` 可作条件 seed；repair/oracle 全部排除 | 建立 initial-only seed 切片，防 oracle leakage |
| unified-uml-multimodal-validation | include conditional | pass with synthetic caveat | HF state parquet available / license unclear | artifact | state subset 可机器下载，生成链路清楚；输入为 synthetic requirements，`SS-B + SA-2` | 交 PR-R2 作为条件主候选，需 row-level parse/render/license 抽检 |
| fsm-bench-20 | include strong | metadata/artifact pass; no paper PDF | dataset/prompt/schema/code pass; generated outputs missing | artifact | NL requirements -> deterministic FSM JSON 明确；但 outputs/gold 未冻结，暂不计主 seed | R2 若使用需复跑并冻结 raw/cleaned outputs |
| ttool-ai-smd-subset | include extended / timed boundary | pass with timing caveat | public partial | artifact | NL->SysML SMD 子集成立，但 `after (5, 5)` 等时间语义使其当前不计主 seed | PR-R3 定义 timed-SMD 规范化；若有 T0-only case 再升级 |
| fsm-gen-iec-61499 | include related-work | pass task relation / private artifact | private / unavailable | fulltext | 控制系统 NL->FSM 贴近，但 fbAssistant、数据和输出不公开，`SA-4` | 只作 related work / private boundary |
| ijisrt-uml-state-diagrams-llm | include recent LLM | pass paper-level relation | paper-only | fulltext | 文本描述 -> UML state diagram 清楚；无数据/代码/raw outputs，`SA-3` | related work；不计主 seed |
| umple-nl-state-machine | include | pass | paper-only | fulltext | NL->Umple state machine 成立，但无 benchmark/output/license | 仅作文献证据；若使用需手工重建 |
| req-mermaid-statechart | include related-work-only | pass | private / unavailable | artifact | 汽车需求 -> Mermaid statechart 任务贴合，但 Volvo/Car Weaver 数据私有 | 不计 R2 主 seed；仅 related work / private-data boundary |
| from-use-cases-to-statecharts | include | pass | paper-only | fulltext | classic use-case -> statechart 候选；含 timing caveat 且无机器可读 artifact | 仅 manual transcription / related work |
| beyond-scenarios-state-models | include | pass via PDF | paper-only | fulltext | restricted NL use case -> hierarchical FSTM；无 UCEd/code/license | 仅 manual transcription / snowball parent |
| executable-state-machines-structured-text | include weak | pass with NL->SPS caveat | paper-only | fulltext | structured text -> executable FSM；第一步 NL->SPS 为人工 | related work；不计主 seed |
| maritaca-use-case-behavior-models | include classic | manual pending | closed / no public artifact | metadata/abstract | semi-structured use case descriptions -> state machine models；无公开 artifact | 人工下载 IEEE PDF |
| dependable-product-families-usecases-state-machines | include classic | manual pending | closed / no public artifact | metadata/abstract | restricted use cases -> state machine models；product-family variability boundary | 人工下载 IEEE PDF |
| automated-transition-use-cases-uml-sm | include classic | manual pending | no public artifact found | metadata/abstract | use case -> UML state machine 经典线索，需全文确认 | 人工下载 Springer PDF |
| execution-nl-req-bt-sm | include extended | manual pending | no public artifact found | metadata/abstract | NL->BT->SM 方向相关，但中间 BT 与 artifact 缺失使其当前不计主 seed | 人工下载 JSS PDF，核 P1/P2/P3/P4 |
| completion-sysml-gwt | include completion boundary | fail strict P3 / completion-only | paper-only | fulltext | partial SysML model + GWT requirements 补全已有 state machine transitions，触发 `X_REPAIR_ONLY` | 保留为 completion boundary，不计主 seed |
| towards-automatic-model-completion | include with completion caveat | pending | pending | title/abstract | GWT requirements / model completion 线索；可能依赖 partial state machine | 下载全文，确认是否仅 completion |
| scenarios-statecharts-interrelated | boundary | fail P1 strict | paper-only | fulltext | 输入是结构化 scenario / OMT event trace diagrams，不是 NL requirements | 保留为 `X_SEQUENCE_CLASS` sentinel |
| generating-statechart-designs-from-scenarios | boundary | fail P1 likely | excluded by metadata / closed ACM optional | metadata + scout | 输入为 sequence/scenario diagrams 而非 NL requirements，`X_SEQUENCE_CLASS`；不需要为 strict seed 再追人工下载 | 保留 sentinel；已移出 manual queue 主队列 |
| synthesis-revisited-scenario-based | boundary | fail P1 strict | paper-only/local | metadata + local/scout | LSC/MSC-style formal scenario -> statechart，不是自然语言需求 | 保留 formal scenario sentinel |
| requirements-analysis-prototyping-scenarios-statecharts | boundary | direction mismatch likely | paper-only/wayback | metadata/scout | 更像 statechart -> scenarios/prototype 或 co-evolution，不是 NL->STM | 低优先人工核验 |
| nl-standard-docs-state-machines | boundary | pending | pending | title/abstract | natural-language standards -> state machines，可能是 protocol / standard extraction | 定位 AIAA PDF，确认是否 `X_PROTOCOL` / standard-only |
| semi-auto-efsm-standard-docs | boundary | manual pending | closed / unknown | metadata | standard documents -> EFSM；protocol/standard risk 高 | 除非证明确为控制标准例外，否则只作 sentinel |
| statechart-use-case-validation-event-driven | pending boundary | manual pending | closed / unknown | metadata | 题名相关，但可能是 validation 而非 generation | 人工下载/全文确认 |
| rscharter-statechart-elements | pending candidate | manual pending | SSRN / unknown | metadata | requirements -> statechart diagram elements，需确认是否完整 statechart | 人工下载 SSRN 全文 |
| most-states-modes | related-work | pending | pending | title/abstract | states/modes formalization 线索，未确认 STM family | 下载全文，确认是否 strict seed 或 formalization-only |
| sysmlv2-formalized-requirements | related-work / formal-spec boundary | pending | local paper | title/abstract | temporal logic + SysML v2，LTL/formalization 风险高 | 读取全文，可能保持 `X_FORMAL_SPEC` |
| protocol-flowfsm-sentinel | exclude main strict | confirmed negative | pending | fulltext | RFC / protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| 3gpp-protocol-sentinel | exclude main strict | confirmed negative | pending | fulltext | 3GPP protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| source-autonomous-driving-hsm | source candidate | pending | local | title/abstract | HSM T0 A/A 高优先；但 `sources/` 是 NL 描述池，不自动 strict | 若用于 seed，需单独构造 STM0 并防泄漏 |
| source-rotorcraft-uas-hsm | source candidate | pending | local | title/abstract | UAS mission HSM T0 A/A 高优先 | 同上 |
| source-smarthand-hsm | source candidate | pending | local | title/abstract | 医疗假肢 HSM T0 A/A 高优先 | 同上 |
| source-hfsm-human-robot | source candidate | pending | local | title/abstract | 协作装配 HFSM T0 A/A 高优先 | 同上 |
| source-avp-hsm | source candidate | pending | local | title/abstract | AVP HSM T0 A/A 高优先 | 同上 |
