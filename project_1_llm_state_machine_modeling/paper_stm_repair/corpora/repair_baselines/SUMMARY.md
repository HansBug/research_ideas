# repair_baselines/SUMMARY.md

## 0. 论文集整体概况

本目录服务于第一篇论文 `<NL, STM_0> -> STM_k / Better STM` 主线，记录 STM 修正任务 baseline 与近邻工作。当前阶段性结论是：**完全同构的 `<NL, STM_0> -> STM_k` 自动 repair baseline 很少；更稳妥的学术定位是分层比较 direct/conditional baseline、生成链内 feedback、异构形式化 repair、模型一致性/补全近邻与 negative evidence**。

| 指标 | 当前值 |
|---|---:|
| 已建单篇目录 | 12 |
| 已完成独立全文阅读 / 等价独立全文阅读支撑 | 12 |
| 直接 / 强条件 baseline | 3 |
| 生成链内 feedback / refinement 近邻 | 3 |
| 异构形式化 repair 强近邻 | 2 |
| 模型一致性 / 补全 / diagnostics 近邻 | 4 |
| 人工下载 / 待全文队列 | 11 条 |

> 注：本目录不替代 [../seed_library/](../seed_library/)；`designing-fsm-gpt4`、`ttool-ai`、`llms-emp`、`fsm-gen-iec-61499` 等若同时具备 seed 与 repair/feedback 线索，必须按“seed 关系”和“repair 能力”分开记录。

## 1. emoji / enum 标准

正式表中 emoji 列只写 emoji，释义如下。有偏序关系的维度默认按 **🟢 > 🟡 > 🟠 > 🔴** 表达；`❓` 表示待核，`⚪` 表示不适用。

| 维度 | 🟢 | 🟡 | 🟠 | 🔴 | ❓ | ⚪ |
|---|---|---|---|---|---|---|
| 修正任务匹配 | 明确同构 `STM_0 -> STM_k` repair / completion | 模型制品 repair，可较清楚映射到 STM | 局部 feedback / consistency / completion 线索 | 无 repair / feedback | 待核 | 不适用 |
| STM 谱系匹配 | T0+FSM/HSM/EFSM/statechart 明确 | UML/SysML/Stateflow/IEC 61499 等可转换模型 | 状态机边界弱或需大量转换 | 非目标形式主义 / 非模型制品 | 待核 | 不适用 |
| NL 参与 | repair 输入同时含 NL 与 STM | 初始生成阶段含 NL，repair 阶段主要看模型 | 无 NL，但 repair 机制重要 | 与 NL/STM 无关 | 待核 | 不适用 |
| 反馈来源 | 结构化 diagnostics / verification / simulation / counterexample / proof | rule / test / consistency feedback | 人工审阅、弱反馈或非结构化反馈 | 无反馈 | 待核 | 不适用 |
| 自动化程度 | 无人化自动闭环 | 半自动，少量人工配置或选择 | 人在回路强依赖 | 手工方法 | 待核 | 不适用 |
| LLM / agent loop | 明确 LLM agentic repair loop | LLM self-refine / feedback regeneration | LLM 只做局部建议或前处理 | 无 LLM | 待核 | 不适用 |
| 可作为 baseline | 代码 / 数据 / 输入输出 / 许可基本可复验 | 可论文级重建或部分复现 | 只能概念对照 | 不可作为 baseline | 待核 | 不适用 |
| 资源可获取性 | 论文、代码、数据、输入输出、许可、版本清楚 | 关键资源部分公开 | 只能从论文图表 / 附录重建 | 关键资源不可得 | 待核 | 不适用 |

## 2. 检索覆盖表

本表记录 PR-R1.8-C 已执行或由独立任务完成的覆盖切片。命中数包含噪声；正式候选以 §6 为准。

| 切片 | 日期 | 来源 / 范围 | query / 方法 | 命中数 | 初筛留存 | 全文入库 | 排除 / 降级 | manual queue 增项 | 备注 |
|---|---|---|---|---:|---:|---:|---:|---:|---|
| `W-LOCAL` | 2026-06-15 | 本地 `baselines/`、[../seed_library/](../seed_library/)、`evidence/` | `repair / feedback / completion / checker / counterexample / simulation` 交叉核验 | 20+ | 12 | 12 | 8+ | 0 | 识别 seed+repair 分段共存与旧 baseline repair slice |
| `W-SE` | 2026-06-15 | SE / Modeling / Requirements venue 与本地候选 | state machine / UML / SysML + repair / completion / consistency | 20 | 15 | 6 | 5 | 5 | 独立候选发现任务给出 SoSyM、ICSE、ASE、EASE、SANER 等候选 |
| `W-FM` | 2026-06-15 | FM / CAV / TACAS / TAP / STTT / FMSD | timed automata / model checking / counterexample + repair | 15+ | 8 | 0 | 7 | 5 | timed automata repair 簇进入人工队列 / related |
| `W-ME` | 2026-06-15 | Maintenance / Evolution / empirical / quality | model consistency / model completion / model evolution | 10+ | 5 | 1 | 4 | 2 | LLM model evolution、model completion、inconsistency repair 多为条件 baseline |
| `W-ARXIV` | 2026-06-15 | arXiv 近三年 + OpenAlex / Crossref 辅助 | LLM state machine repair、Simulink-Stateflow repair、model completion LLM | 76 | 6 | 2 | 60+ | 3 | 噪声很高；FlowRepair / formal spec repair / model completion 为重点 |

## 3. 检索关键词簇分析

### 3.1 当前推荐关键词簇

- `state machine repair` / `statechart repair` / `SysML state machine completion` / `UML state machine repair`。
- `model completion` / `model repair` / `model consistency fixing` + `UML` / `SysML` / `Stateflow`。
- `counterexample-guided repair` / `verification-guided repair` / `simulation-guided repair` / `proof-guided repair`。
- `LLM model repair` / `LLM model completion` / `agentic repair formal model`。

### 3.2 高命中特征

- `partial SysML state machine + GWT requirements` 是最贴近本论文 repair/completion 任务的 direct cluster。
- `generation pipeline + checker feedback` 常见于 LLM4Modeling 工作，适合作为 feedback-regeneration 近邻。
- `PAT/Event-B/timed automata` 不是 STM family，但 checker / counterexample / proof feedback 的方法学价值高。
- UML multi-view inconsistency repair 能提供 repair action、recommendation、repair tree 等经典背景。

### 3.3 低命中特征 / 易误收模式

- 单纯 `model repair` 会大量命中 CAD、ML model、program repair、data repair 等非目标对象。
- 单纯 `state machine` 会命中 protocol FSM、automata learning、runtime workflow FSM，不一定是控制系统 STM。
- arXiv `LLM repair` 噪声极高，多为 program/code/math/citation repair。
- BPMN / process model 与 STM 语义不同，只能作方法近邻，不能升级为 direct baseline。

## 4. 最终结论类型

| 类型 | 定义 | 代表 |
|---|---|---|
| 直接 / 强条件 baseline | 明确以已有状态机或 partial state machine 为输入，输出补全或修正后的 state machine；或 repair slice 可以清楚切出。 | `completion-sysml-gwt`、`towards-automatic-model-completion`、`designing-fsm-gpt4-repair` |
| 生成链内 feedback baseline | `NL -> STM` 生成 pipeline 内含检查、错误反馈、再生成或 refinement，但不是独立 `STM_0 -> STM_k` repair 方法。 | `ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` |
| 异构形式化 repair 强近邻 | 目标工件不是本论文 STM family，但具备形式化 checker / prover / counterexample / proof feedback repair loop。 | `pat-agent`、`event-b-agent`、timed automata repair 簇 |
| 模型一致性 / 补全近邻 | repair 对象是 UML/SysML/BPMN/class/activity 等模型制品，提供 consistency / completion / diagnostics 维度。 | `automatic-debugging-support-uml-designs`、`ai-driven-consistency-sysml`、`few-shot-model-completion` |
| negative evidence | 标题或关键词相似，但对象、任务或资源不满足本论文 repair baseline 要求。 | 纯 `NL -> STM` seed、program repair、protocol FSM、DL model repair |

## 5. 首批入库条目索引

| ID | 目录 | 标题 | 年份 | 当前角色 | 交叉链接 |
|---|---|---|---:|---|---|
| `completion-sysml-gwt` | [completion-sysml-gwt/](./completion-sysml-gwt/) | Completion of SysML state machines from Given-When-Then requirements | 2024 | 直接/强条件 baseline | seed 文库中按 repair-only 边界记录：[../seed_library/completion-sysml-gwt/](../seed_library/completion-sysml-gwt/) |
| `towards-automatic-model-completion` | [towards-automatic-model-completion/](./towards-automatic-model-completion/) | Towards Automatic Model Completion | 2022 | precursor | [../seed_library/towards-automatic-model-completion/](../seed_library/towards-automatic-model-completion/) |
| `designing-fsm-gpt4-repair` | [designing-fsm-gpt4-repair/](./designing-fsm-gpt4-repair/) | Designing FSMs Specifications from Requirements with GPT 4.0 | 2026 | repair slice | seed 部分在 [../seed_library/designing-fsm-gpt4/](../seed_library/designing-fsm-gpt4/) |
| `ttool-ai-feedback` | [ttool-ai-feedback/](./ttool-ai-feedback/) | System Architects Are not Alone Anymore | 2024 | feedback-regeneration | seed/SMD 部分在 [../seed_library/ttool-ai-smd-subset/](../seed_library/ttool-ai-smd-subset/) |
| `llms-emp-feedback` | [llms-emp-feedback/](./llms-emp-feedback/) | Generating SysML Behavior Models via LLMs | 2025 | STM 子集 feedback-regeneration | seed/STM 部分在 [../seed_library/llms-emp-stm-subset/](../seed_library/llms-emp-stm-subset/) |
| `fsm-gen-iec-61499` | [fsm-gen-iec-61499/](./fsm-gen-iec-61499/) | LLM-based iterative requirements refinement in FSM with IEC 61499 code generation | 2025 | 仿真/用户 refinement 近邻 | seed 线索在 [../seed_library/fsm-gen-iec-61499/](../seed_library/fsm-gen-iec-61499/) |
| `automatic-debugging-support-uml-designs` | [automatic-debugging-support-uml-designs/](./automatic-debugging-support-uml-designs/) | Automatic Debugging Support for UML Designs | 2000 | 经典 statechart debugging | project baseline 来源：[../../../baselines/automatic-debugging-support-for-uml-designs/](../../../baselines/automatic-debugging-support-for-uml-designs/) |
| `pat-agent` | [pat-agent/](./pat-agent/) | PAT-Agent: Autoformalization for Model Checking | 2025 | 异构形式化 repair 强近邻 | project baseline 来源：[../../../baselines/pat-agent-autoformalization-model-checking/](../../../baselines/pat-agent-autoformalization-model-checking/) |
| `event-b-agent` | [event-b-agent/](./event-b-agent/) | Event-B Agent | 2026 | 异构 formal-state repair 强近邻 | project baseline 来源：[../../../baselines/event-b-agent/](../../../baselines/event-b-agent/) |
| `ai-driven-consistency-sysml` | [ai-driven-consistency-sysml/](./ai-driven-consistency-sysml/) | AI-Driven Consistency of SysML Diagrams | 2024 | SysML consistency repair 近邻 | project baseline 来源：[../../../baselines/ai-driven-consistency-sysml-diagrams/](../../../baselines/ai-driven-consistency-sysml-diagrams/) |
| `few-shot-model-completion` | [few-shot-model-completion/](./few-shot-model-completion/) | Towards using Few-Shot Prompt Learning for Automating Model Completion | 2023 | 弱近邻 model completion | project baseline 来源：[../../../baselines/few-shot-model-completion/](../../../baselines/few-shot-model-completion/) |
| `automated-bpmn-diagnostic-repair` | [automated-bpmn-diagnostic-repair/](./automated-bpmn-diagnostic-repair/) | Automated BPMN Model Generation from Textual Process Descriptions | 2026 | BPMN diagnostics-to-repair 方法近邻 | project baseline 来源：[../../../baselines/automated-bpmn-model-generation-textual-process-descriptions/](../../../baselines/automated-bpmn-model-generation-textual-process-descriptions/) |

## 6. 多维 baseline / related work 总表

| ID | 年份 | NL类型 | STM / 模型类型 | 修正输入 | 修正输出 | repair / feedback 方法 | 反馈来源 | 自动化 | LLM | Agent | 修正 | 谱系 | baseline | 资源 | 当前角色 | 主要风险 |
|---|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | 2024 | GWT 需求 | SysML SMD | GWT + partial SysML model / states | completed SMD transitions | MetaReq / MetaFragment / refinement rules | rule / feasibility / analyst | 半自动 | 前处理 | 否 | 🟢 | 🟢 | 🟡 | 🟠 | 直接/强条件 | 依赖结构化 GWT 和预置模型；无公开机读数据包 |
| `towards-automatic-model-completion` | 2022 | BDD/GWT | SysML SMD | GWT + partial architecture / states | SMD fragments | ClauseExtractor + AST + completion rules | modeller check | 概念半自动 | 否 | 否 | 🟢 | 🟢 | 🟠 | 🟠 | precursor | 早期构想；工具链未落地 |
| `designing-fsm-gpt4-repair` | 2026 | 合成 DFSM 描述 | CSV DFSM / Mealy | generated DFSM + oracle / trace / fault model | repaired DFSM | oracle diff、distinguishing/checking sequence、mutation repair | oracle / expert / trace | 半自动 | GPT-4/4o | 否 | 🟢 | 🟢 | 🟡 | 🟠 | repair slice | 合成数据、oracle 依赖、语义弱 |
| `ttool-ai-feedback` | 2024 | 系统规范 | SysML/TTool SMD | generated SysML/TTool model + errors | regenerated model | TTool-AI feedback loop | JSON/syntax/constraint | 自动为主 | GPT-3.5 | 否 | 🟡 | 🟡 | 🟡 | 🟡 | 生成链内 feedback | 反馈偏语法/约束；复现依赖 TTool/OpenAI |
| `llms-emp-feedback` | 2025 | behavior requirements | SysML/PlantUML STM | generated model + Error(E) | regenerated behavior model | Phase-II checking feedback regeneration | format/grammar/semantic/requirements | 半自动 | 多模型 | 否 | 🟡 | 🟡 | 🟡 | 🟡 | STM 子集 feedback | checking 含人工；需只取 STM 子集 |
| `fsm-gen-iec-61499` | 2025 | 控制需求 | FSM / IEC 61499 ECC | FSM + user request + simulation observation | refined FSM / FB | NL refinement + simulation validation | user/simulation | 人在回路 | 未明确 | 否 | 🟡 | 🟢 | 🟠 | 🔴 | 仿真/用户 refinement | 代码/数据未公开；非无人闭环 |
| `automatic-debugging-support-uml-designs` | 2000 | 无直接 NL | UML Statecharts | statecharts + annotated SD/domain theory | conflict explanations / patch search | backward consistency debugging | logical conflict/unification | 半自动 | 无 | 否 | 🟡 | 🟡 | 🟠 | 🔴 | 经典 debugging | 输入不是 NL；工具不可复现 |
| `pat-agent` | 2025 | 系统描述 + properties | PAT/CSP# | generated CSP# + failed property | repaired CSP# | model checking counterexample repair | counterexample | 自动 | o3-mini / Claude / DeepSeek | 是 | 🟡 | 🔴 | 🟠 | 🟡 | 异构形式化近邻 | 非 STM family；额外 property supervision |
| `event-b-agent` | 2026 | requirements | Event-B | Event-B model/proof + failures | repaired/refined Event-B | ProB/Rodin/proof-guided repair | proof / counterexample | 自动 | GPT-5 | 是 | 🟡 | 🔴 | 🟠 | 🟢 | 异构 formal-state 近邻 | 非 STM family；运行成本高 |
| `ai-driven-consistency-sysml` | 2024 | system specification | SysML UCD/BD | inconsistent UCD/BD | corrected UCD/BD | rules + LLM inconsistency correction | consistency rules / TTool / user | 半自动 | OpenAI GPT | 否 | 🟠 | 🟠 | 🟠 | 🟡 | consistency 近邻 | 实验主体不是 SMD |
| `few-shot-model-completion` | 2023 | 无 | class/activity diagram | partial model | suggested model elements | few-shot sequence completion | 无 formal feedback | 部分自动 | GPT-3 | 否 | 🟠 | 🔴 | 🟠 | 🟡 | 弱近邻 | activity/class 不是 STM，无 repair loop |
| `automated-bpmn-diagnostic-repair` | 2026 | process description | BPMN XML | non-compliant BPMN | repaired BPMN | SpiffWorkflow diagnostics + LLM localized repair | execution diagnostics | 自动为主 | GPT-4o / Gemini | 否 | 🟠 | 🔴 | 🟠 | 🟠 | 方法近邻 | BPMN 非 STM，数据/代码未公开 |

## 7. 资源可获取性表

| ID | 论文 | 代码/工具 | 输入数据 | 初始模型 | 修正输出 | 原生 repair case | 许可 | 版本 | 资源说明 |
|---|---|---|---|---|---|---|---|---|---|
| `completion-sysml-gwt` | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [DOI](https://doi.org/10.1007/s10270-024-01228-3)；未见公开代码/机读模型/完整数据包 |
| `towards-automatic-model-completion` | 🟢 | 🔴 | 🟠 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/2210.03388)；论文小例子可重建 |
| `designing-fsm-gpt4-repair` | 🟢 | ❓ | 🟠 | 🟠 | 🟠 | 🟠 | ❓ | ❓ | [arXiv](https://arxiv.org/abs/2603.29140)；论文外 [nl2fsm](https://github.com/Paul3246/nl2fsm) 只作待核线索 |
| `ttool-ai-feedback` | 🟢 | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 | ❓ | 🟡 | [HAL](https://telecom-paris.hal.science/hal-04483279) / [GitHub](https://github.com/zebradile/ttool-ai)；需冻结 commit 与许可 |
| `llms-emp-feedback` | 🟢 | 🔴 | 🟢 | 🟡 | 🟡 | 🟡 | ❓ | ❓ | [ACM DOI](https://dl.acm.org/doi/10.1145/3755881.3755926) / [Drive](https://drive.google.com/drive/folders/10eo8KDqlBlkQZxPpPCB7R3-aBQZ7Rsm6?usp=drive_link)；pipeline 未公开 |
| `fsm-gen-iec-61499` | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11279575/)；代码/数据未公开 |
| `automatic-debugging-support-uml-designs` | 🟢 | 🔴 | 🔴 | 🟠 | 🟠 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/cs/0011017)；仅示例和算法说明 |
| `pat-agent` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | ❓ | 🟡 | [arXiv](http://arxiv.org/abs/2509.23675) / [GitHub](https://github.com/ZuoXinyue/PAT-Agent)；需核 license/commit |
| `event-b-agent` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | ❓ | 🟢 | [arXiv](http://arxiv.org/abs/2605.17475) / [GitHub](https://github.com/HongshuW/EventB_Agent) / [Zenodo](https://doi.org/10.5281/zenodo.19642103) |
| `ai-driven-consistency-sysml` | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟠 | ❓ | 🟢 | [DOI](https://doi.org/10.1145/3640310.3674079) / [Zenodo](https://zenodo.org/records/12794339)；非 STM repair |
| `few-shot-model-completion` | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🔴 | ❓ | 🟡 | [DOI](https://doi.org/10.1109/ICSE-NIER58687.2023.00008) / [GitHub](https://github.com/meriembenchaaben/model-completion)；非 STM |
| `automated-bpmn-diagnostic-repair` | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | [arXiv](https://arxiv.org/abs/2604.12105)；完整 pipeline 和 387 对数据未公开 |

## 8. 人工下载 / 待全文队列

长 BibTeX 条目集中保存在 [manual_download_queue.bib](./manual_download_queue.bib)。当前队列用于后续人工下载或机构访问后再全文入库。

| 题名 | 年份 | 来源 | 入队原因 | 预期角色 |
|---|---:|---|---|---|
| Clock Bound Repair for Timed Systems | 2019 | CAV | timed automata repair 强簇；需全文 | 异构 formal repair / time-boundary |
| TarTar: A Timed Automata Repair Tool | 2020 | CAV | timed automata repair tool；需全文 | 工具近邻 |
| Automated repair for timed systems | 2021/2022 | FMSD | TarTar journal extension；需全文 | formal repair related |
| Repairing Timed Automata Clock Guards through Abstraction and Testing | 2019 | TAP@FM | clock guard repair；需全文 | timed automata related |
| FlowRepair: Search-based automated program repair of CPS controllers modeled in Simulink-Stateflow | 2026 | IST | Stateflow/CPS controller repair 强近邻；需全文 | 条件 baseline / Stateflow related |
| Change-Preserving Model Repair | 2017 | FASE | model repair 经典；需全文 | UML/model repair related |
| Fixing Inconsistencies in UML Design Models | 2007 | ICSE | UML consistency repair 经典；需全文 | model consistency baseline |
| Generating and Evaluating Choices for Fixing Inconsistencies in UML Design Models | 2008 | ASE | repair choice generation；需全文 | model consistency baseline |
| Computing repair trees for resolving inconsistencies in design models | 2012 | ASE | repair tree 机制；需全文 | repair recommendation related |
| Software Model Evolution with Large Language Models | 2025 | ICSE | LLM model evolution / completion；需全文 | LLM model completion related |
| Multi-Location Software Model Completion | 2026 | ICSE | model completion 最新线索；需正式论文/全文 | 待核 |

## 9. negative evidence / 排除哨兵

| 类别 | 代表 | 处理理由 |
|---|---|---|
| 纯 `NL -> STM` seed | `sefm-llm-state-machine`、`umple`、`req`、`pushing-generative-envelope` | 若无修正/feedback 环节，回到 seed 文库，不写成本论文 baseline。 |
| protocol FSM | FlowFSM、SpecGPT / 3GPP extraction | 输出是网络协议 FSM，外部效度与控制系统 STM repair 不同；除非专门讨论 out-of-domain。 |
| program / code repair | RepairAgent、一般 APR / vulnerability repair | 目标制品是代码，不是 STM / UML / SysML 模型。 |
| BPMN / process model | BPMN diagnostic repair | 可作 diagnostics-to-repair 方法近邻，但不是 STM baseline。 |
| class/activity completion | few-shot model completion | 模型补全维度有价值，但 activity/class 不能等同于 STM。 |
| formal spec repair | Alloy / TLA+ / Event-B / CSP# | 可作形式化 feedback 近邻；除 PAT/Event-B 等强近邻外不进核心 baseline。 |
| ML / DL model repair | HybridRepair 等 | “model” 指机器学习模型，不是建模制品。 |

## 10. 最终结论表

| 结论 | 条目 | 对本文的直接用途 | 写作边界 |
|---|---|---|---|
| direct / strong conditional baseline 很少但存在 | `completion-sysml-gwt`、`designing-fsm-gpt4-repair` | 支撑“已有方法可做 partial STM completion 或 FSM repair slice” | 不要声称已有大量同构无人 repair baseline |
| generation feedback 是最贴近 LLM4Modeling 的可比线 | `ttool-ai-feedback`、`llms-emp-feedback`、`fsm-gen-iec-61499` | 可对比我们 feedback 的结构化程度、自动化程度、仿真/诊断深度 | 必须说明它们多为生成链内 feedback，不是独立 repair task |
| formal repair 说明闭环范式正在出现 | `pat-agent`、`event-b-agent`、timed automata repair | 支撑 story：从 one-shot generation 转向 checker/prover/verifier-mediated repair | 目标工件不同，不能作为同格式实验 baseline |
| 模型一致性 / completion 文献提供 repair taxonomy | UML inconsistency、SysML consistency、model completion | 用于 Related Work、评价维度和风险讨论 | 不要把非 STM 模型补全写成 STM repair |
| 实验 baseline 需要谨慎降级 | 当前多数条目资源不全或对象不匹配 | 后续 RQ/实验应采用主 baseline + related + ablation 分层 | 可复现实验必须等待 R2/R3/R6 冻结输入、转换器和评价门 |

## 11. 更新日志

| 时间 | 更新内容 |
|---|---|
| 2026-06-15 16:20:00 | PR-R1.8-C 初始化 repair baseline SUMMARY，整合 12 个全文阅读条目、检索覆盖、人工下载队列、负例证据 与最终结论。 |
