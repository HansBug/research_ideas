# screening ledger

筛查层级：`title` / `abstract` / `fulltext` / `artifact`。没有 fulltext / artifact 证据不得标 `SS-A`；`SA-3/SA-4`、timed boundary、completion-only 或 private-data 候选不得计入 PR-R2 主 seed 下限。

| ID | title/abstract 判定 | fulltext 判定 | artifact 判定 | 当前深度 | 纳入 / 排除理由 | 下一步 |
|---|---|---|---|---|---|---|
| sefm-llm-state-machine | include | pass | pending license/hash | artifact | 最贴近 strict seed；已有 8 case × 4 strategy 线索 | 逐 case 冻结输入/输出/参考与 license |
| llms-emp-stm-subset | include STM subset only | pass | pending parquet row check | artifact | 仅 `diagram_type=stm` 可讨论；ACT/SD 排除 | 读取 parquet schema 与样例 |
| ttool-ai-smd-subset | include extended / timed boundary | pass with timing caveat | public partial | artifact | NL->SysML SMD 子集成立，但 `after (5, 5)` 等时间语义使其当前不计主 seed | PR-R3 定义 timed-SMD 规范化；若有 T0-only case 再升级 |
| umple-nl-state-machine | include | pass | paper-only | fulltext | NL->Umple state machine 成立，但无 benchmark/output/license | 仅作文献证据；若使用需手工重建 |
| designing-fsm-gpt4 | include initial generation only | pass | partial / no license | artifact | 初始 `NL->DFSM/Mealy CSV` 可作条件 seed；repair/oracle 全部排除 | 建立 initial-only seed 切片，防 oracle leakage |
| req-mermaid-statechart | include related-work-only | pass | private / unavailable | artifact | 汽车需求 -> Mermaid statechart 任务贴合，但 Volvo/Car Weaver 数据私有 | 不计 R2 主 seed；仅 related work / private-data boundary |
| from-use-cases-to-statecharts | include | pass | paper-only | fulltext | classic use-case -> statechart 候选；含 timing caveat 且无机器可读 artifact | 仅 manual transcription / related work |
| beyond-scenarios-state-models | include | pass via PDF | paper-only | fulltext | restricted NL use case -> hierarchical FSTM；无 UCEd/code/license | 仅 manual transcription / snowball parent |
| scenarios-statecharts-interrelated | boundary | fail P1 strict | paper-only | fulltext | 输入是结构化 scenario / OMT event trace diagrams，不是 NL requirements | 保留为 `X_SEQUENCE_CLASS` sentinel |
| executable-state-machines-structured-text | include weak | pass with NL->SPS caveat | paper-only | fulltext | structured text -> executable FSM；第一步 NL->SPS 为人工 | related work；不计主 seed |
| protocol-flowfsm-sentinel | exclude main strict | confirmed negative | pending | fulltext | RFC / protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| 3gpp-protocol-sentinel | exclude main strict | confirmed negative | pending | fulltext | 3GPP protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| completion-sysml-gwt | include with completion caveat | pending | pending | title/abstract | GWT requirements -> SysML SM，但可能输入含 partial model | 下载全文，确认是否 `X_REPAIR_ONLY` / completion |
| towards-automatic-model-completion | include with completion caveat | pending | pending | title/abstract | GWT requirements / model completion 线索；可能依赖 partial state machine | 下载全文，确认是否仅 completion |
| execution-nl-req-bt-sm | include extended | pending | pending | title/abstract | NL->BT->SM，中间 behavior tree | 定位正式 PDF / artifact |
| automated-transition-use-cases-uml-sm | include | pending | pending | title/abstract | use case -> UML state machine 经典线索 | 找 DOI / PDF |
| generating-statechart-designs-from-scenarios | boundary | pending | pending | title/abstract | 可能 scenario/sequence diagram -> statechart | 查是否触发 `X_SEQUENCE_CLASS` |
| synthesis-revisited-scenario-based | boundary | pending | local paper | title/abstract | LSC / scenario-based -> statechart | 查是否形式化 scenario |
| requirements-analysis-prototyping-scenarios-statecharts | boundary | pending | pending | title/abstract | scenario / statechart co-evolution 线索 | 定位 PDF，确认是否 co-exist-only |
| nl-standard-docs-state-machines | boundary | pending | pending | title/abstract | natural-language standards -> state machines，可能是 protocol / standard extraction | 定位 AIAA PDF，确认是否 `X_PROTOCOL` / standard-only |
| most-states-modes | related-work | pending | pending | title/abstract | states/modes formalization 线索，未确认 STM family | 下载全文，确认是否 strict seed 或 formalization-only |
| sysmlv2-formalized-requirements | related-work / formal-spec boundary | pending | local paper | title/abstract | temporal logic + SysML v2，LTL/formalization 风险高 | 读取全文，可能保持 `X_FORMAL_SPEC` |
| source-autonomous-driving-hsm | source candidate | pending | local | title/abstract | HSM T0 A/A 高优先；但 `sources/` 是 NL 描述池，不自动 strict | 若用于 seed，需单独构造 STM0 并防泄漏 |
| source-rotorcraft-uas-hsm | source candidate | pending | local | title/abstract | UAS mission HSM T0 A/A 高优先 | 同上 |
| source-smarthand-hsm | source candidate | pending | local | title/abstract | 医疗假肢 HSM T0 A/A 高优先 | 同上 |
| source-hfsm-human-robot | source candidate | pending | local | title/abstract | 协作装配 HFSM T0 A/A 高优先 | 同上 |
| source-avp-hsm | source candidate | pending | local | title/abstract | AVP HSM T0 A/A 高优先 | 同上 |
