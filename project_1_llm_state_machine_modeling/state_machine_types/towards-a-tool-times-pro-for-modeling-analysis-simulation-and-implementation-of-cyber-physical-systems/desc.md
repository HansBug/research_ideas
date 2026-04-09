# TIMES-Pro：面向 CPS 建模、分析、仿真与实现的工具 / Towards a Tool: TIMES-Pro for Modeling, Analysis, Simulation and Implementation of Cyber-Physical Systems

## 基本信息

- 标题：Towards a Tool: TIMES-Pro for Modeling, Analysis, Simulation and Implementation of Cyber-Physical Systems
- 中文标题：TIMES-Pro：面向 CPS 建模、分析、仿真与实现的工具
- 作者：Jakaria Abdullah，Gaoyang Dai，Nan Guan，Morteza Mohaqeqi，Wang Yi
- 发表：*Models, Algorithms, Logics and Tools*，pp. 623-639，2017
- DOI：`10.1007/978-3-319-63121-9_31`
- 链接：https://doi.org/10.1007/978-3-319-63121-9_31
- 形式主义：`DRT / SDRT / TIMES-Pro`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 论文角色：基于 `DRT/SDRT` 的 CPS 建模、时序分析、仿真与 Ada 部署工具
- 工具/实现获取方式：原文详细介绍了 `TIMES-Pro` 的 editor、simulator、analysis engine 与 code generator，但未给公开仓库或下载地址。
- 标准/格式获取方式：核心承载是 `DRT/SDRT` task-set 模型、工具内 XML 存取、Java GUI、Python `libdrt` 分析脚本与 Ada 代码生成；不是中立行业交换标准。

## 简报

这篇论文的关键价值，不是再提出一个新的 timed-automata 变体，而是围绕 `DRT/SDRT` 任务图语言搭出一整条 CPS 设计工具链。`TIMES-Pro` 试图在“表达力”和“可分析性”之间折中：离散控制器用 `DRT/SDRT`，连续物理部件通过谓词抽象和近似任务模型接入，再把建模、调度分析、可视仿真和 Ada 代码生成放到同一个环境里。

- 形式主义定位：以 `DRT/SDRT` 为核心的 CPS 建模与时序分析基础设施。
- 构造方式简述：离散任务先建成带执行时间、deadline 和最小释放间隔的有向图，再用同步动作扩展成 `SDRT`，最后接入分析器、仿真器和 Ada 代码生成器。
- 基础设施与场景简述：依托 Java GUI、XML 存储、Python `libdrt`、可视仿真器和 Ada generator，服务 timing analysis、co-simulation 与嵌入式部署。

```text
DRT / SDRT task set -> XML model + editor -> timing analysis / simulation -> Ada code generation -> real-time deployment
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. `Digraph Real-Time (DRT)` 任务模型。
2. 带同步动作的 `Synchronous Digraph Real-Time (SDRT)` 扩展。
3. 由软件、硬件和物理环境组件构成的 `CPS` 系统模型。
4. timing analysis、simulation 与 Ada code generation。
5. 编辑器、分析引擎、仿真器和代码生成器组成的 `TIMES-Pro` 工具架构。

### 核心抽象

论文直接给出 `DRT` 任务是一个带标签有向图，可压成：

$$
G(T) = (V,E,e,d,p)
$$

上式中的符号逐项解释如下：

1. `V` 是任务 `T` 的顶点集合，每个顶点对应一种可释放的实时作业类型。
2. `E` 是有向边集合，表示作业释放的先后关系。
3. `e:V \to \mathbb N_{>0}` 给出顶点的 worst-case execution time。
4. `d:V \to \mathbb N_{>0}` 给出相对 deadline。
5. `p:E \to \mathbb N_{>0}` 给出边上的最小作业释放间隔。

系统级任务集则是：

$$
\tau = \{T_1,\ldots,T_N\}
$$

上式中的符号逐项解释如下：

1. `T_1,\ldots,T_N` 是系统中的 `N` 个 `DRT` 任务。
2. 论文明确用这一记号表示任务集合。

`SDRT` 在 `DRT` 之上增加同步动作，可保守写成：

$$
G_s(T) = (V,E,e,d,p,a)
$$

上式中的符号逐项解释如下：

1. `a:E \to Act_\epsilon` 给出边上的同步动作标签。
2. `Act_\epsilon` 表示普通动作与“无同步”标记共同构成的动作域。
3. 其余符号与 `DRT` 相同。

### 一个最小例子与通俗解释

论文的 `SDRT` 例子非常直观：

1. 两个任务 `T_1` 和 `T_2` 都有若干顶点表示作业。
2. `T_1` 的某条边带 `s2?`，`T_2` 的某条边带 `s2!`。
3. 两个任务各自满足最小释放间隔后，只有当这一对动作都准备好时，同步作业才会一起释放。
4. 如果某一边尚未满足时序条件，另一边即使已准备好也会被阻塞等待。

通俗地说，`DRT` 像“带时间标签的任务流程图”，而 `SDRT` 则像“允许在作业释放瞬间做 rendezvous 的任务流程图”。

### 运行 / 接受 / 转移语义

论文明确把同步动作解释为 release-time rendezvous。这个条件可写成：

$$
a(u,v)=a(u',v')=s \Rightarrow r(u,v)=r(u',v')
$$

上式中的符号逐项解释如下：

1. `(u,v)` 与 `(u',v')` 是两个不同任务上的边。
2. `a(u,v)` 与 `a(u',v')` 是这两条边上的同步动作标签。
3. `s` 是二者共享的同步动作。
4. `r(u,v)` 与 `r(u',v')` 表示对应目标作业的释放时刻。
5. 该式表达论文中的同步语义：带同一同步动作的作业应在同一时刻释放。

系统模型则可压成：

$$
S = \{C_1,C_2,\ldots,C_N\}
$$

上式中的符号逐项解释如下：

1. `C_1,\ldots,C_N` 是系统中的软件、硬件或环境组件。
2. 每个组件内部由 `SDRT` 任务描述。
3. 组件之间通过同步动作粘合。

### 语义边界

1. `TIMES-Pro` 主体不是一般 timed automata，而是任务释放图及其调度分析。
2. 连续物理部分并不直接按通用混成自动机求解，而是通过谓词抽象和 `DRT` 近似接入。
3. 代码生成只实现 `DRT/SDRT` 行为的一个子集，并依赖 Ada 运行时系统。
4. 工具更强调 schedulability、response time、simulation 与 deployment，而不是广义时序逻辑模型检查。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| `DRT` 图骨架 | `$G(T) = (V,E,e,d,p)$` | 一个任务被表示为带执行时间、deadline 和最小间隔的有向图。 |
| 任务集 | `$\tau = \{T_1,\ldots,T_N\}$` | 整个系统由多个任务组成。 |
| `SDRT` 扩展 | `$G_s(T) = (V,E,e,d,p,a)$` | 同步任务在 `DRT` 上增加动作标签。 |
| 同步释放条件 | `$a(u,v)=a(u',v')=s \Rightarrow r(u,v)=r(u',v')$` | 共享动作的作业在 release 时刻同步。 |
| 系统模型 | `$S = \{C_1,\ldots,C_N\}$` | `TIMES-Pro` 面向的是组件化 CPS 设计。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 中等支持 | 核心对象是任务图和作业类型，而非传统状态机状态。 |
| 事件 / 触发 | 中等到强 | 作业释放与同步动作是核心触发机制。 |
| 守卫 / 数据 | 弱支持 | 主线是时序与同步，不是富数据状态机。 |
| 层次 | 弱支持 | 论文未强调层次状态结构。 |
| 并发 / 同步 | 强支持 | 多任务并行与 rendezvous-style release 是 `SDRT` 重点。 |
| 时间约束 | 很强 | `WCET`、deadline、inter-release separation 与 schedulability 分析是核心。 |
| 连续动态 / 随机性 | 中等支持 | 连续部分通过抽象接入，但不是通用连续动力学前端。 |
| 可执行 / 可验证性 | 很强 | editor、simulator、analysis engine 与 Ada generation 全部落地。 |

### 形式化问题与性质

1. 它展示了一条不同于 `timed automata` 的工程路线：把时序控制问题压成任务图，而不是先压成位置-时钟图。
2. `SDRT` 的同步语义与 Ada rendezvous 的映射，是这条工具链最有工程味的一点。
3. 对文库而言，它补的是“调度图 / 同步任务图”这条方法-基础设施交界线。

## 构造方式与承载格式

### 建模入口

原文明确给出：

1. `DRT` 任务图编辑。
2. `SDRT` 同步任务图编辑。
3. 组件级系统组装。
4. 连续物理环境的近似建模与接入。

### 机器可处理承载方式

机器可处理承载方式包括：

1. 工具内部的 task-set 数据结构。
2. XML 文件存取。
3. 由 editor 生成并交给 simulator / analyzer / generator 的统一模型。
4. 生成的 Ada `.adb` 实现文件。

### 交换与互操作

互操作重点在工具内链路：

1. Java GUI 负责编辑与可视配置。
2. Python `libdrt` 负责分析算法。
3. Code generator 把模型映射到 Ada 运行时。
4. 论文还明确表示未来继续扩展到 `C` 代码生成。

## 配套基础设施

- 建模/编辑工具：Java 实现的 editor，支持 `DRT/SDRT` task-set 建模与 XML 存取。
- 解析/交换/元模型支持：统一模型可保存 / 载入 XML 文件。
- 仿真/执行支持：带优先级与 `EDF` 的可视 simulation，支持速度配置与运行展示。
- 验证/分析支持：可行性分析、静态优先级分析、精确响应时间分析、多处理器 workload partitioning。
- 代码生成/转换支持：Ada 代码生成，利用 Ada rendezvous 实现同步发布语义。
- 标准化或社区生态：围绕 `DRT/SDRT`、Java GUI、Python `libdrt` 与 Ada runtime 的研究型工具链；原文未给开放分发入口。

## 适用场景与需求前提

### 适用场景

适合既关心离散控制任务时序，又需要把分析、仿真与最终实现放到一条链上的 CPS / embedded-system 场景，例如带同步任务、调度分析和嵌入式部署要求的控制系统。

### 需求前提

1. 离散控制逻辑能自然表达为 `DRT/SDRT` 任务图。
2. 关键时序约束能写成 `WCET`、deadline 与最小释放间隔。
3. 若涉及物理对象，团队接受先做离散抽象和近似，而不是保留完整连续方程求解。

### 不适用或高成本场景

如果需求更像一般 reactive state machine、rich data statechart 或 dense-time theorem proving，`TIMES-Pro` 这条任务图工具链就不一定最合适。

## 与相邻形式主义的关系

相对 [a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)，那篇更接近 `UPPAAL` 式分析前端，本文则坚持 `DRT/SDRT` 任务图本体；相对 [modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md](../modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md)，`ModeGraph` 仍是状态机 / mode 语言，而本文更像任务调度图；相对 [state-machines-in-modelica/desc.md](../state-machines-in-modelica/desc.md)，后者补语言本体，本文补的是面向 CPS 设计与部署的工具平台。

## 与本研究的关系

### 对 Project 1 的价值

1. 它提示“控制系统状态机建模”不一定非要选择经典状态节点 + 迁移箭头，也可以选择任务图式中间表示。
2. 对带调度、响应时间和同步释放约束的需求，这种图式表示可能比普通状态机更贴近问题本体。
3. 同时它又保留了较强的工具化证据，说明这条路线不只是理论模型。

### 作为目标形式主义还是中间表示

更像某类实时控制需求的中间表示或专用目标语言，而不是覆盖面最广的统一终态形式主义。

### 对需求到模型生成的启发

1. 如果需求主体是任务释放、deadline、调度与同步，而不是丰富状态数据，那么直接生成任务图可能比强行生成普通状态机更自然。
2. 对部署导向场景，应尽早考虑“模型如何映射到实际运行时机制”，例如本文里的 Ada rendezvous。
3. 连续环境部分若无法精确保留，也要在生成阶段明确给出抽象假设，而不是把近似步骤藏起来。

### 现实限制

`TIMES-Pro` 的优势建立在 `DRT/SDRT` 这一路径的结构前提上，对一般交互式、层次化或富数据状态机问题覆盖有限。

## 重要的相关工作

1. [a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md](../a-modeling-framework-for-schedulability-analysis-of-distributed-avionics-systems/desc.md)：另一条面向时序 / 可调度性分析的模型化路线。
2. [modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md](../modegraph-modelica-library-for-embedded-control-based-on-mode-automata/desc.md)：面向嵌入式控制的 mode-automata 工具线。
3. [state-machines-in-modelica/desc.md](../state-machines-in-modelica/desc.md)：Modelica 中更偏语言本体的状态机路线。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🌡️ 物理 / 混成对象
- 所属领域：🌡️ CPS / 物理系统建模
- 形式主义：`DRT / SDRT / TIMES-Pro`
- 归类理由：主贡献是以 `DRT/SDRT` 为核心搭建 CPS 设计、分析、仿真与 Ada 部署工具链，而不是提出新的主干状态机家族。
