# screening ledger

筛查层级：`title` / `abstract` / `fulltext` / `artifact`。没有 fulltext / artifact 证据不得标 `SS-A`。

| ID | title/abstract 判定 | fulltext 判定 | artifact 判定 | 当前深度 | 纳入 / 排除理由 | 下一步 |
|---|---|---|---|---|---|---|
| sefm-llm-state-machine | include | pending case-level check | pending license/hash | artifact | 最贴近 strict seed；已有 8 case × 4 strategy 线索 | 逐 case 冻结输入/输出/参考与 license |
| llms-emp-stm-subset | include STM subset only | pending | pending parquet row check | artifact | 仅 `diagram_type=stm` 可讨论；ACT/SD 排除 | 读取 parquet schema 与样例 |
| ttool-ai-smd-subset | include SMD subset only | pending | pending TTool XML/parquet | artifact | NL->SysML 联合模型，需剥离 state-machine 部分 | 核验 SMD 输出与转换损失 |
| umple-nl-state-machine | include | pending | pending | fulltext | 可能 NL->Umple state machine | 全文确认 generation relation |
| designing-fsm-gpt4 | include with repair caveat | pending | pending | artifact | NL->DFSM/Mealy CSV，但含 refinement | 分离初始生成与后续 repair |
| from-use-cases-to-statecharts | include | pending | unknown | fulltext | classic use-case -> statechart 候选 | 全文核验是否 T0 与生成关系 |
| beyond-scenarios-state-models | include | pending | unknown | fulltext | scenario/use-case -> state model 候选 | 全文核验输出家族 |
| scenarios-statecharts-interrelated | include | pending | unknown | fulltext | scenario -> statechart synthesis 候选 | 核验 scenario 是否 NL 还是形式化 LSC |
| executable-state-machines-structured-text | include | pending | unknown | fulltext | structured text -> executable state machines | 核验结构文本是否可视作 NL |
| protocol-flowfsm-sentinel | exclude main strict | confirmed negative | pending | fulltext | RFC / protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| 3gpp-protocol-sentinel | exclude main strict | confirmed negative | pending | fulltext | 3GPP protocol FSM，触发 `X_PROTOCOL` | 写入 exclusion ledger |
| completion-sysml-gwt | include with completion caveat | pending | pending | title/abstract | GWT requirements -> SysML SM，但可能输入含 partial model | 下载全文，确认是否 `X_REPAIR_ONLY` / completion |
| execution-nl-req-bt-sm | include extended | pending | pending | title/abstract | NL->BT->SM，中间 behavior tree | 定位正式 PDF / artifact |
| automated-transition-use-cases-uml-sm | include | pending | pending | title/abstract | use case -> UML state machine 经典线索 | 找 DOI / PDF |
| generating-statechart-designs-from-scenarios | boundary | pending | pending | title/abstract | 可能 scenario/sequence diagram -> statechart | 查是否触发 `X_SEQUENCE_CLASS` |
| synthesis-revisited-scenario-based | boundary | pending | pending | title/abstract | LSC / scenario-based -> statechart | 查是否形式化 scenario |
| source-autonomous-driving-hsm | source candidate | pending | local | title/abstract | HSM T0 A/A 💎；但 sources 是 NL 描述池 | 若用于 seed，需单独构造 STM0 并防泄漏 |
| source-rotorcraft-uas-hsm | source candidate | pending | local | title/abstract | UAS mission HSM T0 A/A 💎 | 同上 |
| source-smarthand-hsm | source candidate | pending | local | title/abstract | 医疗假肢 HSM T0 A/A 💎 | 同上 |
| source-hfsm-human-robot | source candidate | pending | local | title/abstract | 协作装配 HFSM T0 A/A 💎 | 同上 |
| source-avp-hsm | source candidate | pending | local | title/abstract | AVP HSM T0 A/A 💎 | 同上 |
