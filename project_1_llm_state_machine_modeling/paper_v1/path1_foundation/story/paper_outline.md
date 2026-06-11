# Path-1 第一篇论文章节大纲与 Related Work 主线草案

本文档是 PR #96 / S0a 的论文 outline 草案，只冻结 **story、章节顺序、Related Work 分层和 claim gate**，不冻结最终 venue、不写最终 abstract、不声明实验结果。当前论文主线不再围绕“首个自然语言到状态机生成”，而围绕：

> 在自然语言控制系统需求到状态机模型的任务中，能否通过机器可检查、可执行的状态机表示，把 LLM 初始生成转化为可由确定性 diagnostics、scenario-level simulation feedback 与 structured repair decision 支撑的闭环，并用 baseline-aware protocol 检验其边际作用。

## 1. S0a 写作锚点

1. **不争“会生成状态机”**：S1a 九篇 baseline 已覆盖 NL / 文档到 FSM、UML state machine、SysML behavior、Umple、Mermaid、TTool/SysML、protocol FSM、prompt chaining、RAG、tool feedback 与部分 repair loop。
2. **贡献只围绕反馈闭环机制**：输出表示、确定性 diagnostics、场景仿真反馈、结构化修复决策、baseline-aware evaluation；`pyfcstm`、run record、agent framework 和 prompt 技巧都只是支撑条件。
3. **E1/E2 是实验条件**：自建 agent-loop 与成熟 coding-agent skill route 用于比较 orchestration condition，不作为 hybrid method contribution。
4. **run record 只作证据链**：用于复核、打假、排障、eligibility 与 redaction，不作为论文贡献 bullet。
5. **prior work 边界要公平**：private GT、缺失代码、缺失 prompt、provider drift 只能写成 comparability / reproducibility boundary，不写成 prior work weakness。

## 2. 论文 thesis、gap 与技术挑战

### 2.1 Thesis

本文研究一种 LLM 状态机建模闭环：将自然语言控制系统需求映射到机器可检查且可执行的状态机表示，并把确定性 diagnostics、scenario-level simulation evidence 与 structured repair decision 纳入迭代生成过程；论文评估这些反馈信号在 frozen sample、component-level human adjudication 和 baseline-aware comparison 下是否产生可防守的模型质量与修复稳定性边际变化。

### 2.2 Gap

已有 closest works 已经展示了 NL-to-state-machine family generation、SysML/MBSE tool feedback、rule-based regeneration 与 oracle/trace repair。尚需收敛检验的是：在控制系统需求场景中，**同一受控协议**下将 executable representation、deterministic diagnostics、scenario simulation 和 structured repair decision 组合为反馈数据流时，哪些质量问题被发现、哪些修复决策可审计、哪些 apparent differences 只是由样本 / oracle / 预算差异造成。

### 2.3 Technical challenge

- NL 需求中的状态、事件、guard、action、变量、异常路径和时序暗示不天然对齐到状态机组件。
- 静态 diagnostics 能发现 parse/schema/consistency 问题，但不能替代 behavior oracle。
- Scenario candidates 可能暴露行为缺陷，也可能引入 oracle drift，必须由 deterministic simulator 与 human adjudication 分层处理。
- 修复循环可能振荡、过修或退化，因此需要 accept/reject、diff、FixLog 与回归检查。
- Baseline 比较不能把不同输入上下文、输出语义、人工预算或私有 GT 强行横向排名。

## 3. 建议 RQ

| RQ | 核心问题 | 必需证据 | 失败时的降级写法 |
|---|---|---|---|
| RQ1 Diagnostics | parse / semantic / design diagnostics 能识别哪些状态机组件缺陷，并如何改变后续修复请求？ | diagnostics code、component-level defect mapping、B0/B1/B2 消融、human adjudication | 只报告 diagnostics coverage 与盲区，不宣称整体质量提升 |
| RQ2 Simulation feedback | scenario-level simulation pass/fail、trace 与 behavior evidence 是否发现静态 diagnostics 难以暴露的问题？ | scenario candidates、deterministic simulator traces、B3/B4 消融、oracle 审计 | 写成 simulation feedback failure taxonomy / exploratory evidence |
| RQ3 Structured repair | structured fix request、accept/reject、diff、FixLog 与回归检查如何影响修复过程的可审计性和稳定性？ | repair attempts、convergence / regression / oscillation 统计、representative traces | 只说 structured repair decision 使失败可复盘，不说提高质量 |
| RQ4 Baseline positioning | 在 closest baseline 的 same-sample approximate / near / evidence-only 分层下，本文闭环相对已有生成、工具反馈和 trace repair 的边际在哪里？ | 至少一个 same-sample approximate baseline、baseline budget table、eligibility filter | 降级为 diagnostic protocol / baseline-aware positioning study |
| RQ5 Orchestration condition | 同一方法底座在自建 agent-loop 与成熟 coding-agent skill route 下的质量、成本、失败模式有何差异？ | E1/E2 同样本或可比样本 run record、usage、failure mode | 写成 implementation / reproducibility analysis，不作为贡献 |

## 4. 章节大纲草案

### 1 Introduction

- 开场问题：控制系统状态机只有在可检查、可执行、可追溯时，才可能支撑后续验证、诊断和修复。
- 承认现状：近期 LLM 工作已经覆盖自然语言到 FSM/UML/SysML/Umple/TTool/协议状态机的生成。
- 缺口转向：问题不是“LLM 能不能画状态机”，而是“反馈信号如何进入生成-诊断-仿真-修复闭环，并在公平 baseline 协议下被评估”。
- 贡献表述必须是 planned / evidence-backed：executable representation substrate、deterministic diagnostics、scenario-level simulation feedback、structured repair decision、baseline-aware evaluation。
- 禁止写法：`first NL-to-STM`、`first feedback loop`、`new DSL`、`prior work only draws diagrams`、`we show improvement`。

### 2 Background and Task Definition

- 定义输入：自然语言控制系统需求与必要上下文。
- 定义输出：machine-checkable and executable state-machine representation；说明它是检查 / 仿真 / 反馈底座，不是论文主打的新建模语言。
- 定义组件：states、events、transitions、guards、actions/effects、variables、hierarchy（若支持）、scenario behavior。
- 定义反馈：diagnostics feedback、simulation feedback、repair decision feedback；明确不等同 complete model checking / theorem proving / certification。
- 定义评价：component-level human adjudication、deterministic validity、scenario pass/fail、repair convergence、eligibility filter。

### 3 Related Work and Baseline Positioning

#### 3.1 Mandatory closest works first

Related Work 第一节必须先列出四个 mandatory closest works，而不是先泛泛讲 LLM 或 formal methods。

| Closest work | 已覆盖能力 | 本文边际差异 | 不能写的弱化 novelty |
|---|---|---|---|
| Structure/Event SMF | 非结构化 reactive-system NL → UML state machine；支持 states / transitions / guards / actions / hierarchy 等组件级 F1；artifact 可访问 | 本文不争 NL→UML SM 生成，而聚焦控制系统需求下的 executable target、deterministic diagnostics、scenario simulation 与 structured repair decision | 不能写“自由文本到状态机无人做过” |
| LLMs for EMP | NL → PlantUML/SysML behavior models；STM/ACT/SD 数据；PlantUML/SysML rule-based checking feedback 与 regeneration | 本文需把 rule feedback 与 executable scenario trace feedback 区分；若实验支持，只主张 diagnostics + simulation + repair decision 的组合协议 | 不能写“首次 tool feedback / feedback regeneration” |
| TTool-AI | ChatGPT 集成 TTool/MBSE；NL → SysML blocks/state machines；JSON/constraint/TTool syntax feedback loop；artifact/ODS 可复核 | 本文边际不是工具集成，而是控制需求专用 executable loop、scenario-level simulation as feedback signal、structured fix decision 与 baseline-aware evaluation | 不能把 TTool 的工具背景 model checker/simulator 误写成 prior work 未使用任何反馈 |
| Designing FSMs | 合成 NL → CSV DFSM/Mealy；oracle、distinguishing trace、checking sequence 与 fault-model repair | 本文不能声称 trace/repair 首创；差异限定为真实/准真实控制需求、guard/action/变量等更丰富语义、scenario candidates + deterministic simulator execution + structured decision log | 不能写“首次 trace repair / oracle repair” |

#### 3.2 Near executable/modeling works

- Umple / NL-to-code state machine：作为 structured / RAG / few-shot prompt baseline 或 near work，不把 RAG/few-shot 写成本文 novelty。
- Automotive statechart generation：领域近但数据、微调、专家 GT 私有；用于 evidence-only 或 domain motivation，不写成可直接击败的 direct baseline。
- Pushing the Generative Envelope / MBSE artifacts：用于 prompt-technique 与 SysML v2 artifact trend，不作为 strict STM baseline。

#### 3.3 Protocol FSM、长规格与 boundary works

- FlowFSM、SpecGPT 等长文档 / 协议 FSM 工作说明 prompt chaining、CoT、ensemble、JSON 校验和 expert GT 已覆盖相邻能力；由于领域、输出语义、GT 和 artifact 边界，不强行纳入 direct baseline。
- TLA+、PAT、Event-B、Petri net、BPMN、LTL/STL、property generation 等快速扩张邻域进入 boundary discussion，不能混称 exact STM direct baseline。
- 经典 requirements-to-formal-model / controlled natural language 工作作为 rigor background，不能因“无 LLM”而贬低为不相关。

#### 3.4 Related Work 收束句

本节最后收束到：已有工作分别覆盖了状态机族生成、SysML/MBSE 工具反馈、规则反馈再生成和 oracle/trace repair；本文的可评估空间是这些能力在控制系统状态机任务中以 executable representation、deterministic diagnostics、scenario-level simulation feedback 与 structured repair decision 组合成受控闭环时的边际效果。

### 4 Method

- Overview：NL requirement → initial STM draft → deterministic diagnostics → scenario candidate generation → deterministic simulation → structured repair decision → regression check。
- Representation：machine-checkable executable state-machine representation；`pyfcstm` 仅放 implementation / artifact。
- Deterministic diagnostics：parse、schema、semantic、design / inspect diagnostics；输出 code、message、location、affected component。
- Scenario feedback：LLM 生成需求相关 scenario candidates；deterministic simulator 执行并产出 pass/fail、trace、witness / counterexample-like evidence；human oracle 只裁决 scenario relevance 与组件正确性。
- Structured repair decision：fix request、accept/reject、diff、FixLog、rollback/regression policy。
- Evidence chain：run record 保存 prompt、raw output、usage、stage trace、diagnostics、scenario、diff、eligibility、redaction；作为复核支撑，不作为贡献。

### 5 Experimental Protocol

- Sample registry：样本来源、冻结时间、纳入 / 排除标准、stress-test 与 main benchmark 区分。
- Baseline layering：same-sample approximate、near、evidence-only、boundary；至少一个 closest work 进入 same-sample approximate，优先 Structure/Event SMF 或 LLMs for EMP STM 子集。
- Ablations：B0 direct prompting、B1 structured prompting、B2 no-feedback orchestration、B3 diagnostics-only、B4 diagnostics + scenario simulation、B5 full feedback + structured repair；EXT 单独报告 closest-work approximate baseline，E1/E2 只作 orchestration condition / appendix analysis。
- Human protocol：组件级 rubric、至少两名标注人、blind / independent coding、agreement、adjudication、disagreement log。
- Budget protocol：统一模型、prompt context、feedback rounds、human budget、tool budget、eligibility filter。

### 6 Results

- RQ1：diagnostics coverage、invalid-to-valid transitions、component defect distribution。
- RQ2：simulation feedback 发现的 behavior-level failures、scenario pass/fail、trace-level examples。
- RQ3：repair convergence、regression、oscillation、accept/reject reasons、FixLog completeness。
- RQ4：closest baseline comparison；不同层级 baseline 不放入同一“胜负排名”表。
- RQ5：E1/E2 orchestration condition 的质量、成本、失败模式与审计差异。

### 7 Failure Analysis and Case Study

- 展示成功、失败、振荡、过修、oracle drift 各类代表样本。
- 对每个 case 展示 diagnostics → scenario trace → repair decision → regression outcome。
- 明确哪些问题由确定性工具发现，哪些只能由 human adjudication 发现。

### 8 Threats to Validity and Limitations

- Baseline fairness：输入、输出、GT、artifact、prompt、模型预算和人工预算不可完全对齐。
- Reproducibility boundary：缺代码、缺 prompt、private GT、provider drift 是 comparability/reproducibility boundary，不是 prior work weakness。
- Oracle risk：scenario candidates 与 human adjudication 都可能偏移；LLM-as-Judge 不能作为主 oracle。
- Formal scope：本文是 executable feedback / simulation，不是 complete verification、BMC/LTL/theorem proving 或 certification。
- Generality：Path-2 深控制系统语义、时间自动机、BMC/LTL、工业认证留给后续工作。

### 9 Artifact and Conclusion

- Artifact：代码、grammar/schema、sample registry、prompt、raw output、run records、diagnostics、scenario traces、human rubric、result tables、redaction report。
- Conclusion 只能回到已由实验支持的范围：哪些反馈源有效、哪些失败暴露边界、哪些 baseline 比较可防守。
- 不写 SOTA / solved / complete verification / industrial certification。

## 5. Related Work / Baseline 写作红线

| 禁止 claim | 为什么禁止 | 安全替代表述 |
|---|---|---|
| 首个 NL / 文档到状态机生成方法 | 九篇 direct baseline 已覆盖 FSM、UML SM、SysML behavior、Umple、TTool、protocol FSM | “we study executable feedback for LLM-based state-machine modeling” |
| 首个 tool feedback / 自动修复闭环 | LLMs for EMP、TTool-AI 已有 rule/tool feedback；Designing FSMs 已有 trace/oracle repair | “we combine deterministic diagnostics, scenario simulation, and structured repair decisions under a controlled protocol” |
| prior work only draws diagrams | 多篇已有 machine-readable / tool-backed outputs | “prior work differs in feedback type, execution semantics, evaluation protocol, and comparability boundary” |
| `fcstm` / `pyfcstm` 是新 DSL 贡献 | S0a 术语策略要求弱化工程名 | “an internal implementation substrate for executable checking and simulation” |
| private GT / missing code 是 prior weakness | 这是复现边界，不是方法缺陷 | “strict replication is blocked by private assets / missing prompt / output mismatch; we therefore classify it as evidence-only or near” |

## 6. 投稿与 S0b 边界

S0a 不冻结最终投稿期刊，也不宣布达到 CCF-A 标准。`venue_readiness_gate.md` 只能作为后续 S0b / Direction + Venue Freeze 的输入。当前 outline 的验收标准是：Related Work 分层、RQ、Method 和 Experiment 已经不会把论文带回“首创状态机生成”或“新 DSL 贡献”的旧主线。

## 7. 当前 foundation 允许说什么

当前允许说：

- 已把第一篇论文主线收缩为 diagnostics / simulation feedback / structured repair decision 的受控闭环研究。
- 已识别四个 mandatory closest works 对 claim 的 carve-out。
- 已规划 Related Work 第一层与 baseline 分层，避免把不可比较工作硬当 direct baseline。

当前不能说：

- 方法已经优于 baseline。
- 样本、oracle、baseline runner 或消融已经冻结。
- 可执行反馈已经被证明提升质量或修复稳定性。
- 本文提出了新的 paper-level DSL 或完成了完整形式化验证。
