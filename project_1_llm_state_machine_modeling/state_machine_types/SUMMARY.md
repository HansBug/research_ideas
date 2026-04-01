# Project 1 State Machine Types Summary

本文件是 `project_1_llm_state_machine_modeling/state_machine_types/` 的总账，用于记录当前已经正式入账的状态机类型论文、综述类论文、统一分类口径、关键词簇和更新日志。

推荐使用顺序如下：

1. 先读 [README.md](./README.md)，理解本论文集的定位与边界。
2. 再读 [GUIDE.md](./GUIDE.md)，确认检索、筛选、回填流程。
3. 若任务涉及普通条目，再读 [DESC_GUIDE.md](./DESC_GUIDE.md)。
4. 若任务涉及综述条目，再读 [SURVEY_GUIDE.md](./SURVEY_GUIDE.md)。
5. 最后使用本文件查看统计、双表总账、关键词簇和待补方向。

## 当前收录统计

- 已收录普通类型论文：**29** 篇
- 已收录综述类论文：**10** 篇
- 本轮新增论文：**5** 篇
- 已完成 `desc.md`：**29** 篇
- 已完成 `survey.md`：**10** 篇
- `⏳ 尚未提取`：**0** 篇
- 本轮工作：新增 5 篇应用/专用载体条目，覆盖 `SyncCharts / SFC / Stateflow / StateGraph / StateGraph2`

## 形式主义主类口径

右侧数量统计当前正式入账条目中涉及该主类的次数：普通论文按 `主类` 计数，综述论文按 `覆盖主类` 中出现的每个 emoji 分别计数。

| Emoji | 主类 | 范围 | 数量 |
|---|---|---|---:|
| 🧩 | 经典离散状态机 | `FSM`、`EFSM`、`Statechart`、`UML State Machine`、`SCXML`、`Tree Automata`、`Multi-Tape Automata`、`Two-Dimensional Automata`、`Cellular Automata`、`Weighted Automata` 等 | 17 |
| ⏱️ | 时间/时钟自动机 | `Timed Automata`、`Timed Statecharts`、`TIOA` 等 | 4 |
| 🌊 | 混成/随机扩展 | `Hybrid Automata`、概率/随机自动机、随机混成扩展等 | 2 |
| 🕸️ | Petri 网与并发网模型 | `P/T Net`、`Colored Petri Net`、`Timed Petri Net`、高层网等 | 5 |
| 🔌 | 接口/组合/契约模型 | `I/O Automata`、`Interface Automata`、`Contract Automata`、组合行为模型等 | 4 |
| 📦 | 标准、交换格式与执行载体 | `SCXML`、`PNML`、`UML/XMI`、专用 DSL、元模型、交换标准等 | 11 |

## 描述客体口径

右侧数量统计当前普通论文总表中的 `客体` 条目总数。

| Emoji | 描述客体 | 含义 | 数量 |
|---|---|---|---:|
| 📝 | 序列 / 语言对象 | 主要描述字符串、事件序列、trace、多串关系等离散序列对象 | 3 |
| 🌳 | 树 / 文档对象 | 主要描述树结构、XML 文档、层次内容或其他树形对象 | 1 |
| 🖼️ | 网格 / 图案对象 | 主要描述二维 tape、图片、网格或格点对象 | 2 |
| 🎛️ | 控制 / 反应式逻辑 | 主要描述控制器、反应式行为、事件驱动控制逻辑 | 13 |
| 🤝 | 接口 / 交互契约 | 主要描述协议、组件交互、会话、接口或契约对象 | 5 |
| 🏭 | 并发过程 / 资源流 | 主要描述并发过程、工作流、token/资源流网络 | 4 |
| 🌡️ | 物理 / 混成对象 | 主要描述物理装置、连续动力学对象或混成/CPS 对象 | 1 |

## 所属领域口径

右侧数量统计当前普通论文总表中的 `领域` 条目总数。

| Emoji | 所属领域 | 含义 | 数量 |
|---|---|---|---:|
| 🧮 | 形式语言与自动机理论 | 主要是 automata theory、formal language、语义与判定性研究 | 5 |
| 💻 | 软件建模与程序行为 | 主要面向软件状态、程序行为、反应式软件或模型驱动开发 | 6 |
| 📄 | 文档与数据交换 | 主要面向 XML、schema、文档结构与数据交换 | 0 |
| ⏱️ | 实时与嵌入式系统 | 主要面向实时、调度、时序约束和嵌入式执行 | 4 |
| 🏭 | 工业控制与自动化 | 主要面向控制工程、自动化系统和工业逻辑 | 3 |
| 🌐 | 协议 / 分布式 / 交互系统 | 主要面向通信协议、服务交互、接口组合与分布式行为 | 5 |
| 🌡️ | CPS / 物理系统建模 | 主要面向连续物理过程、CPS、混成系统与物理仿真 | 6 |

## 状态口径

右侧数量统计当前普通论文总表与综述论文总表中的状态条目总数。

| Emoji | 含义 | 数量 |
|---|---|---:|
| 🟢 | 直接可用 | 38 |
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
- 对 `SyncCharts / SFC / Stateflow / StateGraph / StateGraph2 / Modelica / Ptolemy` 这类专用模型或执行载体，若能稳定回填“对象、语义、承载方式、工具入口”，可正式入账。

## 检索关键词簇

### 当前推荐关键词簇

- `finite state machine / extended finite state machine / statechart / UML state machine / SCXML`
- `tree automata / top-down tree automata / hedge automata / XML schema automata`
- `multi-tape automata / two-dimensional automata / cellular automata / weighted automata`
- `timed automata / timed statecharts / timed transition systems / timed I-O automata`
- `hybrid automata / probabilistic automata / stochastic automata / stochastic hybrid automata`
- `petri net / colored petri net / timed petri net / PNML / hierarchical petri net`
- `interface automata / I-O automata / contract automata / reactive modules`
- `communicating finite-state machine / workflow net / synccharts / stateflow / sequential function chart / stategraph / stategraph2`
- `survey / review / tutorial / taxonomy / mapping study` + 上述形式主义关键词

### 已观察到的高命中特征

- `survey/review/tutorial` 与具体家族词绑定时命中率高，例如 `timed automata survey`、`formalizing UML state machines survey`
- 对理论 automata 家族，`family term + survey` 往往能直接命中作者预印本或机构开放仓储，适合先补 `🧱` 再回溯原始文献
- `standardisation / markup language / PNML / formalizing / tool support` 这类“形式主义 + 基础设施”词簇很适合挖标准化与工具生态论文
- `recommendation / specification / formal / xmi / schema` 与形式主义名组合时，适合命中 `UML/SCXML` 这类标准与载体文献
- `cyber-physical systems` 与 `hybrid automata` 联合检索时，更容易命中“建模与验证框架综述”而非单一算法论文
- 精确形式主义名与框架名组合时命中率高，例如 `workflow net`、`synccharts esterel`、`stateflow semantics`、`stategraph modelica`

### 已观察到的低命中特征

- 只搜 `state machine survey` 容易漂移到工作流、AI agent、软件工程流程或分类器论文
- 只搜 `verification` 容易命中算法优化或应用案例，而不是形式主义本体综述
- 只搜 `UML tool` 容易落到商业建模工具宣传页，形式语义与验证基础不足
- 只搜 `workflow state machine` 或 `modelica control` 容易漂到厂商教程、业务流程平台或一般应用案例
- 只搜 `reactive state machine` 容易漂到泛软件工程或教学材料，而不是具体载体论文

### 检索倾向调整

- 继续以“家族词 + survey/review/tutorial”作为第一轮入口，再由 survey 反推出原始文献、标准和工具线
- 对离散 automata 理论支线，优先补“模型谱系 + 经典判定边界 + 构造载体”三类材料，不把纯形式语言技巧论文直接当扩库主线
- 后续普通条目优先补“定义/语义 + 标准/交换格式 + 工具链”三类材料，不把应用论文或纯方法论文当扩库主线
- 对 `Petri Nets` 一类基础设施成熟方向，优先补 `standard / markup language / metamodel / API` 线，而不是只补理论定义
- `SCXML`、`Interface/Contract Automata` 已补基础条目，下一轮应继续补执行器/工具线与更早代表文献
- 方法路线条目只在能够反向支撑某一形式主义的能力边界或基础设施条件时再跟进
- 对应用/专用模型，优先用“精确形式主义名 + 框架名 + pdf/tech report/proceedings”检索，避免被泛领域关键词带偏
- `SyncCharts / SFC / Stateflow / StateGraph` 这类工程载体更适合直接搜准确名称，而不适合先走宽泛的 `state machine` 关键词

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
| 13 | 🕸️ | 🏭 | 💻 | `WorkFlow net (WF-net)` | 领域特化 | The Application of Petri Nets to Workflow Management | 1998 | 把单 case 工作流生命周期压成可分析流程网 | 单入口/单出口、soundness、dead task、routing patterns | places/transitions/marking + workflow routing blocks | Petri 网分析工具线强，workflow analyzer 明确 | 审批流、业务流程、任务路由 | 需求核心是流程路由正确性与终止性 | 🟢 | [desc.md](./application-of-petri-nets-to-workflow-management/desc.md) |
| 14 | 🔌 | 🤝 | 🌐 | `Interface Automata` | 模型提出 | Interface Automata | 2001 | 检查接口兼容与替换性 | compatibility、illegal states、alternating simulation | 输入/输出接口自动机 | 组合与精化语义成熟，无标准格式 | 组件接口匹配、服务组合 | 关注假设/保证式交互 | 🟢 | [desc.md](./interface-automata/desc.md) |
| 15 | 📦 | 🎛️ | 🏭 | `Sequential Function Charts (SFC)` | 工业语义 | A Unifying Semantics for Sequential Function Charts | 2004 | 为 `IEC 61131-3 SFC` 提供统一可参数化 cycle semantics | steps、action qualifiers、parallelism、history、timed extension | steps/transitions + action blocks + priority orders | `PLC` 工具链和 `IEC` 标准明确 | `PLC` 顺控、工业自动化 | 需求可分解为步骤/守卫/动作并按扫描周期执行 | 🟢 | [desc.md](./a-unifying-semantics-for-sequential-function-charts/desc.md) |
| 16 | 📦 | 🎛️ | 🏭 | `StateGraph` | 工具/库 | StateGraph - A Modelica Library for Hierarchical State Machines | 2005 | 在 Modelica 中提供层次状态机库 | `fire/newActive` 方程、parallel/alternative、composite step | steps/transitions/parallel/composite + Modelica equations | `Modelica.StateGraph` + logical blocks | 监督控制、物理过程联调 | 需求需与 Modelica 模型协同并接受单赋值约束 | 🟢 | [desc.md](./stategraph-a-modelica-library-for-hierarchical-state-machines/desc.md) |
| 17 | ⏱️ | 🤝 | ⏱️ | `Timed I/O Automata` | 理论专著 | The Theory of Timed I/O Automata | 2005 | 组合实时组件并比较实现关系 | trajectories、receptiveness、simulation | 动作接口 + 时间轨迹 | 理论框架成熟，无标准格式 | 实时组件系统 | 需求同时包含接口与时间演化 | 🟢 | [desc.md](./the-theory-of-timed-input-output-automata/desc.md) |
| 18 | 🕸️ | 🏭 | 💻 | `Coloured Petri Nets` | 教程讲义 | Coloured Petri Nets | 2005 | 在 Petri 网中引入 typed token 与数据 | colour sets、simulation、state space | 网结构 + 颜色集 + 弧表达式 | 工具生态成熟，交换标准较弱 | 协议与数据驱动并发系统 | 并发 + 显式数据对象 | 🟢 | [desc.md](./coloured-petri-nets/desc.md) |
| 19 | 📦 | 🎛️ | 🌡️ | `Stateflow` | 形式语义 | An Operational Semantics for Stateflow | 2007 | 把工业 `Stateflow` chart 形式化为顺序化图形状态机语义 | junction、local events、`12 o'clock` ordering、安全子集 | states/junctions/transitions + linearized SOS | `Matlab/Simulink/Stateflow` 生态成熟 | 嵌入式控制器、混成系统离散部分 | 需求最终落到 `Stateflow` 工具链且接受工具优先级 | 🟢 | [desc.md](./an-operational-semantics-for-stateflow/desc.md) |
| 20 | 🕸️ | 🏭 | ⏱️ | `Time Petri Nets` | 教程讲义 | Time Petri Nets Part II: State Class based methods | 2008 | 在并发网上加入时间区间 | 静态区间、state class graph | P/T 网 + 变迁时间区间 | TINA 线成熟，标准格式较弱 | 实时并发流程与调度 | 并发资源流 + 时间窗口 | 🟢 | [desc.md](./time-petri-nets/desc.md) |
| 21 | 🧩 | 🌳 | 🧮 | `Tree Automata` | 教程专著 | Tree Automata Techniques and Applications | 2008 | 识别树、项与层次结构语言 | bottom-up、top-down、determinization、decision problems | ranked alphabet + 状态 + 树重写规则 | 理论与算法成熟，XML/hedge 在线路上衔接强 | AST、term rewriting、schema-like structural validation | 输入需显式树/项结构而非平坦事件串 | 🟢 | [desc.md](./tree-automata-techniques-and-applications/desc.md) |
| 22 | 📦 | 🎛️ | 🏭 | `ModeGraph` | 工具/库 | ModeGraph - A Modelica Library for Embedded Control Based on Mode-Automata | 2008 | 在 Modelica 中实现安全层次状态机与 mode-automata 执行 | single-assignment、delayed transition、preemption、parallel | `Step/Transition/Composite/Parallel` + mode equations | Modelica 工具链明确，需语言扩展，无独立交换标准 | 嵌入式控制、混合控制、工业逻辑 | 需求需安全模式切换并与 Modelica 模型协同 | 🟢 | [desc.md](./modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md) |
| 23 | 🧩 | 📝 | 🧮 | `Weighted Automata` | 手册章节 | Weighted Automata Algorithms | 2009 | 在自动机/转导器上附加 semiring 权值 | semiring、path weight、determinization、minimization | 图结构 + label + weight + semiring 运算 | 算法体系成熟，但无统一交换标准 | 概率/代价/评分型字符串与转导建模 | 需求需保留有限状态骨架且每条路径带可组合权值 | 🟢 | [desc.md](./weighted-automata-algorithms/desc.md) |
| 24 | 📦 | 🎛️ | 🌡️ | `Ptolemy II FSM / Modal Models` | 工具教程 | Finite State Machines and Modal Models in Ptolemy II | 2009 | 用状态机控制 refinement 切换并支撑异构执行 | guard/output/set action、mode refinement、microstep、local time | `FSMActor / ModalModel` + `MoML` + compatible directors | Ptolemy II 图形/Java/MoML 生态完整 | 异构嵌入式系统、CPS mode switching | 不同模式需挂不同 refinement 与执行域 | 🟢 | [desc.md](./finite-state-machines-and-modal-models-in-ptolemy-ii/desc.md) |
| 25 | 📦 | 🎛️ | 🌡️ | `Modelica_StateGraph2` | 形式主义 / 工具库 | A New Formalism for Modeling of Reactive and Hybrid Systems | 2009 | 把 Modelica 状态机扩成安全层次并行 generalized steps | generalized steps、suspend/resume、delay、`NuSMV` verification | `\Gamma = \langle V_c,G,T,g_I \rangle` + ports + interpretation algorithm | `Modelica_StateGraph2` + `NuSMV` | reactive/hybrid systems | 需求含模式切换并需与物理模型联仿 | 🟢 | [desc.md](./a-new-formalism-for-modeling-of-reactive-and-hybrid-systems/desc.md) |
| 26 | 📦 | 🎛️ | 🌡️ | `Modelica State Machines` | 语言扩展 | State Machines in Modelica | 2012 | 把状态机纳入 Modelica 语言核心 | 13 方程语义、immediate/delayed、reset/synchronize | Modelica blocks + transition equations + clock | Modelica 3.3 语言级支持明确 | 物理系统中的控制逻辑、嵌入式控制 | 状态逻辑需与同 clock 的 Modelica 模型原生集成 | 🟢 | [desc.md](./state-machines-in-modelica/desc.md) |
| 27 | 🔌 | 🤝 | 🌐 | `Contract Automata` | 模型提出 | Automata for Analysing Service Contracts | 2014 | 分析多方契约匹配与责任 | agreement、weak agreement、liability | 向量动作自动机 + 组合 | 分析方法明确，生态偏研究型 | 服务编排、契约组合 | 多方 request/offer 关系清晰 | 🟢 | [desc.md](./contract-automata/desc.md) |
| 28 | 🧩 | 🎛️ | 💻 | `SCXML` | 标准规范 | State Chart XML (SCXML): State Machine Notation for Control Abstraction | 2015 | 提供可执行层次状态机 XML 载体 | `state/parallel/history/datamodel/invoke` | SCXML XML 文档 | W3C 规范、Schema、测试套件 | 事件驱动流程与互操作 | 需要标准文本载体 | 🟢 | [desc.md](./scxml-state-machine-notation-for-control-abstraction/desc.md) |
| 29 | 🧩 | 🎛️ | 💻 | `UML State Machine` | 标准规范 | OMG Unified Modeling Language (OMG UML), Version 2.5.1 | 2017 | 标准化行为/协议状态机元模型 | regions、pseudostates、XMI | 图形建模 + metamodel + XMI | OMG 标准和工具生态成熟 | MDE、跨工具交换 | 需要与 UML 语境集成 | 🟢 | [desc.md](./uml-251-specification/desc.md) |

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
| 11 | 1996 | 状态图模型检验路线 | `STATEMATE` 语义 | Harel, Naamad, `The STATEMATE Semantics of Statecharts` | 原始语义口径，对 priority/history/inter-level transition 很关键 | 优先补单篇 `desc.md` | 🔴 |
| 12 | 1997 | UML 状态机形式化与自动验证 | `UML` 标准起点 | `OMG UML 1.1 specification` | 形式化工作共同的时间边界和标准起点 | 先补标准条目 | 🟡 |
| 13 | 1998 | 混成自动机与 CPS 验证 | 判定边界 | Henzinger et al., `What's Decidable About Hybrid Automata?` | 混成自动机可判定子类和边界线的关键入口 | 优先补单篇 `desc.md` | 🔴 |
| 14 | 1999 | UML 状态机形式化与自动验证 | UML + model checking | Lilius, Paltor, `Formalising UML State Machines for Model Checking` | UML 形式化主线的重要早期节点 | 优先补单篇 `desc.md` | 🔴 |
| 15 | 1999 | 确定性自顶向下树自动机谱系 | `Hedge Automata` / XML | Murata, `Hedge Automata: A Formal Model for XML Schemata` | 连接 unranked tree automata 与 XML schema 生态的关键节点 | 优先补单篇 `desc.md` | 🔴 |
| 16 | 2000 | 状态图模型检验路线 | 保层次验证 | Alur et al., `Efficient Reachability Analysis of Hierarchic Reactive Machines` | 代表避免完全 flatten 的关键技术路线 | 先找原文并评估是否入库为 `desc.md` | 🟡 |
| 17 | 2004 | Petri 网标准化与交换格式 | `Petri Net` 标准 Part 1 | `ISO/IEC 15909-1` | 标准化术语、语义和图形记法的核心入口 | 优先补标准条目 | 🔴 |
| 18 | 2005 | Petri 网标准化与交换格式 | `PNML` / Part 2 概念线 | Ekkart Kindler, `The Petri Net Markup Language and ISO/IEC 15909-2` | 补足 `PNML` 的核心概念、状态和未来方向 | 优先补单篇 `desc.md` | 🔴 |
| 19 | 2006 | Petri 网标准化与交换格式 | High-level Petri Nets | Jensen, Rozenberg (eds.), `High-Level Petri Nets` | 回补高层网本体与标准化对象之间的理论连接 | 优先补单篇 `desc.md` | 🟠 |
| 20 | 2007 | 加权逻辑与加权自动机统一视角 | automata-logic 等价 | Droste, Gastin, `Weighted Automata and Weighted Logics` | 词上加权自动机与逻辑等价的标准入口 | 优先补单篇 `desc.md` | 🔴 |
| 21 | 2009 | 时间自动机变体与工具生态 | 参数化时间自动机 | Etienne Andre, `IMITATOR` tool line | 连接参数综合与需求到模型自动化 | 先补工具/方法条目 | 🟠 |
| 22 | 2011 | 时间自动机变体与工具生态 | 主流工具线 | Behrmann et al., `A Tutorial on UPPAAL` | 当前最值得优先追踪的时间自动机工具主线 | 优先补工具条目 | 🔴 |
| 23 | 2012 | 加权逻辑与加权自动机统一视角 | valuation monoid 语义 | Droste, Meinecke, `Weighted Automata and Regular Expressions over Valuation Monoids` | 把平均值、折扣和等非半环语义纳入统一权值模型 | 优先补单篇 `desc.md` | 🟠 |
| 24 | 2013 | UML 状态机形式化与自动验证 | 直接操作语义 | Liu et al., `USMMC` / corresponding semantics paper | 代表较完整的 UML 直接语义与验证路线 | 优先补单篇 `desc.md` | 🟠 |
| 25 | 2021 | UML 状态机形式化与自动验证 | 现代工具线 | Jouault et al., `AnimUML` | 代表仍在维护、可实际试用的现代 UML 验证工具 | 先补工具条目 | 🟠 |

## 待优先补入方向

1. `Harel Statecharts -> STATEMATE semantics -> UML profile` 这一条层次状态机语义细化线。
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
12. `SyncCharts / SFC / Stateflow / Modelica carriers` 已补第二批应用/专用载体条目，下一轮可沿 `Argos / Safe State Machines / JGrafchart / Simulink tool semantics / PLC tool semantics` 继续扩展。

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

## 失败与阻塞记录

- 当前无正式失败记录。
