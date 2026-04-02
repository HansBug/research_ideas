# Project 1 State Machine Types Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_types/` 的总账，用于记录当前已经正式入账的状态机类型论文、综述类论文、统一分类口径、关键词簇和更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 若任务涉及普通条目，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 若任务涉及综述条目，再读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
5. 最后使用本文件查看统计、双表总账、关键词簇和待补方向。

## 当前收录统计

- 已收录普通类型论文：**114** 篇
- 已收录综述类论文：**10** 篇
- 本轮新增论文：**5** 篇
- 已完成 `desc.md`：**114** 篇
- 已完成 `survey.md`：**10** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮工作：重新联网筛查 `15+` 个接口/组合、时间/混成与 `Petri` 并发候选后，新入库 5 篇普通条目，覆盖 `Context-Dependent Service Contracts`、`ROS Timed Automata`、`Hybrid Multi-Robot Coordination`、`Manufacturing-Cell Timed Petri Schedules` 与 `DiNeROS Distributed Petri Nets`，并同步回填 `paper.pdf`、`paper_content.txt`、`bibtex.bib`、`desc.md`、普通论文总表、关键词簇、演化树挂接说明与更新日志

## 形式主义主类口径

右侧数量统计当前正式入账条目中涉及该主类的次数：普通论文按 `主类` 计数，综述论文按 `覆盖主类` 中出现的每个 emoji 分别计数。

| Emoji | 主类 | 范围 | 数量 |
|---|---|---|---:|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statecharts`、`Tree Automata`、`Multi-Tape Automata`、`Two-Dimensional Automata`、`Cellular Automata`、`Weighted Automata` 等 | 15 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Statecharts`、`TIOA` 等 | 8 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 | 7 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、高层网等 | 11 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 | 11 |
| 🔣 | DSL / 专用建模语言 | `UML State Machine`、`SCXML`、`SyncCharts`、`SFC`、`Stateflow`、`PLEXIL`、`XABSL`、`RoboChart`、`Modelica State Machines`、`MDL`、`DSD` 等 | 30 |
| 📦 | 标准、交换格式、元模型与执行载体 | `PNML`、`UML/XMI`、`XML Schema`、`JGrafchart` 扩展、`RAFCON/FlexBE/YASMIN` 这类运行时/编辑器/执行载体等 | 47 |

## 描述客体口径

右侧数量统计当前普通论文总表中的 `客体` 条目总数。

| Emoji | 描述客体 | 含义 | 数量 |
|---|---|---|---:|
| 📝 | 序列 / 语言对象 | 主要描述字符串、事件序列、trace、多串关系等离散序列对象 | 3 |
| 🌳 | 树 / 文档对象 | 主要描述树结构、XML 文档、层次内容或其他树形对象 | 1 |
| 🖼️ | 网格 / 图案对象 | 主要描述二维 tape、图片、网格或格点对象 | 2 |
| 🎛️ | 控制 / 反应式逻辑 | 主要描述控制器、反应式行为、事件驱动控制逻辑 | 72 |
| 🤝 | 接口 / 交互契约 | 主要描述协议、组件交互、会话、接口或契约对象 | 20 |
| 🏭 | 并发过程 / 资源流 | 主要描述并发过程、工作流、token/资源流网络 | 23 |
| 🌡️ | 物理 / 混成对象 | 主要描述物理装置、连续动力学对象或混成/CPS 对象 | 55 |

## 所属领域口径

右侧数量统计当前普通论文总表中的 `领域` 条目总数。

| Emoji | 所属领域 | 含义 | 数量 |
|---|---|---|---:|
| 🧮 | 形式语言与自动机理论 | 主要是 automata theory、formal language、语义与判定性研究 | 5 |
| 💻 | 软件建模与程序行为 | 主要面向软件状态、程序行为、反应式软件或模型驱动开发 | 7 |
| 📄 | 文档与数据交换 | 主要面向 XML、schema、文档结构与数据交换 | 0 |
| ⏱️ | 实时与嵌入式系统 | 主要面向实时、调度、时序约束和嵌入式执行 | 10 |
| 🏭 | 工业控制与自动化 | 主要面向控制工程、自动化系统和工业逻辑 | 23 |
| 🌐 | 协议 / 分布式 / 交互系统 | 主要面向通信协议、服务交互、接口组合与分布式行为 | 14 |
| 🌡️ | CPS / 物理系统建模 | 主要面向连续物理过程、CPS、混成系统与物理仿真 | 55 |

## 状态口径

右侧数量统计当前普通论文总表与综述论文总表中的状态条目总数。

| Emoji | 含义 | 数量 |
|---|---|---:|
| 🟢 | 直接可用 | 123 |
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

- 后续普通条目优先补**模型本体**、**DSL / 语言本体**与**标准/基础设施**三层：先定义和语义，再看语言/grammar/profile，再看交换格式、运行时和工具链。
- 方法路线类论文或综述只作为辅助证据使用，前提是它们能说明某一形式主义“能做什么、如何落地、依赖什么基础设施”。
- 应用/案例导向条目原则上不作为本 collection 的正式扩库方向，除非它同时补出了稳定的模型本体或基础设施证据。
- `SUMMARY.md` 里的主蓝本演化树只挂“形式主义家族 / profile / DSL / 标准语言”节点；单一应用监督器、单纯运行库封装、单纯代码生成器和工具扩展不挂主树。
- 对 `SyncCharts / Argos / STATEMATE / SFC / Stateflow / StateGraph / Grafchart / RSML-SpecTRM / CHARON / Polychrony / RSML-e / JGrafchart + DPWS/FMI / PLEXIL / MissionLab / XABSL / FlexBE / VisualHFSM / RoboSim / XRobots / SMACHA / RAFCON / RoboChart / YASMIN / SCR / SEAD / ARGO / Cortex / LLFSM / DSD / Safety4.0 / AutoPlant-SMACH / MERLIN / rFSM / SMACC / package handling / binary decomposition / eye-hand FSM HRC / lane-change CBF FSM / electrical spacer statechart / autonomous driving hierarchical FSM / EFSMSG / pallet manipulation / industrial mobile manipulation / walking machines / HRC task allocation / educational robotics FSM / ROSCo / mission controller / meal assistance FSM / power-line inspection robot / autonomous forklift navigation / annieway chsm / lower limb exoskeleton fsm / underwater swarm pheromone / stair-climbing delivery robot / smhpfc / hobbit smach dmsl / hybrid fes exoskeleton / waiter robot smach / cotton harvesting rover fsm / floor tiling fsm / cardiac rehabilitation social robot finite state machine / robotic excavation statecharts / high-voltage transmission line maintenance robot finite state machine / semi-autonomous robotic surgery statecharts / exoskeleton locomotion mode recognition FSM-HSVM` 这类专用模型、DSL 或执行载体，若能稳定回填“对象、语义、承载方式、工具入口”，可正式入账；但只有主体真的是“族模型 / 语言本体”时才进入演化树。

## 状态机族演化树

说明：

1. 这是一棵“主蓝本树”，只保留每个节点最主要的一条来源边；若某条目明显受多个家族影响，只挂到最核心蓝本，并在对应 `desc.md` 中保留旁系说明。
2. 只有“主体是状态机族模型 / profile / DSL / 标准语言，且原文给出明确语法、语义、元模型或结构定义”的条目才能入树。
3. 单一应用监督器、单纯代码生成器、单纯运行库封装、单纯工具适配扩展，不进主树；它们仍可留在正式总表中，但只作为载体或应用证据。
4. 括号年份默认取当前文库所收代表条目的年份，不强行回填所有概念的最早提出年份。

```text
状态机族形式主义
├─ 有限状态 / 自动机主干
│  └─ Finite Automata (1959)
│     ├─ Multi-Tape Automata (1976)
│     ├─ Two-Dimensional Automata (1978)
│     ├─ Cellular Automata (1983)
│     ├─ Tree Automata (2008，文库代表条目)
│     ├─ Weighted Automata (2009，文库代表条目)
│     ├─ Communicating Finite-State Machines (1983)
│     ├─ Extended Finite State Machine (1990)
│     ├─ 层次状态机支线
│     │  └─ Statecharts (1987)
│     │     ├─ STATEMATE Statecharts (1996)
│     │     ├─ UML State Machine (2017 规范条目)
│     │     │  └─ RoboChart (2017 / 2019 / 2024)
│     │     │     └─ RoboSim (2019)
│     │     ├─ SCXML (2015)
│     │     ├─ Stateflow (2007)
│     │     ├─ rFSM Statecharts (2012)
│     │     └─ 同步反应式状态机支线
│     │        ├─ Argos (2001)
│     │        ├─ SyncCharts (1996)
│     │        └─ Polychronous Mode Automata (2006)
│     ├─ 需求规格 DSL 支线
│     │  ├─ SCR (1998)
│     │  └─ RSML / SpecTRM-RL (1999)
│     │     └─ RSML-e (2002)
│     ├─ 工业顺控 / Modelica DSL 支线
│     │  ├─ Sequential Function Charts, SFC (2004 语义条目；蓝本更早)
│     │  │  └─ Grafchart / JGrafchart (2002)
│     │  │     └─ StateGraph (2005)
│     │  │        ├─ ModeGraph (2008)
│     │  │        ├─ Modelica_StateGraph2 (2009)
│     │  │        └─ Modelica State Machines (2012)
│     │  └─ Ptolemy II FSM / Modal Models (2009)
│     └─ 任务 / 行为 DSL 支线
│        ├─ MissionLab / CDL (1997)
│        ├─ PLEXIL (2006)
│        ├─ XABSL (2006)
│        ├─ XRobots (2011)
│        ├─ SEAD / MDL (2021)
│        └─ DSD (2021)
├─ 接口 / 组合主干
│  └─ I/O Automata (1989)
│     ├─ Timed I/O Automata (2005)
│     ├─ Interface Automata (2001)
│     │  ├─ Transaction-Aware Web Service Interface (2006)
│     │  ├─ Interface Automata for Accessors / IoT Contracts (2015)
│     │  └─ Contract Automata (2014)
│     │     └─ Featured Modal Contract Automata (2020)
│     ├─ ConfiguredService with Context-dependent Contracts (2011)
│     └─ Reactive Modules (1999)
├─ 时间 / 连续主干
│  ├─ Timed Automata (1994)
│  └─ Hybrid Automata (1996)
│     ├─ CHARON (2002)
│     └─ Nested Hybrid Automata (2007，文库代表条目)
└─ Petri 网 / 并发网主干
   └─ Petri Nets (1989，文库代表条目)
      ├─ WorkFlow nets (1998)
      ├─ Coloured Petri Nets (2005)
      ├─ Time Petri Nets (2008)
      ├─ MOPN / GSPN for Multi-Robot Tasks (2008)
      └─ GSPNR / MRA for Persistent Multi-Robot Tasks (2020)
```

挂接说明：

1. `SCXML` 同时具有“标准 + 语言”双重属性；在主蓝本树里按“可执行状态机语言”挂到 `Statecharts` 支线，在主类计数中按 `🔣` 处理。
2. `RoboChart`、`RoboSim`、`SEAD / MDL`、`DSD` 等是领域化 DSL，只在原文给出明确语言骨架、语义约束或机读描述时入树；否则仍留在 `📦` 或应用条目中。
3. `Grafchart + DPWS/FMI`、`RAFCON`、`FlexBE`、`SMACHA/SMACH`、`YASMIN`、`VisualHFSM` 等当前更适合作为“执行载体 / 工具链”而不是主蓝本节点，暂不挂入主树。
4. 最近两次提交新增的 `Transaction-Aware Web Service Interface`、`IoT Interface Theory`、`FMCA`、`MOPN / GSPN for Multi-Robot Tasks` 与 `GSPNR / MRA for Persistent Multi-Robot Tasks`，都在原有主干下补出了可稳定命名的接口/契约或 `Petri` 扩展节点，因此已同步整合进主树。
5. 最近两次提交新增的 `CARE Runtime`、`Commercial Field Bus Timed Automata`、`Timed Multi-Robot Planning`、`Hybrid Action Coordination`、`Hybrid Field Robot Teams` 主要提供运行时、工具链或应用级挂接证据，而不是新的语言本体；因此保留在正式总表中，并作为 `Contract Automata`、`Timed Automata`、`Hybrid Automata` 主干的应用侧代表，不单独挂入主树。
6. 本轮新增的 `Urban Driving NHA` 虽然属于自动驾驶应用条目，但原文显式给出了标准 `HA` 九元组和层次化的 `$HA^k(q^{k-1})$` 嵌套结构，可稳定提炼为 `Nested Hybrid Automata` 子类，因此已在 `Hybrid Automata` 下补出 `Nested Hybrid Automata (2007，文库代表条目)`；其余 `CARE-Uppaal Runtime Verification`、`SCADA Timed Automata`、`Open-Path AGV CPN` 与 `Modular HRC Safety PN` 仍主要作为 `Contract Automata`、`Timed Automata`、`Coloured Petri Nets` / `Petri Nets` 主干的应用侧证，不单独挂入主树。
7. 本轮新增的 `ConfiguredService with Context-dependent Contracts` 原文给出了稳定的服务 tuple、契约分解、组合算子和 `UPPAAL` 转换链，因此作为“接口/组合主干上的服务契约分支”挂到 `I/O Automata` 下；同轮新增的 `ROS Timed Automata`、`Hybrid Multi-Robot Coordination`、`Manufacturing-Cell Timed Petri Schedules` 与 `DiNeROS Distributed Petri Nets` 继续作为 `Timed Automata`、`Hybrid Automata` 与 `Petri Nets` 主干的应用/工具链侧证，不单独挂入主树。

## 检索关键词簇

### 当前推荐关键词簇

- `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
- `tree automata / top-down tree automata / hedge automata / XML schema automata`
- `multi-tape automata / two-dimensional automata / cellular automata / weighted automata`
- `timed automata / timed statecharts / timed transition systems / timed I-O automata / field bus protocol / uppaal industrial protocol / multi-robot planning / scada attack detection / ros communication / kobuki / callback queue / spinOnce`
- `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata / heterogeneous field robot teams / supervisory control / action coordination mobile robots / autonomous urban driving / nested hybrid automata / multi-robot coordination / hytech`
- `petri net / colored petri net / timed petri net / PNML / hierarchical petri net / multi-robot tasks / persistent tasks gspnr / open-path agv / hrc safety control / manufacturing cells / distributed petri nets / dineros / tina`
- `interface automata / I-O automata / contract automata / reactive modules / service contracts / context-dependent services / configured service / frsec / runtime environment / orchestration / web services transactions / internet of things accessor / care uppaal`
- `communicating finite-state machine / workflow net / reactive modules / synccharts / argos / statemate / stateflow / sequential function chart / stategraph / grafchart / spectrm-rl / rsml / rsml-e / charon / polychrony / dpws / fmi / plexil / missionlab / cdl / xabsl / flexbe / visualhfsm / robosim / xrobots / smach / smacha / rafcon / robochart / yasmin / merlin / merlin2 / rfsm / smacc / scr / argo / cortex / llfsm / dynamic stack decider / safety4.0 / smach mission supervisor / autoplant / package handling / binary decomposition / companion robot / manoeuvre design language / human-robot collaborative assembly / eye-hand fsm / autonomous lane change cbf / electrical spacer / efsmsg / emergency uav swarms / autonomous driving hierarchical state machine / pallet manipulation hfsm / industrial mobile manipulation / walking machines llfsm / task allocation hfsm / educational robotics fsm / ros commander / rosco / universal mission controller / mission execution engine / meal assistance / active feeding / power transmission line inspection robot / autonomous forklift navigation / annieway chsm / lower limb exoskeleton fsm / cop gait fsm / underwater pheromone robot / stair-climbing delivery robot / smhpfc / hobbit smach dmsl / hybrid fes robot exoskeleton / waiter robots conveying drinks / cotton harvesting rover finite state machine / floor tiling finite-state machine / cardiac rehabilitation social robot finite state machine / robotic excavation statecharts / high-voltage transmission line maintenance robot finite state machine / semi-autonomous robotic surgery statecharts / exoskeleton locomotion mode recognition FSM-HSVM`
- `survey / review / tutorial / taxonomy / mapping study` + 上述形式主义关键词

### 已观察到的高命中特征

- `survey/review/tutorial` 与具体家族词绑定时命中率高，例如 `timed automata survey`、`formalizing UML state machines survey`；对理论 automata 家族，`family term + survey` 往往还能直接命中作者预印本或机构开放仓储
- `standardisation / markup language / PNML / formalizing / tool support` 与 `recommendation / specification / formal / xmi / schema` 这类“形式主义 + 基础设施”词簇，适合定点挖 `UML/SCXML/PNML` 的标准化与工具生态条目
- `cyber-physical systems + hybrid automata` 更容易命中框架综述；若目标是应用条目，继续绑定 `urban driving / multi-robot coordination / field robots / hytech` 更稳
- 精确形式主义名与框架名组合时命中率高，例如 `workflow net`、`synccharts esterel`、`stateflow semantics`、`stategraph modelica`、`argos statecharts`、`statemate semantics`、`grafchart process control`
- 对需求/规程导向载体，`process control / requirements language / procedural operator support` 与精确语言名组合时命中率高，如 `spectrm-rl`、`rsml`、`grafchart`
- 精确语言名叠加基础设施或工具词也很有效，例如 `charon hybrid systems`、`polychrony mode automata`、`rsml-e nusmv`、`grafchart dpws`、`jgrafchart fmi`；执行载体 / 领域 DSL 继续优先直接搜准确名称，如 `plexil nasa tm`、`missionlab cdl`、`rfsm statecharts`、`merlin rosplan smach`、`robochart robotic applications`
- 对接口/契约与服务组合，`context-dependent services / configured service / service contracts / frsec / uppaal` 的组合明显优于泛搜 `service composition verification`
- 对 ROS / 实时应用，`ros timed automata / kobuki / callback queue / spinOnce / uppaal` 这类“中间件对象 + 时序参数 + 工具名”组合命中稳定
- 对 Petri 并发应用，`manufacturing cells timed petri nets`、`distributed petri nets ros`、`dineros pnml tina` 这类“场景名 + 网模型 + 工具链”组合比泛搜 `robot petri net` 更有效
- 对具体问题型应用条目，精确问题名与状态机词组合命中较好，例如 `human-robot collaborative assembly finite state machine`、`autonomous lane change control barrier function fsm`、`electrical spacer installation statechart`、`uav swarm efsmsg`、`pallet manipulation hierarchical state machine`、`walking machines llfsm`、`industrial mobile manipulation smach`、`ros commander`、`universal mission controller uuv`、`active robot-assisted feeding fsm`、`power transmission line inspection robot fsm`、`autonomous forklift navigation fsm`、`annieway urban challenge state machine`、`lower limb exoskeleton fsm`、`underwater swarm pheromone fsm`、`stair-climbing delivery robot state machine`、`smhpfc waste sorting robot`、`hobbit smach dmsl`、`hybrid fes robot exoskeleton finite state machine`、`waiter robot smach velocity profile`、`cotton harvesting rover state machine`、`floor tiling finite-state machine`、`cardiac rehabilitation social robot finite state machine`、`robotic excavation statecharts`、`high-voltage transmission line maintenance robot finite state machine`、`semi-autonomous robotic surgery statecharts`、`exoskeleton locomotion mode recognition FSM-HSVM`、`web services transactions interface`、`iot accessor interface automata`、`multi-robot planning timed automata`、`scada timed automata`、`urban driving hybrid automata`、`hybrid control action coordination mobile robots`、`multi-robot coordination hytech`、`open-path agv petri net`、`human-robot safety petri net`、`persistent tasks gspnr`

### 已观察到的低命中特征

- 只搜 `state machine survey` 容易漂移到工作流、AI agent、软件工程流程或分类器论文
- 只搜 `verification` 容易命中算法优化或应用案例，而不是形式主义本体综述
- 只搜 `UML tool` 容易落到商业建模工具宣传页，形式语义与验证基础不足
- 只搜 `workflow state machine` 或 `modelica control` 容易漂到厂商教程、业务流程平台或一般应用案例
- 只搜 `reactive state machine` 容易漂到泛软件工程或教学材料，而不是具体载体论文
- 只搜 `process control state machine` 容易漂到一般控制案例、PLC 教程或工艺说明，而不是语言/载体论文
- 只搜 `service-oriented automation` 或 `co-simulation state machine` 容易漂到中间件综述和一般 `FMI` 框架，而不是具体状态机载体
- 只搜 `robot / ros 2 state machine`、`space robot autonomy`、`human robot collaboration safety fsm`、`humanoid framework`、`package handling robot`、`autonomous driving state machine`、`uav swarm state machine` 或 `generic finite state machine robot control` 容易漂到课程项目、软件仓库说明或泛系统论文，难命中可入账条目

### 检索倾向调整

- 继续以“家族词 + survey/review/tutorial”作为第一轮入口，再由 survey 反推出原始文献、标准和工具线
- 对离散 automata 理论支线，优先补“模型谱系 + 经典判定边界 + 构造载体”三类材料，不把纯形式语言技巧论文直接当扩库主线
- 后续普通条目优先补“定义/语义 + 标准/交换格式 + 工具链”三类材料，不把应用论文或纯方法论文当扩库主线
- 对 `Petri Nets` 一类基础设施成熟方向，优先补 `standard / markup language / metamodel / API` 线，而不是只补理论定义
- `SCXML`、`Interface/Contract Automata` 已补基础条目，且接口应用层已覆盖 `web transactions / IoT accessors / context-dependent services / CARE-Uppaal`，下一轮应继续补更纯的接口本体、早期代表文献与执行器/工具线
- 方法路线条目只在能够反向支撑某一形式主义的能力边界或基础设施条件时再跟进；应用/专用模型则优先用“精确形式主义名 + 框架名 + pdf/tech report/proceedings”检索，避免被泛领域关键词带偏
- `SyncCharts / SFC / Stateflow / StateGraph / STATEMATE / Grafchart / SpecTRM-RL / CHARON / RSML-e / Polychrony / PLEXIL / MissionLab / XABSL / FlexBE / VisualHFSM / RoboSim / XRobots / SMACHA / RAFCON / RoboChart / YASMIN / SCR / SEAD / ARGO / LLFSM / DSD / Safety4.0 / AutoPlant / MERLIN / rFSM / SMACC` 这类工程载体更适合直接搜准确名称，而不适合先走宽泛的 `state machine` 关键词
- `Reactive Modules / Argos` 这类语义与组合框架更适合用精确标题或作者名定点命中，否则容易与泛“module / reactive”关键词发生漂移
- 对 `DPWS / FMI / NuSMV / GME / Polychrony / CLARAty / JSON MDL / manoeuvre catalogue / whiteboard / smach mission supervisor / dynamic risk assessment` 这类基础设施词，必须和精确形式主义名绑定检索，否则很容易被泛工具论文淹没
- 对具体问题型应用模型，优先用“精确题目关键词 + pdf/proceedings/project page/preprint/repository”检索，例如 `ros commander / mission controller / active feeding / power transmission line inspection robot / autonomous forklift navigation / annieway / lower limb exoskeleton / underwater pheromone / stair-climbing delivery robot / smhpfc / hobbit / hybrid fes exoskeleton / waiter robot / cotton harvesting rover / floor tiling robot / cardiac rehabilitation social robot / robotic excavation / HVTL maintenance robot / surgical procedure observer / exoskeleton locomotion recognizer` 这类专名应直接定点，而不是只搜宽泛领域词
- 对接口/契约、时间/连续与 `Petri` 并发主干，继续直接搜“精确形式主义名 + 具体应用名 + pdf/proceedings/uppaal/aamas/iros/icra/icinco/formalise”这类定点组合，例如 `configured service uppaal`、`care uppaal`、`web services transactions interface`、`internet of things accessor interface automata`、`ros timed automata kobuki`、`scada timed automata`、`commercial field bus protocol uppaal`、`urban driving hybrid automata`、`multi-robot coordination hytech`、`multi-robot tasks petri nets`、`manufacturing cells timed petri nets`、`distributed petri nets ros`、`dineros pnml tina`

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
| 11 | 🕸️ | 🏭 | 🏭 | `Timed Petri Net Schedules for Manufacturing Cells` | 制造单元调度 / 定时 Petri 网应用建模 | Application of Timed Petri Nets to Modeling the Schedules of Manufacturing Cells | 1995 | 把 simple/composite schedules 压成 timed/colored Petri nets 并分析 cycle time | simple/composite schedules、invariant analysis、colored family representation | configuration sequence -> robot action sequence -> timed/colored `Petri Nets` | timed/colored `Petri Nets` + invariant analysis | flexible manufacturing cells、robotic cell scheduling、throughput 优化 | 动作序列和时间参数可结构化枚举 | 🟢 | [desc.md](./application-of-timed-petri-nets-to-modeling-the-schedules-of-manufacturing-cells/desc.md) |
| 12 | 🌊 | 🌡️ | 🌡️ | `Hybrid Automata` | 理论总结 | The Theory of Hybrid Automata | 1996 | 统一离散模式与连续流 | init/inv/flow/jump 条件 | 控制图 + 连续变量 + 流/跳转条件 | 理论语义强，工具依赖后续子类 | CPS、物理控制系统 | 需求含连续变量与模式切换 | 🟢 | [desc.md](./the-theory-of-hybrid-automata/desc.md) |
| 13 | 🔣 | 🎛️ | ⏱️ | `SyncCharts` | 图形语言 | SyncCharts: A Visual Representation of Reactive Behaviors | 1996 | 用同步图形状态机表达抢占型 reactive behavior | strong/weak abortion、local signals、macrostate hierarchy、`Esterel` translation | star/constellation/macrostate + trigger/effect arcs | 可翻译到 `Esterel`，开放标准弱 | 实时 reactive/control-oriented systems | 需求强调抢占、同步广播和层次并行 | 🟢 | [desc.md](./synccharts-a-visual-representation-of-reactive-behaviors/desc.md) |
| 14 | 🔣 | 🎛️ | 💻 | `STATEMATE Statecharts` | 工具语义 | The STATEMATE Semantics of Statecharts | 1996 | 固定 `STATEMATE` 中层次状态图的可执行 step semantics | configuration、compound transition、static reaction、superstep、racing detection | 层次状态图 + CT/SR + step algorithm | `STATEMATE` simulation/test/codegen 生态明确 | 复杂反应式软件与控制逻辑 | 需求需接受“本步变化、下步感知”的 step 语义 | 🟢 | [desc.md](./the-statemate-semantics-of-statecharts/desc.md) |
| 15 | 🔣 | 🎛️ | 🌡️ | `MissionLab / CDL` | 任务规格与执行框架 | Multiagent Mission Specification and Execution | 1997 | 用 assemblage + `FSA` 统一多机器人任务规格与执行 | assemblage、temporal sequencing、`CDL`、retargetable binding | primitive library + coordination operator + `FSA` + `CDL` | `CfgEdit` + simulator + `AuRA/UGV` code generator | 多机器人 janitor、scouting、search | 需求需可拆为 operating states、skills 和感知触发 | 🟢 | [desc.md](./multiagent-mission-specification-and-execution/desc.md) |
| 16 | 🕸️ | 🏭 | 💻 | `WorkFlow net (WF-net)` | 领域特化 | The Application of Petri Nets to Workflow Management | 1998 | 把单 case 工作流生命周期压成可分析流程网 | 单入口/单出口、soundness、dead task、routing patterns | places/transitions/marking + workflow routing blocks | Petri 网分析工具线强，workflow analyzer 明确 | 审批流、业务流程、任务路由 | 需求核心是流程路由正确性与终止性 | 🟢 | [desc.md](./application-of-petri-nets-to-workflow-management/desc.md) |
| 17 | 🔣 | 🎛️ | 🏭 | `SCR` | 需求规格方法 / 验证工具链 | Using Abstraction and Model Checking to Detect Safety Violations in Requirements Specifications | 1998 | 把安全关键需求规格压成可模拟、可模型检查的表格状态机 | monitored/controlled、condition/event tables、assertions、abstraction | tabular notation + assertion dictionary + conditional assignments | SCR toolset + DGB + simulator + `Spin` | 安全关键控制软件需求分析 | 需求能整理成同步输入事件与表格依赖 | 🟢 | [desc.md](./using-abstraction-and-model-checking-to-detect-safety-violations-in-requirements-specifications/desc.md) |
| 18 | 🔌 | 🤝 | 🌐 | `Reactive Modules` | 组合建模框架 | Reactive Modules | 1999 | 统一同步/异步组件并支持 trace 精化与时间抽象 | atoms、round/subround、hide/next/trigger、assume-guarantee | 变量分区 + guarded commands + 模块操作子 | 验证中间表示成熟，工具线偏研究型 | 协议、硬软协同系统、抽象验证 | 需求需显式变量边界与 round 语义 | 🟢 | [desc.md](./reactive-modules/desc.md) |
| 19 | 🔣 | 🎛️ | 🏭 | `RSML / SpecTRM-RL` | 需求规格语言 | Designing Specification Languages for Process Control Systems: Lessons Learned and Steps to the Future | 1999 | 把控制需求约束成黑盒、模式驱动的状态机规格 | modes、and/or tables、black-box control model、macro/function | 图形模式图 + 输出/状态/转移表 | `SpecTRM` 工具链明确，开放标准弱 | 安全关键过程控制与需求审查 | 需求需先抽成 operating modes、interface 与 process models | 🟢 | [desc.md](./designing-specification-languages-for-process-control-systems/desc.md) |
| 20 | 🌊 | 🌡️ | 🌡️ | `Linear Hybrid Automata for Multi-Robot Coordination` | 多机器人协同 / 线性混成自动机应用建模 | Formal Modeling and Analysis of Hybrid Systems: A Case Study in Multi-robot Coordination | 1999 | 把通信、障碍估计与路径选择统一成可做参数综合的混成模型 | continuous motion、communication sync、sensor uncertainty、`HyTech` reachability | robot/obstacle/coordination automata + linear inequalities + `HyTech` | `HyTech` + linear hybrid automata description | 多机器人协同导航、带通信的障碍规避与目标到达 | 连续动力学需可线性化，空间与感知模型需可保守近似 | 🟢 | [desc.md](./formal-modeling-and-analysis-of-hybrid-systems-a-case-study-in-multi-robot-coordination/desc.md) |
| 21 | 📦 | 🎛️ | 🏭 | `Robotic Excavation UML Statechart Supervisor` | 机器人挖掘监督器 / fuzzy low-level + statechart high-level | Global Control for Robotic Excavation Using Fuzzy Logic and Statecharts | 2000 | 用高层 `UML statechart` 调度 trenching 工作循环并把原子状态绑定到 `FLC_i` 模糊控制器 | task elements、digging sub-machine、characteristic functions、fuzzy low-level controllers | task element base + `UML statechart` + state-to-controller binding | mini-excavator + hydraulic sensors/encoders + fuzzy controller stack | 沟槽开挖、自动土方作业与工作循环监督 | 需求需可拆成稳定作业相位，并允许低层连续控制器按状态切换 | 🟢 | [desc.md](./global-control-for-robotic-excavation-using-fuzzy-logic-and-statecharts/desc.md) |
| 22 | ⏱️ | 🤝 | ⏱️ | `Timed Automata / UPPAAL Network` | 工业协议验证 / 定时自动机应用建模 | Modelling and Analysis of a Commercial Field Bus Protocol | 2000 | 用定时自动机网络建模 `AF100` bus coupler 并定位协议 / 实现缺陷 | `urgent/committed`、timeouts、diagnostic traces、abstraction ladder、semaphore race | `16` automata + `4` clocks + `32` integers + `UPPAAL` queries | `UPPAAL` + abstract `C-like` models + source-level debugging workflow | 工业现场总线、实时协议与数据链路层调试 | 协议需可抽成握手/timeout/sync logic 且核心问题在 race/延迟 | 🟢 | [desc.md](./modelling-and-analysis-of-a-commercial-field-bus-protocol/desc.md) |
| 23 | 🔣 | 🎛️ | ⏱️ | `Argos` | 同步语言 | Argos: an Automaton-Based Synchronous Language | 2001 | 用布尔 Mealy 机构造可组合的同步状态机语言 | local signals、encapsulation、refinement、causality checking | 图形 automata + 局部信号封装 + hierarchy | 同步编译与验证连接明确，无开放标准 | 实时反应式控制与同步控制器 | 需求以离散信号/广播协同为主且接受同步假设 | 🟢 | [desc.md](./argos-an-automaton-based-synchronous-language/desc.md) |
| 24 | 🔌 | 🤝 | 🌐 | `Interface Automata` | 模型提出 | Interface Automata | 2001 | 检查接口兼容与替换性 | compatibility、illegal states、alternating simulation | 输入/输出接口自动机 | 组合与精化语义成熟，无标准格式 | 组件接口匹配、服务组合 | 关注假设/保证式交互 | 🟢 | [desc.md](./interface-automata/desc.md) |
| 25 | 🔣 | 🎛️ | 🏭 | `Grafchart / JGrafchart` | 图形语言 / 工具载体 | GRAFCHART FOR PROCEDURAL OPERATOR SUPPORT TASKS | 2002 | 用步骤、过程和异常转移支撑工业操作规程与程序处理 | procedure step、exception transition、high-level tokens、animation | Grafchart charts + `G2` rules + `JGrafchart` runtime | Grafchart/JGrafchart 工具明确 | 批处理、operator support、程序规程 | 需求需显式步骤流、过程复用与异常中止 | 🟢 | [desc.md](./grafchart-for-procedural-operator-support-tasks/desc.md) |
| 26 | 🌊 | 🌡️ | 🌡️ | `CHARON` | 应用框架 / 软件架构 | A Framework and Architecture for Multi-Robot Coordination | 2002 | 用 agent+mode 统一多机器人控制、感知与协同 | 层次 agent、mode switching、连续流、共享信息 | `CHARON` 文本 DSL + `diff/alge/inv` + channels | `CHARON` + 多线程对象架构 + robot platform | 多机器人协调、编队、协同感知 | 需求需同时给出离散模式、连续控制和通信结构 | 🟢 | [desc.md](./framework-and-architecture-for-multi-robot-coordination/desc.md) |
| 27 | 🔣 | 🎛️ | ⏱️ | `RSML-e / NuSMV` | 验证工具链 / 翻译框架 | Model Checking RSML-e Requirements | 2002 | 把需求状态机自动翻译到可模型检查符号模型 | 层次状态变量、接口、表格逻辑、自动抽象 | `RSML-e` 规格 + translator + `NuSMV` modules | `Nimbus` + `NuSMV` + `PVS` | 飞控与高保证需求验证 | 需求可整理为有限状态、接口和表格条件 | 🟢 | [desc.md](./model-checking-rsmle-requirements/desc.md) |
| 28 | 🌊 | 🌡️ | 🌡️ | `Hybrid Automaton for Behavior Coordination` | 移动机器人行为协调 / hybrid automata 应用 | A Hybrid Control Approach to Action Coordination for Mobile Robots | 2002 | 用混成自动机协调 goal attraction 与 obstacle avoidance 行为 | behavior switching、sliding regularization、Filippov dynamics、unicycle model | behavior nodes + switching surfaces + sliding node + tracking controller | `Nomadic 200` + `Nserver` + cubic-spline path + tracking controller | 移动机器人点到点导航、避障与行为协调 | 系统可拆为有限 behaviors，且切换边界可由几何/距离条件表达 | 🟢 | [desc.md](./a-hybrid-control-approach-to-action-coordination-for-mobile-robots/desc.md) |
| 29 | 🔣 | 🎛️ | 🏭 | `Sequential Function Charts (SFC)` | 工业语义 | A Unifying Semantics for Sequential Function Charts | 2004 | 为 `IEC 61131-3 SFC` 提供统一可参数化 cycle semantics | steps、action qualifiers、parallelism、history、timed extension | steps/transitions + action blocks + priority orders | `PLC` 工具链和 `IEC` 标准明确 | `PLC` 顺控、工业自动化 | 需求可分解为步骤/守卫/动作并按扫描周期执行 | 🟢 | [desc.md](./a-unifying-semantics-for-sequential-function-charts/desc.md) |
| 30 | ⏱️ | 🎛️ | 🌡️ | `Timed Automata / UPPAAL Network for Multi-Robot Planning` | 多机器人规划 / 定时自动机应用建模 | Multi-Robot Planning: A Timed Automata Approach | 2004 | 用 timed automata network 求解共享网格中的多机器人协调规划 | grid workspace、movement clocks、occupancy array、`CTL` queries | obstacle / robot / control automata + channels + global occupancy array | `UPPAAL` + process templates + diagnostic queries | 门口通过、迷宫换位与多机器人高层协调 | 底层 controller 已保证按格移动抽象，环境可离散成网格 | 🟢 | [desc.md](./multi-robot-planning-a-timed-automata-approach/desc.md) |
| 31 | 🔣 | 🎛️ | 🏭 | `StateGraph` | 工具/库 | StateGraph - A Modelica Library for Hierarchical State Machines | 2005 | 在 Modelica 中提供层次状态机库 | `fire/newActive` 方程、parallel/alternative、composite step | steps/transitions/parallel/composite + Modelica equations | `Modelica.StateGraph` + logical blocks | 监督控制、物理过程联调 | 需求需与 Modelica 模型协同并接受单赋值约束 | 🟢 | [desc.md](./stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md) |
| 32 | ⏱️ | 🤝 | ⏱️ | `Timed I/O Automata` | 理论专著 | The Theory of Timed I/O Automata | 2005 | 组合实时组件并比较实现关系 | trajectories、receptiveness、simulation | 动作接口 + 时间轨迹 | 理论框架成熟，无标准格式 | 实时组件系统 | 需求同时包含接口与时间演化 | 🟢 | [desc.md](./the-theory-of-timed-input-output-automata/desc.md) |
| 33 | 🕸️ | 🏭 | 💻 | `Coloured Petri Nets` | 教程讲义 | Coloured Petri Nets | 2005 | 在 Petri 网中引入 typed token 与数据 | colour sets、simulation、state space | 网结构 + 颜色集 + 弧表达式 | 工具生态成熟，交换标准较弱 | 协议与数据驱动并发系统 | 并发 + 显式数据对象 | 🟢 | [desc.md](./coloured-petri-nets/desc.md) |
| 34 | 🔣 | 🎛️ | ⏱️ | `Polychronous Mode Automata` | 多时钟建模构件 | Polychronous Mode Automata | 2006 | 把多时钟数据流与 mode automata 统一到同一建模前端 | 弱/强抢占、多时钟、元模型扩展、Signal 编译 | `GME` metamodel + `Signal` equations + automata | `Polychrony` + `Signal-Meta` + `GME` | 航电与分布式嵌入式系统 | 需求同时含局部时钟、控制模式和数据流 | 🟢 | [desc.md](./polychronous-mode-automata/desc.md) |
| 35 | 🔣 | 🎛️ | 🌡️ | `PLEXIL` | 计划执行语言 / 执行载体 | Plan Execution Interchange Language (PLEXIL) | 2006 | 把 planner 输出统一落成可执行任务节点树 | node conditions、XML、lookup/command、deterministic execution | `NodeList/Command/Assignment` 树 + domain description + XML | universal executive + `CLARAty` + plan editor | 航天器 / 火星车自主任务执行 | 需求需显式命令接口、世界状态查询与时序条件 | 🟢 | [desc.md](./plan-execution-interchange-language-plexil/desc.md) |
| 36 | 🔣 | 🎛️ | 🌡️ | `XABSL` | 机器人行为语言 / 执行引擎 | XABSL - A Pragmatic Approach to Behavior Engineering | 2006 | 用 option hierarchy 组织复杂自主体行为 | option graph、activation path、symbols、basic behaviors、debugging | `XABSL` DSL + decision trees + XML/intermediate code | Ruby compiler + `XabslEngine` + monitor/profiler | RoboCup 与动态机器人行为控制 | 需求需可抽成层次技能、符号接口和 basic behaviors | 🟢 | [desc.md](./xabsl-a-pragmatic-approach-to-behavior-engineering/desc.md) |
| 37 | 📦 | 🎛️ | 🌡️ | `ARGO / Cortex` | 空间机器人操作框架 / 自主工具箱 | A Framework for Autonomous Space Robotic Operations | 2006 | 把空间机器人命令脚本与自治行为统一到层次 `FSM` 工具箱 | `HFSM`、guards/triggers、图形编辑、代码生成、远程监控 | 图形 `FSM/sub-FSM` + `JAVA` snippets + toolbox 组装 | `Cortex` + `RGCS` + `Remote/Log` toolboxes + simulator | 轨道机械臂、行星车与长时延空间机器人操作 | 任务需脚本化且存在长时延、低带宽或间歇通信 | 🟢 | [desc.md](./a-framework-for-autonomous-space-robotic-operations/desc.md) |
| 38 | 🔌 | 🤝 | 🌐 | `Transaction-Aware Web Service Interface / Protocol Interface` | Web 服务组合接口模型 / transaction-aware interface theory | Towards Formal Interfaces for Web Services with Transactions | 2006 | 把长事务服务组合中的补偿、故障处理与替换性压成形式接口 | signature/conversation/protocol interface、`EPA`、compensation、weak simulation | `SI + CI + PI + EPA -> LTS` | `EPA/LTS` semantics + weak simulation，原文无公开工具/交换格式 | 带补偿链的 Web service composition 与 service substitution | 交互需可抽成离散 actions，并显式区分 normal/compensation/fault handling | 🟢 | [desc.md](./towards-formal-interfaces-for-web-services-with-transactions/desc.md) |
| 39 | 🔣 | 🎛️ | 🌡️ | `Stateflow` | 形式语义 | An Operational Semantics for Stateflow | 2007 | 把工业 `Stateflow` chart 形式化为顺序化图形状态机语义 | junction、local events、`12 o'clock` ordering、安全子集 | states/junctions/transitions + linearized SOS | `Matlab/Simulink/Stateflow` 生态成熟 | 嵌入式控制器、混成系统离散部分 | 需求最终落到 `Stateflow` 工具链且接受工具优先级 | 🟢 | [desc.md](./an-operational-semantics-for-stateflow/desc.md) |
| 40 | 🌊 | 🌡️ | 🌡️ | `Nested Hybrid Automata (NHA)` | 城市自动驾驶控制架构 / 混成层次模式切换 | A Modular, Hybrid System Architecture for Autonomous, Urban Driving | 2007 | 用 `NHA` 统一城市驾驶情境切换、感知优先级与连续控制 | modes of operation、behavior voting、guard/reset、multi-level nesting | `HA/NHA` + planning block + behavior arbiter + continuous controllers | retrofitted `Cayenne` + `GPS/IMU` + camera/radar/LADAR，原文无公开代码 | 城市自动驾驶、路口通行、静态障碍绕行、停车 | 需求需存在稳定情境模式，并允许感知/控制器按模式切换 | 🟢 | [desc.md](./a-modular-hybrid-system-architecture-for-autonomous-urban-driving/desc.md) |
| 41 | 🕸️ | 🏭 | ⏱️ | `Time Petri Nets` | 教程讲义 | Time Petri Nets Part II: State Class based methods | 2008 | 在并发网上加入时间区间 | 静态区间、state class graph | P/T 网 + 变迁时间区间 | TINA 线成熟，标准格式较弱 | 实时并发流程与调度 | 并发资源流 + 时间窗口 | 🟢 | [desc.md](./time-petri-nets/desc.md) |
| 42 | 🧩 | 🌳 | 🧮 | `Tree Automata` | 教程专著 | Tree Automata Techniques and Applications | 2008 | 识别树、项与层次结构语言 | bottom-up、top-down、determinization、decision problems | ranked alphabet + 状态 + 树重写规则 | 理论与算法成熟，XML/hedge 在线路上衔接强 | AST、term rewriting、schema-like structural validation | 输入需显式树/项结构而非平坦事件串 | 🟢 | [desc.md](./tree-automata-techniques-and-applications/desc.md) |
| 43 | 🔣 | 🎛️ | 🏭 | `ModeGraph` | 工具/库 | ModeGraph - A Modelica Library for Embedded Control Based on Mode-Automata | 2008 | 在 Modelica 中实现安全层次状态机与 mode-automata 执行 | single-assignment、delayed transition、preemption、parallel | `Step/Transition/Composite/Parallel` + mode equations | Modelica 工具链明确，需语言扩展，无独立交换标准 | 嵌入式控制、混合控制、工业逻辑 | 需求需安全模式切换并与 Modelica 模型协同 | 🟢 | [desc.md](./modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md) |
| 44 | 📦 | 🎛️ | 🌡️ | `AnnieWAY CHSM` | 自动驾驶行为规划器 / 交通规则监督器 | Team AnnieWAY's Autonomous System for the 2007 DARPA Urban Challenge | 2008 | 用 `CHSM` 协调城市驾驶机动与交通规则遵循 | 层次状态、`MTC`、priority handling、recovery、zone navigation | route graph + scene assessment + `UML` CHSM + path stub generation | `VW Passat` + lidar + `DGPS/INS` + ECU + `CAN/Ethernet` | 城市自动驾驶、路口通行、停车区导航 | 需求需可抽成离散交通情境，并有下层轨迹跟踪与感知支撑 | 🟢 | [desc.md](./team-annieways-autonomous-system-for-the-2007-darpa-urban-challenge/desc.md) |
| 45 | 🕸️ | 🏭 | 🌡️ | `MOPN / GSPN for Multi-Robot Tasks` | 多机器人任务建模 / 分析执行框架 | Modelling, Analysis and Execution of Multi-Robot Tasks using Petri Nets | 2008 | 用 `Petri Nets` 统一多机器人任务、同步与性能分析 | macro places、predicate places、`MOPN/GSPN`、message synchronisation | action/environment layers + `PN` modules + macro-place expansion | `PN` analysis + Markov-chain based performance evaluation | robotic soccer、多机器人协作与同步任务 | 任务需可分解为离散动作/消息/环境谓词 | 🟢 | [desc.md](./modelling-analysis-and-execution-of-multi-robot-tasks-using-petri-nets/desc.md) |
| 46 | 🧩 | 📝 | 🧮 | `Weighted Automata` | 手册章节 | Weighted Automata Algorithms | 2009 | 在自动机/转导器上附加 semiring 权值 | semiring、path weight、determinization、minimization | 图结构 + label + weight + semiring 运算 | 算法体系成熟，但无统一交换标准 | 概率/代价/评分型字符串与转导建模 | 需求需保留有限状态骨架且每条路径带可组合权值 | 🟢 | [desc.md](./weighted-automata-algorithms/desc.md) |
| 47 | 🔣 | 🎛️ | 🌡️ | `Ptolemy II FSM / Modal Models` | 工具教程 | Finite State Machines and Modal Models in Ptolemy II | 2009 | 用状态机控制 refinement 切换并支撑异构执行 | guard/output/set action、mode refinement、microstep、local time | `FSMActor / ModalModel` + `MoML` + compatible directors | Ptolemy II 图形/Java/MoML 生态完整 | 异构嵌入式系统、CPS mode switching | 不同模式需挂不同 refinement 与执行域 | 🟢 | [desc.md](./finite-state-machines-and-modal-models-in-ptolemy-ii/desc.md) |
| 48 | 🔣 | 🎛️ | 🌡️ | `Modelica_StateGraph2` | 形式主义 / 工具库 | A New Formalism for Modeling of Reactive and Hybrid Systems | 2009 | 把 Modelica 状态机扩成安全层次并行 generalized steps | generalized steps、suspend/resume、delay、`NuSMV` verification | `\Gamma = \langle V_c,G,T,g_I \rangle` + ports + interpretation algorithm | `Modelica_StateGraph2` + `NuSMV` | reactive/hybrid systems | 需求含模式切换并需与物理模型联仿 | 🟢 | [desc.md](./a-new-formalism-for-modeling-of-reactive-and-hybrid-systems/desc.md) |
| 49 | 🔣 | 🎛️ | 🌡️ | `XRobots` | 领域特化 DSL | An Overview of XRobots: A Hierarchical State Machine-Based Language | 2011 | 用可参数化 behavior 组织移动机器人行为 | HSM、first-class behavior、by-value/by-reference、entry/exit | `Behavior` DSL + parameterized transitions | prototype compiler 路线，原文无公开工具 | 移动机器人行为编程 | 需求可拆为可复用行为并接受高阶参数化 | 🟢 | [desc.md](./an-overview-of-xrobots-a-hierarchical-state-machine-based-language/desc.md) |
| 50 | 📦 | 🎛️ | 🏭 | `Pallet Manipulation HFSM` | 托盘搬运行为架构 / 感知-操作层次状态机 | Robust Behavior and Perception using Hierarchical State Machines: A Pallet Manipulation Experiment | 2011 | 把托盘搜索、接近、识别、位姿细化和插叉操作组织成层次状态机 | active perception、回退边、pose refinement、component network | `RoboComp` components + `Forklift` statechart + `InnerModel XML` | `RoboComp` + `RobEx` + `OpenSceneGraph` + `Gazebo/Stage` + stereo/fork | 仓储托盘定位、接近与搬运 | 目标几何已知、场景半受控，且视觉 / 里程计可用 | 🟢 | [desc.md](./robust-behavior-and-perception-using-hierarchical-state-machines-a-pallet-manipulation-experiment/desc.md) |
| 51 | 📦 | 🎛️ | 🏭 | `Power-Line Inspection Robot Crossing FSM` | 输电巡检越障 `HRI` / step `FSM` | Human-Robot Interaction System Research for 500kV EHV Power Transmission Line Inspection Robot | 2011 | 用 crossing `FSM` 引导操作员完成高压线路巡检机器人越障 | 九步 crossing、remote/local autonomy、state monitor、protocol | dialogue pages + crossing states + `COM` protocol | `GCS` + `Ape32.dll` + `OpenGL` + wireless | 高压输电线路巡检、障碍跨越 | 环境结构稳定且专用机构 / 传感可用 | 🟢 | [desc.md](./human-robot-interaction-system-research-for-500kv-ehv-power-transmission-line-inspection-robot/desc.md) |
| 52 | 🔌 | 🤝 | 🌐 | `ConfiguredService with Context-dependent Contracts` | 服务组合契约 / 上下文敏感服务规格与验证 | Specification and Verification of Context-dependent Services | 2011 | 把服务功能、非功能、法律和上下文约束统一成可组合、可验证的契约模型 | context rules、service contracts、composition constructs、`UPPAAL` transformation | `ConfiguredService` tuple + composition expressions + `UPPAAL` templates | `FrSeC` 形式框架 + `UPPAAL` | 上下文敏感服务编排、应急服务组合、service provision | 服务接口、上下文和合同条款需可结构化枚举 | 🟢 | [desc.md](./specification-and-verification-of-context-dependent-services/desc.md) |
| 53 | 🔣 | 🎛️ | 🌡️ | `Modelica State Machines` | 语言扩展 | State Machines in Modelica | 2012 | 把状态机纳入 Modelica 语言核心 | 13 方程语义、immediate/delayed、reset/synchronize | Modelica blocks + transition equations + clock | Modelica 3.3 语言级支持明确 | 物理系统中的控制逻辑、嵌入式控制 | 状态逻辑需与同 clock 的 Modelica 模型原生集成 | 🟢 | [desc.md](./state-machines-in-modelica/desc.md) |
| 54 | 📦 | 🤝 | 🏭 | `Grafchart / JGrafchart + DPWS` | 工具扩展 / 服务编排载体 | Graphical Programming Language Support for Service Oriented Architecture in Automation | 2012 | 把可发现服务设备嵌入图形状态机协调逻辑 | `DPWS Object`、自动重绑、通知事件、方法式调用 | `JGrafchart` 图形模型 + `DPWS/WSDL` 绑定 | `JGrafchart` + `DPWS` discovery + `WSDL` | 服务化车间集成与设备协调 | 设备需以 `DPWS` 服务暴露并允许事件订阅 | 🟢 | [desc.md](./graphical-programming-language-support-for-service-oriented-architecture-in-automation/desc.md) |
| 55 | 🔣 | 🎛️ | 🌡️ | `rFSM Statecharts` | 机器人协调 DSL / OROCOS statecharts | Coordinating Robotic Tasks and Systems with rFSM Statecharts | 2012 | 用受限 statechart 表达机器人 coordination 逻辑 | hierarchy、structural priority、connectors、internal transitions、codel preemption | `states/transitions/connectors` + `Ecore/OCL` + executable DSL | `rFSM` reference implementation + `OROCOS/RTT` + UML-like notation | 组件协调、任务切换、reactive control | 需求需显式 coordination concern、事件驱动层次和安全可抢占执行 | 🟢 | [desc.md](./coordinating-robotic-tasks-and-systems-with-rfsm-statecharts/desc.md) |
| 56 | 📦 | 🎛️ | 🌡️ | `Universal Mission Controller / MEA` | `UUV` 任务控制 / `Prolog` mission-control engine | An Implemented Universal Mission Controller with Run Time Ethics Checking for Autonomous Unmanned Vehicles---A UUV Example | 2012 | 用通用 `MEE` 与 `Prolog` mission orders 执行可审计任务控制 `FSM` | `RBM` 三层、`MEA/MEE`、queries/commands、runtime ethics | state graph + structured mission orders + `Prolog` rules | `Allegro Prolog` + `RBM` + mission logs | `UUV` 长时自主任务、搜索/取样/会合 | 任务可拆为有限 phase 且可显式回答查询 | 🟢 | [desc.md](./an-implemented-universal-mission-controller-with-run-time-ethics-checking-for-autonomous-unmanned-vehicles/desc.md) |
| 57 | 📦 | 🎛️ | 🌡️ | `Exoskeleton Gait FSM` | 外骨骼监督控制器 / `CoP` 触发步态状态机 | A Method for the Autonomous Control of Lower Limb Exoskeletons for Persons With Paraplegia | 2012 | 用 12 状态 `FSM` 协调坐下、起立和步行切换 | `CoP` thresholds、trajectory templates、variable-gain `PD`、double support states | `FSM` + joint trajectories + `CoP` estimator + gain schedule | powered orthosis + IMU + joint encoders + microcontrollers | 截瘫辅助移动、坐站切换、平地步行 | 用户意图需能由重心与上身姿态稳定估计，且有辅助支撑 | 🟢 | [desc.md](./a-method-for-the-autonomous-control-of-lower-limb-exoskeletons-for-persons-with-paraplegia/desc.md) |
| 58 | 📦 | 🎛️ | 🌡️ | `ROSCo / Home-Robot HFSM` | 家用机器人行为构建 / `HFSM` 编辑执行器 | ROS Commander (ROSCo): Behavior Creation for Home Robots | 2013 | 用参数化 `HFSM` 构建并部署家用机器人行为 | hierarchy、parameterized states、`AR Tags`、behavior reuse | graphical `HFSM` + `RViz` demonstration + `SMACH` compile | `ROS Commander` + `RViz` + `SMACH` + `PR2` | 开门/开抽屉/递物等家居操作 | 任务可拆成技能链且环境可感知绑定 | 🟢 | [desc.md](./ros-commander-behavior-creation-for-home-robots/desc.md) |
| 59 | 📦 | 🌡️ | 🌡️ | `Grafchart / JGrafchart + FMI` | 工具扩展 / 协同仿真载体 | On Extending JGrafchart with Support for FMI for Co-Simulation | 2014 | 把图形顺控应用接入 `FMI` 协同仿真 | communication step、wrapper/FMU 导出、scan-cycle 对齐 | `JGrafchart` + `FMU`/XML + wrapper/export | `JGrafchart` + `FMI` + `CustomIO/SocketIO` | 控制器与物理模型联合验证 | 控制逻辑需为离散 scan-cycle，plant 可作为 `FMU` | 🟢 | [desc.md](./on-extending-jgrafchart-with-support-for-fmi-for-co-simulation/desc.md) |
| 60 | 🔌 | 🤝 | 🌐 | `Contract Automata` | 模型提出 | Automata for Analysing Service Contracts | 2014 | 分析多方契约匹配与责任 | agreement、weak agreement、liability | 向量动作自动机 + 组合 | 分析方法明确，生态偏研究型 | 服务编排、契约组合 | 多方 request/offer 关系清晰 | 🟢 | [desc.md](./contract-automata/desc.md) |
| 61 | 🕸️ | 🏭 | 🏭 | `Open-Path Multi-AGV CPN` | 仓储多 AGV 并发建模 / `CPN` 应用 | A Petri Net Model for an Open Path Multi-AGV System | 2014 | 用 `CPN` 统一开放路径 forklift `AGV` 的动作、安全占用与 deadlock 处理 | colours、meta-cell、virtual occupancy、monitor places、deadlock recovery | `CPN` + basic actions + cell/lane/drop-off places + recovery net | warehouse simulator 线明确，开放标准弱 | 自动分拣仓库、叉车 `AGV` 调度与通行安全 | 场景可离散成 cell 网络，且核心问题是并发占用与互锁 | 🟢 | [desc.md](./a-petri-net-model-for-an-open-path-multi-agv-system/desc.md) |
| 62 | 📦 | 🎛️ | 🌡️ | `SMACH + DMSL Decision-Augmented FSM` | 服务机器人行为组合 / 状态机+规则决策架构 | Combining Finite State Machine and Decision-Making Tools for Adaptable Robot Behavior | 2014 | 用 `SMACH` 任务骨架与 `DMSL` 规则块实现运行时行为适配 | localized decision blocks、profile parameters、`activate/cancel`、`OBSTRUCTED` branching | `SMACH` states + `DMSL if-then-else` + user/robot/env profiles | `HOBBIT` robot + `SMACH` + `DMSL` | 陪伴机器人找人、避障与上下文适配 | 任务需能抽成状态骨架，且上下文可结构化成 profile 参数 | 🟢 | [desc.md](./combining-finite-state-machine-and-decision-making-tools-for-adaptable-robot-behavior/desc.md) |
| 63 | 📦 | 🎛️ | 🌡️ | `Hybrid FES Exoskeleton Dual-FSM` | 康复外骨骼监督器 / dual-FSM 协同控制 | Hybrid FES-robot cooperative control of ambulatory gait rehabilitation exoskeleton | 2014 | 用 `t-FSM + c-FSM` 协调外骨骼助力、`FES` 学习与疲劳管理 | torque field、`ILC`、`TTI` fatigue、`NILC` convergence、gait events | `t-FSM/c-FSM` + torque field + `ILC` + fatigue estimator | `Kinesis` + `Rehastim` + torque sensors + embedded controller | 步态康复、截瘫辅助行走训练 | 需可检测 gait event，并可实时测力和调整刺激参数 | 🟢 | [desc.md](./hybrid-fes-robot-cooperative-control-of-ambulatory-gait-rehabilitation-exoskeleton/desc.md) |
| 64 | 🔣 | 🎛️ | 💻 | `SCXML` | 标准规范 | State Chart XML (SCXML): State Machine Notation for Control Abstraction | 2015 | 提供可执行层次状态机 XML 载体 | `state/parallel/history/datamodel/invoke` | SCXML XML 文档 | W3C 规范、Schema、测试套件 | 事件驱动流程与互操作 | 需要标准文本载体 | 🟢 | [desc.md](./scxml-state-machine-notation-for-control-abstraction/desc.md) |
| 65 | 🔌 | 🤝 | 🌡️ | `Interface Automata for Accessors / IoT Contracts` | IoT accessor 接口模型 / timed actor 契约分析 | An Interface Theory for the Internet of Things | 2015 | 协调 accessor、`DE director` 与 JavaScript callbacks 的接口兼容 | horizontal/vertical contracts、`AAC` callbacks、logical time、pruned composition | `A_DE + A_acc + A_JS -> pruned composition / closed LTS` | `Ptolemy II` accessors + JavaScript host + interface automata composition | timing-sensitive IoT applications 与 actor-accessor integration | 远端服务可抽成 accessor，且系统依赖逻辑时间事件语义 | 🟢 | [desc.md](./an-interface-theory-for-the-internet-of-things/desc.md) |
| 66 | 📦 | 🎛️ | 🌡️ | `FlexBE` | 系统框架 / 行为执行器 | A Comprehensive Software Framework for Complex Locomotion and Manipulation Tasks Applicable to Different Types of Humanoid Robots | 2016 | 用层次状态机在 `ROS` 框架中协调复杂人形机器人任务 | `HFSM`、outcome、input/output keys、autonomy level、behavior mirror | state classes + graphical editor + embedded behaviors + dataflow | `FlexBE` + `SMACH` + `ROS` + runtime control UI | 灾害响应人形机器人任务控制 | 任务可拆为高层 action states 且需要 operator-supervised autonomy | 🟢 | [desc.md](./a-comprehensive-software-framework-for-complex-locomotion-and-manipulation-tasks/desc.md) |
| 67 | 📦 | 🎛️ | 🌡️ | `VisualHFSM / JdeRobot` | 可视化 `HFSM` 工具 / 代码生成 | VisualHFSM 5: recent improvements in programming robots with automata in JdeRobot | 2016 | 图形化设计机器人 `HFSM` 并自动生成 `JdeRobot` 组件 | hierarchy、XML、C++/Python、runtime GUI、multithread templates | graphical editor + XML + state/transition code snippets | `VisualHFSM` + `JdeRobot` + runtime GUI + code generator | 移动机器人与无人机行为编程 | 接受 `JdeRobot` 组件架构并能在状态/转移内填写局部代码 | 🟢 | [desc.md](./visualhfsm-5-recent-improvements-in-programming-robots-with-automata-in-jderobot/desc.md) |
| 68 | 🔣 | 🎛️ | 🌡️ | `RoboChart` | 定时语义 / 形式化 DSL | Modelling and Verification of Timed Robotic Controllers | 2017 | 为机器人控制器提供带 budget/deadline 的 timed 状态机语义 | clock、`since/sinceEntry`、`wait`、deadline、`tock-CSP` | module/platform/controller/machine + timed primitives | `RoboTool` + `Timed CSP/tock-CSP` + `FDR` | timed robotic controllers、swarm transport、chemical detector | 需求含显式时间预算、deadline 和平台接口 | 🟢 | [desc.md](./modelling-and-verification-of-timed-robotic-controllers/desc.md) |
| 69 | 📦 | 🎛️ | 🌡️ | `SMACHA / SMACH` | 状态机装配 / 代码生成 | Rapid state machine assembly for modular robot control using meta-scripting, templating and code generation | 2017 | 用 `YAML` 和模板快速生成可执行 `SMACH` 状态机 | meta-scripting、templating、sub-scripts、container recursion | `YAML` scripts + `Jinja2` templates + generated Python `SMACH` | `SMACHA` API + `SMACH` + ROS/Gazebo/Baxter | `ROS` 任务控制、pick-place、stacking | 需求已接受 `SMACH` 运行时且存在高复用结构 | 🟢 | [desc.md](./rapid-state-machine-assembly-for-modular-robot-control/desc.md) |
| 70 | 📦 | 🎛️ | 🌡️ | `RAFCON` | 图形任务编程 / mission control 载体 | RAFCON: A Graphical Tool for Task Programming and Mission Control | 2017 | 用图形层次状态机协调复杂机器人任务 | hierarchy、concurrency、library state、data flow、remote monitoring | 图形状态机 + Python execute + ports/data flow | GTK+ GUI + execution engine + API | 复杂机器人任务编排与监控 | 需求需能拆成层次技能并依赖中间件执行 | 🟢 | [desc.md](./rafcon-graphical-tool-for-task-programming-and-mission-control/desc.md) |
| 71 | 📦 | 🎛️ | 🏭 | `Industrial Mobile Manipulation Flow Control` | 工业移动操作 flow-control / `SMACH` 层次状态机载体 | Toward fully autonomous mobile manipulation for industrial environments | 2017 | 用高层技能状态机统一工业 fetch-and-carry 任务训练与自主执行 | hierarchical flow control、data flow、skill states、setup/execution phases | `SMACH` states + task parameters + `ROS` modules | `ROS` + `SMACH` + `SensorNet` + object recognition/registration | 工业工位间取放、搬运与供料 | 任务可写成技能链，且 setup phase 可训练工位 / 对象知识 | 🟢 | [desc.md](./toward-fully-autonomous-mobile-manipulation-for-industrial-environments/desc.md) |
| 72 | 🔣 | 🎛️ | 💻 | `UML State Machine` | 标准规范 | OMG Unified Modeling Language (OMG UML), Version 2.5.1 | 2017 | 标准化行为/协议状态机元模型 | regions、pseudostates、XMI | 图形建模 + metamodel + XMI | OMG 标准和工具生态成熟 | MDE、跨工具交换 | 需要与 UML 语境集成 | 🟢 | [desc.md](./uml-251-specification/desc.md) |
| 73 | ⏱️ | 🎛️ | 🌡️ | `Timed Automata Network for ROS Communication` | ROS 通信验证 / 定时自动机应用建模 | Formal Verification of ROS-Based Robotic Applications Using Timed-Automata | 2017 | 把 ROS 节点通信、队列和 callback 时序压成可验证 timed automata network | queue overflow、callback timing、timeouts、priority starvation | publisher/subscriber/channel/queue automata + `UPPAAL` queries | `ROS` + `Kobuki` + `UPPAAL` | ROS 机器人中间件时序分析、消息安全与控制活性验证 | topic/callback 结构明确，关键时序参数可提取 | 🟢 | [desc.md](./formal-verification-of-ros-based-robotic-applications-using-timed-automata/desc.md) |
| 74 | 🧩 | 🎛️ | 🌡️ | `Educational Robotics FSM` | 教育机器人控制 / `FSM` 应用教程 | Using Finite State Automata in Robotics | 2018 | 用普通 `FSM` 组织 line follower、竞赛机器人等入门控制任务 | tuple definition、transition table、`switch-case`、Block language | state diagram + transition matrix + `C/Blocks` | `C/MakeCode` + `micro:bot` + `MART Friday Bot` + `Stateflow` refs | 教育机器人、竞赛机器人、简单离散控制 | 任务可离散成有限模式，传感器输入可事件化 | 🟢 | [desc.md](./using-finite-state-automata-in-robotics/desc.md) |
| 75 | 📦 | 🎛️ | 🌡️ | `Cardiac Rehabilitation Social Robot FSM` | 心脏康复社交机器人监督器 / session `FSM` | Architecture for a Social Assistive Robot in Cardiac Rehabilitation | 2018 | 用会话 `FSM` 协调监护、鼓励、姿态纠正、疲劳询问与风险求助 | monitor/motivation/posture-correct/warning/emergency states、behavior timeline、therapy events | `SARI` + session `FSM` + behavior modules + `NAO` actions | `NAO` + `Naoqi/DCM` + PC/tablet rehab interface + remote TCP/IP link | 心脏康复训练中的社交辅助、监护与风险干预 | 需要稳定病人生理/姿态事件流，并接受监督器按阈值切换干预模式 | 🟢 | [desc.md](./architecture-for-a-social-assistive-robot-in-cardiac-rehabilitation/desc.md) |
| 76 | 📦 | 🤝 | 🌡️ | `Embodied Agent / LLFSM + Whiteboard` | 设计方法 / 通信执行架构 | Communication Within Multi-FSM Based Robotic Systems | 2018 | 用多 `FSM` 子系统、`LLFSM` 与白板通信生成机器人控制器 | embodied agent、hierarchical `FSM`、transition function、terminal condition、shared memory | embodied-agent 规格 + subsystem `FSM` + `LLFSM` + whiteboard | `gusimplewhiteboard` + `LLFSM` runtime/codegen + distributed UDP sharing | 多子系统机器人控制器与通信解耦设计 | 系统需可拆成周期运行的 communicating subsystems | 🟢 | [desc.md](./communication-within-multi-fsm-based-robotic-systems/desc.md) |
| 77 | 🔣 | 🎛️ | 🌡️ | `RoboSim` | 仿真 DSL / 一致性验证 | Verified Simulation for Robotics | 2019 | 用周期化状态机描述仿真并验证其与设计一致 | cycle period、`exec`、register I/O、scheduling assumptions、refinement | module/controller/simulation machine + cyclic exec | `RoboSim` + `RoboChart` + `tock-CSP` + `FDR` | verified simulation、obstacle avoidance、transport swarm | 仿真按周期执行且传感器/执行器可抽成寄存器 | 🟢 | [desc.md](./verified-simulation-for-robotics/desc.md) |
| 78 | 📦 | 🎛️ | ⏱️ | `LLFSM Walking Controller` | 步行机实时控制架构 / `LLFSM` 应用载体 | Finite state automaton based control system for walking machines | 2019 | 用 `LLFSM` 统一全局导航、局部导航与步态切换 | hierarchical FSMs、whiteboard、gait switching、`QNX` | `MiEditLLFSM` + whiteboard repositories + layered `FSMs` | `QNX` + `MiEditLLFSM` + gait library + hexapod platform | 多足步行机避障导航与步态管理 | 任务需分层为 mission/navigation/gait，且 guard 可从传感器生成 | 🟢 | [desc.md](./finite-state-automaton-based-control-system-for-walking-machines/desc.md) |
| 79 | 🔣 | 🎛️ | 🌡️ | `RoboChart` | 机器人 DSL / 形式验证工具链 | RoboChart: modelling and verification of the functional behaviour of robotic applications | 2019 | 用受限 `UML` 状态机建模并自动生成验证语义 | metamodel、well-formedness、timed primitives、`CSP` semantics | module/controller/machine + graphical/textual editors | `RoboTool` + `CSP-M/tock-CSP` + `FDR` + Eclipse | 高可信机器人控制器建模与验证 | 需求需显式平台接口、状态逻辑和时间约束 | 🟢 | [desc.md](./robochart-modelling-and-verification-of-robotic-applications/desc.md) |
| 80 | 📦 | 🤝 | 🌐 | `Underwater Swarm Pheromone FSM` | 群体监测协调器 / 弱通信搜索-汇报 `FSM` | A Pheromone-Inspired Monitoring Strategy Using a Swarm of Underwater Robots | 2019 | 用三态 `FSM` 协调 `AOI` 搜索、节点访问与目标上报 | `Search/Visit/Report`、virtual pheromone、matrix merge、`t_back` | `P_i(t)` matrix + communication nodes + behavior law + 3-state `FSM` | communication network + waypoint/`PID` + lake `USV` experiments | 海域监测、沉船 / 资源搜索、静态目标巡检 | `AOI` 需可网格化，且允许部署通信节点并定期回站同步 | 🟢 | [desc.md](./a-pheromone-inspired-monitoring-strategy-using-a-swarm-of-underwater-robots/desc.md) |
| 81 | 📦 | 🎛️ | 🌡️ | `Delivery Stair-Climbing State Machine` | 递送机器人楼梯机动监督器 / timing-state controller | A Robot with Decoupled Mechanical Structure and Adapted State Machine Control for Both Ground and Staircase Situations | 2019 | 用 Case 状态机组织姿态校正、抬升、滑移与回地面 | `SC1..SC7`、EHs、wheel-legs、posture adjustment、ground/stair modes | sensor guards + Case states + EH/wheel actions + decoupled chassis/tetrapod | hexapod robot + Mecanum wheels + EH encoders + laser sensors | 楼梯递送、室内转向、载货移动机器人 | 需求需匹配规则楼梯和解耦式轮腿硬件结构 | 🟢 | [desc.md](./a-robot-with-decoupled-mechanical-structure-and-adapted-state-machine-control-for-both-ground-and-staircase-situations/desc.md) |
| 82 | ⏱️ | 🎛️ | 🏭 | `Timed Automata Network for SCADA Attack Detection` | SCADA 攻击检测 / 定时自动机应用建模 | Timed Automata Networks for SCADA Attacks Real-Time Mitigation | 2019 | 把 pressure/pump 日志离散成同步 timed automata 并用 `TCTL` 判定攻击窗口 | equal-width discretisation、`Up/Basal/Low`、sync channel、attack queries | feature logs -> per-feature automata + clocks + `TCTL` reachability | `UPPAAL` + SCADA dataset + log-to-model pipeline | 气体管网 SCADA 攻击检测与实时告警 | 信号需可窗口化离散，攻击模式可写成有限状态与计数阈值 | 🟢 | [desc.md](./timed-automata-networks-for-scada-attacks-real-time-mitigation/desc.md) |
| 83 | 📦 | 🎛️ | 🌡️ | `MERLIN` | 认知架构 / 规划-执行状态机桥接 | MERLIN a Cognitive Architecture for Service Robots | 2020 | 用 `ROSPlan + SMACH` 统一长期任务规划与 action 执行 | mission/planning/executive/reactive layers、`PDDL`、`actionlib`、replanning | `PDDL` + Goal Dispatcher/Executor `FSM` + action `FSMs` | `ROSPlan` + `SMACH` + `actionlib` + `SMACH Viewer` | 服务机器人、assistive robots、competition tasks | 需求需能写成 `PDDL` goals，且动作可封装为状态机执行单元 | 🟢 | [desc.md](./merlin-a-cognitive-architecture-for-service-robots/desc.md) |
| 84 | 📦 | 🎛️ | 🌡️ | `Meal Assistance FSM` | 助餐任务管理 / active-feeding `FSM` | Active Robot-Assisted Feeding with a General-Purpose Mobile Manipulator: Design, Evaluation, and Lessons Learned | 2020 | 用任务 `FSM` 协调取食、擦勺与送入口中 | `TN/TA` 转移、motion primitives、anomaly handling、GUI | task `FSM` + motion parameter set + perception outputs | `PR2` + web GUI + execution monitor + food/mouth estimators | assistive feeding、主动喂食 | 取食和嘴部位姿可估计且需异常可中止 | 🟢 | [desc.md](./active-robot-assisted-feeding-with-a-general-purpose-mobile-manipulator/desc.md) |
| 85 | 📦 | 🎛️ | 🌡️ | `Waiter Motion Strategy FSM` | 餐厅服务机器人运动策略监督器 / `VelProSMACH` | Waiter Robots Conveying Drinks | 2020 | 用 `Dock/Cruise` 状态切换 step/ramp/S-velocity 以兼顾平稳与效率 | `Dock` strategy hub、`Cruise`、smooth throttle/brake、jerk-limited S-profile | `SMACH` states + velocity increment equations + `move_base` inputs | `ROS` + `SMACH` + `move_base` + `AMCL` + LiDAR/IR | 餐厅送饮料、送餐与回位导航 | 载荷类型需可分类，且已有稳定导航与障碍感知栈 | 🟢 | [desc.md](./waiter-robots-conveying-drinks/desc.md) |
| 86 | 📦 | 🎛️ | 🏭 | `HVTL Multi-Task Maintenance Robot FSM` | 输电线路维护机器人监督器 / 多任务层次 `FSM` | Autonomous Behavior Intelligence Control of Self-Evolution Mobile Robot for High-Voltage Transmission Line in Complex Smart Grid | 2020 | 用多任务层次 `FSM` 协调输电线路维护中的双臂、末端执行器与移动平台 | 12-bit state vector、`JMB/AMB/RMB` behavior hierarchy、task-specific FSMs、action database | state vector + behavior hierarchy + task `FSM` + motion controller | wheel-arm compound robot + dual manipulators + multi-sensor control stack | 高压输电线路绝缘子、引流板和阻尼器维护 | 任务需可离散成关键姿态与事件，并具备可重构执行器与状态识别前提 | 🟢 | [desc.md](./autonomous-behavior-intelligence-control-of-self-evolution-mobile-robot-for-high-voltage-transmission-line-in-complex-smart-grid/desc.md) |
| 87 | 📦 | 🎛️ | 🌡️ | `Cotton Harvesting Visual-Servo FSM` | 农业采摘任务管理器 / 视觉伺服状态机 | Center-Articulated Hydrostatic Cotton Harvesting Rover Using Visual-Servoing Control and a Finite State Machine | 2020 | 用相对坐标 guard 组织 rover 微调、机械臂对准与棉桃采摘 | `tiny YOLOv3`、`ZED` depth、`Algorithm 1`、`X_b/Y_b/Z_b` guards | `SMACH` + vision/depth + rover/manipulator actions | `ROS` + `SMACH` + `ZED` + `tiny YOLOv3` + vacuum picker | 棉田棉桃检测、对准与逐颗采摘 | 目标需可检测且在末端执行器可达工作空间内 | 🟢 | [desc.md](./center-articulated-hydrostatic-cotton-harvesting-rover-using-visual-servoing-control-and-a-finite-state-machine/desc.md) |
| 88 | 🔌 | 🤝 | 🌐 | `Featured Modal Contract Automata (FMCA)` | 服务契约组合 / 可变性控制综合 | Controller Synthesis of Service Contracts with Variability | 2020 | 在服务契约上同时编码产品线约束与 urgent/lazy 请求并综合 mpc | feature constraints、urgent/lazy、semi-controllability、canonical products | `FMCA` + feature model + product validity + mpc synthesis | `FMCAT` + `CAT/CATLib` + `FeatureIDE` | `SLA` 驱动的服务产品线与契约编排 | 服务需可写成 request/offer 契约并存在稳定配置空间 | 🟢 | [desc.md](./controller-synthesis-of-service-contracts-with-variability/desc.md) |
| 89 | 🕸️ | 🏭 | 🌡️ | `GSPNR / MRA for Persistent Multi-Robot Tasks` | 持续任务规划 / reward-based Petri synthesis | Long-Run Multi-Robot Planning under Uncertain Action Durations for Persistent Tasks | 2020 | 用 `GSPNR` 与 `MRA` 综合长期平均收益最优的多机器人持续任务策略 | immediate/exponential transitions、place rewards、`LRA`、`SSP` reduction | reward `GSPNR -> embedded MRA -> LRA` policy | `GSPNR` / `MRA` / `SSP` policy-synthesis chain | 持续监测、长期巡检与充电协同任务 | 团队状态可有限 marking 化，且动作时长可近似指数分布 | 🟢 | [desc.md](./long-run-multi-robot-planning-under-uncertain-action-durations-for-persistent-tasks/desc.md) |
| 90 | 🔣 | 🤝 | 🌡️ | `SEAD / MDL` | 领域特化框架 / 机动描述语言 | A Hierarchical State-Machine-Based Framework for Platoon Manoeuvre Descriptions | 2021 | 把 platoon manoeuvre 统一成 leader-perspective 分层状态机与 JSON 描述 | idle states、action primitives、PME/RSM、SIM wrapper、MDL | idle states + sub-manoeuvres + `JSON MDL` | manoeuvre catalogue + MDL parser + simulation | 车队 join/split/lane-change/gap-close 协同行为 | 需求需存在 leader-follower 角色与 V2V 协同协议 | 🟢 | [desc.md](./hierarchical-state-machine-based-framework-for-platoon-manoeuvre-descriptions/desc.md) |
| 91 | 🔣 | 🎛️ | 🌡️ | `DSD` | 行为 DSL / 轻量决策框架 | DSD - Dynamic Stack Decider: A Lightweight Decision Making Framework for Robots and Software Agents | 2021 | 用栈式 `DSL` 把行为树式重评估和状态机式 statefulness 结合 | decision/action elements、reevaluation、interrupt、action sequences、traceable stack | `DSL` 描述 `DAG` + decision/action modules + runtime stack | open-source `DSD` + `ROS/rqt` visualization + reusable modules | 机器人与软件 agent 的高层行为控制 | 需求需频繁改控制流、持续检查前置条件并保留决策历史 | 🟢 | [desc.md](./dsd-dynamic-stack-decider/desc.md) |
| 92 | 📦 | 🎛️ | 🌡️ | `Hierarchical FSM Driving Decision Framework` | 自动驾驶行为规划 / 分层决策框架 | Decision making framework for autonomous vehicles driving behavior in complex scenarios via hierarchical state machine | 2021 | 用三层状态机把场景识别、行为评分和动作选择串成自动驾驶决策链 | scenario FSM、energy-efficiency function、state transition matrix、lane vacancy grid | 三层 `FSM` + 能效函数 + 转移矩阵 + `PreScan/Simulink` | `PreScan` + `MATLAB/Simulink` + GPS/radar sensing | 结构化道路自动驾驶行为决策 | 需求可分解为场景分类、候选行为评分和离散动作集 | 🟢 | [desc.md](./decision-making-framework-for-autonomous-vehicles-driving-behavior-in-complex-scenarios-via-hierarchical-state-machine/desc.md) |
| 93 | 📦 | 🎛️ | 🏭 | `Eye-Hand FSM HRC` | `HRC` 交互控制器 / `VR` 装配状态机 | Human-Robot Collaborative Assembly Based on Eye-Hand and a Finite State Machine in a Virtual Environment | 2021 | 用眼-手共指与 `FSM` 组织对象选择、自动抓取和映射微调装配 | eye-hand trigger、`PRM` auto-capture、mapping mode、gesture classes | `Leap + Tobii + Unity/Simulink FSM + PRM` | `Leap Motion` + `Tobii` + `Unity` + `Simulink` + `UDP` | 虚拟协同装配、抓取搬运与精细放置 | 需求需可离散化对象/目标，并允许“自动搬运 + 人工微调”分工 | 🟢 | [desc.md](./human-robot-collaborative-assembly-based-on-eye-hand-and-a-finite-state-machine-in-a-virtual-environment/desc.md) |
| 94 | 📦 | 🎛️ | 🌡️ | `FSM-CLF-CBF Lane Change Controller` | 安全关键控制器 / `FSM + CLF-CBF-QP` | Rule-Based Safety-Critical Control Design using Control Barrier Functions with Application to Autonomous Lane Change | 2021 | 用 `FSM` 切换 `CLF-CBF-QP` 约束组，实现可回退的安全关键变道控制 | `ACC/L/R/BL/BR`、safe-set switching、`CBF/CLF`、high-rate QP | `FSM` + kinematic bicycle model + `CLF-CBF-QP` | GitHub code + simulation videos + barrier-function toolchain | 高速/城市道路安全关键变道 | 需求需有稳定周车感知，并接受车道级机动与安全距离约束建模 | 🟢 | [desc.md](./rule-based-safety-critical-control-design-using-control-barrier-functions-with-application-to-autonomous-lane-change/desc.md) |
| 95 | 📦 | 🎛️ | 🏭 | `SmHPFC` | 垃圾分拣机械臂监督器 / 状态机驱动 hybrid control | State Machine-Based Hybrid Position/Force Control Architecture for a Waste Management Mobile Robot with 5DOF Manipulator | 2021 | 用状态机切换位置 / 力控制并完成抓取投放 | `S`-matrix、homing/position/force states、vision-guided grasping、Festo stack | state machine + `S_p/S_f` + `PID` branches + direct kinematics | Festo `EXCM/EGSK/ERMO/HGPLE` + `PLC` + `CoDeSys` + vision module | 垃圾分拣、抓取投放、仓储式回收 | 目标类型与深度需可检测，执行器需支持控制模式切换 | 🟢 | [desc.md](./state-machine-based-hybrid-position-force-control-architecture-for-a-waste-management-mobile-robot-with-5dof-manipulator/desc.md) |
| 96 | 📦 | 🎛️ | 🌡️ | `Procedure-Observer Surgical Statechart` | 半自主手术流程监督器 / observer-procedure statechart | Modeling of Surgical Procedures Using Statecharts for Semi-Autonomous Robotic Surgery | 2021 | 用 procedure-observer 双区域 statechart 把手术知识、感知触发和 surgeme 执行接入同一闭环 | phase/action/surgeme hierarchy、parallel observers、trigger-only observers、revised statechart rules | procedure region + observer `FSMs` + triggers + surgeme library | `SARAS` platform + speech/force/feature observers + dual-arm surgical setup | 半自主机器人手术流程监督与术中事件驱动执行 | 需求需能把手术知识拆成 phase-action-surgeme 层级，并由 observers 提供稳定触发 | 🟢 | [desc.md](./modeling-of-surgical-procedures-using-statecharts-for-semi-autonomous-robotic-surgery/desc.md) |
| 97 | 📦 | 🎛️ | 🏭 | `Floor-Tiling FSM` | 施工自动化监督器 / 视觉测量铺砖状态机 | Robot Floor-Tiling Control Method Based on Finite-State Machine and Visual Measurement in Limited FOV | 2021 | 用 `S0..S10` 状态闭环协调测量、纠偏与铺砖完成 | `\Sigma_{fsm}=\{S,A,P,C\}`、`con1/con2/con3`、`D1/D2/D3`、directed graph | state/action/parameter/condition table + graph + robot arm actions | `FTR-II` + `ROS` + camera + laser sensor + robot arm | 地砖铺设、施工定位与在线纠偏 | 砖块几何与工位需稳定，且视觉测量能可靠提供偏差参数 | 🟢 | [desc.md](./robot-floor-tiling-control-method-based-on-finite-state-machine-and-visual-measurement-in-limited-fov/desc.md) |
| 98 | 📦 | 🎛️ | ⏱️ | `Asynchronous WMR FSM Controller` | 移动机器人控制器 / 事件驱动 FSM | Design and Implementation of an Asynchronous Finite State Controller for Wheeled Mobile Robots | 2022 | 用 event-based `FSM` 协调轮式移动机器人车道跟踪与遇障换道 | obstacle guards、`PID/P` controller、orientation update、`Stateflow` deployment | `Stateflow` chart + sensor guards + `Simulink` blocks + `PWM` outputs | `Simulink/Stateflow` + `STM Nucleo` + ultrasonic/encoder sensors | 三车道避障、embedded control lab、教学原型 | 需求需可抽成有限车道状态，并接受阈值守卫与简化换道假设 | 🟢 | [desc.md](./design-and-implementation-of-an-asynchronous-finite-state-controller-for-wheeled-mobile-robots/desc.md) |
| 99 | 📦 | 🤝 | 🌐 | `Embodied Agent / Binary Decomposition + FIPA HFSM` | 通信优先设计方法 / agent-FSM 规格 | Communication-Focused Top-Down Design of Robotic Systems Based on Binary Decomposition | 2022 | 用 binary decomposition + `FIPA` protocol 规格化机器人系统控制器 | agent groups、ACL messages、`HFSM` content、protocol verification、`ROS` implementation | requirements tree + group decomposition + channels/protocols + agent `FSM/HFSM` | `IEEE FIPA ACL` + `OWL` + `ROS 1/RPC` + `ClassInterfaceInfo` | companion robot、多 agent task coordination | 系统需可拆为显式 agents，并把 conversation/protocol 当作一等对象建模 | 🟢 | [desc.md](./communication-focused-top-down-design-of-robotic-systems-based-on-binary-decomposition/desc.md) |
| 100 | 📦 | 🎛️ | 🌡️ | `YASMIN` | `ROS 2` 状态机库 / 运行时载体 | YASMIN: Yet Another State MachINe library for ROS 2 | 2022 | 为 `ROS 2` 提供轻量 `FSM/HFSM` 行为层库 | blackboard、nested state machines、Python/C++、viewer | library API + shared blackboard + web viewer | GitHub repo + `ROS 2` integration + web viewer | 服务机器人行为控制与执行层编排 | 需求基于 `ROS 2` 且可用 `FSM/HFSM` 表达 | 🟢 | [desc.md](./yasmin-yet-another-state-machine/desc.md) |
| 101 | 📦 | 🤝 | 🏭 | `Safety4.0 Dynamic FSM` | 安全模式框架 / 风险分析载体 | Towards safety4.0: A novel approach for flexible human-robot-interaction based on safety-related dynamic finite-state machine with multilayer operation modes | 2022 | 把 `HRI` 交互层级、operation clusters 与 safety functions 压成动态安全状态机 | multilayer modes、clustered states、safety guards、dynamic risk analysis | level planner + clustered modes + state graphs + safety-function formulas | dynamic risk assessment tool + `ISO 12100/10218/15066` mapping | 工业 `HRC/HRI` 工作站的安全规划与运行模式切换 | 需求需显式交互层级、协作模式和安全功能集合 | 🟢 | [desc.md](./towards-safety4-0-flexible-human-robot-interaction-based-on-safety-related-dynamic-finite-state-machine-with-multilayer-operation-modes/desc.md) |
| 102 | 📦 | 🎛️ | 🌡️ | `FSM-HSVM Exoskeleton Locomotion Recognizer` | 外骨骼模式识别器 / `FSM`-constrained `HSVM` | FSM-HSVM-Based Locomotion Mode Recognition for Exoskeleton Robot | 2022 | 用 `FSM` 约束可达模式转移，并让 `HSVM` 完成实时 locomotion-mode 分类 | five locomotion modes、eight legal transitions、`IMU/FSR` features、local HSVM sub-classifiers | feature vector + `HSVM` tree + locomotion-mode `FSM` | lower-limb exoskeleton + `IMU/FSR` sensing + embedded recognition pipeline | 外骨骼平地、楼梯与坡道模式识别及后续控制切换 | 需求需存在稳定 gait mode 集合，且模式切换可由有限状态约束表达 | 🟢 | [desc.md](./fsm-hsvm-based-locomotion-mode-recognition-for-exoskeleton-robot/desc.md) |
| 103 | 📦 | 🎛️ | 🏭 | `HFSM Task Allocation` | 人机协同装配任务分配 / workload-aware `HFSM` | A Hierarchical Finite-State Machine-Based Task Allocation Framework for Human-Robot Collaborative Assembly Tasks | 2022 | 把任务分解、能力评估、workload 和执行分派统一到 `HFSM` | task selector/allocator、capability、workload、parallel tasks | `HFSM` modules + task tables + workload model + `MoveIt` | `Panda` + `ROS` + `Matlab` + `Xsens` + `MoveIt` | 人机协同装配与并行作业分配 | 任务可离散分解，human/robot capability 与 workload 可估计 | 🟢 | [desc.md](./a-hierarchical-finite-state-machine-based-task-allocation-framework-for-human-robot-collaborative-assembly-tasks/desc.md) |
| 104 | 📦 | 🎛️ | 🌡️ | `Spacer Installation Harel Statechart` | 安装任务状态图 / 专用 end-effector 控制器 | Autonomous Installation of Electrical Spacers on Power Lines Using Magnetic Localization and Special End Effector | 2023 | 用带超状态的安装状态图编排导线定位、servoing、工具旋转和夹具闭合 | superstates、pose guards、current threshold、magnetic localization | `Harel statechart` + `x_ap/x_pp/x_ip` + `ROS/MoveIt` | `ROS` + `MoveIt!` + `OMPL/RRT` + `smach_ros` + magnetometers | 电力线间隔棒自主安装 | 需求需有平行导线、专用末端执行器和可工作的磁定位前提 | 🟢 | [desc.md](./autonomous-installation-of-electrical-spacers-on-power-lines-using-magnetic-localization-and-special-end-effector/desc.md) |
| 105 | 🔌 | 🤝 | 🌐 | `Contract Automata / CARE` | 运行时实现 / orchestration engine | A Runtime Environment for Contract Automata | 2023 | 把 contract automata orchestration 落成可执行服务运行时并保证实现遵守契约 | centralised/distributed actions、typed labels、choice policies、`Uppaal` validation | `CATLib` synthesis + `CARE` wrappers + socket interactions | `CARE` + `CATLib` + `CATApp` + `Uppaal` model | contract-based applications、service orchestration runtime | 服务接口需可映射为 contract actions 且允许 orchestrator/wrapper | 🟢 | [desc.md](./a-runtime-environment-for-contract-automata/desc.md) |
| 106 | 🌊 | 🌡️ | 🌡️ | `Hybrid Automata + Supervisory Control` | 混成系统应用架构 / 分层监督控制 | A Hybrid Systems-Based Hierarchical Control Architecture for Heterogeneous Field Robot Teams | 2023 | 用 hybrid automata 与 modular supervisor 组织 `UAV+UGV` 田间协作控制 | `CTS/DES` coupling、specification automata、controllability、modular supervisors | `G_h` plant + specs + `G_A \parallel G_{B1} \parallel G_{B2}` + `HSHC` | `MATLAB` + `TCT` + `V-REP` + swarm control | 异构田间机器人协作、障碍规避与编队 | 需求需同时含离散任务事件与连续动力学对象 | 🟢 | [desc.md](./a-hybrid-systems-based-hierarchical-control-architecture-for-heterogeneous-field-robot-teams/desc.md) |
| 107 | 📦 | 🎛️ | 🏭 | `SMACC Parcel Handling Supervisor` | `SMACC` 应用监督器 / 工业拣放系统 | Robotic System for Post Office Package Handling | 2023 | 用 `SMACC` 监督器协调抓取位姿同步、路径规划与包裹拣放循环 | `Orthogonals/Clients/Events`、grasp pose、multi-PC sync、`MoveIt` integration | grasp pose + `SMACC` states + `ROS` parameter server + `MoveIt!` planning | `SMACC` + `MoveIt!` + `UR` driver + `Dex-Net` + `Zivid` | parcel sorting、industrial pick-place | 需求需有稳定 grasp pose 来源、重复循环流程和 `ROS` 栈执行环境 | 🟢 | [desc.md](./robotic-system-for-post-office-package-handling/desc.md) |
| 108 | 📦 | 🎛️ | 🌡️ | `SMACH Mission Supervisor / AutoPlant` | 任务监督器 / 应用控制系统 | Design and Implementation of a Control System for an Autonomous Reforestation Machine Using Finite State Machines | 2023 | 用 `SMACH` 监督器协调造林机器的移动车体、吊机、规划器与种植单元 | hierarchical `FSM`、parallel states、ROS actions/services、digital twin、simulator | top-level `FSM` + submachines + status variables + client actions | `ROS` + `SMACH` + `MoveIt` + `RViz/URDF` + custom simulator | 自主造林机与林业作业流程控制 | 任务需可拆成顺序/并行动作并通过 outcomes 协调多个子系统 | 🟢 | [desc.md](./design-and-implementation-of-a-control-system-for-an-autonomous-reforestation-machine-using-finite-state-machines/desc.md) |
| 109 | 📦 | 🤝 | 🌐 | `EFSMSG` | 协同计算模型 / 资源-状态图 | Finite State Machines-Based Path-Following Collaborative Computing Strategy for Emergency UAV Swarms | 2024 | 用扩展有限状态机空间时间图统一建模 `UAV` 资源状态、跨时隙链路和任务映射 | `EFSMSG`、task `DAG`、cross-slot caching、`CSABPSO` | `UAV FSM` + `SG/EFSMSG` + mapping matrix | `MATLAB` simulation + `CSABPSO` solver | 应急 `UAV` 群协同计算与低时延卸载 | 需求需有路径跟随编队、异构机载资源和可写成 `DAG` 的任务 | 🟢 | [desc.md](./finite-state-machines-based-path-following-collaborative-computing-strategy-for-emergency-uav-swarms/desc.md) |
| 110 | 🔣 | 🎛️ | 🌡️ | `RoboChart / RoboTool` | 设计-验证-实现工具链 | Formal design, verification and implementation of robotic controller software via RoboChart and RoboTool | 2024 | 从 RoboChart 设计自动生成可验证、可执行的机器人控制软件架构 | metamodel、`Sense-Execute-Actuate`、channels、timers、C++ API | module/platform/controller/machine + generated classes | `RoboTool` + Eclipse + `CSP/FDR` + Gazebo/ROS bridge | exploration task、高可信机器人控制软件 | 需求可抽成显式平台接口与层次状态机 | 🟢 | [desc.md](./formal-design-verification-and-implementation-of-robotic-controller-software-via-robochart-and-robotool/desc.md) |
| 111 | 📦 | 🎛️ | 🏭 | `Forklift Navigation FSM` | 工厂物流叉车导航 / planner-controller switching | Autonomous Forklift Navigation Inside a Cluttered Logistics Factory | 2024 | 用三态 `FSM` 协调 rotate/move/avoid 导航模式 | `Rotate/Move/Avoid`、corridor constraints、`A*`、`CLMPC` | road network + `FSM` + local planner + `CLMPC` | `ROS Gazebo` + `TwinswHeel facTHory` forklift + lidar/vision | 工厂物流叉车搬运 | 存在结构化 corridor、可用路网与障碍感知 | 🟢 | [desc.md](./autonomous-forklift-navigation-inside-a-cluttered-logistics-factory/desc.md) |
| 112 | 🕸️ | 🏭 | 🏭 | `Modular HRC Safety PN` | 人机协作任务级安全控制 / modular `Petri` application | Towards a Modular Human-Robot Safety Control System Using Petri Nets | 2024 | 用 `PN + SRI` 统一 human/robot `MAPE` safety loops 和协作任务门控 | task-based safety、`SRI`、decentralized `MAPE`、interaction modality、parallel loops | assembly task net + human loop + robot loop + `SRI` token schema | depth camera + adjustable robot parameters，原文无公开代码 | 工业装配 `HRC` 的任务级动态安全评估 | 任务需可分解成有限步骤，并能枚举 interaction/tool/component 风险因素 | 🟢 | [desc.md](./towards-a-modular-human-robot-safety-control-system-using-petri-nets/desc.md) |
| 113 | 🔌 | 🤝 | 🌐 | `Contract Automata / CARE + Uppaal` | 运行时形式分析 / contract middleware verification | Modelling, Verifying and Testing the Contract Automata Runtime Environment with Uppaal | 2024 | 把 `CARE` 中间件压成 stochastic timed automata 并验证 deadlock/orphan-message/termination | centralised/distributed actions、majoritarian/dictatorial choice、FIFO buffers、timeout | `CARE` Java runtime + `Uppaal` templates + buffer arrays + model-based tests | `CARE` + `CATLib/CATApp` + `Uppaal` + public models/logs | contract-based applications、service orchestration runtime | 服务需可写成有限 request/offer 契约，且运行时允许 wrapper/orchestrator | 🟢 | [desc.md](./modelling-verifying-and-testing-the-contract-automata-runtime-environment-with-uppaal/desc.md) |
| 114 | 🕸️ | 🎛️ | 🌡️ | `Distributed Petri Nets / DiNeROS` | ROS 建模验证工具链 / 分布式 Petri 网应用 | Distributed Petri Nets for Model-Driven Verifiable Robotic Applications in ROS | 2024 | 统一描述 ROS 结构、通信和工作流，并落到可验证/可执行的 Petri 网链路 | node nets、topics/services、signals、overflow/dead-node analysis | `SyM -> RTM -> PNM` model transformations | `DiNeROS` + `PNML` + `TINA` + `ROS` | 分布式 ROS 机器人应用、共享资源控制与工作流验证 | 系统结构和交互对象需可显式建模 | 🟢 | [desc.md](./distributed-petri-nets-for-model-driven-verifiable-robotic-applications-in-ros/desc.md) |
## 综述类论文总表

说明：

1. `对象类型` 与 `状态` 是 emoji 列；正式入账时单元格只写一个 emoji，不写中文说明。
2. survey 正式入账后，应继续把其引出的代表原始文献回填到下一节的追踪表。
3. 除非另有说明，本表正式入账后默认按 `年份升序` 排列。

| # | 综述主题 | 对象类型 | 标题 | 年份 | 覆盖主类 | 覆盖的形式主义 | 是否覆盖构造方式/基础设施 | 主要价值 | 状态 | 目录 |
|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | 二维自动机理论版图 | 🧱 | A Survey of Two-Dimensional Automata Theory | 1991 | 🧩 | `2D Turing Machines`、`2D Finite Automata`、`Marker Automata`、cellular types | 部分覆盖 | 把二维 tape 上的方向限制、alternation、封闭性与判定问题统一进一个谱系 | 🟢 | [survey.md](./survey-of-two-dimensional-automata-theory/survey.md) |
| 2 | 状态图模型检验路线 | 🛠️ | Model Checking of Statechart Models: Survey and Research Directions | 2004 | 🧩 🔣 | `Statecharts`、`STATEMATE`、`RSML`、`UML State Machine`、`HRM/CRSM` | 部分覆盖 | 讲清层次状态机验证中的 flattening、语义歧义与 traceability 问题 | 🟡 | [survey.md](./model-checking-of-statechart-models/survey.md) |
| 3 | 细胞自动机理论版图 | 🧱 | Theory of Cellular Automata: A Survey | 2005 | 🧩 | 同步 `CA`、reversible `CA`、number-conserving/linear `CA`、空间受限识别 `CA` | 部分覆盖 | 把可逆性、守恒量、动力学与语言识别四条理论主线压到一篇里 | 🟢 | [survey.md](./theory-of-cellular-automata-survey/survey.md) |
| 4 | Petri 网标准化与交换格式 | 🏗️ | PN Standardisation: A Survey | 2006 | 🕸️ 📦 | `P/T Nets`、`High-level Petri Nets`、`Symmetric Nets`、`PNML` | 是 | 直接覆盖标准、元模型、XML 承载与 API 实现 | 🟢 | [survey.md](./pn-standardisation-survey/survey.md) |
| 5 | 确定性自顶向下树自动机谱系 | 🧱 | Deterministic Top-Down Tree Automata: Past, Present, and Future | 2008 | 🧩 📦 | blind/sensing、ranked/unranked、`DTD`、`XML Schema`、`Relax NG` | 是 | 讲清 deterministic top-down tree automata 在 ranked/unranked/XML schema 三条线上的 expressive power 与静态分析边界 | 🟢 | [survey.md](./deterministic-top-down-tree-automata/survey.md) |
| 6 | 多带自动机表达力与判定性 | 🧱 | A Survey of Multi-Tape Automata | 2012 | 🧩 | synchronous/asynchronous、one-way/two-way、rewind-bounded、reversal-bounded 多带自动机 | 部分覆盖 | 把多带 automata 的同步、回退、反转与确定性差异压成统一闭包与可判定性版图 | 🟢 | [survey.md](./survey-of-multi-tape-automata/survey.md) |
| 7 | 时间自动机变体与工具生态 | 🧱 | A Survey of Timed Automata for the Development of Real-Time Systems | 2013 | ⏱️ | 经典、参数化、概率、代价、博弈等 `Timed Automata` 变体 | 是 | `80` 个变体、`40` 个工具、实现问题一体化盘点 | 🟢 | [survey.md](./survey-of-timed-automata-for-real-time-systems/survey.md) |
| 8 | 混成自动机与 CPS 验证 | 🧱 | Hybrid Automata for Formal Modeling and Verification of Cyber-Physical Systems | 2013 | 🌊 ⏱️ | 一般 `Hybrid Automata`、`Timed Automata`、`Initialized Rectangular`、`PCD` | 部分覆盖 | 讲清连续动力学引入后的判定边界与工具谱系 | 🟢 | [survey.md](./hybrid-automata-for-cps/survey.md) |
| 9 | 加权逻辑与加权自动机统一视角 | 🧱 | A Unifying Survey on Weighted Logics and Weighted Automata | 2018 | 🧩 | `Weighted Automata`、core weighted logic、words/ranked/unranked trees | 部分覆盖 | 把权值域、承载结构和抽象/具体语义三条轴统一起来，适合补 quantitative automata 本体 | 🟢 | [survey.md](./weighted-logics-and-weighted-automata-survey/survey.md) |
| 10 | UML 状态机形式化与自动验证 | 🛠️ | Formalizing UML State Machines for Automated Verification -- A Survey | 2023 | 🔣 📦 | `UML State Machine`、translation targets、direct operational semantics | 是 | `61` 篇工作双路线盘点，并审计工具长期可用性 | 🟢 | [survey.md](./formalizing-uml-state-machines-survey/survey.md) |

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
2. `Timed Automata + UPPAAL + IMITATOR` 这一条时间自动机基础与工具线；应用层已补工业协议、多机器人规划、`SCADA` 攻击检测与 `ROS` 通信验证，下一轮优先补工具教程与参数化变体。
3. `I/O Automata + TIOA + Interface/Contract Automata` 这一条接口组合与精化线；应用层已补 `web transactions`、`IoT accessor`、context-dependent service contracts 与 `CARE-Uppaal` runtime verification，下一轮优先补更纯的接口本体与早期代表文献。
4. `Hybrid Automata + 1993 origin paper + decidable subclasses` 这一条连续动力学主线；应用层已补 urban driving `NHA`、field robots、mobile robot action coordination 与 multi-robot coordination / `HyTech`，下一轮继续回补奠基和判定边界。
5. `Petri Nets + ISO/IEC 15909 + PNML + High-Level/Timed extensions` 这一条网模型标准与扩展线；应用层已补多机器人任务、持续任务 reward synthesis、open-path `AGV`、modular `HRC` safety、manufacturing-cell timed schedules 与 `DiNeROS`，下一轮仍优先标准化与高层网本体。
6. `SCXML + processors/runtime/tool support` 这一条可执行载体与运行时线。
7. `Tree Automata` 已补基础条目，下一轮继续沿 `Hedge Automata + XML schema validation` 回补结构化承载线。
8. `Weighted Automata` 已补 handbook 级本体条目，下一轮继续回补 `Schutzenberger + weighted logics + valuation monoid` 主线。
9. `Two-Dimensional / Cellular / Multi-Tape Automata` 已补基础代表条目，下一步回补更早奠基论文与典型判定边界。
10. `EFSM` 已补方法支撑型条目，下一轮应继续补更纯粹的定义/标准源，如 `SDL / Estelle / 测试主线`。
11. 上述每条主线都优先补“模型本体 + 标准/基础设施”条目；方法路线只作为辅证，不单独扩成主收录方向。
12. `CHARON / Polychrony / RSML-e / JGrafchart` 已补应用与工具桥接条目，下一轮可沿 `CHARON` 本体、`Signal/Polychrony` 工具线、`RSML-e` 工业案例、`JGrafchart` 导出/runtime 继续扩展。
13. `PLEXIL / MissionLab / XABSL / FlexBE / VisualHFSM / RoboSim / XRobots / SMACHA / RAFCON / YASMIN / RoboChart / SEAD / SCR / ARGO / LLFSM / DSD / Safety4.0 / AutoPlant-SMACH / MERLIN / rFSM / Asynchronous WMR FSM Controller / Binary Decomposition + FIPA HFSM / SMACC` 已补执行载体与机器人任务 DSL/应用条目，下一轮可沿 `CLARAty / RGCS / Remote toolbox`、`MissionLab CfgEdit / CDL`、`LLFSM generator / whiteboard variants`、`DSD GUI / sanity checks`、`SMACH / SMACC`、`ROSPlan / actionlib`、`rFSM patterns / OROCOS deployment`、`Stateflow embedded deployment`、`FIPA protocol verification`、`FlexBE standalone / ROS 2 port`、`VisualHFSM / JdeRobot deployment line`、`RoboSim code generation`、`RoboTool / RoboCalc`、`industrial HRC mode libraries`、`AutoPlant` 任务控制扩展线继续扩展。
14. `Pallet Manipulation HFSM / Industrial Mobile Manipulation Flow Control / LLFSM Walking Controller / HFSM Task Allocation / Educational Robotics FSM / ROSCo / Universal Mission Controller / Meal Assistance FSM / Power-Line Inspection Robot Crossing FSM / Forklift Navigation FSM / AnnieWAY CHSM / Exoskeleton Gait FSM / Underwater Swarm Pheromone FSM / Delivery Stair-Climbing State Machine / SmHPFC / SMACH + DMSL Decision-Augmented FSM / Hybrid FES Exoskeleton Dual-FSM / Waiter Motion Strategy FSM / Cotton Harvesting Visual-Servo FSM / Floor-Tiling FSM / Cardiac Rehabilitation Social Robot FSM / HVTL Multi-Task Maintenance Robot FSM / Procedure-Observer Surgical Statechart / FSM-HSVM Exoskeleton Recognizer / Excavation UML Statechart` 已补多批应用/教程条目，下一轮可沿 `RoboComp/RobEx` 组件网络、`SensorNet` 工位知识训练、`MiEditLLFSM` 建模器/运行时、`workload-aware HRC` 分配策略、`ROSCo` behavior library / `AR-tag` deployment、`MEA/MEE` mission-order verification / `Prolog` tool line、safe feeding supervisor / anomaly monitor、crossing protocol / operator-in-the-loop、driverless behavior law auditing、`CoP`-threshold exoskeleton variants、node-based marine swarm coordination、wheel-legged stair descent supervisors、`HOBBIT` profile adaptation / `DMSL` 规则块、hybrid gait fatigue managers、restaurant motion-profile schedulers、vision-servo cotton picking，以及 `probabilistic rehab supervisor`、`robotic excavation work-cycle libraries`、`surgical observer libraries`、`speed-adaptive exoskeleton recognizers`、`power-line maintenance task generalization` 和 construction tiling measurement/control 继续扩展。

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
| 2026-04-02 01:32:17 | 扩展机器人行为工程与仿真工具链条目 | 新增 5 篇 `desc.md` 条目，覆盖 `FlexBE`、`VisualHFSM`、`RoboChart` 定时语义、`RoboSim`、`RoboChart/RoboTool` 设计到实现链路，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 10:37:53 | 扩展应用型状态机执行载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `ARGO/Cortex`、`Embodied Agent / LLFSM + Whiteboard`、`DSD`、`Safety4.0 Dynamic FSM`、`AutoPlant/SMACH mission supervisor`；其中空间机器人条目的原始 PDF 链接已失效，本轮通过归档快照补齐原文后同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 11:42:41 | 继续扩展应用型状态机执行载体条目 | 新增 5 篇 `desc.md` 条目，覆盖 `MERLIN`、`rFSM Statecharts`、`Asynchronous WMR FSM Controller`、`Embodied Agent / Binary Decomposition + FIPA HFSM`、`SMACC Parcel Handling Supervisor`；本轮均重新联网检索并补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，随后同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 12:28:59 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网筛查 `18+` 个候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Eye-Hand FSM HRC`、`Hierarchical FSM Driving Decision Framework`、`FSM-CLF-CBF Lane Change Controller`、`Spacer Installation Harel Statechart`、`EFSMSG`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表 |
| 2026-04-02 13:26:39 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网检索并筛查应用类状态机候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Pallet Manipulation HFSM`、`Industrial Mobile Manipulation Flow Control`、`Educational Robotics FSM`、`LLFSM Walking Controller`、`HFSM Task Allocation`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 14:40:07 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网检索并筛查应用类状态机候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Power-Line Inspection Robot Crossing FSM`、`Universal Mission Controller / MEA`、`ROSCo / Home-Robot HFSM`、`Meal Assistance FSM`、`Forklift Navigation FSM`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 15:28:48 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网检索并筛查应用类状态机候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `AnnieWAY CHSM`、`Exoskeleton Gait FSM`、`Underwater Swarm Pheromone FSM`、`Delivery Stair-Climbing State Machine`、`SmHPFC`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 16:40:38 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网检索并筛查应用类状态机候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `SMACH + DMSL Decision-Augmented FSM`、`Hybrid FES Exoskeleton Dual-FSM`、`Waiter Motion Strategy FSM`、`Cotton Harvesting Visual-Servo FSM`、`Floor-Tiling FSM`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 17:32:50 | 继续扩展应用型状态机执行载体条目 | 本轮重新联网检索并筛查应用类状态机候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Cardiac Rehabilitation Social Robot FSM`、`Robotic Excavation UML Statechart Supervisor`、`HVTL Multi-Task Maintenance Robot FSM`、`Procedure-Observer Surgical Statechart`、`FSM-HSVM Exoskeleton Recognizer`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表与下一轮扩展方向 |
| 2026-04-02 18:53:53 | 建立状态机族主蓝本演化树并拆分 DSL 主类 | 基于已收录普通条目与 survey 条目梳理“状态机族模型 / profile / DSL / 标准语言”的主蓝本演化树；把具有明确模型本体的 `DSL` 从原 `📦` 类中独立为 `🔣`，并同步回填主类统计、正式总表重分类与 survey 覆盖主类口径 |
| 2026-04-02 20:35:59 | 继续扩展主干形式主义应用条目 | 本轮重新联网筛查接口/组合、时间/混成与 `Petri` 并发主干候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Commercial Field Bus Timed Automata`、`FMCA`、`CARE Runtime`、`Hybrid Field Robot Teams`、`Multi-Robot Task Petri Nets`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表 |
| 2026-04-02 21:24:12 | 继续扩展主干形式主义应用条目 | 本轮重新联网筛查接口/组合、时间/混成与 `Petri` 并发主干候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Web-Service Transactions Interface`、`IoT Interface Theory`、`Timed Multi-Robot Planning`、`Hybrid Action Coordination`、`Persistent-Task GSPNR`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通论文总表、待补方向与更新日志 |
| 2026-04-02 22:48:58 | 强化 tree 同步规则并回填最近两次提交的演化关系 | 在 [GUIDE.md](./GUIDE.md) 中新增“更新正式文献时必须同步检查并更新状态机族演化树及挂接说明”的硬约束；同时回看最近两次提交新增条目，把 `Transaction-Aware Web Service Interface`、`IoT Interface Theory`、`FMCA`、`MOPN / GSPN for Multi-Robot Tasks` 与 `GSPNR / MRA for Persistent Multi-Robot Tasks` 整合进主蓝本树，并把 `CARE Runtime`、`Timed Automata`、`Hybrid Automata` 应用条目明确记为主干侧证而非独立树节点 |
| 2026-04-02 23:25:41 | 继续扩展主干形式主义应用条目 | 本轮重新联网筛查 `15+` 个接口/组合、时间/混成与 `Petri` 并发候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Urban Driving NHA`、`SCADA Timed Automata`、`Open-Path AGV CPN`、`Modular HRC Safety PN` 与 `CARE-Uppaal Runtime Verification`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、关键词簇、普通总表、待补方向、挂接说明与更新日志 |
| 2026-04-02 23:52:35 | 结合最近提交回填 NHA 到演化树 | 回看最新一次提交新增的 5 篇接口/组合、时间/混成与 `Petri` 应用条目后，确认 `Urban Driving NHA` 已给出可稳定提炼的 `Nested Hybrid Automata` 结构定义，因此把 `Nested Hybrid Automata (2007，文库代表条目)` 挂到 `Hybrid Automata` 主干；其余 `SCADA Timed Automata`、`Open-Path AGV CPN`、`Modular HRC Safety PN` 与 `CARE-Uppaal Runtime Verification` 继续保留为主干应用侧证，并同步整理演化树文本排版 |
| 2026-04-03 00:34:11 | 继续扩展主干形式主义应用条目 | 本轮重新联网筛查 `15+` 个接口/组合、时间/混成与 `Petri` 并发候选后，正式新增 5 篇 `desc.md` 条目，覆盖 `Context-Dependent Service Contracts`、`ROS Timed Automata`、`Hybrid Multi-Robot Coordination`、`Manufacturing-Cell Timed Petri Schedules` 与 `DiNeROS Distributed Petri Nets`；全部补齐 `paper.pdf`、`paper_content.txt`、`bibtex.bib` 与 `desc.md`，并同步回填统计、普通论文总表、关键词簇、演化树挂接说明与更新日志 |

## 失败与阻塞记录

- 当前无正式失败记录。
