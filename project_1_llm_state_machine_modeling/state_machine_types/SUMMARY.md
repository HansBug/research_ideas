# Project 1 State Machine Types Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_types/` 的总账，用于记录当前已经正式入账的状态机类型论文、综述类论文、统一分类口径、关键词簇和更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 若任务涉及普通条目，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 若任务涉及综述条目，再读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
5. 最后使用本文件查看统计、双表总账、关键词簇和待补方向。

## 当前收录统计

- 已收录普通类型论文：**49** 篇
- 已收录综述类论文：**10** 篇
- 本轮新增论文：**5** 篇
- 已完成 `desc.md`：**49** 篇
- 已完成 `survey.md`：**10** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮工作：新增 5 篇机器人任务控制 / 行为载体条目，覆盖 `MissionLab/CDL`、`XABSL`、`SMACHA/SMACH`、`RoboChart`、`YASMIN`

## 形式主义主类口径

右侧数量统计当前正式入账条目中涉及该主类的次数：普通论文按 `主类` 计数，综述论文按 `覆盖主类` 中出现的每个 emoji 分别计数。

| Emoji | 主类 | 范围 | 数量 |
|---|---|---|---:|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statechart`、`UML State Machine`、`SCXML`、`Tree Automata`、`Multi-Tape Automata`、`Two-Dimensional Automata`、`Cellular Automata`、`Weighted Automata` 等 | 17 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Statecharts`、`TIOA` 等 | 4 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 | 3 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、高层网等 | 5 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 | 5 |
| 📦 | 标准、交换格式与执行载体 | `SCXML`、`PNML`、`UML/XMI`、专用 DSL、元模型、交换标准等 | 29 |

## 描述客体口径

右侧数量统计当前普通论文总表中的 `客体` 条目总数。

| Emoji | 描述客体 | 含义 | 数量 |
|---|---|---|---:|
| 📝 | 序列 / 语言对象 | 主要描述字符串、事件序列、trace、多串关系等离散序列对象 | 3 |
| 🌳 | 树 / 文档对象 | 主要描述树结构、XML 文档、层次内容或其他树形对象 | 1 |
| 🖼️ | 网格 / 图案对象 | 主要描述二维 tape、图片、网格或格点对象 | 2 |
| 🎛️ | 控制 / 反应式逻辑 | 主要描述控制器、反应式行为、事件驱动控制逻辑 | 28 |
| 🤝 | 接口 / 交互契约 | 主要描述协议、组件交互、会话、接口或契约对象 | 8 |
| 🏭 | 并发过程 / 资源流 | 主要描述并发过程、工作流、token/资源流网络 | 4 |
| 🌡️ | 物理 / 混成对象 | 主要描述物理装置、连续动力学对象或混成/CPS 对象 | 3 |

## 所属领域口径

右侧数量统计当前普通论文总表中的 `领域` 条目总数。

| Emoji | 所属领域 | 含义 | 数量 |
|---|---|---|---:|
| 🧮 | 形式语言与自动机理论 | 主要是 automata theory、formal language、语义与判定性研究 | 5 |
| 💻 | 软件建模与程序行为 | 主要面向软件状态、程序行为、反应式软件或模型驱动开发 | 7 |
| 📄 | 文档与数据交换 | 主要面向 XML、schema、文档结构与数据交换 | 0 |
| ⏱️ | 实时与嵌入式系统 | 主要面向实时、调度、时序约束和嵌入式执行 | 7 |
| 🏭 | 工业控制与自动化 | 主要面向控制工程、自动化系统和工业逻辑 | 7 |
| 🌐 | 协议 / 分布式 / 交互系统 | 主要面向通信协议、服务交互、接口组合与分布式行为 | 6 |
| 🌡️ | CPS / 物理系统建模 | 主要面向连续物理过程、CPS、混成系统与物理仿真 | 17 |

## 状态口径

右侧数量统计当前普通论文总表与综述论文总表中的状态条目总数。

| Emoji | 含义 | 数量 |
|---|---|---:|
| 🟢 | 直接可用 | 58 |
| 🟡 | 可整理 | 1 |
| ⚪ | 未收获 | 0 |
| ⏳ | 尚未提取 | 0 |

## 综述对象类型口径

右侧数量统计当前综述论文总表中的对象类型条目总数。

| Emoji | 对象类型 | 含义 | 数量 |
|---|---|---|---:|
| 🧱 | 模型本体 | 主要综述形式主义本身、语义、变体与边界 | 7 |
| 🛠️ | 方法路线 | 主要综述围绕形式主义的验证、综合、转换、形式化方法 | 2 |
| 🏗️ | 标准/基础设施 | 主要综述标准、交换格式、元模型、API、工具互操作 | 1 |
| 🧪 | 应用/案例 | 主要综述领域应用、案例与工业采用 | 0 |

## 当前收录重心

- 后续普通条目优先补**模型本体**与**标准/基础设施**，即定义、语义、构造方式、交换格式、元模型、工具链与标准材料。
- 方法路线类论文或综述只作为辅助证据使用，前提是它们能说明某一形式主义“能做什么、如何落地、依赖什么基础设施”。
- 应用/案例导向条目原则上不作为本 collection 的正式扩库方向，除非它同时补出了稳定的模型本体或基础设施证据。
- 对 `SyncCharts / Argos / STATEMATE / SFC / Stateflow / StateGraph / Grafchart / RSML-SpecTRM / CHARON / Polychrony / RSML-e / JGrafchart + DPWS/FMI / PLEXIL / MissionLab / XABSL / XRobots / SMACHA / RAFCON / RoboChart / YASMIN / SCR / SEAD` 这类专用模型或执行载体，若能稳定回填“对象、语义、承载方式、工具入口”，可正式入账。

## 检索关键词簇

### 当前推荐关键词簇

- `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
- `tree automata / top-down tree automata / hedge automata / XML schema automata`
- `multi-tape automata / two-dimensional automata / cellular automata / weighted automata`
- `timed automata / timed statecharts / timed transition systems / timed I-O automata`
- `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata`
- `petri net / colored petri net / timed petri net / PNML / hierarchical petri net`
- `interface automata / I-O automata / contract automata / reactive modules`
- `communicating finite-state machine / workflow net / reactive modules / synccharts / argos / statemate / stateflow / sequential function chart / stategraph / grafchart / spectrm-rl / rsml / rsml-e / charon / polychrony / dpws / fmi / plexil / missionlab / cdl / xabsl / xrobots / smach / smacha / rafcon / robochart / yasmin / merlin2 / scr / platoon manoeuvre / manoeuvre design language`
- `survey / review / tutorial / taxonomy / mapping study` + 上述形式主义关键词

### 已观察到的高命中特征

- `survey/review/tutorial` 与具体家族词绑定时命中率高，例如 `timed automata survey`、`formalizing UML state machines survey`
- 对理论 automata 家族，`family term + survey` 往往能直接命中作者预印本或机构开放仓储，适合先补 `🧱` 再回溯原始文献
- `standardisation / markup language / PNML / formalizing / tool support` 这类“形式主义 + 基础设施”词簇很适合挖标准化与工具生态论文
- `recommendation / specification / formal / xmi / schema` 与形式主义名组合时，适合命中 `UML/SCXML` 这类标准与载体文献
- `cyber-physical systems` 与 `hybrid automata` 联合检索时，更容易命中“建模与验证框架综述”而非单一算法论文
- 精确形式主义名与框架名组合时命中率高，例如 `workflow net`、`synccharts esterel`、`stateflow semantics`、`stategraph modelica`、`argos statecharts`、`statemate semantics`、`grafchart process control`
- 对需求/规程导向载体，`process control / requirements language / procedural operator support` 与精确语言名组合时命中率高，如 `spectrm-rl`、`rsml`、`grafchart`
- 精确语言名再叠加基础设施关键词命中率也很高，例如 `charon hybrid systems`、`polychrony mode automata`、`rsml-e nusmv`、`grafchart dpws`、`jgrafchart fmi`
- 对执行载体 / 领域 DSL，精确名称直接定点检索效果很好，例如 `plexil nasa tm`、`missionlab cdl`、`xabsl behavior engineering`、`rafcon task programming`、`robochart robotic applications`、`yasmin ros 2`
- 对车队协同行为，`platoon manoeuvre state machine` 太宽，绑定 `SEAD / MDL / leader perspective / gap close` 后命中显著提升

### 已观察到的低命中特征

- 只搜 `state machine survey` 容易漂移到工作流、AI agent、软件工程流程或分类器论文
- 只搜 `verification` 容易命中算法优化或应用案例，而不是形式主义本体综述
- 只搜 `UML tool` 容易落到商业建模工具宣传页，形式语义与验证基础不足
- 只搜 `workflow state machine` 或 `modelica control` 容易漂到厂商教程、业务流程平台或一般应用案例
- 只搜 `reactive state machine` 容易漂到泛软件工程或教学材料，而不是具体载体论文
- 只搜 `process control state machine` 容易漂到一般控制案例、PLC 教程或工艺说明，而不是语言/载体论文
- 只搜 `service-oriented automation` 或 `co-simulation state machine` 容易漂到中间件综述和一般 `FMI` 框架，而不是具体状态机载体
- 只搜 `robot / ros 2 state machine` 或 `platoon state machine` 容易漂到课程项目、GitHub 库说明或单案例博客，难命中可入账论文

### 检索倾向调整

- 继续以“家族词 + survey/review/tutorial”作为第一轮入口，再由 survey 反推出原始文献、标准和工具线
- 对离散 automata 理论支线，优先补“模型谱系 + 经典判定边界 + 构造载体”三类材料，不把纯形式语言技巧论文直接当扩库主线
- 后续普通条目优先补“定义/语义 + 标准/交换格式 + 工具链”三类材料，不把应用论文或纯方法论文当扩库主线
- 对 `Petri Nets` 一类基础设施成熟方向，优先补 `standard / markup language / metamodel / API` 线，而不是只补理论定义
- `SCXML`、`Interface/Contract Automata` 已补基础条目，下一轮应继续补执行器/工具线与更早代表文献
- 方法路线条目只在能够反向支撑某一形式主义的能力边界或基础设施条件时再跟进
- 对应用/专用模型，优先用“精确形式主义名 + 框架名 + pdf/tech report/proceedings”检索，避免被泛领域关键词带偏
- `SyncCharts / SFC / Stateflow / StateGraph / STATEMATE / Grafchart / SpecTRM-RL / CHARON / RSML-e / Polychrony / PLEXIL / MissionLab / XABSL / XRobots / SMACHA / RAFCON / RoboChart / YASMIN / SCR / SEAD` 这类工程载体更适合直接搜准确名称，而不适合先走宽泛的 `state machine` 关键词
- `Reactive Modules / Argos` 这类语义与组合框架更适合用精确标题或作者名定点命中，否则容易与泛“module / reactive”关键词发生漂移
- 对 `DPWS / FMI / NuSMV / GME / Polychrony / CLARAty / JSON MDL / manoeuvre catalogue` 这类基础设施词，必须和精确形式主义名绑定检索，否则很容易被泛工具论文淹没

## 状态机类型论文总表

说明：

1. `主类`、`客体`、`领域` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. `主类` 的中文释义见上方“形式主义主类口径”，`客体` 的中文释义见上方“描述客体口径”，`领域` 的中文释义见上方“所属领域口径”，`状态` 的中文释义见上方“状态口径”。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 主类 | 客体 | 领域 | 形式主义 | 论文角色 | 标题 | 年份 | 核心功能 | 关键特性 | 构造方式 | 基础设施 | 适用场景 | 需求前提 | 状态 | 目录 |
|---|---|---|---|---|---|---|---:|---|---|---|---|---|---|---|---|
| 1 | 🧩 | 📝 | 🧮 | `Finite Automata` | 奠基定义 | Finite Automata and Their Decision Problems | 1959 | 识别有限符号串与串关系 | 有限状态、正则语言、判定性 | 状态集/字母表/迁移/接受条件 | 理论算法成熟，原文无工程标准 | 词法识别、有限记忆协议模式 | 纯离散、有限记忆、无时间数据 | 🟢 | [desc.md](./finite-automata-and-their-decision-problems/desc.md) |
| 2 | 🧩 | 📝 | 🧮 | `Multi-Tape Automata` | 理论分析 | Closedness Properties and Decision Problems for Finite Multi-Tape Automata | 1976 | 建模多串关系与 `n` 元语言关系 | 多带、端标记敏感、闭包与判定问题 | `n` 带输入 + 有限控制 + 接受集合 | 纯理论模型，无标准格式 | relation language、多路 trace 关系、同步/异步读取基线 | 输入是有限个离散串/trace，且不需数据/时间 | 🟢 | [desc.md](./closedness-properties-and-decision-problems-for-finite-multi-tape-automata/desc.md) |
| 3 | 🧩 | 🖼️ | 🧮 | `Two-Dimensional Automata` | 能力边界 | On the Capability of Finite Automata in 2 and 3 Dimensional Space | 1978 | 研究有限自动机在二维/三维网格中的搜索能力 | 网格移动、pebbles、二维可搜/三维受限 | 网格单元 + 方向动作 + pebble 标记 + 有限控制 | 理论模型，无工程标准 | picture language、maze search、空间模式基线 | 需求必须显式落在网格邻域与局部观测上 | 🟢 | [desc.md](./on-the-capability-of-finite-automata-in-2-and-3-dimensional-space/desc.md) |
| 4 | 🧩 | 🖼️ | 🌡️ | `Cellular Automata` | 模型综述 | Cellular Automata | 1983 | 用局部规则刻画格点系统演化 | lattice、同步更新、邻域、四类行为 | 格点 + 邻域 + 规则表/规则号 | 仿真生态强，但无统一交换标准 | 局部相互作用系统、扩散/生长、并行计算 | 系统由大量同构单元组成且规则局部同质 | 🟢 | [desc.md](./cellular-automata/desc.md) |
| 5 | 🔌 | 🤝 | 🌐 | `Communicating Finite-State Machines` | 模型提出 | On Communicating Finite-State Machines | 1983 | 用局部 `FSM` 与 FIFO 通道联合建模异步协议 | 局部状态机、异步消息、全局状态、boundedness 边界 | 进程状态机 + FIFO 通道 + send/receive 后继关系 | 协议分析路线明确，无标准格式 | 通信协议、分布式组件交互 | 需求需显式消息方向、参与方边界与通道语义 | 🟢 | [desc.md](./on-communicating-finite-state-machines/desc.md) |
| 6 | 🧩 | 🎛️ | 💻 | `Statecharts` | 奠基定义 | Statecharts: A Visual Formalism for Complex Systems | 1987 | 表达复杂反应式系统行为 | 层次、并发、广播事件 | 图形化超状态/并发区/跨层迁移 | 图形工具思路明确，后续生态强 | 复杂反应式控制系统 | 需求存在模式层次与并发子行为 | 🟢 | [desc.md](./statecharts-a-visual-formalism-for-complex-systems/desc.md) |
| 7 | 🔌 | 🤝 | 🌐 | `I/O Automata` | 模型教程 | An Introduction to Input/Output Automata | 1989 | 建模可组合组件交互 | input-enabled、composition、trace semantics | 动作签名 + 状态 + 迁移 | 理论框架成熟，无标准文件 | 分布式协议、组件交互 | 需显式划分输入/输出边界 | 🟢 | [desc.md](./an-introduction-to-input-output-automata/desc.md) |
| 8 | 🕸️ | 🏭 | 💻 | `Petri Nets` | 教程综述 | Petri Nets: Properties, Analysis and Applications | 1989 | 建模并发过程与资源流 | token、marking、活性/有界性 | places/transitions/arcs/marking | 分析方法成熟，标准交换后续补 | 工作流、并发资源共享 | 核心在并发同步与资源流 | 🟢 | [desc.md](./petri-nets-properties-analysis-and-applications/desc.md) |
| 9 | 🧩 | 🎛️ | 🌐 | `Extended Finite State Machine` | 方法佐证 | Method of analysing extended finite-state machine specifications | 1990 | 在 `FSM` 中加入变量、参数和多输出动作 | 状态变量、守卫/动作、队列通信、`Estelle/SDL` | 图形/文本 FDT + `when/from/to/output` + 状态变量 | `Estelle`/`SDL` 生态明确，无统一 JSON/XML | 协议规格、数据驱动控制逻辑、带参数交互 | 需求需显式状态、数据变量和输入输出动作 | 🟢 | [desc.md](./method-of-analysing-extended-finite-state-machine-specifications/desc.md) |
| 10 | ⏱️ | 🎛️ | ⏱️ | `Timed Automata` | 奠基定义 | A Theory of Timed Automata | 1994 | 表达显式时钟约束实时行为 | 时钟、守卫、复位、不变式 | 位置 + 时钟 + 迁移约束 | region/emptiness 理论成熟，无标准文件 | 实时协议、限时响应系统 | 需求含显式时间边界 | 🟢 | [desc.md](./a-theory-of-timed-automata/desc.md) |
| 11 | 🌊 | 🌡️ | 🌡️ | `Hybrid Automata` | 理论总结 | The Theory of Hybrid Automata | 1996 | 统一离散模式与连续流 | init/inv/flow/jump 条件 | 控制图 + 连续变量 + 流/跳转条件 | 理论语义强，工具依赖后续子类 | CPS、物理控制系统 | 需求含连续变量与模式切换 | 🟢 | [desc.md](./the-theory-of-hybrid-automata/desc.md) |
| 12 | 📦 | 🎛️ | ⏱️ | `SyncCharts` | 图形语言 | SyncCharts: A Visual Representation of Reactive Behaviors | 1996 | 用同步图形状态机表达抢占型 reactive behavior | strong/weak abortion、local signals、macrostate hierarchy、`Esterel` translation | star/constellation/macrostate + trigger/effect arcs | 可翻译到 `Esterel`，开放标准弱 | 实时 reactive/control-oriented systems | 需求强调抢占、同步广播和层次并行 | 🟢 | [desc.md](./synccharts-a-visual-representation-of-reactive-behaviors/desc.md) |
| 13 | 📦 | 🎛️ | 💻 | `STATEMATE Statecharts` | 工具语义 | The STATEMATE Semantics of Statecharts | 1996 | 固定 `STATEMATE` 中层次状态图的可执行 step semantics | configuration、compound transition、static reaction、superstep、racing detection | 层次状态图 + CT/SR + step algorithm | `STATEMATE` simulation/test/codegen 生态明确 | 复杂反应式软件与控制逻辑 | 需求需接受“本步变化、下步感知”的 step 语义 | 🟢 | [desc.md](./the-statemate-semantics-of-statecharts/desc.md) |
| 14 | 📦 | 🎛️ | 🌡️ | `MissionLab / CDL` | 任务规格与执行框架 | Multiagent Mission Specification and Execution | 1997 | 用 assemblage + `FSA` 统一多机器人任务规格与执行 | assemblage、temporal sequencing、`CDL`、retargetable binding | primitive library + coordination operator + `FSA` + `CDL` | `CfgEdit` + simulator + `AuRA/UGV` code generator | 多机器人 janitor、scouting、search | 需求需可拆为 operating states、skills 和感知触发 | 🟢 | [desc.md](./multiagent-mission-specification-and-execution/desc.md) |
| 15 | 🕸️ | 🏭 | 💻 | `WorkFlow net (WF-net)` | 领域特化 | The Application of Petri Nets to Workflow Management | 1998 | 把单 case 工作流生命周期压成可分析流程网 | 单入口/单出口、soundness、dead task、routing patterns | places/transitions/marking + workflow routing blocks | Petri 网分析工具线强，workflow analyzer 明确 | 审批流、业务流程、任务路由 | 需求核心是流程路由正确性与终止性 | 🟢 | [desc.md](./application-of-petri-nets-to-workflow-management/desc.md) |
| 16 | 📦 | 🎛️ | 🏭 | `SCR` | 需求规格方法 / 验证工具链 | Using Abstraction and Model Checking to Detect Safety Violations in Requirements Specifications | 1998 | 把安全关键需求规格压成可模拟、可模型检查的表格状态机 | monitored/controlled、condition/event tables、assertions、abstraction | tabular notation + assertion dictionary + conditional assignments | SCR toolset + DGB + simulator + `Spin` | 安全关键控制软件需求分析 | 需求能整理成同步输入事件与表格依赖 | 🟢 | [desc.md](./using-abstraction-and-model-checking-to-detect-safety-violations-in-requirements-specifications/desc.md) |
| 17 | 🔌 | 🤝 | 🌐 | `Reactive Modules` | 组合建模框架 | Reactive Modules | 1999 | 统一同步/异步组件并支持 trace 精化与时间抽象 | atoms、round/subround、hide/next/trigger、assume-guarantee | 变量分区 + guarded commands + 模块操作子 | 验证中间表示成熟，工具线偏研究型 | 协议、硬软协同系统、抽象验证 | 需求需显式变量边界与 round 语义 | 🟢 | [desc.md](./reactive-modules/desc.md) |
| 18 | 📦 | 🎛️ | 🏭 | `RSML / SpecTRM-RL` | 需求规格语言 | Designing Specification Languages for Process Control Systems: Lessons Learned and Steps to the Future | 1999 | 把控制需求约束成黑盒、模式驱动的状态机规格 | modes、and/or tables、black-box control model、macro/function | 图形模式图 + 输出/状态/转移表 | `SpecTRM` 工具链明确，开放标准弱 | 安全关键过程控制与需求审查 | 需求需先抽成 operating modes、interface 与 process models | 🟢 | [desc.md](./designing-specification-languages-for-process-control-systems/desc.md) |
| 19 | 📦 | 🎛️ | ⏱️ | `Argos` | 同步语言 | Argos: an Automaton-Based Synchronous Language | 2001 | 用布尔 Mealy 机构造可组合的同步状态机语言 | local signals、encapsulation、refinement、causality checking | 图形 automata + 局部信号封装 + hierarchy | 同步编译与验证连接明确，无开放标准 | 实时反应式控制与同步控制器 | 需求以离散信号/广播协同为主且接受同步假设 | 🟢 | [desc.md](./argos-an-automaton-based-synchronous-language/desc.md) |
| 20 | 🔌 | 🤝 | 🌐 | `Interface Automata` | 模型提出 | Interface Automata | 2001 | 检查接口兼容与替换性 | compatibility、illegal states、alternating simulation | 输入/输出接口自动机 | 组合与精化语义成熟，无标准格式 | 组件接口匹配、服务组合 | 关注假设/保证式交互 | 🟢 | [desc.md](./interface-automata/desc.md) |
| 21 | 📦 | 🎛️ | 🏭 | `Grafchart / JGrafchart` | 图形语言 / 工具载体 | GRAFCHART FOR PROCEDURAL OPERATOR SUPPORT TASKS | 2002 | 用步骤、过程和异常转移支撑工业操作规程与程序处理 | procedure step、exception transition、high-level tokens、animation | Grafchart charts + `G2` rules + `JGrafchart` runtime | Grafchart/JGrafchart 工具明确 | 批处理、operator support、程序规程 | 需求需显式步骤流、过程复用与异常中止 | 🟢 | [desc.md](./grafchart-for-procedural-operator-support-tasks/desc.md) |
| 22 | 🌊 | 🌡️ | 🌡️ | `CHARON` | 应用框架 / 软件架构 | A Framework and Architecture for Multi-Robot Coordination | 2002 | 用 agent+mode 统一多机器人控制、感知与协同 | 层次 agent、mode switching、连续流、共享信息 | `CHARON` 文本 DSL + `diff/alge/inv` + channels | `CHARON` + 多线程对象架构 + robot platform | 多机器人协调、编队、协同感知 | 需求需同时给出离散模式、连续控制和通信结构 | 🟢 | [desc.md](./framework-and-architecture-for-multi-robot-coordination/desc.md) |
| 23 | 📦 | 🎛️ | ⏱️ | `RSML-e / NuSMV` | 验证工具链 / 翻译框架 | Model Checking RSML-e Requirements | 2002 | 把需求状态机自动翻译到可模型检查符号模型 | 层次状态变量、接口、表格逻辑、自动抽象 | `RSML-e` 规格 + translator + `NuSMV` modules | `Nimbus` + `NuSMV` + `PVS` | 飞控与高保证需求验证 | 需求可整理为有限状态、接口和表格条件 | 🟢 | [desc.md](./model-checking-rsmle-requirements/desc.md) |
| 24 | 📦 | 🎛️ | 🏭 | `Sequential Function Charts (SFC)` | 工业语义 | A Unifying Semantics for Sequential Function Charts | 2004 | 为 `IEC 61131-3 SFC` 提供统一可参数化 cycle semantics | steps、action qualifiers、parallelism、history、timed extension | steps/transitions + action blocks + priority orders | `PLC` 工具链和 `IEC` 标准明确 | `PLC` 顺控、工业自动化 | 需求可分解为步骤/守卫/动作并按扫描周期执行 | 🟢 | [desc.md](./a-unifying-semantics-for-sequential-function-charts/desc.md) |
| 25 | 📦 | 🎛️ | 🏭 | `StateGraph` | 工具/库 | StateGraph - A Modelica Library for Hierarchical State Machines | 2005 | 在 Modelica 中提供层次状态机库 | `fire/newActive` 方程、parallel/alternative、composite step | steps/transitions/parallel/composite + Modelica equations | `Modelica.StateGraph` + logical blocks | 监督控制、物理过程联调 | 需求需与 Modelica 模型协同并接受单赋值约束 | 🟢 | [desc.md](./stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md) |
| 26 | ⏱️ | 🤝 | ⏱️ | `Timed I/O Automata` | 理论专著 | The Theory of Timed I/O Automata | 2005 | 组合实时组件并比较实现关系 | trajectories、receptiveness、simulation | 动作接口 + 时间轨迹 | 理论框架成熟，无标准格式 | 实时组件系统 | 需求同时包含接口与时间演化 | 🟢 | [desc.md](./the-theory-of-timed-input-output-automata/desc.md) |
| 27 | 🕸️ | 🏭 | 💻 | `Coloured Petri Nets` | 教程讲义 | Coloured Petri Nets | 2005 | 在 Petri 网中引入 typed token 与数据 | colour sets、simulation、state space | 网结构 + 颜色集 + 弧表达式 | 工具生态成熟，交换标准较弱 | 协议与数据驱动并发系统 | 并发 + 显式数据对象 | 🟢 | [desc.md](./coloured-petri-nets/desc.md) |
| 28 | 📦 | 🎛️ | ⏱️ | `Polychronous Mode Automata` | 多时钟建模构件 | Polychronous Mode Automata | 2006 | 把多时钟数据流与 mode automata 统一到同一建模前端 | 弱/强抢占、多时钟、元模型扩展、Signal 编译 | `GME` metamodel + `Signal` equations + automata | `Polychrony` + `Signal-Meta` + `GME` | 航电与分布式嵌入式系统 | 需求同时含局部时钟、控制模式和数据流 | 🟢 | [desc.md](./polychronous-mode-automata/desc.md) |
| 29 | 📦 | 🎛️ | 🌡️ | `PLEXIL` | 计划执行语言 / 执行载体 | Plan Execution Interchange Language (PLEXIL) | 2006 | 把 planner 输出统一落成可执行任务节点树 | node conditions、XML、lookup/command、deterministic execution | `NodeList/Command/Assignment` 树 + domain description + XML | universal executive + `CLARAty` + plan editor | 航天器 / 火星车自主任务执行 | 需求需显式命令接口、世界状态查询与时序条件 | 🟢 | [desc.md](./plan-execution-interchange-language-plexil/desc.md) |
| 30 | 📦 | 🎛️ | 🌡️ | `XABSL` | 机器人行为语言 / 执行引擎 | XABSL - A Pragmatic Approach to Behavior Engineering | 2006 | 用 option hierarchy 组织复杂自主体行为 | option graph、activation path、symbols、basic behaviors、debugging | `XABSL` DSL + decision trees + XML/intermediate code | Ruby compiler + `XabslEngine` + monitor/profiler | RoboCup 与动态机器人行为控制 | 需求需可抽成层次技能、符号接口和 basic behaviors | 🟢 | [desc.md](./xabsl-a-pragmatic-approach-to-behavior-engineering/desc.md) |
| 31 | 📦 | 🎛️ | 🌡️ | `Stateflow` | 形式语义 | An Operational Semantics for Stateflow | 2007 | 把工业 `Stateflow` chart 形式化为顺序化图形状态机语义 | junction、local events、`12 o'clock` ordering、安全子集 | states/junctions/transitions + linearized SOS | `Matlab/Simulink/Stateflow` 生态成熟 | 嵌入式控制器、混成系统离散部分 | 需求最终落到 `Stateflow` 工具链且接受工具优先级 | 🟢 | [desc.md](./an-operational-semantics-for-stateflow/desc.md) |
| 32 | 🕸️ | 🏭 | ⏱️ | `Time Petri Nets` | 教程讲义 | Time Petri Nets Part II: State Class based methods | 2008 | 在并发网上加入时间区间 | 静态区间、state class graph | P/T 网 + 变迁时间区间 | TINA 线成熟，标准格式较弱 | 实时并发流程与调度 | 并发资源流 + 时间窗口 | 🟢 | [desc.md](./time-petri-nets/desc.md) |
| 33 | 🧩 | 🌳 | 🧮 | `Tree Automata` | 教程专著 | Tree Automata Techniques and Applications | 2008 | 识别树、项与层次结构语言 | bottom-up、top-down、determinization、decision problems | ranked alphabet + 状态 + 树重写规则 | 理论与算法成熟，XML/hedge 在线路上衔接强 | AST、term rewriting、schema-like structural validation | 输入需显式树/项结构而非平坦事件串 | 🟢 | [desc.md](./tree-automata-techniques-and-applications/desc.md) |
| 34 | 📦 | 🎛️ | 🏭 | `ModeGraph` | 工具/库 | ModeGraph - A Modelica Library for Embedded Control Based on Mode-Automata | 2008 | 在 Modelica 中实现安全层次状态机与 mode-automata 执行 | single-assignment、delayed transition、preemption、parallel | `Step/Transition/Composite/Parallel` + mode equations | Modelica 工具链明确，需语言扩展，无独立交换标准 | 嵌入式控制、混合控制、工业逻辑 | 需求需安全模式切换并与 Modelica 模型协同 | 🟢 | [desc.md](./modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md) |
| 35 | 🧩 | 📝 | 🧮 | `Weighted Automata` | 手册章节 | Weighted Automata Algorithms | 2009 | 在自动机/转导器上附加 semiring 权值 | semiring、path weight、determinization、minimization | 图结构 + label + weight + semiring 运算 | 算法体系成熟，但无统一交换标准 | 概率/代价/评分型字符串与转导建模 | 需求需保留有限状态骨架且每条路径带可组合权值 | 🟢 | [desc.md](./weighted-automata-algorithms/desc.md) |
| 36 | 📦 | 🎛️ | 🌡️ | `Ptolemy II FSM / Modal Models` | 工具教程 | Finite State Machines and Modal Models in Ptolemy II | 2009 | 用状态机控制 refinement 切换并支撑异构执行 | guard/output/set action、mode refinement、microstep、local time | `FSMActor / ModalModel` + `MoML` + compatible directors | Ptolemy II 图形/Java/MoML 生态完整 | 异构嵌入式系统、CPS mode switching | 不同模式需挂不同 refinement 与执行域 | 🟢 | [desc.md](./finite-state-machines-and-modal-models-in-ptolemy-ii/desc.md) |
| 37 | 📦 | 🎛️ | 🌡️ | `Modelica_StateGraph2` | 形式主义 / 工具库 | A New Formalism for Modeling of Reactive and Hybrid Systems | 2009 | 把 Modelica 状态机扩成安全层次并行 generalized steps | generalized steps、suspend/resume、delay、`NuSMV` verification | `\Gamma = \langle V_c,G,T,g_I \rangle` + ports + interpretation algorithm | `Modelica_StateGraph2` + `NuSMV` | reactive/hybrid systems | 需求含模式切换并需与物理模型联仿 | 🟢 | [desc.md](./a-new-formalism-for-modeling-of-reactive-and-hybrid-systems/desc.md) |
| 38 | 📦 | 🎛️ | 🌡️ | `XRobots` | 领域特化 DSL | An Overview of XRobots: A Hierarchical State Machine-Based Language | 2011 | 用可参数化 behavior 组织移动机器人行为 | HSM、first-class behavior、by-value/by-reference、entry/exit | `Behavior` DSL + parameterized transitions | prototype compiler 路线，原文无公开工具 | 移动机器人行为编程 | 需求可拆为可复用行为并接受高阶参数化 | 🟢 | [desc.md](./an-overview-of-xrobots-a-hierarchical-state-machine-based-language/desc.md) |
| 39 | 📦 | 🎛️ | 🌡️ | `Modelica State Machines` | 语言扩展 | State Machines in Modelica | 2012 | 把状态机纳入 Modelica 语言核心 | 13 方程语义、immediate/delayed、reset/synchronize | Modelica blocks + transition equations + clock | Modelica 3.3 语言级支持明确 | 物理系统中的控制逻辑、嵌入式控制 | 状态逻辑需与同 clock 的 Modelica 模型原生集成 | 🟢 | [desc.md](./state-machines-in-modelica/desc.md) |
| 40 | 📦 | 🤝 | 🏭 | `Grafchart / JGrafchart + DPWS` | 工具扩展 / 服务编排载体 | Graphical Programming Language Support for Service Oriented Architecture in Automation | 2012 | 把可发现服务设备嵌入图形状态机协调逻辑 | `DPWS Object`、自动重绑、通知事件、方法式调用 | `JGrafchart` 图形模型 + `DPWS/WSDL` 绑定 | `JGrafchart` + `DPWS` discovery + `WSDL` | 服务化车间集成与设备协调 | 设备需以 `DPWS` 服务暴露并允许事件订阅 | 🟢 | [desc.md](./graphical-programming-language-support-for-service-oriented-architecture-in-automation/desc.md) |
| 41 | 📦 | 🌡️ | 🌡️ | `Grafchart / JGrafchart + FMI` | 工具扩展 / 协同仿真载体 | On Extending JGrafchart with Support for FMI for Co-Simulation | 2014 | 把图形顺控应用接入 `FMI` 协同仿真 | communication step、wrapper/FMU 导出、scan-cycle 对齐 | `JGrafchart` + `FMU`/XML + wrapper/export | `JGrafchart` + `FMI` + `CustomIO/SocketIO` | 控制器与物理模型联合验证 | 控制逻辑需为离散 scan-cycle，plant 可作为 `FMU` | 🟢 | [desc.md](./on-extending-jgrafchart-with-support-for-fmi-for-co-simulation/desc.md) |
| 42 | 🔌 | 🤝 | 🌐 | `Contract Automata` | 模型提出 | Automata for Analysing Service Contracts | 2014 | 分析多方契约匹配与责任 | agreement、weak agreement、liability | 向量动作自动机 + 组合 | 分析方法明确，生态偏研究型 | 服务编排、契约组合 | 多方 request/offer 关系清晰 | 🟢 | [desc.md](./contract-automata/desc.md) |
| 43 | 🧩 | 🎛️ | 💻 | `SCXML` | 标准规范 | State Chart XML (SCXML): State Machine Notation for Control Abstraction | 2015 | 提供可执行层次状态机 XML 载体 | `state/parallel/history/datamodel/invoke` | SCXML XML 文档 | W3C 规范、Schema、测试套件 | 事件驱动流程与互操作 | 需要标准文本载体 | 🟢 | [desc.md](./scxml-state-machine-notation-for-control-abstraction/desc.md) |
| 44 | 📦 | 🎛️ | 🌡️ | `SMACHA / SMACH` | 状态机装配 / 代码生成 | Rapid state machine assembly for modular robot control using meta-scripting, templating and code generation | 2017 | 用 `YAML` 和模板快速生成可执行 `SMACH` 状态机 | meta-scripting、templating、sub-scripts、container recursion | `YAML` scripts + `Jinja2` templates + generated Python `SMACH` | `SMACHA` API + `SMACH` + ROS/Gazebo/Baxter | `ROS` 任务控制、pick-place、stacking | 需求已接受 `SMACH` 运行时且存在高复用结构 | 🟢 | [desc.md](./rapid-state-machine-assembly-for-modular-robot-control/desc.md) |
| 45 | 📦 | 🎛️ | 🌡️ | `RAFCON` | 图形任务编程 / mission control 载体 | RAFCON: A Graphical Tool for Task Programming and Mission Control | 2017 | 用图形层次状态机协调复杂机器人任务 | hierarchy、concurrency、library state、data flow、remote monitoring | 图形状态机 + Python execute + ports/data flow | GTK+ GUI + execution engine + API | 复杂机器人任务编排与监控 | 需求需能拆成层次技能并依赖中间件执行 | 🟢 | [desc.md](./rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md) |
| 46 | 🧩 | 🎛️ | 💻 | `UML State Machine` | 标准规范 | OMG Unified Modeling Language (OMG UML), Version 2.5.1 | 2017 | 标准化行为/协议状态机元模型 | regions、pseudostates、XMI | 图形建模 + metamodel + XMI | OMG 标准和工具生态成熟 | MDE、跨工具交换 | 需要与 UML 语境集成 | 🟢 | [desc.md](./uml-251-specification/desc.md) |
| 47 | 📦 | 🎛️ | 🌡️ | `RoboChart` | 机器人 DSL / 形式验证工具链 | RoboChart: modelling and verification of the functional behaviour of robotic applications | 2019 | 用受限 `UML` 状态机建模并自动生成验证语义 | metamodel、well-formedness、timed primitives、`CSP` semantics | module/controller/machine + graphical/textual editors | `RoboTool` + `CSP-M/tock-CSP` + `FDR` + Eclipse | 高可信机器人控制器建模与验证 | 需求需显式平台接口、状态逻辑和时间约束 | 🟢 | [desc.md](./robochart-modelling-and-verification-of-robotic-applications/desc.md) |
| 48 | 📦 | 🤝 | 🌡️ | `SEAD / MDL` | 领域特化框架 / 机动描述语言 | A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions | 2021 | 把 platoon manoeuvre 统一成 leader-perspective 分层状态机与 JSON 描述 | idle states、action primitives、PME/RSM、SIM wrapper、MDL | idle states + sub-manoeuvres + `JSON MDL` | manoeuvre catalogue + MDL parser + simulation | 车队 join/split/lane-change/gap-close 协同行为 | 需求需存在 leader-follower 角色与 V2V 协同协议 | 🟢 | [desc.md](./hierarchical-state-machine-based-framework-for-platoon-manoeuvre-descriptions/desc.md) |
| 49 | 📦 | 🎛️ | 🌡️ | `YASMIN` | `ROS 2` 状态机库 / 运行时载体 | YASMIN: Yet Another State MachINe library for ROS 2 | 2022 | 为 `ROS 2` 提供轻量 `FSM/HFSM` 行为层库 | blackboard、nested state machines、Python/C++、viewer | library API + shared blackboard + web viewer | GitHub repo + `ROS 2` integration + web viewer | 服务机器人行为控制与执行层编排 | 需求基于 `ROS 2` 且可用 `FSM/HFSM` 表达 | 🟢 | [desc.md](./yasmin-yet-another-state-machine/desc.md) |

## 综述类论文总表

说明：

1. `对象类型` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. survey 正式入账后，应继续把其引出的代表原始文献回填到下一节的追踪表。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 综述主题 | 对象类型 | 标题 | 年份 | 覆盖主类 | 覆盖的形式主义 | 是否覆盖构造方式/基础设施 | 主要价值 | 状态 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 二维自动机理论版图 | 🧱 | A Survey of Two-Dimensional Automata Theory | 1991 | 🧩 | `2D Turing Machines`、`2D Finite Automata`、`Marker Automata`、cellular types | 部分覆盖 | 把二维 tape 上的方向限制、alternation、封闭性与判定问题统一进一个谱系 | 🟢 | [survey.md](./survey-of-two-dimensional-automata-theory/survey.md) |
| 2 | 状态图模型检验路线 | 🛠️ | Model Checking of Statechart Models: Survey and Research Directions | 2004 | 🧩 | `Statecharts`、`STATEMATE`、`RSML`、`UML State Machine`、`HRM/CRSM` | 部分覆盖 | 讲清层次状态机验证中的 flattening、语义歧义与 traceability 问题 | 🟡 | [survey.md](./model-checking-of-statechart-models/survey.md) |
| 3 | 细胞自动机理论版图 | 🧱 | Theory of Cellular Automata: A Survey | 2005 | 🧩 | 同步 `CA`、reversible `CA`、number-conserving/linear `CA`、空间受限识别 `CA` | 部分覆盖 | 把可逆性、守恒量、动力学与语言识别四条理论主线压到一篇里 | 🟢 | [survey.md](./theory-of-cellular-automata-survey/survey.md) |
| 4 | Petri 网标准化与交换格式 | 🏗️ | PN Standardisation: A Survey | 2006 | 🕸️ 📦 | `P/T Nets`、`High-level Petri Nets`、`Symmetric Nets`、`PNML` | 是 | 直接覆盖标准、元模型、XML 承载与 API 实现 | 🟢 | [survey.md](./pn-standardisation-survey/survey.md) |
| 5 | 确定性自顶向下树自动机谱系 | 🧱 | Deterministic Top-Down Tree Automata: Past, Present, and Future | 2008 | 🧩 📦 | blind/sensing、ranked/unranked、`DTD`、`XML Schema`、`Relax NG` | 是 | 讲清 deterministic top-down tree automata 在 ranked/unranked/XML schema 三条线上的 expressive power 与静态分析边界 | 🟢 | [survey.md](./deterministic-top-down-tree-automata/survey.md) |
| 6 | 多带自动机表达力与判定性 | 🧱 | A Survey of Multi-Tape Automata | 2012 | 🧩 | synchronous/asynchronous、one-way/two-way、rewind-bounded、reversal-bounded 多带自动机 | 部分覆盖 | 把多带 automata 的同步、回退、反转与确定性差异压成统一闭包与可判定性版图 | 🟢 | [survey.md](./survey-of-multi-tape-automata/survey.md) |
| 7 | 时间自动机变体与工具生态 | 🧱 | A Survey of Timed Automata for the Development of Real-Time Systems | 2013 | ⏱️ | 经典、参数化、概率、代价、博弈等 `Timed Automata` 变体 | 是 | `80` 个变体、`40` 个工具、实现问题一体化盘点 | 🟢 | [survey.md](./survey-of-timed-automata-for-real-time-systems/survey.md) |
| 8 | 混成自动机与 CPS 验证 | 🧱 | Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems | 2013 | 🌊 ⏱️ | 一般 `Hybrid Automata`、`Timed Automata`、`Initialized Rectangular`、`PCD` | 部分覆盖 | 讲清连续动力学引入后的判定边界与工具谱系 | 🟢 | [survey.md](./hybrid-automata-for-cps/survey.md) |
| 9 | 加权逻辑与加权自动机统一视角 | 🧱 | A Unifying Survey on Weighted Logics and Weighted Automata | 2018 | 🧩 | `Weighted Automata`、core weighted logic、words/ranked/unranked trees | 部分覆盖 | 把权值域、承载结构和抽象/具体语义三条轴统一起来，适合补 quantitative automata 本体 | 🟢 | [survey.md](./weighted-logics-and-weighted-automata-survey/survey.md) |
| 10 | UML 状态机形式化与自动验证 | 🛠️ | Formalizing UML State Machines for Automated Verification -- A Survey | 2023 | 🧩 📦 | `UML State Machine`、translation targets、direct operational semantics | 是 | `61` 篇工作双路线盘点，并审计工具长期可用性 | 🟢 | [survey.md](./formalizing-uml-state-machines-survey/survey.md) |

## 由综述引出的待跟进原始文献

说明：

1. 本表用于把 survey/review 条目转成下一轮可执行的补库入口。
2. `优先级` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
3. 本表属于文献跟进表，默认包含 `年份`，并按 `年份升序` 排列。
4. 若某条原始文献已经正式入库为普通条目、标准条目或其他正式总账条目，应立即从本表移除，不再重复挂在“待跟进”状态。

| # | 年份 | 来源综述 | 形式主义 / 方向 | 应追踪的原始文献或标准 | 推荐原因 | 后续动作 | 优先级 |
|---|---:|---|---|---|---|---|---|
| 1 | 1961 | 加权逻辑与加权自动机统一视角 | `Weighted Automata` | Schützenberger, `On the Definition of a Family of Automata` | 加权自动机与形式幂级数主线的原始起点 | 优先补单篇 `desc.md` | 🔴 |
| 2 | 1965 | 多带自动机表达力与判定性 | relation / multi-tape 基线 | Elgot, Mezei, `On Relations Defined by Generalized Finite Automata` | 连接多带自动机、关系语言与 rational relations 的早期基石 | 优先补单篇 `desc.md` | 🔴 |
| 3 | 1967 | 二维自动机理论版图 | `2D Automata` 起点 | Blum, Hewitt, `Automata on a Two-Dimensional Tape` | 二维 tape 自动机研究的共同起点 | 优先补单篇 `desc.md` | 🔴 |
| 4 | 1968 | 确定性自顶向下树自动机谱系 | 树自动机基线 | Thatcher, Wright, `Generalized Finite Automata Theory with an Application to a Decision Problem of Second-Order Logic` | regular tree language 与 tree automata 主线的早期理论入口 | 优先补单篇 `desc.md` | 🔴 |
| 5 | 1968 | 多带自动机表达力与判定性 | one-way multi-tape | Fischer, Rosenberg, `Multitape One-Way Nonwriting Automata` | 连接 one-way 多带机与 relation 识别能力的早期主线 | 优先补单篇 `desc.md` | 🟠 |
| 6 | 1969 | 细胞自动机理论版图 | 符号动力系统口径 | Hedlund, `Endomorphisms and Automorphisms of Shift Dynamical Systems` | 把 `CA` 放进 shift dynamics 语义框架，是后续可逆性/动力学主线的基准 | 优先补单篇 `desc.md` | 🔴 |
| 7 | 1972 | 细胞自动机理论版图 | injective / surjective 判定 | Amoroso, Patt, `Decision Procedures for Surjectivity and Injectivity of Parallel Maps for Tessellation Structures` | 一维 `CA` 可判定性主线的经典入口 | 优先补单篇 `desc.md` | 🔴 |
| 8 | 1991 | 细胞自动机理论版图 | 加性守恒量 | Hattori, Takesue, `Additive Conserved Quantities in Discrete-Time Lattice Dynamical Systems` | 守恒量与 number-conserving `CA` 主线的关键入口 | 优先补单篇 `desc.md` | 🟠 |
| 9 | 1991 | Petri 网标准化与交换格式 | `Time Petri Nets` | Berthomieu, Diaz, `Modeling and Verification of Time Dependent Systems Using Time Petri Nets` | 连接 `Petri Net` 与时间扩展，是后续 Part 3 重要背景 | 优先补单篇 `desc.md` | 🟠 |
| 10 | 1993 | 混成自动机与 CPS 验证 | 一般 `Hybrid Automata` | Alur et al., `Hybrid Automata: An Algorithmic Approach to the Specification and Verification of Hybrid Systems` | 混成自动机奠基文献 | 优先补单篇 `desc.md` | 🔴 |
| 11 | 1997 | UML 状态机形式化与自动验证 | `UML` 标准起点 | `OMG UML 1.1 specification` | 形式化工作共同的时间边界和标准起点 | 先补标准条目 | 🟡 |
| 12 | 1998 | 混成自动机与 CPS 验证 | 判定边界 | Henzinger et al., `What's Decidable About Hybrid Automata?` | 混成自动机可判定子类和边界线的关键入口 | 优先补单篇 `desc.md` | 🔴 |
| 13 | 1999 | UML 状态机形式化与自动验证 | UML + model checking | Lilius, Paltor, `Formalising UML State Machines for Model Checking` | UML 形式化主线的重要早期节点 | 优先补单篇 `desc.md` | 🔴 |
| 14 | 1999 | 确定性自顶向下树自动机谱系 | `Hedge Automata` / XML | Murata, `Hedge Automata: A Formal Model for XML Schemata` | 连接 unranked tree automata 与 XML schema 生态的关键节点 | 优先补单篇 `desc.md` | 🔴 |
| 15 | 2000 | 状态图模型检验路线 | 保层次验证 | Alur et al., `Efficient Reachability Analysis of Hierarchic Reactive Machines` | 代表避免完全 flatten 的关键技术路线 | 先找原文并评估是否入库为 `desc.md` | 🟡 |
| 16 | 2004 | Petri 网标准化与交换格式 | `Petri Net` 标准 Part 1 | `ISO/IEC 15909-1` | 标准化术语、语义和图形记法的核心入口 | 优先补标准条目 | 🔴 |
| 17 | 2005 | Petri 网标准化与交换格式 | `PNML` / Part 2 概念线 | Ekkart Kindler, `The Petri Net Markup Language and ISO/IEC 15909-2` | 补足 `PNML` 的核心概念、状态和未来方向 | 优先补单篇 `desc.md` | 🔴 |
| 18 | 2006 | Petri 网标准化与交换格式 | High-level Petri Nets | Jensen, Rozenberg (eds.), `High-Level Petri Nets` | 回补高层网本体与标准化对象之间的理论连接 | 优先补单篇 `desc.md` | 🟠 |
| 19 | 2007 | 加权逻辑与加权自动机统一视角 | automata-logic 等价 | Droste, Gastin, `Weighted Automata and Weighted Logics` | 词上加权自动机与逻辑等价的标准入口 | 优先补单篇 `desc.md` | 🔴 |
| 20 | 2009 | 时间自动机变体与工具生态 | 参数化时间自动机 | Etienne Andre, `IMITATOR` tool line | 连接参数综合与需求到模型自动化 | 先补工具/方法条目 | 🟠 |
| 21 | 2011 | 时间自动机变体与工具生态 | 主流工具线 | Behrmann et al., `A Tutorial on UPPAAL` | 当前最值得优先追踪的时间自动机工具主线 | 优先补工具条目 | 🔴 |
| 22 | 2012 | 加权逻辑与加权自动机统一视角 | valuation monoid 语义 | Droste, Meinecke, `Weighted Automata and Regular Expressions over Valuation Monoids` | 把平均值、折扣和等非半环语义纳入统一权值模型 | 优先补单篇 `desc.md` | 🟠 |
| 23 | 2013 | UML 状态机形式化与自动验证 | 直接操作语义 | Liu et al., `USMMC` / corresponding semantics paper | 代表较完整的 UML 直接语义与验证路线 | 优先补单篇 `desc.md` | 🟠 |
| 24 | 2021 | UML 状态机形式化与自动验证 | 现代工具线 | Jouault et al., `AnimUML` | 代表仍在维护、可实际试用的现代 UML 验证工具 | 先补工具条目 | 🟠 |

## 待优先补入方向

1. `Harel Statecharts -> STATEMATE semantics -> HRM/CRSM / UML profile` 这一条层次状态机语义细化线。
2. `Timed Automata + UPPAAL + IMITATOR` 这一条时间自动机基础与工具线。
3. `I/O Automata + TIOA + Interface/Contract Automata` 这一条接口组合与精化线。
4. `Hybrid Automata + 1993 origin paper + decidable subclasses` 这一条连续动力学主线。
5. `Petri Nets + ISO/IEC 15909 + PNML + High-Level/Timed extensions` 这一条网模型标准与扩展线。
6. `SCXML + processors/runtime/tool support` 这一条可执行载体与运行时线。
7. `Tree Automata` 已补基础条目，下一轮继续沿 `Hedge Automata + XML schema validation` 回补结构化承载线。
8. `Weighted Automata` 已补 handbook 级本体条目，下一轮继续回补 `Schutzenberger + weighted logics + valuation monoid` 主线。
9. `Two-Dimensional / Cellular / Multi-Tape Automata` 已补基础代表条目，下一步回补更早奠基论文与典型判定边界。
10. `EFSM` 已补方法支撑型条目，下一轮应继续补更纯粹的定义/标准源，如 `SDL / Estelle / 测试主线`。
11. 上述每条主线都优先补“模型本体 + 标准/基础设施”条目；方法路线只作为辅证，不单独扩成主收录方向。
12. `CHARON / Polychrony / RSML-e / JGrafchart` 已补应用与工具桥接条目，下一轮可沿 `CHARON` 本体、`Signal/Polychrony` 工具线、`RSML-e` 工业案例、`JGrafchart` 导出/runtime 继续扩展。
13. `PLEXIL / MissionLab / XABSL / XRobots / SMACHA / RAFCON / YASMIN / RoboChart / SEAD / SCR` 已补执行载体与机器人任务 DSL 条目，下一轮可沿 `CLARAty / PLEXIL runtime`、`MissionLab CfgEdit / CDL`、`XABSL runtime/engine`、`SMACH / FlexBE / SMACC`、`RoboTool / RoboCalc`、`YASMIN / MERLIN2`、`SEAD` manoeuvre library、`SCR` 规格编辑与验证工具链继续扩展。

## 更新日志

| 时间 | 动作 | 说明 |
|---|---|---|
| 2026-04-01 11:58:00 | 建立 `state_machine_types/` 文库骨架 | 新增 [README.md](./README.md)、[GUIDE.md](./GUIDE.md)、[SUMMARY.md](./SUMMARY.md)、[DESC_GUIDE.md](./DESC_GUIDE.md)、[SURVEY_GUIDE.md](./SURVEY_GUIDE.md)，并固定普通论文/综述论文双表口径 |
| 2026-04-01 13:03:21 | 首次收录综述类论文 | 新增 5 篇 `survey.md` 条目并回填综述总表与 follow-up 原始文献表，覆盖 `Statecharts/UML`、`Timed Automata`、`Hybrid Automata`、`Petri Net standardisation/PNML` |
| 2026-04-01 13:45:03 | 补充图例数量统计口径 | 为“形式主义主类”“状态”“综述对象类型”三张图例表增加右侧数量列，并要求后续随正式总表同步更新 |
| 2026-04-01 14:43:56 | 新增离散 automata 模型本体综述 | 补入 `Two-Dimensional`、`Cellular`、`Deterministic Top-Down Tree`、`Multi-Tape`、`Weighted Automata` 五篇 `🧱` survey，并同步回填统计、综述总表与 follow-up 文献表 |
| 2026-04-01 16:08:21 | 首批收录经典普通条目 | 新增 13 篇 `desc.md` 条目，覆盖 `FSM / Statecharts / UML / SCXML / Timed Automata / I-O 系 / Hybrid Automata / Petri 网系`，并同步回填普通论文总表、图例统计与 follow-up 清单 |
| 2026-04-01 16:28:28 | 补齐离散 automata 普通条目 | 新增 6 篇 `desc.md` 条目，覆盖 `EFSM / Tree / Multi-Tape / 2D / Cellular / Weighted`，并同步回填普通论文总表、图例统计与 follow-up 清单 |
| 2026-04-01 20:16:13 | 补入应用/专用状态机载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `CFSM / WF-net / ModeGraph / Ptolemy modal model / Modelica State Machines`，并同步回填统计、关键词簇、普通论文总表与后续扩展方向 |
| 2026-04-01 21:00:18 | 扩展同步/工业状态机载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `SyncCharts / SFC / Stateflow / StateGraph / StateGraph2`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-01 21:45:20 | 扩展同步语义与需求规格载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `STATEMATE / Reactive Modules / SpecTRM-RL / Argos / Grafchart`，并同步回填统计、关键词簇、普通论文总表、follow-up 清单与下一轮扩展方向 |
| 2026-04-01 22:43:43 | 扩展应用型与工具桥接条目 | 新增 5 篇 `desc.md` 条目，覆盖 `CHARON` 多机器人架构、`Polychronous Mode Automata`、`RSML-e -> NuSMV`、`JGrafchart + DPWS`、`JGrafchart + FMI`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-01 23:42:19 | 扩展应用/专用状态机载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `SCR` 需求规格+模型检查、`PLEXIL` 计划执行语言、`XRobots` 行为 DSL、`RAFCON` 图形任务编程、`SEAD` platoon `MDL`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 00:33:22 | 扩展机器人任务控制载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `MissionLab/CDL`、`XABSL`、`SMACHA/SMACH`、`RoboChart`、`YASMIN`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |

## 失败与阻塞记录

- 当前无正式失败记录。
