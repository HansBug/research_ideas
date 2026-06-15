# repair_baselines/SUMMARY.md

## 0. 论文集整体概况

本目录服务于第一篇论文 `<NL, STM_0> -> STM_k / Better STM` 主线，记录 STM 修正任务 baseline 与近邻工作。当前按更严格的实验 baseline 硬定义重新收紧：**真正 baseline 必须同时满足输入含 `NL` 与 `STM_0`，且 `STM_0` 能明确追溯为由同一 `NL` 生成 / 派生；仅有 `STM + error / tests / oracle / diagnostics` 的工作不能称为本文 baseline。**

阶段性结论因此改为：**当前 14 个入库条目中，严格全绿 baseline 尚未确认；`completion-sysml-gwt` 是唯一 P0 条件 baseline 候选，其余条目应降级为 generation-feedback、repair-engine near-neighbor、异构形式化近邻、模型一致性 / completion 近邻或 negative evidence。**

| 指标 | 当前值 |
|---|---:|
| 已建单篇目录 | 14 |
| 已完成全文阅读 / 旁路核验条目 | 14 |
| 严格全绿 baseline | 0（当前证据尚未确认） |
| P0 条件 baseline 候选 | 1（`completion-sysml-gwt`） |
| 生成链内 feedback / refinement 近邻 | 4（含 `designing-fsm-gpt4-repair`） |
| repair-engine / partial-STM 近邻 | 2 |
| 异构形式化 repair 强近邻 | 2 |
| 模型一致性 / 补全 / diagnostics 近邻 | 4 |
| 人工下载 / 待全文队列 | 10 条 |

> 注：本目录不替代 [../seed_library/](../seed_library/)；`designing-fsm-gpt4`、`ttool-ai`、`llms-emp`、`fsm-gen-iec-61499` 等若同时具备 seed 与 repair/feedback 线索，必须按“seed 关系”和“repair 能力”分开记录。
> 注：`completion-sysml-gwt` 明确使用 GWT/Gherkin 需求 + partial SysML state machine 并补全 transitions，是当前唯一进入主 baseline 候选的 P0 条目；但其 `STM_0` / partial SMD 是否严格由同一组 NL 生成仍需二次核验，因此暂列“条件 baseline 候选”。
> 注：`flowrepair-stateflow-cps`、`execution-partial-state-machine-models`、`designing-fsm-gpt4-repair` 等虽有强 repair / refinement 机制，但不满足“repair 输入同时含 NL 与由该 NL 生成的 STM_0”的硬门槛，不能写成本文 baseline。

## 1. emoji / enum 标准

正式表中 emoji 列只写 emoji，释义如下。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达；`❓` 表示待核，`⚪` 表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| NL 参与 | repair 输入同时含 NL 与 STM | 初始生成阶段含 NL，repair 阶段主要看模型 | 有 NL 但与 repair 输入关系弱，或仅作背景 | 与 NL/STM 无关 | 待核 | 不适用 |
| `STM_0` 输入 | repair / completion 输入明确包含初始 STM 或 partial STM | 有初始模型制品，但是否为 STM 或 repair 输入需重建 | 只有非 STM 模型制品或弱初始制品 | 无初始 STM / 模型输入 | 待核 | 不适用 |
| `NL -> STM_0` 关系 | `STM_0` 明确由同一 NL 生成 / 派生，且作为 repair 输入 | NL 与 `STM_0` 有强 trace / 补全关系，但骨架或生成过程需人工重建 | 只有 NL 或只有 STM，或二者关系弱 | 无 `NL -> STM_0` 关系 | 待核 | 不适用 |
| 修正任务匹配 | 明确同构 `<NL, STM_0> -> STM_k` repair / completion | `STM_0 -> STM_k` 或模型制品 repair，可较清楚映射到 STM | 局部 feedback / consistency / completion 线索 | 无 repair / feedback | 待核 | 不适用 |
| STM 谱系匹配 | T0+FSM/HSM/EFSM/statechart 明确 | UML/SysML/Stateflow/IEC 61499 等可转换模型 | 状态机边界弱或需大量转换 | 非目标形式主义 / 非模型制品 | 待核 | 不适用 |
| 反馈来源 | 结构化 diagnostics / verification / simulation / counterexample / proof | rule / test / consistency feedback | 人工审阅、弱反馈或非结构化反馈 | 无反馈 | 待核 | 不适用 |
| 自动化程度 | 无人化自动闭环 | 半自动，少量人工配置或选择 | 人在回路强依赖 | 手工方法 | 待核 | 不适用 |
| LLM / agent loop | 明确 LLM agentic repair loop | LLM self-refine / feedback regeneration | LLM 只做局部建议或前处理 | 无 LLM | 待核 | 不适用 |
| 可作为 baseline | 满足硬定义且代码 / 数据 / 输入输出 / 许可基本可复验 | 满足主要任务结构但存在条件缺口，可论文级重建或部分复现 | 只能概念对照或 related work | 不可作为 baseline | 待核 | 不适用 |
| 资源可获取性 | 论文、代码、数据、输入输出、许可、版本清楚 | 关键资源部分公开 | 只能从论文图表 / 附录重建 | 关键资源不可得 | 待核 | 不适用 |

## 2. 检索覆盖表

本表记录 PR-R1.8-C 已执行或由独立任务完成的覆盖切片。`粗略命中` 是检索阶段的噪声量级，不参与精确复算；`§2.1 去重候选 / 入库 / 人工队列 / 待核 / 降级或 negative` 必须能从 §2.1 候选池按来源切片复算。跨切片命中的同一候选会在每个来源切片各计一次，用于审计覆盖；正式去重条目数以 §5--§8 为准。

| 切片 | 日期 | 来源 / 范围 | query / 方法 | 粗略命中 | §2.1 去重候选 | 入库 | 人工队列 | 待核 | 降级 / negative | 备注 |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| `W-LOCAL` | 2026-06-15 | 本地 `baselines/`、[../seed_library/](../seed_library/)、`evidence/` | `repair / feedback / completion / checker / counterexample / simulation` 交叉核验 | 20+ | 12 | 12 | 0 | 0 | 0 | 识别 seed+repair 分段共存与旧 baseline repair slice |
| `W-SE` | 2026-06-15 | SE / Modeling / Requirements venue 与本地候选 | state machine / UML / SysML + repair / completion / consistency | 20 | 9 | 4 | 3 | 1 | 1 | SoSyM、ICSE、ASE、EASE、SANER 等候选；已补入 `execution-partial-state-machine-models` |
| `W-FM` | 2026-06-15 | FM / CAV / TACAS / TAP / STTT / FMSD | timed automata / model checking / counterexample + repair | 15+ | 9 | 3 | 4 | 2 | 0 | PAT/Event-B 已入库；timed automata repair 簇待全文后再决定是否升级 |
| `W-ME` | 2026-06-15 | Maintenance / Evolution / empirical / quality | model consistency / model completion / model evolution | 10+ | 11 | 2 | 6 | 3 | 0 | LLM model evolution、model completion、inconsistency repair 多为 near-neighbor 或待核 |
| `W-ARXIV` | 2026-06-15 | arXiv 近三年 + OpenAlex / Crossref 辅助 | LLM state machine repair、Simulink-Stateflow repair、model completion LLM | 76 | 9 | 5 | 1 | 1 | 2 | 噪声很高；`flowrepair-stateflow-cps` 已全文入库，仍保留 formal spec repair / model completion 待核 |

## 2.1 候选池 / 筛查账

本表把 §2 的切片级统计落到逐项候选，便于后续复算“粗略命中—初筛—入库—人工队列—排除/降级”的去向。它不是第二事实源；正式分级和资源状态仍以后文 §6--§10 为准。

| 候选 | 年份 | 来源切片 | venue / source | 初筛结论 | 最终去向 | 降级 / 排除理由 | 证据入口 |
|---|---:|---|---|---|---|---|---|
| Completion of SysML state machines from Given-When-Then requirements | 2024 | W-SE / W-LOCAL | SoSyM | P0 | 入库：`completion-sysml-gwt` | direct completion；但依赖 GWT + partial SysML | [DOI](https://doi.org/10.1007/s10270-024-01228-3) |
| Towards Automatic Model Completion | 2022 | W-SE / W-LOCAL | arXiv | P1 | 入库：`towards-automatic-model-completion` | 同簇 precursor，不重复计数 | [arXiv](https://arxiv.org/abs/2210.03388) |
| Execution of Partial State Machine Models | 2022 | W-SE | TSE / arXiv | P0/P1 | 入库：`execution-partial-state-machine-models` | 无 NL，也无 `NL -> STM_0` 关系；只能作为 `STM_0 -> executable/refined STM` 近邻 | [DOI](https://doi.org/10.1109/TSE.2020.3008850) / [arXiv](https://arxiv.org/abs/2103.17194) |
| Designing FSMs Specifications from Requirements with GPT 4.0 | 2026 | W-LOCAL / W-ARXIV | arXiv | P0/P1 | 入库：`designing-fsm-gpt4-repair` | seed + repair 分段共存；只登记 repair slice | [arXiv](https://arxiv.org/abs/2603.29140) |
| System Architects Are not Alone Anymore | 2024 | W-LOCAL | MODELSWARD | P1 | 入库：`ttool-ai-feedback` | 生成链内 feedback，非独立 repair-only 方法 | [HAL](https://telecom-paris.hal.science/hal-04483279) |
| Generating SysML Behavior Models via LLMs | 2025 | W-LOCAL | MODELSWARD / ACM | P1 | 入库：`llms-emp-feedback` | 只取 STM 子集；checking 含人工 | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926) |
| LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | W-LOCAL | IEEE | P1 | 入库：`fsm-gen-iec-61499` | 工业仿真/用户 refinement；非无人自动 repair | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/) |
| Automatic Debugging Support for UML Designs | 2000 | W-LOCAL / W-SE | arXiv | P1 | 入库：`automatic-debugging-support-uml-designs` | 经典 statechart debugging；输入不是 NL | [arXiv](https://arxiv.org/abs/cs/0011017) |
| PAT-Agent: Autoformalization for Model Checking | 2025 | W-FM / W-ARXIV / W-LOCAL | arXiv | P1 | 入库：`pat-agent` | CSP# / PAT，非 STM family | [arXiv](http://arxiv.org/abs/2509.23675) |
| Event-B Agent | 2026 | W-FM / W-ARXIV / W-LOCAL | arXiv / FSE | P1 | 入库：`event-b-agent` | Event-B，非 STM family | [arXiv](http://arxiv.org/abs/2605.17475) |
| AI-Driven Consistency of SysML Diagrams | 2024 | W-ME / W-LOCAL | EASE | P2 | 入库：`ai-driven-consistency-sysml` | UCD/BD consistency，非 SMD direct | [DOI](https://doi.org/10.1145/3640310.3674079) |
| Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | W-ME / W-LOCAL | ICSE NIER | P2 | 入库：`few-shot-model-completion` | class/activity completion，非 STM repair | [DOI](https://doi.org/10.1109/ICSE-NIER58687.2023.00008) |
| Automated BPMN Model Generation from Textual Process Descriptions | 2026 | W-ARXIV / W-LOCAL | arXiv | P2 | 入库：`automated-bpmn-diagnostic-repair` | BPMN diagnostics-to-repair 方法近邻，非 STM | [arXiv](https://arxiv.org/abs/2604.12105) |
| FlowRepair: Search-based automated program repair of CPS controllers modeled in Simulink-Stateflow | 2026 | W-ARXIV / W-FM | IST / arXiv | P1 | 入库：`flowrepair-stateflow-cps` | Stateflow/CPS controller repair 强近邻；无 NL 且依赖 Simulink/仿真 oracle | [DOI](https://doi.org/10.1016/j.infsof.2025.108010) / [arXiv](https://arxiv.org/abs/2404.04688) |
| Clock Bound Repair for Timed Systems | 2019 | W-FM | CAV | P1/P2 | 人工队列 | timed automata repair，需全文后定位 | [DOI](https://doi.org/10.1007/978-3-030-25540-4_5) |
| TarTar: A Timed Automata Repair Tool | 2020 | W-FM | CAV | P1/P2 | 人工队列 | timed automata repair tool，需全文 | [DOI](https://doi.org/10.1007/978-3-030-53288-8_25) |
| Automated repair for timed systems | 2021/2022 | W-FM | FMSD | P1/P2 | 人工队列 | TarTar journal extension，需全文 | [DOI](https://doi.org/10.1007/s10703-022-00397-5) |
| Repairing Timed Automata Clock Guards through Abstraction and Testing | 2019 | W-FM | TAP@FM | P1/P2 | 人工队列 | clock-guard repair，需全文 | [DOI](https://doi.org/10.1007/978-3-030-31157-5_9) |
| Change-Preserving Model Repair | 2017 | W-ME | FASE | P2 | 人工队列 | model repair 经典；非 STM direct 待全文 | [DOI](https://doi.org/10.1007/978-3-662-54494-5_16) |
| Fixing Inconsistencies in UML Design Models | 2007 | W-SE / W-ME | ICSE | P2 | 人工队列 | UML multi-view consistency repair；待全文 | [DOI](https://doi.org/10.1109/ICSE.2007.38) |
| Generating and Evaluating Choices for Fixing Inconsistencies in UML Design Models | 2008 | W-SE / W-ME | ASE | P2 | 人工队列 | repair choice generation；待全文 | [DOI](https://doi.org/10.1109/ASE.2008.20) |
| Computing repair trees for resolving inconsistencies in design models | 2012 | W-SE / W-ME | ASE | P2 | 人工队列 | repair tree 机制；待全文 | [DOI](https://doi.org/10.1145/2351676.2351707) |
| Software Model Evolution with Large Language Models | 2025 | W-ME / W-ARXIV | ICSE | P2 | 人工队列 | LLM model evolution/completion；需全文核对象 | [DOI](https://doi.org/10.1109/ICSE55347.2025.00112) |
| Multi-Location Software Model Completion | 2026 | W-ME | ICSE | 待核 | 人工队列 | 目前仅会议页元数据，需正式论文/全文 | [ICSE page](https://conf.researchr.org/details/icse-2026/icse-2026-research-track/270/Multi-Location-Software-Model-Completion) |
| Generating repairs for inconsistent models | 2023 | W-SE / W-ME | SoSyM | P2 | 候选待核 | design-model inconsistency repair；需二批全文确认是否含 statechart 规则 | [DOI](https://doi.org/10.1007/s10270-022-00996-0) |
| History-based Model Repair Recommendations | 2021 | W-ME | TOSEM | P2 | 候选待核 | history-based model repair；非 STM direct 待核 | [DOI](https://doi.org/10.1145/3419017) |
| PARMOREL: a framework for customizable model repair | 2022 | W-ME | SoSyM | P2 | 候选待核 | generic model repair framework；对象不一定是 STM | [DOI](https://doi.org/10.1007/s10270-022-01005-0) |
| Automatic B-model repair using model checking and machine learning | 2019 | W-FM | ASE Journal | P2 | 候选待核 | B-method/formal model repair；非 STM family | [DOI](https://doi.org/10.1007/s10515-019-00264-4) |
| On Effectiveness of Formal Model Repair by Large Language Models | 2025 | W-ARXIV / W-FM | ASEW / ASYDE | 待核 | 候选待核 | LLM formal model repair；对象和资源需全文确认 | [DOI](https://doi.org/10.1109/ASEW67777.2025.00033) |
| Synthesis of State Machine Models | 2020 | W-SE | MODELS | Skip/待核 | 降级 | 更像 synthesis / generation；未见 repair loop | [MODELS page](https://conf.researchr.org/details/models-2020/models-2020-technical-track/33/Synthesis-of-State-Machine-Models) |
| RepairAgent | 2025 | W-ARXIV | ICSE | Skip | negative | program repair；FSM 只是 agent workflow，不是 STM artifact | [DOI](https://doi.org/10.1109/ICSE55347.2025.00157) |
| HybridRepair | 2022 | W-ARXIV | ISSTA | Skip | negative | repair 对象是 deep learning model，不是建模制品 | [ISSTA page](https://conf.researchr.org/details/issta-2022/issta-2022-technical-papers/52/HybridRepair-Towards-Annotation-Efficient-Repair-for-Deep-Learning-Models) |

## 3. 检索关键词簇分析

### 3.1 当前推荐关键词簇

- `requirements-derived state machine repair` / `generated state machine repair requirements` / `natural language requirements state machine refinement`。
- `Given-When-Then state machine completion` / `Gherkin SysML state machine completion` / `requirements traceability state machine repair`。
- `SysML state machine requirements completion` / `UML state machine requirements repair` / `statechart requirements consistency repair`。
- `LLM state machine repair requirements` / `NL2FSM repair` / `counterexample requirements state machine repair`。

### 3.2 高命中特征

- `partial SysML state machine + GWT requirements` 是目前唯一接近 `<NL, STM_0> -> STM_k` 的主 baseline cluster。
- 最有价值的新检索方向不是泛化 `state machine repair`，而是先确认 `NL -> STM_0` 生成 / 派生关系，再检查是否有 repair / completion / refinement。
- `generation pipeline + checker feedback` 常见于 LLM4Modeling 工作，适合作为 feedback-regeneration 近邻，但只有当 repair 输入保留 NL 与 `STM_0` 时才可能升级为 baseline。
- `Stateflow / Simulink + simulation-based repair`、`PAT/Event-B/timed automata` 的方法学价值高，但通常缺少 NL 或超出 STM family，只能作为 near-neighbor。

### 3.3 低命中特征 / 易误收模式

- 单纯 `model repair` 会大量命中 CAD、ML model、program repair、data repair 等非目标对象。
- 单纯 `state machine repair` 会命中 `STM + tests / oracle / error`，若没有 NL 与 `NL -> STM_0` 关系，不能作为本文 baseline。
- arXiv `LLM repair` 噪声极高，多为 program/code/math/citation repair。
- BPMN / process model、Event-B / CSP#、timed automata 与 STM 语义不同，只能作方法近邻，不能升级为同构 baseline。

## 4. 最终结论类型

| 类型 | 定义 | 代表 |
|---|---|---|
| 严格全绿 baseline | 明确满足 `<NL, STM_0> -> STM_k`，输入同时含 NL 与 `STM_0`，且 `STM_0` 明确由同一 NL 生成 / 派生；资源足以支撑可复验对照。 | 当前未确认 |
| P0 条件 baseline 候选 | 最接近硬定义，但至少一个关键条件仍需二次核验或资源不完整。 | `completion-sysml-gwt` |
| 生成链内 feedback / refinement 近邻 | `NL -> STM` 生成 pipeline 内含检查、错误反馈、再生成或 refinement，但不是独立 `<NL, STM_0> -> STM_k` repair baseline。 | `designing-fsm-gpt4-repair`、`ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` |
| repair-engine / partial-STM 近邻 | repair / completion / refinement 机制较强，但输入不含 NL 或缺少 `NL -> STM_0` 关系。 | `execution-partial-state-machine-models`、`flowrepair-stateflow-cps` |
| 异构形式化 repair 强近邻 | 目标工件不是本论文 STM family，但具备形式化 checker / prover / counterexample / proof feedback repair loop。 | `pat-agent`、`event-b-agent`、timed automata repair 簇 |
| 模型一致性 / 补全近邻 | repair 对象是 UML/SysML/BPMN/class/activity 等模型制品，提供 consistency / completion / diagnostics 维度，但不满足本文 baseline 硬门槛。 | `automatic-debugging-support-uml-designs`、`ai-driven-consistency-sysml`、`few-shot-model-completion`、`automated-bpmn-diagnostic-repair` |
| negative evidence | 标题或关键词相似，但对象、任务或资源不满足本论文 repair baseline 要求。 | 纯 `NL -> STM` seed、`STM + error/tests` 无 NL、program repair、protocol FSM、DL model repair |

## 5. 首批入库条目索引

| ID | 目录 | 标题 | 年份 | 当前角色 | 交叉链接 |
|---|---|---|---:|---|---|
| `completion-sysml-gwt` | [completion-sysml-gwt/](./completion-sysml-gwt/) | Completion of SysML state machines from Given-When-Then requirements | 2024 | P0 条件 baseline 候选 | seed 文库中按 repair-only 边界记录：[../seed_library/completion-sysml-gwt/](../seed_library/completion-sysml-gwt/) |
| `towards-automatic-model-completion` | [towards-automatic-model-completion/](./towards-automatic-model-completion/) | Towards Automatic Model Completion | 2022 | precursor / 条件线索 | [../seed_library/towards-automatic-model-completion/](../seed_library/towards-automatic-model-completion/) |
| `designing-fsm-gpt4-repair` | [designing-fsm-gpt4-repair/](./designing-fsm-gpt4-repair/) | Designing FSMs Specifications from Requirements with GPT 4.0 | 2026 | 生成链内 repair slice | seed 部分在 [../seed_library/designing-fsm-gpt4/](../seed_library/designing-fsm-gpt4/) |
| `ttool-ai-feedback` | [ttool-ai-feedback/](./ttool-ai-feedback/) | System Architects Are not Alone Anymore | 2024 | 生成链内 feedback-regeneration | seed/SMD 部分在 [../seed_library/ttool-ai-smd-subset/](../seed_library/ttool-ai-smd-subset/) |
| `llms-emp-feedback` | [llms-emp-feedback/](./llms-emp-feedback/) | Generating SysML Behavior Models via LLMs | 2025 | STM 子集 feedback-regeneration | seed/STM 部分在 [../seed_library/llms-emp-stm-subset/](../seed_library/llms-emp-stm-subset/) |
| `fsm-gen-iec-61499` | [fsm-gen-iec-61499/](./fsm-gen-iec-61499/) | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 仿真/用户 refinement 近邻 | seed 线索在 [../seed_library/fsm-gen-iec-61499/](../seed_library/fsm-gen-iec-61499/) |
| `execution-partial-state-machine-models` | [execution-partial-state-machine-models/](./execution-partial-state-machine-models/) | Execution of Partial State Machine Models | 2022 | partial STM refinement / execution 近邻 | 无 seed 交叉；无 NL 输入，作为 `STM_0 -> executable/refined STM` 近邻 |
| `flowrepair-stateflow-cps` | [flowrepair-stateflow-cps/](./flowrepair-stateflow-cps/) | FlowRepair: Search-based automated program repair of CPS controllers modeled in Simulink-Stateflow | 2026 | Stateflow repair-engine 近邻 | 无 seed 交叉；无 NL 输入，作为 `Stateflow STM_0 -> patched Stateflow` 近邻 |
| `automatic-debugging-support-uml-designs` | [automatic-debugging-support-uml-designs/](./automatic-debugging-support-uml-designs/) | Automatic Debugging Support for UML Designs | 2000 | 经典 statechart debugging 近邻 | project baseline 来源：[../../../baselines/automatic-debugging-support-for-uml-designs/](../../../baselines/automatic-debugging-support-for-uml-designs/) |
| `pat-agent` | [pat-agent/](./pat-agent/) | PAT-Agent: Autoformalization for Model Checking | 2025 | 异构形式化 repair 强近邻 | project baseline 来源：[../../../baselines/pat-agent-autoformalization-model-checking/](../../../baselines/pat-agent-autoformalization-model-checking/) |
| `event-b-agent` | [event-b-agent/](./event-b-agent/) | Event-B Agent | 2026 | 异构 formal-state repair 强近邻 | project baseline 来源：[../../../baselines/event-b-agent/](../../../baselines/event-b-agent/) |
| `ai-driven-consistency-sysml` | [ai-driven-consistency-sysml/](./ai-driven-consistency-sysml/) | AI-Driven Consistency of SysML Diagrams | 2024 | SysML consistency repair 近邻 | project baseline 来源：[../../../baselines/ai-driven-consistency-sysml-diagrams/](../../../baselines/ai-driven-consistency-sysml-diagrams/) |
| `few-shot-model-completion` | [few-shot-model-completion/](./few-shot-model-completion/) | Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | 弱近邻 model completion | project baseline 来源：[../../../baselines/few-shot-model-completion/](../../../baselines/few-shot-model-completion/) |
| `automated-bpmn-diagnostic-repair` | [automated-bpmn-diagnostic-repair/](./automated-bpmn-diagnostic-repair/) | Automated BPMN Model Generation from Textual Process Descriptions | 2026 | BPMN diagnostics-to-repair 方法近邻 | project baseline 来源：[../../../baselines/automated-bpmn-model-generation-textual-process-descriptions/](../../../baselines/automated-bpmn-model-generation-textual-process-descriptions/) |

## 6. 多维 baseline / related work 总表

本表把硬门槛拆开显示，避免把“强 repair 机制”误读成“本文 baseline”。其中 `NL -> STM_0` 是新增核心维度：若该列为 🔴，即使 repair 很强，也不能写成本文 `<NL, STM_0> -> STM_k` baseline。

| ID | 年份 | NL类型 | STM / 模型类型 | 修正输入 | 修正输出 | 方法 | feedback类型 | NL | STM0 | NL->STM0 | 修正 | 谱系 | 反馈 | 自动化 | LLM/Agent | baseline | 资源 | 当前角色 | 使用方式 | 主要风险 |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | 2024 | GWT 需求 | SysML SMD | GWT + partial SysML model / states | completed SMD transitions | MetaReq / MetaFragment / refinement rules | rule / feasibility / analyst | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | 🟡 | 🟠 | 🟡 | 🟠 | P0 条件 baseline 候选 | 主 baseline 候选 | partial SMD / states 是否严格由同一 NL 生成仍需二次核验；无公开机读数据包 |
| `towards-automatic-model-completion` | 2022 | BDD/GWT | SysML SMD | GWT + partial architecture / states | SMD fragments | ClauseExtractor + AST + completion rules | modeller check | 🟢 | 🟢 | 🟡 | 🟡 | 🟢 | 🟠 | 🟠 | 🔴 | 🟠 | 🟠 | precursor / 条件线索 | related / 历史线索 | 早期构想，工具链未落地；不独立计 baseline |
| `designing-fsm-gpt4-repair` | 2026 | 合成 DFSM 描述 | CSV DFSM / Mealy | generated DFSM + oracle / trace / fault model | repaired DFSM | oracle diff、distinguishing/checking sequence、mutation repair | oracle / expert / trace | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟠 | 🟠 | 🟠 | 生成链内 repair slice | feedback / repair 近邻 | repair 阶段主要是 STM + oracle/trace，不是 `<NL, STM_0>` 输入；合成数据、oracle 依赖 |
| `ttool-ai-feedback` | 2024 | 系统规范 | SysML/TTool SMD | generated SysML/TTool model + errors | regenerated model | TTool-AI feedback loop | JSON/syntax/constraint | 🟡 | 🟢 | 🟢 | 🟠 | 🟡 | 🟡 | 🟢 | 🟡 | 🟠 | 🟡 | 生成链内 feedback | related / 消融参考 | 反馈偏语法/约束；不是独立 repair task；复现依赖 TTool/OpenAI |
| `llms-emp-feedback` | 2025 | behavior requirements | SysML/PlantUML STM | generated model + Error(E) | regenerated behavior model | Phase-II checking feedback regeneration | format/grammar/semantic/requirements | 🟡 | 🟢 | 🟢 | 🟠 | 🟡 | 🟡 | 🟡 | 🟡 | 🟠 | 🟡 | STM 子集 feedback | related / 消融参考 | checking 含人工；需只取 STM 子集；不是独立 `<NL, STM_0>` baseline |
| `fsm-gen-iec-61499` | 2025 | 控制需求 + 用户 refinement | FSM / IEC 61499 ECC | FSM + user request + simulation observation | refined FSM / FB | NL refinement + simulation validation | user/simulation | 🟢 | 🟢 | 🟡 | 🟠 | 🟢 | 🟠 | 🟠 | 🟠 | 🟠 | 🔴 | 仿真/用户 refinement 近邻 | related / 工业动机 | 人在回路强；代码/数据未公开；非无人闭环 |
| `automatic-debugging-support-uml-designs` | 2000 | 无直接 NL | UML Statecharts | statecharts + annotated SD/domain theory | conflict explanations / patch search | backward consistency debugging | logical conflict/unification | 🔴 | 🟢 | 🔴 | 🟠 | 🟢 | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 | 经典 debugging 近邻 | related / 历史背景 | 输入不是 NL；工具不可复现；更像 debug/explanation |
| `execution-partial-state-machine-models` | 2022 | 无 | UML-RT HSM / partial state machine | partial UML-RT model + completeness setting | refined executable HSM + decision points / execution rules | static analysis + automatic refinement + input-driven execution | semantics diagnostics / stuck config / reachability | 🔴 | 🟢 | 🔴 | 🟡 | 🟢 | 🟢 | 🟡 | 🔴 | 🔴 | 🟡 | partial STM refinement 近邻 | related / 执行语义参考 | 无 NL；目标是可执行/调试而非需求语义 repair |
| `flowrepair-stateflow-cps` | 2026 | 无 | Simulink/Stateflow | buggy Stateflow model + tests/oracle + SBFL ranking | plausible / partial patches | SBFL/Tarantula + global/local search + 15 mutation operators | simulation / oracle / repair objectives | 🔴 | 🟢 | 🔴 | 🟢 | 🟡 | 🟢 | 🟡 | 🔴 | 🔴 | 🟡 | Stateflow repair-engine 近邻 | related / repair 引擎参考 | 无 NL；依赖 MATLAB/Simulink/Stateflow 与仿真 oracle，plausible patch 需人工验证 |
| `pat-agent` | 2025 | 系统描述 + properties | PAT/CSP# | generated CSP# + failed property | repaired CSP# | model checking counterexample repair | counterexample | 🟡 | 🟠 | 🔴 | 🟡 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟡 | 异构形式化近邻 | related / 方法上界 | 非 STM family；额外 property supervision |
| `event-b-agent` | 2026 | requirements | Event-B | Event-B model/proof + failures | repaired/refined Event-B | ProB/Rodin/proof-guided repair | proof / counterexample | 🟡 | 🟠 | 🔴 | 🟡 | 🔴 | 🟢 | 🟢 | 🟢 | 🔴 | 🟢 | 异构 formal-state 近邻 | related / 方法上界 | 非 STM family；运行成本高 |
| `ai-driven-consistency-sysml` | 2024 | system specification | SysML UCD/BD | inconsistent UCD/BD | corrected UCD/BD | rules + LLM inconsistency correction | consistency rules / TTool / user | 🟡 | 🟠 | 🔴 | 🟠 | 🟠 | 🟡 | 🟡 | 🟠 | 🔴 | 🟡 | consistency 近邻 | related / taxonomy | 实验主体不是 SMD / STM repair |
| `few-shot-model-completion` | 2023 | 无 | class/activity diagram | partial model | suggested model elements | few-shot sequence completion | 无 formal feedback | 🔴 | 🟠 | 🔴 | 🟠 | 🔴 | 🔴 | 🟡 | 🟠 | 🔴 | 🟡 | 弱近邻 model completion | related / 低优先 | activity/class 不是 STM，无 repair loop |
| `automated-bpmn-diagnostic-repair` | 2026 | process description | BPMN XML | non-compliant BPMN | repaired BPMN | SpiffWorkflow diagnostics + LLM localized repair | execution diagnostics | 🟡 | 🟠 | 🔴 | 🟠 | 🔴 | 🟢 | 🟢 | 🟡 | 🔴 | 🟠 | BPMN 方法近邻 | related / diagnostics 参考 | BPMN 非 STM，数据/代码未公开 |

## 7. 资源可获取性表

| ID | 论文 | 代码/工具 | 输入数据 | 初始模型 | 修正输出 | 原生 repair case | 许可 | 版本 | 资源说明 |
|---|---|---|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [DOI](https://doi.org/10.1007/s10270-024-01228-3)；未见公开代码/机读模型/完整数据包 |
| `towards-automatic-model-completion` | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/2210.03388)；仅论文本体可获取，论文小例子可重建，核心代码/数据不可复跑 |
| `designing-fsm-gpt4-repair` | 🟢 | ❓ | 🟠 | 🟠 | 🟠 | 🟠 | ❓ | ❓ | [arXiv](https://arxiv.org/abs/2603.29140)；论文外 [nl2fsm](https://github.com/Paul3246/nl2fsm) 只作待核线索 |
| `ttool-ai-feedback` | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 | ❓ | 🟡 | [HAL](https://telecom-paris.hal.science/hal-04483279) / [GitHub](https://github.com/zebradile/ttool-ai)；需冻结 commit 与许可 |
| `llms-emp-feedback` | 🟢 | 🔴 | 🟢 | 🟡 | 🟡 | 🟡 | ❓ | ❓ | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926) / [Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；pipeline 未公开 |
| `fsm-gen-iec-61499` | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/)；仅论文本体可获取，代码/数据未公开，不可作为可复跑 baseline |
| `automatic-debugging-support-uml-designs` | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/cs/0011017)；仅论文本体、示例和算法说明可获取，工具不可复跑 |
| `execution-partial-state-machine-models` | 🟢 | 🟡 | ⚪ | 🟡 | 🟡 | 🟡 | ❓ | ❓ | [DOI](https://doi.org/10.1109/TSE.2020.3008850) / [arXiv](https://arxiv.org/abs/2103.17194)；论文给出 [PMExec Bitbucket 入口](https://bitbucket.org/moji1/partialmodels)，但需核 license/commit；无 NL 输入 |
| `flowrepair-stateflow-cps` | 🟢 | 🟢 | 🟡 | 🟡 | ❓ | 🟡 | ❓ | 🟢 | [DOI](https://doi.org/10.1016/j.infsof.2025.108010) / [arXiv](https://arxiv.org/abs/2404.04688) / [GitHub](https://github.com/aitorarrietamarcos/StateflowRepairTool) / [Zenodo](https://zenodo.org/records/10936238)；需核 license、Zenodo 内容和 MATLAB/Simulink 环境 |
| `pat-agent` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ❓ | 🟡 | [arXiv](http://arxiv.org/abs/2509.23675) / [GitHub](https://github.com/ZuoXinyue/PAT-Agent)；需核 license/commit |
| `event-b-agent` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | ❓ | 🟢 | [arXiv](http://arxiv.org/abs/2605.17475) / [GitHub](https://github.com/HongshuW/EventB_Agent) / [Zenodo](https://doi.org/10.5281/zenodo.19642103) |
| `ai-driven-consistency-sysml` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | ❓ | 🟢 | [DOI](https://doi.org/10.1145/3640310.3674079) / [Zenodo](https://zenodo.org/records/12794339)；非 STM repair |
| `few-shot-model-completion` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 | ❓ | 🟡 | [DOI](https://doi.org/10.1109/ICSE-NIER58687.2023.00008) / [GitHub](https://github.com/meriembenchaaben/model-completion)；非 STM |
| `automated-bpmn-diagnostic-repair` | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/2604.12105)；仅论文本体可获取，完整 pipeline 和 387 对数据未公开，不可作为可复跑 baseline |

## 8. 人工下载 / 待全文队列

长 BibTeX 条目集中保存在 [manual_download_queue.bib](./manual_download_queue.bib)。当前队列用于后续人工下载或机构访问后再全文入库。`FlowRepair` 已因 arXiv 全文可得而移出队列并入库。

| 题名 | 年份 | 来源 | 入队原因 | 预期角色 |
|---|---:|---|---|---|
| Clock Bound Repair for Timed Systems | 2019 | CAV | timed automata repair 强簇；需全文 | 异构 formal repair / time-boundary |
| TarTar: A Timed Automata Repair Tool | 2020 | CAV | timed automata repair tool；需全文 | 工具近邻 |
| Automated repair for timed systems | 2021/2022 | FMSD | TarTar journal extension；需全文 | formal repair related |
| Repairing Timed Automata Clock Guards through Abstraction and Testing | 2019 | TAP@FM | clock guard repair；需全文 | timed automata related |
| Change-Preserving Model Repair | 2017 | FASE | model repair 经典；需全文 | UML/model repair related |
| Fixing Inconsistencies in UML Design Models | 2007 | ICSE | UML consistency repair 经典；需全文 | model consistency baseline |
| Generating and Evaluating Choices for Fixing Inconsistencies in UML Design Models | 2008 | ASE | repair choice generation；需全文 | model consistency baseline |
| Computing repair trees for resolving inconsistencies in design models | 2012 | ASE | repair tree 机制；需全文 | repair recommendation related |
| Software Model Evolution with Large Language Models | 2025 | ICSE | LLM model evolution / completion；需全文 | LLM model completion related |
| Multi-Location Software Model Completion | 2026 | ICSE | model completion 最新线索；仅会议页元数据，需正式论文/全文与作者信息 | 待核 |

## 9. negative evidence / 排除哨兵

| 类别 | 代表 | 处理理由 |
|---|---|---|
| 纯 `NL -> STM` seed | `sefm-llm-state-machine`、`umple`、`req`、`pushing-generative-envelope` | 若无修正/feedback 环节，回到 seed 文库，不写成本论文 baseline。 |
| protocol FSM | FlowFSM、SpecGPT / 3GPP extraction | 输出是网络协议 FSM，外部效度与控制系统 STM repair 不同；除非专门讨论 out-of-domain。 |
| program / code repair | RepairAgent、一般 APR / vulnerability repair | 目标制品是代码，不是 STM / UML / SysML 模型。 |
| BPMN / process model | BPMN diagnostic repair | `automated-bpmn-diagnostic-repair` 已在 §5 按方法近邻入账；它可作 diagnostics-to-repair 方法参照，但不是 STM baseline。 |
| class/activity completion | few-shot model completion | 模型补全维度有价值，但 activity/class 不能等同于 STM。 |
| formal spec repair | Alloy / TLA+ / Event-B / CSP# | 可作形式化 feedback 近邻；除 PAT/Event-B 等强近邻外不进核心 baseline。 |
| ML / DL model repair | HybridRepair 等 | “model” 指机器学习模型，不是建模制品。 |

## 10. 最终结论表

| 结论 | 条目 | 对本文的直接用途 | 写作边界 |
|---|---|---|---|
| 严格 baseline 暂未确认 | 当前 0 条 | 不能在论文中声称已有同构 baseline 已充分存在 | 后续若要升级，必须证明 `NL`、`STM_0`、`NL -> STM_0`、`STM_0 -> STM_k` 与资源可复验同时成立 |
| 唯一 P0 条件 baseline 候选 | `completion-sysml-gwt` | 可作为 completion baseline 的首要候选，用于对比“GWT/NL + partial SysML SMD -> completed SMD transitions” | 需明确它不是无人化 repair loop；还需核验 partial SMD / states 是否严格由同一组 GWT/NL 生成或仅为预置骨架 |
| 生成链内 feedback 只能支撑 story / 消融 | `designing-fsm-gpt4-repair`、`ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` | 支撑“NL->STM 后仍需 feedback / refinement”的论文动机，可对比反馈类型、自动化与 LLM 使用 | 不能替代 `<NL, STM_0> -> STM_k` baseline；特别是 `designing-fsm-gpt4-repair` 的 repair 阶段主要依赖 oracle/trace/fault-model |
| 强 repair engine 只能作近邻 | `flowrepair-stateflow-cps`、`execution-partial-state-machine-models` | 提供 Stateflow mutation/search、partial STM execution/refinement 等机制参考 | 无 NL 或无 `NL -> STM_0` 关系，不能作为本文 baseline；只能在 Related Work / ablation 设计中谨慎引用 |
| 异构形式化 repair 说明闭环范式正在出现 | `pat-agent`、`event-b-agent`、timed automata repair | 支撑 story：从 one-shot generation 转向 checker/prover/verifier-mediated repair | 目标工件不同，不能作为同格式实验 baseline |
| 模型一致性 / completion 文献提供 repair taxonomy | UML inconsistency、SysML consistency、model completion、BPMN diagnostics repair | 用于 Related Work、评价维度和风险讨论 | 不要把非 STM 模型补全或 BPMN diagnostics 写成 STM repair baseline |

## 11. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 18:35:00 | 按 `<NL, STM_0> -> STM_k` 且 `STM_0` 必须由同一 NL 生成 / 派生的硬定义收紧 baseline 口径；新增 `STM_0` 与 `NL -> STM_0` emoji 维度，并将除 `completion-sysml-gwt` 外的条目降级为 near-neighbor / related work。 |
| 2026-06-15 17:40:00 | 将 `flowrepair-stateflow-cps` 从人工队列升级为全文入库条目，补充 Stateflow repair-engine 近邻、资源入口、筛查账可复算统计与最终结论边界。 |
| 2026-06-15 16:50:00 | 补入 `execution-partial-state-machine-models` 与候选池筛查账，修正旧 direct baseline 计数口径。 |
| 2026-06-15 16:20:00 | 初始化 repair baseline SUMMARY，整合首批全文阅读条目、检索覆盖、人工下载队列、负例证据与最终结论。 |
