# 2025-2026 arXiv LLM4Modeling / STM-family 候选初筛记录

## 1. 记录定位

本文固化 PR #92 进入 `baselines/` 的近期 arXiv 候选来源，避免筛选依据只留在 issue、PR comment 或临时 session 中。本文不是完整系统综述，而是本轮补库的最小可追溯 census record。

## 2. 初筛口径

| 项目 | 口径 |
|---|---|
| 检索时间窗 | 2025-01-01 至 2026-06-09 |
| 数据源 | arXiv 官方 API |
| 初筛依据 | title / abstract / category；进入本 PR 后再执行 PDF gate 与全文精读 |
| 初筛规模 | 去重候选池约 2327 篇；自动高分约 188 篇；经 STM-family / 强行为近邻 gate 压缩为 shortlist |
| 四条件 | `LLM4Modeling`、`NL输入`、`LLM方法`、`STM族输出` |
| direct baseline 口径 | 只认 NL / 文档 / 需求 / RFC / specification -> UML/SysML State Machine / Statechart / FSM / EFSM / LTS / protocol state machine / 近同构状态-迁移模型 |
| 强近邻口径 | BPMN、process model、TLA+、Petri net、Event-B、PAT/CSP#、LTL/STL、角色/强化学习内部 FSM/DFA 等只能作为强行为近邻或 related work，不混称 exact STM direct baseline |

## 3. 本轮 completed 入库清单

| 层级 | arXiv | 论文 | 入库目录 | 总账评估 | 四条件 | 处理结论 |
|---|---|---|---|---|---|---|
| P0 direct | [2603.29140](https://arxiv.org/abs/2603.29140) | Designing FSMs Specifications from Requirements with GPT 4.0 | [paper](./designing-fsm-specifications-from-requirements-gpt4/) | 🟢 | 🟢🟢🟢🟢 | NL DFSM 描述 -> CSV DFSM，direct STM baseline |
| P0 direct | [2510.14348](https://arxiv.org/abs/2510.14348) | Automated Extraction of Protocol State Machines from 3GPP Specifications with Domain-Informed Prompts and LLM Ensembles | [paper](./automated-extraction-protocol-state-machines-3gpp-specifications/) | 🟢 | 🟢🟢🟢🟢 | 3GPP 长规格 -> protocol FSM，direct / near-direct baseline |
| P0 direct | [2507.11222](https://arxiv.org/abs/2507.11222) | An Agentic Flow for Finite State Machine Extraction using Prompt Chaining | [paper](./agentic-flow-finite-state-machine-extraction-prompt-chaining/) | 🟢 | 🟢🟢🟢🟢 | RFC -> FSM / rulebook，direct protocol FSM baseline |
| P1 strong | [2509.10216](https://arxiv.org/abs/2509.10216) | RFSeek and Ye Shall Find | [paper](./rfseek-and-ye-shall-find/) | 🟡 | 🟢🟢🟢🟢 | RFC -> provenance-linked protocol state/event summary；强相关但目标是可视摘要与审计 |
| Boundary | [2602.05905](https://arxiv.org/abs/2602.05905) | Codified Finite-State Machines for Role-Playing | [paper](./codified-finite-state-machines-role-playing/) | 🟠 | 🟢🟢🟢🟢 | NL profile -> CFSM/CPFSM；形式同构但任务域是角色扮演内部状态控制 |
| Boundary | [2605.05478](https://arxiv.org/abs/2605.05478) | LANTERN | [paper](./lantern-llm-augmented-neurosymbolic-transfer/) | 🟠 | 🟢🟢🟢🟢 | NL task -> DFA；服务 RL transfer，不是软件系统状态机建模 |
| Strong neighbor | [2606.05792](https://arxiv.org/abs/2606.05792) | Can LLMs Write Correct TLA+ Specifications? | [paper](./llms-write-correct-tla-specifications/) | 🟠 | 🟢🟢🟢🟡 | NL -> TLA+，形式规格强近邻 |
| Strong neighbor | [2604.09318](https://arxiv.org/abs/2604.09318) | CIR+CVN | [paper](./cir-cvn-llm-petri-net-verification/) | 🟠 | 🟢🟢🟢🟡 | LLM + Petri-net verification，并发行为强近邻 |
| Strong neighbor | [2605.24546](https://arxiv.org/abs/2605.24546) | Beyond Control-Flow | [paper](./beyond-control-flow-resource-perspective-process-modeling/) | 🟠 | 🟢🟢🟢🟡 | 文本 -> resource-aware BPMN / process model |
| Strong neighbor | [2604.12105](https://arxiv.org/abs/2604.12105) | Automated BPMN Model Generation from Textual Process Descriptions | [paper](./automated-bpmn-model-generation-textual-process-descriptions/) | 🟠 | 🟢🟢🟢🟡 | 文本 -> executable BPMN 2.0 XML |
| Strong neighbor | [2604.10884](https://arxiv.org/abs/2604.10884) | Ambiguity Detection and Elimination in Automated Executable Process Modeling | [paper](./ambiguity-detection-elimination-executable-process-modeling/) | 🟠 | 🟢🟢🟢🟡 | 流程需求歧义澄清与 executable BPMN 修复 |
| Strong neighbor | [2604.07817](https://arxiv.org/abs/2604.07817) | Automatic Generation of Executable BPMN Models from Medical Guidelines | [paper](./automatic-generation-executable-bpmn-models-medical-guidelines/) | 🟠 | 🟢🟢🟢🟡 | 医疗指南 -> executable BPMN |
| Strong neighbor | [2512.12063](https://arxiv.org/abs/2512.12063) | Instruction-Tuning Open-Weight Language Models for BPMN Model Generation | [paper](./instruction-tuning-open-weight-llms-bpmn-model-generation/) | 🟠 | 🟢🟢🟢🟡 | instruction-tuned open-weight LLM -> BPMN |
| Strong neighbor | [2509.24592](https://arxiv.org/abs/2509.24592) | BPMN Assistant | [paper](./bpmn-assistant/) | 🟠 | 🟢🟢🟢🟡 | LLM + JSON IR / function calls for BPMN generation/editing |
| Strong neighbor | [2505.11646](https://arxiv.org/abs/2505.11646) | FLOW-BENCH | [paper](./flow-bench-flow-gen/) | 🟠 | 🟢🟢🟢🟡 | conversational enterprise workflow generation benchmark |
| Strong neighbor | [2507.11356](https://arxiv.org/abs/2507.11356) | What is the Best Process Model Representation? | [paper](./best-process-model-representation-generation/) | 🟠 | 🟢🟢🟢🟡 | process model representation benchmark |
| Strong neighbor | [2512.17334](https://arxiv.org/abs/2512.17334) | Req2LTL | [paper](./req2ltl/) | 🟠 | 🟢🟢🟢🟡 | NL requirements -> LTL formulas |
| Strong neighbor | [2511.08555](https://arxiv.org/abs/2511.08555) | RESTL | [paper](./restl/) | 🟠 | 🟢🟢🟢🟡 | NL CPS requirements -> STL formulas |
| Strong neighbor | [2605.01209](https://arxiv.org/abs/2605.01209) | ClarifySTL | [paper](./clarifystl/) | 🟠 | 🟢🟢🟢🟡 | requirements clarification + NL -> STL |

## 4. 已在库中去重的 carry-over 条目

| arXiv | 论文 | 现有目录 | 处理 |
|---|---|---|---|
| [2604.00275](https://arxiv.org/abs/2604.00275) | Structure- and Event-Driven Frameworks for State Machine Modeling with Large Language Models | [paper](./structure-and-event-driven-frameworks-for-state-machine-modeling-with-large-language-models/) | 已收录 direct baseline，不重复建目录 |
| [2509.23675](https://arxiv.org/abs/2509.23675) | PAT-Agent | [paper](./pat-agent-autoformalization-model-checking/) | 已收录强近邻，不重复建目录 |
| [2605.17475](https://arxiv.org/abs/2605.17475) | Event-B Agent | [paper](./event-b-agent/) | 已收录强近邻，不重复建目录 |

## 5. 边界结论

1. 本轮真正新增 direct STM baseline 只有 3 篇：`Designing FSMs...`、SpecGPT、FlowFSM。
2. RFSeek 输出接近 protocol FSM summary，但目标是审计/可视摘要，综合评估为 `🟡`。
3. CFSM 与 LANTERN 虽然四条件都是 `🟢🟢🟢🟢`，但任务域不是软件/控制系统建模，因此综合评估为 `🟠`。
4. BPMN / process / TLA+ / Petri / LTL / STL 条目一律作为强近邻入库，不能和 exact STM direct baseline 混称。
5. 本轮入库对象均已通过 PDF gate 并生成四件套；没有因 PDF 失败而新增 `⏳` 主表条目。

## 6. 更新日志

| 时间 | 事项 | 说明 |
|---|---|---|
| 2026-06-09 23:45:00 | 固化 PR #92 arXiv census | 记录 2025-01-01 至 2026-06-09 arXiv 初筛口径、19 篇 completed 入库对象、3 篇已收录 carry-over 去重对象与 direct / strong-neighbor 边界结论。 |
