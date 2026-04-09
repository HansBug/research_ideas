# UltraDES：离散事件系统建模、分析与控制库 / UltraDES - A Library for Modeling, Analysis and Control of Discrete Event Systems

## 基本信息

- 标题：UltraDES - A Library for Modeling, Analysis and Control of Discrete Event Systems
- 中文标题：UltraDES：离散事件系统建模、分析与控制库
- 作者：Lucas V. R. Alves，Lucas R. R. Martins，Patrícia N. Pena
- 发表：*IFAC-PapersOnLine*，50(1):5831-5836，2017
- DOI：`10.1016/j.ifacol.2017.08.540`
- 链接：https://doi.org/10.1016/j.ifacol.2017.08.540
- 形式主义：`DES automata / supervisory control / UltraDES / .NET DFA library`
- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 论文角色：.NET-based DES modeling / analysis / supervisory-control library
- 工具/实现获取方式：论文明确给出 `UltraDES` 下载入口 `https://github.com/lacsed/ultrades`，并说明其基于 `.NET Framework` / `C#`，可被其他 `.NET` 语言调用。
- 标准/格式获取方式：核心承载对象是 `DeterministicFiniteAutomaton`、事件/状态/转移类、`XML/ADS/Wmod/DOT` I/O 与 supervisor synthesis API；它不是标准化交换格式，而是库级基础设施。

## 简报

这篇论文的重点，不是提出新的 DES 理论，而是把离散事件系统领域最常用的 automata、composition、analysis 和 supervisory-control 例程，整理成一个可直接进入工业软件栈的 `.NET` 库。相对很多只停留在研究原型或脚本环境的工具，`UltraDES` 特别强调 object-oriented data structures、跨 `.NET` 语言复用和与工业通信模式的兼容性。

- 形式主义定位：这是 `DES / supervisory control` 的库级基础设施，不是新的 automata 母型。
- 构造方式简述：以状态、事件、转移和 regular expressions 为基本类，再围绕 `DeterministicFiniteAutomaton` 提供 composition、trim、monolithic/local modular supervisor synthesis 等方法。
- 基础设施与场景简述：依托 `C#`、`.NET Framework`、`XML/ADS/Wmod` I/O、bit-sequence state encoding 与 `Nadzoru/TCT/Supremica` 对照测试，服务工业 `DES` 建模与控制综合。

```text
DES automata/classes -> DFA operations and composition -> supervisor synthesis -> XML/ADS/Wmod/DOT export -> industrial or research workflow
```

## 形式主义定义与核心对象

### 定义对象

论文围绕以下对象组织：

1. regular languages 与 finite automata；
2. `DeterministicFiniteAutomaton` 数据结构；
3. plants / specifications / supervisors；
4. monolithic 与 local modular supervisor synthesis；
5. `.NET` 生态下的序列化、互操作与可视化输出。

### 核心抽象

论文从标准 `NFA/DFA` 骨架出发。其 automaton 可保守写成：

$$
G = (\Sigma, Q, \to, Q_0, Q_m)
$$

上式中的符号逐项解释如下：

1. `\Sigma` 是事件字母表。
2. `Q` 是有限状态集合。
3. `\to` 是转移关系。
4. `Q_0` 是初始状态集合；若是 `DFA`，则其大小为 `1`。
5. `Q_m` 是标记状态集合。

论文同时强调 `DES` 的 supervisory-control 视角。闭环语言关系可保守写成：

$$
L_m(S/G)=L(G)\cap E = K
$$

上式中的符号逐项解释如下：

1. `G` 是 plant。
2. `E` 是 specification automaton。
3. `S` 是 supervisor。
4. `L(G)` 是 plant 生成语言。
5. `L_m(S/G)` 是闭环标记语言。
6. `K` 是希望实现的合法行为。

非阻塞 supervisor 存在的关键条件可保守写成：

$$
K\Sigma_{nc}\cap L(G) \subseteq K
$$

上式中的符号逐项解释如下：

1. `\Sigma_{nc}` 是 uncontrollable events 集。
2. 上式表达 `K` 相对于 plant 与不可控事件的 controllability。
3. 若 `K` 不可控，则要改求 supremal controllable sublanguage。
4. 这正是论文中 `MonolithicSupervisor` 例程所服务的理论骨架。

### 一个最小例子与通俗解释

论文给的例子很直白：用类和 API 直接拼 automaton。

1. 先创建状态 `s1,s2` 和事件 `e1,e2`。
2. 再用 `Transition(s1,e1,s2)` 这类对象构造 `DeterministicFiniteAutomaton`。
3. 然后直接调用 `ParallelCompositionWith`、`Trim` 或 `MonolithicSupervisor`。
4. 最后还能导出到 `XML`、`ADS`、`Wmod` 或 `DOT`。

通俗地说，`UltraDES` 就像把 DES 领域常见的“理论算法 + 工具互转 + 性能优化”一起封装成可编程积木，而不是让研究者每做一个实验就重写一遍 automaton container。

### 运行 / 接受 / 转移语义

论文采用标准 DES 语义：

1. automaton `G` 同时实现生成语言 `L(G)` 与标记语言 `L_m(G)`。
2. `AccessiblePart`、`CoaccessiblePart` 与 `Trim` 分别对应标准可达、可共达和修剪。
3. 系统整体通常由多个子 plant 并行组合：

$$
G = \parallel_{i=1}^{n} G_i
$$

4. 规格也可由多个局部规格并行组合：

$$
E = \parallel_{j=1}^{m} E_j
$$

对局部模块化控制，论文给出：

$$
R_i = \mathrm{SupConNB}(H_i, D_i)
$$

其中：

1. `H_i` 是与第 `i` 个规格相关的 modular plant。
2. `D_i` 是第 `i` 个局部 specification。
3. `\mathrm{SupConNB}` 是求 nonblocking supervisor 的核心例程。
4. `R_i` 是得到的 local supervisor。

### 语义边界

这篇论文的边界也很清楚：

1. 核心对象是 `DFA` 风格 DES，而不是 timed/hybrid/probabilistic 全家桶。
2. timed、局部模块化等能力是扩展方向，但母线仍是 supervisory-control automata 库。
3. 论文重点在库设计和工程实现，不在新理论证明。
4. 它是 library-first，而不是 full IDE-first。

### 关键性质与判定边界

| 问题 / 性质 | 形式化写法 | 原文意义 |
|---|---|---|
| automaton 骨架 | `$G=(\Sigma,Q,\to,Q_0,Q_m)$` | `UltraDES` 以标准 automata 数据结构为核心。 |
| 闭环目标 | `$L_m(S/G)=L(G)\cap E=K$` | 监督控制要实现合法行为。 |
| controllability 条件 | `$K\Sigma_{nc}\cap L(G)\subseteq K$` | 非阻塞 supervisor 存在的关键约束。 |
| 并行组合 | `$G=\parallel_{i=1}^{n}G_i$` | 库需要高效支持多个 plants/specs 组合。 |

## 关键特性

| 维度 | 支持情况 | 说明 |
|---|---|---|
| 状态 / 模式 | 很强 | automata states 和 compound states 是核心类。 |
| 事件 / 触发 | 很强 | controllable / uncontrollable 事件是一等对象。 |
| 守卫 / 数据 | 弱支持 | 主要是有限离散事件，不是富数据 guard language。 |
| 层次 | 弱支持 | 主体不是层次状态机，而是 automata / composition。 |
| 并发 / 同步 | 很强 | parallel composition 和 supervisor synthesis 是主轴。 |
| 时间约束 | 弱支持 | 论文核心版本不是 timed DES；重点在离散监督控制。 |
| 连续动态 / 随机性 | 不支持 | 不在主线。 |
| 可执行 / 可验证性 | 很强 | 可直接调用库 API、导出格式并进行性能测试。 |

### 形式化问题与性质

1. 论文关注的是“如何把 DES 领域常见对象和算法组织成高性能、可复用、可工业接入的库”。
2. 与很多只支持单一研究算法的工具相比，`UltraDES` 更强调数据结构、互操作与内存表现。
3. 其 monolithic supervisor 算法特别强调避免显式构造中间 automaton `K`。

## 构造方式与承载格式

### 建模入口

典型入口包括：

1. 状态、事件、转移和 regular expression 类；
2. `DeterministicFiniteAutomaton`；
3. plant/specification lists；
4. `MonolithicSupervisor` 与 `LocalModularSupervisor` API。

### 承载格式

机器可处理承载方式包括：

1. `XML` 文件；
2. `ADS` 文件，用于 `TCT`；
3. `Wmod` 文件，用于 `Supremica`；
4. binary serialization；
5. `DOT` 可视化文本。

### 交换与互操作

这条路线的互操作重点在：

1. `.NET` 生态内可被多语言调用；
2. 可与 `TCT`、`Supremica` 互转；
3. 支持 `DOT/Graphviz` 可视化；
4. 论文实验还把模型在 `UltraDES`、`TCT` 和 `Supremica` 间交叉转换比对。

## 配套基础设施

- 建模/编辑工具：`C#/.NET` API、object-oriented automata classes。
- 解析/交换/元模型支持：`ToXMLFile/FromXMLFile`、`ToAdsFile/FromAdsFile`、`ToWmodFile/FromWmodFile`、binary serialization。
- 仿真/执行支持：核心不是仿真器，而是 automata operations 和 supervisor synthesis。
- 验证/分析支持：composition、accessible/coaccessible/trim、monolithic/local modular supervisors。
- 代码生成/转换支持：重点是格式导出和互操作，不是 PLC 代码生成主论文。
- 标准化或社区生态：论文给出 GitHub 仓库，并明确面向工业 `.NET` 软件栈。

## 适用场景与需求前提

### 适用场景

适合以下场景：

1. 工业离散事件控制系统的监督器综合。
2. 需要在 `.NET` 生态里直接调用 DES 算法的项目。
3. 需要在 `UltraDES`、`TCT`、`Supremica` 等工具之间交换 automata 模型。

### 需求前提

1. 系统需能落成 `DES/DFA` 风格 plant-specification 建模。
2. 关键问题要围绕 controllability、nonblocking 和 composition。
3. 团队接受 library/API 工作方式，而不是只依赖图形 IDE。
4. 工业软件栈最好已经与 `.NET` 兼容。

### 不适用或高成本场景

如果模型主体是连续动力学、丰富数据更新或复杂 timed semantics，这篇条目的直接收益会明显下降。

## 与相邻形式主义的关系

相对 [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)，两者都属于 supervisory-control 库级基础设施，但 `libFAUDES` 偏 `C++/Lua` 研究生态，而 `UltraDES` 更强调 `.NET/C#` 与工业接入。相对 [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)，`Supremica` 更像完整 IDE/workbench，`UltraDES` 更像库型底座。相对 [applying-a-software-framework-for-supervisory-control-of-a-plc-based-discrete-event-system/desc.md](../applying-a-software-framework-for-supervisory-control-of-a-plc-based-discrete-event-system/desc.md)，那篇偏 supervisor 落地到 PLC 的执行框架，这篇偏 DES 算法与模型承载基础设施。

## 与本研究的关系

### 对 Project 1 的价值

它说明在 `FSM / supervisory-control` 方向，文库不能只收模型本体，还需要能真正承载组合、综合、导出与工程互操作的库层资产。

### 作为目标形式主义还是中间表示

更像建模/综合基础设施，而不是研究最终要生成的前端语言。

### 对需求到模型生成的启发

1. 若 LLM 生成的是 `DES` 控制模型，最好同时保留 controllable / uncontrollable 事件划分。
2. 中间表示若能稳定映射到库 API 和交换格式，后续验证与部署更顺畅。
3. 工具链选型不一定非要 IDE，library-first 也能成为很强的基础设施节点。

### 现实限制

论文篇幅较短，更多展示的是库骨架、接口和性能概况，而不是完整工业流程方法论。

## 重要的相关工作

1. [libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md](../libfaudes-an-open-source-cpp-library-for-discrete-event-systems/desc.md)：`C++` 生态的 DES/supervisory-control 库型条目。
2. [supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md](../supremica-an-efficient-tool-for-large-scale-discrete-event-systems/desc.md)：更偏 workbench/IDE 的大规模 DES 工具。
3. [applying-a-software-framework-for-supervisory-control-of-a-plc-based-discrete-event-system/desc.md](../applying-a-software-framework-for-supervisory-control-of-a-plc-based-discrete-event-system/desc.md)：把 supervisory-control 进一步接到 PLC 落地链路的执行框架条目。

## 文献分类总结

- 主类：📦 标准、交换格式、元模型与执行载体
- 对象类型：🏗️ 标准/基础设施
- 描述客体：🎛️ 控制 / 反应式逻辑
- 所属领域：🏭 工业控制与自动化
- 形式主义：`DES automata / supervisory control / UltraDES / .NET DFA library`
- 论文角色：.NET-based DES modeling / analysis / supervisory-control library
- 归类理由：论文主体完全落在库级基础设施设计、互操作、数据结构和 supervisor synthesis API 上，明显属于 `FSM/EFSM/supervisory-control` 支线的 `🏗️` 条目。
