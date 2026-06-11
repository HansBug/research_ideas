# Path-1 第一篇论文章节大纲与 Related Work 主线草案

本文档是 PR #96 / S0a 的论文 outline 草案，只冻结 **story、章节顺序、Related Work 分层和 claim gate**，不冻结最终 venue、不写最终 abstract、不声明实验结果。当前论文主线不再围绕“首个自然语言到状态机生成”，而围绕：

> 在自然语言控制系统需求到状态机模型的任务中，能否通过机器可检查、可执行的状态机表示，把 LLM 初始生成转化为可由确定性诊断、场景级仿真反馈与结构化修复决策支撑的闭环，并用基线感知协议检验其边际作用。

## 1. S0a 写作锚点

1. **不争“会生成状态机”**：S1a 九篇 baseline 已覆盖 NL / 文档到 FSM、UML state machine、SysML behavior、Umple、Mermaid、TTool/SysML、protocol FSM、prompt chaining、RAG、tool feedback 与部分 repair loop。
2. **贡献只围绕反馈闭环机制**：输出表示、确定性诊断、场景仿真反馈、结构化修复决策、基线感知评估；`pyfcstm`、agent framework 和 prompt 技巧都只是实现或实验条件。
3. **E1/E2 是实验条件**：自建 agent-loop 与成熟 coding-agent skill route 用于比较编排条件，不作为 hybrid method contribution。
4. **过程性工程材料不进入论文主线**：不写成 Method 段落或 contribution bullet。
5. **prior work 边界要公平**：私有 GT、缺失代码、缺失 prompt、供应商 / 模型漂移 只能写成可比性 / 复现边界，不写成 prior work weakness。

## 2. 论文 thesis、gap 与技术挑战

### 2.1 Thesis

本文研究一种 LLM 状态机建模闭环：将自然语言控制系统需求映射到机器可检查且可执行的状态机表示，并把确定性诊断、场景级仿真证据与结构化修复决策纳入迭代生成过程；论文评估这些反馈信号在冻结样本、组件级人工裁决和基线感知比较下是否产生可防守的模型质量与修复稳定性边际变化。

### 2.2 Gap

已有最接近工作已经展示自然语言到状态机族工件生成、SysML / MBSE 工具反馈、规则反馈再生成与 oracle / 轨迹修复。尚需收敛检验的是：在控制系统需求场景中，**同一受控协议**下将可执行表示、确定性诊断、场景仿真和结构化修复决策组合为反馈数据流时，哪些质量问题被发现、哪些修复决策可复核、哪些表观差异只是由样本、oracle 或预算差异造成。

### 2.3 Technical challenge

- 自然语言需求中的状态、事件、guard、action、变量、异常路径和时序暗示不天然对齐到状态机组件。
- 静态诊断能发现 parse / schema / consistency 问题，但不能替代行为 oracle。
- 场景候选可能暴露行为缺陷，也可能引入 oracle drift，必须由确定性仿真器与人工裁决分层处理。
- 修复循环可能振荡、过修或退化，因此需要接受 / 拒绝、差异记录、FixLog 与回归检查。
- 基线比较不能把不同输入上下文、输出语义、人工预算或私有 GT 强行横向排名。

## 3. 建议 RQ

| RQ | 核心问题 | 必需证据 | 失败时的降级写法 |
|---|---|---|---|
| RQ1 诊断反馈 | parse / semantic / design diagnostics 能识别哪些状态机组件缺陷，并如何改变后续修复请求？ | 诊断编号、组件级缺陷映射、B0/B1/B2 消融、人工裁决 | 只报告诊断覆盖率与盲区，不宣称整体质量提升 |
| RQ2 场景仿真反馈 | 场景级仿真的通过 / 失败、执行轨迹与行为证据是否能发现静态诊断难以暴露的问题？ | 场景候选、确定性仿真轨迹、B3/B4 消融、oracle 复核 | 写成场景仿真反馈的失败分类或探索性证据 |
| RQ3 结构化修复决策 | 结构化修复请求、接受 / 拒绝、差异记录、FixLog 与回归检查如何影响修复过程的可复核性和稳定性？ | 修复尝试、收敛 / 回退 / 振荡统计、代表性轨迹 | 只说结构化修复决策使失败可复盘，不说提高质量 |
| RQ4 基线定位 | 在最接近基线的同样本近似 / 近邻 / 仅作证据分层下，本文闭环相对已有生成、工具反馈和轨迹修复的边际在哪里？ | 至少一个同样本近似基线、基线预算表、样本纳入 / 排除规则 | 降级为诊断协议或基线感知定位研究 |
| RQ5 编排条件 | 同一方法底座在自建 agent-loop 与成熟 coding-agent skill route 下的质量、成本、失败模式有何差异？ | E1/E2 同样本或可比样本的运行摘要、调用成本、失败模式 | 写成实现条件分析，不作为贡献 |

## 4. 章节大纲草案

### 1 Introduction

- 开场问题：控制系统状态机只有在可检查、可执行、可追溯时，才可能支撑后续诊断、仿真和修复。
- 承认现状：近期 LLM 工作已经覆盖自然语言到 FSM / UML / SysML / Umple / TTool / 协议状态机的生成。
- 缺口转向：问题不是“LLM 能不能生成状态机”，而是“哪些反馈信号能进入生成、诊断、仿真、修复闭环，并在公平基线协议下被评估”。
- 贡献候选必须先通过证据门禁：可执行表示底座、确定性诊断、场景级仿真反馈、结构化修复决策和基线感知评估都只能按证据强度写作。
- 禁止写法：`first NL-to-STM`、`first feedback loop`、`new DSL`、`prior work only draws diagrams`、`we show improvement`。

### 2 Background and Task Definition

- 定义输入：自然语言控制系统需求及必要上下文。
- 定义输出：机器可检查、可执行的状态机表示；说明它是检查、仿真和反馈底座，不是论文主打的新建模语言。
- 定义组件：状态、事件、迁移、守卫、动作 / 效应、变量、层次结构，以及与需求相关的场景行为。
- 定义反馈：诊断反馈、仿真反馈和修复决策反馈；明确它们不等同于完整模型检查、定理证明或工业认证。
- 定义评价：组件级人工裁决、确定性有效性、场景通过 / 失败、修复收敛与样本纳入 / 排除规则。

### 3 Related Work and Baseline Positioning

#### 3.1 先处理四个强相关工作

相关工作第一节必须先列出四个强相关工作，而不是先泛泛讲 LLM 或形式化方法。

| 强相关工作 | 已覆盖能力 | 本文边际差异 | 不能写的弱化新颖性 |
|---|---|---|---|
| Structure/Event SMF | 非结构化 reactive-system 自然语言描述 → UML state machine；支持 states / transitions / guards / actions / hierarchy 等组件级 F1；工件可访问 | 本文不争 NL → UML SM 生成，而聚焦控制系统需求下的可执行目标表示、确定性诊断、场景仿真和结构化修复决策 | 不能写“自由文本到状态机无人做过” |
| LLMs for EMP | NL → PlantUML / SysML behavior models；STM / ACT / SD 数据；PlantUML / SysML rule-based checking feedback 与 regeneration | 本文需把规则反馈与可执行场景轨迹反馈区分；若实验支持，只主张诊断、仿真与修复决策的组合协议 | 不能写“首次 tool feedback / feedback regeneration” |
| TTool-AI | ChatGPT 集成 TTool / MBSE；NL → SysML blocks / state machines；JSON / constraint / TTool syntax feedback loop；工件 / ODS 可复核 | 本文边际不是工具集成，而是控制需求专用可执行闭环、场景级仿真反馈、结构化修复决策与基线感知评估 | 不能把 TTool 的工具背景 model checker / simulator 误写成 prior work 未使用任何反馈 |
| Designing FSMs | 合成 NL → CSV DFSM / Mealy；oracle、distinguishing trace、checking sequence 与 fault-model repair | 本文不能声称 trace / repair 首创；差异限定为真实或准真实控制需求、guard / action / 变量等更丰富语义、场景候选生成、确定性仿真执行和结构化修复决策 | 不能写“首次 trace repair / oracle repair” |

#### 3.2 可执行建模近邻工作

- Umple / NL-to-code state machine：作为结构化提示、RAG、few-shot prompt 基线或近邻工作，不把 RAG / few-shot 写成本文 novelty。
- Automotive statechart generation：领域相近，但数据、微调过程和专家 GT 私有；用于仅作证据或领域动机，不写成可直接击败的直接基线。
- Pushing the Generative Envelope / MBSE artifacts：用于说明提示技巧与 SysML v2 工件趋势，不作为严格 STM 基线。

#### 3.3 协议 FSM、长规格与边界工作

- FlowFSM、SpecGPT 等长文档 / 协议 FSM 工作说明 prompt chaining、CoT、ensemble、JSON 校验和 expert GT 已覆盖相邻能力；由于领域、输出语义、GT 和工件边界，不强行纳入直接基线。
- TLA+、PAT、Event-B、Petri net、BPMN、LTL / STL、property generation 等快速扩张邻域进入边界讨论，不能混称精确 STM 直接基线。
- 经典需求到形式模型 / 受控自然语言工作作为严谨性背景，不能因“无 LLM”而贬低为不相关。

#### 3.4 Related Work 收束句

本节最后收束到：已有工作分别覆盖状态机族生成、SysML / MBSE 工具反馈、规则反馈再生成和 oracle / 轨迹修复；本文的可评估空间是这些能力在控制系统状态机任务中，以可执行表示、确定性诊断、场景级仿真反馈和结构化修复决策组合成受控闭环时的边际效果。

### 4 Method

- 概览：自然语言需求 → 初始状态机草稿 → 确定性诊断 → 场景候选生成 → 确定性仿真 → 结构化修复决策 → 回归检查。
- 目标表示：机器可检查、可执行的状态机表示；`pyfcstm` 只放在实现 / 复现材料说明中。
- 确定性诊断：解析、schema、语义、设计 / 检查诊断；输出诊断编号、消息、位置和受影响组件。
- 场景反馈：LLM 生成需求相关场景候选；确定性仿真器执行并产出通过 / 失败、轨迹和行为证据；人工 oracle 只裁决场景相关性与组件正确性。
- 结构化修复决策：修复请求、接受 / 拒绝、差异、修复记录、回滚和回归检查策略。

### 5 Experimental Protocol

- 样本登记：样本来源、冻结时间、纳入 / 排除标准，以及 压力测试 与主基准的区分。
- 基线分层：同样本近似、近邻、仅作证据、边界工作；至少一个最接近工作进入同样本近似，优先 Structure/Event SMF 或 LLMs for EMP STM 子集。
- 消融设计：B0 直接提示、B1 结构化提示、B2 无反馈编排、B3 仅诊断、B4 诊断 + 场景仿真、B5 完整反馈 + 结构化修复；EXT 单独报告最接近工作的近似基线，E1/E2 只作编排条件或附录分析。
- 人工协议：组件级评分规则、至少两名标注人、盲审 / 独立标注、一致性度量、仲裁和分歧记录。
- 预算协议：统一模型、提示上下文、反馈轮数、人工预算、工具预算和样本纳入 / 排除规则。

### 6 Results

- RQ1：报告诊断覆盖率、无效到有效的转化、组件缺陷分布。
- RQ2：报告仿真反馈发现的行为级失败、场景通过 / 失败结果和轨迹级案例。
- RQ3：报告修复收敛、回归、振荡、接受 / 拒绝理由和修复记录完整性。
- RQ4：报告最接近基线比较；不同层级 baseline 不放入同一“胜负排名”表。
- RQ5：报告 E1/E2 编排条件的质量、成本、失败模式与可复现边界差异。

### 7 Failure Analysis and Case Study

- 展示成功、失败、振荡、过修和 oracle drift 各类代表样本。
- 对每个案例展示诊断 → 场景轨迹 → 修复决策 → 回归结果。
- 明确哪些问题由确定性工具发现，哪些只能由人工裁决发现。

### 8 Threats to Validity and Limitations

- 基线公平性：输入、输出、GT、工件、提示词、模型预算和人工预算不可完全对齐。
- 复现边界：缺代码、缺 prompt、私有 GT、供应商 / 模型漂移 是可比性 / 复现边界，不是 prior work weakness。
- Oracle 风险：场景候选与人工裁决都可能偏移；LLM-as-Judge 不能作为主 oracle。
- 形式化范围：本文是可执行反馈 / 仿真，不是完整验证、BMC / LTL、定理证明或认证。
- 泛化性：Path-2 深控制系统语义、时间自动机、BMC / LTL、工业认证留给后续工作。

### 9 Artifact and Conclusion

- 复现材料：代码、语法 / 模式、样本登记、提示词模板、必要脱敏输入 / 输出摘要、诊断摘要、场景轨迹、人工标注规则、结果表和脱敏报告。
- 结论只能回到已由实验支持的范围：哪些反馈源有效、哪些失败暴露边界、哪些基线比较可防守。
- 不写 最优性能、已解决、完整验证或工业认证。

## 5. Related Work / Baseline 写作红线

| 禁止 claim | 为什么禁止 | 安全替代表述 |
|---|---|---|
| 首个 NL / 文档到状态机生成方法 | 九篇直接基线已覆盖 FSM、UML SM、SysML behavior、Umple、TTool、protocol FSM | “we study executable feedback for LLM-based state-machine modeling” |
| 首个 tool feedback / 自动修复闭环 | LLMs for EMP、TTool-AI 已有 rule/tool feedback；Designing FSMs 已有 trace/oracle repair | “we combine deterministic diagnostics, scenario simulation, and structured repair decisions under a controlled protocol” |
| prior work only draws diagrams | 多篇已有 machine-readable / tool-backed outputs | “prior work differs in feedback type, execution semantics, evaluation protocol, and comparability boundary” |
| `fcstm` / `pyfcstm` 是新 DSL 贡献 | S0a 术语策略要求弱化工程名 | “an internal implementation substrate for executable checking and simulation” |
| 私有 GT / missing code 是 prior weakness | 这是复现边界，不是方法缺陷 | “strict replication is blocked by private assets / missing prompt / output mismatch; we therefore classify it as evidence-only or near” |

## 6. 投稿与 S0b 边界

S0a 不冻结最终投稿期刊，也不宣布达到 CCF-A 标准。`venue_readiness_gate.md` 只能作为后续 S0b / Direction + Venue Freeze 的输入。当前 outline 的验收标准是：Related Work 分层、RQ、Method 和 Experiment 已经不会把论文带回“首创状态机生成”或“新 DSL 贡献”的旧主线。

## 7. 当前 foundation 允许说什么

当前允许说：

- 已把第一篇论文主线收缩为 diagnostics / simulation feedback / structured repair decision 的受控闭环研究。
- 已识别四个 mandatory closest works 对 claim 的 carve-out。
- 已规划 Related Work 第一层与 baseline 分层，避免把不可比较工作硬当直接基线。

当前不能说：

- 方法已经优于 baseline。
- 样本、oracle、baseline runner 或消融已经冻结。
- 可执行反馈已经被证明提升质量或修复稳定性。
- 本文提出了新的 paper-level DSL 或完成了完整形式化验证。
