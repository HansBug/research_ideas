# exclusion ledger

本表记录硬排除与负例 sentinel。排除条目仍可作为 related work、converter boundary 或 reviewer robustness 资产，但不得进入主 strict seed。

## ledger 范围说明

- 本 ledger 同时包含两类条目：
  1. **candidate-bound exclusion**：已经进入 [candidate_matrix.md](./candidate_matrix.md) / [screening_ledger.md](./screening_ledger.md) 的具体候选，若 fulltext / metadata 已触发 hard exclusion，应在这里保留对应 row。
  2. **generic sentinel**：用于提醒 reviewer 的通用负例类型或本地 baseline 负例，可能不与 candidate matrix 一一对应。
- PR-R2 冻结样本时，必须同时检查本 ledger、[screening_ledger.md](./screening_ledger.md) 与 [seed_selection_candidates.md](./seed_selection_candidates.md)，不得只看单一表格。

## 排除码 crosswalk

| PR body hard code | 本文库常用别名 | 含义 |
|---|---|---|
| `X_PROTOCOL_FSM` | `X_PROTOCOL` | RFC / 3GPP / network protocol FSM 或 standard/protocol 风险。 |
| `X_PROCESS_MODEL` | `X_PROCESS` | BPMN / workflow / business process / resource-flow。 |
| `X_NON_STM_FORMALISM` | `X_FORMAL_SPEC` / `X_FORMAL_SPEC_ONLY` | Petri / CSP / Event-B / TLA+ / LTL/STL / formal scenario 等非 STM 输出。 |
| `X_T1PLUS_TIMED_HYBRID` | `X_T1_PLUS` / `X_T1_PLUS_OR_HYBRID` | timed automata / hybrid / critical timeout 语义不可隔离。 |
| `X_SEQUENCE_ONLY` | `X_SEQUENCE_CLASS` | sequence diagram / MSC / LSC / structured scenario trace 输入或输出，不是 NL requirements -> STM。 |
| `X_REPAIR_ONLY` | `X_REPAIR_ONLY` | 已有 model / partial state machine completion、repair 或 refinement，不是 initial `NL -> STM_0`。 |
| `X_COEXIST_ONLY` | `X_NO_GEN_REL?` | 只有 NL 与 STM 共现，方向或生成关系不足。 |


| ID | 排除码 | 对象 | 证据指针 | 可保留用途 | 备注 |
|---|---|---|---|---|---|
| protocol-flowfsm-sentinel | `X_PROTOCOL` | RFC / protocol FSM extraction | `baselines/agentic-flow-finite-state-machine-extraction-prompt-chaining/` | protocol related work / out-of-domain | 不得作为控制系统 strict seed |
| 3gpp-protocol-sentinel | `X_PROTOCOL` | 3GPP protocol FSM extraction | `baselines/automated-extraction-protocol-state-machines-3gpp-specifications/` | protocol related work / out-of-domain | 不得作为控制系统 strict seed |
| bpmn-process-sentinel | `X_PROCESS` | textual requirements -> BPMN / process model | `baselines/automated-generation-bpmn-processes-textual-requirements/` | process-model near neighbor | 待全文核验 |
| formal-spec-sentinel | `X_FORMAL_SPEC` | NL / requirements -> formal spec | `baselines/event-b-agent/`、`baselines/llms-write-correct-tla-specifications/` | formalization related work | 待全文核验 |
| repair-only-sentinel | `X_REPAIR_ONLY` | existing model -> repair/refinement only | `baselines/automatic-debugging-support-for-uml-designs/` | repair feedback related work | 若存在 NL->initial STM 子链，可另拆候选；否则排除 |
| most-states-modes | `X_FORMAL_SPEC?` | states/modes formalization | external scout | related work | 需确认是否输出 STM family |
| sysmlv2-formalized-requirements | `X_FORMAL_SPEC` / `X_T1_PLUS?` | temporal logic + SysML v2 | local baseline / external | extended / boundary | LTL/formalization 风险高 |
| completion-sysml-gwt | `X_REPAIR_ONLY` | partial SysML model + GWT requirements -> state-machine completion | [papers/completion-sysml-gwt/seed_desc.md](./papers/completion-sysml-gwt/seed_desc.md) | completion related work | R1.6 fulltext confirmed；不计 strict seed |
| scenarios-statecharts-interrelated | `X_SEQUENCE_CLASS` | OMT event trace diagrams / structured scenarios -> statecharts | [papers/scenarios-statecharts-interrelated/seed_desc.md](./papers/scenarios-statecharts-interrelated/seed_desc.md) | boundary / snowball | fulltext confirmed；输入不是自然语言需求文本 |
| generating-statechart-designs-from-scenarios | `X_SEQUENCE_CLASS` | UML sequence/scenario diagrams -> statecharts | https://doi.org/10.1145/337180.337217 | boundary / snowball | 输入不是 NL requirements |
| synthesis-revisited-scenario-based | `X_FORMAL_SPEC` / `X_SEQUENCE_CLASS` | LSC / MSC-style formal scenario -> statecharts | https://doi.org/10.1007/978-3-540-31847-7_18 | boundary / snowball | scenario-based formal input，不计 strict seed |
| requirements-analysis-prototyping-scenarios-statecharts | `X_NO_GEN_REL?` | statechart / scenario co-evolution or statechart -> scenarios | external scout | related work | 方向疑似不满足 NL->STM |
| semi-auto-efsm-standard-docs | `X_PROTOCOL?` / `CONTROL_STANDARD_EXCEPTION_PENDING` | standard document -> EFSM | https://doi.org/10.1109/DSN-W.2015.17 | standard/protocol sentinel | reviewer 复核前不得计入四例 |
