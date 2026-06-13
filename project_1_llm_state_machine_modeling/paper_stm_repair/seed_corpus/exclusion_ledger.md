# exclusion ledger

本表记录硬排除与负例 sentinel。排除条目仍可作为 related work、converter boundary 或 reviewer robustness 资产，但不得进入主 strict seed。

| ID | 排除码 | 对象 | 证据指针 | 可保留用途 | 备注 |
|---|---|---|---|---|---|
| protocol-flowfsm-sentinel | `X_PROTOCOL` | RFC / protocol FSM extraction | `baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/` | protocol related work / out-of-domain | 不得作为控制系统 strict seed |
| 3gpp-protocol-sentinel | `X_PROTOCOL` | 3GPP protocol FSM extraction | `baselines/automated-extraction-protocol-state-machines-3gpp-specifications/` | protocol related work / out-of-domain | 不得作为控制系统 strict seed |
| bpmn-process-sentinel | `X_PROCESS` | textual requirements -> BPMN / process model | `baselines/automated-generation-bpmn-processes-textual-requirements/` | process-model near neighbor | 待全文核验 |
| formal-spec-sentinel | `X_FORMAL_SPEC` | NL / requirements -> formal spec | `baselines/event-b-agent/`、`baselines/llms-write-correct-tla-specifications/` | formalization related work | 待全文核验 |
| repair-only-sentinel | `X_REPAIR_ONLY` | existing model -> repair/refinement only | `baselines/automatic-debugging-support-for-uml-designs/` | repair feedback related work | 若存在 NL->initial STM 子链，可另拆候选；否则排除 |
| generating-statechart-designs-from-scenarios | `X_SEQUENCE_CLASS?` | scenario / interaction diagrams to statecharts | external scout | boundary / snowball | 若输入是 sequence diagrams 而非 NL，应排除 strict |
| synthesis-revisited-scenario-based | `X_FORMAL_SPEC?` / `X_SEQUENCE_CLASS?` | LSC / scenario-based requirements | `baselines/synthesis-revisited-scenario-based-requirements/` | boundary / snowball | 需确认 LSC 是否形式化 scenario |
| completion-sysml-gwt | `X_REPAIR_ONLY?` | SysML state machine completion from GWT + partial model | external scout | boundary / possible extended | 若依赖已有 partial state machine，不进 strict seed |
| most-states-modes | `X_FORMAL_SPEC?` | states/modes formalization | external scout | related work | 需确认是否输出 STM family |
| sysmlv2-formalized-requirements | `X_FORMAL_SPEC` / `X_T1_PLUS?` | temporal logic + SysML v2 | local baseline / external | extended / boundary | LTL/formalization 风险高 |
